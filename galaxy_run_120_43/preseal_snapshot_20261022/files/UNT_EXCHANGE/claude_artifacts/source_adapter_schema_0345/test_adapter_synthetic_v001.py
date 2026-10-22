"""Synthetic-only tests for ngc3198_source_bundle_adapter_v001.py (task 0345-A). No real source is read except the adapter source text."""
import copy,hashlib,json,math,random,re,shutil,subprocess,sys
from pathlib import Path
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_adapter_schema_0345/ngc3198_source_bundle_adapter_v001.py')
T=Path(sys.argv[0]).resolve().parent/'work';shutil.rmtree(T,ignore_errors=True);T.mkdir()
SRC=A.read_text();SENT='SENTINEL_VELOCITY_RESPONSE_777'
sha=lambda b:hashlib.sha256(b).hexdigest()
def manifest():
    rows=[{'data_row_index':i+1,'query_id':'NGC3198-Q%02d'%(i+1),'source_line_number':i+4,'Rad_text':'%.2f'%(0.5+i),'Rad_unit':'kpc','Vobs':SENT,'errV':SENT} for i in range(43)]
    return {'schema':'x','rows':rows,'reference_distance':{'v':SENT},'Vflat':SENT}
def s1():
    rows=[]
    for i in range(23):
        h2=({'Gaussian_likelihood_assumed':False,'interpretation':'VALUE_WITH_PUBLISHED_RMS','published_error_field':'9/10','published_value':'-1/5' if i==3 else '51/2'} if i<10 else
            {'Gaussian_likelihood_assumed':False,'interpretation':'MISSING','published_error_field':None,'published_value':None})
        st_err='1' if i==2 else ('0' if i in (16,18,19,20) else '3/10')
        rows.append({'H2':h2,'HI':{'Gaussian_likelihood_assumed':False,'interpretation':'VALUE_WITH_PUBLISHED_RMS','published_error_field':'2/5','published_value':'%d/5'%(20+i)},
          'stars':{'Gaussian_likelihood_assumed':False,'interpretation':'UPPER_LIMIT_NOTE3' if i==2 else 'VALUE_WITH_PUBLISHED_RMS','published_error_field':st_err,'published_value':'%d/10'%(900-30*i),'v_rot':SENT},
          'gas_helium':'ALREADY_INCLUDED','helium_multiplier_applied':False,'original_line_number':320+i,'radius_kpc':'%d/10'%(3+7*i),'radius_over_r25':'1/100','raw_line_ascii':SENT,'stellar_ML_applied_again':False,'units':'Msun/pc^2','Vobs':SENT})
    return {'status':'RETURN','value':{'physical_prediction_released':False,'raw_to_native_map':None,'representation':'MASS_SURFACE_DENSITY','rows':rows,'source_selected':False,'whole_covariance':None,'whole_table_sha256':'f'*64,'response':SENT}}
