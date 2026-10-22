"""Synthetic-only tests for ngc3198_source_bundle_adapter_v003.py (task 0348): the full V002 suite re-pointed at V003 plus
publication-lifecycle tests. Never deletes anything; counts files before/after. Reads no real source; case R reads only
Claude-authored metadata (crosswalk, 0346 correction, ledger). Work files go to a fresh temp dir (or argv[1])."""
import hashlib,json,os,random,re,sys,tempfile
from pathlib import Path
import subprocess
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_adapter_write_0348/ngc3198_source_bundle_adapter_v003.py')
T=Path(sys.argv[1]) if len(sys.argv)>1 else Path(tempfile.mkdtemp(prefix='adapter_v002_tests_'))
T.mkdir(parents=True,exist_ok=True)
SRC=A.read_text();SENT='SENTINEL_VELOCITY_RESPONSE_777';ANCHOR='N_QUERIES=43;'
assert SRC.count(ANCHOR)==1  # test copies differ from the deliverable only by one inserted INPUTS override line
sha=lambda b:hashlib.sha256(b).hexdigest()
def manifest():
    return {'schema':'x','rows':[{'data_row_index':i+1,'query_id':'NGC3198-Q%02d'%(i+1),'source_line_number':i+4,'Rad_text':'%.2f'%(0.5+i),'Rad_unit':'kpc','Vobs':SENT,'errV':SENT} for i in range(43)],'reference_distance':{'v':SENT},'Vflat':SENT}
def s1():
    rows=[]
    for i in range(23):
        h2=({'Gaussian_likelihood_assumed':False,'interpretation':'VALUE_WITH_PUBLISHED_RMS','published_error_field':'9/10','published_value':'-1/5' if i==3 else '51/2','v':SENT} if i<10 else
            {'Gaussian_likelihood_assumed':False,'interpretation':'MISSING','published_error_field':None,'published_value':None})
        st_err='1' if i==2 else ('0' if i in (16,18,19,20) else '3/10')
        rows.append({'H2':h2,'HI':{'Gaussian_likelihood_assumed':False,'interpretation':'VALUE_WITH_PUBLISHED_RMS','published_error_field':'2/5','published_value':'%d/5'%(20+i)},
          'stars':{'Gaussian_likelihood_assumed':False,'interpretation':'UPPER_LIMIT_NOTE3' if i==2 else 'VALUE_WITH_PUBLISHED_RMS','published_error_field':st_err,'published_value':'%d/10'%(900-30*i),'v_rot':SENT},
          'gas_helium':'ALREADY_INCLUDED','helium_multiplier_applied':False,'original_line_number':320+i,'radius_kpc':'%d/10'%(3+7*i),'radius_over_r25':'1/100','raw_line_ascii':SENT,'stellar_ML_applied_again':False,'units':'Msun/pc^2','Vobs':SENT})
    return {'status':'RETURN','value':{'physical_prediction_released':False,'raw_to_native_map':None,'representation':'MASS_SURFACE_DENSITY','rows':rows,'source_selected':False,'whole_covariance':None,'whole_table_sha256':'f'*64,'response':SENT}}
