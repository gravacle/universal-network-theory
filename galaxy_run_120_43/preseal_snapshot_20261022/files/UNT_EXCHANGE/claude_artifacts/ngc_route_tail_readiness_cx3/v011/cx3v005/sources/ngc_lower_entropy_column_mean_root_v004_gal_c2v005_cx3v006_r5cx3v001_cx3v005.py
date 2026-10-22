"""Root-only conditional12 column-mean output; no observations or scores.
Frozen positive lower-entropy REFRESHED lagged rotation; still not converged full flow.
"""
# GAL_C2V005 (Claude2 stage_successor_gal_c2v005): successor of ddo12_lower_entropy_column_mean_root_v004_gal_c2v004.py (sha256 11d6f8b8f54b677ae6a01a044b08db33d425a26a558bd4726d14d647217c9877).
# c2v005 change (ROOT_DECISIONS_NGC3198 V003 addendum 5bef6552b92b0939... A13 deciding work), the shared admission only:
#   schema V005 pin; PER_CALL admitted on the DDO154 per-call geometry fields (PER_CALL_GEOMETRY and the schema
#   per_call_geometry declaration); a config without such a field is admitted exactly as c2v004. No other change.
# GAL_C2V004 (Claude2 ngc_f10_c2/route_b_v006): successor of ddo12_lower_entropy_column_mean_root_v004_gal_c2v003.py (sha256 3d076998a09c2c72da279ab86fcf6fc5f7002dde906ba4b3b12acc4d1ba0de2e).
# c2v004 changes (ROOT_DECISIONS_NGC3198 V002 addendum 4070146dbd85c3cb...):
#   admission: shared c2v004 admit_config on GALAXY_CONFIG_SCHEMA_V004 (A4 values; A2 member entries, CHECK D2);
#       a config without member is admitted exactly as c2v003
#   A4/N1: binding invalid_row_rule -> rows below the innermost radial node are emitted valid=false
#       QUERY_INSIDE_INNERMOST_NODE (speed null) and the call stays valid; without the rule (DDO154) the c2v003
#       code path runs unchanged. NGC3198 observation.binding and the tracer/observation rule are decided in V004 (A4).
# GAL_C2V003 (Claude2 ngc_route_impl_c2/binding): successor of ddo12_lower_entropy_column_mean_root_v004_gal_c2v002.py (sha256 af74c7815e5ef749585e0e00cfbddfc1e43f9a58a67e971e4c510c8ade4a4544).
# c2v003 changes (ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001 06cae881fe075b42...):
#   admission: shared c2v003 admit_config on GALAXY_CONFIG_SCHEMA_V003 (N5)
#   no other change (NGC3198: observation.binding and the tracer/observation rule texts
#       are NONE in V003, so NGC3198 is refused at admission)
import argparse,hashlib,importlib.util,json,math,traceback
from pathlib import Path
import numpy as np
# Galaxy-config successor gal_c2v002 (Claude2 lane ngc_route_construction_c2/v004_fix) of
# helpers/coefficient_method/ddo12_lower_entropy_column_mean_root_v004.py
# (sha256 12504c4b86c31e20d0e019868c406f22c35a568e3ad25ee39a9db8ddabfda3c2); successor of gal_c2v001 (f14ab80d...).
# Only DDO154 literals became galaxy-config fields (schema GALAXY_CONFIG_SCHEMA_V002):
#   PINS                     -> custody.column_mean_input_pins (binding entry == observation.binding)
#   72                       -> radial.n_columns
#   16                       -> mesh.n_phi
#   32                       -> column.n_z
#   'ddo_free_surface_rotation_root_v005.py' (the rotation producer file at base line 27 / gal_c2v001 line 111)
#                            -> config producer_pins.rotation_worker {path, sha256}, per call (CHECK_V001 B1).
#      The base verified that the rotation run's worker_sha256 is the sha of the FIXED reviewed file
#      helpers/coefficient_method/ddo_free_surface_rotation_root_v005.py, so it could not admit a run of a
#      rotation successor. The producer file is now named by the call; its DDO value is exactly that file
#      (sha256 1b42990556ee34d30a7a12eb5b5605aa1e43aa8322e03d73bbab86e5c38497b7). Admission verifies the named
#      file's bytes; the run check verifies rs['worker_sha256'] == that sha and the file's bytes, as before.
# c2v002 also uses the shared status-whitelist admission admit_config (CHECK_V001 D1).
# Every equation, tolerance, guard, output key and the --outdir flag are unchanged; the only
# added flag is --galaxy-config PATH SHA256. Fields this stage consumes that are not admitted refuse (fail closed).
# The docstring above is kept byte-identical (it is the argparse description).
# route_a.accepted_iteration: the reviewed v004 bytes contain no route-A iteration literal;
# the iteration reaches this stage only through the pinned rotation/columns run records.
H=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit')
ADAPTER_SHA='6790e28eb6631c0144f2efda26071a5933f47f7bda7d0c15d3b81e3581cc548c'
OBS_SHA='8e30897e875a619b132ba07e93459333cfd9302bbe2fc98d9a2ff0a2ec6d815d'
CONFIG_FORMAT='UNT_ROUTE_B_STAGE_CONFIG_COLMEAN_C2V003'
CONSUMED=('galaxy.key','custody.column_mean_input_pins','observation.binding','radial.n_columns','mesh.n_phi','column.n_z',
 'observation.query_rows','observation.physical_inclination_rad','observation.released_inclination_rad',
 'observation.HI_to_HI_plus_He_mass_ratio','observation.tracer_rule_and_observation_rule','output.n_queries')
