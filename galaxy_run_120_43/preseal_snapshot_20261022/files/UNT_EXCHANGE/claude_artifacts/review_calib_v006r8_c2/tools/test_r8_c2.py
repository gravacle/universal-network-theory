"""Claude2-lane refute-by-default probes of Codex2 v006r8 (0554 items 1-2), own fixtures.

Synthetic evidence only. No launch: the r5 driver is loaded only for normalize_spec replay.
Every check states the expected refusal; a check PASSES when the code behaves as 0554 requires.
"""
import copy
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location('_c2r8_common', HERE / 'common_c2r8.py')
C = importlib.util.module_from_spec(_s)
_s.loader.exec_module(C)

RUN = C.OUT / ('run_' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '_%d' % os.getpid())
RUN.mkdir(parents=True)
L = C.Ledger()

W = C.load_pinned(C.R8 / 'calibration_orchestrator_cx2v006r8_v004.py', '_c2r8_wrapper', C.WRAPPER_SHA)
M, S, O = W.M, W.S, W.O
CFG = json.loads((C.R8 / 'RUN_CONFIG_DDO154_CX2V006R8_P128_MS128.json').read_bytes())
REG = json.loads((C.R8 / 'REGISTERED_ANCHOR_CX2V006R8.json').read_bytes())
TEMPLATE = json.loads(Path(REG['source_template']['path']).read_bytes())
DRV = C.load_pinned(CFG['driver']['path'], '_c2r8_r5_normalizer', CFG['driver']['sha256'])
MON = C.load_pinned(CFG['monitor']['path'], '_c2r8_monitor', CFG['monitor']['sha256'])
COORD = json.loads((C.ART / 'calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json').read_bytes())
SEQ = [0]
NORMALIZER_REFUSED = {}


def nxt():
    SEQ[0] += 1
    return SEQ[0]


def fixture_run(tag, *, physical=None, coefficients=None, numerics_edit=None):
    """Write own spec/result/finish/receipt for one synthetic COMPLETED fresh run."""
    d = RUN / ('%03d_%s' % (nxt(), tag))
    spec = {'schema': TEMPLATE['schema'], 'galaxy': 'DDO154', 'admit': {},
            'reference_compare': False, 'label': 'C2R8 SYNTHETIC FIXTURE ' + tag,
            'physical': copy.deepcopy(TEMPLATE['physical'] if physical is None else physical),
            'coefficients': copy.deepcopy(TEMPLATE['coefficients'] if coefficients is None else coefficients),
            'numerics': copy.deepcopy(CFG['numerics']['block'])}
    if numerics_edit:
        numerics_edit(spec['numerics'])
    sp = C.write_x(d / 'spec.json', spec)
    try:
        norm = DRV.normalize_spec(copy.deepcopy(spec))
    except Exception as exc:  # driver refuses this spec; the forged result then carries the raw spec
        norm = copy.deepcopy(spec)
        NORMALIZER_REFUSED[tag] = type(exc).__name__ + ': ' + str(exc)[:160]
    res = {'status': 'COMPLETED', 'valid': True, 'driver_sha256': M.DRIVER_SHA,
           'call_spec_sha256': sp['sha256'], 'normalized_spec': norm,
           'c2r8_fixture': tag}
    rp = C.write_x(d / 'result.json', res)
    C.write_x(d / 'finish.json', {'status': 'COMPLETED', 'valid': True,
                                  'result_path': rp['path'], 'result_sha256': rp['sha256']})
    rc = C.write_x(d / 'receipt.json', C.make_receipt(MON.RECEIPT_SCHEMA, sp['sha256'], M.DRIVER_SHA, rp))
    return {'name': None, 'spec': sp, 'spec_sha256': sp['sha256'], 'result': rp, 'receipt': rc}


def named(run, name):
    r = copy.deepcopy(run)
    r['name'] = name
    return r


def anchor_for(run, base=None):
    a = copy.deepcopy(CFG['anchor'] if base is None else base)
    a.update(result=copy.deepcopy(run['result']), receipt=copy.deepcopy(run['receipt']),
             spec_sha256=run['spec_sha256'])
    return a


