#!/usr/bin/env python3
"""Frozen-protocol target for the L4+L4 -> L8 coherent closure screen."""
import hashlib,json,math,os
from pathlib import Path
os.environ.setdefault("OPENBLAS_NUM_THREADS","1");os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
HERE=Path(__file__).resolve().parent; PROTOCOL=HERE/"PROTOCOL.md"; OUT=HERE/"RESULT.json"
assert hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()=="e0245dc81edb15be8b5ece72ff196f19754976a41a5785941e3dba2428bdcbb4"
K=math.pi/2
def edges(L):return [(a*L+i,a*L+(i+1)%L) for a in range(2) for i in range(L)]+[(i,L+(i+1)%L) for i in range(L)]
def source(L):
 D=1<<(2*L);x=np.zeros(D,complex);even=sum(1<<i for i in range(0,2*L,2));w=np.arange(D);ok=(w&even)==0;x[ok]=1/math.sqrt(1<<L);return x
def apply(x,E):
 y=np.zeros_like(x);w=np.arange(x.size)
 for u,v in E:
  m=((w>>u)&1)!=((w>>v)&1);a=w[m];y[a^(1<<u)^(1<<v)]-=x[a]
 return y
def currents(x,E):
 w=np.arange(x.size);z=[]
 for u,v in E:
  m=((w>>u)&1)!=((w>>v)&1);a=w[m];b=a^(1<<u)^(1<<v);sg=((a>>v)&1)-((a>>u)&1);z.append(np.sum(np.conjugate(x[b])*(-1j*sg)*x[a]).real)
 return np.array(z)
def evolve(L,n,order=10):
 E=edges(L);x=source(L);integ=currents(x,E);dt=K/n
 for j in range(1,n+1):
  out=x.copy();term=x.copy()
  for k in range(1,order+1):term=(-1j*dt/k)*apply(term,E);out+=term
  x=out;integ+=(1 if j==n else 4 if j%2 else 2)*currents(x,E)
 return x,integ*dt/3
def matrix_cut(x,L):
 if L==4:A=[0,1,4,5];B=[2,3,6,7]
 else:A=[0,1,2,3,8,9,10,11];B=[4,5,6,7,12,13,14,15]
 M=np.zeros((1<<len(A),1<<len(B)),complex)
 for w,a in enumerate(x):
  i=sum(((w>>s)&1)<<k for k,s in enumerate(A));j=sum(((w>>s)&1)<<k for k,s in enumerate(B));M[i,j]=a
 return M
def diag(x,L,E,J):
 p=abs(x)**2;w=np.arange(x.size);q=np.array([np.sum(p*((w>>i)&1)) for i in range(2*L)]);q0=np.array([0 if i%2==0 else .5 for i in range(2*L)]);bal=np.zeros(2*L)
 for j,(u,v) in enumerate(E):bal[u]+=J[j];bal[v]-=J[j]
 corr=np.array([np.sum(p*((w>>u)&1)*((w>>v)&1))-q[u]*q[v] for u,v in E]);return q,q-q0+bal,corr
rows=[]
for L in (4,8):
 xc,Jc=evolve(L,512 if L==8 else 256);xf,J=evolve(L,1024 if L==8 else 512);xi,_=evolve(L,768 if L==8 else 384,12);E=edges(L);q,res,corr=diag(xf,L,E,J);mat=matrix_cut(xf,L);U,sv,Vh=np.linalg.svd(mat,full_matrices=False);svc=np.linalg.svd(matrix_cut(xc,L),compute_uv=False);svi=np.linalg.svd(matrix_cut(xi,L),compute_uv=False);err=max(np.max(abs(xf-xc)),np.max(abs(xf-xi)));tol=max(1e-11,100*err);ranks=[int(np.sum(s>tol)) for s in (sv,svc,svi)];rank=ranks[0];tails={str(d):float(np.sqrt(np.sum(sv[d:]**2))) for d in sorted(set([0,1,2,4,8,16,rank-1])) if 0<=d<rank};recon=np.zeros_like(mat)
 for k in range(len(sv)):recon+=sv[k]*np.outer(U[:,k],Vh[k,:])
 rows.append({"L":L,"full_state_dimension":1<<(2*L),"boundary_state_dimension_each_side":1<<L,"coefficient_matrix_shape":list(mat.shape),"schmidt_rank":rank,"rank_threshold":tol,"rank_by_fine_coarse_independent":ranks,"smallest_retained_singular_value":float(sv[rank-1]),"largest_excluded_singular_value":float(sv[rank]) if rank<len(sv) else 0.0,"retained_to_excluded_gap":float(sv[rank-1]/sv[rank]) if rank<len(sv) and sv[rank]>0 else None,"svd_reconstruction_linf":float(np.max(abs(mat-recon))),"tail_l2_checkpoints":tails,"solver_linf":err,"source_factorization_error":0.0,"q_after":q.tolist(),"currents":J.tolist(),"max_abs_connected_edge_correlation":float(max(abs(corr))),"retained":float(sum(q)),"ledger_l1":float(sum(abs(res))),"ledger_linf":float(max(abs(res))),"norm_error":float(abs(np.vdot(xf,xf).real-1))})
