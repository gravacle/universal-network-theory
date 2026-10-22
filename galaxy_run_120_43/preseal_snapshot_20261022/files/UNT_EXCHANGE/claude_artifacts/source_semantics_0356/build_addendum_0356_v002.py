"""0356 addendum builder V002 (CLAUDE2 helper 0356-A).

Build mode composes SOURCE_SEMANTICS_ADDENDUM_0356_V002.json from the V002 probe evidence plus separately marked interpretation
text; every quoted source line is asserted against the probe evidence. Before anything is written, a LITERAL SCAN runs over the
addendum bytes and over every other V002 deliverable named on the command line; the build fails if any decimal literal outside the
allowed classes appears. Scan mode runs the same scan over any list of files (used by the deploy step, manifest included).

Allowed decimal classes (everything else fails):
  SHA256        64 lowercase hex digits
  TIMESTAMP     ISO-8601 date-time with fractional seconds (download sidecars)
  FORMAT_CODE   Fortran/CDS format codes such as F5.1 or F3.1
  ARXIV_ID      four digits, a point, four or five digits (document identifiers)
  BAND_LABEL    the band name written as 3.6-micron
  FLAG_OR_QUANTUM  the error flag literals 1.0 and 0.0, and the F5.1 quantum statements 0.05 and 0.1
Integers (counts, line numbers, row indices, byte sizes) are not decimals and are not restricted.

Usage:
  python3 -I -B build_addendum_0356_v002.py build <probe_evidence.json> <probe_script.py> <new_addendum.json> [other V002 files to scan ...]
  python3 -I -B build_addendum_0356_v002.py scan <file> [<file> ...]
"""
import hashlib, json, re, sys

