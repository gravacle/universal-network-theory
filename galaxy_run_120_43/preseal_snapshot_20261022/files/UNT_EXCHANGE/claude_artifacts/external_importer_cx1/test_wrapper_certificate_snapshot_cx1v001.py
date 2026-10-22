"""Exact wrapper method with declared synthetic context/policy/identity/inventory.
Not a test of production policy, driver, mapper, or state derivation.
"""
import ast,hashlib,json,types,sys
from pathlib import Path
root=Path(__file__).resolve().parent
# Reuse fixture construction only; no prior test report is executed or carried.
helper=root/'test_real_guard_snapshot_cx1v001.py'
helper_raw=helper.read_bytes()
cut=helper_raw.decode().split("args={'expected_custody'",1)[0]
exec(compile(cut,str(helper),'exec'),globals())
wrapper=root.parent/'h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py'
wr=wrapper.read_bytes()
assert hashlib.sha256(wr).hexdigest()=='7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229'
tree=ast.parse(wr)
context=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Context')
method=next(n for n in context.body if isinstance(n,ast.FunctionDef) and n.name=='certificate_check')
W=types.ModuleType('_private_wrapper_method');W.__file__=str(wrapper)
O=types.ModuleType('_private_io');O.__file__=str(case/'io.py')
exec("import json,hashlib,types\nfrom pathlib import Path\ndef load_json_file(p,label):return json.loads(Path(p).read_bytes())\ndef sha256_file(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()\ndef sha256_bytes(b):return hashlib.sha256(b).hexdigest()\ndef read_pinned(pin,label):\n b=Path(pin['path']).read_bytes()\n if sha256_bytes(b)!=pin['sha256']:raise ValueError('pin')\n return b\ndef load_pinned_module(pin,name,label):\n b=read_pinned(pin,label);m=types.ModuleType(name);m.__file__=pin['path'];exec(compile(b,pin['path'],'exec'),m.__dict__);return m",O.__dict__)
parent=root.parent/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py'
parent_raw=parent.read_bytes()
assert hashlib.sha256(parent_raw).hexdigest()=='c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'
finish=next(n for n in ast.parse(parent_raw).body if isinstance(n,ast.FunctionDef) and n.name=='finish_binding')
O.os=__import__('os')
exec(compile(ast.Module(body=[finish],type_ignores=[]),str(parent),'exec'),O.__dict__)
M=types.ModuleType('_private_core_io');M.__file__=str(case/'core_io.py');M.O=O;M.digest=G.digest;M.canonical=G.canonical
exec("import json\ndef pin_doc(pin,label):return json.loads(O.read_pinned(pin,label))",M.__dict__)
monpath=root.parent/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'
monraw=monpath.read_bytes();assert hashlib.sha256(monraw).hexdigest()=='ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'
monitor=types.ModuleType('_private_monitor');monitor.__file__=str(monpath);exec(compile(monraw,str(monpath),'exec'),monitor.__dict__)
def codefile(name,text):
 p=case/name;b=text.encode()
 with p.open('xb') as f:f.write(b)
 return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest()}
