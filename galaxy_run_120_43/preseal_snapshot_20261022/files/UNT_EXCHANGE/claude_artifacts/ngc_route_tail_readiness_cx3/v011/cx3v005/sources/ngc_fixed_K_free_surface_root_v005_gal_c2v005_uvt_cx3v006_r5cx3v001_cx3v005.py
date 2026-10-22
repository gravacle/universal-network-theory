"""Root-only bounded free-surface columns in the already prepared lagged field.
Explicit controls JSON, no sampling/operator solve, no density clipping or rotation fit.
V005 reads refreshed TOTAL waves once; K=entropy_scale*originalK is a
separate counted preparation, then fixed within that candidate. Sigma unchanged.
A dispersion label refers to original density, not final observed dispersion.
"""
# UVT_C2V001 (Claude2 tail_scheme_impl_c2/route_b): successor of ddo_fixed_K_free_surface_root_v005_gal_c2v005.py (sha256 99fab2857b3f18e1f05c78da81c9d1dc2b4206e65aaadb4ed0fd78b8a639bea1).
# uvt_c2v001 change (TAIL_SCHEME_DESIGN_V002 sec 1.1/1.3/2.2/3.6 with V002_R1; stage kind le_columns): the UV-tail lapse enters only
#   through the reviewed additive boundary slots, via the pinned shared binding uvt_route_b_binding_c2v001.py. Required argv
#   --uv-tail-config/--uv-tail-config-sha256 (certificates are config fields, verified from bytes at build; R1 IA6).
#   enabled=false: the binding returns the reviewed zero literals and adds no record; the reviewed body runs unchanged.
#   enabled=true with an empty domain (O inside C): the same zero literals (no addition anywhere), plus the uv_tail record.
#   slots: evaluate_line L224 (jets) and lapse_difference L229 (R0 lapse pair); bind after the ids check L212 (stars + feedback rings).
# GAL_C2V005 (Claude2 stage_successor_gal_c2v005): successor of ddo_fixed_K_free_surface_root_v005_gal_c2v004.py (sha256 0fdf435a5366275c0885cca9dbb73558e8a3ed58f509db03448ae75ec7bbf2ca).
# c2v005 change (ROOT_DECISIONS_NGC3198 V003 addendum 5bef6552b92b0939... A13 deciding work), the shared admission only:
#   schema V005 pin; PER_CALL admitted on the DDO154 per-call geometry fields (PER_CALL_GEOMETRY and the schema
#   per_call_geometry declaration); a config without such a field is admitted exactly as c2v004. No other change.
# GAL_C2V004 (Claude2 ngc_f10_c2/route_b_v006): successor of ddo_fixed_K_free_surface_root_v005_gal_c2v003.py (sha256 a72664a6e509801af313e6f616af05ea2ad4caa4661bfcead94922862c2ac07b).
# c2v004 changes (ROOT_DECISIONS_NGC3198 V002 addendum 4070146dbd85c3cb...):
#   admission: shared c2v004 admit_config on GALAXY_CONFIG_SCHEMA_V004 (A4 values; A2 member entries, CHECK D2);
#       a config without member is admitted exactly as c2v003
#   no other change
# GAL_C2V003 (Claude2 ngc_route_impl_c2/binding): successor of ddo_fixed_K_free_surface_root_v005_gal_c2v002.py (sha256 cad9231a5fa7d7e2562cc35a40868f7ac401e84c3868db3aeacd4045e98e10f1).
# c2v003 changes (ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001 06cae881fe075b42...):
#   admission: shared c2v003 admit_config on GALAXY_CONFIG_SCHEMA_V003 (N5)
#   no other change
import argparse,hashlib,importlib.util,json,time
from pathlib import Path
import numpy as np
# GALAXY-CONFIG GENERALIZATION gal_c2v002 (Claude2 ngc_route_construction_c2/v004_fix) of reviewed
# ddo_fixed_K_free_surface_root_v005.py (sha256 8a9b2ec1eaba3661b8e5d11cca66b7761efcb0bd0dab4a53987b222b242cda96);
# successor of gal_c2v001 (d6b04f82...). Only DDO literals changed: OFFSET_SHA, 'iteration_0004', 72 and 16 come
# from the galaxy config (schema GALAXY_CONFIG_SCHEMA_V002); with the DDO154 config each equals the old literal.
# O is the reviewed stage's own directory (absolute) so every PINS path is unchanged by relocation.
# c2v002 changes only admission: shared status-whitelist admission admit_config (CHECK_V001 D1), shared strict
# route-A reader route_a_final_iteration (D2/D3), and the config admission now runs inside the try block after
# the output directory exists, so a refusal writes failure.json (D5). Every equation, tolerance, guard, output
# file and output key is unchanged. A config field that is not admitted is refused, never guessed.
O=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method');HR=O.parent/'recovered_packet_audit'
PINS={
'reuse':(HR/'ddo_homotopy_reference_root_worker_v001.py','acda989d375925bf9a8163d8d8a3a22c3f183b6b253c8137312bccc0cefbbe36'),
'column':(O/'owned_fixed_K_free_surface_column_v001.py','54e56f7b53d8ad705875f30b4ddfb029484585fb9343363dab2ab5a2f93bb0d5')}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(p,s):
 if sha(p)!=s:raise ValueError('Pin mismatch '+str(p))
