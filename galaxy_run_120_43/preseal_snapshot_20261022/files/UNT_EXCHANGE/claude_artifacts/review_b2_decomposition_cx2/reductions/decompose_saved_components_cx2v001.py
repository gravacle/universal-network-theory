"""A97 independent static saved-component readout and per-row telescoping.
No producer/module/stage import or scientific launch. Exact new C2/C3/C4 OFF array
allowlist; never follow other saved pointers. Existing B2 tR components are inputs.
"""
import os, sys, json, hashlib, math, stat, resource, time, struct, zipfile
from pathlib import Path
import numpy as np

A='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
G=A+'gate_b2_c3/'
BASE=A+'review_b2_decomposition_cx2/reductions/'
RUN=BASE+'run_'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())+'_'+str(os.getpid())+'/'
os.mkdir(RUN)
SAFE={__file__,G+'out/B2_GATE_RECORD_C3V002.json',G+'scripts/b2_independent_c3v001.py',
 A+'uv_tail_study_c2/check/adv_tail_check_v001.py',
 A+'uv_tail_study_c2/check/ADV_TAIL_CHECK_C2_KB12_W025_O6_V001.json',
 A+'uv_tail_study_c2/check/ADV_TAIL_CHECK_C3C4_KB12_W025_O6_V001.json',
 '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0618_2026-10-18_claude3_codex2_B2_sanity_decomposition_A97.md'}
for st in ('C2R3','C3R3','C4R3'):
 for suffix in ('.json','.npz'):SAFE.add(G+'out/path2/IND_'+st+'_BASE'+suffix)
 SAFE.add(G+'out/path1/'+st+'_CM_ON/observation/result.json')
PINS={}; ACCESS=[]; DENIED=[]; TESTS=[];start=time.monotonic()
original_stat=os.lstat;original_readlink=os.readlink
def ban(p):
 if isinstance(p,int) or p is None:return
 s=os.fsdecode(p);parts=s.replace('\\','/').lower().split('/')
 if any(x.startswith('uvt_') or 'c5h' in x or x in ('.codex','.vol') for x in parts) or any(x in s.lower() for x in ('observed_veloc','target_veloc')):
  DENIED.append(s);raise PermissionError('PROTECTED')
def lexical(p):return os.path.abspath(os.fsdecode(p))
def permit(p,op):
 if isinstance(p,int) or p is None:return
 p=lexical(p);ban(p)
 if p in SAFE or p.startswith(RUN):return
 if op=='metadata' and any(x.startswith(p.rstrip('/')+'/') for x in SAFE|{RUN}):return
 DENIED.append(p);raise PermissionError('NOT_EXACT_ALLOWLIST')
def audit(e,a):
 if e=='open':
  p,mode,flags=a;permit(p,'open')
  if isinstance(p,(str,bytes,os.PathLike)):
   ACCESS.append(lexical(p))
   if flags&(os.O_WRONLY|os.O_RDWR) and (not lexical(p).startswith(RUN) or not flags&os.O_EXCL):raise PermissionError('EXCLUSIVE_OUTPUT_ONLY')
 if e in ('os.listdir','os.scandir'):raise PermissionError('NO_DIRECTORY_LISTING')
 if e.startswith(('subprocess.','socket.')) or e in ('os.system','os.remove','os.rename','os.rmdir','os.link','os.symlink'):raise PermissionError('NO_LAUNCH_NETWORK_MUTATION')
sys.addaudithook(audit)
for name in ('stat','lstat','readlink'):
 old=getattr(os,name)
 def wrap(p,*a,_old=old,**kw):permit(p,'metadata');return _old(p,*a,**kw)
 setattr(os,name,wrap)
