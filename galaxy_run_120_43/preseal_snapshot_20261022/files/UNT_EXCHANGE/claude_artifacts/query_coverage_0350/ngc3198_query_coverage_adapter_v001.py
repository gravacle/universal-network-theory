"""INERT target-free query-coverage adapter V001 for NGC3198 (task 0350). ROOT runs it; the author has run it only on synthetic
bundles (produced by the reviewed source-bundle adapter code from synthetic inputs).

Input: the root-executed source-only bundle (sha-pinned) and root's saved-output review (sha-pinned; must name the bundle
sha). Output: METADATA-ONLY correspondence of each of the 43 literal query radii to
  S1 (Leroy rings): EXACT_SAMPLE_RADIUS | BRACKETED (lower/upper rows) | BELOW_SAMPLED_RANGE | ABOVE_SAMPLED_RANGE, by exact
     rational comparison (fractions.Fraction of the query decimal text and of the stored exact-rational radius strings);
     the referenced rows' component interpretation / error-kind / missingness flags are carried (no values);
  S2 (HALOGAS planar annuli): for EACH subpixel order (4, 8) and width (40, 120 arcsec), the containing annulus under the
     diagnostic convention [r_lo, r_hi) with the final outer edge handled explicitly (a query equal to the final outer edge
     is ON_FINAL_OUTER_EDGE and not assigned; beyond it OUTSIDE_ABOVE), with the edges as stored, exact boundary flags,
     the completeness flag and each group's stored mask/missingness metadata (zero/finite fractions, raw missing-footprint
     fraction, presence of the complete-only effective density). Floating JSON numbers are compared exactly as stored
     (json parse_float=decimal.Decimal, then Fraction); nothing is rounded into a preferred bin.
It does NOT interpolate, resample, choose a source, average orders, convert units or distances, assert physical aperture
coverage, or copy any density, velocity, force or UNT result. Bracketing S1 radii do NOT establish observed coverage of the
intervening aperture. Every query is kept. Settings, unknown measurement uncertainty, source-specific geometry context and
the existing correction/ledger/OPEN references are carried by pointer, not restated or upgraded.
Fail-closed (exit 2, no file): pin mismatch, duplicate JSON keys, NaN/Infinity tokens, non-finite numbers, unexpected schema,
duplicate/unordered query ids, malformed or non-increasing radii, S1 duplicate radii, S2 grid gap/overlap/inverted bins,
length mismatch, missing fields, pre-existing output/candidate.
Publication: the 0348 preserved-candidate lifecycle, reused narrowly from ngc3198_source_bundle_adapter_v005.py
(fc9cdcfa..., reviewed PASS): exclusive <output>.candidate (0444), fsync, re-read, exclusive hard link, guarded post-link
checks; never unlink/move/overwrite. Exits: 0 published, 2 validation, 4 publication (candidate may remain), 3 unexpected,
130 interrupted.
Usage: python3 -I -B ngc3198_query_coverage_adapter_v001.py <new_coverage.json>
"""
import decimal,hashlib,json,os,re,stat,sys
from fractions import Fraction
from pathlib import Path
C1='/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/'
INPUTS={'bundle':(C1+'NGC3198_SOURCE_ONLY_BUNDLE_CANDIDATE_V001.json','62abc88f12cb9da99ea1f1ba27c7eab2454553391984a65e2aa87a155fcc1fc1'),
 'root_review':(C1+'NGC3198_SOURCE_BUNDLE_ROOT_SAVED_OUTPUT_REVIEW_V001.json','43225b2252c4161373208f8584f101651e32e06156b3b21b7ec23fbcd48eabb4')}