F=['mass_Msun','positive_mass_Msun','negative_mass_Msun','effective_HI_Msun_pc2_complete_only','effective_HI_plus_He_Msun_pc2_complete_only','zero_fraction_of_footprint','finite_fraction_of_footprint','positive_fraction_of_footprint','negative_fraction_of_footprint','nominal_disk_area_pc2','plane_pc2','cosi_times_finite_sky_weighted_LOS_sigma_rms_Msun_pc2_not_measurement_error','missing_footprint_fraction_raw']
def s2():
    orders=[]
    for sp in (4,8):
        o={'subpixels_per_axis':sp,'direct_map_totals':{'mass_Msun':1.0,'v':SENT}}
        for pk,w,n,nc in (('profile_40arcsec',40.0,237,51),('profile_120arcsec',120.0,79,17)):
            step=w*0.0669;comp=[j<nc for j in range(n)]
            p={'width_arcsec':w,'r_lo_kpc':[j*step for j in range(n)],'r_hi_kpc':[(j+1)*step for j in range(n)],'complete_by_conservative_chord_bound':comp,'half_effective_HI_difference_complete_only':[0.0]*n,'groups':{}}
            for g in ('full','X_negative','X_nonnegative'):
                gd={}
                for f in F:
                    if f.startswith('effective'):gd[f]=[(5.0-0.01*j) if comp[j] else None for j in range(n)]
                    elif f=='negative_mass_Msun':gd[f]=[-(j%3)*1.5 for j in range(n)]
                    elif f.startswith('cosi'):gd[f]=[None if j in (n-1,n-2) else 0.1*j for j in range(n)]
                    else:gd[f]=[float(j)+0.25 for j in range(n)]
                gd['velocity_SENTINEL_field']=[SENT]*n
                p['groups'][g]=gd
            o[pk]=p
        orders.append(o)
    st={'HI_atoms_cm2_per_Msun_pc2':1.25e20,'bin_arcsec':40.0,'center_dec_deg':45.5,'center_ra_deg':154.9,'center_source':'synthetic','chunk_rows':4,'column_conversion_from_history':9.3e20,'distance_pc':13800000.0,'geometry':'synthetic plane','helium_factor':1.36,'inclination_deg':72.0,'orientation_source':'synthetic','pa_deg':215.0,'rebin':3,'subsamples':[4,8],'vsys_kms':SENT}
    return {'status':'COMPLETE','failed_checks':[],'passed_checks':63,'interpretation':'synthetic retained signal','settings':st,'pixel_categories':{'finite':100,'negative':2,'nonfinite':0,'positive':30,'total':100,'zero_or_replaced_mask':68},'orders':orders,'newton_force':SENT}
def crosswalk():
    k1=['tracers','radial_coordinate','resolution','geometry','units','helium_conversion_state','masks','error_fields','support'];k2=['tracer','radial_coordinate','geometry','units','helium_conversion_state','masks','error_fields','support','resolution']
    return {'sources':{'S1_LEROY_T7':{k:'s1 '+k for k in k1}|{'vflat':SENT},'S2_HALOGAS_C1':{k:'s2 '+k for k in k2}},'rotation':SENT}
def correction(cw_sha):
    return {'schema':'x','corrects':{'sha256':cw_sha},'Vobs':SENT,'corrections':[
      {'id':'C1','crosswalk_pointer':'/sources/S1_LEROY_T7/helium_conversion_state','now':{'state':'SECONDARY test'},'v_rot':SENT},
      {'id':'C2','crosswalk_pointer':'/sources/S2_HALOGAS_C1/geometry','now':{'state':'DECLARED test'}},
      {'id':'C9','crosswalk_pointer':'/sources/S1_LEROY_T7/units','now':{'state':'other'}}]}
ANCHOR='N_QUERIES=43;'
assert SRC.count(ANCHOR)==1  # test copies differ from the deliverable only by one inserted INPUTS override line before this anchor
res=[]
def case(name,ok,detail=''):res.append((name,bool(ok),detail));print(('PASS ' if ok else 'FAIL ')+name+(' | '+detail if detail else ''))
def build(tag,mods=None,raw=None,cmods=None):
    d=T/tag;d.mkdir();objs={'query_manifest':manifest(),'s1_table':s1(),'s2_results':s2(),'crosswalk':crosswalk()}
    if mods:mods(objs)
    files={};inputs={}
    for k,o in objs.items():
        f=d/(k+'.json');b=(raw or {}).get(k) or json.dumps(o).encode();f.write_bytes(b);files[k]=f;inputs[k]=(str(f),sha(b))
    cc=correction(inputs['crosswalk'][1])
    if cmods:cmods(cc)
    f=d/'crosswalk_correction.json';b=json.dumps(cc).encode();f.write_bytes(b);files['crosswalk_correction']=f;inputs['crosswalk_correction']=(str(f),sha(b));objs['crosswalk_correction']=cc
    s=SRC.replace(ANCHOR,'INPUTS='+repr(inputs)+'  # TEST-ONLY override\n'+ANCHOR)
    ad=d/'adapter.py';ad.write_text(s);return ad,objs,files
