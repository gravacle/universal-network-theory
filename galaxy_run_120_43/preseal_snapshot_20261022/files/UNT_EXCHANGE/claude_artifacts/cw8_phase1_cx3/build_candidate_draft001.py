"""Exclusive, reproducible source composition. Does not execute generated tools."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ART = HERE.parent
PARENT = ART / "phase1_ngc_launch_kit_cx2v004/phase1_ngc_launch_cx2v004.py"
PARENT_SHA = "8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9"
PINS = {}


def read(path, expected=None):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if expected is not None:
        assert digest == expected, (path, digest)
    PINS[str(path)] = digest
    return raw.decode()


source = read(PARENT, PARENT_SHA)
extension = read(HERE / "cw8_extension_draft001.py")
source_pins = ast.literal_eval(next(
    n.value for n in ast.parse(source).body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == "SOURCE_PINS" for t in n.targets)))
fixed = {"driver": source_pins["galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py"]}
paths = {
    "comparator": ("step5_path_c2/tools/compare_identity_pair_c2v001.py",
                   "8e857fff5c2bc16574238cd4fb5c2c510815efe60764f6027d9addd944be0178"),
    "checkpoint_module": ("resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py",
                          "069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114"),
    "serial_worker": (
        "ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/"
        "ngc43_coupled_root_worker_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py",
        "ee27227c2cee3093589ae6b6546a0d88a1bbe20c47ba4dacff497ad7cc80189f"),
    "parallel_worker": (
        "ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/"
        "ngc43_coupled_root_worker_parallel_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py",
        "293a417f493fee2b59176bc60873fa3cdea5e586f375efbe51cbd10651e045b1"),
    "serial_solver": (
        "tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py",
        "8ef3079b0a23c32c688605e96eb5b79beb79768578cc7aef22ea087c7ae12469"),
    "parallel_solver": (
        "tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_uvtail_c2v001.py",
        "7667025bd9382a58688153fde98bf90f2b67d27baa39a939982631c305c229db"),
}
for key, (relative, digest) in paths.items():
    path = ART / relative
    read(path, digest)
    fixed[key] = {"path": str(path), "sha256": digest}
read(Path(fixed["driver"]["path"]), fixed["driver"]["sha256"])
CHANGES = []


def change(old, new, count=1):
    global source
    assert source.count(old) == count, (old[:150], source.count(old), count)
    source = source.replace(old, new)
    CHANGES.append({"old": old, "new": new, "occurrences": count})


def function_change(name, old, new, count=1, cls=None):
    global source
    tree = ast.parse(source)
    nodes = tree.body
    if cls:
        nodes = next(n for n in nodes if isinstance(n, ast.ClassDef) and n.name == cls).body
    matches = [n for n in nodes if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(matches) == 1, (name, len(matches))
    node = matches[0]
    lines = source.splitlines(keepends=True)
    segment = "".join(lines[node.lineno-1:node.end_lineno])
    assert segment.count(old) == count, (name, old, segment.count(old))
    replacement = segment.replace(old, new)
    source = "".join(lines[:node.lineno-1]) + replacement + "".join(lines[node.end_lineno:])
    CHANGES.append({"function": (cls + "." if cls else "") + name,
                    "old": old, "new": new, "occurrences": count})


change('TOOL_NAME = "P112_LAUNCHER_CX2V004"', 'TOOL_NAME = "P112_LAUNCHER_CX3CW8V001"')
change('need(c["schema"] == "P112_CONFIG_CX2V004", "CONFIG_SCHEMA")',
       'need(c["schema"] in ("P112_CONFIG_CX2V004", "P112_CONFIG_CX3CW8V001"), "CONFIG_SCHEMA")')
function_change("first_caps", 'def first_caps(name):\n    return dict(CAPS["twin" if name == TWIN else "serial"])',
                'def first_caps(name, column_workers=1):\n'
                '    caps = dict(CAPS["twin" if name == TWIN else "serial"])\n'
                '    caps["rss_cap_bytes"] = cw8_rss(name, column_workers)\n'
                '    return caps')
function_change("terminal_prefix", 'RAM * (11 if name == TWIN else 1)',
                "cw8_rss(name, current.get('_verified_column_workers', 1))")
function_change("next_attempt", 'has_monitor_refusal=False):',
                'has_monitor_refusal=False, column_workers=1):')
function_change("next_attempt", 'caps = first_caps(name)', 'caps = first_caps(name, column_workers)')
function_change("next_attempt", 'RAM * (11 if name == TWIN else 1)', 'cw8_rss(name, column_workers)')
function_change("decision_for", "has_monitor_refusal=bool(hist.get('refusals')))",
                "has_monitor_refusal=bool(hist.get('refusals')), column_workers=cw8_workers(call))")
function_change("finish_call", 'return {"name": name,', 'return cw8_apply_choice(self, {"name": name,', cls="Context")
function_change("finish_call", '"entry": entry, "entry_pin": ep, "origin": "KIT" if hits else "P112"}',
                '"entry": entry, "entry_pin": ep, "origin": "KIT" if hits else "P112"})', cls="Context")
function_change("registered_entry", "    return entry, pin",
                '    cw8_check_role(call, entry.get("worker_role"))\n    return entry, pin')
function_change("check_monitor_command", "caps, name):", "caps, name, column_workers=1):")
function_change("check_monitor_command", 'RAM * (11 if name == TWIN else 1)', 'cw8_rss(name, column_workers)')
function_change("launch_checks", 'RAM * (11 if plan["name"] == TWIN else 1)',
                'cw8_rss(plan["name"], cw8_plan_workers(plan))')
function_change("run_dry", '    for key in ("driver", "dry_harness"):',
                '    need(dig(read_pin(call["spec"]), LEAF) == cw8_workers(call), "CW8_DRY_EXPECTED_LEAF")\n'
                '    for key in ("driver", "dry_harness"):')
function_change("run_dry", 'verdict.update({"log": lp,',
                'verdict.update({"worker_role": cw8_role(call), "expected_leaf": cw8_workers(call), "log": lp,')
function_change("make_plan", '"spec": call["spec"], "pins":',
                '"worker_role": cw8_role(call), "spec": call["spec"], "pins":')
function_change("register_call", '        return old_pin',
                '        cw8_check_role(call, old.get("worker_role"))\n        return old_pin')
function_change("register_call", 'record.update({"schema":',
                'record.update({"worker_role": cw8_role(call), "schema":')
function_change("kit_kill_target", '"8" if plan["name"] == TWIN else "1"',
                'str(cw8_plan_workers(plan))')
function_change("write_launch_record", '    raw, lj = snapshot',
                '    call = ctx.call(name)\n'
                '    cw8_check_role(call, plan.get("worker_role"))\n'
                '    need(name == TWIN or watch_pid is None, "CW8_FULL_CALL_TWIN_WATCHER")\n'
                '    raw, lj = snapshot')
function_change("write_launch_record", 'record.update({"schema":',
                'record.update({"worker_role": cw8_role(call), "schema":')
function_change("finish_launch", '    mount_first(ctx.cfg, "P112", ctx.system)',
                '    cw8_check_role(ctx.call(plan["name"]), plan.get("worker_role"))\n'
                '    mount_first(ctx.cfg, "P112", ctx.system)')
function_change("launch_resume", '    need(plan["spec"] == call["spec"], "RESUME_SPEC_BINDING")',
                '    need(plan["spec"] == call["spec"], "RESUME_SPEC_BINDING")\n'
                '    cw8_check_role(call, plan.get("worker_role"))')
function_change("launch", '    call = ctx.call(name)',
                '    call = cw8_ensure_default(ctx, ctx.call(name))')
function_change("launch", 'ctx.pins, call["spec"], outdir, decision["caps"], name)',
                'ctx.pins, call["spec"], outdir, decision["caps"], name, cw8_workers(call))')
function_change("history", '        validate_record_location(ctx, rec)',
                '        validate_record_location(ctx, rec)\n'
                '        cw8_check_attempt(ctx, call, rec)')
function_change("close_attempt", '    entry, entry_pin = registered_entry(ctx, call)',
                '    entry, entry_pin = registered_entry(ctx, call)\n'
                '    cw8_check_attempt(ctx, call, record)')
function_change("close_attempt", 'ctx.get_vpin("SPEC_PIN", name)["sha256"]',
                'call.get("v006_spec_pin", call["spec"])["sha256"]')
function_change("close_attempt", '"schema": "STEP5_ATTEMPT_RECEIPT_C2V001", "raw_status": raw,',
                '"schema": "STEP5_ATTEMPT_RECEIPT_C2V001", "worker_role": cw8_role(call), "raw_status": raw,')
function_change("verify_closed_receipt", "    name, k, outdir = record['name'], record['attempt'], record['outdir']",
                "    name, k, outdir = record['name'], record['attempt'], record['outdir']\n"
                "    verified_workers = cw8_check_attempt(ctx, call, record, obj)")
function_change("verify_closed_receipt", 'return dict(obj, receipt_pin=closed_pin, _verified_monitor=monitor,',
                'return dict(obj, receipt_pin=closed_pin, _verified_monitor=monitor,\n'
                '                _verified_column_workers=verified_workers,')
function_change("registry_bytes", '        sources.extend([pin] +',
                '        if is_pin(call.get("worker_choice")) and call["worker_choice"] not in sources:\n'
                '            sources.append(call["worker_choice"])\n'
                '        sources.extend([pin] +')
function_change("cli", '"record-monitor-refused", "status", "_sampler"))',
                '"record-monitor-refused", "status", "_sampler", "select-workers"))')
function_change("cli", '    ap.add_argument("--name")',
                '    ap.add_argument("--name")\n'
                '    ap.add_argument("--forecast")\n'
                '    ap.add_argument("--forecast-sha256")')
function_change("cli", '        if args.command == "launch":',
                '        need(args.command == "select-workers" or '
                '(args.forecast is None and args.forecast_sha256 is None), "CW8_FORECAST_COMMAND")\n'
                '        if args.command == "select-workers":\n'
                '            need(args.name is None and args.attempt is None and '
                'not args.dry and not args.resume, "CW8_SELECT_ARGUMENTS")\n'
                '            need((args.forecast is None) == (args.forecast_sha256 is None), "CW8_FORECAST_ARGUMENTS")\n'
                '            forecast = ({"path": args.forecast, "sha256": args.forecast_sha256}\n'
                '                        if args.forecast is not None else None)\n'
                '            result = select_workers(ctx, forecast)\n'
                '        elif args.command == "launch":')
change('if __name__ == "__main__":\n    sys.exit(cli())',
       '# Conditional full-call cw8 execution policy, composed without runtime imports.\n'
       'CW8_SOURCE_PINS = ' + repr(fixed) + '\n\n' + extension +
       '\n\nif __name__ == "__main__":\n    sys.exit(cli())')
ast.parse(source)
destination = HERE / "phase1_ngc_launch_cx3cw8_draft001.py"
with destination.open("x") as f:
    f.write(source)
record = {"date_u": subprocess.check_output(["/bin/date", "-u"], text=True).strip(),
          "inputs": PINS, "output": {"path": str(destination),
          "sha256": hashlib.sha256(destination.read_bytes()).hexdigest()}, "changes": CHANGES}
with (HERE / "BUILD_CX3CW8_DRAFT001.json").open("x") as f:
    json.dump(record, f, indent=2, sort_keys=True)
    f.write("\n")
print(json.dumps(record["output"], sort_keys=True))
