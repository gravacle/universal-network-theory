"""Root-only complete72 fixed-K column rotation in the SAME saved lagged field.
Manifest: {runs:[{directory,finish_sha256},...]}; all72 unique successful columns.
No root search, field inversion, density reset, target velocity or nonzero solve.
V005 requires all columns in the SAME refreshed TOTAL field and the SAME
explicit global entropy preparation scale. Sigma/native operator unchanged.
"""
# UVT_C2V001 (Claude2 tail_scheme_impl_c2/route_b): successor of ddo_free_surface_rotation_root_v005_gal_c2v005.py (sha256 be1c913f4cfe3f6ccafd5d48bd2fb68856fa080ad8da016091ec237c652bef25).
# uvt_c2v001 change (TAIL_SCHEME_DESIGN_V002 sec 1.1/1.3/2.2/3.6 with V002_R1; stage kind le_rotation): the UV-tail lapse enters only
#   through the reviewed additive boundary slots, via the pinned shared binding uvt_route_b_binding_c2v001.py. Required argv
#   --uv-tail-config/--uv-tail-config-sha256 (certificates are config fields, verified from bytes at build; R1 IA6).
#   enabled=false: the binding returns the reviewed zero literals and adds no record; the reviewed body runs unchanged.
#   enabled=true with an empty domain (O inside C): the same zero literals (no addition anywhere), plus the uv_tail record.
#   slots: evaluate_line L261 (jets); bind after the refreshed-field check L252 (stars + feedback rings).
# GAL_C2V005 (Claude2 stage_successor_gal_c2v005): successor of ddo_free_surface_rotation_root_v005_gal_c2v004.py (sha256 9b2ded4fda7135e047a40586fdaae4a7c52a6998648aa330064c6a8e5ceffb48).
# c2v005 change (ROOT_DECISIONS_NGC3198 V003 addendum 5bef6552b92b0939... A13 deciding work), the shared admission only:
#   schema V005 pin; PER_CALL admitted on the DDO154 per-call geometry fields (PER_CALL_GEOMETRY and the schema
#   per_call_geometry declaration); a config without such a field is admitted exactly as c2v004. No other change.
# GAL_C2V004 (Claude2 ngc_f10_c2/route_b_v006): successor of ddo_free_surface_rotation_root_v005_gal_c2v003.py (sha256 2eec8f5cf55464dc8eb130f76e8cc65dfc94157ab7865ec3e97d39c170dad896).
# c2v004 changes (ROOT_DECISIONS_NGC3198 V002 addendum 4070146dbd85c3cb...):
#   admission: shared c2v004 admit_config on GALAXY_CONFIG_SCHEMA_V004 (A4 values; A2 member entries, CHECK D2);
#       a config without member is admitted exactly as c2v003
#   no other change
# GAL_C2V003 (Claude2 ngc_route_impl_c2/binding): successor of ddo_free_surface_rotation_root_v005_gal_c2v002.py (sha256 6ccc5c4708f65bbf4ee8245776c28dd196ab0d281b5c09d51091a093e2f6540b).
# c2v003 changes (ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001 06cae881fe075b42...):
#   admission: shared c2v003 admit_config on GALAXY_CONFIG_SCHEMA_V003 (N5)
#   join: the stages2 join successor (n_columns keyword) replaces join v001; the JOIN_SHAPE (72,16) refusal is removed
#       (the join successor itself requires exactly n_columns columns and n_phi angles); join receives n_columns=NCOL
#   N2: Rout = sqrt(source s_edges[J])*kpc with J = radial_truncation(source edges, radial.outer_edge_kpc), replacing
#       sqrt(edges[-1]) and the guard sqrt(edges[-1]) == outer edge; DDO154 J = last edge (old values bitwise)
import argparse,json,time
from pathlib import Path
import numpy as np
import importlib.util,hashlib
# gal_c2v002 (Claude2 ngc_route_construction_c2/v004_fix): ddo_free_surface_rotation_root_v005 (1b429905...) with its
# DDO154 literals (monotone source pin, offset finish sha, route-A iteration_0004, 72 columns, 16 angles) read from a
# --galaxy-config instance of GALAXY_CONFIG_SCHEMA_V002; successor of gal_c2v001 (98a7c6aa...). With the DDO154 config
# every equation, tolerance, guard and output is that of v005. Added only: config admission (fail closed) and the
# route-A final-iteration check. c2v002 changes only admission: shared status-whitelist admission admit_config
# (CHECK_V001 D1; field statuses are now read), shared strict route-A reader route_a_final_iteration (D2/D3), the
# admission runs inside the try block after the output directory exists so a refusal writes failure.json (D5), and
# the docstring above is the reviewed v005 docstring byte for byte (D6).
# v005 located its pins relative to its own folder; this successor lives elsewhere, so
# the same folder is named absolutely (identical resolved paths, same pinned bytes).
O=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method');H=O.parent/'recovered_packet_audit'
PINS={
'reuse':(H/'ddo_homotopy_reference_root_worker_v001.py','acda989d375925bf9a8163d8d8a3a22c3f183b6b253c8137312bccc0cefbbe36'),
'join':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_construction_c2/stages2/modules/owned_free_surface_column_packet_join_v001_gal_c2v001.py'),'0a7f53147365db21618a116c300f0bb87850024eb3cf15e1ac8bbd89786d2c25'),
'rotation':(O/'owned_free_surface_rotation_v001.py','e1b354ecd210543fcba46e8cc3339c111c28c794d9870852052f908398f5ab50'),
'mesh':(O/'owned_body_fitted_displacement_binding_v002.py','87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462')}
# SOURCE/SOURCE_SHA/OFFSET_SHA, iteration_0004, 72 and 16 now come from the galaxy config.
CONFIG_FORMAT='UNT_ROUTE_B_STAGE_CONFIG_ROTATION_C2V003'
USED=('galaxy.key','source.monotone_source','custody.seed_sha256','custody.checkpoint_identity_sha256','custody.offset_finish_sha256','route_a.accepted_iteration','radial.n_columns','radial.outer_edge_kpc','mesh.n_phi')
# c2v003: the join successor (stages2 gal_c2v001, n_columns keyword) takes radial.n_columns / mesh.n_phi.
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(p,s):
 if sha(p)!=s:raise ValueError('Pin mismatch '+str(p))
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
# ---- c2v003 shared N2 radial truncation: identical text in reference/body/offset/rotation gal_c2v003 ----
def radial_truncation(edges_kpc2,outer_kpc):
 """ROOT_DECISIONS_NGC3198 N2: index J of the annulus edge where the route-B radial domain ends. radial.outer_edge_kpc
 must equal sqrt(s_edges_kpc2[J]) exactly (IEEE sqrt) for exactly one J>=1. Route B uses annuli 0..J-1 and the domain
 edge sqrt(s_edges_kpc2[J]). J=len(s_edges_kpc2)-1 is the untruncated domain (DDO154: every expression is the old one)."""
 hits=[j for j in range(1,len(edges_kpc2)) if float(np.sqrt(float(edges_kpc2[j])))==outer_kpc]
 if type(outer_kpc) is not float or len(hits)!=1:raise ValueError('RADIAL_TRUNCATION_REFUSED: radial.outer_edge_kpc=%r is not exactly one annulus edge of the source record'%(outer_kpc,))
 return hits[0]
