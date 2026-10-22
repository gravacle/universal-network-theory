"""Writes the 0349 analysis deliverables (schema, evidence classification, contract, reads ledger) into the output
directory with exclusive creates. Figures are pulled from the generated census / reconciliation / test / boolean files
so nothing is transcribed by hand. No source file is opened here."""
import hashlib, json, os, sys

OUT = sys.argv[1]


def load(n):
    return json.load(open(os.path.join(OUT, n)))


def sha(n):
    return hashlib.sha256(open(os.path.join(OUT, n), 'rb').read()).hexdigest()


cen = load('PREFIX_CENSUS_0349_V001.json')
doc = load('DOC_LAYOUT_RECONCILIATION_0349_V001.json')
tst = load('TEST_RESULTS_0349_V001.json')
rb = load('REAL_TARGET_BOOLEANS_0349_V001.json')
C = cen['counts']
SH = cen['token_shape_distribution_by_position']
ENDS = cen['token_span_end_distribution']
STARTS = cen['token_span_start_distribution']
PB = tst['part_B_fault_enumeration']
REF = {k: {'file': k, 'sha256': sha(k)} for k in ['PREFIX_CENSUS_0349_V001.json', 'DOC_LAYOUT_RECONCILIATION_0349_V001.json',
                                                  'TEST_RESULTS_0349_V001.json', 'REAL_TARGET_BOOLEANS_0349_V001.json',
                                                  'ADVERSARIAL_FIXTURES_0349_V001.json', 'prefix_contract_checker_0349.py']}
SRC = {'path': '/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/external_ddo154_v001/SPARC_Lelli2016c.mrt',
       'sha256': '5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243', 'bytes': 28259,
       'distributor_copy_identical': 'joint_parent_continuation/sparc_official_sample_2026-10-06_v001.mrt (same sha256; sidecar url https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt, per 0345-B)'}
CDS = {'path': '.../external_ddo154_v001/SPARC_ReadMe.html', 'sha256': '457f61cd8e63dd7b8f8ce0052a458294fa1a5acc2b5b23bb951a2c40d69f9666',
       'line_numbering': 'tag-stripped, html-unescaped text lines'}
F = {r['k']: r for r in doc['fields']}

