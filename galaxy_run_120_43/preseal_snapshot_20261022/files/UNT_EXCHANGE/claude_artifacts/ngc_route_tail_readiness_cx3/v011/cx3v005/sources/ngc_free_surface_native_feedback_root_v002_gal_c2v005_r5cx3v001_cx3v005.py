"""Root-only exact finite source feedback for the new free-surface gas measure.
Uses cached weighted full10 -K^-1 e_n; no inversion, root search or state change.
New m0 gas azimuth is integrated by exact J0; native response remains anisotropic.
New total = saved G4 + previous body offset + unit*(newgas-old body gas).
The actual stored old-body Fourier source is subtracted, not reconstructed density.
"""
import argparse,hashlib,importlib.util,json,time
from pathlib import Path
import numpy as np
# GAL_C2V005 (Claude2 stage_successor_gal_c2v005): successor of ddo_free_surface_native_feedback_root_v002_gal_c2v004.py (sha256 4bf84ce4e9f8673e87cb0062ac7f38473ec4f312b055c0564891795174a2a09b).
# c2v005 change (ROOT_DECISIONS_NGC3198 V003 addendum 5bef6552b92b0939... A13 deciding work), the shared admission only:
#   schema V005 pin; PER_CALL admitted on the DDO154 per-call geometry fields (PER_CALL_GEOMETRY and the schema
#   per_call_geometry declaration); a config without such a field is admitted exactly as c2v004. No other change.
# GAL_C2V004 (Claude2 ngc_f10_c2/route_b_v006): successor of ddo_free_surface_native_feedback_root_v002_gal_c2v003.py (sha256 0816b3416fdfb7ee599125d2a6393f6e1ed1986d239986ac75cfd8e0d79c6561).
# c2v004 changes (ROOT_DECISIONS_NGC3198 V002 addendum 4070146dbd85c3cb...):
#   admission: shared c2v004 admit_config on GALAXY_CONFIG_SCHEMA_V004 (A4 values; A2 member entries, CHECK D2);
#       a config without member is admitted exactly as c2v003
#   no other change
# GAL_C2V003 (Claude2 ngc_route_impl_c2/binding): successor of ddo_free_surface_native_feedback_root_v002.py (sha256 44376116d64825ce5319e402a47c138e5e69303a6482d3ebc54abee8291ae1fd).
# c2v003 changes (ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001 06cae881fe075b42...):
#   first galaxy-config successor of the reviewed fs native feedback v002. Its DDO154 literals become config values:
#     OFFSET_SHA -> custody.offset_finish_sha256; iteration_0004 -> the strict route-A reader on route_a.accepted_iteration;
#     72/16/32 -> radial.n_columns / mesh.n_phi / column.n_z (also in the two descriptive output strings, which render
#     identically for DDO154); ROTATION_WORKER_SHA (= reviewed fs rotation v001) -> config producer_pins.rotation_worker
#     {path, sha256} (per call; file bytes verified; the driver whitelists the producer).
#   O is the reviewed stage directory spelled absolutely (same resolved paths). Docstring byte-identical.
#   Added: config admission inside the try block and the seed/identity cross-check.
O=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method');H=O.parent/'recovered_packet_audit'
REUSE=H/'ddo_homotopy_reference_root_worker_v001.py'
REUSE_SHA='acda989d375925bf9a8163d8d8a3a22c3f183b6b253c8137312bccc0cefbbe36'
BESSEL=H/'posix_libm_bessel_j0_provider_v001.py'
BESSEL_SHA='c7c9341660beb879da5c6e3362b67256154f2600ec33a7b8d961ed63fc538a1d'
SOURCE=H/'axisymmetric_initial_rest_energy_fourier_v001.py'
SOURCE_SHA='f5670726e75b6854fb8d55c2ffe6423251bb31193e5d13b087e46b8185984756'
# OFFSET_SHA/ROTATION_WORKER_SHA, iteration_0004, 72/16/32 now come from the galaxy config.
CONFIG_FORMAT='UNT_ROUTE_B_STAGE_CONFIG_FS_FEEDBACK_C2V003'
USED=('galaxy.key','custody.seed_sha256','custody.checkpoint_identity_sha256','custody.offset_finish_sha256','route_a.accepted_iteration','radial.n_columns','mesh.n_phi','column.n_z')
PRODUCER_PINS=('rotation_worker',)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(p,s):
 if sha(p)!=s:raise ValueError('Pin mismatch: '+str(p))
