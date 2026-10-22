"""0349 INERT source-specific prefix-token contract checker for the sha-pinned SPARC_Lelli2016c.mrt.

Scope: ONLY the two target rows NGC3198 and DDO154; ONLY fields Galaxy, T, D, e_D, f_D, Inc, e_Inc in bytes 1..41.
This is an observed-file extraction rule. It does NOT assert that any published fixed offsets are correct, and it
adopts no physical geometry.

Two entry points:
  check_prefix(line, target, ...)   pure function used by the synthetic tests (may return parsed values when
                                    emit_values=True; synthetic data only).
  check_pinned_targets(anchor_text) real-file mode used by this audit: verifies pins, locates each target row by bytes
                                    1-11, runs check_prefix with emit_values=False, and returns ONLY booleans, class
                                    masks, spans and fail codes. It never returns, prints or stores a parsed value.
Contract conditions (fail-closed codes in brackets):
  C0  file sha256 pin; MRT header lines 10-17 and CDS ReadMe (sha pin) table1 lines 148-155 verified by regex, i.e.
      the documented order Galaxy,T,D,e_D,f_D,Inc,e_Inc followed by L[3.6] F7.3 [E_PIN, E_HEADER_ORDER, E_CDS_ORDER]
  C1  exactly one post-header row whose bytes 1-11, stripped of blanks, equal the target name; the target name
      contains no blank [E_ROW_NOT_UNIQUE, E_NAME_MISMATCH, E_NAME_INTERNAL_BLANK]
  C2  bytes 1..41 exist; every byte is 0x20 or printable ASCII 0x21-0x7E (no TAB/CR/NUL/non-ASCII)
      [E_SHORT_ROW, E_NON_PRINTABLE]
  C3  byte 41 is 0x20 (so token 7 is complete and ends <= 40, and field 8 cannot have a non-blank byte <= 41)
      [E_BYTE41_NOT_BLANK]
  C4  bytes 1..41 split on runs of 0x20 give exactly 7 tokens [E_TOKEN_COUNT]
  C5  token 1 equals the target name, lies inside bytes 1-11, and bytes 1-11 contain no other token
      (byte 12 blank) [E_NAME_NOT_CONFINED]
  C6  ordered token shapes (documented formats + Notes 1/2 code domains):
        T     ^(?:[0-9]|1[01])$                 I2 width, Note (1) codes 0..11, no leading zero
        D     ^(?:0|[1-9][0-9]{0,2})\.[0-9]{2}$ F6.2: unsigned, <=3 integer digits, no leading zero, exactly 2 decimals
        e_D   ^(?:0|[1-9][0-9]?)\.[0-9]{2}$     F5.2: unsigned, <=2 integer digits, no leading zero, exactly 2 decimals
        f_D   ^[1-5]$                           I2 (header) / I1 (CDS) width, Note (2) codes 1..5
        Inc   ^(?:0|[1-9][0-9]?)\.[0-9]$        F4.1: unsigned, <=2 integer digits, no leading zero, exactly 1 decimal
        e_Inc ^(?:0|[1-9][0-9]?)\.[0-9]$        F4.1: same as Inc
      [E_SHAPE_<field>]
  C7  domain: D > 0, Inc <= 90 [E_DOMAIN_<field>]
  C8  CDS documented [min/max] used as fail-closed GUARDS only (never as identification):
        D [0.98,127.8]  e_D [0.05,12.8]  Inc [15,90]  e_Inc [1,10]   [E_RANGE_<field>]
  C9  observed-file consistency guard (NOT a published offset): token end bytes equal the end bytes observed in all
      175 rows of the pinned file: Galaxy 11, T 14, D 21, e_D 27, f_D 30, Inc 35, e_Inc 40  [E_SPAN_ENDS].
      Not load-bearing for identification (the fault enumeration gives identical misread sets with and without it);
      it only ties each target row to the file-wide census and rejects benign layout shifts (fail-closed).
  C10 NGC3198 only: token 3 is float-equal to the root manifest reference distance text and no other token 2..7 is
      [E_ANCHOR_T3_NOT_EQUAL, E_ANCHOR_OTHER_TOKEN_EQUAL]; DDO154: no anchor available (recorded, not a failure).
Usage (real-file boolean mode): python3 -I prefix_contract_checker_0349.py --pinned-booleans <new_output.json>
"""
import hashlib, html, json, re, sys

SRC = ('/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/'
       'joint_parent_continuation/external_ddo154_v001/SPARC_Lelli2016c.mrt',
       '5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243')
CDS_README = ('/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/'
              'joint_parent_continuation/external_ddo154_v001/SPARC_ReadMe.html',
              '457f61cd8e63dd7b8f8ce0052a458294fa1a5acc2b5b23bb951a2c40d69f9666')
MANIFEST = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
            'CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json',
            'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494')
