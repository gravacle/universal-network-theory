"""0356 addendum builder (CLAUDE2 helper 0356-A). Composes SOURCE_SEMANTICS_ADDENDUM_0356_V001.json from the probe evidence
(source_semantics_probe_0356_v001.py output) plus separately marked interpretation text. Re-verifies the probe evidence pin and
asserts every quoted source line against the probe evidence, so no source statement here is typed by hand without a check.
Usage: python3 -I -B build_addendum_0356_v001.py <probe_evidence.json> <probe_script.py> <new_addendum.json>
"""
import hashlib, json, sys

PE, PS, OUT = sys.argv[1:4]
pe_b = open(PE, 'rb').read()
P = json.loads(pe_b)
sha = lambda b: hashlib.sha256(b).hexdigest()
L = P['leroy_readme_lines']
R = P['readiness_note_lines_digits_masked']
pin = lambda k: {'path': P['pins_verified'][k]['path'], 'sha256': P['pins_verified'][k]['sha256']}


def lr(n, expect):
    assert L[str(n)].strip() == expect, (n, L[str(n)])
    return {'path': pin('leroy_readme')['path'], 'sha256': pin('leroy_readme')['sha256'], 'line': n, 'text': expect,
            'line_method': P['line_method_html']}


def rn(lines, masked_fragment):
    for n in lines:
        assert str(n) in R
    joined = ' '.join(R[str(n)] for n in lines)
    assert masked_fragment in joined, masked_fragment
    return {'path': pin('readiness_note')['path'], 'sha256': pin('readiness_note')['sha256'], 'lines': '%d-%d' % (lines[0], lines[-1]),
            'class': 'SECONDARY local note (cites Leroy et al. 2008 Appendix E, arXiv:0810.2556, not local)',
            'quoted_with_every_digit_masked': masked_fragment}


S = P['sfb_structure']
assert S['n_uncommented_data_rows'] == 66 and S['commented_lines'] == [68, 69] and S['commented_rows_after_last_uncommented_row']
assert S['commented_radius_tokens_equal_0341_texts_#352.17_#387.39'] and S['commented_kill_tokens_equal_1'] == [True, True]
assert S['last_uncommented_radius_token_equals_0341_text_320.16'] and S['line_1_is_commented'] is False
D = P['dens_structure']
assert D['commented_lines'] == [1] and D['n_uncommented_rows'] == 77
ZS = P['zips']['sfb_zip']['aggregate_census']
LB = P['join_0352_stored_labels']
assert LB['2/stars']['upper_limit_marker'] is True and LB['2/stars']['value_missing'] is False
assert all(LB[k]['error_kind'] == 'LITERAL_ZERO_MEANING_UNRESOLVED' for k in ('16/stars', '18/stars', '20/stars'))
assert P['join_0352_HI_rows_with_upper_limit_marker'] == []
IDX = P['sparc_index_lines']
PDF = P['sparc_paper_pdf_present_unread']
assert PDF['content_read'] is False and PDF['sidecar_sha256_matches']
assert all(P['leroy_readme_copies_identical'].values())
FZ = P['p53_freeze_digits_masked']
assert 'SEMANTIC_CONFLICT_PENDING_DISTINCT_REVIEW' in FZ['/choices/error_and_censoring'] and '"Gaussian_likelihood": null' in FZ['/choices/error_and_censoring']
assert 'MISSING_NOT_ZERO' in FZ['/choices/H2_missing_support']
BC = P['bundle_contract_v006_lines']

leroy_paper_missing = ('Leroy et al. 2008, AJ 136, 2782 (arXiv:0810.2556): Appendix E (radial-profile conventions) and the printed Table 7 '
                       'example. No local copy within the 0341 searched paths (name-only check for *leroy*, *0810.2556*, *appendix*, *.pdf); '
                       'the only local Leroy documentation is the CDS ReadMe (four byte-identical copies, sha256 cbd9a431...).')
sparc_paper_missing = ('Lelli, McGaugh & Schombert 2016, AJ 152, 157 (SPARC master paper), description of the 3.6-micron surface-brightness '
                       'profile files (.sfb columns kill/error and commented rows) and of the bulge-disk decompositions (.dens). A local copy '
                       'EXISTS but is outside the 0341/0346 document set and was NOT read: %s (sha256 %s, %d bytes; sidecar url %s, retrieved %s).'
                       % (PDF['path'], PDF['sha256'], PDF['bytes'], PDF['sidecar_url'], PDF['sidecar_retrieved_utc']))
