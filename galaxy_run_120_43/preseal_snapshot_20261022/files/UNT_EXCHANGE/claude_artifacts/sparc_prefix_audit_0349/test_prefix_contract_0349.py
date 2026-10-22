"""0349 adversarial synthetic tests of prefix_contract_checker_0349.py. SYNTHETIC DATA ONLY (no real row is read).

Part A: named fixtures (preserved to a fixtures JSON) with expected status and expected fail codes, run against the
        FULL contract and against ablations that switch single conditions off, to show which condition is load-bearing.
Part B: exhaustive fault-model enumeration (null fields with collapsing writer, merged adjacent fields, blank inside
        the name, same-shape adjacent swaps) over value pools that cover every observed token width; reports how
        many fault patterns each checker variant would PASS while misreading a field.
Usage: python3 -I test_prefix_contract_0349.py <checker_dir> <new_fixtures.json> <new_results.json>
"""
import importlib.util, itertools, json, sys
from collections import Counter

chk_dir, FIX_OUT, RES_OUT = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location('chk', chk_dir.rstrip('/') + '/prefix_contract_checker_0349.py')
chk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chk)

TAIL_FIELDS = [('e_L', 7, '0.123'), ('Reff', 5, '1.23'), ('SBeff', 8, '123.45'), ('Rdisk', 5, '2.34'),
               ('SBdisk', 8, '456.78'), ('MHI', 7, '1.234'), ('RHI', 5, '12.34'), ('Vflat', 5, '99.9'),
               ('e_Vflat', 5, '4.5'), ('Q', 3, '1')]


def tail(sep=' '):
    return ''.join(sep + v.rjust(w) for _, w, v in TAIL_FIELDS) + sep + 'Zz00'.ljust(14)


def hp1(name, T, D, eD, fD, Inc, eInc, L='1.234'):
    """Derived H+1 serialization (header widths, one blank before each field)."""
    return (name.rjust(11) + ' ' + T.rjust(2) + ' ' + D.rjust(6) + ' ' + eD.rjust(5) + ' ' + fD.rjust(2) + ' ' +
            Inc.rjust(4) + ' ' + eInc.rjust(4) + ' ' + L.rjust(7) + tail())


def cds(name, T, D, eD, fD, Inc, eInc, L='1.234'):
    """CDS ReadMe table1.dat serialization (f_Dist I1)."""
    return (name.rjust(11) + ' ' + T.rjust(2) + ' ' + D.rjust(6) + ' ' + eD.rjust(5) + ' ' + fD.rjust(1) + ' ' +
            Inc.rjust(4) + ' ' + eInc.rjust(4) + ' ' + L.rjust(7) + tail())


def hdr(name, T, D, eD, fD, Inc, eInc, L='1.234'):
    """In-file MRT header serialization exactly as written (abutting fields)."""
    return (name.rjust(11) + T.rjust(2) + D.rjust(6) + eD.rjust(5) + fD.rjust(2) + Inc.rjust(4) + eInc.rjust(4) +
            L.rjust(7) + tail(sep=''))


def free(*toks, lead='    ', pad41=True, rest=('0.123', '1.23')):
    """Null-collapsing free-format writer: single blanks, null fields dropped. pad41=True is the attacker's best
    case (the 8th stream token is pushed past byte 41 so byte 41 is blank); pad41=False is a plain free-format row."""
    s = lead + ' '.join(t for t in toks if t)
    return (s.ljust(41) if pad41 else s) + ' ' + ' '.join(rest)


N = 'SYNTH01'
B = dict(T='5', D='42.42', eD='3.33', fD='1', Inc='66.6', eInc='7.7')     # one-digit Type baseline
B2 = dict(T='10', D='7.77', eD='0.88', fD='2', Inc='55.5', eInc='4.4')    # two-digit Type baseline


def row(builder, base, **over):
    d = dict(base); d.update(over)
    L = d.pop('L', '1.234')
    name = d.pop('name', N)
    return builder(name, d['T'], d['D'], d['eD'], d['fD'], d['Inc'], d['eInc'], L=L)