TARGETS = ('NGC3198', 'DDO154')
FIELDS = ('Galaxy', 'T', 'D', 'e_D', 'f_D', 'Inc', 'e_Inc')
SHAPES = {'T': rb'(?:[0-9]|1[01])', 'D': rb'(?:0|[1-9][0-9]{0,2})\.[0-9]{2}', 'e_D': rb'(?:0|[1-9][0-9]?)\.[0-9]{2}',
          'f_D': rb'[1-5]', 'Inc': rb'(?:0|[1-9][0-9]?)\.[0-9]', 'e_Inc': rb'(?:0|[1-9][0-9]?)\.[0-9]'}
GUARDS = {'D': (0.98, 127.8), 'e_D': (0.05, 12.8), 'Inc': (15.0, 90.0), 'e_Inc': (1.0, 10.0)}
OBSERVED_ENDS = (11, 14, 21, 27, 30, 35, 40)
HEADER_LINES = {10: r'^\s+1-\s+11\s+A11\s+---\s+Galaxy\s', 11: r'^\s+12-\s+13\s+I2\s+---\s+T\s',
                12: r'^\s+14-\s+19\s+F6\.2\s+Mpc\s+D\s', 13: r'^\s+20-\s+24\s+F5\.2\s+Mpc\s+e_D\s',
                14: r'^\s+25-\s+26\s+I2\s+---\s+f_D\s', 15: r'^\s+27-\s+30\s+F4\.1\s+deg\s+Inc\s',
                16: r'^\s+31-\s+34\s+F4\.1\s+deg\s+e_Inc\s', 17: r'^\s+35-\s+41\s+F7\.3\s+\S+\s+L\[3\.6\]\s'}
CDS_LINES = {148: r'^\s+1-\s+11\s+A11\s+---\s+Name\s', 149: r'^\s+13-\s+14\s+I2\s+---\s+Type\s+\[0/11\]',
             150: r'^\s+16-\s+21\s+F6\.2\s+Mpc\s+Dist\s+\[0\.98/127\.8\]',
             151: r'^\s+23-\s+27\s+F5\.2\s+Mpc\s+e_Dist\s+\[0\.05/12\.8\]', 152: r'^\s+29\s+I1\s+---\s+f_Dist\s+\[1/5\]',
             153: r'^\s+31-\s+34\s+F4\.1\s+deg\s+i\s+\[15/90\]', 154: r'^\s+36-\s+39\s+F4\.1\s+deg\s+e_i\s+\[1/10\]',
             155: r'^\s+41-\s+47\s+F7\.3\s+\S+\s+L3\.6\s'}
ALL_CONDITIONS = ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10')


def cls_mask(b):
    return ''.join('_' if c == 32 else '9' if 48 <= c <= 57 else '.' if c == 46 else
                   'A' if (65 <= c <= 90 or 97 <= c <= 122) else 'p' if 33 <= c <= 126 else '?' for c in b)


def check_prefix(line, target, anchor_text=None, emit_values=False, disable=()):
    """line: bytes of one row (LF removed). target: expected galaxy name. anchor_text: optional reference D text.
    disable: iterable of condition ids to switch OFF (ablation tests only). Returns a dict."""
    on = lambda c: c not in disable
    fails = []
    tname = target.encode('ascii')
    p = line[:41]
    if on('C1'):
        if b' ' in tname:
            fails.append('E_NAME_INTERNAL_BLANK')
        if p[:11].strip(b' ') != tname:
            fails.append('E_NAME_MISMATCH')
    if on('C2'):
        if len(p) < 41:
            fails.append('E_SHORT_ROW')
        if any(not (c == 32 or 33 <= c <= 126) for c in p):
            fails.append('E_NON_PRINTABLE')
    if on('C3') and not (len(p) == 41 and p[40] == 32):
        fails.append('E_BYTE41_NOT_BLANK')
    spans = [(m.start() + 1, m.end()) for m in re.finditer(rb'[^ ]+', p)]
    toks = [p[a - 1:e] for a, e in spans]
    report = {'class_mask_1_41': cls_mask(p), 'token_spans': [list(s) for s in spans], 'n_tokens': len(spans)}
    if len(toks) != 7:
        if on('C4'):
            fails.append('E_TOKEN_COUNT_%d' % len(toks))
        return _finish(fails, report, None, emit_values)
    t = dict(zip(FIELDS, toks))
    if on('C5'):
        in_1_11 = [s for s in spans if s[0] <= 11]
        if t['Galaxy'] != tname or spans[0][1] > 11 or len(in_1_11) != 1:
            fails.append('E_NAME_NOT_CONFINED')
    elif not re.fullmatch(rb'[A-Za-z0-9+\-.]*[A-Za-z][A-Za-z0-9+\-.]*', t['Galaxy']):
        fails.append('E_SHAPE_Galaxy')  # naive checker still needs an alphanumeric name with a letter
    shape_ok = {}
    for f, rx in SHAPES.items():
        shape_ok[f] = bool(re.fullmatch(rx, t[f]))
        if on('C6') and not shape_ok[f]:
            fails.append('E_SHAPE_' + f)
    report['shape_ok'] = shape_ok
    vals = {}
    for f in ('D', 'e_D', 'Inc', 'e_Inc'):
        if shape_ok[f]:
            vals[f] = float(t[f].decode('ascii'))
    for f in ('T', 'f_D'):
        if shape_ok[f]:
            vals[f] = int(t[f].decode('ascii'))
    if on('C7'):
        if 'D' in vals and not vals['D'] > 0:
            fails.append('E_DOMAIN_D')
        if 'Inc' in vals and not (0 <= vals['Inc'] <= 90):
            fails.append('E_DOMAIN_Inc')
    guard_ok = {}
    for f, (lo, hi) in GUARDS.items():
        guard_ok[f] = (f in vals) and lo <= vals[f] <= hi
        if on('C8') and f in vals and not guard_ok[f]:
            fails.append('E_RANGE_' + f)
    report['guard_ok'] = guard_ok
    ends = tuple(e for a, e in spans)
    report['ends_equal_observed'] = ends == OBSERVED_ENDS
    if on('C9') and ends != OBSERVED_ENDS:
        fails.append('E_SPAN_ENDS')
    if anchor_text is not None:
        a = float(anchor_text)
        eq = {f: (f in vals and float(t[f].decode('ascii')) == a) for f in FIELDS[1:]}
        report['anchor'] = {'t3_equal': eq['D'], 'other_token_equal': any(v for k, v in eq.items() if k != 'D')}
        if on('C10'):
            if not eq['D']:
                fails.append('E_ANCHOR_T3_NOT_EQUAL')
            if report['anchor']['other_token_equal']:
                fails.append('E_ANCHOR_OTHER_TOKEN_EQUAL')
    else:
        report['anchor'] = 'NOT_AVAILABLE'
    out_vals = {k: t[k].decode('ascii', 'replace') for k in FIELDS}  # synthetic mode only
    return _finish(fails, report, out_vals, emit_values)


