"""Lens C cross-file check: tags, section references and cited-entry lists across PREREG, CSM, ROOT_ITEMS. Read-only."""
import json, re, sys
d = sys.argv[1]
P = open(d + '/PREREG_MISS_READING_R2.md', encoding='utf-8').read()
C = open(d + '/CLAUSE_SOURCE_MAP_R2.md', encoding='utf-8').read()
R = open(d + '/ROOT_ITEMS_R2.md', encoding='utf-8').read()
out = {}
ptags = re.findall(r'\[(C-[A-Z0-9.]+)\]', P)
ctags = re.findall(r'^\| (C-[A-Z0-9.]+) \|', C, flags=re.M)
out['prereg_tags'] = ptags
out['csm_rows'] = ctags
out['tags_missing_in_csm'] = [t for t in ptags if t not in ctags]
out['csm_rows_not_in_prereg'] = [t for t in ctags if t not in ptags]
out['duplicate_prereg_tags'] = sorted({t for t in ptags if ptags.count(t) > 1})
# entries cited with section pins in PREREG section 11
pinned = re.findall(r'^\| (A\d+) \| [^|]+\| `[0-9a-f]{64}` \|$', P, flags=re.M)
out['prereg_pinned_v005_entries'] = pinned
m = re.search(r'The following entries were read with no change to this text: ([^\n]+)', P)
out['prereg_no_change_text'] = m.group(1) if m else None
m = re.search(r'\*\*Entries read with no change to this text:\*\*\n((?:- [^\n]+\n)+)', C)
out['csm_no_change_text'] = m.group(1) if m else None
m = re.search(r'the cited entries are ([^;\n]+)', R)
out['root_items_m6_cited'] = m.group(1) if m else None
# every A-number mentioned anywhere in each file
def anums(t):
    return sorted({int(x) for x in re.findall(r'\bA(\d{2})(?:\.\d)?\b', t)})
out['A_mentioned_prereg'] = anums(P)
out['A_mentioned_csm'] = anums(C)
out['A_mentioned_root_items'] = anums(R)
v005 = [a for a in range(47, 92)]
out['A_used_not_pinned_prereg_csm_rootitems'] = sorted({a for a in anums(P) + anums(C) + anums(R) if a >= 47} - {int(x[1:]) for x in pinned})
# root item numbering
out['root_items_headings'] = re.findall(r'^## (M-\d+)\.', R, flags=re.M)
out['prereg_root_item_rows'] = re.findall(r'^\| (M-\d+) \|', P, flags=re.M)
print(json.dumps(out, indent=1))
