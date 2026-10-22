# Claude4 seal tools v002, tool 3 (successor of check_slot_fill_c4v001.py 7f3cf07d): root's slot values, verified from bytes and
# consistent across documents. Read-only (it writes nothing; it loads the REVIEWED compare in-process to call its own functions).
# Inputs: root's slot JSON (schema UNT_V007_SEAL_SLOTS_C4V002, shape in README_SEAL_TOOLS.md), the sealed prereg, and the prereg
# text of record (prereg r5; its sha is TEXT_OF_RECORD_SHA, PENDING until root rules r5 the text of record, then set by a pin-only
# successor). Optional: the reviewed and sealed compare (then tool 2 runs too) and the frozen addendum (then tool 1 runs).
# Kept from v001: refuse any PENDING or null slot value; pin bytes that differ; a sealed prereg that differs from the text of record
# outside seal_slots.<k>.value; slot values that differ from the sealed prereg's; a bound plan whose driver / frozen_addendum pins
# differ from the slots, whose launcher or guard is not a supported entry of the BUILD, whose template is not named in the BUILD or
# whose spec pins do not verify; a bound command other than the binder's line; identity records not on the driver slot; r6 cache
# directory rules (A81 RI-24).
# New in v002:
#  D-01  every M_s field the r12 FIELDS defines, per certificate kind: LO source_gas_M_s (+ its echoes, A73 F2), GQ rosters[].M_s and
#        M_s_doubled = 2 M_s (NGC_T120L at the NGC M_s), DOUBLING ddo_gas_M_s (A73); plus a scan of every other M_s-type key. The DDO
#        M_s is the case block's registered uv_tail gas.M_s (A68 CHK-1; = 128, A57); the NGC M_s is the slot (= the compare's 96).
#  D-04  the sealed prereg must carry binding_inputs.case_block {path, sha256}; it is verified from bytes and validated in-process by
#        the reviewed compare's own validate_case_block, after the slot's driver BUILD record is activated with the compare's own
#        activate_driver_build (sealed-mode order, r12 L5689-5729). Under r5 the CASCADE_MAP_R5_ADDENDUM pin is required (SRR[9],
#        A69) and must name the build's r5 cascade map; the admission-config launcher and guard (SRR[10], A78 N2) are slots that
#        must equal the bound plan's and be BUILD_V007-supported entries. All of these pass through to the builder.
#  D-10  the frozen_addendum slot path must be seal_slots.frozen_addendum.path_to_be.
#  A99.1 the launch-packet BUILD of record is BUILD_V007: its {path, sha256} is read from the prereg's launch-packet slot
#        (named_candidates_verified_from_bytes.build); any other build (V005, V006, ...) refuses; while the sha is the literal
#        PENDING_BUILD_V007 it refuses BUILD_V007_PENDING (a gap). When the text of record holds that literal, the sealed prereg may
#        fill that one leaf with the real sha (verified from bytes): a seal-time fill, not a text change. Its supported-entry
#        allowlist must have exactly 15 sources (V6-S3), each verified from bytes.
#  D-08  layers are reported together: a layer is skipped (and named) only when a pin it reads did not verify.
#  r2    A102 (A-B1 class; the CASCADE_MAP_R5_ADDENDUM probe was patched by the Claude4 main loop at 21:21:40Z, before r1 was installed):
#        the driver check record and the addendum may be text, but if either is JSON it must parse strictly; the only text fallback
#        is a JSON syntax error, so a duplicate key behind a 4,300+ digit integer refuses here even while the reviewed compare r12
#        still admits such a check record (A102: r13 fixes the compare itself).
#  r2    the text of record: TEXT_OF_RECORD_SHA stays PENDING until a pin-only successor sets the r5 sha root rules of record; until
#        then root states that sha with --text-of-record-sha (64 hex, equal to the file's bytes), and the SEAL_RECORD records which
#        of the two pinned it. Without either, tool 3 refuses TEXT_OF_RECORD_PIN_PENDING (a gap; every other layer is still checked).
#  Also: each certificate / identity record is the gate the slot names (schema and `gate` field); the driver BUILD record's
#        build, driver and check_record equal the slots; ngc_gas_M_s equals the compare's NGC constant; when the prereg names a
#        template_plan (prereg r5: BUILD_V007's selected r5 template), the bound plan's template_pin is exactly it.
# usage: python3 -I -B check_slot_fill_c4v003.py --slots S.json --prereg SEALED.json --text-of-record R5.json [--text-of-record-sha H]
#        [--frozen F.md --covered-later A100] [--reviewed R.py --sealed-compare S.py]
import copy, re, shlex, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seal_common_c4v003 as C

SCHEMA = 'UNT_V007_SEAL_SLOTS_C4V002'
SLOT_KEYS = ('schema', 'driver_branch', 'ngc_gas_M_s', 'frozen_addendum', 'driver', 'driver_build_record', 'driver_check_record', 'compare_reviewed_source',
             'identity_comparator', 'identity_gate_records', 'launch_packet', 'certificates', 'producer_registry', 'cache_directory_r6_only',
             'cascade_map_r5_addendum', 'admission_entry')
