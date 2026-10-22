"""Claude2-lane refute-by-default probes of Codex2 v006r9 (0557: deciding-row numerics bound to
config.numerics.block except uv_tail.eps_certificate / lo_certificate), own fixtures.

Synthetic evidence only. No launch: the r5 driver is loaded only for normalize_spec replay.
A check PASSES when the code behaves as 0557 requires (or, for OBSERVATION rows, records behaviour).
"""
import copy
import importlib.util
import json
import math
import os
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location('_c2r9_common', HERE / 'common_c2r9.py')
C = importlib.util.module_from_spec(_s)
_s.loader.exec_module(C)

RUN = C.OUT / ('run_' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '_%d' % os.getpid())
RUN.mkdir(parents=True)
L = C.Ledger()

W = C.load_pinned(C.R9 / 'calibration_orchestrator_cx2v006r9.py', '_c2r9_wrapper', C.WRAPPER_SHA)
M, S, O = W.M, W.S, W.O
CFG_PATH = C.R9 / 'RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json'
CFG = json.loads(CFG_PATH.read_bytes())
BLOCK = CFG['numerics']['block']
REG = json.loads((C.R8 / 'REGISTERED_ANCHOR_CX2V006R8.json').read_bytes())
TEMPLATE = json.loads(Path(REG['source_template']['path']).read_bytes())
DRV = C.load_pinned(CFG['driver']['path'], '_c2r9_r5_normalizer', CFG['driver']['sha256'])
MON = C.load_pinned(CFG['monitor']['path'], '_c2r9_monitor', CFG['monitor']['sha256'])
COORD = json.loads((C.ART / 'calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json').read_bytes())
SEQ = [0]
NORMALIZER_REFUSED = {}
BIND = 'DECIDING_NUMERICS_NOT_CONFIG_BLOCK'
REPLAY = []  # (cid, evidence pin, anchor) for the r8 counterfactual


def nxt():
    SEQ[0] += 1
    return SEQ[0]


def fixture_run(tag, *, physical=None, coefficients=None, numerics_edit=None):
    """Write own spec/result/finish/receipt for one synthetic COMPLETED fresh run."""
    d = RUN / ('%03d_%s' % (nxt(), tag))
    spec = {'schema': TEMPLATE['schema'], 'galaxy': 'DDO154', 'admit': {},
            'reference_compare': False, 'label': 'C2R9 SYNTHETIC FIXTURE ' + tag,
            'physical': copy.deepcopy(TEMPLATE['physical'] if physical is None else physical),
            'coefficients': copy.deepcopy(TEMPLATE['coefficients'] if coefficients is None else coefficients),
            'numerics': copy.deepcopy(BLOCK)}
    if numerics_edit:
        numerics_edit(spec['numerics'])
    sp = C.write_x(d / 'spec.json', spec)
    try:
        norm = DRV.normalize_spec(copy.deepcopy(spec))
    except Exception as exc:  # driver refuses: the forged result carries the raw spec
        norm = copy.deepcopy(spec)
        NORMALIZER_REFUSED[tag] = type(exc).__name__ + ': ' + str(exc)[:200]
    res = {'status': 'COMPLETED', 'valid': True, 'driver_sha256': M.DRIVER_SHA,
           'call_spec_sha256': sp['sha256'], 'normalized_spec': norm, 'c2r9_fixture': tag}
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


def gate_ev(ev, anchor, numerics_block=None):
    g = M.check_deciding(ev, M.DRIVER_SHA, MON, anchor=anchor,
                         numerics_block=BLOCK if numerics_block is None else numerics_block)
    return g['ok'], g['reasons']


def gate(rows, anchor, numerics_block=None, cid=None):
    ev = evidence(rows)
    if cid:
        REPLAY.append((cid, ev, anchor))
    return gate_ev(ev, anchor, numerics_block)


def classify(reasons):
    s = ' '.join(reasons)
    if BIND in s:
        return 'BINDING'
    if 'OrchestratorError' in s and any(w in s for w in ('required', 'must be', 'K_big', 'M_s', 'hull', 'workers')):
        return 'VALIDATE_BLOCK'
    if 'Refusal' in s:
        return 'DRIVER_NORMALIZER'
    return 'OTHER'


