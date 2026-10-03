// Transcripción de api/flow/seed.py (STATUSES + NEXT_STATUSES) con solo los
// campos que leen los getters del store: role, group, priority,
// applicable_models y next_statuses. Si el seed cambia, esto también.
const P = ['example', 'goodpracticepackage']
const GP = ['example', 'goodpractice']
const A = ['survey', 'axisvalue']
const O = ['answer', 'observableresponse']
const G = ['answer', 'groupresponse']
const GPK = ['survey', 'generalpackage']
const GEN = ['survey', 'generalgroupresponse']

// [name, role, applies, priority, next_statuses]
const ROWS = {
  bp: [
    ['bp_draft', 'ies', [P, GP], 50,
      ['bp_completed', 'bp_sent', 'bp_discarded']],
    ['bp_completed', 'reviewer', [GP], 60,
      ['bp_need_changes', 'bp_for_ruling', 'bp_rejected']],
    ['bp_sent', 'reviewer', [P], 75, ['bp_finished', 'bp_need_changes']],
    ['bp_adjusted', 'reviewer', [GP], 80,
      ['bp_need_changes', 'bp_for_ruling', 'bp_rejected']],
    ['bp_resent', 'reviewer', [P], 78, ['bp_finished', 'bp_need_changes']],
    ['bp_for_ruling', null, [GP], 30, []],
    ['bp_finished', null, [P], 10, []],
    ['bp_need_changes', 'ies', [P, GP], 90,
      ['bp_adjusted', 'bp_resent', 'bp_discarded']],
    ['bp_rejected', null, [GP], 20, []],
    ['bp_discarded', 'ies', [P, GP], 15, ['bp_draft']],
  ],
  cp: [
    ['cp_pre_start', 'ies', [A, O, G], 35, ['cp_filling']],
    ['cp_filling', 'ies', [A, O, G], 50,
      ['cp_completed', 'cp_sent', 'cp_postponed', 'cp_partial']],
    ['cp_completed', 'reviewer', [O, G], 60,
      ['cp_approved', 'cp_need_changes']],
    ['cp_sent', 'reviewer', [A], 75, ['cp_in_review']],
    ['cp_in_review', 'reviewer', [A], 72,
      ['cp_approved', 'cp_need_changes']],
    ['cp_need_changes', 'ies', [A, O, G], 90, ['cp_in_adjustment']],
    ['cp_in_adjustment', 'ies', [A, O, G], 70,
      ['cp_adjusted', 'cp_resent', 'cp_postponed']],
    ['cp_adjusted', 'reviewer', [O, G], 80,
      ['cp_approved', 'cp_need_changes']],
    ['cp_resent', 'reviewer', [A], 78, ['cp_in_review']],
    ['cp_postponed', 'ies', [O, G], 40, ['cp_completed', 'cp_partial']],
    ['cp_voluntary_readjust', 'reviewer', [A, O, G], 85,
      ['cp_need_changes']],
    ['cp_partial', 'reviewer', [O, G], 65,
      ['cp_need_changes', 'cp_partial_approved']],
    ['cp_partial_approved', 'ies', [O, G], 55,
      ['cp_completed', 'cp_partial']],
    ['cp_approved', 'ies', [A, O, G], 10, ['cp_voluntary_readjust']],
    ['cp_not_present', null, [O, G], 20, []],
  ],
  gen: [
    ['gen_draft', 'ies', [GPK, GEN], 50, ['gen_completed', 'gen_sent']],
    ['gen_completed', 'reviewer', [GEN], 60,
      ['gen_need_changes', 'gen_approved']],
    ['gen_sent', 'reviewer', [GPK], 75, ['gen_finished', 'gen_need_changes']],
    ['gen_need_changes', 'ies', [GPK, GEN], 90,
      ['gen_adjusted', 'gen_resent']],
    ['gen_adjusted', 'reviewer', [GEN], 80,
      ['gen_need_changes', 'gen_approved']],
    ['gen_resent', 'reviewer', [GPK], 78,
      ['gen_finished', 'gen_need_changes']],
    ['gen_approved', null, [GEN], 15, []],
    ['gen_finished', null, [GPK], 10, []],
  ],
}

// Catálogo como lo guarda el store (`byName`), sin `admin_targets`: así se
// ejercita el respaldo que deriva los destinos del grafo.
export function seedCatalog() {
  const map = {}
  for (const [group, rows] of Object.entries(ROWS)) {
    for (const [name, role, applies, priority, next] of rows) {
      map[name] = {
        name, group, role, priority,
        applicable_models: applies, next_statuses: next,
      }
    }
  }
  return map
}
