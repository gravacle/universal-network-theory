"""A205 offline preparation. No scientific module or comparator executes."""
import ast,contextlib,hashlib,io,json,os,runpy,sys,subprocess,datetime
from pathlib import Path
B=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');H=Path(__file__).parent;S=H/'scratch_prep_v002'
G=B/'b1_policy_successor_c4/tools/make_b1_cascade_c4v002.py'
CTRL=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
CMP=CTRL/'V007_SEAL_ASSEMBLY/kmax_tail_compare_c2v007_r14_cx1v001_SEALED_V007.py';PRE=CTRL/'V007_SEAL_ASSEMBLY/KMAX_TAIL_PREREG_V007_SEALED.json'
ADD=CTRL/'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
T=('a99105a19b582c68d961e0ee12be3a2efa79dbd1e65d63682c3d2d8daa55f0ab','b2989012c92161a7da3dd10d0148e1607422416d369fc4ebe164217758b5c695','c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1','UNT_KMAX_TAIL_COMPARISON_C2V007_R11','0'*64)
R10=B/'calib_tail_readiness_cx2/v006r10_c4';PH=B/'h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4'
POL=R10/'adoption_policy_cx2v006r10_c4.py';CORE=R10/'calibration_core_cx2v006r10_c4.py'
WRAP=B/'h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py';ENTRY=B/'h3_campaign_path_c2/h3_campaign_entry_c2v004.py'
phnames=['adoption_policy_cx2v006r12_c4.py','calibration_core_cx2v006r12_c4.py','calibration_orchestrator_cx2v006r12_c4_q5b1.py','h3_campaign_entry_cx2v006r12_c4.py']
expected=['93d9c0acdb3e9fd40ec63ed0db7c1356b6d2b025eeb5bcde57a2ffebdbd04ba3','192d086348fed9307da99732c0ef146bb336a3d605afc1e9e56b6ce959ad1a73','381fa2957edabf18032afba9a8ff026744f6cc1d933efb5f3d30f289ea9decb9','dd9c951bbe2a374ff56059a392b49e65d3ca369d849b307e7365d28226c0b116']
parentpins=['93d9c0acdb3e9fd40ec63ed0db7c1356b6d2b025eeb5bcde57a2ffebdbd04ba3','dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6','7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229','cbdf0d49b8bfa09bccf8ba1ebfb518f8c00b663c2564db7c3a02c8b7a86e116d']
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
def changes(a,b):
 aa=a.decode().splitlines(keepends=True);bb=b.decode().splitlines(keepends=True)
 if len(aa)!=len(bb):raise ValueError('line count changed')
 return [{'line':i,'before':x.rstrip('\n'),'after':y.rstrip('\n')} for i,(x,y) in enumerate(zip(aa,bb),1) if x!=y]
def seals(raw):
 nodes=[n.value for n in ast.parse(raw).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='APPROVED_V007_SEALS' for t in n.targets)]
 assert len(nodes)==1;n=nodes[0];assert isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='frozenset' and not n.keywords
 return frozenset(ast.literal_eval(n.args[0])) if n.args else frozenset()
now=subprocess.check_output(['/bin/date','-u'],text=True).strip()
assert sha(G.read_bytes())=='a7a5fe58d509b99f14cb000305633c6f192ac71f5093f4ec5fa1a2fa6f1a1f35'
assert sha(CMP.read_bytes())==T[0] and sha(PRE.read_bytes())==T[1]
# Only these source lines are semantically inspected; the entire file is hashed.
const={}
for line_no in [172,188,364]:
 line=CMP.read_bytes().decode().splitlines()[line_no-1];node=ast.parse(line).body[0];const[node.targets[0].id]=ast.literal_eval(node.value)