N_QUERIES=43;N_S1=23;ORDERS=[4,8];PROFILES={'profile_40arcsec':237,'profile_120arcsec':79};GROUPS=['full','X_negative','X_nonnegative']
MASK_FIELDS=['zero_fraction_of_footprint','finite_fraction_of_footprint','missing_footprint_fraction_raw']
PRESENCE_FIELD='effective_HI_Msun_pc2_complete_only'
COMPONENTS=['HI','H2','stars']
OPEN_REFS=['OPEN-1','OPEN-3','OPEN-4','OPEN-5','OPEN-7','OPEN-8','OPEN-9','OPEN-10']
def _a(p):return re.compile(p,re.ASCII)
DECIMAL=_a(r'\d+(\.\d+)?');RATIONAL=_a(r'-?\d+(/[1-9]\d*)?');QID=_a(r'NGC3198-Q(\d{2})')
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
 p,h=INPUTS[key]
 try:b=Path(p).read_bytes()
 except OSError:raise Fail('E_PIN_'+key+'_MISSING')
 if sha(b)!=h:raise Fail('E_PIN_'+key)
 try:return json.loads(b,object_pairs_hook=_pairs,parse_constant=_const,parse_float=decimal.Decimal),{'file':p,'sha256':h,'bytes':len(b)},b
 except ValueError:raise Fail('E_JSON_'+key)
def need(o,k,code,t=None):
 if not isinstance(o,dict) or k not in o:raise Fail(code)
 v=o[k]
 if t is not None and (type(v) is bool and t is not bool or not isinstance(v,t)):raise Fail(code+'_TYPE')
 return v
def dec(x,code):
 if type(x) is bool or not isinstance(x,(int,decimal.Decimal)) or (isinstance(x,decimal.Decimal) and not x.is_finite()):raise Fail(code)
 return x
def as_stored(x):return {'decimal_as_stored':str(x)} if isinstance(x,decimal.Decimal) else x
def frac(x):return Fraction(x) if isinstance(x,int) else Fraction(x)  # Decimal -> exact Fraction of the stored decimal
def jsonable(o):
 if isinstance(o,decimal.Decimal):
  if not o.is_finite():raise Fail('E_NONFINITE')
  return {'decimal_as_stored':str(o)}
 if isinstance(o,dict):return {k:jsonable(v) for k,v in o.items()}
 if isinstance(o,list):return [jsonable(v) for v in o]
 return o
# ---------------- validation of the bundle ----------------
def queries(b):
 items=need(need(b,'queries','E_Q',dict),'items','E_Q_ITEMS',list)
 if len(items)!=N_QUERIES:raise Fail('E_Q_COUNT')
 out=[];seen=set();prev=None
 for i,q in enumerate(items):
  qid=need(q,'query_id','E_Q_ID',str);rt=need(q,'Rad_text','E_Q_RAD',str);un=need(q,'Rad_unit','E_Q_UNIT',str)
  if qid in seen:raise Fail('E_Q_DUPLICATE')
  seen.add(qid);m=QID.fullmatch(qid)
  if not m or int(m.group(1))!=i+1:raise Fail('E_Q_ID_ORDER')
  if un!='kpc':raise Fail('E_Q_UNIT_VALUE')
  if DECIMAL.fullmatch(rt) is None or not Fraction(rt)>0:raise Fail('E_Q_RAD_DOMAIN')
  if prev is not None and not Fraction(rt)>prev:raise Fail('E_Q_RAD_ORDER')
  prev=Fraction(rt);out.append({'query_id':qid,'Rad_text':rt,'Rad_unit':un,'q':prev,'bundle_pointer':'/queries/items/%d'%i,'source_pointer':need(q,'pointer','E_Q_POINTER',str)})
 return out
