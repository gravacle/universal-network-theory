"""Edge cases for the R2B-01 fix thresholds. Loads verify_r2b01.py from this folder by explicit path (no sys.path use).
Synthetic ratios only; writes one JSON file in this verify folder."""
import importlib.util
import json
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('verify_r2b01', os.path.join(TOOLS, 'verify_r2b01.py'))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)          # installs the same audit-hook fence

OQ, TQ = v.OQ, v.TQ


def case(defs):
    return v.mk(defs)


E = {}
spec_ = {q: ('R', -3.0) for q in OQ[:2]}
spec_.update({q: ('R', 0.0) for q in OQ[2:4]})
spec_.update({q: ('PINV',) for q in OQ[4:]})
E['E_tie_2def_2hit_4gated'] = case(spec_)
spec_ = {OQ[0]: ('R', -3.0)}
spec_.update({q: ('PINV',) for q in OQ[1:]})
E['E_one_signed_deficit_7gated'] = case(spec_)
spec_ = {OQ[0]: ('R', -3.0)}
spec_.update({q: ('R', 0.0) for q in OQ[1:4]})
spec_.update({q: ('PINV',) for q in OQ[4:]})
E['E_hit_majority_1def_3hit_4gated'] = case(spec_)
E['E_transition_all_gated'] = case({q: ('PINV',) for q in TQ})
E['E_outer_all_builtin_invalid'] = case({q: ('INV',) for q in OQ})

out = {}
for name, rows in E.items():
    out[name] = {}
    for var, sem in (('R2', 'strict'), ('FQ', 'explicit'), ('FB', 'explicit')):
        for g in ('early', 'late'):
            r = v.classify(rows, var, sem, g)
            O = r['zones']['OUTER']
            out[name]['%s/%s/%s' % (var, sem, g)] = dict(
                patterns=r['patterns'], S_outer=O['S'], Nv=O['Nv'], M=O['M'], U=O['U'], H=O['H'],
                e3=[r['e3_def1'], r['e3_def2']], coverage_ok=r['coverage_ok'])
path = os.path.join(os.path.dirname(TOOLS), 'VERIFY_R2B01_EDGES.json')
with open(path, 'w') as f:
    json.dump(out, f, indent=1, sort_keys=True)
for name, d in out.items():
    print(name)
    for k, s in d.items():
        print('   ', k, s['patterns'], 'S(O)=', s['S_outer'], 'Nv,M,U,H=', s['Nv'], s['M'], s['U'], s['H'], 'e3=', s['e3'], 'cov=', s['coverage_ok'])
print('wrote', path)
