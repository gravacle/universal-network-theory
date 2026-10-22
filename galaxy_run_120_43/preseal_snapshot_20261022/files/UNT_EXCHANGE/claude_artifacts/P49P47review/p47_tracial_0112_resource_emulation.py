"""Claude's own emulation of the archive encoding/arithmetic load (no Codex code)."""
import json, sys, time, resource, itertools
from fractions import Fraction as F
PLAN = "/Users/bgm/Research/UNT_EXCHANGE/lanes/P44_CODEX3/ROOT_COMPLETE_NATIVE_REBLOCK_V001/COMPLETE_REBLOCK_PLAN.json"
t0 = time.monotonic()
def enc(v):
    if isinstance(v, F): return {"$rational": [v.numerator, v.denominator]}
    if isinstance(v, dict): return {k: enc(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)): return [enc(x) for x in v]
    return v
def size(v): return len((json.dumps(enc(v), indent=2, sort_keys=True, allow_nan=False) + "\n").encode())
plan = json.load(open(PLAN))
spec = json.load(open("/Users/bgm/Research/UNT_EXCHANGE/lanes/P47_CODEX3/HELD_P47_NATIVE_TRACIAL_SPEC_V001.json"))
sizes = {}
sizes["BATCH_PRECALL(spec+plan)"] = size(dict(spec=spec, plan=plan))
sizes["PREPARATION_PRECALL(plan)"] = size(dict(plan=plan))
states = sorted(tuple(s) for p in plan["pieces"] for s in p["states"])
rows = [dict(index=i, state=list(s), weight=F(1, 20672)) for i, s in enumerate(states)]
payload = dict(rows=rows, old_site_ids=["a","b"], new_site_ids=["c","d"], old_edge_count=4, expected_dimension=20672,
               conserved_Q=1, conserved_M=1, center_site="a", trace_norm_error_bound="0")
prepared = dict(state_payload=payload, old=192, Born=20480, dimension=20672, preparation="X", dynamics_executed=False)
sizes["PREPARATION_OUTPUT"] = size(prepared)
sizes["NETWORK_PRECALL(source+reference)"] = size(dict(source=payload, reference=payload, groups=[], denominator_floor="1/100"))
sizes["BATCH_OUTPUT(prepared+small result)"] = sizes["PREPARATION_OUTPUT"] + 200000
# Fraction arithmetic load comparable to 2 moment extracts + 2 network arms
t1 = time.monotonic()
for arm in range(2):
    sums = {v: {k: F(0) for k in range(5)} for v in range(4)}
    for r in rows:
        w = F(r["weight"]); sec, inc, p, q, rd, sp = r["state"]
        for i in range(4):
            bits = (int(i < 2 + 2 * sec), (q >> i) & 1, (sp >> i) & 1, (p >> i) & 1, (p & 1) * ((q >> i) & 1))
            for k, b in enumerate(bits): sums[i][k] += b * w
    for idx in ([0, 1], [2, 3], [0, 1, 2, 3]):
        words = {}; pr = F(0); ps = {ij: F(0) for ij in itertools.combinations(range(len(idx)), 2)}
        for r in rows:
            sec, inc, p, q, rd, sp = r["state"]; w = F(r["weight"])
            if all(i < 2 + 2 * sec for i in idx):
                pr += w; wd = "".join(str((q >> i) & 1) for i in idx); words[wd] = words.get(wd, F(0)) + w
            for (i, j) in ps: ps[(i, j)] += w * ((q >> idx[i]) & 1) * ((q >> idx[j]) & 1)
t2 = time.monotonic()
ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
peak = ru if sys.platform == "darwin" else ru * 1024
total = sum(sizes.values())
print(json.dumps(dict(sizes=sizes, total_major_bytes=total, cap_bytes=134217728, fraction_loop_seconds=round(t2 - t1, 2),
                      total_seconds=round(time.monotonic() - t0, 2), peak_rss_bytes=peak, rss_cap=536870912), indent=1))