F=['mass_Msun','positive_mass_Msun','negative_mass_Msun','effective_HI_Msun_pc2_complete_only','effective_HI_plus_He_Msun_pc2_complete_only','zero_fraction_of_footprint','finite_fraction_of_footprint','positive_fraction_of_footprint','negative_fraction_of_footprint','nominal_disk_area_pc2','plane_pc2','cosi_times_finite_sky_weighted_LOS_sigma_rms_Msun_pc2_not_measurement_error','missing_footprint_fraction_raw','los_sigma2_sky_integral']
def s2():
    orders=[]
    for sp in (4,8):
        o={'subpixels_per_axis':sp,'direct_map_totals':{'mass_Msun':1.0,'v':SENT}}
        for pk,w,n,nc in (('profile_40arcsec',40.0,237,51),('profile_120arcsec',120.0,79,17)):
            step=w*0.0669;comp=[j<nc for j in range(n)]
            p={'width_arcsec':w,'r_lo_kpc':[j*step for j in range(n)],'r_hi_kpc':[(j+1)*step for j in range(n)],'complete_by_conservative_chord_bound':comp,'half_effective_HI_difference_complete_only':[SENT]*n,'groups':{}}
            for g in ('full','X_negative','X_nonnegative'):
                gd={}
                for f in F:
                    if f.startswith('effective'):gd[f]=[(5.0-0.01*j) if comp[j] else None for j in range(n)]
                    elif f=='negative_mass_Msun':gd[f]=[-(j%3)*1.5 for j in range(n)]
                    elif f=='missing_footprint_fraction_raw':gd[f]=[(-1e-6 if j%4==0 else 0.0) for j in range(n)]
                    elif f.startswith('cosi'):gd[f]=[None if j in (n-1,n-2) else 0.1*j for j in range(n)]
                    elif f=='los_sigma2_sky_integral':gd[f]=[SENT]*n
                    else:gd[f]=[float(j)+0.25 for j in range(n)]
                gd['velocity_SENTINEL_field']=[SENT]*n
                p['groups'][g]=gd
            o[pk]=p
        orders.append(o)
    st={'HI_atoms_cm2_per_Msun_pc2':1.25e20,'bin_arcsec':40.0,'center_dec_deg':45.5,'center_ra_deg':154.9,'center_source':'synthetic','chunk_rows':4,'column_conversion_from_history':9.3e20,'distance_pc':13800000.0,'geometry':'synthetic plane','helium_factor':1.36,'inclination_deg':72.0,'orientation_source':'synthetic','pa_deg':215.0,'rebin':3,'subsamples':[4,8],'vsys_kms':SENT}
    return {'status':'COMPLETE','failed_checks':[],'passed_checks':63,'interpretation':'synthetic retained signal','settings':st,'pixel_categories':{'finite':100,'negative':2,'nonfinite':0,'positive':30,'total':100,'zero_or_replaced_mask':68},'orders':orders,'newton_force':SENT}
K1=['tracers','radial_coordinate','resolution','geometry','units','helium_conversion_state','masks','error_fields','support'];K2=['tracer','radial_coordinate','geometry','units','helium_conversion_state','masks','error_fields','support','resolution']
def crosswalk():return {'sources':{'S1_LEROY_T7':{k:'s1 '+k for k in K1}|{'helium_conversion_state':{'HI':'h','H2':'h2'},'vflat':SENT},'S2_HALOGAS_C1':{k:'s2 '+k for k in K2},'S3_SPARC_SFB':{'helium_conversion_state':'x'}},'rotation':SENT}
def ledger():return {'items':[{'id':'U%d'%(i+1),'state':'x'} for i in range(19)],'Vobs':SENT}
def correction(cw_sha,cw_file):
    return {'corrects':{'file':cw_file,'sha256':cw_sha,'unchanged':True},'Vobs':SENT,'corrections':[
      {'id':'C1','crosswalk_pointer':'/sources/S1_LEROY_T7/helium_conversion_state/HI','now':{'state':'SECONDARY test','evidence':[{'file':'f','lines':'75'}]},'v_rot':SENT},
      {'id':'C6','crosswalk_pointer':'/sources/S2_HALOGAS_C1/geometry','now':{'state':'DECLARED test'}},
      {'id':'C7','crosswalk_pointer':'/sources/S3_SPARC_SFB/helium_conversion_state','now':{'state':'other'}}]}
res=[]
def case(name,ok,detail=''):res.append((name,bool(ok),detail));print(('PASS ' if ok else 'FAIL ')+name+(' | '+detail if detail else ''))
N=[0]
def build(tag,mods=None,raw=None,cmods=None):
    N[0]+=1;d=T/('%02d_%s'%(N[0],tag));d.mkdir()
    objs={'query_manifest':manifest(),'s1_table':s1(),'s2_results':s2(),'crosswalk':crosswalk(),'ledger':ledger()}
    if mods:mods(objs)
    files={};inputs={}
    for k,o in objs.items():
        f=d/(k+'.json');b=(raw or {}).get(k) or json.dumps(o).encode();f.write_bytes(b);files[k]=f;inputs[k]=(str(f),sha(b))
    cc=correction(inputs['crosswalk'][1],inputs['crosswalk'][0])
    if cmods:cmods(cc)
    f=d/'crosswalk_correction.json';b=(raw or {}).get('crosswalk_correction') or json.dumps(cc).encode();f.write_bytes(b);files['crosswalk_correction']=f;inputs['crosswalk_correction']=(str(f),sha(b));objs['crosswalk_correction']=cc
    s=SRC.replace(ANCHOR,'INPUTS='+repr(inputs)+'  # TEST-ONLY override\n'+ANCHOR)
    ad=d/'adapter.py';ad.write_text(s);return d,ad,objs,files
