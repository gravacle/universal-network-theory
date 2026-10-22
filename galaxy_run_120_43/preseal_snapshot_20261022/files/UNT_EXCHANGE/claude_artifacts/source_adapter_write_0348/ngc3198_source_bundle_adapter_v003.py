"""INERT candidate source-only bundle adapter V003 for NGC3198 (task 0348; derived from V002 3e6ca15a..., 0345-A/0346).
ROOT runs it after admission; the author has run it only on synthetic fixtures. V003 changes ONLY the write/publication
behaviour (CURRENT_INSTRUCTIONS "Do not delete, move"): V002 unlinked its temporary file; V003 never unlinks, moves or
overwrites anything. Extraction, allowlists, validation, bundle content and bundle schema label are unchanged from V002.

Builds ONE JSON bundle holding, side by side and unmodified:
  * queries: the 43 query IDs and literal radii from the root-admitted target-free manifest (radius metadata only);
  * S1_LEROY_T7: the P53 Leroy table7 rows (23 rings) on their own grid: literal exact-rational strings as P53 recorded
    them, literal error fields, P53 interpretation, missingness and quarantine flags;
  * S2_HALOGAS_PLANAR: the reviewed fixed-plane extraction, both subpixel orders (4, 8), both annular widths (40, 120
    arcsec), all three geometric groups, masks, raw missing-footprint fractions and descriptive scatter, on their own grids;
  * conventions: pinned Claude-authored provenance METADATA (0341 crosswalk text, verbatim) with the pinned 0346
    correction companion attached item by item;
  * machine-readable OPEN issues, with OPEN-4 computed from the S1 rows.
It does NOT select, combine, interpolate, extrapolate, deproject, convert units, apply helium, map queries to source
grids, or fill anything. Missing stays null. Negative values pass through unchanged.

Allowlist and provenance: every emitted OBSERVATIONAL value (queries, S1, S2) comes from an enumerated JSON pointer and is
emitted with that pointer; file and sha256 are given once per input block ('provenance'). Array element i comes from
pointer + '/' + i. Values the adapter adds itself are labelled 'adapter_label', 'adapter_constant' or 'derived_count'.
Keys that are not allowlisted never reach the output. The metadata inputs (crosswalk, correction) are pinned
Claude-authored text: they are copied verbatim, type-bounded to strings / string-keyed objects / lists (no numbers or
booleans except the correction's own flag fields), and are not observational values.
Fail-closed, two distinct failure classes:
  VALIDATION failure (exit 2, status FAILED_VALIDATION): duplicate JSON keys, NaN/Infinity tokens, any pin, type,
    null-rule, length, order, duplicate, domain, consistency or structure violation, or a pre-existing output/candidate
    path. Raised before any file is created: NO candidate and NO output are written.
  PUBLICATION failure (exit 4, status FAILED_PUBLICATION): any error while creating, writing, fsyncing, verifying or
    publishing the candidate. The candidate file MAY remain (complete or partial); it is retained, never removed; no
    success is claimed. Unexpected exceptions (exit 3) report the phase they occurred in.
Write lifecycle (V003): the complete bundle is built in memory; an exclusive candidate '<output>.candidate' is created
(O_EXCL), written, flushed and fsynced, re-read and checked against the in-memory sha256, then published by an
exclusive hard link to '<output>' (fails if it exists); the directory is then fsynced and the published file re-read
and checked. Candidate and output are two names of the same complete bytes; both paths and hashes are reported.
Nothing is ever unlinked, moved or overwritten.
Usage: python3 -I -B ngc3198_source_bundle_adapter_v003.py <new_bundle.json>
"""
import hashlib,json,math,os,re,sys
from pathlib import Path
BASE='/Users/bgm/Research/Universal Network Theory/'
XW='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_crosswalk_0341/'
INPUTS={
 'query_manifest':(BASE+'UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json','a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'),
 's1_table':(BASE+'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/P53_COMPLETE_NATIVE_INPUT_PARSER_HELD_SOURCE_V002/ROOT_COMPLETE_PARSER_CALLS_V002/RETURNS/01_TABLE_FULL.json','4cf4b4b386f7a129fceaa4da7b5eede9f2c528e518f058ed71603ff667e29d24'),
 's2_results':(BASE+'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/halogas_source_candidate/PLANAR_SOURCE_RESULTS.json','44b359abbcae5c0c61b26d3adc515a716fd6d45795fcecff3004189814230b2c'),
 'crosswalk':(XW+'SOURCE_CROSSWALK_V001.json','691483835e9d5201957a2b7183deaa1e8d994efeaa2644c3374d8e59f2450c72'),
 'crosswalk_correction':(XW+'SOURCE_CROSSWALK_CORRECTION_0346_V001.json','988e871acc0e6f3c1e3b91abec7143cb5b69241d6894b140f15369a6f29fca24'),
 'ledger':(XW+'UNCERTAINTY_MISSING_INPUT_LEDGER_V001.json','07dd4aa300b8b818a2b962646dffd3711f461cccfa87052f7f9d760e4fdb29e0')}