def s1_rows(b):
 s1=need(need(b,'sources','E_SOURCES',dict),'S1_LEROY_T7','E_S1',dict);rows=need(s1,'rows','E_S1_ROWS',list)
 if len(rows)!=N_S1:raise Fail('E_S1_COUNT')
 out=[]
 for i,r in enumerate(rows):
  rl=need(need(r,'radius_kpc_literal','E_S1_RADIUS',dict),'value','E_S1_RADIUS_VALUE',str)
  if RATIONAL.fullmatch(rl) is None:raise Fail('E_S1_RADIUS_FORMAT')
  rv=Fraction(rl)
  if not rv>0:raise Fail('E_S1_RADIUS_DOMAIN')
  if out and rv==out[-1]['r']:raise Fail('E_S1_GRID_DUPLICATE')
  if out and rv<out[-1]['r']:raise Fail('E_S1_GRID_ORDER')
  comps={}
  for c in COMPONENTS:
   e=need(need(r,'components','E_S1_COMPONENTS',dict),c,'E_S1_'+c,dict)
   vl=need(need(e,'value_literal','E_S1_'+c+'_VALUE',dict),'value','E_S1_'+c+'_VALUE')
   interp=need(need(e,'p53_interpretation','E_S1_'+c+'_INTERP',dict),'value','E_S1_'+c+'_INTERP',str)
   kind=need(need(e,'error_kind','E_S1_'+c+'_KIND',dict),'adapter_label','E_S1_'+c+'_KIND',str)
   if (vl is None)!=(interp=='MISSING'):raise Fail('E_S1_MISSINGNESS_INCONSISTENT')
   comps[c]={'p53_interpretation':interp,'error_kind':kind,'value_missing':vl is None,'upper_limit_marker':interp=='UPPER_LIMIT_NOTE3',
    'bundle_pointer':'/sources/S1_LEROY_T7/rows/%d/components/%s'%(i,c)}
  out.append({'row_index':i,'r':rv,'radius_literal':rl,'original_line_number':need(need(r,'original_line_number','E_S1_LINE',dict),'value','E_S1_LINE',int),
   'bundle_pointer':'/sources/S1_LEROY_T7/rows/%d/radius_kpc_literal'%i,'components':comps})
 return out
def s2_profiles(b):
 s2=need(need(b,'sources','E_SOURCES',dict),'S2_HALOGAS_PLANAR','E_S2',dict);orders=need(s2,'orders','E_S2_ORDERS',list)
 if [need(need(o,'subpixels_per_axis','E_S2_SUBPIX',dict),'value','E_S2_SUBPIX',int) for o in orders]!=ORDERS:raise Fail('E_S2_ORDER_SET')
 out=[]
 for oi,o in enumerate(orders):
  for pk,n in PROFILES.items():
   p=need(need(o,'profiles','E_S2_PROFILES',dict),pk,'E_S2_PROFILE',dict);base='/sources/S2_HALOGAS_PLANAR/orders/%d/profiles/%s'%(oi,pk)
   lo=[dec(x,'E_S2_EDGE_TYPE') for x in need(need(p,'r_lo_kpc','E_S2_RLO',dict),'values','E_S2_RLO',list)]
   hi=[dec(x,'E_S2_EDGE_TYPE') for x in need(need(p,'r_hi_kpc','E_S2_RHI',dict),'values','E_S2_RHI',list)]
   comp=need(need(p,'complete_by_conservative_chord_bound','E_S2_COMPLETE',dict),'values','E_S2_COMPLETE',list)
   if len(lo)!=n or len(hi)!=n or len(comp)!=n or any(type(x) is not bool for x in comp):raise Fail('E_S2_LENGTH_OR_TYPE')
   if frac(lo[0])!=0:raise Fail('E_S2_GRID_START')
   for j in range(n):
    if not frac(hi[j])>frac(lo[j]):raise Fail('E_S2_GRID_INVERTED')
    if j+1<n:
     if frac(hi[j])<frac(lo[j+1]):raise Fail('E_S2_GRID_GAP')
     if frac(hi[j])>frac(lo[j+1]):raise Fail('E_S2_GRID_OVERLAP')
   groups={}
   for g in GROUPS:
    gd=need(need(p,'groups','E_S2_GROUPS',dict),g,'E_S2_GROUP_'+g,dict);groups[g]={}
    for f in MASK_FIELDS:
     v=need(need(gd,f,'E_S2_FIELD_'+f,dict),'values','E_S2_FIELD_'+f,list)
     if len(v)!=n:raise Fail('E_S2_FIELD_LENGTH')
     groups[g][f]=[dec(x,'E_S2_FIELD_TYPE_'+f) for x in v]
    pv=need(need(gd,PRESENCE_FIELD,'E_S2_FIELD_'+PRESENCE_FIELD,dict),'values','E_S2_FIELD_'+PRESENCE_FIELD,list)
    if len(pv)!=n:raise Fail('E_S2_FIELD_LENGTH')
    groups[g]['effective_density_present']=[x is not None for x in pv]
   out.append({'order_index':oi,'subpixels_per_axis':ORDERS[oi],'profile':pk,'lo':lo,'hi':hi,'complete':comp,'groups':groups,'base':base})
 return out
