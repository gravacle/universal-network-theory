"""Owned mock evidence only; production-shaped fixtures never confer real authority."""
import builtins,copy,hashlib,importlib.util,json,math,os,types
from pathlib import Path
from unittest.mock import patch
I=Path(__file__).resolve().parent.parent;OUT=I/'tests/CONTROLS_V005';OUT.mkdir()
sp=importlib.util.spec_from_file_location('W',I/'write_step4_step5_handoff_cx1v008.py');W=importlib.util.module_from_spec(sp);sp.loader.exec_module(W)
checks=[]
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def put(p,obj):
 b=obj.encode() if isinstance(obj,str) else W.encoded(obj)
 with p.open('xb') as f:f.write(b)
 return pin(p)
def check(name,fn,err=None):
 try:v=fn();ok=err is None and v is not False;detail=repr(v)[:180]
 except BaseException as e:ok=err is not None and err in str(e);detail=type(e).__name__+': '+str(e)
 checks.append({'name':name,'passed':ok,'detail':detail})
BASE=W.BASE
policy=json.loads((BASE/'POLICY_CX3V001.json').read_bytes());C=json.loads(Path(policy['coordinates']['path']).read_bytes())
point={'log_index':0,'u':[],'theta_natural':{}}
for c in C['engine_coordinates']:
 if c['role']=='fixed':v=c['trial_value']
 else:
  point['u'].append(.5)
  v=math.exp((math.log(c['lower'])+math.log(c['upper']))/2) if c['transform']=='log' else (c['lower']+c['upper'])/2
 point['theta_natural'][c['name']]=v
