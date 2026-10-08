"""HELD bounded byte/header custody of the NEW-eL represented244 refiner.
Root alone binds a naturally closed transaction and runs this verifier. Numeric
arrays, source norms, actions, controls and inverse claims are never recomputed.
"""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import ast,hashlib,json,math,os,re,sys,zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
SOURCE=('same_geometry_NEW_eL_saved_adjoint_refinement_v002.py', '859589c1dd50756dabc93a1563298d1bf99056beefe7bcd8f00166b59ad30d4e')
RESULT=('SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_REFINEMENT_V002_RESULT.json', 'ae527ae20678c6da63dfca367f59d224688180c7d1f95668367c6165e185f830', 'NEW_E_L_REPRESENTED_ADJOINT_SOURCE_ROWS_NOT_ADMITTED')
RECEIPT=('SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_REFINEMENT_V002_RECEIPT.json', '3b8c345b212922eb852ca1167f8a1e78ed3d83891cb62c77ad6166afe624141f', 'CLOSED')
NATURAL_CLOSURE={'pid': 90887, 'session_id': 84965, 'naturally_closed': True, 'process_absent': True, 'exit_code': 0, 'observed_utc': '2026-10-08T07:29:52.372709+00:00'}
PROOF_FILE='READONLY_NATURAL_CLOSED_NEW_E_L_REFINEMENT_SEALS_V001.json'
PROTOCOL='READONLY_CLOSED_NEW_E_L_REFINEMENT_SEALS_V001.md'
PROTOCOL_SHA='18a57f5507629b9809c4bcfedd10bae062c40d4a566a4d3025ef018118634984'
EXPECTED_SOURCE=('same_geometry_NEW_eL_saved_adjoint_refinement_v002.py','859589c1dd50756dabc93a1563298d1bf99056beefe7bcd8f00166b59ad30d4e')
STEM='SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_REFINEMENT_V002'
STATUS='READONLY_NATURAL_CLOSED_NEW_E_L_REFINEMENT_SEALS_VERIFIED'
MEASUREMENT_STATUSES=('NEW_E_L_REPRESENTED_ADJOINT_SOURCE_ROWS_ADMITTED','NEW_E_L_REPRESENTED_ADJOINT_SOURCE_ROWS_NOT_ADMITTED')
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
        if name=='FLAGS' and isinstance(n.value,ast.Call):
            assert isinstance(n.value.func,ast.Name) and n.value.func.id=='dict' and not n.value.args
            assert all(k.arg is not None for k in n.value.keywords) and len({k.arg for k in n.value.keywords})==len(n.value.keywords)
            out[name]={k.arg:ast.literal_eval(k.value) for k in n.value.keywords}
        else:
            try:out[name]=ast.literal_eval(n.value)
            except (TypeError,ValueError):pass
    return out

def streamed_result(path,record_callback):
    # Decode one checkpoint at a time, not the cumulative RESULT/checkpoint list.
    decoder=json.JSONDecoder();limit=16*1024*1024;buf='';done=False;small={};controls=[];seen=set()
    with path.open('r',encoding='utf-8') as f:
        def fill():
            nonlocal buf,done
            block=f.read(64*1024);done=not block;buf+=block
            assert len(buf)<=limit,'One RESULT value exceeds reviewed bounded parser'
        def space():
            nonlocal buf
            while True:
                buf=buf.lstrip()
                if buf or done:return
                fill()
        def char(c):
            nonlocal buf
            space();assert buf.startswith(c),(c,buf[:32]);buf=buf[1:]
        def value():
            nonlocal buf
            space()
            while True:
                try:v,end=decoder.raw_decode(buf);buf=buf[end:];return v
                except json.JSONDecodeError:
                    assert not done,'Incomplete RESULT JSON value';fill()
        char('{')
        while True:
            key=value();assert isinstance(key,str) and key not in seen;seen.add(key);char(':')
            if key in ('checkpoints','controls'):
                char('[');space();serial=0
                while not buf.startswith(']'):
                    v=value();assert isinstance(v,dict)
                    if key=='checkpoints':record_callback(v,serial)
                    else:controls.append(v);assert len(controls)<=5,'Original cap80 permits at most three candidates plus two reconstruction controls'
                    serial+=1;space()
                    if buf.startswith(']'):break
                    char(',')
                char(']');small[key+'_count']=serial
            else:
                assert key in ('case','owner','qualification','status');small[key]=value()
            space()
            if buf.startswith('}'):break
            char(',')
        char('}');space()
        while not done:fill();space()
        assert not buf and seen=={'case','checkpoints','controls','owner','qualification','status'}
    small['controls']=controls;return small

