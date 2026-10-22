"""Exclusive successor assembly. No execution of launcher operations."""
import ast
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'phase1_ngc_launch_kit_cx2v003/phase1_ngc_launch_cx2v003.py'
raw = BASE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'af0210715f658c43f73f37a5e6e733f7a48dc374caa1b8af5a0defe3987854d7'
s = raw.decode()
tree = ast.parse(s)
lines = s.splitlines(keepends=True)
components = ['policy_core_draft002.py', 'raw_status_draft001.py', 'launch_commit_draft002.py',
              'cause_adapter_draft001.py', 'context_policy_draft001.py']
replacement, extra, manifest = {}, [], []
for file in components:
    r = (HERE / file).read_bytes()
    text = r.decode()
    manifest.append((file, hashlib.sha256(r).hexdigest()))
    for n in ast.parse(text).body:
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
            continue
        lo = min([n.lineno] + [x.lineno for x in getattr(n, 'decorator_list', [])]) - 1
        segment = ''.join(text.splitlines(keepends=True)[lo:n.end_lineno])
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            replacement[n.name] = segment
        else:
            extra.append(segment)

replacement['terminal_prefix'] = replacement['terminal_prefix'].replace(
    "cls = current.get('status_class')",
    "cls = current.get('status_class')\n        if current.get('_known_nonphysics'):\n            continue")
replacement['terminal_prefix'] = replacement['terminal_prefix'].replace(
    "if len({r.get('spec_sha256') for r in actual[:i + 1]}) != 1:",
    "if current['pins']['monitor_receipt']['sha256'] == previous['pins']['monitor_receipt']['sha256']:\n            continue\n        if len({r.get('spec_sha256') for r in actual[:i + 1]}) != 1:")
replacement['held_for_cause'] = replacement['held_for_cause'].replace(
    "a, b = actual[-2:]",
    "a, b = actual[-2:]\n    if a.get('_known_nonphysics') or b.get('_known_nonphysics'):\n        return False")


def change_function(name, transform):
    n = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    lo = min([n.lineno] + [x.lineno for x in n.decorator_list]) - 1
    replacement[name] = transform(''.join(lines[lo:n.end_lineno]))


def once(text, a, b):
    assert text.count(a) == 1, (a, text.count(a))
    return text.replace(a, b)


def history(text):
    text = once(text, 'inspect_next=True, assembly=False):',
                'inspect_next=True, assembly=False, allow_incomplete=False):')
    text = once(text, 'actual, nonattempts, closed_pins, trailing = [], [], [], None',
                'actual, nonattempts, closed_pins, trailing = [], [], [], None\n    pending = []')
    text = once(text, 'raise Refusal("ATTEMPT_ACTIVE" if live else "MONITOR_ENDED_NO_RECEIPT", (name, k))', '''state = "ATTEMPT_ACTIVE" if live else "MONITOR_ENDED_NO_RECEIPT"
            if allow_incomplete:
                pending.append({'attempt': k, 'status': state, 'record': rec['record_pin']})
                continue
            raise Refusal(state, (name, k))''')
    text = once(text, 'need(Path(path).is_file(), "ATTEMPT_NEEDS_CLOSE", (name, k))', '''if not Path(path).is_file() and allow_incomplete:
            pending.append({'attempt': k, 'status': 'ATTEMPT_NEEDS_CLOSE',
                            'record': rec['record_pin'], 'monitor_receipt': monitor_pin})
            continue
        need(Path(path).is_file(), "ATTEMPT_NEEDS_CLOSE", (name, k))''')
    a = text.index('        if not assembly:')
    b = text.index('        trailing = None', a)
    text = text[:a] + '''        obj = strict_json(closed_raw)
        actual.append(verify_closed_receipt(ctx, call, rec, monitor_pin, monitor, pin, obj))
''' + text[b:]
    return once(text, '"consecutive_nonattempts": streak, "refusals": refusals}',
                '"consecutive_nonattempts": streak, "refusals": refusals, "pending": pending}')


change_function('history', history)


def launch(text):
    text = once(text, 'decision = next_attempt(name, hist["records"], hist["actual"], hist["residuals"], hist["trailing_nonattempt"])',
                'decision = decision_for(ctx, call, hist)')
    return once(text, '    invocation = {"schema":', '''    # A249: bind one final argv after dry checks and sampler startup.
    plan, plan_pin = write_launch_commit(ctx, plan, plan_pin, work, ctx.system.utc())
    invocation = {"schema":''')


change_function('launch', launch)


def sampler(text):
    text = once(text, '    mp = Path(work) / "monitor_pid.json"', '''    bootstrap = plan
    bootstrap_pin, _ = read_record(str(Path(work) / 'plan.json'))
    committed = False
    mp = Path(work) / "monitor_pid.json"''')
    text = once(text, '        if monitor_identity is None and mp.exists():', '''        if not committed:
            final = observe_launch_commit(ctx, bootstrap, bootstrap_pin, work)
            if final is not None:
                plan, final_pin = final
                committed = True
        if monitor_identity is None and mp.exists():''')
    return once(text, 'and monitor_identity["monitor_pid"] > 1, "MONITOR_PID_FORM")',
                'and monitor_identity["monitor_pid"] > 1, "MONITOR_PID_FORM")\n'
                '            need(committed and monitor_identity.get("plan") == final_pin, "SAMPLER_FINAL_PLAN_BINDING")')


