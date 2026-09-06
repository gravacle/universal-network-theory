#!/usr/bin/env python3
import json,math,os
from pathlib import Path
os.environ.setdefault("VECLIB_MAXIMUM_THREADS","1");os.environ.setdefault("OPENBLAS_NUM_THREADS","1")
import numpy as np
E=tuple([(i,(i+1)%4,"cycle_0") for i in range(4)]+[(4+i,4+(i+1)%4,"cycle_1") for i in range(4)]+[(i,4+(i+1)%4,"connector") for i in range(4)]);checks=0
def ck(v,s):
 global checks
 if not v:raise AssertionError(s)
 checks+=1
ck(len(E)==12 and len(set((u,v) for u,v,_ in E))==12,"edges");ck([sum(i in (u,v) for u,v,_ in E) for i in range(8)]==[3]*8,"degree")
seen={0};front=[0]
while front:
 x=front.pop()
 for u,v,_ in E:
  y=v if x==u else u if x==v else None
  if y is not None and y not in seen:seen.add(y);front.append(y)
ck(len(seen)==8,"connected");ck(8*8==64 and 8*12==96,"global")
b=np.arange(256);q=np.array([((b>>i)&1).astype(float) for i in range(8)]);H=np.zeros((256,256));Js=[]
for u,v,_ in E:
 J=np.zeros((256,256),complex)
 for w in b:
  if ((w>>u)&1)!=((w>>v)&1):H[w^(1<<u)^(1<<v),w]-=1
  if ((w>>u)&1)==1 and ((w>>v)&1)==0:s=w^(1<<u)^(1<<v);J[s,w]+=1j;J[w,s]-=1j
 Js.append(J)
psi0=np.zeros(256,complex);psi0[[w for w in b if all(((w>>i)&1)==0 for i in range(0,8,2))]]=.25;ev,V=np.linalg.eigh(H);coef=np.einsum("ia,i->a",V.conj(),psi0,optimize=False);Ec=[np.einsum("ia,ij,jb->ab",V.conj(),J,V,optimize=False) for J in Js];de=ev[:,None]-ev[None,:];p0=abs(psi0)**2;q0=np.einsum("im,m->i",q,p0,optimize=False);num=q.sum(0).astype(int);law0=np.array([p0[num==i].sum() for i in range(9)]);e0=float(np.vdot(psi0,np.einsum("ij,j->i",H,psi0,optimize=False)).real);B=np.zeros((8,12))
for i,(u,v,_) in enumerate(E):B[u,i]=1;B[v,i]=-1
rows=[]
for k in (0.,math.pi/2):
 psi=np.einsum("ia,a->i",V,np.exp(-1j*ev*k)*coef,optimize=False);p=abs(psi)**2;q1=np.einsum("im,m->i",q,p,optimize=False);F=np.empty_like(de,dtype=complex);z=abs(de)<1e-12;F[z]=k;F[~z]=(np.exp(1j*de[~z]*k)-1)/(1j*de[~z]);J=np.array([float(np.sum(coef.conj()[:,None]*coef[None,:]*X*F).real) for X in Ec]);r=q1-q0+np.einsum("ve,e->v",B,J,optimize=False);C=np.array([(p*q[u]*q[v]).sum()-q1[u]*q1[v] for u,v,_ in E]);law=np.array([p[num==i].sum() for i in range(9)]);hp=np.einsum("ij,j->i",H,psi,optimize=False);cm=np.array([x=="connector" for _,_,x in E]);t=float(abs(J).sum());c=float(abs(J[cm]).sum())
 rows.append({"kappa":k,"q_before":q0.tolist(),"q_after":q1.tolist(),"integrated_oriented_currents":J.tolist(),"active_internal_supports_per_component":int(np.sum(abs(J[~cm])>1e-12)),"active_connector_supports_per_component":int(np.sum(abs(J[cm])>1e-12)),"absolute_oriented_throughput_per_component":t,"absolute_oriented_throughput_global":8*t,"absolute_connector_throughput_per_component":c,"absolute_connector_throughput_global":8*c,"expected_retained_per_component":float(q1.sum()),"expected_retained_global":float(8*q1.sum()),"max_abs_connected_edge_correlation":float(np.max(abs(C))),"record_ledger_residual_l1_per_component":float(abs(r).sum()),"record_ledger_residual_linf_per_component":float(abs(r).max()),"record_ledger_residual_l1_global_bound":float(8*abs(r).sum()),"norm_error":float(abs(np.vdot(psi,psi).real-1)),"energy_error":float(abs(np.vdot(psi,hp).real-e0)),"number_law_max_change":float(np.max(abs(law-law0))),"uniform_onsite_commutator_linf":0.})
ck(rows[0]["active_internal_supports_per_component"]==rows[0]["active_connector_supports_per_component"]==0,"zero");ck(rows[1]["active_internal_supports_per_component"]==8 and rows[1]["active_connector_supports_per_component"]==4,"active");ck(abs(rows[1]["expected_retained_global"]-16)<2e-12,"retention");ck(max(x["record_ledger_residual_l1_per_component"] for x in rows)<2e-11,"ledger");ck(max(x["norm_error"] for x in rows)<4e-14 and max(x["energy_error"] for x in rows)<4e-13 and max(x["number_law_max_change"] for x in rows)<4e-14,"controls");ck(abs(np.vdot(psi0,psi0)-1)<1e-15,"Z00")
d=next(x for x in json.loads((Path(__file__).parent.parent/"DEVELOPMENT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001/RESULT.json").read_text())["rows"] if x["L"]==4);ratio=rows[1]["absolute_oriented_throughput_global"]/d["absolute_oriented_throughput_total"]
out={"schema":"AUDIT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001","checks":checks,"rows":rows,"ratio":ratio,"census":{"sites_global":64,"sites_per_F3_layer":32,"possible_F3_links":1024,"components":8,"selected_edges_global_owner_once":96,"prepared_source_lineages":32},"ctp":"FINITE_Z00_ONE__NOT_1PI_OR_WARD","conditional":"SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","source":"UNIFORM_NO_EXTRA_ASYMMETRY","scope":"NO_ORDER_STAGGER_DEFECT_GRID_CONTINUUM_CRITICAL_PHASE_WARD_GRAVITY"};(Path(__file__).parent/"INDEPENDENT_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(f"PASS_CONNECTED_INDEPENDENT__{checks}/{checks}")
