#!/usr/bin/env python3
import json,math,os
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1"); os.environ.setdefault("OPENBLAS_NUM_THREADS","1"); os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
checks=0
def ck(v,s):
 global checks
 if not v: raise AssertionError(s)
 checks+=1
def run(L):
 n=2*L; dim=1<<n; basis=np.arange(dim,dtype=np.uint32); bits=np.array([((basis>>i)&1).astype(float) for i in range(n)]); rings=tuple((r+i,r+(i+1)%L) for r in (0,L) for i in range(L)); rungs=tuple((i,i+L) for i in range(L)); edges=rings+rungs
 ck(len(edges)==len(set(edges))==3*L,"supports"); clusters=L*L//4; heads=L**3//2; ck(clusters*2*L==heads,"partition")
 theta=math.pi/8; c,s=math.cos(theta),1j*math.sin(theta); stagger=sum((1 if i%2==0 else -1)*(1 if i<L else -1)*bits[i] for i in range(n)); phase=np.exp(-.5j*theta*stagger); number=np.sum(bits,axis=0).astype(int); law0=np.array([math.comb(n,k)/dim for k in range(n+1)])
 occ=lambda st:np.einsum("im,m->i",bits,abs(st)**2,optimize=False); state=np.ones(dim,complex)/math.sqrt(dim); q0=occ(state); cum={e:0. for e in edges}; traffic=0.; maxge=0.; events=0
 for _ in range(3):
  state*=phase
  for i,j in edges:
   p=abs(state)**2; bi=float(np.dot(bits[i],p)); bj=float(np.dot(bits[j],p)); idx=basis[(bits[i]==1)&(bits[j]==0)]; swp=idx^(1<<i)^(1<<j); a,b=state[idx].copy(),state[swp].copy(); state[idx]=c*a+s*b; state[swp]=s*a+c*b; p=abs(state)**2; ai=float(np.dot(bits[i],p)); aj=float(np.dot(bits[j],p)); v=bi-ai; cum[(i,j)]+=v; traffic+=abs(v); events+=1; maxge=max(maxge,abs(aj-bj-v),abs(ai+aj-bi-bj))
  state*=phase
 p=abs(state)**2;q=occ(state);div=np.zeros(n)
 for (i,j),v in cum.items():div[i]+=v;div[j]-=v
 res=q-q0+div; vals=np.array([cum[e] for e in edges]); rv=np.array([cum[e] for e in rungs]); law=np.array([p[number==k].sum() for k in range(n+1)]); corr=np.array([np.sum(p*bits[i]*bits[j])-q[i]*q[j] for i,j in edges]); retained=float(q.sum()); net=float(abs(vals).sum()); rung=float(abs(rv).sum())
 return {"L":L,"cells":L**3,"prepared_source_lineages":heads,"retained_heads":heads,"sites_per_connected_component":n,"hilbert_dimension_per_component":dim,"connected_components":clusters,"owned_supports_per_component_per_depth":len(edges),"owner_once_gate_events_per_component":events,"active_cumulative_supports_per_component":int(np.sum(abs(vals)>1e-12)),"active_cumulative_inter_cycle_supports_per_component":int(np.sum(abs(rv)>1e-12)),"expected_retained_per_component":retained,"expected_retained_total":clusters*retained,"gate_event_absolute_traffic_per_component":traffic,"gate_event_absolute_traffic_total":clusters*traffic,"gate_event_absolute_traffic_per_retained_head":clusters*traffic/heads,"cumulative_net_edge_throughput_per_component":net,"cumulative_net_edge_throughput_total":clusters*net,"cumulative_net_edge_throughput_per_retained_head":clusters*net/heads,"cumulative_net_inter_cycle_throughput_per_component":rung,"cumulative_net_inter_cycle_throughput_total":clusters*rung,"cumulative_net_inter_cycle_throughput_per_retained_head":clusters*rung/heads,"max_abs_connected_edge_correlation":float(np.max(abs(corr))),"record_ledger_residual_l1_per_component":float(abs(res).sum()),"record_ledger_residual_linf_per_component":float(abs(res).max()),"record_ledger_residual_l1_tiled_bound":float(clusters*abs(res).sum()),"norm_error":float(abs(np.vdot(state,state).real-1)),"number_law_max_change":float(np.max(abs(law-law0))),"max_gate_ledger_error":maxge}
rows=[run(4),run(8)]; a,b=rows
ck((a["connected_components"],a["retained_heads"],b["connected_components"],b["retained_heads"])==(4,32,16,256),"counts");ck(all(x["active_cumulative_supports_per_component"]==3*x["L"] and x["active_cumulative_inter_cycle_supports_per_component"]==x["L"] for x in rows),"activity");ck((a["owner_once_gate_events_per_component"],b["owner_once_gate_events_per_component"])==(36,72),"events");ck(max(x["max_gate_ledger_error"] for x in rows)<1e-13,"signs")
total_fields=("cells","prepared_source_lineages","retained_heads","connected_components","expected_retained_total","gate_event_absolute_traffic_total","cumulative_net_edge_throughput_total","cumulative_net_inter_cycle_throughput_total"); ratios={k:b[k]/a[k] for k in total_fields}; ph=("gate_event_absolute_traffic_per_retained_head","cumulative_net_edge_throughput_per_retained_head","cumulative_net_inter_cycle_throughput_per_retained_head"); phr={k:b[k]/a[k] for k in ph}
ck(all(x["max_abs_connected_edge_correlation"]>1e-3 for x in rows),"correlation");ck(max(x["record_ledger_residual_l1_per_component"] for x in rows)<5e-14 and max(x["record_ledger_residual_linf_per_component"] for x in rows)<7e-15,"ledger");ck(max(x["norm_error"] for x in rows)<3e-14 and max(x["number_law_max_change"] for x in rows)<3e-15,"controls")
out={"schema":"AUDIT_R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY_V001","disposition":"PASS_CONTROLLED_NUMERICAL_CONNECTED_FINITE_SIZE_TRAJECTORY","checks":checks,"rows":rows,"raw_L8_over_L4_ratios":ratios,"raw_L8_over_L4_per_head_ratios":phr,"selected_recipe":{"preparation_pattern":"reversed","gate_order":"forward","depth":3},"terminal_instrument":"COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM","attachment":"INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED","coordinate_status":"FINITE_ENUMERATION__NOT_PHYSICAL_GRID","claim_boundary":"RAW_RATIOS_ONLY__NO_FORCED_FACTOR_8_EXPONENT_LIMIT_OR_GENERIC_LAW__NO_DEFECT_CONTINUUM_CRITICAL_WARD_GRAVITY"}
(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(f"PASS_CONNECTED_FINITE_SIZE__{checks}/{checks}")