N_QUERIES=43;N_S1=23;S1_LINES=list(range(320,343));ORDERS=[4,8];PROFILES={'profile_40arcsec':(40.0,237),'profile_120arcsec':(120.0,79)}
GROUPS=['full','X_negative','X_nonnegative']
S2_SETTINGS=['HI_atoms_cm2_per_Msun_pc2','bin_arcsec','center_dec_deg','center_ra_deg','center_source','column_conversion_from_history','distance_pc','geometry','helium_factor','inclination_deg','orientation_source','pa_deg','rebin']
S2_PIXEL=['finite','negative','nonfinite','positive','total','zero_or_replaced_mask']
# group field -> (adapter_label kind, null rule: 'never' | 'iff_incomplete' | 'allowed')
S2_FIELDS={
 'mass_Msun':('retained_signed_mass','never'),'positive_mass_Msun':('retained_positive_mass','never'),'negative_mass_Msun':('retained_negative_mass_signed','never'),
 'effective_HI_Msun_pc2_complete_only':('effective_density_bare_HI','iff_incomplete'),
 'effective_HI_plus_He_Msun_pc2_complete_only':('effective_density_HI_plus_He_as_extracted (factor at /settings/helium_factor; PROGRAM-DECLARED, see correction C5)','iff_incomplete'),
 'zero_fraction_of_footprint':('mask_fraction_zero_or_replaced','never'),'finite_fraction_of_footprint':('mask_fraction_finite','never'),
 'positive_fraction_of_footprint':('area_fraction_positive','never'),'negative_fraction_of_footprint':('area_fraction_negative','never'),
 'missing_footprint_fraction_raw':('geometric_missing_footprint_fraction_raw_unclipped_quadrature_not_a_noise_model','never'),
 'nominal_disk_area_pc2':('geometry_area','never'),'plane_pc2':('geometry_area','never'),
 'cosi_times_finite_sky_weighted_LOS_sigma_rms_Msun_pc2_not_measurement_error':('descriptive_scatter_not_measurement_error','allowed')}
S2_PROFILE_ARRAYS={'r_lo_kpc':('annulus_inner_edge_kpc','never'),'r_hi_kpc':('annulus_outer_edge_kpc','never'),'complete_by_conservative_chord_bound':('geometric_completeness_flag','bool')}
CROSSWALK_CONVENTIONS={
 'S1_LEROY_T7':['tracers','radial_coordinate','resolution','geometry','units','helium_conversion_state','masks','error_fields','support'],
 'S2_HALOGAS_C1':['tracer','radial_coordinate','geometry','units','helium_conversion_state','masks','error_fields','support','resolution']}