change_function('sampler', sampler)


def resume(text):
    return once(text, '            invocation = read_record(inv)[1]', '''            plan, pin = read_launch_commit(ctx, plan, pin, p.parent)
            invocation = read_record(inv)[1]''')


change_function('launch_resume', resume)


def make_plan(text):
    text = once(text, '"caps_basis": {"rule": "A223 G25; first-attempt caps or identical retry / rule-(c)"}',
                '''"caps_basis": {'rule': 'A249: Phase 1 reporting only; monitor wall uses remaining Phase 2',
                'decision_utc': decision['decision_utc'],
                'phase1_ceiling_utc': ctx.cfg['phase1_ceiling_utc'],
                'phase2_ceiling_utc': ctx.cfg['phase2_ceiling_utc'], 'phase1_requests_stop': False}''')
    return once(text, '"invocation_utc": utc()', '"invocation_utc": decision["decision_utc"]')


change_function('make_plan', make_plan)


def terminal_set(text):
    return once(text, 'term = terminal_prefix(h["actual"], call["name"])', '''eligible = [r for r in h['actual'] if timestamp(r['time_utc'], whole=True) <= timestamp(ctx.cfg['phase1_ceiling_utc'])]
        term = terminal_prefix(eligible, call['name'], authenticated_causes(ctx, eligible))''')


change_function('terminal_set', terminal_set)


def residual(text):
    a = text.index('                decision = next_attempt(')
    b = text.index('\n            caps, solo', a)
    text = text[:a] + '''                # Historical caps come from the saved invocation, never today's clock.
                decision = saved_residual_plan(ctx, name, k, outdir)''' + text[b:]
    return once(text, '            caps, solo = first_caps(name), False', '''            if origin == 'P112':
                saved = saved_residual_plan(ctx, name, k, outdir)
                caps, solo = saved['caps'], saved['solo_mode']
            else:
                caps, solo = first_caps(name), False''')


change_function('honor_residual', residual)
extra.append('''
def saved_residual_plan(ctx, name, k, outdir):
    found = []
    root = Path(ctx.cfg['p112_launch_root']) / 'work'
    for path in sorted(root.glob(name + '_A%d_*/plan.json' % k)):
        inv = path.parent / 'invocation.json'
        if not inv.is_file():
            continue
        pin, plan = read_record(path)
        plan, pin = read_launch_commit(ctx, plan, pin, path.parent)
        _, invocation = read_record(inv)
        need(invocation.get('plan') == pin and invocation.get('planned_monitor_argv') == plan['monitor_argv'],
             'RESIDUAL_PLAN_BINDING')
        if plan.get('name') == name and plan.get('attempt') == k and plan.get('outdir') == outdir:
            found.append(plan)
    need(len(found) == 1, 'RESIDUAL_PLAN_NOT_UNIQUE')
    return found[0]
''')

edits = []
for n in tree.body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in replacement:
        lo = min([n.lineno] + [x.lineno for x in n.decorator_list]) - 1
        edits.append((lo, n.end_lineno, replacement.pop(n.name) + '\n'))
for a, b, text in sorted(edits, reverse=True):
    lines[a:b] = [text]
s = ''.join(lines)
s = once(s, 'TOOL_NAME = "P112_LAUNCHER_CX2V003"', 'TOOL_NAME = "P112_LAUNCHER_CX2V004"')
s = once(s, '"members", "f_points")',
         '"members", "f_points", "phase1_ceiling_utc", "phase2_ceiling_utc", "cause_records", "root_stop_records")')
s = once(s, 'need(c["schema"] == "P112_CONFIG_CX2V001", "CONFIG_SCHEMA")',
         'need(c["schema"] == "P112_CONFIG_CX2V004", "CONFIG_SCHEMA")\n        validate_policy_config(c)')
s = once(s, '    def monotonic(self):\n        return time.monotonic()',
         '    def utc(self):\n        return utc()\n\n    def monotonic(self):\n        return time.monotonic()')
s = once(s, 'description="P-112: root-invoked Phase-1 launch custody, A223 / 0782."',
         'description="P-112: root-invoked Phase-1 custody, A248/A249; no Phase-1 boundary stop."')
end = s.index('if __name__ == "__main__":')
s = s[:end] + '\n\n' + '\n\n'.join(extra + list(replacement.values())) + '\n\n' + s[end:]
compile(s, 'assembled-cx2v004', 'exec')
out = HERE / 'phase1_ngc_launch_cx2v004_draft002.py'
with out.open('x') as f:
    f.write(s)
print(out.name, hashlib.sha256(s.encode()).hexdigest())
for name, h in manifest:
    print(name, h)
