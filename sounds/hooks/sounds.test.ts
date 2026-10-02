import { expect, test } from 'claude-code/testing'

const FLAG = '/Users/acarril/.claude/hooks/.sounds'

test('/sounds toggles bare and sets with on|off', async ($, on) => {
  const files = new Map<string, string>([[FLAG, 'on\n']])
  on('fs.read', async (_, e) => ({ value: files.get(e.path) ?? '' }))
  on('fs.write', async (_, e) => {
    files.set(e.path, e.text)
    return { value: undefined }
  })

  expect((await $.command.run({ command: 'sounds' })).text).toBe('Sounds off.')
  expect(files.get(FLAG)).toBe('off\n')
  expect((await $.command.run({ command: 'sounds' })).text).toBe('Sounds on.')
  expect(files.get(FLAG)).toBe('on\n')

  expect((await $.command.run({ command: 'sounds', args: 'off' })).text).toBe('Sounds off.')
  expect((await $.command.run({ command: 'sounds', args: 'off' })).text).toBe('Sounds off.')
  expect((await $.command.run({ command: 'sounds', args: 'on' })).text).toBe('Sounds on.')
  expect(files.get(FLAG)).toBe('on\n')

  expect((await $.command.run({ command: 'sounds', args: 'loud' })).text).toBe('Usage: /sounds [on|off]')
  expect(files.get(FLAG)).toBe('on\n')
})