def load(p):
 s=importlib.util.spec_from_file_location(Path(p).stem,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
# ---- c2v005 shared stage-config admission (schema V005, members, DDO154 per-call geometry; ROOT_DECISIONS V003 A13): identical text in every gal_c2v005 stage ----
SCHEMA=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/schema/GALAXY_CONFIG_SCHEMA_V005.json'),'f9b8d48eca10e5c8f2299c23dc1ac69c60c9f87bc24486024e675f7927bc042a')
SCHEMA_NAME='UNT_ROUTE_B_GALAXY_CONFIG_SCHEMA_V005'
ADMITTED_STATUS=('DDO154_EXACT_LITERAL','PER_CALL','SUPPLIED_REVIEWED_CODE','SUPPLIED_REVIEWED_DATA','SUPPLIED_REVIEWED_CODE_AND_DATA','SUPPLIED_TARGET_FREE_MANIFEST','SHARED_SAME_VALUE','SUPPLIED_ROOT_DECISION')
CONDITIONAL_STATUS='DERIVED_FROM_BYTES_CONDITIONAL'
SLOT_STATUS='DECLARED_INPUT_SLOT'
SENTINELS=('NONE_IN_REVIEWED_CODE','NOT_APPLICABLE','PER_CALL')
PER_CALL_KINDS=('PER_CALL_CUSTODY','ROUTE_A_RUN_OUTCOME','STAGE_CODE_IDENTITY')
CALL_INPUT_FIELDS=('source.coefficients',)
PER_CALL_GEOMETRY={'DDO154':('source.profile','source.monotone_source','radial.outer_edge_kpc','observation.binding','observation.query_rows')}
GALAXY_ENTRY={'DDO154':'ddo154','NGC3198':'ngc3198'}
MEMBER_ENTRY={('NGC3198','GL10_ALTERNATIVE'):'ngc3198_gl10_alternative'}
class GalaxyConfigRefused(ValueError):pass
def _hex64(v):return type(v) is str and len(v)==64 and all(c in '0123456789abcdef' for c in v)
def _canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)
def _sentinel(v):
 if type(v) is str:return v if v in SENTINELS or v.startswith('PENDING') else None
 for x in (v.values() if type(v) is dict else v if type(v) is list else ()):
  s=_sentinel(x)
  if s:return s
 return None
