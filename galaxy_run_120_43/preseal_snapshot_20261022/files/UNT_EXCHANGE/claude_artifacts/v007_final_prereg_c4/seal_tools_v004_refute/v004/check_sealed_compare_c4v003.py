# Claude4 seal tools v003, tool 2 (r2 check_sealed_compare_c4v002.py aebb7b73 with only the v002->v003 renames; v002 succeeded
# check_sealed_compare_c4v001.py b339a8f6): the sealed compare differs from the
# reviewed source only in the five seal-time pin lines (A82), and each pin equals its slot. Read-only.
# Rules (unchanged from v001):
#  - same number of lines; every differing line is one of V007_PREREG_SHA256, PIN_ADDENDUM_V005, PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK,
#    PIN_PRODUCER_REGISTRY, each exactly once: `NAME = None<comment>` in the reviewed source, `NAME = <literal><same comment>` sealed;
#  - in both files each NAME is assigned exactly once anywhere in the module (AST), so no later assignment can override it;
#  - values: the two sha pins are 64-hex strings, the three file pins are (path, sha256) tuples, each equal to its expected value;
#  - the reviewed source sha equals the prereg's compare slot; the cited V005 addendum path is reported, and its current bytes must
#    hash to PIN_ADDENDUM_V005 (if the compare cites the open addendum path, later writes to that file will make the sealed compare refuse).
# New in v002 (D-07): the five slots a pin is built from (compare_reviewed_source, frozen_addendum, driver_build_record,
# driver_check_record, producer_registry) must each be an exact {path, sha256} pin before any pin is computed; a bare PENDING string,
# a list or a partial object refuses PIN_SHAPE (a code, never a TypeError), and any other unexpected exception refuses
# INTERNAL_EXCEPTION:<type>.
# usage: python3 -I -B check_sealed_compare_c4v003.py --reviewed R.py --sealed S.py --slots SLOTS.json --prereg SEALED_PREREG.json
import ast, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seal_common_c4v003 as C

SHA_PINS = ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005')
FILE_PINS = ('PIN_DRIVER_BUILD_RECORD', 'PIN_V010_R5_CHECK', 'PIN_PRODUCER_REGISTRY')
PIN_SLOTS = ('compare_reviewed_source', 'frozen_addendum', 'driver_build_record', 'driver_check_record', 'producer_registry')


def expected_pins(slots, prereg_path):
    return {'V007_PREREG_SHA256': C.sha(prereg_path), 'PIN_ADDENDUM_V005': slots['frozen_addendum']['sha256'],
            'PIN_DRIVER_BUILD_RECORD': (slots['driver_build_record']['path'], slots['driver_build_record']['sha256']),
            'PIN_V010_R5_CHECK': (slots['driver_check_record']['path'], slots['driver_check_record']['sha256']),
            'PIN_PRODUCER_REGISTRY': (slots['producer_registry']['path'], slots['producer_registry']['sha256'])}


def split_assignment(line, name):
    """'NAME = <rhs>   # comment' -> (rhs, comment) using the tokenizer-safe AST of the statement part."""
    body = line.rstrip('\n')
    m = re.match(r'^%s = (.*)$' % re.escape(name), body)
    if not m:
        return None
    rest = m.group(1)
    # find the first '#' outside a string literal
    q, i = None, 0
    while i < len(rest):
        ch = rest[i]
        if q:
            if ch == '\\':
                i += 2
                continue
            if ch == q:
                q = None
        elif ch in '\'"':
            q = ch
        elif ch == '#':
            return rest[:i].rstrip(), rest[i:]
        i += 1
    return rest.rstrip(), ''


def assign_counts(tree):
    cnt = {n: 0 for n in C.PIN_NAMES}
    for node in ast.walk(tree):
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            targets = [node.target]
        for t in targets:
            for sub in ast.walk(t):
                if isinstance(sub, ast.Name) and sub.id in cnt:
                    cnt[sub.id] += 1
        if isinstance(node, ast.Global):
            for n in node.names:
                if n in cnt:
                    cnt[n] += 100   # any `global PIN` makes a function-level rebinding possible: refuse
    return cnt


