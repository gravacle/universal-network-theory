"""D027 / 0339 A296 baseline variant of 0829; no production module is imported or executed.

--self-test OUT tests synthetic bytes only.
--stage r11|r12 --manifest ROOT_NAMED_INPUTS.json --output OUT checks named inputs.
r11 manifest: report, r11, optional published (one policy pin).
r12 manifest: report, seal_record, regenerate_record, chain (four ordered pins),
optional published (three ordered pins). Publication is not a prerequisite for review.
Every pin is {path,sha256}. Actual report inspection is limited to seven authorized fields.
"""
import argparse
import ast
import copy
import difflib
import hashlib
import json
import subprocess
import types
from pathlib import Path

H = Path(__file__).parent
PARENT = H / 'check_verdict_finalization_cx3v002.py'
PARENT_SHA = '027062d1a114e2ba500b9ef00eade92a3265f5977da4d445eecd498d339323f9'
raw = PARENT.read_bytes()
if hashlib.sha256(raw).hexdigest() != PARENT_SHA:
    raise ValueError('checker parent pin')
B = types.ModuleType('_cx3_verdict_byte_parent')
B.__file__ = str(PARENT)
exec(compile(raw, str(PARENT), 'exec'), B.__dict__)
require, sha = B.require, B.sha
SUB = 'v006r12_c4'
# D027: constant retarget only. All gate functions remain cx3v003's.
B.PH = B.A / 'eps_rule_successor_cx2/integration/campaign/placeholder_chain_a296_cx2v001/v006r12_c4'
B.PINS = ('93d9c0acdb3e9fd40ec63ed0db7c1356b6d2b025eeb5bcde57a2ffebdbd04ba3',
          '192d086348fed9307da99732c0ef146bb336a3d605afc1e9e56b6ce959ad1a73',
          'db0d1646af5d078a288a78ec304b37a74ac546e171a8d021a37e669255492d12',
          'af4e4f36ab74c8be01d3384bcaf83bdfdc3d867207b41bad447087eea4e21743')
GEN = B.A / 'eps_rule_successor_cx2/integration/campaign/make_campaign_cascade_a296_cx2v001.py'
GEN_SHA = '114c90c301c07610eb1d6cd8ad27e5ced27691d42614556ff1a48a5dd58092e8'
CHAIN_CHECKS = ('policy_registers_exactly_the_tuple', 'core_pins_policy',
                'wrapper_pins_core', 'entry_pins_wrapper')


def line_diff(a, b):
    return [s for s in difflib.unified_diff(a.decode().splitlines(),
            b.decode().splitlines(), n=0, lineterm='')
            if s.startswith(('-', '+')) and not s.startswith(('---', '+++'))]


def resolve_sha(wrapper):
    values = [ast.literal_eval(n.value) for n in ast.parse(wrapper).body
              if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name)
              and t.id == '_resolve_source' for t in n.targets)]
    require(len(values) == 1 and isinstance(values[0], str), 'resolve literal')
    return sha(values[0].encode())


def tuple_for(raw, rp):
    fields = B.report_projection(raw)
    require(rp['sha256'] == sha(raw), 'report pin')
    return B.T4 + (sha(raw),), fields


def check_r11(base, report, rp, policy, published=None):
    t, fields = tuple_for(report, rp)
    expected = B.expected_chain(base, t)[0]
    require(policy == expected, 'r11 must equal exact tuple/comment recipe')
    require(B.changed(base[0], policy) == [13, 16], 'r11 diff lines')
    if published is not None:
        require(published == policy, 'r11 publication differs')
    return {'status': 'PASS', 'stage': 'r11', 'tuple': dict(zip(B.KEYS, t)),
            'permitted_report_fields': fields, 'diff_lines': [13, 16],
            'expected_policy_sha256': sha(expected),
            'publication': 'TESTED_EQUAL' if published is not None else 'UNTESTED_NOT_REQUIRED_FOR_GATE'}