def run(ad,out):
    r=subprocess.run([sys.executable,'-I','-B',str(ad),str(out)],capture_output=True,text=True)
    j=json.loads(r.stdout.strip().splitlines()[-1])
    try:b=json.loads(Path(out).read_text()) if Path(out).exists() else None
    except ValueError:b='UNPARSEABLE_NON_BUNDLE_FILE'
    return r.returncode,j,b
def ptr(o,p):
    for t in p.strip('/').split('/'):o=o[int(t)] if isinstance(o,list) else o[t]
    return o
# ---- T1 valid
d,ad,objs,files=build('valid');rc,j,b=run(ad,d/'bundle.json');txt=json.dumps(b)
case('T1 valid synthetic -> bundle written (exit 0)',rc==0 and j['status']=='CANDIDATE_BUNDLE_WRITTEN',json.dumps(j)[:90])
case('T1 sentinel: nothing from non-allowlisted observational keys enters output',SENT not in txt and 'raw_line_ascii' not in txt and 'radius_over_r25' not in txt and 'chunk_rows' not in txt and 'half_effective' not in txt and 'los_sigma2' not in txt and 'direct_map_totals' not in txt)
cand=d/'bundle.json.candidate'
case('T1 candidate retained, complete, same bytes and same file as output; reported paths/hashes match',cand.exists() and cand.read_bytes()==(d/'bundle.json').read_bytes() and os.path.samefile(cand,d/'bundle.json') and j['candidate']['sha256']==sha(cand.read_bytes())==j['output']['sha256'] and j['candidate']['path']==str(cand) and j['phase']=='PUBLISHED')
s2b=b['sources']['S2_HALOGAS_PLANAR'];s1b=b['sources']['S1_LEROY_T7']
case('T1 both orders and both widths, 3 groups x 13 fields',[o['subpixels_per_axis']['value'] for o in s2b['orders']]==[4,8] and all(len(g)==13 for o in s2b['orders'] for p in o['profiles'].values() for g in p['groups'].values()))
neg=s2b['orders'][1]['profiles']['profile_40arcsec']['groups']['full']
case('T1 negative values preserved (S2 masses, raw missing fraction; S1 literal)',min(neg['negative_mass_Msun']['values'])==-3.0 and min(neg['missing_footprint_fraction_raw']['values'])==-1e-6 and s1b['rows'][3]['components']['H2']['value_literal']['value']=='-1/5')
case('T1 missing H2 stays null with MISSING kind; OPEN-4 computed from rows',all(r['components']['H2']['value_literal']['value'] is None and r['components']['H2']['error_kind']['adapter_label']=='MISSING' for r in s1b['rows'][10:]) and [x for x in b['open_issues']['items'] if x['id']=='OPEN-4'][0]['computed']['missing_rows']==list(range(10,23)))
ek=lambda i,c:s1b['rows'][i]['components'][c]['error_kind']['adapter_label']
case('T1 S1 error kinds: note-3 quarantine, literal zero, neutral per-ring rms label',ek(2,'stars').endswith('QUARANTINED') and ek(16,'stars')=='LITERAL_ZERO_MEANING_UNRESOLVED' and ek(0,'HI')=='PUBLISHED_PER_RING_RMS_FIELD')
case('T1 S1 table_level fields carry pointers and exact expected values',all(v['pointer']=='/value/'+k for k,v in s1b['table_level'].items()) and s1b['table_level']['raw_to_native_map']['value'] is None)
eff=s2b['orders'][0]['profiles']['profile_120arcsec']['groups']['full']['effective_HI_Msun_pc2_complete_only']['values']
case('T1 effective density null exactly on incomplete bins',all((x is None)==(k>=17) for k,x in enumerate(eff)))
case('T1 helium label refers to /settings/helium_factor, no numeric factor in kind','x1.36' not in txt and '/settings/helium_factor' in s2b['orders'][0]['profiles']['profile_40arcsec']['groups']['full']['effective_HI_plus_He_Msun_pc2_complete_only']['kind'])
kinds={v['kind'] for o in s2b['orders'] for p in o['profiles'].values() for g in p['groups'].values() for v in g.values()}
case('T1 descriptive scatter / mask fraction / unknown uncertainty labelled distinctly','descriptive_scatter_not_measurement_error' in kinds and 'mask_fraction_zero_or_replaced' in kinds and s2b['measurement_uncertainty']['state']=='UNKNOWN')
# exhaustive provenance round-trip
mis=0;cnt=0
for o in s2b['orders']:
    mis+=ptr(objs['s2_results'],o['subpixels_per_axis']['pointer'])!=o['subpixels_per_axis']['value'];cnt+=1
    for p in o['profiles'].values():
        mis+=ptr(objs['s2_results'],p['width_arcsec']['pointer'])!=p['width_arcsec']['value'];cnt+=1
        arrays=[p[k] for k in ('r_lo_kpc','r_hi_kpc','complete_by_conservative_chord_bound')]+[v for g in p['groups'].values() for v in g.values()]
        for v in arrays:
            for k,x in enumerate(v['values']):
                y=ptr(objs['s2_results'],v['pointer']+'/'+str(k));mis+=(y!=x or type(y)!=type(x));cnt+=1
