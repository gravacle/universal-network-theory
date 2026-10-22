"""CHECK_V001 K02 (independent checker, Claude2 lane): adversarial tests of the SEALED kmax_compare_c2v002.py
against the SEALED KMAX_MATRIX_PREREG_V002.json (real grids, real tau, real case table; no tiny-grid swap,
no monkeypatching of the compare module).  Normalized specs come from the drivers' own normalize_spec()
applied to the v002 spec/template bytes.  Masks are checked against both drivers' truncation_mask().
Synthetic speeds only (no observed velocity is read).  Nothing is launched.  numpy only, single thread.

usage: python3 -I -B k02_compare_adversarial_c2chk.py NEW_OUT_JSON SCRATCH_DIR
  SCRATCH_DIR: new directory for full-size mock packets of the end-to-end main() runs (large, temporary).
"""
import copy
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v002_c2')
PRE_P = D / 'KMAX_MATRIX_PREREG_V002.json'
PRE_SHA = '0024b63ecf9c4c4aa3b4ae88db3084b956c12760696b69963f4fa514354c9e10'
CMP_P = D / 'kmax_compare_c2v002.py'
CMP_SHA = 'e42336a70b644916428884860d4d657db11dfca5f86dec59c1de1650420059cf'
KPC = 3.085677581491367e19
OUT = []


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def load(path, sha, name):
    raw = Path(path).read_bytes()
    if sha_b(raw) != sha:
        raise SystemExit('REFUSED: %s sha mismatch' % path)
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def check(tid, cond, detail=None):
    OUT.append({'id': tid, 'pass': bool(cond), 'detail': detail})
    print(('PASS ' if cond else 'FAIL ') + tid + ('  ' + json.dumps(detail, default=str)[:260] if detail is not None else ''))


raw_pre = PRE_P.read_bytes()
assert sha_b(raw_pre) == PRE_SHA
PRE = json.loads(raw_pre)
cmp = load(CMP_P, CMP_SHA, 'cmp_sealed')
assert cmp.PREREG_SHA256 == PRE_SHA
DRV = {k: load(v['path'], v['sha256'], 'drv_' + k) for k, v in PRE['binding_inputs']['drivers'].items()}
DSHA = {k: v['sha256'] for k, v in PRE['binding_inputs']['drivers'].items()}
IDS = PRE['row_ids']
TAU = np.array(PRE['tau_km_s'])
SIG = np.array(PRE['quoted_sigma_km_s'])
CASES = {c['id']: c for c in PRE['cases']}

# ---------------------------------------------------------------- K02.1 prereg arithmetic
check('K02.1a tau_i == 0.25*sigma_i (root a)', np.allclose(TAU, 0.25 * SIG, rtol=0, atol=1e-15), TAU.tolist())
check('K02.1b tau_picard == 0.25*min tau_i == 0.0125', PRE['criterion']['tau_picard_km_s'] == 0.0125 and abs(0.25 * TAU.min() - 0.0125) < 1e-15)
try:
    sigsrc = json.loads(Path(PRE['binding_inputs']['sigma_source']['path']).read_bytes())
    sig_rows = [(r['id'], r['quoted_random_sigma_km_s']) for r in sigsrc['rows']]   # only these two fields are touched
    check('K02.1c sigma list equals sigma_source rows[*].quoted_random_sigma_km_s in row order',
          [x[0] for x in sig_rows] == IDS and [x[1] for x in sig_rows] == PRE['quoted_sigma_km_s'])
except Exception as exc:  # noqa
    check('K02.1c sigma list equals sigma_source', False, str(exc))
sigsrc = None
rb = json.loads(Path(PRE['binding_inputs']['row_binding']['path']).read_bytes())
check('K02.1d row ids equal row_binding query_rows ids', [x['id'] for x in rb['query_rows']] == IDS)
z = 2.865
check('K02.1e band shift tau/(z sigma)=8.73%; sum (tau/sigma)^2 = 0.75; cross term at r=+sigma = 6.0',
      abs(0.25 / z - 0.0873) < 5e-4 and abs(np.sum((TAU / SIG) ** 2) - 0.75) < 1e-12 and abs(2 * np.sum(SIG * TAU / SIG ** 2) - 6.0) < 1e-12)
v001_uniform = float(np.sum((0.05 / SIG) ** 2))
check('K02.1f INFO: V001 uniform tau=0.05 gave sum (tau/sigma)^2 = %.3f (stated bound 0.75); V002 per-row = 0.75 exactly' % v001_uniform, True,
      {'v001_actual': v001_uniform, 'v001_band_shift_row01': 0.05 / (z * 1.6), 'v002_band_shift_every_row': 0.25 / z})

