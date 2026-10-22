# Independent checker C5: LAUNCH_R2.json argv vs specs, drivers, caps (vs R1 launch.json), outdir/receipt absence; HASHES.txt from bytes.
import json, hashlib, os, re, shlex
B = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/d7_recovery_r2"
R = "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs"
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
PY = "/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
MON = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py"
DRV = {"v001": ("/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/galaxy_m0_forward_c2v001.py", "75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22", 21600),
       "v005": ("/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_impl_c2/binding/galaxy_m0_forward_c2v005.py", "2aef51c4a4cf0ee192594ab366e9b37e54881977df2e4d1b2f259a759818a42f", 28800)}
CASE_DRV = {"C2R2": "v001", "S2R2": "v001", "Y2R2": "v001", "C3R2": "v005", "S3R2": "v005", "Y3R2": "v005", "RR2": "v005"}
R1L = {"C2R2": "KMAX_A2F10_C2R_D7R1_RUN_V001", "S2R2": "KMAX_A2F10_S2R_D7R1_RUN_V001", "Y2R2": "KMAX_A2F10_Y2R_D7R1_RUN_V001",
       "C3R2": "KMAX_A2F10_C3R_D7R1_V005_RUN_V001", "S3R2": "KMAX_A2F10_S3_D7R1_V005_RUN_V001", "Y3R2": "KMAX_A2F10_Y3_D7R1_V005_RUN_V001", "RR2": "KMAX_A2F10_R_V005_RUN_V001"}
L = json.load(open(B + "/LAUNCH_R2.json"))
out = {"launch_sha256": sha(B + "/LAUNCH_R2.json"), "top_keys": sorted(L)}
def find_entries(o):
    if isinstance(o, dict):
        if "argv" in o: yield o
        for v in o.values(): yield from find_entries(v)
    elif isinstance(o, list):
        for v in o: yield from find_entries(v)
ents = list(find_entries(L)); res = {}
for e in ents:
    a = e["argv"]; d = dict(zip(a[4::2], a[5::2])) if a[4:5] and a[4].startswith("--") else {}
    spec = d.get("--spec"); name = re.search(r"CALL_KMAX_(\w+?)_A2F10", spec).group(1)
    dv = CASE_DRV[name]; drv = DRV[dv]
    r1l = json.load(open(R + "/" + R1L[name] + ".receipt.json.launch.json"))
    exp_out = R + "/KMAX_A2F10_%s_D7R2_RUN_V001" % name
    chk = {"prefix_ok": a[:4] == [PY, "-I", "-B", MON], "driver_ok": d.get("--driver") == drv[0], "driver_sha_ok": d.get("--driver-sha256") == drv[1] == sha(drv[0]),
           "spec_exists_sha": sha(spec), "outdir_ok": d.get("--outdir") == exp_out, "receipt_ok": d.get("--receipt") == exp_out + ".receipt.json",
           "caps_ok": [float(d.get("--wall-cap-s")), int(d.get("--rss-cap-bytes")), int(d.get("--output-cap-bytes")), float(d.get("--poll-s"))] == [drv[2], 3221225472, 17179869184, 2.0],
           "caps_equal_R1_launch": [float(d.get("--wall-cap-s")), int(d.get("--rss-cap-bytes")), int(d.get("--output-cap-bytes")), float(d.get("--poll-s"))] == [r1l["caps"]["wall_cap_s"], r1l["caps"]["rss_cap_bytes"], r1l["caps"]["output_cap_bytes"], r1l["caps"]["poll_s"]],
           "R1_driver_same": r1l["pins"]["driver"]["sha256"] == drv[1],
           "outdir_absent": not os.path.exists(exp_out), "receipt_absent": not os.path.exists(exp_out + ".receipt.json"),
           "argv_len": len(a), "extra_args": sorted(set(d) - {"--driver", "--driver-sha256", "--spec", "--outdir", "--receipt", "--wall-cap-s", "--rss-cap-bytes", "--output-cap-bytes", "--poll-s"})}
    for k in ("shell", "command", "cmd"):
        if k in e: chk["shell_equals_argv"] = shlex.split(e[k]) == a
    res[name] = chk
out["entries"] = res
out["n_entries"] = len(ents)
# monitor help: argument names exist
mon_src = open(MON).read()
out["monitor_sha256"] = sha(MON)
out["monitor_has_args"] = {f: (f in mon_src) for f in ["--driver", "--driver-sha256", "--spec", "--outdir", "--receipt", "--wall-cap-s", "--rss-cap-bytes", "--output-cap-bytes", "--poll-s"]}
# HASHES.txt from bytes
bad = []; n = 0
for line in open(B + "/HASHES.txt"):
    m = re.match(r"([0-9a-f]{64})\s+(.+)$", line.strip())
    if not m: continue
    p = m.group(2); p = p if p.startswith("/") else os.path.join(B, p); n += 1
    if not os.path.exists(p): bad.append(("missing", p)); continue
    if sha(p) != m.group(1): bad.append(("mismatch", p))
for line in open(B + "/HASHES_ADDENDUM.txt"):
    m = re.match(r"([0-9a-f]{64})\s+(.+)$", line.strip())
    if m:
        p = m.group(2); p = p if p.startswith("/") else os.path.join(B, p); n += 1
        if sha(p) != m.group(1): bad.append(("mismatch", p))
out["hashes_checked"] = n; out["hashes_bad"] = bad
print(json.dumps(out, indent=1))
