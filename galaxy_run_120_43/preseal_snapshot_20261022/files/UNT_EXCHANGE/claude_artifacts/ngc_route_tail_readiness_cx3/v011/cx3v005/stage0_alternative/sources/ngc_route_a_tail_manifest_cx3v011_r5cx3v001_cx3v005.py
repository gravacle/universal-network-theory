"""Route-A UV-tail manifest writer (Claude2 tail_scheme_impl_c2/driver, c2v001).  INERT at import: no file read, no arithmetic.

Purpose.  The route-B reference, body and offset successors (tail_scheme_impl_c2/route_b, uvt_route_b_binding_c2v001.py
7288a5d1, Binding._manifest / _manifest_gas_roster) read the route-A tail state of the ACCEPTED route-A iteration from a
manifest of schema UNT_UV_TAIL_ROUTE_A_MANIFEST_C2V001 (defined in route_b/tools/route_a_fixture_manifest_c2v002.py).  The
route-A sidecar (route_a_uv_tail_controller_c2v001.py 51d32e7b) stores the per-iteration element rosters and state digests,
not the state arrays.  This stage writes the manifest from a COMPLETED tail-ON route-A attempt:

  1. custody: the attempt finish.json is RETURNED_ACTUAL_RESULT and binds result.json; result.result.uv_tail (the controller's
     result_record) has outcome CONVERGED_FINITE_FIXED_POINT, an accepted iteration n, the request sha of --uv-tail-request,
     a sidecar whose finish record and listed files verify from bytes;
  2. the route-A controller is rebuilt EXACTLY as the route-A binding builds it: the reviewed prep's prepare_inputs on the
     seed numerical_inputs (the driver applies the same prep module patches / LOCAL['prep'] dict item it applies to route A),
     then RouteATailController.from_prepared(galaxy='NGC3198', ..., sidecar_directory=None) -- nothing is written to the sidecar;
     its static identity (+ relaxation, checkpoint identity) must equal the sidecar's SIDECAR_IDENTITY.json identity;
  3. the element rosters elements_0000..n-1 are read from the sidecar (digests checked against each iteration record), the
     iteration-n gas array is read from the checkpoint (iteration_n/START.json gas_fourier_J), and the state is rebuilt with the
     controller's own build path (_i1t, _build: the same code route A ran in begin_iteration / complete_iteration);
  4. the rebuilt state digest must equal (a) the sidecar iteration_n payload state_digest, (b) result uv_tail
     iterations[-1].state_digest and (c) boundary_state_digest_at_return -- else refusal UV_TAIL_MANIFEST_STATE_NOT_REPRODUCED;
  5. writes state arrays (npz), the route-A gas_IT roster (GasColumns.arrays(): the offset's Delta = body gas - route-A gas_IT),
     and the manifest; the manifest state is re-loaded with TailState.from_arrays(expected_digest) before the manifest exists.

Eval radii: the state is the route-A state with the route-A eval radii (gas-column radii, monitor probes, prediction stencil);
the reference/body radii outside that set use the library's on-demand tables (diagnostics.on_demand_radius_builds); the
values are the same arithmetic.  Cost: one reviewed prep pass plus one tail build (UNTESTED at production size).

CLI (run through the driver's _stage shim): --seed --seed-sha256 --attempt-directory --checkpoint-directory
--checkpoint-module --checkpoint-module-sha256 --uv-tail-request --uv-tail-request-sha256 --outdir
"""
import argparse
import hashlib
import importlib.util
import json
import os
import time
from pathlib import Path

ROOT = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
SCHEMA = 'UNT_UV_TAIL_ROUTE_A_MANIFEST_C2V001'
WRITER_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_MANIFEST_WRITER_C2V001'
# LOCAL['prep'] is replaced by the driver (stage_dict_items) for grids > 80 nodes/axis exactly as for the route-A worker.
LOCAL = {
    'prep': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/sources/ngc_actual_initial_source_preparation_cx3v011_cx3v005.py'), 'd578889248f0e2f7a40ded8c6645a14811ac8ba59c192e4e6ef243dde06db5f8'),
}
PINS = {
    'controller': (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001_r5.py'),
                   'c5bdd0553968e3f00b61db89f7944cebe51166006f58b727a7aed2a9b6a434fc'),
}
CONVERGED = 'CONVERGED_FINITE_FIXED_POINT'