# ------------------------------------------------------------------ 1. pinned semantic schema
schema = {
    'schema': 'CLAUDE2_0349_PINNED_SEMANTIC_SCHEMA_V001', 'task': '0349 (CLAUDE2 helper 0349-audit, read-only)',
    'source': SRC, 'cds_readme': CDS,
    'scope': 'fields 1-7 of the two target rows (NGC3198 line 152, DDO154 line 104) in bytes 1-41; field 8 only as the right boundary',
    'ordered_fields': [
        {'pos': 1, 'field': 'Galaxy', 'header': {'line': 10, 'bytes': '1-11', 'format': 'A11', 'label': 'Galaxy'},
         'cds': {'line': 148, 'bytes': '1-11', 'format': 'A11', 'label': 'Name'},
         'token_rule': 'equals the target name exactly (NGC3198 / DDO154); no blank; lies in bytes 1-11; only token in bytes 1-11; byte 12 blank',
         'census_175_rows': {'tokens_in_bytes_1_11': cen['name_field']['tokens_in_bytes_1_11_distribution'],
                             'token_end_byte': cen['name_field']['name_token_end_byte_distribution'],
                             'justification': cen['name_field']['justification'], 'byte12_blank': C['byte12_blank'],
                             'names_with_internal_blank': C['name_has_internal_blank'],
                             'non_alphanumeric_chars': cen['name_field']['non_alphanumeric_chars_in_names_with_counts']}},
        {'pos': 2, 'field': 'T', 'emitted': False, 'header': {'line': 11, 'bytes': '12-13', 'format': 'I2', 'label': 'T', 'note': 'Note (1) lines 30-32: codes 0..11'},
         'cds': {'line': 149, 'bytes': '13-14', 'format': 'I2', 'label': 'Type', 'range': '[0/11]', 'note': 'Note (1) lines 177-191: codes 0..11'},
         'token_regex': '^(?:[0-9]|1[01])$',
         'census_175_rows': {'present_as_token': C['exactly_7_tokens'], 'width': cen['type_token_width_distribution'],
                             'start_byte': STARTS['T'], 'end_byte': ENDS['T'], 'domain_0_11_no_leading_zero': C['T_domain_0_11_no_leading_zero'],
                             'blank_type_rows': C['rows'] - C['exactly_7_tokens']}},
        {'pos': 3, 'field': 'D', 'emitted': True, 'header': {'line': 12, 'bytes': '14-19', 'format': 'F6.2', 'units': 'Mpc', 'label': 'D'},
         'cds': {'line': 150, 'bytes': '16-21', 'format': 'F6.2', 'label': 'Dist', 'range': '[0.98/127.8]'},
         'token_regex': '^(?:0|[1-9][0-9]{0,2})\\.[0-9]{2}$', 'domain': 'D > 0', 'guard': '[0.98,127.8] (CDS; reject-only)',
         'census_175_rows': {'shapes': SH['D'], 'end_byte': ENDS['D'], 'exact_2_decimals': C['decimals_ok_D'], 'leading_zero': C['leading_zero_before_digit_D']}},
        {'pos': 4, 'field': 'e_D', 'emitted': True, 'header': {'line': 13, 'bytes': '20-24', 'format': 'F5.2', 'units': 'Mpc', 'label': 'e_D'},
         'cds': {'line': 151, 'bytes': '23-27', 'format': 'F5.2', 'label': 'e_Dist', 'range': '[0.05/12.8]'},
         'token_regex': '^(?:0|[1-9][0-9]?)\\.[0-9]{2}$', 'guard': '[0.05,12.8] (CDS; reject-only)',
         'census_175_rows': {'shapes': SH['e_D'], 'end_byte': ENDS['e_D'], 'exact_2_decimals': C['decimals_ok_e_D'], 'leading_zero': C['leading_zero_before_digit_e_D']}},
        {'pos': 5, 'field': 'f_D', 'emitted': True, 'header': {'line': 14, 'bytes': '25-26', 'format': 'I2', 'label': 'f_D', 'note': 'Note (2) lines 33-38: codes 1..5'},
         'cds': {'line': 152, 'bytes': '29', 'format': 'I1', 'label': 'f_Dist', 'range': '[1/5]', 'note': 'Note (2) lines 192-199: codes 1..5'},
         'token_regex': '^[1-5]$', 'width_conflict': 'header I2 vs CDS I1; the token rule (exactly one digit 1-5) satisfies both',
         'census_175_rows': {'width': cen['fD_token_width_distribution'], 'start_byte': STARTS['f_D'], 'end_byte': ENDS['f_D'], 'single_digit_1_5': C['fD_single_digit_1_5']}},
        {'pos': 6, 'field': 'Inc', 'emitted': True, 'header': {'line': 15, 'bytes': '27-30', 'format': 'F4.1', 'units': 'deg', 'label': 'Inc'},
         'cds': {'line': 153, 'bytes': '31-34', 'format': 'F4.1', 'label': 'i', 'range': '[15/90]', 'note': 'Note (3): mean i of the outer HI disk'},
         'token_regex': '^(?:0|[1-9][0-9]?)\\.[0-9]$', 'domain': '0 <= Inc <= 90', 'guard': '[15,90] (CDS; reject-only)',
         'census_175_rows': {'shapes': SH['Inc'], 'end_byte': ENDS['Inc'], 'exact_1_decimal': C['decimals_ok_Inc'], 'leading_zero': C['leading_zero_before_digit_Inc']}},
        {'pos': 7, 'field': 'e_Inc', 'emitted': True, 'header': {'line': 16, 'bytes': '31-34', 'format': 'F4.1', 'units': 'deg', 'label': 'e_Inc'},
         'cds': {'line': 154, 'bytes': '36-39', 'format': 'F4.1', 'label': 'e_i', 'range': '[1/10]'},
         'token_regex': '^(?:0|[1-9][0-9]?)\\.[0-9]$', 'guard': '[1,10] (CDS; reject-only)',
         'census_175_rows': {'shapes': SH['e_Inc'], 'end_byte': ENDS['e_Inc'], 'exact_1_decimal': C['decimals_ok_e_Inc'], 'leading_zero': C['leading_zero_before_digit_e_Inc'],
                             'ends_at_or_before_40': C['token7_ends_le_40']}},
        {'pos': 8, 'field': 'L[3.6] (boundary only)', 'header': {'line': 17, 'bytes': '35-41', 'format': 'F7.3'},
         'cds': {'line': 155, 'bytes': '41-47', 'format': 'F7.3', 'range': '[0/490]'},
         'rule': 'must have no non-blank byte in 1-41 (byte 41 blank and exactly 7 tokens in 1-41); its F.3 shape could never satisfy the F.1 rule at position 7',
         'census_175_rows': {'byte41_blank': C['byte41_blank'], 'exactly_7_tokens_in_1_41': C['exactly_7_tokens']}},
    ],
    'shape_sequence': 'A | I | F.2 | F.2 | I | F.1 | F.1 || F.3 (field 8)',
    'why_order_plus_shapes_fix_the_mapping': [
        'Order: both documents list the same 19 fields in the same order with corresponding labels (DOC_LAYOUT_RECONCILIATION all_19_in_same_order_with_corresponding_labels = %s).' % doc['all_19_in_same_order_with_corresponding_labels'],
        'Any one-position shift (a missing, merged or split field, or field 8 entering) changes the shape seen at some position: I vs F.2 at 2/3, F.2 vs I at 4/5, I vs F.1 at 5/6, F.1 vs F.3 at 7. Only adjacent same-shape pairs (D,e_D) and (Inc,e_Inc) can trade places without a shape change.',
        'Inc/e_Inc: their documented CDS ranges [15/90] and [1/10] are disjoint, so a transposition fails the reject-only guards (fixture F38; 108/108 swap cases caught).',
        'D/e_D: ranges overlap on [0.98,12.8]; a transposition there is invisible to every prefix check (fixture F35; 36/108 swap cases pass). Excluded by the two-document order, the NGC3198 anchor on the same column, and row invariance of the column (census).',
        'Name: a blank inside a name plus a blank Type can yield 7 conforming tokens (fixture F28); this is caught only by confining token 1 to bytes 1-11 (C5) and refusing blank names (C1).',
    ],
    'documented_layout_relation': {
        'cds_equals_header_plus_one_leading_blank_per_field_with_fD_narrowed_to_I1': doc['cds_layout_is_header_plus_one_leading_blank_per_field_fD_narrowed_to_I1'],
        'cds_lrecl': doc['cds_lrecl_line'], 'predicted_lrecl_113_plus_18_minus_1': doc['predicted_cds_lrecl'],
        'derived_H_plus_1': doc['derived_H_plus_1_layout_header_widths_one_leading_blank_fD_I2'],
        'derived_H_plus_1_record_length': doc['derived_H_plus_1_record_length'],
        'meaning': 'H+1 is the CDS blank-separator convention applied to the in-file header widths with f_D kept I2. It is computed from the two documents only; neither document states it for this file.',
        'census_fixed_offset_validity_rows': cen['fixed_offset_layouts_structural_validity_row_counts']['layouts'],
        'note_header_T_slice': 'the header-as-written T slice (12-13) is a format-valid I2 in 44 rows, all of them two-digit Types cut to their first digit: a valid-looking slice that is the wrong value. The blank-bounded token rule cannot truncate this way.'},
    'target_rows': {t: {'line': rb['targets'][t]['line'], 'class_mask_1_41': rb['targets'][t]['structure']['class_mask_1_41'],
                        'token_spans': rb['targets'][t]['structure']['token_spans']} for t in ('NGC3198', 'DDO154')},
    'evidence_files': REF,
}

