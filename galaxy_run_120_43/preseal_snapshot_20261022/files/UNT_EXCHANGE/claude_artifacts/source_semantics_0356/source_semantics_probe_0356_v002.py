"""0356 source-semantics probe V002 (CLAUDE2 helper 0356-A). Read-only, metadata/documentation only.

Collects the exact source statements used by SOURCE_SEMANTICS_ADDENDUM_0356_V002.json, with sha256 pins and line numbers:
  * Leroy 2008 CDS ReadMe: table7 byte-by-byte lines and notes (0346 line method) and the per-label "?" null-flag map;
  * the secondary note GALAXY_INPUT_READINESS.md: cited lines with EVERY DIGIT MASKED ('#');
  * P53 freeze /choices/error_and_censoring and /choices/H2_missing_support (digits masked);
  * the 0348 bundle contract V006 interpretation-rule lines; the 0352 join's stored labels for the S1 stars targets;
  * the 0341 crosswalk/ledger statements this addendum qualifies, as booleans, states and pointers (no prose with values);
  * SPARC index page lines; .sfb and .dens header/comment STRUCTURE: token counts, line numbers and equality booleans against the
    texts stored in the 0341 crosswalk (the compared texts are parsed at run time and never emitted);
  * an aggregate header/comment-position census over the two distributor zips (no data row, no galaxy name emitted);
  * hash identity of the Leroy ReadMe copies; hash of a local SPARC paper PDF and of its sidecar (content NOT opened);
  * name-only searches over the 0341 searched paths for the missing primary documents (forbidden names counted, never listed).
Never emitted: density, error, velocity, photometry or radius literals; distances; other galaxies' names.
Note: the name-only search reflects the filesystem at run time; it is the only part that can change if files are added later.
Usage: python3 -I -B source_semantics_probe_0356_v002.py <new_output.json>
"""
import hashlib, html, json, os, re, sys, zipfile

