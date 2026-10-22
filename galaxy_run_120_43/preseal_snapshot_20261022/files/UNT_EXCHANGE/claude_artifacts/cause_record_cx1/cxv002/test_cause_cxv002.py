import copy,hashlib,importlib.util,json,os,sys,tempfile
from pathlib import Path
module=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('cause_record_cxv002.py')
s=importlib.util.spec_from_file_location('tested_cause',module);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
root=Path(tempfile.mkdtemp(prefix='cx1_cause_inert_'));n=0;checks=[];opens={}
def audit(event,args):
 if event=='open' and isinstance(args[0],(str,bytes)) and str(args[0]).startswith(str(root)):
  opens[str(args[0])]=opens.get(str(args[0]),0)+1
sys.addaudithook(audit)
def put(obj,suffix='.json'):
 global n
 n+=1;p=root/(str(n)+suffix);raw=obj if isinstance(obj,bytes) else json.dumps(obj).encode()
 with p.open('xb') as f:f.write(raw)
 return str(p),hashlib.sha256(raw).hexdigest()
source=b"try:\n pass\nexcept RouteANoFixedPoint:\n status = 'ROUTE_A_NO_FIXED_POINT'\noutcome = 'ITERATION_BUDGET_EXHAUSTED'\n"
driver=put(source,'.py');drivers={driver[1]:'DDO'};spec='a'*64
base={'status':'ROUTE_A_NO_FIXED_POINT','route_a_outcome':{'outcome':'NONCONVERGENCE'},'stage_records':[{'name':'01_route_a','exit_code':0}], 'predictions':[{'value':1e99,'secret':'DO_NOT_DECODE'}]}
def fixture(res=None,mon_change=None,fin_change=None,dp=driver):
 rp=put(base if res is None else res)
 mon={'status':'CHILD_FAILED','driver_status':(base if res is None else res)['status'],'exit_code':3,'stop_reason':None,'result':{'path':rp[0],'sha256':rp[1]},'pins':{'spec':{'sha256':spec},'driver':{'path':dp[0],'sha256':dp[1]}}}
 if mon_change:mon_change(mon)
 receipt=put(mon);fin={'status':mon['driver_status'],'result_path':rp[0],'result_sha256':rp[1]}
 if fin_change:fin_change(fin)
 return receipt,put(fin)[0]
def vocabulary(dp,extra=None):
 sites=m.sites(Path(dp[0]).read_bytes())
 modules=[{'path':dp[0],'sha256':dp[1],'sites':[dict(x,token=t,model_outcome=True) for t,rows in sites.items() for x in rows]}]
 return {dp[1]:{'complete':True,'modules':modules+(extra or [])}}
def run(f,ds=drivers,att=None,vs=None):
 mon=json.loads(Path(f[0][0]).read_bytes());d=mon['pins']['driver'];dp=(d['path'],d['sha256'])
 return m.classify(*f,post_seal=att,drivers=ds,vocabularies=vocabulary(dp) if vs is None else vs)
def check(name,v):
 checks.append({'name':name,'pass':bool(v)})
 if not v:raise AssertionError(name)
def changed(fn):r=copy.deepcopy(base);fn(r);return r
f=fixture();v=vocabulary(driver);opens.clear();a=m.classify(*f,drivers=drivers,vocabularies=v);check('route_a_positive',a['model_outcome']);check('single_read_all_inputs',len(opens)==4 and all(v==1 for v in opens.values()))
check('exact_output_fields',set(a)==set('status failing_stage failure_code exception_class raise_site bound_shas model_outcome model_outcome_reason'.split()))
check('exhaustion_positive',run(fixture(changed(lambda r:r['route_a_outcome'].update(outcome='ITERATION_BUDGET_EXHAUSTED'))))['model_outcome'])
check('generic_valueerror',not run(fixture(changed(lambda r:r.update(status='FAILED'))))['model_outcome'])
check('exhaustion_then_generic_failure',not run(fixture(changed(lambda r:(r.update(status='FAILED'),r['route_a_outcome'].update(outcome='ITERATION_BUDGET_EXHAUSTED')))))['model_outcome'])
for code in (-9,137,143,1):check('stage_exit_'+str(code),not run(fixture(changed(lambda r:r['stage_records'][0].update(exit_code=code))))['model_outcome'])
check('monitor_signal',not run(fixture(mon_change=lambda r:r.update(exit_code=-9)))['model_outcome'])
check('missing_finish',not run((f[0],str(root/'missing')))['model_outcome'])
check('tampered_receipt',not run(((f[0][0],'0'*64),f[1]))['model_outcome'])
check('tampered_result',not run(fixture(mon_change=lambda r:r['result'].update(sha256='0'*64)))['model_outcome'])
check('tampered_finish',not run(fixture(fin_change=lambda r:r.update(result_path='/inert/wrong')))['model_outcome'])
check('excluded_source',not run(fixture(changed(lambda r:r['route_a_outcome'].update(outcome='FAILED_SOURCE_PREPARATION'))))['model_outcome'])
check('empty_stage_record',not run(fixture(changed(lambda r:r['stage_records'].append({}))))['model_outcome'])
check('nonobject_stage',not run(fixture(changed(lambda r:r['stage_records'].append(4))))['model_outcome'])
check('duplicate_route_stage',not run(fixture(changed(lambda r:r['stage_records'].append({'name':'route_a','exit_code':0}))))['model_outcome'])
for label,src in [('ambiguous',source+b"status='ROUTE_A_NO_FIXED_POINT'\n"),('missing',b'pass\n')]:
 dp=put(src,'.py');check(label+'_site',run(fixture(dp=dp),{dp[1]:'DDO'})['model_outcome']==(label=='ambiguous'))