def canonical_safe(p):
 # Resolve only this explicitly admitted file. Inspect a symlink's target string
 # for bans before inspecting any target component. No directory enumeration.
 if p not in SAFE:raise PermissionError('UNREGISTERED_CANONICAL_REQUEST')
 q=list(Path(p).parts[1:]);done=[];links=0
 while q:
  x=q.pop(0)
  if x in ('','.'):continue
  if x=='..':done.pop();continue
  v='/'+('/'.join(done+[x]));ban(v)
  st=original_stat(v)
  if stat.S_ISLNK(st.st_mode):
   target=original_readlink(v);ban(target);links+=1
   if links>40:raise ValueError('SYMLINK_LOOP')
   if target.startswith('/'):done=[]
   q=[z for z in target.split('/') if z]+q
  else:done.append(x)
 resolved='/'+('/'.join(done));ban(resolved);SAFE.add(resolved)
 return resolved
def strict_pairs(v):
 d={}
 for k,x in v:
  if k in d:raise ValueError('DUPLICATE_JSON')
  d[k]=x
 return d
def read(p,want=None):
 permit(p,'open');canon=canonical_safe(p)
 with open(p,'rb') as f:b=f.read()
 h=hashlib.sha256(b).hexdigest()
 if want is not None and h!=want:raise ValueError('PIN_MISMATCH')
 if p in PINS and PINS[p]['sha256']!=h:raise ValueError('MUTATED_INPUT')
 PINS[p]={'path':p,'sha256':h,'canonical_path':canon}
 return b
