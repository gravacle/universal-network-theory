"""INERT candidate source-only bundle adapter V001 for NGC3198 (task 0345-A). ROOT runs it after admission; the author has
run it only on synthetic fixtures.

Builds ONE JSON bundle holding, side by side and unmodified:
  * queries: the 43 query IDs and literal radii from the root-admitted target-free manifest (radius metadata only);
  * S1_LEROY_T7: the P53 Leroy table7 rows (23 rings) on their own grid, literal exact-rational strings as P53 recorded
    them, with literal error fields, P53 interpretation, missingness and quarantine flags;
  * S2_HALOGAS_PLANAR: the reviewed fixed-plane extraction, both subpixel orders (4, 8) and both annular widths
    (40, 120 arcsec), all three geometric groups, masks and descriptive scatter, on their own grids;
  * conventions copied verbatim from the pinned 0341 crosswalk (with JSON pointers), with the pinned 0346 correction
    companion attached item by item (numeric conversion factors split into primary-stated / secondary / program-declared);
  * machine-readable OPEN issues.
It does NOT select, combine, interpolate, extrapolate, deproject, convert units, apply helium, map queries to source
grids, or fill anything. Missing stays null. Negative values pass through unchanged.

Allowlist only: every emitted observational value comes from an enumerated JSON pointer of a pinned input. Each emitted
array carries {'pointer','sha256','file'}; element i comes from pointer + '/' + str(i). Keys that are not allowlisted
(including any velocity, response or force field) are never read into the output.
Fail-closed: any pin, type, null-rule, length, order, duplicate, domain or structure violation raises a coded failure and
NO bundle is written. Refuses to overwrite.
Usage: python3 -B ngc3198_source_bundle_adapter_v001.py <new_bundle.json>
"""
import hashlib,json,math,re,sys
from pathlib import Path
BASE='/Users/bgm/Research/Universal Network Theory/'
INPUTS={
 'query_manifest':(BASE+'UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json','a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'),
 's1_table':(BASE+'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/P53_COMPLETE_NATIVE_INPUT_PARSER_HELD_SOURCE_V002/ROOT_COMPLETE_PARSER_CALLS_V002/RETURNS/01_TABLE_FULL.json','4cf4b4b386f7a129fceaa4da7b5eede9f2c528e518f058ed71603ff667e29d24'),
 's2_results':(BASE+'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/halogas_source_candidate/PLANAR_SOURCE_RESULTS.json','44b359abbcae5c0c61b26d3adc515a716fd6d45795fcecff3004189814230b2c'),
 'crosswalk':('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_crosswalk_0341/SOURCE_CROSSWALK_V001.json','691483835e9d5201957a2b7183deaa1e8d994efeaa2644c3374d8e59f2450c72'),
 'crosswalk_correction':('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_crosswalk_0341/SOURCE_CROSSWALK_CORRECTION_0346_V001.json','988e871acc0e6f3c1e3b91abec7143cb5b69241d6894b140f15369a6f29fca24')}
N_QUERIES=43;N_S1=23;S1_LINES=range(320,343);ORDERS=[4,8];PROFILES={'profile_40arcsec':(40.0,237),'profile_120arcsec':(120.0,79)}
GROUPS=['full','X_negative','X_nonnegative']
S2_SETTINGS=['HI_atoms_cm2_per_Msun_pc2','bin_arcsec','center_dec_deg','center_ra_deg','center_source','column_conversion_from_history','distance_pc','geometry','helium_factor','inclination_deg','orientation_source','pa_deg','rebin']
S2_PIXEL=['finite','negative','nonfinite','positive','total','zero_or_replaced_mask']
# group field -> value kind; null rule: 'never' | 'iff_incomplete' | 'allowed'
S2_FIELDS={
 'mass_Msun':('retained_signed_mass','never'),'positive_mass_Msun':('retained_positive_mass','never'),'negative_mass_Msun':('retained_negative_mass_signed','never'),
 'effective_HI_Msun_pc2_complete_only':('effective_density_bare_HI','iff_incomplete'),'effective_HI_plus_He_Msun_pc2_complete_only':('effective_density_HI_plus_He_x1.36_as_extracted','iff_incomplete'),
 'zero_fraction_of_footprint':('mask_fraction_zero_or_replaced','never'),'finite_fraction_of_footprint':('mask_fraction_finite','never'),
 'positive_fraction_of_footprint':('area_fraction_positive','never'),'negative_fraction_of_footprint':('area_fraction_negative','never'),
 'nominal_disk_area_pc2':('geometry_area','never'),'plane_pc2':('geometry_area','never'),
 'cosi_times_finite_sky_weighted_LOS_sigma_rms_Msun_pc2_not_measurement_error':('descriptive_scatter_not_measurement_error','allowed')}