S1_INTERP={'VALUE_WITH_PUBLISHED_RMS','UPPER_LIMIT_NOTE3','MISSING'}
OPEN_ISSUES=[
 {'id':'OPEN-1','topic':'HI_TRACER_DOUBLE_COUNT','state':'OPEN','detail':'S1 HI (THINGS VLA) and S2 (WSRT) observe the same 21-cm HI over 0.3-15.1 kpc; S5 Begeman (not in bundle) overlaps both. Counting the same HI once requires a declared rule; none is made.','refs':['crosswalk:/same_tracer_overlaps/0','ledger:/items/16']},
 {'id':'OPEN-2','topic':'STELLAR_CONVENTION_AND_DOUBLE_COUNT','state':'OPEN','detail':'S1 stars (Leroy, M/L applied) vs SPARC .sfb/.dens (not in bundle): fixed conversion ratio 1.2568 between conventions; inclination 72 vs 73; no source chosen.','refs':['crosswalk:/same_tracer_overlaps/1','ledger:/items/17']},
 {'id':'OPEN-3','topic':'STELLAR_OUTER_SUPPORT','state':'OPEN','detail':'S1 stars end at 15.1 kpc; no observed stellar profile covers 21.42-44.08 kpc (12 queries); SPARC .dens rows there are inferred extrapolation; the last query lies beyond the last .dens row.','refs':['crosswalk:/support_by_query_band','ledger:/items/14']},
 {'id':'OPEN-4','topic':'MISSING_H2','state':'OPEN','detail':'S1 H2 MISSING rows are null, never zero (row indices computed below); no other H2 source found in the searched paths.','refs':['ledger:/items/10'],'computed':None},
 {'id':'OPEN-5','topic':'GEOMETRY_QUARANTINE','state':'OPEN','detail':'SPARC catalogue geometry extraction V001 QUARANTINED; V002 inert pending schema provenance (0344/0345-B). S1 and S2 both use the Leroy table4 working plane (i 72, PA 215) and D 13.8 Mpc without uncertainty; these values are SECONDARY (correction C4/C6); the S2 plane is not a warp solution.','refs':['ledger:/items/7','ledger:/items/15','crosswalk_correction:/corrections/3','crosswalk_correction:/corrections/5']},
 {'id':'OPEN-6','topic':'NATIVE_OBSERVATION_MAP','state':'OPEN','detail':'No map from these observational records to native UNT record-surface inputs exists (S1 table_level raw_to_native_map, checked null). Owned by native-physics work, not by this adapter.','refs':['s1_table:/value/raw_to_native_map']},
 {'id':'OPEN-7','topic':'S2_UNCERTAINTY_AND_MASK','state':'OPEN','detail':'S2 has no measurement uncertainty (unknown, not zero); its mask uses a kinematic window (reduction dependency); 40.14-48.17 kpc annulus is review-flagged (43.66% zero/replaced).','refs':['ledger:/items/0','ledger:/items/4','ledger:/items/5']},
 {'id':'OPEN-8','topic':'S1_ERROR_SEMANTICS','state':'OPEN','detail':'S1 per-ring rms fields: whether each is a measurement uncertainty or a descriptive azimuthal scatter is not established locally; e=1 on HI/stars carries ReadMe Note 3 "upper limit" (quarantined); e=0 is literal with unresolved meaning; no replacement errors.','refs':['ledger:/items/8','ledger:/items/9']},
 {'id':'OPEN-9','topic':'QUERY_TO_SOURCE_GRID','state':'OPEN','detail':'Queries are emitted separately. No mapping, interpolation or extrapolation from source grids to query radii is performed.','refs':[]},
 {'id':'OPEN-10','topic':'PRIMARY_CONVERSION_VERIFICATION','state':'OPEN','detail':'Only "Including helium" (Leroy ReadMe Note 2) is primary-stated. SECONDARY: helium 1.36, X_CO, CO line ratio, stellar M/L relation (C1-C3), S1/S2 geometry values i/PA/D (C4, C6), S2 centre citation (C6). PROGRAM-DECLARED: 1.25e20 per Msun/pc^2 and the S2 helium factor and working plane (C5, C6). Carry rules unchanged; primary verification pending.','refs':['crosswalk_correction:/corrections']}]
FAIL_CODES='see SOURCE_BUNDLE_FIELD_CONTRACT_V002.json /failure_codes'
def _a(p):return re.compile(p,re.ASCII)
RATIONAL=_a(r'-?\d+(/[1-9]\d*)?');DECIMAL=_a(r'\d+(\.\d+)?');QID=_a(r'NGC3198-Q(\d{2})');SHA=_a(r'[0-9a-f]{64}')
def full(rx,s):return isinstance(s,str) and rx.fullmatch(s) is not None
class Fail(Exception):pass
class PublishFail(Exception):
 def __init__(self,code,info):super().__init__(code);self.code=code;self.info=info
