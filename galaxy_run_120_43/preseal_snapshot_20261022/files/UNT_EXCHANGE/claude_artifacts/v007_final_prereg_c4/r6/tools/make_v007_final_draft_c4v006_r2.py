# Claude4 r6 helper, continuation run 2 (A106.1 approves prereg r6; dispatch 0643; Claude4 0109 and 0110; r5 check REPORT_R5CHK_C4V002
# F-01, F-02, F-11, F-13): prereg r6 = prereg r5 (3245899f) plus recorded edits, each traced to a ruling (V005 A102-A106) or an r5-check
# finding, rendered to JSON and Markdown together.
# This file is the successor, before any use, of the first builder's draft make_v007_final_draft_c4v006.py (8787e164), which was stopped
# at 23:03Z because A106 arrived after its V005 read. It is a direct rewrite (no patch script); the diffs against that draft and against
# r5's generator make_v007_final_draft_c4v005_p3.py (ef00666c) are written to tools/ by make_diffs_c4r6.py.
#  - V005 is CLOSED at A106 (A106.3; 0643). The entries are read only from the exclusive byte copy
#    r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md, which must hash to the closed sha and hold the closed size; the live file
#    must still hash to the same sha (else refuse: a change to the closed file is a defect for root).
#  - r5 and every pinned input are read from bytes; a missing file or a sha256 that differs from the full pinned value refuses.
#  - r5's 20 rows A82-A101 must re-hash from the copy (heading, section sha256, section bytes); A47-A101 and the preamble must be
#    byte-equal to r5's own copy; every entry after A101 gets a row (an entry without a row refuses), and A106 must be the newest entry.
#  - Every edit is logged (brief item, clause, kind, added sources, trace, why). Both ways: every clause a REVISED_HERE row names is
#    changed by a logged edit whose trace names that entry, and every edit whose trace names an entry after A101 changes a clause that
#    entry's row names. The leaf diff r5 -> r6 lies inside logged clauses, and every logged clause changes at least one leaf.
#  - The r13 lines the text cites are verified from bytes; r12 and r13 are read as text, and no compare module is imported.
#  - All outputs are built in memory; none may exist; each is then exclusively created. Nothing is overwritten.
# Usage: TS=$(date -u +%Y-%m-%dT%H:%M:%SZ) OUT_DIR=<the r6 folder, or a new folder inside r6/scratch for a dry run> python3 -I -B <this>
import copy, difflib, hashlib, json, os, re
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE'); CA = EX / 'claude_artifacts'; PKT = CA / 'v007_launch_packet_cx1'
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
PR = CA / 'v007_final_prereg_c4'; R5D = PR / 'r5'; R6D = PR / 'r6'; ST3 = PR / 'seal_tools_v003'
R5 = R5D / 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json'
R5_SHA = '3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393'
V005 = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
V005_CLOSED_SHA = 'c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1'     # A106.3; 0643 (pasted from shasum)
V005_CLOSED_BYTES = 143081
V005_LAST = 'A106'
COPY_REL = 'addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md'
COPY = R6D / COPY_REL
R5_COPY = R5D / 'addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md'
R12 = CA / 'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py'
R12_SHA = '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28'
R13 = CA / 'v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py'
R13_SHA = 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'
BUILD_HEADER = '## Supported runtime entry allowlist'
HEX64 = re.compile(r'[0-9a-f]{64}')
RH, NC = 'REVISED_HERE', 'NO_CHANGE'
R5_COMPANIONS = (
    ('KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.md', '2ed287717a831b422d93ad62339a85aa5b1ffbc570d39bd3ddc6066e8989c208'),
    ('ENTRY_TABLE_R5.md', 'b4bf8392db0ed5919b9583cf2f8b71b4d1ec26fd3c735cfd622e9cb81ac3063e'),
    ('SEAL_CHECKLIST_R5.md', '7ff81720e6cf108a6f71d478dcc23493fb1ee943ed2c90e88873715a2921bd13'),
    ('ROOT_ITEMS_R5.md', '2387dc23c790a894b6f969d133d48eb0a095f46ed97448fce67070ed59cdd3d4'),
    ('CLAUSE_SOURCE_MAP_R5.md', '378202ec67f93ddbee2233828ff18432af45b77f42d7c993321bb589ab340b31'),
    ('DELTA_R4_R5.md', '741cb7985125f1cb705a289001a329aee74c6c8314b80b1877a7c72d88e6fd4a'),
    ('DELTA_R4_R5_ERRATUM_E1.md', 'b68a1f539cd0c6e9a4fe5bc4d841d0ceae7c2070a37bb05d2f4f09d46fdc10e8'),
    ('HASHES_R5.txt', '21fe01a4a8f6d6888bdd32f15a8e2229987de8f9cff8d068500e113bfa2d1f8a'),
    ('addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md', '70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e'))
R5_GENERATORS = (
    ('tools/make_v007_final_draft_c4v005_p3.py', 'ef00666cd85ba280f781d8bbb16223573d915bec4f9b4fe503d20e4c23026a30'),
    ('tools/make_v007_final_draft_c4v005_p2.py', '4fd17fcc5c98be05145e717ac7ed20fdc2b7b7a9d17a763d45c682443be14e69'),
    ('tools/make_v007_final_draft_c4v005.py', 'f4de79cb9894ca6c10247cf5f1a11ddaa6f581c8a702d21e84195d162c006c4e'),
    ('tools/patch_gen_c4v005_p2.py', 'c331958a47b8523c5fbf432b91ebabdc11bb750a6d12fca64572b838e79982a1'),
    ('tools/patch_gen_c4v005_p3.py', 'eded69a1669bc51a7ac9aa4d2419f1fa53f813d9f050873e6bdaedc53023759c'))
OUT_NAMES = ('KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json', 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.md', 'ENTRY_TABLE_R6.md', 'SEAL_CHECKLIST_R6.md',
             'ROOT_ITEMS_R6.md', 'CLAUSE_SOURCE_MAP_R6.md', 'DELTA_R5_R6.md')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin(p, full):
    p = Path(p)
    if not HEX64.fullmatch(full or ''):
        raise SystemExit('a pin needs a full sha256: %s' % p)
    if not p.is_file():
        raise SystemExit('missing ' + str(p))
    h = sha(p)
    if h != full:
        raise SystemExit('pin %s != bytes %s for %s' % (full[:12], h[:12], p))
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


def sections(b):
    """V005 entry sections (prereg r5 section_rule): from the first byte of a heading line '## A<n>:' up to, not including, the first
    byte of the next line that begins with '## ' (or the end of the file)."""
    starts = [m.start() for m in re.finditer(rb'(?m)^## ', b)]
    out = {}
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(b)
        head = b[s:b.index(b'\n', s)].decode('utf-8')
        m = re.match(r'## (A[0-9]+):', head)
        if m:
            if m.group(1) in out:
                raise SystemExit('duplicate entry heading ' + m.group(1))
            out[m.group(1)] = (head, b[s:e])
    return out


def leaves(o, p=()):
    """flat {path tuple: json text}; root_items keyed by id and entries_after_A81 rows keyed by entry, so a reorder is not a change."""
    if isinstance(o, dict):
        if not o:
            return {p: '{}'}
        r = {}
        for k, v in o.items():
            r.update(leaves(v, p + (k,)))
        return r
    if isinstance(o, list):
        if not o:
            return {p: '[]'}
        r = {}
        for i, v in enumerate(o):
            key = i
            if p == ('root_items',) and isinstance(v, dict) and 'id' in v:
                key = v['id']
            elif p == ('entries_after_A81', 'rows') and isinstance(v, dict) and 'entry' in v:
                key = v['entry']
            r.update(leaves(v, p + (key,)))
        return r
    return {p: json.dumps(o, ensure_ascii=False)}


def pname(p):
    s = ''
    for k in p:
        s += ('[%d]' % k) if isinstance(k, int) else (('.' if s else '') + str(k))
    return s


def covers(c, leaf):
    return leaf == c or leaf.startswith(c + '.') or leaf.startswith(c + '[')


# ------------------------------------------------------------------ the A99.3 entry-table rows for the entries after A101 (A102-A106)
ROWS6 = {
    'A102': (RH, ['seal_slots.compare', 'outcome_branch_tests_required', 'root_items.RI-28', 'root_items.RI-20',
                  'SEAL_CHECKLIST_R6 A1, SUPERSEDED'],
             'A102 rules that Claude3\'s r12 delta review of record (0083: FAIL, 1 blocking, A-B1) requires a fix round under A81 RI-20: Codex3 '
             'builds r13 = r12 plus exactly the A-B1 fix (parse_int=str inside the duplicate-hook parse; the text fallback only on '
             'json.JSONDecodeError), the A-B1 forms V01-V07 become MUST_FAIL tests, Claude3 and Codex2 delta-check r13, and prereg r5\'s compare '
             'slot takes r13 once both report 0 blocking. r6 names r13 as the final round with r12 superseded, removes r5\'s "or a ruling on the '
             'item" (a blocking item in a review of record means a fix round; r5 check F-02), resolves RI-28, points RI-20 to A102 and lists '
             'compare r12 as superseded in the checklist.'),
    'A103': (RH, ['seal_slots.compare', 'root_items.RI-20', 'not_v007_text_scope', 'SEAL_CHECKLIST_R6 A1'],
             'A103 makes Codex1 the cross-lineage r13 delta reviewer of record in place of Codex2 (out of usage; A81 RI-20 named Codex2), and '
             'accepts cx3r008 as the step-5 NGC driver in place of cx3r007, its registry pinned from bytes before step 5. r6 names Codex1\'s review '
             'of record in the compare slot and checklist A1, points RI-20 to A103 and names cx3r008 in the scope note. Its other reassignments '
             '(the seal pre-stage cross-check, the miss-reading r3 delta, the step-4 reviews) and Codex3\'s reduced role change no clause of this '
             'text.'),
    'A104': (RH, ['seal_slots.compare', 'outcome_branch_tests_required', 'root_items.RI-28', 'root_items.RI-20', 'binding_inputs.case_block_rule',
                  'fixed_across_all_cases.validity_gates', 'gates_before_any_T_result.after_seal_marker_policy', 'seal_record_requirements[11]',
                  'status', 'SEAL_CHECKLIST_R6 A1, B1, B2a'],
             'A104: both delta reviews of record report 0 blocking (Codex1 0076 PASS; Claude3 0092 PASS_WITH_FINDINGS), so compare r13 (f5adfd11, '
             'selected by SELECTED_R13_CX3V001 10acd098) is the compare of record and the sealed compare sets only the five A82 pins on top of it; '
             'and D-05 is made mechanical (0640): a cited entry whose bytes changed is dispositioned revised, or no_change_after_change with a '
             'changed_text excerpt and a reason. r6 names r13 in the compare slot, the outcome-test clause, the status line and checklist A1, '
             'resolves RI-28, moves the compare line citations to r13 (r12 L5706 is r13 L5708; L338 and L341 are unchanged; checklist B2a cites '
             'r13\'s builtin_r5_build, whose text equals r12\'s), and states the D-05 disposition rule in seal_record_requirements[11] and '
             'checklist B1.'),
    'A105': (RH, ['seal_slots.launch_packet', 'root_items.RI-29', 'seal_record_requirements[0]', 'status', 'SEAL_CHECKLIST_R6 A12, B3, B7, B8, C1'],
             'A105: Claude4 0108 is PASS_WITH_FINDINGS with 0 blocking, V6-S1 to V6-S3 are closed and BUILD_V007 (94bc05a5) stays bound; root '
             'rules W7-S1 (the admission config lists exactly BUILD_V007\'s 15 rows; the seal script builds it from BUILD_V007\'s table and '
             'refuses any other row count), RP-S1 (the seal script exclusively creates the step-2 output root before binding) and RP-S2 (outputs '
             'stay on the internal SSD, an 80 GB free-space watchdog, caps unchanged), and discloses E-OPS5 (root\'s du -sh on the C5H run '
             'directory, metadata only) in the seal record\'s E-SEAL1 block. r6 records these in the launch-packet slot, RI-29 (resolved), '
             'seal_record_requirements[0], the status line and checklist A12, B3, B7, B8 and C1. A105\'s disk figures (992 GiB of caps, 452 GiB '
             'free, the measured Z2, B0P and C5H sizes) are root\'s launch-day measurements, not text.'),
    'A106': (RH, ['status', 'revision', 'supersedes_draft', 'assembly', 'entries_after_A81', 'seal_slots.frozen_addendum',
                  'decision_pins_pending_at_seal.V005_addendum_frozen_copy', 'cites_by_name', 'seal_slots.compare', 'seal_slots.producer_registry',
                  'seal_record_requirements[11]', 'seal_record_requirements[13]', 'root_items.RI-29', 'root_items.RI-34',
                  'SEAL_CHECKLIST_R6 A8, B1, B7, SUPERSEDED'],
             'A106.1 approves prereg r6 (Claude4 0109, F-01): r5 plus the rows A102-A106 read from the closed bytes, the r13 compare slot with its '
             'reviews of record (Claude3 0092, Codex1 0076), F-02, BUILD_V007 per A105, the E-OPS5 disclosure and the F-11 fixes, with the case '
             'block 76309ae3, BUILD_V007 94bc05a5 and registry V009 32ddadcb bindings unchanged; this revision is that r6 (header, status, F-02 '
             'in the compare slot, V009 the registry candidate). A106.2 fixes the seal-tool scope: seal tools v003 carry D-05 (with C-01, which '
             'compares every cited entry against the prereg\'s pinned text-of-record bytes), B8, the README fix and the W7-S1 MUST_FAIL cases, and '
             'nothing more; C-02 to C-06 are exactness checks in Claude3\'s seal script, and C-03 and C-08 are in it if each takes 10 minutes or '
             'less, otherwise root checks them by hand and the seal record says so (seal_record_requirements[13] and checklist B7 carry that '
             'statement; seal_record_requirements[11], RI-29, RI-34 and checklist A8 and B1 name v003). A106.3 closes V005 at A106: later root rulings go in the V006 addendum, the table ends at A106 and the frozen copy must '
             'equal these bytes (the entry-table rule, the frozen-addendum slot rule, the pending frozen-copy pin, cites_by_name, '
             'seal_record_requirements[11], RI-34 resolved, checklist B1). A106\'s direction that Codex1 cross-checks r6 is not text.'),
}

