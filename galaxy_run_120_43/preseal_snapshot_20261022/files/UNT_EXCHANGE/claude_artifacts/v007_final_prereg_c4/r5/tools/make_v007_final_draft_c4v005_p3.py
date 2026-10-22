# Claude4 r5 helper (dispatch 0621, A99), revision r5: successor of make_v007_final_draft_c4v004 (r4 e3b6b5b2). Reads r4 and every pinned
# input from bytes (a missing file or a sha prefix that differs refuses), reads the open V005 addendum once from bytes, keeps a byte copy,
# and builds the A99.3 entry table (every entry from A82 to the newest present: "revised here" with the clauses, or "no change, because";
# each with its section sha256 from bytes). Refuses an entry without a row. Binds binding_inputs.case_block (A99.2) and the launch-packet
# BUILD of record BUILD_V007 (A99.1): filled from bytes when found by name, else the literal PENDING_BUILD_V007 (never a guessed sha).
# Every clause edit is logged with its trace (gap / defect / ruling). Seal slots stay PENDING except where a ruling fixes them. No overwrite.
# Usage: TS=$(date -u +%Y-%m-%dT%H:%M:%SZ) [OUT_DIR=...] [BUILD_V007_PATH=...] python3 -I -B make_v007_final_draft_c4v005.py
import copy, hashlib, json, os, re
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE'); CA = EX / 'claude_artifacts'; PKT = CA / 'v007_launch_packet_cx1'
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
R5 = CA / 'v007_final_prereg_c4' / 'r5'
R4 = CA / 'v007_final_prereg_c4/r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json'
R4_SHA = 'e3b6b5b2ba265f54d15381f358913dd3ea931761aaa649c98a7583f58f1b7cf8'
V005 = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
BUILD_HEADER = '## Supported runtime entry allowlist'
PENDING_BUILD = 'PENDING_BUILD_V007'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin(p, prefix=None):
    p = Path(p)
    if not p.is_file():
        raise SystemExit('missing ' + str(p))
    h = sha(p)
    if prefix and not h.startswith(prefix):
        raise SystemExit('pin prefix %s != %s for %s' % (prefix, h[:8], p))
    return {'path': str(p), 'sha256': h}


def strict(raw):
    def hook(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                raise SystemExit('duplicate JSON key %r' % k)
            out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=hook)


def cl(text, *sources):
    return {'text': text, 'sources': list(sources)}


def norm(c):
    """clause names: 'x.2' -> 'x[2]' (list indices), as the rows write them."""
    return re.sub(r'\.(\d+)(?=\.|$)', r'[\1]', c)


def expand(c):
    """a logged clause name may combine names ('a.b / c', 'a.X, Y'); bare names inherit the first name's prefix."""
    parts = [q for part in c.split(' / ') for q in part.split(', ')]
    head = parts[0]
    pre = head.rsplit('.', 1)[0] + '.' if '.' in head else ''
    keep = ('status', 'assembly', 'decision_pins_pending_at_seal', 'cites_by_name')
    return [norm(q if ('.' in q or not pre or q.startswith(keep)) else pre + q) for q in parts]


def sections(b):
    """V005 entry sections: from the first byte of a heading line '## A<n>:' up to, not including, the first byte of the next line that
    begins with '## ' (or the end of the file)."""
    starts = [m.start() for m in re.finditer(rb'(?m)^## ', b)]
    out = {}
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(b)
        head = b[s:b.index(b'\n', s)].decode('utf-8')
        m = re.match(r'## (A\d+):', head)
        if m:
            if m.group(1) in out:
                raise SystemExit('duplicate entry heading ' + m.group(1))
            out[m.group(1)] = (head, b[s:e])
    return out


# ---------------------------------------------------------------------------------------- the A99.3 entry table rows (A82 to the newest)
RH, NC = 'REVISED_HERE', 'NO_CHANGE'
ROWS = {
    'A82': (RH, ['root_items.RI-27', 'seal_slots.frozen_addendum', 'seal_slots.compare', 'seal_record_requirements[2]', 'seal_record_requirements[4]',
                 'seal_record_requirements[8]'],
            'A82 ruled RI-27 as drafted in r4 and said no r5 was needed for it. r5 records the ruling (RI-27 resolved; the citations of the draft '
            'become A82) and A82\'s rule that root writes nothing more to the open V005 file once the frozen copy exists (later entries go in a V006 '
            'addendum).'),
    'A83': (RH, ['seal_slots.compare', 'seal_slots.identity_comparator', 'SEAL_CHECKLIST_R5 A1, A2'],
            'A83 stopped compare r11 at its freeze, before its recheck lenses ran, and made Claude3 and Codex2 the rechecks (reviews) of record; it '
            'stopped the c2v007 own-check workflow and made Codex2\'s review the check of record (rehearsal R-02). Both r4 slot rules named the '
            'stopped checks; r5 names the checks of record.'),
    'A84': (NC, [], 'no change, because A84 schedules speculative r6 identity runs, concurrent lane work and Codex3\'s step-5 readiness; it changes '
                    'no rule of this text, and A96 later made r6 moot (r5\'s r6 edits are traced to A96).'),
    'A85': (NC, [], 'no change, because A85.2-A85.4 (core priority, internal-volume step-2 outputs, caffeinate) are RUNBOOK root steps at launch that '
                    'change no sealed byte (A85), now carried by BUILD_V007 (V6-S2, A99.1); A85.1 (the parallel tail build) adopts nothing before the '
                    'seal under the A72 rule and is moot for V007 (A96).'),
    'A86': (RH, ['gates_before_any_T_result.GQ', 'seal_slots.certificates', 'seal_slots.compare', 'SEAL_CHECKLIST_R5 A7'],
            'A86.1 makes GQ_CERT_V006 (5a1b39f8) the GQ record of record (V005 fbceefe6 reads RECORD_DEFECT under A79.1, which stands); A86 makes '
            'Claude3 and Codex2 the r11 reviews of record. A86.2 (the open V005 path: no compare change), A86.3 (RI-24 fields only under r6: moot, '
            'A96), A86.4 (DOUBLING NGC K_big informational) and A86.5 (NEW-71 to NEW-81 under RI-10, already seal_record_requirements[5]) need no text.'),
    'A87': (RH, ['binding_inputs.gate_b3_record_A87', 'binding_inputs.gate_b3_rule', 'gates_before_any_T_result.DOUBLING', 'gates_before_any_T_result.LO_NGC',
                 'seal_slots.certificates', 'seal_slots.launch_packet', 'seal_slots.producer_registry', 'SEAL_CHECKLIST_R5 A7, A8, A9, DONE'],
            'A87 names the missing pre-seal records of record and their owners: the merged DOUBLING record (ea48ac2b), the B3 FIELDS-shape JSON (the '
            '465cb3c3 Markdown is the human report), LO_NGC_CERT_V002 (33bc2190) as the LO_NGC record of record, the B0-family records, and the '
            'post-seal producers in a new BUILD.'),
    'A88': (RH, ['tests.SR_K', 'gates_before_any_T_result.after_seal_marker_policy', 'run_list.replays', 'seal_slots.producer_registry', 'SEAL_CHECKLIST_R5 A9'],
            'A88 moves SR_K after the seal (produced by the sealed pinned producers before any T-run output is read; registered by producer pins with '
            'PRODUCED_AFTER_THE_SEAL), amending A79 NEW-61 for SR_K only. r4 required the SR_K record before the seal.'),
    'A89': (RH, ['run_list.cpu_hours_estimate_UNTESTED', 'fixed_across_all_cases.production_tail.tail_table_cache', 'scope_untested'],
            'A89 measures the KHI cost (7.84-13.86 h solo; the 27.84 h preview is superseded) and makes A72(c) concrete (r6 only with no seal '
            'delay); A96 then applies it.'),
    'A90': (RH, ['seal_slots.compare', 'gates_before_any_T_result.LO_NGC', 'seal_slots.certificates'],
            'A90 records Codex2\'s blocking r11 item (r12 follows) and makes LO_NGC_K32_CERT_V001 (07745bbf) the NGC N-test record while V007 keeps '
            'LO_NGC V002. Its NGC N-test outcome (N_FAIL_N1 on TRUNCATION_SHAPE only; route A/B OPEN under A66) and its step-5 open item change no '
            'registered N-test, threshold or consequence of this text.'),
    'A91': (RH, ['seal_slots.compare', 'seal_slots.identity_comparator'],
            'A91 fixes the r12 scope (0459, 0462\'s should-fix, A88 SR_K; the RI-24 fields only under r6) and its delta reviews (Codex2, Claude3; 0 '
            'blocking each), and makes identity-digest presence a requirement of c2v007r2.'),
    'A92': (RH, ['seal_slots.identity_comparator', 'seal_slots.identity_gate_records', 'run_list.DDO_gates', 'gates_before_any_T_result.B1_Z2',
                 'gates_before_any_T_result.Z2_OFF_RO1', 'gates_before_any_T_result.B0prime_RERUN', 'SEAL_CHECKLIST_R5 A2, A5'],
            'A92 rules c2v007r2 (052da0fe) the identity-comparator slot and the R5_V001 records (B1 83e7b067, B1_OFF 3b9ad402, B0prime_RERUN e33af53d) '
            'the identity records of record for driver r5.'),
    'A93': (RH, ['not_v007_text_scope'],
            'A93 accepts NGC cx3r007 and makes SPEC_REGISTRY_CX3R007 (cd30429c) the step-5 launch registry, retiring 3c42ca07. The NGC launch path '
            'stays outside this text; r5 corrects the registry named in the scope note.'),
    'A94': (RH, ['gates_before_any_T_result.B2'],
            'A94 rules that B2 follows its controlling text exactly: full static rows with the registered gas rule, le3 for every case, the named '
            'statistic, the basis stated, interpretations listed as ROOT_ITEMs.'),
    'A95': (NC, [], 'no change, because A95 makes taskpolicy -b preferred rather than required in lane work and limits six-thread Accelerate to '
                    'non-production measurement (production stays single-thread BLAS); this text has no clause on lane process priority or BLAS '
                    'threading, and A85.2\'s step-2 rule stays a RUNBOOK root step.'),
    'A96': (RH, ['seal_slots.driver', 'seal_slots.cache_directory_r6_only', 'seal_slots.compare', 'fixed_across_all_cases.production_tail.tail_table_cache',
                 'fixed_across_all_cases.production_tail.memory_guard', 'binding_inputs.successors', 'binding_inputs.ro1_role_table',
                 'gates_before_any_T_result.B0prime_RERUN', 'gates_before_any_T_result.Z2_OFF_RO1', 'run_list.DDO_gates', 'run_list.DDO_tests',
                 'seal_record_requirements[4]', 'seal_record_requirements[8]', 'outcome_branch_tests_required', 'scope_untested', 'root_items.RI-24'],
            'A96: V007 seals on driver v010 r5 (b5cc62af); r6 is deferred and unused; A81 RI-24 and the conditional cache slot are moot; compare r12 '
            'cx3v002 (4bd7b262) is frozen, with Claude3\'s and Codex2\'s delta reviews of record.'),
    'A97': (RH, ['gates_before_any_T_result.B2', 'SEAL_CHECKLIST_R5 A13'],
            'A97 fixes, before the decomposition, the rule by which B2\'s sanity clause is read ((a) the like-for-like reference with the 0.05 '
            'unchanged, (b) fail, (c) C3R3 computed the same way or INCOMPLETE), and holds the seal for B2.'),
    'A98': (NC, [], 'no change, because A98\'s PAR-TB ruling concerns the NGC v011 successors (step 5) and its miss-reading prereg r3 item is on the '
                    'step-6 path; neither is V007 text.'),
    'A99': (RH, ['binding_inputs.case_block', 'binding_inputs.case_block_rule', 'seal_slots.launch_packet', 'seal_record_requirements[10]',
                 'seal_record_requirements[11]', 'run_list.limits', 'entries_after_A81', 'seal_slots.frozen_addendum', 'seal_slots.producer_registry',
                 'gates_before_any_T_result.after_seal_marker_policy', 'SEAL_CHECKLIST_R5 A11, A12, B1, B2a, B8'],
            'A99 (the rehearsal rulings): BUILD_V007 is the launch-packet BUILD of record (D-02); Claude4 builds the case block, pinned as '
            'binding_inputs.case_block (D-03); this entry table (item 3); seal tools v002 (item 4, not text); V6-N2 closed in r12 and BUILD_V007\'s '
            'post-seal producers in the registry (item 5); root writes nothing to V005 after the freeze (item 6).'),
    'A100': (RH, ['gates_before_any_T_result.B2', 'seal_record_requirements[12]', 'scope_untested', 'SEAL_CHECKLIST_R5 A13'],
             'A100 disposes B2 under A97(a): the like-for-like reference (ADV\'s method with production\'s continuum_v001 gas rule), the 0.05 '
             'unchanged, the values of record (reading (ii), P16: 0.0301 / 0.0356 / 0.0384 km/s), the disclosure block repeated in the seal record, '
             'and the limit that B2 does not prove shared physical correctness.'),
    'A101': (RH, ['binding_inputs.case_block_rule', 'gates_before_any_T_result.B2', 'seal_record_requirements[12]', 'seal_slots.producer_registry',
                  'SEAL_CHECKLIST_R5 A9, A11, A13'],
             'A101 makes B2_GATE_RECORD_C3V003 (915fbcda) the B2 record of record with its two documentation errata carried in the seal record, '
             'records Codex2 0507 PASS (zero findings) on the case block CASE_BLOCK_V007_C4V001 (76309ae3) pinned here, and makes registry V008 '
             '(f189cd3f) final pending V009 with BUILD_V007\'s producers. Its step-5 star-transform result (the A90 open item, closed) is outside '
             'this text.'),
}


