"""G-wave build (ks_k3_chain_c2 G-wave c2v001; root A175, A176): every successor is its predecessor's bytes with
exact-once edits, as the wave-1 build (build_ks_chain_c2v001.py) does.

  python3 -I -B build_gwave_c2v001.py --target-dir DIR [--final]

Each edit is (old, new) and must match the predecessor text exactly once, so the DIFF of every successor is exactly the
listed edits. Successor shas are computed from the written bytes in dependency order and substituted where a later
successor pins an earlier one (@@SHA_<name>@@). @@KSDIR@@ is the wave-1 folder (ks_k3_chain_c2: KS1-KS6 live there);
@@GWDIR@@ is the target directory of this build. Every file is written by exclusive create ('xb'): a development build
goes to a NEW folder under ks_k3_chain_c2/dev/; --final requires the target to be ks_k3_chain_c2 itself. A DIFF per
successor goes to <target>/diffs/. Every predecessor and every wave-1 successor pin is checked from bytes first. Nothing
else is read or written. Hashes from bytes.
"""
import argparse
import difflib
import hashlib
import json
import os

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
KSDIR = ART + '/ks_k3_chain_c2'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
B1 = ART + '/s4_acceptance_c2/offset_b1'
PS = ART + '/s4rc1_c3/proof_side_c3v003'
CB_PIN_LINES = ("CB_PIN = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/"
                "CASE_BLOCK_V007_C4V001.json',\n"
                "          'sha256': '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'}\n")
S1_LABEL_LINE = "S1_C3T_LABEL = re.compile(r'S1 transfer test C3T at u_A theta [0-9a-f]{16}; base [0-9a-f]{8}')\n"

# Wave-1 successors the G-wave pins (verified from bytes before anything is written).
WAVE1 = {
    'KS1': ('custody_cx2v002_ks1_c2v001.py', 'ad020470aee354201ab6c68926784d75d3ebe2e16628323d49280bd2eb18aea6'),
    'KS2': ('point_response_producer_cx2v002_ks2_c2v001.py', '99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7'),
    'KS3C': ('s4rc1_common_c3v004_ks3_c2v001.py', '736d2e7e26c6e6f6325796ea83774682a82f2a045a5f6e3f0ae13358725b1656'),
    'KS3R': ('cp1_runner_c3v004_ks3_c2v001.py', '54595c2d68e63e82378e5ca29f7aa48a19fe6c919f8c8775d2ff4d47fbc41730'),
    'KS4': ('registry_assembler_c3v004_ks4_c2v001.py', '080ed1718908948cb1cfac96a7505a19b2e1741e8742055858cc9037ebbf8cad'),
    'KS5': ('certificate_guard_b1_ks5_c2v001.py', 'e394ae94c6f48ff9e0919e9b186103d2f7c5b00077967579029e8404a62215d6'),
    'KS5P': ('calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002.py', '66560a6a8335d36eff8b4ec58ef780445dc8c6fa21088712e334311bd6fce1eb'),
    'KS6CORE': ('lo_core_r5_cx2v001_ks6_c2v001.py', '2cf7c59790638cc1595a615b226143a5a3eb74e713001d85db4d469edf0b2b2f'),
    'KS6CFG': ('lo_config_r5_cx2v001_ks6_c2v001.py', '510ff07b9557c3829063fe25fe127dc0477a0bfdace5627d84f61aba8b256a2b'),
    'KS6AD': ('lo_state_proof_adapter_c3v003_ks6_c2v001.py', '8fa371a719b41c174175942308ca64bebe40fb1e0d42b99ae27def939cbe6c33'),
    'KS6HO': ('acceptance_handoff_c2v004_ks6_c2v001.py', '6642d2090d7f0801c1eeb68fcb2c6304616030370cdc15047719f653718d4132'),
}
PRED = {
    'G3A': (CERT + '/gq_geometry_r5_cx2v001.py', 'c6ffb338fd7e87bca0028afcf8c1b6c0ae52b8d89823bdcaded69ce798305d85'),
    'G3B': (CERT + '/gq_producer_cx2v005.py', '2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd'),
    'G3C': (B1 + '/gq_producer_b1_c2v001.py', '3e668a2b04288ce4ff4f95b582412ceb4aecf2c908516b97e84f4b1d6d42c3c5'),
    'G4': (CERT + '/point_response_admission_adapter_cx2v003.py', '4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372'),
    'G1': (PS + '/lo_slot_proof_c3v003.py', 'cd10cd59df44d7b79f3c3aa7ba88998d94c7292c4c2656e09bbbe16ded01bca3'),
    'G6A': (CERT + '/execution_graph_cx2v002.py', '6d59f1d06e7c69e15e8d9766fa1776da2b0603d16febf4406c96157d77019258'),
    'G6B': (B1 + '/current_source_evidence_b1_c2v001.py', '7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce'),
    'G6C': (B1 + '/consumed_states_b1_c2v001.py', '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'),
    'G2': (PS + '/srb_rot_adapter_c3v003.py', '08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a'),
    'KS5PP': (KSDIR + '/' + WAVE1['KS5P'][0], WAVE1['KS5P'][1]),
    'KS3C2': (KSDIR + '/' + WAVE1['KS3C'][0], WAVE1['KS3C'][1]),
    'KS3R2': (KSDIR + '/' + WAVE1['KS3R'][0], WAVE1['KS3R'][1]),
    'KS42': (KSDIR + '/' + WAVE1['KS4'][0], WAVE1['KS4'][1]),
    'KS6AD2': (KSDIR + '/' + WAVE1['KS6AD'][0], WAVE1['KS6AD'][1]),
    'KS6HO2': (KSDIR + '/' + WAVE1['KS6HO'][0], WAVE1['KS6HO'][1]),
}
NAME = {
    'G3A': 'gq_geometry_r5_cx2v001_g3_c2v001.py',
    'G3B': 'gq_producer_cx2v005_g3_c2v001.py',
    'G3C': 'gq_producer_b1_c2v001_g3_c2v001.py',
    'G4': 'point_response_admission_adapter_cx2v003_g4_c2v001.py',
    'G1': 'lo_slot_proof_c3v003_g1_c2v001.py',
    'G6A': 'execution_graph_cx2v002_g6_c2v001.py',
    'G6B': 'current_source_evidence_b1_c2v001_g6_c2v001.py',
    'G6C': 'consumed_states_b1_c2v001_g6_c2v001.py',
    'G2': 'srb_rot_adapter_c3v003_g2_c2v001.py',
    'KS5PP': 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py',
    'KS3C2': 's4rc1_common_c3v004_ks3_c2v002.py',
    'KS3R2': 'cp1_runner_c3v004_ks3_c2v002.py',
    'KS42': 'registry_assembler_c3v004_ks4_c2v002.py',
    'KS6AD2': 'lo_state_proof_adapter_c3v003_ks6_c2v002.py',
    'KS6HO2': 'acceptance_handoff_c2v004_ks6_c2v002.py',
}
ORDER = ('G3A', 'G3B', 'G3C', 'G4', 'G1', 'G6A', 'G6B', 'G6C', 'G2', 'KS5PP', 'KS3C2', 'KS3R2', 'KS42', 'KS6AD2', 'KS6HO2')
EDITS = {}

# ============================================================================================ G3a: GQ geometry
EDITS['G3A'] = [
('''"""Independent exact-point all-column GQ bound; static computation only.
''',
'''"""G3 geometry (ks_k3_chain_c2 G-wave c2v001; root A175, A176): gq_geometry_r5_cx2v001 (c6ffb338) with the spec's kept
K in place of the literal 4 of L39, for S1_UA_C3T only.

S1_UA_C3T = KS1's gate (the S1 template's C3T label AND composite_grid_spec equal to CB C3T's, case block 76309ae3,
bitwise). For it, produce() is c6ffb338's computation with one substitution: the kept region of the kperp node grid is
kept_region('route_a', None, K/KPC_M) with K = the spec's kept K (max breaks_inverse_kpc = 3; KS2 kept_k), so the
production nodes are the K=3 grid's (B = {0, 3, 3 sqrt2, K_big}). Custody is KS1 (c6ffb338 L18-26 derived it with
6810b7c3, which refuses the +-3 cube); the record's producer and custody_deriver pins name this file and KS1. Every other
spec is handed to the unchanged c6ffb338 module object (P, by path and sha): its record, pins included, is c6ffb338's.
Edits: this docstring head, the custody pin lines (KS1) plus the predecessor and kept_k() after them, the first line of
produce(), and L39.

Independent exact-point all-column GQ bound; static computation only.
'''),
("""CP=HERE/'custody_cx2v002.py'
CS='6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'
if hashlib.sha256(CP.read_bytes()).hexdigest()!=CS:raise ValueError('custody source pin')
sp=importlib.util.spec_from_file_location('cx2gq_custody',CP)
C=importlib.util.module_from_spec(sp);sys.modules[sp.name]=C;sp.loader.exec_module(C)
""",
"""CP=Path('@@KSDIR@@/custody_cx2v002_ks1_c2v001.py')   # G3: KS1 (it hands every other spec to 6810b7c3)
CS='@@SHA_KS1@@'
if hashlib.sha256(CP.read_bytes()).hexdigest()!=CS:raise ValueError('custody source pin')
sp=importlib.util.spec_from_file_location('g3gq_custody_ks1',CP)
C=importlib.util.module_from_spec(sp);sys.modules[sp.name]=C;sp.loader.exec_module(C)
# G3: the predecessor, unchanged, by path and sha. Every spec that is not S1_UA_C3T runs its code (P).
PREDECESSOR=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_geometry_r5_cx2v001.py'),
             'c6ffb338fd7e87bca0028afcf8c1b6c0ae52b8d89823bdcaded69ce798305d85')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest()!=PREDECESSOR[1]:raise ValueError('G3: gq_geometry c6ffb338 pin mismatch')
_psp=importlib.util.spec_from_file_location('g3_predecessor_gq_geometry_r5_cx2v001',PREDECESSOR[0])
P=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=P;_psp.loader.exec_module(P)


def kept_k(spec):
    \"\"\"G3: the spec's kept K, max(breaks_inverse_kpc) (KS2 kept_k). Only S1_UA_C3T reaches it: 3.\"\"\"
    k=max(spec['numerics']['composite_grid_spec']['breaks_inverse_kpc'])
    if k!=C.S1_C3T_KEPT_K:raise ValueError('S1_UA_C3T kept K must be 3')
    return int(k)
"""),
("""def produce(spec,*,node_limit=None,progress=None):
    begin=time.monotonic();details=C.derive_details(spec=spec)
""",
"""def produce(spec,*,node_limit=None,progress=None):
    if not C.s1_c3t_spec(spec):return P.produce(spec,node_limit=node_limit,progress=progress)   # G3: c6ffb338's own code
    begin=time.monotonic();details=C.derive_details(spec=spec)
"""),
("""    kept=U.kept_region('route_a',None,4/U.KPC_M)
""",
"""    kept=U.kept_region('route_a',None,kept_k(spec)/U.KPC_M)   # G3: the kept K (3); c6ffb338 L39 had the literal 4
"""),
]