class ManifestRefusal(RuntimeError):
    """Custody or reproduction failure (never a physical result)."""


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _load(name, path, sha):
    if sha_file(path) != sha:
        raise ManifestRefusal('UV_TAIL_MANIFEST_PIN_MISMATCH ' + str(path))
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if sha_file(path) != sha:
        raise ManifestRefusal('UV_TAIL_MANIFEST_PIN_CHANGED_AFTER_IMPORT ' + str(path))
    return mod


def _write_x(path, obj):
    with open(path, 'x') as f:
        json.dump(obj, f, indent=1, allow_nan=False, sort_keys=True)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    return sha_file(path)


def _savez_x(path, arrays):
    import numpy as np
    with open(path, 'xb') as f:
        np.savez(f, **arrays)
        f.flush()
        os.fsync(f.fileno())
    return sha_file(path)


def attempt_tail_record(attempt_directory, request_sha256):
    """(result.json path, its sha, uv_tail record) of a completed tail-ON route-A attempt; refuses anything else."""
    att = Path(attempt_directory)
    fin = json.loads((att / 'finish.json').read_text())
    rp = att / 'result.json'
    rsha = sha_file(rp)
    if fin.get('status') != 'RETURNED_ACTUAL_RESULT' or fin.get('result_sha256') != rsha:
        raise ManifestRefusal('UV_TAIL_MANIFEST_ATTEMPT_NOT_COMPLETED %s' % att)
    res = json.loads(rp.read_text())
    uv = (res.get('result') or {}).get('uv_tail')
    if not isinstance(uv, dict):
        raise ManifestRefusal('UV_TAIL_MANIFEST_NO_TAIL_RECORD: result.result.uv_tail absent (tail-OFF route A?)')
    if uv.get('request_sha256') != request_sha256:
        raise ManifestRefusal('UV_TAIL_MANIFEST_REQUEST_MISMATCH %r != %r' % (uv.get('request_sha256'), request_sha256))
    n = uv.get('accepted_iteration')
    if uv.get('outcome') != CONVERGED or type(n) is not int or n < 0:
        raise ManifestRefusal('UV_TAIL_MANIFEST_NO_ACCEPTED_ITERATION outcome %r accepted %r' % (uv.get('outcome'), n))
    sc = uv.get('sidecar')
    if not isinstance(sc, dict) or sha_file(sc['finish']['path']) != sc['finish']['sha256']:
        raise ManifestRefusal('UV_TAIL_MANIFEST_SIDECAR_FINISH_PIN')
    for name, s in sc['files'].items():
        if sha_file(Path(sc['directory']) / name) != s:
            raise ManifestRefusal('UV_TAIL_MANIFEST_SIDECAR_FILE_PIN ' + name)
    return rp, rsha, uv


def sidecar_elements(sidecar_directory, n):
    """Element rosters of iterations 0..n-1 and the iteration records 0..n, digests checked (controller _array_digest form)."""
    import numpy as np
    d = Path(sidecar_directory)

    def digest(a):
        a = np.ascontiguousarray(a)
        h = hashlib.sha256()
        h.update(('%s|%s|' % (a.dtype.str, a.shape)).encode())
        h.update(a.tobytes())
        return h.hexdigest()
    records, elements = [], []
    for i in range(n + 1):
        rec = json.loads((d / ('iteration_%04d.json' % i)).read_text())['payload']
        if rec['iteration'] != i:
            raise ManifestRefusal('UV_TAIL_MANIFEST_SIDECAR_SEQUENCE iteration %d' % i)
        records.append(rec)
        if i < n:
            with np.load(d / rec['elements']['file'], allow_pickle=False) as f:
                pos = f['positions_m'].copy()
                J = f['integrated_J'].copy()
            if digest(pos) != rec['elements']['positions_digest'] or digest(J) != rec['elements']['J_digest']:
                raise ManifestRefusal('UV_TAIL_MANIFEST_SIDECAR_ELEMENTS iteration %d' % i)
            elements.append(dict(positions_m=pos, integrated_J=J))
    return records, elements


