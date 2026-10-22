# Claude2 h3_campaign_path_c2 (root V006 A188, A191 B2): deterministic generator of the CAMPAIGN adoption cascade, c2v002.
# c2v002 against make_campaign_cascade_c2v001 (65a70144), and nothing else: E2 the entry template is h3_campaign_entry_c2v002
# (A191 B2: its reingest takes the acceptance record); the result names this generator.  Policy, core and wrapper outputs are
# c2v001's, byte for byte, for every SUB and tuple.  Text below is c2v001's (W1, E1, M1 hold with the c2v002 names).
# Minimal successor of Claude4's make_b1_cascade_c4v002 (a7a5fe58, adopted A129; Codex1 0138 PASS).  Every v002 rule is kept:
# the policy is r7 + P1-P4 (+ P5/P6 with a seal tuple), the core is core r9 + C1/C2 (the policy path and sha), the tuple is
# cross-checked against the SEALED compare / prereg / addendum bytes (C, P, A, SCHEMA; V = 64 lowercase hex), SUB is a
# parameter, output is exclusive create, --dry-run writes nothing.  Changes against v002, and nothing else:
#  W1  the wrapper source is the published q5b1 wrapper calibration_orchestrator_cx2v006r10_c4_q5b1.py (7a6af535, V006 A139:
#      A134 Q5 slot rule, b1 guard 9e3fc109), not the R9 wrapper (24abe3bc, whose L74 / L148-161 still require the retired
#      prelaunch LO envelope, A134 Q1/Q5).  W1 replaces the q5b1 core pin (its L27) by the new core's name and sha; the output
#      wrapper is named calibration_orchestrator_cx2<SUB>_q5b1.py; the _resolve_source literal must be unchanged (as v002).
#  E1  a fourth output, the launch entry h3_campaign_entry_cx2<SUB>.py, from the pinned template h3_campaign_entry_c2v001.py
#      (the w1_campaign_entry_v001 successor): exactly its WRAPPER and WRAPPER_SHA lines are rewritten to the wrapper as it
#      will be published, <publish-root>/<SUB>/<wrapper name> (default publish root: calib_tail_readiness_cx2).
#  M1  main(argv) / build(...) are callable in process (regenerate_h3_c2v001.py); the CLI is v002's plus --publish-root.
# Regression: with SUB = v006r10_c4, no tuple and the default publish root the four outputs are byte-identical to the
# published policy 93d9c0ac, core dc895f8a, q5b1 wrapper 7a6af535 and the entry template itself.
# usage: python3 -I -B make_campaign_cascade_c2v002.py OUTDIR SUB (--dry-run | --write) [--publish-root DIR] [--policy-only]
#        [--seal-tuple C P A SCHEMA V]
import ast, hashlib, json, os, re, sys

CX2 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2'
R7 = (CX2 + '/v006r7/adoption_policy_cx2v006r7.py', '7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d')
CORE9 = (CX2 + '/v006r9/calibration_core_cx2v006r9.py', 'a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605')
WRAPQ = (CX2 + '/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py', '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d')
CORE10_SHA = 'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6'     # the core q5b1 L27 pins
ENTRY_T = (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'h3_campaign_entry_c2v002.py'),
           '75b4cafa8563e31879ab1d70a74fe64dba9f4d61f496c3bc28479668c1e61c10')
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
SEALED_COMPARE = CTRL + '/V007_SEAL_ASSEMBLY/kmax_tail_compare_c2v007_r14_cx1v001_SEALED_V007.py'
SEALED_PREREG = CTRL + '/V007_SEAL_ASSEMBLY/KMAX_TAIL_PREREG_V007_SEALED.json'
HEX = re.compile(r'[0-9a-f]{64}')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def refuse(msg):
    sys.stderr.write('REFUSED: ' + msg + '\n')
    sys.stderr.flush()
    raise SystemExit(2)


