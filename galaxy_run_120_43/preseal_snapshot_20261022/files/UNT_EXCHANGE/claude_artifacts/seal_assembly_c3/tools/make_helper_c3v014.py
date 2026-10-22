# make_helper_c3v014.py: Claude3 (0644 follow-up: wire r6). Derives tools/seal_steps_c3sa_c3v014.py from c3v013 (ad581a06).
import hashlib, sys
C3 = sys.argv[1]
src = open(C3 + '/tools/seal_steps_c3sa_c3v013.py', 'rb').read()
assert hashlib.sha256(src).hexdigest() == 'ad581a06854ad5ce0e337624860cdf07c04181fccb066f71e79128f1d9b05200'
s = src.decode('utf-8')
HDR = '''# c3v014 (0644 follow-up; Claude4 SELECTED_R6_C4V001.json 7200acd9, schema UNT_V007_SELECTED_PREREG_C4V001): C02-SEL-ASSOCIATION is now
# ROLE-QUALIFIED with the real schema's keys: the SELECTED file (strict parse as c3v013) must carry the given schema string and a
# 'files' object whose EVERY entry is exactly {path: <absolute>, sha256: <64 lowercase hex>} with no path given two shas; each
# requested pin must be EXACTLY files[<role>] (check-tor: --selected-schema and --tor-role, e.g. text_of_record; the new
# selected-roles subcommand checks any --role-pin ROLE=PATH=SHA and pins each from bytes). The generic exact-pair search remains
# only for v003's selected-names until Claude4's v003 SELECTED file (and its role keys) exists.
'''
NEW = r'''def _selected_roles(sel_bytes, schema, role_pins):
    """C02-SEL-ASSOCIATION, role-qualified (the real SELECTED schema, Claude4 SELECTED_R6_C4V001): strict parse (c3v013); the schema
    string must match; 'files' is an object whose every entry is exactly {path: absolute str, sha256: 64 lowercase hex}, no path with
    two shas; each requested (role, path, sha) must be EXACTLY files[role]."""
    obj = _selected_strict(sel_bytes)
    if obj.get('schema') != schema:
        raise Refuse('SELECTED_SCHEMA_MISMATCH %r (want %r)' % (obj.get('schema'), schema))
    files = obj.get('files')
    if not isinstance(files, dict) or not files:
        raise Refuse('SELECTED_FILES_NOT_A_NONEMPTY_OBJECT')
    seen = {}
    for role, e in files.items():
        if not (isinstance(e, dict) and set(e) == {'path', 'sha256'} and isinstance(e['path'], str) and e['path'].startswith('/')
                and isinstance(e['sha256'], str) and HEX64.fullmatch(e['sha256'])):
            raise Refuse('SELECTED_FILES_ENTRY_FORM %r (each entry exactly {path: absolute, sha256: 64 lowercase hex})' % role)
        if e['path'] in seen and seen[e['path']] != e['sha256']:
            raise Refuse('SELECTED_CONFLICTING_PAIR_FOR_PATH %s' % e['path'])
        seen[e['path']] = e['sha256']
    for role, p, h in role_pins:
        if not (isinstance(p, str) and p.startswith('/') and isinstance(h, str) and HEX64.fullmatch(h)):
            raise Refuse('SELECTED_REQUEST_FORM %r %r %r' % (role, p, h))
        if role not in files:
            raise Refuse('SELECTED_ROLE_MISSING %r' % role)
        if files[role] != {'path': p, 'sha256': h}:
            raise Refuse('SELECTED_ROLE_PAIR_MISMATCH %r: stored %r, requested %r' % (role, files[role], {'path': p, 'sha256': h}))
    return len(role_pins)


def c_selected_roles(a):
    """r6 wiring (0644 follow-up): every --role-pin ROLE=PATH=SHA is exactly the SELECTED file's files[ROLE]; each pin is verified from bytes."""
    sel = pin(a.selected, a.selected_sha, 'selected')
    rp = []
    for x in a.role_pin:
        if x.count('=') < 2:
            raise Refuse('ROLE_PIN_FORM %r (ROLE=PATH=SHA)' % x)
        role, rest = x.split('=', 1)
        p, h = rest.rsplit('=', 1)
        rp.append((role, p, h))
    if not rp:
        raise Refuse('SELECTED_ROLES_NO_PINS')
    n = _selected_roles(sel, a.schema, rp)
    for role, p, h in rp:
        pin(p, h, 'selected role ' + role)
    return {'selected': {'path': a.selected, 'sha256': a.selected_sha, 'schema': a.schema}, 'roles_verified': {r: {'path': p, 'sha256': h} for r, p, h in rp},
            'n': n}


def c_selected_names(a):'''
R = [
 ("# also carry its gate's pass verdict from r13's own GATE_PASS_VERDICTS (a registered FAIL, an absent or an unknown verdict refuses).\n",
  "# also carry its gate's pass verdict from r13's own GATE_PASS_VERDICTS (a registered FAIL, an absent or an unknown verdict refuses).\n" + HDR),
 ('def c_selected_names(a):', NEW),
 ('''    sel = pin(a.selected, a.selected_sha, 'r6_selected')
    _selected_names(sel, [(a.text_of_record, a.tor_sha)])
''', '''    sel = pin(a.selected, a.selected_sha, 'r6_selected')
    _selected_roles(sel, a.selected_schema, [(a.tor_role, a.text_of_record, a.tor_sha)])     # role-qualified (c3v014)
'''),
 ("    out = {'text_of_record': {'path': a.text_of_record, 'sha256': a.tor_sha}, 'named_by_selected': {'path': a.selected, 'sha256': a.selected_sha},\n",
  "    out = {'text_of_record': {'path': a.text_of_record, 'sha256': a.tor_sha}, 'named_by_selected': {'path': a.selected, 'sha256': a.selected_sha,\n"
  "           'schema': a.selected_schema, 'role': a.tor_role},\n"),
 ("    sub('check-tor', 'text-of-record', 'tor-sha', 'selected', 'selected-sha', opt=('sealed-prereg', 'sealed-prereg-sha', 'slots', 'slots-sha'))\n",
  "    sub('check-tor', 'text-of-record', 'tor-sha', 'selected', 'selected-sha', 'selected-schema', 'tor-role', opt=('sealed-prereg', 'sealed-prereg-sha', 'slots', 'slots-sha'))\n"
  "    sub('selected-roles', 'selected', 'selected-sha', 'schema', multi=('role-pin',))\n"),
 ("          'bound-check': c_bound_check, 'gates-provenance': c_gates_provenance}[a.cmd]\n",
  "          'bound-check': c_bound_check, 'gates-provenance': c_gates_provenance, 'selected-roles': c_selected_roles}[a.cmd]\n"),
 ("    multi_ok = {'--pin', '--path', '--runtime', '--expect', '--ruling', '--identity-record', '--exclude'}\n",
  "    multi_ok = {'--pin', '--path', '--runtime', '--expect', '--ruling', '--identity-record', '--exclude', '--role-pin'}\n"),
]
for o, n in R:
    assert s.count(o) == 1, (o[:90], s.count(o))
    s = s.replace(o, n)
compile(s, 'seal_steps_c3sa_c3v014.py', 'exec', dont_inherit=True)
out = s.encode('utf-8')
with open(C3 + '/tools/seal_steps_c3sa_c3v014.py', 'xb') as f:
    f.write(out)
print('seal_steps_c3sa_c3v014.py', hashlib.sha256(out).hexdigest(), len(out))
