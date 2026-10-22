# Claude4 helper (dispatch 0650, V006 A113 P6; A58 RI-10 / A81 RI-20): build seal tool 4's B7 NEW-item disposition input,
#   {"schema": NEW_ITEMS_SCHEMA, "compare_impl": {path, sha256}, "items": [{id, disposition, reason, must_fail_tests}], "note"}
# The id index is root's C-08 table (SEAL_MANUAL_DISCLOSURES_V002 a0284ece, key c08_table). Every disposition is compiled from the
# compare rounds' IMPL documents (v007_compare_c2/r*/COMPARE_V007_IMPL_R*.md, opened by name). Every quote below is located in the
# cited file's bytes at generation time (unique line; the line must name the id where marked), every file is hashed from bytes, and
# every MUST_FAIL test string is checked to occur verbatim in its IMPL and to resolve to tests that PASS in the run of record of the
# variant's compare (TEST_SUMMARY.json, whose script_sha256 must be that compare). Nothing is imported from the compare or its suite.
# An id whose disposition no IMPL states, and which RI-10 does not decide, is NOT written (root must rule): PENDING_ROOT below.
# Root may later complete the list: --root-ruling NEW-30=ADOPTED --root-ruling-ref "V006 A1xx ..." (repeatable; REJECTED allowed).
# Modes: --dry-run (build + every check, print the sha, write nothing) | --write PATH (exclusive create, open 'x').
# usage: make_new_items_c4v001.py --variant r13|r14 --utc T [--root-ruling ID=ADOPTED|REJECTED ... --root-ruling-ref TEXT]
#        [--require-complete] (--dry-run | --write PATH)
import ast, hashlib, json, re, sys
from pathlib import Path

V = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/'
TOOL4 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004/build_seal_record_c4v004.py',
         '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41')
DISCLOSURES = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json',
               'a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3')
DISCLOSURES_V003_DRAFT = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V003_DRAFT.json',
                          '21968a07f50d6bf5dda9e64cfa61c7e3ec80bca9943c0f84956611ac99b8be3e')
V005 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md',
        'c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1')       # the closed V005 bytes (prereg r6 addendum_read)
IMPL = {'r2': V + 'r2/COMPARE_V007_IMPL_R2.md', 'r3': V + 'r3/COMPARE_V007_IMPL_R3.md', 'r4': V + 'r4/COMPARE_V007_IMPL_R4.md',
        'r5': V + 'r5/COMPARE_V007_IMPL_R5.md', 'r6': V + 'r6/COMPARE_V007_IMPL_R6.md', 'r7': V + 'r7/COMPARE_V007_IMPL_R7.md',
        'r8': V + 'r8/COMPARE_V007_IMPL_R8.md', 'r10': V + 'r10/COMPARE_V007_IMPL_R10.md', 'r11': V + 'r11/COMPARE_V007_IMPL_R11.md',
        'r12': V + 'r12/COMPARE_V007_IMPL_R12.md', 'r13': V + 'r13/COMPARE_V007_IMPL_R13.md'}
