# Claude4 helper (dispatch 0650, V006 A113 P6 / RI-30): build seal tool 4's B7 key-equivalence-map input,
#   {"schema": KEY_MAP_SCHEMA, "key_equivalence_map": [], "note": "..."}
# after TESTING from bytes that the case block of record carries key_equivalence_map == [] at the place r13's validate_case_block
# (L1557) and tool 3 v003 (L482) read it: the top-level key of the case block JSON, cb.get('key_equivalence_map', []).
# Every input is pinned by full sha and verified from bytes; KEY_MAP_SCHEMA is read from tool 4's source by AST (never imported).
# Modes: --dry-run prints the exact bytes' sha and a summary (writes nothing); --write PATH creates PATH exclusively (open 'x').
# usage: make_key_map_c4v001.py --utc 2026-10-19T00:00:00Z (--dry-run | --write PATH)
import ast, hashlib, json, sys
from pathlib import Path

TOOL4 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/build_seal_record_c4v004.py',
         '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41')
CASE_BLOCK = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
              '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71')
PREREG_R6 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json',
             'd28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9')
COMPARE_R13 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py',
               'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157')
TOOL3 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/check_slot_fill_c4v003.py',
         '316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af')


class Refuse(Exception):
    pass


def read_pinned(pin):
    p, h = pin
    raw = Path(p).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != h:
        raise Refuse('PIN_MISMATCH %s has %s, pinned %s' % (p, got, h))
    return raw


def pairs(ps):
    out = {}
    for k, v in ps:
        if k in out:
            raise Refuse('DUPLICATE_JSON_KEY %r' % (k,))
        out[k] = v
    return out


def no_constant(c):
    raise Refuse('NON_FINITE_JSON_CONSTANT %s' % c)


def strict(raw):
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=no_constant)


def module_string(raw, name):
    vals = [n.value.value for n in ast.parse(raw.decode('utf-8')).body if isinstance(n, ast.Assign) and len(n.targets) == 1
            and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name and isinstance(n.value, ast.Constant)
            and isinstance(n.value.value, str)]
    if len(vals) != 1:
        raise Refuse('MODULE_STRING_NOT_UNIQUE %s' % name)
    return vals[0]


def build(utc):
    t4 = read_pinned(TOOL4)
    schema = module_string(t4, 'KEY_MAP_SCHEMA')
    cb_raw = read_pinned(CASE_BLOCK)
    cb = strict(cb_raw)
    if not isinstance(cb, dict) or 'key_equivalence_map' not in cb:
        raise Refuse('CASE_BLOCK_HAS_NO_TOP_LEVEL_KEY_EQUIVALENCE_MAP')
    km = cb['key_equivalence_map']
    if not (isinstance(km, list) and km == []):
        raise Refuse('CASE_BLOCK_KEY_EQUIVALENCE_MAP_IS_NOT_EMPTY_LIST %r' % (km,))
    pr = strict(read_pinned(PREREG_R6))
    if (pr.get('binding_inputs') or {}).get('case_block') != {'path': CASE_BLOCK[0], 'sha256': CASE_BLOCK[1]}:
        raise Refuse('PREREG_R6_BINDING_INPUTS_CASE_BLOCK_IS_NOT_THIS_CASE_BLOCK')
    cmp_txt = read_pinned(COMPARE_R13).decode('utf-8')
    if "    km = cb.get('key_equivalence_map', [])" not in cmp_txt:
        raise Refuse('R13_VALIDATE_CASE_BLOCK_READ_SITE_NOT_FOUND')
    t3_txt = read_pinned(TOOL3).decode('utf-8')
    if "km = cb.get('key_equivalence_map', [])" not in t3_txt or "passthrough['key_equivalence_map'] = km" not in t3_txt:
        raise Refuse('TOOL3_PASSTHROUGH_SITE_NOT_FOUND')
    me = Path(__file__).resolve()
    note = ('RI-30 (V006 A113): there is one key-equivalence map of record; the SEAL_RECORD map equals the validated case block\'s, []. '
            'TESTED from bytes by %s (sha256 %s) at %s: the case block of record %s (sha256 %s), parsed strictly (a duplicate key '
            'refuses), carries the top-level key key_equivalence_map = [] (an empty list); that is the place r13 validate_case_block '
            '(%s, sha256 %s; L1557) and seal tool 3 v003 (sha256 %s; L482, passed through to tool 4 build() as '
            'pt[key_equivalence_map]) read it, cb.get(key_equivalence_map, []). Prereg r6 (sha256 %s) binding_inputs.case_block pins '
            'exactly that path and sha. Tool 4 key_map_codes(chk, this object, the case block map) must report no failure.'
            % (me.name, hashlib.sha256(me.read_bytes()).hexdigest(), utc, CASE_BLOCK[0], CASE_BLOCK[1], COMPARE_R13[0], COMPARE_R13[1],
               TOOL3[1], PREREG_R6[1]))
    obj = {'schema': schema, 'key_equivalence_map': [], 'note': note}
    text = json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    return obj, text


def main(argv):
    if len(argv) != 4 or argv[0] != '--utc' or argv[2] not in ('--dry-run', '--write'):
        print('usage: make_key_map_c4v001.py --utc T (--dry-run X | --write PATH)', file=sys.stderr)
        return 2
    utc, mode, target = argv[1], argv[2], argv[3]
    try:
        obj, text = build(utc)
    except (Refuse, OSError, ValueError) as e:
        print('REFUSED: %s: %s' % (type(e).__name__, e), file=sys.stderr)
        return 2
    sha = hashlib.sha256(text.encode('utf-8')).hexdigest()
    if mode == '--dry-run':
        print('DRY_RUN_OK schema=%s map=%s bytes=%d sha256=%s' % (obj['schema'], obj['key_equivalence_map'], len(text.encode('utf-8')), sha))
        return 0
    with open(target, 'x', encoding='utf-8') as f:
        f.write(text)
    got = hashlib.sha256(Path(target).read_bytes()).hexdigest()
    print('WROTE %s sha256 %s (expected %s) %s' % (target, got, sha, 'MATCH' if got == sha else 'MISMATCH'))
    return 0 if got == sha else 3


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