# ---------- positive controls ----------
RA = fixture_run('reanchor_exact')
W8 = fixture_run('workers8_exact')
ANCHOR = anchor_for(RA)
EXACT_EV = evidence([named(RA, 'reanchor'), named(W8, 'workers_8')])
ok, reasons = gate_ev(EXACT_EV, ANCHOR)
L.check('P1', 'exact config numerics on both rows (+registered point, anchor pins) passes', ok, reasons)
ok, reasons = gate([named(W8, 'workers_8'), named(RA, 'reanchor')], ANCHOR)
L.check('P2', 'row order does not matter (positive)', ok, reasons)
ok, reasons = gate_ev(EXACT_EV, ANCHOR, numerics_block=json.loads(json.dumps(BLOCK)))
L.check('P3', 'config block passed as an independent JSON round-trip copy passes', ok, reasons)

# certificate-only changes (excluded slots): own pinned files
cert_e = C.write_x(RUN / 'cert_eps_fixture.json', {'c2r9_fixture': 'eps'})
cert_l = C.write_x(RUN / 'cert_lo_fixture.json', {'c2r9_fixture': 'lo'})


def certs_pinned(n):
    n['uv_tail']['eps_certificate'] = copy.deepcopy(cert_e)
    n['uv_tail']['lo_certificate'] = copy.deepcopy(cert_l)


ex = copy.deepcopy(BLOCK); certs_pinned(ex)
L.check('P4', 'deciding_numerics_identity(cert-only change) == identity(config block) (canonical bytes)',
        M.canonical(M.deciding_numerics_identity(ex)) == M.canonical(M.deciding_numerics_identity(BLOCK)))
L.check('P5', 'deciding_numerics_identity does not mutate its input (eps/lo still present in the input)',
        'eps_certificate' in ex['uv_tail'] and 'lo_certificate' in ex['uv_tail'])
RAc = fixture_run('reanchor_cert_only', numerics_edit=certs_pinned)
W8c = fixture_run('workers8_cert_only', numerics_edit=certs_pinned)
ok, reasons = gate([named(RAc, 'reanchor'), named(W8c, 'workers_8')], anchor_for(RAc))
L.check('P6', 'cert-only change on both rows: not refused by the numerics binding (gate_ok recorded)',
        not any(BIND in r for r in reasons), {'gate_ok': ok, 'reasons': reasons,
                                             'normalizer_refused': NORMALIZER_REFUSED.get('reanchor_cert_only')})

# ---------- (1a) prior O2 probes rerun: must now refuse ----------
def setp(path, value):
    def f(n):
        d = n
        for k in path[:-1]:
            d = d[k]
        d[path[-1]] = value
    return f


def delp(path):
    def f(n):
        d = n
        for k in path[:-1]:
            d = d[k]
        d.pop(path[-1])
    return f


O2 = [('O2.1', 'picard.passes 2', setp(['picard', 'passes'], 2)),
      ('O2.2', 'route_a.max_iterations 8', setp(['route_a', 'max_iterations'], 8)),
      ('O2.3', 'uv_tail.quadrature.order 4', setp(['uv_tail', 'quadrature', 'order'], 4))]


def hull_one(n):
    n['brackets']['rule']['fs_absolute_overrides']['17'] = [151250000.0, 317625000.5]