def evidence(rows):
    return C.write_x(RUN / ('deciding_%03d.json' % nxt()), {
        'schema': 'DDO154_V010R5_DECIDING_CX2V006', 'status': 'TESTED', 'ok': True,
        'driver_sha256': M.DRIVER_SHA, 'route_a_column_workers': 8, 'runs': rows})


def gate(rows, anchor):
    g = M.check_deciding(evidence(rows), M.DRIVER_SHA, MON, anchor=anchor)
    return g['ok'], g['reasons']


def refuses(cid, name, rows, anchor, want=None):
    ok, reasons = gate(rows, anchor)
    hit = (not ok) and (want is None or any(want in r for r in reasons))
    L.check(cid, name, hit, {'gate_ok': ok, 'reasons': reasons, 'expected_reason': want})


# ---------- positive control ----------
RA = fixture_run('reanchor_exact')
W8 = fixture_run('workers8_exact_point')
ANCHOR = anchor_for(RA)
ok, reasons = gate([named(RA, 'reanchor'), named(W8, 'workers_8')], ANCHOR)
L.check('P1', 'exact registered template point + config.anchor pins + workers_8 row passes', ok, reasons)
ok, reasons = gate([named(W8, 'workers_8'), named(RA, 'reanchor')], ANCHOR)
L.check('P2', 'row order does not matter (positive)', ok, reasons)

# ---------- (1a) near-miss physical / seed coordinate; config.anchor rebound to the bad row ----------
seed = COORD['trial_point']['engine_seed_theta']
seed_phys = copy.deepcopy(TEMPLATE['physical'])
seed_phys.update(common_scale_s=seed['common_scale_s'], ell_F_m=seed['ell_F_m'],
                 gamma=seed['gamma_over_Eref'] * seed['Eref_base_J'], distance_Mpc=seed['distance_Mpc'])
diff_fields = sorted(k for k in seed_phys if seed_phys[k] != TEMPLATE['physical'][k])
bad = fixture_run('reanchor_engine_seed_logexp', physical=seed_phys)
refuses('N1', 'log/exp engine-seed coordinate (differs in %s at ~1e-15) refuses as reanchor' % diff_fields,
        [named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad), 'REANCHOR_NOT_EXACT_REGISTERED_A2F10_POINT')

for cid, dval in [('N2', 4.0400001), ('N3', math.nextafter(4.04, 5.0)), ('N4', math.nextafter(4.04, 0.0))]:
    ph = copy.deepcopy(TEMPLATE['physical'])
    ph['distance_Mpc'] = dval
    bad = fixture_run('reanchor_D_%r' % dval, physical=ph)
    refuses(cid, 'D=%r (near 4.04) refuses as reanchor' % dval,
            [named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))

for i, k in enumerate(['Eref_J', 'common_scale_s', 'ell_F_m', 'entropy_K_factor', 'gamma', 'inclination_deg']):
    ph = copy.deepcopy(TEMPLATE['physical'])
    ph[k] = math.nextafter(ph[k], math.inf)
    bad = fixture_run('reanchor_ulp_' + k, physical=ph)
    refuses('N5.%d' % i, 'one-ulp change in %s refuses as reanchor' % k,
            [named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad), 'REANCHOR_NOT_EXACT_REGISTERED_A2F10_POINT')

ph = copy.deepcopy(TEMPLATE['physical'])
ph['ML_3p6'] = 0.5
bad = fixture_run('reanchor_extra_physical_key', physical=ph)
ok, reasons = gate([named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))
L.check('N6', 'extra physical key refuses (at registration compare or driver normalization)', not ok, reasons)

ph = copy.deepcopy(TEMPLATE['physical'])
ph['inclination_deg'] = 66
bad = fixture_run('reanchor_int_inclination', physical=ph)
ok_int, reasons_int = gate([named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))
L.check('O1', 'OBSERVATION (not a requirement): inclination 66 (int) vs 66.0 (float), gate_ok recorded',
        True, {'gate_ok': ok_int, 'reasons': reasons_int})

