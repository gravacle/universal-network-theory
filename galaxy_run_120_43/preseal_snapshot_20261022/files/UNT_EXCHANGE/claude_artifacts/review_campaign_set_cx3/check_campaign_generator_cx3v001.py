"""Independent A205 part2 generator regression; generator only, no scientific module executes."""
import ast,contextlib,hashlib,importlib.util,io,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;A=H.parent;D=A/'h3_campaign_path_c2';CX=A/'calib_tail_readiness_cx2'
V=A/'review_verdict_finalization_cx3';G=D/'make_campaign_cascade_c2v004.py';P=A/'b1_policy_successor_c4/tools/make_b1_cascade_c4v002.py'
ctrl=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
allow={str(p) for p in [P,G,*[D/('make_campaign_cascade_c2v00%d.py'%i) for i in range(1,4)],D/'calibration_orchestrator_q5b1_ledger_c2v004.py',D/'h3_campaign_entry_c2v004.py',CX/'v006r7/adoption_policy_cx2v006r7.py',CX/'v006r9/calibration_core_cx2v006r9.py',CX/'v006r9/calibration_orchestrator_cx2v006r9.py',CX/'v006r10_c4/adoption_policy_cx2v006r10_c4.py',CX/'v006r10_c4/calibration_core_cx2v006r10_c4.py',ctrl/'V007_SEAL_ASSEMBLY/kmax_tail_compare_c2v007_r14_cx1v001_SEALED_V007.py',ctrl/'V007_SEAL_ASSEMBLY/KMAX_TAIL_PREREG_V007_SEALED.json',ctrl/'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md']}
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
def load(p,name):
 sp=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
now=subprocess.check_output(['/bin/date','-u'],text=True).strip();reads=set();denied=[]
def audit(e,args):
 if e in ['subprocess.Popen','os.system','os.fork','os.posix_spawn','os.remove','os.rmdir','os.rename','os.symlink'] or e.startswith('socket.'):raise PermissionError(e)
 if e=='os.mkdir' and not Path(args[0]).absolute().is_relative_to(H):raise PermissionError('mkdir outside lane')
 if e=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=Path(os.fsdecode(args[0])).absolute();mode,flags=args[1:];w=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)
  if w:
   if not p.is_relative_to(H) or not isinstance(flags,int) or not flags&os.O_EXCL:raise PermissionError('nonexclusive/outside-lane write')
  elif str(p) not in allow and not p.is_relative_to(H) and not p.is_relative_to(V) and not p.is_relative_to(Path(sys.base_prefix)):
   denied.append(str(p));raise PermissionError('unlisted read '+str(p))
  elif str(p) in allow:reads.add(str(p))
sys.addaudithook(audit)
vc=load(V/'check_verdict_finalization_cx3v002.py','checkv');g=load(G,'gen');assert pin(G)['sha256']=='5014b04f0de3cf2fc0289dcabe519e0056f9395302cfd1b9b4082b4d045b228a'
t=vc.T4+('0'*64,)
rows=[]
def check(n,ok):
 rows.append({'case':n,'passed':bool(ok)});assert ok,n
parent=ast.parse(P.read_bytes())
def node(tree,name):
 for n in tree.body:
  if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name:return ast.dump(n,include_attributes=False)
  if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id==name for x in n.targets):return ast.dump(n.value,include_attributes=False)
 raise ValueError(name)
for i in range(1,5):
 p=D/('make_campaign_cascade_c2v00%d.py'%i);tr=ast.parse(p.read_bytes())
 for name in ['POLICY_REPLACEMENTS','sealed_constants','check_tuple','rep1','pinned']:
  check('v00%d AST identity to v002 parent: %s'%(i,name),node(tr,name)==node(parent,name))
 # Core source and the two replacement calls are copied exactly, independent of wrapper source.
 src=p.read_text();par=P.read_text();start='        core = rep1(core9,';end='        wrap = rep1('
 check('v00%d core-generation source identity'%i,src[src.index(start):src.index(end)]==par[par.index(start):par.index(end)])
scratch=H/'generator_scratch_cx3v001';scratch.mkdir();outputs={}
for tag,sub,tup in [('regression','v006r10_c4',None),('placeholder','v006r12_c4',None),('inert','v006r12_c4',t)]:
 out=scratch/tag;out.mkdir();args=[str(out),sub,'--write']+(['--seal-tuple',*tup] if tup else [])
 with contextlib.redirect_stdout(io.StringIO()):r=g.main(args)
 raw=[(out/sub/n).read_bytes() for n in g.names(sub)];outputs[tag]={'generator_record':r,'files':[pin(out/sub/n) for n in g.names(sub)]}
 if tag=='regression':
  check('G01 policy r10 bytes',raw[0]==(CX/'v006r10_c4/adoption_policy_cx2v006r10_c4.py').read_bytes())
  check('G01 core r10 bytes',raw[1]==(CX/'v006r10_c4/calibration_core_cx2v006r10_c4.py').read_bytes())
  check('G01 wrapper source bytes',raw[2]==Path(g.WRAPQ[0]).read_bytes())
  check('G01 entry WRAPPER path only',vc.changed(Path(g.ENTRY_T[0]).read_bytes(),raw[3])==[60])
 if tag=='placeholder':base=raw
 if tag=='inert':
  check('inert outputs equal independent expected byte chain',raw==vc.expected_chain(base,t))
  check('tuple delta2/1/1/1',[vc.changed(a,b) for a,b in zip(base,raw)]==[[13,16],[202],[29],[61]])
  check('policy same inert A129 bytes',raw[0]==(V/'scratch_prep_v002/v006r11_c4/adoption_policy_cx2v006r11_c4.py').read_bytes())
for name,bad in [('wrong C',('f'*64,*t[1:])),('wrong P',(t[0],'f'*64,*t[2:])),('wrong A',(*t[:2],'f'*64,*t[3:])),('wrong schema',(*t[:3],'WRONG',t[4])),('uppercase V',(*t[:4],'A'*64))]:
 try:
  with contextlib.redirect_stderr(io.StringIO()):g.build('v006r12_c4',seal_tuple=bad)
 except SystemExit as e:check('adversarial '+name,e.code==2)
 else:check('adversarial '+name,False)
rec={'schema':'CX3_A205_CAMPAIGN_GENERATOR_REVIEW_V001','date_u':now,'status':'TESTED','checks':rows,'outputs':outputs,'checker':pin(Path(__file__)),'source_pins':[pin(Path(p)) for p in sorted(reads) if not p.endswith('V005_ADDENDUM.md')],'audit_denials':denied,'disclosure':vc.DISCLOSURE,'untested':['Live verdict publication','Campaign admission and execution']}
p=H/'GENERATOR_REVIEW_CX3V001.json'
with p.open('x') as f:json.dump(rec,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'result':pin(p),'passed':len(rows),'audit_denials':denied}))
