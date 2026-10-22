"""Root-only full10 affine source offset, no displacement or fluid solve.
Build -K^-1 e_n once, transform normalized body source, subtract the actual
accepted G4 gas Fourier blob. Fixed stars cancel only because they are unchanged.
No division by old source, isotropization, inverse regularization or new roots.
"""
# UVT_C2V001 (Claude2 tail_scheme_impl_c2/route_b): successor of ddo_body_source_offset_root_v003_gal_c2v005.py (sha256 1ee18dcdcc42fc2465cebcc120297f262839fc4506249416b4d71d6a00be3dd4).
# uvt_c2v001 change (TAIL_SCHEME_DESIGN_V002 sec 1.1/1.3/2.2/3.6 with V002_R1; stage kind offset): the UV-tail lapse enters only
#   through the reviewed additive boundary slots, via the pinned shared binding uvt_route_b_binding_c2v001.py. Required argv
#   --uv-tail-config/--uv-tail-config-sha256 (certificates are config fields, verified from bytes at build; R1 IA6).
#   enabled=false: the binding returns the reviewed zero literals and adds no record; the reviewed body runs unchanged.
#   enabled=true with an empty domain (O inside C): the same zero literals (no addition anywhere), plus the uv_tail record.
#   slots: L258 split: fields[:,0] += t[Delta](pos) before the total, non-empty state only (N1: diagnostic); state built after the forward sum L238-246.
# GAL_C2V005 (Claude2 stage_successor_gal_c2v005): successor of ddo_body_source_offset_root_v003_gal_c2v004.py (sha256 e821ae42b643ecf9ff2362f8d5dd3e56056b3300df929d290e9b3eb7558bc480).
# c2v005 change (ROOT_DECISIONS_NGC3198 V003 addendum 5bef6552b92b0939... A13 deciding work), the shared admission only:
#   schema V005 pin; PER_CALL admitted on the DDO154 per-call geometry fields (PER_CALL_GEOMETRY and the schema
#   per_call_geometry declaration); a config without such a field is admitted exactly as c2v004. No other change.
# GAL_C2V004 (Claude2 ngc_f10_c2/route_b_v006): successor of ddo_body_source_offset_root_v003_gal_c2v003.py (sha256 5fb1660f4fe55599073c8756010a0b6af3254a181f876d1928dedf899686d7f2).
# c2v004 changes (ROOT_DECISIONS_NGC3198 V002 addendum 4070146dbd85c3cb...):
#   admission: shared c2v004 admit_config on GALAXY_CONFIG_SCHEMA_V004 (A4 values; A2 member entries, CHECK D2);
#       a config without member is admitted exactly as c2v003
#   no other change
# GAL_C2V003 (Claude2 ngc_route_impl_c2/binding): successor of ddo_body_source_offset_root_v003_gal_c2v002.py (sha256 4dcf0c5e23d5346d90832f8e625efa6f053ca1572fe651109264be91a884d96f).
# c2v003 changes (ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001 06cae881fe075b42...):
#   admission: shared c2v003 admit_config on GALAXY_CONFIG_SCHEMA_V003 (N5)
#   N2: the outer-edge guard accepts radial.outer_edge_kpc = sqrt(profile s_edges[J]) (radial_truncation) and the mesh
#       domain is [0, sqrt(s_edges[J])*kpc]; DDO154 J = last edge (the old guard and domain, bitwise)
# GAL_C2V002 (Claude2 ngc_route_construction_c2/v004_fix): successor of the galaxy-config
# successor ddo_body_source_offset_root_v003_gal_c2v001 (665b9334...) of reviewed
# ddo_body_source_offset_root_v003 (sha c5faed57...). Only DDO literals are fields of
# --galaxy-config (schema UNT_ROUTE_B_GALAXY_CONFIG_SCHEMA_V002). c2v002 changes ONLY admission:
# the shared status-whitelist admission admit_config (CHECK_V001 D1) and the shared strict
# route-A reader route_a_final_iteration (CHECK_V001 D2/D3). Every equation, tolerance, guard,
# output and flag of v003 is kept. A field that is not admitted is refused, never guessed.
import argparse,hashlib,importlib.util,json,time
from pathlib import Path
import numpy as np
O=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method');H=O.parent/'recovered_packet_audit';HP=O.parent/'response_packet_audit';C=O.parent.parent/'CODEX1'
PINS={
'reuse':(H/'ddo_homotopy_reference_root_worker_v001.py','acda989d375925bf9a8163d8d8a3a22c3f183b6b253c8137312bccc0cefbbe36'),
'mesh':(O/'owned_body_fitted_displacement_binding_v002.py','87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462'),
'fourier':(H/'owned_physical_fourier_metric_quadrature_v005.py','7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491'),
'cache':(H/'owned_scalar_lapse_inverse_cache_v001.py','7b9816aea218d638c2eece184df22e29ca18b68547f3d04193780c2eff96a529'),
'cardinal':(O/'owned_positive_cardinal_source_hessian_v001.py','4d123c1f01bdb20f2bd8a0dcc42e12475f09850eff8f6bbca9d5953d01326848'),
'complex':(O/'owned_complex_symbol_metric_binding_v002.py','701095f9c3cbe90f28605ef3676ae7889dbaa6e4686630c424f79a1feea9cdcc'),
'static':(HP/'owned_static_action_metric_binding_v002.py','7130a277ca59b07c8ce788eb20bcb50c996a3575f6fa0e644e971b0d766aee1f')}
COEFF=None;COEFF_SHA=None # driver override slots only; the value is galaxy-config source.coefficients
CONFIG_FORMAT='UNT_ROUTE_B_STAGE_CONFIG_OFFSET_C2V003';HEX='0123456789abcdef'
NEEDED={'galaxy.key':'key','source.profile':'pin','source.coefficients':'pin','custody.body_worker_sha256':'sha','route_a.accepted_iteration':'iteration','radial.n_columns':'count','radial.outer_edge_kpc':'positive','mesh.n_phi':'count','mesh.eta_order':'count'}
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
def galaxy_config(path,pin):
 """Admitted config -> {field: value} for NEEDED (shared admission, then this stage's type checks)."""
 galaxy,g,_=admit_config(path,pin,CONFIG_FORMAT,tuple(NEEDED));bad=[]
 for name,kind in NEEDED.items():
  v=g[name]
  if kind=='key':ok=type(v)is str and v!=''
  elif kind=='pin':ok=type(v)is dict and set(v)=={'path','sha256'} and type(v['path'])is str and type(v['sha256'])is str and len(v['sha256'])==64 and all(c in HEX for c in v['sha256'])
  elif kind=='sha':ok=type(v)is str and len(v)==64 and all(c in HEX for c in v)
  elif kind=='iteration':ok=type(v)is int and 0<=v<=9999
  elif kind=='count':ok=type(v)is int and v>=1
  else:ok=type(v)is float and bool(np.isfinite(v)) and v>0
  if not ok:bad.append(name+':TYPE')
 if bad:raise GalaxyConfigRefused('GALAXY_CONFIG_INVALID galaxy=%s: %s'%(galaxy,'; '.join(bad)))
 return g
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(p,pin):
 if sha(p)!=pin:raise ValueError('Pin mismatch: '+str(p))