def admit_config(path,pin,fmt,used,extra=None):
 """Shared c2v005 admission (schema V005 = the c2v004 rules + DDO154 per-call geometry). The config {format,schema{name,path,sha256},
 galaxy,fields[,extra]} is pinned by sha256, refers to the pinned schema V003 and names a galaxy with a schema entry.
 A USED field is admitted only if present with a whitelisted status, or DERIVED_FROM_BYTES_CONDITIONAL equal to the
 schema entry with a structured condition {field,equals} naming an admitted field that holds exactly that value.
 DDO154 configs: only DDO154_EXACT_LITERAL (== schema ddo154 value) or PER_CALL. PER_CALL only on a per-call kind, a
 call input, or a field whose schema entry for this galaxy is a DECLARED_INPUT_SLOT. Any other admitted status must be
 the schema entry's own status with the schema entry's own value. No value may hold a sentinel at any depth. extra maps
 each further top-level key to a check returning a refusal or None. Every refusal is listed together; nothing is
 guessed. c2v004: an optional top-level 'member' must name a declared alternative member of the galaxy (MEMBER_ENTRY,
 equal to the schema 'members' entry); every field is then checked against that member's entry instead of the galaxy
 entry. Without member every rule is the c2v003 rule. c2v005: PER_CALL is also admitted on a field that is in
 PER_CALL_GEOMETRY[galaxy] and listed by the pinned schema per_call_geometry[galaxy].fields (DDO154: the five
 distance-dependent fields); every other rule is c2v004. Returns (galaxy, {field: value} for used, config)."""
 if not _hex64(pin):raise GalaxyConfigRefused('Galaxy config sha256 must be 64 lowercase hexadecimal characters')
 raw=Path(path).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=pin:raise GalaxyConfigRefused('Pin mismatch: '+str(path))
 sraw=SCHEMA[0].read_bytes()
 if hashlib.sha256(sraw).hexdigest()!=SCHEMA[1]:raise GalaxyConfigRefused('Pin mismatch: '+str(SCHEMA[0]))
 cfg=json.loads(raw);schema=json.loads(sraw);sf={f['field']:f for f in schema['fields']};extra=extra or {}
 if schema.get('schema')!=SCHEMA_NAME or len(sf)!=len(schema['fields']):raise GalaxyConfigRefused('Galaxy config schema identity')
 if type(cfg) is not dict or set(cfg)-{'member'}!={'format','schema','galaxy','fields'}|set(extra) or cfg['format']!=fmt or cfg['schema']!={'name':SCHEMA_NAME,'path':str(SCHEMA[0]),'sha256':SCHEMA[1]} or type(cfg['fields']) is not dict or not set(cfg['fields'])<=set(sf) or type(cfg['galaxy']) is not str or not cfg['galaxy']:raise GalaxyConfigRefused('Galaxy config must be a '+fmt+' instance of '+SCHEMA_NAME+' with keys format/schema/galaxy/fields[/member]'+''.join('/'+k for k in sorted(extra)))
 if cfg['galaxy'] not in GALAXY_ENTRY:raise GalaxyConfigRefused('GALAXY_NOT_IN_SCHEMA: '+repr(cfg['galaxy']))
 if 'member' in cfg and (type(cfg['member']) is not str or (cfg['galaxy'],cfg['member']) not in MEMBER_ENTRY):raise GalaxyConfigRefused('MEMBER_NOT_IN_SCHEMA: '+repr((cfg['galaxy'],cfg['member'])))
 if 'member' in cfg and (schema.get('members') or {}).get(cfg['galaxy'],{}).get(cfg['member'],{}).get('entry')!=MEMBER_ENTRY[(cfg['galaxy'],cfg['member'])]:raise GalaxyConfigRefused('MEMBER_NOT_DECLARED_BY_SCHEMA: '+repr(cfg['member']))
 F=cfg['fields'];galaxy=cfg['galaxy'];ent=MEMBER_ENTRY[(galaxy,cfg['member'])] if 'member' in cfg else GALAXY_ENTRY[galaxy]
 for n,e in F.items():
  if type(e) is not dict or 'value' not in e or type(e.get('status')) is not str or not set(e)<={'value','status','condition'}:raise GalaxyConfigRefused('Galaxy config field entry {value,status[,condition]} required: '+n)
 def refusal(n,seen=()):
  if n not in F:return n+' (MISSING)'
  e=F[n];st=e['status'];se=sf[n][ent]
  if st==CONDITIONAL_STATUS:
   c=e.get('condition')
   if type(c) is not dict or set(c)!={'field','equals'} or c['field'] in seen+(n,):return n+' ('+st+' without a resolvable condition)'
   if galaxy=='DDO154' or se.get('status')!=st or _canon(se.get('condition'))!=_canon(c) or _canon(se.get('value'))!=_canon(e['value']):return n+' ('+st+' differs from the schema '+ent+' entry)'
   r=refusal(c['field'],seen+(n,))
   if r:return n+' (conditional on '+r+')'
   if _canon(F[c['field']]['value'])!=_canon(c['equals']):return n+' (condition %s==%s not met)'%(c['field'],_canon(c['equals']))
  elif st==SLOT_STATUS:return n+' ('+st+' not filled: '+str(e['value'])+')'
  elif st not in ADMITTED_STATUS:return n+' ('+st+')'
  elif st=='DDO154_EXACT_LITERAL':
   if galaxy!='DDO154' or _canon(e['value'])!=_canon(sf[n]['ddo154']['value']):return n+' (status DDO154_EXACT_LITERAL but not the DDO154 literal)'
  elif st=='PER_CALL':
   if sf[n]['kind'] not in PER_CALL_KINDS and n not in CALL_INPUT_FIELDS and se.get('status')!=SLOT_STATUS and not (n in PER_CALL_GEOMETRY.get(galaxy,()) and n in ((schema.get('per_call_geometry') or {}).get(galaxy) or {}).get('fields',())):return n+' (PER_CALL status on a '+sf[n]['kind']+' field)'
  elif galaxy=='DDO154':return n+' (status '+st+' on DDO154: only DDO154_EXACT_LITERAL or PER_CALL)'
  elif st!=se.get('status') or _canon(e['value'])!=_canon(se.get('value')):return n+' (status/value differ from the schema '+ent+' entry)'
  s=_sentinel(e['value'])
  if s:return n+' ('+s+' value)'
  return None
 refused=[r for r in (refusal(n) for n in used) if r]+[k+': '+r for k,r in ((k,f(cfg[k])) for k,f in sorted(extra.items())) if r]
 if refused:raise GalaxyConfigRefused('GALAXY_CONFIG_REFUSED galaxy=%s; nothing guessed: %s'%(galaxy,'; '.join(refused)))
 if 'galaxy.key' in used and F['galaxy.key']['value']!=galaxy:raise GalaxyConfigRefused('Galaxy config galaxy.key differs from config galaxy')
 return galaxy,{n:F[n]['value'] for n in used},cfg
