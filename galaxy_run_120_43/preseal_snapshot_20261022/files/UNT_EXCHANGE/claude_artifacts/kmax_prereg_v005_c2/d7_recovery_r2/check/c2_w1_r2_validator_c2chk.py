# Independent checker C2: own W1 implementation from the prereg rule TEXT, expected R2, sealed validator.
import json, hashlib, copy, importlib.util, sys, os
B = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2"
R = "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs"
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def canon(o): return json.dumps(o, sort_keys=True, separators=(',',':'))
PRE = B + "/KMAX_MATRIX_PREREG_V005.json"; CMP = B + "/kmax_compare_c2v005.py"
R1F = B + "/d7_recovery/KMAX_D7_RECOVERY_R1.json"; R2F = B + "/d7_recovery_r2/KMAX_D7_RECOVERY_R2.json"
out = {"pins": {"prereg": sha(PRE), "compare": sha(CMP), "R1": sha(R1F), "R2": sha(R2F)}}
assert out["pins"]["prereg"].startswith("dbddc02c") and out["pins"]["compare"].startswith("49404bc4") and out["pins"]["R1"].startswith("b3938db2")
pre = json.load(open(PRE)); d7 = pre["amendment_v005"]["d7_recovery"]
T = d7["fs_template_bracket"]; assert T == [151250000.0, 302500000.0]
r1 = json.load(open(R1F))["brackets"]; assert canon(r1) == canon(d7["R1"]["brackets"])
r2doc = json.load(open(R2F)); r2 = r2doc["brackets"]
scan = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/C1_RUN_SCAN_V001.json"))
CASES = {"C3R": "KMAX_A2F10_C3R_D7R1_V005_RUN_V001", "S3": "KMAX_A2F10_S3_D7R1_V005_RUN_V001", "Y3": "KMAX_A2F10_Y3_D7R1_V005_RUN_V001"}
r1fs = r1["rule"]["fs_absolute_overrides"]
r1_widened = set(json.load(open(R1F))["widened_entries"])
def w1(entry, rlo, rhi):
    # prereg text: if r(lo)>0 and r(hi)>0 (root below lo): lo -> template_lo if lo > template_lo else lo/2
    #              if r(lo)<0 and r(hi)<0 (root above hi): hi -> 1.05*template_hi if hi < 1.05*template_hi else 2*hi; other end kept
    lo, hi = entry
    if rlo > 0 and rhi > 0:
        return ([T[0], hi], "A") if lo > T[0] else ([lo/2, hi], "B")
    if rlo < 0 and rhi < 0:
        return ([lo, 1.05*T[1]], "A") if hi < 1.05*T[1] else ([lo, 2*hi], "B")
    return None, "NOT_A_W1_CASE"
per_col = {}; findings = []
for case, run in CASES.items():
    lj = json.load(open(R + "/" + run + ".receipt.json.launch.json"))
    spec = json.load(open(lj["pins"]["spec"]["path"]))
    assert sha(lj["pins"]["spec"]["path"]) == lj["pins"]["spec"]["sha256"]
    spec_fs = spec["numerics"]["brackets"]["rule"]["fs_absolute_overrides"]
    if canon(spec["numerics"]["brackets"]) != canon(r1): findings.append("%s launched spec brackets != R1" % case)
    for idx, f in scan[run]["passes"]["fs"]["fail"].items():
        if "MASS_ENTHALPY_NOT_BRACKETED" not in f["failure"]["message"]: findings.append("%s col %s non-W1 failure type" % (case, idx))
        used = spec_fs.get(idx, T)
        its = f["iters"]
        if len(its) != 2 or [its[0]["Hc"], its[1]["Hc"]] != used: findings.append("%s col %s iterations Hc %s != entry used %s" % (case, idx, [i["Hc"] for i in its], used))
        new, step = w1(used, its[0]["r"], its[1]["r"])
        exhausted = idx in r1_widened and step == "B"
        per_col.setdefault(idx, []).append({"case": case, "entry_used": used, "source": "R1 key" if idx in spec_fs else "template", "r_lo": its[0]["r"], "r_hi": its[1]["r"], "w1": new, "step": step, "remiss_of_R1_widened": idx in r1_widened})
