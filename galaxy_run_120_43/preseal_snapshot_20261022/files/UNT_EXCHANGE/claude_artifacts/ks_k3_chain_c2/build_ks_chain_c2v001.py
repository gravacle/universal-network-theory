"""KS1-KS6 build (ks_k3_chain_c2, c2v001; root A160): every successor is its predecessor's bytes with exact-once edits.

  python3 -I -B build_ks_chain_c2v001.py --target-dir DIR [--final]

Each edit is (old, new) and must match the predecessor text exactly once, so the DIFF of every successor is exactly the
listed edits. Successor shas are computed from the written bytes in dependency order and substituted where a later
successor pins an earlier one (@@SHA_<name>@@; @@KSDIR@@ is the target directory). --final writes by exclusive create
('xb') and refuses an existing file; without it (development builds only) files are replaced. A DIFF per successor goes
to <target>/diffs/. Nothing else is read or written. Hashes from bytes.
"""
import argparse
import difflib
import hashlib
import json
import os
import sys

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
CB_PIN_LINES = ("CB_PIN = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/"
                "CASE_BLOCK_V007_C4V001.json',\n"
                "          'sha256': '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'}\n")
S1_LABEL_LINE = "S1_C3T_LABEL = re.compile(r'S1 transfer test C3T at u_A theta [0-9a-f]{16}; base [0-9a-f]{8}')\n"