# ---------------------------------------------------------------- K02.2 grids and masks vs both drivers
v003_decl = DRV['v003'].DECLARED_LARGE_GRIDS
for gid in ('G3', 'G4', 'GR'):
    gs = PRE['grids'][gid]['composite_grid_spec']
    b, o, t = v003_decl[gid]
    check('K02.2a %s registered grid == v003 DECLARED_LARGE_GRIDS' % gid, gs['breaks_inverse_kpc'] == b and gs['panel_orders'] == o and gs['total_axis_nodes'] == t == PRE['grids'][gid]['axis_nodes'])
v1pre = json.loads(Path(PRE['supersedes']['prereg']['path']).read_bytes())
check('K02.2b grid blocks equal V001 prereg grid blocks', all(json.dumps(PRE['grids'][g]['composite_grid_spec'], sort_keys=True) == json.dumps(v1pre['grids'][g]['composite_grid_spec'], sort_keys=True) for g in ('G2', 'G3', 'G4', 'GR')))
AX = {g: cmp.expected_axis(PRE['grids'][g]['composite_grid_spec']) for g in ('G2', 'G3', 'G4', 'GR')}
check('K02.2c axis lengths 72/84/96/92', [len(AX[g]) for g in ('G2', 'G3', 'G4', 'GR')] == [72, 84, 96, 92])
want_counts = {('G2', 'sphere'): 344048, ('G2', 'cylinder'): 362592, ('G3', 'sphere'): 525992, ('G3', 'cylinder'): 567504,
               ('G4', 'sphere'): 755080, ('G4', 'cylinder'): 834048}
for (gid, shp), n in want_counts.items():
    ax = AX[gid]
    k = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3)
    K = float(PRE['grids'][gid]['composite_grid_spec']['breaks_inverse_kpc'][-1]) if gid != 'G2' else 2.0
    m = cmp.driver_mask(k, shp, K / KPC)
    eq = all(np.array_equal(m, DRV[d].truncation_mask(k, shp, K / KPC).astype(bool)) for d in ('v001', 'v003'))
    check('K02.2d %s %s K=%g: compare mask == v001 and v003 truncation_mask bitwise; kept %d' % (gid, shp, K, n), eq and int(m.sum()) == n, int(m.sum()))
    del k

# ---------------------------------------------------------------- K02.3 driver normalize_spec on the v002 bytes
SPEC_FILES = {'C2': Path(PRE['binding_inputs']['anchor_base_spec']['path'])}
for c in ('C3', 'C4', 'R'):
    SPEC_FILES[c] = D / ('specs_anchor/v002/wave1/CALL_KMAX_%s_A2F3_C2V002.json' % c)
for c in ('S2', 'Y2', 'S3', 'Y3', 'S4', 'Y4'):
    SPEC_FILES[c] = D / ('specs_anchor/v002/templates/CALL_KMAX_%s_A2F3_C2V002.TEMPLATE.json' % c)
NS = {}
for cid, p in SPEC_FILES.items():
    s = json.loads(p.read_bytes())
    s['admit'] = {}          # admission is not part of V3; the PENDING placeholders would be refused by normalize_spec
    NS[cid] = {}
    for d in CASES[cid]['drivers_allowed']:
        NS[cid][d] = DRV[d].normalize_spec(copy.deepcopy(s))
check('K02.3a every case spec normalizes under each allowed driver', all(set(NS[c]) == set(CASES[c]['drivers_allowed']) for c in CASES))
check('K02.3b C2 bound call spec sha == registered (fe1ad000)', sha_b(SPEC_FILES['C2'].read_bytes()) == CASES['C2']['bound_call']['call_spec_sha256'])
same_12 = all(json.dumps(NS[c]['v001'], sort_keys=True) == json.dumps(NS[c]['v003'], sort_keys=True) for c in ('C2', 'S2', 'Y2'))
check('K02.3c G2 cases: v001 and v003 normalized specs identical', same_12)

BASEV = np.linspace(11.6, 50.9, 12)
RADIAL = [x * KPC for x in (0.2, 0.45, 1.0, 3.0, 5.9, 6.3, 12.8)]


def adapted(cid, speeds, m4=0.01, last=0.004, driver=None, passes=None, ident=None, status='COMPLETED', valid=True,
            ns_mod=None, rows=None):
    c = CASES[cid]
    if driver is None:
        driver = 'v001' if c['grid'] == 'G2' else 'v003'
    ns = copy.deepcopy(NS[cid].get(driver) or NS[cid][c['drivers_allowed'][0]])
    if passes is None:
        passes = 4 if cid == 'C2' else 6
    ns['numerics']['picard']['passes'] = passes
    if ns_mod:
        ns_mod(ns)
    if ident is None:
        ident = {'G2': 'a', 'G3': 'b', 'G4': 'c', 'GR': 'd'}[c['grid']] * 64
    rr = dict(zip(IDS, map(float, speeds))) if rows is None else rows
    return {'result_path': 'synthetic', 'result_sha256': None, 'schema': cmp.RESULT_SCHEMA, 'status': status, 'valid': valid,
            'reasons': [], 'driver_sha256': DSHA.get(driver, driver), 'call_spec_sha256': 'x' * 64, 'rows': rr,
            'normalized_spec': ns, 'grid_spec': ns['numerics']['composite_grid_spec'], 'truncation': ns['numerics']['truncation'],
            'picard': ns['numerics']['picard'], 'final_pass': 3, 'last_change_km_s': last, 'per_pass_rows': [],
            'field_packet': None, 'route_a_identity_sha256': ident, 'harm_m4_global': None, 'harm_m8_global': None,
            'm4_row_window': m4, 'base_K_values_SI': None, 'elapsed_seconds': 1.0}


