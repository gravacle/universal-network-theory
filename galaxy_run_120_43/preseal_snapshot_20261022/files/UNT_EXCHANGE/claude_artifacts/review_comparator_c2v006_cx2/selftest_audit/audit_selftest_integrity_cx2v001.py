from pathlib import Path
import json,ast,hashlib,os
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
PKG=A/'tail_scheme_impl_c2/gates_v006'
SYN=PKG/'selftest/out/SELFTEST_C2V006_V001'
ROOT=Path(__file__).parent
SRC=PKG/'run_identity_compare_c2v006.py'
PIN='097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48'
inputs={}
def rd(p):
 p=Path(p)
 assert str(p).startswith(str(PKG/'selftest')) or p==SRC
 assert '/runs/' not in str(p) and '/runs_ext/' not in str(p)
 b=p.read_bytes();inputs[str(p)]=hashlib.sha256(b).hexdigest();return b
def obj(p):return json.loads(rd(p))
def saved(p,want=None):
 p=Path(p);assert p.is_relative_to(SYN)
 b=rd(p)
 if want:assert hashlib.sha256(b).hexdigest()==want,(p,'HASH_MISMATCH')
 return json.loads(b)
assert hashlib.sha256(rd(SRC)).hexdigest()==PIN
summary=obj(SYN/'SELFTEST_C2V006.json');assert summary['comparator']['sha256']==PIN
source=rd(PKG/'selftest/canaries_c2v006.py').decode();tree=ast.parse(source)
contracts={}
for n in ast.walk(tree):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='case' and len(n.args)>=3 and isinstance(n.args[0],ast.Constant):
  name=n.args[0].value;expect=ast.literal_eval(n.args[2])
  owners=ast.literal_eval(n.args[4]) if len(n.args)>4 else ()
  contracts[name]={'expect':expect,'owners':list(owners)}
# Independent owner mapping for the original structural cases; supplied wrapper checks any FAIL only.
sowners={('F%02d'%i):['STAGE_SET'] for i in range(1,8)}
sowners.update({'F08':['STAGES'],'F09':['RESULT'],'F10':['RESULT'],'F11':['RESULT'],'F12':['FILES_INPUTS'],'F13':['FILES_INPUTS'],'F14':['INVENTORY'],'F15':['INVENTORY'],'F16':['FILES_TOP'],'F17':['FILES_TOP'],'F18':['FILES_ROUTE_A'],'F19':['FILES_ROUTE_A']})
aowners={'key_collision':['NORM_INJECTIVE'],'duplicate_json_key':['STRICT_PARSE'],'duplicate_npz_member':['STRICT_PARSE'],'structured_npz':['STAGES'],'structured_npy':['STAGES'],'npz_storage_order':['STAGES'],'npy_storage_order':['STAGES'],'ordinary_result_change':['RESULT'],'ordinary_result_extra':['RESULT']}
rows=[]
def verify(group,driver,row,name,want,owners):
 rp=row.get('report');rep=saved(rp['path'],rp['sha256']) if rp else None
 if want=='MUST_REFUSE':
  ok=rep is None and str(row.get('exception')).startswith('SystemExit: REFUSED: tokens file')
  rows.append({'group':group,'driver':driver,'name':name,'expect':want,'owners':owners,'ok':ok,'failing':[],'detail':'Token parse refusal; no report'});return
 assert rep is not None,(group,name,'NO_REPORT')
 checks=rep['checks'];failed=[k for k,v in checks.items() if v['pass'] is False]
 expected_pass=want in ('PASS','MUST_PASS')
 ok=rep['comparator']['sha256']==PIN and rep['driver_selected']==driver and rep['failing']==failed
 ok=ok and (rep['verdict']=='PASS_BITWISE_EQUAL' if expected_pass else rep['verdict']=='FAIL')
 ok=ok and all(k in checks and checks[k]['pass'] is False for k in owners)
 if not expected_pass:ok=ok and bool(owners)
 if group=='A' and name=='baseline':ok=ok and failed==['NORM_INJECTIVE']
 if name=='key_collision':
  d=checks['NORM_INJECTIVE']['detail']['new']
  ok=ok and any(x.get('kind')=='KEY_COLLISION' and len(x.get('raw_keys',[]))==2 and '<RUN>/x' in x['raw_keys'] for x in d)
 rows.append({'group':group,'driver':driver,'name':name,'expect':want,'owners':owners,'ok':ok,'failing':failed,'report_path':rp['path'],'report_sha256':rp['sha256']})
for group,entries in summary['results'].items():
 if group=='S':continue
 for key,entry in entries.items():
  driver='r5' if key.endswith('r5') else 'r4'
  data=saved(entry['results'],entry['results_sha256'])
  for r in data.get('rows',data.get('cases',[])):
   name=r.get('name',r.get('case'))
   if group=='A':
    want='FAIL' if name=='baseline' else ('PASS' if r['should_pass'] else 'FAIL');owners=['NORM_INJECTIVE'] if name=='baseline' else aowners.get(name,[])
   elif group=='CD':
    contract=contracts[name];assert r['expect']==contract['expect'];assert r['must_fail']==contract['owners'];want=contract['expect'];owners=contract['owners']
   elif key.startswith('structural'):
    want=r['expect'];owners=sowners.get(name[:3],[])
   else:
    want=r['expected'];owners=r['required_failure']
   verify(group,driver,r,name,want,owners)
assert hashlib.sha256(rd(SRC)).hexdigest()==PIN
result={'date_u':os.environ['UNT_CX2_PACKET_UTC'],'source_pin':PIN,'mode':'Source and saved synthetic selftest-report integrity audit only; no comparator rerun by this script, no supplied harness import/execution, no production report/input reads','checks':len(rows),'matched':sum(x['ok'] for x in rows),'mismatches':[x for x in rows if not x['ok']],'rows':rows,'input_pins':inputs,'limitations':['Saved reports are builder-authored; independent reruns belong to counterexamples lane','GroupS source/unit claims not dynamically rerun here','Structural wrapper lacks owning-check assertions; independently checked its19 negative reports per driver by named owner','Original A baseline is policy-redeclared NORM_INJECTIVE-only; A negatives carry this unrelated failure in addition to required owner; independent clean variants are a separate lane']}
p=ROOT/'SELFTEST_INTEGRITY_CX2V001.json'
with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checks':result['checks'],'matched':result['matched'],'mismatches':result['mismatches']}))