def _finish(fails, report, vals, emit_values):
    res = {'status': 'PASS' if not fails else 'FAIL', 'fail_codes': fails, 'structure': report}
    if emit_values and not fails:
        res['values'] = vals  # synthetic tests only; check_pinned_targets never sets emit_values
    return res


def _verify_docs(lines):
    hdr_ok = all(re.match(rx, lines[n - 1].decode('ascii', 'replace')) for n, rx in HEADER_LINES.items())
    rb = open(CDS_README[0], 'rb').read()
    cds_pin = hashlib.sha256(rb).hexdigest() == CDS_README[1]
    txt = html.unescape(re.sub(r'<[^>]+>', '', rb.decode('utf-8', 'replace'))).splitlines()
    cds_ok = cds_pin and all(re.match(rx, txt[n - 1]) for n, rx in CDS_LINES.items())
    return hdr_ok, cds_pin, cds_ok


def check_pinned_targets(anchor_text):
    """Real-file mode. Returns booleans/masks/spans/fail codes only; never values."""
    b = open(SRC[0], 'rb').read()
    if hashlib.sha256(b).hexdigest() != SRC[1]:
        return {'status': 'FAIL', 'fail_codes': ['E_PIN']}
    lines = b.split(b'\n')
    del b
    hdr_ok, cds_pin, cds_ok = _verify_docs(lines)
    out = {'pin_ok': True, 'header_lines_10_17_verified': hdr_ok, 'cds_pin_ok': cds_pin,
           'cds_lines_148_155_verified': cds_ok, 'targets': {}}
    seps = [i for i, l in enumerate(lines[:200]) if re.fullmatch(rb'-{20,}', l.strip())]
    first = seps[-1] + 1
    for tgt in TARGETS:
        hits = [(i + 1, l) for i, l in enumerate(lines[first:], first) if l[:11].strip(b' ') == tgt.encode()]
        if len(hits) != 1:
            out['targets'][tgt] = {'status': 'FAIL', 'fail_codes': ['E_ROW_NOT_UNIQUE'], 'occurrences': len(hits)}
            continue
        n, l = hits[0]
        r = check_prefix(l[:41], tgt, anchor_text=anchor_text if tgt == 'NGC3198' else None, emit_values=False)
        assert 'values' not in r
        r['line'] = n
        if not (hdr_ok and cds_ok):
            r['status'] = 'FAIL'
            r['fail_codes'] = r['fail_codes'] + ['E_HEADER_ORDER' if not hdr_ok else 'E_CDS_ORDER']
        out['targets'][tgt] = r
    del lines
    out['status'] = 'PASS' if all(v.get('status') == 'PASS' for v in out['targets'].values()) else 'FAIL'
    return out


def load_anchor_text():
    mb = open(MANIFEST[0], 'rb').read()
    if hashlib.sha256(mb).hexdigest() != MANIFEST[1]:
        raise SystemExit('E_MANIFEST_PIN')
    texts = json.loads(mb)['crosscheck_massmodels']['reference_distance_texts']
    if len(texts) != 1:
        raise SystemExit('E_ANCHOR_NOT_UNIQUE')
    return texts[0]


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--pinned-booleans':
        res = check_pinned_targets(load_anchor_text())
        with open(sys.argv[2], 'x') as f:
            json.dump(res, f, indent=1)
        print(json.dumps({'status': res['status'], 'output': sys.argv[2]}))
    else:
        raise SystemExit('usage: --pinned-booleans <new_output.json>')