def find_build_v007():
    env = os.environ.get('BUILD_V007_PATH')
    if env:
        return [Path(env)]
    cands = [PKT / 'BUILD_V007.md', CA / 'build_v007_closure_cx3' / 'BUILD_V007.md']
    return [p for p in cands if p.is_file()]


def main():
    ts = os.environ['TS']
    out = Path(os.environ['OUT_DIR']) if os.environ.get('OUT_DIR') else R5
    if sha(R4) != R4_SHA:
        raise SystemExit('r4 pin')
    doc = json.loads(R4.read_text())
    r4_companions = {n: pin(R4.parent / n, p) for n, p in (('SEAL_CHECKLIST_R4.md', '0d7eb429'), ('ROOT_ITEMS_R4.md', '07c86942'),
                                                            ('CLAUSE_SOURCE_MAP_R4.md', 'd684562d'), ('KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.md', 'f047b84d'),
                                                            ('DELTA_R3_R4.md', '38b733ec'))}
    # ---- the open V005 addendum, read once from bytes; a byte copy is kept with the outputs
    vb = V005.read_bytes()
    v005_observed = hashlib.sha256(vb).hexdigest()
    secs = sections(vb)
    nums = sorted(int(k[1:]) for k in secs)
    newest = 'A%d' % max(nums)
    later = ['A%d' % n for n in nums if n >= 82]
    missing_rows = [e for e in later if e not in ROWS]
    if missing_rows:
        raise SystemExit('entries without a row in the entry table (A99.3): %s' % missing_rows)
    extra_rows = [e for e in ROWS if e not in secs]
    if extra_rows:
        raise SystemExit('rows for entries not in the V005 bytes: %s' % extra_rows)
    reads = [pin(R5 / 'scratch' / 'V005_ADDENDUM_READ_COPY_1_C4R5.md', 'ff7980e8'), pin(R5 / 'scratch' / 'V005_ADDENDUM_READ_COPY_2_C4R5.md', '7f552858'),
             pin(R5 / 'scratch' / 'V005_ADDENDUM_READ_COPY_3_C4R5.md', '70a48f51')]
    # ---- pinned inputs (sha from bytes; prefixes pasted from shasum output)
    P = {}
    for k, p, pre in (
            ('dispatch_0621', EX / 'FROM_CODEX/0621_2026-10-18_claude4_codex1_codex3_claude3_A99.md', '7ab78e6a'),
            ('dispatch_0622', EX / 'FROM_CODEX/0622_2026-10-18_claude3_codex2_B2_disposed_A100.md', 'e6ae0c32'),
            ('dispatch_0602', EX / 'FROM_CODEX/0602_2026-10-18_claude4_build_v006_delta_and_seal_rehearsal.md', 'c19bce2f'),
            ('Claude4_0099', EX / 'FROM_CLAUDE4/0099_2026-10-18_done_0602_v006_delta_and_seal_rehearsal.md', 'b92cf2e8'),
            ('Claude4_0100', EX / 'FROM_CLAUDE4/0100_2026-10-18_ack_0621_A99_seal_path_builds.md', '2f35e1a4'),
            ('Claude3_0083', EX / 'FROM_CLAUDE3/0083_2026-10-18_r12-delta-FAIL-1-blocking-A-B1.md', '8fe311ba'),
            ('Claude3_0084', EX / 'FROM_CLAUDE3/0084_2026-10-18_B2-C3V003-PASS-registry-V008-final.md', '81689210'),
            ('Codex2_0485', EX / 'FROM_CODEX2/0485_2026-10-18_0614_r12_delta_finished_zero_blocking.md', 'f2bfc8a5'),
            ('Codex2_0503', EX / 'FROM_CODEX2/0503_2026-10-18_0622_b2_c3v003_delta_finished.md', '815d1c15'),
            ('Codex2_0507', EX / 'FROM_CODEX2/0507_2026-10-18_0621_case_block_static_review_finished.md', '22957c1f'),
            ('Codex3_0628', EX / 'FROM_CODEX3/0628_2026-10-18_dispatch0621_BUILD_V007_takeover_start.md', 'ca330cfb'),
            ('Codex1_0032', EX / 'FROM_CODEX1/0032_2026-10-18_gq91_pass_and_latest_rulings.md', '3e8c9fc9'),
            ('Codex1_0056', EX / 'FROM_CODEX1/0056_2026-10-18_ngc_k32_complete_n_fail_n1_a66_open.md', '4b67319d'),
            ('rehearsal_index', CA / 'seal_rehearsal_c4/INDEX_SEAL_REHEARSAL_C4V001.md', None),
            ('rehearsal_gaps_md', CA / 'seal_rehearsal_c4/run/GAPS_C4V001.md', '566b2066'),
            ('rehearsal_gaps_json', CA / 'seal_rehearsal_c4/run/GAPS_C4V001.json', 'eb9a0413'),
            ('rehearsal_refute', CA / 'seal_rehearsal_c4/refute/REFUTE.md', '7be3fb34'),
            ('rehearsal_driver_build_draft', CA / 'seal_rehearsal_c4/run/scratch/rehearsal_b/DRIVER_BUILD_R5_REHEARSAL_DRAFT_C4V001.json', '2a3e4308'),
            ('case_block', R5 / 'case_block' / 'CASE_BLOCK_V007_C4V001.json', '76309ae3'),
            ('case_block_build_record', R5 / 'out' / 'CASE_BLOCK_BUILD_C4V001.json', 'bcf560de'),
            ('case_block_draft_not_an_input', CA / 'tail_scheme_impl_c2/driver/out/CASE_BLOCK_V007_DRAFT_C2V001.json', '6bf4ce5a'),
            ('gq_ngc_91_ms96', CA / 'ngc_ntest_eval_cx/out/GQ_NGC_91_MS96_V001.json', 'be148bab'),
            ('lo_ngc_k32', CA / 'tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json', '07745bbf'),
            ('b3_record', CA / 'seal_records_c4/build/records/B3_RECORD_C4V001.json', '83c853b9'),
            ('b0_record', CA / 'seal_records_c4/build/records/B0_R5_RECORD_C4V001.json', 'c2cec35b'),
            ('b0prime_dry_record', CA / 'seal_records_c4/build/records/B0prime_DRY_R5_RECORD_C4V001.json', '7842d2a7'),
            ('b0_fa_record', CA / 'seal_records_c4/build/records/B0_FA_R5_RECORD_C4V001.json', '888488cd'),
            ('b2_record_c3v003', CA / 'gate_b2_c3/out/B2_GATE_RECORD_C3V003.json', '915fbcda'),
            ('b2_record_c3v002_superseded', CA / 'gate_b2_c3/out/B2_GATE_RECORD_C3V002.json', 'd4b41ffc'),
            ('registry_c3v008', CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V008.json', 'f189cd3f'),
            ('registry_c3v007', CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V007.json', '34bbfe40'),
            ('registry_c3v009', CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json', '32ddadcb'),
            ('validate_r12_c3v009_case_block_of_record', CA / 'producer_registry_c3/out/VALIDATE_R12_C3V009_CASEBLOCK_OF_RECORD.json', '537d1a42'),
            ('Claude3_0087', EX / 'FROM_CLAUDE3/0087_2026-10-18_registry-V009-BUILD_V007-producers-final.md', '0f99076e'),
            ('dispatch_0626', EX / 'FROM_CODEX/0626_2026-10-18_claude3_codex2_seal_assembly_prestage.md', 'c555ee94'),
            ('gq_v006', CA / 'producer_registry_c3/out/GQ_CERT_V006.json', '5a1b39f8'),
            ('gq_v005_superseded', CA / 'tail_scheme_impl_c2/certificates_v003/gates/GQ_CERT_V005_MS128.json', 'fbceefe6'),
            ('doubling_merged', CA / 'producer_registry_c3/out/DOUBLING_MERGED_C3V001.json', 'ea48ac2b'),
            ('lo_ngc_v002', CA / 'tail_scheme_impl_c2/certificates_v002/gates/LO_NGC_CERT_V002.json', '33bc2190'),
            ('comparator_c2v007r2', CA / 'tail_scheme_impl_c2/gates_v007/r2/run_identity_compare_c2v007.py', '052da0fe'),
            ('id_B1', CA / 'tail_scheme_impl_c2/gates_v007/r2/records/R5_V001/B1_R5_C2V007.json', '83e7b067'),
            ('id_B1_OFF', CA / 'tail_scheme_impl_c2/gates_v007/r2/records/R5_V001/B1_OFF_R5_C2V007.json', '3b9ad402'),
            ('id_B0prime_RERUN', CA / 'tail_scheme_impl_c2/gates_v007/r2/records/R5_V001/B0prime_RERUN_R5_C2V007.json', 'e33af53d'),
            ('r12_compare', CA / 'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py', '4bd7b262'),
            ('r12_selected', CA / 'v007_compare_c2/r12/SELECTED_R12_CX3V001.json', '91aa9747'),
            ('r12_fields', CA / 'v007_compare_c2/r12/FIELDS_R12_CX3V002.md', '5cc95a06'),
            ('r12_impl', CA / 'v007_compare_c2/r12/COMPARE_V007_IMPL_R12.md', 'ef0db32d'),
            ('r12_hashes', CA / 'v007_compare_c2/r12/HASHES.txt', '3eb2912d'),
            ('r11_compare_superseded', CA / 'v007_compare_c2/r11/kmax_tail_compare_c2v007_r11.py', 'a5d10cb1'),
            ('r12_review_Claude3', CA / 'review_v007_compare_c3/r12_review/REVIEW_V007_COMPARE_R12_C3V001.md', '65dd997f'),
            ('r12_review_Codex2', CA / 'review_v007_compare_final_cx2/r12/REVIEW_CX2V001.md', 'fb8ef4ca'),
            ('build_v006', PKT / 'BUILD_V006.md', 'fb9e6a4a'),
            ('build_v005_superseded', PKT / 'BUILD_V005.md', '46bc5b5d'),
            ('build_v006_review_Claude4', CA / 'review_launch_packet_v006_c4/REVIEW_LAUNCH_PACKET_V006_C4V001.md', 'd0d1c6e7'),
            ('spec_registry', PKT / 'SPEC_REGISTRY_R5_MS128_CX1V004.json', 'c7023846'),
            ('plan_template_v010', PKT / 'P128/LAUNCH_PLAN_V010.json', '26f1ebf9'),
            ('dry_run_record', PKT / 'DRY_R5_MS128_V004.json', 'ff60cd6b'),
            ('driver_r5', CA / 'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py', 'b5cc62af'),
            ('driver_r5_check_candidate', CA / 'tail_scheme_impl_c2/driver_r5/check/CHECK.md', '89a6de88'),
            ('fence_c4v002', R5 / 'tools' / 'fence_c4v002.py', '53078e39')):
        P[k] = pin(p, pre)
    cbr = strict(Path(P['case_block_build_record']['path']).read_bytes())
    if cbr.get('verdict') != 'CASE_BLOCK_VALID_UNDER_R12' or cbr['case_block']['sha256'] != P['case_block']['sha256'] or cbr.get('fail'):
        raise SystemExit('the case block build record does not read the pinned case block valid')
    reg = strict(Path(P['spec_registry']['path']).read_bytes())
    filled = {x['case']: x['filled'] for x in reg['specs']}
    # ---- BUILD_V007 (A99.1): from bytes when found by name; else PENDING_BUILD_V007
    bc = find_build_v007()
    if len(bc) > 1:
        raise SystemExit('more than one BUILD_V007 candidate: %s (root decides; set BUILD_V007_PATH)' % bc)
    bv7, bv7_check = None, {'state': PENDING_BUILD}
    if bc:
        bp = bc[0]
        bv7 = pin(bp)
        text = bp.read_bytes().decode('utf-8')
        try:
            sec = text.split(BUILD_HEADER + '\n', 1)[1].split('\n## ', 1)[0]
        except IndexError:
            raise SystemExit('BUILD_V007 has no allowlist section')
        allow = re.findall(r'^([0-9a-f]{64})  (/\S+\.py)$', sec, re.M)
        if len(allow) != 15 or len({p for _, p in allow}) != 15:
            raise SystemExit('BUILD_V007 allowlist is not exactly 15 distinct sources (V6-S3): %d' % len(allow))
        bad = [p for h, p in allow if sha(p) != h]
        if bad:
            raise SystemExit('BUILD_V007 allowlist entries whose bytes differ: %s' % bad)
        amap = {p: h for h, p in allow}
        lines = re.findall(r'^([0-9a-f]{64})  (/\S+)$', text, re.M)

        def one(rx, what):
            hit = sorted({(h, p) for h, p in lines if re.search(rx, p)})
            if len(hit) != 1:
                raise SystemExit('BUILD_V007 names %d %s files' % (len(hit), what))
            h, p = hit[0]
            if sha(p) != h:
                raise SystemExit('BUILD_V007 %s bytes differ' % what)
            return {'path': p, 'sha256': h}
        named = {'template_plan': one(r'/P128/LAUNCH_PLAN_V\d+[^/]*\.json$', 'template plan'),
                 'template_command': one(r'/P128/LAUNCH_COMMAND_V\d+[^/]*\.txt$', 'template command'),
                 'cases_manifest_template': one(r'/P128/CASES_MANIFEST_TEMPLATE_V\d+[^/]*\.json$', 'cases manifest template'),
                 'runbook': one(r'/RUNBOOK_V\d+[^/]*\.md$', 'runbook'),
                 'admission_format': one(r'/ROOT_SEAL_ADMISSION_FORMAT_V\d+[^/]*\.md$', 'admission format'),
                 'binder': one(r'/bind_sealed_launch_plan_[^/]*\.py$', 'binder'),
                 'allowlist_file': one(r'/ALLOWLIST_DRAFT_V\d+[^/]*\.txt$', 'allowlist file'),
                 'producer_index': one(r'/PRODUCER_INDEX_V\d+[^/]*\.json$', 'producer index'),
                 'predecessor_BUILD_V006': one(r'/BUILD_V006\.md$', 'BUILD_V006')}
        if named['predecessor_BUILD_V006'] != P['build_v006']:
            raise SystemExit('BUILD_V007 does not pin BUILD_V006 fb9e6a4a as its predecessor')
        plan = strict(Path(named['template_plan']['path']).read_bytes())
        lg = {k: plan.get(k) for k in ('launcher', 'guard')}
        for k, v in lg.items():
            if not (isinstance(v, dict) and amap.get(v.get('path')) == v.get('sha256')):
                raise SystemExit('BUILD_V007 template %s is not a supported BUILD_V007 source' % k)
        calls = {c['case']: c['spec'] for c in plan['calls']}
        if calls != filled or len(plan['calls']) != 10:
            raise SystemExit('BUILD_V007 template does not launch exactly the ten FILLED specs of the case block')
        if plan['driver'] != P['driver_r5'] or plan['registry'] != P['spec_registry']:
            raise SystemExit('BUILD_V007 template driver or registry is not r5 / c7023846')
        old = strict(Path(P['plan_template_v010']['path']).read_bytes())

        def leaves(o, p=''):
            if isinstance(o, dict):
                r = {}
                for k, v in o.items():
                    r.update(leaves(v, p + '/' + str(k)))
                return r or {p: '{}'}
            if isinstance(o, list):
                r = {}
                for i, v in enumerate(o):
                    r.update(leaves(v, p + '/' + str(i)))
                return r or {p: '[]'}
            return {p: json.dumps(o)}
        la, lb = leaves(old), leaves(plan)
        diff = sorted(k for k in set(la) | set(lb) if la.get(k) != lb.get(k))
        nonstr = [k for k in diff if not all(x is not None and x.startswith('"') for x in (la.get(k), lb.get(k)))]
        bv7_check = {'state': 'FILLED_FROM_BYTES', 'allowlist_sources': 15, 'allowlist_bytes_verified': True, 'named': named,
                     'launcher': lg['launcher'], 'guard': lg['guard'],
                     'template_launches_the_ten_FILLED_specs_of_the_case_block': True,
                     'template_vs_V010': {'differing_leaves': len(diff), 'non_string_leaves': nonstr, 'order_identical': plan['order'] == old['order']},
                     'review_state': 'Claude4 delta check PENDING; Claude2 adoption PENDING (A99.1)'}
        if nonstr:
            raise SystemExit('BUILD_V007 template differs from V010 in non-string leaves: %s' % nonstr[:5])
    changes = []

    def node(path):
        d = doc
        for k in path:
            d = d[k]
        return d

    def log(clause, kind, srcs, trace, why):
        if not trace:
            raise SystemExit('untraced change ' + clause)
        changes.append({'clause': clause, 'kind': kind, 'added_sources': list(srcs), 'trace': list(trace), 'why': why})

    def addsrc(c, add):
        for s in add:
            if s not in c['sources']:
                c['sources'].append(s)

    def rewrite(path, text, add, trace, why, expect_prefix=None):
        c = node(path)
        if expect_prefix and not c['text'].startswith(expect_prefix):
            raise SystemExit('r4 text of %s does not start as expected' % (path,))
        c['text'] = text
        addsrc(c, add)
        log('.'.join(str(x) for x in path), 'rewritten', add, trace, why)

    def rep(path, old, new, add, trace, why):
        c = node(path)
        n = c['text'].count(old)
        if n != 1:
            raise SystemExit('expected one %r in %s, found %d' % (old[:50], path, n))
        c['text'] = c['text'].replace(old, new)
        addsrc(c, add)
        log('.'.join(str(x) for x in path), 'revised', add, trace, why)

    def app(path, more, add, trace, why):
        c = node(path)
        c['text'] = c['text'].rstrip() + ' ' + more
        addsrc(c, add)
        log('.'.join(str(x) for x in path), 'extended', add, trace, why)

    def swap_src(c, old, new):
        c['sources'] = [new if s == old else s for s in c['sources']]

    bi, fx, pt, gt, sl, sr = doc['binding_inputs'], doc['fixed_across_all_cases'], doc['fixed_across_all_cases']['production_tail'], \
        doc['gates_before_any_T_result'], doc['seal_slots'], doc['seal_record_requirements']
    cbp = P['case_block']['sha256']
    b7 = bv7['sha256'] if bv7 else None
    b7txt = ('BUILD_V007 (%s, filled from bytes; its Claude4 delta check and Claude2 adoption are pending, A99.1)' % b7) if bv7 else \
        'BUILD_V007 (path and sha PENDING_BUILD_V007 until it lands; filled from bytes then)'

    # ================================================================= binding inputs
    bi['case_block'] = {'path': P['case_block']['path'], 'sha256': cbp}
    log('binding_inputs.case_block', 'new pin', ['A99.2', 'A101'], ['A99.2', 'A101', 'D-03', 'GAP-03', 'R-03'],
        'the compare reads the case block in sealed mode only from binding_inputs.case_block {path, sha256} (r12 L5706)')
    bi['case_block_rule'] = cl(
        'binding_inputs.case_block is the V007 case block of record, CASE_BLOCK_V007_C4V001 (schema UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V003; built by Claude4 '
        'under A99.2; Codex2 0507: PASS, zero findings; A101). In sealed mode the compare reads the case block only from this key (r12 cx3v002 L5706) and '
        'refuses CASE_BLOCK_ABSENT without it (rehearsal D-03, R-03). For each of the ten T-cases it registers the /numerics, whole, of the driver v010 r5 '
        'dry run of its FILLED P128/M_s 128 spec (DRY_R5_MS128_V004 ff60cd6b over SPEC_REGISTRY_R5_MS128_CX1V004 c7023846, both byte-pinned in BUILD_V005), '
        'its grid and truncation, tail and ro1_required true, drivers_allowed [v010 r5 b5cc62af] and the pinned-library uv_tail_config_sha256, which equals '
        'the driver-side normalized sha of each dry run; and C5H as the registered call 60b46130 on v009-EXT 999331af, with nothing else registered. '
        'route_a_mode is parallel8 (A47 I4; A51). key_equivalence_map is []: no /numerics key of C4T-D5 outside composite_grid_spec and uv_tail differs '
        'from the C5H reference (A48 AMB-13). It reads valid under r12\'s own validate_case_block, in-process, both in memory and from the written bytes, '
        'and 22 must-refuse mutations refuse (TESTED; out/CASE_BLOCK_BUILD_C4V001 bcf560de). It is target-free spec metadata. The on-disk draft '
        'CASE_BLOCK_V007_DRAFT_C2V001 (6bf4ce5a) is not a V007 input: schema C2V002, retired labels C4T-K16/C4T-K64, v010 r3 drivers, K_big 32, gas M_s 64, '
        'PENDING tail shas, and a C4T-D5 entry marked not buildable.',
        'A99.2', 'A101', 'A48 AMB-13', 'A54 S8', 'A47 I4', 'A51', 'A62 (Claude3 0059)', 'A72 (Claude3 0065)', 'rehearsal D-03', 'R-03', 'GAP-03')
    log('binding_inputs.case_block_rule', 'new', ['A99.2', 'A101'], ['A99.2', 'A101', 'D-03', 'GAP-03', 'R-03'], 'what the pinned case block is and how it was built')
    bi['gate_b3_record_A87'] = {'path': P['b3_record']['path'], 'sha256': P['b3_record']['sha256']}
    bi['gate_b3_rule'] = cl('The B3 record of record is the FIELDS-shape JSON B3_RECORD_C4V001 (binding_inputs.gate_b3_record_A87, 83c853b9; Claude4 0598; '
                            'registered from C3V007 and in C3V008, A101). GATE_B3_C4_V002.md (binding_inputs.gate_b3_final, 465cb3c3) is the human report of '
                            'the same final PASS, not the record (A87).', 'A87', 'A101', 'R1 B3')
    log('binding_inputs.gate_b3_record_A87 / gate_b3_rule', 'new', ['A87', 'A101'], ['A87', 'GAP-02 (A87 evidence)', 'REFUTE DONE row'],
        'A87: the B3 record of record is the FIELDS-shape JSON; the Markdown is the human report')
    rewrite(('binding_inputs', 'successors'),
            'Every route-A and route-B successor, worker, facade, controller, binding and the reference successor exactly as pinned by the build record of the '
            'driver in the driver slot, which is v010 r5 (A96): tail_scheme_impl_c2/driver_r5/ BUILD and CASCADE_MAP_R5 plus the immutable '
            'CASCADE_MAP_R5_ADDENDUM required by A69 before the seal. The tail module is the one r5 pins: the TAIL_MEMORY_CAP_BYTES successor of A55.2. r6 is '
            'deferred and is not a V007 driver (A96: its partial bytes in driver_r6/ are unfinished and unused; A72\'s r6 branch and A81 RI-24 are moot for V007).',
            ['A96'], ['A96', 'GAP-19'], 'V007 seals on r5 (A96)', expect_prefix='Every route-A and route-B successor')
    rep(('binding_inputs', 'ro1_role_table'), 'These are the r5 values; under r6 the table is re-read from r6\'s cascade map (pin-only) before the seal.',
        'These are the r5 values, and V007 seals on r5 (A96), so they are the table.', ['A96'], ['A96'], 'r6 moot (A96)')
    if bv7:
        more = ('Their case block of record is binding_inputs.case_block (A99.2, A101). BUILD_V006 left the r5 templates, caps and order unchanged; BUILD_V007\'s '
                'selected template %s (%s) carries the same ten FILLED spec pins, order, driver and registry as V010 and differs from it only in %d output-path '
                'string leaves (V6-S2; TESTED from bytes at r5 generation).' % (Path(bv7_check['named']['template_plan']['path']).name,
                                                                                 bv7_check['named']['template_plan']['sha256'][:8], bv7_check['template_vs_V010']['differing_leaves']))
    else:
        more = ('Their case block of record is binding_inputs.case_block (A99.2, A101). BUILD_V007 (PENDING_BUILD_V007) must launch exactly these ten FILLED specs; '
                'this is checked from bytes when it lands.')
    app(('binding_inputs', 'spec_set'), more, ['A99.1', 'A99.2', 'A101'], ['A99.1', 'A99.2', 'D-02', 'D-03'], 'case block and BUILD_V007 template bound to the same ten specs')
    # ================================================================= fixed across all cases
    app(('fixed_across_all_cases', 'validity_gates'), 'The registered V007 case block is binding_inputs.case_block (A99.2); the compare reads it from the sealed '
        'prereg only (r12 L5706).', ['A99.2'], ['A99.2', 'D-03', 'R-03'], 'where V3 finds the registered case block')
    app(('fixed_across_all_cases', 'production_tail', 'gas'),
        'NGC gas M_s stays 96: GQ_NGC at M_s 96 against 192 holds on [2, 91] (4096-node max 1.219e-15 P0, every-k_perp bound 2.335e-14 P0, both below '
        '1e-12; Codex1 0032, record GQ_NGC_91_MS96_V001 be148bab; TESTED), so A81 RI-23\'s condition is not met, and LO_NGC and DOUBLING\'s NGC half stay at '
        'M_s 96 (production_tail.ngc_gas_M_s).', ['Codex1 0032'], ['A81 RI-23', 'Codex1 0032', 'R-08'], 'RI-23 condition evaluated from the GQ_NGC record')
    pt['ngc_gas_M_s'] = {'text': '96. The NGC gas M_s (seal tool 3 slot ngc_gas_M_s). A57.1 kept NGC at M_s 96 (its GQ passed to 32); A64.2 and A81 RI-23 make it '
                                 '128 only if GQ_NGC at M_s 96 fails anywhere on [2, 91]; it does not fail (Codex1 0032; GQ_NGC_91_MS96_V001 be148bab, PASS, '
                                 'TESTED). The compare binds the NGC gas M_s to the registered 96 or refuses (A80). Root states the value at seal assembly '
                                 '(rehearsal R-08).',
                         'sources': ['A57.1', 'A60', 'A64.2', 'A80', 'A81 RI-23', 'Codex1 0032', 'R-08'], 'value': 96}
    log('fixed_across_all_cases.production_tail.ngc_gas_M_s', 'new', ['A81 RI-23', 'Codex1 0032'], ['A81 RI-23', 'Codex1 0032', 'R-08'],
        'the value the tool-3 slot ngc_gas_M_s takes, with its ruling and evidence')
    rep(('fixed_across_all_cases', 'production_tail', 'memory_guard'), 'Under r6 the module is v003 (A72.1).',
        'V007 seals on r5 (A96), so no r6 module is used.', ['A96'], ['A96'], 'r6 moot')
    rewrite(('fixed_across_all_cases', 'production_tail', 'tail_table_cache'),
            'A72\'s caching branch is not used for V007. A89 made A72(c) concrete (r6 only if it causes no seal delay), and A96 applied it: at 19:51Z the r6 '
            'BUILD had not landed, so V007 seals on driver v010 r5 (b5cc62af); the r6 build workflow was stopped and its partial bytes in driver_r6/ are '
            'unfinished and unused; no V007 case uses the cache; A81 RI-24 and the conditional cache slot are moot for V007; caching for steps 4-5 is decided '
            'later, with the A85.1 parallel-tail result. At launch the plan\'s driver must equal the SEAL_RECORD\'s driver (C4-S1; A78), so the ten T-cases of '
            'one bound plan share the sealed driver; no T-run starts before the seal names the driver, and every T-run\'s driver_sha256 equals the driver slot '
            '(the T-run clause of A81 RI-24, kept: under r5 it also follows from the case block\'s drivers_allowed [r5] and C4-S1).',
            ['A89', 'A96'], ['A89', 'A96', 'GAP-19'], 'A96 applied A89/A72(c): r5, no cache', expect_prefix='A72: adopted only if')
    # ================================================================= gates
    rep(('gates_before_any_T_result', 'B0prime_RERUN'), 'Rerun on v010 r5. Compared by the identity-comparator slot; carries driver_sha256 = the driver slot '
        '(A67 N1); rerun on r6 if A72 adopts r6.',
        'Rerun on v010 r5 (UVT_B0P_RERUN_ADMIT_PREFIX_R5_RUN_V001, completed). Compared by the identity-comparator slot (c2v007r2, A92); carries driver_sha256 '
        '= the driver slot (A67 N1); no r6 rerun (A96).', ['A92', 'A96'], ['A92', 'A96'], 'r5 run compared by c2v007r2; r6 moot')
    rep(('gates_before_any_T_result', 'Z2_OFF_RO1'), 'Rerun on the driver slot (r5 runs launched 14:56Z; r6 if adopted); carries driver_sha256 = the driver slot.',
        'Rerun on the driver slot (the r5 run launched 14:56Z and completed; compared by root with c2v007r2: PASS_BITWISE_EQUAL, A92; no r6 rerun, A96); '
        'carries driver_sha256 = the driver slot.', ['A92', 'A96'], ['A92', 'A96'], 'r5 run compared; r6 moot')
    rep(('gates_before_any_T_result', 'B1_Z2'), 'Compared with the identity-comparator slot (c2v007 lineage);',
        'Compared with the identity-comparator slot (the c2v007 lineage: c2v007r2, A92);', ['A92'], ['A92', 'GAP-07'], 'the comparator of record')
    app(('gates_before_any_T_result', 'B2'),
        'A94: B2 follows this text exactly, with no substitution it does not name: full static rows (not stars only) with the registered gas rule; le3 for '
        'every case (a historical C3R3 le4 state does not stand in; a missing le3 input reads INCOMPLETE, named); the statistic the text names (P16); the '
        'record states its basis (components, variant, statistic) and lists every interpretation as a ROOT_ITEM. A97: the sanity reference is decomposed '
        'before deciding, under a rule fixed before the decomposition: (a) if an unnamed difference exists and, once it is removed, the named-only residual is '
        '<= 0.05 km/s on C2, C3 and C4, the registered reference was mis-specified and B2\'s sanity reads against the like-for-like reference (ADV\'s method '
        'with only the named differences), the 0.05 unchanged; (b) a larger residual, or a production or shared-input error, fails B2 (a real defect is fixed '
        'before the seal and B2 rerun; if no fix is possible, no ADOPT_TAIL); (c) C3R3\'s sanity is computed the same way, or B2 reads INCOMPLETE. A100: B2 '
        'is disposed under A97(a): the unnamed difference is the gas rule (ADV\'s discrete rings J0(kR_i)E_i against the registered continuum_v001); the '
        'like-for-like reference is ADV\'s method with production\'s continuum_v001 gas rule; the 0.05 allowance is unchanged; the values of record are '
        'reading (ii) with P16: 0.0301 (C2R3), 0.0356 (C3R3, le3) and 0.0384 (C4R3) km/s; the m0 values and reading (i) are disclosed. A101: the B2 record of '
        'record is B2_GATE_RECORD_C3V003 (915fbcda, PASS; Codex2 0503: 0 blocking); its two documentation should-fix items are carried as an erratum in the '
        'seal record\'s disclosure block (seal_record_requirements[12]); C3V002 (d4b41ffc, FAIL) is superseded and kept. B2 does not prove shared physical '
        'correctness (A100).', ['A94', 'A97', 'A100', 'A101'], ['A94', 'A97', 'A100', 'A101', 'R-15', 'GAP-15'], 'B2 rulings A94/A97/A100/A101')
    rep(('gates_before_any_T_result', 'GQ'), 'Record of record: GQ_CERT_V005_MS128 (fbceefe6), with V004 (7ebb1d48) as the FAIL control (A67 SF2, A70).',
        'Record of record: GQ_CERT_V006 (5a1b39f8), exactly the on-map subset of GQ_CERT_V005_MS128 (fbceefe6): 7 rosters, one per name, on the A75.6 fixed '
        'map, numbers bitwise unchanged, written by a registered subset producer from V005\'s bytes; V005 itself carries extra same-name rosters and reads '
        'RECORD_DEFECT under A79.1, which stands (A86.1); V004 (7ebb1d48) stays the FAIL control (A67 SF2).', ['A86'], ['A86', 'GAP-02 (A86 evidence)'],
        'A86.1 GQ record of record')
    app(('gates_before_any_T_result', 'DOUBLING'),
        'The record of record is DOUBLING_MERGED_C3V001 (ea48ac2b; A87: built by Claude3, 0586; PASS: DDO 4.67e-13 tau, NGC 0.0/theta; registered from '
        'C3V003). It states its DDO M_s as ddo_gas_M_s = 128, the field of the A73 merged format and of FIELDS_R12 DOUBLING, not as source_gas_M_s '
        '(rehearsal D-01, R-13).', ['A87'], ['A87', 'A73', 'D-01', 'R-13', 'GAP-11'], 'DOUBLING record of record and its M_s field')
    app(('gates_before_any_T_result', 'LO_NGC'),
        'The V007 LO_NGC slot takes LO_NGC_CERT_V002 (33bc2190), the LO_NGC record of record (A87), reported only; LO_NGC_K32_CERT_V001 (07745bbf) is the NGC '
        'N-test record, with coverage to 91 (A90), and is not a V007 input.', ['A87', 'A90'], ['A87', 'A90', 'GAP-12'], 'LO_NGC records named')
    rewrite(('gates_before_any_T_result', 'after_seal_marker_policy'),
            'PRODUCED_AFTER_THE_SEAL is accepted only for the nine gates whose records are produced after the seal: the eight computed from V007 run outputs '
            '(SRB_ROT, RB_FP, T2I, EA, MT, I1T, FLAG_RULINGS, HARMONICS) and SR_K, which the sealed pinned producers compute right after the seal on the fixed '
            'saved C2R3/C3R3/C4R3 states, before any T-run output is read (A88; r12 GATE_RECORD_AFTER_SEAL_ALLOWED L341 and GATE_RECORD_SHA_REQUIRED = () '
            'L338, A99.5). At compare time those records are verified by producer pin and producer bytes against the producer registry (A62.2, A69); SR_K '
            'keeps the bitwise-identical-Delta RECORD_DEFECT (A67 N2). The token is refused for EPS, GQ, LO, LO_NGC, DOUBLING, B0-B3 and the identity gates, '
            'whose records of record exist before the seal (A88), and for every other gate (r12).',
            ['A88', 'A99.5'], ['A88', 'A99.5', 'GAP-20'], 'SR_K joins the after-seal set', expect_prefix='PRODUCED_AFTER_THE_SEAL is accepted only for the eight')
    # ================================================================= tests
    rep(('tests', 'SR_K'), 'SR_K and its gate record are bound to root-registered producer shas (A62.2); its gate-record sha of record is registered in the '
        'producer registry before the seal (A67 N2), so PRODUCED_AFTER_THE_SEAL is refused for SR_K (A79 NEW-61);',
        'SR_K and its gate record are bound to root-registered producer shas with producer-byte verification (A62.2, A69). A88 (amending A79 NEW-61 for SR_K '
        'only): the SR_K record is produced right after the seal, before any T-run output is read, by the sealed pinned producers (sr_k_static v009, '
        'aggregate_records v008) on the fixed saved C2R3/C3R3/C4R3 states, so it depends on no T result; its registry entry carries the producer pins and '
        'PRODUCED_AFTER_THE_SEAL; root runs it as the first post-seal step (RUNBOOK);', ['A88', 'A69'], ['A88', 'GAP-20'], 'A88: SR_K after the seal')
    # ================================================================= run list
    rewrite(('run_list', 'DDO_gates'),
            'Z2 (2d5e79d0), Z2_OFF_RO1 (894e5b3a), B0prime_RERUN (4ac5527a): the r5 identity reruns launched at 14:56Z (monitor ba031c23; wall 43,200 s, RSS '
            '16 GiB, output 32 GiB; no retries; detached), all COMPLETED with exit 0 and compared by root with the identity-comparator slot c2v007r2 (052da0fe): '
            'Z2, Z2_OFF_RO1 and B0P_RERUN read PASS_BITWISE_EQUAL (A92); the records of record are gates_v007/r2/records/R5_V001 (identity_gate_records slot). '
            'No r6 rerun (A96).', ['A92', 'A96'], ['A92', 'A96', 'GAP-08'], 'r5 identity runs done and compared', expect_prefix='Z2 (2d5e79d0)')
    rewrite(('run_list', 'DDO_tests'),
            'C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO (K_big 64), C4T-KHI (K_big 256), C4T-A: the ten filled P128/M_s 128 specs '
            '(binding_inputs.spec_set; their case block binding_inputs.case_block), launched by root from the bound plan (launch-packet slot: BUILD_V007\'s r5 '
            'template, A99.1), all on driver v010 r5 (A96); no case uses the tail-table cache (A96).',
            ['A96', 'A99.1', 'A99.2'], ['A96', 'A99.1', 'A99.2', 'D-02'], 'r5 only; BUILD_V007 template', expect_prefix='C2T, C3T, C4T, C6T')
    app(('run_list', 'replays'), 'SR_K is produced right after the seal by the sealed pinned producers, before any T-run output is read (A88; RUNBOOK: the first '
        'post-seal root step).', ['A88'], ['A88'], 'SR_K after the seal')
    rep(('run_list', 'limits'), 'The root admission config names the BUILD_V005 launcher and guard sources exactly (A78 N2).',
        'The root admission config names the BUILD_V007 launcher and guard sources exactly (A78 N2; A99.1), and its producer_allowlist is exactly BUILD_V007\'s '
        '15 supported sources (V6-S3).', ['A99.1'], ['A99.1', 'D-02', 'GAP-09', 'GAP-21'], 'BUILD of record V007')
    rewrite(('run_list', 'cpu_hours_estimate_UNTESTED'),
            'A89 (measured: kbig_timing_v003 TIMING_V003 3e3fb600; r5 module, M_s 128, production quadrature): C4T-KHI full call solo 7.84 h expected (I = 7, '
            'P = 3) and 13.86 h at the upper bound (I = 32, P = 6); C4T (K128) solo 5.2-8.1 h; the 27.84 h preview, and with it r4\'s 5.0-27.8 h per case '
            '(104.4 solo hours) from the launch-packet cost model, is superseded; step 2 takes about 10-16 h with core priority (A85.2), set by KHI. I and P '
            'were measured on tail-off runs, so the tail-on counts are UNTESTED. Co-load may lengthen execution; elapsed time is unbounded under the memory '
            'gate. UNTESTED.', ['A89'], ['A89'], 'measured cost', expect_prefix='Restated from the measured-timing cost model')
    # ================================================================= scope, outcome tests, not-V007 scope
    su = doc['scope_untested']
    i = su.index('the A72 cache saving, until kbig_timing_v003 reports (condition (c))')
    su[i] = 'the A72 cache saving (A89: 1.83-2.80 h on KHI solo, caching untested); moot for V007 (A96)'
    su.append('B2\'s like-for-like sanity does not prove shared physical correctness (A100)')
    log('scope_untested', 'revised', [], ['A89', 'A96', 'A100'], 'cache saving measured and moot; B2 limit')
    doc['outcome_branch_tests_required'] = doc['outcome_branch_tests_required'].replace(
        '(the final round: r11, or r12; A80)', '(the final round: r12 cx3v002 4bd7b262, or a fix round root orders under A81 RI-20; A96)')
    if '4bd7b262' not in doc['outcome_branch_tests_required']:
        raise SystemExit('outcome_branch_tests_required anchor')
    log('outcome_branch_tests_required', 'revised', [], ['A96', 'GAP-06'], 'the final round named')
    rep(('not_v007_text_scope',), '(A74 cx3r005, A77 cx3r006, A80 cx3r007; launch registry cx3r006 3c42ca07, retired 47023c27 and c5abc2d5)',
        '(A74 cx3r005, A77 cx3r006, A80 and A93 cx3r007; the step-5 launch registry is SPEC_REGISTRY_CX3R007 cd30429c, A93; retired 3c42ca07, 47023c27 and '
        'c5abc2d5)', ['A93'], ['A93'], 'registry named in the scope note')
    # ================================================================= seal record requirements
    rep(('seal_record_requirements', 2), '(RI-27, as drafted)', '(A82: RI-27 ruled as drafted in r4)', ['A82 (RI-27)'], ['A82'], 'RI-27 ruled')
    swap_src(sr[2], 'RI-27 (draft)', 'A82 (RI-27)')
    c4 = sr[4]
    for old, new in (('(1) the frozen copy of the V005 addendum, after the last pre-seal entry (A81 RI-26);',
                      '(1) the frozen copy of the V005 addendum, after the last pre-seal entry (A81 RI-26), after which root writes nothing more to the open V005 '
                      'file and later entries go to a V006 addendum (A82; A99.6);'),
                     ('(2) with the driver chosen (A72), and under r6 a fresh, empty, root-created cache directory (A81 RI-24), the bound plan and command',
                      '(2) with the driver chosen (r5, A96; no cache directory, A81 RI-24 being moot), the bound plan and command'),
                     ('(4) the sealed compare (RI-27, as drafted);', '(4) the sealed compare (A82);'),
                     ('the bound plan and command shas and, under r6, the cache directory;', 'the bound plan and command shas;')):
        if c4['text'].count(old) != 1:
            raise SystemExit('seal_record_requirements[4] anchor: ' + old[:40])
        c4['text'] = c4['text'].replace(old, new)
    addsrc(c4, ['A82', 'A96', 'A99.6'])
    log('seal_record_requirements[4]', 'revised', ['A82', 'A96', 'A99.6'], ['A82', 'A96', 'A99.6', 'GAP-01'], 'no write after the freeze; r5, no cache')
    sr[8]['text'] = ('Seal-time pins in the compare (A82): V007_PREREG_SHA256 (the sealed prereg), PIN_ADDENDUM_V005 (the frozen copy), PIN_DRIVER_BUILD_RECORD '
                     '(the r5 driver BUILD record, schema UNT_V007_SEALED_DRIVER_BUILD_C2V001, which root exclusively creates at seal assembly before the sealed '
                     'compare, equal to the compare\'s built-in r5 set with check_record = the driver check record of record; rehearsal D-06), PIN_V010_R5_CHECK '
                     '(the r5 check record; r5 per A96), PIN_PRODUCER_REGISTRY; the custody pins follow the A77.2 role table read from the driver slot.')
    addsrc(sr[8], ['A82', 'A96'])
    log('seal_record_requirements[8]', 'rewritten', ['A82', 'A96'], ['A82', 'A96', 'D-06', 'GAP-04'], 'the five pins; the driver BUILD record created at assembly')
    sr[10]['text'] = ('The root admission config names the BUILD_V007 launcher and guard sources exactly (A78 N2: the build check is a substring match), and its '
                      'producer_allowlist names exactly BUILD_V007\'s 15 supported sources (A99.1; V6-S3).')
    addsrc(sr[10], ['A99.1'])
    log('seal_record_requirements[10]', 'rewritten', ['A99.1'], ['A99.1', 'D-02', 'GAP-09', 'GAP-21'], 'BUILD_V007, 15 sources')
    sr[11]['text'] = ('Any A-entry after A81 that touches this text needs a successor revision or an explicit no-change note in the seal record; the seal check '
                      'verifies that every A-entry this text cites is present in the frozen bytes. The entry table entries_after_A81 lists every entry from A82 '
                      'to the newest at r5 generation (%s) as revised here (with its clauses) or no change (with the reason), each with its section sha256 read '
                      'from bytes, and the seal record quotes it (A99.3). At the freeze each row\'s section is re-hashed from the frozen bytes: a row whose '
                      'section differs, and any entry after %s without a row, needs a successor revision or an explicit seal-record note (A81 RI-26).'
                      % (newest, newest))
    addsrc(sr[11], ['A99.3'])
    log('seal_record_requirements[11]', 'rewritten', ['A99.3'], ['A99.3', 'D-05', 'GAP-02', 'R-02'], 'the entry table quoted; rows re-hashed at the freeze')
    sr.append(cl('The seal record repeats the B2 disclosure block of the B2 record of record (A100): the raw misses against ADV\'s saved rows (0.082 / 0.095 on '
                 'le3 / 0.108 km/s), the gas-rule attribution, readings (i) and (ii) with P16 and m0, that ADV\'s saved C3R3 used le4, and the limit that B2 '
                 'does not prove shared physical correctness; and A101\'s erratum for the record\'s two documentation should-fix items (C3V003-RI-1 '
                 'attributes GL6/0.25 to 0622 in error; "<= 3.8e-11" should read approximately 3.83e-11).', 'A100', 'A101'))
    log('seal_record_requirements[%d]' % (len(sr) - 1), 'new', ['A100', 'A101'], ['A100', 'A101', 'R-15'], 'B2 disclosure in the seal record')
    # ================================================================= seal slots
    fa = sl['frozen_addendum']
    fa['rule'] = fa['rule'].rstrip() + (' Once the frozen copy exists, root writes nothing more to the open V005 file; every later root entry goes in a V006 '
                                        'addendum (A82; A99.6: the hazard is live, because the compare cites the open path).')
    swap_src(fa, 'RI-27 (draft)', 'A82 (RI-27)')
    addsrc(fa, ['A99.6'])
    log('seal_slots.frozen_addendum', 'rule extended', ['A82 (RI-27)', 'A99.6'], ['A82', 'A99.6', 'GAP-01', 'D-10'], 'no write after the freeze')
    dv = sl['driver']
    dv['branch'] = ('r5 (A96: V007 seals on driver v010 r5 b5cc62af; A89\'s no-delay condition for r6 was not met; r6 is deferred and its partial bytes are '
                    'unused)')
    dv['named_candidates_verified_from_bytes']['r6'] = 'NOT_A_CANDIDATE (A96)'
    dv['rule'] = dv['rule'].rstrip() + ' The driver is v010 r5 (A96).'
    addsrc(dv, ['A89', 'A96'])
    log('seal_slots.driver', 'branch fixed', ['A89', 'A96'], ['A96', 'GAP-19'], 'r5')
    cp = sl['compare']
    cp['rule'] = ('The final compare round is r12 cx3v002 (4bd7b262; selected by SELECTED_R12_CX3V001 91aa9747; FIELDS_R12_CX3V002 5cc95a06, IMPL ef0db32d, '
                  'HASHES 3eb2912d; frozen 19:48:42Z; A96), whose scope is exactly A91.1-A91.3 (0459, 0462\'s should-fix, A88 SR_K; A91.4\'s RI-24 cache '
                  'fields are moot, A96). V007 seals on the round whose delta reviews of record, Claude3\'s and Codex2\'s, each report 0 blocking (A81 RI-20 as '
                  'applied by A83, A86, A91 and A96: the r11 workflow was stopped at its freeze before its three recheck lenses ran, and the reviews of record '
                  'replaced them, A83; rehearsal R-02); if a review of record reports a blocking item, the slot waits for root\'s ruling (a fix round, or a '
                  'ruling on the item). This slot holds that round\'s reviewed source, with its seal-time pin constants still unset (`None`; the bytes the '
                  'reviews examined), path and sha. The sealed compare (V007_PREREG_SHA256 set to the sealed prereg sha, plus PIN_ADDENDUM_V005, '
                  'PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK and PIN_PRODUCER_REGISTRY) is created after the sealed prereg and is named only in the SEAL_RECORD; '
                  'it may differ from the reviewed source only in those pin lines (A82: RI-27 ruled as drafted in r4).')
    nc = cp['named_candidates_verified_from_bytes']
    cp['named_candidates_verified_from_bytes'] = {
        'r12_cx3v002_final_round': P['r12_compare'], 'r12_selection': P['r12_selected'], 'r12_fields': P['r12_fields'], 'r12_impl': P['r12_impl'],
        'r12_hashes': P['r12_hashes'],
        'delta_review_of_record_Codex2_0485': dict(P['Codex2_0485'], verdict='PASS_WITH_FINDINGS, 0 blocking', report=P['r12_review_Codex2']),
        'delta_review_of_record_Claude3_0083': dict(P['Claude3_0083'], verdict='FAIL, 1 BLOCKING (A-B1: check_record_codes L875-879; an integer longer than 4300 '
                                                    'digits raises ValueError before the duplicate hook, so a duplicate-key check record reaches the text fallback)',
                                                    report=P['r12_review_Claude3']),
        'state_at_r5_generation': ('PENDING_ROOT_RULING: Claude3 0083 reports 1 BLOCKING, so r12 does not yet meet A81 RI-20 (0 blocking from each review of '
                                   'record); root rules a fix round or a ruling on A-B1 (ROOT_ITEMS_R5 RI-28)'),
        'r11_superseded': dict(P['r11_compare_superseded'], note='Codex2 0459/0462 blocking (A90, A91): r12 follows'),
        'r10_frozen_not_for_seal': nc['r10_frozen_not_for_seal']}
    swap_src(cp, 'RI-27 (draft)', 'A82 (RI-27)')
    addsrc(cp, ['A83', 'A86', 'A90', 'A91', 'A96'])
    log('seal_slots.compare', 'rule rewritten', ['A83', 'A86', 'A90', 'A91', 'A96'], ['A83', 'A86', 'A90', 'A91', 'A96', 'R-02', 'GAP-06'],
        'the final round r12 and its reviews of record')
    ic = sl['identity_comparator']
    ic['rule'] = ('The c2v007-lineage round whose check of record reports 0 blocking (A81 RI-21): c2v007r2 (run_identity_compare_c2v007.py 052da0fe, A92), after '
                  'Codex2\'s delta check 0472 (PASS_WITH_FINDINGS, 0 blocking). Codex2\'s cross-lineage review is the c2v007 check of record: the c2v007 '
                  'own-check workflow was stopped after the build froze and its outputs are leads only (A83; rehearsal R-02). c2v007r2 requires identity_sha256 '
                  'and caller.sha256 present on both sides (A91). c2v004-c2v006 are superseded and not used at the seal.')
    old_ic = ic['named_candidates_verified_from_bytes']
    ic['named_candidates_verified_from_bytes'] = {'c2v007r2': P['comparator_c2v007r2'], 'superseded_r4_observation': old_ic}
    addsrc(ic, ['A83', 'A91', 'A92'])
    log('seal_slots.identity_comparator', 'rule rewritten', ['A83', 'A91', 'A92'], ['A83', 'A91', 'A92', 'R-02', 'GAP-07'], 'c2v007r2, the check of record')
    ig = sl['identity_gate_records']
    ig['rule'] = ig['rule'].rstrip() + ' A92: the c2v007r2 records R5_V001.'
    ig['observed_at_assembly'] = ('gates_v007/r2/records/R5_V001/: B1 83e7b067, B1_OFF 3b9ad402, B0prime_RERUN e33af53d (A92); registered from C3V004 and in '
                                  'C3V008 (A101)')
    ig['named_candidates_verified_from_bytes'] = {'Z2': P['id_B1'], 'Z2_OFF_RO1': P['id_B1_OFF'], 'B0prime_RERUN': P['id_B0prime_RERUN']}
    addsrc(ig, ['A92', 'A101'])
    log('seal_slots.identity_gate_records', 'candidates named', ['A92', 'A101'], ['A92', 'GAP-08'], 'R5_V001 records of record')
    lp = sl['launch_packet']
    lp['rule'] = ('BUILD_V007 (A99.1: the V006 successor that closes V6-S1 (non-finite values refuse; records serialized before one exclusive write), V6-S2 (the '
                  'RUNBOOK carries A85.2-4, and the r5 template\'s outputs go to the internal volume, not External1 runs_ext) and V6-S3 (15 supported sources); '
                  'BUILD_V005 and BUILD_V006 are superseded as the BUILD of record), with the bound plan and command that the build-only binder writes from '
                  'BUILD_V007\'s selected r5 template, the chosen driver and the frozen addendum (exclusive create). The binder runs after the addendum is frozen '
                  'and the driver is chosen, and before the SEAL_RECORD is written; the SEAL_RECORD names the bound plan and command shas; root verifies both '
                  'from bytes immediately before running the command. A validate()-level template-equality check is optional and not required (A81 RI-25). The '
                  'template is unbound and PENDING by design. BUILD_V007\'s Claude4 delta check and Claude2\'s adoption are pending (A99.1).')
    if bv7:
        lp['named_candidates_verified_from_bytes'] = dict({'build': bv7}, **{k: v for k, v in bv7_check['named'].items()},
                                                          launcher=bv7_check['launcher'], guard=bv7_check['guard'], spec_registry=P['spec_registry'],
                                                          build_v007_check_at_r5_generation=bv7_check,
                                                          BUILD_V006_delta_review_Claude4_0099=P['build_v006_review_Claude4'],
                                                          BUILD_V005_superseded=P['build_v005_superseded'])
    else:
        old_lp = lp['named_candidates_verified_from_bytes']
        lp['named_candidates_verified_from_bytes'] = {'build': PENDING_BUILD, 'BUILD_V006_predecessor': P['build_v006'],
                                                      'BUILD_V006_delta_review_Claude4_0099': P['build_v006_review_Claude4'],
                                                      'BUILD_V005_era_candidates_superseded': old_lp}
    lp['pending_parts'] = ['bound_plan', 'bound_command', 'BUILD_V007 Claude4 delta check (A99.1)', 'BUILD_V007 adoption (Claude2)']
    addsrc(lp, ['A87', 'A88', 'A99.1'])
    log('seal_slots.launch_packet', 'rule rewritten; build bound', ['A87', 'A88', 'A99.1'], ['A99.1', 'D-02', 'GAP-09', 'GAP-21'],
        'BUILD_V007 is the BUILD of record' + (' (filled from bytes)' if bv7 else ' (PENDING_BUILD_V007)'))
    ct = sl['certificates']
    ct['rule'] = ('Root confirms each record of record at seal assembly. Every record that depends on M_s states its M_s (source_gas_M_s; the merged DOUBLING '
                  'record states ddo_gas_M_s, the A73 merged-format and FIELDS_R12 DOUBLING field; rehearsal D-01, R-13), equal to the case block\'s registered '
                  'gas.M_s, which must be 128 for DDO; an NGC record that states an M_s states 96, the NGC gas M_s (production_tail.ngc_gas_M_s; A81 RI-23 not '
                  'triggered, Codex1 0032). LO_NGC is reported only in V007: the V007 LO_NGC slot takes LO_NGC_CERT_V002 (33bc2190), the LO_NGC record of '
                  'record (A87); coverage to 91 gates the NGC N-test compare (step 5), not the V007 seal (A81 RI-23). DOUBLING is one merged record, registered '
                  'before the seal (A81 RI-22): DOUBLING_MERGED_C3V001 (ea48ac2b, A87). GQ\'s record of record is GQ_CERT_V006 (5a1b39f8, A86).')
    nc = ct['named_candidates_verified_from_bytes']
    nc['GQ'] = P['gq_v006']
    nc['GQ_V005_superseded_A86'] = P['gq_v005_superseded']
    nc['DOUBLING_merged'] = P['doubling_merged']
    nc['LO_NGC'] = P['lo_ngc_v002']
    nc['LO_NGC_91'] = dict(P['lo_ngc_k32'], note='the NGC N-test record with coverage to 91 (A90); not the V007 LO_NGC slot (A87)')
    nc['GQ_NGC_91'] = dict(P['gq_ngc_91_ms96'], note='GQ_NGC at M_s 96 on [2, 91], PASS (Codex1 0032); an NGC N-test input, not a V007 slot')
    addsrc(ct, ['A86', 'A87', 'A90', 'R-13', 'Codex1 0032'])
    log('seal_slots.certificates', 'rule rewritten; candidates named', ['A86', 'A87', 'A90', 'R-13', 'Codex1 0032'],
        ['A86', 'A87', 'A90', 'A81 RI-23', 'D-01', 'R-13', 'GAP-11', 'GAP-12'], 'records of record; M_s field names')
    pr = sl['producer_registry']
    pr['rule'] = ('Root-registered producer paths and shas and the gate-record shas of record (A67 N2); the compare hashes the producer bytes, not only the '
                  'claimed sha (A69.1); every replay gate record is bound to it (A62.2); SR_K is registered by its producer pins with PRODUCED_AFTER_THE_SEAL '
                  '(A88). The registry carries the c2v007r2 comparator, its tokens and the R5_V001 identity records (A92), the B3, B0, B0prime_DRY and B0_FA '
                  'records (Claude4 0598), the B2 record of record C3V003 (A100, A101), BUILD_V007\'s post-seal producers (A99.5, V6-N4) and the B0_N3, B0_RO1 '
                  'and I4 records once built (their empty slots fail closed). Pinned in the compare as PIN_PRODUCER_REGISTRY (A67).')
    pr['named_candidates_verified_from_bytes'] = {
        'C3V009_candidate': dict(P['registry_c3v009'], note=('C3V008 plus BUILD_V007\'s four post-seal producer pins (SRB_ROT 2757847a; MT, I1T and '
                                                            'FLAG_RULINGS 4024d82a) and nothing else (Claude3 0087); on r12 with the case block of '
                                                            'record 76309ae3 all 13 registered records PASS and B0_N3, B0_RO1, I4 fail closed '
                                                            '(VALIDATE_R12_C3V009_CASEBLOCK_OF_RECORD 537d1a42); anticipated by A101 and listed in '
                                                            'dispatch 0626; a record filling B0_N3, B0_RO1 or I4 means a V010')),
        'C3V008_final_A101': P['registry_c3v008'],
        'note': ('V008 is final under A101: all 13 registered records PASS on r12 (Claude3 0084); B0_N3, B0_RO1 and I4 are empty and fail closed; BUILD_V007\'s '
                 'post-seal producers come in V009 (Claude3 0084). The slot value is the registry root pins at seal assembly.'),
        'C3V007_superseded': P['registry_c3v007']}
    addsrc(pr, ['A88', 'A92', 'A99.5', 'A100', 'A101', 'Claude3 0087'])
    log('seal_slots.producer_registry', 'rule rewritten; candidate named', ['A88', 'A92', 'A99.5', 'A100', 'A101'],
        ['A87', 'A88', 'A92', 'A99.5', 'A101', 'GAP-13'], 'what the registry of record carries')
    cd = sl['cache_directory_r6_only']
    cd['value'] = 'NOT_APPLICABLE_R5'
    cd['rule'] = ('Moot for V007: V007 seals on r5 (A96), so no cache directory is created or named; A81 RI-24 and the conditional cache slot are moot. Seal '
                  'tool 3 requires the string NOT_APPLICABLE_R5 under r5.')
    addsrc(cd, ['A96'])
    log('seal_slots.cache_directory_r6_only', 'value fixed by A96', ['A96'], ['A96'], 'NOT_APPLICABLE_R5')
    # ================================================================= root items
    for r in doc['root_items']:
        if r['id'] == 'RI-27':
            if r['status'] != 'OPEN':
                raise SystemExit('RI-27 expected OPEN in r4')
            r['status'] = ('RESOLVED: A82 (RI-27 ruled as drafted in r4: reviewed compare source -> sealed prereg -> sealed compare -> SEAL_RECORD; the '
                           'frozen addendum cites no sealed-prereg sha)')
        if r['id'] == 'RI-24':
            r['status'] = r['status'] + '; moot for V007 under A96 (r5)'
    log('root_items.RI-27, RI-24', 'resolved', ['A82', 'A96'], ['A82', 'A96'], 'RI-27 ruled; RI-24 moot')
    new_items = [
        ('RI-28', 'PENDING_ROOT_RULING (compare slot)', 'seal_slots.compare',
         'Claude3\'s r12 delta review of record (0083, 8fe311ba) is FAIL with 1 BLOCKING item, A-B1: in check_record_codes (r12 L875-879) an integer literal '
         'longer than 4300 digits raises a plain ValueError before the duplicate-key hook, so a duplicate-key check record falls to the text test and is '
         'admitted. Codex2\'s review of record (0485) reads 0 blocking. A81 RI-20 needs 0 blocking from each.',
         'the slot names r12 cx3v002 and its rule; its state is PENDING_ROOT_RULING.',
         'RECOMMENDATION ONLY: rule a fix round (Claude3\'s helper tested in-process the one-line parse_int=str fix at L875; a JSONDecodeError-only text '
         'fallback is the alternative) with delta reviews by Claude3 and Codex2, then name that round in the compare slot; or rule explicitly why A-B1 does not '
         'block the seal (exposure needs a root-pinned check record with an integer longer than 4300 digits).',
         ['A81 RI-20', 'A91', 'A96', 'Claude3 0083', 'Codex2 0485']),
        ('RI-29', 'PENDING (BUILD of record)', 'seal_slots.launch_packet',
         'BUILD_V007 is the BUILD of record (A99.1). ' + ('It landed (Codex3, %s) and is filled here from bytes; its Claude4 delta check and Claude2 adoption '
                                                         'are pending.' % b7 if bv7 else 'It is not on disk at r5 generation: PENDING_BUILD_V007.'),
         'the generator fills the build pin from bytes when BUILD_V007 is found by name; it verifies 15 supported sources, the template\'s spec pins against '
         'the case block and the predecessor BUILD_V006.',
         'RECOMMENDATION ONLY: if the delta check or adoption changes BUILD_V007, re-run this generator on the successor\'s bytes and re-pin seal tool 3 v002 '
         'to the regenerated text.', ['A99.1', 'Codex3 0628']),
        ('RI-30', 'RECOMMENDATION (rehearsal R-10)', 'seal_record_requirements[3]; binding_inputs.case_block',
         'The case block\'s own key_equivalence_map is [] and validate_case_block reads it; the SEAL_RECORD carries a separate key map (seal_record_requirements[3], '
         'A48 AMB-13). No tool checks that the two agree.',
         'the case block map is [] (no C4T-D5 key outside composite_grid_spec and uv_tail differs from the C5H reference; TESTED).',
         'RECOMMENDATION ONLY: one key map of record: the SEAL_RECORD\'s key-equivalence map equals the case block\'s ([]), and the SEAL_RECORD builder '
         'successor requires equality.', ['A48 AMB-13', 'R-10']),
        ('RI-31', 'PENDING_ROOT_RULING (checklist A6)', 'gates_before_any_T_result.B0',
         'The candidate B0 record c2cec35b (Claude4 0598; registered in C3V007/C3V008) covers r5 against r4 on the registry V002 P128 rows at gas M_s 64; the '
         'production M_s 128 set (c7023846) has no r5 == r4 dry-identity row, and A55 ruling 2 asks for every spec (0598 independent check F3).',
         'A6 lists c2cec35b as its candidate (rehearsal R-09).',
         'RECOMMENDATION ONLY: root records A6 done on c2cec35b, or orders the M_s 128 dry-identity run first.', ['A55', 'A87', 'R-09']),
        ('RI-32', 'PENDING_ROOT_RULING (owner)', 'seal_record_requirements[9]',
         'CASCADE_MAP_R5_ADDENDUM (A69: the immutable inventory addendum naming the unreachable pin-only successor) is required before the seal on r5, has no '
         'owner and is not on disk (rehearsal GAP-18).', 'the requirement stands as in r4.',
         'RECOMMENDATION ONLY: assign an owner (the driver r5 lane) and a delta check.', ['A69', 'A96']),
        ('RI-33', 'PENDING (records not built)', 'gates_before_any_T_result.B0_N3, B0_RO1; I4 mode gate',
         'B0_N3 (an r5 static guard scan), B0_RO1 parts (b) and (c) (replays) and I4 (a production run, C2T N8 against N1, whose N1 spec pair root fixes) are '
         'not built; their registry slots are empty and fail closed (rehearsal GAP-14; Claude3 0084).', 'requirements unchanged.',
         'RECOMMENDATION ONLY: root fixes the I4 pair and the run owners (A87 owners build the records once the runs exist).', ['A47 I4', 'A87', 'A101']),
        ('RI-34', 'PROCEDURE (entries after the table)', 'entries_after_A81; seal_record_requirements[11]',
         'The entry table covers A82-%s, the newest entry at r5 generation. Root may add entries before the freeze.' % newest,
         'each row carries its section sha256; the freeze re-hashes the rows.',
         'RECOMMENDATION ONLY: every entry after %s up to the freeze gets a prereg successor or an explicit seal-record note; seal tools 1/4 receive exactly '
         'those entries as --covered-later.' % newest, ['A81 RI-26', 'A99.3']),
        ('RI-35', 'NOTE (rehearsal D-09)', 'status; decision_pins_pending_at_seal',
         'Seal tool 3 forbids changes outside seal_slots.<k>.value, so the sealed prereg keeps this draft\'s status line and the PENDING strings outside the '
         'slot values.', 'unchanged.', 'RECOMMENDATION ONLY: accept, and have the SEAL_RECORD state that it, not the prereg status line, is the authority on '
         'sealed status.', ['A82']),
        ('RI-36', 'PENDING_ROOT_RULING (driver check record)', 'seal_slots.driver; seal_record_requirements[8]',
         'PIN_V010_R5_CHECK has no A-entry naming it. Candidate: driver_r5/check/CHECK.md (89a6de88, the Claude-lineage r5 check, PASS_WITH_FINDINGS); Codex3 '
         '0602 (A69) is the other r5 check (rehearsal GAP-05).', 'unchanged.', 'RECOMMENDATION ONLY: root names the check record of record at A5/B2a.',
         ['A62.3', 'A67', 'A69']),
        ('RI-37', 'PENDING_ROOT_RULING (registry reading)', 'tests.SR_K; seal_slots.producer_registry',
         'Claude3 0087 registers only aggregate_records v008 (9794123d) as the SR_K gate-record producer in C3V009; sr_k_static v009 (cc2eb3bb) writes per-state '
         'component records (schema UNT_SR_K_STATE_CX1V001), whose custody is a runbook item (r12 review note B-N3). PRODUCER_INDEX_V009_CX3V001 lists both '
         'under SR_K. The SR_K clause names both as the sealed pinned producers (A88).', 'unchanged (A88 wording).',
         'RECOMMENDATION ONLY: root confirms Claude3\'s reading (the aggregator alone is the gate-record producer; sr_k_static custody on the producer side, '
         'in the RUNBOOK), or rules both into the registry.', ['A88', 'A99.5', 'Claude3 0087']),
    ]
    for rid, kind, clause, issue, draft, rec, srcs in new_items:
        doc['root_items'].append({'id': rid, 'kind': kind, 'clause': clause, 'issue': issue, 'draft': draft, 'recommendation': rec, 'sources': srcs, 'status': 'OPEN'})
    log('root_items.RI-28..RI-37', 'new', [], ['A81 RI-20', 'A99.1', 'R-10', 'R-09', 'GAP-18', 'GAP-14', 'A99.3', 'D-09', 'GAP-05', 'A88'], 'open items at r5')
    doc['root_items'].sort(key=lambda r: (r['status'] != 'OPEN', int(r['id'].split('-')[1])))
    # ================================================================= the entry table (A99.3)
    rows = []
    for e in later:
        dec, clauses, note = ROWS[e]
        head, b = secs[e]
        rows.append({'entry': e, 'heading': head, 'section_sha256': hashlib.sha256(b).hexdigest(), 'section_bytes': len(b),
                     'decision': dec, 'revised_clauses': clauses, ('scope' if dec == RH else 'reason'): note, 'sources': [e]})
    doc['entries_after_A81'] = {
        'rule': ('A99.3 (confirmed entry-by-entry table): every V005 entry from A82 to the freeze is either revised here (the clauses named) or no change, '
                 'because (the reason). This table covers A82-%s, the newest at r5 generation; the seal record quotes it; any later entry needs a successor '
                 'revision or an explicit seal-record note (A81 RI-26).' % newest),
        'section_rule': ('section_sha256 = sha256 of the V005 bytes from the first byte of the entry\'s heading line "## A<n>:" up to, not including, the first '
                         'byte of the next line that begins with "## " (or the end of the file). At the freeze each row is re-hashed from the frozen bytes; a '
                         'differing row means the entry changed after this text was written.'),
        'addendum_read': {'open_path': str(V005), 'sha256_at_generation': v005_observed, 'bytes': len(vb),
                          'byte_copy': 'addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md (same bytes; written by this generator)'},
        'rows': rows, 'sources': ['A81 RI-26', 'A99.3']}
    changed = {x for c in changes for x in expand(c['clause'])}
    for r in rows:
        for c in r['revised_clauses']:
            if c.startswith('SEAL_CHECKLIST') or c == 'entries_after_A81':
                continue
            if norm(c) not in changed:
                raise SystemExit('row %s names %s, which no edit changed' % (r['entry'], c))
    log('entries_after_A81', 'new', ['A81 RI-26', 'A99.3'], ['A99.3', 'D-05', 'GAP-02', 'R-02'], 'the entry-by-entry table A82-' + newest)
    # ================================================================= header
    doc['revision'] = 'r5'
    doc['status'] = ('FINAL DRAFT r5 (NOT SEALED). Assembled by Claude4 (dispatch 0621, A99) from r4 e3b6b5b2, integrating V005 A82-%s through the entry table '
                     'entries_after_A81 (each row revised here, or no change with the reason); open addendum observed %s at assembly. Written before any V007 '
                     '(tail-corrected) result exists; nothing was launched; C5H, UVT_* and targets were not read. binding_inputs.case_block pins '
                     'CASE_BLOCK_V007_C4V001 (A99.2, A101). The launch-packet BUILD of record is %s. Root fills the named seal slots and seals. Open root items: '
                     'ROOT_ITEMS_R5.' % (newest, v005_observed, b7txt))
    doc['assembly'] = {'by': 'Claude4 r5 helper (prereg r5 and the V007 case block), single author, under dispatch 0621 (A99)', 'utc': ts,
                       'dispatch': P['dispatch_0621'], 'base': {'path': str(R4), 'sha256': R4_SHA}, 'base_companions': r4_companions,
                       'rulings_read': dict(doc['assembly']['rulings_read'],
                                            V005_addendum_open_observed={'path': str(V005), 'sha256': v005_observed},
                                            V005_addendum_reads=doc['assembly']['rulings_read']['V005_addendum_reads'] + [
                                                {'read': 'r5 read 1, 20:22:09Z (A47-A99)', 'sha256': reads[0]['sha256'], 'copy': reads[0]['path']},
                                                {'read': 'r5 read 2, 20:41:18Z (adds A100 only)', 'sha256': reads[1]['sha256'], 'copy': reads[1]['path']},
                                                {'read': 'r5 read 3, 20:46:17Z (adds A101 only)', 'sha256': reads[2]['sha256'], 'copy': reads[2]['path']},
                                                {'read': 'r5 generation (this run)', 'sha256': v005_observed}]),
                       'inputs_verified_from_bytes': P}
    doc['decision_pins_pending_at_seal']['V005_addendum_frozen_copy']['entries'] = ('A47-%s at r5 generation (A82-%s in entries_after_A81); every entry up to '
                                                                                    'the freeze; cited by name until frozen' % (newest, newest))
    doc['cites_by_name'][0] = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM: A47-%s (open; pinned by its frozen copy, PENDING)' % newest
    log('status / assembly / decision_pins_pending_at_seal / cites_by_name', 'header', [], ['A99', 'A99.3'], 'r5 header and cited range A47-' + newest)
    doc['supersedes_draft'] = {'path': str(R4), 'sha256': R4_SHA}
    # ================================================================= checklist (root execution order)
    blist = ', '.join('%s %s' % (r['entry'], 'revised' if r['decision'] == RH else 'no change') for r in rows)
    check = [
        ('A. Before seal assembly (any order; each complete before step B1)', '', ''),
        ('A1. Final compare round r12 cx3v002 (4bd7b262; SELECTED_R12_CX3V001 91aa9747): its delta reviews of record, Claude3\'s and Codex2\'s, each report 0 '
         'blocking (A81 RI-20 as applied by A83, A86, A91, A96); its IMPL lists every NEW item with disposition and MUST_FAIL tests. Fix its reviewed source '
         '(seal-time pins unset) for the compare slot.', 'PENDING_ROOT_RULING: Codex2 0485 0 blocking; Claude3 0083 1 BLOCKING (A-B1); RI-28',
         'A96; A83; A91; R-02'),
        ('A2. Identity comparator: c2v007r2 (052da0fe), whose check of record is Codex2\'s 0472 (0 blocking); registered from C3V004.', 'DONE (A92)', 'A92; A83; A81 RI-21'),
        ('A3. Driver: v010 r5 (b5cc62af); r6 deferred, no cache directory.', 'DONE (A96)', 'A96; A89'),
        ('A4. CASCADE_MAP_R5_ADDENDUM written (immutable inventory addendum).', 'PENDING_ROOT_RULING (owner; RI-32)', 'A69; GAP-18'),
        ('A5. r5 identity runs compared by c2v007r2: records of record R5_V001 (B1 83e7b067, B1_OFF 3b9ad402, B0prime_RERUN e33af53d); the raw '
         'successor-custody check (root: a UVT_* read).', 'records DONE (A92); raw custody PENDING (root)', 'A92; A59; A67 N1'),
        ('A6. Successor B0 tool and B0 record rerun (B0-EMPTY) on r5. Candidate: the 0598 B0 record B0_R5_RECORD_C4V001 (c2cec35b; 64 counted PASS, 16 no '
         'evidence), registered in C3V007/C3V008.', 'CANDIDATE; root records done or names what is missing (RI-31)', 'A54; 0530; R-09'),
        ('A7. Certificates of record: EPS_CERT_V006 598c8fa3 (A70); LO_CERT_V004_MS128 1c384f76 (A70, A72); GQ_CERT_V006 5a1b39f8 (A86; V005 fbceefe6 '
         'superseded; V004 7ebb1d48 FAIL control); DOUBLING_MERGED_C3V001 ea48ac2b (A87; ddo_gas_M_s 128); LO_NGC_CERT_V002 33bc2190 (A87; reported only); '
         'EPS_NGC_91 1d5eef1b and I1T_NGC 3ae7981a (root confirms; GAP-12). Tool-3 slot ngc_gas_M_s = 96 (production_tail.ngc_gas_M_s; A81 RI-23 not '
         'triggered, Codex1 0032).', 'root confirms', 'A70; A86; A87; A81 RI-23; R-08'),
        ('A8. The merged DOUBLING record registered (C3V003 onward). Seal tool 3 v001 refuses it (D-01): seal tools v002 must read ddo_gas_M_s.',
         'registered; tool fix in seal tools v002', 'A87; A81 RI-22; D-01'),
        ('A9. Producer registry of record: candidate C3V009 (32ddadcb; Claude3 0087) = C3V008 (f189cd3f, final under A101) plus BUILD_V007\'s four post-seal '
         'producer pins (V6-N4); 13 registered records PASS on r12 with the case block of record. It carries SR_K by producer pins with PRODUCED_AFTER_THE_SEAL '
         '(A88), c2v007r2 and its tokens and the R5_V001 records (A92), B2 C3V003 (A101), the 0598 records; B0_N3, B0_RO1 and I4 are empty and fail closed '
         '(a record filling one means a V010).', 'CANDIDATE V009; root pins at assembly (RI-37 on the SR_K producer pin)', 'A62.2; A67 N2; A69.1; A88; A99.5; A101'),
        ('A10. Key-equivalence map for the seal record: equal to the case block\'s key_equivalence_map, which is [].', 'PENDING_ROOT_RULING (RI-30)', 'A48 AMB-13; R-10'),
        ('A11. Case block of record CASE_BLOCK_V007_C4V001 (%s) pinned at binding_inputs.case_block: valid under r12 validate_case_block (TESTED); Codex2 0507 '
         'PASS, zero findings.' % cbp[:8], 'DONE (A99.2, A101)', 'A99.2; A101; D-03'),
        ('A12. BUILD_V007 (Codex3 under A99.1) closing V6-S1 to V6-S3, 15 supported sources; Claude4 delta check; Claude2 adoption. This text binds it: '
         + ('filled from bytes, %s.' % b7 if bv7 else 'PENDING_BUILD_V007.'),
         ('LANDED; delta check and adoption PENDING (RI-29)' if bv7 else 'PENDING_BUILD_V007'), 'A99.1; D-02'),
        ('A13. B2 record of record B2_GATE_RECORD_C3V003 (915fbcda): PASS under A100; Codex2 0503 0 blocking; in C3V008.', 'DONE (A101)', 'A94; A97; A100; A101'),
        ('A14. B0_N3, B0_RO1 (b)(c) and I4 records on r5.', 'PENDING (runs missing; RI-33)', 'A87; GAP-14'),
        ('B. Seal assembly (strict order; every file exclusively created; none edited afterwards)', '', ''),
        ('B1. Freeze the V005 addendum: exclusive-create ..._V005_ADDENDUM_FROZEN.md after the last pre-seal entry; from then on root writes nothing to the open '
         'V005 file, and later entries go to a V006 addendum (A82, A99.6). Verify every A-entry this text cites (A47-%s) is present and each entries_after_A81 '
         'row re-hashes to its section_sha256 in the frozen bytes. Entries after A81 (D-05; A99.3): %s. A82-%s are cited here, so they are not --covered-later; '
         'only entries after %s with seal-record notes are (none at r5 generation).' % (newest, blist, newest, newest), 'PENDING (root)', 'A81 RI-26; A82; A99.3; A99.6; D-05'),
        ('B2. Fix the driver: v010 r5, path and sha from bytes (b5cc62af). No cache directory (NOT_APPLICABLE_R5).', 'PENDING (root)', 'A96'),
        ('B2a. Exclusive-create the driver BUILD record (PIN_DRIVER_BUILD_RECORD): schema UNT_V007_SEALED_DRIVER_BUILD_C2V001, build r5, predecessor r4, equal to '
         'compare r12\'s builtin_r5_build() with check_record = the driver check record of record (candidate driver_r5/check/CHECK.md 89a6de88; RI-36). The '
         'rehearsal\'s REHEARSAL DRAFT DRIVER_BUILD_R5_REHEARSAL_DRAFT_C4V001.json (2a3e4308; sealed r11 admitted it) is the template.', 'PENDING (root)',
         'A72; A82; D-06; GAP-04'),
        ('B3. Run the build-only binder on BUILD_V007\'s selected r5 template with the driver and frozen addendum pins: bound plan and command, exclusive create.',
         'PENDING (root)', '0576; A81 RI-25; A99.1'),
        ('B4. Write the sealed prereg: this text with every seal slot filled from bytes (binding_inputs.case_block is text, already pinned).', 'PENDING (root)', '0580; A81; A99.2'),
        ('B5. Create the sealed compare: the A1 reviewed source with exactly the five seal-time pins set (V007_PREREG_SHA256 = B4\'s sha, PIN_ADDENDUM_V005 = B1, '
         'PIN_DRIVER_BUILD_RECORD = B2a, PIN_V010_R5_CHECK, PIN_PRODUCER_REGISTRY = A9); verify it differs from the reviewed source only in those lines.',
         'PENDING (root)', 'A82; A67'),
        ('B6. Run --gates-only and --validity-only --case C5H with the sealed compare on the real records; keep the output; no row value shown (root only).',
         'PENDING (root)', 'A46 RA13; A47 I3'),
        ('B7. Exclusive-create the SEAL_RECORD: sealed prereg sha (first pin), sealed compare, driver, frozen addendum, bound plan and command shas; B6 output; '
         'E5-08; raw successor custody; the NEW-item disposition list; the key-equivalence map (A10); the entry table quoted (A99.3); the B2 disclosure and '
         'the A101 erratum (seal_record_requirements[12]); no-row-shown statement.', 'PENDING (root)', 'A81 RI-19/25; A99.3; A100; A101'),
        ('B8. Exclusive-create the ROOT_SEAL_ADMISSION config pinning the SEAL_RECORD sha, prereg, compare and BUILD_V007; its producer_allowlist names exactly '
         'BUILD_V007\'s 15 supported sources (launcher v007 and guard v008 by exact path).', 'PENDING (root)', '0561; A78 N2; A99.1; V6-S3'),
        ('B9. Exclusive-create the SEAL_ADMISSION_RECEIPT naming the config and seal shas; post it in a numbered root packet.', 'PENDING (root)', '0561; A81 RI-19'),
        ('C. Launch (Claude2 only)', '', ''),
        ('C1. Verify the receipt and config against the numbered root packet; export UNT_ROOT_ADMISSION_SHA256 from the published value; follow BUILD_V007\'s '
         'RUNBOOK (A85.2-4 root steps; SR_K first post-seal step, A88).', 'PENDING', 'RUNBOOK of BUILD_V007; A85; A88'),
        ('C2. Verify the bound plan and command shas from bytes immediately before running the command; run it (ramp-gated; KHI first).', 'PENDING',
         'A81 RI-25; A72; 0559'),
        ('Already DONE (preconditions)', '', ''),
        ('Driver r5 built (b5cc62af), dry runs 25/25, Codex3 review PASS_WITH_FINDINGS; Claude-lineage check (driver_r5/check, 89a6de88) PASS_WITH_FINDINGS.',
         'DONE', 'A67; A69'),
        ('B3 record of record B3_RECORD_C4V001 (83c853b9; A87; the human report GATE_B3_C4_V002 465cb3c3); PICARD member specs gates_v004 PASS; P128/M_s 128 '
         'spec set registered (c7023846); identity records R5_V001 (A92); BUILD_V006 reviewed PASS_WITH_FINDINGS (A99); the case block (A101).', 'DONE',
         'A87; A68; A92; A99; A101'),
        ('SUPERSEDED', '', ''),
        ('Compare r8, r10, r11; comparators c2v004-c2v006; BUILD_V005 and BUILD_V006 as the BUILD of record (A99.1); B2 C3V002 d4b41ffc (A100, A101); r6 (A96); '
         'the r4 checklist.', 'SUPERSEDED', 'A79; A80; A90; A96; A99; A101'),
    ]
    # ================================================================= write
    out.mkdir(parents=True, exist_ok=True)
    (out / 'addendum_read').mkdir(exist_ok=True)
    written = []

    def write(name, data):
        p = out / name
        with p.open('xb') as f:
            f.write(data if isinstance(data, bytes) else data.encode('utf-8'))
        written.append(p)
        return p
    write('addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md', vb)
    write('KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json', json.dumps(doc, indent=1, ensure_ascii=False, allow_nan=False) + '\n')
    D = ['# Delta r4 -> r5 (KMAX_TAIL_PREREG_V007_FINAL_DRAFT)', '',
         'Each line is one recorded edit applied to r4 (e3b6b5b2) by ' + Path(__file__).name + ', with its trace to a ruling (A-entry), a rehearsal defect '
         '(D-), gap (GAP-) or refuter correction (R-). Open V005 addendum at generation: %s (entries A47-%s).' % (v005_observed, newest), '',
         '| # | clause | kind | added sources | trace | why |', '|---|---|---|---|---|---|']
    D += ['| %d | `%s` | %s | %s | %s | %s |' % (i + 1, norm(c['clause']), c['kind'], '; '.join(c['added_sources']), '; '.join(c['trace']), c['why'])
          for i, c in enumerate(changes)]
    write('DELTA_R4_R5.md', '\n'.join(D) + '\n')
    E = ['# ENTRY_TABLE_R5: V005 entries A82-%s against prereg r5 (A99.3; the seal record quotes this table)' % newest, '',
         'Open V005 addendum read at r5 generation: sha256 `%s`, %d bytes (byte copy `addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md`). %s' % (
             v005_observed, len(vb), doc['entries_after_A81']['section_rule']), '',
         '| entry | decision | section sha256 | revised clauses / reason |', '|---|---|---|---|']
    for r in rows:
        E.append('| %s | %s | `%s` | %s |' % (r['entry'], 'revised here' if r['decision'] == RH else 'no change',
                                             r['section_sha256'], ('%s. Clauses: %s' % (r['scope'].rstrip('.'), ', '.join('`%s`' % c for c in r['revised_clauses'])))
                                             if r['decision'] == RH else r['reason']))
    write('ENTRY_TABLE_R5.md', '\n'.join(E) + '\n')
    ri = doc['root_items']
    Rr = ['# Root items r5: KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5 (unsealed)', '',
          'RI-27 is resolved by A82 (ruled as drafted in r4). RI-24 is moot for V007 (A96). Open: %s. Every recommendation is a recommendation only.'
          % ', '.join(r['id'] for r in ri if r['status'] == 'OPEN'), '']
    for r in ri:
        Rr += ['## %s: %s (%s)' % (r['id'], r['kind'], 'OPEN' if r['status'] == 'OPEN' else 'RESOLVED'), '', '- **Status:** %s' % r['status'],
               '- **Clause:** `%s`' % r['clause'], '- **Issue:** %s' % r['issue'], '- **Draft:** %s' % r['draft']]
        if 'recommendation' in r:
            Rr.append('- **Recommendation:** %s' % r['recommendation'])
        Rr += ['- **Sources:** %s' % '; '.join(r['sources']), '']
    write('ROOT_ITEMS_R5.md', '\n'.join(Rr))
    S = ['# SEAL_CHECKLIST r5: V007, in the order root will execute it', '',
         'State at assembly (%s). The draft is unsealed; the slots stay PENDING except where a ruling fixes them (cache slot NOT_APPLICABLE_R5, A96).' % ts, '',
         '| step | state | source |', '|---|---|---|']
    for a, b, c_ in check:
        S.append('| **%s** | | |' % a if not b else '| %s | %s | %s |' % (a, b, c_))
    write('SEAL_CHECKLIST_R5.md', '\n'.join(S) + '\n')
    rowsm = []

    def walk(prefix, obj):
        if isinstance(obj, dict) and 'text' in obj and 'sources' in obj:
            rowsm.append((prefix, obj['sources']))
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(prefix + '.' + k if prefix else k, v)
    for sec in ('binding_inputs', 'fixed_across_all_cases', 'pairing_and_decidability_rule', 'gates_before_any_T_result', 'tests', 'decision_rule', 'run_list'):
        walk(sec, doc[sec])
    for o in doc['outcomes_first_applicable']:
        rowsm.append(('outcomes_first_applicable.%s' % o['outcome'], o['sources']))
    for i, r in enumerate(doc['seal_record_requirements']):
        rowsm.append(('seal_record_requirements[%d]' % i, r['sources']))
    rowsm.append(('ngc3198_N_tests', doc['ngc3198_N_tests']['sources']))
    for k, s in doc['seal_slots'].items():
        rowsm.append(('seal_slots.%s' % k, s['sources']))
    rowsm.append(('not_v007_text_scope', doc['not_v007_text_scope']['sources']))
    for r in rows:
        rowsm.append(('entries_after_A81.%s (%s)' % (r['entry'], r['decision']), r['sources']))
    M = ['# Clause -> source map, r5: KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5 (unsealed)', '',
         'Sources are rulings (A-entries, dispatches) or evidence; the trace of every r5 edit to a ruling, defect, gap or refuter correction is in DELTA_R4_R5.md.',
         '', '| clause | sources | changed in r5 |', '|---|---|---|']
    changed_all = {x for c in changes for x in expand(c['clause'])}
    M += ['| `%s` | %s | %s |' % (k, '; '.join(s), 'yes' if (norm(k) in changed_all or k.startswith('entries_after_A81')) else '')
          for k, s in rowsm]
    write('CLAUSE_SOURCE_MAP_R5.md', '\n'.join(M) + '\n')
    H = ['# KMAX_TAIL_PREREG_V007: final draft r5 (UNSEALED)', '', doc['status'], '',
         '**Assembly:** Claude4 r5 helper, single author, UTC %s. Base: r4 `%s`. Dispatch 0621 `%s`.' % (ts, R4_SHA, P['dispatch_0621']['sha256']), '',
         'The full clause text is in the JSON; `CLAUSE_SOURCE_MAP_R5.md` traces every clause; `DELTA_R4_R5.md` lists every edit with its trace; '
         '`ENTRY_TABLE_R5.md` is the A99.3 table; `SEAL_CHECKLIST_R5.md` and `ROOT_ITEMS_R5.md` are the root-facing lists.', '',
         '## The case block (A99.2, A101)', '', '- `binding_inputs.case_block`: `%s` sha256 `%s`.' % (P['case_block']['path'], cbp),
         '- %s' % bi['case_block_rule']['text'], '', '## The launch-packet BUILD of record (A99.1)', '',
         '- %s' % (('BUILD_V007 `%s` sha256 `%s` (filled from bytes; 15 supported sources verified; template %s launches the case block\'s ten FILLED specs; '
                    'Claude4 delta check and Claude2 adoption pending).' % (bv7['path'], b7, bv7_check['named']['template_plan']['sha256'][:8])) if bv7 else
                   'BUILD_V007: `PENDING_BUILD_V007` (not on disk at generation).'), '',
         '## Seal slots (root fills at seal assembly; never guessed)', '']
    for k, s in doc['seal_slots'].items():
        H.append('- **%s**: value `%s`. %s  \n  *Sources: %s*' % (k, s['value'], s['rule'], '; '.join(s['sources'])))
    H.extend(['', '## Entry table A82-%s (A99.3)' % newest, '', '| entry | decision | section sha256 |', '|---|---|---|'])
    H += ['| %s | %s | `%s` |' % (r['entry'], 'revised here' if r['decision'] == RH else 'no change', r['section_sha256'][:16] + '...') for r in rows]
    H.extend(['', '## Seal record requirements', ''])
    for r in doc['seal_record_requirements']:
        H.append('- %s *(%s)*' % (r['text'], '; '.join(r['sources'])))
    H.extend(['', '## Clauses changed in r5', ''])
    for c in changes:
        H.append('- `%s` (%s; trace %s): %s' % (c['clause'], c['kind'], ', '.join(c['trace']), c['why']))
    H.extend(['', '## Root items', '', 'RI-27 RESOLVED (A82); RI-24 moot (A96). OPEN: %s (see `ROOT_ITEMS_R5.md`).' % ', '.join(
        r['id'] for r in ri if r['status'] == 'OPEN'), ''])
    write('KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.md', '\n'.join(H) + '\n')
    hp = [P['case_block']['path'], P['case_block_build_record']['path']] + [str(p) for p in written]
    hrows = ['%s  %s' % (sha(p), p) for p in hp]
    write('HASHES_R5.txt', '\n'.join(hrows) + '\n')
    print('written', out, len(written), 'files; V005 observed', v005_observed, 'newest', newest, '; rows', len(rows), '; edits', len(changes),
          '; BUILD_V007', b7 or PENDING_BUILD, '; open', [r['id'] for r in ri if r['status'] == 'OPEN'])
    print('prereg r5 sha256', sha(out / 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json'))


if __name__ == '__main__':
    main()
