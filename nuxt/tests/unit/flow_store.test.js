import { describe, it, expect, vi } from 'vitest'
import { USERS, setupFlowStore } from './helpers/flow_store.js'
import { seedCatalog } from './helpers/flow_catalog.js'

vi.mock('~/store/index.js', () => import('./helpers/main_store_stub.js'))
vi.mock('~/store/ies', () => ({ useIesStore: () => ({}) }))

const usersById = Object.fromEntries(
  Object.values(USERS).map((u) => [u.id, u]))

describe('auth.is_admin', () => {
  it.each([
    ['superuser', true],
    ['staff', true],
    ['reviewer', false],
    ['ies', false],
  ])('%s → %s', (key, expected) => {
    const { auth } = setupFlowStore({ user: USERS[key] })
    expect(auth.is_admin).toBe(expected)
  })
})

describe('isAdminEvent', () => {
  const offGraph = { from_status: 'bp_for_ruling',
    to_status: 'bp_need_changes' }

  it('off-graph change with a comment is an admin event', () => {
    const { flow } = setupFlowStore()
    expect(flow.isAdminEvent({ ...offGraph, comment: 'error' })).toBe(true)
  })

  it('off-graph change without a comment is a domain write', () => {
    const { flow } = setupFlowStore()
    expect(flow.isAdminEvent({ ...offGraph, comment: '' })).toBe(false)
  })

  it('a legal edge with a comment is a normal transition', () => {
    const { flow } = setupFlowStore()
    const ev = { from_status: 'bp_completed', to_status: 'bp_rejected',
      comment: 'no cumple' }
    expect(flow.isAdminEvent(ev)).toBe(false)
  })

  it('a pure comment is not an admin event', () => {
    const { flow } = setupFlowStore()
    const ev = { from_status: null, to_status: null, comment: 'nota' }
    expect(flow.isAdminEvent(ev)).toBe(false)
  })
})

describe('getAdminTargets', () => {
  const names = (targets) => targets.map((t) => t.name).sort()

  it.each([
    ['bp_for_ruling', 'example', 'goodpractice',
      ['bp_adjusted', 'bp_completed', 'bp_need_changes', 'bp_rejected']],
    ['gen_approved', 'survey', 'generalgroupresponse',
      ['gen_adjusted', 'gen_completed', 'gen_need_changes']],
    ['cp_approved', 'answer', 'observableresponse',
      ['cp_adjusted', 'cp_completed', 'cp_need_changes', 'cp_partial',
        'cp_partial_approved']],
    ['cp_approved', 'answer', 'groupresponse',
      ['cp_adjusted', 'cp_completed', 'cp_need_changes', 'cp_partial',
        'cp_partial_approved']],
  ])('graph fallback from %s on %s.%s equals the seed set off-graph',
    (current, app, model, expected) => {
      const { flow } = setupFlowStore()
      const targets = flow.getAdminTargets(current, app, model)
      expect(names(targets)).toEqual(expected)
      const priorities = targets.map((t) => t.priority)
      expect(priorities).toEqual([...priorities].sort((a, b) => b - a))
    })

  it('per-status admin_targets wins over the graph', () => {
    const catalog = seedCatalog()
    catalog.bp_for_ruling.admin_targets = ['bp_need_changes', 'bp_rejected']
    const { flow } = setupFlowStore({ catalog })
    const targets = flow.getAdminTargets(
      'bp_for_ruling', 'example', 'goodpractice')
    expect(names(targets)).toEqual(['bp_need_changes', 'bp_rejected'])
  })

  it('excludes the current status and its next_statuses', () => {
    const { flow } = setupFlowStore()
    const targets = flow.getAdminTargets(
      'bp_completed', 'example', 'goodpractice')
    expect(names(targets)).toEqual(['bp_adjusted'])
  })

  it('subtracts next_statuses from per-status admin_targets too', () => {
    const catalog = seedCatalog()
    catalog.bp_completed.admin_targets = [
      'bp_completed', 'bp_adjusted', 'bp_need_changes', 'bp_for_ruling',
      'bp_rejected']
    const { flow } = setupFlowStore({ catalog })
    const targets = flow.getAdminTargets(
      'bp_completed', 'example', 'goodpractice')
    expect(names(targets)).toEqual(['bp_adjusted'])
  })
})

