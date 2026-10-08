"""Read-only byte and header verification of naturally closed ROOT64736."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, zipfile
import numpy as np

BASE = Path(__file__).resolve().parent
STEM = 'SAVED_PREFIX_COEFFICIENT_ADJOINT_CONTINUATION_V003'
PROOF = BASE / 'ROOT_NATURAL_CLOSED_SAVED_PREFIX_COEFFICIENT_ADJOINT_SUCCESS_SEALS_V001.json'
SOURCE = 'saved_prefix_coefficient_adjoint_continuation_v003.py'
SOURCE_SHA = 'eee8a878e3646ee9217166a3f8af8fa369805105a0566a33740046b4d5aac70c'
RESULT_SHA = '36480a114571fb7f976f591eab6cf779bcf7ac3467e2d2ccb0073590d264f4ed'
RECEIPT_SHA = '09084a79011d7720d7ce3c48bb16dc2d15b61e5da0229e6e417b76e26c7c7160'
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

def main():
    assert not PROOF.exists()
    verified(SOURCE, SOURCE_SHA)
    result = json.loads(verified(STEM + '_RESULT.json', RESULT_SHA).read_bytes())
    rc = json.loads(verified(STEM + '_RECEIPT.json', RECEIPT_SHA).read_bytes())
    owner, flags = result['owner'], result['qualification']
    assert owner['pid'] == 64736 and owner['source_sha256'] == SOURCE_SHA
    assert rc['status'] == 'CLOSED' and rc['error_sha256'] is None and rc['result_sha256'] == RESULT_SHA
    assert rc['owner'] == owner and rc['qualification'] == flags and len(flags) == 9 and all(v is False for v in flags.values())
    case = result['case']
    assert result['status'] == case['status'] == 'SAVED_PREFIX_COEFFICIENT_ADJOINT_SOURCE_ROWS_ADMITTED'
    assert case['roles'] == len(result['checkpoints']) == 5771 and len(result['controls']) == 4
    assert len(rc['input_sha256']) == 430 and len(rc['output_sha256']) == 11545
    assert case['cycles'] == 1 and case['restarts'] == 0 and case['cap80_total'] is True
    assert case['physical_adoption'] is case['old_actions_factors_or_controls_replayed'] is case['uniform_adjoint_or_global_inverse_qualified'] is False
    scores = np.asarray(case['source_relative_scores'])
    assert scores.shape == (3, 2) and np.all(np.isfinite(scores)) and np.all(scores <= 1e-10)
    for c in result['controls']:
        assert c['passed'] is True and c['tolerance'] == 2e-11 and 0 <= c['error'] <= 2e-11
    history = case['history']
    assert history['iterations'] == 40 and history['resumed_completed_iterations'] == 7
    assert history['earned_V7_factor_returned_once'] is True
    assert history['acceptance_scope'] == 'same_represented_coefficient_Astar_original53_source_relative_rows'
    assert history['original_forward_physical_six_gates_tested'] is history['self_adjointness_assumed'] is False
    for group in ('input_sha256', 'output_sha256'):
        for name, digest in rc[group].items(): verified(name, digest)
    records, census = [], {}
    for ordinal, ref in enumerate(result['checkpoints']):
        match = re.fullmatch(re.escape(STEM) + r'_(\d{5})_(.+)\.npz', ref['file'])
        assert match and int(match[1]) == ordinal
        role = match[2]
        census[role] = census.get(role, 0) + 1
        assert ref['commit_file'] == ref['file'] + '.COMMIT.json'
        assert rc['output_sha256'][ref['file']] == ref['sha256'] and rc['output_sha256'][ref['commit_file']] == ref['commit_sha256']
        archive = verified(ref['file'], ref['sha256'])
        commit_path = verified(ref['commit_file'], ref['commit_sha256'])
        assert not archive.stat().st_mode & 0o222 and not commit_path.stat().st_mode & 0o222
        commit = json.loads(commit_path.read_bytes())
        assert set(commit) == {'file', 'sha256', 'metadata'} and commit['file'] == ref['file'] and commit['sha256'] == ref['sha256']
        md = commit['metadata']
        assert md == ref['metadata'] and md['owner'] == owner and md['failed'] is False and md['qualification'] == flags
        with zipfile.ZipFile(archive) as z:
            assert set(z.namelist()) == {n + '.npy' for n in md['schema']} | {'metadata_json.npy'}
            for n, schema in md['schema'].items():
                with z.open(n + '.npy') as f: shape, order, dtype = header(f)
                assert list(shape) == schema['shape'] and str(dtype) == schema['dtype'] and schema['finite'] is True
        with np.load(archive, allow_pickle=False) as z:
            assert json.loads(str(z['metadata_json'])) == md
            if role == 'SOLUTION':
                assert {k: ref[k] for k in ('file','sha256','commit_file','commit_sha256')} == case['solution']
                assert np.array_equal(z['scores'].view(np.uint64), scores.view(np.uint64))
        records.append(dict(ordinal=ordinal, role=role, file=ref['file'], sha256=ref['sha256'], commit_file=ref['commit_file'], commit_sha256=ref['commit_sha256']))
    assert census['SOLUTION'] == 1
    proof = dict(status='ROOT_NATURAL_CLOSED_SAVED_PREFIX_COEFFICIENT_ADJOINT_SUCCESS_SEALS_VERIFIED', saved=datetime.now(timezone.utc).isoformat(),
                 source_file=SOURCE, source_sha256=SOURCE_SHA, result_file=STEM+'_RESULT.json', result_sha256=RESULT_SHA,
                 receipt_file=STEM+'_RECEIPT.json', receipt_sha256=RECEIPT_SHA, owner=owner, naturally_closed=True, exit_code=0,
                 observed_session_id=37638, all_input_seals_verified=True, all_success_role_seals_verified=True,
                 input_count=430, output_count=11545, success_roles=5771, records=records, role_census=census,
                 source_relative_adjoint_rows_admitted=True, source_relative_scores=scores.tolist(), tolerance=1e-10,
                 controls=result['controls'], history={k:v for k,v in history.items() if k != 'new_stage_refs'}, solution=case['solution'],
                 qualification=flags, physical_adoption=False, original_forward_physical_six_gates_tested=False,
                 normal_CMC_feedback_or_new43_readout_earned=False, uniform_adjoint_or_global_inverse_qualified=False,
                 old_actions_factors_or_controls_replayed=False, old_lambda_is_only_warmstart_for_new_literal_RHS=True,
                 fresh_verified_bytes_including_metadata=TOTAL_BYTES, verified_sha256=VERIFIED)
    data = (json.dumps(proof, sort_keys=True, indent=2) + '\n').encode()
    with PROOF.open('xb') as f: f.write(data)
    PROOF.chmod(0o444)
    print(json.dumps(dict(file=PROOF.name, sha256=hashlib.sha256(data).hexdigest(), status=proof['status'], bytes=TOTAL_BYTES, roles=5771)))

if __name__ == '__main__': main()
