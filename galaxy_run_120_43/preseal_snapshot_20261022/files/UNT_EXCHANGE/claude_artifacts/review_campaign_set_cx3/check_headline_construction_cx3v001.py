"""Codex3 0778: isolated byte-construction comparison, no scientific calls or certificate reads."""
PINS={'producer': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/handoff_v004/tools/produce_final_step4_specs_c4v004.py', 'sha256': 'fcbf1c3ed175e1cfb3519c33324622a3b0ed190769e71b199687bd46dd1cb7ba'}, 'parent': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py', 'sha256': 'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'}, 'core': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py', 'sha256': 'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6'}, 'ledger': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py', 'sha256': '7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229'}, 'r12core': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4/calibration_core_cx2v006r12_c4.py', 'sha256': '192d086348fed9307da99732c0ef146bb336a3d605afc1e9e56b6ce959ad1a73'}, 'r12wrapper': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4/calibration_orchestrator_cx2v006r12_c4_q5b1.py', 'sha256': '381fa2957edabf18032afba9a8ff026744f6cc1d933efb5f3d30f289ea9decb9'}, 'policy': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r10_c4/adoption_policy_cx2v006r10_c4.py', 'sha256': '93d9c0acdb3e9fd40ec63ed0db7c1356b6d2b025eeb5bcde57a2ffebdbd04ba3'}, 'h11': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/h11_evidence_assembler_c2v001.py', 'sha256': '2a8df9dfb85933b0cbe27af791d6966537537aea9e37d90fe82b6106195b33ee'}, 'inventory': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/SPEC_INVENTORY_C4V001.json', 'sha256': '362bb571f65f7b7568ac389941aa08b4ab61ccaf69e35cb9f715199393caedd1'}, 'registry': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json', 'sha256': '2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319'}, 'manifest': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/registry_c2v001/REGISTRY_MANIFEST_31pts_20261020T140004Z.json', 'sha256': '1164bb48d733e613529696c1c6671cb49ad10b0ace2c57a5344e8ad582794eb0'}, 'make_dry': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/tools/make_step4_specs_c4v001.py', 'sha256': 'b87076aca8dd2153c23495dd8a82d96f6eaf29c661354e9597e73d8ec85c2ab0'}, 'post_probe': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/tools/post_adoption_probe_c4v001.py', 'sha256': '620412f1c256fea295ba158611d386ae9827360b861cf3a1b2cc7a5d33726d09'}, 'c4_tests': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/handoff_v004/tools/test_produce_final_step4_specs_c4v004.py', 'sha256': '74b57d7d19298bd5381459fd470999eaa4936b26ce3a4894337cfd70f6a45268'}, 'c4_results': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/handoff_v004/TEST_RESULTS_C4V004.json', 'sha256': 'd9346dc51672692b1cab9cb8e761bbf7a60365b40be863c0563a017e580d6b39'}, 'c4_notes': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/handoff_v004/TEST_NOTES_C4V004.md', 'sha256': '14cad115ba44f7238a5f8e54f9150d46bf8e70ed94d0293db36a78aed4b138d4'}, 'dispatch': {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0778_2026-10-20_codex3_HEADLINE11_spec_construction_authorization.md', 'sha256': 'c67400e2a1f9c4d3ab1e8f1a78317304ab15c71d72e8dad77744cca266d97738'}}

import ast
import copy
import hashlib
import json
import math
from pathlib import Path
from types import SimpleNamespace
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
DRY=A/'step4_launch_readiness_c4/dryplans/specs_v001/specs'
EXPECTED={
'HEADLINE_TRIAL':'f4ae15461f669979e8648e6686f093c6a909988f9cfb122de71b42c073327aff',
'HEADLINE_CORNER_000':'14e943baa68acceec5dfd600efa8b7b536d7c76adb5239d900a597d4e0c24cec',
'HEADLINE_CORNER_001':'eed3be9b19b6941ba30ab4ac09e8787f6aaf331ba2e6d81317dea51cc597bf40',
'HEADLINE_CORNER_010':'e6c0e3cda12276c3fb830906c0ee30c9a20912015225418755145182e3a81031',
'HEADLINE_CORNER_011':'bb7014113d66c38b634d07e4ff59a730c3762812c10e9bace78c0280bd12505b',
'HEADLINE_CORNER_100':'fac5b8a11754ecc5b4665c2f640f8bce56d5c614c52e42b39ceb3a9ea469ed7c',
'HEADLINE_CORNER_101':'d6a63c4bcb47f0b05b5d08c740d1ea67bf5a4ad2240313ce087410e9f804a290',
'HEADLINE_CORNER_110':'44fee9a4e247d810d508b440c9dc07e67aa5abf7dac312704bc2e2df92b9112e',
'HEADLINE_CORNER_111':'ca46f232cd9d18601c218f895ec490679df85fae710057f2edea9cf71265a510'}
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def need(v,msg='condition'):
 if not v:raise ValueError(msg)
def run():
 opened={};raw={};trees={};checks=[];slot_reads=[]
 def read(p):
  b=Path(p['path']).read_bytes();need(sha(b)==p['sha256'],'pin '+p['path']);opened[p['path']]=p['sha256'];return b
 for n,p in PINS.items():raw[n]=read(p)
 for n in ('parent','core','producer','ledger','r12core','r12wrapper'):trees[n]=ast.parse(raw[n])
 def node(n,name,kind=None):
  return next(x for x in trees[n].body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name==name)
 def method(n,cls,name):return next(x for x in node(n,cls).body if isinstance(x,ast.FunctionDef) and x.name==name)
 def const(n,name):
  for x in trees[n].body:
   if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in x.targets):return ast.literal_eval(x.value)
  raise ValueError(name)
 def execute(nodes,env):
  exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),'<isolated named AST>','exec'),env)
 def check(name,ok):
  checks.append({'id':name,'passed':bool(ok)});need(ok,name)
 inv=json.loads(raw['inventory']);meta={r['name']:r for r in inv['specs']}
 dry={}
 for name in [*EXPECTED,'TAIL_REANCHOR','WORKERS_8_CANDIDATE_ANCHOR']:
  rec=meta[name];need(rec['path']==str(DRY/(name+'.json')),'dry exact path');b=read({'path':rec['path'],'sha256':rec['sha256']});dry[name]=b
 reg=json.loads(raw['registry']);need(len(reg['points'])==31 and reg['complete_31_point_table'] is True)
 base=json.loads(dry['TAIL_REANCHOR']);p=base['physical']
 varying=const('producer','VARYING')
 ths={}
 for name in EXPECTED:ths[name]={**meta[name]['theta'],'Eref_base_J':p['Eref_J'],'entropy_K_factor':p['entropy_K_factor']}
 trial=ths['HEADLINE_TRIAL'];names=list(trial)
 lower={n:min(t[n] for t in ths.values()) for n in names};upper={n:max(t[n] for t in ths.values()) for n in names}
 es={'names':names,'trial_values':trial,'fixed_names':[n for n in names if n not in varying],'lower':lower,'upper':upper,'varying_names':varying}
 allowed_refs={canonical(rec[k]) for rec in reg['points'].values() for k in ('eps_certificate','lo_certificate')}
 def slot_read(ref,*args,**kwargs):
  need(canonical(ref) in allowed_refs,'unlisted slot reference');need(set(ref)=={'path','sha256'},'whole two-key pin')
  slot_reads.append(ref);return b'' # explicit pin-only stand-in: never reads scientific/numeric records
 parent={'copy':copy,'json':json,'math':math,'canonical':canonical,'sha256_bytes':sha,'OrchestratorError':ValueError,
 'SCHEMA_THETA_KEY':const('parent','SCHEMA_THETA_KEY'),'FIXED_TEMPLATE_CHECKS':const('parent','FIXED_TEMPLATE_CHECKS'),'DECLARED_CHANGED_PATHS':const('parent','DECLARED_CHANGED_PATHS')}
 execute([node('parent',n) for n in ('json_bytes','theta_key','diff_paths','Mapper')],parent)
 O=SimpleNamespace(Mapper=parent['Mapper'],json_bytes=parent['json_bytes'],sha256_bytes=sha,diff_paths=parent['diff_paths'],read_pinned=slot_read)
 current_registry=None
 def pin_doc(ref,label):need(ref==PINS['registry'],'registry pin');return current_registry
 native={'O':O,'copy':copy,'Error':ValueError,'DRIVER_SHA':const('core','DRIVER_SHA'),'digest':lambda o:sha(canonical(o)),'pin_doc':pin_doc}
 execute([node('core','point_identity'),node('core','Mapper')],native)
 CoreMapper=native['Mapper']
 ledger={'OldMapper':CoreMapper,'copy':copy,'O':O,'Error':ValueError}
 execute([node('ledger','Mapper')],ledger)
 LedgerMapper=ledger['Mapper']
 prod={'copy':copy,'json':json,'R5':(None,const('core','DRIVER_SHA')),'canonical':canonical,'_sha_bytes':sha,'need':need,
 'same':lambda a,b:canonical(a)==canonical(b),'VARYING':varying,'DECLARED':const('producer','DECLARED'),
 'SCHEMA_THETA_KEY':const('producer','SCHEMA_THETA_KEY'),'diff_paths':parent['diff_paths'],'CAP_CERT':8388608,
 'strict_pin':lambda ref,label:(need(type(ref) is dict and set(ref)=={'path','sha256'},label) or copy.deepcopy(ref)),
 'READER':SimpleNamespace(raw=slot_read)}
 wc=ast.ClassDef(name='World',bases=[],keywords=[],body=[method('producer','World',n) for n in ('probe_points','fill_slots','mapper_spec')],decorator_list=[])
 execute([node('producer',n) for n in ('json_bytes','point_identity','digest','theta_key')]+[wc],prod)
 w=prod['World']();w.base=copy.deepcopy(base);w.names=names;w.trial=trial;w.by={n:{'lower':lower[n],'upper':upper[n]} for n in names};w.records={};w.registry=None
 ctx=SimpleNamespace(base=copy.deepcopy(base),base_sha256=sha(dry['TAIL_REANCHOR']),es=es,inclination_deg=p['inclination_deg'],cfg={'tail_readiness':{}})
 execute([method('parent','Context','probe_points')],parent)
 native_points=parent['probe_points'](ctx);production_points=w.probe_points()
 check('probe_order_and_theta_9',canonical(native_points)==canonical(production_points) and len(native_points)==9)
 check('theta_schema_identity',const('parent','SCHEMA_THETA_KEY')==const('producer','SCHEMA_THETA_KEY'))
 check('r12_core_mapper_AST_identity',ast.dump(node('core','Mapper'),include_attributes=False)==ast.dump(node('r12core','Mapper'),include_attributes=False))
 check('r12_wrapper_mapper_AST_identity',ast.dump(node('ledger','Mapper'),include_attributes=False)==ast.dump(node('r12wrapper','Mapper'),include_attributes=False))
 out=[]
 for label,theta in native_points:
  name='HEADLINE_'+('TRIAL' if label=='trial' else 'CORNER_'+''.join('1' if '=hi' in s else '0' for s in label[len('corner '):].split(',')))
  need(canonical(theta)==canonical(ths[name]),'fixture theta')
  current_registry=None;ctx.cfg={'tail_readiness':{}};w.registry=None
  n=CoreMapper(ctx).build(theta);s,m=w.mapper_spec(theta);pb=prod['json_bytes'](s)
  check(name+'_native_and_producer_dry_bytes',n['raw']==pb)
  expected_dry=json.loads(dry[name])
  actual_label='DDO154 cx2v006 theta %s; point %s'%(meta[name]['theta_key'][:16],meta[name]['certificate_point_key'][:16])
  check(name+'_native_recorded_label_recipe',expected_dry['label']==actual_label)
  # Inventory publishes only four coordinates; additional fixed-coordinate inputs are not opened.
  # Validate all constructed fields, and bind the label to the published full theta digest.
  native_dry=copy.deepcopy(n['spec']);native_dry['label']=actual_label
  production_dry=copy.deepcopy(s);production_dry['label']=actual_label
  check(name+'_native_dry_fields_and_recorded_label',parent['json_bytes'](native_dry)==dry[name])
  check(name+'_producer_dry_fields_and_recorded_label',prod['json_bytes'](production_dry)==dry[name])
  # Both paths now take actual registry pins, but numeric-file reader is a declared stand-in.
  current_registry=reg;ctx.cfg={'tail_readiness':{'certificate_registry':PINS['registry'],'certificate_ledger':{'schema':'DDO154_CERTIFICATE_LEDGER_C2V003','path':'UNUSED_GENESIS_ONLY'}}}
  ctx.genesis_points=lambda:set(reg['points']);ctx.certificate_record=lambda _:(_ for _ in ()).throw(AssertionError('ledger lookup must not happen for genesis'))
  w.registry=reg
  n=CoreMapper(ctx).build(theta);l=LedgerMapper(ctx).build(theta);s,m=w.mapper_spec(theta);b=prod['json_bytes'](s)
  check(name+'_native_production_bytes',b==n['raw'])
  check(name+'_ledger_genesis_unchanged',l['raw']==n['raw'])
  filled_native=copy.deepcopy(n['spec']);filled_native['label']=actual_label
  filled_production=copy.deepcopy(s);filled_production['label']=actual_label
  final_bytes=prod['json_bytes'](filled_production)
  check(name+'_recorded_theta_bound_native_producer',parent['json_bytes'](filled_native)==final_bytes)
  check(name+'_root_predicted_sha',sha(final_bytes)==EXPECTED[name])
  rec=reg['points'][m['point_key']]
  check(name+'_whole_slot_pins',all(set(rec[k])=={'path','sha256'} and s['numerics']['uv_tail'][k]==rec[k] for k in ('eps_certificate','lo_certificate')))
  out.append({'case':name,'point_key':m['point_key'],'spec_sha256':sha(final_bytes),'bytes':len(final_bytes),'dry_spec_sha256':sha(dry[name]),'slots':{k:rec[k] for k in ('eps_certificate','lo_certificate')},'identical_native_production_ledger':True,'label_binding':'Published complete theta_key from dry inventory; all constructed physical/numerical fields tested independently.'})
 # Existing Claude4 results are evidence read, not reruns claimed here.
 c4=json.loads(raw['c4_results']);proof=[r for r in c4['results'] if r['id'].startswith(('R1_','R2_','R3_'))]
 check('published_C4_R1_R2_R3_pass_records',len(proof)==3 and all(r['passed'] is True and r['bitwise_equal']==29 for r in proof))
 return {'schema':'CX3_HEADLINE_CONSTRUCTION_REVIEW_V001','status':'TESTED','ok':True,'blocking_findings':[],
 'checks':checks,'rows':out,'opened_file_pins':[{'path':p,'sha256':s} for p,s in sorted(opened.items())],
 'source_pins':PINS,'slot_reference_checks':len(slot_reads),
 'scope':'TESTED isolated exact mapper/probe/serialization AST on 11 authorized dry fixtures and the real 31-point registry, nine probe rows; independent native/producer fields and registry fills agree. Final hash prediction uses the inventory complete-theta label. FORMAL full label/production equivalence conditional on the same frozen C1 base and full coordinate inputs. Actual producer FINAL bytes and binder_pins remain UNTESTED until C1 freeze.',
 'substitutions':['Context and World construction bypassed: base and six available coordinate values reconstructed from pinned dry inventory/11 DDO154 specs. The inventory exposes four variable/physical coordinates but only the digest of the complete theta (which contains additional fixed inputs). Native and producer reconstructed outputs match each other; all fields match dry fixtures after their label uses the published complete theta digest. The identical label recipes and hash schemas establish the full-theta label equality FORMALLY; no slots/query/coordinate file was opened.',
 'Both numeric-file readers are explicit pin-only stand-ins. They validate the exact two-key registry references and perform no numeric/certificate-file I/O. This checks byte construction, not certificate admission.',
 'No whole production module, driver, validator, campaign, verifier, or launcher executed. Only selected AST definitions with controlled globals.'],
 'later_deciding_test':'Before HEADLINE11 launch, root compares FINAL manifest binder_pins for these nine cases against rows[].spec_sha256. Real C1/adoption/PRELAUNCH checks remain required.',
 'disclosure':'Codex3 holds verdict/output-diff review, campaign-set review, policy signing and per-wave EPS signing. Same-path signer checks are disclosed in the campaign report. No independent scientific certification is claimed.',
 'c4_published_records':proof}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False))