VARIANTS = {
    'r13': {'compare': (V + 'r13/kmax_tail_compare_c2v007_r13_cx3v001.py', 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'),
            'impl': (V + 'r13/COMPARE_V007_IMPL_R13.md', '274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3'),
            'run': (V + 'r13/out/author_cx3v001/TEST_SUMMARY.json', 'cad67c41fd8b7d56d092ac070fabfe5dc79dce6280e3e7f3e98ccfdbf81dd60c'),
            'why': 'the r13 compare of record (V005 A104) and its IMPL of record (prereg r6 erratum E-R6-1)'},
    'r14': {'compare': (V + 'r14/kmax_tail_compare_c2v007_r14_cx1v001.py', 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'),
            'impl': (V + 'r14/COMPARE_V007_IMPL_R14_CX1V002.md', '2ba6d12ecc36ab444365348573b7f49a02a12a818dd15d67de35d77300fa17c9'),
            'run': (V + 'r14/out/author_v002/TEST_SUMMARY.json', '42c4961f8af24836d7da99ba699802a150b06bd68e931b544ed81a42e1a558e1'),
            'why': ('the r14 compare (V006 A114: r13 plus I4 in GATE_RECORD_AFTER_SEAL_ALLOWED; SELECTED_R14_CX1V002 status '
                    'SELECTED_BUILD_FOR_CLAUDE3_CLAUDE4_REVIEW) and its IMPL CX1V002, which binds the r14 source sha and declares no NEW item; '
                    'for use only if root\'s compare_reviewed_source slot is r14')},
}
BASIS = {
    'IMPL_STATED': 'the disposition is stated in an IMPL (quoted)',
    'RI10_FROM_IMPL_DECLARATION': ('no IMPL writes the word adopted for this id: the originating IMPL declares it stricter (quoted), and A58 RI-10 '
                                   '(made general by A81 RI-20) adopts as text an item that is stricter on adoption and fills a gap; root\'s '
                                   'c08_confirmation (SEAL_MANUAL_DISCLOSURES_V002) says the dispositions follow A58 RI-10 / A81 RI-20 as declared '
                                   'in the originating rounds\' IMPLs'),
    'ROOT_RULED_ITEM': ('the item is not a proposal: the originating IMPL states that it carries out root rulings (quoted), and a later IMPL '
                        'records their implementation (quoted)'),
    'ROOT_RULING_SUPPLIED': 'root\'s own ruling, supplied to this generator with --root-ruling and --root-ruling-ref (quoted)',
}
RULE_TEXTS = [('V005', 'adopted as text if it is stricter on adoption and fills a gap, and rejected if it is looser', 'NEW-21'),
              ('V005', 'RI-10\'s adoption rule applies to every NEW item the final compare IMPL declares', None)]
# evidence: (source, quote, id_must_be_on_the_line[, role])   source = an IMPL round key, or 'V005'
# tests: (source, name)   source = an IMPL round key (the name must occur verbatim in that IMPL), 'RUN_TAG' (a run test whose covers
#        name the id) or 'RUN_NAME' (an exact run test name the IMPL describes without printing it)
ITEMS = [
    {'id': 'NEW-4', 'disposition': 'ADOPTED', 'basis': 'RI10_FROM_IMPL_DECLARATION',
     'what': 'the RO1 worker must match the column_workers kind (serial for 1, parallel otherwise)',
     'intro': ('r2', '**NEW-4 (declared, stricter).** The RO1 worker must match the column_workers kind', True),
     'evidence': [('r2', 'None adopts anything.', False, 'context, the r2 section preface: the items are declared for root and none adopts a reading on its own'),
                  ('r3', '**FIXED (stricter).** The NEW-4 worker-kind check now also applies to identity runs.', True, 'the r3 recheck extends the NEW-4 check to identity runs (stricter)'),
                  ('r10', 'The existing custody checks already enforce the role table per case family', False, 'root A77.2 RO1 role table, implemented in r10: the serial or parallel worker by the admitted column_workers')],
     'rulings': [],
     'tests': [('r3', 'R3_ORDER_N8_*'), ('RUN_TAG', 'R4_VALIDITY_F1_D5_NODES_SERIAL_WORKER_ON_PARALLEL8_INVALID')]},
    {'id': 'NEW-7', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'a tau-norm ratio >= 1 on either of the last two ratios makes E unavailable (A53 chose this stricter option)',
     'intro': ('r3', 'Root to say whether a non-contracting run should instead make E unavailable', True),
     'evidence': [('r5', 'on either of the last two ratios makes E unavailable', True, 'r5, section A53 implemented: the stricter option root ruled')],
     'rulings': [('V005', 'on either of the last two ratios has E', True, 'root ruling A53')],
     'tests': [('r5', 'C3_B1_H2_NEW7'), ('r5', 'C3_H1_N7'), ('r5', 'A51_F2_NON_CONTRACTING_RATIO_2_E_UNAVAILABLE_A53_NEW7'),
               ('r5', '…_INFINITE_E_UNAVAILABLE_A53_NEW7')]},
    {'id': 'NEW-13', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'the nodes_v001 RO1 workers are on the custody list, scoped to cases whose registered source_rule is nodes_v001',
     'intro': ('r4', 'Confirm nodes workers dbb331db and 5a4c7d41 on the A50 item 11/12 custody list', True),
     'evidence': [('r5', 'Confirmed as implemented.', True, 'r5, section A53 implemented: confirmed'), ('r7', 'the nodes workers are 0ae245d8 / a5277172 (A62.3)', False, 'r7 moves the nodes pins to driver r5 (A62.3)')],
     'rulings': [('V005', 'Confirmed. The nodes RO1 workers (serial dbb331db, parallel 5a4c7d41, binding 86af6198) are on the custody list', True, 'root ruling A53')],
     'tests': [('r4', 'R4_VALIDITY_F1_*'), ('r5', 'A53_NEW13'), ('r7', 'A53_NEW13_NODES_RO1_WORKERS_ON_THE_CUSTODY_LIST_FROM_BYTES')]},
    {'id': 'NEW-16', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'a ROUTE_A-branch member\'s route-A identity must be a sha and differ from its base\'s',
     'intro': ('r4', 'Confirm the stricter ROUTE_A identity rule.', True),
     'evidence': [('r4', 'A ROUTE_A-branch member\'s route-A identity must be a sha and differ from its base\'s.', False, 'the r4 order N-c fix: FIXED (stricter, DECLARED)'),
                  ('r5', 'Unchanged: the C5H ROUTE_A member carries ro1_workers and runs armed, with its own identity.', True, 'r5, section A53 implemented')],
     'rulings': [('V005', 'NEW-16 is confirmed: a ROUTE_A member\'s route-A identity must differ from its base\'s.', True, 'root ruling A53')],
     'tests': [('r4', 'R4_ORDER_Nc_*'), ('r5', 'C3_R3_P11'), ('r5', 'A53_ROUTE_A_BRANCH_UNCHANGED')]},
    {'id': 'NEW-17', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'R-PAIR members named for a test whose R-PAIR was not triggered are refused at load',
     'intro': ('r4', 'Unused R-PAIR members: refuse them at manifest load, or ignore them for both flags and validity.', True),
     'evidence': [('r5', 'NEW-17: untriggered members refused at load', True, 'r5, section A53 implemented: the option root ruled'),
                  ('r6', 'NEW-17 refuses only when decidability is known and only in full mode.', True, 'r6 keeps the declared scope (A58 RI-10 table, row NEW-25)')],
     'rulings': [('V005', 'This is stricter, and it prevents choosing among reruns.', True, 'root ruling A53')],
     'tests': [('r5', 'A53_NEW17_DECIDABILITY_UNKNOWN…'), ('r5', 'A53_NEW17_CLI_REFUSAL_RC2_NO_OUTDIR')]},
    {'id': 'NEW-19', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'the declared successor EPS field contract envelope_bound {rule, coverage_max_inverse_kpc}; SRB_ROT is not read without it',
     'intro': ('r4', 'Confirm the declared successor EPS field contract:', True),
     'evidence': [('r4', 'The **field contract is DECLARED by R4** (NEW-19)', True, 'r4, the A52.5 implementation'), ('r5', 'NEW-19 is read on the real EPS V006.', True, 'r5, section A53 implemented: confirmed as implemented')],
     'rulings': [('V005', 'The certificates_v002 producer emits exactly this.', True, 'root ruling A53')],
     'tests': [('r4', 'R4_A52_5_*'), ('r5', 'A53_NEW19')]},
    {'id': 'NEW-21', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'the two-directional S5 verdict reading (verdict-data contradictions are defects; VERDICT_ONLY gates; registered fail verdicts)',
     'intro': ('r5', '**NEW-21 (S5 reading).**', True),
     'evidence': [('r5', 'None of these adopts anything; each is the stricter reading where the text is silent.', False, 'context, the r5 section preface'),
                  ('r6', '**Adopted**: stricter and fills gaps.', True, 'the r6 A58 RI-10 disposition table')],
     'rulings': [('V005', 'adopted as text if it is stricter on adoption and fills a gap, and rejected if it is looser', True, 'root ruling A58 RI-10')],
     'tests': [('r5', 'C3_S5_H1_F2'), ('r5', 'D1_I1T_FAIL_VERDICT_WITH_A_FAILING_BUILD_CASES_INCOMPLETE_A54_S5'),
               ('r5', '…_RECORD_DEFECT_NO_RUN_A54_S5'), ('r5', '…_EPS_DATA_AND_VERDICT_AGREE_A54_S5')]},
    {'id': 'NEW-31', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'a B4 gap case whose R-PAIR members reach the floor reads UAIF PROVISIONAL on the B4 step; it adopts nothing',
     'intro': ('r6', 'reads UAIF PROVISIONAL on a B4 step that cannot resolve.', True),
     'evidence': [('r6', 'Pinned as `R6_ORDER_N2_…` (NEW-31).', True, 'r6 keeps the reading and pins it'), ('r8', 'Accepted, as implemented. No change.', True, 'r8, section A67 implemented: accepted')],
     'rulings': [('V005', 'It is undecidable and adopts nothing. Accepted.', True, 'root ruling A67')],
     'tests': [('r6', 'R6_ORDER_N2_…'), ('r8', 'R8_A67_NEW31_…')]},
    {'id': 'NEW-34', 'disposition': 'ADOPTED', 'basis': 'RI10_FROM_IMPL_DECLARATION',
     'what': 'the S9 boundary: a pass with no row-set is the B4 gap; any present row-set that is not exactly the 12 ids is S9 (invalid), '
             'non-object entries included; S9 applies to identity runs too',
     'intro': ('r6', '**NEW-34 (S9 boundary, DECLARED).**', True),
     'evidence': [('r6', 'A rows list with non-object entries is S9; r5 read it as B4.', False, 'declaration, stricter than r5'),
                  ('r6', 'S9 also applies to identity runs (stricter).', False, 'declaration'),
                  ('r7', 'The finding is correct on the compare\'s own declared contract', True, 'r7 accepts the BLOCKING order B1 finding against NEW-34 as the compare\'s declared contract and enforces it')],
     'rulings': [],
     'tests': [('r6', 'S9_UNIT…'), ('r10', 'R10_C3_R7_A_N1_*'), ('RUN_TAG', 'R7_ORDER_B1_UNIT_PRESENT_NON_LIST_ROW_SET_IS_S9_ABSENT_NULL_EMPTY_ARE_THE_B4_GAP')]},
    {'id': 'NEW-39', 'disposition': 'ADOPTED', 'basis': 'ROOT_RULED_ITEM',
     'what': 'the custody pins and the drivers_allowed I4 set move to driver v010 r5 (A56 follow-up 3, carried out as A62.3)',
     'intro': ('r6', '**NEW-39 (A56 follow-up 3).** v010 r5 is not landed.', True),
     'evidence': [('r7', '**A62.3** custody pins to v010 r5', False, 'r7 implements root A62.3: the custody pins move to driver r5')],
     'rulings': [('V005', 'When driver v010 r5 lands, the compare\'s custody pins (PIN_RO1_CUSTODY, PIN_RO1_NODES_CUSTODY, the drivers_allowed I4 set) '
                          'move to r5\'s re-pinned shas', False, 'root A56 entry, row A55 follow-up 3 (the r6 IMPL calls it A56 follow-up 3)')],
     'tests': [('r7', 'A62_3_V010_R5_CHECK_PIN_PENDING_AND_R5_CUSTODY_PINS_VERIFIED_FROM_BYTES'),
               ('r7', 'A54_A62_3_SEALED_MODE_WITH_A55_SET_STILL_REFUSES_WITHOUT_THE_V010_R5_CHECK'),
               ('RUN_TAG', 'R7_A62_3_PINS_ARE_THE_R5_CASCADE_IMAGES_OF_THE_R4_SHAS_BINDING_UNCHANGED')]},
    {'id': 'NEW-52', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'every gate is bound by its gate-record sha of record; PRODUCED_AFTER_THE_SEAL only on the post-seal gate allow-list (A75.7)',
     'intro': ('r8', '**NEW-52 (A67 N2 scope, DECLARED).**', True),
     'evidence': [('r8', 'R8 binds **every** gate that way (stricter).', False, 'declaration (stricter)'),
                  ('r10', 'The token is accepted only on `GATE_RECORD_AFTER_SEAL_ALLOWED`', True, 'r10, section Items implemented: NEW-52 under A75.7'),
                  ('r10', 'Fixed (NEW-52 / A75.7 allow-list).', True, 'r10 disposition of the r8 recheck')],
     'rulings': [('V005', 'PRODUCED_AFTER_THE_SEAL is accepted **only** for gates whose inputs are V007 run outputs', False, 'root A75 item 7 (P-N2), the allow-list r10 implements; A79 and A88 later adjust the list')],
     'tests': [('r10', 'R10_NEW52_*')]},
    {'id': 'NEW-53', 'disposition': 'ADOPTED', 'basis': 'RI10_FROM_IMPL_DECLARATION',
     'what': 'the top-level eps_max_envelope_all_shells must agree with the nested value; a top-level copy with no envelope_bound block '
             'is a RECORD_DEFECT',
     'intro': ('r8', '**NEW-53 (A67 N4 extension, DECLARED, stricter).**', True),
     'evidence': [('r8', 'A top-level copy with no `envelope_bound` block is a RECORD_DEFECT.', False, 'declaration'),
                  ('r8', 'Fixed by A67 N4, plus the top-level maximum (NEW-53).', True, 'r8 disposition of the r7 recheck N4')],
     'rulings': [('V005', 'The top-level and nested "dominates" flags must agree.', False, 'the root A67 N4 ruling this item extends')],
     'tests': [('RUN_TAG', 'R8_A67_N4_EPS_TOP_LEVEL_ENVELOPE_MAX_DISAGREES_RECORD_DEFECT_NO_RUN'),
               ('RUN_NAME', 'R8_A67_N4_EPS_TOP_LEVEL_FLAG_WITHOUT_ENVELOPE_BOUND_RECORD_DEFECT_NO_RUN')]},
    {'id': 'NEW-54', 'disposition': 'ADOPTED', 'basis': 'RI10_FROM_IMPL_DECLARATION',
     'what': 'any two of the SR_K deltas bitwise identical refuses, not only all three',
     'intro': ('r8', 'bitwise identical refuses, not only all three.', True),
     'evidence': [],
     'rulings': [('V005', 'across K is an SR_K RECORD_DEFECT.', False, 'the root A67 N2 ruling this item extends')],
     'tests': [('RUN_TAG', 'R8_A67_N2_SR_K_TWO_OF_THREE_DELTAS_IDENTICAL_RECORD_DEFECT_NO_RUN')]},
    {'id': 'NEW-60', 'disposition': 'ADOPTED', 'basis': 'ROOT_RULED_ITEM',
     'what': 'A68 CHK-1 (certificate M_s bound to the registered gas.M_s) and A69 notes 1 and 3, implemented in the round after r8',
     'intro': ('r8', 'Ruled by A68 and A69 for the round after r8:', True),
     'evidence': [('r10', 'reads the case block\'s C4T uv_tail `gas.M_s`.', False, 'r10 implements A68 CHK-1'),
                  ('r10', 'hashes every pinned file from bytes at load.', False, 'r10 implements A69 note 1'),
                  ('r10', 'on an exact tie the **lowest row index**', False, 'r10 implements A69 note 3')],
     'rulings': [('V005', 'also implements A68 CHK-1 (certificate M_s bound to the registered gas.M_s) and A69 (producer-byte hashing', False, 'root entry naming the implementation of A68 CHK-1 and A69 in the next round')],
     'tests': [('r10', 'R10_A68_CHK1_*'), ('r10', 'R10_A68_RECORDS_*'), ('r10', 'R10_A69_1_*'), ('r10', 'R10_A69_3_*')]},
    {'id': 'NEW-64', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'H-07: every multiply-linked regular file on the registered run\'s device is refused (test-mode full mode), never listing the run',
     'intro': ('r10', '**NEW-64: the H-07 hard-link rule.**', True),
     'evidence': [('r10', 'R10 instead refuses every multiply-linked regular file on the registered run\'s device', False, 'declaration'),
                  ('r11', 'NEW-64 (the multiply-linked-file substitute, accepted in A79)', True, 'r11: carried as ruled')],
     'rulings': [('V005', '**NEW-64 (H-07 substitute) is accepted.**', True, 'root ruling A79')],
     'tests': [('r10', 'R10_H07_*')]},
    {'id': 'NEW-71', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'the A75.6 fixed map extended to every DDO roster name',
     'intro': ('r11', 'stricter where silent (A79.1 "every roster")', True),
     'evidence': [],
     'rulings': [('V005', 'otherwise each is adopted as declared, and the seal record quotes the list.', True, 'root ruling A86.5 on NEW-71 to NEW-81')],
     'tests': [('r11', '…_EXTRA_ROSTER_OFF_THE_MAP_…'), ('r11', '…_WRONG_FIXED_GEOMETRY_ONLY_*')]},
    {'id': 'NEW-73', 'disposition': 'ADOPTED', 'basis': 'IMPL_STATED',
     'what': 'a BUILD check_record must name the driver, carry a PASS verdict token and not be a gate record',
     'intro': ('r11', 'minimal properties; root may tighten', True),
     'evidence': [('r12', 'Preserve NEW-73 lexical text policy', True, 'r12 preserves it (CX2-R11-AB-N1)'),
                  ('r13', 'The check-record parser now uses parse_int=str locally.', False, 'r13 (A102) tightens the same check-record parser')],
     'rulings': [('V005', 'otherwise each is adopted as declared, and the seal record quotes the list.', False, 'root ruling A86.5 on NEW-71 to NEW-81')],
     'tests': [('r11', 'R11_R10_RECHECK_VALIDITY_N2_…')]},
]
PENDING_ROOT = {
    'NEW-30': {'what': 'reporting only: named.gates_failing_reported lists every FAILing gate with its next step, NO_RUN included; no '
                       'reading changes',
               'intro': ('r6', 'Reporting only; the reading is unchanged.', True),
               'evidence': [('r6', 'Root to confirm (NEW-30).', True, 'the r6 IMPL asks root'), ('r10', 'and on the open NEW-30 to NEW-60.', True, 'still open at r10')],
               'why_root': 'RI-10 does not decide it (reporting only: neither stricter nor looser), the r6 IMPL asks root to confirm, '
                           'and no IMPL or addendum entry records a ruling',
               'tests': [('RUN_TAG', 'R6_VALIDITY_F2_NO_RUN_STILL_REPORTS_THE_FAILING_EPS_AND_T2I_GATES_WITH_NEXT_STEPS')]},
    'NEW-44': {'what': 'RB_FP keeps EPS eps_max and is not an envelope consumer; a record that uses the envelope value fails closed '
                       '(CROSSREF_MISMATCH)',
               'intro': ('r7', 'Is RB_FP an envelope consumer?', True),
               'evidence': [('r7', 'Root to rule (NEW-44).', True, 'the r7 IMPL asks root')],
               'why_root': 'it is a question for root (RB_FP is or is not an envelope consumer); a yes would change RB_FP\'s epsilon '
                           '(1.277x larger on V006) and so could change a physics reading; no IMPL or addendum entry records a ruling',
               'tests': [('RUN_TAG', 'R7_SF3_NEW44_RB_FP_ON_THE_ENVELOPE_EPS_CROSSREF_MISMATCH_PINNED')]},
}


class Refuse(Exception):
    pass


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def read_pinned(path, sha=None):
    raw = Path(path).read_bytes()
    got = sha_bytes(raw)
    if sha is not None and got != sha:
        raise Refuse('PIN_MISMATCH %s has %s, pinned %s' % (path, got, sha))
    return raw, got


def pairs(ps):
    out = {}
    for k, v in ps:
        if k in out:
            raise Refuse('DUPLICATE_JSON_KEY %r' % (k,))
        out[k] = v
    return out


def no_constant(c):
    raise Refuse('NON_FINITE_JSON_CONSTANT %s' % c)


def strict(raw):
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=no_constant)


def module_string(raw, name):
    vals = [n.value.value for n in ast.parse(raw.decode('utf-8')).body if isinstance(n, ast.Assign) and len(n.targets) == 1
            and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name and isinstance(n.value, ast.Constant)
            and isinstance(n.value.value, str)]
    if len(vals) != 1:
        raise Refuse('MODULE_STRING_NOT_UNIQUE %s' % name)
    return vals[0]


class Doc:
    def __init__(self, path, sha=None):
        raw, self.sha = read_pinned(path, sha)
        self.path, self.text = path, raw.decode('utf-8')
        self.lines = self.text.split('\n')

    def locate(self, quote, nid=None):
        hits = [i for i, l in enumerate(self.lines) if quote in l]
        if len(hits) != 1:
            raise Refuse('QUOTE_NOT_ON_EXACTLY_ONE_LINE (%d) in %s: %r' % (len(hits), self.path, quote[:120]))
        i = hits[0]
        if nid is not None and not re.search(r'(?<![0-9A-Za-z])%s(?![0-9])' % re.escape(nid), self.lines[i]):
            raise Refuse('QUOTE_LINE_DOES_NOT_NAME_THE_ID %s in %s line %d' % (nid, self.path, i + 1))
        head = next((self.lines[j] for j in range(i, -1, -1) if self.lines[j].startswith('#')), '(no heading)')
        return i + 1, head.lstrip('#').strip()


def segments(s):
    return [p for p in re.split(r'[…*]', s) if p]


def name_matches(n, a):
    """an IMPL test name against a run test name: exact; or the IMPL's own wildcard (the ellipsis or '*') as written; or, for a
    name with no wildcard, the IMPL's short family name (the run name starts with it plus '_')"""
    if not re.search(r'[…*]', n):
        return a == n or a.startswith(n + '_')
    segs, pos = segments(n), 0
    if not segs:
        return False
    if not re.match(r'[…*]', n):
        if not a.startswith(segs[0]):
            return False
        pos, segs = len(segs[0]), segs[1:]
    for sg in segs:
        j = a.find(sg, pos)
        if j < 0:
            return False
        pos = j + len(sg)
    return True


def load_run(run, compare_sha):
    raw, got = read_pinned(*run)
    d = strict(raw)
    tests = d.get('tests')
    if not (isinstance(tests, list) and d.get('script_sha256') == compare_sha and d.get('n') == d.get('n_pass') == len(tests)
            and d.get('n_fail') == 0 and len({x['test'] for x in tests}) == len(tests)):
        raise Refuse('RUN_OF_RECORD_NOT_A_CLEAN_RUN_OF_THIS_COMPARE %s' % run[0])
    return {'path': run[0], 'sha256': got, 'n': d['n'], 'tests_sha256': d.get('tests_sha256'), 'tests': tests}


def resolve_tests(nid, specs, docs, run):
    """[(name, resolved names, source line text)] after checking each spec; refuses on any unresolved or failing test"""
    out = []
    for src, name in specs:
        if src in IMPL:
            d = docs[src]
            ln = [i + 1 for i, l in enumerate(d.lines) if name in l]
            if not ln:
                raise Refuse('TEST_NAME_NOT_IN_ITS_IMPL %s %r %s' % (nid, name, src))
            where = '%s IMPL line %d' % (src, ln[0])
            hit = [x for x in run['tests'] if name_matches(name, x['test'])]
        elif src == 'RUN_TAG':
            hit = [x for x in run['tests'] if x['test'] == name and any(re.search(r'(?<![0-9A-Za-z])%s(?![0-9])' % re.escape(nid), c)
                                                                         for c in (x.get('covers') or []))]
            where = 'run test tagged %s in its covers (no IMPL prints a test name for this clause)' % nid
        elif src == 'RUN_NAME':
            hit = [x for x in run['tests'] if x['test'] == name]
            where = 'run test the IMPL describes without printing its name'
        else:
            raise Refuse('UNKNOWN_TEST_SOURCE %s' % src)
        if not hit or not all(x.get('pass') is True for x in hit):
            raise Refuse('TEST_DOES_NOT_RESOLVE_TO_PASSING_RUN_TESTS %s %r (%d hits)' % (nid, name, len(hit)))
        out.append((name, [x['test'] for x in hit], where))
    return out


def q(s):
    return '"' + s + '"'


def evidence_text(docs, v005, ev, nid):
    parts = []
    for t in ev:
        src, quote, need_id = t[:3]
        role = ('[%s] ' % t[3]) if len(t) > 3 else ''
        d = v005 if src == 'V005' else docs[src]
        line, head = d.locate(quote, nid if need_id else None)
        if src == 'V005':
            parts.append('%sclosed V005 addendum (read copy %s, sha256 %s), entry %s, line %d: %s'
                         % (role, Path(d.path).name, d.sha, q(head), line, q(quote)))
        else:
            parts.append('%s%s IMPL %s (sha256 %s), section %s, line %d: %s' % (role, src, Path(d.path).name, d.sha, q(head), line, q(quote)))
    return parts


def build(variant, utc, root_rulings, root_ref, require_complete):
    if variant not in VARIANTS:
        raise Refuse('UNKNOWN_VARIANT %r' % variant)
    var = VARIANTS[variant]
    t4_raw, _ = read_pinned(*TOOL4)
    schema = module_string(t4_raw, 'NEW_ITEMS_SCHEMA')
    disp = re.compile(r'(?:%s)' % '|'.join(re.escape(x) for x in ast.literal_eval(
        next(n.value for n in ast.parse(t4_raw.decode('utf-8')).body if isinstance(n, ast.Assign) and len(n.targets) == 1
             and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'NEW_DISPOSITIONS'))))
    docs = {k: Doc(p) for k, p in IMPL.items()}
    v005 = Doc(*V005)
    for src, quote, nid in RULE_TEXTS:
        v005.locate(quote, nid)
    c_raw, c_sha = read_pinned(*var['compare'])
    impl = Doc(*var['impl'])
    if c_sha not in impl.text:
        raise Refuse('COMPARE_IMPL_DOES_NOT_NAME_THE_REVIEWED_SOURCE_SHA_IN_FULL %s' % var['impl'][0])
    if re.search(r'NEW-[0-9]+', impl.text):
        raise Refuse('COMPARE_IMPL_DECLARES_A_NEW_ITEM_ID %s' % var['impl'][0])
    run = load_run(var['run'], c_sha)
    d_raw, _ = read_pinned(*DISCLOSURES)
    c08 = [r['new_item_id'] for r in strict(d_raw)['c08_table']]
    if len(set(c08)) != len(c08):
        raise Refuse('C08_IDS_NOT_UNIQUE')
    d3_raw, _ = read_pinned(*DISCLOSURES_V003_DRAFT)
    c08_v3 = [r['new_item_id'] for r in strict(d3_raw)['c08_table']]
    known = [x['id'] for x in ITEMS] + list(PENDING_ROOT)
    if sorted(known) != sorted(c08) or len(set(known)) != len(known):
        raise Refuse('EVIDENCE_TABLE_IS_NOT_THE_C08_ID_SET')
    for nid, dsp in root_rulings.items():
        if nid not in PENDING_ROOT or not disp.fullmatch(dsp):
            raise Refuse('ROOT_RULING_NOT_FOR_A_PENDING_ID_OR_NOT_A_TOOL4_DISPOSITION %s=%s' % (nid, dsp))
    if root_rulings and not (isinstance(root_ref, str) and root_ref.strip()):
        raise Refuse('ROOT_RULING_REF_REQUIRED')
    by_id = {x['id']: x for x in ITEMS}
    items, pending, summary = [], [], []
    for nid in c08:
        if nid in by_id:
            it = by_id[nid]
            if not disp.fullmatch(it['disposition']):
                raise Refuse('DISPOSITION_NOT_A_TOOL4_VALUE %s' % nid)
            intro = evidence_text(docs, v005, [it['intro']], nid)
            ev = evidence_text(docs, v005, it['evidence'], nid)
            ru = evidence_text(docs, v005, it['rulings'], nid)
            tests = resolve_tests(nid, it['tests'], docs, run)
            dsp, basis = it['disposition'], it['basis']
        elif nid in root_rulings:
            it = PENDING_ROOT[nid]
            intro = evidence_text(docs, v005, [it['intro']], nid)
            ev = evidence_text(docs, v005, it['evidence'], nid)
            ru = ['root ruling supplied: %s' % q(root_ref.strip())]
            dsp, basis = root_rulings[nid], 'ROOT_RULING_SUPPLIED'
            tests = resolve_tests(nid, it['tests'], docs, run) if dsp == 'ADOPTED' else []
        else:
            it = PENDING_ROOT[nid]
            evidence_text(docs, v005, [it['intro']] + it['evidence'], nid)
            resolve_tests(nid, it['tests'], docs, run)
            pending.append(nid)
            continue
        tparts = ['%s -> %d run test(s), all PASS: %s [%s]' % (n, len(r), ', '.join(r[:6]) + (', ...' if len(r) > 6 else ''), w)
                  for n, r, w in tests]
        reason = ('%s %s: %s. Basis: %s. Introduced: %s. %s%sMUST_FAIL tests as named (each resolved in the %s run of record %s, '
                  'sha256 %s, %d/%d PASS, script_sha256 %s): %s.'
                  % (nid, dsp, it['what'], BASIS[basis], intro[0],
                     ('Evidence: ' + ' | '.join(ev) + '. ') if ev else '',
                     ('Root text: ' + ' | '.join(ru) + '. ') if ru else '',
                     variant, run['path'], run['sha256'], run['n'], run['n'], c_sha, '; '.join(tparts) if tparts else 'none (REJECTED)'))
        items.append({'id': nid, 'disposition': dsp, 'reason': reason, 'must_fail_tests': [n for n, _, _ in tests]})
        summary.append((nid, dsp, basis, len(tests)))
    if require_complete and pending:
        raise Refuse('INCOMPLETE: no disposition for %s (root must rule)' % ', '.join(pending))
    me = Path(__file__).resolve()
    note = ('B7 NEW-item disposition list for seal tool 4 (A81 RI-20; V006 A113 P6), variant %s: compare_impl is %s. Id index: the C-08 '
            'table of %s (sha256 %s): %d ids. Written: %d items, in C-08 table order, at most one per id%s. Each reason quotes the round, the '
            'IMPL file and section, the IMPL sha256 from bytes and the line; the closed V005 addendum is read from the byte copy %s '
            '(sha256 %s). must_fail_tests lists the tests exactly as the IMPL names them (its ellipsis or * kept as written); where an '
            'IMPL prints no test name for a clause, the entry is the exact run-of-record test that carries the id in its covers (or the '
            'IMPL describes) and the reason says so. Basis kinds: IMPL_STATED; RI10_FROM_IMPL_DECLARATION (no IMPL writes adopted: the '
            'originating IMPL declares the item stricter and A58 RI-10 / A81 RI-20 adopt it, as root\'s c08_confirmation directs); '
            'ROOT_RULED_ITEM (the item carries out root rulings and a later IMPL records their implementation). The C-08 ids of the '
            'root draft %s (sha256 %s) are %s. Generated by %s (sha256 %s) at %s; tool 4 %s (sha256 %s).'
            % (variant, var['why'], DISCLOSURES[0], DISCLOSURES[1], len(c08), len(items),
               ('; NOT WRITTEN, root must rule: %s (no IMPL states a disposition and RI-10 does not decide them; see the README; '
                'complete with --root-ruling) - this list is INCOMPLETE until root rules' % ', '.join(pending)) if pending else '',
               Path(V005[0]).name, V005[1], Path(DISCLOSURES_V003_DRAFT[0]).name, DISCLOSURES_V003_DRAFT[1],
               'the same ids in the same order' if c08_v3 == c08 else 'DIFFERENT: %s' % c08_v3,
               me.name, sha_bytes(me.read_bytes()), utc, Path(TOOL4[0]).name, TOOL4[1]))
    obj = {'schema': schema, 'compare_impl': {'path': var['impl'][0], 'sha256': impl.sha}, 'items': items, 'note': note}
    text = json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    return obj, text, summary, pending, c08


def main(argv):
    a, i = {'rulings': {}}, 0
    seen = set()
    try:
        while i < len(argv):
            f = argv[i]
            if f in seen and f != '--root-ruling':
                raise Refuse('REPEATED_FLAG %s' % f)
            seen.add(f)
            if f in ('--variant', '--utc', '--write', '--root-ruling-ref'):
                a[f], i = argv[i + 1], i + 2
            elif f == '--root-ruling':
                k, _, v = argv[i + 1].partition('=')
                if k in a['rulings']:
                    raise Refuse('REPEATED_ROOT_RULING %s' % k)
                a['rulings'][k], i = v, i + 2
            elif f in ('--dry-run', '--require-complete'):
                a[f], i = True, i + 1
            else:
                raise Refuse('UNKNOWN_ARGUMENT %r' % f)
        if ('--dry-run' in a) == ('--write' in a) or '--variant' not in a or '--utc' not in a:
            raise Refuse('usage: --variant r13|r14 --utc T [--root-ruling ID=D ... --root-ruling-ref TEXT] [--require-complete] '
                         '(--dry-run | --write PATH)')
        obj, text, summary, pending, c08 = build(a['--variant'], a['--utc'], a['rulings'], a.get('--root-ruling-ref'),
                                                 '--require-complete' in a)
    except (Refuse, OSError, ValueError, KeyError, IndexError, StopIteration) as e:
        print('REFUSED: %s: %s' % (type(e).__name__, e), file=sys.stderr)
        return 2
    sha = sha_bytes(text.encode('utf-8'))
    for row in summary:
        print('ITEM %s %s %s tests=%d' % row)
    print('PENDING_ROOT %s' % (','.join(pending) or 'none'))
    print('C08_IDS %d WRITTEN %d' % (len(c08), len(obj['items'])))
    if '--dry-run' in a:
        print('DRY_RUN_OK variant=%s bytes=%d sha256=%s' % (a['--variant'], len(text.encode('utf-8')), sha))
        return 0
    with open(a['--write'], 'x', encoding='utf-8') as f:
        f.write(text)
    got = sha_bytes(Path(a['--write']).read_bytes())
    print('WROTE %s sha256 %s (expected %s) %s' % (a['--write'], got, sha, 'MATCH' if got == sha else 'MISMATCH'))
    return 0 if got == sha else 3


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
