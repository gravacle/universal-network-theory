"""Independent static inspection of the material code hidden by B0's GEO pin map. No imports of reviewed code."""
import ast,datetime,hashlib,json,re
from pathlib import Path
B=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');O=B/'review_v010r4_cx2';hashes={}
def read(p):
 x=p.read_bytes();hashes[str(p)]=hashlib.sha256(x).hexdigest();return x.decode()
def functions(t):return {n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,ast.FunctionDef)}
o=read(B/'kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py');n=read(B/'stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py')
a={m[0]:m[1] for m in re.findall(r"'(\w+)': \(BIND6 / '(stages/[^']+)', '[0-9a-f]{64}'\)",o)};z={m[0]:m[1] for m in re.findall(r"'(\w+)': \(BIND7 / '(stages/[^']+)', '[0-9a-f]{64}'\)",n)}
rows=[]
for k in a:
 p=B/'ngc_f10_c2/route_b_v006'/a[k];q=B/'stage_successor_gal_c2v005'/z[k];ta=ast.parse(read(p));tb=ast.parse(read(q));fa=functions(ta);fb=functions(tb);changed=[x for x in fa if fa[x]!=fb.get(x)];added=list(set(fb)-set(fa));removed=list(set(fa)-set(fb));ad=[ast.unparse(next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='admit_config')) for t in [ta,tb]]
 rows.append(dict(stage=k,parent=str(p),successor=str(q),changed_functions=changed,added_functions=added,removed_functions=removed,identical_numerical_functions=(changed==['admit_config'] and not added and not removed),admission_pair=ad))
with (O/'GEO_MAP_EVIDENCE_V001.json').open('x') as f:json.dump({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'resource_waiver':'nice unavailable (sandbox); 0514 waiver','status':'TESTED static AST','rows':rows,'input_sha256':hashes},f,indent=2);f.write('\n')
print(json.dumps({'stage_pairs':len(rows),'numerical_function_AST_identity':sum(r['identical_numerical_functions'] for r in rows),'admission_pair_example':rows[0]['admission_pair']},indent=2))
