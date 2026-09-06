#!/usr/bin/env python3
"""Independent physical-parent algebra and autonomous-ring reconstruction."""
import json,math,os
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1");os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
checks=0
def ck(v,s):
 global checks
 if not v:raise AssertionError(s)
 checks+=1
# |BB>,|Bx>,|xB>,|xx>: write tail, then native pi/2 transfer.
write=np.array([1,0,-1j,0],complex)/math.sqrt(2); transfer=np.eye(4,dtype=complex);transfer[1,1]=transfer[2,2]=0;transfer[1,2]=transfer[2,1]=1j; final=np.einsum("ij,j->i",transfer,write,optimize=False);expected=np.array([1,1,0,0],complex)/math.sqrt(2);prep_err=float(np.max(abs(final-expected)));ck(prep_err<3e-16,"pulse cancellation")
def run(L):
 dim=1<<L; basis=np.arange(dim); bits=np.array([((basis>>i)&1).astype(float) for i in range(L)]); H=np.zeros((dim,dim))
 for i in range(L):
  j=(i+1)%L
  for m in basis:
   if ((m>>i)&1)!=((m>>j)&1):H[m^(1<<i)^(1<<j),m]+=-1
 Q=np.diag(np.sum(bits,axis=0));comm=np.einsum("ij,jk->ik",H,Q,optimize=False)-np.einsum("ij,jk->ik",Q,H,optimize=False);ck(np.max(abs(comm))==0,"uniform Q commutator")
 psi0=np.zeros(dim,complex);psi0[[m for m in basis if all(((m>>i)&1)==0 for i in range(0,L,2))]]=1/math.sqrt(1<<(L//2));ev,V=np.linalg.eigh(H);coef=np.einsum("ia,i->a",V.conj(),psi0,optimize=False);tau=math.pi/2;psi=np.einsum("ia,a->i",V,np.exp(-1j*ev*tau)*coef,optimize=False);p0=abs(psi0)**2;p=abs(psi)**2;q0=np.einsum("im,m->i",bits,p0,optimize=False);q1=np.einsum("im,m->i",bits,p,optimize=False)
 de=ev[:,None]-ev[None,:];fac=np.empty_like(de,dtype=complex);near=abs(de)<1e-12;fac[near]=tau;fac[~near]=(np.exp(1j*de[~near]*tau)-1)/(1j*de[~near]);curr=[]
 for i in range(L):
  j=(i+1)%L;J=np.zeros((dim,dim),complex)
  for m in basis:
   if ((m>>i)&1)==1 and ((m>>j)&1)==0:s=m^(1<<i)^(1<<j);J[s,m]+=1j;J[m,s]+=-1j
  Je=np.einsum("ia,ij,jb->ab",V.conj(),J,V,optimize=False);curr.append(float(np.sum(coef.conj()[:,None]*coef[None,:]*Je*fac).real))
 curr=np.array(curr);res=q1-q0+curr-np.roll(curr,1);num=np.sum(bits,axis=0).astype(int);law0=np.array([p0[num==k].sum() for k in range(L+1)]);law1=np.array([p[num==k].sum() for k in range(L+1)]);corr=np.array([(p*bits[i]*bits[(i+1)%L]).sum()-q1[i]*q1[(i+1)%L] for i in range(L)]);cycles=L*L;h0=np.einsum("ij,j->i",H,psi0,optimize=False);h1=np.einsum("ij,j->i",H,psi,optimize=False)
 return {"L":L,"cycles_in_VL":cycles,"sites_per_cycle":L,"hilbert_dimension_per_cycle":dim,"prepared_heads_per_cycle":L//2,"prepared_source_lineages":L**3//2,"expected_retained_before_per_cycle":float(q0.sum()),"expected_retained_after_per_cycle":float(q1.sum()),"expected_retained_before_total":float(cycles*q0.sum()),"expected_retained_after_total":float(cycles*q1.sum()),"q_before":q0.tolist(),"q_after":q1.tolist(),"integrated_oriented_currents":curr.tolist(),"active_current_supports_per_cycle":int(np.sum(abs(curr)>1e-12)),"absolute_oriented_throughput_per_cycle":float(abs(curr).sum()),"absolute_oriented_throughput_total":float(cycles*abs(curr).sum()),"record_ledger_residual_l1_per_cycle":float(abs(res).sum()),"record_ledger_residual_linf_per_cycle":float(abs(res).max()),"record_ledger_residual_l1_tiled_bound":float(cycles*abs(res).sum()),"max_abs_connected_edge_correlation":float(np.max(abs(corr))),"norm_error":float(abs(np.vdot(psi,psi).real-1)),"energy_error":float(abs(np.vdot(psi,h1).real-np.vdot(psi0,h0).real)),"number_law_max_change":float(np.max(abs(law1-law0))),"uniform_onsite_commutator_linf":float(np.max(abs(comm)))}
rows=[run(4),run(8)];a,b=rows;ck([x["cycles_in_VL"] for x in rows]==[16,64] and [x["prepared_source_lineages"] for x in rows]==[32,256],"census");ck(all(x["active_current_supports_per_cycle"]==x["L"] for x in rows),"all supports active");ck(all(all(np.sign(x["integrated_oriented_currents"][i])==-np.sign(x["integrated_oriented_currents"][(i+1)%x["L"]]) for i in range(x["L"])) for x in rows),"alternating currents");ck(max(x["record_ledger_residual_l1_per_cycle"] for x in rows)<3e-14,"ledger");ck(max(x["norm_error"] for x in rows)<3e-14 and max(x["energy_error"] for x in rows)<3e-13 and max(x["number_law_max_change"] for x in rows)<3e-14,"controls")
rat={"expected_retained_total":b["expected_retained_after_total"]/a["expected_retained_after_total"],"absolute_oriented_throughput_total":b["absolute_oriented_throughput_total"]/a["absolute_oriented_throughput_total"],"throughput_per_retained_record":(b["absolute_oriented_throughput_total"]/b["expected_retained_after_total"])/(a["absolute_oriented_throughput_total"]/a["expected_retained_after_total"])}
out={"schema":"AUDIT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001","disposition":"PASS_AFTER_REQUIRED_LEDGER_RECLASSIFICATION","checks":checks,"source_preparation_vector_error":prep_err,"rows":rows,"raw_L8_over_L4":rat,"literal_BS09":"H=EPSILON_PSI_Q-T_SUM_N_E_T_E__FIXED_H_SELECTS_EXP_MINUS_I_H_TAU__NO_FINITE_GATE_ORDER","uniform_Q":"COMMUTES_WITH_H_OCCUPATIONS_CURRENTS_AND_NUMBER_CONSERVING_READ","attachment":"INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED","terminal_instrument":"COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM","conditional":"SUPPORT_PROGRAM__T__TAU__CONTENT__READ","open":"AUTONOMOUS_SUPPORT_AND_PHASE_SELECTION","scope":"NO_GRID_DEFECT_CONTINUUM_WARD_GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(f"PASS_AUTONOMOUS_RING_INDEPENDENT__{checks}/{checks}")
