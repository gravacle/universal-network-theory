# make_helper_c3v012.py: Claude3 (FROM_CODEX/0643, A106). Derives tools/seal_steps_c3sa_c3v012.py from c3v011 (7caad125) by exact
# replacements (each old string occurs exactly once); writes it exclusively.
import hashlib, sys
C3 = sys.argv[1]
src = open(C3 + '/tools/seal_steps_c3sa_c3v011.py', 'rb').read()
assert hashlib.sha256(src).hexdigest() == '7caad125be19160c6e431dcf6be8f038cb9bba172c95f1f8059ebcdd938a0aff'
s = src.decode('utf-8')
HDR = '''# c3v012 (FROM_CODEX/0643, ruling A106): (A) freeze takes --open-bytes: BEFORE copying, the open V005 must hash to the pinned FINAL
# sha AND have the pinned length; the exclusive copy is re-read (no-follow) and re-hashed. (C-02) check-tor: the text of record is
# exactly the prereg its SELECTED file stores (path and sha), it is UNSEALED (every seal slot but cache_directory_r6_only still a
# PENDING marker), and a given sealed prereg is not it and is byte-equal to it with only seal_slots.<k>.value filled. (C-04)
# slot-registry: every slot record is checked through the reviewed compare r13's OWN load_producer_registry, gate_record_sha_codes,
# file_pin_codes and identity_comparator_codes (r13 read once, compiled from that buffer, inside the fence) against the slotted
# registry. (C-05 + C-06) bound-check: the launcher and guard are BUILD_V007 rows by EXACT file name and sha, the bound plan names
# exactly them, and the WHOLE bound command is byte-equal to the binder's output form (its comment line and its command line, from
# the pinned binder source). (C-03) gates-provenance: GATES_ONLY.json (sealed mode) evaluated the slotted gate records (record
# sha equal, status PASS). selected-names: a SELECTED file (from bytes) names each given path and sha, and names no other sha for
# the same path. Nothing else changes.
'''
CONSTS = '''C05_LAUNCHER_NAME = 'route_a_token_launcher_cx1v007.py'   # 0643 B / A106.2 C-05: exact file name (and the sha from BUILD_V007)
C05_GUARD_NAME = 'producer_guard_cx1v008.py'
BINDER_PYTHON_LINE = "PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'"
BINDER_COMMENT = ('# Claude2 only after root seal/config/receipt publication, independently verified UNT_ROOT_ADMISSION_SHA256 and all '
                  'root gates. This generator launches nothing.')
BINDER_CMD_FORM = "cmd=shlex.join([PYTHON,'-I','-B',plan['launcher']['path'],str(outs[0].resolve()),'--execute-root-only'])"
BINDER_WRITE_FORM = "f.write('" + BINDER_COMMENT + "\\\\n'+cmd+'\\\\n')"
CERT_SLOT_GATES = {'EPS': ('EPS',), 'LO': ('LO',), 'GQ': ('GQ',), 'DOUBLING': ('DOUBLING',), 'LO_NGC': ('LO_NGC',),
                   'EPS_NGC': ('EPS_NGC', 'EPS'), 'I1T_NGC': ('I1T_NGC', 'I1T')}   # C-04: the gate each certificate slot's record may name
IDENT_SLOT_GATE = {'Z2': 'B1', 'Z2_OFF_RO1': 'B1_OFF', 'B0prime_RERUN': 'B0prime_RERUN'}     # r13 IDENTITY_GATES
C03_SLOT_GATES = (('certificates', 'EPS', 'EPS'), ('certificates', 'LO', 'LO'), ('certificates', 'GQ', 'GQ'),
                  ('certificates', 'DOUBLING', 'DOUBLING'), ('certificates', 'LO_NGC', 'LO_NGC'), ('identity_gate_records', 'Z2', 'B1'),
                  ('identity_gate_records', 'Z2_OFF_RO1', 'B1_OFF'), ('identity_gate_records', 'B0prime_RERUN', 'B0prime_RERUN'))
'''
NEW_FREEZE = '''def c_freeze(a):
    """B1 / step 1 (A106; 0643 A): exclusive byte copy of the FINAL V005 addendum. BEFORE copying, the open bytes must hash to exactly
    the pinned final sha and have exactly the pinned length; the copy is created exclusively and re-read (no-follow) and re-hashed."""
    if not a.out.endswith('_V005_ADDENDUM_FROZEN.md'):
        raise Refuse('FROZEN_NAME (0576: ..._V005_ADDENDUM_FROZEN.md)')
    n = _digits(a.open_bytes, 'open-bytes')
    b = pin(a.open, a.open_sha, 'open_v005')
    if len(b) != n:
        raise Refuse('OPEN_V005_LENGTH %d != %d (A106: the FINAL V005 bytes; nothing was copied)' % (len(b), n))
    ref = write_x(a.out, b, 'frozen')
    copy = read_nofollow(a.out, 'frozen (re-hash)')
    if sha_bytes(copy) != a.open_sha or len(copy) != n or ref['sha256'] != a.open_sha:
        raise Refuse('FROZEN_COPY_REHASH_DIFFERS')
    if sha_bytes(read_nofollow(a.open, 'open_v005 (after the copy)')) != a.open_sha:
        raise Refuse('OPEN_V005_CHANGED_DURING_FREEZE')
    return {'frozen': ref, 'bytes': len(b), 'final_v005': {'sha256': a.open_sha, 'bytes': n}}
'''
NEW_FNS = r'''def _selected_names(sel_bytes, pins):
    """a SELECTED file names each (path, sha): both strings occur in its text, and no {path, sha256} object in it gives the same path
    another sha (format-agnostic: the publisher's own SELECTED schema is not assumed)."""
    t = sel_bytes.decode('utf-8')
    try:
        obj = sjson(sel_bytes)
    except Exception:
        obj = None
    pairs = []

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get('path'), str) and isinstance(o.get('sha256'), str):
                pairs.append((o['path'], o['sha256']))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    for p, h in pins:
        if p not in t or h not in t:
            raise Refuse('SELECTED_DOES_NOT_NAME %s %s' % (p, h))
        other = sorted({q for r, q in pairs if r == p and q != h})
        if other:
            raise Refuse('SELECTED_NAMES_ANOTHER_SHA_FOR %s: %s' % (p, other[0]))
    return len(pins)


def c_selected_names(a):
    """v003 / r6 wiring (0643 C): the SELECTED file, verified from bytes, names every given (path, sha); each pin is verified too."""
    sel = pin(a.selected, a.selected_sha, 'selected')
    pins = [pinref(x, 'pin') for x in a.pin]
    if not pins:
        raise Refuse('SELECTED_NAMES_NO_PINS')
    for p, h in pins:
        pin(p, h, 'selected pin')
    return {'selected': {'path': a.selected, 'sha256': a.selected_sha}, 'names_verified': _selected_names(sel, pins)}


def _tor_unsealed(doc):
    ss = doc.get('seal_slots') if isinstance(doc, dict) else None
    if not isinstance(ss, dict) or set(ss) != set(PREREG_SLOT_OF):
        raise Refuse('C02_TEXT_OF_RECORD_SEAL_SLOTS_KEYS %r' % (sorted(ss) if isinstance(ss, dict) else ss))
    filled = sorted(k for k, v in ss.items() if k != 'cache_directory_r6_only'
                    and not (isinstance(v, dict) and isinstance(v.get('value'), str) and 'PENDING' in v['value']))
    if filled:
        raise Refuse('C02_TEXT_OF_RECORD_HAS_FILLED_SLOTS %r (a sealed or edited prereg named as its own text of record)' % filled)


def _sealed_bytes(tor_bytes, slots):
    doc = sjson(tor_bytes)
    for pk, sk in PREREG_SLOT_OF.items():
        doc['seal_slots'][pk]['value'] = slots[sk]
    return dumps(doc).encode('utf-8')


def c_check_tor(a):
    """C-02 (A106.2; 0643 B): the text of record is exactly the prereg its SELECTED file stores (path and sha, from bytes); it is an
    UNSEALED text; and a given sealed prereg is a different file, byte-equal to the text of record with only seal_slots.<k>.value
    filled from the final slots (so an edited sealed prereg can pass neither as the text of record nor as the sealed prereg)."""
    sel = pin(a.selected, a.selected_sha, 'r6_selected')
    _selected_names(sel, [(a.text_of_record, a.tor_sha)])
    tb = pin(a.text_of_record, a.tor_sha, 'text_of_record')
    _tor_unsealed(sjson(tb))
    out = {'text_of_record': {'path': a.text_of_record, 'sha256': a.tor_sha}, 'named_by_selected': {'path': a.selected, 'sha256': a.selected_sha},
           'unsealed': True}
    if a.sealed_prereg or a.sealed_prereg_sha or a.slots or a.slots_sha:
        if not (a.sealed_prereg and a.sealed_prereg_sha and a.slots and a.slots_sha):
            raise Refuse('C02_ARGS (give --sealed-prereg, --sealed-prereg-sha, --slots and --slots-sha together)')
        if a.sealed_prereg == a.text_of_record or a.sealed_prereg_sha == a.tor_sha:
            raise Refuse('C02_SEALED_PREREG_IS_THE_TEXT_OF_RECORD')
        sp = pin(a.sealed_prereg, a.sealed_prereg_sha, 'sealed_prereg')
        slots = sjson(pin(a.slots, a.slots_sha, 'slots_final'))
        if sp != _sealed_bytes(tb, slots):
            raise Refuse('C02_SEALED_PREREG_NOT_THE_TEXT_OF_RECORD_PLUS_SLOT_VALUES')
        out['sealed_prereg'] = {'path': a.sealed_prereg, 'sha256': a.sealed_prereg_sha, 'rederived_byte_equal': True}
    return {'c02': out}


def _gate_record_codes(M, reg, gate, rec, sha, where):
    """C-04: one slotted gate record through r13's own registry functions (record sha of record; producer path, sha and bytes)."""
    codes = []
    if rec.get('schema') != M.GATE_SCHEMA:
        codes.append('C04_NOT_A_GATE_RECORD_SCHEMA:%s' % where)
    if gate not in M.ALL_GATES:
        return codes + ['C04_NOT_A_REGISTRY_GATE:%s:%s' % (where, gate)]
    codes += list(M.gate_record_sha_codes(gate, sha, reg))
    p = rec.get('producer') if isinstance(rec.get('producer'), dict) else {}
    codes += list(M.file_pin_codes(p.get('path'), p.get('sha256'), reg['producers'].get(gate, frozenset()),
                                   (M.PRODUCER_SHA_CODE, gate, M.PRODUCER_PATH_CODE, M.PRODUCER_BYTES_CODE)))
    return codes


def c_slot_registry(a):
    """C-04 (A106.2; 0643 B): every slot record, loaded through the reviewed compare r13's OWN load_producer_registry against the
    slotted registry (V009), must PASS: each certificate, each identity record (gate, record sha, producer, comparator and token
    set), the identity comparator, and any other slotted gate record (B2 / B3 where slotted). r13 is read once and exec'd from that
    buffer inside the fence."""
    slots = sjson(pin(a.slots, a.slots_sha, 'slots_final'))
    if slots.get('producer_registry') != {'path': a.registry, 'sha256': a.registry_sha}:
        raise Refuse('C04_SLOT_REGISTRY_IS_NOT_THE_GIVEN_REGISTRY %r' % slots.get('producer_registry'))
    pin(a.registry, a.registry_sha, 'producer_registry')
    F = _fence(a, write_roots=())
    M = load_pinned(a.compare, a.compare_sha, 'reviewed_compare_r13_c04')
    reg = M.load_producer_registry(a.registry, a.registry_sha)
    res, bad = {}, {}

    def record(where, ref):
        if not (isinstance(ref, dict) and set(ref) == {'path', 'sha256'}):
            bad[where] = ['C04_SLOT_NOT_A_PIN']
            return None
        return sjson(pin(ref['path'], ref['sha256'], where))
    for k, ref in sorted((slots.get('certificates') or {}).items()):
        where = 'certificates.' + k
        rec = record(where, ref)
        if rec is None:
            continue
        gate = rec.get('gate')
        codes = [] if gate in CERT_SLOT_GATES.get(k, (k,)) else ['C04_CERT_GATE_NOT_THE_SLOT:%s:%s' % (where, gate)]
        codes += _gate_record_codes(M, reg, gate, rec, ref['sha256'], where)
        res[where] = {'gate': gate, 'sha256': ref['sha256'], 'codes': codes}
    comp = slots.get('identity_comparator')
    ccodes = list(M.file_pin_codes((comp or {}).get('path'), (comp or {}).get('sha256'), reg['identity_comparators'],
                                   ('C04_IDENTITY_COMPARATOR_NOT_ROOT_REGISTERED_A57_3', 'identity_comparator',
                                    'C04_IDENTITY_COMPARATOR_PATH_NOT_ROOT_REGISTERED_A69_1',
                                    'C04_IDENTITY_COMPARATOR_BYTES_NOT_THE_REGISTERED_SHA_A69_1')))
    res['identity_comparator'] = {'sha256': (comp or {}).get('sha256'), 'codes': ccodes}
    for k, ref in sorted((slots.get('identity_gate_records') or {}).items()):
        where = 'identity_gate_records.' + k
        rec = record(where, ref)
        if rec is None:
            continue
        gate = rec.get('gate')
        codes = [] if gate == IDENT_SLOT_GATE.get(k) else ['C04_IDENTITY_GATE_NOT_THE_SLOT:%s:%s' % (where, gate)]
        codes += _gate_record_codes(M, reg, gate, rec, ref['sha256'], where)
        if gate in M.IDENTITY_GATES:
            codes += [c for c in M.identity_comparator_codes(rec, gate, {'producer_registry': reg}, [])]
        if rec.get('comparator') != comp:
            codes.append('C04_IDENTITY_RECORD_COMPARATOR_IS_NOT_THE_SLOT_COMPARATOR:%s' % where)
        res[where] = {'gate': gate, 'sha256': ref['sha256'], 'codes': codes}
    other = []                                   # B2 / B3 (or any other gate record) where slotted elsewhere
    for grp, v in sorted(slots.items()):
        if grp in ('certificates', 'identity_gate_records', 'identity_comparator', 'producer_registry') or not isinstance(v, dict):
            continue
        for k, ref in sorted(v.items()) if not set(v) >= {'path', 'sha256'} else [('', v)]:
            if isinstance(ref, dict) and set(ref) == {'path', 'sha256'} and str(ref['path']).endswith('.json'):
                try:
                    rec = sjson(pin(ref['path'], ref['sha256'], grp))
                except Refuse:
                    raise
                except Exception:
                    continue
                if isinstance(rec, dict) and rec.get('schema') == M.GATE_SCHEMA:
                    where = grp + ('.' + k if k else '')
                    res[where] = {'gate': rec.get('gate'), 'sha256': ref['sha256'],
                                  'codes': _gate_record_codes(M, reg, rec.get('gate'), rec, ref['sha256'], where)}
                    other.append(where)
    if F.FENCE['refused']:
        raise Refuse('FENCE_REFUSED %r' % F.FENCE['events'])
    bad.update({w: r['codes'] for w, r in res.items() if r['codes']})
    if bad:
        raise Refuse('C04_SLOT_RECORDS_FAIL_THE_REGISTRY %s' % json.dumps(bad, sort_keys=True))
    return {'c04': {'registry': {'path': a.registry, 'sha256': a.registry_sha}, 'compare': {'path': a.compare, 'sha256': a.compare_sha},
                    'records_passed': sorted(res), 'other_gate_records_slotted': other, 'fence_refused': 0}}


def c_bound_check(a):
    """C-05 + C-06 (A106.2; 0643 B), after the binder: the launcher and the guard are BUILD_V007 rows by EXACT file name and sha, and
    the bound plan names exactly them ('any allowlisted source' does not pass); the WHOLE bound command file is byte-equal to the
    binder's output: its fixed comment line and its shlex command line, both taken from the pinned binder source."""
    rows = _build_table(pin(a.build, a.build_sha, 'build').decode('utf-8'))
    for label, name, p, h in (('LAUNCHER', C05_LAUNCHER_NAME, a.launcher, a.launcher_sha), ('GUARD', C05_GUARD_NAME, a.guard, a.guard_sha)):
        if os.path.basename(p) != name:
            raise Refuse('C05_%s_NAME %r (want %s)' % (label, os.path.basename(p), name))
        hits = [r for r in rows if os.path.basename(r[0]) == name]
        if len(hits) != 1:
            raise Refuse('C05_%s_BUILD_ROWS_NAMED_%s %d (want exactly one)' % (label, name, len(hits)))
        if hits[0] != (p, h):
            raise Refuse('C05_%s_NOT_THE_BUILD_ROW %r (BUILD_V007 row %r)' % (label, (p, h), hits[0]))
        pin(p, h, label.lower())
    plan = sjson(pin(a.plan, a.plan_sha, 'bound_plan'))
    if plan.get('launcher') != {'path': a.launcher, 'sha256': a.launcher_sha}:
        raise Refuse('C05_PLAN_LAUNCHER_NOT_EXACT %r' % (plan.get('launcher'),))
    if plan.get('guard') != {'path': a.guard, 'sha256': a.guard_sha}:
        raise Refuse('C05_PLAN_GUARD_NOT_EXACT %r' % (plan.get('guard'),))
    bsrc = pin(a.binder, a.binder_sha, 'binder').decode('utf-8')
    for frag in (BINDER_PYTHON_LINE, BINDER_CMD_FORM, BINDER_WRITE_FORM):
        if bsrc.count(frag) != 1:
            raise Refuse('C06_BINDER_SOURCE_FORM %r' % frag[:70])
    py = BINDER_PYTHON_LINE.split("'")[1]
    want = (BINDER_COMMENT + '\n' + shlex.join([py, '-I', '-B', plan['launcher']['path'], a.plan, '--execute-root-only']) + '\n').encode('utf-8')
    got = pin(a.command, a.command_sha, 'bound_command')
    if got != want:
        gl, wl = got.split(b'\n'), want.split(b'\n')
        i = next((j for j in range(max(len(gl), len(wl))) if (gl[j] if j < len(gl) else None) != (wl[j] if j < len(wl) else None)), 0)
        raise Refuse('C06_BOUND_COMMAND_NOT_BYTE_EQUAL_TO_THE_BINDER_OUTPUT (first differing line %d; %d bytes, want %d)' % (i + 1, len(got), len(want)))
    return {'c05': {'launcher': {'path': a.launcher, 'sha256': a.launcher_sha}, 'guard': {'path': a.guard, 'sha256': a.guard_sha},
                    'exact_build_rows': True, 'plan_names_exactly_them': True},
            'c06': {'bound_command': {'path': a.command, 'sha256': a.command_sha}, 'byte_equal_to_the_binder_output': True,
                    'lines': len(want.split(b'\n')) - 1}}


def c_gates_provenance(a):
    """C-03 (B6 provenance; A106.2, taken in because it fits 10 minutes): the sealed-mode GATES_ONLY body evaluated the SLOTTED gate
    records: for each certificate and identity slot that is a gates-only gate record, the body's record_sha256 for that gate equals
    the slot's sha and its status is PASS. The NGC certificates EPS_NGC and I1T_NGC are not gates-only gate records (C-04 covers them)."""
    g = sjson(pin(a.gates_json, a.gates_json_sha, 'gates_only_json'))
    slots = sjson(pin(a.slots, a.slots_sha, 'slots_final'))
    if not isinstance(g, dict) or g.get('test_mode') is not False or not isinstance(g.get('gates'), dict):
        raise Refuse('C03_GATES_ONLY_BODY_NOT_SEALED_MODE')
    out, bad = {}, []
    for grp, k, gate in C03_SLOT_GATES:
        ref = (slots.get(grp) or {}).get(k)
        e = g['gates'].get(gate)
        if not (isinstance(ref, dict) and isinstance(e, dict)):
            bad.append('C03_SLOT_GATE_NOT_IN_THE_BODY:%s.%s:%s' % (grp, k, gate))
            continue
        if e.get('record_sha256') != ref.get('sha256'):
            bad.append('C03_BODY_EVALUATED_ANOTHER_RECORD:%s.%s:%s' % (grp, k, gate))
        elif e.get('status') != 'PASS':
            bad.append('C03_SLOT_GATE_STATUS_%s:%s.%s:%s' % (e.get('status'), grp, k, gate))
        else:
            out['%s.%s' % (grp, k)] = {'gate': gate, 'record_sha256': ref['sha256'], 'status': 'PASS'}
    if bad:
        raise Refuse('C03 %s' % ' '.join(bad))
    return {'c03': {'gates_only_json': {'path': a.gates_json, 'sha256': a.gates_json_sha}, 'slotted_records_evaluated': out,
                    'not_gates_only_records': ['certificates.EPS_NGC', 'certificates.I1T_NGC']}}


def c_make_receipt(a):'''
R = [
 ("# Directories this helper creates (output-root only) are created with os.mkdir, which never reuses an existing entry.\n",
  "# Directories this helper creates (output-root only) are created with os.mkdir, which never reuses an existing entry.\n" + HDR),
 ('import argparse, ast, fcntl, hashlib, json, os, re, stat as stat_mod, sys, time, types\n',
  'import argparse, ast, fcntl, hashlib, json, os, re, shlex, stat as stat_mod, sys, time, types\n'),
 ("VOLUME_ROOT = '/System/Volumes/Data'              # RP-S1 / RUNBOOK_V008 L37: the internal startup Data volume (st_dev compare)\n",
  "VOLUME_ROOT = '/System/Volumes/Data'              # RP-S1 / RUNBOOK_V008 L37: the internal startup Data volume (st_dev compare)\n" + CONSTS),
 (s[s.index('def c_freeze(a):'):s.index('def c_same(a):')], NEW_FREEZE + '\n\n'),
 ('def c_make_receipt(a):', NEW_FNS),
 ("    sub('freeze', 'open', 'open-sha', 'out')\n", "    sub('freeze', 'open', 'open-sha', 'open-bytes', 'out')\n"),
 ("    sub('output-root', 'path', 'mode', opt=('min-free-gib', 'expect-dev', 'expect-ino'))\n",
  "    sub('output-root', 'path', 'mode', opt=('min-free-gib', 'expect-dev', 'expect-ino'))\n"
  "    sub('selected-names', 'selected', 'selected-sha', multi=('pin',))\n"
  "    sub('check-tor', 'text-of-record', 'tor-sha', 'selected', 'selected-sha', opt=('sealed-prereg', 'sealed-prereg-sha', 'slots', 'slots-sha'))\n"
  "    sub('slot-registry', 'compare', 'compare-sha', 'registry', 'registry-sha', 'slots', 'slots-sha', 'fence', 'fence-sha')\n"
  "    sub('bound-check', 'build', 'build-sha', 'plan', 'plan-sha', 'command', 'command-sha', 'binder', 'binder-sha', 'launcher', 'launcher-sha', 'guard', 'guard-sha')\n"
  "    sub('gates-provenance', 'gates-json', 'gates-json-sha', 'slots', 'slots-sha')\n"),
 ("          'output-root': c_output_root}[a.cmd]\n",
  "          'output-root': c_output_root, 'selected-names': c_selected_names, 'check-tor': c_check_tor, 'slot-registry': c_slot_registry,\n"
  "          'bound-check': c_bound_check, 'gates-provenance': c_gates_provenance}[a.cmd]\n"),
]
for o, n in R:
    assert s.count(o) == 1, (o[:80], s.count(o))
    s = s.replace(o, n)
assert s.count('def c_make_receipt(a):') == 1
compile(s, 'seal_steps_c3sa_c3v012.py', 'exec', dont_inherit=True)
out = s.encode('utf-8')
with open(C3 + '/tools/seal_steps_c3sa_c3v012.py', 'xb') as f:
    f.write(out)
print('seal_steps_c3sa_c3v012.py', hashlib.sha256(out).hexdigest(), len(out))