def verify_record(ref,ordinal,owner,rc):
    match=re.fullmatch(re.escape(STEM)+r'_(\d{5})_([A-Z_]+)\.npz',ref['file']);assert match and int(match[1])==ordinal
    role=match[2];assert role in {'WARM_REFERENCE_CONTEXT','BASIS_CONTEXT','FACTOR_CONTEXT','ADJOINT_CHUNK','POSITIVE_CHUNK','NEW_RIGHT_ADJOINT','NEW_ASTAR_WEAK','ASTAR_POSITIVE','CANDIDATE','ITERATION_STATE','SOLUTION'}
    assert ref['commit_file']==ref['file']+'.COMMIT.json'
    for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):assert rc['output_sha256'][n]==h
    ap=verified(ref['file'],ref['sha256']);cp=verified(ref['commit_file'],ref['commit_sha256']);assert not ap.stat().st_mode&0o222 and not cp.stat().st_mode&0o222
    assert cp.stat().st_size<=4*1024*1024;commit=json.loads(cp.read_bytes());assert set(commit)=={'file','sha256','metadata'} and commit=={k:ref[k] for k in ('file','sha256','metadata')}
    md=ref['metadata'];assert md['owner']==owner and md['qualification']==FLAGS and md['failed'] is False
    for n in ('physical_adoption','uniform_adjoint_or_global_inverse_qualified','phase_or_gauge_feedback_evaluated'):
        if n in md:assert md[n] is False
    def scalar(shape,dtype='float64'):return dict(shape=list(shape),dtype=dtype,finite=True)
    packed=lambda names:{n:scalar((403340,)) for n in names}
    solution={**packed(n+'_'+w for n in ('lambda','action','residual','increment') for w in ('hi','lo')),'scores':scalar((3,2))}
    schemas={'WARM_REFERENCE_CONTEXT':{'scores':scalar((3,2)),'norms':scalar((3,2)),'zero_source_both_words':scalar((3,),'bool')},'BASIS_CONTEXT':{'R':scalar((4,3784)),'dv':scalar((4,3784)),'hats':scalar((4,4,3,86,44))},'FACTOR_CONTEXT':{'active_nodes':scalar((),'int64')},'NEW_RIGHT_ADJOINT':packed(n+'_'+w for n in ('input','output') for w in ('hi','lo')),'NEW_ASTAR_WEAK':packed(n+'_'+w for n in ('input','output') for w in ('hi','lo')),'ASTAR_POSITIVE':packed(('input_hi','input_lo','envelope')),'CANDIDATE':solution,'SOLUTION':solution}
    if role in ('ADJOINT_CHUNK','POSITIVE_CHUNK'):
        iq=md['column'];lo,hi=md['selection'];assert type(iq) is int and 0<=iq<4 and lo%128==0 and 0<=lo<3784 and hi==min(lo+128,3784);p=hi-lo
        schemas[role]=({**{n:scalar((33,p,3)) for n in ('native_hi','native_lo')},**{n:scalar((p,6)) for n in ('metric_hi','metric_lo')}} if role=='ADJOINT_CHUNK' else {'native':scalar((33,p,3)),'metric':scalar((p,6))})
        source=md['source'];assert set(source)=={'file','sha256','commit_file','commit_sha256'}
        for f,h in (('file','sha256'),('commit_file','commit_sha256')):assert rc['input_sha256'][str((BASE/source[f]).resolve())]==source[h]
    if role=='ITERATION_STATE':
        i=md['iteration'];assert type(i) is int and 1<=i<80 and md['next_iteration']==i and md['cap']==80 and md['old_RHS_prefix_not_imported'] is True
        assert md['column_action_scopes']==['represented_coefficient_Astar']*i
        schemas[role]={**packed(('basis_hi','basis_lo')),**{n:scalar((81,80)) for n in ('H_hi','H_lo','R')},**{n:scalar((80,)) for n in ('Givens_cos','Givens_sin')},'rotated_RHS':scalar((81,)),'initial_norm':scalar(()),'history':scalar((i,4)),**{n:scalar((i,)) for n in ('Arnoldi_contact_norms','Arnoldi_operation_bounds')}}
    assert md['schema']==schemas[role],role
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
            (shape,order,dtype),version,position=header(f);assert shape==() and dtype.kind=='U' and dtype.itemsize<=8*1024*1024
            payload=f.read();assert len(payload)==dtype.itemsize
            big=dtype.byteorder=='>' or dtype.byteorder=='=' and sys.byteorder=='big'
            assert json.loads(payload.decode('utf-32-be' if big else 'utf-32-le').rstrip('\x00'))==md
    after=ap.stat();assert (before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns)
    return role,dict(ordinal=ordinal,role=role,**thin(ref),member_headers=len(md['schema']),public_header_versions=versions,failed=False,owner_equal=True,embedded_metadata_equal=True,member_names_headers_and_structural_lengths_equal=True,qualification_all_false=True)

