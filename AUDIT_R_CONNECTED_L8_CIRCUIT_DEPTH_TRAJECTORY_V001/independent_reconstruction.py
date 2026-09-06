#!/usr/bin/env python3
"""Independent depth-0..8 reconstruction; imports no target code or data."""
import json, math, os
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

checks=0
def check(v,label):
    global checks
    if not v: raise AssertionError(label)
    checks += 1

n=16; dim=1<<n; theta=math.pi/8; basis=np.arange(dim,dtype=np.uint32)
bits=np.array([((basis>>i)&1).astype(float) for i in range(n)])
rings=tuple((r+i,r+(i+1)%8) for r in (0,8) for i in range(8))
rungs=tuple((i,i+8) for i in range(8)); edges=rings+rungs
check(len(edges)==len(set(edges))==24,"oriented supports")
check(len({frozenset(e) for e in edges})==24,"physical supports")
clusters=tuple((x,z) for x in range(8) if x%2 for z in range(8) if z%2==0)
covered={(x,y,zz) for x,z in clusters for zz in (z,z+1) for y in range(8)}
heads={(x,y,z) for x in range(8) if x%2 for y in range(8) for z in range(8)}
check(len(clusters)==16 and covered==heads and len(heads)==256,"V8 partition")
c,s=math.cos(theta),1j*math.sin(theta)
check(abs(c*c+abs(s)**2-1)<2e-16,"gate unitary")
stagger=np.zeros(dim)
for i in range(n): stagger += (1 if i%2==0 else -1)*(1 if i<8 else -1)*bits[i]
phase=np.exp(-.5j*theta*stagger)
check(np.max(abs(abs(phase)-1))<2e-16,"onsite unitary")
check(all((-(1 if i%2==0 else -1))==(-1)*(1 if i%2==0 else -1) for i in range(8)),"reversed stagger")

def occ(state): return np.einsum("im,m->i",bits,abs(state)**2,optimize=False)
number=np.sum(bits,axis=0).astype(int)
law0=np.array([math.comb(n,k)/dim for k in range(n+1)])
psi=np.ones(dim,complex)/math.sqrt(dim); q0=occ(psi)
cum={e:0.0 for e in edges}; event=0.0; gate_records=[]; rows=[]; max_gate_err=0.0

def checkpoint(depth):
    q=occ(psi); div=np.zeros(n)
    for (i,j),v in cum.items(): div[i]+=v; div[j]-=v
    res=q-q0+div; p=abs(psi)**2
    corr=[np.sum(p*bits[i]*bits[j])-q[i]*q[j] for i,j in edges]
    law=np.array([p[number==k].sum() for k in range(n+1)])
    rv=np.array([cum[e] for e in rings]); uv=np.array([cum[e] for e in rungs]); av=np.r_[rv,uv]
    return {"depth":depth,"L8_expected_retained":float(16*q.sum()),
      "expected_retained_per_cluster":float(q.sum()),"q_min":float(q.min()),"q_max":float(q.max()),
      "first_ring_expected_retained":float(q[:8].sum()),"second_ring_expected_retained":float(q[8:].sum()),
      "cumulative_net_edge_throughput":float(abs(av).sum()),
      "cumulative_net_ring_throughput":float(abs(rv).sum()),
      "cumulative_net_inter_ring_throughput":float(abs(uv).sum()),
      "gate_event_absolute_traffic":float(event),
      "active_cumulative_edge_count":int(np.sum(abs(av)>1e-12)),
      "active_cumulative_inter_ring_edge_count":int(np.sum(abs(uv)>1e-12)),
      "max_abs_connected_edge_correlation":float(np.max(np.abs(corr))),
      "record_ledger_residual_l1_per_cluster":float(abs(res).sum()),
      "record_ledger_residual_linf_per_cluster":float(abs(res).max()),
      "norm_error":float(abs(np.vdot(psi,psi).real-1)),
      "number_law_max_change":float(np.max(abs(law-law0)))}