PRODUCER_PINS=('rotation_worker',)
def checked(path,pin):
 p=Path(path);raw=p.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=pin:raise ValueError('Pin mismatch: '+str(p))
 return raw
def module(name,path,pin):
 checked(path,pin);s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
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
# ---- end of shared blocks ----
def _posint(v,name):
 if isinstance(v,bool) or not isinstance(v,int) or v<=0:raise GalaxyConfigRefused('Galaxy config '+name+' must be a positive int')
 return v
def _producer_refusal(pp):
 """producer_pins = {rotation_worker: {path, sha256}}: the script that produced the rotation run (per call)."""
 if type(pp) is not dict or set(pp)!=set(PRODUCER_PINS):return 'must be exactly {rotation_worker: {path, sha256}}'
 rw=pp['rotation_worker']
 if _sentinel(rw):return 'rotation_worker '+_sentinel(rw)
 if type(rw) is not dict or set(rw)!={'path','sha256'} or type(rw['path']) is not str or not _hex64(rw['sha256']):return 'rotation_worker must be {path, sha256}'
 p=Path(rw['path'])
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=rw['sha256']:return 'rotation_worker file bytes differ from its sha256: '+str(p)
 return None
def galaxy_config(spec):
 """Read and refuse-check the galaxy config; returns (PINS,n_columns,n_phi,n_z,observation fields,rotation producer)."""
 path,sha=spec
 galaxy,fv,cfg=admit_config(path,sha,CONFIG_FORMAT,CONSUMED,{'producer_pins':_producer_refusal})
 key=fv['galaxy.key']
 if not isinstance(key,str) or not key:raise GalaxyConfigRefused('Galaxy config galaxy.key must be a nonempty string')
 pins=fv['custody.column_mean_input_pins']
 if not isinstance(pins,list) or len(pins)!=5 or any(not isinstance(x,list) or len(x)!=2 or not isinstance(x[0],str) or not _hex64(x[1]) for x in pins):raise GalaxyConfigRefused('custody.column_mean_input_pins must be 5 ordered [path,sha256] pairs (binding, rotation start, rotation finish, columns start, columns finish)')
 if len({x[0] for x in pins})!=5:raise GalaxyConfigRefused('custody.column_mean_input_pins paths must be distinct')
 b=fv['observation.binding']
 if not isinstance(b,dict) or [b.get('path'),b.get('sha256')]!=pins[0]:raise GalaxyConfigRefused('observation.binding must equal the first column-mean input pin')
 nc=_posint(fv['radial.n_columns'],'radial.n_columns');nphi=_posint(fv['mesh.n_phi'],'mesh.n_phi');nz=_posint(fv['column.n_z'],'column.n_z')
 rows=fv['observation.query_rows'];nq=_posint(fv['output.n_queries'],'output.n_queries')
 if not isinstance(rows,list) or len(rows)!=nq or any(not isinstance(q,dict) or set(q)!={'id','radius_m'} for q in rows):raise GalaxyConfigRefused('observation.query_rows must be output.n_queries {id,radius_m} rows')
 rules=fv['observation.tracer_rule_and_observation_rule']
 if not isinstance(rules,dict) or set(rules)!={'tracer_rule','observation_rule'}:raise GalaxyConfigRefused('observation.tracer_rule_and_observation_rule must hold tracer_rule and observation_rule')
 obsv={'query_rows':rows,'physical_inclination_rad':fv['observation.physical_inclination_rad'],'released_inclination_rad':fv['observation.released_inclination_rad'],
  'HI_to_HI_plus_He_mass_ratio':fv['observation.HI_to_HI_plus_He_mass_ratio'],'tracer_rule':rules['tracer_rule'],'observation_rule':rules['observation_rule']}
 return {p:s for p,s in pins},nc,nphi,nz,obsv,cfg['producer_pins']['rotation_worker']
