"""Seed v002 builder: NGC3198 route A at the A2 factor-10 anchor (diagnosis lane ngc_route_a_freeboundary_c2).

Rebuilds, from the existing packet's own bytes, (1) the route-A seed, (2) the serial launch request and
(3) the parallel N8/N3 launch requests, with
  (i)  the decisions provenance re-pinned to the CURRENT bytes of the V002 addendum (expected 17c26616...,
       fail-closed if the bytes differ from --expect-addendum-sha), optionally plus a frozen-decisions file
       (e.g. a V003 addendum) given by --frozen-decisions PATH, pinned from its bytes;
  (ii) an optional HI numerics override: --hi-search-limit-kpc, --hi-max-metric-calls, --hi-search-step-kpc
       (default = the current seed values 95.0 / 1024 / 0.2).
Nothing else in numerical_inputs changes (asserted). Nothing is launched.

Base inputs (all sha-pinned, read-only):
  seed      ngc_f10_c2/route_a_f10/seed/NGC3198_ROUTE_A_A2F10_SEED_C2V001.json            478a8467
  request   ngc_f10_c2/route_a_f10/launcher/NGC3198_ROUTE_A_A2F10_REQUEST_C2V001.json     9da3461b
  reviewed prep guards   ngc_route_impl_c2/route_a/tools/build_seed_v001.py              ca782709 (executed from bytes)
  parallel request builder ngc_f10_c2/route_a_f10_parallel/tools/build_par_files_c2v002.py acdb2825 (executed from
            bytes; its BASE_REQUEST/SERIAL_RUN/PAR_RUN/HERE globals re-pointed at the v002 serial request)
  install manifest ngc_route_impl_c2/route_a/install/INSTALL_MANIFEST_V001.json            d5dd50d4

CLI:
  build_seed_v002.py --variant NAME --serial-run RUN_NAME --par-run PAR_RUN_NAME [--frozen-decisions PATH]
                     [--expect-addendum-sha SHA] [--hi-search-limit-kpc X] [--hi-max-metric-calls N]
                     [--hi-search-step-kpc X] (--write | --verify | --dry)
  --write  writes seed_v002/<NAME>/{seed,launcher,route_b_spec}/... ('x' mode; --overwrite-own replaces this builder's
           own earlier outputs under seed_v002/<NAME>/ only)
  --verify rebuilds in memory and compares with the files on disk
  --dry    builds in memory only and prints the shas it would write
"""
import argparse
import copy
import hashlib
import json
import math
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent           # .../ngc_route_a_freeboundary_c2/seed_v002
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
R = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
C2 = R / 'CLAUDE2'
RUNS = C2 / 'runs'
BASE_SEED = (EX / 'ngc_f10_c2/route_a_f10/seed/NGC3198_ROUTE_A_A2F10_SEED_C2V001.json',
             '478a84676167457ccb3ac4e3d4e05bc452f57727259db8d95ead1652d7f5f981')
BASE_REQUEST = (EX / 'ngc_f10_c2/route_a_f10/launcher/NGC3198_ROUTE_A_A2F10_REQUEST_C2V001.json',
                '9da3461b62c9a28ef3443928a1bd6b626d11f87dfbe43c80e3b2932b13a55657')
REVIEWED_BUILDER = (EX / 'ngc_route_impl_c2/route_a/tools/build_seed_v001.py',
                    'ca78270928f81ed0482a85b7101fdce25707106c1aefa1dd1effa214fe02b2b4')
PAR_BUILDER = (EX / 'ngc_f10_c2/route_a_f10_parallel/tools/build_par_files_c2v002.py',
               'acdb28251b96d5d560290032eb7733c0e6da9979dccde849887aeb7f58e0ccea')
INSTALL_MANIFEST = (EX / 'ngc_route_impl_c2/route_a/install/INSTALL_MANIFEST_V001.json',
                    'd5dd50d40753f7f359d3ac4b8fbaae9b79c66056a9c6ce37516cd522de0f120e')
ADDENDUM = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V002_ADDENDUM.md'
ADDENDUM_OLD_SHA = '4070146dbd85c3cb6b6059d9ccc4f592ed9983520551fd682063fffbe1aa8b01'
ADDENDUM_EXPECTED = '17c2661603488478bafe2988e34e5c7b311bc7d8f6100fe75612b0c43f32648e'
HI_KEYS = ('hi_search_limit_kpc', 'hi_max_metric_calls', 'hi_search_step_kpc')


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(Path(p).read_bytes())


def pinned(path, sha):
    raw = Path(path).read_bytes()
    if sha_bytes(raw) != sha:
        raise SystemExit('PIN MISMATCH %s' % path)
    return raw


