#!/usr/bin/env python3
import json,os
from itertools import product
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1")
import numpy as np
checks=0
def ck(v,s):
 global checks
 if not v:raise AssertionError(s)
 checks+=1
def components(A):
 m=len(A);g=[[] for _ in range(2*m)]
 for i,j in zip(*np.nonzero(A)):g[i].append(m+j);g[m+j].append(i)
 seen=set();out=[]
 for s in range(2*m):
  if s in seen:continue
  q=[s];seen.add(s);n=0
  while q:
   u=q.pop();n+=1
   for v in g[u]:
    if v not in seen:seen.add(v);q.append(v)
  out.append(n)
 return sorted(out)
rows=[]
for L in (4,8):
 left=[v for v in product(range(L),repeat=3) if v[0]%2==0];right=[v for v in product(range(L),repeat=3) if v[0]%2];li={v:i for i,v in enumerate(left)};ri={v:i for i,v in enumerate(right)};A=np.zeros((len(left),len(right)),dtype=np.int8)
 for x,y,z in left:
  for xp in ((x-1)%L,(x+1)%L):A[li[(x,y,z)],ri[(xp,y,z)]]=1
 M=L**3//2;ck(A.shape==(M,M) and A.sum()==L**3,"census");ck(np.all(A.sum(0)==2)&np.all(A.sum(1)==2),"degree");ck(components(A)==[L]*(L**2),"components")
 a,b=ri[(1,0,0)],ri[(1,0,1)];P=np.eye(M,dtype=np.int8);P[[a,b]]=P[[b,a]];C=np.einsum("ij,kj->ik",A,P,optimize=False);ck(not np.array_equal(A,C) and np.all(C.sum(0)==2) and np.all(C.sum(1)==2),"competitor")
 energy=lambda X:float(X.sum()+np.sum((np.r_[X.sum(1),X.sum(0)]-2)**2));ck(energy(A)==energy(C)==L**3,"degeneracy")
 rows.append({"L":L,"sites_total":L**3,"sites_per_F3_layer":M,"possible_F3_links":M*M,"selected_cycle_edges":int(A.sum()),"selected_cycles":L**2,"selected_degree":2,"BS06_diagonal_energy_at_Delta_eq_Ud_eq_1":energy(A),"explicit_distinct_equal_energy_competitor":True,"component_sizes":components(A)})
for delta,ud in ((.001,1),(1,1),(1.999,1),(3,2)):
 costs=[ud*(d-2)**2+.5*delta*d for d in range(257)];ck(np.argmin(costs)==2 and costs.count(min(costs))==1,"window")
diag=[];words=[]
for w in range(512):
 A=np.array([(w>>e)&1 for e in range(9)]).reshape(3,3);diag.append(A.sum()+np.sum((np.r_[A.sum(1),A.sum(0)]-2)**2))
 if np.all(A.sum(0)==2) and np.all(A.sum(1)==2):words.append(w)
H=np.diag(diag).astype(float)
for w in range(512):
 for e in range(9):H[w,w^(1<<e)]=-.25
ev,V=np.linalg.eigh(H);g=V[:,0];g*=1 if g.sum()>0 else -1;pr=abs(g)**2;small={"possible_edges":9,"hilbert_dimension":512,"classical_ground_energy":float(min(diag)),"classical_ground_multiplicity":diag.count(min(diag)),"degree_two_word_count":len(words),"transverse_h":.25,"transverse_ground_gap":float(ev[1]-ev[0]),"transverse_ground_min_amplitude":float(g.min()),"transverse_ground_probability_spread_on_degree_two_orbit":float(pr[words].max()-pr[words].min()),"transverse_ground_total_probability_outside_one_word":float(1-pr.max())}
ck(small["classical_ground_multiplicity"]==len(words)==6,"K33");ck(small["transverse_ground_gap"]>1e-8 and small["transverse_ground_min_amplitude"]>1e-12,"PF");ck(small["transverse_ground_probability_spread_on_degree_two_orbit"]<2e-11 and small["transverse_ground_total_probability_outside_one_word"]>.5,"orbit")
n=np.diag([0.,1.]);x=np.array([[0.,1.],[1.,0.]]);I=np.eye(2);N=np.kron(n,I);ops={"BS09_with_n_linf":-np.kron(n,x),"BS11_with_n_linf":np.kron(n,n),"BS10_with_n_linf":np.kron(I,x),"BS06_flip_with_n_linf":-np.kron(x,I)};comm={k:float(np.max(abs(np.einsum("ij,jk->ik",v,N,optimize=False)-np.einsum("ij,jk->ik",N,v,optimize=False)))) for k,v in ops.items()};ck(all(comm[k]==0 for k in list(comm)[:3]) and comm["BS06_flip_with_n_linf"]>0,"commutators")
out={"schema":"AUDIT_R_PHYSICAL_PARENT_SUPPORT_SELECTION_SCREEN_V001","disposition":"PASS_EXACT_NON_SELECTION_BOUNDARY","checks":checks,"rows":rows,"degree_two_window":"U_D>0_AND_0<DELTA<2U_D","small_exact_transverse_example":small,"incidence_commutators":comm,"anchoring_boundary":"UNIFORM_SOURCE_INVARIANT__DISTINGUISHING_LINEAGE_OR_PORT_IS_ADDITIONAL_CONDITIONAL_SELECTOR_DATA","scope":"NO_PHYSICAL_GRID_DEFECT_CONTINUUM_WARD_GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(f"PASS_SUPPORT_SELECTION_INDEPENDENT__{checks}/{checks}")