assert (const['V007_PREREG_SHA256'],const['PIN_ADDENDUM_V005'],const['SCHEMA_REPORT'])==T[1:4]
assert not seals(POL.read_bytes())
S.mkdir()
allow={str(p) for p in [G,CMP,PRE,ADD,POL,CORE,WRAP,ENTRY,*[PH/n for n in phnames],B/'calib_tail_readiness_cx2/v006r7/adoption_policy_cx2v006r7.py',B/'calib_tail_readiness_cx2/v006r9/calibration_core_cx2v006r9.py',B/'calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py']}
audit_state={'denials':[],'generator_read_paths':set()}
def audit(event,args):
 if event in ['subprocess.Popen','os.system','os.fork','os.posix_spawn','os.remove','os.rmdir','os.rename','os.symlink'] or event.startswith('socket.'):
  audit_state['denials'].append(event);raise PermissionError(event)
 if event=='os.mkdir' and not Path(args[0]).absolute().is_relative_to(H):raise PermissionError('mkdir outside lane')
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=Path(os.fsdecode(args[0])).absolute();mode,flags=args[1:];writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)
  if writing:
   if not p.is_relative_to(H) or not isinstance(flags,int) or not flags&os.O_EXCL:raise PermissionError('nonexclusive or outside-lane write')
  elif str(p) not in allow and not p.is_relative_to(H) and not p.is_relative_to(Path(sys.base_prefix)):
   audit_state['denials'].append(str(p));raise PermissionError('read not on prep allowlist: '+str(p))
  elif str(p) in allow:audit_state['generator_read_paths'].add(str(p))
sys.addaudithook(audit)
buf=io.StringIO();old=sys.argv
sys.argv=[str(G),str(S),'v006r11_c4','--write','--policy-only','--seal-tuple',*T]
try:
 with contextlib.redirect_stdout(buf):runpy.run_path(str(G),run_name='__main__')
finally:sys.argv=old
result=json.loads(buf.getvalue());new=S/'v006r11_c4/adoption_policy_cx2v006r11_c4.py';delta=changes(POL.read_bytes(),new.read_bytes())
assert len(result['outputs'])==1 and len(list(new.parent.iterdir()))==1
assert len(delta)==2 and seals(new.read_bytes())==frozenset({T})
assert delta[0]['before']=='# No final V007 seal has been supplied. A root-reviewed immutable successor'
assert delta[1]['before']=='APPROVED_V007_SEALS = frozenset()'
assert delta[0]['after'].startswith('# The V007 seal tuple below was registered')
assert delta[1]['after']=='APPROVED_V007_SEALS = frozenset({'+repr(T)+'})'
ph=[]
for name,parent,want,oldsha,lines in zip(phnames,[POL,CORE,WRAP,ENTRY],expected,parentpins,[[],[200],[29],[60,61]]):
 p=PH/name;assert sha(p.read_bytes())==want and sha(parent.read_bytes())==oldsha
 d=changes(parent.read_bytes(),p.read_bytes());assert [x['line'] for x in d]==lines
 ph.append({'placeholder':pin(p),'parent':pin(parent),'diffs':d,'passed':True})
rec={'schema':'CX3_A205_DIFF_PREP_V002','date_u':now,'status':'READY_FOR_NAMED_VERDICT_INPUTS','generator':pin(G),'checker':pin(Path(__file__)),'sealed_compare':pin(CMP),'sealed_prereg':pin(PRE),'constants':const,'inert_tuple':T,'generated_inert_policy':pin(new),'policy_diff':delta,'placeholder_checks':ph,'audit':{'denials':audit_state['denials'],'allowed_paths_read':sorted(audit_state['generator_read_paths'])},'disclosure':'Codex3 revised prior launch-packet pieces feeding V and also holds campaign review, policy signing and per-wave signing. This checks bytes/tuple identity, not independent verdict content.','untested':['Actual verdict and final chain','Production admission','Verdict field-selection exception pending root clarification']}
for name,obj in [('GENERATOR_RESULT_CX3V002.json',result),('PREP_RESULT_CX3V002.json',rec)]:
 with (H/name).open('x') as f:json.dump(obj,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'inert_policy_sha256':pin(new)['sha256'],'policy_diff_lines':[x['line'] for x in delta],'placeholder_diffs':[[x['line'] for x in z['diffs']] for z in ph],'result':pin(H/'PREP_RESULT_CX3V002.json'),'audit_denials':audit_state['denials']}))
