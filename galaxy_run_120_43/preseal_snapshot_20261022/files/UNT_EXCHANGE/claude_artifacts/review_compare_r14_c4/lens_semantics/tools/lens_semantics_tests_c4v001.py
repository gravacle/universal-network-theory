# lens_semantics_tests_c4v001.py -- Claude4 helper, compare r14 delta review of record (dispatch 0651 / root A114, V006).
# LENS 2: I4 after-seal token semantics.  Run ONLY through tools/run_fenced_c4st2.py (fence c993d34c), e.g.
#   python3 -I -B tools/run_fenced_c4st2.py tools/lens_semantics_tests_c4v001.py v001
# Synthetic inputs only.  Writes only under this review folder (out_<tag>/, sandbox/<tag>/; both must not exist).
# Never calls main(), build_context(), read_run/read_all/read_gates, c5h_interlock or registered_identity_code: no run tree,
# no C5H directory (not even a stat), no target data, no driver, no production comparator, no seal tool.
# evaluate_v007 is exercised through its group-1 reading only, with case/identity validity stubbed VALID and flag_rulings
# replaced by a sentinel that proves the reading got past group 1 (the T-tests would be read next).
import copy, difflib, hashlib, importlib.util, inspect, json, os, sys, time
from pathlib import Path

REVIEW = Path(__file__).resolve().parent.parent
TAG = sys.argv[1] if len(sys.argv) > 1 else 'v001'
OUT = REVIEW / ('out_' + TAG)
SB = REVIEW / 'sandbox' / TAG
R14 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py'
R13 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py'
SHA14 = 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'
SHA13 = 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'
EXP14 = ('SRB_ROT', 'RB_FP', 'T2I', 'EA', 'MT', 'I1T', 'FLAG_RULINGS', 'HARMONICS', 'SR_K', 'I4')
EXP13 = EXP14[:-1]
TASK_C = ('B0', 'B0_FA', 'B0_N3', 'B0_RO1', 'B0prime_RERUN', 'B1', 'B1_OFF', 'B2', 'B3', 'EPS', 'GQ', 'LO', 'LO_NGC', 'DOUBLING')


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha_f(p):
    return sha_b(Path(p).read_bytes())


OUT.mkdir(parents=True)
SB.mkdir(parents=True)
src14, src13 = Path(R14).read_bytes(), Path(R13).read_bytes()
if sha_b(src14) != SHA14 or sha_b(src13) != SHA13:
    raise SystemExit('REFUSED: r14/r13 source sha from bytes differs from the pin')


def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


M = load(R14, 'cmp_r14_lens2_c4')
M13 = load(R13, 'cmp_r13_lens2_c4')
TOKEN = M.GATE_RECORD_AFTER_SEAL
RES = []


def t(tid, cond_, label='TESTED', **got):
    RES.append({'id': tid, 'ok': bool(cond_), 'label': label, 'got': got})


def mkfile(rel, data):
    p = SB / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'xb') as f:
        f.write(data if isinstance(data, bytes) else data.encode())
    return str(p), sha_f(p)


def pin(p):
    return {'path': p[0], 'sha256': p[1]}


P_I4 = mkfile('producers/i4_producer_synthetic_c4.txt', 'synthetic I4 producer stand-in (inert text; never executed)\n')
P_I4_COPY = mkfile('producers_copy/i4_producer_synthetic_c4.txt', 'synthetic I4 producer stand-in (inert text; never executed)\n')
P_SRK = mkfile('producers/srk_producer_synthetic_c4.txt', 'synthetic SR_K producer stand-in\n')
P_SRB = mkfile('producers/srbrot_producer_synthetic_c4.txt', 'synthetic SRB_ROT producer stand-in\n')
P_EPS = mkfile('producers/eps_producer_synthetic_c4.txt', 'synthetic EPS producer stand-in\n')
P_MUT = mkfile('producers/i4_producer_mutable_c4.txt', 'synthetic I4 producer, appended to after the registry is loaded\n')
P_OTHER = mkfile('producers/unregistered_producer_c4.txt', 'not registered anywhere\n')
DRV = 'd' * 64          # the synthetic 'sealed driver' (every T-case drivers_allowed)
IDS = ['R%02d' % i for i in range(1, 13)]
TAU = {i: 1.0 for i in IDS}
PRODUCERS = {'I4': [pin(P_I4)], 'SR_K': [pin(P_SRK)], 'SRB_ROT': [pin(P_SRB)], 'EPS': [pin(P_EPS)]}


def reg_obj(gate_records, producers=None, **extra):
    o = {'schema': M.PRODUCER_REGISTRY_SCHEMA, 'producers': copy.deepcopy(PRODUCERS if producers is None else producers),
         'identity_comparators': [], 'identity_tokens': {}, 'gate_records': gate_records, 'gq_all_nodes_counts': {}}
    o.update(extra)
    return o


def load_try(mod, obj):
    try:
        r = mod.producer_registry_from_obj(copy.deepcopy(obj))
        return {'result': 'ACCEPTED', 'gate_records': {g: (v if isinstance(v, str) else sorted(v)) for g, v in r['gate_records'].items()}}
    except mod.Refused as e:
        return {'result': 'REFUSED', 'code': e.refusal_code, 'text': str(e)}
    except Exception as e:                        # never expected
        return {'result': 'EXCEPTION', 'type': type(e).__name__, 'text': str(e)[:200]}


def ctx_for(reg, mode='parallel8'):
    return {'producer_registry': reg, 'case_block': {'cases': {c: {'drivers_allowed': [DRV]} for c in M.T_CASES}},
            'route_a_mode': mode, 'ids': IDS, 'tau': TAU}


def write_rec(name, obj, raw=None):
    p = SB / 'records' / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'xb') as f:
        f.write(raw if raw is not None else json.dumps(obj, indent=1).encode())
    return str(p), sha_f(p)


