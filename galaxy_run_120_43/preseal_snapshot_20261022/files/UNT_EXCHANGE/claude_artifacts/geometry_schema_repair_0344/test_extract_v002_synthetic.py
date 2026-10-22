import hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
T=Path(sys.argv[0]).resolve().parent/'work'; shutil.rmtree(T,ignore_errors=True); T.mkdir()
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
V2=(A/'geometry_schema_repair_0344/extract_sparc_geometry_metadata_v002.py').read_text()
V1=(A/'galaxy_source_preparation_0337/extract_sparc_geometry_metadata_v001.py').read_text()
REAL='/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/external_ddo154_v001/SPARC_Lelli2016c.mrt'
REAL_SHA='5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243'
README='/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/external_ddo154_v001/SPARC_ReadMe.html'
README_SHA='457f61cd8e63dd7b8f8ce0052a458294fa1a5acc2b5b23bb951a2c40d69f9666'
sha=lambda b:hashlib.sha256(b).hexdigest()
# header only (documentation): lines up to and including the last 20+ dash separator among the first 200 lines
hl=[]
with open(REAL,'rb') as fh:
    for i,l in enumerate(fh):
        if i>=200:break
        hl.append(l)
last=max(i for i,l in enumerate(hl) if re.fullmatch(rb'-{20,}',l.strip()))
HEADER=b''.join(hl[:last+1]); del hl
LAY={'CDS':{'Type':(13,14),'D':(16,21),'e_D':(23,27),'f_D':(29,29),'Inc':(31,34),'e_Inc':(36,39),'_vflat':(101,105),'_len':130},
     'MRT':{'Type':(12,13),'D':(14,19),'e_D':(20,24),'f_D':(25,26),'Inc':(27,30),'e_Inc':(31,34),'_vflat':(87,91),'_len':113},
     'OBS':{'Type':(12,14),'D':(15,21),'e_D':(22,27),'f_D':(28,30),'Inc':(31,35),'e_Inc':(36,40),'_vflat':(102,106),'_len':131}}
VAL={'DDO154':{'Type':'10','D':'1.23','e_D':'0.45','f_D':'2','Inc':'66.6','e_Inc':'7.7'},
     'NGC3198':{'Type':'5','D':'12.34','e_D':'1.11','f_D':'3','Inc':'55.5','e_Inc':'2.2'},
     'UGC00128':{'Type':'8','D':'64.50','e_D':'9.68','f_D':'1','Inc':'57.0','e_Inc':'10.0'}}
SENT='777.7'
def row(name,lay,over=None,cut=None):
    L=LAY[lay];b=bytearray(b' '*L['_len'])
    b[0:11]=name.rjust(11).encode()
    v=dict(VAL[name]);v.update(over or {})
    for k,ae in L.items():
        if k.startswith('_'):continue
        a,e=ae
        s=v[k].encode()
        assert len(s)<=e-a+1,(k,s); b[e-len(s):e]=s
    a,e=L['_vflat'];b[a-1:e]=SENT.encode()
    out=bytes(b)
    return out[:cut] if cut else out
def fixture(tag,rows):
    d=T/tag;d.mkdir();f=d/'table.mrt';f.write_bytes(HEADER+b'\n'.join(rows)+b'\n');return f
def script(tag,src,v1=False,readme=(README,README_SHA)):
    d=T/tag;s=(V1 if v1 else V2).replace(REAL,str(src)).replace(REAL_SHA,sha(src.read_bytes()))
    if not v1:s=s.replace(README,readme[0]).replace(README_SHA,readme[1])
    p=d/('v1.py' if v1 else 'v2.py');p.write_text(s);return p
def run(p,out,extra=()):
    r=subprocess.run([sys.executable,'-I','-B',str(p),str(out),*extra],capture_output=True,text=True)
    j=json.loads(r.stdout.strip().splitlines()[-1]);o=json.loads(Path(out).read_text()) if Path(out).exists() else None
    return r.returncode,j,o
