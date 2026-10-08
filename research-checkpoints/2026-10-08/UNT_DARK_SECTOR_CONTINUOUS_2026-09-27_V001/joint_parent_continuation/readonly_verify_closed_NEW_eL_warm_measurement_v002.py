"""HELD three-role successful warm measurement custody; root binds/releases.
Preserves actual refinement-required outcome, not numerical/physical admission.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, math, os, re, sys, zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
SOURCE=('same_geometry_NEW_eL_saved_adjoint_warm_admission_v003.py', 'd416806f106ab608d8c1c7ac69f7c926a55e300e50f6de45acc16552de95b806')
RESULT=('SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_WARM_ADMISSION_V003_RESULT.json', '56f45f3742677c94a9ac3be10c31d4c73fb6453d9a36601e8549e00d0de7a4fd', 'NEW_E_L_SAVED_WARM_RESIDUAL_MEASURED_REFINEMENT_REQUIRED')
RECEIPT=('SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_WARM_ADMISSION_V003_RECEIPT.json', '07d01c6426906ce42f4765bbfd6fd0b93801276ab576fab7a591bdb62817b93d', 'CLOSED')
NATURAL_CLOSURE={'pid': 89302, 'session_id': 87575, 'naturally_closed': True, 'process_absent': True, 'exit_code': 0, 'observed_utc': '2026-10-08T06:30:00.891107+00:00'}
PROOF_FILE='READONLY_NATURAL_CLOSED_NEW_E_L_WARM_MEASUREMENT_SEALS_V001.json'
PROTOCOL='READONLY_CLOSED_NEW_E_L_WARM_MEASUREMENT_SEALS_V001.md'
PROTOCOL_SHA='a317b2b9c8c244d77ca834ec39fe484a0dbaa0f2cd6152c8e62a71b7aa9b4e44'
EXPECTED_SOURCE=('same_geometry_NEW_eL_saved_adjoint_warm_admission_v003.py','d416806f106ab608d8c1c7ac69f7c926a55e300e50f6de45acc16552de95b806')
STEM='SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_WARM_ADMISSION_V003'
MEASUREMENT_STATUS='NEW_E_L_SAVED_WARM_RESIDUAL_MEASURED_REFINEMENT_REQUIRED'
STATUS='READONLY_NATURAL_CLOSED_NEW_E_L_WARM_MEASUREMENT_SEALS_VERIFIED'
ROLES=('WORD_LINKS','WARMSTART_CONTEXT','MEASURED_ADMISSION')
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

def verify_record(ref,ordinal,owner,rc):
    role=ROLES[ordinal];assert ref['file']==STEM+'_%05d_%s.npz'%(ordinal,role) and ref['commit_file']==ref['file']+'.COMMIT.json'
    for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):assert rc['output_sha256'][n]==h
    ap=verified(ref['file'],ref['sha256']);cp=verified(ref['commit_file'],ref['commit_sha256']);assert not ap.stat().st_mode&0o222 and not cp.stat().st_mode&0o222
    assert cp.stat().st_size<=1024*1024;commit=json.loads(cp.read_bytes());assert set(commit)=={'file','sha256','metadata'} and commit=={k:ref[k] for k in ('file','sha256','metadata')}
    md=ref['metadata'];assert md['owner']==owner and md['qualification']==FLAGS and md['failed'] is md['physical_adoption'] is False
    expected={'WORD_LINKS':{'exact_word_ties':dict(shape=[2],dtype='bool',finite=True)},
              'WARMSTART_CONTEXT':{**{n+'_'+w:dict(shape=[403340],dtype='float64',finite=True) for n in ('lambda','saved_action','rhs','residual') for w in ('hi','lo')},**{n:dict(shape=[403340],dtype='float64',finite=True) for n in ('original_scale','saved_positive')},'scores':dict(shape=[3,2],dtype='float64',finite=True)},
              'MEASURED_ADMISSION':{**{n:dict(shape=[3,2],dtype='float64',finite=True) for n in ('scores','new_source_norms')},'new_source_exact_both_word_zero':dict(shape=[3],dtype='bool',finite=True)}}
    assert md['schema']==expected[role]
    before=ap.stat();versions={}
    with zipfile.ZipFile(ap) as z:
        names=z.namelist();assert len(names)==len(set(names)) and set(names)=={n+'.npy' for n in md['schema']}|{'metadata_json.npy'}
        for name,schema in md['schema'].items():
            info=z.getinfo(name+'.npy')
            with z.open(info) as f:(shape,order,dtype),version,position=header(f)
            assert list(shape)==schema['shape'] and str(dtype)==schema['dtype'] and not dtype.hasobject
            assert position+math.prod(shape)*dtype.itemsize==info.file_size,name
            versions[str(version)]=versions.get(str(version),0)+1
        with z.open('metadata_json.npy') as f:
            (shape,order,dtype),version,position=header(f);assert shape==() and dtype.kind=='U' and dtype.itemsize<=4*1024*1024
            payload=f.read();assert len(payload)==dtype.itemsize
            big=dtype.byteorder=='>' or dtype.byteorder=='=' and sys.byteorder=='big'
            assert json.loads(payload.decode('utf-32-be' if big else 'utf-32-le').rstrip('\x00'))==md
    after=ap.stat();assert (before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns)
    return dict(ordinal=ordinal,role=role,**thin(ref),member_headers=len(md['schema']),public_header_versions=versions,failed=False,owner_equal=True,embedded_metadata_equal=True,member_names_headers_and_structural_lengths_equal=True,qualification_all_false=True)

def main():
    global np
    assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and SOURCE==EXPECTED_SOURCE,'Root FULL-reviewed guarded release required'
    assert all(v is not None for q in (SOURCE,RESULT,RECEIPT) for v in q)
    assert RESULT[0]==STEM+'_RESULT.json' and RESULT[2]==MEASUREMENT_STATUS and RECEIPT[0]==STEM+'_RECEIPT.json' and RECEIPT[2]=='CLOSED'
    assert isinstance(PROOF_FILE,str) and re.fullmatch(r'[A-Z0-9_]+\.json',PROOF_FILE) and not (BASE/PROOF_FILE).exists()
    assert isinstance(NATURAL_CLOSURE,dict) and NATURAL_CLOSURE['pid']==89302 and NATURAL_CLOSURE['session_id']==87575
    assert NATURAL_CLOSURE['naturally_closed'] is NATURAL_CLOSURE['process_absent'] is True and NATURAL_CLOSURE['exit_code']==0 and isinstance(NATURAL_CLOSURE['observed_utc'],str)
    assert not (BASE/(STEM+'_ERROR.json')).exists() and not (BASE/(STEM+'_ERROR_RECEIPT.json')).exists()
    verified(PROTOCOL,PROTOCOL_SHA);source=verified(*SOURCE);rp=verified(*RESULT[:2]);cp=verified(*RECEIPT[:2]);constants=source_constants(source)
    assert constants['AUTHOR_DRAFT'] is constants['AUTHORING_IN_PROGRESS'] is False and constants['STEM']==STEM and constants['FLAGS']==FLAGS
    assert rp.stat().st_size<=1024*1024 and cp.stat().st_size<=1024*1024
    result=json.loads(rp.read_bytes());rc=json.loads(cp.read_bytes());owner=result['owner']
    assert owner==rc['owner'] and owner['owner']=='root' and owner['pid']==89302 and owner['source_sha256']==SOURCE[1]
    assert result['status']==MEASUREMENT_STATUS and rc['status']=='CLOSED' and rc['result_sha256']==RESULT[1] and rc['error_sha256'] is None
    assert result['qualification']==rc['qualification']==FLAGS and result['controls']==[] and len(rc['input_sha256'])==34 and len(rc['output_sha256'])==9
    for name,digest in rc['input_sha256'].items():verified(name,digest)
    for name,digest in rc['output_sha256'].items():verified(name,digest)
    for name,digest in ((SOURCE[0],SOURCE[1]),(constants['IO_PARENT'],constants['IO_PARENT_SHA']),(constants['DRIVER_PROTOCOL'],constants['PROTOCOL_SHA']),*constants['PINS'].items()):assert rc['input_sha256'][str((BASE/name).resolve())]==digest
    assert json.loads((BASE/(STEM+'_OWNER_START.json')).read_bytes())==owner
    manifest=json.loads((BASE/(STEM+'_MANIFEST.json')).read_bytes());assert manifest['owner']==owner and manifest['selected_old_payload_roles']==3 and manifest['selected_new_payload_roles']==1
    assert manifest['old_result_not_parsed'] is True and manifest['point_or_factor_actions_scheduled'] is manifest['physical_adoption'] is False
    for name,digest in manifest['input_sha256'].items():assert rc['input_sha256'][name]==digest
    canonical=lambda v:json.loads(json.dumps(v));old=[constants[n] for n in ('OLD_SOURCE','OLD_RESULT','OLD_RECEIPT','OLD_PROOF')];new=[constants[n] for n in ('NEW_E_L_SOURCE','NEW_E_L_RESULT','NEW_E_L_RECEIPT','NEW_E_L_PROOF')]
    assert manifest['old_terminal']==canonical(old) and manifest['new_terminal']==canonical(new)
    import numpy as numpy
    np=numpy
    refs=result['checkpoints'];assert len(refs)==3;records=[verify_record(q,i,owner,rc) for i,q in enumerate(refs)]
    expected={STEM+'_'+n+'.json' for n in ('OWNER_START','MANIFEST','RESULT')}|{q[k] for q in refs for k in ('file','commit_file')};assert set(rc['output_sha256'])==expected
    case=result['case'];assert case['status']==MEASUREMENT_STATUS and case['roles']==3 and case['construction_controls']==case['new_point_actions']==case['new_factor_applications']==0
    assert case['source_relative_adjoint_rows_admitted'] is False and case['refinement_required'] is True and case['new_cycle_cap_if_refined']==80
    for n in ('old_actions_factors_unsigned_or_basis_replayed','normal_phase_or_gauge_feedback_evaluated','uniform_adjoint_or_global_inverse_qualified','physical_adoption'):assert case[n] is False
    assert case['old_RHS_iterations_not_relabelled'] is True
    assert [case[n] for n in ('word_links','warm_context','measured_admission')]==[thin(q) for q in refs]
    m0,m1,m2=[q['metadata'] for q in refs];ad=m2['admission'];assert m2['word_links']==thin(refs[0]) and m2['refinement_required'] is True and m2['source_relative_adjoint_rows_admitted'] is False
    assert m1['NEW_initial_source_rows_admitted'] is False and m1['old_source_rows_admitted'] is True and m1['old_basis_not_reused'] is True and m1['old_action_or_factor_replayed'] is False
    assert m2['old_actions_factors_unsigned_or_basis_replayed'] is False and m1['old_solution']==m0['solution']==ad['old_solution_record'] and m1['fresh_eL']==ad['new_eL_record'] and m0['positive']==ad['old_positive_record']
    assert ad['terminals']==canonical(old+new) and ad['operator']=='represented_directed_original244_coefficient_Astar' and ad['uniform_adjoint_or_global_inverse_qualified'] is ad['physical_adoption'] is False
    for name in ('all_selected_seals_verified','old_solution_and_action_argument_words_verified','same_paired_point_descriptors_and_original_basis_verified','same_147_raw_configuration_and_E0_words_verified','same_right_factor_and_original_coordinate_scale_verified','new_eL_copied_from_fresh139_literal142_bridge','callbacks_publish_completed_operands_without_mutation','old_positive_bound_at_exact_warm_lambda_verified','old_source_rows_admitted'):assert ad[name] is True
    scores=case['source_relative_scores'];assert len(scores)==3 and all(len(row)==2 for row in scores) and all(math.isfinite(x) and x>1e-10 for row in scores for x in row)
    for name,before in STATS.items():
        s=Path(name).stat();assert before==dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=oct(s.st_mode&0o777)),name
    proof=dict(status=STATUS,verified_at=datetime.now(timezone.utc).isoformat(),owner=owner,source_file=SOURCE[0],source_sha256=SOURCE[1],result_file=RESULT[0],result_sha256=RESULT[1],receipt_file=RECEIPT[0],receipt_sha256=RECEIPT[1],naturally_closed=True,exit_code=0,observed_closure=NATURAL_CLOSURE,all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,input_count=34,output_count=9,success_roles=3,controls=[],control_count=0,records=records,word_links=case['word_links'],warm_context=case['warm_context'],measured_admission=case['measured_admission'],measurement_status=MEASUREMENT_STATUS,source_relative_scores=scores,source_relative_adjoint_rows_admitted=False,refinement_required=True,all_six_source_relative_rows_not_admitted=True,new_cycle_cap_if_refined=80,old_terminal=canonical(old),new_eL_terminal=canonical(new),qualification=FLAGS,numeric_arrays_decoded=False,norm_residual_source_or_action_recalculated=False,word_tie_and_finite_assertions_inherited_from_authenticated_producer=True,scientific_or_factor_actions_replayed=False,normal_phase_gauge_feedback_or_physical_admission=False,fresh_verified_bytes=TOTAL_BYTES,verified_sha256=VERIFIED,stable_stats=STATS,scope='Successful byte/header/metadata custody of a nonadmitted NEW-eL warm residual measurement. Original both-word source norm/zero/scaled operands remain saved; no independent numerical norm/word/scale/control certification or physical inference. MEASURED metadata.context is active execution context; the reusable warm record is case.warm_context.')
    data=(json.dumps(proof,indent=2,sort_keys=True,allow_nan=False)+'\n').encode();out=BASE/PROOF_FILE
    with out.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    out.chmod(0o444);print(json.dumps(dict(file=out.name,sha256=hashlib.sha256(data).hexdigest(),roles=3,controls=0,refinement_required=True)))

if __name__=='__main__':main()
