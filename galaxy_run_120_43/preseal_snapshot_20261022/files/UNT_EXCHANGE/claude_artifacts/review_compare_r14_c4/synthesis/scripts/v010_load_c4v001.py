# Claude4 synthesis (dispatch 0651): snapshot integration check of registry C3V010 (published 04:13Z, not yet SELECTED) against
# the r13 and r14 loaders. Read-only; run through tools/run_fenced_c4st2.py; writes one JSON under synthesis/out/.
# This is NOT the V010 review (that is Claude4's separate delta, 0132); it only checks that r14 loads it and r13 refuses it.
# usage: python3 -I -B tools/run_fenced_c4st2.py synthesis/scripts/v010_load_c4v001.py OUTNAME
import hashlib, json, sys, time, types
from pathlib import Path

OUT = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_compare_r14_c4/synthesis/out') / (sys.argv[1] + '.json')
SRC = {'r14': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py',
               'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'),
       'r13': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py',
               'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157')}
V010 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/out/PRODUCER_REGISTRY_C3V010.json',
        'b843587733ea2a532b522c69657dc5aab11cb33771acd3f20a4c4f3656c2331b')
R = {'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'v010': {'path': V010[0], 'sha256': V010[1]}, 'load': {}}
b = Path(V010[0]).read_bytes()
R['v010_sha_ok'] = hashlib.sha256(b).hexdigest() == V010[1]
d = json.loads(b)
R['shape'] = {'I4_gate_records': d['gate_records'].get('I4'), 'I4_producers': d['producers'].get('I4'),
              'top_keys': sorted(d), 'I4_pin_keys': [sorted(x) for x in d['producers'].get('I4', [])]}
for lab, (p, h) in SRC.items():
    sb = Path(p).read_bytes()
    if hashlib.sha256(sb).hexdigest() != h:
        raise SystemExit('STOP: %s differs' % lab)
    m = types.ModuleType('c4v010_' + lab)
    m.__file__ = p
    sys.modules[m.__name__] = m
    exec(compile(sb, p, 'exec'), m.__dict__)
    try:
        reg = m.load_producer_registry(V010[0], V010[1])
        R['load'][lab] = {'code': 'ACCEPT', 'I4_gate_records': reg['gate_records'].get('I4'),
                          'n_producer_gates': len(reg['producers'])}
    except m.Refused as e:
        R['load'][lab] = {'code': e.refusal_code}
R['ok'] = (R['v010_sha_ok'] and R['load']['r14']['code'] == 'ACCEPT' and R['load']['r13']['code'] == 'PRODUCER_REGISTRY_GATE_RECORDS'
           and R['shape']['I4_gate_records'] == 'PRODUCED_AFTER_THE_SEAL' and R['shape']['I4_pin_keys'] == [['path', 'sha256']])
OUT.write_text(json.dumps(R, indent=1) + '\n')
print(json.dumps({'load': R['load'], 'shape_I4': R['shape']['I4_gate_records'], 'pin_keys': R['shape']['I4_pin_keys'], 'ok': R['ok']}))
raise SystemExit(0 if R['ok'] else 1)