PHASE=['VALIDATION']
def sha(b):return hashlib.sha256(b).hexdigest()
def _pairs(ps):
 d={}
 for k,v in ps:
  if k in d:raise Fail('E_JSON_DUPLICATE_KEY')
  d[k]=v
 return d
def _const(c):raise Fail('E_JSON_NONFINITE_TOKEN')
def load(key):
 p,h=INPUTS[key];b=Path(p).read_bytes()
 if sha(b)!=h:raise Fail('E_PIN_'+key)
 try:return json.loads(b,object_pairs_hook=_pairs,parse_constant=_const),{'file':p,'sha256':h,'bytes':len(b)}
 except ValueError:raise Fail('E_JSON_'+key)
def need(o,k,code,t=None):
 if not isinstance(o,dict) or k not in o:raise Fail(code)
 v=o[k]
 if t is not None and (type(v) is bool and t is not bool or not isinstance(v,t)):raise Fail(code+'_TYPE')
 return v
def num(x):return type(x) in (int,float) and math.isfinite(x)
def text_bounded(x,depth=0,allow_flags=False):
 """Metadata copies: strings, string-keyed objects and lists only (bools only for the correction's own flags)."""
 if depth>6:return False
 if isinstance(x,str):return True
 if type(x) is bool:return allow_flags
 if isinstance(x,list):return all(text_bounded(y,depth+1,allow_flags) for y in x)
 if isinstance(x,dict):return all(isinstance(k,str) and text_bounded(v,depth+1,allow_flags) for k,v in x.items())
 return False
def queries(m,pin):
 rows=need(m,'rows','E_Q_ROWS',list)
 if len(rows)!=N_QUERIES:raise Fail('E_Q_COUNT')
 out=[];seen=set();prev=None
 for i,r in enumerate(rows):
  q=need(r,'query_id','E_Q_ID',str);rt=need(r,'Rad_text','E_Q_RAD',str);u=need(r,'Rad_unit','E_Q_UNIT',str)
  if q in seen:raise Fail('E_Q_DUPLICATE')
  seen.add(q)
  mq=QID.fullmatch(q)
  if not mq or int(mq.group(1))!=i+1:raise Fail('E_Q_ID_ORDER')
  if u!='kpc':raise Fail('E_Q_UNIT_VALUE')
  if not full(DECIMAL,rt) or not float(rt)>0:raise Fail('E_Q_RAD_DOMAIN')
  if prev is not None and not float(rt)>prev:raise Fail('E_Q_RAD_ORDER')
  prev=float(rt)
  out.append({'query_id':q,'Rad_text':rt,'Rad_unit':u,'pointer':'/rows/%d'%i})
 return {'provenance':pin,'items':out,'note':'radius metadata only; not mapped to any source grid'}
