# c3v003: flags_of resolves the loop forms of add_argument (v003 tool 4 defines eleven flags in a for loop).
# c3v002: var() also finds an assignment after ';' (T1_SHA etc. share the line with T1); c3v001 refused SCRIPT_VAR_MISSING.
# Claude3 (c3v009 pre-stage, item (b1)): check tool 4 v004 against the RUN FORM the script gives it, the minute Claude4's v004 SELECTED
# file lands. Parameterized on that SELECTED file (path + sha + schema); the script under test is ROOT_SEAL_STEPS_c3v019.sh now and
# c3v020 once wired. Everything is read from bytes through the pinned helper's pin() (no-follow walk, one read, sha) and parsed with its
# strict SELECTED parser (_selected_strict); tool sources are parsed with ast (never imported or executed).
#  IMPORTS: tool 4's non-stdlib imports, closed transitively over the runner modules, must EQUAL the script's T4_RUN --module set:
#    a needed module that is not preloaded would be refused by the runner's sibling guard (or fail); a preloaded module that nothing
#    imports means the RUN FORM and the tool disagree. Relative imports, non-constant importlib/__import__ calls and file-location
#    loaders are refused (the runner cannot pin them). Each --module NAME must equal its file's basename.
#  PINS: each T4_RUN module file (from the script's PINS) must be exactly the file the v004 SELECTED file stores for the role whose
#    path has that basename; if v004's file does not name it, the fallback SELECTED (v003 cf7e5b2f) must (role-qualified either way).
#  CLI: every flag the script passes to tool 4 (step 10 build, step 12 --check-admission-config, COV_ARGS) must be an add_argument
#    flag of tool 4, and tool 4 must define both --manual-disclosures and --manual-disclosures-sha256 (A110 / 0646).
# usage: python3 -I -B check_tool4_imports_c3v001.py HELPER=SHA SCRIPT=SHA SELECTED=SHA SCHEMA [FALLBACK_SELECTED=SHA FALLBACK_SCHEMA]
#   (prints one JSON verdict on stdout; exit 0 PASS, 2 REFUSE)
import ast, hashlib, json, os, re, sys, types
def pa(x):
    p, h = x.rsplit('=', 1); return p, h
(HP, HS), (SP, SS), (VP, VS) = pa(sys.argv[1]), pa(sys.argv[2]), pa(sys.argv[3]); VSCH = sys.argv[4]
FB = (pa(sys.argv[5]), sys.argv[6]) if len(sys.argv) > 6 else None
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; C3 = A + '/seal_assembly_c3'
hb = open(HP, 'rb').read(); assert hashlib.sha256(hb).hexdigest() == HS, 'HELPER_BYTES'
H = types.ModuleType('c3sa_helper_pinned'); H.__file__ = HP; exec(compile(hb, HP, 'exec', dont_inherit=True), H.__dict__)
Refuse = H.Refuse
out = {'check': 'tool4_imports_and_cli_c3v001', 'helper': {'path': HP, 'sha256': HS}, 'script': {'path': SP, 'sha256': SS},
       'selected': {'path': VP, 'sha256': VS, 'schema': VSCH}}
def stdlib(name):
    return name in sys.stdlib_module_names or name in ('__future__',)
def imports_of(src, label):
    """top-level module names imported anywhere in the source (any depth); refuses forms the runner cannot pin"""
    tree = ast.parse(src, label)
    names, dynamic = set(), []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            names.update(a.name.split('.')[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom):
            if n.level:
                dynamic.append('RELATIVE_IMPORT level %d from %r at line %d' % (n.level, n.module, n.lineno))
            elif n.module:
                names.add(n.module.split('.')[0])
        elif isinstance(n, ast.Call):
            f = n.func
            fname = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else '')
            if fname in ('import_module', '__import__'):
                if n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
                    names.add(n.args[0].value.split('.')[0])
                else:
                    dynamic.append('NON_CONSTANT_%s at line %d' % (fname, n.lineno))
            elif fname in ('spec_from_file_location', 'SourceFileLoader', 'module_from_spec', 'exec_module', 'load_module'):
                dynamic.append('FILE_LOCATION_LOADER %s at line %d' % (fname, n.lineno))
    return names, dynamic