UNT = '/Users/bgm/Research/Universal Network Theory'
JPC = UNT + '/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
CA = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
PIN = {
    'leroy_readme': (JPC + '/leroy2008_ReadMe.html', 'cbd9a431c5ef4d9ae1bcda8bc141210bd03360a4d2b0ea5d8dd40e9079763c48'),
    'readiness_note': (JPC + '/GALAXY_INPUT_READINESS.md', '6e23d981e7bf0450a1e51169d29a9d54b6f2d1e4fd014432255988e018e0ec6c'),
    'p53_freeze': ('/Users/bgm/Research/UNT_EXCHANGE/lanes/P53_CODEX2/P53_LINE_A_OBSERVATIONAL_FREEZE_V001.json', 'a8126eb6175f68629cc9e925bcadbced8b153659d8a3b1eed96e0f6985f64053'),
    'bundle_contract_v006': (CA + '/source_adapter_write_0348/SOURCE_BUNDLE_FIELD_CONTRACT_V006.json', '1e8a9a7c399c9ff8c3ba10afc37a637bf57215c5f415e3eca6bb305483757040'),
    'join_0352': (CA + '/query_uncertainty_join_0352/QUERY_UNCERTAINTY_JOIN_0352_V001.json', '2875dc3255de025f457ced11027067c3e1ff37e6e01a16e3fbf1d88c2f28662b'),
    'sparc_index': (JPC + '/sparc_official_index_2026-10-06_v001.html', 'ee7e3eab83de7d698bc14d9eeb91d87a939221dd452e907ea5ad7dedae886038'),
    'sfb': (JPC + '/sparc_official_NGC3198.sfb', 'ae071272156d47f6292fa405adf3a9b2042f8678581af108b2d5d1e9e102ddbc'),
    'dens': (JPC + '/sparc_official_NGC3198.dens', '4dbe84c28033a501c1599998daa534ae4d73957597c342fba21fd7a3def71d21'),
    'sfb_zip': (JPC + '/sparc_official_sfb_LTG_2026-10-06_v001.zip', '2ca5c5e16517d2096dde47247f2b78837e33fed2e323ea77b0412cf6de66eb27'),
    'sfb_zip_source': (JPC + '/sparc_official_sfb_LTG_2026-10-06_v001.zip.SOURCE.json', '274993d0ab0cd1805ba6fea2d7327bd7ba9a8aab9849116e6ac6bc396b6e440c'),
    'dens_zip': (JPC + '/sparc_official_BulgeDiskDec_LTG_2026-10-06_v001.zip', '0733de0d357cbd45c673fd4321a3b339e160abf68530684c09d28e413855fb6d'),
    'dens_zip_source': (JPC + '/sparc_official_BulgeDiskDec_LTG_2026-10-06_v001.zip.SOURCE.json', 'e097262eb3693a83376d8ae48b88fa197efd05fa81cfed0228727f5a5c074cec'),
    'sparc_cds_readme': (JPC + '/external_ddo154_v001/SPARC_ReadMe.html', '457f61cd8e63dd7b8f8ce0052a458294fa1a5acc2b5b23bb951a2c40d69f9666'),
    'sparc_paper_pdf_sidecar': (JPC + '/sparc_lelli_mcgaugh_schombert_2016_AJv152n157_v001.pdf.SOURCE.json', None),
    'crosswalk_0341': (CA + '/source_crosswalk_0341/SOURCE_CROSSWALK_V001.json', '691483835e9d5201957a2b7183deaa1e8d994efeaa2644c3374d8e59f2450c72'),
    'ledger_0341': (CA + '/source_crosswalk_0341/UNCERTAINTY_MISSING_INPUT_LEDGER_V001.json', '07dd4aa300b8b818a2b962646dffd3711f461cccfa87052f7f9d760e4fdb29e0'),
    'correction_0346': (CA + '/source_crosswalk_0341/SOURCE_CROSSWALK_CORRECTION_0346_V001.json', '988e871acc0e6f3c1e3b91abec7143cb5b69241d6894b140f15369a6f29fca24'),
    'root_review_0352': (UNT + '/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/QUERY_UNCERTAINTY_JOIN_ROOT_REVIEW_V001.json', '60551a338d6ea8f28c28de54fcbd9ed6dd528ddee3012faaf124df271fdc58ec'),
}
LEROY_COPIES = [JPC + '/leroy2008_ReadMe_RECOVERED_2026-10-08_V001.html',
                JPC + '/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/P53_COMPLETE_NATIVE_INPUT_PARSER_HELD_SOURCE_V001/ROOT_COMPLETE_PARSER_CALLS_V001/RAW/ReadMe.html',
                JPC + '/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/P53_COMPLETE_NATIVE_INPUT_PARSER_HELD_SOURCE_V002/ROOT_COMPLETE_PARSER_CALLS_V002/RAW/ReadMe.html']
SPARC_PDF = JPC + '/sparc_lelli_mcgaugh_schombert_2016_AJv152n157_v001.pdf'
SEARCH_ROOTS = [JPC, UNT + '/UNT_PROGRAM_CONTROL', '/Users/bgm/Research/UNT_EXCHANGE/lanes', CA]
SEARCH_PATTERNS = {
    'leroy_2008_paper': r'(?i)(0810\.2556|leroy.*\.(pdf|ps|tex|djvu)$|appendix[_ -]?e(?![a-z]))',
    'archangel_documentation': r'(?i)(archangel|schombert|0703646)',
    'sparc_master_paper': r'(?i)(1606\.09251|AJv152n157|lelli.*\.(pdf|ps|tex)$)'}