res=[]
def case(name,ok,detail=''):res.append((name,ok,detail));print(('PASS ' if ok else 'FAIL ')+name+(' | '+detail if detail else ''))
std=lambda lay,**kw:[row('UGC00128',lay),row('DDO154',lay,kw.get('d')),row('NGC3198',lay,kw.get('n'))]
# T1 CDS documented layout
f=fixture('t1_cds',std('CDS'));rc,j,o=run(script('t1_cds',f),T/'t1_cds/out.json')
case('T1 CDS-layout fixture -> PASS_DOCUMENTED_LAYOUT(CDS)',rc==0 and j['status']=='PASS_DOCUMENTED_LAYOUT' and o['chosen_layout']=='CDS_TABLE1_README' and o['objects']['NGC3198']['D']==12.34 and o['objects']['DDO154']['f_D']==2 and o['documentation']['CDS_TABLE1_README']['verified'] and SENT not in json.dumps(o),j['status'])
# T2 MRT documented layout
f=fixture('t2_mrt',std('MRT'));rc,j,o=run(script('t2_mrt',f),T/'t2_mrt/out.json')
case('T2 MRT-layout fixture -> PASS_DOCUMENTED_LAYOUT(MRT)',rc==0 and o['chosen_layout']=='MRT_INFILE_HEADER' and o['objects']['NGC3198']['Inc']==55.5 and o['documentation']['MRT_INFILE_HEADER']['verified'] and SENT not in json.dumps(o),j['status'])
# T3 replica of the REAL row spacing (synthetic values)
f=fixture('t3_obs',std('OBS'));rc,j,o=run(script('t3_obs',f),T/'t3_obs/out.json')
diag=o['layouts_evaluated']
case('T3 real-spacing replica -> FAILED_SCHEMA_VALIDATION, no values emitted',rc==2 and j['status']=='FAILED_SCHEMA_VALIDATION' and o['objects'] is None and '12.34' not in json.dumps(o),j['status'])
masks={obj:re.sub(r'[A9]','A',diag['CDS_TABLE1_README']['diagnosis'][obj]['prefix_class_mask'][:11])+diag['CDS_TABLE1_README']['diagnosis'][obj]['prefix_class_mask'][11:39] for obj in ('DDO154','NGC3198')}
REALMASK={'DDO154':'_____AAAAAA_99___9.99__9.99__9_99.9__9.','NGC3198':'____AAAAAAA__9__99.99__9.99__9_99.9__9.'}
case('T3 replica bytes 1-39 class mask == real-row prefix class mask (both rows)',all(masks[k]==REALMASK[k] for k in masks),json.dumps(masks))
summary={lay:{obj:{k:diag[lay]['diagnosis'][obj][k]['pass'] for k in ('Type','D','e_D','f_D','Inc','e_Inc')}|{'blank_bytes_ok':diag[lay]['diagnosis'][obj]['blank_bytes_ok']} for obj in ('DDO154','NGC3198')} for lay in diag}
(T/'t3_obs/predicted_real_diagnosis.json').write_text(json.dumps(summary,indent=1))
# T3b V001 on the same replica reproduces the defect (status OK with malformed literals)
p=script('t3_obs',f,v1=True);r=subprocess.run([sys.executable,'-I','-B',str(p),str(T/'t3_obs/out_v1.json')],capture_output=True,text=True)
o1=json.loads((T/'t3_obs/out_v1.json').read_text())
bad=[k for k in ('D','e_D','f_D','Inc','e_Inc') if not re.fullmatch(r'\d+(\.\d+)?',o1['objects']['NGC3198'][k])]
case('T3b V001 on replica -> status OK with malformed literals (defect reproduced)','"OK"' in r.stdout and len(bad)>=4,'malformed fields: '+','.join(bad)+' e.g. D='+repr(o1['objects']['NGC3198']['D']))
# T4 declared layout on replica
decl={'name':'OBSERVED_TOKEN_BOUNDARIES_DRAFT','declared_by':'TEST ONLY','evidence':'synthetic test','fields':{'Galaxy':[1,11,'A11'],'Type':[12,14,'I3'],'D':[15,21,'F7.2'],'e_D':[22,27,'F6.2'],'f_D':[28,30,'I3'],'Inc':[31,35,'F5.1'],'e_Inc':[36,40,'F5.1']},'blank_bytes':[41]}
dp=T/'t3_obs/decl.json';dp.write_text(json.dumps(decl));ds=sha(dp.read_bytes())
rc,j,o=run(T/'t3_obs/v2.py',T/'t3_obs/out_decl.json',['--declared-layout',str(dp),ds])
case('T4 replica + pinned declared layout -> PASS_DECLARED_LAYOUT',rc==0 and j['status']=='PASS_DECLARED_LAYOUT' and o['objects']['DDO154']['e_Inc']==7.7 and o['objects']['NGC3198']['D']==12.34 and SENT not in json.dumps(o),j['status'])
# T5 synthetic failures
def expect_fail(tag,rows,code=None,extra=(),readme=(README,README_SHA)):
    f=fixture(tag,rows);rc,j,o=run(script(tag,f,readme=readme),T/tag/'out.json',extra)
    ok=rc!=0 and not j['status'].startswith('PASS') and (code is None or j.get('code')==code or j['status']==code) and (o is None or o['objects'] is None)
    case('T5 '+tag+' -> '+(code or j['status']),ok,json.dumps(j)[:120])
