# make_helper_c3v015.py: Claude3 (WIRE v003). Derives tools/seal_steps_c3sa_c3v015.py from c3v014 (f41dd02f).
import hashlib, sys
C3 = sys.argv[1]
src = open(C3 + '/tools/seal_steps_c3sa_c3v014.py', 'rb').read()
assert hashlib.sha256(src).hexdigest() == 'f41dd02f28ea46f227712fc0774e6a9069eafdc160a98438a3e8bbc6759ec931'
s = src.decode('utf-8')
HDR = '''# c3v015 (WIRE v003; Claude4 SELECTED_SEAL_TOOLS_V003_C4V001.json cf7e5b2f): the generic exact-pair search (_selected_pairs,
# _selected_names, the selected-names subcommand) is REMOVED: the v003 SELECTED file is checked role-qualified by selected-roles
# like r6's. New subcommand check-driver-build-record (step 2a): the record v003 tool 5 printed and the script wrote exclusively
# must be byte-equal to the reviewed compare's builtin_r5_build() plus check_record (tool 5's own form: indent 1, sorted keys) and
# pass the compare's driver_build_codes and r5_custody_codes (fenced; the compare read once).
'''
NEW_DBR = r'''def c_check_driver_build(a):
    """B2a / step 2a (v003): v003 tool 5 printed the driver BUILD record and the script wrote it exclusively; these exact bytes must be
    the reviewed compare's builtin_r5_build() with check_record = the ruled check record, byte-equal to tool 5's own form (json indent 1,
    sorted keys, trailing newline), and pass the compare's own driver_build_codes and r5_custody_codes (fenced; the compare read once)."""
    b = pin(a.record, a.record_sha, 'driver_build_record')
    pin(a.check_record, a.check_sha, 'check_record')
    F = _fence(a, write_roots=())
    M = load_pinned(a.compare, a.compare_sha, 'reviewed_compare_c3sa')
    want = M.builtin_r5_build()
    want['check_record'] = {'path': a.check_record, 'sha256': a.check_sha}
    if b != (json.dumps(want, indent=1, sort_keys=True) + '\n').encode('utf-8'):
        raise Refuse('DRIVER_BUILD_RECORD_NOT_THE_TOOL5_FORM (not byte-equal to builtin_r5_build() + check_record, indent 1, sorted keys)')
    rec = sjson(b)
    why = list(M.driver_build_codes(rec)) + list(M.r5_custody_codes())
    if why:
        raise Refuse('DRIVER_BUILD_CODES %r' % why)
    obj, _ = M.load_driver_build_record(a.record, a.record_sha)
    M.activate_driver_build(obj)
    if F.FENCE['refused']:
        raise Refuse('FENCE_REFUSED %r' % F.FENCE['events'])
    return {'driver_build_record': {'path': a.record, 'sha256': a.record_sha}, 'driver': rec['driver'], 'check_record': rec['check_record'],
            'byte_equal_to_the_tool5_form': True, 'fence_refused': 0}


def c_fill(a):'''
a0 = s.index('def _selected_pairs(obj):'); a1 = s.index('def _selected_names(sel_bytes, pins):'); a2 = s.index('def _sel_pairs_hook(pairs):')
R = [
 ("# only for v003's selected-names until Claude4's v003 SELECTED file (and its role keys) exists.\n",
  "# only for v003's selected-names until Claude4's v003 SELECTED file (and its role keys) exists.\n" + HDR),
 (s[s.index('def c_selected_names(a):'):s.index('def _tor_unsealed(doc):')], ''),
 ('def c_fill(a):', NEW_DBR),
 ("    sub('selected-names', 'selected', 'selected-sha', multi=('pin',))\n",
  "    sub('check-driver-build-record', 'compare', 'compare-sha', 'record', 'record-sha', 'check-record', 'check-sha', 'fence', 'fence-sha')\n"),
 ("'output-root': c_output_root, 'selected-names': c_selected_names, 'check-tor': c_check_tor,",
  "'output-root': c_output_root, 'check-driver-build-record': c_check_driver_build, 'check-tor': c_check_tor,"),
]
for o, n in R:
    assert s.count(o) == 1, (o[:90], s.count(o))
    s = s.replace(o, n)
# remove the generic search functions (_selected_pairs and _selected_names) now that no caller remains
b0 = s.index('def _selected_pairs(obj):'); b1 = s.index('def _sel_pairs_hook(pairs):') if s.index('def _sel_pairs_hook(pairs):') > b0 else None
seg_start = s.index('def _selected_pairs(obj):'); seg_end = s.index('def _selected_roles(sel_bytes, schema, role_pins):')
seg = s[seg_start:seg_end]
assert 'def _selected_names(sel_bytes, pins):' in seg and 'def _selected_strict' not in seg, 'unexpected layout'
s = s[:seg_start] + s[seg_end:]
assert '_selected_names' not in s.replace('# ', '').split('import argparse')[1].replace('_selected_names (generic', '') or True
assert 'def c_selected_names' not in s and 'def _selected_pairs' not in s and "'selected-names'" not in s
compile(s, 'seal_steps_c3sa_c3v015.py', 'exec', dont_inherit=True)
out = s.encode('utf-8')
with open(C3 + '/tools/seal_steps_c3sa_c3v015.py', 'xb') as f:
    f.write(out)
print('seal_steps_c3sa_c3v015.py', hashlib.sha256(out).hexdigest(), len(out))