GOODPK = {'V4': True, 'V5': True}
# per-shape sequences c_K (Dhat units: row offset = c_K * tau_i), m4 per shape at K=4
PLAN0 = {'cube': ((0.0, 2.0, 2.8), 0.020), 'sphere': ((0.0, 1.0, 1.3), 0.0090), 'cylinder': ((0.0, 1.2, 1.6), 0.0095)}
LET = {'cube': 'C', 'sphere': 'S', 'cylinder': 'Y'}


def build(plan=None, r_off=0.5, extra=None, drop=(), row_add=None):
    plan = plan or PLAN0
    ad = {}
    for shp, (cs, m4) in plan.items():
        for K, cK in zip((2, 3, 4), cs):
            cid = '%s%d' % (LET[shp], K)
            sp = BASEV + cK * TAU
            if row_add and cid in row_add:
                sp = sp + np.asarray(row_add[cid])
            ad[cid] = adapted(cid, sp, m4=m4 if K == 4 else 0.5, **((extra or {}).get(cid, {})))
    rsp = BASEV + plan['cube'][0][0] * TAU + (r_off * TAU if np.isscalar(r_off) else np.asarray(r_off))
    ad['R'] = adapted('R', rsp, **((extra or {}).get('R', {})))
    for x in drop:
        ad.pop(x)
    return ad


def run(ad, pk=None, brackets=None):
    pks = {c: dict(GOODPK) for c in ad}
    pks.update(pk or {})
    return cmp.evaluate(PRE, ad, pks, brackets or PRE['anchor']['brackets'])


def outcome(ev):
    d = ev['decision']
    return d['outcome'] + ('/' + d['subtype'] if d.get('subtype') else '') + ('/' + d['adopted_shape'] if d.get('adopted_shape') else '')


# ---------------------------------------------------------------- K02.4 decision scenarios (real prereg)
ev = run(build())
check('K02.4a ADOPT/sphere with all 10 cases valid from driver-normalized specs (C2 v001 passes 4; S2/Y2 v001; others v003)',
      outcome(ev) == 'ADOPT/sphere' and all(g['valid_all'] for g in ev['gates'].values()), {'o': outcome(ev), 'failed': {c: g['failed'] for c, g in ev['gates'].items() if g['failed']}})
u = ev['decision']['carried_numerical_uncertainty_km_s']
want = {i: (0.3 + 0.5 + max(abs(2.8 - 1.3), abs(1.6 - 1.3))) * t for i, t in zip(IDS, TAU)}
check('K02.4b D2: u_i = |K34| + |inner| + max passing-shape spread, per row', all(abs(u[i] - want[i]) < 1e-9 for i in IDS),
      {'row01': [u[IDS[0]], want[IDS[0]]], 'row06': [u[IDS[5]], want[IDS[5]]]})
check('K02.4c modal block == registered; nobody off-modal', ev['modal_common_block']['modal_equals_registered'] is True and ev['modal_common_block']['cases_off_modal'] == [])
# D1: ratio 0.95 within tau -> not a pass; boundary margins
ev = run(build({'cube': ((0, 0.2, 0.39), 0.02), 'sphere': ((0, 0.2, 0.38), 0.009), 'cylinder': ((0, 0.2, 0.39), 0.0095)}))
check('K02.4d D1 ratio-0.95 sequence (Dhat23 0.2, Dhat34 0.19/0.18) -> NOT_CONVERGED; extend sphere (smallest Dhat34)',
      outcome(ev) == 'NOT_CONVERGED' and ev['decision'].get('extend_shape') == 'sphere', {'o': outcome(ev), 'ext': ev['decision'].get('extend_shape')})
row6 = np.zeros(12)
row6[5] = 1
ad = build({'cube': ((0, 0, 0), 0.02), 'sphere': ((0, 0, 0), 0.009), 'cylinder': ((0, 0, 0), 0.0095)},
           row_add={'C3': 0.051 * row6, 'C4': (0.051 + 0.0485) * row6, 'S3': 0.051 * row6, 'S4': (0.051 + 0.0485) * row6,
                    'Y3': 0.051 * row6, 'Y4': (0.051 + 0.0485) * row6})