def main():
    global np
    assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and SOURCE==EXPECTED_SOURCE,'Root FULL-reviewed natural closure required'
    assert all(v is not None for q in (SOURCE,RESULT,RECEIPT) for v in q)
    assert RESULT[0]==STEM+'_RESULT.json' and RESULT[2] in MEASUREMENT_STATUSES and RECEIPT==(STEM+'_RECEIPT.json',RECEIPT[1],'CLOSED')
    assert isinstance(PROOF_FILE,str) and re.fullmatch(r'[A-Z0-9_]+\.json',PROOF_FILE) and not (BASE/PROOF_FILE).exists()
    assert isinstance(NATURAL_CLOSURE,dict) and NATURAL_CLOSURE['pid']==90887 and NATURAL_CLOSURE['session_id']==84965
    assert NATURAL_CLOSURE['naturally_closed'] is NATURAL_CLOSURE['process_absent'] is True and NATURAL_CLOSURE['exit_code']==0 and isinstance(NATURAL_CLOSURE['observed_utc'],str)
    assert not (BASE/(STEM+'_ERROR.json')).exists() and not (BASE/(STEM+'_ERROR_RECEIPT.json')).exists()
    verified(PROTOCOL,PROTOCOL_SHA);source=verified(*SOURCE);rp=verified(*RESULT[:2]);cp=verified(*RECEIPT[:2]);constants=source_constants(source)
    assert constants['AUTHOR_DRAFT'] is constants['AUTHORING_IN_PROGRESS'] is False and constants['STEM']==STEM and constants['FLAGS']==FLAGS
    assert constants['GMRES_LABEL']=='NEW_eL_warm_mechanical_adjoint_GMRES' and constants['PROTOCOL_SHA']=='634291a41fe9e624fbfb0216b13ed00f69839cde03080f3fefb7fab5bb0e0f93'
    assert cp.stat().st_size<=16*1024*1024;rc=json.loads(cp.read_bytes());owner=rc['owner']
    assert owner['owner']=='root' and owner['pid']==90887 and owner['source_sha256']==SOURCE[1] and rc['qualification']==FLAGS
    assert rc['status']=='CLOSED' and rc['result_sha256']==RESULT[1] and rc['error_sha256'] is None
    for name,digest in rc['input_sha256'].items():verified(name,digest)
    for name,digest in rc['output_sha256'].items():verified(name,digest)
    required=[SOURCE,(constants['IO_PARENT'],constants['IO_PARENT_SHA']),(constants['DRIVER_PROTOCOL'],constants['PROTOCOL_SHA']),constants['SUPPORT_SOURCE'],constants['WARM_TEMPLATE'],*constants['PINS'].items()]
    required.extend(constants[n][:2] for n in ('WARM_SOURCE','WARM_RESULT','WARM_RECEIPT','WARM_PROOF','NODAL_SOURCE','NODAL_RECEIPT','NODAL_PROOF','NODAL_PROJECTION'))
    for name,digest in required:assert rc['input_sha256'][str((BASE/name).resolve())]==digest
    assert json.loads((BASE/(STEM+'_OWNER_START.json')).read_bytes())==owner
    manifest_path=BASE/(STEM+'_MANIFEST.json');assert manifest_path.stat().st_size<=16*1024*1024;manifest=json.loads(manifest_path.read_bytes())
    canonical=lambda v:json.loads(json.dumps(v));warm=canonical([constants[n] for n in ('WARM_SOURCE','WARM_RESULT','WARM_RECEIPT','WARM_PROOF')])
    assert manifest['owner']==owner and manifest['warm_terminal']==warm and manifest['nodal_projection']==canonical(constants['NODAL_PROJECTION']) and manifest['new_cycle_cap']==80
    assert manifest['old_result_not_parsed'] is manifest['old_RHS_basis_not_imported'] is True and manifest['physical_adoption'] is False
    for name,digest in manifest['input_sha256'].items():assert rc['input_sha256'][name]==digest
    import numpy as numpy
    np=numpy
    records=[];counts=Counter();response_refs=[];candidate_iterations=[];state_iterations=[];nonreused_positive=0;pending_role=None;pending=[];solution_metadata=None;context_records=[]
    def accept(ref,ordinal):
        nonlocal pending_role,pending,nonreused_positive,solution_metadata
        role,row=verify_record(ref,ordinal,owner,rc);md=ref['metadata'];records.append(row);counts[role]+=1
        if ordinal<3:assert role==('WARM_REFERENCE_CONTEXT','BASIS_CONTEXT','FACTOR_CONTEXT')[ordinal];context_records.append(dict(row,metadata=md))
        if role in ('ADJOINT_CHUNK','POSITIVE_CHUNK'):
            assert pending_role in (None,role);pending_role=role;serial=len(pending);iq,lo=serial//30,(serial%30)*128;hi=min(lo+128,3784)
            assert serial<120 and md['column']==iq and md['selection']==[lo,hi]
            label=md['label'];assert not pending or pending[0]==label;pending.append(label);return
        if role=='NEW_ASTAR_WEAK':
            assert pending_role=='ADJOINT_CHUNK' and len(pending)==120 and md['context']['label']==pending[0] and md['total_or_direction_action_owns_its_argument'] is True
            pending_role=None;pending=[]
        elif role=='ASTAR_POSITIVE':
            reused=md['earned_exact_warm_argument_bound_reused'];assert type(reused) is bool and md['coefficient_scope_only'] is True
            if reused:assert pending_role is None and not pending
            else:
                assert pending_role=='POSITIVE_CHUNK' and len(pending)==120 and md['context']['label']==pending[0];nonreused_positive+=1;pending_role=None;pending=[]
        else:assert pending_role is None and not pending
        if role=='CANDIDATE':
            i=md['iteration'];assert type(i) is int and 1<=i<=80 and (not candidate_iterations or candidate_iterations[-1]<i)
            assert md['total_lambda_not_correction_owns_certificate'] is True and type(md['admitted']) is bool;candidate_iterations.append(i)
        if role=='ITERATION_STATE':state_iterations.append(md['iteration'])
        if role=='SOLUTION':assert solution_metadata is None;solution_metadata=md
        if role in {'NEW_RIGHT_ADJOINT','NEW_ASTAR_WEAK','ASTAR_POSITIVE','CANDIDATE','ITERATION_STATE','SOLUTION'}:response_refs.append(thin(ref))
    result=streamed_result(rp,accept);case=result['case'];history=case['history'];admitted=history['source_relative_adjoint_rows_admitted'];iterations=history['iterations'];reason=history['reason']
    assert result['owner']==owner and result['qualification']==FLAGS and result['status']==case['status']==RESULT[2]
    assert type(iterations) is int and 0<=iterations<=80 and type(admitted) is bool and history['new_cycle_cap']==history['cap']==80 and history['restarts']==case['restarts']==0 and case['cycles']==1 and case['new_cycle_cap80'] is True
    assert result['status']==MEASUREMENT_STATUSES[0 if admitted else 1]
    for n in ('old_actions_factors_or_norm_preparation_replayed','original147_or_forward_physical_rows_tested','normal_phase_or_gauge_feedback_evaluated','uniform_adjoint_or_global_inverse_qualified','physical_adoption'):assert case[n] is False
    assert case['new_rhs_basis'] is case['old_RHS_iterations_not_relabelled'] is True and case['warm_terminal']==warm
    for n in ('old_basis_actions_or_factors_replayed','exact_DD_superposition_assumed','original147_or_forward_physical_rows_tested','uniform_adjoint_or_global_inverse_qualified','physical_adoption','normal_feedback_or_physical_adoption'):assert history[n] is False
    assert history['old_rhs_iterations_not_relabelled'] is history['old_action_at_warm_lambda_reused'] is history['new_rhs'] is history['warm_start'] is True
    assert history['operator']=='represented_directed_original244_coefficient_Astar' and history['column_action_scopes']==['represented_coefficient_Astar']*iterations and history['recurrence_action_scope']=='represented_coefficient_Astar'
    assert reason in {'NEW_source_relative_adjoint_rows_admitted','already_NEW_source_relative_adjoint_rows_admitted','explicit_cap','exact_QR_pivot_breakdown','exact_Arnoldi_breakdown_without_original_admission'}
    scores=case['source_relative_scores'];assert len(scores)==3 and all(len(row)==2 for row in scores) and all(math.isfinite(x) and x>=0 for row in scores for x in row)
    assert admitted==all(x<=1e-10 for row in scores for x in row),'Saved source outcome preserved, not recomputed from arrays'
    assert counts['SOLUTION']==1 and records[-1]['role']=='SOLUTION' and case['solution']=={k:records[-1][k] for k in ('file','sha256','commit_file','commit_sha256')}
    assert history['new_stage_refs']==response_refs and solution_metadata['history']=={k:v for k,v in history.items() if k not in ('new_stage_refs','normal_feedback_or_physical_adoption')}
    assert solution_metadata['NEW_RHS_feedback_admission']==admitted and solution_metadata['phase_or_gauge_feedback_evaluated'] is False
    last_norm_candidate=iterations>0 and iterations%20!=0 and reason in ('NEW_source_relative_adjoint_rows_admitted','exact_Arnoldi_breakdown_without_original_admission')
    planned=[i for i in (20,40,80) if i<=iterations]+([iterations] if last_norm_candidate else []);assert candidate_iterations==planned
    if reason=='explicit_cap':assert iterations==80
    recurrence=iterations+int(reason=='exact_QR_pivot_breakdown');nc=len(planned)
    assert counts['WARM_REFERENCE_CONTEXT']==counts['BASIS_CONTEXT']==counts['FACTOR_CONTEXT']==1
    assert counts['NEW_RIGHT_ADJOINT']==recurrence+nc and counts['NEW_ASTAR_WEAK']==recurrence+3*nc and counts['ADJOINT_CHUNK']==120*counts['NEW_ASTAR_WEAK']
    assert counts['ASTAR_POSITIVE']==4*nc and counts['POSITIVE_CHUNK']==120*nonreused_positive and nonreused_positive<=3*nc
    states=iterations if reason=='exact_QR_pivot_breakdown' else max(0,iterations-1);assert state_iterations==list(range(1,states+1))
    initial_admitted=reason=='already_NEW_source_relative_adjoint_rows_admitted';expected_controls=[constants['GMRES_LABEL']+'_candidate_%03d_NEW_original_residual_update_construction'%i for i in planned]
    if not initial_admitted:expected_controls.append(constants['GMRES_LABEL']+'_all_Arnoldi_reconstructions')
    if iterations:expected_controls.append(constants['GMRES_LABEL']+'_small_QR_operation_norm')
    controls=result['controls'];assert [c['name'] for c in controls]==expected_controls and all(c['passed'] is True and c['tolerance']==2e-11 and math.isfinite(c['error']) and 0<=c['error']<=c['tolerance'] for c in controls)
    assert case['roles']==result['checkpoints_count']==len(records) and case['controls']==result['controls_count']==len(controls)
    assert history['fresh_total_action_evaluated'] is (iterations>0) and history['represented_coefficient_acceptance_action_used'] is (not initial_admitted)
    assert context_records[0]['metadata']['warm_terminal']==warm and context_records[0]['metadata']['norm_preparation_replayed'] is False
    expected={STEM+'_'+n+'.json' for n in ('OWNER_START','MANIFEST','RESULT')}|{q[k] for q in records for k in ('file','commit_file')};assert set(rc['output_sha256'])==expected and len(expected)==3+2*len(records)
    for name,before in STATS.items():
        s=Path(name).stat();assert before==dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=oct(s.st_mode&0o777)),name
    proof=dict(status=STATUS,verified_at=datetime.now(timezone.utc).isoformat(),owner=owner,source_file=SOURCE[0],source_sha256=SOURCE[1],result_file=RESULT[0],result_sha256=RESULT[1],receipt_file=RECEIPT[0],receipt_sha256=RECEIPT[1],naturally_closed=True,exit_code=0,observed_closure=NATURAL_CLOSURE,all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,input_seals_verified=len(rc['input_sha256']),output_seals_verified=len(rc['output_sha256']),role_count=len(records),role_census=dict(counts),records=records,control_count=len(controls),controls=controls,all_original_construction_controls_passed=True,measurement_status=result['status'],source_relative_adjoint_rows_admitted=admitted,source_relative_scores=scores,iterations=iterations,candidate_iterations=planned,case_history=history,total_lambda_source_certificate=case['solution'],warm_reference_context=thin(context_records[0]),warm_terminal=warm,qualification=FLAGS,numeric_arrays_decoded=False,norm_residual_source_or_action_recalculated=False,source_certificate_word_ties_and_numeric_finite_assertions_inherited_from_authenticated_producer=True,scientific_factor_or_control_actions_replayed=False,original147_association_forward_physical_or_global_inverse_recertified=False,physical_adoption=False,fresh_verified_bytes=TOTAL_BYTES,verified_sha256=VERIFIED,stable_stats=STATS,result_streaming_scope='One bounded JSON checkpoint at a time; numeric NPZ payloads skipped; only Unicode metadata payload decoded.',scope='Natural-closure byte/header/metadata custody of the saved represented244 total-lambda NEW-eL source certificate. Admission or nonadmission is preserved from the producer; original source norms/scales, DD argument ties, controls and inverse properties are not independently recomputed.')
    data=(json.dumps(proof,indent=2,sort_keys=True,allow_nan=False)+'\n').encode();out=BASE/PROOF_FILE
    with out.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    out.chmod(0o444);print(json.dumps(dict(file=out.name,sha256=hashlib.sha256(data).hexdigest(),roles=len(records),controls=len(controls),source_relative_adjoint_rows_admitted=admitted)))

if __name__=='__main__':main()