for blk in ('settings','pixel_categories'):
    for k,v in s2b[blk].items():mis+=ptr(objs['s2_results'],v['pointer'])!=v['value'];cnt+=1
for r in s1b['rows']:
    for v in [r['original_line_number'],r['radius_kpc_literal']]+list(r['conventions'].values())+[c[f] for c in r['components'].values() for f in ('value_literal','error_literal','p53_interpretation')]:
        mis+=ptr(objs['s1_table'],v['pointer'])!=v['value'];cnt+=1
for k,v in s1b['table_level'].items():mis+=ptr(objs['s1_table'],v['pointer'])!=v['value'];cnt+=1
for q in b['queries']['items']:mis+=ptr(objs['query_manifest'],q['pointer'])['Rad_text']!=q['Rad_text'];cnt+=1
for sid,items in b['conventions']['items'].items():
    for k,v in items.items():mis+=ptr(objs['crosswalk'],v['pointer'])!=v['text'];cnt+=1
case('T1 exhaustive provenance round-trip (every S2 element, settings, pixels, S1 field, query, convention)',mis==0,'%d values checked, %d mismatches'%(cnt,mis))
pins={'queries':'query_manifest'}
case('T1 all six inputs pinned in output',b['queries']['provenance']['sha256']==sha(files['query_manifest'].read_bytes()) and s1b['provenance']['sha256']==sha(files['s1_table'].read_bytes()) and s2b['provenance']['sha256']==sha(files['s2_results'].read_bytes()) and b['conventions']['provenance']['sha256']==sha(files['crosswalk'].read_bytes()) and b['conventions']['correction_provenance']['sha256']==sha(files['crosswalk_correction'].read_bytes()) and b['open_issues']['ref_files']['ledger']['sha256']==sha(files['ledger'].read_bytes()))
cv=b['conventions']
case('T1 0346 correction attached to S1 helium and S2 geometry; S3 item listed as not in bundle; text verbatim',cv['items']['S1_LEROY_T7']['helium_conversion_state']['corrections'][0]['id']=='C1' and cv['items']['S2_HALOGAS_C1']['geometry']['corrections'][0]['id']=='C6' and cv['corrections_for_sources_not_in_bundle'][0]['id']=='C7' and cv['items']['S1_LEROY_T7']['helium_conversion_state']['text']=={'HI':'h','H2':'h2'})
case('T1 OPEN-1..10 present incl. double count, stellar outer, H2, geometry, native map, primary conversions',[x['id'] for x in b['open_issues']['items']]==['OPEN-%d'%i for i in range(1,11)])
case('T1 queries separate, 43 IDs',len(b['queries']['items'])==43)
# documented narrowed claim: metadata strings are copied verbatim
def meta_sent(c):c['corrections'][0]['now']['note']=SENT
d2,ad2,_,_=build('metadata_string_verbatim',cmods=meta_sent);rc2,j2,b2=run(ad2,d2/'bundle.json')
case('T1b metadata (pinned Claude-authored) strings are copied verbatim and labelled metadata, as documented',rc2==0 and SENT in json.dumps(b2['conventions']) and SENT not in json.dumps(b2['sources'])+json.dumps(b2['queries']) and b2['conventions']['class'].startswith('pinned Claude-authored provenance METADATA'))
# ---- failure tests (exact codes)
def expect(tag,code,mods=None,raw=None,pre=None,cmods=None):
    d,ad,objs,files=build(tag,mods,raw,cmods)
    if pre:pre(d)
    rc,j,b=run(ad,d/'bundle.json')
    ok=rc==2 and j.get('code')==code and j.get('status')=='FAILED_VALIDATION' and j.get('candidate_written') is False and (b is None or tag=='output_exists') and not (d/'bundle.json.candidate').exists()
    case('F '+tag+' -> '+code,ok,json.dumps(j))
def badpin(tag,key):
    d,ad,objs,files=build(tag);files[key].write_bytes(files[key].read_bytes()+b' ')
    rc,j,b=run(ad,d/'bundle.json');case('F '+tag+' -> E_PIN_'+key,rc==2 and j.get('code')=='E_PIN_'+key and b is None)