def s1(t,pin):
 if need(t,'status','E_S1_STATUS',str)!='RETURN':raise Fail('E_S1_STATUS_VALUE')
 v=need(t,'value','E_S1_VALUE',dict)
 if need(v,'representation','E_S1_REPR',str)!='MASS_SURFACE_DENSITY':raise Fail('E_S1_REPR_VALUE')
 tl={}
 ws=need(v,'whole_table_sha256','E_S1_TABLE_SHA',str)
 if not full(SHA,ws):raise Fail('E_S1_TABLE_SHA_FORMAT')
 tl['whole_table_sha256']={'value':ws,'pointer':'/value/whole_table_sha256'}
 for k,exp in (('whole_covariance',None),('raw_to_native_map',None),('source_selected',False),('physical_prediction_released',False)):
  x=need(v,k,'E_S1_TL_'+k)
  if x is not exp:raise Fail('E_S1_TL_VALUE_'+k)
  tl[k]={'value':x,'pointer':'/value/'+k}
 rows=need(v,'rows','E_S1_ROWS',list)
 if len(rows)!=N_S1:raise Fail('E_S1_COUNT')
 out=[];prev=None;lines=[];h2_present=[];h2_missing=[]
 for i,r in enumerate(rows):
  ln=need(r,'original_line_number','E_S1_LINE',int);lines.append(ln)
  rk=need(r,'radius_kpc','E_S1_RADIUS',str)
  if not full(RATIONAL,rk):raise Fail('E_S1_RADIUS_FORMAT')
  a,_,b=rk.partition('/');rv=int(a)/(int(b) if b else 1)
  if not rv>0 or (prev is not None and not rv>prev):raise Fail('E_S1_RADIUS_DOMAIN')
  prev=rv
  un=need(r,'units','E_S1_UNITS',str)
  if un!='Msun/pc^2':raise Fail('E_S1_UNITS_VALUE')
  gh=need(r,'gas_helium','E_S1_CONV_gas_helium',str);hm=need(r,'helium_multiplier_applied','E_S1_CONV_helium_multiplier_applied');sm=need(r,'stellar_ML_applied_again','E_S1_CONV_stellar_ML_applied_again')
  if gh!='ALREADY_INCLUDED' or hm is not False or sm is not False:raise Fail('E_S1_CONV_VALUE')
  conv={k:{'value':x,'pointer':'/value/rows/%d/%s'%(i,k)} for k,x in (('gas_helium',gh),('helium_multiplier_applied',hm),('stellar_ML_applied_again',sm),('units',un))}
  comps={}
  for c in ('HI','H2','stars'):
   e=need(r,c,'E_S1_'+c,dict);base='/value/rows/%d/%s'%(i,c)
   val=need(e,'published_value','E_S1_'+c+'_VALUE');err=need(e,'published_error_field','E_S1_'+c+'_ERR');interp=need(e,'interpretation','E_S1_'+c+'_INTERP',str)
   if interp not in S1_INTERP:raise Fail('E_S1_INTERP_UNKNOWN')
   if interp=='MISSING':
    if val is not None or err is not None:raise Fail('E_S1_MISSING_NOT_NULL')
    kind='MISSING'
   else:
    if not (full(RATIONAL,val) and full(RATIONAL,err)):raise Fail('E_S1_LITERAL_FORMAT')
    if err.startswith('-'):raise Fail('E_S1_NEGATIVE_ERROR')
    note3=(err=='1' and c in ('HI','stars'))
    if note3!=(interp=='UPPER_LIMIT_NOTE3'):raise Fail('E_S1_INTERP_MISMATCH')
    if note3:kind='PUBLISHED_FIELD_1_NOTE3_UPPER_LIMIT_MARKER_QUARANTINED'
    elif err=='0':kind='LITERAL_ZERO_MEANING_UNRESOLVED'
    else:kind='PUBLISHED_PER_RING_RMS_FIELD'
   if c=='H2':(h2_missing if interp=='MISSING' else h2_present).append(i)
   comps[c]={'value_literal':{'value':val,'pointer':base+'/published_value'},'error_literal':{'value':err,'pointer':base+'/published_error_field'},
    'p53_interpretation':{'value':interp,'pointer':base+'/interpretation'},'error_kind':{'adapter_label':kind}}
  out.append({'row_index':i,'original_line_number':{'value':ln,'pointer':'/value/rows/%d/original_line_number'%i},'radius_kpc_literal':{'value':rk,'pointer':'/value/rows/%d/radius_kpc'%i},'conventions':conv,'components':comps})
 if lines!=S1_LINES:raise Fail('E_S1_LINE_ORDER')
 return {'provenance':pin,'literal_format':'exact rational strings as recorded by P53 (e.g. "102/5"); not converted',
  'table_level':tl,'unknown_uncertainty':'ring-to-ring covariance and conversion systematics (X_CO, line ratio, M/L) are unknown; not zero','rows':out},{'present_rows':h2_present,'missing_rows':h2_missing}
def arr(o,k,n,code,rule,comp=None):
 v=need(o,k,code,list)
 if len(v)!=n:raise Fail(code+'_LENGTH')
 for j,x in enumerate(v):
  if rule=='bool':
   if type(x) is not bool:raise Fail(code+'_TYPE')
  elif x is None:
   if rule=='never' or (rule=='iff_incomplete' and comp[j]):raise Fail(code+'_NULL')
  elif not num(x):raise Fail(code+'_TYPE')
  elif rule=='iff_incomplete' and not comp[j]:raise Fail(code+'_VALUE_ON_INCOMPLETE')
 return v