# ---------- (1b) different coefficient file ----------
npz = Path(TEMPLATE['coefficients']['path'])
raw = npz.read_bytes()
altered = C.write_x(RUN / 'coef_altered_copy.npz', raw + b'\0')
bad = fixture_run('reanchor_other_coef_file', coefficients=altered)
refuses('C1', 'different coefficient file (real distinct bytes, sha %s) refuses' % altered['sha256'][:8],
        [named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))
same = C.write_x(RUN / 'coef_exact_copy.npz', raw)
bad = fixture_run('reanchor_same_sha_other_path', coefficients=same)
refuses('C2', 'byte-identical coefficient copy at another path (sha 2e3a36d8) refuses (exact pin object)',
        [named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))
alias = {'path': str(npz.parent) + '/./' + npz.name, 'sha256': TEMPLATE['coefficients']['sha256']}
bad = fixture_run('reanchor_path_alias', coefficients=alias)
refuses('C3', 'same file via path alias "/./" refuses (exact pin object)',
        [named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))
fake = {'path': TEMPLATE['coefficients']['path'], 'sha256': '0' * 64}
bad = fixture_run('reanchor_fake_coef_sha', coefficients=fake)
refuses('C4', 'right path, wrong coefficient sha refuses',
        [named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))

# ---------- (1c) any other D=4.04 workers-8 run refuses as the reanchor ----------
RA2 = fixture_run('second_fresh_run_exact_point')
refuses('S1', 'second fresh run at the exact registered point, config.anchor pins the first: refuses',
        [named(RA2, 'reanchor'), named(W8, 'workers_8')], ANCHOR, 'REANCHOR_ROW_CONFIG_ANCHOR_PIN_MISMATCH')
refuses('S2', 'workers_8 run relabelled reanchor (its own pins) refuses',
        [named(W8, 'reanchor'), named(RA, 'workers_8')], ANCHOR, 'REANCHOR_ROW_CONFIG_ANCHOR_PIN_MISMATCH')
ph = copy.deepcopy(TEMPLATE['physical'])
ph['gamma'] *= 3.0
OTHER = fixture_run('other_headline_theta', physical=ph)
refuses('S3', 'other headline theta, config.anchor rebound to it: refuses on registration',
        [named(OTHER, 'reanchor'), named(W8, 'workers_8')], anchor_for(OTHER), 'REANCHOR_NOT_EXACT_REGISTERED_A2F10_POINT')
refuses('S4', 'two rows both named reanchor refuses',
        [named(RA, 'reanchor'), named(RA2, 'reanchor')], ANCHOR, 'DECIDING_EXACT_NAMED_REANCHOR_AND_WORKERS_8_REQUIRED')
refuses('S5', 'same run in both rows refuses (distinct results)',
        [named(RA, 'reanchor'), named(RA, 'workers_8')], ANCHOR, 'DECIDING_DISTINCT_RUN_RESULTS_REQUIRED')

# ---------- (1d) swapped / rebound pins ----------
for i, (k, v) in enumerate([('result', W8['result']), ('receipt', W8['receipt']), ('spec_sha256', W8['spec_sha256'])]):
    a = copy.deepcopy(ANCHOR)
    a[k] = copy.deepcopy(v)
    refuses('W%d' % (i + 1), 'config.anchor.%s swapped to the workers_8 run refuses' % k,
            [named(RA, 'reanchor'), named(W8, 'workers_8')], a)
r_sw = named(RA, 'reanchor'); r_sw['receipt'] = copy.deepcopy(W8['receipt'])
w_sw = named(W8, 'workers_8'); w_sw['receipt'] = copy.deepcopy(RA['receipt'])
a = copy.deepcopy(ANCHOR); a['receipt'] = copy.deepcopy(W8['receipt'])
refuses('W4', 'receipts swapped between rows, config.anchor.receipt made consistent with the swap: refuses',
        [r_sw, w_sw], a)