for k in ('query_manifest','s1_table','s2_results','crosswalk','crosswalk_correction','ledger'):badpin('bad_hash_'+k,k)
def m(f):return f
expect('missing_query','E_Q_COUNT',lambda o:o['query_manifest']['rows'].pop())
expect('duplicate_query','E_Q_DUPLICATE',lambda o:o['query_manifest']['rows'][5].__setitem__('query_id','NGC3198-Q05'))
expect('query_id_order','E_Q_ID_ORDER',lambda o:o['query_manifest']['rows'][5].__setitem__('query_id','NGC3198-Q07'))
expect('query_unit','E_Q_UNIT_VALUE',lambda o:o['query_manifest']['rows'][5].__setitem__('Rad_unit','arcsec'))
expect('query_radius_negative','E_Q_RAD_DOMAIN',lambda o:o['query_manifest']['rows'][0].__setitem__('Rad_text','-0.50'))
expect('query_radius_trailing_newline','E_Q_RAD_DOMAIN',lambda o:o['query_manifest']['rows'][0].__setitem__('Rad_text','0.50\n'))
expect('query_radius_fullwidth_digits','E_Q_RAD_DOMAIN',lambda o:o['query_manifest']['rows'][0].__setitem__('Rad_text','０.50'))
expect('query_id_trailing_newline','E_Q_ID_ORDER',lambda o:o['query_manifest']['rows'][2].__setitem__('query_id','NGC3198-Q03\n'))
expect('query_radius_order','E_Q_RAD_ORDER',lambda o:o['query_manifest']['rows'][4].__setitem__('Rad_text','1.00'))
expect('query_radius_type','E_Q_RAD_TYPE',lambda o:o['query_manifest']['rows'][7].__setitem__('Rad_text',7.5))
expect('s1_radius_type','E_S1_RADIUS_TYPE',lambda o:o['s1_table']['value']['rows'][4].__setitem__('radius_kpc',3.1))
expect('s1_radius_trailing_newline','E_S1_RADIUS_FORMAT',lambda o:o['s1_table']['value']['rows'][0].__setitem__('radius_kpc','3/10\n'))
expect('s1_missing_must_stay_null','E_S1_MISSING_NOT_NULL',lambda o:o['s1_table']['value']['rows'][12]['H2'].__setitem__('published_value','0'))
expect('s1_null_value','E_S1_LITERAL_FORMAT',lambda o:o['s1_table']['value']['rows'][5]['HI'].__setitem__('published_value',None))
expect('s1_negative_error','E_S1_NEGATIVE_ERROR',lambda o:o['s1_table']['value']['rows'][1]['HI'].__setitem__('published_error_field','-1/5'))
expect('s1_line_order','E_S1_LINE_ORDER',lambda o:o['s1_table']['value']['rows'][9].__setitem__('original_line_number',999))
expect('s1_flag_int_zero_not_false','E_S1_CONV_VALUE',lambda o:o['s1_table']['value']['rows'][0].__setitem__('helium_multiplier_applied',0))
expect('s1_flag_float_zero_not_false','E_S1_CONV_VALUE',lambda o:o['s1_table']['value']['rows'][0].__setitem__('stellar_ML_applied_again',0.0))
expect('s1_err1_without_note3_interp','E_S1_INTERP_MISMATCH',lambda o:o['s1_table']['value']['rows'][5]['HI'].__setitem__('published_error_field','1'))
expect('s1_note3_interp_without_err1','E_S1_INTERP_MISMATCH',lambda o:o['s1_table']['value']['rows'][2]['stars'].__setitem__('published_error_field','3/10'))
expect('s1_note3_err_trailing_newline','E_S1_LITERAL_FORMAT',lambda o:o['s1_table']['value']['rows'][2]['stars'].__setitem__('published_error_field','1\n'))
expect('s1_unknown_interp','E_S1_INTERP_UNKNOWN',lambda o:o['s1_table']['value']['rows'][2]['HI'].__setitem__('interpretation','SOMETHING_ELSE'))
expect('s1_table_level_nested_payload','E_S1_TL_VALUE_raw_to_native_map',lambda o:o['s1_table']['value'].__setitem__('raw_to_native_map',{'v':SENT}))
expect('s1_table_level_covariance_payload','E_S1_TL_VALUE_whole_covariance',lambda o:o['s1_table']['value'].__setitem__('whole_covariance',[[1]]))
expect('s1_table_level_key_absent','E_S1_TL_source_selected',lambda o:o['s1_table']['value'].pop('source_selected'))
expect('s1_table_sha_format','E_S1_TABLE_SHA_FORMAT',lambda o:o['s1_table']['value'].__setitem__('whole_table_sha256',SENT))
expect('s2_null_in_never_null','E_S2_FIELD_mass_Msun_NULL',lambda o:o['s2_results']['orders'][1]['profile_40arcsec']['groups']['full']['mass_Msun'].__setitem__(7,None))
expect('s2_value_on_incomplete_bin','E_S2_FIELD_effective_HI_Msun_pc2_complete_only_VALUE_ON_INCOMPLETE',lambda o:o['s2_results']['orders'][0]['profile_120arcsec']['groups']['X_negative']['effective_HI_Msun_pc2_complete_only'].__setitem__(40,0.0))
expect('s2_null_on_complete_bin','E_S2_FIELD_effective_HI_plus_He_Msun_pc2_complete_only_NULL',lambda o:o['s2_results']['orders'][0]['profile_120arcsec']['groups']['full']['effective_HI_plus_He_Msun_pc2_complete_only'].__setitem__(3,None))
expect('s2_missing_order','E_S2_ORDER_SET',lambda o:o['s2_results']['orders'].pop(0))
expect('s2_wrong_length','E_S2_FIELD_plane_pc2_LENGTH',lambda o:o['s2_results']['orders'][1]['profile_120arcsec']['groups']['full']['plane_pc2'].pop())
expect('s2_missing_setting','E_S2_SETTING_pa_deg',lambda o:o['s2_results']['settings'].pop('pa_deg'))
expect('s2_bool_in_numeric','E_S2_FIELD_zero_fraction_of_footprint_TYPE',lambda o:o['s2_results']['orders'][0]['profile_40arcsec']['groups']['full']['zero_fraction_of_footprint'].__setitem__(0,True))
expect('s2_not_complete','E_S2_NOT_COMPLETE',lambda o:o['s2_results'].__setitem__('status','PARTIAL'))
expect('s2_grid_gap','E_S2_GRID',lambda o:o['s2_results']['orders'][1]['profile_40arcsec']['r_hi_kpc'].__setitem__(10,999.0))
expect('s2_complete_not_prefix','E_S2_COMPLETE_NOT_PREFIX',lambda o:o['s2_results']['orders'][0]['profile_40arcsec']['complete_by_conservative_chord_bound'].__setitem__(100,True))
expect('s2_width_value','E_S2_WIDTH_VALUE',lambda o:o['s2_results']['orders'][0]['profile_40arcsec'].__setitem__('width_arcsec',41.0))
expect('s2_pixel_domain','E_S2_PIXEL_DOMAIN',lambda o:o['s2_results']['pixel_categories'].__setitem__('negative',-1))
expect('crosswalk_key_missing','E_CW_S2_HALOGAS_C1_masks',lambda o:o['crosswalk']['sources']['S2_HALOGAS_C1'].pop('masks'))
expect('crosswalk_numeric_payload','E_CW_TYPE_S2_HALOGAS_C1_units',lambda o:o['crosswalk']['sources']['S2_HALOGAS_C1'].__setitem__('units',[1.0,2.0]))
o=s2();o['orders'][0]['profile_40arcsec']['groups']['full']['mass_Msun'][2]=float('nan')
expect('nan_token','E_JSON_NONFINITE_TOKEN',raw={'s2_results':json.dumps(o).encode()})
o=s2();o['orders'][0]['profile_40arcsec']['groups']['full']['mass_Msun'][2]=float('inf')
expect('infinity_token','E_JSON_NONFINITE_TOKEN',raw={'s2_results':json.dumps(o).encode()})
dupraw=json.dumps(s2()).replace('"mass_Msun": [','"mass_Msun": ["%s"], "mass_Msun": ['%SENT,1).encode()
expect('duplicate_json_key','E_JSON_DUPLICATE_KEY',raw={'s2_results':dupraw})
expect('correction_binds_other_crosswalk','E_CORR_BINDING_SHA',cmods=lambda c:c['corrects'].__setitem__('sha256','0'*64))
expect('correction_binding_file','E_CORR_BINDING_FILE',cmods=lambda c:c['corrects'].__setitem__('file','/x/OTHER.json'))
expect('correction_not_unchanged','E_CORR_BINDING_FILE',cmods=lambda c:c['corrects'].__setitem__('unchanged',False))
expect('correction_pointer_unresolved','E_CORR_POINTER_UNRESOLVED',cmods=lambda c:c['corrections'][0].__setitem__('crosswalk_pointer','/sources/S1_LEROY_T7/no_such_key'))
expect('correction_pointer_syntax','E_CORR_POINTER_SYNTAX',cmods=lambda c:c['corrections'][0].__setitem__('crosswalk_pointer','sources/S1_LEROY_T7/units/'))
expect('correction_duplicate_id','E_CORR_DUPLICATE',cmods=lambda c:c['corrections'][1].__setitem__('id','C1'))
expect('correction_now_numeric','E_CORR_NOW_TYPE',cmods=lambda c:c['corrections'][1]['now'].__setitem__('factor',1.36))
expect('ledger_ref_out_of_range','E_LEDGER_REF',lambda o:o['ledger'].__setitem__('items',o['ledger']['items'][:5]))
def keep_existing(d):(d/'bundle.json').write_bytes(b'{"pre-existing": true}')
dd,ad3,_,_=build('output_exists');keep_existing(dd);rc,j,_b=run(ad3,dd/'bundle.json')
case('F output_exists -> E_OUTPUT_EXISTS (validation phase), existing file byte-identical, no candidate',rc==2 and j.get('code')=='E_OUTPUT_EXISTS' and j.get('status')=='FAILED_VALIDATION' and (dd/'bundle.json').read_bytes()==b'{"pre-existing": true}' and not (dd/'bundle.json.candidate').exists())
# source-level correction pointer
d4,ad4,_,_=build('source_level_pointer',cmods=lambda c:c['corrections'].append({'id':'C9','crosswalk_pointer':'/sources/S1_LEROY_T7','now':{'state':'x'}}))
rc,j,b4=run(ad4,d4/'bundle.json')
case('T2 source-level correction pointer is filed under source_level_corrections',rc==0 and b4['conventions']['source_level_corrections'][0]['id']=='C9')
# ---- R: real Claude-authored metadata only
XW='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_crosswalk_0341/'
rc_=json.load(open(XW+'SOURCE_CROSSWALK_CORRECTION_0346_V001.json'));rw_=json.load(open(XW+'SOURCE_CROSSWALK_V001.json'));lg_=json.load(open(XW+'UNCERTAINTY_MISSING_INPUT_LEDGER_V001.json'))
def res_(o,p):
    for t in p.strip('/').split('/'):
        if not isinstance(o,dict) or t not in o:return False
        o=o[t]
    return True
