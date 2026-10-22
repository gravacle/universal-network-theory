"""Synthetic-only tests for ngc3198_query_coverage_adapter_v001.py (task 0350). The base bundle is a SYNTHETIC bundle produced by
the reviewed source-bundle adapter code (V005 test suite, synthetic inputs); no real bundle is read. Test copies differ from the
deliverable by one inserted INPUTS override line. Work dir: argv[1] or a fresh temp dir. Never deletes anything."""
import copy,decimal,hashlib,json,os,subprocess,sys,tempfile
from fractions import Fraction
from pathlib import Path
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/query_coverage_0350/ngc3198_query_coverage_adapter_v001.py')
BASE=Path(__file__).resolve().parent/'base_synthetic_bundle.json'
T=Path(sys.argv[1]) if len(sys.argv)>1 else Path(tempfile.mkdtemp(prefix='qc_tests_'));T.mkdir(parents=True,exist_ok=True)
SRC=A.read_text();ANCHOR='N_QUERIES=43;';assert SRC.count(ANCHOR)==1
sha=lambda b:hashlib.sha256(b).hexdigest()
BASE_RAW=BASE.read_bytes();BD=json.loads(BASE_RAW,parse_float=decimal.Decimal)
def dumps(o):return json.dumps(o,default=lambda x:float(x) if isinstance(x,decimal.Decimal) else None).encode()
res=[];N=[0]
def case(name,ok,detail=''):res.append((name,bool(ok),detail));print(('PASS ' if ok else 'FAIL ')+name+(' | '+detail if detail else ''))
def build(tag,mut=None,raw=None,review=None):
    N[0]+=1;d=T/('%02d_%s'%(N[0],tag));d.mkdir()
    if raw is not None:bb=raw
    elif mut is None:bb=BASE_RAW
    else:
        o=json.loads(BASE_RAW);mut(o);bb=json.dumps(o).encode()
    (d/'bundle.json').write_bytes(bb)
    rv=review if review is not None else json.dumps({'kind':'SYNTHETIC_ROOT_REVIEW','bundle_sha256':sha(bb)}).encode()
    (d/'review.json').write_bytes(rv)
    inputs={'bundle':(str(d/'bundle.json'),sha(bb)),'root_review':(str(d/'review.json'),sha(rv))}
    ad=d/'adapter.py';ad.write_text(SRC.replace(ANCHOR,'INPUTS='+repr(inputs)+'  # TEST-ONLY override\n'+ANCHOR));return d,ad,bb
def run(d,ad,name='coverage.json'):
    r=subprocess.run([sys.executable,'-I','-B',str(ad),str(d/name)],capture_output=True,text=True)
    j=json.loads(r.stdout.strip().splitlines()[-1]);o=json.loads((d/name).read_text()) if (d/name).exists() else None
    return r.returncode,j,o
def keys(o,acc):
    if isinstance(o,dict):
        for k,v in o.items():acc.add(k);keys(v,acc)
    elif isinstance(o,list):
        for v in o:keys(v,acc)
    return acc
def ptr(o,p):
    for t in p.strip('/').split('/'):o=o[int(t)] if isinstance(o,list) else o[t]
    return o
