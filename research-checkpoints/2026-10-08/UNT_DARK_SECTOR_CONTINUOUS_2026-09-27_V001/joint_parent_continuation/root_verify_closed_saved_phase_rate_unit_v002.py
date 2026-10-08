from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,zipfile
import numpy as np
BASE=Path(__file__).resolve().parent
VERIFIED={};TOTAL_BYTES=0

def verified(path, digest):
    global TOTAL_BYTES
    path = Path(path)
    if not path.is_absolute(): path = BASE / path
    key = str(path)
    if key in VERIFIED:
        assert VERIFIED[key] == digest
        return path
    before = path.stat()
    assert before.st_size > 0, key
    h = hashlib.sha256()
    with path.open('rb') as f:
        while block := f.read(4 * 1024 * 1024): h.update(block)
    assert h.hexdigest() == digest, key
    after = path.stat()
    assert (before.st_ino, before.st_size, before.st_mtime_ns) == (after.st_ino, after.st_size, after.st_mtime_ns), key
    VERIFIED[key] = digest
    TOTAL_BYTES += after.st_size
    return path

def header(f):
    version = np.lib.format.read_magic(f)
    if version == (1, 0): return np.lib.format.read_array_header_1_0(f)
    if version == (2, 0): return np.lib.format.read_array_header_2_0(f)
    raise AssertionError(('unreviewed_header_version', version))

def record(ref, owner, flags, expected_stem, ordinal, receipt=None):
    match = re.fullmatch(re.escape(expected_stem) + r'_(\d{5})_(.+)\.npz', ref['file'])
    assert match and int(match[1]) == ordinal
    role = match[2]
    assert ref['commit_file'] == ref['file'] + '.COMMIT.json'
    if receipt is not None:
        assert receipt['output_sha256'][ref['file']] == ref['sha256']
        assert receipt['output_sha256'][ref['commit_file']] == ref['commit_sha256']
    archive = verified(ref['file'], ref['sha256'])
    commit_path = verified(ref['commit_file'], ref['commit_sha256'])
    assert not archive.stat().st_mode & 0o222 and not commit_path.stat().st_mode & 0o222
    commit = json.loads(commit_path.read_bytes())
    assert set(commit) == {'file', 'sha256', 'metadata'} and commit['file'] == ref['file'] and commit['sha256'] == ref['sha256']
    md = commit['metadata']
    if 'metadata' in ref: assert md == ref['metadata']
    assert md['role'] == role and md['owner'] == owner and md['failed'] is False and md['qualification'] == flags
    if role == 'PREPARATION': assert md['uniform_DD_or_inverse_or_physical_adoption'] is False
    else: assert md['physical_adoption'] is False
    with zipfile.ZipFile(archive) as z:
        assert set(z.namelist()) == {n + '.npy' for n in md['schema']} | {'metadata_json.npy'}
        for n, schema in md['schema'].items():
            with z.open(n + '.npy') as f: shape, order, dtype = header(f)
            assert list(shape) == schema['shape'] and str(dtype) == schema['dtype'] and schema['finite'] is True
    with np.load(archive, allow_pickle=False) as z:
        assert json.loads(str(z['metadata_json'])) == md
    return dict(ordinal=ordinal, role=role, file=ref['file'], sha256=ref['sha256'], commit_file=ref['commit_file'], commit_sha256=ref['commit_sha256'])

