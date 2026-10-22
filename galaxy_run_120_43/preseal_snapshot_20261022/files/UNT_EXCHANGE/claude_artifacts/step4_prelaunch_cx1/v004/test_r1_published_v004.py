import ast,copy,hashlib,json,types,sys
from pathlib import Path
H=Path(__file__).parent.parent;B=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');BASE=B/'step4_launch_packet_cx1/impl'
OUT=B/'review_final_deltas_cx1/R1_SYNTHETIC_V004';seq=0
p=BASE/'step4_guard_cx1v010.py';G=types.ModuleType('guard010');G.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),G.__dict__)
L=types.SimpleNamespace(__file__=str(BASE/'step4_launcher_cx1v010.py'))
R5=B/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py';MON=B/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'
src=BASE/'tests/test_step4_cx1v007.py';t=ast.parse(src.read_bytes());exec(compile(ast.Module(body=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in ['put','build']],type_ignores=[]),str(src),'exec'))
OUT.mkdir()
_,_,plan,cfg=build();call=plan['calls'][0]
sources=json.loads((H/'CUSTODY_SOURCES_V001.json').read_bytes())
rels=['calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4.py','calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py','calib_tail_readiness_cx2/v006r10_c4/adoption_policy_cx2v006r10_c4.py','calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py','calib_tail_readiness_cx2/certificates_per_point/certificate_guard_cx2v003.py','calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py','calib_tail_readiness_cx2/certificates_per_point/consumed_states_cx2v010.py']
for r in rels:sources[str(B/r)]=hashlib.sha256((B/r).read_bytes()).hexdigest()
cfg['sources'].update(sources)
with G.fence(cfg['sources']):C=G.load(G.pin(B/rels[0]),cfg,'r1_native_wrapper')
spec=json.loads((B/'v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_R5_CX1V004.FILLED.json').read_bytes())
slots={k:put(k+'_inert.json',{'synthetic_fixture':True}) for k in ['eps_certificate','lo_certificate']};spec['numerics']['uv_tail'].update(slots)
identity=C.point_identity(spec);custody=json.loads((H/'CUSTODY_PROBE_V001.json').read_bytes())
producer=put('synthetic_producer.py','SYNTHETIC_PROOFS_ONLY=True\n')
def proof(gate,extra):
 d={'schema':C.G.PROOF_SCHEMA,'gate':gate,'status':'TESTED','verdict':'PASS','point_sha256':G.digest(identity),'custody_sha256':G.digest(custody),'producer':producer,'synthetic_fixture':True};d.update(extra);return put(gate+'_proof.json',d)
eps=proof('EPS',{'driver_certificate':slots['eps_certificate'],'envelope_rule':C.G.ENVELOPE,'shells':[{'range_inverse_kpc':[4.,182.],'refinement_failures':0,'eps':1.,'eps_envelope':1.}]})
gq=proof('GQ',{'method':'GEOMETRY_UNIFORM_COLUMN_BOUND','all_columns_included':True,'all_production_kperp_nodes':True,'nonnegative_masses_required':True,'M_s':128,'M_s_doubled':256,'K_big_inverse_kpc':128.,'max_column_difference_over_analytic_Pi0':0.,'max_zero_mode_relative_error':0.})
lo=proof('LO_ENVELOPE',{'driver_certificate':slots['lo_certificate'],'covers_all_consumed_states':True})
bundle=put('bundle.json',{'schema':C.G.SCHEMA,'identity':identity,'custody':custody,'domain':{'K_inverse_kpc':4.,'K_big_inverse_kpc':128.},'prelaunch':{'EPS':eps,'GQ':gq,'LO_ENVELOPE':lo},'driver_certificate_bindings':slots,'acceptance_rule':'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED'})
registry=put('registry_real_identity.json',{'points':{G.digest(identity):{'identity':identity,'bundle':bundle}}})
cert=B/'calib_tail_readiness_cx2/certificates_per_point';deriver=G.pin(cert/'custody_cx2v002.py');enumerator=G.pin(cert/'consumed_states_cx2v010.py')
review=put('certificate_policy_real_binding.json',{'schema':C.POLICY_SCHEMA,'status':'TESTED','ok':True,'synthetic_fixture':True,'driver_sha256':G.R5_SHA,'custody_deriver':deriver,'state_enumerator':enumerator,'approved_certificate_producers':[producer],'guard_sha256':sources[str(cert/'certificate_guard_cx2v003.py')],'driver_slot_rule':'POINT_EPS_AND_REVIEWED_PRELAUNCH_LO_ENVELOPE','post_state_handoff':'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'})
config=G.doc(cfg['config']);config['numerics']['block']=copy.deepcopy(spec['numerics']);config['tail_readiness']={'certificate_registry':registry,'certificate_policy_review':review,'custody_deriver':deriver,'state_enumerator':enumerator,'approved_certificate_producers':[producer]}
context=put('native_certificate_context.py',f'''import types,hashlib
from pathlib import Path
p=Path({str(B/rels[0])!r});b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()=={sources[str(B/rels[0])]!r}
C=types.ModuleType('r1_wrapper_adapter');C.__file__=str(p);exec(compile(b,str(p),'exec'),C.__dict__)
O=C.O
validate_block=C.validate_block
class Context(C.Context):
 def __init__(self,cfg):self.cfg=cfg;self.numerics=cfg['numerics']['block']
 def sensitivity_gate(self,spec):return {{'ok':True,'reasons':[],'synthetic_unrelated_gate':True}}
 def prelaunch_check(self,spec):
  gate=self.certificate_check(spec,'prelaunch')
  if not gate['ok']:raise ValueError(gate['blockers'])
  D=C.O.load_pinned_module({G.pin(R5)!r},'r1_normalize_driver','r5 driver')
  return D.normalize_spec(spec)
''')
cfg['context_module']=context;cfg['sources'].update({x['path']:x['sha256'] for x in [context,producer,deriver,enumerator]});cfg['config']=put('config_real_custody.json',config)
call['spec']=put('spec_real_custody.json',spec);call['prelaunch']=None;cfg['calls']['SYNTH'].update(spec=call['spec'],prelaunch=None);cfg['plan']=None
cfg['source_review']=put('source_review_real_custody.json',{'schema':'UNT_STEP4_SOURCE_REVIEW_CX1V001','status':'TESTED','verdict':'PASS','reviewer':'SYNTHETIC_INDEPENDENT_REVIEWER','blocking_findings':[],'approved_sources':cfg['sources']})
ep=B/'step4_prelaunch_cx1/v004/step4_prelaunch_cx1v004.py'
E=types.ModuleType('emitter');E.__file__=str(ep);exec(compile(ep.read_bytes(),str(ep),'exec'),E.__dict__)
pr=put('candidate_plan.json',plan);ar=put('candidate_admission.json',cfg);out=OUT/'emitted';out.mkdir()
result=E.emit(ar,pr,out)
record=json.loads((out/'PRELAUNCH_0000.json').read_bytes());assert record['checks']['certificate_prelaunch']['ok'] is True
with (OUT/'RESULT.json').open('x') as f:json.dump({'result':result,'scope':'Real wrapper certificate policy/check, real custody derive and certificate guard; synthetic registry/proofs and unrelated adoption/sensitivity adapters. No numerical producer or scientific launch.','guard':G.pin(p),'sources':cfg['sources']},f,indent=2)
print(json.dumps(result))