rows.append(checkpoint(0))
for depth in range(1,9):
    psi*=phase
    for edge_index,(i,j) in enumerate(edges):
        p_before=abs(psi)**2
        before_i=float(np.dot(bits[i],p_before)); before_j=float(np.dot(bits[j],p_before))
        select=(bits[i]==1)&(bits[j]==0); idx=basis[select]
        swp=idx^(1<<i)^(1<<j); a,b=psi[idx].copy(),psi[swp].copy()
        psi[idx]=c*a+s*b; psi[swp]=s*a+c*b
        p_after=abs(psi)**2
        after_i=float(np.dot(bits[i],p_after)); after_j=float(np.dot(bits[j],p_after))
        v=before_i-after_i; cum[(i,j)]+=v; event+=abs(v)
        max_gate_err=max(max_gate_err,abs(after_i-before_i+v),abs(after_j-before_j-v),abs(after_i+after_j-before_i-before_j))
        gate_records.append((depth,edge_index,i,j,v))
    psi*=phase; rows.append(checkpoint(depth))

env={
 "max_gate_event_absolute_traffic":max(r["gate_event_absolute_traffic"] for r in rows),
 "max_cumulative_net_edge_throughput":max(r["cumulative_net_edge_throughput"] for r in rows),
 "max_cumulative_net_inter_ring_throughput":max(r["cumulative_net_inter_ring_throughput"] for r in rows),
 "max_abs_connected_edge_correlation":max(r["max_abs_connected_edge_correlation"] for r in rows),
 "max_record_ledger_residual_l1_per_cluster":max(r["record_ledger_residual_l1_per_cluster"] for r in rows),
 "max_record_ledger_residual_linf_per_cluster":max(r["record_ledger_residual_linf_per_cluster"] for r in rows),
 "max_abs_L8_retained_change":max(abs(r["L8_expected_retained"]-128) for r in rows),
 "max_norm_error":max(r["norm_error"] for r in rows),
 "max_number_law_change":max(r["number_law_max_change"] for r in rows)}
check(len(rows)==9 and len(gate_records)==192,"depth and owner census")
check(max_gate_err<1e-13,"gate endpoint signs")
check(all(r["active_cumulative_edge_count"]==24 for r in rows[1:]),"24 active cumulative supports")
check(all(r["active_cumulative_inter_ring_edge_count"]==8 for r in rows[1:]),"8 active rungs")
check(all(b["gate_event_absolute_traffic"]>a["gate_event_absolute_traffic"] for a,b in zip(rows,rows[1:])),"event traffic strict monotonicity")
check(all(r["gate_event_absolute_traffic"]+1e-14>=r["cumulative_net_edge_throughput"] for r in rows),"event dominates net")
check(rows[3]["cumulative_net_ring_throughput"]<rows[2]["cumulative_net_ring_throughput"],"observed net component cancellation")
check(5e-13<env["max_abs_L8_retained_change"]<1e-12,"documented tolerance repair numerics")
check(env["max_record_ledger_residual_l1_per_cluster"]<8e-14 and env["max_record_ledger_residual_linf_per_cluster"]<9e-15,"raw residual envelope")
check(env["max_norm_error"]<5e-14 and env["max_number_law_change"]<5e-14,"raw controls")
out={"schema":"AUDIT_R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY_V001","disposition":"PASS_CONTROLLED_NUMERICAL_DEPTH_TRAJECTORY",
 "checks":checks,"clusters":16,"heads":256,"supports":24,"gate_records":192,"trajectory":rows,"envelope":env,
 "max_gate_ledger_error":max_gate_err,"attachment":"INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED",
 "read":"COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM","coordinate_status":"FINITE_ENUMERATION__NOT_PHYSICAL_GRID",
 "scope":"MICROSCOPIC_PREPARED_DEPTH_FAMILY","grid_defect_continuum_critical_Ward_gravity":"NOT_PROMOTED"}
(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(f"PASS_CONTROLLED_NUMERICAL_DEPTH_TRAJECTORY__{checks}/{checks}")
