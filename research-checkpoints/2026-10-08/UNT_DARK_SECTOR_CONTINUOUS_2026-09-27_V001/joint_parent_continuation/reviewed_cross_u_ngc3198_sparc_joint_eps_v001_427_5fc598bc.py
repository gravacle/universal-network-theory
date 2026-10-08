"""Guarded fixed EXP24 single-EPS conditional common-parameter solve; root execution only."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,importlib,json,math,os,time,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_SPARC_JOINT_EPS_V001'
STELLAR='CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002'
OLD_SPACE='CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008'
ENGINE_NAME='cross_u_ngc3198_space_quadrature_recovery_v008'
AUTHOR_DRAFT=True
PROTOCOL_SHA='fddc1aa32e4fb9f3f6cb14e57ee17e95d153df66810d4d3a88a0d8e400cf80fe'
PROBE_STEP=1e-4
ML=.5;RD=3.14
ANCHORS={'EXP24':(24.03,.28)}
TARGET_EPS=1e-6
JOINT='constrained_u_joint_pantheon_desi_shape_v001'
np=core=native=direct=engine=None
Run=ScalarInverse=field_controls=fgmres=norm=split=join=None
OWNER=None;INPUTS={};CREATED={};RECORDS=[];CONTEXT={};RAW={};PREPARATION_RAW={}
PARENT_FINAL_REF=None;SOURCE_ID=None;CONTROL_PROBE=None;BINDING=None;SEED_INFO=None
CURRENT_QUADRATURE=2;ORIGINAL_QUADRATURE=None
INHERITED_CONFIG={'newton_cap': 40, 'backtracks': 32, 'final_original_residual': 1e-08, 'native_equilibrium_cap': 40, 'native_equilibrium_tolerance': 1e-10, 'native_trials_cap': 4096, 'native_D_cap': 600, 'native_D_true_tolerance': 1e-10, 'reduced_restart': 24, 'reduced_cap': 240, 'scalar_original_P_tolerance': 1e-10, 'scalar_corrections': 3, 'arithmetic_tolerance': 2e-11, 'energy_gradient_tolerance': 1e-07}
CONFIG=None
PHYSICAL={'source_registration_qualified': False, 'full_SPARC_model_qualified': False, 'refinement_qualified': False, 'full_metric_qualified': False, 'FLRW_junction_qualified': False, 'formation_qualified': False, 'stability_qualified': False, 'observational_qualified': False, 'joint_superiority_qualified': False}
PINS={'cross_u_ngc3198_space_quadrature_recovery_v008.py': '8ebcc132c3933aae2e4868092f13187680aeacd0d94fa74e88790fb14b4c0627', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008.md': 'a9b0780d632c351aab9820a8118ea249e06f8cfac6329db0eea9ab34bf294d80', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_RESULT.json': 'b7c1694a99aed6fbde84324ae9454b30cc50c008d49c535b9cb3603875089b7d', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_RECEIPT.json': 'fb417f6d3125db4c8d50c9157ae9a80e6fc689954c9d912338ba40e2effaedb1', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_MANIFEST.json': 'ff8226e41aabc3b6b9da006cc5a9811346f99709c85471f72a31a903e7599d46', 'cross_u_ngc3198_sparc_stellar_footprint_v002.py': '95c86130b9a348da58f2c3442b51460bdc980998b4395114a4ba3ad69ebd4ac0', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002.md': '0e17b74071cf9bfe1b9066c24ac13dd9a969f7cf21bdf1042b2afd3c6b33ccc9', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_RESULT.json': '9e74228d73b0df6312836dfced7b5053743561289a03b8b0f0245d469c34203a', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_RECEIPT.json': 'bd3f63a75dc1296ae3c6fad84bcf6b1a09c051d5a5dc8a2ee9afe9e483a775b8', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_MANIFEST.json': '31877af20581a9c63d7df0b54488e19b804369c524a7b22fe21d4ff87201b62e', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_EXP24_CASE.json': '2a25fb0da765a9db6490b912aab45cad415506a70b1cfc1a5cfb8d4fd93063a7', 'cross_u_nonzero_native_curvature_split_v001.py': 'a60415dd3983e91161b45428ce5c030ff27ec3b8dd03032aa9e42c9a30a2f028', 'cross_u_direct_scalar_proxy_controls_v001.py': '0d58dcff5ae26ba16bf6f4272144fb7a0ce4f14474ac2edfa50115f911fc7621', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00000_REUSED_SOURCE_FOOTPRINTS.npz': 'a254eac583b7fcb8147893685d2b27bcc35e6ef1388901bc24aa0139a95a796b', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00000_REUSED_SOURCE_FOOTPRINTS.npz.COMMIT.json': 'b8061d69f72302d923a45a4a8875cb687188eb3a4a9ebf13801c92eebbcd4dc7', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00001_INHERITED_NATIVE_CONTROLS.npz': 'b87c291d329929e917770431e21e1bba81ffe536521034d25848bd438d776be2', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00001_INHERITED_NATIVE_CONTROLS.npz.COMMIT.json': '5327394a63440c537ec204cef21751bf1bcbf5fb194f7bd9ccee5cbe1967b552', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00044_FINAL.npz': 'cd4cda3a48f9d104a69a25f896d11af08bf2130d35be9c356cfbc785be1a2fa6', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_00044_FINAL.npz.COMMIT.json': '0b5d5bc5f8217503731b5960f824839c9f572a50573474998eeaae8f89aadb39', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900', 'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1', 'reviewed_cross_u_ngc3198_sparc_space_quadrature_refinement_v001_389_f522fe75.py': 'f522fe750e4282e776ca16d2eba40d7ab2e4122d3e203cfa28ea6e527ef09eef', 'reviewed_CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_25_7e822490.md': '7e8224907b7fb2e8f898d8f873a4c66d68719d176c970b5fcc0565239b45641f', 'cross_u_ngc3198_sparc_space_quadrature_refinement_v001.py': 'e77230a1819e89799e4463d5ca3808b1cab9f6a2c9166b593cbca2b949dec853', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001.md': '3ffc808394102d8b7479d9e1f604ba940e0ac7570181f1c386fb5eddc2c5e729', 'constrained_u_joint_pantheon_desi_shape_v001_RESULT.json': '8e8f37664e5eed4647a259468678b1c997805d1171c5fb26f5f2c7d2dc8a109d', 'constrained_u_joint_pantheon_desi_shape_v001_RECEIPT.json': 'f7cf2b89ab28e5558a1e7fb74bd6bba643b8c438c649fde35ec95e9c9ee0a006', 'CONSTRAINED_U_JOINT_PANTHEON_DESI_SHAPE_V001.md': '6f8869df3f6cc58deda9b73c566c697452988dcdd208c76d5630d6e6799e1820'}
CORE_INPUT_PINS={'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900'}
RECEIPT_EXPECTATIONS={'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'NEW_BBN_ACOUSTIC_ARITHMETIC_PASS'}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'NEW_ATOMIC_PAIR_ARITHMETIC_PASS'}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'FIXED_NEVO_NEW_ACTION_NUMERICALLY_QUALIFIED'}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'NEW_FIXED_PANTHEON_PROFILE_ARITHMETIC_PASS'}, 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'NEW_ATOMIC_PAIR_ARITHMETIC_PASS'}, 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': {'owner_kind': 'str', 'pid': 39330, 'status': 'NUMERICAL_PASS'}, 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001_RECEIPT.json': {'owner_kind': 'dict', 'pid': 56449, 'status': 'CLOSED'}, 'CROSS_U_NGC3198_DIRECT_SCALAR_RECOVERY_V005_RECEIPT.json': {'owner_kind': 'str', 'pid': 57478, 'status': None}, 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json': {'owner_kind': 'str', 'pid': 49006, 'status': None}, 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RECEIPT.json': {'owner_kind': 'dict', 'pid': 62181, 'status': 'CLOSED'}, 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RECEIPT.json': {'owner_kind': 'str', 'pid': 42114, 'status': None}, 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json': {'owner_kind': 'str', 'pid': 42904, 'status': None}, 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_RECEIPT.json': {'owner_kind': 'dict', 'pid': 63945, 'status': 'CLOSED'}, 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V001_RECEIPT.json': {'owner_kind': 'dict', 'pid': 76290, 'status': 'CLOSED'}, 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_RECEIPT.json': {'owner_kind': 'dict', 'pid': 76996, 'status': 'CLOSED'}, 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json': {'owner_kind': 'str', 'pid': 50386, 'status': None}, 'CROSS_U_Q1_PROJECTION_STIFFNESS_V001_RECEIPT.json': {'owner_kind': 'str', 'pid': 47083, 'status': None}, 'NGC3198_STATIONARY_LAPSE_SPAN_V001_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'PASS'}, 'constrained_u_joint_pantheon_desi_shape_v001_RECEIPT.json': {'status': 'NUMERICAL_PASS', 'owner_kind': 'dict', 'pid': 58860}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_DESI_BAO_V002_RECEIPT.json': {'owner_kind': 'NoneType', 'status': 'NEW_BBN_PREDICTED_RULER_BAO_ARITHMETIC_PASS'}, 'CONSTRAINED_U_PANTHEON_FLAT_LCDM_PROFILE_V001_RECEIPT.json': {'owner_kind': 'dict', 'pid': 55862, 'status': 'NUMERICAL_PASS'}}

def now():return datetime.now(timezone.utc).isoformat()
def finite(v):return float(v) if math.isfinite(float(v)) else None

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
    if np is not None and isinstance(v,np.generic):return canonical(v.item())
    if v is None or type(v) in (str,bool,int):return v
    if type(v) is float:assert math.isfinite(v);return v
    raise TypeError(type(v).__name__)

def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(name,v):
    raw=encode(v);p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);assert p.read_bytes()==raw;CREATED[name]=sha(p);return CREATED[name]

def receipt_maps(name):
    r=json.loads((BASE/name).read_text());expect=RECEIPT_EXPECTATIONS[Path(name).name]
    assert r.get('status')==expect['status'] and type(r.get('owner')).__name__==expect['owner_kind']
    owner=r.get('owner')
    if isinstance(owner,str):assert owner=='root' and r['pid']==expect['pid'] and r['pid']>0 and r['closed']>r['started']
    elif isinstance(owner,dict):
        assert owner.get('owner','root')=='root' and owner['pid']==expect['pid'] and owner['pid']>0
        assert r.get('closed',r.get('finished_utc'))>owner.get('started',owner.get('started_utc'))
    else:assert expect['owner_kind']=='NoneType' and 'owner' not in r  # Owned historical status/manifest schemas retained literally.
    ins=dict(r.get('input_sha256',r.get('pins',{})));outs=r['output_sha256'];assert outs
    for key,h in outs.items():assert sha(BASE/key)==h
    # Old receipts use absolute output paths; compare the literal immutable manifest.
    basename=Path(name).name[:-len('_RECEIPT.json')]+'_MANIFEST.json';found=[key for key in outs if Path(key).name==basename]
    if found:
        assert len(found)==1;key=found[0];m=json.loads((BASE/key).read_text())
        if 'manifest' in r:assert r['manifest']==m
        if 'manifest_sha256' in r:assert r['manifest_sha256']==outs[key]
        for key,h in dict(m.get('input_sha256',{}),**m.get('inherited_input_sha256',{})).items():
            assert key not in ins or ins[key]==h;ins[key]=h
    return dict(ins,**outs)

def resolve_inputs():
    merged=dict(PINS,**{STEM+'.md':PROTOCOL_SHA});todo=[STELLAR+'_RECEIPT.json',OLD_SPACE+'_RECEIPT.json',JOINT+'_RECEIPT.json'];done=set()
    while todo:
        n=todo.pop();assert sha(BASE/n)==merged[n]
        if n in done:continue
        done.add(n)
        for key,h in receipt_maps(n).items():
            assert len(h)==64 and (key not in merged or merged[key]==h),(key,'conflicting seal')
            merged[key]=h
            if key.endswith('_RECEIPT.json') and key not in done:todo.append(key)
    for n,h in merged.items():assert sha(BASE/n)==h,('input changed',n)
    return merged

def authenticate():
    assert not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64
    for n,h in INPUTS.items():assert sha(BASE/n)==h,('changed input',n)
    if OWNER is not None:assert sha(__file__)==OWNER['source_sha256']


def parent_binding():
    rc=json.loads((BASE/(STELLAR+'_RECEIPT.json')).read_text())
    case=json.loads((BASE/(STELLAR+'_EXP24_CASE.json')).read_text())
    manifest=json.loads((BASE/(STELLAR+'_MANIFEST.json')).read_text())
    assert rc['status']=='CLOSED' and rc['owner']['pid']==76996 and rc['result_sha256']==INPUTS[STELLAR+'_RESULT.json']
    assert manifest['owner']==rc['owner']
    registered=dict(manifest['source_identity']);physical=case['identity']['source_identity']
    assert set(registered)-set(physical)=={'control_registration','recovery_law_changes','recovery_parent_final'}
    registration=registered.pop('control_registration');law_changes=registered.pop('recovery_law_changes');old_final=registered.pop('recovery_parent_final')
    assert registered==physical and law_changes==[] and old_final==manifest['parent_final']
    assert set(registration)=={'step','signs','direction_parent'} and registration['step']==PROBE_STEP and registration['signs']==[1,-1]
    direction_parent=registration['direction_parent']
    for inherited in (old_final,direction_parent):
        assert INPUTS[inherited['file']]==inherited['sha256'] and INPUTS[inherited['commit_file']]==inherited['commit_sha256']
        assert json.loads((BASE/inherited['commit_file']).read_text())=={k:v for k,v in inherited.items() if k not in ('commit_file','commit_sha256')}
    assert old_final['metadata']['status']==case['historical_status'] and old_final['metadata']['history']==[] and old_final['metadata']['source_identity']==physical
    assert direction_parent['metadata']['kind']=='implementation_controls' and direction_parent['metadata']['controls']==case['historical_native_controls']
    assert manifest['historical_native_controls']==case['historical_native_controls']
    assert case['status']=='CONVERGED' and case['numerical_residual']<=1e-8 and len(case['history'])==4
    assert len(case['source_controls'])==20 and len(case['controls'])==20 and all(v['passed'] for v in case['source_controls']+case['controls'])
    assert len(case['historical_native_controls'])==3 and [v['passed'] for v in case['historical_native_controls']]==[False,True,True]
    assert case['historical_status']=='NATIVE_IMPLEMENTATION_FAILED' and len(case['rows'])==43
    assert case['readout_qualified'] is False and case['physical_flags']==rc['physical_flags']==PHYSICAL
    old=case['identity'];source=old['source_identity']
    assert old['eps']==source['eps']==1e-5 and old['hi_tail'] is False and old['h2_tail'] is False
    assert old['grid_shape']==source['grid_shape']==[65,87,45] and source['native_modes']==32
    assert source['source_id']=='EXP24' and source['M_to_L']==ML and source['Rd_kpc']==RD and source['anchor']==list(ANCHORS['EXP24']) and source['law_changes']==[]
    records=case['own_checkpoints'];assert len(records)==45 and records[0]==case['source_checkpoint'] and records[-1]==case['final_checkpoint']
    for rec in records:
        assert rc['output_sha256'][rec['file']]==INPUTS[rec['file']]==rec['sha256']
        assert rc['output_sha256'][rec['commit_file']]==INPUTS[rec['commit_file']]==rec['commit_sha256']
        assert json.loads((BASE/rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
    final=records[-1];meta=final['metadata']
    assert final['file']==STELLAR+'_00044_FINAL.npz' and meta['kind']=='final_state_and_signed_readouts'
    assert meta['status']==case['status'] and meta['identity']==old and meta['history']==case['history'] and meta['rows']==case['rows'] and meta['error']==case['numerical_residual']
    assert records[0]['metadata']['controls']==case['source_controls'] and records[0]['metadata']['summaries']==case['source_summaries']
    assert records[1]['metadata']['controls']==case['historical_native_controls'] and records[1]['metadata']['not_promoted'] is True
    assert direction_parent==records[1]['metadata']['parent_record']
    # The immutable 414MB result is authenticated as a whole byte binding; the independently sealed CASE and all45 pair dictionaries are the admitted payload.
    return dict(identity=old,status=case['status'],numerical_residual=case['numerical_residual'],rows=case['rows'],controls=case['controls'],source_controls=case['source_controls'],source_summaries=case['source_summaries'],historical_native_controls=case['historical_native_controls'],historical_status=case['historical_status'],source_record=records[0],historical_record=records[1],final_record=final,parent_case_file=STELLAR+'_EXP24_CASE.json',parent_case_sha256=INPUTS[STELLAR+'_EXP24_CASE.json'],physical_flags=case['physical_flags'],native_trials=case['native_trials'])

def parent_ref(rec):return {k:rec[k] for k in ('file','sha256','commit_file','commit_sha256')}

def checkpoint(tag,arrays,meta):
    data=canonical(dict(meta,owner=OWNER,parent_final=PARENT_FINAL_REF,source_identity=SOURCE_ID,control_probe=CONTROL_PROBE,
      seed_registration=SEED_INFO,schema={k:dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a)))) for k,a in arrays.items()}))
    text=encode(data).decode();data=json.loads(text);p=BASE/f'{STEM}_{len(RECORDS):05d}_{tag}.npz'
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p);rec=dict(file=p.name,sha256=CREATED[p.name],metadata=data)
    ch=publish(p.name+'.COMMIT.json',rec);rec=dict(rec,commit_file=p.name+'.COMMIT.json',commit_sha256=ch);RECORDS.append(rec)
    with np.load(p,allow_pickle=False) as z:
        assert str(z['metadata'])==text and set(z.files)==set(arrays)|{'metadata'}
        for k,a in arrays.items():assert np.array_equal(z[k],a,equal_nan=True)
    return rec

def recheck():
    authenticate();assert resolve_inputs()==INPUTS
    for n,h in CREATED.items():assert sha(BASE/n)==h
    for rec in RECORDS:
        assert json.loads((BASE/rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
        with np.load(BASE/rec['file'],allow_pickle=False) as z:
            assert json.loads(str(z['metadata']))==rec['metadata'] and set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
            for k,s in rec['metadata']['schema'].items():
                a=z[k];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
        state=rec['metadata'].get('physical_state_checkpoint')
        if state is not None:assert state in RECORDS
        factor=rec['metadata'].get('factor_checkpoint')
        if factor is not None:assert factor in RECORDS
    assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={v['file'] for v in RECORDS}
    assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={v['commit_file'] for v in RECORDS}
    if STEM+'_OWNER_START.json' in CREATED:assert json.loads((BASE/(STEM+'_OWNER_START.json')).read_text())==OWNER

def read_pair(rec,label):
    arrays={}
    with np.load(BASE/rec['file'],allow_pickle=False) as z:
        assert set(z.files)==set(rec['metadata']['schema'])|{'metadata'}
        for name in rec['metadata']['schema']:
            arrays[name]=z[name].copy();RAW[label+'_'+name]=arrays[name].copy()
        assert json.loads(str(z['metadata']))==rec['metadata']
    for name,a in arrays.items():assert rec['metadata']['schema'][name]==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
    return arrays

def registered_native_controls(model,x):
    global CONTROL_PROBE
    physical=RECORDS[-1];assert physical['metadata']['kind']=='numerical_initial_guess'
    ir,iz=np.indices(model.mask[0].shape);jj=np.arange(32)[:,None,None]
    d=np.zeros_like(x);d[1::2]=model.sw*model.xi[:,None,None]**2*np.sin(.07*(jj+1)+.13*ir+.05*iz)
    d[2::2]=model.sw*model.xi[:,None,None]**2*np.cos(.09*(jj+1)+.03*ir+.11*iz);d[~model.mask]=0
    RAW['control_direction']=d.copy();assert np.all(d[0]==0) and np.all(np.isfinite(d))
    rows=[]
    for sign,label in ((1,'PLUS'),(-1,'MINUS')):
        CONTEXT.update(stage='registered_native_controls',probe=label)
        probe=x+sign*PROBE_STEP*d;RAW['control_probe_'+label]=probe.copy()
        assert np.array_equal(probe[0],x[0]) and np.all(probe[~model.mask]==0)
        rec=checkpoint('CONTROL_STATE_'+label,dict(physical_state=x,probe_state=probe,direction=d),dict(kind='synthetic_native_control_state',probe=label,sign=sign,step=PROBE_STEP,physical_state_checkpoint=physical,not_physical_state=True,direction_source_sha256=INPUTS[ENGINE_NAME+'.py']))
        CONTROL_PROBE=dict(label=label,sign=sign,step=PROBE_STEP,state_checkpoint=rec,physical_input=physical)
        try:controls=engine.native_controls(model,probe)
        finally:CONTROL_PROBE=None
        operand=RECORDS[-1];assert len(controls)==3 and operand['metadata']['kind']=='implementation_controls' and operand['metadata']['controls']==controls
        arrays=read_pair(operand,'control_'+label);assert np.array_equal(arrays['direction'],d) and np.array_equal(arrays['state'],probe)
        rows.extend(dict(v,probe_label=label,probe_sign=sign,probe_state_checkpoint=rec,operand_checkpoint=operand) for v in controls)
    assert len(rows)==6;return rows

def compare_rows(left_name,left,right_name,right):
    out=[]
    for a,b in zip(left,right):
        assert all(a[k]==b[k] for k in ('R_kpc','observed_velocity_kms','observed_error_kms'))
        row={k:a[k] for k in ('R_kpc','observed_velocity_kms','observed_error_kms')};budget=max(.1,.1*a['observed_error_kms']);row['numerical_comparison_budget_kms']=budget
        for label in ('Q1_left','Q1_right','legacy'):
            av,bv=a[label+'_velocity'],b[label+'_velocity'];dv=None if av is None or bv is None else bv-av
            row[label+'_velocity_difference_kms']=dv;row[label+'_force_difference_a0']=b[label+'_force_a0']-a[label+'_force_a0']
            row[label+'_v2_difference']=b[label+'_v2']-a[label+'_v2'];row[label+'_within_comparison_budget']=False if dv is None else abs(dv)<=budget
            row[label+'_reason']=None if dv is not None else 'Negative signed v2 in a retained field; no velocity clipping'
        out.append(row)
    assert len(out)==43;return dict(left=left_name,right=right_name,rows=out,physical_refinement_qualified=False)



def solve(run,x):
    model=run.model;history=[];status='NATIVE_IMPLEMENTATION_FAILED'
    run.current_state_checkpoint=checkpoint('INPUT',dict(state=x),dict(kind='numerical_initial_guess',identity=run.identity,parent_binding=BINDING,numerical_guess_only=True,not_cosmological_preparation=True))
    controls=registered_native_controls(model,x)
    if not all(c['passed'] for c in controls):return x,status,history,controls
    x,eq=run.equilibrate(x,'initial_fixed_potential')
    if not eq['ok']:return x,'NATIVE_EQUILIBRIUM_FAILED',history,controls
    initial_eq=eq;status='NEWTON_ALLOWANCE'
    run.current_state_checkpoint=checkpoint('EQUILIBRATED_INITIAL',dict(state=x),dict(kind='outer_base',identity=run.identity,native_equilibrium=eq))
    for outer in range(CONFIG['newton_cap']):
        CONTEXT.update(outer=outer,stage='reduced_Newton');r,pre,H=model.residual(x);root=np.sqrt(pre);error=norm(r/root)/run.scale
        if not math.isfinite(error):
            checkpoint('ORIGINAL_NORM_FAILED',dict(state=x,residual=r,pre=pre),dict(kind='original_full_norm_refusal',identity=run.identity,unaccepted=True,reason='Nonfinite original normalized residual; raw arrays retained'));status='ORIGINAL_NORM_FAILED';break
        if error<=CONFIG['final_original_residual']:status='CONVERGED';break
        target=min(.5,max(1e-6,.5*math.sqrt(error)));block=None
        try:
            block=ScalarInverse(model,x,root);block.case_identity=run.identity;block.physical_state_checkpoint=run.current_state_checkpoint;block.prepare(x)
        except (ValueError,AssertionError,FloatingPointError):
            checkpoint('SCALAR_FACTOR_FAILED',getattr(block,'arrays',{}),dict(kind='scalar_factor_refusal',identity=run.identity,physical_state_checkpoint=run.current_state_checkpoint,outer=outer,unaccepted=True,controls=getattr(block,'controls',[]),factor=getattr(block,'factor_info',None),context=dict(CONTEXT),traceback=traceback.format_exc()));status='SCALAR_FACTOR_FAILED';break
        block.factor_record=checkpoint('SCALAR_FACTOR',block.arrays,dict(kind='scalar_proxy_factor',identity=run.identity,physical_state_checkpoint=run.current_state_checkpoint,outer=outer,controls=block.controls,factor=block.factor_info))
        controls+=block.controls
        if outer==0:controls+=field_controls(block,H)
        if not all(c['passed'] for c in controls):status='BLOCK_IMPLEMENTATION_FAILED';break
        forms=block.forms;rv=split(r);saved=dict(state=x,original_residual=r,whitening_pre=pre,whitening_root=root)
        try:
            t,first=run.Dsolve(forms,rv,['Schur_rhs',outer]);bred=-r[0]-block.BT(t);saved['native_rhs_response']=t;saved['reduced_physical_rhs']=bred;bn=bred/root[0]
            calls=[]
            def A(v):
                p=v/root[0];response,info=run.Dsolve(forms,block.B(p),['Schur_action',outer,len(calls)]);calls.append(info)
                return (block.K(p)-block.mass(p)-block.BT(response))/root[0]
            def M(v):
                p,info=block.scalar(root[0]*v);return root[0]*p,info
            dpwhite,lin=fgmres(A,bn,M,np.zeros_like(bn),target,restart=CONFIG['reduced_restart'],cap=CONFIG['reduced_cap']);saved['reduced_whitened_partial']=dpwhite
            dp=dpwhite/root[0];dv,last=run.Dsolve(forms,block.B(dp)-rv,['full_reconstruction',outer]);delta=join(model,dp,dv);saved['full_physical_direction']=delta
            hd=H(delta);saved['original_full_H_action']=hd;b=-r/root;cert=norm((hd+r)/root)/norm(b)
            row=dict(outer=outer,error=error,inexact_target=target,reduced_linear=lin,native_rhs_linear=first,native_action_linears=calls,native_reconstruction_linear=last,original_full_H_error=finite(cert),full_linear_pass=math.isfinite(cert) and cert<=target and lin['ok'])
            checkpoint('REDUCED_LINEAR',saved,dict(kind='reduced_linear_certificate',identity=run.identity,outer=outer,row=row,unaccepted=not row['full_linear_pass']))
        except (ValueError,AssertionError,FloatingPointError):
            checkpoint('REDUCED_LINEAR_FAILED',saved,dict(kind='reduced_linear_refusal',identity=run.identity,outer=outer,unaccepted=True,context=dict(CONTEXT),traceback=traceback.format_exc()));status='LINEAR_FAILED';break
        if not row['full_linear_pass']:history.append(row);status='LINEAR_FAILED';break
        accepted=False;row['trials']=[]
        for back in range(CONFIG['backtracks']):
            step=2.**(-back);candidate=x+step*delta
            try:
                model.clock(candidate[0]);candidate,eq=run.equilibrate(candidate,['outer_trial',outer,back])
                if not eq['ok']:trial=dict(backtrack=back,step=step,accepted=False,reason='native_equilibrium_refusal',native_equilibrium=eq)
                else:
                    cr,_=model.residual(candidate,False);ce=norm(cr/root)/run.scale;accepted=math.isfinite(ce) and ce<=(1-1e-4*step)*error
                    trial=dict(backtrack=back,step=step,accepted=accepted,original_full_error=finite(ce),native_equilibrium=eq)
            except (ValueError,AssertionError,FloatingPointError) as exc:accepted=False;trial=dict(backtrack=back,step=step,accepted=False,reason=type(exc).__name__)
            checkpoint('OUTER_TRIAL',dict(base_state=x,candidate=candidate,direction=delta),dict(kind='outer_trial',identity=run.identity,outer=outer,trial=trial,unaccepted=not accepted));row['trials'].append(trial)
            if accepted:x=candidate;row.update(step=step,candidate_error=ce);break
        row['accepted']=accepted;history.append(row)
        if not accepted:status='GLOBALIZATION_FAILED';break
        run.current_state_checkpoint=checkpoint('OUTER_ACCEPTED',dict(state=x),dict(kind='outer_accepted',identity=run.identity,outer=outer+1,history=history))
        print('NATIVE_ELIMINATION','NEWTON',outer+1,'ERROR',ce,'STEP',step,flush=True)
    return x,status,history,controls

def selected_quadrature(r,z):
    if CURRENT_QUADRATURE==2:return ORIGINAL_QUADRATURE(r,z)
    nodes,weights=np.polynomial.legendre.leggauss(3);out=[]
    for u,wu in zip(nodes,weights):
        for v,wv in zip(nodes,weights):
            dr=np.diff(r)[:,None];dz=np.diff(z)[None,:]
            rr=(r[:-1,None]+r[1:,None])/2+u*dr/2
            volume=rr*dr*dz*wu*wv/4;shapes=[]
            for i,j in ((0,0),(1,0),(0,1),(1,1)):
                si=1 if i else -1;sj=1 if j else -1
                shapes.append(((1+si*u)*(1+sj*v)/4,si*(1+sj*v)/(2*dr),sj*(1+si*u)/(2*dz),i,j))
            assert np.all(volume>0) and np.all(np.isfinite(volume));out.append((rr,volume,shapes))
    assert len(out)==9;return out

def warm_start(x,r,z,refine):
    PREPARATION_RAW.clear();PREPARATION_RAW.update(coarse_state=x,coarse_r=r,coarse_z=z)
    if not refine:return x.copy(),r.copy(),z.copy(),dict(nested=False,retained_nodes_exact=True)
    rr=np.sort(np.r_[r,(r[:-1]+r[1:])/2]);zz=np.sort(np.r_[z,(z[:-1]+z[1:])/2]);PREPARATION_RAW.update(new_r=rr,new_z=zz)
    temp=np.empty((x.shape[0],len(rr),len(z)));out=np.empty((x.shape[0],len(rr),len(zz)))
    for c in range(x.shape[0]):
        for k in range(len(z)):temp[c,:,k]=np.interp(rr,r,x[c,:,k])
        for k in range(len(rr)):out[c,k,:]=np.interp(zz,z,temp[c,k,:])
    PREPARATION_RAW['prolonged_state']=out
    assert np.array_equal(rr[::2],r) and np.array_equal(zz[::2],z) and np.array_equal(out[:,::2,::2],x)
    return out,rr,zz,dict(nested=True,retained_nodes_exact=True)

def footprint(photometry,label):
    # Only radius and SBdisk enter this constructor, never Vobs or velocity components.
    assert photometry.shape==(43,2)
    if label=='ROUND43':data=photometry.copy();tail=None
    else:
        ar,sb=ANCHORS[label];loc=np.flatnonzero(photometry[:,0]==ar);assert len(loc)==1 and photometry[loc[0],1]==sb
        data=photometry[:loc[0]+1].copy();tail=RD
    return core.density.Profile(data[:,0],ML*data[:,1],tail),data

def readouts(model,x,observations):
    psi=x[0,:,0].copy();RAW['final_midplane_psi']=psi
    slopes=np.diff(psi)/np.diff(model.r);RAW['final_cell_slopes']=slopes
    oldgrad=np.gradient(psi,model.r,edge_order=2);RAW['final_legacy_nodal_gradient']=oldgrad
    assert np.all(np.isfinite(slopes)) and np.all(np.isfinite(oldgrad))
    signed=[];rows=[]
    for R,V,E,*unused in observations:
        R=float(R);V=float(V);E=float(E);matches=np.flatnonzero(model.r==R)
        if len(matches):
            k=int(matches[0]);assert 0<k<len(model.r)-1;left=float(slopes[k-1]);right=float(slopes[k]);cell=None;node=k
        else:
            k=int(np.searchsorted(model.r,R,side='right')-1);assert 0<=k<len(slopes);left=right=float(slopes[k]);cell=k;node=None
        old=float(np.interp(R,model.r,oldgrad));v2s=[R*core.A0_V*g for g in (left,right,old)]
        signed.append([R,V,E,left,right,old,*v2s]);RAW['final_observed_signed_forces']=np.array(signed)
        assert all(math.isfinite(t) for t in v2s)
        vs=[math.sqrt(v) if v>=0 else None for v in v2s]
        rows.append(dict(R_kpc=R,observed_velocity_kms=V,observed_error_kms=E,cell_index=cell,exact_node_index=node,Q1_left_force_a0=left,Q1_right_force_a0=right,legacy_force_a0=old,Q1_left_v2=v2s[0],Q1_right_v2=v2s[1],legacy_v2=v2s[2],Q1_left_velocity=vs[0],Q1_right_velocity=vs[1],legacy_velocity=vs[2],Q1_left_residual=None if vs[0] is None else vs[0]-V,Q1_right_residual=None if vs[1] is None else vs[1]-V,legacy_residual=None if vs[2] is None else vs[2]-V,negative_force_left=left<0,negative_force_right=right<0,negative_force_legacy=old<0))
    assert len(rows)==43
    return rows

def seed_admission(model,warm):
    rows=[]
    for index in range(9):
        CONTEXT.update(stage='fixed_clock_seed_admission',seed_index=index)
        lam=math.ldexp(1.,-index);candidate=lam*warm;RAW['seed_candidate']=candidate.copy()
        assert candidate.shape==model.shape and np.all(np.isfinite(candidate)) and np.all(candidate[~model.mask]==0)
        if index==0:assert np.array_equal(candidate,warm)
        rec=checkpoint('SEED_CANDIDATE',dict(inherited_warm=warm,numerical_candidate=candidate),dict(kind='unaccepted_numerical_guess_candidate',seed_index=index,scale=lam,numerical_guess_only=True,all_fields_scaled=True,target_eps=TARGET_EPS))
        try:
            clock=model.clock(candidate[0])
        except (ValueError,AssertionError,FloatingPointError) as exc:
            row=dict(seed_index=index,scale=lam,admitted=False,reason=type(exc).__name__,message=str(exc),candidate_checkpoint=rec)
            refused=checkpoint('SEED_REFUSED',dict(numerical_candidate=candidate),dict(kind='strict_target_clock_refusal',row=row,numerical_guess_only=True,unaccepted=True,traceback=traceback.format_exc()))
            row['refusal_checkpoint']=refused;rows.append(row);continue
        clock_arrays={}
        for name,a in zip(('rho','pressure','D','W','density_difference','pressure_difference'),clock):
            RAW['seed_clock_'+name]=a.copy();clock_arrays['clock_'+name]=a.copy()
        row=dict(seed_index=index,scale=lam,admitted=True,reason='First fixed-ladder candidate accepted by unchanged strict target Model.clock',candidate_checkpoint=rec)
        accepted=checkpoint('SEED_ADMITTED',dict(numerical_guess=candidate,**clock_arrays),dict(kind='strict_domain_admitted_numerical_guess',row=row,numerical_guess_only=True,not_cosmological_preparation=True))
        row['admission_checkpoint']=accepted;rows.append(row);return candidate,rows
    return None,rows

def main():
    global np,core,native,direct,engine,OWNER,INPUTS,PARENT_FINAL_REF,SOURCE_ID,ORIGINAL_QUADRATURE,CURRENT_QUADRATURE
    global Run,ScalarInverse,field_controls,fgmres,norm,split,join,CONFIG,BINDING,SEED_INFO
    assert not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64
    assert not list(BASE.glob(STEM+'_*')),'Existing runtime namespace preserved'
    INPUTS=resolve_inputs();parent=parent_binding();PARENT_FINAL_REF=parent_ref(parent['final_record']);BINDING=PARENT_FINAL_REF;source=sha(__file__)
    SOURCE_ID=dict(parent['identity']['source_identity'],eps=TARGET_EPS,global_EPS_trial=dict(from_eps=parent['identity']['eps'],to_eps=TARGET_EPS,other_parameters_changed=False),warm_parent_eps=parent['identity']['eps'])
    joint=json.loads((BASE/(JOINT+'_RESULT.json')).read_text());jrc=json.loads((BASE/(JOINT+'_RECEIPT.json')).read_text())
    assert jrc['status']=='NUMERICAL_PASS' and jrc['result_sha256']==INPUTS[JOINT+'_RESULT.json'] and joint['status']=='NUMERICAL_PASS'
    assert [v['eps'] for v in joint['native_rows']]==[1e-6,1e-5,1e-4,1e-3] and all(v is False for v in joint['physical_flags'].values())
    late_reference=dict(result_file=JOINT+'_RESULT.json',result_sha256=INPUTS[JOINT+'_RESULT.json'],receipt_file=JOINT+'_RECEIPT.json',receipt_sha256=INPUTS[JOINT+'_RECEIPT.json'],scope=joint['scope'],physical_flags=joint['physical_flags'],fixed_candidates=[dict(eps=v['eps'],primary_joint_score=v['primary_joint_score'],E_today=v['E_today'],H_reference=v['H_reference']) for v in joint['native_rows']])
    OWNER=dict(owner='root',pid=os.getpid(),source_sha256=source,started=now());tick=time.monotonic();cases=[]
    try:
        publish(STEM+'_OWNER_START.json',OWNER)
        manifest=dict(owner=OWNER,input_sha256=INPUTS,parent_final=PARENT_FINAL_REF,parent_case_file=parent['parent_case_file'],parent_case_sha256=parent['parent_case_sha256'],source_identity=SOURCE_ID,inherited_warm_eps=parent['identity']['eps'],target_eps=TARGET_EPS,source_controls_copied=parent['source_controls'],historical_native_controls=parent['historical_native_controls'],historical_status=parent['historical_status'],numerical_seed_ladder=dict(count=9,scales=[math.ldexp(1.,-i) for i in range(9)],all65_fields_scaled=True,first_strict_clock_admissible_only=True,numerical_guess_only=True),late_joint_reference=late_reference,numerical_configuration=INHERITED_CONFIG,control_registration=dict(step=PROBE_STEP,signs=[1,-1],direction_source_sha256=INPUTS[ENGINE_NAME+'.py']),physical_flags=PHYSICAL,no_automatic_resume=True)
        publish(STEM+'_MANIFEST.json',manifest);authenticate()
        np=importlib.import_module('numpy');core=importlib.import_module('cross_u_ngc3198_nonlinear_disk_v001')
        native=importlib.import_module('cross_u_nonzero_native_curvature_split_v001');native.np=np;native.core=core
        direct=importlib.import_module('cross_u_direct_scalar_proxy_controls_v001');direct.np=np;direct.core=core;direct.native=native
        engine=importlib.import_module(ENGINE_NAME);engine.np=np;engine.core=core;engine.native=native;engine.direct=direct;engine.checkpoint=checkpoint;engine.CONTEXT=CONTEXT;engine.BINDING=PARENT_FINAL_REF
        for name in ('Run','ScalarInverse','field_controls','fgmres','norm','split','join','CONFIG'):globals()[name]=getattr(engine,name)
        assert CONFIG==INHERITED_CONFIG;core.authenticate();assert core.PINS==CORE_INPUT_PINS;authenticate()
        ORIGINAL_QUADRATURE=core.shape_quadrature;CURRENT_QUADRATURE=2
        source_arrays=read_pair(parent['source_record'],'inherited_sources');history_arrays=read_pair(parent['historical_record'],'historical_native');final_arrays=read_pair(parent['final_record'],'inherited_final')
        warm=final_arrays['final_state'].copy();r=source_arrays['r_kpc'].copy();z=source_arrays['z_kpc'].copy();observations=source_arrays['official_rotmod'].copy();photometry=source_arrays['photometry_only'].copy();rhs=final_arrays['final_rhs'].copy()
        RAW['unmodified_inherited_warm']=warm.copy();RAW['inherited_r']=r.copy();RAW['inherited_z']=z.copy()
        assert warm.shape==(65,87,45) and np.all(np.isfinite(warm)) and observations.shape==(43,8) and np.array_equal(photometry,observations[:,[0,6]])
        assert np.array_equal(r,np.array(parent['identity']['r_kpc'])) and np.array_equal(z,np.array(parent['identity']['z_kpc'])) and np.array_equal(final_arrays['final_midplane_psi'],warm[0,:,0])
        for row,observed in zip(parent['rows'],observations):assert [row['R_kpc'],row['observed_velocity_kms'],row['observed_error_kms']]==[float(v) for v in observed[:3]]
        checkpoint('REUSED_SOURCE_FOOTPRINTS',source_arrays,dict(kind='copied_successful_source_controls',parent_record=parent_ref(parent['source_record']),controls=parent['source_controls'],summaries=parent['source_summaries'],not_recomputed=True))
        checkpoint('HISTORICAL_NATIVE_CONTROLS',history_arrays,dict(kind='copied_historical_native_controls',parent_record=parent_ref(parent['historical_record']),controls=parent['historical_native_controls'],not_recomputed=True,not_promoted=True))
        warm_rec=checkpoint('INHERITED_WARM',dict(unmodified_warm=warm,r_kpc=r,z_kpc=z,official_rotmod=observations,photometry=photometry),dict(kind='inherited_numerical_guess_before_target_domain',parent_record=PARENT_FINAL_REF,inherited_eps=parent['identity']['eps'],target_eps=TARGET_EPS,numerical_guess_only=True,not_cosmological_preparation=True))
        old=parent['identity'];fixed=SOURCE_ID['inherited_fixed'];oldprofiles=core.density.profiles(False,False);star,data=footprint(photometry,'EXP24');profiles=dict(oldprofiles,stars=star)
        CONTEXT.update(stage='target_model');model=core.Model(r,z,32,TARGET_EPS,fixed,profiles);model.fgmres_fixed=fixed
        RAW.update(target_rhs=model.rhs.copy(),target_mask=model.mask.copy(),target_weights=model.w.copy(),target_xi=model.xi.copy())
        assert model.ep==TARGET_EPS and len(model.xi)==32 and np.all(model.w>0) and np.array_equal(model.rhs,rhs)
        assert np.all(warm[~model.mask]==0) and all(model.source_checks[k]<=1e-11 for k in ('surface_quadrature_relative','exact_annular_mass_relative','weight_sum_error')) and model.source_checks['positive_weights']
        target_clock=dict(eps=model.ep,Neps=model.norm,s0=model.s0,u0=model.u0,A=model.A,kappa=model.kappa,B=core.B,rho0=model.rho0,pressure0=model.p0,strict_psi_lower=math.log1p((model.u0-model.ep)/(1+model.ep))/(2*core.B),strict_psi_upper=math.log1p(model.u0)/(2*core.B),actual_clock_source_sha256=INPUTS['cross_u_ngc3198_nonlinear_disk_v001.py'])
        input_rec=checkpoint('TARGET_INPUT',dict(inherited_warm=warm,rhs=model.rhs,r_kpc=r,z_kpc=z,mask=model.mask,xi=model.xi,weight=model.w,photometry=photometry,stellar_profile_prefix=data),dict(kind='fixed_target_source_and_law_before_seed_admission',target_clock=target_clock,source_checks=model.source_checks,numerical_guess_only=True,inherited_warm_checkpoint=warm_rec))
        x,seed_rows=seed_admission(model,warm);SEED_INFO=dict(target_eps=TARGET_EPS,inherited_eps=parent['identity']['eps'],numerical_guess_only=True,not_cosmological_preparation=True,rows=seed_rows,chosen_index=None if x is None else seed_rows[-1]['seed_index'],chosen_scale=None if x is None else seed_rows[-1]['scale'],input_checkpoint=input_rec)
        base_parent=dict(file=parent['parent_case_file'],sha256=parent['parent_case_sha256'],final=PARENT_FINAL_REF,status=parent['status'],numerical_residual=parent['numerical_residual'],rows=parent['rows'],physical_flags=parent['physical_flags'])
        identity=dict(case='E1em06_SPARC_EXP24_HI0_H20_COARSE_Q2',eps=TARGET_EPS,hi_tail=False,h2_tail=False,grid_shape=list(model.shape),r_kpc=r.tolist(),z_kpc=z.tolist(),Hunit=old['Hunit'],source_identity=SOURCE_ID,joint_eps_source_sha256=source,joint_eps_manifest_sha256=CREATED[STEM+'_MANIFEST.json'],source_parent_final=PARENT_FINAL_REF,space_refined=False,quadrature_order=2,numerical_seed_registration=SEED_INFO)
        if x is None:
            status='TARGET_CLOCK_DOMAIN_REFUSED';history=[];controls=[];rows=[];error=None;formal={};native_trials=0;Dfail=[]
            final=checkpoint('FINAL_REFUSAL',dict(RAW),dict(kind='all_predeclared_numerical_guesses_refused',identity=identity,status=status,seed_registration=SEED_INFO,unaccepted=True,readouts_unavailable_reason='No target-domain numerical initial guess; no predicted speeds computed'))
        else:
            _,pre0,_=model.residual(np.zeros(model.shape));scale=norm(model.rhs/np.sqrt(pre0));assert math.isfinite(scale) and scale>0
            run=Run(model,identity,scale);x,status,history,controls=solve(run,x);res,pre,_=model.residual(x);error=norm(res/np.sqrt(pre))/scale
            if error<=1e-8 and all(c['passed'] for c in controls) and status in ('CONVERGED','NEWTON_ALLOWANCE'):status='CONVERGED'
            RAW.update(final_state=x.copy(),final_residual=res.copy(),final_pre=pre.copy(),final_rhs=model.rhs.copy())
            rows=readouts(model,x,observations);formal={}
            for label in ('Q1_left','Q1_right','legacy'):
                vals=[v[label+'_residual'] for v in rows];formal[label]=finite(sum((v/e['observed_error_kms'])**2 for v,e in zip(vals,rows))) if all(v is not None for v in vals) else None
            final=checkpoint('FINAL',dict(RAW),dict(kind='final_state_and_signed_readouts',identity=identity,status=status,history=history,rows=rows,error=finite(error),error_reason=None if math.isfinite(error) else 'Nonfinite original normalized residual retained'))
            native_trials=run.native_trials;Dfail=run.D_failures
        case=dict(identity=identity,status=status,numerical_residual=finite(error) if error is not None else None,history=history,controls=controls,seed_registration=SEED_INFO,target_clock=target_clock,source_checks=model.source_checks,source_controls_copied=parent['source_controls'],historical_native_controls=parent['historical_native_controls'],historical_status=parent['historical_status'],rows=rows,readouts_unavailable_reason='No target-domain numerical initial guess' if not rows else None,formal_independent_error_diagnostic=formal,native_trials=native_trials,native_D_failure_checkpoints=Dfail,own_checkpoints=list(RECORDS),final_checkpoint=final,parent_case=base_parent,readout_qualified=False,physical_flags=PHYSICAL)
        publish(STEM+'_EXP24_CASE.json',case);cases.append(case)
        comparison=None
        if rows:
            comparison=compare_rows('WARM_PARENT_EPS1em05',parent['rows'],'TARGET_EPS1em06',rows);comparison['scope']='Different fixed EPS candidates; not a spatial/time convergence test or adoption criterion'
        result=dict(status='NUMERICAL_CASE_CLOSED',owner=OWNER,manifest=manifest,case=case,parent_comparison=comparison,late_joint_reference=late_reference,inherited_source_controls=parent['source_controls'],historical_native_controls=parent['historical_native_controls'],historical_status=parent['historical_status'],physical_flags=PHYSICAL,elapsed_seconds=time.monotonic()-tick)
        rh=publish(STEM+'_RESULT.json',result);raw=b'# Fixed EXP24 EPS1e-6 conditional common-parameter test\n\nOne target action/source. Fixed nine-candidate all-field numerical seed ladder; every refusal retained. Same six probe controls and original full-H solve. No global EPS adoption or cosmological preparation.\n';report=BASE/(STEM+'_REPORT.md')
        with report.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        report.chmod(0o444);assert report.read_bytes()==raw;CREATED[report.name]=sha(report);recheck()
        receipt=dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,physical_flags=PHYSICAL)
        publish(STEM+'_RECEIPT.json',receipt);recheck();assert json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())==receipt
        return 0 if status=='CONVERGED' else 3
    except Exception:
        failure_traceback=traceback.format_exc();receipt_path=BASE/(STEM+'_RECEIPT.json');prior=None
        if receipt_path.exists():prior=dict(file=receipt_path.name,sha256=sha(receipt_path),registered_sha256=CREATED.get(receipt_path.name))
        available=dict(RAW,**{'preparation_'+k:v for k,v in PREPARATION_RAW.items()});raw_record=None
        if np is not None and available:raw_record=checkpoint('ERROR_RAW',available,dict(kind='unaccepted_available_arrays',unaccepted=True,context=dict(CONTEXT),protected_prior_receipt=prior))
        eh=publish(STEM+'_ERROR.json',dict(status='POSTRECEIPT_ERROR_PRESERVED' if prior is not None else 'ERROR_PRESERVED',owner=OWNER,failed=now(),context=dict(CONTEXT),traceback=failure_traceback,protected_prior_receipt=prior,error_raw_checkpoint=raw_record,completed_cases=[v['identity']['case'] for v in cases],preserved_outputs=dict(CREATED),physical_flags=PHYSICAL));recheck()
        if prior is None:
            receipt=dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),error_sha256=eh,physical_flags=PHYSICAL)
            publish(STEM+'_RECEIPT.json',receipt);recheck();assert json.loads(receipt_path.read_text())==receipt
        else:assert sha(receipt_path)==prior['sha256'],'Existing terminal receipt changed'
        raise

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');assert ap.parse_args().root_owned
    raise SystemExit(main())