ngc={driver[1]:'NGC'};opens.clear();check('ngc_requires_attestation',not m.classify(*f,drivers=ngc,vocabularies=v)['model_outcome']);check('ngc_no_run_open',set(opens)=={f[0][0]})
att=put({'status':'POST_SEAL_ATTESTED','authority':'Claude2','receipt_sha256':f[0][1],'spec_sha256':spec,'driver_sha256':driver[1]})
check('ngc_attested_positive',run(f,ngc,att)['model_outcome'])
check('ngc_tampered_attestation',not run(f,ngc,(att[0],'0'*64))['model_outcome'])
for label,raw,paths in [('forbidden',b'{}',{('predictions',)}),('duplicate',b'{"status":"X","status":"Y"}',{('status',)}),('container',b'{"status":[]}',{('status',)})]:
 try:m.Selector(raw,'result').select(paths);ok=False
 except m.Refused:ok=True
 check(label+'_refused',ok)
old=m.Selector.string
def spy(self,decode=False):
 if decode and self.raw[self.i:].startswith(b'"DO_NOT_DECODE"'):raise AssertionError('scientific string decoded')
 return old(self,decode)
m.Selector.string=spy
check('skipped_content_not_decoded',run(f)['model_outcome']);m.Selector.string=old
p=put(b'{}');alias=root/'alias';os.link(p[0],alias);opens.clear();reader=m.OneRead();reader.read(p[0]);reader.read(str(alias));check('single_read_alias_inode',sum(opens.values())==1)
b=run(fixture());pa,pb=put(a),put(b)
def solo(c,**kw):
 obj={'receipt_sha256':c['bound_shas']['receipt'],'spec_sha256':spec,'solo_mode':True,'other_ngc_processes_max':0};obj.update(kw);return put(obj)
sa,sb=solo(a),solo(b)
check('pair_positive',m.pair(pa,pb,sa,sb,drivers=drivers)['identical_reproduction'])
check('pair_same_attempt',not m.pair(pa,pa,sa,sa,drivers=drivers)['identical_reproduction'])
check('pair_not_solo',not m.pair(pa,pb,solo(a,solo_mode=False),sb,drivers=drivers)['identical_reproduction'])
for key in ('failing_stage','failure_code','exception_class','raise_site'):
 c=copy.deepcopy(b);c[key]='DIFFERENT';check('pair_diff_'+key,not m.pair(pa,put(c),sa,sb,drivers=drivers)['identical_reproduction'])
extra_dp=put(b"outcome='ITERATION_BUDGET_EXHAUSTED'\n",'.py')
extra={'path':extra_dp[0],'sha256':extra_dp[1],'sites':[{'token':'ITERATION_BUDGET_EXHAUSTED','line':1,'model_outcome':True,'exception_class':'NO_EXCEPTION_OUTCOME'}]}
ex_f=fixture(changed(lambda r:r['route_a_outcome'].update(outcome='ITERATION_BUDGET_EXHAUSTED')))
check('multi_module_all_model',run(ex_f,vs=vocabulary(driver,[extra]))['model_outcome'])
mixed=copy.deepcopy(extra);mixed['sites'][0]['model_outcome']=False
check('mixed_module_set',not run(ex_f,vs=vocabulary(driver,[mixed]))['model_outcome'])
empty=vocabulary(driver);empty[driver[1]]['modules'][0]['sites']=[]
check('empty_set',not run(f,vs=empty)['model_outcome'])
bad=copy.deepcopy(extra);bad['sha256']='0'*64
check('module_hash_tamper',not run(ex_f,vs=vocabulary(driver,[bad]))['model_outcome'])
incomplete=vocabulary(driver);incomplete[driver[1]]['complete']=False
check('incomplete_vocabulary',not run(f,vs=incomplete)['model_outcome'])
check('canonical_set_output',run(ex_f,vs=vocabulary(driver,[extra]))['raise_site'].startswith('SITE_SET:'))
print(json.dumps({'pass':True,'count':len(checks),'checks':checks,'inert_fixture_dir':str(root)},sort_keys=True))