def i4_record(drop=(), **over):
    r = {'schema': M.GATE_SCHEMA, 'gate': 'I4', 'producer': pin(P_I4), 'verdict': M.I4_PASS_VERDICT, 'tail': 'ON',
         'driver_sha256': DRV, 'serial_result_sha256': 'a' * 64, 'parallel_result_sha256': 'b' * 64,
         'v8c_f1_fix_confirmed': True, 'bitwise_equal': True, 'differences_outside_custody': []}
    r.update(over)
    for k in drop:
        r.pop(k, None)
    return r


def ev(mod, gate, path, ctx, runs_sha=None):
    o = mod.evaluate_gate(gate, path, ctx, runs_sha)
    o.pop('_record_json', None)
    return o


def short(o):
    return {'status': o['status'], 'codes': o['codes'], 'crossref': o.get('crossref'), 'record_sha256': (o.get('record') or {}).get('sha256')}


# ============================================================ C0 constants (r14 vs r13), TESTED from the loaded modules
t('C0_ALLOWED_SET_R14_IS_R13_PLUS_I4', M.GATE_RECORD_AFTER_SEAL_ALLOWED == EXP14 and M13.GATE_RECORD_AFTER_SEAL_ALLOWED == EXP13,
  r14=list(M.GATE_RECORD_AFTER_SEAL_ALLOWED), r13=list(M13.GATE_RECORD_AFTER_SEAL_ALLOWED))
t('C0_OTHER_GATE_CONSTANTS_UNCHANGED', M.GATE_RECORD_SHA_REQUIRED == () == M13.GATE_RECORD_SHA_REQUIRED and M.ALL_GATES == M13.ALL_GATES
  and M.REQUIRED_GATES == M13.REQUIRED_GATES and M.MODE_GATES == M13.MODE_GATES == ('I4',) and M.OPTIONAL_GATES == M13.OPTIONAL_GATES
  and M.GATE_RECORD_AFTER_SEAL == M13.GATE_RECORD_AFTER_SEAL == 'PRODUCED_AFTER_THE_SEAL'
  and M.PRODUCER_REGISTRY_SCHEMA == M13.PRODUCER_REGISTRY_SCHEMA and M.REGISTRY_KEYS == M13.REGISTRY_KEYS
  and sorted(M.GATE_FUNCS) == sorted(M13.GATE_FUNCS) and M.GATE_PASS_VERDICTS == M13.GATE_PASS_VERDICTS
  and M.VERDICT_ONLY_GATES == M13.VERDICT_ONLY_GATES and M.ROUTE_A_MODES == M13.ROUTE_A_MODES,
  all_gates=list(M.ALL_GATES), mode_gates=list(M.MODE_GATES))

# ============================================================ (c) loader: the token on each gate, r14 and r13
load14, load13 = {}, {}
for g in M.ALL_GATES:
    load14[g] = load_try(M, reg_obj({g: TOKEN}))
    load13[g] = load_try(M13, reg_obj({g: TOKEN}))
for g in TASK_C + ('B0prime_DRY',):
    x = load14[g]
    t('C1_TOKEN_REFUSED_AT_LOAD_R14_' + g, x['result'] == 'REFUSED' and x.get('code') == 'PRODUCER_REGISTRY_GATE_RECORDS', r14=x.get('code'))
t('C1_TOKEN_ACCEPTED_AT_LOAD_R14_I4', load14['I4']['result'] == 'ACCEPTED' and load14['I4']['gate_records'] == {'I4': TOKEN},
  r14=load14['I4'], r13=load13['I4'].get('code'))
acc14 = sorted(g for g, x in load14.items() if x['result'] == 'ACCEPTED')
acc13 = sorted(g for g, x in load13.items() if x['result'] == 'ACCEPTED')
t('C1_ACCEPTED_SET_EXACT_R14_EQ_R13_PLUS_I4', acc14 == sorted(EXP14) and acc13 == sorted(EXP13)
  and all(x['result'] in ('ACCEPTED', 'REFUSED') for x in list(load14.values()) + list(load13.values())), acc14=acc14, acc13=acc13)
t('C1_EVERY_TOKEN_SET_GATE_TOGETHER_ACCEPTED_R14', load_try(M, reg_obj({g: TOKEN for g in EXP14}))['result'] == 'ACCEPTED')
mix = {g: load_try(M, reg_obj({'I4': TOKEN, g: TOKEN}))['result'] for g in TASK_C}
t('C1_I4_TOKEN_PLUS_ANY_REFUSED_GATE_TOKEN_REFUSES_WHOLE_REGISTRY', all(v == 'REFUSED' for v in mix.values()), got=mix)
variants = {'lowercase': 'produced_after_the_seal', 'list_wrapped': [TOKEN], 'trailing_space': TOKEN + ' ', 'short_form': 'PRODUCED_AFTER_SEAL',
            'none': None, 'dict': {'token': TOKEN}, 'true': True}
vres = {k: load_try(M, reg_obj({'I4': v}))['result'] for k, v in variants.items()}
kres = {k: load_try(M, reg_obj({k: TOKEN}))['result'] for k in ('i4', 'I4 ', 'I4_', 'MODE_GATES')}
t('C1_TOKEN_VARIANTS_AND_GATE_NAME_VARIANTS_REFUSED', all(v == 'REFUSED' for v in list(vres.values()) + list(kres.values())), values=vres, keys=kres)
t('C1_EMPTY_SHA_LIST_ON_I4_ACCEPTED_AT_LOAD_BUT_FAILS_CLOSED_LATER', load_try(M, reg_obj({'I4': []}))['result'] == 'ACCEPTED',
  note='an empty list is a legal registry entry; any I4 record then reads GATE_RECORD_SHA_NOT_ROOT_REGISTERED (tested B4b below)')
