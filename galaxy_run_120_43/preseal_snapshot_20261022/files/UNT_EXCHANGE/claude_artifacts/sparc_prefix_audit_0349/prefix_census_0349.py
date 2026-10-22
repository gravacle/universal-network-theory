"""0349 structural prefix census of the sha-pinned SPARC_Lelli2016c.mrt (read-only; aggregate output only).

Exposure discipline:
  * The whole file is read into memory, hashed and split on LF (same as V002).
  * Header lines 1..98 are used only to locate the last header separator.
  * For every data row only bytes 1..41 are sliced (l[:41]); nothing beyond byte 41 is decoded, compared or measured.
    The only length fact used is the boolean "row reaches byte 41" (len(l[:41]) == 41).
  * Output: aggregate counts, class masks of bytes 12..41, span/shape distributions, booleans.
    No galaxy name other than the two targets is emitted; for the targets only masks/spans/booleans.
    No numeric field value of any row is emitted. Domain checks are run only for Type (Note 1) and f_D (Note 2),
    as the brief asks; D/e_D/Inc/e_Inc numeric ranges are NOT evaluated here (structural census only).
Usage: python3 -I prefix_census_0349.py <new_output.json>
"""
import hashlib, json, re, sys
from collections import Counter

SRC = ('/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/'
       'joint_parent_continuation/external_ddo154_v001/SPARC_Lelli2016c.mrt',
       '5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243')
TARGETS = ('DDO154', 'NGC3198')
GIVEN_MASKS = {'DDO154': '_____AAA999_99___9.99__9.99__9_99.9__9.9_',
               'NGC3198': '____AAA9999__9__99.99__9.99__9_99.9__9.9_'}
HPLUS1_SEPARATORS = (12, 15, 22, 28, 31, 36, 41)
CDS_SEPARATORS = (12, 15, 22, 28, 30, 35, 40)
POS = ['Galaxy', 'T', 'D', 'e_D', 'f_D', 'Inc', 'e_Inc']
DEC = {'D': 2, 'e_D': 2, 'Inc': 1, 'e_Inc': 1}
# Same token shapes as prefix_contract_checker_0349.SHAPES (C6), evaluated structurally on every row.
TIGHT = {'T': rb'(?:[0-9]|1[01])', 'D': rb'(?:0|[1-9][0-9]{0,2})\.[0-9]{2}', 'e_D': rb'(?:0|[1-9][0-9]?)\.[0-9]{2}',
         'f_D': rb'[1-5]', 'Inc': rb'(?:0|[1-9][0-9]?)\.[0-9]', 'e_Inc': rb'(?:0|[1-9][0-9]?)\.[0-9]'}
# Fixed-offset layouts evaluated STRUCTURALLY (is each slice a right-justified, format-valid literal?) -- no values.
LAYOUTS = {
    'MRT_HEADER_AS_WRITTEN': {'T': (12, 13, 'I'), 'D': (14, 19, 2), 'e_D': (20, 24, 2), 'f_D': (25, 26, 'I'),
                              'Inc': (27, 30, 1), 'e_Inc': (31, 34, 1)},
    'CDS_TABLE1_README': {'T': (13, 14, 'I'), 'D': (16, 21, 2), 'e_D': (23, 27, 2), 'f_D': (29, 29, 'I'),
                          'Inc': (31, 34, 1), 'e_Inc': (36, 39, 1)},
    'DERIVED_H_PLUS_1': {'T': (13, 14, 'I'), 'D': (16, 21, 2), 'e_D': (23, 27, 2), 'f_D': (29, 30, 'I'),
                         'Inc': (32, 35, 1), 'e_Inc': (37, 40, 1)},
}


def slice_valid(p, a, e, kind):
    s = p[a - 1:e]
    if len(s) != e - a + 1:
        return False
    if kind == 'I':
        return bool(re.fullmatch(rb' *[0-9]+', s))
    return bool(re.fullmatch(rb' *[0-9]+\.[0-9]{%d}' % kind, s))


def cls(c):
    if c == 32: return '_'
    if 48 <= c <= 57: return '9'
    if c == 46: return '.'
    if 65 <= c <= 90 or 97 <= c <= 122: return 'A'
    if 33 <= c <= 126: return 'p'   # other printable ASCII punctuation
    return '?'                       # TAB, CR, control, non-ASCII


def mask(b):
    return ''.join(cls(c) for c in b)