refuses('W5', 'receipts swapped between rows, config.anchor unchanged: refuses', [r_sw, w_sw], ANCHOR)
r_sw = named(RA, 'reanchor'); r_sw['result'] = copy.deepcopy(W8['result'])
w_sw = named(W8, 'workers_8'); w_sw['result'] = copy.deepcopy(RA['result'])
a = copy.deepcopy(ANCHOR); a['result'] = copy.deepcopy(W8['result'])
refuses('W6', 'results swapped between rows, config.anchor.result consistent with swap: refuses', [r_sw, w_sw], a)
copy_res = C.write_x(RUN / 'result_copy_other_path.json', Path(RA['result']['path']).read_bytes())
a = copy.deepcopy(ANCHOR); a['result'] = copy_res
refuses('W7', 'config.anchor.result = byte copy of reanchor result at other path refuses', [named(RA, 'reanchor'), named(W8, 'workers_8')], a)
r_bad = named(RA, 'reanchor'); r_bad['spec_sha256'] = W8['spec_sha256']
refuses('W8', 'row spec_sha256 field differs from its spec pin refuses', [r_bad, named(W8, 'workers_8')], ANCHOR)
for i, k in enumerate(['result', 'receipt', 'spec_sha256']):
    a = copy.deepcopy(ANCHOR); a[k] = None
    refuses('W%d' % (9 + i), 'config.anchor.%s pending (null) refuses' % k,
            [named(RA, 'reanchor'), named(W8, 'workers_8')], a, 'CONFIG_ANCHOR_TAIL_REANCHOR_PENDING')
ok, reasons = gate([named(RA, 'reanchor'), named(W8, 'workers_8')], CFG['anchor'])
L.check('W12', 'shipped config.anchor (pending result) refuses a well-formed pair', not ok and any('PENDING' in r for r in reasons), reasons)

# ---------- (1e) config.anchor registration tampering ----------
tamper = [
    ('T1', 'registered_point sha', lambda a: a['registered_point'].update(sha256='f' * 64)),
    ('T2', 'registered_point path alias', lambda a: a['registered_point'].update(path=str(C.R8) + '/./REGISTERED_ANCHOR_CX2V006R8.json')),
    ('T3', 'physical distance 4.0400001', lambda a: a['physical'].update(distance_Mpc=4.0400001)),
    ('T4', 'physical gamma one ulp', lambda a: a['physical'].update(gamma=math.nextafter(a['physical']['gamma'], math.inf))),
    ('T5', 'coefficients sha', lambda a: a['coefficients'].update(sha256='0' * 64)),
    ('T6', 'driver sha', lambda a: a.update(driver_sha256='0' * 64)),
    ('T7', 'use true (old alias)', lambda a: a.update(use=True)),
    ('T8', 'use missing', lambda a: a.pop('use')),
    ('T9', 'physical removed', lambda a: a.pop('physical')),
]
for cid, label, fn in tamper:
    a = copy.deepcopy(ANCHOR); fn(a)
    refuses(cid, 'config.anchor %s tamper refuses' % label, [named(RA, 'reanchor'), named(W8, 'workers_8')], a)
ok, reasons = gate([named(RA, 'reanchor'), named(W8, 'workers_8')], None) if M.ANCHOR_CONTEXT.get() is None else (True, ['ambient'])
L.check('T10', 'no anchor (direct call, no ambient context) fails closed', not ok, reasons)

# ---------- (1f) numerics probe: fields outside validate_block ----------
def picard2(n): n['picard']['passes'] = 2
def maxit8(n): n['route_a']['max_iterations'] = 8
def quad4(n): n['uv_tail']['quadrature']['order'] = 4
probe = {}
for tag, fn in [('picard_passes_2', picard2), ('route_a_max_iterations_8', maxit8), ('uv_quadrature_order_4', quad4)]:
    try:
        r = fixture_run('reanchor_numerics_' + tag, numerics_edit=fn)
        ok, reasons = gate([named(r, 'reanchor'), named(W8, 'workers_8')], anchor_for(r))
        probe[tag] = {'gate_ok': ok, 'reasons': reasons}
    except Exception as exc:  # normalizer refusal at fixture build
        probe[tag] = {'fixture_refused_by_normalizer': type(exc).__name__ + ': ' + str(exc)[:200]}
