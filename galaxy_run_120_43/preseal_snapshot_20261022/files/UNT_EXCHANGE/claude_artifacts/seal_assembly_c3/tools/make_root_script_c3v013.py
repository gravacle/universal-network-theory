# make_root_script_c3v013.py: Claude3 (0644). Derives ROOT_SEAL_STEPS_c3v013.sh from c3v012 (cb41f72c): tor_table_bytes accepts r6's
# ABSOLUTE byte_copy inside the text of record's own folder (found by the 0644 probe of the r6 candidate d28c95f5); header notes.
import hashlib, sys
C3 = sys.argv[1]
src = open(C3 + '/ROOT_SEAL_STEPS_c3v012.sh', 'rb').read()
assert hashlib.sha256(src).hexdigest() == 'cb41f72c378ace12ba1d71fa3b9dc0964282e6f5c0e40a1a22c9be284da701d6'
s = src.decode('utf-8')
R = [
 ('# ROOT_SEAL_STEPS_c3v012.sh: the V007 seal assembly', '# ROOT_SEAL_STEPS_c3v013.sh: the V007 seal assembly'),
 ('# c3v012 supersedes ROOT_SEAL_STEPS_c3v011.sh (af74e9bd; FROM_CODEX/0644, A107 in the V006 addendum; Codex1 0101): helper c3v013\n',
  '# c3v013 supersedes ROOT_SEAL_STEPS_c3v012.sh (cb41f72c; used only by dry run 20261019T000226Z): tor_table_bytes also accepts an\n'
  '#   ABSOLUTE byte_copy inside the text of record\'s own folder. prereg r6 (candidate d28c95f5) writes it that way, where r5 wrote a\n'
  '#   relative one; c3v012 would have refused r6 in step 0. Nothing else changes.\n'
  '# c3v012 superseded ROOT_SEAL_STEPS_c3v011.sh (af74e9bd; FROM_CODEX/0644, A107 in the V006 addendum; Codex1 0101): helper c3v013\n'),
 ('''tor_table_bytes() {
  local bc; bc="$(jf "$PREREG_TOR" entries_after_A81.addendum_read.byte_copy)"; bc="${bc%% *}"
  case "$bc" in ''|/*|*..*) echo "REFUSE: the text of record's entries_after_A81.addendum_read.byte_copy: '$bc'" >&2; false;; esac
  TABLE_BYTES="$(/usr/bin/dirname "$PREREG_TOR")/$bc"
  TABLE_BYTES_SHA="$(jf "$PREREG_TOR" entries_after_A81.addendum_read.sha256_at_generation)"
}
''', '''tor_table_bytes() {
  local bc d; bc="$(jf "$PREREG_TOR" entries_after_A81.addendum_read.byte_copy)"; bc="${bc%% *}"; d="$(/usr/bin/dirname "$PREREG_TOR")"
  case "$bc" in
    ''|*..*) echo "REFUSE: the text of record's entries_after_A81.addendum_read.byte_copy: '$bc'" >&2; false;;
    "$d"/*) TABLE_BYTES="$bc";;            # r6 form: an absolute path inside the text of record's own folder
    /*) echo "REFUSE: the text of record's byte_copy lies outside its own folder: '$bc'" >&2; false;;
    *) TABLE_BYTES="$d/$bc";;              # r5 form: a path relative to the text of record's folder
  esac
  TABLE_BYTES_SHA="$(jf "$PREREG_TOR" entries_after_A81.addendum_read.sha256_at_generation)"
}
'''),
 ('# addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md and 70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e.\n',
  '# addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md and 70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e. r6 writes an\n'
  '# absolute byte_copy inside its own folder (r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md, c01b3c51); both forms are accepted.\n'),
]
for o, n in R:
    assert s.count(o) == 1, (o[:90], s.count(o))
    s = s.replace(o, n)
out = s.encode('utf-8')
with open(C3 + '/ROOT_SEAL_STEPS_c3v013.sh', 'xb') as f:
    f.write(out)
print('ROOT_SEAL_STEPS_c3v013.sh', hashlib.sha256(out).hexdigest(), len(out))
