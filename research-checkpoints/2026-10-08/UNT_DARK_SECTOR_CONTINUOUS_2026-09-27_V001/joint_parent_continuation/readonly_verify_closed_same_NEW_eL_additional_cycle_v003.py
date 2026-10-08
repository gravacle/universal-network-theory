"""HELD byte/header custody of naturally closed same-NEW-eL cycle2.
Root alone binds and executes. Numeric payloads and scientific bodies are skipped.
"""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import ast,hashlib,json,math,os,re,sys,zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
SOURCE=('same_NEW_eL_adjoint_additional_cycle_v002.py', '3fddd656f7030f1765775b5b8442798b3c835a58b23518e79033208462541f56')
RESULT=('SAME_NEW_E_L_ADJOINT_ADDITIONAL_CYCLE_V002_RESULT.json', '919dedd8f078cf7b3cb04de3ae955f799ce5e29beecd4748ec07203be948a826', 'SAME_NEW_E_L_ADDITIONAL_CYCLE_SOURCE_ROWS_ADMITTED')
ERROR=(None,None,'FAILED')
RECEIPT=('SAME_NEW_E_L_ADJOINT_ADDITIONAL_CYCLE_V002_RECEIPT.json', '429e706174a37bb51b2b3c24771af063355afee486a0c807418956d731743886', 'CLOSED')
NATURAL_CLOSURE={'pid': 3335, 'session_id': 62923, 'naturally_closed': True, 'exit_code': 0, 'process_absent': True, 'observed_utc': '2026-10-08T07:55:37.128886+00:00'}
OUTCOME='success'
PROOF_FILE='READONLY_NATURAL_CLOSED_SAME_NEW_E_L_ADDITIONAL_CYCLE_SEALS_V001.json'
PROTOCOL='READONLY_CLOSED_SAME_NEW_E_L_ADDITIONAL_CYCLE_SEALS_V002.md'
PROTOCOL_SHA='31fb72e2a390ddffa59ca6719c5eb94cc398e59fe328e0e8832d22dedb9b07c0'
EXPECTED_SOURCE=('same_NEW_eL_adjoint_additional_cycle_v002.py','3fddd656f7030f1765775b5b8442798b3c835a58b23518e79033208462541f56')
EXPECTED_PREVIOUS_PROOF=('READONLY_NATURAL_CLOSED_NEW_E_L_REFINEMENT_SEALS_V001.json','5d58d3ff95c4ccd1b9018554ab67c38e021d5e7fbb5760c47e95f50add2b13d7','READONLY_NATURAL_CLOSED_NEW_E_L_REFINEMENT_SEALS_VERIFIED')
STEM='SAME_NEW_E_L_ADJOINT_ADDITIONAL_CYCLE_V002'
STATUS='READONLY_NATURAL_CLOSED_SAME_NEW_E_L_ADDITIONAL_CYCLE_SEALS_VERIFIED'
FAILURE_STATUS='READONLY_NATURAL_CLOSED_SAME_NEW_E_L_ADDITIONAL_CYCLE_FAILED_PREFIX_SEALS_VERIFIED'
MEASUREMENT_STATUSES=('SAME_NEW_E_L_ADDITIONAL_CYCLE_SOURCE_ROWS_ADMITTED','SAME_NEW_E_L_ADDITIONAL_CYCLE_SOURCE_ROWS_NOT_ADMITTED')
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
np=None
VERIFIED={};STATS={};TOTAL_BYTES=0
INITIAL_ROLES=('WARM_REFERENCE_CONTEXT','BASIS_CONTEXT','FACTOR_CONTEXT','CAP80_SOLUTION_COPY','CAP80_CANDIDATE_WORD_LINKS','CAP80_POSITIVE_COPY','ADDITIONAL_CYCLE_CONTEXT')


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

