# Claude4 seal tools v004 REFUTE stage (C4V004R; A110, dispatch 0646): static checks from bytes, run inside tools/run_fenced_c4st2.py.
#  S1  the five unchanged files and the fence/runner in seal_tools_v004 are v003's bytes (sha and byte equality);
#  S2  tool 4 v004 against v003 by AST: every v003 top-level statement, after the two Checker-name renames, against its v004 counterpart;
#      the v004-only statements; the statement-level diff of every changed function (ast.unparse), so "only the new input" is shown, not asserted;
#  S3  E_R6_1: one module-level assignment, a literal, equal to basis.erratum_E_R6_1 of SELECTED_R6_C4V001 (strict parse, sha-pinned) and to
#      e_r6_1_text of root's file b9db6fd1; used in the comparison of manual_disclosures_form_codes, never reassigned;
#  S4  read once: manual_disclosures_codes reads the file once and hashes and parses the same bytes; manual_disclosures_record re-reads once;
#      in build() the check precedes T3.run and the re-read follows later_entry_dispositions and precedes the record;
#  S5  root's file: strict parse, exact key set, keys sorted at every object (0647), the row forms, ASCII, no trailing newline.
# It writes one JSON result, by exclusive create, under probes/run_<UTC>/. Reads only otherwise.
import ast, difflib, hashlib, json, os, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CA = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
V3 = CA / 'v007_final_prereg_c4/seal_tools_v003'
V4 = CA / 'v007_final_prereg_c4/seal_tools_v004'
R6_SELECTED = CA / 'v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json'
ROOT_MD = CA / 'seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json'
PINS = {
    V3 / 'SELECTED_SEAL_TOOLS_V003_C4V001.json': 'cf7e5b2f1b3daf55c485ada1c869bc7249040a8db8202eb1b1a90bebe1431305',
    V3 / 'seal_common_c4v003.py': '101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21',
    V3 / 'check_frozen_addendum_c4v003.py': 'a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4',
    V3 / 'check_sealed_compare_c4v003.py': 'c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1',
    V3 / 'check_slot_fill_c4v003.py': '316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af',
    V3 / 'build_seal_record_c4v003.py': 'de0ceb15ebfb95e04227730bd2785eb46af8cb5980012de91de98f34ea226b96',
    V3 / 'print_driver_build_record_c4v003.py': 'e5bedffe3c91650d5dba7fbd1ed5476e228158679d8959dfea0e2eff436ebdea',
    V3 / 'tests/test_seal_tools_c4v003.py': '67dd8a0085436639ef85650ca966b6b9ae045cc9413f01fc943b7003f142099a',
    V3 / 'tools/fence_c4v002.py': 'c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5',
    V3 / 'tools/run_fenced_c4st2.py': 'fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25',
    V4 / 'build_seal_record_c4v004.py': '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41',
    V4 / 'tests/test_seal_tools_c4v004.py': 'ee237685e24d6efd799f441a4e7340009e1bc65064f86b62d5be6071dfa417e8',
    R6_SELECTED: '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0',
    ROOT_MD: 'b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6',
}
SAME = ('seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py', 'check_slot_fill_c4v003.py',
        'print_driver_build_record_c4v003.py', 'tools/fence_c4v002.py', 'tools/run_fenced_c4st2.py')
RENAMES = {'build_seal_record_c4v003': 'build_seal_record_c4v004', 'check_admission_config_c4v003': 'check_admission_config_c4v004'}


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Dup(ValueError):
    pass


def pairs_strict(ps):
    out = {}
    for k, v in ps:
        if k in out:
            raise Dup(k)
        out[k] = v
    return out


def no_const(c):
    raise ValueError('non-finite ' + c)


def strict(raw):
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs_strict, parse_constant=no_const)


class Rename(ast.NodeTransformer):
    def visit_Constant(self, node):
        if isinstance(node.value, str) and node.value in RENAMES:
            return ast.copy_location(ast.Constant(RENAMES[node.value]), node)
        return node


