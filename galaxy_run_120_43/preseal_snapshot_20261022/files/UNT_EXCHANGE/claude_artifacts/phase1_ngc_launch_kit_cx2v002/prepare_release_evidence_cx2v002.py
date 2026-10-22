"""Exclusive release evidence assembly; reads only named artifacts and authorities."""
import ast
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXCHANGE = ROOT.parent.parent
OLD = ROOT.parent / "phase1_ngc_launch_kit_cx2"
NOW = subprocess.check_output(["/bin/date", "-u"], env=dict(os.environ, LC_ALL="C"), text=True).strip()


def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def save(name, obj):
    raw = obj.encode() if isinstance(obj, str) else (json.dumps(obj, sort_keys=True, indent=1) + "\n").encode()
    path = ROOT / name
    with path.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
        os.fchmod(f.fileno(), 0o444)
    return pin(path)


tool = pin(ROOT / "phase1_ngc_launch_cx2v002.py")
tests = pin(ROOT / "test_phase1_ngc_launch_cx2v002.py")
run_paths = [ROOT / "test_records_cx2v002" / run / "TEST_RECORD.json" for run in ("RUN1", "RUN2")]
raws = [p.read_bytes() for p in run_paths]
assert raws[0] == raws[1]
record = json.loads(raws[0])
assert record["tool_sha256"] == tool["sha256"] and record["test_sha256"] == tests["sha256"]
assert not record["refusal_not_exercised"]
assert all(row["status"] == "PASS" for row in record["cases"])
case_names = {row["name"] for row in record["cases"]}
codes = set()
for node in ast.walk(ast.parse((ROOT / "phase1_ngc_launch_cx2v002.py").read_bytes())):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        index = 1 if node.func.id == "need" else 0 if node.func.id == "Refusal" else None
        if index is not None and len(node.args) > index:
            codes.update(x.value for x in ast.walk(node.args[index])
                         if isinstance(x, ast.Constant) and isinstance(x.value, str))
