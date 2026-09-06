#!/usr/bin/env python3
"""Independent L12 generator-BFS/destination quotient with RK4 evolution."""
import json,math,os
from collections import Counter
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1");os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
from numba import njit
L=12;N=24;D=1<<N;M_EXPECT=704370;NNZ=12582508;STEPS=1536;K=math.pi/2;ROOT=Path(__file__).parent.parent
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def maps():
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
def build_ids(T,S):
 oid=np.full(D,-1,np.int32);reps=np.empty(M_EXPECT,np.int64);sizes=np.empty(M_EXPECT,np.int32);stack=np.empty(24,np.int64);n=0
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
def assemble(reps,sizes,oid):
 src=np.empty(NNZ,np.int32);dst=np.empty(NNZ,np.int32);val=np.empty(NNZ,np.float64);ds=np.empty(36,np.int32);ms=np.empty(36,np.int32);at=0
 for b in range(len(reps)):
  w=reps[b];nd=0
  for e in range(36):
   if e<L:u=e;v=(e+1)%L
   elif e<2*L:u=e;v=L+(e-L+1)%L
   else:u=e-2*L;v=L+(u+1)%L
   if ((w>>u)&1)!=((w>>v)&1):
    a=oid[w^(1<<u)^(1<<v)];found=-1
    for j in range(nd):
     if ds[j]==a:found=j;break
    if found<0:ds[nd]=a;ms[nd]=1;nd+=1
    else:ms[found]+=1
  # insertion sort makes destination ordering deterministic
  for j in range(1,nd):
   da=ds[j];ma=ms[j];k=j-1
   while k>=0 and ds[k]>da:ds[k+1]=ds[k];ms[k+1]=ms[k];k-=1
   ds[k+1]=da;ms[k+1]=ma
  for j in range(nd):
   a=ds[j];src[at]=a;dst[at]=b;val[at]=-ms[j]*math.sqrt(sizes[b]/sizes[a]);at+=1
 return src[:at],dst[:at],val[:at]
@njit
def ha(x,src,dst,val):
 y=np.zeros(len(x),np.complex128)
 for k in range(len(val)):y[dst[k]]+=val[k]*x[src[k]]
 return y
@njit
def jc(x,left,right,f):
 z=0j
 for k in range(len(f)):z+=np.conjugate(x[left[k]])*(1j*f[k])*x[right[k]]
 return z.real
T,S=maps();group={tuple(range(N))};todo=list(group)
while todo:
 q=todo.pop()
 for p in (T,S):
  z=comp(p,q)
  if z not in group:group.add(z);todo.append(z)
assert len(group)==24
edges=[(i,(i+1)%L,"internal") for i in range(L)]+[(L+i,L+(i+1)%L,"internal") for i in range(L)]+[(i,L+(i+1)%L,"connector") for i in range(L)];und={frozenset((u,v)) for u,v,_ in edges};assert all({frozenset((p[u],p[v])) for u,v,_ in edges}==und for p in group) and all(p[i]%2==i%2 for p in group for i in range(N))
oid,reps,sizes=build_ids(np.array(T,np.int64),np.array(S,np.int64));assert len(reps)==M_EXPECT and sum(sizes)==D;src,dst,val=assemble(reps,sizes,oid);assert len(val)==NNZ
keys=src.astype(np.int64)*M_EXPECT+dst;order=np.argsort(keys);rev=dst.astype(np.int64)*M_EXPECT+src;pos=np.searchsorted(keys[order],rev);assert np.all(pos<len(keys)) and np.all(keys[order][pos]==rev);herm=float(max(abs(val-val[order][pos])));del keys,order,rev,pos
oriented=[(u,v) for u,v,_ in edges];lookup={e:(i,1) for i,e in enumerate(oriented)};lookup.update({(v,u):(i,-1) for i,(u,v) in enumerate(oriented)});mapping={};ereps=[]
for seed in range(36):
 if seed in mapping:continue
 ereps.append(seed)
 for p in group:
  i,s=lookup[(p[oriented[seed][0]],p[oriented[seed][1]])]
  if i in mapping:assert mapping[i]==(len(ereps)-1,s)
  mapping[i]=(len(ereps)-1,s)
assert len(ereps)==2 and len(mapping)==36
words=np.arange(D,dtype=np.int64);kern=[]
for ei in ereps:
 u,v=oriented[ei];a=words[((words>>u)&1)!=((words>>v)&1)];sw=a^(1<<u)^(1<<v);left=oid[a];right=oid[sw];sgn=((a>>v)&1)-((a>>u)&1);kern.append((left,right,sgn/np.sqrt(sizes[left]*sizes[right])))
