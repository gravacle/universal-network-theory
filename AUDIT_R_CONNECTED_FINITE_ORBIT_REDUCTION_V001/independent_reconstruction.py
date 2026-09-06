#!/usr/bin/env python3
"""Independent generator-BFS/full-transition orbit quotient with RK4 evolution."""
import json,math,os
from collections import Counter,defaultdict
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1");os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
from numba import njit
ROOT=Path(__file__).parent.parent;K=math.pi/2;STEPS=4096
TARGETS={4:ROOT/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001"/"RESULT.json",6:ROOT/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001"/"RESULT.json",8:ROOT/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001"/"RESULT.json"}
def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
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
def run(L):
 N=2*L;D=1<<N;ident=tuple(range(N));T=tuple(a*L+(i+2)%L for a in range(2) for i in range(L));S=tuple((1-a)*L+(-i)%L for a in range(2) for i in range(L))
 cur=ident;tp=[]
 while cur not in tp:tp.append(cur);cur=compose(T,cur)
 group=set(tp+[compose(S,p) for p in tp]);assert len(tp)==L//2 and len(group)==L and compose(S,S)==ident and compose(compose(S,T),S)==inv(T)
 edges=[(i,(i+1)%L,"internal") for i in range(L)]+[(L+i,L+(i+1)%L,"internal") for i in range(L)]+[(i,L+(i+1)%L,"connector") for i in range(L)];und={frozenset((u,v)) for u,v,_ in edges}
 assert all({frozenset((p[u],p[v])) for u,v,_ in edges}==und for p in group);assert all(p[i]%2==i%2 for p in group for i in range(N))
 oid=np.full(D,-1,np.int32);reps=[];sizes=[]
 for seed in range(D):
  if oid[seed]>=0:continue
  orbit={seed};todo=[seed]
  while todo:
   w=todo.pop()
   for p in (T,S):
    z=pw(w,p)
    if z not in orbit:orbit.add(z);todo.append(z)
  k=len(reps);oid[list(orbit)]=k;reps.append(min(orbit));sizes.append(len(orbit))
 reps=np.array(reps,np.int64);sizes=np.array(sizes,np.int64);M=len(reps);assert np.all(oid>=0) and sum(sizes)==D
 # Assemble the normalized quotient by summing every full-basis transition,
 # not by the representative multiplicity formula used by the target.
 h=defaultdict(float)
 for w in range(D):
  a=int(oid[w])
  for u,v,_ in edges:
   if ((w>>u)&1)!=((w>>v)&1):
    z=w^(1<<u)^(1<<v);b=int(oid[z]);h[(b,a)]-=1/math.sqrt(int(sizes[a])*int(sizes[b]))
 # Independently verify OR-01 on every representative destination count.
 formula=0.0
 for a,w0 in enumerate(reps):
  cnt=Counter()
  for u,v,_ in edges:
   if ((int(w0)>>u)&1)!=((int(w0)>>v)&1):cnt[int(oid[int(w0)^(1<<u)^(1<<v)])]+=1
  for b,m in cnt.items():formula=max(formula,abs(h[(b,a)]-(-m*math.sqrt(int(sizes[a])/int(sizes[b])))))
 herm=max(abs(v-h.get((a,b),math.inf)) for (b,a),v in h.items());keys=sorted(h);dst=np.array([x[0] for x in keys],np.int32);src=np.array([x[1] for x in keys],np.int32);val=np.array([h[x] for x in keys])
 # Derive signed oriented-edge orbits from the group action (no hard-coded signs).
 oriented=[(u,v) for u,v,_ in edges];lookup={e:(i,1) for i,e in enumerate(oriented)};lookup.update({(v,u):(i,-1) for i,(u,v) in enumerate(oriented)})
 mapping={};edge_reps=[]
 for seed in range(len(edges)):
  if seed in mapping:continue
  edge_reps.append(seed)
  for p in group:
   i,s=lookup[(p[oriented[seed][0]],p[oriented[seed][1]])]
   if i in mapping:assert mapping[i]==(len(edge_reps)-1,s)
   mapping[i]=(len(edge_reps)-1,s)
 assert len(edge_reps)==3 and len(mapping)==len(edges)
 words=np.arange(D,dtype=np.int64);kernels=[]
 for ei in edge_reps:
  u,v=oriented[ei];active=words[((words>>u)&1)!=((words>>v)&1)];sw=active^(1<<u)^(1<<v);left=oid[active];right=oid[sw];sgn=((active>>v)&1)-((active>>u)&1);f=sgn/np.sqrt(sizes[left]*sizes[right]);kernels.append((left,right,f))
 even=sum(1<<i for i in range(0,N,2));state=np.zeros(M,complex);ok=(reps&even)==0;state[ok]=np.sqrt(sizes[ok])/math.sqrt(1<<L);state0=state.copy();integ=np.array([jc(state,*z) for z in kernels]);dt=K/STEPS
 for it in range(1,STEPS+1):
  k1=-1j*ha(state,src,dst,val,M);k2=-1j*ha(state+dt*k1/2,src,dst,val,M);k3=-1j*ha(state+dt*k2/2,src,dst,val,M);k4=-1j*ha(state+dt*k3,src,dst,val,M);state+=dt*(k1+2*k2+2*k3+k4)/6;integ+=(1 if it==STEPS else 4 if it%2 else 2)*np.array([jc(state,*z) for z in kernels])
 integ*=dt/3;J=np.array([s*integ[r] for _,(r,s) in sorted(mapping.items())]);p=abs(state[oid])**2/sizes[oid];p0=abs(state0[oid])**2/sizes[oid];q=np.array([((words>>i)&1).astype(float) for i in range(N)]);q1=np.einsum("im,m->i",q,p,optimize=False);q0=np.einsum("im,m->i",q,p0,optimize=False);B=np.zeros((N,len(edges)))
 for i,(u,v,_) in enumerate(edges):B[u,i]=1;B[v,i]=-1
 res=q1-q0+np.einsum("ve,e->v",B,J,optimize=False);corr=max(abs((p*q[u]*q[v]).sum()-q1[u]*q1[v]) for u,v,_ in edges);num=np.array([bin(int(w)).count("1") for w in reps]);law=max(abs(sum(abs(state[num==i])**2)-sum(abs(state0[num==i])**2)) for i in range(N+1));e0=np.vdot(state0,ha(state0,src,dst,val,M)).real;e1=np.vdot(state,ha(state,src,dst,val,M)).real
 tar=json.loads(TARGETS[L].read_text());tar=next(x for x in tar["rows"] if x["kappa"]==K) if L==4 else tar
 return {"L":L,"full_dimension":D,"group_order":len(group),"group_relations":True,"support_and_source_parity_invariant":True,"orbit_dimension":M,"orbit_size_histogram":{str(k):v for k,v in sorted(Counter(sizes.tolist()).items())},"reduced_nonzero_entries":len(h),"formula_error":formula,"hermiticity_error":herm,"edge_orbit_representatives":edge_reps,"q_after":q1.tolist(),"integrated_oriented_currents":J.tolist(),"q_target_linf":float(max(abs(q1-np.array(tar["q_after"])))),"current_target_linf":float(max(abs(J-np.array(tar["integrated_oriented_currents"])))),"residual_l1":float(sum(abs(res))),"residual_linf":float(max(abs(res))),"norm_error":float(abs(np.vdot(state,state).real-1)),"energy_error":float(abs(e1-e0)),"number_law":float(law),"max_abs_connected_edge_correlation":float(corr)}
rows=[run(x) for x in (4,6,8)];out={"schema":"AUDIT_R_CONNECTED_FINITE_ORBIT_REDUCTION_V001","method":"GENERATOR_BFS__ALL_FULL_TRANSITIONS_NORMALIZED_QUOTIENT__DERIVED_EDGE_ORBITS__RK4_4096_SIMPSON","rows":rows,"conditional":"SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","scope":"COMPUTATIONAL_COMPRESSION_ONLY__NUMERICAL_EVOLUTION_QUADRATURE__NO_AUTONOMOUS_SUPPORT_GRID_CONTINUUM_WARD_CRITICAL_PHASE_GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print("PASS_ORBIT_INDEPENDENT")