# ---- end of shared blocks ----
def galaxy_config(path,digest):
 """Shared admission of the fields this stage uses, then this stage's shape/type checks (fail closed)."""
 galaxy,f,_=admit_config(path,digest,CONFIG_FORMAT,USED);bad=[]
 src=f['source.monotone_source']
 if type(src) is not dict or set(src)!={'path','sha256'} or type(src['path']) is not str or not _hex64(src['sha256']):bad.append('source.monotone_source must be {path,sha256}')
 for n in ('custody.seed_sha256','custody.checkpoint_identity_sha256','custody.offset_finish_sha256'):
  if not _hex64(f[n]):bad.append(n+' must be sha256')
 for n in ('route_a.accepted_iteration','radial.n_columns','mesh.n_phi'):
  if type(f[n]) is not int or f[n]<0 or f[n]>9999:bad.append(n+' must be int')
 if type(f['radial.outer_edge_kpc']) is not float or not np.isfinite(f['radial.outer_edge_kpc']) or f['radial.outer_edge_kpc']<=0:bad.append('radial.outer_edge_kpc must be finite positive float')
 if bad:raise GalaxyConfigRefused('GALAXY_CONFIG_REFUSED galaxy=%s (fail closed): '%galaxy+'; '.join(bad))
 return f

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
 for n in ('seed','checkpoint-directory','offset-directory','column-manifest','column-manifest-sha256','feedback-directory','feedback-finish-sha256','outdir'):p.add_argument('--'+n,required=True)
 p.add_argument('--mass-relative-tolerance',required=True,type=float)
 p.add_argument('--entropy-scale',type=float,required=True)
 p.add_argument('--column-worker-sha256',required=True)
 p.add_argument('--feedback-worker-sha256',required=True)
 p.add_argument('--galaxy-config',required=True)
 p.add_argument('--galaxy-config-sha256',required=True)
 UVT=uvt_load();UVT.add_argv(p,'le_rotation');a=p.parse_args()
 if not np.isfinite(a.entropy_scale) or a.entropy_scale<=0:raise ValueError('Finite positive global entropy scale required')
 for value in (a.column_worker_sha256,a.feedback_worker_sha256):
  if len(value)!=64 or any(ch not in '0123456789abcdef' for ch in value):raise ValueError('Producer SHA must be64 lowercase hexadecimal characters')
 out=Path(a.outdir);out.mkdir(exist_ok=False);clock=time.monotonic()
 for path,pin in PINS.values():check(path,pin)
 mods={n:load(path) for n,(path,_) in PINS.items()};reuse=mods['reuse']
 def write(name,obj):
  with (out/name).open('x') as f:json.dump(reuse.serial(obj),f,allow_nan=False,separators=(',',':'));f.flush()
 try:
  G=galaxy_config(a.galaxy_config,a.galaxy_config_sha256)
  SOURCE=Path(G['source.monotone_source']['path']);SOURCE_SHA=G['source.monotone_source']['sha256'];OFFSET_SHA=G['custody.offset_finish_sha256']
  NCOL=G['radial.n_columns'];NPHI=G['mesh.n_phi'];OUTER_KPC=G['radial.outer_edge_kpc']
  if G['custody.seed_sha256']!=reuse.SEED_SHA or G['custody.checkpoint_identity_sha256']!=reuse.IDENTITY:raise ValueError('Galaxy config custody differs from bound reuse module')
  check(a.seed,reuse.SEED_SHA);check(SOURCE,SOURCE_SHA);check(a.column_manifest,a.column_manifest_sha256)
  ni=json.loads(Path(a.seed).read_text())['numerical_inputs'];manifest=json.loads(Path(a.column_manifest).read_text())
  for n in ('checkpoint','line','metric'):
   path,pin=reuse.PINS[n];check(path,pin);mods[n]=load(path)
  cm=mods['checkpoint'];cp=Path(a.checkpoint_directory);od=Path(a.offset_directory)
  ident=cm._read(str(cp/'IDENTITY.json'),'identity')
  if ident['identity_sha256']!=reuse.IDENTITY or cm._sha(cm._canonical(ident['identity']))!=reuse.IDENTITY:raise ValueError('Checkpoint identity mismatch')
  caller=cm.decode(ident['identity']['caller']['record']);phys=caller['physical_parameters']
  if caller['seed']['sha256']!=reuse.SEED_SHA:raise ValueError('Seed identity')
  it=route_a_final_iteration(cm,cp,reuse.IDENTITY,G['route_a.accepted_iteration'])
  ITDIR='iteration_%04d'%it
  start=cm._read(str(cp/(ITDIR+'/START.json')),'iteration_start');done=cm._read(str(cp/(ITDIR+'/COMPLETED.json')),'iteration_completed')
  if start['identity_sha256']!=reuse.IDENTITY or done['iteration_start_sha256']!=start['payload_sha256'] or done['converged']is not True:raise ValueError('Accepted current mismatch')
  check(od/'finish.json',OFFSET_SHA);finish=json.loads((od/'finish.json').read_text());pack={}
  for name in ('updated_base_arrays.npz','offset_prepared.npz'):
   ref=finish['outputs'][name];check(ref['path'],ref['sha256'])
   with np.load(ref['path'],allow_pickle=False) as f:pack[name]={k:f[k].copy() for k in f.files}
  base=pack['updated_base_arrays.npz'];off=pack['offset_prepared.npz'];columns={};custody=[]
  REGISTERED_NCOL=NCOL;NCOL=UVT.ngc_effective_n_columns(REGISTERED_NCOL,ni,caller,(reuse.PROFILE,reuse.PROFILE_SHA),base['radial_nodes_m'])
  base_K_source=finish['outputs']['updated_base_arrays.npz'];base_K_values=base['K0'][:,0,0].copy();scaled_K_values=a.entropy_scale*base_K_values
  if not np.isfinite(scaled_K_values).all() or np.any(scaled_K_values<=0):raise ValueError('Nonfinite/underflowed scaled K')
  fd=Path(a.feedback_directory);check(fd/'finish.json',a.feedback_finish_sha256)
  ff=json.loads((fd/'finish.json').read_text());fs=json.loads((fd/'start.json').read_text())
  if ff['status']!='REFRESHED_LAGGED_PREPARED_FIELD_NOT_EQUILIBRIUM' or fs['worker_sha256']!=a.feedback_worker_sha256 or fs['seed_sha256']!=reuse.SEED_SHA or fs['checkpoint_start']!=start['payload_sha256'] or fs['offset_finish_sha256']!=OFFSET_SHA or ff['source_offset_applied_once']is not True:raise ValueError('Refreshed total field custody')
  totalref=ff['outputs']['refreshed_prepared.npz'];check(totalref['path'],totalref['sha256'])
  currentgasref=ff['outputs']['gas_source_feedback.npz'];check(currentgasref['path'],currentgasref['sha256'])
  field_provenance=dict(kind='refreshed_total',feedback_finish_sha256=a.feedback_finish_sha256,feedback_directory=str(fd.resolve()),prepared_packet=totalref,feedback_worker_sha256=a.feedback_worker_sha256,current_gas_packet=currentgasref,current_gas_array_key='new_gas_fourier_J')
  for run in manifest['runs']:
   folder=Path(run['directory']);check(folder/'finish.json',run['finish_sha256']);rf=json.loads((folder/'finish.json').read_text());rs=json.loads((folder/'start.json').read_text())
   if rs['worker_sha256']!=a.column_worker_sha256 or rs['seed_sha256']!=reuse.SEED_SHA or rs['offset_finish_sha256']!=OFFSET_SHA or rs['checkpoint_start']!=start['payload_sha256']:raise ValueError('Column field/source provenance')
   if rs['entropy_scale']!=a.entropy_scale or rf['entropy_scale']!=a.entropy_scale or rs['base_K_source']!=base_K_source or rf['base_K_source']!=base_K_source or not np.array_equal(rs['base_K_values_SI'],base_K_values) or not np.array_equal(rf['base_K_values_SI'],base_K_values) or not np.array_equal(rs['scaled_K_values_SI'],scaled_K_values) or not np.array_equal(rf['scaled_K_values_SI'],scaled_K_values):raise ValueError('Column entropy scale/baseK preparation mismatch')
   if rf['status']!='LAGGED_FREE_SURFACE_COLUMNS_ONLY' or rs['field_provenance']!=field_provenance or rf['field_provenance']!=field_provenance:raise ValueError('Column run/field identity')
   for item in rf['completed']:
    check(item['path'],item['sha256']);col=json.loads(Path(item['path']).read_text());i=item['index']
    if i in columns or col['radial_index']!=i or col['field_provenance']!=field_provenance or col['entropy_scale']!=a.entropy_scale or col['base_K_source']!=base_K_source or col['base_K_SI']!=base_K_values[i]:raise ValueError('Duplicate/wrong/mixed-field column')
    columns[i]=col;custody.append(item)
  if set(columns)!=set(range(NCOL)):raise ValueError('Missing complete%d successful columns'%NCOL)
  columns=[columns[i] for i in range(NCOL)]
  joined=mods['join'].join(columns=columns,radial_nodes_m=base['radial_nodes_m'],radial_RdR_weights_m2=base['radial_RdR_weights_m2'],expected_Sigma=base['Sigma_kg_m2'],expected_K=scaled_K_values,gamma=5/3,c_m_s=phys['c_m_s'],n_phi=NPHI,mass_relative_tolerance=a.mass_relative_tolerance,n_columns=NCOL)
  arrays=joined['arrays'];R=arrays['radial_nodes_m'];K=arrays['K0'][:,0,0];nz=arrays['z'].shape[2]
  profile=json.loads(SOURCE.read_text())['source_record'];edges=np.asarray(profile['s_edges_kpc2']);d=np.asarray(profile['boundary_controls_Msun_pc2']);mean=np.asarray(profile['annular_means_Msun_pc2']);b=3*mean-d[:-1]-d[1:];kpc=ni['kpc_m'];unit=ni['solar_mass_kg']/(kpc/1000)**2
  q=(R/kpc)**2;bins=np.searchsorted(edges,q,side='right')-1
  if np.any(bins<0) or np.any(bins>=len(mean)):raise ValueError('Radial source domain')
  t=(q-edges[bins])/(edges[bins+1]-edges[bins]);Sigma_R=unit*2*((b[bins]-d[bins])*(1-t)+(d[bins+1]-b[bins])*t)/(edges[bins+1]-edges[bins])*(2*R/kpc**2)
  J=radial_truncation(edges,OUTER_KPC);Rout=np.sqrt(edges[J])*kpc;_,Ds=mods['mesh']._spline_matrices((R/Rout)**2,list((R/Rout)**2));D=2*R[:,None]/Rout**2*Ds
  k=np.einsum('ij,j->i',D,np.log(K),optimize=False);kR=np.einsum('ij,j->i',D,k,optimize=False)
  waves=cm._get(str(cp),start['prepared_wavevectors']);amps=cm._get(str(cp),start['prepared_weighted_responses'])
  if not np.array_equal(waves,off['wavevectors']):raise ValueError('Wave identity')
  with np.load(totalref['path'],allow_pickle=False) as f:prepared={k:f[k].copy() for k in ('wavevectors','weighted_responses')}
  if not np.array_equal(prepared['wavevectors'],waves) or prepared['weighted_responses'].shape!=amps.shape or not np.isfinite(prepared['weighted_responses']).all():raise ValueError('Refreshed field shape/order/finiteness')
  uvt=UVT.open_binding(a,'le_rotation').bind(ni=ni,phys=phys,caller=caller,galaxy=G['galaxy.key'],profile=(reuse.PROFILE,reuse.PROFILE_SHA),identity=reuse.IDENTITY,iteration=it,start=start,prepared=prepared,cm=cm,cp=cp,offset_finish=finish,feedback_start=fs,feedback_finish=ff,column_manifest=manifest,radii=R)
  # TOTAL packet already includes every original/offset contribution, never add again.
  write('start.json',dict(worker_sha256=sha(__file__),entropy_scale=a.entropy_scale,base_K_source=base_K_source,base_K_values_SI=base_K_values,scaled_K_values_SI=scaled_K_values,preparation_scope='Separate global entropy preparation; no guarantee final observed dispersion matches original-density label',producer_sha_inputs={'column-worker-sha256':a.column_worker_sha256,'feedback-worker-sha256':a.feedback_worker_sha256},code_pins={str(p):s for p,s in PINS.values()},dependency_pins={n:[str(p),s] for n,(p,s) in reuse.PINS.items() if n in ('checkpoint','line','metric')},column_manifest_sha256=a.column_manifest_sha256,column_custody=custody,seed_sha256=reuse.SEED_SHA,source_sha256=SOURCE_SHA,offset_finish_sha256=OFFSET_SHA,checkpoint_start=start['payload_sha256'],field_provenance=field_provenance,mass_relative_tolerance=a.mass_relative_tolerance,K_interpolation='Natural cubic log K in s=(R/Rout)^2; nodal K unchanged. Radial second derivative uses same sampled D.',source_contract='Increment refreshedTOTAL only with unit*(latestgas-current_gas_packet/new_gas_fourier_J). Alternatively recompute from original G4+unit*(latestgas-actual G4gas). Never add latest-originalbody to refreshedTOTAL; do not combine routes.',**uvt.record()))
  fields=np.empty((NCOL,NPHI,nz,10),complex);gradient=np.empty(fields.shape+(3,),complex);hessian=np.empty(fields.shape+(3,3),complex);Phi=np.empty((NCOL,NPHI,nz));PR=np.empty_like(Phi);PZ=np.empty_like(Phi);PP=np.empty_like(Phi)
  with (out/'progress.jsonl').open('x') as log:
   for i in range(NCOL):
    for j in range(NPHI):
     phi=2*np.pi*j/NPHI;line=mods['line'].prepare_line(prepared=prepared,x_m=R[i]*np.cos(phi),y_m=R[i]*np.sin(phi))
     for l,z in enumerate(arrays['z'][i,j]):
      pkt=mods['line'].evaluate_line(line=line,z_m=float(z),**uvt.line_jets(line,float(z)))
      f=pkt['fields'][0,:,0];g=pkt['gradient'][0,:,0];hh=pkt['hessian'][0,:,0]
      for value in (f,g,hh):
       if not np.isfinite(value).all() or np.any(np.abs(value.imag)>ni['reality_atol']+ni['reality_rtol']*np.abs(value.real)):raise ValueError('Full field/jet reality')
      metric=mods['metric'].evaluate_point(delta_fields=f.real,delta_gradient_physical=g.real,Cbar=phys['Cbar'],mubar=phys['mubar'],R=float(R[i]),phi=float(phi),z=float(z))
      N=1+f[0].real
      fields[i,j,l]=f;gradient[i,j,l]=g;hessian[i,j,l]=hh
      Phi[i,j,l]=phys['c_m_s']**2*np.log1p(f[0].real)
      PR[i,j,l]=phys['c_m_s']**2*(g[0,0].real*np.cos(phi)+g[0,1].real*np.sin(phi))/N
      PZ[i,j,l]=phys['c_m_s']**2*g[0,2].real/N
      PP[i,j,l]=phys['c_m_s']**2*(-g[0,0].real*np.sin(phi)+g[0,1].real*np.cos(phi))/N
    log.write(json.dumps(dict(radial_index=i,elapsed_seconds=time.monotonic()-clock))+'\n');log.flush()
  pr=np.mean(PR,axis=1);pz=np.mean(PZ,axis=1);phi0=np.mean(Phi,axis=1)
  rotation=mods['rotation'].evaluate(R=R,Sigma=arrays['Sigma_kg_m2'],Sigma_R=Sigma_R,K=K,logK_R=k,logK_RR=kR,radial_derivative=D,weights=np.array([c['weights_m'] for c in columns]),rho=arrays['rho0'][:,0,:],h=arrays['enthalpy'][:,0,:],Phi_R=pr,Phi_z=pz,gamma=5/3)
  arrays.update(full_fields_complex=fields,full_gradient_complex=gradient,full_hessian_complex=hessian,Phi0=np.broadcast_to(phi0[:,None,:],Phi.shape).copy(),angular_forcing_dPhi=Phi-phi0[:,None,:],Phi_R_full=PR,Phi_z_full=PZ,Sigma_R=Sigma_R,radial_derivative=D)
  for name,value in rotation['arrays'].items():arrays['rotation_'+name]=value
  # Full angular radial/vertical residual of the m0 circular construction; no claim they vanish.
  arrays['angular_radial_residual']=PR-pr[:,None,:];arrays['angular_vertical_residual']=PZ-pz[:,None,:];arrays['angular_azimuthal_residual']=PP
  arrays['base_residual_r0']=np.stack((np.broadcast_to(rotation['arrays']['radial_Euler_residual'][:,None,:],Phi.shape),np.zeros_like(Phi),np.broadcast_to(rotation['arrays']['vertical_Euler_residual'][:,None,:],Phi.shape)),axis=-1)
  if rotation['positive_rotation_square']:
   for name in ('Omega','Omega_R_approx','Omega_z'):arrays[name]=np.broadcast_to(rotation['arrays'][name][:,None,:],Phi.shape).copy()
  if any(not np.isfinite(v).all() for v in arrays.values()):raise ValueError('Nonfinite saved output')
  np.savez(out/'rotation_base_arrays.npz',**arrays)
  write('finish.json',dict(status='LAGGED_M0_ROTATION_EVALUATED_NOT_FULL_FLOW',entropy_scale=a.entropy_scale,base_K_source=base_K_source,base_K_values_SI=base_K_values,scaled_K_values_SI=scaled_K_values,preparation_scope='Same scaled entropy candidate across all%d; not an inference of final dispersion'%NCOL,arrays_path=str(out/'rotation_base_arrays.npz'),arrays_sha256=sha(out/'rotation_base_arrays.npz'),field_provenance=field_provenance,positive_rotation_square=rotation['positive_rotation_square'],nonpositive_indices=rotation['nonpositive_indices'],minimum_rotation_square=float(np.min(rotation['arrays']['Omega_squared'])),elapsed_seconds=time.monotonic()-clock,scope=rotation['scope'],source_feedback_applied=False,limits=['Same lagged field, new source has not been fed back','Full anisotropic residual retained; no stationary-flow acceptance','Native mixing unresolved','Fixed K spline and finite32-point quadrature are declared approximations','New weak operator must use32-point source/test quadrature with separately specified8 continuous trial coefficients'],**uvt.record(final=True)))
 except Exception as exc:
  write('failure.json',dict(type=type(exc).__name__,message=str(exc),elapsed_seconds=time.monotonic()-clock));raise
if __name__=='__main__':main()