def tb(x,dep=0,fl=False):
    if dep>6:return False
    if isinstance(x,str):return True
    if type(x) is bool:return fl
    if isinstance(x,list):return all(tb(y,dep+1,fl) for y in x)
    if isinstance(x,dict):return all(isinstance(k,str) and tb(v,dep+1,fl) for k,v in x.items())
    return False
case('R real 0346 correction binds the real crosswalk (sha, file name, unchanged) and all pointers resolve',rc_['corrects']['sha256']==sha(open(XW+'SOURCE_CROSSWALK_V001.json','rb').read()) and Path(rc_['corrects']['file']).name=='SOURCE_CROSSWALK_V001.json' and rc_['corrects']['unchanged'] is True and all(res_(rw_,c['crosswalk_pointer']) and c['crosswalk_pointer'].startswith('/') for c in rc_['corrections']))
case('R real crosswalk convention texts and correction "now" blobs satisfy the metadata type bound',all(tb(rw_['sources'][s][k]) for s,ks in (('S1_LEROY_T7',K1),('S2_HALOGAS_C1',K2)) for k in ks) and all(tb(c['now'],fl=True) for c in rc_['corrections']))
ids=[i['id'] for i in lg_['items']]
case('R ledger refs used by OPEN issues point at the intended ledger items',all(ids[int(r.split('/')[-1])]==u for r,u in (('ledger:/items/16','U17'),('ledger:/items/17','U18'),('ledger:/items/14','U15'),('ledger:/items/10','U11'),('ledger:/items/7','U8'),('ledger:/items/15','U16'),('ledger:/items/0','U1'),('ledger:/items/4','U5'),('ledger:/items/5','U6'),('ledger:/items/8','U9'),('ledger:/items/9','U10'))))
# ---------------- 0348 publication-lifecycle tests ----------------
def build_patched(tag,patch):
    d,ad,objs,files=build(tag);s=ad.read_text();anchor='def candidate_path(outp):'
    assert s.count(anchor)==1;ad.write_text(s.replace(anchor,patch+'\n'+anchor));return d,ad
