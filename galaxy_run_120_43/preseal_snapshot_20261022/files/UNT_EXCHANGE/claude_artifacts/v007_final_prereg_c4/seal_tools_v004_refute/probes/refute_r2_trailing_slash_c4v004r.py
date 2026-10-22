# Claude4 seal tools v004 REFUTE stage (C4V004R), probe r2: the one refuter MUST_FAIL that tool 4 v004 did not refuse (a pin path
# with a trailing slash). Measures, for a SYNTHETIC disclosures file F (exclusive create, in probes/run_<UTC>/) and the suffixes
# '/', '/.', '//', '/./': what pathlib, os.path and the builtin open() make of F+suffix; whether tool 4 v004's manual_disclosures_codes
# accepts the pin and which path string its record pin then carries; and whether v003's own pin helpers (seal_common Checker.pin, tool 1
# dispositions_file; both byte-identical in v004) accept the same path (is the class inherited?). Run inside tools/run_fenced_c4st2.py.
import hashlib, json, os, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
V4 = HERE.parent / 'v004'
sys.path.insert(0, str(V4))
import seal_common_c4v003 as C
import check_frozen_addendum_c4v003 as T1
import build_seal_record_c4v004 as T4

R6 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json')


def main():
    assert C.sha(V4 / 'build_seal_record_c4v004.py') == '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41'
    assert C.sha(R6) == '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0'
    e = C.strict_json(R6)['basis']['erratum_E_R6_1']
    run = HERE / ('run_r2_' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()))
    run.mkdir()
    obj = {'schema': 'SEAL_MANUAL_DISCLOSURES_V001', 'e_r6_1_text': e,
           'c08_table': [{'new_item_id': 'NEW-71', 'file': 'SYNTHETIC/r2_probe.py', 'line': 7, 'declared_in_r13': False}],
           'c08_confirmation': 'SYNTHETIC TEST CONFIRMATION (Claude4 v004 refuter r2): not root\'s',
           'root_disclosures': [{'id': 'SYNTH_R2', 'source': 'SYNTHETIC', 'text': 'SYNTHETIC (Claude4 v004 refuter r2): not root\'s'}]}
    f = run / 'SEAL_MANUAL_DISCLOSURES_SYNTH_R2_C4V004R.json'
    with open(f, 'x') as fh:
        fh.write(json.dumps(obj, indent=1, sort_keys=True) + '\n')
    h = C.sha(f)
    rows = []
    for suf in ('', '/', '/.', '//', '/./'):
        p = str(f) + suf
        try:
            with open(p, 'rb') as fh:
                op = 'read %d bytes' % len(fh.read())
        except Exception as ex:
            op = type(ex).__name__
        chk = C.Checker('r2')
        md = T4.manual_disclosures_codes(chk, (p, h))
        recpin = None
        if md is not None:
            rec = T4.manual_disclosures_record(chk, md)
            recpin = rec and rec['pin']
        c3 = C.Checker('r2v003')
        v003_pin = c3.pin('x', {'path': p, 'sha256': h})
        c1 = C.Checker('r2t1')
        v003_disp = T1.dispositions_file(c1, (p, h)) is not None
        rows.append({'suffix': suf, 'pathlib_str': str(Path(p)), 'pathlib_is_file': Path(p).is_file(), 'os_path_isfile': os.path.isfile(p),
                     'builtin_open': op, 'tool4_v004_accepts': md is not None, 'tool4_codes': [x['code'] for x in chk.failures],
                     'record_pin_path': recpin and recpin['path'], 'record_pin_opens_with_builtin_open': (recpin is not None and op.startswith('read')),
                     'v003_Checker_pin_accepts': v003_pin, 'v003_tool1_dispositions_file_accepts': v003_disp})
    out = {'probe': 'refute_r2_trailing_slash_c4v004r.py', 'probe_sha256': C.sha(__file__), 'file': {'path': str(f), 'sha256': h}, 'rows': rows}
    with open(run / 'TRAILING_SLASH_C4V004R.json', 'x') as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