def rebuild_state(controller, *, sidecar_identity, elements, n, gas):
    """The accepted-iteration TailState through the controller's own build path (no sidecar writes): relaxation from the
    sidecar identity, element rosters 0..n-1, I1-T on the iteration-n gas array, then _build(n, i1t)."""
    ctl = controller
    ctl.relaxation = float(sidecar_identity['relaxation'])
    ctl.elements = list(elements)
    ctl._T_upd = []
    ctl._T_init = None
    return ctl._build(n, ctl._i1t(n, gas))


def write_outputs(outdir, *, controller, state, n, identity_sha256, start_payload_sha256, provenance):
    """State npz, gas_IT roster npz, manifest (after a from_arrays reload check).  Returns the manifest record."""
    import numpy as np
    ctl = controller
    out = Path(outdir)
    out.mkdir(exist_ok=False)
    state_path = out / 'route_a_tail_state.npz'
    state_sha = _savez_x(state_path, state.to_arrays())
    record = json.loads(json.dumps(state.record))
    with np.load(state_path, allow_pickle=False) as f:
        back = ctl.lib.TailState.from_arrays({k: f[k].copy() for k in f.files}, record, expected_digest=state.digest)
    gas = ctl.rs.roster_route_a(ctl.stars, ctl.init_rings, ctl.elements[:n], ctl.relaxation, s_edges_kpc2=ctl.s_edges,
                                kpc_m=ctl.kpc_m, M_s=ctl.M_s, c_m_s=ctl.c_m_s).gas
    roster_path = out / 'route_a_gas_it_roster.npz'
    roster_sha = _savez_x(roster_path, gas.arrays())
    man = dict(schema=SCHEMA,
               route_a=dict(identity_sha256=identity_sha256, accepted_iteration=n, iteration_start_payload_sha256=start_payload_sha256),
               config_sha256=ctl.config['sha256'],
               state=dict(record=record, digest=back.digest, arrays=dict(path=str(state_path.resolve()), sha256=state_sha)),
               i1t=record['i1t'],
               roster=dict(kind='registered_gas_columns', record=json.loads(json.dumps(gas.record())),
                           arrays=dict(path=str(roster_path.resolve()), sha256=roster_sha)),
               writer=dict(schema=WRITER_SCHEMA, path=str(Path(__file__).resolve()), sha256=sha_file(__file__)),
               provenance=provenance)
    msha = _write_x(out / 'ROUTE_A_TAIL_MANIFEST.json', man)
    return dict(manifest=str((out / 'ROUTE_A_TAIL_MANIFEST.json').resolve()), manifest_sha256=msha, state_digest=back.digest,
                empty=bool(state.empty), production_admissible=bool(record.get('production_admissible')))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('seed', 'seed-sha256', 'attempt-directory', 'checkpoint-directory', 'checkpoint-module',
                 'checkpoint-module-sha256', 'uv-tail-request', 'uv-tail-request-sha256', 'outdir'):
        p.add_argument('--' + name, required=True)
    a = p.parse_args()
    t0 = time.monotonic()
    if sha_file(a.seed) != a.seed_sha256 or sha_file(a.uv_tail_request) != a.uv_tail_request_sha256:
        raise ManifestRefusal('UV_TAIL_MANIFEST_INPUT_PIN (seed or request)')
    seed = json.loads(Path(a.seed).read_text())
    for path, expected in seed['pins'].items():
        if sha_file(path) != expected:
            raise ManifestRefusal('UV_TAIL_MANIFEST_SEED_PROVENANCE ' + path)
    cm = _load('uvt_manifest_checkpoint', Path(a.checkpoint_module), a.checkpoint_module_sha256)
    ctl_mod = _load('route_a_uv_tail_controller_c2v001', *PINS['controller'])
    prep_path, prep_sha = LOCAL['prep']
    prep = _load('root_composite_prep', Path(prep_path), prep_sha)
    raw_request = json.loads(Path(a.uv_tail_request).read_text())
    libs = ctl_mod.load_libraries()
    req_norm = ctl_mod.normalize_request(raw_request, libs['lib'])
    rp, rsha, uv = attempt_tail_record(a.attempt_directory, req_norm['sha256'])
    n = uv['accepted_iteration']
    cp = Path(a.checkpoint_directory)
    ident = cm._read(str(cp / 'IDENTITY.json'), 'identity')
    if uv.get('checkpoint_identity_sha256') != ident['identity_sha256']:
        raise ManifestRefusal('UV_TAIL_MANIFEST_CHECKPOINT_MISMATCH %r != %r' % (uv.get('checkpoint_identity_sha256'), ident['identity_sha256']))
    start = cm._read(str(cp / ('iteration_%04d' % n) / 'START.json'), 'iteration_start')
    done = cm._read(str(cp / ('iteration_%04d' % n) / 'COMPLETED.json'), 'iteration_completed')
    if start['iteration'] != n or done['converged'] is not True or done['iteration_start_sha256'] != start['payload_sha256']:
        raise ManifestRefusal('UV_TAIL_MANIFEST_NOT_CONVERGED_AT_ACCEPTED_ITERATION %d' % n)
    gas = cm._get(str(cp), start['gas_fourier_J'])
    sidecar = Path(uv['sidecar']['directory'])
    sid = json.loads((sidecar / 'SIDECAR_IDENTITY.json').read_text())['identity']
    records, elements = sidecar_elements(sidecar, n)
    data = prep.prepare_inputs(**seed['numerical_inputs'])
    ctl = ctl_mod.RouteATailController.from_prepared(galaxy='NGC3198', prep_module=prep, prep_arguments=seed['numerical_inputs'],
                                                     data=data, request=raw_request, sidecar_directory=None, libraries=libs)
    want = dict(ctl.static_identity, relaxation=float(sid['relaxation']), checkpoint_identity_sha256=ident['identity_sha256'])
    if json.loads(_canon(want)) != sid:
        diff = sorted(k for k in set(want) | set(sid) if json.loads(_canon(want.get(k))) != sid.get(k))
        raise ManifestRefusal('UV_TAIL_MANIFEST_CONTROLLER_IDENTITY_DIFFERS fields %s' % diff)
    st = rebuild_state(ctl, sidecar_identity=sid, elements=elements, n=n, gas=gas)
    expect = {'sidecar_iteration_payload': records[n]['state_digest'],
              'result_iterations_last': (uv.get('iterations') or [{}])[-1].get('state_digest'),
              'result_boundary_state_at_return': uv.get('boundary_state_digest_at_return')}
    if any(v != st.digest for v in expect.values()):
        raise ManifestRefusal('UV_TAIL_MANIFEST_STATE_NOT_REPRODUCED rebuilt %s expected %s' % (st.digest, expect))
    prov = dict(route_a_attempt=dict(result=str(rp.resolve()), result_sha256=rsha, accepted_iteration=n,
                                     flags=uv.get('flags'), monitor_status=uv.get('monitor_status'), M_T_accepted=uv.get('M_T_accepted')),
                checkpoint=dict(directory=str(cp.resolve()), identity_sha256=ident['identity_sha256']),
                sidecar=dict(directory=str(sidecar.resolve()), finish=uv['sidecar']['finish']),
                request=dict(path=str(Path(a.uv_tail_request).resolve()), sha256=a.uv_tail_request_sha256, normalized_sha256=req_norm['sha256']),
                prep=dict(path=str(Path(prep.__file__).resolve()), sha256=sha_file(prep.__file__)),
                reproduced=dict(expect, rebuilt=st.digest),
                eval_radii='route-A eval radii (gas columns + monitor probes + prediction stencil); other radii on demand')
    rec = write_outputs(a.outdir, controller=ctl, state=st, n=n, identity_sha256=ident['identity_sha256'],
                        start_payload_sha256=start['payload_sha256'], provenance=prov)
    _write_x(Path(a.outdir) / 'finish.json', dict(status='ROUTE_A_TAIL_MANIFEST_WRITTEN', elapsed_seconds=time.monotonic() - t0,
                                                   worker_sha256=sha_file(__file__), **rec))


if __name__ == '__main__':
    main()
