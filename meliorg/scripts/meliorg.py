#!/usr/bin/env python3
"""Query MercadoLibre's org chart through the Grid API.

Grid resolves identity at the edge, so requests carry no auth headers -- you
just need the corporate VPN (or Fury/Swarm with GRID_HOST set).

Three primitives back everything here:
  GET  /api/v1/me                 -> your own record, incl. manager_username
  GET  /api/v1/people/search?q=   -> any person + manager_username (upward)
  POST /api/v1/engine/run/json    -> "reportes de <X>" dry-run (downward)

The engine call is a dry-run: share_with with no file/doc_id/slack_to resolves
recipients and grants nothing. Omitting skill_version skips the version check
entirely -- do not send one (skip_version_check does not rescue a stale value).

Answers are cached for 7 days at ~/.cache/meliorg.json. Off-VPN, the cache is
served with a staleness marker rather than failing; --json always reports it in
the envelope, and a banner goes to stderr.

Usage:
    meliorg.py whoami
    meliorg.py find "Ignacio Campos" [--limit N]
    meliorg.py chain [username]
    meliorg.py reports <username>
    meliorg.py peers [username]
    meliorg.py tree <username> [--depth 2] [--enrich]
    ... plus --json on any subcommand, and --refresh to bypass the cache.

    from meliorg import whoami, manager_chain, reports, peers, tree
"""

import argparse
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HOST = os.environ.get("GRID_HOST", "https://grid.melioffice.com")
CACHE_PATH = os.path.expanduser("~/.cache/meliorg.json")
CACHE_TTL = 7 * 24 * 3600
RATE_LIMIT = 50  # Grid allows 60/min per user; leave headroom.
MAX_DEPTH = 4  # tree() costs one request per node -- refuse to crawl the company.

REFRESH = False
_cache = None
_calls = []
_stale = {}


class GridError(RuntimeError):
    def __init__(self, message, offline=False):
        super().__init__(message)
        self.offline = offline


def _load_cache():
    global _cache
    if _cache is None:
        try:
            _cache = json.load(open(CACHE_PATH))
        except (OSError, json.JSONDecodeError):
            _cache = {}
    return _cache


def _cached(key, produce):
    """Serve fresh cache, else fetch. If the fetch fails because we are offline
    and any cached value exists, serve it and record how old it is."""
    cache = _load_cache()
    entry = cache.get(key)
    if entry and not REFRESH and time.time() - entry["at"] < CACHE_TTL:
        return entry["value"]
    try:
        value = produce()
    except GridError as error:
        if error.offline and entry:
            _stale[key] = entry["at"]
            return entry["value"]
        raise
    cache[key] = {"at": time.time(), "value": value}
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as handle:
        json.dump(cache, handle)
    return value


def stale_as_of():
    """ISO date of the oldest stale entry served this run, or None."""
    if not _stale:
        return None
    oldest = min(_stale.values())
    return datetime.datetime.fromtimestamp(oldest).isoformat(timespec="seconds")


def _throttle():
    now = time.time()
    _calls[:] = [t for t in _calls if now - t < 60]
    if len(_calls) >= RATE_LIMIT:
        time.sleep(60 - (now - _calls[0]) + 0.5)
    _calls.append(time.time())


def _request(path, data=None):
    _throttle()
    headers = {"Content-Type": "application/json"} if data else {}
    body = json.dumps(data).encode() if data else None
    try:
        with urllib.request.urlopen(
            urllib.request.Request(HOST + path, body, headers), timeout=30
        ) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")[:400]
        if error.code == 401:
            raise GridError("401 from Grid -- is the corporate VPN up?", offline=True)
        if error.code == 429:
            time.sleep(int(error.headers.get("Retry-After", 30)))
            return _request(path, data)
        raise GridError("HTTP %d from %s: %s" % (error.code, path, detail))
    except urllib.error.URLError as error:
        raise GridError("cannot reach %s (%s)" % (HOST, error.reason), offline=True)


def whoami():
    """Your own directory record, including manager_username."""
    return _cached("me", lambda: _request("/api/v1/me"))


def find_person(query, limit=10):
    """Search by full name or LDAP. Title and department are NOT searchable."""
    qs = urllib.parse.urlencode({"q": query, "limit": limit})

    def fetch():
        return _request("/api/v1/people/search?" + qs).get("people", [])

    return _cached("search:%s:%d" % (query.lower(), limit), fetch)


def get_person(username):
    """Exact record for an LDAP username, or None."""
    for person in find_person(username, limit=50):
        if person.get("username") == username:
            return person
    return None


