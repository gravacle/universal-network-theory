"""Static byte derivation for 0829. No generators or scientific modules execute."""
import ast
import hashlib
import json
import subprocess
from pathlib import Path
H = Path(__file__).parent
A = H.parent
CX = A / 'calib_tail_readiness_cx2'
PH = A / 'h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4'
G5 = A / 'b1_policy_successor_c4/tools/make_b1_cascade_c4v002.py'
G6 = A / 'h3_campaign_path_c2/make_campaign_cascade_c2v004.py'
R7 = CX / 'v006r7/adoption_policy_cx2v006r7.py'
C9 = CX / 'v006r9/calibration_core_cx2v006r9.py'
WQ = A / 'h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py'
ET = A / 'h3_campaign_path_c2/h3_campaign_entry_c2v004.py'
N = ('adoption_policy_cx2v006r12_c4.py', 'calibration_core_cx2v006r12_c4.py',
     'calibration_orchestrator_cx2v006r12_c4_q5b1.py', 'h3_campaign_entry_cx2v006r12_c4.py')
inputs = []
def sha(b):
    return hashlib.sha256(b).hexdigest()
def read(p, expected=None):
    b = p.read_bytes()
    if expected is not None and sha(b) != expected:
        raise ValueError('source pin ' + str(p))
    inputs.append({'path': str(p), 'sha256': sha(b)})
    return b
def replace(b, old, new):
    if b.count(old) != 1:
        raise ValueError('replacement occurrence')
    return b.replace(old, new)
def literals(b, name):
    values = [ast.literal_eval(n.value) for n in ast.parse(b).body if isinstance(n, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    if len(values) != 1:
        raise ValueError('literal assignment ' + name)
    return values[0]
g5 = read(G5, 'a7a5fe58d509b99f14cb000305633c6f192ac71f5093f4ec5fa1a2fa6f1a1f35')
g6 = read(G6, '5014b04f0de3cf2fc0289dcabe519e0056f9395302cfd1b9b4082b4d045b228a')
replacements = literals(g5, 'POLICY_REPLACEMENTS')
if replacements != literals(g6, 'POLICY_REPLACEMENTS'):
    raise ValueError('policy replacement lists differ')
p = read(R7, '7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d')
for tag, old, new in replacements:
    p = replace(p, old.encode(), new.encode())
r10 = read(CX / 'v006r10_c4/adoption_policy_cx2v006r10_c4.py',
           '93d9c0acdb3e9fd40ec63ed0db7c1356b6d2b025eeb5bcde57a2ffebdbd04ba3')
if p != r10:
    raise ValueError('P1-P4 not r10')
c = read(C9, 'a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605')
c = replace(c, b"    p = Path(__file__).resolve().parent.parent/'v006r7/adoption_policy_cx2v006r7.py'\n",
            ("    p = Path(__file__).resolve().parent.parent/'v006r12_c4/" + N[0] + "'\n").encode())
c = replace(c, b'7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d', sha(p).encode())
w = read(WQ, '7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229')
w = replace(w, b"M=load(HERE/'calibration_core_cx2v006r10_c4.py','_cx2v006r1',expected='dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6')\n",
            ("M=load(HERE/'" + N[1] + "','_cx2v006r1',expected='" + sha(c) + "')\n").encode())
e = read(ET, 'cbdf0d49b8bfa09bccf8ba1ebfb518f8c00b663c2564db7c3a02c8b7a86e116d')
e = replace(e, ("WRAPPER = Path('" + str(WQ) + "')\n").encode(),
            ("WRAPPER = Path('" + str(CX / 'v006r12_c4' / N[2]) + "')\n").encode())
e = replace(e, b"WRAPPER_SHA = '7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229'\n",
            ("WRAPPER_SHA = '" + sha(w) + "'\n").encode())
rows = []
for n, b in zip(N, (p, c, w, e)):
    saved = read(PH / n)
    if b != saved:
        raise ValueError('placeholder reconstruction mismatch ' + n)
    rows.append({'name': n, 'sha256': sha(b), 'source_reconstruction_equal': True})
controls = json.loads(read(H / 'STAGE_GATE_CONTROLS_CX3V003.json',
                          '1dfc393f7b223d55b03e21627accda1e8a868a9b4df90c196377dba299263cb5'))
if controls['count'] != 45 or not all(x['passed'] for x in controls['checks']):
    raise ValueError('stage controls')
for path in [
    H / 'check_verdict_gates_cx3v003.py',
    A / 'h3_campaign_path_c2/regenerate_h3_c2v004.py',
    A / 'verdict_day_sheet_cx1/VERDICT_DAY_COMMAND_SHEET_CX1V001.md',
    A / 'b1_policy_successor_c4/tools/run_fenced_c4st2.py',
    A / 'b1_policy_successor_c4/tools/fence_c4v002.py']:
    read(path)
result = {
    'schema': 'CX3_0829_PARAMETRIC_PRE_REVIEW_V001',
    'date_u': subprocess.check_output(['/bin/date', '-u'], text=True).strip(),
    'status': 'TESTED_SOURCE_RECONSTRUCTION_AND_SYNTHETIC_GATES',
    'inputs': inputs, 'script': {'path': str(Path(__file__)), 'sha256': sha(Path(__file__).read_bytes())},
    'placeholder_reconstruction': rows,
    'policy_bytes_equal_between_r11_and_r12_for_same_tuple': True,
    'allowed_r11_lines': [13, 16],
    'allowed_r12_lines': [[13, 16], [202], [29], [61]],
    'allowed_changes': [
        'policy: fixed A126 registration comment and sole approved tuple (C,P,A,SCHEMA,V)',
        'core: exact SHA256 of final policy',
        'wrapper: exact SHA256 of final core',
        'entry: exact SHA256 of final wrapper'],
    'template_scope': 'All other bytes fixed, including names/paths, newlines, and _resolve_source literal.',
    'synthetic_stage_checks_passed': 45,
    'actual_final_output_sha256': None,
    'actual_V': None,
    'actual_sheet_dry_run': 'NOT_RUN_FUTURE_VERDICT_SHA_NOT_AVAILABLE',
    'formal_dependency': 'V is SHA256 of complete future report bytes. It changes policy bytes and all derived chain hashes.',
    'actual_verdict_review': 'UNTESTED',
    'scientific_execution': 'NONE',
}
out = H / 'PRESTAGE_0829_CX3V001.json'
with out.open('x') as f:
    json.dump(result, f, indent=2, sort_keys=True); f.write('\n')
print(json.dumps({'result': {'path': str(out), 'sha256': sha(out.read_bytes())},
                  'source_reconstructions': 4, 'synthetic_controls': 45}))