# ---- c2v002 shared strict route-A reader (verbatim; stages2 CHECK D2): identical text in every gal_c2v003 stage that reads route A ----
ROUTE_A_CONVERGED_OUTCOME='CONVERGED_FINITE_FIXED_POINT'
def route_a_final_iteration(cm,cp,identity,declared):
 """Shared c2v002 route-A reader (CHECK_V001 D2/D3): the final iteration as the checkpoint's own
 integrity-checked records report it. Every entry named iteration_* is a directory iteration_NNNN with
 exactly four ASCII digits; they are contiguous from 0; each holds START.json and COMPLETED.json bound to
 this identity, to its own iteration and to each other; converged is a bool, True only at the last
 iteration; every attempts/*.end.json carries this identity and exactly one reports
 CONVERGED_FINITE_FIXED_POINT; the declared config value (an int, not a bool) equals the last iteration."""
 cp=Path(cp);its=[]
 for x in sorted(cp.iterdir(),key=lambda q:q.name):
  if not x.name.startswith('iteration_'):continue
  d=x.name[len('iteration_'):]
  if len(d)!=4 or any(ch not in '0123456789' for ch in d) or not x.is_dir():raise ValueError('ROUTE_A_ITERATION_AMBIGUOUS: unexpected checkpoint entry '+x.name)
  its.append(int(d))
 if not its or its!=list(range(len(its))):raise ValueError('ROUTE_A_ITERATION_AMBIGUOUS: iterations %s are not contiguous from 0'%(its,))
 converged=[]
 for i in its:
  folder=cp/('iteration_%04d'%i)
  if not (folder/'START.json').is_file() or not (folder/'COMPLETED.json').is_file():raise ValueError('ROUTE_A_ITERATION_AMBIGUOUS: iteration %d lacks START or COMPLETED'%i)
  s=cm._read(str(folder/'START.json'),'iteration_start');c=cm._read(str(folder/'COMPLETED.json'),'iteration_completed')
  if s['iteration']!=i or c['iteration']!=i or s['identity_sha256']!=identity or c['identity_sha256']!=identity or c['iteration_start_sha256']!=s['payload_sha256'] or type(c['converged']) is not bool:raise ValueError('ROUTE_A_ITERATION_AMBIGUOUS: records of iteration %d not bound to this identity/iteration'%i)
  if c['converged']:converged.append(i)
 if converged!=[its[-1]]:raise ValueError('ROUTE_A_ITERATION_AMBIGUOUS: converged %s of present %s; exactly the last must be converged'%(converged,its))
 ad=cp/'attempts';ends=[]
 if not ad.is_dir():raise ValueError('ROUTE_A_ITERATION_AMBIGUOUS: no attempts directory')
 for x in sorted(ad.glob('*.end.json'),key=lambda q:q.name):
  rec=cm._read(str(x),'attempt_end')
  if rec['identity_sha256']!=identity:raise ValueError('ROUTE_A_ITERATION_AMBIGUOUS: attempt_end of another identity '+x.name)
  if rec['outcome']==ROUTE_A_CONVERGED_OUTCOME:ends.append(x.name)
 if len(ends)!=1:raise ValueError('ROUTE_A_ITERATION_AMBIGUOUS: %d attempt_end records report %s (exactly one required)'%(len(ends),ROUTE_A_CONVERGED_OUTCOME))
 if type(declared) is not int or declared!=its[-1]:raise ValueError('ROUTE_A_ITERATION_CONFIG_MISMATCH: config route_a.accepted_iteration=%r, route A reports %d'%(declared,its[-1]))
 return its[-1]
