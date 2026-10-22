# Claude4 lens_diff, run ONLY through tools/run_fenced_c4st2.py.  Imports r13 and r14 (no CLI, no driver, no comparator run) and
# calls pure functions on SYNTHETIC inputs: (a) the runtime token tuple; (b) the registry loader with a minimal synthetic registry
# carrying PRODUCED_AFTER_THE_SEAL on one gate at a time (no file pins); (c) gate_record_sha_codes on a synthetic registry dict;
# (d) write_field_contract into this review folder, compared with the published FIELDS files.
import difflib, hashlib, importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
GEN = HERE / 'gen'
OUT = HERE / 'out' / 'TOKEN_AND_CONTRACT_C4.json'
C = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2')
SRC = {'r13': (C / 'r13/kmax_tail_compare_c2v007_r13_cx3v001.py', 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'),
       'r14': (C / 'r14/kmax_tail_compare_c2v007_r14_cx1v001.py', 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7')}
res = {}
M = {}
for tag, (p, want) in SRC.items():
    b = p.read_bytes()
    got = hashlib.sha256(b).hexdigest()
    if got != want:
        raise SystemExit('SHA MISMATCH %s %s' % (tag, got))
    spec = importlib.util.spec_from_file_location('cmp_%s_c4review' % tag, str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    M[tag] = m
    res[tag] = {'sha256': got, 'GATE_RECORD_AFTER_SEAL_ALLOWED': list(m.GATE_RECORD_AFTER_SEAL_ALLOWED),
                'GATE_RECORD_SHA_REQUIRED': list(m.GATE_RECORD_SHA_REQUIRED), 'ALL_GATES': list(m.ALL_GATES),
                'IDENTITY_GATES': list(m.IDENTITY_GATES), 'MODE_GATES': list(m.MODE_GATES)}
assert res['r13']['ALL_GATES'] == res['r14']['ALL_GATES']
GATES = res['r14']['ALL_GATES']

def loader_accepts(m, g):
    obj = {'schema': m.PRODUCER_REGISTRY_SCHEMA, 'producers': {}, 'identity_comparators': [], 'identity_tokens': {},
           'gate_records': {g: m.GATE_RECORD_AFTER_SEAL}, 'gq_all_nodes_counts': {}}
    try:
        m.producer_registry_from_obj(obj)
        return True, None
    except m.Refused as e:
        return False, [getattr(e, 'refusal_code', None), str(e)]

tok = {}
for g in GATES:
    a13, e13 = loader_accepts(M['r13'], g)
    a14, e14 = loader_accepts(M['r14'], g)
    c13 = M['r13'].gate_record_sha_codes(g, 'a' * 64, {'gate_records': {g: M['r13'].GATE_RECORD_AFTER_SEAL}})
    c14 = M['r14'].gate_record_sha_codes(g, 'a' * 64, {'gate_records': {g: M['r14'].GATE_RECORD_AFTER_SEAL}})
    tok[g] = {'loader_r13': a13, 'loader_r14': a14, 'sha_codes_r13': c13, 'sha_codes_r14': c14,
              'refusal_code_r14': e14[0] if e14 else None, 'refusal_msg_r14': e14[1] if e14 else None,
              'refusal_msg_r13': e13[1] if e13 else None}
res['token_by_gate'] = tok
res['loader_changed_gates'] = [g for g in GATES if tok[g]['loader_r13'] != tok[g]['loader_r14']]
res['sha_codes_changed_gates'] = [g for g in GATES if tok[g]['sha_codes_r13'] != tok[g]['sha_codes_r14']]
res['loader_accepts_r14'] = [g for g in GATES if tok[g]['loader_r14']]
res['loader_refuses_r14'] = [g for g in GATES if not tok[g]['loader_r14']]
A114_REFUSED = sorted(set(('B0', 'B1', 'B2', 'B3', 'EPS', 'GQ', 'LO', 'LO_NGC', 'DOUBLING') + tuple(res['r14']['IDENTITY_GATES'])))
res['A114_MUST'] = {'I4_accepted_loader': tok['I4']['loader_r14'] is True, 'I4_sha_codes_empty': tok['I4']['sha_codes_r14'] == [],
                    'refused_list': A114_REFUSED,
                    'all_refused_loader': all(tok[g]['loader_r14'] is False for g in A114_REFUSED),
                    'all_refused_sha_codes': all(tok[g]['sha_codes_r14'] == ['GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:%s' % g]
                                                 for g in A114_REFUSED)}
res['gates_refused_but_not_in_A114_list'] = [g for g in res['loader_refuses_r14'] if g not in A114_REFUSED]
# the refusal message renders the token set; compare r13 vs r14 for EPS
res['refusal_msg_EPS'] = {'r13': tok['EPS']['refusal_msg_r13'], 'r14': tok['EPS']['refusal_msg_r14']}

# (d) regenerate the field contract of each round into this folder and compare with the published files
GEN.mkdir()
files = {'r12_FIELDS_R12_CX3V002': C / 'r12/FIELDS_R12_CX3V002.md', 'r13_FIELDS_R13_CX3V001': C / 'r13/FIELDS_R13_CX3V001.md',
         'r14_FIELDS_R14_CX1V001': C / 'r14/FIELDS_R14_CX1V001.md', 'r14_FIELDS_R14_CX1V002': C / 'r14/FIELDS_R14_CX1V002.md'}
fb = {k: v.read_bytes() for k, v in files.items()}
res['published_fields'] = {k: {'path': str(files[k]), 'sha256': hashlib.sha256(v).hexdigest(), 'bytes': len(v)} for k, v in fb.items()}
regen = {}
for tag in ('r13', 'r14'):
    p = GEN / ('FIELDS_REGEN_%s_C4.md' % tag)
    M[tag].write_field_contract(str(p))
    regen[tag] = p.read_bytes()
res['regen'] = {tag: {'path': str(GEN / ('FIELDS_REGEN_%s_C4.md' % tag)), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
                for tag, b in regen.items()}
res['regen_r14_eq_FIELDS_R14_CX1V001'] = regen['r14'] == fb['r14_FIELDS_R14_CX1V001']
res['regen_r13_eq_FIELDS_R12_CX3V002'] = regen['r13'] == fb['r12_FIELDS_R12_CX3V002']
res['regen_r13_vs_r14_diff'] = ''.join(difflib.unified_diff(regen['r13'].decode().splitlines(True), regen['r14'].decode().splitlines(True),
                                                             'regen_r13', 'regen_r14', n=0))
with open(OUT, 'x') as f:
    json.dump(res, f, indent=1, default=str)
show = {k: res[k] for k in ('loader_changed_gates', 'sha_codes_changed_gates', 'loader_accepts_r14', 'loader_refuses_r14', 'A114_MUST',
                            'gates_refused_but_not_in_A114_list', 'refusal_msg_EPS', 'published_fields', 'regen',
                            'regen_r14_eq_FIELDS_R14_CX1V001', 'regen_r13_eq_FIELDS_R12_CX3V002')}
show['runtime_tuples'] = {t: res[t]['GATE_RECORD_AFTER_SEAL_ALLOWED'] for t in ('r13', 'r14')}
print(json.dumps(show, indent=1))
print(res['regen_r13_vs_r14_diff'])