# file route (load_producer_registry), including a duplicate-key file that names I4 twice (token and a sha list)
file14 = {}
for g in ('I4',) + TASK_C:
    p, _ = mkfile('registries/token_on_%s.json' % g, json.dumps(reg_obj({g: TOKEN}), indent=1))
    try:
        M.load_producer_registry(p)
        file14[g] = 'ACCEPTED'
    except M.Refused as e:
        file14[g] = 'REFUSED:' + str(e.refusal_code)
t('C1_FILE_ROUTE_SAME_AS_OBJECT_ROUTE', file14['I4'] == 'ACCEPTED' and all(file14[g] == 'REFUSED:PRODUCER_REGISTRY_GATE_RECORDS' for g in TASK_C),
  got=file14)
dup_txt = json.dumps(reg_obj({'I4': TOKEN}), indent=1).replace('"gate_records": {', '"gate_records": {\n  "I4": ["%s"],' % ('c' * 64), 1)
pdup, _ = mkfile('registries/i4_token_and_sha_duplicate_key.json', dup_txt)
try:
    M.load_producer_registry(pdup)
    dres = 'ACCEPTED'
except M.Refused as e:
    dres = 'REFUSED:' + str(e.refusal_code)
t('C1_I4_TOKEN_AND_SHA_LIST_AS_DUPLICATE_JSON_KEY_REFUSED', dres == 'REFUSED:PRODUCER_REGISTRY_DUPLICATE_JSON_KEY_A71', got=dres)

# ============================================================ (c) defence in depth: hand-built (loader-bypassing) registries
hb14 = {g: M.gate_record_sha_codes(g, 'c' * 64, {'gate_records': {g: TOKEN}}) for g in M.ALL_GATES}
hb13 = {g: M13.gate_record_sha_codes(g, 'c' * 64, {'gate_records': {g: TOKEN}}) for g in M.ALL_GATES}
t('C2_HAND_BUILT_TOKEN_FAILS_CLOSED_FOR_EVERY_REFUSED_GATE_R14',
  all(hb14[g] == [] for g in EXP14) and all(hb14[g] == ['GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:%s' % g] for g in M.ALL_GATES if g not in EXP14),
  open_gates=sorted(g for g, v in hb14.items() if not v))
t('C2_HAND_BUILT_TOKEN_R13_REFUSES_I4_ONLY_DIFFERENCE', {g for g in M.ALL_GATES if hb14[g] != hb13[g]} == {'I4'}
  and hb13['I4'] == ['GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:I4'], r13_I4=hb13['I4'])

# ============================================================ registries used below
REG_TOKEN = M.producer_registry_from_obj(reg_obj({g: TOKEN for g in EXP14}))
CTX = ctx_for(REG_TOKEN)

# ============================================================ (a) before the real record exists
a_none = ev(M, 'I4', None, CTX)
a_absent = ev(M, 'I4', str(SB / 'records' / 'I4_NOT_YET_WRITTEN.json'), CTX)
a_dir = ev(M, 'I4', str(SB), CTX)
pe, _ = write_rec('I4_empty_placeholder.json', None, raw=b'')
a_empty = ev(M, 'I4', pe, CTX)
pp, _ = write_rec('I4_placeholder_pending.json', i4_record(verdict='PENDING', drop=('bitwise_equal',)))
a_pend = ev(M, 'I4', pp, CTX)
s_none = ev(M, 'SR_K', None, CTX)
t('A1_I4_TOKEN_NO_RECORD_IS_MISSING_NEVER_PASS', a_none['status'] == 'MISSING' and a_none['codes'] == ['GATE_RECORD_MISSING:I4']
  and a_absent['status'] == 'MISSING' and a_dir['status'] == 'MISSING', none=short(a_none), absent=short(a_absent), directory=short(a_dir))
t('A1_SR_K_TOKEN_NO_RECORD_IS_MISSING_SAME_AS_I4', s_none['status'] == 'MISSING' and s_none['codes'] == ['GATE_RECORD_MISSING:SR_K'])
t('A1_PLACEHOLDER_OR_EMPTY_I4_FILE_IS_RECORD_DEFECT', a_empty['status'] == 'RECORD_DEFECT' and a_pend['status'] == 'RECORD_DEFECT',
  empty=short(a_empty), pending=short(a_pend))
bl = M.blinded_gate(dict(a_none))
t('A1_GATES_ONLY_BLINDED_VIEW_OF_MISSING_I4', bl['status'] == 'MISSING' and bl['codes'] == ['GATE_RECORD_MISSING:I4'], got=bl)


class Reached(Exception):
    pass


def reading(mod, gates, mode):
    """evaluate_v007 group 1 only: every case and identity run stubbed VALID; flag_rulings (called on the line after
    dec['tests_read'] = True) raises the sentinel, which proves the reading would read the T-tests next."""
    names = ('case_validity', 'identity_run_validity', 'rpair_untriggered', '_numerics_of', 'flag_rulings', 'gate_fail_next_step')
    saved = {n: getattr(mod, n) for n in names}
    calls = []
    real_gfns = saved['gate_fail_next_step']
    try:
        mod.case_validity = lambda lab, run, ctx, *a, **k: {'valid_all': True, 'failed': [], 'reading': None, 'accepted_route_a_iteration': 8}
        mod.identity_run_validity = lambda n, run, ctx=None: {'valid': True, 'codes': [], 'ro1_codes': [], 'ro1_fired': False}
        mod.rpair_untriggered = lambda *a, **k: []
        mod._numerics_of = lambda run: None

        def _fr(g):
            raise Reached()
        mod.flag_rulings = _fr

        def _g(g):
            calls.append(g)
            return real_gfns(g)
        mod.gate_fail_next_step = _g
        ctx = {'route_a_mode': mode, 'c5h_admission': {}}
        R = {lab: {'present': False} for lab in mod.REGISTERED}
        try:
            rep = mod.evaluate_v007(ctx, R, {}, gates)
        except Reached:
            return {'outcome': 'GROUP1_PASSED_T_TESTS_READ_NEXT', 'tests_read': True, 'failing_reported': calls}
        d = rep['decision']
        return {'outcome': d['outcome'], 'subtype': d.get('subtype'), 'reasons': d['reasons'], 'tests_read': d['tests_read'],
                'next_step': d['next_step'], 'failing_reported': calls}
    finally:
        for n, f in saved.items():
            setattr(mod, n, f)