def check_binding(binding,obsv):
 """The pinned binding stays the value source; the config must agree with it exactly."""
 for k,v in obsv.items():
  got=[{'id':q.get('id'),'radius_m':q.get('radius_m')} for q in binding.get(k,[])] if k=='query_rows' else binding.get(k)
  if got!=v:raise ValueError('Galaxy config/binding mismatch: '+k)
# ---- c2v004 N1 invalid-row handling (ROOT_DECISIONS_NGC3198 V002 addendum A4) ----
INVALID_ROW_REASON='QUERY_INSIDE_INNERMOST_NODE'
def query_partition(binding,R):
 """Retain all queries in final output; evaluate only supported rows before the certified cut."""
 rows=binding['query_rows'];cut=binding.get('_ngc_outer_cut_radius_m')
 rule=binding.get('invalid_row_rule')
 if rule is not None and (type(rule) is not dict or rule.get('reason')!=INVALID_ROW_REASON):raise ValueError('Unsupported binding invalid_row_rule: '+repr(rule))
 if rule is None and cut is None:return rows,None
 valid=[];invalid=[]
 for q in rows:
  reason=OUTER_INVALID_ROW_REASON if cut is not None and q['radius_m']>=cut else INVALID_ROW_REASON if rule is not None and q['radius_m']<R[0] else None
  if reason is not None:invalid.append(dict(q,_reason=reason))
  elif q['radius_m']>R[-1]:
   if cut is None:raise ValueError('NGC_QUERY_OUTSIDE_UNCUT_INTERPOLATION_SUPPORT: '+q['id'])
   invalid.append(dict(q,_reason=SUPPORT_GAP_ROW_REASON))
  else:valid.append(q)
 if not valid:raise ValueError('No query row has a supporting radial node')
 return valid,invalid

def merge_invalid_rows(packet,binding,invalid,R):
 """Restore original roster/order, null speed for each explicit INVALID; no extrapolation."""
 got={r['id']:r for r in packet['rows']};bad={q['id']:q['_reason'] for q in invalid};rows=[]
 expected={q['id'] for q in binding['query_rows']}-set(bad)
 if len(got)!=len(packet['rows']) or set(got)!=expected:raise ValueError('NGC adapter valid query roster mismatch')
 for q in binding['query_rows']:
  if q['id'] in bad:
   row={'id':q['id'],'speed_km_s':None,'valid':False,'reason':bad[q['id']],'radius_m':q['radius_m']}
   if bad[q['id']]==INVALID_ROW_REASON:row['innermost_radial_node_m']=float(R[0])
   else:
    row['first_unconfined_R_m']=binding['_ngc_outer_cut_radius_m']
    if bad[q['id']]==SUPPORT_GAP_ROW_REASON:row['last_retained_radial_node_m']=float(R[-1])
   rows.append(row)
  else:rows.append(dict(got[q['id']],valid=True))
 out=dict(packet);out['rows']=rows;out['invalid_rows']=[q['id'] for q in invalid];out['valid_row_count']=len(rows)-len(bad)
 if 'invalid_row_rule' in binding:out['invalid_row_rule']=binding['invalid_row_rule']
 if '_ngc_outer_cut_radius_m' in binding:out['ngc_outer_gas_cut_custody']=binding['_ngc_outer_cut_custody']
 out['adapter_query_ids']=[r['id'] for r in packet['rows']]
 return out


