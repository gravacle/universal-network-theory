"""HELD closed-baseline43 general diagnostic byte/header custody only.
ROOT binds observed natural closure and terminal bytes; no numeric array decoding.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,re,sys,zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
SOURCE=(None,None)
EXPECTED_SOURCE=('baseline_DIRECT43_general_raw_jet_diagnostic_v003.py','fae2f715dd379f3ff9e38e61785ebc8d23620c5a51fd214920486475450bc29b')
RESULT=(None,None,'BASELINE_DIRECT43_GENERAL_INSTANTANEOUS_RADIAL_DIAGNOSTICS_MEASURED')
RECEIPT=(None,None,'CLOSED')
NATURAL_CLOSURE=None
EXPECTED_EXECUTION=(17716,9746,'exec-b8c92cd3-cc41-4e74-b3c3-294dac038757')
PROOF_FILE=None
PROTOCOL='READONLY_CLOSED_BASELINE_DIRECT43_GENERAL_DIAGNOSTIC_SEALS_V001.md'
PROTOCOL_SHA=None
CUSTODY_PARENT=('readonly_verify_closed_DIRECT43_baseline_v003.py','492cf191e619e9fa706d41c8d6db995fb852c1669028c965effe8366c25589c1')
STEM='BASELINE_DIRECT43_GENERAL_RAW_JET_DIAGNOSTIC_V002'
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

def canonical(value):return json.loads(json.dumps(value))

def bounded_json(path,limit=16*1024*1024):
    assert 0<path.stat().st_size<=limit,path.name
    return json.loads(path.read_bytes())

def archive_record(ref,ordinal,role,owner,receipt):
    failure=False
    assert ref['file']==STEM+'_%05d_%s.npz'%(ordinal,role) and ref['commit_file']==ref['file']+'.COMMIT.json'
    for name,digest in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):assert receipt['output_sha256'][name]==digest
    ap=verified(ref['file'],ref['sha256']);cp=verified(ref['commit_file'],ref['commit_sha256']);assert not ap.stat().st_mode&0o222 and not cp.stat().st_mode&0o222
    commit=bounded_json(cp);assert set(commit)=={'file','sha256','metadata'} and commit=={k:ref[k] for k in ('file','sha256','metadata')}
    md=ref['metadata'];assert md['owner']==owner and md['qualification']==FLAGS and md['failed'] is failure
    assert isinstance(md['schema'],dict) and all(isinstance(n,str) and n for n in md['schema'])
    if not failure:assert md['physical_adoption'] is False and all(field['finite'] is True for field in md['schema'].values())
    def slot(name,shape,dtype='float64'):assert md['schema'][name]==dict(shape=list(shape),dtype=dtype,finite=True)
    assert md['role']==role and md['baseline_only'] is True and isinstance(md['completed_payload'],dict)
    if role.endswith('_RAW_PAIR'):
        for name,shape in (('g',(4,4)),('dg',(4,4,4))):
            for word in (0,1):slot('completed_'+name+'_'+str(word)+'_',shape)
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


def event_contract(event,index,refs,offset,owner,receipt,ancestor):
    assert event['index']==index and type(event['index']) is int and event['R']==ancestor['events'][index]['R'] and type(event['R']) is float and math.isfinite(event['R']) and event['R']>0
    assert event['physical_adoption'] is False
    raw=event['raw_pair_stages'];assert set(raw)=={'input','time','raw_pair','output'}
    seq=[(raw[n],'EVENT_%02d_RAW_'%index+r) for n,r in (('input','INPUT'),('time','TIME'),('raw_pair','RAW_PAIR'),('output','OUTPUT'))]
    ins=event['interval_stages'];suffixes=['INPUT','SAMPLING_CHI','SAMPLING_CORRECTION','SAMPLING_TOTAL','CONFORMAL','METRIC']+['FIRST_JET%d'%i for i in range(4)]+['PRIMITIVE_BOX']
    assert len(ins)==11;seq.extend((r,'EVENT_%02d_INTERVAL_'%index+s) for r,s in zip(ins,suffixes))
    ats=event['attachment_stages'];assert len(ats)==2;seq.extend((r,'EVENT_%02d_ATTACH_OUTPUT_'%index+n) for r,n in zip(ats,('g','dg')))
    readout=event['readout'];status=readout['status'];assert status in ('UNRESOLVED_METRIC_DOMAIN','UNRESOLVED_TIME_GRADIENT','UNRESOLVED_NORMAL_FRAME_ENDPOINTS','GENERAL_INSTANTANEOUS_RADIAL_BALANCE_INTERVALS')
    gs=['INPUT_INTERVAL_DOMAINS']
    if status=='UNRESOLVED_TIME_GRADIENT':gs+=['INVERSE_REFUSAL']
    elif status in ('UNRESOLVED_NORMAL_FRAME_ENDPOINTS','GENERAL_INSTANTANEOUS_RADIAL_BALANCE_INTERVALS'):
        gs+=['INVERSE_AND_CONNECTION','RADIAL_ROOT_INTERVALS']
        if status=='UNRESOLVED_NORMAL_FRAME_ENDPOINTS':gs+=['NORMAL_FRAME_REFUSAL']
        else:
            assert len(readout['candidates'])<=2;gs+=['ROOT_%d_DIAGNOSTICS'%i for i in range(len(readout['candidates']))]
    gs+=['READOUT'];gen=event['general_stages'];assert len(gen)==event['general_role_count']==len(gs) and type(event['general_role_count']) is int and 2<=len(gen)<=6
    assert readout['completed_stage_refs']==gen;seq.extend((r,'EVENT_%02d_GENERAL_'%index+s) for r,s in zip(gen,gs))
    byrole={};out=[]
    for i,(ref,role) in enumerate(seq,offset):
        actual=refs[i];assert thin(actual)==ref
        md=actual['metadata'];c=md['context'];assert c['index']==index and c['R']==event['R'] and c['radial_side']=='left' and c['vertical_side']=='upper' and c['stage']==role
        assert c['source_reference_event']==ancestor['events'][index]['reference_event'] and c['source_baseline_event']==ancestor['events'][index]['baseline_event']
        out.append(archive_record(actual,i,role,owner,receipt));byrole[role]=md['completed_payload']
    ri=byrole['EVENT_%02d_RAW_INPUT'%index];adm=ri['admission'];assert adm['baseline_terminal']==ancestor['baseline_terminal']
    assert adm['reference_record']==ancestor['events'][index]['reference_event'] and adm['baseline_record']==ancestor['events'][index]['baseline_event']
    assert adm['selected_metadata_and_words_authenticated'] is adm['same_geometry_baseline_not_new_coupled_trial'] is True
    ro=byrole['EVENT_%02d_RAW_OUTPUT'%index];assert event['source_association_gaps']==ro['source_association_gaps']
    box=byrole['EVENT_%02d_INTERVAL_PRIMITIVE_BOX'%index];ia=box['provenance'];assert box['completed']==ins[:-1]
    assert ia['input_scope']=='closed_direct_baseline_evidence' and ia['baseline_naturally_closed'] is True and ia['baseline_exit_code']==0
    assert ia['sampling_refs']=={n:adm[n] for n in ('reference_record','baseline_record')} and ia['terminals']=={n:ancestor['baseline_terminal'][n] for n in ('source','result','receipt','proof')}
    assert ia['same_geometry_baseline_not_new_coupled_trial'] is ia['all_original_word_hex_and_gauge_time_phi_retained'] is True
    assert ia['finite_constraint_solution_admitted'] is ia['physical_metric_admitted'] is False
    assert box['finite_input_exact_law_enclosure'] is True and box['finite_constraint_solution_admitted'] is box['physical_metric_admitted'] is box['circle_or_velocity_adopted'] is False
    ga=readout['supplied_admission'];assert ga['event_provenance']['ancestral_closed_baseline']==ancestor['baseline_terminal'] and ga['event_provenance']['same_owner_completed_raw_pair']==raw['raw_pair']
    assert ga['event_provenance']['source_records']==ia['sampling_refs'] and ga['interval_event_provenance']==readout['supplied_interval_provenance']==ia
    assert ga['interval_proof']==[ins[-1]['commit_file'],ins[-1]['commit_sha256'],'same_owner_completed_exact_primitive_box']
    assert ga['input_scope']=='closed_direct_baseline_evidence' and ga['coordinate_event']==[0.,event['R'],0.,0.] and ga['radial_side']=='left' and ga['vertical_side']=='upper'
    assert ga['naturally_closed'] is True and ga['exit_code']==0 and ga['all_selected_byte_owner_and_header_seals_verified'] is True and ga['physical_metric_admitted'] is False
    for n in ('source','result','receipt','proof'):assert ga[n]==ancestor['baseline_terminal'][n]
    for n in ('input_phi_or_time_words_changed','paired_words_collapsed_to_binary64','orientation_selected_using_observations','old_circle_or_metric_producers_replayed','exact_axisymmetry_guard_promoted','instantaneous_vertical_balance_or_full_circle_admitted','persistent_orbit_or_stability_claimed','physical_or_velocity_adoption'):assert readout[n] is False
    assert readout['declared_orientation']==1 and readout['finite_input_source_output_hull_only'] is True
    saved=byrole['EVENT_%02d_GENERAL_READOUT'%index];assert saved['completed_stage_refs']==gen[:-1]
    assert {n:v for n,v in saved.items() if n!='completed_stage_refs'}=={n:v for n,v in readout.items() if n!='completed_stage_refs'}
    first=byrole['EVENT_%02d_GENERAL_INPUT_INTERVAL_DOMAINS'%index]['bounds']
    assert first['source_box']['provenance']==ia and first['authentic_output_words']['completed_raw_pair']==raw['raw_pair']
    for n in ('g','dg'):assert first['authentic_output_words'][n]==byrole['EVENT_%02d_ATTACH_OUTPUT_'%index+n]['exact_output_words']
    return out,dict(index=index,R=event['R'],status=status,general_roles=len(gen),selected_index=readout['selected_index'],raw_phi_both_words_exact_zero=readout['raw_phi_both_words_exact_zero'],represented_phi_derivative_exact_zero=readout['represented_phi_derivative_exact_zero'],readout_ref=gen[-1],physical_adoption=False)


def main():
    global np
    assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and SOURCE==EXPECTED_SOURCE
    assert all(v is not None for pin in (SOURCE,RESULT,RECEIPT) for v in pin) and PROTOCOL_SHA is not None
    assert isinstance(PROOF_FILE,str) and re.fullmatch(r'[A-Z0-9_]+\.json',PROOF_FILE) and not (BASE/PROOF_FILE).exists()
    nc=NATURAL_CLOSURE;assert isinstance(nc,dict) and (nc['pid'],nc['session_id'],nc['app_command_execution_id'])==EXPECTED_EXECUTION
    assert nc['naturally_closed'] is nc['process_absent'] is True and type(nc['exit_code']) is int and nc['exit_code']==0 and isinstance(nc['observed_utc'],str) and nc['observed_utc']
    assert RESULT[0]==STEM+'_RESULT.json' and RECEIPT[0]==STEM+'_RECEIPT.json' and RECEIPT[2]=='CLOSED'
    assert not (BASE/(STEM+'_ERROR.json')).exists() and not (BASE/(STEM+'_ERROR_RECEIPT.json')).exists()
    verified(PROTOCOL,PROTOCOL_SHA);verified(*CUSTODY_PARENT);src=verified(*SOURCE);vp=verified(*RESULT[:2]);rp=verified(*RECEIPT[:2]);c=source_constants(src)
    assert c['AUTHOR_DRAFT'] is c['AUTHORING_IN_PROGRESS'] is False and c['STEM']==STEM and c['FLAGS']==FLAGS and len(c['PINS'])==16
    value=bounded_json(vp,64*1024*1024);rc=bounded_json(rp);owner=value['owner'];assert owner==rc['owner'] and owner['owner']=='root' and owner['pid']==nc['pid'] and owner['source_sha256']==SOURCE[1]
    assert value['status']==RESULT[2] and rc['status']=='CLOSED' and value['qualification']==rc['qualification']==FLAGS and value['controls']==[] and rc['result_sha256']==RESULT[1] and rc['error_sha256'] is None
    assert len(rc['input_sha256'])==194 and len(rc['output_sha256'])==1983
    for name,digest in rc['input_sha256'].items():verified(name,digest)
    for name,digest in rc['output_sha256'].items():verified(name,digest)
    required=[SOURCE,(c['IO_PARENT'],c['IO_PARENT_SHA']),(c['PROTOCOL'],c['PROTOCOL_SHA']),*c['PINS'].items(),*(c[n][:2] for n in ('SOURCE','RESULT','RECEIPT','PROOF'))]
    for name,digest in required:assert rc['input_sha256'][str((BASE/name).resolve())]==digest
    assert bounded_json(BASE/(STEM+'_OWNER_START.json'))==owner
    manifest=bounded_json(BASE/(STEM+'_MANIFEST.json'));assert manifest['owner']==owner and manifest['events']==43 and manifest['controls']==0 and manifest['qualification']==FLAGS
    assert manifest['roles']=='1+43*(4raw+11primitive+2attachment)+sum(general2to6)'
    for name,digest in manifest['input_sha256'].items():assert rc['input_sha256'][name]==digest
    refs=value['checkpoints'];case=value['case'];assert len(refs)==case['roles']==990 and len(case['events'])==43 and case['controls']==0 and case['status']==RESULT[2]
    assert case['baseline_only'] is True
    for n in ('new_coupled_or_corrected_finite_metric_evaluated','source_or_installed_rounding_accuracy_admitted','full_circle_or_galaxy_prediction_admitted','physical_adoption'):assert case[n] is False
    expected={STEM+'_'+n+'.json' for n in ('OWNER_START','MANIFEST','RESULT')}|{q[k] for q in refs for k in ('file','commit_file')};assert set(rc['output_sha256'])==expected
    import numpy as numpy
    np=numpy
    records=[archive_record(refs[0],0,'INPUT',owner,rc)];assert case['input']==thin(refs[0])
    ancestor=refs[0]['metadata']['completed_payload'];assert ancestor['orientation']==1 and ancestor['new_coupled_or_finite_closure_used'] is False and ancestor['interval_limits']==dict(bits=128,max_terms=256,max_squarings=16) and len(ancestor['events'])==43
    terminal=ancestor['baseline_terminal'];assert manifest['baseline_terminal']==terminal
    for n in ('source','result','receipt','proof'):assert terminal[n]==list(c[n.upper()])
    assert terminal['naturally_closed'] is True and terminal['exit_code']==0 and terminal['all_input_seals_verified'] is terminal['all_success_role_seals_verified'] is True
    ap=bounded_json(BASE/c['PROOF'][0]);assert ap['status']==c['PROOF'][2] and ap['owner']==terminal['owner'] and ap['source_sha256']==c['SOURCE'][1] and ap['result_sha256']==c['RESULT'][1] and ap['receipt_sha256']==c['RECEIPT'][1] and ap['science_role_count']==87
    assert ap['naturally_closed'] is True and ap['exit_code']==0 and ap['all_input_seals_verified'] is ap['all_output_seals_verified'] is ap['all_success_role_seals_verified'] is True
    offset=1;events=[]
    for index,event in enumerate(case['events']):
        new,summary=event_contract(event,index,refs,offset,owner,rc,ancestor);records.extend(new);offset+=len(new);events.append(summary)
    assert offset==len(refs)==990==1+43*17+sum(e['general_roles'] for e in events) and len(records)==990
    for name,before in STATS.items():
        st=Path(name).stat();assert before==dict(inode=st.st_ino,size=st.st_size,mtime_ns=st.st_mtime_ns,mode=oct(st.st_mode&0o777)),name
    proof=dict(status='READONLY_NATURAL_CLOSED_BASELINE_DIRECT43_GENERAL_DIAGNOSTIC_SEALS_VERIFIED',verified_at=datetime.now(timezone.utc).isoformat(),owner=owner,source_sha256=SOURCE[1],result_sha256=RESULT[1],receipt_sha256=RECEIPT[1],observed_closure=nc,naturally_closed=True,exit_code=0,all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,input_count=194,output_count=1983,role_count=990,event_count=43,control_count=0,controls=[],records=records,events=events,baseline_terminal=terminal,qualification=FLAGS,physical_adoption=False,corrected_or_physical43_admitted=False,numeric_arrays_decoded=False,source_or_readout_arithmetic_replayed=False,source_finite_word_and_interval_assertions_inherited=True,all_recorded_branch_refusals_retained=True,fresh_verified_bytes=TOTAL_BYTES,verified_sha256=VERIFIED,stable_stats=STATS)
    raw=(json.dumps(proof,indent=2,sort_keys=True,allow_nan=False)+'\n').encode();out=BASE/PROOF_FILE
    with out.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    out.chmod(0o444);print(json.dumps(dict(file=out.name,sha256=hashlib.sha256(raw).hexdigest(),roles=990,events=43,controls=0)))

if __name__=='__main__':main()
