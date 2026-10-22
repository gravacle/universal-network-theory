"""Independent offline arithmetic and custody checks; never imports a producer."""
from pathlib import Path
import sys,json,hashlib,math,re,subprocess,resource
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE')
OUT=BASE/'claude_artifacts/cp1_eps_reviews_cx3'
DISPATCH=BASE/'FROM_CODEX/0852_2026-10-21_claude3_W3_row302_EPS_UNCERTIFIED_analysis_and_EPS_reviews_300_301.md'
RUN=BASE/'claude_artifacts/s4rc1_c3/cp1_run_c3v004b'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pairs(xs):
 d={}
 for k,v in xs:
  if k in d:raise ValueError('duplicate key '+k)
  d[k]=v
 return d
def strict(b):
 x=json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
 def walk(v):
  if isinstance(v,float) and not math.isfinite(v):raise ValueError('nonfinite')
  if isinstance(v,dict):
   for z in v.values():walk(z)
  if isinstance(v,list):
   for z in v:walk(z)
 walk(x);return x
# Hashes below are our first byte snapshot of the four-file scope, not root-supplied pins.
rows={300: ('P300_06c3e863688de635_W0003_P00_a1', '7acd195086dd575dcd36eb78e054b9b464f8c8a6769db95b4bd7468170828f72', '10a887cb787fd746e0aad0c217e031f240a5ce460a5e8d70f2d53b5597842c0e'), 301: ('P301_95540f067efd4a14_W0003_P01_a1', 'ce94f420b30cce2028ca3bd219264947c9166545618953df9a1f6ed03655cb26', 'ae53cf31ac81922fdb0860a46f5764e464390d91ac1c2b70e7aa2a76bbe3bed5')}
selected=[300,301]
for row in selected:
 folder,rh,nh=rows[row];key=folder.split('_')[1]
 blobs={};data={};pins=[]
 for kind in ['EPS_REVIEW_REQUEST','EPS_NUMERIC','STAGE_EPS','STAGE_CONTEXT']:
  path=RUN/folder/(kind+'_'+key+'.json')
  assert 'NGC3198' not in str(path) and path.parent==RUN/folder
  blob=path.read_bytes();blobs[kind]=blob;data[kind]=strict(blob)
  pins.append({'path':str(path),'sha256':sha(blob),'bytes':len(blob)})
 req,num,stage,ctx=[data[k] for k in ['EPS_REVIEW_REQUEST','EPS_NUMERIC','STAGE_EPS','STAGE_CONTEXT']]
 b=req['bindings'];checks={}
 def ck(k,condition):checks[k]=bool(condition)
 ck('request_initial_byte_snapshot',sha(blobs['EPS_REVIEW_REQUEST']).startswith(rh))
 ck('numeric_initial_byte_snapshot',sha(blobs['EPS_NUMERIC']).startswith(nh))
 ck('schema',num['schema']=='UNT_POINT_EPS_NUMERICAL_CX2V001' and b['schema']=='UNT_POINT_EPS_REVIEW_CX2V001')
 ck('point_binding',len(b['point_sha256'])==64 and b['point_sha256'].startswith(key) and all(x==b['point_sha256'] for x in [num['point_sha256'],ctx['point_sha256'],ctx['key'],stage['key']]))
 ck('numeric_pin',b['numeric_ref']==stage['record']=={'path':str(RUN/folder/('EPS_NUMERIC_'+key+'.json')),'sha256':sha(blobs['EPS_NUMERIC'])})
 ck('custody',num['custody']==ctx['custody'] and sha(canon(num['custody']))==ctx['custody_sha256']==b['custody_sha256'])
 ck('context_checks',all(v is True for v in ctx['checks'].values()))
 ck('dependencies_match',num['dependencies']==ctx['source_pins'])
 ck('producer_identity',num['producer']==ctx['source_pins']['producer'] and num['producer']['sha256']=='a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231')
 ck('registered',num['settings']=='registered' and num['full_registered_search_executed'] is True and num['coverage_complete'] is True)
 shells=num['shells'];audits=num['envelope_audit']
 ck('coverage',len(shells)==178 and num['required_coverage_inverse_kpc']==[4,182] and all(s['range_inverse_kpc']==[i,i+1] and s['lo_inverse_kpc']==i and s['hi_inverse_kpc']==i+1 for i,s in enumerate(shells,4)))
 ck('certified',num['registered_discrete_verdict']=='CERTIFIED' and all(s['certified'] is True and type(s['refinements']) is int and s['refinements'] in [0,1] for s in shells))
 audit_map={tuple(a['range_inverse_kpc']):a for a in audits}
 ck('audit_count',len(audits)==len(audit_map)==14 and all(k in {tuple(s['range_inverse_kpc']) for s in shells} for k in audit_map))
 for i,s in enumerate(shells,4):
  env=s['envelope'];a=audit_map.get(tuple(s['range_inverse_kpc']));dense=a['dense'] if a else 0.0
  ck(f'shell_{i}_search',env['torus_m']==12 and env['direction_count']==200 and env['starts']==(8 if i==4 else 9) and env['radial_fractions']==[0,.5,1] and env['n_grid']==12**3*200*3)
  ck(f'shell_{i}_envelope',s['eps_envelope']==max(env['estimate'],dense) and env['estimate']>=env['grid_max']>=0)
  ck(f'shell_{i}_max',s['eps']==max(s['actual']['estimate'],s['eps_base'],s['eps_refined'],s['eps_envelope'],dense) and s['eps']>=s['eps_envelope']>=0)
  ck(f'shell_{i}_actual',s['actual']['estimate']==max(s['actual']['dense_max'],s['actual']['local_max']))
  nf=s['refinements'];levels=s['levels']
  ck(f'shell_{i}_relative_rule',s['eps_refined']<=1.1*s['eps_base'] and (nf==0 or levels['1']['eps']>1.1*levels['0']['eps']))
  ck(f'shell_{i}_level_values',set(levels)==({'0','1'} if nf==0 else {'0','1','2'}) and s['eps_base']==levels[str(nf)]['eps'] and s['eps_refined']==levels[str(nf+1)]['eps'] and all(0<=v['eps']<=s['eps'] for v in levels.values()))
 for a in audits:
  i=int(a['range_inverse_kpc'][0]);ds=a['dense_search'];s=shells[i-4]
  ck(f'audit_{i}_search',ds['torus_m']==20 and ds['direction_count']==400 and ds['starts']==16 and ds['radial_fractions']==[0,.25,.5,.75,1] and ds['n_grid']==20**3*400*5)
  ck(f'audit_{i}_ratio',a['production']>0 and a['production']==s['envelope']['estimate'] and a['dense']==ds['estimate'] and a['dense_over_production']==a['dense']/a['production'])
  ck(f'audit_{i}_dominance',s['eps']>=a['dense']>=ds['grid_max']>=0)
 max_eps=max(s['eps'] for s in shells);max_ranges=[s['range_inverse_kpc'] for s in shells if s['eps']==max_eps]
 ck('maximum',num['eps_max']==stage['eps_max']==max_eps and num['eps_max_shell']==stage['eps_max_shell'] and num['eps_max_shell'] in max_ranges)
 ck('stage',stage['ok'] is True and all(v is True for v in stage['checks'].values()) and stage['record_bytes']==len(blobs['EPS_NUMERIC']) and stage['n_shells']==178 and stage['n_audits']==14)
 ck('stage_timing',stage['seconds']>=0 and stage['cpu_seconds']>=0 and stage['producer_peak_rss_bytes']==num['peak_rss_bytes'] and stage['producer_seconds']==num['seconds'])
 ck('limited_claim',num['rigorous_supremum'] is False and num['production_admissible'] is False and num['covers_all_consumed_states'] is False and num['verdict']==stage['verdict']=='NUMERICAL_RULE_PASSED_REVIEW_REQUIRED')
 ck('distinct_lane','Codex3' not in req['excluded_reviewer_lanes'] and req['excluded_reviewer_lanes']==['Claude2','Codex2'])
 ratios=[a['dense_over_production'] for a in audits]
 result={'schema':'CX3_INDEPENDENT_EPS_W3_0852_V001','row':row,'key16':key,'date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'status':'CHECKS_ONLY_NOT_A_SIGNED_REVIEW','checks':checks,'failed_checks':[k for k,v in checks.items() if not v],'inputs':pins,'script':{'path':str(Path(__file__)),'sha256':sha(Path(__file__).read_bytes())},'dispatch':{'path':str(DISPATCH),'sha256':sha(DISPATCH.read_bytes())},'metrics':{'eps_max':max_eps,'eps_max_shell':num['eps_max_shell'],'dense_ratio_min':min(ratios),'dense_ratio_max':max(ratios),'refined_shells':[s['range_inverse_kpc'] for s in shells if s['refinements']>0],'ratio_to_approx_anchor_2_05e_4':max_eps/2.05e-4,'context_kind':ctx['checks_info']['anchor_context']},'untested':['Optimization rerun','Independent source/provenance rehash except the four permitted files','Adapter execution; byte hash and E1–E10 checklist checked separately by signer'],'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 dest=OUT/('CHECKS_CX3_'+key+'_W3_0852_V001.json')
 with dest.open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
 print(json.dumps({'row':row,'checks':len(checks),'failed_count':len(result['failed_checks']),'first_failures':result['failed_checks'][:5],'metrics':result['metrics'],'path':str(dest),'sha256':sha(dest.read_bytes())}))
