# Claude4 helper: write RESULTS_SEAL_TOOLS_V002_CHECK_C4CHK.json (exclusive create). Every sha is computed from bytes here; the UTC
# stamp is taken from the clock. The report text lives in this JSON (the harness refuses report .md files from subagents).
import glob, hashlib, json, os, re, sys, time
from pathlib import Path
CHK = Path(__file__).resolve().parent.parent
CA = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ENV = 'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1'
RUNF = 'cd %s/tests && %s taskpolicy -b %s -I -B %s/tools/run_fenced_c4chk.py ' % (CHK, ENV, PY, CHK)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin(p):
    return {'path': str(p), 'sha256': sha(p)}


def one(pattern):
    m = sorted(glob.glob(str(CHK / pattern)))
    return Path(m[-1])


v2 = one('tests/run_v2_*')
v3 = one('tests/run_v3_r13_*')
cli = one('tests/cli_base_*')
ab1 = one('tests/ab1_*')
bs = one('builder_suite/r2/tests/run_*')
r_v2 = json.loads((v2 / 'TEST_RESULTS_C4CHK_V2.json').read_bytes())
r_v3 = json.loads((v3 / 'TEST_RESULTS_C4CHK_V3_R13.json').read_bytes())
r_bs = json.loads((bs / 'TEST_RESULTS_C4V002.json').read_bytes())
blocked = {}
for f in sorted(glob.glob(str(CHK / 'out/*.stderr.txt'))) + [str(CHK / 'out/SECTION_DIFF_R5GEN_VS_OPEN_ACB7F44A_C4CHK.txt')]:
    t = Path(f).read_text(encoding='utf-8', errors='replace')
    m = re.search(r'FENCE_C4CHK_SUMMARY (\{.*\})', t)
    if m:
        s = json.loads(m.group(1))
        blocked[os.path.basename(f)] = {'selftest': s['selftest'], 'probes': s['probes'], 'blocked_during_run': s['blocked_during_run']}
cases_v2 = {r['case']: r for r in r_v2['results']}


def case(name):
    r = cases_v2[name]
    return {'verdict': r['verdict'], 'ok': r['ok'], 'codes': r['codes'][:6]}