expect_fail('a_nonnumeric_D',std('CDS',n={'D':'1x.34'}))
expect_fail('b_signed_D',std('CDS',n={'D':'-2.34'}))
expect_fail('c_zero_D',std('CDS',n={'D':'0.00'}))
expect_fail('d_bad_method_code',std('CDS',n={'f_D':'7'}))
expect_fail('e_inclination_95',std('CDS',n={'Inc':'95.0'}))
expect_fail('f_blank_e_Inc',std('CDS',n={'e_Inc':''}))
expect_fail('g_missing_NGC3198',[row('UGC00128','CDS'),row('DDO154','CDS')])
expect_fail('h_duplicate_DDO154',std('CDS')+[row('DDO154','CDS')])
expect_fail('i_truncated_row',[row('UGC00128','CDS'),row('DDO154','CDS',cut=33),row('NGC3198','CDS')])
expect_fail('j_nan_D',std('CDS',n={'D':'nan'}))
expect_fail('q_exponent_D',std('CDS',n={'D':'1e+01'}))
expect_fail('r_one_decimal_for_F6.2',std('CDS',n={'D':'12.3'}))
expect_fail('s_inside_doc_range_violation_e_Inc_0.5',std('CDS',n={'e_Inc':'0.5'}))
# declaration failures and conflicts on the CDS fixture
f=fixture('k_decl_pin',std('CDS'));p=script('k_decl_pin',f);rc,j,o=run(p,T/'k_decl_pin/out.json',['--declared-layout',str(dp),'0'*64])
case('T5 k declared layout wrong sha -> E_DECLARATION_PIN',j.get('code')=='E_DECLARATION_PIN' and o is None)
d2=dict(decl,fields=dict(decl['fields'],e_Inc=[36,42,'F7.1']));dp2=T/'k_decl_pin/decl_far.json';dp2.write_text(json.dumps(d2))
rc,j,o=run(p,T/'k_decl_pin/out2.json',['--declared-layout',str(dp2),sha(dp2.read_bytes())])
case('T5 l declared field beyond byte 41 -> refused',j.get('code','').startswith('E_LAYOUT') and o is None,json.dumps(j))
d3={'name':'CDS_COPY','declared_by':'TEST ONLY','evidence':'x','fields':{'Galaxy':[1,11,'A11'],'Type':[13,14,'I2'],'D':[16,21,'F6.2'],'e_D':[23,27,'F5.2'],'f_D':[29,29,'I1'],'Inc':[31,34,'F4.1'],'e_Inc':[36,39,'F4.1']},'blank_bytes':[40]}
dp3=T/'k_decl_pin/decl_cds.json';dp3.write_text(json.dumps(d3))
rc,j,o=run(p,T/'k_decl_pin/out3.json',['--declared-layout',str(dp3),sha(dp3.read_bytes())])
case('T5 m declaration while a documented layout passes -> FAILED_DECLARATION_CONFLICT',j['status']=='FAILED_DECLARATION_CONFLICT' and o['objects'] is None)
(T/'k_decl_pin/exists.json').write_text('{}');rc,j,o=run(p,T/'k_decl_pin/exists.json')
case('T5 n output exists -> E_OUTPUT_EXISTS',j.get('code')=='E_OUTPUT_EXISTS')
f=fixture('o_src_pin',std('CDS'));p=script('o_src_pin',f);f.write_bytes(f.read_bytes()+b' ');rc,j,o=run(p,T/'o_src_pin/out.json')
case('T5 o source pin mismatch -> E_PIN',j.get('code')=='E_PIN' and o is None)
bad=T/'readme_tampered.html';bad.write_bytes(Path(README).read_bytes().replace(b'16- 21',b'17- 22',1))
expect_fail('p_cds_readme_tampered',std('CDS'),readme=(str(bad),README_SHA))
print('SUMMARY',sum(ok for _,ok,_ in res),'/',len(res),'passed')
