# R2-C lens: inventory of every digit-bearing substring that check v002's stripping rules remove from the three real
# round-2 text files, by rule, in the order the check applies them. Read-only; prints JSON to stdout (redirect to runs/).
import sys, os, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_r2c
fence_r2c.install()
O = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r2/round2'
sys.path.insert(0, O + '/tools')
import check_target_free_c4v002 as T
rules = [('HEX64', T.HEX64), ('ELIDED', T.ELIDED), ('HEXL', T.HEXL), ('ISO', T.ISO), ('SECTION', T.SECTION), ('BACKTICK', re.compile('`')),
         ('TAGSPAN', re.compile(r'\[C-[^\]]+\]')), ('IDENT_CHAIN', T.IDENT_CHAIN), ('IDENT_DIGIT', T.IDENT_DIGIT)]
out = {}
for name in T.TEXT_FILES:
    t = T.norm(open(os.path.join(O, name), 'rb').read().decode('utf-8'))
    per = collections.OrderedDict()
    for rn, rx in rules:
        found = [m.group(0) for m in rx.finditer(t) if re.search(r'\d', m.group(0))]
        per[rn] = dict(collections.Counter(found))
        t = rx.sub(' ', t)
    # digits glued to a preceding word char that NUM's lookbehind skips, after all stripping
    per['NUM_LOOKBEHIND_SKIPPED'] = dict(collections.Counter(m.group(0) for m in re.finditer(r'(?<=[^\W\d])\d+(?:\.\d+)?', t)))
    tags = set(T.TAG.findall(open(os.path.join(O, name), encoding='utf-8').read()))
    per['TAGSPAN_not_wellformed_tags'] = [s for s in per['TAGSPAN'] if s[1:-1] not in tags]
    out[name] = per
print(json.dumps(out, indent=1, ensure_ascii=False))