PRODUCER=r"""import json,hashlib,math
ADMISSION_API='UNT_STEP4_TARGET_FREE_PRODUCER_API_CX1V001'
def verify_admission(*,snapshots,record_pin,decision_pin,acceptance_pin,mode):
 def doc(ref):
  b=snapshots[ref['path']]
  if hashlib.sha256(b).hexdigest()!=ref['sha256']:raise ValueError('MOCK_SNAPSHOT_PIN')
  return json.loads(b)
 r=doc(record_pin);d=doc(decision_pin);a=doc(acceptance_pin);e=doc(r['scientific_evidence_pin'])
 ps=hashlib.sha256(json.dumps(r['point'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
 reasons=[]
 if set(e)!={'schema','mode','synthetic_fixture','point_sha256','valid','model_values','bounds'} or e['schema']!='UNT_OWNED_MOCK_RECTANGLE_EVIDENCE' or e['synthetic_fixture'] is not True or e['mode']!=mode or e['point_sha256']!=ps or e['valid'] is not True:reasons.append('MOCK_RECTANGLE_SCHEMA')
 if len(e['model_values'])!=len(e['bounds']) or not all(type(x) in (int,float) and math.isfinite(x) and lo<=x<=hi for x,(lo,hi) in zip(e['model_values'],e['bounds'])):reasons.append('MOCK_RECTANGLE_MEMBERSHIP')
 for kind,pin in r['certificate_pins'].items():
  c=doc(pin)
  if set(c)!={'schema','mode','synthetic_fixture','kind','point_sha256','valid'} or c!={'schema':'UNT_OWNED_MOCK_CERTIFICATE','mode':mode,'synthetic_fixture':True,'kind':kind,'point_sha256':ps,'valid':True}:reasons.append('MOCK_CERTIFICATE')
 if d['engine_status']!='COMPLETE' or d['engine_ok'] is not True or d['replay']['complete_runs']!=2 or d['replay']['match'] is not True:reasons.append('MOCK_FULL_DECISION')
 return {'api':ADMISSION_API,'ok':not reasons,'reasons':reasons,'point_sha256':ps,'provenance':r['provenance'],'certificate_pins':r['certificate_pins'],'decision_sha256':decision_pin['sha256']}
"""
def fixture(name,mutations=None,production=False,producer_text=None):
 d=OUT/name;d.mkdir();m=mutations or {};mode='PRODUCTION' if production else 'SYNTHETIC_DRY_ONLY';owner=W.ROOT if production else W.SYNTHETIC
 def change(k,obj):
  if k in m:m[k](obj)
  return obj
 def wx(name,obj):return put(d/name,obj)
 p=copy.deepcopy(point);ps=W.digest(W.canonical(p));prod=wx('MOCK_PRODUCER.py',producer_text or PRODUCER)
 review=wx('producer_review.json',change('review',{'schema':'UNT_STEP4_TARGET_FREE_PRODUCER_REVIEW_CX1V001','mode':mode,'verdict':'PASS','producer_pin':prod,'record_schema':'UNT_STEP4_SCIENTIFIC_POINT_ADMISSION_CX1V001','blocking_findings':[],'reviewer':'INDEPENDENT_SYNTHETIC_FIXTURE','semantic_scope':['NATIVE_RECTANGLE_MEMBERSHIP_RECOMPUTED','COMPLETE_DOUBLE_REPLAY','NATIVE_RECORD_REGISTRY_VERIFIED','GUARDED_ADMISSION_PROVENANCE','POST_STATE_CERTIFICATES_VERIFIED','NGC_POINT_CERTIFICATES_VERIFIED','UNCHANGED_NATIVE_COORDINATES']}))
 case=wx('case.json',{'schema':'SYNTHETIC_CASE','value':1});compare=wx('compare.py','# Owned inert mock compare; never executed.\n');addendum=wx('addendum.md','Owned synthetic metadata; no scientific adoption.\n')
 prereg=wx('prereg.json',{'schema':'UNT_V007_PREREG_VIEW_CX1V001','binding_inputs':{'case_block':case}})
 report=wx('verdict.json',change('verdict',{'schema':'UNT_V007_VERDICT_VIEW_CX1V001','test_mode':not production,'decision':{'tests_read':True,'outcome':'ADOPT_TAIL'},'script_sha256':compare['sha256'],'prereg':prereg,'case_block':case}))
 seal=wx('seal.json',change('seal',{'schema':'UNT_V007_ADOPTION_SEAL_VIEW_CX1V001','sealed_by':owner,'prereg':prereg,'compare':compare,'frozen_addendum':addendum,'verdict':report,'case_block':case}))
 v007={'seal':seal,'verdict':report,'prereg':prereg,'compare':compare,'addendum':addendum,'case_block':case}
 dec=wx('decision.json',change('decision',{'schema':'UNT_STEP4_FINAL_DECISION_TARGET_FREE_VIEW_CX1V001','mode':mode,'target_free':True,'scope':'FULL_FINAL_DECISION','engine_status':'COMPLETE','engine_ok':True,'coordinate_pin':policy['coordinates'],'admitted_points':[copy.deepcopy(p)],'replay':{'complete_runs':2,'match':True,'canonical_run_sha256':'1'*64},'registry':{'record_file_sha256':'2'*64,'record_sha256':'3'*64,'registry_line_sha256':'4'*64,'verify_ok':True,'registry_chain_ok':True,'verify_reasons':[]},'blocking_findings':[]}))
 certs={k:wx(k+'.json',change(k,{'schema':'UNT_OWNED_MOCK_CERTIFICATE','mode':mode,'synthetic_fixture':True,'kind':k,'point_sha256':ps,'valid':True})) for k in ('eps_certificate','lo_certificate')}
 bundle=wx('bundle.json',{'schema':'UNT_STEP4_POST_STATE_BUNDLE_VIEW_CX1V001','mode':mode,'target_free':True,'point_sha256':ps,'phase':'acceptance','certificate_pins':certs})
 ce=wx('certificate_evidence.json',change('certificate_evidence',{'schema':'UNT_STEP5_POINT_CERTIFICATE_EVIDENCE_CX1V001','mode':mode,'target_free':True,'point_sha256':ps,'certificate_pins':certs,'verified':True,'scope':'NGC91_K32_MS96','blockers':[]}))
 ac=wx('acceptance.json',change('acceptance',{'schema':'UNT_STEP4_POST_STATE_ACCEPTANCE_VIEW_CX1V001','mode':mode,'phase':'acceptance','ok':True,'blockers':[],'point_sha256':ps,'decision_pin':dec,'guarded_plan_sha256':'5'*64,'guarded_admission_sha256':'6'*64,'v007_verdict_pin':report,'post_state_bundle_pin':bundle,'certificate_pins':certs}))
 ev=wx('scientific_evidence.json',change('science',{'schema':'UNT_OWNED_MOCK_RECTANGLE_EVIDENCE','mode':mode,'synthetic_fixture':True,'point_sha256':ps,'valid':True,'model_values':[1.,2.],'bounds':[[0.,2.],[1.,3.]]}))
 rec=wx('record.json',change('record',{'schema':'UNT_STEP4_SCIENTIFIC_POINT_ADMISSION_CX1V001','mode':mode,'status':'SCIENTIFICALLY_ADMITTED','target_free':True,'coordinate_pin':policy['coordinates'],'point':p,'v007':v007,'decision_pin':dec,'acceptance_pin':ac,'certificate_pins':certs,'certificate_evidence_pin':ce,'scientific_evidence_pin':ev,'provenance':{'native_record_sha256':'2'*64,'native_registry_line_sha256':'4'*64,'replay_run_sha256':'1'*64,'guarded_plan_sha256':'5'*64,'guarded_admission_sha256':'6'*64,'record_producer_pin':prod}}))
 rule=wx('rule.json',change('rule',{'schema':'UNT_STEP4_STEP5_RELEASE_RULE_CX1V001','mode':mode,'authority':owner,'release_scope':'FULL_FINAL_DECISION','requires_full_decision':True,'pointwise_streaming_allowed':False,'coordinate_pin':policy['coordinates']}))
 anchor=wx('authority.json',change('authority',{'schema':W.SCHEMA,'mode':mode,'authority':owner,'writer_pin':pin(Path(W.__file__)),'record_pin':rec,'rule_pin':rule,'producer_pin':prod,'producer_review_pin':review,'selected_registry_pin':W.REGISTRY,'driver_branch':'r006_fallback','driver_acceptance_pin':None}))
 return d,anchor