def pass_gate(g):
    return {'gate': g, 'status': 'PASS', 'codes': [], 'fields_read': [], 'record': None, 'crossref': {}, 'derived': {}}


def gates_with(mod, **over):
    G = {g: pass_gate(g) for g in mod.ALL_GATES}
    G.update(over)
    return G


p_ok, s_ok = write_rec('I4_pass_synthetic.json', i4_record())
g_ok = ev(M, 'I4', p_ok, CTX)
p_fail, _ = write_rec('I4_fail_not_bitwise.json', i4_record(verdict='FAIL', bitwise_equal=False))
g_fail = ev(M, 'I4', p_fail, CTX)
p_def, _ = write_rec('I4_defect_unregistered_producer.json', i4_record(producer=pin(P_OTHER)))
g_def = ev(M, 'I4', p_def, CTX)
t('A2_I4_GATE_STATUSES_FROM_REAL_EVALUATE_GATE', g_ok['status'] == 'PASS' and g_fail['status'] == 'FAIL' and g_def['status'] == 'RECORD_DEFECT',
  ok=short(g_ok), fail=short(g_fail), defect=short(g_def))
RD = {}
RD['p8_I4_missing'] = reading(M, gates_with(M, I4=a_none), 'parallel8')
RD['p8_I4_pass'] = reading(M, gates_with(M, I4=g_ok), 'parallel8')
RD['p8_I4_fail'] = reading(M, gates_with(M, I4=g_fail), 'parallel8')
RD['p8_I4_defect'] = reading(M, gates_with(M, I4=g_def), 'parallel8')
RD['p8_I4_absent_from_gates_dict'] = reading(M, {g: pass_gate(g) for g in M.ALL_GATES if g != 'I4'}, 'parallel8')
RD['ser_I4_missing'] = reading(M, gates_with(M, I4=a_none), 'serial_with_exemption')
RD['ser_I4_fail'] = reading(M, gates_with(M, I4=g_fail), 'serial_with_exemption')
RD['ser_I4_defect'] = reading(M, gates_with(M, I4=g_def), 'serial_with_exemption')
RD['p8_SR_K_missing'] = reading(M, gates_with(M, SR_K=s_none), 'parallel8')
srk_fail = dict(pass_gate('SR_K'), status='FAIL', codes=['VERDICT:SR_K:FAIL'])
RD['p8_SR_K_fail'] = reading(M, gates_with(M, SR_K=srk_fail), 'parallel8')
RD['p8_I4_and_SR_K_missing'] = reading(M, gates_with(M, I4=a_none, SR_K=s_none), 'parallel8')
x = RD['p8_I4_missing']
t('A3_P8_I4_MISSING_READS_INCOMPLETE_T_TESTS_NOT_READ', x['outcome'] == 'INCOMPLETE' and x['subtype'] == 'CASES_OR_RECORDS'
  and x['reasons'] == ['gate record I4 missing'] and x['tests_read'] is False and 'I4' in x['next_step'], got=x)
x = RD['p8_I4_absent_from_gates_dict']
x13 = reading(M13, {g: pass_gate(g) for g in M13.ALL_GATES if g != 'I4'}, 'parallel8')
t('A3_PROBE_GATES_DICT_WITHOUT_I4_LETS_P8_READING_PROCEED_R13_SAME', x['outcome'] == 'GROUP1_PASSED_T_TESTS_READ_NEXT' and x13 == x, got=x,
  note='absent is not MISSING (gates.get(I4, {}) has no status); the CLI never builds such a dict (read_gates evaluates ALL_GATES), inherited')
x = RD['p8_I4_fail']
t('A3_P8_I4_FAIL_READS_INCOMPLETE_PARALLEL8_NOT_LICENSED', x['outcome'] == 'INCOMPLETE' and x['tests_read'] is False
  and any(r.endswith('parallel8 route A not licensed') for r in x['reasons']) and x['next_step'].get('I4') == M.I4_NEXT, got=x)
x = RD['p8_I4_defect']
t('A3_P8_I4_RECORD_DEFECT_READS_NO_RUN', x['outcome'] == 'NO_RUN' and x['tests_read'] is False, got=x)
t('A3_P8_I4_PASS_LETS_THE_READING_PROCEED', RD['p8_I4_pass']['outcome'] == 'GROUP1_PASSED_T_TESTS_READ_NEXT', got=RD['p8_I4_pass'])
t('A3_SERIAL_I4_MISSING_OR_FAIL_DOES_NOT_BLOCK_DEFECT_STILL_NO_RUN', RD['ser_I4_missing']['outcome'] == 'GROUP1_PASSED_T_TESTS_READ_NEXT'
  and RD['ser_I4_fail']['outcome'] == 'GROUP1_PASSED_T_TESTS_READ_NEXT' and 'I4' in RD['ser_I4_fail']['failing_reported']
  and RD['ser_I4_defect']['outcome'] == 'NO_RUN', ser_missing=RD['ser_I4_missing'], ser_fail=RD['ser_I4_fail'], ser_defect=RD['ser_I4_defect'])