NEW = [
    ('D01', 'uv_tail.gas.M_s 64', setp(['uv_tail', 'gas', 'M_s'], 64)),
    ('D02', 'uv_tail.outer.K_big_inverse_kpc 64.0', setp(['uv_tail', 'outer', 'K_big_inverse_kpc'], 64.0)),
    ('D03', 'block.column_workers 2 -> 1 (top-level campaign workers)', setp(['column_workers'], 1)),
    ('D04', 'block.column_workers 2 -> 4', setp(['column_workers'], 4)),
    ('D05', 'route_a.column_workers 8 -> 4', setp(['route_a', 'column_workers'], 4)),
    ('D06', 'brackets.rule.rfs_factors [0.8,1.2] -> [0.8,1.3]', setp(['brackets', 'rule', 'rfs_factors'], [0.8, 1.3])),
    ('D07', 'brackets.rule.le_first_factors [0.4,0.9] -> [0.5,0.9]', setp(['brackets', 'rule', 'le_first_factors'], [0.5, 0.9])),
    ('D08', 'brackets.rule.le_next_factors -> [0.8,1.2]', setp(['brackets', 'rule', 'le_next_factors'], [0.8, 1.2])),
    ('D09', 'brackets.rule.rfs_factor_overrides {} (column 71 override removed)', setp(['brackets', 'rule', 'rfs_factor_overrides'], {})),
    ('D10', 'brackets.rule.fs_absolute_overrides col 17 hull hi +0.5', hull_one),
    ('D11', 'brackets.mode rule -> fixed', setp(['brackets', 'mode'], 'fixed')),
    ('D12', 'picard.speed_change_bound_km_s 0.01 -> 0.1 (picard bound)', setp(['picard', 'speed_change_bound_km_s'], 0.1)),
    ('D13', 'picard.observe_every_pass true -> false', setp(['picard', 'observe_every_pass'], False)),
    ('D14', 'route_a.max_iterations 32 -> 64 (increase also refuses: equality, not floor)', setp(['route_a', 'max_iterations'], 64)),
    ('D15', 'uv_tail.quadrature.w_perp_max_inverse_kpc 0.05 -> 0.1', setp(['uv_tail', 'quadrature', 'w_perp_max_inverse_kpc'], 0.1)),
    ('D16', 'uv_tail.quadrature.w_z_max_inverse_kpc 0.02 -> 0.04', setp(['uv_tail', 'quadrature', 'w_z_max_inverse_kpc'], 0.04)),
    ('D17', 'composite_grid_spec.panel_orders[0] 6 -> 4', lambda n: n['composite_grid_spec']['panel_orders'].__setitem__(0, 4)),
    ('D18', 'composite_grid_spec.breaks interior -0.3 -> -0.4', lambda n: n['composite_grid_spec']['breaks_inverse_kpc'].__setitem__(4, -0.4)),
    ('D19', 'composite_grid_spec.scope string edited', lambda n: n['composite_grid_spec'].__setitem__('scope', n['composite_grid_spec']['scope'] + ' ')),
    ('D20', 'uv_tail.jet_order.route_b 2 -> 1', setp(['uv_tail', 'jet_order', 'route_b'], 1)),
    ('D21', 'uv_tail.domain.z_src_max_kpc 32.0 -> 30.0', setp(['uv_tail', 'domain', 'z_src_max_kpc'], 30.0)),
    ('D22', 'uv_tail.stars.tail_rule edited', setp(['uv_tail', 'stars', 'tail_rule'], 't_panels_20a_phase1p5_gl12')),
    ('D23', 'uv_tail.asymptote edited', setp(['uv_tail', 'asymptote'], 'EH_exact')),
    ('D24', 'REPRESENTATION: uv_tail.outer.K_big_inverse_kpc 128.0 -> 128 (int; validate_block == passes)', setp(['uv_tail', 'outer', 'K_big_inverse_kpc'], 128)),
    ('D25', 'REPRESENTATION: picard.passes 6 -> 6.0 (float)', setp(['picard', 'passes'], 6.0)),
    ('D26', 'REPRESENTATION: uv_tail.lambda_scale 1.0 -> 1 (int)', setp(['uv_tail', 'lambda_scale'], 1)),
    ('D27', 'extra key numerics.c2r9_extra', setp(['c2r9_extra'], 1)),
    ('D28', 'extra key picard.max_passes', setp(['picard', 'max_passes'], 6)),
    ('D29', 'picard.speed_change_bound_km_s removed', delp(['picard', 'speed_change_bound_km_s'])),
    ('D30', 'cert slot moved to numerics top level (numerics.eps_certificate added)', setp(['eps_certificate'], 'PENDING_UV_TAIL_CERTIFICATE')),
    ('D31', 'cert-only change PLUS picard.passes 5 (exclusion does not mask a real change)',
     lambda n: (certs_pinned(n), setp(['picard', 'passes'], 5)(n))),
]