def runfixture(name,m=None,error=None,production=False,producer_text=None):
 d,a=fixture(name,m,production,producer_text)
 check(name,lambda:W.prepare(a['path'],a['sha256'],d/'out',synthetic_dry_only=not production),error)
 if error:check(name+'_no_output',lambda:not (d/'out').exists())
 return d,a
def flip_representation(r):
 k,v=next((k,v) for k,v in r['point']['theta_natural'].items() if type(v) is float and v.is_integer())
 r['point']['theta_natural'][k]=int(v)
D,A=runfixture('nominal_synthetic')
runfixture('nominal_production_control_only',production=True)
runfixture('no_sealed_v007',{'seal':lambda s:s.update(sealed_by={})},'SEALED_V007_REQUIRED')
runfixture('no_adopt_tail',{'verdict':lambda s:s['decision'].update(outcome='REFUSE')},'SEALED_ADOPT_TAIL_REQUIRED')
runfixture('no_admitted_point',{'record':lambda s:s.update(status='VALID')},'SCIENTIFIC_ADMITTED_POINT_REQUIRED')
runfixture('prelaunch_not_admission',{'acceptance':lambda s:s.update(phase='prelaunch')},'POST_STATE_ACCEPTANCE_REQUIRED')
runfixture('full_workflow_not_engine_complete',{'decision':lambda s:s.update(engine_status='BUDGET_EXHAUSTED')},'FULL_FINAL_DECISION_REQUIRED')
runfixture('no_complete_double_replay',{'decision':lambda s:s['replay'].update(complete_runs=1)},'COMPLETE_DOUBLE_REPLAY_REQUIRED')
runfixture('broken_native_registry',{'decision':lambda s:s['registry'].update(registry_chain_ok=False)},'VERIFIED_NATIVE_REGISTRY_REQUIRED')
runfixture('forged_record_pin',{'authority':lambda s:s['record_pin'].update(sha256='0'*64)},'PIN_BYTES_CHANGED')
runfixture('missing_producer',{'authority':lambda s:s.update(producer_pin=None)},'FINAL_EXPORT_PRODUCER_PENDING')
runfixture('unreviewed_producer',{'review':lambda s:s.update(blocking_findings=['OPEN'])},'PRODUCER_REVIEW_REQUIRED')
runfixture('streaming_not_adopted',{'rule':lambda s:s.update(pointwise_streaming_allowed=True)},'FULL_FINAL_DECISION_RULE_REQUIRED')
runfixture('native_three_u_refuses_consumer',{'decision':lambda s:s['admitted_points'][0]['u'].pop()},'CONSUMER_COORDINATE_CONTRACT')
runfixture('selected_boolean_index',{'record':lambda s:s['point'].update(log_index=False)},'CONSUMER_COORDINATE_CONTRACT')
runfixture('native_point_not_unchanged',{'record':flip_representation},'POINT_NOT_IN_FINAL_ADMITTED_SET')
runfixture('wrong_acceptance_point',{'acceptance':lambda s:s.update(point_sha256='0'*64)},'ACCEPTANCE_POINT_PROVENANCE_BINDING')
runfixture('forged_membership',{'science':lambda s:s.update(model_values=[99.,2.])},'PRODUCER_SCIENTIFIC_VERIFICATION_REQUIRED')
runfixture('forged_certificate',{'eps_certificate':lambda s:s.update(valid=False)},'PRODUCER_SCIENTIFIC_VERIFICATION_REQUIRED')
runfixture('wrong_certificate_scope',{'certificate_evidence':lambda s:s.update(scope='DDO_ONLY')},'POINT_CERTIFICATE_EVIDENCE_REQUIRED')
runfixture('target_field_in_record',{'record':lambda s:s.update(observed_velocities=[10.])},'TARGET_FIELD_REFUSED')
runfixture('nested_target_field',{'record':lambda s:s['provenance'].update(extra={'target_values':[10.]})},'TARGET_FIELD_REFUSED')
runfixture('target_field_in_certificate',{'eps_certificate':lambda s:s.update(target_values=[10.])},'TARGET_FIELD_REFUSED')
runfixture('unknown_record_field',{'record':lambda s:s.update(extra=1)},'EXACT_FIELDS_ADMISSION_RECORD')
runfixture('integer_rule_true',{'rule':lambda s:s.update(requires_full_decision=1)},'FULL_FINAL_DECISION_RULE_REQUIRED')
runfixture('integer_rule_false',{'rule':lambda s:s.update(pointwise_streaming_allowed=0)},'FULL_FINAL_DECISION_RULE_REQUIRED')
runfixture('integer_tests_read',{'verdict':lambda s:s['decision'].update(tests_read=1)},'SEALED_ADOPT_TAIL_REQUIRED')
runfixture('integer_cert_verified',{'certificate_evidence':lambda s:s.update(verified=1)},'POINT_CERTIFICATE_EVIDENCE_REQUIRED')
runfixture('integer_cert_target_free',{'certificate_evidence':lambda s:s.update(target_free=1)},'POINT_CERTIFICATE_EVIDENCE_REQUIRED')
runfixture('integer_producer_ok',producer_text=PRODUCER.replace("'ok':not reasons","'ok':1"),error='PRODUCER_SCIENTIFIC_VERIFICATION_REQUIRED')
runfixture('producer_io_denied',producer_text=PRODUCER+'\nopen("/private/tmp/NEVER_CREATED_BY_PRODUCER","w")\n',error='PRODUCER_IO_OR_PROCESS_REFUSED')
runfixture('producer_metadata_denied',producer_text=PRODUCER+'\nimport os\nos.stat("/private/tmp/NEVER_PROBED_BY_PRODUCER")\n',error='PRODUCER_METADATA_REFUSED')
# Emit audit events only. None of these probes calls an OS mutation function.
for event in ('os.chmod','os.chown','os.utime','os.setxattr','os.removexattr','os.rename','os.truncate','os.putenv','shutil.copyfile','ctypes.dlopen'):
 runfixture('pure_audit_'+event.replace('.','_'),producer_text=PRODUCER+'\nimport sys\nsys.audit('+repr(event)+',"INERT_EVENT_ONLY")\n',error='PRODUCER_IO_OR_PROCESS_REFUSED')
