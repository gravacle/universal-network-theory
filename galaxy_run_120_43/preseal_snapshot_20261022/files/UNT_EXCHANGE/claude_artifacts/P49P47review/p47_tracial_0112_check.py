"""Independent Claude check of P47-tracial-0112. Own code; no Codex imports."""
import json, sys, itertools
from fractions import Fraction as F
from collections import Counter, defaultdict

PLAN = "/Users/bgm/Research/UNT_EXCHANGE/lanes/P44_CODEX3/ROOT_COMPLETE_NATIVE_REBLOCK_V001/COMPLETE_REBLOCK_PLAN.json"
plan = json.load(open(PLAN))
out = {}
pieces = plan["pieces"]
out["plan_scalars"] = {k: plan[k] for k in plan if k not in ("pieces", "components")}
out["n_pieces"] = len(pieces)
ids = [p["id"] for p in pieces]
out["unique_piece_ids"] = len(set(ids)) == len(ids)
out["piece_dim_match"] = all(len(p["states"]) == p["dimension"] for p in pieces)
states = []
comp_of = {}
pflag = {}
for p in pieces:
    for s in p["states"]:
        t = tuple(s)
        states.append(t)
        comp_of[t] = p["component"]
        pflag[t] = p["P"]
out["n_states_listed"] = len(states)
out["n_unique"] = len(set(states))
out["P_count"] = sum(1 for t in states if pflag[t] is True)

# analytic sector enumeration (my own)
def sector():
    S = set()
    for sec in (0, 1):
        n = 2 + 2 * sec; e = 4 + 4 * sec
        for inc in range(1 << e):
            for q in range(1 << n):
                # Ready at a (bit0), no carrier
                S.add((sec, inc, 0, q, 1, 0))
                # Spent at a, carrier at one site
                for v in range(n):
                    S.add((sec, inc, 1 << v, q, 0, 1))
    return S
A = sector()
out["analytic_old"] = sum(1 for t in A if t[0] == 0)
out["analytic_born"] = sum(1 for t in A if t[0] == 1)
out["plan_equals_analytic_sector"] = set(states) == A

D = len(A); w = F(1, D)
old_n = out["analytic_old"]; born_n = out["analytic_born"]
out["D"] = D
out["w_born"] = str(F(born_n, D))

def bit(x, i): return (x >> i) & 1
sites = ["a", "b", "c", "d"]
def present(t, i): return i < 2 + 2 * t[0]

mom = {}
for i, v in enumerate(sites):
    mom[v] = dict(
        present=sum(F(present(t, i)) for t in A) * w,
        q=sum(bit(t[3], i) for t in A) * w,
        p=sum(bit(t[2], i) for t in A) * w,
        S=sum(bit(t[5], i) for t in A) * w,
        R=sum(bit(t[4], i) for t in A) * w,
        p_center_q=sum(bit(t[2], 0) * bit(t[3], i) for t in A) * w,
    )
center_p = sum(bit(t[2], 0) for t in A) * w
out["center_p"] = str(center_p)
out["moments"] = {v: {k: str(x) for k, x in d.items()} for v, d in mom.items()}
out["q_c_given_pa"] = str(mom["c"]["p_center_q"] / center_p)
out["q_c_given_pa_minus_q_c"] = str(mom["c"]["p_center_q"] / center_p - mom["c"]["q"])
out["q_a_given_pa"] = str(mom["a"]["p_center_q"] / center_p)

# pairs (zero-extended) and connected
pairs = {}
for i, j in itertools.combinations(range(4), 2):
    qq = sum(bit(t[3], i) * bit(t[3], j) for t in A) * w
    conn = qq - mom[sites[i]]["q"] * mom[sites[j]]["q"]
    pairs[sites[i] + sites[j]] = dict(qq=str(qq), connected=str(conn))
out["pairs"] = pairs
# presence covariance decomposition
out["Ccd_formula_w(1-w)/4"] = str(F(born_n, D) * (1 - F(born_n, D)) / 4)

# words
groups = {"old": [0, 1], "new": [2, 3], "all": [0, 1, 2, 3]}
words = {}
for g, idx in groups.items():
    k = len(idx)
    pres = sum(F(all(present(t, i) for i in idx)) for t in A) * w
    W = Counter()
    for t in A:
        if all(present(t, i) for i in idx):
            W["".join(str(bit(t[3], i)) for i in idx)] += 1
    probs = {format(x, "0%db" % k): F(W[format(x, "0%db" % k)]) * w for x in range(1 << k)}
    cond = {s: probs[s] / pres for s in probs}
    words[g] = dict(present=str(pres), distinct_word_probs=sorted(set(str(x) for x in probs.values())),
                    distinct_conditional=sorted(set(str(x) for x in cond.values())), nbins=len(probs))
out["words"] = words

# conditional new word independence given presence
# p_center joint with old q
out["p_a_q_a"] = str(sum(bit(t[2], 0) * bit(t[3], 0) for t in A) * w)
out["p_a_q_b"] = str(sum(bit(t[2], 0) * bit(t[3], 1) for t in A) * w)

# carrier probabilities, other sites
out["carrier_marginals"] = {v: str(mom[v]["p"]) for v in sites}
out["ready_a"] = str(mom["a"]["R"]); out["spent_a"] = str(mom["a"]["S"])

# per-component composition
comp = defaultdict(lambda: Counter())
cstats = defaultdict(lambda: dict(n=0, old=0, born=0, pa=0, qcqd=0, qc=0, qd=0, P=0))
for t in states:
    c = comp_of[t]; s = cstats[c]
    s["n"] += 1; s["old" if t[0] == 0 else "born"] += 1
    s["pa"] += bit(t[2], 0); s["qc"] += bit(t[3], 2); s["qd"] += bit(t[3], 3)
    s["qcqd"] += bit(t[3], 2) * bit(t[3], 3); s["P"] += int(pflag[t] is True)
cs = {}
for c, s in sorted(cstats.items()):
    n = s["n"]
    cs[c] = dict(n=n, old=s["old"], born=s["born"], P=s["P"], w_born=str(F(s["born"], n)), center_p=str(F(s["pa"], n)),
                 C_cd=str(F(s["qcqd"], n) - F(s["qc"], n) * F(s["qd"], n)))
out["components"] = cs

# per-component: what distinguishes them? look at incidence/carrier/ready/q patterns
def feat(t):
    sec, inc, p, q, r, s = t
    return dict(sec=sec, ready=r, carrier=p, inc_pop=bin(inc).count("1"))
compfeat = defaultdict(lambda: defaultdict(Counter))
for t in states:
    c = comp_of[t]
    for k, v in feat(t).items():
        compfeat[c][k][v] += 1
    compfeat[c]["q"][t[3]] += 1
out["component_features"] = {c: {k: dict(sorted(v.items())) for k, v in d.items()} for c, d in sorted(compfeat.items())}
json.dump(out, open(sys.argv[1], "w"), indent=1, sort_keys=True)
print(json.dumps({k: out[k] for k in out if k not in ("component_features",)}, indent=1, sort_keys=True))