L.check('O2', 'OBSERVATION: reanchor numerics differing from config.numerics.block outside validate_block', True, probe)

# ---------- (1g) Context-level binding (actual inherited init + fresh_gates) ----------
def local_cfg(label, ra, w8):
    c = copy.deepcopy(CFG)
    d = RUN / ('ctx_' + label)
    c['work_dir'] = str(d); c['work_dir_volume'] = None
    c['work_dir_identity'] = {'resolved': str(d.resolve()), 'volume': None, 'volume_uuid': None, 'symlinks': []}
    c['anchor'] = anchor_for(ra)
    c['deciding_test'] = evidence([named(ra, 'reanchor'), named(w8, 'workers_8')])
    return c
cfg_good = local_cfg('good', RA, W8)
try:
    ctx = W.Context(cfg_good)
    L.check('X1', 'actual Context: own fixture config with bound anchor -> deciding gate ok', ctx.gates['deciding_test']['ok'],
            ctx.gates['deciding_test'].get('reasons'))
    fg = ctx.fresh_gates()
    L.check('X2', 'actual inherited fresh_gates re-binds the instance anchor', fg['deciding_test']['ok'] and M.ANCHOR_CONTEXT.get() is None,
            fg['deciding_test'].get('reasons'))
except Exception as exc:
    L.check('X1', 'actual Context construction', False, type(exc).__name__ + ': ' + str(exc)[:400])
cfg_sub = local_cfg('substitute', RA, W8)
cfg_sub['deciding_test'] = evidence([named(RA2, 'reanchor'), named(W8, 'workers_8')])
try:
    ctx2 = W.Context(cfg_sub)
    g2 = ctx2.gates['deciding_test']
    L.check('X3', 'actual Context: substitute D=4.04 workers-8 reanchor (config.anchor = original) -> gate refuses',
            not g2['ok'] and any('REANCHOR_ROW_CONFIG_ANCHOR_PIN_MISMATCH' in r for r in g2['reasons']), g2['reasons'])
except Exception as exc:
    L.check('X3', 'actual Context substitute', False, type(exc).__name__ + ': ' + str(exc)[:400])
cfg_bad = local_cfg('anchor_tampered', RA, W8)
cfg_bad['anchor']['physical']['distance_Mpc'] = 4.0400001
try:
    W.Context(cfg_bad); ok = False; why = 'constructed'
except M.Error as exc:
    ok = 'CONFIG_ANCHOR_REGISTRATION_MISMATCH' in str(exc); why = str(exc)
L.check('X4', 'actual Context refuses at construction when config.anchor physical is not the registration', ok, why)
L.check('X5', 'ANCHOR_CONTEXT restored to None after all Context work', M.ANCHOR_CONTEXT.get() is None)

# ---------- (4) config.anchor target-free ----------
an = CFG['anchor']
words = [w for w in ('ngc', 'target', 'observed', 'rotmod', 'vobs', 'velocity', 'v_obs') if w in json.dumps(an).lower()]
L.check('F1', 'config.anchor key set is registration-only', set(an) == {'use', 'receipt', 'result', 'spec_sha256', 'driver_sha256',
        'registered_point', 'physical', 'coefficients'}, sorted(an))
L.check('F2', 'config.anchor contains no target words', not words, words)
L.check('F3', 'config.anchor.physical == registered == source template physical (exact objects)',
        an['physical'] == REG['physical'] == TEMPLATE['physical'])
L.check('F4', 'config.anchor.coefficients == template coefficients and sha 2e3a36d8 from bytes',
        an['coefficients'] == TEMPLATE['coefficients'] and C.sha_file(an['coefficients']['path']) == an['coefficients']['sha256']
        and an['coefficients']['sha256'].startswith('2e3a36d8'))
L.check('F5', 'registered_point / source_template / coordinate_registration pins verify from bytes',
        C.sha_file(an['registered_point']['path']) == an['registered_point']['sha256']
        and C.sha_file(REG['source_template']['path']) == REG['source_template']['sha256']
        and C.sha_file(REG['coordinate_registration']['path']) == REG['coordinate_registration']['sha256'])