def main(out):
    b = open(SRC[0], 'rb').read()
    sha = hashlib.sha256(b).hexdigest()
    if sha != SRC[1]:
        raise SystemExit('E_PIN')
    lines = b.split(b'\n')
    del b
    seps = [i for i, l in enumerate(lines[:200]) if re.fullmatch(rb'-{20,}', l.strip())]
    first_data_idx = seps[-1] + 1            # 0-based
    data = lines[first_data_idx:]
    trailing_empty = 0
    while data and data[-1] == b'':
        data.pop(); trailing_empty += 1
    n = len(data)
    first_line_no = first_data_idx + 1
    last_line_no = first_line_no + n - 1

    C = Counter()
    tokcount = Counter()
    name_tok_in_1_11 = Counter()
    name_just = Counter()
    name_end = Counter()
    name_punct = Counter()
    span_start = {p: Counter() for p in POS}
    span_end = {p: Counter() for p in POS}
    shape = {p: Counter() for p in POS[1:]}
    mask12_41 = Counter()
    type_width = Counter()
    fd_width = Counter()
    anomalies = []
    target_report = {}
    target_hits = Counter()
    layout_valid = {k: Counter() for k in LAYOUTS}

    for k, l in enumerate(data):
        line_no = first_line_no + k
        p = l[:41]
        reaches41 = len(p) == 41
        C['rows'] += 1
        C['reaches_byte_41'] += reaches41
        bad = [c for c in p if not (c == 32 or 33 <= c <= 126)]
        C['prefix_all_printable_ascii_or_blank'] += (not bad)
        C['prefix_has_tab'] += (9 in p)
        C['prefix_has_cr'] += (13 in p)
        b41 = reaches41 and p[40] == 32
        C['byte41_blank'] += b41
        toks = [(m.start() + 1, m.end()) for m in re.finditer(rb'[^ ]+', p)]
        tokcount[len(toks)] += 1
        # name field bytes 1-11
        ntoks = list(re.finditer(rb'[^ ]+', p[:11]))
        name_tok_in_1_11[len(ntoks)] += 1
        name = p[:11].strip(b' ')
        C['name_has_internal_blank'] += (b' ' in name)
        if p[:1] != b' ' and p[10:11] == b' ': name_just['left'] += 1
        elif p[:1] == b' ' and p[10:11] != b' ': name_just['right'] += 1
        elif p[:1] != b' ' and p[10:11] != b' ': name_just['full_11'] += 1
        else: name_just['other'] += 1
        C['byte12_blank'] += (len(p) >= 12 and p[11] == 32)
        for ch in name:
            if not (48 <= ch <= 57 or 65 <= ch <= 90 or 97 <= ch <= 122):
                name_punct[chr(ch)] += 1
        C['hplus1_separators_all_blank'] += all(len(p) >= x and p[x - 1] == 32 for x in HPLUS1_SEPARATORS)
        C['cds_separators_all_blank'] += all(len(p) >= x and p[x - 1] == 32 for x in CDS_SEPARATORS)
        mask12_41[mask(p[11:41])] += 1
        for lname, lay in LAYOUTS.items():
            allok = True
            for fld, (a, e, kind) in lay.items():
                ok = slice_valid(p, a, e, kind)
                layout_valid[lname][fld] += ok
                allok &= ok
            layout_valid[lname]['ALL_SIX'] += allok
        if len(toks) == 7:
            C['exactly_7_tokens'] += 1
            name_end[toks[0][1]] += 1
            C['token1_within_1_11'] += (toks[0][1] <= 11)
            for (a, e), fld in zip(toks, POS):
                span_start[fld][a] += 1
                span_end[fld][e] += 1
            for (a, e), fld in zip(toks[1:], POS[1:]):
                shape[fld][mask(p[a - 1:e])] += 1
            t = {fld: p[a - 1:e] for (a, e), fld in zip(toks, POS)}
            # Type (Note 1) and f_D (Note 2) domain: the only value-level checks in this census
            type_width[len(t['T'])] += 1
            C['T_is_digits'] += bool(re.fullmatch(rb'[0-9]+', t['T']))
            C['T_domain_0_11_no_leading_zero'] += bool(re.fullmatch(rb'(?:[0-9]|1[01])', t['T']))
            fd_width[len(t['f_D'])] += 1
            C['fD_single_digit_1_5'] += bool(re.fullmatch(rb'[1-5]', t['f_D']))
            ok_dec = True
            for fld, d in DEC.items():
                good = bool(re.fullmatch(rb'[0-9]+\.[0-9]{%d}' % d, t[fld]))
                C['decimals_ok_' + fld] += good
                ok_dec &= good
            C['F_widths_ok'] += (len(t['D']) <= 6 and len(t['e_D']) <= 5 and len(t['Inc']) <= 4 and len(t['e_Inc']) <= 4)
            C['all_four_F_decimals_ok'] += ok_dec
            ends = tuple(e for (a, e) in toks[1:])
            C['token_ends_2_7_eq_14_21_27_30_35_40'] += (ends == (14, 21, 27, 30, 35, 40))
            tight_all = True
            for fld, rx in TIGHT.items():
                ok = bool(re.fullmatch(rx, t[fld]))
                C['tight_shape_ok_' + fld] += ok
                tight_all &= ok
                C['leading_zero_before_digit_' + fld] += bool(re.match(rb'0[0-9]', t[fld]))
            structural = (b41 and not bad and toks[0][1] <= 11 and len(ntoks) == 1 and tight_all
                          and tuple(e for (a, e) in toks) == (11, 14, 21, 27, 30, 35, 40))
            C['structural_contract_C2_C3_C4_C5_C6_C9_pass_own_name'] += structural
            C['token7_ends_le_40'] += (toks[6][1] <= 40)
        else:
            anomalies.append({'line': line_no, 'n_tokens_1_41': len(toks)})
        nm = name.decode('ascii', 'replace')
        if nm in TARGETS:
            target_hits[nm] += 1
            target_report[nm] = {
                'line': line_no,
                'class_mask_1_41': mask(p).replace('p', '?'),
                'matches_given_mask': mask(p) == GIVEN_MASKS[nm],
                'token_spans': [[a, e] for a, e in toks],
                'n_tokens': len(toks),
                'byte41_blank': b41,
            }

    def srt(c):
        return {str(k): v for k, v in sorted(c.items(), key=lambda kv: (str(kv[0])))}

    res = {
        'schema': 'CLAUDE2_0349_SPARC_PREFIX_CENSUS_V001',
        'source': {'path': SRC[0], 'sha256': sha},
        'scope': 'bytes 1-41 of every data row; aggregate only; no values except Type/f_D domain booleans',
        'data_rows': {'first_line': first_line_no, 'last_line': last_line_no, 'count': n,
                      'trailing_empty_split_elements': trailing_empty,
                      'last_header_separator_line': seps[-1] + 1},
        'counts': dict(C),
        'tokens_in_bytes_1_41_distribution': srt(tokcount),
        'name_field': {'tokens_in_bytes_1_11_distribution': srt(name_tok_in_1_11),
                       'justification': dict(name_just),
                       'name_token_end_byte_distribution': srt(name_end),
                       'non_alphanumeric_chars_in_names_with_counts': dict(name_punct)},
        'token_span_start_distribution': {f: srt(c) for f, c in span_start.items()},
        'token_span_end_distribution': {f: srt(c) for f, c in span_end.items()},
        'token_shape_distribution_by_position': {f: srt(c) for f, c in shape.items()},
        'type_token_width_distribution': srt(type_width),
        'fD_token_width_distribution': srt(fd_width),
        'distinct_class_masks_bytes_12_41': {'n_distinct': len(mask12_41), 'masks_with_counts': srt(mask12_41)},
        'fixed_offset_layouts_structural_validity_row_counts': {
            'definition': 'rows (of 175) whose slice is a right-justified format-valid literal (I: blanks then digits; '
                          'Fw.d: blanks, digits, point, exactly d digits); ALL_SIX = all six slices valid',
            'layouts': {k: dict(v) for k, v in layout_valid.items()},
            'layout_bytes': {k: {f: [a, e] for f, (a, e, _) in v.items()} for k, v in LAYOUTS.items()}},
        'anomalous_rows_not_7_tokens': anomalies,
        'targets': {'hits': dict(target_hits), 'report': target_report},
        'mask_legend': "_ blank, 9 digit, . point, A letter, p other printable ASCII, ? control/non-ASCII",
    }
    with open(out, 'x') as f:
        json.dump(res, f, indent=1)
    print(json.dumps({'ok': True, 'output': out}))


if __name__ == '__main__':
    main(sys.argv[1])