DEV_OBS = {}
for cid, label, fn in O2 + NEW:
    # (a) reanchor deviates, config.anchor rebound to it (only the numerics binding can catch it)
    bad = fixture_run('reanchor_' + cid, numerics_edit=fn)
    ok_a, reasons_a = gate([named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad), cid=cid + '.ra')
    # (b) workers_8 deviates, reanchor exact
    badw = fixture_run('workers8_' + cid, numerics_edit=fn)
    ok_b, reasons_b = gate([named(RA, 'reanchor'), named(badw, 'workers_8')], ANCHOR, cid=cid + '.w8')
    # (c) reverse direction: rows exact, config block deviates (binding isolated from validate_block)
    dev = copy.deepcopy(BLOCK); fn(dev)
    ok_c, reasons_c = gate_ev(EXACT_EV, ANCHOR, numerics_block=dev)
    cls = (classify(reasons_a), classify(reasons_b))
    DEV_OBS[cid] = {'label': label, 'reanchor_class': cls[0], 'workers8_class': cls[1],
                    'reverse_class': classify(reasons_c)}
    L.check(cid + '.ra', label + ': as reanchor (config.anchor rebound) refuses', not ok_a,
            {'class': cls[0], 'reasons': reasons_a})
    L.check(cid + '.w8', label + ': as workers_8 row refuses', not ok_b, {'class': cls[1], 'reasons': reasons_b})
    L.check(cid + '.rev', label + ': rows exact vs deviated config block refuses on the binding',
            (not ok_c) and any(BIND in r for r in reasons_c), reasons_c)

# The fields validate_block does NOT cover must be caught by the binding itself (not incidentally).
VB_COVERED = {'D01', 'D02', 'D05', 'D10'}
not_binding = [c for c in [x[0] for x in O2 + NEW] if c not in VB_COVERED and
               (DEV_OBS[c]['reanchor_class'] != 'BINDING' or DEV_OBS[c]['workers8_class'] != 'BINDING')]
L.check('B1', 'every deviation outside validate_block refuses with DECIDING_NUMERICS_NOT_CONFIG_BLOCK on both rows',
        not not_binding, {'not_binding': not_binding})

# missing cert keys: identity passes but the actual driver normalization must refuse
miss = lambda n: (n['uv_tail'].pop('eps_certificate'), n['uv_tail'].pop('lo_certificate'))
bad = fixture_run('reanchor_missing_certs', numerics_edit=miss)
ok, reasons = gate([named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))
L.check('K1', 'both cert keys absent: identity exclusion does not admit it; gate refuses (driver normalization)',
        not ok and not any(BIND in r for r in reasons), {'reasons': reasons,
                                                       'normalizer_at_fixture': NORMALIZER_REFUSED.get('reanchor_missing_certs')})
bad = fixture_run('reanchor_missing_eps', numerics_edit=lambda n: n['uv_tail'].pop('eps_certificate'))
ok, reasons = gate([named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))
L.check('K2', 'eps cert key absent only: gate refuses', not ok, reasons)

# NONE_TEST_ONLY certificate sentinel: observation only (cert validity is out of 0557 scope)
tonly = lambda n: (n['uv_tail'].__setitem__('eps_certificate', DRV.UVT_TEST_ONLY),
                   n['uv_tail'].__setitem__('lo_certificate', DRV.UVT_TEST_ONLY))
bt = fixture_run('reanchor_test_only_certs', numerics_edit=tonly)
bw = fixture_run('workers8_test_only_certs', numerics_edit=tonly)
ok, reasons = gate([named(bt, 'reanchor'), named(bw, 'workers_8')], anchor_for(bt))
L.check('K3', 'OBSERVATION: NONE_TEST_ONLY certificate sentinels in both deciding rows (forged COMPLETED result) - gate_ok recorded',
        True, {'gate_ok': ok, 'reasons': reasons,
               'normalizer_at_fixture': NORMALIZER_REFUSED.get('reanchor_test_only_certs')})

# direct unbound call fails closed
if M.DECIDING_NUMERICS_CONTEXT.get() is None:
    g = M.check_deciding(EXACT_EV, M.DRIVER_SHA, MON, anchor=ANCHOR)
    L.check('U1', 'direct call with anchor but no numerics context/argument fails closed',
            not g['ok'] and any('DECIDING_CONFIG_NUMERICS_BLOCK_REQUIRED' in r for r in g['reasons']), g['reasons'])
for cid, blk in [('U2', {}), ('U3', {'uv_tail': 'x'}), ('U4', [])]:
    g = M.check_deciding(EXACT_EV, M.DRIVER_SHA, MON, anchor=ANCHOR, numerics_block=blk)
    L.check(cid, 'malformed numerics_block %r fails closed' % (blk,), not g['ok'], g['reasons'])


