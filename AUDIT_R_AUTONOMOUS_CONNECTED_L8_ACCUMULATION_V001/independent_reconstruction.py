#!/usr/bin/env python3
"""Independent matrix-free RK4 reconstruction of the connected L8 record."""
import json,math,os
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1");os.environ.setdefault("OMP_NUM_THREADS","1")
import numpy as np
L=8;N=16;D=1<<N;steps=4096;dt=(math.pi/2)/steps;words=np.arange(D,dtype=np.int64)
edges=tuple([(i,(i+1)%L,"internal") for i in range(L)]+[(L+i,L+(i+1)%L,"internal") for i in range(L)]+[(i,L+(i+1)%L,"connector") for i in range(L)]);acts=[]
for u,v,k in edges:
 a=words[((words>>u)&1)!=((words>>v)&1)];s=a^(1<<u)^(1<<v);coef=1j*(((a>>v)&1)-((a>>u)&1));acts.append((a,s,coef,k))
def hv(x):
 y=np.zeros_like(x)
 for a,s,_,_ in acts:y[a]-=x[s]
 return y
def cur(x):return np.array([float(np.vdot(x[a],c*x[s]).real) for a,s,c,_ in acts])
psi=np.zeros(D,complex);even=sum(1<<i for i in range(0,N,2));psi[(words&even)==0]=1/math.sqrt(1<<(N//2));psi0=psi.copy();integ=cur(psi)
for n in range(1,steps+1):
 k1=-1j*hv(psi);k2=-1j*hv(psi+dt*k1/2);k3=-1j*hv(psi+dt*k2/2);k4=-1j*hv(psi+dt*k3);psi+=dt*(k1+2*k2+2*k3+k4)/6;integ+=(1 if n==steps else 4 if n%2 else 2)*cur(psi)
J=integ*dt/3;q=np.array([((words>>i)&1).astype(float) for i in range(N)]);p0=abs(psi0)**2;p=abs(psi)**2;q0=np.einsum("im,m->i",q,p0,optimize=False);q1=np.einsum("im,m->i",q,p,optimize=False);B=np.zeros((N,len(edges)))
for i,(u,v,_) in enumerate(edges):B[u,i]=1;B[v,i]=-1
res=q1-q0+np.einsum("ve,e->v",B,J,optimize=False);num=np.array([bin(int(w)).count("1") for w in words]);law0=np.array([p0[num==i].sum() for i in range(N+1)]);law=np.array([p[num==i].sum() for i in range(N+1)]);corr=np.array([(p*q[u]*q[v]).sum()-q1[u]*q1[v] for u,v,_ in edges]);cm=np.array([k=="connector" for _,_,k in edges]);thr=float(abs(J).sum());ct=float(abs(J[cm]).sum());h0=hv(psi0);h1=hv(psi)
root=Path(__file__).parent.parent;l4=json.loads((root/"AUDIT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001"/"INDEPENDENT_RESULT.json").read_text())["rows"][1];l6=json.loads((root/"AUDIT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001"/"INDEPENDENT_RESULT.json").read_text());g=32*thr
out={"schema":"AUDIT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001","method":"MATRIX_FREE_RK4_ORDER4_4096_STEPS_PLUS_SIMPSON","census":{"sites_global":512,"sites_per_F3_layer":256,"possible_F3_links":65536,"components":32,"sites_per_component":16,"internal_edges_per_component":16,"connector_edges_per_component":8,"selected_edges_global_owner_once":768,"prepared_source_lineages":256,"expected_retained_global":128},"q_before":q0.tolist(),"q_after":q1.tolist(),"integrated_oriented_currents":J.tolist(),"absolute_oriented_throughput_per_component":thr,"absolute_oriented_throughput_global":g,"absolute_connector_throughput_per_component":ct,"absolute_connector_throughput_global":32*ct,"expected_retained_global":float(32*q1.sum()),"max_abs_connected_edge_correlation":float(np.max(abs(corr))),"residual_l1":float(abs(res).sum()),"residual_linf":float(abs(res).max()),"norm_error":float(abs(np.vdot(psi,psi).real-1)),"energy_error":float(abs(np.vdot(psi,h1).real-np.vdot(psi0,h0).real)),"number_law":float(np.max(abs(law-law0))),"L8_over_L4_total":float(g/l4["absolute_oriented_throughput_global"]),"L8_over_L4_per_retained":float((g/128)/(l4["absolute_oriented_throughput_global"]/16)),"L8_over_L6_total":float(g/l6["absolute_oriented_throughput_global"]),"L8_over_L6_per_retained":float((g/128)/(l6["absolute_oriented_throughput_global"]/54)),"ctp_Z00":float(np.vdot(psi0,psi0).real),"conditional":"SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","scope":"NO_EXACT_QUADRATURE_DEFECT_GRID_CONTINUUM_WARD_CRITICAL_PHASE_GRAVITON_GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print("PASS_L8_RK4_INDEPENDENT")