def jr(p,want=None):return json.loads(read(p,want),object_pairs_hook=strict_pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def nr(p,want,keys=None):
 read(p,want)
 with zipfile.ZipFile(p) as z:
  n=z.namelist();assert len(n)==len(set(n)) and all(x.endswith('.npy') for x in n)
 with np.load(p,allow_pickle=False) as z:d={k:z[k] for k in (keys or z.files)}
 assert all(np.isfinite(v).all() for v in d.values())
 return d
def ck(n,ok,detail=None):TESTS.append({'name':n,'pass':bool(ok),'detail':detail})
def ar(x):return np.asarray(x,dtype=np.float64)
def mx(x):return float(np.max(np.abs(x)))
def close(n,a,b,tol=2e-11):
 a=ar(a);b=ar(b);d=mx(a-b);ck(n,a.shape==b.shape and d<=tol,{'max_abs':d,'tolerance':tol});return d
def vector(x,ids):
 x=ar(x);i=int(np.argmax(np.abs(x)))
 return {'per_row_km_s':x.tolist(),'max_abs_km_s':mx(x),'argmax_row_id':ids[i],'signed_at_argmax_km_s':float(x[i])}
def put(n,x):
 p=RUN+n
 with open(p,'x') as f:json.dump(x,f,sort_keys=True,indent=1,allow_nan=False);f.write('\n')
 with open(p,'rb') as f:h=hashlib.sha256(f.read()).hexdigest()
 return {'path':p,'sha256':h}

record=jr(G+'out/B2_GATE_RECORD_C3V002.json','d4b41ffcab00a05bf0bead8c943b8f3555fdeb91beda2cba430efa65431315d7')
adv={}
for suffix in ('C2','C3C4'):
 adv.update(jr(A+'uv_tail_study_c2/check/ADV_TAIL_CHECK_'+suffix+'_KB12_W025_O6_V001.json')['cases'])
read(G+'scripts/b2_independent_c3v001.py','6c013801d8b86255c9ca042deb9de2a95adaa37a11fad06ea23abe104c6089d5')
read(A+'uv_tail_study_c2/check/adv_tail_check_v001.py')
read('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0618_2026-10-18_claude3_codex2_B2_sanity_decomposition_A97.md','78ba2e9a645cbdf3d31e2dc4dcc35b552e2af323500383bd81b3a0b8d9ab9d01')
results={}
for st in ('C2R3','C3R3','C4R3'):
 rr=record['per_state'][st];j=jr(G+'out/path2/IND_'+st+'_BASE.json',rr['inputs']['path2_base']['sha256'])
 comp=nr(G+'out/path2/IND_'+st+'_BASE.npz',j['npz_sha256'])
 pred=jr(G+'out/path1/'+st+'_CM_ON/observation/result.json',rr['production_path']['column_mean_result_sha256'])['prediction']
 ref=j['inputs']['le3_rotation'];expected='/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_'+st+'_D7R3_RUN_V001/stages/19_le3_rotation/rotation/rotation_base_arrays.npz'
 assert ref['path']==expected
 SAFE.add(expected)
 rot=nr(expected,ref['sha256'],['radial_nodes_m','rho0','enthalpy','rotation_Omega_squared','full_fields_complex','full_gradient_complex','Phi_R_full'])
 R=rot['radial_nodes_m'];h=rot['enthalpy'][:,0,:];om0=rot['rotation_Omega_squared'];ids=j['row_ids']
 weights=ar([c['emissivity_path_weights'] for c in pred['columns']]);assert weights.shape==h.shape
 wrh=weights/h;norm=np.sum(wrh,axis=1)
 inclination=math.sin(pred['physical_inclination_rad'])/math.sin(pred['released_inclination_rad'])
 def readout(om):
  assert np.all(om>0)
  col=np.sum(weights*(R[:,None]*np.sqrt(om)),axis=1)/np.sum(weights,axis=1)
  return ar([sum(col[i]*w for i,w in zip(q['column_indices'],q['interpolation_weights']))*inclination/1000 for q in pred['query_support']])
 def rows_for_force(dpr):return readout(om0+(np.sum(wrh*dpr,axis=1)/norm/R)[:,None])
 close(st+':zero_force_baseline',readout(om0),j['rows_saved_le3_km_s'],1e-12)
 c=j['c_m_s'];ph=2*math.pi*np.arange(16)/16
 f0=rot['full_fields_complex'][...,0].real;grad=rot['full_gradient_complex'][...,0,:].real
 gR=grad[...,0]*np.cos(ph)[None,:,None]+grad[...,1]*np.sin(ph)[None,:,None]
 fcheck=c*c*gR/(1+f0)
 close(st+':kept_radial_field',fcheck,rot['Phi_R_full'],1e-25)
 tR=comp['tR_stars_cont']+comp['tR_gas_cont'];tt=comp['t_total']
 exact=np.mean(c*c*(gR+tR[:,None,:])/(1+f0+tt[:,None,:])-fcheck,axis=1)
 close(st+':nonlinear_force_recomputed',exact,comp['dpr_B2'],1e-25)
 forces={'discrete_total':c*c*(comp['tR_stars_disc']+comp['tR_gas_disc']),
  'mixed_gas_cont_stars_disc':c*c*(comp['tR_stars_disc']+comp['tR_gas_cont']),
  'mixed_gas_disc_stars_cont':c*c*(comp['tR_stars_cont']+comp['tR_gas_disc']),
  'B2_continuum_v001_linear':c*c*tR,'B2_continuum_v001':exact}
 v={k:rows_for_force(x) for k,x in forces.items()}
 for k,x in v.items():close(st+':saved_variant:'+k,x,j['rows'][k]['rows_km_s'])
 v['production']=ar(rr['rows_production_km_s']);v['ADV_P16']=ar(adv['C'+st[1]]['box_discrete']['rows_P16'])
 same_baseline=ar(adv['C'+st[1]]['rows_saved']).tobytes()==ar(j['rows_saved_le3_km_s']).tobytes()
 seq=['ADV_P16','discrete_total','mixed_gas_cont_stars_disc','B2_continuum_v001_linear','B2_continuum_v001','production']
 names=['reference_representation_residual_or_C3_off_state','gas_rule_discrete_to_continuum_unnamed','star_roster_discrete_to_continuum_named','nonlinear_denominator_readout_unnamed','production_vs_rebuilt_independent']
 steps={n:vector(v[y]-v[x],ids) for n,x,y in zip(names,seq,seq[1:])}
 summed=sum((ar(steps[k]['per_row_km_s']) for k in names),np.zeros(12))
 close(st+':telescoping_closure',summed,v['production']-v['ADV_P16'],2e-14)
 star_last=v['B2_continuum_v001_linear']-v['mixed_gas_cont_stars_disc']
 star_first=v['mixed_gas_disc_stars_cont']-v['discrete_total']
 gas_second=v['B2_continuum_v001_linear']-v['mixed_gas_disc_stars_cont']
 close(st+':order_interaction_closure',(star_last-star_first)+(v['mixed_gas_cont_stars_disc']-v['discrete_total']-gas_second),np.zeros(12),2e-14)
 corrected_reference=v['ADV_P16']+(v['discrete_total']-v['ADV_P16'])+(v['mixed_gas_cont_stars_disc']-v['discrete_total'])+(v['B2_continuum_v001']-v['B2_continuum_v001_linear'])+(v['production']-v['B2_continuum_v001'])
 close(st+':named_only_pathwise_residual',v['production']-corrected_reference,star_last,3e-14)
 results[st]={'same_ADV_baseline':same_baseline,'row_ids':ids,'rebuilt_rows':{k:x.tolist() for k,x in v.items()},'gas_first_chain':steps,
  'raw_sanity':vector(v['production']-v['ADV_P16'],ids),'same_le3_named_star_residual_gas_matched_linear':vector(star_last,ids),
  'same_le3_named_star_residual_star_first_linear':vector(star_first,ids),'nonlinear_source_switch_interaction':vector(star_last-star_first,ids),
  'named_alias_actual_P16_to_P16':vector(np.zeros(12),ids),
  'old_ADV_alias_P16_minus_m0_DIAGNOSTIC_ONLY':vector(v['ADV_P16']-ar(adv['C'+st[1]]['box_discrete']['rows_m0']),ids),
  'pathwise_corrected_reference_rows':corrected_reference.tolist(),
  'C3_reference_status':'same-le3 fresh ADV computation delegated; old ADV remains off-state' if st=='C3R3' else 'same-state archived ADV',
  'interpretation':'Named-only residual is exact pathwise telescoping after gas/readout/implementation matching in the stated order. It is NOT an independently integrated mixed-source nonlinear potential: t_total for discrete stars is absent from these component archives. Both star/gas switch orders are reported.',
  'baseline_source_pin':PINS[expected]}
 # Same force + same readout control; avoid assuming scalar maxima are additive.
 close(st+':force_addition_control',forces['mixed_gas_cont_stars_disc']+forces['mixed_gas_disc_stars_cont'],forces['discrete_total']+forces['B2_continuum_v001_linear'],1e-25)

for p,ref in list(PINS.items()):read(p,ref['sha256'])
ck('protected_attempts_zero',DENIED==[])
out={'schema':'A97_B2_COMPONENT_DECOMPOSITION_CX2V001','date_u':sys.argv[1],
 'tested':'Saved-component NPZ -> independent kept-field nonlinear force -> exact weighted/sqrt/interpolated row readout; row-vector telescope',
 'scientific_reading':'No advocacy or admission; 0.05 km/s allowance unchanged. Fresh C3 ADV and method attribution supplied separately.',
 'per_state':results,'tests':TESTS,'passed':sum(x['pass'] for x in TESTS),'total':len(TESTS),'failures':[x for x in TESTS if not x['pass']],
 'input_pins':list(PINS.values()),'protected_attempts':DENIED,'seconds':time.monotonic()-start,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
 'limitations':['No quadrature reintegration in this suite; tR/t_total arrays are pinned saved inputs.',
 'No source-builder execution. Exact permitted OFF arrays newly accessed under A97; prior review remains unchanged.',
 'C3 old ADV is le4 and is not promoted to a same-le3 reference.',
 'Pathwise component attribution depends on stated order through sqrt; both star-order contrasts are retained.']}
put('ACCESS_LOG_CX2V001.json',sorted(set(ACCESS)));ref=put('RESULTS_CX2V001.json',out)
print(json.dumps({'result':ref,'passed':out['passed'],'total':out['total'],'failures':out['failures'],
 'named_star_maxima':{k:v['same_le3_named_star_residual_gas_matched_linear']['max_abs_km_s'] for k,v in results.items()},
 'seconds':out['seconds'],'peak_rss_bytes':out['peak_rss_bytes']}))
