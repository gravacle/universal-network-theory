"""Q4 canonical row-contract records, one per distinct DDO154 distance D (A134 Q4; Codex1 0141, 0152). Claude2, C2V001.

What lo_core_r5_cx2v001 (12d36305) produce_current_lo L225-231 matches each row-reference policy approval against:
review.row_contract_sha256 == ctx['details']['custody']['row_contract_sha256'], where ctx comes from the response producer
a1dcdea8 point_context -> custody_cx2v002 (6810b7c3) derive_details, which builds the row record at L119-128 and hashes it
at L139 (digest = sha256 of canonical JSON, L25-29).

Method (no production run; no run tree opened):
  A  the record is rebuilt with the pinned custody's own functions, statement for statement as L119-128:
     point_geometry (L93-101 -> driver r5 derive_geometry at float(D), inclination 66.0), cc.pin('prereg_v005'), read_pin,
     and the row_contract_sha256 is custody.digest(record).
  B  proof of byte equality: the real custody.derive_details runs on a spec built as the final-spec producer v004 builds it
     (A2F10 template a93c95b9 + run-config numerics.block + physical.distance_Mpc = D). One driver attribute is intercepted:
     uvt_static_pins (custody L129), because it hashes the A2F10 monitor pin under CLAUDE2/runs (hard rule). It feeds only
     modules_sha256, never the row record. derive_details' own row_contract must equal A byte for byte (custody.canonical),
     and its custody.row_contract_sha256 must equal A's digest.
  C  the same digest from the adapter c3v003 and the row producer v003 digest functions, and from hashlib directly; the
     row producer's row_reference() accepts the record on a synthetic call (its L116 digest check), and lo_core L69-72
     row_values checks are emulated (lo_core is hashed, never imported).
An audit hook refuses any open/listdir of a hard-rule path. Outputs are written by exclusive create only (--write).
"""
import copy
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

OUT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/q4_row_contracts_c2')
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
UPC = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
CPP = ART + '/calib_tail_readiness_cx2/certificates_per_point'

