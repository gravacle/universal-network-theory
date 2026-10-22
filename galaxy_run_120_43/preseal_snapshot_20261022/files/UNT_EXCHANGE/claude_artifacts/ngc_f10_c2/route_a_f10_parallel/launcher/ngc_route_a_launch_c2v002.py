"""INERT minimal launch adapter: NGC3198 route A at the A2 factor-3 anchor (Claude2 lane, c2v001).

Exists only because the reviewed monitor root_monitor_c2v001.py (ba031c23) can run nothing but
    <python> -I -B <driver> run --spec SPEC --outdir OUTDIR
and the reviewed NGC worker v002 (42bdd23e) has a different CLI.  The MONITOR supplies the caps
(wall, tree RSS, output bytes), the fresh-OUTDIR rule, process-group kill and the receipt.

This adapter:
  1. reads SPEC once (a stage request in the driver c2v001 '_stage' format plus 'launch_pins');
  2. verifies, from bytes, every launch pin and the exact request shape (script = installed worker,
     one module patch = COEFFICIENT/COEFFICIENT_SHA on the installed NGC prep, no stage globals,
     no mask) and that --outdir equals the worker --outdir, OUTDIR is absent, the checkpoint
     directory is OUTDIR/checkpoint, start iteration 0, no --resume, single-thread BLAS env;
  3. executes, in this process, the reviewed driver c2v001 stage shim steps with the already-read
     request: driver._install_hooks(request); driver.exec_verified(worker); sys.argv; worker.main().
     These are driver c2v001 stage_main lines 358-367 verbatim except that the request is not
     re-read from disk.  This is the mechanism that ran the DDO A2 factor-3 route-A stage
     (A2_ANCHOR_F3_RUN_V001/stages/01_route_a/request.json).
No physics, numerics, tolerance or retry is added.  The worker writes start/progress/result/finish
(and failure.json on error) into OUTDIR; the checkpoint lives in OUTDIR/checkpoint.

CLI:  ngc_route_a_launch_c2v002.py run --spec SPEC.json --outdir OUTDIR
Importing this module does nothing.

c2v002 (PARALLEL; minimal successor of reviewed c2v001 f5e5e0fe, same request schema).  Only:
  (a) the worker must be the parallel NGC worker 5f16525a and the solver the parallel solver aed4dd59;
  (b) argv must carry '--column-workers N' (decimal 1..64, no sign/leading zero), exactly once;
  (c) the reviewed helper modules are resolved at the install packet directory INSTALL_H (the
      parallel worker's absolute H) instead of beside the worker file (it lives outside the packet).
Everything else, including the run steps, is c2v001 verbatim.  Worker processes are spawned by the
solver; spawn re-imports this file as __mp_main__, which only defines names (main guard below).
"""
import hashlib
import json
import os
import sys
import types
from pathlib import Path

THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')
SCHEMA = 'NGC3198_ROUTE_A_LAUNCH_REQUEST_C2V001'
REQUIRED_PIN_KEYS = ('driver_c2v001', 'worker', 'binding', 'prep', 'base', 'composite', 'stream', 'prediction',
                     'seed', 'solver', 'checkpoint_module', 'coefficients')
INSTALL_H = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_impl_c2/route_a/install/recovered_packet_audit')
PARALLEL_WORKER_SHA256 = '5f16525a094b54b19d9a9987edfeaf944e096d66f61f0663a19c7a68587fe890'
PARALLEL_SOLVER_SHA256 = 'aed4dd59b38bfe1043e0c38ad4592e4b6bb74c8c4bbee969a707a310926e6f58'


class Refusal(ValueError):
    pass


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def _argv_value(argv, flag):
    if argv.count(flag) != 1:
        raise Refusal('request argv must contain %s exactly once' % flag)
    i = argv.index(flag)
    if i + 1 >= len(argv):
        raise Refusal('request argv %s has no value' % flag)
    return argv[i + 1]


