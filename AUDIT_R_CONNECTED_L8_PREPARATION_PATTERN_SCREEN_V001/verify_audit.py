#!/usr/bin/env python3
"""Custody, independent four-pattern, label-swap, and scope verifier."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent; TARGET=ROOT/"DEVELOPMENT_R_CONNECTED_L8_PREPARATION_PATTERN_SCREEN_V001"; DEPTH=ROOT/"DEVELOPMENT_R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY_V001"
EXPECTED={"README.md":"0f6b5998b21a16d8e9e3cdda6a7c035ab2869afb0063446fb7a48338b32873f3","RESULT.json":"67a60a68dafcf800a32bed1eadab9e9635f154dd103487694d1f8e9285826a28","THEOREM.md":"e3e3bcb3e911dfa708398595874612ed4db4b9ab3fdc8165afbabe17a6ba67e9","compute_preparation_screen.py":"83beedadb9f0b3a2f3a2ec66ade89ec69bcebe9e7d3e2b9410cf1a1557c69387"}
checks=0
def check(v,label):
 global checks
 if not v: raise AssertionError(label)
 checks+=1
for name,d in EXPECTED.items(): check(hashlib.sha256((TARGET/name).read_bytes()).hexdigest()==d,"custody "+name)
check("compute_preparation_screen" not in (HERE/"independent_reconstruction.py").read_text(),"no target import")
env=os.environ.copy(); env["PYTHONWARNINGS"]="error"
t=subprocess.run([sys.executable,"-B",str(TARGET/"compute_preparation_screen.py")],capture_output=True,text=True,check=True,env=env)
check("PASS__R_CONNECTED_L8_PREPARATION_PATTERN_SCREEN__16/16" in t.stdout,"warning-free target")
check(hashlib.sha256((TARGET/"RESULT.json").read_bytes()).hexdigest()==EXPECTED["RESULT.json"],"deterministic target")
i=subprocess.run([sys.executable,"-B",str(HERE/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env)
check("PASS_CONTROLLED_NUMERICAL_PREPARATION_SCREEN__14/14" in i.stdout,"independent run")
h=json.loads((TARGET/"RESULT.json").read_text()); r=json.loads((HERE/"INDEPENDENT_RESULT.json").read_text())
check((r["clusters"],r["heads"],r["support_count"],r["rung_count"],r["events_per_pattern"],r["total_events"])==(16,256,24,8,72,288),"census")
nums=("expected_retained_per_cluster","L8_expected_retained","first_ring_expected_retained","second_ring_expected_retained","gate_event_absolute_traffic","cumulative_net_edge_throughput","cumulative_net_inter_ring_throughput","max_abs_connected_edge_correlation","record_ledger_residual_l1_per_cluster","record_ledger_residual_linf_per_cluster","norm_error","number_law_max_change")
for a,b in zip(r["patterns"],h["patterns"]):
 check(a["preparation_pattern"]==b["preparation_pattern"] and a["onsite_weights"]==b["onsite_weights"] and a["active_cumulative_edge_count"]==b["active_cumulative_edge_count"] and a["active_cumulative_inter_ring_edge_count"]==b["active_cumulative_inter_ring_edge_count"],"pattern exact fields")
 check(max(abs(a[k]-b[k]) for k in nums)<5e-13 and max(abs(x-y) for x,y in zip(a["q_final"],b["q_final"]))<5e-13,"pattern numerics")
for a,b in zip(r["pairwise_pattern_comparisons"],h["pairwise_pattern_comparisons"]): check(a["first"]==b["first"] and a["second"]==b["second"] and max(abs(a[k]-b[k]) for k in ("terminal_distribution_total_variation","state_fidelity","occupation_l1_distance"))<5e-13,"pairwise")
check(max(abs(r["envelope"][k]-h["envelope"][k]) for k in h["envelope"])<5e-13,"envelope")
same=r["patterns"][0]; check(same["active_cumulative_inter_ring_edge_count"]==0 and same["active_cumulative_edge_count"]==16 and same["cumulative_net_edge_throughput"]>1,"same control")
check(all(x["active_cumulative_inter_ring_edge_count"]==8 and x["active_cumulative_edge_count"]==24 for x in r["patterns"][1:]),"asymmetric activation")
swap=r["first_second_ring_label_swap_control"]; check(swap["terminal_distribution_total_variation_after_ring_swap"]<2e-14 and swap["occupation_l1_after_ring_swap"]<2e-13,"ring-label equivalence")
depth=json.loads((DEPTH/"RESULT.json").read_text())["trajectory"][3]; rev=r["patterns"][1]
keys=("L8_expected_retained","expected_retained_per_cluster","first_ring_expected_retained","second_ring_expected_retained","gate_event_absolute_traffic","cumulative_net_edge_throughput","cumulative_net_inter_ring_throughput","max_abs_connected_edge_correlation","record_ledger_residual_l1_per_cluster","record_ledger_residual_linf_per_cluster","norm_error","number_law_max_change")
check(max(abs(rev[k]-depth[k]) for k in keys)<5e-13 and rev["active_cumulative_edge_count"]==depth["active_cumulative_edge_count"]==24 and rev["active_cumulative_inter_ring_edge_count"]==depth["active_cumulative_inter_ring_edge_count"]==8,"reversed prior consistency")
e=r["envelope"]; check(e["max_record_ledger_residual_l1_per_cluster"]<5e-14 and e["max_record_ledger_residual_linf_per_cluster"]<7e-15 and e["max_abs_L8_retained_change"]<5e-13 and e["max_norm_error"]<2e-14 and e["max_number_law_change"]<3e-15,"controls")
check(r["terminal_instrument"]=="COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM" and r["attachment"]=="INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED","read attachment")
check(r["conclusion"]=="ASYMMETRY_NECESSARY_ONLY_FOR_THIS_FIXED_SYMMETRIC_CIRCUIT__NO_PREFERRED_PREPARATION_MEASURE_OR_AVERAGING" and r["coordinate_status"]=="FINITE_ENUMERATION__NOT_PHYSICAL_GRID" and r["defect_continuum_critical_Ward_gravity"]=="NOT_PROMOTED","scope")
report=(HERE/"AUDIT_REPORT.md").read_text()
for tok in ("No material defect or repair","288 total","zero active rungs","16 ring supports","exact permutation","only in this fixed symmetric circuit","No generic necessity","not a physical grid","Ward","gravity claim"): check(tok in report,"report "+tok)
print(f"PASS__PREPARATION_PATTERN_HOSTILE_AUDIT__{checks}/{checks}")