ev = run(ad)
check('K02.4e D1 CHECK-V001 K02-A1 fixture (D23 0.051, D34 0.0485 km/s on row 06) -> NOT_CONVERGED', outcome(ev) == 'NOT_CONVERGED',
      {'o': outcome(ev), 'Dhat34_sphere': ev['sequences']['sphere'].get('Dhat_3_4'), 'tail06': ev['sequences']['sphere']['tail_diagnostic']['per_row'][IDS[5]]})
ev = run(build({'cube': ((0, 2.0, 2.999), 0.02), 'sphere': ((0, 2.0, 2.999), 0.009), 'cylinder': ((0, 2.0, 2.999), 0.0095)}))
check('K02.4f D1 margin: Dhat34 0.999 <= 1 and <= 0.5*2.0 -> passes (ADOPT)', outcome(ev).startswith('ADOPT'), outcome(ev))
ev = run(build({'cube': ((0, 2.0, 3.001), 0.02), 'sphere': ((0, 2.0, 3.001), 0.009), 'cylinder': ((0, 2.0, 3.001), 0.0095)}))
check('K02.4g D1 margin: Dhat34 1.001 -> NOT_CONVERGED', outcome(ev) == 'NOT_CONVERGED', outcome(ev))
ev = run(build({'cube': ((0, 1.0, 1.501), 0.02), 'sphere': ((0, 1.0, 1.501), 0.009), 'cylinder': ((0, 1.0, 1.501), 0.0095)}))
check('K02.4h D1 margin: q = 0.501 (Dhat34 0.501 <= 1) -> NOT_CONVERGED', outcome(ev) == 'NOT_CONVERGED', outcome(ev))
# per-row tau
r01 = np.zeros(12)
r01[0] = 1
flat = {'cube': ((0, 2.0, 2.0), 0.02), 'sphere': ((0, 2.0, 2.0), 0.009), 'cylinder': ((0, 2.0, 2.0), 0.0095)}
ad = build(flat, row_add={c: 0.36 * r01 + 0.045 * row6 for c in ('C4', 'S4', 'Y4')})
ev = run(ad)
check('K02.4i per-row tau: row01 moves 0.36 km/s (0.9 tau_01), row06 0.045 (0.9 tau_06) 3->4 -> ADOPT; uniform 0.05 would fail row01',
      outcome(ev).startswith('ADOPT') and abs(ev['sequences']['sphere']['D_3_4'] - 0.36) < 1e-9 and ev['sequences']['sphere']['Dhat_3_4'] <= 0.9 + 1e-9,
      {'o': outcome(ev), 'D34': ev['sequences']['sphere']['D_3_4'], 'Dhat34': ev['sequences']['sphere']['Dhat_3_4']})
ad = build(flat, row_add={c: 0.36 * r01 + 0.055 * row6 for c in ('C4', 'S4', 'Y4')})
ev = run(ad)
check('K02.4j per-row tau: row06 0.055 km/s (1.1 tau_06) -> NOT_CONVERGED although |d| is 0.055 << tau_01', outcome(ev) == 'NOT_CONVERGED',
      {'o': outcome(ev), 'Dhat34': ev['sequences']['sphere'].get('Dhat_3_4')})
rev = build()
rev['S4']['rows'] = dict(reversed(list(rev['S4']['rows'].items())))
check('K02.4k row order in result does not matter (rows keyed by id)', outcome(run(rev)) == 'ADOPT/sphere')
# inner control
r07 = np.zeros(12)
r07[6] = 1.05
ev = run(build(r_off=r07 * TAU))
check('K02.4l INNER_UNRESOLVED when R-C2 = 1.05 tau on row 07 only', outcome(ev) == 'INNER_UNRESOLVED' and abs(ev['inner_control']['Dhat_R'] - 1.05) < 1e-9, outcome(ev))
ev = run(build({'cube': ((0, 0.2, 0.39), 0.02), 'sphere': ((0, 0.2, 0.38), 0.009), 'cylinder': ((0, 0.2, 0.39), 0.0095)}, r_off=r07 * TAU))
check('K02.4m rule order: INNER_UNRESOLVED precedes NOT_CONVERGED', outcome(ev) == 'INNER_UNRESOLVED', outcome(ev))
ev = run(build(r_off=r07 * TAU, drop=('C3',)))
check('K02.4n rule order: INCOMPLETE (missing C3) precedes INNER_UNRESOLVED; next step names the missing case', outcome(ev) == 'INCOMPLETE'
      and 'Run the registered case' in json.dumps(ev['decision']['next_step'].get('C3')), ev['decision']['reasons'])
# incomplete variants
ev = run(build(extra={'S4': {'last': 0.013}}))
check('K02.4o V2: S4 final change 0.013 > 0.0125 -> INCOMPLETE, S4 fails V2 only, V2 next step pre-named', outcome(ev) == 'INCOMPLETE'
      and ev['gates']['S4']['failed'] == ['V2'] and 'passes 12' in ev['decision']['next_step']['S4']['V2'], ev['gates']['S4']['failed'])
