#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;T=H.parent/"DEVELOPMENT_R_PHYSICAL_PARENT_SUPPORT_SELECTION_SCREEN_V001";c=0
def ck(v,s):
 global c
 if not v:raise AssertionError(s)
 c+=1
X={"README.md":"406c6742ad7e13ae79468751d4f96dfc8c1aabd82e612c9fc9d16dbe36508e44","RESULT.json":"ebd422320950281f0b62fdf71d2bad59865fd51ec19f954ca043734d04e66a3e","THEOREM.md":"871447192f3d2ffc036ad6a5764d3975eafa3b131aa0e9afaa085e9a53b90dc0","compute_support_selection_screen.py":"b04ac597197e7e1e4adbbf0663932a3cc04d1fd67dcab86d5cf4c40ce775eeb4"}
for f,x in X.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==x,"custody")
e=os.environ.copy();e["PYTHONWARNINGS"]="error";o=subprocess.run([sys.executable,"-B",str(T/"compute_support_selection_screen.py")],capture_output=True,text=True,check=True,env=e);ck("__29/29" in o.stdout,"target");o=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=e);ck("PASS_SUPPORT_SELECTION_INDEPENDENT__18/18" in o.stdout,"independent")
a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text())
for x,y in zip(a["rows"],b["rows"]):ck(all(x[k]==y[k] for k in y),"rows")
s=a["small_exact_transverse_example"];t=b["small_exact_transverse_example"];ck(max(abs(s[k]-t[k]) for k in t)<2e-11,"K33");ck(a["incidence_commutators"]==b["incidence_commutators"],"commutators");ck(a["degree_two_window"]=="U_D>0_AND_0<DELTA<2U_D","window");ck("DISTINGUISHING_LINEAGE_OR_PORT_IS_ADDITIONAL_CONDITIONAL_SELECTOR_DATA" in a["anchoring_boundary"],"anchoring");ck("NO_PHYSICAL_GRID_DEFECT_CONTINUUM_WARD_GRAVITY"==a["scope"],"scope")
report=(H/"AUDIT_REPORT.md").read_text();ck("No correction is required before promotion" in report and "additional conditional selector data" in report,"logic report")
print(f"PASS__SUPPORT_SELECTION_HOSTILE_AUDIT__{c}/{c}")