def load(p):
 s=importlib.util.spec_from_file_location('offset_'+Path(p).stem,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def finite(x,label):
 if not np.isfinite(x).all():raise ValueError('Nonfinite '+label)
 return x

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
 for k in ('seed','checkpoint-directory','body-directory','body-finish-sha256','outdir'):p.add_argument('--'+k,required=True)
 for k in ('wave-batch','position-batch'):p.add_argument('--'+k,required=True,type=int)
 for k in ('galaxy-config','galaxy-config-sha256'):p.add_argument('--'+k,required=True)
 UVT=uvt_load();UVT.add_argv(p,'offset');a=p.parse_args();out=Path(a.outdir);out.mkdir(exist_ok=False);t0=time.monotonic();stage='admission'
 if not 1<=a.wave_batch<=1024 or not 1<=a.position_batch<=1024:raise ValueError('Explicit bounded batches1..1024 required')
 def write(name,obj):
  with (out/name).open('x') as f:json.dump(reuse.serial(obj),f,allow_nan=False,separators=(',',':'));f.flush()
 try:
  g=galaxy_config(a.galaxy_config,a.galaxy_config_sha256);GK=g['galaxy.key'];NC=g['radial.n_columns'];NPHI=g['mesh.n_phi'];NETA=g['mesh.eta_order']
  coeff=Path(g['source.coefficients']['path']);coeff_sha=g['source.coefficients']['sha256']
  if (COEFF,COEFF_SHA)!=(None,None) and (COEFF is None or COEFF_SHA is None or Path(COEFF).resolve()!=coeff.resolve() or COEFF_SHA!=coeff_sha):raise ValueError('Driver coefficient override differs from galaxy config source.coefficients')
  for path,pin in PINS.values():check(path,pin)
  check(coeff,coeff_sha);mods={k:load(path) for k,(path,_) in PINS.items()};reuse=mods['reuse']
  check(a.seed,reuse.SEED_SHA);seed=json.loads(Path(a.seed).read_text());ni=seed['numerical_inputs'];cp=Path(a.checkpoint_directory)
  path,pin=reuse.PINS['checkpoint'];check(path,pin);cm=load(path)
  ident=cm._read(str(cp/'IDENTITY.json'),'identity')
  if ident['identity_sha256']!=reuse.IDENTITY or cm._sha(cm._canonical(ident['identity']))!=reuse.IDENTITY:raise ValueError('Identity mismatch')
  caller=cm.decode(ident['identity']['caller']['record']);phys=caller['physical_parameters']
  if caller['seed']['sha256']!=reuse.SEED_SHA:raise ValueError('Seed identity mismatch')
  REGISTERED_NC=NC;NC=UVT.ngc_effective_n_columns(REGISTERED_NC,ni,caller,(reuse.PROFILE,reuse.PROFILE_SHA))
  it=route_a_final_iteration(cm,cp,reuse.IDENTITY,g['route_a.accepted_iteration'])
  start=cm._read(str(cp/('iteration_%04d'%it)/'START.json'),'iteration_start');done=cm._read(str(cp/('iteration_%04d'%it)/'COMPLETED.json'),'iteration_completed')
  if start['iteration']!=it or done['iteration']!=it:raise ValueError('Route-A iteration record mismatch')
  bd=Path(a.body_directory);check(bd/'finish.json',a.body_finish_sha256);bf=json.loads((bd/'finish.json').read_text());bs=json.loads((bd/'start.json').read_text())
  if bs['worker_sha256']!=g['custody.body_worker_sha256'] or bf['status']!='EVALUATED_REFERENCE_ARRAYS_NOT_FLOW_SOLUTION' or len(bf['completed'])!=NC:raise ValueError('Actual complete reviewed body assembly required')
  if start['identity_sha256']!=reuse.IDENTITY or done['identity_sha256']!=reuse.IDENTITY or done['converged']is not True or done['iteration_start_sha256']!=start['payload_sha256'] or bs['prepared_custody']['start']!=start['payload_sha256'] or bs['prepared_custody']['completed']!=done['payload_sha256']:raise ValueError('Body/current source custody mismatch')
  check(bf['array_file'],bf['array_sha256'])
  with np.load(bf['array_file'],allow_pickle=False) as f:body={k:f[k].copy() for k in f.files}
  UVT.ngc_effective_n_columns(REGISTERED_NC,ni,caller,(reuse.PROFILE,reuse.PROFILE_SHA),body['radial_nodes_m'])
  uvt=UVT.open_binding(a,'offset').bind(ni=ni,phys=phys,caller=caller,galaxy=GK,profile=(reuse.PROFILE,reuse.PROFILE_SHA),identity=reuse.IDENTITY,iteration=it,start=start,body_finish=bf)
  check(reuse.PROFILE,reuse.PROFILE_SHA)
  if Path(g['source.profile']['path']).resolve()!=Path(reuse.PROFILE).resolve() or g['source.profile']['sha256']!=reuse.PROFILE_SHA:raise ValueError('Galaxy config source.profile differs from the reviewed reference profile')
  PE=json.loads(reuse.PROFILE.read_text())['galaxies'][GK]['HI_plus_He']['s_edges_kpc2'];J=radial_truncation(PE,g['radial.outer_edge_kpc'])
  mesh=mods['mesh'].make_mesh(radial_nodes_m=body['radial_nodes_m'],radial_RdR_weights_m2=body['radial_RdR_weights_m2'],radial_domain_m=[0.,UVT.ngc_radial_domain_upper(float(np.sqrt(PE[J])*ni['kpc_m']),ni,caller)],roots_m=body['roots_m'],eta_nodes=body['eta_nodes'],eta_weights=body['eta_weights'],n_phi=NPHI)
  for k in ('R','phi','z','volume_weights_m3','physical_positions_m'):
   if not np.array_equal(mesh[k],body[k]):raise ValueError('Reconstructed mesh differs: '+k)
  old=cm._get(str(cp),start['gas_fourier_J']);waves=cm._get(str(cp),start['prepared_wavevectors'])
  if bs['old_source_references']['gas_fourier_J']!=start['gas_fourier_J'] or bs['old_source_references']['fixed_source_fourier_J']!=start['fixed_source_fourier_J']:raise ValueError('Old source blob reference mismatch')
  if old.shape!=(len(waves),10,1) or np.any(old[:,1:,:]!=0):raise ValueError('Actual G4 must use existing scalar rest-energy source')
  # Exact existing panel quadrature; never infer weights from old response/source.
  rebuilt,weights=UVT.ngc_offset_grid(ni)
  if not np.array_equal(waves,rebuilt):raise ValueError('Existing physical wave node order mismatch')
  with np.load(coeff,allow_pickle=False) as f:grid=f['source_hessian_grid'].copy();mu=f['background_mu'].copy();Cbar=f['background_C'].copy()
  if not np.array_equal(Cbar,phys['Cbar']) or not np.array_equal(mu,phys['mubar']):raise ValueError('Frozen background mismatch')
  fa=dict(source_hessian_grid=grid,k_physical=waves,dk_weights=weights,registered_bravais=np.array([[0.,.5,.5],[.5,0.,.5],[.5,.5,0.]]),jbar=np.zeros(9),mubar=mu,Cbar=Cbar,Eref=ni['Eref_J'],ell_F=ni['ell_F_m'],gamma=ni['gamma'],cardinal_module=mods['cardinal'],complex_binding_module=mods['complex'],static_binding_module=mods['static'],relative_singular_floor=ni['relative_singular_floor'],hermitian_tolerance=ni['hermitian_tolerance'],full_residual_relative_tolerance=ni['solve_rtol'],full_residual_absolute_tolerance=ni['solve_atol'],node_convention='full_signed',real_source_pairing_declared=True,finite_domain_description='Exact accepted signed composite cube; no tail/quadrature error bound',boundary_description='Same isolated zero perturbation boundary; fixed stars unchanged')
  # Check every numeric physics/control argument against original checkpoint digests.
  dig=ident['identity']['inputs_sha256']['fourier_arguments']
  for k,v in fa.items():
   if k.endswith('_module') or k in ('finite_domain_description','boundary_description'):continue
   if cm.digest(v)!=dig[k]:raise ValueError('Original operator argument differs: '+k)
  write('start.json',dict(worker_sha256=sha(__file__),code_pins={str(p):s for p,s in PINS.values()},body_finish_sha256=a.body_finish_sha256,body_array_sha256=bf['array_sha256'],coefficient_sha256=coeff_sha,seed_sha256=reuse.SEED_SHA,old_gas=start['gas_fourier_J'],fixed_stars=start['fixed_source_fourier_J'],checkpoint_directory=str(cp.resolve()),wave_batch=a.wave_batch,position_batch=a.position_batch,scope='Affine base-source offset only; no flow solution or revised native state',**uvt.record()))
  stage='unit_response';cache=mods['cache'].make_fourier_module(base_module=mods['fourier'],log_directory=str(out/'unit_nodes'),start_iteration=0)
  unit_source=np.zeros((len(waves),10,1),complex);unit_source[:,0,0]=1
  unit=cache.prepare(**fa,source_density_fourier=unit_source)
  np.savez(out/'unit_response.npz',wavevectors=waves,dk_weights=weights,weighted_responses=unit['weighted_responses'])
  stage='new_body_forward_transform';pos=body['physical_positions_m'].reshape(-1,3);J=body['base_integrated_source_J'].reshape(-1,10,1)
  if np.any(J[:,1:,:]!=0):raise ValueError('Only existing leading scalar base source supported')
  new=np.zeros_like(old)
  with (out/'progress.jsonl').open('x') as log:
   for i in range(0,len(waves),a.wave_batch):
    k=waves[i:i+a.wave_batch];s=np.zeros(len(k),complex)
    for j in range(0,len(pos),a.position_batch):
     phase=np.exp(-1j*np.einsum('ai,bi->ab',k,pos[j:j+a.position_batch],optimize=False));s+=np.einsum('ab,b->a',phase,J[j:j+a.position_batch,0,0],optimize=False)
    new[i:i+len(k),0,0]=finite(s,'forward source')
    log.write(json.dumps(dict(stage=stage,nodes_completed=i+len(k),elapsed_seconds=time.monotonic()-t0))+'\n');log.flush()
   delta=finite(new-old,'source offset');np.savez(out/'source_offset.npz',new_body_fourier_J=new,delta_source_fourier_J=delta)
   uvt.bind_offset(body=body,new=new,waves=waves,unit_weighted_responses=unit['weighted_responses'])
   stage='offset_inverse_transform';offset=cache.prepare(**fa,source_density_fourier=delta)
   np.savez(out/'offset_prepared.npz',wavevectors=waves,weighted_responses=offset['weighted_responses'])
   fields=np.zeros((len(pos),10),complex)
   for j in range(0,len(pos),a.position_batch):
    q=pos[j:j+a.position_batch];v=np.zeros((len(q),10),complex)
    for i in range(0,len(waves),a.wave_batch):
     phase=np.exp(1j*np.einsum('ai,bi->ab',q,waves[i:i+a.wave_batch],optimize=False));v+=np.einsum('ab,bc->ac',phase,offset['weighted_responses'][i:i+a.wave_batch,:,0],optimize=False)
    fields[j:j+len(q)]=finite(v,'offset inverse')
    log.write(json.dumps(dict(stage=stage,positions_completed=j+len(q),elapsed_seconds=time.monotonic()-t0))+'\n');log.flush()
  fields=uvt.offset_fields(fields,pos);fields=fields.reshape((NC,NPHI,NETA,10));total=finite(body['full_fields_real']+1j*body['full_fields_imag']+fields,'total updated fields')
  maxima=np.max(np.abs(total.imag),axis=(0,1,2));bounds=ni['reality_atol']+ni['reality_rtol']*np.max(np.abs(total.real),axis=(0,1,2))
  if np.any(maxima>bounds):raise ValueError('Full updated ten-field reality check failed')
  real=total.real;N=1+real[...,0]
  if np.any(N<=0):raise ValueError('Updated lapse nonpositive')
  minC=float('inf')
  for point in real.reshape(-1,10):
   ev=finite(np.linalg.eigvalsh(Cbar+mods['static'].mandel_matrix(point[1:7])),'updated C eigenvalues');minC=min(minC,float(ev[0]))
  if minC<=0:raise ValueError('Updated spatial metric nonpositive')
  potential=finite(phys['c_m_s']**2*np.log1p(real[...,0]),'updated potential');mean=np.mean(potential,axis=1,keepdims=True);phi0=finite(np.broadcast_to(mean,(NC,NPHI,NETA)).copy(),'updated mean potential')
  r0=np.stack((mesh['partial_R'](phi0)+mesh['partial_R'](body['P0'])/body['rho0']-mesh['R']*body['Omega']**2,np.zeros((NC,NPHI,NETA)),mesh['partial_z'](phi0)+mesh['partial_z'](body['P0'])/body['rho0']),axis=-1)
  saved={k:body[k] for k in ('R','phi','z','volume_weights_m3','physical_positions_m','radial_nodes_m','radial_RdR_weights_m2','eta_nodes','eta_weights','roots_m','rho0','P0','K0','Omega','Sigma_kg_m2')}
  saved.update(Phi0=phi0,angular_forcing_dPhi=potential-phi0,base_residual_r0=r0,offset_fields_complex=fields,full_fields_complex=total)
  for key,value in saved.items():finite(value,'saved '+key)
  np.savez(out/'updated_base_arrays.npz',**saved)
  write('finish.json',dict(status='AFFINE_BASE_OFFSET_EVALUATED_NOT_FLOW_SOLUTION',outputs={name:dict(path=str(out/name),sha256=sha(out/name)) for name in ('unit_response.npz','source_offset.npz','offset_prepared.npz','updated_base_arrays.npz')},elapsed_seconds=time.monotonic()-t0,reality_maxima=maxima,reality_bounds=bounds,minimum_C_eigenvalue=minC,source_offset_applied_once=True,lagged_callback_contract='ONLY displacement delta_f=-c^2 delta_rho; do not add base-G4 again',base_scope='rho/P/K/Omega and saved surfaces retained as reference, not re-equilibrated; updated m0 and angular potential and same-discrete r0 include complete offset',limits=['Native mixing failed','Finite Fourier/GL8 source quadrature errors not certified','No nonlinear gas equilibrium, boundary solve, modal action or stationary flow asserted'],**uvt.record(final=True)))
 except Exception as exc:
  with (out/'failure.json').open('x') as f:json.dump(dict(stage=stage,type=type(exc).__name__,message=str(exc),elapsed_seconds=time.monotonic()-t0),f)
  raise
if __name__=='__main__':main()
