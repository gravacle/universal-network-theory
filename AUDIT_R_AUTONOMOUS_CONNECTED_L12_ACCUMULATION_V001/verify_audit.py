#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;T=H.parent/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L12_ACCUMULATION_V001";n=0
def ck(v,m):
 global n
 if not v:raise AssertionError(m)
 n+=1
def near(a,b,t,m):ck(abs(float(a)-float(b))<=t,m)
def vmax(a,b):return max(abs(float(x)-float(y)) for x,y in zip(a,b))
pins={"README.md":"310b93d56a6ca919c865f73532d33614325ad059693de43ad760db0423afb9c1","RESULT.json":"154c9195b8ea516e4e637c1f4d66422ab82603163119f9b4451e7c2eb7ff5184","THEOREM.md":"3b174c54ef07977ca422a19e9f2588ac151653cbf69f4f6747cc365e37984b18","compute_connected_l12.py":"ec75d74a4517d457504306a5b83433d4061a510aa0d699d74e600575130a6805","RUN_OBSERVATION.md":"05514fada531ead89cdbffa8f407cd04b32675a98c5e7c4bf93b5b27966195ea"}
for f,h in pins.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==h,"custody "+f)
env=os.environ.copy();env["PYTHONWARNINGS"]="error";r=subprocess.run([sys.executable,"-B",str(T/"compute_connected_l12.py")],capture_output=True,text=True,check=True,env=env);ck("__22/22" in r.stdout,"target replay");ck(hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==pins["RESULT.json"],"canonical result")
r=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env);ck("PASS_L12_INDEPENDENT" in r.stdout,"independent replay");a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text())
o=a["finite_orbit_basis"];hist={"1":4,"2":6,"3":12,"4":30,"6":142,"8":15,"12":10316,"24":693845};ck((o["finite_group_order"],o["full_dimension"],o["orbit_dimension"],o["orbit_size_histogram"],o["quotient_nonzero_entries"],o["quotient_array_bytes"],o["quotient_hermiticity_error"],o["signed_edge_orbits"])==(24,16777216,704370,hist,12582508,201320128,0,2),"orbit quotient")
edges=[(i,(i+1)%12) for i in range(12)]+[(12+i,12+(i+1)%12) for i in range(12)]+[(i,12+(i+1)%12) for i in range(12)];deg=[0]*24;adj=[set() for _ in range(24)]
for u,v in edges:deg[u]+=1;deg[v]+=1;adj[u].add(v);adj[v].add(u)
seen={0};todo=[0]
while todo:
 u=todo.pop()
 for v in adj[u]-seen:seen.add(v);todo.append(v)
ck(len(edges)==36 and deg==[3]*24 and seen==set(range(24)),"connected cubic graph")
c=a["census"];ck((c["components"],c["sites_global"],c["sites_per_F3_layer"],c["possible_F3_links"],c["selected_edges_global_owner_once"],c["prepared_source_lineages"],c["expected_retained_global"])==(72,1728,864,746496,2592,864,432),"global census")
ck(vmax(a["q_before"],b["q_before"])<3e-10 and vmax(a["q_after"],b["q_after"])<3e-10,"all occupations");ck(vmax(a["integrated_oriented_currents"],b["integrated_oriented_currents"])<8e-11,"all 36 signed currents")
for k in ("absolute_oriented_throughput_per_component","absolute_oriented_throughput_global","absolute_connector_throughput_per_component","absolute_connector_throughput_global","expected_retained_global","max_abs_connected_edge_correlation"):near(a[k],b[k],3e-7,"observable "+k)
for k in b["comparators"]:near(a["comparators"][k]["total"],b["comparators"][k]["throughput_total"],3e-7,k+" total");near(a["comparators"][k]["per_retained"],b["comparators"][k]["throughput_per_retained_record"],3e-7,k+" retained")
ck(a["residual_l1"]<2e-9 and a["residual_linf"]<1e-10,"independent continuity");ck(a["norm_error"]<5e-11 and a["energy_error"]<3e-10 and a["number_law"]<2e-11,"independent conservation")
ratio=b["coarse_record_ledger_residual_l1_per_component"]/b["record_ledger_residual_l1_per_component"];ck(14<ratio<19,"target refinement ratio");ck(b["current_refinement_linf"]<1e-10 and b["state_refinement_linf"]<1e-13 and b["occupation_refinement_linf"]<1e-13,"target refinement envelope");ck("EXACT_ORDER_2L_FINITE_ORBIT_BASIS__REFINED_NUMERICAL" in b["classification"] and "EXACT_TIME_EVOLUTION__EXACT_CURRENT_QUADRATURE" in b["not_claimed"],"exact numerical boundary");ck(b["residual_status"]=="RAW_UNASSIGNED_RECORD_LEDGER_RESIDUALS__NOT_CALLED_DEFECTS","residual classification")
note=(T/"RUN_OBSERVATION.md").read_text();ck(all(s in note for s in ("48 GiB","321.367049417 s","2,399,076,352","2.23431396484375 GiB","not a universal runtime or\ncomplexity claim")),"resource custody")
ck(b["ctp_bookkeeping"]=="ONE_DEFORMATION_SOURCE_PER_UNIQUE_EDGE__Z_0_0_EQUALS_ONE" and abs(a["ctp_Z00"]-1)<1e-12,"finite CTP");ck(a["conditional"]=="SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","conditional inputs");ck(all(s in a["scope"] for s in ("NO_DEFECT","GRID","CONTINUUM","MONOTONICITY","LIMIT","SCALING","WARD","CRITICAL","PHASE","GRAVITON","GRAVITY")),"claim ceiling");ck("No correction required" in (H/"AUDIT_REPORT.md").read_text(),"disposition")
print(f"PASS__CONNECTED_L12_HOSTILE_AUDIT__{n}/{n}")
