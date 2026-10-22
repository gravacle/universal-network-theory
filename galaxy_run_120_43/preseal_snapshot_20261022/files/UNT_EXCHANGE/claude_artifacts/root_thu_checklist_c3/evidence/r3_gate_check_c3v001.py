"""Claude3 deputy check (D016 return, Codex3 0709): run the three A296 R3 signer reviews through
(1) the pinned stage v002 review_gate, extracted by AST from its pinned bytes, with an in-memory snapshot, and
(2) a literal restatement of the core adapt_saved_eps review predicates (L405-413).
Read-only. No adapt/prepare call, no producer execution, no writes except --out (exclusive create).
usage: python3 -I -B r3_gate_check_c3v001.py --out ABS_NEW_JSON"""
import ast, copy, hashlib, json, os, sys
from pathlib import Path
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
I = ART/'eps_rule_successor_cx2/integration'
STAGE = {'path': str(I/'stage/cp1_saved_eps_stage_cx2v002.py'), 'sha256': '0c9d0243c57bab053bb0a73e00183b0366b0c83b6eac33d9d5344b136238ccc5'}
BRIDGE_SHA = '1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4'
CORE_SHA = '1a44bc59a5fc6a72c381d3c0c0875b6aa154c21fc108730d67c9ec529a39d9d7'
PRODUCERS = [BRIDGE_SHA, '669f0640b4a9e2a005e91245c27223499dc96a35189c6b4852a11a1e99190e3b',
             '618ba8fa9db2e7d7747c007d00f0ec64fd30083a164b01ad8ff60195e1b0d341', 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231']
REVIEWS = {'302': 'ca3fb3a2a118a9766fa9aae00ccd4b668e8835f4fcf61d0d96c6a13109f6936c',
           '501': '5f9fd691252271c154602f062b2e4380af4828334215dcce86a87e1b721d7818',
           '504': '48a599e2074a81e9e7c07e7bdc7482f6c4dd3aa06e4c4c977afd136469aee2ac'}
RDIR = ART/'a296_r3_signer_reviews_cx3'
OUT_ROOT_OK = ART/'root_a296_adapt_out_HYPOTHETICAL_not_created'   # lexical only; never created
def sha(b): return hashlib.sha256(b).hexdigest()
def pinned(ref):
    raw = Path(ref['path']).read_bytes(); assert sha(raw) == ref['sha256'], ref; return raw
src = pinned(STAGE)
want_fns = {'need', 'canonical', 'lexical', 'safe_existing', 'read', '_functions', 'review_gate'}
tree = ast.parse(src)
nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in want_fns]
consts = [n for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
          and n.targets[0].id in {'ART', 'BASE', 'BRIDGE', 'COMMON'}]
assert {n.name for n in nodes} == want_fns and len(consts) == 4
ns = {'__name__': 'stage_extract', 'ast': ast, 'json': json, 'hashlib': hashlib, 'os': os, 'Path': Path}
exec(compile(ast.Module(body=consts + nodes, type_ignores=[]), STAGE['path'] + ':extract', 'exec'), ns)
assert ns['BRIDGE']['sha256'] == BRIDGE_SHA
class Snap:
    def __init__(self, override=None): self.override = override
    def doc(self, ref):
        if self.override is not None: return copy.deepcopy(self.override)
        return json.loads(pinned(ref))
def core_predicates(rv, numeric_ref, details, trace):
    bad = []
    if not (isinstance(rv, dict) and rv.get('schema') == 'UNT_POINT_EPS_REVIEW_CX2V001' and rv.get('verdict') == 'APPROVED'): bad.append('EPS_REVIEW_NOT_APPROVED')
    if rv.get('test_fixture_only'): bad.append('EPS_SYNTHETIC_REVIEW_NOT_ADMISSIBLE')
    if not (rv.get('numeric_ref') == numeric_ref and rv.get('point_sha256') == details['point_sha256'] and rv.get('custody_sha256') == details['custody_sha256']): bad.append('EPS_REVIEW_EXACT_BYTES_OR_SCOPE_MISMATCH')
    if rv.get('accepts_registered_numerical_estimate_not_rigorous_sup') is not True: bad.append('EPS_REVIEW_NUMERICAL_CONVENTION_UNRESOLVED')
    if rv.get('adapter_sha256') != BRIDGE_SHA: bad.append('EPS_REVIEW_ADAPTER_MISMATCH')
    if not (rv.get('accepts_a296_negligible_shells') is True and rv.get('a296_acceptance') == trace): bad.append('EPS_A296_REVIEW_EXACT_ACCEPTANCE_REQUIRED')
    return bad