# T1 valid
d,ad,bb=build('valid');rc,j,o=run(d,ad)
case('T1 valid -> exit 0, 43 queries, S1 + 4 S2 entries each, candidate retained (same file)',rc==0 and len(o['queries'])==43 and all(len(q['S2'])==4 for q in o['queries']) and os.path.samefile(d/'coverage.json',d/'coverage.json.candidate'),json.dumps(j)[:120])
q1=o['queries'][0]
case('T1 S1 bracket with explicit non-coverage note (query 0.50 between 3/10 and 10/10)',q1['S1']['status']=='BRACKETED' and q1['S1']['lower_row']['radius_literal']=='3/10' and q1['S1']['upper_row']['radius_literal']=='10/10' and 'does NOT establish' in q1['S1']['note'])
case('T1 S1 above range for queries beyond last ring (15.7)',all(q['S1']['status']=='ABOVE_SAMPLED_RANGE' for q in o['queries'] if Fraction(q['Rad_text'])>Fraction(157,10)))
q2=o['queries'][1]
case('T1 upper-limit flag carried (row 2 stars UPPER_LIMIT_NOTE3) without value',q2['S1']['upper_row']['row_index']==2 and q2['S1']['upper_row']['components']['stars']['upper_limit_marker'] is True)
q8=[q for q in o['queries'] if q['Rad_text']=='7.50'][0]
case('T1 missing H2 carried as value_missing true (no zero)',q8['S1']['lower_row']['row_index']==10 and q8['S1']['lower_row']['components']['H2']['value_missing'] is True and q8['S1']['lower_row']['components']['H2']['p53_interpretation']=='MISSING')
forbidden={'mass_Msun','positive_mass_Msun','negative_mass_Msun','nominal_disk_area_pc2','plane_pc2','value_literal','error_literal','effective_HI_Msun_pc2_complete_only','effective_HI_plus_He_Msun_pc2_complete_only','cosi_times_finite_sky_weighted_LOS_sigma_rms_Msun_pc2_not_measurement_error'}
ks=keys(o,set());txt=(d/'coverage.json').read_text()
s1vals={r['components'][c]['value_literal']['value'] for r in BD['sources']['S1_LEROY_T7']['rows'] for c in ('HI','H2','stars')}-{None}
case('T1 no density/value fields: forbidden keys absent and no S1 value literal appears',not (ks&forbidden) and not any('"%s"'%v in txt for v in s1vals),str(ks&forbidden))
# provenance: every S2 edge/mask pointer resolves to the stored value (as stored)
bad=0;cnt=0
for q in o['queries']:
    for e in q['S2']:
        if e['status']!='IN_ANNULUS':continue
        for k,pk in (('inner_edge_as_stored','r_lo'),('outer_edge_as_stored','r_hi')):
            v=ptr(BD,e['edge_pointers'][pk]);cnt+=1;bad+=str(v)!=e[k]['decimal_as_stored']
        for g,gv in e['groups'].items():
            for f in ('zero_fraction_of_footprint','finite_fraction_of_footprint','missing_footprint_fraction_raw'):
                v=ptr(BD,gv['pointers'][f]);cnt+=1;bad+=str(v)!=gv[f]['decimal_as_stored']
            cnt+=1;bad+=(ptr(BD,gv['pointers']['effective_density_present']) is not None)!=gv['effective_density_present']
        cnt+=1;bad+=ptr(BD,e['complete_pointer'])!=e['complete_by_conservative_chord_bound']
case('T1 every S2 edge/mask/presence/completeness value equals the bundle value at its pointer (decimal as stored)',bad==0 and cnt>1000,'%d checked, %d bad'%(cnt,bad))
case('T1 context carried by pointer: settings as stored, uncertainty UNKNOWN, OPEN refs resolve, geometry correction ids',o['context']['s2_measurement_uncertainty']['state']=='UNKNOWN' and all(ptr(BD,x['bundle_pointer'])['id']==x['id'] for x in o['context']['open_issue_refs']) and 'S2_HALOGAS_C1/geometry' in o['context']['geometry_and_conversion_context'] and o['context']['s2_settings']['inclination_deg']['value_as_stored']=={'decimal_as_stored':'72.0'})
# exact boundary + no rounding
lo1=str(BD['sources']['S2_HALOGAS_PLANAR']['orders'][0]['profiles']['profile_40arcsec']['r_lo_kpc']['values'][1])
def set_q(idx,val):
    def m(b):b['queries']['items'][idx]['Rad_text']=val
    return m