def files_in(d):return sorted(x.name for x in d.iterdir())
def pubcase(tag,patch,code,cand_expect,out_expect,pre=None):
    d,ad=build_patched(tag,patch)
    if pre:pre(d)
    before=files_in(d);rc,j,_=run(ad,d/'bundle.json');after=files_in(d)
    c=d/'bundle.json.candidate';o=d/'bundle.json'
    ok=rc==4 and j.get('status')=='FAILED_PUBLICATION' and j.get('code')==code and j.get('success_claimed') is False and set(before)<=set(after)
    if cand_expect=='complete':ok&=c.exists() and sha(c.read_bytes())==j['publication']['expected_sha256']
    elif cand_expect=='partial':ok&=c.exists() and 0<c.stat().st_size<j['publication']['expected_bytes']
    elif cand_expect=='absent':ok&=not c.exists() and j['publication']['candidate_created'] is False
    if out_expect=='absent':ok&=not o.exists()
    elif out_expect=='racer':ok&=o.read_bytes()==b'RACER'
    elif out_expect=='published_not_claimed':ok&=o.exists() and j['publication']['output_published'] is True
    case('P '+tag+' -> '+code+' (candidate '+cand_expect+', output '+out_expect+', nothing removed)',ok,json.dumps(j)[:160])
