#!/usr/bin/env python3
"""r3a_final_bytecheck_c3v001.py: Claude3-lane pre-stage for root dispatch 0850 item 4 (S7).

FOR THE LEAD, AT CLAUDE4'S FINAL r3a RENDER. NOT RUN AT PRE-STAGE TIME (2026-10-21).
Read-only. It reads only the files passed by the lead, writes nothing, and prints
sha256 values, counts, booleans and line numbers. It prints no V006 text and no prereg text
(the only strings echoed are the two read-time stamps captured from the rendered text).

What it proves when ALL_CHECKS_TRUE:
  the final rendered text equals the basis template the M-12 classifiers were built on
  (classifier_a_c4/build_c4v001/basis/PREREG_MISS_READING_R3A.md, sha256 1e17eb45...),
  byte for byte, outside the nine generator sites of section 11, and the filled sites
  agree with the bytes they describe.

Usage (the program's isolated interpreter, -I -B):
  python3 -I -B r3a_final_bytecheck_c3v001.py FINAL=<rendered PREREG_MISS_READING_R3A.md> \
     [ROOT_ITEMS=<rendered ROOT_ITEMS_R3A.md>] [CSM=<rendered CLAUSE_SOURCE_MAP_R3A.md>] \
     [POST=<FROM_CLAUDE4 SEAL CANDIDATE post>] [V006=<V006 addendum>] \
     [V006_JSON=<V006_ENTRY_TABLE_R3A.json>] [V005=<V005 addendum>] [FREEZE_SHA=<sha root posted at FREEZE OPEN>] \
     [D0519=<FROM_CODEX/0519_*>] [D0521=<FROM_CODEX/0521_*>] [D0523=<FROM_CODEX/0523_*>]
Exit status 0 only if every check that ran is True. A False is a STOP for the lead, not a finding by itself:
the lead then runs the plain diff of step R4 and reviews each hunk.
"""
import hashlib
import json
import pathlib
import re
import sys

BASIS = pathlib.Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/classifier_a_c4/build_c4v001/basis')
PIN = {
    'TEMPLATE': '1e17eb459c43d40205e7ed913da16de8b67e2762fa5e1a440699de796d9216a5',
    'CSM': '03ded7fa39b4b7cf1400cd2f89536eed727ca8c420c97d60485afddcce771e09',
    'ROOT_ITEMS': '9c40b567410e066465f01b21d656398ce6abd9c62fd16959b8bb92ed56aee6ae',
    'CLASSIFIER_A': 'e92aa30e22b98fea6c6e517702c02f77c43bfe429f69f8e0392963c94edc4cb0',
}
# The nine generator sites of the template (pre-stage grep: each occurs exactly once, section 11).
SITES = ['@@SHA_0519@@', '@@SHA_0521@@', '@@SHA_0523@@', '@@V005_SHA@@', '@@V006_SHA@@',
         '@@V005_READ_UTC@@', '@@V005_ENTRY_TABLE@@', '@@V006_READ_UTC@@', '@@V006_ENTRY_TABLE@@']
HEX64 = re.compile(r'[0-9a-f]{64}')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rd(p):
    return pathlib.Path(p).read_bytes()


def fill_sites(tpl, fin):
    """Return {placeholder: filled text} if fin is tpl with each site replaced, else None."""
    parts = re.split(r'(@@[A-Z0-9_]+@@)', tpl)
    phs = parts[1::2]
    if sorted(phs) != sorted(SITES) or len(set(phs)) != len(phs):
        raise SystemExit('STOP: template sites differ from the pre-staged nine')
    if not fin.startswith(parts[0]):
        return None
    pos, caps = len(parts[0]), {}
    for k in range(1, len(parts), 2):
        ph, nxt = parts[k], parts[k + 1]
        if k + 1 == len(parts) - 1:
            if not fin.endswith(nxt):
                return None
            end = len(fin) - len(nxt)
        else:
            end = fin.find(nxt, pos)
        if end < pos:
            return None
        caps[ph] = fin[pos:end]
        pos = end + len(nxt)
    return caps if pos == len(fin) else None


