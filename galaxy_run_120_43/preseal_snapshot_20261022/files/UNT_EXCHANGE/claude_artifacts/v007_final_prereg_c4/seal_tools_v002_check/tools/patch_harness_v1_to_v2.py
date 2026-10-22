# patch tests/test_c4chk_v1.py -> tests/test_c4chk_v2.py (exclusive create); every replacement must match exactly once, else exit 1
import ast, sys
from pathlib import Path
T = Path(__file__).resolve().parent.parent / 'tests'
src = (T / 'test_c4chk_v1.py').read_text(encoding='utf-8')
R = [
    ("    bad_cmd = xw(run / 'BOUND_COMMAND_NOT_UTF8_C4CHK.txt', 'x')\n    with open(bad_cmd, 'wb') as f:\n        pass\n",
     "    bad_cmd = run / 'BOUND_COMMAND_NOT_UTF8_C4CHK.txt'\n    with open(bad_cmd, 'xb') as f:\n        f.write(b'\\xff\\xfe not utf-8\\n')\n"),
    ("    rec_(G7, 'INFO', 'D-07 class: an empty bound command file', r_['verdict'] == 'REFUSE', r_['verdict'], codes_of(r_), 'REFUSE')\n",
     "    check(G7, 'MUT', 'D-07 class: a bound command file that is not UTF-8 refuses with a code (no traceback)', r_['verdict'] == 'REFUSE' and bool(codes_of(r_)), repr(codes_of(r_)[:3]))\n"),
    ("gates_body(mt_crosscheck='DEADBEEF' + '1234567890' * 5 + 'AB')", "gates_body(mt_crosscheck='DEADBEEF' + '1234567890' * 5 + 'ABCDEF')"),
    ("        M.load_producer_registry(str(regx_p), C.sha(regx_p))\n        regload = 'loaded'\n    except SystemExit as e:\n        regload = 'REFUSED %s' % getattr(e, 'refusal_code', None)\n",
     "        M.load_producer_registry(str(regx_p), C.sha(regx_p))\n        regload = 'loaded'\n    except BaseException as e:\n        regload = 'REFUSED %s %s' % (type(e).__name__, getattr(e, 'refusal_code', None))\n"),
    ("    # =========================================================== D-04 case block\n",
     "    dbl = json.loads(CERTS['DOUBLING'].read_bytes())\n"
     "    chk_ = C.Checker('x')\n"
     "    n_ = T3.certificate_ms_codes(chk_, 'DOUBLING', dbl, 128, 96)\n"
     "    check(G1, 'REAL', 'D-01 REAL: v002 reads exactly one M_s field (ddo_gas_M_s 128) in DOUBLING ea48ac2b and raises nothing', n_ == 1 and not chk_.failures, repr((n_, chk_.failures)))\n"
     "    comp4 = M.IDENTITY_COMPARATOR_C2V004\n"
     "    s2, p2, sp2, sc2 = variant('comparator_c2v004', lambda s: s.update(identity_comparator={'path': comp4[0], 'sha256': comp4[1]}))\n"
     "    r_ = t3(p2, sp2, full=False)\n"
     "    finding(G1, 'slot identity_comparator = the superseded c2v004 e3d153b6 (not registry C3V009 identity_comparators) passes tool 3', r_.get('verdict') == 'PASS'\n"
     "            and comp4[1] not in json.dumps(reg.get('identity_comparators')), r_, 'tool 3 pins the comparator but never compares it with the registry or the r5-named c2v007r2')\n"
     "    # =========================================================== D-04 case block\n"),
]
for old, new in R:
    n = src.count(old)
    if n != 1:
        print('REPLACEMENT_COUNT', n, repr(old[:70])); sys.exit(1)
    src = src.replace(old, new)
src = src.replace("'harness': 'test_c4chk_v1.py'", "'harness': 'test_c4chk_v2.py'").replace("'run_v1_' + stamp", "'run_v2_' + stamp").replace("'TEST_RESULTS_C4CHK_V1.json'", "'TEST_RESULTS_C4CHK_V2.json'")
ast.parse(src)
if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
    print('DRY_RUN_OK', len(src)); sys.exit(0)
with open(T / 'test_c4chk_v2.py', 'x', encoding='utf-8') as f:
    f.write(src)
print('WROTE test_c4chk_v2.py')