F = [
 {'id': 'C-01', 'severity': 'BLOCKING', 'label': 'TESTED + FORMAL (new since the v002 build: A104, 22:13Z)',
  'claim': ('A104 made D-05 mechanical: a cited entry whose bytes changed needs the disposition revised, or no_change_after_change with a changed_text '
            'excerpt (present in the new bytes, absent from the old) and a reason. Seal tools v002 r2 cannot enforce this. Tool 1 re-hashes only the '
            'A82-A101 table rows, so an edit inside a cited entry from A47 to A81 passes unseen (TESTED: an edit inside A62 gives tool 1 PASS). For a '
            'changed table row a bare --covered-later A<n> is enough: tool 1 passes and the SEAL_RECORD carries only the two section shas, with no '
            'disposition, excerpt or reason (TESTED: an edit inside A99 plus --covered-later A99 gives PASS with note ENTRY_TABLE_SECTION_CHANGED_NOTED). '
            'The successor (seal tools v003, A103) must implement A104 before the freeze. Until then root can diff every cited section against prereg '
            'r5\'s pinned read copy 70a48f51 (assembly.rulings_read.V005_addendum_open_observed = r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md). '
            'As of the open file acb7f44a (22:15Z) no section has changed; only A102, A103 and A104 were added (TESTED).'),
  'reproduction': (RUNF + 'test_c4chk_v2.py ; cases "tool 1: an edit inside cited entry A62 ..." and "tool 1: the A99 edit with root\'s note ..." in '
                   + str(v2 / 'TEST_RESULTS_C4CHK_V2.json') + ' ; section diff: ' + RUNF + '../tools/section_diff_c4chk.py '
                   + str(CA / 'v007_final_prereg_c4/r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md') + ' <open V005 copy> (out/SECTION_DIFF_R5GEN_VS_OPEN_ACB7F44A_C4CHK.txt)'),
  'evidence': {'A62_edit': case('tool 1: an edit inside cited entry A62 (before A82, no table row) after r5 was written passes'),
               'A99_edit_noted': case("tool 1: the A99 edit with root's note (--covered-later A99,...)")},
  'owner': 'Claude4 (seal tools v003)'},
 {'id': 'C-02', 'severity': 'SHOULD_FIX', 'label': 'TESTED',
  'claim': ('Text of record. While TEXT_OF_RECORD_SHA is PENDING, tool 3 accepts any file root names with --text-of-record together with that file\'s own '
            'sha. If the file is the sealed prereg itself, the check that nothing changed outside slot values compares the file with itself. TESTED: a '
            'sealed prereg whose tests.T3 text was edited refuses SEALED_PREREG_TEXT_CHANGED against the r5 text, but passes tool 3 when named as its own '
            'text of record, and the builder then prints a SEAL_RECORD (text_of_record = the sealed prereg, pinned_by ROOT_ARGUMENT). The v001 constant '
            'pin made this impossible. Fix: refuse a text of record that equals the sealed prereg or has any filled seal_slots.<k>.value (r5 holds '
            'PENDING_ROOT_AT_SEAL_ASSEMBLY in all of them except cache_directory_r6_only NOT_APPLICABLE_R5); or set the pin in the successor once root '
            'rules the text of record.'),
  'reproduction': RUNF + 'test_c4chk_v2.py ; cases "root names the SEALED prereg itself as the text of record ...", "the same edited sealed prereg named as its own text of record ...", "the builder then prints a SEAL_RECORD for the edited sealed prereg ..."',
  'evidence': {'self_text': case('root names the SEALED prereg itself as the text of record (its own sha): tool 3 passes'),
               'edited_self_text': case('the same edited sealed prereg named as its own text of record passes tool 3 (the edit is invisible)'),
               'control': case('control: an edited T3 text in the sealed prereg against the scratch r5 text of record')}},
 {'id': 'C-03', 'severity': 'SHOULD_FIX', 'label': 'TESTED',
  'claim': ('B6 provenance (R-04, incomplete). The builder checks the form of the B6 bodies (schema, blinded, test_mode false, script_sha256 = the sealed '
            'compare, route_a_mode, C5H only, no numbers), but not that they evaluated the slotted records. TESTED: a GATES_ONLY body whose DOUBLING '
            'record_sha256 is not the slot\'s, and whose GQ record_sha256 is the superseded V005, still yields a SEAL_RECORD. SRR[0] requires the gate '
            'functions to run on the real input records. Fix: require each blinded gate\'s record_sha256 to equal the slot record (EPS, LO, GQ, DOUBLING, '
            'LO_NGC; B1, B1_OFF and B0prime_RERUN from the identity slots; B2 from --b2-record) or the registry\'s record of record.'),
  'reproduction': RUNF + 'test_c4chk_v2.py ; case "R-04 GATES body whose DOUBLING / GQ record_sha256 are not the slot records ..."',
  'evidence': {'record_shas': case('R-04 GATES body whose DOUBLING / GQ record_sha256 are not the slot records (GQ = superseded V005) still yields a SEAL_RECORD')}},
 {'id': 'C-04', 'severity': 'SHOULD_FIX', 'label': 'TESTED (the D-04 failure class)',
  'claim': ('Tool 3 pins the producer registry from bytes but never loads it with the compare\'s own load_producer_registry, and never checks the slot '
            'records against it. TESTED, each passes tool 3: (a) a registry that r12 refuses at load (PRODUCER_REGISTRY_DUPLICATE_ENTRY, A71); (b) the GQ '
            'slot holding the superseded GQ_CERT_V005 fbceefe6 (A86), which registry C3V009 does not list; (c) the comparator slot holding the superseded '
            'c2v004 e3d153b6. So slots that pass tools 1-4 can still be unusable by the sealed compare, the D-04 failure class. Fix: call '
            'M.load_producer_registry(slot) in-process, and require every slot record to be listed in the registry\'s gate_records for its gate and the '
            'comparator to be listed in identity_comparators.'),
  'reproduction': RUNF + 'test_c4chk_v2.py ; cases "a producer registry r12 refuses at load ...", "slot GQ = the superseded GQ_CERT_V005 ...", "slot identity_comparator = the superseded c2v004 ..."',
  'evidence': {'registry_refused_at_load': case([c for c in cases_v2 if c.startswith('a producer registry r12 refuses at load')][0]),
               'gq_v005': case('slot GQ = the superseded GQ_CERT_V005 fbceefe6 (A86; not in registry C3V009 gate_records.GQ)'),
               'comparator_c2v004': case('slot identity_comparator = the superseded c2v004 e3d153b6 (not registry C3V009 identity_comparators) passes tool 3')}},
 {'id': 'C-05', 'severity': 'SHOULD_FIX', 'label': 'TESTED (tool 3) / FORMAL (B8 check)',
  'claim': ('Launch entry identity (D-04, SRR[10]). Tool 3 and the B8 admission check accept any BUILD_V007-allowlisted source as the launcher or the '
            'guard. TESTED: a bound plan whose launcher is aggregate_records_cx1v008.py, an allowlisted producer, with a matching command and '
            'admission_entry, passes tool 3. The B8 check accepts it too, by code (build_seal_record L417-421). SRR[10] needs the BUILD_V007 launcher and '
            'guard named exactly, and prereg r5 names them: launcher 861bba68 and guard 294cb776 '
            '(launch_packet.named_candidates_verified_from_bytes.build_v007_check_at_r5_generation). Fix: require plan.launcher and plan.guard to equal '
            'those two pins.'),
  'reproduction': RUNF + 'test_c4chk_v2.py ; case "a bound plan whose launcher is aggregate_records_cx1v008.py ..."',
  'evidence': {'launcher_swapped': case('a bound plan whose launcher is aggregate_records_cx1v008.py (an allowlisted producer, not the launcher) passes tool 3')}},
 {'id': 'C-06', 'severity': 'SHOULD_FIX', 'label': 'TESTED',
  'claim': ('Bound command, line 1. Only the last line of the bound command is compared with the binder\'s line. TESTED: a command file whose first line is a '
            'shell command, not the binder\'s "#" comment, passes tool 3 (the file never ran). The binder writes exactly two lines, a fixed comment and the '
            'command, so the whole file can be compared with the binder\'s output.'),
  'reproduction': RUNF + 'test_c4chk_v2.py ; case "a bound command whose first line is a shell command ..."',
  'evidence': {'line1': case("a bound command whose first line is a shell command (not the binder's comment) passes tool 3")}},
 {'id': 'C-07', 'severity': 'SHOULD_FIX', 'label': 'TESTED / FORMAL',
  'claim': ('Covered-later notes. Each --covered-later entry becomes the fixed sentence "<entry>: covers this entry for the prereg text of record (A81 '
            'RI-26)", with no disposition and no reason. TESTED: the CLI SEAL_RECORD carries that sentence for A102, A103 and A104. A102 and A104 move the '
            'compare slot from r12 to r13, while prereg r5\'s compare rule still names r12 as the final round, so the sentence is not an explicit '
            'no-change note (A81 RI-26). The builder half of rehearsal R-02 is still open. Fix: take a per-entry disposition and reason, as A99.3 and A104 '
            'require; or root issues a prereg r6 that integrates A102-A104.'),
  'reproduction': ('see ' + str(cli / 'SEAL_RECORD_CLI_C4CHK.json') + ' no_change_notes; command: the builder line in out/CLI_T4_BUILD.stderr.txt context (README B7 form, '
                   '--covered-later A102,A103,A104)'),
  'evidence': {'no_change_notes': json.loads((cli / 'SEAL_RECORD_CLI_C4CHK.json').read_bytes()).get('no_change_notes')}},
 {'id': 'C-08', 'severity': 'SHOULD_FIX', 'label': 'TESTED',
  'claim': ('NEW-item IMPL rule (B7). The NEW-item list must cite one compare IMPL that names the reviewed source sha in full. With r13 as the reviewed '
            'source (A104), the r11 IMPL 2d795028, which declares NEW-61 to NEW-81 (20 ids), refuses NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE. The r12 IMPL '
            'refuses too. Only the r13 IMPL 274f7049 passes, and it declares no NEW id. Item ids are never checked against any IMPL: NEW-999 passes, and '
            'NEW-071 next to NEW-71 is not a duplicate (TESTED). So the quoted list cannot be traced to the IMPL that declares the items (A81 RI-20). '
            'Fix: accept the IMPL lineage r11 -> r12 -> r13, the last naming the reviewed sha, and require the ids to equal the union of the declared '
            'NEW ids.'),
  'reproduction': RUNF + '../tests/new_items_impl_lineage_c4chk.py (out/NEW_ITEMS_IMPL_LINEAGE_C4CHK.stdout.txt); and test_c4chk_v2.py cases "R-04/B7 ..."',
  'evidence': json.loads((CHK / 'out/NEW_ITEMS_IMPL_LINEAGE_C4CHK.stdout.txt').read_bytes())},
 {'id': 'N-01', 'severity': 'NOTE', 'label': 'TESTED',
  'claim': ('D-01 holds. Every FIELDS_R12 per-kind M_s field is read, and 20 contradicting mutations refuse: DOUBLING float, string, bool, null, the '
            'ngc_half and ddo_half M_s, and per-K; LO echoes, the evidence block and a missing source; GQ rename, M_s_doubled, empty rosters and the '
            'top-level DDO/NGC keys; EPS_NGC; LO_NGC; and a galaxy NGC context. The real DOUBLING ea48ac2b gives exactly one field and no failure. A '
            'contradicting M_s under an unscanned key passes: gas_M_s_ddo (lower case), "gas.M_s", M_s_value, gas_M_s_source. r12 and r13 read only the '
            'per-kind fields, so this is internal-consistency coverage only.')},
 {'id': 'N-02', 'severity': 'NOTE', 'label': 'TESTED',
  'claim': ('BUILD allowlist parsing skips any line in the section that does not match its regex, so a 16th source line in upper-case hex passes as 15 '
            'sources. The guard admits only the config\'s entries (the parsed 15), so admission is not affected. Optional: refuse unparsed non-blank lines '
            'inside the section.')},
 {'id': 'N-03', 'severity': 'NOTE', 'label': 'TESTED',
  'claim': ('The bound plan is not compared with its template: a plan with two calls\' specs swapped, template_pin still V011, passes tool 3. A81 RI-25 '
            '(and r5\'s launch rule) make template equality optional. The README wording "bound from the template the prereg names" rests only on the '
            'declared template_pin.')},
 {'id': 'N-04', 'severity': 'NOTE', 'label': 'TESTED',
  'claim': ('The builder never reads B6 statuses or completeness. A GATES_ONLY body showing DOUBLING and B2 FAIL, a VALIDITY body with C5H valid_all false, '
            'and a body with a single gate entry each yield a SEAL_RECORD. SRR[0] asks only that the output go into the record, so the reading is root\'s. '
            'A summary of non-PASS gates in the record would help.')},
 {'id': 'N-05', 'severity': 'NOTE', 'label': 'TESTED',
  'claim': ('The check-record text fallback (NEW-73 in r12/r13) admits two FAIL-looking records that name the driver: a prose record ("verdict FAIL (the '
            'PASS criteria were not met)") and a truncated JSON with duplicate verdict keys. r12, r13 and tools 3/5 all admit them, and tool 5 prints a '
            'driver BUILD record around them. The A102 hardening covers JSON-parseable records only. r13 refuses the big-integer duplicate-key record that '
            'r12 admits. CHECK.md 89a6de88 is root-confirmed, so the exposure is low.'),
  'evidence': json.loads((ab1 / 'AB1_RESULTS_C4CHK.json').read_bytes())},
 {'id': 'N-06', 'severity': 'NOTE', 'label': 'FORMAL', 'claim': 'Raw successor custody: the evidence pins are optional, and a custody JSON with none passes. The check is root\'s (A59), so this is by design.'},
 {'id': 'N-07', 'severity': 'NOTE', 'label': 'TESTED',
  'claim': ('v001 regression: all 40 v001 cases hold under v002 on my own r5-based base, as 41 checks (T1 9, T2 11, T3 16, T4 3, integration 2). The one '
            'changed expectation is the one the builder names: r6 with an empty cache directory now refuses DRIVER_BUILD_NOT_THE_BRANCH, with no CACHE '
            'code.')},
 {'id': 'N-08', 'severity': 'NOTE', 'label': 'TESTED',
  'claim': ('r13 compatibility (the builder\'s open item): tools v002 r2 run unchanged with r13 f5adfd11 (the compare of record, A104) as the reviewed '
            'source. My harness gives 153/154; the only miss is the expected setup check, because r5 names r12. Tool 5\'s bytes equal the r12 ones '
            '(25b4ff69). The CLI chain passes. The README pipeline writes bytes whose sha equals the printed one, also under LC_ALL=C.')},
 {'id': 'N-09', 'severity': 'NOTE', 'label': 'FORMAL',
  'claim': ('Prereg r5\'s compare rule names r12 4bd7b262 as the final round, but A104 makes r13 the compare slot. Slot values are free, so tools 3/4 '
            'accept either round. Root needs a prereg r6 or an explicit seal-record note (see C-07).')},
 {'id': 'N-10', 'severity': 'NOTE', 'label': 'TESTED / FORMAL',
  'claim': ('The builder\'s deliverables re-verified from bytes: all 21 listed shas match, and its HASHES.txt is 528/528. The builder suite runs 148/148 '
            'from byte copies under my own fence (NEW 96, PORT 39, PORT_CHANGED 1, REAL 12). Its fence c993d34c differs from f813c430 only by the two '
            'read-only exceptions (diff read, FORMAL). My independent fence 3d9d6925 gives 8/8 selftest and 21/21 exception probes. BLOCKED was [] in '
            'every run here and in the builder\'s captures. The copied blinding constants (_RE_NUMBER, ALLOWED_NUMBER_TOKENS, _RE_HEX64) equal r12\'s and '
            'r13\'s. r12/r13 import-time code is definitions, constants, re.compile and math.sqrt (AST), and no function the tools call reaches the C5H '
            'stat or interlock helpers (call graph, FORMAL).')},
 {'id': 'N-11', 'severity': 'NOTE', 'label': 'process (self-reported)',
  'claim': ('Process. At about 21:47Z one echo line starting with "=" tripped zsh =-expansion (rule 6); it errored and wrote nothing. At about 21:40Z one '
            'temp file was written outside my folder: the session scratchpad claimed_shas.txt, holding the builder\'s listed paths and shas. CLI captures '
            'were created by shell redirection to new paths, and nothing was overwritten (noclobber from about 22:18Z). Harness v1 was never run. No '
            'compare CLI, no --validity-only, no launch, no runs_ext, UVT_* or C5H path and no target data were touched, and there was no recursive '
            'content search. The seal tools v003 folder (in progress, A103) was listed by name only and not reviewed.')},
]
OPEN = ['A104 D-05: the successor (v003) re-hashes every cited section (A47 onward) against prereg r5\'s pinned read copy 70a48f51 and takes revised | '
        'no_change_after_change (changed_text present in new, absent in old, plus reason) per changed entry (C-01).',
        'Prereg r6, or explicit per-entry notes the builder can carry, for A102-A104, which move the compare slot to r13 while r5\'s text names r12 (C-07, N-09).',
        'Until C-03, C-04 and C-05 are fixed, root checks by hand that the B6 gates\' record_sha256 equal the slot records, that the slot records and '
        'comparator are in the pinned registry, and that the plan\'s launcher and guard are 861bba68 and 294cb776.',
        'UNTESTED here (root-only or not yet existing): the real B6 bodies (--gates-only, and --validity-only --case C5H, with the sealed compare); the '
        'frozen copy at path_to_be; the real CASCADE_MAP_R5_ADDENDUM (GAP-18); the real B7 inputs; and the text-of-record ruling.',
        'Seal tools v003 is being built (seal_tools_v003/, A103: Codex3 keeps its delta); these findings are inputs for it.']