FORBIDDEN = re.compile(r'Newton|FIELD_|RESPONSE|ROTATION|FIT|TRIAL|MOM1|rotmod|MassModels')
LINE_METHOD = 'tags removed (re.sub <[^>]+> -> ""), html.unescape, splitlines; 1-based (the 0346 line_method)'
ROW = re.compile(r'^\s*(\d+)(?:-\s*(\d+))?\s+([AIF]\d+(?:\.\d+)?)\s+(\S+)\s+(\S+)\s*(.*)$')
MASK = lambda s: re.sub(r'\d', '#', s)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_pinned(key):
    p, h = PIN[key]
    b = open(p, 'rb').read()
    if h is not None and sha(b) != h:
        raise SystemExit('E_PIN ' + key)
    return b


def html_lines(b):
    return html.unescape(re.sub(r'<[^>]+>', '', b.decode('utf-8', 'replace'))).splitlines()


def name_search():
    out = {}
    rx = {k: re.compile(v) for k, v in SEARCH_PATTERNS.items()}
    hits = {k: [] for k in rx}
    hidden = {k: 0 for k in rx}
    for root in SEARCH_ROOTS:
        for dp, dns, fns in os.walk(root):
            dns.sort()
            for n in sorted(fns):
                for k, r in rx.items():
                    if r.search(n):
                        rel = os.path.join(dp, n).replace(UNT, '<UNT>')
                        if FORBIDDEN.search(rel):
                            hidden[k] += 1
                        else:
                            hits[k].append(rel)
    for k in rx:
        out[k] = {'pattern_on_file_names': SEARCH_PATTERNS[k], 'matches': sorted(hits[k]), 'matches_with_forbidden_names_not_listed': hidden[k]}
    return {'roots': [r.replace(UNT, '<UNT>') for r in SEARCH_ROOTS], 'method': 'os.walk, file names only (no content), followlinks False',
            'results': out}