d,ad,bb=build('inner_edge_exact',mut=set_q(3,lo1));rc,j,o=run(d,ad)
e=[x for x in o['queries'][3]['S2'] if x['order_index']==0 and x['profile']=='profile_40arcsec'][0]
case('B1 query exactly on a stored inner edge -> that annulus, query_equals_inner_edge true',rc==0 and e['annulus_index']==1 and e['query_equals_inner_edge'] is True and e['inner_edge_as_stored']=={'decimal_as_stored':lo1},lo1)
below=str(decimal.Decimal(lo1)-decimal.Decimal('1e-10'))
d,ad,bb=build('just_below_edge',mut=set_q(3,below));rc,j,o=run(d,ad)
e=[x for x in o['queries'][3]['S2'] if x['order_index']==0 and x['profile']=='profile_40arcsec'][0]
case('B2 query 1e-10 below an edge -> lower annulus, not flagged, not rounded',rc==0 and e['annulus_index']==0 and e['query_equals_inner_edge'] is False,below)
hiN=str(BD['sources']['S2_HALOGAS_PLANAR']['orders'][1]['profiles']['profile_120arcsec']['r_hi_kpc']['values'][-1])
d,ad,bb=build('final_outer_edge',mut=set_q(42,hiN));rc,j,o=run(d,ad)
e=[x for x in o['queries'][42]['S2'] if x['order_index']==1 and x['profile']=='profile_120arcsec'][0]
case('B3 query equal to final outer edge -> ON_FINAL_OUTER_EDGE, not assigned',rc==0 and e['status']=='ON_FINAL_OUTER_EDGE' and 'annulus_index' not in e,hiN)
d,ad,bb=build('outside_above',mut=set_q(42,'9999.0'));rc,j,o=run(d,ad)
case('B4 query beyond all edges -> OUTSIDE_ABOVE in all 4 S2 entries; S1 ABOVE',rc==0 and all(e['status']=='OUTSIDE_ABOVE' for e in o['queries'][42]['S2']) and o['queries'][42]['S1']['status']=='ABOVE_SAMPLED_RANGE')
d,ad,bb=build('s1_exact',mut=set_q(0,'0.30'));rc,j,o=run(d,ad)
case('B5 query equal to a ring radius (0.30 == 3/10) -> EXACT_SAMPLE_RADIUS',rc==0 and o['queries'][0]['S1']['status']=='EXACT_SAMPLE_RADIUS' and o['queries'][0]['S1']['row']['row_index']==0)
d,ad,bb=build('s1_below',mut=set_q(0,'0.10'));rc,j,o=run(d,ad)
case('B6 query below first ring -> BELOW_SAMPLED_RANGE',rc==0 and o['queries'][0]['S1']['status']=='BELOW_SAMPLED_RANGE')
# failures
def expect(tag,code,**kw):
    pre=kw.pop('pre',None);d,ad,bb=build(tag,**kw)
    if pre:pre(d)
    rc,j,o=run(d,ad)
    ok=rc==2 and j.get('code')==code and j.get('status')=='FAILED_VALIDATION' and (tag=='output_exists' or o is None) and not (d/'coverage.json.candidate').exists()
    case('F '+tag+' -> '+code,ok,json.dumps(j)[:150])
def dupq(b):b['queries']['items'][5]['query_id']='NGC3198-Q05'
expect('duplicate_query','E_Q_DUPLICATE',mut=dupq)
d,ad,bb=build('bad_bundle_pin');(d/'bundle.json').write_bytes(bb+b' ');rc,j,o=run(d,ad)
case('F bad bundle pin -> E_PIN_bundle',rc==2 and j['code']=='E_PIN_bundle' and o is None)
expect('review_not_naming_bundle','E_ROOT_REVIEW_DOES_NOT_NAME_BUNDLE',review=b'{"kind":"x","bundle_sha256":"0000"}')
d,ad,bb=build('bad_review_pin');(d/'review.json').write_bytes(b'tampered');rc,j,o=run(d,ad)
case('F bad review pin -> E_PIN_root_review',rc==2 and j['code']=='E_PIN_root_review' and o is None)
expect('nan_token','E_JSON_NONFINITE_TOKEN',raw=BASE_RAW.replace(b'"inclination_deg": {\n     "value": 72.0',b'"inclination_deg": {\n     "value": NaN',1) if b'"inclination_deg": {\n     "value": 72.0' in BASE_RAW else json.dumps({'x':float('nan')}).encode())
expect('duplicate_json_key','E_JSON_DUPLICATE_KEY',raw=b'{"schema":"a","schema":"b"}')
def gap(b):
    p=b['sources']['S2_HALOGAS_PLANAR']['orders'][1]['profiles']['profile_40arcsec'];p['r_hi_kpc']['values'][10]-=1e-6