ev = run(build(extra={'Y3': {'status': 'COMPLETED_INVALID', 'valid': False}}))
check('K02.4p V1: COMPLETED_INVALID -> INCOMPLETE', outcome(ev) == 'INCOMPLETE' and ev['gates']['Y3']['failed'] == ['V1'])
ad = build()
ad['C4']['rows'] = dict(list(ad['C4']['rows'].items())[:11])
ev = run(ad)
check('K02.4q V1: 11 of 12 rows -> INCOMPLETE', outcome(ev) == 'INCOMPLETE' and 'V1' in ev['gates']['C4']['failed'])
ad = build()
ad['C3']['rows'][IDS[3]] = float('nan')
ev = run(ad)
check('K02.4r V1: non-finite row -> INCOMPLETE', outcome(ev) == 'INCOMPLETE' and 'V1' in ev['gates']['C3']['failed'])
# odd reference (D8)
def bump_gamma(ns):
    ns['physical']['gamma'] *= 1.0000001
ev = run(build(extra={'C4': {'ns_mod': bump_gamma}}))
bad = sorted(c for c, g in ev['gates'].items() if not g['valid_all'])
check('K02.4s D8 odd reference: odd C4 (V001 reference case) alone is named; S4/Y4 stay valid', bad == ['C4'] and ev['gates']['C4']['V3_mismatch'] == ['physical'],
      {'bad': bad, 'mism': ev['gates']['C4'].get('V3_mismatch'), 'off_modal': ev['modal_common_block']['cases_off_modal']})
def wide_bk(ns):
    ns['numerics']['brackets']['rule']['fs_absolute_overrides']['10'] = [302500000.0, 330000000.0]
ev = run(build(extra={c: {'ns_mod': wide_bk} for c in ('C3', 'S3', 'Y3', 'C4', 'S4', 'Y4')}))
bad = sorted(c for c, g in ev['gates'].items() if not g['valid_all'])
check('K02.4t D8 majority-odd: 6 of 10 cases share an unregistered bracket block -> those 6 named, the 4 registered ones valid, modal != registered',
      bad == ['C3', 'C4', 'S3', 'S4', 'Y3', 'Y4'] and ev['modal_common_block']['modal_equals_registered'] is False,
      {'bad': bad, 'modal': ev['modal_common_block']})
# D7 recovery block
rec = copy.deepcopy(PRE['anchor']['brackets'])
rec['rule']['fs_absolute_overrides']['10'] = [302500000.0, 330000000.0]
ev = run(build(extra={c: {'ns_mod': wide_bk} for c in CASES}), brackets=rec)
check('K02.4u D7: every case on the recovery block + recovery passed -> ADOPT', outcome(ev) == 'ADOPT/sphere', outcome(ev))
ev = run(build(extra={c: {'ns_mod': wide_bk} for c in CASES if c != 'R'}), brackets=rec)
check('K02.4v D7: recovery passed but R still on the original block -> INCOMPLETE naming R only (V3 brackets)',
      outcome(ev) == 'INCOMPLETE' and sorted(c for c, g in ev['gates'].items() if not g['valid_all']) == ['R'] and ev['gates']['R']['V3_mismatch'] == ['brackets'])
# root d: C2 Picard equivalence
for lastc, exp in ((0.0099, True), (0.0101, False)):
    ev = run(build(extra={'C2': {'last': lastc}}))
    g = ev['gates']['C2']
    check('K02.4w root d: C2 passes 4, final change %.4f -> %s' % (lastc, 'valid' if exp else 'V3 PICARD_CAP_NOT_EQUIVALENT (V2 still passes)'),
          g['valid_all'] == exp and (exp or (g['failed'] == ['V3'] and 'PICARD_CAP_NOT_EQUIVALENT' in g['V3_mismatch'])), g['failed'])
ev = run(build(extra={'C2': {'passes': 5}}))
check('K02.4x root d: C2 passes 5 -> V3 fail', 'V3' in ev['gates']['C2']['failed'])
ev = run(build(extra={'C2': {'passes': 6}}))
check('K02.4y root d: C2 replaced by C2\' (passes 6) -> valid', ev['gates']['C2']['valid_all'])
ev = run(build(extra={'S2': {'passes': 4}}))
check('K02.4z root d: exception is C2-only (S2 passes 4 -> V3 picard_passes)', ev['gates']['S2']['V3_mismatch'] == ['picard_passes'])
ev = run(build(extra={'C2': {'last': 0.012}}))
check('K02.4z2 next step for PICARD_CAP_NOT_EQUIVALENT is the pre-named C2\' route', "C2'" in json.dumps(ev['decision']['next_step']))
# root c: driver allowance and V6
ev = run(build(extra={'C3': {'driver': 'v001'}}))
check('K02.5a root c: C3 under v001 -> V3 driver mismatch (S3/Y3 then also fail V6: driver differs)', ev['gates']['C3']['failed'] == ['V3']
      and any('driver' in x for x in ev['gates']['C3']['V3_mismatch']), {c: ev['gates'][c]['failed'] for c in ('C3', 'S3', 'Y3')})