summary = {
 'schema': 'UNT_V007_SEAL_TOOLS_V002_CHECK_C4CHK', 'lane': 'Claude4 helper (independent check, dispatch 0621 / A99 item 4)',
 'utc_written': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
 'object': {'tools_r2': {n: sha(CA / 'v007_final_prereg_c4/seal_tools_v002/r2' / n) for n in ('seal_common_c4v002.py', 'check_frozen_addendum_c4v002.py',
                         'check_sealed_compare_c4v002.py', 'check_slot_fill_c4v002.py', 'build_seal_record_c4v002.py', 'print_driver_build_record_c4v002.py')},
            'builder_results': pin(CA / 'v007_final_prereg_c4/seal_tools_v002/RESULTS_SEAL_TOOLS_C4V002.json'),
            'builder_readme': pin(CA / 'v007_final_prereg_c4/seal_tools_v002/README_SEAL_TOOLS.md')},
 'verdict': 'CONFIRMED_WITH_FINDINGS',
 'verdict_text': ('The v002 r2 fixes hold as built and tested: D-01, D-04 (case block and CMA), D-07, D-10, R-04 (form), R-10, the BUILD_V007 set and '
                  'A99.3 (r5 table rows). One BLOCKING item remains, new since the build (A104 D-05), plus 7 SHOULD_FIX gaps (C-02 to C-08) and notes.'),
 'rulings_read': {'V005_copy_1': pin(CHK / 'addendum_read/V005_ADDENDUM_READ_COPY_1_C4ST2CHK.md'), 'V005_copy_2': pin(CHK / 'addendum_read/V005_ADDENDUM_READ_COPY_2_C4ST2CHK.md'),
                  'entries': 'A47-A104 (A47-A102 from copy 1, A103-A104 from copy 2)'},
 'inputs': {k: pin(v) for k, v in {'prereg_r5': CA / 'v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json',
            'case_block': CA / 'v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
            'compare_r12': CA / 'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py', 'compare_r13': CA / 'v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py',
            'FIELDS_R12': CA / 'v007_compare_c2/r12/FIELDS_R12_CX3V002.md', 'IMPL_R12': CA / 'v007_compare_c2/r12/COMPARE_V007_IMPL_R12.md',
            'BUILD_V007': CA / 'v007_launch_packet_cx1/BUILD_V007.md', 'DOUBLING': CA / 'producer_registry_c3/out/DOUBLING_MERGED_C3V001.json',
            'registry_C3V009': CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json', 'B2_C3V003': CA / 'gate_b2_c3/out/B2_GATE_RECORD_C3V003.json',
            'fence_v001_source': CA / 'review_launch_packet_0559_c4/tools/fence_c4v001.py'}.items()},
 'fence': {'fence_c4v001_copy': pin(CHK / 'tools/fence_c4v001.py'), 'fence_c4v002': pin(CHK / 'tools/fence_c4v002.py'), 'diff': pin(CHK / 'out/FENCE_C4V001_TO_C4V002_C4CHK.diff'),
           'exceptions': ['(a) uvt_*.py source modules (lowercase uvt_ basename, .py, no uvt_* directory component) outside both runs_ext roots; lifts only the UVT-component rule',
                          '(b) CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md, literal and resolved path; lifts only the NGC3198 rule'],
           'runner': pin(CHK / 'tools/run_fenced_c4chk.py'), 'blocked_lists': blocked},
 'test_runs': {'builder_suite_under_my_fence': {'run': str(bs), 'passed': r_bs['passed'], 'total': r_bs['total'], 'by_tag': r_bs['by_tag']},
               'harness_v2_r12': {'run': str(v2), 'harness': pin(CHK / 'tests/test_c4chk_v2.py'), 'passed': r_v2['passed'], 'total': r_v2['total'], 'by_tag': r_v2['by_tag'],
                                  'open_V005_sha': r_v2['open_V005_sha_start'], 'command': RUNF + 'test_c4chk_v2.py'},
               'harness_v3_r13': {'run': str(v3), 'harness': pin(CHK / 'tests/test_c4chk_v3_r13.py'), 'passed': r_v3['passed'], 'total': r_v3['total'], 'by_tag': r_v3['by_tag'],
                                  'not_ok': [r['case'] for r in r_v3['results'] if not r['ok']]},
               'cli_base_r13': {'run': str(cli), 'seal_record': pin(cli / 'SEAL_RECORD_CLI_C4CHK.json')},
               'gap_probes_confirmed': [r['case'] for r in r_v2['results'] if r['tag'] == 'GAP_PROBE' and r['ok']]},
 'findings': F, 'open_items': OPEN,
 'labels': 'TESTED = run or read from bytes here; FORMAL = follows from code or text read here; UNTESTED = not checked here',
 'note': 'The report is this JSON plus the structured output: the harness refuses report .md files from subagents.'}
out = CHK / 'RESULTS_SEAL_TOOLS_V002_CHECK_C4CHK.json'
text = json.dumps(summary, indent=1, ensure_ascii=False) + '\n'
if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
    print('DRY_RUN_OK', len(text), hashlib.sha256(text.encode()).hexdigest()); sys.exit(0)
with open(out, 'x', encoding='utf-8') as f:
    f.write(text)
print('WROTE', out, sha(out))
