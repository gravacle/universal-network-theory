# Claude4 r6 refute helper (r6_check), checks (3)/(4): r13 and r12 read as TEXT only (never imported or executed; ast.parse
# builds a syntax tree and runs nothing). Verifies the r6 line citations into r13, the five seal-time pin lines, the
# builtin_r5_build text, the r12 -> r13 hunks, and FIELDS_R13 = A102 preamble + FIELDS_R12 bytes.
# Read-only; writes OUT.json by exclusive create.
# usage: python3 -I -B r13lines_r6chk.py R12.py R12_SHA R13.py R13_SHA FIELDS_R12 FIELDS_R13 R6.json OUT.json
import ast, difflib, hashlib, json, re, sys


def read(p, want=None):
    raw = open(p, 'rb').read()
    h = hashlib.sha256(raw).hexdigest()
    if want is not None and h != want:
        raise SystemExit('SHA_MISMATCH %s %s != %s' % (p, h, want))
    return raw, h


def funcs(text):
    t = ast.parse(text)
    out = {}
    for n in t.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.setdefault(n.name, []).append((n.lineno, n.end_lineno, n.decorator_list[0].lineno if n.decorator_list else n.lineno))
    return out


def assigns(text, name):
    t = ast.parse(text)
    hits = []
    for n in t.body:
        if isinstance(n, ast.Assign):
            for tg in n.targets:
                if isinstance(tg, ast.Name) and tg.id == name:
                    hits.append((n.lineno, ast.get_source_segment(text, n)))
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == name:
            hits.append((n.lineno, ast.get_source_segment(text, n)))
    return hits


