"""Exclusive release evidence, after two passing executions of the final bytes."""
import ast
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / "phase1_ngc_launch_kit_cx2v002"
EXCHANGE = ROOT.parent.parent
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


tool = pin(ROOT / "phase1_ngc_launch_cx2v003.py")
tests = pin(ROOT / "test_phase1_ngc_launch_cx2v003.py")
run_paths = [ROOT / "test_records_cx2v003" / run / "TEST_RECORD.json" for run in ("RUN1", "RUN2")]
raws = [p.read_bytes() for p in run_paths]
assert raws[0] == raws[1], "final test records differ"
record = json.loads(raws[0])
assert record["tool_sha256"] == tool["sha256"] and record["test_sha256"] == tests["sha256"]
assert all(row["status"] == "PASS" for row in record["cases"])
assert not record["refusal_not_exercised"]
case_names = {row["name"] for row in record["cases"]}
mutants = [row for row in record["cases"] if "MUTANT_" in row["name"]]
assert (len(record["cases"]), len(mutants)) == (681, 78)
codes = set()
for node in ast.walk(ast.parse(Path(tool["path"]).read_bytes())):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        index = 1 if node.func.id == "need" else 0 if node.func.id == "Refusal" else None
        if index is not None and len(node.args) > index:
            codes.update(x.value for x in ast.walk(node.args[index])
                         if isinstance(x, ast.Constant) and isinstance(x.value, str))
assert not codes - set(record["refusal_coverage"])
run_pins = [pin(p) for p in run_paths]
executions = [pin(p.with_name("EXECUTION_METADATA.json")) for p in run_paths]
stamp = pin(ROOT / "test_records_cx2v003/TEST_RUN_STAMP_CX2V003.json")
components = json.loads((ROOT / "RELEASE_COMPONENTS_CX2V003.json").read_bytes())
for row in components["source_parts"] + components["test_parts"]:
    assert pin(row["path"])["sha256"] == row["sha256"]
component_pin = pin(ROOT / "RELEASE_COMPONENTS_CX2V003.json")
doc_contract = pin(ROOT / "README_CONTRACT_CX2V003.md")
assert doc_contract["sha256"] == record["interfaces"]["cx2v003_readme_contract"]["sha256"]
assert not record["interfaces"]["all_public_command_read_audit"]["violations"]
assert len(record["interfaces"]["cx2v003_restoring_mutants"]) == 20
assert len(record["interfaces"]["cx2v003_documentation_mutants"]) == 2
assert all(r["control"] == "PASS" and r["status"] == "KILLED"
           for r in record["interfaces"]["cx2v003_restoring_mutants"] +
           record["interfaces"]["cx2v003_documentation_mutants"])

