# Claude4 (dispatch 0584) seal tool 3: root's slot values, verified from bytes and consistent across documents. Read-only.
# Inputs: root's slot JSON (schema UNT_V007_SEAL_SLOTS_C4V001, shape in README_SEAL_TOOLS.md), the sealed prereg, and the prereg text
# of record (r4 e3b6b5b2). Optional: the reviewed and sealed compare (then tool 2 runs too) and the frozen addendum (then tool 1 runs).
# Refused: any PENDING or null value; any pin whose bytes differ; a sealed prereg that differs from the text of record anywhere except
# seal_slots.<k>.value; a slot value that differs from the sealed prereg's; a bound plan whose driver / frozen_addendum pins differ from
# the slots, whose launcher or guard is not BUILD's supported entry, whose template_pin is not named in BUILD, or whose spec pins do not
# verify; a bound command other than the binder's exact line; identity records whose driver_sha256 is absent or not the driver slot;
# DDO certificates whose M_s values are not 128, NGC M_s values not the registered NGC value; an r6 cache directory that is missing,
# not a directory or not empty (no pre-warming, A81 RI-24); an r5 slot set that names a cache directory.
# usage: python3 -I -B check_slot_fill_c4v001.py --slots S.json --prereg SEALED.json --text-of-record R4.json [--frozen F.md --covered-later A82]
#        [--reviewed R.py --sealed-compare S.py]
import copy, re, shlex, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seal_common_c4v001 as C

SCHEMA = 'UNT_V007_SEAL_SLOTS_C4V001'
SLOT_KEYS = ('schema', 'driver_branch', 'ngc_gas_M_s', 'frozen_addendum', 'driver', 'driver_build_record', 'driver_check_record', 'compare_reviewed_source',
             'identity_comparator', 'identity_gate_records', 'launch_packet', 'certificates', 'producer_registry', 'cache_directory_r6_only')
PREREG_SLOT_OF = {'frozen_addendum': 'frozen_addendum', 'driver': 'driver', 'compare': 'compare_reviewed_source', 'identity_comparator': 'identity_comparator',
                  'identity_gate_records': 'identity_gate_records', 'launch_packet': 'launch_packet', 'certificates': 'certificates',
                  'producer_registry': 'producer_registry', 'cache_directory_r6_only': 'cache_directory_r6_only'}
IDENTITY_KEYS = ('Z2', 'Z2_OFF_RO1', 'B0prime_RERUN')
CERT_KEYS = ('EPS', 'LO', 'GQ', 'DOUBLING', 'EPS_NGC', 'LO_NGC', 'I1T_NGC')
LAUNCH_KEYS = ('build', 'bound_plan', 'bound_command')
TEXT_OF_RECORD_SHA = 'e3b6b5b2ba265f54d15381f358913dd3ea931761aaa649c98a7583f58f1b7cf8'   # r4 (0584)
BUILD_HEADER = '## Supported runtime entry allowlist'
NOT_APPLICABLE_R5 = 'NOT_APPLICABLE_R5'


def blank_slot_values(doc):
    d = copy.deepcopy(doc)
    for v in (d.get('seal_slots') or {}).values():
        if isinstance(v, dict) and 'value' in v:
            v['value'] = '<SLOT>'
    return d


MS_KEYS = ('source_gas_M_s', 'gas_M_s', 'gas_M_s_DDO', 'M_s', 'gas_M_s_NGC')
CONTEXT_KEYS = ('roster', 'name', 'geometry', 'part_roster_name', 'galaxy')


def ms_values(o, path='$', ngc=False):
    """(path, value, is_ngc) for every M_s-type scalar; a dict whose roster/name/geometry/galaxy names NGC, or a key naming NGC, marks its subtree NGC"""
    out = []
    if isinstance(o, dict):
        here = ngc or any(isinstance(o.get(k), str) and 'NGC' in o[k].upper() for k in CONTEXT_KEYS)
        for k, v in o.items():
            p = path + '.' + k
            kn = here or 'NGC' in k.upper()
            if k in MS_KEYS and not isinstance(v, (dict, list)):
                out.append((p, v, kn))
            out += ms_values(v, p, kn)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += ms_values(v, '%s[%d]' % (path, i), ngc)
    return out


