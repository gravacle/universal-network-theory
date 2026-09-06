#!/usr/bin/env python3
"""Independent three-order 65536-state reconstruction; no target imports."""
import json,math,os
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1"); os.environ.setdefault("OPENBLAS_NUM_THREADS","1"); os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
checks=0
def check(v,label):
 global checks
 if not v: raise AssertionError(label)
 checks+=1
n=16; dim=1<<n; depth=3; theta=math.pi/8; basis=np.arange(dim,dtype=np.uint32)
bits=np.array([((basis>>i)&1).astype(float) for i in range(n)])
r0=tuple((i,(i+1)%8) for i in range(8)); r1=tuple((8+i,8+(i+1)%8) for i in range(8)); rungs=tuple((i,i+8) for i in range(8)); forward=r0+r1+rungs
orders={"forward":forward,"reverse":tuple(reversed(forward)),"interleaved":tuple(e for i in range(8) for e in (r0[i],r1[i],rungs[i]))}
check(set(orders)=={"forward","reverse","interleaved"},"three orders")
check(all(len(o)==len(set(o))==24 and set(o)==set(forward) for o in orders.values()),"same owner-once support")
check(len({frozenset(e) for e in forward})==24,"unique physical support")
clusters=tuple((x,z) for x in range(8) if x%2 for z in range(8) if z%2==0)
heads={(x,y,z) for x in range(8) if x%2 for y in range(8) for z in range(8)}
covered={(x,y,zz) for x,z in clusters for y in range(8) for zz in (z,z+1)}
check(len(clusters)==16 and covered==heads and len(heads)==256,"V8 partition")
c,s=math.cos(theta),1j*math.sin(theta); stagger=np.zeros(dim)
for i in range(n): stagger+=(1 if i%2==0 else -1)*(1 if i<8 else -1)*bits[i]
phase=np.exp(-.5j*theta*stagger); number=np.sum(bits,axis=0).astype(int); law0=np.array([math.comb(n,k)/dim for k in range(n+1)])
def occ(state): return np.einsum("im,m->i",bits,abs(state)**2,optimize=False)
def run(name,order):
 state=np.ones(dim,complex)/math.sqrt(dim); q0=occ(state); cum={e:0.0 for e in forward}; traffic=0.; max_gate_err=0.; events=0
 for _ in range(depth):
  state*=phase
  for i,j in order:
   pb=abs(state)**2; bi=float(np.dot(bits[i],pb)); bj=float(np.dot(bits[j],pb)); idx=basis[(bits[i]==1)&(bits[j]==0)]; swp=idx^(1<<i)^(1<<j)
   a,b=state[idx].copy(),state[swp].copy(); state[idx]=c*a+s*b; state[swp]=s*a+c*b
   pa=abs(state)**2; ai=float(np.dot(bits[i],pa)); aj=float(np.dot(bits[j],pa)); v=bi-ai
   max_gate_err=max(max_gate_err,abs(ai-bi+v),abs(aj-bj-v),abs(ai+aj-bi-bj)); cum[(i,j)]+=v; traffic+=abs(v); events+=1
  state*=phase
 p=abs(state)**2; q=occ(state); div=np.zeros(n)
 for (i,j),v in cum.items(): div[i]+=v; div[j]-=v
 res=q-q0+div; law=np.array([p[number==k].sum() for k in range(n+1)]); currents=np.array([cum[e] for e in forward]); rv=np.array([cum[e] for e in rungs])
 corr=np.array([np.sum(p*bits[i]*bits[j])-q[i]*q[j] for i,j in forward])
 rec={"order":name,"edge_sequence":[list(e) for e in order],"expected_retained_per_cluster":float(q.sum()),"L8_expected_retained":float(16*q.sum()),"q_final":q.tolist(),"first_ring_expected_retained":float(q[:8].sum()),"second_ring_expected_retained":float(q[8:].sum()),"gate_event_absolute_traffic":float(traffic),"cumulative_net_edge_throughput":float(abs(currents).sum()),"cumulative_net_inter_ring_throughput":float(abs(rv).sum()),"active_cumulative_edge_count":int(np.sum(abs(currents)>1e-12)),"active_cumulative_inter_ring_edge_count":int(np.sum(abs(rv)>1e-12)),"max_abs_connected_edge_correlation":float(np.max(abs(corr))),"record_ledger_residual_l1_per_cluster":float(abs(res).sum()),"record_ledger_residual_linf_per_cluster":float(abs(res).max()),"norm_error":float(abs(np.vdot(state,state).real-1)),"number_law_max_change":float(np.max(abs(law-law0))),"gate_events":events,"max_gate_ledger_error":max_gate_err}
 return state,p,rec