PREREG_SLOT_OF = {'frozen_addendum': 'frozen_addendum', 'driver': 'driver', 'compare': 'compare_reviewed_source', 'identity_comparator': 'identity_comparator',
                  'identity_gate_records': 'identity_gate_records', 'launch_packet': 'launch_packet', 'certificates': 'certificates',
                  'producer_registry': 'producer_registry', 'cache_directory_r6_only': 'cache_directory_r6_only'}
OPTIONAL_PREREG_SLOT_OF = {'cascade_map_r5_addendum': 'cascade_map_r5_addendum', 'admission_entry': 'admission_entry'}
IDENTITY_KEYS = ('Z2', 'Z2_OFF_RO1', 'B0prime_RERUN')
IDENTITY_GATE_OF = {'Z2': 'B1', 'Z2_OFF_RO1': 'B1_OFF', 'B0prime_RERUN': 'B0prime_RERUN'}      # A92; FIELDS r12 B1 / B1_OFF / B0prime_RERUN
CERT_KEYS = ('EPS', 'LO', 'GQ', 'DOUBLING', 'EPS_NGC', 'LO_NGC', 'I1T_NGC')
CERT_GATE_OF = {'EPS': 'EPS', 'LO': 'LO', 'GQ': 'GQ', 'DOUBLING': 'DOUBLING', 'EPS_NGC': 'EPS', 'LO_NGC': 'LO_NGC', 'I1T_NGC': 'I1T_NGC'}
NGC_CERTS = ('EPS_NGC', 'LO_NGC', 'I1T_NGC')
LAUNCH_KEYS = ('build', 'bound_plan', 'bound_command')
ADMISSION_KEYS = ('launcher', 'guard')
TEXT_OF_RECORD_PENDING = 'PENDING_PREREG_R5_TEXT_OF_RECORD'
TEXT_OF_RECORD_SHA = TEXT_OF_RECORD_PENDING      # prereg r5 (A99): a pin-only successor sets the sha once root rules r5 the text of record
NOT_APPLICABLE_R5 = 'NOT_APPLICABLE_R5'
NOT_APPLICABLE_R6 = 'NOT_APPLICABLE_R6'
NAMED_BUILD_PATH = ('seal_slots', 'launch_packet', 'named_candidates_verified_from_bytes', 'build')
NAMED_TEMPLATE_PATH = ('seal_slots', 'launch_packet', 'named_candidates_verified_from_bytes', 'template_plan')   # prereg r5 names it
BUILD_FILL = '<BUILD_V007_SHA_FILLED_AT_SEAL>'
CASCADE_ADDENDUM_PREFIX = 'CASCADE_MAP_R5_ADDENDUM'
COMPARE_API = ('validate_case_block', 'activate_driver_build', 'load_driver_build_record', 'load_strict_file', 'registered_gas_M_s',
               'PRODUCTION_GAS_M_S_A57', 'NGC_GAS_M_S_A57', 'CASE_BLOCK_SCHEMA', 'GATE_SCHEMA', 'ROUTE_A_MODES', 'ROUTE_A_MODE_DEFAULT')
A57_DDO_M_S = 128
# D-01: an M_s-type key (FIELDS r12): M_s, gas_M_s, source_gas_M_s, ddo_gas_M_s, ngc_gas_M_s, gas_M_s_DDO, gas_M_s_NGC,
# tail_config_gas/M_s, build/roster_gas/M_s, ...; M_s_doubled is checked as 2 M_s, never as an M_s
MS_KEY_RX = re.compile(r'(?:^|[_/])M_s(?:_(?:DDO|NGC))?$')
CONTEXT_KEYS = ('roster', 'name', 'geometry', 'part_roster_name', 'galaxy')


def blank_slot_values(doc):
    d = copy.deepcopy(doc)
    for v in (d.get('seal_slots') or {}).values():
        if isinstance(v, dict) and 'value' in v:
            v['value'] = '<SLOT>'
    return d


def dig(doc, path):
    cur = doc
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


def ms_values(o, path='$', ngc=False):
    """(path, value, side) for every M_s-type scalar; side 'NGC' or 'DDO', or 'AMBIGUOUS' for a key naming both. A key naming DDO or
    NGC decides; otherwise a dict whose roster/name/geometry/galaxy names NGC, or a parent key naming NGC, marks its subtree NGC."""
    out = []
    if isinstance(o, dict):
        here = ngc or any(isinstance(o.get(k), str) and 'NGC' in o[k].upper() for k in CONTEXT_KEYS)
        for k, v in o.items():
            p = path + '.' + k
            ku = k.upper()
            kn = here or 'NGC' in ku
            if MS_KEY_RX.search(k) and not isinstance(v, (dict, list)):
                if 'DDO' in ku and 'NGC' in ku:
                    side = 'AMBIGUOUS'
                elif 'DDO' in ku:
                    side = 'DDO'
                elif 'NGC' in ku or kn:
                    side = 'NGC'
                else:
                    side = 'DDO'
                out.append((p, v, side))
            out += ms_values(v, p, kn)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += ms_values(v, '%s[%d]' % (path, i), ngc)
    return out


def _int(v):
    return type(v) is int