def ms_check(chk, label, rec, ddo_value, ngc_value):
    found = 0
    for path, val, is_ngc in ms_values(rec):
        want = ngc_value if is_ngc else ddo_value
        found += 0 if is_ngc else 1
        if type(val) is not int or val != want:
            chk.fail('CERTIFICATE_M_S', '%s %s = %r, want %r' % (label, path, val, want))
    return found


def run(slots_path, prereg_path, text_of_record_path, frozen=None, covered_later=(), reviewed=None, sealed_compare=None):
    chk = C.Checker('check_slot_fill_c4v001')
    try:
        slots = C.strict_json(slots_path)
        sp = C.strict_json(prereg_path)
        tor = C.strict_json(text_of_record_path)
    except Exception as e:
        chk.fail('INPUT_JSON', type(e).__name__ + ': ' + str(e))
        return chk.result()
    if C.sha(text_of_record_path) != TEXT_OF_RECORD_SHA:
        chk.fail('TEXT_OF_RECORD_NOT_R4', 'the text of record is r4 %s (0584)' % TEXT_OF_RECORD_SHA[:8])
    if set(slots) != set(SLOT_KEYS):
        chk.fail('SLOT_KEYS', 'missing %s; extra %s' % (sorted(set(SLOT_KEYS) - set(slots)), sorted(set(slots) - set(SLOT_KEYS))))
        return chk.result()
    if slots['schema'] != SCHEMA:
        chk.fail('SLOT_SCHEMA', slots['schema'])
    br = slots['driver_branch']
    if br not in ('r5', 'r6'):
        chk.fail('DRIVER_BRANCH', repr(br))
    if slots['ngc_gas_M_s'] not in (96, 128) or type(slots['ngc_gas_M_s']) is not int:
        chk.fail('NGC_GAS_M_S', '96, or 128 under A81 RI-23: %r' % slots['ngc_gas_M_s'])
    pend = {k: v for k, v in slots.items() if k != 'cache_directory_r6_only'}
    C.no_pending_anywhere(chk, 'slots', pend)
    # pins
    for k in ('frozen_addendum', 'driver', 'driver_build_record', 'driver_check_record', 'compare_reviewed_source', 'identity_comparator', 'producer_registry'):
        chk.pin(k, slots[k])
    for group, keys in (('identity_gate_records', IDENTITY_KEYS), ('launch_packet', LAUNCH_KEYS), ('certificates', CERT_KEYS)):
        g = slots[group]
        if not isinstance(g, dict) or set(g) != set(keys):
            chk.fail('SLOT_GROUP_KEYS', '%s must have exactly %s' % (group, ', '.join(keys)))
            continue
        for k in keys:
            chk.pin('%s.%s' % (group, k), g[k])
    # cache directory
    cd = slots['cache_directory_r6_only']
    if br == 'r5':
        if cd != NOT_APPLICABLE_R5:
            chk.fail('CACHE_DIRECTORY_UNDER_R5', 'r5 names no cache directory; use %s' % NOT_APPLICABLE_R5)
    elif br == 'r6':
        if not (isinstance(cd, dict) and set(cd) == {'path'} and isinstance(cd['path'], str) and Path(cd['path']).is_absolute()):
            chk.fail('CACHE_DIRECTORY_SHAPE', repr(cd))
        else:
            p = Path(cd['path'])
            if not p.is_dir() or p.is_symlink():
                chk.fail('CACHE_DIRECTORY_NOT_A_DIRECTORY', str(p))
            elif any(p.iterdir()):
                chk.fail('CACHE_DIRECTORY_NOT_EMPTY', 'no pre-warming before the seal (A81 RI-24): %s' % p)
    if chk.failures:
        return chk.result()
    # sealed prereg = text of record except the slot values; its values = the slots
    if blank_slot_values(sp) != blank_slot_values(tor):
        chk.fail('SEALED_PREREG_TEXT_CHANGED', 'the sealed prereg differs from r4 outside seal_slots.<k>.value')
    ss = sp.get('seal_slots') or {}
    for pk, sk in PREREG_SLOT_OF.items():
        if pk not in ss:
            chk.fail('PREREG_SLOT_MISSING', pk)
            continue
        if ss[pk].get('value') != slots[sk]:
            chk.fail('PREREG_SLOT_VALUE_DIFFERS', pk)
    C.no_pending_anywhere(chk, 'sealed prereg slot values', {k: v.get('value') for k, v in ss.items() if k != 'cache_directory_r6_only' or br == 'r6'})
    # BUILD, bound plan and command
    lp = slots['launch_packet']
    build_text = Path(lp['build']['path']).read_bytes().decode('utf-8')
    named_build = (((tor.get('seal_slots') or {}).get('launch_packet') or {}).get('named_candidates_verified_from_bytes') or {}).get('build')
    if not named_build or lp['build'] != named_build:
        chk.fail('BUILD_NOT_THE_PREREG_NAMED_BUILD', 'the prereg names %r' % named_build)
    try:
        sec = build_text.split(BUILD_HEADER + '\n', 1)[1].split('\n## ', 1)[0]
        allow = {p: h for h, p in re.findall(r'^([0-9a-f]{64})  (/\S+\.py)$', sec, re.M)}
    except IndexError:
        allow = {}
        chk.fail('BUILD_ALLOWLIST_SECTION', BUILD_HEADER)
    try:
        plan = C.strict_json(lp['bound_plan']['path'])
    except Exception as e:
        chk.fail('BOUND_PLAN_JSON', type(e).__name__ + ': ' + str(e))
        return chk.result()
    if plan.get('driver') != slots['driver']:
        chk.fail('PLAN_DRIVER_NOT_THE_SLOT', 'exact path/sha equality is required (launcher v007)')
    if plan.get('frozen_addendum') != slots['frozen_addendum']:
        chk.fail('PLAN_ADDENDUM_NOT_THE_SLOT', 'exact path/sha equality is required (launcher v007)')
    for k in ('launcher', 'guard'):
        ref = plan.get(k)
        if not (isinstance(ref, dict) and allow.get(ref.get('path')) == ref.get('sha256')):
            chk.fail('PLAN_%s_NOT_BUILD_SUPPORTED' % k.upper(), repr(ref))
        else:
            chk.pin('plan.' + k, ref)
    tp = plan.get('template_pin')
    if not (isinstance(tp, dict) and chk.pin('plan.template_pin', tp) and ('%s  %s' % (tp['sha256'], tp['path'])) in build_text):
        chk.fail('PLAN_TEMPLATE_NOT_NAMED_IN_BUILD', repr(tp))
    if not str(plan.get('seal_binding_status', '')).startswith('BOUND'):
        chk.fail('PLAN_NOT_BOUND', repr(plan.get('seal_binding_status')))
    for i, call in enumerate(plan.get('calls') or []):
        chk.pin('plan.calls[%d].spec' % i, call.get('spec'))
    if len(plan.get('calls') or []) != 10:
        chk.fail('PLAN_CALLS', 'ten calls expected')
    cmd = Path(lp['bound_command']['path']).read_bytes().decode('utf-8').splitlines()
    want = shlex.join([C.PYTHON, '-I', '-B', (plan.get('launcher') or {}).get('path', ''), str(Path(lp['bound_plan']['path']).resolve()), '--execute-root-only'])
    if not cmd or cmd[-1] != want or len(cmd) != 2:
        chk.fail('BOUND_COMMAND_NOT_THE_BINDER_LINE', 'expected: %s' % want)
    # driver vs its build record
    if slots['driver']['sha256'] not in Path(slots['driver_build_record']['path']).read_bytes().decode('utf-8', 'replace'):
        chk.fail('DRIVER_NOT_IN_ITS_BUILD_RECORD', 'the driver build record does not name the driver sha')
    # identity records
    for k in IDENTITY_KEYS:
        try:
            rec = C.strict_json(slots['identity_gate_records'][k]['path'])
        except Exception as e:
            chk.fail('IDENTITY_RECORD_JSON', '%s: %s' % (k, e))
            continue
        # the NEW side must carry the driver slot (A67 N1, A81 RI-21); the reference side legitimately carries its own driver.
        dsha = slots['driver']['sha256']
        raw = Path(slots['identity_gate_records'][k]['path']).read_bytes().decode('utf-8', 'replace')
        if dsha not in raw:
            chk.fail('IDENTITY_RECORD_LACKS_DRIVER_SHA', '%s does not name the driver slot sha' % k)
        for path, v in C.find_key(rec, 'result_json_driver_sha256'):
            if v != dsha:
                chk.fail('IDENTITY_RECORD_NEW_DRIVER_SHA', '%s %s = %r' % (k, path, v))
        for path, v in C.find_key(rec, 'NEW_DRIVER_PIN'):
            ok = [x for _, x in C.find_key(v, 'passed') + C.find_key(v, 'pass') + C.find_key(v, 'ok')] if isinstance(v, dict) else [v]
            if any(x is not True for x in ok if isinstance(x, bool)) or not any(x is True for x in ok if isinstance(x, bool)):
                chk.fail('IDENTITY_RECORD_NEW_DRIVER_PIN_NOT_PASSED', '%s %s' % (k, path))
    # certificates
    for k in CERT_KEYS:
        try:
            rec = C.strict_json(slots['certificates'][k]['path'])
        except Exception as e:
            chk.fail('CERTIFICATE_JSON', '%s: %s' % (k, e))
            continue
        ddo = None if k.endswith('_NGC') else 128
        n = ms_check(chk, k, rec, ddo if ddo else slots['ngc_gas_M_s'], slots['ngc_gas_M_s']) if k != 'EPS' and k != 'EPS_NGC' else 0
        if k in ('LO', 'GQ', 'DOUBLING') and n == 0:
            chk.fail('CERTIFICATE_STATES_NO_M_S', '%s must state its M_s (A68)' % k)
    # optional: tools 1 and 2
    if frozen:
        import check_frozen_addendum_c4v001 as T1
        r1 = T1.run(prereg_path, frozen, slots['frozen_addendum']['sha256'], covered_later)
        if Path(frozen).resolve() != Path(slots['frozen_addendum']['path']).resolve():
            chk.fail('FROZEN_ARG_NOT_THE_SLOT', str(frozen))
        for f in r1['failures']:
            chk.fail('T1:' + f['code'], f['detail'])
    if reviewed or sealed_compare:
        if not (reviewed and sealed_compare):
            chk.fail('COMPARE_ARGS', 'give both --reviewed and --sealed-compare')
        else:
            import check_sealed_compare_c4v001 as T2
            r2 = T2.run(reviewed, sealed_compare, slots_path, prereg_path)
            for f in r2['failures']:
                chk.fail('T2:' + f['code'], f['detail'])
            chk.pins['sealed_compare'] = r2['pins_verified'].get('sealed_compare')
    chk.pins['sealed_prereg'] = {'path': str(Path(prereg_path).resolve()), 'sha256': C.sha(prereg_path)}
    return chk.result()


def main(argv=None):
    p = C.parser('root slot values: from bytes, no PENDING, consistent across prereg, compare pins, bound plan and BUILD')
    p.add_argument('--slots', required=True)
    p.add_argument('--prereg', required=True)
    p.add_argument('--text-of-record', required=True)
    p.add_argument('--frozen')
    p.add_argument('--covered-later', default='')
    p.add_argument('--reviewed')
    p.add_argument('--sealed-compare')
    a = C.parse_args(p, argv)
    cov = [x for x in a.covered_later.split(',') if x.strip()]
    return C.emit(run(a.slots, a.prereg, a.text_of_record, a.frozen, cov, a.reviewed, a.sealed_compare))


if __name__ == '__main__':
    raise SystemExit(main())
