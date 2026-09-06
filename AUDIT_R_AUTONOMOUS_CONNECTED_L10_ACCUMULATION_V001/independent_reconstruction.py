#!/usr/bin/env python3
"""Generator-BFS/destination-normalized L10 quotient with RK4 evolution."""
import json,math,os
from collections import Counter
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1");os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
from numba import njit
L=10;N=20;D=1<<N;STEPS=4096;K=math.pi/2;ROOT=Path(__file__).parent.parent
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 z=[0]*len(p)
 for i,j in enumerate(p):z[j]=i
 return tuple(z)
def pw(w,p):
 z=0
 for i,j in enumerate(p):
  if (w>>i)&1:z|=1<<j
 return z
@njit
def ha(x,src,dst,val,n):
 y=np.zeros(n,np.complex128)
 for k in range(len(val)):y[dst[k]]+=val[k]*x[src[k]]
 return y
@njit
def jc(x,left,right,f):
 z=0j
 for k in range(len(f)):z+=np.conjugate(x[left[k]])*(1j*f[k])*x[right[k]]
 return z.real
I=tuple(range(N));T=tuple(a*L+(i+2)%L for a in range(2) for i in range(L));S=tuple((1-a)*L+(-i)%L for a in range(2) for i in range(L));tp=[];p=I
while p not in tp:tp.append(p);p=comp(T,p)
group=set(tp+[comp(S,p) for p in tp]);assert len(tp)==5 and len(group)==10 and comp(S,S)==I and comp(comp(S,T),S)==inv(T)
edges=[(i,(i+1)%L,"internal") for i in range(L)]+[(L+i,L+(i+1)%L,"internal") for i in range(L)]+[(i,L+(i+1)%L,"connector") for i in range(L)];und={frozenset((u,v)) for u,v,_ in edges};assert all({frozenset((p[u],p[v])) for u,v,_ in edges}==und for p in group);assert all(p[i]%2==i%2 for p in group for i in range(N))
# Generator BFS, independent of the target's explicit full group image sets.
oid=np.full(D,-1,np.int32);reps=[];sizes=[]
for seed in range(D):
 if oid[seed]>=0:continue
 orb={seed};todo=[seed]
 while todo:
  w=todo.pop()
  for p in (T,S):
   z=pw(w,p)
   if z not in orb:orb.add(z);todo.append(z)
 k=len(reps);oid[list(orb)]=k;reps.append(min(orb));sizes.append(len(orb))
reps=np.array(reps,np.int64);sizes=np.array(sizes,np.int64);M=len(reps);assert np.all(oid>=0) and sum(sizes)==D
# Assemble from destination representatives (incoming multiplicity), the
# transpose-normalization route rather than target source multiplicities.
src=[];dst=[];val=[]
for b,w0 in enumerate(reps):
 cnt=Counter()
 for u,v,_ in edges:
  w=int(w0)
  if ((w>>u)&1)!=((w>>v)&1):cnt[int(oid[w^(1<<u)^(1<<v)])]+=1
 for a,m in sorted(cnt.items()):src.append(a);dst.append(b);val.append(-m*math.sqrt(int(sizes[b])/int(sizes[a])))
src=np.array(src,np.int32);dst=np.array(dst,np.int32);val=np.array(val,float);keys=src.astype(np.int64)*M+dst;order=np.argsort(keys);rev=dst.astype(np.int64)*M+src;pos=np.searchsorted(keys[order],rev);assert np.all(pos<len(keys)) and np.all(keys[order][pos]==rev);herm=float(max(abs(val-val[order][pos])))
# Derive signed oriented-edge orbits, then calculate their kernels from every word.
oriented=[(u,v) for u,v,_ in edges];lookup={e:(i,1) for i,e in enumerate(oriented)};lookup.update({(v,u):(i,-1) for i,(u,v) in enumerate(oriented)});mapping={};ereps=[]
for seed in range(len(edges)):
 if seed in mapping:continue
 ereps.append(seed)
 for p in group:
  i,s=lookup[(p[oriented[seed][0]],p[oriented[seed][1]])]
  if i in mapping:assert mapping[i]==(len(ereps)-1,s)
  mapping[i]=(len(ereps)-1,s)
assert len(ereps)==3 and len(mapping)==30
words=np.arange(D,dtype=np.int64);kern=[]
for ei in ereps:
 u,v=oriented[ei];a=words[((words>>u)&1)!=((words>>v)&1)];sw=a^(1<<u)^(1<<v);left=oid[a];right=oid[sw];sgn=((a>>v)&1)-((a>>u)&1);kern.append((left,right,sgn/np.sqrt(sizes[left]*sizes[right])))
