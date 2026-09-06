#!/usr/bin/env python3
"""Custody, warning, numerical result, and scope checks for ladder audit."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
TARGET=HERE.parent/"DEVELOPMENT_R_CONNECTED_L8_LADDER_CIRCUIT_V001"
EXPECTED={
 "README.md":"396135f3ae44e8b2cb7df491b968f48465fbe6f3507d5014979c3ccc15478583",
 "RESULT.json":"d25b0fbee3b077d5c3f503d8c970c668843046882e7924936d976517a6d22f81",
 "THEOREM.md":"46cd0eb4372ba0cf983435988928b2f291021a63944fe9d5c83d1bcded76f360",
 "compute_ladder_circuit.py":"b8f060d4ac61f488a24816f0fa7dd0a03a992e88f1fbec4000fd1297a70d05c8",
}
checks=0
def check(v,label):
 global checks
 if not v: raise AssertionError(label)
 checks+=1
for name,digest in EXPECTED.items():
 check(hashlib.sha256((TARGET/name).read_bytes()).hexdigest()==digest,"custody "+name)
check("compute_ladder_circuit" not in (HERE/"independent_reconstruction.py").read_text(),
      "no target import")
env=os.environ.copy(); env["PYTHONWARNINGS"]="error"
target=subprocess.run([sys.executable,"-B",str(TARGET/"compute_ladder_circuit.py")],
 capture_output=True,text=True,check=True,env=env)
check("PASS__R_CONNECTED_L8_LADDER_CIRCUIT__12/12" in target.stdout,
      "warning-free target")
payload=json.loads(target.stdout[:target.stdout.rfind("\nPASS__")])
hard=json.loads((TARGET/"RESULT.json").read_text())
for key in ("active_edge_count","clusters_in_L8_tiling","current_definition",
            "terminal_instrument","attachment","coordinate_status","classification"):
 check(hard[key]==payload[key],"hard field "+key)
for key,tol in (("L8_total_retained_final",3e-13),
                ("absolute_owned_throughput_per_cluster",5e-13),
                ("record_ledger_residual_l1_per_cluster",1e-13),
                ("record_ledger_residual_linf_per_cluster",1e-13)):
 check(abs(hard[key]-payload[key])<tol,"hard numeric "+key)
check(len(hard["gate_records"])==72 and len(hard["cumulative_edge_currents"])==24,
      "hard owner census")

ind=subprocess.run([sys.executable,"-B",str(HERE/"independent_reconstruction.py")],
 capture_output=True,text=True,check=True,env=env)
check("PASS_CONTROLLED_NUMERICAL_FINITE_CIRCUIT__" in ind.stdout,"independent run")
r=json.loads((HERE/"INDEPENDENT_RESULT.json").read_text())
check(r["disposition"]=="PASS_CONTROLLED_NUMERICAL_FINITE_CIRCUIT","pass")
check((r["clusters"],r["heads"],r["supports"],r["gate_records"])==(16,256,24,72),
      "finite census")
check(min(abs(x) for x in r["rung_currents"])>1e-4,"all rungs active")
check(abs(r["retained_L8"]-128)<2e-12,"retention")
check(abs(r["throughput_per_cluster"]-hard["absolute_owned_throughput_per_cluster"])<5e-13,
      "throughput")
check(r["residual_l1"]<2e-12 and r["residual_linf"]<3e-13,"residuals")
check(r["max_gate_ledger_error"]<1e-13,"gate ledgers")
check(r["coordinate_status"]=="FINITE_ENUMERATION__NOT_PHYSICAL_GRID","no grid")
check(r["defect_continuum_critical_Ward_gravity"]=="NOT_PROMOTED","scope")
report=(HERE/"AUDIT_REPORT.md").read_text()
for tok in ("PASS_CONTROLLED_NUMERICAL_FINITE_CIRCUIT","65,536-state",
 "all 72","all eight physical","not a bare-F3","no physical grid",
 "simultaneous Hamiltonian evolution","No material defect"):
 check(tok in report,"report "+tok)
print(f"PASS__LADDER_CIRCUIT_HOSTILE_AUDIT__{checks}/{checks}")
