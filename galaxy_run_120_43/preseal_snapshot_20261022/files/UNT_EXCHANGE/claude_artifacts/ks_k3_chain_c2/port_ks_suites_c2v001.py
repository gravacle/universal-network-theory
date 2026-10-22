"""Ported predecessor suites (ks_k3_chain_c2 c2v001; root A160): text substitutions only, each exact and counted.

  python3 -I -B port_ks_suites_c2v001.py TARGET_DIR [suite ...]

Each predecessor suite is read from its own path (sha256 checked from bytes) and written, with the substitutions listed
here and nothing else, beside the successors it tests (TARGET_DIR), by exclusive create. A unified DIFF of every port
goes to TARGET_DIR/diffs/PORT_<name>.diff. Substitutions point the suite at the successor file, at predecessor
siblings by absolute path, or, where marked PORT, adapt a seam or a static check to the successor (README section 5).
"""
import difflib
import hashlib
import os
import sys
ART='/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
SUITES = {
 'cp1': (ART+'/s4rc1_c3/build_c3v004/test_s4rc1_c3v004.py','6f4ce315ff37120d3a555da525955e6f0fe57c7e1f2ae806c9f81cac913ebff4',
         'test_s4rc1_c3v004_PORT_ks3_ks4_c2v001.py',
         [("'/cp1_runner_c3v004.py'", "'/cp1_runner_c3v004_ks3_c2v001.py'"),
          ("'/registry_assembler_c3v004.py'", "'/registry_assembler_c3v004_ks4_c2v001.py'"),
          ("os.path.join(build, 'C1_DRAFT_APPROVED_PRODUCERS_C3V004.json')",
           "os.path.join('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v004', 'C1_DRAFT_APPROVED_PRODUCERS_C3V004.json')")]),
}
PS3 = ART + '/s4rc1_c3/proof_side_c3v003'
SUITES['proofside'] = (PS3 + '/test_proof_side_c3v003.py', 'd28df3a58488a95ada72490b3cc78dad7c50a1ce35c16542a0e101fab9e877fc', 'test_proof_side_c3v003_PORT_ks6_c2v001.py',
    [("""        self.paths = {k: b + '/' + f for k, f in (('slot', 'lo_slot_proof_c3v003.py'),
                                                   ('state', 'lo_state_proof_adapter_c3v003.py'),
                                                   ('srb', 'srb_rot_adapter_c3v003.py'))}""",
      """        self.paths = {'slot': '%s/lo_slot_proof_c3v003.py', 'state': b + '/lo_state_proof_adapter_c3v003_ks6_c2v001.py',
                      'srb': '%s/srb_rot_adapter_c3v003.py'}   # PORT (ks_k3_chain_c2): the state adapter is KS6""" % (PS3, PS3))])
Q2 = ART + '/s4_acceptance_c2/acceptance_q2'
SUITES['q2'] = (Q2 + '/tests/test_acceptance_q2_c2v004.py', '085cafbe8c7abebe15a0364eefa53dccb80214cd58c2d51e974b02c3d85ce4d4', 'tests/test_acceptance_q2_c2v004_PORT_ks6_c2v001.py',
    [("ITEM / 'replay_inputs_writer_c2v002.py'", "Path(%r) / 'replay_inputs_writer_c2v002.py'" % Q2),
     ("ITEM / 'row_reference_producer_c2v003.py'", "Path(%r) / 'row_reference_producer_c2v003.py'" % Q2),
     ("ITEM / 'row_reference_producer_c2v002.py'", "Path(%r) / 'row_reference_producer_c2v002.py'" % Q2),
     ("ITEM / 'acceptance_handoff_c2v004.py'", "ITEM / 'acceptance_handoff_c2v004_ks6_c2v001.py'"),
     ("""    real_ex = HAND.execution_block
    HAND.execution_block = lambda **kw: None
    try:
        _, (r, _) = accept('H45_NO_EXECUTION')
    finally:
        HAND.execution_block = real_ex""",
      """    real_ex = HAND.execution_block
    HAND.execution_block = lambda **kw: None
    _pred_ex = HAND._predecessor().execution_block      # PORT: a non-S1 call runs in 5ff464cc (delegation): patch its seam too
    HAND._predecessor().execution_block = lambda **kw: None
    try:
        _, (r, _) = accept('H45_NO_EXECUTION')
    finally:
        HAND.execution_block = real_ex
        HAND._predecessor().execution_block = _pred_ex""")])
B1T = ART + '/s4_acceptance_c2/offset_b1/tests'
def _ks5_pin(tgt):
    q = os.path.join(tgt, 'certificate_guard_b1_ks5_c2v001.py')
    return q, hashlib.sha256(open(q, 'rb').read()).hexdigest()
SUITES['b1common'] = (B1T + '/b1_common_c2v001.py', '8b407c95c615c987acb78aee8dec1b300ff5bfabe4f566eb4d0707c07bc1c9bd', 'tests_b1/b1_common_c2v001_PORT_ks5_c2v001.py',
    [("    'guard': (B1 / 'certificate_guard_b1_c2v001.py', '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'),\n}",
      "    'guard': (Path(%r), %r),   # PORT (ks_k3_chain_c2): the successor under test is KS5\n}"),
     ("    if not d.parent.is_relative_to(B1 / 'tests')", "    if not d.parent.is_relative_to(Path(__file__).resolve().parent)")])
