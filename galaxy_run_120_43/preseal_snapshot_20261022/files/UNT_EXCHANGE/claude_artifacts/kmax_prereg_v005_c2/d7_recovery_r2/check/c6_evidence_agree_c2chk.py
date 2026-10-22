# Independent checker C6: builder evidence file vs checker scan (hashes, residuals, entries, finish status, launch pins).
import json, hashlib, os
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(H)
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
e = json.load(open(B + "/D7_EVIDENCE_C3R_S3_Y3_V001.json")); s = json.load(open(H + "/C1_RUN_SCAN_V001.json"))
w = json.load(open(H + "/C2_W1_R2_VALIDATOR_V001.json"))
bad = []; n = 0
for case, ce in e.items():
    run = os.path.basename(ce["run"]); sc = s[run]
    if ce["finish"]["status"] != sc["finish"]["status"] or ce["finish"]["reasons"] != sc["finish"]["reasons"]: bad.append((case, "finish"))
    if ce["finish"].get("sha256") and ce["finish"]["sha256"] != sc["finish"]["sha256"]: bad.append((case, "finish sha"))
    if sorted(m["index"] for m in ce["missed_columns"]) != sorted(int(i) for i in sc["passes"]["fs"]["fail"]): bad.append((case, "miss set"))
    for m in ce["missed_columns"]:
        n += 1; f = sc["passes"]["fs"]["fail"][str(m["index"])]
        if m["failure_file"]["sha256"] != f["failure_sha256"] or m["iterations_file"]["sha256"] != f["iterations_sha256"]: bad.append((case, m["index"], "hash"))
        if [(x["Hc_m2_s2"], x["mass_relative_residual"]) for x in m["evidence"]] != [(x["Hc"], x["r"]) for x in f["iters"]]: bad.append((case, m["index"], "evidence"))
        mine = [r for r in w["per_column"][str(m["index"])] if r["case"] == case][0]
        if m["entry_in_failed_call"] != mine["entry_used"] or m["W1"]["new_entry"] != mine["w1"] or m["W1"]["declared_step"] != mine["step"]: bad.append((case, m["index"], "W1"))
    if ce["call_spec"]["sha256"] != sha(ce["call_spec"]["path"]): bad.append((case, "spec sha"))
print(json.dumps({"n_missed_entries_checked": n, "disagreements": bad}))
