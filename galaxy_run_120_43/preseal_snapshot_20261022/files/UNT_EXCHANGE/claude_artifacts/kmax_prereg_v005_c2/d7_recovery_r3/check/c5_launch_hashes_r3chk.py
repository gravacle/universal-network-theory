"""R3 checker C5: LAUNCH_R3 vs LAUNCH_R2 (argv modulo R2->R3 names), HASHES.txt from bytes, stop record untouched."""
import hashlib, json, os

BASE = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2"
R3D = BASE + "/d7_recovery_r3"
OUT = R3D + "/check/C5_LAUNCH_HASHES_V001.json"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


F, out = [], {}
L2 = json.load(open(BASE + "/d7_recovery_r2/LAUNCH_R2.json"))
L3 = json.load(open(R3D + "/LAUNCH_R3.json"))
c2 = {c["case"]: c for c in L2["calls"]}
c3 = {c["case"]: c for c in L3["calls"]}
spec_shas = {n: sha(f"{R3D}/specs_d7r3/CALL_KMAX_{n}_A2F10_D7R3_C2V005.json") for n in c3}
argv_cmp = {}
for n3, c in c3.items():
    n2 = n3[:-1] + "2"
    if n2 in c2:
        exp = [a.replace("d7_recovery_r2/specs_d7r2/", "d7_recovery_r3/specs_d7r3/").replace(n2 + "_A2F10_D7R2", n3 + "_A2F10_D7R3")
               .replace("KMAX_A2F10_%s_D7R2_RUN_V001" % n2, "KMAX_A2F10_%s_D7R3_RUN_V001" % n3) for a in c2[n2]["argv"]]
        argv_cmp[n3] = {"vs": n2, "equal_mod_names": exp == c["argv"], "caps_equal": c2[n2]["caps"] == c["caps"]}
    else:
        # C4/S4/Y4 had no R2 launch entry in LAUNCH_R2 (templates); compare with C3R3 shape
        ref = c3["C3R3"]["argv"]
        exp = [a.replace("C3R3", n3) for a in ref]
        argv_cmp[n3] = {"vs": "C3R3 shape", "equal_mod_names": exp == c["argv"], "caps_equal": c["caps"] == c3["C3R3"]["caps"]}
    if c["spec"]["sha256"] != spec_shas[n3]:
        F.append(f"{n3}: launch spec sha != spec bytes")
    if not (argv_cmp[n3]["equal_mod_names"] and argv_cmp[n3]["caps_equal"]):
        F.append(f"{n3}: argv/caps differ from R2 pattern")
out["argv_cmp"] = argv_cmp
out["templates_pending"] = L3.get("templates_pending")
out["R3_pin_ok"] = L3["R3"]["sha256"] == sha(R3D + "/KMAX_D7_RECOVERY_R3.json")
out["prereg_pin_ok"] = L3["prereg"]["sha256"] == sha(BASE + "/KMAX_MATRIX_PREREG_V005.json")
out["monitor_pin_ok"] = L3["monitor"]["sha256"] == sha(L3["monitor"]["path"])
out["comparison_binding"] = L3["comparison_binding"]
out["comparison_flag_ok"] = L3["comparison_flag"] == "--bracket-recovery " + R3D + "/KMAX_D7_RECOVERY_R3.json"
for k in ("R3_pin_ok", "prereg_pin_ok", "monitor_pin_ok", "comparison_flag_ok"):
    if not out[k]:
        F.append(k + " false")
if L3.get("templates_pending"):
    F.append("templates pending")
# HASHES.txt
bad, n, listed = [], 0, set()
for line in open(R3D + "/HASHES.txt"):
    line = line.rstrip("\n")
    if not line.strip():
        continue
    h, p = line.split(None, 1)
    p = p.strip().lstrip("*")
    full = p if p.startswith("/") else os.path.join(R3D, p)
    listed.add(os.path.relpath(full, R3D))
    n += 1
    if not os.path.exists(full) or sha(full) != h:
        bad.append(p)
out["hashes_lines"] = n
out["hashes_bad"] = bad
on_disk = set()
for root, dirs, files in os.walk(R3D):
    if os.path.relpath(root, R3D).split(os.sep)[0] == "check":
        continue
    for fn in files:
        on_disk.add(os.path.relpath(os.path.join(root, fn), R3D))
out["unlisted_on_disk"] = sorted(on_disk - listed - {"HASHES.txt"})
if bad:
    F.append(f"HASHES.txt mismatches: {bad[:10]}")
out["file_shas"] = {f: sha(R3D + "/" + f) for f in ("LAUNCH_R3.json", "LAUNCH_R3.md", "HASHES.txt", "make_d7r3_c2.py",
                                                    "BUILD_R3_RECORD.json", "DRYRUN_R3_CHECKS.json", "KMAX_D7_RECOVERY_R3.json",
                                                    "D7_EVIDENCE_C4R2_S4R2_Y4R2_V001.json", "STOPPED_R2_RUNS_V001.json")}
if out["file_shas"]["STOPPED_R2_RUNS_V001.json"] != "f8a99d55b202a5c17635c860297e7f0a599de079c7d3dc86891c25730f7c9149":
    F.append("stop record sha differs from builder-reported")
out["findings"] = F
json.dump(out, open(OUT, "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1))