archangel_missing = ('Archangel photometry-system documentation (Schombert 2007), named by the SPARC index line 64 as the system producing the '
                     'surface-brightness profiles: not found locally (name-only check for *archangel*, *schombert*, *0703646*).')

items = [
    {'id': 'UR-4/U9/COLUMN_NOTE3',
     'binds': {'UR': ['UR-4'], 'U': ['U9'], 'OPEN': ['OPEN-8'], 'root_review_notes': ['D1']},
     'question': 'published meaning of the error literal 1.0 in the Leroy table7 error columns',
     'source_statements': [lr(186, 'Note (3): 1.0 = upper limit.'),
                           lr(172, '26- 28  F3.1 Msun/pc2         e_SigmaHI  rms uncertainty in SigmaHI (3)'),
                           lr(176, '50- 54  F5.1 Msun/pc2         e_Sigma*   rms uncertainty in Sigma* (3)'),
                           lr(174, '37- 40  F4.1 Msun/pc2         e_SigmaH2  ? RMS uncertainty in SigmaH2'),
                           lr(179, '64- 68  F5.1 10-4Msun/yr/kpc2 e_FUV+24   rms uncertainty in FUV+24')],
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'Note (3) is a column-level declaration attached to exactly two error columns, e_SigmaHI and e_Sigma*; it is not '
                                'attached to e_SigmaH2 or e_FUV+24. It declares that the literal 1.0 in those columns denotes "upper limit". The '
                                'ReadMe does not state which quantity is limited (the same-row surface density or the uncertainty), the value or '
                                'significance of any limit, or whether every literal 1.0 in those columns is a marker.'},
     'status': 'RESOLVED_DOCUMENTARY',
     'scope_of_resolution': 'what the local primary documentation (CDS ReadMe) states; its applicability to populated rows is item UR-4/U9/STARS_ROW2',
     'physically_open': 'no limit value, significance or likelihood is stated'},
    {'id': 'UR-4/U9/STARS_ROW2',
     'binds': {'UR': ['UR-4'], 'U': ['U9'], 'OPEN': ['OPEN-8', 'OPEN-9'], 'queries_via_bracketing_row': ['NGC3198-Q04', 'NGC3198-Q05', 'NGC3198-Q06', 'NGC3198-Q07'],
               'root_review_notes': ['D1']},
     'question': 'does the Note-3 marker apply to the only NGC3198 occurrence, stars row 2 (raw table7 line %d), whose Sigma* is populated'
                 % LB['2/stars']['original_line_number'],
     'source_statements': [
         lr(175, '42- 48  F7.1 Msun/pc2           Sigma*   Surface density of stars'),
         lr(171, '20- 24  F5.2 Msun/pc2           SigmaHI  ? Surface density of H I (2)'),
         lr(196, 'follows the rules of the Standard Description for Astronomical Catalogues;'),
         {'path': pin('join_0352')['path'], 'sha256': pin('join_0352')['sha256'], 'pointer': '/per_query/*/S1/rows (row_index 2, stars)',
          'stored_labels': LB['2/stars'], 'class': 'saved program product (bundle labels as carried by the root-reviewed 0352 join)'},
         {'path': pin('bundle_contract_v006')['path'], 'sha256': pin('bundle_contract_v006')['sha256'], 'line': 58, 'text': BC['58'],
          'class': 'program adapter rule (literal application of Note 3)'},
         rn([170, 171, 172, 173, 174, 175], 'The CDS note saying `#.# = upper limit` cannot be applied to every numeric error equal to one. '
            'The original printed example explicitly gives NGC ### at #.# kpc as stellar density ###.# with RMS #.#, and at #.#/#.# kpc as HI '
            '#.#/#.# with RMS #.#. These match the raw bytes. Thus NGC ####\'s populated stellar density ###.# and RMS #.# at #.# kpc is not a '
            'limit flag. In contrast, raw HI limits have blank density and #.# in the error slot.'),
         {'path': pin('p53_freeze')['path'], 'sha256': pin('p53_freeze')['sha256'], 'pointer': '/choices/error_and_censoring',
          'quoted_with_every_digit_masked': FZ['/choices/error_and_censoring'], 'class': 'program freeze record'}],
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'Two local readings conflict for this row. (a) Literal CDS reading: Note (3) applies to every 1.0 in e_Sigma*, so stars '
                                'row 2 carries an upper-limit marker (P53 label UPPER_LIMIT_NOTE3; bundle upper_limit_marker true; value present). '
                                '(b) The secondary note reports that the primary paper\'s printed example (Appendix E) lists populated values with '
                                'RMS 1.0, concludes that NGC 3198\'s populated stellar row with RMS 1.0 "is not a limit flag", and says HI limits are '
                                'encoded as a blank density with 1.0 in the error slot. Schema fact relevant to both: only SigmaHI is nullable ("?", '
                                'line 171); Sigma* has no "?" (line 175), so the blank-density encoding described in (b) cannot occur in the stellar '
                                'column, and the ReadMe gives no other encoding for a stellar limit. The P53 freeze already records this as '
                                'SEMANTIC_CONFLICT_PENDING_DISTINCT_REVIEW with Gaussian_likelihood null. Neither reading is adopted here.'},
     'status': 'UNRESOLVED_MISSING_DOCUMENT',
     'missing_document': leroy_paper_missing,
     'missing_statement': 'whether a populated Sigma* with e_Sigma* = 1.0 in the electronic table7 is an upper limit or a measured value with rms 1.0',
     'physically_open': 'whether stars row 2 is a measurement or a limit; no bound value, significance, measurement error or likelihood is stated by any local source'},
    {'id': 'UR-4/D1/HI_COLUMN_NOTE',
     'binds': {'UR': ['UR-4'], 'U': ['U9'], 'OPEN': ['OPEN-8'], 'root_review_notes': ['D1']},
     'question': 'stars row-2 marker versus the HI column note',
     'source_statements': [lr(171, '20- 24  F5.2 Msun/pc2           SigmaHI  ? Surface density of H I (2)'),
                           lr(172, '26- 28  F3.1 Msun/pc2         e_SigmaHI  rms uncertainty in SigmaHI (3)'),
                           {'path': pin('join_0352')['path'], 'sha256': pin('join_0352')['sha256'], 'pointer': '/disagreements/0',
                            'text': P['join_0352_D1'], 'HI_rows_with_upper_limit_marker_in_stored_labels': P['join_0352_HI_rows_with_upper_limit_marker']},
                           rn([175], 'raw HI limits have blank density and #.# in the error slot.'),
                           rn([47], 'HI and stellar densities are populated throughout.')],
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'The HI attachment of Note (3) is a column-level statement. No NGC3198 HI row carries the marker in the stored labels '
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
                           {'path': pin('join_0352')['path'], 'sha256': pin('join_0352')['sha256'], 'pointer': '/per_query/*/S1/rows (row_index 16, 18, 20, stars)',
                            'stored_labels': {k: LB[k] for k in ('16/stars', '18/stars', '20/stars')},
                            'note': 'row 19 brackets no query (0352 issue_to_query_summary U10); its label is carried by 0352 item_classification U10'},
                           {'path': pin('bundle_contract_v006')['path'], 'sha256': pin('bundle_contract_v006')['sha256'], 'line': 140, 'text': BC['140']}],
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'e_Sigma* = 0.0 is an explicit, present literal in a column documented as "rms uncertainty in Sigma*" that carries no '
                                '"?" null flag. It is therefore not an absence marker (absence in table7 is a blank in a "?"-flagged column, e.g. '
                                'SigmaH2 line 173) and not the Note-3 marker (Note 3 defines only 1.0). No local primary statement says that the '
                                'stellar rms is zero, below the format quantum, or not computed. Format fact: F5.1 carries one decimal, so a stored '
                                '0.0 is what any rms rounded (or truncated) to one decimal below 0.1 would print as; the producer\'s rounding rule is '
                                'not documented, so "rounding" stays a hypothesis (ledger U10).',
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
                           {'path': pin('p53_freeze')['path'], 'sha256': pin('p53_freeze')['sha256'], 'pointer': '/choices/H2_missing_support',
                            'quoted_with_every_digit_masked': FZ['/choices/H2_missing_support']},
                           {'path': pin('crosswalk_0341')['path'], 'sha256': pin('crosswalk_0341')['sha256'], 'pointer': '/sources/S1_LEROY_T7/tracers/H2',
                            'text': 'HERACLES CO (ReadMe abstract; table2 survey field)', 'class': 'reviewed 0341 extract (reused)'}],
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'Blank H2 is a CDS null ("?" on both SigmaH2 and e_SigmaH2), so "absent, not zero" (ledger U11) is documentarily '
                                'correct; e_SigmaH2 carries no Note 3, so no limit marker is defined for H2. The ReadMe does not say why a field is '
                                'null. The secondary note reports that printed H2 upper limits became blank in the electronic file, and that galaxies '
                                'without CO are also blank, so a blank does not distinguish a printed limit from no measurement.'},
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
         {'path': pin('sfb')['path'], 'sha256': pin('sfb')['sha256'], 'class': 'saved source product (structure only; no data literal read out)',
          'observed': {'line_1': S['line_1_text'] + ' (uncommented header)', 'uncommented_rows': 'lines 2-67 (66 rows, 4 tokens each)',
                       'commented_rows': 'lines 68-69, "#" attached to the first token, 4 tokens each, after the last uncommented row',
                       'commented_radius_tokens': '#352.17, #387.39 (equal to the texts published in 0341/0352)',
                       'kill_token_on_commented_rows': '1, 1', 'last_uncommented_radius_token': '320.16 (equal to 0341)'}},
         {'path': pin('sparc_index')['path'], 'sha256': pin('sparc_index')['sha256'], 'line': 55, 'text': IDX['55'],
          'note': 'the only local description of the photometric-profile files; the page mentions none of "kill", "comment", ".sfb" or "#" '
                  '(its one "error" occurrence is not about these files)'},
         {'path': pin('sparc_index')['path'], 'sha256': pin('sparc_index')['sha256'], 'line': 64, 'text': IDX['64']},
         {'path': pin('sfb_zip')['path'], 'sha256': pin('sfb_zip')['sha256'], 'observed': 'no documentation member (%d members, all .sfb); NGC3198.sfb byte-identical to the local file' % ZS['members']},
         {'path': pin('sparc_cds_readme')['path'], 'sha256': pin('sparc_cds_readme')['sha256'], 'observed': P['sparc_cds_readme_mentions'],
          'class': 'SPARC CDS ReadMe (identified in 0344/0349, consulted here for absence only): describes table1, table2, refs; no .sfb'}],
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
                                'not supported by the format alone. kill is 1 on commented and uncommented rows alike, so kill does not separate '
                                'them; kill and error semantics remain undocumented locally (U14).'},
     'status': 'UNRESOLVED_MISSING_DOCUMENT',
     'missing_document': [sparc_paper_missing, archangel_missing],
     'missing_statement': 'the SPARC/Archangel definition of commented rows in the .sfb profiles, and of the kill and error columns',
     'physically_open': 'whether the rows at 352.17 and 387.39 arcsec are observed stellar support (UR-5 named choice); queries affected need an '
                        'arcsec-to-kpc conversion at the 13.8 Mpc convention (0346 C4, SECONDARY), not performed'},
    {'id': 'UR-5/U15/S3_S4_OBSERVED_SUPPORT',
     'binds': {'UR': ['UR-5'], 'U': ['U15'], 'OPEN': ['OPEN-3'], 'root_review_notes': ['N3'], 'queries': ['NGC3198-Q%02d' % q for q in range(32, 44)]},
     'question': 'observed support of the stored S3 (.sfb) and S4 (.dens) products',
     'source_statements': [
         {'path': pin('dens')['path'], 'sha256': pin('dens')['sha256'], 'line': 1, 'text': D['line_1_text'],
          'observed': '77 uncommented rows; NGC3198.dens byte-identical to the distributor zip member'},
         {'path': pin('sparc_index')['path'], 'sha256': pin('sparc_index')['sha256'], 'line': 56, 'text': IDX['56']},
         {'path': pin('crosswalk_0341')['path'], 'sha256': pin('crosswalk_0341')['sha256'], 'pointer': '/sources/S4_SPARC_DENS/radial_coordinate',
          'text': '77 rows 0.0435-42.8435 kpc; 66 rows equal .sfb radii x 13.8 Mpc (relative 5e-5); 11 rows 23.37-42.84 kpc have no .sfb counterpart',
          'class': 'reviewed 0341 extract (reused)'},
         {'path': pin('crosswalk_0341')['path'], 'sha256': pin('crosswalk_0341')['sha256'], 'pointer': '/sources/S3_SPARC_SFB/radial_coordinate',
          'text': 'arcsec on sky; 66 rows 0.65-320.16 arcsec (0.0435-21.42 kpc at 13.8 Mpc); 2 commented rows at 352.17 and 387.39 arcsec',
          'class': 'reviewed 0341 extract (reused)'}],
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
    'schema': 'CLAUDE2_0356_SOURCE_SEMANTICS_ADDENDUM_V001',
    'task': '0356 (author: CLAUDE2 helper 0356-A; provenance check by a distinct helper)',
    'status': 'DOCUMENTARY ADDENDUM, metadata only. No interpolation, extrapolation, mask threshold, uncertainty distribution, galaxy state, '
              'response law, calibration, query-mapping rule or source choice is made.',
    'status_vocabulary': ['RESOLVED_DOCUMENTARY', 'PARTIAL', 'UNRESOLVED_MISSING_DOCUMENT'],
    'binding_inputs': {
        'root_review_0352': dict(pin('root_review_0352'), retained_notes=P['root_review_0352_retained_notes'],
                                 effect='N1, N2, N3, D2, D3 unchanged; D1 re-grounded on ReadMe lines 171-172 and 175-176'),
        'correction_0346': dict(pin('correction_0346'), effect='preserved unchanged; its line_number_note (e_SigmaHI 172, e_Sigma* 176, Note 2 185, '
                                                               'Note 3 186) is reproduced by the same line method; C4 binds any arcsec-to-kpc step in UR-5'),
        'crosswalk_0341': pin('crosswalk_0341'), 'ledger_0341': pin('ledger_0341'), 'join_0352': pin('join_0352')},
    'evidence': {'probe_evidence': {'file': PE.split('/')[-1], 'sha256': sha(pe_b)},
                 'probe_script': {'file': PS.split('/')[-1], 'sha256': sha(open(PS, 'rb').read())},
                 'leroy_readme_copies_byte_identical': True},
    'items': items,
    'summary': {it['id']: it['status'] for it in items},
    'remaining_named_choices_not_made': [
        'OPEN-9: S1 query-mapping/representation rule (UR-4 query-level consequence)',
        'UR-5: whether commented .sfb rows count as observed stellar support',
        'arcsec-to-kpc conversion at 13.8 Mpc for the commented radii (0346 C4, SECONDARY)'],
    'qualifications_of_prior_wording': [
        {'id': 'Q1', 'where': 'crosswalk_0341 /sources/S1_LEROY_T7/error_fields/e_SigmaHI ("per-ring rms, F5.1")',
         'source': lr(172, '26- 28  F3.1 Msun/pc2         e_SigmaHI  rms uncertainty in SigmaHI (3)'),
         'qualification': 'the documented format of e_SigmaHI is F3.1 (bytes 26-28); F5.1 is the format of e_Sigma* (line 176). No value or attachment changes.'},
        {'id': 'Q2', 'where': 'ledger_0341 U14 ("unit/meaning not documented locally") and crosswalk S3 masks/error_fields; absence scope includes joint_parent_continuation/',
         'qualification': 'a local SPARC master-paper PDF exists in that searched path and was read by none of 0341, 0346 or 0356; the absence claim '
                          'should read "not documented in the local documents read". ' + sparc_paper_missing},
        {'id': 'Q3', 'where': 'ledger_0341 U9 ("primary Appendix E not local")',
         'qualification': 'confirmed by a name-only check; the secondary note GALAXY_INPUT_READINESS.md lines 170-179 reports the Appendix E printed '
                          'example and contradicts the literal Note-3 reading for NGC 3198 stars row 2; the P53 freeze records '
                          'SEMANTIC_CONFLICT_PENDING_DISTINCT_REVIEW. The ledger state QUARANTINED stands.'}],
    'not_consulted': [
        'Leroy table7/table4/table2 data rows (labels reused from the root-reviewed 0352 join instead)',
        'P53 parsed-input program review (ROOT_COMPLETE_PARSED_INPUT_REVIEW_V002/REVIEW.json, named in the P53 freeze): not in the 0341/0346 set; a program review, not a primary source',
        'the local SPARC paper PDF (hash only)',
        'any velocity, rotation, rotmod, MassModels, Newton, FIELD_, RESPONSE, ROTATION, FIT, TRIAL or MOM1 file; S2 products'],
    'exposure_incidents': [
        'E1: during discovery a keyword search displayed GALAXY_INPUT_READINESS.md lines 172-174 unmasked; they contain one NGC 3198 stellar '
        'surface-density literal with its rms literal at the row-2 radius and NGC 628 example literals. Not used beyond the masked text; not reproduced here.',
        'E2: during a census of the distributor zips one non-target .sfb file without a header line had its first data row printed, and the first-line '
        'header comments of two non-target .dens files (luminosity, distance) were printed; no galaxy name was printed. Not used; not reproduced. The '
        'delivered probe emits counts only.'],
}
with open(OUT, 'x') as f:
    json.dump(addendum, f, indent=1, ensure_ascii=False)
print(json.dumps({'ok': True, 'output': OUT, 'items': len(items), 'summary': addendum['summary']}))