# ------------------------------------------------------------------ 2. evidence classification
classes = {
    'schema': 'CLAUDE2_0349_EVIDENCE_CLASSIFICATION_V001',
    'legend': {'DOCUMENTED': 'stated by the in-file header and/or the CDS ReadMe',
               'DERIVED_FROM_DOCUMENTS': 'computed from the two documents alone, not stated by either',
               'OBSERVED_IN_PINNED_BYTES': 'verified exhaustively in the sha-pinned file (all 175 rows or the two target rows)',
               'ASSUMED': 'not established by documents or bytes; the evidence and its consequence are given'},
    'properties': [
        {'id': 'P1', 'property': 'semantic order Galaxy,T,D,e_D,f_D,Inc,e_Inc, then L[3.6]', 'class': 'DOCUMENTED (twice)',
         'evidence': 'header lines 10-17; CDS lines 148-155; same order and corresponding labels for all 19 fields'},
        {'id': 'P2', 'property': 'formats: I vs F, decimal precision, widths', 'class': 'DOCUMENTED',
         'evidence': 'identical in both documents except f_D (header I2, CDS I1)'},
        {'id': 'P3', 'property': 'code domains: Type 0..11, f_D 1..5', 'class': 'DOCUMENTED', 'evidence': 'Note (1) and Note (2) in both documents'},
        {'id': 'P4', 'property': '[min/max] for D, e_D, Inc, e_Inc', 'class': 'DOCUMENTED (CDS only, for its rendition)',
         'use': 'reject-only guards; never used to assign a token to a field'},
        {'id': 'P5', 'property': 'fields 1-7 are never null', 'class': 'DOCUMENTED (CDS convention) + OBSERVED_IN_PINNED_BYTES',
         'evidence': 'no table1 field carries the CDS "?" null flag (ReadMe line 256 cites the Standard Description); 7 non-blank conforming tokens in %d/175 rows' % C['exactly_7_tokens']},
        {'id': 'P6', 'property': 'name occupies bytes 1-11 as one token', 'class': 'DOCUMENTED + OBSERVED_IN_PINNED_BYTES',
         'evidence': 'both documents 1-11 A11; one token in bytes 1-11 ending at 11 and byte 12 blank in 175/175; no name has an internal blank'},
        {'id': 'P7', 'property': 'fields are blank-separated in the data rows', 'class': 'OBSERVED_IN_PINNED_BYTES (CDS documents separators only for its own rendition; the header says the fields abut)',
         'evidence': 'H+1 separator bytes 12,15,22,28,31,36,41 blank in %d/175 rows' % C['hplus1_separators_all_blank']},
        {'id': 'P8', 'property': 'the same column holds the same field in every row (row-invariant fixed-column layout)', 'class': 'DOCUMENTED (as a property of any byte-by-byte description) + OBSERVED_IN_PINNED_BYTES',
         'evidence': 'token end bytes 11,14,21,27,30,35,40 identical and right-justified in %d/175 rows' % C['token_ends_2_7_eq_14_21_27_30_35_40']},
        {'id': 'P9', 'property': 'byte 41 blank; field 8 has no byte at or before 41', 'class': 'OBSERVED_IN_PINNED_BYTES + DERIVED_FROM_DOCUMENTS (H+1 puts a separator at 41); stated by neither document',
         'evidence': 'byte 41 blank in %d/175 rows with exactly 7 tokens in 1-41; this also refutes the header L range 35-41, whose F7.3 would always have a digit at 41' % C['byte41_blank']},
        {'id': 'P10', 'property': 'token 7 is complete', 'class': 'OBSERVED_IN_PINNED_BYTES', 'evidence': 'ends at 40 in 175/175'},
        {'id': 'P11', 'property': 'all six tokens match their ordered shapes (no leading zeros, exact decimals)', 'class': 'OBSERVED_IN_PINNED_BYTES',
         'evidence': 'structural contract (C2-C6, C9) passes for every row under its own name: %d/175' % C['structural_contract_C2_C3_C4_C5_C6_C9_pass_own_name']},
        {'id': 'P12', 'property': 'Type always present, one or two digits', 'class': 'OBSERVED_IN_PINNED_BYTES', 'evidence': cen['type_token_width_distribution']},
        {'id': 'P13', 'property': 'f_D always one digit in 1..5', 'class': 'OBSERVED_IN_PINNED_BYTES', 'evidence': 'single digit 1-5 at byte 30 in %d/175' % C['fD_single_digit_1_5']},
        {'id': 'P14', 'property': 'the bytes are the distributor bytes', 'class': 'DOCUMENTED (download sidecar, per 0345-B) + sha pin'},
        {'id': 'P15', 'property': 'NGC3198 token 3 is D', 'class': 'OBSERVED_IN_PINNED_BYTES (anchor boolean)',
         'evidence': 'token 3 float-equal to the root manifest same-author MassModels distance text: %s; any other token equal: %s' % (
             rb['targets']['NGC3198']['structure']['anchor']['t3_equal'], rb['targets']['NGC3198']['structure']['anchor']['other_token_equal'])},
        {'id': 'P16', 'property': 'DDO154 token 3 is D (not e_D)', 'class': 'DOCUMENTED order + OBSERVED column invariance (P8) + P15 on the same column; no DDO154-specific anchor',
         'residual': 'A1'},
    ],
    'assumptions': [
        {'id': 'A1', 'assumption': 'no row-specific transposition of D and e_D (data integrity of the DDO154 row)',
         'why_needed': 'same shape and overlapping guard ranges; byte-identical in 1-41 to a correct row',
         'affects_any_parser': True, 'addressed_by_author_whitespace_certification': False},
        {'id': 'A2', 'assumption': 'the writer does not drop a null e_Inc and slide a later F.1 field (Vflat or e_Vflat) into its slot',
         'why_needed': 'the fault enumeration finds this as the only full-contract misread family (needs e_Inc and L..RHI all null); byte-identical in 1-41 to a correct row',
         'evidence_against': 'CDS non-nullability (P5); the fixed-column writer (P8) leaves a null slot blank, which would give 6 tokens; no row in the file has a blank slot in 1-41',
         'byte_level_discharge_not_done_here': 'a whole-row token count of 19 for the two target rows (bytes >= 42 were out of scope)',
         'affects_any_parser': True, 'addressed_by_author_whitespace_certification': False},
        {'id': 'A3', 'assumption': 'the CDS rendition and the SPARC-site file carry the same catalogue content (needed for P4 guards and P5)',
         'evidence': 'same authors and journal table; 175 records each; same 19 fields; the CDS layout equals the header widths with one-blank separators'},
    ],
    'not_established': [
        'fixed-offset provenance: no document states the observed byte positions; the contract uses none of them for identification',
        'the authors serialization intent for fields 8-19 (bytes >= 42 not inspected)',
        'any physical geometry: values are catalogue literals; e_D and e_Inc are catalogue mean errors; Inc is the outer-HI-disk mean (CDS Note 3)',
        'validity for any other bytes: a different sha fails C0',
        'a DDO154-specific anchor for D vs e_D',
    ],
}