def overwrite(s, pos1, text):
    """Overwrite starting at 1-based byte pos1 (used to build overrun / swapped fixtures exactly)."""
    return s[:pos1 - 1] + text + s[pos1 - 1 + len(text):]


FIX = []


def fx(fid, desc, line, target=N, anchor=None, expect='FAIL', must=(), truth=None, ablate=None):
    FIX.append(dict(id=fid, description=desc, line=line, target=target, anchor=anchor, expect=expect,
                    must_include=list(must), truth=truth, ablation=ablate))


tB = {'Galaxy': N, 'T': '5', 'D': '42.42', 'e_D': '3.33', 'f_D': '1', 'Inc': '66.6', 'e_Inc': '7.7'}
tB2 = {'Galaxy': N, 'T': '10', 'D': '7.77', 'e_D': '0.88', 'f_D': '2', 'Inc': '55.5', 'e_Inc': '4.4'}

# --- baselines and legitimate width variants
fx('F01_baseline_T_one_digit', 'H+1 row, one-digit Type (NGC3198-like class mask)', row(hp1, B), expect='PASS', truth=tB)
fx('F02_baseline_T_two_digit', 'H+1 row, two-digit Type (DDO154-like class mask)', row(hp1, B2), expect='PASS', truth=tB2)
fx('F03_eInc_two_integer_digits', 'e_Inc = 10.0 fills 37-40 (observed 99.9 shape)', row(hp1, B, eInc='10.0'),
   expect='PASS', truth=dict(tB, e_Inc='10.0'))
fx('F04_D_three_integer_digits', 'D = 111.11 fills 16-21 (observed 999.99 shape)', row(hp1, B, D='111.11'),
   expect='PASS', truth=dict(tB, D='111.11'))
fx('F05_Type_zero', 'Type 0 (S0) is a valid Note (1) code', row(hp1, B, T='0'), expect='PASS', truth=dict(tB, T='0'))
# --- decimal precision per field
fx('F06_D_one_decimal', 'D written with 1 decimal', row(hp1, B, D='42.4'), must=['E_SHAPE_D'])
fx('F07_D_three_decimals', 'D written with 3 decimals', row(hp1, B, D='4.242'), must=['E_SHAPE_D'])
fx('F08_eD_three_decimals', 'e_D written with 3 decimals', row(hp1, B, eD='3.333'), must=['E_SHAPE_e_D'])
fx('F09_eD_one_decimal', 'e_D written with 1 decimal', row(hp1, B, eD='3.3'), must=['E_SHAPE_e_D'])
fx('F10_Inc_two_decimals', 'Inc written with 2 decimals (5 chars, overflows F4.1 slot)', row(hp1, B, Inc='66.66'),
   must=['E_SHAPE_Inc'])
fx('F11_Inc_integer', 'Inc written as integer', row(hp1, B, Inc='66'), must=['E_SHAPE_Inc'])
fx('F12_eInc_two_decimals', 'e_Inc written with 2 decimals inside 37-40', row(hp1, B, eInc='7.70'), must=['E_SHAPE_e_Inc'])
fx('F13_T_decimal', 'Type written as 5.0 at 13-15', overwrite(row(hp1, B), 13, '5.0'), must=['E_SHAPE_T'])
fx('F14_eD_negative', 'e_D with a sign', row(hp1, B, eD='-3.33'), must=['E_SHAPE_e_D'])
fx('F15_D_exponent', 'D in exponent notation', row(hp1, B, D='4.2e1'), must=['E_SHAPE_D'])
fx('F59_D_leading_zero', 'D written 07.77 (a fixed-width F writer never pads with zeros; also blocks T+D merges like 0|7.77)',
   row(hp1, B, D='07.77'), must=['E_SHAPE_D'])
