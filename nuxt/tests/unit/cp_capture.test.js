import { describe, it, expect, vi } from 'vitest'
import { saveThenTransition } from '~/utils/cp_capture.js'

// task-174: el primer guardado de un grupo «Por iniciar» ya lo promueve a
// «En llenado»; el POST de esa misma transición volvía 400.
describe('saveThenTransition', () => {
  const filling = { name: 'cp_filling', public_name: 'En llenado' }

  function setup(statusAfterSave) {
    const group = { status: 'cp_pre_start' }
    const save = vi.fn(async () => {
      group.status = statusAfterSave
      return true
    })
    const select = vi.fn(async (t) => ({ to_status: t.name }))
    const deps = { dirty: true, save, select, status: () => group.status }
    return { deps, save, select }
  }

  it('skips the POST when the save already reached the target', async () => {
    const { deps, save, select } = setup('cp_filling')
    const res = await saveThenTransition(filling, deps)
    expect(save).toHaveBeenCalledOnce()
    expect(select).not.toHaveBeenCalled()
    expect(res).toMatchObject({ done: true, skipped: true })
  })

  it('still transitions when the save left another status', async () => {
    const { deps, select } = setup('cp_pre_start')
    const res = await saveThenTransition(filling, deps)
    expect(select).toHaveBeenCalledWith(filling)
    expect(res.done).toBe(true)
  })
})