def streamed_result(path,record_callback,outcome):
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
                assert key in (('case','owner','qualification','status') if outcome=='success' else ('owner','qualification','status','traceback','raw_preservation_traceback','closing_traceback','input_sha256'));small[key]=value()
            space()
            if buf.startswith('}'):break
            char(',')
        char('}');space()
        while not done:fill();space()
        assert not buf and seen==({'case','checkpoints','controls','owner','qualification','status'} if outcome=='success' else {'owner','qualification','status','traceback','raw_preservation_traceback','closing_traceback','controls','checkpoints','input_sha256'})
    small['controls']=controls;return small

def verify_record(ref,ordinal,owner,rc,failed=False):
    match=re.fullmatch(re.escape(STEM)+r'_(\d{5})_([A-Z_]+)\.npz',ref['file']);assert match and int(match[1])==ordinal
    role=match[2];assert (role=='ERROR_RAW') if failed else role in set(INITIAL_ROLES)|{'ADJOINT_CHUNK','POSITIVE_CHUNK','NEW_RIGHT_ADJOINT','NEW_ASTAR_WEAK','ASTAR_POSITIVE','CANDIDATE','ITERATION_STATE','SOLUTION'}
    assert ref['commit_file']==ref['file']+'.COMMIT.json'
    for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):assert rc['output_sha256'][n]==h
    ap=verified(ref['file'],ref['sha256']);cp=verified(ref['commit_file'],ref['commit_sha256']);assert not ap.stat().st_mode&0o222 and not cp.stat().st_mode&0o222
    assert cp.stat().st_size<=4*1024*1024;commit=json.loads(cp.read_bytes());assert set(commit)=={'file','sha256','metadata'} and commit=={k:ref[k] for k in ('file','sha256','metadata')}
    md=ref['metadata'];assert md['owner']==owner and md['qualification']==FLAGS and md['failed'] is failed
    for n in ('physical_adoption','uniform_adjoint_or_global_inverse_qualified','phase_or_gauge_feedback_evaluated'):
        if n in md:assert md[n] is False
    def scalar(shape,dtype='float64'):return dict(shape=list(shape),dtype=dtype,finite=True)
    packed=lambda names:{n:scalar((403340,)) for n in names}
    solution={**packed(n+'_'+w for n in ('lambda','action','residual','increment') for w in ('hi','lo')),'scores':scalar((3,2))}
    schemas={'WARM_REFERENCE_CONTEXT':{'scores':scalar((3,2)),'norms':scalar((3,2)),'zero_source_both_words':scalar((3,),'bool')},'BASIS_CONTEXT':{'R':scalar((4,3784)),'dv':scalar((4,3784)),'hats':scalar((4,4,3,86,44))},'FACTOR_CONTEXT':{'active_nodes':scalar((),'int64')},'NEW_RIGHT_ADJOINT':packed(n+'_'+w for n in ('input','output') for w in ('hi','lo')),'NEW_ASTAR_WEAK':packed(n+'_'+w for n in ('input','output') for w in ('hi','lo')),'ASTAR_POSITIVE':packed(('input_hi','input_lo','envelope')),'CANDIDATE':solution,'SOLUTION':solution}
    schemas.update(CAP80_SOLUTION_COPY=solution,CAP80_CANDIDATE_WORD_LINKS={'exact_word_ties':scalar((9,),'bool')},CAP80_POSITIVE_COPY=packed(('input_hi','input_lo','envelope')),ADDITIONAL_CYCLE_CONTEXT={**packed(n+'_'+w for n in ('lambda','saved_action','rhs','residual') for w in ('hi','lo')),**packed(('original_scale','saved_positive')),'scores':scalar((3,2)),'source_norms':scalar((3,2)),'zero_source_both_words':scalar((3,),'bool')})
    if failed:
        assert md['kind']=='unfinished_same_NEW_eL_additional_cycle' and isinstance(md['context'],dict)
        schemas[role]=md['schema'];assert isinstance(md['schema'],dict)
        for name,s in md['schema'].items():assert isinstance(name,str) and s['finite'] is True and s['dtype'] in ('float64','int64','bool') and all(type(d) is int and d>=0 for d in s['shape'])
    else:
        assert md['additional_cycle'] is md['same_NEW_eL_source'] is True and len(md['previous_terminal'])==4
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
    return role,dict(ordinal=ordinal,role=role,**thin(ref),member_headers=len(md['schema']),public_header_versions=versions,failed=failed,owner_equal=True,embedded_metadata_equal=True,member_names_headers_and_structural_lengths_equal=True,qualification_all_false=True)