def top_key(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return 'def ' + node.name
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        return 'assign ' + node.targets[0].id
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return 'import ' + ast.unparse(node)
    return 'stmt ' + ast.unparse(node)[:80]


def main():
    out = {'stage': 'refute', 'probe': 'refute_static_c4v004r.py', 'probe_sha256': sha(Path(__file__).read_bytes()),
           'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'checks': []}

    def check(name, ok, detail=None):
        out['checks'].append({'check': name, 'ok': bool(ok), 'detail': detail})
    # S0 pins from bytes
    got = {str(p): sha(p.read_bytes()) for p in PINS}
    check('S0 every base pin hashes to the brief\'s sha (v003 SELECTED, six v003 sources, v003 tests, fence, runner, tool 4 v004, the v004 '
          'suite, r6 SELECTED, root\'s file)', all(got[str(p)] == h for p, h in PINS.items()),
          {str(p): got[str(p)] for p, h in PINS.items() if got[str(p)] != h})
    # S1 the unchanged files
    s1 = {n: ((V3 / n).read_bytes() == (V4 / n).read_bytes(), sha((V4 / n).read_bytes())) for n in SAME}
    check('S1 seal_common, tools 1, 2, 3 and 5, the fence and the runner in seal_tools_v004 are byte-equal to v003\'s', all(v[0] for v in s1.values()),
          {n: v[1] for n, v in s1.items()})
    top4 = sorted(p.name for p in V4.glob('*.py'))
    check('S1 the top-level tool set of v004 is exactly the five v003 names plus build_seal_record_c4v004.py (no v003 tool 4 beside it)',
          top4 == sorted(['build_seal_record_c4v004.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py', 'check_slot_fill_c4v003.py',
                          'print_driver_build_record_c4v003.py', 'seal_common_c4v003.py']), top4)
    # S2 AST comparison of tool 4
    src3 = (V3 / 'build_seal_record_c4v003.py').read_bytes().decode('utf-8')
    src4 = (V4 / 'build_seal_record_c4v004.py').read_bytes().decode('utf-8')
    t3 = Rename().visit(ast.parse(src3))
    t4 = ast.parse(src4)
    m3 = {top_key(n): n for n in t3.body}
    m4 = {top_key(n): n for n in t4.body}
    same, changed, only3, only4 = [], {}, [], []
    for k, n in m3.items():
        if k not in m4:
            only3.append(k)
        elif ast.dump(n) == ast.dump(m4[k]):
            same.append(k)
        else:
            a = ast.unparse(n).splitlines()
            b = ast.unparse(m4[k]).splitlines()
            changed[k] = [ln for ln in difflib.unified_diff(a, b, 'v003 (renamed)', 'v004', n=0, lineterm='') if not ln.startswith(('---', '+++'))]
    only4 = [k for k in m4 if k not in m3]
    out['s2_tool4_ast'] = {'v003_statements': len(m3), 'v004_statements': len(m4), 'identical_after_renames': len(same), 'changed': changed,
                           'only_in_v003': only3, 'only_in_v004': only4}
    expect_changed = {'assign SCHEMA', 'def build', 'def main'}
    expect_new = {'assign MANUAL_DISCLOSURES_SCHEMA', 'assign MANUAL_DISCLOSURES_KEYS', 'assign C08_ROW_KEYS', 'assign C08_ID_RX',
                  'assign ROOT_DISCLOSURE_KEYS', 'assign E_R6_1', 'def strings_of', 'def has_utf8_form', 'def manual_disclosures_form_codes',
                  'def manual_disclosures_codes', 'def manual_disclosures_record'}
    check('S2 tool 4: after the renames build_seal_record_c4v003 -> c4v004 and check_admission_config_c4v003 -> c4v004 (Checker and refusal names), '
          'every v003 top-level statement is AST-identical in v004 except SCHEMA, build() and main(); none is removed; the v004-only statements '
          'are the five new constants, E_R6_1 and the five new functions', set(changed) == expect_changed and not only3 and set(only4) == expect_new,
          {'changed': sorted(changed), 'only_in_v003': only3, 'only_in_v004': only4})
    # the exact content of the changes in build() and main(): statement-level opcodes on the function bodies (ast.dump equality)
    def body_ops(k):
        b3, b4 = m3[k].body, m4[k].body
        d3, d4 = [ast.dump(s) for s in b3], [ast.dump(s) for s in b4]
        ops = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, d3, d4, autojunk=False).get_opcodes():
            if tag != 'equal':
                ops.append({'op': tag, 'v003': [ast.unparse(s)[:200] for s in b3[i1:i2]], 'v004': [ast.unparse(s)[:200] for s in b4[j1:j2]],
                            'v003_nodes': b3[i1:i2], 'v004_nodes': b4[j1:j2]})
        return ops
    bops, mops = body_ops('def build'), body_ops('def main')
    out['s2_build_ops'] = [{k: v for k, v in o.items() if not k.endswith('_nodes')} for o in bops]
    out['s2_main_ops'] = [{k: v for k, v in o.items() if not k.endswith('_nodes')} for o in mops]
    ins = [s for o in bops for s in o['v004']]
    dele = [s for o in bops for s in o['v003']]
    rec_pair = [(o['v003_nodes'][0], o['v004_nodes'][0]) for o in bops if o['op'] == 'replace' and len(o['v003_nodes']) == 1 and len(o['v004_nodes']) == 1
                and ast.unparse(o['v003_nodes'][0]).startswith('rec = {')]
    dict_ok, dict_detail = False, None
    if len(rec_pair) == 1:
        d3n, d4n = rec_pair[0][0].value, rec_pair[0][1].value
        k3 = [ast.unparse(k) if k is not None else '**' for k in d3n.keys]
        k4 = [ast.unparse(k) if k is not None else '**' for k in d4n.keys]
        v3d = {k: ast.dump(v) for k, v in zip(k3, d3n.values)}
        v4d = {k: ast.dump(v) for k, v in zip(k4, d4n.values)}
        extra = [k for k in k4 if k not in k3]
        dict_ok = (extra == ["'manual_disclosures'"] and [k for k in k4 if k != "'manual_disclosures'"] == k3 and all(v3d[k] == v4d[k] for k in k3)
                   and ast.unparse(d4n.values[k4.index("'manual_disclosures'")]) == 'mdr' and k4.index("'manual_disclosures'") == k4.index("'disclosures'") + 1)
        dict_detail = {'extra_keys': extra, 'position_after': k4[k4.index("'manual_disclosures'") - 1] if "'manual_disclosures'" in k4 else None}
    want_ins = ["chk = C.Checker('build_seal_record_c4v004')", "md = manual_disclosures_codes(chk, getattr(a, 'manual_disclosures', None))",
                'mdr = manual_disclosures_record(chk, md)']
    other_ins = [s for s in ins if not s.startswith('rec = {') and s not in want_ins]
    other_del = [s for s in dele if not s.startswith('rec = {') and s != "chk = C.Checker('build_seal_record_c4v004')"]
    check('S2 build(): besides the record dict, the only inserted statements are the Checker (moved before T3.run), the manual disclosures check and '
          'its re-read, and the only deleted statement is the Checker at its old place; the record dict is v003\'s with exactly one key added, '
          '\'manual_disclosures\': mdr, right after \'disclosures\', every other key and value AST-identical',
          sorted(set(want_ins)) == sorted(set(s for s in ins if not s.startswith('rec = {'))) and not other_ins and not other_del and dict_ok,
          {'inserted': ins, 'deleted': dele, 'dict': dict_detail})
    m_ins = [s for o in mops for s in o['v004']]
    m_del = [s for o in mops for s in o['v003']]
    check('S2 main(): the only change is three inserted statements, the two new flags and the API pin built from them; nothing deleted or replaced',
          all(o['op'] == 'insert' for o in mops) and not m_del and len(m_ins) == 3
          and "p.add_argument('--manual-disclosures')" in m_ins and "p.add_argument('--manual-disclosures-sha256')" in m_ins
          and any(s.startswith('a.manual_disclosures = None if a.manual_disclosures is None and a.manual_disclosures_sha256 is None else') for s in m_ins),
          {'inserted': m_ins, 'deleted': m_del})
    s3, s4 = [n for n in t3.body if top_key(n) == 'assign SCHEMA'], [n for n in t4.body if top_key(n) == 'assign SCHEMA']
    check('S2 SCHEMA: UNT_V007_SEAL_RECORD_C4V003 -> UNT_V007_SEAL_RECORD_C4V004 (a change beyond the new input; disclosed as B-N1)',
          ast.literal_eval(s3[0].value) == 'UNT_V007_SEAL_RECORD_C4V003' and ast.literal_eval(s4[0].value) == 'UNT_V007_SEAL_RECORD_C4V004',
          [ast.literal_eval(s3[0].value), ast.literal_eval(s4[0].value)])
    # S3 E_R6_1
    assigns = [n for n in ast.walk(t4) if isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign))
               and any(isinstance(t, ast.Name) and t.id == 'E_R6_1' for t in (n.targets if isinstance(n, ast.Assign) else [n.target]))]
    glob = [n for n in ast.walk(t4) if isinstance(n, (ast.Global, ast.Nonlocal)) and 'E_R6_1' in n.names]
    e_const = ast.literal_eval(assigns[0].value) if len(assigns) == 1 else None
    sel_raw = R6_SELECTED.read_bytes()
    sel = strict(sel_raw)
    e_sel = sel['basis']['erratum_E_R6_1']
    root_raw = ROOT_MD.read_bytes()
    root = strict(root_raw)
    check('S3 E_R6_1 has exactly one assignment (module level, a literal) and no global/nonlocal rebinding',
          len(assigns) == 1 and assigns[0] in t4.body and isinstance(e_const, str) and not glob, len(assigns))
    check('S3 E_R6_1 == SELECTED_R6_C4V001 basis.erratum_E_R6_1 (strict parse, 7200acd9), byte for byte as UTF-8', e_const == e_sel
          and e_const.encode('utf-8') == e_sel.encode('utf-8'), {'len_const': len(e_const or ''), 'len_selected': len(e_sel),
                                                               'sha_const': sha((e_const or '').encode('utf-8')), 'sha_selected': sha(e_sel.encode('utf-8'))})
    check('S3 E_R6_1: 469 characters, ASCII, UTF-8 sha256 c28202b0909371f43180ca832e4652f3d835a977852cde5c261842315deb33f4 (the README\'s figures)',
          len(e_const) == 469 and e_const.isascii() and sha(e_const.encode('utf-8')) == 'c28202b0909371f43180ca832e4652f3d835a977852cde5c261842315deb33f4',
          {'len': len(e_const), 'ascii': e_const.isascii(), 'sha': sha(e_const.encode('utf-8'))})
    check('S3 root\'s file e_r6_1_text == E_R6_1', root.get('e_r6_1_text') == e_const, None)
    fc = [n for n in t4.body if isinstance(n, ast.FunctionDef) and n.name == 'manual_disclosures_form_codes'][0]
    cmp_ok = any(isinstance(n, ast.Compare) and isinstance(n.left, ast.Name) and n.left.id == 'e' and len(n.ops) == 1 and isinstance(n.ops[0], ast.NotEq)
                 and isinstance(n.comparators[0], ast.Name) and n.comparators[0].id == 'E_R6_1' for n in ast.walk(fc))
    norm = [ast.unparse(n) for n in ast.walk(fc) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr in ('normalize', 'casefold', 'lower', 'upper', 'replace', 'translate') and 'e' in ast.unparse(n.func.value)]
    check('S3 manual_disclosures_form_codes compares the parsed e_r6_1_text to E_R6_1 with a plain e != E_R6_1 (no normalize, casefold, strip or '
          'replace on the compared value; strip() is used only for the emptiness test)', cmp_ok and not norm, norm)
    # S4 read once, order in build()
    fcodes = [n for n in t4.body if isinstance(n, ast.FunctionDef) and n.name == 'manual_disclosures_codes'][0]
    frec = [n for n in t4.body if isinstance(n, ast.FunctionDef) and n.name == 'manual_disclosures_record'][0]

    def calls(fn, attr):
        return [n for n in ast.walk(fn) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == attr]
    rb = calls(fcodes, 'read_bytes')
    shab = calls(fcodes, 'sha_bytes')
    sjt = calls(fcodes, 'strict_json_typed')
    check('S4 manual_disclosures_codes: one read_bytes, and sha_bytes and strict_json_typed take the same variable (raw): the hashed bytes are the '
          'parsed bytes', len(rb) == 1 and len(shab) == 1 and len(sjt) == 1 and ast.unparse(shab[0].args[0]) == 'raw' and ast.unparse(sjt[0].args[0]) == 'raw'
          and any(isinstance(n, ast.Assign) and ast.unparse(n) == 'raw = Path(p).read_bytes()' for n in ast.walk(fcodes)),
          [ast.unparse(x) for x in rb + shab + sjt])
    check('S4 manual_disclosures_record: one re-read (read_bytes), compared by sha to the pin; the record keeps the CHECKED text and parse',
          len(calls(frec, 'read_bytes')) == 1 and "return {'pin': {'path': p, 'sha256': h}, 'content': obj, 'raw_text': text}" in ast.unparse(frec)
          and 'p, h, obj, text = md' in ast.unparse(frec), ast.unparse(frec)[-300:])
    fb = [n for n in t4.body if isinstance(n, ast.FunctionDef) and n.name == 'build'][0]
    order = [ast.unparse(s)[:70] for s in fb.body]

    def idx(pfx):
        return next((i for i, s in enumerate(order) if s.startswith(pfx)), -1)
    i_md, i_t3, i_led, i_mdr, i_rec, i_text = (idx('md = manual_disclosures_codes'), idx('res = T3.run'), idx('led = later_entry_dispositions'),
                                               idx('mdr = manual_disclosures_record'), idx('rec = {'), idx('text = json.dumps'))
    check('S4 build(): check before T3.run; re-read after the dispositions re-read and before the record and its serialization; an early return '
          'on any failure follows T3 and the re-read', 0 <= i_md < i_t3 < i_led < i_mdr < i_rec < i_text
          and order[i_t3 + 3].startswith('if chk.failures') and order[i_mdr + 1].startswith('if chk.failures'),
          {'md': i_md, 't3': i_t3, 'led': i_led, 'mdr': i_mdr, 'rec': i_rec, 'text': i_text})
    # S5 root's file
    orders = []

    def pairs_order(ps):
        orders.append([k for k, _ in ps])
        return pairs_strict(ps)
    json.loads(root_raw.decode('utf-8'), object_pairs_hook=pairs_order, parse_constant=no_const)
    rows, rds = root['c08_table'], root['root_disclosures']
    check('S5 root\'s file: strict parse, keys exactly {schema, e_r6_1_text, c08_table, c08_confirmation, root_disclosures}, schema '
          'SEAL_MANUAL_DISCLOSURES_V001, keys sorted in every object (0647), 19 C-08 rows of {declared_in_r13 false, file, line > 0, new_item_id '
          'NEW-n}, 5 root disclosures of {id, source, text}', set(root) == {'schema', 'e_r6_1_text', 'c08_table', 'c08_confirmation', 'root_disclosures'}
          and root['schema'] == 'SEAL_MANUAL_DISCLOSURES_V001' and all(o == sorted(o) for o in orders) and len(rows) == 19
          and all(set(r) == {'declared_in_r13', 'file', 'line', 'new_item_id'} and r['declared_in_r13'] is False and type(r['line']) is int and r['line'] > 0
                  for r in rows) and len({r['new_item_id'] for r in rows}) == 19 and len(rds) == 5
          and [x['id'] for x in rds] == ['A100_B2_SANITY', 'A101_B2_DOC_ERRATUM', 'A105_E_OPS5', 'A107_P12', 'A111_P3_P4']
          and all(set(x) == {'id', 'source', 'text'} for x in rds),
          {'ids': [r['new_item_id'] for r in rows], 'lines': [r['line'] for r in rows], 'unsorted_objects': [o for o in orders if o != sorted(o)]})
    check('S5 root\'s file is ASCII, has no CR and no trailing newline (so raw_text carries no non-ASCII character)', root_raw.isascii()
          and b'\r' not in root_raw and not root_raw.endswith(b'\n'), {'bytes': len(root_raw)})
    # end: the pins again (nothing changed during this run)
    got2 = {str(p): sha(p.read_bytes()) for p in PINS}
    check('S6 at the end every base pin still hashes to its sha (v003, root\'s file, r6 SELECTED, v004 unchanged by this run)', got2 == got
          and all(got2[str(p)] == h for p, h in PINS.items()), None)
    out['passed'] = sum(c['ok'] for c in out['checks'])
    out['total'] = len(out['checks'])
    run = HERE / ('run_' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()))
    run.mkdir()
    with open(run / 'STATIC_C4V004R.json', 'x') as f:
        json.dump(out, f, indent=1)
    for c in out['checks']:
        print('%-6s %s' % ('ok' if c['ok'] else 'NOT_OK', c['check'][:150]))
        if not c['ok']:
            print('       detail:', json.dumps(c['detail'])[:1500])
    print('passed', out['passed'], '/', out['total'], 'written', run / 'STATIC_C4V004R.json')
    print(json.dumps(out['s2_tool4_ast']['changed'], indent=1)[:6000])
    return 0 if out['passed'] == out['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