# ---------- (1b) actual Context binding ----------
def local_cfg(label, ev, anchor, block=None):
    c = copy.deepcopy(CFG)
    d = RUN / ('ctx_' + label)
    c['work_dir'] = str(d); c['work_dir_volume'] = None
    c['work_dir_identity'] = {'resolved': str(d.resolve()), 'volume': None, 'volume_uuid': None, 'symlinks': []}
    c['anchor'] = copy.deepcopy(anchor)
    c['deciding_test'] = ev
    if block is not None:
        c['numerics']['block'] = block
    return c


def ctx_gate(cfg):
    try:
        ctx = W.Context(cfg)
        return ctx, ctx.gates['deciding_test']
    except Exception as exc:
        return None, {'ok': False, 'reasons': ['CONSTRUCT ' + type(exc).__name__ + ': ' + str(exc)[:300]]}


ctxA, gA = ctx_gate(local_cfg('A_exact', EXACT_EV, ANCHOR))
L.check('X1', 'actual Context, exact rows + exact config: deciding gate ok', gA['ok'], gA.get('reasons'))
bad = fixture_run('ctx_reanchor_picard2', numerics_edit=O2[0][2])
ev_bad = evidence([named(bad, 'reanchor'), named(W8, 'workers_8')])
ctxB, gB = ctx_gate(local_cfg('B_reduced_rows', ev_bad, anchor_for(bad)))
L.check('X2', 'actual Context: reduced-numerics reanchor (anchor rebound) refuses on the binding',
        not gB['ok'] and any(BIND in r for r in gB['reasons']), gB['reasons'])
if ctxB is not None:
    fg = ctxB.fresh_gates()
    L.check('X3', 'actual inherited fresh_gates also refuses it', not fg['deciding_test']['ok'] and
            any(BIND in r for r in fg['deciding_test']['reasons']), fg['deciding_test']['reasons'])
# config block itself changed, rows match it: deciding binding follows the config (by design)
blk12 = copy.deepcopy(BLOCK); NEW[11][2](blk12)
r12 = fixture_run('ctx_reanchor_D12', numerics_edit=NEW[11][2])
w12 = fixture_run('ctx_workers8_D12', numerics_edit=NEW[11][2])
ev12 = evidence([named(r12, 'reanchor'), named(w12, 'workers_8')])
ctxC, gC = ctx_gate(local_cfg('C_config_changed', ev12, anchor_for(r12), block=blk12))
L.check('X4', 'OBSERVATION: config block changed (picard bound 0.1) + matching rows -> deciding gate ok; '
        'numerics_verdict gate (V007 ADOPT) remains not ok', True,
        {'deciding_ok': gC['ok'], 'deciding_reasons': gC.get('reasons'),
         'numerics_verdict_ok': None if ctxC is None else ctxC.gates['numerics_verdict']['ok'],
         'numerics_verdict_reasons': None if ctxC is None else ctxC.gates['numerics_verdict']['reasons'][:2]})
ctxD, gD = ctx_gate(local_cfg('D_cross', EXACT_EV, ANCHOR, block=blk12))
L.check('X5', 'actual Context: exact rows under a changed config block refuse (cross-config)',
        not gD['ok'] and any(BIND in r for r in gD['reasons']), gD['reasons'])
if ctxA is not None and ctxC is not None:
    a1 = ctxA.fresh_gates()['deciding_test']['ok']
    c1 = ctxC.fresh_gates()['deciding_test']['ok']
    a2 = ctxA.fresh_gates()['deciding_test']['ok']
    L.check('X6', 'A -> C -> A fresh_gates: each context uses its own block (no leak)',
            a1 and c1 and a2 and M.DECIDING_NUMERICS_CONTEXT.get() is None, [a1, c1, a2])
    # in-memory mutation of the running context's config block is caught at fresh_gates
    ctxA.cfg['numerics']['block']['picard']['passes'] = 2
    fgm = ctxA.fresh_gates()
    L.check('X7', 'running Context: cfg block mutated to picard 2 -> fresh_gates deciding refuses (exact rows) '
            'and numerics_verdict flags the changed block',
            not fgm['deciding_test']['ok'] and any(BIND in r for r in fgm['deciding_test']['reasons'])
            and not fgm['numerics_verdict']['ok'], {'deciding': fgm['deciding_test']['reasons'],
                                                     'numerics_verdict': fgm['numerics_verdict']['reasons'][:3]})
    ctxA.cfg['numerics']['block']['picard']['passes'] = 6