EA={tuple(sorted((u if u<4 else u+4,v if v<4 else v+4))) for u,v in edges(4)}
EB={tuple(sorted((u+4 if u<4 else u+8,v+4 if v<4 else v+8))) for u,v in edges(4)}
isolated=EA|EB
removed={(0,3),(8,11),(3,8),(4,7),(12,15),(7,12)};added={(3,4),(0,7),(11,12),(8,15),(3,12),(7,8)};composed=(isolated-removed)|added;canonical=set(tuple(sorted(e)) for e in edges(8))
lower=ROOT=HERE.parent/"ADVERSARIAL_R_GATE_C_L4_L4_TO_L8_BOUNDARY_RECORD_V001"/"RESULT.json";lower_hash=hashlib.sha256(lower.read_bytes()).hexdigest();assert lower_hash=="fd0347a57dc10aaaa03c91f661b5715db1db57e86e48ed161144110c9e4fe924"
out={"schema":"R_GATE_C_L4_L4_TO_L8_COMPOSITION_CLOSURE_V001","protocol_sha256":hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),"owner_surgery_exact":composed==canonical and len(composed)==24,"removed_owners":sorted(map(list,removed)),"added_owners":sorted(map(list,added)),"rows":rows,"target_threshold_rank_estimates":{"D4":16,"D8":254},"hostile_common_robust_D8_lower_bound":251,"exact_D8_interval_pending_hostile_resolution":[251,256],"exact_reconstruction_dimension_D8":256,"certified_ratio_lower_bound":251/16,"target_estimate_ratio":254/16,"fractional_lower_bound_L8":251/256,"lower_order_adversarial_result_sha256":lower_hash,"lower_order_attack_status":"PINNED_PASS_EQUAL_TIME_RECORD_NOT_CLOSED","stop_rule":"STOP_EXPONENTIAL_LOWER_BOUND__EXACT_D8_UNRESOLVED","classification":"CANDIDATE_CONDITIONAL_FINITE_COHERENT_INTERFACE_OBSTRUCTION__PENDING_HOSTILE_AUDIT","claim_classes":{"proved":"OWNER_SURGERY__SVD_MINIMALITY_IDENTITY__SOURCE_FACTORIZATION__LOWER_ORDER_COUNTEREXAMPLE_BY_PIN","adopted":"F3_MDC_ALPHA_R0__CONDITIONAL_INTERSCALE_JOIN","conditional":"SUPPORT__SOURCE_ROUTING__KAPPA__CLOCK__READ","numerical":"EVOLVED_STATES__SCHMIDT_SPECTRA_AND_THRESHOLD_RANKS__CURRENTS__CORRELATIONS__RESIDUALS","open":"EXACT_D8_RANK_WITHIN_251_TO_256__HOSTILE_AUDIT"},"not_claimed":"TRUNCATION__SCALING_LAW__GRID__CONTINUUM__WARD__PHASE__GRAVITON__GRAVITY"}
if OUT.exists():
 old=json.loads(OUT.read_text());assert old==out
else:OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print("PASS__CANDIDATE_COMPOSITION_CLOSURE_TARGET")