prior_coverage_path = OLD / "FIX_COVERAGE_PROOF_CX2V002.json"
prior_coverage = json.loads(prior_coverage_path.read_bytes())
mapping = dict(prior_coverage["mapping"])
mapping.update({
    "0789_V1": ["CX2V003_V1_transient_decoy_MUST_PASS", "CX2V003_V1_persistent_decoy_MUST_PASS",
                "CX2V003_V1_exact_before_pid_MUST_PASS", "CX2V003_V1_monitor_identity_form",
                "CX2V003_MUTANT_V1_restore_broad_sampler_and_raise", "CX2V003_MUTANT_V1_reread_monitor_identity"],
    "0789_Fa": ["CX2V003_Fa_exact_resume_and_null_pid", "CX2V003_MUTANT_Fa_null_pid_broad_match",
                "CX2V003_MUTANT_Fa_resume_broad_match", "CX2V003_MUTANT_Fa_ignore_process_group"],
    "0789_Fb": ["CX2V003_Fb_blank_argv", "CX2V003_MUTANT_Fb_reject_blank_argv"],
    "0789_Fc": ["CX2V003_Fc_regular_bounded_identity", "CX2V003_MUTANT_Fc_restore_unbounded_identity"],
    "0789_Fd": ["CX2V003_Fd_whitespace_tokens", "CX2V003_MUTANT_Fd_restore_shlex"],
    "0789_Fe": ["CX2V003_Fe_child_pid_alive", "CX2V003_Fe_planned_command_alive",
                "CX2V003_Fe_non_UTF8_stderr", "CX2V003_Fe_timeout", "CX2V003_Fe_ended_after_ps_check",
                "CX2V003_MUTANT_Fe_ignore_child_pid", "CX2V003_MUTANT_Fe_ignore_planned_command",
                "CX2V003_MUTANT_Fe_restore_text_stderr", "CX2V003_MUTANT_Fe_remove_timeout"],
    "0789_A15": ["CX2V003_A15_launch_json_shape", "CX2V003_MUTANT_A15_skip_shape_validation"],
    "0789_A06": ["CX2V003_A06_orphan_status_and_retry", "CX2V003_MUTANT_A06_ignore_orphan_status",
                 "CX2V003_MUTANT_A06_retry_orphan_write"],
    "0789_A10": ["CX2V003_A10_record_and_cutoff_hardlinks", "CX2V003_MUTANT_A10_allow_hardlinks"],
    "0789_A09": ["CX2V003_A09_and_V1_documentation", "CX2V003_MUTANT_A09_restore_blanket_realpath_claim"],
    "0789_Lens1_s0": ["CX2V003_Lens1_s0_realpaths", "CX2V003_MUTANT_Lens1_s0_alias"],
    "0789_Lens1_sample": ["CX2V003_Lens1_sample_receipt_pin", "CX2V003_MUTANT_Lens1_ignore_sample_receipt"],
    "0789_Lens1_dead_fields": ["CX2V003_Lens1_remove_dead_fields", "CX2V003_MUTANT_Lens1_restore_dead_revision",
                              "CX2V003_MUTANT_Lens1_restore_dead_observation"],
    "0789_Lens1_disclosure": ["CX2V003_A09_and_V1_documentation", "CX2V003_MUTANT_V1_hide_MULTIPLE_MONITORS_change"],
})
assert all(name in case_names for names in mapping.values() for name in names)
authorities = [
    EXCHANGE / "FROM_CODEX/0781_2026-10-20_codex2_part3_P112_launcher_build_start.md",
    EXCHANGE / "FROM_CODEX/0784_2026-10-20_codex2_P112_cx2v002_required_fixes.md",
    EXCHANGE / "FROM_CODEX/0785_2026-10-20_codex2_P112_single_read_scope_confirmed.md",
    EXCHANGE / "FROM_CODEX/0786_2026-10-20_codex2_P112_cx2v002_interface_answers.md",
    EXCHANGE / "FROM_CODEX/0789_2026-10-20_codex2_P112_cx2v003_fixes.md",
    ROOT.parent / "runbook_rulings_c2/P112_LAUNCHER_BRIEF_V005.md",
    ROOT.parent / "phase1_ngc_launch_kit_cx2v002_rootverify_c2/ROOT_REVERIFY_FINDINGS_C2V002.md",
    ROOT.parent / "phase1_ngc_launch_kit_cx2v002_rootverify_c2/fresh_adversarial/rv_fresh_adversarial_c2v002.py",
]
authority_pins = [pin(p) for p in authorities]
assert authority_pins[4]["sha256"] == "0287a19d6f5ede0293e0fb495f26811e9a9b7079c9fda02aa0352d09fa3dbf9e"
assert authority_pins[6]["sha256"] == "1f280b7967d48b3db88920719ee5026c5509ab8c16b734c534ff11595d3463a3"

# Rehash exactly the previously authorized brief references. No linked data pins
# are followed and no source module is executed.
prior_audit_path = OLD / "SOURCE_BYTE_AUDIT_CX2V002.json"
prior_audit = json.loads(prior_audit_path.read_bytes())
source_rows, cache = [], {}
for row in prior_audit["rows"]:
    path = Path(row["path"])
    lowered = str(path).lower()
    assert not any(x in lowered for x in ("runs_ext/", "/a_side/", "v007_postseal_records", "/.codex/"))
    if str(path) not in cache:
        cache[str(path)] = pin(path)
    current = cache[str(path)]
    assert current["sha256"] == row["sha256"], str(path)
    source_rows.append(dict(current, use=row["use"]))
source_audit = save("SOURCE_BYTE_AUDIT_CX2V003.json", {
    "schema": "P112_SOURCE_BYTE_AUDIT_CX2V003", "date_u": NOW, "status": "TESTED_PASS",
    "prior_inventory": pin(prior_audit_path), "n_rows": len(source_rows), "n_unique_paths": len(cache),
    "rows": source_rows,
})
repro = save("REPRODUCIBILITY_PROOF_CX2V003.json", {
    "schema": "P112_REPRODUCIBILITY_PROOF_CX2V003", "date_u": NOW, "status": "TESTED_PASS",
    "tool": tool, "test_program": tests, "test_records": run_pins, "execution_metadata": executions,
    "run_stamp": stamp, "byte_identical": True, "passed_per_run": len(record["cases"]),
    "statically_named_refusals": len(codes), "named_refusals_missing": [],
    "extra_injected_refusal_codes": sorted(set(record["refusal_coverage"]) - codes),
    "mutants_killed_per_run": len(mutants), "code_mutants": 76, "documentation_mutants": 2,
    "components": component_pin,
    "scope": "Two independent final executions in separate directories, run concurrently; synthetic saved states and owned inert processes only.",
})
coverage = save("FIX_COVERAGE_PROOF_CX2V003.json", {
    "schema": "P112_FIX_COVERAGE_PROOF_CX2V003", "date_u": NOW, "status": "TESTED_PASS",
    "authorities": authority_pins, "retained_coverage": pin(prior_coverage_path),
    "test_record": run_pins[0], "tool": tool, "test_program": tests, "mapping": mapping,
    "audit": record["interfaces"]["all_public_command_read_audit"], "documentation_contract": doc_contract,
    "mutants": record["interfaces"]["cx2v003_restoring_mutants"] + record["interfaces"]["cx2v003_documentation_mutants"],
    "child_reopen_disclosure": "Pinned executables are hashed in the parent then executed by path; the root integrity envelope covers child reads.",
})
prior_interface_path = OLD / "INTERFACE_PROOF_CX2V002.json"
prior_interface = json.loads(prior_interface_path.read_bytes())
interface = save("INTERFACE_PROOF_CX2V003.json", {
    "schema": "P112_INTERFACE_PROOF_CX2V003", "date_u": NOW, "status": "TESTED",
    "tool": tool, "test_program": tests, "test_record": run_pins[0],
    "source_pins": prior_interface["source_pins"], "source_inventory": source_audit,
    "prior_interface_inventory": pin(prior_interface_path), "receipt_roles": prior_interface["receipt_roles"],
    "status_map_sha256": prior_interface["status_map_sha256"],
    "declared_list_sha256": prior_interface["declared_list_sha256"], "interfaces": record["interfaces"],
    "limits": prior_interface["limits"],
})


