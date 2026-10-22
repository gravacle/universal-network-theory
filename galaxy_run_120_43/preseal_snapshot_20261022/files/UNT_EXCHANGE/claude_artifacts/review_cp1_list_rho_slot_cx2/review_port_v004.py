import copy,hashlib,json,sys,types,subprocess,datetime
# Independent 0824 review port: original source pinned; output policy redirects
# only to this new review directory. CLI is exercised in process, never in a
# child. The positive fixture spans all 27 requested row identifiers.
import io,contextlib,os
_REVIEW_ROOT='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_cp1_list_rho_slot_cx2'
_READS=[]
def _review_audit(event,args):
 if event in ('subprocess.Popen','os.system','os.fork','os.posix_spawn','os.rename','os.remove','os.rmdir'):
  raise AssertionError('REVIEW_FENCE:'+event)
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  name=os.path.realpath(os.fsdecode(args[0]));flags=args[2]
  writing=isinstance(flags,int) and bool(flags & (os.O_WRONLY|os.O_RDWR))
  if writing:
   if not name.startswith(_REVIEW_ROOT+os.sep) or os.path.lexists(name):raise AssertionError('WRITE_FENCE:'+name)
  else:
   if '/.codex/' in name or '/runs_ext/' in name or '/V007_POSTSEAL_RECORDS/' in name or 'NGC3198' in os.path.basename(name):raise AssertionError('READ_FENCE:'+name)
   if ('/cp1_run_' in name or '/RHO_NUMERIC_' in name or '/EPS_NUMERIC_' in name or '/EPS_PROOF_' in name or '/GQ_PROOF_' in name) and not name.startswith(_REVIEW_ROOT+os.sep):raise AssertionError('LIVE_CP1_FENCE:'+name)
   _READS.append(name)
import sys
sys.addaudithook(_review_audit)

from pathlib import Path
D=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_cp1_list_rho_slot_cx2');T=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cp1_list_rho_slot_cx1/cp1_list_rho_slot_cx1v004.py')
m=types.ModuleType('candidate');source=T.read_bytes();assert hashlib.sha256(source).hexdigest()=='820d16a53920b3d956d18b2bf5e0b18cf1a8c65f52210624562e2ad218e631c2';exec(compile(source,str(T),'exec'),m.__dict__);m.OUTPUT=D
F=D/'inert_fixtures'/datetime.datetime.now(datetime.timezone.utc).strftime('case_%Y%m%dT%H%M%S%f');F.mkdir(parents=True)
R=F/'cp1_run_inert';R.mkdir()
def put(name,obj):
 p=F/name;p.parent.mkdir(parents=True,exist_ok=True);b=m.encode(obj)
 with p.open('xb') as f:f.write(b)
 return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest()}
s=m.Snapshot();H,P,C,S,shim=m.setup(s)
ap=[{'path':C['PINS'][n][0],'sha256':C['PINS'][n][1]} for n in C['CANONICAL_APPROVED_PRODUCERS']]
approved=put('approved.json',{'approved_certificate_producers':ap})
producer={'path':str(m.ART/'calib_tail_readiness_cx2/certificates_per_point/point_response_producer_cx2v002.py'),'sha256':S['RESPONSE_SHA']}
cust={k:'a'*64 for k in H.CUSTODY_KEYS}
def rho(ident,nonce):
 return {'schema':S['RHO_SCHEMA'],'gate':S['RHO_GATE'],'status':'TESTED','verdict':S['RHO_VERDICT'],'settings':'registered','full_registered_search_executed':True,'coverage_complete':True,'required_coverage_inverse_kpc':S['RHO_COVERAGE'],'shells':[{'range_inverse_kpc':p} for p in S['RHO_PARTITION']],'producer':producer,'identity':ident,'point_sha256':m.digest(ident),'custody':cust,'inert_nonce':nonce}
table,_=H.table();anchor_spec=s.doc(table[0]['spec_path'],table[0]['spec_sha256']);aid=H.point_identity(anchor_spec,C['DRIVER_SHA']);assert m.digest(aid)==S['ANCHOR_KEY']
pair=[put('anchor_'+t+'.json',rho(aid,t)) for t in ['a','b']]
anchor=put('anchor_registration.json',{'anchor_rho_pair':pair,'registered_rho_records':pair})
points=[]
for i in range(27):
 spec={'physical':{'distance_Mpc':4.04,'synthetic_axis':i},'coefficients':{},'numerics':{'uv_tail':{'eps_certificate':'PENDING','lo_certificate':'PENDING'}}}
 ident=H.point_identity(spec,C['DRIVER_SHA']);key=m.digest(ident);k=key[:16];label='INERT_%d'%i;row=([300,301,302]+list(range(400,412))+list(range(500,512)))[i]
 sp=put('spec%d.json'%i,spec);point={'row':row,'key':key,'label':label,'spec':sp,'theta':{'inert':i},'pending_spec_sha256':sp['sha256']};points.append(point)
 folder='cp1_run_inert/P%02d_%s_%s_a1'%(row,k,label)
 rr=put(folder+'/RHO_NUMERIC_'+k+'_a.json',rho(ident,'point'))
 er=put(folder+'/EPS_NUMERIC_'+k+'.json',{'schema':H.EPS_NUMERIC_SCHEMA,'identity':ident,'settings':'registered','full_registered_search_executed':True,'custody':cust,'producer':{'inert':True},'dependencies':{'inert':True}})
 for gate,prod in [('EPS',ap[0]),('GQ',ap[1])]:
  p={'schema':C['PROOF_SCHEMA'],'gate':gate,'status':'TESTED','verdict':'PASS','point_sha256':key,'custody_sha256':m.digest(cust),'producer':prod}
  if gate=='EPS':p['driver_certificate']=er
  else:p.update(all_production_kperp_nodes=True,nodes_tested=2,production_nodes=2)
  put(folder+'/'+gate+'_PROOF_'+k+'.json',p)