def s2(d,pin):
 if need(d,'status','E_S2_STATUS',str)!='COMPLETE' or need(d,'failed_checks','E_S2_FAILED',list)!=[]:raise Fail('E_S2_NOT_COMPLETE')
 st=need(d,'settings','E_S2_SETTINGS',dict);settings={}
 for k in S2_SETTINGS:
  x=need(st,k,'E_S2_SETTING_'+k)
  if not (num(x) or isinstance(x,str)):raise Fail('E_S2_SETTING_TYPE_'+k)
  settings[k]={'value':x,'pointer':'/settings/'+k}
 pc=need(d,'pixel_categories','E_S2_PIXELS',dict);pix={}
 for k in S2_PIXEL:
  x=need(pc,k,'E_S2_PIXEL_'+k,int)
  if x<0:raise Fail('E_S2_PIXEL_DOMAIN')
  pix[k]={'value':x,'pointer':'/pixel_categories/'+k}
 orders=need(d,'orders','E_S2_ORDERS',list)
 if [need(o,'subpixels_per_axis','E_S2_SUBPIX',int) for o in orders]!=ORDERS:raise Fail('E_S2_ORDER_SET')
 out=[]
 for oi,o in enumerate(orders):
  po={}
  for pk,(w,n) in PROFILES.items():
   p=need(o,pk,'E_S2_PROFILE',dict);base='/orders/%d/%s'%(oi,pk)
   wv=need(p,'width_arcsec','E_S2_WIDTH')
   if not num(wv) or wv!=w:raise Fail('E_S2_WIDTH_VALUE')
   comp=arr(p,'complete_by_conservative_chord_bound',n,'E_S2_COMPLETE','bool')
   lo=arr(p,'r_lo_kpc',n,'E_S2_RLO','never');hi=arr(p,'r_hi_kpc',n,'E_S2_RHI','never')
   if lo[0]!=0 or any(not hi[j]>lo[j] for j in range(n)) or any(abs(hi[j]-lo[j+1])>1e-9*max(1,hi[j]) for j in range(n-1)):raise Fail('E_S2_GRID')
   if any(comp[j+1] and not comp[j] for j in range(n-1)):raise Fail('E_S2_COMPLETE_NOT_PREFIX')
   prof={'width_arcsec':{'value':wv,'pointer':base+'/width_arcsec'},'n_bins':{'derived_count':n}}
   for k,(kind,rule) in S2_PROFILE_ARRAYS.items():prof[k]={'kind':kind,'pointer':base+'/'+k,'values':p[k]}
   gs=need(p,'groups','E_S2_GROUPS',dict);prof['groups']={}
   for g in GROUPS:
    gd=need(gs,g,'E_S2_GROUP_'+g,dict);prof['groups'][g]={}
    for f,(kind,rule) in S2_FIELDS.items():
     prof['groups'][g][f]={'kind':kind,'null_rule':rule,'pointer':base+'/groups/%s/%s'%(g,f),'values':arr(gd,f,n,'E_S2_FIELD_'+f,rule,comp)}
   po[pk]=prof
  out.append({'order_index':oi,'subpixels_per_axis':{'value':orders[oi]['subpixels_per_axis'],'pointer':'/orders/%d/subpixels_per_axis'%oi},'profiles':po})
 return {'provenance':pin,'interpretation':{'value':need(d,'interpretation','E_S2_INTERP',str),'pointer':'/interpretation'},'settings':settings,'pixel_categories':pix,'orders':out,
  'measurement_uncertainty':{'state':'UNKNOWN','note':'no noise/error product in the release; not zero; the descriptive scatter field is not a measurement error'}}
def resolve(o,ptr,code):
 if not isinstance(ptr,str) or not ptr.startswith('/') or ptr.endswith('/') or '//' in ptr or '~' in ptr:raise Fail(code+'_SYNTAX')
 parts=ptr[1:].split('/')
 for t in parts:
  if not isinstance(o,dict) or t not in o:raise Fail(code+'_UNRESOLVED')
  o=o[t]
 return parts