# ---------------- correspondence ----------------
def s1_correspondence(q,rows):
 def ref(r):return {'row_index':r['row_index'],'original_line_number':r['original_line_number'],'radius_literal':r['radius_literal'],'bundle_pointer':r['bundle_pointer'],'components':r['components']}
 for r in rows:
  if q==r['r']:return {'status':'EXACT_SAMPLE_RADIUS','row':ref(r)}
 if q<rows[0]['r']:return {'status':'BELOW_SAMPLED_RANGE','nearest_sampled_row':ref(rows[0])}
 if q>rows[-1]['r']:return {'status':'ABOVE_SAMPLED_RANGE','nearest_sampled_row':ref(rows[-1])}
 for a,b in zip(rows,rows[1:]):
  if a['r']<q<b['r']:return {'status':'BRACKETED','lower_row':ref(a),'upper_row':ref(b),'note':'two sampled ring radii bracket the query; this does NOT establish observed coverage of the intervening aperture'}
 raise Fail('E_S1_CORRESPONDENCE_INTERNAL')
def s2_correspondence(q,p):
 lo,hi=p['lo'],p['hi'];n=len(lo)
 res={'order_index':p['order_index'],'subpixels_per_axis':p['subpixels_per_axis'],'profile':p['profile'],'convention':'[r_lo, r_hi); final outer edge explicit'}
 if q<frac(lo[0]):res['status']='OUTSIDE_BELOW';return res
 if q==frac(hi[n-1]):res.update(status='ON_FINAL_OUTER_EDGE',final_outer_edge_as_stored=as_stored(hi[n-1]),final_outer_edge_pointer=p['base']+'/r_hi_kpc/values/%d'%(n-1));return res
 if q>frac(hi[n-1]):res.update(status='OUTSIDE_ABOVE',final_outer_edge_as_stored=as_stored(hi[n-1]));return res
 js=[j for j in range(n) if frac(lo[j])<=q<frac(hi[j])]
 if len(js)!=1:raise Fail('E_S2_CORRESPONDENCE_INTERNAL')
 j=js[0]
 res.update(status='IN_ANNULUS',annulus_index=j,inner_edge_as_stored=as_stored(lo[j]),outer_edge_as_stored=as_stored(hi[j]),
  query_equals_inner_edge=q==frac(lo[j]),edge_pointers={'r_lo':p['base']+'/r_lo_kpc/values/%d'%j,'r_hi':p['base']+'/r_hi_kpc/values/%d'%j},
  complete_by_conservative_chord_bound=p['complete'][j],complete_pointer=p['base']+'/complete_by_conservative_chord_bound/values/%d'%j,
  groups={g:{**{f:as_stored(p['groups'][g][f][j]) for f in MASK_FIELDS},'effective_density_present':p['groups'][g]['effective_density_present'][j],
   'pointers':{**{f:p['base']+'/groups/%s/%s/values/%d'%(g,f,j) for f in MASK_FIELDS},'effective_density_present':p['base']+'/groups/%s/%s/values/%d'%(g,PRESENCE_FIELD,j)}} for g in GROUPS})
 return res