merged = {}
for idx, rows in per_col.items():
    vals = {canon(r["w1"]) for r in rows}
    if len(vals) == 1: merged[idx] = rows[0]["w1"]
    else:
        merged[idx] = [min(r["w1"][0] for r in rows), max(r["w1"][1] for r in rows)]; findings.append("conflict col %s -> hull" % idx)
exp = copy.deepcopy(r1); exp["rule"]["fs_absolute_overrides"].update(merged)
out["miss_set"] = {c: sorted(int(i) for i in scan[r]["passes"]["fs"]["fail"]) for c, r in CASES.items()}
out["per_column"] = per_col; out["merged_new_entries"] = merged
out["expected_R2_equals_builder_R2"] = canon(exp) == canon(r2)
out["R2_changed_keys_vs_R1"] = sorted(k for k in r2["rule"] if canon(r2["rule"][k]) != canon(r1["rule"][k]))
out["R2_fs_diff_vs_R1"] = {k: [r1fs.get(k), v] for k, v in r2["rule"]["fs_absolute_overrides"].items() if r1fs.get(k) != v}
# sealed validator
spec_ = importlib.util.spec_from_file_location("kmax_compare_c2v005_sealed", CMP); m = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(m)
out["validator_R2"] = m.validate_recovery(pre, r2)
out["validator_R1"] = m.validate_recovery(pre, r1)
keys_ok = {"brackets", "reason"} <= set(r2doc) <= {"brackets", "reason", "invocation", "widened_entries", "evidence"}
out["main_file_schema_ok"] = keys_ok and isinstance(r2doc.get("brackets"), dict) and r2doc["brackets"].get("mode") == "rule"
muts = {}
x = copy.deepcopy(r2); x["rule"]["fs_absolute_overrides"]["5"] = [302500000.0, 317625000.0]; muts["R1_entry5_reverted"] = m.validate_recovery(pre, x)
x = copy.deepcopy(r2); x["rule"]["fs_absolute_overrides"]["3"] = [160000000.0, 317625000.0]; muts["new3_not_contain_template"] = m.validate_recovery(pre, x)
x = copy.deepcopy(r2); x["rule"]["rfs_factors"] = [0.8, 1.3]; muts["nonoverride_changed"] = m.validate_recovery(pre, x)
x = copy.deepcopy(r2); del x["rule"]["fs_absolute_overrides"]["46"]; muts["anchor46_removed"] = m.validate_recovery(pre, x)
x = copy.deepcopy(r2); x["rule"]["fs_absolute_overrides"]["46"] = [151250000.0, 310000000.0]; muts["anchor46_narrowed"] = m.validate_recovery(pre, x)
out["validator_mutations"] = muts
out["validator_live"] = all(len(v) > 0 for v in muts.values())
import re
out["R2_key_lint_bad"] = [k for t in ("fs_absolute_overrides", "rfs_factor_overrides") for k in r2["rule"][t] if not re.fullmatch(r"0|[1-9][0-9]*", k)] + \
    [k for ps, tab in r2["rule"]["le_factor_overrides"].items() for k in [ps, *tab] if not re.fullmatch(r"0|[1-9][0-9]*", k)]
# widened_entries record consistency
we = r2doc["widened_entries"]
out["widened_entries_R1_part_equals_R1"] = all(canon({k: v for k, v in we[i].items() if k != "invocation"}) == canon(json.load(open(R1F))["widened_entries"][i]) for i in r1_widened)
out["widened_entries_R2_part_to_equals_merged"] = all(we[i]["to"] == merged[i] for i in merged)
out["findings"] = findings
print(json.dumps(out, indent=1))