L.check('F6', 'coordinate registration declares ngc3198_access NONE and pins the same anchor spec',
        COORD.get('ngc3198_access') == 'NONE' and COORD['trial_point']['anchor_spec'] == REG['source_template'])
L.check('F7', 'template galaxy DDO154, no NGC key anywhere in template',
        TEMPLATE['galaxy'] == 'DDO154' and 'ngc' not in json.dumps(TEMPLATE).lower())
L.check('F8', 'result/receipt/spec_sha256 pending (null), use false', an['result'] is None and an['receipt'] is None
        and an['spec_sha256'] is None and an['use'] is False)

# ---------- (2) sensitivity review pinned by bytes ----------
def rv(name, **extra):
    body = {'schema': S.SCHEMA_REVIEW, 'status': 'TESTED', 'verdict': 'PASS', 'reviewer': name}
    body.update(extra)
    return C.write_x(RUN / ('review_%03d.json' % nxt()), body)
good = rv('Claude3 distinct lane')
renamed = rv('Claude3  distinct lane')
renamed2 = rv('Codex2')
L.check('R1', 'shipped allowlist is empty frozenset', S.REGISTERED_DISTINCT_REVIEW_SHA256 == frozenset()
        and type(S.REGISTERED_DISTINCT_REVIEW_SHA256) is frozenset)
for cid, ref in [('R2', good), ('R3', renamed2)]:
    try:
        S.registered_review(ref); ok = False; why = 'accepted'
    except S.Refusal as e:
        ok = 'DISTINCT_REVIEW_SHA_NOT_ROOT_REGISTERED' in str(e); why = str(e)
    L.check(cid, 'empty allowlist refuses any review bytes (%s)' % json.loads(Path(ref['path']).read_bytes())['reviewer'], ok, why)