def certificate_ms_codes(chk, k, rec, ddo, ngc):
    """D-01: the per-kind M_s fields of FIELDS r12, then every other M_s-type field; returns the number of M_s fields read."""
    seen = set()
    n = 0

    def want_eq(path, v, want, why):
        seen.add(path)
        if not _int(v) or v != want:
            chk.fail('CERTIFICATE_M_S', '%s %s = %r, want %r (%s)' % (k, path, v, want, why))
    if k == 'LO':
        v = rec.get('source_gas_M_s')
        if 'source_gas_M_s' not in rec:
            chk.fail('CERTIFICATE_STATES_NO_M_S', 'LO must state source_gas_M_s (FIELDS r12 LO; A68)')
        else:
            n += 1
            want_eq('$.source_gas_M_s', v, ddo, 'the registered uv_tail gas.M_s, A68 CHK-1')
            for echo in (('gas_M_s',), ('tail_config_gas', 'M_s'), ('build', 'roster_gas', 'M_s')):          # A73 F2; FIELDS r12 LO echoes
                e = dig(rec, echo)
                if e is not None:
                    n += 1
                    want_eq('$.' + '.'.join(echo), e, v, 'an echo equals source_gas_M_s, A73 F2')
    elif k == 'GQ':
        rs = rec.get('rosters')
        if not (isinstance(rs, list) and rs):
            chk.fail('CERTIFICATE_STATES_NO_M_S', 'GQ must state rosters[].M_s (FIELDS r12 GQ)')
        else:
            for j, r in enumerate(rs):
                if not isinstance(r, dict) or 'M_s' not in r:
                    chk.fail('CERTIFICATE_STATES_NO_M_S', 'GQ rosters[%d] must state M_s (FIELDS r12 GQ)' % j)
                    continue
                n += 1
                name = r.get('roster')
                is_ngc = isinstance(name, str) and name.upper().startswith('NGC')
                want_eq('$.rosters[%d].M_s' % j, r['M_s'], ngc if is_ngc else ddo, 'NGC_T120L at the NGC M_s, DDO rosters at the registered M_s')
                d = r.get('M_s_doubled')
                seen.add('$.rosters[%d].M_s_doubled' % j)
                if not (_int(d) and _int(r['M_s']) and d == 2 * r['M_s']):
                    chk.fail('CERTIFICATE_M_S_DOUBLED', 'GQ rosters[%d].M_s_doubled = %r, want 2 x M_s (FIELDS r12 GQ)' % (j, d))
    elif k == 'DOUBLING':
        if 'ddo_gas_M_s' not in rec:
            chk.fail('CERTIFICATE_STATES_NO_M_S', 'DOUBLING must state ddo_gas_M_s (FIELDS r12 DOUBLING; A73)')
        else:
            n += 1
            want_eq('$.ddo_gas_M_s', rec['ddo_gas_M_s'], ddo, 'FIELDS r12 DOUBLING ddo_gas_M_s; A73')
    for path, v, side in ms_values(rec, '$', k in NGC_CERTS):
        if path in seen:
            continue
        n += 1
        if side == 'AMBIGUOUS':
            chk.fail('CERTIFICATE_M_S_CONTEXT_AMBIGUOUS', '%s %s names both DDO and NGC' % (k, path))
            continue
        want = ngc if (side == 'NGC' or k in NGC_CERTS) else ddo
        want_eq(path, v, want, 'NGC context' if want == ngc and (side == 'NGC' or k in NGC_CERTS) else 'DDO context')
    return n


def ngc_stated(rec, k):
    return [v for _, v, side in ms_values(rec, '$', k in NGC_CERTS) if side == 'NGC' or k in NGC_CERTS]