def context(b):
 s2=b['sources']['S2_HALOGAS_PLANAR'];s1=b['sources']['S1_LEROY_T7'];cv=need(b,'conventions','E_CONVENTIONS',dict)
 settings={k:{'value_as_stored':as_stored(need(v,'value','E_S2_SETTING')),'bundle_pointer':'/sources/S2_HALOGAS_PLANAR/settings/'+k,'source_pointer':need(v,'pointer','E_S2_SETTING_POINTER',str)} for k,v in need(s2,'settings','E_S2_SETTINGS',dict).items()}
 items=need(cv,'items','E_CONVENTION_ITEMS',dict);geo={}
 for sid in ('S1_LEROY_T7','S2_HALOGAS_C1'):
  for key in ('geometry','radial_coordinate','helium_conversion_state','error_fields','masks','support'):
   it=need(need(items,sid,'E_CONV_'+sid,dict),key,'E_CONV_'+sid+'_'+key,dict)
   geo['%s/%s'%(sid,key)]={'bundle_pointer':'/conventions/items/%s/%s'%(sid,key),'attached_correction_ids':[c.get('id') for c in need(it,'corrections','E_CONV_CORR',list)]}
 oi=need(need(b,'open_issues','E_OPEN',dict),'items','E_OPEN_ITEMS',list);ids=[x.get('id') for x in oi]
 for r in OPEN_REFS:
  if r not in ids:raise Fail('E_OPEN_REF_MISSING')
 return {'s2_settings':settings,'s2_measurement_uncertainty':{'state':need(need(s2,'measurement_uncertainty','E_S2_UNC',dict),'state','E_S2_UNC',str),'bundle_pointer':'/sources/S2_HALOGAS_PLANAR/measurement_uncertainty'},
  's1_unknown_uncertainty':{'bundle_pointer':'/sources/S1_LEROY_T7/unknown_uncertainty'},'s1_table_level':{'bundle_pointer':'/sources/S1_LEROY_T7/table_level'},
  'geometry_and_conversion_context':geo,'open_issue_refs':[{'id':r,'bundle_pointer':'/open_issues/items/%d'%ids.index(r)} for r in OPEN_REFS],
  'radius_convention_note':'S1 ring radii, S2 annulus edges and query radii are compared as the literal kpc numbers each source records; each source keeps its own geometry/distance convention (by reference); no rescaling, deprojection or aperture equivalence is asserted'}