def flags_of(src, label):
    """c3v003: the add_argument option strings, including the loop forms tool 4 uses: for flag in ('--a', ...): p.add_argument(flag)
    and for name in ('a', ...): p.add_argument('--' + name). Any other non-constant first argument is reported as unresolved."""
    tree = ast.parse(src, label); fl = set(); unresolved = []
    def const_strs(node):
        if isinstance(node, (ast.Tuple, ast.List)) and node.elts and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
            return [e.value for e in node.elts]
        return None
    loops = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.For) and isinstance(n.target, ast.Name):
            vals = const_strs(n.iter)
            if vals is not None:
                for m in ast.walk(n):
                    if isinstance(m, ast.Call) and isinstance(m.func, ast.Attribute) and m.func.attr == 'add_argument':
                        loops.setdefault(id(m), []).append((n.target.id, vals))
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'add_argument' and n.args):
            continue
        a0 = n.args[0]
        if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
            fl.update(a.value for a in n.args if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value.startswith('--'))
            continue
        done = False
        for var, vals in loops.get(id(n), []):
            if isinstance(a0, ast.Name) and a0.id == var:
                fl.update(v for v in vals if v.startswith('--')); done = True
            elif (isinstance(a0, ast.BinOp) and isinstance(a0.op, ast.Add) and isinstance(a0.left, ast.Constant) and a0.left.value == '--'
                  and isinstance(a0.right, ast.Name) and a0.right.id == var):
                fl.update('--' + v for v in vals); done = True
        if not done:
            unresolved.append(n.lineno)
    return fl, unresolved
