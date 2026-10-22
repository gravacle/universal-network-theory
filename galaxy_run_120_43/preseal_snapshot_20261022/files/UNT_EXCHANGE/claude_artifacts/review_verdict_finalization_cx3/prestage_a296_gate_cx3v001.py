"""D027 source reconstruction and cross-lineage controls; no production execution."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import types

H = Path(__file__).parent
A = H.parent
C = A / 'eps_rule_successor_cx2/integration/campaign'
inputs = {}
checks = []


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, expected=None):
    raw = path.read_bytes()
    if expected is not None:
        assert sha(raw) == expected, str(path)
    inputs[str(path)] = sha(raw)
    return raw


def check(name, condition):
    assert condition, name
    checks.append({'case': name, 'passed': True})


def load(path, expected):
    raw = read(path, expected)
    module = types.ModuleType('_cx3_' + path.stem)
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


def funcs(raw):
    return {n.name: ast.dump(n, include_attributes=False)
            for n in ast.parse(raw).body if isinstance(n, ast.FunctionDef)}


def literal(raw, name):
    nodes = [n.value for n in ast.parse(raw).body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    assert len(nodes) == 1, name
    return ast.literal_eval(nodes[0])


def replace(raw, old, new):
    assert raw.count(old) == 1, old
    return raw.replace(old, new)


old_path = H / 'check_verdict_gates_cx3v003.py'
new_path = H / 'check_verdict_gates_a296_cx3v001.py'
old = load(old_path, '78358dac30a92e8068706ec1e44bde715b043707dad8473e6d4e723a436de295')
new = load(new_path, 'd2ecfd18c29d1359f5007c44fdc369a07ab3a7571679645fed61785ee764c5d7')
read(new.PARENT, new.PARENT_SHA)
check('all_gate_function_ASTs_unchanged', funcs(read(old_path)) == funcs(read(new_path)))
base = new.B.baseline()
legacy = old.B.baseline()
for module, values in ((new, base), (old, legacy)):
    for name, raw, pin in zip(module.B.NAMES, values, module.B.PINS):
        check('baseline_byte_pin:' + str(module.B.PH / name),
              read(module.B.PH / name, pin) == raw)
read(new.B.CX / 'v006r10_c4/adoption_policy_cx2v006r10_c4.py', new.B.PINS[0])
g = read(new.GEN, new.GEN_SHA)
og = read(old.GEN, old.GEN_SHA)
check('generator_build_AST_unchanged', funcs(g)['build'] == funcs(og)['build'])
replacements = literal(g, 'POLICY_REPLACEMENTS')
check('policy_replacement_literals_unchanged',
      replacements == literal(og, 'POLICY_REPLACEMENTS'))
p = read(new.B.CX / 'v006r7/adoption_policy_cx2v006r7.py',
         '7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d')
for _, old_text, new_text in replacements:
    p = replace(p, old_text.encode(), new_text.encode())
c = read(new.B.CX / 'v006r9/calibration_core_cx2v006r9.py',
         'a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605')
c = replace(c, b"    p = Path(__file__).resolve().parent.parent/'v006r7/adoption_policy_cx2v006r7.py'\n",
            ("    p = Path(__file__).resolve().parent.parent/'v006r12_c4/" + new.B.NAMES[0] + "'\n").encode())
c = replace(c, b'7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d', sha(p).encode())
wrapper_source = C / 'calibration_orchestrator_q5b1_ledger_a296_cx2v001.py'
w = read(wrapper_source, 'cb1f5e73753b69d1e8b6067c746b8fcda89d94d6bc4f34fb0a78f927e07cca04')
w = replace(w, b"M=load(HERE/'calibration_core_cx2v006r10_c4.py','_cx2v006r1',expected='dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6')\n",
            ("M=load(HERE/'" + new.B.NAMES[1] + "','_cx2v006r1',expected='" + sha(c) + "')\n").encode())
e = read(C / 'h3_campaign_entry_a296_cx2v001.py',
         '05738509efb85f1a64d0031bf0e1c6b0d96f3427ab1a5670704affcd47f4ff28')
e = replace(e, ("WRAPPER = Path('" + str(wrapper_source) + "')\n").encode(),
            ("WRAPPER = Path('" + str(new.B.CX / new.SUB / new.B.NAMES[2]) + "')\n").encode())
e = replace(e, b"WRAPPER_SHA = 'cb1f5e73753b69d1e8b6067c746b8fcda89d94d6bc4f34fb0a78f927e07cca04'\n",
            ("WRAPPER_SHA = '" + sha(w) + "'\n").encode())
for name, actual, expected in zip(new.B.NAMES, (p, c, w, e), base):
    check('independent_source_reconstruction:' + name, actual == expected)
check('resolve_source_literal_preserved', new.resolve_sha(read(wrapper_source)) == new.resolve_sha(w))
nr = read(C / 'regenerate_h3_a296_cx2v001.py',
          '2a69e63782ee29591eaa6b0d1abf311b072d6f304d6372cd56be0872254099a1')
oraw = read(A / 'h3_campaign_path_c2/regenerate_h3_c2v004.py')
nfunc, ofunc = funcs(nr), funcs(oraw)
check('regenerator_functions_equal_except_fill_label',
      {k: v for k, v in nfunc.items() if k != 'fill'} ==
      {k: v for k, v in ofunc.items() if k != 'fill'})
normalized = nr.replace(b'regenerate_h3_a296_cx2v001 fill: sealed compare constants + report bytes',
                        b'regenerate_h3_c2v004 fill: sealed compare constants + report bytes')
check('regenerator_fill_AST_only_label_change', funcs(normalized)['fill'] == ofunc['fill'])

doc = {'schema': new.B.T4[3], 'script_sha256': new.B.T4[0],
       'prereg': {'sha256': new.B.T4[1]}, 'pins_verified': {'V005_addendum': new.B.T4[2]},
       'decision': {'outcome': 'ADOPT_TAIL', 'tests_read': True}, 'test_mode': False}
report = json.dumps(doc, sort_keys=True).encode()
rp = {'path': str(H / 'D027_SYNTHETIC_REPORT_NOT_WRITTEN.json'), 'sha256': sha(report)}
tup = new.B.T4 + (sha(report),)


def fixture(module, baseline):
    chain = module.B.expected_chain(baseline, tup)
    seal = {'schema': 'H3_V007_SEAL_TUPLE_RECORD_C2V001', 'status': 'ROOT_FILLED',
            'tuple': dict(zip(module.B.KEYS, tup)), 'report': rp,
            'compare': {'path': str(module.B.CMP), 'sha256': tup[0]}, 'sub': module.SUB,
            'publish_root': str(module.B.CX), 'filled_by': 'SYNTHETIC', 'ruling': 'SYNTHETIC'}
    sp = {'path': str(H / 'D027_SYNTHETIC_SEAL_NOT_WRITTEN.json'),
          'sha256': sha(json.dumps(seal, sort_keys=True).encode())}
    regen = {'schema': 'H3_REGENERATE_RECORD_C2V004', 'dry_run': False,
             'seal_record': sp, 'tuple': seal['tuple'], 'report': rp,
             'compare': seal['compare'], 'sub': module.SUB, 'publish_root': str(module.B.CX),
             'generator': {'path': str(module.GEN), 'sha256': module.GEN_SHA},
             'outputs': dict(zip(module.B.NAMES, map(sha, chain))),
             'no_tuple_build_outputs': dict(zip(module.B.NAMES, module.B.PINS)),
             'resolve_source_literal_sha256_utf8': module.resolve_sha(baseline[2]),
             'line_diff_vs_no_tuple_build': dict(zip(module.B.NAMES,
                 [module.line_diff(x, y) for x, y in zip(baseline, chain)])),
             'chain_checks': {key: True for key in module.CHAIN_CHECKS}}
    return [baseline, report, rp, chain, seal, sp, regen]


def refuse(name, module, args):
    try:
        module.check_r12(*args)
    except (ValueError, TypeError, KeyError) as exc:
        checks.append({'case': name, 'passed': True, 'refusal': str(exc)})
    else:
        raise AssertionError('Accepted negative: ' + name)


na, oa = fixture(new, base), fixture(old, legacy)
check('A296_synthetic_exact_chain_passes', new.check_r12(*na)['status'] == 'PASS')
check('legacy_synthetic_exact_chain_still_passes', old.check_r12(*oa)['status'] == 'PASS')
check('r11_policy_bytes_and_gate_result_unchanged',
      na[3][0] == oa[3][0] and new.check_r11(base, report, rp, na[3][0]) ==
      old.check_r11(legacy, report, rp, oa[3][0]))
check('synthetic_r12_chain_difference_is_wrapper_and_entry_only',
      [x == y for x, y in zip(na[3], oa[3])] == [True, True, False, False])
x = copy.deepcopy(na)
x[3], x[6] = oa[3], oa[6]
refuse('A296_gate_refuses_complete_legacy_chain', new, x)
x = copy.deepcopy(oa)
x[3], x[6] = na[3], na[6]
refuse('legacy_gate_refuses_complete_A296_chain', old, x)
x = copy.deepcopy(na)
x[6]['generator'] = oa[6]['generator']
refuse('A296_gate_refuses_legacy_generator_pin', new, x)
x = copy.deepcopy(na)
x[6]['no_tuple_build_outputs'] = oa[6]['no_tuple_build_outputs']
refuse('A296_gate_refuses_legacy_baseline_hashes', new, x)
for index in (2, 3):
    x = copy.deepcopy(na)
    x[3][index] = oa[3][index]
    refuse('A296_gate_refuses_mixed_chain_' + str(index), new, x)

control_path = H / 'STAGE_GATE_CONTROLS_A296_CX3V001.json'
control = json.loads(read(control_path, 'b4c082cd17087d35559e2da23b5c8119de281e0abbc78697e953be8a95efc4c6'))
check('inherited_synthetic_controls_45_of_45',
      control['count'] == 45 and all(x['passed'] for x in control['checks']))
for path, expected in inputs.items():
    assert sha(Path(path).read_bytes()) == expected, 'Source changed: ' + path
out = H / 'PRESTAGE_A296_GATE_CX3V001.json'
record = {'schema': 'CX3_D027_A296_GATE_PRESTAGE_V001', 'status': 'TESTED',
          'date_u': subprocess.check_output(['/bin/date', '-u'], text=True).strip(),
          'count': len(checks), 'checks': checks,
          'inherited_gate_controls': 45,
          'inputs': [{'path': p, 'sha256': s} for p, s in sorted(inputs.items())],
          'script': {'path': str(Path(__file__)), 'sha256': sha(Path(__file__).read_bytes())},
          'scope': 'Source reconstruction and synthetic byte gates only; production source read as text/AST, never executed.',
          'actual_verdict_review': 'UNTESTED', 'actual_root_chain_selection': 'PENDING_ROOT_DECISION',
          'actual_final_output_digests': 'UNKNOWN_UNTIL_REPORT_BYTES_EXIST'}
with out.open('x') as handle:
    json.dump(record, handle, sort_keys=True, indent=2)
    handle.write('\n')
print(json.dumps({'result': {'path': str(out), 'sha256': sha(out.read_bytes())},
                  'checks': len(checks), 'inherited_gate_controls': 45}))