def load(p):
 s=importlib.util.spec_from_file_location(Path(p).stem,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
CONFIG_FORMAT='UNT_ROUTE_B_STAGE_CONFIG_COLUMNS_C2V003'
USED=('galaxy.key','custody.seed_sha256','custody.checkpoint_identity_sha256','custody.offset_finish_sha256','route_a.accepted_iteration','radial.n_columns','mesh.n_phi','brackets.solver_template')
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
def galaxy_config(path,pin):
 # Shared admission, then this stage's type checks; all admission refusals are listed together.
 galaxy,G,_=admit_config(path,pin,CONFIG_FORMAT,USED)
 for n in ('custody.seed_sha256','custody.checkpoint_identity_sha256','custody.offset_finish_sha256'):
  if not _hex64(G[n]):raise GalaxyConfigRefused('Galaxy config '+n+' must be 64 lowercase hexadecimal characters')
 if any(type(G[n]) is not int or G[n]<lo for n,lo in (('route_a.accepted_iteration',0),('radial.n_columns',1),('mesh.n_phi',1))):raise GalaxyConfigRefused('Galaxy config integer field')
 t=G['brackets.solver_template']
 if type(t) is not dict:raise GalaxyConfigRefused('Galaxy config solver template')
 check(t['path'],t['sha256']);return G

# ---- uvt_c2v001 shared UV-tail binding loader (tail_scheme_impl_c2/route_b): identical text in every gal_c2v005_uvt_c2v001 stage ----
UVT_BINDING=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_uvt_route_b_binding_cx3v006_r5cx3v001_cx3v005.py'),'aee7af1286f2d3d9d52117d6b4d4ae82e31d8776af4a4b0a6da7cee96be12fb3')
def uvt_load():
 """The pinned shared UV-tail binding (bytes checked before and after exec; inert at import)."""
 path,pin=UVT_BINDING
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('UV_TAIL_PIN_MISMATCH '+str(path))
 s=importlib.util.spec_from_file_location('uvt_route_b_binding_c2v001',str(path));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('UV_TAIL_PIN_CHANGED_AFTER_IMPORT '+str(path))
 return m
# ---- end of uvt block ----
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ('seed','checkpoint-directory','offset-directory','controls','controls-sha256','feedback-directory','feedback-finish-sha256','outdir'):p.add_argument('--'+n,required=True)
 for n in ('galaxy-config','galaxy-config-sha256'):p.add_argument('--'+n,required=True)
 p.add_argument('--feedback-worker-sha256',required=True)
 p.add_argument('--entropy-scale',type=float,required=True)
 UVT=uvt_load();UVT.add_argv(p,'le_columns');a=p.parse_args()
 if not np.isfinite(a.entropy_scale) or a.entropy_scale<=0:raise ValueError('Finite positive global entropy scale required')
 for value in (a.feedback_worker_sha256,):
  if len(value)!=64 or any(ch not in '0123456789abcdef' for ch in value):raise ValueError('Producer SHA must be64 lowercase hexadecimal characters')
 out=Path(a.outdir);out.mkdir(exist_ok=False);clock=time.monotonic()
 for path,pin in PINS.values():check(path,pin)
 reuse=load(PINS['reuse'][0]);column=load(PINS['column'][0]);check(a.seed,reuse.SEED_SHA);check(a.controls,a.controls_sha256)
 seed=json.loads(Path(a.seed).read_text());ni=seed['numerical_inputs'];controls=json.loads(Path(a.controls).read_text())
 def write(name,obj):
  with (out/name).open('x') as f:json.dump(reuse.serial(obj),f,allow_nan=False,separators=(',',':'));f.flush()
 try:
  G=galaxy_config(a.galaxy_config,a.galaxy_config_sha256);OFFSET_SHA,NCOL,NPHI=G['custody.offset_finish_sha256'],G['radial.n_columns'],G['mesh.n_phi']
  if reuse.SEED_SHA!=G['custody.seed_sha256'] or reuse.IDENTITY!=G['custody.checkpoint_identity_sha256']:raise ValueError('Galaxy config custody differs from the reuse module seed/identity')
  mods={}
  for n in ('checkpoint','line','metric'):
   path,pin=reuse.PINS[n];check(path,pin);mods[n]=load(path)
  cm=mods['checkpoint'];cp=Path(a.checkpoint_directory);od=Path(a.offset_directory)
  identity=cm._read(str(cp/'IDENTITY.json'),'identity')
  if identity['identity_sha256']!=reuse.IDENTITY or cm._sha(cm._canonical(identity['identity']))!=reuse.IDENTITY:raise ValueError('Checkpoint identity')
  caller=cm.decode(identity['identity']['caller']['record']);phys=caller['physical_parameters']
  if caller['seed']['sha256']!=reuse.SEED_SHA:raise ValueError('Checkpoint seed mismatch')
  IT=route_a_final_iteration(cm,cp,reuse.IDENTITY,G['route_a.accepted_iteration'])
  start=cm._read(str(cp/('iteration_%04d/START.json'%IT)),'iteration_start');done=cm._read(str(cp/('iteration_%04d/COMPLETED.json'%IT)),'iteration_completed')
  if start['identity_sha256']!=reuse.IDENTITY or done['iteration_start_sha256']!=start['payload_sha256'] or done['converged']is not True:raise ValueError('Accepted current custody')
  check(od/'finish.json',OFFSET_SHA);finish=json.loads((od/'finish.json').read_text())
  data={}
  for n in ('updated_base_arrays.npz','offset_prepared.npz'):
   ref=finish['outputs'][n];check(ref['path'],ref['sha256'])
   with np.load(ref['path'],allow_pickle=False) as f:data[n]={k:f[k].copy() for k in f.files}
  base=data['updated_base_arrays.npz'];off=data['offset_prepared.npz']
  REGISTERED_NCOL=NCOL;NCOL=UVT.ngc_effective_n_columns(REGISTERED_NCOL,ni,caller,(reuse.PROFILE,reuse.PROFILE_SHA),base['radial_nodes_m'])
  base_K_source=finish['outputs']['updated_base_arrays.npz'];base_K_values=base['K0'][:,0,0].copy()
  scaled_K_values=a.entropy_scale*base_K_values
  if not np.isfinite(scaled_K_values).all() or np.any(scaled_K_values<=0):raise ValueError('Nonfinite/underflowed scaled K')
  waves=cm._get(str(cp),start['prepared_wavevectors']);amps=cm._get(str(cp),start['prepared_weighted_responses'])
  if not np.array_equal(waves,off['wavevectors']):raise ValueError('Wave identity')
  fd=Path(a.feedback_directory);check(fd/'finish.json',a.feedback_finish_sha256)
  ff=json.loads((fd/'finish.json').read_text());fs=json.loads((fd/'start.json').read_text())
  if ff['status']!='REFRESHED_LAGGED_PREPARED_FIELD_NOT_EQUILIBRIUM' or fs['worker_sha256']!=a.feedback_worker_sha256 or fs['seed_sha256']!=reuse.SEED_SHA or fs['checkpoint_start']!=start['payload_sha256'] or fs['offset_finish_sha256']!=OFFSET_SHA or ff['source_offset_applied_once']is not True:raise ValueError('Refreshed total field custody')
  totalref=ff['outputs']['refreshed_prepared.npz'];check(totalref['path'],totalref['sha256'])
  currentgasref=ff['outputs']['gas_source_feedback.npz'];check(currentgasref['path'],currentgasref['sha256'])
  with np.load(totalref['path'],allow_pickle=False) as f:prepared={k:f[k].copy() for k in ('wavevectors','weighted_responses')}
  if not np.array_equal(prepared['wavevectors'],waves) or prepared['weighted_responses'].shape!=amps.shape or not np.isfinite(prepared['weighted_responses']).all():raise ValueError('Refreshed total field shape/order/finiteness')
  # This packet already contains G4 and every applied offset. Never add amps/off here.
  field_provenance=dict(kind='refreshed_total',feedback_finish_sha256=a.feedback_finish_sha256,feedback_directory=str(fd.resolve()),prepared_packet=totalref,feedback_worker_sha256=a.feedback_worker_sha256,current_gas_packet=currentgasref,current_gas_array_key='new_gas_fourier_J')
  ids=controls['radial_indices']
  if not ids or len(set(ids))!=len(ids) or any(type(i)is not int or not 0<=i<NCOL for i in ids):raise ValueError('Unique actual radial indices required')
  uvt=UVT.open_binding(a,'le_columns').bind(ni=ni,phys=phys,caller=caller,galaxy=G['galaxy.key'],profile=(reuse.PROFILE,reuse.PROFILE_SHA),identity=reuse.IDENTITY,iteration=IT,start=start,prepared=prepared,cm=cm,cp=cp,offset_finish=finish,feedback_start=fs,feedback_finish=ff,radii=[float(base['radial_nodes_m'][i]) for i in ids])
  opts=controls['solver'];brackets=controls.get('column_enthalpy_brackets',{});results=[];failures=[]
  if not isinstance(brackets,dict) or any(key not in [str(i) for i in ids] for key in brackets):raise ValueError('Column bracket keys must name selected indices')
  write('start.json',dict(worker_sha256=sha(__file__),entropy_scale=a.entropy_scale,base_K_source=base_K_source,base_K_values_SI=base_K_values,scaled_K_values_SI=scaled_K_values,preparation_scope='Global entropy-state sensitivity, not same fixed-K evolution or guaranteed final dispersion; fixed thereafter within candidate',producer_sha_inputs={'feedback-worker-sha256':a.feedback_worker_sha256},code_pins={str(p):s for p,s in PINS.values()},dependency_pins={n:[str(p),s] for n,(p,s) in reuse.PINS.items() if n in mods},controls_sha256=a.controls_sha256,seed_sha256=reuse.SEED_SHA,offset_finish_sha256=OFFSET_SHA,checkpoint_start=start['payload_sha256'],old_base_source=finish['outputs']['source_offset.npz'],field_provenance=field_provenance,scope='Fixed scaled K and original Sigma; refreshed TOTAL field exactly once, no new native solve',**uvt.record()))
  for i in ids:
   R=float(base['radial_nodes_m'][i]);base_K=float(base_K_values[i]);K=float(scaled_K_values[i]);Sigma=float(base['Sigma_kg_m2'][i]);lines=[]
   try:
    if not np.all(base['K0'][i]==base_K):raise ValueError('Column K not constant')
    for phi in np.arange(NPHI)*2*np.pi/NPHI:
     lines.append(mods['line'].prepare_line(prepared=prepared,x_m=R*np.cos(phi),y_m=R*np.sin(phi)))
    def potential(z):
     values=[]
     for j,line in enumerate(lines):
      pkt=mods['line'].evaluate_line(line=line,z_m=z,**uvt.line_jets(line,float(z)))
      for key in ('fields','gradient','hessian'):
       v=pkt[key];bound=ni['reality_atol']+ni['reality_rtol']*np.abs(v.real)
       if not np.isfinite(v).all() or np.any(np.abs(v.imag)>bound):raise ValueError('Full complex reality '+key)
      mods['metric'].evaluate_point(delta_fields=pkt['fields'][0,:,0].real,delta_gradient_physical=pkt['gradient'][0,:,0,:].real,Cbar=phys['Cbar'],mubar=phys['mubar'],R=R,phi=2*np.pi*j/NPHI,z=z)
      q=mods['line'].lapse_difference(line=line,z_m=z,**uvt.line_lapse_pair(line,float(z)),reality_atol=ni['reality_atol'],reality_rtol=ni['reality_rtol'])
      values.append(float(q['log_lapse_ratio_from_midplane'][0]))
     return phys['c_m_s']**2*float(np.mean(values))
    with (out/f'column_{i:04d}_iterations.jsonl').open('x') as log:
     def progress(rec):log.write(json.dumps(rec,allow_nan=False)+'\n');log.flush()
     local_opts=dict(opts)
     if str(i) in brackets:local_opts['enthalpy_bracket']=brackets[str(i)]
     ans=column.solve_column(potential_difference=potential,Sigma=Sigma,K=K,gamma=5/3,progress=progress,**local_opts)
    # New support is a physical source measure, not a difference at old GL8 nodes.
    z=np.asarray(ans['z_m']);w=np.asarray(ans['weights_m']);rho=np.asarray(ans['rho_kg_m3']);phi=np.arange(NPHI)*2*np.pi/NPHI
    positions=np.array([[R*np.cos(t),R*np.sin(t),zz] for t in phi for zz in z])
    mass=np.tile(w*rho*base['radial_RdR_weights_m2'][i]*(2*np.pi/NPHI),NPHI)
    J=np.zeros((len(mass),10,1));J[:,0,0]=-phys['c_m_s']**2*mass
    if not np.isfinite(J).all():raise ValueError('Nonfinite source')
    array=out/f'column_{i:04d}_source.npz';np.savez(array,physical_positions_m=positions,integrated_source_J=J)
    ans.update(radial_index=i,R_m=R,entropy_scale=a.entropy_scale,base_K_SI=base_K,base_K_source=base_K_source,preparation_scope='Scaled entropy candidate fixed throughout, not guaranteed final dispersion',field_provenance=field_provenance,source_packet=dict(path=str(array),sha256=sha(array)),rotation_status='NOT_EVALUATED: radial derivatives on new columns required',source_delta_contract='For an incremental update to this refreshed total, transform these new mass points and subtract the exact current_gas_packet/new_gas_fourier_J in field_provenance, never original body gas. Alternatively recompute from original G4 plus unit*(latestgas-actual G4gas). Do not combine both routes. Unchanged stars cancel; no feedback applied here.')
    write(f'column_{i:04d}.json',ans);results.append(dict(index=i,path=str(out/f'column_{i:04d}.json'),sha256=sha(out/f'column_{i:04d}.json')))
   except Exception as exc:
    fail=dict(index=i,entropy_scale=a.entropy_scale,base_K_SI=base_K,base_K_source=base_K_source,type=type(exc).__name__,message=str(exc));write(f'column_{i:04d}_failure.json',fail);failures.append(fail)
  write('finish.json',dict(status='LAGGED_FREE_SURFACE_COLUMNS_ONLY',entropy_scale=a.entropy_scale,base_K_source=base_K_source,base_K_values_SI=base_K_values,scaled_K_values_SI=scaled_K_values,preparation_scope='Separate entropy preparation, fixed thereafter; no final dispersion assertion',completed=results,failures=failures,selected_radial_indices=ids,field_provenance=field_provenance,elapsed_seconds=time.monotonic()-clock,limits=['No source self-consistency or full stationary Euler acceptance','No positivity clipping or within-candidate K reset','Finite crossing/quadrature resolution not certified','Native mixing unresolved','Nonzero displacement amplitudes remain failed'],**uvt.record(final=True)))
 except Exception as exc:
  write('failure.json',dict(type=type(exc).__name__,message=str(exc)));raise
if __name__=='__main__':main()
