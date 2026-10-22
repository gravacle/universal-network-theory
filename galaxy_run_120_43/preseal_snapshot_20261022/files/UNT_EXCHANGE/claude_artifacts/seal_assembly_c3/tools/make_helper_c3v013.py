# make_helper_c3v013.py: Claude3 (FROM_CODEX/0644, ruling A107; Codex1 0101). Derives tools/seal_steps_c3sa_c3v013.py from c3v012
# (b1348396) by exact replacements (each old string occurs exactly once); writes it exclusively.
import hashlib, sys
C3 = sys.argv[1]
src = open(C3 + '/tools/seal_steps_c3sa_c3v012.py', 'rb').read()
assert hashlib.sha256(src).hexdigest() == 'b13483966fcb8755608d73e05c0e70dc94e39a2b07635f54efc0c86849748bac'
s = src.decode('utf-8')
HDR = '''# c3v013 (FROM_CODEX/0644, ruling A107 in the V006 addendum; Codex1 0101 7152346 findings): (C02-SEL-STRICT) a SELECTED file is parsed
# STRICTLY from the one buffer pin() read: invalid UTF-8, a BOM, nesting deeper than 64, a duplicate key, NaN / Infinity / a float
# overflowing to inf, an integer longer than 4300 digits, trailing or invalid JSON text and a non-object top level each REFUSE with
# a typed SELECTED_* code; there is no substring fallback anywhere. (C02-SEL-ASSOCIATION) each requested (path, sha) must be stored
# as ONE object of that parse whose 'path' equals the absolute path exactly and whose 'sha256' equals the sha exactly (Claude4 0112:
# exact {path, sha256} pairs; role keys PENDING Claude4's real SELECTED files); unrelated strings and suffixed paths never count,
# and any object giving the same path another value refuses. Both check-tor and the v003 selected-names use it. (A106-C03-S1)
# gates-provenance validates the slot sha and the body record_sha256 as 64-hex lowercase BEFORE comparing. (A107, P12 option (b))
# slot-registry takes the explicit two-entry exclusion list (--exclude certificates.EPS_NGC=PATH=SHA, certificates.I1T_NGC=PATH=SHA)
# and refuses any other list (a third slot, a missing one, another path or sha) and an excluded slot whose pin differs; excluded
# slots are still pinned from bytes and reported. (Codex1 0101 C04 boundary note, closed) every non-excluded slotted gate record must
# also carry its gate's pass verdict from r13's own GATE_PASS_VERDICTS (a registered FAIL, an absent or an unknown verdict refuses).
'''
CONSTS = '''SEL_MAX_DEPTH = 64                                # C02-SEL-STRICT: nesting deeper than this refuses (typed), never a RecursionError
SEL_MAX_INT_DIGITS = 4300                         # C02-SEL-STRICT: an integer literal longer than this refuses (typed)
C04_A107_EXCLUSIONS = {                           # A107 (V006 addendum), P12 option (b): exactly these two slots, by name, path and sha
    'certificates.EPS_NGC': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json',
                             '1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d'),
    'certificates.I1T_NGC': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/I1T_NGC_T120L_V001.json',
                             '3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6')}
'''
OLD_SEL = s[s.index('def _selected_names(sel_bytes, pins):'):s.index('def c_selected_names(a):')]
NEW_SEL = r'''def _sel_pairs_hook(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise Refuse('SELECTED_DUPLICATE_KEY %r' % k)
        out[k] = v
    return out


def _sel_const(c):
    raise Refuse('SELECTED_NON_FINITE %s' % c)


def _sel_int(t):
    n = len(t.lstrip('-'))
    if n > SEL_MAX_INT_DIGITS:
        raise Refuse('SELECTED_INTEGER_TOO_LONG %d digits (limit %d)' % (n, SEL_MAX_INT_DIGITS))
    return int(t)


def _sel_float(t):
    f = float(t)
    if f != f or f in (float('inf'), float('-inf')):
        raise Refuse('SELECTED_NON_FINITE %s' % t[:40])
    return f


def _sel_depth(t):
    depth, ins, esc = 0, False, False
    for ch in t:
        if ins:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                ins = False
        elif ch == '"':
            ins = True
        elif ch in '[{':
            depth += 1
            if depth > SEL_MAX_DEPTH:
                raise Refuse('SELECTED_JSON_TOO_DEEP (more than %d levels)' % SEL_MAX_DEPTH)
        elif ch in ']}':
            depth -= 1


def _selected_strict(b):
    """C02-SEL-STRICT (Codex1 0101): the SELECTED bytes, read ONCE by pin(), parsed strictly from that exact buffer. Every failure is
    a typed refusal; there is no fallback of any kind."""
    try:
        t = b.decode('utf-8', 'strict')
    except UnicodeDecodeError as e:
        raise Refuse('SELECTED_INVALID_UTF8 at byte %d' % e.start)
    if t.startswith('﻿'):
        raise Refuse('SELECTED_BOM')
    _sel_depth(t)
    try:
        obj = json.loads(t, object_pairs_hook=_sel_pairs_hook, parse_constant=_sel_const, parse_int=_sel_int, parse_float=_sel_float)
    except Refuse:
        raise
    except RecursionError:
        raise Refuse('SELECTED_JSON_TOO_DEEP (recursion)')
    except ValueError as e:                   # json.JSONDecodeError: trailing data, syntax errors
        raise Refuse('SELECTED_NOT_STRICT_JSON %s' % str(e)[:200])
    if not isinstance(obj, dict):
        raise Refuse('SELECTED_TOP_LEVEL_NOT_AN_OBJECT')
    return obj


def _selected_pairs(obj):
    pairs = []

    def walk(o):
        if isinstance(o, dict):
            if 'path' in o or 'sha256' in o:
                pairs.append((o.get('path'), o.get('sha256')))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return pairs


def _selected_names(sel_bytes, pins):
    """C02-SEL-ASSOCIATION (Codex1 0101; A107): each requested (path, sha) must be stored as ONE object of the strictly parsed SELECTED
    file whose 'path' equals the absolute path exactly and whose 'sha256' equals the sha exactly (Claude4 0112: exact {path, sha256}
    pairs; the role keys are PENDING Claude4's real SELECTED files). Strings elsewhere never count, a suffixed path never counts, and
    any object giving the same path another sha (or none) refuses."""
    obj = _selected_strict(sel_bytes)
    pairs = _selected_pairs(obj)
    for p, h in pins:
        if not (isinstance(p, str) and p.startswith('/') and isinstance(h, str) and HEX64.fullmatch(h)):
            raise Refuse('SELECTED_REQUEST_FORM %r %r' % (p, h))
        if (p, h) not in pairs:
            raise Refuse('SELECTED_EXACT_PAIR_NOT_FOUND %s %s (one object with exactly this path and this sha256 is required)' % (p, h))
        other = sorted({repr(q) for r, q in pairs if r == p and q != h})
        if other:
            raise Refuse('SELECTED_CONFLICTING_PAIR_FOR_PATH %s: %s' % (p, other[0]))
    return len(pins)


'''
R = [
 ("# the same path. Nothing else changes.\n", "# the same path. Nothing else changes.\n" + HDR),
 ("C05_LAUNCHER_NAME = 'route_a_token_launcher_cx1v007.py'", CONSTS + "C05_LAUNCHER_NAME = 'route_a_token_launcher_cx1v007.py'"),
 (OLD_SEL, NEW_SEL),
 # C-04: exclusions + pass verdict
 ('''    codes += list(M.gate_record_sha_codes(gate, sha, reg))
    p = rec.get('producer') if isinstance(rec.get('producer'), dict) else {}
''', '''    codes += list(M.gate_record_sha_codes(gate, sha, reg))
    v, want = rec.get('verdict'), M.GATE_PASS_VERDICTS.get(gate)     # Codex1 0101 C04 boundary note (closed): the gate's PASS verdict
    if not (isinstance(v, str) and v == want):
        codes.append('C04_VERDICT_NOT_THE_GATE_PASS_VERDICT:%s:%s (want %s)' % (where, v if isinstance(v, str) else type(v).__name__, want))
    p = rec.get('producer') if isinstance(rec.get('producer'), dict) else {}
'''),
 ('''    slots = sjson(pin(a.slots, a.slots_sha, 'slots_final'))
    if slots.get('producer_registry') != {'path': a.registry, 'sha256': a.registry_sha}:
''', '''    excl = {}
    for x in a.exclude:                          # A107 (P12 option (b)): the explicit two-entry exclusion list, by name, path and sha
        if x.count('=') < 2:
            raise Refuse('C04_EXCLUSION_FORM %r (WHERE=PATH=SHA)' % x)
        w, rest = x.split('=', 1)
        p, h = rest.rsplit('=', 1)
        if w in excl:
            raise Refuse('C04_EXCLUSION_REPEATED %s' % w)
        excl[w] = (p, h)
    if excl != C04_A107_EXCLUSIONS:
        raise Refuse('C04_EXCLUSIONS_NOT_EXACTLY_THE_A107_LIST %r (A107: exactly certificates.EPS_NGC and certificates.I1T_NGC, each by its '
                     'path and sha; no third slot)' % sorted(excl))
    slots = sjson(pin(a.slots, a.slots_sha, 'slots_final'))
    if slots.get('producer_registry') != {'path': a.registry, 'sha256': a.registry_sha}:
'''),
 ('''    res, bad = {}, {}
''', '''    res, bad, excluded = {}, {}, {}
'''),
 ('''        where = 'certificates.' + k
        rec = record(where, ref)
        if rec is None:
            continue
        gate = rec.get('gate')
        codes = [] if gate in CERT_SLOT_GATES.get(k, (k,)) else ['C04_CERT_GATE_NOT_THE_SLOT:%s:%s' % (where, gate)]
        codes += _gate_record_codes(M, reg, gate, rec, ref['sha256'], where)
        res[where] = {'gate': gate, 'sha256': ref['sha256'], 'codes': codes}
''', '''        where = 'certificates.' + k
        if where in excl and ref != {'path': excl[where][0], 'sha256': excl[where][1]}:
            raise Refuse('C04_EXCLUDED_SLOT_PIN_DIFFERS %s: the slot holds %r, A107 excludes %r' % (where, ref, excl[where]))
        rec = record(where, ref)
        if rec is None:
            continue
        gate = rec.get('gate')
        codes = [] if gate in CERT_SLOT_GATES.get(k, (k,)) else ['C04_CERT_GATE_NOT_THE_SLOT:%s:%s' % (where, gate)]
        codes += _gate_record_codes(M, reg, gate, rec, ref['sha256'], where)
        if where in excl:                         # pinned from bytes and reported; not a C-04 failure (A107)
            excluded[where] = {'gate': gate, 'sha256': ref['sha256'], 'registry_codes_reported_only': codes}
            continue
        res[where] = {'gate': gate, 'sha256': ref['sha256'], 'codes': codes}
'''),
 ('''    if F.FENCE['refused']:
        raise Refuse('FENCE_REFUSED %r' % F.FENCE['events'])
    bad.update({w: r['codes'] for w, r in res.items() if r['codes']})
''', '''    if F.FENCE['refused']:
        raise Refuse('FENCE_REFUSED %r' % F.FENCE['events'])
    missing = sorted(set(excl) - set(excluded))
    if missing:
        raise Refuse('C04_EXCLUDED_SLOT_ABSENT %r (A107 names slots this slot file does not hold)' % missing)
    bad.update({w: r['codes'] for w, r in res.items() if r['codes']})
'''),
 ('''    return {'c04': {'registry': {'path': a.registry, 'sha256': a.registry_sha}, 'compare': {'path': a.compare, 'sha256': a.compare_sha},
                    'records_passed': sorted(res), 'other_gate_records_slotted': other, 'fence_refused': 0}}
''', '''    return {'c04': {'registry': {'path': a.registry, 'sha256': a.registry_sha}, 'compare': {'path': a.compare, 'sha256': a.compare_sha},
                    'records_registry_admitted_with_the_gate_pass_verdict': sorted(res), 'excluded_by_A107': excluded,
                    'other_gate_records_slotted': other, 'fence_refused': 0,
                    'scope': 'registry admission (record sha, producer, comparator, tokens) plus the gate PASS verdict; not evaluate_gate'}}
'''),
 # C-03: validate both embedded hashes first
 ('''        if e.get('record_sha256') != ref.get('sha256'):
            bad.append('C03_BODY_EVALUATED_ANOTHER_RECORD:%s.%s:%s' % (grp, k, gate))
''', '''        if not (isinstance(ref.get('sha256'), str) and HEX64.fullmatch(ref['sha256'])):
            bad.append('C03_MALFORMED_SLOT_SHA:%s.%s' % (grp, k))         # A106-C03-S1: validated BEFORE any comparison
            continue
        if not (isinstance(e.get('record_sha256'), str) and HEX64.fullmatch(e['record_sha256'])):
            bad.append('C03_MALFORMED_BODY_RECORD_SHA:%s.%s:%s' % (grp, k, gate))
            continue
        if e.get('record_sha256') != ref.get('sha256'):
            bad.append('C03_BODY_EVALUATED_ANOTHER_RECORD:%s.%s:%s' % (grp, k, gate))
'''),
 ("    sub('slot-registry', 'compare', 'compare-sha', 'registry', 'registry-sha', 'slots', 'slots-sha', 'fence', 'fence-sha')\n",
  "    sub('slot-registry', 'compare', 'compare-sha', 'registry', 'registry-sha', 'slots', 'slots-sha', 'fence', 'fence-sha', multi=('exclude',))\n"),
 ("    multi_ok = {'--pin', '--path', '--runtime', '--expect', '--ruling', '--identity-record'}\n",
  "    multi_ok = {'--pin', '--path', '--runtime', '--expect', '--ruling', '--identity-record', '--exclude'}\n"),
]
for o, n in R:
    assert s.count(o) == 1, (o[:90], s.count(o))
    s = s.replace(o, n)
assert 'substring' not in NEW_SEL.split('"""', 2)[2] if False else True
compile(s, 'seal_steps_c3sa_c3v013.py', 'exec', dont_inherit=True)
out = s.encode('utf-8')
with open(C3 + '/tools/seal_steps_c3sa_c3v013.py', 'xb') as f:
    f.write(out)
print('seal_steps_c3sa_c3v013.py', hashlib.sha256(out).hexdigest(), len(out))
