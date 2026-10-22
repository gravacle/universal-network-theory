"""Synthetic / simulate-mode tests for galaxy_m0_forward_c2v003b (no project stage is executed; no launch).
usage: python3 -I -B tests_c2v003b.py WORK_DIR   (WORK_DIR must be absent)
Writes WORK_DIR/TEST_RESULTS.json.  Run-mode tests replace subprocess.Popen by a no-op so the REAL
run_stages writes every request.json it would hand to a stage, and nothing is executed."""
import hashlib
import json
import math
import subprocess
import sys
import traceback
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRV_B = HERE / 'galaxy_m0_forward_c2v003b.py'
DRV_3 = HERE / 'galaxy_m0_forward_c2v003.py'
DRV_3_SHA = 'b052e3ae43fcf8782cc9cca99dec2cdc8f7fcbf479af7b92738feb196c00033b'
SPECS = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/specs')
WAVE1 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_prep_c2_0470/kmax_convergence/specs/wave1')
CAL_SPEC = (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_prep_c2_0470/calibration_spec/'
                 'DDO154_CALIBRATION_COORDINATE_SPEC_DRAFT_C2V001.json'),
            'a7709bd2a9ace5dc34ae31cb75b07f570ff39fcbbd99c6f4bbaa367eed620d54')
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
REG_SPECS = [SPECS / 'CALL_REPRO_PINNED_FULL_C2V001.json', SPECS / 'CALL_REPRO_PINNED_ADMIT_PREFIX_C2V001.json',
             SPECS / 'CALL_REPRO_RULE_FULL_C2V001.json', SPECS / 'CALL_EXAMPLE_CANDIDATE_SPHERE_C2V001.json',
             WAVE1 / 'CALL_KMAX_C2_C2V001.json', WAVE1 / 'CALL_KMAX_C3_C2V001.json', WAVE1 / 'CALL_KMAX_C4_C2V001.json',
             WAVE1 / 'CALL_KMAX_R_C2V001.json']
D_LO, D_HI = 3.9810717055349722, 4.111497211045223  # calibration-spec distance box (checked in t10)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(path, name, expected=None):
    raw = Path(path).read_bytes()
    if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
        raise AssertionError('pin mismatch ' + str(path))
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


B = load(DRV_B, 'drv3b')
V3 = load(DRV_3, 'drv3', DRV_3_SHA)
RESULTS = []


def test(fn):
    def run(work):
        try:
            detail = fn(work)
            RESULTS.append({'test': fn.__name__, 'pass': True, 'detail': detail})
        except Exception as exc:
            RESULTS.append({'test': fn.__name__, 'pass': False, 'error': '%s: %s' % (type(exc).__name__, exc),
                            'traceback': traceback.format_exc()})
    run.__name__ = fn.__name__
    return run


def jl(p):
    return json.loads(Path(p).read_text())


def refused(fn, *a):
    try:
        fn(*a)
    except Exception as exc:  # Refusal/Blocked of either driver module (distinct classes per module)
        if type(exc).__name__ not in ('Refusal', 'Blocked'):
            raise
        return str(exc)
    raise AssertionError('not refused')


def spec_with(base, **phys):
    s = jl(base)
    s['physical'] = dict(s['physical'], **phys)
    return s


def pinned(key):
    return json.loads(Path(B.GALAXIES['DDO154'][key][0]).read_bytes())