S2_PROFILE_ARRAYS={'r_lo_kpc':'annulus_inner_edge_kpc','r_hi_kpc':'annulus_outer_edge_kpc','complete_by_conservative_chord_bound':'geometric_completeness_flag'}
CROSSWALK_CONVENTIONS={
 'S1_LEROY_T7':['tracers','radial_coordinate','resolution','geometry','units','helium_conversion_state','masks','error_fields','support'],
 'S2_HALOGAS_C1':['tracer','radial_coordinate','geometry','units','helium_conversion_state','masks','error_fields','support','resolution']}
OPEN_ISSUES=[
 {'id':'OPEN-1','topic':'HI_TRACER_DOUBLE_COUNT','state':'OPEN','detail':'S1 HI (THINGS VLA) and S2 (WSRT) observe the same 21-cm HI over 0.3-15.1 kpc; S5 Begeman (not in bundle) overlaps both. Counting the same HI once requires a declared rule; none is made.','refs':['crosswalk:/same_tracer_overlaps/0','ledger:U17']},
 {'id':'OPEN-2','topic':'STELLAR_CONVENTION_AND_DOUBLE_COUNT','state':'OPEN','detail':'S1 stars (Leroy, M/L applied) vs SPARC .sfb/.dens (not in bundle): fixed conversion ratio 1.2568; inclination 72 vs 73; no source chosen.','refs':['crosswalk:/same_tracer_overlaps/1','ledger:U18']},
 {'id':'OPEN-3','topic':'STELLAR_OUTER_SUPPORT','state':'OPEN','detail':'S1 stars end at 15.1 kpc; no observed stellar profile covers 21.42-44.08 kpc (12 queries); SPARC .dens rows there are inferred extrapolation; the last query lies beyond the last .dens row.','refs':['crosswalk:/support_by_query_band','ledger:U15']},
 {'id':'OPEN-4','topic':'MISSING_H2','state':'OPEN','detail':'S1 H2 present rows 0-9 (to 6.4 kpc) only; rows 10-22 MISSING (null, not zero); no other H2 source found in searched paths.','refs':['ledger:U11']},
 {'id':'OPEN-5','topic':'GEOMETRY_QUARANTINE','state':'OPEN','detail':'SPARC catalogue geometry extraction V001 QUARANTINED; V002 inert pending schema provenance (0344/0345-B). S1 and S2 both use the Leroy table4 working plane (i 72, PA 215) and D 13.8 Mpc without uncertainty; S2 plane is not a warp solution.','refs':['ledger:U8','ledger:U16']},
 {'id':'OPEN-6','topic':'NATIVE_OBSERVATION_MAP','state':'OPEN','detail':'No map from these observational records to native UNT record-surface inputs exists (P53 raw_to_native_map is null). Owned by native-physics work, not by this adapter.','refs':['s1_table:/value/raw_to_native_map']},
 {'id':'OPEN-7','topic':'S2_UNCERTAINTY_AND_MASK','state':'OPEN','detail':'S2 has no measurement uncertainty (unknown, not zero); its mask uses a kinematic window (reduction dependency); 40.14-48.17 kpc annulus is review-flagged (43.66% zero/replaced).','refs':['ledger:U1','ledger:U5','ledger:U6']},
 {'id':'OPEN-8','topic':'S1_ERROR_SEMANTICS','state':'OPEN','detail':'e=1 on HI/stars carries ReadMe Note 3 "upper limit" (quarantined); e=0 is literal with unresolved meaning; no replacement errors.','refs':['ledger:U9','ledger:U10']},
 {'id':'OPEN-9','topic':'QUERY_TO_SOURCE_GRID','state':'OPEN','detail':'Queries are emitted separately. No mapping, interpolation or extrapolation from source grids to query radii is performed.','refs':[]},
 {'id':'OPEN-10','topic':'PRIMARY_CONVERSION_VERIFICATION','state':'OPEN','detail':'Numeric conversion values (helium 1.36, X_CO, CO line ratio, stellar M/L relation, S2 working-plane orientation) are SECONDARY or PROGRAM-DECLARED; only "Including helium" is primary-stated (Leroy ReadMe Note 2). Carry rules unchanged; primary verification pending.','refs':['crosswalk_correction:/corrections']}]
