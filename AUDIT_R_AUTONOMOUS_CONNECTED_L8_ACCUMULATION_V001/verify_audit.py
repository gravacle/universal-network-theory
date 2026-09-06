#!/usr/bin/env python3
"""Pinned hostile verification for the connected L8 packet."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;T=H.parent/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001";n=0
def ck(v,msg):
 global n
 if not v:raise AssertionError(msg)
 n+=1
def near(x,y,t,msg):ck(abs(float(x)-float(y))<=t,msg)
def vmax(x,y):return max(abs(float(a)-float(b)) for a,b in zip(x,y))
pins={"README.md":"69464dc6382b59dc9a74267a3cf545c5c4f414e5bb2e4c5ac11ddf0ff4b5dba0","RESULT.json":"7e4d763138c3090552b7f7a40098c761607653bacb81dfc29bbab7ae4b4f6a63","THEOREM.md":"cf64b4a0e618b09e03ed951af8b960b4a54f25eece6d1e09c549c423259affaa","compute_connected_l8.py":"82a6cd6d3d1b7ed980e379f3686c579e1d583b6edcb430c935a7f5652c615661","RUN_OBSERVATION.md":"4fdacd53b81157118ae0c04d5fa1acbae97f003983968c7c104c27873f089ad0"}
for f,h in pins.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==h,"target custody: "+f)
env=os.environ.copy();env["PYTHONWARNINGS"]="error"
r=subprocess.run([sys.executable,"-B",str(T/"compute_connected_l8.py")],capture_output=True,text=True,check=True,env=env)
ck("__21/21" in r.stdout,"target canonical suite");ck(hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==pins["RESULT.json"],"canonical result custody")
r=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env)
ck("PASS_L8_RK4_INDEPENDENT" in r.stdout,"independent RK4 replay")
a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text())
edges=[(i,(i+1)%8) for i in range(8)]+[(8+i,8+(i+1)%8) for i in range(8)]+[(i,8+(i+1)%8) for i in range(8)]
ck(len(edges)==len(set(tuple(sorted(e)) for e in edges))==24,"24 unique component edges")
deg=[0]*16;adj=[set() for _ in range(16)]
for u,v in edges:deg[u]+=1;deg[v]+=1;adj[u].add(v);adj[v].add(u)
seen={0};todo=[0]
while todo:
 u=todo.pop()
 for v in adj[u]-seen:seen.add(v);todo.append(v)
ck(seen==set(range(16)) and deg==[3]*16,"connected cubic component")
c=a["census"];ck((c["components"],c["sites_global"],c["sites_per_F3_layer"],c["possible_F3_links"])==(32,512,256,65536),"global site/link census");ck((c["selected_edges_global_owner_once"],c["prepared_source_lineages"],c["expected_retained_global"])==(768,256,128),"owner/source/retained census")
ck(vmax(a["q_before"],b["q_before"])<3e-12 and vmax(a["q_after"],b["q_after"])<3e-12,"all occupations");ck(vmax(a["integrated_oriented_currents"],b["integrated_oriented_currents"])<3e-12,"all 24 signed currents")
for k in ("absolute_oriented_throughput_per_component","absolute_oriented_throughput_global","absolute_connector_throughput_per_component","absolute_connector_throughput_global","max_abs_connected_edge_correlation","expected_retained_global"):near(a[k],b[k],8e-10,"observable: "+k)
near(a["L8_over_L4_total"],b["L8_over_L4"]["throughput_total"],8e-10,"L8/L4 total");near(a["L8_over_L4_per_retained"],b["L8_over_L4"]["throughput_per_retained_record"],8e-10,"L8/L4 retained");near(a["L8_over_L6_total"],b["L8_over_L6"]["throughput_total"],8e-10,"L8/L6 total");near(a["L8_over_L6_per_retained"],b["L8_over_L6"]["throughput_per_retained_record"],8e-10,"L8/L6 retained")
ck(a["norm_error"]<3e-12 and a["energy_error"]<3e-12 and a["number_law"]<3e-12,"independent conservation");ck(a["residual_l1"]<3e-11 and a["residual_linf"]<3e-12,"independent continuity")
ratio=b["coarse_record_ledger_residual_l1_per_component"]/b["record_ledger_residual_l1_per_component"];ck(14<ratio<18,"fourth-order-consistent refinement");ck(b["current_refinement_linf"]<3e-11 and b["state_refinement_linf"]<3e-13 and b["occupation_refinement_linf"]<3e-13,"refinement envelope");ck("REFINED_NUMERICAL_CURRENT_INTEGRATION" in b["classification"] and "EXACT_CURRENT_QUADRATURE" in b["not_claimed"],"numerical not exact")
ck(b["ctp_bookkeeping"]=="ONE_DEFORMATION_SOURCE_PER_UNIQUE_EDGE__Z_0_0_EQUALS_ONE" and a["ctp_Z00"]==1,"owner-once CTP")
note=(T/"RUN_OBSERVATION.md").read_text();src=(T/"compute_connected_l8.py").read_text();ck(all(s in note for s in ("48 GiB","55.522473084 s","73,613,312","70.203125 MiB","not a universal runtime or\ncomplexity claim")),"resource observation custody");ck("int.bit_count" in note and "It wrote no\n`RESULT.json`" in note and ".bit_count(" not in src and 'bin(word).count("1")' in src,"Python compatibility custody note")
ck(a["conditional"]=="SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","conditional inputs");ck(a["scope"]=="NO_EXACT_QUADRATURE_DEFECT_GRID_CONTINUUM_WARD_CRITICAL_PHASE_GRAVITON_GRAVITY","claim ceiling");ck("No correction required" in (H/"AUDIT_REPORT.md").read_text(),"audit disposition")
print(f"PASS__CONNECTED_L8_HOSTILE_AUDIT__{n}/{n}")
