"""0349 documentation-only reconciliation of the in-file MRT header (lines 10-28) and the CDS ReadMe table1.dat
byte-by-byte description (tag-stripped lines 148-175). Reads NO data rows (only header lines 1..98 of the MRT).

Checks:
  * field order and label correspondence for all 19 fields;
  * formats equal except f_D (I2 vs I1);
  * CDS start/end == header start/end + (k-1) for fields k=2..5 and + (k-2) for k>=6 (one blank before every field,
    f_D narrowed to one byte), Galaxy unchanged;
  * CDS Lrecl 130 == 113 + 18 separators - 1;
  * derived 'H+1' layout (header widths, one blank before every field, f_D kept I2);
  * CDS null markers: whether any explanation of fields 1-7 starts with '?' (CDS Standard: nullable column).
Usage: python3 -I doc_reconciliation_0349.py <new_output.json>
"""
import hashlib, html, json, re, sys

MRT = ('/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/'
       'joint_parent_continuation/external_ddo154_v001/SPARC_Lelli2016c.mrt',
       '5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243')
CDS = ('/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/'
       'joint_parent_continuation/external_ddo154_v001/SPARC_ReadMe.html',
       '457f61cd8e63dd7b8f8ce0052a458294fa1a5acc2b5b23bb951a2c40d69f9666')
LABEL_MAP = [('Galaxy', 'Name'), ('T', 'Type'), ('D', 'Dist'), ('e_D', 'e_Dist'), ('f_D', 'f_Dist'), ('Inc', 'i'),
             ('e_Inc', 'e_i'), ('L[3.6]', 'L3.6'), ('e_L[3.6]', 'e_L3.6'), ('Reff', 'Reff'), ('SBeff', 'SBeff'),
             ('Rdisk', 'Rdisk'), ('SBdisk', 'SBdisk'), ('MHI', 'MHI'), ('RHI', 'RHI'), ('Vflat', 'Vflat'),
             ('e_Vflat', 'e_Vflat'), ('Q', 'Qual'), ('Ref.', 'Ref')]
ROW = re.compile(r'^\s*(\d+)(?:-\s*(\d+))?\s+([AIF]\d+(?:\.\d+)?)\s+(\S+)\s+(\S+)\s*(.*)$')


def main(out):
    mb = open(MRT[0], 'rb').read()
    assert hashlib.sha256(mb).hexdigest() == MRT[1], 'E_PIN_MRT'
    hdr_lines = mb.split(b'\n')[:98]
    del mb
    hdr = []
    for i in range(9, 28):  # lines 10..28
        m = ROW.match(hdr_lines[i].decode('ascii'))
        a, e = int(m.group(1)), int(m.group(2) or m.group(1))
        hdr.append({'line': i + 1, 'start': a, 'end': e, 'fmt': m.group(3), 'label': m.group(5), 'expl': m.group(6)})
    cb = open(CDS[0], 'rb').read()
    assert hashlib.sha256(cb).hexdigest() == CDS[1], 'E_PIN_CDS'
    txt = html.unescape(re.sub(r'<[^>]+>', '', cb.decode('utf-8', 'replace'))).splitlines()
    cds = []
    for i in range(147, 175):  # lines 148..175
        m = ROW.match(txt[i])
        if m:
            a, e = int(m.group(1)), int(m.group(2) or m.group(1))
            cds.append({'line': i + 1, 'start': a, 'end': e, 'fmt': m.group(3), 'label': m.group(5),
                        'expl_starts_with_question_mark': m.group(6).lstrip().startswith('?')})
    lrecl_line = [l for l in txt if l.startswith('table1.dat')]
    res = {'n_header_fields': len(hdr), 'n_cds_fields': len(cds)}
    rows = []
    all_order = all_fmt = all_shift = True
    hplus1 = {}
    for k, ((hl, cl), h, c) in enumerate(zip(LABEL_MAP, hdr, cds), start=1):
        order_ok = (h['label'] == hl and c['label'] == cl)
        fmt_eq = h['fmt'] == c['fmt']
        width_h = int(re.match(r'[AIF](\d+)', h['fmt']).group(1))
        shift = 0 if k == 1 else (k - 1 if k <= 5 else k - 2)
        exp_start = h['start'] + shift
        exp_end = h['end'] + shift - (1 if k == 5 else 0)
        shift_ok = (c['start'] == exp_start and c['end'] == exp_end)
        hp = 0 if k == 1 else k - 1
        hplus1[hl] = [h['start'] + hp, h['end'] + hp, h['fmt']]
        all_order &= order_ok
        all_fmt &= (fmt_eq or k == 5)
        all_shift &= shift_ok
        rows.append({'k': k, 'header': [h['start'], h['end'], h['fmt'], h['label'], 'line %d' % h['line']],
                     'cds': [c['start'], c['end'], c['fmt'], c['label'], 'line %d' % c['line']],
                     'order_label_ok': order_ok, 'format_equal': fmt_eq, 'header_width': width_h,
                     'cds_equals_header_plus_one_blank_per_field_with_fD_I1': shift_ok,
                     'cds_null_marker_question_mark': c['expl_starts_with_question_mark']})
    res['fields'] = rows
    res['all_19_in_same_order_with_corresponding_labels'] = all_order
    res['formats_equal_except_fD'] = all_fmt
    res['fD_formats'] = [hdr[4]['fmt'], cds[4]['fmt']]
    res['cds_layout_is_header_plus_one_leading_blank_per_field_fD_narrowed_to_I1'] = all_shift
    res['header_total_width'] = hdr[-1]['end']
    res['cds_lrecl_line'] = lrecl_line
    res['predicted_cds_lrecl'] = hdr[-1]['end'] + 18 - 1
    res['derived_H_plus_1_layout_header_widths_one_leading_blank_fD_I2'] = hplus1
    res['derived_H_plus_1_record_length'] = hdr[-1]['end'] + 18
    res['fields_1_7_any_cds_null_marker'] = any(r['cds_null_marker_question_mark'] for r in rows[:7])
    res['any_cds_null_marker'] = any(r['cds_null_marker_question_mark'] for r in rows)
    res['notes'] = {
        'header_note_1_lines': '30-32 (Type codes 0..11)', 'header_note_2_lines': '33-38 (f_D codes 1..5)',
        'cds_note_1_lines': '177-191 (Type codes 0..11)', 'cds_note_2_lines': '192-199 (f_Dist codes 1..5)',
        'cds_standard_reference_line': '256 (follows the Standard Description for Astronomical Catalogues)'}
    with open(out, 'x') as f:
        json.dump(res, f, indent=1)
    print(json.dumps({'ok': True, 'order': all_order, 'shift_rule': all_shift, 'output': out}))


if __name__ == '__main__':
    main(sys.argv[1])