SUITES['b1guard'] = (B1T + '/test_guard_b1_c2v001.py', '5210e2150fa3988047ee4e668abd72590f8ce74bf4755743a7d68acc59c9ea50', 'tests_b1/test_guard_b1_c2v001_PORT_ks5_c2v001.py',
    [("sys.path.insert(0, '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/tests')",
      "sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.realpath(__file__)))"),
     ("import b1_common_c2v001 as T", "import b1_common_c2v001_PORT_ks5_c2v001 as T"),
     ("""old_text, new_text = open(T.PRED['guard'][0]).read(), open(T.SUCC['guard'][0]).read()
ol = old_text.splitlines()
first = next(i for i, x in enumerate(ol, 1) if x.strip() == "if state['nonnegative_masses'] is False:")
last = next(i for i, x in enumerate(ol, 1) if x.strip() == "lo = proof(row['LO'], 'LO')") - 1
touched = T.changed_lines(old_text, new_text)
allowed = {1} | set(range(first, last + 1))
ck('MF_diff_confined_to_docstring_and_signed_branch', touched and touched <= allowed, 'MUST_FAIL', {'outside': sorted(touched - allowed), 'signed_branch': [first, last]})
lits = ('1e-12', '0.005', '0.05', '1e-15', '1e-18', '8 * 1024 * 1024', "(64.0, 128.0)", 'K != 4.0')
ck('MF_threshold_literals_unchanged', all(old_text.count(x) == new_text.count(x) for x in lits), 'MUST_FAIL', {x: [old_text.count(x), new_text.count(x)] for x in lits})
""",
      """# PORT (ks_k3_chain_c2): the static checks are KS5's against its own predecessor b1 (the b1-vs-v003 checks do not apply).
old_text, new_text = open('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py').read(), open(T.SUCC['guard'][0]).read()
ol = old_text.splitlines()
l94 = next(i for i, x in enumerate(ol, 1) if x.strip() == "if K != 4.0 or Kbig not in (64.0, 128.0):")
lart = next(i for i, x in enumerate(ol, 1) if x.startswith("ART = Path("))
limp = next(i for i, x in enumerate(ol, 1) if x == "import hashlib")
touched = T.changed_lines(old_text, new_text)
allowed = {1, limp - 1, lart, l94, l94 + 1}
ck('MF_diff_confined_to_docstring_import_art_block_and_L94', touched and touched <= allowed, 'MUST_FAIL', {'outside': sorted(touched - allowed), 'allowed': sorted(allowed)})
lits = ('1e-12', '0.005', '0.05', '1e-15', '1e-18', '8 * 1024 * 1024', "(64.0, 128.0)")
ck('MF_threshold_literals_unchanged_and_K_literal_replaced', all(old_text.count(x) == new_text.count(x) for x in lits)
   and old_text.count('K != 4.0') == 1 and new_text.count('K != 4.0') == 0 and new_text.count('if K != kept or') == 1,
   'MUST_FAIL', {x: [old_text.count(x), new_text.count(x)] for x in lits + ('K != 4.0', 'if K != kept or')})
""")])
S1S = ART + '/s1_successors_c2'
SUITES['s1k3'] = (S1S + '/test_wrapper_s1k3_c2v001.py', '9d2d355ba63765c3f8b8e4cb0ed7c358c7da3f4c6613a7277aa14ae3b442a296', 'test_wrapper_s1k3_c2v001_PORT_ks5p_c2v002.py',
    [("SUCC_PATH = str(HERE / 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v001.py')",
      "SUCC_PATH = str(HERE / 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002.py')   # PORT: KS5'"),
     ("G12_PATH = str(HERE / 'step4_guard_c2v012.py')", "G12_PATH = %r" % (S1S + '/step4_guard_c2v012.py')),
     ("""    srcs = {p: h for p, h in (Q5B1, CORE, ORC, SENS, GB1)}
    srcs[SUCC_PATH] = sha(rb(SUCC_PATH))
    cfg = {'sources': srcs}""",
      """    srcs = {p: h for p, h in (Q5B1, CORE, ORC, SENS, GB1)}
    srcs[SUCC_PATH] = sha(rb(SUCC_PATH))
    srcs[str(HERE / 'certificate_guard_b1_ks5_c2v001.py')] = sha(rb(str(HERE / 'certificate_guard_b1_ks5_c2v001.py')))   # PORT: KS5' loads KS5
    cfg = {'sources': srcs}"""),
     ("m.MODULE_NAME.endswith('s1k3_c2v001')", "m.MODULE_NAME.endswith('s1k3_c2v002')")])
def main():
    tgt = os.path.realpath(sys.argv[1])
    which = sys.argv[2:] or list(SUITES)
    os.makedirs(os.path.join(tgt, 'diffs'), exist_ok=True)
    for k in which:
        src, sha, name, subs = SUITES[k]
        with open(src, 'rb') as f:
            raw = f.read()
        if hashlib.sha256(raw).hexdigest() != sha:
            raise SystemExit('PREDECESSOR_SUITE_PIN_MISMATCH ' + src)
        t = raw.decode()
        if k == 'b1common':
            subs = [(a, b % _ks5_pin(tgt)) if '%r' in b else (a, b) for a, b in subs]
        counts = []
        for a, b in subs:
            n = t.count(a)
            if n < 1:
                raise SystemExit('PORT_SUBSTITUTION_NOT_FOUND %s: %r' % (k, a[:80]))
            t = t.replace(a, b)
            counts.append(n)
        p = os.path.join(tgt, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        data = t.encode()
        with open(p, 'xb') as f:
            f.write(data)
        diff = ''.join(difflib.unified_diff(raw.decode().splitlines(True), t.splitlines(True), fromfile=src, tofile=p, n=2))
        dp = os.path.join(tgt, 'diffs', 'PORT_%s.diff' % os.path.basename(name)[:-3])
        with open(dp, 'xb') as f:
            f.write(diff.encode())
        print('%s %s %s substitutions=%s diff=%s' % (k, p, hashlib.sha256(data).hexdigest(), counts, dp))


if __name__ == '__main__':
    main()