RATIONAL=re.compile(r'^-?\d+(/[1-9]\d*)?$');DECIMAL=re.compile(r'^\d+(\.\d+)?$');QID=re.compile(r'^NGC3198-Q(\d{2})$')
class Fail(Exception):pass
def sha(b):return hashlib.sha256(b).hexdigest()
def load(key):
 p,h=INPUTS[key];b=Path(p).read_bytes()
 if sha(b)!=h:raise Fail('E_PIN_'+key)
 try:return json.loads(b),{'file':p,'sha256':h,'bytes':len(b)}
 except ValueError:raise Fail('E_JSON_'+key)
def need(o,k,code,t=None):
 if not isinstance(o,dict) or k not in o:raise Fail(code)
 v=o[k]
 if t is not None and (type(v) is bool and t is not bool or not isinstance(v,t)):raise Fail(code+'_TYPE')
 return v
def num(x):return type(x) in (int,float) and math.isfinite(x)
def queries(m,pin):
 rows=need(m,'rows','E_Q_ROWS',list)
 if len(rows)!=N_QUERIES:raise Fail('E_Q_COUNT')
 out=[];seen=set();prev=None
 for i,r in enumerate(rows):
  q=need(r,'query_id','E_Q_ID',str);rt=need(r,'Rad_text','E_Q_RAD',str);u=need(r,'Rad_unit','E_Q_UNIT',str)
  if q in seen:raise Fail('E_Q_DUPLICATE')
  seen.add(q)
  mq=QID.match(q)
  if not mq or int(mq.group(1))!=i+1:raise Fail('E_Q_ID_ORDER')
  if u!='kpc':raise Fail('E_Q_UNIT_VALUE')
  if not DECIMAL.match(rt) or not float(rt)>0:raise Fail('E_Q_RAD_DOMAIN')
  if prev is not None and not float(rt)>prev:raise Fail('E_Q_RAD_ORDER')
  prev=float(rt)
  out.append({'query_id':q,'Rad_text':rt,'Rad_unit':u,'pointer':'/rows/%d'%i})
 return {'provenance':pin,'items':out,'note':'radius metadata only; not mapped to any source grid'}