def previous_records(constants,rc):
    terminal=[constants[n] for n in ('PREVIOUS_SOURCE','PREVIOUS_RESULT','PREVIOUS_RECEIPT','PREVIOUS_PROOF')]
    assert tuple(terminal[3])==EXPECTED_PREVIOUS_PROOF and terminal[2][2]=='CLOSED' and terminal[1][2]=='NEW_E_L_REPRESENTED_ADJOINT_SOURCE_ROWS_NOT_ADMITTED'
    path=verified(*terminal[3][:2]);assert path.stat().st_size<=48*1024*1024;proof=json.loads(path.read_bytes())
    assert proof['status']==terminal[3][2] and proof['source_sha256']==terminal[0][1] and proof['result_sha256']==terminal[1][1] and proof['receipt_sha256']==terminal[2][1]
    assert proof['naturally_closed'] is proof['all_input_seals_verified'] is proof['all_output_seals_verified'] is proof['all_success_role_seals_verified'] is True and proof['exit_code']==0
    assert proof['source_relative_adjoint_rows_admitted'] is False and proof['iterations']==80 and proof['candidate_iterations']==[20,40,80] and proof['all_original_construction_controls_passed'] is True
    assert proof['numeric_arrays_decoded'] is proof['scientific_factor_or_control_actions_replayed'] is proof['physical_adoption'] is False
    rows={n:[] for n in ('SOLUTION','WARM_REFERENCE_CONTEXT','CANDIDATE','ASTAR_POSITIVE','ITERATION_STATE')};selected={}
    for row in proof['records']:
        if row['role'] in rows:rows[row['role']].append(row)
    assert len(rows['SOLUTION'])==len(rows['WARM_REFERENCE_CONTEXT'])==1 and len(rows['CANDIDATE'])==3 and len(rows['ITERATION_STATE'])==79
    previous_source=source_constants(verified(*terminal[0]));label=previous_source['GMRES_LABEL']+'_candidate_080_new_positive'
    for role in rows:
        for row in rows[role]:
            if role=='ITERATION_STATE' and row!=rows[role][-1]:continue
            p=verified(row['commit_file'],row['commit_sha256']);assert p.stat().st_size<=4*1024*1024;q=json.loads(p.read_bytes());md=q['metadata']
            assert q['file']==row['file'] and q['sha256']==row['sha256'] and md['owner']==proof['owner'] and md['failed'] is False and md['qualification']==FLAGS
            if role=='CANDIDATE' and md['iteration']!=80:continue
            if role=='ASTAR_POSITIVE' and md['context']['label']!=label:continue
            assert role not in selected;selected[role]=thin(row)
    assert set(selected)==set(rows) and selected['SOLUTION']==proof['total_lambda_source_certificate'] and selected['WARM_REFERENCE_CONTEXT']==proof['warm_reference_context']
    return terminal,proof,selected


