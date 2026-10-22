"""Boundary only: execute exact wrapper write_acceptance method with synthetic successful certificate-check stand-in."""
import ast,hashlib,json,subprocess,types
from pathlib import Path
H=Path(__file__).parent;W=H.parent/'h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py';S=H/'handoff_idempotence_scratch_cx3v001';S.mkdir();(S/'out').mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,d):
 with Path(p).open('x') as f:json.dump(d,f,sort_keys=True);f.write('\n')
def read(p,*a):return json.loads(Path(p).read_bytes())
def pin(p):return {'path':str(p),'sha256':sha(p)}
put(S/'spec.json',{'synthetic':'spec'});put(S/'out/result.json',{'synthetic':'result'})
ctx=next(n for n in ast.parse(W.read_bytes()).body if isinstance(n,ast.ClassDef) and n.name=='Context');fn=next(n for n in ctx.body if isinstance(n,ast.FunctionDef) and n.name=='write_acceptance')
e={'Path':Path,'O':types.SimpleNamespace(load_json_file=read,sha256_file=sha,write_json_x=put),'point_identity':lambda s:{'synthetic':True},'Error':ValueError,'__file__':str(W)}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(W),'exec'),e)
C=type('SyntheticContext',(),{'write_acceptance':e['write_acceptance'],'certificate_record':lambda s,i:{'bundle':{'path':'SYNTHETIC_PRE','sha256':'a'*64}},'certificate_check':lambda *a,**kw:{'ok':True}});c=C()
b={'path':'SYNTHETIC_ACCEPTED','sha256':'b'*64};r1=c.write_acceptance(S,b);before=pin(S/'TAIL_CERTIFICATE_ACCEPTANCE.json');r2=c.write_acceptance(S,b);after=pin(S/'TAIL_CERTIFICATE_ACCEPTANCE.json')
assert r1['ok'] and r2['ok'] and before==after
try:c.write_acceptance(S,dict(b,sha256='c'*64))
except ValueError as ex:why=str(ex)
else:raise AssertionError('different handoff accepted')
assert 'immutable handoff already differs' in why and pin(S/'TAIL_CERTIFICATE_ACCEPTANCE.json')==before
rec={'schema':'CX3_HANDOFF_IDEMPOTENCE_BOUNDARY_V001','date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'status':'TESTED','same_handoff_repeat_ok_no_byte_change':True,'different_handoff_refused':why,'source':pin(W),'method_lines':'320-340','checker':pin(Path(__file__)),'scope':'Isolated write_acceptance; certificate check is a declared synthetic stand-in. Not a whole VALID reingest or proof-science test. FORMAL: existing identical handoff is idempotent, so blanket refusal-on-existence is stronger than this method. No wrong admission demonstrated; A115 non-blocking note.','disclosure':'Codex3 holds generator/output-diff review, campaign review, policy signing and per-wave signing.'}
p=H/'HANDOFF_IDEMPOTENCE_CX3V001.json';put(p,rec);print(json.dumps(pin(p)))
