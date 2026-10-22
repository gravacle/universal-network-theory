"""CHECK_V001 K01: v002 specs/templates vs anchor base spec and vs the prereg matrix (independent checker, Claude2 lane).
Reads only spec/template/manifest bytes in the prereg dir, the base spec, the V001 prereg and generator. Writes one JSON."""
import hashlib, json, sys
from pathlib import Path
D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v002_c2')
pre = json.loads((D / 'KMAX_MATRIX_PREREG_V002.json').read_bytes())
base_p = pre['binding_inputs']['anchor_base_spec']['path']
base = json.loads(Path(base_p).read_bytes())
F3 = pre['cases'][6]['bound_call']['outdir']
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def flat(o, pre_=''):
    out = {}
    if isinstance(o, dict) and o:
        for k, v in o.items(): out.update(flat(v, pre_ + '/' + k))
    else:
        out[pre_] = o
    return out
cases = {c['id']: c for c in pre['cases']}
fb = flat(base)
rep = {'base_spec_sha256': sha(base_p), 'files': {}}
anc = pre['anchor']
ok_all = True
for kind, pat in (('wave1', 'CALL_KMAX_%s_A2F3_C2V002.json'), ('templates', 'CALL_KMAX_%s_A2F3_C2V002.TEMPLATE.json')):
    for p in sorted((D / 'specs_anchor/v002' / kind).glob('*.json')):
        cid = p.name.split('_')[2]
        c = cases[cid]
        s = json.loads(p.read_bytes())
        fs = flat(s)
        keys = sorted(set(fs) | set(fb))
        diff = {k: [fb.get(k, '<absent>'), fs.get(k, '<absent>')] for k in keys if json.dumps(fb.get(k, '<absent>'), sort_keys=True) != json.dumps(fs.get(k, '<absent>'), sort_keys=True)}
        allowed_prefix = ('/label', '/numerics/composite_grid_spec', '/numerics/truncation', '/numerics/picard/passes', '/admit')
        off = sorted(k for k in diff if not k.startswith(allowed_prefix))
        reg_grid = pre['grids'][c['grid']]['composite_grid_spec']
        want_tr = {'shape': c['shape']} if c['shape'] == 'cube' else {'shape': c['shape'], 'kmax_inverse_kpc': c['kmax_inverse_kpc']}
        chk = {
            'sha256': sha(p),
            'diff_keys_vs_base': sorted(diff),
            'off_matrix_diffs': off,
            'physical_equal_anchor': s['physical'] == anc['physical'] == base['physical'],
            'coefficients_equal_anchor': s['coefficients'] == anc['coefficients'],
            'brackets_equal_anchor': s['numerics']['brackets'] == anc['brackets'] == base['numerics']['brackets'],
            'picard_equal_anchor': s['numerics']['picard'] == {k: anc['picard'][k] for k in ('passes', 'speed_change_bound_km_s', 'observe_every_pass')},
            'column_workers_equal': s['numerics']['column_workers'] == anc['column_workers'] == base['numerics']['column_workers'],
            'grid_equal_registered': s['numerics']['composite_grid_spec'] == reg_grid,
            'truncation_equal_registered': s['numerics']['truncation'] == want_tr,
            'label': s.get('label'),
            'label_has_prereg_sha': '0024b63e' in json.dumps(s.get('label')),
            'admit': s.get('admit'),
        }
        if kind == 'templates':
            adm = json.dumps(s.get('admit'))
            exp_cube = c['prefix'].split(':')[1] if c['prefix'].startswith('admit:') else None
            chk['admit_refers_F3'] = F3 in adm
            chk['admit_placeholder_left'] = '<' in adm
            chk['expected_admit_cube'] = exp_cube
        ok = not off and all(chk[k] for k in ('physical_equal_anchor', 'coefficients_equal_anchor', 'brackets_equal_anchor', 'picard_equal_anchor', 'column_workers_equal', 'grid_equal_registered', 'truncation_equal_registered'))
        chk['ok'] = ok
        ok_all &= ok
        rep['files']['%s/%s' % (kind, p.name)] = chk
rep['all_ok'] = ok_all
out = Path(sys.argv[1])
with open(out, 'x') as f:
    json.dump(rep, f, indent=1, default=str)
for k, v in rep['files'].items():
    print(k, 'ok' if v['ok'] else 'FAIL', 'diff:', v['diff_keys_vs_base'][:12], 'off:', v['off_matrix_diffs'], 'admit:', json.dumps(v['admit'])[:200], 'labelsha:', v['label_has_prereg_sha'])
print('ALL_OK', ok_all)