# ---------------- publication (0348 lifecycle, reused from source-bundle adapter V005) ----------------
def candidate_path(outp):return outp.with_name(outp.name+'.candidate')
def publish(outp,b):
 cand=candidate_path(outp);want=sha(b)
 info={'candidate_path':str(cand),'candidate_created':False,'expected_sha256':want,'expected_bytes':len(b),'output_path':str(outp),'output_published':False}
 try:fd=os.open(cand,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
 except FileExistsError:raise PublishFail('E_CANDIDATE_EXISTS',info)
 except OSError as e:info['error']={'type':type(e).__name__,'errno':e.errno};raise PublishFail('E_CANDIDATE_CREATE',info)
 info['candidate_created']=True
 try:
  with os.fdopen(fd,'wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 except OSError as e:info['error']={'type':type(e).__name__,'errno':e.errno};raise PublishFail('E_CANDIDATE_WRITE',info)
 try:cb=cand.read_bytes()
 except OSError as e:info['error']={'type':type(e).__name__,'errno':e.errno};raise PublishFail('E_CANDIDATE_VERIFY',info)
 info['candidate_sha256']=sha(cb);info['candidate_bytes']=len(cb)
 if cb!=b:raise PublishFail('E_CANDIDATE_VERIFY',info)
 try:os.link(cand,outp)
 except FileExistsError:raise PublishFail('E_OUTPUT_EXISTS_AT_PUBLICATION',info)
 except OSError as e:info['error']={'type':type(e).__name__,'errno':e.errno};raise PublishFail('E_PUBLICATION_LINK',info)
 info['output_published']=True
 try:
  dfd=os.open(str(outp.parent),os.O_RDONLY)
  try:os.fsync(dfd)
  finally:os.close(dfd)
 except Exception as e:info['error']={'type':type(e).__name__,'errno':getattr(e,'errno',None)};raise PublishFail('E_DIRECTORY_FSYNC',info)
 try:ob=outp.read_bytes()
 except Exception as e:info['error']={'type':type(e).__name__,'errno':getattr(e,'errno',None)};raise PublishFail('E_OUTPUT_VERIFY',info)
 info['output_sha256']=sha(ob);info['output_bytes']=len(ob)
 if ob!=b:raise PublishFail('E_OUTPUT_VERIFY',info)
 try:same=os.path.samefile(cand,outp)
 except Exception as e:info['error']={'type':type(e).__name__,'errno':getattr(e,'errno',None)};raise PublishFail('E_POST_PUBLICATION_CHECK',info)
 if not same:raise PublishFail('E_OUTPUT_NOT_SAME_FILE',info)
 try:mode=oct(stat.S_IMODE(os.stat(cand).st_mode))
 except Exception as e:info['error']={'type':type(e).__name__,'errno':getattr(e,'errno',None)};raise PublishFail('E_POST_PUBLICATION_CHECK',info)
 return {'candidate':{'path':str(cand),'sha256':info['candidate_sha256'],'bytes':info['candidate_bytes'],'mode':mode,'mode_requested':'0o444'},'output':{'path':str(outp),'sha256':info['output_sha256'],'bytes':info['output_bytes']},'same_file':True}
def main(argv):
 if len(argv)!=2:raise Fail('E_USAGE')
 outp=Path(os.path.abspath(argv[1]))
 if os.path.lexists(outp):raise Fail('E_OUTPUT_EXISTS')
 if os.path.lexists(candidate_path(outp)):raise Fail('E_CANDIDATE_EXISTS')
 b,pb,_=load('bundle');rv,pr,rvb=load('root_review')
 if INPUTS['bundle'][1].encode() not in rvb:raise Fail('E_ROOT_REVIEW_DOES_NOT_NAME_BUNDLE')
 if need(b,'schema','E_SCHEMA',str)!='NGC3198_SOURCE_ONLY_BUNDLE_CANDIDATE_V002':raise Fail('E_SCHEMA_VALUE')
 qs=queries(b);rows=s1_rows(b);profs=s2_profiles(b);ctx=context(b)
 out_q=[]
 for q in qs:
  out_q.append({'query_id':q['query_id'],'Rad_text':q['Rad_text'],'Rad_unit':q['Rad_unit'],'bundle_pointer':q['bundle_pointer'],'source_pointer':q['source_pointer'],
   'S1':s1_correspondence(q['q'],rows),'S2':[s2_correspondence(q['q'],p) for p in profs]})
 res={'schema':'NGC3198_QUERY_SOURCE_COVERAGE_CANDIDATE_V001','status':'CANDIDATE_METADATA_ONLY',
  'adapter':{'file':os.path.abspath(__file__),'sha256':sha(Path(os.path.abspath(__file__)).read_bytes())},
  'inputs':{'bundle':pb,'root_review':pr},'scope':'metadata-only correspondence of literal query radii to stored source grids; no interpolation, resampling, source choice, order averaging, unit/distance conversion, aperture assertion, density, velocity, force or UNT result',
  'comparison':{'queries':'Fraction(Rad_text)','S1':'Fraction(exact rational radius string)','S2':'Fraction(Decimal(edge as stored in the bundle JSON))','rounding':'none'},
  'labels':{'S1':['EXACT_SAMPLE_RADIUS','BRACKETED','BELOW_SAMPLED_RANGE','ABOVE_SAMPLED_RANGE'],'S2':['IN_ANNULUS','ON_FINAL_OUTER_EDGE','OUTSIDE_ABOVE','OUTSIDE_BELOW'],'S2_flags':['query_equals_inner_edge'],
   'S1_component_flags':['p53_interpretation','error_kind','value_missing','upper_limit_marker']},
  'queries':out_q,'context':ctx}
 data=(json.dumps(jsonable(res),indent=1,allow_nan=False)+'\n').encode()
 PHASE[0]='PUBLICATION'
 pub=publish(outp,data)
 print(json.dumps({'status':'COVERAGE_WRITTEN','phase':'PUBLISHED',**pub,'queries':len(out_q)}))
 return 0
if __name__=='__main__':
 try:sys.exit(main(sys.argv))
 except Fail as e:print(json.dumps({'status':'FAILED_VALIDATION','code':str(e),'phase':'VALIDATION','candidate_written':False,'success_claimed':False}));sys.exit(2)
 except PublishFail as e:print(json.dumps({'status':'FAILED_PUBLICATION','code':e.code,'phase':'PUBLICATION','publication':e.info,'candidate_retained_if_created':True,'success_claimed':False}));sys.exit(4)
 except KeyboardInterrupt:print(json.dumps({'status':'FAILED_INTERRUPTED','phase':PHASE[0],'candidate_may_remain':PHASE[0]=='PUBLICATION','output_may_exist':PHASE[0]=='PUBLICATION','success_claimed':False}));sys.exit(130)
 except Exception as e:print(json.dumps({'status':'FAILED','code':'E_UNEXPECTED','type':type(e).__name__,'phase':PHASE[0],'candidate_may_remain':PHASE[0]=='PUBLICATION','output_may_exist':PHASE[0]=='PUBLICATION','success_claimed':False}));sys.exit(3)
