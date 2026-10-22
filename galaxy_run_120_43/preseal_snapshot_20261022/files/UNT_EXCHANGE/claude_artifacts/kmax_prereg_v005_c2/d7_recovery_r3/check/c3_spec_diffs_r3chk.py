"""R3 checker C3: every R3 spec vs its R2 counterpart (deep diff), brackets == R3 block, key lint, sha."""
import hashlib, json, re

BASE = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2"
R2S = BASE + "/d7_recovery_r2/specs_d7r2"
R3S = BASE + "/d7_recovery_r3/specs_d7r3"
RUNS = "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs"
OUT = BASE + "/d7_recovery_r3/check/C3_SPEC_DIFFS_V001.json"
KEY = re.compile(r"0|[1-9][0-9]*")
NAMES = ["C2", "S2", "Y2", "C3", "S3", "Y3", "R", "C4", "S4", "Y4"]
ADDED = {"2", "66", "67", "68", "71"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def diff(a, b, p=""):
    d = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                d.append(("added", p + "/" + k))
            elif k not in b:
                d.append(("removed", p + "/" + k))
            else:
                d += diff(a[k], b[k], p + "/" + k)
    elif a != b or type(a) != type(b):
        d.append(("changed", p))
    return d


def keys_lint(o, p=""):
    bad = []
    if isinstance(o, dict):
        for k, v in o.items():
            if p.endswith("_overrides") and not KEY.fullmatch(k):
                bad.append(p + "/" + k)
            bad += keys_lint(v, p + "/" + k)
    return bad


r3 = json.load(open(BASE + "/d7_recovery_r3/KMAX_D7_RECOVERY_R3.json"))["brackets"]
f, out = [], {}
for n in NAMES:
    nm2 = ("RR2" if n == "R" else n + "R2")
    nm3 = ("RR3" if n == "R" else n + "R3")
    p2 = (f"{R2S}/filled/CALL_KMAX_{nm2}_A2F10_D7R2_C2V005.json" if n.endswith("4")
          else f"{R2S}/CALL_KMAX_{nm2}_A2F10_D7R2_C2V005.json")
    p3 = f"{R3S}/CALL_KMAX_{nm3}_A2F10_D7R3_C2V005.json"
    a, b = json.load(open(p2)), json.load(open(p3))
    d = diff(a, b)
    allowed = {("changed", "/label")} | {("added", "/numerics/brackets/rule/fs_absolute_overrides/" + k) for k in ADDED}
    rec = {"r2_spec": p2, "r2_sha256": sha(p2), "r3_spec": p3, "r3_sha256": sha(p3),
           "diff": d, "diff_only_allowed": set(d) == allowed,
           "brackets_equal_R3": b["numerics"]["brackets"] == r3,
           "lint": keys_lint(b), "label_r3": b.get("label", "")[-200:],
           "admit_equal_R2": a.get("admit") == b.get("admit")}
    # launched R2 spec identity for the failed C4/S4/Y4 runs
    if n.endswith("4"):
        lj = open(f"{RUNS}/KMAX_A2F10_{nm2}_D7R2_RUN_V001.receipt.json.launch.json").read()
        rec["r2_spec_sha_in_launch_json"] = rec["r2_sha256"] in lj
        rec["r2_spec_path_in_launch_json"] = p2 in lj or p2.replace("/", "\\/") in lj
    for k in ("diff_only_allowed", "brackets_equal_R3", "admit_equal_R2"):
        if not rec[k]:
            f.append(f"{nm3}: {k} false ({d})")
    if rec["lint"]:
        f.append(f"{nm3}: key lint {rec['lint']}")
    if "D7R3" not in json.dumps(b.get("label")) and "R3" not in json.dumps(b.get("label")):
        f.append(f"{nm3}: label does not name R3")
    out[nm3] = rec
json.dump({"cases": out, "findings": f}, open(OUT, "w"), indent=1, sort_keys=True)
print(json.dumps({k: (v["r3_sha256"], v["diff_only_allowed"], v["brackets_equal_R3"], v["admit_equal_R2"],
                      v.get("r2_spec_sha_in_launch_json"), v.get("r2_spec_path_in_launch_json")) for k, v in out.items()}, indent=1))
print("label example:", out["C4R3"]["label_r3"])
print("findings", f)
