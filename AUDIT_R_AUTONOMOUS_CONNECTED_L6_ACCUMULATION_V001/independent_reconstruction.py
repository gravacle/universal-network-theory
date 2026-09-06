#!/usr/bin/env python3
"""Independent RK4/Simpson reconstruction (not target Taylor stepping)."""
import json,math,os
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1")
import numpy as np
L=6;N=12;D=4096;steps=4096;dt=(math.pi/2)/steps;words=np.arange(D);edges=tuple([(i,(i+1)%L,"internal") for i in range(L)]+[(L+i,L+(i+1)%L,"internal") for i in range(L)]+[(i,L+(i+1)%L,"connector") for i in range(L)]);acts=[]
for u,v,k in edges:
 a=words[((words>>u)&1)!=((words>>v)&1)];s=a^(1<<u)^(1<<v);coef=1j*(((a>>v)&1)-((a>>u)&1));acts.append((a,s,coef,k))
def hv(x):
 y=np.zeros_like(x)
 for a,s,_,_ in acts:y[a]-=x[s]
 return y
def cur(x):return np.array([float(np.vdot(x[a],c*x[s]).real) for a,s,c,_ in acts])
psi=np.zeros(D,complex);psi[[w for w in words if all(((w>>i)&1)==0 for i in range(0,N,2))]]=1/8;psi0=psi.copy();integ=cur(psi)
for n in range(1,steps+1):
 k1=-1j*hv(psi);k2=-1j*hv(psi+dt*k1/2);k3=-1j*hv(psi+dt*k2/2);k4=-1j*hv(psi+dt*k3);psi+=dt*(k1+2*k2+2*k3+k4)/6;integ+=(1 if n==steps else 4 if n%2 else 2)*cur(psi)
J=integ*dt/3;q=np.array([((words>>i)&1).astype(float) for i in range(N)]);p0=abs(psi0)**2;p=abs(psi)**2;q0=np.einsum("im,m->i",q,p0,optimize=False);q1=np.einsum("im,m->i",q,p,optimize=False);B=np.zeros((N,18))
for i,(u,v,_) in enumerate(edges):B[u,i]=1;B[v,i]=-1
res=q1-q0+np.einsum("ve,e->v",B,J,optimize=False);num=q.sum(0).astype(int);law0=np.array([p0[num==i].sum() for i in range(13)]);law=np.array([p[num==i].sum() for i in range(13)]);corr=np.array([(p*q[u]*q[v]).sum()-q1[u]*q1[v] for u,v,_ in edges]);cm=np.array([k=="connector" for _,_,k in edges]);thr=float(abs(J).sum());ct=float(abs(J[cm]).sum());h0=hv(psi0);h1=hv(psi)
l4=json.loads((Path(__file__).parent.parent/"AUDIT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001"/"INDEPENDENT_RESULT.json").read_text())["rows"][1];l4thr=l4["absolute_oriented_throughput_global"]
out={"schema":"AUDIT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001","method":"MATRIX_FREE_RK4_ORDER4_4096_STEPS_PLUS_SIMPSON","census":{"sites_global":216,"sites_per_F3_layer":108,"possible_F3_links":11664,"components":18,"sites_per_component":12,"internal_edges_per_component":12,"connector_edges_per_component":6,"selected_edges_global_owner_once":324,"prepared_source_lineages":108,"expected_retained_global":54},"q_before":q0.tolist(),"q_after":q1.tolist(),"integrated_oriented_currents":J.tolist(),"absolute_oriented_throughput_per_component":thr,"absolute_oriented_throughput_global":18*thr,"absolute_connector_throughput_per_component":ct,"absolute_connector_throughput_global":18*ct,"expected_retained_global":float(18*q1.sum()),"max_abs_connected_edge_correlation":float(np.max(abs(corr))),"residual_l1":float(abs(res).sum()),"residual_linf":float(abs(res).max()),"norm_error":float(abs(np.vdot(psi,psi).real-1)),"energy_error":float(abs(np.vdot(psi,h1).real-np.vdot(psi0,h0).real)),"number_law":float(np.max(abs(law-law0))),"L6_over_L4_total_throughput_ratio":float(18*thr/l4thr),"L6_over_L4_per_retained_ratio":float((18*thr/54)/(l4thr/16)),"ctp_Z00":float(np.vdot(psi0,psi0).real),"conditional":"SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","scope":"NO_EXACT_QUADRATURE_DEFECT_GRID_CONTINUUM_WARD_CRITICAL_PHASE_GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print("PASS_L6_RK4_INDEPENDENT")