def check_r12(base, report, rp, chain, seal, sp, regen, published=None):
    t, fields = tuple_for(report, rp)
    td = dict(zip(B.KEYS, t))
    cp = {'path': str(B.CMP), 'sha256': t[0]}
    require(seal.get('schema') == 'H3_V007_SEAL_TUPLE_RECORD_C2V001'
            and seal.get('status') == 'ROOT_FILLED', 'seal schema/status')
    require(seal.get('tuple') == td and seal.get('report') == rp
            and seal.get('compare') == cp, 'seal tuple/input bindings')
    require(seal.get('sub') == SUB and seal.get('publish_root') == str(B.CX),
            'seal sub/publish root')
    require(all(isinstance(seal.get(k), str) and seal[k].strip()
                for k in ('filled_by', 'ruling')), 'seal author/ruling')
    require(chain == B.expected_chain(base, t), 'r12 exact tuple/comment/hash cascade bytes')
    diffs = [B.changed(x, y) for x, y in zip(base, chain)]
    require(diffs == [[13, 16], [202], [29], [61]], 'r12 diff lines')
    require(regen.get('schema') == 'H3_REGENERATE_RECORD_C2V004'
            and regen.get('dry_run') is False, 'regenerate schema/dry-run')
    for key, value in [('seal_record', sp), ('tuple', td), ('report', rp),
                       ('compare', cp), ('sub', SUB), ('publish_root', str(B.CX)),
                       ('generator', {'path': str(GEN), 'sha256': GEN_SHA}),
                       ('outputs', dict(zip(B.NAMES, map(sha, chain)))),
                       ('no_tuple_build_outputs', dict(zip(B.NAMES, B.PINS))),
                       ('resolve_source_literal_sha256_utf8', resolve_sha(base[2])),
                       ('line_diff_vs_no_tuple_build',
                        dict(zip(B.NAMES, [line_diff(x, y) for x, y in zip(base, chain)])))]:
        require(regen.get(key) == value, 'regenerate ' + key)
    cc = regen.get('chain_checks')
    require(isinstance(cc, dict) and set(cc) == set(CHAIN_CHECKS)
            and all(cc[k] is True for k in CHAIN_CHECKS), 'regenerate chain checks')
    if published is not None:
        require(published == chain[:3], 'r12 publication differs')
    return {'status': 'PASS', 'stage': 'r12', 'tuple': td,
            'permitted_report_fields': fields, 'diff_lines': diffs,
            'outputs': dict(zip(B.NAMES, map(sha, chain))),
            'publication': 'TESTED_EQUAL' if published is not None else 'UNTESTED_NOT_REQUIRED_FOR_GATE'}


