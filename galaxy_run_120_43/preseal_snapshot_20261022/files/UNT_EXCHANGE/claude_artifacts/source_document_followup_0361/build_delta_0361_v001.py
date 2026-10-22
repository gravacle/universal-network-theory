"""0361 delta builder (CLAUDE2 helper 0361-A). Composes SOURCE_DOCUMENT_DELTA_0361_V001.json from the evidence JSON; every quote is
taken from the evidence (asserted found on its stated page), so no source wording is typed twice.
Usage: python3 -I -B build_delta_0361_v001.py <SOURCE_DOCUMENT_EVIDENCE_0361_V001.json> <evidence_script.py> <new_delta.json>"""
import hashlib, json, sys

EV, ES, OUT = sys.argv[1:4]
eb = open(EV, 'rb').read()
E = json.loads(eb)
sha = lambda b: hashlib.sha256(b).hexdigest()
assert E['all_quotes_found'] and E['sparc_paper']['resolved_from_0356_evidence']['match']
Q = {q['id']: q for q in E['quotes']}
SP = E['sparc_paper']
T = E['whole_paper_term_counts_text_layer']
assert T['kill'] == 0 and T['comment'] == 0 and T['sfb'] == 0 and T['#'] == 0
LS = E['bounded_filename_search']['results']
assert LS['leroy_2008_paper_appendix_E_or_printed_table7']['matches'] == [] and LS['archangel_or_schombert_mcgaugh_2014b']['matches'] == []
B = E['leroy_2008_identifiers_local']
src = {'path': SP['path'], 'sha256': SP['sha256'], 'sidecar_sha256': SP['sidecar']['sha256']}


def cite(i):
    q = Q[i]
    c = dict(src, page=q['page'], section=q['section'], exact_words=q['text'], words=q['words'])
    if 'sentence_subject' in q:
        c['sentence_subject'] = q['sentence_subject']
    if 'text_layer_order' in q:
        c['text_layer_note'] = q['text_layer_order']
    return c


absence = dict(src, scope='text layer of all %d pages (decoded with each font ToUnicode map)' % SP['n_pages'],
               term_counts={k: T[k] for k in ('kill', 'comment', 'sfb', '#')})
archangel_target = {'reference_as_printed': Q['SP-7']['text'], 'page': 14, 'note': 'the SPARC index (0356) says "see Schombert 2007"; the paper cites the 2011 ASCL record',
                    'local_copy': 'none (bounded filename search, pattern archangel_or_schombert_mcgaugh_2014b)'}
procedure_target = {'reference_as_printed': Q['SP-8']['text'], 'page': 14, 'cited_at': cite('SP-2'),
                    'local_copy': 'none (bounded filename search)'}
leroy_target = {'journal': 'The Astronomical Journal', 'volume': 136, 'pages': '2782-2845', 'year': 2008,
                'title': 'The star formation efficiency in nearby galaxies: measuring where gas forms stars effectively',
                'authors': 'Leroy A.K., Walter F., Brinks E., Bigiel F., De Blok W.J.G., Madore B., Thornley M.D.',
                'bibcode': '2008AJ....136.2782L', 'cds_catalogue': 'J/AJ/136/2782', 'arXiv': '0810.2556', 'doi': 'not present in any local document checked',
                'identifier_sources': {'cds_readme': {'path': B['cds_readme']['path'], 'sha256': B['cds_readme']['sha256'], 'lines': '58-64'},
                                       'arXiv_id': {'path': B['secondary_note_arxiv_links']['path'], 'sha256': B['secondary_note_arxiv_links']['sha256'],
                                                    'lines': B['secondary_note_arxiv_links']['lines_with_arxiv_0810_2556'], 'class': 'SECONDARY local note link; also cited by correction 0346 C1'}},
                'local_copy': 'none (bounded filename search under /Users/bgm/Research, pattern leroy_2008_paper_appendix_E_or_printed_table7)',
                'minimal_retrieval_target': 'Leroy et al. 2008 (AJ 136, 2782; arXiv:0810.2556): Appendix E text on the radial-profile conventions and '
                                            'upper limits, plus the printed Table 7 header and notes, enough to decide whether a populated stellar '
                                            'entry with e_Sigma* = 1.0 (NGC 3198 stars row 2) is an upper limit or a measured value with rms 1.0, what '
                                            'a printed e_Sigma* = 0.0 denotes, and whether blank H2 rings are printed limits. No value rows are needed.'}

