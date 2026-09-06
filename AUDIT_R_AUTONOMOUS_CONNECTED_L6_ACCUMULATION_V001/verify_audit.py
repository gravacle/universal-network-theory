#!/usr/bin/env python3
"""Hostile replay and independent cross-check for the connected L6 packet."""
import hashlib,json,os,subprocess,sys
from pathlib import Path

H=Path(__file__).parent
T=H.parent/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001"
n=0
def ck(v,msg):
 global n
 if not v: raise AssertionError(msg)
 n+=1
def near(a,b,tol,msg): ck(abs(float(a)-float(b))<=tol,msg)
def vmax(a,b): return max(abs(float(x)-float(y)) for x,y in zip(a,b))

pins={
 "README.md":"63d09b574abe488ce9f8be033421387a6f7728e4d24761c51e9c279ff08118df",
 "RESULT.json":"e601f1a206eeb90eb3861587133bfc30ca9974e521a06031b8ee4ca5eff86f14",
 "THEOREM.md":"10fc1956c0c0fc4d60bac3bf788f1a5a774cc4352babec5ca4e9cbadce9aabfb",
 "compute_connected_l6.py":"00206db522631821eb10c0aa8815ff5cc7ec349997aa30b8ae5a73bd78bab87a",
}
for f,h in pins.items(): ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==h,"target custody: "+f)
env=os.environ.copy();env["PYTHONWARNINGS"]="error"
for _ in range(2):
 r=subprocess.run([sys.executable,"-B",str(T/"compute_connected_l6.py")],capture_output=True,text=True,check=True,env=env)
 ck("__20/20" in r.stdout,"target suite")
 ck(hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==pins["RESULT.json"],"canonical replay custody")
r=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env)
ck("PASS_L6_RK4_INDEPENDENT" in r.stdout,"independent RK4 replay")
a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text())

# Independent component graph: simple, connected, and degree three.
edges=[(i,(i+1)%6) for i in range(6)]+[(6+i,6+(i+1)%6) for i in range(6)]+[(i,6+(i+1)%6) for i in range(6)]
ck(len(edges)==len(set(tuple(sorted(e)) for e in edges))==18,"18 unique edges")
deg=[0]*12;adj=[set() for _ in range(12)]
for u,v in edges: deg[u]+=1;deg[v]+=1;adj[u].add(v);adj[v].add(u)
seen={0};todo=[0]
while todo:
 u=todo.pop()
 for v in adj[u]-seen: seen.add(v);todo.append(v)
ck(seen==set(range(12)) and deg==[3]*12,"connected cubic component")
c=a["census"]
ck((c["components"],c["sites_global"],c["sites_per_F3_layer"],c["possible_F3_links"])==(18,216,108,11664),"global site/link census")
ck((c["selected_edges_global_owner_once"],c["prepared_source_lineages"],c["expected_retained_global"])==(324,108,54),"owner/source/retained census")

ck(vmax(a["q_before"],b["q_before"])<2e-12 and vmax(a["q_after"],b["q_after"])<2e-12,"all occupations")
ck(vmax(a["integrated_oriented_currents"],b["integrated_oriented_currents"])<2e-12,"all 18 current values and signs")
for k in ("absolute_oriented_throughput_per_component","absolute_oriented_throughput_global","absolute_connector_throughput_per_component","absolute_connector_throughput_global","max_abs_connected_edge_correlation","expected_retained_global"):
 near(a[k],b[k],2e-10,"observable: "+k)
near(a["L6_over_L4_total_throughput_ratio"],b["L6_over_L4"]["throughput_total"],2e-10,"L6/L4 total")
near(a["L6_over_L4_per_retained_ratio"],b["L6_over_L4"]["throughput_per_retained_record"],2e-10,"L6/L4 per retained")
ck(a["norm_error"]<2e-12 and a["energy_error"]<2e-12 and a["number_law"]<2e-12,"independent conserved quantities")
ck(a["residual_l1"]<2e-11 and a["residual_linf"]<2e-12,"independent continuity residual")

# One 1024/2048 pair is a refinement diagnostic.  The residual reduction is
# consistent with Simpson's fourth order; it is not an exactness proof.
ratio=b["coarse_record_ledger_residual_l1_per_component"]/b["record_ledger_residual_l1_per_component"]
ck(14.0<ratio<18.0,"coarse/fine residual is fourth-order-consistent")
ck(b["current_refinement_linf"]<2e-11 and b["state_refinement_linf"]<2e-13 and b["occupation_refinement_linf"]<2e-13,"refinement envelope")
ck("REFINED_NUMERICAL_CURRENT_INTEGRATION" in b["classification"] and "EXACT_CURRENT_QUADRATURE" in b["not_claimed"],"numerical not exact")
ck(b["ctp_bookkeeping"]=="ONE_DEFORMATION_SOURCE_PER_UNIQUE_EDGE__Z_0_0_EQUALS_ONE" and a["ctp_Z00"]==1.0,"finite owner-once CTP normalization")
ck(a["conditional"]=="SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","conditional inputs")
ck(a["scope"]=="NO_EXACT_QUADRATURE_DEFECT_GRID_CONTINUUM_WARD_CRITICAL_PHASE_GRAVITY","forbidden promotion absent")
ck("No correction required" in (H/"AUDIT_REPORT.md").read_text(),"report disposition")
print(f"PASS__CONNECTED_L6_HOSTILE_AUDIT__{n}/{n}")
