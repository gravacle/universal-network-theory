"""verify_consistency_2: re-read the lens-C 'C-3/C-8' AMBIGUITY events (finding L-C02) under the
precedence clauses that the r2 bytes already contain.

Read-only inputs (sha-checked): the r2 PREREG and ROOT_ITEMS, and lens C's synthetic case results
and classifier. No target, no NGC3198 data table, no run output is read. Writes one JSON file
(path given as argv[1]) and prints a summary.
"""
import hashlib, json, sys, collections

R1 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r2/round1/'
LC = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r2/checks/consistency/'
FILES = {
    'PREREG': (R1 + 'PREREG_MISS_READING_R2.md', '6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143'),
    'ROOT_ITEMS': (R1 + 'ROOT_ITEMS_R2.md', '1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f'),
    'CASES': (LC + 'CASES_RESULTS_V2.json', '73adc286a5edb8e6e81a53da3304e1a57d18064e1281b4149b327caffb090576'),
    'CLASSIFIER': (LC + 'tools/lensc_classifier.py', 'a890c8fd468bc5efe544e895ab66ede7c2c58e6a6065a52cbdec3f1ffadf7533'),
}
raw = {}
for k, (p, sha) in FILES.items():
    b = open(p, 'rb').read()
    got = hashlib.sha256(b).hexdigest()
    if got != sha:
        sys.exit('SHA MISMATCH %s %s != %s' % (k, got, sha))
    raw[k] = b.decode('utf-8')
lines = {k: raw[k].split('\n') for k in raw}

# ---- 1. the quoted and the precedence-bearing clauses, by file and 1-based line
QUOTES = [
    # the finding's own quotes
    ('PREREG', 168, 'The 43-row score can make a reading **consistent** or **inconsistent**.', 'finding quote'),
    ('PREREG', 169, 'A reading whose deciding test has not run stays OPEN, whatever the score shows.', 'finding quote; precedence (general)'),
    ('PREREG', 196, 'A41 item 3 (FORMAL + TESTED) already registers', 'finding quote'),
    ('PREREG', 207, 'Route B consumes the azimuthal mean, so the', 'finding quote'),
    ('PREREG', 340, 'each with the status consistent, inconsistent or OPEN, plus each deciding test\'s status.', 'finding quote (full clause)'),
    # precedence the finding does not cite
    ('ROOT_ITEMS', 89, 'Their readings (R-UT1, R-HIST, R-REACH and R-TSR) then stay OPEN after the score, whatever it shows.', 'precedence (M-4)'),
    ('PREREG', 201, 'DT-GEO is not evaluated, so this reading stays OPEN by construction.', 'precedence (R-GEO)'),
    ('PREREG', 207, 'DT-TSR (NOT SCHEDULED): R-TSR stays OPEN', 'precedence (R-TSR)'),
    ('PREREG', 207, 'R-TSR is therefore registered as an open possibility, not an expected cause.', 'A66.2 framed as a caveat, not an inconsistency trigger'),
    ('PREREG', 284, 'and R-DRIFT stays OPEN.', 'precedence (R-DRIFT, STAGE0 NOT_EVALUATED)'),
    ('PREREG', 199, 'DT-S0G; it can make R-DRIFT consistent or inconsistent, never supported (§6.3)', 'decider for R-DRIFT'),
    ('PREREG', 199, 'OUTER miss-dominated (P1, P1g or P2)', 'R-DRIFT consistent column'),
    ('PREREG', 363, 'They are NOT SCHEDULED, and their readings stay OPEN (§3).', 'precedence (self-check)'),
    ('PREREG', 366, 'R-TSR may cite only flagged rows, and it stays OPEN.', 'precedence (self-check, R-TSR)'),
    ('PREREG', 44, '| ORIGINAL_K | state | EVALUATED_BEFORE_FREEZE |', 'R-GRID test has run'),
    ('PREREG', 185, 'ORIGINAL_K is evaluated.', 'R-GRID test has run'),
    ('PREREG', 200, 'ORIGINAL_K shows the same excess (against R-GRID)', 'R-GRID decider'),
    ('PREREG', 183, 'runs only after a verified freeze (A10, A16.3). | registered |', 'DT-T1a timing'),
    ('PREREG', 21, 'Where this text is silent, the reading less favourable to any adopted hypothesis is chosen', 'general gap-filler'),
    # lens classifier: how the events are generated
    ('CLASSIFIER', 237, 'if not test_run:', 'OPEN added whenever test not run'),
    ('CLASSIFIER', 238, "cands.append('OPEN')", 'OPEN added whenever test not run'),
    ('CLASSIFIER', 266, "reading_status('R-UT1', True, FACT_A41_ITEM3, False, ev)", 'A41 item 3 mapped to inconsistent'),
    ('CLASSIFIER', 282, "R['R-GRID'] = {'cands': reading_status('R-GRID', True, False, False, ev,", 'R-GRID test_run hard-coded False'),
    ('CLASSIFIER', 307, "reading_status('R-TSR', True, FACT_A66_2_AZIMUTHAL, False, ev)", 'A66.2 mapped to inconsistent'),
]
quote_results = []
for f, ln, s, role in QUOTES:
    ok = s in lines[f][ln - 1]
    quote_results.append({'file': f, 'line': ln, 'text': s, 'role': role, 'present': ok})
all_quotes_ok = all(q['present'] for q in quote_results)

