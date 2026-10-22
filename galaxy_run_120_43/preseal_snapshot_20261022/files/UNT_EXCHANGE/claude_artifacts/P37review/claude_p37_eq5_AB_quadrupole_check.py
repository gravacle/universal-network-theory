# Synthesizer check (Claude-authored, plain python3): does P37 eq.(5), which writes the
# per-A-cell diagonal-traceless insertion with ONE vertex polarization, equal the exact
# per-vertex sum (Ud/3) sum_i j_ii (Q_A,i + Q_B,i) on generic diamond ice states?
# Tests the uniform-source totals sum_A Q_A,i vs sum_B Q_B,i (and sum_A e_A vs sum_B e_B).
import random, itertools, json
random.seed(12345)
SIG = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
A1,A2,A3 = (0,1,1),(1,0,1),(1,1,0)   # FCC primitive vectors in units of a/2
def run(L, nupd):
    cells = list(itertools.product(range(L), repeat=3))
    idx = {c:i for i,c in enumerate(cells)}
    def sub(c, a): return tuple((c[k]-a[k]) % L for k in range(3))
    # edges: (A cell i, bond a) -> B cell
    edges = []
    for c in cells:
        for a, off in enumerate([(0,0,0), A1, A2, A3]):
            edges.append((idx[c], a, idx[sub(c, off)]))
    E = len(edges)
    occ = [1 if e[1] in (0,1) else 0 for e in edges]          # all A on pair {0,1}: valid ice
    adjA = [[] for _ in cells]; adjB = [[] for _ in cells]
    for k,(ia,a,ib) in enumerate(edges): adjA[ia].append(k); adjB[ib].append(k)
    def check():
        return all(sum(occ[k] for k in adjA[i]) == 2 for i in range(len(cells))) and \
               all(sum(occ[k] for k in adjB[i]) == 2 for i in range(len(cells)))
    assert check()
    for _ in range(nupd):          # alternating-loop updates (occupied A->B, empty B->A)
        v = ('A', random.randrange(len(cells))); path=[v]; epath=[]; seen={v:0}
        while True:
            if v[0]=='A':
                k = random.choice([k for k in adjA[v[1]] if occ[k]==1]); w=('B', edges[k][2])
            else:
                k = random.choice([k for k in adjB[v[1]] if occ[k]==0 and k != (epath[-1] if epath else -1)]); w=('A', edges[k][0])
            epath.append(k); v=w
            if v in seen:
                cyc = epath[seen[v]:]
                if v[0]=='A':
                    for kk in cyc: occ[kk]^=1
                break
            seen[v]=len(path); path.append(v)
    assert check()
    def pol(adj, i):
        s=[0,0,0]
        for k in adj[i]:
            if occ[k]:
                for t in range(3): s[t]+=SIG[edges[k][1]][t]
        return s
    eA=[pol(adjA,i) for i in range(len(cells))]; eB=[pol(adjB,i) for i in range(len(cells))]
    sumeA=[sum(e[t] for e in eA) for t in range(3)]; sumeB=[sum(e[t] for e in eB) for t in range(3)]
    axA=[sum(1 for e in eA if e[t]!=0) for t in range(3)]; axB=[sum(1 for e in eB if e[t]!=0) for t in range(3)]
    percell_mismatch = sum(1 for i in range(len(cells)) if [x*x for x in eA[i]]!=[x*x for x in eB[i]])
    return dict(L=L, cells=len(cells), sum_e_A=sumeA, sum_e_B=sumeB, axis_counts_A=axA, axis_counts_B=axB,
                cells_with_QA_ne_QB=percell_mismatch)
out=[]
for L in (2,3,4):
    for trial in range(5):
        out.append(run(L, 200))
res=dict(rows=out,
         linear_sums_equal_all=all(r['sum_e_A']==r['sum_e_B'] for r in out),
         quadrupole_sums_equal_all=all(r['axis_counts_A']==r['axis_counts_B'] for r in out),
         n_rows=len(out))
json.dump(res, open('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/P37review/claude_p37_eq5_AB_quadrupole_check_results.json','w'), indent=1)
print(json.dumps(res, indent=0)[:3000])