def main():
    a = dict(x.split('=', 1) for x in sys.argv[1:])
    out, oks = {}, []

    def chk(name, val):
        out[name] = bool(val)
        oks.append(bool(val))

    tpl_b = rd(BASIS / 'PREREG_MISS_READING_R3A.md')
    chk('R1_template_is_basis_1e17eb45', sha(tpl_b) == PIN['TEMPLATE'])
    fin_b = rd(a['FINAL'])
    fin_sha = sha(fin_b)
    out['final_text_sha256'] = fin_sha
    fin = fin_b.decode('utf-8')
    chk('R1_final_has_no_@@_token', '@@' not in fin)
    caps = fill_sites(tpl_b.decode('utf-8'), fin)
    chk('R2_final_equals_template_outside_the_nine_sites', caps is not None)
    if caps:
        for ph in ('@@SHA_0519@@', '@@SHA_0521@@', '@@SHA_0523@@', '@@V005_SHA@@', '@@V006_SHA@@'):
            chk('R2_site_is_64_hex_' + ph.strip('@'), HEX64.fullmatch(caps[ph]) is not None)
        for ph in ('@@V005_READ_UTC@@', '@@V006_READ_UTC@@'):
            chk('R2_site_is_one_line_' + ph.strip('@'), '\n' not in caps[ph])
        out['v005_read_utc_in_text'] = caps['@@V005_READ_UTC@@']
        out['v006_read_utc_in_text'] = caps['@@V006_READ_UTC@@']
        out['v006_whole_sha_in_text'] = caps['@@V006_SHA@@']
        for d in ('0519', '0521', '0523'):
            if 'D' + d in a:
                chk('R3_dispatch_' + d + '_sha_matches_bytes', sha(rd(a['D' + d])) == caps['@@SHA_' + d + '@@'])
        if 'V005' in a:
            chk('R3_v005_whole_sha_matches_bytes', sha(rd(a['V005'])) == caps['@@V005_SHA@@'])
        if 'FREEZE_SHA' in a:
            chk('R5_v006_sha_in_text_equals_FREEZE_OPEN_sha', caps['@@V006_SHA@@'] == a['FREEZE_SHA'])
    if 'V006' in a:
        v6 = rd(a['V006'])
        lines = v6.split(b'\n')
        heads = [i for i, ln in enumerate(lines) if ln.startswith(b'## ')]

        def section(j):
            end = heads[j + 1] if j + 1 < len(heads) else len(lines)
            return b'\n'.join(lines[heads[j]:end])

        seal_j = next((j for j in range(len(heads)) if fin_sha.encode() in section(j)), None)
        out['v006_headings_total'] = len(heads)
        out['v006_seal_entry_heading_line'] = (heads[seal_j] + 1) if seal_j is not None else None
        if seal_j is None:
            n = len(heads)
            chk('R5_final_sha_absent_from_v006', fin_sha.encode() not in v6)
            if caps:
                chk('R5_v006_unchanged_since_assembly_read', sha(v6) == caps['@@V006_SHA@@'])
            out['v006_trimmed_sha_now'] = sha(v6.rstrip(b'\n'))
        else:
            n = seal_j
            prefix = b'\n'.join(lines[:heads[seal_j]])
            chk('R6_final_sha_absent_before_seal_entry', fin_sha.encode() not in prefix)
            out['v006_prefix_trimmed_sha'] = sha(prefix.rstrip(b'\n'))
        out['v006_headings_before_seal'] = n
        a133 = [j for j in range(n) if re.match(rb'## A133(\D|$)', lines[heads[j]])]
        if caps:
            tb = caps['@@V006_ENTRY_TABLE@@']
            if a133:
                s133 = sha(section(a133[0]).rstrip(b'\n'))
                out['a133_section_trimmed_sha'] = s133
                chk('R5_a133_section_sha_in_v006_table', s133 in tb)
            missing = []
            for j in range(n):
                hid = lines[heads[j]][3:].split(b':')[0].strip().decode('utf-8', 'replace')
                if not re.search(r'(?<![0-9A-Za-z])' + re.escape(hid) + r'(?![0-9])', tb):
                    missing.append(heads[j] + 1)
            out['v006_heading_ids_missing_from_table_at_lines'] = missing
            chk('R5_v006_table_names_every_heading_before_seal', not missing)
            out['v006_table_pipe_lines'] = sum(1 for ln in tb.split('\n') if ln.startswith('|'))
    if 'V006_JSON' in a:
        jb = rd(a['V006_JSON'])
        out['v006_table_json_sha256'] = sha(jb)
        j = json.loads(jb)
        top = j if isinstance(j, dict) else {}
        out['v006_json_top_keys'] = sorted(top.keys())
        hexes = sorted({v for v in top.values() if isinstance(v, str) and HEX64.fullmatch(v)})
        out['v006_json_top_level_hex'] = hexes
        rows = max((v for v in top.values() if isinstance(v, list)), key=len, default=[])
        out['v006_json_longest_list'] = len(rows)
        if 'v006_prefix_trimmed_sha' in out:
            chk('R6_prefix_trimmed_sha_is_the_json_trimmed_sha', out['v006_prefix_trimmed_sha'] in hexes)
        if 'v006_headings_before_seal' in out:
            chk('R5_json_rows_equal_headings_before_seal', len(rows) == out['v006_headings_before_seal'])
    for key in ('ROOT_ITEMS', 'CSM'):
        if key in a:
            s = sha(rd(a[key]))
            out[key.lower() + '_sha256'] = s
            chk('R4_' + key.lower() + '_identical_to_basis', s == PIN[key])
    if 'POST' in a:
        pb = rd(a['POST'])
        pt = pb.decode('utf-8', 'replace')
        out['post_sha256'] = sha(pb)
        chk('R7_post_title_line_has_SEAL_CANDIDATE', 'SEAL CANDIDATE' in pt.split('\n', 1)[0])
        chk('R7_post_names_text_sha_once', pt.count(fin_sha) == 1)
        if 'root_items_sha256' in out:
            chk('R7_post_names_root_items_sha_once', pt.count(out['root_items_sha256']) == 1)
        chk('R7_post_names_classifier_A_c4v004_once', pt.count(PIN['CLASSIFIER_A']) == 1)
        out['post_contains_classifier_none'] = 'classifier: none' in pt
    out['ALL_CHECKS_TRUE'] = all(oks)
    print(json.dumps(out, indent=1, sort_keys=True))
    sys.exit(0 if all(oks) else 1)


if __name__ == '__main__':
    main()