def exec_pinned(path, sha, name):
    raw = pinned(path, sha)
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


def dump(obj):
    return (json.dumps(obj, indent=1, allow_nan=False) + '\n').encode()


def json_diff(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            p = path + '/' + str(k)
            if k not in a:
                out.append((p, '<absent>', b[k]))
            elif k not in b:
                out.append((p, a[k], '<absent>'))
            else:
                out += json_diff(a[k], b[k], p)
        return out
    if type(a) is not type(b) or a != b:
        return [(path, a, b)]
    return []


def argv_set(argv, flag, value):
    if argv.count(flag) != 1:
        raise SystemExit('flag count ' + flag)
    a = list(argv)
    a[a.index(flag) + 1] = value
    return a


def calls_at_limit(limit_kpc, step_kpc):
    # the packet's counted formula (build_seed_f10_v001.py:207; dryrun_route_a_f10_v001.py d4 hi_budget)
    return 67 + 2 * math.ceil(limit_kpc / step_kpc - 1e-12)


def variant_paths(name):
    d = ROOT / name
    return {'dir': d,
            'seed': d / 'seed' / ('NGC3198_ROUTE_A_A2F10_SEED_C2V002_%s.json' % name),
            'seed_diff': d / 'seed' / ('SEED_DIFF_C2V002_%s.json' % name),
            'request': d / 'launcher' / ('NGC3198_ROUTE_A_A2F10_REQUEST_C2V002_%s.json' % name)}


def build_seed(a):
    raw = pinned(*BASE_SEED)
    base = json.loads(raw)
    seed = copy.deepcopy(base)
    add_raw = ADDENDUM.read_bytes()
    add_sha = sha_bytes(add_raw)
    if add_sha != a.expect_addendum_sha:
        raise SystemExit('V002 addendum bytes are %s, expected %s (decisions not frozen as stated)' % (add_sha, a.expect_addendum_sha))
    pins = dict(seed['pins'])
    if pins.get(str(ADDENDUM)) != ADDENDUM_OLD_SHA:
        raise SystemExit('base seed does not pin the V002 addendum at 4070146d')
    pins[str(ADDENDUM)] = add_sha
    seed['decision_refs']['addendum_v002'] = {'path': str(ADDENDUM), 'sha256': add_sha}
    frozen = None
    if a.frozen_decisions:
        fp = Path(a.frozen_decisions).resolve()
        frozen = {'path': str(fp), 'sha256': sha_file(fp)}
        pins[str(fp)] = frozen['sha256']
        seed['decision_refs']['frozen_decisions'] = frozen
    seed['pins'] = pins
    ni = seed['numerical_inputs']
    over = {'hi_search_limit_kpc': a.hi_search_limit_kpc, 'hi_max_metric_calls': a.hi_max_metric_calls,
            'hi_search_step_kpc': a.hi_search_step_kpc}
    changed = []
    for k, v in over.items():
        if v is None:
            continue
        if type(v) is not type(ni[k]):
            raise SystemExit('override %s type %s differs from seed type %s' % (k, type(v).__name__, type(ni[k]).__name__))
        if v != ni[k]:
            changed.append(k)
            seed['parameter_provenance'][k] = ('SEED_V002_NUMERICS_OVERRIDE (variant %s): %r -> %r; counted numerics; '
                                               'requires a root decision before launch (diagnosis ngc_route_a_freeboundary_c2 '
                                               'DIAGNOSIS_V001 option a); previous provenance: %s'
                                               % (a.variant, ni[k], v, base['parameter_provenance'].get(k)))
            ni[k] = v
    calls = calls_at_limit(ni['hi_search_limit_kpc'], ni['hi_search_step_kpc'])
    if calls > ni['hi_max_metric_calls']:
        raise SystemExit('hi calls at limit %d exceed hi_max_metric_calls %d' % (calls, ni['hi_max_metric_calls']))
    seed['derived']['hi_metric_calls_at_limit'] = calls
    seed['status'] = ('C2V002_NGC3198_ROUTE_A_A2F10_SEED_%s (seed v002: decisions provenance re-pinned to current bytes; '
                      'HI numerics %s); target-free; NOT LAUNCHED' % (a.variant, 'changed: ' + ','.join(changed) if changed else 'unchanged'))
    seed['seed_v002'] = {'base_seed': {'path': str(BASE_SEED[0]), 'sha256': BASE_SEED[1]},
                         'builder': {'path': str(Path(__file__).resolve()), 'sha256': sha_file(__file__)},
                         'addendum_v002': {'path': str(ADDENDUM), 'sha256_previous': ADDENDUM_OLD_SHA, 'sha256_now': add_sha},
                         'frozen_decisions': frozen, 'numerics_overrides_changed': changed,
                         'hi_numerics': {k: ni[k] for k in HI_KEYS}, 'hi_metric_calls_at_limit': calls}
    # ---- closed-list assertions
    d_ni = sorted(p for p, _, _ in json_diff(base['numerical_inputs'], seed['numerical_inputs']))
    if d_ni != sorted('/' + k for k in changed):
        raise SystemExit('numerical_inputs changed beyond the overrides: %s' % d_ni)
    allowed_top = {'status', 'numerical_inputs', 'pins', 'parameter_provenance', 'decision_refs', 'derived', 'seed_v002'}
    top = {p.split('/')[1] for p, _, _ in json_diff(base, seed)}
    if not top <= allowed_top:
        raise SystemExit('unexpected top-level change: %s' % sorted(top - allowed_top))
    for p, h in seed['pins'].items():
        if sha_file(p) != h:
            raise SystemExit('seed pin does not verify from bytes: ' + p)
    rb = exec_pinned(*REVIEWED_BUILDER, 'c2v001_reviewed_build_seed_v001')
    ok, nodes = rb.prep_grid_guards(ni)
    guards = {'seed_keys_equal_prep_signature': set(ni) == rb.prep_signature(), 'prep_grid_integer_guards_pass': ok,
              'axis_nodes': nodes, 'hi_calls_at_limit': calls, 'hi_calls_within_cap': calls <= ni['hi_max_metric_calls'],
              'binding_preconditions': ni['analytic_initial_azimuth'] is True and ni['composite_grid_spec'] is not None
                                       and ni['progress_directory'] is None,
              'all_seed_pins_verify_from_bytes': True}
    if not all(v for k, v in guards.items() if k not in ('axis_nodes', 'hi_calls_at_limit')):
        raise SystemExit('guard failure %s' % guards)
    diff = {'schema': 'NGC3198_ROUTE_A_A2F10_SEED_DIFF_C2V002', 'variant': a.variant,
            'base_seed': {'path': str(BASE_SEED[0]), 'sha256': BASE_SEED[1]},
            'numerical_inputs_changed': d_ni,
            'all_leaf_changes': [{'path': p, 'from': x, 'to': y} for p, x, y in json_diff(base, seed)
                                 if not p.startswith('/seed_v002')],
            'prep_guards_reviewed_functions': {'builder': {'path': str(REVIEWED_BUILDER[0]), 'sha256': REVIEWED_BUILDER[1]},
                                               'results': guards}}
    return seed, diff


def build_request(seed_path, seed_sha, outdir, note):
    raw = pinned(*BASE_REQUEST)
    pinned(*INSTALL_MANIFEST)
    base = json.loads(raw)
    if dump(base) != raw:
        raise SystemExit('base request not reproduced by the serializer')
    req = copy.deepcopy(base)
    a = argv_set(req['argv'], '--seed', str(seed_path))
    a = argv_set(a, '--seed-sha256', seed_sha)
    a = argv_set(a, '--outdir', str(outdir))
    a = argv_set(a, '--checkpoint-directory', str(outdir / 'checkpoint'))
    req['argv'] = a
    req['launch_pins']['seed'] = {'path': str(seed_path), 'sha256': seed_sha}
    req['note'] = note
    man = json.loads(Path(INSTALL_MANIFEST[0]).read_bytes())
    by_key = {f['key']: f for f in man['files']}
    for k, v in req['launch_pins'].items():
        if k != 'seed' and sha_file(v['path']) != v['sha256']:
            raise SystemExit('pin does not verify: ' + k)
        if k in by_key and (by_key[k]['installed_path'] != v['path'] or by_key[k]['sha256'] != v['sha256']):
            raise SystemExit('pin differs from install manifest: ' + k)
    changed = sorted(k for k in set(base) | set(req) if base.get(k) != req.get(k))
    if changed != ['argv', 'launch_pins', 'note']:
        raise SystemExit('unexpected request changes: %s' % changed)
    if [k for k in base['launch_pins'] if base['launch_pins'][k] != req['launch_pins'][k]] != ['seed']:
        raise SystemExit('launch_pins changed beyond seed')
    diff_argv = [i for i, (x, y) in enumerate(zip(base['argv'], req['argv'])) if x != y]
    if len(base['argv']) != len(req['argv']) or [base['argv'][i - 1] for i in diff_argv] != \
            ['--seed', '--seed-sha256', '--outdir', '--checkpoint-directory']:
        raise SystemExit('argv changed beyond seed/outdir/checkpoint')
    return dump(req)


def build_par(variant_dir, serial_request_path, serial_request_bytes, serial_run, par_run, n):
    pb = exec_pinned(*PAR_BUILDER, 'c2v002_par_builder')
    pb.BASE_REQUEST = (Path(serial_request_path), sha_bytes(serial_request_bytes))
    # pb.SERIAL_RUN stays 'NGC3198_ROUTE_A_A2F10_RUN_V001': it is the run name INSIDE the base route-B template
    # bbb37ca6 that the PAR template copy replaces; the serial v002 run name is carried by the serial request.
    if pb.SERIAL_RUN != 'NGC3198_ROUTE_A_A2F10_RUN_V001':
        raise SystemExit('unexpected base template run name')
    pb.PAR_RUN = par_run
    pb.HERE = variant_dir
    pb.OUT_TEMPLATE = variant_dir / 'route_b_spec/CALL_NGC3198_ROUTE_B_A2F10_PAR_TEMPLATE_C2V006.json'
    # pb.build reads BASE_REQUEST from disk: the serial request must already be on disk with these bytes
    if Path(serial_request_path).read_bytes() != serial_request_bytes:
        raise SystemExit('serial request on disk differs from the build')
    req, tpl, diff = pb.build(n)
    return pb.out_request(n), req, pb.out_diff(n), diff, pb.OUT_TEMPLATE, tpl


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--variant', required=True)
    ap.add_argument('--serial-run', required=True)
    ap.add_argument('--par-run', required=True)
    ap.add_argument('--frozen-decisions')
    ap.add_argument('--expect-addendum-sha', default=ADDENDUM_EXPECTED)
    ap.add_argument('--hi-search-limit-kpc', type=float)
    ap.add_argument('--hi-max-metric-calls', type=int)
    ap.add_argument('--hi-search-step-kpc', type=float)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--write', action='store_true')
    g.add_argument('--verify', action='store_true')
    g.add_argument('--dry', action='store_true')
    ap.add_argument('--overwrite-own', action='store_true', help='with --write: replace files this builder wrote earlier under seed_v002/<variant>/')
    a = ap.parse_args(argv)
    mode = 'wb' if a.overwrite_own else 'xb'
    if not a.variant.replace('_', '').isalnum():
        raise SystemExit('variant must be alphanumeric/underscore')
    for run in (a.serial_run, a.par_run):
        if '/' in run or (RUNS / run).exists():
            raise SystemExit('run name must be new under CLAUDE2/runs: %s' % run)
    vp = variant_paths(a.variant)
    seed, sdiff = build_seed(a)
    seed_b = dump(seed)
    seed_sha = sha_bytes(seed_b)
    sdiff['outputs'] = {'seed': {'path': str(vp['seed']), 'sha256': seed_sha}}
    note = ('NGC3198 route A, A2 FACTOR-10 anchor (A0), N1 GL4 primary, seed v002 variant %s (decisions provenance '
            're-pinned; HI numerics %s). New checkpoint, iteration 0. NOT LAUNCHED by the builder.'
            % (a.variant, json.dumps(seed['seed_v002']['hi_numerics'], sort_keys=True)))
    req_b = build_request(vp['seed'], seed_sha, RUNS / a.serial_run, note)
    outs = [(vp['seed'], seed_b), (vp['request'], req_b)]
    if a.dry:
        for p, b in outs:
            print(sha_bytes(b), p, '(not written)')
        print('PAR requests need the serial request on disk; run --write to build them')
        return 0
    if a.write:
        for p, b in outs:
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, mode) as f:
                f.write(b)
    par = []
    for n in (8, 3):
        if a.write:
            # build_par re-reads the serial request from disk; under --write it was just written above
            pass
        rp, rb, dp, db, tp, tb = build_par(vp['dir'], vp['request'], req_b, a.serial_run, a.par_run, n)
        par += [(rp, rb), (dp, db)]
        tpl = (tp, tb)
    par.append(tpl)
    sdiff['outputs']['serial_request'] = {'path': str(vp['request']), 'sha256': sha_bytes(req_b)}
    sdiff['outputs']['par_files'] = {str(p): sha_bytes(b) for p, b in par}
    sd_b = dump(sdiff)
    allf = outs + par + [(vp['seed_diff'], sd_b)]
    if a.write:
        for p, b in par + [(vp['seed_diff'], sd_b)]:
            p.parent.mkdir(parents=True, exist_ok=True)
            if p == tpl[0] and p.exists() and p.read_bytes() == b:
                continue  # N-independent; identical bytes already written
            with open(p, mode) as f:
                f.write(b)
    ok = all(Path(p).read_bytes() == b for p, b in allf)
    for p, b in allf:
        print(sha_bytes(b), p)
    print('VERIFY', ok)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
