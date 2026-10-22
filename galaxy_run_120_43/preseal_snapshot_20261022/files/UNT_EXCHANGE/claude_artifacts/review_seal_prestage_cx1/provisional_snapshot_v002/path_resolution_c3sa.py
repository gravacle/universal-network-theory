# Claude3 seal-assembly builder (0626): read-only path-resolution probe. Writes ONE new JSON (exclusive create) given as argv[1].
# For every slot / binder path: literal vs os.path.realpath vs Path.resolve() vs the binder's own pin() (imported in-process; pin() only
# resolves and reads bytes), symlink components (lstat walk), and the /System/Volumes/Data firmlink spelling (stat identity).
# Never touches runs_ext, UVT_*, the registered C5H run, NGC targets or /.vol (a refusal list is checked before any metadata call).
import hashlib, importlib.util, json, os, sys
from pathlib import Path

FORBID = ('runs_ext', 'UVT_', 'KMAX_A2F10_C5H_RUN_V001', '/.vol', 'NGC3198_TARGET', 'SPARC')
BINDER = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/bind_sealed_launch_plan_cx1v001.py'
BINDER_SHA = 'f3e4e2beeb8f1cb151892fd903b889c471cea58fea1b67c72552137d037575ca'
TEMPLATE = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/LAUNCH_PLAN_V011_CX3V001.json'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
FROZEN = CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md'
OPEN_V005 = CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
FIRM = '/System/Volumes/Data'


def guard(p):
    for f in FORBID:
        if f in p:
            raise SystemExit('FENCE_REFUSED %r contains %r' % (p, f))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def symlink_components(p):
    out, cur = [], '/'
    for comp in Path(p).parts[1:]:
        cur = os.path.join(cur, comp)
        try:
            if os.path.islink(cur):
                out.append({'component': cur, 'target': os.readlink(cur)})
        except OSError as e:
            out.append({'component': cur, 'error': type(e).__name__})
            break
    return out


def firm_identity(p):
    try:
        a, b = os.stat(p), os.stat(FIRM + p)
        return {'firmlink_spelling': FIRM + p, 'same_dev_ino': (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino),
                'realpath_of_firmlink_spelling': os.path.realpath(FIRM + p)}
    except OSError as e:
        return {'firmlink_spelling': FIRM + p, 'error': type(e).__name__}


def main(out_path):
    guard(BINDER)
    assert sha(BINDER) == BINDER_SHA, 'binder sha'
    spec = importlib.util.spec_from_file_location('binder_c3sa_probe', BINDER)
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)          # top level: imports, HERE, PYTHON, def pin/bind/main; main() not run (__name__ != __main__)
    tpl = json.loads(Path(TEMPLATE).read_bytes())
    paths = {'binder': BINDER, 'template': TEMPLATE, 'ctrl_dir': CTRL, 'open_v005': OPEN_V005,
             'driver': tpl['driver']['path'], 'launcher': tpl['launcher']['path'], 'guard': tpl['guard']['path'],
             'monitor': tpl['monitor']['path'], 'python': B.PYTHON}
    for i, c in enumerate(tpl['calls']):
        paths['call%02d_spec_%s' % (i, c['case'])] = c['spec']['path']
    extra = json.loads(Path(sys.argv[2]).read_bytes()) if len(sys.argv) > 2 else {}
    paths.update(extra)
    rows = {}
    for k, p in paths.items():
        guard(p)
        r = {'literal': p, 'exists': os.path.exists(p), 'realpath': os.path.realpath(p), 'Path_resolve': str(Path(p).resolve())}
        r['realpath_equals_literal'] = r['realpath'] == p
        r['resolve_equals_literal'] = r['Path_resolve'] == p
        r['symlink_components'] = symlink_components(p)
        if os.path.isfile(p):
            r['sha256'] = sha(p)
            bp = B.pin(p)
            r['binder_pin'] = bp
            r['binder_pin_path_equals_literal'] = bp['path'] == p
        r['firmlink'] = firm_identity(p) if os.path.exists(p) else None
        rows[k] = r
    fz = {'literal': FROZEN, 'exists_now': os.path.exists(FROZEN), 'realpath': os.path.realpath(FROZEN),
          'Path_resolve': str(Path(FROZEN).resolve()), 'parent_symlink_components': symlink_components(CTRL)}
    fz['resolve_equals_literal'] = fz['Path_resolve'] == FROZEN
    tpl_checks = {'driver_pin_equals_binder_pin_of_driver': tpl['driver'] == B.pin(tpl['driver']['path']),
                  'launcher_pin_ok': B.pin(tpl['launcher']['path']) == tpl['launcher'],
                  'guard_pin_ok': B.pin(tpl['guard']['path']) == tpl['guard'],
                  'monitor_pin_ok': B.pin(tpl['monitor']['path']) == tpl['monitor'],
                  'spec_pins_ok': [B.pin(c['spec']['path']) == c['spec'] for c in tpl['calls']],
                  'n_calls': len(tpl['calls']), 'binder_HERE': str(B.HERE),
                  'template_frozen_addendum_field': tpl.get('frozen_addendum'),
                  'template_seal_binding_status': tpl.get('seal_binding_status')}
    res = {'schema': 'C3SA_PATH_RESOLUTION_V001', 'utc': __import__('time').strftime('%Y-%m-%dT%H:%M:%SZ', __import__('time').gmtime()),
           'python': sys.executable, 'cwd': os.getcwd(), 'paths': rows, 'frozen_expected': fz, 'template_checks': tpl_checks}
    with open(out_path, 'x') as f:
        json.dump(res, f, indent=1, sort_keys=True)
        f.write('\n')
    print(json.dumps({'all_resolve_equal': all(r['resolve_equals_literal'] for r in rows.values()), 'frozen_resolve_equal': fz['resolve_equals_literal'],
                      'template_checks': {k: v for k, v in tpl_checks.items() if k != 'spec_pins_ok'}, 'spec_pins_all_ok': all(tpl_checks['spec_pins_ok']),
                      'not_equal': [k for k, r in rows.items() if not r['resolve_equals_literal']]}, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])
