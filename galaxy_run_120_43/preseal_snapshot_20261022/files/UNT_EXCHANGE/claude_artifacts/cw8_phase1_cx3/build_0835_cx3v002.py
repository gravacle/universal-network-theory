"""0835/A270: exclusive F1-F3 successor and its necessary consumer pins."""
import ast
import difflib
import hashlib
import json
from pathlib import Path
import subprocess

H = Path(__file__).parent
INPUTS, OUTPUTS = [], []
def pin(p):
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
def read(name, expected):
    p = H/name
    assert pin(p)['sha256'] == expected
    INPUTS.append(pin(p))
    return p.read_text()
def write(name, text):
    ast.parse(text)
    p = H/name
    with p.open('x') as f:
        f.write(text)
    OUTPUTS.append(pin(p))
    return OUTPUTS[-1]
def rep(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)

pold = read('phase1_ngc_launch_cx3cw8v001.py',
            '04dfc429e335458494fa377f2f46e8d54adbe7e0f0b9a4c3b2121c6b0964f0c2')
pnew = rep(pold, 'TOOL_NAME = "P112_LAUNCHER_CX3CW8V001"',
           'TOOL_NAME = "P112_LAUNCHER_CX3CW8V002"')
pnew = rep(pnew, '    A249 passes Phase 2 as monitor_ceiling_utc. Phase 1 only limits Phase-1\n'
           '    admissions and reporting; it never stops an active run.',
           '    A270: Phase 2 is the only admission and monitor ceiling. Phase 1\n'
           '    is a reporting cutoff, including for first admissions and reruns.')
for line in ("    remaining_wall(phase_ceiling_utc, now_utc)\n",
             "    remaining_wall(ctx.cfg['phase1_ceiling_utc'], now_utc)\n",
             "    remaining_wall(ctx.cfg['phase1_ceiling_utc'], basis['decision_utc'])\n"):
    pnew = rep(pnew, line, '')
pnew = rep(pnew,
    "    if timestamp(now_utc) >= cutoff:\n"
    "        return {'status': 'UNEVALUATED_SCHEDULE_CEILING', 'terminal': None,\n"
    "                'continues_for_next_phase': True, 'stop_requested': False}\n"
    "    return {'status': ('HELD_FOR_FIX' if held_for_fix(actual) else\n"
    "                       'HELD_FOR_CAUSE' if held_for_cause(actual, authenticated_causes) else 'NOT_TERMINAL'),\n"
    "            'terminal': None, 'stop_requested': False}\n",
    "    hold = ('HELD_FOR_FIX' if held_for_fix(actual) else\n"
    "            'HELD_FOR_CAUSE' if held_for_cause(actual, authenticated_causes) else None)\n"
    "    if hold is not None:\n"
    "        return {'status': hold, 'terminal': None, 'stop_requested': False}\n"
    "    if timestamp(now_utc) >= cutoff:\n"
    "        return {'status': 'UNEVALUATED_SCHEDULE_CEILING', 'terminal': None,\n"
    "                'continues_for_next_phase': True, 'stop_requested': False}\n"
    "    return {'status': 'NOT_TERMINAL', 'terminal': None, 'stop_requested': False}\n")
pnew = rep(pnew,
    '    """Map only bound, independently rederived closed receipts; unknown stays absent."""',
    '    """Map bound causes; explicit non-model records release cause holds without counting."""')
pnew = rep(pnew,
    "        if not cause['model_outcome']:\n"
    "            if cause['model_outcome_reason'] in KNOWN_NONPHYSICS_CAUSES:\n"
    "                mapped[key] = None\n"
    "            continue\n",
    "        if not cause['model_outcome']:\n"
    "            # A270: retain the pinned record, but release an uncounted solo\n"
    "            # retry even when its reason awaits later readable classification.\n"
    "            mapped[key] = None\n"
    "            continue\n")
def functions(text):
    return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(text).body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
pf0, pf1 = functions(pold), functions(pnew)
changed = sorted(k for k in pf0 if pf0[k] != pf1[k])
assert changed == ['_commit_plan_check', 'authenticated_causes', 'fresh_launch_plan',
                   'next_attempt', 'phase_disposition'], changed
lp = write('phase1_ngc_launch_cx3cw8v002.py', pnew)

bold = read('roster_builder_c2v007_cx3cw8v001.py',
            'e6102ba15542e6b2a10c073b4f8647c48facaadf2209d664818e81ee6058da31')
bnew = rep(bold, "BUILDER_NAME = 'roster_builder_c2v007_cx3cw8v001'",
           "BUILDER_NAME = 'roster_builder_c2v007_cx3cw8v002'")
bnew = rep(bnew, "P112_REVIEWED_SHA = '04dfc429e335458494fa377f2f46e8d54adbe7e0f0b9a4c3b2121c6b0964f0c2'",
           'P112_REVIEWED_SHA = '+repr(lp['sha256']))
bnew = rep(bnew, "P112_REVIEWED_SHAS = frozenset((P112_REVIEWED_SHA,\n"
           "    '8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9'))",
           "P112_REVIEWED_SHAS = frozenset((P112_REVIEWED_SHA,))")
assert functions(bold) == functions(bnew)
bp = write('roster_builder_c2v007_cx3cw8v002.py', bnew)
gold = read('g26_freeze_cx3cw8v001.py',
            'e0e3139816d5337bb54b08bb4d9ddfd3cbb8dfe90dab5b37bc1c1d365437f5af')
gnew = rep(gold, str(H/'roster_builder_c2v007_cx3cw8v001.py'), bp['path'])
gnew = rep(gnew, 'e6102ba15542e6b2a10c073b4f8647c48facaadf2209d664818e81ee6058da31', bp['sha256'])
assert functions(gold) == functions(gnew)
gp = write('g26_freeze_cx3cw8v002.py', gnew)
diffs = {}
for name, old, new in [('launcher', pold, pnew), ('builder', bold, bnew), ('G26', gold, gnew)]:
    diffs[name] = ''.join(difflib.unified_diff(old.splitlines(keepends=True),
                              new.splitlines(keepends=True), fromfile=name+'_v001', tofile=name+'_v002'))
doc = {'date_u': subprocess.check_output(['/bin/date','-u'],text=True).strip(),
       'schema': 'CW8_0835_BUILD_CX3V002', 'inputs': INPUTS, 'outputs': OUTPUTS,
       'launcher_functions_changed': changed,
       'builder_and_G26_function_AST_unchanged': True,
       'additional_nonfunctional_changes': ['tool/version labels', 'consumer source pins',
           'only v002 launcher accepted, per 0835 single launcher / cx2v004 not adopted'],
       'diffs': diffs, 'tests': 'PENDING', 'scientific_execution': 'NONE'}
out = H/'BUILD_0835_CX3V002.json'
with out.open('x') as f:
    json.dump(doc,f,indent=2,sort_keys=True); f.write('\n')
print(json.dumps({'record': pin(out), 'outputs': OUTPUTS, 'functions_changed': changed}))
