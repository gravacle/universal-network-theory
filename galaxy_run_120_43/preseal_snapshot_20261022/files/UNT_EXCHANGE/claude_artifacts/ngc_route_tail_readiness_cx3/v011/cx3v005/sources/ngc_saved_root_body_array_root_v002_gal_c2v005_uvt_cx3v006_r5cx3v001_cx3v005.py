"""Inert root CLI: evaluated n_columns x n_phi x eta_order normalized reference, not a flow solution.
Reuses accepted route-A final-iteration CURRENT waves and saved roots. No source inversion,
root search, action import, or displacement solve. Keeps old-field/new-source offset explicit.
"""
import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path
import numpy as np
# UVT_C2V001 (Claude2 tail_scheme_impl_c2/route_b): successor of ddo_saved_root_body_array_root_v002_gal_c2v005.py (sha256 7387493b6e2e153afd0e2352cf630edd32944d641dc563a706381983add0b1e3).
# uvt_c2v001 change (TAIL_SCHEME_DESIGN_V002 sec 1.1/1.3/2.2/3.6 with V002_R1; stage kind body): the UV-tail lapse enters only
#   through the reviewed additive boundary slots, via the pinned shared binding uvt_route_b_binding_c2v001.py. Required argv
#   --uv-tail-config/--uv-tail-config-sha256 (certificates are config fields, verified from bytes at build; R1 IA6).
#   enabled=false: the binding returns the reviewed zero literals and adds no record; the reviewed body runs unchanged.
#   enabled=true with an empty domain (O inside C): the same zero literals (no addition anywhere), plus the uv_tail record.
#   slots: boundary closure L248-249 (tail jets; K0 via the reference logN0 and the body angular reads, CHECK F1); bind after prepared L220 (route-A manifest state == reference state).
# GAL_C2V005 (Claude2 stage_successor_gal_c2v005): successor of ddo_saved_root_body_array_root_v002_gal_c2v004.py (sha256 0bf1c4cbd1e768f7b0ab461c5cb439d8e40ebe64cf91fedccc5254603f8c0dd7).
# c2v005 change (ROOT_DECISIONS_NGC3198 V003 addendum 5bef6552b92b0939... A13 deciding work), the shared admission only:
#   schema V005 pin; PER_CALL admitted on the DDO154 per-call geometry fields (PER_CALL_GEOMETRY and the schema
#   per_call_geometry declaration); a config without such a field is admitted exactly as c2v004. No other change.
# GAL_C2V004 (Claude2 ngc_f10_c2/route_b_v006): successor of ddo_saved_root_body_array_root_v002_gal_c2v003.py (sha256 5eb33018e2ce7fbc52caea897651169cf3d0b310f140b98f99136fa9540e6d63).
# c2v004 changes (ROOT_DECISIONS_NGC3198 V002 addendum 4070146dbd85c3cb...):
#   admission: shared c2v004 admit_config on GALAXY_CONFIG_SCHEMA_V004 (A4 values; A2 member entries, CHECK D2);
#       a config without member is admitted exactly as c2v003
#   D3: J < last edge -> the monotone source record must be the prefix form (edges[:J+1], means[:J]); J = last -> the
#       full form (DDO154, as before)
#   D4: the N2 domain-edge guard runs before the per-radius loop (same condition and message)
# GAL_C2V003 (Claude2 ngc_route_impl_c2/binding): successor of ddo_saved_root_body_array_root_v002_gal_c2v001.py (sha256 48cc60c4a046bcf26a6109d3c9711502c0905ce012d920bfbd0d3c3e4464a66b).
# c2v003 changes (ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001 06cae881fe075b42...):
#   admission: shared c2v003 admit_config on GALAXY_CONFIG_SCHEMA_V003 (N5; supersedes both V002 files, stages2 CHECK D1/D6)
#   route A: the c2v002 strict reader route_a_final_iteration verbatim (stages2 CHECK D2)
#   N2: radial.outer_edge_kpc consumed; J = radial_truncation(profile s_edges); the monotone source record must equal the
#       profile edges/means in full or cut at J; the GL roster runs over annuli 0..J-1; the reference domain edge must be
#       sqrt(s_edges[J])*kpc (added guard). DDO154: J = last edge, every expression is the old one.
# GAL_C2V001 (Claude2 ngc_route_construction_c2/stages2): galaxy-config successor of reviewed
# ddo_saved_root_body_array_root_v002.py (sha 271e5612caf00cbde3a154d6deb4c7c4d5c7ec342b9ede893e0bf820d044a8f6).
# Only DDO154 literals became fields of --galaxy-config (schema UNT_ROUTE_B_GALAXY_CONFIG_SCHEMA_V002,
# format UNT_ROUTE_B_GALAXY_CONFIG_INSTANCE_STAGES2_C2V001); with the DDO154 config each equals the old literal.
# The route-A iteration is the config value AND the checkpoint records' single converged final iteration.
# The reviewed stage directory is absolute so every PINS path is unchanged by relocation. Every equation,
# tolerance, guard, output file and output key of the base is kept. A field holding NONE_IN_REVIEWED_CODE,
# NOT_APPLICABLE or DERIVED_FROM_BYTES_CONDITIONAL is refused before any output, never guessed.
# Also: the reference roster rule (reference:74-77,85: drop GL nodes whose reference-profile Sigma is exactly 0)
# is applied before the unchanged guard R == reference radii_m (schema S2); the body base is the n_phi successor
# owned_saved_root_body_base_v003_gal_c2v001.py; REFERENCE/SOURCE/DATA_PINS come from custody.reference_run and source.monotone_source.