def run(ad,out):
    r=subprocess.run([sys.executable,'-I','-B',str(ad),str(out)],capture_output=True,text=True)
    j=json.loads(r.stdout.strip().splitlines()[-1]);return r.returncode,j,(json.loads(Path(out).read_text()) if Path(out).exists() else None)
def ptr(o,p):
    for t in p.strip('/').split('/'):o=o[int(t)] if isinstance(o,list) else o[t]
    return o
# T1 valid
ad,objs,files=build('t1');rc,j,b=run(ad,T/'t1/bundle.json');txt=json.dumps(b)
case('T1 valid synthetic -> bundle written',rc==0 and j['status']=='CANDIDATE_BUNDLE_WRITTEN',json.dumps(j)[:100])
case('T1 sentinel: no velocity/response/force field or value enters output',SENT not in txt and 'raw_line_ascii' not in txt and 'radius_over_r25' not in txt and 'chunk_rows' not in txt and 'missing_footprint_fraction_raw' not in txt and 'half_effective' not in txt)
s2b=b['sources']['S2_HALOGAS_PLANAR']
case('T1 both orders and both widths, 3 groups x 12 fields',[o['subpixels_per_axis'] for o in s2b['orders']]==[4,8] and all(len(o['profiles'][pk]['groups'][g])==12 for o in s2b['orders'] for pk in o['profiles'] for g in o['profiles'][pk]['groups']) and set(s2b['orders'][0]['profiles'])=={'profile_40arcsec','profile_120arcsec'})
neg=s2b['orders'][1]['profiles']['profile_40arcsec']['groups']['full']['negative_mass_Msun']['values']
case('T1 negative values preserved',min(neg)==-3.0 and b['sources']['S1_LEROY_T7']['rows'][3]['components']['H2']['value_literal']=='-1/5')
s1b=b['sources']['S1_LEROY_T7']['rows']
case('T1 missing H2 stays null with MISSING kind (never zero)',all(r['components']['H2']['value_literal'] is None and r['components']['H2']['error_kind']=='MISSING' for r in s1b[10:]))
case('T1 error kinds: note-3 quarantine, literal zero, published rms',s1b[2]['components']['stars']['error_kind'].endswith('QUARANTINED') and s1b[16]['components']['stars']['error_kind']=='LITERAL_ZERO_MEANING_UNRESOLVED' and s1b[0]['components']['HI']['error_kind']=='PUBLISHED_RMS_MEASUREMENT_ERROR')
eff=s2b['orders'][0]['profiles']['profile_120arcsec']['groups']['full']['effective_HI_Msun_pc2_complete_only']['values']
case('T1 effective density null exactly on incomplete bins (not zero)',all((x is None)==(k>=17) for k,x in enumerate(eff)))
kinds={v['kind'] for o in s2b['orders'] for p in o['profiles'].values() for g in p['groups'].values() for v in g.values()}
case('T1 descriptive scatter / mask fraction / unknown uncertainty labelled distinctly','descriptive_scatter_not_measurement_error' in kinds and 'mask_fraction_zero_or_replaced' in kinds and s2b['measurement_uncertainty']['state']=='UNKNOWN')
random.seed(1);ok=True
for o in s2b['orders']:
    for p in o['profiles'].values():
        for g in p['groups'].values():
            for v in g.values():
                k=random.randrange(len(v['values']));ok&=ptr(objs['s2_results'],v['pointer']+'/'+str(k))==v['values'][k]
for r in s1b:
    for c,v in r['components'].items():ok&=ptr(objs['s1_table'],v['pointer'])['published_value']==v['value_literal']
for q in b['queries']['items']:ok&=ptr(objs['query_manifest'],q['pointer'])['Rad_text']==q['Rad_text']
for sid,items in b['conventions']['items'].items():
    for k,v in items.items():ok&=ptr(objs['crosswalk'],v['pointer'])==v['text']