def manager_chain(username=None):
    """Walk from a person up to the root. Returns records, person first."""
    person = whoami() if username is None else get_person(username)
    if person is None:
        raise GridError("no such user: %s" % username)
    chain, seen = [person], {person["username"]}
    while person.get("manager_username"):
        nxt = person["manager_username"]
        if nxt in seen:  # defensive: the directory should be acyclic
            break
        person = get_person(nxt)
        if person is None:
            break
        seen.add(person["username"])
        chain.append(person)
    return chain


def _resolve(keyword):
    """Dry-run the engine's people resolution. No file/doc_id/slack_to means
    nothing is shared -- we only read back resolved_recipients."""

    def fetch():
        response = _request("/api/v1/engine/run/json", {"share_with": [keyword]})
        # A >10-recipient result comes back as confirmation_required with
        # ok:false, but resolved_recipients is populated either way.
        return response.get("data", {}).get("resolved_recipients", [])

    return _cached("resolve:" + keyword.lower(), fetch)


def reports(username):
    """Direct reports of a person (1 level)."""
    return _resolve("reportes de %s" % username)


def peers(username=None):
    """People sharing a direct manager."""
    return _resolve("mis pares" if username is None else "pares de %s" % username)


def tree(username=None, depth=2, enrich=False):
    """BFS the subtree under a person. Returns {username: record}, each with a
    "reports" list and a "depth". Costs one request per node (two with enrich),
    so depth is capped at MAX_DEPTH -- this cannot enumerate the company."""
    if depth > MAX_DEPTH:
        raise GridError("depth %d exceeds MAX_DEPTH %d" % (depth, MAX_DEPTH))
    root = whoami() if username is None else get_person(username)
    if root is None:
        raise GridError("no such user: %s" % username)
    nodes, queue = {}, [(root, 0)]
    while queue:
        person, level = queue.pop(0)
        name = person["username"]
        if name in nodes:
            continue
        person = dict(person, depth=level, reports=[])
        nodes[name] = person
        if level >= depth:
            continue
        for child in reports(name):
            person["reports"].append(child["username"])
            if enrich:
                child = get_person(child["username"]) or child
            queue.append((child, level + 1))
    return nodes


def _print_tree(nodes, username, indent=0):
    person = nodes[username]
    print("%s%s  %s  %s" % ("  " * indent, username,
                            person.get("full_name", ""), person.get("title", "")))
    for child in person.get("reports", []):
        _print_tree(nodes, child, indent + 1)


def main():
    global REFRESH
    # Shared flags go on a parent parser so they work on either side of the
    # subcommand -- plain global flags would only parse before it.
    common = argparse.ArgumentParser(add_help=False)
    # SUPPRESS: without it the subparser's default would clobber a value the
    # parent already parsed, so flags would work on only one side.
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help='envelope: {"stale_as_of": null|iso, "data": ...}')
    common.add_argument("--refresh", action="store_true",
                        default=argparse.SUPPRESS, help="bypass the cache")

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                     parents=[common])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("whoami", parents=[common])
    find = sub.add_parser("find", parents=[common])
    find.add_argument("query")
    find.add_argument("--limit", type=int, default=10)
    chain = sub.add_parser("chain", parents=[common])
    chain.add_argument("username", nargs="?")
    rep = sub.add_parser("reports", parents=[common])
    rep.add_argument("username")
    prs = sub.add_parser("peers", parents=[common])
    prs.add_argument("username", nargs="?")
    tre = sub.add_parser("tree", parents=[common])
    tre.add_argument("username", nargs="?")
    tre.add_argument("--depth", type=int, default=2)
    tre.add_argument("--enrich", action="store_true", help="fetch title per node")
    args = parser.parse_args()
    REFRESH = getattr(args, "refresh", False)
    as_json = getattr(args, "json", False)

    nodes = None
    try:
        if args.command == "whoami":
            result = whoami()
        elif args.command == "find":
            result = find_person(args.query, args.limit)
        elif args.command == "chain":
            result = manager_chain(args.username)
        elif args.command == "reports":
            result = reports(args.username)
        elif args.command == "peers":
            result = peers(args.username)
        elif args.command == "tree":
            nodes = tree(args.username, args.depth, args.enrich)
            result = nodes
    except GridError as error:
        sys.exit("meliorg: %s" % error)

    stale = stale_as_of()
    if stale:
        sys.stderr.write(
            "meliorg: OFFLINE -- served from cache, as of %s. Not live.\n" % stale)

    if as_json:
        print(json.dumps({"stale_as_of": stale, "data": result}, indent=2))
    elif nodes is not None:
        root = min(nodes.values(), key=lambda p: p["depth"])["username"]
        _print_tree(nodes, root)
    elif isinstance(result, dict):
        print(json.dumps(result, indent=2))
    else:
        for person in result:
            print("%-16s %-34s %s" % (person.get("username", ""),
                                      person.get("full_name", ""),
                                      person.get("title", person.get("email", ""))))


if __name__ == "__main__":
    main()