even=sum(1<<i for i in range(0,N,2));state=np.zeros(M_EXPECT,complex);ok=(reps&even)==0;state[ok]=np.sqrt(sizes[ok])/math.sqrt(1<<L);state0=state.copy();integ=np.array([jc(state,*z) for z in kern]);dt=K/STEPS
for it in range(1,STEPS+1):
 k1=-1j*ha(state,src,dst,val);k2=-1j*ha(state+dt*k1/2,src,dst,val);k3=-1j*ha(state+dt*k2/2,src,dst,val);k4=-1j*ha(state+dt*k3,src,dst,val);state+=dt*(k1+2*k2+2*k3+k4)/6;integ+=(1 if it==STEPS else 4 if it%2 else 2)*np.array([jc(state,*z) for z in kern])
integ*=dt/3;J=np.array([s*integ[r] for _,(r,s) in sorted(mapping.items())]);p=abs(state[oid])**2/sizes[oid];p0=abs(state0[oid])**2/sizes[oid];q0=[];q1=[]
for i in range(N):
 mask=((words>>i)&1)==1;q0.append(float(sum(p0[mask])));q1.append(float(sum(p[mask])))
q0=np.array(q0);q1=np.array(q1);B=np.zeros((N,36))
for i,(u,v,_) in enumerate(edges):B[u,i]=1;B[v,i]=-1
res=q1-q0+np.einsum("ve,e->v",B,J,optimize=False);corr=[]
for ei in ereps:
 u,v=oriented[ei];both=(((words>>u)&1)*((words>>v)&1)).astype(bool);corr.append(float(sum(p[both])-q1[u]*q1[v]))
num=np.array([bin(int(w)).count("1") for w in reps]);law=max(abs(sum(abs(state[num==i])**2)-sum(abs(state0[num==i])**2)) for i in range(N+1));e0=np.vdot(state0,ha(state0,src,dst,val)).real;e1=np.vdot(state,ha(state,src,dst,val)).real;cm=np.array([k=="connector" for _,_,k in edges]);thr=float(sum(abs(J)));ct=float(sum(abs(J[cm])));g=72*thr
def prior(name):return json.loads((ROOT/name/"INDEPENDENT_RESULT.json").read_text())
l4=prior("AUDIT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001")["rows"][1];l6=prior("AUDIT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001");l8=prior("AUDIT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001");l10=prior("AUDIT_R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001")
def ratio(x,ret):return {"total":g/x["absolute_oriented_throughput_global"],"per_retained":(g/432)/(x["absolute_oriented_throughput_global"]/ret)}
out={"schema":"AUDIT_R_AUTONOMOUS_CONNECTED_L12_ACCUMULATION_V001","method":"GENERATOR_BFS__DESTINATION_NORMALIZED_QUOTIENT__RK4_1536_SIMPSON","finite_orbit_basis":{"finite_group_order":24,"full_dimension":D,"orbit_dimension":len(reps),"orbit_size_histogram":{str(k):v for k,v in sorted(Counter(sizes.tolist()).items())},"quotient_nonzero_entries":len(val),"quotient_array_bytes":int(src.nbytes+dst.nbytes+val.nbytes),"quotient_hermiticity_error":herm,"signed_edge_orbits":len(ereps)},"census":{"components":72,"sites_global":1728,"sites_per_F3_layer":864,"possible_F3_links":746496,"selected_edges_global_owner_once":2592,"prepared_source_lineages":864,"expected_retained_global":432},"q_before":q0.tolist(),"q_after":q1.tolist(),"integrated_oriented_currents":J.tolist(),"absolute_oriented_throughput_per_component":thr,"absolute_oriented_throughput_global":g,"absolute_connector_throughput_per_component":ct,"absolute_connector_throughput_global":72*ct,"expected_retained_global":float(72*sum(q1)),"max_abs_connected_edge_correlation":float(max(abs(np.array(corr)))),"residual_l1":float(sum(abs(res))),"residual_linf":float(max(abs(res))),"norm_error":float(abs(np.vdot(state,state).real-1)),"energy_error":float(abs(e1-e0)),"number_law":float(law),"comparators":{"L12_over_L4":ratio(l4,16),"L12_over_L6":ratio(l6,54),"L12_over_L8":ratio(l8,128),"L12_over_L10":ratio(l10,250)},"ctp_Z00":float(np.vdot(state0,state0).real),"conditional":"SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","scope":"EXACT_FINITE_BASIS__NUMERICAL_EVOLUTION_QUADRATURE__NO_DEFECT_GRID_CONTINUUM_MONOTONICITY_LIMIT_SCALING_WARD_CRITICAL_PHASE_GRAVITON_GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print("PASS_L12_INDEPENDENT")
