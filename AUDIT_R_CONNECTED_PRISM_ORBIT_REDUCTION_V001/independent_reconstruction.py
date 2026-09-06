#!/usr/bin/env python3
"""Generator orbit BFS, destination quotient, RK4, and L12 structural screen."""
import json,math,os
from collections import Counter
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1");os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
from numba import njit
ROOT=Path(__file__).parent.parent;K=math.pi/2;STEPS=4096
TARGETS={4:ROOT/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001"/"RESULT.json",6:ROOT/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001"/"RESULT.json",8:ROOT/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001"/"RESULT.json",10:ROOT/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001"/"RESULT.json"}
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def pw(w,p):
 z=0
 for i,j in enumerate(p):
  if (w>>i)&1:z|=1<<j
 return z
def maps(L):
 # Generated directly from x=i-a: unit rotation and zero-shift reflection.
 rot=[];ref=[]
 for a in range(2):
  for i in range(L):
   x=(i-a)%L;ap=a^1;rot.append(ap*L+(x+1+ap)%L);ref.append(a*L+((-x)+a)%L)
 return tuple(rot),tuple(ref)
@njit
def pword(w,p):
 z=0
 for i in range(len(p)):
  if (w>>i)&1:z|=1<<p[i]
 return z
@njit
def build_ids(D,T,S,maxg):
 oid=np.full(D,-1,np.int32);reps=np.empty(D,np.int64);sizes=np.empty(D,np.int32);stack=np.empty(maxg,np.int64);n=0
 for seed in range(D):
  if oid[seed]>=0:continue
  count=1;stack[0]=seed;pos=0
  while pos<count:
   w=stack[pos];pos+=1
   for p in (T,S):
    z=pword(w,p);found=False
    for j in range(count):
     if stack[j]==z:found=True;break
    if not found:stack[count]=z;count+=1
  for j in range(count):oid[stack[j]]=n
  reps[n]=seed;sizes[n]=count;n+=1
 return oid,reps[:n],sizes[:n]
@njit
def count_nnz(reps,oid,L):
 dest=np.empty(3*L,np.int32);total=0
 for ii in range(len(reps)):
  w=reps[ii];nd=0
  for e in range(3*L):
   if e<L:u=e;v=(e+1)%L
   elif e<2*L:u=e;v=L+(e-L+1)%L
   else:u=e-2*L;v=L+(u+1)%L
   if ((w>>u)&1)!=((w>>v)&1):
    d=oid[w^(1<<u)^(1<<v)];seen=False
    for j in range(nd):
     if dest[j]==d:seen=True;break
    if not seen:dest[nd]=d;nd+=1
  total+=nd
 return total
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
def group_from_generators(T,S):
 I=tuple(range(len(T)));g={I};todo=[I]
 while todo:
  q=todo.pop()
  for p in (T,S):
   z=comp(p,q)
   if z not in g:g.add(z);todo.append(z)
 return g
