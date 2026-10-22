"""R3 checker C4: evaluate checker-rerun dry-runs (Y2R3 v001, C4R3 v005) independently, and all 10 builder dry-runs' fs tables."""
import glob, hashlib, json, os, re

BASE = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2"
R3D = BASE + "/d7_recovery_r3"
CHK = R3D + "/check/dryrun_chk_r3"
OUT = R3D + "/check/C4_DRYRUN_EVAL_V001.json"
TPL = [1.5125e8, 3.025e8]
DRV = {"v001": "75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22",
       "v005": "2aef51c4a4cf0ee192594ab366e9b37e54881977df2e4d1b2f259a759818a42f"}
CASES = {"C2R3": ("v001", "dryrun_r2/C2R2"), "S2R3": ("v001", "dryrun_r2/S2R2"), "Y2R3": ("v001", "dryrun_r2/Y2R2"),
         "C3R3": ("v005", "dryrun_r2/C3R2"), "S3R3": ("v005", "dryrun_r2/S3R2"), "Y3R3": ("v005", "dryrun_r2/Y3R2"),
         "RR3": ("v005", "dryrun_r2/RR2"), "C4R3": ("v005", "dryrun_r2_c4/C4R2"), "S4R3": ("v005", "dryrun_r2_c4/S4R2"),
         "Y4R3": ("v005", "dryrun_r2_c4/Y4R2")}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def fs_table(d):
    t, dup = {}, []
    for f in sorted(glob.glob(d + "/simulated_call/inputs/fs_controls_*.json")):
        c = json.load(open(f))
        for i in c["radial_indices"]:
            if i in t:
                dup.append(i)
            t[i] = c["solver"]["enthalpy_bracket"]
    return t, dup


def get(rep, k):
    if k in rep:
        return rep[k]
    return (rep.get("summary") or {}).get(k)


def norm(o, root):
    s = json.dumps(o, sort_keys=True).replace(root, "$DRY")
    return re.sub(r"PENDING_SHA256\([^)]*\)", "PENDING", s)


r3 = json.load(open(R3D + "/KMAX_D7_RECOVERY_R3.json"))["brackets"]["rule"]["fs_absolute_overrides"]
expect = {i: r3.get(str(i), TPL) for i in range(72)}
F, out = [], {"builder_dryruns": {}, "checker_reruns": {}}
for name, (drv, r2rel) in CASES.items():
    d = R3D + "/dryrun_r3/" + name
    t, dup = fs_table(d)
    t2, _ = fs_table(BASE + "/d7_recovery_r2/" + r2rel)
    rep = json.load(open(d + "/DRYRUN_REPORT.json"))
    spec = f"{R3D}/specs_d7r3/CALL_KMAX_{name}_A2F10_D7R3_C2V005.json"
    diffc = sorted(i for i in range(72) if t.get(i) != t2.get(i))
    rec = {"fs_equals_R3": t == expect, "dups": dup, "diff_vs_R2_dryrun": diffc,
           "spec_sha_ok": rep["call_spec_sha256"] == sha(spec), "driver_sha_ok": rep["driver_sha256"] == DRV[drv],
           "n_stages": len(rep["stages"]), "pin_problems": get(rep, "pin_problems"), "scipy_imports": get(rep, "scipy_imports"),
           "stderr_bytes": os.path.getsize(R3D + "/dryrun_r3/" + name + ".stderr.txt")}
    if drv == "v005":
        rec.update({k: get(rep, k) for k in ("binding_blockers", "unexplained_refusals", "refusals_beyond_pending_inputs",
                                              "stage_admission_refused", "remaining_refusals_by_class")})
    ok = (rec["fs_equals_R3"] and not dup and diffc == [2, 66, 67, 68, 71] and rec["spec_sha_ok"] and rec["driver_sha_ok"]
          and rec["n_stages"] == 9 and not rec["pin_problems"] and not rec["scipy_imports"] and rec["stderr_bytes"] == 0)
    if drv == "v005":
        ok = ok and not rec["binding_blockers"] and not rec["unexplained_refusals"] and not rec["refusals_beyond_pending_inputs"] \
            and not rec["stage_admission_refused"] and rec["remaining_refusals_by_class"] == {"PRODUCED_BY_THIS_CALL": ["custody.offset_finish_sha256"]}
    rec["ok"] = ok
    if not ok:
        F.append(f"builder dry-run {name} fails checker evaluation: {rec}")
    out["builder_dryruns"][name] = rec
# checker reruns
for name in ("Y2R3", "C4R3"):
    d, bd = CHK + "/" + name, R3D + "/dryrun_r3/" + name
    rep = json.load(open(d + "/DRYRUN_REPORT.json"))
    brep = json.load(open(bd + "/DRYRUN_REPORT.json"))
    t, dup = fs_table(d)
    bt, _ = fs_table(bd)
    rec = {"report_sha256": sha(d + "/DRYRUN_REPORT.json"), "fs_equals_R3": t == expect, "fs_equals_builder": t == bt,
           "stderr_bytes": os.path.getsize(CHK + "/" + name + ".stderr.txt"),
           "spec_sha_ok": rep["call_spec_sha256"] == sha(f"{R3D}/specs_d7r3/CALL_KMAX_{name}_A2F10_D7R3_C2V005.json"),
           "driver_sha_ok": rep["driver_sha256"] == DRV[CASES[name][0]], "n_stages": len(rep["stages"]),
           "report_equal_builder_after_path_norm": norm(rep, d) == norm(brep, bd)}
    if not rec["report_equal_builder_after_path_norm"]:
        a, b = json.loads(norm(rep, d)), json.loads(norm(brep, bd))
        rec["differing_top_keys"] = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    # inputs other than path-bearing must match too
    same_inputs = []
    for f in sorted(glob.glob(d + "/simulated_call/inputs/*.json")):
        g = bd + "/simulated_call/inputs/" + os.path.basename(f)
        same_inputs.append((os.path.basename(f), os.path.exists(g) and norm(json.load(open(f)), d) == norm(json.load(open(g)), bd)))
    rec["inputs_equal_builder_after_path_norm"] = same_inputs
    for k in ("fs_equals_R3", "fs_equals_builder", "spec_sha_ok", "driver_sha_ok"):
        if not rec[k]:
            F.append(f"checker rerun {name}: {k} false")
    if rec["stderr_bytes"] or rec["n_stages"] != 9:
        F.append(f"checker rerun {name}: stderr/stages")
    out["checker_reruns"][name] = rec
out["findings"] = F
json.dump(out, open(OUT, "w"), indent=1, sort_keys=True)
print(json.dumps({k: {n: v.get("ok", v) for n, v in out[k].items()} for k in ("builder_dryruns",)}, indent=1))
print(json.dumps(out["checker_reruns"], indent=1))
print("findings", F)