# ------------------------------------------------------------------ inputs read from bytes at r6 generation (full sha256, pasted from shasum)
INPUTS = (
    ('dispatch_0643', EX / 'FROM_CODEX/0643_2026-10-18_claude4_claude3_codex1_A106_final_V005.md', '2926f7ab57cac05168d079807224f05317d2b71e0f0a86e7a78b92e98005172e'),
    ('Claude4_0110', EX / 'FROM_CLAUDE4/0110_2026-10-18_ack_0643_r6_through_A106_v003_option_b.md', 'a2c90720a9d1bfde26acaf5933a1eec2ead8b8ff03c1c3d646c388d0060af48f'),
    ('Claude4_0109', EX / 'FROM_CLAUDE4/0109_2026-10-18_r5_check_r6_recommended_v002_check_scope.md', 'd0b20717170661f7bcc7b5866fd6f8c074dc5058929c4e669d0515c962983bc7'),
    ('r5_check_report_C4V002', PR / 'r5_check/REPORT_R5CHK_C4V002.md', 'caea77aae21e19419c6d61778edb1f3ed984bf0ba21e82bbf595382dcfa3dacd'),
    ('r5_check_results_C4V002', PR / 'r5_check/RESULTS_R5CHK_C4V002.json', 'dc2a661ec5571f56f9a1fa17cfbd3f94f1591234a77360732dda893586333ae6'),
    ('dispatch_0621_r5', EX / 'FROM_CODEX/0621_2026-10-18_claude4_codex1_codex3_claude3_A99.md', '7ab78e6a0aa4c3d11d6c4dd9887ea2fc8b65e40a84bc75de387a319534b99504'),
    ('dispatch_0629', EX / 'FROM_CODEX/0629_2026-10-18_codex3_r13_A_B1_fix.md', 'ca8606b0d89c449c912bb36b745ba4f3a3a6c250221d865acb9c909907b88b21'),
    ('dispatch_0632', EX / 'FROM_CODEX/0632_2026-10-18_claude3_codex2_r13_frozen_delta_now.md', '27c9b70ad5b40c2274036ad0531df8e4ed758a39d8947349e38e8270e04e8e79'),
    ('dispatch_0633', EX / 'FROM_CODEX/0633_2026-10-18_claude4_seal_tools_v003_D05.md', '3b3e0d4a8be56e6a3a49d6aca3cb9e0c40f752481a96344e8ca7d0c7a3edb83b'),
    ('dispatch_0634', EX / 'FROM_CODEX/0634_2026-10-18_claude4_v003_add_B8.md', 'eda276080429e2bceba2925bf8485f8b8a73069b56aba5931e6f8cca99f489da'),
    ('dispatch_0635', EX / 'FROM_CODEX/0635_2026-10-18_reassign_codex2_queue.md', 'c6fd229feeef4c399198118d5c1465a1af9a5bff029f44865e1813b5eeec9758'),
    ('dispatch_0636', EX / 'FROM_CODEX/0636_2026-10-18_codex3_conserve_codex1_takes_prestage.md', '6b29ccf2ef10e7643975c79b232a98bd080968044acfedde7a18606aa0265621'),
    ('dispatch_0638', EX / 'FROM_CODEX/0638_2026-10-18_codex1_takes_v003_codex3_reserve.md', 'cc02bdbc54d5a33da07c3629772564d2538083412a790ddc9f841d37e9e54fcb'),
    ('dispatch_0640', EX / 'FROM_CODEX/0640_2026-10-18_claude4_claude3_D05_rule_and_contract.md', '03b4ff4987fd3a82a3a46692a7ab75beddd9d78788373863ea3b2dcd3db91138'),
    ('dispatch_0641', EX / 'FROM_CODEX/0641_2026-10-18_claude3_N1_nonblocking_publish.md', '1fe3f2e9b934e0cd13e69d606c428601230c7a5619cf67bd0d5a79d76c829841'),
    ('dispatch_0642', EX / 'FROM_CODEX/0642_2026-10-18_claude3_script_add_RP_S1_W7_S1.md', 'b96f14fb3116cb277ff4b14ebf7e51f0c73ad8de1333464aa783cd799ad9ea74'),
    ('r13_compare', R13, R13_SHA),
    ('r13_selected', CA / 'v007_compare_c2/r13/SELECTED_R13_CX3V001.json', '10acd09887bffa5130e2ebbff7d54ab2d70ea7aff0fb2cd696e0cda0fcf6bb5e'),
    ('r13_fields', CA / 'v007_compare_c2/r13/FIELDS_R13_CX3V001.md', '7b116b0103fdeb83d2cd358976e2c901be15313ad7f9ab8d159af6d9ee3bb365'),
    ('r13_impl', CA / 'v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md', '274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3'),
    ('r13_hashes', CA / 'v007_compare_c2/r13/HASHES_R13_CX3V001.json', 'd4509325af5feae7f3e5bcc15552c38004072f525cebb7a9da111940a4985557'),
    ('r12_compare', R12, R12_SHA),
    ('Claude3_0092', EX / 'FROM_CLAUDE3/0092_2026-10-18_r13-delta-PASS_WITH_FINDINGS-0-blocking.md', 'c82772750777733863c4a1779167367ec6e240782ff3e0e590d2fbd7f361ba8b'),
    ('r13_review_Claude3', CA / 'review_v007_compare_c3/r13_review/REVIEW_V007_COMPARE_R13_C3V001.md', '35271b95ebff58a0fe630673d6424b4994f2391f5f04270b86bb940dd4b98a7f'),
    ('r13_review_Claude3_hashes', CA / 'review_v007_compare_c3/r13_review/HASHES_REVIEW_V007_R13_C3V001.txt', '0430f0009b4ed9296922767ac5dadf8ea2345b6e21e3c8316d95cfaf99d94e92'),
    ('Codex1_0076', EX / 'FROM_CODEX1/0076_2026-10-18_r13_delta_PASS_zero_blocking.md', 'd1da986c921b76f284ed69686944d652abf8c7712b1a08eb5fff2f2763eee613'),
    ('r13_review_Codex1', CA / 'review_r13_delta_cx1/REVIEW_R13_CX1V001.json', '0005519b934169a75c88276f122e773d27900d2bab708783626268cdf1b954e8'),
    ('Claude3_0083', EX / 'FROM_CLAUDE3/0083_2026-10-18_r12-delta-FAIL-1-blocking-A-B1.md', '8fe311ba47a7e831ae794927945fc6a499e36e091f3e19cc975718538d1659d9'),
    ('Codex2_0485', EX / 'FROM_CODEX2/0485_2026-10-18_0614_r12_delta_finished_zero_blocking.md', 'f2bfc8a5240d76668e22596271b47db16cd431448d602668a938fdb049d80711'),
    ('Claude4_0108', EX / 'FROM_CLAUDE4/0108_2026-10-18_build_v007_delta_PASS_WITH_FINDINGS.md', '766d183bfd03ff0b5c3665e4cbe864d7562d96123c99cbdfacfc24f05e9b1b09'),
    ('build_v007_review_Claude4', CA / 'review_build_v007_c4/REVIEW_BUILD_V007_C4V001.md', '6ed80d59dee135d2202622295bc404e9a48569992ba8a025badf445c2f48b06f'),
    ('build_v007_review_Claude4_hashes', CA / 'review_build_v007_c4/HASHES_REVIEW_BUILD_V007_C4V001.txt', 'c1a1a0f28cb22678dccfa1810761feae9ca6b3e242e7193f9a123b71754916ae'),
    ('build_v007', PKT / 'BUILD_V007.md', '94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de'),
    ('build_v006', PKT / 'BUILD_V006.md', 'fb9e6a4a19395f35b9929fb163df6305c1b472f504266e2b4b98453f5bbb004f'),
    ('Claude4_0104', EX / 'FROM_CLAUDE4/0104_2026-10-18_cx3r008_delta_PASS_WITH_FINDINGS.md', '57a8267851ab3fd7996d547617dafcadc19dd4cb04a0622170003cd21c86bea4'),
    ('registry_c3v009', CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json', '32ddadcb7567213f42288004f19def122da1d8c4db1a426f0f888bc3242484e8'),
    ('registry_c3v008', CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V008.json', 'f189cd3fcd45426c23ba8600104a0a2ebf8ca7bcb453327aae19e6ebc1ee1120'),
    ('validate_r12_c3v009', CA / 'producer_registry_c3/out/VALIDATE_R12_C3V009_CASEBLOCK_OF_RECORD.json', '537d1a428c690a8ebb5a1ac8bdb4ab31e469566c9e869153f017eb4d66f158d9'),
    ('validate_r13_c3v009', CA / 'producer_registry_c3/out/VALIDATE_R13_C3V009_CASEBLOCK_OF_RECORD.json', 'f14dd9a65a4c27365e802aeef49625923618b6eef0120e73cfd25f4cdb5e971f'),
    ('Claude3_0087', EX / 'FROM_CLAUDE3/0087_2026-10-18_registry-V009-BUILD_V007-producers-final.md', '0f99076eb97d6d4bcb53e7aab1d7ab18c8b8c09a8a12927e8d7c43d531c1a5d9'),
    ('gq_ngc_91_ms96', CA / 'ngc_ntest_eval_cx/out/GQ_NGC_91_MS96_V001.json', 'be148bab4d80ef412d55d2011cac2e3a1d44725a0ba21a4d2bf43c7ffbdc1a76'),
    ('Codex1_0032', EX / 'FROM_CODEX1/0032_2026-10-18_gq91_pass_and_latest_rulings.md', '3e8c9fc9e65a10791f8ecbda3702556a851391350f06ed013222bd12876ab2f7'),
    ('case_block', R5D / 'case_block/CASE_BLOCK_V007_C4V001.json', '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'),
    ('case_block_build_record', R5D / 'out/CASE_BLOCK_BUILD_C4V001.json', 'bcf560de77cd42f67fedb62744df0723a052c1f2ffc4f4b2a7bed874eb5b59ad'),
    ('fence_c4v002_r6_copy', R6D / 'tools/fence_c4v002.py', '53078e39b34a22d1ee83e5b2d68c85e7644970838a2c88974397bb31912c1a4e'),
    ('run_fenced_c4r6_v2', R6D / 'tools/run_fenced_c4r6_v2.py', '843e0cfbf76fb03baf57414e89fd0c0786b9a8ba5667d7cf1b87c5d9b9cb5631'),
    ('copy_addendum_c4r6_v2', R6D / 'tools/copy_addendum_c4r6_v2.py', 'a9957506a92e9b935a638ef8f19dc7a8428e0c345dc43335c09bc0047a3f412d'),
    ('first_builder_draft_generator', R6D / 'tools/make_v007_final_draft_c4v006.py', '8787e164d5eecb90da281ef69edb113131de442d8635eea6f26803fc39518cbe'))

# ------------------------------------------------------------------ r5 texts this generator replaces whole (asserted equal before the edit)
R5_SRR11 = ('Any A-entry after A81 that touches this text needs a successor revision or an explicit no-change note in the seal record; the seal check '
            'verifies that every A-entry this text cites is present in the frozen bytes. The entry table entries_after_A81 lists every entry from A82 '
            'to the newest at r5 generation (A101) as revised here (with its clauses) or no change (with the reason), each with its section sha256 '
            'read from bytes, and the seal record quotes it (A99.3). At the freeze each row\'s section is re-hashed from the frozen bytes: a row whose '
            'section differs, and any entry after A101 without a row, needs a successor revision or an explicit seal-record note (A81 RI-26).')
R5_FROZEN_ENTRIES = 'A47-A101 at r5 generation (A82-A101 in entries_after_A81); every entry up to the freeze; cited by name until frozen'
R5_CITES0 = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM: A47-A101 (open; pinned by its frozen copy, PENDING)'


def line_checks():
    """the r13 lines this text cites, read from bytes (text only); refuses on any difference. Returns the record."""
    l12 = Path(R12).read_bytes().decode('utf-8').split('\n')
    l13 = Path(R13).read_bytes().decode('utf-8').split('\n')
    rec = []
    for what, n12, n13, must in (('sealed mode reads binding_inputs.case_block', 5706, 5708, "get('case_block')"),
                                 ('GATE_RECORD_SHA_REQUIRED', 338, 338, 'GATE_RECORD_SHA_REQUIRED = ()'),
                                 ('GATE_RECORD_AFTER_SEAL_ALLOWED', 341, 341, 'GATE_RECORD_AFTER_SEAL_ALLOWED = (')):
        a, b = l12[n12 - 1], l13[n13 - 1]
        if a != b or must not in b:
            raise SystemExit('r13 line check failed: %s r12 L%d / r13 L%d' % (what, n12, n13))
        rec.append({'what': what, 'r12_line': n12, 'r13_line': n13, 'text_equal': True, 'contains': must})
    if "'SR_K'" not in l13[340]:
        raise SystemExit('r13 L341 does not carry SR_K in the after-seal set')

    def func(lines, name):
        i = next(k for k, s in enumerate(lines) if s.startswith('def %s(' % name))
        j = next(k for k in range(i + 1, len(lines)) if lines[k] and not lines[k][0].isspace() and not lines[k].startswith('#'))
        return i + 1, '\n'.join(lines[i:j])
    a12, t12 = func(l12, 'builtin_r5_build')
    a13, t13 = func(l13, 'builtin_r5_build')
    if t12 != t13:
        raise SystemExit('builtin_r5_build differs between r12 and r13')
    rec.append({'what': 'def builtin_r5_build (whole function text equal)', 'r12_line': a12, 'r13_line': a13, 'text_equal': True})
    for k in ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005', 'PIN_DRIVER_BUILD_RECORD', 'PIN_V010_R5_CHECK', 'PIN_PRODUCER_REGISTRY'):
        hits = [n + 1 for n, s in enumerate(l13) if re.match(r'%s\s*=' % k, s)]
        if len(hits) != 1 or not re.match(r'%s\s*=\s*None(\s|#|$)' % k, l13[hits[0] - 1]):
            raise SystemExit('r13 seal-time pin %s is not a single unset (None) assignment' % k)
        rec.append({'what': 'seal-time pin %s = None in the reviewed source' % k, 'r13_line': hits[0]})
    sm = difflib.SequenceMatcher(None, l12, l13, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
    c0 = func(l12, 'check_record_codes')[0]          # 1-based line of the def
    c1 = next(k for k in range(c0, len(l12)) if l12[k] and not l12[k][0].isspace() and not l12[k].startswith('#'))   # 0-based end
    if not ops or any(not (c0 <= o[1] + 1 and o[2] <= c1) for o in ops):
        raise SystemExit('the r12 -> r13 line diff is not confined to check_record_codes (r12 L%d-L%d): %s' % (c0, c1, ops))
    rec.append({'what': 'r12 -> r13 line diff hunks (0-based opcodes), all inside r12 check_record_codes L%d-L%d' % (c0, c1),
                'hunks': [list(o) for o in ops]})
    return rec


def check_build_v007(P5, bp):
    """r5's BUILD_V007 checks, unchanged in substance, re-run on the bytes at r6 generation."""
    text = Path(bp['path']).read_bytes().decode('utf-8')
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
    plan = strict(Path(named['template_plan']['path']).read_bytes())
    lg = {k: plan.get(k) for k in ('launcher', 'guard')}
    for k, v in lg.items():
        if not (isinstance(v, dict) and amap.get(v.get('path')) == v.get('sha256')):
            raise SystemExit('BUILD_V007 template %s is not a supported BUILD_V007 source' % k)
    reg = strict(Path(P5['spec_registry']['path']).read_bytes())
    filled = {x['case']: x['filled'] for x in reg['specs']}
    calls = {c['case']: c['spec'] for c in plan['calls']}
    if calls != filled or len(plan['calls']) != 10:
        raise SystemExit('BUILD_V007 template does not launch exactly the ten FILLED specs of the case block')
    if plan['driver'] != P5['driver_r5'] or plan['registry'] != P5['spec_registry']:
        raise SystemExit('BUILD_V007 template driver or registry is not r5 / c7023846')
    old = strict(Path(P5['plan_template_v010']['path']).read_bytes())
    la, lb = {pname(k): v for k, v in leaves(old).items()}, {pname(k): v for k, v in leaves(plan).items()}
    diff = sorted(k for k in set(la) | set(lb) if la.get(k) != lb.get(k))
    nonstr = [k for k in diff if not all(x is not None and x.startswith('"') for x in (la.get(k), lb.get(k)))]
    if nonstr:
        raise SystemExit('BUILD_V007 template differs from V010 in non-string leaves: %s' % nonstr[:5])
    return named, lg, {'differing_leaves': len(diff), 'non_string_leaves': nonstr, 'order_identical': plan['order'] == old['order']}


def parse_checklist(text, rev):
    lines = text.split('\n')
    if lines[-1] != '' or not lines[0].startswith('# SEAL_CHECKLIST %s' % rev) or lines[4] != '| step | state | source |' or lines[5] != '|---|---|---|':
        raise SystemExit('SEAL_CHECKLIST: unexpected layout')
    m = re.fullmatch(r'State at assembly \((.+?)\)\. (.*)', lines[2])
    if not m:
        raise SystemExit('SEAL_CHECKLIST: state line')
    rows = []
    for ln in lines[6:-1]:
        s = re.fullmatch(r'\| \*\*(.+)\*\* \| \| \|', ln)
        if s:
            rows.append([s.group(1), '', ''])
            continue
        if not (ln.startswith('| ') and ln.endswith(' |')):
            raise SystemExit('checklist row: ' + ln[:60])
        cells = ln[2:-2].split(' | ')
        if len(cells) != 3 or not all(cells):
            raise SystemExit('checklist row is not exactly three cells: ' + ln[:60])
        rows.append(cells)
    return m.group(1), m.group(2), rows


def render_checklist(rev, ts, tail, rows):
    S = ['# SEAL_CHECKLIST %s: V007, in the order root will execute it' % rev, '', 'State at assembly (%s). %s' % (ts, tail), '',
         '| step | state | source |', '|---|---|---|']
    for a, b, c_ in rows:
        if ' | ' in a or ' | ' in b or ' | ' in c_:
            raise SystemExit('a checklist cell holds the cell separator')
        S.append('| **%s** | | |' % a if not b else '| %s | %s | %s |' % (a, b, c_))
    return '\n'.join(S) + '\n'


def render_root_items(rev, intro, ri):
    Rr = ['# Root items %s: KMAX_TAIL_PREREG_V007_FINAL_DRAFT_%s (unsealed)' % (rev, rev.upper()), '', intro, '']
    for r in ri:
        Rr += ['## %s: %s (%s)' % (r['id'], r['kind'], 'OPEN' if r['status'] == 'OPEN' else 'RESOLVED'), '', '- **Status:** %s' % r['status'],
               '- **Clause:** `%s`' % r['clause'], '- **Issue:** %s' % r['issue'], '- **Draft:** %s' % r['draft']]
        if 'recommendation' in r:
            Rr.append('- **Recommendation:** %s' % r['recommendation'])
        Rr += ['- **Sources:** %s' % '; '.join(r['sources']), '']
    return '\n'.join(Rr)


def render_entry_table(rev, head_line, rows):
    E = [head_line, '', '| entry | decision | section sha256 | revised clauses / reason |', '|---|---|---|---|']
    for r in rows:
        E.append('| %s | %s | `%s` | %s |' % (r['entry'], 'revised here' if r['decision'] == RH else 'no change', r['section_sha256'],
                                             ('%s. Clauses: %s' % (r['scope'].rstrip('.'), ', '.join('`%s`' % c for c in r['revised_clauses'])))
                                             if r['decision'] == RH else r['reason']))
    return '\n'.join(E) + '\n'


def entry_table_r5_header(v_sha, v_len, section_rule):
    return ('# ENTRY_TABLE_R5: V005 entries A82-A101 against prereg r5 (A99.3; the seal record quotes this table)\n\n'
            'Open V005 addendum read at r5 generation: sha256 `%s`, %d bytes (byte copy `addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md`). %s'
            % (v_sha, v_len, section_rule))


def clause_rows(doc, rows):
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
    return rowsm


def main():
    ts = os.environ['TS']
    if not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', ts):
        raise SystemExit('TS must be date -u +%Y-%m-%dT%H:%M:%SZ')
    out = Path(os.environ['OUT_DIR']).resolve()
    if not (out == R6D or str(out).startswith(str(R6D / 'scratch') + '/')):
        raise SystemExit('OUT_DIR must be the r6 folder, or a folder inside r6/scratch for a dry run')
    if not out.is_dir():
        raise SystemExit('OUT_DIR must exist: %s' % out)
    targets = [out / n for n in OUT_NAMES]
    present = [str(p) for p in targets if os.path.lexists(p)]
    if present:
        raise SystemExit('outputs already exist (exclusive create; nothing is overwritten): %s' % present)
    # ================================================================= r5 and its companions, from bytes
    raw5 = R5.read_bytes()
    if hashlib.sha256(raw5).hexdigest() != R5_SHA:
        raise SystemExit('r5 pin')
    doc = strict(raw5)
    doc5 = copy.deepcopy(doc)
    r5_companions = {n: pin(R5D / n, h) for n, h in R5_COMPANIONS}
    r5_generators = {n: pin(R5D / n, h) for n, h in R5_GENERATORS}
    P = {k: pin(p, h) for k, p, h in INPUTS}
    P5 = doc['assembly']['inputs_verified_from_bytes']
    for k in ('spec_registry', 'plan_template_v010', 'driver_r5'):
        pin(P5[k]['path'], P5[k]['sha256'])
    case_block_r5 = copy.deepcopy(doc['binding_inputs']['case_block'])
    if case_block_r5 != {'path': P['case_block']['path'], 'sha256': P['case_block']['sha256']}:
        raise SystemExit('r5 binding_inputs.case_block is not the case block of record')
    cbr = strict(Path(P['case_block_build_record']['path']).read_bytes())
    if cbr.get('verdict') != 'CASE_BLOCK_VALID_UNDER_R12' or cbr['case_block']['sha256'] != P['case_block']['sha256'] or cbr.get('fail'):
        raise SystemExit('the case block build record does not read the pinned case block valid')
    # ================================================================= the CLOSED V005 addendum: ONLY the exclusive byte copy
    vb = COPY.read_bytes()
    v005_sha = hashlib.sha256(vb).hexdigest()
    if v005_sha != V005_CLOSED_SHA or len(vb) != V005_CLOSED_BYTES:
        raise SystemExit('the r6 byte copy is not the closed V005 bytes (%s, %d bytes)' % (v005_sha, len(vb)))
    live = sha(V005)
    if live != V005_CLOSED_SHA:
        raise SystemExit('V005_CLOSED_FILE_CHANGED: the live V005 file hashes to %s, not the closed %s (A106.3); a defect for root' % (live, V005_CLOSED_SHA))
    secs = sections(vb)
    nums = sorted(int(k[1:]) for k in secs)
    newest = 'A%d' % max(nums)
    if nums != list(range(47, max(nums) + 1)) or newest != V005_LAST:
        raise SystemExit('the copy does not hold A47-%s exactly once each: %s' % (V005_LAST, nums))
    b5 = R5_COPY.read_bytes()
    s5 = sections(b5)
    if b5[:b5.index(b'\n## A')] != vb[:vb.index(b'\n## A')]:
        raise SystemExit('the V005 preamble differs from r5\'s copy')
    changed_since_r5 = sorted((e for e in s5 if s5[e] != secs.get(e)), key=lambda x: int(x[1:]))
    if changed_since_r5:
        raise SystemExit('entries changed since r5\'s copy (each needs its own disposition): %s' % changed_since_r5)
    ea = doc['entries_after_A81']
    rows = ea['rows']
    if [r['entry'] for r in rows] != ['A%d' % n for n in range(82, 102)]:
        raise SystemExit('r5 rows are not A82-A101')
    rehash = []
    for r in rows:
        head, b = secs[r['entry']]
        h = hashlib.sha256(b).hexdigest()
        if head != r['heading'] or h != r['section_sha256'] or len(b) != r['section_bytes']:
            raise SystemExit('r5 row %s does not re-hash from the copy (a revised row is needed)' % r['entry'])
        rehash.append({'entry': r['entry'], 'section_sha256': h, 'section_bytes': len(b), 'heading_equal': True})
    later = ['A%d' % n for n in nums if n > 101]
    if later != sorted(ROWS6, key=lambda x: int(x[1:])):
        raise SystemExit('entries after A101 %s do not match the rows of this generator %s' % (later, sorted(ROWS6)))
    lines_rec = line_checks()
    # ================================================================= BUILD_V007, re-verified from bytes
    lp = doc['seal_slots']['launch_packet']
    lpn = lp['named_candidates_verified_from_bytes']
    if lpn['build'] != P['build_v007']:
        raise SystemExit('r5 launch_packet build is not BUILD_V007 94bc05a5')
    named6, lg6, tv6 = check_build_v007(P5, P['build_v007'])
    if any(lpn[k] != v for k, v in named6.items()) or lpn['launcher'] != lg6['launcher'] or lpn['guard'] != lg6['guard']:
        raise SystemExit('BUILD_V007 names other files at r6 generation than r5 recorded')
    if named6['predecessor_BUILD_V006'] != P['build_v006']:
        raise SystemExit('BUILD_V007 does not pin BUILD_V006 fb9e6a4a as its predecessor')
    # ================================================================= registry V009 records (scalar fields only)
    vr = {}
    for k, cmp in (('validate_r12_c3v009', 'r12 4bd7b262'), ('validate_r13_c3v009', 'r13 f5adfd11')):
        v = strict(Path(P[k]['path']).read_bytes())
        if not (v.get('registry') == P['registry_c3v009'] and str(v.get('compare', '')).startswith(cmp) and v.get('all_registered_preseal_pass') is True
                and v.get('all_registered_shas_match_files') is True and v.get('guard_refused') == 0 and v.get('case_block_refusals') == []
                and len(v.get('preseal_records', {})) == 13 and v.get('empty_slots') == ['B0_N3', 'B0_RO1', 'I4']):
            raise SystemExit('%s does not read: V009 on %s, 13 records PASS, shas match, B0_N3/B0_RO1/I4 empty, guard refused 0' % (k, cmp))
        vr[k] = {'compare': v['compare'], 'preseal_records': len(v['preseal_records']), 'all_registered_preseal_pass': True, 'empty_slots': v['empty_slots']}
    # ================================================================= edits (each logged)
    changes = []

    def node(path):
        d = doc
        for k in path:
            d = d[k]
        return d

    def log(item, clause, kind, srcs, trace, why):
        if not trace or not any(re.match(r'(A\d+|F-\d+)', t) for t in trace):
            raise SystemExit('edit without a ruling or finding in its trace: ' + clause)
        changes.append({'item': item, 'clause': clause, 'kind': kind, 'added_sources': list(srcs), 'trace': list(trace), 'why': why})

    def addsrc(c, add):
        for s in add:
            if s in c['sources']:
                raise SystemExit('source %s already present' % s)
            c['sources'].append(s)

    def sub1(s, old, new, where):
        if s.count(old) != 1:
            raise SystemExit('expected exactly one %r in %s, found %d' % (old[:60], where, s.count(old)))
        return s.replace(old, new)

    def rep(path, old, new, add, item, clause, trace, why, field='text', kind='revised'):
        c = node(path)
        c[field] = sub1(c[field], old, new, '%s.%s' % (pname(path), field))
        if add:
            addsrc(c, add)
        log(item, clause, kind, add, trace, why)

    def app(path, more, add, item, clause, trace, why, field='text'):
        c = node(path)
        c[field] = c[field].rstrip() + ' ' + more
        if add:
            addsrc(c, add)
        log(item, clause, 'extended', add, trace, why)

    sl, sr, ri_by = doc['seal_slots'], doc['seal_record_requirements'], {r['id']: r for r in doc['root_items']}
    b7 = P['build_v007']['sha256']
    st3 = str(ST3) + '/'
    copy_abs = str(COPY)
    # ---------------------------------------------------------------- item 2: the compare slot (A102, A103, A104; F-02)
    cp = sl['compare']
    if 'or a ruling on the item' not in cp['rule'] or cp['value'] != 'PENDING_ROOT_AT_SEAL_ASSEMBLY':
        raise SystemExit('r5 compare rule anchor')
    cp['rule'] = ('The final compare round is r13 cx3v001 (f5adfd11; selected and frozen by SELECTED_R13_CX3V001 10acd098, 21:22:22Z; FIELDS_R13_CX3V001 '
                  '7b116b01, IMPL 274f7049, HASHES_R13_CX3V001 d4509325): r12 cx3v002 (4bd7b262) plus exactly the A102 fix of A-B1 in check_record_codes '
                  '(parse_int=str inside the duplicate-hook parse; the text fallback only on json.JSONDecodeError, any other ValueError a typed refusal), '
                  'so its scope is A91.1-A91.3 (0459, 0462\'s should-fix, A88 SR_K; A91.4\'s RI-24 cache fields are moot, A96) and A102. Its delta '
                  'reviews of record each report 0 blocking: Claude3\'s (0092, PASS_WITH_FINDINGS) and Codex1\'s (0076, PASS; Codex1 is the Codex-lineage '
                  'reviewer of record in place of Codex2, A103); A104 makes r13 the compare of record. r12 is superseded: Claude3\'s r12 review of record '
                  '(0083) reported 1 blocking item (A-B1), and A102 ordered the r13 fix round. V007 seals on the final compare round whose delta reviews of '
                  'record each report 0 blocking (A81 RI-20, as applied by A83, A86, A91, A96, A102, A103, A104; A83: the r11 workflow was stopped at its '
                  'freeze before its three recheck lenses ran, and the reviews of record replaced them; rehearsal R-02); a blocking item in a review of '
                  'record means a fix round (A102), never a seal on that round. This slot holds that round\'s reviewed source, with its seal-time pin '
                  'constants still unset (`None`; the bytes the reviews examined), path and sha. The sealed compare sets only the five A82 pins on top of '
                  'r13 (A104): V007_PREREG_SHA256 set to the sealed prereg sha, plus PIN_ADDENDUM_V005, PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK and '
                  'PIN_PRODUCER_REGISTRY. It is created after the sealed prereg and is named only in the SEAL_RECORD; it may differ from the reviewed source '
                  'only in those pin lines (A82: RI-27 ruled as drafted in r4).')
    if 'or a ruling' in cp['rule']:
        raise SystemExit('the F-02 route survived')
    addsrc(cp, ['A102', 'A103', 'A104', 'Claude3 0092', 'Codex1 0076'])
    log(2, 'seal_slots.compare.rule', 'rule rewritten', ['A102', 'A103', 'A104', 'Claude3 0092', 'Codex1 0076'],
        ['A102', 'A103', 'A104', 'A106.1', 'A81 RI-20', 'F-01', 'F-02'],
        'the final round is r13 with its reviews of record (Claude3 0092, Codex1 0076); r12 superseded; F-02 (A106.1): a blocking item means a '
        'fix round, never a seal on that round, and r5\'s "or a ruling on the item" is removed; the sealed compare sets only the five A82 pins on r13')
    nc5 = cp['named_candidates_verified_from_bytes']
    if nc5['r12_cx3v002_final_round'] != P['r12_compare']:
        raise SystemExit('r5 names another r12')
    cp['named_candidates_verified_from_bytes'] = {
        'r13_cx3v001_final_round': P['r13_compare'], 'r13_selection': P['r13_selected'], 'r13_fields': P['r13_fields'], 'r13_impl': P['r13_impl'],
        'r13_hashes': P['r13_hashes'],
        'delta_review_of_record_Claude3_0092': dict(P['Claude3_0092'], verdict=('PASS_WITH_FINDINGS, 0 blocking; 2 SHOULD_FIX, neither blocking the '
                                                                                'seal: the A102 V01-V07 MUST_FAIL tests are not in the selected r13 '
                                                                                'suite (a successor suite; no source change), and FIELDS_R13 L113 should '
                                                                                'state that text check records must decode'),
                                                    report=P['r13_review_Claude3'], hashes=P['r13_review_Claude3_hashes']),
        'delta_review_of_record_Codex1_0076': dict(P['Codex1_0076'], verdict='PASS, 0 blocking (cross-lineage; Codex1 in place of Codex2, A103)',
                                                   report=P['r13_review_Codex1']),
        'state_at_r6_generation': ('COMPARE_OF_RECORD (A104): Claude3 0092 and Codex1 0076, the delta reviews of record, each report 0 blocking; the '
                                   'slot value stays PENDING_ROOT_AT_SEAL_ASSEMBLY until root fills it at seal assembly'),
        'r12_superseded_A102': dict(nc5['r12_cx3v002_final_round'],
                                    note=('superseded (A102): Claude3 0083, a review of record, reported 1 BLOCKING item (A-B1: check_record_codes r12 '
                                          'L875-879); Codex2 0485 reported 0 blocking; A102 ordered the fix round r13'),
                                    selection=nc5['r12_selection'], fields=nc5['r12_fields'], impl=nc5['r12_impl'], hashes=nc5['r12_hashes'],
                                    delta_review_Codex2_0485=nc5['delta_review_of_record_Codex2_0485'],
                                    delta_review_Claude3_0083=nc5['delta_review_of_record_Claude3_0083']),
        'r11_superseded': nc5['r11_superseded'], 'r10_frozen_not_for_seal': nc5['r10_frozen_not_for_seal']}
    log(2, 'seal_slots.compare.named_candidates_verified_from_bytes', 'candidates replaced', [], ['A102', 'A103', 'A104', 'F-01'],
        'r13 (source, selection, FIELDS, IMPL, HASHES) and its two reviews of record, from bytes; r12 and its reviews kept as superseded (A102)')
    doc['outcome_branch_tests_required'] = sub1(doc['outcome_branch_tests_required'],
                                                '(the final round: r12 cx3v002 4bd7b262, or a fix round root orders under A81 RI-20; A96)',
                                                '(the final round: r13 cx3v001 f5adfd11, the fix round A102 ordered on r12 cx3v002 4bd7b262; A104)',
                                                'outcome_branch_tests_required')
    log(2, 'outcome_branch_tests_required', 'revised', [], ['A102', 'A104', 'F-01'], 'the final round named: r13')
    r = ri_by['RI-28']
    if r['status'] != 'OPEN':
        raise SystemExit('RI-28 expected OPEN in r5')
    r['status'] = ('RESOLVED: A102 (a fix round: compare r13 = r12 plus exactly the A-B1 fix, built by Codex3, 0629) and A104 (r13 is the compare of '
                   'record: the delta reviews of record, Claude3 0092 and Codex1 0076, Codex1 in place of Codex2 under A103, each report 0 blocking)')
    addsrc(r, ['A102', 'A103', 'A104', 'Claude3 0092', 'Codex1 0076'])
    log(2, 'root_items.RI-28', 'resolved', ['A102', 'A103', 'A104', 'Claude3 0092', 'Codex1 0076'], ['A102', 'A104', 'F-01'],
        'the r12 A-B1 item: fix round r13 (A102), the compare of record (A104)')
    # ---------------------------------------------------------------- item 1 (entry A103): the scope note names cx3r008
    rep(('not_v007_text_scope',), '(A74 cx3r005, A77 cx3r006, A80 and A93 cx3r007; the step-5 launch registry is SPEC_REGISTRY_CX3R007 cd30429c, A93; '
        'retired 3c42ca07, 47023c27 and c5abc2d5)',
        '(A74 cx3r005, A77 cx3r006, A80 and A93 cx3r007, A103 cx3r008; cx3r008 replaces cx3r007 as the step-5 NGC driver and its registry is pinned '
        'from bytes before step 5 (A103; A93 had made SPEC_REGISTRY_CX3R007 cd30429c the step-5 launch registry); retired 3c42ca07, 47023c27 and '
        'c5abc2d5)', ['A103'], 1, 'not_v007_text_scope', ['A103', 'F-01'], 'A103: the step-5 NGC driver is cx3r008 (r5\'s scope-note sentence was false after A103)')
    # ---------------------------------------------------------------- item 3: the launch packet (A105; Claude4 0108)
    rep(('seal_slots', 'launch_packet'), 'BUILD_V007\'s Claude4 delta check and Claude2\'s adoption are pending (A99.1).',
        'Claude4\'s BUILD_V007 delta (0108) is PASS_WITH_FINDINGS with 0 blocking and V6-S1 to V6-S3 closed, and BUILD_V007 (94bc05a5) stays bound '
        '(A105). A105 rules its three should-fix items: W7-S1, root\'s admission config lists exactly BUILD_V007\'s 15 rows and nothing else (A78 N2): '
        'the seal script builds it from BUILD_V007\'s table and refuses any other row count, and Codex1 checks this; RP-S1, the seal script creates '
        'the step-2 output root /Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007 before binding, as a new, empty directory created '
        'exclusively; RP-S2, the outputs stay on the internal SSD (A85.3), a watchdog alerts root if free space falls below 80 GB, the per-case caps '
        'remain as they are, and if the alert fires root rules either relocating the cases that have not yet started or pausing admission.',
        ['A105', 'Claude4 0108'], 3, 'seal_slots.launch_packet.rule', ['A105', 'F-01'],
        'BUILD_V007 delta 0108 (0 blocking) and A105\'s rulings W7-S1, RP-S1, RP-S2; BUILD_V007 stays bound (A105)', field='rule')
    if lp['pending_parts'] != ['bound_plan', 'bound_command', 'BUILD_V007 Claude4 delta check (A99.1)', 'BUILD_V007 adoption (Claude2)']:
        raise SystemExit('r5 pending_parts')
    lp['pending_parts'] = ['bound_plan', 'bound_command']
    log(3, 'seal_slots.launch_packet.pending_parts', 'revised', [], ['A105', 'F-01'],
        'the delta check is done (0108: 0 blocking) and BUILD_V007 stays bound (A105); the bound plan and command stay PENDING by design')
    lpn['build_v007_delta_review_Claude4_0108'] = dict(P['Claude4_0108'], verdict=('PASS_WITH_FINDINGS, 0 blocking; V6-S1, V6-S2 and V6-S3 closed; '
                                                                                   '3 SHOULD_FIX (W7-S1, RP-S1, RP-S2), ruled by A105'),
                                                       report=P['build_v007_review_Claude4'], hashes=P['build_v007_review_Claude4_hashes'])
    lpn['build_v007_reverified_at_r6_generation'] = {
        'state': 'REVERIFIED_FROM_BYTES', 'allowlist_sources': 15, 'allowlist_bytes_verified': True, 'named_files_equal_to_r5_generation': True,
        'launcher_and_guard_equal_to_r5_generation': True, 'template_launches_the_ten_FILLED_specs_of_the_case_block': True, 'template_vs_V010': tv6,
        'review_state': 'Claude4 delta 0108 PASS_WITH_FINDINGS, 0 blocking; BUILD_V007 stays bound (A105)'}
    log(3, 'seal_slots.launch_packet.named_candidates_verified_from_bytes', 'extended', [], ['A105', 'F-01'],
        'the 0108 review pinned; BUILD_V007 re-verified from bytes at r6 generation (the r5-generation record is kept as written)')
    r = ri_by['RI-29']
    if r['status'] != 'OPEN':
        raise SystemExit('RI-29 expected OPEN in r5')
    r['status'] = ('RESOLVED: A105 (Claude4 0108: PASS_WITH_FINDINGS, 0 blocking, V6-S1 to V6-S3 closed; BUILD_V007 94bc05a5 stays bound; its '
                   'should-fix items W7-S1, RP-S1 and RP-S2 are ruled)')
    r['recommendation'] = sub1(r['recommendation'], 're-pin seal tool 3 v002 to the regenerated text.',
                               're-pin seal tool 3 (seal tools v003, %s; root uses the v003 tuple Claude4 posts) to the regenerated text.' % st3,
                               'RI-29.recommendation')
    addsrc(r, ['A105', 'Claude4 0108', 'A106.2'])
    log(3, 'root_items.RI-29', 'resolved; the seal tool named as v003', ['A105', 'Claude4 0108', 'A106.2'], ['A105', 'A106.2', 'F-01'],
        'BUILD of record: delta 0108 PASS_WITH_FINDINGS, 0 blocking; it stays bound (A105); item 9: the recommendation names seal tools v003')
    # ---------------------------------------------------------------- item 4: seal record requirements (A105 E-OPS5; F-11(c); A106.2)
    app(('seal_record_requirements', 0), 'A105 (E-OPS5): the E-SEAL1 block also discloses that root, sizing outputs at about 22:31Z, ran du -sh on the '
        'C5H run directory: metadata only, its aggregate size (25 GB); no file content was read and no result value or row was obtained. This goes '
        'beyond the "validity-only booleans before the seal" rule in letter, and root makes no further metadata access to C5H before the seal.',
        ['A105'], 4, 'seal_record_requirements[0]', ['A105', 'F-01'], 'E-OPS5 disclosed in the seal record\'s E-SEAL1 block (A105)')
    rep(('seal_record_requirements', 4), '(2) with the driver chosen (r5, A96; no cache directory, A81 RI-24 being moot), the bound plan and command '
        'written by the build-only binder (0576; A81 RI-25);',
        '(2) with the driver chosen (r5, A96; no cache directory, A81 RI-24 being moot), the r5 driver BUILD record (PIN_DRIVER_BUILD_RECORD; schema '
        'UNT_V007_SEALED_DRIVER_BUILD_C2V001; seal_record_requirements[8]; rehearsal D-06; checklist B2a), then the bound plan and command written by '
        'the build-only binder (0576; A81 RI-25);', [], 4, 'seal_record_requirements[4]', ['A82', 'F-11'],
        'F-11(c): the order of record names the driver BUILD record step that [8] and checklist B2a place before the sealed compare')
    if len(sr) != 13:
        raise SystemExit('r5 has %d seal_record_requirements, not 13' % len(sr))
    sr.append({'text': ('A106.2: the seal record states which of the exactness checks C-02 to C-08 (Claude4 0109) the seal script checked and which root '
                        'checked by hand at assembly. A106.2 places C-02 (the text-of-record pin equals r6\'s stored sha), C-04 (the slot records load '
                        'through r13\'s own load_producer_registry against registry V009, and every slot passes), C-05 (the launcher and guard match '
                        'BUILD_V007 by exact name and sha) and C-06 (the whole bound command is byte-compared with the binder\'s output) in Claude3\'s '
                        'seal script, as exactness checks at assembly; '
                        'C-03 (B6 provenance) and C-08 (NEW-item ids against the IMPL) are in the script if each takes 10 minutes or less, otherwise root '
                        'checks them by hand at assembly and the seal record says so; C-07 (the generic covered-later sentence) is D-05, which seal tools '
                        'v003 carry (A106.2: v003 carries D-05 with C-01, B8, the README fix and the W7-S1 MUST_FAIL cases, and nothing more).'),
               'sources': ['A106.2', 'Claude4 0109', '0643']})
    log(4, 'seal_record_requirements[13]', 'new', ['A106.2', 'Claude4 0109', '0643'], ['A106.2'],
        'A106.2: the seal record states which of C-02 to C-08 the seal script checked and which root checked by hand')
    # ---------------------------------------------------------------- item 5: F-11 small fixes (line citations into r13; RI-20/21; B2)
    rep(('binding_inputs', 'case_block_rule'), '(r12 cx3v002 L5706)', '(r13 cx3v001 L5708)', ['A104'], 5, 'binding_inputs.case_block_rule',
        ['A104', 'F-11'], 'F-11(d): the line citation moves to r13, verified from bytes (r12 L5706 = r13 L5708)')
    rep(('fixed_across_all_cases', 'validity_gates'), '(r12 L5706)', '(r13 L5708)', ['A104'], 5, 'fixed_across_all_cases.validity_gates',
        ['A104', 'F-11'], 'F-11(d): r12 L5706 = r13 L5708, verified from bytes')
    c = node(('gates_before_any_T_result', 'after_seal_marker_policy'))
    for o, n_ in (('(A88; r12 GATE_RECORD_AFTER_SEAL_ALLOWED L341 and GATE_RECORD_SHA_REQUIRED = () L338, A99.5)',
                   '(A88; r13 GATE_RECORD_AFTER_SEAL_ALLOWED L341 and GATE_RECORD_SHA_REQUIRED = () L338, A99.5)'),
                  ('and for every other gate (r12).', 'and for every other gate (r13).')):
        c['text'] = sub1(c['text'], o, n_, 'after_seal_marker_policy')
    addsrc(c, ['A104'])
    log(5, 'gates_before_any_T_result.after_seal_marker_policy', 'revised', ['A104'], ['A104', 'F-11'],
        'F-11(d): the citations move to r13 (L338 and L341 unchanged, verified from bytes)')
    rep(('gates_before_any_T_result', 'B2'), '(<= 0.05 km/s) A94:', '(<= 0.05 km/s). A94:', [], 5, 'gates_before_any_T_result.B2', ['F-11', 'A94'],
        'F-11(b): the clause separator before "A94:"')
    r = ri_by['RI-20']
    r['status'] = r['status'] + ('; as applied by A83, A86, A91, A96, A102, A103 and A104 (A83: the r11 workflow was stopped at its freeze before its '
                                 'three recheck lenses ran, and the reviews of record replaced them; A102: a blocking item in a review of record means a '
                                 'fix round, r13; A103: Codex1 in place of Codex2 as the Codex-lineage reviewer of record; A104: both reviews of record '
                                 'report 0 blocking on r13)')
    addsrc(r, ['A83', 'A86', 'A91', 'A96', 'A102', 'A103', 'A104'])
    log(5, 'root_items.RI-20', 'status pointers added', ['A83', 'A86', 'A91', 'A96', 'A102', 'A103', 'A104'], ['A83', 'A102', 'A103', 'A104', 'F-11'],
        'F-11(a): the RI-20 status names how A81 RI-20 was applied (the r4 "three recheck lenses" criterion was replaced, A83)')
    r = ri_by['RI-21']
    r['status'] = r['status'] + ('; as applied by A83 (Codex2\'s cross-lineage review is the c2v007 check of record; the c2v007 own-check workflow was '
                                 'stopped and its outputs are leads only) and A92 (c2v007r2 is the identity-comparator slot after Codex2\'s delta check '
                                 '0472, 0 blocking; the R5_V001 records are the identity records of record)')
    addsrc(r, ['A83', 'A92'])
    log(5, 'root_items.RI-21', 'status pointers added', ['A83', 'A92'], ['A83', 'F-11'],
        'F-11(a): the RI-21 status names A83 (the r4 "own check" criterion was replaced) and A92')
    # ---------------------------------------------------------------- item 6: F-13 (ngc_gas_M_s 96, root's confirmation at checklist A7)
    rep(('fixed_across_all_cases', 'production_tail', 'ngc_gas_M_s'), 'Root states the value at seal assembly (rehearsal R-08).',
        'Root states the value at seal assembly (rehearsal R-08) and confirms it, with its record GQ_NGC_91_MS96_V001 (be148bab; Codex1 0032), at '
        'checklist A7; no A-entry names that record, so the SEAL_RECORD records root\'s A7 confirmation (r5 check F-13).', ['r5 check F-13'], 6,
        'fixed_across_all_cases.production_tail.ngc_gas_M_s', ['F-13', 'A81 RI-23'], 'F-13: root\'s checklist-A7 confirmation of the lane record is '
        'recorded in the SEAL_RECORD')
    # ---------------------------------------------------------------- item 7: the producer registry candidate (A101, A106.1; Claude3 0087)
    pr = sl['producer_registry']
    prn = pr['named_candidates_verified_from_bytes']
    if prn['C3V009_candidate']['sha256'] != P['registry_c3v009']['sha256'] or prn['C3V008_final_A101'] != P['registry_c3v008']:
        raise SystemExit('r5 registry candidates')
    pr['named_candidates_verified_from_bytes'] = {
        'C3V009_candidate': dict(P['registry_c3v009'], note=(
            'The candidate (A101: V009 adds BUILD_V007\'s post-seal producers to V008; Claude3 0087: V009 supersedes V008 as the registry to pin; '
            'A106.1: the registry V009 32ddadcb binding is unchanged): C3V008 plus BUILD_V007\'s four post-seal producer pins (SRB_ROT 2757847a; MT, '
            'I1T and FLAG_RULINGS 4024d82a) and nothing else; with the case block of record 76309ae3 all 13 registered records PASS and B0_N3, '
            'B0_RO1, I4 fail closed, on r12 (VALIDATE_R12_C3V009_CASEBLOCK_OF_RECORD 537d1a42) and on r13 (VALIDATE_R13_C3V009_CASEBLOCK_OF_RECORD '
            'f14dd9a6; Claude3 0092); listed in dispatch 0626; a record filling B0_N3, B0_RO1 or I4 means a V010'),
            validation_on_r12=P['validate_r12_c3v009'], validation_on_r13=P['validate_r13_c3v009']),
        'C3V008_superseded': dict(prn['C3V008_final_A101'], note=('final under A101 (13 registered records PASS on r12; Claude3 0084), with '
                                                                  'BUILD_V007\'s post-seal producers to come as V009; superseded by C3V009 (A101; '
                                                                  'Claude3 0087)')),
        'note': ('The slot value is the registry root pins at seal assembly; the candidate is C3V009 (A101; Claude3 0087; A106.1), and C3V008 and '
                 'C3V007 are superseded. B0_N3, B0_RO1 and I4 are empty and fail closed (RI-33); the SR_K producer-pin reading is RI-37.'),
        'C3V007_superseded': prn['C3V007_superseded']}
    addsrc(pr, ['A106.1', 'Claude3 0092'])
    log(7, 'seal_slots.producer_registry.named_candidates_verified_from_bytes', 'candidate named; V008 superseded', ['A106.1', 'Claude3 0092'],
        ['A101', 'A106.1', 'Claude3 0087'], 'C3V009 is the candidate (A101; Claude3 0087; A106.1), C3V008 superseded; V009 also passes on r13 '
        '(f14dd9a6); the slot rule is kept')
    # ---------------------------------------------------------------- item 1: the entry table, its rule, the closed V005 (A106.3)
    new_rows = []
    for e in later:
        dec, clauses, note = ROWS6[e]
        head, b = secs[e]
        new_rows.append({'entry': e, 'heading': head, 'section_sha256': hashlib.sha256(b).hexdigest(), 'section_bytes': len(b), 'decision': dec,
                         'revised_clauses': clauses, ('scope' if dec == RH else 'reason'): note, 'sources': [e]})
    rows.extend(new_rows)
    log(1, 'entries_after_A81.rows', 'rows added', [], ['A99.3', 'A81 RI-26', 'A106.1', 'F-01'],
        'rows for %s (each revised here, naming its clauses), section sha256 from the closed bytes; the 20 r5 rows re-hash unchanged' % ', '.join(later))
    ea['rule'] = sub1(ea['rule'], 'This table covers A82-A101, the newest at r5 generation; the seal record quotes it; any later entry needs a successor '
                      'revision or an explicit seal-record note (A81 RI-26).',
                      'This table covers A82-A106. V005 is closed at A106, its last entry (A106.3), and the frozen copy taken at assembly must equal '
                      'the closed bytes that addendum_read pins, so the table covers every V005 entry after A81; the seal record quotes it. Root\'s '
                      'later rulings (the seal entry, flag rulings, steps 4-7) are in the V006 addendum (A82; A106.3) and are not V005 entries.',
                      'entries_after_A81.rule')
    addsrc(ea, ['A106.3'])
    log(1, 'entries_after_A81.rule', 'revised', ['A106.3'], ['A99.3', 'A106.3', 'F-01'],
        'the table covers A82-A106; V005 closed at A106 (A106.3); later root rulings are V006 entries, not V005 entries')
    if set(ea['addendum_read']) != {'open_path', 'sha256_at_generation', 'bytes', 'byte_copy'}:
        raise SystemExit('r5 addendum_read keys')
    ea['addendum_read'] = {'open_path': str(V005), 'sha256_at_generation': v005_sha, 'bytes': len(vb),
                           'byte_copy': ('%s (same bytes: an exclusive byte copy of the closed V005 file, A106.3, made at r6 generation by '
                                         'tools/copy_addendum_c4r6_v2.py; the generator read the entries only from it)' % copy_abs)}
    log(1, 'entries_after_A81.addendum_read', 'revised', [], ['A99.3', 'A106.3', 'A106.2', 'F-01'],
        'the closed bytes: sha256, size and the r6 byte copy (the bytes seal tools v003 tool 1 takes as --addendum-at-text-of-record, C-01)')
    sr[11]['text'] = sub1(sr[11]['text'], R5_SRR11,
                          'Any A-entry after A81 that touches this text needs a successor revision or an explicit no-change note in the seal record; '
                          'the seal check verifies that every A-entry this text cites is present in the frozen bytes. The entry table entries_after_A81 '
                          'lists every entry from A82 to A106, the last V005 entry (A106.3), as revised here (with its clauses) or no change (with the '
                          'reason), each with its section sha256 read from bytes, and the seal record quotes it (A99.3). V005 is closed at A106 '
                          '(A106.3): the frozen copy taken at assembly must equal the closed bytes that entries_after_A81.addendum_read pins '
                          '(%s, %d bytes), so at the freeze every row re-hashes from the frozen bytes, no cited entry\'s bytes change and no V005 entry '
                          'follows the table; root\'s later rulings go in the V006 addendum (A82) and are not V005 entries. Seal tools v003 tool 1 (%s; '
                          'root uses the v003 tuple Claude4 posts) takes r6\'s addendum_read byte copy (%s) as --addendum-at-text-of-record and compares '
                          'every cited entry with the frozen copy (C-01; A106.2); with equal bytes the later and changed sets are empty and no '
                          'dispositions file is needed (Claude4 0110). A frozen copy that differs from these bytes is a defect for root (A106.3); a '
                          'changed or later entry would then need root\'s byte-pinned dispositions JSON (D-05: revised, pointing to the prereg revision, '
                          'or no_change_after_change with a changed_text excerpt present in the new bytes and absent from the old, and a reason; plain '
                          'no_change only for unchanged bytes; A104; 0640), and bare --covered-later names are refused (0633).'
                          % (v005_sha, len(vb), st3, copy_abs), 'seal_record_requirements[11]')
    addsrc(sr[11], ['A104', 'A106.2', 'A106.3', '0633', '0640', 'Claude4 0110'])
    log(1, 'seal_record_requirements[11]', 'rewritten', ['A104', 'A106.2', 'A106.3', '0633', '0640', 'Claude4 0110'],
        ['A99.3', 'A104', 'A106.2', 'A106.3', 'F-01'],
        'the table covers A82-A106; the frozen copy equals the closed bytes (A106.3); seal tools v003 tool 1 and its input (item 9); the D-05 rule (A104)')
    r = ri_by['RI-34']
    if r['status'] != 'OPEN':
        raise SystemExit('RI-34 expected OPEN in r5')
    r['status'] = ('RESOLVED: A106.3 (V005 closes with A106, its last entry; r6\'s entry table ends at A106; the frozen copy taken at assembly must equal '
                   'the closed bytes %s; later root rulings go in the V006 addendum and are not V005 entries); seal tools v003 tool 1 compares every '
                   'cited entry against r6\'s addendum_read byte copy (--addendum-at-text-of-record; A106.2, C-01) and refuses the bare --covered-later '
                   'names of v002 (0633); root uses the v003 tuple Claude4 posts' % v005_sha)
    r['recommendation'] = sub1(r['recommendation'], 'seal tools 1/4 receive exactly those entries as --covered-later.',
                               'seal tools 1/4 receive exactly those entries as --covered-later (superseded: seal tools v003 refuse bare --covered-later '
                               'names, 0633, and after A106.3 no V005 entry follows the table).', 'RI-34.recommendation')
    addsrc(r, ['A106.2', 'A106.3', '0633'])
    log(1, 'root_items.RI-34', 'resolved', ['A106.2', 'A106.3', '0633'], ['A106.3', 'A106.2', 'F-01'],
        'A106.3: V005 closed at A106 and the table ends there; item 9: v003 refuses bare --covered-later names')
    fa = sl['frozen_addendum']
    app(('seal_slots', 'frozen_addendum'), 'V005 is closed at A106 (A106.3): the frozen copy must equal the closed bytes, sha256 %s, %d bytes (the bytes '
        'entries_after_A81.addendum_read pins); a frozen copy that differs is a defect for root.' % (v005_sha, len(vb)), ['A106.3'], 1,
        'seal_slots.frozen_addendum.rule', ['A106.3'], 'A106.3: the frozen copy must equal the closed V005 bytes', field='rule')
    if fa['value'] != 'PENDING_ROOT_AT_SEAL_ASSEMBLY':
        raise SystemExit('frozen_addendum value')
    fc = doc['decision_pins_pending_at_seal']['V005_addendum_frozen_copy']
    if fc['entries'] != R5_FROZEN_ENTRIES or fc['sha256'] != 'PENDING_ROOT_AT_SEAL_ASSEMBLY':
        raise SystemExit('decision_pins_pending_at_seal anchor')
    fc['entries'] = ('A47-A106 (A82-A106 in entries_after_A81); V005 is closed at A106 (A106.3): the frozen copy must equal the closed bytes %s (%d '
                     'bytes); cited by name until frozen' % (v005_sha, len(vb)))
    log(1, 'decision_pins_pending_at_seal.V005_addendum_frozen_copy.entries', 'revised', [], ['A106.3', 'F-01'],
        'the cited range A47-A106; the frozen copy must equal the closed bytes (A106.3)')
    if doc['cites_by_name'][0] != R5_CITES0:
        raise SystemExit('cites_by_name anchor')
    doc['cites_by_name'][0] = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM: A47-A106 (closed at A106, A106.3; pinned by its frozen copy, PENDING)'
    log(1, 'cites_by_name[0]', 'revised', [], ['A106.3', 'F-01'], 'the cited range A47-A106; V005 closed (A106.3)')
    # ---------------------------------------------------------------- root items order (r5's rule: open first, then by id)
    order5 = [x['id'] for x in doc['root_items']]
    doc['root_items'].sort(key=lambda x: (x['status'] != 'OPEN', int(x['id'].split('-')[1])))
    order6 = [x['id'] for x in doc['root_items']]
    if order6 != order5:
        log(1, 'root_items (order)', 'reordered by r5\'s rule (open first, then by id)', [], ['A102', 'A104', 'A105', 'A106.3'],
            'RI-28, RI-29 and RI-34 are resolved, so they move into the resolved group')
    # ---------------------------------------------------------------- header (item 1; A106.1)
    doc['revision'] = 'r6'
    log(1, 'revision', 'header', [], ['A106.1', 'F-01'], 'r5 -> r6 (A106.1 approves prereg r6)')
    doc['supersedes_draft'] = {'path': str(R5), 'sha256': R5_SHA}
    log(1, 'supersedes_draft', 'header', [], ['A106.1', 'F-01'], 'the r5 pin replaces the r4 pin')
    doc['status'] = ('FINAL DRAFT r6 (NOT SEALED). Assembled by Claude4 (A106.1 approves prereg r6; dispatch 0643) from r5 3245899f, integrating V005 '
                     'A102-A106 through the entry table entries_after_A81 (A82-A106; each row revised here, or no change with the reason). V005 is closed '
                     'at A106 (A106.3); its closed bytes %s were read at assembly (byte copy %s). Written before any V007 (tail-corrected) result exists; '
                     'nothing was launched; C5H, UVT_* and targets were not read. binding_inputs.case_block pins CASE_BLOCK_V007_C4V001 (A99.2, A101). The '
                     'final compare round is r13 cx3v001 (f5adfd11; A102, A104). The launch-packet BUILD of record is BUILD_V007 (%s; Claude4 delta 0108 '
                     'PASS_WITH_FINDINGS, 0 blocking; it stays bound, A105). Root fills the named seal slots and seals. Open root items: ROOT_ITEMS_R6.'
                     % (v005_sha, COPY_REL, b7))
    log(1, 'status', 'header', [], ['A104', 'A105', 'A106.1', 'F-01'], 'r6 status line: A102-A106 integrated; V005 closed; r13; BUILD_V007 stays bound')
    reads6 = [{'read': 'r6 read 1 (first builder, stopped), 22:35:01Z (A47-A105; superseded by A106)',
               'sha256': sha(R6D / 'scratch/V005_ADDENDUM_READ_COPY_1_C4R6.md'), 'copy': str(R6D / 'scratch/V005_ADDENDUM_READ_COPY_1_C4R6.md')},
              {'read': 'r6 generation (continuation run 2): the closed bytes (A47-A106), byte copy made at 23:06Z', 'sha256': v005_sha, 'copy': copy_abs}]
    doc['assembly'] = {
        'by': 'Claude4 r6 helper (prereg r6), single author; continuation run 2 of the r6 build',
        'utc': ts,
        'dispatch': ('0643 (Claude2): prereg r6 is approved (A106.1); build its entry table through A106 from the closed V005 bytes. The build was '
                     'announced in Claude4 0109 and acknowledged in Claude4 0110; r5 was assembled under dispatch 0621 (A99). All are pinned in '
                     'revision_basis'),
        'continuation': ('the first r6 builder read V005 at 22:35Z, before A106 existed, and was stopped by Claude4 at 23:03Z before it wrote any '
                         'output (Claude4 0110); this run rewrote its draft generator (pinned in inputs_verified_from_bytes) for A106'),
        'revision_basis': {'dispatch_0643': P['dispatch_0643'], 'Claude4_0110': P['Claude4_0110'], 'Claude4_0109': P['Claude4_0109'],
                           'r5_check_report_C4V002': P['r5_check_report_C4V002'], 'r5_check_results_C4V002': P['r5_check_results_C4V002'],
                           'dispatch_0621_r5': P['dispatch_0621_r5']},
        'base': {'path': str(R5), 'sha256': R5_SHA}, 'base_companions': r5_companions, 'base_generators': r5_generators,
        'rulings_read': dict(doc5['assembly']['rulings_read'],
                             V005_addendum_open_observed={'path': str(V005), 'sha256': v005_sha, 'state': 'CLOSED at A106 (A106.3; 0643)'},
                             V005_addendum_reads=doc5['assembly']['rulings_read']['V005_addendum_reads'] + reads6),
        'v005_closed_bytes_check': {'copy_sha256': v005_sha, 'copy_bytes': len(vb), 'live_file_sha256_at_generation': live,
                                    'entries': 'A47-%s, %d entries, each once' % (newest, len(secs)),
                                    'entries_A47_A101_and_preamble_equal_to_the_r5_copy': True, 'entries_added_since_the_r5_copy': later},
        'r13_line_checks': lines_rec,
        'r5_rows_rehashed_from_the_r6_copy': rehash,
        'registry_v009_validations_read': vr,
        'inputs_verified_from_bytes': {k: v for k, v in P.items()},
        'inputs_verified_from_bytes_at_r5': doc5['assembly']['inputs_verified_from_bytes']}
    log(1, 'assembly', 'header', [], ['A106.1', 'F-01'], 'r6 assembly: dispatch 0643, basis, base r5, the closed-bytes check, line checks, inputs from bytes; '
        'r5\'s inputs kept')
    # ================================================================= the checklist (r5's rows; logged edits only)
    ck_text = (R5D / 'SEAL_CHECKLIST_R5.md').read_text()
    ts5, tail5, ck = parse_checklist(ck_text, 'r5')
    if render_checklist('r5', ts5, tail5, ck) != ck_text:
        raise SystemExit('the r5 checklist does not round-trip')
    cedits = {}

    def crow(prefix):
        hits = [x for x in ck if x[0].startswith(prefix)]
        if len(hits) != 1:
            raise SystemExit('checklist step %r: %d rows' % (prefix, len(hits)))
        return hits[0]

    def cset(step, prefix, new, item, kind, trace, why):
        row = crow(prefix)
        if step in cedits:
            raise SystemExit('checklist step %s edited twice' % step)
        for i in range(3):
            if new[i] is not None:
                row[i] = new[i]
        cedits[step] = list(trace)
        log(item, 'SEAL_CHECKLIST_R6 ' + step, kind, [], trace, why)

    row = crow('A1. ')
    if not row[0].startswith('A1. Final compare round r12 cx3v002'):
        raise SystemExit('A1 anchor')
    cset('A1', 'A1. ', ('A1. Final compare round r13 cx3v001 (f5adfd11; SELECTED_R13_CX3V001 10acd098), the A102 fix round of r12 cx3v002 (4bd7b262, '
                        'superseded): its delta reviews of record, Claude3\'s (0092) and Codex1\'s (0076; Codex1 in place of Codex2, A103), each report 0 '
                        'blocking (A81 RI-20 as applied by A83, A86, A91, A96, A102, A103, A104); its IMPL lists every NEW item with disposition and '
                        'MUST_FAIL tests. Fix its reviewed source (seal-time pins unset) for the compare slot.',
                        'DONE (A104: r13 is the compare of record): Claude3 0092 PASS_WITH_FINDINGS, 0 blocking (SF1: the A102 V01-V07 MUST_FAIL tests are '
                        'not in the selected r13 suite; SF2: FIELDS_R13 L113); Codex1 0076 PASS, 0 blocking',
                        'A104; A102; A103; A96; A83; A91; R-02'), 2, 'step rewritten', ['A102', 'A103', 'A104', 'F-11'],
         'F-11(e): A1 names r13 and its reviews of record')
    row = crow('A7. ')
    cset('A7', 'A7. ', (row[0] + ' Root\'s confirmation of ngc_gas_M_s 96 with its record GQ_NGC_91_MS96_V001 (be148bab; Codex1 0032) is recorded in the '
                        'SEAL_RECORD (F-13: no A-entry names that record).', None, sub1(row[2], 'A70; A86; A87; A81 RI-23; R-08',
                                                                                       'A70; A86; A87; A81 RI-23; R-08; F-13', 'A7 source')),
         6, 'revised', ['F-13', 'A81 RI-23'], 'F-13: root\'s A7 confirmation of ngc_gas_M_s 96 is recorded in the SEAL_RECORD')
    row = crow('A8. ')
    cset('A8', 'A8. ', (sub1(row[0], 'Seal tool 3 v001 refuses it (D-01): seal tools v002 must read ddo_gas_M_s.',
                             'Seal tool 3 v001 refused it (D-01); seal tools v002 r2 reads ddo_gas_M_s (GAP-11 closed; r5 check T3b), and seal tools v003 '
                             '(%s) change only D-05 (with C-01), B8, the README and the W7-S1 MUST_FAIL cases (A106.2); root uses the v003 tuple Claude4 '
                             'posts.' % st3, 'A8'),
                        sub1(row[1], 'registered; tool fix in seal tools v002', 'registered; tool fix in seal tools v002 r2, carried into v003 (A106.2)', 'A8 state'),
                        sub1(row[2], 'A87; A81 RI-22; D-01', 'A87; A81 RI-22; D-01; A106.2; 0633; 0634', 'A8 source')),
         9, 'revised', ['A106.2', 'A87'], 'item 9: the seal tools named are v003 (A106.2 scope)')
    row = crow('A12. ')
    cset('A12', 'A12. ', (sub1(row[0], '15 supported sources; Claude4 delta check; Claude2 adoption.',
                               '15 supported sources; Claude4 delta check 0108: PASS_WITH_FINDINGS, 0 blocking; A105: BUILD_V007 stays bound, and its '
                               'should-fix items W7-S1, RP-S1 and RP-S2 are ruled (steps B3, B8, C1).', 'A12'),
                          'DONE (A105)', sub1(row[2], 'A99.1; D-02', 'A99.1; D-02; A105', 'A12 source')), 3, 'revised', ['A105'], 'BUILD_V007 delta done; A105')
    row = crow('B1. ')
    blist = ', '.join('%s %s' % (x['entry'], 'revised' if x['decision'] == RH else 'no change') for x in rows)
    if not row[0].endswith('only entries after A101 with seal-record notes are (none at r5 generation).'):
        raise SystemExit('B1 anchor')
    b1 = ('B1. Freeze the V005 addendum: exclusive-create ..._V005_ADDENDUM_FROZEN.md. V005 is closed at A106, its last entry (A106.3; 0643): the '
          'frozen copy must equal the closed bytes, sha256 %s, %d bytes (entries_after_A81.addendum_read; the r6 byte copy %s), and root writes '
          'nothing more to the open V005 file; root\'s later rulings go to the V006 addendum and are not V005 entries (A82, A99.6, A106.3). Verify '
          'every A-entry this text cites (A47-A106) is present and each of the %d entries_after_A81 rows (A82-A106) re-hashes to its section_sha256 '
          'in the frozen bytes. Entries after A81 (D-05; A99.3): %s. Seal tools v003 tool 1 (%s; root uses the v003 tuple Claude4 posts) takes the '
          'r6 byte copy as --addendum-at-text-of-record and compares every cited entry with the frozen copy (C-01; A106.2): with equal bytes the later '
          'and changed sets are empty and no dispositions file is needed. A frozen copy that differs from these bytes is a defect for root (A106.3); a '
          'changed or later entry would need root\'s byte-pinned dispositions JSON under D-05 (A104; 0640), and bare --covered-later names are '
          'refused (0633).' % (v005_sha, len(vb), copy_abs, len(rows), blist, st3))
    cset('B1', 'B1. ', (b1, None, sub1(row[2], 'A81 RI-26; A82; A99.3; A99.6; D-05', 'A81 RI-26; A82; A99.3; A99.6; D-05; A104; A106.3; 0633; 0640; 0643',
                                       'B1 source')), 5, 'step rewritten', ['A104', 'A106.2', 'A106.3', 'F-11'],
         'F-11(e): B1 lists A82-A106 and requires the frozen copy to equal the closed bytes (A106.3); item 9: v003 tool 1 and its input')
    row = crow('B2a. ')
    cset('B2a', 'B2a. ', (sub1(row[0], 'equal to compare r12\'s builtin_r5_build()', 'equal to compare r13\'s builtin_r5_build() (unchanged from r12)', 'B2a'),
                          None, sub1(row[2], 'A72; A82; D-06; GAP-04', 'A72; A82; D-06; GAP-04; A104', 'B2a source')), 5, 'revised', ['A104', 'F-11'],
         'F-11(d): B2a cites r13 (the function text is equal in r12 and r13, verified from bytes)')
    row = crow('B3. ')
    cset('B3', 'B3. ', ('B3. Before the binder runs, the seal script exclusively creates the step-2 output root '
                        '/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007 as a new, empty directory, refusing if it exists (A105 RP-S1; '
                        '0642). ' + sub1(row[0][len('B3. '):], 'Run the build-only binder', 'Then run the build-only binder', 'B3'),
                        None, sub1(row[2], '0576; A81 RI-25; A99.1', '0576; A81 RI-25; A99.1; A105; 0642', 'B3 source')), 3, 'revised', ['A105'], 'A105 RP-S1')
    row = crow('B7. ')
    t0 = sub1(row[0], 'B6 output; E5-08;', 'B6 output (E-SEAL1, with A105\'s E-OPS5 disclosure: seal_record_requirements[0]); E5-08;', 'B7')
    t0 = sub1(t0, 'the B2 disclosure and the A101 erratum (seal_record_requirements[12]); no-row-shown statement.',
              'the B2 disclosure and the A101 erratum (seal_record_requirements[12]); root\'s A7 confirmation of ngc_gas_M_s 96 (F-13); which of the '
              'checks C-02 to C-08 the seal script checked and which root checked by hand (A106.2; seal_record_requirements[13]); no-row-shown statement.', 'B7')
    cset('B7', 'B7. ', (t0, None, sub1(row[2], 'A81 RI-19/25; A99.3; A100; A101', 'A81 RI-19/25; A99.3; A100; A101; A105; A106.2; F-13', 'B7 source')), 4,
         'revised', ['A105', 'A106.2', 'F-13'], 'the SEAL_RECORD carries E-OPS5 in E-SEAL1 (A105), root\'s A7 confirmation (F-13) and the C-02..C-08 '
         'statement (A106.2)')
    row = crow('B8. ')
    cset('B8', 'B8. ', (row[0] + ' The seal script builds that allowlist from BUILD_V007\'s 15-row table exactly and refuses any other row count or any row '
                        'not byte-equal to that table (A105 W7-S1; 0642); Codex1 checks this.', None,
                        sub1(row[2], '0561; A78 N2; A99.1; V6-S3', '0561; A78 N2; A99.1; V6-S3; A105; 0642', 'B8 source')), 3, 'revised', ['A105'], 'A105 W7-S1')
    row = crow('C1. ')
    cset('C1', 'C1. ', (row[0] + ' The outputs stay on the internal SSD (A85.3); root\'s watchdog alerts below 80 GB free, and if it fires root rules either '
                        'relocating the cases not yet started or pausing admission; the per-case caps are unchanged (A105 RP-S2).', None,
                        sub1(row[2], 'RUNBOOK of BUILD_V007; A85; A88', 'RUNBOOK of BUILD_V007; A85; A88; A105', 'C1 source')), 3, 'revised', ['A105'], 'A105 RP-S2')
    row = crow('Compare r8, r10, r11;')
    t0 = sub1(row[0], 'Compare r8, r10, r11;', 'Compare r8, r10, r11 and r12 (r12: A102);', 'SUPERSEDED')
    t0 = sub1(t0, 'B2 C3V002 d4b41ffc (A100, A101); r6 (A96); the r4 checklist.',
              'B2 C3V002 d4b41ffc (A100, A101); registry C3V008 f189cd3f (C3V009 is the candidate: A101, Claude3 0087, A106.1); driver r6 (A96); the r4 and '
              'r5 checklists.', 'SUPERSEDED')
    cset('SUPERSEDED', 'Compare r8, r10, r11;', (t0, None, sub1(row[2], 'A79; A80; A90; A96; A99; A101', 'A79; A80; A90; A96; A99; A101; A102; A106.1',
                                                                 'SUPERSEDED source')), 2,
         'revised', ['A102', 'A106.1', 'A101'], 'compare r12 (A102) and registry C3V008 superseded; "driver r6" kept apart from prereg r6; the r5 '
         'checklist superseded by this one (A106.1)')
    log(1, 'SEAL_CHECKLIST_R6 header', 'header', [], ['A99.3', 'F-01'], 'title r6 and the assembly time')
    # ================================================================= consistency, both ways, between the rows A102-A106 and the edits
    logged = [c for c in changes if c['clause'] not in ('root_items (order)', 'SEAL_CHECKLIST_R6 header')]

    def entries_of(trace):
        return {m.group(1) for t in trace for m in [re.match(r'(A[0-9]+)(\.[0-9]+)?$', t)] if m and m.group(1) in ROWS6}

    def row_steps(x):
        out_ = []
        for cl_ in x['revised_clauses']:
            if cl_.startswith('SEAL_CHECKLIST_R6 '):
                out_ += [s.strip() for s in cl_[len('SEAL_CHECKLIST_R6 '):].split(',')]
        return out_
    for x in new_rows:
        e = x['entry']
        for cl_ in x['revised_clauses']:
            if cl_.startswith('SEAL_CHECKLIST_R6 '):
                continue
            if not any(e in entries_of(c['trace']) and (covers(cl_, c['clause']) or covers(c['clause'], cl_)) for c in logged):
                raise SystemExit('row %s names %s, which no edit traced to %s changes' % (e, cl_, e))
        for s in row_steps(x):
            if s not in cedits or e not in entries_of(cedits[s]):
                raise SystemExit('row %s names checklist step %s, which no edit traced to %s changes' % (e, s, e))
    rows_by = {x['entry']: x for x in new_rows}
    for c in logged:
        for e in entries_of(c['trace']):
            x = rows_by[e]
            if c['clause'].startswith('SEAL_CHECKLIST_R6 '):
                if c['clause'][len('SEAL_CHECKLIST_R6 '):] not in row_steps(x):
                    raise SystemExit('edit %s is traced to %s, whose row does not name that step' % (c['clause'], e))
            elif not any(covers(cl_, c['clause']) for cl_ in x['revised_clauses'] if not cl_.startswith('SEAL_CHECKLIST_R6 ')):
                raise SystemExit('edit %s is traced to %s, whose row does not name that clause' % (c['clause'], e))
    # ================================================================= the leaf diff r5 -> r6 must lie inside logged clauses
    L5 = {pname(k): v for k, v in leaves(doc5).items()}
    L6 = {pname(k): v for k, v in leaves(doc).items()}
    dl = sorted(k for k in set(L5) | set(L6) if L5.get(k) != L6.get(k))
    json_logged = [c['clause'] for c in changes if not c['clause'].startswith('SEAL_CHECKLIST') and c['clause'] != 'root_items (order)']
    unc = []
    for k in dl:
        if any(covers(c, k) for c in json_logged):
            continue
        m = re.match(r'(.+)\.sources\[\d+\]$', k)
        if m and any(c == m.group(1) or c.startswith(m.group(1) + '.') for c in json_logged):
            continue
        unc.append(k)
    if unc:
        raise SystemExit('leaves changed outside logged clauses: %s' % unc[:8])
    idle = [c for c in json_logged if not any(covers(c, k) for k in dl)]
    if idle:
        raise SystemExit('logged clauses with no changed leaf: %s' % idle)
    for x in doc5['entries_after_A81']['rows']:
        if x not in rows:
            raise SystemExit('an r5 row changed')
    if doc['binding_inputs']['case_block'] != case_block_r5 or sha(case_block_r5['path']) != P['case_block']['sha256']:
        raise SystemExit('binding_inputs.case_block is not byte-identical to r5 (item 8)')
    ck5 = parse_checklist(ck_text, 'r5')[2]
    n_changed = sum(1 for i in range(len(ck)) if ck[i] != ck5[i])
    if len(ck) != len(ck5) or n_changed != len(cedits):
        raise SystemExit('checklist rows changed (%d of %d) differ from the logged checklist edits (%d)' % (n_changed, len(ck), len(cedits)))
    # ================================================================= render everything in memory, then write (exclusive create)
    outs = {}
    outs['KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json'] = json.dumps(doc, indent=1, ensure_ascii=False, allow_nan=False) + '\n'
    D = ['# Delta r5 -> r6 (KMAX_TAIL_PREREG_V007_FINAL_DRAFT)', '',
         'Each line is one recorded edit applied to r5 (3245899f) by %s, with its trace to a ruling (A-entry) or a finding of the r5 check (F-; '
         'REPORT_R5CHK_C4V002 caea77aa). The item column is the r6 brief item: 1 the entry table, the closed V005 and the header; 2 the compare slot; '
         '3 the launch packet; 4 the seal record requirements; 5 the F-11 fixes; 6 F-13; 7 the registry; 9 seal tools v003. Item 8 (the case block '
         'binding) changes nothing. Rows named SEAL_CHECKLIST_R6 are edits of the root checklist. Closed V005 addendum at generation: %s, %d bytes '
         '(entries A47-%s; byte copy %s).' % (Path(__file__).name, v005_sha, len(vb), newest, COPY_REL), '',
         '| # | item | clause | kind | added sources | trace | why |', '|---|---|---|---|---|---|---|']
    D += ['| %d | %d | `%s` | %s | %s | %s | %s |' % (i + 1, c['item'], c['clause'], c['kind'], '; '.join(c['added_sources']), '; '.join(c['trace']), c['why'])
          for i, c in enumerate(changes)]
    outs['DELTA_R5_R6.md'] = '\n'.join(D) + '\n'
    if render_entry_table('r5', entry_table_r5_header(doc5['entries_after_A81']['addendum_read']['sha256_at_generation'], len(b5),
                                                      doc5['entries_after_A81']['section_rule']), doc5['entries_after_A81']['rows']) != \
            (R5D / 'ENTRY_TABLE_R5.md').read_text():
        raise SystemExit('the entry-table renderer does not reproduce ENTRY_TABLE_R5.md')
    et_head = ('# ENTRY_TABLE_R6: V005 entries A82-%s against prereg r6 (A99.3; the seal record quotes this table)\n\n'
               'Closed V005 addendum (A106.3) read at r6 generation: sha256 `%s`, %d bytes (byte copy `%s`). V005 closes with A106, so this table '
               'covers every V005 entry after A81; root\'s later rulings are V006 entries. %s' % (newest, v005_sha, len(vb), COPY_REL, ea['section_rule']))
    outs['ENTRY_TABLE_R6.md'] = render_entry_table('r6', et_head, rows)
    ri = doc['root_items']
    opened = [x['id'] for x in ri if x['status'] == 'OPEN']
    ri5 = doc5['root_items']
    if render_root_items('r5', 'RI-27 is resolved by A82 (ruled as drafted in r4). RI-24 is moot for V007 (A96). Open: %s. Every recommendation is a '
                         'recommendation only.' % ', '.join(x['id'] for x in ri5 if x['status'] == 'OPEN'), ri5) != (R5D / 'ROOT_ITEMS_R5.md').read_text():
        raise SystemExit('the root-items renderer does not reproduce ROOT_ITEMS_R5.md')
    outs['ROOT_ITEMS_R6.md'] = render_root_items('r6', 'RI-27 is resolved by A82 (ruled as drafted in r4); RI-28 by A102 and A104 (the fix round r13 is the '
                                                       'compare of record); RI-29 by A105 (BUILD_V007 stays bound); RI-34 by A106.3 (V005 closed at A106; '
                                                       'the table ends at A106). RI-24 is moot for V007 (A96). Open: %s. Every recommendation is a '
                                                       'recommendation only.' % ', '.join(opened), ri)
    outs['SEAL_CHECKLIST_R6.md'] = render_checklist('r6', ts, tail5, ck)
    changed_all = [c for c in json_logged]
    M = ['# Clause -> source map, r6: KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6 (unsealed)', '',
         'Sources are rulings (A-entries, dispatches) or evidence; the trace of every r6 edit to a ruling or an r5-check finding is in DELTA_R5_R6.md.',
         '', '| clause | sources | changed in r6 |', '|---|---|---|']
    newset = set(later)
    for k, s in clause_rows(doc, rows):
        if k.startswith('entries_after_A81.'):
            yes = k.split(' ')[0].split('.', 1)[1] in newset
        else:
            yes = any(c == k or c.startswith(k + '.') or c.startswith(k + '[') or k.startswith(c + '.') for c in changed_all)
        M.append('| `%s` | %s | %s |' % (k, '; '.join(s), 'yes' if yes else ''))
    outs['CLAUSE_SOURCE_MAP_R6.md'] = '\n'.join(M) + '\n'
    bi = doc['binding_inputs']
    cpn = doc['seal_slots']['compare']['named_candidates_verified_from_bytes']
    H = ['# KMAX_TAIL_PREREG_V007: final draft r6 (UNSEALED)', '', doc['status'], '',
         '**Assembly:** Claude4 r6 helper, single author, UTC %s. Base: r5 `%s`. Dispatch 0643 `%s` (A106.1 approves r6); Claude4 0109 `%s`; r5 check '
         'REPORT_R5CHK_C4V002 `%s`.' % (ts, R5_SHA, P['dispatch_0643']['sha256'], P['Claude4_0109']['sha256'], P['r5_check_report_C4V002']['sha256']), '',
         'The full clause text is in the JSON; `CLAUSE_SOURCE_MAP_R6.md` traces every clause; `DELTA_R5_R6.md` lists every edit with its trace; '
         '`ENTRY_TABLE_R6.md` is the A99.3 table; `SEAL_CHECKLIST_R6.md` and `ROOT_ITEMS_R6.md` are the root-facing lists.', '',
         '## The closed V005 addendum (A106.3)', '',
         '- `entries_after_A81.addendum_read`: sha256 `%s`, %d bytes; byte copy `%s`.' % (ea['addendum_read']['sha256_at_generation'],
                                                                                          ea['addendum_read']['bytes'], copy_abs),
         '- %s' % ea['rule'], '',
         '## The case block (A99.2, A101)', '', '- `binding_inputs.case_block`: `%s` sha256 `%s`.' % (bi['case_block']['path'], bi['case_block']['sha256']),
         '- %s' % bi['case_block_rule']['text'], '',
         '## The final compare round (A102, A103, A104)', '',
         '- r13 `%s` sha256 `%s`; selection `%s` sha256 `%s`.' % (cpn['r13_cx3v001_final_round']['path'], cpn['r13_cx3v001_final_round']['sha256'],
                                                                  cpn['r13_selection']['path'], cpn['r13_selection']['sha256']),
         '- Delta review of record, Claude3 0092 `%s`: %s.' % (cpn['delta_review_of_record_Claude3_0092']['sha256'], cpn['delta_review_of_record_Claude3_0092']['verdict']),
         '- Delta review of record, Codex1 0076 `%s`: %s.' % (cpn['delta_review_of_record_Codex1_0076']['sha256'], cpn['delta_review_of_record_Codex1_0076']['verdict']),
         '- r12 `%s`: %s.' % (cpn['r12_superseded_A102']['sha256'], cpn['r12_superseded_A102']['note']), '',
         '## The launch-packet BUILD of record (A99.1, A105)', '',
         '- BUILD_V007 `%s` sha256 `%s` (filled from bytes; re-verified at r6 generation: 15 supported sources, template %s launches the case block\'s '
         'ten FILLED specs; Claude4 delta 0108 `%s`: %s; it stays bound, A105).' % (
             lpn['build']['path'], lpn['build']['sha256'], lpn['template_plan']['sha256'][:8], lpn['build_v007_delta_review_Claude4_0108']['sha256'],
             lpn['build_v007_delta_review_Claude4_0108']['verdict']), '',
         '## Seal slots (root fills at seal assembly; never guessed)', '']
    for k, s in doc['seal_slots'].items():
        H.append('- **%s**: value `%s`. %s  \n  *Sources: %s*' % (k, s['value'], s['rule'], '; '.join(s['sources'])))
    H.extend(['', '## Entry table A82-%s (A99.3)' % newest, '', '| entry | decision | section sha256 |', '|---|---|---|'])
    H += ['| %s | %s | `%s` |' % (x['entry'], 'revised here' if x['decision'] == RH else 'no change', x['section_sha256'][:16] + '...') for x in rows]
    H.extend(['', '## Seal record requirements', ''])
    for x in doc['seal_record_requirements']:
        H.append('- %s *(%s)*' % (x['text'], '; '.join(x['sources'])))
    H.extend(['', '## Clauses changed in r6', ''])
    for c in changes:
        H.append('- `%s` (%s; item %d; trace %s): %s' % (c['clause'], c['kind'], c['item'], ', '.join(c['trace']), c['why']))
    H.extend(['', '## Root items', '', 'RI-27 RESOLVED (A82); RI-28 RESOLVED (A102, A104); RI-29 RESOLVED (A105); RI-34 RESOLVED (A106.3); RI-24 moot (A96). '
              'OPEN: %s (see `ROOT_ITEMS_R6.md`).' % ', '.join(opened), ''])
    outs['KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.md'] = '\n'.join(H) + '\n'
    if sorted(outs) != sorted(OUT_NAMES):
        raise SystemExit('output set')
    present = [str(p) for p in targets if os.path.lexists(p)]
    if present:
        raise SystemExit('outputs appeared during the run: %s' % present)
    for n in OUT_NAMES:
        with open(out / n, 'xb') as f:
            f.write(outs[n].encode('utf-8'))
    for n in OUT_NAMES:
        if (out / n).read_bytes() != outs[n].encode('utf-8'):
            raise SystemExit('%s does not read back equal' % n)
    print(json.dumps({'written': str(out), 'files': {n: sha(out / n) for n in OUT_NAMES}, 'v005_closed_copy': v005_sha, 'newest': newest,
                      'rows': len(rows), 'edits': len(changes), 'checklist_edits': sorted(cedits), 'leaves_changed': len(dl), 'open_root_items': opened},
                     indent=1))


if __name__ == '__main__':
    main()