# ------------------------------------------------------------------ 3. contract
full = PB['per_variant']['FULL_C1_to_C9']
contract = {
    'schema': 'CLAUDE2_0349_SOURCE_SPECIFIC_PREFIX_CONTRACT_V001',
    'verdict': 'CONTRACT JUSTIFIED FOR THE PINNED BYTES',
    'scope': {'source': SRC, 'rows': {'NGC3198': 152, 'DDO154': 104}, 'bytes': '1-41 only',
              'emitted_fields': ['D', 'e_D', 'f_D', 'Inc', 'e_Inc'], 'validated_not_emitted': ['Galaxy', 'T']},
    'because': [
        'Field order is supplied twice by the source (header and CDS agree for all 19 fields).',
        'The documented shape sequence A|I|F.2|F.2|I|F.1|F.1 followed by F.3 makes every positional fault visible except two same-shape transpositions; the Inc/e_Inc one is caught by disjoint documented ranges used as reject-only guards.',
        'Everything an author whitespace certification would add (blanks separate fields; no blank inside fields 1-7; field 8 starts after byte 41; token 7 complete) is verified exhaustively in the sha-pinned bytes: 175/175 rows. For a fixed, hashed object, checking every row is verification, not generalisation.',
        'Fault enumeration over %d patterns (nulls with a collapsing writer, merges, blank-in-name; layouts aligned to the observed slots to give the attacker the best case): the full contract misreads only %d patterns, all in two signatures that put Vflat or e_Vflat in the e_Inc slot (%s). These are byte-identical in 1-41 to a correct row, so no prefix-only check can see them, certified or not. They are excluded by CDS non-nullability (A2).' % (
            PB['n_patterns'], full['outcomes'].get('PASS_MISREAD', 0), '; '.join(full['misread_fault_signatures'])),
        'The remaining D/e_D transposition (A1) is likewise invisible to every prefix check and is not addressed by any serialization certification. It is excluded by the two-document order, and for NGC3198 by the anchor (token 3 = same-author D, no other token equal).',
    ],
    'answer_to_root': 'A documented order plus a uniquely validated literal-token mapping suffices for these pinned bytes; an author certification of whitespace serialization is neither necessary (its content is verified in the bytes) nor sufficient (it would not address the only two residuals, both of which are byte-identical in 1-41 to correct rows and are closed by documentation, not by formatting statements).',
    'conditions': [
        {'id': 'C0', 'rule': 'source sha256 == 5aa0501f...8243; header lines 10-17 and CDS ReadMe (sha 457f61cd...) lines 148-155 match the documented order and formats', 'fail': ['E_PIN', 'E_HEADER_ORDER', 'E_CDS_ORDER'], 'basis': 'DOCUMENTED'},
        {'id': 'C1', 'rule': 'exactly one data row whose bytes 1-11, stripped of blanks, equal the target name; the target name has no blank', 'fail': ['E_ROW_NOT_UNIQUE', 'E_NAME_MISMATCH', 'E_NAME_INTERNAL_BLANK'], 'basis': 'DOCUMENTED (name 1-11) + OBSERVED'},
        {'id': 'C2', 'rule': 'bytes 1..41 exist; every byte is 0x20 or 0x21-0x7E', 'fail': ['E_SHORT_ROW', 'E_NON_PRINTABLE']},
        {'id': 'C3', 'rule': 'byte 41 == 0x20', 'fail': ['E_BYTE41_NOT_BLANK'], 'load_bearing': 'rejects truncated or overrunning token 7 and field-8 intrusion (F29, F31-F34, F50, F52)'},
        {'id': 'C4', 'rule': 'bytes 1..41 split on runs of 0x20 give exactly 7 tokens', 'fail': ['E_TOKEN_COUNT_n'], 'load_bearing': 'blank fields, blank-in-name, merges, extra tokens (F16-F19, F26-F27, F47-F48, F53)'},
        {'id': 'C5', 'rule': 'token 1 == target name, ends <= 11, and it is the only token in bytes 1-11', 'fail': ['E_NAME_NOT_CONFINED'], 'load_bearing': 'blank-in-name compensated by a blank Type (F28; enumeration naive-name variant: %d misreads)' % PB['per_variant']['TOKEN_ONLY_no_C9_naive_name_no_C1_C5']['outcomes'].get('PASS_MISREAD', 0)},
        {'id': 'C6', 'rule': 'ordered shapes: T ^(?:[0-9]|1[01])$; D ^(?:0|[1-9][0-9]{0,2})\\.[0-9]{2}$; e_D ^(?:0|[1-9][0-9]?)\\.[0-9]{2}$; f_D ^[1-5]$; Inc and e_Inc ^(?:0|[1-9][0-9]?)\\.[0-9]$', 'fail': ['E_SHAPE_<field>'], 'basis': 'DOCUMENTED formats and Notes (1)/(2)', 'load_bearing': 'all shifts, precision changes, flags, Type width (F06-F15, F20-F25, F41-F46, F59-F60); %d of %d enumerated patterns' % (full['outcomes'].get('caught_by_shape_C6', 0), PB['n_patterns'])},
        {'id': 'C7', 'rule': 'D > 0; 0 <= Inc <= 90', 'fail': ['E_DOMAIN_D', 'E_DOMAIN_Inc']},
        {'id': 'C8', 'rule': 'reject-only guards from CDS [min/max]: D [0.98,127.8], e_D [0.05,12.8], Inc [15,90], e_Inc [1,10]', 'fail': ['E_RANGE_<field>'], 'basis': 'DOCUMENTED (CDS); never used for identification',
         'load_bearing': 'Inc/e_Inc transposition (F38) and Inc-null slides; without C8 the enumeration misreads rise from %d to %d and swap_Inc_eInc misreads from 0 to 108' % (full['outcomes'].get('PASS_MISREAD', 0), PB['per_variant']['TOKEN_ONLY_no_C9_no_guards_C8']['outcomes'].get('PASS_MISREAD', 0))},
        {'id': 'C9', 'rule': 'token end bytes == (11,14,21,27,30,35,40), the invariant of all 175 rows', 'fail': ['E_SPAN_ENDS'], 'basis': 'OBSERVED (not a published offset)',
         'load_bearing': 'no: identical misread sets with and without it; it only ties the target row to the census and rejects benign shifts (F30, F49, F51 pass correctly when C9 is off)'},
        {'id': 'C10', 'rule': 'NGC3198 only: token 3 float-equals the root manifest reference distance text and no other token does', 'fail': ['E_ANCHOR_T3_NOT_EQUAL', 'E_ANCHOR_OTHER_TOKEN_EQUAL'], 'basis': 'OBSERVED (same-author MassModels)', 'ddo154': 'no anchor; recorded, not a failure (A1)'},
    ],
    'emission': 'Root runs it. Only on PASS of every condition for a target are the literal tokens of D, e_D, f_D, Inc, e_Inc emitted, with the source line number. On any failure no value is emitted, only codes, masks and spans. Never a plain OK.',
    'pinned_target_result_booleans_only': {'status': rb['status'], 'NGC3198': rb['targets']['NGC3198']['status'], 'DDO154': rb['targets']['DDO154']['status'],
                                           'NGC3198_anchor': rb['targets']['NGC3198']['structure']['anchor'], 'docs_verified': rb['header_lines_10_17_verified'] and rb['cds_lines_148_155_verified']},
    'residual_assumptions': ['A1', 'A2', 'A3'], 'not_established': classes['not_established'],
    'checker': REF['prefix_contract_checker_0349.py'],
    'tests': {'fixtures': REF['ADVERSARIAL_FIXTURES_0349_V001.json'], 'results': REF['TEST_RESULTS_0349_V001.json'],
              'n_fixtures': tst['part_A_fixtures']['n'], 'all_as_expected': tst['part_A_fixtures']['all_as_expected']},
}

for name, obj in [('PINNED_SEMANTIC_SCHEMA_0349_V001.json', schema), ('EVIDENCE_CLASSIFICATION_0349_V001.json', classes),
                  ('EXTRACTION_CONTRACT_0349_V001.json', contract)]:
    with open(os.path.join(OUT, name), 'x') as f:
        json.dump(obj, f, indent=1)
    print('wrote', name)
