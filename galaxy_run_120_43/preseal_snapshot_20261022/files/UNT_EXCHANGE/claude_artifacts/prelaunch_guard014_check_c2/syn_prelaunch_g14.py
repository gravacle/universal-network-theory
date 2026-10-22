"""Synthetic deciding test (scratch only): does PRELAUNCH005 refuse a guard014 HEADLINE plan, and does a two-line
re-pinned successor produce a record that guard014's validate (binder c2v011's call form) replays exactly?
Reads real code files only (guard011, guard014, launcher015, monitor, driver r5, PRELAUNCH005) by path; every data
file is synthetic and lives under W. Writes only under W."""
import hashlib, json, os, subprocess, sys, types, copy
from pathlib import Path

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
W = Path(sys.argv[1]); W.mkdir(parents=True, exist_ok=False)
P5 = ART + '/step4_prelaunch_cx1/v005/step4_prelaunch_c2v005.py'
G11 = ART + '/step4_launch_packet_cx1/impl/step4_guard_c2v011.py'
G14 = ART + '/s1_successors_c2/step4_guard_c2v014.py'
L15 = ART + '/s1_successors_c2/step4_launcher_c2v015.py'
MON = ART + '/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'
DRV = ART + '/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py'
AUTH = {'identity': 'Claude2', 'role': 'coordinator_and_single_scientific_launch_owner'}
CP_INACTIVE = {'normal_qos_required': True, 'step2_route_a_inactive': True, 'campaign_inactive': True,
               'background_noncritical_lanes': True, 'sleep_assertion_required': True}
RULE = {'max_active': 3, 'poll_seconds': 60, 'ramp': 'previous_first_completed_route_a_iteration'}

def sha_b(b): return hashlib.sha256(b).hexdigest()
def pin(p): return {'path': str(p), 'sha256': sha_b(Path(p).read_bytes())}
def wb(name, b):
    p = W / name; p.write_bytes(b); return pin(p)
def wj(name, d): return wb(name, (json.dumps(d, sort_keys=True, indent=2) + '\n').encode())

# --- synthetic world
spec = wj('spec_SYN.json', {'galaxy': 'DDO154', 'admit': {}, 'numerics': {'uv_tail': {'enabled': True}},
                            'physical': {'distance_Mpc': 4.04}, 'synthetic': 'SYN_TEST_ONLY'})
ctx = wb('syn_ctx.py', b"import types\nO=types.SimpleNamespace(name='SYN')\ndef validate_block(b):\n    return None\n")
compare = wb('syn_compare.py', b"# synthetic compare\n")
addendum = wb('syn_addendum.md', b"synthetic addendum\n")
case_block = wj('syn_case_block.json', {'schema': 'SYN_CASE_BLOCK'})
prereg = wj('syn_prereg.json', {'binding_inputs': {'case_block': case_block}})
verdict = wj('syn_verdict.json', {'schema': 'SYN_VERDICT', 'test_mode': False,
                                  'decision': {'tests_read': True, 'outcome': 'ADOPT_TAIL'},
                                  'script_sha256': compare['sha256'], 'prereg': prereg, 'case_block': case_block})