expect('grid_gap','E_S2_GRID_GAP',mut=gap)
def overlap(b):
    p=b['sources']['S2_HALOGAS_PLANAR']['orders'][0]['profiles']['profile_120arcsec'];p['r_hi_kpc']['values'][5]+=1e-6
expect('grid_overlap','E_S2_GRID_OVERLAP',mut=overlap)
def s1dup(b):b['sources']['S1_LEROY_T7']['rows'][5]['radius_kpc_literal']['value']=b['sources']['S1_LEROY_T7']['rows'][4]['radius_kpc_literal']['value']
expect('s1_duplicate_radius','E_S1_GRID_DUPLICATE',mut=s1dup)
def miss_inc(b):b['sources']['S1_LEROY_T7']['rows'][3]['components']['HI']['value_literal']['value']=None
expect('missingness_inconsistent','E_S1_MISSINGNESS_INCONSISTENT',mut=miss_inc)
def edge_str(b):b['sources']['S2_HALOGAS_PLANAR']['orders'][0]['profiles']['profile_40arcsec']['r_lo_kpc']['values'][3]='2.0'
expect('edge_not_numeric','E_S2_EDGE_TYPE',mut=edge_str)
def schema(b):b['schema']='OTHER'
expect('schema_mismatch','E_SCHEMA_VALUE',mut=schema)
def open_missing(b):b['open_issues']['items']=[x for x in b['open_issues']['items'] if x['id']!='OPEN-5']
expect('open_ref_missing','E_OPEN_REF_MISSING',mut=open_missing)
def unorder(b):b['queries']['items'][4]['Rad_text']='1.00'
expect('query_order','E_Q_RAD_ORDER',mut=unorder)
def badq(b):b['queries']['items'][0]['Rad_text']='0.50\n'
expect('query_trailing_newline','E_Q_RAD_DOMAIN',mut=badq)
def lenmis(b):b['sources']['S2_HALOGAS_PLANAR']['orders'][0]['profiles']['profile_40arcsec']['groups']['full']['zero_fraction_of_footprint']['values'].pop()
expect('mask_length_mismatch','E_S2_FIELD_LENGTH',mut=lenmis)
d,ad,bb=build('output_exists');(d/'coverage.json').write_bytes(b'PRE');rc,j,o=run(d,ad) if False else (None,None,None)
r=subprocess.run([sys.executable,'-I','-B',str(ad),str(d/'coverage.json')],capture_output=True,text=True);j=json.loads(r.stdout.strip().splitlines()[-1])
case('F output exists -> E_OUTPUT_EXISTS, bytes untouched, no candidate',r.returncode==2 and j['code']=='E_OUTPUT_EXISTS' and (d/'coverage.json').read_bytes()==b'PRE' and not (d/'coverage.json.candidate').exists())
src=A.read_text()
case('S static: no unlink/remove/rename/replace/rmtree/truncate/O_TRUNC/write_bytes/write_text/shutil',not any(t in src for t in ('os.unlink(','os.remove(','os.rename(','os.replace(','rmtree(','.unlink(','O_TRUNC','truncate(','write_bytes(','write_text(','shutil')))
print('WORKDIR',T)
print('SUMMARY',sum(ok for _,ok,_ in res),'/',len(res),'passed')
