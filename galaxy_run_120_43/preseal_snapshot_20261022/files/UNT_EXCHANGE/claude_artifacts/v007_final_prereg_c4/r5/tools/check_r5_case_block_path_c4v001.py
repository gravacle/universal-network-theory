"""Claude4 r5 helper: replay compare r12 cx3v002's sealed-mode case-block steps (L5705-L5729: prereg strict load, binding_inputs.case_block
{path, sha256}, case-block bytes and sha, strict load, route-A mode sources, validate_case_block) with r12's OWN functions, in-process, on
prereg r5 (expected valid) and on prereg r4 (expected CASE_BLOCK_ABSENT). It reads no run, gate record or manifest and calls no main().
Run ONLY under run_fenced_c4r5.py. usage: ... check_r5_case_block_path_c4v001.py PREREG_R5 PREREG_R4 OUT_JSON UTC"""
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import load_r12_c4r5 as L                                                     # noqa: E402

pr5, pr4, outp, utc = sys.argv[1:5]
M = L.load()
sha = lambda b: hashlib.sha256(b).hexdigest()


def sealed_case_block_steps(prereg_path, cli_case_block=None, cli_mode=None):
    """The r12 steps from 'pre = load_strict_file(a.prereg, ...)' to 'validate_case_block' (sealed mode: no --case-block)."""
    try:
        pre = M.load_strict_file(prereg_path, 'prereg')
        cbp = (pre.get('binding_inputs') or {}).get('case_block') if isinstance(pre, dict) else None
        if isinstance(cbp, dict):
            cb_path, cb_sha = cbp['path'], cbp['sha256']
        else:
            raise M.Refused('REFUSED: no case block (prereg binding_inputs.case_block, or --case-block in test mode)', 'CASE_BLOCK_ABSENT')
        cb_raw = Path(cb_path).read_bytes()
        if cb_sha is not None and sha(cb_raw) != cb_sha:
            raise M.Refused('REFUSED: case block sha mismatch', 'CASE_BLOCK_SHA_MISMATCH')
        cb = M.load_strict_file(cb_path, 'case block')
        mode_sources = [x for x in (pre.get('route_a_mode'), (cb or {}).get('route_a_mode') if isinstance(cb, dict) else None, cli_mode) if x is not None]
        if len(set(map(str, mode_sources))) > 1:
            raise M.Refused('REFUSED: route-A mode differs', 'ROUTE_A_MODE_SOURCES_DIFFER')
        mode = mode_sources[0] if mode_sources else M.ROUTE_A_MODE_DEFAULT
        why = M.validate_case_block(cb, route_a_mode=mode)
        if why:
            raise M.Refused('REFUSED: case block: %s' % why, 'CASE_BLOCK_INVALID')
        return {'reading': 'CASE_BLOCK_ACCEPTED', 'case_block': {'path': cb_path, 'sha256': sha(cb_raw)}, 'route_a_mode': mode, 'mode_sources': mode_sources,
                'validate_case_block': why, 'prereg_sha256': sha(Path(prereg_path).read_bytes())}
    except M.Refused as exc:
        return {'reading': 'REFUSED', 'code': getattr(exc, 'refusal_code', None), 'prereg_sha256': sha(Path(prereg_path).read_bytes())}


out = {'schema': 'UNT_V007_R5_CASE_BLOCK_PATH_CHECK_C4V001', 'utc': utc, 'compare': {'path': L.CMP, 'sha256': L.CMP_SHA},
       'label': 'TESTED: r12\'s own functions replayed in-process on the r5 and r4 prereg bytes; FORMAL: that the steps equal r12 L5705-L5729 (code reading)',
       'r5': sealed_case_block_steps(pr5), 'r4_control': sealed_case_block_steps(pr4),
       'r5_with_cli_mode_parallel8': sealed_case_block_steps(pr5, cli_mode='parallel8'),
       'r5_with_cli_mode_serial_must_refuse': sealed_case_block_steps(pr5, cli_mode='serial_with_exemption'),
       'sealed_driver_of_active_build': M.sealed_driver_sha(), 'loader_stat_guard': {'refused': L.GUARD['refused'], 'events': L.GUARD['events']}}
out['verdict'] = ('PASS' if out['r5']['reading'] == 'CASE_BLOCK_ACCEPTED' and out['r4_control'].get('code') == 'CASE_BLOCK_ABSENT'
                  and out['r5_with_cli_mode_parallel8']['reading'] == 'CASE_BLOCK_ACCEPTED'
                  and out['r5_with_cli_mode_serial_must_refuse'].get('code') == 'ROUTE_A_MODE_SOURCES_DIFFER' else 'FAIL')
with open(outp, 'x') as f:
    f.write(json.dumps(out, indent=1) + '\n')
print(out['verdict'], '| r5', out['r5']['reading'], out['r5'].get('case_block'), '| r4', out['r4_control'].get('code'),
      '| cli parallel8', out['r5_with_cli_mode_parallel8']['reading'], '| cli serial', out['r5_with_cli_mode_serial_must_refuse'].get('code'),
      '| stat guard', L.GUARD['refused'])
print('out', outp, hashlib.sha256(Path(outp).read_bytes()).hexdigest())
