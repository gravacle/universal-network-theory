import ast,hashlib,json,os,re,subprocess,types
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
base=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1')
out=base/'dispositions_controls_v001';out.mkdir()
helper=base/'provisional_snapshot_v001/helper.py';hb=helper.read_bytes();assert sha(hb)=='2f08fb88c17dbe340fe5f03da10ed510aff384cdb404d8e3d9544664d2d79172'
tool=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v001/check_frozen_addendum_c4v003.py');tb=tool.read_bytes();assert sha(tb)=='72d9191d064e61e0a3f6d40d04848971d1babd852236ddae4da36b8ca910a612'
# Pure tool disposition validator only; no module import, prereg or live data access.
names={'DISPOSITIONS_KEYS','DISPOSITION_ROW_KEYS','DISPOSITION_CHANGE_KEYS','DISPOSITION_VALUES','DISPOSITION_ENTRY_RX'}
tree=ast.parse(tb);selected=[n for n in tree.body if (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets)) or (isinstance(n,ast.FunctionDef) and n.name=='disposition_codes')]
C=types.SimpleNamespace(DISPOSITIONS_SCHEMA='UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001',sha_bytes=sha)
tns={'re':re,'C':C};exec(compile(ast.Module(body=selected,type_ignores=[]),str(tool),'exec'),tns)
ns={'__name__':'inert_dispositions_review','__file__':str(helper)};exec(compile(hb,str(helper),'exec'),ns)
section=b'## A102: Inert later section\nThis fixture names no real science.\n';fsha='1'*64
obj={'schema':C.DISPOSITIONS_SCHEMA,'frozen_addendum_sha256':fsha,'entries':[{'entry':'A102','disposition':'no_change','reason':'Inert fixture outside the cited synthetic table.','section_sha256':sha(section)}]}
raw=(json.dumps(obj,indent=2)+'\n').encode();path=out/'inert_dispositions.json'
with path.open('xb') as f:f.write(raw)
class Checker:
 def __init__(self):self.failures=[]
 def fail(self,code,detail):self.failures.append({'code':code,'detail':detail})
chk=Checker();seen=tns['disposition_codes'](chk,obj,fsha,{102:[('unused',section)]},{102},{},{},{102},101)
a=types.SimpleNamespace(dispositions=str(path),dispositions_sha=sha(raw))
try:ns['_dispositions'](a);outcome='ACCEPTED'
except ns['Refuse'] as e:outcome=str(e)
checks=[{'id':'v003_pure_validator_accepts_contract_shape','passed':not chk.failures and seen=={102},'failures':chk.failures}, {'id':'helper007_refuses_same_shape_before_any_frozen_prereg_input','passed':outcome=='DISPOSITIONS_NOT_A_LIST','actual':outcome}, {'id':'priority_nice10','passed':os.getpriority(os.PRIO_PROCESS,0)>=10}]
result={'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'label':'TESTED_INERT_INTERFACE_MISMATCH','finding':'SA-CX1-B3','verdict':'FAIL_INTERFACE' if all(c['passed'] for c in checks) else 'CONTROL_FAILED','checks':checks,'helper':{'path':str(helper),'sha256':sha(hb),'lines':[239,242]},'v003_tool1':{'path':str(tool),'sha256':sha(tb),'lines':[43,146,161]},'fixture':{'path':str(path),'sha256':sha(raw)},'harness':{'path':__file__,'sha256':sha(Path(__file__).read_bytes())},'scope':'Only copied helper plus extracted pure validator. No real script/comparator, protected run, observed target or native Context. Current provisional snapshot only.'}
rp=out/'RESULTS.json'
with rp.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'verdict':result['verdict'],'controls_passed':sum(c['passed'] for c in checks),'total':len(checks),'result':str(rp),'sha256':sha(rp.read_bytes())}))