def _run(slots_path, prereg_path, text_of_record_path, frozen=None, covered_later=(), reviewed=None, sealed_compare=None, text_of_record_sha=None):
    chk = C.Checker('check_slot_fill_c4v003')
    passthrough = {}
    try:
        slots = C.strict_json(slots_path)
        sp = C.strict_json(prereg_path)
        tor = C.strict_json(text_of_record_path)
    except Exception as e:
        chk.fail('INPUT_JSON', type(e).__name__ + ': ' + str(e))
        return chk.result()
    if not (isinstance(slots, dict) and isinstance(sp, dict) and isinstance(tor, dict)):
        chk.fail('INPUT_SHAPE', 'the slots, the sealed prereg and the text of record must be JSON objects')
        return chk.result()
    tor_sha = C.sha(text_of_record_path)
    passthrough['text_of_record'] = {'path': str(Path(text_of_record_path).resolve()), 'sha256': tor_sha}
    if TEXT_OF_RECORD_SHA != TEXT_OF_RECORD_PENDING:
        passthrough['text_of_record_pinned_by'] = 'TOOL_CONSTANT'
        if tor_sha != TEXT_OF_RECORD_SHA:
            chk.fail('TEXT_OF_RECORD_NOT_R5', 'the text of record is prereg r5 %s' % TEXT_OF_RECORD_SHA[:8])
        if text_of_record_sha is not None and text_of_record_sha != TEXT_OF_RECORD_SHA:
            chk.fail('TEXT_OF_RECORD_SHA_ARG_DIFFERS', 'the stated sha differs from the tool\'s pin %s' % TEXT_OF_RECORD_SHA[:8])
    elif text_of_record_sha is None:
        chk.fail('TEXT_OF_RECORD_PIN_PENDING', 'tool 3 v002 binds the prereg r5 text of record: root states its sha (--text-of-record-sha) until a '
                 'pin-only successor sets it (gap; the other layers are still checked)')
    elif not (isinstance(text_of_record_sha, str) and C.HEX64.fullmatch(text_of_record_sha)) or text_of_record_sha != tor_sha:
        chk.fail('TEXT_OF_RECORD_SHA_ARG_MISMATCH', 'the stated text-of-record sha is not the file\'s bytes (%s)' % tor_sha[:8])
    else:
        passthrough['text_of_record_pinned_by'] = 'ROOT_ARGUMENT'
        chk.note('TEXT_OF_RECORD_FROM_ROOT_ARGUMENT', 'root stated the text-of-record sha %s; the SEAL_RECORD records it' % tor_sha[:8])
    if set(slots) != set(SLOT_KEYS):
        chk.fail('SLOT_KEYS', 'missing %s; extra %s' % (sorted(set(SLOT_KEYS) - set(slots)), sorted(set(slots) - set(SLOT_KEYS))))
        return chk.result()
    if slots['schema'] != SCHEMA:
        chk.fail('SLOT_SCHEMA', repr(slots['schema']))
    br = slots['driver_branch']
    if br not in ('r5', 'r6'):
        chk.fail('DRIVER_BRANCH', repr(br))
    ngc_ms = slots['ngc_gas_M_s']
    if type(ngc_ms) is not int or ngc_ms not in (96, 128):
        chk.fail('NGC_GAS_M_S', '96, or 128 under A81 RI-23: %r' % (ngc_ms,))
    passthrough['ngc_gas_M_s'] = ngc_ms
    C.no_pending_anywhere(chk, 'slots', {k: v for k, v in slots.items() if k != 'cache_directory_r6_only'})
    # ---- pins (D-08: every pin is checked; later layers read only verified pins)
    for k in ('frozen_addendum', 'driver', 'driver_build_record', 'driver_check_record', 'compare_reviewed_source', 'identity_comparator', 'producer_registry'):
        chk.pin(k, slots[k])
    for group, keys in (('identity_gate_records', IDENTITY_KEYS), ('launch_packet', LAUNCH_KEYS), ('certificates', CERT_KEYS), ('admission_entry', ADMISSION_KEYS)):
        g = slots[group]
        if not isinstance(g, dict) or set(g) != set(keys):
            chk.fail('SLOT_GROUP_KEYS', '%s must have exactly %s' % (group, ', '.join(keys)))
            continue
        for k in keys:
            chk.pin('%s.%s' % (group, k), g[k])
    ok = lambda *labels: all(x in chk.pins for x in labels)

    def skipped(layer, *labels):
        chk.note('LAYER_SKIPPED', '%s: needs verified %s' % (layer, ', '.join(x for x in labels if x not in chk.pins)))
    # ---- cache directory (A81 RI-24) and the CASCADE_MAP_R5_ADDENDUM slot (SRR[9], A69)
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
    cma = slots['cascade_map_r5_addendum']
    cma_ok = False
    if br == 'r5':
        if cma == NOT_APPLICABLE_R6 or not isinstance(cma, dict):
            chk.fail('CASCADE_MAP_R5_ADDENDUM_REQUIRED_UNDER_R5', 'the immutable inventory addendum must exist before the seal under r5 (SRR[9], A69)')
        elif chk.pin('cascade_map_r5_addendum', cma):
            cma_ok = True
            if not Path(cma['path']).name.startswith(CASCADE_ADDENDUM_PREFIX):
                chk.fail('CASCADE_MAP_R5_ADDENDUM_NAME', Path(cma['path']).name)
            raw = Path(cma['path']).read_bytes()
            try:
                C.strict_json_bytes(raw)
            except C.DuplicateKey as e:
                chk.fail('CASCADE_MAP_R5_ADDENDUM_JSON', str(e))
            except C.json.JSONDecodeError:
                pass                                                            # a Markdown addendum is allowed (not JSON at all)
            except ValueError as e:                                             # A102 (A-B1 class, Claude4 main-loop patch): no text fallback on any other ValueError
                chk.fail('CASCADE_MAP_R5_ADDENDUM_JSON', '%s: %s' % (type(e).__name__, str(e)[:200]))
            passthrough['cascade_map_r5_addendum'] = dict(cma)
    elif br == 'r6':
        if cma != NOT_APPLICABLE_R6:
            chk.fail('CASCADE_MAP_R5_ADDENDUM_UNDER_R6', 'r6 names no r5 cascade addendum; use %s' % NOT_APPLICABLE_R6)
    # ---- the sealed prereg = the text of record except the slot values (and the one BUILD_V007 seal-time fill)
    tor_named = dig(tor, NAMED_BUILD_PATH)
    fill_allowed = isinstance(tor_named, dict) and tor_named.get('sha256') == C.PENDING_BUILD_V007

    def blanked(doc):
        d = blank_slot_values(doc)
        nb = dig(d, NAMED_BUILD_PATH)
        if fill_allowed and isinstance(nb, dict) and 'sha256' in nb:
            nb['sha256'] = BUILD_FILL
        return d
    if blanked(sp) != blanked(tor):
        chk.fail('SEALED_PREREG_TEXT_CHANGED', 'the sealed prereg differs from the text of record outside seal_slots.<k>.value')
    ss = sp.get('seal_slots') if isinstance(sp.get('seal_slots'), dict) else {}
    for pk in ss:
        if pk not in PREREG_SLOT_OF and pk not in OPTIONAL_PREREG_SLOT_OF:
            chk.fail('PREREG_SLOT_UNKNOWN', '%s: this tool does not know that slot, so it cannot check its value' % pk)
    for pk, sk in list(PREREG_SLOT_OF.items()) + [(k, v) for k, v in OPTIONAL_PREREG_SLOT_OF.items() if k in ss]:
        if pk not in ss:
            chk.fail('PREREG_SLOT_MISSING', pk)
            continue
        if not isinstance(ss[pk], dict):
            chk.fail('PREREG_SLOT_SHAPE', pk)
            continue
        if ss[pk].get('value') != slots[sk]:
            chk.fail('PREREG_SLOT_VALUE_DIFFERS', pk)
    C.no_pending_anywhere(chk, 'sealed prereg slot values', {k: v.get('value') for k, v in ss.items()
                                                             if isinstance(v, dict) and (k != 'cache_directory_r6_only' or br == 'r6')})
    passthrough['pending_strings_outside_slot_values'] = C.pending_paths(blank_slot_values(sp))
    # ---- D-10: the frozen addendum slot sits at path_to_be
    ptb = ((ss.get('frozen_addendum') or {}) if isinstance(ss.get('frozen_addendum'), dict) else {}).get('path_to_be')
    if not (isinstance(ptb, str) and Path(ptb).is_absolute()):
        chk.fail('FROZEN_PATH_TO_BE_ABSENT', 'seal_slots.frozen_addendum.path_to_be (D-10)')
    elif isinstance(slots['frozen_addendum'], dict) and slots['frozen_addendum'].get('path') != ptb:
        chk.fail('FROZEN_SLOT_NOT_PATH_TO_BE', 'the frozen_addendum slot path must be %s (D-10)' % ptb)
    # ---- A99.1: BUILD_V007, named by the prereg's launch-packet slot
    named = dig(sp, NAMED_BUILD_PATH)
    lp = slots['launch_packet'] if isinstance(slots['launch_packet'], dict) else {}
    build_ok = False
    allow = None
    build_text = ''
    if not (isinstance(named, dict) and set(named) == {'path', 'sha256'} and isinstance(named['path'], str) and isinstance(named['sha256'], str)
            and Path(named['path']).is_absolute()):
        chk.fail('BUILD_NAMED_SHAPE', 'seal_slots.launch_packet.named_candidates_verified_from_bytes.build must be {path, sha256}: %r' % (named,))
    else:
        if Path(named['path']).name != C.BUILD_V007_NAME:
            chk.fail('BUILD_NOT_BUILD_V007', 'the launch-packet BUILD of record is BUILD_V007 (A99.1); the prereg names %s' % Path(named['path']).name)
        if named['sha256'] == C.PENDING_BUILD_V007:
            chk.fail('BUILD_V007_PENDING', 'the prereg holds the literal %s: BUILD_V007 has not landed (gap, A99.1)' % C.PENDING_BUILD_V007)
        elif chk.pin('named_build', named):
            build_ok = Path(named['path']).name == C.BUILD_V007_NAME
            if fill_allowed:
                chk.note('BUILD_V007_SHA_FILLED_AT_SEAL', 'the text of record holds %s; the sealed prereg fills that leaf (verified from bytes)' % C.PENDING_BUILD_V007)
        if lp.get('build') != named:
            chk.fail('BUILD_NOT_THE_PREREG_NAMED_BUILD', 'the prereg names %r' % (named,))
            build_ok = False
    if build_ok and ok('launch_packet.build'):
        build_text = Path(named['path']).read_bytes().decode('utf-8')
        allow = C.build_allowlist_codes(chk, build_text)
        if allow is not None:
            passthrough['build'] = dict(named)
            passthrough['admission_allowlist'] = dict(allow)
    elif not build_ok:
        skipped('BUILD_V007 allowlist', 'named_build')
    # ---- bound plan and command; the admission-config launcher and guard (SRR[10], A78 N2)
    plan = None
    if ok('launch_packet.bound_plan'):
        try:
            plan = C.strict_json(lp['bound_plan']['path'])
        except Exception as e:
            chk.fail('BOUND_PLAN_JSON', type(e).__name__ + ': ' + str(e))
    else:
        skipped('bound plan', 'launch_packet.bound_plan')
    if isinstance(plan, dict):
        if plan.get('driver') != slots['driver']:
            chk.fail('PLAN_DRIVER_NOT_THE_SLOT', 'exact path/sha equality is required (launcher v007)')
        if plan.get('frozen_addendum') != slots['frozen_addendum']:
            chk.fail('PLAN_ADDENDUM_NOT_THE_SLOT', 'exact path/sha equality is required (launcher v007)')
        if allow is None:
            skipped('plan launcher/guard/template vs BUILD_V007', 'named_build')
        else:
            for k in ADMISSION_KEYS:
                ref = plan.get(k)
                if not (isinstance(ref, dict) and allow.get(ref.get('path')) == ref.get('sha256')):
                    chk.fail('PLAN_%s_NOT_BUILD_SUPPORTED' % k.upper(), repr(ref))
                else:
                    chk.pin('plan.' + k, ref)
            tp = plan.get('template_pin')
            if not (isinstance(tp, dict) and chk.pin('plan.template_pin', tp) and ('%s  %s' % (tp['sha256'], tp['path'])) in build_text):
                chk.fail('PLAN_TEMPLATE_NOT_NAMED_IN_BUILD', repr(tp))
        named_tp = dig(sp, NAMED_TEMPLATE_PATH)
        if isinstance(named_tp, dict) and plan.get('template_pin') != named_tp:
            chk.fail('PLAN_TEMPLATE_NOT_THE_PREREG_NAMED_TEMPLATE', 'the binder must bind the template the prereg names (%s)' % str(named_tp.get('sha256'))[:8])
        if not str(plan.get('seal_binding_status', '')).startswith('BOUND'):
            chk.fail('PLAN_NOT_BOUND', repr(plan.get('seal_binding_status')))
        calls = plan.get('calls') if isinstance(plan.get('calls'), list) else []
        for i, call in enumerate(calls):
            chk.pin('plan.calls[%d].spec' % i, call.get('spec') if isinstance(call, dict) else None)
        if len(calls) != 10:
            chk.fail('PLAN_CALLS', 'ten calls expected')
        if ok('launch_packet.bound_command'):
            cmd = Path(lp['bound_command']['path']).read_bytes().decode('utf-8').splitlines()
            want = shlex.join([C.PYTHON, '-I', '-B', (plan.get('launcher') or {}).get('path', ''), str(Path(lp['bound_plan']['path']).resolve()), '--execute-root-only'])
            if not cmd or cmd[-1] != want or len(cmd) != 2:
                chk.fail('BOUND_COMMAND_NOT_THE_BINDER_LINE', 'expected: %s' % want)
        ae = slots['admission_entry']
        if isinstance(ae, dict) and set(ae) == set(ADMISSION_KEYS):
            if ae != {'launcher': plan.get('launcher'), 'guard': plan.get('guard')}:
                chk.fail('ADMISSION_ENTRY_NOT_THE_PLAN', 'the admission config must name exactly the bound plan\'s launcher and guard (SRR[10], A78 N2)')
            if allow is not None:
                for k in ADMISSION_KEYS:
                    if not (isinstance(ae[k], dict) and allow.get(ae[k].get('path')) == ae[k].get('sha256')):
                        chk.fail('ADMISSION_ENTRY_NOT_BUILD_SUPPORTED', '%s is not a supported BUILD_V007 entry' % k)
            if ok('admission_entry.launcher', 'admission_entry.guard'):
                passthrough['admission_entry'] = {k: dict(ae[k]) for k in ADMISSION_KEYS}
    # ---- the reviewed compare, in-process: driver BUILD record (activated), then the case block (D-04)
    M = None
    if ok('compare_reviewed_source'):
        try:
            M = C.load_reviewed_compare(slots['compare_reviewed_source']['path'], slots['compare_reviewed_source']['sha256'])
        except (Exception, SystemExit) as e:
            chk.fail('COMPARE_LOAD', '%s: %s' % (type(e).__name__, str(e)[:200]))
        if M is not None:
            missing = [a for a in COMPARE_API if not hasattr(M, a)]
            if missing:
                chk.fail('COMPARE_API_MISSING', ', '.join(missing))
                M = None
    else:
        skipped('reviewed compare (driver build, case block)', 'compare_reviewed_source')
    if M is not None:
        if type(ngc_ms) is int and ngc_ms != M.NGC_GAS_M_S_A57:
            chk.fail('NGC_GAS_M_S_NOT_THE_COMPARE_NGC_M_S', 'the slot says %r; the reviewed compare binds NGC_T120L to %r (A57; a 128 ruling under RI-23 '
                     'needs a compare successor)' % (ngc_ms, M.NGC_GAS_M_S_A57))
    if ok('driver_check_record'):                                               # r2 (A102 A-B1): independent of the compare's own parse
        try:
            C.json_or_text(Path(slots['driver_check_record']['path']).read_bytes())
        except ValueError as e:
            chk.fail('DRIVER_CHECK_RECORD_JSON_DEFECT', 'the check record is JSON with a defect (%s); the compare\'s text fallback must never admit '
                     'it (A102 A-B1)' % type(e).__name__)
    bld = None
    if M is not None and ok('driver_build_record'):
        try:
            obj, _ = M.load_driver_build_record(slots['driver_build_record']['path'], slots['driver_build_record']['sha256'])
            bld = M.activate_driver_build(obj)
        except SystemExit as e:
            chk.fail('DRIVER_BUILD_RECORD_REFUSED', '%s: %s' % (getattr(e, 'refusal_code', None), str(e)[:300]))
        except Exception as e:
            chk.fail('DRIVER_BUILD_RECORD_EXCEPTION', '%s: %s' % (type(e).__name__, str(e)[:200]))
        if isinstance(bld, dict):
            if bld.get('build') != br:
                chk.fail('DRIVER_BUILD_NOT_THE_BRANCH', 'the driver BUILD record is %r; the slot branch is %r' % (bld.get('build'), br))
            if bld.get('driver') != slots['driver']:
                chk.fail('DRIVER_BUILD_DRIVER_NOT_THE_SLOT', 'the driver BUILD record\'s driver must equal the driver slot (A72; launcher v007 byte equality)')
            if bld.get('check_record') != slots['driver_check_record']:
                chk.fail('DRIVER_BUILD_CHECK_RECORD_NOT_THE_SLOT', 'sealed mode needs the build\'s check_record = PIN_V010_R5_CHECK = the driver_check_record slot')
            passthrough['driver_build'] = {'build': bld.get('build'), 'driver': bld.get('driver'), 'cascade_map': bld.get('cascade_map'),
                                           'check_record': bld.get('check_record')}
            if cma_ok and isinstance(bld.get('cascade_map'), dict):
                ms_ = bld['cascade_map'].get('sha256', '')
                txt = Path(cma['path']).read_bytes().decode('utf-8', 'replace')
                if not (isinstance(ms_, str) and len(ms_) == 64 and (ms_ in txt or ms_[:8] in txt)):
                    chk.fail('CASCADE_MAP_R5_ADDENDUM_DOES_NOT_NAME_THE_R5_MAP', 'the addendum must name the cascade map it extends (%s)' % str(ms_)[:8])
    elif M is not None:
        skipped('driver build record', 'driver_build_record')
    cb = None
    ddo_ms = None
    cbp = (sp.get('binding_inputs') or {}).get('case_block') if isinstance(sp.get('binding_inputs'), dict) else None
    if cbp is None:
        chk.fail('CASE_BLOCK_PIN_ABSENT', 'the sealed prereg must carry binding_inputs.case_block {path, sha256}: in sealed mode the compare reads it '
                 'only there (r12 L5706; D-03, D-04)')
    elif not C.is_pin(cbp):
        chk.fail('CASE_BLOCK_PIN_SHAPE', 'binding_inputs.case_block must be exactly {path (absolute), sha256 (64 hex)}: %r' % (cbp,))
    elif chk.pin('case_block', cbp):
        if M is None:
            chk.fail('CASE_BLOCK_NOT_VALIDATED', 'the reviewed compare is not loaded, so its validate_case_block cannot run')
        elif bld is None:
            chk.fail('CASE_BLOCK_NOT_VALIDATED', 'the driver BUILD record is not active (validate_case_block reads the sealed driver, r12 L5689)')
        else:
            try:
                cb = M.load_strict_file(cbp['path'], 'case block')
            except SystemExit as e:
                chk.fail('CASE_BLOCK_JSON', '%s' % getattr(e, 'refusal_code', None))
            if isinstance(cb, dict):
                srcs = [x for x in (sp.get('route_a_mode'), cb.get('route_a_mode')) if x is not None]
                mode = srcs[0] if srcs else M.ROUTE_A_MODE_DEFAULT
                if len(set(map(str, srcs))) > 1:
                    chk.fail('ROUTE_A_MODE_SOURCES_DIFFER', 'the prereg and the case block name different route-A modes (r12 L5719)')
                try:
                    why = M.validate_case_block(cb, route_a_mode=mode)
                except SystemExit as e:
                    why = ['REFUSED %s' % getattr(e, 'refusal_code', None)]
                except Exception as e:
                    why = ['EXCEPTION %s' % type(e).__name__]
                if why:
                    chk.fail('CASE_BLOCK_INVALID', '%d reason(s) from the reviewed compare\'s validate_case_block: %s' % (len(why), '; '.join(str(w) for w in why[:4])[:600]))
                else:
                    ddo_ms = M.registered_gas_M_s({'case_block': cb})
                    km = cb.get('key_equivalence_map', [])
                    passthrough['case_block'] = dict(cbp)
                    passthrough['route_a_mode'] = mode
                    passthrough['key_equivalence_map'] = km
                    passthrough['ddo_gas_M_s_registered'] = ddo_ms
            elif cb is not None:
                chk.fail('CASE_BLOCK_JSON', 'the case block is not a JSON object')
    if ddo_ms is None:
        ddo_ms = M.PRODUCTION_GAS_M_S_A57 if M is not None else A57_DDO_M_S
        chk.note('DDO_M_S_FROM_THE_A57_CONSTANT', 'the case block is not validated; certificates are read against the A57 production M_s %r' % ddo_ms)
    if ddo_ms != A57_DDO_M_S or (M is not None and ddo_ms != M.PRODUCTION_GAS_M_S_A57):
        chk.fail('DDO_M_S_NOT_THE_A57_PRODUCTION_M_S', 'registered %r (A57: 128)' % (ddo_ms,))
    # ---- identity records (A67 N1, A81 RI-21; A92 records of record)
    gate_schema = M.GATE_SCHEMA if M is not None else 'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002'
    passthrough['gate_schema'] = gate_schema
    dsha = slots['driver']['sha256'] if isinstance(slots['driver'], dict) else None
    for k in IDENTITY_KEYS:
        if not ok('identity_gate_records.%s' % k):
            skipped('identity record %s' % k, 'identity_gate_records.%s' % k)
            continue
        try:
            rec = C.strict_json(slots['identity_gate_records'][k]['path'])
        except Exception as e:
            chk.fail('IDENTITY_RECORD_JSON', '%s: %s' % (k, e))
            continue
        if not isinstance(rec, dict):
            chk.fail('IDENTITY_RECORD_JSON', '%s is not a JSON object' % k)
            continue
        if rec.get('schema') != gate_schema or rec.get('gate') != IDENTITY_GATE_OF[k]:
            chk.fail('IDENTITY_RECORD_NOT_THE_SLOT_GATE', 'the %s slot holds the %s gate record (schema %s); got gate %r, schema %r'
                     % (k, IDENTITY_GATE_OF[k], gate_schema, rec.get('gate'), rec.get('schema')))
        # the NEW side must carry the driver slot (A67 N1, A81 RI-21); the reference side legitimately carries its own driver.
        raw = Path(slots['identity_gate_records'][k]['path']).read_bytes().decode('utf-8', 'replace')
        if not dsha or dsha not in raw:
            chk.fail('IDENTITY_RECORD_LACKS_DRIVER_SHA', '%s does not name the driver slot sha' % k)
        for path, v in C.find_key(rec, 'result_json_driver_sha256'):
            if v != dsha:
                chk.fail('IDENTITY_RECORD_NEW_DRIVER_SHA', '%s %s = %r' % (k, path, v))
        for path, v in C.find_key(rec, 'NEW_DRIVER_PIN'):
            okv = [x for _, x in C.find_key(v, 'passed') + C.find_key(v, 'pass') + C.find_key(v, 'ok')] if isinstance(v, dict) else [v]
            if any(x is not True for x in okv if isinstance(x, bool)) or not any(x is True for x in okv if isinstance(x, bool)):
                chk.fail('IDENTITY_RECORD_NEW_DRIVER_PIN_NOT_PASSED', '%s %s' % (k, path))
    # ---- certificates (D-01)
    for k in CERT_KEYS:
        if not ok('certificates.%s' % k):
            skipped('certificate %s' % k, 'certificates.%s' % k)
            continue
        try:
            rec = C.strict_json(slots['certificates'][k]['path'])
        except Exception as e:
            chk.fail('CERTIFICATE_JSON', '%s: %s' % (k, e))
            continue
        if not isinstance(rec, dict):
            chk.fail('CERTIFICATE_JSON', '%s is not a JSON object' % k)
            continue
        if rec.get('schema') != gate_schema or rec.get('gate') != CERT_GATE_OF[k]:
            chk.fail('CERTIFICATE_NOT_THE_SLOT_GATE', 'the %s slot holds a %s gate record (schema %s); got gate %r, schema %r'
                     % (k, CERT_GATE_OF[k], gate_schema, rec.get('gate'), rec.get('schema')))
        certificate_ms_codes(chk, k, rec, ddo_ms, ngc_ms)
        if ngc_ms == 128 and k in ('DOUBLING', 'LO_NGC') and 128 not in ngc_stated(rec, k):
            chk.fail('NGC_M_S_128_NOT_EVIDENCED', '%s: under RI-23 the NGC half is recomputed at M_s 128, and the record must state it' % k)
    # ---- optional: tools 1 and 2
    if frozen:
        import check_frozen_addendum_c4v003 as T1
        fa = slots['frozen_addendum'] if isinstance(slots['frozen_addendum'], dict) else {}
        r1 = T1.run(prereg_path, frozen, fa.get('sha256'), covered_later)
        if Path(frozen).resolve() != Path(fa.get('path', '/nonexistent')).resolve():
            chk.fail('FROZEN_ARG_NOT_THE_SLOT', str(frozen))
        for f in r1['failures']:
            chk.fail('T1:' + f['code'], f['detail'])
        passthrough['entry_table'] = r1.get('entry_table')
        passthrough['covered_later'] = r1.get('covered_later')
        passthrough['later_entries'] = r1.get('later_entries')
        passthrough['changed_sections'] = r1.get('changed_sections')
    if reviewed or sealed_compare:
        if not (reviewed and sealed_compare):
            chk.fail('COMPARE_ARGS', 'give both --reviewed and --sealed-compare')
        else:
            import check_sealed_compare_c4v003 as T2
            r2 = T2.run(reviewed, sealed_compare, slots_path, prereg_path)
            for f in r2['failures']:
                chk.fail('T2:' + f['code'], f['detail'])
            chk.pins['sealed_compare'] = r2['pins_verified'].get('sealed_compare')
    chk.pins['sealed_prereg'] = {'path': str(Path(prereg_path).resolve()), 'sha256': C.sha(prereg_path)}
    res = chk.result()
    res['passthrough'] = passthrough
    return res


def run(slots_path, prereg_path, text_of_record_path, frozen=None, covered_later=(), reviewed=None, sealed_compare=None, text_of_record_sha=None):
    return C.guarded_run('check_slot_fill_c4v003', _run, slots_path, prereg_path, text_of_record_path, frozen, covered_later, reviewed, sealed_compare,
                         text_of_record_sha)


def main(argv=None):
    p = C.parser('root slot values: from bytes, no PENDING, consistent across prereg, case block, compare pins, bound plan and BUILD_V007')
    p.add_argument('--slots', required=True)
    p.add_argument('--prereg', required=True)
    p.add_argument('--text-of-record', required=True)
    p.add_argument('--frozen')
    p.add_argument('--covered-later', default='')
    p.add_argument('--reviewed')
    p.add_argument('--sealed-compare')
    p.add_argument('--text-of-record-sha')
    a = C.parse_args(p, argv)
    cov = [x for x in a.covered_later.split(',') if x.strip()]
    return C.emit(run(a.slots, a.prereg, a.text_of_record, a.frozen, cov, a.reviewed, a.sealed_compare, a.text_of_record_sha))


if __name__ == '__main__':
    raise SystemExit(main())
