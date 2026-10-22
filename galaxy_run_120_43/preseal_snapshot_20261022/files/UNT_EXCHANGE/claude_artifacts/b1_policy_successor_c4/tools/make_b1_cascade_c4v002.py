# Claude4 B1/R-A2 (root A122/A126): deterministic generator of the adoption-policy successor cascade, v002.
# v002 = v001 (6d426c68) plus, after Claude4's own refute pass (SEM-7/CAS-B1, SEM-8/CAS-N4, CAS-N7):
#  - SUB (the output subfolder of calib_tail_readiness_cx2, e.g. v006r11_c4) is a parameter; every file name and the core's
#    policy path derive from it, so a finalized set can live beside the published v006r10_c4 set with its relative loads intact;
#  - --policy-only writes only the policy file (step-4 finalization: guard adoption() consults cfg['adoption_policy'] only, CAS-N2);
#  - --seal-tuple C P A SCHEMA V is cross-checked against the SEALED bytes: C = sha256 of the sealed compare file, P = its
#    V007_PREREG_SHA256 = sha256 of the sealed prereg file, A = its PIN_ADDENDUM_V005 = sha256 of the cited addendum file,
#    SCHEMA = its SCHEMA_REPORT, V = 64 lowercase hex; any mismatch refuses (no assert statements);
#  - with a tuple, the r7 comment 'No final V007 seal has been supplied.' becomes a statement of the registered seal.
# With SUB = v006r10_c4 and no tuple the three outputs are byte-identical to the published v001 outputs (regression check).
# From the VERIFIED bytes of policy r7 7c726fa2, core r9 a595c5c0 and wrapper r9 24abe3bc. Exclusive create; --dry-run writes nothing.
# usage: python3 -I -B run_fenced_c4st2.py make_b1_cascade_c4v002.py OUTDIR SUB (--dry-run | --write) [--policy-only]
#        [--seal-tuple C P A SCHEMA V]
import ast, hashlib, json, os, re, sys

CX2 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2'
R7 = (CX2 + '/v006r7/adoption_policy_cx2v006r7.py', '7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d')
CORE9 = (CX2 + '/v006r9/calibration_core_cx2v006r9.py', 'a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605')
WRAP9 = (CX2 + '/v006r9/calibration_orchestrator_cx2v006r9.py', '24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af')
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
    return 'adoption_policy_%s.py' % tag, 'calibration_core_%s.py' % tag, 'calibration_orchestrator_%s.py' % tag


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


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        refuse('usage: OUTDIR SUB (--dry-run|--write) [--policy-only] [--seal-tuple C P A SCHEMA V]')
    out, sub, mode = args[0], args[1], args[2]
    rest = args[3:]
    if mode not in ('--dry-run', '--write'):
        refuse('mode must be --dry-run or --write')
    policy_only = False
    if rest and rest[0] == '--policy-only':
        policy_only, rest = True, rest[1:]
    seal_tuple = None
    if rest:
        if rest[0] != '--seal-tuple' or len(rest) != 6:
            refuse('expected --seal-tuple C P A SCHEMA V')
        seal_tuple = tuple(rest[1:6])
        check_tuple(seal_tuple)
    POLICY_NAME, CORE_NAME, WRAP_NAME = names(sub)
    r7, core9, wrap9 = pinned(R7), pinned(CORE9), pinned(WRAP9)
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
        wrap = rep1(wrap9, "M=load(HERE/'calibration_core_cx2v006r9.py','_cx2v006r1',expected='%s')\n" % CORE9[1],
                    "M=load(HERE/'%s','_cx2v006r1',expected='%s')\n" % (CORE_NAME, core_sha), 'W1_core_pin')
        ast.parse(wrap)
        wrap_b = wrap.encode('utf-8')

        def resolve_literal(src):
            for node in ast.parse(src).body:
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '_resolve_source' for t in node.targets):
                    return node.value.value
            refuse('no _resolve_source literal')
        lit9, lit10 = resolve_literal(wrap9), resolve_literal(wrap)
        if lit9 != lit10:
            refuse('_resolve_source changed')
        lit_sha = sha(lit10.encode('utf-8'))
        outputs.update({CORE_NAME: core_sha, WRAP_NAME: sha(wrap_b)})
        files += [(CORE_NAME, core_b), (WRAP_NAME, wrap_b)]
    res = {'generator': 'make_b1_cascade_c4v002', 'mode': mode, 'sub': sub, 'policy_only': policy_only, 'seal_tuple': seal_tuple,
           'outdir': os.path.join(out, sub), 'inputs': {'policy_r7': R7[1], 'core_r9': CORE9[1], 'wrapper_r9': WRAP9[1]},
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


if __name__ == '__main__':
    main()