def main(out):
    res = {'schema': 'CLAUDE2_0356_SOURCE_SEMANTICS_PROBE_V002', 'line_method_html': LINE_METHOD,
           'pins_verified': {k: {'path': v[0], 'sha256': v[1] if v[1] else sha(open(v[0], 'rb').read())} for k, v in PIN.items()}}
    # ---- Leroy ReadMe (primary CDS documentation of table7)
    t = html_lines(read_pinned('leroy_readme'))
    res['leroy_readme_lines'] = {str(n): t[n - 1] for n in (96, 163, 165, 171, 172, 173, 174, 175, 176, 179, 185, 186, 190, 196)}
    nf = {}
    for n in range(167, 184):
        m = ROW.match(t[n - 1])
        if m:
            nf[m.group(5)] = {'line': n, 'format': m.group(3), 'question_mark_null_flag': m.group(6).lstrip().startswith('?'),
                              'note3_attached': '(3)' in m.group(6)}
    res['leroy_table7_null_flag_by_label'] = nf
    res['leroy_readme_copies_identical'] = {p: sha(open(p, 'rb').read()) == PIN['leroy_readme'][1] for p in LEROY_COPIES}
    # ---- secondary readiness note: cited lines, all digits masked
    rl = read_pinned('readiness_note').decode('utf-8', 'replace').splitlines()
    res['readiness_note_lines_digits_masked'] = {str(n): MASK(rl[n - 1]) for n in list(range(46, 50)) + list(range(170, 180))}
    # ---- P53 freeze (program record)
    fz = json.loads(read_pinned('p53_freeze'))
    res['p53_freeze_digits_masked'] = {
        '/status': MASK(json.dumps(fz['status'])),
        '/choices/error_and_censoring': MASK(json.dumps(fz['choices']['error_and_censoring'])),
        '/choices/H2_missing_support': MASK(json.dumps(fz['choices']['H2_missing_support'])),
        '/distinct_freeze_review': fz.get('distinct_freeze_review')}
    # ---- bundle contract V006 interpretation-rule lines
    cl = read_pinned('bundle_contract_v006').decode('utf-8').splitlines()
    res['bundle_contract_v006_lines'] = {str(n): cl[n - 1].strip() for n in (56, 57, 58, 139, 140, 141)}
    # ---- 0352 join: stored S1 labels of the U9/U10 targets (labels only; no literal)
    j = json.loads(read_pinned('join_0352'))
    lab = {}
    for q in j['per_query']:
        for r in (q.get('S1') or {}).get('rows', []) or []:
            for comp in ('stars', 'H2', 'HI'):
                c = r['components'].get(comp)
                if c is not None:
                    lab.setdefault('row_%d_%s' % (r['row_index'], comp), {**c, 'original_line_number': r['original_line_number']})
    res['join_0352_stored_labels'] = {k: lab[k] for k in ('row_2_stars', 'row_16_stars', 'row_18_stars', 'row_20_stars')}
    res['join_0352_HI_rows_with_upper_limit_marker'] = sorted(k for k, v in lab.items() if k.endswith('_HI') and v.get('upper_limit_marker'))
    res['join_0352_D1'] = {'pointer': '/disagreements/0', 'finding': j['disagreements'][0]['finding']}
    # ---- 0341 statements qualified here: booleans, states and pointers only
    cw = json.loads(read_pinned('crosswalk_0341'))
    lg = json.loads(read_pinned('ledger_0341'))
    ef = cw['sources']['S1_LEROY_T7']['error_fields']
    fmt = re.search(r'F\d+\.\d+', ef['e_SigmaHI'])
    res['crosswalk_0341_checks'] = {
        '/sources/S1_LEROY_T7/error_fields/e_SigmaHI format text': fmt.group(0) if fmt else None,
        '/sources/S1_LEROY_T7/error_fields/e_Sigma* contains "not zero uncertainty"': 'not zero uncertainty' in ef['e_Sigma*'],
        '/sources/S3_SPARC_SFB/error_fields contains "not documented locally"': 'not documented locally' in cw['sources']['S3_SPARC_SFB']['error_fields'],
        '/sources/S3_SPARC_SFB/masks contains "not documented locally"': 'not documented locally' in cw['sources']['S3_SPARC_SFB']['masks']}
    res['ledger_0341_items'] = {it['id']: {'pointer': '/items/%d' % i, 'state': it['state']} for i, it in enumerate(lg['items'])
                                if it['id'] in ('U9', 'U10', 'U11', 'U14', 'U15')}
    byid = {it['id']: it for it in lg['items']}
    res['ledger_0341_checks'] = {'U14 evidence contains "not documented locally"': 'not documented locally' in byid['U14']['evidence'],
                                 'U9 evidence contains "primary Appendix E not local"': 'primary Appendix E not local' in byid['U9']['evidence'],
                                 'U10 evidence contains "rounding is a hypothesis"': 'rounding is a hypothesis' in byid['U10']['evidence']}
    res['ledger_0341_absence_scope'] = lg['absence_scope']
    # ---- SPARC index page
    it_ = read_pinned('sparc_index')
    tl = html_lines(it_)
    res['sparc_index_lines'] = {str(n): tl[n - 1].strip() for n in (53, 55, 56, 64)}
    res['sparc_index_links_present'] = {'sfb_LTG.zip': b'sfb_LTG.zip' in it_, 'BulgeDiskDec_LTG.zip': b'BulgeDiskDec_LTG.zip' in it_}
    low = '\n'.join(tl).lower()
    res['sparc_index_mentions'] = {w: (w in low) for w in ('kill', 'comment', 'uncertaint', '.sfb', '#')}
    res['sparc_index_error_word_lines'] = [i + 1 for i, l in enumerate(tl) if 'error' in l.lower()]
    # ---- SPARC CDS ReadMe (J/AJ/152/157), absence check only
    st = '\n'.join(html_lines(read_pinned('sparc_cds_readme'))).lower()
    res['sparc_cds_readme_mentions'] = {w: (w in st) for w in ('sfb', 'kill', 'photometric profile', 'surface brightness profile')}
    # ---- .sfb structure (NGC3198); compared texts come from the crosswalk at run time and are never emitted
    s3 = cw['sources']['S3_SPARC_SFB']['radial_coordinate']
    m_last = re.search(r'(\d+) rows [0-9.]+-([0-9.]+) arcsec', s3)
    m_com = re.search(r'(\d+) commented rows at ([0-9.]+) and ([0-9.]+) arcsec', s3)
    L = read_pinned('sfb').split(b'\n')
    while L and L[-1] == b'':
        L.pop()
    com = [i + 1 for i, l in enumerate(L) if l.lstrip().startswith(b'#')]
    dat = [i + 1 for i, l in enumerate(L) if i > 0 and l.strip() and not l.lstrip().startswith(b'#')]
    res['sfb_structure'] = {
        'n_lines': len(L), 'line_1_text': L[0].decode('ascii'), 'line_1_is_commented': L[0].lstrip().startswith(b'#'),
        'uncommented_data_lines': [dat[0], dat[-1]], 'n_uncommented_data_rows': len(dat),
        'commented_lines': com, 'n_commented_rows': len(com),
        'commented_rows_are_the_last_lines_of_the_file': com == list(range(len(L) - len(com) + 1, len(L) + 1)),
        'comment_char_attached_to_first_token': all(re.match(rb'^#\S', L[i - 1].lstrip()) is not None for i in com),
        'commented_rows_token_counts': [len(L[i - 1].split()) for i in com],
        'uncommented_rows_all_4_tokens': all(len(L[i - 1].split()) == 4 for i in dat),
        'commented_rows_after_last_uncommented_row': min(com) > max(dat),
        'kill_token_of_commented_rows_equals_flag_one': [L[i - 1].split()[2] == b'1' for i in com],
        'crosswalk_masks_states_kill_on_all_rows_including_both_commented_rows': ('in all' in cw['sources']['S3_SPARC_SFB']['masks'] and 'both commented rows' in cw['sources']['S3_SPARC_SFB']['masks']),
        'crosswalk_pointer': '/sources/S3_SPARC_SFB/radial_coordinate',
        'crosswalk_uncommented_row_count_equals_observed': bool(m_last) and int(m_last.group(1)) == len(dat),
        'crosswalk_commented_row_count_equals_observed': bool(m_com) and int(m_com.group(1)) == len(com),
        'commented_radius_tokens_equal_crosswalk_texts': bool(m_com) and [L[i - 1].split()[0] for i in com] == [b'#' + m_com.group(2).encode(), b'#' + m_com.group(3).encode()],
        'last_uncommented_radius_token_equals_crosswalk_text': bool(m_last) and L[dat[-1] - 1].split()[0] == m_last.group(2).encode(),
        'CR_present': any(l.endswith(b'\r') for l in L)}
    # ---- .dens structure (NGC3198)
    s4 = cw['sources']['S4_SPARC_DENS']['radial_coordinate']
    counts = [int(x) for x in re.findall(r'(\d+) rows', s4)]
    D = read_pinned('dens').split(b'\n')
    while D and D[-1] == b'':
        D.pop()
    nd = sum(1 for l in D if l.strip() and not l.lstrip().startswith(b'#'))
    res['dens_structure'] = {
        'line_1_text': D[0].decode('ascii'), 'commented_lines': [i + 1 for i, l in enumerate(D) if l.lstrip().startswith(b'#')],
        'n_uncommented_rows': nd, 'crosswalk_pointer': '/sources/S4_SPARC_DENS/radial_coordinate',
        'crosswalk_row_counts_in_order': counts,
        'crosswalk_total_equals_observed': bool(counts) and counts[0] == nd,
        'crosswalk_matched_equals_sfb_uncommented_rows': len(counts) > 1 and counts[1] == len(dat),
        'crosswalk_counts_add_up': len(counts) == 3 and counts[0] == counts[1] + counts[2]}
    # ---- zips: member metadata and aggregate header/comment-position census (no data row, no name emitted)
    numtok = re.compile(rb'^[-+]?\d+(\.\d+)?([eE][-+]?\d+)?$')
    zres = {}
    for key, kind, hdr in (('sfb_zip', 'sfb', b'radius mu kill error'), ('dens_zip', 'dens', b'# Rad[kpc] SBdisk[Lsun/pc^2] SBbulge[Lsun/pc^2]')):
        read_pinned(key)
        z = zipfile.ZipFile(PIN[key][0])
        names = z.namelist()
        agg = {'members': len(names), 'members_not_sfb_or_dens': sum(1 for n in names if not (n.endswith('.sfb') or n.endswith('.dens'))),
               'zip_comment_empty': z.comment == b'', 'first_line_equals_canonical_header': 0, 'first_line_other': 0,
               'files_with_commented_rows_beyond_line_1': 0, 'commented_rows_beyond_line_1': 0,
               'files_commented_rows_all_after_last_uncommented_row': 0, 'files_commented_rows_all_before_first_uncommented_row': 0,
               'files_commented_rows_interleaved': 0, 'commented_rows_data_shaped_4_numeric_tokens': 0, 'commented_rows_other_shape': 0}
        for n in names:
            X = z.read(n).replace(b'\r', b'').split(b'\n')
            while X and X[-1] == b'':
                X.pop()
            agg['first_line_equals_canonical_header' if re.sub(rb'\s+', b' ', X[0].strip()) == hdr else 'first_line_other'] += 1
            c = [i for i, l in enumerate(X) if i > 0 and l.lstrip().startswith(b'#')]
            d = [i for i, l in enumerate(X) if i > 0 and l.strip() and not l.lstrip().startswith(b'#')]
            if c:
                agg['files_with_commented_rows_beyond_line_1'] += 1
                agg['commented_rows_beyond_line_1'] += len(c)
                if d:
                    if min(c) > max(d):
                        agg['files_commented_rows_all_after_last_uncommented_row'] += 1
                    elif max(c) < min(d):
                        agg['files_commented_rows_all_before_first_uncommented_row'] += 1
                    else:
                        agg['files_commented_rows_interleaved'] += 1
                for i in c:
                    tk = X[i].lstrip()[1:].split()
                    agg['commented_rows_data_shaped_4_numeric_tokens' if (len(tk) == 4 and all(numtok.match(x) for x in tk)) else 'commented_rows_other_shape'] += 1
        ngc = [{'member': i.filename, 'file_size': i.file_size, 'date_time': list(i.date_time),
                'member_sha256_equals_local_file': sha(z.read(i.filename)) == PIN[kind][1]} for i in z.infolist() if i.filename == 'NGC3198.' + kind]
        zres[key] = {'aggregate_census': agg, 'NGC3198_member': ngc, 'source_sidecar': json.loads(read_pinned(key + '_source'))}
    res['zips'] = zres
    # ---- local SPARC paper PDF: CANDIDATE; content unverified (hashed only; outside the 0341/0346 set)
    pb = open(SPARC_PDF, 'rb').read()
    scb = read_pinned('sparc_paper_pdf_sidecar')
    sc = json.loads(scb)
    res['sparc_paper_pdf'] = {'label': 'CANDIDATE; CONTENT UNVERIFIED (hashed only, not opened)', 'path': SPARC_PDF, 'sha256': sha(pb), 'bytes': len(pb),
                              'sidecar': {'path': PIN['sparc_paper_pdf_sidecar'][0], 'sha256': sha(scb), 'content': sc},
                              'sidecar_sha256_matches_pdf': sc.get('sha256') == sha(pb), 'content_read': False}
    del pb
    # ---- name-only searches for the missing primary documents
    res['name_only_search'] = name_search()
    rr = json.loads(read_pinned('root_review_0352'))
    res['root_review_0352_retained_notes'] = rr['retained_notes']
    read_pinned('correction_0346')
    with open(out, 'x') as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    print(json.dumps({'ok': True, 'output': out, 'bytes': os.path.getsize(out)}))


if __name__ == '__main__':
    main(sys.argv[1])
