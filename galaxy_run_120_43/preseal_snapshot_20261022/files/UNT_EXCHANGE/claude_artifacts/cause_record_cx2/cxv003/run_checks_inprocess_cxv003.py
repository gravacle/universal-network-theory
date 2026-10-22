"""In-process synthetic checks only; no child commands, science runs or production data."""
import contextlib,hashlib,io,json,os,sys
from pathlib import Path
ROOT=Path(__file__).parent
forbidden=[]
def fence(event,args):
 if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.posix_spawn','socket.connect','socket.bind','os.remove','os.rmdir','os.rename','os.replace'):
  forbidden.append(event);raise RuntimeError('AUDIT_DENIED '+event)
 if event=='open' and isinstance(args[0],(str,bytes)):
  path=os.path.abspath(os.fsdecode(args[0]))
  if path.startswith('/Volumes/') or '/.codex/' in path or 'V007_POSTSEAL_RECORDS' in path or 'NGC3198' in os.path.basename(path):
   forbidden.append('open:'+path);raise RuntimeError('PRODUCTION_READ_DENIED')
  flags=args[2]
  if type(flags) is int and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
   if not path.startswith(str(ROOT)+'/') or os.path.lexists(path):
    forbidden.append('write:'+path);raise RuntimeError('NONEXCLUSIVE_WRITE_DENIED')
 if event=='os.link' and os.path.lexists(args[1]):raise RuntimeError('EXISTING_LINK_DENIED')
sys.addaudithook(fence)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
 p=ROOT/name
 with p.open('x') as f:json.dump(obj,f,sort_keys=True,indent=2);f.write('\n')
 return {'path':str(p),'sha256':sha(p)}
test=ROOT/'test_cause_cxv003.py';code=compile(test.read_bytes(),str(test),'exec')
def run(module=None):
 sys.argv=[str(test)]+([str(module)] if module else [])
 ns={'__name__':'inert_test','__file__':str(test)};buf=io.StringIO()
 with contextlib.redirect_stdout(buf):exec(code,ns)
 return ns,json.loads(buf.getvalue())
ns,result=run();assert result['count']==59 and result['pass']
regular=save('CAUSE_TESTS_CXV003.json',result)
src=(ROOT/'cause_record_cxv003.py').read_text()
mutations=[
 ('finish_association',"if fin.get(('result_path',))!=rp or fin.get(('result_sha256',))!=rh or fin.get(('status',))!=status:","if False:"),
 ('all_to_any',"all(s.get('model_outcome') is True for s in found)","any(s.get('model_outcome') is True for s in found)"),
 ('empty_allowed',"if not found or not all(s.get('model_outcome') is True for s in found):","if not all(s.get('model_outcome') is True for s in found):"),
 ('ngc_gate',"if lane=='NGC':","if False:"),
 ('generic_exhaustion',"if status != 'ROUTE_A_NO_FIXED_POINT':","if status not in ('FAILED','ROUTE_A_NO_FIXED_POINT'):"),
 ('solo',"s.get(('solo_mode',)) is not True","False"),
 ('module_pin',"reader.read(module['path'],module['sha256'])","reader.read(module['path'],None)"),
 ('remove_outcome_gate',"  if status=='ROUTE_A_NO_FIXED_POINT' and outcome not in ('CONVERGED_FINITE_FIXED_POINT','FAILED_SOURCE_PREPARATION','ITERATION_BUDGET_EXHAUSTED'):return no('ROUTE_A_OUTCOME_MISSING_OR_UNKNOWN')\n",'')]
rows=[]
for i,(label,old,new) in enumerate(mutations,1):
 assert src.count(old)==1,label
 p=ROOT/('CXV003_MUTANT_M%02d.py'%i)
 with p.open('x') as f:f.write(src.replace(old,new))
 killed=False;reason=''
 try:run(p)
 except AssertionError as exc:killed=True;reason=str(exc)
 rows.append({'name':label,'killed':killed,'failure':reason,'path':str(p),'sha256':sha(p)})
assert all(x['killed'] for x in rows)
mutants=save('CAUSE_MUTANTS_CXV003.json',rows)
# Exercise the real main() in-process; inject only inert driver and vocabulary.
m=ns['m'];m.DRIVERS=ns['drivers'];m.VOCABULARIES=ns['vocabulary'](ns['driver'])
cli=[]
for monitor_status in ('CHILD_FAILED','FAILED'):
 for driver_status in ('FAILED','FAILED_AT_STAGE','ROUTE_A_NO_FIXED_POINT'):
  ff=ns['fixture'](ns['changed'](lambda r:r.update(status=driver_status)),mon_change=lambda r:r.update(status=monitor_status))
  for missing_finish in (False,True):
   out=ns['root']/('cause_'+monitor_status+'_'+driver_status+('_missing_finish' if missing_finish else '')+'.json')
   sys.argv=['inert_cause','classify','--receipt',*ff[0],'--finish',str(ns['root']/'missing_finish_cli') if missing_finish else ff[1],'--out',str(out)]
   with contextlib.redirect_stdout(io.StringIO()):assert m.main()==0
   row=json.loads(out.read_bytes());assert set(row)==set(ns['a']) and type(row['model_outcome']) is bool
   if missing_finish or monitor_status=='FAILED' or driver_status!='ROUTE_A_NO_FIXED_POINT':assert row['model_outcome'] is False
   cli.append({'monitor_status':monitor_status,'driver_status':driver_status,'missing_finish':missing_finish,'pass':True,'model_outcome':row['model_outcome'],'reason':row['model_outcome_reason'],'path':str(out),'sha256':sha(out)})
cli_pin=save('CAUSE_CLI_TOTALITY_CXV003.json',{'pass':True,'count':len(cli),'cases':cli})
assert not forbidden,forbidden
summary={'status':'TESTED_PASS','scope':'in-process synthetic metadata only; no production runs or data','tests':59,'mutants_killed':8,'cli_cause_rows':12,'forbidden_events':forbidden,'sources':[{'path':str(ROOT/n),'sha256':sha(ROOT/n)} for n in ('cause_record_cxv003.py','test_cause_cxv003.py','run_checks_inprocess_cxv003.py','metadata_selector_cx1v002.py','CAUSE_VOCABULARY_CXV002.json')],'evidence':[regular,mutants,cli_pin]}
print(json.dumps(save('CAUSE_VERIFICATION_CXV003.json',summary),sort_keys=True))
print(json.dumps({k:summary[k] for k in ('status','tests','mutants_killed','cli_cause_rows','forbidden_events')},sort_keys=True))