def function_inventory(raw):
    tree = ast.parse(raw)
    found = {}
    def visit(nodes, prefix=""):
        for node in nodes:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + node.name
                found[name] = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
                visit(node.body, name + ".")
    visit(tree.body)
    return found


old_tool = OLD / "phase1_ngc_launch_cx2v002.py"
before, after = function_inventory(old_tool.read_bytes()), function_inventory(Path(tool["path"]).read_bytes())
delta = save("SOURCE_DELTA_CX2V003.json", {
    "schema": "P112_SOURCE_DELTA_CX2V003", "date_u": NOW, "status": "TESTED_STATIC",
    "baseline": pin(old_tool), "successor": tool,
    "added_definitions": sorted(set(after) - set(before)),
    "removed_definitions": sorted(set(before) - set(after)),
    "changed_definitions": sorted(k for k in set(before) & set(after) if before[k] != after[k]),
    "scope": "AST function/class comparison; lexical-only changes and top-level constants/imports are not included.",
})
delivery_pins = [tool, tests, repro, coverage, interface, delta, source_audit, component_pin, doc_contract, stamp, *run_pins, *executions]
readme = f"""# P-112 Phase-1 launch custody, CX2V003 — submitted for coordinator review

date -u: {NOW}

**TESTED.** Both final runs passed {len(record["cases"])}/{len(record["cases"])} checks and exercised all {len(codes)} statically named refusal codes. All 78 restoring mutants were killed: 76 code mutants and 2 documentation mutants. The two test records are byte-identical, SHA256 `{run_pins[0]["sha256"]}`. The in-process audit reports zero single-read violations across all ten public entrypoints.

**FORMAL.** This is a successor submitted for Claude2/root verification and Claude4 review. It is not adopted. The executable requires TOOL_PIN P112_LAUNCHER_CX2V003. No scientific process was launched. Part 5 still awaits the separate G26 dispatch.

The final executions used separate fixture directories and ran concurrently. Their actual start/end metadata are pinned below. The shared test-record date is the actual suite-start stamp. The source audit rehashed all 43 authorized brief references, 42 unique paths.

| Delivered file | Byte SHA256 |
|---|---|
"""
for row in delivery_pins:
    readme += "| `" + str(Path(row["path"]).relative_to(ROOT)) + "` | `" + row["sha256"] + "` |\n"
readme += "\nThe following immutable documentation contract is included verbatim and checked by the release artifact verification.\n\n"
contract_raw = (ROOT / "README_CONTRACT_CX2V003.md").read_bytes()
readme += contract_raw.decode()
readme_pin = save("README_PHASE1_NGC_LAUNCH_CX2V003.md", readme)
assert contract_raw in Path(readme_pin["path"]).read_bytes()

paths = {
    Path(__file__).resolve(), Path(readme_pin["path"]), prior_audit_path, prior_coverage_path,
    prior_interface_path, old_tool, *authorities,
    *(Path(row["path"]) for row in delivery_pins),
    *(Path(row["path"]) for row in components["source_parts"] + components["test_parts"]),
    *(Path(row["path"]) for row in source_rows),
    Path(components["builder"]["path"]), Path(components["baseline_test_footer"]["path"]),
    Path(components["passing_preflight"]["path"]),
}
manifest = save("HASHES_CX2V003.txt", "".join(pin(p)["sha256"] + "  " + str(p) + "\n" for p in sorted(paths)))
print(json.dumps({"date_u": NOW, "counts": {"tests": len(record["cases"]), "refusals": len(codes), "mutants": len(mutants)},
                  "readme": readme_pin, "manifest": manifest, "entries": len(paths),
                  "reproducibility": repro, "coverage": coverage, "interface": interface, "source_audit": source_audit, "delta": delta}))