def bitwise_equal(a, b):
    """Exact equality with float bits compared (66 == 66.0 counts as equal: same value, JSON int vs float)."""
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(bitwise_equal(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(bitwise_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, float) or isinstance(b, float):
        return float(a).hex() == float(b).hex()
    return a == b


# ----------------------------------------------------------------------------------------- derivation
@test
def t01_registered_derivation_reproduces_pinned_files(work):
    """derive_geometry at 4.04 Mpc / 66 deg reproduces every field of the pinned DDO154 profile record, the
    pinned monotone source (via the reviewed reducer) and the pinned column-mean binding, bitwise."""
    prof, mono, bind, rec = B.derive_geometry('DDO154', 4.04, 66.0)
    assert all(rec['registered_formula_guards'].values()), rec['registered_formula_guards']
    P = pinned('profile')
    for sec in ('HI_plus_He', 'stellar_reference', 'geometry'):
        assert bitwise_equal(prof['galaxies']['DDO154'][sec], P['galaxies']['DDO154'][sec]), sec
    assert bitwise_equal(prof['galaxies'], P['galaxies'])
    assert sorted(set(prof) - set(P)) == ['c2_geometry'] and all(bitwise_equal(prof[k], P[k]) for k in P)
    S = pinned('monotone_source')
    assert sorted(k for k in set(S) | set(mono) if not bitwise_equal(S.get(k), mono.get(k))) == ['c2_geometry', 'input']
    Bd = pinned('column_mean_binding')
    # source_profile is re-pointed to the per-call profile only when the files are written (geometry_inputs)
    assert sorted(k for k in set(Bd) | set(bind) if not bitwise_equal(Bd.get(k), bind.get(k))) == ['c2_geometry']
    assert rec['monotone_controls_bitwise_equal_to_registered'] is True
    return {'guards': rec['registered_formula_guards'], 'profile_sections_bitwise': ['HI_plus_He', 'stellar_reference', 'geometry'],
            'monotone_keys_reproduced': sorted(set(S) - {'input'}), 'binding_keys_reproduced': sorted(set(Bd) - {'source_profile'})}


@test
def t02_scaling_laws_across_distance(work):
    """At D != 4.04: every source/query length x D/4.04 (gas via lambda=D/4.3), surface densities and the
    monotone controls bitwise unchanged, masses x (D/4.04)^2, inclination quantities unchanged."""
    P = pinned('profile')['galaxies']['DDO154']
    Bd = pinned('column_mean_binding')
    S = pinned('monotone_source')
    out = {}
    for D in (D_LO, D_HI, 3.0, 5.5):
        prof, mono, bind, rec = B.derive_geometry('DDO154', D, 66.0)
        n = prof['galaxies']['DDO154']
        mu = D / 4.04
        rel = lambda a, b, p=1: abs(a / b / mu ** p - 1)
        gas, star = n['HI_plus_He'], n['stellar_reference']
        e = gas['s_edges_kpc2']
        assert e[0] == 0.0 and len(e) == 19
        mx = {'edge_radius': max(rel(math.sqrt(a), math.sqrt(b)) for a, b in zip(e[1:], P['HI_plus_He']['s_edges_kpc2'][1:])),
              'star_radius': max(rel(a, b) for a, b in zip(star['radius_kpc'], P['stellar_reference']['radius_kpc'])),
              'outer_scale': rel(star['outer_scale_kpc'], P['stellar_reference']['outer_scale_kpc']),
              'height': rel(star['height_kpc'], P['stellar_reference']['height_kpc']),
              'support': rel(gas['support_radius_kpc'], P['HI_plus_He']['support_radius_kpc']),
              'query_radius': max(rel(a['radius_m'], b['radius_m']) for a, b in zip(bind['query_rows'], Bd['query_rows'])),
              'gas_mass': rel(gas['integrated_mass_Msun'], P['HI_plus_He']['integrated_mass_Msun'], 2),
              'gas_mass_original': rel(gas['original_retained_mass_scaled_Msun'], P['HI_plus_He']['original_retained_mass_scaled_Msun'], 2),
              'star_mass': rel(star['total_reference_stellar_mass_Msun'], P['stellar_reference']['total_reference_stellar_mass_Msun'], 2),
              'midplane': max(rel(a, b, -1) for a, b in zip(star['midplane_density_Msun_pc3'], P['stellar_reference']['midplane_density_Msun_pc3']))}
        assert max(mx.values()) < 2e-15, mx
        for k in ('annular_means_Msun_pc2', 'boundary_controls_Msun_pc2', 'middle_controls_Msun_pc2'):
            assert bitwise_equal(gas[k], P['HI_plus_He'][k]), k
        assert bitwise_equal(star['surface_density_Msun_pc2'], P['stellar_reference']['surface_density_Msun_pc2'])
        for k in ('boundary_controls_Msun_pc2', 'middle_controls_Msun_pc2', 'annular_means_Msun_pc2'):
            assert bitwise_equal(mono['source_record'][k], S['source_record'][k]), k
        assert mono['source_record']['s_edges_kpc2'] == e and mono['status'] == S['status']
        assert gas['relative_mass_pairing_difference'] < 1e-15
        assert bind['physical_inclination_rad'] == Bd['physical_inclination_rad'] and bind['released_inclination_rad'] == Bd['released_inclination_rad']
        assert n['geometry']['stellar_faceon_factor_from_64deg'] == P['geometry']['stellar_faceon_factor_from_64deg']
        assert n['geometry']['distance_Mpc'] == D and n['geometry']['radial_distance_scale'] == D / 4.3
        assert bitwise_equal(prof['galaxies']['NGC3198'], pinned('profile')['galaxies']['NGC3198'])
        # route-B radial roster as built by prep/reference/body (GL4 in s=R^2): 72 radii, each x mu
        import numpy as np
        gx, _ = np.polynomial.legendre.leggauss(4)
        R = [math.sqrt((lo + hi) / 2 + (hi - lo) * x / 2) for lo, hi in zip(e, e[1:]) for x in gx]
        R0 = [math.sqrt((lo + hi) / 2 + (hi - lo) * x / 2) for lo, hi in zip(P['HI_plus_He']['s_edges_kpc2'], P['HI_plus_He']['s_edges_kpc2'][1:]) for x in gx]
        assert len(R) == 72 and max(rel(a, b) for a, b in zip(R, R0)) < 1e-14
        out[repr(D)] = dict(mx, mu=mu, lam=rec['hi_lambda_D_over_4p3'], monotone_sweeps=mono['diagnostics']['sweeps'])
    return out


@test
def t03_spec_acceptance_and_inclination_blocker(work):
    base = SPECS / 'CALL_REPRO_PINNED_FULL_C2V001.json'
    out = {}
    for D in (D_LO, D_HI, 4.04, 3.0):
        ns = B.normalize_spec(spec_with(base, distance_Mpc=D))
        assert ns['physical']['distance_Mpc'] == D and B.geometry_active(ns) == (D != 4.04)
    for bad in (0, -1.0, '4.04', float('inf'), True):
        out['distance_%r' % (bad,)] = refused(B.normalize_spec, spec_with(base, distance_Mpc=bad))
    for i in (61.0, 64.0, 67.0, 65.999):
        msg = refused(B.normalize_spec, spec_with(base, inclination_deg=i))
        assert 'BLOCKED_GAS_REDEPROJECTION' in msg, msg
        out['inclination_%r' % i] = msg[:120]
    assert not B.geometry_active(B.normalize_spec(spec_with(base, inclination_deg=66)))
    assert 'BLOCKED_GAS_REDEPROJECTION' in refused(B.derive_geometry, 'DDO154', 4.04, 64.0)
    # v003 refuses every non-registered distance; v003b accepts it (the only acceptance change)
    assert 'UNSUPPORTED geometry' in refused(V3.normalize_spec, spec_with(base, distance_Mpc=D_HI))
    for p in REG_SPECS:
        assert V3.normalize_spec(jl(p)) == B.normalize_spec(jl(p)), p.name
    return out


@test
def t10_calibration_spec_trial_point_is_registered(work):
    cs = json.loads(Path(CAL_SPEC[0]).read_bytes())
    assert sha(CAL_SPEC[0]) == CAL_SPEC[1]
    c = {x['name']: x for x in cs['coordinates']}
    d, i = c['distance_Mpc'], c['inclination_deg']
    assert (d['transform'], d['trial_value'], d['lower'], d['upper']) == ('log', 4.04, D_LO, D_HI)
    assert (i['transform'], i['trial_value']) == ('linear', 66.0)
    ns = B.normalize_spec(spec_with(SPECS / 'CALL_REPRO_PINNED_FULL_C2V001.json', distance_Mpc=d['trial_value'], inclination_deg=i['trial_value']))
    assert not B.geometry_active(ns)
    edges = {}
    for v in (i['lower'], i['upper']):
        edges[repr(v)] = 'BLOCKED_GAS_REDEPROJECTION' in refused(B.normalize_spec, spec_with(SPECS / 'CALL_REPRO_PINNED_FULL_C2V001.json', inclination_deg=v))
    return {'distance': {k: d[k] for k in ('transform', 'trial_value', 'lower', 'upper')}, 'trial_point_geometry_active': False,
            'inclination_box_edges_refused': edges}


# ----------------------------------------------------------------------------------------- registered identity
def dry(driver, spec, rd):
    p = subprocess.run([PY, '-I', '-B', str(driver), 'dry-run', '--spec', str(spec), '--report-dir', str(rd)],
                       capture_output=True, text=True, env=B.single_thread_env())
    Path(str(rd) + '.stdout.txt').write_text(p.stdout + '\n--- stderr ---\n' + p.stderr)
    return p


def norm_report(rd):
    raw = (Path(rd) / 'DRYRUN_REPORT.json').read_text().replace(str(rd), '$DRY')
    manifests = {}
    for m in sorted((Path(rd) / 'simulated_call' / 'inputs').glob('*')):
        if m.is_file():
            manifests[sha(m)] = 'INPUT_' + hashlib.sha256(m.read_bytes().decode().replace(str(rd), '$DRY').encode()).hexdigest()[:16]
    for k, v in manifests.items():
        raw = raw.replace(k, v)
    r = json.loads(raw)
    drv = r.pop('driver_sha256')
    plan = (Path(rd) / 'DRYRUN_PLAN.txt').read_text().replace(str(rd), '$DRY')
    for k, v in manifests.items():
        plan = plan.replace(k, v)
    return r, drv, plan


@test
def t04_registered_dryrun_reports_identical_to_v003(work):
    """Simulate mode, every shipped DDO154 spec at the registered geometry: the WHOLE dry-run report (stages,
    identity, pins, summary, simulated final rows) and DRYRUN_PLAN.txt are identical between v003 and v003b
    after normalizing only the report-dir prefix; driver_sha256 is the sole difference."""
    out = {}
    for p in REG_SPECS:
        tag = p.name.replace('CALL_', '').replace('_C2V001.json', '')
        a, b = Path(work) / ('t04_v003_' + tag), Path(work) / ('t04_v003b_' + tag)
        pa, pb = dry(DRV_3, p, a), dry(DRV_B, p, b)
        assert pa.returncode == 0 and pb.returncode == 0, (tag, pa.stderr[-800:], pb.stderr[-800:])
        ra, da, la = norm_report(a)
        rb, db, lb = norm_report(b)
        assert da == DRV_3_SHA and db == sha(DRV_B)
        assert ra == rb, (tag, [k for k in set(ra) | set(rb) if ra.get(k) != rb.get(k)])
        assert la == lb, tag
        assert ra['executed_stages'] == 0
        out[tag] = {'stages': len(ra['stages']), 'repro_like': ra['summary']['repro_like'],
                    'final_rows': bool(ra.get('final_rows_from_saved_chain')), 'report_v003b_sha256': sha(b / 'DRYRUN_REPORT.json')}
    # NGC spec: identical refusal
    ngc = SPECS / 'CALL_NGC3198_SEED_C2V002.json'
    ma = refused(V3.normalize_spec, jl(ngc))
    mb = refused(B.normalize_spec, jl(ngc))
    assert ma == mb
    out['NGC3198_refusal_identical'] = True
    return out


class FakePopen:
    """No-op stand-in for subprocess.Popen: the real run_stages writes request.json, nothing executes."""
    calls = []

    def __init__(self, argv, **kw):
        FakePopen.calls.append(list(map(str, argv)))
        self.pid = 0

    def wait(self):
        return 0


def fake_run(driver_mod, spec_obj, outdir):
    sp = Path(str(outdir) + '.spec.json')
    sp.write_text(json.dumps(spec_obj))
    real = subprocess.Popen
    subprocess.Popen = FakePopen
    try:
        code = driver_mod.cmd_run(str(sp), str(outdir))
    finally:
        subprocess.Popen = real
    return code


VOLATILE = ('elapsed_seconds', 'utc', 'pid', 'driver_sha256', 'driver')  # 'driver' = the driver file path (start.json)


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in VOLATILE}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o


def normalizer(outdir):
    """Text normalizer for one run dir: outdir prefix -> $OUT, and the sha256 of every file the run wrote
    (whose bytes embed the outdir path) -> a token of its normalized content.  Inputs first, then requests."""
    M = {}

    def nt(t):
        t = t.replace(str(outdir), '$OUT')
        for k, v in M.items():
            t = t.replace(k, v)
        return t
    groups = [sorted(f for f in (Path(outdir) / 'inputs').rglob('*') if f.is_file()) if (Path(outdir) / 'inputs').is_dir() else [],
              sorted(Path(outdir).glob('stages/*/request.json'))]
    for grp in groups:
        for f in grp:
            M[sha(f)] = 'FILE_' + hashlib.sha256(nt(f.read_text()).encode()).hexdigest()[:16]
    return nt


def run_tree(outdir):
    """Every file the run wrote (requests, inputs, start/result/finish) normalized by normalizer();
    JSON records with volatile keys removed.  progress.jsonl/stdout/stderr excluded (timings, pids)."""
    tree = {}
    nt = normalizer(outdir)
    for f in sorted(Path(outdir).rglob('*')):
        if not f.is_file() or f.name in ('progress.jsonl', 'stdout.txt', 'stderr.txt'):
            continue
        txt = nt(f.read_text())
        rel = str(f.relative_to(outdir))
        if f.name in ('start.json', 'result.json', 'finish.json'):
            obj = strip(json.loads(txt))
            if f.name == 'finish.json':
                obj.pop('result_sha256', None)
            tree[rel] = obj
        else:
            tree[rel] = txt
    return tree


@test
def t05_registered_run_mode_files_identical_to_v003(work):
    """Run mode with subprocess.Popen replaced by a no-op: every request.json, generated input and the
    start/result/finish records written by v003 and v003b are identical (outdir prefix and timing keys
    normalized).  Same stage commands."""
    out = {}
    for p in (SPECS / 'CALL_REPRO_PINNED_FULL_C2V001.json', SPECS / 'CALL_REPRO_RULE_FULL_C2V001.json',
              SPECS / 'CALL_EXAMPLE_CANDIDATE_SPHERE_C2V001.json', WAVE1 / 'CALL_KMAX_C2_C2V001.json', WAVE1 / 'CALL_KMAX_C3_C2V001.json'):
        tag = p.name.replace('CALL_', '').replace('_C2V001.json', '')
        a, b = Path(work) / ('t05_v003_' + tag), Path(work) / ('t05_v003b_' + tag)
        FakePopen.calls = []
        ca = fake_run(V3, jl(p), a)
        calls_a = [[x.replace(str(a), '$OUT') for x in c[:3] + c[4:]] for c in FakePopen.calls]
        FakePopen.calls = []
        cb = fake_run(B, jl(p), b)
        calls_b = [[x.replace(str(b), '$OUT') for x in c[:3] + c[4:]] for c in FakePopen.calls]
        ta, tb = run_tree(a), run_tree(b)
        assert ca == cb and calls_a == calls_b and len(calls_a) > 0, tag
        assert sorted(ta) == sorted(tb), (tag, sorted(set(ta) ^ set(tb)))
        bad = [k for k in ta if ta[k] != tb[k]]
        assert not bad, (tag, bad)
        assert not any('geometry' in k for k in tb), tag
        out[tag] = {'exit': ca, 'status': tb['result.json']['status'], 'requests': sum(1 for k in tb if k.endswith('request.json')),
                    'files_compared': len(tb)}
    return out


# ----------------------------------------------------------------------------------------- active geometry
GEO_GLOBALS = ('PROFILE', 'PROFILE_SHA', 'SOURCE', 'SOURCE_SHA')


def scrub_geometry(req, reg_req):
    """Remove exactly the c2v003b geometry inputs from an active-geometry request (restoring the registered
    values where an existing entry is re-pointed)."""
    r = json.loads(json.dumps(req))
    for k in GEO_GLOBALS:
        r['stage_globals'].pop(k, None)
    for p in r['module_patches']:
        for k in GEO_GLOBALS + ('C',):
            p['set'].pop(k, None)
    r['module_patches'] = [p for p in r['module_patches'] if p['set']]
    if 'DATA_PINS' in r['stage_globals']:
        r['stage_globals']['DATA_PINS']['__pathdict__'][2] = reg_req['stage_globals']['DATA_PINS']['__pathdict__'][2]
    if 'PINS' in r['stage_globals']:
        r['stage_globals']['PINS']['__ordered__'][0] = reg_req['stage_globals']['PINS']['__ordered__'][0]
    return r


@test
def t06_active_run_mode_requests_differ_only_in_geometry_inputs(work):
    """Run mode (no-op Popen) at D = box upper/lower edge: the geometry files are written under inputs/,
    every request differs from the registered request ONLY by the geometry inputs, and each geometry input
    points at the per-call file with its sha computed from bytes."""
    out = {}
    for p in (SPECS / 'CALL_REPRO_PINNED_FULL_C2V001.json', WAVE1 / 'CALL_KMAX_C2_C2V001.json'):
        tag = p.name.replace('CALL_', '').replace('_C2V001.json', '')
        reg = Path(work) / ('t06_reg_' + tag)
        fake_run(B, jl(p), reg)
        for D in (D_HI, D_LO):
            act = Path(work) / ('t06_D%.4f_%s' % (D, tag))
            code = fake_run(B, spec_with(p, distance_Mpc=D), act)
            res = jl(act / 'result.json')
            geo = res['identity']['geometry']
            files = geo['files']
            for key in ('profile', 'source_binding_v003_copy', 'monotone_source', 'column_mean_binding'):
                assert sha(files[key][0]) == files[key][1], key
            assert files['source_binding_v003_copy'][1] == B.GEOMETRY_PINS['source_binding_v003'][1]
            assert Path(files['profile'][0]).parent == Path(files['C_directory']) and Path(files['profile'][0]).name == B.PROFILE_NAME
            assert jl(files['monotone_source'][0])['input'] == {'path': files['profile'][0], 'sha256': files['profile'][1], 'record': 'galaxies.DDO154.HI_plus_He'}
            assert jl(files['column_mean_binding'][0])['source_profile'] == {'path': files['profile'][0], 'sha256': files['profile'][1]}
            reqs_a = sorted(act.glob('stages/*/request.json'))
            reqs_r = sorted(reg.glob('stages/*/request.json'))
            assert [x.parent.name for x in reqs_a] == [x.parent.name for x in reqs_r]
            nta, ntr = normalizer(act), normalizer(reg)
            seen = {}
            for fa, fr in zip(reqs_a, reqs_r):
                ra = json.loads(nta(fa.read_text()))
                rr = json.loads(ntr(fr.read_text()))
                raw = jl(fa)
                name = raw['name']
                kind = raw['kind']
                sg = raw['stage_globals']
                pat = {k: v for mp in raw['module_patches'] for k, v in mp['set'].items()}
                if kind == 'route_a':
                    prep = [mp for mp in raw['module_patches'] if mp['path'] == str(B.AUX['prep'][0])]
                    assert len(prep) == 1 and prep[0]['set']['C'] == {'__path__': files['C_directory']}
                if kind == 'reference':
                    assert sg['PROFILE'] == {'__path__': files['profile'][0]} and sg['PROFILE_SHA'] == files['profile'][1]
                if kind in ('body', 'offset') or kind.startswith(('columns', 'rotation', 'feedback')):
                    assert pat['PROFILE'] == {'__path__': files['profile'][0]} and pat['PROFILE_SHA'] == files['profile'][1], name
                if kind == 'body':
                    assert sg['SOURCE'] == {'__path__': files['monotone_source'][0]}
                    assert sg['DATA_PINS']['__pathdict__'][2] == files['monotone_source']
                if kind.startswith('rotation'):
                    assert sg['SOURCE'] == {'__path__': files['monotone_source'][0]} and sg['SOURCE_SHA'] == files['monotone_source'][1], name
                else:
                    assert 'SOURCE_SHA' not in sg and (kind == 'body' or 'SOURCE' not in sg), name  # feedback SOURCE is a module: untouched
                if kind == 'column_mean_v004':
                    assert sg['PINS']['__ordered__'][0] == files['column_mean_binding']
                assert scrub_geometry(ra, rr) == rr, name
                seen[kind] = seen.get(kind, 0) + 1
            out['%s D=%r' % (tag, D)] = {'exit': code, 'status': res['status'], 'requests_checked': len(reqs_a), 'kinds': seen,
                                         'route_a_rows_scope_present': 'route_a_rows_scope' in res['identity']['route_a'] or 'not reached (fake stages)',
                                         'files': {k: v[1][:16] if isinstance(v, list) else v for k, v in files.items()}}
    return out


@test
def t07_active_dryrun_overrides_resolve(work):
    """Simulate-mode dry run at D = box edge: every geometry override targets an existing global
    (no OVERRIDE_TARGET_ABSENT), pins verify, no scipy, repro_like false (saved outputs not reused)."""
    out = {}
    for D in (D_HI, D_LO):
        sp = Path(work) / ('t07_spec_D%.4f.json' % D)
        sp.write_text(json.dumps(spec_with(SPECS / 'CALL_REPRO_PINNED_FULL_C2V001.json', distance_Mpc=D)))
        rd = Path(work) / ('t07_dry_D%.4f' % D)
        pr = dry(DRV_B, sp, rd)
        assert pr.returncode == 0, pr.stderr[-1500:]
        r = jl(rd / 'DRYRUN_REPORT.json')
        s = r['summary']
        assert s['repro_like'] is False and not s['pin_problems'] and not s['scipy_imports'] and r['executed_stages'] == 0
        verdicts = [o['verdict'] for st in r['stages'] for o in (st.get('override_comparison') or [])]
        assert 'OVERRIDE_TARGET_ABSENT' not in verdicts
        geo_ov = [(st['name'], o['where'], o['name'], o['verdict']) for st in r['stages'] for o in (st.get('override_comparison') or [])
                  if o['name'] in GEO_GLOBALS + ('C',)]
        assert all(v == 'PER_CALL_VALUE_DIFFERS_FROM_HARDCODED' for *_, v in geo_ov), geo_ov
        for k in B.GEOMETRY_PINS:
            assert str(B.GEOMETRY_PINS[k][0]) in r['static_pins']
        assert len([st for st in r['stages'] if st['kind'] == 'column_mean_v004']) == 3
        out[repr(D)] = {'stages': s['stages_planned'], 'geometry_overrides': len(geo_ov),
                        'distinct': sorted({(w, n) for _, w, n, _ in geo_ov}), 'overrides_wording': s['overrides_wording']}
    return out


TOY_STAGE = r'''
import importlib.util, json, sys, hashlib
from pathlib import Path
def load(p, name):
    s = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def main():
    prep = load(PREP, 'toy_prep'); reuse = load(REUSE, 'toy_reuse')
    c = Path(prep.C)
    out = {'C': str(c), 'COEFFICIENT': str(prep.COEFFICIENT), 'COEFFICIENT_SHA': prep.COEFFICIENT_SHA,
           'reuse_PROFILE': str(reuse.PROFILE), 'reuse_PROFILE_SHA': reuse.PROFILE_SHA,
           'profile_read_by_prep_sha256': hashlib.sha256((c / 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json').read_bytes()).hexdigest(),
           'binding_v003_read_by_prep_sha256': hashlib.sha256((c / 'GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json').read_bytes()).hexdigest()}
    Path(sys.argv[1]).write_text(json.dumps(out))
'''


@test
def t08_stage_shim_patches_real_prep_and_reuse(work):
    """The real _stage shim in a fresh -I -B process: a toy stage loads the REAL prep V007 and the REAL
    homotopy worker (inert imports) through spec_from_file_location; the module patches of an active-geometry
    route-A/body request redirect prep.C and reuse.PROFILE to the per-call files; COEFFICIENT is untouched."""
    act = sorted(Path(work).glob('t06_D4.1115_REPRO_PINNED_FULL'))[0]
    reqs = {jl(f)['kind']: jl(f) for f in sorted(act.glob('stages/*/request.json'))}
    files = jl(act / 'result.json')['identity']['geometry']['files']
    w = Path(work) / 't08'
    w.mkdir()
    toy = w / 'toy_stage.py'
    toy.write_text('PREP = %r\nREUSE = %r\n' % (str(B.AUX['prep'][0]), str(B.SCRIPTS['reference'][0])) + TOY_STAGE)
    req = {'script': str(toy), 'script_sha256': sha(toy), 'argv': [str(w / 'out.json')], 'stage_globals': {},
           'module_patches': reqs['route_a']['module_patches'] + reqs['body']['module_patches'], 'mask': None}
    rp = w / 'request.json'
    rp.write_text(json.dumps(req))
    p = subprocess.run([PY, '-I', '-B', str(DRV_B), '_stage', str(rp)], capture_output=True, text=True, cwd=str(w), env=B.single_thread_env())
    assert p.returncode == 0, p.stderr[-2000:]
    o = jl(w / 'out.json')
    assert o['C'] == files['C_directory']
    assert o['profile_read_by_prep_sha256'] == files['profile'][1]
    assert o['binding_v003_read_by_prep_sha256'] == B.GEOMETRY_PINS['source_binding_v003'][1]
    assert o['COEFFICIENT'] == str(B.GALAXIES['DDO154']['default_coefficients'][0])
    assert o['reuse_PROFILE'] == files['profile'][0] and o['reuse_PROFILE_SHA'] == files['profile'][1]
    return o


@test
def t09_admitted_outputs_must_match_call_geometry(work):
    """Admitted route-A/reference/body outputs built at the registered geometry are refused at another distance."""
    out = {}
    ns = B.normalize_spec(spec_with(SPECS / 'CALL_REPRO_PINNED_ADMIT_PREFIX_C2V001.json', distance_Mpc=D_HI))
    ctx = B.Ctx('simulate', ns, Path(work) / 't09_admit')
    try:
        B.execute_chain(ctx)
        raise AssertionError('admitted registered outputs accepted at D != 4.04')
    except B.Blocked as exc:
        out['admit_prefix'] = str(exc)
        assert 'ROUTE_A_GEOMETRY_MISMATCH' in str(exc)
    sv = B.GALAXIES['DDO154']['saved_runs']['route_a']['checkpoint']
    seed_path, seed_sha = B.GALAXIES['DDO154']['base_seed']
    phys = {k: jl(seed_path)['numerical_inputs'][k] for k in ('Eref_J', 'ell_F_m', 'gamma')}
    coeff = str(B.GALAXIES['DDO154']['default_coefficients'][0])
    B.route_a_custody(sv, seed_sha, coeff, phys, profile_sha=B.GALAXIES['DDO154']['profile'][1])
    out['saved_route_a_with_pinned_profile'] = 'accepted'
    out['saved_route_a_with_other_profile'] = refused(B.route_a_custody, sv, seed_sha, coeff, phys, 'f' * 64)
    # reference/body admit checks, exercised directly on the saved records
    ref = B.GALAXIES['DDO154']['saved_runs']['reference']
    body = B.GALAXIES['DDO154']['saved_runs']['body']
    assert jl(Path(ref) / 'start.json')['source_custody']['sha256'] == B.GALAXIES['DDO154']['profile'][1]
    assert B.GALAXIES['DDO154']['monotone_source'][1] in jl(Path(body) / 'start.json')['input_pins'].values()
    return out


@test
def t11_reviewed_prep_consumes_per_call_profile(work):
    """The REAL prep V007 prepare_inputs (in-process, tiny 8-node Gauss cube, analytic azimuth off: a synthetic
    evaluation, not the route-A stage) with module global C pointed at a per-call geometry_C directory:
    at 4.04 Mpc every prepared source array is bitwise equal to the pinned-C preparation; at the box edge the
    gas/stellar radii and positions scale by D/4.04, masses by (D/4.04)^2, gas surface densities unchanged."""
    import inspect
    import numpy as np
    seed = jl(B.GALAXIES['DDO154']['base_seed'][0])
    ni = dict(seed['numerical_inputs'], fourier_points_per_axis=8, composite_grid_spec=None, analytic_initial_azimuth=False)

    def prep_with(cdir):
        m = load(B.AUX['prep'][0], 'prep_t11', B.AUX['prep'][1])
        if cdir is not None:
            m.C = Path(cdir)
        args = {k: v for k, v in ni.items() if k in inspect.signature(m.prepare_inputs).parameters}
        return m.prepare_inputs(**args)

    def cdir_for(D):
        ns = B.normalize_spec(spec_with(SPECS / 'CALL_REPRO_PINNED_FULL_C2V001.json', distance_Mpc=D))
        ctx = B.Ctx('simulate', ns, Path(work) / ('t11_D%r' % D))
        prof, mono, bind, rec = B.derive_geometry('DDO154', D, 66.0)
        gdir = ctx.out / 'inputs' / 'geometry_C'
        gdir.mkdir(parents=True)
        ctx.write_input('geometry_C/' + B.PROFILE_NAME, prof)
        raw = Path(B.GEOMETRY_PINS['source_binding_v003'][0]).read_bytes()
        (gdir / B.GEOMETRY_PINS['source_binding_v003'][0].name).write_bytes(raw)
        return gdir

    def arrays(d):
        g = d['gas_columns']
        return {'R': np.array([c['R_m'] for c in g]), 'dR': np.array([c['radial_weight_m'] for c in g]),
                'Sigma': np.array([c['Sigma_kg_m2'] for c in g]), 'fixed_positions': np.asarray(d['fixed_positions_m']),
                'fixed_J': np.asarray(d['fixed_integrated_columns_J']), 'initial_gas_J': np.asarray(d['initial_gas_fourier_J']),
                'stellar_mass': np.array([d['stellar_quadrature_mass_kg']]), 'queries': np.array([q['radius_kpc'] for q in d['queries']])}
    base = arrays(prep_with(None))
    reg = prep_with(cdir_for(4.04))
    assert Path(next(p for p in reg['source_pins'] if p.endswith(B.PROFILE_NAME))).parent.name == 'geometry_C'
    reg = arrays(reg)
    for k in base:
        assert base[k].shape == reg[k].shape and np.array_equal(base[k], reg[k]), k
    D = D_HI
    mu = D / 4.04
    act = arrays(prep_with(cdir_for(D)))
    dev = {'R': float(np.max(np.abs(act['R'] / base['R'] / mu - 1))),
           'dR': float(np.max(np.abs(act['dR'] / base['dR'] / mu - 1))),
           'Sigma': float(np.max(np.abs(act['Sigma'] / base['Sigma'] - 1))),
           'fixed_positions': float(np.max(np.abs(act['fixed_positions'] - mu * base['fixed_positions'])) / float(np.max(np.abs(base['fixed_positions'])))),
           'fixed_mass_J': float(np.max(np.abs(act['fixed_J'][:, 0, 0] / base['fixed_J'][:, 0, 0] / mu ** 2 - 1))),
           'stellar_mass': float(abs(act['stellar_mass'][0] / base['stellar_mass'][0] / mu ** 2 - 1))}
    assert len(act['R']) == len(base['R']) and max(dev.values()) < 1e-12, dev
    assert np.array_equal(act['queries'], base['queries']), 'route-A query radii are read from the calibration input (not geometry-adjusted)'
    return {'registered_bitwise_equal_arrays': sorted(base), 'gas_columns': int(len(base['R'])), 'scaling_deviation_at_D_HI': dev,
            'route_a_query_radii_unchanged': True}


def main(work):
    work = Path(work).resolve()
    work.mkdir(parents=True)
    for t in (t01_registered_derivation_reproduces_pinned_files, t02_scaling_laws_across_distance,
              t03_spec_acceptance_and_inclination_blocker, t04_registered_dryrun_reports_identical_to_v003,
              t05_registered_run_mode_files_identical_to_v003, t06_active_run_mode_requests_differ_only_in_geometry_inputs,
              t07_active_dryrun_overrides_resolve, t08_stage_shim_patches_real_prep_and_reuse,
              t09_admitted_outputs_must_match_call_geometry, t10_calibration_spec_trial_point_is_registered,
              t11_reviewed_prep_consumes_per_call_profile):
        t(work)
    res = {'schema': 'UNT_GALAXY_M0_FORWARD_TESTS_C2V003B', 'driver_sha256': sha(DRV_B), 'base_driver_sha256': sha(DRV_3),
           'tests_sha256': sha(__file__), 'passed': sum(r['pass'] for r in RESULTS), 'total': len(RESULTS), 'results': RESULTS,
           'scope': 'synthetic and simulate-mode only; subprocess.Popen replaced by a no-op in run-mode tests; no project stage executed'}
    with open(work / 'TEST_RESULTS.json', 'x') as f:
        json.dump(res, f, indent=1, default=str)
    for r in RESULTS:
        print('PASS' if r['pass'] else 'FAIL', r['test'], '' if r['pass'] else r['error'][:600])
    print('%d/%d' % (res['passed'], res['total']))
    return 0 if res['passed'] == res['total'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
