"""R3 checker C2: R3 contents, sealed validator acceptance, checker-chosen tampers refused."""
import copy, hashlib, importlib.util, json, re

BASE = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2"
OUT = BASE + "/d7_recovery_r3/check/C2_R3_VALIDATOR_V001.json"
KEY = re.compile(r"0|[1-9][0-9]*")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"))


def contains(o, i):
    return isinstance(o, list) and len(o) == 2 and o[0] <= i[0] and i[1] <= o[1]


f = []
cmp_path = BASE + "/kmax_compare_c2v005.py"
pre_path = BASE + "/KMAX_MATRIX_PREREG_V005.json"
out = {"compare_sha256": sha(cmp_path), "prereg_sha256": sha(pre_path)}
if not out["compare_sha256"].startswith("49404bc4"):
    f.append("compare sha mismatch")
if not out["prereg_sha256"].startswith("dbddc02c"):
    f.append("prereg sha mismatch")
spec = importlib.util.spec_from_file_location("kmax_compare_sealed", cmp_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
pre = json.load(open(pre_path))
r1p, r2p, r3p = (BASE + "/d7_recovery/KMAX_D7_RECOVERY_R1.json", BASE + "/d7_recovery_r2/KMAX_D7_RECOVERY_R2.json",
                 BASE + "/d7_recovery_r3/KMAX_D7_RECOVERY_R3.json")
r1, r2, r3 = (json.load(open(p)) for p in (r1p, r2p, r3p))
out["shas"] = {"R1": sha(r1p), "R2": sha(r2p), "R3": sha(r3p)}
# file schema exactly as compare main()
keys_ok = {"brackets", "reason"} <= set(r3) <= {"brackets", "reason", "invocation", "widened_entries", "evidence"} \
    and isinstance(r3.get("brackets"), dict) and r3["brackets"].get("mode") == "rule"
out["file_schema_ok"] = keys_ok
out["validate_R3"] = mod.validate_recovery(pre, r3["brackets"])
out["validate_R2"] = mod.validate_recovery(pre, r2["brackets"])
if out["validate_R3"] or not keys_ok:
    f.append("R3 refused by sealed validator: %s" % out["validate_R3"])
b2, b3 = r2["brackets"]["rule"], r3["brackets"]["rule"]
out["changed_rule_keys_vs_R2"] = sorted(k for k in set(b2) | set(b3) if canon(b2.get(k)) != canon(b3.get(k)))
if out["changed_rule_keys_vs_R2"] != ["fs_absolute_overrides"]:
    f.append("rule keys other than fs changed vs R2: %s" % out["changed_rule_keys_vs_R2"])
fs2, fs3 = b2["fs_absolute_overrides"], b3["fs_absolute_overrides"]
out["fs_added_vs_R2"] = sorted(set(fs3) - set(fs2), key=int)
out["fs_removed_vs_R2"] = sorted(set(fs2) - set(fs3), key=int)
out["fs_changed_vs_R2"] = sorted((k for k in fs2 if k in fs3 and fs2[k] != fs3[k]), key=int)
if out["fs_added_vs_R2"] != ["2", "66", "67", "68", "71"] or out["fs_removed_vs_R2"] or out["fs_changed_vs_R2"]:
    f.append("fs delta vs R2 unexpected")
for nm, prev in (("R1", r1["brackets"]["rule"]), ("R2", b2), ("anchor", pre["anchor"]["brackets"]["rule"])):
    for key in ("fs_absolute_overrides", "rfs_factor_overrides"):
        for k, e in prev[key].items():
            if not contains(b3[key].get(k), e):
                f.append("%s %s[%s] not contained in R3" % (nm, key, k))
lint = []
for key in ("fs_absolute_overrides", "rfs_factor_overrides"):
    for k in b3[key]:
        if not KEY.fullmatch(k) or not (0 <= int(k) < 72):
            lint.append((key, k))
for ps, tab in b3["le_factor_overrides"].items():
    for k in tab:
        if not KEY.fullmatch(k):
            lint.append(("le", ps, k))
out["key_lint_failures"] = lint
if lint:
    f.append("key lint: %s" % lint)
# metadata consistency
we = r3["widened_entries"]
for k in out["fs_added_vs_R2"]:
    w = we.get(k, {})
    if w.get("invocation") != "R3" or w.get("to") != fs3[k] or w.get("from_R2") != [1.5125e8, 3.025e8]:
        f.append("widened_entries[%s] metadata mismatch: %s" % (k, w))
for k, w in r2["widened_entries"].items():
    if canon(we.get(k)) != canon(w):
        f.append("R2 widened_entries[%s] not carried verbatim" % k)
ev = r3["evidence"]
for nm, p in (("R1_recovery_file", r1p), ("R2_recovery_file", r2p),
              ("R3_evidence_file", BASE + "/d7_recovery_r3/D7_EVIDENCE_C4R2_S4R2_Y4R2_V001.json")):
    if ev.get(nm, {}).get("sha256") != sha(p):
        f.append("evidence pointer %s sha mismatch" % nm)
out["r3_invocation"] = r3.get("invocation")
# checker-chosen tampers (distinct from the builder's two)
tampers = {}
t = copy.deepcopy(r3["brackets"]); del t["rule"]["fs_absolute_overrides"]["46"]
tampers["T1_remove_anchor_R1_entry_46"] = t
t = copy.deepcopy(r3["brackets"]); t["rule"]["rfs_factors"] = [0.7, 1.2]
tampers["T2_change_nonoverride_rfs_factors"] = t
t = copy.deepcopy(r3["brackets"]); t["rule"]["rfs_factor_overrides"]["71"] = [0.85, 1.01]
tampers["T3_narrow_anchor_rfs71"] = t
t = copy.deepcopy(r3["brackets"]); t["rule"]["fs_absolute_overrides"]["71"] = [1.5125e8, 3.0e8]
tampers["T4_new_fs71_narrower_than_template"] = t
t = copy.deepcopy(r3["brackets"]); t["rule"]["extra"] = 1
tampers["T5_extra_rule_key"] = t
out["tampers"] = {}
for nm, blk in tampers.items():
    why = mod.validate_recovery(pre, blk)
    out["tampers"][nm] = why
    if not why:
        f.append("tamper %s ACCEPTED by validator" % nm)
# limitation probe: validator does not enforce R2 containment (only anchor + R1)
t = copy.deepcopy(r3["brackets"]); t["rule"]["fs_absolute_overrides"]["3"] = [1.5125e8, 3.025e8]
out["probe_R2_entry3_reverted_validator_reasons"] = mod.validate_recovery(pre, t)
out["findings"] = f
json.dump(out, open(OUT, "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1))
