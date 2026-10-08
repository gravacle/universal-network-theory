"""Guarded recovery of closed pre-solve outer256 RHS indexing failure; no author science."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,importlib,json,math,os,time,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V002'
FAILED='CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001'
PARENT='CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001'
ENGINE_NAME='cross_u_ngc3198_space_quadrature_recovery_v008'
AUTHOR_DRAFT=True
PROTOCOL_SHA='352af46192d7c4adc536880218cc3e56b149a9abc8567fbf767499e5aaab9bba'
PROBE_STEP=1e-4
ML=.5;RD=3.14
ANCHORS={'EXP24':(24.03,.28)}
EXTERIOR_NODES=(144.,160.,192.,224.,256.)
ARM='OUTER256_Q3'
np=core=native=direct=engine=None
Run=ScalarInverse=field_controls=fgmres=norm=split=join=None
OWNER=None;INPUTS={};CREATED={};RECORDS=[];CONTEXT={};RAW={};PREPARATION_RAW={}
PARENT_FINAL_REF=None;SOURCE_ID=None;CONTROL_PROBE=None;BINDING=None
CURRENT_QUADRATURE=3;ORIGINAL_QUADRATURE=None
CONFIG=None
INHERITED_CONFIG={'newton_cap': 40, 'backtracks': 32, 'final_original_residual': 1e-08, 'native_equilibrium_cap': 40, 'native_equilibrium_tolerance': 1e-10, 'native_trials_cap': 4096, 'native_D_cap': 600, 'native_D_true_tolerance': 1e-10, 'reduced_restart': 24, 'reduced_cap': 240, 'scalar_original_P_tolerance': 1e-10, 'scalar_corrections': 3, 'arithmetic_tolerance': 2e-11, 'energy_gradient_tolerance': 1e-07}
PHYSICAL={'source_registration_qualified': False, 'full_SPARC_model_qualified': False, 'refinement_qualified': False, 'full_metric_qualified': False, 'FLRW_junction_qualified': False, 'formation_qualified': False, 'stability_qualified': False, 'observational_qualified': False, 'joint_superiority_qualified': False}
PINS={'cross_u_ngc3198_space_quadrature_recovery_v008.py': '8ebcc132c3933aae2e4868092f13187680aeacd0d94fa74e88790fb14b4c0627', 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008.md': 'a9b0780d632c351aab9820a8118ea249e06f8cfac6329db0eea9ab34bf294d80', 'cross_u_ngc3198_sparc_stellar_footprint_v002.py': '95c86130b9a348da58f2c3442b51460bdc980998b4395114a4ba3ad69ebd4ac0', 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002.md': '0e17b74071cf9bfe1b9066c24ac13dd9a969f7cf21bdf1042b2afd3c6b33ccc9', 'cross_u_nonzero_native_curvature_split_v001.py': 'a60415dd3983e91161b45428ce5c030ff27ec3b8dd03032aa9e42c9a30a2f028', 'cross_u_direct_scalar_proxy_controls_v001.py': '0d58dcff5ae26ba16bf6f4272144fb7a0ce4f14474ac2edfa50115f911fc7621', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1', 'reviewed_cross_u_ngc3198_sparc_space_quadrature_refinement_v001_389_f522fe75.py': 'f522fe750e4282e776ca16d2eba40d7ab2e4122d3e203cfa28ea6e527ef09eef', 'reviewed_CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_25_7e822490.md': '7e8224907b7fb2e8f898d8f873a4c66d68719d176c970b5fcc0565239b45641f', 'cross_u_ngc3198_sparc_space_quadrature_refinement_v001.py': 'e77230a1819e89799e4463d5ca3808b1cab9f6a2c9166b593cbca2b949dec853', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001.md': '3ffc808394102d8b7479d9e1f604ba940e0ac7570181f1c386fb5eddc2c5e729', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RECEIPT.json': 'b7834e205c379e8f9444e3ac17243744fc2266f92ccd186bcd780a7cebaac926', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_MANIFEST.json': 'a103ef976e3035fb48c57b878328620cf49f92118f5aeb45a84ee9dc4665ea0c', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RESULT.json': '963de6b73e19820fc424bbb994d7e07fbed4ecea4401b25730fbe38499f1524d', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_COARSE_Q3_CASE.json': '416f36b0df212c6ca9531a393478f7e6d98178a654e1e8dd20306819008bcb72', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00002_PROLONGATION.npz': 'f3c76eb486dbace2994f2fb769139436b506529a0ba96814d3b295d9cf4bd1a7', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00002_PROLONGATION.npz.COMMIT.json': '4098ffa37f0c75acdb1b00f7a04d9a3dc0fdbebf3c37f8914ecf2fb744920cae', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00003_ARM_SOURCE_INPUT.npz': 'a158d703f988c9f3323010057cb6fefcd1b3ca9cd685b10c3eb06abdd9fe2352', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00003_ARM_SOURCE_INPUT.npz.COMMIT.json': '34d2f43da2aa9838de1dbb7236e91bc97c40b54de0412413b346e1cd6cbb9205', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00027_FINAL.npz': '6fd1b0205f3cf22fafecc12e2dded38faf28a8cf6107f574fa3812ba806f00bf', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00027_FINAL.npz.COMMIT.json': '6f84777a05aaa51e966ebdb5314a5727effdbff8f549a8e9e26d4228bca6807b', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00000_REUSED_SOURCE_FOOTPRINTS.npz': 'a9f8f81d31e03b7f65cc5c647fa65fae291eaeff411ec5e8bc2babf8b82d05c9', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00000_REUSED_SOURCE_FOOTPRINTS.npz.COMMIT.json': 'f4e947d31e01cf44e302b3e7dc8dde1b24627bd6d636c090fe8c2ef2237baee2', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00001_HISTORICAL_NATIVE_CONTROLS.npz': '16adab8896501d801cbec4612f9280077dd7f20cea2f89f4f47665d3d2ce9490', 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_00001_HISTORICAL_NATIVE_CONTROLS.npz.COMMIT.json': 'ad2002019479b1acb923dcda2091f509e41683c93247840ba6bf1bf6cdaf6a21', 'cross_u_ngc3198_sparc_outer_domain_v001.py': '314ad0f084e4497eec5f5a62eaf2376989b3c32d1972949de440572724326210', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001.md': '4aa8d56ab208adbd55de543484b89891673fa1c1794b3050fb3c2724566131d3', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_RECEIPT.json': 'a47e38973d108079cc2ce11b231b0e07f8c620f04c63be3d990a51c74199ae9b', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_00000_BASELINE.npz': '1f7ef31751c0b2d73af77f0e05c6f776489c6939392b27d95456500faafad653', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_00000_BASELINE.npz.COMMIT.json': 'af420b002dcb1913aa58614e7a76dad917ab70cc67bd1b8f511e8a3972675428', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_00001_EXTENSION.npz': '56a36f7322141d5329145513e549385e1e4a753f65a3986dc451caaf11ac1606', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_00001_EXTENSION.npz.COMMIT.json': 'b3e53231a43c5bdf9df8e995ed218d45a4bf5ce2801a76f0d96a4a8b3050ea69', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_00002_ERROR_RAW.npz': 'a04009ca944d9a2d020b41498af1664701e81c1af28a41f7f7780d8f2d026dec', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_00002_ERROR_RAW.npz.COMMIT.json': '98e2043f0918ba7ff118b1e0973619a98d77468c544bfd0d6725203e1a60a29f', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_ERROR.json': '735915a510e206b1848c10a027088f429b3238ca593875e2d05d6f976f5582b2', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_MANIFEST.json': 'a192b977006cfc7d2e4f4e4e597f3c1be0942c6f95f156d6cd98a507ed3f9077', 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_OWNER_START.json': '5ba6902d945c157ddb44256e703b7ac816be2cf55cf80ef8fe7e5420af3fec08'}
CORE_INPUT_PINS={'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900'}
RECEIPT_EXPECTATIONS={'CONSTRAINED_U_CLOCK_GRADIENT_BBN_ACOUSTIC_READOUT_V001_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'NEW_BBN_ACOUSTIC_ARITHMETIC_PASS'}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V002_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'NEW_ATOMIC_PAIR_ARITHMETIC_PASS'}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'FIXED_NEVO_NEW_ACTION_NUMERICALLY_QUALIFIED'}, 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PANTHEON_PROFILE_V002_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'NEW_FIXED_PANTHEON_PROFILE_ARITHMETIC_PASS'}, 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'NEW_ATOMIC_PAIR_ARITHMETIC_PASS'}, 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': {'owner_kind': 'str', 'pid': 39330, 'status': 'NUMERICAL_PASS'}, 'CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001_RECEIPT.json': {'owner_kind': 'dict', 'pid': 56449, 'status': 'CLOSED'}, 'CROSS_U_NGC3198_DIRECT_SCALAR_RECOVERY_V005_RECEIPT.json': {'owner_kind': 'str', 'pid': 57478, 'status': None}, 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json': {'owner_kind': 'str', 'pid': 49006, 'status': None}, 'CROSS_U_NGC3198_NATIVE_ELIMINATION_RECOVERY_V006_RECEIPT.json': {'owner_kind': 'dict', 'pid': 62181, 'status': 'CLOSED'}, 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RECEIPT.json': {'owner_kind': 'str', 'pid': 42114, 'status': None}, 'CROSS_U_NGC3198_PARTIAL_RECOVERY_V002_RECEIPT.json': {'owner_kind': 'str', 'pid': 42904, 'status': None}, 'CROSS_U_NGC3198_SPACE_QUADRATURE_RECOVERY_V008_RECEIPT.json': {'owner_kind': 'dict', 'pid': 63945, 'status': 'CLOSED'}, 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V001_RECEIPT.json': {'owner_kind': 'dict', 'pid': 76290, 'status': 'CLOSED'}, 'CROSS_U_NGC3198_SPARC_STELLAR_FOOTPRINT_V002_RECEIPT.json': {'owner_kind': 'dict', 'pid': 76996, 'status': 'CLOSED'}, 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json': {'owner_kind': 'str', 'pid': 50386, 'status': None}, 'CROSS_U_Q1_PROJECTION_STIFFNESS_V001_RECEIPT.json': {'owner_kind': 'str', 'pid': 47083, 'status': None}, 'NGC3198_STATIONARY_LAPSE_SPAN_V001_RECEIPT.json': {'owner_kind': 'NoneType', 'pid': None, 'status': 'PASS'}, 'CROSS_U_NGC3198_SPARC_SPACE_QUADRATURE_REFINEMENT_V001_RECEIPT.json': {'owner_kind': 'dict', 'pid': 78729, 'status': 'CLOSED'}, 'CROSS_U_NGC3198_SPARC_OUTER_DOMAIN_V001_RECEIPT.json': {'owner_kind': 'dict', 'pid': 90146, 'status': 'CLOSED'}}


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
    merged=dict(PINS,**{STEM+'.md':PROTOCOL_SHA});todo=[PARENT+'_RECEIPT.json',FAILED+'_RECEIPT.json'];done=set()
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
    rc=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text())
    manifest=json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text())
    result=json.loads((BASE/(PARENT+'_RESULT.json')).read_text())
    case=json.loads((BASE/(PARENT+'_COARSE_Q3_CASE.json')).read_text())
    assert rc['status']=='CLOSED' and rc['owner']['owner']=='root' and rc['owner']['pid']==78729
    assert rc['owner']['source_sha256']==INPUTS['cross_u_ngc3198_sparc_space_quadrature_refinement_v001.py'] and rc['closed']>rc['owner']['started']
    assert rc['result_sha256']==INPUTS[PARENT+'_RESULT.json'] and manifest['owner']==rc['owner']==result['owner']
    assert result['status']=='NUMERICAL_ARMS_CLOSED' and result['manifest']==manifest
    assert manifest['physics_changes']==[] and manifest['no_automatic_resume'] is True and manifest['numerical_configuration']==INHERITED_CONFIG
    assert [c['arm'] for c in result['cases']]==['COARSE_Q3','FINE_Q2','FINE_Q3'] and result['cases'][0]==case
    assert case['arm']=='COARSE_Q3' and case['status']=='CONVERGED' and case['numerical_residual']==5.30115226620514e-10 and len(case['history'])==2
    assert case['identity']['grid_shape']==[65,87,45] and case['identity']['quadrature_order']==3 and case['identity']['space_refined'] is False
    assert case['identity']['eps']==1e-5 and case['identity']['hi_tail'] is False and case['identity']['h2_tail'] is False
    source=case['identity']['source_identity'];assert source==manifest['source_identity'] and source['native_modes']==32 and source['source_id']=='EXP24'
    assert source['eps']==1e-5 and source['M_to_L']==ML and source['Rd_kpc']==RD and source['anchor']==list(ANCHORS['EXP24']) and source['law_changes']==[]
    assert len(case['source_controls_copied'])==20 and len(case['controls'])==16 and all(c['passed'] for c in case['source_controls_copied']+case['controls'])
    assert case['historical_status']=='NATIVE_IMPLEMENTATION_FAILED' and [c['passed'] for c in case['historical_native_controls']]==[False,True,True]
    assert case['physical_flags']==manifest['physical_flags']==result['physical_flags']==rc['physical_flags']==PHYSICAL and case['readout_qualified'] is False
    records=[]
    for c in result['cases']:
        assert c['status']=='CONVERGED' and c['readout_qualified'] is False and c['physical_flags']==PHYSICAL and len(c['rows'])==43
        for rec in c['own_checkpoints']:
            assert INPUTS[rec['file']]==rc['output_sha256'][rec['file']]==rec['sha256']
            assert INPUTS[rec['commit_file']]==rc['output_sha256'][rec['commit_file']]==rec['commit_sha256']
            assert json.loads((BASE/rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
            records.append(rec)
    assert len(records)==164 and len({r['file'] for r in records})==164
    assert sum(n.startswith(PARENT+'_') and n.endswith('.npz') for n in rc['output_sha256'])==166
    assert sum(n.startswith(PARENT+'_') and n.endswith('.npz.COMMIT.json') for n in rc['output_sha256'])==166
    final=case['final_checkpoint'];assert final==case['own_checkpoints'][-1] and final['file']==PARENT+'_00027_FINAL.npz'
    assert final['metadata']['status']==case['status'] and final['metadata']['history']==case['history'] and final['metadata']['rows']==case['rows'] and final['metadata']['identity']==case['identity'] and final['metadata']['error']==case['numerical_residual']
    for n,label in [('00000_REUSED_SOURCE_FOOTPRINTS','source'),('00001_HISTORICAL_NATIVE_CONTROLS','historical')]:
        file=PARENT+'_'+n+'.npz';rec=json.loads((BASE/(file+'.COMMIT.json')).read_text())
        assert rec['file']==file and rec['sha256']==INPUTS[file] and rc['output_sha256'][file]==rec['sha256']
        rec=dict(rec,commit_file=file+'.COMMIT.json',commit_sha256=INPUTS[file+'.COMMIT.json'])
        if label=='source':source_record=rec
        else:historical_record=rec
    assert source_record['metadata']['controls']==case['source_controls_copied'] and historical_record['metadata']['controls']==case['historical_native_controls']
    assert historical_record['metadata']['not_promoted'] is True
    return dict(case=case,manifest=manifest,final_record=final,source_record=source_record,historical_record=historical_record,source_input=case['own_checkpoints'][1],closed_parent_cases=[dict(arm=c['arm'],status=c['status'],numerical_residual=c['numerical_residual'],readout_qualified=c['readout_qualified'],physical_flags=c['physical_flags']) for c in result['cases']])


def failed_binding(parent):
    rc=json.loads((BASE/(FAILED+'_RECEIPT.json')).read_text());m=json.loads((BASE/(FAILED+'_MANIFEST.json')).read_text());e=json.loads((BASE/(FAILED+'_ERROR.json')).read_text())
    assert rc['status']=='CLOSED' and rc['owner']['owner']=='root' and rc['owner']['pid']==90146 and rc['closed']=='2026-10-06T20:02:05.742421+00:00'
    assert rc['owner']['started']=='2026-10-06T20:01:35.779892+00:00' and rc['owner']['source_sha256']==INPUTS['cross_u_ngc3198_sparc_outer_domain_v001.py']
    assert rc['owner']==m['owner']==e['owner']==json.loads((BASE/(FAILED+'_OWNER_START.json')).read_text()) and rc['error_sha256']==INPUTS[FAILED+'_ERROR.json']
    assert m['input_sha256']==rc['input_sha256'] and len(rc['input_sha256'])==3546 and m['numerical_configuration']==INHERITED_CONFIG and m['physics_changes']==[]
    assert m['baseline']['final']==parent_ref(parent['final_record']) and m['baseline']['rows']==parent['case']['rows'] and m['source_identity']==parent['case']['identity']['source_identity']
    assert m['added_R_kpc']==m['added_Z_kpc']==list(EXTERIOR_NODES) and m['old_extent_kpc']==128. and m['new_extent_kpc']==256. and m['quadrature_order']==3 and m['native_modes']==32
    assert e['status']=='ERROR_PRESERVED' and e['completed_case'] is None and e['raw_preservation_error'] is None and e['protected_prior_receipt'] is None and e['partial_unqualified_files']==[]
    assert e['context']==dict(arm=ARM,stage='zero_extension') and 'IndexError: boolean index did not match' in e['traceback'] and 'model.rhs[:87,:45]' in e['traceback']
    assert m['physical_flags']==rc['physical_flags']==e['physical_flags']==PHYSICAL
    records=[]
    expected={FAILED+'_OWNER_START.json',FAILED+'_MANIFEST.json',FAILED+'_ERROR.json'}
    for tag in ('00000_BASELINE','00001_EXTENSION','00002_ERROR_RAW'):
        f=FAILED+'_'+tag+'.npz';c=f+'.COMMIT.json';rec=json.loads((BASE/c).read_text())
        assert rec['file']==f and rec['sha256']==INPUTS[f]==rc['output_sha256'][f] and INPUTS[c]==rc['output_sha256'][c]
        rec=dict(rec,commit_file=c,commit_sha256=INPUTS[c]);assert rec['metadata']['owner']==rc['owner'] and rec['metadata']['parent_final']==parent_ref(parent['final_record']) and rec['metadata']['source_identity']==m['source_identity']
        assert all(s['finite'] for s in rec['metadata']['schema'].values());records.append(rec);expected.update((f,c))
    assert set(rc['output_sha256'])==expected and len(expected)==9
    assert {p.name for p in BASE.glob(FAILED+'_*.npz')}=={r['file'] for r in records} and {p.name for p in BASE.glob(FAILED+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in records}
    assert records[0]['metadata']['kind']=='unchanged_closed128baseline' and records[0]['metadata']['baseline']==m['baseline']
    names=['retained_R_nodes_and_cells','retained_Z_nodes_and_cells','retained_parent_nodal_field','zero_added_numerical_guess']
    assert records[1]['metadata']['controls']==[dict(name=n,passed=True,tolerance=0.) for n in names] and records[1]['metadata']['numerical_only'] is True
    assert records[2]==e['error_raw_checkpoint'] and records[2]['metadata']['unaccepted'] is True
    summary=dict(source_file='cross_u_ngc3198_sparc_outer_domain_v001.py',source_sha256=rc['owner']['source_sha256'],receipt_file=FAILED+'_RECEIPT.json',receipt_sha256=INPUTS[FAILED+'_RECEIPT.json'],error_file=FAILED+'_ERROR.json',error_sha256=rc['error_sha256'],owner=rc['owner'],closed=rc['closed'],failed_before_solve=True,old_failure_unchanged=True,completed_controls_copied=records[1]['metadata']['controls'],records=[parent_ref(r) for r in records])
    return dict(summary=summary,baseline_record=records[0],extension_record=records[1],raw_record=records[2],baseline=m['baseline'])


def parent_ref(rec):return {k:rec[k] for k in ('file','sha256','commit_file','commit_sha256')}

def checkpoint(tag,arrays,meta):
    data=canonical(dict(meta,owner=OWNER,parent_final=PARENT_FINAL_REF,source_identity=SOURCE_ID,control_probe=CONTROL_PROBE,
      schema={k:dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a)))) for k,a in arrays.items()}))
    text=encode(data).decode();data=json.loads(text);p=BASE/f'{STEM}_{len(RECORDS):05d}_{tag}.npz'
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);CREATED[p.name]=sha(p);rec=dict(file=p.name,sha256=CREATED[p.name],metadata=data)
    ch=publish(p.name+'.COMMIT.json',rec);rec=dict(rec,commit_file=p.name+'.COMMIT.json',commit_sha256=ch);RECORDS.append(rec)
    with np.load(p,allow_pickle=False) as z:
        assert str(z['metadata'])==text and set(z.files)==set(arrays)|{'metadata'}
        for k,a in arrays.items():assert np.array_equal(z[k],a,equal_nan=True)
    return rec

def recheck(strict=True):
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
    if strict:
        assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={v['file'] for v in RECORDS}
        assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={v['commit_file'] for v in RECORDS}
    if STEM+'_OWNER_START.json' in CREATED:assert json.loads((BASE/(STEM+'_OWNER_START.json')).read_text())==OWNER

def read_pair(rec,label,selected):
    arrays={};assert set(selected)<=set(rec['metadata']['schema'])
    with np.load(BASE/rec['file'],allow_pickle=False) as z:
        assert set(z.files)==set(rec['metadata']['schema'])|{'metadata'} and json.loads(str(z['metadata']))==rec['metadata']
        for name in selected:
            arrays[name]=z[name].copy();RAW[label+'_'+name]=arrays[name].copy()
    for name,a in arrays.items():assert rec['metadata']['schema'][name]==dict(shape=list(a.shape),dtype=str(a.dtype),finite=bool(np.all(np.isfinite(a))))
    return arrays


def registered_native_controls(model,x):
    global CONTROL_PROBE
    physical=RECORDS[-1];assert physical['metadata']['kind']=='warm_start_from_converged_parent'
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
        arrays=read_pair(operand,'control_'+label,list(operand['metadata']['schema']));assert np.array_equal(arrays['direction'],d) and np.array_equal(arrays['state'],probe)
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
    run.current_state_checkpoint=checkpoint('INPUT',dict(state=x),dict(kind='warm_start_from_converged_parent',identity=run.identity,parent_binding=BINDING))
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

def outer_guess(old,r,z):
    PREPARATION_RAW.clear();PREPARATION_RAW.update(parent_state=old,parent_r=r,parent_z=z)
    assert old.shape==(65,87,45) and r.shape==(87,) and z.shape==(45,) and r[-1]==z[-1]==128
    extra=np.array(EXTERIOR_NODES);rr=np.r_[r,extra];zz=np.r_[z,extra];PREPARATION_RAW.update(extended_r=rr,extended_z=zz)
    warm=np.zeros((old.shape[0],len(rr),len(zz)));warm[:,:len(r),:len(z)]=old;PREPARATION_RAW['warm_state']=warm
    controls=[dict(name='retained_R_nodes_and_cells',passed=bool(np.array_equal(rr[:len(r)],r) and np.array_equal(np.diff(rr)[:len(r)-1],np.diff(r))),tolerance=0.),
      dict(name='retained_Z_nodes_and_cells',passed=bool(np.array_equal(zz[:len(z)],z) and np.array_equal(np.diff(zz)[:len(z)-1],np.diff(z))),tolerance=0.),
      dict(name='retained_parent_nodal_field',passed=bool(np.array_equal(warm[:,:len(r),:len(z)],old)),tolerance=0.),
      dict(name='zero_added_numerical_guess',passed=bool(np.all(warm[:,len(r):,:]==0) and np.all(warm[:,:,len(z):]==0)),tolerance=0.)]
    assert all(c['passed'] for c in controls) and np.all(np.diff(rr)>0) and np.all(np.diff(zz)>0) and warm.shape==(65,92,50) and rr[-1]==zz[-1]==256
    return warm,rr,zz,controls

def freeze_actual_files():
    out={}
    for p in sorted(BASE.glob(STEM+'_*')):
        if p.is_file():p.chmod(0o444);out[p.name]=sha(p)
    return out


def main():
    global np,core,native,direct,engine,OWNER,INPUTS,PARENT_FINAL_REF,SOURCE_ID,ORIGINAL_QUADRATURE
    global Run,ScalarInverse,field_controls,fgmres,norm,split,join,CONFIG,BINDING
    assert not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64
    assert not list(BASE.glob(STEM+'_*')),'Existing runtime namespace preserved'
    INPUTS=resolve_inputs();parent=parent_binding();failed=failed_binding(parent);base=parent['case'];PARENT_FINAL_REF=parent_ref(parent['final_record']);BINDING=PARENT_FINAL_REF;SOURCE_ID=base['identity']['source_identity'];source=sha(__file__)
    OWNER=dict(owner='root',pid=os.getpid(),source_sha256=source,started=now());tick=time.monotonic();case=None
    try:
        publish(STEM+'_OWNER_START.json',OWNER)
        baseline=dict(case_file=PARENT+'_COARSE_Q3_CASE.json',case_sha256=INPUTS[PARENT+'_COARSE_Q3_CASE.json'],final=PARENT_FINAL_REF,status=base['status'],numerical_residual=base['numerical_residual'],history_length=len(base['history']),rows=base['rows'],controls=base['controls'],source_controls=base['source_controls_copied'],historical_native_controls=base['historical_native_controls'],historical_status=base['historical_status'],readout_qualified=False,physical_flags=PHYSICAL)
        manifest=dict(owner=OWNER,input_sha256=INPUTS,baseline=baseline,failed_attempt=failed['summary'],recovery_change='Scalar RHS component [0] selected before old-mask indexing; saved preparation/source operands reused',constructor_scope='Reconstruct same Model only to certify exact saved source operands; saved arrays remain authoritative',closed_parent_cases=parent['closed_parent_cases'],source_identity=SOURCE_ID,added_R_kpc=list(EXTERIOR_NODES),added_Z_kpc=list(EXTERIOR_NODES),old_extent_kpc=128.,new_extent_kpc=256.,quadrature_order=3,native_modes=32,numerical_configuration=INHERITED_CONFIG,physics_changes=[],boundary_registration='Same conditional zero Dirichlet wall moved to256kpc; no physical exterior adopted',numerical_guess='Exact closed COARSE_Q3 on retained128square and zero extension; no physical preparation adopted',no_automatic_resume=True,physical_flags=PHYSICAL)
        publish(STEM+'_MANIFEST.json',manifest);authenticate()
        np=importlib.import_module('numpy');core=importlib.import_module('cross_u_ngc3198_nonlinear_disk_v001')
        native=importlib.import_module('cross_u_nonzero_native_curvature_split_v001');native.np=np;native.core=core
        direct=importlib.import_module('cross_u_direct_scalar_proxy_controls_v001');direct.np=np;direct.core=core;direct.native=native
        engine=importlib.import_module(ENGINE_NAME);engine.np=np;engine.core=core;engine.native=native;engine.direct=direct;engine.checkpoint=checkpoint;engine.CONTEXT=CONTEXT;engine.BINDING=PARENT_FINAL_REF
        for name in ('Run','ScalarInverse','field_controls','fgmres','norm','split','join','CONFIG'):globals()[name]=getattr(engine,name)
        assert CONFIG==INHERITED_CONFIG;core.authenticate();assert core.PINS==CORE_INPUT_PINS;authenticate()
        ORIGINAL_QUADRATURE=core.shape_quadrature;core.shape_quadrature=selected_quadrature
        inherited=read_pair(failed['baseline_record'],'failed_baseline',list(failed['baseline_record']['metadata']['schema']))
        extension=read_pair(failed['extension_record'],'failed_extension',list(failed['extension_record']['metadata']['schema']))
        saved=read_pair(failed['raw_record'],'failed_raw',list(failed['raw_record']['metadata']['schema']))
        old=inherited['parent_state'];final_rhs=inherited['parent_rhs'];oldmask=inherited['parent_mask'];cr=inherited['r_kpc'];cz=inherited['z_kpc'];observations=inherited['official_rotmod'];photometry=inherited['photometry']
        x=saved['current_warm_state'].copy();r=extension['extended_r'];z=extension['extended_z'];geometry_controls=json.loads(encode(failed['extension_record']['metadata']['controls']))
        assert old.shape==final_rhs.shape==oldmask.shape==(65,87,45) and x.shape==saved['current_rhs'].shape==saved['current_mask'].shape==(65,92,50)
        assert observations.shape==(43,8) and photometry.shape==(43,2) and np.array_equal(photometry,observations[:,[0,6]])
        assert np.array_equal(cr,np.array(base['identity']['r_kpc'])) and np.array_equal(cz,np.array(base['identity']['z_kpc']))
        assert np.array_equal(extension['parent_state'],old) and np.array_equal(extension['parent_r'],cr) and np.array_equal(extension['parent_z'],cz)
        for name in ('parent_state','parent_r','parent_z','extended_r','extended_z','warm_state'):assert np.array_equal(saved['preparation_'+name],extension[name])
        assert np.array_equal(x,extension['warm_state']) and np.array_equal(x[:,:87,:45],old) and np.all(x[:,87:,:]==0) and np.all(x[:,:,45:]==0)
        assert np.array_equal(r[:87],cr) and np.array_equal(z[:45],cz) and np.array_equal(r[87:],np.array(EXTERIOR_NODES)) and np.array_equal(z[45:],np.array(EXTERIOR_NODES))
        assert np.array_equal(saved['current_xi'],inherited['xi']) and np.array_equal(saved['current_weights'],inherited['weight']) and np.all(x[~saved['current_mask']]==0) and np.all(old[~oldmask]==0)
        for row,observed in zip(base['rows'],observations):assert [row['R_kpc'],row['observed_velocity_kms'],row['observed_error_kms']]==[float(v) for v in observed[:3]]
        checkpoint('BASELINE_REUSED',inherited,dict(kind='unchanged_closed128baseline_reused',baseline=baseline,failed_parent_pair=parent_ref(failed['baseline_record']),old_controls_not_recomputed=True))
        prep=checkpoint('EXTENSION_REUSED',extension,dict(kind='saved_numerical_guess_extension',arm=ARM,controls_copied=geometry_controls,failed_parent_pair=parent_ref(failed['extension_record']),numerical_only=True,no_physical_preparation=True,extension_not_recomputed=True))
        fixed=SOURCE_ID['inherited_fixed'];oldprofiles=core.density.profiles(False,False);star,prefix=footprint(photometry,'EXP24');profiles=dict(oldprofiles,stars=star)
        source_input=read_pair(parent['source_input'],'baseline_source_certificate',['photometry','stellar_profile_prefix'])
        assert np.array_equal(prefix,source_input['stellar_profile_prefix']) and np.array_equal(photometry,source_input['photometry'])
        CONTEXT.update(arm=ARM,stage='saved_operand_reconstruction_certificate');model=core.Model(r,z,32,1e-5,fixed,profiles);model.fgmres_fixed=fixed
        RAW.update(current_warm_state=x.copy(),saved_rhs=saved['current_rhs'].copy(),saved_mask=saved['current_mask'].copy(),saved_weights=saved['current_weights'].copy(),saved_xi=saved['current_xi'].copy(),reconstructed_rhs=model.rhs.copy(),reconstructed_mask=model.mask.copy(),reconstructed_weights=model.w.copy(),reconstructed_xi=model.xi.copy(),stellar_profile_prefix=prefix.copy())
        certification=[dict(name='reconstructed_'+name+'_equals_saved',passed=bool(np.array_equal(a,b)),tolerance=0.) for name,a,b in [('rhs',model.rhs,saved['current_rhs']),('mask',model.mask,saved['current_mask']),('xi',model.xi,saved['current_xi']),('weights',model.w,saved['current_weights'])]]
        cert=checkpoint('RECONSTRUCTION_CERTIFICATE',dict(RAW),dict(kind='same_Model_saved_operand_certificate',arm=ARM,controls=certification,failed_raw_pair=parent_ref(failed['raw_record']),constructor_repeated_for_certification_only=True,no_replacement_source=True,source_checks=model.source_checks))
        assert all(c['passed'] for c in certification) and x.shape==model.shape and np.all(np.isfinite(x))
        assert all(model.source_checks[k]<=1e-11 for k in ('surface_quadrature_relative','exact_annular_mass_relative','weight_sum_error')) and model.source_checks['positive_weights']
        model.rhs=saved['current_rhs'].copy();model.mask=saved['current_mask'].copy();model.xi=saved['current_xi'].copy();model.w=saved['current_weights'].copy()
        geometry_controls.extend([dict(name='unchanged_32_xi',passed=bool(np.array_equal(model.xi,inherited['xi'])),tolerance=0.),dict(name='unchanged_32_weights',passed=bool(np.array_equal(model.w,inherited['weight'])),tolerance=0.),dict(name='retained_inner_source_RHS',passed=bool(np.array_equal(model.rhs[0,:87,:45][oldmask[0]],final_rhs[0][oldmask[0]])),tolerance=0.)])
        source_rec=checkpoint('SOURCE_INPUT',dict(state=x,rhs=model.rhs,r_kpc=r,z_kpc=z,mask=model.mask,xi=model.xi,weight=model.w,photometry=photometry,stellar_profile_prefix=prefix,original_rhs=final_rhs,original_mask=oldmask),dict(kind='same_law_saved_extended_domain',arm=ARM,controls=geometry_controls,completed_geometry_controls_copied=geometry_controls[:4],new_geometry_controls=geometry_controls[4:],source_checks=model.source_checks,reconstruction_certificate=cert,failed_raw_pair=parent_ref(failed['raw_record']),unchanged_source=True,extension_not_recomputed=True,old_footprint_controls_not_recomputed=True))
        assert all(c['passed'] for c in geometry_controls);model.clock(x[0])
        identity=dict(case='E1em05_SPARC_EXP24_HI0_H20_'+ARM,eps=1e-5,hi_tail=False,h2_tail=False,grid_shape=list(model.shape),r_kpc=r.tolist(),z_kpc=z.tolist(),Hunit=base['identity']['Hunit'],source_identity=SOURCE_ID,outer_domain_source_sha256=source,outer_domain_manifest_sha256=CREATED[STEM+'_MANIFEST.json'],source_parent_final=PARENT_FINAL_REF,quadrature_order=3,warm_start_checkpoint=prep,source_checkpoint=source_rec,old_extent_kpc=128.,new_extent_kpc=256.,added_R_kpc=list(EXTERIOR_NODES),added_Z_kpc=list(EXTERIOR_NODES))
        _,pre0,_=model.residual(np.zeros(model.shape));scale=norm(model.rhs/np.sqrt(pre0));assert math.isfinite(scale) and scale>0
        run=Run(model,identity,scale);x,status,history,controls=solve(run,x);res,pre,_=model.residual(x);error=norm(res/np.sqrt(pre))/scale
        if math.isfinite(error) and error<=CONFIG['final_original_residual'] and all(c['passed'] for c in controls) and status in ('CONVERGED','NEWTON_ALLOWANCE'):status='CONVERGED'
        RAW.update(final_state=x.copy(),final_residual=res.copy(),final_pre=pre.copy(),final_rhs=model.rhs.copy())
        rows=readouts(model,x,observations);formal={}
        for label in ('Q1_left','Q1_right','legacy'):
            vals=[v[label+'_residual'] for v in rows];formal[label]=finite(sum((v/e['observed_error_kms'])**2 for v,e in zip(vals,rows))) if all(v is not None for v in vals) else None
        final_rec=checkpoint('FINAL',dict(RAW),dict(kind='final_state_and_signed_readouts',arm=ARM,identity=identity,status=status,history=history,rows=rows,error=finite(error),error_reason=None if math.isfinite(error) else 'Nonfinite original normalized residual retained'))
        comparison=compare_rows('CLOSED128_COARSE_Q3',base['rows'],ARM,rows)
        case=dict(arm=ARM,identity=identity,status=status,numerical_residual=finite(error),history=history,controls=controls,geometry_controls=geometry_controls,source_checks=model.source_checks,rows=rows,formal_independent_error_diagnostic=formal,comparison=comparison,native_trials=run.native_trials,native_D_failure_checkpoints=run.D_failures,own_checkpoints=list(RECORDS),final_checkpoint=final_rec,baseline=baseline,readout_qualified=False,physical_flags=PHYSICAL)
        publish(STEM+'_'+ARM+'_CASE.json',case);RAW.clear();PREPARATION_RAW.clear();recheck()
        result=dict(status='NUMERICAL_OUTCOME_CLOSED',owner=OWNER,manifest=manifest,failed_attempt=failed['summary'],case=case,comparison=comparison,copied_parent_dispositions=baseline,closed_parent_cases=parent['closed_parent_cases'],physical_flags=PHYSICAL,elapsed_seconds=time.monotonic()-tick)
        rh=publish(STEM+'_RESULT.json',result);raw=(f'# Fixed EXP24 outer-domain sensitivity\n\n{ARM}: {status}; original residual={finite(error)}. All43 signed one-sided and legacy comparisons retained. No source fit, best-arm, exterior or metric qualification.\n').encode();report=BASE/(STEM+'_REPORT.md')
        with report.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        report.chmod(0o444);assert report.read_bytes()==raw;CREATED[report.name]=sha(report);recheck()
        receipt=dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),result_sha256=rh,physical_flags=PHYSICAL)
        publish(STEM+'_RECEIPT.json',receipt);recheck();assert json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())==receipt
        return 0 if status=='CONVERGED' else 3
    except Exception:
        failure_traceback=traceback.format_exc();receipt_path=BASE/(STEM+'_RECEIPT.json');prior=None
        if receipt_path.exists():prior=dict(file=receipt_path.name,sha256=sha(receipt_path),registered_sha256=CREATED.get(receipt_path.name))
        available=dict(RAW,**{'preparation_'+k:v for k,v in PREPARATION_RAW.items()});raw_record=None;raw_error=None
        if np is not None and available:
            try:raw_record=checkpoint('ERROR_RAW',available,dict(kind='unaccepted_available_arrays',unaccepted=True,context=dict(CONTEXT),protected_prior_receipt=prior))
            except Exception:raw_error=traceback.format_exc()
        actual=freeze_actual_files();registered_npz={r['file'] for r in RECORDS};registered_commit={r['commit_file'] for r in RECORDS}
        partial=[n for n in actual if (n.endswith('.npz') and n not in registered_npz) or (n.endswith('.npz.COMMIT.json') and n not in registered_commit)]
        CREATED.update(actual)
        eh=publish(STEM+'_ERROR.json',dict(status='POSTRECEIPT_ERROR_PRESERVED' if prior is not None else 'ERROR_PRESERVED',owner=OWNER,failed=now(),context=dict(CONTEXT),traceback=failure_traceback,raw_preservation_error=raw_error,protected_prior_receipt=prior,error_raw_checkpoint=raw_record,completed_case=None if case is None else case['arm'],preserved_outputs=actual,partial_unqualified_files=partial,physical_flags=PHYSICAL))
        authenticate()
        for n,h in CREATED.items():assert sha(BASE/n)==h
        if prior is None:
            receipt=dict(status='CLOSED',owner=OWNER,closed=now(),input_sha256=INPUTS,output_sha256=dict(CREATED),error_sha256=eh,physical_flags=PHYSICAL)
            publish(STEM+'_RECEIPT.json',receipt);assert json.loads(receipt_path.read_text())==receipt
        else:assert sha(receipt_path)==prior['sha256'],'Existing terminal receipt changed'
        for n,h in CREATED.items():assert sha(BASE/n)==h
        raise

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root-run',action='store_true');args=parser.parse_args()
    assert args.root_run and not AUTHOR_DRAFT,'Root-only execution after prospective review'
    raise SystemExit(main())

