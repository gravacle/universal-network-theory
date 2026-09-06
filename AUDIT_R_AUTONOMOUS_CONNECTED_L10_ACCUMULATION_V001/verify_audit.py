#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;T=H.parent/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001";n=0
def ck(v,m):
 global n
 if not v:raise AssertionError(m)
 n+=1
def near(a,b,t,m):ck(abs(float(a)-float(b))<=t,m)
def vmax(a,b):return max(abs(float(x)-float(y)) for x,y in zip(a,b))
pins={"README.md":"5b74ad0a638d4592d3e7a599eaf58927d452c210f49a07a81f45ae64fdcf7a51","RESULT.json":"06256f48fb39df0b5121ea01b38893ffeb84ba1bc7f842d22935ccd5279cdcbf","THEOREM.md":"07645b4a3a9095e3faf3c9587e0162c2eed17caea068a76c63de0e960c621804","compute_connected_l10.py":"d5334e3af6beb062126a00f2859ecdc9f8bb01bf3a8937d460f09e5feab30b26","RUN_OBSERVATION.md":"8e1cdb5db2fa58997d6fc110c1fdcc6752a9f9e7714dfe52ff1bff493d831d17"}
for f,h in pins.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==h,"custody "+f)
env=os.environ.copy();env["PYTHONWARNINGS"]="error";r=subprocess.run([sys.executable,"-B",str(T/"compute_connected_l10.py")],capture_output=True,text=True,check=True,env=env);ck("__24/24" in r.stdout,"target replay");ck(hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==pins["RESULT.json"],"canonical result")
r=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env);ck("PASS_L10_INDEPENDENT" in r.stdout,"independent replay");a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text())
o=a["finite_orbit_basis"];ck((o["full_dimension"],o["finite_group_order"],o["orbit_dimension"],o["reduced_hamiltonian_nonzero_entries"],o["reduced_hamiltonian_hermiticity_error"])==(1048576,10,105376,1570516,0),"orbit/quotient census");ck(o["orbit_size_histogram"]=={"1":4,"2":6,"5":1020,"10":104346},"orbit histogram");ck(sum(int(k)*v for k,v in o["orbit_size_histogram"].items())==1048576,"complete orbit coverage")
edges=[(i,(i+1)%10) for i in range(10)]+[(10+i,10+(i+1)%10) for i in range(10)]+[(i,10+(i+1)%10) for i in range(10)];deg=[0]*20;adj=[set() for _ in range(20)]
for u,v in edges:deg[u]+=1;deg[v]+=1;adj[u].add(v);adj[v].add(u)
seen={0};todo=[0]
while todo:
 u=todo.pop()
 for v in adj[u]-seen:seen.add(v);todo.append(v)
ck(len(edges)==30 and deg==[3]*20 and seen==set(range(20)),"connected cubic graph")
c=a["census"];ck((c["components"],c["sites_global"],c["sites_per_F3_layer"],c["possible_F3_links"])==(50,1000,500,250000),"site/link census");ck((c["selected_edges_global_owner_once"],c["prepared_source_lineages"],c["expected_retained_global"])==(1500,500,250),"owner/source/retained census")
ck(vmax(a["q_before"],b["q_before"])<3e-12 and vmax(a["q_after"],b["q_after"])<3e-12,"all occupations");ck(vmax(a["integrated_oriented_currents"],b["integrated_oriented_currents"])<2e-12,"all signed currents")
for k in ("absolute_oriented_throughput_per_component","absolute_oriented_throughput_global","absolute_connector_throughput_per_component","absolute_connector_throughput_global","expected_retained_global","max_abs_connected_edge_correlation"):near(a[k],b[k],2e-9,"observable "+k)
for k in ("L10_over_L4","L10_over_L6","L10_over_L8"):near(a[k]["total"],b[k]["throughput_total"],2e-9,k+" total");near(a[k]["per_retained"],b[k]["throughput_per_retained_record"],2e-9,k+" retained")
ck(a["residual_l1"]<3e-11 and a["residual_linf"]<3e-12,"continuity");ck(a["norm_error"]<3e-12 and a["energy_error"]<3e-12 and a["number_law"]<3e-12,"conservation")
ratio=b["coarse_record_ledger_residual_l1_per_component"]/b["record_ledger_residual_l1_per_component"];ck(14<ratio<18,"fourth-order-consistent residual refinement");ck(b["current_refinement_linf"]<3e-11 and b["state_refinement_linf"]<3e-13 and b["occupation_refinement_linf"]<3e-13,"refinement envelope");ck("EXACT_FINITE_ORBIT_BASIS__REFINED_NUMERICAL" in b["classification"] and "EXACT_TIME_EVOLUTION__EXACT_CURRENT_QUADRATURE" in b["not_claimed"],"exact/numerical boundary")
note=(T/"RUN_OBSERVATION.md").read_text();ck(all(x in note for x in ("48 GiB","48.279534083 s","349,585,408","333.390625 MiB","not a universal runtime or\ncomplexity claim")),"resource custody")
ck(b["ctp_bookkeeping"]=="ONE_DEFORMATION_SOURCE_PER_UNIQUE_EDGE__Z_0_0_EQUALS_ONE" and abs(a["ctp_Z00"]-1)<1e-12,"owner-once CTP");ck(a["conditional"]=="SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","conditional inputs");ck(all(x in a["scope"] for x in ("NO_DEFECT","AUTONOMOUS_SUPPORT","GRID","CONTINUUM","WARD","CRITICAL","PHASE","GRAVITON","GRAVITY")),"claim ceiling");ck("No correction required" in (H/"AUDIT_REPORT.md").read_text(),"disposition")
print(f"PASS__CONNECTED_L10_HOSTILE_AUDIT__{n}/{n}")