def cycle_seed_metadata(md,role,previous,warm,selected,initial):
    canonical=lambda v:json.loads(json.dumps(v))
    assert md['previous_terminal']==canonical(previous)
    if role=='WARM_REFERENCE_CONTEXT':assert md['warm_terminal']==warm and md['norm_preparation_replayed'] is False
    if role=='CAP80_SOLUTION_COPY':assert md['previous_solution']==selected['SOLUTION'] and md['measured_admitted'] is False and md['prior_iteration_count']==80 and md['source_certificate_owns_total_lambda'] is True
    if role=='CAP80_CANDIDATE_WORD_LINKS':assert md['previous_solution']==selected['SOLUTION'] and md['previous_candidate']==selected['CANDIDATE'] and md['iteration']==80
    if role=='CAP80_POSITIVE_COPY':assert md['previous_positive']==selected['ASTAR_POSITIVE'] and md['exact_cap80_argument_words_verified'] is md['coefficient_unsigned_scope_only'] is True
    if role=='ADDITIONAL_CYCLE_CONTEXT':
        expected={**{n:selected[n] for n in ('SOLUTION','CANDIDATE','ASTAR_POSITIVE','WARM_REFERENCE_CONTEXT')},'LAST_ITERATION_STATE':selected['ITERATION_STATE']}
        assert md['previous_records']==expected and md['same_NEW_eL_source_and_original53_reference'] is md['cap80_not_resume_iteration80'] is True
        assert md['old80_basis_or_H_QR_imported'] is md['old80_actions_factors_or_source_norms_replayed'] is md['previous_source_rows_admitted'] is md['physical_adoption'] is False
        assert md['cycle_number']==2 and md['additional_cycle_cap']==80


