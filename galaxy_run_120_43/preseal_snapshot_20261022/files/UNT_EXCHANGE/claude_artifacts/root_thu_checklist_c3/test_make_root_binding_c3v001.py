"""Synthetic in-process tests of make_root_binding_c3v001 (no file is written). Fixtures: the fill v003 synthetic-mode
output (a synthetic C1 shape, never a C1) and its synthetic review, both in scratch. usage: python3 -I -B THIS TOOL FIXDIR OUT_JSON"""
import hashlib, importlib.util, json, sys
tool, fix, outp = sys.argv[1:4]
sp = importlib.util.spec_from_file_location('mrb', tool); M = importlib.util.module_from_spec(sp); sp.loader.exec_module(M)
H = M.validator()
def pin(p): return {'path': p, 'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest()}
C1S, POL = pin(fix + '/out_positive.json'), pin(fix + '/review_positive.json')
OLD_C1 = {'path': M.ART + '/c1_h1_c2/C1_H1_C2V001.json', 'sha256': '4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1'}
OLD_POL = {'path': M.ART + '/cert_policy_reviews_cx3/DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V001.json', 'sha256': 'f848888f7778124414302b8f216813f44dcdf89c594a4a3c066c17da887b6bdc'}
DRAFT = pin(M.ART + '/root_thu_checklist_c3/c1_successor/draft_c3v001/C1_H1_DRAFT_C2V003.json')
def attempt(c1, pol, mutate=None):
    b = M.build(c1, pol)
    if mutate: mutate(b)
    data = (json.dumps(b, indent=1, sort_keys=True) + '\n').encode()
    ref = {'path': fix + '/binding_inmem.json', 'sha256': hashlib.sha256(data).hexdigest()}
    class Pre(M.Snap):
        def doc(self, r):
            return json.loads(data) if r == ref else M.Snap.doc(self, r)
    try: H.validate_binding(Pre(), ref); return 'VALID'
    except (ValueError, OSError, KeyError, TypeError) as e: return 'REFUSED:' + str(e)[:80]
cases = {
 'positive_synthetic': (attempt(C1S, POL), 'VALID'),
 'old_c1': (attempt(OLD_C1, OLD_POL), 'A296_BINDING_NEW_C1_AND_POLICY_REQUIRED'),
 'policy_not_the_c1_tail_pin': (attempt(C1S, OLD_POL), 'A296_BINDING_POLICY_PIN_MISMATCH'),
 'draft_as_c1': (attempt(DRAFT, POL), 'A296_BINDING_POLICY_PIN_MISMATCH'),
 'guard_swapped_to_old': (attempt(C1S, POL, lambda b: b.update(guard={'path': M.ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py', 'sha256': '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'})), 'A296_BINDING_REVIEWED_SOURCE_PINS'),
 'status_unbound': (attempt(C1S, POL, lambda b: b.update(status='UNBOUND_TEMPLATE')), 'A296_BINDING_UNBOUND_OR_SCHEMA'),
 'extra_field': (attempt(C1S, POL, lambda b: b.update(note='x')), 'A296_BINDING_FIELDS'),
}
res = {k: {'got': g, 'want': w, 'pass': (g == w) if w == 'VALID' else g.startswith('REFUSED:' + w)} for k, (g, w) in cases.items()}
rec = {'schema': 'TEST_MAKE_ROOT_BINDING_C3V001', 'tool_sha256': hashlib.sha256(open(tool, 'rb').read()).hexdigest(), 'n': len(res), 'passed': sum(v['pass'] for v in res.values()), 'cases': res}
# hardening: the synthetic fixture C1 is refused by real_c1_checks (outside the pinned validator)
try:
    M.real_c1_checks(M.Snap(), C1S, POL); hard = 'NOT_REFUSED'
except ValueError as e: hard = 'REFUSED:' + str(e)[:60]
try:
    M.real_c1_checks(M.Snap(), DRAFT, POL); hard2 = 'NOT_REFUSED'
except ValueError as e: hard2 = 'REFUSED:' + str(e)[:60]
rec['hardening'] = {'synthetic_c1': hard, 'draft_c1': hard2, 'pass': hard.startswith('REFUSED:C1_SCHEMA') and hard2.startswith('REFUSED:C1_SCHEMA')}
rec['passed_all'] = rec['passed'] == rec['n'] and rec['hardening']['pass']
open(outp, 'x').write(json.dumps(rec, indent=1, sort_keys=True) + '\n')
print(json.dumps({'n': rec['n'], 'passed': rec['passed'], 'hardening': rec['hardening']['pass'], 'failed': {k: v['got'] for k, v in res.items() if not v['pass']}}))