deriver=codefile('derive.py','def derive_custody(**kw):return '+repr(custody)+'\n')
enumerator=codefile('enumerate.py','def consumed_states(**kw):return '+repr({'complete':True,'states':[state]})+'\n')
rho_obj={'schema':'UNT_POINT_RHO_NUMERICAL_CX2V001','gate':'RHO_G','identity':identity,'point_sha256':G.digest(identity),'custody':custody,'settings':'registered','coverage_complete':True,'required_coverage_inverse_kpc':edge,'full_registered_search_executed':True,'shells':[{'range_inverse_kpc':[4,edge],'rho':1e-6}]}
rho=put(case/'rho.json',rho_obj);eps_slot=put(case/'eps_slot.json',{'inert':True})
eps2=put(case/'eps_bound.json',dict(json.loads(Path(eps['path']).read_bytes()),driver_certificate=eps_slot))
los=put(case/'lo_slot_proof.json',proof('LO_RHO_SLOT',driver_certificate=rho))
lo_core=put(case/'lo_core.json',{'schema':'UNT_POINT_LO_NUMERICAL_CX2V001','kind':'CURRENT_SAVED_STATE','state':state,'rho':rho_obj})
lo2=put(case/'lo_bound.json',dict(json.loads(Path(lo['path']).read_bytes()),core_record=lo_core))
b= {'schema':G.SCHEMA,'identity':identity,'custody':custody,'domain':{'K_inverse_kpc':4.0,'K_big_inverse_kpc':128.0},'prelaunch':{'EPS':eps2,'GQ':gq,'LO_RHO_SLOT':los},'acceptance_rule':'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED','states':[{'state':state,'LO':lo2}],'driver_certificate_bindings':{'eps_certificate':eps_slot,'lo_certificate':rho}}
bound=put(case/'bound_bundle.json',b)
record={'identity':identity,'bundle':bound,'eps_certificate':eps_slot,'lo_certificate':rho}
spec=json.loads(json.dumps(identity));spec['numerics']['uv_tail'].update(b['driver_certificate_bindings'])
call=case/'direct';(call/'out/inputs').mkdir(parents=True)
sp=put(call/'spec.json',spec);put(call/'out/inputs/call_spec.json',spec)
driver_sha='a'*64
result={'status':'COMPLETED','driver_sha256':driver_sha,'call_spec_sha256':sp['sha256']}
rp=put(call/'out/result.json',result)
put(call/'out/finish.json',{'result_path':rp['path'],'result_sha256':rp['sha256']})
receipt={'schema':monitor.RECEIPT_SCHEMA,'status':'FINISHED','driver_status':'COMPLETED','pins':{'spec':sp,'driver':{'sha256':driver_sha}},'result':rp}
receipt['receipt_sha256']=hashlib.sha256(monitor.canonical(receipt).encode()).hexdigest();put(call/'RECEIPT.json',receipt)
put(call/'TAIL_CERTIFICATE_ACCEPTANCE.json',{'schema':'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001','result_sha256':rp['sha256'],'call_spec_sha256':sp['sha256'],'certificate_bundle':bound,'prelaunch_bundle':bound})
W.__dict__.update(Path=Path,json=json,O=O,M=M,G=G,Error=ValueError,DRIVER_SHA=driver_sha,validate_block=lambda n:None,point_identity=lambda s:identity)
exec(compile(ast.Module(body=[method],type_ignores=[]),str(wrapper),'exec'),W.__dict__)
ctx=types.SimpleNamespace(numerics=spec['numerics'],cfg={'tail_readiness':{'custody_deriver':deriver,'state_enumerator':enumerator,'approved_certificate_producers':[producer]}},M=monitor,certificate_policy_gate=lambda:{'ok':True},certificate_record=lambda ident:record)
baseline=W.certificate_check(ctx,spec,'acceptance',result=result,call_dir=call)
assert baseline['ok'],baseline
active=False;reads={}
def audit(event,args):
 if active and event=='open' and isinstance(args[0],str) and args[0].startswith(str(case)+'/'):reads[args[0]]=reads.get(args[0],0)+1
sys.addaudithook(audit)
snap=Snapshot();active=True
with ReadOnlyScope(snap,[W,O,M,G,monitor]):
 got=W.certificate_check(ctx,spec,'acceptance',result=result,call_dir=call)
active=False
assert got==baseline,(got,baseline)
assert max(reads.values())==1,reads
passed=['exact wrapper method baseline','snapshot result equality','OS read count max one including dynamic modules']
with ReadOnlyScope(Snapshot(),[W,O,M,G,monitor]):
 bad=W.certificate_check(ctx,spec,'acceptance',result=dict(result,driver_sha256='b'*64),call_dir=call)
assert not bad['ok'];passed.append('wrong result driver refused')
ctx.certificate_record=lambda ident:None
with ReadOnlyScope(Snapshot(),[W,O,M,G,monitor]):bad=W.certificate_check(ctx,spec,'acceptance',result=result,call_dir=call)
assert not bad['ok'];passed.append('unregistered point refused')
report={'status':'PASS','blocking_count':0,'scope':'Exact wrapper certificate_check method with synthetic context and proof data','tested':passed,'files_read_once':len(reads),'substitutions':['validate_block no-op','point_identity fixed fixture identity','policy gate true','registry fixture record','synthetic custody and complete state enumerator','fixture driver hash'], 'untested':['production policy/identity/driver/state enumeration','full Context initialization','whole engine','F6','entry integration'], 'pins':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [wrapper,parent,source,helper,Path(__file__)]]}
with (case/'WRAPPER_TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(case/'WRAPPER_TEST_REPORT.json')