# ---- end of shared blocks ----
def _producer_refusal(pp):
 """producer_pins = {name: {path, sha256}} for PRODUCER_PINS: the script that produced the upstream run (per call)."""
 if type(pp) is not dict or set(pp)!=set(PRODUCER_PINS):return 'must be exactly {%s: {path, sha256}}'%', '.join(PRODUCER_PINS)
 for k in PRODUCER_PINS:
  rw=pp[k]
  if _sentinel(rw):return k+' '+_sentinel(rw)
  if type(rw) is not dict or set(rw)!={'path','sha256'} or type(rw['path']) is not str or not _hex64(rw['sha256']):return k+' must be {path, sha256}'
  p=Path(rw['path'])
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=rw['sha256']:return k+' file bytes differ from its sha256: '+str(p)
 return None
def galaxy_config(path,pin):
 """Shared c2v003 admission of USED + producer_pins, then this stage's typed checks. Returns (G, rotation producer)."""
 galaxy,G,cfg=admit_config(path,pin,CONFIG_FORMAT,USED,{'producer_pins':_producer_refusal});bad=[]
 for n in ('custody.seed_sha256','custody.checkpoint_identity_sha256','custody.offset_finish_sha256'):
  if not _hex64(G[n]):bad.append(n+' must be sha256')
 if type(G['route_a.accepted_iteration']) is not int or G['route_a.accepted_iteration']<0:bad.append('route_a.accepted_iteration must be int')
 for n in ('radial.n_columns','mesh.n_phi','column.n_z'):
  if type(G[n]) is not int or G[n]<1:bad.append(n+' must be a positive int')
 if bad:raise GalaxyConfigRefused('GALAXY_CONFIG_INVALID galaxy=%s: %s'%(galaxy,'; '.join(bad)))
 return G,cfg['producer_pins'][PRODUCER_PINS[0]]

def finite(x,name):
 if not np.isfinite(x).all():raise ValueError('Nonfinite '+name)
 return x