fx('F60_Inc_leading_zero', 'Inc written 05.5', row(hp1, B, Inc='05.5'), must=['E_SHAPE_Inc'])
# --- missing field (fixed-column writer leaves blanks)
fx('F16_blank_T_fixed_column', 'Type blank in its fixed slot: 6 tokens', row(hp1, B, T=''), must=['E_TOKEN_COUNT_6'])
fx('F17_blank_D_fixed_column', 'D blank in its slot', row(hp1, B, D=''), must=['E_TOKEN_COUNT_6'])
fx('F18_blank_fD_fixed_column', 'f_D blank in its slot', row(hp1, B, fD=''), must=['E_TOKEN_COUNT_6'])
fx('F19_blank_eInc_fixed_column', 'e_Inc blank in its slot', row(hp1, B, eInc=''), must=['E_TOKEN_COUNT_6'])
# --- missing field (null-collapsing writer: later fields slide left; 8th field L enters bytes 1-41)
fx('F20_missing_T_L_slides_in', 'T null, collapsed; L (F7.3) becomes token 7',
   free(N, '', '42.42', '3.33', '1', '66.6', '7.7', '1.234', lead='    '), must=['E_SHAPE_T'])
fx('F21_missing_D_L_slides_in', 'D null, collapsed', free(N, '5', '', '3.33', '1', '66.6', '7.7', '1.234', lead='    '),
   must=['E_SHAPE_e_D'])
fx('F22_missing_eD_L_slides_in', 'e_D null, collapsed', free(N, '5', '42.42', '', '1', '66.6', '7.7', '1.234', lead='    '),
   must=['E_SHAPE_e_D'])
fx('F23_missing_fD_L_slides_in', 'f_D null, collapsed', free(N, '5', '42.42', '3.33', '', '66.6', '7.7', '1.234', lead='    '),
   must=['E_SHAPE_f_D'])
fx('F24_missing_Inc_L_slides_in', 'Inc null, collapsed: e_Inc lands in Inc slot, L is token 7',
   free(N, '5', '42.42', '3.33', '1', '', '7.7', '1.234', lead='    '), must=['E_SHAPE_e_Inc'])
fx('F25_missing_eInc_L_slides_in', 'e_Inc null, collapsed: L is token 7',
   free(N, '5', '42.42', '3.33', '1', '66.6', '', '1.234', lead='    '), must=['E_SHAPE_e_Inc'])
# --- blank inside the name
fx('F26_blank_in_name_not_located', 'catalogue name SYN TH01 (internal blank); locator asks for SYNTH01',
   row(hp1, B, name='SYN TH01'), must=['E_NAME_MISMATCH', 'E_TOKEN_COUNT_8'])
fx('F27_blank_in_name_target_with_blank', 'target name itself has a blank', row(hp1, B, name='SYN TH01'),
   target='SYN TH01', must=['E_NAME_INTERNAL_BLANK', 'E_TOKEN_COUNT_8'])
fx('F28_blank_in_name_plus_blank_T_compensates', 'name "SYNTH 5" + Type blank: 7 shape-conforming tokens; '
   'T would be read from the name', row(hp1, B, name='SYNTH 5', T=''), target='SYNTH 5',
   must=['E_NAME_INTERNAL_BLANK', 'E_NAME_NOT_CONFINED'], truth=dict(tB, Galaxy='SYNTH 5', T=None),
   ablate=['C1', 'C5', 'C9'])
# --- shifted tokens
fx('F29_row_shifted_right_1', 'whole row shifted one byte right: e_Inc ends at 41', ' ' + row(hp1, B),
   must=['E_BYTE41_NOT_BLANK', 'E_NAME_MISMATCH'])
fx('F30_row_shifted_left_1_smallL', 'whole row shifted one byte left (L<100 so byte 41 stays blank): values intact; '
   'only the observed-ends guard C9 rejects', row(hp1, B)[1:], must=['E_SPAN_ENDS'], truth=tB, ablate=['C9'])
fx('F31_row_shifted_left_1_bigL', 'shifted left with L>=100: L reaches byte 41', row(hp1, B, L='123.456')[1:],
   must=['E_BYTE41_NOT_BLANK'])
fx('F32_tokens_3_7_shifted_right_1', 'fields D..e_Inc one byte right (T separator widened)',
   row(hp1, B)[:14] + ' ' + row(hp1, B)[14:], must=['E_BYTE41_NOT_BLANK'])
# --- token-7 overrun
fx('F33_eInc_overruns_to_41', 'e_Inc 10.5 written at 38-41', overwrite(row(hp1, B), 37, ' 10.5'),
   must=['E_BYTE41_NOT_BLANK'])