def conventions(cw,pin,corr,cpin):
 src=need(cw,'sources','E_CW_SOURCES',dict);out={}
 for sid,keys in CROSSWALK_CONVENTIONS.items():
  s=need(src,sid,'E_CW_'+sid,dict);out[sid]={}
  for k in keys:
   x=need(s,k,'E_CW_'+sid+'_'+k)
   if not text_bounded(x):raise Fail('E_CW_TYPE_'+sid+'_'+k)
   out[sid][k]={'text':x,'pointer':'/sources/%s/%s'%(sid,k),'corrections':[]}
 cb=need(corr,'corrects','E_CORR_BINDING',dict)
 if need(cb,'sha256','E_CORR_BINDING',str)!=pin['sha256']:raise Fail('E_CORR_BINDING_SHA')
 if Path(need(cb,'file','E_CORR_BINDING_FILE',str)).name!=Path(pin['file']).name or need(cb,'unchanged','E_CORR_BINDING_UNCHANGED') is not True:raise Fail('E_CORR_BINDING_FILE')
 other=[];ids=set();source_level=[]
 for i,c in enumerate(need(corr,'corrections','E_CORR_LIST',list)):
  cid=need(c,'id','E_CORR_ID',str);ptr=need(c,'crosswalk_pointer','E_CORR_POINTER',str);now=need(c,'now','E_CORR_NOW',dict)
  if not text_bounded(now,allow_flags=True):raise Fail('E_CORR_NOW_TYPE')
  if cid in ids:raise Fail('E_CORR_DUPLICATE')
  ids.add(cid);parts=resolve(cw,ptr,'E_CORR_POINTER')
  ref={'id':cid,'crosswalk_pointer':ptr,'correction_pointer':'/corrections/%d'%i,'now':now}
  if parts[0]=='sources' and len(parts)>=3 and parts[1] in out and parts[2] in out[parts[1]]:out[parts[1]][parts[2]]['corrections'].append(ref)
  elif parts[0]=='sources' and len(parts)>=2 and parts[1] in out:source_level.append(ref)
  else:other.append(ref)
 return {'class':'pinned Claude-authored provenance METADATA (not observational values)','provenance':pin,'correction_provenance':cpin,'items':out,'source_level_corrections':source_level,'corrections_for_sources_not_in_bundle':other,
  'rule':'where a correction is attached, its "now" supersedes the crosswalk text for provenance class; the crosswalk text is kept verbatim'}
def open_issues(ledger,lpin,cpin,h2):
 items=need(ledger,'items','E_LEDGER_ITEMS',list);out=[]
 for o in OPEN_ISSUES:
  x=dict(o)
  for r in x['refs']:
   if r.startswith('ledger:'):
    j=int(r.split('/')[-1])
    if not (0<=j<len(items)):raise Fail('E_LEDGER_REF')
  if x['id']=='OPEN-4':x['computed']=dict(h2,source='S1 rows by H2 interpretation')
  out.append(x)
 return {'ref_files':{'ledger':lpin,'crosswalk_correction':cpin,'crosswalk':'see conventions.provenance','s1_table':'see sources.S1_LEROY_T7.provenance'},'items':out}