UVT_BINDING=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_uvt_route_b_binding_cx3v006_r5cx3v001_cx3v005.py'),'aee7af1286f2d3d9d52117d6b4d4ae82e31d8776af4a4b0a6da7cee96be12fb3')
def uvt_load():
 """The pinned shared UV-tail binding (bytes checked before and after exec; inert at import)."""
 path,pin=UVT_BINDING
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('UV_TAIL_PIN_MISMATCH '+str(path))
 s=importlib.util.spec_from_file_location('uvt_route_b_binding_c2v001',str(path));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('UV_TAIL_PIN_CHANGED_AFTER_IMPORT '+str(path))
 return m

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ('seed','checkpoint-directory','offset-directory','rotation-directory','rotation-finish-sha256','outdir'):p.add_argument('--'+n,required=True)
 for n in ('wave-batch','position-batch'):p.add_argument('--'+n,type=int,required=True)
 p.add_argument('--bessel-cache-entries',type=int,required=True)
 p.add_argument('--galaxy-config',required=True)
 p.add_argument('--galaxy-config-sha256',required=True)
 a=p.parse_args();out=Path(a.outdir);out.mkdir(exist_ok=False);clock=time.monotonic();stage='admission'
 check(REUSE,REUSE_SHA);reuse=load(REUSE)
 def write(name,obj):
  with (out/name).open('x') as f:json.dump(reuse.serial(obj),f,allow_nan=False,separators=(',',':'));f.flush()
 try:
  G,ROTW=galaxy_config(a.galaxy_config,a.galaxy_config_sha256)
  if G['custody.seed_sha256']!=reuse.SEED_SHA or G['custody.checkpoint_identity_sha256']!=reuse.IDENTITY:raise ValueError('GALAXY_CONFIG_CUSTODY: config seed/checkpoint identity differ from the bound reuse module')
  OFFSET_SHA=G['custody.offset_finish_sha256'];ROTATION_WORKER_SHA=ROTW['sha256'];NCOL=G['radial.n_columns'];NPHI=G['mesh.n_phi'];NZ=G['column.n_z']
  if not 1<=a.wave_batch<=1024 or not 1<=a.position_batch<=1024:raise ValueError('Explicit batch sizes1..1024 required')
  check(BESSEL,BESSEL_SHA);check(SOURCE,SOURCE_SHA);source_module=load(SOURCE);bessel,provider_metadata=load(BESSEL).create_provider(max_cache_entries=a.bessel_cache_entries)
  check(a.seed,reuse.SEED_SHA);seed=json.loads(Path(a.seed).read_text());ni=seed['numerical_inputs']
  path,pin=reuse.PINS['checkpoint'];check(path,pin);cm=load(path);cp=Path(a.checkpoint_directory)
  identity=cm._read(str(cp/'IDENTITY.json'),'identity')
  if identity['identity_sha256']!=reuse.IDENTITY or cm._sha(cm._canonical(identity['identity']))!=reuse.IDENTITY:raise ValueError('Current checkpoint identity')
  caller=cm.decode(identity['identity']['caller']['record']);phys=caller['physical_parameters']
  if caller['seed']['sha256']!=reuse.SEED_SHA:raise ValueError('Current seed identity')
  ITER=route_a_final_iteration(cm,cp,reuse.IDENTITY,G['route_a.accepted_iteration'])
  start=cm._read(str(cp/('iteration_%04d/START.json'%ITER)),'iteration_start');done=cm._read(str(cp/('iteration_%04d/COMPLETED.json'%ITER)),'iteration_completed')
  if start['identity_sha256']!=reuse.IDENTITY or done['identity_sha256']!=reuse.IDENTITY or done['iteration_start_sha256']!=start['payload_sha256'] or done['converged']is not True:raise ValueError('Accepted current custody')
  od=Path(a.offset_directory);rd=Path(a.rotation_directory)
  check(od/'finish.json',OFFSET_SHA);of=json.loads((od/'finish.json').read_text());os=json.loads((od/'start.json').read_text())
  if of['status']!='AFFINE_BASE_OFFSET_EVALUATED_NOT_FLOW_SOLUTION' or os['seed_sha256']!=reuse.SEED_SHA or os['old_gas']!=start['gas_fourier_J'] or os['fixed_stars']!=start['fixed_source_fourier_J']:raise ValueError('Actual old-body source/field custody')
  check(rd/'finish.json',a.rotation_finish_sha256);rf=json.loads((rd/'finish.json').read_text());rs=json.loads((rd/'start.json').read_text())
  if rf['status']!='LAGGED_M0_ROTATION_EVALUATED_NOT_FULL_FLOW' or rs['worker_sha256']!=ROTATION_WORKER_SHA or rs['seed_sha256']!=reuse.SEED_SHA or rs['offset_finish_sha256']!=OFFSET_SHA or rs['checkpoint_start']!=start['payload_sha256']:raise ValueError('Complete new-source provenance')
  check(rf['arrays_path'],rf['arrays_sha256'])
  with np.load(rf['arrays_path'],allow_pickle=False) as f:
   positions=finite(f['physical_positions_m'].copy(),'new positions').reshape(-1,3)
   J=finite(f['integrated_source_J'].copy(),'new integrated source').reshape(-1,10,1)
   density=finite(f['rho0'].copy(),'new density');volume=finite(f['volume_weights_m3'].copy(),'new volume')
   sigma=finite(f['Sigma_kg_m2'].copy(),'new Sigma');wr=finite(f['radial_RdR_weights_m2'].copy(),'new annular weights')
   radius=finite(f['radial_nodes_m'].copy(),'new radii');heights=finite(f['z'].copy(),'new heights')
  UVT=uvt_load();REGISTERED_NCOL=NCOL;NCOL=UVT.ngc_effective_n_columns(REGISTERED_NCOL,ni,caller,(reuse.PROFILE,reuse.PROFILE_SHA),radius)
  if density.shape!=(NCOL,NPHI,NZ) or volume.shape!=density.shape or sigma.shape!=(NCOL,) or wr.shape!=(NCOL,) or len(positions)!=NCOL*NPHI*NZ or np.any(density<=0) or np.any(volume<=0) or np.any(J[:,1:,:]!=0):raise ValueError('Actual complete%dx%dx%d positive scalar gas measure required'%(NCOL,NPHI,NZ))
  if radius.shape!=(NCOL,) or heights.shape!=density.shape or not np.array_equal(density,np.broadcast_to(density[:,0:1,:],density.shape)) or not np.array_equal(volume,np.broadcast_to(volume[:,0:1,:],volume.shape)) or not np.array_equal(heights,np.broadcast_to(heights[:,0:1,:],heights.shape)):raise ValueError('Exact axisymmetric m0 measure required; anisotropic gas must retain full transform')
  ring_radius=np.repeat(radius,NZ);ring_z=heights[:,0,:].reshape(-1);ring_mass=np.sum(volume*density,axis=1).reshape(-1)
  expected=-phys['c_m_s']**2*density.reshape(-1)*volume.reshape(-1)
  if not np.array_equal(J[:,0,0],expected):raise ValueError('Source units/volume differ from actual solved gas')
  # Preserve source measure rather than rescaling it to the independent annular mass.
  column_mass=np.sum(volume*density,axis=(1,2));expected_mass=2*np.pi*wr*sigma
  mass_residual=finite((column_mass-expected_mass)/expected_mass,'column mass residual')
  refs=of['outputs']
  for name in ('unit_response.npz','source_offset.npz','offset_prepared.npz'):check(refs[name]['path'],refs[name]['sha256'])
  with np.load(refs['unit_response.npz']['path'],allow_pickle=False) as f:
   waves=finite(f['wavevectors'].copy(),'unit waves');unit=finite(f['weighted_responses'].copy(),'unit response');dk=finite(f['dk_weights'].copy(),'wave weights')
  with np.load(refs['source_offset.npz']['path'],allow_pickle=False) as f:oldgas=finite(f['new_body_fourier_J'].copy(),'actual old body gas')
  with np.load(refs['offset_prepared.npz']['path'],allow_pickle=False) as f:
   oldoffset=finite(f['weighted_responses'].copy(),'actual old offset')
   if not np.array_equal(f['wavevectors'],waves):raise ValueError('Old offset wave order')
  original_waves=cm._get(str(cp),start['prepared_wavevectors']);original=cm._get(str(cp),start['prepared_weighted_responses'])
  if not np.array_equal(waves,original_waves) or waves.shape!=(len(waves),3) or unit.shape!=(len(waves),10,1) or oldgas.shape!=unit.shape or oldoffset.shape!=unit.shape or original.shape!=unit.shape or np.any(oldgas[:,1:,:]!=0) or dk.shape!=(len(waves),) or np.any(dk<=0):raise ValueError('Full signed packet shape/order/source mismatch')
  write('start.json',dict(ngc_radial_count_custody=dict(registered_n_columns=REGISTERED_NCOL,effective_n_columns=NCOL),worker_sha256=sha(__file__),reuse_sha256=REUSE_SHA,checkpoint_module_pin=[str(path),pin],seed_sha256=reuse.SEED_SHA,checkpoint_start=start['payload_sha256'],offset_finish_sha256=OFFSET_SHA,rotation_finish_sha256=a.rotation_finish_sha256,new_source_arrays_sha256=rf['arrays_sha256'],unit_packet=refs['unit_response.npz'],old_body_source_packet=refs['source_offset.npz'],old_offset_packet=refs['offset_prepared.npz'],fixed_stars=start['fixed_source_fourier_J'],new_rotation_positive=rf['positive_rotation_square'],wave_batch=a.wave_batch,position_batch=a.position_batch,source_measure_relative_mass_residual=mass_residual,bessel_module_pin=[str(BESSEL),BESSEL_SHA],source_module_pin=[str(SOURCE),SOURCE_SHA],bessel_provider=provider_metadata,azimuth_rule='Exact J0 contraction of actual axisymmetric new gas, replaces%dangle quadrature only; old stored source unchanged; native anisotropic response retained'%NPHI,scope='Diagnostic actual measure accepted independently of rotation sign; no physical flow acceptance'))
  stage='new_source_forward';newgas=np.zeros_like(oldgas)
  with (out/'progress.jsonl').open('x') as log:
   for i in range(0,len(waves),a.wave_batch):
    kk=waves[i:i+a.wave_batch]
    block=source_module.source_fourier(radius_m=ring_radius,z_m=ring_z,ring_mass_kg=ring_mass,k_physical_inverse_m=kk,c_m_s=phys['c_m_s'],bessel_j0=bessel,wave_chunk=len(kk),ring_chunk=a.position_batch)
    newgas[i:i+len(kk)]=finite(block,'analytic azimuth source')
    log.write(json.dumps(dict(stage=stage,nodes_completed=i+len(kk),bessel_evaluations=provider_metadata['evaluations'],bessel_cache_hits=provider_metadata['cache_hits'],elapsed_seconds=time.monotonic()-clock))+'\n');log.flush()
  stage='apply_cached_response';delta=finite(newgas-oldgas,'actual source difference')
  delta_response=finite(unit*delta[:,0:1,:],'full10 feedback')
  oldtotal=finite(original+oldoffset,'old base total field')
  refreshed=finite(oldtotal+delta_response,'refreshed prepared response')
  np.savez(out/'gas_source_feedback.npz',new_gas_fourier_J=newgas,old_body_gas_fourier_J=oldgas,delta_gas_fourier_J=delta)
  np.savez(out/'feedback_prepared.npz',wavevectors=waves,weighted_responses=delta_response)
  np.savez(out/'refreshed_prepared.npz',wavevectors=waves,weighted_responses=refreshed)
  write('finish.json',dict(ngc_radial_count_custody=dict(registered_n_columns=REGISTERED_NCOL,effective_n_columns=NCOL),status='REFRESHED_LAGGED_PREPARED_FIELD_NOT_EQUILIBRIUM',outputs={name:dict(path=str(out/name),sha256=sha(out/name)) for name in ('gas_source_feedback.npz','feedback_prepared.npz','refreshed_prepared.npz')},elapsed_seconds=time.monotonic()-clock,source_offset_applied_once=True,operator_inversions=0,bessel_provider=provider_metadata,new_source_azimuth='analytic J0, actual%dz quadrature and full ring mass; oldbody subtraction remains exact stored%dangle Fourier measure'%(NZ,NPHI),new_rotation_positive=rf['positive_rotation_square'],fixed_stars_unchanged=True,
    composition='G4 + saved oldbody-G4 response + cached unit*(newgas-actual oldbodygas); all10 fields; no new dk/(2pi)^3 factor',
    next_column_contract='Use ONLY refreshed_prepared as total perturbation field with original zero boundary; do not add G4 or any source offset again. Reevaluate roots/mass at fixed K/Sigma. Existing free-surface V001 hardcodes the old packet and must be bound by an immutable successor before reuse.',
    limits=['No physical acceptance from source feedback alone','No real-space field/metric admissibility checked at new query points here','Original failed native mixing and finite Fourier/source quadrature limits retained','No coefficient/calibration state changed']))
 except Exception as exc:
  write('failure.json',dict(stage=stage,type=type(exc).__name__,message=str(exc),elapsed_seconds=time.monotonic()-clock));raise
if __name__=='__main__':main()