def main():
 stem='SAVED_PHASE_RATE_UNIT_COEFFICIENT_PREPARATION_V005'
 proof=BASE/'ROOT_NATURAL_CLOSED_SAVED_PHASE_RATE_UNIT_SUCCESS_SEALS_V001.json'
 assert not proof.exists()
 source='saved_phase_rate_unit_coefficient_preparation_v005.py';sh='e567e782be60aa8378030f3a02c97762000df9c058a33f7cacf30062024c9368'
 rh='f5965c99906a34564dd1dfed95205be28367ed60a75dcaff68cfd51711ddffd5';ch='812d617bdc5f640d0637afe66c4eb1439bbe6ad239b99c3d52de5fc54b40ccc3'
 r=json.loads(verified(stem+'_RESULT.json',rh).read_bytes());rc=json.loads(verified(stem+'_RECEIPT.json',ch).read_bytes());verified(source,sh)
 assert r['owner']==rc['owner'] and r['owner']['pid']==82730 and r['owner']['source_sha256']==sh
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==rh
 assert r['status']=='SAVED_CURRENT_PHASE_RATE_UNIT_COEFFICIENTS_PREPARED_UNQUALIFIED'
 assert r['qualification']==rc['qualification'] and len(r['qualification'])==9 and all(v is False for v in r['qualification'].values())
 assert not (BASE/(stem+'_ERROR.json')).exists() and not (BASE/(stem+'_ERROR_RECEIPT.json')).exists()
 for n,h in rc['input_sha256'].items():verified(n,h)
 for n,h in rc['output_sha256'].items():verified(n,h)
 roles=['INPUT']+(['CACHE_COPY','UNIT_EOS']+['UNIT_NORMAL_ROW']*4+['UNIT_COLUMN'])*4+['PREPARATION']
 assert len(r['checkpoints'])==30 and [q['metadata']['role'] for q in r['checkpoints']]==roles
 for i,q in enumerate(r['checkpoints']):record(q,r['owner'],r['qualification'],stem,i,rc)
 expected=['column%d_NEW_unit_fraction_%s'%(iq,n) for iq in range(4) for n in ('p','H','normal0','normal1','normal2','normal3')]
 assert len(r['controls'])==24 and [c['name'] for c in r['controls']]==expected
 assert all(c['passed'] is True and c['tolerance']==2e-11 and 0<=c['error']<=2e-11 for c in r['controls'])
 case=r['case'];assert case['roles']==30 and case['controls']==24 and case['unit_ports']==16 and case['physical_adoption'] is False and case['old_VALUE_preparation_action_or_control_replayed'] is False
 assert len(case['columns'])==4
 for iq,ref in enumerate(case['columns']):
  q=next(x for x in r['checkpoints'] if x['file']==ref['file']);md=q['metadata'];assert md['column']==iq and md['normal_row_order']==['lapse','beta_R','beta_Z','beta_phi'] and md['normal_test_jet_order']==['value','R','Z','t']
  for n in ('normal_value_coefficient_hi','normal_value_coefficient_lo','raw_source_unsigned','represented_proxy_unsigned'):assert md['schema']['completed_UNIT_COLUMN_'+n]['shape']==[3784,4]
  assert md['only_value_coefficient_nonzero'] is md['time_primary_and_CMC_phase_rate_exact_zero'] is md['original157_whole_correction_required'] is True and md['arbitrary_DD_association_qualified'] is md['physical_adoption'] is False
 d=dict(status='ROOT_NATURAL_CLOSED_SAVED_PHASE_RATE_UNIT_SUCCESS_SEALS_VERIFIED',verified_at=datetime.now(timezone.utc).isoformat(),owner=r['owner'],source_sha256=sh,result_sha256=rh,receipt_sha256=ch,naturally_closed=True,exit_code=0,observed_session=72407,input_seals_verified=len(rc['input_sha256']),output_seals_verified=len(rc['output_sha256']),all_input_seals_verified=True,all_output_seals_verified=True,all_success_role_seals_verified=True,role_count=30,controls=24,original_controls_passed=True,max_control_error=max(c['error'] for c in r['controls']),new_point_unit_directions=4,new_normal_VALUE_derivatives=16,headers_and_embedded_metadata_verified=True,numeric_arrays_decoded=False,numeric_finite_assertions_scope='Authenticated producing-worker schema; numeric arrays not independently decoded',total_bytes_verified=TOTAL_BYTES,current19724_H_and_closed28110_cache_preserved=True,original_V004_failure_preserved=True,all_four_exact_original_cache_recovery_proof='ROOT_RECOVERED_EXACT_ORIGINAL_PHASE_RATE_CACHES_V001.json',physical_adoption=False,uniform_DD_or_global_inverse_qualified=False,whole157_correction_and_fresh_finite_authority_required=True,qualification=r['qualification'])
 proof.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');proof.chmod(0o444);print(proof.name,hashlib.sha256(proof.read_bytes()).hexdigest(),TOTAL_BYTES,d['max_control_error'])
if __name__=='__main__':main()