# No read/stat/resolve of the virtual protected destination is allowed.
probes=[]
def deny(*a,**kw):probes.append(a);raise AssertionError('METADATA')
with patch.object(os,'lstat',deny),patch.object(os,'readlink',deny):
 check('protected_lexical_before_metadata',lambda:W.safe_path('/private/tmp/UVT_NEVER_OPEN/file.json'),'PROTECTED_PATH_REFUSED')
 check('target_lexical_before_metadata',lambda:W.safe_path('/private/tmp/NGC3198_observed_velocities.json'),'NGC_TARGET_PATH_REFUSED')
check('zero_protected_metadata',lambda:probes==[])
# Snapshots are read once and later accesses use the validated immutable buffer.
origopen=builtins.open;counts={}
def counted(path,*args,**kw):
 path=str(path)
 if path==A['path']:counts[path]=counts.get(path,0)+1
 return origopen(path,*args,**kw)
with patch.object(builtins,'open',counted):payloads,receipt=W.prepare(A['path'],A['sha256'],D/'snapshot_out',synthetic_dry_only=True)
check('authority_read_once',lambda:counts=={A['path']:1})
anchor_doc=json.loads(Path(A['path']).read_bytes());rpin=anchor_doc['record_pin'];real=W.Snapshots.raw;access=[0]
def later_changed(self,ref):
 # Return verified snapshots; introduce a changed backing read only if the
 # implementation tries reopening the same record path.
 return real(self,ref)
