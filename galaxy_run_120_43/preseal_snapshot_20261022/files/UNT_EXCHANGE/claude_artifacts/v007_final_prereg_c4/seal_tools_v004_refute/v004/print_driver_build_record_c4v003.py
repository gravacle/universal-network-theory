# Claude4 seal tools v003, tool 5 (r2 print_driver_build_record_c4v002.py fde0b26e with only the v002->v003 renames; new in v002:
# rehearsal D-06 / R-06: no checklist step created the driver BUILD record that
# PIN_DRIVER_BUILD_RECORD names). It prints the exact bytes of the r5 driver BUILD record (schema UNT_V007_SEALED_DRIVER_BUILD_C2V001)
# for root to create exclusively before B5. It writes nothing.
# The record is the reviewed compare's own builtin_r5_build() (the A62.3 r5 pins: driver b5cc62af, cascade map a7281e10, RO1 and
# nodes_v001 RO1 workers, binding 86af6198, predecessor r4) with check_record = the driver check record root confirms (A62.3: the
# r5 check; the driver_check_record slot, which the sealed compare pins as PIN_V010_R5_CHECK). Before printing, the record is
# admitted by the compare's own activate_driver_build (driver_build_codes, r5_custody_codes and check_record_codes: every file
# hashed from bytes; the check record must name the driver and carry a PASS token). Only r5: V007 seals on r5 (A96).
# r2 (A102, A-B1 class): a check record that is JSON must parse strictly (only a JSON syntax error means text), before the compare sees it.
# usage: python3 -I -B print_driver_build_record_c4v003.py --reviewed R.py --reviewed-sha H --check-record CHECK.md
#        | python3 -I -B -c "import sys; open(sys.argv[1], 'x').write(sys.stdin.read())" DRIVER_BUILD_R5_C2V001.json
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seal_common_c4v003 as C


def record_bytes(reviewed, reviewed_sha, check_record):
    chk = C.Checker('print_driver_build_record_c4v003')
    if not C.HEX64.fullmatch(reviewed_sha or ''):
        chk.fail('REVIEWED_SHA_FORMAT', repr(reviewed_sha))
        return chk.result(), None
    try:
        M = C.load_reviewed_compare(str(Path(reviewed).resolve()), reviewed_sha)
    except (Exception, SystemExit) as e:
        chk.fail('COMPARE_LOAD', '%s: %s' % (type(e).__name__, str(e)[:200]))
        return chk.result(), None
    cr = Path(check_record)
    if not cr.is_file():
        chk.fail('CHECK_RECORD_MISSING', str(cr))
        return chk.result(), None
    try:
        C.json_or_text(cr.read_bytes())                  # r2 (A102 A-B1): a defective JSON check record never reaches the compare's text fallback
    except ValueError as e:
        chk.fail('CHECK_RECORD_JSON_DEFECT', type(e).__name__)
        return chk.result(), None
    b = M.builtin_r5_build()
    b['check_record'] = {'path': str(cr.resolve()), 'sha256': C.sha(cr)}
    try:
        M.activate_driver_build(b)
    except SystemExit as e:
        chk.fail('DRIVER_BUILD_NOT_ADMISSIBLE', '%s: %s' % (getattr(e, 'refusal_code', None), str(e)[:300]))
        return chk.result(), None
    text = json.dumps(b, indent=1, sort_keys=True) + '\n'
    try:
        obj = C.strict_json_bytes(text.encode('utf-8'))
        M.activate_driver_build(obj)                     # the printed bytes themselves are admitted (round trip)
    except (Exception, SystemExit) as e:
        chk.fail('ROUND_TRIP', '%s: %s' % (type(e).__name__, str(e)[:200]))
        return chk.result(), None
    out = chk.result()
    out['driver_build_record_sha256'] = C.sha_bytes(text.encode('utf-8'))
    out['check_record'] = dict(b['check_record'])
    return out, text


def main(argv=None):
    p = C.parser('print the exact r5 driver BUILD record bytes (writes nothing)')
    p.add_argument('--reviewed', required=True)
    p.add_argument('--reviewed-sha', required=True)
    p.add_argument('--check-record', required=True)
    a = C.parse_args(p, argv)
    try:
        res, text = record_bytes(a.reviewed, a.reviewed_sha, a.check_record)
    except (Exception, SystemExit) as e:
        res, text = {'check': 'print_driver_build_record_c4v003', 'verdict': 'REFUSE',
                     'failures': [{'code': 'INTERNAL_EXCEPTION:%s' % type(e).__name__, 'detail': str(e)[:300]}], 'notes': [], 'pins_verified': {}}, None
    print(json.dumps(res, indent=1, sort_keys=True), file=sys.stderr)
    if text is None:
        return 2
    sys.stdout.write(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