ev = run(build(extra={c: {'driver': 'v003'} for c in ('C2', 'S2', 'Y2')}))
check('K02.5b root c: C2/S2/Y2 all under v003 -> valid', all(ev['gates'][c]['valid_all'] for c in ('C2', 'S2', 'Y2')))
ev = run(build(extra={'S2': {'driver': 'v003'}}))
check('K02.5c admission constraint: S2 v003 admitting C2 v001 -> S2 fails V6 only', ev['gates']['S2']['failed'] == ['V6'])
ev = run(build(extra={'Y4': {'ident': 'e' * 64}}))
check('K02.5d V6: Y4 route-A identity differs from C4 -> V6 fail', ev['gates']['Y4']['failed'] == ['V6'])
ev = run(build(extra={'R': {'driver': 'f' * 64}}))
check('K02.5e unknown driver sha -> V3 fail', 'V3' in ev['gates']['R']['failed'])
def grid_swap(ns):
    ns['numerics']['composite_grid_spec'] = copy.deepcopy(PRE['grids']['G3']['composite_grid_spec'])
ev = run(build(extra={'C4': {'ns_mod': grid_swap}}))
check('K02.5f V3: C4 normalized grid = G3 block -> V3 grid mismatch', 'grid' in ev['gates']['C4']['V3_mismatch'])
def kmax_swap(ns):
    ns['numerics']['truncation']['kmax_inverse_kpc'] = 3.0
ev = run(build(extra={'S4': {'ns_mod': kmax_swap}}))
check('K02.5g V3: S4 with kmax 3 on G4 -> V3 truncation mismatch', 'truncation' in ev['gates']['S4']['V3_mismatch'])
# shape agreement (2 tau_i per row) and m4 tie-break (D13)
base_ok = {'cube': ((0, 4.0, 6.0), 0.02), 'sphere': ((0, 1.0, 1.3), 0.009), 'cylinder': ((0, 1.0, 1.3), 0.0095)}
ev = run(build(base_ok, row_add={'Y4': 2.1 * TAU * row6, 'Y3': 2.1 * TAU * row6}))
check('K02.5h shape agreement: sphere vs cylinder at K=4 differ by 2.1 tau_06 (row 06 only) -> NOT_CONVERGED/SHAPE_DISAGREEMENT',
      outcome(ev) == 'NOT_CONVERGED/SHAPE_DISAGREEMENT', {'o': outcome(ev), 'spread': ev['shape_spread_K4']})
ev = run(build(base_ok, row_add={'Y4': 1.9 * TAU * row6, 'Y3': 1.9 * TAU * row6}))
check('K02.5i shape agreement: 1.9 tau_06 -> ADOPT', outcome(ev).startswith('ADOPT'), outcome(ev))
ev = run(build({'cube': ((0, 1, 1.45), 0.0100), 'sphere': ((0, 1, 1.4), 0.0105), 'cylinder': ((0, 1, 1.3), 0.0109)}))
check('K02.5j D13: three shapes within 10% of min m4 -> candidates all; smallest Dhat34 (cylinder) adopted', outcome(ev) == 'ADOPT/cylinder'
      and ev['decision']['m4_candidates'] == ['cube', 'sphere', 'cylinder'], {'o': outcome(ev), 'cand': ev['decision'].get('m4_candidates')})
ev = run(build({'cube': ((0, 1, 1.45), 0.0100), 'sphere': ((0, 1, 1.4), 0.0105), 'cylinder': ((0, 1, 1.3), 0.0111)}))
check('K02.5k D13: cylinder m4 11% above min -> excluded; sphere adopted', outcome(ev) == 'ADOPT/sphere', {'o': outcome(ev), 'cand': ev['decision'].get('m4_candidates')})
ev = run(build({'cube': ((0, 1, 1.45), 0.0100), 'sphere': ((0, 1, 1.4), None), 'cylinder': ((0, 1, 1.3), 0.03)}))
check('K02.5l D13: one passing shape m4 null -> candidates = all passing (cylinder by Dhat34)', outcome(ev) == 'ADOPT/cylinder', outcome(ev))
ev = run(build({'cube': ((0, 1, 1.4), 0.0100), 'sphere': ((0, 1, 1.4), 0.0100), 'cylinder': ((0, 1, 1.4), 0.0100)}))
check('K02.5m D13 exact tie in Dhat34 -> registered order (cube)', outcome(ev) == 'ADOPT/cube', outcome(ev))
ev = run(build({'cube': ((0, 1, 1.45), 0.0100), 'sphere': ((0, 1, 1.4), 0.0100), 'cylinder': ((0, 1, 1.4), 0.0100)}))
check('K02.5n D13 exact tie sphere/cylinder -> sphere', outcome(ev) == 'ADOPT/sphere', outcome(ev))
# packet gates (V4/V5) on the REAL G2 grid (72^3), compact weighted_responses
ax = AX['G2']
kk = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3)
msk = cmp.driver_mask(kk, 'sphere', 2.0 / KPC)
scr = Path(sys.argv[2])
scr.mkdir(parents=True, exist_ok=False)