t('A3_SR_K_PARITY_MISSING_INCOMPLETE_BUT_FAIL_IS_READ_IN_THE_T_TESTS', RD['p8_SR_K_missing']['outcome'] == 'INCOMPLETE'
  and RD['p8_SR_K_missing']['reasons'] == ['gate record SR_K missing'] and RD['p8_SR_K_fail']['outcome'] == 'GROUP1_PASSED_T_TESTS_READ_NEXT',
  srk_missing=RD['p8_SR_K_missing'], srk_fail=RD['p8_SR_K_fail'])
t('A3_BOTH_MISSING_BOTH_NAMED', RD['p8_I4_and_SR_K_missing']['outcome'] == 'INCOMPLETE'
  and sorted(RD['p8_I4_and_SR_K_missing']['reasons']) == ['gate record I4 missing', 'gate record SR_K missing'], got=RD['p8_I4_and_SR_K_missing'])
# every token gate MISSING, both modes (parity of the token set in the reading)
miss = {}
for g in EXP14:
    gm = ev(M, g, None, CTX)
    for mode in ('parallel8', 'serial_with_exemption'):
        miss['%s|%s' % (g, mode)] = reading(M, gates_with(M, **{g: gm}), mode)['outcome']
t('A4_TOKEN_GATES_MISSING_READING_BY_GROUP', all(miss['%s|%s' % (g, m)] == 'INCOMPLETE' for g in M.OTHER_REQUIRED_GATES for m in ('parallel8', 'serial_with_exemption'))
  and miss['I4|parallel8'] == 'INCOMPLETE' and miss['I4|serial_with_exemption'] == 'GROUP1_PASSED_T_TESTS_READ_NEXT'
  and all(miss['%s|%s' % (g, m)] == 'GROUP1_PASSED_T_TESTS_READ_NEXT' for g in ('MT', 'HARMONICS', 'FLAG_RULINGS') for m in ('parallel8', 'serial_with_exemption')),
  got=miss)

# ============================================================ (b) binding of a real (post-seal) I4 record
RUNS = {'C2T': 'e' * 64, 'C4T': 'f' * 64}
b = {}
b['B1_token_pass'] = ev(M, 'I4', p_ok, CTX, RUNS)
REG_SHA_OTHER = M.producer_registry_from_obj(reg_obj(dict({g: TOKEN for g in EXP13}, I4=['c' * 64])))
REG_SHA_SELF = M.producer_registry_from_obj(reg_obj(dict({g: TOKEN for g in EXP13}, I4=[s_ok])))
REG_NO_I4 = M.producer_registry_from_obj(reg_obj({g: TOKEN for g in EXP13}))
REG_EMPTY_I4 = M.producer_registry_from_obj(reg_obj(dict({g: TOKEN for g in EXP13}, I4=[])))
b['B2_sha_regime_other_sha'] = ev(M, 'I4', p_ok, ctx_for(REG_SHA_OTHER), RUNS)
b['B3_sha_regime_this_sha'] = ev(M, 'I4', p_ok, ctx_for(REG_SHA_SELF), RUNS)
b['B4_gate_absent_from_gate_records'] = ev(M, 'I4', p_ok, ctx_for(REG_NO_I4), RUNS)
b['B4b_empty_sha_list'] = ev(M, 'I4', p_ok, ctx_for(REG_EMPTY_I4), RUNS)
t('B1_TOKEN_BINDS_BY_PRODUCER_PIN_ONLY_RECORD_SHA_NOT_CHECKED', b['B1_token_pass']['status'] == 'PASS'
  and b['B2_sha_regime_other_sha']['codes'] == ['GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:I4']
  and b['B3_sha_regime_this_sha']['status'] == 'PASS' and b['B4_gate_absent_from_gate_records']['status'] == 'RECORD_DEFECT'
  and b['B4b_empty_sha_list']['status'] == 'RECORD_DEFECT', got={k: short(v) for k, v in b.items()})
t('B1_RECORD_SHA_IS_REPORTED_NOT_VERIFIED', b['B1_token_pass']['record']['sha256'] == s_ok, record_sha256=s_ok)
# not the producer's output: a hand-written record that names the registered producer
p_c2t, _ = write_rec('I4_handwritten_parallel_not_C2T.json', i4_record(parallel_result_sha256='9' * 64))
p_same, _ = write_rec('I4_handwritten_serial_equals_parallel.json', i4_record(serial_result_sha256='7' * 64, parallel_result_sha256='7' * 64))
p_extra, _ = write_rec('I4_with_unread_n1_spec_field.json', i4_record(n1_spec_sha256='5' * 64, n1_column_workers=8, comment='not read'))
b['B6_parallel_not_C2T'] = ev(M, 'I4', p_c2t, CTX, RUNS)
b['B7_serial_equals_parallel'] = ev(M, 'I4', p_same, CTX, RUNS)
b['B27_unread_fields'] = ev(M, 'I4', p_extra, CTX, RUNS)
t('B6_RECORD_NOT_FROM_THE_PRODUCER_PASSES_WHEN_IT_NAMES_THE_PRODUCER', b['B6_parallel_not_C2T']['status'] == 'PASS'
  and b['B6_parallel_not_C2T']['crossref'] == {} and b['B7_serial_equals_parallel']['status'] == 'PASS' and b['B27_unread_fields']['status'] == 'PASS',
  parallel_not_C2T=short(b['B6_parallel_not_C2T']), serial_eq_parallel=short(b['B7_serial_equals_parallel']), extra=short(b['B27_unread_fields']),
  runs_sha_C2T=RUNS['C2T'])