# exception inside super().__init__ restores both ContextVars
cfgE = local_cfg('E_exception', EXACT_EV, ANCHOR)
cfgE['monitor'] = dict(cfgE['monitor'], sha256='0' * 64)
try:
    W.Context(cfgE); raised = False
except Exception as exc:
    raised = type(exc).__name__ + ': ' + str(exc)[:120]
L.check('X8', 'exception during inherited init: both ContextVars restored to None',
        bool(raised) and M.DECIDING_NUMERICS_CONTEXT.get() is None and M.ANCHOR_CONTEXT.get() is None, raised)
cfgF = local_cfg('F_bad_block', EXACT_EV, ANCHOR, block={'picard': {}})
try:
    W.Context(cfgF); okF = False; why = 'constructed'
except Exception as exc:
    okF = True; why = type(exc).__name__ + ': ' + str(exc)[:160]
L.check('X9', 'Context refuses a config block without uv_tail before binding; ContextVars None',
        okF and M.DECIDING_NUMERICS_CONTEXT.get() is None, why)

# ---------- (3) r8 protections spot-check ----------
seed = COORD['trial_point']['engine_seed_theta']
seed_phys = copy.deepcopy(TEMPLATE['physical'])
seed_phys.update(common_scale_s=seed['common_scale_s'], ell_F_m=seed['ell_F_m'],
                 gamma=seed['gamma_over_Eref'] * seed['Eref_base_J'], distance_Mpc=seed['distance_Mpc'])
bad = fixture_run('sp_seed_logexp', physical=seed_phys)
ok, reasons = gate([named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))
L.check('Q1', 'r8 N1: log/exp engine-seed coordinate refuses as reanchor',
        not ok and any('REANCHOR_NOT_EXACT_REGISTERED_A2F10_POINT' in r for r in reasons), reasons)
ph = copy.deepcopy(TEMPLATE['physical']); ph['distance_Mpc'] = math.nextafter(4.04, 5.0)
bad = fixture_run('sp_D_ulp', physical=ph)
ok, reasons = gate([named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))
L.check('Q2', 'r8 N3: D = 4.04 + 1 ulp refuses', not ok, reasons)
raw = Path(TEMPLATE['coefficients']['path']).read_bytes()
same = C.write_x(RUN / 'coef_exact_copy.npz', raw)
bad = fixture_run('sp_coef_copy', coefficients=same)
ok, reasons = gate([named(bad, 'reanchor'), named(W8, 'workers_8')], anchor_for(bad))
L.check('Q3', 'r8 C2: byte-identical coefficient copy at another path refuses', not ok, reasons)
RA2 = fixture_run('sp_second_fresh_exact')
ok, reasons = gate([named(RA2, 'reanchor'), named(W8, 'workers_8')], ANCHOR)
L.check('Q4', 'r8 S1: second fresh exact-point run (config.anchor pins the first) refuses',
        not ok and any('REANCHOR_ROW_CONFIG_ANCHOR_PIN_MISMATCH' in r for r in reasons), reasons)
ok, reasons = gate([named(W8, 'reanchor'), named(RA, 'workers_8')], ANCHOR)
L.check('Q5', 'r8 S2: workers_8 run relabelled reanchor refuses',
        not ok and any('REANCHOR_ROW_CONFIG_ANCHOR_PIN_MISMATCH' in r for r in reasons), reasons)
r_sw = named(RA, 'reanchor'); r_sw['receipt'] = copy.deepcopy(W8['receipt'])
w_sw = named(W8, 'workers_8'); w_sw['receipt'] = copy.deepcopy(RA['receipt'])
a = copy.deepcopy(ANCHOR); a['receipt'] = copy.deepcopy(W8['receipt'])
ok, reasons = gate([r_sw, w_sw], a)
L.check('Q6', 'r8 W4: receipts swapped, config.anchor.receipt consistent with swap: refuses', not ok, reasons)
a = copy.deepcopy(ANCHOR); a['registered_point'] = dict(a['registered_point'], path=str(C.R8) + '/./REGISTERED_ANCHOR_CX2V006R8.json')
ok, reasons = gate([named(RA, 'reanchor'), named(W8, 'workers_8')], a)
L.check('Q7', 'r8 T2: registered_point path alias refuses', not ok, reasons)
ok, reasons = gate([named(RA, 'reanchor'), named(W8, 'workers_8')], CFG['anchor'])
L.check('Q8', 'r8 W12: shipped config.anchor (pending) refuses a well-formed pair',
        not ok and any('PENDING' in r for r in reasons), reasons)