def candidate_path(outp):return outp.with_name(outp.name+'.candidate')
def publish(outp,b):
 """Create, fsync and verify an exclusive candidate, then publish it by exclusive hard link. Never unlinks/moves/overwrites."""
 cand=candidate_path(outp);want=sha(b)
 info={'candidate_path':str(cand),'candidate_created':False,'expected_sha256':want,'expected_bytes':len(b),'output_path':str(outp),'output_published':False}
 try:fd=os.open(cand,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
 except FileExistsError:raise PublishFail('E_CANDIDATE_EXISTS',info)
 except OSError as e:info['error']=type(e).__name__;raise PublishFail('E_CANDIDATE_CREATE',info)
 info['candidate_created']=True
 try:
  with os.fdopen(fd,'wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 except OSError as e:info['error']=type(e).__name__;raise PublishFail('E_CANDIDATE_WRITE',info)
 try:cb=cand.read_bytes()
 except OSError as e:info['error']=type(e).__name__;raise PublishFail('E_CANDIDATE_VERIFY',info)
 info['candidate_sha256']=sha(cb);info['candidate_bytes']=len(cb)
 if cb!=b:raise PublishFail('E_CANDIDATE_VERIFY',info)
 try:os.link(cand,outp)
 except FileExistsError:raise PublishFail('E_OUTPUT_EXISTS_AT_PUBLICATION',info)
 except OSError as e:info['error']=type(e).__name__;raise PublishFail('E_PUBLICATION_LINK',info)
 info['output_published']=True
 try:
  dfd=os.open(str(outp.parent),os.O_RDONLY)
  try:os.fsync(dfd)
  finally:os.close(dfd)
 except OSError as e:info['error']=type(e).__name__;raise PublishFail('E_DIRECTORY_FSYNC',info)
 try:ob=outp.read_bytes()
 except OSError as e:info['error']=type(e).__name__;raise PublishFail('E_OUTPUT_VERIFY',info)
 info['output_sha256']=sha(ob);info['output_bytes']=len(ob)
 if ob!=b:raise PublishFail('E_OUTPUT_VERIFY',info)
 return {'candidate':{'path':str(cand),'sha256':info['candidate_sha256'],'bytes':info['candidate_bytes']},'output':{'path':str(outp),'sha256':info['output_sha256'],'bytes':info['output_bytes']},
  'same_file':os.path.samefile(cand,outp),'note':'candidate and output are two names of the same complete bytes; neither is ever removed'}
def main(argv):
 if len(argv)!=2:raise Fail('E_USAGE')
 outp=Path(argv[1])
 if os.path.lexists(outp):raise Fail('E_OUTPUT_EXISTS')
 if os.path.lexists(candidate_path(outp)):raise Fail('E_CANDIDATE_EXISTS')
 m,pm=load('query_manifest');t,pt=load('s1_table');d,pd=load('s2_results');cw,pc=load('crosswalk');cc,pcc=load('crosswalk_correction');lg,plg=load('ledger')
 s1rec,h2=s1(t,pt)
 bundle={'schema':'NGC3198_SOURCE_ONLY_BUNDLE_CANDIDATE_V002','status':'CANDIDATE_NOT_ADMITTED',
  'adapter':{'file':str(Path(__file__)),'sha256':sha(Path(__file__).read_bytes())},
  'scope':'S1 and S2 as separate source records on original grids and conventions; no selection, combination, interpolation, extrapolation, deprojection, unit/helium conversion or query mapping; missing stays null; negative values preserved',
  'provenance_rule':'every observational value carries a JSON pointer; file and sha256 are in the enclosing block provenance; array element i = pointer + "/" + i; adapter_label / adapter_constant / derived_count mark values the adapter adds',
  'value_kinds':{'PUBLISHED_PER_RING_RMS_FIELD':'S1 published per-ring rms field (measurement vs descriptive meaning OPEN-8)','descriptive_scatter_not_measurement_error':'S2 descriptive scatter','mask_fraction_*':'S2 mask bookkeeping','UNKNOWN':'uncertainty not available; never zero','MISSING':'value absent; null'},
  'queries':queries(m,pm),'sources':{'S1_LEROY_T7':s1rec,'S2_HALOGAS_PLANAR':s2(d,pd)},'conventions':conventions(cw,pc,cc,pcc),'open_issues':open_issues(lg,plg,pcc,h2)}
 b=(json.dumps(bundle,indent=1,allow_nan=False)+'\n').encode()
 PHASE[0]='PUBLICATION'
 pub=publish(outp,b)
 print(json.dumps({'status':'CANDIDATE_BUNDLE_WRITTEN','phase':'PUBLISHED','candidate':pub['candidate'],'output':pub['output'],'same_file':pub['same_file'],'queries':N_QUERIES,'s1_rows':N_S1,'s2_orders':ORDERS}))
 return 0
if __name__=='__main__':
 try:sys.exit(main(sys.argv))
 except Fail as e:print(json.dumps({'status':'FAILED_VALIDATION','code':str(e),'phase':'VALIDATION','candidate_written':False,'success_claimed':False}));sys.exit(2)
 except PublishFail as e:print(json.dumps({'status':'FAILED_PUBLICATION','code':e.code,'phase':'PUBLICATION','publication':e.info,'candidate_retained_if_created':True,'success_claimed':False}));sys.exit(4)
 except Exception as e:print(json.dumps({'status':'FAILED','code':'E_UNEXPECTED','type':type(e).__name__,'phase':PHASE[0],'candidate_may_remain':PHASE[0]=='PUBLICATION','success_claimed':False}));sys.exit(3)