def gate(review_ref, stage, context, *, approved, lanes, out_root):
    try:
        ns['review_gate'](review_ref, stage, context, approved_review_sha256=approved, approved_signer_lanes=lanes,
                          approved_producer_sha256=PRODUCERS, output_root=str(out_root)); return 'PASS'
    except ValueError as e: return 'REFUSED:' + str(e)[:160]
out = {'schema': 'R3_GATE_CHECK_C3V001', 'stage': STAGE, 'self_sha256': sha(Path(__file__).read_bytes()), 'rows': {}}
allok = True
for r, rsha in REVIEWS.items():
    rp = RDIR/('REVIEW_ROW%s_CX3V001.json' % r)
    assert not rp.is_symlink() and rp.is_file()
    rraw = rp.read_bytes(); assert sha(rraw) == rsha, (r, sha(rraw))
    rv = json.loads(rraw)
    so = json.loads((I/('stage/STAGE_ONLY_ROW%s_CX2V003.json' % r)).read_bytes())
    req = json.loads(Path(so['request']['path']).read_bytes())
    start = json.loads(Path(req['point_start']['path']).read_bytes())
    succ = json.loads(pinned(so['record']))
    context = {'snapshot': Snap(), 'start': {'operator_lane': start['operator_lane']}, 'successor': succ}
    ref = {'path': str(rp), 'sha256': rsha}
    res = {'review': ref, 'reviewer_lane': rv.get('reviewer_lane'), 'operator_lane': start['operator_lane']}
    res['stage_gate'] = gate(ref, so, context, approved=rsha, lanes=['Codex3'], out_root=OUT_ROOT_OK)
    res['core_predicates'] = core_predicates(rv, so['record'], {'point_sha256': so['key'], 'custody_sha256': so['custody_sha256']}, so['a296_acceptance']) or 'PASS'
    neg = {}
    def mut(name, f, *, lanes=('Codex3',), out_root=OUT_ROOT_OK, approved=rsha):
        m = copy.deepcopy(rv); f(m)
        g = gate(ref, so, dict(context, snapshot=Snap(m)), approved=approved, lanes=list(lanes), out_root=out_root)
        c = core_predicates(m, so['record'], {'point_sha256': so['key'], 'custody_sha256': so['custody_sha256']}, so['a296_acceptance'])
        neg[name] = {'stage': g, 'core': c or 'PASS', 'refused_by_some_gate': g != 'PASS' or bool(c)}
    mut('verdict_rejected', lambda m: m.update(verdict='REJECTED'))
    mut('lane_Codex2', lambda m: m.update(reviewer_lane='Codex2'))
    mut('lane_operator_Claude2', lambda m: m.update(reviewer_lane='Claude2'))
    mut('lane_not_root_approved', lambda m: None, lanes=('Codex1',))
    mut('adapter_is_core_not_bridge', lambda m: m.update(adapter_sha256=CORE_SHA))
    mut('trace_float_to_int', lambda m: m['a296_acceptance'].update(accepted_shells=[[int(a), int(b)] for a, b in m['a296_acceptance']['accepted_shells']]))
    mut('trace_drop_key', lambda m: m['a296_acceptance'].pop('retains_discrete_failure'))
    mut('numeric_ref_extra_key', lambda m: m['numeric_ref'].update(note='x'))
    mut('template_marker', lambda m: m.update(note='<FILL me>'))
    mut('not_distinct_flag', lambda m: m.update(distinct_from_producer_lane=False))
    mut('a296_flag_false', lambda m: m.update(accepts_a296_negligible_shells=False))
    mut('review_inside_output_root', lambda m: None, out_root=RDIR)
    mut('output_root_is_claude_artifacts', lambda m: None, out_root=ART)
    mut('unapproved_review_sha', lambda m: None, approved='0' * 64)
    res['negative_controls'] = neg
    res['all_negatives_refused'] = all(v['refused_by_some_gate'] for v in neg.values())
    # trace-only mutants that python == would accept: report which gate catches them
    res['float_to_int_caught_by'] = 'stage canonical' if neg['trace_float_to_int']['stage'] != 'PASS' else 'NONE'
    ok = res['stage_gate'] == 'PASS' and res['core_predicates'] == 'PASS' and res['all_negatives_refused']
    res['ok'] = ok; allok &= ok
    out['rows'][r] = res
out['ok'] = allok
o = Path(sys.argv[sys.argv.index('--out') + 1]); assert o.is_absolute()
fd = os.open(str(o), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
with os.fdopen(fd, 'w') as f: f.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
print(json.dumps({'ok': allok, **{r: [v['stage_gate'], v['core_predicates'], v['all_negatives_refused'], v['float_to_int_caught_by']] for r, v in out['rows'].items()}}))
