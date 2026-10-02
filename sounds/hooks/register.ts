import type { EngineInterface, Register } from 'claude-code'

// Read by ~/.claude/hooks/claude-notify.py: "off" silences play().
const FLAG = '/Users/acarril/.claude/hooks/.sounds'

const isOff = async ($: EngineInterface) =>
  (await $.fs.read(FLAG).catch(() => 'on')).trim() === 'off'

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'sounds', description: 'Toggle notification sounds (or: /sounds on|off)' })
    $.ui.status((await isOff($)) ? 'sounds off' : undefined)

    return next(e)
  })

  on('command.run', { command: 'sounds' }, async ($, e) => {
    const arg = (e.args ?? '').trim().toLowerCase()
    if (arg !== '' && arg !== 'on' && arg !== 'off') return { text: 'Usage: /sounds [on|off]' }
    const off = arg === '' ? !(await isOff($)) : arg === 'off'
    await $.fs.write(FLAG, off ? 'off\n' : 'on\n')
    $.ui.status(off ? 'sounds off' : undefined)

    return { text: off ? 'Sounds off.' : 'Sounds on.' }
  })
}