fx('F34_eInc_abuts_L', 'e_Inc ends at 40 and a 7-char L starts at 41 (no separator)',
   row(hp1, B)[:40] + '123.456' + row(hp1, B)[48:], must=['E_BYTE41_NOT_BLANK'])
# --- swaps where shapes coincide
fx('F35_D_eD_swapped_no_anchor', 'D and e_D swapped, both in the overlap of the guard ranges, no anchor (DDO154 case)',
   row(hp1, B, D='1.11', eD='5.55'), expect='PASS', truth=dict(tB, D='5.55', e_D='1.11'))
fx('F36_D_eD_swapped_with_anchor', 'same swap, NGC3198 case: anchor = true D', row(hp1, B, D='1.11', eD='5.55'),
   anchor='5.55', must=['E_ANCHOR_T3_NOT_EQUAL', 'E_ANCHOR_OTHER_TOKEN_EQUAL'])
fx('F37_D_eD_swap_outside_overlap', 'D/e_D swap with D>12.8: e_D guard catches', row(hp1, B, D='3.33', eD='42.42'),
   must=['E_RANGE_e_D'])
fx('F38_Inc_eInc_swapped', 'Inc and e_Inc swapped (both F.1): only the disjoint CDS guard ranges catch it',
   row(hp1, B, Inc='7.7', eInc='66.6'), must=['E_RANGE_Inc'], truth=dict(tB, Inc='66.6', e_Inc='7.7'), ablate=['C8'])
fx('F39_anchor_correct', 'anchor equals token 3 only', row(hp1, B), anchor='42.42', expect='PASS', truth=tB)
fx('F40_anchor_equal_text_variant', 'anchor text 42.420 is float-equal', row(hp1, B), anchor='42.420', expect='PASS', truth=tB)
# --- flag domain
fx('F41_fD_6', 'f_D outside 1..5', row(hp1, B, fD='6'), must=['E_SHAPE_f_D'])
fx('F42_fD_0', 'f_D = 0', row(hp1, B, fD='0'), must=['E_SHAPE_f_D'])
fx('F43_fD_two_digit', 'f_D = 12 fills the I2 slot', row(hp1, B, fD='12'), must=['E_SHAPE_f_D'])
fx('F44_fD_leading_zero', 'f_D = 01', row(hp1, B, fD='01'), must=['E_SHAPE_f_D'])
# --- Type ambiguity
fx('F45_T_12', 'Type 12 outside Note (1)', row(hp1, B, T='12'), must=['E_SHAPE_T'])
fx('F46_T_leading_zero', 'Type 05', row(hp1, B, T='05'), must=['E_SHAPE_T'])
fx('F47_T_three_digit_merges_name', 'Type 100 written at 12-14 merges with the name',
   overwrite(row(hp1, B), 12, '100'), must=['E_TOKEN_COUNT_6'])
fx('F48_T_two_digit_abuts_11char_name', '11-char name with Type at 12-13 (header-as-written T slot)',
   'SYNTH012345' + '10' + ' ' + row(hp1, B)[14:], target='SYNTH012345', must=['E_TOKEN_COUNT_6'])
fx('F49_T_one_digit_header_slot', 'one-digit Type at byte 13 (header slot 12-13, right-justified): tokens intact; '
   'only C9 rejects', overwrite(row(hp1, B), 12, ' 5 '), must=['E_SPAN_ENDS'], truth=tB, ablate=['C9'])
# --- whole-row serializations
fx('F50_header_as_written', 'abutting serialization exactly per in-file header', row(hdr, B), must=['E_BYTE41_NOT_BLANK'])
fx('F51_cds_layout_smallL', 'CDS layout (f_Dist I1) with L<100: token mapping correct, only C9 rejects',
   row(cds, B), must=['E_SPAN_ENDS'], truth=tB, ablate=['C9'])