ALLOWED = [('SHA256', r'[0-9a-f]{64}'),
           ('TIMESTAMP', r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+'),
           ('FORMAT_CODE', r'(?<![A-Za-z0-9_])[AIF]\d+\.\d+(?![0-9])'),
           ('ARXIV_ID', r'(?<![0-9.])\d{4}\.\d{4,5}(?![0-9]|\.[0-9])'),
           ('BAND_LABEL', r'(?<![0-9.])3\.6(?=-micron)'),
           ('FLAG_OR_QUANTUM', r'(?<![0-9.])(?:1\.0|0\.0|0\.05|0\.1)(?![0-9]|\.[0-9])')]
RESIDUAL = r'\d+\.\d+'


def literal_scan(name, text):
    s = text
    used = {}
    for cls, rx in ALLOWED:
        n = len(re.findall(rx, s))
        if n:
            used[cls] = n
        s = re.sub(rx, ' ', s)
    bad = []
    for m in re.finditer(RESIDUAL, s):
        line = s.count('\n', 0, m.start()) + 1
        bad.append({'line_after_masking': line, 'context_digits_masked': re.sub(r'\d', '#', s[max(0, m.start() - 20):m.end() + 20])})
    return {'file': name, 'pass': not bad, 'allowed_class_counts': used, 'violations': bad}


def scan_files(paths):
    out = [literal_scan(p.split('/')[-1], open(p, encoding='utf-8').read()) for p in paths]
    return out


if len(sys.argv) >= 3 and sys.argv[1] == 'scan':
    res = scan_files(sys.argv[2:])
    print(json.dumps({'literal_scan': 'PASS' if all(r['pass'] for r in res) else 'FAIL', 'files': res}, indent=1))
    sys.exit(0 if all(r['pass'] for r in res) else 1)
if len(sys.argv) < 5 or sys.argv[1] != 'build':
    raise SystemExit('usage: build <probe_evidence.json> <probe_script.py> <new_addendum.json> [files ...] | scan <files ...>')

PE, PS, OUT = sys.argv[2:5]
OTHERS = sys.argv[5:]
pe_b = open(PE, 'rb').read()
P = json.loads(pe_b)
sha = lambda b: hashlib.sha256(b).hexdigest()
L = P['leroy_readme_lines']
R = P['readiness_note_lines_digits_masked']
NF = P['leroy_table7_null_flag_by_label']
pin = lambda k: {'path': P['pins_verified'][k]['path'], 'sha256': P['pins_verified'][k]['sha256']}


def lr(n, expect):
    assert L[str(n)].strip() == expect, (n, L[str(n)])
    return {'path': pin('leroy_readme')['path'], 'sha256': pin('leroy_readme')['sha256'], 'line': n, 'text': expect,
            'class': 'PRIMARY (CDS ReadMe J/AJ/136/2782)', 'line_method': P['line_method_html']}


def rn(lines, masked_fragment):
    joined = ' '.join(R[str(n)] for n in lines)
    assert masked_fragment in joined, masked_fragment
    return {'path': pin('readiness_note')['path'], 'sha256': pin('readiness_note')['sha256'], 'lines': '%d-%d' % (lines[0], lines[-1]),
            'class': 'SECONDARY local note (cites Leroy et al. 2008 Appendix E, arXiv:0810.2556, not local)',
            'quoted_with_every_digit_masked': masked_fragment}


# ---- evidence assertions
S = P['sfb_structure']
assert S['n_uncommented_data_rows'] == 66 and S['commented_lines'] == [68, 69] and S['commented_rows_after_last_uncommented_row']
assert S['commented_rows_are_the_last_lines_of_the_file'] and S['commented_radius_tokens_equal_crosswalk_texts']
assert S['last_uncommented_radius_token_equals_crosswalk_text'] and S['kill_token_of_commented_rows_equals_flag_one'] == [True, True]
assert S['crosswalk_uncommented_row_count_equals_observed'] and S['crosswalk_commented_row_count_equals_observed'] and not S['line_1_is_commented']
D = P['dens_structure']
assert D['commented_lines'] == [1] and D['n_uncommented_rows'] == 77 and D['crosswalk_row_counts_in_order'] == [77, 66, 11]
assert D['crosswalk_total_equals_observed'] and D['crosswalk_matched_equals_sfb_uncommented_rows'] and D['crosswalk_counts_add_up']
ZS = P['zips']['sfb_zip']['aggregate_census']
LB = P['join_0352_stored_labels']
assert LB['row_2_stars']['upper_limit_marker'] is True and LB['row_2_stars']['value_missing'] is False
assert all(LB[k]['error_kind'] == 'LITERAL_ZERO_MEANING_UNRESOLVED' for k in ('row_16_stars', 'row_18_stars', 'row_20_stars'))
assert P['join_0352_HI_rows_with_upper_limit_marker'] == []
nullable = sorted(k for k, v in NF.items() if v['question_mark_null_flag'])
assert nullable == sorted(['SigmaHI', 'SigmaH2', 'e_SigmaH2', 'FUV+24', 'FUV', '24'])
assert not NF['Sigma*']['question_mark_null_flag'] and not NF['e_Sigma*']['question_mark_null_flag'] and NF['e_Sigma*']['note3_attached']
assert sorted(k for k, v in NF.items() if v['note3_attached']) == ['e_Sigma*', 'e_SigmaHI']
IDX = P['sparc_index_lines']
PDF = P['sparc_paper_pdf']
assert PDF['content_read'] is False and PDF['sidecar_sha256_matches_pdf']
assert all(P['leroy_readme_copies_identical'].values())
FZ = P['p53_freeze_digits_masked']
assert 'SEMANTIC_CONFLICT_PENDING_DISTINCT_REVIEW' in FZ['/choices/error_and_censoring'] and '"Gaussian_likelihood": null' in FZ['/choices/error_and_censoring']
assert 'MISSING_NOT_ZERO' in FZ['/choices/H2_missing_support']
BC = P['bundle_contract_v006_lines']
CW = P['crosswalk_0341_checks']
LG = P['ledger_0341_checks']
NS = P['name_only_search']['results']
assert NS['leroy_2008_paper']['matches'] == [] and all(PDF['path'].split('/')[-1] in m or PDF['path'].split('/')[-1] + '.SOURCE.json' in m for m in NS['archangel_documentation']['matches'])

pdf_ref = {'label': PDF['label'], 'path': PDF['path'], 'sha256': PDF['sha256'], 'bytes': PDF['bytes'],
           'sidecar': {'path': PDF['sidecar']['path'], 'sha256': PDF['sidecar']['sha256'], 'url': PDF['sidecar']['content']['url']}}
leroy_paper_missing = ('Leroy et al. 2008, AJ 136, 2782 (arXiv:0810.2556): Appendix E (radial-profile conventions) and the printed Table 7 '
                       'example. No local copy: the probe name-only search (PROBE_EVIDENCE /name_only_search/results/leroy_2008_paper) has no '
                       'match; the only local Leroy documentation is the CDS ReadMe (four byte-identical copies).')
sparc_paper_missing = {'statement': 'Lelli, McGaugh & Schombert 2016, AJ 152, 157 (SPARC master paper): description of the 3.6-micron surface-'
                                    'brightness profile files (.sfb columns kill/error and commented rows) and of the bulge-disk decompositions '
                                    '(.dens). A local file exists, outside the 0341/0346 document set; it was hashed, not opened.',
                       'candidate_local_copy': pdf_ref}
archangel_missing = ('Archangel photometry-system documentation (Schombert 2007), named by the SPARC index line 64: no local file. The probe '
                     'name-only search (/name_only_search/results/archangel_documentation) matches only the SPARC paper PDF and its sidecar, '
                     'whose file name contains an author name.')
ptr = lambda key, pointer, cls: {'path': pin(key)['path'], 'sha256': pin(key)['sha256'], 'pointer': pointer, 'class': cls}

items = [
    {'id': 'UR-4/U9/COLUMN_NOTE3',
     'binds': {'UR': ['UR-4'], 'U': ['U9'], 'OPEN': ['OPEN-8'], 'root_review_notes': ['D1']},
     'question': 'published meaning of the error literal 1.0 in the Leroy table7 error columns',
     'source_statements': [lr(186, 'Note (3): 1.0 = upper limit.'),
                           lr(172, '26- 28  F3.1 Msun/pc2         e_SigmaHI  rms uncertainty in SigmaHI (3)'),
                           lr(176, '50- 54  F5.1 Msun/pc2         e_Sigma*   rms uncertainty in Sigma* (3)'),
                           lr(174, '37- 40  F4.1 Msun/pc2         e_SigmaH2  ? RMS uncertainty in SigmaH2'),
                           lr(179, '64- 68  F5.1 10-4Msun/yr/kpc2 e_FUV+24   rms uncertainty in FUV+24'),
                           ptr('leroy_readme', 'PROBE_EVIDENCE /leroy_table7_null_flag_by_label (note3_attached)', 'PRIMARY, parsed per label')],
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'Note (3) is a column-level declaration attached to exactly two error columns, e_SigmaHI and e_Sigma*; it is not '
                                'attached to e_SigmaH2 or e_FUV+24. It declares that the literal 1.0 in those columns denotes "upper limit". The '
                                'ReadMe does not state which quantity is limited (the same-row surface density or the uncertainty), the value or '
                                'significance of any limit, or whether every literal 1.0 in those columns is a marker.'},
     'status': 'RESOLVED_DOCUMENTARY',
     'scope_of_resolution': 'what the local primary documentation (CDS ReadMe) states; its applicability to a populated row is item UR-4/U9/STARS_ROW2',
     'physically_open': 'no limit value, significance or likelihood is stated'},
    {'id': 'UR-4/U9/STARS_ROW2',
     'binds': {'UR': ['UR-4'], 'U': ['U9'], 'OPEN': ['OPEN-8', 'OPEN-9'], 'queries_via_bracketing_row': ['NGC3198-Q04', 'NGC3198-Q05', 'NGC3198-Q06', 'NGC3198-Q07'],
               'root_review_notes': ['D1']},
     'question': 'does the Note-3 marker apply to the only NGC 3198 occurrence, stars row 2 (raw table7 line %d), whose Sigma* is populated'
                 % LB['row_2_stars']['original_line_number'],
     'source_statements': [
         lr(175, '42- 48  F7.1 Msun/pc2           Sigma*   Surface density of stars'),
         lr(176, '50- 54  F5.1 Msun/pc2         e_Sigma*   rms uncertainty in Sigma* (3)'),
         lr(196, 'follows the rules of the Standard Description for Astronomical Catalogues;'),
         ptr('leroy_readme', 'PROBE_EVIDENCE /leroy_table7_null_flag_by_label', 'PRIMARY, parsed per label: "?" on %s; none on Sigma* or e_Sigma*' % ', '.join(sorted(nullable))),
         dict(ptr('join_0352', '/per_query/*/S1/rows (row_index 2, stars)', 'PROGRAM PRODUCT (bundle labels carried by the root-reviewed 0352 join)'),
              stored_labels=LB['row_2_stars']),
         dict(ptr('bundle_contract_v006', 'line 58', 'PROGRAM ADAPTER RULE (literal application of Note 3)'), text=BC['58']),
         rn([170, 171, 172, 173, 174, 175], 'The CDS note saying `#.# = upper limit` cannot be applied to every numeric error equal to one. '
            'The original printed example explicitly gives NGC ### at #.# kpc as stellar density ###.# with RMS #.#, and at #.#/#.# kpc as HI '
            '#.#/#.# with RMS #.#. These match the raw bytes. Thus NGC ####\'s populated stellar density ###.# and RMS #.# at #.# kpc is not a '
            'limit flag. In contrast, raw HI limits have blank density and #.# in the error slot.'),
         dict(ptr('p53_freeze', '/choices/error_and_censoring', 'PROGRAM FREEZE RECORD'), quoted_with_every_digit_masked=FZ['/choices/error_and_censoring'])],
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'Two local readings conflict for this row. (a) Literal CDS reading: Note (3) applies to every 1.0 in e_Sigma*, so stars '
                                'row 2 carries an upper-limit marker (P53 label UPPER_LIMIT_NOTE3; bundle upper_limit_marker true; value present). '
                                '(b) The secondary note reports that the primary paper\'s printed example (Appendix E) lists populated values with '
                                'RMS 1.0, concludes that NGC 3198\'s populated stellar row with RMS 1.0 "is not a limit flag", and says HI limits are '
                                'encoded as a blank density with 1.0 in the error slot. Schema fact relevant to both: Sigma* and e_Sigma* carry no '
                                '"?" null flag (lines 175-176), so a stellar entry is never blank and the blank-density encoding described in (b) '
                                'cannot occur for stars; Note (3) on e_Sigma* is the stellar-limit encoding the ReadMe gives. The P53 freeze already '
                                'records this as SEMANTIC_CONFLICT_PENDING_DISTINCT_REVIEW with Gaussian_likelihood null. Neither reading is adopted.'},
     'status': 'UNRESOLVED_MISSING_DOCUMENT',
     'missing_document': leroy_paper_missing,
     'missing_statement': 'whether a populated Sigma* with e_Sigma* = 1.0 in the electronic table7 is an upper limit or a measured value with rms 1.0',
     'physically_open': 'whether stars row 2 is a measurement or a limit; no bound value, significance, measurement error or likelihood is stated by any local source'},
    {'id': 'UR-4/D1/HI_COLUMN_NOTE',
     'binds': {'UR': ['UR-4'], 'U': ['U9'], 'OPEN': ['OPEN-8'], 'root_review_notes': ['D1']},
     'question': 'stars row-2 marker versus the HI column note',
     'source_statements': [lr(171, '20- 24  F5.2 Msun/pc2           SigmaHI  ? Surface density of H I (2)'),
                           lr(172, '26- 28  F3.1 Msun/pc2         e_SigmaHI  rms uncertainty in SigmaHI (3)'),
                           dict(ptr('join_0352', P['join_0352_D1']['pointer'], 'PROGRAM PRODUCT (root-reviewed 0352 join finding D1; retained by root review 60551a33...)'),
                                text=P['join_0352_D1']['finding'], HI_rows_with_upper_limit_marker_in_stored_labels=P['join_0352_HI_rows_with_upper_limit_marker']),
                           rn([175], 'raw HI limits have blank density and #.# in the error slot.'),
                           rn([47], 'HI and stellar densities are populated throughout.')],
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'The HI attachment of Note (3) is a column-level statement. No NGC 3198 HI row carries the marker in the stored labels '
                                '(root-retained D1), and the secondary note says NGC 3198 HI is populated throughout while HI limits would be blank '
                                'densities. Both readings of UR-4/U9/STARS_ROW2 therefore agree that no query receives an HI upper-limit attachment.'},
     'status': 'RESOLVED_DOCUMENTARY',
     'physically_open': 'none from this item; HI uncertainty remains the published per-ring rms field as stored (no likelihood implied)'},
    {'id': 'UR-4/U10/STARS_ERROR_ZERO',
     'binds': {'UR': ['UR-4'], 'U': ['U10'], 'OPEN': ['OPEN-8', 'OPEN-9'], 'queries_via_bracketing_row': ['NGC3198-Q26', 'NGC3198-Q27', 'NGC3198-Q28'],
               'rows': [16, 18, 19, 20]},
     'question': 'meaning of the literal e_Sigma* = 0.0: explicit documented zero error, or absent/unspecified uncertainty',
     'source_statements': [lr(176, '50- 54  F5.1 Msun/pc2         e_Sigma*   rms uncertainty in Sigma* (3)'),
                           lr(186, 'Note (3): 1.0 = upper limit.'),
                           lr(173, '30- 35  F6.2 Msun/pc2           SigmaH2  ? Surface density of H2 (2)'),
                           lr(196, 'follows the rules of the Standard Description for Astronomical Catalogues;'),
                           dict(ptr('join_0352', '/per_query/*/S1/rows (row_index 16, 18, 20, stars)', 'PROGRAM PRODUCT (bundle labels carried by the root-reviewed 0352 join)'),
                                stored_labels={k: LB[k] for k in ('row_16_stars', 'row_18_stars', 'row_20_stars')},
                                note='row 19 brackets no query (0352 issue_to_query_summary U10); its label is carried by 0352 item_classification U10'),
                           dict(ptr('bundle_contract_v006', 'line 140', 'PROGRAM ADAPTER VOCABULARY (error_kind label for the literal zero)'), text=BC['140'])],
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'e_Sigma* = 0.0 is an explicit, present literal in a column documented as "rms uncertainty in Sigma*" that carries no '
                                '"?" null flag. It is therefore not an absence marker (absence in table7 is a blank in a "?"-flagged column, e.g. '
                                'SigmaH2 line 173) and not the Note-3 marker (Note 3 defines only 1.0). No local primary statement says that the '
                                'stellar rms is zero, below the format quantum, or not computed. Format fact, kept as a hypothesis about the writer: '
                                'F5.1 carries one decimal, so if the producer rounded, only values below 0.05 print as 0.0; if it truncated, values '
                                'below 0.1 print as 0.0. Which rule (if either) applies is not documented (ledger U10 "rounding is a hypothesis").',
                        'classification': 'EXPLICIT_LITERAL_PRESENT_SEMANTICS_UNSPECIFIED: neither a documented zero error nor an absent uncertainty'},
     'status': 'PARTIAL',
     'resolved_part': 'present literal, not a null marker, not the Note-3 marker, documented quantity = rms uncertainty at F5.1',
     'missing_document': leroy_paper_missing,
     'missing_statement': 'how the per-ring rms of Sigma* was computed and rounded, and what a printed 0.0 denotes',
     'physically_open': 'size of the stellar rms on rows 16, 18, 19, 20; no replacement error, lower bound or likelihood is implied'},
    {'id': 'UR-4/U11/H2_BLANK',
     'binds': {'UR': ['UR-4'], 'U': ['U11'], 'OPEN': ['OPEN-4', 'OPEN-9'], 'rows': list(range(10, 23))},
     'question': 'documentary meaning of blank H2 rows (UR-4 lists U11 among the bracketing-row items)',
     'source_statements': [lr(173, '30- 35  F6.2 Msun/pc2           SigmaH2  ? Surface density of H2 (2)'),
                           lr(174, '37- 40  F4.1 Msun/pc2         e_SigmaH2  ? RMS uncertainty in SigmaH2'),
                           lr(196, 'follows the rules of the Standard Description for Astronomical Catalogues;'),
                           rn([175, 176, 177, 178], 'Blank/blank H# still needs contextual treatment; the printed NGC ### H# upper limits become '
                              'blank/blank in the electronic file, while galaxies without CO also have blank/blank. Do not invent a universal zero '
                              'or limit from that encoding.'),
                           dict(ptr('p53_freeze', '/choices/H2_missing_support', 'PROGRAM FREEZE RECORD'), quoted_with_every_digit_masked=FZ['/choices/H2_missing_support']),
                           dict(ptr('crosswalk_0341', '/sources/S1_LEROY_T7/tracers/H2', 'REVIEWED 0341 EXTRACT (reused)'), text='HERACLES CO (ReadMe abstract; table2 survey field)')],
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'Blank H2 is a CDS null ("?" on both SigmaH2 and e_SigmaH2), so "absent, not zero" (ledger U11) is documentarily '
                                'correct; e_SigmaH2 carries no Note 3, so no limit marker is defined for H2. The ReadMe does not say why a field is '
                                'null. The secondary note reports, for its single NGC 628 example, that printed H2 upper limits became blank/blank in '
                                'the electronic file, and states that galaxies without CO are also blank/blank; on that report a blank cannot be '
                                'told apart from no measurement. Whether the same holds for NGC 3198 is not stated locally.'},
     'status': 'PARTIAL',
     'resolved_part': 'blank = CDS null; no H2 limit marker defined in the ReadMe',
     'missing_document': leroy_paper_missing,
     'missing_statement': 'whether the printed Table 7 gives H2 upper limits for NGC 3198 rings beyond the last populated H2 ring',
     'physically_open': 'H2 surface density on rows 10-22: absent; no zero, bound or likelihood'},
    {'id': 'UR-5/U14/SFB_COMMENTED_ROWS_AND_KILL',
     'binds': {'UR': ['UR-5'], 'U': ['U14', 'U15'], 'OPEN': ['OPEN-3'], 'root_review_notes': ['N3'],
               'queries': ['NGC3198-Q%02d' % q for q in range(32, 44)]},
     'question': 'published or file-format meaning of the two commented .sfb rows (and of kill/error)',
     'source_statements': [
         dict(ptr('sfb', 'PROBE_EVIDENCE /sfb_structure', 'SAVED SOURCE PRODUCT (structure only; no data literal read out)'),
              observed={'line_1': S['line_1_text'] + ' (uncommented header)', 'uncommented_rows': 'lines 2-67 (66 rows, 4 tokens each)',
                        'commented_rows': 'lines 68-69, the last two lines of the file; "#" attached to the first token; 4 tokens each',
                        'radius_tokens_of_commented_rows': 'equal to the texts stored at crosswalk_0341 /sources/S3_SPARC_SFB/radial_coordinate (boolean in PROBE_EVIDENCE; values not reproduced)',
                        'kill_token_of_commented_rows': 'the flag literal one on both rows; crosswalk_0341 /sources/S3_SPARC_SFB/masks states the same kill value on every row'}),
         dict(ptr('sparc_index', 'line 55', 'PRIMARY (distributor index page)'), text=IDX['55'],
              note='the only local description of the photometric-profile files; the page mentions none of "kill", "comment", ".sfb" or "#" '
                   '(its only "error" occurrence, line %s, is about line fitting, not these files)' % ', '.join(str(x) for x in P['sparc_index_error_word_lines'])),
         dict(ptr('sparc_index', 'line 64', 'PRIMARY (distributor index page)'), text=IDX['64']),
         dict(ptr('sfb_zip', 'archive members', 'SAVED SOURCE PRODUCT'), observed='no documentation member (%d members, all .sfb); NGC3198.sfb byte-identical to the local file' % ZS['members']),
         dict(ptr('sparc_cds_readme', 'whole text (absence check)', 'PRIMARY (SPARC CDS ReadMe, identified in 0344/0349; consulted for absence only)'),
              observed=P['sparc_cds_readme_mentions'])],
     'observed_format_pattern': {'marked': 'OBSERVED across the distributor zip (aggregate, no data literal); not a meaning',
                                 'files': ZS['members'], 'files_with_commented_rows': ZS['files_with_commented_rows_beyond_line_1'],
                                 'commented_rows': ZS['commented_rows_beyond_line_1'], 'all_commented_rows_data_shaped': ZS['commented_rows_data_shaped_4_numeric_tokens'] == ZS['commented_rows_beyond_line_1'],
                                 'files_commented_rows_after_last_uncommented_row': ZS['files_commented_rows_all_after_last_uncommented_row'],
                                 'files_commented_rows_interleaved': ZS['files_commented_rows_interleaved'],
                                 'files_with_canonical_header_line': ZS['first_line_equals_canonical_header']},
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': '"#" excludes the two rows from the file\'s uncommented profile; no local document states why (for example unreliable '
                                'photometry, a sky or noise limit, or the end of the fitted region) or whether the distributor counts them as observed '
                                'support. Commented rows are interleaved in two other distributor files, so a universal "outer truncation" reading is '
                                'not supported by the format alone. kill is the same flag on commented and uncommented rows, so kill does not separate '
                                'them; kill and error semantics remain undocumented in the local documents read (U14).'},
     'status': 'UNRESOLVED_MISSING_DOCUMENT',
     'missing_document': [sparc_paper_missing, archangel_missing],
     'missing_statement': 'the SPARC/Archangel definition of commented rows in the .sfb profiles, and of the kill and error columns',
     'physically_open': 'whether the two commented rows (the last two lines of the .sfb file) are observed stellar support (UR-5 named choice); the '
                        'queries affected need an arcsec-to-kpc conversion at the program reference distance (crosswalk_0341 '
                        '/query_domain/reference_distance; 0346 C4, SECONDARY), not performed'},
    {'id': 'UR-5/U15/S3_S4_OBSERVED_SUPPORT',
     'binds': {'UR': ['UR-5'], 'U': ['U15'], 'OPEN': ['OPEN-3'], 'root_review_notes': ['N3'], 'queries': ['NGC3198-Q%02d' % q for q in range(32, 44)]},
     'question': 'observed support of the stored S3 (.sfb) and S4 (.dens) products',
     'source_statements': [
         dict(ptr('dens', 'line 1', 'SAVED SOURCE PRODUCT (header only)'), text=D['line_1_text'],
              observed='77 uncommented rows; NGC3198.dens byte-identical to the distributor zip member'),
         dict(ptr('sparc_index', 'line 56', 'PRIMARY (distributor index page)'), text=IDX['56']),
         dict(ptr('crosswalk_0341', D['crosswalk_pointer'], 'REVIEWED 0341 EXTRACT (reused; quote replaced by pointer, radius values not reproduced)'),
              row_counts_as_stated={'total': D['crosswalk_row_counts_in_order'][0], 'equal_to_uncommented_sfb_radii_at_reference_distance': D['crosswalk_row_counts_in_order'][1],
                                    'without_sfb_counterpart': D['crosswalk_row_counts_in_order'][2]}),
         dict(ptr('crosswalk_0341', S['crosswalk_pointer'], 'REVIEWED 0341 EXTRACT (reused; quote replaced by pointer, radius values not reproduced)'),
              row_counts_as_stated={'uncommented': S['n_uncommented_data_rows'], 'commented': S['n_commented_rows']})],
     'interpretation': {'marked': 'INTERPRETATION (counting only; no conversion)',
                        'text': 'The 66 uncommented .sfb rows account for 66 .dens rows. The 2 commented .sfb rows could account for at most 2 of the '
                                'other 11, so at least 9 of the 11 outer .dens rows have no .sfb row of any kind, whatever is decided for the '
                                'commented rows. The index statement on extrapolation is generic; no local statement says that the NGC 3198 outer '
                                '.dens rows are extrapolated, so U15 stays an INFERENCE. S3/S4 grids remain outside the stored bundle/coverage '
                                '(0352: no per-query join; N3).'},
     'status': 'PARTIAL',
     'resolved_part': 'stored support facts (header, row counts, commented-row positions) and the counting bound',
     'missing_document': [sparc_paper_missing],
     'missing_statement': 'a galaxy-specific statement of which .dens radii are extrapolated',
     'physically_open': 'which of Q32-Q43 lie beyond observed stellar support (depends on the UR-5 choice and a C4-bound conversion); extrapolated versus observed outer stellar profile'},
]

