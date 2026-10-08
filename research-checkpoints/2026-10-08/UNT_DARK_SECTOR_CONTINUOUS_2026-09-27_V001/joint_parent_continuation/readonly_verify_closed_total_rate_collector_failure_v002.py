"""HELD65759 natural-failure byte/public-header verifier, root release only.
No numeric-array decoding, scientific replay or original artifact mutation.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, math, re, sys, zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
SOURCE='cross_u_fixed_geometry_total_rate_state_evaluation_v004.py'
SOURCE_SHA='59f23b9476d38aadc8297c104d4cf8e5ab217ac1ce3a0bc077e34f2fec99b39f'
STEM='CROSS_U_FIXED_GEOMETRY_TOTAL_RATE_STATE_EVALUATION_V004'
ERROR_SHA='183070c4620623ee5f82f93f8c65de2a73815c0c60bcaeead64ea6fcecb09fea'
RECEIPT_SHA='fa2972d289c42d29be375c1d42e3533ec0d40ddd67724adebf0a1e3d4928487d'
NATURAL_CLOSURE={'pid': 65759, 'session_id': 37471, 'naturally_closed': True, 'exit_code': 1, 'observed_utc': '2026-10-08T05:42:00+00:00'}
PROOF=BASE/'READONLY_NATURAL_CLOSED_TOTAL_RATE_COLLECTOR_FAILURE_SEALS_V001.json'
FLAGS=dict(physical_adoption=False,uniform_DD_or_global_inverse_qualified=False,fresh_current_six_or_normal_CMC_admitted=False,changed_spatial_geometry=False,stationarity_feedback_or_new43_earned=False)
np=None
VERIFIED={};STATS={};TOTAL_BYTES=0;ERROR_CONTEXT=None
TRACEBACK_SHA='238de507d083034f0e2cf5a3586df7407b1befa6407cd5ae3574258775703643'
RAW_SCHEMA={'NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_full_metric_current_hi': [6, 87, 45], 'NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_full_metric_current_lo': [6, 87, 45], 'NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_full_native_current_hi': [33, 3, 87, 45], 'NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_full_native_current_lo': [33, 3, 87, 45], 'last_DD_e': [6, 45], 'last_DD_s': [6, 45], 'metric_scatter_current_restricted_hi': [6, 87, 45], 'metric_scatter_current_restricted_lo': [6, 87, 45], 'native_scatter_current_restricted_hi': [33, 3, 87, 45], 'native_scatter_current_restricted_lo': [33, 3, 87, 45], 'scatter_current_partial_hi': [6, 87, 45], 'scatter_current_partial_lo': [6, 87, 45]}

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

def required_pair(md, name, shape):
    for word in ('hi', 'lo'):
        s = md['schema'][name + '_' + word]
        assert s['shape'] == list(shape) and s['dtype'] == 'float64' and s['finite'] is True, name

def current_schema(md, role):
    prefix = 'completed_' + role + '_'; pairs = {}
    if role == 'INPUT': pairs = dict(native=(33, 3, 87, 45), metric=(6, 87, 45), sheet=(4, 87, 45))
    if role == 'RATE_INCREMENT': pairs = dict(native_nodes=(33, 3, 87, 45), metric_nodes=(6, 87, 45), native=(33, 15136, 3), metric=(15136, 6))
    if role == 'BASELINE_COLUMN_INPUT':
        pairs = dict(covectors_u_jets=(3784, 4, 3), covectors_z_jets=(32, 3784, 4, 3), mechanical_h_dot=(3784, 3, 3),
                     gauge_N_jets=(3784, 4), gauge_beta_jets=(3784, 4, 3), reference_E0=(3784, 4, 4, 4), h_first=(3784, 4, 3, 3),
                     Lie_beta_h=(3784, 3, 3), updated_phase_covector=(3784, 4), intrinsic_curvature_Q=(3784,), intrinsic_curvature_V=(3784, 3),
                     fixed_terms_phase_action=(3784, 4, 4), fixed_terms_ordinary_Hamiltonian=(3784, 4, 4))
    if role == 'RATE_STATE_INPUT': pairs = dict(h_first=(3784, 4, 3, 3), u_jets=(3784, 4, 3), z_jets=(32, 3784, 4, 3), N_jets=(3784, 4), beta_jets=(3784, 4, 3), E0=(3784, 4, 4, 4), updated_phase=(3784, 4))
    if role == 'RATE_STATE_FIRST_JETS': pairs = dict(first_inverse_first=(3784, 4, 3, 3), first_up_first=(3784, 4, 3), first_gamma_first=(3784, 4), owned_covectors_u_jets=(3784, 4, 3), owned_covectors_z_jets=(32, 3784, 4, 3), fixed_E0=(3784, 4, 4, 4))
    if role == 'RATE_STATE_MOMENTA': pairs = dict(momenta_native_density=(3784, 99), momenta_metric_total_density=(3784, 6))
    if role == 'RATE_STATE_NORMAL_TEST': pairs = dict(total_action=(3784,), total_Hamiltonian=(3784,), initial_CMC_density=(3784,))
    if role == 'RATE_STATE_COLUMN':
        pairs = dict(value_normal_coefficients=(3784, 4, 4), value_initial_CMC_density=(3784,), delta_normal_coefficients=(3784, 4, 4), delta_initial_CMC_density=(3784,),
                     native_EH_coefficients=(3784, 4, 4), new_point_current_native_density=(3784, 99), new_point_current_metric_total_density=(3784, 6),
                     new_TOTAL_time_words_u_jets=(3784, 4, 3), new_TOTAL_time_words_z_jets=(32, 3784, 4, 3), new_TOTAL_time_words_h_dot=(3784, 3, 3))
    if role == 'READOUT': pairs = dict(current_native=(33, 3, 87, 45), current_metric=(6, 87, 45), weak_normal=(4, 87, 45), weak_initial_CMC=(87, 45), unchanged_sheet_weak_normal=(4, 87, 45), normal_CMC_value_time_primary_action_coefficients=(15136, 4))
    for name, shape in pairs.items(): required_pair(md, prefix + name, shape)

def verify_record(ref, ordinal, role, owner, rc, failed=False):
    match = re.fullmatch(re.escape(STEM) + r'_(\d{5})_(.+)\.npz', ref['file'])
    assert match and int(match[1]) == ordinal and match[2] == role
    assert ref['commit_file'] == ref['file'] + '.COMMIT.json'
    for n, h in ((ref['file'], ref['sha256']), (ref['commit_file'], ref['commit_sha256'])): assert rc['output_sha256'][n] == h
    ap = verified(ref['file'], ref['sha256']); cp = verified(ref['commit_file'], ref['commit_sha256'])
    assert not ap.stat().st_mode & 0o222 and not cp.stat().st_mode & 0o222
    commit = json.loads(cp.read_bytes())
    assert set(commit) == {'file', 'sha256', 'metadata'} and commit['file'] == ref['file'] and commit['sha256'] == ref['sha256']
    md = commit['metadata']; assert md == ref['metadata'] and md['owner'] == owner and md['qualification'] == FLAGS and md['failed'] is failed
    if failed:
        assert md['kind']=='incomplete_TOTAL_rate_value_state' and md['context']==ERROR_CONTEXT and len(md['schema'])==12
        for name,shape in RAW_SCHEMA.items():
            assert md['schema'][name]==dict(shape=shape,dtype='float64',finite=True),name
    else:
        assert md['kind'] == role and md['physical_adoption'] is False; current_schema(md, role)
    before = ap.stat(); versions = {}
    with zipfile.ZipFile(ap) as z:
        names = z.namelist(); assert len(names) == len(set(names)) and set(names) == {n + '.npy' for n in md['schema']} | {'metadata_json.npy'}
        for name, schema in md['schema'].items():
            info = z.getinfo(name + '.npy')
            with z.open(info) as f: (shape, order, dtype), version, position = header(f)
            assert list(shape) == schema['shape'] and str(dtype) == schema['dtype'] and schema['finite'] is True and not dtype.hasobject
            assert position + math.prod(shape) * dtype.itemsize == info.file_size, name
            versions[str(version)] = versions.get(str(version), 0) + 1
        with z.open('metadata_json.npy') as f:
            (shape, order, dtype), version, position = header(f); assert shape == () and dtype.kind == 'U'
            payload = f.read(); assert len(payload) == dtype.itemsize
            big=dtype.byteorder=='>' or dtype.byteorder=='=' and sys.byteorder=='big'
            text = payload.decode('utf-32-be' if big else 'utf-32-le').rstrip('\x00')
            assert json.loads(text) == md
    after = ap.stat(); assert (before.st_ino, before.st_size, before.st_mtime_ns) == (after.st_ino, after.st_size, after.st_mtime_ns)
    return dict(ordinal=ordinal, role=role, **thin(ref), member_headers=len(md['schema']), public_header_versions=versions,
                owner_equal=True, embedded_metadata_equal=True, member_names_headers_and_structural_lengths_equal=True, failed=failed, qualification_all_false=True)

def main():
    global np,ERROR_CONTEXT
    assert not AUTHOR_DRAFT and isinstance(NATURAL_CLOSURE,dict),'Root FULL-reviewed guard-only release required'
    assert NATURAL_CLOSURE['pid']==65759 and NATURAL_CLOSURE['session_id']==37471 and NATURAL_CLOSURE['naturally_closed'] is True
    assert NATURAL_CLOSURE['exit_code']==1 and isinstance(NATURAL_CLOSURE['observed_utc'],str)
    assert not PROOF.exists() and not (BASE/(STEM+'_RESULT.json')).exists() and not (BASE/(STEM+'_ERROR_RECEIPT.json')).exists()
    import numpy as numpy
    np=numpy
    source=verified(SOURCE,SOURCE_SHA);constants={}
    for n in ast.parse(source.read_text()).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:constants[n.targets[0].id]=ast.literal_eval(n.value)
            except (ValueError,TypeError):pass
    assert constants['STEM']==STEM and constants['FLAGS']==FLAGS and constants['AUTHOR_DRAFT'] is constants['AUTHORING_IN_PROGRESS'] is False
    error=json.loads(verified(STEM+'_ERROR.json',ERROR_SHA).read_bytes());rc=json.loads(verified(STEM+'_RECEIPT.json',RECEIPT_SHA).read_bytes())
    owner=error['owner'];assert owner==rc['owner'] and owner['owner']=='root' and owner['pid']==65759 and owner['source_sha256']==SOURCE_SHA
    assert error['status']=='FAILED' and rc['status']=='CLOSED_ERROR' and rc['error_sha256']==ERROR_SHA and rc['prior_receipt_sha256'] is None
    assert error['qualification']==rc['qualification']==FLAGS and all(v is False for v in FLAGS.values())
    assert error['raw_preservation_traceback'] is error['closing_traceback'] is None and error['controls']==[]
    assert hashlib.sha256(error['traceback'].encode()).hexdigest()==TRACEBACK_SHA
    assert 'finite_candidate_test_polynomials' in error['traceback'] and 'line 196' in error['traceback'] and 'normal_test[~N.normal_test_mask()]' in error['traceback']
    assert error['input_sha256']==rc['input_sha256'] and len(rc['input_sha256'])==77
    assert rc['input_sha256'][str(source.resolve())]==SOURCE_SHA
    for name,digest in constants['PINS'].items():assert rc['input_sha256'][str((BASE/name).resolve())]==digest
    assert rc['input_sha256'][str((BASE/constants['IO_PARENT']).resolve())]==constants['IO_PARENT_SHA']
    assert rc['input_sha256'][str((BASE/constants['DRIVER_PROTOCOL']).resolve())]==constants['PROTOCOL_SHA']
    roles=['INPUT','RATE_INCREMENT']+(['BASELINE_COLUMN_INPUT','RATE_STATE_INPUT','RATE_STATE_FIRST_JETS','RATE_STATE_FEATURES','RATE_STATE_MOMENTA']+['RATE_STATE_NORMAL_TEST']*16+['RATE_STATE_COLUMN'])*4+['ERROR_RAW']
    refs=error['checkpoints'];assert len(refs)==len(roles)==91 and len(rc['output_sha256'])==185
    expected={STEM+'_'+n+'.json' for n in ('OWNER_START','MANIFEST','ERROR')}|{q[k] for q in refs for k in ('file','commit_file')}
    assert set(rc['output_sha256'])==expected
    for side in ('input_sha256','output_sha256'):
        for name,digest in rc[side].items():verified(name,digest)
    assert json.loads((BASE/(STEM+'_OWNER_START.json')).read_bytes())==owner
    manifest=json.loads((BASE/(STEM+'_MANIFEST.json')).read_bytes());assert manifest['owner']==owner and manifest['original_TOTAL_words'] is True and manifest['source_only_old_producer_replay'] is manifest['physical_adoption'] is False
    canonicalize=lambda x:json.loads(json.dumps(x));assert manifest['selected22_proof']==canonicalize(constants['SELECTED22_PROOF'])
    plan=json.loads(verified(constants['PLAN_FILE'],constants['PLAN_SHA']).read_bytes());assert plan['source_only'] is True and len(plan['columns'])==4
    sb=constants['SELECTED22_PROOF'];selected=json.loads(verified(sb[0],sb[1]).read_bytes())
    assert selected['status']==sb[2] and selected['selected_refs']==plan['retrieval']['mandatory_payload_refs'] and len(selected['selected_refs'])==22
    assert selected['all_selected_archive_bytes_verified'] is selected['all_selected_COMMIT_bytes_verified'] is selected['all_selected_owners_naturally_closed'] is True
    for field,name in (('baseline_proof','BASELINE_CLOSURE'),('finite_phase_proof','UPDATED_PHASE_CLOSURE'),('join_proof','JOIN_CLOSURE')):assert selected[field]==canonicalize(constants[name][3])
    ERROR_CONTEXT=error['context'];records=[verify_record(q,i,roles[i],owner,rc,i==90) for i,q in enumerate(refs)]
    provenance=refs[0]['metadata']['provenance'];assert provenance['all_source_seals_authenticated'] is provenance['correction_original_six_gates_admitted'] is provenance['original_fixed_references_verified'] is provenance['unchanged_sheet_value_identity_verified'] is True
    assert provenance['physical_adoption'] is False and len(provenance['columns'])==len(provenance['original_owned_TOTAL_time_words'])==4
    assert provenance['unchanged_sheet_weak_normal']==plan['unchanged_sheet']['ref'] and provenance['unchanged_original_targets']==plan['closed_metadata']['original_canonical_target_refs']
    assert refs[0]['metadata']['selected22_proof']==canonicalize(constants['SELECTED22_PROOF'])
    helper=ast.parse(verified('author_fragment_fixed_geometry_total_rate_state_v002.py',constants['PINS']['author_fragment_fixed_geometry_total_rate_state_v002.py']).read_text())
    hp=next(ast.literal_eval(n.value) for n in helper.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIXED_RATE_STATE_SOURCE_PINS' for t in n.targets));assert provenance['source_pins']==hp
    for name in ('BASELINE_CLOSURE','CORRECTION_CLOSURE','UPDATED_PHASE_CLOSURE','FIXED_BINDING'):assert provenance[name.lower()]==canonicalize(constants[name])
    for iq,spec in enumerate(plan['columns']):
        first=2+22*iq;baseline=refs[first]['metadata'];pr=provenance['columns'][iq]
        assert baseline['column']==iq and baseline['state']==thin(spec['state']['ref'])==provenance['original_owned_TOTAL_time_words'][iq]
        assert baseline['phase_rows']==[thin(q['ref']) for q in spec['phase_rows']] and pr==dict(column=iq,state=baseline['state'],phase_rows=baseline['phase_rows'])
        assert baseline['raw225_Lie_authoritative_contact_Lie_retained'] is baseline['owned_TOTAL_time_words_copied_not_reconstructed'] is True
        for offset in range(1,22):
            md=refs[first+offset]['metadata'];assert md['column']==iq and md['provenance']==pr
            if 5<=offset<=20:assert (md['row'],md['jet'])==divmod(offset-5,4)
    for name,before in STATS.items():
        s=Path(name).stat();assert before==dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,mode=oct(s.st_mode&0o777)),name
    columns=[thin(refs[23+22*iq]) for iq in range(4)]
    proof=dict(status='READONLY_NATURAL_CLOSED_TOTAL_RATE_COLLECTOR_FAILURE_SEALS_VERIFIED',verified_at=datetime.now(timezone.utc).isoformat(),owner=owner,source_file=SOURCE,source_sha256=SOURCE_SHA,error_file=STEM+'_ERROR.json',error_sha256=ERROR_SHA,receipt_file=STEM+'_RECEIPT.json',receipt_sha256=RECEIPT_SHA,naturally_closed=True,exit_code=1,observed_closure=NATURAL_CLOSURE,all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,all_failed_raw_seals_verified=True,input_count=77,output_count=185,success_roles=90,failed_raw_roles=1,original_controls_passed=0,controls=[],collector_controls_earned=False,columns=columns,input=thin(refs[0]),error_raw=thin(refs[90]),records=records,qualification=FLAGS,original_failure_preserved=True,readout_or_original_six_or_physical_admission=False,numeric_arrays_decoded=False,scientific_actions_or_controls_replayed=False,cause='Original diagnostic beta_Z sheet support violated normal_test_mask before collector polynomial/controls; completed columns and currents retained',source_traceback_sha256=TRACEBACK_SHA,scope='Full saved byte/public-header/embedded-metadata/owner/provenance custody only; numeric finite assertions inherited from authenticated worker schemas',fresh_verified_bytes=TOTAL_BYTES,verified_sha256=VERIFIED,stable_stats=STATS)
    data=(json.dumps(proof,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    with PROOF.open('xb') as f:f.write(data)
    PROOF.chmod(0o444);print(json.dumps(dict(file=PROOF.name,sha256=hashlib.sha256(data).hexdigest(),roles=91,success_roles=90,controls=0)))

if __name__=='__main__':main()
