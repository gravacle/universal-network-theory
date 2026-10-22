"""Independent binder execution on builder-owned SYNTHETIC ADAPTER fixtures only."""
import copy,hashlib,json,types
from pathlib import Path
R=Path(__file__).resolve().parent;I=R.parent/'impl';O=R/'BINDER_INDEPENDENT_V002';O.mkdir()
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
p=I/'step4_bind_cx1v004.py';B=types.ModuleType('binder');B.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),B.__dict__)
F=I/'tests/SYNTH_V004';plan=json.loads((F/'001plan.json').read_bytes());cfg=json.loads((F/'001admission.json').read_bytes());cfg['plan']=None
checks=[]
def write(p,d):
 with p.open('x') as f:json.dump(d,f,allow_nan=False);f.write('\n')
 return p
def ck(n,v,detail=None):checks.append({'id':n,'pass':v is True,'detail':detail})
def test(n,mut=None,outputs=None,expected=None):
 d=O/n;d.mkdir();pl=copy.deepcopy(plan);c=copy.deepcopy(cfg)
 if mut:mut(pl,c)
 pp=write(d/'input_plan.json',pl);cp=write(d/'candidate.json',c)
 outs=[d/'bound_plan.json',d/'bound_admission.json',d/'command.sh']
 if outputs:outputs(outs)
 try:
  ret=B.bind(pp,cp,*outs)
  ck(n,expected is None,ret)
 except Exception as e:ck(n,expected is not None and expected in str(e),type(e).__name__+': '+str(e))
 return d,outs
d,outs=test('positive')
ck('bound_plan_same_bytes',outs[0].read_bytes()==(d/'input_plan.json').read_bytes())
bound=json.loads(outs[1].read_bytes());ck('bound_plan_ref',bound['plan']==pin(outs[0]))
cmd=outs[2].read_text();ck('command_no_autoauth','export UNT_STEP4' not in cmd and '--execute-root-only' in cmd)
old={str(p):p.read_bytes() for p in outs}
try:B.bind(d/'input_plan.json',d/'candidate.json',*outs);ck('repeat_refusal',False)
except Exception as e:ck('repeat_refusal','EXCLUSIVE_PACKET_OUTPUT_REQUIRED' in str(e),str(e))
ck('repeat_unchanged',all(p.read_bytes()==old[str(p)] for p in outs))
def existing(outs):
 with outs[2].open('x') as f:f.write('sentinel')
d,o=test('third_output_exists',outputs=existing,expected='EXCLUSIVE_PACKET_OUTPUT_REQUIRED')
ck('third_collision_no_prefix',not o[0].exists() and not o[1].exists() and o[2].read_text()=='sentinel')
test('duplicate_output',outputs=lambda o:o.__setitem__(2,o[1]),expected='DISTINCT_NEW_OUTPUTS_REQUIRED')
test('wrong_authority',mut=lambda p,c:c.__setitem__('authority',{'identity':'Codex1'}),expected='ROOT_STEP4_AUTHORITY_REQUIRED')
test('pending_spec',mut=lambda p,c:p['calls'][0].__setitem__('pending',['pending']),expected='PENDING_SPEC_REFUSED')
test('output_alias',mut=lambda p,c:p['calls'][0].__setitem__('receipt',p['calls'][0]['outdir']),expected='ALIASED_OUTPUTS')
test('nested_output',mut=lambda p,c:p['calls'][0].__setitem__('receipt',p['calls'][0]['outdir']+'/receipt'),expected='NESTED_OUTPUTS')
test('source_bytes_mismatch',mut=lambda p,c:c['sources'].__setitem__(next(iter(c['sources'])),'0'*64),expected='PIN_BYTES_CHANGED')
result={'schema':'STEP4_BINDER_INDEPENDENT_CX1V002','label':'TESTED_SYNTHETIC_ADAPTER_FIXTURES','verdict':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,'pins':[pin(I/'step4_bind_cx1v004.py'),pin(I/'step4_guard_cx1v005.py'),pin(F/'001plan.json'),pin(F/'001admission.json'),pin(Path(__file__))],'limitations':['Scientific policy/certificate/sensitivity providers in builder fixture are stubs. No real admission published, production native preflight or processes run. Output script generated but never executed.']}
p=write(O/'RESULTS.json',result);print(json.dumps({'result':pin(p),'total':len(checks),'failed':[x for x in checks if not x['pass']]}))