PRED = {
    'KS1': (CERT + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'),
    'KS2': (CERT + '/point_response_producer_cx2v002.py', 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'),
    'KS5': (ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py', '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'),
    'KS5P': (ART + '/s1_successors_c2/calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v001.py', 'e7f52461c33d45d7e506daf25a8c115161cf5cfe661e31afd5a2b1848443856e'),
    'KS3C': (ART + '/s4rc1_c3/build_c3v004/s4rc1_common_c3v004.py', '53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083'),
    'KS3R': (ART + '/s4rc1_c3/build_c3v004/cp1_runner_c3v004.py', '3f5e5c188d4a6967afdb3bfab805d1cc8650e9c26793895096be55ca8f4f1a48'),
    'KS4': (ART + '/s4rc1_c3/build_c3v004/registry_assembler_c3v004.py', 'cb5c61ee3d515588394c694b115aca733426db670385eddf92ed389894d065b0'),
    'KS6CORE': (CERT + '/lo_core_r5_cx2v001.py', '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e'),
    'KS6CFG': (CERT + '/lo_config_r5_cx2v001.py', '6654d93c0241afd230d90bfcf327f16c22dd24c4da1d3eea72602212c2b6ae5a'),
    'KS6AD': (ART + '/s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py', '211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c'),
    'KS6HO': (ART + '/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py', '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'),
}
NAME = {
    'KS1': 'custody_cx2v002_ks1_c2v001.py',
    'KS2': 'point_response_producer_cx2v002_ks2_c2v001.py',
    'KS5': 'certificate_guard_b1_ks5_c2v001.py',
    'KS5P': 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002.py',
    'KS3C': 's4rc1_common_c3v004_ks3_c2v001.py',
    'KS3R': 'cp1_runner_c3v004_ks3_c2v001.py',
    'KS4': 'registry_assembler_c3v004_ks4_c2v001.py',
    'KS6CORE': 'lo_core_r5_cx2v001_ks6_c2v001.py',
    'KS6CFG': 'lo_config_r5_cx2v001_ks6_c2v001.py',
    'KS6AD': 'lo_state_proof_adapter_c3v003_ks6_c2v001.py',
    'KS6HO': 'acceptance_handoff_c2v004_ks6_c2v001.py',
}
ORDER = ('KS1', 'KS2', 'KS5', 'KS5P', 'KS3C', 'KS3R', 'KS4', 'KS6CORE', 'KS6CFG', 'KS6AD', 'KS6HO')
EDITS = {}

# ===================================================================================================== KS1 custody
EDITS['KS1'] = [
("""\"\"\"Inert, byte-pinned DDO154 point custody. No launch or run-directory discovery.
""",
"""\"\"\"KS1 (ks_k3_chain_c2 c2v001; root A160): custody_cx2v002 (6810b7c3) plus ONE allowance, for S1_UA_C3T only.

S1_UA_C3T = the S1 template's C3T label (s1k3 c2v001 L40) AND composite_grid_spec equal to CB C3T's (case block
76309ae3) bitwise. For it, derive_details accepts the +-3 cube (kept K 3); every other line it runs is 6810b7c3's, so
grid_sha256 still includes the composite grid (the C3T custody differs from u_A's) and modules_sha256 names this file.
Every other spec is handed to the unchanged 6810b7c3 module object, loaded below by path and sha (P), so its custody,
modules_sha256 included (it names the custody file, L133), is 6810b7c3's own. The label is checked first: no other
spec reads the case block. Edits: this docstring head, `import re`, HERE (the predecessor's folder), the block after
libraries(), the first line of derive_details and its cube check.

Inert, byte-pinned DDO154 point custody. No launch or run-directory discovery.
"""),
("""import math
from pathlib import Path
""",
"""import math
from pathlib import Path
import re
"""),
("""HERE = Path(__file__).resolve().parent
""",
"""HERE = ART/'calib_tail_readiness_cx2/certificates_per_point'   # KS1: 6810b7c3's folder (COMMON below; write_new scope)
"""),
("""def libraries():
    return (module(DRIVER,'cx2pc_driver',DRIVER_SHA),
            module(COMMON,'cx2pc_common',COMMON_SHA))
""",
"""def libraries():
    return (module(DRIVER,'cx2pc_driver',DRIVER_SHA),
            module(COMMON,'cx2pc_common',COMMON_SHA))

# KS1: the predecessor, unchanged, by path and sha. Every spec that is not S1_UA_C3T runs its code (P).
PREDECESSOR = (HERE/'custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377')
P = module(PREDECESSOR[0], 'ks1_predecessor_custody_cx2v002', PREDECESSOR[1])
# KS1: the S1_UA_C3T identity, as the wrapper successor s1k3 c2v001 reads it (L38-41, L72-86, L89-92).
""" + CB_PIN_LINES + S1_LABEL_LINE + """S1_C3T_KEPT_K = 3
_CB = {}

def cb_grid(case):
    \"\"\"CB `cases.<case>.normalized_spec_equal./numerics.composite_grid_spec`, from the pinned bytes (read once).\"\"\"
    if not _CB:
        raw = Path(CB_PIN['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != CB_PIN['sha256']:
            raise ValueError('CB case block: sha256 mismatch')
        doc = json.loads(raw)
        for c in ('C3T', 'C4T'):
            _CB[c] = doc['cases'][c]['normalized_spec_equal']['/numerics']['composite_grid_spec']
    return copy.deepcopy(_CB[case])

def s1_c3t_label(spec):
    lab = spec.get('label') if isinstance(spec, dict) else None
    return isinstance(lab, str) and S1_C3T_LABEL.fullmatch(lab) is not None

def s1_c3t_grid(numerics):
    \"\"\"composite_grid_spec == CB C3T bitwise (canonical JSON). A grid whose last break is not 3 never reads CB.\"\"\"
    try:
        grid = numerics.get('composite_grid_spec')
        if grid['breaks_inverse_kpc'][-1] != S1_C3T_KEPT_K:
            return False
        return canonical(grid) == canonical(cb_grid('C3T'))
    except (AttributeError, KeyError, IndexError, TypeError, ValueError):
        return False

def s1_c3t_spec(spec):
    \"\"\"The KS gate: S1_UA_C3T label AND CB C3T grid. Every K=3 allowance of the chain is behind it.\"\"\"
    return s1_c3t_label(spec) and s1_c3t_grid(spec.get('numerics'))
"""),
("""def derive_details(*,spec,driver_sha256=DRIVER_SHA):
    if driver_sha256!=DRIVER_SHA:raise ValueError('unsupported driver')
""",
"""def derive_details(*,spec,driver_sha256=DRIVER_SHA):
    if not s1_c3t_spec(spec):return P.derive_details(spec=spec,driver_sha256=driver_sha256)   # KS1: 6810b7c3's own code
    if driver_sha256!=DRIVER_SHA:raise ValueError('unsupported driver')
"""),
("""    if spec['numerics']['truncation']!={'shape':'cube'} or max(grid['breaks_inverse_kpc'])!=4 or min(grid['breaks_inverse_kpc'])!=-4:
        raise ValueError('K4 cube required')
""",
"""    if spec['numerics']['truncation']!={'shape':'cube'} or max(grid['breaks_inverse_kpc'])!=S1_C3T_KEPT_K or min(grid['breaks_inverse_kpc'])!=-S1_C3T_KEPT_K:
        raise ValueError('K3 cube required (S1_UA_C3T)')   # KS1: the kept K is 3 (CB C3T grid); 6810b7c3 L112-113 required 4
"""),
]

# ===================================================================================================== KS2 response producer
EDITS['KS2'] = [
("""\"\"\"Independent point-scoped numerical EPS/rho producer; static replay only.
""",
"""\"\"\"KS2 (ks_k3_chain_c2 c2v001; root A160): point_response_producer_cx2v002 (a1dcdea8) with the shell lower edge at the
spec's kept K, for S1_UA_C3T only (KS1's gate: the C3T label AND the CB C3T grid, bitwise).

For S1_UA_C3T (kept K = max(breaks_inverse_kpc) = 3): EPS has 179 unit shells [3,4]..[181,182]; rho has the 10-shell
partition [3,4],[4,5],[5,6],[6,8],[8,12],[12,16],[16,32],[32,64],[64,128],[128,182]; required_coverage_inverse_kpc is
[3, 182]; the rho sampled levels keep the k outside the K=3 cube (a1dcdea8 L347 kept those outside the K=4 cube, which
leaves the [3,4] shell empty); audit shells (AUDIT_LO) unchanged. Custody is KS1. Every other spec is handed to the
unchanged a1dcdea8 module object (P, by path and sha): its records, producer and custody pins included, are a1dcdea8's.

Independent point-scoped numerical EPS/rho producer; static replay only.
"""),
("""HERE = Path(__file__).resolve().parent
ART = HERE.parent.parent
CUSTODY_PATH = HERE / 'custody_cx2v002.py'
CUSTODY_SHA = '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'
""",
"""HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point')   # KS2: a1dcdea8's folder
ART = HERE.parent.parent
CUSTODY_PATH = Path('@@KSDIR@@/custody_cx2v002_ks1_c2v001.py')   # KS2: KS1 (it hands every other spec to 6810b7c3)
CUSTODY_SHA = '@@SHA_KS1@@'
PREDECESSOR = (HERE / 'point_response_producer_cx2v002.py', 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231')
"""),
("""CU = _module(CUSTODY_PATH, 'cx2_response_custody', CUSTODY_SHA)
C2 = _module(C2_PATH, 'cx2_response_c2', C2_SHA)
CC = C2.CC
""",
"""P = _module(PREDECESSOR[0], 'ks2_predecessor_point_response_cx2v002', PREDECESSOR[1])   # KS2: a1dcdea8, unchanged
CU = _module(CUSTODY_PATH, 'ks2_response_custody_ks1', CUSTODY_SHA)
C2 = _module(C2_PATH, 'ks2_response_c2', C2_SHA)
CC = C2.CC


def kept_k(spec):
    \"\"\"KS2: the spec's kept K, max(breaks_inverse_kpc) (procedure section 2). Only S1_UA_C3T reaches it: 3.\"\"\"
    k = max(spec['numerics']['composite_grid_spec']['breaks_inverse_kpc'])
    if k != CU.S1_C3T_KEPT_K:
        raise ValueError('S1_UA_C3T kept K must be 3')
    return int(k)
"""),
("""    \"\"\"Derive trusted custody and a new Binder at THIS point, not the anchor.\"\"\"
    details = CU.derive_details(spec=spec)
""",
"""    \"\"\"Derive trusted custody and a new Binder at THIS point, not the anchor.\"\"\"
    if not CU.s1_c3t_spec(spec):
        return P.point_context(spec)                          # KS2: a1dcdea8's own code path
    details = CU.derive_details(spec=spec)
"""),
("""def shell_plan(spec, shell_ranges=None, *, unit=True):
    end = int(math.ceil(math.sqrt(2) * spec['numerics']['uv_tail']['outer']['K_big_inverse_kpc']))
    full = [[float(n), float(n + 1)] for n in range(4, end)]
    if not unit:
        edges = [4, 5, 6, 8, 12, 16, 32, 64]
""",
"""def shell_plan(spec, shell_ranges=None, *, unit=True):
    if not CU.s1_c3t_spec(spec):
        return P.shell_plan(spec, shell_ranges, unit=unit)    # KS2: a1dcdea8's own code path
    K = kept_k(spec)                                          # KS2: lower edge = the kept K (3), not the literal 4
    end = int(math.ceil(math.sqrt(2) * spec['numerics']['uv_tail']['outer']['K_big_inverse_kpc']))
    full = [[float(n), float(n + 1)] for n in range(K, end)]
    if not unit:
        edges = [K] + [e for e in (4, 5, 6, 8, 12, 16, 32, 64) if e > K]
"""),
("""        if not (math.isfinite(lo) and math.isfinite(hi) and 4 <= lo < hi <= end):
""",
"""        if not (math.isfinite(lo) and math.isfinite(hi) and K <= lo < hi <= end):
"""),
("""    complete = selected[0][0] == 4 and selected[-1][1] == end and all(
""",
"""    complete = selected[0][0] == K and selected[-1][1] == end and all(
"""),
("""def produce_eps(spec, *, settings='registered', shell_ranges=None, context=None, progress=None):
    start = time.monotonic()
""",
"""def produce_eps(spec, *, settings='registered', shell_ranges=None, context=None, progress=None):
    if not CU.s1_c3t_spec(spec):                              # KS2: a1dcdea8's own code path
        return P.produce_eps(spec, settings=settings, shell_ranges=shell_ranges, context=context, progress=progress)
    K = kept_k(spec)
    start = time.monotonic()
"""),
("""        required_coverage_inverse_kpc=[4., float(end)], shells=rows, envelope_audit=audits,
""",
"""        required_coverage_inverse_kpc=[float(K), float(end)], shells=rows, envelope_audit=audits,
"""),
("""def produce_rho(spec, *, settings='registered', shell_ranges=None, context=None, progress=None):
    start = time.monotonic()
""",
"""def produce_rho(spec, *, settings='registered', shell_ranges=None, context=None, progress=None):
    if not CU.s1_c3t_spec(spec):                              # KS2: a1dcdea8's own code path
        return P.produce_rho(spec, settings=settings, shell_ranges=shell_ranges, context=context, progress=progress)
    K = kept_k(spec)
    start = time.monotonic()
"""),
("""            kv = kv[np.max(np.abs(kv), axis=1) * ctx['L'].KPC > 4 * (1 + 1e-12)]
""",
"""            kv = kv[np.max(np.abs(kv), axis=1) * ctx['L'].KPC > K * (1 + 1e-12)]   # KS2: outside the kept-K cube
"""),
("""        coverage_complete=complete, required_coverage_inverse_kpc=[4., float(end)],
""",
"""        coverage_complete=complete, required_coverage_inverse_kpc=[float(K), float(end)],
"""),
]

# ===================================================================================================== KS5 guard
EDITS['KS5'] = [
("""\"\"\"Fail-closed A134 (b1) successor of guard v003: offset GQ by the max component; nonnegative path unchanged.
""",
"""\"\"\"KS5 (ks_k3_chain_c2 c2v001; root A160): certificate guard b1 (9e3fc109) with ONE change, at L94.

The bundle's domain K must equal the expected identity's kept K: 4.0 for every identity, except an identity whose
numerics.composite_grid_spec equals CB C3T's (case block 76309ae3) bitwise, whose kept K is 3.0. b1 accepted K == 4.0
only, which also let a K=4 bundle certify a K=3 point; KS5 refuses that. A grid whose last break is not 3 never reads
the case block, so every other identity runs exactly b1's checks with b1's messages. The shell cursor (L123) already
starts at the domain K. Edits: this docstring head, `import copy`, the block after ART, and L94.

Fail-closed A134 (b1) successor of guard v003: offset GQ by the max component; nonnegative path unchanged.
"""),
("""import hashlib
import json
""",
"""import copy
import hashlib
import json
"""),
("""ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
""",
"""ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
# KS5: the expected identity's kept K (the identity carries no label: the CB C3T grid alone decides, bitwise).
""" + CB_PIN_LINES + """S1_C3T_KEPT_K = 3.0
_CB = {}


def cb_c3t_grid():
    if not _CB:
        raw = Path(CB_PIN['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != CB_PIN['sha256']:
            raise ValueError('CB case block: sha256 mismatch')
        _CB['C3T'] = json.loads(raw)['cases']['C3T']['normalized_spec_equal']['/numerics']['composite_grid_spec']
    return copy.deepcopy(_CB['C3T'])


def kept_k(identity):
    \"\"\"4.0, or 3.0 for the CB C3T grid only. None (no domain K passes) if a last-break-3 grid cannot be compared.\"\"\"
    try:
        grid = identity['numerics']['composite_grid_spec']
        if grid['breaks_inverse_kpc'][-1] != 3:
            return 4.0
    except (KeyError, IndexError, TypeError):
        return 4.0
    try:
        return S1_C3T_KEPT_K if canonical(grid) == canonical(cb_c3t_grid()) else 4.0
    except (OSError, ValueError, KeyError, TypeError):
        return None
"""),
("""        if K != 4.0 or Kbig not in (64.0, 128.0):
            raise ValueError('unsupported calibration domain')
""",
"""        kept = kept_k(expected_identity)                  # KS5: the identity's kept K (b1: the literal 4.0)
        if K != kept or Kbig not in (64.0, 128.0):
            raise ValueError('unsupported calibration domain' if kept == 4.0 else
                             'unsupported calibration domain: bundle domain K %r is not the kept K %r of this identity' % (K, kept))
"""),
]

# ===================================================================================================== KS5' wrapper
EDITS['KS5P'] = [
("""\"\"\"S1-only kept-K-3 successor of wrapper v002 q5b1 (Claude2 root workflow s1_successors_c2, c2v001; A150 R-S1-3 (2)).
""",
"""\"\"\"KS5' (ks_k3_chain_c2 c2v002; root A160): s1k3 c2v001 (e7f52461) whose S1_UA_C3T certificate checks use KS5.

c2v002 changes one thing. q5b1's module-global guard G (L30) becomes a dispatch that is certificate guard b1 (9e3fc109,
unchanged) except inside a KS5 scope, where it is KS5 (certificate_guard_b1_ks5_c2v001, by path and sha below):
  * certificate_check / prelaunch_check of an S1_UA_C3T spec (label, then CB C3T grid as c2v001) run in a KS5 scope:
    q5b1 L73 (policy review guard_sha256), L150 (PROOF_SCHEMA) and L192 (verify_bundle) read KS5;
  * every other spec runs in an explicit b1 scope: q5b1's code with b1, exactly as c2v001 and q5b1;
  * outside a spec (Context construction, a direct certificate_policy_gate() call: guard012 L256) the scope is the
    Context's own: KS5 iff its C1's certificate policy review binds KS5's sha, else b1. So an S1_UA_C3T C1 binds KS5
    (procedure step 6.6); under it every other spec still meets b1's sha and its policy gate reads pending.
c2v001's S1-only domain check (bundle domain K == kept K 3) is kept. The text of c2v001 follows.

S1-only kept-K-3 successor of wrapper v002 q5b1 (Claude2 root workflow s1_successors_c2, c2v001; A150 R-S1-3 (2)).
"""),
("""MODULE_NAME = 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v001'
""",
"""MODULE_NAME = 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002'
"""),
("""S1_C3T_KEPT_K = 3
GRID = 'numerics.composite_grid_spec'
""",
"""S1_C3T_KEPT_K = 3
GRID = 'numerics.composite_grid_spec'
GUARD_KS5 = ('@@KSDIR@@/certificate_guard_b1_ks5_c2v001.py', '@@SHA_KS5@@')   # c2v002
"""),
("""PREDECESSOR_VALIDATE_BLOCK = W.validate_block  # the same object (q5b1 L35: validate_block = M.validate_block)
""",
"""PREDECESSOR_VALIDATE_BLOCK = W.validate_block  # the same object (q5b1 L35: validate_block = M.validate_block)
G_B1 = W.G                                     # c2v002: q5b1 L30's guard, b1 9e3fc109, unchanged
G_KS5 = _load(GUARD_KS5[0], '_ks5_guard_for_s1k3_c2v002', GUARD_KS5[1])
_GUARD = contextvars.ContextVar('s1k3_c2v002_guard', default=None)


class _GuardDispatch(object):
    \"\"\"c2v002: q5b1's module-global G. b1 outside a KS5 scope; KS5 inside one (see the module docstring).\"\"\"

    def __getattr__(self, name):
        g = _GUARD.get()
        return getattr(G_B1 if g is None else g, name)


W.G = _GuardDispatch()


def _policy_binds_ks5(cfg):
    \"\"\"c2v002: True iff the C1's certificate policy review binds KS5's sha (the q5b1 L73 guard_sha256).\"\"\"
    try:
        doc = M.pin_doc(cfg['tail_readiness']['certificate_policy_review'], 'certificate policy review')
        return isinstance(doc, dict) and doc.get('guard_sha256') == GUARD_KS5[1]
    except Exception:
        return False
"""),
("""class Context(W.Context):
    \"\"\"q5b1's Context; S1_UA_C3T specs only take the two overrides below.\"\"\"

    def certificate_check(self, spec, phase, *, result=None, call_dir=None, _handoff=None):
        if not s1_c3t_identified(spec):
            return super().certificate_check(spec, phase, result=result, call_dir=call_dir, _handoff=_handoff)
        validate_s1_c3t_block(spec['numerics'])
        token = _S1_BLOCK.set(spec['numerics'])
        try:
            g = super().certificate_check(spec, phase, result=result, call_dir=call_dir, _handoff=_handoff)
        finally:
            _S1_BLOCK.reset(token)
""",
"""class Context(W.Context):
    \"\"\"q5b1's Context; S1_UA_C3T specs only take the two overrides below (c2v002: and the KS5 guard scope).\"\"\"

    def __init__(self, config):
        cfg = O.load_json_file(config, 'config') if isinstance(config, (str, Path)) else config
        self._s1_guard_ks5 = _policy_binds_ks5(cfg)                    # c2v002: the Context's own guard scope
        token = _GUARD.set(G_KS5 if self._s1_guard_ks5 else G_B1)
        try:
            super().__init__(config)
        finally:
            _GUARD.reset(token)

    def certificate_policy_gate(self):
        if _GUARD.get() is not None:                                   # c2v002: inside a spec (or init) scope
            return super().certificate_policy_gate()
        token = _GUARD.set(G_KS5 if getattr(self, '_s1_guard_ks5', False) else G_B1)
        try:
            return super().certificate_policy_gate()
        finally:
            _GUARD.reset(token)

    def certificate_check(self, spec, phase, *, result=None, call_dir=None, _handoff=None):
        if not s1_c3t_identified(spec):
            gtoken = _GUARD.set(G_B1)                                  # c2v002: every other spec meets b1
            try:
                return super().certificate_check(spec, phase, result=result, call_dir=call_dir, _handoff=_handoff)
            finally:
                _GUARD.reset(gtoken)
        validate_s1_c3t_block(spec['numerics'])
        token = _S1_BLOCK.set(spec['numerics'])
        gtoken = _GUARD.set(G_KS5)                                     # c2v002: S1_UA_C3T meets KS5
        try:
            g = super().certificate_check(spec, phase, result=result, call_dir=call_dir, _handoff=_handoff)
        finally:
            _GUARD.reset(gtoken)
            _S1_BLOCK.reset(token)
"""),
("""    def prelaunch_check(self, spec, recovery=False):
        if not s1_c3t_identified(spec):
            return super().prelaunch_check(spec, recovery=recovery)
""",
"""    def prelaunch_check(self, spec, recovery=False):
        if not s1_c3t_identified(spec):
            gtoken = _GUARD.set(G_B1)                                  # c2v002: every other spec meets b1
            try:
                return super().prelaunch_check(spec, recovery=recovery)
            finally:
                _GUARD.reset(gtoken)
"""),
]

# ===================================================================================================== KS3 common
EDITS['KS3C'] = [
("""\"\"\"S4-R-C1 shared helpers and pinned tables (Claude3 lane; root A122; reviewer Codex1 under A115).
""",
"""\"\"\"KS3 common (ks_k3_chain_c2 c2v001; root A160): s4rc1_common_c3v004 (53f10e6e) plus row 32, S1_UA_C3T.

Rows 1-31, POINTS, point_rows(), DOMAIN and every existing PINS entry are unchanged, so select_points(None), the plan
of rows 1-31 and the registry's 31-point table are c3v004's. Row 32 is not in POINTS: it is read from S1_ROW_FILE, a
root-written record (procedure step 3: row, key, label S1_UA_C3T, spec path under s4rc1_c3/s1_c3t_specs/, spec sha,
distance, q_inf), and admitted only if the spec's bytes hash to the recorded sha, its point key (core recipe) is the
recorded key, it is not one of the 31, and it is S1_UA_C3T (the C3T label AND the CB C3T grid, bitwise). The row file is
read only when a selection token or key is not one of the 31. New PINS: KS1, KS2, KS5, the wrapper successor KS5' and
the case block. New helpers: s1_rows, rows_for_key, is_s1_row, kept_k_of_row, domain_of_row, s1_pins_as_table and the
S1_UA_C3T gate. select_points tries row 32 only for a token no table row takes. The c3v004 text follows.

S4-R-C1 shared helpers and pinned tables (Claude3 lane; root A122; reviewer Codex1 under A115).
"""),
("""    'ruling_0674': (EXCHANGE + '/FROM_CODEX/0674_2026-10-19_S4RC1_partial_rulings_GQ_EPS_go_R1_guard.md', '592bb0f5b099b291684074c4af22dc21a32a6379cd05ccc4b2f49f96b1dc180d'),
}
""",
"""    'ruling_0674': (EXCHANGE + '/FROM_CODEX/0674_2026-10-19_S4RC1_partial_rulings_GQ_EPS_go_R1_guard.md', '592bb0f5b099b291684074c4af22dc21a32a6379cd05ccc4b2f49f96b1dc180d'),
    # KS3 (A160): the K=3 chain, used for row 32 (S1_UA_C3T) only; rows 1-31 keep every pin above.
    'custody_ks1': ('@@KSDIR@@/custody_cx2v002_ks1_c2v001.py', '@@SHA_KS1@@'),
    'response_producer_ks2': ('@@KSDIR@@/point_response_producer_cx2v002_ks2_c2v001.py', '@@SHA_KS2@@'),
    'guard_ks5': ('@@KSDIR@@/certificate_guard_b1_ks5_c2v001.py', '@@SHA_KS5@@'),
    'wrapper_s1k3_ks5p': ('@@KSDIR@@/calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002.py', '@@SHA_KS5P@@'),
    'case_block': (ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json', '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'),
}
"""),
("""    chosen = set()
    for tok in [t.strip() for t in selection.split(',') if t.strip()]:
        hit = [r for r in rows if tok == str(r['row']) or tok in r['names']
               or (len(tok) >= 8 and re.fullmatch('[0-9a-f]+', tok) and r['key'].startswith(tok))]
        if len(hit) != 1:
            raise Refusal('POINT_SELECTION_UNRESOLVED: ' + tok)
        chosen.add(hit[0]['key'])
    return [r for r in rows if r['key'] in chosen]
""",
"""    chosen = set()
    s1_hits = {}
    for tok in [t.strip() for t in selection.split(',') if t.strip()]:
        hit = [r for r in rows if tok == str(r['row']) or tok in r['names']
               or (len(tok) >= 8 and re.fullmatch('[0-9a-f]+', tok) and r['key'].startswith(tok))]
        if not hit:                                   # KS3: a token no table row takes may name row 32 (S1_UA_C3T)
            hit = [r for r in s1_rows() if tok == str(r['row']) or tok in r['names']
                   or (len(tok) >= 8 and re.fullmatch('[0-9a-f]+', tok) and r['key'].startswith(tok))]
            s1_hits.update({r['key']: r for r in hit})
        if len(hit) != 1:
            raise Refusal('POINT_SELECTION_UNRESOLVED: ' + tok)
        chosen.add(hit[0]['key'])
    return [r for r in rows if r['key'] in chosen] + list(s1_hits.values())


# ---------------------------------------------------------------- KS3 (A160): row 32, S1_UA_C3T
S1_ROW_FILE = LANE_ROOT + '/s1_c3t_specs/S1_UA_C3T_CP1_ROW32.json'   # root writes it (exclusive create), procedure step 3
S1_ROW_SCHEMA = 'S4RC1_CP1_S1_UA_C3T_ROW_KS3_C2V001'
S1_SPEC_PREFIX = 's4rc1_c3/s1_c3t_specs/'          # the CP-1 input spec folder of procedure step 2
S1_ROW, S1_NAME, S1_C3T_KEPT_K = 32, 'S1_UA_C3T', 3
S1_ROW_KEYS = {'schema', 'row', 'key', 'label', 'names', 'spec_path', 'spec_sha256', 'distance_Mpc', 'q_inf'}
""" + S1_LABEL_LINE + """_CB = {}


def cb_grid(case):
    \"\"\"CB `cases.<case>.normalized_spec_equal./numerics.composite_grid_spec` (PINS case_block), read once.\"\"\"
    if not _CB:
        doc = json.loads(read_bytes_pinned(canonical_pin('case_block'), (ART,), 'case block'))
        for c in ('C3T', 'C4T'):
            _CB[c] = doc['cases'][c]['normalized_spec_equal']['/numerics']['composite_grid_spec']
    return copy.deepcopy(_CB[case])


def s1_c3t_label(spec):
    lab = spec.get('label') if isinstance(spec, dict) else None
    return isinstance(lab, str) and S1_C3T_LABEL.fullmatch(lab) is not None


def s1_c3t_spec(spec):
    \"\"\"S1_UA_C3T: the C3T label AND composite_grid_spec == CB C3T bitwise (s1k3 c2v001 L84-92).\"\"\"
    if not s1_c3t_label(spec):
        return False
    try:
        return canonical(spec['numerics']['composite_grid_spec']) == canonical(cb_grid('C3T'))
    except (KeyError, TypeError, ValueError):
        return False


def s1_rows():
    \"\"\"[row 32] if S1_ROW_FILE exists and verifies, [] if it does not exist; Refusal if it exists and fails.\"\"\"
    if not os.path.exists(S1_ROW_FILE):
        return []
    try:
        with open(require_policy(S1_ROW_FILE, (ART,), 'S1 row file'), 'rb') as f:
            raw = f.read()
        doc = json.loads(raw)
        if not isinstance(doc, dict) or set(doc) != S1_ROW_KEYS or doc['schema'] != S1_ROW_SCHEMA:
            raise Refusal('schema/keys')
        if (doc['row'] != S1_ROW or doc['label'] != S1_NAME or doc['names'] != [S1_NAME] or not is_sha(doc['key'])
                or not is_sha(doc['spec_sha256']) or not finite_number(doc['distance_Mpc'], 0) or not finite_number(doc['q_inf'], 0)
                or doc['q_inf'] <= 0 or not isinstance(doc['spec_path'], str) or not doc['spec_path'].startswith(S1_SPEC_PREFIX)):
            raise Refusal('row fields')
        if doc['key'] in [r[1] for r in POINTS]:
            raise Refusal('key is one of the 31 table points')
        spec_path = require_policy(ART + '/' + doc['spec_path'], (ART,), 'S1 spec')
        with open(spec_path, 'rb') as f:
            sraw = f.read()
        if sha256_bytes(sraw) != doc['spec_sha256']:
            raise Refusal('spec sha256 from bytes differs')
        spec = json.loads(sraw)
        if point_key(spec) != doc['key']:
            raise Refusal('point key from the spec bytes differs')
        if not s1_c3t_spec(spec):
            raise Refusal('spec is not S1_UA_C3T (C3T label and CB C3T grid)')
        if spec['physical']['distance_Mpc'] != doc['distance_Mpc']:
            raise Refusal('distance differs from the spec')
    except (Refusal, OSError, ValueError, KeyError, TypeError) as exc:
        raise Refusal('S1_ROW_FILE_INVALID (%s): %s: %s' % (S1_ROW_FILE, type(exc).__name__, exc))
    return [dict(row=S1_ROW, key=doc['key'], label=S1_NAME, names=[S1_NAME], spec_path=spec_path,
                 spec_sha256=doc['spec_sha256'], distance_Mpc=doc['distance_Mpc'], q_inf=doc['q_inf'], s1_c3t=True,
                 kept_K=S1_C3T_KEPT_K, row_file={'path': S1_ROW_FILE, 'sha256': sha256_bytes(raw)})]


def rows_for_key(key):
    \"\"\"The table row(s) with this key; row 32 is looked up only for a key none of the 31 has.\"\"\"
    return [r for r in point_rows() if r['key'] == key] or [r for r in s1_rows() if r['key'] == key]


def is_s1_row(row):
    return isinstance(row, dict) and row.get('s1_c3t') is True


def kept_k_of_row(row):
    return S1_C3T_KEPT_K if is_s1_row(row) else 4


def domain_of_row(row):
    \"\"\"Bundle domain: DOMAIN (K 4) for rows 1-31; K 3 for row 32 (KS4, procedure section 2).\"\"\"
    return {'K_inverse_kpc': float(S1_C3T_KEPT_K), 'K_big_inverse_kpc': 128.0} if is_s1_row(row) else dict(DOMAIN)


def s1_pins_as_table(pins):
    \"\"\"Row 32's source pins in the form rows 1-31 record: KS2's point_context records custody = KS1 and producer = KS2
    where a1dcdea8 records 6810b7c3 and a1dcdea8. Both are checked, then replaced; every other pin is kept as is.\"\"\"
    if (not isinstance(pins, dict) or pins.get('custody') != canonical_pin('custody_ks1')
            or pins.get('producer') != canonical_pin('response_producer_ks2')):
        raise Refusal('S1_SOURCE_PINS_ARE_NOT_KS1_AND_KS2')
    out = dict(pins)
    out['custody'], out['producer'] = canonical_pin('custody'), canonical_pin('response_producer')
    return out
"""),
]

# ===================================================================================================== KS3 runner
EDITS['KS3R'] = [
("""\"\"\"S4-R-C1 CP-1 runner c3v004, GQ, EPS and RHO (Claude3 lane; root A122, A134, A138; reviewer Codex1 under A115).
""",
"""\"\"\"KS3 runner (ks_k3_chain_c2 c2v001; root A160): cp1_runner_c3v004 (3f5e5c18) plus row 32, S1_UA_C3T.

It loads the KS3 common (rows 1-31 and every c3v004 pin unchanged; row 32 from the root-written row file). For rows
1-31 every stage, check, gate and record is c3v004's; only the runner/common self-pins in the records name this build.
Row 32 (S1_UA_C3T) only: the response producer is KS2 (custody KS1); check_eps wants the 179 unit shells [3,4]..[181,182]
and the KS2 producer pin; check_rho wants coverage [3, 182], the 10-shell partition from [3,4] and the KS2 pin; the F6
source-pin match compares the anchor's pins with row 32's after its custody/producer pins (KS1/KS2, checked) are mapped
to 6810b7c3/a1dcdea8 (C.s1_pins_as_table). GQ is the canonical gq_producer 2832ceb9: its kernel gq_geometry (c6ffb338)
derives custody with 6810b7c3 and takes the K=4 kept region (L39), so row 32 stops at GQ until a K=3 GQ successor exists
(open item for root). adapt-eps is c3v004's (EPS adapter 4de70486, K=4 only: open item for root). The c3v004 text follows.

S4-R-C1 CP-1 runner c3v004, GQ, EPS and RHO (Claude3 lane; root A122, A134, A138; reviewer Codex1 under A115).
"""),
("""COMMON_PATH = HERE + '/s4rc1_common_c3v004.py'
COMMON_SHA = '53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083'
""",
"""COMMON_PATH = HERE + '/s4rc1_common_c3v004_ks3_c2v001.py'          # KS3 common
COMMON_SHA = '@@SHA_KS3C@@'
"""),
("""    spec = importlib.util.spec_from_file_location('s4rc1_common_c3v004', COMMON_PATH)
""",
"""    spec = importlib.util.spec_from_file_location('s4rc1_common_c3v004_ks3_c2v001', COMMON_PATH)
"""),
("""RHO_COMPARE_KEYS = ('schema', 'gate', 'identity', 'point_sha256', 'custody', 'settings', 'coverage_complete',
                    'required_coverage_inverse_kpc', 'full_registered_search_executed', 'shells')   # wrapper v002 L177-178
""",
"""RHO_COMPARE_KEYS = ('schema', 'gate', 'identity', 'point_sha256', 'custody', 'settings', 'coverage_complete',
                    'required_coverage_inverse_kpc', 'full_registered_search_executed', 'shells')   # wrapper v002 L177-178
# KS3 (A160): row 32 (S1_UA_C3T, kept K 3) only.
EPS_LO_S1 = 3                                     # 179 unit shells [3,4] .. [181,182]
RHO_COVERAGE_S1 = [3.0, float(C.SHELL_END)]
RHO_PARTITION_S1 = [[3.0, 4.0]] + RHO_PARTITION   # the 10-shell partition of KS2 shell_plan(unit=False) at K 3
"""),
("""def real_loader():
    \"\"\"Canonical-path imports of the two pinned producers (R4).\"\"\"
    gq = C.load_pinned('gq_producer', 's4rc1_cp1_gq_producer_cx2v005')
    pr = C.load_pinned('response_producer', 's4rc1_cp1_point_response_cx2v002')
    return gq, pr
""",
"""def real_loader():
    \"\"\"Canonical-path imports of the two pinned producers (R4).\"\"\"
    gq = C.load_pinned('gq_producer', 's4rc1_cp1_gq_producer_cx2v005')
    pr = C.load_pinned('response_producer', 's4rc1_cp1_point_response_cx2v002')
    return gq, pr


def real_loader_s1():
    \"\"\"KS3, row 32 (S1_UA_C3T): the canonical GQ producer and the KS2 response producer (which imports KS1).\"\"\"
    gq = C.load_pinned('gq_producer', 's4rc1_cp1_gq_producer_cx2v005')
    pr = C.load_pinned('response_producer_ks2', 's4rc1_cp1_point_response_ks2_c2v001')
    return gq, pr
"""),
("""def check_eps(eps, key, custody):
    shells = eps.get('shells') or []
    want = [[float(n), float(n + 1)] for n in range(4, C.SHELL_END)]
""",
"""def check_eps(eps, key, custody, s1=False):
    shells = eps.get('shells') or []
    want = [[float(n), float(n + 1)] for n in range(EPS_LO_S1 if s1 else 4, C.SHELL_END)]   # KS3: row 32 from 3
"""),
("""        'producer_pin_canonical_R4': eps.get('producer') == C.canonical_pin('response_producer'),
        'shells_4_to_182_unit': [s.get('range_inverse_kpc') for s in shells] == want,
""",
"""        'producer_pin_canonical_R4': eps.get('producer') == C.canonical_pin('response_producer_ks2' if s1 else 'response_producer'),
        ('shells_3_to_182_unit' if s1 else 'shells_4_to_182_unit'): [s.get('range_inverse_kpc') for s in shells] == want,
"""),
("""def check_rho(rho, key, custody):
""",
"""def check_rho(rho, key, custody, s1=False):
"""),
("""        'coverage_4_to_182': rho.get('required_coverage_inverse_kpc') == RHO_COVERAGE,
        'partition_9_shells_K_big_128': [s.get('range_inverse_kpc') if isinstance(s, dict) else None for s in shells] == RHO_PARTITION,
""",
"""        ('coverage_3_to_182' if s1 else 'coverage_4_to_182'):
            rho.get('required_coverage_inverse_kpc') == (RHO_COVERAGE_S1 if s1 else RHO_COVERAGE),
        ('partition_10_shells_K_big_128' if s1 else 'partition_9_shells_K_big_128'):
            [s.get('range_inverse_kpc') if isinstance(s, dict) else None for s in shells] == (RHO_PARTITION_S1 if s1 else RHO_PARTITION),
"""),
("""        'producer_pin_canonical_R4': rho.get('producer') == C.canonical_pin('response_producer'),
""",
"""        'producer_pin_canonical_R4': rho.get('producer') == C.canonical_pin('response_producer_ks2' if s1 else 'response_producer'),
"""),
("""def rho_stage(pr, spec, ctx, key, details, out_root, out, k16, letter, gate):
""",
"""def rho_stage(pr, spec, ctx, key, details, out_root, out, k16, letter, gate, s1=False):
"""),
("""    checks = check_rho(rho, key, details['custody'])
""",
"""    checks = check_rho(rho, key, details['custody'], s1=s1)
"""),
("""def run_point(row, out_root, *, operator_lane, attempt=1, run_id='', loader=real_loader,
""",
"""def run_point(row, out_root, *, operator_lane, attempt=1, run_id='', loader=None,
"""),
("""    \"\"\"One point, GQ then EPS then RHO (c3v003), in this process (anchor attempt b in a separate one). (exit, summary).\"\"\"
    require_registered(settings, shell_ranges, node_limit)
""",
"""    \"\"\"One point, GQ then EPS then RHO (c3v003), in this process (anchor attempt b in a separate one). (exit, summary).\"\"\"
    s1 = C.is_s1_row(row)                             # KS3: row 32 (S1_UA_C3T) takes KS1/KS2 and the kept-K-3 checks
    loader = loader or (real_loader_s1 if s1 else real_loader)
    require_registered(settings, shell_ranges, node_limit)
"""),
("""             'producers': {'gq': C.canonical_pin('gq_producer'), 'eps': C.canonical_pin('response_producer')},
""",
"""             'producers': {'gq': C.canonical_pin('gq_producer'), 'eps': C.canonical_pin('response_producer_ks2' if s1 else 'response_producer')},
"""),
("""    start.update(thread_env_record())                 # F4
""",
"""    start.update(thread_env_record())                 # F4
    if s1:                                            # KS3: the row file it came from (row 32 only)
        start['s1_c3t_row'] = {'row_file': row['row_file'], 'kept_K': row['kept_K']}
"""),
("""        anchor_ctx, anchor_why, hold = None, None, None
""",
"""        mine = ctx_rec['source_pins']
        if s1:                                        # KS3: KS1/KS2 replace exactly the custody and producer pins (F6)
            try:
                mine = C.s1_pins_as_table(mine)
                ctx_rec['checks']['s1_source_pins_are_ks1_and_ks2'] = True
            except Refusal:
                mine, ctx_rec['checks']['s1_source_pins_are_ks1_and_ks2'] = None, False
        anchor_ctx, anchor_why, hold = None, None, None
"""),
("""        ctx_rec['checks_info'] = {'source_pins_match_anchor': None if anchor_ctx is None else
                                  anchor_ctx.get('source_pins') == ctx_rec['source_pins'],
""",
"""        ctx_rec['checks_info'] = {'source_pins_match_anchor': None if anchor_ctx is None else
                                  anchor_ctx.get('source_pins') == mine,
"""),
("""            ctx_rec['checks']['source_pins_match_anchor'] = anchor_ctx.get('source_pins') == ctx_rec['source_pins']
""",
"""            ctx_rec['checks']['source_pins_match_anchor'] = anchor_ctx.get('source_pins') == mine
"""),
("""        eps_checks = check_eps(eps, key, details['custody'])
""",
"""        eps_checks = check_eps(eps, key, details['custody'], s1=s1)
"""),
("""            ok_a, rec_a = rho_stage(pr, spec, ctx, key, details, out_root, out, k16, 'a', gate)
""",
"""            ok_a, rec_a = rho_stage(pr, spec, ctx, key, details, out_root, out, k16, 'a', gate, s1=s1)
"""),
("""        out.append({'row': row['row'], 'label': row['label'], 'names': row['names'], 'key': row['key'],
                    'spec': pin, 'status': status, 'q_inf': row['q_inf'], 'distance_Mpc': row['distance_Mpc']})
""",
"""        out.append({'row': row['row'], 'label': row['label'], 'names': row['names'], 'key': row['key'],
                    'spec': pin, 'status': status, 'q_inf': row['q_inf'], 'distance_Mpc': row['distance_Mpc']})
        if C.is_s1_row(row):                          # KS3: row 32 only
            out[-1].update(kept_K=row['kept_K'], row_file=row['row_file'], eps_shells='179 unit shells [3,4]..[181,182]',
                           rho='coverage [3,182], 10 shells from [3,4]', producers={'eps_rho': C.canonical_pin('response_producer_ks2'),
                                                                                     'gq': C.canonical_pin('gq_producer')},
                           as_built_open='GQ 2832ceb9 (gq_geometry c6ffb338 L18-26 custody 6810b7c3, L39 K=4 kept region) and '
                                         'adapt-eps 4de70486 refuse K=3: root items (ks_k3_chain_c2 README)')
"""),
("""        if ns.cmd == 'worker':
            rows = [x for x in C.point_rows() if x['key'] == ns.point]
""",
"""        if ns.cmd == 'worker':
            rows = C.rows_for_key(ns.point)           # KS3: row 32 only for a key none of the 31 has
"""),
("""        if ns.cmd == 'rho-repeat':
            rows = [x for x in C.point_rows() if x['key'] == ns.point]
""",
"""        if ns.cmd == 'rho-repeat':
            rows = C.rows_for_key(ns.point)
"""),
]

# ===================================================================================================== KS4 assembler
EDITS['KS4'] = [
("""\"\"\"S4-R-C1 C1 certificate registry assembler and OFFLINE verifier c3v004 (Claude3; A122, A134, A138; Codex1 under A115).
""",
"""\"\"\"KS4 (ks_k3_chain_c2 c2v001; root A160): registry_assembler_c3v004 (cb5c61ee) plus row 32, S1_UA_C3T.

Loads the KS3 common. Rows 1-31: every check, document and verification is c3v004's (only the generator/common
self-pins name this build). Row 32 (S1_UA_C3T) only:
  bundle    domain K_inverse_kpc = 3.0 (the kept K), and the spec must be S1_UA_C3T;
  registry  row 32 is found through the KS3 row file; its EPS source pins enter the single-value rule (L308-309) after
            KS1/KS2 are checked and mapped to 6810b7c3/a1dcdea8 (C.s1_pins_as_table); 'complete_31_point_table' is
            "all 31 table keys present" (equal to c3v004's count rule for any registry of table points);
            's1_c3t_points' and the S1 C1 draft fields (custody deriver KS1, guard KS5) appear only with row 32;
  verify    replicates the wrapper successor s1k3 c2v002 (KS5'): the S1 block rule (CB C3T grid, then core's checks on
            the CB C4T shadow), the C1 policy gate with custody deriver KS1 and guard_sha256 KS5, wrapper v002 L145-191
            from its bytes, KS5's verify_bundle, and the bundle domain K == 3 check. Every other row is checked against
            the c3v004 gate (6810b7c3, b1), so one C1 never certifies both kinds.
The c3v004 text follows.

S4-R-C1 C1 certificate registry assembler and OFFLINE verifier c3v004 (Claude3; A122, A134, A138; Codex1 under A115).
"""),
("""COMMON_PATH = HERE + '/s4rc1_common_c3v004.py'
COMMON_SHA = '53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083'
""",
"""COMMON_PATH = HERE + '/s4rc1_common_c3v004_ks3_c2v001.py'          # KS3 common
COMMON_SHA = '@@SHA_KS3C@@'
"""),
("""    spec = importlib.util.spec_from_file_location('s4rc1_common_c3v004', COMMON_PATH)
""",
"""    spec = importlib.util.spec_from_file_location('s4rc1_common_c3v004_ks3_c2v001', COMMON_PATH)
"""),
("""    fs = block['brackets']['rule']['fs_absolute_overrides']
    if set(fs) != {str(i) for i in range(72)} or any(v != HULL for v in fs.values()):
        raise Refusal('full A32 hull required on every one of 72 columns')
""",
"""    fs = block['brackets']['rule']['fs_absolute_overrides']
    if set(fs) != {str(i) for i in range(72)} or any(v != HULL for v in fs.values()):
        raise Refusal('full A32 hull required on every one of 72 columns')


def validate_spec_block(spec):
    \"\"\"KS4: the wrapper successor's spec-level rule (s1k3 L89-102). An S1_UA_C3T-labelled spec: its grid must equal CB C3T
    bitwise, then the transcription above runs on the block with only the grid set to CB C4T's. Every other spec: the
    transcription above, unchanged.\"\"\"
    if C.s1_c3t_label(spec):
        n = spec['numerics']
        if C.canonical(n.get('composite_grid_spec')) != C.canonical(C.cb_grid('C3T')):
            raise Refusal('S1_UA_C3T: composite_grid_spec must equal CB C3T bitwise (kept K 3)')
        shadow = dict(n)
        shadow['composite_grid_spec'] = C.cb_grid('C4T')
        return validate_block(shadow)
    return validate_block(spec['numerics'])
"""),
("""    spec = load_point_spec(row)
    ident = C.point_identity(spec)
    key = C.digest(ident)
    eps_pin, eps = _proof(eps_proof, 'EPS', roots)
""",
"""    spec = load_point_spec(row)
    if C.is_s1_row(row) and not C.s1_c3t_spec(spec):              # KS4: row 32 must be S1_UA_C3T
        raise Refusal('S1_ROW_SPEC_IS_NOT_S1_UA_C3T')
    ident = C.point_identity(spec)
    key = C.digest(ident)
    eps_pin, eps = _proof(eps_proof, 'EPS', roots)
"""),
("""    bundle = {'schema': C.BUNDLE_SCHEMA, 'identity': ident, 'custody': custody, 'domain': dict(C.DOMAIN),
""",
"""    bundle = {'schema': C.BUNDLE_SCHEMA, 'identity': ident, 'custody': custody, 'domain': C.domain_of_row(row),
"""),
("""        if key not in table:
            raise Refusal('BUNDLE_POINT_NOT_IN_31_POINT_TABLE: ' + key[:16])
""",
"""        if key not in table:                          # KS4: row 32 (S1_UA_C3T), looked up only for a non-table key
            table.update({r['key']: r for r in C.s1_rows() if r['key'] == key})
        if key not in table:
            raise Refusal('BUNDLE_POINT_NOT_IN_31_POINT_TABLE: ' + key[:16])
"""),
("""        deps[key] = C.digest({'dependencies': eps_rec.get('dependencies'), 'producer': eps_rec.get('producer')})
""",
"""        if C.is_s1_row(table[key]):                   # KS4: KS1/KS2 checked, then mapped (one rule for all points)
            if eps_rec.get('producer') != C.canonical_pin('response_producer_ks2'):
                raise Refusal('S1_EPS_RECORD_PRODUCER_IS_NOT_KS2')
            deps[key] = C.digest({'dependencies': C.s1_pins_as_table(eps_rec.get('dependencies')),
                                  'producer': C.canonical_pin('response_producer')})
        else:
            deps[key] = C.digest({'dependencies': eps_rec.get('dependencies'), 'producer': eps_rec.get('producer')})
"""),
("""           'count': len(points), 'complete_31_point_table': len(points) == len(C.POINTS),
""",
"""           'count': len(points), 'complete_31_point_table': all(r['key'] in points for r in C.point_rows()),
"""),
("""    stamp = C.utc_compact()
    rpin = C.write_new(os.path.join(out_root, 'REGISTRY_%02dpts_%s.json' % (len(points), stamp)), reg, out_root)
""",
"""    s1_keys = [k for k in points if C.is_s1_row(table[k])]
    if s1_keys:                                       # KS4: row 32 only
        reg['s1_c3t_points'] = s1_keys
    stamp = C.utc_compact()
    rpin = C.write_new(os.path.join(out_root, 'REGISTRY_%02dpts_%s.json' % (len(points), stamp)), reg, out_root)
"""),
("""           'note': 'DRAFT for root: C1 content and certificate_policy_review are root items (brief 1.5, 6 Q9).'}
""",
"""           'note': 'DRAFT for root: C1 content and certificate_policy_review are root items (brief 1.5, 6 Q9).'}
    if s1_keys:                                       # KS4: the S1_UA_C3T C1 (its own C1; KS5' binds KS5 for it)
        man['s1_c3t_c1_tail_readiness_fields'] = {'certificate_registry': rpin, 'approved_certificate_producers': approved,
                                                  'custody_deriver': C.canonical_pin('custody_ks1'),
                                                  'state_enumerator': C.canonical_pin('state_enumerator')}
        man['s1_c3t_guard'] = C.canonical_pin('guard_ks5')
        man['s1_c3t_wrapper'] = C.canonical_pin('wrapper_s1k3_ks5p')
"""),
("""def real_guard():
    \"\"\"The guard that wrapper v002 L30 loads (path and sha read from the 7a6af535 bytes): b1 9e3fc109.\"\"\"
    g = wrapper_l30_guard_pin()
    return C.load_exact(g['path'], g['sha256'], 's4rc1_verify_guard_l30_c3v003')
""",
"""def real_guard():
    \"\"\"The guard that wrapper v002 L30 loads (path and sha read from the 7a6af535 bytes): b1 9e3fc109.\"\"\"
    g = wrapper_l30_guard_pin()
    return C.load_exact(g['path'], g['sha256'], 's4rc1_verify_guard_l30_c3v003')


def real_guard_s1():
    \"\"\"KS4: the guard the wrapper successor s1k3 c2v002 uses for S1_UA_C3T: KS5.\"\"\"
    path, sha = C.PINS['guard_ks5']
    return C.load_exact(path, sha, 's4rc1_verify_guard_ks5_c2v001')
"""),
("""def c1_policy_gate(c1_ref, registry_ref, *, roots=(C.ART,), canonical_producers=None):
""",
"""def c1_policy_gate(c1_ref, registry_ref, *, roots=(C.ART,), canonical_producers=None, s1=False):
"""),
("""        bad = ([] if r['custody_deriver'] == C.canonical_pin('custody') else
""",
"""        bad = ([] if r['custody_deriver'] == C.canonical_pin('custody_ks1' if s1 else 'custody') else   # KS4: S1 C1 -> KS1
"""),
("""                'guard_sha256': wrapper_l30_guard_pin()['sha256'], 'driver_slot_rule': SLOT_RULE,
""",
"""                'guard_sha256': C.PINS['guard_ks5'][1] if s1 else wrapper_l30_guard_pin()['sha256'],   # KS4: S1 C1 -> KS5
                'driver_slot_rule': SLOT_RULE,
"""),
("""    res = {'row': row['row'], 'label': row['label'], 'key': row['key'], 'wrapper_replica': {'ok': False, 'blockers': []},
           'guard_b1': None}
""",
"""    res = {'row': row['row'], 'label': row['label'], 'key': row['key'], 'wrapper_replica': {'ok': False, 'blockers': []},
           'guard_b1': None}
    s1 = C.is_s1_row(row)
    if s1:                                            # KS4: row 32 replicates KS5' (its 'guard_b1' slot holds KS5's result)
        res['wrapper_replica']['wrapper'] = C.canonical_pin('wrapper_s1k3_ks5p')
        res['guard'] = C.canonical_pin('guard_ks5')
"""),
("""        spec = load_point_spec(row)
        validate_block(spec['numerics'])                                                  # L80
""",
"""        spec = load_point_spec(row)
        if s1 and not C.s1_c3t_spec(spec):
            raise Refusal('S1_ROW_SPEC_IS_NOT_S1_UA_C3T')
        validate_spec_block(spec)                                                         # L80 (KS4: s1k3 L89-102)
"""),
("""        res['guard_b1'] = guard.verify_bundle(bundle_ref, ident, expected_custody=custody,       # L192-194
                                              approved_producer_sha256=[p['sha256'] for p in approved],
                                              phase='prelaunch', required_states=[], **kw)
""",
"""        res['guard_b1'] = guard.verify_bundle(bundle_ref, ident, expected_custody=custody,       # L192-194
                                              approved_producer_sha256=[p['sha256'] for p in approved],
                                              phase='prelaunch', required_states=[], **kw)
        if s1 and res['guard_b1'].get('ok') is True and (bundle.get('domain') or {}).get('K_inverse_kpc') != 3.0:
            res['guard_b1'] = {'ok': False, 'blockers': ['S1_UA_C3T_CERTIFICATE_DOMAIN_K_IS_NOT_THE_KEPT_K (s1k3 L145-147)']}
"""),
("""def verify_registry(registry_ref, rows, *, c1_ref, custody_loader, guard, roots=(C.ART,), guard_roots=None,
                    canonical_producers=None):
""",
"""def verify_registry(registry_ref, rows, *, c1_ref, custody_loader, guard, roots=(C.ART,), guard_roots=None,
                    canonical_producers=None, guard_s1=None):
"""),
("""    out = [verify_point(r, registry, approved=approved, custody_fn=custody_fn, guard=guard, roots=roots,
                        guard_roots=guard_roots, policy_blockers=policy) for r in rows]
""",
"""    s1rows = [r for r in rows if C.is_s1_row(r)]     # KS4: row 32 is checked against the S1 C1 gate (KS1, KS5)
    tr1, policy1, approved1, custody_fn1, g1 = None, [], None, None, None
    if s1rows:
        tr1, policy1 = c1_policy_gate(c1_ref, registry_ref, roots=roots, canonical_producers=canonical_producers, s1=True)
        if not policy1:
            approved1, custody_fn1 = tr1['approved_certificate_producers'], custody_loader(tr1['custody_deriver'])
        g1 = guard_s1 if guard_s1 is not None else real_guard_s1()
    out = [verify_point(r, registry, approved=approved1, custody_fn=custody_fn1, guard=g1, roots=roots,
                        guard_roots=guard_roots, policy_blockers=policy1) if C.is_s1_row(r) else
           verify_point(r, registry, approved=approved, custody_fn=custody_fn, guard=guard, roots=roots,
                        guard_roots=guard_roots, policy_blockers=policy) for r in rows]
"""),
("""    return {'schema': 'S4RC1_C1_REGISTRY_OFFLINE_VERIFY_C3V003', 'utc': C.utc(), 'registry': registry_ref,
            'c1': c1_ref, 'c1_policy_gate': {'ok': not policy, 'blockers': policy, 'approved_certificate_producers': approved,
                                             'custody_deriver': (tr or {}).get('custody_deriver')},
            'generator': generator_pin(), 'guard': wrapper_l30_guard_pin(), 'wrapper': C.canonical_pin('wrapper_q5b1'),
            'points': out, 'ok': not policy and all(x['ok'] for x in out), 'n_ok': sum(x['ok'] for x in out), 'n': len(out),
""",
"""    rep = {'schema': 'S4RC1_C1_REGISTRY_OFFLINE_VERIFY_C3V003', 'utc': C.utc(), 'registry': registry_ref,
            'c1': c1_ref, 'c1_policy_gate': {'ok': not policy, 'blockers': policy, 'approved_certificate_producers': approved,
                                             'custody_deriver': (tr or {}).get('custody_deriver')},
            'generator': generator_pin(), 'guard': wrapper_l30_guard_pin(), 'wrapper': C.canonical_pin('wrapper_q5b1'),
            'points': out, 'ok': ((not policy or (bool(s1rows) and len(s1rows) == len(rows))) and (not policy1)
                                  and all(x['ok'] for x in out)),
            'n_ok': sum(x['ok'] for x in out), 'n': len(out),
"""),
("""                     'the canonical pins; prelaunch certificate_check L80-93 and L140 transcribed; L145-191 EXECUTED from the '
                     '7a6af535 bytes (AST-extracted); the L30 guard (b1 9e3fc109) verify_bundle (L192-194). NOT replicated: '
                     'Context construction (L43-57: driver pin, parent config validation), the sensitivity and other '
                     'prelaunch gates, and the guard007/guard009 fence (R1). Not launch authorization.'}
""",
"""                     'the canonical pins; prelaunch certificate_check L80-93 and L140 transcribed; L145-191 EXECUTED from the '
                     '7a6af535 bytes (AST-extracted); the L30 guard (b1 9e3fc109) verify_bundle (L192-194). NOT replicated: '
                     'Context construction (L43-57: driver pin, parent config validation), the sensitivity and other '
                     'prelaunch gates, and the guard007/guard009 fence (R1). Not launch authorization.'}
    if s1rows:                                        # KS4: row 32 only
        rep['c1_policy_gate_s1_c3t'] = {'ok': not policy1, 'blockers': policy1, 'approved_certificate_producers': approved1,
                                        'custody_deriver': (tr1 or {}).get('custody_deriver'), 'guard': C.canonical_pin('guard_ks5'),
                                        'wrapper': C.canonical_pin('wrapper_s1k3_ks5p')}
    return rep
"""),
("""        rep = verify_registry(ref, C.select_points(ns.points), c1_ref=c1_ref, custody_loader=real_custody_fn,
                              guard=real_guard())
""",
"""        rep = verify_registry(ref, C.select_points(ns.points), c1_ref=c1_ref, custody_loader=real_custody_fn,
                              guard=real_guard())    # KS4: KS5 is loaded only if row 32 is selected
"""),
]

# ===================================================================================================== KS6 lo_core
EDITS['KS6CORE'] = [
("""\"\"\"Point-scoped LO evidence from saved TailState arrays or reviewed source caps.
""",
"""\"\"\"KS6 lo_core (ks_k3_chain_c2 c2v001; root A160): lo_core_r5_cx2v001 (12d36305) accepting K=3 states for S1_UA_C3T only.

The response producer is KS2 (custody KS1). For an S1_UA_C3T spec (KS1's gate: C3T label AND CB C3T grid) the saved
state's kept region must be the K=3 cube and its B1 shell edges must start at 3 (12d36305 L85-86, L104 required 4);
produce_current_lo is otherwise 12d36305's code. Every other spec goes to the unchanged 12d36305 module object (P, by
path and sha): its records, producer pins included, are 12d36305's. The retired prelaunch conditional path and the
legacy diagnostic are not extended: S1_UA_C3T is refused there, every other spec is 12d36305's. validate_tail_arrays and
recompute_b1 take kept_k (default 4.0, 12d36305's behaviour). The 12d36305 text follows.

Point-scoped LO evidence from saved TailState arrays or reviewed source caps.
"""),
("""HERE = Path(__file__).resolve().parent
RESPONSE_PATH = HERE / 'point_response_producer_cx2v002.py'
if hashlib.sha256(RESPONSE_PATH.read_bytes()).hexdigest()!='a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231':raise ValueError('r5 response pin mismatch')
sp = importlib.util.spec_from_file_location('cx2_lo_point_response_r5', RESPONSE_PATH)
""",
"""HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point')   # KS6: 12d36305's folder
PREDECESSOR = (HERE / 'lo_core_r5_cx2v001.py', '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e')
RESPONSE_PATH = Path('@@KSDIR@@/point_response_producer_cx2v002_ks2_c2v001.py')   # KS6: KS2
if hashlib.sha256(RESPONSE_PATH.read_bytes()).hexdigest()!='@@SHA_KS2@@':raise ValueError('r5 response pin mismatch')
sp = importlib.util.spec_from_file_location('ks6_lo_point_response_ks2', RESPONSE_PATH)
"""),
("""CU, CC = PR.CU, PR.CC
""",
"""CU, CC = PR.CU, PR.CC
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest() != PREDECESSOR[1]:
    raise ValueError('KS6: lo_core 12d36305 pin mismatch')
_psp = importlib.util.spec_from_file_location('ks6_predecessor_lo_core_r5_cx2v001', PREDECESSOR[0])
P = importlib.util.module_from_spec(_psp)          # KS6: 12d36305, unchanged; every non-S1_UA_C3T spec runs its code
sys.modules[_psp.name] = P
_psp.loader.exec_module(P)
"""),
("""def validate_tail_arrays(arrays, record):
    \"\"\"Validate tensor arrays before any arithmetic; cube/cylinder only.\"\"\"
    if record.get('empty') is not False:
        raise ValueError('nonempty saved state required')
    if record['kept'].get('shape') != 'cube' or record['kept'].get('K_inverse_kpc') != 4.0:
        raise ValueError('K4 cube required')
""",
"""def validate_tail_arrays(arrays, record, kept_k=4.0):
    \"\"\"Validate tensor arrays before any arithmetic; cube/cylinder only. KS6: kept_k 3.0 for S1_UA_C3T only.\"\"\"
    if record.get('empty') is not False:
        raise ValueError('nonempty saved state required')
    if record['kept'].get('shape') != 'cube' or record['kept'].get('K_inverse_kpc') != kept_k:
        raise ValueError('K4 cube required' if kept_k == 4.0 else 'K3 cube required (S1_UA_C3T)')
"""),
("""    if edges.ndim != 1 or np.any(np.diff(edges) <= 0) or edges[0] != 4 or stored.shape != (len(edges) - 1, 3):
""",
"""    if edges.ndim != 1 or np.any(np.diff(edges) <= 0) or edges[0] != kept_k or stored.shape != (len(edges) - 1, 3):
"""),
("""def recompute_b1(arrays, record, U, *, chunk=64):
    \"\"\"Recompute stored B1 independently from P/F and the module angular mask.\"\"\"
    edges = validate_tail_arrays(arrays, record)
""",
"""def recompute_b1(arrays, record, U, *, chunk=64, kept_k=4.0):
    \"\"\"Recompute stored B1 independently from P/F and the module angular mask.\"\"\"
    edges = validate_tail_arrays(arrays, record, kept_k)
"""),
("""                       context=None, progress=None):
    start = time.monotonic()
    ctx = context or PR.point_context(spec)
    obj = reference(state_ref, schema=STATE_SCHEMA)
""",
"""                       context=None, progress=None):
    if not CU.s1_c3t_spec(spec):                      # KS6: 12d36305's own code path
        return P.produce_current_lo(spec, state_ref, expected_state=expected_state,
                                    trusted_source_producers=trusted_source_producers,
                                    trusted_review_hashes=trusted_review_hashes, settings=settings,
                                    shell_ranges=shell_ranges, context=context, progress=progress)
    start = time.monotonic()
    ctx = context or PR.point_context(spec)
    obj = reference(state_ref, schema=STATE_SCHEMA)
"""),
("""    B1, b1check = recompute_b1(arrays, record, U)
""",
"""    B1, b1check = recompute_b1(arrays, record, U, kept_k=float(PR.kept_k(spec)))   # KS6: the K=3 cube, edges from 3
"""),
("""                           settings='registered', shell_ranges=None, context=None, progress=None):
    start = time.monotonic()
    ctx = context or PR.point_context(spec)
    rec = base(ctx, 'PRELAUNCH_CONDITIONAL_SOURCE_ENVELOPE')
""",
"""                           settings='registered', shell_ranges=None, context=None, progress=None):
    if not CU.s1_c3t_spec(spec):                      # KS6: 12d36305's own code path
        return P.produce_conditional_lo(spec, cap_ref, review_ref=review_ref, trusted_review_hashes=trusted_review_hashes,
                                        settings=settings, shell_ranges=shell_ranges, context=context, progress=progress)
    raise ValueError('KS6: the retired prelaunch conditional LO path (A134 Q1/Q5) is not extended to S1_UA_C3T')
    start = time.monotonic()
    ctx = context or PR.point_context(spec)
    rec = base(ctx, 'PRELAUNCH_CONDITIONAL_SOURCE_ENVELOPE')
"""),
("""    Geometry must remain exactly the legacy DDO154 registered distance.
    \"\"\"
    ctx = context or PR.point_context(spec)
""",
"""    Geometry must remain exactly the legacy DDO154 registered distance.
    \"\"\"
    if not CU.s1_c3t_spec(spec):                      # KS6: 12d36305's own code path
        return P.saved_b1_diagnostic(spec, legacy_ref, settings=settings, shell_ranges=shell_ranges, context=context)
    raise ValueError('KS6: the legacy saved-source diagnostic is not extended to S1_UA_C3T')
    ctx = context or PR.point_context(spec)
"""),
]

# ===================================================================================================== KS6 lo_config
EDITS['KS6CFG'] = [
("""\"\"\"Successor of LO v001: additionally derive exact state configuration/grid.
""",
"""\"\"\"KS6 lo_config (ks_k3_chain_c2 c2v001; root A160): lo_config_r5_cx2v001 (6654d93c) over the KS6 lo_core.

Needed by KS6 (deviation from the KS list, disclosed): the c3v003 adapter runs this module's validate_current_config
(adapter L553), whose L51 builds the K=4 kept region, so no K=3 state can pass without it. For an S1_UA_C3T spec
(KS1's gate) the wanted kept region is the K=3 cube (kept K from the spec's grid, KS2 kept_k); everything else in
validate_current_config and produce_current_lo is 6654d93c's code over the KS6 lo_core (V1) and KS2. Every other
spec goes to the unchanged 6654d93c module object (P, by path and sha). The 6654d93c text follows.

Successor of LO v001: additionally derive exact state configuration/grid.
"""),
("""HERE = Path(__file__).resolve().parent
BASE = HERE/'lo_core_r5_cx2v001.py'
BASE_SHA = '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e'
""",
"""HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point')   # KS6: 6654d93c's folder
PREDECESSOR = (HERE/'lo_config_r5_cx2v001.py', '6654d93c0241afd230d90bfcf327f16c22dd24c4da1d3eea72602212c2b6ae5a')
BASE = Path('@@KSDIR@@/lo_core_r5_cx2v001_ks6_c2v001.py')   # KS6: the lo_core successor
BASE_SHA = '@@SHA_KS6CORE@@'
"""),
("""sp=importlib.util.spec_from_file_location('cx2_lo_core_v001',BASE)
""",
"""sp=importlib.util.spec_from_file_location('ks6_lo_core_ks6_c2v001',BASE)
"""),
("""if CU.sha(PR.__file__) != 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231':
    raise ValueError('point response core pin mismatch')
""",
"""if CU.sha(PR.__file__) != '@@SHA_KS2@@':
    raise ValueError('point response core pin mismatch')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest() != PREDECESSOR[1]:
    raise ValueError('KS6: lo_config 6654d93c pin mismatch')
_psp=importlib.util.spec_from_file_location('ks6_predecessor_lo_config_r5_cx2v001',PREDECESSOR[0])
P=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=P;_psp.loader.exec_module(P)   # KS6: 6654d93c, unchanged
"""),
("""def validate_current_config(spec, record, arrays, U):
    raw=copy.deepcopy(spec['numerics']['uv_tail'])
""",
"""def validate_current_config(spec, record, arrays, U):
    if not CU.s1_c3t_spec(spec):                      # KS6: 6654d93c's own code path
        return P.validate_current_config(spec, record, arrays, U)
    raw=copy.deepcopy(spec['numerics']['uv_tail'])
"""),
("""    wanted_kept=U.kept_region(record['stage_kind'],spec['numerics']['truncation'],4/U.KPC_M)
""",
"""    wanted_kept=U.kept_region(record['stage_kind'],spec['numerics']['truncation'],PR.kept_k(spec)/U.KPC_M)   # KS6: kept K 3
"""),
("""def produce_current_lo(spec,state_ref,**kwargs):
    ctx=kwargs.pop('context',None) or PR.point_context(spec)
""",
"""def produce_current_lo(spec,state_ref,**kwargs):
    if not CU.s1_c3t_spec(spec):                      # KS6: 6654d93c's own code path
        return P.produce_current_lo(spec,state_ref,**kwargs)
    ctx=kwargs.pop('context',None) or PR.point_context(spec)
"""),
]

# ===================================================================================================== KS6 adapter
EDITS['KS6AD'] = [
("""\"\"\"S4-R-C1 per-state LO proof adapter c3v003 (A134: Q2, Q3, Q4, Q5). Claude3 builds it; Codex1 reviews it in one pass (0688).
""",
"""\"\"\"KS6 adapter (ks_k3_chain_c2 c2v001; root A160): lo_state_proof_adapter_c3v003 (211a3220) for S1_UA_C3T K=3 states.

adapt_call_lo and main() hand every spec that is not S1_UA_C3T (the C3T label AND the CB C3T grid, bitwise) to the
unchanged 211a3220 module object (loaded lazily, after F9's root gate, by path and sha), so its records, self-pin
included, are 211a3220's. For S1_UA_C3T the adapter is 211a3220's code with: custody KS1, lo_config/lo_core KS6, and
the point's rho contract from its identity (_rho_contract): coverage [3, 182], the 10-shell partition from [3,4], the
KS2 response producer and the KS6 lo_core (check_rho_record, L573); every other identity keeps the c3v003 constants.
The inventory enumerator stays the b1 enumerator 4ca7f364 (its custody is 6810b7c3: open item for root). The c3v003
text follows.

S4-R-C1 per-state LO proof adapter c3v003 (A134: Q2, Q3, Q4, Q5). Claude3 builds it; Codex1 reviews it in one pass (0688).
"""),
("""import datetime
import hashlib
""",
"""import copy
import datetime
import hashlib
"""),
("""import os
import struct
""",
"""import os
import re
import struct
"""),
("""ENUMERATOR_SHA = '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'   # V02: b1 enumerator consumed_states_b1_c2v001
""",
"""ENUMERATOR_SHA = '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'   # V02: b1 enumerator consumed_states_b1_c2v001
# KS6 (A160): the predecessor and the S1_UA_C3T (kept K 3) chain. Every other identity keeps the c3v003 pins above.
PREDECESSOR = (ART + '/s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py',
               '211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c')
CUSTODY_KS1 = ('@@KSDIR@@/custody_cx2v002_ks1_c2v001.py', '@@SHA_KS1@@')
LO_CONFIG_KS6 = ('@@KSDIR@@/lo_config_r5_cx2v001_ks6_c2v001.py', '@@SHA_KS6CFG@@')
LO_CORE_KS6 = ('@@KSDIR@@/lo_core_r5_cx2v001_ks6_c2v001.py', '@@SHA_KS6CORE@@')
RESPONSE_KS2_SHA = '@@SHA_KS2@@'
""" + CB_PIN_LINES + S1_LABEL_LINE),
("""RHO_PARTITION = [[4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0],
                 [32.0, 64.0], [64.0, 128.0], [128.0, 182.0]]
""",
"""RHO_PARTITION = [[4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0],
                 [32.0, 64.0], [64.0, 128.0], [128.0, 182.0]]
RHO_COVERAGE_S1 = [3.0, 182.0]                                  # KS6: S1_UA_C3T (KS2 shell_plan at kept K 3)
RHO_PARTITION_S1 = [[3.0, 4.0]] + RHO_PARTITION
"""),
("""def check_rho_record(rec, *, read_raw, identity=None, custody=None, point_sha256=None):
""",
"""_CB = {}


def _cb_c3t_grid():
    if not _CB:
        with open(CB_PIN['path'], 'rb') as f:
            raw = f.read()
        if hashlib.sha256(raw).hexdigest() != CB_PIN['sha256']:
            raise Refusal('CB case block: sha256 mismatch')
        _CB['C3T'] = json.loads(raw)['cases']['C3T']['normalized_spec_equal']['/numerics']['composite_grid_spec']
    return copy.deepcopy(_CB['C3T'])


def _s1_c3t_numerics(numerics):
    \"\"\"KS6: composite_grid_spec == CB C3T bitwise. A grid whose last break is not 3 never reads CB.\"\"\"
    try:
        grid = numerics.get('composite_grid_spec')
        if grid['breaks_inverse_kpc'][-1] != 3:
            return False
        return canonical(grid) == canonical(_cb_c3t_grid())
    except (AttributeError, KeyError, IndexError, TypeError, ValueError):
        return False


def _s1_c3t_spec(spec):
    \"\"\"KS6 gate (as KS1's): the S1 C3T label AND the CB C3T grid.\"\"\"
    lab = spec.get('label') if isinstance(spec, dict) else None
    return (isinstance(lab, str) and S1_C3T_LABEL.fullmatch(lab) is not None
            and _s1_c3t_numerics(spec.get('numerics')))


def _rho_contract(identity):
    \"\"\"KS6: (coverage, partition, response sha, lo_core sha, kept K) of a point. The CB C3T grid (S1_UA_C3T; its
    custody, and so every record, comes from KS1, which admits it only with the S1 label) takes K 3; every other
    identity, c3v003's.\"\"\"
    if isinstance(identity, dict) and _s1_c3t_numerics(identity.get('numerics')):
        return RHO_COVERAGE_S1, RHO_PARTITION_S1, RESPONSE_KS2_SHA, LO_CORE_KS6[1], 3
    return RHO_COVERAGE, RHO_PARTITION, RESPONSE_SHA, LO_CORE[1], 4


_PRED = {}


def _predecessor():
    \"\"\"KS6: 211a3220, unchanged, loaded on first use only (after the F9 root gate in main).\"\"\"
    if 'm' not in _PRED:
        _PRED['m'] = _load_exact(PREDECESSOR[0], PREDECESSOR[1], 'ks6_predecessor_lo_state_proof_adapter_c3v003')
    return _PRED['m']


def check_rho_record(rec, *, read_raw, identity=None, custody=None, point_sha256=None):
"""),
("""    if rec.get('coverage_complete') is not True or rec.get('required_coverage_inverse_kpc') != RHO_COVERAGE:
        raise Refusal('RHO_COVERAGE_NOT_4_TO_182')
    if [s.get('range_inverse_kpc') for s in rec.get('shells') or [] if isinstance(s, dict)] != RHO_PARTITION:
        raise Refusal('RHO_PARTITION_NOT_REGISTERED')
    producer = rec.get('producer')
    if not _is_pin(producer) or producer['sha256'] != RESPONSE_SHA:
        raise Refusal('RHO_PRODUCER_NOT_RESPONSE_A1DCDEA8')
    try:
        read_raw(dict(producer))                                  # F5: the producer's bytes are read (sha from bytes)
    except Exception as exc:
        raise Refusal('RHO_PRODUCER_BYTES_NOT_A1DCDEA8 (F5: %s: %s: %s)' % (producer['path'], type(exc).__name__, exc))
""",
"""    cov, part, resp, _core, k = _rho_contract(rec.get('identity'))   # KS6: the K=3 contract for S1_UA_C3T only
    if rec.get('coverage_complete') is not True or rec.get('required_coverage_inverse_kpc') != cov:
        raise Refusal('RHO_COVERAGE_NOT_4_TO_182' if k == 4 else 'RHO_COVERAGE_NOT_3_TO_182')
    if [s.get('range_inverse_kpc') for s in rec.get('shells') or [] if isinstance(s, dict)] != part:
        raise Refusal('RHO_PARTITION_NOT_REGISTERED')
    producer = rec.get('producer')
    if not _is_pin(producer) or producer['sha256'] != resp:
        raise Refusal('RHO_PRODUCER_NOT_RESPONSE_A1DCDEA8' if k == 4 else 'RHO_PRODUCER_NOT_RESPONSE_KS2')
    try:
        read_raw(dict(producer))                                  # F5: the producer's bytes are read (sha from bytes)
    except Exception as exc:
        raise Refusal('RHO_PRODUCER_BYTES_NOT_%s (F5: %s: %s: %s)' % ('A1DCDEA8' if k == 4 else 'KS2', producer['path'],
                                                                       type(exc).__name__, exc))
"""),
("""            state['cu'] = _load_exact(CUSTODY[0], CUSTODY[1], 's4rc1_proofside_state_custody_cx2v002')
""",
"""            state['cu'] = _load_exact(CUSTODY_KS1[0], CUSTODY_KS1[1], 's4rc1_proofside_state_custody_ks1_c2v001')   # KS6
"""),
("""            cfg = _load_exact(LO_CONFIG[0], LO_CONFIG[1], 's4rc1_proofside_lo_config_r5_cx2v001')
            v1 = cfg.V1
            if getattr(v1, '__file__', None) != LO_CORE[0] or cu().sha(v1.__file__) != LO_CORE[1]:
                raise Refusal('LO_CORE_NOT_THE_UNCHANGED_12D36305')
""",
"""            cfg = _load_exact(LO_CONFIG_KS6[0], LO_CONFIG_KS6[1], 's4rc1_proofside_lo_config_ks6_c2v001')   # KS6
            v1 = cfg.V1
            if getattr(v1, '__file__', None) != LO_CORE_KS6[0] or cu().sha(v1.__file__) != LO_CORE_KS6[1]:
                raise Refusal('LO_CORE_NOT_THE_KS6_LO_CORE')
"""),
("""        if (core.get('producer') or {}).get('sha256') != LO_CORE[1] or (core.get('response_producer') or {}).get('sha256') != RESPONSE_SHA:
            raise Refusal('CORE_PRODUCER_NOT_UNCHANGED_12D36305_A1DCDEA8')
""",
"""        _cov, _part, resp, core_sha, k = _rho_contract(details['identity'])     # KS6: KS6 lo_core and KS2 at K 3
        if (core.get('producer') or {}).get('sha256') != core_sha or (core.get('response_producer') or {}).get('sha256') != resp:
            raise Refusal('CORE_PRODUCER_NOT_UNCHANGED_12D36305_A1DCDEA8' if k == 4 else 'CORE_PRODUCER_NOT_KS6_LO_CORE_AND_KS2')
"""),
("""    \"\"\"Public entry (root operates it at post-run acceptance). INCOMPLETE unless every gate above holds.\"\"\"
    return _adapt_call(spec, call_dir=call_dir, result=result, inventory=inventory, bundle_ref=bundle_ref,
""",
"""    \"\"\"Public entry (root operates it at post-run acceptance). INCOMPLETE unless every gate above holds.\"\"\"
    if not _s1_c3t_spec(spec):                        # KS6: 211a3220's own entry, unchanged
        return _predecessor().adapt_call_lo(spec, call_dir=call_dir, result=result, inventory=inventory, bundle_ref=bundle_ref,
                                            state_inputs=state_inputs, root_ruling_refs=root_ruling_refs,
                                            approved_producer_sha256=approved_producer_sha256,
                                            trusted_source_producers=trusted_source_producers,
                                            trusted_row_policy_review_sha256=trusted_row_policy_review_sha256,
                                            out_root=out_root)
    return _adapt_call(spec, call_dir=call_dir, result=result, inventory=inventory, bundle_ref=bundle_ref,
"""),
("""        spec = env.read_pin(args['spec_ref'])
""",
"""        spec = env.read_pin(args['spec_ref'])
        if not _s1_c3t_spec(spec):                    # KS6: 211a3220's own CLI, unchanged
            return _predecessor().main(argv)
"""),
]

# ===================================================================================================== KS6 handoff
EDITS['KS6HO'] = [
("""\"\"\"Q2 acceptance input side, part 3 (A134; rulings 56774ba7 Q2, Q3, Q4(c), Q5 readings, Q10): the acceptance handoff.
""",
"""\"\"\"KS6 handoff (ks_k3_chain_c2 c2v001; root A160): acceptance_handoff_c2v004 (5ff464cc) with the KS6 LO adapter for
S1_UA_C3T only.

accept_call hands every spec that is not S1_UA_C3T (the C3T label AND the CB C3T grid, bitwise) to the unchanged
5ff464cc module object (P, by path and sha): its records, the handoff pin and LO_ADAPTER 211a3220 included, are
5ff464cc's. For S1_UA_C3T the handoff is 5ff464cc's code with LO_ADAPTER_KS6 (the KS6 adapter) in place of LO_ADAPTER.
load_deps accepts either adapter pin (deps carry no spec); each accept_call path checks its own. Root supplies the other
deps, as before; for S1_UA_C3T they must be K=3-capable (lo_core KS6, guard KS5; enumerator/evidence/SRB successors
are open items for root). The 5ff464cc text follows.

Q2 acceptance input side, part 3 (A134; rulings 56774ba7 Q2, Q3, Q4(c), Q5 readings, Q10): the acceptance handoff.
"""),
("""import hashlib
import importlib.util
import json
import sys
""",
"""import copy
import hashlib
import importlib.util
import json
import re
import sys
"""),
("""B1_EVIDENCE = {'path': str(ART / 's4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py'),
""",
"""# KS6 (A160): the KS6 adapter, for S1_UA_C3T only; 5ff464cc itself, for every other spec.
LO_ADAPTER_KS6 = {'path': '@@KSDIR@@/lo_state_proof_adapter_c3v003_ks6_c2v001.py',
                  'sha256': '@@SHA_KS6AD@@', 'entry': 'adapt_call_lo'}
PREDECESSOR = {'path': str(ART / 's4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py'),
               'sha256': '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'}
""" + CB_PIN_LINES + S1_LABEL_LINE + """B1_EVIDENCE = {'path': str(ART / 's4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py'),
"""),
("""def load_deps(pins):
""",
"""_CB = {}


def _s1_c3t_spec(spec):
    \"\"\"KS6 gate (as KS1's): the S1 C3T label AND composite_grid_spec == CB C3T bitwise; other labels never read CB.\"\"\"
    lab = spec.get('label') if isinstance(spec, dict) else None
    if not (isinstance(lab, str) and S1_C3T_LABEL.fullmatch(lab) is not None):
        return False
    try:
        grid = spec['numerics']['composite_grid_spec']
        if not _CB:
            raw = Path(CB_PIN['path']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != CB_PIN['sha256']:
                raise ValueError('CB case block: sha256 mismatch')
            _CB['C3T'] = json.loads(raw)['cases']['C3T']['normalized_spec_equal']['/numerics']['composite_grid_spec']
        return canonical(grid) == canonical(copy.deepcopy(_CB['C3T']))
    except (KeyError, TypeError, ValueError):
        return False


def load_deps(pins):
"""),
("""    if pins.get('lo_adapter') != LO_ADAPTER:
        raise ValueError('LO_ADAPTER_PIN_NOT_A138 (the handoff calls only %s %s)' % (LO_ADAPTER['path'], LO_ADAPTER['sha256']))
""",
"""    if pins.get('lo_adapter') not in (LO_ADAPTER, LO_ADAPTER_KS6):   # KS6: accept_call checks the one its spec needs
        raise ValueError('LO_ADAPTER_PIN_NOT_A138 (the handoff calls only %s %s)' % (LO_ADAPTER['path'], LO_ADAPTER['sha256']))
"""),
("""def lo_adapter_problem(deps):
    \"\"\"A138 V01(a): the callable is the pinned adapt_call_lo, compiled from the pinned file, whose bytes still match.\"\"\"
    fn = deps.get('lo_adapter')
    if (deps.get('pins') or {}).get('lo_adapter') != LO_ADAPTER:
        return 'LO_ADAPTER_PIN_NOT_A138 (required %s %s)' % (LO_ADAPTER['path'], LO_ADAPTER['sha256'])
    if getattr(fn, '__name__', None) != LO_ADAPTER['entry'] or \\
            getattr(getattr(fn, '__code__', None), 'co_filename', None) != LO_ADAPTER['path']:
        return 'LO_ADAPTER_CALLABLE_NOT_THE_PINNED_ENTRY'
    if sha_file(LO_ADAPTER['path']) != LO_ADAPTER['sha256']:
        return 'LO_ADAPTER_BYTES_CHANGED'
    return None
""",
"""def lo_adapter_problem(deps, want=LO_ADAPTER):
    \"\"\"A138 V01(a): the callable is the pinned adapt_call_lo, compiled from the pinned file, whose bytes still match.
    KS6: want is LO_ADAPTER_KS6 on the S1_UA_C3T path.\"\"\"
    fn = deps.get('lo_adapter')
    if (deps.get('pins') or {}).get('lo_adapter') != want:
        return 'LO_ADAPTER_PIN_NOT_A138 (required %s %s)' % (want['path'], want['sha256'])
    if getattr(fn, '__name__', None) != want['entry'] or \\
            getattr(getattr(fn, '__code__', None), 'co_filename', None) != want['path']:
        return 'LO_ADAPTER_CALLABLE_NOT_THE_PINNED_ENTRY'
    if sha_file(want['path']) != want['sha256']:
        return 'LO_ADAPTER_BYTES_CHANGED'
    return None
"""),
("""                initial_rings_ref=None, final_next_gas_ref=None):
    t0 = time.monotonic()
""",
"""                initial_rings_ref=None, final_next_gas_ref=None):
    if not _s1_c3t_spec(spec):                        # KS6: 5ff464cc's own code path
        return _predecessor().accept_call(call_dir=call_dir, spec=spec, deps=deps, policy=policy, records_dir=records_dir,
                                          tailstate_dir=tailstate_dir, mode=mode, wrapper_context=wrapper_context,
                                          initial_rings_ref=initial_rings_ref, final_next_gas_ref=final_next_gas_ref)
    t0 = time.monotonic()
"""),
("""        bad = lo_adapter_problem(deps)            # v003: A138 V01(a), before anything is read
""",
"""        bad = lo_adapter_problem(deps, LO_ADAPTER_KS6)   # v003: A138 V01(a), before anything is read (KS6 adapter)
"""),
("""            rec['lo_adapter'] = {'pin': dict(LO_ADAPTER), 'call_record': store.put('LO_ADAPTER_CALL_RECORD.json', lo_call),
""",
"""            rec['lo_adapter'] = {'pin': dict(LO_ADAPTER_KS6), 'call_record': store.put('LO_ADAPTER_CALL_RECORD.json', lo_call),
"""),
("""            rec['lo_adapter'] = {'pin': dict(LO_ADAPTER), 'call_record': None, 'blockers': lo_call['blockers']}
""",
"""            rec['lo_adapter'] = {'pin': dict(LO_ADAPTER_KS6), 'call_record': None, 'blockers': lo_call['blockers']}
"""),
("""def receipt_ok(receipt_ref, result_sha):
""",
"""_PRED = {}


def _predecessor():
    \"\"\"KS6: 5ff464cc, unchanged, by path and sha (loaded on first use).\"\"\"
    if 'm' not in _PRED:
        _PRED['m'] = load_pinned(PREDECESSOR, 'ks6_predecessor_acceptance_handoff_c2v004')
    return _PRED['m']


def receipt_ok(receipt_ref, result_sha):
"""),
]


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def render(key, shas, ksdir):
    path, want = PRED[key]
    with open(path, 'rb') as f:
        raw = f.read()
    if sha256(raw) != want:
        raise SystemExit('PREDECESSOR_PIN_MISMATCH %s %s' % (key, path))
    text = raw.decode('utf-8')
    for i, (old, new) in enumerate(EDITS[key]):
        n = text.count(old)
        if n != 1:
            raise SystemExit('EDIT_NOT_EXACTLY_ONCE %s #%d (%d matches): %r' % (key, i, n, old[:120]))
        text = text.replace(old, new, 1)
    text = text.replace('@@KSDIR@@', ksdir)
    for name, s in shas.items():
        text = text.replace('@@SHA_%s@@' % name, s)
    if '@@' in text:
        raise SystemExit('UNRESOLVED_PLACEHOLDER %s: %s' % (key, text[text.index('@@'):text.index('@@') + 40]))
    return raw.decode('utf-8'), text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--target-dir', required=True)
    ap.add_argument('--final', action='store_true')
    a = ap.parse_args()
    ksdir = os.path.realpath(a.target_dir)
    if not ksdir.startswith(ART + '/ks_k3_chain_c2'):
        raise SystemExit('target must be ks_k3_chain_c2 or a folder under it')
    os.makedirs(os.path.join(ksdir, 'diffs'), exist_ok=True)
    shas, out = {}, []
    for key in ORDER:
        old, new = render(key, shas, ksdir)
        data = new.encode('utf-8')
        p = os.path.join(ksdir, NAME[key])
        with open(p, 'xb' if a.final else 'wb') as f:
            f.write(data)
        shas[key] = sha256(data)
        diff = ''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile=PRED[key][0],
                                            tofile=p, n=2))
        dp = os.path.join(ksdir, 'diffs', 'DIFF_%s.diff' % NAME[key][:-3])
        with open(dp, 'xb' if a.final else 'wb') as f:
            f.write(diff.encode('utf-8'))
        out.append({'id': key, 'successor': {'path': p, 'sha256': shas[key]},
                    'predecessor': {'path': PRED[key][0], 'sha256': PRED[key][1]},
                    'edits': len(EDITS[key]), 'diff': {'path': dp, 'sha256': sha256(diff.encode('utf-8'))}})
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