def verify_request(request, outdir):
    """All refusals happen here, before anything is created.  Returns the pinned driver path/sha."""
    if not isinstance(request, dict) or request.get('schema') != SCHEMA:
        raise Refusal('spec schema must be ' + SCHEMA)
    pins = request.get('launch_pins')
    if not isinstance(pins, dict) or set(pins) != set(REQUIRED_PIN_KEYS):
        raise Refusal('launch_pins must have exactly the keys %s' % (REQUIRED_PIN_KEYS,))
    for key in REQUIRED_PIN_KEYS:
        item = pins[key]
        if not (isinstance(item, dict) and set(item) == {'path', 'sha256'}):
            raise Refusal('launch_pins.%s must be {path, sha256}' % key)
        p = Path(item['path'])
        if not p.is_file():
            raise Refusal('pinned file missing: %s %s' % (key, p))
        if sha_file(p) != item['sha256']:
            raise Refusal('pin mismatch: %s %s' % (key, p))
    if pins['worker']['sha256'] != PARALLEL_WORKER_SHA256 or pins['solver']['sha256'] != PARALLEL_SOLVER_SHA256:
        raise Refusal('c2v002 launches only the parallel NGC worker %s with the parallel solver %s'
                      % (PARALLEL_WORKER_SHA256[:8], PARALLEL_SOLVER_SHA256[:8]))
    worker = Path(pins['worker']['path']).resolve()
    H = INSTALL_H
    O = H.parent / 'coefficient_method'
    local_names = {'binding': H / 'ngc_composite_full_coupled_binding_v002.py',
                   'prep': H / 'ngc_actual_initial_source_preparation_v001.py',
                   'base': H / 'owned_physical_fourier_metric_quadrature_v005.py',
                   'composite': O / 'owned_composite_prepared_coupled_gas_adapter_v001.py',
                   'stream': O / 'owned_streamed_fourier_per_run_adapter_v001.py',
                   'prediction': O / 'galaxy_coupled_fourier_hi_prediction_v005.py'}
    for key, path in local_names.items():
        if Path(pins[key]['path']).resolve() != path.resolve():
            raise Refusal('launch pin %s is not the module the worker resolves beside itself: %s' % (key, path))
    if set(request) - {'schema', 'name', 'kind', 'script', 'script_sha256', 'argv', 'stage_globals',
                       'module_patches', 'mask', 'launch_pins', 'note'}:
        raise Refusal('unknown request keys')
    if Path(request.get('script', '')).resolve() != worker or request.get('script_sha256') != pins['worker']['sha256']:
        raise Refusal('request script must be the pinned installed worker')
    if request.get('stage_globals') != {} or request.get('mask') is not None:
        raise Refusal('no stage globals and no truncation mask allowed (route A cube only)')
    patches = request.get('module_patches')
    expected_patch = {'path': str(Path(pins['prep']['path'])), 'sha256': pins['prep']['sha256'],
                      'set': {'COEFFICIENT': {'__path__': pins['coefficients']['path']},
                              'COEFFICIENT_SHA': pins['coefficients']['sha256']}}
    if patches != [expected_patch]:
        raise Refusal('module_patches must be exactly the A2 coefficient patch on the installed prep')
    argv = request.get('argv')
    if not (isinstance(argv, list) and all(isinstance(a, str) for a in argv)):
        raise Refusal('argv must be a list of str')
    if '--resume' in argv:
        raise Refusal('this adapter launches a NEW checkpoint only (no --resume)')
    flags = [a for a in argv if a.startswith('--')]
    if sorted(flags) != sorted(['--seed', '--seed-sha256', '--solver', '--solver-sha256', '--checkpoint-module',
                                '--checkpoint-module-sha256', '--outdir', '--checkpoint-directory', '--start-iteration',
                                '--column-workers']):
        raise Refusal('argv flags differ from the parallel worker v002 new-run CLI')
    n = _argv_value(argv, '--column-workers')
    if not (n.isdigit() and n.isascii() and n[0] != '0' and 1 <= int(n) <= 64):
        raise Refusal('--column-workers must be a decimal int 1..64')
    for flag, key in (('--seed', 'seed'), ('--solver', 'solver'), ('--checkpoint-module', 'checkpoint_module')):
        if Path(_argv_value(argv, flag)).resolve() != Path(pins[key]['path']).resolve():
            raise Refusal('%s is not the pinned %s' % (flag, key))
        if _argv_value(argv, flag + '-sha256') != pins[key]['sha256']:
            raise Refusal('%s-sha256 is not the pinned sha' % flag)
    if _argv_value(argv, '--start-iteration') != '0':
        raise Refusal('start iteration must be 0')
    out = Path(outdir)
    if not out.is_absolute():
        raise Refusal('outdir must be absolute')
    if Path(_argv_value(argv, '--outdir')) != out:
        raise Refusal('--outdir differs from the request worker --outdir')
    if Path(_argv_value(argv, '--checkpoint-directory')) != out / 'checkpoint':
        raise Refusal('checkpoint directory must be OUTDIR/checkpoint')
    if out.exists() or os.path.lexists(out):
        raise Refusal('outdir exists (must be absent): %s' % out)
    if not out.parent.is_dir():
        raise Refusal('outdir parent missing: %s' % out.parent)
    bad = [k for k in THREAD_ENV if os.environ.get(k) != '1']
    if bad:
        raise Refusal('single-thread env required (run under the monitor): %s' % bad)
    return pins['driver_c2v001']['path'], pins['driver_c2v001']['sha256']


def load_driver(path, sha):
    """Execute the pinned driver bytes (importing it does nothing: definitions only)."""
    raw = Path(path).read_bytes()
    if sha_bytes(raw) != sha:
        raise Refusal('driver pin mismatch on load')
    module = types.ModuleType('ngc_route_a_c2v001_driver')
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


def run(spec_path, outdir):
    raw = Path(spec_path).read_bytes()
    request = json.loads(raw)
    driver_path, driver_sha = verify_request(request, outdir)
    driver = load_driver(driver_path, driver_sha)
    # driver c2v001 stage_main (lines 358-367), with the request already read and verified:
    driver._install_hooks(request)
    module = driver.exec_verified(request['script'], request['script_sha256'],
                                  'c2v001_stage_' + Path(request['script']).stem)
    sys.argv = [request['script']] + list(request['argv'])
    module.main()
    return 0


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('command', choices=['run'])
    ap.add_argument('--spec', required=True)
    ap.add_argument('--outdir', required=True)
    a = ap.parse_args(argv)
    try:
        return run(a.spec, a.outdir)
    except Refusal as exc:
        sys.stderr.write('REFUSED: %s\n' % exc)
        return 3


if __name__ == '__main__':
    sys.exit(main())