def self_test():
    base = B.baseline()
    doc = {'schema': B.T4[3], 'script_sha256': B.T4[0],
           'prereg': {'sha256': B.T4[1]}, 'pins_verified': {'V005_addendum': B.T4[2]},
           'decision': {'outcome': 'ADOPT_TAIL', 'tests_read': True}, 'test_mode': False}
    report = json.dumps(doc, sort_keys=True).encode()
    rp = {'path': str(H / 'SYNTHETIC_NOT_WRITTEN_REPORT.json'), 'sha256': sha(report)}
    t = B.T4 + (sha(report),)
    ch = B.expected_chain(base, t)
    seal = {'schema': 'H3_V007_SEAL_TUPLE_RECORD_C2V001', 'status': 'ROOT_FILLED',
            'tuple': dict(zip(B.KEYS, t)), 'report': rp,
            'compare': {'path': str(B.CMP), 'sha256': t[0]}, 'sub': SUB,
            'publish_root': str(B.CX), 'filled_by': 'SYNTHETIC', 'ruling': 'SYNTHETIC'}
    sp = {'path': str(H / 'SYNTHETIC_NOT_WRITTEN_SEAL.json'),
          'sha256': sha(json.dumps(seal, sort_keys=True).encode())}
    regen = {'schema': 'H3_REGENERATE_RECORD_C2V004', 'dry_run': False,
             'seal_record': sp, 'tuple': seal['tuple'], 'report': rp, 'compare': seal['compare'],
             'sub': SUB, 'publish_root': str(B.CX), 'generator': {'path': str(GEN), 'sha256': GEN_SHA},
             'outputs': dict(zip(B.NAMES, map(sha, ch))),
             'no_tuple_build_outputs': dict(zip(B.NAMES, B.PINS)),
             'resolve_source_literal_sha256_utf8': resolve_sha(base[2]),
             'line_diff_vs_no_tuple_build': dict(zip(B.NAMES, [line_diff(x, y) for x, y in zip(base, ch)])),
             'chain_checks': {k: True for k in CHAIN_CHECKS}}
    a11 = [base, report, rp, ch[0]]
    a12 = [base, report, rp, ch, seal, sp, regen]
    rows = []
    def positive(name, f, args):
        require(f(*args)['status'] == 'PASS', name)
        rows.append({'case': name, 'passed': True})
    def refusal(name, f, args):
        try:
            f(*args)
        except (ValueError, TypeError, KeyError) as exc:
            rows.append({'case': name, 'passed': True, 'refusal': str(exc)})
        else:
            raise ValueError('accepted negative control: ' + name)
    positive('r11 before r12 and before publication', check_r11, a11)
    positive('r11 with identical publication', check_r11, a11 + [ch[0]])
    positive('r12 before publication', check_r12, a12)
    positive('r12 with identical publication', check_r12, a12 + [ch[:3]])
    for index, name in enumerate(B.NAMES):
        x = copy.deepcopy(a12); x[3][index] += b'# unexpected\n'
        refusal('r12 extra bytes ' + name, check_r12, x)
    for key in ('schema', 'dry_run', 'seal_record', 'tuple', 'report', 'compare',
                'sub', 'publish_root', 'generator', 'outputs', 'no_tuple_build_outputs',
                'resolve_source_literal_sha256_utf8', 'line_diff_vs_no_tuple_build', 'chain_checks'):
        x = copy.deepcopy(a12); x[6][key] = None
        refusal('regenerate wrong ' + key, check_r12, x)
    for key in ('schema', 'status', 'tuple', 'report', 'compare', 'sub', 'publish_root', 'filled_by', 'ruling'):
        x = copy.deepcopy(a12); x[4][key] = None
        refusal('seal wrong ' + key, check_r12, x)
    for path, value in [(('decision', 'outcome'), 'DO_NOT_ADOPT'),
                        (('decision', 'tests_read'), 1), (('test_mode',), 0),
                        (('script_sha256',), '0'*64), (('schema',), 'WRONG')]:
        d = copy.deepcopy(doc)
        if len(path) == 2:
            d[path[0]][path[1]] = value
        else:
            d[path[0]] = value
        for fn, args in [(check_r11, a11), (check_r12, a12)]:
            x = copy.deepcopy(args); x[1] = json.dumps(d).encode()
            x[2]['sha256'] = sha(x[1])
            refusal(fn.__name__ + ' report ' + '.'.join(path), fn, x)
    refusal('r11 extra bytes', check_r11, a11[:3] + [ch[0] + b'\n'])
    refusal('r11 publication mismatch', check_r11, a11 + [base[0]])
    refusal('r12 publication mismatch', check_r12, a12 + [base[:3]])
    # JSON whitespace changes V while preserving the seven projected field values.
    second = json.dumps(doc, indent=2).encode()
    require(B.report_projection(second) == B.report_projection(report)
            and sha(second) != sha(report), 'synthetic report serialization distinction')
    ch2 = B.expected_chain(base, B.T4 + (sha(second),))
    require(all(sha(x) != sha(y) for x, y in zip(ch, ch2)), 'V dependency')
    rows.append({'case': 'same seven report values, different report bytes change all four outputs', 'passed': True})
    require(all(r['passed'] for r in rows), 'test failure')
    return {'status': 'TESTED', 'scope': 'synthetic stage gates only', 'count': len(rows),
            'checks': rows, 'actual_verdict_review': 'UNTESTED',
            'actual_final_output_digests': 'UNKNOWN_UNTIL_REPORT_BYTES_EXIST'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test')
    ap.add_argument('--stage', choices=('r11', 'r12'))
    ap.add_argument('--manifest')
    ap.add_argument('--output')
    a = ap.parse_args()
    if a.self_test:
        require(not any((a.stage, a.manifest, a.output)), 'self-test exclusive')
        out = Path(a.self_test); result = self_test()
    else:
        require(a.stage and a.manifest and a.output, 'stage/manifest/output required')
        out = Path(a.output)
        mp = Path(a.manifest)
        mraw = mp.read_bytes()
        m = json.loads(mraw)
        opened = []
        def read(p):
            require(isinstance(p, dict) and set(p) == {'path', 'sha256'}
                    and Path(p['path']).is_absolute(), 'pin shape')
            require('/runs_ext/' not in p['path'] and '/.codex/' not in p['path'],
                    'forbidden input tree')
            raw = Path(p['path']).read_bytes()
            require(sha(raw) == p['sha256'], 'input pin ' + p['path'])
            opened.append(p)
            return raw
        base = B.baseline()
        require(sha(B.CMP.read_bytes()) == B.T4[0] and sha(B.PRE.read_bytes()) == B.T4[1],
                'sealed comparator/prereg bytes')
        report = read(m['report'])
        tuple_for(report, m['report'])  # refuse before opening dependent files
        if a.stage == 'r11':
            require(set(m) in ({'report', 'r11'}, {'report', 'r11', 'published'}), 'r11 manifest')
            policy = read(m['r11'])
            published = read(m['published']) if 'published' in m else None
            result = check_r11(base, report, m['report'], policy, published)
        else:
            require(set(m) in ({'report', 'seal_record', 'regenerate_record', 'chain'},
                    {'report', 'seal_record', 'regenerate_record', 'chain', 'published'}), 'r12 manifest')
            require(len(m['chain']) == 4, 'four chain pins')
            seal = json.loads(read(m['seal_record']))
            regen = json.loads(read(m['regenerate_record']))
            chain = [read(p) for p in m['chain']]
            published = [read(p) for p in m['published']] if 'published' in m else None
            require(sha(GEN.read_bytes()) == GEN_SHA, 'generator pin')
            result = check_r12(base, report, m['report'], chain, seal, m['seal_record'], regen, published)
        result['inputs'] = opened
        result['manifest'] = {'path': str(mp), 'sha256': sha(mraw)}
    require(out.absolute().is_relative_to(H), 'output outside own lane')
    result.update(date_u=subprocess.check_output(['/bin/date', '-u'], text=True).strip(),
                  checker=B.pin(Path(__file__)), parent=B.pin(PARENT), disclosure=B.DISCLOSURE)
    with out.open('x') as f:
        json.dump(result, f, indent=2, sort_keys=True); f.write('\n')
    print(json.dumps({'result': B.pin(out), 'status': result['status'], 'checks': result.get('count')}))


if __name__ == '__main__':
    main()
