"""Inert batch atomic validation and actual guard fence checks."""
import ast,copy,hashlib,importlib.util,json,types
from pathlib import Path
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl');HERE=Path(__file__).parent
sp=importlib.util.spec_from_file_location('emitter',HERE/'step4_prelaunch_cx1v001.py');E=importlib.util.module_from_spec(sp);sp.loader.exec_module(E)
G=E.guard();L=types.SimpleNamespace(__file__=str(BASE/'step4_launcher_cx1v008.py'))
OUT=HERE/'batch_fixtures_v001';OUT.mkdir();seq=0
R5=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py');MON=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py')
source=BASE/'tests/test_step4_cx1v007.py';tree=ast.parse(source.read_bytes());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('put','build')],type_ignores=[]),str(source),'exec'))
checks=[]
for label,mode in [('batch_positive','ok'),('later_gate_refusal','bad'),('fence_write','write'),('fence_process','process')]:
 _,_,plan,cfg=build();cfg['plan']=None;call=plan['calls'][0];call['prelaunch']=None;cfg['calls']['SYNTH']['prelaunch']=None
 c=copy.deepcopy(call);c['case']='SECOND';plan['calls'].append(c);cfg['case_order'].append('SECOND');cfg['calls']['SECOND']={k:c[k] for k in ('spec','driver','prelaunch')}
 expected=None
 if mode=='bad':c['driver']['sha256']='0'*64;expected='EXACT_DRIVER_REQUIRED'
 if mode in ('write','process'):
  code="open("+repr(str(OUT/'forbidden_sentinel'))+",'x')" if mode=='write' else "__import__('subprocess').Popen(['/usr/bin/true'])"
  ref=put(label+'_adapter.py',"DIRECT_CONTEXT_API='UNT_STEP4_DIRECT_PREFLIGHT_CX1V001'\ndef build(C,config,**kw):\n "+code+"\n return C.Context(config)\n")
  cfg['direct_context']=ref;cfg['sources'][ref['path']]=ref['sha256'];review=G.doc(cfg['source_review']);review['approved_sources']=cfg['sources'];cfg['source_review']=put(label+'_review.json',review)
  expected='PREFLIGHT_WRITE_REFUSED' if mode=='write' else 'PREFLIGHT_PROCESS_OR_NETWORK_REFUSED'
 pr=put(label+'_plan.json',plan);ar=put(label+'_cfg.json',cfg);out=OUT/label;out.mkdir()
 try:
  r=E.emit(ar,pr,out);m=G.doc(r['manifest']);assert r['records']==2 and [x['case'] for x in m['calls']]==['SYNTH','SECOND']
  for entry,cc in zip(m['calls'],plan['calls']):assert G.doc(entry['prelaunch'])==G.native_preflight(cfg,cc)
  ok=expected is None;detail='two exact native returns and manifest pins'
 except Exception as e:detail=str(e);ok=expected is not None and expected in detail and not list(out.iterdir())
 checks.append({'name':label,'passed':ok,'detail':detail})
assert not (OUT/'forbidden_sentinel').exists()
r={'scope':'TESTED inert adapters, actual guard fence, no scientific execution','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'source':G.pin(__file__),'emitter':G.pin(E.__file__),'guard':G.pin(G.__file__)}
with (HERE/'BATCH_TEST_RESULTS_V001.json').open('x') as f:json.dump(r,f,indent=2)
print(json.dumps(r,indent=2));raise SystemExit(not all(x['passed'] for x in checks))