seal = wj('syn_seal.json', {'sealed_by': AUTH, 'prereg': prereg, 'compare': compare,
                            'driver': {'sha256': 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'},
                            'frozen_addendum': addendum})
key = (compare['sha256'], prereg['sha256'], addendum['sha256'], 'SYN_VERDICT', verdict['sha256'])
policy = wb('syn_policy.py', ("APPROVED_V007_SEALS=frozenset({%r})\n"
                              "def check_numerics(ncfg,block,n,O=None,validate_block=None,driver_sha=None,synthetic=None):\n"
                              "    return None,{'ok':True,'reasons':[]}\n" % (key,)).encode())
registry = wj('syn_registry.json', {'schema': 'SYN_REGISTRY'})
cpr = wj('syn_cpr.json', {'schema': 'SYN_CPR'})
custody = wb('syn_custody.py', b"X=1\n")
enum = wb('syn_enum.py', b"X=2\n")
producer = wb('syn_producer.py', b"X=3\n")
adapter = wb('syn_adapter.py', (
    b"DIRECT_CONTEXT_API='UNT_STEP4_DIRECT_PREFLIGHT_CX1V001'\n"
    b"class _Ctx:\n"
    b"    def certificate_policy_gate(self):return {'ok':True,'reasons':[]}\n"
    b"    def certificate_check(self,spec,mode):return {'ok':True,'blockers':[],'mode':mode}\n"
    b"    def sensitivity_gate(self,spec):return {'ok':True,'reasons':[]}\n"
    b"    def prelaunch_check(self,spec):return {'normalized':sorted(spec)}\n"
    b"def build(C,config,*,guard,admission):\n"
    b"    return _Ctx()\n"))
config = wj('syn_config.json', {'numerics': {'verdict_artifact': verdict, 'sealed_prereg': prereg, 'compare': compare,
                                             'block': {'route_a': {'column_workers': 8}}},
                                'tail_readiness': {'certificate_registry': registry, 'certificate_policy_review': cpr,
                                                   'custody_deriver': custody, 'state_enumerator': enum,
                                                   'approved_certificate_producers': [producer]}})
drv = pin(DRV)
sources = {r['path']: r['sha256'] for r in (pin(G11), pin(G14), pin(L15), pin(MON), drv, ctx, policy, adapter,
                                            custody, enum, producer)}
review = wj('syn_source_review.json', {'schema': 'UNT_STEP4_SOURCE_REVIEW_CX1V001', 'status': 'TESTED', 'verdict': 'PASS',
                                       'approved_sources': sources, 'blocking_findings': [], 'reviewer': 'SYNTHETIC_TEST'})
CASE = 'SYN_HEADLINE_TRIAL'
caps = {'wall_cap_s': 144000, 'rss_cap_bytes': 137438953472, 'output_cap_bytes': 85899345920}
runs = W / 'runs'; runs.mkdir()
def call(prelaunch):
    o = str(runs / CASE)
    return dict({'case': CASE, 'spec': spec, 'driver': drv, 'spec_status': 'ROOT_FINAL', 'pending': [],
                 'prelaunch': prelaunch, 'tail_on': True, 'family': 'HEADLINE', 'distance_Mpc': 4.04,
                 'outdir': o, 'receipt': o + '.receipt.json', 'monitor_log': o + '.monitor.log'}, **caps)
def admission(prelaunch):
    return {'schema': 'UNT_STEP4_ADMISSION_CX1V001', 'authority': AUTH, 'status': 'ROOT_AUTHORIZED', 'plan': None,
            'sources': sources, 'source_review': review, 'context_module': ctx, 'direct_context': adapter,
            'adoption_policy': policy, 'config': config,
            'v007': {'seal': seal, 'verdict': verdict, 'prereg': prereg, 'compare': compare, 'addendum': addendum,
                     'case_block': case_block},
            'calls': {CASE: {'spec': spec, 'driver': drv, 'prelaunch': prelaunch}}, 'case_order': [CASE],
            'caps': {CASE: caps}, 'route_a_admission': RULE, 'core_priority': CP_INACTIVE, 'tail_off_policy': None}
def plan(guard, prelaunch):
    return {'schema': 'UNT_STEP4_LAUNCH_PLAN_CX1V001', 'binding_status': 'ROOT_BOUND', 'batch': 'HEADLINE',
            'guard': pin(guard), 'launcher': pin(L15), 'monitor': pin(MON), 'route_a_admission': RULE,
            'launcher_log': str(runs / 'launcher.log'), 'calls': [call(prelaunch)]}
A0 = wj('ADMISSION_CANDIDATE_A0.json', admission(None))
P0_g14 = wj('PLAN_PRELAUNCH_INPUT_G14.json', plan(G14, None))
P0_g11 = wj('PLAN_PRELAUNCH_INPUT_G11.json', plan(G11, None))
# successor: PRELAUNCH005 with L12-13 only re-pinned to guard014
src = Path(P5).read_bytes().decode()
old12 = "GUARD_PATH = Path('%s')" % G11; old13 = "GUARD_SHA256 = 'eb97e303b968dc941e2059ada813be95340662253c327a7b9a9634bb8a2c8033'"
assert src.count(old12) == 1 and src.count(old13) == 1
succ = src.replace(old12, "GUARD_PATH = Path('%s')" % G14).replace(old13, "GUARD_SHA256 = '%s'" % pin(G14)['sha256'])
S6 = W / 'step4_prelaunch_SYN_successor_g14.py'; S6.write_text(succ)
nd = [l for l in zip(src.splitlines(), succ.splitlines()) if l[0] != l[1]]
out = {'P5_sha256': pin(P5)['sha256'], 'successor_sha256': pin(S6)['sha256'], 'successor_changed_lines': len(nd)}

def run(prog, plan_ref, tag):
    od = W / ('out_' + tag); od.mkdir()
    r = subprocess.run([PY, '-I', '-B', str(prog), '--admission', A0['path'], '--admission-sha256', A0['sha256'],
                        '--plan', plan_ref['path'], '--plan-sha256', plan_ref['sha256'], '--output-dir', str(od)],
                       capture_output=True, text=True, cwd=str(W), env={'PATH': '/usr/bin:/bin'})
    last = (r.stderr.strip().splitlines() or [''])[-1]
    return {'rc': r.returncode, 'stdout': r.stdout.strip()[:400], 'stderr_last': last[:300], 'files': sorted(os.listdir(od))}, od
out['T1_P5_on_guard014_plan'], _ = run(P5, P0_g14, 't1')
out['T2_successor_on_guard014_plan'], od2 = run(S6, P0_g14, 't2')
out['T5_P5_on_guard011_plan'], od5 = run(P5, P0_g11, 't5')
out['T6_successor_on_guard011_plan'], _ = run(S6, P0_g11, 't6')
r2 = (od2 / 'PRELAUNCH_0000.json'); r5 = (od5 / 'PRELAUNCH_0000.json')
out['T2_T5_records_byte_equal'] = r2.exists() and r5.exists() and r2.read_bytes() == r5.read_bytes()

# --- binder c2v011 call form (L33-38), read-only: guard014.validate with the probe admission, execute_native=True
gb = Path(G14).read_bytes(); G = types.ModuleType('_syn_g14'); G.__file__ = G14
exec(compile(gb, G14, 'exec'), G.__dict__)
def binder_validate(rec_path, tag, tamper=False):
    pre = pin(rec_path)
    if tamper:
        d = json.loads(Path(rec_path).read_bytes()); d['checks']['normalized_sha256'] = '0' * 64
        pre = wj('TAMPERED_%s.json' % tag, d)
    P1 = wj('PLAN_FINAL_%s.json' % tag, plan(G14, pre))
    cfg = admission(pre); probe = copy.deepcopy(cfg); probe['plan'] = P1
    try:
        G.validate(P1, L15, _candidate_config=probe, _plan_bytes=Path(P1['path']).read_bytes(), disk_batch=False)
        return 'PASS'
    except Exception as e:
        return 'REFUSED:%s' % (e.args[0] if e.args else type(e).__name__)
if r2.exists():
    out['T3_g14_validate_with_successor_record'] = binder_validate(r2, 't3')
    out['T4_g14_validate_tampered_record'] = binder_validate(r2, 't4', tamper=True)
if r5.exists():
    out['T7_g14_validate_with_P5_g11_record'] = binder_validate(r5, 't7')
out['T8_g14_validate_no_prelaunch'] = (lambda: None)() or None
try:
    P1n = wj('PLAN_FINAL_t8.json', plan(G14, None)); pr = copy.deepcopy(admission(None)); pr['plan'] = P1n
    G.validate(P1n, L15, _candidate_config=pr, _plan_bytes=Path(P1n['path']).read_bytes(), disk_batch=False)
    out['T8_g14_validate_no_prelaunch'] = 'PASS'
except Exception as e:
    out['T8_g14_validate_no_prelaunch'] = 'REFUSED:%s' % (e.args[0] if e.args else type(e).__name__)
(W / 'RESULT.json').write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
print(json.dumps(out, indent=2, sort_keys=True))
