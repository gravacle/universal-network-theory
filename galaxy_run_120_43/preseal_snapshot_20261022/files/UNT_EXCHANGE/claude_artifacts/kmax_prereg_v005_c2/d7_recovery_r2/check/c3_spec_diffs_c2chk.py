# Independent checker C3: deep-diff every R2 spec vs its R1 counterpart; key lint; evidence-file agreement.
import json, hashlib, re, os, sys
B = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2"
N = B + "/d7_recovery_r2/specs_d7r2"
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
PAIRS = {
 "C2R2": (B+"/specs_d7r1/CALL_KMAX_C2R_A2F10_D7R1_C2V005.json", N+"/CALL_KMAX_C2R2_A2F10_D7R2_C2V005.json"),
 "S2R2": (B+"/specs_d7r1/CALL_KMAX_S2R_A2F10_D7R1_C2V005.json", N+"/CALL_KMAX_S2R2_A2F10_D7R2_C2V005.json"),
 "Y2R2": (B+"/specs_d7r1/CALL_KMAX_Y2R_A2F10_D7R1_C2V005.json", N+"/CALL_KMAX_Y2R2_A2F10_D7R2_C2V005.json"),
 "C3R2": (B+"/specs_d7r1/filled/CALL_KMAX_C3R_A2F10_D7R1_C2V005.json", N+"/CALL_KMAX_C3R2_A2F10_D7R2_C2V005.json"),
 "S3R2": (B+"/specs_d7r1/filled/CALL_KMAX_S3_A2F10_D7R1_C2V005.json", N+"/CALL_KMAX_S3R2_A2F10_D7R2_C2V005.json"),
 "Y3R2": (B+"/specs_d7r1/filled/CALL_KMAX_Y3_A2F10_D7R1_C2V005.json", N+"/CALL_KMAX_Y3R2_A2F10_D7R2_C2V005.json"),
 "RR2": (B+"/specs_d7r1/templates/CALL_KMAX_RR_A2F10_D7R1_C2V005.TEMPLATE.json", N+"/CALL_KMAX_RR2_A2F10_D7R2_C2V005.json"),
 "C4R2": (B+"/specs_d7r1/templates/CALL_KMAX_C4R_A2F10_D7R1_C2V005.TEMPLATE.json", N+"/templates/CALL_KMAX_C4R2_A2F10_D7R2_C2V005.TEMPLATE.json"),
 "S4R2": (B+"/specs_d7r1/templates/CALL_KMAX_S4_A2F10_D7R1_C2V005.TEMPLATE.json", N+"/templates/CALL_KMAX_S4R2_A2F10_D7R2_C2V005.TEMPLATE.json"),
 "Y4R2": (B+"/specs_d7r1/templates/CALL_KMAX_Y4_A2F10_D7R1_C2V005.TEMPLATE.json", N+"/templates/CALL_KMAX_Y4R2_A2F10_D7R2_C2V005.TEMPLATE.json"),
}
R2 = json.load(open(B+"/d7_recovery_r2/KMAX_D7_RECOVERY_R2.json"))["brackets"]
NEW = {"3","4","46","47","48","49"}
def diff(a, b, p=""):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a)|set(b)):
            if k not in a: out.append((p+"/"+k, "ADDED"))
            elif k not in b: out.append((p+"/"+k, "REMOVED"))
            else: out += diff(a[k], b[k], p+"/"+k)
        return out
    return [] if a == b else [(p, "CHANGED")]
def lint(o, p="", bad=None):
    bad = [] if bad is None else bad
    if isinstance(o, dict):
        for k, v in o.items():
            if p.endswith("_overrides") or re.search(r"le_factor_overrides$", p):
                if not re.fullmatch(r"0|[1-9][0-9]*", k): bad.append(p+"/"+k)
            lint(v, p+"/"+k, bad)
    return bad
res = {}
for name, (a, b) in PAIRS.items():
    A, Bj = json.load(open(a)), json.load(open(b))
    d = diff(A, Bj)
    allowed = []; unexpected = []
    for path, kind in d:
        m = re.fullmatch(r"/numerics/brackets/rule/fs_absolute_overrides/(\d+)", path)
        if m and m.group(1) in NEW: allowed.append((path, kind)); continue
        if path == "/label": allowed.append((path, kind)); continue
        if name == "RR2" and path.startswith("/admit"): allowed.append((path, kind)); continue
        unexpected.append((path, kind))
    res[name] = {"r1": a, "r1_sha256": sha(a), "r2": b, "r2_sha256": sha(b),
                 "brackets_equal_R2": json.dumps(Bj["numerics"]["brackets"], sort_keys=True) == json.dumps(R2, sort_keys=True),
                 "allowed_diffs": allowed, "unexpected_diffs": unexpected, "key_lint_bad": lint(Bj),
                 "picard_passes": Bj["numerics"]["picard"]["passes"],
                 "admit_keys": sorted(Bj.get("admit", {})) if isinstance(Bj.get("admit"), dict) else Bj.get("admit"),
                 "label_r1": A.get("label"), "label_r2": Bj.get("label")}
print(json.dumps(res, indent=1))
