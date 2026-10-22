# Claude4 helper: which A-entry sections differ between two V005 addendum byte copies (tool 1 r2's own sections() rule)?
import hashlib, json, sys
sys.path.insert(0, '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2')
import check_frozen_addendum_c4v002 as T1
old, new = open(sys.argv[1], 'rb').read(), open(sys.argv[2], 'rb').read()
so, sn = T1.sections(old), T1.sections(new)
out = {'old': {'path': sys.argv[1], 'sha256': hashlib.sha256(old).hexdigest()}, 'new': {'path': sys.argv[2], 'sha256': hashlib.sha256(new).hexdigest()},
       'only_in_old': sorted(set(so) - set(sn)), 'only_in_new': sorted(set(sn) - set(so)),
       'changed': sorted(n for n in set(so) & set(sn) if so[n][0][1] != sn[n][0][1]),
       'duplicated_headings_new': sorted(n for n, v in sn.items() if len(v) > 1)}
print(json.dumps(out, indent=1))