CUSTODY = (CPP + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377')
LO_CORE = (CPP + '/lo_core_r5_cx2v001.py', '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e')
RESPONSE = (CPP + '/point_response_producer_cx2v002.py', 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231')
LO_CONFIG = (CPP + '/lo_config_r5_cx2v001.py', '6654d93c0241afd230d90bfcf327f16c22dd24c4da1d3eea72602212c2b6ae5a')
ADAPTER = (ART + '/s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py',
           '211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c')
ROW_PRODUCER = (ART + '/s4_acceptance_c2/acceptance_q2/row_reference_producer_c2v003.py',
                '67fddd24945de31d70f940cb1ff85ef9d467b20d62a764cd159f58afc909e01e')
FINAL_SPEC_PRODUCER = (ART + '/step4_launch_readiness_c4/handoff_v004/tools/produce_final_step4_specs_c4v004.py',
                       'fcbf1c3ed175e1cfb3519c33324622a3b0ed190769e71b199687bd46dd1cb7ba')
PARAMS = (ART + '/sched_s45_c2/v003/DIRECT_BATCH_PARAMS_S45_C2V003A.json',
          '4adc296bcb0ddcd154ec0dcea820908ac525d1d39ce00d633eecc4d0c95f87e7')
PARAMS_A139 = (ART + '/sched_s45_c2/v003/DIRECT_BATCH_PARAMS_S45_C2V003.json',
               'b7fdaf100dc8329c4f873888a3f975b5cc0860ebcb7fbaa9dd795dc26cde2564')
RUN_CONFIG = (ART + '/sched_s45_c2/v003/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V003.json',
              'd9241676c3b7b32bd3067a55bdfb7821ebc33a68adbdc011ab4e4c58b6e50a4d')
COORD = (ART + '/calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json',
         '50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f')
ADDENDUM = (ART + '/calib_tail_readiness_cx2/COORDINATE_ADDENDUM_CX2V006.json',
            '9962b2aa673572a712d07fd74d12e61fe2418acbeb03b0ef3437118a6ca1e2b9')
REGION = (UPC + '/CODEX1/DDO154_CALIBRATION_OBSERVATION_REGION_V001.json',
          '13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d')
PREREG = (ART + '/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json',
          'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174')
SPEC_TEMPLATE_SHA = 'a93c95b95c1f112b7293ffd598371335227cb93d7334981be33e368c6cd9f52b'
HISTORICAL_D404 = (CPP + '/CUSTODY_KB064_C000_CX2V001.json',
                   '92b54db5dc6f365b169ef3d236bbc504ee6b315fd9e86447d52170d61b11db11')
RULINGS = (UPC + '/CLAUDE2/S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md',
           '56774ba7a1ad54be89cb1cbb6bd256333de4134ed9ef8a8e949898f7ed8c2c82')
REQUESTS = ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0141_2026-10-19_A134_ACK_reviews_row_contract_inputs.md',
            '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0152_2026-10-19_Q4_missing_contracts_deadline_warning.md')
LABELS = {'DLO': 'SENS lower distance (region reported68_low = coordinate box lower)',
          'D404': 'registered distance (anchor, HEADLINE, campaign, POST_S1)',
          'DHI': 'SENS upper distance (region reported68_high = coordinate box upper)'}

# ------------------------------------------------------------------------------------------------ hard-rule guard
FORBIDDEN_SUBSTR = ('/CLAUDE2/runs', 'UNT_INTERNAL_RUNS', '/Volumes/External1', '/.codex', 'c5h_hull_c2', 'runs_ext')
OPENED = []


def _forbidden(s):
    parts = s.split('/')
    return (any(f in s for f in FORBIDDEN_SUBSTR) or any(p.startswith('UVT_') for p in parts)
            or any('NGC3198' in p.upper() for p in parts) or s.rstrip('/').endswith('/CLAUDE2/runs'))


def _hook(event, args):
    if event not in ('open', 'os.listdir', 'os.scandir', 'os.walk', 'glob.glob'):
        return
    p = args[0] if args else None
    if isinstance(p, bytes):
        p = p.decode('utf-8', 'replace')
    if isinstance(p, os.PathLike):
        p = os.fspath(p)
    if not isinstance(p, str):
        return
    if _forbidden(p):
        raise PermissionError('HARD_RULE_FORBIDDEN_PATH: ' + p)
    if '/__pycache__/' in p and p.startswith('/Users/bgm/Research'):
        raise PermissionError('PYCACHE_READ_REFUSED (modules must execute their hashed source): ' + p)
    if p.startswith('/Users/bgm/Research') or p.startswith('/Volumes'):
        OPENED.append([event, p])


sys.addaudithook(_hook)
# Loaders that go through importlib (custody L59-63) must compile the hashed .py, never a cached .pyc beside it:
# with -B nothing is written, and this empty prefix makes the bytecode cache lookup miss.
sys.pycache_prefix = '/private/tmp/q4rc_c2v001_no_pycache'


class Stop(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Stop(msg)


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def read_exact(path, sha, label):
    raw = Path(path).read_bytes()
    need(sha_bytes(raw) == sha, 'PIN_MISMATCH %s %s' % (label, path))
    return raw


def load_json(path, sha, label):
    return json.loads(read_exact(path, sha, label))


def load_exact(path, sha, name):
    """Import by path: the executed bytes are the hashed bytes."""
    need(os.path.isabs(path) and os.path.realpath(path) == path, 'NONCANONICAL_MODULE_PATH ' + path)
    raw = read_exact(path, sha, name)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


class DriverProxy:
    """The real driver r5 module, except uvt_static_pins (custody L129), which hashes the A2F10 monitor pin under
    CLAUDE2/runs (driver L341-345, L1215-1223). That value enters modules_sha256 only, never the row record."""

    def __init__(self, real):
        self._real = real

    def __getattr__(self, k):
        return getattr(self._real, k)

    def uvt_static_pins(self, nodes=False):
        return {'SYNTHETIC_PROOF_CALL': 'uvt_static_pins intercepted; modules_sha256 of this call is not a production value'}


# ------------------------------------------------------------------------------------------------ step 1: the D set
def establish_d_set(checks):
    params = load_json(*PARAMS, 'direct batch params C2V003A')
    need(params.get('schema') == 'DIRECT_BATCH_PARAMS_S45_C2V003A', 'PARAMS_SCHEMA')
    sup = params.get('supersedes') or {}
    need([sup.get('path'), sup.get('sha256')] == list(PARAMS_A139), 'PARAMS_A_DOES_NOT_SUPERSEDE_A139_PARAMS')
    read_exact(*PARAMS_A139, 'direct batch params C2V003 (A139)')
    calls = []
    for batch, b in sorted(params['batches'].items()):
        t = b.get('template')
        if t is None:
            need(batch == 'POST_S1', 'TEMPLATE_MISSING ' + batch)
            for case in b['case_order']:
                calls.append({'batch': batch, 'case': case, 'distance_Mpc': None, 'tail_on': True,
                              'distance_source': 'POST_S1: no template; see campaign rule'})
            continue
        tpl = load_json(t['path'], t['sha256'], 'plan template ' + batch)
        need([c['case'] for c in tpl['calls']] == b['case_order'], 'TEMPLATE_CASE_ORDER ' + batch)
        need(len(tpl['calls']) == b['n_calls'], 'TEMPLATE_N_CALLS ' + batch)
        for c in tpl['calls']:
            need(isinstance(c['distance_Mpc'], float), 'TEMPLATE_D_NOT_FLOAT %s %s' % (batch, c['case']))
            calls.append({'batch': batch, 'case': c['case'], 'distance_Mpc': c['distance_Mpc'], 'tail_on': c['tail_on'],
                          'distance_source': {'path': t['path'], 'sha256': t['sha256'], 'field': 'calls[case=%s].distance_Mpc' % c['case']}})
    coord = load_json(*COORD, 'coordinate spec')
    add = load_json(*ADDENDUM, 'coordinate addendum')
    region = load_json(*REGION, 'observation region')
    rc = load_json(*RUN_CONFIG, 'run config')
    need(rc['coordinate_spec'] == {'path': COORD[0], 'sha256': COORD[1]}, 'RUN_CONFIG_COORD_PIN')
    need(rc['coordinate_spec_addendum'] == {'path': ADDENDUM[0], 'sha256': ADDENDUM[1]}, 'RUN_CONFIG_ADDENDUM_PIN')
    need(rc['observation_region'] == {'path': REGION[0], 'sha256': REGION[1]}, 'RUN_CONFIG_REGION_PIN')
    cm = add['coordinate_mode']
    need(cm['mode'] == 'DDO154_DISTANCE_FIXED_AT_REGISTERED' and cm['fixed_engine_coordinates'] == {'distance_Mpc': 4.04},
         'CAMPAIGN_D_NOT_FIXED_4.04')
    dc = [c for c in coord['engine_coordinates'] if c['name'] == 'distance_Mpc']
    need(len(dc) == 1, 'COORD_DISTANCE_ENTRY')
    dc = dc[0]
    lo, hi, trial = float(dc['lower']), float(dc['upper']), float(dc['trial_value'])
    ds = region['distance_summary']
    need(lo == ds['reported68_low_Mpc'] and hi == ds['reported68_high_Mpc'], 'REGION_BOX_MISMATCH')
    need(trial == 4.04 and rc['anchor']['physical']['distance_Mpc'] == 4.04, 'TRIAL_OR_ANCHOR_D')
    fsp = read_exact(*FINAL_SPEC_PRODUCER, 'final-spec producer v004')
    for frag in (b"d = float(self.by['distance_Mpc'][edge])", b"need(d == 4.04, 'HEADLINE_D_NOT_4.04 ' + nm)",
                 b"ph['distance_Mpc'] = th['distance_Mpc']", b"need(self.trial['distance_Mpc'] == 4.04, 'TRIAL_D_NOT_4.04')",
                 b"need((batch == 'SENS_LO') == (d < 4.04), 'SENS_BATCH_D ' + nm)"):
        need(frag in fsp, 'FINAL_SPEC_PRODUCER_FRAGMENT_MISSING ' + frag.decode())
    for c in calls:
        if c['batch'] == 'POST_S1':
            c['distance_Mpc'] = 4.04
            c['distance_source'] = ('DERIVED: POST_S1 is the S1 pair at the campaign point u_A (V006 A150/A160); the campaign '
                                    'coordinate mode fixes distance_Mpc = 4.04 for every campaign call spec (addendum 9962b2aa '
                                    'coordinate_mode.fixed_engine_coordinates; rule text). Params C2V003A carry no template.')
        if c['batch'] == 'HEADLINE':
            need(c['distance_Mpc'] == trial, 'HEADLINE_D')
        if c['batch'] == 'SENS_LO':
            need(c['distance_Mpc'] == lo, 'SENS_LO_D')
        if c['batch'] == 'SENS_HI':
            need(c['distance_Mpc'] == hi, 'SENS_HI_D')
    tail_on = [c for c in calls if c['tail_on']]
    need(len(tail_on) == 31, 'TAIL_ON_DIRECT_CALLS_NOT_31: %d' % len(tail_on))
    ds_set = sorted({c['distance_Mpc'] for c in tail_on} | {4.04})
    need(ds_set == [lo, trial, hi], 'D_SET %r' % ds_set)
    need(len(ds_set) == 3, 'D_SET_NOT_THREE')
    tail_off = sorted({c['distance_Mpc'] for c in calls if not c['tail_on']})
    need(set(tail_off) <= set(ds_set), 'TAIL_OFF_D_OUTSIDE_SET')
    checks['d_set'] = {'values': ds_set, 'hex': [x.hex() for x in ds_set], 'json': [json.dumps(x) for x in ds_set],
                       'tail_on_direct_calls': len(tail_on), 'tail_off_direct_D_subset': True}
    by_label = {'DLO': lo, 'D404': trial, 'DHI': hi}
    users = {k: [] for k in by_label}
    for c in calls:
        for k, v in by_label.items():
            if c['distance_Mpc'] == v:
                users[k].append({'batch': c['batch'], 'case': c['case'], 'tail_on': c['tail_on'],
                                 'distance_source': c['distance_source']})
    users['D404'].append({'batch': 'CAMPAIGN', 'case': 'every campaign point', 'tail_on': True,
                          'distance_source': {'path': ADDENDUM[0], 'sha256': ADDENDUM[1],
                                              'field': 'coordinate_mode.fixed_engine_coordinates.distance_Mpc'}})
    d_sources = {
        'DLO': [{'path': COORD[0], 'sha256': COORD[1], 'field': 'engine_coordinates[name=distance_Mpc].lower'},
                {'path': REGION[0], 'sha256': REGION[1], 'field': 'distance_summary.reported68_low_Mpc'},
                {'path': FINAL_SPEC_PRODUCER[0], 'sha256': FINAL_SPEC_PRODUCER[1],
                 'field': 'World.build_all L551-565: d = float(self.by[distance_Mpc][lower]) -> physical.distance_Mpc'}],
        'D404': [{'path': COORD[0], 'sha256': COORD[1], 'field': 'engine_coordinates[name=distance_Mpc].trial_value'},
                 {'path': ADDENDUM[0], 'sha256': ADDENDUM[1], 'field': 'coordinate_mode.fixed_engine_coordinates.distance_Mpc'},
                 {'path': RUN_CONFIG[0], 'sha256': RUN_CONFIG[1], 'field': 'anchor.physical.distance_Mpc'},
                 {'path': FINAL_SPEC_PRODUCER[0], 'sha256': FINAL_SPEC_PRODUCER[1],
                  'field': 'World.build_all L540-549 (template physical; mapper th[distance_Mpc] = trial) and L576-577 need(d == 4.04)'}],
        'DHI': [{'path': COORD[0], 'sha256': COORD[1], 'field': 'engine_coordinates[name=distance_Mpc].upper'},
                {'path': REGION[0], 'sha256': REGION[1], 'field': 'distance_summary.reported68_high_Mpc'},
                {'path': FINAL_SPEC_PRODUCER[0], 'sha256': FINAL_SPEC_PRODUCER[1],
                 'field': 'World.build_all L551-565: d = float(self.by[distance_Mpc][upper]) -> physical.distance_Mpc'}]}
    return by_label, users, d_sources, coord, rc, region


# ------------------------------------------------------------------------------------------------ step 2: records
def build(by_label, coord, rc, region, checks):
    CU = load_exact(CUSTODY[0], CUSTODY[1], 'q4rc_custody_cx2v002')
    for p, s, lab in (LO_CORE + ('lo_core',), RESPONSE + ('response producer',), LO_CONFIG + ('lo_config',),
                      RULINGS + ('A134 rulings',)):
        read_exact(p, s, lab)
    resp = Path(RESPONSE[0]).read_bytes()
    need(b"CUSTODY_PATH = HERE / 'custody_cx2v002.py'" in resp and CUSTODY[1].encode() in resp,
         'RESPONSE_PRODUCER_CUSTODY_NOT_6810B7C3 (lo_core ctx custody)')
    AD = load_exact(ADAPTER[0], ADAPTER[1], 'q4rc_adapter_c3v003')
    need(AD.CUSTODY == CUSTODY and AD.LO_CORE == LO_CORE, 'ADAPTER_PINS_DIFFER')
    RP = load_exact(ROW_PRODUCER[0], ROW_PRODUCER[1], 'q4rc_row_producer_c2v003')
    d, cc = CU.libraries()                                      # driver r5 b5cc62af + certs_common c75aaa5a, pinned by custody
    need(cc.PINS['prereg_v005'] == (Path(PREREG[0]), PREREG[1]), 'CC_PREREG_PIN')
    tpin = coord['call_spec_mapping']['template']
    need(tpin['sha256'] == SPEC_TEMPLATE_SHA, 'SPEC_TEMPLATE_PIN')
    template = load_json(tpin['path'], tpin['sha256'], 'A2F10 template')
    need(rc['anchor']['physical'] == template['physical'] and rc['anchor']['coefficients'] == template['coefficients'],
         'ANCHOR_NOT_TEMPLATE_POINT')
    base = copy.deepcopy(template)
    base['numerics'] = copy.deepcopy(rc['numerics']['block'])   # final-spec producer v004 World.__init__ L460-463
    prereg_raw = read_exact(*PREREG, 'prereg V005')
    prereg_obj = json.loads(prereg_raw)
    sig = {r['id']: r['quoted_random_sigma_km_s'] for r in region['rows']}
    by = {c['name']: c for c in coord['engine_coordinates']}
    eref = float(by['Eref_base_J']['trial_value'])
    out = {}
    for label, D in by_label.items():
        t0 = time.monotonic()
        spec = copy.deepcopy(base)
        if D != spec['physical']['distance_Mpc']:
            spec['physical'].update({'distance_Mpc': D})      # hand_spec L531-536 (SENS_DISTANCE family)
        need(type(spec['physical']['distance_Mpc']) is float and spec['physical']['distance_Mpc'] == D, 'SPEC_D ' + label)
        # A: custody L118-128, statement for statement, with the pinned functions
        profile, mono, binding, record = CU.point_geometry(spec, d)
        need(all(record['registered_formula_guards'].values()), 'GEOMETRY_GUARDS ' + label)
        prereg = CU.read_pin(cc.pin('prereg_v005'))
        rows = binding['query_rows']
        ids = [x['id'] for x in rows]
        need(ids == prereg['row_ids'] and len(set(ids)) == len(ids), 'ordered row contract mismatch')
        tau = prereg['tau_km_s']
        need(len(tau) == len(ids) and all(x > 0 for x in tau), 'invalid tau')
        row = {'schema': 'DDO154_POINT_ROWS_CX2V001', 'rows': rows, 'tau_km_s': tau,
               'distance_Mpc': spec['physical']['distance_Mpc'],
               'speed_reference_policy': 'PENDING_REVIEWED_LO_COVERAGE_OBJECT',
               'uncertainty_carrier_policy': 'PREREG_V005_TAU; CALIBRATION_CARRIER_PENDING_ROOT',
               'prereg': cc.pin('prereg_v005')}
        rc_sha = CU.digest(row)
        canon = CU.canonical(row)
        # B: the real derive_details (one intercepted attribute; see DriverProxy)
        real_lib = CU.libraries
        CU.libraries = lambda: (DriverProxy(d), cc)
        try:
            details = CU.derive_details(spec=spec)
        finally:
            CU.libraries = real_lib
        need(CU.canonical(details['row_contract']) == canon, 'DERIVE_DETAILS_ROW_CONTRACT_BYTES_DIFFER ' + label)
        need(details['custody']['row_contract_sha256'] == rc_sha, 'DERIVE_DETAILS_ROW_CONTRACT_SHA_DIFFERS ' + label)
        # C: independent digests and consumer checks
        direct = sha_bytes(json.dumps(row, sort_keys=True, separators=(',', ':'), allow_nan=False).encode())
        need(AD.digest(row) == rc_sha and RP.digest(row) == rc_sha and direct == rc_sha, 'DIGEST_FUNCTIONS_DISAGREE ' + label)
        need(AD.canonical(row) == canon and RP.canonical(row) == canon, 'CANONICAL_FUNCTIONS_DISAGREE ' + label)
        st = {'state_sha256': '0' * 64, 'source_sha256': '1' * 64, 'stage_kind': 'SYNTHETIC', 'nonnegative_masses': True}
        syn_result = {'passes': [{'pass': 1, 'rows': [{'id': i, 'speed_km_s': 1.0} for i in ids]}]}
        ref = RP.row_reference(state=st, row_contract=row, row_contract_sha256=rc_sha, result=syn_result,
                               result_ref={'path': '/SYNTHETIC/out/result.json', 'sha256': '2' * 64}, policy_review=None)
        radii = [r['radius_m'] for r in row['rows']]
        need(ref['row_contract_sha256'] == rc_sha and ref['row_ids'] == ids, 'ROW_PRODUCER_SYNTHETIC ' + label)
        need(ref['R_m'] == radii and ref['tau_km_s'] == tau, 'LO_CORE_L71_EMULATION ' + label)   # lo_core L69-72
        need(all(isinstance(x, float) and x > 0 for x in radii), 'RADII ' + label)
        # tau = 0.25 sigma (Q4(c)) against the region file and the prereg's own quoted sigma
        need([sig[i] for i in ids] == prereg_obj['quoted_sigma_km_s'], 'PREREG_SIGMA_NOT_REGION_SIGMA')
        need(all(t == 0.25 * s for t, s in zip(tau, prereg_obj['quoted_sigma_km_s'])), 'TAU_NOT_QUARTER_SIGMA')
        # invariance: other physical coordinates at the same D give the same record
        spec2 = copy.deepcopy(spec)
        spec2['physical'].update({'common_scale_s': float(by['common_scale_s']['upper']),
                                  'gamma': float(by['gamma_over_Eref']['upper']) * eref, 'ell_F_m': float(by['ell_F_m']['upper'])})
        _, _, binding2, _ = CU.point_geometry(spec2, d)
        need(binding2['query_rows'] == rows, 'ROWS_DEPEND_ON_NON_D_PHYSICAL ' + label)
        historical = None
        if label == 'D404':
            cmb = d.GALAXIES['DDO154']['column_mean_binding']
            base_bind = load_json(str(cmb[0]), cmb[1], 'registered column-mean binding')
            need(rows == base_bind['query_rows'], 'D404_ROWS_NOT_REGISTERED_BINDING')
            hist = load_json(*HISTORICAL_D404, 'historical custody record (custody_cx2v001, KB064 C000, D 4.04)')
            need(CU.canonical(hist['row_contract']) == canon and hist['custody']['row_contract_sha256'] == rc_sha,
                 'D404_DIFFERS_FROM_HISTORICAL_CUSTODY_RECORD')
            historical = {'path': HISTORICAL_D404[0], 'sha256': HISTORICAL_D404[1],
                          'producer': 'custody_cx2v001.py 3b29dff5 (its modules field)',
                          'row_contract_bytes_equal': True, 'row_contract_sha256_equal': True}
        out[label] = {'row': row, 'canonical': canon, 'row_contract_sha256': rc_sha,
                      'proof': {'A_rebuilt_with_custody_functions': True,
                                'B_derive_details_row_contract_bytes_equal': True,
                                'B_derive_details_row_contract_sha256_equal': True,
                                'C_digest_custody_adapter_rowproducer_hashlib_equal': True,
                                'C_row_producer_synthetic_row_reference_accepts': True,
                                'C_lo_core_L69_72_emulation_pass': True,
                                'tau_equals_quarter_region_sigma': True,
                                'rows_invariant_to_non_D_physical': True,
                                'geometry_guards_all_true': True,
                                'D404_rows_equal_registered_binding': (label == 'D404') or None,
                                'D404_equal_to_historical_custody_record': historical,
                                'seconds': round(time.monotonic() - t0, 3)}}
    checks['modules'] = {'custody': CUSTODY[1], 'driver_r5': CU.DRIVER_SHA, 'certs_common': CU.COMMON_SHA,
                         'adapter_c3v003': ADAPTER[1], 'row_producer_v003': ROW_PRODUCER[1],
                         'lo_core_hashed_only': LO_CORE[1], 'response_producer_hashed_only': RESPONSE[1],
                         'final_spec_producer_hashed_only': FINAL_SPEC_PRODUCER[1]}
    return out


def write_x(path, raw):
    with open(path, 'xb') as f:
        f.write(raw)
    back = Path(path).read_bytes()
    need(back == raw, 'READBACK ' + str(path))
    return sha_bytes(back)


def main(argv):
    write = '--write' in argv
    checks = {'python': sys.version.split()[0], 'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode}
    need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1, 'PYTHON_-I_-B_REQUIRED')
    req = {p: sha_bytes(Path(p).read_bytes()) for p in REQUESTS}
    by_label, users, d_sources, coord, rc, region = establish_d_set(checks)
    recs = build(by_label, coord, rc, region, checks)
    field_sources = {
        'schema': 'custody_cx2v002 L124 literal',
        'rows': ('custody L120 binding[query_rows], binding from custody point_geometry L93-101 -> driver r5 derive_geometry '
                 '(L1493-1611) at float(D), inclination 66.0: query_rows(D) L1548-1550, L1600 = '
                 '[{id, radius_m = radius_reference_kpc * (D / reference_distance_Mpc) * KPC_M}] over the calibration input '
                 'response_rows (driver GEOMETRY_PINS calibration_input 8fff3e43); ids == prereg V005 row_ids (custody L121)'),
        'tau_km_s': 'custody L122 prereg V005 (dbddc02c) tau_km_s = 0.25 * quoted_sigma_km_s (= region quoted_random_sigma_km_s)',
        'distance_Mpc': ('custody L125 spec physical.distance_Mpc verbatim (JSON float); the value the final-spec producer v004 '
                         'writes for the calls listed under used_by'),
        'speed_reference_policy': 'custody L126 literal (the Q4 policy is carried by the row reference and the review, not here)',
        'uncertainty_carrier_policy': 'custody L127 literal',
        'prereg': "custody L128 cc.pin('prereg_v005') (certs_common c75aaa5a L49-50, L77-82)"}
    files = {}
    if write:
        for label in ('DLO', 'D404', 'DHI'):
            p = OUT / ('ROW_CONTRACT_%s_C2V001.json' % label)
            fsha = write_x(p, recs[label]['canonical'])
            need(fsha == recs[label]['row_contract_sha256'], 'FILE_SHA_NOT_ROW_CONTRACT_SHA ' + label)
            files[label] = {'path': str(p), 'sha256': fsha}
    index = {
        'schema': 'Q4_ROW_CONTRACTS_INDEX_C2V001',
        'purpose': ('The three canonical row-contract records that lo_core_r5_cx2v001 (12d36305) produce_current_lo L225-231 '
                    'matches each Q4 row-reference policy approval against (review.verdict == APPROVED and '
                    'review.row_contract_sha256 == custody row_contract_sha256), one per distinct distance D (A134 Q4; '
                    'rulings 56774ba7 L102-104; Codex1 0141, 0152).'),
        'file_format': ('Each ROW_CONTRACT file is exactly custody.canonical(record): sorted keys, compact separators, no '
                        'trailing newline. So sha256(file bytes) == row_contract_sha256 == custody.digest(json.load(file)).'),
        'records': [{'label': k, 'note': LABELS[k], 'distance_Mpc': by_label[k], 'distance_hex': by_label[k].hex(),
                     'distance_json': json.dumps(by_label[k]),
                     'path': files.get(k, {}).get('path'), 'file_sha256': files.get(k, {}).get('sha256'),
                     'row_contract_sha256': recs[k]['row_contract_sha256'],
                     'distance_sources': d_sources[k], 'used_by': users[k], 'proof': recs[k]['proof']}
                    for k in ('DLO', 'D404', 'DHI')],
        'field_sources': field_sources,
        'code_pins': {'custody_cx2v002': {'path': CUSTODY[0], 'sha256': CUSTODY[1]},
                      'lo_core_r5_cx2v001': {'path': LO_CORE[0], 'sha256': LO_CORE[1]},
                      'point_response_producer_cx2v002': {'path': RESPONSE[0], 'sha256': RESPONSE[1],
                                                          'note': 'L24-25, L53: its CU (lo_core ctx custody) is custody 6810b7c3'},
                      'lo_state_proof_adapter_c3v003': {'path': ADAPTER[0], 'sha256': ADAPTER[1]},
                      'row_reference_producer_c2v003': {'path': ROW_PRODUCER[0], 'sha256': ROW_PRODUCER[1]},
                      'driver_r5': {'sha256': checks['modules']['driver_r5']},
                      'certs_common_r5_cx2v001': {'sha256': checks['modules']['certs_common']},
                      'final_spec_producer_c4v004': {'path': FINAL_SPEC_PRODUCER[0], 'sha256': FINAL_SPEC_PRODUCER[1]}},
        'inputs': {'direct_batch_params_c2v003a': {'path': PARAMS[0], 'sha256': PARAMS[1]},
                   'direct_batch_params_c2v003_a139': {'path': PARAMS_A139[0], 'sha256': PARAMS_A139[1]},
                   'run_config': {'path': RUN_CONFIG[0], 'sha256': RUN_CONFIG[1]},
                   'coordinate_spec': {'path': COORD[0], 'sha256': COORD[1]},
                   'coordinate_addendum': {'path': ADDENDUM[0], 'sha256': ADDENDUM[1]},
                   'observation_region': {'path': REGION[0], 'sha256': REGION[1]},
                   'prereg_v005': {'path': PREREG[0], 'sha256': PREREG[1]},
                   'a2f10_spec_template': {'path': coord['call_spec_mapping']['template']['path'], 'sha256': SPEC_TEMPLATE_SHA},
                   'rulings_a134': {'path': RULINGS[0], 'sha256': RULINGS[1]},
                   'codex1_requests': [{'path': p, 'sha256': s} for p, s in req.items()]},
        'd_set': checks['d_set'],
        'labels': {'TESTED': ['the three D values from bytes (templates, coordinate spec, region, addendum, final-spec producer source)',
                              'each record rebuilt with the pinned custody functions equals the real derive_details row_contract '
                              'byte for byte on a spec built as the final-spec producer builds it',
                              'row_contract_sha256 agrees across custody, adapter c3v003, row producer v003 and hashlib',
                              'tau = 0.25 sigma; rows depend on D only'],
                   'UNTESTED': [{'claim': 'the launched final specs carry exactly these physical.distance_Mpc floats',
                                 'deciding_test': ('custody derive_details on each launched spec (first real TAIL_REANCHOR '
                                                   'acceptance for D404; first SENS acceptance for DLO/DHI); a different float '
                                                   'gives a different hash, and lo_core blocks with '
                                                   'ROW_REFERENCE_POLICY_REVIEW_SCOPE_MISMATCH (fail-closed)')},
                                {'claim': 'POST_S1 (S1_UA_C3T, K=3) uses the D404 contract',
                                 'deciding_test': ('the KS1 custody successor (V006 A160) must build the same row record; '
                                                   'its derive_details on the S1 spec decides it')}]},
        'run_checks': checks,
    }
    raw_index = json.dumps(index, sort_keys=True, indent=1, allow_nan=False).encode() + b'\n'
    summary = {k: {'D': by_label[k], 'row_contract_sha256': recs[k]['row_contract_sha256'], 'used_by_n': len(users[k])}
               for k in ('DLO', 'D404', 'DHI')}
    if write:
        isha = write_x(OUT / 'ROW_CONTRACTS_INDEX_C2V001.json', raw_index)
        opened = sorted({tuple(x) for x in OPENED})
        run = {'schema': 'Q4_ROW_CONTRACTS_BUILD_RUN_C2V001', 'summary': summary, 'index_sha256': isha,
               'opened_research_paths': [list(x) for x in opened], 'checks': checks}
        write_x(OUT / 'BUILD_RUN_C2V001.json', json.dumps(run, sort_keys=True, indent=1).encode() + b'\n')
    print(json.dumps({'write': write, 'summary': summary, 'files': files,
                      'proof': {k: recs[k]['proof'] for k in recs},
                      'opened_research_paths': sorted({x[1] for x in OPENED})}, indent=1))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except Stop as exc:
        print('STOP: ' + str(exc))
        sys.exit(3)