O=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method');H=O.parent/'recovered_packet_audit';C=O.parent.parent/'CODEX1'
PINS={
 'reuse':(H/'ddo_homotopy_reference_root_worker_v001.py','acda989d375925bf9a8163d8d8a3a22c3f183b6b253c8137312bccc0cefbbe36'),
 'base':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_construction_c2/stages2/modules/owned_saved_root_body_base_v003_gal_c2v001.py'),'d540fd7c1a943e94355d273f4329e1f0d350dbcf8be5a2db22b82577d6d87329'),
 'mesh':(O/'owned_body_fitted_displacement_binding_v002.py','87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462'),
 'kernel':(H/'annular_bernstein_nonnegative_source_kernel_v002.py','93b6ad2ca1d6c9051f14aca8b7f95eb9c7a9bd16482bad95115824d6d6cf224b')}
USED={'galaxy.key':'key','source.profile':'pin','source.monotone_source':'pin','custody.seed_sha256':'sha','custody.checkpoint_identity_sha256':'sha','custody.reference_run':'run','route_a.accepted_iteration':'iteration','radial.source_gauss_order':'count','radial.n_columns':'count','mesh.n_phi':'count','mesh.eta_order':'count','radial.outer_edge_kpc':'positive'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(p,s):
 if sha(p)!=s:raise ValueError('Pin mismatch: '+str(p))
def load(p):
 s=importlib.util.spec_from_file_location('body_'+Path(p).stem,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
CONFIG_FORMAT='UNT_ROUTE_B_STAGE_CONFIG_BODY_C2V003'
HEX='0123456789abcdef'
def _is_sha(v):return type(v) is str and len(v)==64 and all(ch in HEX for ch in v)
def _typed(kind,v):
 if kind=='key':return type(v) is str and v!=''
 if kind=='sha':return _is_sha(v)
 if kind=='pin':return type(v) is dict and set(v)=={'path','sha256'} and type(v['path']) is str and _is_sha(v['sha256'])
 if kind=='run':return type(v) is dict and set(v)=={'directory','start_sha256','finish_sha256'} and type(v['directory']) is str and _is_sha(v['start_sha256']) and _is_sha(v['finish_sha256'])
 if kind=='iteration':return type(v) is int and 0<=v<=9999
 if kind=='count':return type(v) is int and v>=1
 if kind=='positive':return type(v) is float and bool(np.isfinite(v)) and v>0
 raise ValueError('Unknown galaxy-config field kind '+kind)
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
 """Shared c2v003 admission of USED, then this stage's typed checks (stages2 _typed). Fail closed; nothing is guessed."""
 galaxy,G,_=admit_config(path,pin,CONFIG_FORMAT,tuple(USED))
 bad=[n+' has the wrong type for '+kind for n,kind in USED.items() if not _typed(kind,G[n])]
 if bad:raise GalaxyConfigRefused('GALAXY_CONFIG_INVALID galaxy=%s: %s'%(galaxy,'; '.join(bad)))
 return G

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
 for k in ('seed','checkpoint-directory','outdir'):p.add_argument('--'+k,required=True)
 for k in ('galaxy-config','galaxy-config-sha256'):p.add_argument('--'+k,required=True)
 UVT=uvt_load();UVT.add_argv(p,'body');a=p.parse_args()
 G=galaxy_config(a.galaxy_config,a.galaxy_config_sha256);GK,NG,NC,NPHI,NETA=G['galaxy.key'],G['radial.source_gauss_order'],G['radial.n_columns'],G['mesh.n_phi'],G['mesh.eta_order']
 REFERENCE=Path(G['custody.reference_run']['directory']);SOURCE=Path(G['source.monotone_source']['path'])
 DATA_PINS={REFERENCE/'start.json':G['custody.reference_run']['start_sha256'],REFERENCE/'finish.json':G['custody.reference_run']['finish_sha256'],SOURCE:G['source.monotone_source']['sha256']}
 out=Path(a.outdir);out.mkdir(exist_ok=False);t0=time.monotonic();completed=[]
 def write(name,value):
  with (out/name).open('x') as f:json.dump(reuse.serial(value),f,allow_nan=False,separators=(',',':'));f.flush()
 try:
  for path,pin in [*PINS.values(),*DATA_PINS.items()]:check(path,pin)
  reuse=load(PINS['reuse'][0]);base=load(PINS['base'][0]);binding=load(PINS['mesh'][0]);kernel=load(PINS['kernel'][0])
  # Reuse only needed existing modules, never invoke the root-search worker.
  mods={}
  for key in ('checkpoint','line','metric','bernstein'):
   path,pin=reuse.PINS[key];check(path,pin);mods[key]=load(path)
  if reuse.SEED_SHA!=G['custody.seed_sha256'] or reuse.IDENTITY!=G['custody.checkpoint_identity_sha256']:raise ValueError('Galaxy config custody differs from the reuse module seed/identity')
  if Path(G['source.profile']['path']).resolve()!=Path(reuse.PROFILE).resolve() or G['source.profile']['sha256']!=reuse.PROFILE_SHA:raise ValueError('Galaxy config source.profile differs from the reviewed reference profile')
  cm=mods['checkpoint'];check(a.seed,reuse.SEED_SHA);seed=json.loads(Path(a.seed).read_text());ni=seed['numerical_inputs']
  cp=Path(a.checkpoint_directory);identity=cm._read(str(cp/'IDENTITY.json'),'identity')
  if identity['identity_sha256']!=reuse.IDENTITY or cm._sha(cm._canonical(identity['identity']))!=reuse.IDENTITY:raise ValueError('Checkpoint identity mismatch')
  caller=cm.decode(identity['identity']['caller']['record']);phys=caller['physical_parameters']
  if caller['seed']['sha256']!=reuse.SEED_SHA:raise ValueError('Checkpoint seed mismatch')
  IT=route_a_final_iteration(cm,cp,reuse.IDENTITY,G['route_a.accepted_iteration'])
  start=cm._read(str(cp/('iteration_%04d/START.json'%IT)),'iteration_start');done=cm._read(str(cp/('iteration_%04d/COMPLETED.json'%IT)),'iteration_completed')
  refstart=json.loads((REFERENCE/'start.json').read_text());finish=json.loads((REFERENCE/'finish.json').read_text());custody=refstart['prepared_custody']
  if start['identity_sha256']!=reuse.IDENTITY or done['identity_sha256']!=reuse.IDENTITY or start['iteration']!=IT or done['iteration']!=IT or done['converged']is not True or done['iteration_start_sha256']!=start['payload_sha256'] or custody['start']!=start['payload_sha256'] or custody['completed']!=done['payload_sha256']:raise ValueError('Accepted CURRENT/reference custody mismatch')
  for k in ('wavevectors','weighted_responses'):
   if custody[k]!=start['prepared_'+k]:raise ValueError('Prepared array reference mismatch')
  prepared={k:cm._get(str(cp),start['prepared_'+k]) for k in ('wavevectors','weighted_responses')}
  uvt=UVT.open_binding(a,'body').bind(ni=ni,phys=phys,caller=caller,galaxy=GK,profile=(reuse.PROFILE,reuse.PROFILE_SHA),identity=reuse.IDENTITY,iteration=IT,start=start,prepared=prepared,reference_start=refstart,reference_finish=finish)
  # Preserve exact old gas blob provenance; do not replace it with a new quadrature of old density.
  oldrefs={k:start[k] for k in ('gas_fourier_J','fixed_source_fourier_J','current_source_fourier_J')}
  for record in oldrefs.values():check(cp/record['blob'],record['file_sha256'])
  profile=json.loads(SOURCE.read_text())['source_record'];edges=np.asarray(profile['s_edges_kpc2']);kpc=ni['kpc_m']
  old=json.loads(reuse.PROFILE.read_text())['galaxies'][GK]['HI_plus_He'];check(reuse.PROFILE,reuse.PROFILE_SHA)
  J=radial_truncation(old['s_edges_kpc2'],G['radial.outer_edge_kpc'])
  FULL=J==len(old['s_edges_kpc2'])-1
  if (list(edges),profile['annular_means_Msun_pc2'])!=((old['s_edges_kpc2'],old['annular_means_Msun_pc2']) if FULL else (old['s_edges_kpc2'][:J+1],old['annular_means_Msun_pc2'][:J])):raise ValueError('New profile changed independent annular means/domain' if FULL else 'N2 truncated domain requires the monotone source record in the prefix form edges[:J+1], means[:J] (CHECK D3)')
  if refstart['source_custody']['full_radial_domain_m'][1]!=UVT.ngc_radial_domain_upper(float(np.sqrt(old['s_edges_kpc2'][J]))*kpc,ni,caller):raise ValueError('Reference radial domain edge differs from the N2 domain edge')
  if ni['source_gauss_order']!=NG:raise ValueError('Actual GL%d radial roster required'%NG)
  gx,gw=np.polynomial.legendre.leggauss(NG);R=[];wr=[]
  for lo,hi in zip(edges[:J],edges[1:J+1]):
   for x,w in zip(gx,gw):R.append(float(np.sqrt((lo+hi)/2+(hi-lo)*x/2)*kpc));wr.append(float((hi-lo)*w*kpc*kpc/4))
  # Reference roster rule (reference:74-77,85), same kernel/profile/query: drop nodes whose reference Sigma is exactly 0.
  ref_edges=[float(x) for x in old['s_edges_kpc2']];ref_means=[float(x) for x in old['annular_means_Msun_pc2']];ref_controls=[float(x) for x in old['boundary_controls_Msun_pc2']];ref_unit=ni['solar_mass_kg']/(kpc/1000)**2;keep=[]
  for r in R:
   pr=mods['bernstein'].annular_bernstein_sigma(s_edges=ref_edges,annular_means=ref_means,boundary_controls=ref_controls,s_query=[float((r/kpc)**2)])
   if not pr['ok']:raise ValueError('Independent HI source-domain failure: '+str(pr['failures']))
   keep.append(float(pr['sigma'][0])*ref_unit!=0)
  R=[r for r,k in zip(R,keep) if k];wr=[x for x,k in zip(wr,keep) if k]
  REGISTERED_NC=NC
  if len(R)!=REGISTERED_NC:raise ValueError('Registered full radial count mismatch')
  R,wr=UVT.ngc_filter_radial_nodes(R,wr,ni,caller)
  NC=UVT.ngc_effective_n_columns(REGISTERED_NC,ni,caller,(reuse.PROFILE,reuse.PROFILE_SHA),R)
  if R!=refstart['radii_m'] or len(R)!=NC or finish['failures'] or len(finish['completed'])!=NC:raise ValueError('Full exact saved %d-radius roster required'%NC)
  eta,we=np.polynomial.legendre.leggauss(NETA);sigmaunit=ni['solar_mass_kg']/(kpc/1000)**2
  ans=kernel.annular_bernstein_sigma(s_edges=[float(x) for x in edges],annular_means=profile['annular_means_Msun_pc2'],boundary_controls=profile['boundary_controls_Msun_pc2'],s_query=[(r/kpc)**2 for r in R])
  if not ans['ok']:raise ValueError(str(ans['failures']))
  sigmas=np.asarray(ans['sigma'])*sigmaunit
  pins={str(path):pin for path,pin in PINS.values()};pins.update({str(path):pin for path,pin in DATA_PINS.items()});pins.update({str(path):pin for path,pin in reuse.PINS.values() if path in [reuse.PINS[k][0] for k in mods]})
  write('start.json',dict(worker_sha256=sha(__file__),input_pins=pins,seed_sha256=reuse.SEED_SHA,prepared_custody=custody,old_source_references=oldrefs,checkpoint_directory=str(cp.resolve()),shape=[NC,NPHI,NETA],status='OLD_FIELD_NEW_NORMALIZED_SOURCE',action_successor='Not imported or accepted by this assembler',**uvt.record()))
  def boundary(pos):
   if uvt.enabled:return uvt.jets(pos)
   n=len(pos);return dict(boundary_fields=np.zeros((n,10,1)),boundary_gradient=np.zeros((n,10,1,3)),boundary_hessian=np.zeros((n,10,1,3,3)))
  results=[]
  with (out/'progress.jsonl').open('x') as log:
   for i,item in enumerate(finish['completed']):
    if item['index']!=i or item['R_m']!=R[i]:raise ValueError('Reference order mismatch')
    check(item['path'],item['sha256']);record=json.loads(Path(item['path']).read_text())
    result=base.evaluate_saved_radius(reference_record=record,prepared=prepared,prepared_custody=custody,eta_nodes=eta,eta_weights=we,new_surface_kg_m2=float(sigmas[i]),c_m_s=phys['c_m_s'],Cbar=phys['Cbar'],mubar=phys['mubar'],line_module=mods['line'],metric_module=mods['metric'],boundary_jet_at_positions=boundary,accepted_module_pins=pins,reality_atol=ni['reality_atol'],reality_rtol=ni['reality_rtol'],n_phi=NPHI)
    name='radius_%04d.json'%i;write(name,result);completed.append(dict(index=i,path=str(out/name),sha256=sha(out/name),reference_sha256=item['sha256']));results.append(result)
    log.write(json.dumps(dict(index=i,status='SAVED',elapsed_seconds=time.monotonic()-t0))+'\n');log.flush()
  mesh=binding.make_mesh(radial_nodes_m=R,radial_RdR_weights_m2=wr,radial_domain_m=refstart['source_custody']['full_radial_domain_m'],roots_m=[r['roots_m'] for r in results],eta_nodes=eta,eta_weights=we,n_phi=NPHI)
  arrays={k:mesh[k] for k in ('R','phi','z','volume_weights_m3','physical_positions_m')}
  arrays.update(radial_nodes_m=np.asarray(R),radial_RdR_weights_m2=np.asarray(wr),eta_nodes=eta,eta_weights=we,roots_m=np.asarray([r['roots_m'] for r in results]),Sigma_kg_m2=sigmas)
  for target,key in [('rho0','rho0_kg_m3'),('P0','P0_Pa'),('K0','K0_SI'),('Omega','Omega_per_s'),('Phi0','Phi0_m2_s2')]:
   values=np.asarray([[row[key] for row in r['rows']] for r in results]);arrays[target]=np.broadcast_to(values[:,None,:],(NC,NPHI,NETA)).copy()
  for key in ('angular_forcing_dPhi_m2_s2','full_fields_real','full_fields_imag'):
   values=np.asarray([[row[key] for row in r['rows']] for r in results]);arrays[key]=np.swapaxes(values,1,2)
  arrays['base_residual_r0']=np.stack((mesh['partial_R'](arrays['Phi0'])+mesh['partial_R'](arrays['P0'])/arrays['rho0']-mesh['R']*arrays['Omega']**2,np.zeros((NC,NPHI,NETA)),mesh['partial_z'](arrays['Phi0'])+mesh['partial_z'](arrays['P0'])/arrays['rho0']),axis=-1)
  # Leading source convention of the adopted displacement equation, with quadrature exactly once.
  arrays['base_integrated_source_J']=np.zeros((NC,NPHI,NETA,10,1));arrays['base_integrated_source_J'][...,0,0]=-phys['c_m_s']**2*arrays['rho0']*arrays['volume_weights_m3']
  for key,value in arrays.items():
   if not np.all(np.isfinite(value)):raise ValueError('Nonfinite assembled '+key)
  np.savez(out/'body_arrays.npz',**arrays)
  write('finish.json',dict(status='EVALUATED_REFERENCE_ARRAYS_NOT_FLOW_SOLUTION',completed=completed,array_file=str(out/'body_arrays.npz'),array_sha256=sha(out/'body_arrays.npz'),arrays={k:dict(shape=list(v.shape),dtype=str(v.dtype)) for k,v in arrays.items()},elapsed_seconds=time.monotonic()-t0,accepted_for_calibration=False,source_self_consistent=False,source_offset=dict(equation='h_total=h_G4+G(f_base_new-f_G4)+G(-c^2 delta_rho)',old_gas=oldrefs['gas_fourier_J'],fixed_stars_cancel_only_if_identical=True,new_base='Fourier transform physical_positions_m and base_integrated_source_J with exp(-ik.x); no additional quadrature factor',implementation='Offset not evaluated here. Before action solve add it once to complete base field, recompute Phi0/angular split and same-discrete r0. Offset may contain m0 and must not be put in angular-only forcing.',source_scope='Leading Euclidean rest-energy density convention; all 10 response fields retained by subsequent full response. Current fields remain old G4.'),limitations=['Failed native coefficient mixing retained','Natural-cubic/GL8 finite discretization; no continuum error bound','No new roots, source equilibration, boundary solve or final action import'],**uvt.record(final=True)))
 except Exception as exc:
  with (out/'failure.json').open('x') as f:json.dump(dict(type=type(exc).__name__,message=str(exc),completed=completed,elapsed_seconds=time.monotonic()-t0),f)
  raise

if __name__=='__main__':main()