def s1(t,pin):
 if need(t,'status','E_S1_STATUS',str)!='RETURN':raise Fail('E_S1_STATUS_VALUE')
 v=need(t,'value','E_S1_VALUE',dict)
 if need(v,'representation','E_S1_REPR',str)!='MASS_SURFACE_DENSITY':raise Fail('E_S1_REPR_VALUE')
 rows=need(v,'rows','E_S1_ROWS',list)
 if len(rows)!=N_S1:raise Fail('E_S1_COUNT')
 out=[];prev=None;lines=[]
 for i,r in enumerate(rows):
  ln=need(r,'original_line_number','E_S1_LINE',int);lines.append(ln)
  rk=need(r,'radius_kpc','E_S1_RADIUS',str)
  if not RATIONAL.match(rk):raise Fail('E_S1_RADIUS_FORMAT')
  a,_,b=rk.partition('/');rv=int(a)/(int(b) if b else 1)
  if not rv>0 or (prev is not None and not rv>prev):raise Fail('E_S1_RADIUS_DOMAIN')
  prev=rv
  if need(r,'units','E_S1_UNITS',str)!='Msun/pc^2':raise Fail('E_S1_UNITS_VALUE')
  conv={k:need(r,k,'E_S1_CONV_'+k) for k in ('gas_helium','helium_multiplier_applied','stellar_ML_applied_again')}
  if conv!={'gas_helium':'ALREADY_INCLUDED','helium_multiplier_applied':False,'stellar_ML_applied_again':False}:raise Fail('E_S1_CONV_VALUE')
  comps={}
  for c in ('HI','H2','stars'):
   e=need(r,c,'E_S1_'+c,dict)
   val=need(e,'published_value','E_S1_'+c+'_VALUE');err=need(e,'published_error_field','E_S1_'+c+'_ERR');interp=need(e,'interpretation','E_S1_'+c+'_INTERP',str)
   if interp=='MISSING':
    if val is not None or err is not None:raise Fail('E_S1_MISSING_NOT_NULL')
    kind='MISSING'
   else:
    if not (isinstance(val,str) and RATIONAL.match(val) and isinstance(err,str) and RATIONAL.match(err)):raise Fail('E_S1_LITERAL_FORMAT')
    if err.startswith('-'):raise Fail('E_S1_NEGATIVE_ERROR')
    if err=='1' and c in ('HI','stars'):kind='PUBLISHED_FIELD_1_NOTE3_UPPER_LIMIT_MARKER_QUARANTINED'
    elif err=='0':kind='LITERAL_ZERO_MEANING_UNRESOLVED'
    else:kind='PUBLISHED_RMS_MEASUREMENT_ERROR'
   if c=='H2' and i<10 and interp=='MISSING':raise Fail('E_S1_H2_UNEXPECTED_MISSING')
   comps[c]={'value_literal':val,'error_literal':err,'error_kind':kind,'p53_interpretation':interp,'pointer':'/value/rows/%d/%s'%(i,c)}
  out.append({'row_index':i,'original_line_number':ln,'radius_kpc_literal':rk,'radius_pointer':'/value/rows/%d/radius_kpc'%i,'conventions':conv,'components':comps})
 if lines!=list(S1_LINES):raise Fail('E_S1_LINE_ORDER')
 return {'provenance':pin,'literal_format':'exact rational strings as recorded by P53 (e.g. "102/5"); not converted','units':'Msun/pc^2',
  'table_level':{'whole_table_sha256':need(v,'whole_table_sha256','E_S1_TABLE_SHA',str),'whole_covariance':v.get('whole_covariance'),'source_selected':v.get('source_selected'),'raw_to_native_map':v.get('raw_to_native_map')},
  'unknown_uncertainty':'ring-to-ring covariance and conversion systematics (X_CO, line ratio, M/L) are unknown; not zero','rows':out}
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
   if need(p,'width_arcsec','E_S2_WIDTH')!=w:raise Fail('E_S2_WIDTH_VALUE')
   comp=arr(p,'complete_by_conservative_chord_bound',n,'E_S2_COMPLETE','bool')
   lo=arr(p,'r_lo_kpc',n,'E_S2_RLO','never');hi=arr(p,'r_hi_kpc',n,'E_S2_RHI','never')
   if lo[0]!=0 or any(not hi[j]>lo[j] for j in range(n)) or any(abs(hi[j]-lo[j+1])>1e-9*max(1,hi[j]) for j in range(n-1)):raise Fail('E_S2_GRID')
   if any(comp[j+1] and not comp[j] for j in range(n-1)):raise Fail('E_S2_COMPLETE_NOT_PREFIX')
   prof={'width_arcsec':w,'n_bins':n}
   for k,kind in S2_PROFILE_ARRAYS.items():prof[k]={'kind':kind,'pointer':base+'/'+k,'values':p[k]}
   gs=need(p,'groups','E_S2_GROUPS',dict);prof['groups']={}
   for g in GROUPS:
    gd=need(gs,g,'E_S2_GROUP_'+g,dict);prof['groups'][g]={}
    for f,(kind,rule) in S2_FIELDS.items():
     prof['groups'][g][f]={'kind':kind,'null_rule':rule,'pointer':base+'/groups/%s/%s'%(g,f),'values':arr(gd,f,n,'E_S2_FIELD_'+f,rule,comp)}
   po[pk]=prof
  out.append({'order_index':oi,'subpixels_per_axis':ORDERS[oi],'pointer':'/orders/%d'%oi,'profiles':po})
 return {'provenance':pin,'interpretation':{'value':need(d,'interpretation','E_S2_INTERP',str),'pointer':'/interpretation'},'settings':settings,'pixel_categories':pix,'orders':out,
  'measurement_uncertainty':{'state':'UNKNOWN','note':'no noise/error product in the release; not zero; the descriptive scatter field is not a measurement error'}}