fr = b['B1_token_pass']['fields_read']
t('B6_G_I4_READS_NO_CROSSREF_AND_NO_N1_SPEC', 'n1_spec_sha256' not in fr and b['B1_token_pass']['crossref'] == {}, fields_read=fr)
# producer-pin negatives
p_srkprod, _ = write_rec('I4_names_SR_K_producer.json', i4_record(producer=pin(P_SRK)))
p_copy, _ = write_rec('I4_names_copy_path.json', i4_record(producer=pin(P_I4_COPY)))
b['B8_names_other_gates_producer'] = ev(M, 'I4', p_srkprod, CTX, RUNS)
b['B9_unregistered_producer'] = g_def
b['B10_registered_sha_other_path'] = ev(M, 'I4', p_copy, CTX, RUNS)
REG_MUT = M.producer_registry_from_obj(reg_obj({g: TOKEN for g in EXP14}, producers=dict(PRODUCERS, I4=[pin(P_MUT)])))
p_mut, _ = write_rec('I4_names_mutable_producer.json', i4_record(producer=pin(P_MUT)))
before = ev(M, 'I4', p_mut, ctx_for(REG_MUT), RUNS)
with open(P_MUT[0], 'ab') as f:
    f.write(b'appended after the registry load\n')
b['B11_producer_bytes_changed_after_load'] = ev(M, 'I4', p_mut, ctx_for(REG_MUT), RUNS)
b['B12_no_registry'] = ev(M, 'I4', p_ok, ctx_for(None), RUNS)
REG_NOPROD = M.producer_registry_from_obj(reg_obj({g: TOKEN for g in EXP14}, producers={k: v for k, v in PRODUCERS.items() if k != 'I4'}))
b['B13_no_I4_producer_registered'] = ev(M, 'I4', p_ok, ctx_for(REG_NOPROD), RUNS)
t('B8_PRODUCER_PIN_NEGATIVES_ALL_RECORD_DEFECT', before['status'] == 'PASS'
  and b['B8_names_other_gates_producer']['codes'][:1] == ['PRODUCER_NOT_ROOT_REGISTERED_A62_2:I4']
  and b['B9_unregistered_producer']['codes'][:1] == ['PRODUCER_NOT_ROOT_REGISTERED_A62_2:I4']
  and b['B10_registered_sha_other_path']['codes'][:1] == ['PRODUCER_PATH_NOT_ROOT_REGISTERED_A69_1:I4']
  and b['B11_producer_bytes_changed_after_load']['codes'][:1] == ['PRODUCER_BYTES_NOT_THE_REGISTERED_SHA_A69_1:I4']
  and b['B12_no_registry']['codes'][:1] == ['PRODUCER_REGISTRY_ABSENT_A62_2:I4']
  and b['B13_no_I4_producer_registered']['codes'][:1] == ['PRODUCER_NOT_ROOT_REGISTERED_A62_2:I4']
  and all(b[k]['status'] == 'RECORD_DEFECT' for k in ('B8_names_other_gates_producer', 'B9_unregistered_producer', 'B10_registered_sha_other_path',
                                                      'B11_producer_bytes_changed_after_load', 'B12_no_registry', 'B13_no_I4_producer_registered')),
  got={k: short(b[k]) for k in ('B8_names_other_gates_producer', 'B9_unregistered_producer', 'B10_registered_sha_other_path',
                                'B11_producer_bytes_changed_after_load', 'B12_no_registry', 'B13_no_I4_producer_registered')})
# g_I4 field clauses under the token
cl = {}
for nm, rec_ in (('B14_driver_not_sealed', i4_record(driver_sha256='0' * 64)), ('B15_tail_off', i4_record(tail='OFF')),
                 ('B16_not_bitwise_verdict_pass', i4_record(bitwise_equal=False)), ('B17_not_bitwise_verdict_fail', i4_record(verdict='FAIL', bitwise_equal=False)),
                 ('B18_fail_verdict_no_failing_clause', i4_record(verdict='FAIL')), ('B19_verdict_pending', i4_record(verdict='PENDING')),
                 ('B20_differences_outside_custody', i4_record(verdict='FAIL', differences_outside_custody=['route_a.column_workers'])),
                 ('B21_v8c_not_confirmed', i4_record(verdict='FAIL', v8c_f1_fix_confirmed=False)),
                 ('B22_parallel_sha_missing', i4_record(drop=('parallel_result_sha256',))), ('B23_gate_name_SR_K', i4_record(gate='SR_K')),
                 ('B24_schema_wrong', i4_record(schema='UNT_SOMETHING_ELSE')),
                 ('B25_numbers_producer_wrong_sha', i4_record(numbers_producer={'path': P_I4[0], 'sha256': '1' * 64})),
                 ('B26b_bitwise_equal_string_true', i4_record(bitwise_equal='true'))):
    p_, _ = write_rec('I4_%s.json' % nm, rec_)
    cl[nm] = short(ev(M, 'I4', p_, CTX, RUNS))
pdk, _ = write_rec('I4_B26_duplicate_key.json', None, raw=json.dumps(i4_record()).replace('"tail": "ON"', '"tail": "OFF", "tail": "ON"', 1).encode())
cl['B26_duplicate_json_key'] = short(ev(M, 'I4', pdk, CTX, RUNS))
exp_status = {'B14_driver_not_sealed': 'RECORD_DEFECT', 'B15_tail_off': 'RECORD_DEFECT', 'B16_not_bitwise_verdict_pass': 'RECORD_DEFECT',
              'B17_not_bitwise_verdict_fail': 'FAIL', 'B18_fail_verdict_no_failing_clause': 'RECORD_DEFECT', 'B19_verdict_pending': 'RECORD_DEFECT',
              'B20_differences_outside_custody': 'FAIL', 'B21_v8c_not_confirmed': 'FAIL', 'B22_parallel_sha_missing': 'RECORD_DEFECT',
              'B23_gate_name_SR_K': 'RECORD_DEFECT', 'B24_schema_wrong': 'RECORD_DEFECT', 'B25_numbers_producer_wrong_sha': 'RECORD_DEFECT',
              'B26b_bitwise_equal_string_true': 'RECORD_DEFECT', 'B26_duplicate_json_key': 'RECORD_DEFECT'}