assert not codes - set(record["refusal_coverage"])
mutants = [row for row in record["cases"] if "MUTANT_" in row["name"]]
assert (len(record["cases"]), len(codes), len(mutants)) == (639, 236, 56)
run_pins = [pin(p) for p in run_paths]
execution_pins = [pin(p.with_name("EXECUTION_METADATA.json")) for p in run_paths]
stamp_pin = pin(ROOT / "test_records_cx2v002/TEST_RUN_STAMP_CX2V002.json")
components_pin = pin(ROOT / "RELEASE_COMPONENTS_CX2V002.json")
source_audit_pin = pin(ROOT / "SOURCE_BYTE_AUDIT_CX2V002.json")
authorities = [
    EXCHANGE / "FROM_CODEX/0784_2026-10-20_codex2_P112_cx2v002_required_fixes.md",
    EXCHANGE / "FROM_CODEX/0785_2026-10-20_codex2_P112_single_read_scope_confirmed.md",
    EXCHANGE / "FROM_CODEX/0786_2026-10-20_codex2_P112_cx2v002_interface_answers.md",
    ROOT.parent / "runbook_rulings_c2/P112_LAUNCHER_BRIEF_V005.md",
    ROOT.parent / "phase1_ngc_launch_kit_cx2_rootverify_c2/ROOT_VERIFY_FINDINGS_C2V001.md",
    ROOT.parent / "phase1_ngc_launch_kit_cx2_rootverify_c2/rv_adversarial_c2v001.py",
    ROOT.parent / "phase1_ngc_launch_kit_cx2_rootverify_c2/rv_static_a226_c2v001.py",
    ROOT.parent / "phase1_ngc_launch_kit_cx2_rootverify_c2/rv_suite_audit_c2v002.py",
]
authority_pins = [pin(p) for p in authorities]
repro = save("REPRODUCIBILITY_PROOF_CX2V002.json", {
    "schema": "P112_REPRODUCIBILITY_PROOF_CX2V002", "date_u": NOW, "status": "TESTED_PASS",
    "tool": tool, "test_program": tests, "test_records": run_pins, "execution_metadata": execution_pins,
    "run_stamp": stamp_pin, "byte_identical": True, "passed_per_run": len(record["cases"]),
    "statically_named_refusals": len(codes), "named_refusals_missing": [],
    "extra_injected_refusal_codes": sorted(set(record["refusal_coverage"]) - codes),
    "mutants_killed_per_run": len(mutants), "components": components_pin,
    "scope": "Two independent final executions; synthetic saved states and suite-owned inert processes only.",
})
mapping = {
    "B1": ["B1_RV01_checked_launch_buffer", "CX2V002_MUTANT_B1_launch_reread"],
    "B2": ["B2_RV02_classified_receipt_buffer", "CX2V002_MUTANT_B2_receipt_reread"],
    "B3": ["B3_RV03_verified_registry_buffer", "CX2V002_MUTANT_B3_registry_reread"],
    "B4": ["B4_RV11_real_apostrophe_ps", "B4_RV12_transient_apostrophe", "B4_RV13_persistent_apostrophe",
           "B4_RV14_first_apostrophe", "CX2V002_MUTANT_B4_command_parse_refusal",
           "B4_non_UTF8_ps_command_does_not_fail_sample", "CX2V002_MUTANT_strict_ps_decoding"],
    "F1": ["F1_RV05_RV06_record_alias_blinding", "F1_resume_alias_plan.json",
           "F1_resume_alias_invocation.json", "F1_resume_alias_monitor_pid.json",
           "F1_sampler_alias_monitor_pid.json", "F1_sampler_alias_invocation.json",
           "F1_sampler_alias_receipt", "F1_first_sample_alias_refuses_before_monitor",
           "CX2V002_MUTANT_F1_unguarded_launch_observation", "CX2V002_MUTANT_F1_allow_record_alias"],
    "F2": ["F2_RV08_actual_line_grammar", "CX2V002_MUTANT_F2_tool_splitlines",
           "CX2V002_MUTANT_F2_residual_splitlines"],
    "F3": ["F3_missing_monitor_pid_recovery", "F3_RV21_actual_inert_Popen_interruption_resume_close",
           "F3_null_pid_status_live_by_command", "F3_null_pid_close_live_by_command",
           "F3_null_pid_solo_live_by_command", "CX2V002_MUTANT_F3_require_monitor_pid_file"],
    "F4": ["F4_RV19_kit_exit_one_semantics", "CX2V002_MUTANT_F4_any_exit_one_ended"],
    "F5": ["F5_RV24_production_V006_constant", "CX2V002_MUTANT_F5_configured_V006"],
    "F6": ["F6_postseal_component_guard", "CX2V002_MUTANT_F6_postseal_guard_removed"],
    "cleanup": ["CLEANUP_RV04_single_guarded_read", "CLEANUP_fill_single_read_MUST_PASS",
                "CX2V002_MUTANT_cleanup_pin_then_reread", "CX2V002_MUTANT_cleanup_certificate_reread"],
    "0785": ["0785_immutable_audit_MUST_PASS", "0785_volatile_audit_MUST_PASS",
             "0785_cutoff_audit_MUST_PASS", "ALL_PUBLIC_COMMANDS_IMMUTABLE_READ_ONCE_MUST_PASS",
             "ALL_PUBLIC_COMMANDS_AUDIT_COVERAGE_MUST_PASS", "CX2V002_MUTANT_0785_immutable_cache_bypassed",
             "CX2V002_MUTANT_0785_volatile_pin_reread", "CX2V002_MUTANT_0785_cutoff_copy_reread"],
    "0786": ["0786_root_and_P112_siblings_accepted", "0786_missing_sibling_refused",
             "0786_changed_sibling_refused", "0786_rule_binding_required", "0786_sibling_form_required",
             "0786_sibling_written_before_exact_key_record", "CX2V002_MUTANT_0786_ignore_sibling_sha",
             "CX2V002_MUTANT_0786_ignore_missing_sibling", "CX2V002_MUTANT_0786_parent_written_first"],
}
assert all(name in case_names for names in mapping.values() for name in names)
coverage = save("FIX_COVERAGE_PROOF_CX2V002.json", {
    "schema": "P112_FIX_COVERAGE_PROOF_CX2V002", "date_u": NOW, "status": "TESTED_PASS",
    "authorities": authority_pins, "test_record": run_pins[0], "tool": tool, "test_program": tests,
    "mapping": mapping, "audit": record["interfaces"]["all_public_command_read_audit"],
    "child_reopen_disclosure": (
        "Pinned executables are hashed in the parent, then executed by path in child processes. "
        "The root integrity envelope covers those child reads (A226 item 2)."),
    "additional_tested_fix": (
        "A real preflight ps observation contained non-UTF-8 bytes. System.processes now decodes "
        "losslessly with surrogateescape; a controlled invalid-byte subprocess and restoring mutant verify this."),
})
prior_interface_path = OLD / "INTERFACE_PROOF_CX2V001.json"
prior_interface = json.loads(prior_interface_path.read_bytes())
interface = save("INTERFACE_PROOF_CX2V002.json", {
    "schema": "P112_INTERFACE_PROOF_CX2V002", "date_u": NOW, "status": "TESTED",
    "tool": tool, "test_program": tests, "test_record": run_pins[0],
    "source_pins": prior_interface["source_pins"],
    "source_inventory": source_audit_pin, "prior_interface_inventory": pin(prior_interface_path),
    "receipt_roles": prior_interface["receipt_roles"],
    "status_map_sha256": prior_interface["status_map_sha256"],
    "declared_list_sha256": prior_interface["declared_list_sha256"],
    "interfaces": record["interfaces"],
    "limits": [
        "UNTESTED full real PLAN/registry assembly, v003g execution, slots access, production scientific operation.",
        "TESTED c2v006 helpers retain the documented registry shape/theta limitation and sibling-receipt residence refusal.",
        "UNTESTED G26 successor acceptance: part 5 remains a separately dispatched root review.",
        "TESTED in-process audited operations; child executable reopening is covered by root's integrity envelope.",
    ],
})
readme = f"""# P-112 Phase-1 launch custody, CX2V002 — for coordinator review

date -u: {NOW}

**TESTED.** Both final runs passed 639/639 checks, exercised all 236 statically named refusals, and killed 56/56 restoring mutants. The test records are byte-identical: `{run_pins[0]["sha256"]}`. This successor is submitted for Claude2/root verification and Claude4 review; it is not adopted. No scientific process was launched by this build. Tests use saved synthetic states and inert fixture processes.

**Delivered bytes.**

| File | Byte SHA256 |
|---|---|
| `{Path(tool["path"]).name}` ({tool["bytes"]} bytes) | `{tool["sha256"]}` |
| `{Path(tests["path"]).name}` ({tests["bytes"]} bytes) | `{tests["sha256"]}` |
| `REPRODUCIBILITY_PROOF_CX2V002.json` | `{repro["sha256"]}` |
| `FIX_COVERAGE_PROOF_CX2V002.json` | `{coverage["sha256"]}` |
| `INTERFACE_PROOF_CX2V002.json` | `{interface["sha256"]}` |
| `SOURCE_BYTE_AUDIT_CX2V002.json` | `{source_audit_pin["sha256"]}` |
| `RELEASE_COMPONENTS_CX2V002.json` | `{components_pin["sha256"]}` |
| `test_records_cx2v002/TEST_RUN_STAMP_CX2V002.json` | `{stamp_pin["sha256"]}` |
| `test_records_cx2v002/RUN1/TEST_RECORD.json` | `{run_pins[0]["sha256"]}` |
| `test_records_cx2v002/RUN2/TEST_RECORD.json` | `{run_pins[1]["sha256"]}` |

The reproducibility proof pins each execution's actual start/finish metadata. The common test-record date is the actual shared suite-start stamp. The source audit rechecks all 43 brief references / 42 unique pinned paths. The component inventory identifies the exclusive source and test successors used to assemble these files.

**FORMAL — authority.** Dispatches 0784, 0785, and 0786 govern this successor, alongside the V005 brief and its previously binding ROUND5/0782 rulings. The coverage proof pins the exact dispatches and root verifier sources and maps every new requirement to passing regressions and restoring mutants. Root is the only scientific launch owner. Part 5 still requires the separate G26 dispatch.

**TESTED — checked bytes.** Immutable pinned inputs use one guarded byte snapshot per command, shared across validation and pin production. Aliases of the same allowed immutable input share that snapshot; monitor/work records additionally require realpath equal to the supplied path. A launch record pins and quotes the same launch JSON buffer used for its checks. Receipt classification and registry verification also pin their checked buffers. EPS/GQ objects pass from fill validation to call construction without another file read.

**TESTED — changing observations.** An absent or unparseable launch JSON may be polled; a post-bound observation after stopping the monitor is separate. Each successful observation reads once, and its checks, quotes, and hash use those bytes. Failed opens before creation are not byte observations. The sampler retains its first parsed launch snapshot. V006 gate and cutoff reads are separate observations; the cutoff copy is written from the exact buffer whose hash names it. Observation reports contain counts and the last observed pin/byte count for each kind. Other evidence records carry `observations` directly.

**TESTED — refusal observation custody (0786).** A MONITOR_REFUSED record keeps the exact V005 key set. The writer first creates `<record>.observations.json` exclusively, then includes `observations_sha256=<64 hex>` in the record's existing rule text. The sibling contains `counts`, `last_observation`, and the writer's date_u. For each present kind, the positive integer count has a matching last observation with kind, pin, and byte count; absent kinds have no entry. Status and registry verification check sibling presence and its byte hash for both P112 and root-written kit refusals. No observation pin is followed to another file.

**TESTED — recovery and process handling.** Resume no longer depends on monitor_pid.json surviving the Popen interruption. It uses a single matching monitor command, or records no live match, and discloses the PID source. Tests include an actual inert invocation exiting between monitor Popen and PID-record creation, followed by resume and close. Null-PID liveness checks use the command line. A malformed shell quote in a ps command falls back to whitespace splitting; an individual unusable command does not invalidate the whole sample. Non-UTF-8 ps bytes decode losslessly. Completeness depends on ps acquisition/parsing, not shell tokenization. Kit exit 1 means ALREADY_ENDED only when its stderr JSON explicitly says alive:false.

**TESTED — gate and blinding.** The whole-line TOOL_PIN name is `P112_LAUNCHER_CX2V002`; exactly one matching sha/realpath line is required. Other version names do not conflict. TOOL_PIN and RESIDUAL_RETRY split on actual newline and strip trailing carriage returns. Production config must name the fixed program V006 constant. V007_POSTSEAL_RECORDS is a forbidden component. Every changed monitor/work metadata read site has a symlink regression, including the first sampler record before monitor start.

**FORMAL — retained V005 interfaces, authorized by 0786.**

| Category | Retained identifiers |
|---|---|
| Config and synthetic manifest | P112_CONFIG_CX2V001; P112_SYNTHETIC_PINS_CX2V001 |
| Internal evidence | P112_DRY_VERDICT_CX2V001; P112_THETA_CHECK_CX2V001; P112_SAMPLER_FIRST_CX2V001; P112_INVOCATION_CX2V001; P112_MONITOR_PID_CX2V001; P112_STATUS_CX2V001 |
| P112 records | UNT_P112_LAUNCH_PLAN_CX2V001; UNT_P112_LAUNCH_REGISTRY_ENTRY_CX2V001; UNT_P112_LAUNCH_RECORD_CX2V001; UNT_P112_MISLAUNCH_RECORD_CX2V001; STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001 |
| Shared schemas | STEP5_SOLO_SAMPLE_CX2V001; STEP5_ATTEMPT_RECEIPT_C2V001; STEP4_CUTOFF_RECORD_C2V001; STEP5_LAUNCH_REGISTRY_C2V003; MONITOR_REFUSED_ATTEMPT_RECORD_C2V001; S0_OUTSIDE_SET_STOP_RECORD_C2V001 |
| Refusal launcher field | P112_CX2V001; writer name is now P112_LAUNCHER_CX2V002 |
| Run and attempt names | NGC_P1_&lt;NAME&gt;_RUN_CX2V001_A&lt;k&gt;; P112_&lt;NAME&gt;_&lt;LAUNCH/MISLAUNCH/MONITOR_REFUSED&gt;_CX2V001_A&lt;k&gt;.json |
| Registry / outside stop / assembly | P112_&lt;NAME&gt;_CX2V001.json; &lt;NAME&gt;_A&lt;k&gt;_CX2V001.json; STEP5_LAUNCH_REGISTRY_PHASE1_CX2V001.json; STEP5_REGISTRY_ASSEMBLY_RECORD_CX2V001.json |

Existing kit C2V003A naming, Step-4 cutoff naming, and spec/fill filenames retain their brief forms. These are format identifiers; the executable and its required TOOL_PIN are CX2V002. A CX2V001 adoption line is neither needed nor accepted as this executable's gate.

**FORMAL — invocation.** Every command takes `--config <absolute path> --config-sha256 <hex>`. Commands are `launch --name NAME [--attempt k]`, `launch --name NAME --dry`, `launch --name NAME --attempt k --resume`, `close-attempt --name NAME --attempt k`, `assemble-registry [--verify]`, `record-monitor-refused --plan PATH --plan-sha256 SHA --work DIR`, `stop-outside-set --name S0_NAME [--attempt k]`, and advisory `status`. The internal sampler uses the same gate. Dry launch and status remain TOOL_PIN-exempt as specified. There is no automatic retry. Config keys and filled-spec responsibilities remain those of V005; root supplies already-filled, pinned inputs.

**TESTED — audit scope.** One audit covers all ten public operation entrypoints exercised in-process, checking spelled and resolved paths and one immutable-file read per outer command. There were no violations in either final run. Directory handles opened solely to fsync output parents are not reads of pinned file bytes. Volatile observations and process-counter identity probes are classified separately; the executable's own-sha read is excepted. The audit does not observe another process's opens.

**FORMAL — A226 item 2 disclosure.** Pinned executables are hashed in the parent, then executed by path in child processes. The root integrity envelope covers these later child reads. This build does not prove that a child's executable bytes equal the earlier parent buffer.

**TESTED / UNTESTED limits.** The process count is sampled and limited to the declared tools and supported command forms; arbitrary relative copies, suffixless copies, and unquoted paths containing spaces are not comprehensively identified. Root's whole-interval HOLD remains necessary. The sample validator retains its n_samples >= 2 form check in addition to the specified timing/completeness cases. Synthetic tests verify c2v006 helper behavior, including its shape-valid theta limitation and its refusal of the true sibling receipt residence. Full real PLAN/registry assembly, v003g execution, slots access, G26 successor acceptance, production host sampling, actual volume loss/restart, real scientific status behavior, and real twin kill-watch operation remain UNTESTED. Their deciding checks occur under the root's separately authorized real operations and G26 review.

**FORMAL — reproduction.** Use the pinned Python with `-I -B`, `nice -n 10`, and OPENBLAS_NUM_THREADS, OMP_NUM_THREADS, MKL_NUM_THREADS, VECLIB_MAXIMUM_THREADS, NUMEXPR_NUM_THREADS, and BLIS_NUM_THREADS all set to 1. The standalone suite takes `--tool`, `--tool-sha256`, `--out` (new absolute directory), `--run-stamp`, and `--run-stamp-sha256`. Process-list access and permission to stop only suite-owned inert processes are needed. Existing artifacts and test directories are immutable; use new output names.
"""
readme_pin = save("README_PHASE1_NGC_LAUNCH_CX2V002.md", readme)
components = json.loads((ROOT / "RELEASE_COMPONENTS_CX2V002.json").read_bytes())
source_audit = json.loads((ROOT / "SOURCE_BYTE_AUDIT_CX2V002.json").read_bytes())
paths = {
    Path(__file__).resolve(), Path(tool["path"]), Path(tests["path"]),
    Path(repro["path"]), Path(coverage["path"]), Path(interface["path"]), Path(readme_pin["path"]),
    Path(components_pin["path"]), Path(source_audit_pin["path"]), Path(stamp_pin["path"]),
    prior_interface_path, Path(source_audit["prior_inventory"]["path"]),
    *run_paths, *(p.with_name("EXECUTION_METADATA.json") for p in run_paths), *authorities,
    *(Path(row["path"]) for row in components["source_parts"] + components["test_parts"]),
    *(Path(row["path"]) for row in source_audit["rows"]),
}
manifest = "".join(pin(p)["sha256"] + "  " + str(p) + "\n" for p in sorted(paths))
manifest_pin = save("HASHES_CX2V002.txt", manifest)
print(json.dumps({"date_u": NOW, "reproducibility": repro, "coverage": coverage, "interface": interface,
                  "readme": readme_pin, "manifest": manifest_pin, "manifest_entries": len(paths)}))