fx('F52_cds_layout_bigL', 'CDS layout with L>=100: L starts at byte 41', row(cds, B, L='123.456'), must=['E_BYTE41_NOT_BLANK'])
fx('F53_free_format_all_present', 'single-blank free format: L and e_L fall inside 1-41',
   free(N, '5', '42.42', '3.33', '1', '66.6', '7.7', '1.234', lead='    ', pad41=False), must=['E_TOKEN_COUNT_8'])
# --- byte hygiene
fx('F54_tab_separator', 'TAB instead of blank before e_Inc', overwrite(row(hp1, B), 36, '\t'), must=['E_NON_PRINTABLE'])
fx('F55_cr_in_prefix', 'CR inside the prefix', overwrite(row(hp1, B), 36, '\r'), must=['E_NON_PRINTABLE'])
fx('F56_short_row', 'row ends at byte 40', row(hp1, B)[:40], must=['E_SHORT_ROW', 'E_BYTE41_NOT_BLANK'])
fx('F57_non_ascii', 'non-ASCII byte in the name field', 'SYNTH01'.rjust(11).replace('S', '§') + row(hp1, B)[11:],
   must=['E_NON_PRINTABLE'])
# --- multi-fault null collapse that is byte-identical in 1-41 to a legitimate row
fx('F58_null_collapse_eVflat_into_eInc_slot', 'e_Inc, L..Vflat null; collapsing writer right-justifies e_Vflat into '
   'the e_Inc slot: bytes 1-41 identical to a legitimate row; NO prefix-only check can see it',
   row(hp1, B, eInc='4.5'), expect='PASS', truth=dict(tB, e_Inc=None))


def run_fixture(f, disable=()):
    line = f['line'].encode('latin-1') if any(ord(c) > 127 for c in f['line']) else f['line'].encode('ascii')
    return chk.check_prefix(line, f['target'], anchor_text=f['anchor'], emit_values=True, disable=disable)


def misread(res, truth):
    if res['status'] != 'PASS' or truth is None:
        return None
    return any(truth.get(k) != v for k, v in res['values'].items())


results = []
ok_all = True
for f in FIX:
    r = run_fixture(f)
    passed_expect = (r['status'] == f['expect']) and all(c in r['fail_codes'] for c in f['must_include'])
    row_res = {'id': f['id'], 'expect': f['expect'], 'status': r['status'], 'fail_codes': r['fail_codes'],
               'must_include': f['must_include'], 'as_expected': passed_expect,
               'class_mask_1_41': r['structure']['class_mask_1_41'], 'token_spans': r['structure']['token_spans']}
    if f['truth'] is not None and r['status'] == 'PASS':
        row_res['values_equal_truth'] = not misread(r, f['truth'])
    if f['ablation']:
        a = run_fixture(f, disable=tuple(f['ablation']))
        row_res['ablation'] = {'disabled': f['ablation'], 'status': a['status'], 'fail_codes': a['fail_codes'],
                               'misread_if_passed': misread(a, f['truth'])}
    ok_all &= passed_expect
    results.append(row_res)

# ---------------- Part B: fault-model enumeration ----------------
POOLS = [('T', ['5', '10', '0']), ('D', ['7.77', '42.42', '111.11', '1.11']), ('e_D', ['0.88', '10.50', '5.55']),
         ('f_D', ['3']), ('Inc', ['55.5', '15.0']), ('e_Inc', ['4.4', '10.0']), ('L', ['1.234', '123.456']),
         ('e_L', ['0.123']), ('Reff', ['1.23']), ('SBeff', ['123.45']), ('Rdisk', ['2.34']), ('SBdisk', ['456.78']),
         ('MHI', ['1.234']), ('RHI', ['12.34', '0.00']), ('Vflat', ['99.9', '5.0', '123.4', '0.0']),
         ('e_Vflat', ['4.5', '12.3', '0.0']), ('Q', ['1']), ('Ref', ['Zz00'])]
NAMES = [('SYNTH01', ['SYNTH01']), ('SYNTH 5', ['SYNTH', '5']), ('SYNTH 10', ['SYNTH', '10']), ('SYN TH01', ['SYN', 'TH01'])]
import re as _re
SH = {2: chk.SHAPES['T'], 3: chk.SHAPES['D'], 4: chk.SHAPES['e_D'], 5: chk.SHAPES['f_D'], 6: chk.SHAPES['Inc'],
      7: chk.SHAPES['e_Inc']}