def run(L):
 N=2*L;D=1<<N;T,S=maps(L);group=group_from_generators(T,S);assert len(group)==2*L
 edges=[(i,(i+1)%L,"internal") for i in range(L)]+[(L+i,L+(i+1)%L,"internal") for i in range(L)]+[(i,L+(i+1)%L,"connector") for i in range(L)];und={frozenset((u,v)) for u,v,_ in edges};assert all({frozenset((p[u],p[v])) for u,v,_ in edges}==und for p in group) and all(p[i]%2==i%2 for p in group for i in range(N))
 oid,reps,sizes=build_ids(D,np.array(T,np.int64),np.array(S,np.int64),2*L);M=len(reps);assert sum(sizes)==D
 # Destination-side incoming multiplicities, distinct from target source assembly.
 src=[];dst=[];val=[]
 for b,w0 in enumerate(reps):
  c=Counter();w=int(w0)
  for u,v,_ in edges:
   if ((w>>u)&1)!=((w>>v)&1):c[int(oid[w^(1<<u)^(1<<v)])]+=1
  for a,m in sorted(c.items()):src.append(a);dst.append(b);val.append(-m*math.sqrt(int(sizes[b])/int(sizes[a])))
 src=np.array(src,np.int32);dst=np.array(dst,np.int32);val=np.array(val,float);keys=src.astype(np.int64)*M+dst;order=np.argsort(keys);rev=dst.astype(np.int64)*M+src;pos=np.searchsorted(keys[order],rev);assert np.all(pos<len(keys)) and np.all(keys[order][pos]==rev);herm=float(max(abs(val-val[order][pos])))
 oriented=[(u,v) for u,v,_ in edges];lookup={e:(i,1) for i,e in enumerate(oriented)};lookup.update({(v,u):(i,-1) for i,(u,v) in enumerate(oriented)});mapping={};ereps=[]
 for seed in range(len(edges)):
  if seed in mapping:continue
  ereps.append(seed)
  for p in group:
   i,s=lookup[(p[oriented[seed][0]],p[oriented[seed][1]])]
   if i in mapping:assert mapping[i]==(len(ereps)-1,s)
   mapping[i]=(len(ereps)-1,s)
 assert len(ereps)==2 and len(mapping)==3*L
 words=np.arange(D,dtype=np.int64);kern=[]
 for ei in ereps:
  u,v=oriented[ei];a=words[((words>>u)&1)!=((words>>v)&1)];sw=a^(1<<u)^(1<<v);left=oid[a];right=oid[sw];sgn=((a>>v)&1)-((a>>u)&1);kern.append((left,right,sgn/np.sqrt(sizes[left]*sizes[right])))
 even=sum(1<<i for i in range(0,N,2));state=np.zeros(M,complex);ok=(reps&even)==0;state[ok]=np.sqrt(sizes[ok])/math.sqrt(1<<L);state0=state.copy();integ=np.array([jc(state,*z) for z in kern]);dt=K/STEPS
 for it in range(1,STEPS+1):
  k1=-1j*ha(state,src,dst,val,M);k2=-1j*ha(state+dt*k1/2,src,dst,val,M);k3=-1j*ha(state+dt*k2/2,src,dst,val,M);k4=-1j*ha(state+dt*k3,src,dst,val,M);state+=dt*(k1+2*k2+2*k3+k4)/6;integ+=(1 if it==STEPS else 4 if it%2 else 2)*np.array([jc(state,*z) for z in kern])
 integ*=dt/3;J=np.array([s*integ[r] for _,(r,s) in sorted(mapping.items())]);p=abs(state[oid])**2/sizes[oid];p0=abs(state0[oid])**2/sizes[oid];q=np.array([((words>>i)&1).astype(float) for i in range(N)]);q1=np.einsum("im,m->i",q,p,optimize=False);q0=np.einsum("im,m->i",q,p0,optimize=False);B=np.zeros((N,3*L))
 for i,(u,v,_) in enumerate(edges):B[u,i]=1;B[v,i]=-1
 res=q1-q0+np.einsum("ve,e->v",B,J,optimize=False);num=np.array([bin(int(w)).count("1") for w in reps]);law=max(abs(sum(abs(state[num==i])**2)-sum(abs(state0[num==i])**2)) for i in range(N+1));e0=np.vdot(state0,ha(state0,src,dst,val,M)).real;e1=np.vdot(state,ha(state,src,dst,val,M)).real;tar=json.loads(TARGETS[L].read_text());tar=next(x for x in tar["rows"] if x["kappa"]==K) if L==4 else tar
 return {"L":L,"full_dimension":D,"finite_group_order":len(group),"orbit_dimension":M,"orbit_size_histogram":{str(k):v for k,v in sorted(Counter(sizes.tolist()).items())},"quotient_nonzero_entries":len(val),"quotient_hermiticity_error":herm,"signed_edge_orbits":len(ereps),"q_after":q1.tolist(),"integrated_oriented_currents":J.tolist(),"q_target_linf":float(max(abs(q1-np.array(tar["q_after"])))),"current_target_linf":float(max(abs(J-np.array(tar["integrated_oriented_currents"])))),"record_ledger_residual_l1":float(sum(abs(res))),"record_ledger_residual_linf":float(max(abs(res))),"norm_error":float(abs(np.vdot(state,state).real-1)),"energy_error":float(abs(e1-e0)),"number_law_max_change":float(law)}
rows=[run(L) for L in (4,6,8,10)]
# Independent structural-only L12 screen; no state evolution is performed.
T12,S12=maps(12);oid12,reps12,sizes12=build_ids(1<<24,np.array(T12,np.int64),np.array(S12,np.int64),24);nnz12=int(count_nnz(reps12,oid12,12));hist12={str(k):v for k,v in sorted(Counter(sizes12.tolist()).items())};del oid12,reps12,sizes12
out={"schema":"AUDIT_R_CONNECTED_PRISM_ORBIT_REDUCTION_V001","method":"GENERATOR_BFS__DESTINATION_NORMALIZED_QUOTIENT__DERIVED_SIGNED_EDGE_ORBITS__RK4_4096_SIMPSON","group_definition_verified":"X_EQUALS_I_MINUS_A__UNIT_ROTATION_PARITY_LAYER_SWAP__ZERO_SHIFT_REFLECTION","support_and_source_parity_preserved":True,"rows":rows,"L12_structural_screen":{"full_dimension":1<<24,"orbit_dimension":sum(hist12.values()),"orbit_size_histogram":hist12,"quotient_nonzero_entries":nnz12,"operator_bytes":16*nnz12,"operator_MiB":16*nnz12/2**20,"evolution_performed":False},"conditional":"SUPPORT_SOURCE_KAPPA_ROUTING_CONTENT_CLOCK_READ","scope":"COMPUTATIONAL_COMPRESSION_ONLY__NO_MAXIMALITY_PHYSICAL_GEOMETRY_GRID_CONTINUUM_WARD_CRITICAL_PHASE_GRAVITON_GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print("PASS_PRISM_INDEPENDENT")
