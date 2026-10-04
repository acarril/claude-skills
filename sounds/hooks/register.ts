import type { EngineInterface, Register } from 'claude-code'

// Read by ~/.claude/hooks/claude-notify.py: "off" silences play().
const FLAG = '/Users/acarril/.claude/hooks/.sounds'
// Shown among the footer's mode labels: U+266A (a note) while on, struck through (+ U+0336) while off.
const ON_LABEL = '\u266a'
const OFF_LABEL = '\u266a\u0336'

const isOff = async ($: EngineInterface) =>
  (await $.fs.read(FLAG).catch(() => 'on')).trim() === 'off'

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'sounds', description: 'Toggle notification sounds (or: /sounds on|off)' })
    // Clears the status row an earlier version set.
    $.ui.status(undefined)

    return next(e)
  })

  on('command.run', { command: 'sounds' }, async ($, e) => {
    const arg = (e.args ?? '').trim().toLowerCase()
    if (arg !== '' && arg !== 'on' && arg !== 'off') return { text: 'Usage: /sounds [on|off]' }
    const off = arg === '' ? !(await isOff($)) : arg === 'off'
    await $.fs.write(FLAG, off ? 'off\n' : 'on\n')
    $.ui.invalidate('ui.render')

    return { text: off ? 'Sounds off.' : 'Sounds on.' }
  })

  // Read on each draw, so a /sounds run in another session shows here at the next redraw.
  on('ui.render', { component: 'SessionMode' }, async ($, e, next) =>
    next({ ...e, props: { ...e.props, modes: [...e.props.modes, (await isOff($)) ? OFF_LABEL : ON_LABEL] } }),
  )
}
