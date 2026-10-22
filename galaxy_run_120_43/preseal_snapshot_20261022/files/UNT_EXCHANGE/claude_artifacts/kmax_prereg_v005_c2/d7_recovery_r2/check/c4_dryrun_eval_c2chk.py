# Independent checker C4: evaluate the checker's own dry-runs of all 7 filled R2 specs.
import json, glob, os, re, hashlib
H = os.path.dirname(os.path.abspath(__file__))
B = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2"
R2 = json.load(open(B+"/d7_recovery_r2/KMAX_D7_RECOVERY_R2.json"))["brackets"]["rule"]["fs_absolute_overrides"]
T = [151250000.0, 302500000.0]
R1D = {"C2R2": B+"/dryrun/C2R", "S2R2": B+"/dryrun/S2R", "Y2R2": B+"/dryrun/Y2R", "C3R2": B+"/dryrun_filled/C3R", "S3R2": B+"/dryrun_filled/S3", "Y3R2": B+"/dryrun_filled/Y3", "RR2": None}
def fs_table(d):
    t = {}
    for f in sorted(glob.glob(d + "/simulated_call/inputs/fs_controls_*.json")):
        c = json.load(open(f))
        for i in c["radial_indices"]:
            assert i not in t; t[i] = c["solver"]["enthalpy_bracket"]
    return t
def stage_names(d):
    return sorted(os.listdir(d + "/simulated_call/stages")) if os.path.isdir(d + "/simulated_call/stages") else None
out = {}
for n, r1d in R1D.items():
    d = H + "/dryrun_chk_r2/" + n
    full = json.load(open(d + "/DRYRUN_REPORT.json"))
    rep = json.load(open(H + "/dryrun_chk_r2/%s.stdout.txt" % n))
    assert rep == full["summary"], n
    t = fs_table(d)
    exp = {i: R2.get(str(i), T) for i in range(72)}
    r = {"stderr_bytes": os.path.getsize(H + "/dryrun_chk_r2/%s.stderr.txt" % n),
         "fs_cover_0_71": sorted(t) == list(range(72)), "fs_table_equals_R2": t == exp,
         "pin_problems": rep.get("pin_problems"), "scipy_imports": rep.get("scipy_imports"),
         "binding_blockers": rep.get("binding_blockers", "absent"), "unexplained_refusals": rep.get("unexplained_refusals", "absent"),
         "refusals_beyond_pending_inputs": rep.get("refusals_beyond_pending_inputs", "absent"),
         "stage_admission_refused": rep.get("stage_admission_refused", "absent"),
         "remaining_refusals_by_class": rep.get("remaining_refusals_by_class", "absent"),
         "stages_planned": rep.get("stages_planned"), "spec_sha_in_report": full["call_spec_sha256"], "driver_sha_in_report": full["driver_sha256"], "remaining_refusals_full": full.get("remaining_refusals", "absent")}
    if r1d:
        t1 = fs_table(r1d)
        r["fs_diff_vs_R1_dryrun"] = sorted(i for i in range(72) if t1.get(i) != t.get(i))
        rep1 = json.load(open(r1d + "/DRYRUN_REPORT.json"))["summary"]
        r["r1_stages_planned"] = rep1.get("stages_planned")
    # compare with builder dry-run report (ignoring paths)
    bd = B + "/d7_recovery_r2/dryrun_r2/" + n
    if os.path.isdir(bd):
        bt = fs_table(bd)
        r["fs_table_equals_builder_dryrun"] = bt == t
        brep = json.load(open(bd + "/DRYRUN_REPORT.json"))["summary"]
        strip = lambda o: json.loads(re.sub(r'"/[^"]*"', '"P"', json.dumps(o, sort_keys=True)))
        r["report_equals_builder_modulo_paths"] = strip(brep) == strip(rep)
    out[n] = r
print(json.dumps(out, indent=1))