VARIANTS = {
    'FULL_C1_to_C9': (),
    'TOKEN_ONLY_no_C9': ('C9',),
    'TOKEN_ONLY_no_C9_no_guards_C8': ('C9', 'C8'),
    'TOKEN_ONLY_no_C9_naive_name_no_C1_C5': ('C9', 'C1', 'C5'),
    'BARE_SHAPES_no_C1_C5_C8_C9': ('C9', 'C1', 'C5', 'C8'),
}
stats = {v: Counter() for v in VARIANTS}
stats_layout = Counter()
misreads = {v: Counter() for v in VARIANTS}
n_patterns = 0
MAX_MERGES = 2


def evaluate(name_str, toks, faults, truth7):
    """A pattern is CORRECT iff the first 7 stream tokens are, in order, the unsplit name and the single unmerged
    fields T, D, e_D, f_D, Inc, e_Inc (faults on fields >= 8 that do not reach the first 7 tokens are irrelevant).
    Signature of a misread = the field composition of the first 7 tokens."""
    global n_patterns
    n_patterns += 1
    first7 = toks[:7]
    if len(first7) < 7:
        for v in VARIANTS: stats[v]['caught_fewer_than_7_tokens_C4'] += 1
        return
    comp = [c for _, c in first7]
    n_name = 2 if ' ' in name_str else 1
    correct = (n_name == 1 and comp == ['name', 'T', 'D', 'e_D', 'f_D', 'Inc', 'e_Inc'])
    # C6 shapes are on in every variant: evaluate them first, independent of layout
    if not all(_re.fullmatch(SH[pos], first7[pos - 1][0].encode()) for pos in range(2, 8)):
        for v in VARIANTS: stats[v]['caught_by_shape_C6'] += 1
        return
    ftoks = [t for t, _ in first7[n_name:]]
    widths = [2, 6, 5, 2, 4, 4] if n_name == 1 else [6, 5, 2, 4, 4]
    pre = '' if n_name == 1 else '   '   # name split: the Type slot (12-14) is left blank
    if len(ftoks) == len(widths) and all(len(t) <= w for t, w in zip(ftoks, widths)):
        # attacker's best case vs C9: right-justify into the observed slots (ends 14,21,27,30,35,40)
        line = name_str.rjust(11) + pre + ''.join(' ' + t.rjust(w) for t, w in zip(ftoks, widths))
        stats_layout['slot_layout'] += 1
    else:
        line = name_str.rjust(11) + ' ' + ' '.join(ftoks)
        stats_layout['single_blank_layout'] += 1
    if len(line) > 40:
        for v in VARIANTS: stats[v]['shape_ok_but_cannot_fit_bytes_1_40_C3_C4'] += 1
        return
    line = line.ljust(41) + ' 9.999'   # an 8th token after byte 41
    sig = '|'.join(comp) + (' [name has blank]' if n_name == 2 else '')
    for v, dis in VARIANTS.items():
        r = chk.check_prefix(line.encode('ascii'), name_str, emit_values=True, disable=dis)
        if r['status'] != 'PASS':
            stats[v]['caught_by_' + '+'.join(sorted(set(c.rsplit('_', 1)[0] if c.startswith('E_TOKEN') else c
                                                           for c in r['fail_codes'])))] += 1
            continue
        if correct and all(r['values'][k] == truth7[k] for k in chk.FIELDS):
            stats[v]['pass_correct'] += 1
        else:
            stats[v]['PASS_MISREAD'] += 1
            misreads[v][sig] += 1