t('B14_G_I4_CLAUSES_UNDER_THE_TOKEN', all(cl[k]['status'] == v for k, v in exp_status.items()), got=cl)
# registry cannot carry an N1 spec pin in the I4 producer entry (A114.3 'pinned in V010's I4 entry')
bad_prod = dict(PRODUCERS, I4=[dict(pin(P_I4), n1_spec_sha256='5' * 64)])
t('B28_REGISTRY_PRODUCER_ENTRY_CANNOT_CARRY_AN_N1_SPEC_SHA', load_try(M, reg_obj({'I4': TOKEN}, producers=bad_prod)).get('code') == 'PRODUCER_REGISTRY_PRODUCERS'
  and load_try(M, reg_obj({'I4': TOKEN}, note={'I4_N1_spec_sha256': '5' * 64}))['result'] == 'ACCEPTED',
  note='only the free note key can carry it; the compare never reads note')
# parity: SR_K (A88) and SRB_ROT (crossref) under the same token regime
srk = {'schema': M.GATE_SCHEMA, 'gate': 'SR_K', 'producer': pin(P_SRK), 'verdict': M.GATE_PASS_VERDICTS['SR_K'],
       'states': {s: M.PIN_R3[s][1] for s in ('C2R3', 'C3R3', 'C4R3')},
       'Delta_km_s': {K: [0.01 * (int(K) + j) for j in range(12)] for K in ('2', '3', '4')}}
p_srk_ok, _ = write_rec('SR_K_handwritten_ok.json', srk)
p_srk_bad, _ = write_rec('SR_K_handwritten_wrong_state.json', dict(srk, states=dict(srk['states'], C4R3='2' * 64)))
srb = {'schema': M.GATE_SCHEMA, 'gate': 'SRB_ROT', 'producer': pin(P_SRB), 'verdict': M.GATE_PASS_VERDICTS['SRB_ROT'], 'case': 'C4T',
       'c4t_result_sha256': RUNS['C4T'], 'srb_rot_km_s': [0.0] * 12}
p_srb_ok, _ = write_rec('SRB_ROT_handwritten_ok.json', srb)
p_srb_bad, _ = write_rec('SRB_ROT_handwritten_not_C4T.json', dict(srb, c4t_result_sha256='3' * 64))
par = {'SR_K_handwritten_ok': short(ev(M, 'SR_K', p_srk_ok, CTX, RUNS)), 'SR_K_wrong_state': short(ev(M, 'SR_K', p_srk_bad, CTX, RUNS)),
       'SRB_ROT_ok': short(ev(M, 'SRB_ROT', p_srb_ok, CTX, RUNS)), 'SRB_ROT_not_C4T': short(ev(M, 'SRB_ROT', p_srb_bad, CTX, RUNS))}
t('P1_SAME_PRODUCER_PIN_PROPERTY_ON_SR_K_BUT_SR_K_CONTENT_IS_PINNED', par['SR_K_handwritten_ok']['status'] == 'PASS'
  and par['SR_K_wrong_state']['status'] == 'RECORD_DEFECT' and 'SR_K_STATE_C4R3' in ' '.join(par['SR_K_wrong_state']['codes']), got=par)
t('P2_SRB_ROT_CROSSREFS_ITS_RUN_I4_DOES_NOT', par['SRB_ROT_ok']['status'] == 'PASS' and par['SRB_ROT_not_C4T']['status'] == 'RECORD_DEFECT'
  and par['SRB_ROT_not_C4T']['codes'] == ['CROSSREF_MISMATCH:SRB_ROT:c4t_result_sha256'] and b['B6_parallel_not_C2T']['status'] == 'PASS', got=par)
xr_sites = {}
for g, f in M.GATE_FUNCS.items():
    srcg = inspect.getsource(f)
    xr_sites[g] = srcg.count("xr('") + srcg.count('xr("')
t('P3_CROSSREF_CALL_SITES_PER_TOKEN_GATE', xr_sites['I4'] == 0, label='TESTED', per_gate={g: xr_sites[g] for g in EXP14},
  note='xr calls whose target is a run label vs derived (_...) values: see LENS_SEMANTICS.md; I4 has none')

# ============================================================ (d) does adding I4 change any other gate?
diff = [l for l in difflib.unified_diff(src13.decode().splitlines(), src14.decode().splitlines(), lineterm='', n=0)
        if not l.startswith(('---', '+++', '@@'))]
t('D1_SOURCE_DIFF_IS_ONE_LINE', len(diff) == 2 and diff[0].startswith('-GATE_RECORD_AFTER_SEAL_ALLOWED') and diff[1].startswith('+GATE_RECORD_AFTER_SEAL_ALLOWED')
  and diff[1] == diff[0].replace("'SR_K')", "'SR_K', 'I4')").replace('-', '+', 1), diff=diff)
same_load = {g: (load14[g]['result'] == load13[g]['result'] and load14[g].get('code') == load13[g].get('code')) for g in M.ALL_GATES}
same_sha_list = {}
for g in M.ALL_GATES:
    o = reg_obj({g: ['c' * 64]})
    a14, a13 = load_try(M, o), load_try(M13, o)
    same_sha_list[g] = a14['result'] == a13['result'] == 'ACCEPTED'
t('D2_LOADER_IDENTICAL_FOR_EVERY_OTHER_GATE', all(v for g, v in same_load.items() if g != 'I4') and not same_load['I4'] and all(same_sha_list.values()),
  differs=[g for g, v in same_load.items() if not v])
codes_eq = {}
for g in M.ALL_GATES:
    for regv in ({'gate_records': {g: TOKEN}}, {'gate_records': {g: frozenset(['c' * 64])}}, {'gate_records': {}}):
        for rs in ('c' * 64, '4' * 64):
            codes_eq.setdefault(g, []).append(M.gate_record_sha_codes(g, rs, regv) == M13.gate_record_sha_codes(g, rs, regv))
