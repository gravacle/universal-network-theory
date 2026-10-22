# make_helper_c3v011.py: Claude3 (0642). Derives tools/seal_steps_c3sa_c3v011.py from c3v010 (823c8aca) by exact replacements.
import hashlib, sys
C3 = sys.argv[1]
src = open(C3 + '/tools/seal_steps_c3sa_c3v010.py', 'rb').read()
assert hashlib.sha256(src).hexdigest() == '823c8aca8c230d78f6a4c2e3a7b494a64546030622e4b186db799f873c537df2'
s = src.decode('utf-8')
R = [("# Directories this helper creates (output-root only) are created with os.mkdir, which never reuses an existing entry.\n",
      "# Directories this helper creates (output-root only) are created with os.mkdir, which never reuses an existing entry.\n"
      "# c3v011 supersedes c3v010 (823c8aca; used only by dry run 20261018T225153Z): output-root refuses an empty, '.' or '..' component\n"
      "# LEXICALLY, before any walk or mkdir (c3v010 walked the root's own last component only when its parent existed, so a path\n"
      "# ending in '..' under an absent parent could have created that parent before refusing). Nothing else changes.\n"),
     ("    p = a.path\n    path_policy(p, must_exist=None, label='output_root')\n    parent = os.path.dirname(p)\n",
      "    p = a.path\n    path_policy(p, must_exist=None, label='output_root')\n"
      "    if any(c in ('', '.', '..') for c in p.split('/')[1:]):\n"
      "        raise Refuse('PATH_COMPONENT_REFUSED output_root: %r (lexical, before any walk or mkdir)' % p)\n"
      "    parent = os.path.dirname(p)\n")]
for o, n in R:
    assert s.count(o) == 1, (o[:80], s.count(o))
    s = s.replace(o, n)
compile(s, 'seal_steps_c3sa_c3v011.py', 'exec', dont_inherit=True)
out = s.encode('utf-8')
with open(C3 + '/tools/seal_steps_c3sa_c3v011.py', 'xb') as f:
    f.write(out)
print('seal_steps_c3sa_c3v011.py', hashlib.sha256(out).hexdigest(), len(out))