def main():
    global np
    assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and SOURCE==EXPECTED_SOURCE and OUTCOME in ('success','failure')
    assert all(v is not None for v in SOURCE+RECEIPT) and all(v is not None for v in (RESULT if OUTCOME=='success' else ERROR))
    assert isinstance(PROOF_FILE,str) and re.fullmatch(r'[A-Z0-9_]+\.json',PROOF_FILE) and not (BASE/PROOF_FILE).exists()
    nc=NATURAL_CLOSURE;assert isinstance(nc,dict) and type(nc['pid']) is int and nc['pid']>0 and nc['session_id']==62923
    assert nc['naturally_closed'] is nc['process_absent'] is True and type(nc['exit_code']) is int and nc['exit_code']==(0 if OUTCOME=='success' else 1) and isinstance(nc['observed_utc'],str)
    terminal=RESULT if OUTCOME=='success' else ERROR;assert terminal[0]==STEM+('_RESULT.json' if OUTCOME=='success' else '_ERROR.json') and terminal[2] in (MEASUREMENT_STATUSES if OUTCOME=='success' else ('FAILED',))
    assert RECEIPT[0] in (STEM+'_RECEIPT.json',STEM+'_ERROR_RECEIPT.json') and RECEIPT[2]==('CLOSED' if OUTCOME=='success' else 'CLOSED_ERROR')
    if OUTCOME=='success':assert RECEIPT[0]==STEM+'_RECEIPT.json' and not (BASE/(STEM+'_ERROR.json')).exists() and not (BASE/(STEM+'_ERROR_RECEIPT.json')).exists()
    verified(PROTOCOL,PROTOCOL_SHA);source=verified(*SOURCE);tp=verified(*terminal[:2]);cp=verified(*RECEIPT[:2]);constants=source_constants(source)
    assert constants['AUTHOR_DRAFT'] is constants['AUTHORING_IN_PROGRESS'] is False and constants['STEM']==STEM and constants['FLAGS']==FLAGS
    assert constants['GMRES_LABEL']=='SAME_NEW_eL_additional80_mechanical_adjoint_GMRES' and constants['PROTOCOL_SHA']=='c38a4cfba0e845db32cc9975573c52de2c4ea7a5c980b528289b9ccfa2cc95e1'
    warm_names=('WARM_SOURCE','WARM_RESULT','WARM_RECEIPT','WARM_PROOF')
    assert constants['WARM_SOURCE']==(None,None) and all(constants[n]==(None,None,None) for n in warm_names[1:])
    parent_constants=source_constants(verified(*constants['PREVIOUS_SOURCE']))
    assert parent_constants['AUTHOR_DRAFT'] is parent_constants['AUTHORING_IN_PROGRESS'] is False
    effective_constants=dict(constants)
    for n in warm_names:
        value=parent_constants[n];assert isinstance(value,tuple) and len(value)==(2 if n=='WARM_SOURCE' else 3) and all(v is not None for v in value)
        effective_constants[n]=value
    constants=effective_constants
    assert cp.stat().st_size<=16*1024*1024;rc=json.loads(cp.read_bytes());owner=rc['owner'];assert owner['owner']=='root' and owner['pid']==nc['pid'] and owner['source_sha256']==SOURCE[1] and rc['qualification']==FLAGS and rc['status']==RECEIPT[2]
    if OUTCOME=='success':assert rc['result_sha256']==RESULT[1] and rc['error_sha256'] is None
    else:assert rc['error_sha256']==ERROR[1]
    for name,digest in rc['input_sha256'].items():verified(name,digest)
    for name,digest in rc['output_sha256'].items():verified(name,digest)
    required=[SOURCE,(constants['IO_PARENT'],constants['IO_PARENT_SHA']),(constants['DRIVER_PROTOCOL'],constants['PROTOCOL_SHA']),constants['SUPPORT_SOURCE'],constants['WARM_TEMPLATE'],constants['PARENT_TEMPLATE'],*constants['PINS'].items()]
    required.extend(constants[n][:2] for n in ('PREVIOUS_SOURCE','PREVIOUS_RESULT','PREVIOUS_RECEIPT','PREVIOUS_PROOF','WARM_SOURCE','WARM_RESULT','WARM_RECEIPT','WARM_PROOF','NODAL_SOURCE','NODAL_RECEIPT','NODAL_PROOF','NODAL_PROJECTION'))
    for name,digest in required:
        key=str((BASE/name).resolve())
        if OUTCOME=='success' or key in rc['input_sha256']:assert rc['input_sha256'][key]==digest
    canonical=lambda v:json.loads(json.dumps(v));warm=canonical([constants[n] for n in ('WARM_SOURCE','WARM_RESULT','WARM_RECEIPT','WARM_PROOF')]);previous=canonical([constants[n] for n in ('PREVIOUS_SOURCE','PREVIOUS_RESULT','PREVIOUS_RECEIPT','PREVIOUS_PROOF')])
    priorproof=None;selected={}
    if OUTCOME=='success' or str((BASE/constants['PREVIOUS_PROOF'][0]).resolve()) in rc['input_sha256']:
        previous,priorproof,selected=previous_records(constants,rc);previous=canonical(previous);assert priorproof['warm_terminal']==warm
    assert json.loads((BASE/(STEM+'_OWNER_START.json')).read_bytes())==owner
    manifest_path=BASE/(STEM+'_MANIFEST.json');manifest=None
    if manifest_path.exists():
        assert manifest_path.name in rc['output_sha256'] and manifest_path.stat().st_size<=16*1024*1024;manifest=json.loads(manifest_path.read_bytes())
        assert manifest['owner']==owner and manifest['warm_terminal']==warm and manifest['previous_terminal']==previous and manifest['additional_cycle_cap']==80 and manifest['cumulative_budget']==160
        assert manifest['same_NEW_eL_source_and_reference'] is True and manifest['old80_actions_factors_or_basis_replayed'] is manifest['physical_adoption'] is False
        for name,digest in manifest['input_sha256'].items():assert rc['input_sha256'][name]==digest
    if OUTCOME=='success':assert manifest is not None and priorproof is not None
    import numpy as numpy
    np=numpy
    records=[];counts=Counter();response_refs=[];candidate_iterations=[];state_iterations=[];nonreused_positive=0;pending_role=None;pending=[];solution_metadata=None;context_records=[];raw_seen=False
    def accept(ref,ordinal):
        nonlocal pending_role,pending,nonreused_positive,solution_metadata,raw_seen
        failed=ref['metadata']['failed'];assert type(failed) is bool and (not failed or OUTCOME=='failure') and not raw_seen
        role,row=verify_record(ref,ordinal,owner,rc,failed);records.append(row);counts[role]+=1;md=ref['metadata']
        if failed:raw_seen=True;assert md['previous_terminal']==previous;return
        assert md['previous_terminal']==previous
        if ordinal<len(INITIAL_ROLES):
            assert role==INITIAL_ROLES[ordinal];context_records.append(dict(row,metadata=md));assert priorproof is not None
            cycle_seed_metadata(md,role,previous,warm,selected,context_records);return
        if role in ('ADJOINT_CHUNK','POSITIVE_CHUNK'):
            assert pending_role in (None,role);pending_role=role;serial=len(pending);iq,lo=serial//30,(serial%30)*128;hi=min(lo+128,3784)
            assert serial<120 and md['column']==iq and md['selection']==[lo,hi];label=md['label'];assert not pending or pending[0]==label;pending.append(label);return
        if role=='NEW_ASTAR_WEAK':
            assert pending_role=='ADJOINT_CHUNK' and len(pending)==120 and md['context']['label']==pending[0] and md['total_or_direction_action_owns_its_argument'] is True;pending_role=None;pending=[]
        elif role=='ASTAR_POSITIVE':
            reused=md['earned_exact_warm_argument_bound_reused'];assert type(reused) is bool and md['coefficient_scope_only'] is True
            if reused:assert pending_role is None and not pending
            else:assert pending_role=='POSITIVE_CHUNK' and len(pending)==120 and md['context']['label']==pending[0];nonreused_positive+=1;pending_role=None;pending=[]
        else:assert pending_role is None and not pending
        if role=='CANDIDATE':
            i=md['iteration'];assert type(i) is int and 1<=i<=80 and (not candidate_iterations or candidate_iterations[-1]<i) and md['total_lambda_not_correction_owns_certificate'] is True and type(md['admitted']) is bool;candidate_iterations.append(i)
        if role=='ITERATION_STATE':state_iterations.append(md['iteration'])
        if role=='SOLUTION':assert solution_metadata is None;solution_metadata=md
        if role in {'NEW_RIGHT_ADJOINT','NEW_ASTAR_WEAK','ASTAR_POSITIVE','CANDIDATE','ITERATION_STATE','SOLUTION'}:response_refs.append(thin(ref))
    value=streamed_result(tp,accept,OUTCOME);assert value['owner']==owner and value['qualification']==FLAGS and value['status']==terminal[2]
    controls=value['controls'];assert len(controls)<=5
    for control in controls:
        assert control['tolerance']==2e-11 and type(control['passed']) is bool and math.isfinite(control['error']) and control['error']>=0 and control['passed']==(control['error']<=control['tolerance'])
        assert control['name'].startswith(constants['GMRES_LABEL']+'_')
    case=history=None;admitted=False;iterations=None;scores=None;planned=[]
    if OUTCOME=='success':
        assert not raw_seen and not pending and pending_role is None;case=value['case'];history=case['history'];admitted=history['source_relative_adjoint_rows_admitted'];iterations=history['iterations'];reason=history['reason']
        assert type(iterations) is int and 0<=iterations<=80 and type(admitted) is bool and history['new_cycle_cap']==history['cap']==case['current_cycle_cap']==80
        assert history['restarts']==case['restarts']==1 and history['current_cycle_restarts']==case['current_cycle_restarts']==0 and case['cycles']==history['cycle_number']==2
        assert history['previous_completed_iterations']==case['previous_completed_iterations']==80 and history['cumulative_iterations']==case['cumulative_iterations']==80+iterations and history['cumulative_iteration_budget']==160
        assert history['new_rhs'] is False and history['same_NEW_eL_source_and_original53_reference'] is history['additional_correction_cycle'] is case['same_NEW_eL_source_and_reference'] is True
        assert history['previous_terminal']==case['previous_terminal']==previous and case['previous_solution']==selected['SOLUTION'] and case['original_cap80_measurement_preserved'] is True
        assert value['status']==case['status']==MEASUREMENT_STATUSES[0 if admitted else 1]
        for n in ('old_actions_factors_or_norm_preparation_replayed','original147_or_forward_physical_rows_tested','normal_phase_or_gauge_feedback_evaluated','uniform_adjoint_or_global_inverse_qualified','previous80_actions_factors_or_basis_replayed','physical_adoption'):assert case[n] is False
        assert case['new_rhs_basis'] is case['old_RHS_iterations_not_relabelled'] is True and case['warm_terminal']==warm
        for n in ('old_basis_actions_or_factors_replayed','exact_DD_superposition_assumed','original147_or_forward_physical_rows_tested','uniform_adjoint_or_global_inverse_qualified','previous80_actions_factors_and_basis_replayed','physical_adoption','normal_feedback_or_physical_adoption'):assert history[n] is False
        assert history['old_rhs_iterations_not_relabelled'] is history['old_action_at_warm_lambda_reused'] is history['warm_start'] is True
        assert history['operator']=='represented_directed_original244_coefficient_Astar' and history['column_action_scopes']==['represented_coefficient_Astar']*iterations and history['recurrence_action_scope']=='represented_coefficient_Astar'
        assert reason in {'NEW_source_relative_adjoint_rows_admitted','explicit_cap','exact_QR_pivot_breakdown','exact_Arnoldi_breakdown_without_original_admission'}
        scores=case['source_relative_scores'];assert len(scores)==3 and all(len(row)==2 for row in scores) and all(math.isfinite(x) and x>=0 for row in scores for x in row)
        assert admitted==all(x<=1e-10 for row in scores for x in row)
        assert counts['SOLUTION']==1 and records[-1]['role']=='SOLUTION' and case['solution']==thin(records[-1])
        assert history['new_stage_refs']==response_refs and solution_metadata['history']=={k:v for k,v in history.items() if k not in ('new_stage_refs','normal_feedback_or_physical_adoption')}
        assert solution_metadata['NEW_RHS_feedback_admission']==admitted and solution_metadata['phase_or_gauge_feedback_evaluated'] is False
        last_norm_candidate=iterations>0 and iterations%20!=0 and reason in ('NEW_source_relative_adjoint_rows_admitted','exact_Arnoldi_breakdown_without_original_admission')
        planned=[i for i in (20,40,80) if i<=iterations]+([iterations] if last_norm_candidate else []);assert candidate_iterations==planned
        if reason=='explicit_cap':assert iterations==80
        recurrence=iterations+int(reason=='exact_QR_pivot_breakdown');ncandidates=len(planned)
        assert all(counts[n]==1 for n in INITIAL_ROLES)
        assert counts['NEW_RIGHT_ADJOINT']==recurrence+ncandidates and counts['NEW_ASTAR_WEAK']==recurrence+3*ncandidates and counts['ADJOINT_CHUNK']==120*counts['NEW_ASTAR_WEAK']
        assert counts['ASTAR_POSITIVE']==4*ncandidates and counts['POSITIVE_CHUNK']==120*nonreused_positive and nonreused_positive<=3*ncandidates
        states=iterations if reason=='exact_QR_pivot_breakdown' else max(0,iterations-1);assert state_iterations==list(range(1,states+1))
        expected_controls=[constants['GMRES_LABEL']+'_candidate_%03d_NEW_original_residual_update_construction'%i for i in planned]+[constants['GMRES_LABEL']+'_all_Arnoldi_reconstructions']
        if iterations:expected_controls.append(constants['GMRES_LABEL']+'_small_QR_operation_norm')
        assert [c['name'] for c in controls]==expected_controls and all(c['passed'] is True for c in controls)
        assert case['roles']==value['checkpoints_count']==len(records) and case['controls']==value['controls_count']==len(controls)
        assert history['fresh_total_action_evaluated'] is (iterations>0) and history['represented_coefficient_acceptance_action_used'] is True
        expected={STEM+'_'+n+'.json' for n in ('OWNER_START','MANIFEST','RESULT')}|{q[k] for q in records for k in ('file','commit_file')};assert set(rc['output_sha256'])==expected and len(expected)==3+2*len(records)
    else:
        assert isinstance(value['traceback'],str) and value['traceback'] and all(value.get(n) is None or isinstance(value[n],str) for n in ('raw_preservation_traceback','closing_traceback'))
        assert value['input_sha256']==rc['input_sha256'] and (not state_iterations or state_iterations==list(range(1,state_iterations[-1]+1)))
        names=[c['name'] for c in controls];prefix=constants['GMRES_LABEL'];candidate_controls=[];tail=[]
        for name in names:
            match=re.fullmatch(re.escape(prefix)+r'_candidate_(\d{3})_NEW_original_residual_update_construction',name)
            if match:assert not tail and 1<=int(match[1])<=80;candidate_controls.append(int(match[1]))
            else:tail.append(name)
        assert candidate_controls==sorted(set(candidate_controls)) and tail in ([],[prefix+'_all_Arnoldi_reconstructions'],[prefix+'_all_Arnoldi_reconstructions',prefix+'_small_QR_operation_norm'])
        assert all(c['passed'] for c in controls[:-1])
        if rc.get('prior_receipt_sha256') is not None:verified(STEM+'_RECEIPT.json',rc['prior_receipt_sha256'])
    for name,before in STATS.items():
        s=Path(name).stat();assert before==dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=oct(s.st_mode&0o777)),name
    proof=dict(status=STATUS if OUTCOME=='success' else FAILURE_STATUS,verified_at=datetime.now(timezone.utc).isoformat(),owner=owner,source_file=SOURCE[0],source_sha256=SOURCE[1],result_file=RESULT[0] if OUTCOME=='success' else None,result_sha256=RESULT[1] if OUTCOME=='success' else None,error_file=ERROR[0] if OUTCOME=='failure' else None,error_sha256=ERROR[1] if OUTCOME=='failure' else None,receipt_file=RECEIPT[0],receipt_sha256=RECEIPT[1],naturally_closed=True,exit_code=nc['exit_code'],observed_closure=nc,all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,input_seals_verified=len(rc['input_sha256']),output_seals_verified=len(rc['output_sha256']),role_count=len(records),science_role_count=len(records)-counts['ERROR_RAW'],role_census=dict(counts),records=records,control_count=len(controls),controls=controls,all_original_construction_controls_passed=all(c['passed'] for c in controls),measurement_status=value['status'],source_relative_adjoint_rows_admitted=admitted if OUTCOME=='success' else None,source_relative_scores=scores,iterations=iterations,candidate_iterations=planned,case_history=history,total_lambda_source_certificate=case['solution'] if case is not None else None,warm_reference_context=thin(context_records[0]) if context_records else None,additional_cycle_context=thin(context_records[6]) if len(context_records)==7 else None,warm_terminal=warm,previous_terminal=previous,previous_cap80_admitted=False,cycle_number=2,previous_completed_iterations=80,cumulative_iteration_budget=160,pending_batch_role=pending_role,pending_batch_count=len(pending),qualification=FLAGS,numeric_arrays_decoded=False,norm_residual_source_or_action_recalculated=False,source_certificate_word_ties_and_numeric_finite_assertions_inherited_from_authenticated_producer=True,scientific_factor_or_control_actions_replayed=False,original147_association_forward_physical_or_global_inverse_recertified=False,physical_adoption=False,fresh_verified_bytes=TOTAL_BYTES,verified_sha256=VERIFIED,stable_stats=STATS,result_streaming_scope='One bounded JSON checkpoint/control value at a time; numeric NPZ payloads skipped; only Unicode metadata decoded.',scope='Natural-closure byte/header/metadata custody of cycle2 represented244 total-lambda SAME-NEW-eL measurement, or separate failed sealed prefix. No norm/action/control or physical admission is independently recomputed.')
    data=(json.dumps(proof,indent=2,sort_keys=True,allow_nan=False)+'\n').encode();out=BASE/PROOF_FILE
    with out.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    out.chmod(0o444);print(json.dumps(dict(file=out.name,sha256=hashlib.sha256(data).hexdigest(),roles=len(records),controls=len(controls),outcome=OUTCOME,source_relative_adjoint_rows_admitted=proof['source_relative_adjoint_rows_admitted'])))

if __name__=='__main__':main()