try:
    st = open(SP, 'rb').read()
    if hashlib.sha256(st).hexdigest() != SS:
        raise Refuse('SCRIPT_BYTES_MISMATCH')
    st = st.decode('utf-8')
    def var(name):
        m = re.search(r'(?:^|;\s*)%s="([^"]*)"' % re.escape(name), st, re.M)   # c3v002: also NAME_SHA after a ';' on the PINS line
        if not m:
            raise Refuse('SCRIPT_VAR_MISSING %s' % name)
        v = m.group(1)
        for k, val in (('$TD', var('TD') if name != 'TD' else None), ('$A', A), ('$C3', C3)):
            if val is not None and k in v:
                v = v.replace(k, val)
        return v
    m = re.search(r'^RUN_MODS_COMMON=\((.*)\)$', st, re.M); t4 = re.search(r'^T4_RUN=\((.*)\)$', st, re.M)
    if not (m and t4):
        raise Refuse('SCRIPT_RUN_FORM_NOT_FOUND')
    t4_line = t4.group(1).replace('"${RUN_MODS_COMMON[@]}"', m.group(1))
    mods = re.findall(r'--module "([A-Za-z_][A-Za-z0-9_]*)=\$([A-Z0-9_]+)=\$([A-Z0-9_]+)"', t4_line)
    mainm = re.search(r'--main "\$([A-Z0-9_]+)=\$([A-Z0-9_]+)"', t4_line)
    if not mods or not mainm:
        raise Refuse('SCRIPT_T4_RUN_FORM %r' % t4_line[:200])
    runner_mods = {n: (var(pv), var(hv)) for n, pv, hv in mods}
    if len(runner_mods) != len(mods):
        raise Refuse('SCRIPT_T4_RUN_DUPLICATE_MODULE')
    out['t4_run_modules'] = {n: {'path_var': pv, 'path': runner_mods[n][0], 'sha256': runner_mods[n][1]} for n, pv, hv in mods}
    out['t4_run_main_var'] = mainm.group(1)
    for n, (p, h) in runner_mods.items():
        if os.path.basename(p) != n + '.py':
            raise Refuse('RUN_MODULE_NAME_NOT_ITS_FILE %s -> %s' % (n, os.path.basename(p)))
    # the v004 SELECTED file (strict, read once) and, optionally, the fallback (v003)
    sel = H._selected_strict(H.pin(VP, VS, 'v004_selected'))
    if sel.get('schema') != VSCH:
        raise Refuse('V004_SELECTED_SCHEMA %r (want %r)' % (sel.get('schema'), VSCH))
    files = sel.get('files')
    if not isinstance(files, dict) or 'tool_4_build_seal_record' not in files:
        raise Refuse('V004_SELECTED_HAS_NO_tool_4_build_seal_record')
    def entry(fs, role):
        e = fs[role]
        if not (isinstance(e, dict) and set(e) == {'path', 'sha256'} and isinstance(e['path'], str) and e['path'].startswith('/')
                and isinstance(e['sha256'], str) and H.HEX64.fullmatch(e['sha256'])):
            raise Refuse('SELECTED_ENTRY_FORM %s' % role)
        return e['path'], e['sha256']
    t4p, t4h = entry(files, 'tool_4_build_seal_record')
    out['tool_4'] = {'path': t4p, 'sha256': t4h}
    fbfiles = None
    if FB:
        (fp, fh), fsch = FB
        fsel = H._selected_strict(H.pin(fp, fh, 'fallback_selected'))
        if fsel.get('schema') != fsch:
            raise Refuse('FALLBACK_SELECTED_SCHEMA %r' % fsel.get('schema'))
        fbfiles = fsel.get('files') or {}
        out['fallback_selected'] = {'path': fp, 'sha256': fh, 'schema': fsch}
    # PINS: each runner module file is exactly what a SELECTED file stores for the role with that basename
    pin_src = {}
    for n, (p, h) in runner_mods.items():
        hit = [(r, entry(files, r)) for r in files if isinstance(files[r], dict) and os.path.basename(str(files[r].get('path'))) == n + '.py']
        src = 'v004_selected'
        if not hit and fbfiles is not None:
            hit = [(r, entry(fbfiles, r)) for r in fbfiles if isinstance(fbfiles[r], dict) and os.path.basename(str(fbfiles[r].get('path'))) == n + '.py']
            src = 'fallback_selected'
        if len(hit) != 1:
            raise Refuse('RUN_MODULE_NOT_IN_A_SELECTED_FILE %s (%d roles)' % (n, len(hit)))
        role, (sp_, sh_) = hit[0]
        if (sp_, sh_) != (p, h):
            raise Refuse('RUN_MODULE_PIN_NOT_THE_SELECTED_FILE %s: script %s %s, %s role %s %s %s' % (n, p, h[:12], src, role, sp_, sh_[:12]))
        pin_src[n] = {'role': role, 'selected': src}
    out['t4_run_module_pins'] = pin_src
    # IMPORTS (transitive over the runner modules)
    srcs = {'__tool4__': H.pin(t4p, t4h, 'tool_4').decode('utf-8')}
    for n, (p, h) in runner_mods.items():
        srcs[n] = H.pin(p, h, n).decode('utf-8')
    need, seen, dyn, per = set(), set(), [], {}
    todo = ['__tool4__']
    while todo:
        k = todo.pop()
        if k in seen:
            continue
        seen.add(k)
        names, d = imports_of(srcs[k], k)
        dyn += ['%s: %s' % (k, x) for x in d]
        ext = sorted(x for x in names if not stdlib(x) and x != k)
        per[k] = ext
        for x in ext:
            need.add(x)
            if x in srcs:
                todo.append(x)
    out['imports_non_stdlib'] = per
    missing = sorted(need - set(runner_mods)); extra = sorted(set(runner_mods) - need)
    out['missing_from_t4_run'] = missing; out['extra_in_t4_run'] = extra; out['unpinnable_import_forms'] = dyn
    if dyn:
        raise Refuse('UNPINNABLE_IMPORT_FORMS %r' % dyn[:5])
    if missing or extra:
        raise Refuse('T4_IMPORTS_NOT_EQUAL_TO_T4_RUN missing %r extra %r' % (missing, extra))
    # CLI: the flags the script passes to tool 4 must all be tool 4 flags; both A110 flags must exist
    t4flags, unres = flags_of(srcs['__tool4__'], '__tool4__')
    calls = re.findall(r'"\$\{T4_RUN\[@\]\}"((?:[^\n]*\\\n)*[^\n]*)', st)
    passed = set()
    for c in calls:
        passed.update(re.findall(r'(?<![\w-])(--[a-z][a-z0-9-]*)', c))
    cov = re.search(r'^\s*COV_ARGS=\((.*)\)', st, re.M)
    if cov:
        passed.update(re.findall(r'(--[a-z][a-z0-9-]*)', cov.group(1)))
    passed.discard('--')
    out['cli'] = {'tool4_flags': sorted(t4flags), 'flags_the_script_passes': sorted(passed), 'not_accepted': sorted(passed - t4flags),
                  'a110_flags_defined': sorted({'--manual-disclosures', '--manual-disclosures-sha256'} & t4flags), 'unresolved_add_argument_lines': unres}
    if passed - t4flags:
        raise Refuse('SCRIPT_PASSES_FLAGS_TOOL4_DOES_NOT_DEFINE %r%s' % (sorted(passed - t4flags), (' (unresolved add_argument at lines %r)' % unres) if unres else ''))
    if not {'--manual-disclosures', '--manual-disclosures-sha256'} <= t4flags:
        raise Refuse('TOOL4_LACKS_THE_A110_FLAGS (has %r)' % sorted({'--manual-disclosures', '--manual-disclosures-sha256'} & t4flags))
    out['verdict'] = 'PASS'; rc = 0
except Refuse as e:
    out['verdict'] = 'REFUSE'; out['code'] = str(e)[:600]; rc = 2
print(json.dumps(out, indent=1, sort_keys=True))
sys.exit(rc)