addendum = {
    'schema': 'CLAUDE2_0356_SOURCE_SEMANTICS_ADDENDUM_V002',
    'task': '0356 V002 (author: CLAUDE2 helper 0356-A; V001 retained unchanged; provenance check of V001 by a distinct helper: PASS_WITH_NOTES F1-F7, addressed here)',
    'status': 'DOCUMENTARY ADDENDUM, metadata only. No interpolation, extrapolation, mask threshold, uncertainty distribution, galaxy state, '
              'response law, calibration, query-mapping rule or source choice is made.',
    'status_vocabulary': ['RESOLVED_DOCUMENTARY', 'PARTIAL', 'UNRESOLVED_MISSING_DOCUMENT'],
    'literal_policy': {'rule': 'no data value (density, error, radius, distance, velocity, photometry) is reproduced; values are referenced by pointer',
                       'allowed_decimal_classes': [c for c, _ in ALLOWED], 'scan': 'build_addendum_0356_v002.py scan (run on every V002 deliverable)'},
    'binding_inputs': {
        'root_review_0352': dict(pin('root_review_0352'), retained_notes=P['root_review_0352_retained_notes'],
                                 effect='N1, N2, N3, D2, D3 unchanged; D1 re-grounded on ReadMe lines 171-172 and 175-176'),
        'correction_0346': dict(pin('correction_0346'), effect='preserved unchanged; its line_number_note (e_SigmaHI 172, e_Sigma* 176, Note 2 185, '
                                                               'Note 3 186) is reproduced by the same line method; C4 binds any arcsec-to-kpc step in UR-5'),
        'crosswalk_0341': pin('crosswalk_0341'), 'ledger_0341': pin('ledger_0341'), 'join_0352': pin('join_0352')},
    'evidence': {'probe_evidence': {'file': PE.split('/')[-1], 'sha256': sha(pe_b)},
                 'probe_script': {'file': PS.split('/')[-1], 'sha256': sha(open(PS, 'rb').read())},
                 'leroy_readme_copies_byte_identical': True,
                 'name_only_search': 'PROBE_EVIDENCE /name_only_search (roots, patterns, matches; forbidden names counted, not listed)'},
    'items': items,
    'summary': {it['id']: it['status'] for it in items},
    'remaining_named_choices_not_made': [
        'OPEN-9: S1 query-mapping/representation rule (UR-4 query-level consequence)',
        'UR-5: whether commented .sfb rows count as observed stellar support',
        'arcsec-to-kpc conversion at the program reference distance for the commented radii (0346 C4, SECONDARY)'],
    'qualifications_of_prior_wording': [
        {'id': 'Q1', 'where': 'crosswalk_0341 /sources/S1_LEROY_T7/error_fields/e_SigmaHI (format text %s)' % CW['/sources/S1_LEROY_T7/error_fields/e_SigmaHI format text'],
         'source': lr(172, '26- 28  F3.1 Msun/pc2         e_SigmaHI  rms uncertainty in SigmaHI (3)'),
         'qualification': 'the documented format of e_SigmaHI is F3.1 (bytes 26-28); F5.1 is the format of e_Sigma* (line 176). No value or attachment changes.'},
        {'id': 'Q2', 'where': 'ledger_0341 U14 and crosswalk_0341 /sources/S3_SPARC_SFB/{masks,error_fields} ("not documented locally"); the ledger absence scope includes joint_parent_continuation/',
         'checks': {'ledger_U14_phrase_present': LG['U14 evidence contains "not documented locally"'],
                    'crosswalk_S3_error_fields_phrase_present': CW['/sources/S3_SPARC_SFB/error_fields contains "not documented locally"'],
                    'crosswalk_S3_masks_phrase_present': CW['/sources/S3_SPARC_SFB/masks contains "not documented locally"']},
         'qualification': 'a candidate SPARC master-paper PDF exists in that searched path and was opened by none of 0341, 0346 or 0356; the absence '
                          'claim should read "not documented in the local documents read".', 'candidate_local_copy': pdf_ref},
        {'id': 'Q3', 'where': 'ledger_0341 U9 ("primary Appendix E not local")', 'checks': {'phrase_present': LG['U9 evidence contains "primary Appendix E not local"']},
         'qualification': 'confirmed by the probe name-only search; the secondary note GALAXY_INPUT_READINESS.md lines 170-179 reports the Appendix E '
                          'printed example and contradicts the literal Note-3 reading for NGC 3198 stars row 2; the P53 freeze records '
                          'SEMANTIC_CONFLICT_PENDING_DISTINCT_REVIEW. The ledger state QUARANTINED stands.'},
        {'id': 'Q4', 'where': 'crosswalk_0341 /sources/S1_LEROY_T7/error_fields/e_Sigma* ("not zero uncertainty")',
         'checks': {'phrase_present': CW['/sources/S1_LEROY_T7/error_fields/e_Sigma* contains "not zero uncertainty"']},
         'qualification': 'no local source states that the literal 0.0 is, or is not, a zero uncertainty; "not zero uncertainty" should read "meaning '
                          'unspecified (neither a documented zero uncertainty nor an absence)". The carry rule "no replacement" is unchanged.'}],
    'not_consulted': [
        'Leroy table7/table4/table2 data rows (labels reused from the root-reviewed 0352 join instead)',
        'P53 parsed-input program review (ROOT_COMPLETE_PARSED_INPUT_REVIEW_V002/REVIEW.json, named in the P53 freeze): not in the 0341/0346 set; a program review, not a primary source',
        'the candidate SPARC paper PDF (hash only; content unverified)',
        'any velocity, rotation, rotmod, MassModels, Newton, FIELD_, RESPONSE, ROTATION, FIT, TRIAL or MOM1 file; S2 products'],
    'exposure_incidents': [
        'E1 (V001 discovery, unchanged): a keyword search displayed GALAXY_INPUT_READINESS.md lines 172-174 unmasked; they contain one NGC 3198 stellar '
        'surface-density literal with its rms literal at the row-2 radius and NGC 628 example literals. Not used beyond the masked text; not reproduced.',
        'E2 (V001 discovery, unchanged): during a census of the distributor zips one non-target .sfb file without a header line had its first data row '
        'printed, and the first-line header comments of two non-target .dens files were printed; no galaxy name was printed. Not used; not reproduced.',
        'V002 work: no new exposure; the V002 probe emits counts, booleans, pointers, masked text and flag literals only.'],
}
text = json.dumps(addendum, indent=1, ensure_ascii=False)
scans = [literal_scan(OUT.split('/')[-1], text)] + scan_files([PE, PS, __file__] + OTHERS)
if not all(r['pass'] for r in scans):
    print(json.dumps({'ok': False, 'literal_scan': scans}, indent=1))
    raise SystemExit('E_LITERAL_SCAN')
with open(OUT, 'x', encoding='utf-8') as f:
    f.write(text)
print(json.dumps({'ok': True, 'output': OUT, 'items': len(items), 'summary': addendum['summary'],
                  'literal_scan': {r['file']: r['allowed_class_counts'] for r in scans}}, indent=1))
