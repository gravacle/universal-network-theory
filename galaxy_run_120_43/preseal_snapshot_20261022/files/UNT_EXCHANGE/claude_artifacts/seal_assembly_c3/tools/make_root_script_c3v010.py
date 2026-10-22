# make_root_script_c3v010.py: Claude3 (0642). Derives ROOT_SEAL_STEPS_c3v010.sh from c3v009 (ebef7377): the helper pin (c3v011) and
# the header only.
import hashlib, sys
C3, HELPER_SHA = sys.argv[1], sys.argv[2]
src = open(C3 + '/ROOT_SEAL_STEPS_c3v009.sh', 'rb').read()
assert hashlib.sha256(src).hexdigest() == 'ebef7377d54ad98aaaad4ba436dc0be0856d0c33e3bbe530cc7498828d92ffc1'
assert hashlib.sha256(open(C3 + '/tools/seal_steps_c3sa_c3v011.py', 'rb').read()).hexdigest() == HELPER_SHA
s = src.decode('utf-8')
R = [('# ROOT_SEAL_STEPS_c3v009.sh: the V007 seal assembly', '# ROOT_SEAL_STEPS_c3v010.sh: the V007 seal assembly'),
     ('# c3v009 supersedes ROOT_SEAL_STEPS_c3v008.sh (023b2bbf; FROM_CODEX/0642, A105, from Claude4 0108; heads-up Claude4 0109):\n',
      '# c3v010 supersedes ROOT_SEAL_STEPS_c3v009.sh (ebef7377; used only by dry run 20261018T225153Z): ONLY the helper pin changes, to\n'
      '#   seal_steps_c3sa_c3v011.py (output-root refuses an empty, "." or ".." component lexically, before any walk or mkdir).\n'
      '# c3v009 superseded ROOT_SEAL_STEPS_c3v008.sh (023b2bbf; FROM_CODEX/0642, A105, from Claude4 0108; heads-up Claude4 0109):\n'),
     ('HELPER="$C3/tools/seal_steps_c3sa_c3v010.py";          HELPER_SHA="823c8aca8c230d78f6a4c2e3a7b494a64546030622e4b186db799f873c537df2"',
      'HELPER="$C3/tools/seal_steps_c3sa_c3v011.py";          HELPER_SHA="%s"' % HELPER_SHA)]
for o, n in R:
    assert s.count(o) == 1, (o[:80], s.count(o))
    s = s.replace(o, n)
out = s.encode('utf-8')
with open(C3 + '/ROOT_SEAL_STEPS_c3v010.sh', 'xb') as f:
    f.write(out)
print('ROOT_SEAL_STEPS_c3v010.sh', hashlib.sha256(out).hexdigest(), len(out))