items = [
    {'id': 'UR-5/U14/COMMENT_MARKER', 'binds': {'UR': ['UR-5'], 'U': ['U14', 'U15'], 'OPEN': ['OPEN-3']},
     'question': 'does the SPARC paper define the "#" commented rows of the distributed .sfb files',
     'status_0356_V002': 'UNRESOLVED_MISSING_DOCUMENT', 'status_0361': 'UNRESOLVED_MISSING_DOCUMENT', 'status_change': 'none',
     'deciding_evidence': [absence, cite('SP-5'), cite('SP-1')],
     'finding': 'The paper does not define the distributor\'s commented rows: the character "#" and the words "comment" and "sfb" do not occur in '
                'its text. Section 3.1 describes the photometry method and states that the profiles are distributed (SP-5), but no file format.',
     'missing_document': [archangel_target, procedure_target],
     'remains_open': 'whether the two commented rows count as observed stellar support (UR-5 choice); no inference from the general photometry method'},
    {'id': 'UR-5/U14/KILL_COLUMN', 'binds': {'UR': ['UR-5'], 'U': ['U14']},
     'question': 'does the SPARC paper define the kill column',
     'status_0356_V002': 'UNRESOLVED_MISSING_DOCUMENT', 'status_0361': 'UNRESOLVED_MISSING_DOCUMENT', 'status_change': 'none',
     'deciding_evidence': [absence],
     'finding': 'The word "kill" does not occur in the paper. The pixel masking described in Section 3.1 is not identified with any distributed column '
                'and is not used here to infer one.',
     'missing_document': [archangel_target, procedure_target],
     'remains_open': 'kill semantics'},
    {'id': 'UR-5/U14/ERROR_COLUMN', 'binds': {'UR': ['UR-5'], 'U': ['U14']},
     'question': 'does the SPARC paper define the error column of the distributed .sfb files',
     'status_0356_V002': 'UNRESOLVED_MISSING_DOCUMENT', 'status_0361': 'UNRESOLVED_MISSING_DOCUMENT', 'status_change': 'none',
     'deciding_evidence': [cite('SP-4'), cite('SP-3'), cite('SP-5')],
     'finding': 'The paper states what dominates the errors of its surface-brightness profiles (SP-4) and how the sky value and its error were estimated '
                '(SP-3). It does not name the distributed error column or give its unit, confidence level or construction, so the column is not '
                'defined by this document. Relating SP-4 to the column would be an inference from the general method and is not made.',
     'missing_document': [archangel_target, procedure_target],
     'remains_open': 'error-column definition and unit; no likelihood or uncertainty distribution is implied'},
    {'id': 'UR-5/U15/OUTER_STELLAR_SUPPORT_POLICY', 'binds': {'UR': ['UR-5'], 'U': ['U15'], 'OPEN': ['OPEN-3'], 'root_review_notes': ['N3']},
     'question': 'published policy for outer stellar surface-brightness support',
     'status_0356_V002': 'PARTIAL', 'status_0361': 'PARTIAL', 'status_change': 'none (evidence strengthened)',
     'deciding_evidence': [cite('SP-6')],
     'finding': 'Primary statement (Section 3.3 Mass Models): the stellar contribution uses the observed [3.6] profile and an exponential-fit '
                'extrapolation, unless the profile shows a clear truncation. This makes the general extrapolation policy PRIMARY-STATED, which '
                'the 0356 SPARC index line stated only generically.',
     'interpretation': {'marked': 'INTERPRETATION (not a source statement)',
                        'text': 'SP-6 is stated for the mass-model stellar contribution; that the distributed .dens rows beyond the uncommented .sfb '
                                'radii are this extrapolation is an interpretation. The paper names no galaxy-specific radii and does not say whether '
                                'NGC 3198 shows a clear truncation, so U15 stays an INFERENCE at row level.'},
     'remains_open': 'which NGC 3198 .dens rows are extrapolated; whether the commented .sfb rows enter the observed profile; the C4-bound conversion (not performed)'},
    {'id': 'UR-4/U9/STARS_ROW2', 'binds': {'UR': ['UR-4'], 'U': ['U9'], 'OPEN': ['OPEN-8'], 'root_review_notes': ['D1']},
     'question': 'e = 1.0 marker conflict for NGC 3198 stars row 2',
     'status_0356_V002': 'UNRESOLVED_MISSING_DOCUMENT', 'status_0361': 'UNRESOLVED_MISSING_DOCUMENT', 'status_change': 'none',
     'deciding_evidence': [{'bounded_filename_search': LS['leroy_2008_paper_appendix_E_or_printed_table7'], 'root': E['bounded_filename_search']['root']}],
     'finding': 'No local copy of Leroy et al. 2008 (paper, Appendix E or printed Table 7) exists under /Users/bgm/Research. The SPARC paper does not '
                'bear on this item.',
     'missing_document': leroy_target,
     'remains_open': 'whether stars row 2 is a limit or a measurement; no bound, significance or likelihood'},
    {'id': 'UR-4/U10/STARS_ERROR_ZERO', 'binds': {'UR': ['UR-4'], 'U': ['U10'], 'OPEN': ['OPEN-8']},
     'status_0356_V002': 'PARTIAL', 'status_0361': 'PARTIAL', 'status_change': 'none',
     'finding': 'No new local primary document. e_Sigma* = 0.0 remains an explicit literal of unspecified meaning; it is not a known zero uncertainty.',
     'missing_document': 'as UR-4/U9/STARS_ROW2', 'remains_open': 'size of the stellar rms on rows 16, 18, 19, 20'},
    {'id': 'UR-4/U11/H2_BLANK', 'binds': {'UR': ['UR-4'], 'U': ['U11'], 'OPEN': ['OPEN-4']},
     'status_0356_V002': 'PARTIAL', 'status_0361': 'PARTIAL', 'status_change': 'none',
     'finding': 'No new local primary document. Blank H2 remains a CDS null: absent, not zero, and not a known limit.',
     'missing_document': 'as UR-4/U9/STARS_ROW2', 'remains_open': 'H2 on rows 10-22'},
    {'id': 'UR-4/U9/COLUMN_NOTE3 and UR-4/D1/HI_COLUMN_NOTE', 'status_0356_V002': 'RESOLVED_DOCUMENTARY', 'status_0361': 'RESOLVED_DOCUMENTARY',
     'status_change': 'none', 'finding': 'unchanged; no new evidence'}]