OUTER_INVALID_ROW_REASON='QUERY_BEYOND_OUTER_GAS_CUT'
SUPPORT_GAP_ROW_REASON='QUERY_OUTSIDE_RETAINED_SUPPORT'
def ngc_column_cut_custody(rs,rf):
 """The pinned rotation producer carries the same checkpoint-bound cut at start/finish."""
 a=(rs.get('uv_tail') or {}).get('ngc_outer_gas_cut_custody')
 b=(rf.get('uv_tail') or {}).get('ngc_outer_gas_cut_custody')
 if a!=b:raise ValueError('NGC outer-cut rotation start/finish custody mismatch')
 if a is None:return None
 if type(a) is not dict or set(a)!={'pin','record','seed_sha256','seed_pin','profile_pin','kpc_m','first_unconfined_R_m'}:raise ValueError('NGC outer-cut custody shape')
 pin=a['pin']
 if type(pin) is not dict or set(pin)!={'path','sha256'}:raise ValueError('NGC outer-cut pin shape')
 rec=json.loads(checked(pin['path'],pin['sha256']))
 if rec!=a['record'] or rec.get('schema')!='NGC_CANDIDATE_ROSTER_CUT_CX3V001' or rec.get('confinement_status')!='CERTIFIED_UNCONFINED' or type(rec.get('classification_evidence')) is not dict or not rec['classification_evidence']:raise ValueError('NGC outer-cut record/certificate mismatch')
 if a['seed_sha256']!=rs.get('seed_sha256') or a['seed_pin'].get('sha256')!=a['seed_sha256']:raise ValueError('NGC outer-cut seed mismatch')
 checked(a['seed_pin']['path'],a['seed_pin']['sha256'])
 cut=rec.get('first_unconfined_R_kpc');unit=a['kpc_m'];radius=a['first_unconfined_R_m']
 if any(type(v) not in (float,int) or not math.isfinite(v) or v<=0 for v in (cut,unit,radius)) or radius!=cut*unit:raise ValueError('NGC outer-cut radius/units mismatch')
 return a