describe('canEditComment / eventSide', () => {
  const sent = { status: 'bp_sent' }
  const byReviewer = { user: USERS.reviewer.id, comment: 'nota' }

  function asReviewer() {
    return setupFlowStore({ user: USERS.reviewer, users: usersById }).flow
  }

  it('reviewer edits a reviewer-side event while the root is theirs', () => {
    const flow = asReviewer()
    expect(flow.eventSide(byReviewer)).toBe('reviewer')
    expect(flow.canEditComment(byReviewer, sent)).toBe(true)
  })

  it('not once the root is in the IES turn', () => {
    const flow = asReviewer()
    expect(flow.canEditComment(byReviewer, { status: 'bp_need_changes' }))
      .toBe(false)
  })

  it('not with a terminal root', () => {
    const flow = asReviewer()
    expect(flow.canEditComment(byReviewer, { status: 'bp_finished' }))
      .toBe(false)
  })

  it('not on an event of the other side', () => {
    const flow = asReviewer()
    const byIes = { user: USERS.ies.id, comment: 'respuesta' }
    expect(flow.eventSide(byIes)).toBe('ies')
    expect(flow.canEditComment(byIes, sent)).toBe(false)
  })

  it('an author missing from the catalog counts as reviewer', () => {
    const flow = asReviewer()
    const byUnknown = { user: 999, comment: 'staff' }
    expect(flow.eventSide(byUnknown)).toBe('reviewer')
    expect(flow.canEditComment(byUnknown, sent)).toBe(true)
  })
})

describe('canEditComment: current round only', () => {
  const at = (minute) => `2026-10-02T10:${String(minute).padStart(2, '0')}:00Z`
  const move = (from, to, minute) => ({ from_status: from, to_status: to,
    created_at: at(minute), user: USERS.ies.id })
  // bp_sent (1) → bp_need_changes (3) → bp_resent (5)
  const root = { status: 'bp_resent', flow_events: [
    move('bp_draft', 'bp_sent', 1),
    move('bp_sent', 'bp_need_changes', 3),
    move('bp_need_changes', 'bp_resent', 5),
  ] }
  const note = (minute, user = USERS.reviewer.id) => (
    { user, comment: 'nota', created_at: at(minute) })

  function as(user) {
    return setupFlowStore({ user, users: usersById }).flow
  }

  it('reviewer: a comment of the first round is frozen', () => {
    expect(as(USERS.reviewer).canEditComment(note(2), root)).toBe(false)
  })

  it('reviewer: a comment after the root came back is editable', () => {
    expect(as(USERS.reviewer).canEditComment(note(6), root)).toBe(true)
  })

  it('IES: only what was written after bp_need_changes', () => {
    const iesRoot = { ...root, status: 'bp_need_changes',
      flow_events: root.flow_events.slice(0, 2) }
    const flow = as(USERS.ies)
    expect(flow.canEditComment(note(0, USERS.ies.id), iesRoot)).toBe(false)
    expect(flow.canEditComment(note(4, USERS.ies.id), iesRoot)).toBe(true)
  })

  it('a root that never changed side keeps every comment editable', () => {
    const flow = as(USERS.ies)
    const draft = { status: 'bp_draft', flow_events: [] }
    expect(flow.canEditComment(note(0, USERS.ies.id), draft)).toBe(true)
  })

  it('a root without flow_events falls back to turn and side', () => {
    expect(as(USERS.reviewer).canEditComment(note(2), { status: 'bp_resent' }))
      .toBe(true)
  })
})

describe('canEditComment: admin reason', () => {
  const root = { status: 'bp_sent' }
  const reason = { from_status: 'bp_for_ruling',
    to_status: 'bp_need_changes', comment: 'error', user: USERS.staff.id }

  it('a reviewer without admin cannot edit it', () => {
    const flow = setupFlowStore({ user: USERS.reviewer, users: usersById })
      .flow
    expect(flow.canEditComment(reason, root)).toBe(false)
  })

  it('an admin account can', () => {
    const flow = setupFlowStore({ user: USERS.staff, users: usersById }).flow
    expect(flow.canEditComment(reason, root)).toBe(true)
  })
})

describe('getAdminRootBlock', () => {
  it('open when the root is on the reviewer side', () => {
    const { flow } = setupFlowStore()
    expect(flow.getAdminRootBlock({ status: 'bp_sent' })).toEqual([])
  })

  it('names the root not_sent_message while in the IES turn', () => {
    const { flow } = setupFlowStore()
    const root = { status: 'bp_need_changes', not_sent_message: 'Aún no' }
    expect(flow.getAdminRootBlock(root)).toEqual(['Aún no'])
  })

  it('falls back to a generic text without not_sent_message', () => {
    const { flow } = setupFlowStore()
    const reasons = flow.getAdminRootBlock({ status: 'bp_draft' })
    expect(reasons).toHaveLength(1)
    expect(reasons[0]).toMatch(/no ha enviado/)
  })

  it('reports a closed root as closed', () => {
    const { flow } = setupFlowStore()
    const reasons = flow.getAdminRootBlock({ status: 'bp_finished' })
    expect(reasons).toHaveLength(1)
    expect(reasons[0]).toMatch(/cerrado/)
  })
})