# ---- 2. recount the lens events and check the finding's evidence
cases = json.loads(raw['CASES'])['cases']
evs = []
for c in cases:
    for e in c['events']:
        if e['kind'] == 'AMBIGUITY' and e['tag'] == 'C-3/C-8':
            evs.append((c['case'], e['detail'], tuple(e['options']),
                        (c.get('stage0') or {}).get('comparison')))
by_case = {c['case'][:3]: c for c in cases}
evidence = {
    'n_events': len(evs),
    'C01_R-UT1': by_case['C01']['readings']['R-UT1']['cands'],
    'C01_R-HIST': by_case['C01']['readings']['R-HIST']['cands'],
    'C16_R-TSR': by_case['C16']['readings']['R-TSR']['cands'],
    'C21_R-DRIFT': by_case['C21']['readings']['R-DRIFT']['cands'],
}

# ---- 3. structural check: is the 'consistent with the reading if' column true for every reported reading?
n_inst = n_cons = 0
for c in cases:
    for name, v in (c.get('readings') or {}).items():
        if isinstance(v, dict) and 'cands' in v:
            n_inst += 1
            n_cons += ('consistent' in v['cands'])

# ---- 4. re-apply the text's own precedence
EXPLICIT = {
    'R-UT1': 'OPEN: PREREG L169 + ROOT_ITEMS L89 (M-4) + PREREG L363',
    'R-HIST': 'OPEN: PREREG L169 + ROOT_ITEMS L89 (M-4) + PREREG L363',
    'R-REACH': 'OPEN: PREREG L169 + ROOT_ITEMS L89 (M-4) + PREREG L363',
    'R-TSR': 'OPEN: PREREG L169 + L207 + L366 + ROOT_ITEMS L89 (M-4)',
    'R-GEO': 'OPEN: PREREG L169 + L201',
}
GENERAL = {
    'R-NAX': 'OPEN: PREREG L169 (DT-NAX "not run", L186)',
    'R-S1': 'OPEN: PREREG L169 (DT-S1 "UNTESTED", L187)',
    'P5-onset': 'OPEN: PREREG L169 (deciding test "as P1; DT-NAX", L202)',
}
TIMING = {
    'R-ML': 'OPEN by L169 iff DT-T1a ("registered", runs after a verified freeze, L183) has not run at report time',
    'R-SPEC': 'OPEN by L169 iff DT-T1a has not run at report time (C-3.3 joint with R-ML)',
    'R-GEFF': 'OPEN by L169; the P3/P4 row names no test for R-GEFF individually (L201)',
}
resolved = []
for case, name, opts, s0 in evs:
    if name in EXPLICIT:
        cls, res, why = 'EXPLICIT_OPEN', 'OPEN', EXPLICIT[name]
    elif name in GENERAL:
        cls, res, why = 'GENERAL_L169_OPEN', 'OPEN', GENERAL[name]
    elif name in TIMING:
        cls, res, why = 'L169_OPEN_TIMING_DEPENDENT', 'OPEN (if DT-T1a not yet run)', TIMING[name]
    elif name == 'R-DRIFT' and s0 == 'NOT_EVALUATED':
        cls, res, why = 'EXPLICIT_OPEN', 'OPEN', 'PREREG L284 (+ L169)'
    elif name == 'R-DRIFT' and s0 == 'AGAINST':
        cls, res, why = 'DT_CLAUSE_STRUCTURAL', 'inconsistent', ('PREREG L199: DT-S0G "can make R-DRIFT consistent or '
                                                             'inconsistent"; against column names AGAINST; the consistent '
                                                             'column holds whenever R-DRIFT is reported')
    elif name == 'R-DRIFT' and s0 == 'NOT_DECIDED':
        cls, res, why = 'RESIDUAL_UNRULED_ALREADY_L-C08d', None, 'no clause maps NOT_DECIDED; lens L-C08 (d) already proposes OPEN'
    elif name == 'R-GRID':
        cls, res, why = 'LENS_INPUT_ERROR', 'consistent or inconsistent per ORIGINAL_K', ('DT-ALT/ORIGINAL_K is evaluated (PREREG '
                                                                                      'L44, L185); the OPEN candidate is spurious; '
                                                                                      'residual is the undefined "same excess" (L-C09)')
    elif name == 'R-MF':
        cls, res, why = 'OTHER_FINDING_L-C01', None, 'P1-row against vs P2-row consistent: cross-row conflict (L-C01)'
    else:
        cls, res, why = 'UNCLASSIFIED', None, ''
    resolved.append({'case': case, 'reading': name, 'lens_options': list(opts), 'stage0': s0,
                     'class': cls, 'status_under_text_precedence': res, 'basis': why})
cls_count = collections.Counter(r['class'] for r in resolved)
out = {
    'inputs_sha256': {k: FILES[k][1] for k in FILES},
    'quotes_all_present': all_quotes_ok,
    'quotes': quote_results,
    'finding_evidence_reproduced': evidence,
    'consistent_column_true_in_reported_instances': {'instances': n_inst, 'with_consistent': n_cons},
    'event_classes': dict(cls_count),
    'events': resolved,
}
json.dump(out, open(sys.argv[1], 'x'), indent=1, ensure_ascii=False)
print('quotes_all_present', all_quotes_ok)
print('evidence', json.dumps(evidence))
print('consistent column true in', n_cons, 'of', n_inst, 'reported reading instances')
print('classes', json.dumps(dict(cls_count), indent=1))