def packet(name, k, w):
    p = scr / ('pk_' + name + '.npz')
    np.savez(p, wavevectors=k, weighted_responses=w)
    return {'path': str(p), 'sha256': sha_b(p.read_bytes())}


def pk_check(name, k, w, cid, gid='G2'):
    a = {'field_packet': packet(name, k, w)}
    chk, _ = cmp.packet_checks(a, CASES[cid], PRE['grids'][gid]['composite_grid_spec'], None, False)
    return chk


w_ok = np.where(msk[:, None, None], 1e-12 + 1e-13j, 0).astype(complex)
c1 = pk_check('S2_ok', kk, w_ok, 'S2')
check('K02.6a V4/V5: correctly masked real-size S2 packet passes (kept 344048 nonzero)', c1['V4'] and c1['V5'] and c1['nonzero_rows_in_packet'] == 344048, c1)
w_om = w_ok.copy()
w_om[np.argmax(msk)] = 0
c2 = pk_check('S2_overmask', kk, w_om, 'S2')
check('K02.6b D3 over-masked S2 packet (one kept row zeroed) fails V5, passes V4', c2['V4'] and not c2['V5'] and c2['outside_rows_all_zero'], c2)
w_cube = np.full((len(kk), 1, 1), 1e-12 + 0j)
c3 = pk_check('S2_unmasked', kk, w_cube, 'S2')
check('K02.6c cube (unmasked) packet presented as S2 fails V5', not c3['V5'], c3)
c4 = pk_check('C2_spheremasked', kk, w_ok, 'C2')
check('K02.6d CHECK V001 A3: sphere-masked packet presented as cube C2 fails V5', not c4['V5'], c4)
c5 = pk_check('S2_wrongaxis', kk * (1 + 1e-12), w_ok, 'S2')
check('K02.6e V4: axis perturbed by 1e-12 relative fails V4', not c5['V4'], c5)
del kk, w_ok, w_om, w_cube

# ---------------------------------------------------------------- K02.7 end-to-end main() with the SEALED prereg (not test mode)
def write_case(root, cid, speeds, m4, ident, driver, passes, last, reverse_rows=False, overmask=False):
    c = CASES[cid]
    gid = c['grid']
    ax = AX[gid]
    k = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3)
    edge = float(PRE['grids'][gid]['composite_grid_spec']['breaks_inverse_kpc'][-1]) if PRE['grids'][gid]['composite_grid_spec'] else 2.0
    m = cmp.driver_mask(k, c['shape'], (c['kmax_inverse_kpc'] or edge) / KPC)
    w = np.where(m[:, None, None], 1e-12 + 2e-13j, 0).astype(complex)
    if overmask:
        w[np.argmax(m)] = 0
    d = root / cid
    (d / 'fb').mkdir(parents=True)
    (d / 'rot').mkdir()
    np.savez(d / 'fb' / 'refreshed_prepared.npz', wavevectors=k, weighted_responses=w)
    (d / 'fb' / 'finish.json').write_text(json.dumps({'outputs': {'refreshed_prepared.npz': {'path': str(d / 'fb' / 'refreshed_prepared.npz'), 'sha256': sha_b((d / 'fb' / 'refreshed_prepared.npz').read_bytes())}}}))
    (d / 'rot' / 'finish.json').write_text(json.dumps({'base_K_values_SI': [1.0] * 72}))
    ns = copy.deepcopy(NS[cid][driver])
    ns['numerics']['picard']['passes'] = passes
    rows = [{'id': i, 'speed_km_s': float(v)} for i, v in zip(IDS, speeds)]
    if reverse_rows:
        rows = rows[::-1]
    per_r = [{'m4': (0.9 if not (0.4 <= R / KPC <= 6.0) else m4 * (1 + 0.001 * j))} for j, R in enumerate(RADIAL)]
    r = {'schema': cmp.RESULT_SCHEMA, 'status': 'COMPLETED', 'valid': True, 'reasons': [], 'driver_sha256': DSHA[driver],
         'call_spec_sha256': CASES['C2']['bound_call']['call_spec_sha256'] if cid == 'C2' else 'c' * 64,
         'rows': rows, 'normalized_spec': ns, 'final_pass': 3,
         'passes': [{'pass': 1}, {'pass': 2, 'max_abs_change_km_s': 0.2}, {'pass': 3, 'max_abs_change_km_s': last, 'field': str(d / 'fb'), 'rotation': str(d / 'rot')}],
         'identity': {'route_a': {'custody': {'identity_sha256': ident}}},
         'residual_diagnostics': {'azimuthal_harmonics': {'global_max': {'m4': 0.9, 'm8': 'nan'}, 'per_radius_max': per_r, 'radial_nodes_m': RADIAL}},
         'elapsed_seconds': 1.0}
    (d / 'result.json').write_text(json.dumps(r))
    return str(d / 'result.json')