# ============================================================================================ G3b: GQ producer (uniform)
EDITS['G3B'] = [
('''"""0528 policy facade over reviewed-correction candidate v002; static only.
''',
'''"""G3 producer (ks_k3_chain_c2 G-wave c2v001; root A175, A176): gq_producer_cx2v005 (2832ceb9) over the G3 geometry
successor, for S1_UA_C3T only.

The kernel is gq_geometry_r5_cx2v001_g3_c2v001 (by path and sha, under a module name of its own: MAP H7); C is its
custody, KS1. produce() hands every spec that is not S1_UA_C3T (KS1's gate) to the unchanged 2832ceb9 module object
(PRED, by path and sha), so its record, both producer pins included, is 2832ceb9's. For S1_UA_C3T it is 2832ceb9's code
over the G3 kernel: numeric_producer = the G3 geometry, producer = this file. policy() and signed_bound() take no spec
and read no K; they are 2832ceb9's text over KS1 (whose pin/read_pin are 6810b7c3's): equal outputs, the self-pin aside.
Edits: this docstring head, the kernel pin lines plus the predecessor after them, the first line of produce().

0528 policy facade over reviewed-correction candidate v002; static only.
'''),
("""P=H/'gq_geometry_r5_cx2v001.py'
S='c6ffb338fd7e87bca0028afcf8c1b6c0ae52b8d89823bdcaded69ce798305d85'
if hashlib.sha256(P.read_bytes()).hexdigest()!=S:raise ValueError('GQ kernel pin mismatch')
sp=importlib.util.spec_from_file_location('cx2gq_policy_kernel',P)
K=importlib.util.module_from_spec(sp);sys.modules[sp.name]=K;sp.loader.exec_module(K)
C=K.C
""",
"""P=Path('@@GWDIR@@/gq_geometry_r5_cx2v001_g3_c2v001.py')   # G3: the geometry successor (c6ffb338 for every other spec)
S='@@SHA_G3A@@'
if hashlib.sha256(P.read_bytes()).hexdigest()!=S:raise ValueError('GQ kernel pin mismatch')
sp=importlib.util.spec_from_file_location('g3gq_policy_kernel_g3_for_v005',P)   # G3: a module name of its own (MAP H7)
K=importlib.util.module_from_spec(sp);sys.modules[sp.name]=K;sp.loader.exec_module(K)
C=K.C
# G3: the predecessor, unchanged, by path and sha (it loads c6ffb338 under its own name). Every other spec runs it.
PREDECESSOR=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_producer_cx2v005.py'),
             '2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest()!=PREDECESSOR[1]:raise ValueError('G3: gq_producer 2832ceb9 pin mismatch')
_psp=importlib.util.spec_from_file_location('g3_predecessor_gq_producer_cx2v005',PREDECESSOR[0])
PRED=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=PRED;_psp.loader.exec_module(PRED)
"""),
("""def produce(spec,*,node_limit=None,progress=None):
    result=K.produce(spec,node_limit=node_limit,progress=progress)
""",
"""def produce(spec,*,node_limit=None,progress=None):
    if not C.s1_c3t_spec(spec):return PRED.produce(spec,node_limit=node_limit,progress=progress)   # G3: 2832ceb9's own code
    result=K.produce(spec,node_limit=node_limit,progress=progress)
"""),
]

# ============================================================================================ G3c: GQ producer b1
EDITS['G3C'] = [
('''"""A134 (b1) successor of gq_producer_cx2v005: offset max-component normalization.
''',
'''"""G3 producer b1 (ks_k3_chain_c2 G-wave c2v001; root A175, A176): gq_producer_b1_c2v001 (3e668a2b) over the G3
geometry successor, for S1_UA_C3T only.

produce() is 3e668a2b's only K site (MAP H6): it hands every spec that is not S1_UA_C3T (KS1's gate) to the unchanged
3e668a2b module object (PRED, by path and sha), whose record is its own; for S1_UA_C3T it runs over the G3 kernel
(gq_geometry_r5_cx2v001_g3_c2v001, its own module name: MAP H7). policy() and signed_bound() take no spec and read no
K; they are 3e668a2b's text over KS1 (pin/read_pin are 6810b7c3's): equal outputs, the self-pin aside. Edits: this
docstring head, the kernel pin lines plus the predecessor after them, the first line of produce().

A134 (b1) successor of gq_producer_cx2v005: offset max-component normalization.
'''),
("""P=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/gq_geometry_r5_cx2v001.py')
S='c6ffb338fd7e87bca0028afcf8c1b6c0ae52b8d89823bdcaded69ce798305d85'
if hashlib.sha256(P.read_bytes()).hexdigest()!=S:raise ValueError('GQ kernel pin mismatch')
sp=importlib.util.spec_from_file_location('cx2gq_policy_kernel',P)
K=importlib.util.module_from_spec(sp);sys.modules[sp.name]=K;sp.loader.exec_module(K)
C=K.C
""",
"""P=Path('@@GWDIR@@/gq_geometry_r5_cx2v001_g3_c2v001.py')   # G3: the geometry successor (c6ffb338 for every other spec)
S='@@SHA_G3A@@'
if hashlib.sha256(P.read_bytes()).hexdigest()!=S:raise ValueError('GQ kernel pin mismatch')
sp=importlib.util.spec_from_file_location('g3gq_policy_kernel_g3_for_b1',P)   # G3: a module name of its own (MAP H7)
K=importlib.util.module_from_spec(sp);sys.modules[sp.name]=K;sp.loader.exec_module(K)
C=K.C
# G3: the predecessor, unchanged, by path and sha (it loads c6ffb338 under its own name). Every other spec runs it.
PREDECESSOR=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/gq_producer_b1_c2v001.py'),
             '3e668a2b04288ce4ff4f95b582412ceb4aecf2c908516b97e84f4b1d6d42c3c5')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest()!=PREDECESSOR[1]:raise ValueError('G3: gq_producer_b1 3e668a2b pin mismatch')
_psp=importlib.util.spec_from_file_location('g3_predecessor_gq_producer_b1_c2v001',PREDECESSOR[0])
PRED=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=PRED;_psp.loader.exec_module(PRED)
"""),
("""def produce(spec,*,node_limit=None,progress=None):
    result=K.produce(spec,node_limit=node_limit,progress=progress)
""",
"""def produce(spec,*,node_limit=None,progress=None):
    if not C.s1_c3t_spec(spec):return PRED.produce(spec,node_limit=node_limit,progress=progress)   # G3: 3e668a2b's own code
    result=K.produce(spec,node_limit=node_limit,progress=progress)
"""),
]

# ============================================================================================ G4: EPS adapter
EDITS['G4'] = [
('''"""EPS adapter successor: finite candidates, dominant values, unique audits.
''',
'''"""G4 (ks_k3_chain_c2 G-wave c2v001; root A175, A176): EPS adapter point_response_admission_adapter_cx2v003 (4de70486)
over KS2 (custody KS1), for S1_UA_C3T only.

adapt_eps hands every spec that is not S1_UA_C3T (KS1's gate) to the unchanged 4de70486 module object (P, by path and
sha), whose base 381b3eaa supplies a1dcdea8 and 6810b7c3: its result, proof producer pin included, is 4de70486's. For
S1_UA_C3T it is 4de70486's code with PR = KS2 (shell_plan from the kept K: the 179 unit shells [3,4]..[181,182]),
CU = KS1 (derive_details admits the +-3 cube) and RESPONSE_SHA = KS2's sha; this file's own sha must be approved and
bound by the review (L177-178, L188), and the proof's producer pin names it. The audit filter (L89, 4 <= n < edge) is
unchanged: AUDIT_LO starts at 4, so a K=3 record carries the same 14 audits (wave-1 K2-P4). Edits: this docstring head
and the predecessor block (base 381b3eaa -> the adapter 4de70486 itself, plus KS2), and the first line of adapt_eps.

EPS adapter successor: finite candidates, dominant values, unique audits.
'''),
("""HERE=Path(__file__).resolve().parent
PREDECESSOR=HERE/'point_response_admission_base_r5_cx2v001.py'
PREDECESSOR_SHA='381b3eaa6ba8a56c2ca4c89f88c6e5e333d7152b52c5386892b19d0a8f50d4e6'
if hashlib.sha256(PREDECESSOR.read_bytes()).hexdigest()!=PREDECESSOR_SHA:
    raise ValueError('EPS adapter predecessor pin mismatch')
sp=importlib.util.spec_from_file_location('cx2_eps_adapter_v001_for_v002',PREDECESSOR)
OLD=importlib.util.module_from_spec(sp);sys.modules[sp.name]=OLD;sp.loader.exec_module(OLD)
PR,CU=OLD.PR,OLD.CU
RESPONSE_SHA=OLD.RESPONSE_SHA
""",
"""HERE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point')   # G4: 4de70486's folder
PREDECESSOR=HERE/'point_response_admission_adapter_cx2v003.py'          # G4: the adapter 4de70486 itself (P)
PREDECESSOR_SHA='4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372'
if hashlib.sha256(PREDECESSOR.read_bytes()).hexdigest()!=PREDECESSOR_SHA:
    raise ValueError('EPS adapter predecessor pin mismatch')
sp=importlib.util.spec_from_file_location('g4_predecessor_eps_adapter_cx2v003',PREDECESSOR)
P=importlib.util.module_from_spec(sp);sys.modules[sp.name]=P;sp.loader.exec_module(P)
RESPONSE_PATH=Path('@@KSDIR@@/point_response_producer_cx2v002_ks2_c2v001.py')   # G4: KS2 (custody KS1)
if hashlib.sha256(RESPONSE_PATH.read_bytes()).hexdigest()!='@@SHA_KS2@@':
    raise ValueError('G4: KS2 response producer pin mismatch')
sp=importlib.util.spec_from_file_location('g4_eps_adapter_response_ks2',RESPONSE_PATH)
PR=importlib.util.module_from_spec(sp);sys.modules[sp.name]=PR;sp.loader.exec_module(PR)
CU=PR.CU
RESPONSE_SHA='@@SHA_KS2@@'
"""),
("""def adapt_eps(spec,numeric_ref,*,review_ref=None,approved_producer_sha256=(),approved_review_sha256=()):
    out={'schema':'UNT_POINT_EPS_ADAPTER_RESULT_CX2V002','utc':PR.utc(),'status':'TESTED',
""",
"""def adapt_eps(spec,numeric_ref,*,review_ref=None,approved_producer_sha256=(),approved_review_sha256=()):
    if not CU.s1_c3t_spec(spec):   # G4: 4de70486's own code path
        return P.adapt_eps(spec,numeric_ref,review_ref=review_ref,approved_producer_sha256=approved_producer_sha256,
                           approved_review_sha256=approved_review_sha256)
    out={'schema':'UNT_POINT_EPS_ADAPTER_RESULT_CX2V002','utc':PR.utc(),'status':'TESTED',
"""),
]