class LateReader:
 def __init__(self,wrapped):self.wrapped=wrapped
 def __enter__(self):return self
 def __exit__(self,*args):self.wrapped.close()
 def read(self,*args):
  access[0]+=1
  return self.wrapped.read(*args) if access[0]==1 else b'{"forged_late_record":true}'
def lateopen(path,*args,**kw):
 f=origopen(path,*args,**kw)
 return LateReader(f) if str(path)==rpin['path'] else f
with patch.object(builtins,'open',lateopen):late_payloads,_=W.prepare(A['path'],A['sha256'],D/'late_out',synthetic_dry_only=True)
check('record_snapshot_read_once',lambda:access==[1])
check('late_read_does_not_change_point',lambda:json.loads(late_payloads['TARGET_FREE_EXPORT_CX1V001.json'])['admitted_points']==[point])
# Actual selected filler receives only synthetic handoff/export; it performs its
# own locked-policy/source/spec checks, with pending certificate sentinels.
receipt=W.write_point(A['path'],A['sha256'],D/'handoff_output',synthetic_dry_only=True)
F=W.load_filler(W.Snapshots());hp=receipt['handoff_pin']
filled=F.fill(hp['path'],hp['sha256'],D/'filled_output',True)
check('actual_selected_filler_four_specs',lambda:len(filled['outputs'])==4 and filled['launch_authorized'] is False and filled['mode']=='SYNTHETIC_DRY_ONLY')
check('synthetic_certificates_pending',lambda:set(filled['pending_certificates'])=={'eps_certificate','lo_certificate'})
check('exclusive_writer_output',lambda:W.write_point(A['path'],A['sha256'],D/'handoff_output',synthetic_dry_only=True),'NEW_OUTPUT_DIRECTORY_REQUIRED')
check('synthetic_default_refusal',lambda:W.prepare(A['path'],A['sha256'],D/'wrong_mode'),'EXTERNAL_ROOT_PUBLICATION_REQUIRED')
check('duplicate_keys',lambda:W.decode(b'{"a":1,"a":2}'),'DUPLICATE_JSON_KEY')
check('overflow_float',lambda:W.decode(b'{"a":1e999}'),'NONFINITE_JSON')
report={'status':'TESTED','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'writer_pin':pin(Path(W.__file__)),'selected_filler_pin':W.FILLER,'synthetic_filled_directory':str(D/'filled_output'),'scientific_launches':0,'real_admission':'UNTESTED','production_shape_fixture_scope':'Owned mock only; prepare buffers never published as real authority or ADMITTED handoffs.'}
put(OUT/'RESULTS.json',report)
print(json.dumps({'passed':report['passed'],'total':report['total'],'failed':[x for x in checks if not x['passed']]}))
raise SystemExit(0 if report['passed']==report['total'] else 1)