def conventions(cw,pin,corr,cpin):
 src=need(cw,'sources','E_CW_SOURCES',dict);out={}
 for sid,keys in CROSSWALK_CONVENTIONS.items():
  s=need(src,sid,'E_CW_'+sid,dict)
  out[sid]={k:{'text':need(s,k,'E_CW_'+sid+'_'+k),'pointer':'/sources/%s/%s'%(sid,k),'corrections':[]} for k in keys}
 if need(need(corr,'corrects','E_CORR_BINDING',dict),'sha256','E_CORR_BINDING',str)!=pin['sha256']:raise Fail('E_CORR_BINDING_SHA')
 other=[];ids=set()
 for i,c in enumerate(need(corr,'corrections','E_CORR_LIST',list)):
  cid=need(c,'id','E_CORR_ID',str);ptr=need(c,'crosswalk_pointer','E_CORR_POINTER',str);need(c,'now','E_CORR_NOW',dict)
  if cid in ids:raise Fail('E_CORR_DUPLICATE')
  ids.add(cid);parts=ptr.strip('/').split('/');o=cw
  for t in parts:
   if not isinstance(o,dict) or t not in o:raise Fail('E_CORR_POINTER_UNRESOLVED')
   o=o[t]
  ref={'id':cid,'crosswalk_pointer':ptr,'correction_pointer':'/corrections/%d'%i,'now':c['now']}
  if len(parts)>=3 and parts[0]=='sources' and parts[1] in out and parts[2] in out[parts[1]]:out[parts[1]][parts[2]]['corrections'].append(ref)
  else:other.append(ref)
 return {'provenance':pin,'correction_provenance':cpin,'items':out,'corrections_for_sources_not_in_bundle':other,
  'rule':'where a correction is attached, its "now" supersedes the crosswalk text for provenance class; the crosswalk text is kept verbatim'}
def main(argv):
 if len(argv)!=2:raise Fail('E_USAGE')
 outp=Path(argv[1])
 if outp.exists():raise Fail('E_OUTPUT_EXISTS')
 m,pm=load('query_manifest');t,pt=load('s1_table');d,pd=load('s2_results');cw,pc=load('crosswalk');cc,pcc=load('crosswalk_correction')
 bundle={'schema':'NGC3198_SOURCE_ONLY_BUNDLE_CANDIDATE_V001','status':'CANDIDATE_NOT_ADMITTED',
  'adapter':{'file':str(Path(__file__)),'sha256':sha(Path(__file__).read_bytes())},
  'scope':'S1 and S2 as separate source records on original grids and conventions; no selection, combination, interpolation, extrapolation, deprojection, unit/helium conversion or query mapping; missing stays null; negative values preserved',
  'element_provenance_rule':'each array element i comes from <file sha256> at pointer + "/" + i',
  'value_kinds':{'PUBLISHED_RMS_MEASUREMENT_ERROR':'S1 published per-ring rms','descriptive_scatter_not_measurement_error':'S2 descriptive scatter','mask_fraction_*':'S2 mask bookkeeping','UNKNOWN':'uncertainty not available; never zero','MISSING':'value absent; null'},
  'queries':queries(m,pm),'sources':{'S1_LEROY_T7':s1(t,pt),'S2_HALOGAS_PLANAR':s2(d,pd)},'conventions':conventions(cw,pc,cc,pcc),'open_issues':OPEN_ISSUES}
 b=(json.dumps(bundle,indent=1,allow_nan=False)+'\n').encode()
 with outp.open('xb') as f:f.write(b)
 print(json.dumps({'status':'CANDIDATE_BUNDLE_WRITTEN','output':str(outp),'sha256':sha(b),'queries':N_QUERIES,'s1_rows':N_S1,'s2_orders':ORDERS}))
 return 0
if __name__=='__main__':
 try:sys.exit(main(sys.argv))
 except Fail as e:print(json.dumps({'status':'FAILED','code':str(e)}));sys.exit(2)
 except Exception as e:print(json.dumps({'status':'FAILED','code':'E_UNEXPECTED','type':type(e).__name__}));sys.exit(3)