saved = S.REGISTERED_DISTINCT_REVIEW_SHA256
S.REGISTERED_DISTINCT_REVIEW_SHA256 = frozenset([good['sha256']])  # in-memory only
try:
    L.check('R4', 'in-memory root registration of exact bytes accepts', S.registered_review(good)['reviewer'] == 'Claude3 distinct lane')
    for cid, label, ref in [
            ('R5', 'renamed reviewer string (one extra space), own correct pin, wrong sha', renamed),
            ('R6', 'reviewer renamed to Codex2, own correct pin', renamed2),
            ('R7', 'renamed file claiming the registered sha', {'path': renamed['path'], 'sha256': good['sha256']}),
            ('R8', 'registered sha with extra pin key', dict(good, note='x')),
            ('R9', 'relative path to registered bytes', {'path': os.path.relpath(good['path']), 'sha256': good['sha256']})]:
        try:
            S.registered_review(ref); ok = False; why = 'accepted'
        except S.Refusal as e:
            ok = True; why = str(e)
        L.check(cid, label + ' refuses', ok, why)
    # Full sensitivity_gate path at a registered alternate D.
    dist = 4.111497211045223
    key, pair = S.plan_pair(dist)
    spec = {'galaxy': 'DDO154', 'physical': {'distance_Mpc': dist}}
    ev = C.write_x(RUN / 'pair_evidence_synthetic.json', {'schema': S.SCHEMA_EVIDENCE, 'status': 'TESTED', 'ok': True,
        'plan': S.PLAN, 'distance_hex': key, 'distance_mpc': dist, 'launch_owner': 'Claude2', 'tail_on': False,
        'test': 'iii', 'runs': {}, 'comparator_report': good})
    bound = rv('anyone', evidence=ev, comparator_report=good, runs={}, plan=S.PLAN, distance_hex=key)
    bound_renamed = rv('anyone else', evidence=ev, comparator_report=good, runs={}, plan=S.PLAN, distance_hex=key)
    S.REGISTERED_DISTINCT_REVIEW_SHA256 = frozenset([bound['sha256']])
    def cfg_with(review):
        return {'tail_readiness': {'sensitivity_deciding_iii': {'schema': S.SCHEMA_REGISTRY,
                'per_distance': {key: {'evidence': ev, 'review': review}}}}}
    g = S.sensitivity_gate(config=cfg_with(bound_renamed), spec=spec)
    L.check('R10', 'sensitivity_gate: renamed-reviewer review (unregistered sha) refuses on sha, before A68',
            not g['ok'] and any('DISTINCT_REVIEW_SHA_NOT_ROOT_REGISTERED' in r for r in g['reasons']), g['reasons'])
    g = S.sensitivity_gate(config=cfg_with(bound), spec=spec)
    L.check('R11', 'sensitivity_gate: registered review still refuses while A68 comparator unreviewed',
            not g['ok'] and any('COMPARATOR_A68_SUCCESSOR_REQUIRED' in r for r in g['reasons']), g['reasons'])
    S.COMPARATOR_A68_REVIEWED = True  # in-memory only, to reach the binding checks
    try:
        g = S.sensitivity_gate(config=cfg_with(bound), spec=spec)
        L.check('R12', 'with A68 flipped in memory, registered+bound review passes review checks then refuses later (synthetic report)',
                not g['ok'] and not any('DISTINCT_REVIEW' in r for r in g['reasons']), g['reasons'])
        unb = rv('anyone', evidence=ev, comparator_report=good, runs={}, plan=S.PLAN, distance_hex='0x1p+2')
        S.REGISTERED_DISTINCT_REVIEW_SHA256 = frozenset([unb['sha256']])
        g = S.sensitivity_gate(config=cfg_with(unb), spec=spec)
        L.check('R13', 'registered sha does not excuse binding: wrong distance_hex refuses DISTINCT_REVIEW_BINDING',
                not g['ok'] and any('DISTINCT_REVIEW_BINDING' in r for r in g['reasons']), g['reasons'])
        nam = rv('Codex2', evidence=ev, comparator_report=good, runs={}, plan=S.PLAN, distance_hex=key)
        S.REGISTERED_DISTINCT_REVIEW_SHA256 = frozenset([nam['sha256']])
        g = S.sensitivity_gate(config=cfg_with(nam), spec=spec)
        L.check('R14', 'OBSERVATION: registered bytes naming Codex2 are not refused on name (trust is the root sha registration)',
                True, {'distinct_review_refusal': any('DISTINCT_REVIEW' in r for r in g['reasons']), 'reasons': g['reasons']})
    finally:
        S.COMPARATOR_A68_REVIEWED = False
    g = S.sensitivity_gate(config={}, spec={'galaxy': 'DDO154', 'physical': {'distance_Mpc': 4.04}})
    L.check('R15', 'headline D=4.04 ungated (unchanged)', g['ok'] and g['status'] == 'HEADLINE_NOT_GATED', g)
finally:
    S.REGISTERED_DISTINCT_REVIEW_SHA256 = saved
try:
    S.compute_pair(4.111497211045223, {}); ok = False; why = 'ran'
except S.Refusal as e:
    ok = str(e) == 'COMPARATOR_A68_SUCCESSOR_REQUIRED'; why = str(e)
L.check('R16', 'compute_pair refuses on A68 before plan/run reads', ok, why)
src = Path(S.__file__).read_text()
L.check('R17', 'self-attested reviewer-name denylist removed from source', "review.get('reviewer')" not in src
        and "'Codex2 build'" not in src)

out = {'schema': 'C2_REVIEW_V006R8_RESULTS_V001', 'status': 'TESTED', 'scope': 'synthetic fixtures only; no launch',
       'summary': L.summary(), 'rows': L.rows, 'fixtures_driver_normalizer_refused': NORMALIZER_REFUSED,
       'sources': [C.pin(p) for p in (W.__file__, M.__file__, S.__file__, C.R8 / 'RUN_CONFIG_DDO154_CX2V006R8_P128_MS128.json',
                                       C.R8 / 'REGISTERED_ANCHOR_CX2V006R8.json', Path(__file__))]}
res = C.write_x(RUN / 'RESULTS.json', out)
print(json.dumps({'results': res, **L.summary()}))