even=sum(1<<i for i in range(0,N,2));state=np.zeros(M,complex);ok=(reps&even)==0;state[ok]=np.sqrt(sizes[ok])/math.sqrt(1<<L);state0=state.copy();integ=np.array([jc(state,*z) for z in kern]);dt=K/STEPS
for it in range(1,STEPS+1):
 k1=-1j*ha(state,src,dst,val,M);k2=-1j*ha(state+dt*k1/2,src,dst,val,M);k3=-1j*ha(state+dt*k2/2,src,dst,val,M);k4=-1j*ha(state+dt*k3,src,dst,val,M);state+=dt*(k1+2*k2+2*k3+k4)/6;integ+=(1 if it==STEPS else 4 if it%2 else 2)*np.array([jc(state,*z) for z in kern])
integ*=dt/3;J=np.array([s*integ[r] for _,(r,s) in sorted(mapping.items())]);p=abs(state[oid])**2/sizes[oid];p0=abs(state0[oid])**2/sizes[oid];q=np.array([((words>>i)&1).astype(float) for i in range(N)]);q1=np.einsum("im,m->i",q,p,optimize=False);q0=np.einsum("im,m->i",q,p0,optimize=False);B=np.zeros((N,30))
for i,(u,v,_) in enumerate(edges):B[u,i]=1;B[v,i]=-1
res=q1-q0+np.einsum("ve,e->v",B,J,optimize=False);corr=max(abs((p*q[u]*q[v]).sum()-q1[u]*q1[v]) for u,v,_ in edges);num=np.array([bin(int(w)).count("1") for w in reps]);law=max(abs(sum(abs(state[num==i])**2)-sum(abs(state0[num==i])**2)) for i in range(N+1));e0=np.vdot(state0,ha(state0,src,dst,val,M)).real;e1=np.vdot(state,ha(state,src,dst,val,M)).real;cm=np.array([k=="connector" for _,_,k in edges]);thr=float(sum(abs(J)));ct=float(sum(abs(J[cm])));g=50*thr
l4=json.loads((ROOT/"AUDIT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001"/"INDEPENDENT_RESULT.json").read_text())["rows"][1];l6=json.loads((ROOT/"AUDIT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001"/"INDEPENDENT_RESULT.json").read_text());l8=json.loads((ROOT/"AUDIT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001"/"INDEPENDENT_RESULT.json").read_text())
def ratios(x,ret):return {"total":g/x["absolute_oriented_throughput_global"],"per_retained":(g/250)/(x["absolute_oriented_throughput_global"]/ret)}
out={"schema":"AUDIT_R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001","method":"GENERATOR_BFS__DESTINATION_NORMALIZED_QUOTIENT__DERIVED_EDGE_ORBITS__RK4_4096_SIMPSON","finite_orbit_basis":{"full_dimension":D,"finite_group_order":len(group),"orbit_dimension":M,"orbit_size_histogram":{str(k):v for k,v in sorted(Counter(sizes.tolist()).items())},"reduced_hamiltonian_nonzero_entries":len(val),"reduced_hamiltonian_hermiticity_error":herm},"census":{"components":50,"sites_global":1000,"sites_per_F3_layer":500,"possible_F3_links":250000,"selected_edges_global_owner_once":1500,"prepared_source_lineages":500,"expected_retained_global":250},"q_before":q0.tolist(),"q_after":q1.tolist(),"integrated_oriented_currents":J.tolist(),"absolute_oriented_throughput_per_component":thr,"absolute_oriented_throughput_global":g,"absolute_connector_throughput_per_component":ct,"absolute_connector_throughput_global":50*ct,"expected_retained_global":float(50*sum(q1)),"max_abs_connected_edge_correlation":float(corr),"residual_l1":float(sum(abs(res))),"residual_linf":float(max(abs(res))),"norm_error":float(abs(np.vdot(state,state).real-1)),"energy_error":float(abs(e1-e0)),"number_law":float(law),"L10_over_L4":ratios(l4,16),"L10_over_L6":ratios(l6,54),"L10_over_L8":ratios(l8,128),"ctp_Z00":float(np.vdot(state0,state0).real),"conditional":"SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","scope":"EXACT_FINITE_BASIS__NUMERICAL_EVOLUTION_QUADRATURE__NO_DEFECT_AUTONOMOUS_SUPPORT_GRID_CONTINUUM_WARD_CRITICAL_PHASE_GRAVITON_GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print("PASS_L10_INDEPENDENT")
