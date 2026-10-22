"""INERT root-only reference/residual binding to the accepted route-A final-iteration CURRENT field (galaxy config).
No Fourier-source reconstruction, inversion, physical averaging of final response,
new calibration data or self-consistent gas solution. Per-radius results durable.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
import numpy as np
# UVT_C2V002 (Claude2 tail_scheme_impl_c2/route_b): successor of ddo_homotopy_reference_root_worker_v001_gal_c2v005.py (sha256 cdf155e8161a89fd78518bbe048fae2b8114a5fb04b0fb770c30a8502308eb7f); supersedes the C2V001 reference successor
#   (which also rewrote the start.json 'boundary' text when the tail is enabled; an empty domain must keep the reviewed record).
# uvt change (TAIL_SCHEME_DESIGN_V002 sec 1.1/1.3/2.2/3.6 with V002_R1; stage kind reference): the UV-tail lapse enters only
#   through the reviewed additive boundary slots, via the pinned shared binding uvt_route_b_binding_c2v001.py. Required argv
#   --uv-tail-config/--uv-tail-config-sha256 (certificates are config fields, verified from bytes at build; R1 IA6).
#   enabled=false: the binding returns the reviewed zero literals and adds no record; the reviewed body runs unchanged.
#   enabled=true with an empty domain (O inside C): the same zero literals (no addition anywhere), plus the uv_tail record.
#   slots: boundary closure L261-263 (tail jets, order 2); bind after prepared L230-231 (route-A manifest state).
# GAL_C2V005 (Claude2 stage_successor_gal_c2v005): successor of ddo_homotopy_reference_root_worker_v001_gal_c2v004.py (sha256 dbdbfba1d693452a62076a7fc1f4d6cb348fb135d9d15a7f060f2908ff3158a7).
# c2v005 change (ROOT_DECISIONS_NGC3198 V003 addendum 5bef6552b92b0939... A13 deciding work), the shared admission only:
#   schema V005 pin; PER_CALL admitted on the DDO154 per-call geometry fields (PER_CALL_GEOMETRY and the schema
#   per_call_geometry declaration); a config without such a field is admitted exactly as c2v004. No other change.
# GAL_C2V004 (Claude2 ngc_f10_c2/route_b_v006): successor of ddo_homotopy_reference_root_worker_v001_gal_c2v003.py (sha256 406dda4412ba1a87624908689a4a804ff7e07a140574e6e823a254d544dd66f1).
# c2v004 changes (ROOT_DECISIONS_NGC3198 V002 addendum 4070146dbd85c3cb...):
#   admission: shared c2v004 admit_config on GALAXY_CONFIG_SCHEMA_V004 (A4 values; A2 member entries, CHECK D2);
#       a config without member is admitted exactly as c2v003
#   no other change
# GAL_C2V003 (Claude2 ngc_route_impl_c2/binding): successor of ddo_homotopy_reference_root_worker_v001_gal_c2v001.py (sha256 67580ebe4acef38b9864f9059d0262ecce84552eaff033678bba6f2440aa0416).
# c2v003 changes (ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001 06cae881fe075b42...):
#   admission: shared c2v003 admit_config on GALAXY_CONFIG_SCHEMA_V003 (N5; supersedes both V002 files, stages2 CHECK D1/D6)
#   route A: the c2v002 strict reader route_a_final_iteration verbatim (stages2 CHECK D2)
#   N2: radial.outer_edge_kpc consumed; the route-A roster digest is still checked on the FULL roster; route-B radii are
#       the roster radii inside sqrt(s_edges[J])*kpc and the domain is [sqrt(s_edges[0]), sqrt(s_edges[J])]*kpc
#       (J = radial_truncation; DDO154 J = last edge: radii and domain are the old values bitwise)
# GAL_C2V001 (Claude2 ngc_route_construction_c2/stages2): galaxy-config successor of reviewed
# ddo_homotopy_reference_root_worker_v001.py (sha acda989d375925bf9a8163d8d8a3a22c3f183b6b253c8137312bccc0cefbbe36).
# Only DDO154 literals became fields of --galaxy-config (schema UNT_ROUTE_B_GALAXY_CONFIG_SCHEMA_V002,
# format UNT_ROUTE_B_GALAXY_CONFIG_INSTANCE_STAGES2_C2V001); with the DDO154 config each equals the old literal.
# The route-A iteration is the config value AND the checkpoint records' single converged final iteration.
# The reviewed stage directory is absolute so every PINS path is unchanged by relocation. Every equation,
# tolerance, guard, output file and output key of the base is kept. A field holding NONE_IN_REVIEWED_CODE,
# NOT_APPLICABLE or DERIVED_FROM_BYTES_CONDITIONAL is refused before any output, never guessed.
# Also: the reference module is the n_phi successor owned_axisymmetric_homotopy_reference_v003_gal_c2v001.py (mesh.n_phi passed);
# SEED_SHA/IDENTITY are no longer module globals (config custody.*), so a stale driver patch fails closed.

H=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit');HC=H.parent/'coefficient_method';C=H.parent.parent/'CODEX1'
PINS={
 'checkpoint':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py'),'069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114'),
 'line':(H/'owned_fixed_xy_fourier_line_v002.py','3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18'),
 'metric':(HC/'owned_fourier_physical_metric_evaluator_v002.py','8f01bd5b352a5ec5f74f6c19ed8ad4295c55ff80ba895dac93628f62bace73a4'),
 'column':(HC/'owned_leading_homotopy_column_v001.py','022ed7f1e273e9d058ff1641b0120534ee8b0a59ff43922ced750f6fcc16f137'),
 'quadrature':(H/'general_column_mass_quadrature_v002.py','a67b526b378390fa91ccd030efb9ff1c868d379986ff3321335780c485ef0d04'),
 'bernstein':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/annular_source_kernel_0403/annular_bernstein_source_kernel_v001.py'),'2544d22f46dbf225139f92f6a566f814e5857f265c43d88565c6a4d3894a759e')}
PROFILE=C/'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json'
PROFILE_SHA='f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'
USED={'galaxy.key':'key','source.profile':'pin','custody.seed_sha256':'sha','custody.checkpoint_identity_sha256':'sha','route_a.accepted_iteration':'iteration','mesh.n_phi':'count','radial.outer_edge_kpc':'positive'}
def check(p,s):
    if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=s:raise ValueError('Pin mismatch: '+str(p))
CONFIG_FORMAT='UNT_ROUTE_B_STAGE_CONFIG_REFERENCE_C2V003'
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

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):
    s=importlib.util.spec_from_file_location('homotopy_'+Path(p).stem,p)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def serial(v):
    if isinstance(v,np.ndarray):return serial(v.tolist())
    if isinstance(v,np.generic):return serial(v.item())
    if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [serial(x) for x in v]
    return v

def write(p,v):
    with p.open('x') as f:json.dump(serial(v),f,allow_nan=False,separators=(',',':'));f.flush()

# UVT_C2V003 F4 (Claude2 tail_scheme_impl_c2/driver_r4): successor of ddo_homotopy_reference_root_worker_v001_gal_c2v005_uvt_c2v002.py (sha256 6775599ed3c3ee4e32517246a323f692cbd47257629eb5425c1e15742057f9cd): CHECK_V001 F4 -- the
#   start.json 'boundary' text is the reviewed one unless the tail state is non-empty (then the binding's boundary_text());
#   an empty domain keeps the reviewed record byte for byte; nothing else changes.
# ---- uvt_c2v001 shared UV-tail binding loader (tail_scheme_impl_c2/route_b): identical text in every gal_c2v005_uvt_c2v001 stage ----
UVT_BINDING=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py'),'1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329')
def uvt_load():
 """The pinned shared UV-tail binding (bytes checked before and after exec; inert at import)."""
 path,pin=UVT_BINDING
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('UV_TAIL_PIN_MISMATCH '+str(path))
 s=importlib.util.spec_from_file_location('uvt_route_b_binding_c2v001',str(path));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('UV_TAIL_PIN_CHANGED_AFTER_IMPORT '+str(path))
 return m
def uvt_boundary_text(uvt):
 """CHECK_V001 F4: the reviewed start.json 'boundary' text unless the tail state is non-empty (then the binding's text)."""
 if not uvt.enabled or uvt.state is None or uvt.state.empty:return 'Actual zero imposed perturbations'
 return uvt.boundary_text()
# ---- end of uvt block ----
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('seed','checkpoint-directory','reference-module','reference-sha256','outdir'):
        p.add_argument('--'+key,required=True)
    for key in ('galaxy-config','galaxy-config-sha256'):p.add_argument('--'+key,required=True)
    UVT=uvt_load();UVT.add_argv(p,'reference');a=p.parse_args()
    G=galaxy_config(a.galaxy_config,a.galaxy_config_sha256);SEED_SHA,IDENTITY,GK,NPHI=G['custody.seed_sha256'],G['custody.checkpoint_identity_sha256'],G['galaxy.key'],G['mesh.n_phi']
    if Path(G['source.profile']['path']).resolve()!=PROFILE.resolve() or G['source.profile']['sha256']!=PROFILE_SHA:raise ValueError('Galaxy config source.profile differs from the reviewed reference profile')
    out=Path(a.outdir);out.mkdir(exist_ok=False);t0=time.monotonic()
    if a.reference_sha256!='1b00add9fb6b7ee563fe4ab86e971345d45123a6a10beccebae4b93b7558383b':raise ValueError('Only the reviewed common-interior V003 reference (n_phi successor gal_c2v001) is bound')
    try:
        pins={str(path.resolve()):pin for path,pin in PINS.values()}
        pins.update({str(Path(a.seed).resolve()):SEED_SHA,str(PROFILE):PROFILE_SHA,str(Path(a.reference_module).resolve()):a.reference_sha256})
        for path,pin in pins.items():
            if sha(path)!=pin:raise ValueError('Actual code/source pin mismatch: '+path)
        mods={key:load(path) for key,(path,_) in PINS.items()};ref=load(a.reference_module);cm=mods['checkpoint']
        seed=json.loads(Path(a.seed).read_text());ni=seed['numerical_inputs']
        identity=cm._read(str(Path(a.checkpoint_directory)/'IDENTITY.json'),'identity')
        if identity['identity_sha256']!=IDENTITY or cm._sha(cm._canonical(identity['identity']))!=IDENTITY:
            raise ValueError('Actual accepted checkpoint identity mismatch')
        caller=cm.decode(identity['identity']['caller']['record']);phys=caller['physical_parameters']
        if caller['seed']['sha256']!=SEED_SHA:raise ValueError('Checkpoint seed mismatch')
        IT=route_a_final_iteration(cm,a.checkpoint_directory,IDENTITY,G['route_a.accepted_iteration'])
        folder=Path(a.checkpoint_directory)/('iteration_%04d'%IT)
        start=cm._read(str(folder/'START.json'),'iteration_start');done=cm._read(str(folder/'COMPLETED.json'),'iteration_completed')
        if start['identity_sha256']!=IDENTITY or start['iteration']!=IT or done['identity_sha256']!=IDENTITY or done['iteration']!=IT or done['iteration_start_sha256']!=start['payload_sha256'] or done['converged']is not True:
            raise ValueError('Actual iteration%d convergence custody mismatch'%IT)
        prepared={'wavevectors':cm._get(a.checkpoint_directory,start['prepared_wavevectors']),
                  'weighted_responses':cm._get(a.checkpoint_directory,start['prepared_weighted_responses'])}
        uvt=UVT.open_binding(a,'reference').bind(ni=ni,phys=phys,galaxy=GK,profile=(PROFILE,PROFILE_SHA),identity=IDENTITY,iteration=IT,start=start,prepared=prepared)
        # Independent source profile, identical original GL/R² roster construction.
        gas=json.loads(PROFILE.read_text())['galaxies'][GK]['HI_plus_He']
        edges=[float(x) for x in gas['s_edges_kpc2']];means=[float(x) for x in gas['annular_means_Msun_pc2']]
        controls=[float(x) for x in gas['boundary_controls_Msun_pc2']]
        kpc=ni['kpc_m'];sigmaunit=ni['solar_mass_kg']/(kpc/1000)**2
        hi=dict(sigma0_m_s=11000.,gamma=5/3,search_step_m=ni['hi_search_step_kpc']*kpc,
            search_limit_m=ni['hi_search_limit_kpc']*kpc,root_tolerance_m=ni['hi_root_tolerance_kpc']*kpc,
            log_lapse_tolerance=ni['hi_log_lapse_tolerance'],max_metric_calls=ni['hi_max_metric_calls'],panels_per_side=ni['hi_panels_per_side'])
        def profile(R):
            ans=mods['bernstein'].annular_bernstein_sigma(s_edges=edges,annular_means=means,boundary_controls=controls,s_query=[float((R/kpc)**2)])
            if not ans['ok']:raise ValueError('Independent HI source-domain failure: '+str(ans['failures']))
            return {'Sigma_kg_m2':float(ans['sigma'][0])*sigmaunit,'hi_options':dict(hi)}
        gx,gw=np.polynomial.legendre.leggauss(ni['source_gauss_order'])
        gauss=[(float(x),float(w)) for x,w in zip(gx,gw)]
        phis=[2*math.pi*i/ni['source_azimuth_count'] for i in range(ni['source_azimuth_count'])]
        dphi=2*math.pi/ni['source_azimuth_count'];roster=[]
        for lo,up in zip(edges,edges[1:]):
            for x,w in gauss:
                s=(lo+up)/2+(up-lo)*x/2;R=math.sqrt(s)*kpc;dR=(up-lo)*w*kpc*kpc/(4*R);pr=profile(R)
                if pr['Sigma_kg_m2']==0:continue
                for phi in phis:roster.append(dict(R_m=R,phi=phi,radial_weight_m=dR,azimuth_weight_rad=dphi,**pr))
        digest=cm.digest(roster)
        if digest!=identity['identity']['inputs_sha256']['gas_columns'] or len(roster)!=start['column_count']:
            raise ValueError('Independent profile does not reproduce original actual roster')
        J=radial_truncation(edges,G['radial.outer_edge_kpc'])
        radii=[r for r in dict.fromkeys(col['R_m'] for col in roster) if r<math.sqrt(edges[J])*kpc];domain=[math.sqrt(edges[0])*kpc,math.sqrt(edges[J])*kpc]
        step=.005*kpc
        if ni['pressure_step_kpc']!=.005:raise ValueError('Expected actual .005kpc radial stencil')
        hi_ref={k:v for k,v in hi.items() if k not in ('sigma0_m_s','gamma')}
        def boundary(pos):
            if uvt.enabled:return uvt.jets(pos)
            n=len(pos);return {'boundary_fields':np.zeros((n,10,1)),
                'boundary_gradient':np.zeros((n,10,1,3)),'boundary_hessian':np.zeros((n,10,1,3,3))}
        custody={'identity':IDENTITY,'iteration':IT,'start':start['payload_sha256'],'completed':done['payload_sha256'],
                 'wavevectors':start['prepared_wavevectors'],'weighted_responses':start['prepared_weighted_responses'],
                 'meaning':'Actual accepted CURRENT field; reconstructed successor unused'}
        source={'profile_path':str(PROFILE),'sha256':PROFILE_SHA,'roster_digest':digest,'full_radial_domain_m':domain}
        if J<len(edges)-1:source['radial_truncation_N2']={'outer_edge_kpc':G['radial.outer_edge_kpc'],'edge_index':J,'route_a_roster_radii':len(dict.fromkeys(col['R_m'] for col in roster)),'route_b_radii':len(radii)}
        write(out/'start.json',{'input_pins':pins,'worker_sha256':sha(__file__),'prepared_custody':custody,
            'source_custody':source,'radii_m':radii,'radial_step_m':step,'boundary':uvt_boundary_text(uvt),
            'scope':'Homotopy reference/residual evaluation, no equilibrium or predicted observed velocities',**uvt.record()})
        completed=[];failures=[]
        with (out/'progress.jsonl').open('x') as log:
            for i,R in enumerate(radii):
                event={'radius_index':i,'radius_count':len(radii),'R_m':R,'stage':'radius_started','elapsed_seconds':time.monotonic()-t0}
                log.write(json.dumps(event)+'\n');log.flush()
                try:
                    result=ref.evaluate_radius(prepared=prepared,R_m=R,radial_step_m=step,
                        z_positions_m='center_common_interior',radial_domain_m=domain,
                        profile_at_radius=profile,hi_options=hi_ref,c_m_s=phys['c_m_s'],Cbar=phys['Cbar'],mubar=phys['mubar'],
                        boundary_jet_at_positions=boundary,line_module=mods['line'],metric_module=mods['metric'],
                        column_module=mods['column'],quadrature_module=mods['quadrature'],reality_atol=ni['reality_atol'],reality_rtol=ni['reality_rtol'],
                        prepared_custody=custody,source_roster_custody=source,accepted_module_pins=pins,n_phi=NPHI)
                    path=out/('radius_%04d.json'%i);write(path,result)
                    completed.append({'index':i,'R_m':R,'path':str(path),'sha256':sha(path)})
                    event['stage']='radius_completed'
                except ValueError as exc:
                    failure={'index':i,'R_m':R,'type':type(exc).__name__,'message':str(exc),'scope':'No extrapolation, fabricated height or replaced source'}
                    write(out/('radius_%04d_failure.json'%i),failure);failures.append(failure);event['stage']='radius_failed';event['failure']=failure
                event['elapsed_seconds']=time.monotonic()-t0;log.write(json.dumps(event)+'\n');log.flush()
        write(out/'finish.json',{'status':'RETURNED_REFERENCE_RADIUS_RECORDS','completed':completed,'failures':failures,
            'accepted_for_calibration':False,'elapsed_seconds':time.monotonic()-t0,
            'scope':'Per-radius completed records retained. Neither forcing feedback nor a corrected stationary flow/prediction is asserted.',**uvt.record(final=True)})
    except Exception as exc:
        write(out/'failure.json',{'type':type(exc).__name__,'message':str(exc),'elapsed_seconds':time.monotonic()-t0});raise

if __name__=='__main__':main()