lst={'schema':'H3_CAMPAIGN_POINTS_LIST_C2V003','wave':3,'points':points};lp=put('points.json',lst);keys=[x['key'] for x in points]
base=[sys.executable,'-I','-B',str(T)]
args=['--points-list',lp['path'],'--points-list-sha256',lp['sha256'],'--out-root',str(R),'--anchor-registration',anchor['path'],'--anchor-registration-sha256',anchor['sha256'],'--approved-producers',approved['path'],'--approved-producers-sha256',approved['sha256']]
for key in keys:args+=['--key',key]
rows=[]
def cli(name,command,extra,good=True,override=None):
 out=F/name
 saved_argv=sys.argv;buffer=io.StringIO()
 try:
  sys.argv=[str(T),command]+(args if override is None else override)+['--output-dir',str(out)]+extra
  with contextlib.redirect_stdout(buffer):code=m.main()
 finally:sys.argv=saved_argv
 r=types.SimpleNamespace(returncode=code,stdout=buffer.getvalue(),stderr='')
 j=json.loads(r.stdout);assert (r.returncode==0)==good,(name,r.stdout,r.stderr)
 if not good:assert not out.exists()
 rows.append({'case':name,'PASS':True,'status':j['status'],'reason':j.get('reason')});return j
reg=cli('registered','register',[])['outputs']['RHO_REGISTRATION.json']
stageargs=['--registration',reg['path'],'--registration-sha256',reg['sha256'],'--slot-out-root',str(m.ART/'s4rc1_c3/lo_slot_INERT_NEVER_EXECUTE'),'--bundle-out-root',str(m.ART/'s4rc1_c3/registry_INERT_NEVER_EXECUTE')]
st=cli('staged','stage',stageargs)
assert sum(n.startswith('FILLED_SPEC') for n in st['outputs'])==27
assert sum(n.startswith('SLOT_ARGS') for n in st['outputs'])==27
commands=Path(st['outputs']['COMMANDS.txt']['path']).read_text();assert commands.count('lo_slot_proof_c3v003.py')==27 and commands.count('cp1_points_assembler_c2v001.py')==27
# CLI refusal matrix; every mutation is a new file, no overwrites.
def replace(a,flag,value):
 a=list(a);a[a.index(flag)+1]=value;return a
cli('bad_list_sha','register',[],False,replace(args,'--points-list-sha256','0'*64))
cli('wrong_selection','register',[],False,replace(args,'--key','f'*64))
for name,change in [('wrong_key',lambda x:x['points'][0].update(key='f'*64)),('table_key',lambda x:x['points'][0].update(key=table[0]['key'])),('table_label',lambda x:x['points'][0].update(label=C['POINTS'][0][3][0]))]:
 obj=copy.deepcopy(lst);change(obj);p=put(name+'.json',obj);aa=replace(replace(args,'--points-list',p['path']),'--points-list-sha256',p['sha256']);cli(name,'register',[],False,aa)
p=put('missing_anchor.json',{'registered_rho_records':pair});aa=replace(replace(args,'--anchor-registration',p['path']),'--anchor-registration-sha256',p['sha256']);cli('missing_anchor','register',[],False,aa)
x=json.loads(Path(reg['path']).read_bytes());x['registered_rho_records']=pair;p=put('unregistered.json',x);ex=replace(replace(stageargs,'--registration',p['path']),'--registration-sha256',p['sha256']);cli('unregistered_rho','stage',ex,False)
# Direct staging invariant mutation: corrupt one filled slot and require refusal.
ss=m.Snapshot();registration,pts,_,_=m.collect(ss,lp,str(R),keys,anchor,approved)
f=copy.deepcopy(pts[0]['spec']);f['numerics']['uv_tail'].update(lo_certificate=pair[0],eps_certificate=pts[0]['eps_ref'])
try:m.filled_check(pts[0]['spec'],f,pts[0]['rho_ref'],pts[0]['eps_ref'],registration['registered_rho_records']);raise AssertionError('slot mutation accepted')
except m.Refusal as e:rows.append({'case':'slot_not_pin','PASS':True,'reason':str(e)})
# Count actual OS open audit events while validating; does not trust Snapshot's counters.
watch=False;opens={}
def audit(event,a):
 if watch and event=='open' and isinstance(a[0],str):opens[a[0]]=opens.get(a[0],0)+1
sys.addaudithook(audit);watch=True
ss=m.Snapshot();m.collect(ss,lp,str(R),keys,anchor,approved)
watch=False
assert opens and max(opens.values())==1,opens
rows.append({'case':'actual_single_read_audit','PASS':True,'files':len(opens),'max_opens':max(opens.values())})
exec(compile((D/'additional_checks_v004.py').read_bytes(),str(D/'additional_checks_v004.py'),'exec'),globals())
report={'review_dispatch':'0824','requested_row_ids':[300,301,302]+list(range(400,412))+list(range(500,512)),'subprocesses':0,'actual_live_record_reads':[],'read_paths':sorted(set(_READS)),'verdict':'PASS','tests':rows,'helper':{'path':str(T),'sha256':hashlib.sha256(T.read_bytes()).hexdigest()},'fixtures':str(F),'scope':'Inert synthetic records only; real pinned source code, rulings and anchor template read. No real CP1 record files opened; no proof/producer/solver launched. CLI register and stage tested.','production':'UNTESTED; independent Codex3 review and root verification required'}
p=F/'TEST_REPORT.json'
with p.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps({'verdict':'PASS','tests':len(rows),'report':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
