#!/usr/bin/env python3
import json,math,os
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1");os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
ks=(0.,math.pi/16,math.pi/8,math.pi/4,3*math.pi/8,math.pi/2,3*math.pi/4,math.pi,3*math.pi/2,2*math.pi);rows=[];checks=0
def ck(v,s):
 global checks
 if not v:raise AssertionError(s)
 checks+=1
for L in (4,6,8):
 dim=1<<L;b=np.arange(dim);q=np.array([((b>>i)&1).astype(float) for i in range(L)]);H=np.zeros((dim,dim));Js=[]
 for i in range(L):
  j=(i+1)%L;J=np.zeros((dim,dim),complex)
  for w in b:
   if ((w>>i)&1)!=((w>>j)&1):H[w^(1<<i)^(1<<j),w]-=1
   if ((w>>i)&1)==1 and ((w>>j)&1)==0:s=w^(1<<i)^(1<<j);J[s,w]+=1j;J[w,s]-=1j
  Js.append(J)
 Q=np.diag(q.sum(0));comm=np.einsum("ij,jk->ik",H,Q,optimize=False)-np.einsum("ij,jk->ik",Q,H,optimize=False);ck(np.max(abs(comm))==0,"Q commutes")
 psi0=np.zeros(dim,complex);psi0[[w for w in b if all(((w>>i)&1)==0 for i in range(0,L,2))]]=1/math.sqrt(1<<(L//2));ev,V=np.linalg.eigh(H);coef=np.einsum("ia,i->a",V.conj(),psi0,optimize=False);Ec=[np.einsum("ia,ij,jb->ab",V.conj(),J,V,optimize=False) for J in Js];de=ev[:,None]-ev[None,:];p0=abs(psi0)**2;q0=np.einsum("im,m->i",q,p0,optimize=False);num=q.sum(0).astype(int);law0=np.array([p0[num==n].sum() for n in range(L+1)]);e0=float(np.vdot(psi0,np.einsum("ij,j->i",H,psi0,optimize=False)).real)
 for k in ks:
  psi=np.einsum("ia,a->i",V,np.exp(-1j*ev*k)*coef,optimize=False);p=abs(psi)**2;q1=np.einsum("im,m->i",q,p,optimize=False);fac=np.empty_like(de,dtype=complex);near=abs(de)<1e-12;fac[near]=k;fac[~near]=(np.exp(1j*de[~near]*k)-1)/(1j*de[~near]);cur=np.array([float(np.sum(coef.conj()[:,None]*coef[None,:]*E*fac).real) for E in Ec]);res=q1-q0+cur-np.roll(cur,1);law=np.array([p[num==n].sum() for n in range(L+1)]);corr=np.array([(p*q[i]*q[(i+1)%L]).sum()-q1[i]*q1[(i+1)%L] for i in range(L)]);cycles=L*L;ret=float(cycles*q1.sum());thr=float(cycles*abs(cur).sum());hp=np.einsum("ij,j->i",H,psi,optimize=False)
  rows.append({"L":L,"kappa":k,"cycles":cycles,"prepared_source_lineages":L**3//2,"expected_retained_total":ret,"active_current_supports_per_cycle":int(np.sum(abs(cur)>1e-12)),"q_after":q1.tolist(),"integrated_oriented_currents":cur.tolist(),"absolute_oriented_throughput_per_cycle":float(abs(cur).sum()),"absolute_oriented_throughput_total":thr,"throughput_per_retained_record":thr/ret,"max_abs_connected_edge_correlation":float(np.max(abs(corr))),"record_ledger_residual_l1_per_cycle":float(abs(res).sum()),"record_ledger_residual_linf_per_cycle":float(abs(res).max()),"record_ledger_residual_l1_tiled_bound":float(cycles*abs(res).sum()),"norm_error":float(abs(np.vdot(psi,psi).real-1)),"energy_error":float(abs(np.vdot(psi,hp).real-e0)),"number_law_max_change":float(np.max(abs(law-law0))),"uniform_onsite_commutator_linf":float(np.max(abs(comm)))})
ck(len(rows)==30,"census");ck(all(abs(r["expected_retained_total"]-r["L"]**3/4)<5e-12 for r in rows),"retention");ck(all(r["active_current_supports_per_cycle"]==0 for r in rows if r["kappa"]==0),"zero");ck(all(r["active_current_supports_per_cycle"]==r["L"] for r in rows if r["kappa"]==math.pi/2),"baseline activity");ck(max(r["record_ledger_residual_l1_per_cycle"] for r in rows)<5e-11,"ledger");ck(max(r["norm_error"] for r in rows)<8e-14 and max(r["energy_error"] for r in rows)<5e-13 and max(r["number_law_max_change"] for r in rows)<8e-14,"controls")
rat=[]
for k in ks:
 a=next(r for r in rows if r["L"]==4 and r["kappa"]==k);z=next(r for r in rows if r["L"]==8 and r["kappa"]==k);rat.append({"kappa":k,"L8_over_L4_throughput_total":None if k==0 else z["absolute_oriented_throughput_total"]/a["absolute_oriented_throughput_total"],"L8_over_L4_throughput_per_retained_record":None if k==0 else z["throughput_per_retained_record"]/a["throughput_per_retained_record"]})
out={"schema":"AUDIT_R_AUTONOMOUS_KAPPA_TRAJECTORY_V001","disposition":"PASS_CONDITIONAL_AUTONOMOUS_KAPPA_MAP","checks":checks,"kappas":list(ks),"rows":rows,"ratios":rat,"uniform_onsite_algebra":"[Q,A]=0_AND_RECORDED_OBSERVABLES_COMMUTE_WITH_Q__UNIFORM_ONSITE_IS_SECTOR_PHASE__KAPPA_ONLY","conditional":"SUPPORT__KAPPA_SAMPLES__SEPARATE_T_TAU_CLOCK__CONTENT__COMPLETE_READ","not_claimed":"FINITE_GATE_ORDER__STAGGER__COEFFICIENT_SELECTION__DEFECT__PHYSICAL_GRID__CONTINUUM__WARD__GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(f"PASS_KAPPA_INDEPENDENT__{checks}/{checks}")
