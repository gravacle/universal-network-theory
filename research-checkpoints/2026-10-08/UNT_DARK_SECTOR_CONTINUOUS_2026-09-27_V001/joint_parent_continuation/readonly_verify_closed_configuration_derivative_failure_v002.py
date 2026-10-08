"""HELD old29468/29272 natural-closure failure byte/header custody only.
Root alone binds/releases; no numeric-array decode or scientific replay.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, math, os, re, sys, zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
KIND='configuration'
SOURCE=('cross_u_candidate_whole_configuration_york_contact_v002.py', '4e22dfa402b4938805852f6127fb5ab3cffd53d03b4c709c85d3230648f71c52')
ERROR=('CROSS_U_CANDIDATE_WHOLE_CONFIGURATION_YORK_CONTACT_V002_ERROR.json', 'f84553f6d4a6ec3e5b24444bf23e3de63019c6da6026401b0bf506c386aaf4bb')
RECEIPT=('CROSS_U_CANDIDATE_WHOLE_CONFIGURATION_YORK_CONTACT_V002_RECEIPT.json', 'aa66d3725ef6da56301646cd7a4468ad0275c7aa56055dba878ac64fed642601')
NATURAL_CLOSURE={'pid': 29272, 'session_id': 92578, 'naturally_closed': True, 'process_absent': True, 'exit_code': 1, 'observed_utc': '2026-10-08T06:37:25.836142+00:00'}
PROOF_FILE='READONLY_NATURAL_CLOSED_CONFIGURATION_DERIVATIVE_FAILURE_SEALS_V001.json'
PROTOCOL='READONLY_CLOSED_COMPLETED_DERIVATIVE_FAILURE_SEALS_V001.md'
PROTOCOL_SHA='2ddb26c7ce4f1245481feeeced3b69c9ded0fb59035fe6400bec21e613303db1'
STATUS='READONLY_NATURAL_CLOSED_COMPLETED_DERIVATIVE_CLOSURE_FAILURE_SEALS_VERIFIED'
MAX_RECORD_TEXT=16*1024*1024
MAX_TAIL_TEXT=1024*1024
SPECS={
 'mechanical':dict(source=('cross_u_candidate_mechanical_rate_normal_controls_v002.py','2631ad5e878e27ac45cb3cc4b514481cd5bac81d412edc7c1862b62daecad206'),stem='CROSS_U_CANDIDATE_MECHANICAL_RATE_NORMAL_CONTROLS_V002',pid=29468,session=55508,success=153,controls=40,inputs=172,outputs=311,readouts=(78,152),readout_role='READOUT',raw_kind='available_unfinished_NEW_mechanical_rate_normal_CMC',traceback_sha256='1be6928b7708c59a4f10dd95afe6fd50bca07b8e62b8ea39387874de414d3914',closing_traceback_sha256='33ad5d5ce88d673d6b09f704848e1e22aceed05750b47c3f3a0593ecaa71dc33'),
 'configuration':dict(source=('cross_u_candidate_whole_configuration_york_contact_v002.py','4e22dfa402b4938805852f6127fb5ab3cffd53d03b4c709c85d3230648f71c52'),stem='CROSS_U_CANDIDATE_WHOLE_CONFIGURATION_YORK_CONTACT_V002',pid=29272,session=92578,success=147,controls=22,inputs=189,outputs=299,readouts=(76,146),readout_role='FULL_WEAK',raw_kind='available_unfinished_NEW_whole_configuration_York_contact',traceback_sha256='cd4f45db870a1fd9337ba0e4bf4eda17419ae325e7afb09791cfedcf66f9a445',closing_traceback_sha256='dafefb425929af7473b446033ca4703183d44e9eee3c2a2d80658874ba464e33')}
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

def unique_object(pairs):
    value={}
    for key,item in pairs:assert key not in value,key;value[key]=item
    return value

def small_json(path,limit=MAX_RECORD_TEXT):
    assert path.stat().st_size<=limit,path.name
    return json.loads(path.read_bytes(),object_pairs_hook=unique_object)

def checkpoint_stream(path,state,count):
    # The original pinned P.encode writes sorted compact JSON with checkpoints first.
    decoder=json.JSONDecoder(object_pairs_hook=unique_object)
    with path.open('r',encoding='utf-8') as f:
        assert f.read(16)=='{"checkpoints":[',path.name
        buffer=''
        for ordinal in range(count):
            while True:
                try:record,end=decoder.raw_decode(buffer);break
                except json.JSONDecodeError:
                    part=f.read(65536);assert part and len(buffer)+len(part)<=MAX_RECORD_TEXT,'checkpoint_metadata_read_bound'
                    buffer+=part
            assert isinstance(record,dict);yield ordinal,record
            buffer=buffer[end:]
            if not buffer:buffer=f.read(65536)
            delimiter=',' if ordinal<count-1 else ']'
            assert buffer.startswith(delimiter),(ordinal,delimiter)
            buffer=buffer[1:]
        tail=buffer+f.read(MAX_TAIL_TEXT+1);assert len(tail)<=MAX_TAIL_TEXT and f.read(1)=='','ERROR_tail_read_bound'
        assert tail.startswith(',');state['tail']=json.loads('{'+tail[1:],object_pairs_hook=unique_object)
        assert set(state['tail'])=={'closing_traceback','context','controls','input_sha256','owner','qualification','raw_preservation_traceback','status','traceback'}

def inventory(kind):
    roles=['INPUT']+['CACHE_COLUMN']*4;names=[]
    if kind=='configuration':roles+=['SHEET_CACHE','PREPARATION']
    for direction in range(2):
        if kind=='mechanical':
            label='direction%d_NEW_mechanical_rate'%direction
            roles+=['DIRECTION']+(['MATCHING_ACTION']+['NORMAL_TEST']*16+['COLUMN'])*4+['READOUT']
            names += [label+'_column%d_'%iq+n+'_160_vs147' for iq in range(4) for n in ('native','metric_native','metric_EH','metric_total')]+[label+'_'+n+'_polynomial_transpose' for n in ('native','metric')]+[label+'_normal_CMC_'+n+'_polynomial_transpose' for n in ('normal','CMC')]
        else:
            label='direction%d_NEW_whole_configuration'%direction
            roles+=['DIRECTION']+(['NORMAL_TEST']*16+['COLUMN'])*4+['FULL_WEAK']
            names += [label+'_column%d_York_actual_trace_JVP'%iq for iq in range(4)]+[label+'_'+n+'_polynomial_transpose' for n in ('native','metric','phase','York_target')]+[label+'_normal_CMC_'+n+'_polynomial_transpose' for n in ('normal','CMC')]+[label+'_fixed_label_sheet_polynomial_transpose']
    return roles+['ERROR_RAW'],names

def source_constants(path):
    constants={}
    for n in ast.parse(path.read_text()).body:
        if not isinstance(n,ast.Assign) or len(n.targets)!=1 or not isinstance(n.targets[0],ast.Name):continue
        name=n.targets[0].id
        if name=='FLAGS':
            assert isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='dict' and not n.value.args
            assert all(k.arg is not None for k in n.value.keywords)
            constants[name]=unique_object([(k.arg,ast.literal_eval(k.value)) for k in n.value.keywords])
        else:
            try:constants[name]=ast.literal_eval(n.value)
            except (ValueError,TypeError):pass
    return constants

def verify_record(ref,ordinal,role,owner,rc,spec):
    assert ref['file']==spec['stem']+'_%05d_%s.npz'%(ordinal,role) and ref['commit_file']==ref['file']+'.COMMIT.json'
    for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):assert rc['output_sha256'][n]==h
    ap=verified(ref['file'],ref['sha256']);cp=verified(ref['commit_file'],ref['commit_sha256'])
    assert not ap.stat().st_mode&0o222 and not cp.stat().st_mode&0o222
    commit=small_json(cp);assert set(commit)=={'file','sha256','metadata'} and commit=={k:ref[k] for k in ('file','sha256','metadata')}
    md=ref['metadata'];failed=ordinal==spec['success']
    assert md['owner']==owner and md['qualification']==FLAGS and md['failed'] is failed
    if failed:assert role=='ERROR_RAW' and md['kind']==spec['raw_kind'] and md['schema']=={}
    else:assert md['role']==role and md['physical_adoption'] is False and md['schema']
    before=ap.stat();versions={}
    with zipfile.ZipFile(ap) as z:
        names=z.namelist();assert len(names)==len(set(names)) and set(names)=={n+'.npy' for n in md['schema']}|{'metadata_json.npy'}
        for name,schema in md['schema'].items():
            info=z.getinfo(name+'.npy')
            with z.open(info) as f:(shape,order,dtype),version,position=header(f)
            assert list(shape)==schema['shape'] and str(dtype)==schema['dtype'] and schema['finite'] is True and not dtype.hasobject
            assert position+math.prod(shape)*dtype.itemsize==info.file_size,name
            versions[str(version)]=versions.get(str(version),0)+1
        with z.open('metadata_json.npy') as f:
            (shape,order,dtype),version,position=header(f);assert shape==() and dtype.kind=='U' and dtype.itemsize<=4*MAX_RECORD_TEXT
            payload=f.read();assert len(payload)==dtype.itemsize
            big=dtype.byteorder=='>' or dtype.byteorder=='=' and sys.byteorder=='big'
            text=payload.decode('utf-32-be' if big else 'utf-32-le').rstrip('\x00')
            assert json.loads(text,object_pairs_hook=unique_object)==md
    after=ap.stat();assert (before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns)
    return dict(ordinal=ordinal,role=role,**thin(ref),member_headers=len(md['schema']),public_header_versions=versions,failed=failed,owner_equal=True,embedded_metadata_equal=True,member_names_headers_and_structural_lengths_equal=True,qualification_all_false=True)

def verify_links(ref,ordinal,role,state,spec,names):
    md=ref['metadata'];tr=thin(ref)
    if ordinal==0:state.update(header=tr,header_metadata=md,caches=[],readouts=[],readout_controls=[],columns=[],tests=[],actions=[]);assert md['expected_control_names']==names;return
    if role=='CACHE_COLUMN':assert md['column']==ordinal-1 and md['input']==state['header'];state['caches'].append(tr);return
    if role in ('SHEET_CACHE','PREPARATION'):
        assert md['input']==state['header'];state[role]=tr
        if role=='PREPARATION':assert md['cached_columns']==state['caches'] and md['sheet_cache']==state['SHEET_CACHE'] and md['original_current_prior_epsilon_words_unchanged'] is True
        return
    if role=='ERROR_RAW':state['failed_metadata']=md;return
    initial,stride,width=(5,74,18) if KIND=='mechanical' else (7,70,17)
    direction=(ordinal-initial)//stride;start=initial+direction*stride;assert direction in (0,1) and md['direction']==direction and md['input']==state['header']
    if role=='DIRECTION':
        assert ordinal==start and md['entries']==state['header_metadata']['directions'][direction]
        if KIND=='configuration':assert md['preparation']==state['PREPARATION']
        state.update(direction=tr,columns=[],tests=[],actions=[],last_tests=[]);return
    if role==spec['readout_role']:
        controls=names[direction*(spec['controls']//2):(direction+1)*(spec['controls']//2)]
        assert ordinal==spec['readouts'][direction] and md['direction_record']==state['direction'] and md['columns']==state['columns'] and md['normal_tests']==state['tests']
        assert [q['name'] for q in md['controls']]==controls
        if KIND=='mechanical':assert md['matching_actions']==state['actions'] and md['full_inverse_or_finite_state_or_physical_admission'] is False
        else:assert md['reduced_stage_complete'] is False and md['original_six_canonical_restoration_not_evaluated'] is True
        state['readouts'].append(tr);state['readout_controls'].extend(md['controls']);return
    iq=(ordinal-start-1)//width;offset=(ordinal-start-1)%width
    assert iq in range(4) and md['column']==iq
    if role=='MATCHING_ACTION':
        assert offset==0 and md['direction_record']==state['direction'] and md['cache']==state['caches'][iq]
        state['actions'].append(tr);state['action']=tr;state['last_tests']=[];return
    if role=='NORMAL_TEST':
        slot=offset-1 if KIND=='mechanical' else offset
        assert (md['row'],md['jet'])==divmod(slot,4) and md['direction_record']==state['direction'] and md['cache']==state['caches'][iq]
        if KIND=='mechanical':assert md['matching_action']==state['action']
        if slot==0:state['last_tests']=[]
        state['tests'].append(tr);state['last_tests'].append(tr);return
    assert role=='COLUMN' and offset==width-1 and md['normal_tests']==state['last_tests'] and len(state['last_tests'])==16
    if KIND=='mechanical':assert md['matching_action']==state['action'] and [q['name'] for q in md['controls']]==names[20*direction+4*iq:20*direction+4*iq+4]
    else:assert md['direction_record']==state['direction'] and md['cache']==state['caches'][iq] and md['reduced_stage_complete'] is False
    state['columns'].append(tr)

def main():
    global np
    assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and KIND in SPECS,'Root FULL-reviewed guarded release required'
    spec=SPECS[KIND];assert SOURCE==spec['source'] and ERROR[0]==spec['stem']+'_ERROR.json' and RECEIPT[0]==spec['stem']+'_RECEIPT.json'
    assert all(v is not None for q in (SOURCE,ERROR,RECEIPT) for v in q) and isinstance(PROOF_FILE,str) and re.fullmatch(r'[A-Z0-9_]+\.json',PROOF_FILE)
    assert isinstance(NATURAL_CLOSURE,dict) and NATURAL_CLOSURE['pid']==spec['pid'] and NATURAL_CLOSURE['session_id']==spec['session']
    assert NATURAL_CLOSURE['naturally_closed'] is NATURAL_CLOSURE['process_absent'] is True and NATURAL_CLOSURE['exit_code']==1 and isinstance(NATURAL_CLOSURE['observed_utc'],str)
    proof_path=BASE/PROOF_FILE;assert not proof_path.exists()
    assert not (BASE/(spec['stem']+'_RESULT.json')).exists() and not (BASE/(spec['stem']+'_ERROR_RECEIPT.json')).exists()
    verified(PROTOCOL,PROTOCOL_SHA);source=verified(*SOURCE);ep=verified(*ERROR);rp=verified(*RECEIPT);constants=source_constants(source)
    assert constants['STEM']==spec['stem'] and constants['FLAGS']==FLAGS and constants['AUTHOR_DRAFT'] is constants['AUTHORING_IN_PROGRESS'] is False
    rc=small_json(rp);owner=rc['owner'];assert owner['owner']=='root' and owner['pid']==spec['pid'] and owner['source_sha256']==SOURCE[1]
    assert rc['status']=='CLOSED_ERROR' and rc['error_sha256']==ERROR[1] and rc['prior_receipt_sha256'] is None and rc['qualification']==FLAGS
    assert len(rc['input_sha256'])==spec['inputs'] and len(rc['output_sha256'])==spec['outputs']
    assert rc['input_sha256'][str(source.resolve())]==SOURCE[1]
    for n,h in constants['PINS'].items():assert rc['input_sha256'][str((BASE/n).resolve())]==h
    for name,digest in ((constants['IO_PARENT'],constants['IO_PARENT_SHA']),(constants['DRIVER_PROTOCOL'],constants['PROTOCOL_SHA'])):assert rc['input_sha256'][str((BASE/name).resolve())]==digest
    # A full success proof is impossible while even one original selected input or output remains mismatched/unread.
    for side in ('input_sha256','output_sha256'):
        for name,digest in rc[side].items():verified(name,digest)
    assert small_json(BASE/(spec['stem']+'_OWNER_START.json'))==owner
    manifest=small_json(BASE/(spec['stem']+'_MANIFEST.json'));roles,names=inventory(KIND)
    assert len(roles)==spec['success']+1 and len(names)==len(set(names))==spec['controls']
    assert manifest['owner']==owner and manifest['qualification']==FLAGS and manifest['expected_control_names']==names
    for n,h in manifest['input_sha256'].items():assert rc['input_sha256'][n]==h
    import numpy as numpy
    np=numpy
    state={};records=[];stream={}
    for ordinal,ref in checkpoint_stream(ep,stream,len(roles)):
        records.append(verify_record(ref,ordinal,roles[ordinal],owner,rc,spec));verify_links(ref,ordinal,roles[ordinal],state,spec,names)
    error=stream['tail'];assert error['status']=='FAILED' and error['owner']==owner and error['qualification']==FLAGS and error['input_sha256']==rc['input_sha256']
    assert error['raw_preservation_traceback'] is None and state['failed_metadata']['context']==error['context']
    assert error['context']['last_completed_role']==state['readouts'][-1] and state['failed_metadata']['schema']=={}
    assert hashlib.sha256(error['traceback'].encode()).hexdigest()==spec['traceback_sha256'] and hashlib.sha256(error['closing_traceback'].encode()).hexdigest()==spec['closing_traceback_sha256']
    controls=error['controls'];assert [q['name'] for q in controls]==names and [q['ordinal'] for q in controls]==list(range(spec['controls'])) and state['readout_controls']==controls
    assert all(q['passed'] is True and q['tolerance']==2e-11 and math.isfinite(q['error']) and 0<=q['error']<=2e-11 for q in controls)
    assert state['header_metadata']['directions']==manifest['directions']
    expected={spec['stem']+'_'+n+'.json' for n in ('OWNER_START','MANIFEST','ERROR')}|{q[k] for q in records for k in ('file','commit_file')}
    assert set(rc['output_sha256'])==expected
    for name,before in STATS.items():
        s=Path(name).stat();assert before==dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=oct(s.st_mode&0o777)),name
    proof=dict(status=STATUS,kind=KIND,verified_at=datetime.now(timezone.utc).isoformat(),owner=owner,source_file=SOURCE[0],source_sha256=SOURCE[1],error_file=ERROR[0],error_sha256=ERROR[1],receipt_file=RECEIPT[0],receipt_sha256=RECEIPT[1],naturally_closed=True,exit_code=1,observed_closure=NATURAL_CLOSURE,all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,all_partial_error_seals_verified=True,completed_scientific_roles=spec['success'],earned_controls=spec['controls'],error_raw_roles=1,original_controls_passed=True,input_count=spec['inputs'],output_count=spec['outputs'],records=records,controls=controls,readouts=state['readouts'],input=state['header'],cached_columns=state['caches'],original_failure_preserved=True,original_RESULT_absent=True,traceback=error['traceback'],closing_traceback=error['closing_traceback'],raw_preservation_traceback=None,qualification=FLAGS,numeric_arrays_decoded=False,scientific_actions_or_controls_replayed=False,original_publication_input_failure=True,distinct_closing_failure_preserved=True,physical_or_NEW139_admission=False,fresh_verified_bytes=TOTAL_BYTES,verified_sha256=VERIFIED,stable_stats=STATS,scope='Full original saved byte/public-header/embedded-metadata/owner/control custody only. Finite=True is inherited from authenticated producer schema; no numeric finiteness or control recomputation. Original FAILED/CLOSED_ERROR and any closing output failure remain unchanged.')
    data=(json.dumps(proof,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with proof_path.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    proof_path.chmod(0o444);print(json.dumps(dict(file=proof_path.name,sha256=hashlib.sha256(data).hexdigest(),success_roles=spec['success'],controls=spec['controls'])))

if __name__=='__main__':main()