t('D3_GATE_RECORD_SHA_CODES_IDENTICAL_FOR_EVERY_OTHER_GATE', all(all(v) for g, v in codes_eq.items() if g != 'I4') and not all(codes_eq['I4']),
  differs=[g for g, v in codes_eq.items() if not all(v)])
e14, e13 = load14['EPS'], load13['EPS']
t('D4_REFUSAL_TEXT_ONLY_GAINS_I4_CODE_UNCHANGED', e14['code'] == e13['code'] == 'PRODUCER_REGISTRY_GATE_RECORDS'
  and e14['text'] == e13['text'].replace('HARMONICS/SR_K;', 'HARMONICS/SR_K/I4;'), r14=e14['text'], r13=e13['text'])
f14, f13 = SB / 'FIELDS_from_r14.md', SB / 'FIELDS_from_r13.md'
M.write_field_contract(str(f14))
M13.write_field_contract(str(f13))
fd = [l for l in difflib.unified_diff(f13.read_text().splitlines(), f14.read_text().splitlines(), lineterm='', n=0)
      if not l.startswith(('---', '+++', '@@'))]
gen = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/FIELDS_R14_CX1V001.md').read_bytes()
t('D5_FIELD_CONTRACT_DIFF_IS_THE_ALLOWED_LIST_LINE_ONLY', len(fd) == 2 and ', SR_K, I4; every other gate' in fd[1] and ', SR_K; every other gate' in fd[0],
  diff=fd, generated_now_sha256=sha_f(f14), published_FIELDS_R14_CX1V001_sha256=sha_b(gen), generated_equals_published=(f14.read_bytes() == gen))
# reading parity r13 vs r14 for every gate other than I4 (MISSING / FAIL / RECORD_DEFECT of each gate, both modes)
rp = {}
for g in M.ALL_GATES:
    for st in ('MISSING', 'FAIL', 'RECORD_DEFECT'):
        gd = dict(pass_gate(g), status=st, codes=['SYNTHETIC_%s:%s' % (st, g)])
        for mode in ('parallel8', 'serial_with_exemption'):
            o14, o13 = reading(M, gates_with(M, **{g: gd}), mode), reading(M13, gates_with(M13, **{g: gd}), mode)
            rp['%s|%s|%s' % (g, st, mode)] = (o14 == o13, o14['outcome'])
t('D6_READING_IDENTICAL_R13_R14_FOR_EVERY_GATE_STATUS_MODE', all(v[0] for v in rp.values()),
  differs=[k for k, v in rp.items() if not v[0]], i4=dict((k, v[1]) for k, v in rp.items() if k.startswith('I4|')))
uses = [(n + 1, l.strip()[:150]) for n, l in enumerate(src14.decode().splitlines()) if 'GATE_RECORD_AFTER_SEAL_ALLOWED' in l]
def _cat(l):
    s_ = l.strip()
    if s_.startswith('#'):
        return 'comment'
    if s_.startswith('GATE_RECORD_AFTER_SEAL_ALLOWED ='):
        return 'definition'
    if 'in GATE_RECORD_AFTER_SEAL_ALLOWED' in s_:
        return 'membership'
    if 'join(GATE_RECORD_AFTER_SEAL_ALLOWED)' in s_:
        return 'joined_string'
    if 'for ' in s_ and 'GATE_RECORD_AFTER_SEAL_ALLOWED' in s_:
        return 'LOOP'
    return 'docstring_or_other'
cats = [(n, _cat(l), l) for n, l in uses]
t('D7_EVERY_USE_OF_THE_SET_IS_MEMBERSHIP_OR_A_JOINED_STRING', all(c in ('comment', 'definition', 'membership', 'joined_string') or (c == 'docstring_or_other' and n == 1106)
                                                                 for n, c, _ in cats) and not any(c == 'LOOP' for _, c, _ in cats),
  uses=cats)
REG13 = M13.producer_registry_from_obj(reg_obj(dict({g: TOKEN for g in EXP13}, I4=['c' * 64])))
g13 = ev(M13, 'I4', p_ok, ctx_for(REG13), RUNS)
r13p8 = reading(M13, gates_with(M13, I4=g13), 'parallel8')
t('D9_R13_CONTRADICTION_A114_POST_SEAL_I4_RECORD_READS_NO_RUN', g13['status'] == 'RECORD_DEFECT'
  and g13['codes'] == ['GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:I4'] and r13p8['outcome'] == 'NO_RUN'
  and load13['I4'].get('code') == 'PRODUCER_REGISTRY_GATE_RECORDS', r13_gate=short(g13), r13_reading=r13p8)
stale = [(n + 1, l.strip()[:160]) for n, l in enumerate(src14.decode().splitlines()) if 'I4) is registered by record sha' in l or 'SR_K always by sha' in l]
t('D8_STALE_COMMENTS_STILL_SAY_I4_BY_SHA', len(stale) >= 1, label='TESTED', lines=stale)

# ============================================================ write results
summary = {'n': len(RES), 'pass': sum(1 for r in RES if r['ok']), 'fail': [r['id'] for r in RES if not r['ok']]}
body = {'tool': 'lens_semantics_tests_c4v001.py', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'tag': TAG,
        'r14_sha256': SHA14, 'r13_sha256': SHA13, 'summary': summary, 'readings': RD, 'results': RES}
with open(OUT / 'LENS_SEMANTICS_TESTS.json', 'x') as f:
    f.write(json.dumps(body, indent=1, default=str) + '\n')
print(json.dumps(summary, indent=1))
for r in RES:
    print('%s %s' % ('OK  ' if r['ok'] else 'FAIL', r['id']))