def pinned(pin):
    raw = open(pin[0], 'rb').read()
    if sha(raw) != pin[1]:
        refuse('%s is not %s' % (pin[0], pin[1]))
    return raw.decode('utf-8')


def rep1(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        refuse('replacement %s matches %d times (must be exactly 1)' % (tag, n))
    return text.replace(old, new)


def names(sub):
    if re.fullmatch(r'v006r[0-9]+_c4', sub) is None:
        refuse('SUB must look like v006rNN_c4: %r' % sub)
    tag = 'cx2' + sub
    return ('adoption_policy_%s.py' % tag, 'calibration_core_%s.py' % tag, 'calibration_orchestrator_%s_q5b1.py' % tag,
            'h3_campaign_entry_%s.py' % tag)


POLICY_REPLACEMENTS = [
    ('P1_docstring',
     '"""0540 F1: inert verification of a sealed V007 ADOPT_TAIL report; never runs the comparator."""\n',
     '"""0540 F1: inert verification of a sealed V007 ADOPT_TAIL report; never runs the comparator.\n'
     'Claude4 B1/R-A2 successor (root A122) of adoption_policy_cx2v006r7.py (7c726fa2): the sealed compare carries\n'
     'PIN_ADDENDUM_V005 as a bare sha256 (r14 L172) and cites the addendum by ADDENDUM_V005_CITED = CTRL + literal (L171);\n'
     'its report writes pins_verified.V005_addendum as that bare sha (L5766). Only those three reads change; every other\n'
     'check is r7\'s, byte for byte."""\n'),
    ('P2_constants_binop',
     '                    try:\n'
     '                        out[target.id] = ast.literal_eval(node.value)\n'
     '                    except (ValueError, TypeError):\n'
     '                        pass\n',
     '                    try:\n'
     '                        out[target.id] = ast.literal_eval(node.value)\n'
     '                    except (ValueError, TypeError):\n'
     '                        # B1: exactly NAME + \'literal\' for an already collected str constant (ADDENDUM_V005_CITED)\n'
     '                        v = node.value\n'
     '                        if (isinstance(v, ast.BinOp) and isinstance(v.op, ast.Add) and isinstance(v.left, ast.Name)\n'
     '                                and isinstance(out.get(v.left.id), str) and isinstance(v.right, ast.Constant)\n'
     '                                and isinstance(v.right.value, str)):\n'
     '                            out[target.id] = out[v.left.id] + v.right.value\n'),
    ('P3_bare_sha_pin',
     "        add=c.get('PIN_ADDENDUM_V005')\n"
     "        if not isinstance(add,(list,tuple)) or len(add)!=2 or not all(isinstance(v,str) for v in add):\n"
     "            raise ValueError('V007_ADDENDUM_EXACT_BYTE_PIN_REQUIRED')\n"
     "        O.read_pinned({'path':add[0],'sha256':add[1]},'sealed V005 addendum')\n"
     "        seal=(cmpref['sha256'],preref['sha256'],add[1],c.get('SCHEMA_REPORT'),art['sha256'])\n",
     "        add=c.get('PIN_ADDENDUM_V005')\n"
     "        if not isinstance(add,str) or len(add)!=64 or any(ch not in '0123456789abcdef' for ch in add):\n"
     "            raise ValueError('V007_ADDENDUM_BARE_SHA_PIN_REQUIRED')\n"
     "        cited=c.get('ADDENDUM_V005_CITED')\n"
     "        if not isinstance(cited,str) or not cited.startswith('/'):\n"
     "            raise ValueError('V007_ADDENDUM_CITED_PATH_REQUIRED')\n"
     "        O.read_pinned({'path':cited,'sha256':add},'sealed V005 addendum')\n"
     "        seal=(cmpref['sha256'],preref['sha256'],add,c.get('SCHEMA_REPORT'),art['sha256'])\n"),
    ('P4_report_pin',
     "        if (rep.get('pins_verified') or {}).get('V005_addendum') not in (list(add),tuple(add)):\n",
     "        if (rep.get('pins_verified') or {}).get('V005_addendum')!=add:\n"),
]


def sealed_constants():
    """The sealed compare's own module-level literals and NAME + literal bindings (as policy r8's constants() reads them)."""
    raw = open(SEALED_COMPARE, 'rb').read()
    out = {}
    for node in ast.parse(raw.decode('utf-8')).body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    try:
                        out[t.id] = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        v = node.value
                        if (isinstance(v, ast.BinOp) and isinstance(v.op, ast.Add) and isinstance(v.left, ast.Name)
                                and isinstance(out.get(v.left.id), str) and isinstance(v.right, ast.Constant)
                                and isinstance(v.right.value, str)):
                            out[t.id] = out[v.left.id] + v.right.value
    return sha(raw), out


def check_tuple(tup):
    c, p, a, schema, v = tup
    for name, x in (('compare', c), ('prereg', p), ('addendum', a), ('verdict', v)):
        if HEX.fullmatch(x) is None:
            refuse('%s sha must be 64 lowercase hex: %r' % (name, x))
    csha, k = sealed_constants()
    if c != csha:
        refuse('C is not the sealed compare (%s)' % csha)
    if p != k.get('V007_PREREG_SHA256') or p != sha(open(SEALED_PREREG, 'rb').read()):
        refuse('P is not the sealed prereg / the compare V007_PREREG_SHA256')
    cited = k.get('ADDENDUM_V005_CITED')
    if a != k.get('PIN_ADDENDUM_V005') or not isinstance(cited, str) or a != sha(open(cited, 'rb').read()):
        refuse('A is not the compare PIN_ADDENDUM_V005 / the cited addendum bytes')
    if schema != k.get('SCHEMA_REPORT'):
        refuse('SCHEMA is not the compare SCHEMA_REPORT (%r)' % k.get('SCHEMA_REPORT'))


def build(sub, policy_only=False, seal_tuple=None, publish_root=CX2):
    """-> (files [(name, bytes)], outputs {name: sha256}, resolve_source_literal_sha256 or None).  Writes nothing."""
    if seal_tuple is not None:
        check_tuple(seal_tuple)
    if not isinstance(publish_root, str) or not os.path.isabs(publish_root):
        refuse('publish root must be an absolute path: %r' % (publish_root,))
    POLICY_NAME, CORE_NAME, WRAP_NAME, ENTRY_NAME = names(sub)
    r7, core9, wrapq = pinned(R7), pinned(CORE9), pinned(WRAPQ)
    pol = r7
    for tag, old, new in POLICY_REPLACEMENTS:
        pol = rep1(pol, old, new, tag)
    if seal_tuple is not None:
        pol = rep1(pol, 'APPROVED_V007_SEALS = frozenset()\n', 'APPROVED_V007_SEALS = frozenset({%r})\n' % (seal_tuple,), 'P5_seal_tuple')
        pol = rep1(pol, '# No final V007 seal has been supplied. A root-reviewed immutable successor\n',
                   '# The V007 seal tuple below was registered at the A126 finalization, after the V007 verdict. A root-reviewed immutable successor\n',
                   'P6_comment')
    ast.parse(pol)
    pol_b = pol.encode('utf-8')
    pol_sha = sha(pol_b)
    outputs = {POLICY_NAME: pol_sha}
    files = [(POLICY_NAME, pol_b)]
    lit_sha = None
    if not policy_only:
        core = rep1(core9, "    p = Path(__file__).resolve().parent.parent/'v006r7/adoption_policy_cx2v006r7.py'\n",
                    "    p = Path(__file__).resolve().parent.parent/'%s/%s'\n" % (sub, POLICY_NAME), 'C1_policy_path')
        core = rep1(core, "    if hashlib.sha256(raw).hexdigest() != '%s':\n" % R7[1],
                    "    if hashlib.sha256(raw).hexdigest() != '%s':\n" % pol_sha, 'C2_policy_sha')
        ast.parse(core)
        core_b = core.encode('utf-8')
        core_sha = sha(core_b)
        wrap = rep1(wrapq, "M=load(HERE/'calibration_core_cx2v006r10_c4.py','_cx2v006r1',expected='%s')\n" % CORE10_SHA,
                    "M=load(HERE/'%s','_cx2v006r1',expected='%s')\n" % (CORE_NAME, core_sha), 'W1_core_pin')
        ast.parse(wrap)
        wrap_b = wrap.encode('utf-8')
        wrap_sha = sha(wrap_b)

        def resolve_literal(src):
            for node in ast.parse(src).body:
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '_resolve_source' for t in node.targets):
                    return node.value.value
            refuse('no _resolve_source literal')
        litq, litn = resolve_literal(wrapq), resolve_literal(wrap)
        if litq != litn:
            refuse('_resolve_source changed')
        lit_sha = sha(litn.encode('utf-8'))
        entry = pinned(ENTRY_T)
        entry = rep1(entry, "WRAPPER = Path('%s')\n" % WRAPQ[0],
                     "WRAPPER = Path('%s')\n" % os.path.join(publish_root, sub, WRAP_NAME), 'E1_wrapper_path')
        entry = rep1(entry, "WRAPPER_SHA = '%s'\n" % WRAPQ[1], "WRAPPER_SHA = '%s'\n" % wrap_sha, 'E1_wrapper_sha')
        ast.parse(entry)
        entry_b = entry.encode('utf-8')
        outputs.update({CORE_NAME: core_sha, WRAP_NAME: wrap_sha, ENTRY_NAME: sha(entry_b)})
        files += [(CORE_NAME, core_b), (WRAP_NAME, wrap_b), (ENTRY_NAME, entry_b)]
    return files, outputs, lit_sha


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) < 3:
        refuse('usage: OUTDIR SUB (--dry-run|--write) [--publish-root DIR] [--policy-only] [--seal-tuple C P A SCHEMA V]')
    out, sub, mode = args[0], args[1], args[2]
    rest = args[3:]
    if mode not in ('--dry-run', '--write'):
        refuse('mode must be --dry-run or --write')
    publish_root = CX2
    if rest and rest[0] == '--publish-root':
        if len(rest) < 2:
            refuse('--publish-root needs a directory')
        publish_root, rest = rest[1], rest[2:]
    policy_only = False
    if rest and rest[0] == '--policy-only':
        policy_only, rest = True, rest[1:]
    seal_tuple = None
    if rest:
        if rest[0] != '--seal-tuple' or len(rest) != 6:
            refuse('expected --seal-tuple C P A SCHEMA V')
        seal_tuple = tuple(rest[1:6])
    files, outputs, lit_sha = build(sub, policy_only=policy_only, seal_tuple=seal_tuple, publish_root=publish_root)
    res = {'generator': 'make_campaign_cascade_c2v002', 'mode': mode, 'sub': sub, 'policy_only': policy_only,
           'seal_tuple': seal_tuple, 'publish_root': publish_root, 'outdir': os.path.join(out, sub),
           'inputs': {'policy_r7': R7[1], 'core_r9': CORE9[1], 'wrapper_q5b1': WRAPQ[1], 'entry_template': ENTRY_T[1]},
           'outputs': outputs, 'resolve_source_literal_sha256_utf8': lit_sha}
    if mode == '--write':
        d = os.path.join(out, sub)
        os.mkdir(d)
        for name, b in files:
            with open(os.path.join(d, name), 'xb') as f:
                f.write(b)
        for name, s in outputs.items():
            if sha(open(os.path.join(d, name), 'rb').read()) != s:
                refuse('written bytes differ for ' + name)
    print(json.dumps(res, indent=1))
    return res


if __name__ == '__main__':
    main()