cfgT = local_cfg('T_anchor_tamper', EXACT_EV, ANCHOR); cfgT['anchor']['physical']['distance_Mpc'] = 4.0400001
try:
    W.Context(cfgT); ok = False; why = 'constructed'
except M.Error as exc:
    ok = 'CONFIG_ANCHOR_REGISTRATION_MISMATCH' in str(exc); why = str(exc)
L.check('Q9', 'r8 X4: Context refuses tampered config.anchor physical at construction', ok, why)
L.check('Q10', 'r8 R1: sensitivity review allowlist is an empty frozenset',
        S.REGISTERED_DISTINCT_REVIEW_SHA256 == frozenset() and type(S.REGISTERED_DISTINCT_REVIEW_SHA256) is frozenset)
try:
    S.compute_pair(4.111497211045223, {}); ok = False; why = 'ran'
except S.Refusal as e:
    ok = str(e) == 'COMPARATOR_A68_SUCCESSOR_REQUIRED'; why = str(e)
L.check('Q11', 'r8 R16: compute_pair refuses on A68 before plan/run reads', ok, why)
L.check('Q12', 'sensitivity module is the r8 file at sha 8fb06600 (from bytes) and A68 flag false',
        C.sha_file(S.__file__) == '8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f'
        and Path(S.__file__).resolve() == (C.R8 / 'sensitivity_policy_cx2v006r8_v002.py').resolve()
        and S.COMPARATOR_A68_REVIEWED is False, S.__file__)
g = S.sensitivity_gate(config={}, spec={'galaxy': 'DDO154', 'physical': {'distance_Mpc': 4.04}})
L.check('Q13', 'headline D=4.04 ungated (unchanged)', g['ok'] and g['status'] == 'HEADLINE_NOT_GATED', g)
L.check('Q14', 'ANCHOR_CONTEXT and DECIDING_NUMERICS_CONTEXT None after all r9 work',
        M.ANCHOR_CONTEXT.get() is None and M.DECIDING_NUMERICS_CONTEXT.get() is None)

# ---------- r8 counterfactual: the same deviation evidence through the r8 core ----------
W8MOD = C.load_pinned(C.R8 / 'calibration_orchestrator_cx2v006r8_v004.py', '_c2r9_r8wrapper', C.R8_WRAPPER_SHA)
r8_accepts = {}
for cid, ev, anc in REPLAY:
    g = W8MOD.M.check_deciding(ev, W8MOD.M.DRIVER_SHA, MON, anchor=anc)
    r8_accepts[cid] = g['ok']
acc = sorted(k for k, v in r8_accepts.items() if v)
L.check('R8CF', 'COUNTERFACTUAL (observation): deviation cases the r8 core accepted, all refused by r9',
        True, {'r8_accepted': acc, 'n_replayed': len(r8_accepts)})

out = {'schema': 'C2_REVIEW_V006R9_RESULTS_V001', 'status': 'TESTED', 'scope': 'synthetic fixtures only; no launch',
       'summary': L.summary(), 'rows': L.rows, 'deviation_classes': DEV_OBS,
       'r8_counterfactual_accepts': r8_accepts, 'fixtures_driver_normalizer_refused': NORMALIZER_REFUSED,
       'sources': [C.pin(p) for p in (W.__file__, M.__file__, S.__file__, CFG_PATH,
                                       C.R8 / 'REGISTERED_ANCHOR_CX2V006R8.json', W8MOD.__file__, W8MOD.M.__file__,
                                       Path(__file__), HERE / 'common_c2r9.py')]}
res = C.write_x(RUN / 'RESULTS.json', out)
print(json.dumps({'results': res, **L.summary(), 'r8_accepted': acc}))
