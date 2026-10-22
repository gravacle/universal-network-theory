# Independent checker C1: scan column outcome listings + failure/iterations files (allowed D7 evidence only).
import json, os, re, sys, hashlib
R = "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs"
RUNS = sys.argv[1:]
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
out = {}
for name in RUNS:
    d = os.path.join(R, name)
    st = os.path.join(d, "stages")
    fin = os.path.join(d, "finish.json")
    rec = {"finish": None, "passes": {}}
    if os.path.exists(fin):
        f = json.load(open(fin)); rec["finish"] = {"status": f.get("status"), "reasons": f.get("reasons"), "sha256": sha(fin)}
    for s in sorted(os.listdir(st)):
        m = re.match(r"\d+_(fs|rfs|le\d+)_columns_\d+$", s)
        if not m: continue
        cd = os.path.join(st, s, "columns")
        if not os.path.isdir(cd): continue
        names = os.listdir(cd)
        ok = sorted(int(x[7:11]) for x in names if re.fullmatch(r"column_\d{4}\.json", x))
        fail = sorted(int(x[7:11]) for x in names if re.fullmatch(r"column_\d{4}_failure\.json", x))
        its = sorted(int(x[7:11]) for x in names if re.fullmatch(r"column_\d{4}_iterations\.jsonl", x))
        p = rec["passes"].setdefault(m.group(1), {"ok": [], "fail": {}, "iter_only": []})
        p["ok"] += ok
        for i in fail:
            ff = os.path.join(cd, "column_%04d_failure.json" % i)
            itf = os.path.join(cd, "column_%04d_iterations.jsonl" % i)
            fj = json.load(open(ff))
            iters = [json.loads(l) for l in open(itf) if l.strip()] if os.path.exists(itf) else None
            p["fail"][str(i)] = {"stage": s, "failure": fj, "failure_sha256": sha(ff),
                                 "iterations_sha256": sha(itf) if iters is not None else None,
                                 "iters": [{"Hc": it.get("Hc_m2_s2"), "r": it.get("mass_relative_residual")} for it in (iters or [])]}
        p["iter_only"] += [i for i in its if i not in ok and i not in fail]
    for k, p in rec["passes"].items():
        p["ok"] = sorted(p["ok"]); allidx = set(p["ok"]) | set(int(x) for x in p["fail"])
        p["n_ok"] = len(p["ok"]); p["missing_from_0_71"] = sorted(set(range(72)) - allidx)
        p["ok_and_fail_overlap"] = sorted(set(p["ok"]) & set(int(x) for x in p["fail"]))
        del p["ok"]
    out[name] = rec
print(json.dumps(out, indent=1))
