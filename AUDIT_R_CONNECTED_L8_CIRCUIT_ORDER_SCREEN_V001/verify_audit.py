#!/usr/bin/env python3
"""Hostile custody, independent numerical, forward-consistency, and scope audit."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent; TARGET=ROOT/"DEVELOPMENT_R_CONNECTED_L8_CIRCUIT_ORDER_SCREEN_V001"; DEPTH=ROOT/"DEVELOPMENT_R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY_V001"
EXPECTED={"README.md":"70611e603751c17b90dc900e02c5c71b0f1acbd1d06b4b50cae4d8759f54f0d1","RESULT.json":"0ceb0c10df2ad03e5ec264d6fe27c9bde2bf15f8f9ea7af25bebe187aacc266a","THEOREM.md":"4079f52477b79aeb5b90444fbf46cefc828cb6b9c577299eef41f7138fad2fba","compute_order_screen.py":"b4dee89c54cdf50779b35a1030449236be7b025c07f899de91f09c585e83dd83"}
checks=0
def check(v,label):
 global checks
 if not v: raise AssertionError(label)
 checks+=1
for name,d in EXPECTED.items(): check(hashlib.sha256((TARGET/name).read_bytes()).hexdigest()==d,"custody "+name)
check("compute_order_screen" not in (HERE/"independent_reconstruction.py").read_text(),"no target import")
env=os.environ.copy(); env["PYTHONWARNINGS"]="error"
t=subprocess.run([sys.executable,"-B",str(TARGET/"compute_order_screen.py")],capture_output=True,text=True,check=True,env=env)
check("PASS__R_CONNECTED_L8_CIRCUIT_ORDER_SCREEN__14/14" in t.stdout,"warning-free target")
check(hashlib.sha256((TARGET/"RESULT.json").read_bytes()).hexdigest()==EXPECTED["RESULT.json"],"deterministic target")
i=subprocess.run([sys.executable,"-B",str(HERE/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env)
check("PASS_CONTROLLED_NUMERICAL_ORDER_SCREEN__12/12" in i.stdout,"independent run")
h=json.loads((TARGET/"RESULT.json").read_text()); r=json.loads((HERE/"INDEPENDENT_RESULT.json").read_text())
check((r["clusters"],r["heads"],r["unique_supports"],r["rungs"],r["events_per_order"],r["total_events"])==(16,256,24,8,72,216),"census")
nums=("expected_retained_per_cluster","L8_expected_retained","first_ring_expected_retained","second_ring_expected_retained","gate_event_absolute_traffic","cumulative_net_edge_throughput","cumulative_net_inter_ring_throughput","max_abs_connected_edge_correlation","record_ledger_residual_l1_per_cluster","record_ledger_residual_linf_per_cluster","norm_error","number_law_max_change")
for a,b in zip(r["orders"],h["orders"]):
 check(a["order"]==b["order"] and a["edge_sequence"]==b["edge_sequence"] and a["active_cumulative_edge_count"]==b["active_cumulative_edge_count"] and a["active_cumulative_inter_ring_edge_count"]==b["active_cumulative_inter_ring_edge_count"],"order exact fields")
 check(max(abs(a[k]-b[k]) for k in nums)<5e-13 and max(abs(x-y) for x,y in zip(a["q_final"],b["q_final"]))<5e-13,"order numerics")
for a,b in zip(r["pairwise_order_comparisons"],h["pairwise_order_comparisons"]):
 check(a["first"]==b["first"] and a["second"]==b["second"] and max(abs(a[k]-b[k]) for k in ("terminal_distribution_total_variation","state_fidelity","occupation_l1_distance"))<5e-13,"pairwise")
check(max(abs(r["envelope"][k]-h["envelope"][k]) for k in h["envelope"])<5e-13,"envelope")
depth=json.loads((DEPTH/"RESULT.json").read_text())["trajectory"][3]; f=r["orders"][0]
forward_map={"L8_expected_retained":"L8_expected_retained","expected_retained_per_cluster":"expected_retained_per_cluster","first_ring_expected_retained":"first_ring_expected_retained","second_ring_expected_retained":"second_ring_expected_retained","gate_event_absolute_traffic":"gate_event_absolute_traffic","cumulative_net_edge_throughput":"cumulative_net_edge_throughput","cumulative_net_inter_ring_throughput":"cumulative_net_inter_ring_throughput","max_abs_connected_edge_correlation":"max_abs_connected_edge_correlation","record_ledger_residual_l1_per_cluster":"record_ledger_residual_l1_per_cluster","record_ledger_residual_linf_per_cluster":"record_ledger_residual_linf_per_cluster","norm_error":"norm_error","number_law_max_change":"number_law_max_change"}
check(max(abs(f[a]-depth[b]) for a,b in forward_map.items())<5e-13,"forward depth-3 scalars")
check(f["active_cumulative_edge_count"]==depth["active_cumulative_edge_count"]==24 and f["active_cumulative_inter_ring_edge_count"]==depth["active_cumulative_inter_ring_edge_count"]==8,"forward activity")
e=r["envelope"]; check(e["max_terminal_distribution_total_variation"]>1e-3 and e["min_state_fidelity"]<.999 and e["max_occupation_l1_distance"]>1e-3,"material order dependence")
check(e["max_record_ledger_residual_l1_per_cluster"]<5e-14 and e["max_record_ledger_residual_linf_per_cluster"]<7e-15 and e["max_abs_L8_retained_change"]<5e-13 and e["max_norm_error"]<2e-14 and e["max_number_law_change"]<3e-15,"controls")
check(r["terminal_instrument"]=="COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM" and r["attachment"]=="INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED","read attachment")
check(r["conclusion"]=="SCHEDULE_NECESSARY_SELECTED_PARENT_DATA__NO_PREFERRED_ORDER_OR_AVERAGING_SELECTION_LAW" and r["coordinate_status"]=="FINITE_ENUMERATION__NOT_PHYSICAL_GRID" and r["defect_continuum_critical_Ward_gravity"]=="NOT_PROMOTED","scope")
report=(HERE/"AUDIT_REPORT.md").read_text()
for tok in ("No material defect or repair","216 independently","complete terminal probability","necessary selected-parent data","no preferred order","not a physical grid","not bare-F3","Ward","gravity claim"): check(tok in report,"report "+tok)
print(f"PASS__ORDER_SCREEN_HOSTILE_AUDIT__{checks}/{checks}")