case('T1 provenance pointers resolve to the emitted values (S1, S2 sampled, queries, conventions)',ok)
case('T1 inputs pinned with sha256 in output',all(b[x]['provenance']['sha256']==sha(files[k].read_bytes()) for x,k in (('queries','query_manifest'),)) and b['sources']['S2_HALOGAS_PLANAR']['provenance']['sha256']==sha(files['s2_results'].read_bytes()))
case('T1 queries separate, 43 IDs, no grid mapping',len(b['queries']['items'])==43 and 'OPEN-9' in [x['id'] for x in b['open_issues']])
case('T1 OPEN issues machine-readable (double count, stellar outer, H2, geometry, native map)',{'HI_TRACER_DOUBLE_COUNT','STELLAR_OUTER_SUPPORT','MISSING_H2','GEOMETRY_QUARANTINE','NATIVE_OBSERVATION_MAP'}<= {x['topic'] for x in b['open_issues']})
# failure tests
def expect(tag,code,mods=None,raw=None,pre=None,cmods=None):
    ad,objs,files=build(tag,mods,raw,cmods)
    if pre:pre(T/tag)
    rc,j,b=run(ad,T/tag/'bundle.json')
    out_ok=b is None or tag=='n_output_exists'
    case('F '+tag+' -> '+code,rc!=0 and j.get('code','').startswith(code) and out_ok,json.dumps(j))
def badpin(tag):
    ad,objs,files=build(tag);files['s2_results'].write_bytes(files['s2_results'].read_bytes()+b' ')
    rc,j,b=run(ad,T/tag/'bundle.json');case('F '+tag+' -> E_PIN_s2_results',j.get('code')=='E_PIN_s2_results' and b is None)