def dfs(i, toks, faults, truth7, merges, name_str):
    # prune: every completed token at stream position 2..7 must match its shape (C6 is on in every variant)
    k = len(toks) - 1  # index of last (possibly incomplete) token; completed are 0..k-1
    if len(toks) >= 8 or i == len(POOLS):
        evaluate(name_str, toks, faults, truth7)
        return
    fname, pool = POOLS[i]
    # choice 1: null (collapsing writer drops it)
    if len(faults) < 12:
        dfs(i + 1, toks, faults + ['null:' + fname], truth7, merges, name_str)
    for val in pool:
        t7 = dict(truth7)
        if fname in ('T', 'D', 'e_D', 'f_D', 'Inc', 'e_Inc'):
            t7[fname] = val
        # choice 2: new token
        prev_ok = True
        if len(toks) >= 2 and len(toks) <= 7:
            pos = len(toks)          # 1-based position of the token just completed
            prev_ok = bool(_re.fullmatch(SH[pos], toks[-1][0].encode())) if pos >= 2 else True
        if prev_ok:
            dfs(i + 1, toks + [(val, fname)], faults, t7, merges, name_str)
        # choice 3: merge with previous field token (abutting, no separator)
        if merges < MAX_MERGES and toks and toks[-1][1] != 'name':
            nt = toks[:-1] + [(toks[-1][0] + val, toks[-1][1] + '+' + fname)]
            dfs(i + 1, nt, faults + ['merge:' + toks[-1][1].split('+')[-1] + '+' + fname], t7, merges + 1, name_str)


for name_str, ntoks in NAMES:
    base_faults = [] if ' ' not in name_str else ['blank_in_name']
    dfs(0, [(t, 'name') for t in ntoks], base_faults, {'Galaxy': name_str}, 0, name_str)

# same-shape adjacent swaps (all fields present, fixed-column H+1 serialization)
swap_stats = {v: Counter() for v in VARIANTS}
for D, eD, Inc, eInc in itertools.product(['1.11', '7.77', '42.42', '111.11'], ['0.88', '5.55', '10.50'],
                                          ['55.5', '15.0', '89.9'], ['4.4', '10.0', '1.0']):
    for kind in ('swap_D_eD', 'swap_Inc_eInc'):
        args = dict(T='5', D=D, eD=eD, fD='3', Inc=Inc, eInc=eInc)
        if kind == 'swap_D_eD':
            args['D'], args['eD'] = eD, D
        else:
            args['Inc'], args['eInc'] = eInc, Inc
        line = hp1(N, **args)
        for v, dis in VARIANTS.items():
            r = chk.check_prefix(line.encode('ascii'), N, emit_values=True, disable=dis)
            swap_stats[v][kind + (':PASS_MISREAD' if r['status'] == 'PASS' else ':caught')] += 1

summary = {
    'schema': 'CLAUDE2_0349_PREFIX_CONTRACT_TEST_RESULTS_V001',
    'checker_sha256': __import__('hashlib').sha256(open(chk_dir.rstrip('/') + '/prefix_contract_checker_0349.py', 'rb').read()).hexdigest(),
    'part_A_fixtures': {'n': len(FIX), 'all_as_expected': ok_all, 'results': results},
    'part_B_fault_enumeration': {
        'model': 'token stream = name tokens (name may contain one blank) + fields 2..19 in documented order, each '
                 'field present / null (collapsing writer drops it) / merged into the previous field token '
                 '(<= %d merges); first 7 stream tokens laid into bytes 1-40, an 8th token after byte 41; value pools '
                 'cover every observed token width. A PASS is a MISREAD unless no fault was applied and all 7 tokens '
                 'equal the true fields.' % MAX_MERGES,
        'n_patterns': n_patterns,
        'layouts_used': dict(stats_layout),
        'per_variant': {v: {'disabled': list(VARIANTS[v]), 'outcomes': dict(stats[v]),
                            'misread_fault_signatures': dict(misreads[v].most_common())} for v in VARIANTS},
        'same_shape_swaps_fixed_column': {v: dict(swap_stats[v]) for v in VARIANTS},
    },
}
with open(FIX_OUT, 'x') as f:
    json.dump({'schema': 'CLAUDE2_0349_ADVERSARIAL_FIXTURES_V001', 'note': 'synthetic rows only; no real values',
               'fixtures': FIX}, f, indent=1)
with open(RES_OUT, 'x') as f:
    json.dump(summary, f, indent=1)
print(json.dumps({'fixtures': len(FIX), 'all_as_expected': ok_all, 'n_patterns': n_patterns}))