runs={name:run(name,o) for name,o in orders.items()}; records=[runs[x][2] for x in orders]
check(all(r["gate_events"]==72 for r in records),"72 events each")
check(all(r["active_cumulative_edge_count"]==24 for r in records),"all supports active")
check(all(r["active_cumulative_inter_ring_edge_count"]==8 for r in records),"all rungs active")
check(max(r["max_gate_ledger_error"] for r in records)<1e-13,"gate signs")
pairs=[]
names=tuple(orders)
for ai in range(3):
 for bi in range(ai+1,3):
  a,b=names[ai],names[bi]; sa,pa,_=runs[a]; sb,pb,_=runs[b]
  pairs.append({"first":a,"second":b,"terminal_distribution_total_variation":float(.5*abs(pa-pb).sum()),"state_fidelity":float(abs(np.vdot(sa,sb))**2),"occupation_l1_distance":float(abs(np.array(runs[a][2]["q_final"])-np.array(runs[b][2]["q_final"])).sum())})
env={"max_terminal_distribution_total_variation":max(x["terminal_distribution_total_variation"] for x in pairs),"min_state_fidelity":min(x["state_fidelity"] for x in pairs),"max_occupation_l1_distance":max(x["occupation_l1_distance"] for x in pairs),"max_record_ledger_residual_l1_per_cluster":max(x["record_ledger_residual_l1_per_cluster"] for x in records),"max_record_ledger_residual_linf_per_cluster":max(x["record_ledger_residual_linf_per_cluster"] for x in records),"max_abs_L8_retained_change":max(abs(x["L8_expected_retained"]-128) for x in records),"max_norm_error":max(x["norm_error"] for x in records),"max_number_law_change":max(x["number_law_max_change"] for x in records)}
check(len(pairs)==3 and min(x["terminal_distribution_total_variation"] for x in pairs)>1e-3,"full distribution differs")
check(env["min_state_fidelity"]<.999 and min(x["occupation_l1_distance"] for x in pairs)>1e-3,"state and occupations differ")
check(env["max_record_ledger_residual_l1_per_cluster"]<5e-14 and env["max_record_ledger_residual_linf_per_cluster"]<7e-15,"ledger controls")
check(env["max_abs_L8_retained_change"]<5e-13 and env["max_norm_error"]<2e-14 and env["max_number_law_change"]<3e-15,"retention norm number")
out={"schema":"AUDIT_R_CONNECTED_L8_CIRCUIT_ORDER_SCREEN_V001","disposition":"PASS_CONTROLLED_NUMERICAL_ORDER_SCREEN","checks":checks,"clusters":16,"heads":256,"unique_supports":24,"rungs":8,"events_per_order":72,"total_events":216,"orders":records,"pairwise_order_comparisons":pairs,"envelope":env,"terminal_instrument":"COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM","attachment":"INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED","coordinate_status":"FINITE_ENUMERATION__NOT_PHYSICAL_GRID","conclusion":"SCHEDULE_NECESSARY_SELECTED_PARENT_DATA__NO_PREFERRED_ORDER_OR_AVERAGING_SELECTION_LAW","defect_continuum_critical_Ward_gravity":"NOT_PROMOTED"}
(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(f"PASS_CONTROLLED_NUMERICAL_ORDER_SCREEN__{checks}/{checks}")
