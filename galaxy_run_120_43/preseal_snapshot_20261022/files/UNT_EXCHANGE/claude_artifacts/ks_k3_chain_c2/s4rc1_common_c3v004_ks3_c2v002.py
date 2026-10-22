"""KS3' common (ks_k3_chain_c2 G-wave c2v002; root A175, A176): KS3 common c2v001 (736d2e7e) with row 32's canonical
producers and the S1 acceptance inventory pinned.

New PINS (row 32, S1_UA_C3T, only; rows 1-31 keep every pin): the G3 GQ producer and geometry, the G4 EPS adapter, the
G1 LO slot proof, the G6c state enumerator and the wrapper KS5''. CANONICAL_APPROVED_PRODUCERS (rows 1-31) is
unchanged; CANONICAL_APPROVED_PRODUCERS_S1 is the S1 C1's list (G4, G3, G1). s1_rho_slot_problems is the S1-only rho slot
check (coverage [3, 182], the 10-shell partition, the KS2 producer, whole pin and bytes) that the KS4' verify shares
with KS5'' (A175). Edits: this docstring head, the PINS block's end, the line after CANONICAL_APPROVED_PRODUCERS and the
block after s1_pins_as_table. The text of c2v001 follows.

KS3 common (ks_k3_chain_c2 c2v001; root A160): s4rc1_common_c3v004 (53f10e6e) plus row 32, S1_UA_C3T.

Rows 1-31, POINTS, point_rows(), DOMAIN and every existing PINS entry are unchanged, so select_points(None), the plan
of rows 1-31 and the registry's 31-point table are c3v004's. Row 32 is not in POINTS: it is read from S1_ROW_FILE, a
root-written record (procedure step 3: row, key, label S1_UA_C3T, spec path under s4rc1_c3/s1_c3t_specs/, spec sha,
distance, q_inf), and admitted only if the spec's bytes hash to the recorded sha, its point key (core recipe) is the
recorded key, it is not one of the 31, and it is S1_UA_C3T (the C3T label AND the CB C3T grid, bitwise). The row file is
read only when a selection token or key is not one of the 31. New PINS: KS1, KS2, KS5, the wrapper successor KS5' and
the case block. New helpers: s1_rows, rows_for_key, is_s1_row, kept_k_of_row, domain_of_row, s1_pins_as_table and the
S1_UA_C3T gate. select_points tries row 32 only for a token no table row takes. The c3v004 text follows.

S4-R-C1 shared helpers and pinned tables (Claude3 lane; root A122; reviewer Codex1 under A115).

Pure helpers only: no producer import, no compute, no network. Hashes come from bytes.
The single writer, write_new(), creates files exclusively ('xb') inside a caller-named
output root that is policy-checked; nothing is ever overwritten or deleted.
Brief: claude_artifacts/s4rc1_c3/UNDERSTAND_S4RC1_SYNTH_C3V001.md (699d8ea8).
Rulings: FROM_CODEX/0674 (592bb0f5): per-point cx2 slots (Q6), R10 naming, R5, memory gate.
c3v002: NOTE fixes F1-F8 of the c3v001 verification (VERIFY_S4RC1_BUILD_RESULT_C3V001 65bdeee4) only.
FROM_CODEX/0679: the LO facade and adapter stay HELD in build_c3v001; they are not part of c3v002.
Wrapper of record: v006r10_c4 ef3d3d69 (core dc895f8a; A126/A129, 0670/0675).
c3v003 (FROM_CODEX/0696, 0697): adds two canonical pins and nothing else. They are root's wrapper v002 (7a6af535;
A134 Q5 + (b1); it replaces ef3d3d69 as the wrapper the offline verifier replicates) and the LO slot proof c3v002
(proof_side_c3v002), which also becomes a canonical approved producer. Every other byte is the c3v002 file.
c3v004 (root ruling A138, FROM_CODEX/0703; A139, 0704): erratum-class; three PINS values and their comments only.
- V09: wrapper_q5b1 is the published path calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py
  beside its core dc895f8a, with the same sha 7a6af535 (at the build_v002 path wrapper L27 cannot load its core);
- V02: state_enumerator is the b1 enumerator consumed_states_b1_c2v001 (4ca7f364), which C1 names;
- the canonical LO slot producer is lo_slot_proof_c3v003 (proof side c3v003; V03: wrapper v002's 10-key rho comparison).
"""
import copy
import datetime
import hashlib
import importlib.util
import json
import math
import os
import re
import resource
import subprocess
import sys
import time
from pathlib import Path

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
LANE_ROOT = ART + '/s4rc1_c3'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
EXCHANGE = '/Users/bgm/Research/UNT_EXCHANGE'
DRIVER_SHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
PENDING = 'PENDING_UV_TAIL_CERTIFICATE'
EIGHT_MIB = 8 * 1024 * 1024
PROOF_SCHEMA = 'UNT_CALIBRATION_POINT_PROOF_CX2V001'
BUNDLE_SCHEMA = 'UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001'
EPS_ENVELOPE_RULE = 'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS'
ACCEPTANCE_RULE = 'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED'
DOMAIN = {'K_inverse_kpc': 4.0, 'K_big_inverse_kpc': 128.0}
SHELL_END = 182          # ceil(sqrt(2) * 128), guard v003 L102
THREAD_ENV = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')
MEMORY_PRESSURE = '/usr/bin/memory_pressure'      # launcher cx1v010 L29-34 metric (A127, 0674)
VM_STAT = '/usr/bin/vm_stat'                       # F1: physical-headroom floor, stricter-only beside 0674
GIB = 1 << 30
TASKPOLICY = '/usr/sbin/taskpolicy'
PRIO_DARWIN_PROCESS = 4                            # getpriority(4, 0) == 1 under taskpolicy -b
CODEX2_PRODUCER_LANE = 'Codex2'                    # author lane of the pinned cx2 producers

