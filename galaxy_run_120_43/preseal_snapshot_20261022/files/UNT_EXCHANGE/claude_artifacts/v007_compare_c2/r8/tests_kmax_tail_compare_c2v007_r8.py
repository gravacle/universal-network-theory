"""Tests of kmax_tail_compare_c2v007_r8.py (V007 compare R8, Claude2 root lane).  R8 = the R7 suite, adapted only where an
A67 ruling changes a premise (the TEST registry is schema C2V002: gate_records [A67 N2] -- the fixture SR_K record of record
registered by sha, every other gate PRODUCED_AFTER_THE_SEAL, and run_eval registering every record it writes -- and
gq_all_nodes_counts [A67 SF1]; every DDO GQ roster carries its geometry and that geometry's production count; every identity
run runs on driver v010 r5 b5cc62af [A67 N1]; the RB_FP fixture ranges end exactly at sqrt(2) x 128 [A67 N3]; the r7 probe
G9 / G8-G10 worlds re-based on the record of record GQ_CERT_V005_MS128 [A67 SF1, SF2]), plus one test (or more) per A67
item (ids 'A67.*' in 'covers'; function r8_tests).
R7 = the R6 suite, adapted only where an
A62 ruling or an r6-recheck fix changes a premise (the fixture now carries: a TEST producer registry naming the fixture producers
[A62.2], passed to the CLI by --test-producer-registry; comparator/tokens on the identity-gate records [A57.3, A59]; EPS shells
covering the declared coverage and the full envelope fields [SF3, SF4]; GQ named rosters DDO_C2T / DDO_C3T reaching P = 128 and
all_nodes on every DDO roster [SF1, SF2]; RB_FP shell ranges covering [4, sqrt(2) x 128] with full_tail_domain true [A62.1];
the v010 r5 driver b5cc62af in every T-case drivers_allowed and the r5 custody pins [A62.3]), plus one test (or more) per A62
item and per r6-recheck finding (ids 'A62.*', 'R7.*' in 'covers'; function r7_tests), the recheck probe worlds re-built as
regression tests where feasible.
R6 = the R5 suite, adapted only where a ruling
made after r5 changes a premise (the fixture registers P = 128 [A55, A56 follow-up 1]: C4T-KLO 64, C4T-KHI 256, gas M_s 128
[A57], EPS DDO coverage 363 and NGC 46 [A58 RI-17], the LO partition to 363 with source_gas_M_s 128 [A58 RI-06], DOUBLING at
K_big 128 and 256 with gas M_s 128 [A58 RI-03], GQ rosters at M_s 128 / NGC 96 reaching 2P = 256 [A57]; the q cap removed
[A58 RI-18]; the alternating per-row bound [A56 N1]), plus one test (or more) per A54 S9, A55, A56, A57, A58 ruling the
compare reads and per r5-recheck finding (ids 'S9', 'A55.*', 'A56.*', 'A57.*', 'A58.*', 'R6.*' in 'covers'; function
r6_tests), the recheck probe worlds re-built as regression tests where feasible.
R5 = the R4 suite, adapted only where an A53 /
A54 ruling changes a premise (labels C4T-K16/K64 -> C4T-KLO/KHI and pairs T3_K16/K64 -> T3_KLO/KHI [A54 generic T3]; PICARD
R-PAIR members in the A53 shape [admit the base route A]; consistent producer verdicts [A54 S5]; EPS/LO coverage sqrt(2) x 2P
[A54]), plus one test (or more) per A53 / A54 ruling, per Claude3 0053 finding and per r4-recheck finding (ids 'A53.*', 'A54.*',
'C3.*', 'R5.*' in 'covers'; function r5_tests), Claude3's probe worlds re-built as regression tests where feasible.
R4 = the R3 suite (adapted only where an R4
fix changes a fixture: C4T-D5 runs on the nodes_v001 RO1 workers; ROUTE_A R-PAIR members carry their own route-A identity),
plus one test (or more) per fixed R3-recheck finding (ids 'R4.*' in 'covers').  The R1 suite (one test per pre-named
outcome, per A48 ruling, per fixed verify_v001 finding, plus the A47 clause tests), adapted where A50 changed a reading,
plus one test (or more) per A50 item and per fixed R1-recheck finding (ids 'A50.*' in 'covers').  Base rows are the REAL R3
results (C2R3/C3R3/C4R3 forward-model rows, read-only); every other run is synthetic (rows = C4R3 + k*tau_i), with no
observed velocity anywhere (tau and sigma come from the pinned V005 prereg).  CLI tests run on real R3 / C5R3 bytes and on
synthetic run directories written under OUT.  The registered C5H run (runs_ext/KMAX_A2F10_C5H_RUN_V001) is never named.
Writes only into OUT (must not exist).
usage: python3 -I -B tests_kmax_tail_compare_c2v007_r7.py OUT"""
import builtins
import copy
import hashlib
import importlib.util
import io
import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
CMP = HERE / 'kmax_tail_compare_c2v007_r8.py'
CT = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
V010 = None              # R7 [A62.3] (R8 [A67 N1]: also every identity run's driver): set below to the pinned driver v010 r5 sha (every T-case drivers_allowed = [b5cc62af])
CANARY = '41.2345678'
FORBIDDEN = 'KMAX_A2F10_C5H_RUN_V001'


def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


M = load(CMP, 'cmp7r8')
V010 = M.PIN_DRIVER_V010_R5[1]
CTX = M.build_context()
IDS = CTX['ids']
TAU = CTX['tau']
RADII = CTX['row_radii_m']
LIB = M.load_uvt_lib()
REAL = {k: CTX['C5M'].adapt_result(M.PIN_R3[k][0]) for k in ('C2R3', 'C3R3', 'C4R3')}
for k in REAL:
    assert REAL[k]['result_sha256'] == M.PIN_R3[k][1]


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


# R7 [A62.2] the TEST producer registry: the fixture producers (sha(gate)), the fixture identity comparator / token sets, and the
# real EPS_CERT_V006 producer (read by the A53 NEW-19 test); NOT a root registration.  CLI tests pass it as a file (REGARGS).
REAL_EPS_V006 = M.ART + '/tail_scheme_impl_c2/certificates_v002/gates/EPS_CERT_V006.json'
# R8 [A67 SF1] the fixture production node counts per geometry (the certificates_v003 part-record values of these geometries)
GQ_GEOMETRY = {'DDO_C2T': ('C2T_KB128', 1059379200), 'DDO_C3T': ('C3T_KB128', 1060288000), 'DDO_C4T': ('C4T_KB256', 4219494400)}
# R8 [A67 N2] gate_records: SR_K by sha (its fixture record of record, appended below once complete_records exists); every
# other gate PRODUCED_AFTER_THE_SEAL here (run_eval registers every record it writes, by sha, for every gate)
REG_OBJ = {'schema': M.PRODUCER_REGISTRY_SCHEMA, 'producers': {g: [sha(g)] for g in M.ALL_GATES},
           'identity_comparators': [sha('comparator')], 'identity_tokens': {g: [sha('tokens' + g)] for g in M.IDENTITY_GATES},
           'gate_records': dict({g: M.GATE_RECORD_AFTER_SEAL for g in M.ALL_GATES if g != 'SR_K'}, SR_K=[]),
           'gq_all_nodes_counts': {geo: n for geo, n in GQ_GEOMETRY.values()},
           'note': 'TEST registry of the R8 suite (fixture producers and records); not a root registration'}
REG_OBJ['producers']['EPS'].append(json.loads(Path(REAL_EPS_V006).read_bytes())['producer']['sha256'])
CTX['producer_registry'] = M.producer_registry_from_obj(REG_OBJ)
REGARGS = []              # ['--test-producer-registry', <file>], set when main() writes the registry file


def ident(g):
    """R7 [A57.3] [A59] the comparator / token fields of an identity-gate record (fixture shas, registered in REG_OBJ)."""
    return {'comparator': {'path': '/synthetic/run_identity_compare.py', 'sha256': sha('comparator')},
            'tokens': {'path': '/synthetic/TOKENS_%s.json' % g, 'sha256': sha('tokens' + g)}}


# ---------------------------------------------------------------------------------------------------- registered configs
def uv_cfg(lab):
    """A library-valid uv_tail block per T-case, shaped like the v010 V007 templates (certificates filled synthetically)."""
    c = {'asymptote': 'EH_exact_minus_quarter', 'domain': {'R_eval_max_kpc': 14.2, 'z_eval_max_kpc': 35.0, 'z_src_max_kpc': 32.0},
         'enabled': True, 'eps_certificate': {'path': '/synthetic/EPS.json', 'sha256': '1' * 64}, 'gas': {'M_s': 128, 'interp': 'lagrange3_s_gl4'},
         'jet_order': {'ngc_eval': 1, 'route_a': 1, 'route_b': 2}, 'lambda_scale': 1.0, 'lapse_only': True,
         'lo_certificate': {'path': '/synthetic/LO.json', 'sha256': '2' * 64}, 'outer': {'K_big_inverse_kpc': 128.0, 'shape': 'cylinder'},
         'quadrature': {'order': 8, 'w_perp_max_inverse_kpc': 0.05, 'w_z_max_inverse_kpc': 0.02}, 'source_rule': 'continuum_v001',
         'stars': {'segment_rule': 'max16_ceil_kdr_plus8', 'tail_rule': 't_panels_40a_phase1p5_gl12'}}
    if lab == 'C4T-KLO':                                   # [A55] P = 128: KLO = P/2 = 64, KHI = 2P = 256
        c['outer'] = {'K_big_inverse_kpc': 64.0, 'shape': 'cylinder'}
    if lab == 'C4T-KHI':
        c['outer'] = {'K_big_inverse_kpc': 256.0, 'shape': 'cylinder'}
    if lab == 'C4T-A':
        c['lambda_scale'] = 1.05
    if lab == 'C4T-C5c':
        c['outer'] = {'K_out_inverse_kpc': 5.0, 'shape': 'cube'}
    if lab == 'C4T-D5':
        c['source_rule'] = {'rule': 'nodes_v001', 'ext_grid': CTX['grids']['G5']}
    return c


UVT_SHA = {lab: LIB.normalize_config(uv_cfg(lab))['sha256'] for lab in M.T_CASES}


WORKER_SERIAL, WORKER_PARALLEL, BINDING = (M.PIN_RO1_CUSTODY[k][1] for k in ('worker', 'worker_parallel', 'binding'))
NODES_SERIAL, NODES_PARALLEL = (M.PIN_RO1_NODES_CUSTODY[k][1] for k in ('worker', 'worker_parallel'))   # [R4 validity F1]


def ro1b(fired=False, armed=True, cw=8, events=None, nodes=False):
    """An RO1 c2v002 record (route_a_outcome.ro1): worker/binding from the custody list when armed, null when not.
    [R4 validity F1] nodes=True: the nodes_v001 RO1 workers v010 r4 runs for C4T-D5 (and its R-PAIR member)."""
    ws, wp = (NODES_SERIAL, NODES_PARALLEL) if nodes else (WORKER_SERIAL, WORKER_PARALLEL)
    return {'rule': 'RO1', 'fired': fired, 'armed': armed, 'events': list(events or []),
            'worker_sha256': (ws if cw == 1 else wp) if armed else None,
            'binding_sha256': BINDING if armed else None}


def numerics_for(lab, cw=8):
    """[A50 S1] built on the C5H spec numerics as normalized by its dry run (the reference of the C5H run and of RA1)."""
    n = copy.deepcopy(CTX['c5h_numerics_reference'])
    n['truncation'] = dict(M.EXPECTED_TRUNCATION[lab])
    n['composite_grid_spec'] = copy.deepcopy(CTX['grids'][M.EXPECTED_GRID[lab]])
    if lab != M.C5H:
        n['uv_tail'] = uv_cfg(lab)
        n['route_a'] = {'column_workers': cw, 'max_iterations': 32}
    return n


def case_block(mode=None, cw=8, over=None, keymap=None):
    cb = {'schema': M.CASE_BLOCK_SCHEMA, 'cases': {}}
    if mode:
        cb['route_a_mode'] = mode
    if keymap is not None:
        cb['key_equivalence_map'] = keymap
    for lab in M.REGISTERED:
        e = {'grid': M.EXPECTED_GRID[lab], 'truncation': M.EXPECTED_TRUNCATION[lab], 'normalized_spec_equal': {}}
        if lab == M.C5H:
            e.update(tail=False, ro1_required=False, call_spec_sha256=M.PIN_C5H_SPEC[1], drivers_allowed=[M.DRIVER_V009_EXT])
        else:
            e.update(tail=True, ro1_required=True, uv_tail_config_sha256=UVT_SHA[lab], drivers_allowed=[V010],
                     normalized_spec_equal={'/numerics': numerics_for(lab, cw)})
        cb['cases'][lab] = e
    if over:
        over(cb)
    return cb


CB = case_block()
assert not M.validate_case_block(CB), M.validate_case_block(CB)
CB_SERIAL = case_block('serial_with_exemption', cw=1)
assert not M.validate_case_block(CB_SERIAL), M.validate_case_block(CB_SERIAL)


def passes_from(final, dlast=0.0005, q=1 / 3.0, n=3):
    """n Picard passes ending at final: d_last = -dlast, d_prev = -dlast/q (so the E_i ratio is q)."""
    p3 = dict(final)
    p2 = {i: final[i] + dlast for i in IDS}
    p1 = {i: p2[i] + dlast / q for i in IDS}
    return [p1, p2, p3][3 - n:]


def receipt_for(rsha, rpath, spec, drv, status='COMPLETED'):
    return {'schema': M.RECEIPT_SCHEMA, 'status': 'FINISHED' if status == 'COMPLETED' else 'CHILD_FAILED',
            'driver_status': status, 'exit_code': 0 if status == 'COMPLETED' else 3, 'stop_reason': None,
            'result': {'path': rpath, 'sha256': rsha}, 'pins': {'spec': {'sha256': spec}, 'driver': {'sha256': drv}}}


def make_run(lab, rows, *, dlast=0.0005, q=1 / 3.0, ea=0.005, flagged=False, cw=8, driver=None, ro1=None, maxit=32,
             numerics=None, ra_ident='e' * 64, uvt_over=None, present=True, ea_none=False, probe=True, npass=3, receipt=True,
             last_change=None, raw_ids=None, key=None):
    """A synthetic run in exactly the read_run() layout (receipt included: A48 AMB-26)."""
    if not present:
        return {'label': lab, 'present': False, 'absent': 'NOT_IN_MANIFEST'}
    base = lab.split('@')[0]
    c5m = lab.startswith(M.C5H + '@RPAIR:')          # [A50 root item 11] C5H R-PAIR member: v010 tail OFF, RO1 armed
    rows = dict(rows)
    num = numerics if numerics is not None else numerics_for(base, cw)
    if base != M.C5H:
        num.setdefault('route_a', {})['max_iterations'] = maxit
    ns = {'galaxy': 'DDO154', 'physical': CTX['anchor']['physical'], 'coefficients': CTX['anchor']['coefficients'], 'numerics': num}
    pr = passes_from(rows, dlast, q, npass)
    rsha = sha(json.dumps([key or lab, rows, dlast, q, ea, flagged, cw, maxit, npass, M.canon(num)]))
    rpath = '/synthetic/%s/result.json' % lab
    rao = {'classification': 'CONVERGED', 'converged_iteration': 6, 'result_path': '/synthetic', 'result_sha256': 'f' * 64}
    if base != M.C5H or c5m:
        rao['ro1'] = ro1 if ro1 is not None else ro1b(cw=(num.get('route_a') or {}).get('column_workers', 8), nodes=(base == 'C4T-D5'))
    drv = driver or (M.DRIVER_V009_EXT if (base == M.C5H and not c5m) else V010)
    spec = M.PIN_C5H_SPEC[1] if (base == M.C5H and not c5m) else sha('spec' + lab)
    result = {'schema': M.RESULT_SCHEMA, 'status': 'COMPLETED', 'valid': True, 'normalized_spec': ns,
              'driver_sha256': drv, 'call_spec_sha256': spec, 'route_a_outcome': rao}
    adapted = {'schema': M.RESULT_SCHEMA, 'status': 'COMPLETED', 'valid': True, 'rows': rows, 'result_sha256': rsha,
               'last_change_km_s': dlast if last_change is None else last_change, 'route_a_identity_sha256': ra_ident,
               'm4_row_window': 0.01, 'normalized_spec': ns}
    uvt = None
    if base != M.C5H:
        uvt = {'schema': M.UVT_RA_RECORD_SCHEMA, 'outcome': 'CONVERGED_FINITE_FIXED_POINT', 'production_admissible': True,
               'admissibility': 'production', 'config_sha256': UVT_SHA[base], 'flags': [M.FLAG_TSU] if flagged else [],
               'monitor_status': 'FLAGGED' if flagged else 'M_T_WITHIN_THRESHOLD', 'M_T_threshold': 0.25,
               'M_T_accepted': 0.3 if flagged else 0.05, 'accepted_iteration': 6,
               'E_A_rows_km_s_accepted': None if ea_none else [ea * TAU[i] for i in IDS]}
        if probe:
            uvt['probe_R_m'] = list(RADII)
        uvt.update(uvt_over or {})
    return {'label': lab, 'dir': '/synthetic/' + lab, 'present': True, 'result': result, 'result_sha256': rsha, 'adapted': adapted,
            'adapted_sha_equal': True, 'finish': {'result_sha256': rsha}, 'receipt': receipt_for(rsha, rpath, spec, drv) if receipt else None,
            'spec_for_reading': ns, 'spec_source': 'result', 'pass_rows': pr, 'route_a_outcome': rao, 'uvt_record': uvt,
            'uvt_code': None, 'failure': None, 'ro1_required': base != M.C5H, 'result_path': rpath, 'read_codes': [],
            'raw_row_ids': list(raw_ids) if raw_ids is not None else list(rows)}


def identity_run(name, ro1_fired=False, receipt=True, receipt_sha=None, armed=None, ro1_over=None, cw=1):
    if armed is None:                       # [A52.1] B0prime_RERUN: armed false (exempt from A50 item 12); Z2, Z2-OFF: armed
        armed = name != 'B0prime_RERUN'
    rows = REAL['C2R3']['rows']
    rsha = sha('id' + name)
    rpath = '/synthetic/id/%s/result.json' % name
    spec, drv = sha('idspec' + name), V010                 # R8 [A67 N1] every identity run on driver v010 r5 (r7: a fixture sha)
    ns = {'numerics': {'route_a': {'column_workers': cw}}} if cw is not None else {}   # [R3 order N8] the kind check reads it
    return {'label': name, 'present': True, 'result': {'status': 'COMPLETED', 'call_spec_sha256': spec, 'driver_sha256': drv,
                                                       'normalized_spec': ns},
            'result_sha256': rsha, 'adapted_sha_equal': True, 'result_path': rpath, 'read_codes': [], 'raw_row_ids': list(rows),
            'adapted': {'status': 'COMPLETED', 'valid': True, 'rows': rows}, 'finish': {'result_sha256': rsha}, 'failure': None,
            'receipt': receipt_for(receipt_sha or rsha, rpath, spec, drv) if receipt else None,
            'route_a_outcome': {'ro1': dict(ro1b(fired=ro1_fired, armed=armed, cw=1),
                                            events=[{'code': M.RO1_CODE, 'refusal': M.READOUT_REFUSALS[0], 'query': 3, 'phi_rad': 0.785,
                                                     'R_kpc': 1.48, 'numerator': -0.2, 'denominator': 1.0, 'after_convergence': True}]
                                            if ro1_fired else [], **(ro1_over or {}))}}


def a53_picard_shape(run, base, keep=()):
    """[A53] an R-PAIR PICARD member admits its base run's route A: the base's route_a_outcome (classification, iteration,
    result path and sha) and tail record, the base's route-A identity, route_a.column_workers 1 (planning only); a T-case
    member carries the base's RO1 record; the C5H member carries no ro1_workers and an ro1 block armed false, fired false.
    keep: fields a test set explicitly ('ro1', 'ra_ident', 'uvt_over')."""
    c5 = run['label'].split('@')[0] == M.C5H
    num = run['result']['normalized_spec']['numerics']
    num.setdefault('route_a', {})['column_workers'] = M.RPAIR_PICARD_COLUMN_WORKERS
    if c5:
        num['route_a'].pop('ro1_workers', None)
    rao = copy.deepcopy(base['route_a_outcome'])
    if 'ro1' in keep:
        rao['ro1'] = run['route_a_outcome'].get('ro1')
    elif c5:
        rao['ro1'] = ro1b(armed=False)
    run['route_a_outcome'] = run['result']['route_a_outcome'] = rao
    if 'ra_ident' not in keep:
        run['adapted']['route_a_identity_sha256'] = base['adapted']['route_a_identity_sha256']
    if not c5 and 'uvt_over' not in keep:
        run['uvt_record'] = copy.deepcopy(base['uvt_record'])
    return run


def shift(base, k, rows_k=None):
    """base + k*tau_i (k a number) or + rows_k[i]*tau_i."""
    return {i: base[i] + (rows_k[i] if rows_k else k) * TAU[i] for i in IDS}


C2, C3, C4 = REAL['C2R3']['rows'], REAL['C3R3']['rows'], REAL['C4R3']['rows']
D23 = {i: C3[i] - C2[i] for i in IDS}
D34 = {i: C4[i] - C3[i] for i in IDS}


def t1_rows(d23, d34):
    """C2T = C2R3; C3T = C2T + d23; C4T = C3T + d34 (all km/s)."""
    r2 = dict(C2)
    r3 = {i: r2[i] + d23[i] for i in IDS}
    r4 = {i: r3[i] + d34[i] for i in IDS}
    return r2, r3, r4


GOOD_D23 = {i: 2.0 * TAU[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(IDS)}
GOOD_D34 = {i: 0.4 * TAU[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(IDS)}


def base_runs(d23=None, d34=None, **over):
    """A complete set of runs that reads ADOPT_TAIL; 'over' replaces or modifies members."""
    r2, r3, r4 = t1_rows(d23 or GOOD_D23, d34 or GOOD_D34)
    R = {'C2T': make_run('C2T', r2), 'C3T': make_run('C3T', r3), 'C4T': make_run('C4T', r4)}
    R['C6T'] = make_run('C6T', shift(r4, 0.1))
    R['S4T'] = make_run('S4T', shift(r4, 0.5))
    R['C5H'] = make_run('C5H', shift(r4, 0.05))
    R['C4T-D5'] = make_run('C4T-D5', shift(r4, 0.1))
    R['C4T-C5c'] = make_run('C4T-C5c', shift(r4, 0.15))
    R['C4T-KLO'] = make_run('C4T-KLO', shift(r4, 0.05))
    R['C4T-KHI'] = make_run('C4T-KHI', shift(r4, -0.05))
    R['C4T-A'] = make_run('C4T-A', shift(r4, 0.5))
    for k, v in over.items():
        R[k] = v(R) if callable(v) else v
    return R


def remake(lab, **kw):
    return lambda R: make_run(lab, R[lab]['adapted']['rows'], **kw)


# ---------------------------------------------------------------------------------------------------- gate records
def rec(gate, verdict=None, **fields):
    r = {'schema': M.GATE_SCHEMA, 'gate': gate, 'verdict': verdict or M.GATE_PASS_VERDICTS[gate],
         'producer': {'path': '/synthetic/tool_%s.py' % gate, 'sha256': sha(gate)}}
    r.update(fields)
    return r


def _sh(run):
    return run.get('result_sha256') or '0' * 64


def complete_records(R, IDR, RP=None, sr_delta=None, srb=None, dV_total=0.5, eps=6e-4, rulings=None, b0_c5h=False):
    t12 = [TAU[i] for i in IDS]
    rp_keys = ['%s@RPAIR:%s' % (m, pid) for pid, rp in (RP or {}).items() for m in rp['_runs']]
    rp_runs = {('%s@RPAIR:%s' % (m, pid)): x for pid, rp in (RP or {}).items() for m, x in rp['_runs'].items()}

    def specs():
        ext = [{'label': 'V005', 'sha256': 'd' * 64}] + ([{'label': 'C5H', 'sha256': M.PIN_C5H_SPEC[1]}] if b0_c5h else [])
        if b0_c5h:                                   # [A52.3] each C5H R-PAIR member spec gets its B0 record against v009-EXT
            ext += [b0_ext_entry(k, rp_runs[k]) for k in rp_keys if k.split('@')[0] == M.C5H]
        return {'EXT': ext, 'GEO': [{'label': '2029f26a', 'sha256': '2029f26a' + '0' * 56},
                                    {'label': '4ac5527a', 'sha256': M.B0PRIME_RERUN_SPEC_SHA256}], 'NGC': [{'label': 'T', 'sha256': 'b' * 64}]}
    b3case = {k: (0.0 if op == '==' else t / 10) for k, op, t in M.B3_TOL}
    b3case['hi_v003_L67_pass'] = True
    d = sr_delta or {'2': [0.01 * t for t in t12], '3': [0.012 * t for t in t12], '4': [0.013 * t for t in t12]}
    out = {
        'B0': rec('B0', maps={'EXT': {'a': 'b'}, 'GEO': {'c': 'd'}}, spec_sets=specs()),
        'B0prime_DRY': rec('B0prime_DRY', files_compared=['DRYRUN_REPORT.json', 'DRYRUN_PLAN.txt'], spec_sets=specs()),
        'B0prime_RERUN': rec('B0prime_RERUN', **ident('B0prime_RERUN'), run_result_sha256=_sh(IDR['B0prime_RERUN']),
                             reference_result_sha256=M.GEO_DECIDING_I_RESULT_SHA256, call_spec_sha256=M.B0PRIME_RERUN_SPEC_SHA256,
                             declared_exceptions=['elapsed_seconds'], differences_outside_declared=[], tail='OFF'),
        'B0_FA': rec('B0_FA', cases={c: {'status': 'REFUSED', 'code': 'ROUTE_A_CHECKPOINT_MISSING'} for c in ('A1', 'A2', 'A4')}),
        'B1': rec('B1', **ident('B1'), run_result_sha256=_sh(IDR['Z2']), reference_result_sha256=M.Z2_REFERENCE_RESULT_SHA256, tail='ON',
                  outer_K_big_equals_K=True, precondition_L={'verdict': 'PASS_BITWISE_EQUAL', 'reference_result_sha256': M.PRECONDITION_L_REFERENCE_SHA256},
                  declared_exceptions=['driver_sha256'], differences_outside_custody=[]),
        'B1_OFF': rec('B1_OFF', **ident('B1_OFF'), run_result_sha256=_sh(IDR['Z2-OFF']), reference_result_sha256=M.Z2_REFERENCE_RESULT_SHA256,
                      tail='OFF', declared_exceptions=['driver_sha256'], differences_outside_custody=[]),
        'B2': rec('B2', O_cube_K_out_inverse_kpc=12, azimuths=16,
                  per_state={s: {'state_result_sha256': M.PIN_R3[s][1], 'max_row_diff_km_s': 1e-6, 'sanity_vs_KB12_km_s': 0.01}
                             for s in ('C2R3', 'C3R3', 'C4R3')}),
        'B3': rec('B3', independent_lane='Claude3', imports_tail_library=False, state_result_sha256=M.PIN_R3['C4R3'][1],
                  cases={'cube_O8': dict(b3case), 'cylinder_O8': dict(b3case)}),
        'B0_RO1': rec('B0_RO1', part_a={'identity_runs': {n: {'result_sha256': _sh(IDR[n]), 'ro1_fired': False} for n in M.IDENTITY_RUNS}},
                      part_b={'checkpoint_source': 'C6 iteration 8', 'recorded_code': M.RO1_CODE, 'query': 3, 'handed_to_route_b': True},
                      part_c={'cases': [{'kind': 'OTHER_EXCEPTION', 'expected': 'CALL_FAILED', 'observed': 'CALL_FAILED'},
                                        {'kind': 'REFUSAL_BEFORE_CONVERGENCE', 'expected': 'CALL_FAILED', 'observed': 'CALL_FAILED'}]}),
        'B0_N3': rec('B0_N3', files_scanned=['driver.py'], constructions=[{'file': 'driver.py', 'line': 10, 'guarded': True}],
                     runtime_checks=['B0prime_RERUN', 'B1_OFF']),
        'EPS': rec('EPS', eps_max=eps, evaluator_sha256=M.QINF_EVALUATOR_PREFIX + '0' * 56,
                   coverage_inverse_kpc={'DDO': [2, EPS_COV], 'NGC': [2, 46]},     # [A54] >= sqrt(2) x 2P; [A58 RI-17] NGC 46
                   shells=[{'range_inverse_kpc': list(rg), 'eps_base': 5e-4, 'eps_refined': 5.2e-4, 'refinements': 1}
                           for rg in EPS_SHELLS],                                                # R7 [SF4 a] cover [2, 363]
                   envelope_bound={'rule': M.EPS_ENVELOPE_RULE, 'coverage_max_inverse_kpc': EPS_COV,   # [A52.5] successor EPS
                                   'eps_max_envelope_all_shells': eps, 'dominates_actual_every_shell': True}),   # R7 [A57.4]
        'DOUBLING': rec('DOUBLING', ddo_state_result_sha256=M.PIN_R3['C4R3'][1], ddo_max_change_over_tau=0.01,
                        ngc_operator_sha256=M.NGC_T120L_OPERATOR_SHA256, ngc_max_change_over_theta=0.01,
                        ddo_K_big_inverse_kpc=[P_KBIG, 2 * P_KBIG], ddo_gas_M_s=M.PRODUCTION_GAS_M_S_A57),    # [A58 RI-03]
        'GQ': rec('GQ', rosters=[{'roster': n, 'k_range_inverse_kpc': [2, kb], 'M_s': ms, 'M_s_doubled': 2 * ms, 'nodes': 4096,
                                  'max_abs_diff_over_P0': 1e-14,
                                  **({} if n == 'NGC_T120L' else {'geometry': GQ_GEOMETRY[n][0],         # R8 [A67 SF1]
                                                                  'all_nodes': {'max_abs_diff_over_P0': 2e-14, 'nodes': GQ_GEOMETRY[n][1]}})}
                                 for n, kb, ms in GQ_FIXTURE]),            # [A57] M_s 128 / NGC 96; R7 [A57.1] all_nodes (DDO)
        'LO': rec('LO', state_result_sha256=M.PIN_R3['C4R3'][1], summed_max_over_tau=0.01, source_gas_M_s=M.PRODUCTION_GAS_M_S_A57,
                  shells=[{'range_inverse_kpc': list(r), 'max_over_tau': 0.001} for r in M.LO_RANGES + LO_EXT]),   # [A58 RI-06]
        'LO_NGC': rec('LO_NGC', operator_sha256=M.NGC_T120L_OPERATOR_SHA256, summed_max_over_theta=0.01,
                      shells=[{'range_inverse_kpc': list(r), 'max_over_theta': 0.001} for r in M.LO_NGC_RANGES]),
        'I1T': rec('I1T', builds=[{'case': c, 'stage': 'route_a', 'max_rel': 1e-15, 'nodes': 4096}
                                  for c in list(M.T_CASES) + [k for k in rp_keys if k.split('@')[0] != M.C5H]]),
        'T2I': rec('T2I', case='C5H', region='G5\\G4', c5h_result_sha256=R['C5H'].get('result_sha256') or '0' * 64,
                   components={'route_a_updated': 1e-14, 'offset_new_body_fourier_J': 1e-14, 'feedback_gas_source_feedback': 1e-14}, max_rel=1e-14),
        'SRB_ROT': rec('SRB_ROT', case='C4T', c4t_result_sha256=R['C4T'].get('result_sha256') or '0' * 64, srb_rot_km_s=srb or [0.01 * t for t in t12]),
        'RB_FP': rec('RB_FP', case='C4T', c4t_result_sha256=R['C4T'].get('result_sha256') or '0' * 64, eps_max=eps, shells=['4-8', '8-32'],
                     shell_ranges_inverse_kpc=[[4, 8], [8, RB_FP_TOP]], full_tail_domain=True,   # R7 [A62.1]; R8 [A67 N3] exact top
                     dV_static_shells_km_s={'4-8': [dV_total * 0.7] * 12, '8-32': [dV_total * 0.3] * 12}),
        'SR_K': rec('SR_K', states={s: M.PIN_R3[s][1] for s in ('C2R3', 'C3R3', 'C4R3')}, Delta_km_s=d),
        'EA': rec('EA', per_case=dict({'C5H': {'result_sha256': R['C5H'].get('result_sha256') or '0' * 64, 'E_A_rows_km_s': [0.005 * t for t in t12],
                                               'accepted_iteration': 7, 'row_radii_m': list(RADII)}},
                                      **{k: {'result_sha256': _sh(rp_runs[k]), 'E_A_rows_km_s': [0.005 * t for t in t12],    # [A50 B1] C5H
                                             'accepted_iteration': 7, 'row_radii_m': list(RADII)}                             # R-PAIR member
                                         for k in rp_keys if k.split('@')[0] == M.C5H})),
        'HARMONICS': rec('HARMONICS', rows=[{'case': 'C4T', 'source': 'replay', 'query': 3, 'R_kpc': 1.48, 'a0': 2.0, 'a4': 0.2,
                                             'a8': -0.5, 'units': '1e-28/m'}]),
        'MT': mt_record({c: {'result_sha256': _sh(x), 'M_T_accepted': ((x.get('uvt_record') or {}).get('M_T_accepted') or 0.05),
                             'flags': list((x.get('uvt_record') or {}).get('flags') or [])}
                         for c, x in [(c, R[c]) for c in M.T_CASES] + [(k, rp_runs[k]) for k in rp_keys if k.split('@')[0] != M.C5H]}),
        'FLAG_RULINGS': rec('FLAG_RULINGS', rulings=rulings or []),
        'I4': rec('I4', tail='ON', driver_sha256=V010, serial_result_sha256='3' * 64, parallel_result_sha256='4' * 64,
                  v8c_f1_fix_confirmed=True, bitwise_equal=True, differences_outside_custody=[])}
    return out


P_KBIG = 128.0                                       # [A55] the registered production K_big of the fixture case block (C4T)
RB_FP_TOP = M.RB_FP_DOMAIN_FACTOR_OF_P * P_KBIG      # R8 [A67 N3] the RB_FP shells end exactly at sqrt(2) x P (r7 fixture: 182)
EPS_COV = 363.0                                     # >= sqrt(2) x 2P = 362.04 (A54, A55)
LO_EXT = ()                                         # R6 [A58 RI-06] M.LO_RANGES is the registered ten-shell partition to 363
GQ_FIXTURE = [('DDO_C2T', P_KBIG, 128), ('DDO_C3T', P_KBIG, 128), ('DDO_C4T', 2 * P_KBIG, 128), ('NGC_T120L', 32.0, 96)]   # [A57]
# R7 [RA7] (validity SF1): DDO_C2T / DDO_C3T reach their registered K_big P = 128 (r6: 32, the R1 P = 32 instance)
EPS_SHELLS = ((2, 5), (5, 64), (64, EPS_COV))        # R7 [SF4 (a)] the EPS shells cover the declared coverage [2, 363]


def _default_srk_record():
    return complete_records(base_runs(), {n: identity_run(n) for n in M.IDENTITY_RUNS})['SR_K']


def b0_ext_entry(key, run):
    """[A53 r4 validity F1 option (a)] the B0 EXT entry of a C5H R-PAIR member spec, with its evidence: the projection sha and
    exactly the declarable leaves the member carries."""
    ns = (run.get('result') or {}).get('normalized_spec') or {}
    carried = [x for x in M.B0_EXT_DECLARABLE if M.jptr(ns, x)[0]]
    return {'label': key, 'sha256': (run.get('result') or {}).get('call_spec_sha256') or '0' * 64,
            'projection_sha256': sha('projection' + key), 'declared_differences': carried}


def mt_record(per_case, verdict=None):
    """[A50 S2] an internally consistent MT record: verdict FAIL iff some run's M_T(accepted) > 1/4."""
    v = verdict or ('FAIL' if any(x['M_T_accepted'] > M.MT_THRESHOLD for x in per_case.values()) else 'PASS')
    return rec('MT', verdict=v, per_case=per_case)


def write_records(out, tag, records):
    d = out / 'gates' / tag
    d.mkdir(parents=True)
    paths = {}
    for g, r in records.items():
        if r is None:
            paths[g] = None
            continue
        p = d / ('%s.json' % g)
        p.write_text(r if isinstance(r, str) else json.dumps(r, indent=1))
        paths[g] = str(p)
    return paths


def consistent_verdicts(records, ctx):
    """[A54 S5] fixture producer: a record whose (mutated) data fails a data clause carries a registered failing verdict, as a
    consistent producer writes it (verdict-only, coverage-only and defective records are left as they are)."""
    for g, r in records.items():
        if not isinstance(r, dict) or g in M.VERDICT_ONLY_GATES or r.get('verdict') != M.GATE_PASS_VERDICTS.get(g):
            continue
        try:
            codes = M.GATE_FUNCS[g](copy.deepcopy(r), ctx, lambda *a: None, [])
        except Exception:
            continue
        fails = [c for c in codes if not c.startswith('DEFECT:')]
        if fails and not all(c.startswith(M.COVERAGE_CODE_PREFIXES) for c in fails) and not any(c.startswith('DEFECT:') for c in codes):
            r['verdict'] = M.GATE_FAIL_VERDICTS[g][0]


def registry_with_records(reg, paths, only=None):
    """R8 [A67 N2] a copy of a normalized registry with the written records (sha from bytes) registered as records of record for
    their gates (only: those gates; default every written gate).  None stays None."""
    if reg is None:
        return None
    r2 = dict(reg, gate_records=dict(reg['gate_records']))
    for g, p_ in paths.items():
        if p_ is None or (only is not None and g not in only):
            continue
        cur = r2['gate_records'].get(g)
        r2['gate_records'][g] = (cur if isinstance(cur, frozenset) else frozenset()) | {hashlib.sha256(Path(p_).read_bytes()).hexdigest()}
    return r2


def run_eval(out, tag, R=None, IDR=None, mutate=None, drop=(), RP=None, mode=None, packets_bad=(), cb=None, ctx_over=None,
             rulings=None, b0_c5h=False, skip_mt=False, auto_verdict=True, register_records=True):
    ctx = dict(CTX)
    ctx['case_block'] = cb if cb is not None else (CB_SERIAL if mode == 'serial_with_exemption' else CB)
    if mode:
        ctx['route_a_mode'] = mode
    if ctx_over:
        ctx.update(ctx_over)
    ctx['c4r3_adapted'] = REAL['C4R3']
    R = R if R is not None else base_runs()
    IDR = IDR if IDR is not None else {n: identity_run(n) for n in M.IDENTITY_RUNS}
    records = complete_records(R, IDR, RP, rulings=rulings, b0_c5h=b0_c5h)
    if mutate:
        mutate(records)
    if auto_verdict:
        consistent_verdicts(records, ctx)
    for g in drop:
        records[g] = None
    paths = write_records(out, tag, records)
    if register_records:                           # R8 [A67 N2] the fixture's records are its records of record
        ctx['producer_registry'] = registry_with_records(ctx.get('producer_registry'), paths)
    rsha = M.runs_sha_map(R, IDR, RP)
    gates = M.cross_gate_checks({g: M.evaluate_gate(g, paths.get(g), ctx, rsha) for g in M.ALL_GATES}, R, RP, skip_mt)

    packets = {k: {'V4': k not in packets_bad, 'V5': True} for k in list(R) + ['%s@RPAIR:%s' % (m, p) for p, rp in (RP or {}).items() for m in rp['_runs']]}
    try:
        return M.evaluate_v007(ctx, R, IDR, gates, RP or {}, packets)
    except M.Refused as exc:                       # [A53 NEW-17] refused at load: a sentinel the checks can read
        return {'decision': {'outcome': 'REFUSED_AT_LOAD', 'reasons': [str(exc)]}, 'refused': str(exc)}


# R8 [A67 N2] the fixture SR_K record of record (default Delta), in the two byte forms the suite writes (indent 1, compact)
_SRK0 = _default_srk_record()
REG_OBJ['gate_records']['SR_K'] = sorted({sha(json.dumps(_SRK0, indent=1)), sha(json.dumps(_SRK0))})
CTX['producer_registry'] = M.producer_registry_from_obj(REG_OBJ)

TESTS = []


def check(name, ev, outcome, extra=None, why='', ids=()):
    d = ev['decision']
    try:
        ok_extra = extra is None or bool(extra(ev))
    except Exception as exc:
        ok_extra = False
        why = why + ' [extra raised %s: %s]' % (type(exc).__name__, exc)
    ok = d['outcome'] == outcome and ok_extra
    TESTS.append({'test': name, 'covers': list(ids), 'pass': bool(ok), 'outcome': d['outcome'], 'position': d.get('position'),
                  'expected': outcome, 'subtype': d.get('subtype'),
                  'reasons': [str(x)[:300] for x in (d['reasons'] if isinstance(d['reasons'], list) else [d['reasons']])][:4],
                  'pending_steps': [str(x)[:200] for x in d.get('pending_steps') or []][:4], 'why': why})


def t(name, cond, ids=(), **info):
    TESTS.append({'test': name, 'covers': list(ids), 'pass': bool(cond), **{k: (str(v)[:400]) for k, v in info.items()}})


def has(ev, code, where='V1_codes', lab=None):
    return any(code in str(c) for v in ([ev['validity'][lab]] if lab else ev['validity'].values()) for c in v.get(where, []))


# ---------------------------------------------------------------------------------------------------- on-disk runs
def write_run_dir(root, name, result, *, receipt=True, finish=True, start=None, raw=None):
    """Write a run directory in the driver layout; returns its path.  result: dict (or raw bytes via raw)."""
    d = root / name
    d.mkdir(parents=True)
    rb = raw if raw is not None else json.dumps(result, indent=1).encode()
    (d / 'result.json').write_bytes(rb)
    rsha = hashlib.sha256(rb).hexdigest()
    if finish:
        (d / 'finish.json').write_text(finish if isinstance(finish, str) else json.dumps({'status': 'x', 'result_sha256': rsha}))
    if start is not None:
        (d / 'start.json').write_text(json.dumps(start))
    if receipt:
        r = result if isinstance(result, dict) else {}
        rc = receipt_for(rsha, str(d / 'result.json'), r.get('call_spec_sha256'), r.get('driver_sha256'), r.get('status', 'COMPLETED'))
        if isinstance(receipt, dict):
            rc.update(receipt)
        Path(str(d) + '.receipt.json').write_text(json.dumps(rc))
    return d


def synthetic_completed_result(rows, numerics, *, drv, spec):
    """A COMPLETED result.json body (no field packet: V4/V5 read False; used where only V1-V3/blinding matter)."""
    ns = {'galaxy': 'DDO154', 'physical': CTX['anchor']['physical'], 'coefficients': CTX['anchor']['coefficients'], 'numerics': numerics}
    pr = passes_from(rows)
    passes = [{'pass': j + 1, 'rows': [{'id': i, 'speed_km_s': p[i]} for i in IDS],
               'max_abs_change_km_s': max(abs(p[i] - pr[j - 1][i]) for i in IDS) if j else 1.0} for j, p in enumerate(pr)]
    return {'schema': M.RESULT_SCHEMA, 'status': 'COMPLETED', 'valid': True, 'normalized_spec': ns, 'driver_sha256': drv,
            'call_spec_sha256': spec, 'rows': [{'id': i, 'speed_km_s': rows[i]} for i in IDS], 'passes': passes,
            'route_a_outcome': {'classification': 'CONVERGED', 'converged_iteration': 6, 'result_path': '/nonexistent', 'result_sha256': 'f' * 64}}


class _quiet:
    def __enter__(self):
        self._o = sys.stdout
        sys.stdout = io.StringIO()

    def __exit__(self, *exc):
        sys.stdout = self._o
        return False


class OpenTrace:
    """In-process trace of every file opened (builtins.open / io.open) while the compare's main() runs."""

    def __init__(self):
        self.paths = []

    def __enter__(self):
        self._b, self._i = builtins.open, io.open
        tr = self

        def op(file, *a, **k):
            try:
                tr.paths.append(str(Path(file).resolve()) if isinstance(file, (str, Path)) else str(file))
            except Exception:
                tr.paths.append(str(file))
            return tr._b(file, *a, **k)
        builtins.open = op
        io.open = op
        return self

    def __exit__(self, *exc):
        builtins.open, io.open = self._b, self._i
        return False


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    regf = out / 'PRODUCER_REGISTRY_TEST.json'                     # R7 [A62.2] the test registry, given to every test-mode CLI call
    regf.write_text(json.dumps(REG_OBJ, indent=1))
    REGARGS.extend(['--test-producer-registry', str(regf)])
    # ================================================================ one branch test per outcome
    check('O16_ADOPT_TAIL', run_eval(out, 'adopt'), 'ADOPT_TAIL',
          extra=lambda e: all(e['decision']['carried_numerical_uncertainty_km_s'][i] is not None for i in IDS)
          and abs(e['decision']['carried_terms']['K34'][IDS[0]] - 0.4 * TAU[IDS[0]]) < 1e-9)

    def b3fail(r):
        r['B3']['cases']['cube_O8']['value_rel'] = 1e-6
    check('O01_NO_RUN_B3_FAIL_IS_IMPLEMENTATION_DEFECT_OF_GATE', run_eval(out, 'b3', mutate=b3fail), 'NO_RUN',
          extra=lambda e: 'B3' in str(e['decision'].get('subtype')))

    def b1off_fail(r):
        r['B1_OFF']['differences_outside_custody'] = ['/passes/0/rows']
    check('O01b_NO_RUN_B1_OFF_FAIL_Z2OFF_MANDATORY_A47_I6', run_eval(out, 'b1off', mutate=b1off_fail), 'NO_RUN', ids=('AMB-01',))
    check('O02_INCOMPLETE_MISSING_CASE', run_eval(out, 'miss', R=base_runs(**{'C6T': make_run('C6T', {}, present=False)})), 'INCOMPLETE',
          extra=lambda e: any('C6T' in r for r in e['decision']['reasons']) and e['decision']['tests_read'] is False
          and e['decision']['subtype'] == 'CASES_OR_RECORDS', ids=('AMB-18',))
    check('O02b_INCOMPLETE_B1_OFF_RECORD_MISSING_A47_I6', run_eval(out, 'b1offmiss', drop=('B1_OFF',)), 'INCOMPLETE',
          extra=lambda e: any('B1_OFF' in r for r in e['decision']['reasons']))
    check('O02c_INCOMPLETE_IDENTITY_RUN_Z2OFF_MISSING_A47_I1', run_eval(out, 'idmiss', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS},
                                                                                              'Z2-OFF': {'present': False, 'absent': 'NO_RUN_DIR'}}),
          'INCOMPLETE', extra=lambda e: any('Z2-OFF' in r for r in e['decision']['reasons']))

    def eps_unc(r):                         # [R5 adapted, A54 S5: the producer's verdict must agree with its data]
        r['EPS']['verdict'] = 'EPS_UNCERTIFIED'
        r['EPS']['shells'][0]['refinements'] = 2
    check('O03_NUMERICS_UNCERTIFIED_EPS_DATA_AND_VERDICT_AGREE_A54_S5', run_eval(out, 'eps', mutate=eps_unc, auto_verdict=False),
          'NUMERICS_UNCERTIFIED', ids=('AMB-03', 'AMB-18', 'A54.S5'), extra=lambda e: e['decision']['tests_read'] is False)

    def gq_fail(r):
        r['GQ']['rosters'][2]['max_abs_diff_over_P0'] = 2e-12
    check('O03b_NUMERICS_UNCERTIFIED_GQ_RA7', run_eval(out, 'gq', mutate=gq_fail), 'NUMERICS_UNCERTIFIED', ids=('AMB-03',),
          extra=lambda e: any('UV_TAIL_GAS_QUADRATURE_UNCERTIFIED' in r for r in e['decision']['reasons']))

    def lo_fail(r):
        r['LO']['shells'][3]['max_over_tau'] = 0.006
    check('O03c_NON_LAPSE_TAIL_MATERIAL_LO', run_eval(out, 'lo', mutate=lo_fail), 'NON_LAPSE_TAIL_MATERIAL',
          extra=lambda e: e['decision']['position'] == 3)
    check('O04_UTA_FLAGGED_TEST_FAILS_NO_DECIDED_FAILURE_AMB04',
          run_eval(out, 'uta', R=base_runs(**{'C4T-KLO': lambda R: make_run('C4T-KLO', shift(R['C4T']['adapted']['rows'], 0.3), flagged=True)})),
          'UNDECIDABLE_ROUTE_A_TAIL', ids=('AMB-04', 'M1', 'B6'),
          extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['status'] == 'UNDECIDABLE_FLAGGED' and 'C4T-KLO' in e['decision']['next_step'])
    slow = dict(dlast=0.001, q=0.95)                       # E_i = 9 * 0.001 km/s per run: > tau_i/8 on rows 06-09
    Rf = base_runs(**{'C4T-KLO': remake('C4T-KLO', **slow)})
    check('O05a_RPAIR_PENDING_READS_INCOMPLETE_UNRESOLVED_WITH_BRANCH', run_eval(out, 'pend', R=Rf), 'INCOMPLETE', ids=('AMB-17', 'AMB-07'),
          extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['status'] == 'RPAIR_PENDING'
          and e['tests']['T3']['pairs']['T3_KLO']['rpair_branch'] == 'PICARD' and e['decision']['subtype'] == 'UNRESOLVED'
          and e['decision']['tests_read'] is True and any('T3_KLO' in x for x in e['decision']['pending_steps']))

    def rpair_runs(R, **kw):
        RP = {'T3_KLO': {'branch': 'PICARD', '_runs': {}}}
        for m in ('C4T', 'C4T-KLO'):
            RP['T3_KLO']['_runs'][m] = make_run(m + '@RPAIR:T3_KLO', R[m]['adapted']['rows'], key='rp' + m, **kw)
            RP['T3_KLO']['_runs'][m]['result']['normalized_spec']['numerics']['picard'] = dict(M.RPAIR_PICARD)
            a53_picard_shape(RP['T3_KLO']['_runs'][m], R[m])                  # [A53] admits the base route A
        return RP
    RPf = rpair_runs(Rf, **slow)
    check('O05_UNDECIDABLE_AT_ITERATION_FLOOR_NEITHER_PASS_NOR_FAIL', run_eval(out, 'floor', R=Rf, RP=RPf), 'UNDECIDABLE_AT_ITERATION_FLOOR',
          extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['status'] not in ('PASS', 'FAIL'))
    RPok = rpair_runs(Rf, dlast=0.0002, q=1 / 3.0)
    check('O05b_RPAIR_PICARD_DECIDED_PASS_THEN_ADOPT_I1T_MT_COVER_RPAIR_BUILDS', run_eval(out, 'rpok', R=Rf, RP=RPok), 'ADOPT_TAIL',
          ids=('D5',), extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['source'] == 'RPAIR'
          and e['rpair_validity']['C4T@RPAIR:T3_KLO']['V6'] is True and e['gates']['I1T']['status'] == 'PASS' and e['gates']['MT']['status'] == 'PASS')

    def drop_rpair_build(r):
        r['I1T']['builds'] = [b for b in r['I1T']['builds'] if b['case'] != 'C4T-KLO@RPAIR:T3_KLO']
    check('D5_RPAIR_MEMBER_BUILD_NOT_I1T_COVERED_INCOMPLETE', run_eval(out, 'rpnoi1t', R=Rf, RP=RPok, mutate=drop_rpair_build), 'INCOMPLETE',
          ids=('D5',), extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['status'] == 'INCOMPLETE'
          and 'I1T_UNCOVERED' in str(e['rpair_validity']['C4T-KLO@RPAIR:T3_KLO']['V1_codes']))
    RPbad = copy.deepcopy(RPok)
    RPbad['T3_KLO']['branch'] = 'ROUTE_A'
    check('O05c_RPAIR_BRANCH_MISMATCH_INCOMPLETE', run_eval(out, 'rpbad', R=Rf, RP=RPbad), 'INCOMPLETE')
    ev_ra = run_eval(out, 'rabranch', R=base_runs(**{'C4T-KLO': remake('C4T-KLO', ea=0.2)}))
    t('O05d_RPAIR_BRANCH_ROUTE_A_WHEN_EA_DOMINATES', ev_ra['tests']['T3']['pairs']['T3_KLO'].get('rpair_branch') == 'ROUTE_A', ids=('AMB-07',),
      branch=ev_ra['tests']['T3']['pairs']['T3_KLO'].get('rpair_branch'))
    check('O06_IMPLEMENTATION_DEFECT_T2_DECIDABLE_FAILS', run_eval(out, 't2', R=base_runs(**{'C4T-D5': lambda R: make_run('C4T-D5', shift(R['C5H']['adapted']['rows'], 0.3))})),
          'IMPLEMENTATION_DEFECT', extra=lambda e: e['decision']['subtype'] == 'T2')
    check('O07_SOURCE_RULE_MATERIAL_T2c', run_eval(out, 't2c', R=base_runs(**{'C4T-C5c': lambda R: make_run('C4T-C5c', shift(R['C4T-D5']['adapted']['rows'], 0.6))})),
          'SOURCE_RULE_MATERIAL')
    check('O08_KBIG_NOT_CONVERGED_T3', run_eval(out, 't3', R=base_runs(**{'C4T-KHI': lambda R: make_run('C4T-KHI', shift(R['C4T']['adapted']['rows'], 0.3))})),
          'KBIG_NOT_CONVERGED')
    check('O09_BOUND_INSUFFICIENT_RB_FP', run_eval(out, 'rbfp', R=base_runs(**{'C4T-A': lambda R: make_run('C4T-A', shift(R['C4T']['adapted']['rows'], 10.0))})),
          'BOUND_INSUFFICIENT')

    def srb_fail(r):
        r['SRB_ROT']['srb_rot_km_s'][5] = 0.2 * TAU[IDS[5]]
    check('O09b_BOUND_INSUFFICIENT_SRB_ROT', run_eval(out, 'srb', mutate=srb_fail), 'BOUND_INSUFFICIENT')
    fl23 = {i: 0.5 * TAU[i] for i in IDS}
    fl34 = {i: 0.4 * TAU[i] for i in IDS}
    check('O10_FLOOR_LIKE_BEFORE_T1_FAIL_SPLIT', run_eval(out, 'floorlike', R=base_runs(d23=fl23, d34=fl34)), 'FLOOR_LIKE',
          extra=lambda e: e['tests']['T1']['status'] == 'FAIL' and e['tests']['T1']['floor_like'])
    big23 = {i: 4.0 * TAU[i] for i in IDS}
    big34 = {i: 3.0 * TAU[i] for i in IDS}
    check('O11_NOT_UV_RESIDUAL', run_eval(out, 'notuv', R=base_runs(d23=big23, d34=big34)), 'NOT_UV_RESIDUAL')

    def srk_kdep(r):
        r['SR_K']['Delta_km_s']['3'][4] = 0.5 * TAU[IDS[4]]
    check('O12_SOURCE_REPRESENTATION_K_DEPENDENT', run_eval(out, 'srkd', R=base_runs(d23=big23, d34=big34), mutate=srk_kdep),
          'SOURCE_REPRESENTATION_K_DEPENDENT')
    check('O13_HIGHER_K_DISAGREEMENT', run_eval(out, 'hk', R=base_runs(**{'C6T': lambda R: make_run('C6T', shift(R['C4T']['adapted']['rows'], 0.6))})),
          'HIGHER_K_DISAGREEMENT')
    check('O14_SHAPE_DISAGREEMENT', run_eval(out, 'shape', R=base_runs(**{'S4T': lambda R: make_run('S4T', shift(R['C4T']['adapted']['rows'], 2.5))})),
          'SHAPE_DISAGREEMENT')

    def sqm(r):
        r['SR_K']['Delta_km_s']['4'][2] = 1.5 * TAU[IDS[2]]
        r['SR_K']['Delta_km_s']['3'][2] = 1.4 * TAU[IDS[2]]
        r['SR_K']['Delta_km_s']['2'][2] = 1.3 * TAU[IDS[2]]
    check('O15_FLAG_PENDING_RULING_SOURCE_QUADRATURE_MATERIAL', run_eval(out, 'sqm', mutate=sqm), 'FLAG_PENDING_RULING')
    R0 = base_runs()

    def ruling(flag, run, disp, R=None):
        x = {'flag': flag, 'run': run, 'run_result_sha256': (R or R0)[run]['result_sha256'],
             'evidence': 'synthetic evidence record', 'disposition': disp, 'root_decision': 'A99 (synthetic)'}
        if disp == 'CLEARED':
            x['reason'] = 'synthetic stated reason'
        return x
    check('O15b_AMB19_SQM_CLEARED_THEN_ADOPT', run_eval(out, 'sqmruled', R=R0, mutate=sqm, rulings=[ruling(M.FLAG_SQM, 'C4T', 'CLEARED')]),
          'ADOPT_TAIL', ids=('AMB-19',))
    check('AMB19_RERUN_ORDERED_KEEPS_FLAG_PENDING_RULING', run_eval(out, 'sqmrerun', R=R0, mutate=sqm,
                                                                    rulings=[ruling(M.FLAG_SQM, 'C4T', 'RERUN_ORDERED')]),
          'FLAG_PENDING_RULING', ids=('AMB-19', 'M5', 'B5', 'S57'), extra=lambda e: 'registered reruns ordered' in e['decision']['next_step'])

    def bad_ruling(r):
        sqm(r)
        del r['FLAG_RULINGS']['rulings'][0]['evidence']
    check('AMB19_RULING_WITHOUT_EVIDENCE_IS_RECORD_DEFECT_NO_RUN', run_eval(out, 'sqmnoev', R=R0, mutate=bad_ruling,
                                                                            rulings=[ruling(M.FLAG_SQM, 'C4T', 'CLEARED')]),
          'NO_RUN', ids=('AMB-19', 'AMB-02'))

    def wrong_run_sha(r):
        sqm(r)
        r['FLAG_RULINGS']['rulings'][0]['run_result_sha256'] = '9' * 64
    check('AMB19_RULING_NAMING_ANOTHER_RESULT_IS_DEFECT_NO_RUN', run_eval(out, 'sqmwrongrun', R=R0, mutate=wrong_run_sha,
                                                                          rulings=[ruling(M.FLAG_SQM, 'C4T', 'CLEARED')]), 'NO_RUN', ids=('AMB-19',))
    # ================================================================ A48 AMB-04 (flags per test) [M1, B6]
    check('AMB04_FLAG_ON_PASSING_K16_ALL_PASS_FLAG_PENDING_RULING',
          run_eval(out, 'f_k16pass', R=base_runs(**{'C4T-KLO': remake('C4T-KLO', flagged=True)})), 'FLAG_PENDING_RULING',
          ids=('AMB-04', 'M1', 'S40'), extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['status'] == 'PASS_FLAGGED')
    check('AMB04_C4T_FLAGGED_ALL_PASS_FLAG_PENDING_RULING',
          run_eval(out, 'f_c4t', R=base_runs(**{'C4T': remake('C4T', flagged=True)})), 'FLAG_PENDING_RULING', ids=('AMB-04', 'S47'),
          extra=lambda e: e['tests']['T1']['status'] == 'PASS_FLAGGED' and e['tests']['RB_FP']['status'] == 'PASS_FLAGGED')
    Rk = base_runs(**{'C4T-KLO': remake('C4T-KLO', flagged=True)})
    check('AMB04_AMB19_FLAG_CLEARED_BY_RULING_THEN_ADOPT',
          run_eval(out, 'f_cleared', R=Rk, rulings=[ruling(M.FLAG_TSU, 'C4T-KLO', 'CLEARED', R=Rk)]), 'ADOPT_TAIL', ids=('AMB-04', 'AMB-19', 'S43'))
    check('AMB04_AMB19_FLAG_RERUN_ORDERED_STAYS_FLAG_PENDING_RULING',
          run_eval(out, 'f_rerun', R=Rk, rulings=[ruling(M.FLAG_TSU, 'C4T-KLO', 'RERUN_ORDERED', R=Rk)]), 'FLAG_PENDING_RULING', ids=('AMB-19',))
    check('F1_FLAGGED_T2_FAIL_IS_UNDECIDABLE_UTA',
          run_eval(out, 'flagt2', R=base_runs(**{'C4T-D5': lambda R: make_run('C4T-D5', shift(R['C5H']['adapted']['rows'], 0.3), flagged=True)})),
          'UNDECIDABLE_ROUTE_A_TAIL', ids=('AMB-04',), extra=lambda e: e['tests']['T2']['status'] == 'UNDECIDABLE_FLAGGED')
    check('F2_AMB04_UNFLAGGED_DECIDED_T2_FAIL_READS_IMPLEMENTATION_DEFECT_DESPITE_FLAG_ELSEWHERE',
          run_eval(out, 'flagk16', R=base_runs(**{'C4T-D5': lambda R: make_run('C4T-D5', shift(R['C5H']['adapted']['rows'], 0.3)),
                                                  'C4T-KLO': remake('C4T-KLO', flagged=True)})),
          'IMPLEMENTATION_DEFECT', ids=('AMB-04', 'M1', 'B6'), extra=lambda e: e['tests']['T2']['status'] == 'FAIL')
    check('AMB04_FLAGGED_T3_FAIL_PLUS_UNFLAGGED_T2_FAIL_IMPLEMENTATION_DEFECT',
          run_eval(out, 's41', R=base_runs(**{'C4T-D5': lambda R: make_run('C4T-D5', shift(R['C5H']['adapted']['rows'], 0.3)),
                                              'C4T-KHI': lambda R: make_run('C4T-KHI', shift(R['C4T']['adapted']['rows'], 0.3), flagged=True)})),
          'IMPLEMENTATION_DEFECT', ids=('AMB-04', 'S41'), extra=lambda e: e['tests']['T3']['pairs']['T3_KHI']['status'] == 'UNDECIDABLE_FLAGGED')
    check('AMB04_FLAGGED_FLOOR_LIKE_T1_CANNOT_READ_FLOOR_LIKE',
          run_eval(out, 'f_floor', R=base_runs(d23=fl23, d34=fl34, **{'C3T': remake('C3T', flagged=True)})), 'UNDECIDABLE_ROUTE_A_TAIL',
          ids=('AMB-04', 'S44'), extra=lambda e: e['tests']['T1']['status'] == 'UNDECIDABLE_FLAGGED')
    check('AMB04_NOT_UV_SPLIT_RESTING_ON_A_FLAG_IS_UNRESOLVED_NOT_SRKD',
          run_eval(out, 'f_split', R=base_runs(d23=big23, d34=big34, **{'C6T': remake('C6T', flagged=True)})), 'INCOMPLETE',
          ids=('AMB-04', 'S48', 'N2'), extra=lambda e: e['decision']['subtype'] == 'UNRESOLVED'
          and any('T1-fail split' in x for x in e['decision']['pending_steps']))
    check('AMB04_SRKD_DECIDED_WITHOUT_THE_FLAG_STILL_READ',
          run_eval(out, 'f_srkd', R=base_runs(d23=big23, d34=big34, **{'C6T': remake('C6T', flagged=True)}), mutate=srk_kdep),
          'SOURCE_REPRESENTATION_K_DEPENDENT', ids=('AMB-04',))
    check('AMB04_SRB_ROT_FAIL_ON_FLAGGED_C4T_IS_UNDECIDABLE_NOT_BOUND',
          run_eval(out, 'f_srb', R=base_runs(**{'C4T': remake('C4T', flagged=True)}), mutate=srb_fail), 'UNDECIDABLE_ROUTE_A_TAIL',
          ids=('AMB-04',), extra=lambda e: e['tests']['SRB_ROT']['status'] == 'UNDECIDABLE_FLAGGED')
    Rfk = base_runs(**{'C4T-KLO': remake('C4T-KLO', flagged=True, **slow)})
    RPfk = rpair_runs(Rfk, dlast=0.0002, q=1 / 3.0)
    RPfk['T3_KLO']['_runs']['C4T-KLO']['uvt_record'].update(flags=[M.FLAG_TSU], monitor_status='FLAGGED', M_T_accepted=0.3)
    check('AMB04_PICARD_RPAIR_MEMBER_CARRIES_BASE_FLAG_AND_ITS_CLEARING',
          run_eval(out, 'f_rpclear', R=Rfk, RP=RPfk, rulings=[ruling(M.FLAG_TSU, 'C4T-KLO', 'CLEARED', R=Rfk)]), 'ADOPT_TAIL', ids=('AMB-04', 'AMB-19'),
          extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['source'] == 'RPAIR')
    check('AMB04_PICARD_RPAIR_MEMBER_FLAG_UNRULED_FLAG_PENDING_RULING',
          run_eval(out, 'f_rpflag', R=Rfk, RP=RPfk), 'FLAG_PENDING_RULING', ids=('AMB-04',),
          extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['status'] == 'PASS_FLAGGED')
    # ================================================================ A48 AMB-17 [M2, B7]
    check('AMB17_T2_FAILS_WHILE_T3_RPAIR_PENDING_IMPLEMENTATION_DEFECT_PENDING_LISTED',
          run_eval(out, 's50', R=base_runs(**{'C4T-D5': lambda R: make_run('C4T-D5', shift(R['C5H']['adapted']['rows'], 0.3)),
                                              'C4T-KHI': remake('C4T-KHI', **slow)})),
          'IMPLEMENTATION_DEFECT', ids=('AMB-17', 'M2', 'B7', 'S50'),
          extra=lambda e: any('T3_KHI' in x for x in e['decision']['pending_steps']))
    check('AMB17_T3K16_FAILS_WHILE_K64_PENDING_KBIG',
          run_eval(out, 's51', R=base_runs(**{'C4T-KLO': lambda R: make_run('C4T-KLO', shift(R['C4T']['adapted']['rows'], 0.3)),
                                              'C4T-KHI': remake('C4T-KHI', **slow)})),
          'KBIG_NOT_CONVERGED', ids=('AMB-17', 'S51'), extra=lambda e: e['tests']['T3']['status'] == 'FAIL')
    check('AMB17_T1S_FAILS_WHILE_T1H_PENDING_SHAPE',
          run_eval(out, 's53', R=base_runs(**{'S4T': lambda R: make_run('S4T', shift(R['C4T']['adapted']['rows'], 2.5)),
                                              'C6T': remake('C6T', **slow)})),
          'SHAPE_DISAGREEMENT', ids=('AMB-17', 'S53'))
    # ================================================================ A48 AMB-10 [M3, B8]

    def t2i_fail(r):
        r['T2I']['max_rel'] = 1e-9
    check('AMB10_T2I_FAIL_READS_IMPLEMENTATION_DEFECT_T2I', run_eval(out, 't2i', mutate=t2i_fail), 'IMPLEMENTATION_DEFECT',
          ids=('AMB-10', 'M3', 'B8', 'S55'), extra=lambda e: e['decision']['subtype'] == 'T2I' and e['tests']['T2']['status'] == 'NOT_READ'
          and e['decision']['next_step'] == M.T2I_DEFECT_NEXT)
    check('AMB10_T2I_FAIL_WITH_C4TD5_FLAGGED_STILL_IMPLEMENTATION_DEFECT',
          run_eval(out, 't2iflag', R=base_runs(**{'C4T-D5': remake('C4T-D5', flagged=True)}), mutate=t2i_fail), 'IMPLEMENTATION_DEFECT',
          ids=('AMB-10', 'S55b'))
    # ================================================================ A48 AMB-05 [M6, S1, G1]
    check('AMB05_ONE_PASS_NO_INCREMENT_UNDECIDABLE_RPAIR_PENDING_PICARD_DECLARED',
          run_eval(out, 'onepass', R=base_runs(**{'C6T': remake('C6T', npass=1)})), 'INCOMPLETE', ids=('AMB-05', 'M6', 'S1', 'G1', 'S56'),
          extra=lambda e: e['tests']['T1_H']['status'] == 'RPAIR_PENDING' and e['tests']['T1_H']['rpair_branch'] == 'PICARD'
          and 'A50 root item 1' in e['tests']['T1_H']['rpair_branch_basis'])
    E, c = M.picard_noise(make_run('C6T', C4, npass=2, dlast=0.0007), IDS, TAU)
    nrm1 = max(0.0007 / TAU[i] for i in IDS)                  # [A51 F2] adapted: E_i = tau_i ||d_last||_tau (q/(1-q) taken as 1)
    t('AMB05_EXACTLY_ONE_INCREMENT_E_IS_TAU_I_TIMES_THE_TAU_NORM_A51', c is None and all(abs(E[i] - TAU[i] * nrm1) < 1e-12 for i in IDS),
      ids=('AMB-05', 'A51.F2'))
    # ================================================================ A48 AMB-26 receipts [M4, B1]
    check('AMB26_TCASE_RECEIPT_ABSENT_INCOMPLETE', run_eval(out, 'rc_c4t', R=base_runs(**{'C4T': remake('C4T', receipt=False)})), 'INCOMPLETE',
          ids=('AMB-26', 'M4', 'B1', 'S14'), extra=lambda e: has(e, 'RECEIPT_ABSENT', lab='C4T'))
    check('AMB26_C5H_RECEIPT_ABSENT_INCOMPLETE', run_eval(out, 'rc_c5h', R=base_runs(**{'C5H': remake('C5H', receipt=False)})), 'INCOMPLETE',
          ids=('AMB-26', 'S15'))
    check('AMB26_IDENTITY_RUN_RECEIPT_ABSENT_INCOMPLETE',
          run_eval(out, 'rc_z2', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS}, 'Z2': identity_run('Z2', receipt=False)}), 'INCOMPLETE',
          ids=('AMB-26', 'S16'))
    check('AMB26_IDENTITY_RECEIPT_WRONG_RESULT_SHA_INCOMPLETE',
          run_eval(out, 'rc_z2sha', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS}, 'Z2': identity_run('Z2', receipt_sha='7' * 64)}),
          'INCOMPLETE', ids=('AMB-26', 'S16b'))
    for tag, mut, code in (('childfail', lambda rc: rc.update(status='CHILD_FAILED'), 'RECEIPT_STATUS_NOT_FINISHED'),
                           ('spec', lambda rc: rc['pins']['spec'].update(sha256='6' * 64), 'RECEIPT_SPEC_PIN_MISMATCH'),
                           ('driver', lambda rc: rc['pins']['driver'].update(sha256='6' * 64), 'RECEIPT_DRIVER_PIN_MISMATCH'),
                           ('stop', lambda rc: rc.update(stop_reason='WALL_CAP'), 'RECEIPT_STOP_REASON:WALL_CAP'),
                           ('exit', lambda rc: rc.update(exit_code=1), 'RECEIPT_EXIT_CODE_NOT_0'),
                           ('path', lambda rc: rc['result'].update(path='/elsewhere/result.json'), 'RECEIPT_RESULT_PATH_MISMATCH')):
        def bad(R, mut=mut):
            r = make_run('C4T-A', R['C4T-A']['adapted']['rows'])
            mut(r['receipt'])
            return r
        check('AMB26_RECEIPT_FIELD_%s_INCOMPLETE' % tag.upper(), run_eval(out, 'rc_' + tag, R=base_runs(**{'C4T-A': bad})), 'INCOMPLETE',
              ids=('AMB-26', 'B1'), extra=lambda e, code=code: has(e, code, lab='C4T-A'))
    RPnr = copy.deepcopy(RPok)
    RPnr['T3_KLO']['_runs']['C4T-KLO']['receipt'] = None
    check('AMB26_RPAIR_MEMBER_RECEIPT_ABSENT_TEST_INCOMPLETE', run_eval(out, 'rc_rpair', R=Rf, RP=RPnr), 'INCOMPLETE', ids=('AMB-26',),
          extra=lambda e: 'RECEIPT_ABSENT' in str(e['rpair_validity']['C4T-KLO@RPAIR:T3_KLO']['V1_codes']))
    # ================================================================ A48 AMB-12 GQ union [M7, B4]

    def gq_lower(r):
        for x in r['GQ']['rosters']:
            x['k_range_inverse_kpc'][0] = 16

    def gq_gap(r):
        r['GQ']['rosters'][0]['k_range_inverse_kpc'] = [2, 30]
        r['GQ']['rosters'][1]['k_range_inverse_kpc'] = [2, 32]
        r['GQ']['rosters'][2]['k_range_inverse_kpc'] = [40, 64]

    def gq_name(r):
        r['GQ']['rosters'][0]['roster'] = 'DDO_%s' % CANARY
    for tag, mut, want in (('lower16', gq_lower, 'NUMERICS_UNCERTIFIED'), ('gap', gq_gap, 'NUMERICS_UNCERTIFIED'), ('name', gq_name, 'NO_RUN')):
        ev = run_eval(out, 'gq_' + tag, mutate=mut)
        check('AMB12_GQ_%s' % tag.upper(), ev, want, ids=('AMB-12', 'M7', 'B4', 'S32'),
              extra=lambda e: CANARY not in json.dumps(e['gates']['GQ']['codes']))
    # ================================================================ A48 AMB-22 row radii [M8, B3, G4]

    def ea_noradii(r):
        del r['EA']['per_case']['C5H']['row_radii_m']
    check('AMB22_EA_RECORD_WITHOUT_ROW_RADII_RECORD_DEFECT_NO_RUN', run_eval(out, 'ea_norad', mutate=ea_noradii), 'NO_RUN',
          ids=('AMB-22', 'M8', 'B3', 'S58'))

    def ea_order(r):
        r['EA']['per_case']['C5H']['row_radii_m'] = list(reversed(RADII))
    check('AMB22_EA_ROW_RADII_WRONG_ORDER_RECORD_DEFECT_NO_RUN', run_eval(out, 'ea_order', mutate=ea_order), 'NO_RUN', ids=('AMB-22',))
    Rnp = base_runs(**{'C6T': remake('C6T', probe=False)})

    def ea_c6t(r):
        r['EA']['per_case']['C6T'] = {'result_sha256': Rnp['C6T']['result_sha256'], 'E_A_rows_km_s': [0.005 * TAU[i] for i in IDS],
                                      'accepted_iteration': 6, 'row_radii_m': list(RADII)}
    check('AMB22_TAIL_RECORD_WITHOUT_PROBE_R_FALLS_BACK_TO_EA_RECORD', run_eval(out, 'ea_fallback', R=Rnp, mutate=ea_c6t), 'ADOPT_TAIL',
          ids=('AMB-22', 'G4'), extra=lambda e: e['tests']['T1_H']['noise']['EA_sources'] == ['route_a_record', 'EA_record']
          and e['validity']['C6T']['uvt']['E_A_row_order'] == 'UNVERIFIED_NO_PROBE_R')
    check('AMB22_TAIL_RECORD_UNVERIFIED_AND_NO_EA_ENTRY_INCOMPLETE', run_eval(out, 'ea_none', R=Rnp), 'INCOMPLETE', ids=('AMB-22', 'G4'),
          extra=lambda e: e['tests']['T1_H']['status'] == 'INCOMPLETE')
    check('AMB22_TAIL_PROBE_R_NOT_REGISTERED_RADII_INVALID',
          run_eval(out, 'ea_probe', R=base_runs(**{'C6T': remake('C6T', uvt_over={'probe_R_m': [r * 1.01 for r in RADII]})})), 'INCOMPLETE',
          ids=('AMB-22',), extra=lambda e: 'UVT_PROBE_R_NOT_REGISTERED_ROW_RADII' in e['validity']['C6T']['V3_mismatch'])
    # ================================================================ A48 AMB-13 key-equivalence map [M9, S2] / AMB-14 seed factor
    num_d5 = numerics_for('C4T-D5')
    num_d5['route_a']['seed_source_rtol_factor'] = 1.0
    cb_nomap = case_block(over=lambda cb: cb['cases']['C4T-D5']['normalized_spec_equal'].update({'/numerics': copy.deepcopy(num_d5)}))
    km = [{'pointer': '/numerics/route_a/seed_source_rtol_factor', 'absent_equivalent_value': 1.0,
           'b0_identity_evidence': 'B0 plan identity: absent seed_source_rtol_factor reproduces v009 (synthetic)'}]
    cb_map = case_block(keymap=km, over=lambda cb: cb['cases']['C4T-D5']['normalized_spec_equal'].update({'/numerics': copy.deepcopy(num_d5)}))
    t('AMB13_CASE_BLOCK_WITH_KEY_MAP_VALID', not M.validate_case_block(cb_map), ids=('AMB-13',), why=M.validate_case_block(cb_map))
    Rd5 = base_runs(**{'C4T-D5': remake('C4T-D5', numerics=copy.deepcopy(num_d5))})
    check('AMB13_UNMAPPED_EXTRA_KEY_FAILS_V3', run_eval(out, 'km_none', R=Rd5, cb=cb_nomap), 'INCOMPLETE', ids=('AMB-13',),
          extra=lambda e: any('numerics_not_byte_equal_to_C5H' in x for x in e['validity']['C4T-D5']['V3_mismatch']))
    check('AMB13_MAPPED_DEFAULT_KEY_WITH_B0_COVERING_60b46130_ADOPTS', run_eval(out, 'km_ok', R=Rd5, cb=cb_map, b0_c5h=True), 'ADOPT_TAIL',
          ids=('AMB-13', 'M9', 'S2', 'S28'), extra=lambda e: e['validity']['C4T-D5']['key_equivalence_map_used'] == [km[0]['pointer']])
    check('AMB13_MAPPED_KEY_WITHOUT_B0_COVERAGE_INVALID', run_eval(out, 'km_nob0', R=Rd5, cb=cb_map), 'INCOMPLETE', ids=('AMB-13', 'G7'),
          extra=lambda e: any('KEY_EQUIVALENCE_MAP_USED_WITHOUT_B0' in x for x in e['validity']['C4T-D5']['V3_mismatch']))
    num_d5b = copy.deepcopy(num_d5)
    num_d5b['route_a']['seed_source_rtol_factor'] = 0.5
    check('AMB13_MAPPED_KEY_WITH_NON_DEFAULT_VALUE_NOT_DROPPED', run_eval(out, 'km_val', R=base_runs(**{'C4T-D5': remake('C4T-D5', numerics=num_d5b)}),
                                                                          cb=cb_map, b0_c5h=True), 'INCOMPLETE', ids=('AMB-13', 'AMB-14'))
    num_c4 = numerics_for('C4T')
    num_c4['route_a']['seed_source_rtol_factor'] = 0.5
    check('AMB14_BASE_T_CASE_SEED_FACTOR_0p5_INVALID', run_eval(out, 'seed05', R=base_runs(**{'C4T': remake('C4T', numerics=num_c4)})), 'INCOMPLETE',
          ids=('AMB-14', 'P14', 'D4'), extra=lambda e: 'route_a.seed_source_rtol_factor_not_absent_or_1' in e['validity']['C4T']['V3_mismatch'])
    bad_cb = case_block(over=lambda cb: cb['cases']['C4T']['normalized_spec_equal'].update({'/numerics': num_c4}))
    t('AMB14_CASE_BLOCK_REGISTERING_SEED_FACTOR_0p5_REFUSED', any('seed_source_rtol_factor' in w for w in M.validate_case_block(bad_cb)), ids=('AMB-14',))
    # ================================================================ A48 AMB-16 [M10, S5]
    check('AMB16_V2_FAILURE_NEXT_STEP_IS_NAMED_DEFECT_RERUN_UNDER_V007', run_eval(out, 'v2', R=base_runs(**{'C2T': remake('C2T', dlast=0.02)})),
          'INCOMPLETE', ids=('AMB-16', 'M10', 'S5', 'S59'),
          extra=lambda e: e['decision']['next_step']['C2T']['V2'].startswith('named defect V2') and 'A48 AMB-16' in e['decision']['next_step']['C2T']['V2'])
    # ================================================================ A48 AMB-20 [M11, B2]
    adm = CTX['c5h_admission']
    t('AMB20_C5H_ADMITTED_FROM_PINNED_BYTES_REVIEW_DIFF_DRYRUN', adm['admitted'] and not adm['failed'], ids=('AMB-20', 'M11', 'B2'), checks=adm['checks'])
    t('AMB20_A48_LITERAL_PREMISE_SHAS_REVIEWED_CARRIES_60b46130_IS_FALSE_ON_BYTES_REPORTED_NOT_A_GROUND',
      adm['a48_literal_premise_shas_reviewed_carries_60b46130'] is False and 'a48' not in ' '.join(adm['checks']).lower(),
      ids=('AMB-20', 'B2', 'A50.AMB20'))

    check('AMB20_ADMISSION_BASIS_FAILING_MAKES_C5H_INVALID',
          run_eval(out, 'adm', ctx_over={'c5h_admission': dict(adm, admitted=False, failed=['review_verdict_PASS'])}), 'INCOMPLETE',
          ids=('AMB-20',), extra=lambda e: any('C5H_ADMISSION_AMB20' in x for x in e['validity']['C5H']['V3_mismatch']))
    # ================================================================ verifier defects D1-D9
    check('D1_I1T_VERDICT_FAIL_WITH_CLEAN_BUILDS_RECORD_DEFECT_NO_RUN_A54_S5',          # [R5 adapted: A54 S5]
          run_eval(out, 'd1', mutate=lambda r: r['I1T'].update(verdict='FAIL'), auto_verdict=False), 'NO_RUN',
          ids=('D1', 'S24', 'A54.S5'), extra=lambda e: 'VERDICT_FAIL_CONTRADICTS_DATA:I1T' in e['gates']['I1T']['codes'])
    check('D1_I1T_FAIL_VERDICT_WITH_A_FAILING_BUILD_CASES_INCOMPLETE_A54_S5',
          run_eval(out, 'd1b', mutate=lambda r: (r['I1T'].update(verdict='UV_TAIL_SOURCE_MISMATCH'),
                                                 r['I1T']['builds'][0].update(max_rel=1e-9)), auto_verdict=False), 'INCOMPLETE',
          ids=('D1', 'A54.S5'), extra=lambda e: has(e, 'I1T_GATE_FAIL', lab='C4T') and e['gates']['I1T']['status'] == 'FAIL')
    check('D2_DUPLICATE_ROW_ID_HIDING_A_ROW_INCOMPLETE',
          run_eval(out, 'd2', R=base_runs(**{'C4T-KLO': remake('C4T-KLO', raw_ids=IDS[:4] + [IDS[4], IDS[4]] + IDS[6:])})), 'INCOMPLETE',
          ids=('D2', 'S17b'), extra=lambda e: has(e, 'ROWS_NOT_EXACTLY_THE_12_REGISTERED_IDS_EACH_ONCE', lab='C4T-KLO'))
    check('D2_THIRTEEN_ROWS_INCOMPLETE', run_eval(out, 'd2b', R=base_runs(**{'C4T': remake('C4T', raw_ids=IDS + [IDS[0]])})), 'INCOMPLETE',
          ids=('D2', 'S17'))

    def nan_prev(R):
        r = make_run('C4T-KLO', R['C4T-KLO']['adapted']['rows'])
        r['pass_rows'][-2][IDS[3]] = float('nan')
        return r
    check('D3_NAN_IN_PREVIOUS_PASS_FAILS_V2_CROSSCHECK', run_eval(out, 'd3', R=base_runs(**{'C4T-KLO': nan_prev})), 'INCOMPLETE', ids=('D3', 'D9', 'S96'),
          extra=lambda e: 'V2_PASS_ROWS_NOT_FINITE' in e['validity']['C4T-KLO']['V2_codes'])

    def nan_third(R):
        r = make_run('C4T-KLO', R['C4T-KLO']['adapted']['rows'])
        r['pass_rows'][-3][IDS[3]] = float('nan')
        return r
    check('D3_NAN_IN_THIRD_LAST_PASS_E_UNAVAILABLE_TEST_INCOMPLETE_NOT_DECIDABLE', run_eval(out, 'd3c', R=base_runs(**{'C4T-KLO': nan_third})),
          'INCOMPLETE', ids=('D3', 'S96'), extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['status'] == 'INCOMPLETE'
          and 'PASS_ROWS_NONFINITE_OR_MISSING' in str(e['tests']['T3']['pairs']['T3_KLO']['reason']))

    def miss_prev(R):
        r = make_run('C4T-KLO', R['C4T-KLO']['adapted']['rows'])
        del r['pass_rows'][-2][IDS[3]]
        return r
    try:
        check('D3_MISSING_ROW_IN_PREVIOUS_PASS_NO_CRASH', run_eval(out, 'd3b', R=base_runs(**{'C4T-KLO': miss_prev})), 'INCOMPLETE', ids=('D3', 'S97'))
    except Exception as exc:
        t('D3_MISSING_ROW_IN_PREVIOUS_PASS_NO_CRASH', False, ids=('D3',), crash=type(exc).__name__)
    check('D4_TWO_LABELS_ONE_RESULT_ALIASED_INCOMPLETE', run_eval(out, 'd4', R=base_runs(**{'C4T-KLO': lambda R: dict(R['C4T']),
                                                                                           'C4T-KHI': lambda R: dict(R['C4T'])})), 'INCOMPLETE',
          ids=('D4', 'S98'), extra=lambda e: 'ALIAS' in e['validity']['C4T-KLO']['failed'] and 'ALIAS' in e['validity']['C4T']['failed'])
    cb_alias = case_block(over=lambda cb: cb['cases'].__setitem__('C4T-KLO', copy.deepcopy(cb['cases']['C4T'])))
    t('D4_CASE_BLOCK_COPYING_C4T_INTO_K16_REFUSED', any('identical' in w or 'must differ' in w for w in M.validate_case_block(cb_alias)),
      ids=('D4', 'S29'), why=M.validate_case_block(cb_alias)[:3])

    def same_uv(cb):
        n = copy.deepcopy(cb['cases']['C4T-A']['normalized_spec_equal']['/numerics'])
        n['uv_tail'] = uv_cfg('C4T')
        n['column_workers'] = 3
        cb['cases']['C4T-A']['normalized_spec_equal']['/numerics'] = n
        cb['cases']['C4T-A']['uv_tail_config_sha256'] = UVT_SHA['C4T']
    t('D4_RB_FP_PAIR_WITH_IDENTICAL_UV_TAIL_REFUSED', any('C4T and C4T-A' in w for w in M.validate_case_block(case_block(over=same_uv))), ids=('D4',))
    acc = []
    clean = M.finite_or_null({'a': float('nan'), 'b': [1.0, float('inf')], 'c': 2}, '$', acc)
    t('D6_NONFINITE_VALUES_NULLED_AND_NAMED_BEFORE_DUMP', clean == {'a': None, 'b': [1.0, None], 'c': 2} and acc == ['$.a', '$.b[1]'], ids=('D6',))
    p = out / 'd6.json'
    M.write_json_new(p, {'x': float('nan')})
    t('D6_REPORT_FILE_PARSES_WITH_NONFINITE_INPUT', json.loads(p.read_text()) == {'x': None, 'nonfinite_values_nulled': ['$.x']}, ids=('D6',))
    check('D7_PARALLEL8_I4_RECORD_MISSING_INCOMPLETE', run_eval(out, 'd7m', drop=('I4',)), 'INCOMPLETE', ids=('D7', 'N4'),
          extra=lambda e: any('I4' in r for r in e['decision']['reasons']))
    check('D7_PARALLEL8_I4_FAIL_INCOMPLETE_WITH_A47_I4_NEXT_STEP', run_eval(out, 'd7f', mutate=lambda r: r['I4'].update(bitwise_equal=False)),
          'INCOMPLETE', ids=('D7',), extra=lambda e: e['decision']['next_step'].get('I4') == M.I4_NEXT)
    check('D7_I4_DRIVER_NOT_REGISTERED_RECORD_DEFECT_NO_RUN', run_eval(out, 'd7d', mutate=lambda r: r['I4'].update(driver_sha256='5' * 64)),
          'NO_RUN', ids=('D7', 'AMB-02'))
    Rser = base_runs()
    for lab in M.T_CASES:
        Rser[lab] = make_run(lab, Rser[lab]['adapted']['rows'], cw=1)
    check('D7_SERIAL_MODE_DOES_NOT_NEED_I4', run_eval(out, 'd7s', R=Rser, mode='serial_with_exemption', drop=('I4',)), 'ADOPT_TAIL', ids=('D7',))

    def dup_lo(r):
        r['LO'] = json.dumps(r['LO'])[:-1] + ', "verdict": "PASS"}'
    check('D8_GATE_RECORD_WITH_DUPLICATE_KEY_RECORD_DEFECT', run_eval(out, 'd8', mutate=dup_lo), 'NO_RUN', ids=('D8',),
          extra=lambda e: 'DuplicateKey' in str(e['gates']['LO']['codes']))
    check('D9_V2_FIELD_INCONSISTENT_WITH_PASS_ROWS_INVALID', run_eval(out, 'd9', R=base_runs(**{'C4T': remake('C4T', last_change=0.0001)})),
          'INCOMPLETE', ids=('D9',), extra=lambda e: 'V2_FIELD_INCONSISTENT_WITH_PASS_ROWS' in e['validity']['C4T']['V2_codes'])
    # ================================================================ fields S3 / S4; NOTEs A1d, A1e
    cb_s3 = case_block(over=lambda cb: cb['cases']['C4T'].__setitem__('normalized_spec_equal', {'/numerics/uv_tail': uv_cfg('C4T')}))
    t('S3_CASE_BLOCK_WITHOUT_NUMERICS_WHOLE_REFUSED', any('/numerics whole' in w for w in M.validate_case_block(cb_s3)), ids=('S3',))
    num_cw = numerics_for('C4T')
    num_cw['column_workers'] = 3
    check('S3_NUMERICS_COLUMN_WORKERS_CHANGE_CAUGHT_BY_REGISTERED_NUMERICS', run_eval(out, 's3', R=base_runs(**{'C4T': remake('C4T', numerics=num_cw)})),
          'INCOMPLETE', ids=('S3',), extra=lambda e: 'registered:/numerics' in e['validity']['C4T']['V3_mismatch'])
    cb_s4 = case_block(over=lambda cb: cb['cases']['C4T'].__setitem__('uv_tail_config_sha256', '8' * 64))
    t('S4_UV_TAIL_CONFIG_SHA_NOT_LIBRARY_SHA_OF_REGISTERED_BLOCK_REFUSED', any('pinned-library sha' in w for w in M.validate_case_block(cb_s4)), ids=('S4',))

    def eps_two(r):
        r['EPS']['shells'][0]['refinements'] = 2
    check('A1d_EPS_TWO_REFINEMENTS_IS_TWO_FAILURES_UNCERTIFIED', run_eval(out, 'eps2', mutate=eps_two), 'NUMERICS_UNCERTIFIED', ids=('A1d',))

    def rbfp_zero(r):
        r['RB_FP']['dV_static_shells_km_s'] = {'4-8': [0.0] * 12, '8-32': [0.0] * 12}
    check('A1e_RB_FP_KAPPA_UNDEFINED_IS_NOT_A_PASS', run_eval(out, 'kappa0', mutate=rbfp_zero), 'INCOMPLETE', ids=('A1e',),
          extra=lambda e: e['tests']['RB_FP']['status'] == 'INCOMPLETE')
    # ================================================================ carried A47 / RA tests
    check('A47_I1_INVALID_T_CASE_CANNOT_REACH_NOT_UV_RESIDUAL', run_eval(out, 'i1a', R=base_runs(d23=big23, d34=big34, **{'C3T': remake('C3T', maxit=16)})),
          'INCOMPLETE', extra=lambda e: e['decision']['tests_read'] is False)
    check('A47_I1_INVALID_T_CASE_CANNOT_REACH_SOURCE_REPRESENTATION_K_DEPENDENT',
          run_eval(out, 'i1b', R=base_runs(d23=big23, d34=big34, **{'C2T': remake('C2T', cw=1)}), mutate=srk_kdep), 'INCOMPLETE')
    check('A47_I1_INVALID_C5H_READS_INCOMPLETE', run_eval(out, 'i1c', R=base_runs(**{'C5H': remake('C5H', driver=V010)})),
          'INCOMPLETE', extra=lambda e: any(r.startswith('C5H') for r in e['decision']['reasons']))
    check('A47_I1_INVALID_C4T_D5_READS_INCOMPLETE', run_eval(out, 'i1d', R=base_runs(), packets_bad=('C4T-D5',)), 'INCOMPLETE',
          extra=lambda e: any(r.startswith('C4T-D5') for r in e['decision']['reasons']))
    s_ = 0.99 / max(abs(D34[i]) / TAU[i] for i in IDS)
    ev = run_eval(out, 'g1', R=base_runs(d23={i: s_ * D23[i] for i in IDS}, d34={i: s_ * D34[i] for i in IDS}))
    t1 = ev['tests']['T1']
    t('RA6_G1_R3_SCALED_MAX_BASED_PASSES_PER_ROW_FAILS', t1['shape_pass_V005'] and not t1['per_row_clause_pass'] and t1['status'] == 'FAIL'
      and t1['fail_by'] == ['PER_ROW'] and not t1['floor_like'] and ev['decision']['outcome'] in ('NOT_UV_RESIDUAL', 'SOURCE_REPRESENTATION_K_DEPENDENT'),
      outcome=ev['decision']['outcome'])
    g2a = {i: (0.3 if i.endswith('_04') else 2.0) * TAU[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(IDS)}
    g2b = {i: (0.84 if i.endswith('_04') else 0.4) * TAU[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(IDS)}
    ev = run_eval(out, 'g2', R=base_runs(d23=g2a, d34=g2b))
    t1 = ev['tests']['T1']
    t('RA6_G2_GROWING_ROW04_HIDDEN_UNDER_MAX_CAUGHT', t1['shape_pass_V005'] and t1['status'] == 'FAIL'
      and [i[-2:] for i, x in t1['per_row_clause'].items() if x.startswith('FAIL')] == ['04'], outcome=ev['decision']['outcome'])
    g3b = {i: (-0.05 if i.endswith('_03') else 0.8) * TAU[i] for i in IDS}
    ev = run_eval(out, 'g3', R=base_runs(d23={i: 2.0 * TAU[i] for i in IDS}, d34=g3b))
    t('RA6_G3_SIGN_CHANGE_ROW03_CAUGHT', ev['tests']['T1']['per_row_clause'][IDS[2]] == 'FAIL_SIGN' and ev['tests']['T1']['status'] == 'FAIL')
    g4a = {i: (1e-7 if i.endswith('_07') else 2.0 * TAU[i]) for i in IDS}
    g4b = {i: (1e-6 if i.endswith('_07') else 0.8 * TAU[i]) for i in IDS}
    ev = run_eval(out, 'g4', R=base_runs(d23=g4a, d34=g4b))
    t('RA6_G4_TINY_EXEMPTION_PICARD_NOISE_ROW_PASSES', ev['tests']['T1']['status'] == 'PASS' and ev['tests']['T1']['tiny_rows'] == [IDS[6]]
      and ev['decision']['outcome'] == 'ADOPT_TAIL', outcome=ev['decision']['outcome'])
    g5a, g5b = dict(g2a), dict(g2b)
    g5a[IDS[3]], g5b[IDS[3]] = 0.01 * TAU[IDS[3]], 0.12 * TAU[IDS[3]]
    ev = run_eval(out, 'g5', R=base_runs(d23=g5a, d34=g5b))
    t('RA6_G5_TINY_BLIND_SPOT_T1_PASSES', ev['tests']['T1']['status'] == 'PASS' and IDS[3] in ev['tests']['T1']['tiny_rows'])
    r4 = ev['rows_km_s']['C4T']
    c6 = shift(r4, 0.1)
    c6[IDS[3]] = r4[IDS[3]] + 1.44 * TAU[IDS[3]] * (1 if g5b[IDS[3]] > 0 else -1)
    check('RA6_G5_BACKSTOP_T1_H_NO_TINY_HIGHER_K_DISAGREEMENT', run_eval(out, 'g5b', R=base_runs(d23=g5a, d34=g5b, **{'C6T': make_run('C6T', c6)})),
          'HIGHER_K_DISAGREEMENT')
    tiny23 = {i: 0.10 * TAU[i] for i in IDS}
    tiny34 = {i: 0.09 * TAU[i] for i in IDS}
    ev = run_eval(out, 'tinymax', R=base_runs(d23=tiny23, d34=tiny34))
    t('A47_I2_TINY_DOES_NOT_EXEMPT_MAX_BASED_SHAPE_PASS', ev['tests']['T1']['per_row_clause_pass'] and not ev['tests']['T1']['shape_pass_V005']
      and ev['decision']['outcome'] == 'FLOOR_LIKE', outcome=ev['decision']['outcome'])
    # ---- BRACKET_HULL_MISS from on-disk failure records (+ AMB-16: no V4/V5 for a call without a packet)
    for tag, block, want in (('hull', CTX['ra4_block'], 'BRACKET_HULL_MISS'),
                             ('offhull', {'mode': 'rule', 'rule': {**CTX['ra4_block']['rule'], 'fs_absolute_overrides': {'0': [3.025e8, 3.17625e8]}}},
                              'BRACKET_MISS_OFF_RA4_BLOCK')):
        d = out / 'runs' / ('bracket_' + tag)
        sd = d / 'stages' / '05_fs_columns_00'
        (sd / 'columns').mkdir(parents=True)
        (sd / 'columns' / 'finish.json').write_text(json.dumps({'status': 'LAGGED_FREE_SURFACE_COLUMNS_ONLY', 'completed': [],
                                                                 'failures': [{'index': 1, 'type': 'ValueError',
                                                                               'message': 'MASS_ENTHALPY_NOT_BRACKETED: supply a resolved compact-support bracket'}]}))
        res = {'schema': M.RESULT_SCHEMA, 'status': 'FAILED_AT_STAGE', 'valid': False, 'reasons': ["stage(s) exited nonzero: ['fs_rotation']"],
               'driver_sha256': V010, 'call_spec_sha256': 'd' * 64, 'passes': [],
               'stage_records': [{'name': 'fs_columns_00', 'kind': 'columns_v001', 'exit_code': 0, 'stage_dir': str(sd)},
                                 {'name': 'fs_rotation', 'kind': 'rotation_v001', 'exit_code': 1, 'stage_dir': str(d / 'stages' / '09')}]}
        raw = json.dumps(res).encode()
        (d / 'result.json').write_bytes(raw)
        rs = hashlib.sha256(raw).hexdigest()
        (d / 'finish.json').write_text(json.dumps({'status': 'FAILED_AT_STAGE', 'result_sha256': rs}))
        Path(str(d) + '.receipt.json').write_text(json.dumps(receipt_for(rs, str(d / 'result.json'), 'd' * 64, V010, 'FAILED_AT_STAGE')))
        (d / 'start.json').write_text(json.dumps({'normalized_spec': {'galaxy': 'DDO154', 'numerics': {'brackets': block}}}))
        run = M.read_run('C3T', str(d), dict(CTX, case_block=CB), True)
        ev = run_eval(out, 'br_' + tag, R=base_runs(**{'C3T': run}))
        nx = ev['decision']['next_step'].get('C3T', {}) if isinstance(ev['decision']['next_step'], dict) else {}
        check('BRACKET_%s_READING_AMB16_NEXT_STEP' % tag.upper(), ev, 'INCOMPLETE', ids=('AMB-16', 'M10'),
              extra=lambda e, want=want, nx=nx: e['validity']['C3T']['reading'] == want and 'V4' not in nx and 'V5' not in nx
              and (nx.get('V1') == M.RA4_NEXT if want == 'BRACKET_HULL_MISS' else nx.get('V1', '').startswith('named defect V1')))
    ro1 = ro1b(fired=True, events=[{'code': M.RO1_CODE, 'refusal': 'NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH', 'query': 3,
                                    'phi_rad': 0.785, 'R_kpc': 1.48, 'numerator': -0.2, 'denominator': 1.1, 'after_convergence': True}])
    check('RO1_FIRED_IN_T_RUN_RECORDED_NOT_INVALID', run_eval(out, 'ro1', R=base_runs(**{'C6T': remake('C6T', ro1=ro1)})),
          'ADOPT_TAIL', ids=('AMB-15',), extra=lambda e: e['validity']['C6T']['valid_all'] and 'C6T' in e['ro1_recorded'])
    bad_ro1 = copy.deepcopy(ro1)
    del bad_ro1['events'][0]['denominator']
    check('RO1_RECORD_MISSING_FIELD_LOUD', run_eval(out, 'ro1bad', R=base_runs(**{'C6T': remake('C6T', ro1=bad_ro1)})), 'INCOMPLETE',
          extra=lambda e: 'FIELD_MISSING:result:route_a_outcome/ro1/events[0]:denominator' in e['validity']['C6T']['V3_mismatch'])
    ro1d = copy.deepcopy(ro1)
    ro1d['events'][0]['refusal'] = 'DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed'
    check('A49_1_A50_DEGENERATE_RADIAL_EULER_FULL_L205_TEXT_IS_AN_RO1_REFUSAL', run_eval(out, 'a49dre', R=base_runs(**{'C6T': remake('C6T', ro1=ro1d)})),
          'ADOPT_TAIL', ids=('A49.1', 'A50.A49_EXACT_TEXTS'), extra=lambda e: 'C6T' in e['ro1_recorded'])
    ro1t = copy.deepcopy(ro1)
    ro1t['events'][0]['refusal'] = 'DEGENERATE_RADIAL_EULER'
    check('A50_A49_BARE_DEGENERATE_TOKEN_IS_NOT_AN_RO1_TEXT_INVALID', run_eval(out, 'a49bare', R=base_runs(**{'C6T': remake('C6T', ro1=ro1t)})),
          'INCOMPLETE', ids=('A49.1', 'A50.A49_EXACT_TEXTS'), extra=lambda e: 'RO1_EVENT_REFUSAL' in e['validity']['C6T']['V3_mismatch'])
    check('A49_2_RO1_CASE_WITH_UNARMED_WORKER_INVALID',
          run_eval(out, 'a49arm', R=base_runs(**{'C4T': remake('C4T', ro1=ro1b(armed=False))})),
          'INCOMPLETE', ids=('A49.2',), extra=lambda e: 'RO1_NOT_ARMED' in e['validity']['C4T']['V3_mismatch'])
    noarm = {'rule': 'RO1', 'fired': False, 'events': []}
    check('A49_2_RO1_RECORD_WITHOUT_ARMED_FIELD_LOUD', run_eval(out, 'a49noarm', R=base_runs(**{'C4T': remake('C4T', ro1=noarm)})), 'INCOMPLETE',
          ids=('A49.2',), extra=lambda e: 'FIELD_MISSING:result:route_a_outcome/ro1:armed' in e['validity']['C4T']['V3_mismatch'])

    def c5h_ro1(R, armed):
        r = make_run('C5H', R['C5H']['adapted']['rows'])
        r['route_a_outcome']['ro1'] = ro1b(armed=armed)
        return r
    check('A49_2_UNARMED_RO1_BLOCK_ON_C5H_VALID', run_eval(out, 'a49c5h', R=base_runs(**{'C5H': lambda R: c5h_ro1(R, False)})), 'ADOPT_TAIL', ids=('A49.2',))
    check('A49_2_ARMED_RO1_BLOCK_ON_NON_RO1_C5H_INVALID', run_eval(out, 'a49c5ha', R=base_runs(**{'C5H': lambda R: c5h_ro1(R, True)})), 'INCOMPLETE',
          ids=('A49.2',))
    check('A50_ROOT12_IDENTITY_RUN_UNARMED_RO1_INVALID_INCOMPLETE',
          run_eval(out, 'a49id', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS}, 'Z2-OFF': identity_run('Z2-OFF', armed=False)}),
          'INCOMPLETE', ids=('A49.4', 'A50.root12'), extra=lambda e: e['identity_runs']['Z2-OFF']['ro1_armed'] is False
          and 'RO1_NOT_ARMED' in e['identity_runs']['Z2-OFF']['ro1_codes'])
    check('A50_ROOT12_IDENTITY_RUN_WORKER_NOT_ON_CUSTODY_LIST_INCOMPLETE_ON_Z2_A52_1',     # [R4 adapted: B0prime_RERUN is unarmed by A52.1]
          run_eval(out, 'a50idpin', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS},
                                         'Z2': identity_run('Z2', ro1_over={'worker_sha256': '7' * 64})}),
          'INCOMPLETE', ids=('A50.root12',), extra=lambda e: 'RO1_WORKER_NOT_ON_CUSTODY_LIST' in e['identity_runs']['Z2']['ro1_codes'])
    check('A50_ROOT12_IDENTITY_RUNS_ARMED_ON_CUSTODY_LIST_ADOPT_B0PRIME_UNARMED_A52_1', run_eval(out, 'a50idok'), 'ADOPT_TAIL',
          ids=('A50.root12', 'A52.1'),
          extra=lambda e: all(e['identity_runs'][n]['ro1_armed'] is True and not e['identity_runs'][n]['ro1_codes'] for n in ('Z2', 'Z2-OFF'))
          and e['identity_runs']['B0prime_RERUN']['ro1_armed'] is False and not e['identity_runs']['B0prime_RERUN']['ro1_codes'])
    check('RA5a_RO1_FIRED_IN_IDENTITY_RUN_NO_RUN', run_eval(out, 'ro1id', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS}, 'Z2': identity_run('Z2', ro1_fired=True)}),
          'NO_RUN')
    check('A47_I5_MAX_ITERATIONS_16_INVALID', run_eval(out, 'maxit', R=base_runs(**{'C4T-KHI': remake('C4T-KHI', maxit=16)})),
          'INCOMPLETE', extra=lambda e: 'route_a.max_iterations!=32' in e['validity']['C4T-KHI']['V3_mismatch'])
    ev = run_eval(out, 'iter')
    t('A47_I5_ACCEPTED_ITERATION_REPORTED', all(ev['accepted_route_a_iteration'][c] == 6 for c in M.REGISTERED), ids=('AMB-21',))
    check('A47_I4_PARALLEL8_SERIAL_T_CASE_INVALID', run_eval(out, 'cw1', R=base_runs(**{'C4T': remake('C4T', cw=1)})), 'INCOMPLETE')
    check('A47_I4_SERIAL_WITH_EXEMPTION_ALTERNATIVE_ADOPTS', run_eval(out, 'serial', R=Rser, mode='serial_with_exemption'), 'ADOPT_TAIL')
    check('A47_I4_PARALLEL8_C4TD5_SERIAL_NOT_EXEMPT', run_eval(out, 'd5ser', R=base_runs(**{'C4T-D5': remake('C4T-D5', cw=1)})),
          'INCOMPLETE', extra=lambda e: any('numerics_not_byte_equal_to_C5H' in x for x in e['validity']['C4T-D5']['V3_mismatch']))

    def i1t_fail(r):
        r['I1T']['builds'][3]['max_rel'] = 1e-9
    check('I1T_FAIL_CASE_INVALID_INCOMPLETE', run_eval(out, 'i1t', mutate=i1t_fail), 'INCOMPLETE', ids=('AMB-11',),
          extra=lambda e: 'I1T' in e['validity'][M.T_CASES[3]]['failed'])
    check('UVT_FLAG_INCONSISTENT_INVALID', run_eval(out, 'uvtinc', R=base_runs(**{'C4T': remake('C4T', uvt_over={'M_T_accepted': 0.4})}),
                                                    mutate=lambda r: (r['MT']['per_case']['C4T'].update(M_T_accepted=0.05), r['MT'].update(verdict='PASS'))),

          'INCOMPLETE', extra=lambda e: 'UVT_FLAG_INCONSISTENT' in e['validity']['C4T']['V3_mismatch'])

    check('EA_UNAVAILABLE_READS_INCOMPLETE_UNRESOLVED', run_eval(out, 'eanone', R=base_runs(**{'C6T': remake('C6T', ea_none=True)})), 'INCOMPLETE',
          ids=('AMB-08',), extra=lambda e: e['tests']['T1_H']['status'] == 'INCOMPLETE')

    def mt_mismatch(r):                     # internally consistent MT record (A50 S2) that contradicts the C4T tail record
        r['MT']['per_case']['C4T'].update(flags=[M.FLAG_TSU], M_T_accepted=0.3)
        r['MT']['verdict'] = 'FAIL'
    check('MT_CROSSCHECK_MISMATCH_RECORD_DEFECT_NO_RUN', run_eval(out, 'mt', mutate=mt_mismatch), 'NO_RUN', ids=('AMB-25',),
          extra=lambda e: 'CROSSREF_MISMATCH:MT:per_case/C4T/flags' in e['gates']['MT']['codes'])


    def mt_short(r):
        del r['MT']['per_case']['C6T']
    check('AMB25_MT_NOT_COVERING_EVERY_T_CASE_RECORD_DEFECT', run_eval(out, 'mtshort', mutate=mt_short), 'NO_RUN', ids=('AMB-25',))

    def rb_eps(r):
        r['RB_FP']['eps_max'] = 7e-4
    check('RB_FP_EPS_CROSSREF_RECORD_DEFECT_NO_RUN', run_eval(out, 'rbeps', mutate=rb_eps), 'NO_RUN', ids=('AMB-09',))

    def wrong_ref(r):
        r['B1']['run_result_sha256'] = '9' * 64
    check('GATE_CROSSREF_RUN_SHA_MISMATCH_NO_RUN', run_eval(out, 'xref', mutate=wrong_ref), 'NO_RUN', ids=('AMB-02',))

    def lo_state(r):
        r['LO']['state_result_sha256'] = '8' * 64
    check('LO_WRONG_STATE_IS_DEFECT_NOT_NON_LAPSE_TAIL_MATERIAL', run_eval(out, 'lostate', mutate=lo_state), 'NO_RUN', ids=('AMB-02',))
    check('AMB23_LO_NGC_REPORTED_NOT_REQUIRED', run_eval(out, 'longc', drop=('LO_NGC',)), 'ADOPT_TAIL', ids=('AMB-23',),
          extra=lambda e: e['reported']['LO_NGC']['status'] == 'MISSING')
    # ================================================================ blinding (verify blinding B1-B4, N3)
    canary_run = make_run('C5H', dict(C4))
    canary_run['result'].update(status='FAILED_%s' % CANARY, driver_sha256=CANARY, valid=False)
    canary_run['adapted'].update(status=canary_run['result']['status'], valid=False)
    canary_run['receipt'].update(stop_reason='WALL_CAP row05=%s' % CANARY)
    canary_run['failure'] = M.classify_failure(canary_run, CTX)
    v = M.case_validity('C5H', canary_run, dict(CTX, case_block=CB), None, None, None)
    txt = json.dumps(M.blinded_case(v))
    t('B1_RECORD_STRINGS_WITH_A_NUMBER_NEVER_REACH_A_BLINDED_CODE', CANARY not in txt and '41.23' not in txt, ids=('blinding B1',), sample=txt[:300])
    g = {'gate': 'T2I', 'status': 'FAIL', 'codes': ['VERDICT:T2I:%s' % M._enum('FAIL max_rel=%s' % CANARY, pattern=M._RE_UPPER_CODE),
                                                    'x=%s' % CANARY],
         'fields_read': ['per_case/C5H@%s/x' % CANARY], 'record': None, 'crossref': {}}
    bg = M.blinded_gate(g)
    t('B1_GATE_VERDICT_ENUM_AND_REDACTION_BACKSTOP', CANARY not in json.dumps(bg) and bg['blinding_redaction_applied'] is True
      and bg['codes'][0] == 'VERDICT:T2I:OTHER', ids=('blinding B1',), got=bg['codes'])
    t('B1_REDACTION_KEEPS_SHAS_AND_CODE_CONSTANTS', M._blind_str('driver_not_allowed:%s T2I_MAX_GT_1e-12 x=%s' % ('3e5' + 'a' * 61, CANARY), []) ==
      'driver_not_allowed:%s T2I_MAX_GT_1e-12 x=<REDACTED_NUMBER>' % ('3e5' + 'a' * 61), ids=('blinding B1',))

    def ea_label(r):
        r['EA']['per_case']['C5H@%s' % CANARY] = dict(r['EA']['per_case']['C5H'])
    ev = run_eval(out, 'ealabel', mutate=ea_label)
    t('B1_EA_LABEL_EXACT_MATCH_NO_VALUE_IN_CODE', ev['gates']['EA']['status'] == 'RECORD_DEFECT' and CANARY not in json.dumps(ev['gates']['EA']['codes']),
      ids=('blinding B1',), codes=ev['gates']['EA']['codes'])

    def i1t_label(r):
        r['I1T']['builds'][0]['case'] = CANARY
    ev = run_eval(out, 'i1tlabel', mutate=i1t_label)
    t('B1_I1T_UNREGISTERED_CASE_NO_VALUE_IN_CODE', ev['gates']['I1T']['status'] == 'RECORD_DEFECT' and CANARY not in json.dumps(ev['gates']['I1T']['codes']),
      ids=('blinding B1',))
    root = out / 'disk'
    good = synthetic_completed_result(C4, numerics_for('C4T'), drv=V010, spec='c' * 64)
    dmal = write_run_dir(root, 'C4T_badfinish', good, finish='{not json')
    run = M.read_run('C4T', str(dmal), dict(CTX, case_block=CB), True)
    vv = M.case_validity('C4T', run, dict(CTX, case_block=CB), None, None, None)
    t('N3_MALFORMED_FINISH_JSON_IS_A_CODE_NOT_AN_EXCEPTION', 'FINISH_UNREADABLE:JSONDecodeError' in vv['V1_codes'] and vv['valid_all'] is False,
      ids=('N3',), codes=vv['V1_codes'])
    ddup = write_run_dir(root, 'C4T_dupkey', None, raw=b'{"schema": "a", "schema": "b"}', receipt=False)
    run = M.read_run('C4T', str(ddup), dict(CTX, case_block=CB), True)
    t('D8_RESULT_JSON_WITH_DUPLICATE_KEY_UNREADABLE', run.get('unreadable') == 'RESULT_UNREADABLE:DuplicateKey', ids=('D8',))
    nores = dict(good, rows=[{'id': i} for i in IDS])
    dmis = write_run_dir(root, 'C5H_missing_speed', nores)
    run = M.read_run('C5H', str(dmis), dict(CTX, case_block=CB), False)
    vv = M.case_validity('C5H', run, dict(CTX, case_block=CB), None, None, None)
    t('N3_ROW_WITHOUT_SPEED_IS_A_CODE_NOT_AN_EXCEPTION', vv['valid_all'] is False and 'ADAPT_RESULT_FAILED:KeyError' in vv['V1_codes'], ids=('N3',))
    # ---- CLI on real bytes (+ A47 I3 blinding)
    cbp = out / 'CASE_BLOCK_PROBE.json'
    cbp.write_text(json.dumps(CB, indent=1))
    man = {'schema': M.MANIFEST_SCHEMA, 'cases': {'C2T': CT + '/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001', 'C3T': CT + '/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001',
                                                  'C4T': CT + '/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001', 'C5H': CT + '/runs_ext/KMAX_A2F10_C5R3_RUN_V001'},
           'identity_runs': {}, 'gates': {}}
    mp = out / 'MANIFEST_REAL_PROBE.json'
    mp.write_text(json.dumps(man, indent=1))
    assert FORBIDDEN not in json.dumps(man)

    def cli(name, *extra, manifest=mp, cbpath=cbp):
        assert FORBIDDEN not in Path(manifest).read_text() or 'interlock' in Path(manifest).read_text()
        p = subprocess.run([PY, '-I', '-B', str(CMP), '--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(manifest), '--case-block', str(cbpath),
                            '--outdir', str(out / name), '--test-allow-unpinned-prereg', *REGARGS] + list(extra), capture_output=True, text=True)
        (out / (name + '.stdout.txt')).write_text(p.stdout + '\n--- stderr ---\n' + p.stderr)
        return p
    p = cli('E2E_REAL_PROBE')
    rep = json.loads((out / 'E2E_REAL_PROBE' / 'KMAX_TAIL_COMPARISON.json').read_text()) if p.returncode == 0 else {}
    t('E2E_REAL_R3_PROBE_READS_INCOMPLETE_NOT_A_SILENT_PASS', p.returncode == 0 and rep['decision']['outcome'] == 'INCOMPLETE' and rep['test_mode']
      and rep['decision']['tests_read'] is False and rep['validity']['C4T']['V4'] and rep['validity']['C4T']['V5']
      and rep['validity']['C4T']['V1'] is True, rc=p.returncode, stderr=p.stderr[-300:])
    speeds = [x for lab in ('C2R3', 'C3R3', 'C4R3') for x in REAL[lab]['rows'].values()]
    p = cli('VALIDITY_ONLY_C4T_C5H', '--validity-only', '--case', 'C4T', '--case', 'C5H')
    txt = (out / 'VALIDITY_ONLY_C4T_C5H' / 'VALIDITY_ONLY.json').read_text() if p.returncode == 0 else ''
    body = json.loads(txt) if txt else {}
    # [R3 harness fix] 64-hex shas are masked first and a speed must appear as a whole number token: in R3 the bare '%.4g' form
    # of a C2R3 speed ('29') matched inside the new script_sha256 hex (a false positive; a sha is not a row value)
    def _tok(fs, s):
        s = re.sub(r'[0-9a-f]{64}', 'h' * 64, s)
        return re.search(r'(?<![0-9.])%s(?![0-9])' % re.escape(fs), s) is not None
    leaks = [x for x in speeds for fmt in ('%r', '%.6f', '%.5f', '%.4f', '%.3f', '%.2f', '%.6g', '%.4g') if _tok(fmt % x, txt) or _tok(fmt % x, p.stdout)]
    nums = []
    _find_numbers(body, '$', nums)
    t('A47_I3_VALIDITY_ONLY_HAS_NO_ROW_VALUE_AND_NO_NUMBER', p.returncode == 0 and not leaks and not nums and body.get('blinded') is True
      and body['cases']['C5H']['reading'] == 'BRACKET_MISS_OFF_RA4_BLOCK' and body['cases']['C4T']['V1'] is True,
      leaks=leaks[:5], numbers=nums[:5], rc=p.returncode, stderr=p.stderr[-300:])
    can_rows = {i: 41.2345678 + 1.1111111 * k for k, i in enumerate(IDS)}
    c5h_res = synthetic_completed_result(can_rows, copy.deepcopy(CTX['c5h_spec_numerics']), drv=M.DRIVER_V009_EXT, spec='9' * 64)
    dcan = write_run_dir(root, 'C5H_CANARY', c5h_res, receipt={'stop_reason': 'WALL_CAP row05=%s' % CANARY})
    man_c = dict(man, cases=dict(man['cases'], C5H=str(dcan)))
    mpc = out / 'MANIFEST_CANARY.json'
    mpc.write_text(json.dumps(man_c))
    p = cli('VALIDITY_ONLY_CANARY_C5H', '--validity-only', '--case', 'C5H', manifest=mpc)
    txt = (out / 'VALIDITY_ONLY_CANARY_C5H' / 'VALIDITY_ONLY.json').read_text() if p.returncode == 0 else ''
    cl = ['%.4f' % x for x in can_rows.values()] + [CANARY, '41.23']
    t('B1_N3_VALIDITY_ONLY_CANARY_C5H_NO_LEAK', p.returncode == 0 and not any(c in txt or c in p.stdout for c in cl),
      ids=('blinding B1', 'N3'), rc=p.returncode, stderr=p.stderr[-300:])
    dcor = write_run_dir(root, 'C5H_CORRUPT', None, raw=b'{"rows": [1, 2', receipt=False)
    mpg = out / 'MANIFEST_GATES.json'
    mpg.write_text(json.dumps(dict(man, cases=dict(man['cases'], C5H=str(dcor)))))
    p = cli('GATES_ONLY_CORRUPT_C5H', '--gates-only', manifest=mpg)
    t('B2_GATES_ONLY_READS_C5H_BY_SHA_ONLY_CORRUPT_RESULT_NO_CRASH', p.returncode == 0, ids=('blinding B2',), rc=p.returncode, stderr=p.stderr[-300:])
    with OpenTrace() as tr, _quiet():
        rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mpc), '--case-block', str(cbp), '--outdir', str(out / 'GATES_ONLY_TRACE'),
                     '--test-allow-unpinned-prereg', *REGARGS, '--gates-only'])
    opened = [x for x in tr.paths if str(dcan.resolve()) in x]
    t('B2_GATES_ONLY_OPENS_ONLY_THE_C5H_RESULT_BYTES', rc == 0 and opened and all(x.endswith('/C5H_CANARY/result.json') for x in opened),
      ids=('blinding B2',), opened=opened)
    with OpenTrace() as tr, _quiet():
        rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mpc), '--case-block', str(cbp), '--outdir', str(out / 'VALIDITY_D5_TRACE'),
                     '--test-allow-unpinned-prereg', *REGARGS, '--validity-only', '--case', 'C4T-D5'])
    opened = [x for x in tr.paths if str(dcan.resolve()) in x]
    t('B3_VALIDITY_ONLY_C4TD5_READS_C5H_NUMERICS_ONLY', rc == 0 and all(x.endswith('/C5H_CANARY/result.json') for x in opened)
      and not any('receipt' in x or 'npz' in x or 'finish' in x for x in opened), ids=('blinding B3',), opened=opened)
    dname = write_run_dir(root / 'interlock', FORBIDDEN, c5h_res)
    mpn = out / 'MANIFEST_INTERLOCK_NAME.json'
    mpn.write_text(json.dumps(dict(man, cases=dict(man['cases'], C5H=str(dname)))))
    p = cli('INTERLOCK_NAME', manifest=mpn)
    t('B4_TEST_MODE_FULL_MODE_REFUSES_REGISTERED_C5H_DIR_NAME', p.returncode == 2 and 'registered C5H' in p.stderr and not (out / 'INTERLOCK_NAME').exists(),
      ids=('blinding B4',))
    dspec = write_run_dir(root, 'C5H_SPEC_STANDIN', c5h_res, start={'call_spec_sha256': M.PIN_C5H_SPEC[1]})
    mps = out / 'MANIFEST_INTERLOCK_SPEC.json'
    mps.write_text(json.dumps(dict(man, cases=dict(man['cases'], C5H=str(dspec)))))
    p = cli('INTERLOCK_SPEC', manifest=mps)
    t('B4_TEST_MODE_FULL_MODE_REFUSES_C5H_CALL_SPEC_60b46130', p.returncode == 2 and '60b46130' in p.stderr, ids=('blinding B4',))
    p = cli('INTERLOCK_SPEC_VALIDITY_ONLY_ALLOWED', '--validity-only', '--case', 'C5H', manifest=mps)
    t('B4_BLINDED_MODES_STILL_ALLOWED_ON_THE_REGISTERED_CALL', p.returncode == 0, ids=('blinding B4',))
    Rp = {'C4T': {'result_sha256': hashlib.sha256(Path(CT + '/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/result.json').read_bytes()).hexdigest()},
          'C5H': {'result_sha256': hashlib.sha256(Path(CT + '/runs_ext/KMAX_A2F10_C5R3_RUN_V001/result.json').read_bytes()).hexdigest()}}
    for lab, k in (('C2T', 'C2R3'), ('C3T', 'C3R3')):
        Rp[lab] = {'result_sha256': hashlib.sha256(Path(M.PIN_R3[k][0]).read_bytes()).hexdigest()}
    Rp.update({c: {} for c in M.T_CASES if c not in Rp})
    gp = write_records(out, 'gates_only_complete', complete_records(Rp, {n: {} for n in M.IDENTITY_RUNS}))
    mpd = out / 'MANIFEST_GATES_COMPLETE.json'
    mpd.write_text(json.dumps(dict(man, gates=gp)))
    p = cli('GATES_ONLY_COMPLETE', '--gates-only', manifest=mpd)
    body = json.loads((out / 'GATES_ONLY_COMPLETE' / 'GATES_ONLY.json').read_text()) if p.returncode == 0 else {}
    nums = []
    _find_numbers(body, '$', nums)
    st = {g: x['status'] for g, x in (body.get('gates') or {}).items()}
    t('RA13_GATES_ONLY_COMPLETE_RECORDS_BLINDED', p.returncode == 0 and not nums and all(v == 'PASS' for v in st.values())
      and not any(x['blinding_redaction_applied'] for x in body['gates'].values()) and body['mt_crosscheck'] == 'MT_FLAG_CROSSCHECK_NOT_RUN_GATES_ONLY',
      ids=('blinding N3', 'RA13'), statuses=st, rc=p.returncode, stderr=p.stderr[-300:])
    p = subprocess.run([PY, '-I', '-B', str(CMP), '--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mp), '--case-block', str(cbp),
                        '--outdir', str(out / 'REFUSE_PIN')], capture_output=True, text=True)
    t('UNPINNED_PREREG_REFUSED_WITHOUT_TEST_FLAG', p.returncode == 2 and 'REFUSED' in p.stderr)
    (out / 'MANIFEST_BAD.json').write_text(json.dumps(dict(man, cases=dict(man['cases'], C9T='/x'))))
    p = cli('REFUSE_LABEL', manifest=out / 'MANIFEST_BAD.json')
    t('UNKNOWN_CASE_LABEL_REFUSED', p.returncode == 2 and 'unknown cases' in p.stderr)
    (out / 'MANIFEST_DUP.json').write_text(json.dumps(man)[:-1] + ', "cases": {}}')
    p = cli('REFUSE_DUP', manifest=out / 'MANIFEST_DUP.json')
    t('D8_MANIFEST_WITH_DUPLICATE_KEY_REFUSED', p.returncode == 2 and 'duplicate JSON key' in p.stderr, ids=('D8',))
    (out / 'CB_SERIAL.json').write_text(json.dumps(CB_SERIAL))
    p = cli('REFUSE_MODE', '--route-a-mode', 'parallel8', cbpath=out / 'CB_SERIAL.json')
    t('A47_I4_ROUTE_A_MODE_SINGLE_PARAMETER_CONFLICT_REFUSED', p.returncode == 2 and 'route-A mode differs' in p.stderr)
    saved = M.V007_PREREG_SHA256
    try:
        M.V007_PREREG_SHA256 = hashlib.sha256(Path(M.PIN_DRAFT_R1[0]).read_bytes()).hexdigest()   # pretend sealed (in-process only)
        err = io.StringIO()
        _e, sys.stderr = sys.stderr, err
        try:
            rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mp), '--case-block', str(cbp), '--outdir', str(out / 'SEALED_NO_V005_PIN')])
        finally:
            sys.stderr = _e
    finally:
        M.V007_PREREG_SHA256 = saved
    t('S1_SEALED_MODE_REFUSES_WITHOUT_FROZEN_V005_ADDENDUM_PIN', rc == 2 and 'frozen V005 addendum' in err.getvalue() and M.PIN_ADDENDUM_V005 is None,
      ids=('blinding S1', 'G9'))
    fp = out / 'FIELDS_TEST.md'
    M.write_field_contract(str(fp))
    t('FIELDS_MD_WRITTEN', fp.is_file() and all(g in fp.read_text() for g in M.ALL_GATES))
    p = subprocess.run([PY, '-I', '-B', str(CMP), '--write-field-contract', str(fp)], capture_output=True, text=True)
    t('FIELDS_MD_NEVER_OVERWRITTEN', p.returncode == 2 and 'exists' in p.stderr, ids=('blinding NOTE',))
    # ================================================================ E-SEAL1: every gate, every field
    R0, IDR0 = base_runs(), {n: identity_run(n) for n in M.IDENTITY_RUNS}
    recs = complete_records(R0, IDR0, rulings=[ruling(M.FLAG_TSU, 'C4T-C5c', 'CLEARED', R=R0)])
    rsha = M.runs_sha_map(R0, IDR0)
    ctx = dict(CTX, case_block=CB)
    common, G = M.gate_field_contract()
    total = bad = 0
    detail, unread = [], []
    for g, r in recs.items():
        p_ = out / 'gates' / 'mf' / ('%s.json' % g)
        p_.parent.mkdir(parents=True, exist_ok=True)
        p_.write_text(json.dumps(r))
        ok0 = M.evaluate_gate(g, str(p_), ctx, rsha)
        if ok0['status'] != 'PASS':
            bad += 1
            detail.append('%s complete record not PASS: %s' % (g, ok0['codes']))
        pats = [_pat(x[0]) for x in common + G[g]]
        for fr in ok0['fields_read']:
            if not any(re.fullmatch(pt, fr) for pt in pats):
                unread.append('%s:%s' % (g, fr))
        for path, expect in _leaf_paths(g, r):
            if len(path) == 1 and path[0] in M.OPTIONAL_GATE_FIELDS.get(g, ()):   # [A52.5] tested on its own (R4_A52_5_*)
                continue
            total += 1
            r2 = copy.deepcopy(r)
            _delete(r2, path)
            q = out / 'gates' / 'mf' / ('%s__%d.json' % (g, total))
            q.write_text(json.dumps(r2))
            ev = M.evaluate_gate(g, str(q), ctx, rsha)
            if g == 'RB_FP' and path[0] == 'dV_static_shells_km_s' and len(path) == 2:   # [A54 S6] named by index, never by label
                expect = 'FIELD_MISSING:RB_FP:dV_static_shells_km_s/<shells[%d]>' % r['shells'].index(path[1])
            if ev['status'] != 'RECORD_DEFECT' or not any(expect in c for c in ev['codes']):
                bad += 1
                detail.append('%s delete %s -> %s %s (expected %s)' % (g, path, ev['status'], ev['codes'], expect))
    t('E_SEAL1_EVERY_GATE_FIELD_DELETION_FAILS_LOUDLY_NAMING_IT', bad == 0 and total > 150, deletions=total, failures=detail[:10])
    t('E_SEAL1_EVERY_FIELD_READ_IS_DOCUMENTED_IN_FIELDS_MD', not unread, undocumented=unread[:20])
    missing = M.evaluate_gate('EPS', None, ctx, rsha)
    t('GATE_RECORD_ABSENT_READS_MISSING', missing['status'] == 'MISSING' and missing['codes'] == ['GATE_RECORD_MISSING:EPS'])
    v = M.case_validity('C4T', dict(make_run('C4T', C4), uvt_record={k: x for k, x in make_run('C4T', C4)['uvt_record'].items() if k != 'E_A_rows_km_s_accepted'}),
                        ctx, {'V4': True, 'V5': True}, {'status': 'PASS', 'per': {c: 'PASS' for c in M.T_CASES}}, None)
    t('UVT_RECORD_MISSING_FIELD_NAMED', 'FIELD_MISSING:route_a_attempt_result:result/uv_tail:E_A_rows_km_s_accepted' in v['V3_mismatch'], codes=v['V3_mismatch'])
    # ================================================================ A50 (V005 addendum A50; R1 recheck B1/S1/S2/N1/N3/N4)
    def rp_clean(pid, branch, R, **kw):
        """Clean R-PAIR members for pid on branch: each member = its base registration + only the branch's R-PAIR leaves.
        R5 [A53]: a PICARD member admits its base route A (route_a.column_workers 1; the base's route_a_outcome, tail record and
        RO1 record; the C5H PICARD member without ro1_workers and with an unarmed, unfired ro1 block): a53_picard_shape, which
        keeps any field a test overrides explicitly (ro1, ra_ident, uvt_over, post)."""
        RP = {pid: {'branch': branch, '_runs': {}}}
        for m in M.PAIRS[pid]:
            key = '%s@RPAIR:%s' % (m, pid)
            num = numerics_for(m)
            if branch == 'PICARD':
                num['picard'] = dict(M.RPAIR_PICARD)
                num.setdefault('route_a', {})['column_workers'] = M.RPAIR_PICARD_COLUMN_WORKERS      # [A53] the Picard leaf
            else:
                num.setdefault('route_a', {})['seed_source_rtol_factor'] = M.RPAIR_ROUTE_A_FACTOR
                if m == M.C5H:                              # [A52.3] the C5H ROUTE_A member spec: route_a.ro1_workers true
                    num.setdefault('route_a', {})['ro1_workers'] = True
            args = dict(dlast=0.0002, q=1 / 3.0, ea=0.005)
            if branch == 'ROUTE_A':                     # [R4 order N-c] a ROUTE_A member recomputes route A: its own identity
                args['ra_ident'] = sha('ra_ident' + key)
            args.update(kw.get(m, {}))
            nover = args.pop('num_over', None)
            post = args.pop('post', None)
            keep = {k for k in ('ro1', 'ra_ident', 'uvt_over') if k in kw.get(m, {})}
            if nover:
                nover(num)
            RP[pid]['_runs'][m] = make_run(key, R[m]['adapted']['rows'], numerics=num, key='rp' + key + branch, **args)
            if branch == 'PICARD':
                a53_picard_shape(RP[pid]['_runs'][m], R[m], keep=keep)
            if post:
                post(RP[pid]['_runs'][m], R)
        return RP

    def ptest(e, pid):
        return e['tests']['T3']['pairs'][pid] if pid.startswith('T3') else e['tests'][pid]
    UNDEC = {'PICARD': lambda lab: {lab: slow}, 'ROUTE_A': lambda lab: {lab: {'ea': 0.2}}}
    NOISY = {'T1_H': 'C6T', 'T2': 'C4T-D5', 'T3_KLO': 'C4T-KLO', 'T3_KHI': 'C4T-KHI'}
    for pid in M.RPAIR_IDS:                                   # [A50 B1] one test per R-PAIR branch for each paired test
        for br in ('PICARD', 'ROUTE_A'):
            mods = UNDEC[br](NOISY[pid])
            Rb = base_runs(**{lab: remake(lab, **kw) for lab, kw in mods.items()})
            RPb = rp_clean(pid, br, Rb)
            check('A50_B1_RPAIR_%s_%s_RESOLVES_ON_ITS_MEMBERS' % (pid, br), run_eval(out, 'b1_%s_%s' % (pid, br), R=Rb, RP=RPb, b0_c5h=True),
                  'ADOPT_TAIL', ids=('A50.B1', 'recheck B1'),
                  extra=lambda e, pid=pid, br=br: ptest(e, pid).get('source') == 'RPAIR' and ptest(e, pid)['noise']['rpair_branch'] == br
                  and all(v['valid_all'] for v in e['rpair_validity'].values()))
    Rt2 = base_runs(**{'C4T-D5': remake('C4T-D5', **slow)})
    RPc = rp_clean('T2', 'PICARD', Rt2, **{'C5H': {'num_over': lambda n: n.update(column_workers=4)}})
    check('A50_B1_C5H_MEMBER_DIFFERING_FROM_ITS_BASE_OUTSIDE_RPAIR_LEAVES_INVALID', run_eval(out, 'b1_c5hoff', R=Rt2, RP=RPc, b0_c5h=True),
          'INCOMPLETE', ids=('A50.B1',), extra=lambda e: any('RPAIR_MEMBER_NUMERICS_DIFFER_FROM_BASE_OUTSIDE_RPAIR_LEAVES' in x
                                                             for x in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch'])
          and any('numerics_not_byte_equal_to_C5H_RPAIR_PARTNER' in x for x in e['rpair_validity']['C4T-D5@RPAIR:T2']['V3_mismatch'])
          and e['tests']['T2']['status'] == 'INCOMPLETE')
    Rk16 = base_runs(**{'C4T-KLO': remake('C4T-KLO', **slow)})
    RPt = rp_clean('T3_KLO', 'PICARD', Rk16, **{'C4T': {'num_over': lambda n: n.update(column_workers=3)}})
    check('A50_B1_T_MEMBER_DIFFERING_FROM_ITS_BASE_OUTSIDE_RPAIR_LEAVES_INVALID', run_eval(out, 'b1_toff', R=Rk16, RP=RPt), 'INCOMPLETE',
          ids=('A50.B1',), extra=lambda e: any('RPAIR_MEMBER_NUMERICS_DIFFER_FROM_BASE_OUTSIDE_RPAIR_LEAVES' in x
                                               for x in e['rpair_validity']['C4T@RPAIR:T3_KLO']['V3_mismatch']))
    RPl = rp_clean('T3_KLO', 'PICARD', Rk16, **{'C4T-KLO': {'num_over': lambda n: n['picard'].update(passes=11)}})
    check('A50_B1_RPAIR_LEAVES_NOT_BYTE_EQUAL_BETWEEN_MEMBERS_INVALIDATES_BOTH', run_eval(out, 'b1_leaves', R=Rk16, RP=RPl), 'INCOMPLETE',
          ids=('A50.B1',), extra=lambda e: 'RPAIR_LEAVES_NOT_BYTE_EQUAL_BETWEEN_MEMBERS' in e['rpair_validity']['C4T@RPAIR:T3_KLO']['V3_mismatch']
          and e['rpair_validity']['C4T@RPAIR:T3_KLO']['valid_all'] is False)
    # ---- root item 11: C5H R-PAIR member under v010 tail OFF, RO1 armed, admitted through B0 identity
    RPd = rp_clean('T2', 'PICARD', Rt2, **{'C5H': {'driver': M.DRIVER_V009_EXT}})
    check('A50_ROOT11_C5H_MEMBER_ON_V009_EXT_NOT_THE_V010_DRIVER_INVALID', run_eval(out, 'r11_drv', R=Rt2, RP=RPd, b0_c5h=True), 'INCOMPLETE',
          ids=('A50.root11',), extra=lambda e: any(x.startswith('driver_not_allowed') for x in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch']))
    Rt2ra = base_runs(**{'C4T-D5': remake('C4T-D5', ea=0.2)})                      # [R5 adapted, A53: only the ROUTE_A C5H
    RPu = rp_clean('T2', 'ROUTE_A', Rt2ra, **{'C5H': {'ro1': ro1b(armed=False)}})     # member runs the RO1 workers armed]
    check('A50_ROOT11_C5H_ROUTE_A_MEMBER_WITHOUT_ARMED_RO1_WORKERS_INVALID_A53', run_eval(out, 'r11_arm', R=Rt2ra, RP=RPu, b0_c5h=True),
          'INCOMPLETE', ids=('A50.root11', 'A53'), extra=lambda e: 'RO1_NOT_ARMED' in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch'])
    check('A50_ROOT11_C5H_MEMBER_WITHOUT_B0_COVERING_60b46130_NOT_ADMITTED', run_eval(out, 'r11_b0', R=Rt2, RP=rp_clean('T2', 'PICARD', Rt2)),
          'INCOMPLETE', ids=('A50.root11',),
          extra=lambda e: 'C5H_RPAIR_MEMBER_NOT_ADMITTED_B0_DOES_NOT_COVER_C5H_SPEC_60b46130' in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch'])
    # ---- S1: RA1 against the C5H spec 60b46130 (registration and C5H run)
    cb_p3 = case_block(over=lambda cb: cb['cases']['C4T-D5']['normalized_spec_equal']['/numerics'].update(column_workers=4))
    t('A50_S1_CASE_BLOCK_D5_NUMERICS_OFF_THE_C5H_SPEC_REFUSED', any('A50 S1' in w for w in M.validate_case_block(cb_p3)),
      ids=('A50.S1', 'recheck S1 P3'), why=M.validate_case_block(cb_p3)[:2])
    cb_ser_p8 = {k: v for k, v in CB_SERIAL.items() if k != 'route_a_mode'}
    t('A50_S1_SERIAL_REGISTRATION_ACCEPTED_ONLY_IN_SERIAL_MODE',
      not M.validate_case_block(cb_ser_p8, route_a_mode='serial_with_exemption') and any('A50 S1' in w for w in M.validate_case_block(cb_ser_p8)),
      ids=('A50.S1',))
    t('A50_S1_AMB13_UNMAPPED_V010_KEY_IN_D5_REGISTRATION_REFUSED', any('A50 S1' in w for w in M.validate_case_block(cb_nomap)), ids=('A50.S1', 'AMB-13'))
    num_c5_off = numerics_for(M.C5H)
    num_c5_off['column_workers'] = 4
    num_d5_off = numerics_for('C4T-D5')
    num_d5_off['column_workers'] = 4
    check('A50_S1_C5H_RUN_NUMERICS_OFF_THE_SPEC_INVALID_EVEN_WITH_D5_MATCHING',
          run_eval(out, 's1_p2', R=base_runs(**{'C5H': remake('C5H', numerics=num_c5_off), 'C4T-D5': remake('C4T-D5', numerics=num_d5_off)}), cb=cb_p3),
          'INCOMPLETE', ids=('A50.S1', 'recheck S1 P2'),
          extra=lambda e: 'C5H_NUMERICS_NOT_SPEC_60b46130_AS_NORMALIZED_BY_ITS_DRY_RUN' in e['validity']['C5H']['V3_mismatch']
          and e['validity']['C4T-D5']['valid_all'])
    t('A50_S1_C5H_REFERENCE_IS_THE_DRY_RUN_NORMALIZATION_ADDING_ONLY_KMAX_NULL',
      CTX['c5h_admission']['dryrun_normalization_added_leaves'] == ['/truncation/kmax_inverse_kpc']
      and not CTX['c5h_admission']['dryrun_normalization_changed_leaves'], ids=('A50.S1',))
    # ---- S2: an MT verdict FAIL for a run is that run's flag; a defective MT record reads NO_RUN
    check('A50_S2_MT_VERDICT_FAIL_WITHOUT_A_FAILING_RUN_NO_RUN', run_eval(out, 's2_p1', mutate=lambda r: r['MT'].update(verdict='FAIL')), 'NO_RUN',
          ids=('A50.S2', 'recheck S2 P1'), extra=lambda e: 'MT_VERDICT_FAIL_WITHOUT_A_FAILING_RUN' in e['gates']['MT']['codes'])

    def mt_k16_fail(verdict):
        def f(r):
            r['MT']['per_case']['C4T-KLO'].update(M_T_accepted=0.3, flags=[M.FLAG_TSU])
            r['MT']['verdict'] = verdict
        return f
    check('A50_S2_MT_VERDICT_PASS_WITH_A_FAILING_RUN_NO_RUN', run_eval(out, 's2_pass', mutate=mt_k16_fail('PASS'), skip_mt=True), 'NO_RUN',
          ids=('A50.S2',), extra=lambda e: 'MT_VERDICT_PASS_WITH_A_FAILING_RUN' in e['gates']['MT']['codes'])
    check('A50_S2_MT_FAIL_FOR_A_RUN_IS_ITS_FLAG_FLAG_PENDING_RULING', run_eval(out, 's2_flag', mutate=mt_k16_fail('FAIL'), skip_mt=True),
          'FLAG_PENDING_RULING', ids=('A50.S2',), extra=lambda e: e['gates']['MT']['status'] == 'FAIL'
          and e['flags']['TAIL_SOURCE_UNDERCONVERGED_from_MT_verdict_FAIL'] == ['C4T-KLO'] and e['validity']['C4T-KLO']['uvt']['flagged'] is False)
    check('A50_S2_MT_FAIL_FLAG_MAKES_THE_FAILING_T3_UNDECIDABLE_UTA',
          run_eval(out, 's2_uta', R=base_runs(**{'C4T-KLO': lambda R: make_run('C4T-KLO', shift(R['C4T']['adapted']['rows'], 0.3))}),
                   mutate=mt_k16_fail('FAIL'), skip_mt=True), 'UNDECIDABLE_ROUTE_A_TAIL', ids=('A50.S2',),
          extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['status'] == 'UNDECIDABLE_FLAGGED')
    check('A50_S2_MT_FAIL_CONSISTENT_WITH_THE_TAIL_FLAG_FULL_CROSSCHECK', run_eval(out, 's2_cons', R=base_runs(**{'C4T-KLO': remake('C4T-KLO', flagged=True)})),
          'FLAG_PENDING_RULING', ids=('A50.S2',), extra=lambda e: e['gates']['MT']['status'] == 'FAIL' and 'VERDICT:MT:FAIL' in e['gates']['MT']['codes'])
    # ---- N1: stage-name allow-list
    fr = make_run('C5H', dict(C4))
    fr['result'].update(status='FAILED_AT_STAGE', valid=False, stage_records=[{'name': 'v41_2345678', 'kind': 'x', 'exit_code': 1}])
    fr['adapted'].update(status='FAILED_AT_STAGE', valid=False)
    fr['failure'] = M.classify_failure(fr, CTX)
    bt = json.dumps(M.blinded_case(M.case_validity('C5H', fr, dict(CTX, case_block=CB), None, None, None)))
    t('A50_N1_STAGE_NAME_NOT_ON_THE_ALLOW_LIST_IS_REDACTED', fr['failure']['failed_stages'] == [M.STAGE_OTHER] and '2345678' not in bt
      and 'FAILED:%s' % M.STAGE_OTHER in bt, ids=('A50.N1', 'recheck N1'), sample=bt[:300])
    t('A50_N1_ALLOW_LIST_HOLDS_THE_DRIVER_CONSTANTS_ONLY', all(x in M.STAGE_NAMES for x in ('body', 'offset', 'reference', 'route_a',
      'route_a_tail_manifest', 'fs_columns_05', 'rfs_columns_01', 'le4_column_mean', 'le12_feedback', 'le3_columns'))
      and not any(x in M.STAGE_NAMES for x in ('le13_rotation', 'fs_columns_100', 'v41_2345678', 'route_a_ngc43', 'fs_column_00')), ids=('A50.N1',))
    root = out / 'disk'
    dn1 = write_run_dir(root, 'C5H_STAGE_CANARY', {'schema': M.RESULT_SCHEMA, 'status': 'FAILED_AT_STAGE', 'valid': False,
                                                   'driver_sha256': M.DRIVER_V009_EXT, 'call_spec_sha256': '9' * 64, 'passes': [],
                                                   'reasons': ['stage(s) exited nonzero'],
                                                   'stage_records': [{'name': 'v41_2345678', 'kind': 'columns_v001', 'exit_code': 1}]})
    mpn1 = out / 'MANIFEST_N1.json'
    mpn1.write_text(json.dumps(dict(man, cases=dict(man['cases'], C5H=str(dn1)))))
    p = cli('VALIDITY_ONLY_N1_STAGE_CANARY', '--validity-only', '--case', 'C5H', manifest=mpn1)
    txt = (out / 'VALIDITY_ONLY_N1_STAGE_CANARY' / 'VALIDITY_ONLY.json').read_text() if p.returncode == 0 else ''
    t('A50_N1_VALIDITY_ONLY_STAGE_CANARY_NOT_IN_OUTPUT_OR_STDOUT', p.returncode == 0 and '2345678' not in txt and '2345678' not in p.stdout
      and M.STAGE_OTHER in txt, ids=('A50.N1',), rc=p.returncode, stderr=p.stderr[-300:])

    # ---- N3 + A49 exact texts on disk: the RO1 label follows the record's ro1 block
    def ra_fail_run(name, message, rao=None):
        d = root / name
        sd = d / 'stages' / '04_route_a'
        (sd / 'attempt_000').mkdir(parents=True)
        (sd / 'attempt_000' / 'failure.json').write_text(json.dumps({'type': 'ValueError', 'message': message}))
        res = {'schema': M.RESULT_SCHEMA, 'status': 'FAILED_AT_STAGE', 'valid': False, 'driver_sha256': V010, 'call_spec_sha256': 'c' * 64,
               'passes': [], 'stage_records': [{'name': 'route_a', 'kind': 'route_a', 'exit_code': 1, 'stage_dir': str(sd)}]}
        if rao is not None:
            res['route_a_outcome'] = rao
        raw = json.dumps(res).encode()

        (d / 'result.json').write_bytes(raw)
        return M.read_run('C6T', str(d), dict(CTX, case_block=CB), True)
    r_no = ra_fail_run('C6T_RO1_NOBLOCK', M.READOUT_REFUSALS[0])
    r_arm = ra_fail_run('C6T_RO1_ARMED', M.READOUT_REFUSALS[0], rao={'ro1': ro1b(armed=True)})
    t('A50_N3_RO1_LABEL_FOLLOWS_THE_RECORD_NOT_THE_REGISTRATION', r_no['failure']['class'] == 'ROUTE_A_READOUT_REFUSAL_NO_RO1'
      and r_arm['failure']['class'] == 'ROUTE_A_READOUT_REFUSAL_UNDER_RO1', ids=('A50.N3', 'recheck N3'),
      got=[r_no['failure']['class'], r_arm['failure']['class']])
    r_deg = ra_fail_run('C6T_DEGENERATE_FULL', 'DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed')
    r_tok = ra_fail_run('C6T_DEGENERATE_TOKEN', 'DEGENERATE_RADIAL_EULER')
    t('A50_A49_EXACT_TEXTS_IN_THE_FAILURE_READING', r_deg['failure']['class'] == 'ROUTE_A_READOUT_REFUSAL_NO_RO1'
      and r_tok['failure']['class'] == 'ROUTE_A_STAGE_FAILED', ids=('A50.A49_EXACT_TEXTS', 'A49.1'),
      got=[r_deg['failure']['class'], r_tok['failure']['class']])
    # ---- N4: an R-PAIR member's V2 uses its registered bound (Picard 0.0025)
    RPn4 = rp_clean('T3_KLO', 'PICARD', Rk16, **{'C4T-KLO': {'dlast': 0.004}})
    check('A50_N4_PICARD_MEMBER_V2_USES_ITS_0p0025_BOUND', run_eval(out, 'n4', R=Rk16, RP=RPn4), 'INCOMPLETE', ids=('A50.N4', 'recheck N4 P6'),
          extra=lambda e: e['rpair_validity']['C4T-KLO@RPAIR:T3_KLO']['V2'] is False and e['tests']['T3']['pairs']['T3_KLO']['status'] == 'INCOMPLETE')
    RPn4b = rp_clean('T3_KLO', 'PICARD', Rk16, **{'C4T-KLO': {'dlast': 0.002}, 'C4T': {'dlast': 0.002}})
    ev = run_eval(out, 'n4ok', R=Rk16, RP=RPn4b)
    t('A50_N4_PICARD_MEMBER_WITHIN_0p0025_PASSES_V2', ev['rpair_validity']['C4T-KLO@RPAIR:T3_KLO']['V2'] is True, ids=('A50.N4',))
    # ---- AMB-20 restated: the diff of 60b46130 against 09ff5a96 is limited to /label and fs_absolute_overrides
    adm = CTX['c5h_admission']
    t('A50_AMB20_RESTATED_THREE_GROUNDS_TRUE_ON_BYTES', adm['admitted'] and
      adm['checks']['C5H_spec_differs_from_reviewed_09ff5a96_only_at_label_and_fs_absolute_overrides'] and adm['spec_diff_leaf_count_outside_allowed'] == 0,
      ids=('A50.AMB20', 'A50.root2'))
    rv = json.loads(Path(M.PIN_C5R3_SPEC_REVIEWED[0]).read_bytes())
    rv['numerics']['brackets']['rule']['rfs_factors'] = [0.8, 1.3]
    pr = out / 'REVIEWED_SPEC_WITH_AN_RFS_FACTOR_CHANGE.json'
    pr.write_text(json.dumps(rv))
    saved_pin = M.PIN_C5R3_SPEC_REVIEWED
    try:
        M.PIN_C5R3_SPEC_REVIEWED = (str(pr), hashlib.sha256(pr.read_bytes()).hexdigest())
        adm2 = M.c5h_admission_bases()
    finally:
        M.PIN_C5R3_SPEC_REVIEWED = saved_pin
    t('A50_AMB20_A_BRACKET_DIFF_OUTSIDE_FS_ABSOLUTE_OVERRIDES_IS_NOT_ADMITTED', adm2['admitted'] is False
      and 'C5H_spec_differs_from_reviewed_09ff5a96_only_at_label_and_fs_absolute_overrides' in adm2['failed']
      and adm2['spec_diff_leaves_outside_allowed'] == ['/numerics/brackets/rule/rfs_factors'], ids=('A50.AMB20',), failed=adm2['failed'])
    # ---- FINAL OUTCOME ORDER (A50) and PROVISIONAL marking (root items 3, 6)
    Rfl = base_runs(**{'C6T': remake('C6T', **slow)})
    RPfl = rp_clean('T1_H', 'PICARD', Rfl, **{'C4T': slow, 'C6T': slow})
    Rfl_k64 = base_runs(**{'C6T': remake('C6T', **slow), 'C4T-KHI': lambda R: make_run('C4T-KHI', shift(R['C4T']['adapted']['rows'], 0.3))})
    check('A50_ORDER_DECIDED_KBIG_AHEAD_OF_UAIF_BOTH_LISTED', run_eval(out, 'ord_kbig_uaif', R=Rfl_k64, RP=rp_clean('T1_H', 'PICARD', Rfl_k64, **{'C4T': slow, 'C6T': slow})),
          'KBIG_NOT_CONVERGED', ids=('A50.ORDER', 'recheck N2'),
          extra=lambda e: e['decision']['undecidable_readings'] == ['UNDECIDABLE_AT_ITERATION_FLOOR'] and e['decision']['a50_group'] == 2)
    check('A50_ORDER_UAIF_ALONE_IS_GROUP_4', run_eval(out, 'ord_uaif', R=Rfl, RP=RPfl), 'UNDECIDABLE_AT_ITERATION_FLOOR', ids=('A50.ORDER',),
          extra=lambda e: e['decision']['a50_group'] == 4 and e['decision']['position'] == M.outcome_position('UNDECIDABLE_AT_ITERATION_FLOOR'))
    Rfl_uta = base_runs(**{'C6T': remake('C6T', **slow),
                           'C4T-KLO': lambda R: make_run('C4T-KLO', shift(R['C4T']['adapted']['rows'], 0.3), flagged=True)})
    check('A50_ORDER_UTA_AHEAD_OF_UAIF_BOTH_LISTED', run_eval(out, 'ord_uta_uaif', R=Rfl_uta, RP=rp_clean('T1_H', 'PICARD', Rfl_uta, **{'C4T': slow, 'C6T': slow})),
          'UNDECIDABLE_ROUTE_A_TAIL', ids=('A50.ORDER', 'A50.root6', 'recheck N2'),
          extra=lambda e: e['decision']['undecidable_readings'] == ['UNDECIDABLE_ROUTE_A_TAIL', 'UNDECIDABLE_AT_ITERATION_FLOOR']
          and e['decision']['also_named'] == ['UNDECIDABLE_AT_ITERATION_FLOOR'] and e['decision']['a50_group'] == 3
          and isinstance(e['decision']['next_step'], dict))
    check('A50_PROVISIONAL_KBIG_WHILE_T2_PENDING', run_eval(out, 'prov_kbig_t2', R=base_runs(**{
        'C4T-KHI': lambda R: make_run('C4T-KHI', shift(R['C4T']['adapted']['rows'], 0.3)), 'C4T-D5': remake('C4T-D5', **slow)})),
        'KBIG_NOT_CONVERGED', ids=('A50.PROVISIONAL', 'A50.root3'),
        extra=lambda e: e['decision']['provisional'] is True and e['decision']['marking'] == 'PROVISIONAL'
        and any(x.startswith('T2 (could read IMPLEMENTATION_DEFECT)') for x in e['decision']['provisional_on']))
    check('A50_PROVISIONAL_NOT_MARKED_WHEN_THE_PENDING_STEP_SITS_LATER_ID_T2_WITH_T3_PENDING',
          run_eval(out, 'prov_id_t3', R=base_runs(**{'C4T-D5': lambda R: make_run('C4T-D5', shift(R['C5H']['adapted']['rows'], 0.3)),
                                                      'C4T-KHI': remake('C4T-KHI', **slow)})),
          'IMPLEMENTATION_DEFECT', ids=('A50.PROVISIONAL',),
          extra=lambda e: e['decision']['provisional'] is False and any('T3_KHI' in x for x in e['decision']['pending_steps']))
    check('A50_PROVISIONAL_SHAPE_WHILE_T1H_PENDING', run_eval(out, 'prov_shape', R=base_runs(**{
        'S4T': lambda R: make_run('S4T', shift(R['C4T']['adapted']['rows'], 2.5)), 'C6T': remake('C6T', **slow)})),
        'SHAPE_DISAGREEMENT', ids=('A50.PROVISIONAL', 'A50.root3'),
        extra=lambda e: e['decision']['provisional'] is True and any(x.startswith('T1_H') for x in e['decision']['provisional_on']))
    check('A50_PROVISIONAL_UTA_WHILE_T3_KHI_PENDING', run_eval(out, 'prov_uta', R=base_runs(**{
        'C4T-KLO': lambda R: make_run('C4T-KLO', shift(R['C4T']['adapted']['rows'], 0.3), flagged=True), 'C4T-KHI': remake('C4T-KHI', **slow)})),
        'UNDECIDABLE_ROUTE_A_TAIL', ids=('A50.PROVISIONAL',),
        extra=lambda e: e['decision']['provisional'] is True and any(x.startswith('T3_KHI') for x in e['decision']['provisional_on']))
    check('A50_PROVISIONAL_KBIG_WITH_A_FLAGGED_UNDECIDABLE_T2_DECLARED', run_eval(out, 'prov_flagt2', R=base_runs(**{
        'C4T-D5': lambda R: make_run('C4T-D5', shift(R['C5H']['adapted']['rows'], 0.3), flagged=True),
        'C4T-KHI': lambda R: make_run('C4T-KHI', shift(R['C4T']['adapted']['rows'], 0.3))})),
        'KBIG_NOT_CONVERGED', ids=('A50.PROVISIONAL', 'NEW-1'),
        extra=lambda e: e['decision']['provisional'] is True and 'UNDECIDABLE_ROUTE_A_TAIL' in e['decision']['undecidable_readings']
        and any('UNDECIDABLE_FLAGGED' in x for x in e['decision']['provisional_on']))
    ev = run_eval(out, 'ord_adopt')
    t('A50_ORDER_POSITIONS_AND_GROUPS', ev['decision']['outcome'] == 'ADOPT_TAIL' and ev['decision']['position'] == 16 and ev['decision']['a50_group'] == 6
      and M.OUTCOME_ORDER[3:12] == M.DECIDED_FAILURES and M.outcome_position('NON_LAPSE_TAIL_MATERIAL') == 3
      and [M.A50_GROUP[o] for o in ('NO_RUN', 'SHAPE_DISAGREEMENT', 'UNDECIDABLE_ROUTE_A_TAIL', 'UNDECIDABLE_AT_ITERATION_FLOOR',
                                    'FLAG_PENDING_RULING', 'ADOPT_TAIL')] == [1, 2, 3, 4, 5, 6] and ev['decision']['provisional'] is False,
      ids=('A50.ORDER',))
    # ---- root items agreed (each re-read on its own scenario)
    check('A50_ROOT1_E_UNAVAILABLE_BRANCH_PICARD', run_eval(out, 'r1', R=base_runs(**{'C6T': remake('C6T', npass=1)})), 'INCOMPLETE', ids=('A50.root1',),
          extra=lambda e: e['tests']['T1_H']['rpair_branch'] == 'PICARD' and 'A50 root item 1' in e['tests']['T1_H']['rpair_branch_basis'])
    e1 = run_eval(out, 'r4a', R=base_runs(**{'C6T': make_run('C6T', {}, present=False)}))
    e2 = run_eval(out, 'r4b', R=Rf)
    t('A50_ROOT4_INCOMPLETE_SUBTYPES', e1['decision']['subtype'] == 'CASES_OR_RECORDS' and e1['decision']['tests_read'] is False
      and e2['decision']['subtype'] == 'UNRESOLVED' and e2['decision']['tests_read'] is True, ids=('A50.root4',))
    check('A50_ROOT5_NOT_UV_SPLIT_ON_A_FLAG_UNRESOLVED', run_eval(out, 'r5', R=base_runs(d23=big23, d34=big34, **{'C6T': remake('C6T', flagged=True)})),
          'INCOMPLETE', ids=('A50.root5',), extra=lambda e: e['decision']['subtype'] == 'UNRESOLVED')
    check('A50_ROOT7_SRB_ROT_FAIL_ON_FLAGGED_C4T_UNDECIDABLE', run_eval(out, 'r7', R=base_runs(**{'C4T': remake('C4T', flagged=True)}), mutate=srb_fail),
          'UNDECIDABLE_ROUTE_A_TAIL', ids=('A50.root7',))
    check('A50_ROOT8_GQ_COVERAGE_SHORTFALL_NUMERICS_UNCERTIFIED', run_eval(out, 'r8', mutate=gq_lower), 'NUMERICS_UNCERTIFIED', ids=('A50.root8',))
    e1 = run_eval(out, 'r9a', mutate=eps_two)
    e2 = run_eval(out, 'r9b', mutate=rbfp_zero)
    t('A50_ROOT9_EPS_TWO_REFINEMENTS_UNCERTIFIED_AND_KAPPA_UNDEFINED_INCOMPLETE', e1['decision']['outcome'] == 'NUMERICS_UNCERTIFIED'
      and e2['decision']['outcome'] == 'INCOMPLETE' and e2['tests']['RB_FP']['status'] == 'INCOMPLETE', ids=('A50.root9',))
    check('A50_ROOT10_PICARD_MEMBER_INHERITS_THE_BASE_FLAG_AND_ITS_CLEARING',
          run_eval(out, 'r10', R=Rfk, RP=RPfk, rulings=[ruling(M.FLAG_TSU, 'C4T-KLO', 'CLEARED', R=Rfk)]), 'ADOPT_TAIL', ids=('A50.root10',))
    Rnp13 = base_runs(**{lab: remake(lab, probe=False) for lab in M.T_CASES})

    def ea13(cases):
        def f(r):
            for lab in cases:
                r['EA']['per_case'][lab] = {'result_sha256': Rnp13[lab]['result_sha256'], 'E_A_rows_km_s': [0.005 * TAU[i] for i in IDS],
                                            'accepted_iteration': 6, 'row_radii_m': list(RADII)}
        return f
    six = ('C4T', 'C6T', 'C4T-D5', 'C4T-KLO', 'C4T-KHI')
    check('A50_ROOT13_NO_PROBE_R_EA_RECORD_COVERING_THE_SIX_CASES_SUFFICES', run_eval(out, 'r13', R=Rnp13, mutate=ea13(six)), 'ADOPT_TAIL',
          ids=('A50.root13',), extra=lambda e: all(e['validity'][c]['uvt']['E_A_row_order'] == 'UNVERIFIED_NO_PROBE_R' for c in M.T_CASES))
    check('A50_ROOT13_EA_RECORD_MISSING_ONE_OF_THE_SIX_INCOMPLETE', run_eval(out, 'r13b', R=Rnp13, mutate=ea13(six[:-1])), 'INCOMPLETE',
          ids=('A50.root13',), extra=lambda e: e['tests']['T3']['pairs']['T3_KHI']['status'] == 'INCOMPLETE')
    # ---- RO1 custody list (root items 11, 12) on T-cases
    check('A50_RO1_WORKER_NOT_ON_THE_CUSTODY_LIST_INVALID', run_eval(out, 'cust_w', R=base_runs(**{'C4T': remake('C4T', ro1=dict(ro1b(), worker_sha256='7' * 64))})),
          'INCOMPLETE', ids=('A50.root11', 'A50.root12'), extra=lambda e: 'RO1_WORKER_NOT_ON_CUSTODY_LIST' in e['validity']['C4T']['V3_mismatch'])
    check('A50_RO1_BINDING_NOT_ON_THE_CUSTODY_LIST_INVALID', run_eval(out, 'cust_b', R=base_runs(**{'C4T': remake('C4T', ro1=dict(ro1b(), binding_sha256='7' * 64))})),
          'INCOMPLETE', ids=('A50.root11',), extra=lambda e: 'RO1_BINDING_NOT_ON_CUSTODY_LIST' in e['validity']['C4T']['V3_mismatch'])
    check('A50_RO1_SERIAL_WORKER_ON_A_PARALLEL8_CASE_INVALID', run_eval(out, 'cust_k', R=base_runs(**{'C4T': remake('C4T', ro1=ro1b(cw=1))})),
          'INCOMPLETE', ids=('A50.root11',),
          extra=lambda e: 'RO1_WORKER_IS_NOT_THE_PARALLEL_CUSTODY_WORKER_FOR_THE_COLUMN_WORKERS' in e['validity']['C4T']['V3_mismatch'])

    def c5h_pins(R):
        r = make_run('C5H', R['C5H']['adapted']['rows'])
        r['route_a_outcome']['ro1'] = dict(ro1b(armed=False), worker_sha256=WORKER_PARALLEL)
        return r
    check('A50_RO1_UNARMED_RECORD_NAMING_PINS_INVALID', run_eval(out, 'cust_u', R=base_runs(**{'C5H': c5h_pins})), 'INCOMPLETE',
          ids=('A50.root11',), extra=lambda e: 'RO1_PINS_ON_AN_UNARMED_RECORD' in e['validity']['C5H']['V3_mismatch'])
    r3_tests(out, root, man, cli, c5h_res, slow, rp_clean, big23, srk_kdep, ruling)
    r4_tests(out, root, man, cli, slow, rp_clean)
    r5_tests(out, root, man, cli, slow, rp_clean)
    r6_tests(out, root, man, cli, slow, rp_clean)
    r7_tests(out, root, man, cli, slow, rp_clean)
    r8_tests(out, root, man, cli, slow, rp_clean)
    # ================================================================ summary
    n_pass = sum(1 for x in TESTS if x['pass'])
    summary = {'schema': 'UNT_V007_COMPARE_TESTS_C2V005', 'script_sha256': hashlib.sha256(CMP.read_bytes()).hexdigest(),
               'tests_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'n': len(TESTS), 'n_pass': n_pass,
               'n_fail': len(TESTS) - n_pass, 'tests': TESTS}
    (out / 'TEST_SUMMARY.json').write_text(json.dumps(summary, indent=1))
    for x in TESTS:
        print('%s %s %s' % ('PASS' if x['pass'] else 'FAIL', x['test'], '' if x['pass'] else json.dumps(x)[:700]))
    print('%d/%d pass' % (n_pass, len(TESTS)))
    return 0 if n_pass == len(TESTS) else 1


def with_passes(run, plist):
    """A run whose Picard pass rows are plist (the last = its final rows); V2's field = max_i |d_last_i| (verify D9)."""
    r = copy.deepcopy(run)
    r['pass_rows'] = [dict(p) for p in plist]
    r['adapted']['rows'] = dict(plist[-1])
    r['adapted']['last_change_km_s'] = max(abs(plist[-1][i] - plist[-2][i]) for i in IDS) if len(plist) > 1 else 0.0
    return r


def passes_by_increments(final, incs):
    """Pass rows ending at final whose successive increments (oldest first) are incs[k][i] km/s."""
    rows = [dict(final)]
    for d in reversed(incs):
        rows.insert(0, {i: rows[0][i] - d[i] for i in IDS})
    return rows


def r1_per_row_E(pr):
    """R1's per-row formula (superseded by A51 F2), for the A51 contrast test only."""
    E = {}
    for i in IDS:
        dl, dp = pr[-1][i] - pr[-2][i], pr[-2][i] - pr[-3][i]
        q = 0.9 if dp == 0 else min(0.9, abs(dl) / abs(dp))
        E[i] = 0.0 if dl == 0 else abs(dl) * q / (1 - q)
    return E


def r3_tests(out, root, man, cli, c5h_res, slow, rp_clean, big23, srk_kdep, ruling):
    """[R3] one test (or more) per A51 F2 item and per fixed R2-recheck finding (ids 'A51.*' / 'R3.*' in 'covers')."""
    # ================================================================ A51 F2: the tau-norm a-posteriori Picard bound
    z = {i: 0.0 for i in IDS}
    incs0 = [{i: 0.2 * TAU[i] for i in IDS}, dict(z, **{IDS[0]: 0.05 * TAU[IDS[0]]}), dict(z, **{IDS[2]: 0.004 * TAU[IDS[2]]})]
    r = with_passes(make_run('C6T', C4), passes_by_increments(C4, incs0))      # R6 [A56 N1]: row 03 has d_prev 0 < d_last (q_i inf)
    E, c, det = M.picard_noise_detail(r, IDS, TAU)
    t('A56_N1_R3_WORLD_ROW_WITH_ZERO_PREVIOUS_INCREMENT_E_UNAVAILABLE', E is None and c == M.E_UNAVAILABLE_ROW_RATIO
      and det.get('rows_with_ratio_ge_1') == [IDS[2]], ids=('A56.N1', 'R6'), code=c)
    # [R6 adapted, A56 N1 + A58 RI-18] the A51 F2 norm formula on uniform-shape increments (every row's q_i = the norm ratio < 1;
    # the same-sign per-row bound then equals the norm bound, so E = the norm bound exactly)
    incs = [{i: x * TAU[i] for i in IDS} for x in (0.2, 0.05, 0.004)]
    r = with_passes(make_run('C6T', C4), passes_by_increments(C4, incs))
    E, c, det = M.picard_noise_detail(r, IDS, TAU)
    want = {i: TAU[i] * 0.004 * (0.25 / 0.75) for i in IDS}
    t('A51_F2_E_IS_TAU_I_TIMES_NORM_LAST_TIMES_Q_OVER_1_MINUS_Q_Q_LARGEST_OF_LAST_TWO_RATIOS', c is None
      and all(abs(E[i] - want[i]) < 1e-12 for i in IDS) and abs(det['q'] - 0.25) < 1e-12 and det['contraction_observed'] is True,
      ids=('A51.F2',), q=det.get('q'))
    r = with_passes(make_run('C6T', C4), passes_by_increments(C4, incs[1:]))
    E, c, det = M.picard_noise_detail(r, IDS, TAU)
    t('A51_F2_ONLY_ONE_RATIO_USES_THAT_RATIO', c is None and abs(det['q'] - 0.08) < 1e-12
      and all(abs(E[i] - TAU[i] * 0.004 * 0.08 / 0.92) < 1e-12 for i in IDS), ids=('A51.F2',))
    r = with_passes(make_run('C6T', C4), passes_by_increments(C4, [{i: 0.01 * TAU[i] for i in IDS}, {i: 0.02 * TAU[i] for i in IDS}]))
    E, c, det = M.picard_noise_detail(r, IDS, TAU)
    t('A51_F2_NON_CONTRACTING_RATIO_2_E_UNAVAILABLE_A53_NEW7', E is None and c == M.E_UNAVAILABLE_NONCONTRACTING   # [R5 adapted]
      and det['contraction_observed'] is False, ids=('A51.F2', 'A53.NEW-7'), code=c)
    r = with_passes(make_run('C6T', C4), passes_by_increments(C4, [z, {i: 0.01 * TAU[i] for i in IDS}]))
    E, c, det = M.picard_noise_detail(r, IDS, TAU)
    t('A51_F2_ZERO_PREVIOUS_NORM_RATIO_INFINITE_E_UNAVAILABLE_A53_NEW7', E is None and c == M.E_UNAVAILABLE_NONCONTRACTING,  # [R5 adapted]
      ids=('A51.F2', 'A53.NEW-7'), code=c)
    r = with_passes(make_run('C6T', C4), [dict(C4)])
    t('A51_F2_NO_INCREMENT_E_UNAVAILABLE_AMB05', M.picard_noise(r, IDS, TAU) == (None, M.E_UNAVAILABLE), ids=('A51.F2', 'AMB-05'))
    got = {}
    for k in ('C2R3', 'C3R3', 'C4R3'):
        pr = M._pass_rows(json.loads(Path(M.PIN_R3[k][0]).read_bytes()))
        E, c, det = M.picard_noise_detail({'pass_rows': pr, 'adapted': REAL[k]}, IDS, TAU)
        got[k] = (c, None if E is None else round(max(E[i] / (TAU[i] / 8) for i in IDS), 2),
                  [round(x, 3) for x in det['tau_norm_ratios_used']], det.get('rows_with_ratio_ge_1'))
    # [R6 adapted, A56 N1 + A58 RI-18] TESTED on the real R3 bytes: C2R3 rows 03/04/05 (q_i 1.06, 8.2, 1.9) and C3R3 row 10 (q_i 1.31)
    # do not contract while the tau norm does (ratios 0.141; 0.095, 0.206): E unavailable; C4R3 keeps the A54 value 0.24
    t('A51_F2_REAL_R3_HISTORIES_UNDER_A56_N1_AND_RI18', got == {
        'C2R3': (M.E_UNAVAILABLE_ROW_RATIO, None, [0.141], ['DDO154_SPARC12_03', 'DDO154_SPARC12_04', 'DDO154_SPARC12_05']),
        'C3R3': (M.E_UNAVAILABLE_ROW_RATIO, None, [0.095, 0.206], ['DDO154_SPARC12_10']),
        'C4R3': (None, 0.24, [0.023], None)}, ids=('A51.F2', 'A54.S7', 'A56.N1', 'A58.RI-18'), got=got)
    # a row whose increment changes sign while the norm contracts strongly: R1 read it undecidable, A51 reads it decidable.
    # [R6 adapted, A56 N1] that world's row 06 has q_i = 1e-3 / 1e-5 = 100 >= 1: E is now unavailable (-> R-PAIR, PICARD)
    sc = [dict({i: 0.1 * TAU[i] for i in IDS}, **{IDS[5]: -1e-5}), dict(z, **{IDS[5]: 1e-3})]   # ratio 0.02/0.1 = 0.2

    def c6_sign(R):
        rr = make_run('C6T', R['C6T']['adapted']['rows'])
        return with_passes(rr, passes_by_increments(rr['adapted']['rows'], sc))
    Rsc = base_runs(**{'C6T': c6_sign})
    E1 = r1_per_row_E(Rsc['C6T']['pass_rows'])
    r1_undecidable = E1[IDS[5]] > TAU[IDS[5]] / 8
    check('A51_F2_SIGN_CHANGING_ROW_WITH_ROW_RATIO_100_E_UNAVAILABLE_A56_N1', run_eval(out, 'a51_sign', R=Rsc), 'INCOMPLETE',
          ids=('A51.F2', 'A56.N1'), extra=lambda e: r1_undecidable and e['tests']['T1_H']['status'] == 'RPAIR_PENDING'
          and M.E_UNAVAILABLE_ROW_RATIO in e['tests']['T1_H']['noise']['reason'])
    # the same idea with an alternating row that contracts (q_i 0.5): the A56 N1 alternating bound keeps it decidable (ADOPT)
    sc2 = [dict({i: 0.1 * TAU[i] for i in IDS}, **{IDS[5]: -0.01 * TAU[IDS[5]]}), dict(z, **{IDS[5]: 0.005 * TAU[IDS[5]]})]

    def c6_alt(R):
        rr = make_run('C6T', R['C6T']['adapted']['rows'])
        return with_passes(rr, passes_by_increments(rr['adapted']['rows'], sc2))
    Ralt = base_runs(**{'C6T': c6_alt})
    check('A51_F2_A56_N1_ALTERNATING_CONTRACTING_ROW_DECIDABLE_ADOPT', run_eval(out, 'a51_alt', R=Ralt), 'ADOPT_TAIL', ids=('A51.F2', 'A56.N1'),
          extra=lambda e: e['tests']['T1_H']['noise']['decidable'] is True and e['tests']['T1_H']['source'] == 'base'
          and e['tests']['T1_H']['noise']['picard_bound']['C6T']['per_row_bound_kind'].get(IDS[5]) == 'ALTERNATING')
    # ================================================================ R3 order F1: AMB-17 in the T1-fail split, SR_K unavailable
    m15 = {i: 1.5 * TAU[i] for i in IDS}

    def srk_not_replayed(r):                 # [R5 adapted, A54 S5: 'NOT_REPLAYED' is not a registered verdict -> RECORD_DEFECT;
        r['SR_K']['verdict'] = 'FAIL'        # SR_K is unavailable through its registered failing verdict]

    def c5c_over(k):
        return lambda R: make_run('C4T-C5c', shift(R['C4T-D5']['adapted']['rows'], k))
    check('R3_ORDER_F1_SRKD_DECIDED_BY_T2c_WHILE_SR_K_UNAVAILABLE', run_eval(out, 'f1_srkd', R=base_runs(d23=big23, d34=m15, **{'C4T-C5c': c5c_over(0.3)}),
                                                                               mutate=srk_not_replayed),
          'SOURCE_REPRESENTATION_K_DEPENDENT', ids=('R3.order.F1', 'AMB-17'),
          extra=lambda e: e['decision']['subtype'] == 'T2c' and e['tests']['SR_K']['status'] == 'INCOMPLETE' and e['gates']['SR_K']['status'] == 'FAIL'
          and e['tests']['T1']['status'] == 'FAIL' and not e['tests']['T1']['floor_like'])
    check('R3_ORDER_F1_CONTROL_T2c_WITHIN_QUARTER_TAU_STAYS_PENDING', run_eval(out, 'f1_ctrl', R=base_runs(d23=big23, d34=m15), mutate=srk_not_replayed),
          'INCOMPLETE', ids=('R3.order.F1',), extra=lambda e: e['decision']['subtype'] == 'UNRESOLVED'
          and any('SR_K unavailable' in x for x in e['decision']['pending_steps']))
    check('R3_ORDER_F1_PROBE_SHAPE_ALSO_FAILS_READS_SRKD_NOT_PROVISIONAL_SHAPE',
          run_eval(out, 'f1_shape', R=base_runs(d23=big23, d34=m15, **{'C4T-C5c': c5c_over(0.3),
                                                                        'S4T': lambda R: make_run('S4T', shift(R['C4T']['adapted']['rows'], 2.5))}),
                   mutate=srk_not_replayed),
          'SOURCE_REPRESENTATION_K_DEPENDENT', ids=('R3.order.F1',),
          extra=lambda e: 'SHAPE_DISAGREEMENT' in e['decision']['also_decided'] and e['decision']['provisional'] is False)
    check('R3_ORDER_F1_FLAGGED_T2c_WITH_SR_K_UNAVAILABLE_STAYS_PENDING_ROOT5',
          run_eval(out, 'f1_flag', R=base_runs(d23=big23, d34=m15, **{'C4T-C5c': lambda R: make_run('C4T-C5c', shift(R['C4T-D5']['adapted']['rows'], 0.3),
                                                                                                         flagged=True)}),
                   mutate=srk_not_replayed),
          'INCOMPLETE', ids=('R3.order.F1', 'A50.root5'), extra=lambda e: e['decision']['subtype'] == 'UNRESOLVED')
    # ================================================================ R3 validity F1: RO1 event fields num-or-null (c2v002 producer)
    def ev_(**kw):
        e = {'code': M.RO1_CODE, 'refusal': M.READOUT_REFUSALS[0], 'query': 3, 'phi_rad': 0.785, 'R_kpc': 1.48, 'numerator': -0.2,
             'denominator': 1.0, 'after_convergence': True}
        e.update(kw)
        return e
    k16 = lambda **kw: {'C4T-KLO': remake('C4T-KLO', ro1=ro1b(fired=True, events=[ev_(**kw)]))}
    check('R3_VALIDITY_F1_FIRED_EVENT_WITH_NULL_NUMERATOR_DENOMINATOR_IS_VALID_RECORDED',
          run_eval(out, 'vf1_null', R=base_runs(**k16(numerator=None, denominator=None))), 'ADOPT_TAIL', ids=('R3.validity.F1',),
          extra=lambda e: e['validity']['C4T-KLO']['valid_all'] and 'C4T-KLO' in e['ro1_recorded'])
    check('R3_VALIDITY_F1_FIRED_EVENT_WITH_EVERY_DOCUMENTED_NULL_IS_VALID',
          run_eval(out, 'vf1_allnull', R=base_runs(**k16(query=None, phi_rad=None, R_kpc=None, numerator=None, denominator=None))), 'ADOPT_TAIL',
          ids=('R3.validity.F1',))
    check('R3_VALIDITY_F1_NONFINITE_REPR_STRING_STILL_A_LOUD_TYPE_CODE', run_eval(out, 'vf1_inf', R=base_runs(**k16(numerator='inf'))), 'INCOMPLETE',
          ids=('R3.validity.F1',), extra=lambda e: any('FIELD_TYPE_num|null' in x and 'numerator' in x for x in e['validity']['C4T-KLO']['V3_mismatch']))

    def k16_missing(R):
        e = ev_()
        del e['denominator']
        return make_run('C4T-KLO', R['C4T-KLO']['adapted']['rows'], ro1=ro1b(fired=True, events=[e]))
    check('R3_VALIDITY_F1_ABSENT_FIELD_STILL_NAMED', run_eval(out, 'vf1_abs', R=base_runs(**{'C4T-KLO': k16_missing})), 'INCOMPLETE',
          ids=('R3.validity.F1',), extra=lambda e: any('FIELD_MISSING' in x and 'denominator' in x for x in e['validity']['C4T-KLO']['V3_mismatch']))
    check('R3_VALIDITY_F1_EXACT_TEXT_AND_AFTER_CONVERGENCE_STILL_CHECKED',
          run_eval(out, 'vf1_txt', R=base_runs(**k16(numerator=None, denominator=None, refusal='DEGENERATE_RADIAL_EULER', after_convergence=False))),
          'INCOMPLETE', ids=('R3.validity.F1', 'A49.1'),
          extra=lambda e: {'RO1_EVENT_REFUSAL', 'RO1_EVENT_BEFORE_CONVERGENCE'} <= set(e['validity']['C4T-KLO']['V3_mismatch']))
    # ================================================================ R3 validity F2: the C5H interlock on every run path
    dspec = root / 'C5H_SPEC_STANDIN'                         # start.json carries call_spec 60b46130 (written by the B4 test)
    dname = root / 'interlock' / FORBIDDEN
    slots = {'cases_C4T-D5': dict(man, cases=dict(man['cases'], **{'C4T-D5': str(dspec)})),
             'rpair_T2_C5H': dict(man, rpair={'T2': {'branch': 'PICARD', 'members': {'C5H': str(dspec), 'C4T-D5': str(dspec) + '_X'}}}),
             'identity_runs_Z2': dict(man, identity_runs={'Z2': str(dspec)}),
             'identity_runs_Z2_by_name': dict(man, identity_runs={'Z2': str(dname)}),
             'rpair_T3_KLO_C4T_by_name': dict(man, rpair={'T3_KLO': {'branch': 'PICARD', 'members': {'C4T': str(dname), 'C4T-KLO': str(dspec) + '_Y'}}})}
    res = {}
    for nm, mf in slots.items():
        mpth = out / ('MANIFEST_F2_%s.json' % nm)
        mpth.write_text(json.dumps(mf))
        err = io.StringIO()
        _e, sys.stderr = sys.stderr, err
        try:
            with OpenTrace() as tr, _quiet():
                rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mpth), '--case-block', str(out / 'CASE_BLOCK_PROBE.json'),
                             '--outdir', str(out / ('F2_%s' % nm)), '--test-allow-unpinned-prereg', *REGARGS])
        finally:
            sys.stderr = _e
        opened = [x for x in tr.paths if x.endswith('/result.json') and ('C5H_SPEC_STANDIN' in x or FORBIDDEN in x)]
        res[nm] = (rc, 'registered C5H' in err.getvalue() or '60b46130' in err.getvalue(), opened, (out / ('F2_%s' % nm)).exists())
    t('R3_VALIDITY_F2_FULL_MODE_REFUSES_THE_REGISTERED_C5H_IN_EVERY_MANIFEST_SLOT',
      all(v[0] == 2 and v[1] and not v[2] and not v[3] for v in res.values()), ids=('R3.validity.F2', 'blinding B4'), res=res)
    t('R3_VALIDITY_F2_MANIFEST_RUN_PATHS_COVER_CASES_IDENTITY_AND_RPAIR_MEMBERS',
      [s for s, _ in M.manifest_run_paths({'cases': {'C4T': 'a'}, 'identity_runs': {'Z2': 'b'}, 'rpair': {'T2': {'members': {'C5H': 'c', 'C4T-D5': 'd'}}}})]
      == ['cases:C4T', 'identity_runs:Z2', 'rpair:T2:C4T-D5', 'rpair:T2:C5H'], ids=('R3.validity.F2',))
    # ================================================================ R3 validity F3: --gates-only identity runs carry the RO1 codes
    zres = synthetic_completed_result(dict(C2), {'route_a': {'column_workers': 1}}, drv='5' * 64, spec='6' * 64)
    zres['route_a_outcome']['ro1'] = ro1b(armed=False, cw=1)
    dz = write_run_dir(root / 'f3', 'Z2_UNARMED', zres)
    mz = out / 'MANIFEST_F3.json'
    mz.write_text(json.dumps(dict(man, identity_runs={'Z2': str(dz)})))
    p = cli('F3_GATES_ONLY_Z2_UNARMED', '--gates-only', manifest=mz)
    body = json.loads((out / 'F3_GATES_ONLY_Z2_UNARMED' / 'GATES_ONLY.json').read_text()) if p.returncode == 0 else {}
    z2 = (body.get('identity_runs') or {}).get('Z2') or {}
    t('R3_VALIDITY_F3_GATES_ONLY_UNARMED_IDENTITY_RUN_INVALID_WITH_RO1_NOT_ARMED', p.returncode == 0 and z2.get('valid') is False
      and 'RO1_NOT_ARMED' in z2.get('codes', []), ids=('R3.validity.F3', 'A50.root12'), z2=z2, stderr=p.stderr[-300:])
    iv = M.identity_run_validity('Z2', identity_run('Z2', armed=False), CTX)
    t('R3_VALIDITY_F3_IDENTITY_VALID_FLAG_INCLUDES_THE_RO1_CODES', iv['valid'] is False and 'RO1_NOT_ARMED' in iv['ro1_codes'], ids=('R3.validity.F3',))
    # ================================================================ R3 validity F4: bounded identifiers, registered numerics paths
    sd = root / 'f4' / 'stage_fs'
    (sd / 'columns').mkdir(parents=True)
    (sd / 'columns' / 'finish.json').write_text(json.dumps({'failures': [{'index': 4123, 'message': 'MASS_ENTHALPY_NOT_BRACKETED: a'},
                                                                         {'index': 5, 'message': 'MASS_ENTHALPY_NOT_BRACKETED: b'}]}))
    fr = {'result': {'status': 'COMPLETED_INVALID', 'stage_records': [{'name': 'fs_columns', 'kind': 'columns_v001', 'exit_code': 0, 'stage_dir': str(sd)}],
                     'passes': [{'pass': 4123, 'column_failures': [{'message': 'MASS_ENTHALPY_NOT_BRACKETED: c'}]},
                                {'pass': 6, 'column_failures': [{'message': 'MASS_ENTHALPY_NOT_BRACKETED: d'}]}]},
          'receipt': {}, 'spec_for_reading': {}}
    fc = M.classify_failure(fr, CTX)
    t('R3_VALIDITY_F4_COLUMN_INDEX_AND_PASS_NUMBER_BOUNDED_BY_REGISTERED_CONSTANTS',
      fc['misses'] == ['fs_columns:col?:MASS_ENTHALPY_NOT_BRACKETED', 'fs_columns:col0005:MASS_ENTHALPY_NOT_BRACKETED',
                       'pass?:MASS_ENTHALPY_NOT_BRACKETED', 'pass6:MASS_ENTHALPY_NOT_BRACKETED'] and '4123' not in json.dumps(fc),
      ids=('R3.validity.F4',), misses=fc['misses'])
    ctx4 = dict(CTX, case_block=CB)
    code = M.diff_paths_code(['/route_a/column_workers=8', '/k41_2345678=1', '/uv_tail/outer/K_big_inverse_kpc=32.0'], ctx4)
    t('R3_VALIDITY_F4_DIFF_PATHS_ONLY_REGISTERED_KEYS_EMITTED', code == '/route_a/column_workers;/uv_tail/outer/K_big_inverse_kpc;' + M.NUMERICS_PATH_OTHER
      and '2345678' not in code, ids=('R3.validity.F4',), code=code)
    n5 = numerics_for(M.C5H)
    n5['k41_2345678'] = 1
    ev4 = run_eval(out, 'vf4', R=base_runs(**{'C5H': remake('C5H', numerics=n5)}))
    d5c = [x for x in ev4['validity']['C4T-D5']['V3_mismatch'] if x.startswith('numerics_not_byte_equal_to_C5H')]
    t('R3_VALIDITY_F4_RECORD_KEY_NOT_IN_A_D5_V3_CODE', d5c == ['numerics_not_byte_equal_to_C5H:' + M.NUMERICS_PATH_OTHER]
      and '2345678' not in json.dumps(M.blinded_case(ev4['validity']['C4T-D5'])), ids=('R3.validity.F4', 'blinding'), codes=d5c)
    # ================================================================ R3 order N2 / N8
    Rk16 = base_runs(**{'C4T-KLO': remake('C4T-KLO', **slow)})
    RPn2 = rp_clean('T3_KLO', 'PICARD', Rk16, **{'C4T-KLO': {'dlast': 0.004}})
    check('R3_ORDER_N2_INVALID_RPAIR_MEMBER_NEXT_STEP_NAMED_IN_THE_READING', run_eval(out, 'n2', R=Rk16, RP=RPn2), 'INCOMPLETE', ids=('R3.order.N2',),
          extra=lambda e: e['decision']['subtype'] == 'UNRESOLVED'
          and 'V2' in e['decision']['rpair_member_next_steps']['C4T-KLO@RPAIR:T3_KLO'])
    check('R3_ORDER_N8_IDENTITY_RUN_SERIAL_WORKER_WITH_COLUMN_WORKERS_8_INVALID',
          run_eval(out, 'n8', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS}, 'Z2': identity_run('Z2', cw=8)}), 'INCOMPLETE',
          ids=('R3.order.N8', 'NEW-4'), extra=lambda e: 'RO1_WORKER_IS_NOT_THE_PARALLEL_CUSTODY_WORKER_FOR_THE_COLUMN_WORKERS' in e['identity_runs']['Z2']['ro1_codes'])
    check('R3_ORDER_N8_IDENTITY_RUN_COLUMN_WORKERS_UNREADABLE_INVALID',
          run_eval(out, 'n8b', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS}, 'Z2-OFF': identity_run('Z2-OFF', cw=None)}), 'INCOMPLETE',
          ids=('R3.order.N8',), extra=lambda e: 'RO1_KIND_CHECK_COLUMN_WORKERS_UNREADABLE' in e['identity_runs']['Z2-OFF']['ro1_codes'])
    check('R3_ORDER_N8_IDENTITY_RUN_MATCHING_KIND_ADOPT', run_eval(out, 'n8ok'), 'ADOPT_TAIL', ids=('R3.order.N8',),
          extra=lambda e: all(e['identity_runs'][n]['valid'] for n in M.IDENTITY_RUNS))
    # ---- NEW-12, ruled by A52.3 (R4 adapted): the C5H R-PAIR member spec carries numerics.route_a.ro1_workers true; the leaf is
    # required on the C5H member and excluded from its base and partner equalities; without it the member is invalid
    Rra = base_runs(**{'C4T-D5': remake('C4T-D5', ea=0.2)})
    RPra = rp_clean('T2', 'ROUTE_A', Rra)
    RPra_no = rp_clean('T2', 'ROUTE_A', Rra, **{'C5H': {'num_over': lambda n: n['route_a'].pop('ro1_workers')}})
    e_no = run_eval(out, 'new12_no', R=Rra, RP=RPra_no, b0_c5h=True)
    check('R3_OBS_NEW12_C5H_MEMBER_CARRYING_ROUTE_A_RO1_WORKERS_VALID_A52_3_AND_REQUIRED', run_eval(out, 'new12', R=Rra, RP=RPra, b0_c5h=True),
          'ADOPT_TAIL', ids=('NEW-12', 'A50.B1', 'A50.root11', 'A52.3'),
          extra=lambda e: e['rpair_validity']['C5H@RPAIR:T2']['valid_all'] and e['rpair_validity']['C4T-D5@RPAIR:T2']['valid_all']
          and e['tests']['T2']['source'] == 'RPAIR' and e_no['decision']['outcome'] == 'INCOMPLETE'
          and 'C5H_RPAIR_MEMBER_LACKS_ROUTE_A_RO1_WORKERS_TRUE_A52_3' in e_no['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch'])
    idr_noroute = identity_run('Z2')                  # [R4 adapted: on Z2, since B0prime_RERUN is unarmed by A52.1]
    idr_noroute['result']['normalized_spec'] = {'numerics': {'picard': {'passes': 6}}}      # route_a absent: the driver default 1
    iv = M.identity_run_validity('Z2', idr_noroute, CTX)
    idr_noroute8 = identity_run('Z2')
    idr_noroute8['result']['normalized_spec'] = {'numerics': {}}
    idr_noroute8['route_a_outcome']['ro1'] = ro1b(cw=8)
    iv8 = M.identity_run_validity('Z2', idr_noroute8, CTX)
    t('R3_ORDER_N8_ROUTE_A_ABSENT_IS_COLUMN_WORKERS_1_THE_V010_L837_DEFAULT_ON_Z2_A52_1', iv['valid'] is True and iv8['valid'] is False
      and 'RO1_WORKER_IS_NOT_THE_SERIAL_CUSTODY_WORKER_FOR_THE_COLUMN_WORKERS' in iv8['ro1_codes'], ids=('R3.order.N8',), codes=iv8['ro1_codes'])


def r4_tests(out, root, man, cli, slow, rp_clean):
    """[R4] one test (or more) per fixed R3-recheck finding (ids 'R4.*' in 'covers'), plus the observations carried to root."""
    # ================================================================ R4 validity F1: the nodes_v001 RO1 workers (scoped custody)
    drv4 = Path(M.PIN_DRIVER_V010_R5[0]).read_text()               # [R7 renamed, A62.3] the pins are the v010 r5 NODES_ROUTE_A
    t('R4_VALIDITY_F1_NODES_CUSTODY_PINS_FROM_BYTES_EQUAL_V010_R5_NODES_ROUTE_A',
      all(M.sha256_file(p) == s_ for p, s_ in M.PIN_RO1_NODES_CUSTODY.values())
      and all("'%s'" % s_ in drv4 for _, s_ in M.PIN_RO1_NODES_CUSTODY.values()) and 'NODES_ROUTE_A = {' in drv4,
      ids=('R4.validity.F1', 'A50.root11'))
    sv = M.PIN_RO1_NODES_CUSTODY
    M.PIN_RO1_NODES_CUSTODY = dict(sv, worker=(sv['worker'][0], '0' * 64))
    try:
        M.build_context()
        refused = False
    except M.Refused:
        refused = True
    finally:
        M.PIN_RO1_NODES_CUSTODY = sv
    t('R4_VALIDITY_F1_NODES_CUSTODY_PIN_MISMATCH_REFUSED_AT_START', refused, ids=('R4.validity.F1',))
    check('R4_VALIDITY_F1_D5_ARMED_ON_THE_NODES_PARALLEL_WORKER_VALID_ADOPT', run_eval(out, 'r4f1_ok'), 'ADOPT_TAIL', ids=('R4.validity.F1', 'A50.root11'),
          extra=lambda e: e['validity']['C4T-D5']['valid_all'] and e['validity']['C4T-D5']['ro1']['custody_list'] == 'NODES'
          and e['validity']['C4T']['ro1']['custody_list'] == 'CONTINUUM')
    check('R4_VALIDITY_F1_D5_ON_A_CONTINUUM_WORKER_INVALID', run_eval(out, 'r4f1_cont', R=base_runs(**{'C4T-D5': remake('C4T-D5', ro1=ro1b(cw=8))})),
          'INCOMPLETE', ids=('R4.validity.F1',),
          extra=lambda e: 'RO1_CONTINUUM_WORKER_ON_A_NODES_V001_CASE' in e['validity']['C4T-D5']['V3_mismatch']
          and e['decision']['subtype'] == 'CASES_OR_RECORDS')
    check('R4_VALIDITY_F1_NODES_WORKER_ON_A_CONTINUUM_CASE_INVALID', run_eval(out, 'r4f1_rev', R=base_runs(**{'C4T': remake('C4T', ro1=ro1b(cw=8, nodes=True))})),
          'INCOMPLETE', ids=('R4.validity.F1',), extra=lambda e: 'RO1_NODES_V001_WORKER_ON_A_NON_NODES_CASE' in e['validity']['C4T']['V3_mismatch'])
    check('R4_VALIDITY_F1_D5_NODES_SERIAL_WORKER_ON_PARALLEL8_INVALID', run_eval(out, 'r4f1_kind', R=base_runs(**{'C4T-D5': remake('C4T-D5', ro1=ro1b(cw=1, nodes=True))})),
          'INCOMPLETE', ids=('R4.validity.F1', 'NEW-4'),
          extra=lambda e: 'RO1_WORKER_IS_NOT_THE_PARALLEL_CUSTODY_WORKER_FOR_THE_COLUMN_WORKERS' in e['validity']['C4T-D5']['V3_mismatch'])
    Rd5 = base_runs(**{'C4T-D5': remake('C4T-D5', ea=0.2)})
    RPd5 = rp_clean('T2', 'ROUTE_A', Rd5)
    check('R4_VALIDITY_F1_D5_RPAIR_MEMBER_ON_THE_NODES_WORKER_VALID', run_eval(out, 'r4f1_rp', R=Rd5, RP=RPd5, b0_c5h=True), 'ADOPT_TAIL',
          ids=('R4.validity.F1', 'A50.B1'), extra=lambda e: e['rpair_validity']['C4T-D5@RPAIR:T2']['valid_all']
          and e['rpair_validity']['C4T-D5@RPAIR:T2']['ro1']['custody_list'] == 'NODES' and e['tests']['T2']['source'] == 'RPAIR')
    RPd5c = rp_clean('T2', 'ROUTE_A', Rd5, **{'C4T-D5': {'ro1': ro1b(cw=8)}})
    check('R4_VALIDITY_F1_D5_RPAIR_MEMBER_ON_A_CONTINUUM_WORKER_INVALID', run_eval(out, 'r4f1_rpc', R=Rd5, RP=RPd5c, b0_c5h=True), 'INCOMPLETE',
          ids=('R4.validity.F1',), extra=lambda e: 'RO1_CONTINUUM_WORKER_ON_A_NODES_V001_CASE' in e['rpair_validity']['C4T-D5@RPAIR:T2']['V3_mismatch']
          and e['tests']['T2']['status'] == 'INCOMPLETE')
    ivn = M.identity_run_validity('Z2', identity_run('Z2', ro1_over={'worker_sha256': NODES_SERIAL}), CTX)
    t('R4_VALIDITY_F1_IDENTITY_RUN_ON_A_NODES_WORKER_INVALID', ivn['valid'] is False and 'RO1_NODES_V001_WORKER_ON_A_NON_NODES_CASE' in ivn['ro1_codes'],
      ids=('R4.validity.F1', 'A50.root12'), codes=ivn['ro1_codes'])
    reg_d5 = CB['cases']['C4T-D5']
    t('R4_VALIDITY_F1_SCOPE_IS_THE_REGISTERED_SOURCE_RULE', M.registered_source_rule_is_nodes(reg_d5)
      and not any(M.registered_source_rule_is_nodes(CB['cases'][c]) for c in M.REGISTERED if c != 'C4T-D5')
      and not M.registered_source_rule_is_nodes(dict(reg_d5, tail=False)), ids=('R4.validity.F1',))
    # ================================================================ R4 validity F2, ruled by A52.1: B0prime_RERUN exempt from item 12
    check('R4_A52_1_B0PRIME_RERUN_UNARMED_NOT_FIRED_VALID_ADOPT', run_eval(out, 'a521_ok'), 'ADOPT_TAIL', ids=('R4.validity.F2', 'A52.1'),
          extra=lambda e: e['identity_runs']['B0prime_RERUN']['valid'] and e['identity_runs']['B0prime_RERUN']['ro1_armed'] is False
          and e['identity_runs']['B0prime_RERUN']['ro1_item12'] == M.B0PRIME_RERUN_RO1_RULE)
    check('R4_A52_1_B0PRIME_RERUN_ARMED_INVALID', run_eval(out, 'a521_arm', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS},
                                                                          'B0prime_RERUN': identity_run('B0prime_RERUN', armed=True)}),
          'INCOMPLETE', ids=('R4.validity.F2', 'A52.1'),
          extra=lambda e: 'RO1_B0PRIME_RERUN_MUST_BE_UNARMED_A52_1' in e['identity_runs']['B0prime_RERUN']['ro1_codes'])
    noblk = identity_run('B0prime_RERUN')
    del noblk['route_a_outcome']['ro1']
    check('R4_A52_1_B0PRIME_RERUN_WITHOUT_AN_RO1_BLOCK_INVALID_NAMED', run_eval(out, 'a521_nob', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS},
                                                                                               'B0prime_RERUN': noblk}),
          'INCOMPLETE', ids=('R4.validity.F2', 'A52.1'),
          extra=lambda e: any('FIELD_MISSING' in c and 'ro1' in c for c in e['identity_runs']['B0prime_RERUN']['ro1_codes']))
    fu = identity_run('B0prime_RERUN')
    fu['route_a_outcome']['ro1']['fired'] = True
    ivf = M.identity_run_validity('B0prime_RERUN', fu, CTX)
    ivz = M.identity_run_validity('Z2-OFF', identity_run('Z2-OFF', armed=False), CTX)
    t('R4_A52_1_FIRED_UNARMED_B0PRIME_INVALID_AND_Z2_OFF_STILL_ARMED_REQUIRED', ivf['valid'] is False and 'RO1_FIRED_WITHOUT_ARMED' in ivf['ro1_codes']
      and ivz['valid'] is False and 'RO1_NOT_ARMED' in ivz['ro1_codes'], ids=('R4.validity.F2', 'A52.1', 'A50.root12'), f=ivf['ro1_codes'], z=ivz['ro1_codes'])
    # ================================================================ A52.3: C5H R-PAIR member specs (ro1_workers, own B0 record)
    Rra = base_runs(**{'C4T-D5': remake('C4T-D5', ea=0.2)})
    Rt2p = base_runs(**{'C4T-D5': remake('C4T-D5', **slow)})
    RPp2 = rp_clean('T2', 'PICARD', Rt2p)
    check('R4_A52_3_C5H_PICARD_MEMBER_WITH_RO1_WORKERS_AND_ITS_B0_RECORD_VALID', run_eval(out, 'a523_ok', R=Rt2p, RP=RPp2, b0_c5h=True), 'ADOPT_TAIL',
          ids=('A52.3', 'A50.root11'), extra=lambda e: all(v['valid_all'] for v in e['rpair_validity'].values())
          and e['tests']['T2']['source'] == 'RPAIR')

    def drop_member_b0(r):
        r['B0']['spec_sets']['EXT'] = [x for x in r['B0']['spec_sets']['EXT'] if '@RPAIR' not in x['label']]
    check('R4_A52_3_C5H_MEMBER_SPEC_WITHOUT_ITS_B0_RECORD_INVALID', run_eval(out, 'a523_b0', R=Rt2p, RP=RPp2, b0_c5h=True, mutate=drop_member_b0),
          'INCOMPLETE', ids=('A52.3',),
          extra=lambda e: 'C5H_RPAIR_MEMBER_SPEC_HAS_NO_B0_RECORD_AGAINST_V009_EXT_A52_3' in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch'])
    RPd5w = rp_clean('T2', 'ROUTE_A', Rra, **{'C4T-D5': {'num_over': lambda n: n['route_a'].update(ro1_workers=True)}})
    check('R4_A52_3_RO1_WORKERS_LEAF_ON_THE_D5_MEMBER_INVALID', run_eval(out, 'a523_d5', R=Rra, RP=RPd5w, b0_c5h=True), 'INCOMPLETE', ids=('A52.3',),
          extra=lambda e: any('RPAIR_MEMBER_NUMERICS_DIFFER_FROM_BASE_OUTSIDE_RPAIR_LEAVES' in x for x in e['rpair_validity']['C4T-D5@RPAIR:T2']['V3_mismatch']))
    # OBSERVED for root (NEW-18): A49.4 says RO1 workers change checkpoint identity, and a C5H Picard member with ro1_workers must
    # compute route A (r4 L1406), so its route-A identity cannot equal the v009-EXT base's; V6 (kept) then reads it invalid
    RPp2i = rp_clean('T2', 'PICARD', Rt2p, **{'C5H': {'ra_ident': sha('recomputed C5H route A under RO1 workers')}})
    check('R4_OBS_NEW18_C5H_PICARD_MEMBER_WITH_RECOMPUTED_ROUTE_A_IDENTITY_FAILS_V6_STRICTER', run_eval(out, 'new18', R=Rt2p, RP=RPp2i, b0_c5h=True),
          'INCOMPLETE', ids=('NEW-18', 'A52.3', 'A49.4', 'V6'), extra=lambda e: e['rpair_validity']['C5H@RPAIR:T2']['V6'] is False)
    # ================================================================ A52.5: SRB_ROT read only with the successor EPS envelope bound
    def no_env(r):
        del r['EPS']['envelope_bound']
    e5 = run_eval(out, 'a525_noenv', mutate=no_env)
    check('R4_A52_5_NO_ENVELOPE_BOUND_SRB_ROT_NOT_READ_NO_ADOPT', e5, 'INCOMPLETE', ids=('A52.5',),
          extra=lambda e: e['tests']['SRB_ROT']['status'] == 'NOT_READ' and e['decision']['subtype'] == 'UNRESOLVED'
          and e['gates']['EPS']['status'] == 'PASS' and any('SRB_ROT' in str(x) for x in e['decision']['pending_steps']))

    def srb_fail_noenv(r):
        del r['EPS']['envelope_bound']
        r['SRB_ROT']['srb_rot_km_s'] = [0.5 * TAU[i] for i in IDS]
    check('R4_A52_5_SRB_ROT_FAIL_WITHOUT_ENVELOPE_IS_NOT_BOUND_INSUFFICIENT', run_eval(out, 'a525_fail', mutate=srb_fail_noenv), 'INCOMPLETE',
          ids=('A52.5',), extra=lambda e: e['tests']['SRB_ROT']['status'] == 'NOT_READ' and e['tests']['SRB_ROT']['gate_status'] == 'FAIL')

    def env_short(r):                        # [R6 adapted, A55: sqrt(2) x 2P = 362.04 at P = 128 (R5: 90.51 at P = 32)]
        r['EPS']['envelope_bound']['coverage_max_inverse_kpc'] = 362.0
    def env_rule(r):
        r['EPS']['envelope_bound']['rule'] = 'PER_SHELL_SAMPLED'
    def env_ok(r):
        r['EPS']['envelope_bound']['coverage_max_inverse_kpc'] = 362.1
    es, er, eo = run_eval(out, 'a525_short', mutate=env_short), run_eval(out, 'a525_rule', mutate=env_rule), run_eval(out, 'a525_okb', mutate=env_ok)
    t('R4_A52_5_ENVELOPE_COVERAGE_BELOW_SQRT2_2P_OR_OTHER_RULE_NOT_READ_AT_BOUND_READ_A54',
      es['tests']['SRB_ROT']['status'] == 'NOT_READ' and er['tests']['SRB_ROT']['status'] == 'NOT_READ'
      and eo['tests']['SRB_ROT']['status'] == 'PASS' and eo['decision']['outcome'] == 'ADOPT_TAIL', ids=('A52.5',),
      reasons=[es['tests']['SRB_ROT'].get('reason'), er['tests']['SRB_ROT'].get('reason')])

    def env_bad(r):
        del r['EPS']['envelope_bound']['coverage_max_inverse_kpc']
    eb = run_eval(out, 'a525_bad', mutate=env_bad)
    t('R4_A52_5_ENVELOPE_BLOCK_PRESENT_BUT_MALFORMED_IS_A_LOUD_EPS_DEFECT', eb['gates']['EPS']['status'] == 'RECORD_DEFECT'
      and any('envelope_bound/coverage_max_inverse_kpc' in c for c in eb['gates']['EPS']['codes']) and eb['decision']['outcome'] == 'NO_RUN',
      ids=('A52.5', 'E-SEAL1'), codes=eb['gates']['EPS']['codes'])
    check('R4_A52_5_LATER_DECIDED_FAILURE_PROVISIONAL_BEHIND_UNREAD_SRB_ROT',
          run_eval(out, 'a525_prov', R=base_runs(**{'S4T': lambda R: make_run('S4T', shift(R['C4T']['adapted']['rows'], 2.5))}), mutate=no_env),
          'SHAPE_DISAGREEMENT', ids=('A52.5', 'A50.PROVISIONAL'),
          extra=lambda e: e['decision']['provisional'] is True and 'SRB_ROT' in str(e['decision']['provisional_on']))
    # ================================================================ R4 validity F5: interlock case-insensitive + same-file
    low = root / 'f5' / FORBIDDEN.lower()
    low.mkdir(parents=True)
    with OpenTrace() as tr:
        w_low = M.c5h_interlock(str(low))
        w_mix = M.c5h_interlock(str(root / 'f5' / FORBIDDEN.swapcase()))
    t('R4_VALIDITY_F5_LOWER_AND_SWAPPED_CASE_NAME_REFUSED_WITH_NO_FILE_OPENED', bool(w_low) and bool(w_mix) and not tr.paths,
      ids=('R4.validity.F5', 'blinding B4'), opened=tr.paths)
    stand = write_run_dir(root / 'f5', 'REG_STANDIN', {'status': 'x'})          # a stand-in for the registered directory
    alias = root / 'f5' / 'ALIAS_OF_STANDIN'
    alias.symlink_to(stand.resolve(), target_is_directory=True)      # absolute target (a relative one is resolved from f5/)
    sv_dirs = M.C5H_REGISTERED_RUN_DIRS
    M.C5H_REGISTERED_RUN_DIRS = (str(stand),)
    try:
        with OpenTrace() as tr2:
            w_alias = M.c5h_interlock(str(alias))
            w_other = M.c5h_interlock(str(root / 'f5' / 'C4T_badfinish_NOT_THERE'))
        mpa = out / 'MANIFEST_F5_ALIAS.json'
        mpa.write_text(json.dumps(dict(man, identity_runs={'Z2': str(alias)})))
        err = io.StringIO()
        _e, sys.stderr = sys.stderr, err
        try:
            with OpenTrace() as tr3, _quiet():
                rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mpa), '--case-block', str(out / 'CASE_BLOCK_PROBE.json'),
                             '--outdir', str(out / 'F5_ALIAS'), '--test-allow-unpinned-prereg', *REGARGS])
        finally:
            sys.stderr = _e
    finally:
        M.C5H_REGISTERED_RUN_DIRS = sv_dirs
    opened = [x for x in tr2.paths + tr3.paths if 'REG_STANDIN' in x or 'ALIAS_OF_STANDIN' in x]
    t('R4_VALIDITY_F5_SAME_DIRECTORY_UNDER_ANOTHER_NAME_REFUSED_BY_STAT_IDENTITY',
      bool(w_alias) and ('another name' in w_alias or 'inside the registered' in w_alias) and w_other is None and rc == 2
      and ('another name' in err.getvalue() or 'inside the registered' in err.getvalue())         # [R5: A53 F2 realpath refuses first]
      and not opened and not (out / 'F5_ALIAS').exists(), ids=('R4.validity.F5', 'R3.validity.F2'), opened=opened, rc=rc)
    t('R4_VALIDITY_F5_REGISTERED_DIRS_ARE_THE_ONE_REGISTERED_NAME', all(Path(d).name == FORBIDDEN for d in M.C5H_REGISTERED_RUN_DIRS),
      ids=('R4.validity.F5',))
    # ================================================================ R4 order N-c: a ROUTE_A member carries its own route-A identity
    Rk = base_runs(**{'C4T-KLO': remake('C4T-KLO', ea=0.2)})
    RPnc = rp_clean('T3_KLO', 'ROUTE_A', Rk, **{'C4T-KLO': {'ra_ident': 'e' * 64}})     # = the base runs' identity
    check('R4_ORDER_Nc_ROUTE_A_MEMBER_ADMITTING_THE_BASE_ROUTE_A_IDENTITY_INVALID', run_eval(out, 'r4nc', R=Rk, RP=RPnc), 'INCOMPLETE',
          ids=('R4.order.N-c',), extra=lambda e: 'RPAIR_ROUTE_A_MEMBER_ADMITS_THE_BASE_ROUTE_A_IDENTITY_NOT_RECOMPUTED'
          in e['rpair_validity']['C4T-KLO@RPAIR:T3_KLO']['V3_mismatch'] and e['rpair_validity']['C4T@RPAIR:T3_KLO']['valid_all']
          and e['tests']['T3']['pairs']['T3_KLO']['status'] == 'INCOMPLETE')
    RPnc2 = rp_clean('T3_KLO', 'ROUTE_A', Rk, **{'C4T': {'ra_ident': None}})
    check('R4_ORDER_Nc_ROUTE_A_MEMBER_WITHOUT_A_ROUTE_A_IDENTITY_INVALID', run_eval(out, 'r4nc2', R=Rk, RP=RPnc2), 'INCOMPLETE',
          ids=('R4.order.N-c',), extra=lambda e: 'RPAIR_ROUTE_A_MEMBER_ROUTE_A_IDENTITY_NOT_A_SHA' in e['rpair_validity']['C4T@RPAIR:T3_KLO']['V3_mismatch'])
    check('R4_ORDER_Nc_CONTROL_RECOMPUTED_IDENTITIES_ADOPT', run_eval(out, 'r4nc3', R=Rk, RP=rp_clean('T3_KLO', 'ROUTE_A', Rk)), 'ADOPT_TAIL',
          ids=('R4.order.N-c',), extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['source'] == 'RPAIR')
    RPp = rp_clean('T3_KLO', 'PICARD', base_runs(**{'C4T-KLO': remake('C4T-KLO', **slow)}))
    check('R4_ORDER_Nc_PICARD_MEMBER_STILL_NEEDS_THE_BASE_IDENTITY_V6', run_eval(out, 'r4nc4', R=base_runs(**{'C4T-KLO': remake('C4T-KLO', **slow)}),
                                                                             RP=RPp), 'ADOPT_TAIL',
          ids=('R4.order.N-c', 'V6'), extra=lambda e: e['rpair_validity']['C4T-KLO@RPAIR:T3_KLO']['V6'] is True)
    # ================================================================ R4 order F1 (kept stricter; observation for root, NEW-15)
    # v010 r4 L1404-1405 refuses route_a.column_workers > 1 with admit.route_a, so the only Picard member r4 normalizes while
    # admitting its base's route A carries route_a.column_workers 1; the compare reads it invalid (V3 column_workers != 8 and the
    # member-vs-base leaf diff): the PICARD branch cannot resolve for any of the four pairs until root rules.
    res = {}
    for pid in M.RPAIR_IDS:
        noisy = {'T1_H': 'C6T', 'T2': 'C4T-D5', 'T3_KLO': 'C4T-KLO', 'T3_KHI': 'C4T-KHI'}[pid]
        Rp = base_runs(**{noisy: remake(noisy, **slow)})
        RPq = rp_clean(pid, 'PICARD', Rp, **{m: {'num_over': lambda n: n.setdefault('route_a', {}).update(column_workers=1)} for m in M.PAIRS[pid]})
        e = run_eval(out, 'r4of1_%s' % pid, R=Rp, RP=RPq, b0_c5h=True)
        tst = e['tests']['T3']['pairs'][pid] if pid.startswith('T3') else e['tests'][pid]
        mv = [e['rpair_validity']['%s@RPAIR:%s' % (m, pid)] for m in M.PAIRS[pid]]
        res[pid] = (e['decision']['outcome'], tst['status'], all(not v['valid_all'] for v in mv),
                    all(any('RPAIR_MEMBER_NUMERICS_DIFFER_FROM_BASE_OUTSIDE_RPAIR_LEAVES' in x for x in v['V3_mismatch']) for v in mv))
    t('R4_ORDER_F1_PICARD_MEMBERS_ADMITTING_ROUTE_A_AT_COLUMN_WORKERS_1_VALID_AND_RESOLVE_ON_EVERY_PAIR_A53',     # [R5 adapted:
      all(r == ('ADOPT_TAIL', 'PASS', False, False) for r in res.values()),                                     # A53 rules NEW-15]
      ids=('R4.order.F1', 'NEW-15', 'A53', 'A50.root1'), res=res)
    # ================================================================ R4 order N-a: the A50-tag counts of R2 and R3, from bytes
    def a50_count(p):
        return sum(1 for x in json.loads(Path(p).read_text())['tests'] if any(str(c).startswith('A50.') for c in x.get('covers', [])))
    n2 = a50_count(HERE.parent / 'r2' / 'out' / 'tests_R2' / 'TEST_SUMMARY.json')
    n3 = a50_count(HERE.parent / 'r3' / 'out' / 'tests_R3_v2' / 'TEST_SUMMARY.json')
    n4 = sum(1 for x in TESTS if any(str(c).startswith('A50.') for c in x.get('covers', [])))
    t('R4_ORDER_Na_A50_TAG_COUNTS_FROM_BYTES_R2_61_R3_64', n2 == 61 and n3 == 64 and n4 >= 64, ids=('R4.order.N-a',), r2=n2, r3=n3, r4_so_far=n4)


def set_hist(run, norms, signs=None, shape=None):
    """[Claude3 H2 set_hist, rebuilt] replace a run's Picard pass rows by a history ENDING at its final rows whose increments
    are norms[k] * tau_i * shape_i (signs[k] per increment); V2's field follows the last increment."""
    final = dict(run['adapted']['rows'])
    shp = {i: 1.0 for i in IDS} if shape is None else dict(zip(IDS, shape))
    incs = [{i: (1.0 if signs is None else signs[k]) * x * TAU[i] * shp[i] for i in IDS} for k, x in enumerate(norms)]
    rows = passes_by_increments(final, incs)
    rows[-1] = final
    run['pass_rows'] = rows
    run['adapted']['last_change_km_s'] = max(abs(rows[-1][i] - rows[-2][i]) for i in IDS)
    return run


def driver_passes(rows_list, gap_at=None, index=None):
    """A driver-layout passes[] list (pass k+1, rows, field max_abs_change); gap_at: that pass written with rows []."""
    out_ = []
    for k, p in enumerate(rows_list):
        out_.append({'pass': (index[k] if index else k + 1),
                     'rows': [] if k == gap_at else [{'id': i, 'speed_km_s': p[i]} for i in IDS],
                     'max_abs_change_km_s': max(abs(p[i] - rows_list[k - 1][i]) for i in IDS) if k else 1.0})
    return out_


def with_gap(run, gap_at=1, index=None):
    """[A54 B4] give a fixture run a driver passes[] record with a pass-row gap, read exactly as read_run reads it."""
    full = list(run['pass_rows'])
    ps = driver_passes(full, gap_at=gap_at, index=index)
    run['result']['passes'] = ps
    run['pass_rows'] = M._pass_rows({'passes': ps})
    run['pass_rows_gap'] = M.pass_rows_gap({'passes': ps})
    return run


def r5_tests(out, root, man, cli, slow, rp_clean):
    """[R5] one test (or more) per A53 / A54 ruling, per Claude3 0053 finding (B1-B4, S1-S8, with its probe worlds rebuilt as
    regression tests where feasible) and per r4-recheck finding (ids 'A53.*', 'A54.*', 'C3.*', 'R5.*' in 'covers')."""
    def ptest(e, pid):
        return e['tests']['T3']['pairs'][pid] if pid.startswith('T3') else e['tests'][pid]
    NOISY = {'T1_H': 'C6T', 'T2': 'C4T-D5', 'T3_KLO': 'C4T-KLO', 'T3_KHI': 'C4T-KHI'}

    def world(pid, branch):
        return base_runs(**{NOISY[pid]: remake(NOISY[pid], **slow)} if branch == 'PICARD' else {NOISY[pid]: remake(NOISY[pid], ea=0.2)})
    # ================================================================ A53 (Claude3 R3 P0-P11; B3, S1, S2, S3)
    for pid in M.RPAIR_IDS:                                                       # P0 / S1: A53-shaped members resolve, both branches
        for br in ('PICARD', 'ROUTE_A'):
            Rw = world(pid, br)
            e = run_eval(out, 'r5p0_%s_%s' % (pid, br), R=Rw, RP=rp_clean(pid, br, Rw), b0_c5h=True)
            check('C3_R3_P0_A53_SHAPED_MEMBERS_RESOLVE_%s_%s' % (pid, br), e, 'ADOPT_TAIL', ids=('A53', 'C3.R3.P0', 'C3.S1'),
                  extra=lambda e, pid=pid, br=br: ptest(e, pid).get('source') == 'RPAIR' and all(v['valid_all'] for v in e['rpair_validity'].values())
                  and (br == 'ROUTE_A' or all(v['V6'] is True for v in e['rpair_validity'].values())))
    Rk = world('T3_KLO', 'PICARD')
    RP8 = rp_clean('T3_KLO', 'PICARD', Rk, **{m: {'num_over': lambda n: n['route_a'].update(column_workers=8)} for m in M.PAIRS['T3_KLO']})
    for m in M.PAIRS['T3_KLO']:                     # num_over runs before the A53 shape sets cw 1; set 8 after it (a computing member)
        RP8['T3_KLO']['_runs'][m]['result']['normalized_spec']['numerics']['route_a']['column_workers'] = 8
    check('A53_PICARD_MEMBER_NOT_AT_THE_COLUMN_WORKERS_1_LEAF_INVALID', run_eval(out, 'r5cw8', R=Rk, RP=RP8), 'INCOMPLETE', ids=('A53', 'C3.R3.P1'),
          extra=lambda e: any('route_a.column_workers!=1' in x for x in e['rpair_validity']['C4T@RPAIR:T3_KLO']['V3_mismatch']))

    def diff_rao(run, R):
        run['route_a_outcome']['result_sha256'] = 'd' * 64
    RPv6 = rp_clean('T3_KLO', 'PICARD', Rk, **{m: {'post': diff_rao} for m in M.PAIRS['T3_KLO']})
    check('C3_B3_R3_P2_PICARD_V6_RESULT_SHA256_NOT_THE_BASE_INVALID_NOT_ADOPT', run_eval(out, 'r5p2', R=Rk, RP=RPv6), 'INCOMPLETE',
          ids=('A53', 'C3.B3', 'C3.R3.P2'), extra=lambda e: e['rpair_validity']['C4T@RPAIR:T3_KLO']['V6'] is False
          and 'V6_ROUTE_A_OUTCOME_RESULT_SHA256_NOT_THE_BASE_A53' in e['rpair_validity']['C4T@RPAIR:T3_KLO']['V6_codes'])
    Rt2 = world('T2', 'PICARD')
    e = run_eval(out, 'r5p3', R=Rt2, RP=rp_clean('T2', 'PICARD', Rt2), b0_c5h=True)
    check('C3_S2_R3_P3_A53_C5H_PICARD_MEMBER_NO_RO1_WORKERS_UNARMED_VALID', e, 'ADOPT_TAIL', ids=('A53', 'C3.S2', 'C3.R3.P3'),
          extra=lambda e: e['rpair_validity']['C5H@RPAIR:T2']['valid_all'] and e['rpair_validity']['C5H@RPAIR:T2']['ro1']['armed'] is False
          and e['tests']['T2']['source'] == 'RPAIR')
    RPw = rp_clean('T2', 'PICARD', Rt2, **{'C5H': {'num_over': lambda n: n['route_a'].update(ro1_workers=True)}})
    for x in RPw['T2']['_runs'].values():           # num_over precedes the A53 shape (which drops the leaf): set it again after
        if x['label'].startswith('C5H'):
            x['result']['normalized_spec']['numerics']['route_a']['ro1_workers'] = True
    check('A53_C5H_PICARD_MEMBER_CARRYING_RO1_WORKERS_INVALID', run_eval(out, 'r5c5w', R=Rt2, RP=RPw, b0_c5h=True), 'INCOMPLETE', ids=('A53',),
          extra=lambda e: 'C5H_RPAIR_PICARD_MEMBER_CARRIES_ROUTE_A_RO1_WORKERS_A53' in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch'])
    RPa = rp_clean('T2', 'PICARD', Rt2, **{'C5H': {'ro1': ro1b(armed=True, cw=8)}})
    check('A53_C5H_PICARD_MEMBER_ARMED_INVALID', run_eval(out, 'r5c5a', R=Rt2, RP=RPa, b0_c5h=True), 'INCOMPLETE', ids=('A53',),
          extra=lambda e: 'RO1_C5H_PICARD_MEMBER_MUST_BE_UNARMED_AND_NOT_FIRED_A53' in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch'])

    def no_ro1_block(run, R):
        run['route_a_outcome'].pop('ro1', None)
    RPn = rp_clean('T2', 'PICARD', Rt2, **{'C5H': {'post': no_ro1_block}})
    check('A53_C5H_PICARD_MEMBER_WITHOUT_AN_RO1_BLOCK_FIELD_MISSING', run_eval(out, 'r5c5n', R=Rt2, RP=RPn, b0_c5h=True), 'INCOMPLETE',
          ids=('A53',), extra=lambda e: any('FIELD_MISSING' in x and 'ro1' in x for x in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch']))
    e = run_eval(out, 'r5p4', R=Rk, RP=rp_clean('T3_KLO', 'PICARD', Rk))
    check('C3_S3_R3_4_P4_T_CASE_PICARD_MEMBER_CARRIES_THE_BASE_PARALLEL_RO1_RECORD_VALID', e, 'ADOPT_TAIL', ids=('A53.R3-4', 'C3.S3', 'C3.R3.P4'),
          extra=lambda e: e['rpair_validity']['C4T@RPAIR:T3_KLO']['ro1'].get('worker_kind_from') == 'ADMITTED_BASE_ATTEMPT_A53_R3_4'
          and e['rpair_validity']['C4T@RPAIR:T3_KLO']['valid_all'])
    RPs = rp_clean('T3_KLO', 'PICARD', Rk, **{m: {'ro1': ro1b(cw=1)} for m in M.PAIRS['T3_KLO']})
    check('A53_R3_4_T_CASE_PICARD_MEMBER_WITH_ITS_OWN_SERIAL_RO1_RECORD_INVALID', run_eval(out, 'r5p4b', R=Rk, RP=RPs), 'INCOMPLETE',
          ids=('A53.R3-4',), extra=lambda e: 'RPAIR_PICARD_MEMBER_RO1_RECORD_NOT_THE_BASE_RECORD_A53_R3_4'
          in e['rpair_validity']['C4T@RPAIR:T3_KLO']['V3_mismatch'])
    Rra = world('T2', 'ROUTE_A')
    e = run_eval(out, 'r5ra', R=Rra, RP=rp_clean('T2', 'ROUTE_A', Rra), b0_c5h=True)
    check('A53_ROUTE_A_BRANCH_UNCHANGED_C5H_MEMBER_RO1_WORKERS_ARMED_OWN_IDENTITY_NEW16', e, 'ADOPT_TAIL', ids=('A53', 'NEW-16', 'A52.3'),
          extra=lambda e: e['rpair_validity']['C5H@RPAIR:T2']['ro1']['armed'] is True and e['tests']['T2']['source'] == 'RPAIR')

    def alias(run, R):
        b = R[run['label'].split('@')[0]]
        run['result_sha256'] = b['result_sha256']
        run['finish'] = {'result_sha256': b['result_sha256']}
        run['adapted']['result_sha256'] = b['result_sha256']
    check('C3_R3_P7_ALIAS_MEMBER_IS_THE_BASE_RESULT_INCOMPLETE', run_eval(out, 'r5p7', R=Rk, RP=rp_clean('T3_KLO', 'PICARD', Rk, **{'C4T': {'post': alias}})),
          'INCOMPLETE', ids=('C3.R3.P7',))
    check('C3_R3_P8_PICARD_LEAVES_NOT_EQUAL_BETWEEN_MEMBERS_INCOMPLETE',
          run_eval(out, 'r5p8', R=Rk, RP=rp_clean('T3_KLO', 'PICARD', Rk, **{'C4T': {'num_over': lambda n: n['picard'].update(passes=11)}})),
          'INCOMPLETE', ids=('C3.R3.P8',))
    check('C3_R3_P9_PICARD_MEMBER_WITH_SEED_FACTOR_INCOMPLETE',
          run_eval(out, 'r5p9', R=Rk, RP=rp_clean('T3_KLO', 'PICARD', Rk, **{'C4T': {'num_over': lambda n: n['route_a'].update(seed_source_rtol_factor=0.1)}})),
          'INCOMPLETE', ids=('C3.R3.P9',))
    Rkr = world('T3_KLO', 'ROUTE_A')
    check('C3_R3_P10_ROUTE_A_MEMBER_WITH_PICARD_PASSES_12_INCOMPLETE',
          run_eval(out, 'r5p10', R=Rkr, RP=rp_clean('T3_KLO', 'ROUTE_A', Rkr, **{'C4T': {'num_over': lambda n: n.update(picard=dict(M.RPAIR_PICARD))}})),
          'INCOMPLETE', ids=('C3.R3.P10',))
    check('C3_R3_P11_ROUTE_A_MEMBER_IDENTITY_EQUALS_BASE_INCOMPLETE_NEW16',
          run_eval(out, 'r5p11', R=Rkr, RP=rp_clean('T3_KLO', 'ROUTE_A', Rkr, **{'C4T': {'ra_ident': 'e' * 64}})), 'INCOMPLETE',
          ids=('C3.R3.P11', 'NEW-16'))
    RPmm = rp_clean('T3_KLO', 'PICARD', Rk)
    RPmm['T3_KLO']['branch'] = 'ROUTE_A'
    check('C3_R3_P6_BRANCH_FROM_THE_RULE_MANIFEST_OTHER_BRANCH_INCOMPLETE', run_eval(out, 'r5p6', R=Rk, RP=RPmm), 'INCOMPLETE', ids=('C3.R3.P6',),
          extra=lambda e: 'RPAIR_BRANCH_MISMATCH' in str(ptest(e, 'T3_KLO').get('reason')))
    # order lens N1: a Picard member whose own route-A tail record differs from its base's (smaller E^A, same identity)
    RPea = rp_clean('T3_KLO', 'PICARD', Rk, **{'C4T-KLO': {'uvt_over': {'E_A_rows_km_s_accepted': [0.0001 * TAU[i] for i in IDS]}}})
    check('R5_ORDER_N1_PICARD_MEMBER_OWN_TAIL_RECORD_NOT_THE_BASE_V6_INVALID', run_eval(out, 'r5n1', R=Rk, RP=RPea), 'INCOMPLETE',
          ids=('R4.order.N1', 'A53'), extra=lambda e: 'V6_ROUTE_A_TAIL_RECORD_NOT_THE_BASE_RECORD'
          in e['rpair_validity']['C4T-KLO@RPAIR:T3_KLO']['V6_codes'])
    # ================================================================ A53 NEW-17 (Claude3 B2 / R3-5 P5a P5b / H1-F3 N17a N17b)
    R0 = base_runs()
    RP5 = rp_clean('T3_KLO', 'PICARD', R0)
    e = run_eval(out, 'r5p5a', R=R0, RP=RP5)
    t('C3_B2_R3_P5a_NEW17_UNTRIGGERED_VALID_MEMBERS_REFUSED_AT_LOAD', e['decision']['outcome'] == 'REFUSED_AT_LOAD' and 'NEW-17' in e.get('refused', ''),
      ids=('A53.NEW-17', 'C3.B2', 'C3.R3.P5a', 'C3.H1-F3'), got=e['decision'])
    RP5b = rp_clean('T3_KLO', 'PICARD', R0, **{m: {'receipt': False} for m in M.PAIRS['T3_KLO']})
    e = run_eval(out, 'r5p5b', R=R0, RP=RP5b)
    t('C3_B2_R3_P5b_NEW17_UNTRIGGERED_INVALID_MEMBERS_REFUSED_AT_LOAD', e['decision']['outcome'] == 'REFUSED_AT_LOAD',
      ids=('A53.NEW-17', 'C3.B2', 'C3.R3.P5b'), got=e['decision'])
    Rgone = base_runs(**{'C4T-KLO': make_run('C4T-KLO', {}, present=False)})
    e = run_eval(out, 'r5n17u', R=Rgone, RP=rp_clean('T3_KLO', 'PICARD', base_runs()))
    t('A53_NEW17_DECIDABILITY_UNKNOWN_NOT_REFUSED_TEST_UNREAD_INCOMPLETE', e['decision']['outcome'] == 'INCOMPLETE', ids=('A53.NEW-17',),
      got=e['decision'].get('outcome'))
    sv = M.evaluate_v007
    err = io.StringIO()
    try:
        def boom(*a, **k):
            raise M.Refused('REFUSED: synthetic NEW-17 refusal (A53)')
        M.evaluate_v007 = boom
        _e, sys.stderr = sys.stderr, err
        try:
            with _quiet():
                rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(out / 'MANIFEST_REAL_PROBE.json'), '--case-block',
                             str(out / 'CASE_BLOCK_PROBE.json'), '--outdir', str(out / 'NEW17_CLI'), '--test-allow-unpinned-prereg', *REGARGS,
                             '--no-packets'])
        finally:
            sys.stderr = _e
    finally:
        M.evaluate_v007 = sv
    t('A53_NEW17_CLI_REFUSAL_RC2_NO_OUTDIR', rc == 2 and 'NEW-17' in err.getvalue() and not (out / 'NEW17_CLI').exists(), ids=('A53.NEW-17',), rc=rc)
    # ================================================================ A53 NEW-7 (Claude3 B1; H2 NEW7_* 12 probes, H1 N7a-c)
    GROW, EQUAL = [0.004, 0.0048, 0.00576], [0.004, 0.004, 0.004]
    for lab, tests in (('C6T', ('T1_H',)), ('C4T-KLO', ('T3_KLO',)), ('C5H', ('T2',)), ('C4T-D5', ('T2',)),
                       ('C4T', ('T1_H', 'T3_KLO', 'T3_KHI', 'RB_FP')), ('C4T-A', ('RB_FP',))):
        for nm, hh in (('growing', GROW), ('equal', EQUAL)):
            Rn = base_runs()
            set_hist(Rn[lab], hh)
            e = run_eval(out, 'r5n7_%s_%s' % (lab, nm), R=Rn)
            check('C3_B1_H2_NEW7_%s_%s_NO_ADOPT' % (lab, nm.upper()), e, 'INCOMPLETE', ids=('A53.NEW-7', 'C3.B1', 'C3.H2-F1'),
                  extra=lambda e, tests=tests: all(e['test_status'][u] in ('RPAIR_PENDING', 'INCOMPLETE') for u in tests)
                  and all(e['test_status'][u] == 'RPAIR_PENDING' and ptest(e, u)['rpair_branch'] == 'PICARD'
                          for u in tests if u != 'RB_FP'))
    Rn = base_runs()
    set_hist(Rn['C6T'], [0.00001 / 0.05, 0.00002 / 0.05])                          # H1 N7: ratio 2.0, a tiny last increment
    E, c, det = M.picard_noise_detail(Rn['C6T'], IDS, TAU)
    t('C3_H1_N7_RATIO_2_TINY_INCREMENT_E_UNAVAILABLE', E is None and c == M.E_UNAVAILABLE_NONCONTRACTING and det['contraction_observed'] is False,
      ids=('A53.NEW-7', 'C3.H1-F4'), code=c)
    RPn7 = rp_clean('T1_H', 'PICARD', Rn)
    check('A53_NEW7_TRIGGERED_PICARD_RPAIR_RESOLVES', run_eval(out, 'r5n7rp', R=Rn, RP=RPn7), 'ADOPT_TAIL', ids=('A53.NEW-7', 'A50.root1'),
          extra=lambda e: e['tests']['T1_H']['source'] == 'RPAIR')
    RPn7b = rp_clean('T1_H', 'PICARD', Rn)
    set_hist(RPn7b['T1_H']['_runs']['C6T'], [0.0002 / 0.05, 0.0002 / 0.05])        # the member does not contract either
    check('A53_NEW7_NON_CONTRACTING_PICARD_MEMBER_READS_UAIF', run_eval(out, 'r5n7uaif', R=Rn, RP=RPn7b), 'UNDECIDABLE_AT_ITERATION_FLOOR',
          ids=('A53.NEW-7',))
    # ================================================================ A53 r4 validity F1 option (a): the B0 EXT evidence
    def b0_noevid(r):
        for x in r['B0']['spec_sets']['EXT']:
            x.pop('projection_sha256', None)
            x.pop('declared_differences', None)
    check('A53_F1_B0_EXT_MEMBER_ENTRY_WITHOUT_EVIDENCE_INVALID', run_eval(out, 'r5b0e', R=Rra, RP=rp_clean('T2', 'ROUTE_A', Rra), b0_c5h=True,
                                                                        mutate=b0_noevid), 'INCOMPLETE', ids=('A53.F1', 'R4.validity.F1'),
          extra=lambda e: 'C5H_RPAIR_MEMBER_B0_EXT_ENTRY_LACKS_PROJECTION_EVIDENCE_A53_F1' in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch'])

    def b0_wrongdecl(r):
        for x in r['B0']['spec_sets']['EXT']:
            if 'declared_differences' in x:
                x['declared_differences'] = ['/numerics/route_a/ro1_workers']
    check('A53_F1_B0_EXT_DECLARED_DIFFERENCES_NOT_THE_CARRIED_LEAVES_INVALID',
          run_eval(out, 'r5b0d', R=Rra, RP=rp_clean('T2', 'ROUTE_A', Rra), b0_c5h=True, mutate=b0_wrongdecl), 'INCOMPLETE', ids=('A53.F1',),
          extra=lambda e: 'C5H_RPAIR_MEMBER_B0_EXT_DECLARED_DIFFERENCES_NOT_THE_CARRIED_LEAVES_A53_F1' in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch'])

    def b0_badevid(r):
        for x in r['B0']['spec_sets']['EXT']:
            if 'declared_differences' in x:
                x['declared_differences'] = ['/numerics/picard/passes']
    check('A53_F1_B0_EXT_EVIDENCE_OUTSIDE_THE_DECLARABLE_SET_RECORD_DEFECT', run_eval(out, 'r5b0b', R=Rra, RP=rp_clean('T2', 'ROUTE_A', Rra),
                                                                                   b0_c5h=True, mutate=b0_badevid), 'NO_RUN', ids=('A53.F1',))
    check('A53_F1_PICARD_C5H_MEMBER_DECLARES_NO_DIFFERENCE_VALID', run_eval(out, 'r5b0p', R=Rt2, RP=rp_clean('T2', 'PICARD', Rt2), b0_c5h=True),
          'ADOPT_TAIL', ids=('A53.F1',))
    # ================================================================ A53 r4 validity F2: interlock on ancestors / realpath (string only)
    anc = root / 'r5f2' / FORBIDDEN / 'stages' / '01_route_a' / 'attempt_000'
    anc.mkdir(parents=True)
    (anc / 'start.json').write_text(json.dumps({'call_spec_sha256': 'not the pin'}))
    with OpenTrace() as tr:
        w1 = M.c5h_interlock(str(anc))
        w2 = M.c5h_interlock(str(root / 'r5f2' / FORBIDDEN.lower() / 'x'))
        w3 = M.c5h_interlock(str(root / 'r5f2' / 'elsewhere'))
    t('A53_F2_INTERLOCK_ANCESTOR_COMPONENT_REFUSED_NO_FILE_OPENED', bool(w1) and bool(w2) and w3 is None and not tr.paths,
      ids=('A53.F2', 'R4.validity.F2'), opened=tr.paths)
    sv_dirs = M.C5H_REGISTERED_RUN_DIRS
    stand = root / 'r5f2' / 'REG_STANDIN_R5'
    (stand / 'stages').mkdir(parents=True)
    link = root / 'r5f2' / 'LINK_INTO_STANDIN'
    link.symlink_to((stand / 'stages').resolve())                 # absolute target (a relative OUT made it dangle: R5 errors register)
    try:
        M.C5H_REGISTERED_RUN_DIRS = (str(stand.resolve()),)
        with OpenTrace() as tr:
            w4 = M.c5h_interlock(str(link))
            ok_side = M.c5h_path_hit(str(stand / 'stages' / 'route_a' / 'attempt_000' / 'result.json'))
    finally:
        M.C5H_REGISTERED_RUN_DIRS = sv_dirs
    t('A53_F2_INTERLOCK_REALPATH_INSIDE_THE_REGISTERED_DIR_REFUSED_NO_FILE_OPENED', bool(w4) and 'inside' in w4 and ok_side and not tr.paths,
      ids=('A53.F2',), opened=tr.paths)
    dside = write_run_dir(root, 'C6T_SIDE_PATH_INTO_REGISTERED', dict(synthetic_completed_result(C4, numerics_for('C6T'), drv=V010, spec='c' * 64),
                          route_a_outcome={'classification': 'CONVERGED', 'converged_iteration': 6,
                                           'result_path': str(root / 'r5f2' / FORBIDDEN / 'stages' / 'x' / 'result.json'), 'result_sha256': 'f' * 64}))
    with OpenTrace() as tr:
        rs = M.read_run('C6T', str(dside), dict(CTX, case_block=CB, interlock_side_paths=True), True)
    t('A53_F2_TEST_MODE_FULL_MODE_RECORD_SIDE_PATH_INTO_THE_REGISTERED_RUN_NOT_OPENED',
      rs.get('unreadable') == 'SIDE_PATH_INTO_THE_REGISTERED_C5H_RUN_REFUSED' and not any(FORBIDDEN in x for x in tr.paths), ids=('A53.F2',),
      opened=[x for x in tr.paths if FORBIDDEN in x])
    # ================================================================ A53 r4 validity F3: RO1_FIRED_IN_IDENTITY_RUN
    iv = M.identity_run_validity('Z2', identity_run('Z2', ro1_fired=True), CTX)
    t('A53_F3_FIRED_ARMED_IDENTITY_RUN_NAMED_AND_NOT_VALID_IN_GATES_ONLY', 'RO1_FIRED_IN_IDENTITY_RUN' in iv['ro1_codes']
      and not (bool(iv['valid']) and not iv['ro1_codes']), ids=('A53.F3', 'R4.validity.F3'), codes=iv['ro1_codes'])
    check('A53_F3_FIRED_IDENTITY_RUN_STILL_NO_RUN_RA5a', run_eval(out, 'r5f3', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS},
                                                                                  'Z2': identity_run('Z2', ro1_fired=True)}), 'NO_RUN', ids=('A53.F3', 'RA5'))
    # ================================================================ A53: REVIEW_V009 repoint; NEW-13; NEW-19; NEW-9
    t('A53_REVIEW_V009_READ_AT_THE_PRESERVED_ORIGINAL_3bce7c02', M.PIN_REVIEW_V009[0].endswith('REVIEW_V009_PREP_V009_V001_ORIG_3bce7c02.json')
      and hashlib.sha256(Path(M.PIN_REVIEW_V009[0]).read_bytes()).hexdigest() == M.PIN_REVIEW_V009[1] == '3bce7c02926526edf2a594418097ff379604ee1c9760dc1145bcd37ed2882d9f'
      and CTX['c5h_admission']['admitted'], ids=('A53.REVIEW_V009', 'C3.H2-N3'))
    t('A53_NEW13_NODES_RO1_WORKERS_ON_THE_CUSTODY_LIST_FROM_BYTES', M.PIN_RO1_NODES_CUSTODY['worker'][1].startswith('0ae245d8')   # [R7 adapted,
      and M.PIN_RO1_NODES_CUSTODY['worker_parallel'][1].startswith('a5277172') and M.PIN_RO1_CUSTODY['binding'][1].startswith('86af6198')   # A62.3: r5]
      and all(hashlib.sha256(Path(p_).read_bytes()).hexdigest() == s_ for p_, s_ in M.PIN_RO1_NODES_CUSTODY.values()), ids=('A53.NEW-13',))
    eps_real = M.ART + '/tail_scheme_impl_c2/certificates_v002/gates/EPS_CERT_V006.json'
    g = M.evaluate_gate('EPS', eps_real, dict(CTX, case_block=CB), {})
    rd, why_ = M.srb_rot_readable({'EPS': g}, dict(CTX, case_block=CB))
    t('A53_NEW19_REAL_EPS_V006_ENVELOPE_BOUND_FIELDS_READ_PASS_AND_SRB_ROT_READABLE_AT_P32', g['status'] == 'PASS'
      and g['derived'].get('envelope_bound', {}).get('rule_ok') is True and rd, ids=('A53.NEW-19', 'A54.COVERAGE'), status=g['status'],
      codes=g['codes'], why=why_)
    ev9 = {'code': M.RO1_CODE, 'refusal': M.READOUT_REFUSALS[0], 'query': None, 'phi_rad': None, 'R_kpc': None, 'numerator': None,
           'denominator': None, 'after_convergence': True}
    c9a, _ = M.check_ro1_record({'ro1': dict(ro1b(fired=True), events=[ev9])})
    c9b, _ = M.check_ro1_record({'ro1': dict(ro1b(fired=True), events=[dict(ev9, numerator='inf')])})
    t('A53_NEW9_NULL_ACCEPTED_REPR_STRING_REFUSED', c9a == [] and any('FIELD_TYPE' in x for x in c9b), ids=('A53.NEW-9',), a=c9a, b=c9b)
    # ================================================================ A54 B4 (Claude3 B4; H2-F2 PASSROWS world)
    pr_ = M._pass_rows({'passes': driver_passes([dict(C4)] * 4, gap_at=1)})
    t('C3_B4_H2_F2_PASS_WITHOUT_ROWS_IS_A_RECORD_GAP', len(pr_) == 3 and M.pass_rows_gap({'passes': driver_passes([dict(C4)] * 4, gap_at=1)}) == 'PASS_WITHOUT_ROWS'
      and M.pass_rows_gap({'passes': driver_passes([dict(C4)] * 3, index=[1, 2, 4])}) == 'PASS_INDICES_NOT_CONSECUTIVE_FROM_1'
      and M.pass_rows_gap({'passes': driver_passes([dict(C4)] * 3)}) is None, ids=('A54.B4', 'C3.B4'))
    SMALL = [1.0 if TAU[i] == 0.05 else 0.0 for i in IDS]
    Rg = base_runs()
    set_hist(Rg['C6T'], [0.08, 0.064, 0.0512], shape=SMALL)                       # monotone q = 0.8 on the tau = 0.05 rows
    Rg['C6T']['pass_rows'] = [dict(x) for x in Rg['C6T']['pass_rows']]
    with_gap(Rg['C6T'], gap_at=1)
    e = run_eval(out, 'r5b4', R=Rg)
    check('C3_B4_H2_E2E3_GAP_RUN_E_UNAVAILABLE_NO_ADOPT', e, 'INCOMPLETE', ids=('A54.B4', 'C3.B4', 'C3.H2-F2'),
          extra=lambda e: e['tests']['T1_H']['status'] == 'RPAIR_PENDING' and M.PASS_ROW_GAP in e['tests']['T1_H']['noise']['reason'])
    Rg2 = base_runs()
    set_hist(Rg2['C6T'], [0.08, 0.064, 0.0512], shape=SMALL)
    check('C3_B4_H2_E2E3b_SAME_HISTORY_WITHOUT_THE_GAP_CONTROL', run_eval(out, 'r5b4c', R=Rg2), 'INCOMPLETE', ids=('A54.B4', 'C3.H2-F2'),
          extra=lambda e: e['tests']['T1_H']['status'] == 'RPAIR_PENDING')
    Rg3 = base_runs()
    with_gap(Rg3['C2T'], gap_at=0)                                                # the first pass without rows (last two intact)
    check('A54_B4_GAP_ON_A_CASE_NO_RPAIR_CAN_RESOLVE_READS_INCOMPLETE', run_eval(out, 'r5b4t1', R=Rg3), 'INCOMPLETE', ids=('A54.B4',),
          extra=lambda e: e['decision']['subtype'] == 'UNRESOLVED' and any('A54 B4 pass-row gap on C2T' in x for x in e['decision']['pending_steps']))
    Rg4 = base_runs()
    with_gap(Rg4['C6T'], gap_at=0)
    check('A54_B4_GAP_RESOLVED_BY_A_CLEAN_PICARD_RPAIR_ADOPT', run_eval(out, 'r5b4rp', R=Rg4, RP=rp_clean('T1_H', 'PICARD', Rg4)), 'ADOPT_TAIL',
          ids=('A54.B4',), extra=lambda e: e['tests']['T1_H']['source'] == 'RPAIR')
    RPg = rp_clean('T1_H', 'PICARD', Rg4)
    with_gap(RPg['T1_H']['_runs']['C6T'], gap_at=0)
    check('A54_B4_GAP_ON_AN_RPAIR_MEMBER_READS_INCOMPLETE_NOT_UAIF', run_eval(out, 'r5b4m', R=Rg4, RP=RPg), 'INCOMPLETE', ids=('A54.B4',),
          extra=lambda e: 'A54 B4' in str(e['tests']['T1_H'].get('reason')))
    Rg5 = base_runs()
    with_gap(Rg5['C4T-KHI'], gap_at=2)                                            # the last pass without rows: V2 cannot be cross-checked
    check('A54_B4_GAP_AT_THE_LAST_PASS_V2_CROSSCHECK_IMPOSSIBLE_CASE_INVALID', run_eval(out, 'r5b4v2', R=Rg5), 'INCOMPLETE', ids=('A54.B4', 'D9'),
          extra=lambda e: 'V2_CROSSCHECK_IMPOSSIBLE_PASS_ROW_GAP_AT_THE_LAST_PASSES' in e['validity']['C4T-KHI']['V2_codes'])
    graw = synthetic_completed_result(C4, numerics_for('C6T'), drv=V010, spec='c' * 64)
    graw['passes'][1]['rows'] = []
    dg = write_run_dir(root, 'C6T_PASS_ROW_GAP', graw)
    rg = M.read_run('C6T', str(dg), dict(CTX, case_block=CB), True)
    t('A54_B4_READ_RUN_ON_DISK_RECORDS_THE_GAP', rg.get('pass_rows_gap') == 'PASS_WITHOUT_ROWS' and len(rg['pass_rows']) == 2, ids=('A54.B4',))
    # ================================================================ A54 S7 (Claude3 H2-F3 masked world)
    i_slow = 6
    fast = [0.7, 0.07, 0.007]
    slw = [0.007 / 0.95 ** 2, 0.007 / 0.95, 0.007]
    P_ = [{i: 40.0 for i in IDS}]
    for k in range(3):
        P_.append({i: P_[-1][i] + (slw[k] if j == i_slow else fast[k]) * TAU[i] for j, i in enumerate(IDS)})
    runm = {'pass_rows': P_, 'adapted': {'rows': dict(P_[-1])}}
    E, c, det = M.picard_noise_detail(runm, IDS, TAU)
    rid = IDS[i_slow]
    dl, dp = P_[-1][rid] - P_[-2][rid], P_[-2][rid] - P_[-3][rid]
    qi = abs(dl) / abs(dp)                                    # [R6 adapted, A58 RI-18] no cap: q_i = 0.95, tail 0.133 tau
    want = abs(dl) * qi / (1 - qi)
    t('C3_S7_H2_F3_MASKED_SAME_SIGN_SLOW_ROW_GETS_ITS_PER_ROW_BOUND', c is None and abs(E[rid] - want) < 1e-12
      and abs(E[rid] / TAU[rid] - 0.133) < 1e-6
      and E[rid] / TAU[rid] > 50 * (TAU[rid] * det['tau_norm_last'] * det['factor']) / TAU[rid]
      and rid in det['rows_where_per_row_bound_exceeds_norm_bound'], ids=('A54.S7', 'C3.S7', 'C3.H2-F3'), E_over_tau=E[rid] / TAU[rid],
      norm_only_over_tau=det['tau_norm_last'] * det['factor'])
    slw2 = [0.015 / 0.95 ** 2, 0.015 / 0.95, 0.015]                      # the same world with the slow row's own tail > tau/8 (A54 S7)
    incs2 = [{i: (slw2[k] if j == i_slow else fast[k]) * TAU[i] for j, i in enumerate(IDS)} for k in range(3)]
    Rm = base_runs()
    Rm['C6T'] = with_passes(Rm['C6T'], passes_by_increments(Rm['C6T']['adapted']['rows'], incs2))
    check('A54_S7_MASKED_SLOW_ROW_MAKES_T1_H_UNDECIDABLE_RPAIR_PICARD', run_eval(out, 'r5s7', R=Rm), 'INCOMPLETE', ids=('A54.S7',),
          extra=lambda e: e['tests']['T1_H']['status'] == 'RPAIR_PENDING' and e['tests']['T1_H']['rpair_branch'] == 'PICARD')
    sgn = [{i: 0.1 * TAU[i] * (-1 if i == rid else 1) for i in IDS}, {i: 0.01 * TAU[i] for i in IDS}]
    E2, c2, det2 = M.picard_noise_detail(with_passes(make_run('C6T', C4), passes_by_increments(C4, sgn)), IDS, TAU)
    t('A54_S7_SIGN_CHANGING_ROW_PER_ROW_BOUND_ZERO_NORM_BOUND_KEPT', c2 is None and abs(E2[rid] - TAU[rid] * 0.01 * (0.1 / 0.9)) < 1e-12,
      ids=('A54.S7',))
    # ================================================================ A54 S4 (Claude3 H1-F1 C1-C4)
    Rmiss = base_runs(**{'C6T': make_run('C6T', {}, present=False)})
    e = run_eval(out, 'r5s4c1', R=Rmiss, mutate=lambda r: r['MT']['per_case'].pop('C6T'))      # an MT record cannot cover an absent case
    t('C3_S4_H1_F1_C1_MISSING_CASE_WITH_MT_RECORD_NO_RUN_STILL_NAMES_THE_CASE', e['decision']['outcome'] == 'NO_RUN'
      and any(x.startswith('C6T') for x in e['decision']['named']['cases_identity_runs_and_gates_missing_or_invalid'])
      and 'C6T' in e['decision']['named']['next_steps'] and any(x.startswith('C6T') for x in e['decision']['also_named_missing_or_invalid']),
      ids=('A54.S4', 'C3.S4', 'C3.H1-F1'), named=e['decision'].get('named'))
    e = run_eval(out, 'r5s4c2', R=Rmiss, drop=('MT',))
    t('C3_S4_H1_F1_C2_MISSING_CASE_WITHOUT_MT_INCOMPLETE_NAMES_IT', e['decision']['outcome'] == 'INCOMPLETE'
      and any(x.startswith('C6T') for x in e['decision']['named']['cases_identity_runs_and_gates_missing_or_invalid']), ids=('A54.S4', 'C3.H1-F1'))
    Rmc = base_runs(**{'C5H': make_run('C5H', {}, present=False)})

    def ea_no_c5h(r):
        del r['EA']['per_case']['C5H']
    e = run_eval(out, 'r5s4c3', R=Rmc, mutate=ea_no_c5h)
    t('C3_S4_H1_F1_C3_MISSING_C5H_WITH_EA_DEFECT_NO_RUN_NAMES_C5H', e['decision']['outcome'] == 'NO_RUN'
      and any(x.startswith('C5H') for x in e['decision']['named']['cases_identity_runs_and_gates_missing_or_invalid'])
      and any(x.startswith('EA') for x in e['decision']['named']['gates_record_defect']), ids=('A54.S4', 'C3.H1-F1'))
    e = run_eval(out, 'r5s4c4', R=Rmc, drop=('EA',))
    t('C3_S4_H1_F1_C4_MISSING_C5H_EA_ABSENT_INCOMPLETE_NAMES_BOTH', e['decision']['outcome'] == 'INCOMPLETE'
      and any(x.startswith('C5H') for x in e['decision']['reasons']) and any('EA' in x for x in e['decision']['reasons']), ids=('A54.S4',))
    e = run_eval(out, 'r5s4adopt')
    t('A54_S4_NAMED_BLOCK_ON_EVERY_READING_EMPTY_WHEN_ALL_VALID', e['decision']['outcome'] == 'ADOPT_TAIL'
      and e['decision']['named']['cases_identity_runs_and_gates_missing_or_invalid'] == [] and e['decision']['named']['gates_record_defect'] == [],
      ids=('A54.S4',))
    # ================================================================ A54 S5 (Claude3 H1-F2 section 6 probes)
    for gname, outcome_r4 in (('SRB_ROT', 'BOUND_INSUFFICIENT'), ('T2I', 'IMPLEMENTATION_DEFECT'), ('LO', 'NON_LAPSE_TAIL_MATERIAL'),
                              ('DOUBLING', 'NUMERICS_UNCERTIFIED'), ('GQ', 'NUMERICS_UNCERTIFIED')):
        for vv in ('NOT_COMPUTED', 'FAIL'):
            e = run_eval(out, 'r5s5_%s_%s' % (gname, vv), mutate=lambda r, g_=gname, v_=vv: r[g_].update(verdict=v_), auto_verdict=False)
            check('C3_S5_H1_F2_%s_VERDICT_%s_ON_PASSING_DATA_RECORD_DEFECT' % (gname, vv), e, 'NO_RUN', ids=('A54.S5', 'C3.S5', 'C3.H1-F2'),
                  extra=lambda e, g_=gname, v_=vv: e['gates'][g_]['status'] == 'RECORD_DEFECT' and any(
                      ('VERDICT_NOT_REGISTERED' if v_ == 'NOT_COMPUTED' else 'VERDICT_FAIL_CONTRADICTS_DATA') in x for x in e['gates'][g_]['codes']),
                  why='r4 read %s' % outcome_r4)

    def srb_fail_pass_verdict(r):
        r['SRB_ROT']['srb_rot_km_s'][5] = 0.2 * TAU[IDS[5]]
    check('A54_S5_PASS_VERDICT_WITH_A_FAILING_DATA_CLAUSE_RECORD_DEFECT', run_eval(out, 'r5s5p', mutate=srb_fail_pass_verdict, auto_verdict=False),
          'NO_RUN', ids=('A54.S5',), extra=lambda e: 'VERDICT_PASS_CONTRADICTS_DATA:SRB_ROT' in e['gates']['SRB_ROT']['codes'])
    check('A54_S5_FAIL_VERDICT_WITH_THE_FAILING_DATA_CLAUSE_DECIDED', run_eval(out, 'r5s5f', mutate=srb_fail_pass_verdict), 'BOUND_INSUFFICIENT',
          ids=('A54.S5',))

    def gq_short(r):
        for x in r['GQ']['rosters']:
            x['k_range_inverse_kpc'][0] = 16
    check('A54_S5_COVERAGE_SHORTFALL_UNDER_A_PASS_VERDICT_READS_FAIL_ROOT8', run_eval(out, 'r5s5cov', mutate=gq_short, auto_verdict=False),
          'NUMERICS_UNCERTIFIED', ids=('A54.S5', 'A50.root8'))
    check('A54_S5_VERDICT_ONLY_GATE_RB_FP_FAIL_READS_FAIL_NOT_DEFECT', run_eval(out, 'r5s5rb', mutate=lambda r: r['RB_FP'].update(verdict='FAIL'),
                                                                           auto_verdict=False), 'INCOMPLETE', ids=('A54.S5',),
          extra=lambda e: e['gates']['RB_FP']['status'] == 'FAIL' and e['tests']['RB_FP']['status'] == 'INCOMPLETE')
    # ================================================================ A54 S6 (Claude3 H1-F5): RB_FP labels; numbers glued to letters
    t('C3_S6_H1_N5_REDACTION_CATCHES_GLUED_AND_LEADING_DOT_NUMBERS', '61.2222222' not in M._blind_str('dV/x61.2222222', [])
      and '25' not in M._blind_str('a.25b', []) and M._blind_str('B2_C2R3_SANITY_GT_0.05 2029f26a T2I_MAX_GT_1e-12', []) ==
      'B2_C2R3_SANITY_GT_0.05 2029f26a T2I_MAX_GT_1e-12', ids=('A54.S6', 'C3.S6', 'C3.H1-N5'))
    Rp = {'C4T': {'result_sha256': hashlib.sha256(Path(CT + '/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/result.json').read_bytes()).hexdigest()},
          'C5H': {'result_sha256': hashlib.sha256(Path(CT + '/runs_ext/KMAX_A2F10_C5R3_RUN_V001/result.json').read_bytes()).hexdigest()}}
    for lab_, k in (('C2T', 'C2R3'), ('C3T', 'C3R3')):
        Rp[lab_] = {'result_sha256': hashlib.sha256(Path(M.PIN_R3[k][0]).read_bytes()).hexdigest()}
    Rp.update({c_: {} for c_ in M.T_CASES if c_ not in Rp})
    recs = complete_records(Rp, {n: {} for n in M.IDENTITY_RUNS})
    recs['RB_FP']['shells'] = ['x61.2222222', 'q.7777777']
    recs['RB_FP']['dV_static_shells_km_s'] = {'x61.2222222': [0.35] * 12, 'q.7777777': [0.15] * 12}
    gp = write_records(out, 'r5_s6_labels', recs)
    mps6 = out / 'MANIFEST_R5_S6.json'
    mps6.write_text(json.dumps(dict(man, gates=gp)))
    p = cli('R5_GATES_ONLY_S6_LABELS', '--gates-only', manifest=mps6)
    txt = (out / 'R5_GATES_ONLY_S6_LABELS' / 'GATES_ONLY.json').read_text() if p.returncode == 0 else ''
    t('C3_S6_H1_F5_GATES_ONLY_NEVER_EMITS_RB_FP_SHELL_LABELS', p.returncode == 0 and '61.2222222' not in txt + p.stdout
      and '7777777' not in txt + p.stdout and json.loads(txt)['gates']['RB_FP']['status'] == 'PASS', ids=('A54.S6', 'C3.S6', 'C3.H1-F5'),
      rc=p.returncode, stderr=p.stderr[-300:])
    # ================================================================ A54 S8 (Claude3 H2-F4 case blocks) and the generic T3
    def cb_with(f):
        return case_block(over=f)

    def swap(cb):
        a_, b_ = cb['cases']['C4T-D5'], cb['cases']['C4T-C5c']
        ua, ub = a_['normalized_spec_equal']['/numerics']['uv_tail'], b_['normalized_spec_equal']['/numerics']['uv_tail']
        a_['normalized_spec_equal']['/numerics']['uv_tail'], b_['normalized_spec_equal']['/numerics']['uv_tail'] = ub, ua
        a_['uv_tail_config_sha256'], b_['uv_tail_config_sha256'] = b_['uv_tail_config_sha256'], a_['uv_tail_config_sha256']

    def setuv(lab, f):
        def g_(cb):
            uv = cb['cases'][lab]['normalized_spec_equal']['/numerics']['uv_tail']
            f(uv)
            try:
                cb['cases'][lab]['uv_tail_config_sha256'] = LIB.normalize_config(uv)['sha256']
            except ValueError:
                pass                                           # the library refuses it: validate_case_block names that too
        return g_
    probes = {'swapped_D5_C5c_tails': swap,
              'D5_ext_grid_G6': setuv('C4T-D5', lambda uv: uv['source_rule'].update(ext_grid=CTX['grids']['G6'])),
              'C5c_K_out_6': setuv('C4T-C5c', lambda uv: uv['outer'].update(K_out_inverse_kpc=6.0)),
              'KLO_K_big_8': setuv('C4T-KLO', lambda uv: uv['outer'].update(K_big_inverse_kpc=8.0)),
              'KHI_K_big_32': setuv('C4T-KHI', lambda uv: uv['outer'].update(K_big_inverse_kpc=32.0)),
              'C4TA_lambda_1': setuv('C4T-A', lambda uv: uv.update(lambda_scale=1.0)),
              'C6T_gas_M_s_64': setuv('C6T', lambda uv: uv['gas'].update(M_s=64)),        # [R6 adapted, A57: C4T is M_s 128]
              'C3T_continuum_rule_on_D5_kind': setuv('C3T', lambda uv: uv.update(source_rule={'rule': 'nodes_v001', 'ext_grid': CTX['grids']['G5']})),
              'C2T_grid_G3': lambda cb: cb['cases']['C2T']['normalized_spec_equal']['/numerics'].update(composite_grid_spec=copy.deepcopy(CTX['grids']['G3'])),
              'C4T_outer_cube': setuv('C4T', lambda uv: uv.update(outer={'shape': 'cube', 'K_out_inverse_kpc': 5.0}))}
    res = {k: M.validate_case_block(cb_with(f)) for k, f in probes.items()}
    t('C3_S8_H2_F4_CASE_BLOCK_TAIL_CONTENT_SWAPS_AND_WRONG_VALUES_REFUSED', all(bool(w) for w in res.values()) and not M.validate_case_block(CB),
      ids=('A54.S8', 'C3.S8', 'C3.H2-F4'), res={k: [x[:90] for x in w[:2]] for k, w in res.items()})

    def scale_P(P):
        def f(cb):
            for lab in M.T_CASES:
                uv = cb['cases'][lab]['normalized_spec_equal']['/numerics']['uv_tail']
                if uv['outer'].get('shape') == 'cylinder':
                    uv['outer']['K_big_inverse_kpc'] = P * M.T3_KBIG_FACTOR.get(lab, 1.0)
                cb['cases'][lab]['uv_tail_config_sha256'] = LIB.normalize_config(uv)['sha256']
        return f
    cb64 = case_block(over=scale_P(64.0))
    cb256 = case_block(over=scale_P(256.0))
    sv_p = M.PRODUCTION_K_BIG_A55
    try:                      # [R6 adapted, A55] the generic T3 logic, read with the A55 pin lifted in-process (the pin is 128)
        M.PRODUCTION_K_BIG_A55 = None
        why64 = M.validate_case_block(cb64)
        bad_lo = case_block(over=lambda cb: (scale_P(64.0)(cb), setuv('C4T-KLO', lambda uv: uv['outer'].update(K_big_inverse_kpc=16.0))(cb)))
        bad_hi = case_block(over=lambda cb: (scale_P(64.0)(cb), setuv('C4T-KHI', lambda uv: uv['outer'].update(K_big_inverse_kpc=64.0))(cb)))
        why_lo, why_hi = M.validate_case_block(bad_lo), M.validate_case_block(bad_hi)
    finally:
        M.PRODUCTION_K_BIG_A55 = sv_p
    t('A54_T3_GENERIC_P_64_REGISTRATION_ACCEPTED_P_READ_FROM_C4T', not why64 and M.registered_P(cb64) == 64.0
      and M.registered_P(CB) == 128.0, ids=('A54.T3',), why=why64[:2])
    t('A54_T3_KLO_NOT_P_OVER_2_OR_KHI_NOT_2P_REFUSED', any('P/2' in w for w in why_lo) and any('2P' in w for w in why_hi), ids=('A54.T3',))
    t('A54_T3_R1_LABELS_C4T_K16_K64_RETIRED', 'C4T-K16' not in M.REGISTERED and 'C4T-K64' not in M.REGISTERED and 'T3_K16' not in M.RPAIR_IDS
      and M.PAIRS['T3_KLO'] == ('C4T', 'C4T-KLO') and M.PAIRS['T3_KHI'] == ('C4T', 'C4T-KHI'), ids=('A54.T3',))
    (out / 'MANIFEST_R5_RETIRED_LABEL.json').write_text(json.dumps(dict(man, cases=dict(man['cases'], **{'C4T-K16': '/x'}))))
    p = cli('R5_REFUSE_RETIRED_LABEL', manifest=out / 'MANIFEST_R5_RETIRED_LABEL.json')
    t('A54_T3_MANIFEST_NAMING_A_RETIRED_LABEL_REFUSED', p.returncode == 2 and 'unknown cases' in p.stderr, ids=('A54.T3',))
    try:                      # [R6 adapted, A55] the P = 128 certificates do not cover sqrt(2) x 2P = 724 at P = 256 (pin lifted)
        M.PRODUCTION_K_BIG_A55 = None
        e = run_eval(out, 'r5p256', cb=cb256)
    finally:
        M.PRODUCTION_K_BIG_A55 = sv_p
    t('A54_COVERAGE_AT_P256_EPS_LO_GQ_ENVELOPE_SHORT', e['gates']['EPS']['status'] == 'FAIL' and 'EPS_COVERAGE' in e['gates']['EPS']['codes']
      and e['gates']['LO']['status'] == 'RECORD_DEFECT' and any('LO_COVERAGE_BELOW_SQRT2_TIMES_2P_A54' in x for x in e['gates']['LO']['codes'])
      and e['gates']['GQ']['status'] == 'FAIL' and e['decision']['outcome'] == 'NO_RUN', ids=('A54.COVERAGE', 'A54.T3'),
      st={g_: e['gates'][g_]['status'] for g_ in ('EPS', 'LO', 'GQ')})
    t('A55_PIN_128_REFUSES_A_P_64_REGISTRATION', any('A55' in w for w in M.validate_case_block(cb64)) and not M.validate_case_block(CB)
      and M.PRODUCTION_K_BIG_A55 == 128.0, ids=('A55', 'A56.FU1'))

    def lo_to_64(r):
        r['LO']['shells'] = [x for x in r['LO']['shells'] if x['range_inverse_kpc'][1] <= 64]
    check('A54_LO_COVERAGE_ONLY_TO_64_AT_P128_RECORD_DEFECT', run_eval(out, 'r5lo64', mutate=lo_to_64), 'NO_RUN', ids=('A54.COVERAGE',),
          extra=lambda e: any('LO_COVERAGE_BELOW_SQRT2_TIMES_2P_A54' in x for x in e['gates']['LO']['codes']))

    def lo_ext_fail(r):
        r['LO']['shells'][-1]['max_over_tau'] = 0.006
    check('A54_LO_EXTENDED_SHELL_ABOVE_0p005_NON_LAPSE_TAIL_MATERIAL', run_eval(out, 'r5loext', mutate=lo_ext_fail), 'NON_LAPSE_TAIL_MATERIAL',
          ids=('A54.COVERAGE',))

    def eps_90(r):                                                   # [R6 adapted, A55] 362 < sqrt(2) x 256 = 362.04
        r['EPS']['coverage_inverse_kpc']['DDO'] = [2, 362]
    check('A54_EPS_COVERAGE_BELOW_SQRT2_2P_AT_P128_NUMERICS_UNCERTIFIED', run_eval(out, 'r5eps90', mutate=eps_90), 'NUMERICS_UNCERTIFIED',
          ids=('A54.COVERAGE',), extra=lambda e: 'EPS_COVERAGE' in e['gates']['EPS']['codes'])
    e = run_eval(out, 'r5kbig', R=base_runs(**{'C4T-KHI': lambda R: make_run('C4T-KHI', shift(R['C4T']['adapted']['rows'], 0.3))}))
    t('A54_A56_N4_KBIG_NOT_CONVERGED_NEXT_STEP_READS_P_FROM_THE_CASE_BLOCK', e['decision']['outcome'] == 'KBIG_NOT_CONVERGED'
      and e['decision']['next_step'].startswith('T3prime: production 2P with {P, 4P}; EPS/LO coverage >= sqrt(2) x 4P (A56 N4)')
      and 'production K_big 256 with {128, 512}; EPS/LO coverage >= sqrt(2) x 512' in e['decision']['next_step'], ids=('A54.T3', 'A56.N4'),
      ns=e['decision']['next_step'])
    sv = M.PRODUCTION_K_BIG_A55
    try:                                                  # [R6 adapted, A56 follow-up 1] the pin is 128.0; the fixture P is 128
        M.PRODUCTION_K_BIG_A55 = 32.0
        no32 = any('A55' in w for w in M.validate_case_block(CB))
    finally:
        M.PRODUCTION_K_BIG_A55 = sv
    t('A54_A55_P_PIN_WHEN_SET_MUST_EQUAL_THE_REGISTERED_P', no32 and not M.validate_case_block(CB) and M.PRODUCTION_K_BIG_A55 == 128.0,
      ids=('A54.T3', 'A55', 'A56.FU1'))
    saved = (M.V007_PREREG_SHA256, M.PIN_ADDENDUM_V005)
    err = io.StringIO()
    try:
        M.V007_PREREG_SHA256 = hashlib.sha256(Path(M.PIN_DRAFT_R1[0]).read_bytes()).hexdigest()
        M.PIN_ADDENDUM_V005 = hashlib.sha256(Path(M.ADDENDUM_V005_CITED).read_bytes()).hexdigest()
        _e, sys.stderr = sys.stderr, err
        try:
            rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(out / 'MANIFEST_REAL_PROBE.json'), '--case-block',
                         str(out / 'CASE_BLOCK_PROBE.json'), '--outdir', str(out / 'SEALED_NO_A55')])
        finally:
            sys.stderr = _e
    finally:
        M.V007_PREREG_SHA256, M.PIN_ADDENDUM_V005 = saved
    t('A54_A62_3_SEALED_MODE_WITH_A55_SET_STILL_REFUSES_WITHOUT_THE_V010_R5_CHECK', rc == 2 and 'A62.3' in err.getvalue()   # [R7 renamed]
      and 'A55' not in err.getvalue() and not (out / 'SEALED_NO_A55').exists() and M.PIN_V010_R5_CHECK is None,
      ids=('A54.T3', 'A55', 'A56.FU3', 'A62.3'), err=err.getvalue()[-300:])
    # ================================================================ r4 validity F1: the regenerated field contract
    fp5 = out / 'FIELDS_R6_TEST.md'
    M.write_field_contract(str(fp5))
    ftxt = fp5.read_text()
    t('R5_VALIDITY_F1_FIELD_CONTRACT_CARRIES_A52_1_A52_3_A53_B0_RULES', all(x in ftxt for x in ('A52.1', 'ro1_workers', 'projection_sha256',
      'declared_differences', 'NEW-17', 'B0prime_RERUN (A52.1)', 'C4T-KLO', 'A54 B4', 'A54 S5')) and 'FIELDS_R8.md' in ftxt,   # [R8 adapted]
      ids=('R4.validity.F1', 'A53.F1'))
    t('R6_FIELD_CONTRACT_CARRIES_THE_POST_R5_RULINGS', all(x in ftxt for x in (
        'A54 S9', 'A58 RI-18', 'A56 N1', 'A56 N2', 'RB_FP', 'source_gas_M_s', 'ddo_K_big_inverse_kpc', 'ddo_gas_M_s', 'A58 RI-17',
        'inadmissible_record', 'r5 recheck order F1', 'r5 recheck order N4', 'r5 validity F1', 'A57')), ids=('R6', 'S9', 'A56.N2', 'A57', 'A58'))


def with_s9(run, edit):
    """[A54 S9] give a fixture run a driver passes[] record (built from its pass rows) edited by edit(passes), read exactly as
    read_run reads it: the S9 code is computed on the raw record before any dict is built."""
    ps = driver_passes([dict(p) for p in run['pass_rows']])
    edit(ps)
    run['result']['passes'] = ps
    run['pass_rows_s9'] = M.pass_rows_ids_code(run['result'], IDS)
    run['pass_rows'] = [] if run['pass_rows_s9'] else M._pass_rows(run['result'])
    run['pass_rows_gap'] = M.pass_rows_gap(run['result'])
    return run


def merge_rp(*rps):
    out_ = {}
    for x in rps:
        out_.update(x)
    return out_


def r6_tests(out, root, man, cli, slow, rp_clean):
    """[R6] one test (or more) per ruling made after r5 that the compare reads (A54 S9, A55 / A56 follow-ups, A56 N1/N2/N4, A57,
    A58 RI-03/06/17/18) and per r5-recheck finding (order B1, F1, N1-N4; validity F1-F8), the recheck probe worlds re-built as
    regression tests where feasible (ids 'S9', 'A55', 'A56.*', 'A57', 'A58.*', 'R6.*' in 'covers')."""
    GROW = [0.004, 0.0048, 0.00576]
    # ================================================================ A54 S9 (Codex2 CX2-R5-B1; r5 order B1, validity F5)
    ok_ps = driver_passes([dict(C4)] * 3)

    def variant(f):
        ps = copy.deepcopy(ok_ps)
        f(ps)
        return M.pass_rows_ids_code({'passes': ps}, IDS)
    v_dup = variant(lambda ps: ps[0]['rows'].append(dict(ps[0]['rows'][3])))
    v_unk = variant(lambda ps: ps[1]['rows'].append({'id': 'DDO154_SPARC12_99', 'speed_km_s': 1.0}))
    v_mis = variant(lambda ps: ps[1]['rows'].pop(4))
    v_swp = variant(lambda ps: ps[0]['rows'].__setitem__(2, dict(ps[0]['rows'][2], id='DDO154_SPARC12_99')))
    v_int = variant(lambda ps: ps[0]['rows'].__setitem__(2, dict(ps[0]['rows'][2], id=3)))
    v_nd = variant(lambda ps: ps[0]['rows'].__setitem__(2, 'row'))
    v_fin = variant(lambda ps: ps[-1]['rows'].append(dict(ps[-1]['rows'][0])))
    v_gap = variant(lambda ps: ps[0].__setitem__('rows', []))
    t('S9_UNIT_EVERY_PASS_ROW_SET_EXACTLY_THE_12_IDS_EACH_ONCE', M.pass_rows_ids_code({'passes': ok_ps}, IDS) is None
      and all(x == M.PASS_ROWS_S9 for x in (v_dup, v_unk, v_mis, v_swp, v_int, v_nd, v_fin)) and v_gap is None
      and M.pass_rows_gap({'passes': [dict(ok_ps[0], rows=[])] + ok_ps[1:]}) == 'PASS_WITHOUT_ROWS',
      ids=('A54.S9', 'R6.order.B1', 'R6.validity.F5'), got=[v_dup, v_unk, v_mis, v_swp, v_int, v_nd, v_fin, v_gap])
    # order B1 world: the C4T-KLO 'loud' history (undecidable) whose non-final passes also list all 12 ids at quiet values
    Rl = base_runs(**{'C4T-KLO': remake('C4T-KLO', **slow)})
    check('S9_CONTROL_LOUD_HISTORY_RPAIR_PENDING', run_eval(out, 'r6s9c', R=Rl), 'INCOMPLETE', ids=('A54.S9',),
          extra=lambda e: e['tests']['T3']['pairs']['T3_KLO']['status'] == 'RPAIR_PENDING')
    Rd = base_runs(**{'C4T-KLO': remake('C4T-KLO', **slow)})
    fin = dict(Rd['C4T-KLO']['adapted']['rows'])

    def dup_quiet(ps):
        quiet = [{i: fin[i] + 4e-6 for i in IDS}, {i: fin[i] + 1e-6 for i in IDS}]
        for k, p in enumerate(ps[:-1]):
            p['rows'] = p['rows'] + [{'id': i, 'speed_km_s': quiet[k][i]} for i in IDS]
    with_s9(Rd['C4T-KLO'], dup_quiet)
    hidden = M._pass_rows(Rd['C4T-KLO']['result'])           # what a dict-building reader (r5) reads: the quiet history
    Eh, ch = M.picard_noise({'pass_rows': hidden, 'adapted': Rd['C4T-KLO']['adapted']}, IDS, TAU)
    check('S9_DUPLICATE_PASS_ROW_IDS_WITH_QUIET_VALUES_RECORD_DEFECT_CASE_INCOMPLETE', run_eval(out, 'r6s9d', R=Rd), 'INCOMPLETE',
          ids=('A54.S9', 'R6.order.B1'), extra=lambda e: e['decision']['subtype'] == 'CASES_OR_RECORDS'
          and M.PASS_ROWS_S9 in e['validity']['C4T-KLO']['V1_codes'] and e['decision']['tests_read'] is False
          and ch is None and max(Eh[i] / TAU[i] for i in IDS) < 1e-3,
          why='r5 read this record ADOPT_TAIL (the last duplicate won)')
    Ru = base_runs()
    with_s9(Ru['C4T-KLO'], lambda ps: [p['rows'].append({'id': 'DDO154_SPARC12_99', 'speed_km_s': 1.0}) for p in ps])
    check('S9_UNKNOWN_13TH_PASS_ROW_ID_RECORD_DEFECT_CASE_INCOMPLETE', run_eval(out, 'r6s9u', R=Ru), 'INCOMPLETE',
          ids=('A54.S9', 'R6.order.B1'), extra=lambda e: M.PASS_ROWS_S9 in e['validity']['C4T-KLO']['V1_codes'],
          why='r5 read this record ADOPT_TAIL')
    RPs = rp_clean('T3_KLO', 'PICARD', Rl)
    with_s9(RPs['T3_KLO']['_runs']['C4T-KLO'], lambda ps: ps[0]['rows'].append(dict(ps[0]['rows'][0])))
    check('S9_ON_AN_RPAIR_MEMBER_MEMBER_INVALID_TEST_INCOMPLETE', run_eval(out, 'r6s9m', R=Rl, RP=RPs), 'INCOMPLETE', ids=('A54.S9',),
          extra=lambda e: M.PASS_ROWS_S9 in e['rpair_validity']['C4T-KLO@RPAIR:T3_KLO']['V1_codes']
          and e['tests']['T3']['pairs']['T3_KLO']['status'] == 'INCOMPLETE')
    idr = identity_run('Z2')
    idr['pass_rows_s9'] = M.PASS_ROWS_S9
    iv = M.identity_run_validity('Z2', idr, CTX)
    t('S9_ON_AN_IDENTITY_RUN_INVALID', iv['valid'] is False and M.PASS_ROWS_S9 in iv['codes'], ids=('A54.S9',), codes=iv['codes'])
    graw = synthetic_completed_result(C4, numerics_for('C6T'), drv=V010, spec='c' * 64)
    graw['passes'][0]['rows'].append(dict(graw['passes'][0]['rows'][5]))
    ds9 = write_run_dir(root, 'C6T_S9_DUPLICATE', graw)
    rs9 = M.read_run('C6T', str(ds9), dict(CTX, case_block=CB), True)
    vs9 = M.case_validity('C6T', rs9, dict(CTX, case_block=CB), {'V4': True, 'V5': True}, None, None)
    t('S9_READ_RUN_ON_DISK_CODE_BEFORE_ANY_DICT_NO_PASS_ROWS_BUILT', rs9.get('pass_rows_s9') == M.PASS_ROWS_S9 and rs9['pass_rows'] == []
      and M.PASS_ROWS_S9 in vs9['V1_codes'] and vs9['V1'] is False, ids=('A54.S9',))
    # ================================================================ r5 recheck order F1: a PICARD member's EA entry is its base's
    Rn2 = base_runs()
    set_hist(Rn2['C4T-D5'], GROW)                                                     # NEW-7 on C4T-D5: T2 -> R-PAIR PICARD
    RPt2 = rp_clean('T2', 'PICARD', Rn2)

    def ea_base(v, member=None, drop_member=False):
        def f(r):
            r['EA']['per_case']['C5H']['E_A_rows_km_s'] = [v * TAU[i] for i in IDS]
            if member is not None:
                r['EA']['per_case']['C5H@RPAIR:T2']['E_A_rows_km_s'] = [member * TAU[i] for i in IDS]
            if drop_member:
                del r['EA']['per_case']['C5H@RPAIR:T2']
        return f
    check('R6_ORDER_F1_PICARD_MEMBER_EA_ENTRY_CONTRADICTS_BASE_MEMBER_INVALID_NOT_ADOPT',
          run_eval(out, 'r6f1a', R=Rn2, RP=RPt2, b0_c5h=True, mutate=ea_base(0.13)), 'INCOMPLETE', ids=('R6.order.F1', 'A53'),
          extra=lambda e: M.PICARD_EA_ENTRY_CODE in e['rpair_validity']['C5H@RPAIR:T2']['V3_mismatch']
          and e['tests']['T2']['status'] == 'INCOMPLETE', why='r5 read this world ADOPT_TAIL (member entry 0.005 tau replaced base 0.13 tau)')
    check('R6_ORDER_F1_CONTROL_MEMBER_ENTRY_EQUAL_TO_BASE_UAIF', run_eval(out, 'r6f1b', R=Rn2, RP=RPt2, b0_c5h=True, mutate=ea_base(0.13, 0.13)),
          'UNDECIDABLE_AT_ITERATION_FLOOR', ids=('R6.order.F1',), extra=lambda e: e['rpair_validity']['C5H@RPAIR:T2']['valid_all'])
    check('R6_ORDER_F1_CONTROL_MEMBER_ENTRY_ABSENT_READS_THE_BASE_E_A_UAIF',
          run_eval(out, 'r6f1c', R=Rn2, RP=RPt2, b0_c5h=True, mutate=ea_base(0.13, drop_member=True)), 'UNDECIDABLE_AT_ITERATION_FLOOR',
          ids=('R6.order.F1',))
    Rnp = base_runs(**{lab: remake(lab, probe=False) for lab in ('C4T', 'C4T-KLO')})
    set_hist(Rnp['C4T-KLO'], GROW)
    RPnp = rp_clean('T3_KLO', 'PICARD', Rnp)

    def ea_tcase(member_entry):
        def f(r):
            for lab, v in (('C4T', 0.005), ('C4T-KLO', 0.13)):
                r['EA']['per_case'][lab] = {'result_sha256': Rnp[lab]['result_sha256'], 'E_A_rows_km_s': [v * TAU[i] for i in IDS],
                                            'accepted_iteration': 6, 'row_radii_m': list(RADII)}
            if member_entry:
                r['EA']['per_case']['C4T-KLO@RPAIR:T3_KLO'] = {
                    'result_sha256': RPnp['T3_KLO']['_runs']['C4T-KLO']['result_sha256'], 'E_A_rows_km_s': [0.005 * TAU[i] for i in IDS],
                    'accepted_iteration': 6, 'row_radii_m': list(RADII)}
        return f
    check('R6_ORDER_F1_T_CASE_NO_PROBE_MEMBER_EA_ENTRY_CONTRADICTS_BASE_INVALID', run_eval(out, 'r6f1d', R=Rnp, RP=RPnp, mutate=ea_tcase(True)),
          'INCOMPLETE', ids=('R6.order.F1',), extra=lambda e: M.PICARD_EA_ENTRY_CODE in e['rpair_validity']['C4T-KLO@RPAIR:T3_KLO']['V3_mismatch'],
          why='r5 read this world ADOPT_TAIL')
    check('R6_ORDER_F1_T_CASE_CONTROL_NO_MEMBER_ENTRY_UAIF', run_eval(out, 'r6f1e', R=Rnp, RP=RPnp, mutate=ea_tcase(False)),
          'UNDECIDABLE_AT_ITERATION_FLOOR', ids=('R6.order.F1',))
    # ================================================================ A56 N1 + A58 RI-18 (r5 order N1 post-r5 probes)
    def hist(rowq, sign, row=3):
        fast = [0.05, 0.005, 0.0005]
        r4_ = [0.0004 / rowq ** 2, 0.0004 / rowq, 0.0004]
        P_ = [dict(C4)]
        for k in range(3):
            nxt = {i: P_[-1][i] + fast[k] * TAU[i] for i in IDS}
            nxt[IDS[row]] = P_[-1][IDS[row]] + (sign ** k) * r4_[k] * TAU[IDS[row]]
            P_.append(nxt)
        return {'pass_rows': P_, 'adapted': {'rows': dict(P_[-1])}, 'pass_rows_gap': None}

    def expected_E(run):
        """An independent re-derivation of the R6 rule (A51 F2 uncapped by RI-18, A54 S7, A56 N1) from the pass rows."""
        pr = run['pass_rows'][-4:]
        d = [{i: pr[j][i] - pr[j - 1][i] for i in IDS} for j in range(1, len(pr))]
        n = [max(abs(x[i]) / TAU[i] for i in IDS) for x in d]
        rs = [n[j] / n[j - 1] for j in range(1, len(n))]
        q = max(rs[-2:])
        out_ = {}
        for i in IDS:
            a_, b_ = abs(d[-1][i]), abs(d[-2][i])
            qi = (a_ / b_) if b_ else (0.0 if a_ == 0 else math.inf)
            if qi >= 1:
                return None
            row = 0.0 if a_ == 0 else (a_ * qi / (1 - qi) if d[-1][i] * d[-2][i] > 0 else a_ * qi / (1 + qi))
            out_[i] = max(TAU[i] * n[-1] * q / (1 - q), row)
        return out_
    res = {}
    for nm, q_, sg in (('ALTERNATING_ROW_Q_0p95', 0.95, -1), ('SAME_SIGN_ROW_Q_1p2', 1.2, 1), ('ALTERNATING_ROW_Q_1p2', 1.2, -1)):
        run = hist(q_, sg)
        E, c, det = M.picard_noise_detail(run, IDS, TAU)
        want = expected_E(run)
        res[nm] = (c, None if E is None else E[IDS[3]] / TAU[IDS[3]])
        ok = (want is None and E is None and c == M.E_UNAVAILABLE_ROW_RATIO and det.get('rows_with_ratio_ge_1') == [IDS[3]]) or (
            want is not None and c is None and all(abs(E[i] - want[i]) <= 1e-12 * max(want[i], 1e-30) for i in IDS))
        t('A56_N1_%s' % nm, ok, ids=('A56.N1', 'A58.RI-18', 'R6.order.N1'), got=res[nm])
    t('A56_N1_ALTERNATING_ROW_Q_0p95_E_OVER_TAU_1p95e-4_NOT_R5S_5p6e-5', abs(res['ALTERNATING_ROW_Q_0p95'][1] - 0.0004 * 0.95 / 1.95) < 1e-12,
      ids=('A56.N1', 'R6.order.N1'), got=res['ALTERNATING_ROW_Q_0p95'])
    Ra = base_runs()
    Ra['C4T-KHI'] = with_passes(Ra['C4T-KHI'], hist(1.2, -1)['pass_rows'])
    check('A56_N1_ALTERNATING_ROW_Q_1p2_SENDS_T3_KHI_TO_RPAIR_PICARD', run_eval(out, 'r6n1', R=Ra), 'INCOMPLETE', ids=('A56.N1',),
          extra=lambda e: e['tests']['T3']['pairs']['T3_KHI']['status'] == 'RPAIR_PENDING'
          and e['tests']['T3']['pairs']['T3_KHI']['rpair_branch'] == 'PICARD'
          and M.E_UNAVAILABLE_ROW_RATIO in e['tests']['T3']['pairs']['T3_KHI']['noise']['reason'])
    E, c, det = M.picard_noise_detail(make_run('C6T', C4, dlast=0.001, q=0.95), IDS, TAU)
    t('A58_RI18_Q_CAP_REMOVED_FACTOR_19_AT_Q_0p95', c is None and abs(det['q'] - 0.95) < 1e-9 and abs(det['factor'] - 19.0) < 1e-6
      and M.PICARD_Q_CAP is None, ids=('A58.RI-18',), factor=det.get('factor'))
    check('A58_RI18_SLOW_Q_0p99_RUN_LARGE_E_GOES_TO_RPAIR', run_eval(out, 'r6ri18', R=base_runs(**{'C6T': remake('C6T', dlast=0.0002, q=0.99)})),
          'INCOMPLETE', ids=('A58.RI-18',), extra=lambda e: e['tests']['T1_H']['status'] == 'RPAIR_PENDING')
    # ================================================================ A56 N2: the RB_FP R-PAIR path (C4T / C4T-A)
    Rb = base_runs()
    set_hist(Rb['C4T-A'], GROW)
    check('A56_N2_C4TA_E_UNAVAILABLE_RB_FP_RPAIR_PENDING', run_eval(out, 'r6n2p', R=Rb), 'INCOMPLETE', ids=('A56.N2',),
          extra=lambda e: e['tests']['RB_FP']['status'] == 'RPAIR_PENDING' and e['decision']['subtype'] == 'UNRESOLVED'
          and any(x.startswith('RB_FP') for x in e['decision']['pending_steps']))
    RPb = rp_clean('RB_FP', 'PICARD', Rb)
    check('A56_N2_RB_FP_READ_ON_ITS_PICARD_RPAIR_ADOPT', run_eval(out, 'r6n2a', R=Rb, RP=RPb), 'ADOPT_TAIL', ids=('A56.N2',),
          extra=lambda e: e['tests']['RB_FP']['source'] == 'RPAIR' and e['tests']['RB_FP']['status'] == 'PASS'
          and all(e['rpair_validity'][k]['valid_all'] and e['rpair_validity'][k]['V6'] for k in ('C4T@RPAIR:RB_FP', 'C4T-A@RPAIR:RB_FP')))
    RPb2 = rp_clean('RB_FP', 'PICARD', Rb)
    set_hist(RPb2['RB_FP']['_runs']['C4T-A'], GROW)
    check('A56_N2_RB_FP_MEMBER_STILL_UNAVAILABLE_INCOMPLETE', run_eval(out, 'r6n2u', R=Rb, RP=RPb2), 'INCOMPLETE', ids=('A56.N2',),
          extra=lambda e: 'A56 N2: still unresolved' in str(e['tests']['RB_FP'].get('reason')))
    RPb3 = rp_clean('RB_FP', 'PICARD', Rb, **{'C4T-A': {'receipt': False}})
    check('A56_N2_RB_FP_MEMBER_INVALID_INCOMPLETE', run_eval(out, 'r6n2i', R=Rb, RP=RPb3), 'INCOMPLETE', ids=('A56.N2',),
          extra=lambda e: 'RPAIR_MEMBER_INVALID_OR_MISSING' in str(e['tests']['RB_FP'].get('reason')))
    R0 = base_runs()
    e = run_eval(out, 'r6n2r', R=R0, RP=rp_clean('RB_FP', 'PICARD', R0))
    t('A56_N2_NEW17_RB_FP_MEMBERS_NAMED_WITH_BOTH_E_AVAILABLE_REFUSED_AT_LOAD', e['decision']['outcome'] == 'REFUSED_AT_LOAD'
      and 'RB_FP' in e.get('refused', ''), ids=('A56.N2', 'A53.NEW-17'), got=e['decision'])
    mra = out / 'MANIFEST_R6_RB_FP_ROUTE_A.json'
    mra.write_text(json.dumps(dict(man, rpair={'RB_FP': {'branch': 'ROUTE_A', 'members': {'C4T': '/x1', 'C4T-A': '/x2'}}})))
    try:
        M.load_manifest(str(mra))
        refused = None
    except M.Refused as exc:
        refused = str(exc)
    mpk = out / 'MANIFEST_R6_RB_FP_PICARD.json'
    mpk.write_text(json.dumps(dict(man, rpair={'RB_FP': {'branch': 'PICARD', 'members': {'C4T': '/x1', 'C4T-A': '/x2'}}})))
    t('A56_N2_RB_FP_RPAIR_IS_PICARD_ONLY_AT_MANIFEST_LOAD', refused is not None and 'A56 N2' in refused
      and M.load_manifest(str(mpk))['rpair']['RB_FP']['branch'] == 'PICARD' and M.rpair_key_ok('C4T-A@RPAIR:RB_FP')
      and not M.rpair_key_ok('C6T@RPAIR:RB_FP'), ids=('A56.N2',))
    Rga = base_runs()
    with_gap(Rga['C4T-A'], gap_at=0)
    check('A56_N2_C4TA_B4_GAP_RESOLVED_BY_THE_RB_FP_RPAIR_ADOPT_NOT_PROVISIONAL', run_eval(out, 'r6n2g', R=Rga, RP=rp_clean('RB_FP', 'PICARD', Rga)),
          'ADOPT_TAIL', ids=('A56.N2', 'A54.B4'), extra=lambda e: e['decision']['provisional'] is False and e['tests']['RB_FP']['source'] == 'RPAIR')
    check('A56_N2_C4TA_B4_GAP_WITHOUT_ITS_RPAIR_PENDING', run_eval(out, 'r6n2g0', R=Rga), 'INCOMPLETE', ids=('A56.N2', 'A54.B4'),
          extra=lambda e: e['tests']['RB_FP']['status'] == 'RPAIR_PENDING' and any('A54 B4 pass-row gap on C4T-A' in x for x in e['decision']['pending_steps']))
    Rg4 = base_runs()
    with_gap(Rg4['C4T'], gap_at=0)
    RP4 = merge_rp(*(rp_clean(p_, 'PICARD', Rg4) for p_ in ('T1_H', 'T3_KLO', 'T3_KHI', 'RB_FP')))
    check('A56_N2_C4T_B4_GAP_RESOLVED_BY_ITS_FOUR_RPAIRS_ADOPT', run_eval(out, 'r6n2c4', R=Rg4, RP=RP4), 'ADOPT_TAIL', ids=('A56.N2', 'A54.B4'),
          extra=lambda e: e['decision']['provisional'] is False and all(
              (e['tests']['T3']['pairs'][u] if u.startswith('T3') else e['tests'][u])['source'] == 'RPAIR' for u in ('T1_H', 'T3_KLO', 'T3_KHI', 'RB_FP')),
          why='r5 read RB_FP INCOMPLETE here (r5 order N1, B4 world)')
    RP3 = merge_rp(*(rp_clean(p_, 'PICARD', Rg4) for p_ in ('T1_H', 'T3_KLO', 'T3_KHI')))
    check('A56_N2_C4T_B4_GAP_THREE_RPAIRS_WITHOUT_RB_FP_PENDING', run_eval(out, 'r6n2c3', R=Rg4, RP=RP3), 'INCOMPLETE', ids=('A56.N2', 'A54.B4'),
          extra=lambda e: e['tests']['RB_FP']['status'] == 'RPAIR_PENDING')
    # ================================================================ A57 ruling 1: production gas M_s 128 (NGC 96)
    def all_ms(v):
        def f(cb):
            for lab in M.T_CASES:
                uv = cb['cases'][lab]['normalized_spec_equal']['/numerics']['uv_tail']
                uv['gas']['M_s'] = v
                cb['cases'][lab]['uv_tail_config_sha256'] = LIB.normalize_config(uv)['sha256']
        return f
    why = M.validate_case_block(case_block(over=all_ms(64)))
    t('A57_CASE_BLOCK_GAS_M_S_64_EVERYWHERE_REFUSED', any('A57' in w for w in why) and not M.validate_case_block(CB), ids=('A57',), why=why[:2])

    def gq_ms(j, ms):
        def f(r):
            r['GQ']['rosters'][j]['M_s'] = ms
            r['GQ']['rosters'][j]['M_s_doubled'] = 2 * ms
        return f
    check('A57_GQ_DDO_ROSTER_AT_M_S_64_RECORD_DEFECT', run_eval(out, 'r6gq64', mutate=gq_ms(0, 64)), 'NO_RUN', ids=('A57',),
          extra=lambda e: 'GQ_DDO_C2T_M_S_NOT_THE_A57_PRODUCTION_M_S' in e['gates']['GQ']['codes'])
    check('A57_GQ_NGC_ROSTER_AT_M_S_128_RECORD_DEFECT', run_eval(out, 'r6gqngc', mutate=gq_ms(3, 128)), 'NO_RUN', ids=('A57',),
          extra=lambda e: 'GQ_NGC_T120L_M_S_NOT_THE_A57_PRODUCTION_M_S' in e['gates']['GQ']['codes'])
    check('A57_RI06_LO_CERTIFICATE_SOURCE_M_S_64_RECORD_DEFECT', run_eval(out, 'r6lo64', mutate=lambda r: r['LO'].update(source_gas_M_s=64)),
          'NO_RUN', ids=('A57', 'A58.RI-06'), extra=lambda e: 'LO_SOURCE_GAS_M_S_NOT_THE_A57_PRODUCTION_M_S' in e['gates']['LO']['codes'])
    # ================================================================ A58 RI-03 / RI-06 / RI-17
    check('A58_RI03_DOUBLING_ONLY_AT_K_BIG_128_RECORD_DEFECT', run_eval(out, 'r6dbl1', mutate=lambda r: r['DOUBLING'].update(ddo_K_big_inverse_kpc=[128.0])),
          'NO_RUN', ids=('A58.RI-03',), extra=lambda e: 'DOUBLING_NOT_AT_K_BIG_P_AND_2P_RI03' in e['gates']['DOUBLING']['codes'])
    check('A58_RI03_DOUBLING_AT_GAS_M_S_64_RECORD_DEFECT', run_eval(out, 'r6dbl2', mutate=lambda r: r['DOUBLING'].update(ddo_gas_M_s=64)),
          'NO_RUN', ids=('A58.RI-03',), extra=lambda e: 'DOUBLING_GAS_M_S_NOT_THE_A57_PRODUCTION_M_S_RI03' in e['gates']['DOUBLING']['codes'])

    def lo_drop(rg):
        def f(r):
            r['LO']['shells'] = [x for x in r['LO']['shells'] if x['range_inverse_kpc'] != list(rg)]
        return f
    check('A58_RI06_LO_PARTITION_SHELL_128_256_ABSENT_RECORD_DEFECT', run_eval(out, 'r6lop', mutate=lo_drop((128, 256))), 'NO_RUN',
          ids=('A58.RI-06',), extra=lambda e: 'LO_SHELL_128_256_ABSENT' in e['gates']['LO']['codes'])

    def lo_r5_shape(r):
        r['LO']['shells'] = [{'range_inverse_kpc': list(x), 'max_over_tau': 0.001} for x in M.LO_RANGES_R1 + ((64, 128), (128, 363))]
    check('A58_RI06_LO_NOT_THE_REGISTERED_PARTITION_RECORD_DEFECT', run_eval(out, 'r6lor5', mutate=lo_r5_shape), 'NO_RUN', ids=('A58.RI-06',),
          extra=lambda e: 'LO_SHELL_256_363_ABSENT' in e['gates']['LO']['codes'])
    check('A58_RI17_EPS_NGC_COVERAGE_45_NUMERICS_UNCERTIFIED', run_eval(out, 'r6ngc45', mutate=lambda r: r['EPS']['coverage_inverse_kpc'].update(NGC=[2, 45])),
          'NUMERICS_UNCERTIFIED', ids=('A58.RI-17',), extra=lambda e: 'EPS_COVERAGE' in e['gates']['EPS']['codes'])
    check('A58_RI17_EPS_NGC_COVERAGE_46_ADOPT', run_eval(out, 'r6ngc46'), 'ADOPT_TAIL', ids=('A58.RI-17',),
          extra=lambda e: e['gates']['EPS']['status'] == 'PASS')
    # ================================================================ r5 recheck order N2, N3, N4 (root items; DECLARED behaviour)
    Rgh = base_runs()
    with_gap(Rgh['C4T-KHI'], gap_at=0)
    RPfl = rp_clean('T3_KHI', 'PICARD', Rgh, **{m: dict(slow) for m in M.PAIRS['T3_KHI']})
    check('R6_ORDER_N2_B4_GAP_BASE_MEMBERS_AT_THE_FLOOR_READ_UAIF_PROVISIONAL_ON_THE_GAP', run_eval(out, 'r6on2', R=Rgh, RP=RPfl),
          'UNDECIDABLE_AT_ITERATION_FLOOR', ids=('R6.order.N2', 'NEW-31'), extra=lambda e: e['decision']['provisional'] is True
          and any('A54 B4 pass-row gap on C4T-KHI' in x for x in e['decision']['provisional_on']),
          why='DECLARED (r5 behaviour kept; root rules UAIF or INCOMPLETE: NEW-31)')
    Rt2 = base_runs(**{'C4T-D5': remake('C4T-D5', **slow)})

    def t2i_fail(r):
        r['T2I']['max_rel'] = 1e-10
    e = run_eval(out, 'r6on3', R=Rt2, RP=rp_clean('T2', 'PICARD', Rt2), b0_c5h=True, mutate=t2i_fail)
    t('R6_ORDER_N3a_T2I_FAIL_T2_UNDECIDABLE_MEMBERS_NAMED_NOT_REFUSED_READS_ID', e['decision']['outcome'] == 'IMPLEMENTATION_DEFECT'
      and e['tests']['T2']['status'] == 'NOT_READ', ids=('R6.order.N3', 'NEW-25'), got=e['decision'].get('outcome'))
    mg = out / 'MANIFEST_R6_NEW17_GATES_ONLY.json'
    mg.write_text(json.dumps(dict(man, rpair={'T3_KLO': {'branch': 'PICARD', 'members': {'C4T': str(root / 'nx1'), 'C4T-KLO': str(root / 'nx2')}}})))
    with _quiet():
        rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mg), '--case-block', str(out / 'CASE_BLOCK_PROBE.json'), '--outdir',
                     str(out / 'R6_NEW17_GATES_ONLY'), '--test-allow-unpinned-prereg', *REGARGS, '--gates-only'])
    t('R6_ORDER_N3b_GATES_ONLY_COMPUTES_NO_DECIDABILITY_NEW17_NOT_APPLIED', rc == 0 and (out / 'R6_NEW17_GATES_ONLY' / 'GATES_ONLY.json').is_file(),
      ids=('R6.order.N3', 'NEW-25'))
    Rra = base_runs(**{'C4T-D5': remake('C4T-D5', ea=0.2)})

    def b0_partial(r):
        for x in r['B0']['spec_sets']['EXT']:
            x.pop('projection_sha256', None)
    check('R6_ORDER_N4_PARTIAL_B0_EVIDENCE_IS_A_B0_RECORD_DEFECT_NO_RUN', run_eval(out, 'r6on4', R=Rra, RP=rp_clean('T2', 'ROUTE_A', Rra),
                                                                                   b0_c5h=True, mutate=b0_partial), 'NO_RUN', ids=('R6.order.N4',),
          extra=lambda e: e['gates']['B0']['status'] == 'RECORD_DEFECT')
    # ================================================================ r5 recheck validity F1: file-level links into the registered run
    decoy = root / 'r6decoy' / 'REGISTERED_DECOY_R6'
    decoy.mkdir(parents=True)
    (decoy / 'result.json').write_text(json.dumps({'canary': CANARY}))
    (decoy / 'finish.json').write_text(json.dumps({'canary': CANARY}))
    look = root / 'r6decoy' / 'C5H_LOOKALIKE'
    look.mkdir()
    (look / 'result.json').symlink_to((decoy / 'result.json').resolve())
    (look / 'finish.json').symlink_to((decoy / 'finish.json').resolve())
    mlook = out / 'MANIFEST_R6_DECOY_LOOKALIKE.json'
    mlook.write_text(json.dumps(dict(man, cases=dict(man['cases'], C5H=str(look)))))
    sv_dirs = M.C5H_REGISTERED_RUN_DIRS
    err = io.StringIO()
    try:
        M.C5H_REGISTERED_RUN_DIRS = (str(decoy.resolve()),)
        with OpenTrace() as tr, _quiet():
            _e, sys.stderr = sys.stderr, err
            try:
                rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mlook), '--case-block', str(out / 'CASE_BLOCK_PROBE.json'),
                             '--outdir', str(out / 'R6_DECOY_LOOKALIKE'), '--test-allow-unpinned-prereg', *REGARGS, '--no-packets'])
            finally:
                sys.stderr = _e
        ws = M.c5h_interlock(str(look))
        rr = M.read_run('C5H', str(look), dict(CTX, case_block=CB, interlock_side_paths=True), False)
    finally:
        M.C5H_REGISTERED_RUN_DIRS = sv_dirs
    dec_r = str(decoy.resolve())
    t('R6_VALIDITY_F1_FILE_LEVEL_SYMLINK_INTO_THE_REGISTERED_RUN_REFUSED_RC2_NOTHING_OPENED', rc == 2 and 'by realpath' in err.getvalue()
      and not (out / 'R6_DECOY_LOOKALIKE').exists() and not any(x.startswith(dec_r) for x in tr.paths) and bool(ws)
      and rr.get('unreadable') == 'RUN_FILE_INTO_THE_REGISTERED_C5H_RUN_REFUSED', ids=('R6.validity.F1',),
      opened=[x for x in tr.paths if x.startswith(dec_r)], err=err.getvalue()[-200:])
    stage = root / 'r6decoy' / 'C6T_FIELD_STAGE'
    stage.mkdir()
    (stage / 'finish.json').symlink_to((decoy / 'finish.json').resolve())
    cres = synthetic_completed_result(C4, numerics_for('C6T'), drv=V010, spec='c' * 64)
    cres['passes'][-1]['field'] = str(stage)
    dlook = write_run_dir(root / 'r6decoy', 'C6T_LOOKALIKE_FIELD', cres)
    mfield = out / 'MANIFEST_R6_DECOY_FIELD.json'
    mfield.write_text(json.dumps(dict(man, cases=dict(man['cases'], C6T=str(dlook)))))
    err = io.StringIO()
    try:
        M.C5H_REGISTERED_RUN_DIRS = (str(decoy.resolve()),)
        with _quiet():
            _e, sys.stderr = sys.stderr, err
            try:
                rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mfield), '--case-block', str(out / 'CASE_BLOCK_PROBE.json'),
                             '--outdir', str(out / 'R6_DECOY_FIELD'), '--test-allow-unpinned-prereg', *REGARGS, '--no-packets'])
            finally:
                sys.stderr = _e
        refused_n = M._GUARD['refused']
        active_after = M._GUARD['active']
        with open(str(stage / 'finish.json')) as fh:           # the guard is disarmed after main: an ordinary open works again
            ok_after = 'canary' in fh.read()
    finally:
        M.C5H_REGISTERED_RUN_DIRS = sv_dirs
    t('R6_VALIDITY_F1_AUDIT_HOOK_REFUSES_A_NESTED_FILE_LINK_THE_STRING_CHECKS_CANNOT_SEE_RC2', rc == 2 and 'interlock guard' in err.getvalue()
      and refused_n >= 1 and not (out / 'R6_DECOY_FIELD').exists() and active_after is False and ok_after, ids=('R6.validity.F1',),
      err=err.getvalue()[-200:], refused=refused_n)
    # ================================================================ r5 recheck validity F2 (NEW-30), F3, F7
    def three_fail(r):
        r['B3']['cases']['cube_O8']['value_rel'] = 1e-6
        r['EPS']['shells'][0]['refinements'] = 2
        r['T2I']['max_rel'] = 1e-10
    e = run_eval(out, 'r6vf2', mutate=three_fail)
    gf = e['decision']['named'].get('gates_failing_reported') or {}
    t('R6_VALIDITY_F2_NO_RUN_STILL_REPORTS_THE_FAILING_EPS_AND_T2I_GATES_WITH_NEXT_STEPS', e['decision']['outcome'] == 'NO_RUN'
      and {'B3', 'EPS', 'T2I'} <= set(gf) and gf['EPS']['next_step'] == M.NEXT_STEP['NUMERICS_UNCERTIFIED']
      and gf['T2I']['next_step'] == M.T2I_DEFECT_NEXT, ids=('R6.validity.F2', 'NEW-30'), got=sorted(gf))
    zi = identity_run('Z2', ro1_over={'inadmissible_record': {'refusal': 'x'}})
    ivz = M.identity_run_validity('Z2', zi, CTX)
    check('R6_VALIDITY_F3_T_CASE_RO1_INADMISSIBLE_RECORD_INVALID', run_eval(out, 'r6vf3', R=base_runs(
        **{'C4T': remake('C4T', ro1=dict(ro1b(), inadmissible_record={'refusal': 'x'}))})), 'INCOMPLETE', ids=('R6.validity.F3',),
        extra=lambda e: 'RO1_INADMISSIBLE_RECORD' in e['validity']['C4T']['V3_mismatch'])
    t('R6_VALIDITY_F3_ARMED_UNFIRED_Z2_WITH_INADMISSIBLE_RECORD_INVALID', 'RO1_INADMISSIBLE_RECORD' in ivz['ro1_codes'] and ivz['valid'] is False,
      ids=('R6.validity.F3',), codes=ivz['ro1_codes'])
    b1 = M._blind_str('x61. k412345678 q.7777777 x61.2222222', [])
    b2 = M._blind_str('B2_C2R3_SANITY_GT_0.05 2029f26a T2I_MAX_GT_1e-12 fs_columns_00:col0001:MASS_ENTHALPY_NOT_BRACKETED SRB_ROT_ROW_05_GT_TAU_OVER_10', [])
    t('R6_VALIDITY_F7_TRAILING_DOT_AND_LONG_DIGIT_RUNS_REDACTED_CODES_INTACT', '61' not in b1 and '412345678' not in b1 and '7777777' not in b1
      and b2 == 'B2_C2R3_SANITY_GT_0.05 2029f26a T2I_MAX_GT_1e-12 fs_columns_00:col0001:MASS_ENTHALPY_NOT_BRACKETED SRB_ROT_ROW_05_GT_TAU_OVER_10',
      ids=('R6.validity.F7',), b1=b1)
    # ================================================================ A56 follow-up 3; the pins of record
    t('A62_3_V010_R5_CHECK_PIN_PENDING_AND_R5_CUSTODY_PINS_VERIFIED_FROM_BYTES', M.PIN_V010_R5_CHECK is None   # [R7 renamed, A62.3]
      and all(hashlib.sha256(Path(p_).read_bytes()).hexdigest() == s_ for p_, s_ in list(M.PIN_RO1_CUSTODY.values()) + list(M.PIN_RO1_NODES_CUSTODY.values())
              + [M.PIN_DRIVER_V010_R5]) and not M.r5_custody_codes(),
      ids=('A56.FU3', 'A62.3'))


def ctx_with(extra_producers=None, registry='fixture', cb=None):
    """R7: a test context whose registry is the fixture registry plus extra {gate: [sha]} (or registry=None: no registry)."""
    c = dict(CTX, case_block=cb if cb is not None else CB)
    if registry is None:
        c['producer_registry'] = None
        return c
    obj = copy.deepcopy(REG_OBJ)
    for g_, shs in (extra_producers or {}).items():
        obj['producers'].setdefault(g_, []).extend(shs)
    c['producer_registry'] = M.producer_registry_from_obj(obj)
    return c


CERTS3 = Path(M.ART) / 'tail_scheme_impl_c2/certificates_v003'


def gq_part_counts(rec_):
    """R8 [A67 SF1] {geometry: full_domain.nodes} read from the gq_full part records a GQ record names (each part record's sha
    from bytes must equal the roster's part_record.sha256; label = the roster geometry).  TEST registration only."""
    out_ = {}
    for x in rec_['rosters']:
        pr = x.get('part_record')
        if not pr:
            continue
        b = Path(pr['path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == pr['sha256']
        part = json.loads(b)
        assert part['label'] == x['geometry']
        out_[part['label']] = part['full_domain']['nodes']
    return out_


def gq_v005_record_and_ctx(extra_records=()):
    """R8 [A67 SF2] the GQ record of record GQ_CERT_V005_MS128 (fbceefe6) and a TEST context registering its producer (and the
    V004 producer, the FAIL control) and the part-record production counts of every geometry either names (not a root registration)."""
    v5 = CERTS3 / 'gates/GQ_CERT_V005_MS128.json'
    v4 = CERTS3 / 'gates/GQ_CERT_V004_MS128.json'
    assert hashlib.sha256(v5.read_bytes()).hexdigest().startswith('fbceefe6')
    r5_, r4_ = json.loads(v5.read_bytes()), json.loads(v4.read_bytes())
    obj = copy.deepcopy(REG_OBJ)
    obj['producers']['GQ'] += [r5_['producer']['sha256'], r4_['producer']['sha256']]
    obj['gq_all_nodes_counts'].update(gq_part_counts(r5_))
    obj['gq_all_nodes_counts'].update(gq_part_counts(r4_))
    return r5_, dict(CTX, case_block=CB, producer_registry=M.producer_registry_from_obj(obj))


def eval_record(out, tag, gate, rec_, ctx):
    """Write one gate record under out/gates/r7/<tag>.json and evaluate it alone."""
    d = out / 'gates' / 'r7'
    d.mkdir(parents=True, exist_ok=True)
    p_ = d / ('%s.json' % tag)
    p_.write_text(json.dumps(rec_, indent=1))
    return M.evaluate_gate(gate, str(p_), ctx, {})


def r7_tests(out, root, man, cli, slow, rp_clean):
    """[R7] one test (or more) per A62 item the compare reads (A62.1-3) and per r6-recheck finding (order B1, N1-N4; validity
    SF1-SF4, N1-N3), the recheck probe worlds re-built as regression tests where feasible (ids 'A62.*', 'R7.*' in 'covers')."""
    cert = Path(M.ART) / 'tail_scheme_impl_c2/certificates_v002/gates'
    packet = Path(M.ART) / 'v007_launch_packet_cx1'
    # ================================================================ order B1: a present non-list pass row-set is S9, not a B4 gap
    ok_ps = driver_passes([dict(C4)] * 3)
    forms = {'DICT_OF_12': lambda ps: {r_['id']: r_ for r_ in ps[0]['rows']}, 'STRING': lambda ps: 'ROWS_LOST',
             'EMPTY_DICT': lambda ps: {}, 'WRAPPED': lambda ps: {'a': list(ps[0]['rows'])}, 'NUMBER': lambda ps: 0,
             'BOOL': lambda ps: False}
    unit = {}
    for nm, f in forms.items():
        ps = copy.deepcopy(ok_ps)
        ps[0]['rows'] = f(ps)
        unit[nm] = M.pass_rows_ids_code({'passes': ps}, IDS)
    gaps = {}
    for nm, edit in (('ABSENT', lambda p: p.pop('rows')), ('NULL', lambda p: p.__setitem__('rows', None)),
                     ('EMPTY_LIST', lambda p: p.__setitem__('rows', []))):
        ps = copy.deepcopy(ok_ps)
        edit(ps[0])
        gaps[nm] = (M.pass_rows_ids_code({'passes': ps}, IDS), M.pass_rows_gap({'passes': ps}))
    t('R7_ORDER_B1_UNIT_PRESENT_NON_LIST_ROW_SET_IS_S9_ABSENT_NULL_EMPTY_ARE_THE_B4_GAP',
      all(v == M.PASS_ROWS_S9 for v in unit.values()) and all(v == (None, 'PASS_WITHOUT_ROWS') for v in gaps.values()),
      ids=('R7.order.B1', 'A54.S9', 'A54.B4', 'NEW-34'), unit=unit, gaps=gaps)
    for nm in ('DICT_OF_12', 'STRING', 'EMPTY_DICT', 'WRAPPED'):       # the four probe worlds (probe_s9_shape_V001, C4T-KHI pass 1)
        Rk = base_runs()
        with_s9(Rk['C4T-KHI'], lambda ps, f=forms[nm]: ps[0].__setitem__('rows', f(ps)))
        check('R7_ORDER_B1_%s_ROW_SET_ON_C4T_KHI_RECORD_DEFECT_CASE_INCOMPLETE' % nm, run_eval(out, 'r7b1_' + nm.lower(), R=Rk),
              'INCOMPLETE', ids=('R7.order.B1', 'A54.S9'), extra=lambda e: e['decision']['subtype'] == 'CASES_OR_RECORDS'
              and M.PASS_ROWS_S9 in e['validity']['C4T-KHI']['V1_codes'] and e['validity']['C4T-KHI']['valid_all'] is False,
              why='r6 read the case valid (INCOMPLETE UNRESOLVED, a B4 gap)')
        Rk2 = base_runs()
        with_s9(Rk2['C4T-KHI'], lambda ps, f=forms[nm]: ps[0].__setitem__('rows', f(ps)))
        check('R7_ORDER_B1_%s_ROW_SET_WITH_A_VALID_T3_KHI_PICARD_RPAIR_STILL_INCOMPLETE_NOT_ADOPT' % nm,
              run_eval(out, 'r7b1rp_' + nm.lower(), R=Rk2, RP=rp_clean('T3_KHI', 'PICARD', Rk2)), 'INCOMPLETE',
              ids=('R7.order.B1', 'A54.S9'), extra=lambda e: e['decision']['subtype'] == 'CASES_OR_RECORDS'
              and M.PASS_ROWS_S9 in e['validity']['C4T-KHI']['V1_codes'],
              why='r6 read this world ADOPT_TAIL (the R-PAIR resolved the "gap")')
    graw = synthetic_completed_result(C4, numerics_for('C6T'), drv=V010, spec='c' * 64)
    graw['passes'][0]['rows'] = {r_['id']: r_ for r_ in graw['passes'][0]['rows']}
    dnl = write_run_dir(root, 'C6T_S9_ROWS_DICT', graw)
    rnl = M.read_run('C6T', str(dnl), dict(CTX, case_block=CB), True)
    vnl = M.case_validity('C6T', rnl, dict(CTX, case_block=CB), {'V4': True, 'V5': True}, None, None)
    t('R7_ORDER_B1_READ_RUN_ON_DISK_DICT_ROW_SET_S9_NO_PASS_ROWS_BUILT', rnl.get('pass_rows_s9') == M.PASS_ROWS_S9 and rnl['pass_rows'] == []
      and M.PASS_ROWS_S9 in vnl['V1_codes'] and vnl['V1'] is False, ids=('R7.order.B1', 'A54.S9'))
    zraw = synthetic_completed_result(C4, {'route_a': {'column_workers': 1}}, drv=sha('iddrvZ2'), spec=sha('idspecZ2'))
    zraw['passes'][1]['rows'] = 'ROWS_LOST'
    zraw['route_a_outcome']['ro1'] = ro1b(cw=1)
    dz = write_run_dir(root, 'Z2_S9_ROWS_STRING', zraw)
    rz = M.read_run('Z2', str(dz), dict(CTX, case_block=CB), True)
    ivz = M.identity_run_validity('Z2', rz, CTX)
    t('R7_ORDER_B1_IDENTITY_RUN_WITH_A_NON_LIST_ROW_SET_INVALID', rz.get('pass_rows_s9') == M.PASS_ROWS_S9 and ivz['valid'] is False
      and M.PASS_ROWS_S9 in ivz['codes'], ids=('R7.order.B1', 'A54.S9'), codes=ivz['codes'])
    # ================================================================ A62.1: RB_FP shell-domain coverage
    top = M.RB_FP_DOMAIN_FACTOR_OF_P * P_KBIG

    def rb(**kw):
        def f(r):
            r['RB_FP'].update(kw)
        return f
    for tag, mut, code in (
            ('PARTIAL_DECLARED', rb(full_tail_domain=False), 'RB_FP_PARTIAL_TAIL_DOMAIN_DECLARED_A62_1'),
            ('SHELLS_TO_6_ONLY', rb(shell_ranges_inverse_kpc=[[4, 5], [5, 6]]), 'RB_FP_SHELLS_DO_NOT_COVER_THE_TAIL_DOMAIN_A62_1'),
            ('GAP_8_TO_9', rb(shell_ranges_inverse_kpc=[[4, 8], [9, 182]]), 'RB_FP_SHELLS_DO_NOT_COVER_THE_TAIL_DOMAIN_A62_1'),
            ('STARTS_AT_5', rb(shell_ranges_inverse_kpc=[[5, 8], [8, 182]]), 'RB_FP_SHELLS_DO_NOT_COVER_THE_TAIL_DOMAIN_A62_1'),
            ('ENDS_AT_181', rb(shell_ranges_inverse_kpc=[[4, 8], [8, 181.0]]), 'RB_FP_SHELLS_DO_NOT_COVER_THE_TAIL_DOMAIN_A62_1'),
            ('OVERLAP', rb(shell_ranges_inverse_kpc=[[4, 10], [8, 182]]), 'RB_FP_SHELL_RANGES_OVERLAP_A62_1'),
            ('EXTRA_DV_KEY', lambda r: r['RB_FP']['dV_static_shells_km_s'].update({'32-64': [0.0] * 12}),
             'RB_FP_DV_KEYS_NOT_EXACTLY_THE_LISTED_SHELLS_A62_1'),
            ('RANGES_NOT_ALIGNED', rb(shell_ranges_inverse_kpc=[[4, 182]]), 'FIELD_TYPE_range2_list_aligned_with_shells:RB_FP:shell_ranges_inverse_kpc'),
            ('RANGES_ABSENT', lambda r: r['RB_FP'].pop('shell_ranges_inverse_kpc'), 'FIELD_MISSING:RB_FP:shell_ranges_inverse_kpc')):
        check('R7_A62_1_RB_FP_%s_RECORD_DEFECT_NO_RUN' % tag, run_eval(out, 'r7rb_' + tag.lower(), mutate=mut), 'NO_RUN',
              ids=('A62.1', 'R7.order.N4', 'R7.validity.N1'), extra=lambda e, c=code: e['gates']['RB_FP']['status'] == 'RECORD_DEFECT'
              and any(c in x for x in e['gates']['RB_FP']['codes']), why='r6 read a partial-domain RB_FP record PASS')
    check('R7_A62_1_RB_FP_SHELLS_ENDING_EXACTLY_AT_SQRT2_P_ADOPT', run_eval(out, 'r7rb_exact', mutate=rb(shell_ranges_inverse_kpc=[[4, 8], [8, top]])),
          'ADOPT_TAIL', ids=('A62.1',), extra=lambda e: e['gates']['RB_FP']['status'] == 'PASS')
    pk = json.loads((packet / 'SHELL_CONTRACT_C4T_SYNTHETIC_V001.json').read_bytes())     # Claude3 0059 item 1: the packet's C4T record
    cpk = ctx_with({'RB_FP': [pk['producer']['sha256']]})
    g_as_is = eval_record(out, 'rbfp_packet_as_is', 'RB_FP', pk, cpk)
    pk2 = dict(copy.deepcopy(pk), shell_ranges_inverse_kpc=[[4, 5], [5, 6]])                # its two shells, ranges from its labels
    g_rng = eval_record(out, 'rbfp_packet_ranges', 'RB_FP', pk2, cpk)
    t('R7_A62_1_REAL_PACKET_PARTIAL_DOMAIN_C4T_RB_FP_RECORD_NOT_PASS', g_as_is['status'] == 'RECORD_DEFECT'
      and any('shell_ranges_inverse_kpc' in c for c in g_as_is['codes']) and g_rng['status'] == 'RECORD_DEFECT'
      and 'RB_FP_PARTIAL_TAIL_DOMAIN_DECLARED_A62_1' in g_rng['codes'] and 'RB_FP_SHELLS_DO_NOT_COVER_THE_TAIL_DOMAIN_A62_1' in g_rng['codes'],
      ids=('A62.1', 'R7.validity.N1'), as_is=g_as_is['codes'][:3], ranges=g_rng['codes'][:4], why='r6 read this record PASS (TESTED, Claude3 0059)')
    # ================================================================ A62.2: producer shas root-registered
    sk = json.loads((packet / 'SR_K_CONTRACT_SYNTHETIC_V001.json').read_bytes())          # Claude3 0059 item 2: identical Delta across K
    g_sk = eval_record(out, 'srk_packet', 'SR_K', sk, ctx_with())
    same = sk['Delta_km_s']['2'] == sk['Delta_km_s']['3'] == sk['Delta_km_s']['4']
    t('R7_A62_2_REAL_PACKET_SYNTHETIC_SR_K_RECORD_REFUSED_AS_UNREGISTERED', same and g_sk['status'] == 'RECORD_DEFECT'
      and 'PRODUCER_NOT_ROOT_REGISTERED_A62_2:SR_K' in g_sk['codes'], ids=('A62.2', 'R7.validity.N1'), codes=g_sk['codes'][:3],
      why='r6 read this record PASS (identical Delta across K biases the T1-fail split)')
    check('R7_A62_2_SR_K_FIXTURE_PRODUCER_NOT_REGISTERED_NO_RUN', run_eval(out, 'r7srk', mutate=lambda r: r['SR_K']['producer'].update(
        path='/synthetic/tool_SR_K_fixture.py', sha256=sha('fixture SR_K'))), 'NO_RUN', ids=('A62.2',),
        extra=lambda e: 'PRODUCER_NOT_ROOT_REGISTERED_A62_2:SR_K' in e['gates']['SR_K']['codes'])
    R0, IDR0 = base_runs(), {n: identity_run(n) for n in M.IDENTITY_RUNS}
    recs = complete_records(R0, IDR0)
    rsha = M.runs_sha_map(R0, IDR0)
    bad = []
    for g_, r_ in recs.items():
        r2 = copy.deepcopy(r_)
        r2['producer']['sha256'] = sha('unregistered ' + g_)
        ev_ = eval_record(out, 'unreg_' + g_, g_, r2, ctx_with())
        ev0 = eval_record(out, 'noreg_' + g_, g_, r_, ctx_with(registry=None))
        if not (ev_['status'] == 'RECORD_DEFECT' and 'PRODUCER_NOT_ROOT_REGISTERED_A62_2:%s' % g_ in ev_['codes']
                and ev0['status'] == 'RECORD_DEFECT' and 'PRODUCER_REGISTRY_ABSENT_A62_2:%s' % g_ in ev0['codes']):
            bad.append(g_)
    t('R7_A62_2_EVERY_GATE_UNREGISTERED_PRODUCER_OR_NO_REGISTRY_IS_A_RECORD_DEFECT', not bad and len(recs) == len(M.ALL_GATES),
      ids=('A62.2', 'NEW-42'), bad=bad)
    e = run_eval(out, 'r7noreg', ctx_over={'producer_registry': None})
    t('R7_A62_2_NO_REGISTRY_FULL_READING_NO_RUN', e['decision']['outcome'] == 'NO_RUN'
      and all(e['gates'][g_]['status'] == 'RECORD_DEFECT' for g_ in M.ALL_GATES), ids=('A62.2',), got=e['decision']['outcome'])
    rbad = {}
    for nm, obj in (('UNKNOWN_KEY', dict(REG_OBJ, extra=1)), ('UNKNOWN_GATE', dict(REG_OBJ, producers=dict(REG_OBJ['producers'], X9=[sha('x')]))),
                    ('NOT_SHA', dict(REG_OBJ, identity_comparators=['abc'])), ('SCHEMA', dict(REG_OBJ, schema='OTHER')),
                    ('TOKENS_GATE', dict(REG_OBJ, identity_tokens={'EPS': [sha('t')]}))):
        try:
            M.producer_registry_from_obj(obj)
            rbad[nm] = False
        except M.Refused:
            rbad[nm] = True
    dupf = out / 'REGISTRY_DUPLICATE_KEY.json'
    dupf.write_text(json.dumps(REG_OBJ)[:-1] + ', "note": "x"}')
    try:
        M.load_producer_registry(str(dupf))
        rbad['DUPLICATE_KEY'] = False
    except M.Refused:
        rbad['DUPLICATE_KEY'] = True
    try:
        M.load_producer_registry(str(out / 'PRODUCER_REGISTRY_TEST.json'), expected_sha='0' * 64)
        rbad['PINNED_SHA_MISMATCH'] = False
    except M.Refused:
        rbad['PINNED_SHA_MISMATCH'] = True
    t('R7_A62_2_MALFORMED_OR_MISPINNED_REGISTRY_REFUSED', all(rbad.values()), ids=('A62.2',), got=rbad)
    Rp = {'C4T': {'result_sha256': hashlib.sha256(Path(CT + '/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/result.json').read_bytes()).hexdigest()},
          'C5H': {'result_sha256': hashlib.sha256(Path(CT + '/runs_ext/KMAX_A2F10_C5R3_RUN_V001/result.json').read_bytes()).hexdigest()}}
    for lab_, k in (('C2T', 'C2R3'), ('C3T', 'C3R3')):
        Rp[lab_] = {'result_sha256': hashlib.sha256(Path(M.PIN_R3[k][0]).read_bytes()).hexdigest()}
    Rp.update({c_: {} for c_ in M.T_CASES if c_ not in Rp})
    gp = write_records(out, 'r7_gates_only_noreg', complete_records(Rp, {n: {} for n in M.IDENTITY_RUNS}))
    mpn = out / 'MANIFEST_R7_GATES_NOREG.json'
    mpn.write_text(json.dumps(dict(man, gates=gp)))
    p = subprocess.run([PY, '-I', '-B', str(CMP), '--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mpn), '--case-block', str(out / 'CASE_BLOCK_PROBE.json'),
                        '--outdir', str(out / 'R7_GATES_ONLY_NO_REGISTRY'), '--test-allow-unpinned-prereg', '--gates-only'], capture_output=True, text=True)
    body = json.loads((out / 'R7_GATES_ONLY_NO_REGISTRY' / 'GATES_ONLY.json').read_text()) if p.returncode == 0 else {}
    p2 = cli('R7_GATES_ONLY_WITH_TEST_REGISTRY', '--gates-only', manifest=mpn)
    body2 = json.loads((out / 'R7_GATES_ONLY_WITH_TEST_REGISTRY' / 'GATES_ONLY.json').read_text()) if p2.returncode == 0 else {}
    t('R7_A62_2_CLI_GATES_ONLY_WITHOUT_A_REGISTRY_EVERY_GATE_RECORD_DEFECT_WITH_ONE_PASS', p.returncode == 0 and body
      and all(x['status'] == 'RECORD_DEFECT' for x in body['gates'].values()) and p2.returncode == 0
      and all(x['status'] == 'PASS' for x in body2['gates'].values()), ids=('A62.2',), rc=(p.returncode, p2.returncode), stderr=p.stderr[-200:])
    saved = (M.V007_PREREG_SHA256, M.PIN_ADDENDUM_V005, M.PIN_V010_R5_CHECK)
    errs = {}
    try:
        M.V007_PREREG_SHA256 = hashlib.sha256(Path(M.PIN_DRAFT_R1[0]).read_bytes()).hexdigest()
        M.PIN_ADDENDUM_V005 = hashlib.sha256(Path(M.ADDENDUM_V005_CITED).read_bytes()).hexdigest()
        M.PIN_V010_R5_CHECK = 'TEST_ONLY_IN_PROCESS'
        for nm, extra in (('NO_REGISTRY_PIN', []), ('TEST_REGISTRY_IN_SEALED_MODE', [])):
            err = io.StringIO()
            _e, sys.stderr = sys.stderr, err
            try:
                if nm == 'TEST_REGISTRY_IN_SEALED_MODE':
                    M.PIN_PRODUCER_REGISTRY = (str(out / 'PRODUCER_REGISTRY_TEST.json'),
                                               hashlib.sha256((out / 'PRODUCER_REGISTRY_TEST.json').read_bytes()).hexdigest())
                    extra = list(REGARGS)
                rc = M.main(['--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(out / 'MANIFEST_REAL_PROBE.json'), '--case-block',
                             str(out / 'CASE_BLOCK_PROBE.json'), '--outdir', str(out / ('R7_SEALED_' + nm))] + extra)
            finally:
                sys.stderr = _e
                M.PIN_PRODUCER_REGISTRY = None
            errs[nm] = (rc, err.getvalue()[-200:], (out / ('R7_SEALED_' + nm)).exists())
    finally:
        M.V007_PREREG_SHA256, M.PIN_ADDENDUM_V005, M.PIN_V010_R5_CHECK = saved
    t('R7_A62_2_SEALED_MODE_REFUSES_WITHOUT_THE_PINNED_REGISTRY_AND_REFUSES_A_TEST_REGISTRY', errs['NO_REGISTRY_PIN'][0] == 2
      and 'A62.2' in errs['NO_REGISTRY_PIN'][1] and errs['TEST_REGISTRY_IN_SEALED_MODE'][0] == 2
      and 'test-mode option' in errs['TEST_REGISTRY_IN_SEALED_MODE'][1] and not errs['NO_REGISTRY_PIN'][2]
      and not errs['TEST_REGISTRY_IN_SEALED_MODE'][2] and M.PIN_PRODUCER_REGISTRY is None, ids=('A62.2',), got=errs)
    # ================================================================ validity SF4 (b): identity gates bind comparator and tokens
    for g_ in M.IDENTITY_GATES:
        for part, code in (('comparator', '%s_COMPARATOR_NOT_ROOT_REGISTERED_A57_3' % g_), ('tokens', '%s_TOKENS_NOT_ROOT_REGISTERED_A59' % g_)):
            check('R7_SF4b_%s_%s_NOT_REGISTERED_RECORD_DEFECT_NO_RUN' % (g_.upper(), part.upper()),
                  run_eval(out, 'r7id_%s_%s' % (g_, part), mutate=lambda r, g_=g_, part=part: r[g_][part].update(sha256=sha('c2v003 append ' + part))),
                  'NO_RUN', ids=('R7.validity.SF4', 'A57.3', 'A59'), extra=lambda e, g_=g_, code=code: code in e['gates'][g_]['codes'],
                  why='r6 read no comparator or token field')
    zr = Path(M.ART) / 'tail_scheme_impl_c2/gates_v004/out/IDENTITY_C2V004_V001/IDENTITY_Z2_C2V004_V001.json'
    gz = M.evaluate_gate('B1', str(zr), ctx_with(), {})
    t('R7_SF4b_REAL_C2V004_IDENTITY_RECORD_IS_NOT_A_B1_GATE_RECORD_FAILS_CLOSED', gz['status'] == 'RECORD_DEFECT'
      and 'GATE_RECORD_SCHEMA:B1' in gz['codes'], ids=('R7.validity.SF4',), codes=gz['codes'][:3])
    # ================================================================ A62.3: custody pins at v010 r5
    cmap = json.loads(Path(M.PIN_R5_CASCADE_MAP[0]).read_bytes())['declared_sha_map']
    t('R7_A62_3_PINS_ARE_THE_R5_CASCADE_IMAGES_OF_THE_R4_SHAS_BINDING_UNCHANGED',
      cmap[M.R4_CUSTODY_SHAS['driver']] == M.PIN_DRIVER_V010_R5[1] == 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
      and cmap[M.R4_CUSTODY_SHAS['worker']] == M.PIN_RO1_CUSTODY['worker'][1] and M.PIN_RO1_CUSTODY['worker'][1].startswith('fbe9ae79')
      and cmap[M.R4_CUSTODY_SHAS['worker_parallel']] == M.PIN_RO1_CUSTODY['worker_parallel'][1] and M.PIN_RO1_CUSTODY['worker_parallel'][1].startswith('869ce387')
      and M.PIN_RO1_NODES_CUSTODY['worker'][1].startswith('0ae245d8') and M.PIN_RO1_NODES_CUSTODY['worker_parallel'][1].startswith('a5277172')
      and M.PIN_RO1_CUSTODY['binding'][1].startswith('86af6198') and M.PIN_RO1_CUSTODY['binding'][1] not in cmap and not M.r5_custody_codes(),
      ids=('A62.3', 'NEW-39'))
    sv = dict(M.R4_CUSTODY_SHAS)
    try:
        M.R4_CUSTODY_SHAS['worker'] = '0' * 64
        try:
            M.build_context()
            ref = None
        except M.Refused as exc:
            ref = str(exc)
    finally:
        M.R4_CUSTODY_SHAS.clear()
        M.R4_CUSTODY_SHAS.update(sv)
    t('R7_A62_3_A_PIN_THAT_IS_NOT_THE_CASCADE_IMAGE_REFUSES_AT_START', ref is not None and 'A62.3' in ref, ids=('A62.3',), got=ref)
    r4w = M.R4_CUSTODY_SHAS['worker_parallel']
    check('R7_A62_3_T_CASE_ON_THE_R4_RO1_WORKER_INVALID', run_eval(out, 'r7r4w', R=base_runs(**{'C4T': remake('C4T', ro1=dict(ro1b(), worker_sha256=r4w))})),
          'INCOMPLETE', ids=('A62.3',), extra=lambda e: 'RO1_WORKER_NOT_ON_CUSTODY_LIST' in e['validity']['C4T']['V3_mismatch'])
    r4n = M.R4_CUSTODY_SHAS['nodes_worker_parallel']
    check('R7_A62_3_C4TD5_ON_THE_R4_NODES_WORKER_INVALID', run_eval(out, 'r7r4n', R=base_runs(**{'C4T-D5': remake('C4T-D5', ro1=dict(ro1b(nodes=True), worker_sha256=r4n))})),
          'INCOMPLETE', ids=('A62.3',), extra=lambda e: 'RO1_WORKER_NOT_ON_CUSTODY_LIST' in e['validity']['C4T-D5']['V3_mismatch'])

    def r4_driver(cb):
        cb['cases']['C2T']['drivers_allowed'] = [M.R4_CUSTODY_SHAS['driver']]
    why = M.validate_case_block(case_block(over=r4_driver))
    t('R7_A62_3_CASE_BLOCK_T_CASE_DRIVERS_ALLOWED_NOT_V010_R5_REFUSED', any('A62.3' in w and w.startswith('C2T') for w in why)
      and not M.validate_case_block(CB), ids=('A62.3', 'A58.RI-01'), why=why[:2])
    check('R7_A62_3_I4_ON_THE_R4_DRIVER_RECORD_DEFECT', run_eval(out, 'r7i4', mutate=lambda r: r['I4'].update(driver_sha256=M.R4_CUSTODY_SHAS['driver'])),
          'NO_RUN', ids=('A62.3', 'A47.I4'), extra=lambda e: 'I4_DRIVER_NOT_REGISTERED_FOR_EVERY_T_CASE' in e['gates']['I4']['codes'])
    # ================================================================ validity SF1: GQ named rosters reach their case's K_big
    def gq_reach(j, hi):
        def f(r):
            r['GQ']['rosters'][j]['k_range_inverse_kpc'] = [2, hi]
        return f
    for j, nm in ((0, 'DDO_C2T'), (1, 'DDO_C3T')):
        check('R7_SF1_%s_REACH_32_THE_P32_INSTANCE_NUMERICS_UNCERTIFIED_AT_P128' % nm, run_eval(out, 'r7sf1_%d' % j, mutate=gq_reach(j, 32.0)),
              'NUMERICS_UNCERTIFIED', ids=('R7.validity.SF1', 'RA7'), extra=lambda e, nm=nm: 'GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT:%s' % nm in e['gates']['GQ']['codes'],
              why='r6 read this record PASS (GQ_REQUIRED DDO_C2T/DDO_C3T 32)')
    check('R7_SF1_C3T_REACH_EXACTLY_ITS_REGISTERED_K_BIG_ADOPT', run_eval(out, 'r7sf1_ok', mutate=gq_reach(1, 128.0)), 'ADOPT_TAIL',
          ids=('R7.validity.SF1',))
    gq_real = json.loads((cert / 'GQ_CERT_V003_KB256_MS128.json').read_bytes())
    cgq = ctx_with({'GQ': [gq_real['producer']['sha256']]})

    def gq_aug(rec_, cut=None, kperp=None, stand_in=True):
        r_ = copy.deepcopy(rec_)
        for x in r_['rosters']:
            if x['roster'] != 'NGC_T120L' and stand_in:
                x['all_nodes'] = {'max_abs_diff_over_P0': x['max_abs_diff_over_P0'], 'nodes': x['nodes']}     # sample stands in (TEST)
            if cut and x['roster'] in ('DDO_C2T', 'DDO_C3T'):
                x['k_range_inverse_kpc'] = [x['k_range_inverse_kpc'][0], cut]
            if kperp is not None:
                x['all_kperp_nodes_bound_over_P0'] = kperp
        return r_
    # [R8 renamed, A67 SF1/SF2: the r7 sample stand-in for all_nodes now refuses; probe G9 is re-based on the GQ record of record
    # GQ_CERT_V005_MS128, which carries real all_nodes blocks, under a TEST registry of its producer and part-record counts]
    gq5, c5 = gq_v005_record_and_ctx()
    g_ok = eval_record(out, 'gq_v005_as_is', 'GQ', gq5, c5)
    g_cut = eval_record(out, 'gq_v005_cut32', 'GQ', gq_aug(gq5, cut=32.0, stand_in=False), c5)
    t('R7_SF1_PROBE_G9_REAL_GQ_V005_ROSTERS_C2T_C3T_CUT_TO_32_NOT_PASS', g_ok['status'] == 'PASS' and g_cut['status'] == 'FAIL'
      and 'GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT:DDO_C2T' in g_cut['codes'] and 'GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT:DDO_C3T' in g_cut['codes'],
      ids=('R7.validity.SF1', 'A67.SF2'), ok=g_ok['codes'][:3], cut=g_cut['codes'][:4], why='r6 read the cut record PASS (probe G9)')
    # ================================================================ validity SF2: A57.1 all nodes
    def gq_all(j, **kw):
        def f(r):
            r['GQ']['rosters'][j]['all_nodes'].update(kw)
        return f
    check('R7_SF2_DDO_ROSTER_ALL_NODES_ABOVE_1e-12_NUMERICS_UNCERTIFIED', run_eval(out, 'r7sf2a', mutate=gq_all(2, max_abs_diff_over_P0=2e-12)),
          'NUMERICS_UNCERTIFIED', ids=('R7.validity.SF2', 'A57.1'), extra=lambda e: 'UV_TAIL_GAS_QUADRATURE_UNCERTIFIED:DDO_C4T:ALL_NODES' in e['gates']['GQ']['codes'])
    check('R7_SF2_DDO_ROSTER_ALL_NODES_COUNT_BELOW_THE_SAMPLE_RECORD_DEFECT', run_eval(out, 'r7sf2b', mutate=gq_all(0, nodes=100)), 'NO_RUN',
          ids=('R7.validity.SF2',), extra=lambda e: 'GQ_DDO_C2T_ALL_NODES_COUNT_BELOW_THE_SAMPLE_A57_1' in e['gates']['GQ']['codes'])
    check('R7_SF2_DDO_ROSTER_WITHOUT_ALL_NODES_RECORD_DEFECT', run_eval(out, 'r7sf2c', mutate=lambda r: r['GQ']['rosters'][1].pop('all_nodes')), 'NO_RUN',
          ids=('R7.validity.SF2',), extra=lambda e: any('FIELD_MISSING:GQ:rosters[1]:all_nodes' in c for c in e['gates']['GQ']['codes']))
    check('R7_SF2_ALL_KPERP_BOUND_ABOVE_1e-12_NUMERICS_UNCERTIFIED', run_eval(out, 'r7sf2d', mutate=lambda r: r['GQ']['rosters'][0].update(all_kperp_nodes_bound_over_P0=1e-3)),
          'NUMERICS_UNCERTIFIED', ids=('R7.validity.SF2',), extra=lambda e: 'UV_TAIL_GAS_QUADRATURE_UNCERTIFIED:DDO_C2T:ALL_KPERP_NODES' in e['gates']['GQ']['codes'])
    check('R7_SF2_NGC_ROSTER_NEEDS_NO_ALL_NODES_ADOPT', run_eval(out, 'r7sf2e'), 'ADOPT_TAIL', ids=('R7.validity.SF2',),
          extra=lambda e: e['gates']['GQ']['status'] == 'PASS')
    g_as = eval_record(out, 'gq_real_as_is', 'GQ', gq_real, cgq)
    g_kp = eval_record(out, 'gq_v005_kperp', 'GQ', gq_aug(gq5, kperp=1e-3, stand_in=False), c5)          # [R8 renamed: V005 base]
    t('R7_SF2_PROBES_G8_G10_REAL_GQ_KB256_AS_IS_AND_V005_WITH_A_FAILING_EVERY_KPERP_BOUND_NOT_PASS', g_as['status'] == 'RECORD_DEFECT'
      and any('all_nodes' in c for c in g_as['codes']) and g_kp['status'] == 'RECORD_DEFECT'
      and 'VERDICT_PASS_CONTRADICTS_DATA:GQ' in g_kp['codes'] and any(c.endswith(':ALL_KPERP_NODES') for c in g_kp['codes']),
      ids=('R7.validity.SF2', 'A57.1'), as_is=g_as['codes'][:2], kperp=g_kp['codes'][:3], why='r6 read both PASS (probes G8, G10)')
    # ================================================================ validity SF3: A57.4 the full envelope fields
    eps_rec = json.loads(Path(REAL_EPS_V006).read_bytes())
    g6 = eval_record(out, 'eps_real_as_is', 'EPS', eps_rec, ctx_with())
    rd6, _w6 = M.srb_rot_readable({'EPS': g6}, ctx_with())
    e5 = copy.deepcopy(eps_rec)
    j5 = next(k for k, s in enumerate(e5['shells']) if s['lo_inverse_kpc'] >= 5)
    e5['shells'][j5]['eps'] = e5['shells'][j5]['eps_envelope'] = 10 * e5['eps_max']
    g5 = eval_record(out, 'eps_real_g5', 'EPS', e5, ctx_with())
    t('R7_SF3_PROBE_G5_REAL_EPS_V006_SHELL_EPS_10X_EPS_MAX_RECORD_DEFECT_AS_IS_PASS', g6['status'] == 'PASS' and rd6
      and g5['status'] == 'RECORD_DEFECT' and 'EPS_MAX_BELOW_A_SHELL' in g5['codes'] and 'EPS_ENVELOPE_MAX_BELOW_A_SHELL_ENVELOPE_A57_4' in g5['codes'],
      ids=('R7.validity.SF3', 'A57.4'), as_is=g6['codes'][:2], g5=g5['codes'][:3], why='r6 read the G5 record PASS')

    def env(**kw):
        def f(r):
            r['EPS']['envelope_bound'].update(kw)
        return f
    check('R7_SF3_ENVELOPE_DOES_NOT_DOMINATE_SRB_ROT_NOT_READ_NO_ADOPT', run_eval(out, 'r7sf3a', mutate=env(dominates_actual_every_shell=False)),
          'INCOMPLETE', ids=('R7.validity.SF3', 'A57.4'), extra=lambda e: e['gates']['EPS']['status'] == 'PASS'
          and e['tests']['SRB_ROT']['status'] == 'NOT_READ')
    check('R7_SF3_DOMINATES_TRUE_BUT_ENVELOPE_MAX_BELOW_EPS_MAX_RECORD_DEFECT', run_eval(out, 'r7sf3b', mutate=env(eps_max_envelope_all_shells=1e-4)),
          'NO_RUN', ids=('R7.validity.SF3',), extra=lambda e: 'EPS_ENVELOPE_DOMINATES_FLAG_CONTRADICTS_THE_SHELLS_A57_4' in e['gates']['EPS']['codes'])

    def shell_env(r):
        r['EPS']['shells'][1].update(eps_envelope=4e-4, eps_actual_set=5e-4)
    check('R7_SF3_DOMINATES_TRUE_BUT_A_SHELL_ENVELOPE_BELOW_ITS_ACTUAL_RECORD_DEFECT', run_eval(out, 'r7sf3c', mutate=shell_env), 'NO_RUN',
          ids=('R7.validity.SF3',), extra=lambda e: 'EPS_ENVELOPE_DOMINATES_FLAG_CONTRADICTS_THE_SHELLS_A57_4' in e['gates']['EPS']['codes'])
    check('R7_SF3_ENVELOPE_PRESENT_WITHOUT_ITS_MAXIMUM_RECORD_DEFECT', run_eval(out, 'r7sf3d', mutate=lambda r: r['EPS']['envelope_bound'].pop('eps_max_envelope_all_shells')),
          'NO_RUN', ids=('R7.validity.SF3',), extra=lambda e: any('envelope_bound/eps_max_envelope_all_shells' in c for c in e['gates']['EPS']['codes']))

    def rbfp_env(r):
        r['EPS']['envelope_bound']['eps_max_envelope_all_shells'] = 8e-4
        r['RB_FP']['eps_max'] = 8e-4
    check('R7_SF3_NEW44_RB_FP_ON_THE_ENVELOPE_EPS_CROSSREF_MISMATCH_PINNED', run_eval(out, 'r7sf3e', mutate=rbfp_env), 'NO_RUN',
          ids=('R7.validity.SF3', 'NEW-44'), extra=lambda e: 'CROSSREF_MISMATCH:RB_FP:eps_max' in e['gates']['RB_FP']['codes'],
          why='DECLARED: RB_FP keeps EPS eps_max (A52.5); root to rule whether RB_FP is an envelope consumer (NEW-44)')
    # ================================================================ validity SF4 (a): the EPS shells cover the declared coverage
    e6 = copy.deepcopy(eps_rec)
    e6['shells'] = [s for s in e6['shells'] if s['hi_inverse_kpc'] <= 100]
    g6c = eval_record(out, 'eps_real_g6', 'EPS', e6, ctx_with())
    t('R7_SF4a_PROBE_G6_REAL_EPS_V006_SHELLS_CUT_TO_100_RECORD_DEFECT', len(e6['shells']) == 98 and g6c['status'] == 'RECORD_DEFECT'
      and 'EPS_SHELLS_DO_NOT_COVER_THE_DECLARED_COVERAGE' in g6c['codes'], ids=('R7.validity.SF4',), codes=g6c['codes'][:3],
      why='r6 read this record PASS (probe G6)')
    check('R7_SF4a_FIXTURE_EPS_SHELLS_TO_64_UNDER_A_DECLARED_363_RECORD_DEFECT', run_eval(out, 'r7sf4a', mutate=lambda r: r['EPS']['shells'].pop()),
          'NO_RUN', ids=('R7.validity.SF4',), extra=lambda e: 'EPS_SHELLS_DO_NOT_COVER_THE_DECLARED_COVERAGE' in e['gates']['EPS']['codes'])
    # ================================================================ NOTES carried (order N1-N3, validity N2, N3)
    t('R7_VALIDITY_N2_NEW47_GQ_DDO_EDGE_IS_THE_CYLINDER_K_BIG_2P', M.gq_ddo_edge(128.0) == 256.0 and abs(M.coverage_edge_2P(128.0) - 362.0387) < 1e-3,
      ids=('R7.validity.N2', 'NEW-38', 'NEW-47'))
    b3 = M._blind_str('PRODUCER_NOT_ROOT_REGISTERED_A62_2:SR_K RB_FP_SHELLS_DO_NOT_COVER_THE_TAIL_DOMAIN_A62_1 UV_TAIL_GAS_QUADRATURE_UNCERTIFIED:DDO_C4T:ALL_NODES', [])
    t('R7_VALIDITY_N3_NEW_CODES_CARRY_NO_RECORD_NUMBER_AND_SURVIVE_REDACTION', b3 == 'PRODUCER_NOT_ROOT_REGISTERED_A62_2:SR_K '
      'RB_FP_SHELLS_DO_NOT_COVER_THE_TAIL_DOMAIN_A62_1 UV_TAIL_GAS_QUADRATURE_UNCERTIFIED:DDO_C4T:ALL_NODES', ids=('R7.validity.N3', 'NEW-41'), b3=b3)
    zero2 = {i: C4[i] for i in IDS}
    one = dict(zero2)
    one[IDS[0]] = math.nextafter(zero2[IDS[0]], math.inf)
    En, cn, _d = M.picard_noise_detail({'pass_rows': [dict(zero2), dict(zero2), dict(zero2), one], 'adapted': {'rows': one}, 'pass_rows_gap': None}, IDS, TAU)
    t('R7_ORDER_N2_ONE_ULP_AFTER_TWO_EXACT_ZERO_INCREMENTS_E_UNAVAILABLE_PINNED', En is None and cn == M.E_UNAVAILABLE_NONCONTRACTING,
      ids=('R7.order.N2',), code=cn, why='DECLARED: the text has no float floor (deciding test on a real 12-pass member)')


def r8_tests(out, root, man, cli, slow, rp_clean):
    """[R8] one test (or more) per A67 item the compare reads (SF1, SF2, N1, N2, N3, N4, NEW-31, the float floor, order N1, the
    seal-time pins), the r7 recheck probe worlds re-built as regression tests where feasible (ids 'A67.*' in 'covers')."""
    packet = Path(M.ART) / 'v007_launch_packet_cx1'
    cert = Path(M.ART) / 'tail_scheme_impl_c2/certificates_v002/gates'
    gqc = lambda e: e['gates']['GQ']['codes']

    # ================================================================ A67 SF1: all-nodes counts are the root-registered production counts
    def gq_all(j, **kw):
        def f(r):
            r['GQ']['rosters'][j]['all_nodes'].update(kw)
        return f
    check('R8_A67_SF1_ALL_NODES_COUNT_EQUAL_TO_THE_4096_SAMPLE_REFUSES_NO_RUN', run_eval(out, 'r8sf1a', mutate=gq_all(0, nodes=4096)), 'NO_RUN',
          ids=('A67.SF1',), extra=lambda e: 'GQ_DDO_C2T_ALL_NODES_COUNT_EQUALS_THE_4096_SAMPLE_A67_SF1' in gqc(e)
          and 'GQ_DDO_C2T_ALL_NODES_COUNT_NOT_THE_ROOT_REGISTERED_PRODUCTION_COUNT_A67_SF1' in gqc(e),
          why='r7 accepted nodes >= 4096, the sample itself (r7 recheck validity SF1)')
    check('R8_A67_SF1_ALL_NODES_COUNT_NOT_THE_REGISTERED_PRODUCTION_COUNT_NO_RUN',
          run_eval(out, 'r8sf1b', mutate=gq_all(1, nodes=GQ_GEOMETRY['DDO_C3T'][1] - 1)), 'NO_RUN', ids=('A67.SF1',),
          extra=lambda e: 'GQ_DDO_C3T_ALL_NODES_COUNT_NOT_THE_ROOT_REGISTERED_PRODUCTION_COUNT_A67_SF1' in gqc(e))
    check('R8_A67_SF1_ALL_NODES_COUNT_ABOVE_THE_REGISTERED_COUNT_NO_RUN',
          run_eval(out, 'r8sf1b2', mutate=gq_all(2, nodes=GQ_GEOMETRY['DDO_C4T'][1] + 1)), 'NO_RUN', ids=('A67.SF1',),
          extra=lambda e: 'GQ_DDO_C4T_ALL_NODES_COUNT_NOT_THE_ROOT_REGISTERED_PRODUCTION_COUNT_A67_SF1' in gqc(e),
          why='equality, not a floor (stricter)')

    def geo(j, v):
        def f(r):
            r['GQ']['rosters'][j]['geometry'] = v
        return f
    e = run_eval(out, 'r8sf1c', mutate=geo(2, 'C4T_KB' + CANARY))
    bg = json.dumps(M.blinded_gate(e['gates']['GQ']))
    t('R8_A67_SF1_GEOMETRY_NOT_ROOT_REGISTERED_NO_RUN_AND_THE_LABEL_NEVER_EMITTED', e['decision']['outcome'] == 'NO_RUN'
      and 'GQ_DDO_C4T_GEOMETRY_NOT_ROOT_REGISTERED_A67_SF1' in gqc(e) and CANARY not in json.dumps(gqc(e)) and CANARY not in bg,
      ids=('A67.SF1', 'A54.S6'), codes=gqc(e)[:4])
    check('R8_A67_SF1_DDO_ROSTER_WITHOUT_GEOMETRY_RECORD_DEFECT', run_eval(out, 'r8sf1d', mutate=lambda r: r['GQ']['rosters'][0].pop('geometry')),
          'NO_RUN', ids=('A67.SF1',), extra=lambda e: any('FIELD_MISSING:GQ:rosters[0]:geometry' in c for c in gqc(e)))
    check('R8_A67_SF1_REGISTERED_PRODUCTION_COUNTS_ADOPT', run_eval(out, 'r8sf1e'), 'ADOPT_TAIL', ids=('A67.SF1',),
          extra=lambda e: e['gates']['GQ']['status'] == 'PASS')
    gq5, c5 = gq_v005_record_and_ctx()
    g4w = copy.deepcopy(gq5)                                     # the r7 recheck's G4 world: every all_nodes block = the 4096 sample
    for x in g4w['rosters']:
        if x['roster'] != 'NGC_T120L':
            x['all_nodes'] = dict(x['all_nodes'], nodes=x['nodes'], max_abs_diff_over_P0=x['max_abs_diff_over_P0'])
    gw = eval_record(out, 'r8_gq_v005_sample_as_all_nodes', 'GQ', g4w, c5)
    t('R8_A67_SF1_PROBE_G4_REAL_GQ_V005_WITH_THE_SAMPLE_AS_ALL_NODES_RECORD_DEFECT', gw['status'] == 'RECORD_DEFECT'
      and all('GQ_%s_ALL_NODES_COUNT_EQUALS_THE_4096_SAMPLE_A67_SF1' % n in gw['codes'] for n in ('DDO_C2T', 'DDO_C3T', 'DDO_C4T')),
      ids=('A67.SF1', 'R7.recheck.validity.SF1'), codes=gw['codes'][:4], why='r7 read this world PASS (TESTED, r7 recheck validity G4)')
    rbad = {}
    for nm, val in (('COUNT_4096', 4096), ('COUNT_100', 100), ('COUNT_BOOL', True), ('COUNT_FLOAT', 1.5e9), ('COUNT_STR', '1059379200')):
        obj = copy.deepcopy(REG_OBJ)
        obj['gq_all_nodes_counts']['C2T_KB128'] = val
        try:
            M.producer_registry_from_obj(obj)
            rbad[nm] = False
        except M.Refused:
            rbad[nm] = True
    obj = copy.deepcopy(REG_OBJ)
    obj.pop('gq_all_nodes_counts')
    try:
        M.producer_registry_from_obj(obj)
        rbad['KEY_ABSENT'] = False
    except M.Refused:
        rbad['KEY_ABSENT'] = True
    t('R8_A67_SF1_REGISTRY_REFUSES_A_COUNT_NOT_ABOVE_THE_SAMPLE_OR_NOT_AN_INT_OR_THE_KEY_ABSENT', all(rbad.values()), ids=('A67.SF1',), got=rbad)
    # ================================================================ A67 SF2: the GQ record of record V005 (PASS) and V004 (FAIL control)
    g5 = eval_record(out, 'r8_gq_v005_record_of_record', 'GQ', gq5, c5)
    gq4 = json.loads((CERTS3 / 'gates/GQ_CERT_V004_MS128.json').read_bytes())
    g4 = eval_record(out, 'r8_gq_v004_fail_control', 'GQ', gq4, c5)
    g5f = M.evaluate_gate('GQ', str(CERTS3 / 'gates/GQ_CERT_V005_MS128.json'), c5, {})
    t('R8_A67_SF2_REAL_GQ_V005_MS128_PASS_AND_V004_FAIL_DDO_C4T_SHORT', g5['status'] == 'PASS' and not g5['codes'] and g5f['status'] == 'PASS'
      and g5f['record']['sha256'].startswith('fbceefe6') and g4['status'] == 'FAIL'
      and 'GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT:DDO_C4T' in g4['codes'], ids=('A67.SF2', 'A67.SF1'), v5=g5['codes'][:3], v4=g4['codes'][:4])
    g5n = eval_record(out, 'r8_gq_v005_no_counts', 'GQ', gq5, ctx_with({'GQ': [gq5['producer']['sha256']]}))
    t('R8_A67_SF2_REAL_GQ_V005_WITHOUT_ITS_REGISTERED_COUNTS_RECORD_DEFECT', g5n['status'] == 'RECORD_DEFECT'
      and all('GQ_%s_GEOMETRY_NOT_ROOT_REGISTERED_A67_SF1' % n in g5n['codes'] for n in ('DDO_C2T', 'DDO_C3T', 'DDO_C4T', 'DDO_S4T', 'DDO_C6T')),
      ids=('A67.SF2', 'A67.SF1'), codes=g5n['codes'][:4],
      why='the fixture registry registers C2T_KB128 / C3T_KB128 / C4T_KB256 only: V005 names C2T_KB256, C3T_KB256, C4T_KB64/KB128, S4T, C6T too')
    # ================================================================ A67 N1: identity runs on the v010 r5 driver
    r4d = M.R4_CUSTODY_SHAS['driver']
    for n in M.IDENTITY_RUNS:
        IDR = {m: identity_run(m) for m in M.IDENTITY_RUNS}
        IDR[n]['result']['driver_sha256'] = r4d
        IDR[n]['receipt']['pins']['driver']['sha256'] = r4d
        check('R8_A67_N1_%s_ON_THE_R4_DRIVER_INVALID' % n.upper().replace('-', '_'), run_eval(out, 'r8n1_' + n, IDR=IDR), 'INCOMPLETE',
              ids=('A67.N1', 'A55.3'), extra=lambda e, n=n: M.IDENTITY_DRIVER_CODE in e['identity_runs'][n]['codes']
              and e['identity_runs'][n]['valid'] is False and not any(M.IDENTITY_DRIVER_CODE in e['identity_runs'][m]['codes'] for m in M.IDENTITY_RUNS if m != n),
              why='r7 read no identity-run driver (r7 recheck validity N1)')
    IDR = {m: identity_run(m) for m in M.IDENTITY_RUNS}
    IDR['Z2']['result'].pop('driver_sha256')
    IDR['Z2']['receipt']['pins']['driver']['sha256'] = None
    check('R8_A67_N1_Z2_WITHOUT_A_DRIVER_SHA_INVALID', run_eval(out, 'r8n1_nodrv', IDR=IDR), 'INCOMPLETE', ids=('A67.N1',),
          extra=lambda e: M.IDENTITY_DRIVER_CODE in e['identity_runs']['Z2']['codes'])
    check('R8_A67_N1_IDENTITY_RUNS_ON_V010_R5_ADOPT', run_eval(out, 'r8n1_ok'), 'ADOPT_TAIL', ids=('A67.N1',),
          extra=lambda e: all(e['identity_runs'][m]['valid'] for m in M.IDENTITY_RUNS) and M.PIN_DRIVER_V010_R5[1].startswith('b5cc62af'))
    # ================================================================ A67 N2: gate-record shas of record; SR_K identical Delta
    t12 = [TAU[i] for i in IDS]
    L = [0.011 * x for x in t12]
    check('R8_A67_N2_SR_K_DELTA_BITWISE_IDENTICAL_ACROSS_ALL_THREE_K_RECORD_DEFECT_NO_RUN',
          run_eval(out, 'r8n2a', mutate=lambda r: r['SR_K'].update(Delta_km_s={'2': list(L), '3': list(L), '4': list(L)})), 'NO_RUN',
          ids=('A67.N2',), extra=lambda e: all('SR_K_DELTA_BITWISE_IDENTICAL_ACROSS_K_%s_A67_N2' % k in e['gates']['SR_K']['codes'] for k in ('2_3', '2_4', '3_4')),
          why='r7 read an identical-Delta SR_K record PASS once its producer was registered (r7 recheck validity N2)')
    check('R8_A67_N2_SR_K_TWO_OF_THREE_DELTAS_IDENTICAL_RECORD_DEFECT_NO_RUN',
          run_eval(out, 'r8n2b', mutate=lambda r: r['SR_K']['Delta_km_s'].update({'3': list(r['SR_K']['Delta_km_s']['4'])})), 'NO_RUN',
          ids=('A67.N2', 'NEW-54'), extra=lambda e: e['gates']['SR_K']['codes'] == ['SR_K_DELTA_BITWISE_IDENTICAL_ACROSS_K_3_4_A67_N2'],
          why='DECLARED: any pair (stricter)')

    def one_ulp(r):
        d4 = list(r['SR_K']['Delta_km_s']['3'])
        d4[0] = math.nextafter(d4[0], math.inf)
        r['SR_K']['Delta_km_s']['4'] = d4
    check('R8_A67_N2_SR_K_DELTAS_ONE_ULP_APART_ARE_NOT_IDENTICAL_ADOPT', run_eval(out, 'r8n2c', mutate=one_ulp), 'ADOPT_TAIL', ids=('A67.N2',),
          extra=lambda e: e['gates']['SR_K']['status'] == 'PASS', why='bitwise means bitwise')
    check('R8_A67_N2_FIXTURE_SR_K_RECORD_OF_RECORD_REGISTERED_BY_SHA_ADOPT', run_eval(out, 'r8n2d', register_records=False), 'ADOPT_TAIL',
          ids=('A67.N2',), extra=lambda e: e['gates']['SR_K']['status'] == 'PASS')
    check('R8_A67_N2_SR_K_RECORD_NOT_A_REGISTERED_RECORD_OF_RECORD_NO_RUN',
          run_eval(out, 'r8n2e', register_records=False, mutate=lambda r: r['SR_K']['Delta_km_s']['2'].__setitem__(0, 0.0101 * t12[0])), 'NO_RUN',
          ids=('A67.N2',), extra=lambda e: 'GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:SR_K' in e['gates']['SR_K']['codes'],
          why='the producer sha is registered; the record bytes are not')
    pkf = packet / 'SR_K_CONTRACT_SYNTHETIC_V001.json'
    pk = json.loads(pkf.read_bytes())
    obj = copy.deepcopy(REG_OBJ)
    obj['producers']['SR_K'].append(pk['producer']['sha256'])
    obj['gate_records']['SR_K'].append(hashlib.sha256(pkf.read_bytes()).hexdigest())
    gpk = M.evaluate_gate('SR_K', str(pkf), dict(CTX, case_block=CB, producer_registry=M.producer_registry_from_obj(obj)), {})
    t('R8_A67_N2_REAL_PACKET_SR_K_WITH_ITS_PRODUCER_AND_RECORD_REGISTERED_STILL_RECORD_DEFECT_IDENTICAL_DELTA', gpk['status'] == 'RECORD_DEFECT'
      and 'SR_K_DELTA_BITWISE_IDENTICAL_ACROSS_K_2_3_A67_N2' in gpk['codes'] and not any('NOT_ROOT_REGISTERED' in c for c in gpk['codes']),
      ids=('A67.N2', 'R7.recheck.validity.N2'), codes=gpk['codes'][:4], why='the copied-sha world of the r7 recheck N2')
    R0, IDR0 = base_runs(), {n: identity_run(n) for n in M.IDENTITY_RUNS}
    recs = complete_records(R0, IDR0)
    bad = []
    for g_, r_ in recs.items():
        o1 = copy.deepcopy(REG_OBJ)
        o1['gate_records'][g_] = [sha('another record of ' + g_)]
        o2 = copy.deepcopy(REG_OBJ)
        o2['gate_records'].pop(g_)
        ev1 = eval_record(out, 'r8_grec_other_' + g_, g_, r_, dict(CTX, case_block=CB, producer_registry=M.producer_registry_from_obj(o1)))
        ev2 = eval_record(out, 'r8_grec_absent_' + g_, g_, r_, dict(CTX, case_block=CB, producer_registry=M.producer_registry_from_obj(o2)))
        code = 'GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:%s' % g_
        if not (ev1['status'] == 'RECORD_DEFECT' and code in ev1['codes'] and ev2['status'] == 'RECORD_DEFECT' and code in ev2['codes']):
            bad.append(g_)
    t('R8_A67_N2_EVERY_GATE_RECORD_NOT_REGISTERED_OR_ITS_GATE_ABSENT_FROM_GATE_RECORDS_IS_A_RECORD_DEFECT', not bad and len(recs) == len(M.ALL_GATES),
      ids=('A67.N2', 'NEW-52'), bad=bad)
    e = run_eval(out, 'r8n2f', register_records=False)
    t('R8_A67_N2_PRODUCED_AFTER_THE_SEAL_TOKEN_BINDS_BY_PRODUCER_ONLY_ADOPT', e['decision']['outcome'] == 'ADOPT_TAIL'
      and all(M.producer_registry_from_obj(REG_OBJ)['gate_records'][g_] == M.GATE_RECORD_AFTER_SEAL for g_ in M.ALL_GATES if g_ != 'SR_K'),
      ids=('A67.N2', 'NEW-52'), got=e['decision']['outcome'])
    rb2 = {}
    for nm, edit in (('SR_K_TOKEN', lambda o: o['gate_records'].__setitem__('SR_K', M.GATE_RECORD_AFTER_SEAL)),
                     ('OTHER_STRING', lambda o: o['gate_records'].__setitem__('EPS', 'LATER')),
                     ('UNKNOWN_GATE', lambda o: o['gate_records'].__setitem__('X9', [sha('x')])),
                     ('NOT_SHA', lambda o: o['gate_records'].__setitem__('EPS', ['abc'])),
                     ('KEY_ABSENT', lambda o: o.pop('gate_records')),
                     ('R7_SCHEMA_C2V001', lambda o: o.__setitem__('schema', 'UNT_KMAX_TAIL_V007_PRODUCER_REGISTRY_C2V001'))):
        o = copy.deepcopy(REG_OBJ)
        edit(o)
        try:
            M.producer_registry_from_obj(o)
            rb2[nm] = False
        except M.Refused:
            rb2[nm] = True
    t('R8_A67_N2_REGISTRY_REFUSES_THE_TOKEN_ON_SR_K_A_MALFORMED_GATE_RECORDS_OR_THE_R7_SCHEMA', all(rb2.values()), ids=('A67.N2',), got=rb2)
    Rp = {'C4T': {'result_sha256': hashlib.sha256(Path(CT + '/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/result.json').read_bytes()).hexdigest()},
          'C5H': {'result_sha256': hashlib.sha256(Path(CT + '/runs_ext/KMAX_A2F10_C5R3_RUN_V001/result.json').read_bytes()).hexdigest()}}
    for lab_, k in (('C2T', 'C2R3'), ('C3T', 'C3R3')):
        Rp[lab_] = {'result_sha256': hashlib.sha256(Path(M.PIN_R3[k][0]).read_bytes()).hexdigest()}
    Rp.update({c_: {} for c_ in M.T_CASES if c_ not in Rp})
    recs2 = complete_records(Rp, {n: {} for n in M.IDENTITY_RUNS})
    recs2['SR_K']['Delta_km_s']['2'][0] = 0.0101 * t12[0]
    gp = write_records(out, 'r8_gates_only_srk_unregistered', recs2)
    mpn = out / 'MANIFEST_R8_GATES_SRK_UNREGISTERED.json'
    mpn.write_text(json.dumps(dict(man, gates=gp)))
    p = cli('R8_GATES_ONLY_SRK_UNREGISTERED', '--gates-only', manifest=mpn)
    body = json.loads((out / 'R8_GATES_ONLY_SRK_UNREGISTERED' / 'GATES_ONLY.json').read_text()) if p.returncode == 0 else {}
    t('R8_A67_N2_CLI_GATES_ONLY_AN_UNREGISTERED_SR_K_RECORD_IS_A_RECORD_DEFECT_THE_OTHERS_PASS', p.returncode == 0 and body
      and body['gates']['SR_K']['status'] == 'RECORD_DEFECT' and 'GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:SR_K' in body['gates']['SR_K']['codes']
      and all(x['status'] == 'PASS' for g_, x in body['gates'].items() if g_ != 'SR_K'), ids=('A67.N2',), rc=p.returncode, stderr=p.stderr[-200:])
    # ================================================================ A67 N3: RB_FP shell ranges exactly [K, sqrt(2) x P]
    top = RB_FP_TOP

    def rbr(rng):
        def f(r):
            r['RB_FP']['shell_ranges_inverse_kpc'] = rng
        return f
    for tag, rng, code in (('2_TO_400', [[2, 8], [8, 400]], 'EXCEED'), ('R7_FIXTURE_TOP_182', [[4, 8], [8, 182]], 'EXCEED'),
                           ('START_3P5', [[3.5, 8], [8, top]], 'EXCEED'), ('TOP_ONE_ULP_ABOVE', [[4, 8], [8, math.nextafter(top, math.inf)]], 'EXCEED'),
                           ('TOP_ONE_ULP_BELOW', [[4, 8], [8, math.nextafter(top, 0.0)]], 'FALL_SHORT'),
                           ('START_4P5', [[4.5, 8], [8, top]], 'FALL_SHORT')):
        c_ = 'RB_FP_SHELL_RANGES_%s_K_TO_SQRT2_P_A67_N3' % ('EXCEED' if code == 'EXCEED' else 'FALL_SHORT_OF')
        check('R8_A67_N3_RB_FP_RANGES_%s_RECORD_DEFECT_NO_RUN' % tag, run_eval(out, 'r8n3_' + tag.lower(), mutate=rbr(rng)), 'NO_RUN',
              ids=('A67.N3',), extra=lambda e, c_=c_: e['gates']['RB_FP']['status'] == 'RECORD_DEFECT' and c_ in e['gates']['RB_FP']['codes'],
              why='r7 read an excess PASS (r7 recheck validity N3: [[2, 8], [8, 400]])' if code == 'EXCEED' else '')
    check('R8_A67_N3_RB_FP_RANGES_EXACTLY_4_TO_SQRT2_P_ADOPT', run_eval(out, 'r8n3_exact'), 'ADOPT_TAIL', ids=('A67.N3',),
          extra=lambda e: e['gates']['RB_FP']['status'] == 'PASS' and top == math.sqrt(2) * 128.0)
    # ================================================================ A67 N4: EPS top-level and nested envelope fields agree
    def eps_top(**kw):
        def f(r):
            r['EPS'].update(kw)
        return f
    epc = lambda e: e['gates']['EPS']['codes']
    check('R8_A67_N4_EPS_TOP_LEVEL_DOMINATES_FALSE_NESTED_TRUE_RECORD_DEFECT_NO_RUN',
          run_eval(out, 'r8n4a', mutate=eps_top(envelope_dominates_actual_every_shell=False)), 'NO_RUN', ids=('A67.N4', 'A54.S5'),
          extra=lambda e: 'EPS_TOP_LEVEL_DOMINATES_FLAG_DISAGREES_WITH_ENVELOPE_BOUND_A67_N4' in epc(e),
          why='r7 read only the nested flag (r7 recheck validity N4: PASS, SRB_ROT readable)')

    def top_true_nested_false(r):
        r['EPS']['envelope_dominates_actual_every_shell'] = True
        r['EPS']['envelope_bound']['dominates_actual_every_shell'] = False
    check('R8_A67_N4_EPS_TOP_LEVEL_DOMINATES_TRUE_NESTED_FALSE_RECORD_DEFECT_NO_RUN', run_eval(out, 'r8n4b', mutate=top_true_nested_false), 'NO_RUN',
          ids=('A67.N4',), extra=lambda e: 'EPS_TOP_LEVEL_DOMINATES_FLAG_DISAGREES_WITH_ENVELOPE_BOUND_A67_N4' in epc(e))
    check('R8_A67_N4_EPS_TOP_LEVEL_FIELDS_AGREE_ADOPT', run_eval(out, 'r8n4c', mutate=eps_top(envelope_dominates_actual_every_shell=True,
                                                                                                 eps_max_envelope_all_shells=6e-4)),
          'ADOPT_TAIL', ids=('A67.N4',), extra=lambda e: e['gates']['EPS']['status'] == 'PASS' and e['tests']['SRB_ROT']['status'] != 'NOT_READ')

    def top_without_block(r):
        r['EPS'].pop('envelope_bound')
        r['EPS']['envelope_dominates_actual_every_shell'] = True
    check('R8_A67_N4_EPS_TOP_LEVEL_FLAG_WITHOUT_ENVELOPE_BOUND_RECORD_DEFECT_NO_RUN', run_eval(out, 'r8n4d', mutate=top_without_block), 'NO_RUN',
          ids=('A67.N4',), extra=lambda e: 'EPS_TOP_LEVEL_DOMINATES_FLAG_WITHOUT_ENVELOPE_BOUND_A67_N4' in epc(e), why='DECLARED (stricter)')
    check('R8_A67_N4_EPS_TOP_LEVEL_ENVELOPE_MAX_DISAGREES_RECORD_DEFECT_NO_RUN',
          run_eval(out, 'r8n4e', mutate=eps_top(eps_max_envelope_all_shells=7e-4)), 'NO_RUN', ids=('A67.N4', 'NEW-53'),
          extra=lambda e: 'EPS_TOP_LEVEL_ENVELOPE_MAX_DISAGREES_WITH_ENVELOPE_BOUND_A67_N4' in epc(e), why='DECLARED (stricter): NEW-53')
    check('R8_A67_N4_EPS_TOP_LEVEL_FLAG_NOT_A_BOOL_RECORD_DEFECT', run_eval(out, 'r8n4f', mutate=eps_top(envelope_dominates_actual_every_shell='true')),
          'NO_RUN', ids=('A67.N4',), extra=lambda e: any('FIELD_TYPE_bool:EPS:envelope_dominates_actual_every_shell' in c for c in epc(e)))
    eps6 = json.loads(Path(REAL_EPS_V006).read_bytes())
    g6 = eval_record(out, 'r8_eps_v006_as_is', 'EPS', eps6, ctx_with())
    e6f = dict(copy.deepcopy(eps6), envelope_dominates_actual_every_shell=False)
    g6f = eval_record(out, 'r8_eps_v006_top_false', 'EPS', e6f, ctx_with())
    eps5 = json.loads((cert / 'EPS_CERT_V005.json').read_bytes())
    g5e = eval_record(out, 'r8_eps_v005_as_is', 'EPS', eps5, ctx_with({'EPS': [eps5['producer']['sha256']]}))
    t('R8_A67_N4_REAL_EPS_V006_AGREES_PASS_ITS_TOP_LEVEL_FLIPPED_DEFECT_AND_EPS_V005_TOP_LEVEL_ONLY_DEFECT', g6['status'] == 'PASS'
      and eps6['envelope_dominates_actual_every_shell'] is True and eps6['envelope_bound']['dominates_actual_every_shell'] is True
      and M.srb_rot_readable({'EPS': g6}, ctx_with())[0] and g6f['status'] == 'RECORD_DEFECT'
      and 'EPS_TOP_LEVEL_DOMINATES_FLAG_DISAGREES_WITH_ENVELOPE_BOUND_A67_N4' in g6f['codes'] and g5e['status'] == 'RECORD_DEFECT'
      and 'EPS_TOP_LEVEL_DOMINATES_FLAG_WITHOUT_ENVELOPE_BOUND_A67_N4' in g5e['codes'], ids=('A67.N4',),
      v6=g6['codes'][:2], v6f=g6f['codes'][:3], v5=g5e['codes'][:3])
    # ================================================================ A67 NEW-31 (accepted) and the float floor (UNTESTED, kept)
    Rgh = base_runs()
    with_gap(Rgh['C4T-KHI'], gap_at=0)
    RPfl = rp_clean('T3_KHI', 'PICARD', Rgh, **{m: dict(slow) for m in M.PAIRS['T3_KHI']})
    check('R8_A67_NEW31_ACCEPTED_C4T_KHI_B4_GAP_WITH_PICARD_MEMBERS_AT_THE_FLOOR_UAIF_PROVISIONAL_ADOPTS_NOTHING',
          run_eval(out, 'r8new31', R=Rgh, RP=RPfl), 'UNDECIDABLE_AT_ITERATION_FLOOR', ids=('A67.NEW-31', 'NEW-31'),
          extra=lambda e: e['decision']['provisional'] is True and any('A54 B4 pass-row gap on C4T-KHI' in x for x in e['decision']['provisional_on']),
          why='A67: accepted as implemented; undecidable, adopts nothing')
    zero2 = {i: C4[i] for i in IDS}
    one = dict(zero2)
    one[IDS[0]] = math.nextafter(zero2[IDS[0]], math.inf)
    En, cn, _d = M.picard_noise_detail({'pass_rows': [dict(zero2), dict(zero2), dict(zero2), one], 'adapted': {'rows': one}, 'pass_rows_gap': None}, IDS, TAU)
    t('R8_A67_FLOAT_FLOOR_KEPT_NO_FLOOR_ONE_ULP_AFTER_TWO_EXACT_ZERO_INCREMENTS_E_UNAVAILABLE', En is None and cn == M.E_UNAVAILABLE_NONCONTRACTING
      and not any('FLOAT_FLOOR' in k for k in dir(M)), ids=('A67.FLOAT_FLOOR', 'R7.order.N2'), code=cn,
      why='UNTESTED, kept (A67): the deciding test is the late-pass increments of the first real 12-pass member')
    # ================================================================ A67 order N1: the FIELDS text; the seal-time pins
    fp8 = out / 'FIELDS_R8_TEST.md'
    M.write_field_contract(str(fp8))
    ft = fp8.read_text()
    t('R8_A67_ORDER_N1_FIELDS_SAYS_AN_UNREGISTERED_RECORD_READS_NO_RUN_A48_AMB02', 'which reads NO_RUN (A48 AMB-02' in ft
      and "for the NO_RUN group and the gate's own reading otherwise" not in ft and ft.startswith('# FIELDS_R8.md'), ids=('A67.order.N1', 'AMB-02'))
    t('R8_FIELD_CONTRACT_CARRIES_THE_A67_RULINGS', all(x in ft for x in ('A67 SF1', 'A67 N1', 'A67 N2', 'A67 N3', 'A67 N4', 'gate_records',
                                                                     'gq_all_nodes_counts', 'rosters[].geometry', M.GATE_RECORD_AFTER_SEAL,
                                                                     'envelope_dominates_actual_every_shell', M.PRODUCER_REGISTRY_SCHEMA)),
      ids=('A67',))
    t('R8_A67_SEAL_TIME_PINS_STAY_NONE', M.PIN_ADDENDUM_V005 is None and M.PIN_V010_R5_CHECK is None and M.PIN_PRODUCER_REGISTRY is None
      and M.V007_PREREG_SHA256 is None and M.PRODUCER_REGISTRY_SCHEMA.endswith('C2V002'), ids=('A67.PINS',))


def _pat(doc_path):
    p = doc_path.split('[]')[0]
    p = re.sub(r'\{([^}]*)\}', lambda m: '(' + '|'.join(re.escape(x) for x in m.group(1).split(',')) + ')', p)
    return re.sub(r'<[^>]+>', '[^/]+', p)


def _leaf_paths(g, r):
    """(deletion path, expected code substring) for every key of the record: dict keys recursively; for lists of dicts, every
    key of the first element."""
    out = []

    def walk(o, path, where_list):
        if isinstance(o, dict):
            for k, v in o.items():
                p = path + [k]
                if where_list is None:
                    out.append((p, 'FIELD_MISSING:%s:%s' % (g, '/'.join(p))))
                else:
                    lp, j, inner = where_list
                    out.append((p, 'FIELD_MISSING:%s:%s[%d]:%s' % (g, '/'.join(lp), j, '/'.join(p[len(lp) + 1:]))))
                if isinstance(v, dict) and k not in ('maps',) and where_list is None:
                    walk(v, p, None)
                elif isinstance(v, list) and v and isinstance(v[0], dict) and where_list is None:
                    walk(v[0], p + [0], (p, 0, True))
    walk(r, [], None)
    return out


def _delete(o, path):
    for k in path[:-1]:
        o = o[k]
    del o[path[-1]]


def _find_numbers(o, where, acc):
    if isinstance(o, bool) or o is None or isinstance(o, str):
        return
    if isinstance(o, (int, float)):
        acc.append(where)
        return
    if isinstance(o, dict):
        for k, v in o.items():
            _find_numbers(v, where + '.' + str(k), acc)
    elif isinstance(o, list):
        for j, v in enumerate(o):
            _find_numbers(v, '%s[%d]' % (where, j), acc)


if __name__ == '__main__':
    sys.exit(main())