badpin('a_bad_hash')
expect('b_missing_query','E_Q_COUNT',lambda o:o['query_manifest']['rows'].pop())
def dup(o):o['query_manifest']['rows'][5]['query_id']='NGC3198-Q05'
expect('c_duplicate_query','E_Q_DUPLICATE',dup)
def neg_r(o):o['query_manifest']['rows'][0]['Rad_text']='-0.50'
expect('d_out_of_domain_radius','E_Q_RAD_DOMAIN',neg_r)
def order(o):o['query_manifest']['rows'][4]['Rad_text']='1.00'
expect('e_non_increasing_radius','E_Q_RAD_ORDER',order)
def qtype(o):o['query_manifest']['rows'][7]['Rad_text']=7.5
expect('f_query_type','E_Q_RAD_TYPE',qtype)
def s1type(o):o['s1_table']['value']['rows'][4]['radius_kpc']=3.1
expect('g_s1_radius_type','E_S1_RADIUS_TYPE',s1type)
def s1miss(o):o['s1_table']['value']['rows'][12]['H2']['published_value']='0'
expect('h_missing_must_stay_null','E_S1_MISSING_NOT_NULL',s1miss)
def s1null(o):o['s1_table']['value']['rows'][5]['HI']['published_value']=None
expect('i_s1_null_value','E_S1_LITERAL_FORMAT',s1null)
def s2null(o):o['s2_results']['orders'][1]['profile_40arcsec']['groups']['full']['mass_Msun'][7]=None
expect('j_s2_null_in_never_null','E_S2_FIELD_mass_Msun_NULL',s2null)
def s2inc(o):o['s2_results']['orders'][0]['profile_120arcsec']['groups']['X_negative']['effective_HI_Msun_pc2_complete_only'][40]=0.0
expect('k_value_on_incomplete_bin','E_S2_FIELD_effective_HI_Msun_pc2_complete_only_VALUE_ON_INCOMPLETE',s2inc)
def s2nc(o):o['s2_results']['orders'][0]['profile_120arcsec']['groups']['full']['effective_HI_plus_He_Msun_pc2_complete_only'][3]=None
expect('l_null_on_complete_bin','E_S2_FIELD_effective_HI_plus_He_Msun_pc2_complete_only_NULL',s2nc)
def s2ord(o):o['s2_results']['orders'].pop(0)
expect('m_missing_order','E_S2_ORDER_SET',s2ord)
expect('n_output_exists','E_OUTPUT_EXISTS',pre=lambda d:(d/'bundle.json').write_text('{}'))
def s2len(o):o['s2_results']['orders'][1]['profile_120arcsec']['groups']['full']['plane_pc2'].pop()
expect('o_wrong_length','E_S2_FIELD_plane_pc2_LENGTH',s2len)
def s2set(o):del o['s2_results']['settings']['pa_deg']
expect('p_missing_setting','E_S2_SETTING_pa_deg',s2set)
def s2bool(o):o['s2_results']['orders'][0]['profile_40arcsec']['groups']['full']['zero_fraction_of_footprint'][0]=True
expect('q_bool_in_numeric','E_S2_FIELD_zero_fraction_of_footprint_TYPE',s2bool)
def s2stat(o):o['s2_results']['status']='PARTIAL'
expect('r_s2_not_complete','E_S2_NOT_COMPLETE',s2stat)
def cwmiss(o):del o['crosswalk']['sources']['S2_HALOGAS_C1']['masks']
expect('s_crosswalk_key_missing','E_CW_S2_HALOGAS_C1_masks',cwmiss)
o=s2();o['orders'][0]['profile_40arcsec']['groups']['full']['mass_Msun'][2]=float('nan')
expect('t_nan_value','E_S2_FIELD_mass_Msun_TYPE',raw={'s2_results':json.dumps(o).encode()})
def s1neg_err(o):o['s1_table']['value']['rows'][1]['HI']['published_error_field']='-1/5'
expect('u_negative_error','E_S1_NEGATIVE_ERROR',s1neg_err)
def s1line(o):o['s1_table']['value']['rows'][9]['original_line_number']=999
expect('v_s1_line_order','E_S1_LINE_ORDER',s1line)
def grid(o):o['s2_results']['orders'][1]['profile_40arcsec']['r_hi_kpc'][10]+=0.5
expect('w_s2_grid_gap','E_S2_GRID',grid)
cv=b['conventions']
case('T1 0346 correction bound: attached to S1 helium and S2 geometry items, pinned, sentinel-free',cv['items']['S1_LEROY_T7']['helium_conversion_state']['corrections'][0]['id']=='C1' and cv['items']['S2_HALOGAS_C1']['geometry']['corrections'][0]['id']=='C2' and cv['correction_provenance']['sha256']==sha(files['crosswalk_correction'].read_bytes()) and 'OPEN-10' in [x['id'] for x in b['open_issues']])
def cbind(c):c['corrects']['sha256']='0'*64
expect('x_correction_binds_other_crosswalk','E_CORR_BINDING_SHA',cmods=cbind)
def cptr(c):c['corrections'][0]['crosswalk_pointer']='/sources/S1_LEROY_T7/no_such_key'
expect('y_correction_pointer_unresolved','E_CORR_POINTER_UNRESOLVED',cmods=cptr)
def cdup(c):c['corrections'][1]['id']='C1'
expect('z_correction_duplicate_id','E_CORR_DUPLICATE',cmods=cdup)
# deliverable-level check (Claude's own artifacts, not source data): every real correction pointer resolves in the real crosswalk
rc_=json.load(open('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_crosswalk_0341/SOURCE_CROSSWALK_CORRECTION_0346_V001.json'));rw_=json.load(open('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_crosswalk_0341/SOURCE_CROSSWALK_V001.json'))
def res_(o,p):
    for t in p.strip('/').split('/'):
        if not isinstance(o,dict) or t not in o:return False
        o=o[t]
    return True
case('R real 0346 correction: binds crosswalk sha and all 8 pointers resolve in the real crosswalk',rc_['corrects']['sha256']==sha(open('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_crosswalk_0341/SOURCE_CROSSWALK_V001.json','rb').read()) and len(rc_['corrections'])==8 and all(res_(rw_,c['crosswalk_pointer']) for c in rc_['corrections']))
print('SUMMARY',sum(ok for _,ok,_ in res),'/',len(res),'passed')
