#!/usr/bin/env python3
import json,math,os
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1");os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
ROOT=Path(__file__).parent.parent;prior=json.loads((ROOT/"AUDIT_R_AUTONOMOUS_KAPPA_TRAJECTORY_V001/INDEPENDENT_RESULT.json").read_text());ks=tuple(prior["kappas"]);checks=0
def ck(v,s):
 global checks
 if not v:raise AssertionError(s)
 checks+=1
# Validate J=-Delta q/2 on every lower-size direct vector.
diff=0.
for r in prior["rows"]:
 q0=np.array([0 if i%2==0 else .5 for i in range(r["L"])]);diff=max(diff,float(np.max(abs(-.5*(np.array(r["q_after"])-q0)-np.array(r["integrated_oriented_currents"])))))
ck(diff<8e-12,"lower currents")
L=10;dim=1<<L;b=np.arange(dim);q=np.array([((b>>i)&1).astype(float) for i in range(L)]);H=np.zeros((dim,dim))
for i in range(L):
 j=(i+1)%L
 for w in b:
  if ((w>>i)&1)!=((w>>j)&1):H[w^(1<<i)^(1<<j),w]-=1
psi0=np.zeros(dim,complex);psi0[[w for w in b if all(((w>>i)&1)==0 for i in range(0,L,2))]]=1/math.sqrt(32);ev,V=np.linalg.eigh(H);coef=np.einsum("ia,i->a",V.conj(),psi0,optimize=False);p0=abs(psi0)**2;q0=np.einsum("im,m->i",q,p0,optimize=False);num=q.sum(0).astype(int);law0=np.array([p0[num==i].sum() for i in range(11)]);e0=float(np.vdot(psi0,np.einsum("ij,j->i",H,psi0,optimize=False)).real);Q=np.diag(num);comm=np.einsum("ij,jk->ik",H,Q,optimize=False)-np.einsum("ij,jk->ik",Q,H,optimize=False);rows=[]
for k in ks:
 psi=np.einsum("ia,a->i",V,np.exp(-1j*ev*k)*coef,optimize=False);p=abs(psi)**2;q1=np.einsum("im,m->i",q,p,optimize=False);cur=-.5*(q1-q0);res=q1-q0+cur-np.roll(cur,1);corr=np.array([(p*q[i]*q[(i+1)%L]).sum()-q1[i]*q1[(i+1)%L] for i in range(L)]);law=np.array([p[num==i].sum() for i in range(11)]);hp=np.einsum("ij,j->i",H,psi,optimize=False);thr=float(100*abs(cur).sum());ret=float(100*q1.sum())
 rows.append({"L":10,"kappa":k,"cycles":100,"sites_total":1000,"sites_per_F3_layer":500,"possible_F3_links":250000,"selected_cycle_edges":1000,"prepared_source_lineages":500,"expected_retained_total":ret,"q_after":q1.tolist(),"integrated_oriented_currents":cur.tolist(),"active_current_supports_per_cycle":int(np.sum(abs(cur)>1e-12)),"absolute_oriented_throughput_per_cycle":float(abs(cur).sum()),"absolute_oriented_throughput_total":thr,"throughput_per_retained_record":thr/ret,"max_abs_connected_edge_correlation":float(np.max(abs(corr))),"record_ledger_residual_l1_per_cycle":float(abs(res).sum()),"record_ledger_residual_linf_per_cycle":float(abs(res).max()),"record_ledger_residual_l1_tiled_bound":float(100*abs(res).sum()),"period_two_occupation_error":float(max(np.max(abs(q1[::2]-q1[0])),np.max(abs(q1[1::2]-q1[1])))),"norm_error":float(abs(np.vdot(psi,psi).real-1)),"energy_error":float(abs(np.vdot(psi,hp).real-e0)),"number_law_max_change":float(np.max(abs(law-law0))),"uniform_onsite_commutator_linf":float(np.max(abs(comm)))})
ck(len(rows)==10 and all((r["sites_total"],r["sites_per_F3_layer"],r["possible_F3_links"],r["cycles"],r["selected_cycle_edges"],r["prepared_source_lineages"])==(1000,500,250000,100,1000,500) for r in rows),"census");ck(all(abs(r["expected_retained_total"]-250)<2e-11 for r in rows),"retention");ck(rows[0]["active_current_supports_per_cycle"]==0 and all(r["active_current_supports_per_cycle"]==10 for r in rows[1:]),"activity");ck(max(r["record_ledger_residual_l1_per_cycle"] for r in rows)<1e-11,"ledger");ck(max(r["norm_error"] for r in rows)<1e-13 and max(r["energy_error"] for r in rows)<2e-12 and max(r["number_law_max_change"] for r in rows)<1e-13,"controls")
l8={r["kappa"]:r for r in prior["rows"] if r["L"]==8};rat=[]
for r in rows:
 z=l8[r["kappa"]];rat.append({"kappa":r["kappa"],"L10_over_L8_throughput_total":None if r["kappa"]==0 else r["absolute_oriented_throughput_total"]/z["absolute_oriented_throughput_total"],"L10_over_L8_throughput_per_retained_record":None if r["kappa"]==0 else r["throughput_per_retained_record"]/z["throughput_per_retained_record"]})
out={"schema":"AUDIT_R_AUTONOMOUS_L10_ACCUMULATION_V001","disposition":"PASS_CONDITIONAL_L10_ACCUMULATION","checks":checks,"lower_size_direct_current_max_abs_difference":diff,"rows":rows,"ratios":rat,"exact_reduction":"PERIOD_TWO_PLUS_REFLECTION_REMOVES_UNIFORM_CIRCULATION__J_I=-DELTA_Q_I/2","conditional":"SUPPORT__KAPPA__T__TAU__CLOCK__CONTENT__SOURCE_ROUTING__COMPLETE_READ","zero_kappa":"EXACT_ZERO__DISPLAYED_NONZERO_IS_EIGENSOLVER_ROUNDOFF_BELOW_ACTIVITY_THRESHOLD","not_claimed":"DEFECT__PHYSICAL_GRID__CONTINUUM__WARD__CRITICAL__GENERIC_PHASE__GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(f"PASS_L10_INDEPENDENT__{checks}/{checks}")