UVT_BINDING=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_uvt_route_b_binding_cx3v006_r5cx3v001_cx3v005.py'),'aee7af1286f2d3d9d52117d6b4d4ae82e31d8776af4a4b0a6da7cee96be12fb3')
def uvt_load():
 """The pinned shared UV-tail binding (bytes checked before and after exec; inert at import)."""
 path,pin=UVT_BINDING
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('UV_TAIL_PIN_MISMATCH '+str(path))
 s=importlib.util.spec_from_file_location('uvt_route_b_binding_c2v001',str(path));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('UV_TAIL_PIN_CHANGED_AFTER_IMPORT '+str(path))
 return m

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--outdir',required=True);ap.add_argument('--galaxy-config',required=True,nargs=2,metavar=('PATH','SHA256'));a=ap.parse_args()
 out=Path(a.outdir);out.mkdir(exist_ok=False);result={'accepted_for_calibration':False,'scored':False,'input_pins':{}}
 try:
  PINS,NC,NPHI,NZ,OBSV,ROTW=galaxy_config(a.galaxy_config);result['input_pins']=PINS
  binding,rs,rf,cs,cf=[json.loads(checked(p,s)) for p,s in PINS.items()]
  check_binding(binding,OBSV)
  cut=ngc_column_cut_custody(rs,rf)
  if cut is not None:binding=dict(binding,_ngc_outer_cut_radius_m=cut['first_unconfined_R_m'],_ngc_outer_cut_custody=cut)
  if binding['source_convergence_claimed'] or binding['calibration_admission'] or binding['scoring_authorized_in_this_adapter']:raise ValueError('Conditional-only binding required')
  if rf['positive_rotation_square']is not True or rf['status']!='LAGGED_M0_ROTATION_EVALUATED_NOT_FULL_FLOW' or cf['failures']:raise ValueError('Complete positive lagged preparation required')
  if rs['producer_sha_inputs']['column-worker-sha256']!=cs['worker_sha256']:raise ValueError('Column worker mismatch')
  for key in ('entropy_scale','base_K_source','scaled_K_values_SI','field_provenance'):
   if not(rs[key]==rf[key]==cs[key]==cf[key]):raise ValueError('Same-K/field mismatch: '+key)
  if rs['worker_sha256']!=ROTW['sha256']:raise ValueError('Pin mismatch: '+str(ROTW['path']))
  for path,sha in [(ROTW['path'],rs['worker_sha256'])]:checked(path,sha)
  checked(rf['arrays_path'],rf['arrays_sha256'])
  with np.load(rf['arrays_path'],allow_pickle=False) as f:arrays={k:f[k].copy() for k in ('radial_nodes_m','z','rho0','K0','Omega','angular_radial_residual','angular_vertical_residual','angular_azimuthal_residual')}
  R=arrays['radial_nodes_m'];rho=arrays['rho0'];z=arrays['z'];K=arrays['K0'];omega=arrays['Omega']
  REGISTERED_NC=NC
  if cut is not None:
   UVT=uvt_load();seed=json.loads(checked(cut['seed_pin']['path'],cut['seed_pin']['sha256']));ni=seed['numerical_inputs']
   profile=cut['profile_pin']
   if profile is None:raise ValueError('NGC cut column-mean seed profile custody missing')
   caller={'numerical_controls':ni,'seed':cut['seed_pin']}
   NC=UVT.ngc_effective_n_columns(REGISTERED_NC,ni,caller,(profile['path'],profile['sha256']),R)
  result['ngc_radial_count_custody']=dict(registered_n_columns=REGISTERED_NC,effective_n_columns=NC)
  if R.shape!=(NC,) or rho.shape!=(NC,NPHI,NZ) or any(x.shape!=rho.shape for x in (z,K,omega)):raise ValueError('Frozen%d-node geometry mismatch'%NZ)
  if any(not np.isfinite(x).all() for x in arrays.values()) or np.any(omega<=0):raise ValueError('Invalid finite positive rotation')
  if any(not np.array_equal(x,np.broadcast_to(x[:,0:1,:],x.shape)) for x in (rho,z,K,omega)):raise ValueError('Actual m0 arrays required; no angular averaging')
  roster=rs['column_custody']
  if [x['index'] for x in roster]!=list(range(NC)) or len(cf['completed'])!=NC:raise ValueError('Complete%d ordered columns required'%NC)
  weights=[]
  for i,rec in enumerate(roster):
   col=json.loads(checked(rec['path'],rec['sha256']))
   if col['R_m']!=R[i] or col['radial_index']!=i or col['field_provenance']!=rs['field_provenance'] or col['entropy_scale']!=rs['entropy_scale']:raise ValueError('Column identity mismatch')
   if not np.array_equal(np.asarray(col['z_m']),z[i,0]) or not np.array_equal(np.asarray(col['rho_kg_m3']),rho[i,0]) or not np.all(K[i]==col['K_SI']):raise ValueError('Column/rotation physical arrays differ')
   w=np.asarray(col['weights_m'],float)*rho[i,0]*binding['HI_to_HI_plus_He_mass_ratio']
   if w.shape!=(NZ,) or not np.isfinite(w).all() or np.any(w<0):raise ValueError('Invalid explicit atomic-H tracer weights')
   weights.append(w.tolist())
  obs=module('obs',H/'galaxy_hi_observation_forward_v001.py',OBS_SHA)
  adapter=module('column_mean',H/'owned_column_mean_streaming_observation_v002.py',ADAPTER_SHA)
  speed=R[:,None]*omega[:,0,:]
  QROWS,INVALID=query_partition(binding,R)
  packet=adapter.evaluate(observation_module=obs,radial_nodes_m=R,query_ids=[q['id'] for q in QROWS],query_radii_m=[q['radius_m'] for q in QROWS],v_phi_m_s=speed,emissivity_path_weights=weights,physical_inclination_rad=binding['physical_inclination_rad'],released_inclination_rad=binding['released_inclination_rad'],approximation_provenance=binding['observation_rule'],tracer_provenance=binding['tracer_rule'],source_status=cf['status'],motion_status=rf['status'],nonaxisymmetric_residual_provenance='Pinned rotation arrays retain all%d azimuthal residuals; maxima below are diagnostics, never zeroed.'%NPHI)
  if INVALID is not None:packet=merge_invalid_rows(packet,binding,INVALID,R)
  result.update(status='CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION',prediction=packet,
   rotation_array_pin={'path':rf['arrays_path'],'sha256':rf['arrays_sha256']},column_custody=roster,
   module_pins={'adapter':ADAPTER_SHA,'observation':OBS_SHA},
   nonaxisymmetric_residual_maxima={k:float(np.max(np.abs(arrays[k]))) for k in ('angular_radial_residual','angular_vertical_residual','angular_azimuthal_residual')},
   residual_units='All three components are leading cylindrical reference-frame m/s^2; phi=(1/R)*partial_phi Phi. Not full-metric contravariant acceleration.',field_provenance=rs['field_provenance'])
 except Exception as exc:result.update(status='FAILED_NO_PREPARATION_OUTPUT',failure={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()})
 with (out/'result.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
if __name__=='__main__':main()