# ============================================================================================ G1: LO slot proof
EDITS['G1'] = [
('''"""S4-R-C1 LO slot proof c3v003 (A134: Q5, Q9a and (a)4). Claude3 builds it; Codex1 reviews it in one pass (FROM_CODEX/0688).
''',
'''"""G1 (ks_k3_chain_c2 G-wave c2v001; root A175, A176): LO slot proof lo_slot_proof_c3v003 (cd10cd59) for S1_UA_C3T.

prove_lo_slot and main() hand every spec that is not S1_UA_C3T (the C3T label AND the CB C3T grid, bitwise) to the
unchanged cd10cd59 module object (loaded lazily by path and sha, after F9's root gate in main), so its result, proof
producer pin included, is cd10cd59's. For S1_UA_C3T it is cd10cd59's code with custody KS1 and the slot rho checked
against the point's K=3 contract: coverage [3, 182], the 10-shell partition from [3,4] and the KS2 response producer
(sha and bytes). check_rho_record decides the contract by the expected identity it is given (an identity-only site: the
CB C3T grid alone, as KS5 does); with no identity (the anchor pair, L297) and for every other identity it is cd10cd59's
K=4 contract, unchanged. The anchor-pair logic, ANCHOR_KEY and the bitwise (a)4 rule are unchanged, so the pair stays
two registered K=4 a1dcdea8 runs at the TAIL_REANCHOR key. Edits: this docstring head, `import copy` and `import re`,
the pins after RESPONSE_SHA, the S1 constants after RHO_PARTITION, the gate helpers before check_rho_record, three
contract checks in it, the custody loader, prove_lo_slot's first line and one line in main().

S4-R-C1 LO slot proof c3v003 (A134: Q5, Q9a and (a)4). Claude3 builds it; Codex1 reviews it in one pass (FROM_CODEX/0688).
'''),
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
("""RESPONSE_SHA = 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'
""",
"""RESPONSE_SHA = 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'
# G1 (A175): the predecessor and the S1_UA_C3T (kept K 3) chain. Every other point keeps the pins above.
PREDECESSOR = (ART + '/s4rc1_c3/proof_side_c3v003/lo_slot_proof_c3v003.py',
               'cd10cd59df44d7b79f3c3aa7ba88998d94c7292c4c2656e09bbbe16ded01bca3')
CUSTODY_KS1 = ('@@KSDIR@@/custody_cx2v002_ks1_c2v001.py', '@@SHA_KS1@@')
RESPONSE_KS2_SHA = '@@SHA_KS2@@'
""" + CB_PIN_LINES + S1_LABEL_LINE),
("""                 [32.0, 64.0], [64.0, 128.0], [128.0, 182.0]]  # response producer shell_plan(unit=False) L112-121
""",
"""                 [32.0, 64.0], [64.0, 128.0], [128.0, 182.0]]  # response producer shell_plan(unit=False) L112-121
RHO_COVERAGE_S1 = [3.0, 182.0]                                # G1: S1_UA_C3T (KS2 shell_plan at kept K 3)
RHO_PARTITION_S1 = [[3.0, 4.0]] + RHO_PARTITION               # G1: the 10-shell partition from [3,4]
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
    \"\"\"G1: composite_grid_spec == CB C3T bitwise. A grid whose last break is not 3 never reads CB.\"\"\"
    try:
        grid = numerics.get('composite_grid_spec')
        if grid['breaks_inverse_kpc'][-1] != 3:
            return False
        return canonical(grid) == canonical(_cb_c3t_grid())
    except (AttributeError, KeyError, IndexError, TypeError, ValueError):
        return False


def _s1_c3t_spec(spec):
    \"\"\"G1 gate (as KS1's): the S1 C3T label AND the CB C3T grid.\"\"\"
    lab = spec.get('label') if isinstance(spec, dict) else None
    return (isinstance(lab, str) and S1_C3T_LABEL.fullmatch(lab) is not None
            and _s1_c3t_numerics(spec.get('numerics')))


def _rho_contract(identity):
    \"\"\"G1: (coverage, partition, response sha, kept K) of the expected identity. The CB C3T grid (S1_UA_C3T; its custody,
    and so every record, comes from KS1, which admits it only with the S1 label) takes K 3; no identity (the anchor pair)
    and every other identity take cd10cd59's.\"\"\"
    if isinstance(identity, dict) and _s1_c3t_numerics(identity.get('numerics')):
        return RHO_COVERAGE_S1, RHO_PARTITION_S1, RESPONSE_KS2_SHA, 3
    return RHO_COVERAGE, RHO_PARTITION, RESPONSE_SHA, 4


_PRED = {}


def _predecessor():
    \"\"\"G1: cd10cd59, unchanged, loaded on first use only (after the F9 root gate in main).\"\"\"
    if 'm' not in _PRED:
        _PRED['m'] = _load_exact(PREDECESSOR[0], PREDECESSOR[1], 'g1_predecessor_lo_slot_proof_c3v003')
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
"""    cov, part, resp, k = _rho_contract(identity)                 # G1: the K=3 contract for S1_UA_C3T only
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
("""            state['cu'] = _load_exact(CUSTODY[0], CUSTODY[1], 's4rc1_proofside_slot_custody_cx2v002')
""",
"""            state['cu'] = _load_exact(CUSTODY_KS1[0], CUSTODY_KS1[1], 's4rc1_proofside_slot_custody_ks1_g1')   # G1: KS1
"""),
("""    \"\"\"Public entry. BLOCKED unless the A134 root gate, approval, registration, slot and (a)4 all hold.\"\"\"
    return _prove(spec, rho_ref, registered_rho_records=registered_rho_records, anchor_rho_pair=anchor_rho_pair,
""",
"""    \"\"\"Public entry. BLOCKED unless the A134 root gate, approval, registration, slot and (a)4 all hold.\"\"\"
    if not _s1_c3t_spec(spec):                        # G1: cd10cd59's own entry, unchanged
        return _predecessor().prove_lo_slot(spec, rho_ref, registered_rho_records=registered_rho_records,
                                            anchor_rho_pair=anchor_rho_pair, root_ruling_refs=root_ruling_refs,
                                            approved_producer_sha256=approved_producer_sha256)
    return _prove(spec, rho_ref, registered_rho_records=registered_rho_records, anchor_rho_pair=anchor_rho_pair,
"""),
("""        spec = env.read_pin(args['spec_ref'])
        res = _prove(spec, args.get('rho_ref'), registered_rho_records=args.get('registered_rho_records', ()),
""",
"""        spec = env.read_pin(args['spec_ref'])
        if not _s1_c3t_spec(spec):                    # G1: cd10cd59's own CLI, unchanged
            return _predecessor().main(argv)
        res = _prove(spec, args.get('rho_ref'), registered_rho_records=args.get('registered_rho_records', ()),
"""),
]

# ============================================================================================ G6a: execution graph
EDITS['G6A'] = [
('''"""Independent expected-stage graph for the frozen calibration call grammar.
''',
'''"""G6a (ks_k3_chain_c2 G-wave c2v001; root A175, A176): execution_graph_cx2v002 (6d59f1d0) with custody KS1, for
S1_UA_C3T only.

expected_stages and validate_graph hand every spec that is not S1_UA_C3T (KS1's gate) to the unchanged 6d59f1d0 module
object (PRED, by path and sha), so its record is 6d59f1d0's. For S1_UA_C3T they are 6d59f1d0's code with C = KS1, whose
derive_details admits the +-3 cube (6d59f1d0 L67 derived it with 6810b7c3: 'K4 cube required'). Nothing else here reads
K: the stage grammar, the A32 hull (L35) and the row checks are unchanged. Edits: this docstring head, the custody pin
lines (KS1) plus the predecessor after them, and the first line of expected_stages and of validate_graph.

Independent expected-stage graph for the frozen calibration call grammar.
'''),
("""P=H/'custody_cx2v002.py';SHA='6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'
if hashlib.sha256(P.read_bytes()).hexdigest()!=SHA:raise ValueError('custody source changed')
s=importlib.util.spec_from_file_location('cx2_graph_custody',P);C=importlib.util.module_from_spec(s)
sys.modules[s.name]=C;s.loader.exec_module(C)
""",
"""P=Path('@@KSDIR@@/custody_cx2v002_ks1_c2v001.py');SHA='@@SHA_KS1@@'   # G6a: KS1 (6810b7c3 for every other spec)
if hashlib.sha256(P.read_bytes()).hexdigest()!=SHA:raise ValueError('custody source changed')
s=importlib.util.spec_from_file_location('g6a_graph_custody_ks1',P);C=importlib.util.module_from_spec(s)
sys.modules[s.name]=C;s.loader.exec_module(C)
# G6a: the predecessor, unchanged, by path and sha. Every spec that is not S1_UA_C3T runs its code (PRED).
PREDECESSOR=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/execution_graph_cx2v002.py'),
             '6d59f1d06e7c69e15e8d9766fa1776da2b0603d16febf4406c96157d77019258')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest()!=PREDECESSOR[1]:raise ValueError('G6a: execution_graph 6d59f1d0 pin mismatch')
_psp=importlib.util.spec_from_file_location('g6a_predecessor_execution_graph_cx2v002',PREDECESSOR[0])
PRED=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=PRED;_psp.loader.exec_module(PRED)
"""),
("""def expected_stages(spec,pass_count):
    C.production_scope(spec)
""",
"""def expected_stages(spec,pass_count):
    if not C.s1_c3t_spec(spec):return PRED.expected_stages(spec,pass_count)   # G6a: 6d59f1d0's own code
    C.production_scope(spec)
"""),
("""def validate_graph(*,spec,result):
    out={'schema':'DDO154_EXECUTION_GRAPH_CX2V002','status':'TESTED','ok':False,'blockers':[],'controls':[]}
""",
"""def validate_graph(*,spec,result):
    if not C.s1_c3t_spec(spec):return PRED.validate_graph(spec=spec,result=result)   # G6a: 6d59f1d0's own code
    out={'schema':'DDO154_EXECUTION_GRAPH_CX2V002','status':'TESTED','ok':False,'blockers':[],'controls':[]}
"""),
]

# ============================================================================================ G6b: current-source evidence
EDITS['G6B'] = [
('''"""Independent saved-source/I1-T replay and current GQ/LO evidence assembly.
''',
'''"""G6b (ks_k3_chain_c2 G-wave c2v001; root A175, A176): current_source_evidence_b1_c2v001 (7044e131) over the KS6
LO config, for S1_UA_C3T only.

Its custody and its current-config check ran through lo_producer_cx2v004 (5db60d0f; MAP H1) -> lo_config 6654d93c,
whose L51 kept region is K=4, with custody 6810b7c3. Here L is the KS6 lo_config 510ff07b directly (MAP H1 option (a);
its PR is KS2 and its CU is KS1, and the four uses of L are L.CU, L.PR.CC (twice) and the current-config check), and G is
the G3 b1 producer successor (signed_bound/policy: 3e668a2b's text). The public entries that take a spec
(assemble_current, export_lo_source, verify_point, verify_occurrence) hand every spec that is not S1_UA_C3T (KS1's gate)
to the unchanged 7044e131 module object (PRED, by path and sha): their records, producer pins included, are 7044e131's.
For S1_UA_C3T they are 7044e131's code with C = KS1 and the KS6 lo_config's validate_current_config, which wants the K=3
kept region. compute_i1t, verify_gas and verify_product take no spec and read no K (MAP H8): 7044e131's text over KS1.
Edits: this docstring head, the PINS L and G values, the module names of the pinned loads, the predecessor after them,
the first line of each spec entry, and the current-config call (L.V2.validate_current_config -> L.validate_current_config).

Independent saved-source/I1-T replay and current GQ/LO evidence assembly.
'''),
(""" 'L':('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/lo_producer_cx2v004.py','5db60d0f6db6d481e2f748b19bef08ce425f19a0e463d58727c184d633e03d51'),
 'G':('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/gq_producer_b1_c2v001.py','3e668a2b04288ce4ff4f95b582412ceb4aecf2c908516b97e84f4b1d6d42c3c5')}
""",
""" 'L':('@@KSDIR@@/lo_config_r5_cx2v001_ks6_c2v001.py','@@SHA_KS6CFG@@'),   # G6b: the KS6 lo_config (MAP H1 (a))
 'G':('@@GWDIR@@/gq_producer_b1_c2v001_g3_c2v001.py','@@SHA_G3C@@')}   # G6b: the G3 b1 producer successor
"""),
("""    sp=importlib.util.spec_from_file_location('cx2_current_'+key,p)
    m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m);return m
R,L,G=(_module(k) for k in ('R','L','G'))
C=L.CU
""",
"""    sp=importlib.util.spec_from_file_location('g6b_current_'+key,p)   # G6b: module names of its own
    m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m);return m
R,L,G=(_module(k) for k in ('R','L','G'))
C=L.CU
# G6b: the predecessor, unchanged, by path and sha. Every spec that is not S1_UA_C3T runs its code (PRED).
PREDECESSOR=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py'),
             '7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest()!=PREDECESSOR[1]:raise ValueError('G6b: evidence 7044e131 pin mismatch')
_psp=importlib.util.spec_from_file_location('g6b_predecessor_current_source_evidence_b1_c2v001',PREDECESSOR[0])
PRED=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=PRED;_psp.loader.exec_module(PRED)
"""),
("""def verify_point(spec,r,p,details):
    if r.profile['galaxies']['DDO154']!=details['geometry']['profile']:raise ValueError('POINT_PROFILE_MISMATCH')
""",
"""def verify_point(spec,r,p,details):
    if not C.s1_c3t_spec(spec):return PRED.verify_point(spec,r,p,details)   # G6b: 7044e131's own code
    if r.profile['galaxies']['DDO154']!=details['geometry']['profile']:raise ValueError('POINT_PROFILE_MISMATCH')
"""),
("""    check=L.V2.validate_current_config(spec,p.state.record,p.state.to_arrays(),r.lib)
""",
"""    check=L.validate_current_config(spec,p.state.record,p.state.to_arrays(),r.lib)   # G6b: the KS6 lo_config (kept K 3)
"""),
("""    \"\"\"One exact own-call occurrence, not completeness of the full call graph.\"\"\"
    o=occurrence;role=o['role'];path=o['state_field_path']
""",
"""    \"\"\"One exact own-call occurrence, not completeness of the full call graph.\"\"\"
    if not C.s1_c3t_spec(spec):return PRED.verify_occurrence(spec,r,p,occurrence)   # G6b: 7044e131's own code
    o=occurrence;role=o['role'];path=o['state_field_path']
"""),
("""    Any absent evidence is typed UNAVAILABLE, with no production PASS emitted.
    \"\"\"
""",
"""    Any absent evidence is typed UNAVAILABLE, with no production PASS emitted.
    \"\"\"
    if not C.s1_c3t_spec(spec):   # G6b: 7044e131's own code path
        return PRED.assemble_current(spec,reconstruction_ref,packet_ref,occurrence,uniform_gq_ref=uniform_gq_ref,review_ref=review_ref,
                                     approved_review_sha256=approved_review_sha256,approved_producer_sha256=approved_producer_sha256,
                                     approved_uniform_producer_sha256=approved_uniform_producer_sha256)
"""),
("""    Rehashes and restores the exact exported TailState before returning.
    \"\"\"
""",
"""    Rehashes and restores the exact exported TailState before returning.
    \"\"\"
    if not C.s1_c3t_spec(spec):return PRED.export_lo_source(spec,reconstruction_ref,packet_ref,occurrence,tail_state_refs,**kwargs)   # G6b
"""),
]

# ============================================================================================ G6c: state enumerator
EDITS['G6C'] = [
('''"""r5 complete-state join from explicit own-call replay descriptors.
''',
'''"""G6c (ks_k3_chain_c2 G-wave c2v001; root A175, A176): the C1 state enumerator consumed_states_b1_c2v001 (4ca7f364)
over the G6a graph and the G6b evidence successors, for S1_UA_C3T only.

consumed_states hands every spec that is not S1_UA_C3T (KS1's gate) to the unchanged 4ca7f364 module object (PRED, by
path and sha): its inventory, producer pin included, is 4ca7f364's. For S1_UA_C3T it is 4ca7f364's code with A = the G6b
evidence successor (so C = A.C = KS1, MAP H2, and verify_point checks the K=3 kept region) and X = the G6a graph
successor; D (consumed_states_cx2v005, K-free) is unchanged. The inventory's producer pin names this file, which the
KS6' LO adapter and the G2 SRB adapter require for an S1_UA_C3T point (MAP H3, H4). Edits: this docstring head, the
PINS A and X values, the module names of the pinned loads, the predecessor after them, and the first line of
consumed_states.

r5 complete-state join from explicit own-call replay descriptors.
'''),
(""" 'A':('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py','7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce'),
 'X':('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/execution_graph_cx2v002.py','6d59f1d06e7c69e15e8d9766fa1776da2b0603d16febf4406c96157d77019258'),
""",
""" 'A':('@@GWDIR@@/current_source_evidence_b1_c2v001_g6_c2v001.py','@@SHA_G6B@@'),   # G6c: the G6b evidence successor
 'X':('@@GWDIR@@/execution_graph_cx2v002_g6_c2v001.py','@@SHA_G6A@@'),   # G6c: the G6a graph successor
"""),
("""    sp=importlib.util.spec_from_file_location('cx2_join_'+key,p)
""",
"""    sp=importlib.util.spec_from_file_location('g6c_join_'+key,p)   # G6c: module names of its own
"""),
("""D,A,X=(module(k) for k in ('D','A','X'))
C=A.C
""",
"""D,A,X=(module(k) for k in ('D','A','X'))
C=A.C
# G6c: the predecessor, unchanged, by path and sha. Every spec that is not S1_UA_C3T runs its code (PRED).
PREDECESSOR=(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py'),
             '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0')
if hashlib.sha256(PREDECESSOR[0].read_bytes()).hexdigest()!=PREDECESSOR[1]:raise ValueError('G6c: enumerator 4ca7f364 pin mismatch')
_psp=importlib.util.spec_from_file_location('g6c_predecessor_consumed_states_b1_c2v001',PREDECESSOR[0])
PRED=importlib.util.module_from_spec(_psp);sys.modules[_psp.name]=PRED;_psp.loader.exec_module(PRED)
"""),
("""def consumed_states(*,spec,result,call_dir):
    out={'schema':'DDO154_CONSUMED_STATE_JOIN_CX2V010','status':'TESTED','complete':False,'states':[],
""",
"""def consumed_states(*,spec,result,call_dir):
    if not C.s1_c3t_spec(spec):return PRED.consumed_states(spec=spec,result=result,call_dir=call_dir)   # G6c: 4ca7f364's own code
    out={'schema':'DDO154_CONSUMED_STATE_JOIN_CX2V010','status':'TESTED','complete':False,'states':[],
"""),
]

# ============================================================================================ G2: SRB-ROT adapter
EDITS['G2'] = [
('''"""S4-R-C1 SRB-ROT adapter c3v003 (A134 Q10). Claude3 builds it; Codex1 reviews it in one pass (FROM_CODEX/0688).
''',
'''"""G2 (ks_k3_chain_c2 G-wave c2v001; root A175, A176): SRB-ROT adapter srb_rot_adapter_c3v003 (08e9ac0a) for S1_UA_C3T.

Deciding test first (README section G2, TESTED): library 2026f2b6 builds a K=3 TailState with unit shells from min(K) = 3
(L730-731), and field_bound / srb_rot run on it with an EPS certificate over [3,182]; with one over [4,182] they refuse
UV_TAIL_EPS_COVERAGE at the [3,4) shell. So the library needs no change, and this adapter does.
adapt_call_srb_rot and main() hand every spec that is not S1_UA_C3T (the C3T label AND the CB C3T grid, bitwise) to the
unchanged 08e9ac0a module object (loaded lazily by path and sha, after F9's root gate in main): its result, proof
producer pin included, is 08e9ac0a's. For S1_UA_C3T it is 08e9ac0a's code with custody KS1, the EPS coverage of the kept
K ([3,182]: the cursor starts at 3) and the inventory producer the G6c enumerator successor (MAP H3). format_eps and
check_inventory decide by the expected identity (identity-only sites: the CB C3T grid alone, as KS5 does); every other
identity keeps 08e9ac0a's [4,182] and 4ca7f364. Edits: this docstring head, `import copy` and `import re`, the pins after
ENUMERATOR_SHA, the S1 coverage after EPS_COVERAGE, the gate helpers before check_inventory, its producer check,
format_eps's coverage lines, the custody loader, adapt_call_srb_rot's first line and one line in main().

S4-R-C1 SRB-ROT adapter c3v003 (A134 Q10). Claude3 builds it; Codex1 reviews it in one pass (FROM_CODEX/0688).
'''),
("""import ast
import datetime
""",
"""import ast
import copy
import datetime
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
# G2 (A175): the predecessor and the S1_UA_C3T (kept K 3) chain. Every other point keeps the pins above.
PREDECESSOR = (ART + '/s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py',
               '08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a')
CUSTODY_KS1 = ('@@KSDIR@@/custody_cx2v002_ks1_c2v001.py', '@@SHA_KS1@@')
ENUMERATOR_G6 = ('@@GWDIR@@/consumed_states_b1_c2v001_g6_c2v001.py', '@@SHA_G6C@@')   # MAP H3
""" + CB_PIN_LINES + S1_LABEL_LINE),
("""EPS_COVERAGE = (4.0, 182.0)                                   # [K, ceil(sqrt(2) * 128)]
""",
"""EPS_COVERAGE = (4.0, 182.0)                                   # [K, ceil(sqrt(2) * 128)]
EPS_COVERAGE_S1 = (3.0, 182.0)                                # G2: S1_UA_C3T, the kept K 3 (KS2 shell_plan)
"""),
("""# ----------------------------------------------------------------------------------------------- inputs
def check_inventory(inventory, details):
    if not isinstance(inventory, dict) or inventory.get('schema') != INVENTORY_SCHEMA or inventory.get('complete') is not True:
        raise Refusal('COMPLETE_V010_INVENTORY_REQUIRED')
    prod = inventory.get('producer')
    if not _is_pin(prod) or prod['sha256'] != ENUMERATOR_SHA:
        raise Refusal('INVENTORY_PRODUCER_NOT_B1_4CA7F364')         # V02
""",
"""# ----------------------------------------------------------------------------------------------- G2: S1_UA_C3T gate
_CB = {}


def _cb_c3t_grid():
    if not _CB:
        with open(CB_PIN['path'], 'rb') as f:
            raw = f.read()
        if hashlib.sha256(raw).hexdigest() != CB_PIN['sha256']:
            raise Refusal('CB case block: sha256 mismatch')
        _CB['C3T'] = json.loads(raw)['cases']['C3T']['normalized_spec_equal']['/numerics']['composite_grid_spec']
    return copy.deepcopy(_CB['C3T'])


def _s1_c3t_numerics(numerics):
    \"\"\"G2: composite_grid_spec == CB C3T bitwise. A grid whose last break is not 3 never reads CB.\"\"\"
    try:
        grid = numerics.get('composite_grid_spec')
        if grid['breaks_inverse_kpc'][-1] != 3:
            return False
        return canonical(grid) == canonical(_cb_c3t_grid())
    except (AttributeError, KeyError, IndexError, TypeError, ValueError):
        return False


def _s1_c3t_spec(spec):
    \"\"\"G2 gate (as KS1's): the S1 C3T label AND the CB C3T grid.\"\"\"
    lab = spec.get('label') if isinstance(spec, dict) else None
    return (isinstance(lab, str) and S1_C3T_LABEL.fullmatch(lab) is not None
            and _s1_c3t_numerics(spec.get('numerics')))


def _s1_identity(details):
    \"\"\"G2: the expected identity is the CB C3T grid's (identity-only sites; its custody is KS1, which needs the label).\"\"\"
    ident = details.get('identity') if isinstance(details, dict) else None
    return isinstance(ident, dict) and _s1_c3t_numerics(ident.get('numerics'))


_PRED = {}


def _predecessor():
    \"\"\"G2: 08e9ac0a, unchanged, loaded on first use only (after the F9 root gate in main).\"\"\"
    if 'm' not in _PRED:
        _PRED['m'] = _load_exact(PREDECESSOR[0], PREDECESSOR[1], 'g2_predecessor_srb_rot_adapter_c3v003')
    return _PRED['m']


# ----------------------------------------------------------------------------------------------- inputs
def check_inventory(inventory, details):
    if not isinstance(inventory, dict) or inventory.get('schema') != INVENTORY_SCHEMA or inventory.get('complete') is not True:
        raise Refusal('COMPLETE_V010_INVENTORY_REQUIRED')
    prod = inventory.get('producer')
    s1 = _s1_identity(details)                                     # G2: the G6c enumerator for S1_UA_C3T (MAP H3)
    if not _is_pin(prod) or prod['sha256'] != (ENUMERATOR_G6[1] if s1 else ENUMERATOR_SHA):
        raise Refusal('INVENTORY_PRODUCER_NOT_THE_G6_ENUMERATOR' if s1 else 'INVENTORY_PRODUCER_NOT_B1_4CA7F364')         # V02
"""),
("""    if eps_rec.get('required_coverage_inverse_kpc') != list(EPS_COVERAGE):
        raise Refusal('EPS_COVERAGE_NOT_4_TO_182')
    shells = eps_rec.get('shells')
    if not isinstance(shells, list) or not shells:
        raise Refusal('EPS_SHELLS_MISSING')
    cursor, out = EPS_COVERAGE[0], []
    for s in shells:
        lo, hi = _float(s.get('lo_inverse_kpc'), 'lo'), _float(s.get('hi_inverse_kpc'), 'hi')
        if s.get('range_inverse_kpc') != [lo, hi] or lo != cursor or hi != lo + 1:
            raise Refusal('EPS_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS_FROM_4')
""",
"""    cov = EPS_COVERAGE_S1 if _s1_identity(details) else EPS_COVERAGE   # G2: [3,182] for S1_UA_C3T only
    if eps_rec.get('required_coverage_inverse_kpc') != list(cov):
        raise Refusal('EPS_COVERAGE_NOT_4_TO_182' if cov == EPS_COVERAGE else 'EPS_COVERAGE_NOT_3_TO_182')
    shells = eps_rec.get('shells')
    if not isinstance(shells, list) or not shells:
        raise Refusal('EPS_SHELLS_MISSING')
    cursor, out = cov[0], []
    for s in shells:
        lo, hi = _float(s.get('lo_inverse_kpc'), 'lo'), _float(s.get('hi_inverse_kpc'), 'hi')
        if s.get('range_inverse_kpc') != [lo, hi] or lo != cursor or hi != lo + 1:
            raise Refusal('EPS_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS_FROM_4' if cov == EPS_COVERAGE else
                          'EPS_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS_FROM_3')
"""),
("""    if cursor != EPS_COVERAGE[1]:
        raise Refusal('EPS_COVERAGE_NOT_4_TO_182')
""",
"""    if cursor != cov[1]:
        raise Refusal('EPS_COVERAGE_NOT_4_TO_182' if cov == EPS_COVERAGE else 'EPS_COVERAGE_NOT_3_TO_182')
"""),
("""            state['cu'] = _load_exact(CUSTODY[0], CUSTODY[1], 's4rc1_proofside_srb_custody_cx2v002')
""",
"""            state['cu'] = _load_exact(CUSTODY_KS1[0], CUSTODY_KS1[1], 's4rc1_proofside_srb_custody_ks1_g2')   # G2: KS1
"""),
("""    \"\"\"Public entry (root operates it at post-run acceptance).\"\"\"
    return _adapt(spec, call_dir=call_dir, result=result, inventory=inventory, bundle_ref=bundle_ref,
""",
"""    \"\"\"Public entry (root operates it at post-run acceptance).\"\"\"
    if not _s1_c3t_spec(spec):                        # G2: 08e9ac0a's own entry, unchanged
        return _predecessor().adapt_call_srb_rot(spec, call_dir=call_dir, result=result, inventory=inventory,
                                                 bundle_ref=bundle_ref, state_input_ref=state_input_ref,
                                                 rows_input_ref=rows_input_ref, root_ruling_refs=root_ruling_refs,
                                                 approved_producer_sha256=approved_producer_sha256,
                                                 trusted_source_producers=trusted_source_producers)
    return _adapt(spec, call_dir=call_dir, result=result, inventory=inventory, bundle_ref=bundle_ref,
"""),
("""        spec = env.read_pin(args['spec_ref'])
        result = json.loads(env.read_bytes(os.path.join(args['call_dir'], 'out', 'result.json')))
""",
"""        spec = env.read_pin(args['spec_ref'])
        if not _s1_c3t_spec(spec):                    # G2: 08e9ac0a's own CLI, unchanged
            return _predecessor().main(argv)
        result = json.loads(env.read_bytes(os.path.join(args['call_dir'], 'out', 'result.json')))
"""),
]

# ============================================================================================ KS5'': wrapper c2v003
EDITS['KS5PP'] = [
('''"""KS5' (ks_k3_chain_c2 c2v002; root A160): s1k3 c2v001 (e7f52461) whose S1_UA_C3T certificate checks use KS5.
''',
'''"""KS5'' (ks_k3_chain_c2 G-wave c2v003; root A175 ruling on ADV-D1/D2): KS5' (66560a6a) plus an S1-only rho slot check.

c2v003 changes one thing. In an S1_UA_C3T certificate_check (prelaunch, so prelaunch_check too, and acceptance), after
q5b1's checks with KS5 and c2v001's domain-K check pass, the point's registered lo slot (the rho record) must be the K=3
contract: required_coverage_inverse_kpc [3, 182] with coverage_complete, the 10-shell partition [3,4], [4,5], [5,6],
[6,8], [8,12], [12,16], [16,32], [32,64], [64,128], [128,182], and the KS2 response producer (the whole pin, and its
bytes read through q5b1's O.read_pinned). q5b1 L168-172 checks only the slot rho's schema, custody and flags, so a K=4
slot cost a 10-18 h S1 call before the acceptance adapter refused it (wave-1 P-F2 note; A175). Every other spec, and
every non-rho clause, is c2v002's. Edits: this docstring head, MODULE_NAME, the S1 rho contract after GUARD_KS5, the
check function after _bundle_domain_k, and three lines after the domain-K check. The text of c2v002 follows.

KS5' (ks_k3_chain_c2 c2v002; root A160): s1k3 c2v001 (e7f52461) whose S1_UA_C3T certificate checks use KS5.
'''),
("""MODULE_NAME = 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002'
""",
"""MODULE_NAME = 'calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003'
"""),
("""GUARD_KS5 = ('@@KSDIR@@/certificate_guard_b1_ks5_c2v001.py', '@@SHA_KS5@@')   # c2v002
""".replace('@@KSDIR@@', KSDIR).replace('@@SHA_KS5@@', WAVE1['KS5'][1]),
"""GUARD_KS5 = ('@@KSDIR@@/certificate_guard_b1_ks5_c2v001.py', '@@SHA_KS5@@')   # c2v002
""".replace('@@KSDIR@@', KSDIR).replace('@@SHA_KS5@@', WAVE1['KS5'][1]) +
"""# c2v003 (A175): the S1_UA_C3T lo slot's rho contract (KS2 shell_plan(unit=False) at kept K 3; KS6 adapter _rho_contract).
RESPONSE_KS2 = {'path': '@@KSDIR@@/point_response_producer_cx2v002_ks2_c2v001.py', 'sha256': '@@SHA_KS2@@'}
RHO_COVERAGE_S1 = [3.0, 182.0]
RHO_PARTITION_S1 = [[3.0, 4.0], [4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0],
                    [64.0, 128.0], [128.0, 182.0]]
"""),
("""def _bundle_domain_k(ref):
    b = M.pin_doc(ref, 'S1_UA_C3T point certificate bundle')
    return (b.get('domain') or {}).get('K_inverse_kpc')
""",
"""def _bundle_domain_k(ref):
    b = M.pin_doc(ref, 'S1_UA_C3T point certificate bundle')
    return (b.get('domain') or {}).get('K_inverse_kpc')


def s1_rho_slot_problems(rho):
    \"\"\"c2v003 (A175): the S1_UA_C3T lo slot rho against the K=3 contract. Returns the problems (empty: it is the contract).\"\"\"
    if not isinstance(rho, dict):
        return ['S1_RHO_SLOT_NOT_AN_OBJECT']
    bad = []
    if rho.get('coverage_complete') is not True or rho.get('required_coverage_inverse_kpc') != RHO_COVERAGE_S1:
        bad.append('S1_RHO_SLOT_COVERAGE_NOT_3_TO_182')
    shells = rho.get('shells') if isinstance(rho.get('shells'), list) else []
    if [s.get('range_inverse_kpc') if isinstance(s, dict) else None for s in shells] != RHO_PARTITION_S1:
        bad.append('S1_RHO_SLOT_PARTITION_NOT_THE_10_SHELLS_FROM_3')
    if rho.get('producer') != RESPONSE_KS2:
        bad.append('S1_RHO_SLOT_PRODUCER_NOT_KS2')
    else:
        try:
            O.read_pinned(dict(RESPONSE_KS2), 'S1_UA_C3T rho producer (KS2)')
        except Exception as exc:
            bad.append('S1_RHO_SLOT_PRODUCER_BYTES_NOT_KS2: %s: %s' % (type(exc).__name__, exc))
    return bad
"""),
("""                if k != float(S1_C3T_KEPT_K):
                    raise Error('S1_UA_C3T_CERTIFICATE_DOMAIN_K_IS_NOT_THE_KEPT_K: bundle domain K %r, kept K %d'
                                % (k, S1_C3T_KEPT_K))
""",
"""                if k != float(S1_C3T_KEPT_K):
                    raise Error('S1_UA_C3T_CERTIFICATE_DOMAIN_K_IS_NOT_THE_KEPT_K: bundle domain K %r, kept K %d'
                                % (k, S1_C3T_KEPT_K))
            bad = s1_rho_slot_problems(M.pin_doc(rec['lo_certificate'], 'S1_UA_C3T registered rho record'))   # c2v003
            if bad:
                raise Error('S1_UA_C3T_RHO_SLOT_NOT_THE_K3_CONTRACT: ' + '; '.join(bad))
"""),
]

# ============================================================================================ KS3' common
EDITS['KS3C2'] = [
('''"""KS3 common (ks_k3_chain_c2 c2v001; root A160): s4rc1_common_c3v004 (53f10e6e) plus row 32, S1_UA_C3T.
''',
'''"""KS3' common (ks_k3_chain_c2 G-wave c2v002; root A175, A176): KS3 common c2v001 (736d2e7e) with row 32's canonical
producers and the S1 acceptance inventory pinned.

New PINS (row 32, S1_UA_C3T, only; rows 1-31 keep every pin): the G3 GQ producer and geometry, the G4 EPS adapter, the
G1 LO slot proof, the G6c state enumerator and the wrapper KS5''. CANONICAL_APPROVED_PRODUCERS (rows 1-31) is
unchanged; CANONICAL_APPROVED_PRODUCERS_S1 is the S1 C1's list (G4, G3, G1). s1_rho_slot_problems is the S1-only rho slot
check (coverage [3, 182], the 10-shell partition, the KS2 producer, whole pin and bytes) that the KS4' verify shares
with KS5'' (A175). Edits: this docstring head, the PINS block's end, the line after CANONICAL_APPROVED_PRODUCERS and the
block after s1_pins_as_table. The text of c2v001 follows.

KS3 common (ks_k3_chain_c2 c2v001; root A160): s4rc1_common_c3v004 (53f10e6e) plus row 32, S1_UA_C3T.
'''),
("""    'case_block': (ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json', '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'),
}
""",
"""    'case_block': (ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json', '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'),
    # KS3' (G-wave, A175/A176): row 32's canonical producers and acceptance inventory; rows 1-31 keep every pin above.
    'gq_producer_g3': ('@@GWDIR@@/gq_producer_cx2v005_g3_c2v001.py', '@@SHA_G3B@@'),
    'gq_geometry_g3': ('@@GWDIR@@/gq_geometry_r5_cx2v001_g3_c2v001.py', '@@SHA_G3A@@'),
    'eps_adapter_g4': ('@@GWDIR@@/point_response_admission_adapter_cx2v003_g4_c2v001.py', '@@SHA_G4@@'),
    'lo_slot_proof_g1': ('@@GWDIR@@/lo_slot_proof_c3v003_g1_c2v001.py', '@@SHA_G1@@'),
    'state_enumerator_g6': ('@@GWDIR@@/consumed_states_b1_c2v001_g6_c2v001.py', '@@SHA_G6C@@'),
    'wrapper_s1k3_ks5pp': ('@@GWDIR@@/calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py', '@@SHA_KS5PP@@'),
}
"""),
("""CANONICAL_APPROVED_PRODUCERS = ('eps_adapter', 'gq_producer', 'lo_slot_proof')
""",
"""CANONICAL_APPROVED_PRODUCERS = ('eps_adapter', 'gq_producer', 'lo_slot_proof')
CANONICAL_APPROVED_PRODUCERS_S1 = ('eps_adapter_g4', 'gq_producer_g3', 'lo_slot_proof_g1')   # KS3': the S1 C1 (row 32)
"""),
("""    out['custody'], out['producer'] = canonical_pin('custody'), canonical_pin('response_producer')
    return out
""",
"""    out['custody'], out['producer'] = canonical_pin('custody'), canonical_pin('response_producer')
    return out


S1_RHO_COVERAGE = [3.0, float(SHELL_END)]                  # KS3' (A175): KS2 shell_plan(unit=False) at kept K 3
S1_RHO_PARTITION = [[3.0, 4.0], [4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0],
                    [64.0, 128.0], [128.0, 182.0]]


def s1_rho_slot_problems(rho, roots=(ART,)):
    \"\"\"KS3' (A175): row 32's lo slot rho against the K=3 contract: coverage [3, 182] (complete), the 10-shell partition
    from [3,4], and the KS2 producer (whole pin; bytes read). Returns the problems; empty means the contract holds.\"\"\"
    if not isinstance(rho, dict):
        return ['S1_RHO_SLOT_NOT_AN_OBJECT']
    bad = []
    if rho.get('coverage_complete') is not True or rho.get('required_coverage_inverse_kpc') != S1_RHO_COVERAGE:
        bad.append('S1_RHO_SLOT_COVERAGE_NOT_3_TO_182')
    shells = rho.get('shells') if isinstance(rho.get('shells'), list) else []
    if [s.get('range_inverse_kpc') if isinstance(s, dict) else None for s in shells] != S1_RHO_PARTITION:
        bad.append('S1_RHO_SLOT_PARTITION_NOT_THE_10_SHELLS_FROM_3')
    if rho.get('producer') != canonical_pin('response_producer_ks2'):
        bad.append('S1_RHO_SLOT_PRODUCER_NOT_KS2')
    else:
        try:
            read_bytes_pinned(rho['producer'], roots, 'S1 rho producer (KS2)', max_bytes=None)
        except (Refusal, OSError, ValueError) as exc:
            bad.append('S1_RHO_SLOT_PRODUCER_BYTES_NOT_KS2: %s' % exc)
    return bad
"""),
]

# ============================================================================================ KS3' runner
EDITS['KS3R2'] = [
('''"""KS3 runner (ks_k3_chain_c2 c2v001; root A160): cp1_runner_c3v004 (3f5e5c18) plus row 32, S1_UA_C3T.
''',
'''"""KS3' runner (ks_k3_chain_c2 G-wave c2v002; root A175, A176): KS3 runner c2v001 (54595c2d) whose row 32 takes the
G3 GQ producer and the G4 EPS adapter.

It loads the KS3' common. Rows 1-31: unchanged (2832ceb9 GQ, 4de70486 adapt-eps, every check and record c2v001's and so
c3v004's; only the runner/common self-pins name this build). Row 32 (S1_UA_C3T) only: the GQ producer is the G3
successor (kept K 3 node grid; custody KS1), and check_gq wants its pin; POINT_START names it; the EPS review request
and adapt-eps bind the G4 adapter (KS2 producer, 179 shells from 3), whose proof check wants the G4 pin; the plan names
the G-wave producers. Edits: this docstring head, the common pin (2) and S1 approved-producer constant, real_loader_s1,
check_gq's signature and want, three lines of run_point, real_adapter_s1, adapt_point's loader/review/approval/check
lines, and the row-32 plan entry. The text of c2v001 follows.

KS3 runner (ks_k3_chain_c2 c2v001; root A160): cp1_runner_c3v004 (3f5e5c18) plus row 32, S1_UA_C3T.
'''),
("""COMMON_PATH = HERE + '/s4rc1_common_c3v004_ks3_c2v001.py'          # KS3 common
COMMON_SHA = '736d2e7e26c6e6f6325796ea83774682a82f2a045a5f6e3f0ae13358725b1656'
""",
"""COMMON_PATH = HERE + '/s4rc1_common_c3v004_ks3_c2v002.py'          # KS3' common
COMMON_SHA = '@@SHA_KS3C2@@'
"""),
("""    spec = importlib.util.spec_from_file_location('s4rc1_common_c3v004_ks3_c2v001', COMMON_PATH)
""",
"""    spec = importlib.util.spec_from_file_location('s4rc1_common_c3v004_ks3_c2v002', COMMON_PATH)
"""),
("""RHO_PARTITION_S1 = [[3.0, 4.0]] + RHO_PARTITION   # the 10-shell partition of KS2 shell_plan(unit=False) at K 3
""",
"""RHO_PARTITION_S1 = [[3.0, 4.0]] + RHO_PARTITION   # the 10-shell partition of KS2 shell_plan(unit=False) at K 3
ADAPT_EPS_APPROVED_PRODUCERS_S1 = (C.PINS['response_producer_ks2'][1], C.PINS['eps_adapter_g4'][1])   # KS3' (G4)
"""),
("""    \"\"\"KS3, row 32 (S1_UA_C3T): the canonical GQ producer and the KS2 response producer (which imports KS1).\"\"\"
    gq = C.load_pinned('gq_producer', 's4rc1_cp1_gq_producer_cx2v005')
""",
"""    \"\"\"KS3', row 32 (S1_UA_C3T): the G3 GQ producer successor and the KS2 response producer (both on KS1).\"\"\"
    gq = C.load_pinned('gq_producer_g3', 's4rc1_cp1_gq_producer_g3_c2v001')
"""),
("""def check_gq(gq, key, custody_sha256):
    want = C.canonical_pin('gq_producer')
""",
"""def check_gq(gq, key, custody_sha256, s1=False):
    want = C.canonical_pin('gq_producer_g3' if s1 else 'gq_producer')   # KS3': row 32's GQ producer is the G3 successor
"""),
("""             'producers': {'gq': C.canonical_pin('gq_producer'), 'eps': C.canonical_pin('response_producer_ks2' if s1 else 'response_producer')},
""",
"""             'producers': {'gq': C.canonical_pin('gq_producer_g3' if s1 else 'gq_producer'), 'eps': C.canonical_pin('response_producer_ks2' if s1 else 'response_producer')},
"""),
("""        gq_checks = check_gq(gq, key, details['custody_sha256'])
""",
"""        gq_checks = check_gq(gq, key, details['custody_sha256'], s1=s1)
"""),
("""                                'point_sha256': key, 'custody_sha256': details['custody_sha256'],
                                'adapter_sha256': C.PINS['eps_adapter'][1],
""",
"""                                'point_sha256': key, 'custody_sha256': details['custody_sha256'],
                                'adapter_sha256': C.PINS['eps_adapter_g4' if s1 else 'eps_adapter'][1],   # KS3': G4 for row 32
"""),
("""def real_adapter():
    return C.load_pinned('eps_adapter', 's4rc1_cp1_eps_adapter_cx2v003')
""",
"""def real_adapter():
    return C.load_pinned('eps_adapter', 's4rc1_cp1_eps_adapter_cx2v003')


def real_adapter_s1():
    \"\"\"KS3', row 32 (S1_UA_C3T): the G4 EPS adapter successor (KS2, KS1).\"\"\"
    return C.load_pinned('eps_adapter_g4', 's4rc1_cp1_eps_adapter_g4_c2v001')
"""),
("""                attempt=1, adapter_loader=real_adapter, require_env=True, review_roots=(C.EXCHANGE,)):
    \"\"\"Distinct-lane review first, then adapter v003 adapt_eps, then the proof (exclusive create).\"\"\"
""",
"""                attempt=1, adapter_loader=None, require_env=True, review_roots=(C.EXCHANGE,)):
    \"\"\"Distinct-lane review first, then adapter v003 adapt_eps, then the proof (exclusive create).\"\"\"
    s1 = C.is_s1_row(row)                             # KS3': row 32 (S1_UA_C3T) takes the G4 adapter
    adapter_loader = adapter_loader or (real_adapter_s1 if s1 else real_adapter)
"""),
("""            'custody_sha256': ctx.get('custody_sha256'), 'adapter_sha256': C.PINS['eps_adapter'][1],
""",
"""            'custody_sha256': ctx.get('custody_sha256'), 'adapter_sha256': C.PINS['eps_adapter_g4' if s1 else 'eps_adapter'][1],
"""),
("""                       approved_producer_sha256=ADAPT_EPS_APPROVED_PRODUCERS,
""",
"""                       approved_producer_sha256=ADAPT_EPS_APPROVED_PRODUCERS_S1 if s1 else ADAPT_EPS_APPROVED_PRODUCERS,
"""),
("""    checks = {'producer_pin_canonical_R4': proof.get('producer') == C.canonical_pin('eps_adapter'),
""",
"""    checks = {'producer_pin_canonical_R4': proof.get('producer') == C.canonical_pin('eps_adapter_g4' if s1 else 'eps_adapter'),
"""),
("""                           rho='coverage [3,182], 10 shells from [3,4]', producers={'eps_rho': C.canonical_pin('response_producer_ks2'),
                                                                                     'gq': C.canonical_pin('gq_producer')},
                           as_built_open='GQ 2832ceb9 (gq_geometry c6ffb338 L18-26 custody 6810b7c3, L39 K=4 kept region) and '
                                         'adapt-eps 4de70486 refuse K=3: root items (ks_k3_chain_c2 README)')
""",
"""                           rho='coverage [3,182], 10 shells from [3,4]', producers={'eps_rho': C.canonical_pin('response_producer_ks2'),
                                                                                     'gq': C.canonical_pin('gq_producer_g3'),
                                                                                     'eps_adapter': C.canonical_pin('eps_adapter_g4')},
                           gwave='KS3\\' (A175/A176): GQ is the G3 successor (kept K 3 node grid, custody KS1) and adapt-eps the '
                                 'G4 successor (KS2, 179 shells from 3); the S1 C1 approves G4, G3 and the G1 slot proof')
"""),
]

# ============================================================================================ KS4' assembler
EDITS['KS42'] = [
('''"""KS4 (ks_k3_chain_c2 c2v001; root A160): registry_assembler_c3v004 (cb5c61ee) plus row 32, S1_UA_C3T.
''',
'''"""KS4' (ks_k3_chain_c2 G-wave c2v002; root A175, A176): KS4 c2v001 (080ed171) with the S1 C1's canonical producers,
its state enumerator, KS5'' and the S1-only rho slot check.

It loads the KS3' common. Rows 1-31 and every non-S1 C1: unchanged (c2v001's and so c3v004's). Row 32 / the S1 C1
only: c1_policy_gate's canonical producer list is CANONICAL_APPROVED_PRODUCERS_S1 (G4 EPS adapter, G3 GQ producer, G1
slot proof) and its state_enumerator must be the G6c enumerator (q5b1 L114-117 calls it at acceptance; MAP H4); the
manifest's S1 C1 draft names G6c and KS5'' and lists the canonical S1 producers; verify replicates KS5'' (A175): after
the guard and the domain-K check, the registered lo slot rho must be the K=3 contract (C.s1_rho_slot_problems). Edits:
this docstring head, the common pin (2), the canon and enumerator lines of c1_policy_gate, the S1 manifest fields, the
wrapper pin in verify (2) and the rho check after the domain-K check. The text of c2v001 follows.

KS4 (ks_k3_chain_c2 c2v001; root A160): registry_assembler_c3v004 (cb5c61ee) plus row 32, S1_UA_C3T.
'''),
("""COMMON_PATH = HERE + '/s4rc1_common_c3v004_ks3_c2v001.py'          # KS3 common
COMMON_SHA = '736d2e7e26c6e6f6325796ea83774682a82f2a045a5f6e3f0ae13358725b1656'
""",
"""COMMON_PATH = HERE + '/s4rc1_common_c3v004_ks3_c2v002.py'          # KS3' common
COMMON_SHA = '@@SHA_KS3C2@@'
"""),
("""    spec = importlib.util.spec_from_file_location('s4rc1_common_c3v004_ks3_c2v001', COMMON_PATH)
""",
"""    spec = importlib.util.spec_from_file_location('s4rc1_common_c3v004_ks3_c2v002', COMMON_PATH)
"""),
("""                                                  'custody_deriver': C.canonical_pin('custody_ks1'),
                                                  'state_enumerator': C.canonical_pin('state_enumerator')}
        man['s1_c3t_guard'] = C.canonical_pin('guard_ks5')
        man['s1_c3t_wrapper'] = C.canonical_pin('wrapper_s1k3_ks5p')
""",
"""                                                  'custody_deriver': C.canonical_pin('custody_ks1'),
                                                  'state_enumerator': C.canonical_pin('state_enumerator_g6')}   # KS4': G6c
        man['s1_c3t_guard'] = C.canonical_pin('guard_ks5')
        man['s1_c3t_wrapper'] = C.canonical_pin('wrapper_s1k3_ks5pp')                                    # KS4': KS5''
        man['s1_c3t_canonical_approved_producers'] = [C.canonical_pin(n) for n in C.CANONICAL_APPROVED_PRODUCERS_S1]
"""),
("""        canon = ([C.canonical_pin(n) for n in C.CANONICAL_APPROVED_PRODUCERS] if canonical_producers is None
                 else list(canonical_producers))
        bad = ([] if r['custody_deriver'] == C.canonical_pin('custody_ks1' if s1 else 'custody') else   # KS4: S1 C1 -> KS1
               ['C1_CUSTODY_DERIVER_NOT_CANONICAL: %r' % (r['custody_deriver'],)])
""",
"""        canon = ([C.canonical_pin(n) for n in (C.CANONICAL_APPROVED_PRODUCERS_S1 if s1 else C.CANONICAL_APPROVED_PRODUCERS)]
                 if canonical_producers is None else list(canonical_producers))   # KS4': the S1 C1's list is G4, G3, G1
        bad = ([] if r['custody_deriver'] == C.canonical_pin('custody_ks1' if s1 else 'custody') else   # KS4: S1 C1 -> KS1
               ['C1_CUSTODY_DERIVER_NOT_CANONICAL: %r' % (r['custody_deriver'],)])
        if s1 and r['state_enumerator'] != C.canonical_pin('state_enumerator_g6'):   # KS4': q5b1 L114-117 (MAP H4)
            bad.append('C1_STATE_ENUMERATOR_NOT_THE_G6_ENUMERATOR: %r' % (r['state_enumerator'],))
"""),
("""        res['wrapper_replica']['wrapper'] = C.canonical_pin('wrapper_s1k3_ks5p')
""",
"""        res['wrapper_replica']['wrapper'] = C.canonical_pin('wrapper_s1k3_ks5pp')
"""),
("""        if s1 and res['guard_b1'].get('ok') is True and (bundle.get('domain') or {}).get('K_inverse_kpc') != 3.0:
            res['guard_b1'] = {'ok': False, 'blockers': ['S1_UA_C3T_CERTIFICATE_DOMAIN_K_IS_NOT_THE_KEPT_K (s1k3 L145-147)']}
""",
"""        if s1 and res['guard_b1'].get('ok') is True and (bundle.get('domain') or {}).get('K_inverse_kpc') != 3.0:
            res['guard_b1'] = {'ok': False, 'blockers': ['S1_UA_C3T_CERTIFICATE_DOMAIN_K_IS_NOT_THE_KEPT_K (s1k3 L145-147)']}
        if s1 and res['guard_b1'].get('ok') is True:                                      # KS4' (A175): replicates KS5''
            bad = C.s1_rho_slot_problems(C.read_json_pinned(rec['lo_certificate'], roots, 'S1 lo slot rho', max_bytes=None), roots)
            if bad:
                res['guard_b1'] = {'ok': False, 'blockers': ['S1_UA_C3T_RHO_SLOT_NOT_THE_K3_CONTRACT: ' + '; '.join(bad)]}
"""),
("""                                        'custody_deriver': (tr1 or {}).get('custody_deriver'), 'guard': C.canonical_pin('guard_ks5'),
                                        'wrapper': C.canonical_pin('wrapper_s1k3_ks5p')}
""",
"""                                        'custody_deriver': (tr1 or {}).get('custody_deriver'), 'guard': C.canonical_pin('guard_ks5'),
                                        'wrapper': C.canonical_pin('wrapper_s1k3_ks5pp')}
"""),
]

# ============================================================================================ KS6' adapter
EDITS['KS6AD2'] = [
('''"""KS6 adapter (ks_k3_chain_c2 c2v001; root A160): lo_state_proof_adapter_c3v003 (211a3220) for S1_UA_C3T K=3 states.
''',
'''"""KS6' adapter (ks_k3_chain_c2 G-wave c2v002; root A175, A176): KS6 adapter c2v001 (8fa371a7) whose S1_UA_C3T
inventory comes from the G6c enumerator.

One change: check_inventory wants the inventory producer of the expected identity (an identity-only site: the CB C3T
grid alone, as KS5 does): the G6c enumerator successor for S1_UA_C3T (MAP H3/H4; 4ca7f364 derives custody with 6810b7c3,
so its K=3 inventory reads INCOMPLETE), the b1 enumerator 4ca7f364 (ENUMERATOR_SHA, unchanged) for every other identity.
adapt_call_lo and main() still hand every non-S1_UA_C3T spec to 211a3220. Edits: this docstring head, the G6c pin after
RESPONSE_KS2_SHA, and the producer check of check_inventory. The text of c2v001 follows.

KS6 adapter (ks_k3_chain_c2 c2v001; root A160): lo_state_proof_adapter_c3v003 (211a3220) for S1_UA_C3T K=3 states.
'''),
("""RESPONSE_KS2_SHA = '99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7'
""",
"""RESPONSE_KS2_SHA = '99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7'
ENUMERATOR_G6 = ('@@GWDIR@@/consumed_states_b1_c2v001_g6_c2v001.py', '@@SHA_G6C@@')   # KS6' (G-wave): S1_UA_C3T only
"""),
("""    prod = inventory.get('producer')
    if not _is_pin(prod) or prod['sha256'] != ENUMERATOR_SHA:
        raise Refusal('INVENTORY_PRODUCER_NOT_B1_4CA7F364')         # V02
""",
"""    prod = inventory.get('producer')
    s1 = isinstance(details.get('identity'), dict) and _s1_c3t_numerics(details['identity'].get('numerics'))   # KS6'
    if not _is_pin(prod) or prod['sha256'] != (ENUMERATOR_G6[1] if s1 else ENUMERATOR_SHA):
        raise Refusal('INVENTORY_PRODUCER_NOT_THE_G6_ENUMERATOR' if s1 else 'INVENTORY_PRODUCER_NOT_B1_4CA7F364')         # V02
"""),
]

# ============================================================================================ KS6' handoff
EDITS['KS6HO2'] = [
('''"""KS6 handoff (ks_k3_chain_c2 c2v001; root A160): acceptance_handoff_c2v004 (5ff464cc) with the KS6 LO adapter for
S1_UA_C3T only.
''',
'''"""KS6' handoff (ks_k3_chain_c2 G-wave c2v002; root A175, A176): KS6 handoff c2v001 (6642d209) re-pinned to the KS6'
LO adapter and, on the S1_UA_C3T path, to the G6b evidence module.

Two changes, on the S1_UA_C3T path only (every other spec is still handed to 5ff464cc): LO_ADAPTER_KS6 is the KS6'
adapter (G6c inventories), and root's trusted_source_producers must name the G6b evidence successor (B1_EVIDENCE_G6;
export_lo_source for an S1_UA_C3T state), not 7044e131. Root still supplies the deps; for S1_UA_C3T they are the G6c
enumerator, the G6b evidence, the KS6 lo_core, KS5 and the G2 SRB adapter (README). Edits: this docstring head, the
LO_ADAPTER_KS6 value, the G6b pin and blocker after B1_UNTRUSTED_BLOCKER, and two lines of the trust check.

KS6 handoff (ks_k3_chain_c2 c2v001; root A160): acceptance_handoff_c2v004 (5ff464cc) with the KS6 LO adapter for
S1_UA_C3T only.
'''),
("""LO_ADAPTER_KS6 = {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/lo_state_proof_adapter_c3v003_ks6_c2v001.py',
                  'sha256': '8fa371a719b41c174175942308ca64bebe40fb1e0d42b99ae27def939cbe6c33', 'entry': 'adapt_call_lo'}
""",
"""LO_ADAPTER_KS6 = {'path': '@@GWDIR@@/lo_state_proof_adapter_c3v003_ks6_c2v002.py',   # KS6' (G-wave): the KS6' adapter
                  'sha256': '@@SHA_KS6AD2@@', 'entry': 'adapt_call_lo'}
"""),
("""B1_UNTRUSTED_BLOCKER = 'TRUSTED_SOURCE_PRODUCERS_WITHOUT_B1_EVIDENCE_7044E131 (offset_b1 README item 5; Claude3 0208 N5)'
""",
"""B1_UNTRUSTED_BLOCKER = 'TRUSTED_SOURCE_PRODUCERS_WITHOUT_B1_EVIDENCE_7044E131 (offset_b1 README item 5; Claude3 0208 N5)'
# KS6' (G-wave): on the S1_UA_C3T path export_lo_source is the G6b evidence successor, so root's list must name it.
B1_EVIDENCE_G6 = {'path': '@@GWDIR@@/current_source_evidence_b1_c2v001_g6_c2v001.py', 'sha256': '@@SHA_G6B@@'}
B1_UNTRUSTED_BLOCKER_G6 = 'TRUSTED_SOURCE_PRODUCERS_WITHOUT_G6B_EVIDENCE (S1_UA_C3T; ks_k3_chain_c2 G-wave README)'
"""),
("""        b1_untrusted = not (isinstance(tsp, (list, tuple)) and B1_EVIDENCE['sha256'] in tsp)
        if b1_untrusted:
            rec['blockers'].append(B1_UNTRUSTED_BLOCKER)
""",
"""        b1_untrusted = not (isinstance(tsp, (list, tuple)) and B1_EVIDENCE_G6['sha256'] in tsp)   # KS6': G6b on this path
        if b1_untrusted:
            rec['blockers'].append(B1_UNTRUSTED_BLOCKER_G6)
"""),
]


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def render(key, shas, gwdir):
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
    text = text.replace('@@KSDIR@@', KSDIR).replace('@@GWDIR@@', gwdir)
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
    gwdir = os.path.realpath(a.target_dir)
    if a.final:
        if gwdir != KSDIR:
            raise SystemExit('--final: the target must be %s' % KSDIR)
    elif not gwdir.startswith(KSDIR + '/dev/'):
        raise SystemExit('development builds go to a NEW folder under %s/dev/' % KSDIR)
    else:
        os.mkdir(gwdir)                                   # a development folder is new (exclusive)
    shas = {}
    for k, (name, want) in WAVE1.items():                 # the wave-1 successors this build pins, from bytes
        with open(os.path.join(KSDIR, name), 'rb') as f:
            got = sha256(f.read())
        if got != want:
            raise SystemExit('WAVE1_PIN_MISMATCH %s %s' % (k, name))
        shas[k] = got
    os.makedirs(os.path.join(gwdir, 'diffs'), exist_ok=True)
    out = []
    for key in ORDER:
        old, new = render(key, shas, gwdir)
        data = new.encode('utf-8')
        p = os.path.join(gwdir, NAME[key])
        with open(p, 'xb') as f:
            f.write(data)
        shas[key] = sha256(data)
        diff = ''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile=PRED[key][0],
                                            tofile=p, n=2))
        dp = os.path.join(gwdir, 'diffs', 'DIFF_%s.diff' % NAME[key][:-3])
        with open(dp, 'xb') as f:
            f.write(diff.encode('utf-8'))
        out.append({'id': key, 'successor': {'path': p, 'sha256': shas[key]},
                    'predecessor': {'path': PRED[key][0], 'sha256': PRED[key][1]},
                    'edits': len(EDITS[key]), 'diff': {'path': dp, 'sha256': sha256(diff.encode('utf-8'))}})
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