# Canonical absolute paths (realpath-equal; no symlink, no '..'). Whole-dict producer pins
# are compared by the wrapper (r10_c4 ef3d3d69 L158, byte-identical to r9 there), so producers
# must be imported by exactly these strings (brief R4).
PINS = {
    'custody': (CERT + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'),
    'response_producer': (CERT + '/point_response_producer_cx2v002.py', 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'),
    'eps_adapter': (CERT + '/point_response_admission_adapter_cx2v003.py', '4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372'),
    'gq_producer': (CERT + '/gq_producer_cx2v005.py', '2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd'),
    'lo_core': (CERT + '/lo_core_r5_cx2v001.py', '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e'),
    'lo_facade_v004': (CERT + '/lo_producer_cx2v004.py', '5db60d0f6db6d481e2f748b19bef08ce425f19a0e463d58727c184d633e03d51'),
    'guard_v003': (CERT + '/certificate_guard_cx2v003.py', '5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f'),
    'state_enumerator': (ART + '/s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py', '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'),   # c3v004 V02 (b1)
    'gq_record_c000': (CERT + '/GQ_P128_MS128_C000_R5_CX2V001.json', 'a785ccca92349515356fdd565848ef6bd7bc1bb31b792defb85b1a843f963a7f'),
    'wrapper_r10_c4': (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4.py', 'ef3d3d69e01999dcfa255a75c98bcdee31a9512f0e284053139ea190ef9445c3'),
    'core_r10_c4': (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py', 'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6'),
    # c3v003 (0697): root's wrapper v002, L30 b1 guard, L74 slot rule, L148-191 LO_RHO_SLOT. Its core is dc895f8a above.
    # c3v004 (V09, A138/A139): the published path beside core dc895f8a (root publishes it with cp -n); the same sha.
    'wrapper_q5b1': (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py', '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d'),
    # c3v003 (0696): the A134 Q5 LO slot-proof producer (proof side c3v002), imported by this canonical path (R4).
    # c3v004 (A138): its erratum successor, proof side c3v003 (V03: wrapper v002's 10-key canonical rho comparison).
    'lo_slot_proof': (LANE_ROOT + '/proof_side_c3v003/lo_slot_proof_c3v003.py', 'cd10cd59df44d7b79f3c3aa7ba88998d94c7292c4c2656e09bbbe16ded01bca3'),
    'config_r9': (ART + '/calib_tail_readiness_cx2/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json', '721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e'),
    'eps_cert_v006': (ART + '/tail_scheme_impl_c2/certificates_v002/gates/EPS_CERT_V006.json', '598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192'),
    'lo_cert_v004': (ART + '/tail_scheme_impl_c2/certificates_v004/gates/LO_CERT_V004_MS128.json', '1c384f763e663d85414f25ef8c02b4291efd88b63353a77961f2e88aca2e204a'),
    'brief': (LANE_ROOT + '/UNDERSTAND_S4RC1_SYNTH_C3V001.md', '699d8ea8cb0bf8665eab02cb543ca275b45aeb7866813c0da50b63c14d87f4b0'),
    'ruling_0528': (EXCHANGE + '/FROM_CODEX/0528_2026-10-18_codex2_rulings_P0_normalization_and_certificate_admission.md', 'd11654e5a2ab24944a861372769e75e0a2bbac035feecdf4a54286e3841aae83'),
    'ruling_0674': (EXCHANGE + '/FROM_CODEX/0674_2026-10-19_S4RC1_partial_rulings_GQ_EPS_go_R1_guard.md', '592bb0f5b099b291684074c4af22dc21a32a6379cd05ccc4b2f49f96b1dc180d'),
    # KS3 (A160): the K=3 chain, used for row 32 (S1_UA_C3T) only; rows 1-31 keep every pin above.
    'custody_ks1': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/custody_cx2v002_ks1_c2v001.py', 'ad020470aee354201ab6c68926784d75d3ebe2e16628323d49280bd2eb18aea6'),
    'response_producer_ks2': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/point_response_producer_cx2v002_ks2_c2v001.py', '99c29df639482032114f84420a309d29017cfca7fe01a8412be2757fbff75dd7'),
    'guard_ks5': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/certificate_guard_b1_ks5_c2v001.py', 'e394ae94c6f48ff9e0919e9b186103d2f7c5b00077967579029e8404a62215d6'),
    'wrapper_s1k3_ks5p': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002.py', '66560a6a8335d36eff8b4ec58ef780445dc8c6fa21088712e334311bd6fce1eb'),
    'case_block': (ART + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json', '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'),
    # KS3' (G-wave, A175/A176): row 32's canonical producers and acceptance inventory; rows 1-31 keep every pin above.
    'gq_producer_g3': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/gq_producer_cx2v005_g3_c2v001.py', 'c3699c78703c19a0b82485c022af714b8da1f7e3094759170805913cd2109cf8'),
    'gq_geometry_g3': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/gq_geometry_r5_cx2v001_g3_c2v001.py', '572c86c6a9c49c8946c8be424644dd33932f2f1c3961623f15a036a1830a249b'),
    'eps_adapter_g4': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/point_response_admission_adapter_cx2v003_g4_c2v001.py', 'e00ab71dcbfadecea19c2f28afcd70140c630b8cc50fb73ddb21bbcf2f03fa9e'),
    'lo_slot_proof_g1': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/lo_slot_proof_c3v003_g1_c2v001.py', '6af9ed6c39b47ceb4d772a026603ac6d884b62700a5e4725cfee62f229e0d594'),
    'state_enumerator_g6': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/consumed_states_b1_c2v001_g6_c2v001.py', '4ea0c2caf6802b5f5b8b94661958383d21ad7a0a5d5248ac5d7990e8680cb176'),
    'wrapper_s1k3_ks5pp': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2/calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py', '51a6fb278a57f1504e8b8f2818a6044ff41510f609fc30a6e68f8d52bcdcc993'),
}

# F3/F7: the canonical approved-producer pins of the GQ/EPS phase. The offline verifier fails closed unless
# every C1 approved producer equals one of these whole dicts. No LO_ENVELOPE producer is canonical while
# FROM_CODEX/0679 holds LO; a successor adds one only after root rules LO.
# c3v003 (0696/0697): A134 ruled LO (Q5): the LO_RHO_SLOT producer, lo_slot_proof_c3v002, is canonical too.
# c3v004 (A138): that producer is now lo_slot_proof_c3v003 (the 'lo_slot_proof' pin above).
CANONICAL_APPROVED_PRODUCERS = ('eps_adapter', 'gq_producer', 'lo_slot_proof')
CANONICAL_APPROVED_PRODUCERS_S1 = ('eps_adapter_g4', 'gq_producer_g3', 'lo_slot_proof_g1')   # KS3': the S1 C1 (row 32)

# The 31 CP-1 points (brief section 3; keys recomputed from spec bytes with the core
# a595c5c0 L34-38/L233-238 recipe by the builder at 2026-10-19T07:47Z: all match).
# (row, point key, label, names, spec path under ART, spec sha256, distance Mpc, Q_inf)
POINTS = (
    (1, '8ad6ca4e867854dad71f56a97fda66f7d7b295473092a0bec84a4aca968635f8', 'TAIL_REANCHOR', ('TAIL_REANCHOR', 'WORKERS_8_CANDIDATE_ANCHOR', 'HEADLINE_TRIAL'), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/TAIL_REANCHOR.json', '5fc6f0bdcbe5c58c371f77e886facfc6610ae10c5018a544aa0b67c6facd58e3', 4.04, 8.062),
    (2, '64dc775b80425f8a890e4b23aa985922b19bfe9512456ebf51b0207b4e2eba80', 'HEADLINE_CORNER_000', ('HEADLINE_CORNER_000',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_000.json', 'f3c72d953ad21659cb2d4382a9d19994770fd720f183e34dabdcc3bc0dbc0dd4', 4.04, 161.2),
    (3, '4890508b11bcbd7af814748552125e6b963cd238cf3783b15160b2c5a8c1ba5b', 'HEADLINE_CORNER_001', ('HEADLINE_CORNER_001',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_001.json', '850c8e22d594d20ca3f42e965d5dcd9136b1bde1e25a70f5768045b89d7e4fdb', 4.04, 161.2),
    (4, 'cf78cc9a812ec13578dec8f2af7f9bc50d275965029176672661547b9c415f43', 'HEADLINE_CORNER_010', ('HEADLINE_CORNER_010',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_010.json', '77c54de5f07d0f47c279d63bded14d704c583fb14d2d9e68269bb4cac55f162a', 4.04, 1.612),
    (5, 'b6de7aa886bb243c13cfc55aa64ce49b80180eaf5992ebcb229e3c84ee2609d4', 'HEADLINE_CORNER_011', ('HEADLINE_CORNER_011',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_011.json', '4c8bb2bc1a6fa07baf2be6d981bb3f04ae61d781773cfd3d4bd5cd84c524f1f5', 4.04, 1.612),
    (6, '1f0f44c1bcdb42ebc9a928a983c7121f456e18ce09efc57fb2848ff5f1d4655e', 'HEADLINE_CORNER_100', ('HEADLINE_CORNER_100',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_100.json', '28011f300e5fbdb357af2882da2ba145919770b5583f9804ab4cc16ebf581f90', 4.04, 40.31),
    (7, '662d198de1dfd5f09e1c4ce3f503a836dd53f2abf493ba59af54f7a06203c2d3', 'HEADLINE_CORNER_101', ('HEADLINE_CORNER_101',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_101.json', '478ae40fe70ebd3b869f779e72193adb6934e5ef4fdac473935e2b05bbbc8cf7', 4.04, 40.31),
    (8, 'caec85f43de6f021c36e96d08aae9263156f1f9f13a689effe14a82df0a545dd', 'HEADLINE_CORNER_110', ('HEADLINE_CORNER_110',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_110.json', 'ef8b7d4cd46f50c981b606fa4594271a9c50452d39c7a4c427a28233645138db', 4.04, 0.4031),
    (9, '6b98a3645842963857902644850e4851da5d55408828c1b20e4dcb438fde37d5', 'HEADLINE_CORNER_111', ('HEADLINE_CORNER_111',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_111.json', '36e0ffdbdb90cbb522118439b7a1547e2ea8a26092b5bed22bfd9b14f062f27a', 4.04, 0.4031),
    (10, '54c432f396692faf536b9404c9e3d5d4db43faa8aaeea415c67c4bc28a85ab9e', 'SENS_CORNER_C000_DLO', ('SENS_CORNER_C000_DLO',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C000_DLO.json', '9202dbd70293b2b1f2dd30664733d6742ec245f6ad1f924aa072ad6d474b9fd9', 3.9810717055349722, 161.2),
    (11, '4becefe561f0cb909b532547e0a817f3b3b167a72c88e3e2ad298ab349685d52', 'SENS_CORNER_C001_DLO', ('SENS_CORNER_C001_DLO',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C001_DLO.json', 'e5600f4b1ce036652cab4f68ba4059c73a64e1154a5c59249a86d56b4ee7bb9d', 3.9810717055349722, 161.2),
    (12, '31fff1d0ce2cf95282a576f1e7cb9af2b01d37ce565088769656597ee7212b08', 'SENS_CORNER_C010_DLO', ('SENS_CORNER_C010_DLO',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C010_DLO.json', '5f6f5d00090095dd55b03789bfeb16cf02601079dac138c4c6b73815ea585f90', 3.9810717055349722, 1.612),
    (13, '97b390858255b548c4581b310f18a914fefb0141c58a57954bb0ca7ad76d69c2', 'SENS_CORNER_C011_DLO', ('SENS_CORNER_C011_DLO',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C011_DLO.json', 'a17dce28118f31905abf5132b2ec333de1f2051894d2531c96e90e280efdf03c', 3.9810717055349722, 1.612),
    (14, '2984a4188b131d794e281cfd193339bfd2d6710e09dcbd7bb06dc40cff0a2657', 'SENS_CORNER_C100_DLO', ('SENS_CORNER_C100_DLO',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C100_DLO.json', 'a8115a4409e8c1caf37003c547a35af7f956858c688b2be24c7b81104e4f566d', 3.9810717055349722, 40.31),
    (15, '27f18eeb43b2e37233035cea1185bb4f0c49335b188eb80a267e5ff009623cb5', 'SENS_CORNER_C101_DLO', ('SENS_CORNER_C101_DLO',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C101_DLO.json', '36c04ad025268149f6ff0056308da0a9a720e9d9767a704506bdf63d80118aab', 3.9810717055349722, 40.31),
    (16, '2097d210588c4d78f0a5fbac1675d8f48778a53c9798e55f278f84ea0568e762', 'SENS_CORNER_C110_DLO', ('SENS_CORNER_C110_DLO',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C110_DLO.json', '6b7f30f18dffa569122d5fbfc7c019076b7cd133cf716c5e87a0ddcaf6d26870', 3.9810717055349722, 0.4031),
    (17, '39a63954cc81c01c0d9a14c085df3eff58c1bb8ce8c57771077e35dd7d01d035', 'SENS_CORNER_C111_DLO', ('SENS_CORNER_C111_DLO',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C111_DLO.json', '338184cb84e3ee0464597b0e880d0840640a8d197560e5dfec8ffc0db4e23b63', 3.9810717055349722, 0.4031),
    (18, '1c1f3d896912930687b79e48f0e13576ed912cfaf87a2c64dceff7c81fae2de3', 'SENS_CORNER_C000_DHI', ('SENS_CORNER_C000_DHI',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C000_DHI.json', 'aefd2f8d20418803d1276c5f03b125435220c4877011dfccfbc80f24e72e9810', 4.111497211045223, 161.2),
    (19, 'abba6ef95f58a7c7d57655ca07e3c497ff9d550fcb33f15824909152fe004b04', 'SENS_CORNER_C001_DHI', ('SENS_CORNER_C001_DHI',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C001_DHI.json', 'fc4d321fe62f90e97846b7dc63a1cfa8e078df6c7790866e488e83801df55e20', 4.111497211045223, 161.2),
    (20, '1b19d71d11118cc23903b8ee8b6fdc3ffd2fbc3373eb17a08797a73e76ae3149', 'SENS_CORNER_C010_DHI', ('SENS_CORNER_C010_DHI',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C010_DHI.json', 'e06b845f383f8265c43388c2353c0ba68c9266c6ad9986475d31cb129e617173', 4.111497211045223, 1.612),
    (21, 'a8a7f0b703a22d4965f2c8fe22d6a46eb53c4b488ec55604bd3cd322766b0260', 'SENS_CORNER_C011_DHI', ('SENS_CORNER_C011_DHI',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C011_DHI.json', 'e6a3e5ea53ba34b1b0e42831094acd8e936324107cde4956e3860f02bcffdb57', 4.111497211045223, 1.612),
    (22, '24283deb79ee0c31501ba7a2d5e9f17f38a67b7c837f217347bfd1eb3c3686b0', 'SENS_CORNER_C100_DHI', ('SENS_CORNER_C100_DHI',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C100_DHI.json', '4ae5c8c7287747c0447c7e9898eb2f0d36bdb9b90a07eae1c4801ced7d6cd974', 4.111497211045223, 40.31),
    (23, 'b04418e4e2b21900e3bfa9286224c2d7da56348f74d036d27f958ae8af5820c6', 'SENS_CORNER_C101_DHI', ('SENS_CORNER_C101_DHI',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C101_DHI.json', '97545b83bb1b4a2e2c434c4fdcf373724380357986c37d953f9f667f42a0749c', 4.111497211045223, 40.31),
    (24, 'ad55e0fb26f9e7b184efb4b0f8e9e5cca5a1f017e25b4286ef99d7dfeda58b0a', 'SENS_CORNER_C110_DHI', ('SENS_CORNER_C110_DHI',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C110_DHI.json', '348928f24215e08ff4e7187a2654b7638bb8213bacb235e02caf2e714cd1a4f4', 4.111497211045223, 0.4031),
    (25, '79e77b5302f28ecc09a8bbc2084a0f47a47b953c032abcd365b17848a1a10426', 'SENS_CORNER_C111_DHI', ('SENS_CORNER_C111_DHI',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_CORNER_C111_DHI.json', '1b3fde18a7d3ec13b0aa556c64110a843deb0a2e4471ab892d947066ed7a9527', 4.111497211045223, 0.4031),
    (26, 'a863b917b5775584afed12985b5f1c0e81d1376238835ff3719417f7b2f189ab', 'SENS_DISTANCE_LOWER', ('SENS_DISTANCE_LOWER',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_DISTANCE_LOWER.json', 'e020397cbf7b5d54de9cba0f98adf4d5a18a5944bcae3d02f18a69dec7ecd760', 3.9810717055349722, 8.062),
    (27, 'cb8ca22bffc51d4ea6713f028f2a1ed816210c3d3b631161b5d83c3d055cfcc2', 'SENS_DISTANCE_UPPER', ('SENS_DISTANCE_UPPER',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/SENS_DISTANCE_UPPER.json', '49bce3b5cf7b7124f85cc95fec00aa8f08126a36b24b5d09f44a492bbc6c5ff9', 4.111497211045223, 8.062),
    (28, '6944e210d071c17b502fd5188ea8967503dbf9bb1d5530b67d0b151da02b13cd', 'CAMPAIGN_W1_SEED', ('CAMPAIGN_W1_SEED',), 'step4_launch_readiness_c4/dryplans/specs_v001/specs/CAMPAIGN_W1_SEED.json', '3958aed31353908fe695de6694aab0f1b81ec9d6aab0641c58a0d7425cd9c355', 4.04, 8.062),
    (29, '39a36ac345a431922b6b64a3dafbdc2202ad2d5dbcd07439bf9aee73ea870f71', 'JACOBIAN_PLUS_S', ('JACOBIAN_PLUS_S',), 'calib_tail_readiness_cx2/v006r7/dryplans_v001/P128_MS128_jacobian_00.json', '7488b3c7ec31f78f29f078520938c688497385179d2819b03ba54334dee9d8ae', 4.04, 7.522),
    (30, '2a17398ba37976a713e2631272d4578de679af4fd49d07fa80651c2345aa7e39', 'JACOBIAN_PLUS_GAMMA_OVER_EREF', ('JACOBIAN_PLUS_GAMMA_OVER_EREF',), 'calib_tail_readiness_cx2/v006r7/dryplans_v001/P128_MS128_jacobian_01.json', '5b51529aeeac04d1d12303fdfd376b21645bc48af56d365e3db8b3677d91099c', 4.04, 6.404),
    (31, 'a1b7660c2ebc9540b17d76972f91ea683dc0f21e4ecf3ac58e9755405ad0a90c', 'JACOBIAN_PLUS_ELL_F', ('JACOBIAN_PLUS_ELL_F',), 'calib_tail_readiness_cx2/v006r7/dryplans_v001/P128_MS128_jacobian_02.json', 'e93e2022225b502bbbd60894ff374bf70efb97435b764aeef41d0602d80acc08', 4.04, 8.062),
)
ANCHOR_KEY = POINTS[0][1]
CORNER000_KEY = POINTS[1][1]


class Refusal(Exception):
    """A fail-closed refusal with a stable code."""


def point_rows():
    return [dict(row=r[0], key=r[1], label=r[2], names=list(r[3]), spec_path=ART + '/' + r[4],
                 spec_sha256=r[5], distance_Mpc=r[6], q_inf=r[7]) for r in POINTS]


def select_points(selection=None):
    """Table order (anchor first, HEADLINE_CORNER_000 second). Tokens: row number, name, or >=8-hex key prefix."""
    rows = point_rows()
    if not selection:
        return rows
    chosen = set()
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
S1_C3T_LABEL = re.compile(r'S1 transfer test C3T at u_A theta [0-9a-f]{16}; base [0-9a-f]{8}')
_CB = {}


def cb_grid(case):
    """CB `cases.<case>.normalized_spec_equal./numerics.composite_grid_spec` (PINS case_block), read once."""
    if not _CB:
        doc = json.loads(read_bytes_pinned(canonical_pin('case_block'), (ART,), 'case block'))
        for c in ('C3T', 'C4T'):
            _CB[c] = doc['cases'][c]['normalized_spec_equal']['/numerics']['composite_grid_spec']
    return copy.deepcopy(_CB[case])


def s1_c3t_label(spec):
    lab = spec.get('label') if isinstance(spec, dict) else None
    return isinstance(lab, str) and S1_C3T_LABEL.fullmatch(lab) is not None


def s1_c3t_spec(spec):
    """S1_UA_C3T: the C3T label AND composite_grid_spec == CB C3T bitwise (s1k3 c2v001 L84-92)."""
    if not s1_c3t_label(spec):
        return False
    try:
        return canonical(spec['numerics']['composite_grid_spec']) == canonical(cb_grid('C3T'))
    except (KeyError, TypeError, ValueError):
        return False


def s1_rows():
    """[row 32] if S1_ROW_FILE exists and verifies, [] if it does not exist; Refusal if it exists and fails."""
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
    """The table row(s) with this key; row 32 is looked up only for a key none of the 31 has."""
    return [r for r in point_rows() if r['key'] == key] or [r for r in s1_rows() if r['key'] == key]


def is_s1_row(row):
    return isinstance(row, dict) and row.get('s1_c3t') is True


def kept_k_of_row(row):
    return S1_C3T_KEPT_K if is_s1_row(row) else 4


def domain_of_row(row):
    """Bundle domain: DOMAIN (K 4) for rows 1-31; K 3 for row 32 (KS4, procedure section 2)."""
    return {'K_inverse_kpc': float(S1_C3T_KEPT_K), 'K_big_inverse_kpc': 128.0} if is_s1_row(row) else dict(DOMAIN)


def s1_pins_as_table(pins):
    """Row 32's source pins in the form rows 1-31 record: KS2's point_context records custody = KS1 and producer = KS2
    where a1dcdea8 records 6810b7c3 and a1dcdea8. Both are checked, then replaced; every other pin is kept as is."""
    if (not isinstance(pins, dict) or pins.get('custody') != canonical_pin('custody_ks1')
            or pins.get('producer') != canonical_pin('response_producer_ks2')):
        raise Refusal('S1_SOURCE_PINS_ARE_NOT_KS1_AND_KS2')
    out = dict(pins)
    out['custody'], out['producer'] = canonical_pin('custody'), canonical_pin('response_producer')
    return out


S1_RHO_COVERAGE = [3.0, float(SHELL_END)]                  # KS3' (A175): KS2 shell_plan(unit=False) at kept K 3
S1_RHO_PARTITION = [[3.0, 4.0], [4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0],
                    [64.0, 128.0], [128.0, 182.0]]


def s1_rho_slot_problems(rho, roots=(ART,)):
    """KS3' (A175): row 32's lo slot rho against the K=3 contract: coverage [3, 182] (complete), the 10-shell partition
    from [3,4], and the KS2 producer (whole pin; bytes read). Returns the problems; empty means the contract holds."""
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


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def is_sha(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and is_sha(x['sha256'])


def point_identity(spec):
    """Transcribed from core a595c5c0 L233-238 (unchanged in r10_c4 dc895f8a)."""
    n = copy.deepcopy(spec['numerics'])
    for key in ('eps_certificate', 'lo_certificate'):
        n['uv_tail'].pop(key, None)
    return {'driver_sha256': DRIVER_SHA, 'physical': spec['physical'],
            'coefficients': spec['coefficients'], 'numerics': n}


def point_key(spec):
    return digest(point_identity(spec))


def policy_violations(path, allowed_roots=(ART,)):
    """Lexical path policy: guard v003 L37-55 (+ guard007 L29 ngc3198), run trees, R10.

    Purely lexical (no filesystem access), so it may be applied before anything is opened.
    """
    bad = []
    p = str(path)
    if not os.path.isabs(p):
        return ['PATH_NOT_ABSOLUTE']
    parts = Path(p).parts
    if '..' in parts or '.' in parts or os.path.normpath(p) != p:
        bad.append('PATH_NOT_NORMALIZED')
    for s in parts:
        f = s.casefold()
        if f.startswith('uvt_'):
            bad.append('UVT_COMPONENT_REFUSED')
        if 'ngc3198' in f:
            bad.append('NGC3198_COMPONENT_REFUSED')
        if f == 'kmax_a2f10_c5h_run_v001':
            bad.append('C5H_COMPONENT_REFUSED')
        if s == '.codex':
            bad.append('CODEX_COMPONENT_REFUSED')
        if f in ('runs_ext', 'unt_internal_runs'):
            bad.append('RUN_TREE_REFUSED')
    if not any(p == r or p.startswith(r.rstrip('/') + '/') for r in allowed_roots):
        bad.append('OUTSIDE_ALLOWED_ROOTS')
    return sorted(set(bad))


def require_policy(path, allowed_roots=(ART,), label='path'):
    bad = policy_violations(path, allowed_roots)
    if bad:
        raise Refusal('%s %s: %s' % (label, path, ','.join(bad)))
    return str(path)


def require_canonical(path):
    p = str(path)
    if not os.path.isabs(p) or os.path.realpath(p) != p:
        raise Refusal('NONCANONICAL_PATH (realpath differs; R4): ' + p)
    return p


def read_bytes_pinned(ref, allowed_roots=(ART,), label='pin', max_bytes=EIGHT_MIB):
    """Exact {path, sha256}; lexical policy; canonical; size <= 8 MiB; sha from bytes."""
    if not is_pin(ref):
        raise Refusal(label + ': exact {path, sha256} pin required')
    p = require_policy(ref['path'], allowed_roots, label)
    require_canonical(p)
    st = os.stat(p)
    if max_bytes is not None and st.st_size > max_bytes:
        raise Refusal(label + ': file exceeds 8 MiB: ' + p)
    with open(p, 'rb') as f:
        raw = f.read()
    if sha256_bytes(raw) != ref['sha256']:
        raise Refusal(label + ': sha256 mismatch: ' + p)
    return raw


def read_json_pinned(ref, allowed_roots=(ART,), label='pin', max_bytes=EIGHT_MIB):
    return json.loads(read_bytes_pinned(ref, allowed_roots, label, max_bytes))


def pin_of(path, allowed_roots=(ART,), label='file'):
    """Pin of an existing file, hashed from bytes; the path string is kept exactly."""
    p = require_policy(path, allowed_roots, label)
    require_canonical(p)
    with open(p, 'rb') as f:
        raw = f.read()
    return {'path': p, 'sha256': sha256_bytes(raw)}


def canonical_pin(name):
    path, sha = PINS[name]
    return {'path': path, 'sha256': sha}


def load_exact(path, sha, name):
    """Import a pinned module by its canonical absolute path from the exact hashed bytes.

    The module's __file__ is exactly `path`, so custody.pin(__file__) inside the module
    yields the canonical producer pin the wrapper compares as a whole dict (brief R4).
    """
    p = require_canonical(path)
    with open(p, 'rb') as f:
        raw = f.read()
    if sha256_bytes(raw) != sha:
        raise Refusal('MODULE_PIN_MISMATCH: ' + p)
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    if getattr(mod, '__file__', None) != p:
        raise Refusal('MODULE_FILE_STRING_NOT_CANONICAL: ' + p)
    sys.modules[name] = mod
    exec(compile(raw, p, 'exec'), mod.__dict__)
    if sha256_file(p) != sha:
        raise Refusal('MODULE_CHANGED_WHILE_LOADING: ' + p)
    return mod


def load_pinned(name, module_name):
    path, sha = PINS[name]
    return load_exact(path, sha, module_name)


def encode_record(obj):
    """custody_cx2v002 L149 encoding (sorted keys, indent 2, finite numbers, trailing newline)."""
    return json.dumps(obj, sort_keys=True, indent=2, allow_nan=False).encode() + b'\n'


def write_new(path, obj, out_root, *, raw=None):
    """Exclusive create inside out_root only. Returns the exact pin of the bytes written."""
    p = require_policy(path, (out_root,), 'output')
    parent = os.path.dirname(p)
    if os.path.realpath(parent) != parent:
        raise Refusal('OUTPUT_PARENT_NOT_CANONICAL: ' + parent)
    data = encode_record(obj) if raw is None else raw
    with open(p, 'xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    return {'path': p, 'sha256': sha256_bytes(data)}


class LineLog:
    """A JSONL file created exclusively, then appended line by line (our own new file)."""

    def __init__(self, path, out_root):
        p = require_policy(path, (out_root,), 'log')
        self.path = p
        self.f = open(p, 'x', encoding='utf-8')

    def write(self, obj):
        self.f.write(json.dumps(obj, sort_keys=True, allow_nan=False) + '\n')
        self.f.flush()

    def close(self):
        self.f.close()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def utc_compact():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def parse_memory_pressure(text):
    """Launcher cx1v010 L32-33 exactly: one 'System-wide memory free percentage: N%' line."""
    m = re.findall(r'^System-wide memory free percentage:\s*(\d+)%\s*$', text, re.M)
    return int(m[0]) if len(m) == 1 and 0 <= int(m[0]) <= 100 else None


def memory_free_percent():
    """/usr/bin/memory_pressure with NO arguments (read-only report); never -l/-p/-S."""
    try:
        out = subprocess.check_output([MEMORY_PRESSURE], text=True, stderr=subprocess.STDOUT, timeout=10)
        return parse_memory_pressure(out)
    except Exception:
        return None


def memory_gate(free, margin_pct, floor_pct=25):
    """Start a point only if free >= 25 % + margin (A122, 0674). None/malformed never passes."""
    if type(free) is not int or not 0 <= free <= 100:
        return False, 'MEMORY_METRIC_UNAVAILABLE'
    if type(margin_pct) not in (int, float) or not math.isfinite(margin_pct) or margin_pct <= 0:
        return False, 'MEMORY_MARGIN_INVALID'
    need = floor_pct + margin_pct
    if free < need:
        return False, 'MEMORY_BELOW_GATE: free %d%% < %.1f%%' % (free, need)
    return True, 'MEMORY_GATE_OK: free %d%% >= %.1f%%' % (free, need)


def parse_swapusage(text):
    m = re.search(r'used\s*=\s*([0-9.]+)M', text or '')
    return float(m.group(1)) if m else None


def swap_used_mib():
    try:
        out = subprocess.check_output(['/usr/sbin/sysctl', '-n', 'vm.swapusage'], text=True, timeout=10)
        return parse_swapusage(out)
    except Exception:
        return None


def parse_vm_stat(text):
    """F1: fail-closed parse of /usr/bin/vm_stat (no arguments).

    Exactly one header 'Mach Virtual Memory Statistics: (page size of N bytes)' (N a power of two) and
    exactly one 'Pages free:' and one 'Pages speculative:' line, each an integer and '.'. Purgeable pages
    are deliberately not counted (conservative). Anything else returns None, and None never passes.
    """
    if not isinstance(text, str):
        return None
    page = re.findall(r'^Mach Virtual Memory Statistics: \(page size of (\d+) bytes\)\s*$', text, re.M)
    free = re.findall(r'^Pages free:\s+(\d+)\.\s*$', text, re.M)
    spec = re.findall(r'^Pages speculative:\s+(\d+)\.\s*$', text, re.M)
    if len(page) != 1 or len(free) != 1 or len(spec) != 1:
        return None
    ps, nf, ns = int(page[0]), int(free[0]), int(spec[0])
    if ps <= 0 or ps & (ps - 1):
        return None
    return {'page_size_bytes': ps, 'free_pages': nf, 'speculative_pages': ns,
            'available_bytes': (nf + ns) * ps, 'purgeable_counted': False}


def vm_stat_reading():
    """/usr/bin/vm_stat with NO arguments (one read-only report). None if unreadable or unparseable."""
    try:
        out = subprocess.check_output([VM_STAT], text=True, stderr=subprocess.STDOUT, timeout=10)
        return parse_vm_stat(out)
    except Exception:
        return None


def physical_floor(vm, *, running, r2_spike_allowance_bytes, per_worker_peak_bytes, floor_margin_bytes):
    """F1: stricter-only physical-headroom floor beside the unchanged 0674 gate; a start needs BOTH.

    available = (free + speculative) pages x page size (vm_stat; purgeable excluded) must be
    >= r2_spike_allowance + (running + 1) x per_worker_peak + floor_margin (all in bytes).
    Returns (ok, reason, detail). An unparseable vm_stat or an invalid setting never passes.
    """
    detail = {'r2_spike_allowance_bytes': r2_spike_allowance_bytes, 'per_worker_peak_bytes': per_worker_peak_bytes,
              'floor_margin_bytes': floor_margin_bytes, 'running': running, 'vm_stat': vm,
              'available_bytes': None, 'required_bytes': None}
    if (not all(finite_number(v, 0) for v in (r2_spike_allowance_bytes, per_worker_peak_bytes, floor_margin_bytes))
            or type(running) is not int or running < 0):
        return False, 'PHYSICAL_FLOOR_SETTING_INVALID (no start)', detail
    if not isinstance(vm, dict) or type(vm.get('available_bytes')) is not int or vm['available_bytes'] < 0:
        return False, 'PHYSICAL_FLOOR_METRIC_UNAVAILABLE (vm_stat unreadable or unparseable; no start)', detail
    need = r2_spike_allowance_bytes + (running + 1) * per_worker_peak_bytes + floor_margin_bytes
    if not math.isfinite(need):
        return False, 'PHYSICAL_FLOOR_SETTING_INVALID (no start)', detail
    detail.update(available_bytes=vm['available_bytes'], required_bytes=need)
    text = 'available %.1f GiB %s required %.1f GiB = %.1f + (%d + 1) x %.1f + %.1f GiB' % (
        vm['available_bytes'] / GIB, '%s', need / GIB, r2_spike_allowance_bytes / GIB, running,
        per_worker_peak_bytes / GIB, floor_margin_bytes / GIB)
    if vm['available_bytes'] < need:
        return False, 'PHYSICAL_FLOOR_BELOW_REQUIRED: ' + text % '<', detail
    return True, 'PHYSICAL_FLOOR_OK: ' + text % '>=', detail


def background_qos():
    """True only under taskpolicy -b (PRIO_DARWIN_BG): getpriority(PRIO_DARWIN_PROCESS, 0) == 1."""
    try:
        return os.getpriority(PRIO_DARWIN_PROCESS, 0) == 1
    except Exception:
        return False


def single_thread_env():
    return {k: os.environ.get(k) for k in THREAD_ENV}


def isolated_interpreter():
    return sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1


def usage():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return {'wall': time.monotonic(), 'cpu': r.ru_utime + r.ru_stime, 'maxrss_bytes': int(r.ru_maxrss)}


def stage_metrics(before, after):
    return {'seconds': after['wall'] - before['wall'], 'cpu_seconds': after['cpu'] - before['cpu'],
            'peak_rss_bytes_process_high_water': after['maxrss_bytes'],
            'peak_rss_note': 'ru_maxrss (bytes on macOS) of this worker process at stage end; '
                             'stages run sequentially in one process, so it is the high-water mark so far'}


def contains_template_marker(obj):
    if isinstance(obj, dict):
        return any(contains_template_marker(k) or contains_template_marker(v) for k, v in obj.items())
    if isinstance(obj, list):
        return any(contains_template_marker(v) for v in obj)
    return isinstance(obj, str) and ('<FILL' in obj or 'TEMPLATE_NOT_A_REVIEW' in obj)


def distinct_review_problems(review, *, approved_signer_lanes, excluded_lanes):
    """Distinct-lane rule shared by every review check (the tool never approves its own output)."""
    bad = []
    if contains_template_marker(review):
        bad.append('REVIEW_IS_AN_UNFILLED_TEMPLATE')
    lane = review.get('reviewer_lane')
    if not isinstance(lane, str) or not lane.strip():
        bad.append('REVIEWER_LANE_MISSING')
    elif lane in set(excluded_lanes):
        bad.append('REVIEW_NOT_DISTINCT: reviewer lane ' + lane + ' is a producer/operator lane')
    elif lane not in set(approved_signer_lanes):
        bad.append('REVIEWER_LANE_NOT_ROOT_APPROVED_SIGNER: ' + lane)
    if review.get('distinct_from_producer_lane') is not True:
        bad.append('REVIEW_DOES_NOT_ASSERT_DISTINCT_LANE')
    if not approved_signer_lanes:
        bad.append('NO_ROOT_APPROVED_SIGNER_LANES (brief section 6 Q8)')
    return bad


def finite_number(x, lower=None):
    return type(x) in (int, float) and math.isfinite(x) and (lower is None or x >= lower)