delta = {'schema': 'CLAUDE2_0361_SOURCE_DOCUMENT_DELTA_V001',
         'task': '0361 (author CLAUDE2 helper 0361-A; provenance check by a distinct helper)',
         'baseline': {'addendum_0356_V002': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/source_semantics_0356/SOURCE_SEMANTICS_ADDENDUM_0356_V002.json',
                                             'sha256': '13ebe908e93d25dd0ec10442cf5fc5a28a0ef6a587815cdb873b929c481b965a'}},
         'status': 'DOCUMENTARY DELTA, metadata only. No likelihood, interpolation, conversion, model, calibration or physical source state is chosen.',
         'sparc_paper': {'path': SP['path'], 'sha256': SP['sha256'], 'bytes': SP['bytes'], 'sidecar': {'path': SP['sidecar']['path'], 'sha256': SP['sidecar']['sha256']},
                         'resolved_from': SP['resolved_from_0356_evidence'], 'n_pages': SP['n_pages'],
                         'pages_rendered_with_Read_tool': [p['page'] for p in SP['pages'] if p['handling'].startswith('rendered')],
                         'pages_not_rendered_reason': {'4': 'Table 1 (numeric table)', '6': 'carries a Table 2 excerpt (numeric table); the one quoted sentence was taken from the decoded text layer',
                                                       '7-13': 'figures including mass models / rotation curves', '1-2, 14': 'not needed (14 = references; read from the text layer for two entries)'}},
         'items': items,
         'summary': {i['id']: {'from': i['status_0356_V002'], 'to': i['status_0361'], 'change': i['status_change']} for i in items},
         'preserved': {'correction_0346': 'unchanged; no conversion touched; C4 still binds any arcsec-to-kpc step',
                       'UR-4_UR-5_distinctions': 'unchanged', 'missingness': 'e_Sigma* = 0.0 is not a known zero; blank H2 is not zero; commented .sfb rows are not adopted as support'},
         'evidence': {'evidence_json': {'file': EV.split('/')[-1], 'sha256': sha(eb)}, 'evidence_script': {'file': ES.split('/')[-1], 'sha256': sha(open(ES, 'rb').read())}},
         'exposures': [
             'X1: page 3 rendered (Read tool): sample-level text incl. the sample range of rotation velocities, the distance error scheme, the Ursa Major '
             'cluster distance and the distances of two non-target galaxies. No target value; nothing reproduced.',
             'X2: page 5 rendered (Read tool): Section 3.2 rotation-curve methodology text (qualitative; source counts; no target value). Nothing reproduced.',
             'X3: during page location, keyword contexts were printed with digits masked and velocity-related contexts suppressed (pages 1-6, 13); a '
             'page-6 content-stream fragment around the quoted sentence (layout coordinates and glyph codes only) and two page-14 reference entries '
             'were printed. No table value.',
             'X4: text layers of all 14 pages (incl. page 4 Table 1, the page 6 Table 2 excerpt and the figure pages) were decoded in memory for quote '
             'assertion and term counts only; no table or figure text was printed.',
             'X5: filename searches printed matching file names only (including unrelated lane block files and git object names that matched a '
             'numeric pattern); custody/sidecar files were grepped for identifier strings and only their file names were printed.']}
with open(OUT, 'x', encoding='utf-8') as f:
    json.dump(delta, f, indent=1, ensure_ascii=False)
print(json.dumps({'ok': True, 'summary': delta['summary']}, indent=1))