def module_strings(tree):
    env = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            v = node.value
            try:
                env[node.targets[0].id] = eval_str(v, env)
            except ValueError:
                pass
    return env


def eval_str(v, env):
    if isinstance(v, ast.Constant) and isinstance(v.value, str):
        return v.value
    if isinstance(v, ast.Name) and v.id in env:
        return env[v.id]
    if isinstance(v, ast.BinOp) and isinstance(v.op, ast.Add):
        return eval_str(v.left, env) + eval_str(v.right, env)
    raise ValueError('not a string expression')


def _run(reviewed, sealed, slots_path, prereg_path):
    chk = C.Checker('check_sealed_compare_c4v003')
    try:
        slots = C.strict_json(slots_path)
        prereg = C.strict_json(prereg_path)
    except Exception as e:
        chk.fail('INPUT_JSON', type(e).__name__ + ': ' + str(e))
        return chk.result()
    if not isinstance(slots, dict) or not isinstance(prereg, dict):
        chk.fail('INPUT_SHAPE', 'the slots and the prereg must be JSON objects')
        return chk.result()
    for k in PIN_SLOTS:
        if k not in slots:
            chk.fail('SLOT_MISSING', k)
        elif not (isinstance(slots[k], dict) and set(slots[k]) == {'path', 'sha256'}
                  and isinstance(slots[k]['path'], str) and isinstance(slots[k]['sha256'], str)):
            chk.fail('PIN_SHAPE', '%s must be an exact {path, sha256} pin before the sealed compare is checked (D-07): %r' % (k, slots[k]))
    if chk.failures:
        return chk.result()
    rv, sv = Path(reviewed), Path(sealed)
    chk.pin('reviewed_source', slots['compare_reviewed_source'])
    if not rv.is_file() or str(rv.resolve()) != str(Path(slots['compare_reviewed_source']['path']).resolve()):
        chk.fail('REVIEWED_PATH_NOT_THE_SLOT', '%s vs slot %s' % (rv, slots['compare_reviewed_source']['path']))
    pslot = ((prereg.get('seal_slots') or {}).get('compare') or {}).get('value')
    if pslot != slots['compare_reviewed_source']:
        chk.fail('PREREG_COMPARE_SLOT_DIFFERS', 'the sealed prereg\'s compare slot must hold the reviewed source pin (A82)')
    if not sv.is_file():
        chk.fail('SEALED_MISSING', str(sv))
        return chk.result()
    if not rv.is_file():
        return chk.result()
    if rv.resolve() == sv.resolve():
        chk.fail('SEALED_IS_REVIEWED', 'the sealed compare must be a separate file')
    r_text, s_text = rv.read_bytes().decode('utf-8'), sv.read_bytes().decode('utf-8')
    R, S = r_text.splitlines(keepends=True), s_text.splitlines(keepends=True)
    if len(R) != len(S):
        chk.fail('LINE_COUNT_DIFFERS', '%d reviewed vs %d sealed' % (len(R), len(S)))
        return chk.result()
    exp = expected_pins(slots, prereg_path)
    seen = {}
    for i, (a, b) in enumerate(zip(R, S)):
        if a == b:
            continue
        name = next((n for n in C.PIN_NAMES if a.startswith(n + ' = ')), None)
        if name is None or not b.startswith(name + ' = '):
            chk.fail('NON_PIN_LINE_DIFFERS', 'line %d' % (i + 1))
            continue
        if name in seen:
            chk.fail('PIN_LINE_DIFFERS_TWICE', name)
            continue
        seen[name] = i + 1
        ra, rb = split_assignment(a, name), split_assignment(b, name)
        if ra is None or rb is None:
            chk.fail('PIN_LINE_SHAPE', name)
            continue
        if ra[0] != 'None':
            chk.fail('REVIEWED_PIN_NOT_UNSET', '%s in the reviewed source is %s' % (name, ra[0]))
        if ra[1] != rb[1]:
            chk.fail('PIN_COMMENT_CHANGED', name)
        if not (a.endswith('\n') == b.endswith('\n')):
            chk.fail('PIN_LINE_ENDING_CHANGED', name)
        try:
            val = ast.literal_eval(rb[0])
        except Exception:
            chk.fail('PIN_VALUE_NOT_A_LITERAL', name)
            continue
        want = exp[name]
        if name in SHA_PINS:
            if not (isinstance(val, str) and C.HEX64.fullmatch(val)):
                chk.fail('PIN_SHA_FORMAT', name)
            elif val != want:
                chk.fail('PIN_VALUE_MISMATCH', '%s = %s, slot %s' % (name, val, want))
        else:
            if not (isinstance(val, tuple) and len(val) == 2 and all(isinstance(x, str) for x in val)):
                chk.fail('PIN_PAIR_SHAPE', '%s must be a (path, sha256) tuple' % name)
            elif val != want:
                chk.fail('PIN_VALUE_MISMATCH', '%s = %r, slot %r' % (name, val, want))
            else:
                chk.pin(name, {'path': val[0], 'sha256': val[1]})
    for n in C.PIN_NAMES:
        if n not in seen:
            chk.fail('PIN_NOT_SET', n)
    for label, text in (('reviewed', r_text), ('sealed', s_text)):
        try:
            tree = ast.parse(text)
        except SyntaxError as e:
            chk.fail('SYNTAX', '%s: %s' % (label, e))
            continue
        cnt = assign_counts(tree)
        bad = {n: c for n, c in cnt.items() if c != 1}
        if bad:
            chk.fail('PIN_ASSIGNED_NOT_EXACTLY_ONCE', '%s: %r' % (label, bad))
        if label == 'sealed':
            env = module_strings(tree)
            cited = env.get('ADDENDUM_V005_CITED')
            if cited is None:
                chk.note('ADDENDUM_PATH_NOT_FOUND', 'no module-level ADDENDUM_V005_CITED string in the sealed compare')
            else:
                chk.notes.append({'code': 'ADDENDUM_V005_CITED', 'detail': cited})
                if not cited.endswith('_V005_ADDENDUM_FROZEN.md'):
                    chk.note('CITES_OPEN_ADDENDUM_PATH', 'the compare hashes the open addendum path, not the frozen copy: any later write to that file makes '
                             'the sealed compare refuse (fail-closed); root must stop writing to it after the freeze, or the compare should cite the frozen copy')
                if not Path(cited).is_file():
                    chk.fail('CITED_ADDENDUM_MISSING', cited)
                elif C.sha(cited) != exp['PIN_ADDENDUM_V005']:
                    chk.fail('CITED_ADDENDUM_BYTES_NOT_PINNED', 'the file the compare hashes does not hash to PIN_ADDENDUM_V005 now: the sealed compare would refuse')
    chk.pins['sealed_compare'] = {'path': str(sv.resolve()), 'sha256': C.sha(sv)}
    return chk.result()


def run(reviewed, sealed, slots_path, prereg_path):
    return C.guarded_run('check_sealed_compare_c4v003', _run, reviewed, sealed, slots_path, prereg_path)


def main(argv=None):
    p = C.parser('sealed compare vs reviewed source: only the five seal-time pins may differ (A82)')
    p.add_argument('--reviewed', required=True)
    p.add_argument('--sealed', required=True)
    p.add_argument('--slots', required=True)
    p.add_argument('--prereg', required=True)
    a = C.parse_args(p, argv)
    return C.emit(run(a.reviewed, a.sealed, a.slots, a.prereg))


if __name__ == '__main__':
    raise SystemExit(main())