def main():
    r12p, r12s, r13p, r13s, f12p, f13p, r6p, outp = sys.argv[1:9]
    r12raw, _ = read(r12p, r12s)
    r13raw, _ = read(r13p, r13s)
    t12, t13 = r12raw.decode('utf-8'), r13raw.decode('utf-8')
    L12, L13 = t12.split('\n'), t13.split('\n')
    res = {'r12': {'path': r12p, 'sha256': r12s, 'lines': len(L12)}, 'r13': {'path': r13p, 'sha256': r13s, 'lines': len(L13)}}
    # line citations used by r6
    def line(L, n):
        return L[n - 1] if 0 < n <= len(L) else None
    cites = [
        ('case_block read in sealed mode', 5706, 5708, "get('case_block')"),
        ('GATE_RECORD_SHA_REQUIRED = ()', 338, 338, 'GATE_RECORD_SHA_REQUIRED = ()'),
        ('GATE_RECORD_AFTER_SEAL_ALLOWED', 341, 341, 'GATE_RECORD_AFTER_SEAL_ALLOWED = ('),
    ]
    res['citations'] = []
    for what, n12, n13, needle in cites:
        a, b = line(L12, n12), line(L13, n13)
        res['citations'].append({'what': what, 'r12_line': n12, 'r13_line': n13, 'r12_text': a, 'r13_text': b,
                                 'equal': a == b, 'contains': (needle in (a or '')) and (needle in (b or ''))})
    # the context of the case-block read (a few lines either side) must be equal too
    res['case_block_context_equal'] = L12[5706 - 6:5706 + 5] == L13[5708 - 6:5708 + 5]
    res['case_block_context_r13'] = L13[5708 - 4:5708 + 3]
    # where else does r13 read case_block from the prereg?
    res['r13_case_block_get_lines'] = [i + 1 for i, s in enumerate(L13) if "get('case_block')" in s or 'get("case_block")' in s or "['case_block']" in s]
    # five seal-time pins
    res['pins'] = {}
    for nm in ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005', 'PIN_DRIVER_BUILD_RECORD', 'PIN_V010_R5_CHECK', 'PIN_PRODUCER_REGISTRY'):
        res['pins'][nm] = {'r13': assigns(t13, nm), 'r12': assigns(t12, nm)}
    # builtin_r5_build
    f12, f13 = funcs(t12), funcs(t13)
    b12, b13 = f12.get('builtin_r5_build'), f13.get('builtin_r5_build')
    res['builtin_r5_build'] = {'r12': b12, 'r13': b13}
    if b12 and b13 and len(b12) == 1 and len(b13) == 1:
        s12 = '\n'.join(L12[b12[0][2] - 1:b12[0][1]])
        s13 = '\n'.join(L13[b13[0][2] - 1:b13[0][1]])
        res['builtin_r5_build']['text_equal'] = s12 == s13
        res['builtin_r5_build']['sha256_r13_text'] = hashlib.sha256(s13.encode()).hexdigest()
    # hunks r12 -> r13
    sm = difflib.SequenceMatcher(a=L12, b=L13, autojunk=False)
    ops = [op for op in sm.get_opcodes() if op[0] != 'equal']
    crc = f12.get('check_record_codes')
    crc13 = f13.get('check_record_codes')
    res['check_record_codes'] = {'r12': crc, 'r13': crc13}
    res['hunks'] = []
    for tag, i1, i2, j1, j2 in ops:
        res['hunks'].append({'op': [tag, i1, i2, j1, j2], 'r12_lines': L12[i1:i2], 'r13_lines': L13[j1:j2],
                             'inside_r12_check_record_codes': bool(crc) and crc[0][0] <= i1 + 1 and (i2 if i2 > i1 else i1 + 1) <= crc[0][1]})
    # top-level functions other than check_record_codes: text identical?
    diff_funcs = []
    for name in sorted(set(f12) | set(f13)):
        a, b = f12.get(name), f13.get(name)
        if not a or not b or len(a) != 1 or len(b) != 1:
            diff_funcs.append((name, 'presence/duplicate'))
            continue
        sa = '\n'.join(L12[a[0][2] - 1:a[0][1]])
        sb = '\n'.join(L13[b[0][2] - 1:b[0][1]])
        if sa != sb:
            diff_funcs.append((name, 'text differs'))
    res['top_level_functions_differing'] = diff_funcs
    # FIELDS_R13 = preamble + FIELDS_R12 ?
    f12raw, f12s = read(f12p)
    f13raw, f13s = read(f13p)
    res['fields'] = {'r12_sha256': f12s, 'r13_sha256': f13s, 'r13_endswith_r12_bytes': f13raw.endswith(f12raw),
                     'preamble_lines': f13raw[:len(f13raw) - len(f12raw)].count(b'\n') if f13raw.endswith(f12raw) else None,
                     'doubling_ddo_gas_M_s_in_r12': b'ddo_gas_M_s' in f12raw, 'doubling_ddo_gas_M_s_in_r13': b'ddo_gas_M_s' in f13raw}
    fl13 = f13raw.decode('utf-8').split('\n')
    res['fields']['r13_L113'] = fl13[112] if len(fl13) > 112 else None
    # r6 claims (assembly.r13_line_checks) against these results
    d6 = json.load(open(r6p, 'rb'))
    res['r6_r13_line_checks'] = d6['assembly']['r13_line_checks']
    with open(outp, 'x') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print(json.dumps({'citations': [(c['what'], c['equal'], c['contains']) for c in res['citations']],
                      'case_block_context_equal': res['case_block_context_equal'],
                      'r13_case_block_get_lines': res['r13_case_block_get_lines'],
                      'pins_r13': {k: v['r13'] for k, v in res['pins'].items()},
                      'builtin_r5_build': res['builtin_r5_build'],
                      'check_record_codes': res['check_record_codes'],
                      'hunk_ops': [h['op'] + [h['inside_r12_check_record_codes']] for h in res['hunks']],
                      'top_level_functions_differing': diff_funcs, 'fields': res['fields']}, indent=1))
    for h in res['hunks']:
        print('HUNK', h['op'])
        for s in h['r12_lines']:
            print('  - ' + s)
        for s in h['r13_lines']:
            print('  + ' + s)


if __name__ == '__main__':
    main()
