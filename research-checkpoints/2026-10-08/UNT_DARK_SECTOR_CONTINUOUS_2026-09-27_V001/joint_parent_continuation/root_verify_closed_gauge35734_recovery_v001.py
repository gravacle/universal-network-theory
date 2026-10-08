"""Read-only byte/header verification of naturally closed ROOT66785."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, zipfile
import numpy as np

BASE = Path(__file__).resolve().parent
STEM = 'SAVED_GAUGE35734_ARITHMETIC_TAIL_RECOVERY_V005'
PROOF = BASE / 'ROOT_NATURAL_CLOSED_SAVED_GAUGE35734_RECOVERY_SUCCESS_SEALS_V001.json'
SOURCE = 'saved_gauge35734_arithmetic_tail_recovery_v005.py'
SOURCE_SHA = '6dcb4ac53f9597a848f1c2b7c26caf383ff63542dde4f229a882d83815b60d2a'
RESULT_SHA = 'd62f903a5812248f463b4c4b61408669113e153cf4eaa127a663a7159a296960'
RECEIPT_SHA = '3e5d4fe3fc1f41f893509692387cd0ad6ce256b496e4951e008c2793394fb91c'
OLD_PROOF = 'ROOT_CLOSED_GAUGE35734_PARTIAL_SUCCESS_BYTE_SEALS_V001.json'
OLD_PROOF_SHA = '66eb1d867f22fa09ab51ee0b3e5690a3a77d7ba398a9af6d7369d3cc7fd87961'
VERIFIED = {}
TOTAL_BYTES = 0

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
    assert md['physical_adoption'] is False
    with zipfile.ZipFile(archive) as z:
        assert set(z.namelist()) == {n + '.npy' for n in md['schema']} | {'metadata_json.npy'}
        for n, schema in md['schema'].items():
            with z.open(n + '.npy') as f: shape, order, dtype = header(f)
            assert list(shape) == schema['shape'] and str(dtype) == schema['dtype'] and schema['finite'] is True
    with np.load(archive, allow_pickle=False) as z:
        assert json.loads(str(z['metadata_json'])) == md
    return dict(ordinal=ordinal, role=role, file=ref['file'], sha256=ref['sha256'], commit_file=ref['commit_file'], commit_sha256=ref['commit_sha256'])

def main():
    assert not PROOF.exists()
    verified(SOURCE, SOURCE_SHA)
    result = json.loads(verified(STEM + '_RESULT.json', RESULT_SHA).read_bytes())
    rc = json.loads(verified(STEM + '_RECEIPT.json', RECEIPT_SHA).read_bytes())
    old = json.loads(verified(OLD_PROOF, OLD_PROOF_SHA).read_bytes())
    owner, flags, case = result['owner'], result['qualification'], result['case']
    assert owner['pid'] == 66785 and owner['source_sha256'] == SOURCE_SHA
    assert rc['status'] == 'CLOSED' and rc['error_sha256'] is None and rc['result_sha256'] == RESULT_SHA
    assert rc['owner'] == owner and rc['qualification'] == flags and len(flags) == 9 and all(v is False for v in flags.values())
    assert result['status'] == case['status'] == 'CANDIDATE_GAUGE_REGISTERED_CURRENT_FORWARD_CONTACTS_MEASURED'
    assert len(result['checkpoints']) == case['current_roles'] == 51
    assert case['new_scientific_roles'] == 48 and case['auxiliary_roles'] == 3
    assert case['inherited_scientific_roles'] == len(result['inherited_checkpoints']) == 30
    assert case['logical_scientific_roles'] == 78 and case['genuinely_unstarted_ports_evaluated'] == 43
    assert case['lost_serialization_tail_reconstructed'] is True
    assert case['original_missing_COMMIT_and_failed_ERROR_RAW_preserved'] is True
    assert case['earned20_port_bodies_and80_controls_replayed'] is case['C_equals_minus_Rv_transpose_assumed'] is case['global_or_physical_adoption'] is case['physical_adoption'] is False
    assert case['new_controls'] == 0 and result['new_controls'] == []
    assert result['controls'] == case['original_control_descriptors'] == old['controls'] and len(result['controls']) == 80
    for c in result['controls']:
        assert c['passed'] is True and c['tolerance'] == 2e-11 and 0 <= c['error'] <= 2e-11
    assert old['verified_roles'] == 30 and old['all30_committed_role_seals_verified'] is True and old['pending'] == []
    assert len(rc['input_sha256']) == 65 and len(rc['output_sha256']) == 105
    for group in ('input_sha256', 'output_sha256'):
        for name, digest in rc[group].items(): verified(name, digest)
    current, inherited, census = [], [], {}
    for ordinal, ref in enumerate(result['checkpoints']):
        row = record(ref, owner, flags, STEM, ordinal, rc)
        census[row['role']] = census.get(row['role'], 0) + 1
        current.append(row)
    assert census == dict(SURVIVOR_SELECTION=1, DIVISION_TAIL=1, RAW_MECHANICAL_TAIL=1, GAUGE_TEST=44, COLUMN=3, PREPARATION=1)
    keys = ('file', 'sha256', 'commit_file', 'commit_sha256')
    assert result['inherited_checkpoints'] == [{k: r[k] for k in keys} for r in old['records']]
    for ordinal, ref in enumerate(result['inherited_checkpoints']):
        inherited.append(record(ref, old['owner'], flags, 'CROSS_U_CANDIDATE_GAUGE_REGISTERED_CURRENT_CONTROLS_V002', ordinal))
    assert case['columns'][0] == {k: result['inherited_checkpoints'][25][k] for k in keys}
    assert len(case['columns']) == 4 and len(case['tests']) == 4 and all(len(x) == 16 for x in case['tests'])
    proof = dict(status='ROOT_NATURAL_CLOSED_SAVED_GAUGE35734_RECOVERY_SUCCESS_SEALS_VERIFIED', saved=datetime.now(timezone.utc).isoformat(),
                 source_file=SOURCE, source_sha256=SOURCE_SHA, result_file=STEM+'_RESULT.json', result_sha256=RESULT_SHA,
                 receipt_file=STEM+'_RECEIPT.json', receipt_sha256=RECEIPT_SHA, owner=owner, naturally_closed=True, exit_code=0,
                 observed_session_id=23003, all_input_seals_verified=True, all_success_role_seals_verified=True,
                 input_count=65, output_count=105, current_roles=51, new_scientific_roles=48, inherited_scientific_roles=30,
                 logical_scientific_roles=78, records=current, inherited_records=inherited, role_census=census,
                 original80_controls_passed_and_preserved=True, controls=result['controls'], new_controls=0,
                 cache_columns=case['cache_columns'], columns=case['columns'], tests=case['tests'], preparation=case['preparation'],
                 qualification=flags, physical_adoption=False, normal_CMC_feedback_or_new43_readout_earned=False,
                 uniform_adjoint_or_global_inverse_qualified=False, old_actions_factors_or_controls_replayed=False,
                 C_equals_minus_Rv_transpose_assumed=False, source_scope='old-rate fixed-geometry registered-current forward coefficient block',
                 fresh_verified_bytes_including_metadata=TOTAL_BYTES, verified_sha256=VERIFIED)
    data = (json.dumps(proof, sort_keys=True, indent=2) + '\n').encode()
    with PROOF.open('xb') as f: f.write(data)
    PROOF.chmod(0o444)
    print(json.dumps(dict(file=PROOF.name, sha256=hashlib.sha256(data).hexdigest(), status=proof['status'], bytes=TOTAL_BYTES, current_roles=51, inherited_roles=30)))

if __name__ == '__main__': main()
