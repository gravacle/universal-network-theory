"""HELD byte/header natural-closure custody of DIRECT43 baseline preparation.
No numeric arrays, source arithmetic, field/control replay or circle admission.
V001 empty author-write artifact is preserved; no source body was evaluated.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,re,sys,zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
SOURCE=('direct43_original_baseline_preparation_v003.py','68fff180edacd39e1d88c828201f6ea6c5018eaec78bbdd2e4bb90f4528ae336')
EXPECTED_SOURCE=SOURCE
RESULT=('DIRECT43_ORIGINAL_BASELINE_PREPARATION_V003_RESULT.json', 'c606d05dd627d3befdd3dab107e64d88e9a227654eb6cbf6742dee3a5cd144d1', 'DIRECT43_ORIGINAL_BASELINE_FIELDS_PREPARED_UNQUALIFIED')
ERROR=(None,None,None)
RECEIPT=('DIRECT43_ORIGINAL_BASELINE_PREPARATION_V003_RECEIPT.json', 'a78bed8c643bf9b426ceb92e590374e9297d1c440d25078840c183d8a95417e9', 'CLOSED')
OUTCOME='success'
NATURAL_CLOSURE={'pid': 1071, 'session_id': 4932, 'naturally_closed': True, 'exit_code': 0, 'process_absent': True, 'observed_utc': '2026-10-08T07:37:21.458079+00:00', 'exit_observation': 'root actual session completion recorded before continuation; fresh ps absence rechecked'}
PROOF_FILE='READONLY_NATURAL_CLOSED_DIRECT43_BASELINE_SUCCESS_SEALS_V001.json'
STEM='DIRECT43_ORIGINAL_BASELINE_PREPARATION_V003'
MEASUREMENT_STATUS='DIRECT43_ORIGINAL_BASELINE_FIELDS_PREPARED_UNQUALIFIED'
PROTOCOL='READONLY_CLOSED_DIRECT43_BASELINE_SEALS_V001.md'
PROTOCOL_SHA='13d9cd55af0e3ca37fd53eb1a149b1e9a3e477af5700cd944164868b114d858d'
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
np=None
VERIFIED={};STATS={};TOTAL_BYTES=0

def verified(name, digest):
    global TOTAL_BYTES
    p = Path(name); p = (p if p.is_absolute() else BASE / p).resolve()
    key = str(p)
    if key in VERIFIED:
        assert VERIFIED[key] == digest
        s = p.stat(); assert STATS[key] == dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=oct(s.st_mode & 0o777)); return p
    before = p.stat(); assert before.st_size > 0
    h = hashlib.sha256()
    with p.open('rb') as f:
        while block := f.read(1024 * 1024): h.update(block)
    assert h.hexdigest() == digest, name
    after = p.stat()
    assert (before.st_ino, before.st_size, before.st_mtime_ns) == (after.st_ino, after.st_size, after.st_mtime_ns), name
    VERIFIED[key] = digest; TOTAL_BYTES += after.st_size
    STATS[key] = dict(inode=after.st_ino, size=after.st_size, mtime_ns=after.st_mtime_ns, mode=oct(after.st_mode & 0o777))
    return p

def header(f):
    version = np.lib.format.read_magic(f)
    assert version in ((1, 0), (2, 0)), ('unreviewed_public_NPY_header_version', version)
    value = np.lib.format.read_array_header_1_0(f) if version == (1, 0) else np.lib.format.read_array_header_2_0(f)
    return value, version, f.tell()

def thin(ref):
    return {k: ref[k] for k in ('file', 'sha256', 'commit_file', 'commit_sha256')}

def source_constants(path):
    out={}
    for n in ast.parse(path.read_text()).body:
        if not isinstance(n,ast.Assign) or len(n.targets)!=1 or not isinstance(n.targets[0],ast.Name):continue
        name=n.targets[0].id
        if name=='FLAGS':
            assert isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='dict' and not n.value.args
            assert all(k.arg is not None for k in n.value.keywords) and len({k.arg for k in n.value.keywords})==len(n.value.keywords)
            out[name]={k.arg:ast.literal_eval(k.value) for k in n.value.keywords}
        else:
            try:out[name]=ast.literal_eval(n.value)
            except (TypeError,ValueError):pass
    return out

def bounded_json(path):
    assert path.stat().st_size<=16*1024*1024,path.name
    return json.loads(path.read_bytes())

def canonical(value):return json.loads(json.dumps(value))

def record_role(ordinal):
    assert type(ordinal) is int and 0<=ordinal<87
    return 'INPUT' if ordinal==0 else ('REFERENCE_EVENT' if ordinal%2 else 'BASELINE_EVENT')

def archive_record(ref,ordinal,owner,receipt,failure=False):
    role='ERROR_RAW' if failure else record_role(ordinal)
    assert ref['file']==STEM+'_%05d_%s.npz'%(ordinal,role) and ref['commit_file']==ref['file']+'.COMMIT.json'
    for name,digest in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):assert receipt['output_sha256'][name]==digest
    ap=verified(ref['file'],ref['sha256']);cp=verified(ref['commit_file'],ref['commit_sha256']);assert not ap.stat().st_mode&0o222 and not cp.stat().st_mode&0o222
    commit=bounded_json(cp);assert set(commit)=={'file','sha256','metadata'} and commit=={k:ref[k] for k in ('file','sha256','metadata')}
    md=ref['metadata'];assert md['owner']==owner and md['qualification']==FLAGS and md['failed'] is failure
    assert isinstance(md['schema'],dict) and all(isinstance(n,str) and n for n in md['schema'])
    if not failure:assert md['physical_adoption'] is False and all(field['finite'] is True for field in md['schema'].values())
    def slot(name,shape,dtype='float64'):assert md['schema'][name]==dict(shape=list(shape),dtype=dtype,finite=True)
    if role=='REFERENCE_EVENT':
        for name,shape in {'h':(3,3),'h_spatial_jets':(2,3,3),'N':(),'beta':(3,),'N_jets':(4,),'beta_jets':(4,3),'g':(4,4),'dg':(4,4,4)}.items():
            for word in ('hi','lo'):slot(name+'_'+word,shape)
        slot('axisymmetric_gauge_phi_exact_zero',(),'bool');assert type(md['axisymmetric_gauge_phi_exact_zero']) is bool and md['stationary_seed_adopted_as_current'] is False
    if role=='BASELINE_EVENT':
        for name in ('baseline_TOTAL_hdot','original47969_hdot','original60363_correction_hdot'):
            for word in ('hi','lo'):slot(name+'_'+word,(3,3))
        assert md['original_point_first_order'] is True and md['node_sum_then_lift_equivalence_claimed'] is md['Gauss_rate_interpolated'] is md['KADM_plus_Lie_inverse_used'] is False
    if role in ('REFERENCE_EVENT','BASELINE_EVENT'):
        assert md['index']==(ordinal-1)//2 and type(md['index']) is int and type(md['R']) is float and math.isfinite(md['R']) and md['R']>0
        assert md['Z']==0. and md['radial_side']=='left' and md['vertical_side']=='upper' and md['context']['index']==md['index'] and md['context']['R']==md['R']
    before=ap.stat();versions={};orders={}
    with zipfile.ZipFile(ap) as z:
        names=z.namelist();assert len(names)==len(set(names)) and set(names)=={n+'.npy' for n in md['schema']}|{'metadata_json.npy'}
        for name,schema in md['schema'].items():
            info=z.getinfo(name+'.npy')
            with z.open(info) as f:(shape,order,dtype),version,position=header(f)
            assert list(shape)==schema['shape'] and str(dtype)==schema['dtype'] and not dtype.hasobject and dtype.kind in 'fiub'
            assert position+math.prod(shape)*dtype.itemsize==info.file_size,name
            versions[str(version)]=versions.get(str(version),0)+1;orders[str(order)]=orders.get(str(order),0)+1
        with z.open('metadata_json.npy') as f:
            (shape,order,dtype),version,position=header(f);assert shape==() and not order and dtype.kind=='U' and dtype.itemsize<=16*1024*1024
            payload=f.read();assert len(payload)==dtype.itemsize and position+dtype.itemsize==z.getinfo('metadata_json.npy').file_size
            big=dtype.byteorder=='>' or dtype.byteorder=='=' and sys.byteorder=='big'
            assert json.loads(payload.decode('utf-32-be' if big else 'utf-32-le').rstrip('\x00'))==md
    after=ap.stat();assert (before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns)
    return dict(ordinal=ordinal,role=role,**thin(ref),owner_equal=True,failed=failure,embedded_metadata_equal=True,member_headers=len(md['schema']),public_header_versions=versions,fortran_order_counts=orders)

def input_contract(ref,constants,receipt):
    md=ref['metadata'];adm=md['admission'];selected=md['selected_records']
    assert set(selected)=={'reference_fields','current_metric_nodes','current_RATE_JETS','rate_correction','basis'} and md['catalogue']==list(constants['CATALOGUE'])
    assert adm['source_pins'] and adm['owned_K_Hbar_uses_original_q1_operation_order'] is True
    for group,terminal in constants['TERMINALS'].items():
        q=adm[group]
        for name,pin in terminal.items():assert q[name]==list(pin)
        assert q['all_selected_seals_verified'] is True
        if group in ('reference_fields','nodal_current'):
            assert q['closure_kind']=='historical_source_success_publications' and q['naturally_closed'] is q['exit_code'] is None
            assert q['authenticated_source_success_publications'] is q['original_process_absent'] is q['original_ERROR_and_ERROR_RECEIPT_absent'] is True
        else:assert q['closure_kind']=='observed_natural_success' and q['naturally_closed'] is True and q['exit_code']==0
    assert adm['point_TOTAL_baseline']['inherited_scientific_owner_preserved'] is True
    for name in ('reference_nodes_and_sigma1_shift_owned_by_original24903','current47969_solution_and_RATE_JETS_same_coefficients','correction60363_is_original139_point_increment','same_original_mesh_basis_and_fixed_materials','point_TOTAL_baseline_law_matches_original139_ancestry'):assert adm[name] is True
    assert adm['reference_event_provenance']==adm['finite_reference_provenance']
    for row in selected.values():
        assert set(row)=={'file','sha256','commit_file','commit_sha256'}
        for name,digest in ((row['file'],row['sha256']),(row['commit_file'],row['commit_sha256'])):assert receipt['input_sha256'][str((BASE/name).resolve())]==digest
    return adm

def main():
    global np
    assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and SOURCE==EXPECTED_SOURCE and OUTCOME in ('success','failure')
    assert all(v is not None for v in SOURCE+RECEIPT) and all(v is not None for v in (RESULT if OUTCOME=='success' else ERROR))
    assert isinstance(PROOF_FILE,str) and re.fullmatch(r'[A-Z0-9_]+\.json',PROOF_FILE) and not (BASE/PROOF_FILE).exists()
    nc=NATURAL_CLOSURE;assert isinstance(nc,dict) and nc['pid']==1071 and nc['session_id']==4932 and nc['naturally_closed'] is nc['process_absent'] is True and isinstance(nc['observed_utc'],str)
    assert type(nc['exit_code']) is int and nc['exit_code']==(0 if OUTCOME=='success' else 1)
    terminal=RESULT if OUTCOME=='success' else ERROR;assert terminal[0]==STEM+('_RESULT.json' if OUTCOME=='success' else '_ERROR.json') and terminal[2]==(MEASUREMENT_STATUS if OUTCOME=='success' else 'FAILED')
    assert RECEIPT[0] in (STEM+'_RECEIPT.json',STEM+'_ERROR_RECEIPT.json') and RECEIPT[2]==('CLOSED' if OUTCOME=='success' else 'CLOSED_ERROR')
    if OUTCOME=='success':assert RECEIPT[0]==STEM+'_RECEIPT.json' and not (BASE/(STEM+'_ERROR.json')).exists() and not (BASE/(STEM+'_ERROR_RECEIPT.json')).exists()
    verified(PROTOCOL,PROTOCOL_SHA);src=verified(*SOURCE);terminal_path=verified(*terminal[:2]);rcp=verified(*RECEIPT[:2]);constants=source_constants(src)
    assert constants['AUTHOR_DRAFT'] is constants['AUTHORING_IN_PROGRESS'] is False and constants['STEM']==STEM and constants['FLAGS']==FLAGS
    value=bounded_json(terminal_path);rc=bounded_json(rcp);owner=value['owner'];assert owner==rc['owner'] and owner['owner']=='root' and owner['pid']==nc['pid'] and owner['source_sha256']==SOURCE[1]
    assert value['status']==terminal[2] and value['qualification']==rc['qualification']==FLAGS and value['controls']==[] and rc['status']==RECEIPT[2]
    if OUTCOME=='success':assert rc['result_sha256']==RESULT[1] and rc['error_sha256'] is None
    else:assert rc['error_sha256']==ERROR[1]
    for name,digest in rc['input_sha256'].items():verified(name,digest)
    for name,digest in rc['output_sha256'].items():verified(name,digest)
    required=[SOURCE,(constants['IO_PARENT'],constants['IO_PARENT_SHA']),(constants['DRIVER_PROTOCOL'],constants['PROTOCOL_SHA']),*constants['PINS'].items(),constants['SELECTED_PROOF'][:2],constants['CATALOGUE']]
    required.extend(pin[:2] for group in constants['TERMINALS'].values() for pin in group.values())
    for name,digest in required:
        key=str((BASE/name).resolve())
        if OUTCOME=='success' or key in rc['input_sha256']:assert rc['input_sha256'][key]==digest
    assert bounded_json(BASE/(STEM+'_OWNER_START.json'))==owner
    manifest_path=BASE/(STEM+'_MANIFEST.json');manifest=None
    if manifest_path.exists():
        assert manifest_path.name in rc['output_sha256'];manifest=bounded_json(manifest_path)
        assert manifest['owner']==owner and manifest['events']==43 and manifest['planned_roles']==87 and manifest['controls']==0 and manifest['source_law_changed'] is manifest['physical_adoption'] is False
        assert manifest['terminal_bindings']==canonical(constants['TERMINALS']) and manifest['selected_proof']==list(constants['SELECTED_PROOF'])
        for name,digest in manifest['input_sha256'].items():assert rc['input_sha256'][name]==digest
    if OUTCOME=='success':assert manifest is not None
    import numpy as numpy
    np=numpy
    refs=value['checkpoints'];assert isinstance(refs,list);science=len(refs)-int(bool(refs and refs[-1]['metadata']['failed'] is True))
    assert 0<=science<=87 and (OUTCOME=='failure' or science==len(refs)==87)
    records=[archive_record(ref,i,owner,rc,i>=science) for i,ref in enumerate(refs)];assert len(refs)<=science+1 and all(ref['metadata']['failed'] is False for ref in refs[:science])
    adm=input_contract(refs[0],constants,rc) if science else None;axisym=[];events=[]
    for i in range(1,science):
        md=refs[i]['metadata']
        if i%2:
            assert md['reference_event_provenance']==adm['reference_event_provenance'] and md['finite_reference_provenance']==adm['finite_reference_provenance'];axisym.append(md['axisymmetric_gauge_phi_exact_zero'])
        else:
            rmd=refs[i-1]['metadata'];assert md['reference_event']==thin(refs[i-1]) and md['context']['reference_event']==thin(refs[i-1]) and md['R']==rmd['R'];events.append(dict(index=md['index'],R=md['R'],reference_event=thin(refs[i-1]),baseline_event=thin(refs[i])))
    if OUTCOME=='success':
        case=value['case'];assert case['status']==MEASUREMENT_STATUS and case['input']==thin(refs[0]) and case['events']==events and case['roles']==87 and case['controls']==0
        assert len(events)==len(axisym)==43 and len(rc['input_sha256'])==41 and len(rc['output_sha256'])==177
        assert case['baseline_only'] is case['new_coupled_increment_not_evaluated'] is True
        assert case['coupled_or_finite_correction_required_for_baseline_preparation'] is case['physical_circle_or_new43_prediction_earned'] is case['physical_adoption'] is False
        expected={STEM+'_'+n+'.json' for n in ('OWNER_START','MANIFEST','RESULT')}|{q[k] for q in refs for k in ('file','commit_file')};assert set(rc['output_sha256'])==expected
    else:
        assert isinstance(value['traceback'],str) and value['traceback'] and all(value.get(n) is None or isinstance(value[n],str) for n in ('raw_preservation_traceback','closing_traceback'))
        if rc.get('prior_receipt_sha256') is not None:verified(STEM+'_RECEIPT.json',rc['prior_receipt_sha256'])
    for name,before in STATS.items():
        st=Path(name).stat();assert before==dict(inode=st.st_ino,size=st.st_size,mtime_ns=st.st_mtime_ns,mode=oct(st.st_mode&0o777)),name
    proof=dict(status='READONLY_NATURAL_CLOSED_DIRECT43_BASELINE_SUCCESS_SEALS_VERIFIED' if OUTCOME=='success' else 'READONLY_NATURAL_CLOSED_DIRECT43_BASELINE_FAILED_PREFIX_SEALS_VERIFIED',verified_at=datetime.now(timezone.utc).isoformat(),owner=owner,source_sha256=SOURCE[1],result_sha256=RESULT[1] if OUTCOME=='success' else None,error_sha256=ERROR[1] if OUTCOME=='failure' else None,receipt_sha256=RECEIPT[1],observed_closure=nc,naturally_closed=True,exit_code=nc['exit_code'],all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,input_count=len(rc['input_sha256']),output_count=len(rc['output_sha256']),science_role_count=science,total_records=len(refs),records=records,controls=[],axisymmetric_gauge_phi_exact_zero_metadata=axisym,all_gauge_phi_exact_zero_metadata=bool(axisym and all(axisym)),gauge_phi_numeric_words_not_decoded=True,measurement_status=MEASUREMENT_STATUS if OUTCOME=='success' else 'FAILED',full87_preparation_completed=OUTCOME=='success',events=events,qualification=FLAGS,physical_adoption=False,circle_or_precision_admission=False,numeric_arrays_decoded=False,scientific_bodies_or_controls_replayed=False,source_finite_and_word_assertions_inherited=True,fresh_verified_bytes=TOTAL_BYTES,verified_sha256=VERIFIED,stable_stats=STATS)
    raw=(json.dumps(proof,indent=2,sort_keys=True,allow_nan=False)+'\n').encode();out=BASE/PROOF_FILE
    with out.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    out.chmod(0o444);print(json.dumps(dict(file=out.name,sha256=hashlib.sha256(raw).hexdigest(),outcome=OUTCOME,science_roles=science,controls=0)))

if __name__=='__main__':main()
