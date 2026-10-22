"""Actual exporter main on synthetic run trees; in-memory synthetic admission."""
import sys,json,hashlib,copy,importlib.util
from pathlib import Path
R=Path(__file__).parent;sys.path.insert(0,str(R))
import producer_guard_cx1v008 as G
D=R/'POSTSEAL_CLI_SYNTH_V003';D.mkdir();G.REGISTERED=()
G.admission=lambda *a,**k:{'_verified_seal':{'driver':{'sha256':'d'*64}}}
G.stamp=lambda o,*a:dict(o,root_admission={'synthetic':True})
import postseal_records_cx1v006 as C
P=R.parent/'v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py'
s=importlib.util.spec_from_file_location('cx1_test_r11',P);M=importlib.util.module_from_spec(s);sys.modules[s.name]=M;s.loader.exec_module(M)
C.comparator=lambda:M
checks=[]
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def put(p,o):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(o,f)
 return pin(p)
def ck(n,fn,refuse=False):
 try:v=fn();ok=not refuse and v is not False;err=None
 except Exception as e:ok=refuse;err=type(e).__name__+': '+str(e)
 checks.append({'name':n,'passed':ok,'error':err})
refs={};b={'verdict':'PASS','max_rel':1e-14,'n':4096,'rtol':1e-12}
for lab in C.CASES:
 root=D/lab;ra=root/'route_a';sc=ra/'uv_tail_sidecar'
 summary={'iteration':0,'state_digest':'1'*64,'next_state_digest':'2'*64,'converged':True}
 it=put(sc/'iteration_0000.json',{'payload':{'iteration':0,'state_digest':'1'*64,'next_state_digest':'2'*64,'summary':summary,'i1t':b,'next_i1t':b}})
 u={'schema':'SYNTHETIC_COMPUTED_RA','M_T_accepted':.1,'M_T_threshold':.25,'flags':[],'monitor_status':'M_T_WITHIN_THRESHOLD','outcome':'CONVERGED_FINITE_FIXED_POINT','accepted_iteration':0,'production_admissible':True,'admissibility':'production','iterations':[summary],'config_sha256':'c'*64,'request_sha256':'3'*64,'boundary_state_digest_at_return':'1'*64}
 files={'iteration_0000.json':it['sha256']};sf=put(sc/'finish_000.json',{'record':copy.deepcopy(u),'files':files})
 u['sidecar']={'directory':str(sc),'finish':sf,'files':files}
 arp=put(ra/'result.json',{'result':{'uv_tail':u}})
 st=root/'ref';put(st/'finish.json',{'uv_tail':{'production_admissible':True,'config_sha256':'c'*64,'i1t':b,'state_digest':'1'*64}})
 result={'status':'COMPLETED','driver_sha256':'d'*64,'normalized_spec':{'galaxy':'DDO154'},'route_a_outcome':{'result_path':arp['path'],'result_sha256':arp['sha256']},'uv_tail':{'route_a_record':u},'stage_records':[{'name':'reference','kind':'reference','executed':True,'argv':['--outdir',str(st)]}]}
 refs[lab]=put(root/'result.json',result);put(root/'finish.json',{'result_sha256':refs[lab]['sha256']})
manifest={'runs':refs};mp=put(D/'manifest.json',manifest)
def run(mode,man,out):
 C.SNAPSHOTS.clear();sys.argv=['producer',mode,str(man),str(out)];C.main();return C.loads(out.read_bytes())
ck('actual_MT_main',lambda:run('MT',Path(mp['path']),D/'MT.json')['verdict']=='PASS')
ck('actual_I1T_main_all_builds',lambda:len(run('I1T',Path(mp['path']),D/'I1T.json')['builds'])==30)
rule={'flag':'SOURCE_QUADRATURE_MATERIAL','run':'C4T','run_result_sha256':refs['C4T']['sha256'],'evidence':'synthetic pinned check','disposition':'CLEARED','reason':'synthetic only','root_decision':'synthetic root decision'}
rp=put(D/'root_rulings.json',{'schema':'UNT_ROOT_FLAG_RULINGS_REQUEST_CX1V001','authority':G.AUTHORITY,'rulings':[rule]})
fp=put(D/'flag_manifest.json',dict(manifest,root_rulings=rp))
ck('actual_FLAG_main',lambda:run('FLAG_RULINGS',Path(fp['path']),D/'FLAG.json')['verdict']=='ROOT_RULINGS')
ck('exclusive_no_overwrite',lambda:run('MT',Path(mp['path']),D/'MT.json'),True)
q=copy.deepcopy(manifest);q['runs'].pop('C2T');bad=put(D/'missing_case.json',q)
ck('missing_case_refused',lambda:run('MT',Path(bad['path']),D/'missing_output.json'),True)
q=copy.deepcopy(manifest);q['runs']['C2T']=q['runs']['C3T'];bad=put(D/'alias.json',q)
ck('aliased_runs_refused',lambda:run('MT',Path(bad['path']),D/'alias_output.json'),True)
q=copy.deepcopy(manifest);q['runs']['C2T']['sha256']='0'*64;bad=put(D/'pin_bad.json',q)
ck('bad_pin_refused',lambda:run('MT',Path(bad['path']),D/'pinbad_output.json'),True)
rp=put(D/'root_duplicate.json',{'schema':'UNT_ROOT_FLAG_RULINGS_REQUEST_CX1V001','authority':G.AUTHORITY,'rulings':[rule,rule]});bad=put(D/'flags_duplicate_manifest.json',dict(manifest,root_rulings=rp))
ck('duplicate_ruling_refused',lambda:run('FLAG_RULINGS',Path(bad['path']),D/'duplicate_output.json'),True)
rule2=dict(rule,run='C3T',run_result_sha256=refs['C3T']['sha256']);rp=put(D/'root_wrong_sqm.json',{'schema':'UNT_ROOT_FLAG_RULINGS_REQUEST_CX1V001','authority':G.AUTHORITY,'rulings':[rule2]});bad=put(D/'wrong_sqm_manifest.json',dict(manifest,root_rulings=rp))
ck('r11_wrong_sqm_refused',lambda:run('FLAG_RULINGS',Path(bad['path']),D/'sqm_output.json'),True)
ck('forbidden_UVT_output',lambda:run('MT',Path(mp['path']),D/'UVT_SYNTHETIC'/'out.json'),True)
# A parser must not stamp or alter source JSON while reading it.
ck('read_preserves_schema_bytes',lambda:C.read(rp)==json.loads(Path(rp['path']).read_bytes()))
# Every entry remains closed if admission is withdrawn after import.
old=G.admission
G.admission=lambda *a,**k:(_ for _ in ()).throw(PermissionError('SYNTHETIC_ADMISSION_WITHDRAWN'))
ck('entry_revalidates_admission',lambda:C.i1_value(b),True);G.admission=old
with (R/'POSTSEAL_CLI_0599_TESTS_V003.json').open('x') as f:json.dump({'scope':'TESTED actual main with synthetic admission/run records; no production files','tests':checks,'source_pins':[pin(R/'postseal_records_cx1v006.py'),pin(P)]},f,indent=1)
print(sum(x['passed'] for x in checks),len(checks));print([x for x in checks if not x['passed']]);assert all(x['passed'] for x in checks)