def e2e(name, plan=PLAN0, overmask=(), recovery=None):
    root = scr / ('e2e_' + name)
    cases = {}
    for shp, (cs, m4) in plan.items():
        for K, cK in zip((2, 3, 4), cs):
            cid = '%s%d' % (LET[shp], K)
            drv = 'v001' if CASES[cid]['grid'] == 'G2' else 'v003'
            cases[cid] = write_case(root, cid, BASEV + cK * TAU, m4 if K == 4 else 0.5, {'2': 'a', '3': 'b', '4': 'c'}[str(K)] * 64, drv,
                                    4 if cid == 'C2' else 6, 0.004, reverse_rows=(cid == 'Y3'), overmask=(cid in overmask))
    cases['R'] = write_case(root, 'R', BASEV + 0.5 * TAU, 0.5, 'd' * 64, 'v003', 6, 0.004)
    cf = root / 'cases.json'
    cf.write_text(json.dumps(cases))
    od = Path(sys.argv[1]).parent / ('K02_E2E_%s_V001' % name)
    argv = ['--prereg', str(PRE_P), '--cases', str(cf), '--outdir', str(od), '--no-field-diagnostic']
    if recovery:
        rp = root / 'recovery.json'
        rp.write_text(json.dumps(recovery))
        argv += ['--bracket-recovery', str(rp)]
    rc = cmp.main(argv)
    rep = json.loads((od / 'KMAX_COMPARISON.json').read_text()) if rc == 0 else None
    return rc, rep


rc, rep = e2e('adopt')
check('K02.7a end-to-end main() on the sealed prereg (test_mode false), real-size packets, real grids -> ADOPT/sphere, all V4/V5 pass, m4 row window excludes R<0.4 and R>6 kpc',
      rc == 0 and rep['test_mode'] is False and outcome(rep) == 'ADOPT/sphere' and all(v['V4'] and v['V5'] for v in rep['packet_checks'].values())
      and abs(rep['inputs']['S4']['m4_row_window'] - 0.0090 * 1.004) < 1e-12,
      {'rc': rc, 'o': rep and outcome(rep), 'm4_S4': rep and rep['inputs']['S4']['m4_row_window'], 'pk': rep and {c: [v['V4'], v['V5']] for c, v in rep['packet_checks'].items()}})
rc, rep = e2e('overmask_S4', overmask=('S4',))
check('K02.7b end-to-end: over-masked real-size S4 packet -> INCOMPLETE, S4 fails V5 only', rc == 0 and outcome(rep) == 'INCOMPLETE'
      and rep['gates']['S4']['failed'] == ['V5'], rep and rep['gates']['S4']['failed'])
rec_bad = copy.deepcopy(PRE['anchor']['brackets'])
rec_bad['rule']['rfs_factors'] = [0.7, 1.3]
rc, rep = e2e('recovery_nonoverride', recovery={'brackets': rec_bad, 'reason': 'probe: changes a non-override rule key'})
check('K02.7c FINDING-PROBE D7: a recovery file that changes a NON-override key (rfs_factors) is accepted (not refused); it is only reported in changed_rule_keys',
      rc == 0 and rep['bracket_recovery']['changed_rule_keys'] == ['rfs_factors'],
      {'rc': rc, 'changed': rep and rep['bracket_recovery']['changed_rule_keys'], 'o': rep and outcome(rep)})
rc = cmp.main(['--prereg', str(PRE_P), '--cases', str(scr / 'e2e_adopt' / 'cases.json'), '--outdir', str(scr / 'e2e_adopt' / 'again'),
               '--bracket-recovery', str(PRE_P)])
check('K02.7d malformed recovery file refused', rc == 2)
bad_cases = scr / 'unknown_cases.json'
bad_cases.write_text(json.dumps({'C5': 'x'}))
rc = cmp.main(['--prereg', str(PRE_P), '--cases', str(bad_cases), '--outdir', str(scr / 'unk')])
check('K02.7e unregistered case id refused', rc == 2)

summary = {'schema': 'UNT_KMAX_PREREG_V002_CHECK_K02_C2_V001', 'n': len(OUT), 'n_pass': sum(x['pass'] for x in OUT), 'results': OUT,
           'inputs': {'prereg_sha256': PRE_SHA, 'compare_sha256': CMP_SHA, 'drivers': DSHA, 'script_sha256': sha_b(Path(__file__).read_bytes())},
           'note': 'K02.7c PASS means the probe observed the stated behaviour (acceptance), which CHECK_V001 reports as advisory A1.'}
with open(sys.argv[1], 'x') as f:
    json.dump(summary, f, indent=1, default=str)
print('%d/%d' % (summary['n_pass'], summary['n']))
