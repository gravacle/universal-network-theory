"""Inert adapters exercise unchanged guard007; no launcher entrypoint is invoked."""
import ast, copy, hashlib, importlib.util, json, types
from pathlib import Path
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl')
HERE=Path(__file__).parent
sp=importlib.util.spec_from_file_location('emitter',Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_prelaunch_cx1/v003/step4_prelaunch_cx1v003.py')); E=importlib.util.module_from_spec(sp);sp.loader.exec_module(E)
G=E.guard(); L=types.SimpleNamespace(__file__=str(BASE/'step4_launcher_cx1v008.py'))
OUT=HERE/'fixtures_v003';OUT.mkdir();seq=0
R5=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py')
MON=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py')
source=BASE/'tests/test_step4_cx1v007.py'
tree=ast.parse(source.read_bytes());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('put','build')]
exec(compile(ast.Module(body=defs,type_ignores=[]),str(source),'exec'))
results=[]
def run(name, change=None, reason=None):
    _,_,plan,cfg=build();call=plan['calls'][0]
    cfg['plan']=None;call['prelaunch']=None;cfg['calls']['SYNTH']['prelaunch']=None
    if change:change(plan,cfg)
    pr=put(name+'_plan.json',plan);ar=put(name+'_admission.json',cfg)
    out=OUT/name;out.mkdir()
    try:
        result=E.emit(ar,pr,out)
        record=json.loads((out/'PRELAUNCH_0000.json').read_bytes())
        native=G.native_preflight(cfg,call)
        manifest=G.doc(result['manifest'])
        ok=reason is None and record==native and manifest['calls'][0]['prelaunch']==G.pin(out/'PRELAUNCH_0000.json')
        detail='exact native return and manifest byte pins'
        if name=='nominal':
            before={p.name:p.read_bytes() for p in out.iterdir()}
            try:E.emit(ar,pr,out);raise AssertionError('replay accepted')
            except G.Refusal: pass
            except Exception as e:
                assert 'EXISTING_OUTPUT_REFUSED' in str(e),str(e)
            assert before=={p.name:p.read_bytes() for p in out.iterdir()}
    except Exception as e:
        detail=type(e).__name__+': '+str(e)
        ok=reason is not None and reason in detail and not list(out.iterdir())
    results.append(dict(name=name,passed=ok,detail=detail))
def config_change(cfg,key,value):
    c=G.doc(cfg['config']);c['tail_readiness'][key]=value;cfg['config']=put('changed_config_'+str(seq)+'.json',c)
def unregistered(plan,cfg):
    # Deliberately inert registry-sensitive adapter: proves wrapper propagates
    # native certificate refusal; production registry semantics remain untested.
    p=put('registry_context.py', '''class O: pass
class Context:
 def __init__(self,cfg): self.cfg=cfg
 def certificate_policy_gate(self): return {'ok':True,'reasons':[]}
 def certificate_check(self,spec,phase):
  import json
  with open(self.cfg['tail_readiness']['certificate_registry']['path']) as f:r=json.load(f)
  ok=str(spec['physical']['distance_Mpc']) in r['points']
  return {'ok':ok,'blockers':[] if ok else ['UNREGISTERED_POINT']}
 def sensitivity_gate(self,spec):return {'ok':True,'reasons':[]}
 def prelaunch_check(self,spec):return spec
def validate_block(block):return True
''')
    cfg['context_module']=p;cfg['sources'][p['path']]=p['sha256']
    review=G.doc(cfg['source_review']);review['approved_sources']=cfg['sources'];cfg['source_review']=put('registry_review.json',review)
def changed_spec(plan,cfg):
    c=plan['calls'][0];b=Path(c['spec']['path']).read_bytes()+b'\n';p=OUT/'changed_spec_bytes.json';p.write_bytes(b)
    c['spec']={'path':str(p),'sha256':c['spec']['sha256']};cfg['calls']['SYNTH']['spec']=c['spec']
def diii(plan,cfg):
    c=plan['calls'][0];c.update(tail_on=False,family='DECIDING_III');s=G.doc(c['spec']);s['numerics']={};c['spec']=put('diii_spec.json',s);cfg['calls']['SYNTH']['spec']=c['spec'];cfg['tail_off_policy']=None
run('nominal')
run('null_registry',lambda p,c:config_change(c,'certificate_registry',None),'PIN_REQUIRED')
run('null_policy',lambda p,c:config_change(c,'certificate_policy_review',None),'PIN_REQUIRED')
run('unregistered_point',unregistered,'NATIVE_GATE_REFUSED')
run('pass_label',lambda p,c:p['calls'][0].update(prelaunch='PASS'),'PRELAUNCH_INPUT_MUST_BE_PENDING')
run('changed_spec',changed_spec,'PIN_BYTES_CHANGED')
run('wrong_driver',lambda p,c:p['calls'][0]['driver'].update(sha256='0'*64),'EXACT_DRIVER_REQUIRED')
run('diii_without_policy',diii,'PIN_REQUIRED')
report={'scope':'TESTED unchanged guard007 with inert context/policy adapters; production native stack and scientific execution UNTESTED','checks':results,'passed':sum(x['passed'] for x in results),'total':len(results),'sources':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_prelaunch_cx1/v003/step4_prelaunch_cx1v003.py'),source,Path(G.__file__))}}
with (HERE/'PRELAUNCH_RESULTS_V003.json').open('x') as f:json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
raise SystemExit(not all(x['passed'] for x in results))