pubcase('race_output_created_before_link',"_rl=os.link\ndef _race(a,b):\n Path(b).write_bytes(b'RACER');return _rl(a,b)\nos.link=_race  # TEST-ONLY","E_OUTPUT_EXISTS_AT_PUBLICATION",'complete','racer')
pubcase('link_unsupported',"def _nolink(a,b):raise OSError(1,'Operation not permitted (TEST-ONLY)')\nos.link=_nolink","E_PUBLICATION_LINK",'complete','absent')
pubcase('partial_write',"_fd=os.fdopen\nclass _W:\n def __init__(s,f):s.f=f\n def __enter__(s):return s\n def __exit__(s,*a):s.f.close()\n def write(s,b):s.f.write(b[:len(b)//2]);s.f.flush();raise OSError(28,'No space left on device (TEST-ONLY)')\n def flush(s):pass\n def fileno(s):return s.f.fileno()\nos.fdopen=lambda fd,m:_W(_fd(fd,m))","E_CANDIDATE_WRITE",'partial','absent')
pubcase('candidate_verify_mismatch',"_rb=Path.read_bytes\ndef _bad(self):\n x=_rb(self)\n return x+b' ' if self.name.endswith('.candidate') else x\nPath.read_bytes=_bad","E_CANDIDATE_VERIFY",'complete','absent')
pubcase('candidate_create_denied',"_op=os.open\ndef _deny(p,fl,*a):\n if str(p).endswith('.candidate'):raise PermissionError(13,'denied (TEST-ONLY)')\n return _op(p,fl,*a)\nos.open=_deny","E_CANDIDATE_CREATE",'absent','absent')
pubcase('candidate_appears_before_create',"_op=os.open\ndef _pre(p,fl,*a):\n if str(p).endswith('.candidate') and not Path(p).exists():Path(p).write_bytes(b'OTHER')\n return _op(p,fl,*a)\nos.open=_pre","E_CANDIDATE_EXISTS",'other','absent')
pubcase('directory_fsync_fails',"_fs=os.fsync\n_cnt=[0]\ndef _dfs(fd):\n import stat\n if stat.S_ISDIR(os.fstat(fd).st_mode):raise OSError(5,'I/O error (TEST-ONLY)')\n return _fs(fd)\nos.fsync=_dfs","E_DIRECTORY_FSYNC",'complete','published_not_claimed')
d5,ad5,_,_=build('pre_existing_candidate')
(d5/'bundle.json.candidate').write_bytes(b'OLD');rc,j,_=run(ad5,d5/'bundle.json')
case('V pre-existing candidate -> E_CANDIDATE_EXISTS in validation phase; old candidate byte-identical; no output',rc==2 and j.get('status')=='FAILED_VALIDATION' and j.get('code')=='E_CANDIDATE_EXISTS' and (d5/'bundle.json.candidate').read_bytes()==b'OLD' and not (d5/'bundle.json').exists())
srcv3=A.read_text()
case('S static: no unlink/remove/rename/replace/rmtree call in adapter V003 code',not any(t in srcv3 for t in ('os.unlink(','os.remove(','os.rename(','os.replace(','rmtree(','.unlink(')))
print('WORKDIR',T)
print('SUMMARY',sum(ok for _,ok,_ in res),'/',len(res),'passed')
