"""P-88 k_max TAIL-CORRECTED scheme: comparison and pre-registered decision for prereg V007 (Claude2 root lane), c2v007 R12.

R12 [A91]: duplicate JSON BUILD check records refuse before text fallback, with both positions.
NPY duplicate headers name the archive member and both header-key positions. No r6 cache change.
R12 [A88]: SR_K may use PRODUCED_AFTER_THE_SEAL with root-registered producer pins and byte verification.
Its identical-Delta rejection is unchanged. EPS/GQ/LO/LO_NGC/DOUBLING/B0-B3 and identity gates still refuse the token.

R11 = successor of kmax_tail_compare_c2v007_r10.py (e801adc4), ordered by root ruling A79 (A80: the successor round r11).  R11 keeps
A47-A77 as r10 implements them and closes (dispositions and the closure table in COMPARE_V007_IMPL_R11.md): A79.1 (every duplicate
guard keyed on the SEMANTIC identity -- the B0_RO1 case kind, the B0_N3 construction site (file, line), the HARMONICS row (case,
source, query), the RO1 event, the GQ roster NAME -- and the A75.6 fixed roster -> geometry map enforced on every GQ roster,
required or extra, with the NGC roster at its registered range); A79.2 (a coded ArgumentParser: error() raises a typed refusal and
prints a code only, allow_abbrev=False, a repeated option refused naming both argv positions, no help / usage in a blinded mode);
A79.3 (an unavailable registered C5H identity is a refusal, never an empty set); A79.4 (the field packet: raw-name and NumPy
logical-name collisions refused before loading, extensionless members refused outright, the strict NPY header audit on every
member); A79.5 (the H-07 symlink / firmlink / NFD / 'symlink/..' class: the name test and the identity walk on the RESOLVED path,
kernel order, every prefix checked before its child is touched; NFC before every comparison; a leading '//' read as '/'); A79.6 /
A75.3 (every duplicate refusal names both entries by index or JSON path, blinding-safe); A77.2 (the RO1 record parsed strictly:
the driver's exact block keys, typed pins, one event, a positive admitted column_workers); and the r10 recheck and lane-review
notes (LO_NGC extra shells, the top-level gas_M_s_NGC bound to 96, case-entry key allow-list, the BUILD check record content,
numbers_producer bytes, REFUSED/BLOCKED reasons beyond reasons[0], --case outside --validity-only refused).

R10 = successor of kmax_tail_compare_c2v007_r8.py (bd51db15; the stopped r9 is superseded and unused, A72).  R10 keeps A47-A67
as r8 implements them and adds (every ruling stricter where the text is silent; dispositions in COMPARE_V007_IMPL_R10.md):
A71 (no last-wins anywhere: every list-to-mapping conversion and every JSON object rejects a duplicate before the mapping is
built; a duplicate is a RECORD_DEFECT naming both entries by index, DUPLICATE_ENTRY_A71 / DUPLICATE_JSON_KEY_A71; Codex2 0442
B1: duplicate LO / LO_NGC shells); A68 CHK-1 (the LO / GQ / DOUBLING certificate M_s bound to the registered uv_tail gas.M_s of
the case block, and the LO record's explicit source_gas_M_s agreeing with every M_s field it carries); A69 note 1 (the producer
registry, schema C2V003, carries producer PATHS and the compare hashes the producer BYTES; identity comparators and token sets
too), note 2 (shell coverage starts at lo >= K), note 3 (the AMB-07 R-PAIR branch row on an exact (E + E^A)/tau tie is the lowest
row index, explicitly); the r8 recheck SF1 / order N1 (a GQ roster's geometry label is derived from its own kept / outer node set
and bound to its roster name, each geometry once); NEW-52 (the PRODUCED_AFTER_THE_SEAL token is refused outside the post-seal
gate list); Codex2 0442 S1 (blinded modes never echo record-controlled input on an early-refusal stderr path: fixed refusal
codes); Claude3 0065 H-07 (c5h_path_hit catches /.vol paths, aliases by directory identity and hard links by inode); A72 (the
sealed-driver custody pins are a seal-time PIN set, r5 or r6, read from a registered driver BUILD record; anything else is
refused); Claude3 r7 A-N1 (a pass row-set present but not a list is S9 only, never also a B4 gap).  Read after the brief and
implemented as stricter-where-silent closures of the same items: A73 F2 (source_gas_M_s equals the record's gas_M_s and
tail_config gas.M_s), A75 (Claude3 0067: A05 -- a named GQ reach is met by ONE roster spanning from its case's kept K, never a
max-merge; A75.6 -- the fixed map DDO_C2T -> C2T_KB<P>, DDO_C3T -> C3T_KB<P>, DDO_C4T -> C4T_KB<2P>; S01 -- a duplicate-key
interlock marker refuses; B03-B06, A06-A07, B12 -- the remaining list sites; A75.7 -- B0 off the token list), A77.2 (the RO1 role
table per case family, TESTED with the r5 NGC worker / binding shas), and the A74.1 class for the transitive packet (an NPY header
with a repeated key reads V4/V5 False).

R8 = successor of kmax_tail_compare_c2v007_r7.py (528dd23a).  R8 keeps A47-A62 as r7 implements them and adds A67 (the last
round; every ruling stricter where the text is silent): SF1 (the GQ all-nodes count of every DDO roster must equal the
ROOT-REGISTERED production node count of its geometry, read from the producer registry gq_all_nodes_counts {geometry: nodes}
that root takes from the gq_full part records; a count equal to the 4096 sample refuses); N1 (every identity run Z2, Z2-OFF,
B0prime_RERUN carries driver_sha256 = the v010 r5 sha b5cc62af); N2 (the gate-record shas of record are registered in the
producer registry, gate_records {gate: [sha256] | PRODUCED_AFTER_THE_SEAL}, SR_K always by sha; an SR_K record whose Delta is
bitwise identical across any two K is a RECORD_DEFECT); N3 (the RB_FP shell ranges run exactly from K = 4 to sqrt(2) x P: an
excess or a shortfall refuses); N4 (the EPS top-level envelope_dominates_actual_every_shell, and the top-level
eps_max_envelope_all_shells, must equal the nested envelope_bound values: a disagreement, or a top-level flag with no
envelope_bound block, is a RECORD_DEFECT, A54 S5); order N1 (the FIELDS text: an unregistered record reads NO_RUN, A48
AMB-02).  The registry schema moves to C2V002 (the two new required keys).  NEW-31 (accepted) and the float floor (UNTESTED)
are unchanged.  Dispositions are in COMPARE_V007_IMPL_R8.md.

R7 = successor of kmax_tail_compare_c2v007_r6.py (e2fe4745).  R7 keeps A47-A61 as r6 implements them and adds A62 and the r6
recheck findings: order B1 (A54 S9: a pass row-set that is PRESENT but not a list -- a dict, {}, a string, a number -- is a
RECORD_DEFECT; only rows absent, null or [] is the A54 B4 gap); A62.1 (RB_FP shell-domain coverage: the record's shell ranges
cover the C4T tail domain [4, sqrt(2) x P] without overlap and it declares full_tail_domain true, else RECORD_DEFECT); A62.2
(every gate record, SR_K and every replay gate included, is bound to a ROOT-REGISTERED producer sha: a producer registry file,
pinned at the seal, given in test mode by --test-producer-registry; an unregistered producer is a RECORD_DEFECT); A62.3 (the
custody pins move to driver v010 r5: driver b5cc62af, RO1 workers fbe9ae79 / 869ce387, nodes workers 0ae245d8 / a5277172,
binding 86af6198 unchanged, cross-checked against the r5 cascade map; every T-case drivers_allowed = [b5cc62af]); validity SF1
(the GQ named rosters DDO_C2T / DDO_C3T reach their case's registered K_big, read from the case block); SF2 (A57.1: every DDO GQ
roster carries all_nodes {max_abs_diff_over_P0, nodes}); SF3 (A57.4: the EPS envelope fields read in full; eps_max >= every
registered shell eps; SRB_ROT read only when the envelope dominates the actual set on every shell); SF4 (the EPS shells cover the
declared coverage; B1 / B1_OFF / B0prime_RERUN bind their comparator and token set to the registry, A57.3 / A59).
Dispositions are in COMPARE_V007_IMPL_R7.md.

R6 = successor of kmax_tail_compare_c2v007_r5.py (78ac63b7).  R6 keeps A47-A54 as r5 implements them and adds the rulings
made after r5 (V005 addendum, open; the newest governs where it differs): A54 S9 (every pass row-set carries exactly the 12
registered row ids, each once, checked before any dict is built; otherwise RECORD_DEFECT, the case INCOMPLETE); A55 / A56
follow-up 1 (PRODUCTION_K_BIG_A55 = 128); A56 N1 with A58 RI-18 (per-row bounds: same-sign q/(1-q), alternating q/(1+q),
the q cap removed; any row ratio >= 1 or a tau-norm ratio >= 1 makes E unavailable); A56 N2 (RB_FP reads E from a PICARD
R-PAIR of C4T / C4T-A when a base E is unavailable; RB_FP joins the resolvable list); A56 N4 (the KBIG next step); A57 (DDO
gas M_s 128, NGC 96, read in the case block and the GQ rosters); A58 RI-06 (the LO partition), RI-17 (NGC EPS coverage 46);
the r5 recheck findings (order F1: a PICARD member's EA entry must equal its base's; validity F1: every file the reader opens
is checked against the registered C5H run, plus an audit-hook guard in test-mode full mode; F3: RO1_INADMISSIBLE_RECORD;
F7: the blinding backstop catches trailing-dot numbers and long digit runs).  Dispositions are in COMPARE_V007_IMPL_R6.md.

R5 = successor of kmax_tail_compare_c2v007_r4.py (fc2d6465), itself the successor of r3 (30db782c), r2 (b382cb04), r1 (0a44ce58)
and 0621b336.  R5 keeps A47-A52 (and the r1-r4 recheck fixes) and implements A53 and A54 (V005 addendum, open; A54 governs
where it differs): A53 the R-PAIR Picard members admit their base route A (route_a.column_workers 1 leaf; V6 requires
route_a_outcome.result_sha256 equal to the base's; a T-case Picard member's RO1 record equals its base's and its worker kind
is the admitted attempt's; the C5H Picard member carries no ro1_workers and an unarmed, unfired ro1 block), NEW-17 (R-PAIR
members named for an untriggered test are REFUSED at load, once decidability is known and before any test is read), NEW-7
(a tau-norm ratio >= 1 on either of the last two ratios: E unavailable), r4 validity F1 option (a) (each C5H member spec in
the B0 EXT set with its projection and declared differences as evidence), F2 (interlock on every path component and on the
realpath), F3 (RO1_FIRED_IN_IDENTITY_RUN), the REVIEW_V009 repoint to the preserved original 3bce7c02; A54 B4 (a pass
without rows is a record gap: E unavailable), S7 (E_i = max(A51 norm bound, same-sign per-row bound)), S4 (every reading
names every missing or invalid case and gate), S5 (a verdict contradicting its own data is a RECORD_DEFECT), S6 (record-
controlled labels never verbatim in blinded modes; numbers glued to letters redacted), S8 (validate_case_block asserts the
registered tail content) and the GENERIC T3 = {C4T-KLO at P/2, C4T-KHI at 2P} against C4T at P read from the case block,
with EPS and LO coverage >= sqrt(2) x 2P.  Dispositions are in COMPARE_V007_IMPL_R5.md.

Binding text, highest precedence first (clause tags [..] in the code name the clause each line implements):
  [A71] [A72] [A69] [A68]  same file as A50, sections A68 (CHK-1), A69 (Claude3 r7 notes 1-3), A71 (no last-wins anywhere), A72
         (tail-table caching; the sealed driver r5 or r6; H-07; the final compare round r10); also read: A73 (F2; the A62 NGC
         worker correction), A74 (the c2v007 comparator; the NPY class), A75 (the must-guard list), A77 (the RO1 role table).
  [A67]  same file as A50, section A67 (compare r7 and the last round, r8: SF1, SF2, N1-N4, NEW-31 accepted, the float floor
         UNTESTED, order N1; the seal-time pins stay None).  A68 (certificates_v003 / gates_v004 results) rules CHK-1 for the
         round AFTER r8: not implemented here (NEW-60).
  [A62]  same file as A50, section A62 (the final-round compare items: RB_FP shell-domain coverage; gate records bound to
         root-registered producer shas; the custody pins moved to v010 r5).  Also read: A57.3 / A57.4 and A59 (comparator
         c2v004; the Z2 token set replaces the base mapping), A60, A61 (no compare rule).
  [A58]  same file as A50, section A58 (RI-03 DOUBLING at K_big P and 2P with gas M_s 128; RI-05 outer domains; RI-06 the LO
         partition; RI-10 NEW-21..29 dispositions; RI-17 NGC EPS coverage [2, 46]; RI-18 the q cap removed).
  [A57]  same file, section A57 (production DDO gas M_s 128, NGC M_s 96; the Picard member specs per A53).
  [A56]  same file, section A56 (N1 alternating per-row bound and q_i >= 1 unavailable; N2 RB_FP R-PAIR path; N4 KBIG next
         step; A55 follow-ups 1-3).
  [A55]  same file, section A55 (P = 128).
  [A54]  same file as A50, section A54 (Claude3 0053 rulings B4, S3-S8; the generic T3; the tightened A51 bound).
  [A53]  same file as A50, section A53 (R-PAIR Picard members admit the base route A; NEW-7, NEW-17, r4 validity F1-F3;
         REVIEW_V009 read at the preserved original 3bce7c02; R3-4).
  [A52]  same file as A50, section A52 (rulings 1, 3, 5 read by the compare; 2, 4, 6 are producer / NGC side).
  [A51]  same file as A50, section A51 F2 (ruled pre-result): E_i = tau_i ||d_last||_tau q/(1-q), q from the tau-norm ratios.
  [A50]  ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md, section A50 (open file; cited by name, NOT pinned
         until frozen; PIN_ADDENDUM_V005 is None -> sealed mode REFUSES): governs where it differs from A47-A49.
  [A48]  same file, section A48: rulings AMB-01..26 (AMB-20 as restated by A50).
  [A49]  same file, section A49: the RO1 refusal set (three exact raised texts) and ro1.armed required on RO1 cases.
  [A47]  same file, section A47: I1 INCOMPLETE after NO_RUN; I2 T1 = V005 shape_pass AND RA6; I3 blinding; I4 route-A
         mode (conditional on gate I4); I5 max_iterations 32; I6 Z2-OFF mandatory.
  [A46]  RA1-RA13 of ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md (frozen; sha256 487d4449... verified
         from bytes at every start; REFUSED on mismatch).  Also read: A22, A28, A32, A38, A42-A45.
  [R1]   KMAX_TAIL_PREREG_V007_DRAFT_R1.json (c691cab6...) and TAIL_SCHEME_DESIGN_V002(_R1).md where A46-A50 do not override.
  [V005] sealed KMAX_MATRIX_PREREG_V005.json (dbddc02c...): tau_i, Dhat, shape_pass, per_case_validity_gates V1-V6,
         gate_next_steps, D14.  Its sealed compare kmax_compare_c2v005.py (49404bc4...) is loaded pinned and supplies
         adapt_result, packet_checks, diffs and canon unchanged.

Read-only on every input; writes only into a NEW --outdir.  numpy only.  Never opens observed velocities (sigma and tau
come from the pinned V005 prereg; the row radii come from the pinned DDO154 binding query_rows[].{id,radius_m}).  Field
names read from every input are listed in FIELDS_R12_CX3V002.md (generated by --write-field-contract); a record lacking a field
FAILS loudly naming it (E-SEAL1 lesson).

usage:
  full decision:   python3 -I -B kmax_tail_compare_c2v007_r12_cx3v002.py --prereg V007.json --manifest MANIFEST.json --outdir NEW
                       [--case-block CASE_BLOCK.json] [--route-a-mode parallel8|serial_with_exemption]
                       [--test-allow-unpinned-prereg]     (test mode REFUSES full mode on the registered C5H call)
                       [--test-producer-registry REGISTRY.json]   (test mode only; sealed mode reads the pinned registry, A62.2)
                       [--test-driver-build-record BUILD.json]    (test mode only; R10 [A72] the sealed driver build r5 / r6;
                                                                   absent in test mode: the built-in r5 set; sealed: the pin)
  blinded validity: ... --validity-only --case C5H [--case ...]    (A47 I3: no row value printed or written)
  blinded gates:    ... --gates-only                                 (RA13: gate functions on the real records, codes only;
                                                                      case results are read by sha256 of their bytes only)
  field contract:   python3 -I -B kmax_tail_compare_c2v007_r12_cx3v002.py --write-field-contract FIELDS_R12_CX3V002.md   (refuses to overwrite)
"""
import argparse
import ast
import hashlib
import importlib.util
import io
import json
import math
import os
import re
import stat as stat_mod
import sys
import time
import unicodedata
import zipfile
from pathlib import Path

import numpy as np

# ============================================================================================ pins (sha256 from bytes)
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
PIN_ADDENDUM_V004 = (CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md',
                     '487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b')          # [A46] [RA12]
ADDENDUM_V005_CITED = CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'   # [A47] [A48] cited
PIN_ADDENDUM_V005 = None    # PENDING_FROM_BYTES: set when the V005 addendum (A47, A48) is FROZEN (freeze rule; blinding G9/S1).
                            # Until then the open file's sha is only reported; sealed mode (V007_PREREG_SHA256 matched) REFUSES.
PIN_PREREG_V005 = (ART + '/kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json',
                   'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174')
PIN_COMPARE_V005 = (ART + '/kmax_prereg_v005_c2/kmax_compare_c2v005.py',
                    '49404bc4b0d558c93113ed650802d9009f03be64c364f0d862213783389786f5')
PIN_PREREG_V006R1 = (ART + '/kmax_prereg_v005_c2/extension_c5c6/v006_r1/prereg/KMAX_MATRIX_PREREG_V006_R1.json',
                     '807fc5bfcb24ee779137746db3536f41dd97c16bd5f367f79ad5a1b8c3ec067c')            # G5/G6 grids [RA12]
PIN_DRAFT_R1 = (ART + '/tail_scheme_design_c2/v002/r1/KMAX_TAIL_PREREG_V007_DRAFT_R1.json',
                'c691cab6dd9752a7bd98025cf7357a5c729b3fef90a78a6277195c5520671e33')
PIN_C5H_SPEC = (ART + '/c5h_hull_c2/CALL_KMAX_C5H_A2F10_HULL_N8_M32_C2V009.json',
                '60b4613080055aedd92dbb649cdfa45675f64a4d133c7ba3e4fbb15b59c7704e')                # [RA1] [RA4] [A44]
PIN_R3 = {  # saved R3 states (SR-K states, B2/B3/LO/DOUBLING state, D_m4 / RA10 C4R3 reference)
    'C2R3': (CTRL + '/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001/result.json', '1f6b32a4edd0dd28438536165bdb10e13c8125eb5ccafb60ceb17315eba8c169'),
    'C3R3': (CTRL + '/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001/result.json', 'c9c802f44854d4f41f9e119707235899aba75a8bd42e89c19983f9ca9b817674'),
    'C4R3': (CTRL + '/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/result.json', 'aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee')}
V007_PREREG_SHA256 = None   # PENDING_FROM_BYTES: set at the seal (the seal record then pins this script); until then TEST mode
Z2_REFERENCE_RESULT_SHA256 = '883b37a0ed1ad948723cf6288d3f31e8069a2c817c5a55e92caa629982be15bd'          # [R1 B1] from bytes
PRECONDITION_L_REFERENCE_SHA256 = 'b76f7afc272a98e65a61df9294fd0db324fa60b0e47ee10a000afb79751de11f'     # [R1 B1] from bytes
GEO_DECIDING_I_RESULT_SHA256 = 'f33eb362f5311a76cbb4058f7697e50e1e2fb31a60d3faf7ebecad37a6e96d5c'        # [R1 B0prime_RERUN]
B0PRIME_RERUN_SPEC_SHA256 = '4ac5527ad1731353d798c2648adc1033335a12102ec071b3ae6a619334313cb7'           # spec 4ac5527a (V005)
NGC_T120L_OPERATOR_SHA256 = 'e6453d520f902e77da77e49b8f8d1cdbed84639f11ed6cc661943553741b2af4'           # [R1 ngc3198_N_tests]
QINF_EVALUATOR_PREFIX = 'f58de0dc'                                                                      # [R1 EPS] (prefix only)
DRIVER_V009_EXT = '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6'                    # C5H driver [A44]
# [A48 AMB-20] C5H admission bases (pinned, read from bytes at every start)
# [A53] V007 reads the PRESERVED ORIGINAL (3bce7c02, the bytes A48/A50 referenced); the reissued record at the old path
# (d3164b71, E-SEAL1c) is not a V007 input.
PIN_REVIEW_V009 = (ART + '/kmax_prereg_v005_c2/extension_c5c6/check/REVIEW_V009_PREP_V009_V001_ORIG_3bce7c02.json',
                   '3bce7c02926526edf2a594418097ff379604ee1c9760dc1145bcd37ed2882d9f')
PIN_C5H_DRYRUN = (ART + '/c5h_hull_c2/dryrun/C5H/DRYRUN_REPORT.json',
                  'cbd2885dd6a41ded3ec34f6daa07069108fec68d644d22f0819f972747d9bf7a')
PIN_C5R3_SPEC_REVIEWED = (ART + '/kmax_prereg_v005_c2/extension_c5c6/v006_r1/specs/CALL_KMAX_C5R3_A2F10_EXT_N8_M32_C2V009.json',
                          '09ff5a96c02b0428f121138f5ebc23072333c743506a93774af9f496d7fc51e8')
C5H_SPEC_ALLOWED_DIFF_FROM_REVIEWED = ('/label', '/numerics/brackets/rule/fs_absolute_overrides/')   # [A50 AMB-20 restated]
# [A50 root items 11, 12] the declared RO1 custody list (DDO154 route A; RO1_IMPL_V002.md, driver patch c2v002 RO1_ROUTE_A):
# an armed ro1 record must name one of these workers and this binding.  Verified from bytes at every start (REFUSED on mismatch).
RO1_DIR = ART + '/ro1_readout_c2'
# R7 [A62.3] (A56 follow-up 3, NEW-39): the custody pins move to driver v010 r5 (A55 ruling 2: r4 with only the memory-cap pins
# swapped): driver b5cc62af, RO1 workers fbe9ae79 (serial) / 869ce387 (parallel), nodes_v001 RO1 workers 0ae245d8 / a5277172;
# the binding 86af6198 is UNCHANGED.  Verified from bytes at every start, and cross-checked against the r5 cascade map (each pin
# must be the map's r5 image of the r4 sha it replaces; the binding must not be remapped).  The r4 workers are no longer on the
# custody list (stricter).  A62.3 says the pins are verified from bytes "when the r5 check lands": PIN_V010_R5_CHECK stays
# None until root records that check, and sealed mode REFUSES while it is None.
DRIVER_R5_DIR = ART + '/tail_scheme_impl_c2/driver_r5'
R5_CASCADE = DRIVER_R5_DIR + '/cascade'
PIN_DRIVER_V010_R5 = (DRIVER_R5_DIR + '/galaxy_m0_forward_c2v010.py',
                      'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6')               # [A62.3] [A58 RI-01]
PIN_R5_CASCADE_MAP = (DRIVER_R5_DIR + '/CASCADE_MAP_R5_C2V001.json',
                      'a7281e10a15c7f51eae8b5d5336648c1d0a7d04a8cf932b3860c9eba3636a880')
PIN_RO1_CUSTODY = {
    'worker': (R5_CASCADE + '/ro1_readout_c2/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002_r5.py',
               'fbe9ae79ac113aab76109ece785d8030729ce62890dc76ff58144a75af6c17b3'),                # serial (column_workers 1)
    'worker_parallel': (R5_CASCADE + '/ro1_readout_c2/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_c2v002_r5.py',
                        '869ce3870a13fdc94a014cdb0b34eab867c05e59ab7d8abfb15f7db382fd52da'),       # parallel (column_workers > 1)
    'binding': (RO1_DIR + '/ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py',
                '86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885')}               # unchanged (A62.3)
# the r4 shas the r5 cascade map replaces (r4 -> r5), read from the map at every start (A62.3 cross-check only; not accepted)
R4_CUSTODY_SHAS = {'driver': 'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b',
                   'worker': '9f74d4652dbbc237f2d38951440a9a95875251fb2cd286499b404a0cf35a8ad1',
                   'worker_parallel': 'd676ecb2c05e8017a4ffbde74a01e7a7ec1a4290149baa6cbfe62435bb573d97',
                   'nodes_worker': 'dbb331db412027e3499e1700e1df8dac90b30fcd9216951ced0fbbccd6df1457',
                   'nodes_worker_parallel': '5a4c7d41c5a02d2ed0af74e09b4d3b8e726eab7484069dbb459474d1f8cbc177'}
# [R4 validity F1] the nodes_v001 RO1 workers v010 r4 runs for a nodes_v001 uv_tail (r4 b9ae92d5 NODES_ROUTE_A L378-382,
# uvt_active L947-949, worker selection L2855; ro1_outcome counts them armed, L1939-1940), with the same binding 86af6198.
# DECLARED on the custody list, root to confirm (NEW-13): an armed record on a case whose REGISTERED uv_tail source rule is
# nodes_v001 (C4T-D5 and its R-PAIR member) must name one of THESE workers, and every other case one of PIN_RO1_CUSTODY's
# (stricter both ways: a nodes case on a continuum worker, or the reverse, is invalid).  Verified from bytes at every start.
NODES_DIR = R5_CASCADE + '/tail_scheme_impl_c2/nodes_v001/route_a'                    # R7 [A62.3] the r5 nodes workers
PIN_RO1_NODES_CUSTODY = {
    'worker': (NODES_DIR + '/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_nodes_c2v001_r5.py',
               '0ae245d86ef4f28c9a348094cedca14e5b2f4e704a9c90905a167084ac88af15'),                # serial (column_workers 1)
    'worker_parallel': (NODES_DIR + '/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_nodes_c2v001_r5.py',
                        'a527717283f8234df6a562eae6a4f28d5c9d34abfbc08cd7cf3f18d7d5f903f2')}       # parallel (column_workers > 1)
# [A48 AMB-22] the 12 registered row radii: the DDO154 binding query_rows[].{id, radius_m} (that block carries no velocity);
# the same pinned bytes v010 uses for the route-A monitor probe_R_m (v010 UVT_MONITOR_PINS['binding'])
PIN_ROW_RADII_BINDING = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/'
                         'DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json',
                         'f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600')
ROW_RADII_REL_TOL = 1e-12
# [verify fields S4] the pinned tail library (A45 module HASHES a82d0338: lapse c28d4209); used ONLY for normalize_config (inert)
PIN_UVT_LIB = (ART + '/tail_scheme_impl_c2/module/owned_uv_tail_lapse_v001.py',
               'c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22')
C5H_REGISTERED_RUN_NAME = 'KMAX_A2F10_C5H_RUN_V001'            # [verify blinding B4] test-mode full-mode interlock (by name)
# [R4 validity F5] the registered C5H run directory, for a same-file check (os.stat of the directory only; nothing is opened)
C5H_REGISTERED_RUN_DIRS = (CTRL + '/runs_ext/' + C5H_REGISTERED_RUN_NAME,
                           '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/'
                           'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/' + C5H_REGISTERED_RUN_NAME)
# [A52.1] (root ruling on R4 validity F2): B0prime_RERUN is EXEMPT from A50 item 12 (its route A is admitted from a saved
# run, spec 4ac5527a, so RO1 cannot be armed; v010 r4 L1406-1407): it REQUIRES an ro1 block with armed false and fired
# false.  Z2 and Z2-OFF (= Z2_OFF_RO1, spec 894e5b3a, A52.1) keep item 12 (armed true, fired false).
B0PRIME_RERUN_RO1_RULE = 'A52.1_EXEMPT_REQUIRES_ARMED_FALSE_FIRED_FALSE'
# [A52.3] as amended by [A53]: the C5H ROUTE_A-branch member spec carries numerics.route_a.ro1_workers true plus its branch
# leaf (the leaf is required there, excluded from its member-vs-base equality and from the C4T-D5 member's partner equality);
# the C5H PICARD-branch member admits its base's route A and carries NO ro1_workers (its ro1 block reads armed false, fired
# false, as for B0prime_RERUN).  Each C5H member spec has its own B0 record against v009-EXT: [A53 r4 validity F1 option (a)]
# its own call spec sha in the B0 spec_sets/EXT list, the entry carrying the projection to v009-EXT form (projection_sha256)
# and the declared differences (declared_differences, exactly the pointers of B0_EXT_DECLARABLE the member carries).
C5H_RPAIR_RO1_LEAF = 'route_a.ro1_workers'
C5H_RPAIR_RO1_POINTER = '/numerics/route_a/ro1_workers'
# [A52.5] SRB_ROT is not read until a successor EPS record computes the envelope bound (sup over direction x the cardinal
# torus) with coverage >= sqrt(2) x the production K_big.  DECLARED record contract (R4, root/producer to confirm, NEW-19):
# optional EPS field envelope_bound = {rule: EPS_ENVELOPE_RULE, coverage_max_inverse_kpc: number}; the production K_big
# is the registered C4T uv_tail outer.K_big_inverse_kpc (A53 rules it before any T result).
EPS_ENVELOPE_RULE = 'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS'
EPS_ENVELOPE_COVERAGE_FACTOR = math.sqrt(2.0)
OPTIONAL_GATE_FIELDS = {'EPS': ('envelope_bound',)}      # an absent optional field is a reading (A52.5), never a defect
B0_EXT_DECLARABLE = ('/numerics/route_a/ro1_workers', '/numerics/route_a/seed_source_rtol_factor')   # [A53 r4 validity F1 (a)]
# [A54] GENERIC T3: with production K_big = P, T3 = {C4T-KLO at P/2, C4T-KHI at 2P}, each against C4T at P per row <= tau/4,
# decidable.  P, P/2 and 2P are read from the registered case block (C4T uv_tail outer.K_big_inverse_kpc); any other value is
# REFUSED (validate_case_block).  EPS and LO coverage must be >= sqrt(2) x 2P (never below R1's 64 /kpc DDO edge: stricter).
# A55 sets P before any T result: PRODUCTION_K_BIG_A55 is None until then (PENDING_A55); once set, the registered P must
# equal it, and sealed mode REFUSES while it is None.
PRODUCTION_K_BIG_A55 = 128.0      # R6 [A55 ruling 1] [A56 follow-up 1]: P = 128 (T3 = {C4T-KLO 64, C4T-KHI 256} against C4T)
# R6 [A57 ruling 1] production gas M_s: 128 for the DDO tail-corrected cases (every T-case uv_tail: checked on C4T, and every other
# T-case equals C4T outside outer / lambda_scale / source_rule, A54 S8), read in the GQ DDO rosters, the LO source and the
# DOUBLING record (A58 RI-03, RI-06); NGC keeps 96 (the GQ NGC_T120L roster).
PRODUCTION_GAS_M_S_A57 = 128
NGC_GAS_M_S_A57 = 96
NGC_EPS_COVERAGE_EDGE_RI17 = 46.0  # R6 [A58 RI-17] NGC EPS coverage [2, ceil(sqrt(2) x 32)] = [2, 46] (R1 read [2, 32])
# R7 [A62.3]: the custody pins (PIN_RO1_CUSTODY, PIN_RO1_NODES_CUSTODY, PIN_DRIVER_V010_R5 = every T-case drivers_allowed and
# so the I4 driver) are the r5 shas of the r5 cascade map, verified from bytes at every start.  A62.3: "verified from bytes when
# the r5 check lands": the record of that check is PENDING (PIN_V010_R5_CHECK None); sealed mode REFUSES while it is None.
PIN_V010_R5_CHECK = None
# R10 [A72] (ruling 3: if the cache successor v003 is adopted, the sealed driver is v010 r6, reached by a pin-only cascade from r5,
# and the identity runs are rerun on r6): the driver custody pins (the driver = every T-case drivers_allowed, the I4 driver and the
# A67 N1 identity-run driver; the RO1 and nodes_v001 RO1 workers; the binding) are a SEAL-TIME PIN SET, read from a registered
# driver BUILD record (schema DRIVER_BUILD_SCHEMA) pinned at the seal as PIN_DRIVER_BUILD_RECORD (path, sha256); build 'r5' or 'r6'
# only, anything else REFUSED.  An r5 record must equal the built-in r5 set exactly (the A62.3 pins above, predecessor r4).  An r6
# record must be the pin-only image of r5: predecessor r5 with the r5 shas, the binding 86af6198 unchanged, every file under the
# driver_r6 tree (or, for an unchanged pin, the r5 file itself), every sha from bytes, a new driver, and its cascade map (schema of
# the r5 map, declared_sha_map) mapping each changed r5 sha to its r6 image and never remapping the binding.  PENDING: root writes
# and pins the record at the seal; sealed mode REFUSES while PIN_DRIVER_BUILD_RECORD is None.  Test mode reads a test record from
# --test-driver-build-record, or uses the built-in r5 set when none is given (the r8 behaviour, DECLARED).
PIN_DRIVER_BUILD_RECORD = None
DRIVER_BUILD_SCHEMA = 'UNT_V007_SEALED_DRIVER_BUILD_C2V001'
DRIVER_BUILDS = ('r5', 'r6')
DRIVER_R6_DIR = ART + '/tail_scheme_impl_c2/driver_r6'
DRIVER_FILE_NAME = 'galaxy_m0_forward_c2v010.py'
DRIVER_BUILD_KEYS = ('schema', 'build', 'predecessor', 'predecessor_shas', 'driver', 'cascade_map', 'ro1_custody',
                     'ro1_nodes_custody', 'check_record', 'note')
CUSTODY_KEYS = ('driver', 'worker', 'worker_parallel', 'nodes_worker', 'nodes_worker_parallel')
# R7 [A62.2] the ROOT-REGISTERED producer registry (schema PRODUCER_REGISTRY_SCHEMA; FIELDS_R8.md): {producers: {gate: [sha256]},
# identity_comparators: [sha256], identity_tokens: {B1|B1_OFF|B0prime_RERUN: [sha256]}}.  Every gate record's producer/sha256 must
# be registered for its gate, and every identity-gate record's comparator/sha256 and tokens/sha256 too (A57.3, A59; r6 recheck
# validity SF4 (b)).  PENDING: root writes and registers it; sealed mode REFUSES while it is None.  Test mode reads a test
# registry from --test-producer-registry; without one every gate record is a RECORD_DEFECT (fail closed).
# R8 [A67 N2] (r7 recheck validity N2): the registry also holds the GATE-RECORD shas of record, gate_records {gate: [sha256 of the
# record file bytes] | GATE_RECORD_AFTER_SEAL}: a gate record must be one of its gate's registered records; a gate absent from
# gate_records is a RECORD_DEFECT (fail closed).  DECLARED (NEW-52): root may mark a gate whose record of record can only exist
# after the seal (it cross-references a T-case or R-PAIR result: SRB_ROT, RB_FP, T2I, EA, MT, I1T, FLAG_RULINGS, ...) with the
# token GATE_RECORD_AFTER_SEAL, which binds that gate by its producer pin and bytes (A62.2/A69).
# R12 [A88] SR_K joins this set: sealed producers replay the fixed saved R3 states immediately after the seal.
# R8 [A67 SF1] (r7 recheck validity SF1): gq_all_nodes_counts {geometry label: production node count}, the per-geometry counts
# root registers from the gq_full part records (label, full_domain.nodes); every count an int > the 4096 sample.
# R10 [A69 note 1] (A62.2; Codex2 0442 deferred A69.1: a registered claimed producer sha with a nonexistent producer path passed):
# schema C2V003.  producers {gate: [{path, sha256}]}, identity_comparators [{path, sha256}], identity_tokens {gate: [{path,
# sha256}]}: the registry names each producer FILE, and the compare hashes its BYTES -- at load (a missing file or a sha that is
# not its bytes REFUSES the registry) and again at every gate read (a record's producer/{path, sha256} must be a registered entry
# of its gate, path and sha both, and the file's bytes must still hash to it; else RECORD_DEFECT).  R10 [A71] a duplicate entry
# in any registry list REFUSES the registry.  R10 (NEW-52; r8 recheck validity N1, order N2, Claude3 P-N2; stricter where silent):
# the token is refused at load outside GATE_RECORD_AFTER_SEAL_ALLOWED, the gates whose record of record cross-references a T-case
# or R-PAIR result (NEW-52's list, B0 member evidence and HARMONICS included); every other gate (EPS, GQ, LO, LO_NGC, DOUBLING,
# the B-gates, I4) is registered by record sha. SR_K joins the token set under A88.
PRODUCER_REGISTRY_SCHEMA = 'UNT_KMAX_TAIL_V007_PRODUCER_REGISTRY_C2V003'
PIN_PRODUCER_REGISTRY = None
GATE_RECORD_AFTER_SEAL = 'PRODUCED_AFTER_THE_SEAL'
GATE_RECORD_SHA_REQUIRED = ()  # R12 [A88]: SR_K now permits the after-seal token.
# R10 [A75.7] (Claude3 P-N2): only gates whose inputs are V007 run outputs; B0 (plan / spec identity) is not one (NEW-52 named it
# 'possibly'). R12 [A88] supersedes the former SR_K-by-sha-only requirement.
GATE_RECORD_AFTER_SEAL_ALLOWED = ('SRB_ROT', 'RB_FP', 'T2I', 'EA', 'MT', 'I1T', 'FLAG_RULINGS', 'HARMONICS', 'SR_K')
REGISTRY_KEYS = ('schema', 'producers', 'identity_comparators', 'identity_tokens', 'gate_records', 'gq_all_nodes_counts', 'note')
IDENTITY_GATES = ('B1', 'B1_OFF', 'B0prime_RERUN')
# reported only (the registry decides): the comparator c2v004 bytes of gates_v004 (A57.3; an r5 pin-swap successor is pending)
IDENTITY_COMPARATOR_C2V004 = (ART + '/tail_scheme_impl_c2/gates_v004/run_identity_compare_c2v004.py',
                              'e3d153b6dd5bf07ffd74ca8eeb75087d7a1bfd5cab67039c5514fa8744f7abcf')
# R7 [A62.1] the RB_FP shell domain: the C4T tail domain, from the kept cube K = 4 (R1 cube_K4) to |k| = sqrt(2) x P (the
# cylinder K_big = P reaches |k| = sqrt(2) P; the launch-packet shell producer cuts at the same top)
RB_FP_DOMAIN_LOWER = 4.0
RB_FP_DOMAIN_FACTOR_OF_P = math.sqrt(2.0)
T3_KBIG_FACTOR = {'C4T-KLO': 0.5, 'C4T-KHI': 2.0}
COVERAGE_FACTOR_OF_2P = math.sqrt(2.0)
R1_DDO_COVERAGE_EDGE = 64.0                                 # [R1 EPS] DDO [2, 64]; [R1 LO] shells to (32, 64]; [RA7] C4T to 64
LO_COVERAGE_LOWER = 4.0                                     # [R1 LO] the shells start at K = 4
# [A54 S8] the registered tail content per T-case (RA1 / RA2 / R1 run list, generic T3): the uv_tail of every T-case equals
# C4T's except at the registered differing keys below; source_rule continuum_v001 except C4T-D5 (nodes_v001 with ext_grid = the
# registered G5 grid, RA1 'nodes_v001 tail on G5\\G4'); outer cylinder K_big = P except C4T-KLO (P/2), C4T-KHI (2P) and
# C4T-C5c (cube K_out 5, RA2); lambda_scale 1.0 except C4T-A (1.05, R1 RB_FP_run); enabled and lapse_only true.
UV_TAIL_DIFFERING_KEYS = ('outer', 'lambda_scale', 'source_rule')
C5C_OUTER = {'shape': 'cube', 'K_out_inverse_kpc': 5.0}                                              # [RA2]
C4TA_LAMBDA_SCALE = 1.05                                                                            # [R1 RB_FP_run]

# ============================================================================================ registered constants
SCHEMA_REPORT = 'UNT_KMAX_TAIL_COMPARISON_C2V007_R11'
MANIFEST_SCHEMA = 'UNT_KMAX_TAIL_V007_MANIFEST_C2V002'            # R5 [A54]: T3 pair ids T3_KLO / T3_KHI
CASE_BLOCK_SCHEMA = 'UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V003'       # R1: /numerics whole, key map; R5 [A54]: KLO/KHI, S8 content
GATE_SCHEMA = 'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002'            # R1: EA row radii, FLAG_RULINGS disposition, gate I4
UVT_RA_RECORD_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_RECORD_C2V001'      # route_a_uv_tail_controller_c2v001 result_record
RESULT_SCHEMA = 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001'
RECEIPT_SCHEMA = 'UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001'
T_CASES = ('C2T', 'C3T', 'C4T', 'C6T', 'S4T', 'C4T-D5', 'C4T-C5c', 'C4T-KLO', 'C4T-KHI', 'C4T-A')   # [RA4] [RA11]
C5H = 'C5H'                                                                                            # [RA1] [A44]
REGISTERED = T_CASES + (C5H,)
IDENTITY_RUNS = ('Z2', 'Z2-OFF', 'B0prime_RERUN')                                                      # [A47 I1] [A47 I6]
IDENTITY_GATE_OF_RUN = {'Z2': 'B1', 'Z2-OFF': 'B1_OFF', 'B0prime_RERUN': 'B0prime_RERUN'}
EXPECTED_GRID = {'C2T': 'G2', 'C3T': 'G3', 'C4T': 'G4', 'C6T': 'G6', 'S4T': 'G4', 'C4T-D5': 'G4', 'C4T-C5c': 'G4',
                 'C4T-KLO': 'G4', 'C4T-KHI': 'G4', 'C4T-A': 'G4', 'C5H': 'G5'}
EXPECTED_TRUNCATION = {c: {'shape': 'cube', 'kmax_inverse_kpc': None} for c in REGISTERED}
EXPECTED_TRUNCATION['S4T'] = {'shape': 'sphere', 'kmax_inverse_kpc': 4.0}                             # [R1 T1_S]
ROUTE_A_MAX_ITERATIONS = 32                                                                            # [A47 I5]
ROUTE_A_MODES = {   # [A47 I4] the single declared parameter; default parallel8
    'parallel8': {'t_case_column_workers': 8, 'c4td5_exempt': ('composite_grid_spec', 'uv_tail')},
    'serial_with_exemption': {'t_case_column_workers': 1, 'c4td5_exempt': ('composite_grid_spec', 'uv_tail', 'route_a.column_workers')}}
ROUTE_A_MODE_DEFAULT = 'parallel8'
C5H_ROUTE_A = {'column_workers': 8, 'max_iterations': 32}                                              # C5H spec 60b46130
RPAIR_PICARD = {'passes': 12, 'speed_change_bound_km_s': 0.0025, 'observe_every_pass': True}           # [R1 R-PAIR]
RPAIR_ROUTE_A_POINTER = '/numerics/route_a/seed_source_rtol_factor'                                     # [A48 AMB-14]
RPAIR_ROUTE_A_FACTOR = 0.1                                                                             # seed source_rtol/10
SEED_FACTOR_ABSENT_EQUIVALENT = 1.0                                                                    # [A48 AMB-14] absent = 1.0
RPAIR_PICARD_EXEMPT = ('/numerics/picard/passes', '/numerics/picard/speed_change_bound_km_s', '/numerics/route_a/column_workers',
                       '/admit')        # [A53] column_workers 1 is a registered Picard leaf (the member admits the base route A)
RPAIR_PICARD_COLUMN_WORKERS = 1        # [A53] v010 r4 L1404: an admitted route A requires column_workers 1 (planning only)
# [A50 B1] the registered R-PAIR leaves inside /numerics, per branch: the only leaves an R-PAIR member may differ from its
# base at, and the leaves that must be byte-equal between the two members (R1 'byte-equal between members')
RPAIR_NUMERICS_LEAVES = {'PICARD': ('picard.passes', 'picard.speed_change_bound_km_s', 'route_a.column_workers'),   # [A53]
                         'ROUTE_A': ('route_a.seed_source_rtol_factor',)}
RPAIR_BRANCH_E_UNAVAILABLE = 'PICARD'   # [A48 AMB-05] E unavailable -> R-PAIR; [A50 root item 1] branch PICARD (agreed)
TINY_FRACTION = 1.0 / 8.0                                                                              # [RA6] TINY
DECIDABLE_FRACTION = 1.0 / 8.0                                                                         # [R1 decidable_iff]
TH = {'T1_H': 0.5, 'T2': 0.25, 'T2c': 0.5, 'T3': 0.25, 'T1_S': 2.0, 'NOT_UV_T2c': 0.25, 'NOT_UV_SRK': 0.25,
      'RB_FP': 0.1, 'SRB_ROT': 0.1}
LAMBDA_STEP = 0.05                                                                                     # [R1 RB_FP] lambda 1.05
RB_FP_FACTOR = 2.0
MT_THRESHOLD = 0.25                                                                                    # [R1 MT_monitor]
# [A49.1] [A50 'A49 in the compare'] the three EXACT raised texts (str(exc)) = RO1_MESSAGES of the RO1 c2v002 binding and driver
# patch, including the full e9be043b L205 string (R1 carried the bare token 'DEGENERATE_RADIAL_EULER': corrected in R2)
READOUT_REFUSALS = ('NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH',
                    'DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed',
                    'NON_TIMELIKE_COLUMN')
MT_FAIL_VERDICT = 'FAIL'           # [A50 S2] an MT record whose run M_T(accepted) > 1/4 carries verdict FAIL (that run is flagged)
RO1_CODE = 'ROUTE_A_READOUT_NO_CIRCULAR_BRANCH'
FLAG_TSU = 'TAIL_SOURCE_UNDERCONVERGED'
FLAG_SQM = 'SOURCE_QUADRATURE_MATERIAL'
PAIRS = {'T1_H': ('C4T', 'C6T'), 'T1_S': ('C4T', 'S4T'), 'T2': ('C5H', 'C4T-D5'), 'T2c': ('C4T-D5', 'C4T-C5c'),
         'T3_KLO': ('C4T', 'C4T-KLO'), 'T3_KHI': ('C4T', 'C4T-KHI'), 'RB_FP': ('C4T', 'C4T-A')}
DECIDABILITY_PAIRS = ('T1_H', 'T2', 'T3_KLO', 'T3_KHI')                                                # AMB-06
TEST_RUNS = {'T1': ('C2T', 'C3T', 'C4T'), 'T1_H': PAIRS['T1_H'], 'T1_S': PAIRS['T1_S'], 'T2': PAIRS['T2'],
             'T2c': PAIRS['T2c'], 'T3': ('C4T', 'C4T-KLO', 'C4T-KHI'), 'RB_FP': PAIRS['RB_FP']}
NO_RUN_GATES = ('B0', 'B0prime_DRY', 'B0prime_RERUN', 'B0_FA', 'B1', 'B1_OFF', 'B2', 'B3', 'B0_RO1', 'B0_N3')  # AMB-01
CERT_NUMERICS_GATES = ('EPS', 'DOUBLING', 'GQ')                                                        # [RA7] GQ
CERT_LAPSE_GATES = ('LO',)
OTHER_REQUIRED_GATES = ('I1T', 'T2I', 'SRB_ROT', 'RB_FP', 'SR_K', 'EA')
MODE_GATES = ('I4',)              # [A47 I4] [verify D7] required in route-A mode parallel8 only
OPTIONAL_GATES = ('LO_NGC', 'MT', 'HARMONICS', 'FLAG_RULINGS')
REQUIRED_GATES = NO_RUN_GATES + CERT_NUMERICS_GATES + CERT_LAPSE_GATES + OTHER_REQUIRED_GATES
ALL_GATES = REQUIRED_GATES + MODE_GATES + OPTIONAL_GATES
RPAIR_IDS = DECIDABILITY_PAIRS
# R6 [A56 N2] RB_FP has a PICARD R-PAIR: when the E of C4T or C4T-A is unavailable (NEW-7, A56 N1, a B4 gap, no increment), RB_FP
# reads E (and rows) from 12-pass PICARD reruns admitting their base route A, '<C4T|C4T-A>@RPAIR:RB_FP'.  RB_FP is not a
# decidability pair (AMB-06); it joins the RESOLVABLE list (A54 B4).  Manifest key 'RB_FP', branch PICARD only.
RPAIR_RB_FP = 'RB_FP'
RPAIR_MANIFEST_IDS = RPAIR_IDS + (RPAIR_RB_FP,)
RPAIR_RESOLVABLE = DECIDABILITY_PAIRS + (RPAIR_RB_FP,)
# [verify D4] pairs whose registered uv_tail differ by the text (K_big P/2, P, 2P [A54]; lambda_scale 1.05; K_out 5 / nodes_v001)
UV_TAIL_MUST_DIFFER = (('C4T', 'C4T-KLO'), ('C4T', 'C4T-KHI'), ('C4T-KLO', 'C4T-KHI'), ('C4T', 'C4T-A'), ('C4T-D5', 'C4T-C5c'))
GQ_GEOMETRY_DOMAIN = {'DDO': (2.0, 64.0), 'NGC': (2.0, 32.0)}     # [A48 AMB-12]; R5 [A54]: the DDO edge is max(64, 2P)
GQ_ROSTER_NAMES = tuple('DDO_' + c for c in T_CASES) + ('NGC_T120L',)
FLAG_DISPOSITIONS = ('CLEARED', 'RERUN_ORDERED')                                                       # [A48 AMB-19]
I4_PASS_VERDICT = 'PASS_SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON'

# [A50 'Outcome order, final'] 1 NO_RUN, INCOMPLETE, NUMERICS_UNCERTIFIED / NON_LAPSE_TAIL_MATERIAL; 2 the decided failure
# outcomes in R1 order; 3 UNDECIDABLE_ROUTE_A_TAIL; 4 UNDECIDABLE_AT_ITERATION_FLOOR; 5 FLAG_PENDING_RULING; 6 ADOPT_TAIL.
# 'position' in the report = index in OUTCOME_ORDER (+1; NON_LAPSE shares NUMERICS_UNCERTIFIED's); 'a50_group' = 1..6.
DECIDED_FAILURES = ('IMPLEMENTATION_DEFECT', 'SOURCE_RULE_MATERIAL', 'KBIG_NOT_CONVERGED', 'BOUND_INSUFFICIENT', 'FLOOR_LIKE',
                    'NOT_UV_RESIDUAL', 'SOURCE_REPRESENTATION_K_DEPENDENT', 'HIGHER_K_DISAGREEMENT', 'SHAPE_DISAGREEMENT')
OUTCOME_ORDER = (('NO_RUN', 'INCOMPLETE', 'NUMERICS_UNCERTIFIED') + DECIDED_FAILURES
                 + ('UNDECIDABLE_ROUTE_A_TAIL', 'UNDECIDABLE_AT_ITERATION_FLOOR', 'FLAG_PENDING_RULING', 'ADOPT_TAIL'))
A50_GROUP = dict([(o, 1) for o in ('NO_RUN', 'INCOMPLETE', 'NUMERICS_UNCERTIFIED', 'NON_LAPSE_TAIL_MATERIAL')]
                 + [(o, 2) for o in DECIDED_FAILURES]
                 + [('UNDECIDABLE_ROUTE_A_TAIL', 3), ('UNDECIDABLE_AT_ITERATION_FLOOR', 4), ('FLAG_PENDING_RULING', 5), ('ADOPT_TAIL', 6)])


def outcome_position(o):
    return OUTCOME_ORDER.index('NUMERICS_UNCERTIFIED' if o == 'NON_LAPSE_TAIL_MATERIAL' else o) + 1


# [A50 PROVISIONAL] the earliest outcome each test unit can produce when it resolves (a pending unit 'sits at' that position)
UNIT_EARLIEST_OUTCOME = {'T1': 'FLOOR_LIKE', 'T1_H': 'HIGHER_K_DISAGREEMENT', 'T1_S': 'SHAPE_DISAGREEMENT',
                         'T2': 'IMPLEMENTATION_DEFECT', 'T2c': 'SOURCE_RULE_MATERIAL', 'T3_KLO': 'KBIG_NOT_CONVERGED',
                         'T3_KHI': 'KBIG_NOT_CONVERGED', 'RB_FP': 'BOUND_INSUFFICIENT', 'SRB_ROT': 'BOUND_INSUFFICIENT'}
# [A50 N1] stage names reach a code only through this exact allow-list of driver constants (v009-EXT / v010 stage_dir names:
# body, offset, reference, route_a, route_a_tail_manifest; <tag>_{columns, columns_NN, rotation, feedback, column_mean} with
# tag fs, rfs, le1..le12 and NN the '%02d' column-chunk index); any other name becomes STAGE_NOT_ON_ALLOW_LIST
STAGE_NAMES = frozenset(('body', 'offset', 'reference', 'route_a', 'route_a_tail_manifest')
                        + tuple('%s_%s' % (t, x) for t in ('fs', 'rfs') + tuple('le%d' % p for p in range(1, 13))
                                for x in ('columns', 'rotation', 'feedback', 'column_mean') + tuple('columns_%02d' % j for j in range(100))))
STAGE_OTHER = 'STAGE_NOT_ON_ALLOW_LIST'
# [R3 validity F4] the other record-controlled identifiers that reach a code are bounded by registered constants: a bracket
# failure's column index by the DDO154 column count (v010 L406 / v009 DDO154 radial.n_columns = 72), a final-pass number by
# the largest registered pass count (R-PAIR Picard 12); V3 numerics diff paths are emitted only when every key is a key of
# the registered numerics (case block /numerics, C5H spec reference), else NUMERICS_PATH_NOT_REGISTERED.
DDO_N_COLUMNS = 72
MAX_REGISTERED_PASSES = 12
NUMERICS_PATH_OTHER = 'NUMERICS_PATH_NOT_REGISTERED'

NEXT_STEP = {  # [R1 outcomes_first_applicable] verbatim next steps
    'NO_RUN': 'fix and re-review (B2/B3 failure = IMPLEMENTATION_DEFECT of the gate); a missing gate record: produce it (RA13)',
    'INCOMPLETE': 'per case/gate below; no T-test is read (A47 I1)',
    'NUMERICS_UNCERTIFIED': 'named successor (EPS: EPS_UNCERTIFIED blocks all T runs; GQ: UV_TAIL_GAS_QUADRATURE_UNCERTIFIED; '
                            'DOUBLING: quadrature successor)',
    'NON_LAPSE_TAIL_MATERIAL': 'a design successor carrying all 10 components; no T run starts',
    'UNDECIDABLE_ROUTE_A_TAIL': 'rerun that case with seed source_rtol/10',
    'UNDECIDABLE_AT_ITERATION_FLOOR': 'reported; the test neither passes nor fails; no adoption',
    'IMPLEMENTATION_DEFECT': 'stop, T1/T3 not read as physics',
    'SOURCE_RULE_MATERIAL': 'root ruling on the gas rule before adoption',
    'KBIG_NOT_CONVERGED': 'production K_big 64 under T3prime (32/64/128), EPS and LO to 128',
    'BOUND_INSUFFICIENT': 'q-corrected shell (second asymptotic order), design successor',
    'FLOOR_LIKE': 'a floor clause needs a new prereg version before any further case',
    'NOT_UV_RESIDUAL': 'column/Picard map, own prereg',
    'SOURCE_REPRESENTATION_K_DEPENDENT': 'fixed-point SR runs C2T-SR/C3T-SR/C4T-SR (packets over the smooth source), own design and prereg',
    'HIGHER_K_DISAGREEMENT': 'adopt nothing; C6T candidate under a V007 amendment sealed before further results',
    'SHAPE_DISAGREEMENT': 'review per-stage C wiring',
    'FLAG_PENDING_RULING': 'no adoption; root rules on the flag',
    'ADOPT_TAIL': 'calibration numerics: cube K=4 tail-corrected (the C4T configuration) with u_i carried; V005 S1 transfer test '
                  'at the calibrated point before prediction (scope_untested S1)'}
RA4_NEXT = ('BRACKET_HULL_MISS (RA4): a miss under the full-hull bracket block makes the case invalid; there is no W1 widening '
            'clause; the next step is its own registration')
AMB16_NEXT = 'named defect %s: fix and rerun that case under V007 with thresholds unchanged (A48 AMB-16)'
T2I_DEFECT_NEXT = 'IMPLEMENTATION_DEFECT (T2I): stop; the comparison object is not faithful (A48 AMB-10); T1/T3 not read as physics'
I4_NEXT = ('A47 I4 condition not confirmed: every T-case runs serial (route-A mode serial_with_exemption), the declared '
           'column_workers exemption returns, and I4 is reported')


class DuplicateKey(ValueError):
    """[verify D8] R10 [A71]: .code names both members by position (object ordinal in parse order, member indices), never the key
    text (record-controlled, A54 S6)."""

    def __init__(self, code='DUPLICATE_JSON_KEY'):
        self.code = code
        super().__init__(code)


class DuplicateEntry(ValueError):
    """R10 [A71] a list-to-mapping conversion met two entries with one key: a RECORD_DEFECT naming both entries (by index; the key
    itself is record-controlled and never emitted, A54 S6).  .codes: the defect codes (inside a gate: the gate is RECORD_DEFECT)."""

    def __init__(self, codes):
        self.codes = list(codes) if isinstance(codes, (list, tuple)) else [codes]
        super().__init__(';'.join(self.codes))


def duplicate_entry_code(where, what, i, j):
    return 'DUPLICATE_ENTRY_A71:%s:%s[%d]:%s[%d]' % (where, what, i, what, j)


def unique_map(pairs, where, what):
    """R10 [A71] the ONE list-to-mapping builder: pairs [(key, value)] in list order; a repeated key raises DuplicateEntry naming
    the first and the repeating entry; else the mapping (insertion order = list order)."""
    out, first = {}, {}
    for j, (k, v) in enumerate(pairs):
        if k in first:
            raise DuplicateEntry(duplicate_entry_code(where, what, first[k], j))
        first[k] = j
        out[k] = v
    return out


def unique_keys_codes(keys, where, what):
    """R10 [A71] the same check as unique_map for a list whose keys feed a mapping or a set: [] or every duplicate's code."""
    first, out = {}, []
    for j, k in enumerate(keys):
        if k in first:
            out.append(duplicate_entry_code(where, what, first[k], j))
        else:
            first[k] = j
    return out


def _hook_factory():
    n = [0]

    def hook(pairs):
        """[verify D8] R10 [A71] json object_pairs_hook: a duplicate key is refused before the object is built (json would keep the
        last value silently); the code names both members by index and the object by its parse ordinal."""
        out, first = {}, {}
        for j, (k, v) in enumerate(pairs):
            if k in first:
                raise DuplicateKey('DUPLICATE_JSON_KEY_A71:object[%d]:members[%d]:members[%d]' % (n[0], first[k], j))
            first[k] = j
            out[k] = v
        n[0] += 1
        return out
    return hook


def _no_dup_pairs(pairs):
    """Kept for callers of r8: a one-object hook (ordinal 0)."""
    return _hook_factory()(pairs)


def loads_strict(raw):
    return json.loads(raw, object_pairs_hook=_hook_factory())


class Refused(SystemExit):
    """R10 [Codex2 0442 S1]: .refusal_code is a fixed code (never record content): the only text a blinded mode prints.
    R11 [A79.6 / A75.3] .refusal_naming: for a duplicate refusal, the positions of BOTH entries (a DUPLICATE_ENTRY_A71 /
    DUPLICATE_JSON_KEY_A71 code built by this script from indices and constant list names only); printed in every mode, because
    it carries no record-controlled text (refusal_text re-checks its grammar)."""

    def __init__(self, msg='REFUSED', code=None, naming=None):
        super().__init__(msg)
        self.refusal_code = code
        self.refusal_naming = naming


REFUSAL_CODE_UNCODED = 'REFUSED_UNCODED'
_RE_REFUSAL_CODE = re.compile(r'[A-Z][A-Z0-9_]*\Z')
# R11 [A79.6] the grammar of a naming code: DUPLICATE_ENTRY_A71 / DUPLICATE_JSON_KEY_A71 fields that are constant list names with
# indices (object[n], members[i], <list>[i], argv[i]); ';' joins several.  Anything else is withheld (never printed).
_RE_NAMING_FIELD = r'(?:[A-Za-z][A-Za-z0-9_/\-]*(?:\[[0-9]{1,6}\])*)'      # no '.': a record number cannot pass
_RE_NAMING_ONE = r'DUPLICATE_(?:ENTRY|JSON_KEY)_A71(?::%s)+' % _RE_NAMING_FIELD
_RE_NAMING = re.compile(r'%s(?:;%s)*\Z' % (_RE_NAMING_ONE, _RE_NAMING_ONE))
NAMING_WITHHELD = 'NAMING_WITHHELD_NOT_A_POSITION_CODE'


def naming_text(n):
    """R11 [A79.6] a naming code is printed only when it matches the position grammar (indices and constant names only)."""
    if n is None:
        return None
    return n if (isinstance(n, str) and _RE_NAMING.match(n)) else NAMING_WITHHELD


def refusal_text(exc, blinded):
    """R10 [Codex2 0442 S1] (A54 S6, A47 I3): in --validity-only / --gates-only every early refusal prints ONLY its fixed code (a
    compare constant: no record-controlled key, label, path or number); in the other modes the full text, as before.  R11 [A79.6]
    a duplicate refusal also prints the positions of both entries (index naming; blinding-safe by construction and by grammar)."""
    nm = naming_text(getattr(exc, 'refusal_naming', None))
    if not blinded:
        return str(exc) + ('' if nm is None or nm in str(exc) else ' [%s]' % nm)
    c = getattr(exc, 'refusal_code', None)
    if not (isinstance(c, str) and _RE_REFUSAL_CODE.match(c) and not re.search(r'\d{5,}', c)):
        c = REFUSAL_CODE_UNCODED
    return 'REFUSED: %s%s (blinded mode: refusal detail withheld, A54 S6 / A47 I3)' % (c, '' if nm is None else ' [%s]' % nm)


class FieldMissing(Exception):
    """A record lacks a field the compare reads (or has the wrong type): the gate FAILS loudly naming it (E-SEAL1)."""

    def __init__(self, where, path, problem='MISSING'):
        self.code = 'FIELD_%s:%s:%s' % (problem, where, path)
        super().__init__(self.code)


# ============================================================================================ small helpers
def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _hex64(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


KINDS = {
    'str': lambda x: isinstance(x, str) and x != '',
    'bool': lambda x: isinstance(x, bool),
    'int': lambda x: isinstance(x, int) and not isinstance(x, bool),
    'num': _num,
    'num>=0': lambda x: _num(x) and x >= 0,
    'list': lambda x: isinstance(x, list),
    'nonempty_list': lambda x: isinstance(x, list) and len(x) > 0,
    'dict': lambda x: isinstance(x, dict),
    'sha': _hex64,
    'num12': lambda x: isinstance(x, list) and len(x) == 12 and all(_num(v) for v in x),
    'num12>=0': lambda x: isinstance(x, list) and len(x) == 12 and all(_num(v) and v >= 0 for v in x),
    'range2': lambda x: isinstance(x, list) and len(x) == 2 and all(_num(v) for v in x),
    'num|null': lambda x: x is None or _num(x),                                   # [R3 validity F1] RO1 event fields
    'int|null': lambda x: x is None or (isinstance(x, int) and not isinstance(x, bool)),
    'any': lambda x: True}


def need(obj, path, where, kind=None, read=None):
    """Read a '/'-separated path from obj; FieldMissing (named) if absent or of the wrong kind."""
    if read is not None:
        read.append(path)
    cur = obj
    for k in path.split('/'):
        if not isinstance(cur, dict) or k not in cur:
            raise FieldMissing(where, path)
        cur = cur[k]
    if kind is not None and not KINDS[kind](cur):
        raise FieldMissing(where, path, 'TYPE_' + kind)
    return cur


def jptr(obj, pointer):
    """RFC-6901-style pointer ('/a/b'); returns (found, value)."""
    cur = obj
    for k in pointer.lstrip('/').split('/'):
        k = k.replace('~1', '/').replace('~0', '~')
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return False, None
    return True, cur


def load_pinned_module(path, sha, name):
    if sha256_file(path) != sha:
        raise Refused('REFUSED: pin mismatch %s' % path, 'PIN_MISMATCH')
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_pinned_json(pin):
    path, sha = pin
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refused('REFUSED: pin mismatch %s (sha %s, pinned %s)' % (path, sha256_bytes(raw), sha), 'PIN_MISMATCH')
    try:
        return loads_strict(raw)                     # R10 [A71] pinned bytes are parsed strictly too (r8: json.loads, last-wins)
    except DuplicateKey as exc:
        raise Refused('REFUSED: pinned file %s has a duplicate JSON key (%s)' % (path, exc.code), 'PINNED_FILE_DUPLICATE_JSON_KEY_A71',
                      exc.code)


def _read_json(p):
    """Strict read: a duplicate key raises DuplicateKey (verify D8)."""
    raw = Path(p).read_bytes()
    return loads_strict(raw), sha256_bytes(raw)


def dup_naming_code(exc, tag):
    """R11 [A79.6 / A75.3] (Claude3 0070 §2; Codex2 CX2-R10-A71-S2, BR-S2): the both-entry position code of a DuplicateKey met while
    reading a <tag> file: DUPLICATE_JSON_KEY_A71:object[n]:members[i]:members[j]:<TAG> (indices only; never the key text); None for
    any other exception."""
    return '%s:%s' % (exc.code, tag) if isinstance(exc, DuplicateKey) and isinstance(getattr(exc, 'code', None), str) else None


def _side_json(p, tag, codes):
    """[verify N3] a side file (finish/receipt/start/stage finish): absent -> None; unreadable -> loud code, never an exception.
    R11 [A79.6]: a duplicate key also appends the both-entry position code (the r10 code <TAG>_UNREADABLE:DuplicateKey is kept)."""
    if not Path(p).is_file():
        return None
    try:
        return _read_json(p)[0]
    except Exception as exc:
        codes.append('%s_UNREADABLE:%s' % (tag, type(exc).__name__))
        nc = dup_naming_code(exc, tag)
        if nc:
            codes.append(nc)
        return None


# ============================================================================================ context
def ra4_block_expected():
    """[RA4] the C5H bracket block as A46 lists it; checked equal to the C5H spec bytes at every start."""
    return {'mode': 'rule', 'rule': {'fs_absolute_overrides': {str(i): [151250000.0, 317625000.0] for i in range(72)},
                                     'le_factor_overrides': {}, 'le_first_factors': [0.4, 0.9], 'le_next_factors': [0.8, 1.1],
                                     'rfs_factor_overrides': {'71': [0.8, 1.01]}, 'rfs_factors': [0.8, 1.2]}}


_UVT_LIB = {}


def load_uvt_lib():
    """[verify fields S4] the pinned, inert tail library (normalize_config only); REFUSED on a pin mismatch."""
    if 'lib' not in _UVT_LIB:
        _UVT_LIB['lib'] = load_pinned_module(PIN_UVT_LIB[0], PIN_UVT_LIB[1], 'owned_uv_tail_lapse_v001_pinned')
    return _UVT_LIB['lib']


def registered_row_radii(ids):
    """[A48 AMB-22] the 12 registered row radii (m) in row_ids order, from the pinned binding query_rows[].{id, radius_m}."""
    b = load_pinned_json(PIN_ROW_RADII_BINDING)
    try:                                                                    # R10 [A71] a repeated row id refuses (r8: last-wins)
        q = unique_map([(x['id'], x['radius_m']) for x in b['query_rows']], 'ROW_RADII_BINDING', 'query_rows')
    except DuplicateEntry as exc:
        raise Refused('REFUSED: row-radius binding: %s' % exc.codes[0], 'ROW_RADII_BINDING_DUPLICATE_ROW_ID_A71', exc.codes[0])
    if sorted(q) != sorted(ids) or not all(_num(q[i]) and q[i] > 0 for i in ids):
        raise Refused('REFUSED: row-radius binding query_rows do not carry the 12 registered row ids with finite radii',
                      'ROW_RADII_BINDING_NOT_THE_12_ROW_IDS')
    return [float(q[i]) for i in ids]


def radii_equal(got, want):
    return (isinstance(got, list) and len(got) == len(want) and all(_num(g) for g in got)
            and all(abs(g - w) <= ROW_RADII_REL_TOL * abs(w) for g, w in zip(got, want)))


def _spec_leaves(o, p=''):
    """Leaf map {pointer: canonical value}.  R10 [A71] (Claude3 helper I item 5): a key containing '/' could collide with a nested
    path and update() would keep the last; a collision now raises DuplicateEntry (pinned specs only: build_context REFUSES)."""
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            for kk, vv in _spec_leaves(v, p + '/' + str(k)).items():
                if kk in out:                    # R11 [A79.6] both entries named by their member index in this object
                    ks = list(o)
                    j0 = next((ks.index(k0) for k0 in ks if any(x == kk for x in _spec_leaves(o[k0], p + '/' + str(k0)))), -1)
                    raise DuplicateEntry('DUPLICATE_ENTRY_A71:SPEC_LEAVES:pointer_collision:members[%d]:members[%d]' % (j0, ks.index(k)))
                out[kk] = vv
        return out or {p: '{}'}
    return {p: canon(o)}


def c5h_admission_bases():
    """[A50 AMB-20 restated] C5H is admitted on three grounds, all from pinned bytes: (1) REVIEW_V009 3bce7c02 verdict PASS
    (0 blocking findings) for driver 999331af and the C5 spec 09ff5a96; (2) the byte diff of the C5H spec 60b46130 against
    09ff5a96 is limited to /label and /numerics/brackets/rule/fs_absolute_overrides (any other difference: not admitted);
    (3) the clean dry run cbd2885d (60b46130 / 999331af, no blocker, no unexplained refusal).  The literal A48 premise
    ('shas_reviewed carries both shas') is false on bytes (A50, TESTED); it is reported, never a ground.
    [A50 S1] Also returns the reference numerics of the C5H run: the dry run's normalized_spec.numerics, admitted only if the
    dry-run normalization ADDS leaves to the spec numerics and changes or removes none (it adds truncation.kmax_inverse_kpc)."""
    rv = load_pinned_json(PIN_REVIEW_V009)
    dry = load_pinned_json(PIN_C5H_DRYRUN)
    reviewed_spec = load_pinned_json(PIN_C5R3_SPEC_REVIEWED)
    c5h_spec = load_pinned_json(PIN_C5H_SPEC)
    sr = rv.get('shas_reviewed') or {}
    reviewed = {(x or {}).get('sha256') for x in sr.values() if isinstance(x, dict)}
    dnum = ((dry.get('normalized_spec') or {}).get('numerics'))
    try:                                                                  # R10 [A71] a leaf-pointer collision refuses
        la, lb = _spec_leaves(c5h_spec), _spec_leaves(reviewed_spec)
        ls, ld = _spec_leaves(c5h_spec['numerics']), _spec_leaves(dnum if isinstance(dnum, dict) else {})
    except DuplicateEntry as exc:
        raise Refused('REFUSED: C5H admission bases: %s' % exc.codes[0], 'C5H_ADMISSION_SPEC_LEAF_COLLISION_A71', exc.codes[0])
    diff = sorted(k for k in set(la) | set(lb) if la.get(k) != lb.get(k))
    off = [k for k in diff if not (k == C5H_SPEC_ALLOWED_DIFF_FROM_REVIEWED[0] or k.startswith(C5H_SPEC_ALLOWED_DIFF_FROM_REVIEWED[1]))]
    rr = dry.get('remaining_refusals') or {}
    changed = sorted(k for k in ls if ld.get(k) != ls[k])
    added = sorted(k for k in ld if k not in ls)
    checks = {
        'review_verdict_PASS': rv.get('verdict') == 'PASS',
        'review_no_blocking_findings': rv.get('blocking_findings') == 0,
        'review_shas_reviewed_driver_v009_EXT_is_999331af': (sr.get('driver_v009_EXT') or {}).get('sha256') == DRIVER_V009_EXT,
        'review_shas_reviewed_carries_C5_spec_09ff5a96': PIN_C5R3_SPEC_REVIEWED[1] in reviewed,
        'C5H_spec_differs_from_reviewed_09ff5a96_only_at_label_and_fs_absolute_overrides': bool(diff) and not off,
        'dryrun_call_spec_is_60b46130': dry.get('call_spec_sha256') == PIN_C5H_SPEC[1],
        'dryrun_driver_is_999331af': dry.get('driver_sha256') == DRIVER_V009_EXT,
        'dryrun_binding_blockers_empty': dry.get('binding_blockers') == [],
        'dryrun_unexplained_refusals_empty': rr.get('unexplained') == [] and rr.get('beyond_pending_inputs') == [],
        'dryrun_normalized_numerics_only_add_to_the_spec_numerics': isinstance(dnum, dict) and not changed}
    return {'admitted': all(checks.values()), 'checks': checks, 'failed': sorted(k for k, v in checks.items() if not v),
            'grounds': 'A50 AMB-20 restated: review (999331af, 09ff5a96) + diff limited to label/fs_absolute_overrides + dry run',
            'a48_literal_premise_shas_reviewed_carries_60b46130': PIN_C5H_SPEC[1] in reviewed,
            'spec_diff_leaf_count_outside_allowed': len(off), 'spec_diff_leaves_outside_allowed': off[:8],
            'dryrun_normalization_added_leaves': added, 'dryrun_normalization_changed_leaves': changed,
            '_numerics_reference': json.loads(canon(dnum)) if isinstance(dnum, dict) else None}


def r5_custody_codes():
    """R7 [A62.3] the r5 custody pins against bytes and against the r5 cascade map (r4 sha -> r5 sha); [] when consistent."""
    why = []
    if sha256_file(PIN_DRIVER_V010_R5[0]) != PIN_DRIVER_V010_R5[1]:
        why.append('driver v010 r5 pin mismatch')
    cmap = (load_pinned_json(PIN_R5_CASCADE_MAP).get('declared_sha_map')) or {}
    want = {'driver': PIN_DRIVER_V010_R5[1], 'worker': PIN_RO1_CUSTODY['worker'][1],
            'worker_parallel': PIN_RO1_CUSTODY['worker_parallel'][1], 'nodes_worker': PIN_RO1_NODES_CUSTODY['worker'][1],
            'nodes_worker_parallel': PIN_RO1_NODES_CUSTODY['worker_parallel'][1]}
    for k, new in want.items():
        if cmap.get(R4_CUSTODY_SHAS[k]) != new:
            why.append('the r5 cascade map does not map the r4 %s to the pinned r5 sha' % k)
    if PIN_RO1_CUSTODY['binding'][1] in cmap:
        why.append('the r5 cascade map remaps the RO1 binding (A62.3: unchanged)')
    return why


# ============================================================================================ R10 [A72] the sealed driver build
def _pin_pair(x):
    return x if (isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and x['path'].startswith('/')
                 and _hex64(x['sha256'])) else None


def check_record_codes(path, driver_sha):
    """R11 (r10 recheck validity N2: any file whose bytes matched its pin was accepted as the build's check record, the LO certificate
    included) the check record of a BUILD must read as the independent check of THAT build: its text names the build's driver (the
    full sha256 or its 8-hex prefix, as the real r5 check driver_r5/check/CHECK.md does), carries a PASS verdict token (PASS or
    PASS_WITH_FINDINGS) within its first 4096 bytes, and is not a gate record (schema %s).  DECLARED minimal properties (NEW-73):
    the record format is root's.  [] or the reasons.""" % GATE_SCHEMA
    try:
        raw = Path(path).read_bytes()
    except OSError:
        return ['driver build: the check_record is unreadable']
    txt = raw.decode('utf-8', 'replace')
    out = []
    try:
        obj = json.loads(raw, object_pairs_hook=_hook_factory(), parse_int=str)  # R13 A102: no integer-limit bypass before duplicate checks.
    except DuplicateKey as exc:  # R12 A91 / CX2-R11-AB-B1: never downgrade duplicate JSON to text.
        return ['DRIVER_BUILD_CHECK_RECORD_DUPLICATE_JSON_KEY_A71', dup_naming_code(exc, 'CHECK_RECORD')]
    except json.JSONDecodeError:  # Only lexical JSON syntax failures retain the registered text fallback.
        obj = None
    except ValueError:
        return ['DRIVER_BUILD_CHECK_RECORD_UNREADABLE']
    if isinstance(obj, dict) and obj.get('schema') == GATE_SCHEMA:
        out.append('driver build: the check_record is a gate record, not a check of the build')
    if not (_hex64(driver_sha) and (driver_sha in txt or driver_sha[:8] in txt)):
        out.append('driver build: the check_record does not name the build\'s driver sha256')
    if not re.search(r'\bPASS(?:_WITH_FINDINGS)?\b', txt[:4096]):
        out.append('driver build: the check_record carries no PASS verdict token')
    return out


def builtin_r5_build():
    """The r8 (A62.3) custody pin set as a build object: driver v010 r5, the r5 cascade map, the r5 RO1 / nodes workers."""
    pp = lambda t: {'path': t[0], 'sha256': t[1]}
    return {'schema': DRIVER_BUILD_SCHEMA, 'build': 'r5', 'predecessor': 'r4', 'predecessor_shas': dict(R4_CUSTODY_SHAS),
            'driver': pp(PIN_DRIVER_V010_R5), 'cascade_map': pp(PIN_R5_CASCADE_MAP),
            'ro1_custody': {k: pp(v) for k, v in PIN_RO1_CUSTODY.items()},
            'ro1_nodes_custody': {k: pp(v) for k, v in PIN_RO1_NODES_CUSTODY.items()},
            'check_record': None if PIN_V010_R5_CHECK is None else pp(PIN_V010_R5_CHECK)}


def _build_shas(b):
    return {'driver': b['driver']['sha256'], 'worker': b['ro1_custody']['worker']['sha256'],
            'worker_parallel': b['ro1_custody']['worker_parallel']['sha256'],
            'nodes_worker': b['ro1_nodes_custody']['worker']['sha256'],
            'nodes_worker_parallel': b['ro1_nodes_custody']['worker_parallel']['sha256']}


def driver_build_codes(b):
    """R10 [A72] validate a driver BUILD object; [] when it is an admissible sealed-driver pin set (r5 or r6), else the reasons.
    Every file named is hashed from bytes."""
    why = []
    if not isinstance(b, dict) or b.get('schema') != DRIVER_BUILD_SCHEMA:
        return ['driver build schema must be %s' % DRIVER_BUILD_SCHEMA]
    if set(b) - set(DRIVER_BUILD_KEYS) or set(DRIVER_BUILD_KEYS) - set(b) - {'note', 'check_record'}:
        return ['driver build keys must be exactly %s (note, check_record optional)' % list(DRIVER_BUILD_KEYS)]
    if b.get('build') not in DRIVER_BUILDS:
        return ['driver build must be one of %s (A72: the sealed driver is v010 r5 or r6; anything else refused)' % list(DRIVER_BUILDS)]
    rc, nc = b.get('ro1_custody'), b.get('ro1_nodes_custody')
    if not (isinstance(rc, dict) and set(rc) == {'worker', 'worker_parallel', 'binding'} and all(_pin_pair(v) for v in rc.values())
            and isinstance(nc, dict) and set(nc) == {'worker', 'worker_parallel'} and all(_pin_pair(v) for v in nc.values())
            and _pin_pair(b.get('driver')) and _pin_pair(b.get('cascade_map'))
            and (b.get('check_record') is None or _pin_pair(b.get('check_record')))
            and isinstance(b.get('predecessor_shas'), dict) and set(b['predecessor_shas']) == set(CUSTODY_KEYS)
            and all(_hex64(v) for v in b['predecessor_shas'].values())):
        return ['driver build: driver / cascade_map / ro1_custody {worker, worker_parallel, binding} / ro1_nodes_custody {worker, '
                'worker_parallel} must be {path (absolute), sha256} pairs and predecessor_shas the five custody shas']
    files = [b['driver'], b['cascade_map']] + list(rc.values()) + list(nc.values()) + ([b['check_record']] if b.get('check_record') else [])
    for x in files:                                                                               # every sha from bytes
        try:
            if sha256_file(x['path']) != x['sha256']:
                why.append('driver build: a pinned file is not its sha from bytes (%s)' % os.path.basename(x['path']))
        except OSError:
            why.append('driver build: a pinned file is unreadable (%s)' % os.path.basename(x['path']))
    if b.get('check_record') and not why:                       # R11 (r10 recheck validity N2) the check record is a check of THIS build
        why += check_record_codes(b['check_record']['path'], b['driver']['sha256'])
    new = _build_shas(b)
    if len(set(new.values())) != len(new):                                                         # R10 [A71] no two pins alike
        why.append('driver build: two custody pins share one sha (the worker-kind maps would collapse, A71)')
    if b['build'] == 'r5':
        bb = {k: v for k, v in b.items() if k != 'note'}
        if canon(dict(bb, check_record=None)) != canon(dict(builtin_r5_build(), check_record=None)):
            why.append('driver build r5 must equal the built-in r5 set exactly (A62.3 pins, predecessor r4)')
        if PIN_V010_R5_CHECK is not None and b.get('check_record') != {'path': PIN_V010_R5_CHECK[0], 'sha256': PIN_V010_R5_CHECK[1]}:
            why.append('driver build r5 check_record must be PIN_V010_R5_CHECK')
        return why
    r5 = builtin_r5_build()
    old = _build_shas(r5)
    if b.get('predecessor') != 'r5' or b['predecessor_shas'] != old:
        why.append('driver build r6 must name predecessor r5 with the r5 custody shas (A72: a pin-only cascade from r5)')
    if rc['binding'] != r5['ro1_custody']['binding']:
        why.append('driver build r6 must keep the RO1 binding 86af6198 (A62.3: unchanged)')
    if new['driver'] == old['driver'] or os.path.basename(b['driver']['path']) != DRIVER_FILE_NAME:
        why.append('driver build r6 must name a new %s' % DRIVER_FILE_NAME)
    r6root = os.path.realpath(DRIVER_R6_DIR).rstrip('/') + '/'
    in_r6 = lambda p: os.path.realpath(p).startswith(r6root)
    for k, x in (('driver', b['driver']), ('cascade_map', b['cascade_map'])):
        if not in_r6(x['path']):
            why.append('driver build r6: the %s must lie under the driver_r6 tree' % k)
    r5files = {'worker': r5['ro1_custody']['worker'], 'worker_parallel': r5['ro1_custody']['worker_parallel'],
               'nodes_worker': r5['ro1_nodes_custody']['worker'], 'nodes_worker_parallel': r5['ro1_nodes_custody']['worker_parallel']}
    r6files = {'worker': rc['worker'], 'worker_parallel': rc['worker_parallel'], 'nodes_worker': nc['worker'],
               'nodes_worker_parallel': nc['worker_parallel']}
    for k in r5files:
        if not (in_r6(r6files[k]['path']) or r6files[k] == r5files[k]):
            why.append('driver build r6: the %s must lie under the driver_r6 tree, or be the unchanged r5 file' % k)
    try:
        cm = loads_strict(Path(b['cascade_map']['path']).read_bytes())
        cmap = cm.get('declared_sha_map') if isinstance(cm, dict) else None
    except (OSError, ValueError):
        cmap = None
    if not isinstance(cmap, dict):
        why.append('driver build r6: the cascade map carries no declared_sha_map')
        return why
    for k in CUSTODY_KEYS:
        if new[k] != old[k] and cmap.get(old[k]) != new[k]:
            why.append('driver build r6: the cascade map does not map the r5 %s to the pinned r6 sha' % k)
        if new[k] == old[k] and old[k] in cmap:
            why.append('driver build r6: the cascade map remaps the r5 %s, which the build keeps' % k)
    if rc['binding']['sha256'] in cmap:
        why.append('driver build r6: the cascade map remaps the RO1 binding (A62.3: unchanged)')
    return why


_BUILD = {'active': None}


def activate_driver_build(b=None):
    """R10 [A72] make b (default: the built-in r5 set) the active custody pin set of this process; REFUSED if inadmissible."""
    b = builtin_r5_build() if b is None else b
    why = driver_build_codes(b)
    if not why and b.get('build') == 'r5':
        why += r5_custody_codes()                                        # A62.3: the r5 pins are the r5 cascade images of r4
    if why:
        named = [c for c in why if isinstance(c, str) and _RE_NAMING.match(c)]
        raise Refused('REFUSED: driver build (A72): %s' % '; '.join(why), 'DRIVER_BUILD_NOT_ADMISSIBLE_A72',
                      ';'.join(named) or None)  # R12 A91: both positions survive blinded activation refusal.
    _BUILD['active'] = json.loads(canon(b))
    return _BUILD['active']


def load_driver_build_record(path, expected_sha=None):
    """R10 [A72] read a driver BUILD record strictly (a duplicate key refuses); expected_sha: the seal pin."""
    try:
        raw = Path(path).read_bytes()
    except OSError as exc:
        raise Refused('REFUSED: driver build record unreadable (%s)' % type(exc).__name__, 'DRIVER_BUILD_RECORD_UNREADABLE')
    if expected_sha is not None and sha256_bytes(raw) != expected_sha:
        raise Refused('REFUSED: driver build record sha mismatch (pinned %s)' % expected_sha, 'DRIVER_BUILD_RECORD_SHA_MISMATCH')
    try:
        obj = loads_strict(raw)
    except DuplicateKey as exc:                                                     # R11 [A79.6] both members named
        raise Refused('REFUSED: driver build record has a duplicate JSON key (%s)' % exc.code, 'DRIVER_BUILD_RECORD_DUPLICATE_JSON_KEY_A71',
                      exc.code)
    except ValueError as exc:
        raise Refused('REFUSED: driver build record unreadable (%s)' % type(exc).__name__, 'DRIVER_BUILD_RECORD_UNREADABLE')
    return obj, sha256_bytes(raw)


def active_build():
    if _BUILD['active'] is None:
        activate_driver_build(None)
    return _BUILD['active']


def sealed_driver_sha():
    """R10 [A72] the sealed driver (every T-case drivers_allowed, the I4 driver, the A67 N1 identity-run driver)."""
    return active_build()['driver']['sha256']


def ro1_custody_sha(k):
    return active_build()['ro1_custody'][k]['sha256']


def ro1_worker_kind():
    b = active_build()
    return {b['ro1_custody']['worker']['sha256']: 'serial', b['ro1_custody']['worker_parallel']['sha256']: 'parallel'}


def ro1_nodes_worker_kind():
    b = active_build()
    return {b['ro1_nodes_custody']['worker']['sha256']: 'serial', b['ro1_nodes_custody']['worker_parallel']['sha256']: 'parallel'}


def _file_pin_list(v):
    """R10 [A69 note 1] a registry list of {path, sha256} file pins (absolute path, 64-hex sha), no entry twice [A71]."""
    if not (isinstance(v, list) and all(_pin_pair(x) for x in v)):
        return None
    if unique_keys_codes([os.path.realpath(x['path']) for x in v], 'REGISTRY', 'entries') or \
            unique_keys_codes([x['sha256'] for x in v], 'REGISTRY', 'entries'):
        return None
    return v


def _file_pins_bytes_codes(entries):
    """R10 [A69 note 1] every registered file pin hashed from bytes: [] or the basenames that are missing / not their sha."""
    bad = []
    for x in entries:
        try:
            ok = sha256_file(x['path']) == x['sha256']
        except OSError:
            ok = False
        if not ok:
            bad.append(os.path.basename(x['path']))
    return bad


def registry_duplicate_naming(obj):
    """R11 [A79.6 / A75.3] (Claude3 0070 §2: the six registry-list duplicate forms named neither entry): the both-entry position code
    of the first duplicate in any registry list -- producers/<gate>, identity_comparators, identity_tokens/<gate> (a pin twice by
    realpath or by sha) and gate_records/<gate> (a sha twice) -- or None.  The gate names are registry keys checked against the
    registered gate set first (constants), so no record text enters a code."""
    def pins(v, where):
        if not (isinstance(v, list) and all(_pin_pair(x) for x in v)):
            return None
        for key in (lambda x: ('path', os.path.realpath(x['path'])), lambda x: ('sha', x['sha256'])):
            d = unique_keys_codes([key(x) for x in v], 'REGISTRY', where)
            if d:
                return d[0]
        return None
    prod, comp, tok, grec = obj.get('producers'), obj.get('identity_comparators'), obj.get('identity_tokens'), obj.get('gate_records')
    for g, v in sorted((prod or {}).items()) if isinstance(prod, dict) else []:
        if g in ALL_GATES:
            c = pins(v, 'producers/%s' % g)
            if c:
                return c
    c = pins(comp, 'identity_comparators')
    if c:
        return c
    for g, v in sorted((tok or {}).items()) if isinstance(tok, dict) else []:
        if g in IDENTITY_GATES:
            c = pins(v, 'identity_tokens/%s' % g)
            if c:
                return c
    for g, v in sorted((grec or {}).items()) if isinstance(grec, dict) else []:
        if g in ALL_GATES and isinstance(v, list) and all(_hex64(x) for x in v):
            d = unique_keys_codes(v, 'REGISTRY', 'gate_records/%s' % g)
            if d:
                return d[0]
    return None


def producer_registry_from_obj(obj, sha=None, path=None, verify_bytes=True):
    """R7 [A62.2] validate a producer registry object; returns the normalized registry, or raises Refused.  R10 [A69 note 1]
    schema C2V003: producers / identity_comparators / identity_tokens are {path, sha256} file pins, each file hashed from bytes
    here (verify_bytes; a missing file or a wrong sha REFUSES) and again at every gate read; [A71] a duplicate entry refuses;
    [NEW-52] the PRODUCED_AFTER_THE_SEAL token outside GATE_RECORD_AFTER_SEAL_ALLOWED refuses."""
    if not isinstance(obj, dict) or obj.get('schema') != PRODUCER_REGISTRY_SCHEMA:
        raise Refused('REFUSED: producer registry schema must be %s' % PRODUCER_REGISTRY_SCHEMA, 'PRODUCER_REGISTRY_SCHEMA')
    extra = set(obj) - set(REGISTRY_KEYS)
    if extra:
        raise Refused('REFUSED: producer registry: unknown keys %s' % sorted(extra), 'PRODUCER_REGISTRY_UNKNOWN_KEYS')
    missing = set(REGISTRY_KEYS) - {'note'} - set(obj)
    if missing:
        raise Refused('REFUSED: producer registry: missing keys %s' % sorted(missing), 'PRODUCER_REGISTRY_MISSING_KEYS')
    prod, comp, tok = obj.get('producers'), obj.get('identity_comparators'), obj.get('identity_tokens')
    grec, gqn = obj.get('gate_records'), obj.get('gq_all_nodes_counts')                             # R8 [A67 N2] [A67 SF1]
    dn = registry_duplicate_naming(obj)                                     # R11 [A79.6] a duplicate entry names both entries
    if dn:
        raise Refused('REFUSED: producer registry: an entry is listed twice (%s) (A71)' % dn, 'PRODUCER_REGISTRY_DUPLICATE_ENTRY_A71', dn)
    if not (isinstance(grec, dict) and set(grec) <= set(ALL_GATES)
            and all((isinstance(v, list) and all(_hex64(x) for x in v) and not unique_keys_codes(v, 'REGISTRY', 'gate_records'))
                    or (v == GATE_RECORD_AFTER_SEAL and g not in GATE_RECORD_SHA_REQUIRED and g in GATE_RECORD_AFTER_SEAL_ALLOWED)
                    for g, v in grec.items())):
        raise Refused('REFUSED: producer registry: gate_records must map gate names to lists of distinct sha256 (or %s, only for '
                      'the post-seal gates %s; all other gates require registered record shas) (A67 N2, NEW-52, A71, A88)'
                      % (GATE_RECORD_AFTER_SEAL, '/'.join(GATE_RECORD_AFTER_SEAL_ALLOWED)),
                      'PRODUCER_REGISTRY_GATE_RECORDS')
    if not (isinstance(gqn, dict) and all(isinstance(k, str) and k and KINDS['int'](n) and n > GQ_SAMPLE_NODES for k, n in gqn.items())):
        raise Refused('REFUSED: producer registry: gq_all_nodes_counts must map geometry labels to production node counts '
                      '(int > %d, the sample) (A67 SF1)' % GQ_SAMPLE_NODES, 'PRODUCER_REGISTRY_GQ_ALL_NODES_COUNTS')
    if not (isinstance(prod, dict) and set(prod) <= set(ALL_GATES) and all(_file_pin_list(v) is not None for v in prod.values())):
        raise Refused('REFUSED: producer registry: producers must map gate names to lists of distinct {path, sha256} file pins '
                      '(A69 note 1, A71)', 'PRODUCER_REGISTRY_PRODUCERS')
    if _file_pin_list(comp) is None:
        raise Refused('REFUSED: producer registry: identity_comparators must be a list of distinct {path, sha256} file pins',
                      'PRODUCER_REGISTRY_IDENTITY_COMPARATORS')
    if not (isinstance(tok, dict) and set(tok) <= set(IDENTITY_GATES) and all(_file_pin_list(v) is not None for v in tok.values())):
        raise Refused('REFUSED: producer registry: identity_tokens must map %s to lists of distinct {path, sha256} file pins'
                      % '/'.join(IDENTITY_GATES), 'PRODUCER_REGISTRY_IDENTITY_TOKENS')
    if verify_bytes:                                                                              # R10 [A69 note 1]
        bad = _file_pins_bytes_codes([x for v in prod.values() for x in v] + list(comp) + [x for v in tok.values() for x in v])
        if bad:
            raise Refused('REFUSED: producer registry: registered files missing or not their sha from bytes: %s (A69 note 1)'
                          % sorted(set(bad)), 'PRODUCER_REGISTRY_FILE_BYTES_A69_1')
    pins = lambda v: {(os.path.realpath(x['path']), x['sha256']) for x in v}
    return {'producers': {g: frozenset(pins(v)) for g, v in prod.items()}, 'identity_comparators': frozenset(pins(comp)),
            'identity_tokens': {g: frozenset(pins(v)) for g, v in tok.items()},
            'gate_records': {g: (frozenset(v) if isinstance(v, list) else v) for g, v in grec.items()},
            'gq_all_nodes_counts': dict(gqn), 'sha256': sha, 'path': path}


PRODUCER_SHA_CODE = 'PRODUCER_NOT_ROOT_REGISTERED_A62_2'
PRODUCER_PATH_CODE = 'PRODUCER_PATH_NOT_ROOT_REGISTERED_A69_1'
PRODUCER_BYTES_CODE = 'PRODUCER_BYTES_NOT_THE_REGISTERED_SHA_A69_1'


def file_pin_codes(path, sha, registered, tag):
    """R10 [A69 note 1] a record's {path, sha256} pin against registered {(realpath, sha256)}: the sha must be registered (A62.2
    code, as r8), the path must be the registered path of that sha, and the file's bytes must hash to it now.  [] when bound."""
    shas = {s for _, s in registered}
    if sha not in shas:
        return ['%s:%s' % (tag[0], tag[1])]
    try:
        rp = os.path.realpath(path)
    except (OSError, ValueError, TypeError):
        rp = None
    if (rp, sha) not in registered:
        return ['%s:%s' % (tag[2], tag[1])]
    try:
        ok = sha256_file(rp) == sha
    except OSError:
        ok = False
    return [] if ok else ['%s:%s' % (tag[3], tag[1])]


def gate_record_sha_codes(name, record_sha, reg):
    """R8 [A67 N2] the gate record itself must be a root-registered record of record (its sha from bytes in gate_records[gate]),
    unless root marked the gate GATE_RECORD_AFTER_SEAL (NEW-52; SR_K included by A88).  [] with no registry (evaluate_gate already makes the
    record a RECORD_DEFECT, PRODUCER_REGISTRY_ABSENT_A62_2)."""
    if reg is None:
        return []
    v = reg['gate_records'].get(name)
    if v == GATE_RECORD_AFTER_SEAL:            # R10 [NEW-52] the loader refuses it elsewhere; a hand-built registry fails closed too
        return [] if (name in GATE_RECORD_AFTER_SEAL_ALLOWED and name not in GATE_RECORD_SHA_REQUIRED) else \
            ['GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:%s' % name]
    if v is None or record_sha not in v:
        return ['GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:%s' % name]
    return []


def load_producer_registry(path, expected_sha=None):
    """R7 [A62.2] read a producer registry file strictly (a duplicate key refuses); expected_sha: the pinned sha (sealed mode)."""
    try:
        raw = Path(path).read_bytes()
    except OSError as exc:
        raise Refused('REFUSED: producer registry unreadable (%s)' % type(exc).__name__, 'PRODUCER_REGISTRY_UNREADABLE')
    sh = sha256_bytes(raw)
    if expected_sha is not None and sh != expected_sha:
        raise Refused('REFUSED: producer registry sha mismatch (pinned %s)' % expected_sha, 'PRODUCER_REGISTRY_SHA_MISMATCH')
    try:
        obj = loads_strict(raw)
    except DuplicateKey as exc:                                                     # R11 [A79.6] both members named
        raise Refused('REFUSED: producer registry has a duplicate JSON key (%s)' % exc.code, 'PRODUCER_REGISTRY_DUPLICATE_JSON_KEY_A71',
                      exc.code)
    except ValueError as exc:
        raise Refused('REFUSED: producer registry unreadable (%s)' % type(exc).__name__, 'PRODUCER_REGISTRY_UNREADABLE')
    return producer_registry_from_obj(obj, sh, str(Path(path).resolve()))


def registered_kbig(ctx, lab):
    """R7 [RA7] (r6 recheck validity SF1) the registered cylinder K_big of a T-case, read from the case block (None if unreadable)."""
    try:
        o = (ctx or {})['case_block']['cases'][lab]['normalized_spec_equal']['/numerics']['uv_tail']['outer']
        kb = o['K_big_inverse_kpc']
    except (KeyError, TypeError):
        return None
    return float(kb) if (isinstance(o, dict) and o.get('shape') == 'cylinder' and _num(kb) and kb > 0) else None


def registered_row_maps(pre5):
    """R10 [A71] the row ids, tau and sigma lists of the pinned V005 prereg become mappings: 12 distinct ids and lists of exactly
    that length (zip would silently truncate; a repeated id would keep the last tau), built by unique_map; else REFUSED."""
    ids, tau, sig = pre5.get('row_ids'), pre5.get('tau_km_s'), pre5.get('quoted_sigma_km_s')
    if not (isinstance(ids, list) and len(ids) == 12 and isinstance(tau, list) and isinstance(sig, list)
            and len(tau) == len(ids) and len(sig) == len(ids)):
        raise Refused('REFUSED: V005 prereg row_ids / tau_km_s / quoted_sigma_km_s are not 12 ids with 12 values each',
                      'V005_PREREG_ROW_IDS_A71')
    try:
        return ids, unique_map(list(zip(ids, tau)), 'V005_PREREG', 'row_ids'), unique_map(list(zip(ids, sig)), 'V005_PREREG', 'row_ids')
    except DuplicateEntry as exc:
        raise Refused('REFUSED: V005 prereg: %s' % exc.codes[0], 'V005_PREREG_ROW_IDS_A71', exc.codes[0])


def build_context(route_a_mode=ROUTE_A_MODE_DEFAULT, case_block=None, producer_registry=None, driver_build=None):
    """Verify every pin from bytes (REFUSED on mismatch) and assemble the registered constants.  R7: also the v010 r5 custody
    pins against the r5 cascade map (A62.3), and the producer registry (A62.2) carried in ctx['producer_registry'].
    R10 [A72]: driver_build (a BUILD object, r5 or r6) becomes the active custody pin set; None keeps the active one (the
    built-in r5 set when none was activated)."""
    if sha256_file(PIN_ADDENDUM_V004[0]) != PIN_ADDENDUM_V004[1]:                                     # [A46] verify, refuse
        raise Refused('REFUSED: V004 addendum sha mismatch (frozen 487d4449 required)', 'V004_ADDENDUM_SHA_MISMATCH')
    if PIN_ADDENDUM_V005 is not None and sha256_file(ADDENDUM_V005_CITED) != PIN_ADDENDUM_V005:      # [A48] once frozen
        raise Refused('REFUSED: V005 addendum sha mismatch (pinned %s)' % PIN_ADDENDUM_V005, 'V005_ADDENDUM_SHA_MISMATCH')
    if driver_build is not None:
        activate_driver_build(driver_build)
    bld = active_build()
    pre5 = load_pinned_json(PIN_PREREG_V005)
    pre6 = load_pinned_json(PIN_PREREG_V006R1)
    draft = load_pinned_json(PIN_DRAFT_R1)
    c5h_spec = load_pinned_json(PIN_C5H_SPEC)
    C5M = load_pinned_module(PIN_COMPARE_V005[0], PIN_COMPARE_V005[1], 'kmax_compare_c2v005_pinned')
    ra4 = c5h_spec['numerics']['brackets']
    if C5M.canon(ra4) != C5M.canon(ra4_block_expected()):                                             # [RA4] byte-for-byte
        raise Refused('REFUSED: C5H spec bracket block differs from the RA4 list', 'C5H_SPEC_BRACKETS_NOT_RA4')
    if route_a_mode not in ROUTE_A_MODES:
        raise Refused('REFUSED: route-A mode %r not in %s' % (route_a_mode, sorted(ROUTE_A_MODES)), 'ROUTE_A_MODE_UNKNOWN')
    ids, tau_map, sigma_map = registered_row_maps(pre5)                                               # R10 [A71]
    grids = {g: pre5['grids'][g]['composite_grid_spec'] for g in ('G2', 'G3', 'G4')}
    grids.update({g: pre6['grids'][g]['composite_grid_spec'] for g in ('G5', 'G6')})
    anc = pre5['anchor']
    for k, x in list(bld['ro1_custody'].items()) + [('nodes_' + k, x) for k, x in bld['ro1_nodes_custody'].items()]:
        if sha256_file(x['path']) != x['sha256']:                                                    # [A50 root items 11, 12]
            raise Refused('REFUSED: RO1 custody pin mismatch %s (%s)' % (k, x['path']), 'RO1_CUSTODY_PIN_MISMATCH')   # [R4 F1]
    if bld['build'] == 'r5':
        why_r5 = r5_custody_codes()                                                                  # R7 [A62.3]
        if why_r5:
            raise Refused('REFUSED: v010 r5 custody (A62.3): %s' % '; '.join(why_r5), 'V010_R5_CUSTODY_A62_3')
    adm = c5h_admission_bases()
    c5h_ref = adm.pop('_numerics_reference')
    ctx = {'pre5': pre5, 'draft': draft, 'C5M': C5M, 'ids': ids, 'tau': tau_map,
           'driver_build': bld['build'],
           'sigma': sigma_map, 'tau_picard': pre5['criterion']['tau_picard_km_s'],
           'grids': grids, 'anchor': {'galaxy': 'DDO154', 'physical': anc['physical'], 'coefficients': anc['coefficients'],
                                      'picard': anc['picard']},
           'ra4_block': ra4, 'c5h_spec_numerics': c5h_spec['numerics'], 'c5h_numerics_reference': c5h_ref,
           'route_a_mode': route_a_mode, 'case_block': case_block, 'v005_next_steps': pre5['criterion']['gate_next_steps'],
           'row_radii_m': registered_row_radii(ids), 'c5h_admission': adm, 'producer_registry': producer_registry}
    return ctx


def c5h_numerics_reference():
    """[A50 S1] the C5H spec 60b46130 numerics as normalized by its pinned dry run (cbd2885d); REFUSED if unavailable."""
    ref = c5h_admission_bases()['_numerics_reference']
    if not isinstance(ref, dict):
        raise Refused('REFUSED: the C5H dry run carries no normalized_spec.numerics', 'C5H_DRYRUN_NUMERICS_ABSENT')
    return ref


def drop_mapped_keys(a, b, keymap):
    """[A48 AMB-13] drop, from deep copies of a and b, every key_equivalence_map pointer that a carries with exactly its
    absent-equivalent value while b lacks it or carries the same value.  Returns (a', b', used pointers)."""
    a, b = json.loads(canon(a or {})), json.loads(canon(b or {}))
    used = []
    for e in keymap or []:
        parts = e['pointer'].split('/')[2:]
        fa, va = jptr({'n': a}, '/n/' + '/'.join(parts))
        fb, vb = jptr({'n': b}, '/n/' + '/'.join(parts))
        if fa and canon(va) == canon(e['absent_equivalent_value']) and (not fb or canon(vb) == canon(va)):
            for x in (a, b):
                cur = x
                for k in parts[:-1]:
                    cur = cur.get(k) if isinstance(cur, dict) else None
                if isinstance(cur, dict):
                    cur.pop(parts[-1], None)
            used.append(e['pointer'])
    return a, b, used



def required_gates(route_a_mode):
    """[A47 I4] gate I4 is required in route-A mode parallel8 only."""
    return REQUIRED_GATES + (MODE_GATES if route_a_mode == 'parallel8' else ())


def _strip_ptrs(value, base_ptr, exempt):
    """A deep copy of value (found at base_ptr) with every exempt pointer at or under base_ptr removed."""
    v = json.loads(canon(value)) if value is not None else None
    for e in exempt:
        if e == base_ptr:
            return None
        if e.startswith(base_ptr.rstrip('/') + '/'):
            parts = e[len(base_ptr.rstrip('/')) + 1:].split('/')
            cur = v
            for k in parts[:-1]:
                cur = cur.get(k) if isinstance(cur, dict) else None
            if isinstance(cur, dict):
                cur.pop(parts[-1], None)
    return v


_GRIDS = {}


def registered_grids():
    """The registered composite grids G2-G6 from the pinned V005 / V006 R1 preregs (as build_context reads them)."""
    if 'g' not in _GRIDS:
        pre5, pre6 = load_pinned_json(PIN_PREREG_V005), load_pinned_json(PIN_PREREG_V006R1)
        g = {x: pre5['grids'][x]['composite_grid_spec'] for x in ('G2', 'G3', 'G4')}
        g.update({x: pre6['grids'][x]['composite_grid_spec'] for x in ('G5', 'G6')})
        _GRIDS['g'] = g
    return _GRIDS['g']


def registered_P(cb):
    """[A54] the production K_big P: the registered C4T uv_tail outer.K_big_inverse_kpc (cylinder), or None if unreadable."""
    try:
        o = cb['cases']['C4T']['normalized_spec_equal']['/numerics']['uv_tail']['outer']
        kb = o['K_big_inverse_kpc']
    except (KeyError, TypeError):
        return None
    return float(kb) if (isinstance(o, dict) and o.get('shape') == 'cylinder' and _num(kb) and kb > 0) else None


def production_kbig(ctx):
    """[A54] P read from the case block of ctx (None when no readable registration)."""
    return registered_P((ctx or {}).get('case_block') or {})


def registered_gas_M_s(ctx):
    """R10 [A68 CHK-1] the registered uv_tail gas.M_s of the case block (C4T; every other T-case equals C4T there by A54 S8), or None
    when unreadable.  The certificates bind to THIS value (and it must be the A57 production M_s 128: validate_case_block refuses
    any other, and the gates refuse a context that is not, so a direct gate call with an M_s 64 context cannot pass)."""
    try:
        g = (ctx or {})['case_block']['cases']['C4T']['normalized_spec_equal']['/numerics']['uv_tail']['gas']
        ms = g['M_s']
    except (KeyError, TypeError):
        return None
    return ms if KINDS['int'](ms) else None


def gas_M_s_context_codes(ctx, gate):
    """R10 [A68 CHK-1] [] when the registered gas.M_s is readable and is the A57 production M_s; else the DEFECT code."""
    ms = registered_gas_M_s(ctx)
    if ms is None:
        return ['DEFECT:%s_REGISTERED_GAS_M_S_UNREADABLE_FROM_THE_CASE_BLOCK_A68_CHK1' % gate]
    if ms != PRODUCTION_GAS_M_S_A57:
        return ['DEFECT:%s_REGISTERED_GAS_M_S_NOT_THE_A57_PRODUCTION_M_S_A68_CHK1' % gate]
    return []


def coverage_edge_2P(P):
    """[A54] the EPS / LO coverage requirement sqrt(2) x 2P, never below R1's DDO edge 64 /kpc (stricter); None without P."""
    return None if P is None else max(R1_DDO_COVERAGE_EDGE, COVERAGE_FACTOR_OF_2P * 2.0 * P)


def gq_ddo_edge(P):
    """[A48 AMB-12] [RA7] with [A54]: the GQ DDO domain edge = the largest T-case K_big (C4T-KHI = 2P), never below 64 /kpc."""
    return None if P is None else max(R1_DDO_COVERAGE_EDGE, 2.0 * P)


def kbig_next_step(P):
    """[R1 KBIG_NOT_CONVERGED] next step with the generic T3 [A54]: R1 'production K_big 64 under T3prime (32/64/128), EPS and
    LO to 128' is the P = 32 instance of 'production K_big 2P under T3prime (P/2P/4P), EPS and LO to 4P' (coverage then
    >= sqrt(2) x 4P by A54 applied to T3prime: DERIVED, root to confirm)."""
    if P is None:
        return NEXT_STEP['KBIG_NOT_CONVERGED']
    return ('T3prime: production 2P with {P, 4P}; EPS/LO coverage >= sqrt(2) x 4P (A56 N4); with P = %g read from the case block: '
            'production K_big %g with {%g, %g}; EPS/LO coverage >= sqrt(2) x %g' % (P, 2 * P, P, 4 * P, 4 * P))


def _strip_keys(d, keys):
    return {k: v for k, v in d.items() if k not in keys} if isinstance(d, dict) else d


def tail_content_codes(reg_num, grids):
    """[A54 S8] [A54 T3] the registered tail content of every T-case (RA1/RA2/R1): grid (kept K), truncation, source rule,
    outer shape and K_out/K_big against P read from C4T, lambda_scale, and every other uv_tail key equal to C4T's.  A swapped
    tail, a wrong grid, a wrong K_out or a wrong K_big is refused."""
    why = []
    if 'C4T' not in reg_num:
        return ['C4T: no registered /numerics, so the production K_big P cannot be read (A54)']
    uv4 = reg_num['C4T'].get('uv_tail')
    o4 = uv4.get('outer') if isinstance(uv4, dict) else None
    P = (float(o4['K_big_inverse_kpc']) if isinstance(o4, dict) and set(o4) == {'shape', 'K_big_inverse_kpc'}
         and o4.get('shape') == 'cylinder' and _num(o4.get('K_big_inverse_kpc')) and o4['K_big_inverse_kpc'] > 0 else None)
    if P is None:
        return ['C4T: registered uv_tail outer must be exactly {shape: cylinder, K_big_inverse_kpc: P > 0} (A54: P is read there)']
    if PRODUCTION_K_BIG_A55 is not None and P != PRODUCTION_K_BIG_A55:
        why.append('C4T: registered K_big P differs from the A55 production K_big')
    g4 = uv4.get('gas') if isinstance(uv4, dict) else None                                             # R6 [A57 ruling 1]
    if not (isinstance(g4, dict) and KINDS['int'](g4.get('M_s')) and g4['M_s'] == PRODUCTION_GAS_M_S_A57):
        why.append('C4T: registered uv_tail gas.M_s must be the A57 production M_s 128 (every other T-case equals C4T there, A54 S8)')
    for lab in T_CASES:
        num = reg_num.get(lab)
        if not isinstance(num, dict):
            continue
        uv = num.get('uv_tail')
        if not isinstance(uv, dict):
            continue
        if canon(num.get('composite_grid_spec')) != canon(grids.get(EXPECTED_GRID[lab])):
            why.append('%s: registered composite_grid_spec is not the registered grid %s (A54 S8: kept K)' % (lab, EXPECTED_GRID[lab]))
        tr = num.get('truncation') or {}
        et = EXPECTED_TRUNCATION[lab]
        if not (isinstance(tr, dict) and tr.get('shape') == et['shape'] and tr.get('kmax_inverse_kpc') == et['kmax_inverse_kpc']):
            why.append('%s: registered /numerics truncation differs from the prereg (A54 S8)' % lab)
        if uv.get('enabled') is not True or uv.get('lapse_only') is not True:
            why.append('%s: registered uv_tail must be enabled and lapse_only (A54 S8; A52.6)' % lab)
        sr = uv.get('source_rule')
        if lab == 'C4T-D5':
            if not (isinstance(sr, dict) and sr.get('rule') == 'nodes_v001' and canon(sr.get('ext_grid')) == canon(grids.get('G5'))):
                why.append('C4T-D5: registered source_rule must be nodes_v001 with ext_grid = the registered G5 grid (RA1; A54 S8)')
        elif sr != 'continuum_v001':
            why.append('%s: registered source_rule must be continuum_v001 (RA2 / R1 production tail; A54 S8)' % lab)
        o = uv.get('outer')
        if lab == 'C4T-C5c':
            if not (isinstance(o, dict) and set(o) == set(C5C_OUTER) and o.get('shape') == 'cube'
                    and _num(o.get('K_out_inverse_kpc')) and o['K_out_inverse_kpc'] == C5C_OUTER['K_out_inverse_kpc']):
                why.append('C4T-C5c: registered outer must be cube K_out 5 (RA2; A54 S8)')
        else:
            want = P * T3_KBIG_FACTOR.get(lab, 1.0)
            if not (isinstance(o, dict) and set(o) == {'shape', 'K_big_inverse_kpc'} and o.get('shape') == 'cylinder'
                    and _num(o.get('K_big_inverse_kpc')) and o['K_big_inverse_kpc'] == want):
                why.append('%s: registered outer must be cylinder K_big = %s (A54: P read from C4T)'
                           % (lab, {'C4T-KLO': 'P/2', 'C4T-KHI': '2P'}.get(lab, 'P')))
        ls = uv.get('lambda_scale')
        want_ls = C4TA_LAMBDA_SCALE if lab == 'C4T-A' else 1.0
        if not (_num(ls) and ls == want_ls):
            why.append('%s: registered uv_tail lambda_scale must be %s (R1 RB_FP_run; A54 S8)' % (lab, want_ls))
        if lab != 'C4T' and canon(_strip_keys(uv, UV_TAIL_DIFFERING_KEYS)) != canon(_strip_keys(uv4, UV_TAIL_DIFFERING_KEYS)):
            why.append('%s: registered uv_tail differs from C4T\'s outside %s (R1 production tail fixed across cases; A54 S8)'
                       % (lab, '/'.join(UV_TAIL_DIFFERING_KEYS)))
    return why


# R11 (r10 recheck validity N4: unknown keys inside a case entry were accepted) the keys a case entry may carry (FIELDS section 3)
CASE_ENTRY_KEYS_T = ('grid', 'truncation', 'normalized_spec_equal', 'tail', 'ro1_required', 'uv_tail_config_sha256', 'drivers_allowed',
                     'note')
CASE_ENTRY_KEYS_C5H = ('grid', 'truncation', 'normalized_spec_equal', 'tail', 'ro1_required', 'call_spec_sha256', 'drivers_allowed',
                       'note')


def validate_case_block(cb, check_uv_link=True, route_a_mode=None):
    """The registered V007 case block (V3 'registered case block'); REFUSED if incomplete.  Format: FIELDS_R8.md section 3.
    R2 [A50 S1]: RA1 against the C5H spec 60b46130: the registered C4T-D5 /numerics equal the spec numerics (as normalized by
    its dry run) apart from composite_grid_spec, uv_tail (route_a.column_workers too in serial_with_exemption) and mapped keys.
    R1: /numerics registered WHOLE for every T-case (verify S3; A48 stricter-where-silent); the registered uv_tail block
    normalizes (pinned library) to uv_tail_config_sha256 (verify S4); registered numerics pairwise distinct across T-cases and
    uv_tail distinct for UV_TAIL_MUST_DIFFER (verify D4); no seed_source_rtol_factor other than absent/1.0 (A48 AMB-14);
    key_equivalence_map entries well formed (A48 AMB-13).
    R5: [A54 S8] the registered tail content of every T-case (tail_content_codes) and [A54] the generic T3: P read from the
    registered C4T, C4T-KLO at P/2 and C4T-KHI at 2P, any other value refused."""
    why = []
    if not isinstance(cb, dict) or cb.get('schema') != CASE_BLOCK_SCHEMA:
        return ['case block schema must be %s' % CASE_BLOCK_SCHEMA]
    extra = set(cb) - {'schema', 'cases', 'route_a_mode', 'key_equivalence_map', 'note'}
    if extra:
        return ['case block: unknown keys %s' % sorted(extra)]
    cases = cb.get('cases')
    if not isinstance(cases, dict) or set(cases) != set(REGISTERED):
        return ['case block cases must be exactly %s' % list(REGISTERED)]
    reg_num = {}
    for lab, e in cases.items():
        if not isinstance(e, dict):
            why.append('%s: entry not an object' % lab)
            continue
        allowed_ = CASE_ENTRY_KEYS_C5H if lab == C5H else CASE_ENTRY_KEYS_T      # R11 (r10 recheck validity N4) a key allow-list
        if set(e) - set(allowed_):
            why.append('%s: unknown case-entry keys (the entry carries only %s)' % (lab, '/'.join(allowed_)))
        if e.get('grid') != EXPECTED_GRID[lab]:
            why.append('%s: grid %r, registered %s' % (lab, e.get('grid'), EXPECTED_GRID[lab]))
        if e.get('truncation') != EXPECTED_TRUNCATION[lab]:
            why.append('%s: truncation differs from the prereg' % lab)
        da = e.get('drivers_allowed')
        if not (isinstance(da, list) and da and all(_hex64(x) for x in da)):
            why.append('%s: drivers_allowed must be a non-empty list of sha256' % lab)
        nse = e.get('normalized_spec_equal')
        if not isinstance(nse, dict) or not all(isinstance(k, str) and k.startswith('/') for k in nse):
            why.append('%s: normalized_spec_equal must map JSON pointers to values' % lab)
            nse = {}
        if lab == C5H:
            if e.get('tail') is not False or e.get('ro1_required') is not False:
                why.append('C5H: tail and ro1_required must be false (v009-EXT, A44)')
            if e.get('call_spec_sha256') != PIN_C5H_SPEC[1]:
                why.append('C5H: call_spec_sha256 must be the registered spec 60b46130 (A44)')
            if da != [DRIVER_V009_EXT]:
                why.append('C5H: drivers_allowed must be [v009-EXT 999331af]')
        else:
            if e.get('tail') is not True or e.get('ro1_required') is not True:
                why.append('%s: tail and ro1_required must be true (RA5: RO1 in every V007 run)' % lab)
            if da != [sealed_driver_sha()]:                                          # R7 [A62.3] [A58 RI-01]; R10 [A72]
                why.append('%s: drivers_allowed must be [the sealed driver of the active build (v010 r5 b5cc62af, or r6 by A72)] '
                           '(A62.3; A58 RI-01; A72)' % lab)
            if not _hex64(e.get('uv_tail_config_sha256')):
                why.append('%s: uv_tail_config_sha256 required' % lab)
            num = nse.get('/numerics')
            if not isinstance(num, dict):
                why.append('%s: normalized_spec_equal must register /numerics whole (R1, verify S3)' % lab)
                continue
            reg_num[lab] = num
            uv = num.get('uv_tail')
            if not isinstance(uv, dict):
                why.append('%s: registered /numerics lacks the uv_tail block' % lab)
            elif check_uv_link:
                try:
                    n = load_uvt_lib().normalize_config(uv)
                    if n['sha256'] != e.get('uv_tail_config_sha256'):
                        why.append('%s: uv_tail_config_sha256 is not the pinned-library sha of the registered uv_tail' % lab)
                except ValueError as exc:
                    why.append('%s: registered uv_tail refused by the pinned library: %s' % (lab, str(exc).split(' ')[0]))
            f = ((num.get('route_a') or {}).get('seed_source_rtol_factor', SEED_FACTOR_ABSENT_EQUIVALENT))
            if f != SEED_FACTOR_ABSENT_EQUIVALENT:
                why.append('%s: registered route_a.seed_source_rtol_factor must be absent or 1.0 (A48 AMB-14)' % lab)
            if canon(num.get('brackets')) != canon(ra4_block_expected()):
                why.append('%s: registered brackets differ from RA4' % lab)
        if '/numerics/brackets' in nse and canon(nse['/numerics/brackets']) != canon(ra4_block_expected()):
            why.append('%s: registered brackets differ from RA4' % lab)
    labs = sorted(reg_num)
    for i, a in enumerate(labs):                                                                    # [verify D4] no alias
        for b in labs[i + 1:]:
            if canon(reg_num[a]) == canon(reg_num[b]):
                why.append('%s and %s: registered numerics are identical (aliasing; every T-case differs by the text)' % (a, b))
    for a, b in UV_TAIL_MUST_DIFFER:
        if a in reg_num and b in reg_num:
            if canon(reg_num[a].get('uv_tail')) == canon(reg_num[b].get('uv_tail')) or \
                    cases[a].get('uv_tail_config_sha256') == cases[b].get('uv_tail_config_sha256'):
                why.append('%s and %s: registered uv_tail must differ (K_big / lambda_scale / source rule by the text)' % (a, b))
    why += tail_content_codes(reg_num, registered_grids())                                   # [A54 S8] [A54 T3]
    km = cb.get('key_equivalence_map', [])
    if not isinstance(km, list):
        why.append('key_equivalence_map must be a list')
    else:
        for j, x in enumerate(km):
            if not (isinstance(x, dict) and set(x) == {'pointer', 'absent_equivalent_value', 'b0_identity_evidence'}
                    and isinstance(x['pointer'], str) and x['pointer'].startswith('/numerics/')
                    and isinstance(x['b0_identity_evidence'], str) and x['b0_identity_evidence']):
                why.append('key_equivalence_map[%d]: needs exactly {pointer (/numerics/..), absent_equivalent_value, '
                           'b0_identity_evidence} (A48 AMB-13)' % j)
            elif x['pointer'].split('/')[2] in ('composite_grid_spec', 'uv_tail', 'brackets', 'picard', 'truncation'):
                why.append('key_equivalence_map[%d]: %s may not be mapped' % (j, x['pointer']))
        # R10 [A71] (Claude3 helper I item 4): one pointer mapped twice is refused (r8 applied each entry: either value counted)
        why += ['key_equivalence_map: %s (one pointer mapped twice, A71)' % c for c in
                unique_keys_codes([x.get('pointer') if isinstance(x, dict) else None for x in km], 'CASE_BLOCK', 'key_equivalence_map')]
    if 'route_a_mode' in cb and cb['route_a_mode'] not in ROUTE_A_MODES:
        why.append('route_a_mode %r unknown' % cb['route_a_mode'])
        return why
    mode = cb.get('route_a_mode') or route_a_mode or ROUTE_A_MODE_DEFAULT
    if mode not in ROUTE_A_MODES:
        return why + ['route_a_mode %r unknown' % mode]
    if 'C4T-D5' in reg_num and not any(w.startswith('key_equivalence_map') for w in why):          # [A50 S1] [RA1]
        d5, ref, used = drop_mapped_keys(reg_num['C4T-D5'], c5h_numerics_reference(), km if isinstance(km, list) else [])
        eq, diff = numerics_equal_except(d5, ref, ROUTE_A_MODES[mode]['c4td5_exempt'])
        if not eq:
            why.append('C4T-D5: registered /numerics differ from the C5H spec 60b46130 numerics (as normalized by its dry run) '
                       'outside %s and mapped keys (RA1, A50 S1): %s' % (', '.join(ROUTE_A_MODES[mode]['c4td5_exempt']),
                                                                          sorted({d.split('=')[0] for d in diff})[:8]))
    return why



# ============================================================================================ run reading
# [verify blinding B1] record-controlled strings enter reason codes only through these enums / patterns (no digit can pass
# _RE_UPPER_CODE or _RE_IDENT); [A50 N1] stage names only through the exact allow-list STAGE_NAMES; anything else is OTHER.
STOP_REASONS = ('WALL_CAP', 'RSS_CAP', 'OUTPUT_CAP')
_RE_UPPER_CODE = re.compile(r'[A-Z][A-Z_]*\Z')
_RE_IDENT = re.compile(r'[A-Za-z_]+\Z')


def _stage(x):
    """[A50 N1] a stage name from a record: kept only if it is exactly a driver constant (STAGE_NAMES), else redacted."""
    return x if isinstance(x, str) and x in STAGE_NAMES else STAGE_OTHER


def _enum(x, allowed=None, pattern=None, other='OTHER'):
    x = str(x).strip()
    if allowed is not None:
        return x if x in allowed else other
    return x if pattern.match(x) else other


PASS_ROW_GAP = 'E_UNAVAILABLE_PASS_ROW_GAP'


def pass_rows_gap(r):
    """[A54 B4] a pass recorded without rows is a record gap: pass_rows must equal passes in number, with consecutive indices
    (1..n, as the driver writes them).  Returns None, or a code (E is then unavailable: -> R-PAIR; INCOMPLETE if none resolves)."""
    ps = r.get('passes')
    if not isinstance(ps, list):
        return None if ps is None else 'PASSES_NOT_A_LIST'
    for j, x in enumerate(ps):
        rows = x.get('rows') if isinstance(x, dict) else None
        if rows is None or (isinstance(rows, list) and not rows):
            return 'PASS_WITHOUT_ROWS'
        # R10 (Claude3 r7 addendum A-N1): a row-set that is PRESENT but not a list of objects is A54 S9 only (pass_rows_ids_code),
        # never also a B4 gap (r7 / r8 read both); its pass index is still checked
        if not (KINDS['int'](x.get('pass')) and x['pass'] == j + 1):
            return 'PASS_INDICES_NOT_CONSECUTIVE_FROM_1'
    return None


PASS_ROWS_S9 = 'PASS_ROWS_NOT_EXACTLY_THE_12_REGISTERED_IDS_EACH_ONCE_A54_S9'


def pass_rows_ids_code(r, ids):
    """R6 [A54 S9] (Codex2 CX2-R5-B1): every recorded pass row-set carries exactly the 12 registered row ids, each once (no
    duplicate, no unknown, none missing; every entry an object with a string id), checked on the raw record BEFORE any dict is
    built (a dict keeps the last duplicate).  Any violation is a RECORD_DEFECT of the run: the case is invalid (V1) and reads
    INCOMPLETE.  A pass with NO row-set (rows absent, null or []) is the A54 B4 record gap (pass_rows_gap), not an S9 code; the
    final row-set is verify D2 (rows_codes).  R7 (r6 recheck order B1): a row-set that is PRESENT but not a list (a dict, {}, a
    string, a number, a bool) is S9 too, never a B4 gap (FIELDS_R7; NEW-34).  A pass entry that is not an object is left to the
    V005 adapt_result (it refuses the record: invalid).  Returns None or PASS_ROWS_S9."""
    ps = r.get('passes') if isinstance(r, dict) else None
    if not isinstance(ps, list):
        return None
    want = sorted(ids)
    for x in ps:
        if not isinstance(x, dict):
            continue
        rows = x.get('rows')
        if rows is None or (isinstance(rows, list) and not rows):
            continue                                                  # [A54 B4] no row-set recorded: a gap, read by pass_rows_gap
        if not isinstance(rows, list):
            return PASS_ROWS_S9                                       # R7 [r6 recheck order B1] present, not a list: S9
        if not all(isinstance(y, dict) for y in rows):
            return PASS_ROWS_S9
        got = [y.get('id') for y in rows]
        if len(got) != len(want) or not all(isinstance(g, str) for g in got) or sorted(got) != want:
            return PASS_ROWS_S9
    return None


def pass_rows_s9_naming(r, ids):
    """R11 [A79.6 / A75.3] (Claude3 0070 §2: the S9 / D2 row codes named neither entry): the both-entry position codes of every
    repeated row id inside a pass row-set, DUPLICATE_ENTRY_A71:RUN:passes[k]/rows[i]:passes[k]/rows[j] (indices only).  An S9 violation
    that is not a duplicate (an unknown, missing or malformed row) has no second entry: S9_AT_PASS:passes[k] names the pass."""
    out = []
    ps = r.get('passes') if isinstance(r, dict) else None
    for k, x in enumerate(ps if isinstance(ps, list) else []):
        rows = x.get('rows') if isinstance(x, dict) else None
        if rows is None or (isinstance(rows, list) and not rows):
            continue
        if not (isinstance(rows, list) and all(isinstance(y, dict) for y in rows)):
            out.append('S9_AT_PASS:passes[%d]' % k)
            continue
        got = [y.get('id') if isinstance(y.get('id'), str) else ('NOT_A_STRING', j) for j, y in enumerate(rows)]
        d = unique_keys_codes(got, 'RUN', 'passes[%d]/rows' % k)
        out += d
        if not d and sorted(g for g in got if isinstance(g, str)) != sorted(ids):
            out.append('S9_AT_PASS:passes[%d]' % k)
    return out


def _pass_rows(r):
    """Per-pass {row id: speed}.  Called only when A54 S9 found no defect (so every row-set has the 12 ids once); R10 [A71] the
    dict is built by unique_map all the same (defence in depth: a repeated id raises DuplicateEntry, read_run makes it S9)."""
    out = []
    for k, p in enumerate(r.get('passes') or []):
        rows = p.get('rows') if isinstance(p, dict) else None
        if isinstance(rows, list) and rows:
            out.append(unique_map([(x.get('id'), x.get('speed_km_s')) for x in rows if isinstance(x, dict)], 'RUN', 'passes[%d]/rows' % k))
    return out


def read_route_a_attempt(result):
    """The route-A attempt result named by route_a_outcome (v009/v010); returns (attempt_json, code_or_None)."""
    rao = result.get('route_a_outcome')
    if not isinstance(rao, dict):
        return None, 'FIELD_MISSING:result:route_a_outcome'
    p, s = rao.get('result_path'), rao.get('result_sha256')
    if not isinstance(p, str):
        return None, 'FIELD_MISSING:result:route_a_outcome/result_path'
    if not Path(p).is_file():
        return None, 'ROUTE_A_ATTEMPT_RESULT_ABSENT'
    try:
        a, sh = _read_json(p)
    except Exception as exc:                                                         # R11 [A79.6] C04: both members named
        nc = dup_naming_code(exc, 'ROUTE_A_ATTEMPT_RESULT')
        return None, 'ROUTE_A_ATTEMPT_RESULT_UNREADABLE:%s%s' % (type(exc).__name__, (';' + nc) if nc else '')
    if sh != s:
        return None, 'ROUTE_A_ATTEMPT_RESULT_SHA_MISMATCH'
    return a, None


def route_a_tail_record(attempt):
    """[RA5/RA13] the route-A uv_tail record = attempt['result']['uv_tail'] (controller result_record)."""
    res = attempt.get('result') if isinstance(attempt, dict) else None
    if not isinstance(res, dict) or 'uv_tail' not in res:
        return None, 'FIELD_MISSING:route_a_attempt_result:result/uv_tail'
    return res['uv_tail'], None


def classify_failure(run, ctx):
    """V1 reading of a call that did not complete validly.  Returns {'class', 'codes', 'misses', ...} with codes only; every
    record-controlled string is mapped through _enum (verify blinding B1)."""
    r = run['result']
    st = r.get('status')
    st_code = _enum(st, pattern=_RE_UPPER_CODE)
    out = {'status': st_code, 'class': None, 'codes': [], 'misses': []}
    rc = run.get('receipt') or {}
    if rc.get('stop_reason'):
        out['class'] = 'MONITOR_STOP'
        out['codes'].append('MONITOR_STOP:%s' % _enum(rc.get('stop_reason'), allowed=STOP_REASONS))
    srec = [s for s in (r.get('stage_records') or []) if isinstance(s, dict)]
    failed = [_stage(s.get('name')) for s in srec if s.get('exit_code') not in (0, None)]
    out['failed_stages'] = failed
    for s in srec:                                     # bracket misses in any column pass (fs/rfs/le) [RA4] [V005 V1 (ii)]
        if not str(s.get('kind', '')).startswith('columns') or not isinstance(s.get('stage_dir'), str):
            continue
        fj = _side_json(Path(s['stage_dir']) / 'columns' / 'finish.json', 'COLUMN_FINISH', out['codes'])
        for x in ((fj or {}).get('failures') or []) if isinstance(fj, dict) else []:
            msg = str((x or {}).get('message', '')) if isinstance(x, dict) else str(x)
            if 'BRACKET' in msg.upper():
                idx = x.get('index') if isinstance(x, dict) else None
                out['misses'].append('%s:col%s:%s' % (_stage(s.get('name')),                  # [R3 validity F4] bounded
                                                      ('%04d' % idx) if KINDS['int'](idx) and 0 <= idx < DDO_N_COLUMNS else '?',
                                                      _enum(msg.split(':')[0], pattern=_RE_UPPER_CODE, other='BRACKET_MESSAGE_OTHER')))
    for p in r.get('passes') or []:                    # COMPLETED_INVALID: final-pass column failures
        if not isinstance(p, dict):
            continue
        for x in p.get('column_failures') or []:
            msg = str((x or {}).get('message', x)) if isinstance(x, dict) else str(x)
            if 'BRACKET' in msg.upper():
                pn = p.get('pass')
                out['misses'].append('pass%s:%s' % (pn if KINDS['int'](pn) and 0 <= pn <= MAX_REGISTERED_PASSES else '?',
                                                    _enum(msg.split(':')[0], pattern=_RE_UPPER_CODE, other='BRACKET_MESSAGE_OTHER')))
    if out['misses'] and out['class'] is None:
        block = ((run.get('spec_for_reading') or {}).get('numerics') or {}).get('brackets')
        out['bracket_block_is_RA4'] = bool(block is not None and canon(block) == canon(ctx['ra4_block']))
        out['class'] = 'BRACKET_HULL_MISS' if out['bracket_block_is_RA4'] else 'BRACKET_MISS_OFF_RA4_BLOCK'
        out['codes'].append(out['class'])
    if out['class'] is None and 'route_a' in failed:
        sd = next((Path(s['stage_dir']) for s in srec if s.get('name') == 'route_a' and isinstance(s.get('stage_dir'), str)), None)
        if sum(1 for s in srec if s.get('name') == 'route_a') > 1:   # R10 [A71 A06] the first of two route_a records was read silently
            out['codes'].append('ROUTE_A_STAGE_RECORD_REPEATED_A71')
            out['codes'] += unique_keys_codes([s.get('name') == 'route_a' or ('OTHER', j) for j, s in enumerate(srec)],
                                              'RESULT', 'stage_records')            # R11 [A79.6] both route_a records named
        msgs = []
        if sd is not None:
            for fp in sorted(sd.glob('attempt_*/failure.json')):
                fj = _side_json(fp, 'ROUTE_A_FAILURE', out['codes'])
                if isinstance(fj, dict):
                    msgs.append((_enum(fj.get('type'), pattern=_RE_IDENT), str(fj.get('message'))))
                else:
                    msgs.append(('UNREADABLE', ''))
        hit = [m for t, m in msgs if m in READOUT_REFUSALS]                                       # [A49.1] exact texts
        if hit:
            rao = run.get('route_a_outcome') if isinstance(run.get('route_a_outcome'), dict) else r.get('route_a_outcome')
            armed = isinstance(rao, dict) and isinstance(rao.get('ro1'), dict) and rao['ro1'].get('armed') is True
            out['class'] = 'ROUTE_A_READOUT_REFUSAL_UNDER_RO1' if armed else 'ROUTE_A_READOUT_REFUSAL_NO_RO1'   # [A50 N3] the record
            out['codes'].append('%s:%s' % (out['class'], hit[-1]))                                # [A42] [RA5 (c)]
            if len(set(hit)) > 1:                       # R10 [A71 A07] two different refusal texts: the last was kept silently
                out['codes'].append('ROUTE_A_READOUT_REFUSALS_DIFFER_A71')
                hj = [j for j, (t_, m_) in enumerate(msgs) if m_ in READOUT_REFUSALS]           # R11 [A79.6] both attempts named
                out['codes'].append('DUPLICATE_ENTRY_A71:ROUTE_A:attempt_failures[%d]:attempt_failures[%d]'
                                    % (hj[0], next(j for j in hj if msgs[j][1] != msgs[hj[0]][1])))

        else:
            out['class'] = 'ROUTE_A_STAGE_FAILED'
            out['codes'] += ['ROUTE_A_STAGE_FAILED:%s' % t for t, _ in msgs] or ['ROUTE_A_STAGE_FAILED']
    if out['class'] is None:
        if st == 'ROUTE_A_NO_FIXED_POINT':
            out['class'] = 'ROUTE_A_NO_FIXED_POINT'
        elif st in ('REFUSED', 'BLOCKED'):
            rs_ = r.get('reasons') if isinstance(r.get('reasons'), list) and r.get('reasons') else ['?']
            out['class'] = st
            # R11 [A75 A08] (Codex2 CX2-R10-A71-B2): every reason's token is read, not only reasons[0]; a token given twice is named
            toks = [_enum(str(x).split(':')[0].split(' ')[0], pattern=_RE_IDENT) for x in rs_]
            out['codes'] += ['%s:%s' % (st, t_) for t_ in dict.fromkeys(toks)]
            out['codes'] += unique_keys_codes([str(x) for x in rs_], 'RESULT', 'reasons')
        elif st == 'COMPLETED_INVALID':
            out['class'] = 'COMPLETED_INVALID'
        else:
            out['class'] = 'FAILED:%s' % (','.join(failed) or st_code)
        if not out['codes']:
            out['codes'].append(out['class'])
    return out


def adapter_side_file_codes(r):
    """R10 [A71] (A75 T01 / T02; Claude3 helper I T01, T02, T05): the pinned V005 adapt_result parses the last pass's field and rotation
    finish.json with plain json.loads (last-wins; the field one selects the V4/V5 packet).  Both are parsed strictly here first: [] or
    the loud read codes (a duplicate key makes the run invalid).  A file that is absent is not opened (the adapter skips it too)."""
    codes = []
    ps_ = r.get('passes') if isinstance(r, dict) and isinstance(r.get('passes'), list) else []
    last_ = ps_[-1] if ps_ and isinstance(ps_[-1], dict) else {}
    for k_, tag_ in (('field', 'FIELD_STAGE_FINISH'), ('rotation', 'ROTATION_STAGE_FINISH')):
        sd_ = last_.get(k_)
        if isinstance(sd_, str) and sd_:
            _side_json(Path(sd_) / 'finish.json', tag_, codes)
    return codes


def read_run(label, run_dir, ctx, ro1_required=None):
    """Read one registered run directory (result/finish/start/receipt, route-A attempt and tail record).  No output.
    [verify N3] never raises on a malformed record: every failure becomes a loud code in out['read_codes']."""
    out = {'label': label, 'dir': None if run_dir is None else str(run_dir), 'present': False, 'read_codes': []}
    if run_dir is None:
        out['absent'] = 'NOT_IN_MANIFEST'
        return out
    d = Path(run_dir)
    rp = d / 'result.json'
    if ctx.get('interlock_side_paths') and any(c5h_path_hit(fp) for fp in run_file_paths(run_dir)):   # R6 [validity F1]
        out.update(present=True, unreadable='RUN_FILE_INTO_THE_REGISTERED_C5H_RUN_REFUSED', result={}, result_sha256=None)
        return out
    if not rp.is_file():
        out['absent'] = 'NO_RESULT_JSON' if d.is_dir() else 'NO_RUN_DIR'
        return out
    try:
        r, rsha = _read_json(rp)
        if not isinstance(r, dict):
            raise TypeError('result not an object')
    except Exception as exc:
        out.update(present=True, unreadable='RESULT_UNREADABLE:%s' % type(exc).__name__, result={}, result_sha256=None)
        nc = dup_naming_code(exc, 'RESULT')                                          # R11 [A79.6] C02: both members named
        if nc:
            out['unreadable_detail'] = [nc]
        return out
    out.update(present=True, result=r, result_sha256=rsha, ro1_required=ro1_required, result_path=str(rp))
    if ctx.get('interlock_side_paths'):     # [A53 F2, defence in depth] test-mode full mode: record-controlled side paths into the
        rao_ = r.get('route_a_outcome') if isinstance(r.get('route_a_outcome'), dict) else {}      # registered C5H run are never
        side = [rao_.get('result_path')] + [x.get('stage_dir') for x in (r.get('stage_records') or []) if isinstance(x, dict)]  # opened
        side += [x.get(k) for x in (r.get('passes') or []) if isinstance(x, dict) for k in ('field', 'rotation')]
        if any(isinstance(x, str) and c5h_path_hit(x) for x in side):
            out.update(unreadable='SIDE_PATH_INTO_THE_REGISTERED_C5H_RUN_REFUSED')
            return out
    out['read_codes'] += adapter_side_file_codes(r)                              # R10 [A71 / A75 T01, T02]
    try:
        out['adapted'] = ctx['C5M'].adapt_result(rp)
        out['adapted_sha_equal'] = out['adapted']['result_sha256'] == rsha
    except Exception as exc:
        out.update(unreadable='ADAPT_RESULT_FAILED:%s' % type(exc).__name__)
        return out
    rows = r.get('rows')
    out['raw_row_ids'] = [x.get('id') if isinstance(x, dict) else None for x in rows] if isinstance(rows, list) else None
    out['finish'] = _side_json(d / 'finish.json', 'FINISH', out['read_codes'])
    out['receipt'] = _side_json(Path(str(d) + '.receipt.json'), 'RECEIPT', out['read_codes'])
    start = _side_json(d / 'start.json', 'START', out['read_codes'])
    start = start if isinstance(start, dict) else None
    out['spec_for_reading'] = r.get('normalized_spec') or (start or {}).get('normalized_spec') or {}
    out['spec_source'] = 'result' if r.get('normalized_spec') else ('start' if (start or {}).get('normalized_spec') else None)
    out['pass_rows_s9'] = pass_rows_ids_code(r, ctx['ids'])                     # R6 [A54 S9]: checked before any dict is built
    out['pass_rows_s9_naming'] = pass_rows_s9_naming(r, ctx['ids']) if out['pass_rows_s9'] else []      # R11 [A79.6]
    try:
        out['pass_rows'] = [] if out['pass_rows_s9'] else _pass_rows(r)
    except DuplicateEntry:                                                      # R10 [A71] unreachable after S9: S9 all the same
        out['pass_rows_s9'], out['pass_rows'] = PASS_ROWS_S9, []
    out['pass_rows_gap'] = pass_rows_gap(r)                                                      # [A54 B4]
    out['route_a_outcome'] = r.get('route_a_outcome')
    att, code = read_route_a_attempt(r)
    out['route_a_attempt_code'] = code
    out['uvt_record'], out['uvt_code'] = (None, code) if att is None else route_a_tail_record(att)
    ok = r.get('status') == 'COMPLETED' and r.get('valid') is True
    try:
        out['failure'] = None if ok else classify_failure(out, ctx)
    except Exception as exc:
        out['failure'] = {'class': 'FAILURE_UNREADABLE', 'codes': ['FAILURE_UNREADABLE:%s' % type(exc).__name__], 'misses': [],
                          'status': None, 'failed_stages': []}
    return out


def read_run_sha_only(label, run_dir):
    """[verify blinding B2] --gates-only: a case result is read as the sha256 of its bytes ONLY (no parse, no rows, no packet,
    no side file).  The gates need nothing else from a case (T2I/EA/SRB_ROT/RB_FP cross-references)."""
    out = {'label': label, 'dir': None if run_dir is None else str(run_dir), 'present': False, 'sha_only': True}
    if run_dir is None:
        out['absent'] = 'NOT_IN_MANIFEST'
        return out
    rp = Path(run_dir) / 'result.json'
    if not rp.is_file():
        out['absent'] = 'NO_RESULT_JSON' if Path(run_dir).is_dir() else 'NO_RUN_DIR'
        return out
    out.update(present=True, result_sha256=sha256_file(rp))
    return out


def read_numerics_only(run_dir):
    """[verify blinding B3] C5H for --validity-only --case C4T-D5: normalized_spec.numerics only (result.json, or start.json
    when the result lacks normalized_spec); rows, stages and packets are never touched.  Absent result -> None (as before)."""
    if run_dir is None:
        return None
    rp = Path(run_dir) / 'result.json'
    if not rp.is_file():
        return None
    try:
        r = _read_json(rp)[0]
        ns = r.get('normalized_spec') if isinstance(r, dict) else None
        if not ns:
            st = _side_json(Path(run_dir) / 'start.json', 'START', [])
            ns = (st or {}).get('normalized_spec') if isinstance(st, dict) else None
        num = (ns or {}).get('numerics')
        del r
        return json.loads(canon(num)) if isinstance(num, dict) else None
    except Exception:
        return None


def manifest_run_paths(manifest):
    """[R3 validity F2] every run directory a manifest names: cases.*, identity_runs.*, rpair.*.members.* (slot, path)."""
    out = [('cases:%s' % k, d) for k, d in sorted((manifest.get('cases') or {}).items())]
    out += [('identity_runs:%s' % k, d) for k, d in sorted((manifest.get('identity_runs') or {}).items())]
    for pid, rp in sorted((manifest.get('rpair') or {}).items()):
        out += [('rpair:%s:%s' % (pid, m), d) for m, d in sorted(((rp or {}).get('members') or {}).items())]
    return out


class RegisteredIdentityUnavailable(OSError):
    """R11 [A79.3] (Codex2 0455, CX2-R10-H07-S1; r10 recheck validity B2, order B4): a registered C5H run directory could not be
    stat'ed, so its (st_dev, st_ino) identity is unknown.  Every guard that needs the identity REFUSES (never an empty set)."""


REGISTERED_IDENTITY_CODE = 'C5H_REGISTERED_RUN_IDENTITY_UNAVAILABLE_A79_3'


def _registered_run_identities():
    """R10 [H-07] (st_dev, st_ino) of each registered C5H run directory (os.stat of the directory itself: metadata only, nothing
    inside it is listed or opened), and their devices.  R11 [A79.3]: a directory that cannot be stat'ed RAISES
    RegisteredIdentityUnavailable (r10 dropped it silently, so the identity and hard-link layers turned off)."""
    ids, devs = set(), set()
    for reg_dir in C5H_REGISTERED_RUN_DIRS:
        try:
            st = os.stat(reg_dir)
        except OSError as exc:
            raise RegisteredIdentityUnavailable('%s:%s' % (REGISTERED_IDENTITY_CODE, type(exc).__name__))
        ids.add((st.st_dev, st.st_ino))
        devs.add(st.st_dev)
    if not ids:
        raise RegisteredIdentityUnavailable('%s:NO_REGISTERED_DIRECTORY' % REGISTERED_IDENTITY_CODE)
    return ids, devs


def registered_identity_code():
    """R11 [A79.3] None when every registered C5H run directory has a readable identity, else REGISTERED_IDENTITY_CODE."""
    try:
        _registered_run_identities()
    except RegisteredIdentityUnavailable:
        return REGISTERED_IDENTITY_CODE
    return None


def _nfc(x):
    """R11 [A79.5] every string comparison is made on the NFC form (APFS resolves NFC and NFD spellings to one file)."""
    return unicodedata.normalize('NFC', x)


def _lead(p):
    """R11 (r10 recheck validity N3): a leading '//' (kept by normpath) is read as '/'."""
    return '/' + p.lstrip('/') if p.startswith('/') else p


def _is_volfs(p):
    """macOS volfs: /.vol/<device>/<inode>[/...] names a file by inode, bypassing every name and realpath test.  R11: NFC, and a
    leading '//' spelling too (r10 recheck validity N3)."""
    parts = Path(_lead(_nfc(p))).parts
    return len(parts) >= 2 and parts[0] == '/' and parts[1].casefold() == '.vol'


_MAX_SYMLINKS = 40


def _resolved_walk_hit(raw, ids):
    """R11 [A79.5] (Claude3 0070 §1; helper I P4 H16/H17): resolve the absolute path string raw component by component, the way the
    kernel does (a symlink is followed BEFORE a later '..' is applied, so 'link/..' is the parent of the link's target, not of the
    link), and at EVERY resolved prefix check, before any metadata call on its child: the registered name (NFC, casefolded), the
    /.vol root, and the registered (st_dev, st_ino).  So a symlink to the /System/Volumes/Data firmlink spelling or to an NFD
    spelling of the run, of a file in it, or of a subdirectory followed by '/..', is caught at the run directory itself; nothing
    inside the run is lstat'ed, stat'ed, read-linked or opened.  Returns (hit, final_stat_or_None)."""
    name = _nfc(C5H_REGISTERED_RUN_NAME).casefold()
    todo = [c for c in _nfc(raw).split('/') if c]
    cur, final, links = '/', None, 0
    while todo:
        c = todo.pop(0)
        if c == '.':
            continue
        if c == '..':
            cur = os.path.dirname(cur) or '/'                       # cur is resolved: its parent was walked (and checked) before
            final = None
            continue
        if c.casefold() == name or (cur == '/' and c.casefold() == '.vol'):
            return True, None
        cand = os.path.join(cur, c)
        try:
            lst = os.lstat(cand)
        except (FileNotFoundError, NotADirectoryError):
            return False, None                                       # does not exist: nothing can be opened through it
        if stat_mod.S_ISLNK(lst.st_mode):
            links += 1
            if links > _MAX_SYMLINKS:
                return True, None                                    # a link loop or a deep chain: refuse (stricter)
            tgt = _nfc(os.readlink(cand))
            if tgt.startswith('/'):
                cur = '/'
            todo = [x for x in tgt.split('/') if x] + todo
            final = None
            continue
        if (lst.st_dev, lst.st_ino) in ids:
            return True, None
        cur, final = cand, lst
    return False, final


def c5h_path_hit(path):
    """[A53 r4 validity F2] no file is opened (metadata only, never inside a registered run): True when the path can lead into the
    registered C5H run.  R10 [H-07] (Claude3 0065, A72): /.vol paths, directory identity (st_dev, st_ino), hard links.  R11:
      - [A79.3] the registered identity unavailable (a stat failure of a registered directory): True for every path (refused);
      - [A79.5] NFC before every string comparison; the name test and the identity walk on the lexical spelling AND on the RESOLVED
        path (_resolved_walk_hit, kernel order: links followed before '..'), so a firmlink, a second mount, an NFD spelling or a
        'symlink/..' detour is caught at the run directory before anything inside it is touched; then every prefix of realpath(s)
        is stat-walked against the registered identity too, and the realpath string tests run on the NFC casefolded form;
      - (r10 recheck validity N3) a leading '//' is read as '/' before the /.vol test (no volfs lstat).
    A regular file with st_nlink > 1 on a registered run's device is a hit (DECLARED, NEW-64, accepted in A79).  A path that does
    not exist is not a hit; an unreadable or permission-denied path is a hit (stricter)."""
    if path is None:
        return False
    try:
        s = os.fspath(path)
        s = os.fsdecode(s) if isinstance(s, bytes) else str(s)
        s = _lead(_nfc(s))
        raw = s if s.startswith('/') else _lead(_nfc(os.getcwd()).rstrip('/') + '/' + s)
        norm = _lead(os.path.normpath(raw))
        name = _nfc(C5H_REGISTERED_RUN_NAME).casefold()
        if name in [x.casefold() for x in Path(norm).parts] or name in [x.casefold() for x in raw.split('/') if x]:
            return True
        if _is_volfs(norm) or _is_volfs(raw):                                                   # R10 [H-07]
            return True
        try:
            ids, devs = _registered_run_identities()                                            # R11 [A79.3]
        except RegisteredIdentityUnavailable:
            return True
        hit, final = _resolved_walk_hit(raw, ids)                                                # R11 [A79.5] kernel order
        if hit:
            return True
        hit_n, _ = _resolved_walk_hit(norm, ids)                                                 # the lexical spelling too
        if hit_n:
            return True
        rp0 = _lead(_nfc(os.path.realpath(raw)))       # safe now: no prefix of the resolved path is a registered run directory
        if _is_volfs(rp0) or name in [x.casefold() for x in Path(rp0).parts]:
            return True
        rp = rp0.casefold()
        for reg_dir in C5H_REGISTERED_RUN_DIRS:
            rr = _nfc(os.path.realpath(reg_dir)).casefold().rstrip('/')
            if rp == rr or rp.startswith(rr + '/'):
                return True
        cur = None
        for comp in Path(rp0).parts:                                     # [A79.5] every prefix of realpath(s), stat-walked
            cur = comp if cur is None else os.path.join(cur, comp)
            try:
                st = os.stat(cur)
            except (FileNotFoundError, NotADirectoryError):
                break
            if (st.st_dev, st.st_ino) in ids:
                return True
        if final is not None and stat_mod.S_ISREG(final.st_mode) and final.st_nlink > 1 and final.st_dev in devs:
            return True                                                                          # a hard link on the run's device
    except (OSError, ValueError, TypeError):
        return True                                       # unreadable path string or metadata: refuse (stricter)
    return False


def run_file_paths(run_dir):
    """R6 [r5 recheck validity F1] every file read_run and c5h_interlock open directly for a run directory: result, finish, start,
    the receipt and the launch marker (string paths; nothing is opened here)."""
    d = str(run_dir)
    return [os.path.join(d, 'result.json'), os.path.join(d, 'finish.json'), os.path.join(d, 'start.json'), d + '.receipt.json',
            d + '.receipt.json.launch.json']


_GUARD = {'installed': False, 'active': False, 'busy': False, 'refused': 0}


def _interlock_audit_hook(event, args):
    """R6 [r5 recheck validity F1, defence in depth] in test-mode full mode, any open (by this script or the pinned V005 compare)
    whose realpath lies at or inside the registered C5H run is refused (PermissionError) before a byte is read; string-only."""
    if not _GUARD['active'] or _GUARD['busy'] or event != 'open' or not args:
        return
    p = args[0]
    if isinstance(p, int) or not isinstance(p, (str, bytes, os.PathLike)):
        return
    _GUARD['busy'] = True
    try:
        hit = c5h_path_hit(os.fsdecode(p))
    finally:
        _GUARD['busy'] = False
    if hit:
        _GUARD['refused'] += 1
        raise PermissionError('R6 interlock guard: an open into the registered C5H run was refused (test mode, full mode)')


def interlock_guard(active):
    """Arm (test-mode full mode) or disarm the audit-hook guard; installed once per process (an audit hook cannot be removed)."""
    if active and not _GUARD['installed']:
        sys.addaudithook(_interlock_audit_hook)
        _GUARD['installed'] = True
    _GUARD['active'] = bool(active)
    if active:
        _GUARD['refused'] = 0


def c5h_interlock(run_dir):
    """[verify blinding B4] test mode, full mode: REFUSE when the C5H entry is the registered C5H call.  The name check uses no
    file access; then only the launch record / start.json call-spec field is read (never result.json, rows or stages).
    [R4 validity F5] the name check is case-insensitive (the run volume is case-insensitive), and a directory that is the
    registered run directory under another name (symlink, alias, other case) is refused by os.stat identity (no file opened).
    [A53 r4 validity F2] also refused, before any marker file is read: any path component casefolding to the registered name,
    or a realpath at or inside the registered directory (c5h_path_hit, string-only)."""
    if run_dir is None:
        return None
    if os.path.basename(os.path.normpath(str(run_dir))).casefold() == C5H_REGISTERED_RUN_NAME.casefold():
        return 'C5H entry is the registered C5H run directory (%s)' % C5H_REGISTERED_RUN_NAME
    if c5h_path_hit(run_dir):                         # [A53 r4 validity F2] an ancestor component, or inside the registered dir
        return 'C5H entry lies inside the registered C5H run directory (%s), by path component or realpath' % C5H_REGISTERED_RUN_NAME
    for reg_dir in C5H_REGISTERED_RUN_DIRS:
        try:
            if os.path.isdir(str(run_dir)) and os.path.isdir(reg_dir) and os.path.samefile(str(run_dir), reg_dir):
                return 'C5H entry is the registered C5H run directory under another name (%s)' % C5H_REGISTERED_RUN_NAME
        except OSError:
            pass
    for fp in run_file_paths(run_dir):                # R6 [r5 recheck validity F1] each file's realpath, before any file is read
        if c5h_path_hit(fp):
            return ('C5H entry file %s resolves into the registered C5H run directory (%s), by realpath'
                    % (os.path.basename(fp), C5H_REGISTERED_RUN_NAME))
    for p, path in ((Path(str(run_dir) + '.receipt.json.launch.json'), ('pins', 'spec', 'sha256')),
                    (Path(str(run_dir)) / 'start.json', ('call_spec_sha256',))):
        mc = []
        x = _side_json(p, 'INTERLOCK', mc)
        if mc:                                 # R10 [A75.2 S01] an unreadable / duplicate-key marker refuses (r8 read it as absent)
            return 'C5H entry marker %s is unreadable or carries a duplicate key (%s): refused, fail closed (A71)' % (p.name, '; '.join(mc))
        for k in path:
            x = x.get(k) if isinstance(x, dict) else None
        if x == PIN_C5H_SPEC[1]:
            return 'C5H entry carries the registered C5H call spec 60b46130 (%s)' % p.name
    return None


# ============================================================================================ tail and RO1 records
def check_uvt_record(rec, reg, where='uvt', radii=None):
    """[R1 MT_monitor] [R1 route_a_noise] [IA6] fields of the route-A uv_tail record.  Returns (codes, info).
    [A48 AMB-22] [verify G4/B3] E_A_rows_km_s_accepted is USED only when the record also carries probe_R_m equal to the 12
    registered row radii in row_ids order; otherwise its row order is unverified and E^A comes from the EA replay record."""
    codes, info = [], {'flagged': None, 'E_A_rows_km_s': None, 'E_A_row_order': None, 'accepted_iteration': None,
                       'M_T_accepted': None}
    try:
        if need(rec, 'schema', where, 'str') != UVT_RA_RECORD_SCHEMA:
            codes.append('UVT_SCHEMA')
        if need(rec, 'outcome', where, 'str') != 'CONVERGED_FINITE_FIXED_POINT':
            codes.append('UVT_OUTCOME_NOT_CONVERGED')
        if need(rec, 'production_admissible', where) is not True:
            codes.append('UVT_NOT_PRODUCTION_ADMISSIBLE')                                               # [IA6]
        if need(rec, 'admissibility', where, 'str') != 'production':
            codes.append('UVT_ADMISSIBILITY_NOT_PRODUCTION')
        if reg is not None and need(rec, 'config_sha256', where, 'sha') != reg.get('uv_tail_config_sha256'):
            codes.append('UVT_CONFIG_SHA_NOT_REGISTERED')                                              # [R1 validity V3]
        flags = need(rec, 'flags', where, 'list')
        ms = need(rec, 'monitor_status', where, 'str')
        thr = need(rec, 'M_T_threshold', where, 'num')
        mt = need(rec, 'M_T_accepted', where)
        acc = need(rec, 'accepted_iteration', where)
        ea = need(rec, 'E_A_rows_km_s_accepted', where)
        if thr != MT_THRESHOLD:
            codes.append('UVT_MT_THRESHOLD_NOT_PRENAMED')
        if any(f != FLAG_TSU for f in flags):
            codes.append('UVT_UNKNOWN_FLAG')
        elif len(flags) > 1:                                    # R10 [A71] a repeated flag (c2v004 S1 class): a record defect
            codes.append('UVT_FLAG_REPEATED_A71')
            codes += unique_keys_codes(flags, 'UVT', 'flags')      # R11 [A79.6] both entries named (Claude3 0070 §2, B09)
        if ms not in ('M_T_WITHIN_THRESHOLD', 'FLAGGED'):
            codes.append('UVT_MONITOR_STATUS:%s' % _enum(ms, pattern=_RE_UPPER_CODE))                  # M_T unreadable -> loud
        if not _num(mt):
            codes.append('UVT_M_T_ACCEPTED_NOT_A_NUMBER')
        elif (mt > MT_THRESHOLD) != (FLAG_TSU in flags) or (ms == 'FLAGGED') != (FLAG_TSU in flags):
            codes.append('UVT_FLAG_INCONSISTENT')
        if not KINDS['int'](acc):
            codes.append('UVT_ACCEPTED_ITERATION_NOT_INT')
        if ea is not None and not KINDS['num12>=0'](ea):
            codes.append('UVT_E_A_ROWS_NOT_12_NONNEGATIVE')
        order = None
        if KINDS['num12>=0'](ea):
            pr = rec.get('probe_R_m')
            if pr is None:
                order = 'UNVERIFIED_NO_PROBE_R'
            elif radii is not None and radii_equal(pr, radii):
                order = 'VERIFIED'
            else:
                order = 'PROBE_R_NOT_REGISTERED_ROW_RADII'
                codes.append('UVT_PROBE_R_NOT_REGISTERED_ROW_RADII')
        info.update(flagged=FLAG_TSU in flags, E_A_rows_km_s=ea if order == 'VERIFIED' else None, E_A_row_order=order,
                    accepted_iteration=acc if KINDS['int'](acc) else None, M_T_accepted=mt if _num(mt) else None)
    except FieldMissing as exc:
        codes.append(exc.code)
    return codes, info


RO1_BLOCK_KEYS = ('rule', 'fired', 'events', 'armed', 'worker_sha256', 'binding_sha256')      # R11 [A77.2] v010 ro1_outcome
# the r5 worker-kind maps (kept for readers of r8); R10 [A72] check_ro1_record reads the ACTIVE build's maps (ro1_worker_kind /
# ro1_nodes_worker_kind), which equal these under the built-in r5 build.  [A71] the build refuses two pins sharing one sha.
RO1_WORKER_KIND = {PIN_RO1_CUSTODY['worker'][1]: 'serial', PIN_RO1_CUSTODY['worker_parallel'][1]: 'parallel'}
RO1_NODES_WORKER_KIND = {PIN_RO1_NODES_CUSTODY['worker'][1]: 'serial', PIN_RO1_NODES_CUSTODY['worker_parallel'][1]: 'parallel'}


def registered_source_rule_is_nodes(reg):
    """[R4 validity F1] True when a registered case entry's /numerics uv_tail declares source_rule {rule: nodes_v001, ..}
    (C4T-D5 by the text; its R-PAIR member is validated against the same registration).  Tail-OFF entries: False."""
    if not (isinstance(reg, dict) and reg.get('tail')):
        return False
    uv = ((reg.get('normalized_spec_equal') or {}).get('/numerics') or {}).get('uv_tail')
    sr = uv.get('source_rule') if isinstance(uv, dict) else None
    return isinstance(sr, dict) and sr.get('rule') == 'nodes_v001'


def check_ro1_record(rao, where='result', require_armed=True, nodes=False):
    """[RA5] route_a_outcome.ro1: recorded, never an invalidity; a missing or malformed record is a loud V3 code.
    [A49.2] a case that requires RO1 needs ro1.armed is True (an unarmed worker cannot pass as an RO1 run); an unarmed
    record (armed false) must not have fired.  [A50 root items 11, 12] an armed record names a worker and the binding on the
    declared custody list (PIN_RO1_CUSTODY); an unarmed record names neither (the c2v002 driver patch writes None).
    [R4 validity F1] nodes=True (registered source rule nodes_v001): the worker must be a nodes_v001 RO1 worker
    (PIN_RO1_NODES_CUSTODY); nodes=False: a continuum worker.  A worker of the other list reads its own named code."""
    codes, info = [], {'present': False, 'fired': None, 'armed': None, 'events': [], 'worker_kind': None}
    wk_c, wk_n = ro1_worker_kind(), ro1_nodes_worker_kind()                                          # R10 [A72] the active build
    kinds, other = (wk_n, wk_c) if nodes else (wk_c, wk_n)
    try:
        ro1 = need(rao if isinstance(rao, dict) else {}, 'ro1', where + ':route_a_outcome', 'dict')
        info['present'] = True
        # R11 [A77.2 'the record is parsed strictly'] the block carries exactly the keys driver v010 ro1_outcome writes (r5 b5cc62af
        # L1941-1952: rule, fired, events, armed, worker_sha256, binding_sha256; inadmissible_record only when one was kept)
        if set(ro1) - set(RO1_BLOCK_KEYS) - {'inadmissible_record'} or set(RO1_BLOCK_KEYS) - set(ro1):
            codes.append('RO1_BLOCK_KEYS_NOT_THE_DRIVER_SET_A77_2')
        if need(ro1, 'rule', where + ':route_a_outcome/ro1', 'str') != 'RO1':
            codes.append('RO1_RULE_NAME')
        fired = need(ro1, 'fired', where + ':route_a_outcome/ro1', 'bool')
        ev = need(ro1, 'events', where + ':route_a_outcome/ro1', 'list')
        armed = need(ro1, 'armed', where + ':route_a_outcome/ro1', 'bool')
        wk = need(ro1, 'worker_sha256', where + ':route_a_outcome/ro1')
        bd = need(ro1, 'binding_sha256', where + ':route_a_outcome/ro1')
        info.update(fired=fired, armed=armed)
        if not ((wk is None or _hex64(wk)) and (bd is None or _hex64(bd))):   # R11 (Codex2 BR-N1) typed before any map lookup
            codes.append('RO1_PIN_NOT_A_SHA256_OR_NULL_A77_2')
            wk = wk if _hex64(wk) else None
            bd = bd if _hex64(bd) else None
        if 'inadmissible_record' in ro1:              # R6 [r5 recheck validity F3] v010 r4 ro1_outcome keeps an inadmissible
            codes.append('RO1_INADMISSIBLE_RECORD')   # readout-refusal record there (fired false); comparator c2v003 fails it too
        if require_armed and armed is not True:
            codes.append('RO1_NOT_ARMED')                                                         # [A49.2]
        if armed and (wk is None or bd is None):                     # R11 [A77.2] an armed record names both pins as shas
            codes.append('RO1_ARMED_RECORD_WITHOUT_BOTH_PINS_A77_2')
        if armed:
            if wk in other:                                                                        # [R4 validity F1]
                codes.append('RO1_CONTINUUM_WORKER_ON_A_NODES_V001_CASE' if nodes else 'RO1_NODES_V001_WORKER_ON_A_NON_NODES_CASE')
            elif wk not in kinds:
                codes.append('RO1_WORKER_NOT_ON_CUSTODY_LIST')
            if bd != ro1_custody_sha('binding'):
                codes.append('RO1_BINDING_NOT_ON_CUSTODY_LIST')
            info['worker_kind'] = kinds.get(wk)
        elif wk is not None or bd is not None:
            codes.append('RO1_PINS_ON_AN_UNARMED_RECORD')

        if fired and not armed:
            codes.append('RO1_FIRED_WITHOUT_ARMED')
        if fired and not ev:
            codes.append('RO1_FIRED_WITHOUT_EVENTS')
        if not fired and ev:
            codes.append('RO1_EVENTS_WITHOUT_FIRED')
        if fired and len(ev) > 1:              # R11 [A75 B10] (Codex2 BR-B1): driver v010 ro1_outcome writes events = [the record], one
            codes.append('RO1_FIRED_RECORD_CARRIES_MORE_THAN_ONE_EVENT_A75_B10')
        ekeys = []
        for j, e in enumerate(ev):
            w = '%s:route_a_outcome/ro1/events[%d]' % (where, j)
            if need(e, 'code', w, 'str') != RO1_CODE:
                codes.append('RO1_EVENT_CODE')
            if need(e, 'refusal', w, 'str') not in READOUT_REFUSALS:
                codes.append('RO1_EVENT_REFUSAL')
            # [R3 validity F1] the RO1 c2v002 binding (86af6198 _ro1_record) writes query/phi_rad/R_kpc/numerator/
            # denominator as None when the value is not available (numerator/denominator are None whenever the refusal was
            # raised by circular_trial_readout, not by pressure_streaming_speed): each field must be present and a finite
            # number (query an int) or null.  A non-finite value (the producer's repr string) stays a loud FIELD_TYPE code.
            q = need(e, 'query', w, 'int|null')
            for k in ('phi_rad', 'R_kpc', 'numerator', 'denominator'):
                need(e, k, w, 'num|null')
            if need(e, 'after_convergence', w, 'bool') is not True:
                codes.append('RO1_EVENT_BEFORE_CONVERGENCE')                                           # [RA5 (c)]
            ekeys.append((q, canon(e.get('phi_rad')), canon(e.get('R_kpc')), e['refusal']))
            info['events'].append({'code': e['code'] if e['code'] == RO1_CODE else 'OTHER',
                                   'refusal': e['refusal'] if e['refusal'] in READOUT_REFUSALS else 'OTHER', 'query': q})
        # R11 [A75 B10] [A79.1] (Codex2 BR-B1): an event is identified by (query, phi_rad, R_kpc, refusal); one event given twice is a
        # record defect naming both events (r10 checked each event alone)
        codes += unique_keys_codes(ekeys, 'RO1', 'events')
    except FieldMissing as exc:
        codes.append(exc.code)
    return codes, info


# ============================================================================================ per-case validity
def _normalized(run):
    return (run.get('result') or {}).get('normalized_spec') or {}


def numerics_equal_except(a, b, exempt):
    """[RA1] [A47 I4] canonical equality of numerics blocks except the named top-level / dotted keys."""
    a, b = json.loads(canon(a or {})), json.loads(canon(b or {}))
    for k in exempt:
        parts = k.split('.')
        for x in (a, b):
            cur = x
            for p in parts[:-1]:
                cur = cur.get(p) if isinstance(cur, dict) else None
            if isinstance(cur, dict):
                cur.pop(parts[-1], None)
    diff = sorted(set(_leaves(a)) ^ set(_leaves(b)))
    return canon(a) == canon(b), diff


def _key_paths(o, p='', acc=None):
    acc = set() if acc is None else acc
    if isinstance(o, dict):
        for k, v in o.items():
            q = p + '/' + str(k)
            acc.add(q)
            _key_paths(v, q, acc)
    return acc


def registered_numerics_paths(ctx):
    """[R3 validity F4] every key path of the registered numerics: the C5H spec reference numerics (A50 S1) and each T-case
    /numerics registered in the case block."""
    acc = _key_paths(ctx.get('c5h_numerics_reference') or {})
    for e in (((ctx.get('case_block') or {}).get('cases')) or {}).values():
        _key_paths(((e or {}).get('normalized_spec_equal') or {}).get('/numerics') or {}, '', acc)
    return acc


def diff_paths_code(diff, ctx, n=8):
    """[R3 validity F4] the V3 numerics diff paths of a code: a path is emitted only when it is a key path of the registered
    numerics; any other (record-controlled) key path becomes NUMERICS_PATH_NOT_REGISTERED."""
    reg = registered_numerics_paths(ctx)
    ps = sorted({d.split('=')[0] for d in diff})
    return ';'.join(sorted({p if p in reg else NUMERICS_PATH_OTHER for p in ps})[:n])


def _leaves(o, p=''):
    if isinstance(o, dict):
        out = []
        for k, v in o.items():
            out += _leaves(v, p + '/' + str(k))
        return out or [p + '={}']
    return [p + '=' + canon(o)]


def receipt_codes(run):
    """[A48 AMB-26] [verify fields B1] a receipt is REQUIRED for every run case; it must name this result (sha from bytes and
    path), its spec and driver pins must equal the result's, and its driver_status the result status; a COMPLETED result
    needs status FINISHED, exit_code 0 and no stop_reason."""
    rc = run.get('receipt')
    r = run.get('result') or {}
    if rc is None:
        return [c for c in run.get('read_codes', []) if c.startswith('RECEIPT_')] or ['RECEIPT_ABSENT']
    if not isinstance(rc, dict):
        return ['RECEIPT_NOT_AN_OBJECT']
    codes = []
    if rc.get('schema') != RECEIPT_SCHEMA:
        codes.append('RECEIPT_SCHEMA')
    res = rc.get('result') if isinstance(rc.get('result'), dict) else {}
    if res.get('sha256') != run.get('result_sha256'):
        codes.append('RECEIPT_RESULT_SHA_MISMATCH')
    rp = res.get('path')
    try:
        same = isinstance(rp, str) and run.get('result_path') is not None and Path(rp).resolve() == Path(run['result_path']).resolve()
    except Exception:
        same = False
    if not same:
        codes.append('RECEIPT_RESULT_PATH_MISMATCH')
    pins = rc.get('pins') if isinstance(rc.get('pins'), dict) else {}
    if (pins.get('spec') or {}).get('sha256') != r.get('call_spec_sha256'):
        codes.append('RECEIPT_SPEC_PIN_MISMATCH')
    if (pins.get('driver') or {}).get('sha256') != r.get('driver_sha256'):
        codes.append('RECEIPT_DRIVER_PIN_MISMATCH')
    if rc.get('driver_status') != r.get('status'):
        codes.append('RECEIPT_DRIVER_STATUS_MISMATCH')
    if r.get('status') == 'COMPLETED':
        if rc.get('status') != 'FINISHED':
            codes.append('RECEIPT_STATUS_NOT_FINISHED')
        if rc.get('exit_code') != 0 or isinstance(rc.get('exit_code'), bool):
            codes.append('RECEIPT_EXIT_CODE_NOT_0')
        if rc.get('stop_reason') is not None:
            codes.append('RECEIPT_STOP_REASON:%s' % _enum(rc.get('stop_reason'), allowed=STOP_REASONS))
    return codes


def rows_codes(run, ids):
    """[V005 V1] [verify D2] exactly the 12 registered row ids, each once (a duplicate id would hide a row: adapt_result keeps
    the last copy), with finite speeds."""
    raw = run.get('raw_row_ids')
    a = run.get('adapted') or {}
    codes = []
    if not (isinstance(raw, list) and len(raw) == len(ids) and len(set(raw)) == len(raw) and sorted(raw) == sorted(ids)):
        codes.append('ROWS_NOT_EXACTLY_THE_12_REGISTERED_IDS_EACH_ONCE')
        if isinstance(raw, list):                                    # R11 [A79.6] a repeated final row id: both entries named
            codes += unique_keys_codes([x if isinstance(x, str) else ('NOT_A_STRING', j) for j, x in enumerate(raw)], 'RUN', 'rows')
    if not all(_num((a.get('rows') or {}).get(i)) for i in ids):
        codes.append('ROWS_NOT_FINITE')
    return codes


def v2_check(run, ctx, bound=None):
    """[V005 V2] final-pass max_abs_change_km_s <= 0.0125, cross-checked against the pass rows (verify D9: on every real R3
    record the field equals max_i |d_last_i| over the 12 rows).  [A50 N4] bound: the run's registered speed bound (an R-PAIR
    Picard-branch member: 0.0025); default the V005 tau_picard."""
    a = run['adapted']
    lc = a.get('last_change_km_s')
    ok = bool(_num(lc) and lc <= (ctx['tau_picard'] if bound is None else bound))
    codes = []
    pr = run.get('pass_rows') or []
    if ok and run.get('pass_rows_gap'):          # [A54 B4] the cross-check needs the record's last two passes intact and consecutive
        ps = (run.get('result') or {}).get('passes')
        intact = (isinstance(ps, list) and len(ps) >= 2 and all(isinstance(x, dict) and isinstance(x.get('rows'), list) and x['rows']
                                                                 for x in ps[-2:])
                  and KINDS['int'](ps[-1].get('pass')) and KINDS['int'](ps[-2].get('pass')) and ps[-1]['pass'] == ps[-2]['pass'] + 1)
        if not intact:
            ok = False
            codes.append('V2_CROSSCHECK_IMPOSSIBLE_PASS_ROW_GAP_AT_THE_LAST_PASSES')
    if ok and len(pr) >= 2:
        d = [pr[-1].get(i) for i in ctx['ids']], [pr[-2].get(i) for i in ctx['ids']]
        if not all(_num(x) for x in d[0] + d[1]):
            ok = False
            codes.append('V2_PASS_ROWS_NOT_FINITE')
        else:
            m = max(abs(x - y) for x, y in zip(*d))
            if abs(lc - m) > 1e-9 * max(abs(m), 1e-3):
                ok = False
                codes.append('V2_FIELD_INCONSISTENT_WITH_PASS_ROWS')
    return ok, codes


def case_validity(label, run, ctx, packet=None, i1t=None, c5h_numerics=None, rpair=None, extra=None):
    """V005 per_case_validity_gates V1-V6 [V005], V3 against the registered V007 case block [R1 validity_gates] [RA1] [RA4]
    [A47 I4/I5], RO1 recorded [RA5], BRACKET_HULL_MISS reading [RA4], I1-T [R1 I1T] (gate status PASS AND per build PASS,
    verify D1/D5), receipts [A48 AMB-26], key-equivalence map [A48 AMB-13], C5H admission [A48 AMB-20].  Codes only.
    i1t: {'status': I1T gate status, 'per': {build key: PASS|FAIL|UNCOVERED}} or None.
    rpair: None, or {'base': label, 'branch': 'PICARD'|'ROUTE_A', 'base_run': run} for an R-PAIR member.
    extra: {'b0_spec_shas': set or None}.  Never raises (verify N3): an exception becomes reading VALIDITY_EXCEPTION."""
    try:
        return _case_validity(label, run, ctx, packet, i1t, c5h_numerics, rpair, extra or {})
    except Exception as exc:
        return {'label': label, 'present': bool(run.get('present')), 'valid_all': False, 'failed': ['V1'], 'V1': False,
                'V1_codes': ['VALIDITY_EXCEPTION:%s' % type(exc).__name__], 'V3_mismatch': [], 'notes': [],
                'reading': 'VALIDITY_EXCEPTION', 'uvt': {}, 'ro1': {}}


def _case_validity(label, run, ctx, packet, i1t, c5h_numerics, rpair, extra):
    cb = ctx['case_block'] or {'cases': {}}
    base = rpair['base'] if rpair else label
    reg = cb['cases'].get(base)
    v = {'label': label, 'present': bool(run.get('present')), 'V3_mismatch': [], 'V1_codes': [], 'notes': [], 'reading': None}
    if not run.get('present'):
        v.update(valid_all=False, failed=['missing'], reading='MISSING:%s' % run.get('absent'))
        return v
    if reg is None:
        v.update(valid_all=False, failed=['unregistered'], reading='UNREGISTERED_CASE')
        return v
    c5h_member = bool(rpair) and base == C5H
    picard_member = bool(rpair) and rpair.get('branch') == 'PICARD'          # [A53] admits its base's route A
    if c5h_member:          # [A50 root item 11] a C5H R-PAIR member runs under v010 tail OFF; [A52.3] ROUTE_A: RO1 workers armed;
        reg = dict(reg, drivers_allowed=list((cb['cases'].get('C4T-D5') or {}).get('drivers_allowed') or []),   # [A53] PICARD:
                   ro1_required=not picard_member, tail=False)                          # no RO1 (unarmed, unfired block)
    if run.get('unreadable'):
        v.update(valid_all=False, failed=['V1'], V1=False, V1_codes=[run['unreadable']] + list(run.get('unreadable_detail') or []),
                 reading=run['unreadable'])
        return v
    a = run['adapted']
    r = run['result']
    ids = ctx['ids']
    completed = a.get('status') == 'COMPLETED'
    # ---- V1 [V005 V1] + result custody + receipt [A48 AMB-26]
    v1 = a['schema'] == RESULT_SCHEMA and completed and a['valid'] is True
    rc = rows_codes(run, ids) if completed else []
    v['V1_codes'] += rc
    v1 = v1 and not rc
    if run.get('pass_rows_s9'):                                              # R6 [A54 S9] a pass row-set record defect: INVALID
        v['V1_codes'].append(run['pass_rows_s9'])
        v['V1_codes'] += list(run.get('pass_rows_s9_naming') or [])          # R11 [A79.6] the entries named by index
        v1 = False
    if not run.get('adapted_sha_equal', False):
        v1 = False
        v['V1_codes'].append('RESULT_CHANGED_DURING_READ')
    rcodes = [c for c in run.get('read_codes', []) if not c.startswith('RECEIPT_')]
    if rcodes:                                                                                  # [verify N3] loud, invalid
        v['V1_codes'] += rcodes
        v1 = False
    fin = run.get('finish')
    if not isinstance(fin, dict):
        v['V1_codes'].append('FINISH_JSON_ABSENT_OR_UNREADABLE')
        v1 = False
    elif fin.get('result_sha256') != run['result_sha256']:
        v['V1_codes'].append('FINISH_RESULT_SHA_MISMATCH')
        v1 = False
    rcp = receipt_codes(run)
    if rcp:
        v['V1_codes'] += rcp
        v1 = False
    if run.get('failure'):
        v['V1_codes'] += run['failure']['codes']
        v['reading'] = run['failure']['class']
        v['misses'] = run['failure']['misses']
    v['V1'] = bool(v1)
    # ---- V2 [V005 V2]
    if completed:                                                                                 # [A50 N4] member bound
        v['V2'], c2 = v2_check(run, ctx, RPAIR_PICARD['speed_change_bound_km_s'] if (rpair and rpair['branch'] == 'PICARD') else None)
        v['V2_codes'] = c2
    else:
        v['V2'] = None                                                                            # no final pass to read
    # ---- V3 [V005 V3] against the registered V007 case block
    ns = _normalized(run) or run.get('spec_for_reading') or {}
    if not _normalized(run):
        v['notes'].append('normalized_spec absent from result.json; V3 read from %s' % run.get('spec_source'))
    num = ns.get('numerics') or {}
    m = v['V3_mismatch']
    anc = ctx['anchor']
    if ns.get('galaxy') != anc['galaxy']:
        m.append('galaxy')
    if canon(ns.get('physical')) != canon(anc['physical']):
        m.append('physical')
    if canon(ns.get('coefficients')) != canon(anc['coefficients']):
        m.append('coefficients')
    pc = num.get('picard') or {}
    want_pc = RPAIR_PICARD if (rpair and rpair['branch'] == 'PICARD') else {
        'passes': anc['picard']['passes'], 'speed_change_bound_km_s': anc['picard']['speed_change_bound_km_s'],
        'observe_every_pass': anc['picard']['observe_every_pass']}
    for k, w in want_pc.items():
        if pc.get(k) != w:
            m.append('picard.%s' % k)
    if canon(num.get('brackets')) != canon(ctx['ra4_block']):                                         # [RA4]
        m.append('brackets_not_RA4_block')
    if num.get('composite_grid_spec') != ctx['grids'][EXPECTED_GRID[base]]:
        m.append('grid')
    tr = num.get('truncation') or {}
    et = EXPECTED_TRUNCATION[base]
    if not (tr.get('shape') == et['shape'] and tr.get('kmax_inverse_kpc') == et['kmax_inverse_kpc']):
        m.append('truncation')
    ra = num.get('route_a') or {}
    if ra.get('max_iterations') != ROUTE_A_MAX_ITERATIONS:                                            # [A47 I5]
        m.append('route_a.max_iterations!=32')
    want_cw = (RPAIR_PICARD_COLUMN_WORKERS if picard_member                                    # [A53] the Picard leaf (planning only)
               else C5H_ROUTE_A['column_workers'] if base == C5H else ROUTE_A_MODES[ctx['route_a_mode']]['t_case_column_workers'])
    if ra.get('column_workers') != want_cw:                                                           # [A47 I4]
        m.append('route_a.column_workers!=%d (route-A mode %s)' % (want_cw, ctx['route_a_mode']))
    drv = r.get('driver_sha256')
    if drv not in reg['drivers_allowed']:
        m.append('driver_not_allowed:%s' % (drv if _hex64(drv) else 'NOT_A_SHA'))
    if base == C5H and not rpair:
        if r.get('call_spec_sha256') != PIN_C5H_SPEC[1]:                                              # [A44]
            m.append('call_spec_sha256_not_C5H_registered')
        if not ctx['c5h_admission']['admitted']:                                                       # [A50 AMB-20 restated]
            m.append('C5H_ADMISSION_AMB20:%s' % ','.join(ctx['c5h_admission']['failed']))
        ref = ctx.get('c5h_numerics_reference')                                                        # [A50 S1]
        if not isinstance(ref, dict) or canon(num) != canon(ref):
            m.append('C5H_NUMERICS_NOT_SPEC_60b46130_AS_NORMALIZED_BY_ITS_DRY_RUN')
    if c5h_member and PIN_C5H_SPEC[1] not in (extra.get('b0_spec_shas') or set()):                   # [A50 root item 11]
        m.append('C5H_RPAIR_MEMBER_NOT_ADMITTED_B0_DOES_NOT_COVER_C5H_SPEC_60b46130')
    if c5h_member:                                                                                   # [A52.3] [A53]
        fr, vr = jptr(ns, C5H_RPAIR_RO1_POINTER)
        if picard_member:
            if fr:
                m.append('C5H_RPAIR_PICARD_MEMBER_CARRIES_ROUTE_A_RO1_WORKERS_A53')
        elif not (fr and vr is True):
            m.append('C5H_RPAIR_MEMBER_LACKS_ROUTE_A_RO1_WORKERS_TRUE_A52_3')
        csha = r.get('call_spec_sha256')
        if csha not in (extra.get('b0_ext_spec_shas') or set()):
            m.append('C5H_RPAIR_MEMBER_SPEC_HAS_NO_B0_RECORD_AGAINST_V009_EXT_A52_3')
        else:                                          # [A53 r4 validity F1 option (a)] the entry carries its evidence
            ev = (extra.get('b0_ext_entries') or {}).get(csha) or {}
            carried = sorted(ptr for ptr in B0_EXT_DECLARABLE if jptr(ns, ptr)[0])
            if not _hex64(ev.get('projection_sha256')):
                m.append('C5H_RPAIR_MEMBER_B0_EXT_ENTRY_LACKS_PROJECTION_EVIDENCE_A53_F1')
            if not isinstance(ev.get('declared_differences'), list) or sorted(ev['declared_differences']) != carried:
                m.append('C5H_RPAIR_MEMBER_B0_EXT_DECLARED_DIFFERENCES_NOT_THE_CARRIED_LEAVES_A53_F1')
    exempt_ptr = set()
    if rpair and rpair['branch'] == 'PICARD':
        exempt_ptr |= set(RPAIR_PICARD_EXEMPT)
    f, val = jptr(ns, RPAIR_ROUTE_A_POINTER)                                                          # [A48 AMB-14]
    if rpair and rpair['branch'] == 'ROUTE_A':
        exempt_ptr |= {RPAIR_ROUTE_A_POINTER}
        if not f:
            m.append('FIELD_MISSING:normalized_spec:%s' % RPAIR_ROUTE_A_POINTER)
        elif val != RPAIR_ROUTE_A_FACTOR:
            m.append('rpair_route_a_seed_factor_not_0.1')
    elif f and val != SEED_FACTOR_ABSENT_EQUIVALENT:
        m.append('route_a.seed_source_rtol_factor_not_absent_or_1')
    for ptr, want in sorted(reg['normalized_spec_equal'].items()):
        if ptr in exempt_ptr:
            continue
        fnd, got = jptr(ns, ptr)
        if not fnd:
            m.append('FIELD_MISSING:normalized_spec:%s' % ptr)
        elif canon(_strip_ptrs(got, ptr, exempt_ptr)) != canon(_strip_ptrs(want, ptr, exempt_ptr)):
            m.append('registered:%s' % ptr)
    if base == 'C4T-D5':                                                       # [RA1] [A47 I4]; [A50 B1] a member: its partner
        partner = 'C5H_RPAIR_PARTNER' if rpair else 'C5H'
        if c5h_numerics is None:
            m.append('%s_NORMALIZED_NUMERICS_UNAVAILABLE' % partner)
        else:
            d5, c5, used = drop_mapped_keys(num, c5h_numerics, cb.get('key_equivalence_map'))        # [A48 AMB-13]
            v['key_equivalence_map_used'] = used
            if used and PIN_C5H_SPEC[1] not in (extra.get('b0_spec_shas') or set()):
                m.append('KEY_EQUIVALENCE_MAP_USED_WITHOUT_B0_COVERING_C5H_SPEC_60b46130')        # verify blinding G7
            ex5 = ROUTE_A_MODES[ctx['route_a_mode']]['c4td5_exempt'] + (
                (C5H_RPAIR_RO1_LEAF,) if (rpair and not picard_member) else ())       # [A52.3]; [A53] PICARD: neither carries it
            eq, diff = numerics_equal_except(d5, c5, ex5)
            if not eq:
                m.append('numerics_not_byte_equal_to_%s:%s' % (partner, diff_paths_code(diff, ctx)))    # [R3 validity F4]
    if rpair:                       # [A50 B1] each member against its base run: only the registered R-PAIR leaves may differ
        b = rpair.get('base_run') or {}
        bnum = ((_normalized(b) or b.get('spec_for_reading') or {}).get('numerics')
                if b.get('present') and not b.get('unreadable') else None)
        if not isinstance(bnum, dict):
            m.append('RPAIR_BASE_RUN_NUMERICS_UNAVAILABLE')
        else:
            mn, bn, used_b = drop_mapped_keys(num, bnum, cb.get('key_equivalence_map')) if c5h_member else (num, bnum, [])
            eq, diff = numerics_equal_except(mn, bn, tuple(RPAIR_NUMERICS_LEAVES.get(rpair['branch'], ()))
                                             + ((C5H_RPAIR_RO1_LEAF,) if (c5h_member and not picard_member) else ()))   # [A52.3]
            if not eq:
                m.append('RPAIR_MEMBER_NUMERICS_DIFFER_FROM_BASE_OUTSIDE_RPAIR_LEAVES:%s' % diff_paths_code(diff, ctx))
            v['key_equivalence_map_used_vs_base'] = used_b
        if rpair['branch'] == 'ROUTE_A':     # [R4 order N-c] a ROUTE_A member recomputes route A (seed source_rtol/10): its
            mid = a.get('route_a_identity_sha256')    # route-A identity is its own, never the base's (stricter; DECLARED)
            bid = (b.get('adapted') or {}).get('route_a_identity_sha256') if b.get('present') else None
            if not _hex64(mid):
                m.append('RPAIR_ROUTE_A_MEMBER_ROUTE_A_IDENTITY_NOT_A_SHA')
            elif mid == bid:
                m.append('RPAIR_ROUTE_A_MEMBER_ADMITS_THE_BASE_ROUTE_A_IDENTITY_NOT_RECOMPUTED')
    # ---- route-A outcome (accepted iteration reported, A47 I5); tail record; RO1 record
    rao = run.get('route_a_outcome')
    v['accepted_route_a_iteration'] = None
    if not isinstance(rao, dict):
        m.append('FIELD_MISSING:result:route_a_outcome')
    else:
        if rao.get('classification') != 'CONVERGED':
            m.append('route_a_outcome.classification!=CONVERGED')
        it = rao.get('converged_iteration')
        if KINDS['int'](it):
            v['accepted_route_a_iteration'] = it
        else:
            m.append('FIELD_MISSING:result:route_a_outcome/converged_iteration')
    v['uvt'] = {'required': bool(reg.get('tail')), 'present': False, 'flagged': None, 'E_A_row_order': None}
    if reg.get('tail'):
        if run.get('uvt_record') is None:
            m.append(run.get('uvt_code') or 'FIELD_MISSING:route_a_attempt_result:result/uv_tail')
        else:
            c, info = check_uvt_record(run['uvt_record'], reg, 'route_a_attempt_result:result/uv_tail', ctx.get('row_radii_m'))
            m += c
            v['uvt'].update(present=True, flagged=info['flagged'], E_A_row_order=info['E_A_row_order'])
            v['_uvt_info'] = info
            if info['accepted_iteration'] is not None and v['accepted_route_a_iteration'] is not None \
                    and info['accepted_iteration'] != v['accepted_route_a_iteration']:
                m.append('UVT_ACCEPTED_ITERATION_MISMATCH')
    v['ro1'] = {'required': bool(reg.get('ro1_required')), 'present': False, 'fired': None, 'armed': None, 'events': []}
    if reg.get('ro1_required'):
        c, info = check_ro1_record(rao, nodes=registered_source_rule_is_nodes(reg))                    # [R4 validity F1]
        v['ro1']['custody_list'] = 'NODES' if registered_source_rule_is_nodes(reg) else 'CONTINUUM'
        m += c
        v['ro1'].update(present=info['present'], fired=info['fired'], armed=info['armed'], events=info['events'])
        cw = ra.get('column_workers')
        if picard_member:            # [A53 R3-4] a T-case Picard member carries the ADMITTED (base) attempt's RO1 record: it must
            b_ = rpair.get('base_run') or {}                       # equal the base's canonically, and its worker kind is that
            brao = b_.get('route_a_outcome') if isinstance(b_.get('route_a_outcome'), dict) else {}     # attempt's (the base's
            bro1 = brao.get('ro1')                                                                     # column_workers), not the
            if not isinstance(bro1, dict) or canon(rao.get('ro1') if isinstance(rao, dict) else None) != canon(bro1):   # member's
                m.append('RPAIR_PICARD_MEMBER_RO1_RECORD_NOT_THE_BASE_RECORD_A53_R3_4')                  # planning-only 1
            bns = (_normalized(b_) or b_.get('spec_for_reading') or {}) if b_.get('present') else {}
            cw = ((bns.get('numerics') or {}).get('route_a') or {}).get('column_workers')
            v['ro1']['worker_kind_from'] = 'ADMITTED_BASE_ATTEMPT_A53_R3_4'
        if info.get('worker_kind') and KINDS['int'](cw) and cw >= 1:                                # [A50 root item 11/12]
            want_kind = 'serial' if cw == 1 else 'parallel'                       # R11 (Codex2 BR-B2): a POSITIVE admitted count
            if info['worker_kind'] != want_kind:
                m.append('RO1_WORKER_IS_NOT_THE_%s_CUSTODY_WORKER_FOR_THE_COLUMN_WORKERS' % want_kind.upper())
        elif info.get('worker_kind') and picard_member:
            m.append('RO1_KIND_CHECK_BASE_COLUMN_WORKERS_UNREADABLE')
        elif info.get('worker_kind'):                                   # R11 [A77.2] the admitted attempt's count unreadable or < 1
            m.append('RO1_KIND_CHECK_COLUMN_WORKERS_NOT_A_POSITIVE_INT_A77_2')
    elif c5h_member and picard_member:   # [A53] the C5H Picard member admits the v009-EXT route A (no RO1): block required, unarmed
        c, info = check_ro1_record(rao, require_armed=False)                                      # and not fired (as B0prime_RERUN)
        m += c
        if info.get('armed') is True or info.get('fired') is True:
            m.append('RO1_C5H_PICARD_MEMBER_MUST_BE_UNARMED_AND_NOT_FIRED_A53')
        v['ro1'].update(present=info['present'], fired=info['fired'], armed=info['armed'], rule='A53_C5H_PICARD_MEMBER_UNARMED')
    elif isinstance(rao, dict) and 'ro1' in rao:                                                  # [A49.2] non-RO1 worker
        c, info = check_ro1_record(rao, require_armed=False)
        m += c
        if info['armed'] or info['fired']:
            m.append('RO1_BLOCK_ON_A_NON_RO1_CASE_MUST_BE_UNARMED_AND_NOT_FIRED')
        v['ro1'].update(present=info['present'], fired=info['fired'], armed=info['armed'])
        if info['fired']:
            v['notes'].append('RO1 fired: recorded, not an invalidity (RA5); route-A circular-trial rows diagnostic only')
    v['V3_mismatch'] = m = list(dict.fromkeys(m))                                                    # de-duplicated, ordered
    v['V3'] = not m
    # ---- V4/V5 [V005 V4 V5] final field packet (only a COMPLETED call has one: verify M10)
    if completed:
        pk = packet or {}
        v['V4'] = bool(pk.get('V4'))
        v['V5'] = bool(pk.get('V5'))
        if pk.get('reason'):
            v['notes'].append('packet: %s' % pk['reason'])
    else:
        v['V4'] = v['V5'] = None
        v['notes'].append('V4/V5 not evaluated: the call produced no final field packet')
    # ---- V6 [V005 V6]: only R-PAIR Picard-branch members admit a prefix: [A53] their BASE's route A
    if picard_member:
        b = rpair['base_run']
        v6 = []
        bad_base = not (b.get('present') and b.get('adapted') and not b.get('unreadable'))
        if bad_base:
            v6.append('V6_BASE_RUN_UNAVAILABLE')
        else:
            if not (_hex64(a.get('route_a_identity_sha256')) and a['route_a_identity_sha256'] == b['adapted'].get('route_a_identity_sha256')):
                v6.append('V6_ROUTE_A_IDENTITY_NOT_THE_BASE_IDENTITY')
            mrs = (rao or {}).get('result_sha256') if isinstance(rao, dict) else None
            brs = (b.get('route_a_outcome') or {}).get('result_sha256') if isinstance(b.get('route_a_outcome'), dict) else None
            if not (_hex64(mrs) and mrs == brs):                                                        # [A53] (R3-2, order N1)
                v6.append('V6_ROUTE_A_OUTCOME_RESULT_SHA256_NOT_THE_BASE_A53')
            if not c5h_member and r.get('driver_sha256') != (b.get('result') or {}).get('driver_sha256'):
                v6.append('V6_DRIVER_NOT_THE_BASE_DRIVER')
            if reg.get('tail') and canon(run.get('uvt_record')) != canon(b.get('uvt_record')):           # same attempt, same record
                v6.append('V6_ROUTE_A_TAIL_RECORD_NOT_THE_BASE_RECORD')
        v['V6'] = not v6
        v['V6_codes'] = v6
        if c5h_member:                                                                                  # [A50 root item 11]
            v['notes'].append('V6: C5H R-PAIR member runs v010 tail OFF (root item 11), so driver equality with the v009-EXT base '
                              'is not required; the admitted route-A identity and result sha must equal the base (A53)')

    # ---- I1-T [R1 I1T]: gate status PASS (verify D1) and this build covered and PASS (R-PAIR builds too: verify D5)
    if reg.get('tail'):
        gst = (i1t or {}).get('status')
        per = (i1t or {}).get('per')
        st = per.get(label, 'UNCOVERED') if isinstance(per, dict) else None
        v['I1T'] = gst == 'PASS' and st == 'PASS'
        if gst != 'PASS':
            v['V1_codes'].append('I1T_GATE_%s' % (gst or 'NOT_EVALUATED'))
        if st != 'PASS':
            v['V1_codes'].append('I1T_%s' % (st or 'NOT_EVALUATED'))
    gates = ('V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'I1T')
    v['failed'] = [k for k in gates if k in v and v[k] is False]
    v['valid_all'] = not v['failed']
    if not v['valid_all'] and v['reading'] is None:
        v['reading'] = 'INVALID:%s' % ','.join(v['failed'])
    return v


def next_steps_for_case(v, ctx):
    """[A47 I1] [A48 AMB-16] the next step of each failed gate: BRACKET_HULL_MISS -> its own registration (RA4); any other
    V1-V6 failure -> named defect, fix and rerun that case under V007 with thresholds unchanged."""
    out = {}
    for g in v['failed']:
        if g == 'missing':
            out[g] = 'Run the registered case (V007 case block).'
        elif g == 'unregistered':
            out[g] = 'Register the case in the V007 case block before the seal.'
        elif g == 'ALIAS':
            out[g] = 'Two registered labels name one result (verify D4): run each registered case as its own call.'
        elif g == 'V1' and v.get('reading') == 'BRACKET_HULL_MISS':
            out[g] = RA4_NEXT
        elif g == 'I1T':
            out[g] = 'I1-T (UV_TAIL_SOURCE_MISMATCH) coverage/failure: review the tail source roster of that case; no T reading'
        else:
            codes = (v.get('V1_codes') if g == 'V1' else v.get('V3_mismatch') if g == 'V3' else
                     v.get('V2_codes') if g == 'V2' else v.get('V6_codes') if g == 'V6' else []) or [g]
            out[g] = AMB16_NEXT % ('%s %s' % (g, ','.join(str(c) for c in codes[:6])))
    return out


IDENTITY_DRIVER_CODE = 'IDENTITY_RUN_DRIVER_NOT_V010_R5_A67_N1'


def identity_driver_code():
    """R10 [A72] the N1 code names the active build: r5 keeps the r8 code; r6 reads IDENTITY_RUN_DRIVER_NOT_V010_R6_A67_N1_A72."""
    b = active_build()['build']
    return IDENTITY_DRIVER_CODE if b == 'r5' else 'IDENTITY_RUN_DRIVER_NOT_V010_%s_A67_N1_A72' % b.upper()


def identity_driver_codes(run):
    """R8 [A67 N1] (r7 recheck validity N1; defence in depth for A55.3): every identity run (Z2, Z2-OFF, B0prime_RERUN) carries
    result driver_sha256 = the v010 r5 sha (PIN_DRIVER_V010_R5; the receipt driver pin must equal it too, receipt_codes).
    R10 [A72 ruling 3]: the sealed driver of the active build (r5, or r6 when adopted: the identity runs are then rerun on r6)."""
    drv = (run.get('result') or {}).get('driver_sha256')
    return [] if drv == sealed_driver_sha() else [identity_driver_code()]


def identity_run_validity(name, run, ctx=None):
    """[A47 I1] identity-gate run (Z2, Z2-OFF, B0prime_RERUN): COMPLETED, valid, exactly the 12 registered row ids (verify D2)
    with finite speeds, finish and receipt custody (A48 AMB-26); RO1 must not fire [RA5 (a)].  [A50 root item 12] the RO1
    workers run armed: ro1.armed true (fired false), worker and binding on the declared custody list.  Never raises."""
    v = {'run': name, 'present': bool(run.get('present')), 'codes': [], 'ro1_fired': None, 'ro1_codes': []}
    if not run.get('present'):
        v.update(valid=False, codes=['MISSING:%s' % run.get('absent')])
        return v
    if run.get('unreadable'):
        v.update(valid=False, codes=[run['unreadable']] + list(run.get('unreadable_detail') or []))
        return v
    try:
        a = run['adapted']
        ids = (ctx or {}).get('ids') or sorted(a.get('rows') or {})
        ok = a['status'] == 'COMPLETED' and a['valid'] is True
        rc = rows_codes(run, ids)
        v['codes'] += rc
        if run.get('pass_rows_s9'):                                          # R6 [A54 S9] (identity runs too: stricter, DECLARED)
            v['codes'].append(run['pass_rows_s9'])
            v['codes'] += list(run.get('pass_rows_s9_naming') or [])         # R11 [A79.6]
        fin = run.get('finish')
        if not isinstance(fin, dict) or fin.get('result_sha256') != run['result_sha256']:
            v['codes'].append('FINISH_RESULT_SHA_MISMATCH_OR_ABSENT')
        v['codes'] += receipt_codes(run)
        v['codes'] += identity_driver_codes(run)                            # R8 [A67 N1]
        v['codes'] += [c for c in run.get('read_codes', []) if not c.startswith('RECEIPT_')]
        if run.get('failure'):
            v['codes'] += run['failure']['codes']
        rao = run.get('route_a_outcome')
        if name == 'B0prime_RERUN':                    # [A52.1] exempt from item 12: ro1 block required, armed false, fired false
            c, info = check_ro1_record(rao, require_armed=False)
            if info.get('armed') is True:
                c = c + ['RO1_B0PRIME_RERUN_MUST_BE_UNARMED_A52_1']
            v['ro1_item12'] = B0PRIME_RERUN_RO1_RULE
        else:
            c, info = check_ro1_record(rao, require_armed=True)                                     # [A50 root item 12]
            v['ro1_item12'] = 'A50_ITEM_12_ARMED_TRUE_FIRED_FALSE'
        if info.get('worker_kind'):                    # [R3 order N8] the NEW-4 worker-kind check applies to identity runs too
            ns = (run.get('result') or {}).get('normalized_spec') or run.get('spec_for_reading') or {}
            num = ns.get('numerics') if isinstance(ns, dict) else None
            # the driver's own rule (v010 L837): route_a.column_workers absent -> 1 (route_a is normalized only when declared)
            cw = ((num.get('route_a') or {}).get('column_workers', 1)) if isinstance(num, dict) else None
            if not (KINDS['int'](cw) and cw >= 1):                      # R11 (Codex2 BR-B2): 0 / -1 are not a parallel count
                c.append('RO1_KIND_CHECK_COLUMN_WORKERS_UNREADABLE')
            elif info['worker_kind'] != ('serial' if cw == 1 else 'parallel'):
                c.append('RO1_WORKER_IS_NOT_THE_%s_CUSTODY_WORKER_FOR_THE_COLUMN_WORKERS' % ('SERIAL' if cw == 1 else 'PARALLEL'))
        if info.get('fired') is True:                  # [A53 r4 validity F3] named in --gates-only too (RA5 (a): NO_RUN)
            c = c + ['RO1_FIRED_IN_IDENTITY_RUN']
        v['ro1_fired'] = info['fired']
        v['ro1_armed'] = info['armed']
        v['ro1_codes'] = c
        v['valid'] = bool(ok and not v['codes'] and not c)                                           # [R3 validity F3]
    except Exception as exc:
        v.update(valid=False, codes=v['codes'] + ['IDENTITY_VALIDITY_EXCEPTION:%s' % type(exc).__name__])
    return v


# ============================================================================================ gate records
def _tau12(ctx):
    return [ctx['tau'][i] for i in ctx['ids']]


def _shells(rec, path, where, value_key, read):
    """{(lo, hi): value} of a shell list.  R10 [A71] (Codex2 0441 / 0442 CX2-R8-B1: r8 kept the LAST of two entries for one range,
    so a failing [4, 5] shell followed by a passing duplicate read PASS): every raw entry is read and type-checked first, and a
    range given twice raises DuplicateEntry naming both entries (the gate reads RECORD_DEFECT) before the mapping is built."""
    raw = []
    for j, s in enumerate(need(rec, path, where, 'nonempty_list', read)):
        w = '%s:%s[%d]' % (where, path, j)
        rg = need(s, 'range_inverse_kpc', w, 'range2')
        raw.append(((float(rg[0]), float(rg[1])), need(s, value_key, w, 'num>=0')))
    return unique_map(raw, where, path)


# Gate functions return codes; a code starting 'DEFECT:' means the gate was not established as specified (wrong state,
# reference, configuration or coverage of the record) and turns the gate RECORD_DEFECT (-> NO_RUN, AMB-02); any other code
# is a FAIL of an established gate.
def _spec_sets(rec, gate, read, evidence=None):
    """spec_sets/{EXT,GEO,NGC}[].{label, sha256}.  [A53 r4 validity F1 option (a)] an EXT entry may carry the evidence of a C5H
    R-PAIR member spec: projection_sha256 (sha) and declared_differences (list of /numerics pointers in B0_EXT_DECLARABLE);
    present-but-malformed evidence is a loud field defect.  evidence: a dict filled {sha256: {projection_sha256, declared_differences}}."""
    out = {}
    for k in ('EXT', 'GEO', 'NGC'):
        out[k] = []
        for j, x in enumerate(need(rec, 'spec_sets/' + k, gate, 'nonempty_list', read)):
            w = '%s:spec_sets/%s[%d]' % (gate, k, j)
            need(x, 'label', w, 'str')
            sh = need(x, 'sha256', w, 'sha')
            out[k].append(sh)
        # R10 [A71] (Claude3 helper I item 3): a spec sha listed twice in one set (r8: the EXT evidence of the last entry won)
        dup = unique_keys_codes(out[k], gate, 'spec_sets/%s' % k)
        if dup:
            raise DuplicateEntry(dup)
        for j, x in enumerate(need(rec, 'spec_sets/' + k, gate, 'nonempty_list', [])):
            w = '%s:spec_sets/%s[%d]' % (gate, k, j)
            if k == 'EXT' and evidence is not None and ('projection_sha256' in x or 'declared_differences' in x):
                ps = need(x, 'projection_sha256', w, 'sha')
                dd = need(x, 'declared_differences', w, 'list')
                if not all(isinstance(y, str) and y in B0_EXT_DECLARABLE for y in dd):
                    raise FieldMissing(w, 'declared_differences', 'UNREGISTERED_VALUE')
                dup = unique_keys_codes(dd, gate, 'spec_sets/EXT[%d]/declared_differences' % j)   # R11 [A79.6] C10: both named
                if dup:
                    raise DuplicateEntry(dup)
                evidence[x['sha256']] = {'projection_sha256': ps, 'declared_differences': list(dd)}
    return out


def g_B0(rec, ctx, xr, read):
    fails = []
    need(rec, 'maps/EXT', 'B0', 'dict', read)
    need(rec, 'maps/GEO', 'B0', 'dict', read)
    ev = {}
    sets = _spec_sets(rec, 'B0', read, evidence=ev)
    xr('_b0_ext_entries', ev, None)                                                                  # [A53 r4 validity F1 (a)]
    geo = sets['GEO']
    xr('_b0_spec_shas', sorted({x for v in sets.values() for x in v}), None)                       # [A48 AMB-13] (G7)
    xr('_b0_ext_spec_shas', sorted(set(sets['EXT'])), None)                                        # [A52.3] against v009-EXT
    for pre in ('2029f26a', '4ac5527a'):
        if not any(s.startswith(pre) for s in geo):
            fails.append('DEFECT:B0_GEO_SET_LACKS_%s' % pre)
    return fails


def g_B0prime_DRY(rec, ctx, xr, read):
    fc = need(rec, 'files_compared', 'B0prime_DRY', 'nonempty_list', read)
    dup = unique_keys_codes([canon(x) for x in fc], 'B0prime_DRY', 'files_compared')   # R10 [A71 B05]
    if dup:
        raise DuplicateEntry(dup)
    _spec_sets(rec, 'B0prime_DRY', read)
    return [] if {'DRYRUN_REPORT.json', 'DRYRUN_PLAN.txt'} <= set(fc) else ['DEFECT:B0prime_DRY_FILES']


def identity_comparator_codes(rec, gate, ctx, read):
    """R7 [A57.3] [A59] (r6 recheck validity SF4 (b)): an identity-gate record (B1, B1_OFF, B0prime_RERUN) names the comparator
    and the token set it was built with, comparator/{path, sha256} and tokens/{path, sha256}; both shas must be ROOT-REGISTERED
    (the producer registry: identity_comparators, identity_tokens[gate]; A57.3 comparator c2v004 or its r5 pin-swap successor,
    A59 the Z2 token set REPLACING the base mapping).  Unregistered: a RECORD_DEFECT.  With no registry at all, evaluate_gate
    already makes the record a RECORD_DEFECT (PRODUCER_REGISTRY_ABSENT_A62_2)."""
    cp = need(rec, 'comparator/path', gate, 'str', read)
    cs = need(rec, 'comparator/sha256', gate, 'sha', read)
    tp = need(rec, 'tokens/path', gate, 'str', read)
    ts = need(rec, 'tokens/sha256', gate, 'sha', read)
    reg = (ctx or {}).get('producer_registry')
    if reg is None:
        return []
    out = []
    # R10 [A69 note 1, applied to the identity comparator and token files too: stricter] path and sha registered, bytes hashed
    out += ['DEFECT:' + c for c in file_pin_codes(cp, cs, reg['identity_comparators'], (
        '%s_COMPARATOR_NOT_ROOT_REGISTERED_A57_3' % gate, gate, '%s_COMPARATOR_PATH_NOT_ROOT_REGISTERED_A69_1' % gate,
        '%s_COMPARATOR_BYTES_NOT_THE_REGISTERED_SHA_A69_1' % gate))]
    out += ['DEFECT:' + c for c in file_pin_codes(tp, ts, reg['identity_tokens'].get(gate, frozenset()), (
        '%s_TOKENS_NOT_ROOT_REGISTERED_A59' % gate, gate, '%s_TOKENS_PATH_NOT_ROOT_REGISTERED_A69_1' % gate,
        '%s_TOKENS_BYTES_NOT_THE_REGISTERED_SHA_A69_1' % gate))]
    return [c.rsplit(':', 1)[0] if c.endswith(':' + gate) else c for c in out]


def g_B0prime_RERUN(rec, ctx, xr, read):
    fails = identity_comparator_codes(rec, 'B0prime_RERUN', ctx, read)                               # R7 [A57.3] [A59]
    xr('run_result_sha256', need(rec, 'run_result_sha256', 'B0prime_RERUN', 'sha', read), 'B0prime_RERUN')
    if need(rec, 'reference_result_sha256', 'B0prime_RERUN', 'sha', read) != GEO_DECIDING_I_RESULT_SHA256:
        fails.append('DEFECT:B0prime_RERUN_REFERENCE_NOT_GEO_DECIDING_I')
    if need(rec, 'call_spec_sha256', 'B0prime_RERUN', 'sha', read) != B0PRIME_RERUN_SPEC_SHA256:
        fails.append('DEFECT:B0prime_RERUN_SPEC_NOT_4ac5527a')
    need(rec, 'declared_exceptions', 'B0prime_RERUN', 'list', read)
    if need(rec, 'differences_outside_declared', 'B0prime_RERUN', 'list', read):
        fails.append('B0prime_RERUN_UNDECLARED_DIFFERENCES')
    if need(rec, 'tail', 'B0prime_RERUN', 'str', read) != 'OFF':
        fails.append('DEFECT:B0prime_RERUN_TAIL_NOT_OFF')
    return fails


def g_B0_FA(rec, ctx, xr, read):
    fails = []
    for c in ('A1', 'A2', 'A4'):
        if need(rec, 'cases/%s/status' % c, 'B0_FA', 'str', read) != 'REFUSED' or \
                need(rec, 'cases/%s/code' % c, 'B0_FA', 'str', read) != 'ROUTE_A_CHECKPOINT_MISSING':
            fails.append('B0_FA_%s_NOT_REFUSED_CHECKPOINT_MISSING' % c)
    return fails


def _g_B1(rec, gate, run, tail, read, xr, ctx=None):
    fails = identity_comparator_codes(rec, gate, ctx, read)                                          # R7 [A57.3] [A59]
    xr('run_result_sha256', need(rec, 'run_result_sha256', gate, 'sha', read), run)
    if need(rec, 'reference_result_sha256', gate, 'sha', read) != Z2_REFERENCE_RESULT_SHA256:
        fails.append('DEFECT:%s_REFERENCE_NOT_883b37a0' % gate)
    if need(rec, 'tail', gate, 'str', read) != tail:
        fails.append('DEFECT:%s_TAIL_MODE' % gate)
    if need(rec, 'differences_outside_custody', gate, 'list', read):
        fails.append('%s_DIFFERENCES_OUTSIDE_CUSTODY' % gate)
    need(rec, 'declared_exceptions', gate, 'list', read)
    if tail == 'ON' and need(rec, 'outer_K_big_equals_K', gate, 'bool', read) is not True:
        fails.append('DEFECT:B1_DOMAIN_NOT_EMPTY')
    if tail == 'ON':
        if need(rec, 'precondition_L/verdict', gate, 'str', read) != 'PASS_BITWISE_EQUAL' or \
                need(rec, 'precondition_L/reference_result_sha256', gate, 'sha', read) != PRECONDITION_L_REFERENCE_SHA256:
            fails.append('B1_PRECONDITION_L_NOT_PASS')
    return fails


def g_B1(rec, ctx, xr, read):
    return _g_B1(rec, 'B1', 'Z2', 'ON', read, xr, ctx)


def g_B1_OFF(rec, ctx, xr, read):                                                                     # [A47 I6]
    return _g_B1(rec, 'B1_OFF', 'Z2-OFF', 'OFF', read, xr, ctx)


def g_B2(rec, ctx, xr, read):
    fails = []
    if need(rec, 'O_cube_K_out_inverse_kpc', 'B2', 'num', read) != 12 or need(rec, 'azimuths', 'B2', 'int', read) != 16:
        fails.append('DEFECT:B2_CONFIGURATION')
    for s in ('C2R3', 'C3R3', 'C4R3'):
        if need(rec, 'per_state/%s/state_result_sha256' % s, 'B2', 'sha', read) != PIN_R3[s][1]:
            fails.append('DEFECT:B2_%s_STATE_SHA' % s)
        if need(rec, 'per_state/%s/max_row_diff_km_s' % s, 'B2', 'num>=0', read) > 1e-4:
            fails.append('B2_%s_ROWS_GT_1e-4' % s)
        if need(rec, 'per_state/%s/sanity_vs_KB12_km_s' % s, 'B2', 'num>=0', read) > 0.05:
            fails.append('B2_%s_SANITY_GT_0.05' % s)
    return fails


B3_TOL = (('value_rel', '<=', 1e-8), ('gradient_rel', '<=', 1e-7), ('hessian_rel', '<=', 1e-6), ('lapse_pair_rel', '<=', 1e-8),
          ('bd_z0_max_abs', '==', 0.0), ('facade_midplane_ratio_max_abs', '==', 0.0), ('angular_reads_rel', '<=', 1e-7),
          ('column_potential_rel', '<=', 1e-7), ('imag_max_abs', '==', 0.0), ('doubling_rel', '<=', 1e-10))


def g_B3(rec, ctx, xr, read):
    fails = []
    if need(rec, 'independent_lane', 'B3', 'str', read) not in ('Claude3', 'Claude4'):
        fails.append('DEFECT:B3_NOT_INDEPENDENT_LANE')
    if need(rec, 'imports_tail_library', 'B3', 'bool', read) is not False:
        fails.append('DEFECT:B3_IMPORTS_TAIL_LIBRARY')
    if need(rec, 'state_result_sha256', 'B3', 'sha', read) != PIN_R3['C4R3'][1]:
        fails.append('DEFECT:B3_STATE_NOT_C4R3')
    for case in ('cube_O8', 'cylinder_O8'):                                                            # [R1 L4] cylinder-O
        for k, op, t in B3_TOL:
            x = need(rec, 'cases/%s/%s' % (case, k), 'B3', 'num>=0', read)
            if (op == '<=' and x > t) or (op == '==' and x != t):
                fails.append('B3_%s_%s' % (case, k))
        if need(rec, 'cases/%s/hi_v003_L67_pass' % case, 'B3', 'bool', read) is not True:
            fails.append('B3_%s_HI_L67' % case)
    return fails


def g_B0_RO1(rec, ctx, xr, read):                                                                     # [RA5]
    fails = []
    for run in IDENTITY_RUNS:
        xr('part_a/identity_runs/%s/result_sha256' % run,
           need(rec, 'part_a/identity_runs/%s/result_sha256' % run, 'B0_RO1', 'sha', read), run)
        if need(rec, 'part_a/identity_runs/%s/ro1_fired' % run, 'B0_RO1', 'bool', read) is not False:
            fails.append('B0_RO1_a_FIRED_IN_%s' % run)
    need(rec, 'part_b/checkpoint_source', 'B0_RO1', 'str', read)
    if need(rec, 'part_b/recorded_code', 'B0_RO1', 'str', read) != RO1_CODE or \
            need(rec, 'part_b/query', 'B0_RO1', 'int', read) != 3 or \
            need(rec, 'part_b/handed_to_route_b', 'B0_RO1', 'bool', read) is not True:
        fails.append('B0_RO1_b_REPLAY')
    kinds = set()
    pc_ = need(rec, 'part_c/cases', 'B0_RO1', 'nonempty_list', read)
    # R10 [A71 B03] one case listed twice.  R11 [A79.1] (Codex2 0454; helper I B03s): keyed on the SEMANTIC identity, the case kind
    # (r10 compared whole objects, so the same kind with one extra evidence field read PASS)
    dup = unique_keys_codes([need(c, 'kind', 'B0_RO1:part_c/cases[%d]' % j, 'str') for j, c in enumerate(pc_)], 'B0_RO1', 'part_c/cases')
    if dup:
        raise DuplicateEntry(dup)
    for j, c in enumerate(pc_):
        w = 'B0_RO1:part_c/cases[%d]' % j
        kinds.add(need(c, 'kind', w, 'str'))
        if need(c, 'observed', w, 'str') != 'CALL_FAILED' or need(c, 'expected', w, 'str') != 'CALL_FAILED':
            fails.append('B0_RO1_c_CASE_%d' % j)
    if not {'OTHER_EXCEPTION', 'REFUSAL_BEFORE_CONVERGENCE'} <= kinds:
        fails.append('DEFECT:B0_RO1_c_KINDS')
    return fails


def g_B0_N3(rec, ctx, xr, read):                                                                      # [RA8]
    fails = []
    fs_ = need(rec, 'files_scanned', 'B0_N3', 'nonempty_list', read)
    if not all(isinstance(x, str) and x for x in fs_):
        raise FieldMissing('B0_N3', 'files_scanned[]', 'TYPE_nonempty_str')
    dup = unique_keys_codes(fs_, 'B0_N3', 'files_scanned')                           # R11 [A79.1] a scanned file listed twice
    if dup:
        raise DuplicateEntry(dup)
    cons, ckeys = need(rec, 'constructions', 'B0_N3', 'nonempty_list', read), []
    for j, c in enumerate(cons):
        w = 'B0_N3:constructions[%d]' % j
        ckeys.append((need(c, 'file', w, 'str'), need(c, 'line', w, 'int')))
        if need(c, 'guarded', w, 'bool') is not True:
            fails.append('B0_N3_UNGUARDED_%d' % j)
    # R11 [A79.1] (Codex2 0454; helper I B04s): a construction is identified by its site (file, line); one site listed twice (exactly,
    # or with another field) is a RECORD_DEFECT naming both entries (r10 guarded runtime_checks only)
    dup = unique_keys_codes(ckeys, 'B0_N3', 'constructions')
    if dup:
        raise DuplicateEntry(dup)
    rt = need(rec, 'runtime_checks', 'B0_N3', 'list', read)
    dup = unique_keys_codes([canon(x) for x in rt], 'B0_N3', 'runtime_checks')       # R10 [A71 B04]
    if dup:
        raise DuplicateEntry(dup)
    if not {'B0prime_RERUN', 'B1_OFF'} <= set(rt):
        fails.append('DEFECT:B0_N3_RUNTIME_CHECKS')
    return fails


def g_EPS(rec, ctx, xr, read):
    fails = []
    em = need(rec, 'eps_max', 'EPS', 'num>=0', read)
    xr('_eps_max', em, None)
    if not str(need(rec, 'evaluator_sha256', 'EPS', 'sha', read)).startswith(QINF_EVALUATOR_PREFIX):
        fails.append('DEFECT:EPS_EVALUATOR_NOT_f58de0dc')
    d = need(rec, 'coverage_inverse_kpc/DDO', 'EPS', 'range2', read)
    n = need(rec, 'coverage_inverse_kpc/NGC', 'EPS', 'range2', read)
    edge = coverage_edge_2P(production_kbig(ctx))                     # [A54] DDO coverage >= sqrt(2) x 2P (never below 64)
    if edge is None:
        fails.append('DEFECT:EPS_PRODUCTION_K_BIG_P_UNREADABLE_FROM_THE_CASE_BLOCK')
    elif d[0] > 2 or d[1] < edge or n[0] > 2 or n[1] < NGC_EPS_COVERAGE_EDGE_RI17:                  # R6 [A58 RI-17] NGC 46
        fails.append('EPS_COVERAGE')
    mx, mx_env, dom_violated, ranges = 0.0, None, False, []
    for j, s in enumerate(need(rec, 'shells', 'EPS', 'nonempty_list', read)):
        w = 'EPS:shells[%d]' % j
        rg = need(s, 'range_inverse_kpc', w, 'range2')
        ranges.append((float(rg[0]), float(rg[1])))
        b = need(s, 'eps_base', w, 'num>=0')
        f = need(s, 'eps_refined', w, 'num>=0')
        if need(s, 'refinements', w, 'int') >= 2 or f > 1.1 * b:          # [R1 EPS] 2 failures (stricter reading, A1d)
            fails.append('EPS_SHELL_%d_UNCERTIFIED' % j)
        mx = max(mx, f)
        if 'eps' in s:                          # R7 [A57.4] (validity SF3): the registered per-shell value, when the record has it
            mx = max(mx, need(s, 'eps', w, 'num>=0'))
        if 'eps_envelope' in s:
            ee = need(s, 'eps_envelope', w, 'num>=0')
            mx_env = ee if mx_env is None else max(mx_env, ee)
            if 'eps_actual_set' in s and ee < need(s, 'eps_actual_set', w, 'num>=0'):
                dom_violated = True
    dup = unique_keys_codes(ranges, 'EPS', 'shells')                     # R10 [A71] one shell range listed twice
    if dup:
        raise DuplicateEntry(dup)
    if em < mx:
        fails.append('DEFECT:EPS_MAX_BELOW_A_SHELL')
    if not (_union_covers(ranges, float(d[0]), float(d[1])) and _union_covers(ranges, float(n[0]), float(n[1]))):
        fails.append('DEFECT:EPS_SHELLS_DO_NOT_COVER_THE_DECLARED_COVERAGE')                   # R7 (validity SF4 (a))
    env = rec.get('envelope_bound')                                    # [A52.5] optional (OPTIONAL_GATE_FIELDS); DECLARED
    if env is not None:
        rule = need(rec, 'envelope_bound/rule', 'EPS', 'str', read)
        cov = need(rec, 'envelope_bound/coverage_max_inverse_kpc', 'EPS', 'num>=0', read)
        emax = need(rec, 'envelope_bound/eps_max_envelope_all_shells', 'EPS', 'num>=0', read)        # R7 [A57.4] the full
        dom = need(rec, 'envelope_bound/dominates_actual_every_shell', 'EPS', 'bool', read)          # envelope fields
        if mx_env is not None and emax < mx_env:
            fails.append('DEFECT:EPS_ENVELOPE_MAX_BELOW_A_SHELL_ENVELOPE_A57_4')
        if dom and (emax < em or dom_violated):
            fails.append('DEFECT:EPS_ENVELOPE_DOMINATES_FLAG_CONTRADICTS_THE_SHELLS_A57_4')
        fails += eps_duplicate_field_codes(rec, {'dominates_actual_every_shell': dom, 'eps_max_envelope_all_shells': emax}, read)
        xr('_envelope_bound', {'rule_ok': rule == EPS_ENVELOPE_RULE, 'coverage_max_inverse_kpc': cov,
                               'eps_max_envelope_all_shells': emax, 'dominates_actual_every_shell': dom}, None)
    else:
        fails += eps_duplicate_field_codes(rec, None, read)
        xr('_envelope_bound', None, None)
    return fails


# R8 [A67 N4] (r7 recheck validity N4; A54 S5): the EPS record carries the envelope flag and maximum twice, at the top level and in
# envelope_bound.  The two must agree (compared exactly); a top-level copy with no envelope_bound block is a RECORD_DEFECT too
# (DECLARED: a record asserting envelope dominance without the envelope block contradicts itself).  The top-level maximum is held
# to the same rule as the flag (DECLARED, stricter: NEW-53).
EPS_TOP_LEVEL_DUPLICATES = (('envelope_dominates_actual_every_shell', 'dominates_actual_every_shell', 'bool', 'DOMINATES_FLAG'),
                            ('eps_max_envelope_all_shells', 'eps_max_envelope_all_shells', 'num>=0', 'ENVELOPE_MAX'))


def eps_duplicate_field_codes(rec, nested, read):
    """nested: {field: value} of the envelope_bound block already read (None when the block is absent)."""
    out = []
    for top, key, kind, tag in EPS_TOP_LEVEL_DUPLICATES:
        if top not in rec:
            continue
        tv = need(rec, top, 'EPS', kind, read)
        if nested is None:
            out.append('DEFECT:EPS_TOP_LEVEL_%s_WITHOUT_ENVELOPE_BOUND_A67_N4' % tag)
        elif tv != nested[key]:                       # both read with the same kind (bool / num>=0)
            out.append('DEFECT:EPS_TOP_LEVEL_%s_DISAGREES_WITH_ENVELOPE_BOUND_A67_N4' % tag)
    return out


def g_DOUBLING(rec, ctx, xr, read):
    fails = []
    if need(rec, 'ddo_state_result_sha256', 'DOUBLING', 'sha', read) != PIN_R3['C4R3'][1]:
        fails.append('DEFECT:DOUBLING_STATE_NOT_C4R3')
    if need(rec, 'ddo_max_change_over_tau', 'DOUBLING', 'num>=0', read) > 1.0 / 20:
        fails.append('DOUBLING_DDO_GT_TAU_OVER_20')
    kb = need(rec, 'ddo_K_big_inverse_kpc', 'DOUBLING', 'nonempty_list', read)                    # R6 [A58 RI-03] DECLARED fields
    dup = unique_keys_codes([float(x) if _num(x) else canon(x) for x in kb], 'DOUBLING', 'ddo_K_big_inverse_kpc')   # R10 [A71 B06]
    if dup:
        raise DuplicateEntry(dup)
    P = production_kbig(ctx)
    if P is None:
        fails.append('DEFECT:DOUBLING_PRODUCTION_K_BIG_P_UNREADABLE_FROM_THE_CASE_BLOCK')
    elif not (all(_num(x) for x in kb) and {P, 2.0 * P} <= {float(x) for x in kb}):
        fails.append('DEFECT:DOUBLING_NOT_AT_K_BIG_P_AND_2P_RI03')
    if need(rec, 'ddo_gas_M_s', 'DOUBLING', 'int', read) != PRODUCTION_GAS_M_S_A57:
        fails.append('DEFECT:DOUBLING_GAS_M_S_NOT_THE_A57_PRODUCTION_M_S_RI03')
    fails += gas_M_s_context_codes(ctx, 'DOUBLING')                          # R10 [A68 CHK-1] bound to the registered gas.M_s
    if rec['ddo_gas_M_s'] != registered_gas_M_s(ctx):
        fails.append('DEFECT:DOUBLING_GAS_M_S_NOT_THE_REGISTERED_UV_TAIL_GAS_M_S_A68_CHK1')
    if need(rec, 'ngc_operator_sha256', 'DOUBLING', 'sha', read) != NGC_T120L_OPERATOR_SHA256:
        fails.append('DEFECT:DOUBLING_NGC_OPERATOR')
    if need(rec, 'ngc_max_change_over_theta', 'DOUBLING', 'num>=0', read) > 1.0 / 20:
        fails.append('DOUBLING_NGC_GT_THETA_OVER_20')
    return fails


GQ_REQUIRED = {'DDO_C2T': 32.0, 'DDO_C3T': 32.0, 'DDO_C4T': 64.0, 'NGC_T120L': 32.0}                  # [RA7] named rosters
# R5 [A54]: RA7's 'to 64 /kpc for C4T-K64' becomes 'to 2P for C4T-KHI' (never below 64): DDO_C4T reach = gq_ddo_edge(P)
# R7 [RA7] (r6 recheck validity SF1): RA7 certifies every roster used 'over [K, K_big]'; the R1 values 32 / 32 are the P = 32
# instance.  DDO_C2T and DDO_C3T must reach their case's REGISTERED K_big, read from the case block (A58 RI-05: P = 128), never
# below the R1 value (stricter).
GQ_REACH_FROM_CASE = {'DDO_C2T': 'C2T', 'DDO_C3T': 'C3T'}
# R7 [A57.1] (r6 recheck validity SF2): 'the GQ certificate at M_s 128 over the full DDO reach (all nodes, not only sampled
# ones)': every DDO roster carries all_nodes {max_abs_diff_over_P0 <= 1e-12, nodes >= the 4096-node sample} (DECLARED field
# names: the certificates_v003 producer emits them, all_nodes = its full_domain block); an every-k_perp bound
# all_kperp_nodes_bound_over_P0, when present on a roster or in its all_nodes, must also be <= 1e-12.
GQ_SAMPLE_NODES = 4096
GQ_THRESHOLD_OVER_P0 = 1e-12


def gq_all_nodes_count_codes(name, x, n_all, ctx, w):
    """R8 [A67 SF1] (r7 recheck validity SF1: the r7 floor `nodes >= 4096` accepted the 4096-node sample itself): a DDO roster
    names its production node set, rosters[].geometry (DECLARED field: the certificates_v003 assembler writes it, = the gq_full part
    record label), and its all_nodes/nodes must EQUAL the root-registered production count of that geometry (producer registry
    gq_all_nodes_counts).  A count equal to the 4096 sample refuses whatever the registry says.  Each violation is a RECORD_DEFECT
    (the record is not established as specified).  The geometry label is record-controlled: it never enters a code (A54 S6)."""
    out = []
    if n_all == GQ_SAMPLE_NODES:
        out.append('DEFECT:GQ_%s_ALL_NODES_COUNT_EQUALS_THE_4096_SAMPLE_A67_SF1' % name)
    geo = need(x, 'geometry', w, 'str')
    reg = (ctx or {}).get('producer_registry')
    if reg is None:
        return out
    want = reg['gq_all_nodes_counts'].get(geo)
    if want is None:
        out.append('DEFECT:GQ_%s_GEOMETRY_NOT_ROOT_REGISTERED_A67_SF1' % name)
    elif n_all != want:
        out.append('DEFECT:GQ_%s_ALL_NODES_COUNT_NOT_THE_ROOT_REGISTERED_PRODUCTION_COUNT_A67_SF1' % name)
    return out


# R10 [r8 recheck validity SF1, order N1; Claude3 P-SF1] the kept node set of each DDO roster's case (RA1 / RA2 / R1 labels: the
# kept cube K of C<K>T, the kept sphere 4 of S4T; every C4T-* variant keeps the C4T cube 4)
DDO_ROSTER_KEPT = {'C2T': ('cube', 2.0), 'C3T': ('cube', 3.0), 'C4T': ('cube', 4.0), 'C6T': ('cube', 6.0), 'S4T': ('sphere', 4.0),
                   'C4T-D5': ('cube', 4.0), 'C4T-C5c': ('cube', 4.0), 'C4T-KLO': ('cube', 4.0), 'C4T-KHI': ('cube', 4.0),
                   'C4T-A': ('cube', 4.0)}


def _int_label(x):
    return ('%d' % x) if (_num(x) and float(x).is_integer() and x > 0) else None


def gq_derived_geometry(kept, outer):
    """R10 the geometry label a DDO roster's own node set has, derived from its kept and outer blocks the way the certificates_v003
    part records name them: cube kept K + cylinder K_big -> C<K>T_KB<K_big>; sphere kept K -> S<K>T_SPHERE_KB<K_big>; cube kept K
    + cube outer K_out -> C<K>T-C<K_out>c.  None when the blocks are not of those forms (or not integral)."""
    if not (isinstance(kept, dict) and isinstance(outer, dict)):
        return None
    k = _int_label(kept.get('K_inverse_kpc'))
    if k is None or kept.get('shape') not in ('cube', 'sphere'):
        return None
    head = ('C%sT' % k) if kept['shape'] == 'cube' else ('S%sT_SPHERE' % k)
    if outer.get('shape') == 'cylinder' and set(outer) == {'shape', 'K_big_inverse_kpc'}:
        kb = _int_label(outer.get('K_big_inverse_kpc'))
        return None if kb is None else '%s_KB%s' % (head, kb)
    if outer.get('shape') == 'cube' and set(outer) == {'shape', 'K_out_inverse_kpc'} and kept['shape'] == 'cube':
        ko = _int_label(outer.get('K_out_inverse_kpc'))
        return None if ko is None else '%s-C%sc' % (head, ko)
    return None


def gq_geometry_binding_codes(name, x, kr, w):
    """R10 [r8 recheck validity SF1, order N1; Claude3 P-SF1] (A67 SF1 'the root-registered per-geometry production node counts':
    r8 looked the count up by a record-declared label tied to nothing): a DDO roster's geometry must be the label DERIVED from its
    own kept / outer node-set blocks (gq_derived_geometry), its kept block must be its roster case's kept node set
    (DDO_ROSTER_KEPT), and its k range must not reach above its outer edge (a roster cannot claim reach its node set lacks; the
    lower edge is not bound: DECLARED, the per-geometry union check reads it, and the r8 fixture's [2, K_big] form stays valid).  Each
    violation is a RECORD_DEFECT; no record string enters a code (A54 S6).  With A71 (g_GQ) each geometry is named once."""
    kept = need(x, 'kept', w, 'dict')
    outer = need(x, 'outer', w, 'dict')
    out = []
    want = gq_derived_geometry(kept, outer)
    case = name[len('DDO_'):]
    if want is None:
        out.append('DEFECT:GQ_%s_NODE_SET_BLOCKS_NOT_A_REGISTERED_FORM_R10' % name)
    elif x.get('geometry') != want:
        out.append('DEFECT:GQ_%s_GEOMETRY_NOT_THE_ROSTER_NODE_SET_R10' % name)
    if (kept.get('shape'), float(kept['K_inverse_kpc']) if _num(kept.get('K_inverse_kpc')) else None) != DDO_ROSTER_KEPT.get(case):
        out.append('DEFECT:GQ_%s_KEPT_NODE_SET_NOT_THE_ROSTER_CASE_R10' % name)
    edge = outer.get('K_big_inverse_kpc', outer.get('K_out_inverse_kpc'))
    if not (_num(edge) and kr[1] <= edge):
        out.append('DEFECT:GQ_%s_K_RANGE_ABOVE_THE_ROSTER_NODE_SET_R10' % name)
    return out


# R11 [A79.1] (Codex2 0454 / CX2-R10-BN-F1; Claude3 0070 §3, helper I A05s): the NGC roster's registered range is A48 AMB-12's
# NGC T120L over [2, 32] /kpc (GQ_GEOMETRY_DOMAIN['NGC'], GQ_REQUIRED NGC_T120L 32): ONE NGC_T120L roster (A79.1, the name is its
# semantic identity) must reach it from k <= 2; a shorter one is the A50 root item 8 coverage shortfall (NUMERICS_UNCERTIFIED, as
# r10), and a second NGC_T120L roster with another range is a RECORD_DEFECT naming both (DECLARED: the range is bound by the reach,
# not by equality, so that A50 root item 8 still reads a shortfall as a FAIL)
GQ_NGC_REGISTERED_RANGE = GQ_GEOMETRY_DOMAIN['NGC']


def registered_outer(ctx, lab):
    """R11 the registered uv_tail outer block of a T-case, read from the case block (None if unreadable)."""
    try:
        o = (ctx or {})['case_block']['cases'][lab]['normalized_spec_equal']['/numerics']['uv_tail']['outer']
    except (KeyError, TypeError):
        return None
    return o if isinstance(o, dict) else None


def gq_fixed_geometry(name, ctx, P):
    """R11 [A75.6] [A79.1] the FIXED roster -> geometry map, applied to EVERY DDO roster (required or extra):
      DDO_C2T -> C2T_KB<K_big of C2T>, DDO_C3T -> C3T_KB<K_big of C3T>, DDO_C4T -> C4T_KB<2P> (A75.6, verbatim);
      every other DDO_<case> -> the node set its case registers (DECLARED extension, NEW-71): the case's kept set (DDO_ROSTER_KEPT)
      with its registered uv_tail outer from the case block (C<K>T_KB<K_big>, S<K>T_SPHERE_KB<K_big>, C<K>T-C<K_out>c).
    The label is derived by gq_derived_geometry from registered blocks only (never from the record).  None when unreadable."""
    case = name[len('DDO_'):]
    kept = DDO_ROSTER_KEPT.get(case)
    if kept is None:
        return None
    kb = {'shape': kept[0], 'K_inverse_kpc': kept[1]}
    if name == 'DDO_C4T':
        return None if P is None else gq_derived_geometry(kb, {'shape': 'cylinder', 'K_big_inverse_kpc': 2.0 * P})
    o = registered_outer(ctx, case)
    return None if o is None else gq_derived_geometry(kb, o)


def _union_covers(intervals, lo, hi):
    """True iff the union of the closed intervals covers [lo, hi] without a gap."""
    reach = lo
    for a, b in sorted(intervals):
        if a > reach:
            break
        reach = max(reach, b)
    return bool(intervals) and min(a for a, _ in intervals) <= lo and reach >= hi


def g_GQ(rec, ctx, xr, read):                                                                          # [RA7] [A48 AMB-12]
    """Every roster: M_s vs 2 M_s at the 4096 nodes <= 1e-12 P0.  RA7's named rosters are present with their reach, AND
    per source geometry the union of the roster k-ranges covers DDO [2, 64] and NGC [2, 32] /kpc, both edges (A48 AMB-12)."""
    fails, seen, by_geo = [], {}, {g: [] for g in GQ_GEOMETRY_DOMAIN}
    edge = gq_ddo_edge(production_kbig(ctx))                                                           # [A54]
    if edge is None:
        return ['DEFECT:GQ_PRODUCTION_K_BIG_P_UNREADABLE_FROM_THE_CASE_BLOCK']
    required = dict(GQ_REQUIRED, DDO_C4T=edge)
    # R10 [A75.6] (Claude3 P-SF1): a fixed map binds each named DDO roster to its production geometry: DDO_C2T -> C2T_KB<K_big of C2T>,
    # DDO_C3T -> C3T_KB<K_big of C3T>, DDO_C4T -> C4T_KB<2P>; the named reach is met only by a roster carrying that geometry
    required_geo = {'DDO_C4T': 'C4T_KB%s' % _int_label(edge)}
    for name, lab in GQ_REACH_FROM_CASE.items():                                                      # R7 [RA7] (SF1)
        kb = registered_kbig(ctx, lab)
        if kb is None:
            return ['DEFECT:GQ_REGISTERED_K_BIG_UNREADABLE_FROM_THE_CASE_BLOCK:%s' % lab]
        required[name] = max(GQ_REQUIRED[name], kb)
        required_geo[name] = '%s_KB%s' % (lab, _int_label(kb))
    domain = dict(GQ_GEOMETRY_DOMAIN, DDO=(GQ_GEOMETRY_DOMAIN['DDO'][0], edge))
    fails += gas_M_s_context_codes(ctx, 'GQ')                                                         # R10 [A68 CHK-1]
    ms_reg = registered_gas_M_s(ctx)
    for top in ('gas_M_s_DDO', 'source_gas_M_s'):           # R10 [A68 CHK-1] a top-level DDO M_s, when present, is the registered one
        if top in rec and need(rec, top, 'GQ', 'int', read) != ms_reg:
            fails.append('DEFECT:GQ_TOP_LEVEL_%s_NOT_THE_REGISTERED_UV_TAIL_GAS_M_S_A68_CHK1' % top.upper())
    for top, want_ms in (('gas_M_s_NGC', NGC_GAS_M_S_A57),):    # R11 (r10 recheck validity note): the top-level NGC M_s, when present,
        if top in rec and need(rec, top, 'GQ', 'int', read) != want_ms:   # is the NGC registered M_s 96 (A57 ruling 1), else DEFECT
            fails.append('DEFECT:GQ_TOP_LEVEL_GAS_M_S_NGC_NOT_THE_REGISTERED_NGC_M_S_96_A57')
    P_ = production_kbig(ctx)
    name_keys, geo_keys = [], []
    for j, x in enumerate(need(rec, 'rosters', 'GQ', 'nonempty_list', read)):
        w = 'GQ:rosters[%d]' % j
        name = need(x, 'roster', w, 'str')
        if name not in GQ_ROSTER_NAMES:
            raise FieldMissing(w, 'roster', 'UNREGISTERED_VALUE')                                  # no record string in codes
        kr = need(x, 'k_range_inverse_kpc', w, 'range2')
        ms = need(x, 'M_s', w, 'int')
        if need(x, 'M_s_doubled', w, 'int') != 2 * ms or need(x, 'nodes', w, 'int') != 4096 or not kr[0] < kr[1]:
            fails.append('DEFECT:GQ_%s_SETUP' % name)
        if ms != (NGC_GAS_M_S_A57 if name == 'NGC_T120L' else PRODUCTION_GAS_M_S_A57):                  # R6 [A57 ruling 1]
            fails.append('DEFECT:GQ_%s_M_S_NOT_THE_A57_PRODUCTION_M_S' % name)
        if name != 'NGC_T120L' and ms != ms_reg:                                                       # R10 [A68 CHK-1]
            fails.append('DEFECT:GQ_%s_M_S_NOT_THE_REGISTERED_UV_TAIL_GAS_M_S_A68_CHK1' % name)
        if need(x, 'max_abs_diff_over_P0', w, 'num>=0') > GQ_THRESHOLD_OVER_P0:
            fails.append('UV_TAIL_GAS_QUADRATURE_UNCERTIFIED:%s' % name)
        geo = x.get('geometry') if name != 'NGC_T120L' else None
        name_keys.append(name)                         # R11 [A79.1] the semantic identity of a roster is its NAME (one roster per name)
        geo_keys.append(('NGC_ROSTER', j) if name == 'NGC_T120L' else ('GEOMETRY', geo if isinstance(geo, str) else ('ABSENT', j)))
        if name != 'NGC_T120L':                                                                       # R7 [A57.1] (SF2)
            n_all = need(x, 'all_nodes/nodes', w, 'int')
            if n_all < GQ_SAMPLE_NODES:
                fails.append('DEFECT:GQ_%s_ALL_NODES_COUNT_BELOW_THE_SAMPLE_A57_1' % name)
            fails += gq_all_nodes_count_codes(name, x, n_all, ctx, w)                                 # R8 [A67 SF1]
            fails += gq_geometry_binding_codes(name, x, kr, w)                                       # R10 [r8 recheck SF1]
            want_geo = gq_fixed_geometry(name, ctx, P_)                       # R11 [A75.6] [A79.1] every roster, required or extra
            if want_geo is None:
                fails.append('DEFECT:GQ_%s_FIXED_MAP_GEOMETRY_UNREADABLE_FROM_THE_CASE_BLOCK_A79_1' % name)
            elif x.get('geometry') != want_geo:
                fails.append('DEFECT:GQ_%s_GEOMETRY_NOT_THE_FIXED_MAP_GEOMETRY_A75_6_A79_1' % name)
            if need(x, 'all_nodes/max_abs_diff_over_P0', w, 'num>=0') > GQ_THRESHOLD_OVER_P0:
                fails.append('UV_TAIL_GAS_QUADRATURE_UNCERTIFIED:%s:ALL_NODES' % name)
        for src in (x, x.get('all_nodes')):
            if isinstance(src, dict) and 'all_kperp_nodes_bound_over_P0' in src and \
                    need(src, 'all_kperp_nodes_bound_over_P0', w, 'num>=0') > GQ_THRESHOLD_OVER_P0:
                fails.append('UV_TAIL_GAS_QUADRATURE_UNCERTIFIED:%s:ALL_KPERP_NODES' % name)
        # R10 [A75.1 A05] a named reach is met by ONE roster spanning from its case's kept K (NGC: 2) to the reach, carrying the
        # A75.6 geometry; never a merge of partial ones.  R11: with one roster per name (A79.1) this is that roster
        lo_req = GQ_GEOMETRY_DOMAIN['NGC'][0] if name == 'NGC_T120L' else (DDO_ROSTER_KEPT.get(name[len('DDO_'):]) or (None, -1.0))[1]
        if float(kr[0]) <= lo_req and (name not in required_geo or x.get('geometry') == required_geo[name]):
            seen[name] = max(seen.get(name, 0.0), kr[1])
        by_geo[name.split('_')[0]].append((float(kr[0]), float(kr[1])))
    # R10 [A71] one DDO geometry named by two rosters is a RECORD_DEFECT naming both rosters (r8 recheck SF1 / N1).  R11 [A79.1] (Codex2
    # 0454; helper I A05s): a roster NAME given twice is a RECORD_DEFECT naming both (r10 keyed on (name, geometry, range), so the same
    # name with another valid geometry, or NGC_T120L with another range, read PASS): the guard keys on the semantic identity
    dup = unique_keys_codes(name_keys, 'GQ', 'rosters') + [c + ':ONE_GEOMETRY' for c in unique_keys_codes(geo_keys, 'GQ', 'rosters')]
    fails += ['DEFECT:' + c for c in dup]          # named with every other defect of the record (the binding codes included)
    for name, reach in required.items():
        if seen.get(name, -1.0) < reach:
            fails.append('GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT:%s' % name)
    for geo, (lo, hi) in domain.items():
        if not _union_covers(by_geo[geo], lo, hi):
            fails.append('GQ_%s_UNION_DOES_NOT_COVER_REGISTERED_DOMAIN' % geo)
    return fails


LO_RANGES_R1 = ((4, 5), (5, 6), (6, 8), (8, 12), (12, 16), (16, 32), (32, 64))
LO_RANGES = LO_RANGES_R1 + ((64, 128), (128, 256), (256, 363))       # R6 [A58 RI-06] the registered DDO partition (P = 128)
LO_NGC_RANGES = ((2, 3), (3, 4), (4, 6), (6, 8), (8, 12), (12, 16))
# R10 [A68 'Records'] the other M_s fields an LO record may carry (LO_CERT_V003/V004 carry all three): each must equal source_gas_M_s
LO_M_S_ECHO_FIELDS = ('gas_M_s', 'tail_config_gas/M_s', 'build/roster_gas/M_s')


def _g_lo(rec, gate, ranges, unit, read):
    fails = []
    sh = _shells(rec, 'shells', gate, 'max_over_' + unit, read)
    for rg in ranges:
        x = sh.get((float(rg[0]), float(rg[1])))
        if x is None:
            fails.append('DEFECT:%s_SHELL_%s_%s_ABSENT' % (gate, rg[0], rg[1]))
        elif x > 0.005:
            fails.append('%s_SHELL_%s_%s_GT_0.005' % (gate, rg[0], rg[1]))
    if need(rec, 'summed_max_over_' + unit, gate, 'num>=0', read) > 0.05:
        fails.append('%s_SUM_GT_0.05' % gate)
    return fails


def g_LO(rec, ctx, xr, read):
    """[R1 LO] the registered shells (R6 [A58 RI-06]: the ten-shell partition (4,5] .. (256,363], each <= 0.005 tau, summed
    <= 0.05 tau, with the gas M_s 128 source: field source_gas_M_s, A57 ruling 1, DECLARED field); R5 [A54] LO coverage >= sqrt(2) x 2P: the record's shells cover [4, coverage edge]
    without a gap (else DEFECT: the certificate does not reach the registered domain; DECLARED: a shortfall is a record not
    established as specified, like an absent registered shell), and EVERY shell is <= 0.005 tau (the R1 per-shell bound applied
    to the extended shells: stricter)."""
    f = _g_lo(rec, 'LO', LO_RANGES, 'tau', read)
    if need(rec, 'state_result_sha256', 'LO', 'sha', read) != PIN_R3['C4R3'][1]:
        f.append('DEFECT:LO_STATE_NOT_C4R3')
    src = need(rec, 'source_gas_M_s', 'LO', 'int', read)
    if src != PRODUCTION_GAS_M_S_A57:                                                                  # R6 [A57 ruling 1] [RI-06]
        f.append('DEFECT:LO_SOURCE_GAS_M_S_NOT_THE_A57_PRODUCTION_M_S')
    f += gas_M_s_context_codes(ctx, 'LO')                                                              # R10 [A68 CHK-1]
    if src != registered_gas_M_s(ctx):
        f.append('DEFECT:LO_SOURCE_GAS_M_S_NOT_THE_REGISTERED_UV_TAIL_GAS_M_S_A68_CHK1')
    for p_ in LO_M_S_ECHO_FIELDS:              # R10 [A68 'Records'] every other M_s field the record carries agrees with source_gas_M_s
        fnd, val = jptr(rec, '/' + p_)
        if fnd:
            read.append(p_)
            if not KINDS['int'](val) or val != src:
                f.append('DEFECT:LO_M_S_FIELDS_DISAGREE_WITH_SOURCE_GAS_M_S_A68')
                break
    edge = coverage_edge_2P(production_kbig(ctx))
    sh = _shells(rec, 'shells', 'LO', 'max_over_tau', [])
    if any(lo_ < LO_COVERAGE_LOWER for lo_, _ in sh):                       # R10 [A69 note 2] shell coverage starts at lo >= K
        f.append('DEFECT:LO_SHELL_BELOW_K_A69_2')
    if edge is None:
        f.append('DEFECT:LO_PRODUCTION_K_BIG_P_UNREADABLE_FROM_THE_CASE_BLOCK')
    elif not _union_covers(list(sh), LO_COVERAGE_LOWER, edge):
        f.append('DEFECT:LO_COVERAGE_BELOW_SQRT2_TIMES_2P_A54')
    reg = {(float(a), float(b)) for a, b in LO_RANGES}
    for j, (rg, x) in enumerate(sorted(sh.items())):
        if rg not in reg and x > 0.005:
            f.append('LO_EXTENDED_SHELL_%d_GT_0.005' % j)
    return f


def g_LO_NGC(rec, ctx, xr, read):
    f = _g_lo(rec, 'LO_NGC', LO_NGC_RANGES, 'theta', read)
    if need(rec, 'operator_sha256', 'LO_NGC', 'sha', read) != NGC_T120L_OPERATOR_SHA256:
        f.append('DEFECT:LO_NGC_OPERATOR')
    # R11 (r10 recheck order N2: a failing [2, 3.000001] or [16, 46] shell left LO_NGC PASS): EVERY shell the record carries is held
    # to the per-shell bound, registered or not (LO's R5 rule applied to LO_NGC: stricter, DECLARED); and below K = 2 refuses
    sh = _shells(rec, 'shells', 'LO_NGC', 'max_over_theta', [])
    reg = {(float(a), float(b)) for a, b in LO_NGC_RANGES}
    for j, (rg, x) in enumerate(sorted(sh.items())):
        if rg not in reg and x > 0.005:
            f.append('LO_NGC_EXTENDED_SHELL_%d_GT_0.005' % j)
    if any(lo_ < LO_NGC_RANGES[0][0] for lo_, _ in sh):
        f.append('DEFECT:LO_NGC_SHELL_BELOW_K_A69_2')
    return f


def rpair_key_ok(key, members=T_CASES):
    """'<label>@RPAIR:<pair>' with <pair> a registered R-PAIR id and <label> a member of that pair (exact match)."""
    if not isinstance(key, str) or '@RPAIR:' not in key:
        return False
    lab, pid = key.split('@RPAIR:', 1)
    return pid in RPAIR_MANIFEST_IDS and lab in PAIRS[pid] and lab in members                 # R6 [A56 N2] incl. RB_FP


def g_I1T(rec, ctx, xr, read):
    """[R1 I1T] 'at every tail build': every T-case build, and every R-PAIR member build '<label>@RPAIR:<pair>' (verify D5)."""
    fails, per, keys = [], {}, []
    for j, b in enumerate(need(rec, 'builds', 'I1T', 'nonempty_list', read)):
        w = 'I1T:builds[%d]' % j
        c = need(b, 'case', w, 'str')
        if c not in T_CASES and not rpair_key_ok(c):
            raise FieldMissing(w, 'case', 'UNREGISTERED_VALUE')
        keys.append((c, need(b, 'stage', w, 'str')))
    dup = unique_keys_codes(keys, 'I1T', 'builds')           # R10 [A71] one (case, stage) build listed twice (per-case map below)
    if dup:
        raise DuplicateEntry(dup)
    for j, b in enumerate(rec['builds']):
        w = 'I1T:builds[%d]' % j
        c = b['case']
        ok = need(b, 'max_rel', w, 'num>=0') <= 1e-12 and need(b, 'nodes', w, 'int') == 4096
        per[c] = 'FAIL' if (not ok or per.get(c) == 'FAIL') else 'PASS'
        if not ok:
            fails.append('UV_TAIL_SOURCE_MISMATCH:%s' % c)
    for c in T_CASES:
        per.setdefault(c, 'UNCOVERED')
    xr('_i1t_per_case', per, None)
    return fails


def g_T2I(rec, ctx, xr, read):                                                                         # [RA3]
    fails = []
    if need(rec, 'case', 'T2I', 'str', read) != 'C5H' or need(rec, 'region', 'T2I', 'str', read) != 'G5\\G4':
        fails.append('DEFECT:T2I_NOT_C5H_G5_MINUS_G4')
    xr('c5h_result_sha256', need(rec, 'c5h_result_sha256', 'T2I', 'sha', read), C5H)
    for k in ('route_a_updated', 'offset_new_body_fourier_J', 'feedback_gas_source_feedback'):
        if need(rec, 'components/' + k, 'T2I', 'num>=0', read) > 1e-12:
            fails.append('T2I_%s_GT_1e-12' % k)
    if need(rec, 'max_rel', 'T2I', 'num>=0', read) > 1e-12:
        fails.append('T2I_MAX_GT_1e-12')
    return fails


def g_SRB_ROT(rec, ctx, xr, read):
    if need(rec, 'case', 'SRB_ROT', 'str', read) != 'C4T':
        return ['DEFECT:SRB_ROT_NOT_C4T']
    xr('c4t_result_sha256', need(rec, 'c4t_result_sha256', 'SRB_ROT', 'sha', read), 'C4T')
    s = need(rec, 'srb_rot_km_s', 'SRB_ROT', 'num12>=0', read)
    return ['SRB_ROT_ROW_%02d_GT_TAU_OVER_10' % (j + 1) for j, (x, t) in enumerate(zip(s, _tau12(ctx))) if x > TH['SRB_ROT'] * t]


def g_RB_FP(rec, ctx, xr, read):
    fails = []
    if need(rec, 'case', 'RB_FP', 'str', read) != 'C4T':
        fails.append('DEFECT:RB_FP_STATE_NOT_C4T')
    xr('c4t_result_sha256', need(rec, 'c4t_result_sha256', 'RB_FP', 'sha', read), 'C4T')
    xr('_eps_max', need(rec, 'eps_max', 'RB_FP', 'num>=0', read), None)     # = EPS eps_max (checked in read_gates)
    shells = need(rec, 'shells', 'RB_FP', 'nonempty_list', read)
    dv = need(rec, 'dV_static_shells_km_s', 'RB_FP', 'dict', read)
    rng = need(rec, 'shell_ranges_inverse_kpc', 'RB_FP', 'list', read)                                 # R7 [A62.1] DECLARED
    full = need(rec, 'full_tail_domain', 'RB_FP', 'bool', read)                                        # R7 [A62.1]
    if not all(isinstance(x, str) and x for x in shells):
        raise FieldMissing('RB_FP', 'shells[]', 'TYPE_unique_nonempty_str')
    if len(set(shells)) != len(shells):                 # R10 [A71] (the labels key dV): the r8 code, plus both entries named
        raise DuplicateEntry(['GATE_RECORD_FIELD_TYPE_unique_nonempty_str:RB_FP:shells[]'] + unique_keys_codes(shells, 'RB_FP', 'shells'))
    for j, lab in enumerate(shells):           # [A54 S6] a record-controlled shell label never enters a path or a code: by index
        read.append('dV_static_shells_km_s/<shells[%d]>' % j)
        if lab not in dv:
            raise FieldMissing('RB_FP', 'dV_static_shells_km_s/<shells[%d]>' % j)
        if not KINDS['num12'](dv[lab]):
            raise FieldMissing('RB_FP', 'dV_static_shells_km_s/<shells[%d]>' % j, 'TYPE_num12')
    if len(rng) != len(shells) or not all(KINDS['range2'](r) and r[0] < r[1] for r in rng):
        raise FieldMissing('RB_FP', 'shell_ranges_inverse_kpc', 'TYPE_range2_list_aligned_with_shells')
    dup = unique_keys_codes([(float(r[0]), float(r[1])) for r in rng], 'RB_FP', 'shell_ranges_inverse_kpc')
    if dup:                                                                            # R10 [A71] one range given twice
        raise DuplicateEntry(dup)
    # R7 [A62.1] (Claude3 0059 item 1; r6 recheck order N4, validity N1): the shell split must cover the C4T tail domain
    # [4, sqrt(2) x P] -- a partial-domain record must not PASS.  The shells (by their registered ranges, in shells order) cover
    # it without a gap and without overlap (kappa sums the shell effects), every dV key is a listed shell, and the record
    # declares full_tail_domain true.  Any violation is a RECORD_DEFECT (the record is not established as specified).
    if set(dv) != set(shells):
        fails.append('DEFECT:RB_FP_DV_KEYS_NOT_EXACTLY_THE_LISTED_SHELLS_A62_1')
    if full is not True:
        fails.append('DEFECT:RB_FP_PARTIAL_TAIL_DOMAIN_DECLARED_A62_1')
    iv = sorted((float(r[0]), float(r[1])) for r in rng)
    if any(b[0] < a[1] for a, b in zip(iv, iv[1:])):
        fails.append('DEFECT:RB_FP_SHELL_RANGES_OVERLAP_A62_1')
    P = production_kbig(ctx)
    if P is None:
        fails.append('DEFECT:RB_FP_PRODUCTION_K_BIG_P_UNREADABLE_FROM_THE_CASE_BLOCK')
    else:
        if not _union_covers(iv, RB_FP_DOMAIN_LOWER, RB_FP_DOMAIN_FACTOR_OF_P * P):
            fails.append('DEFECT:RB_FP_SHELLS_DO_NOT_COVER_THE_TAIL_DOMAIN_A62_1')
        fails += rb_fp_exact_range_codes(iv, P)                                                        # R8 [A67 N3]
    return fails


def rb_fp_exact_range_codes(iv, P):
    """R8 [A67 N3] (r7 recheck validity N3: [[2, 8], [8, 400]] read PASS): the shell ranges run EXACTLY from K = 4 to sqrt(2) x P
    (compared exactly: the launch-packet producer cuts at math.sqrt(2) * K_big, the same float); a range below K or above
    sqrt(2) x P is an excess, a lowest edge above K or a highest edge below sqrt(2) x P a shortfall; both refuse (RECORD_DEFECT)."""
    if not iv:
        return []
    lo, hi, top = min(a for a, _ in iv), max(b for _, b in iv), RB_FP_DOMAIN_FACTOR_OF_P * P
    out = []
    if lo < RB_FP_DOMAIN_LOWER or hi > top:
        out.append('DEFECT:RB_FP_SHELL_RANGES_EXCEED_K_TO_SQRT2_P_A67_N3')
    if lo < RB_FP_DOMAIN_LOWER:                                     # R10 [A69 note 2] named on its own: coverage starts at lo >= K
        out.append('DEFECT:RB_FP_SHELL_BELOW_K_A69_2')
    if lo > RB_FP_DOMAIN_LOWER or hi < top:
        out.append('DEFECT:RB_FP_SHELL_RANGES_FALL_SHORT_OF_K_TO_SQRT2_P_A67_N3')
    return out


def g_SR_K(rec, ctx, xr, read):
    fails = []
    for s in ('C2R3', 'C3R3', 'C4R3'):
        if need(rec, 'states/' + s, 'SR_K', 'sha', read) != PIN_R3[s][1]:
            fails.append('DEFECT:SR_K_STATE_%s' % s)
    D = {K: need(rec, 'Delta_km_s/' + K, 'SR_K', 'num12', read) for K in ('2', '3', '4')}
    return fails + sr_k_identical_delta_codes(D)                                                       # R8 [A67 N2]


def sr_k_identical_delta_codes(D):
    """R8 [A67 N2] (Claude3 0059 item 2; r7 recheck validity N2): a Delta that is bitwise identical across K is an SR_K
    RECORD_DEFECT.  DECLARED (stricter, NEW-54): ANY two of Delta_2, Delta_3, Delta_4 bitwise identical (float.hex of every row
    value) refuses, not only all three."""
    out = []
    for a, b in (('2', '3'), ('2', '4'), ('3', '4')):
        if all(float(x).hex() == float(y).hex() for x, y in zip(D[a], D[b])):
            out.append('DEFECT:SR_K_DELTA_BITWISE_IDENTICAL_ACROSS_K_%s_%s_A67_N2' % (a, b))
    return out


def g_EA(rec, ctx, xr, read):
    """[A48 AMB-08] E^A replay per case (C5H required); [A48 AMB-22] each entry carries row_radii_m = the 12 registered row
    radii in row_ids order (else RECORD_DEFECT); labels are exact: <label> or <label>@RPAIR:<pair> (verify blinding B1)."""
    per = need(rec, 'per_case', 'EA', 'dict', read)
    need(rec, 'per_case/C5H', 'EA', 'dict', read)
    fails = []
    for lab in per:
        if lab not in REGISTERED and not rpair_key_ok(lab, REGISTERED):
            raise FieldMissing('EA', 'per_case/<unregistered label>', 'UNREGISTERED_LABEL')
        xr('per_case/%s/result_sha256' % lab, need(rec, 'per_case/%s/result_sha256' % lab, 'EA', 'sha', read), lab)
        need(rec, 'per_case/%s/E_A_rows_km_s' % lab, 'EA', 'num12>=0', read)
        need(rec, 'per_case/%s/accepted_iteration' % lab, 'EA', 'int', read)
        if not radii_equal(need(rec, 'per_case/%s/row_radii_m' % lab, 'EA', 'num12', read), ctx['row_radii_m']):
            fails.append('DEFECT:EA_ROW_RADII_NOT_REGISTERED:%s' % lab)
    return fails


def g_MT(rec, ctx, xr, read):
    """[R1 MT_monitor] [A48 AMB-25] if supplied, covers every T-case.  [A50 S2] an MT verdict FAIL for a run (M_T(accepted)
    > 1/4) IS the TAIL_SOURCE_UNDERCONVERGED flag on that run: per run, flags = [TAIL_SOURCE_UNDERCONVERGED] iff M_T > 1/4,
    and the record verdict is FAIL iff some run fails, else PASS; any inconsistency is a record defect (NO_RUN, AMB-02).
    The failing runs are derived (mt_failed_runs) and flag those runs in the decision."""
    per = need(rec, 'per_case', 'MT', 'dict', read)
    for lab in T_CASES:                                                                   # if supplied, it covers every T-case
        if lab not in per:
            raise FieldMissing('MT', 'per_case/%s' % lab)
    out, failed = [], []
    for lab in per:
        if lab not in T_CASES and not rpair_key_ok(lab):
            raise FieldMissing('MT', 'per_case/<unregistered label>', 'UNREGISTERED_LABEL')
        xr('per_case/%s/result_sha256' % lab, need(rec, 'per_case/%s/result_sha256' % lab, 'MT', 'sha', read), lab)
        mt = need(rec, 'per_case/%s/M_T_accepted' % lab, 'MT', 'num', read)
        fl = need(rec, 'per_case/%s/flags' % lab, 'MT', 'list', read)
        xr('per_case/%s/flags' % lab, fl, '_mt:' + lab)
        run_fails = mt > MT_THRESHOLD
        if fl != ([FLAG_TSU] if run_fails else []):
            out.append('DEFECT:MT_FLAGS_INCONSISTENT_WITH_M_T:%s' % lab)
        if run_fails:
            failed.append(lab)
            out.append('MT_RUN_FAILS_FLAGGED:%s' % lab)
    verdict = rec.get('verdict')
    if verdict == GATE_PASS_VERDICTS['MT'] and failed:
        out.append('DEFECT:MT_VERDICT_PASS_WITH_A_FAILING_RUN')
    elif verdict == MT_FAIL_VERDICT and not failed:
        out.append('DEFECT:MT_VERDICT_FAIL_WITHOUT_A_FAILING_RUN')
    elif verdict not in (GATE_PASS_VERDICTS['MT'], MT_FAIL_VERDICT):
        out.append('DEFECT:MT_VERDICT_NOT_PASS_OR_FAIL')
    xr('_mt_failed_runs', sorted(failed), None)
    return out


def g_HARMONICS(rec, ctx, xr, read):                                                                    # [RA10]
    keys = []
    for j, x in enumerate(need(rec, 'rows', 'HARMONICS', 'nonempty_list', read)):
        w = 'HARMONICS:rows[%d]' % j
        keys.append((need(x, 'case', w, 'str'), need(x, 'source', w, 'str'), need(x, 'query', w, 'int')))
        for k in ('R_kpc', 'a0', 'a4', 'a8'):
            need(x, k, w, 'num')
        need(x, 'units', w, 'str')
    # R11 [A79.1] (Codex2 0454; helper I B11s; A75.2 B11): a harmonics row is identified by (case, source, query); one row given twice
    # (exactly, or with another a4) is a RECORD_DEFECT naming both rows (r10: declared 'not mapped')
    dup = unique_keys_codes(keys, 'HARMONICS', 'rows')
    if dup:
        raise DuplicateEntry(dup)
    return []


def g_FLAG_RULINGS(rec, ctx, xr, read):
    """[A48 AMB-19] a ruling is a root addendum entry naming the flag, the run (label + result sha) and the evidence; its
    disposition is CLEARED (with a stated reason) or RERUN_ORDERED (the registered rerun).  Only CLEARED rules the flag."""
    out = []
    for j, x in enumerate(need(rec, 'rulings', 'FLAG_RULINGS', 'list', read)):
        w = 'FLAG_RULINGS:rulings[%d]' % j
        flag = need(x, 'flag', w, 'str')
        if flag not in (FLAG_TSU, FLAG_SQM):
            raise FieldMissing(w, 'flag', 'UNKNOWN_VALUE')
        run = need(x, 'run', w, 'str')
        if not (run in T_CASES or rpair_key_ok(run)) or (flag == FLAG_SQM and run != 'C4T'):
            raise FieldMissing(w, 'run', 'UNREGISTERED_VALUE')
        xr('rulings[%d]/run_result_sha256' % j, need(x, 'run_result_sha256', w, 'sha'), run)
        need(x, 'evidence', w, 'str')
        disp = need(x, 'disposition', w, 'str')
        if disp not in FLAG_DISPOSITIONS:
            raise FieldMissing(w, 'disposition', 'UNKNOWN_VALUE')
        if disp == 'CLEARED':
            need(x, 'reason', w, 'str')
        need(x, 'root_decision', w, 'str')
        out.append({'flag': flag, 'run': run, 'disposition': disp, 'root_decision': x['root_decision']})
    # R10 [A71] (Claude3 helper I item 1: flag_rulings built {(flag, run): ruling} last-wins, so a RERUN_ORDERED ruling followed by
    # a CLEARED duplicate cleared the flag): one (flag, run) ruled twice is a RECORD_DEFECT naming both rulings
    dup = unique_keys_codes([(x['flag'], x['run']) for x in out], 'FLAG_RULINGS', 'rulings')
    if dup:
        raise DuplicateEntry(dup)
    xr('_rulings', out, None)
    return []


def g_I4(rec, ctx, xr, read):
    """[A47 I4] [verify D7] the final implementation check: the V8c-F1 fix confirmed and serial == parallel bitwise with the
    tail on, under a driver every T-case registers.  Required in route-A mode parallel8."""
    fails = []
    if need(rec, 'tail', 'I4', 'str', read) != 'ON':
        fails.append('DEFECT:I4_TAIL_NOT_ON')
    drv = need(rec, 'driver_sha256', 'I4', 'sha', read)
    cases = ((ctx.get('case_block') or {}).get('cases') or {})
    if not all(drv in (cases.get(c) or {}).get('drivers_allowed', []) for c in T_CASES):
        fails.append('DEFECT:I4_DRIVER_NOT_REGISTERED_FOR_EVERY_T_CASE')
    need(rec, 'serial_result_sha256', 'I4', 'sha', read)
    need(rec, 'parallel_result_sha256', 'I4', 'sha', read)
    if need(rec, 'v8c_f1_fix_confirmed', 'I4', 'bool', read) is not True:
        fails.append('I4_V8C_F1_FIX_NOT_CONFIRMED')
    if need(rec, 'bitwise_equal', 'I4', 'bool', read) is not True:
        fails.append('I4_SERIAL_PARALLEL_NOT_BITWISE_EQUAL')
    if need(rec, 'differences_outside_custody', 'I4', 'list', read):
        fails.append('I4_DIFFERENCES_OUTSIDE_CUSTODY')
    return fails


GATE_PASS_VERDICTS = {
    'B0': 'PASS_PLAN_IDENTICAL', 'B0prime_DRY': 'PASS_DRY_IDENTICAL', 'B0prime_RERUN': 'PASS_RESULT_EQUAL_EXCEPT_DECLARED',
    'B0_FA': 'PASS', 'B1': 'PASS_BITWISE_EQUAL_EXCEPT_DECLARED', 'B1_OFF': 'PASS_BITWISE_EQUAL_EXCEPT_DECLARED', 'B2': 'PASS',
    'B3': 'PASS', 'B0_RO1': 'PASS', 'B0_N3': 'PASS', 'EPS': 'CERTIFIED', 'DOUBLING': 'PASS', 'GQ': 'PASS', 'LO': 'PASS',
    'LO_NGC': 'PASS', 'I1T': 'PASS', 'T2I': 'PASS', 'SRB_ROT': 'PASS', 'RB_FP': 'SHELL_SPLIT_COMPUTED', 'SR_K': 'REPLAYED',
    'EA': 'REPLAYED', 'MT': 'PASS', 'HARMONICS': 'REPORTED', 'FLAG_RULINGS': 'ROOT_RULINGS', 'I4': I4_PASS_VERDICT}
# [A54 S5] per-gate FAILING verdicts (Claude3 0053 S5: 'failing verdicts should be defined per gate').  A verdict that is neither
# the pass verdict nor a registered failing verdict is a RECORD_DEFECT (VERDICT_NOT_REGISTERED: e.g. NOT_COMPUTED, ERROR).
GATE_FAIL_VERDICTS = dict({g: ('FAIL',) for g in GATE_PASS_VERDICTS},
                          EPS=('EPS_UNCERTIFIED', 'FAIL'), GQ=('UV_TAIL_GAS_QUADRATURE_UNCERTIFIED', 'FAIL'),
                          I1T=('UV_TAIL_SOURCE_MISMATCH', 'FAIL'))
# Gates whose record carries no failing clause the compare recomputes (only DEFECT codes): their registered failing verdict
# cannot contradict their data and is read as FAIL (DECLARED).  Every other gate's verdict must AGREE with its data [A54 S5]:
# a failing verdict with no failing clause, or the pass verdict with a failing data clause, is a RECORD_DEFECT (NO_RUN group).
VERDICT_ONLY_GATES = ('B0', 'B0prime_DRY', 'RB_FP', 'SR_K', 'EA', 'HARMONICS', 'FLAG_RULINGS')
# Coverage / requirement clauses: the record does not reach a registered domain (A48 AMB-12, A50 root item 8, A54 coverage).  A
# pass verdict over such a shortfall does not contradict the record's own measured data; the shortfall reads as the gate's FAIL
# (GQ, EPS: NUMERICS_UNCERTIFIED), as A50 root item 8 rules (DECLARED reading of S5's 'its own data').
COVERAGE_CODE_PREFIXES = ('EPS_COVERAGE', 'GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT', 'GQ_DDO_UNION_DOES_NOT_COVER', 'GQ_NGC_UNION_DOES_NOT_COVER')


GATE_FUNCS = {'B0': g_B0, 'B0prime_DRY': g_B0prime_DRY, 'B0prime_RERUN': g_B0prime_RERUN, 'B0_FA': g_B0_FA, 'B1': g_B1,
              'B1_OFF': g_B1_OFF, 'B2': g_B2, 'B3': g_B3, 'B0_RO1': g_B0_RO1, 'B0_N3': g_B0_N3, 'EPS': g_EPS,
              'DOUBLING': g_DOUBLING, 'GQ': g_GQ, 'LO': g_LO, 'LO_NGC': g_LO_NGC, 'I1T': g_I1T, 'T2I': g_T2I,
              'SRB_ROT': g_SRB_ROT, 'RB_FP': g_RB_FP, 'SR_K': g_SR_K, 'EA': g_EA, 'MT': g_MT, 'HARMONICS': g_HARMONICS,
              'FLAG_RULINGS': g_FLAG_RULINGS, 'I4': g_I4}


def evaluate_gate(name, path, ctx, runs_sha=None):
    """Callable on its own.  status: PASS | FAIL | RECORD_DEFECT | MISSING.  codes name the failing clause or missing field.
    runs_sha: {label: result_sha256 or None} for cross-references (a record naming another result is a RECORD_DEFECT)."""
    out = {'gate': name, 'status': None, 'codes': [], 'fields_read': [], 'record': None, 'crossref': {}, 'derived': {}}
    if path is None or not Path(path).is_file():
        out.update(status='MISSING', codes=['GATE_RECORD_MISSING:%s' % name])
        return out
    try:
        rec, sh = _read_json(path)
    except Exception as exc:
        out.update(status='RECORD_DEFECT', codes=['GATE_RECORD_UNREADABLE:%s:%s' % (name, type(exc).__name__)]  # incl. DuplicateKey
                   + (['%s:%s' % (exc.code, name)] if isinstance(exc, DuplicateKey) else []))       # R10 [A71] both members named
        return out
    out['record'] = {'path': str(Path(path).resolve()), 'sha256': sh}
    read = out['fields_read']
    runs_sha = runs_sha or {}
    defects = []

    def xr(field, value, target):
        if field.startswith('_'):
            out['derived'][field.lstrip('_')] = value
            return
        if isinstance(target, str) and target.startswith('_mt:'):
            mf = out['derived'].setdefault('mt_flags', {})
            if target[4:] in mf:                          # R10 [A71] (g_MT labels are JSON keys: unique; defence in depth)
                defects.append('DUPLICATE_ENTRY_A71:%s:mt_flags[%d]:mt_flags[%d]' % (name, list(mf).index(target[4:]), len(mf)))
            mf[target[4:]] = value
            return
        have = runs_sha.get(target)
        if field in out['crossref']:                     # R10 [A71] one crossref field written twice: a defect, never last-wins
            defects.append('DUPLICATE_ENTRY_A71:%s:crossref[%d]:crossref[%d]' % (name, list(out['crossref']).index(field), len(out['crossref'])))
        out['crossref'][field] = {'target': target, 'target_present': have is not None, 'equal': None if have is None else have == value}
        if have is not None and have != value:
            defects.append('CROSSREF_MISMATCH:%s:%s' % (name, field))
    try:
        if need(rec, 'schema', name, 'str', read) != GATE_SCHEMA:
            defects.append('GATE_RECORD_SCHEMA:%s' % name)
        if need(rec, 'gate', name, 'str', read) != name:
            defects.append('GATE_RECORD_NAME:%s' % name)
        ppath = need(rec, 'producer/path', name, 'str', read)
        psha = need(rec, 'producer/sha256', name, 'sha', read)
        reg = (ctx or {}).get('producer_registry')                                                   # R7 [A62.2]
        if reg is None:
            defects.append('PRODUCER_REGISTRY_ABSENT_A62_2:%s' % name)
        else:                                       # R10 [A69 note 1] the registered path and sha, and the producer's bytes now
            defects += file_pin_codes(ppath, psha, reg['producers'].get(name, frozenset()),
                                      (PRODUCER_SHA_CODE, name, PRODUCER_PATH_CODE, PRODUCER_BYTES_CODE))
        defects += gate_record_sha_codes(name, sh, reg)                                              # R8 [A67 N2]
        if 'numbers_producer' in rec:          # R11 (r10 recheck validity N5) the computing tool a successor record names is bound
            npp = need(rec, 'numbers_producer/path', name, 'str', read)      # by its bytes too (it is not a registry entry: DECLARED)
            nps = need(rec, 'numbers_producer/sha256', name, 'sha', read)
            try:
                okn = npp.startswith('/') and sha256_file(npp) == nps
            except OSError:
                okn = False
            if not okn:
                defects.append('NUMBERS_PRODUCER_BYTES_NOT_THE_NAMED_SHA_R11:%s' % name)
        verdict = need(rec, 'verdict', name, 'str', read)
        codes = GATE_FUNCS[name](rec, ctx, xr, read)
    except FieldMissing as exc:
        out.update(status='RECORD_DEFECT', codes=defects + ['GATE_RECORD_' + exc.code])
        return out
    except DuplicateEntry as exc:                                  # R10 [A71] a duplicate entry: a RECORD_DEFECT naming both
        out.update(status='RECORD_DEFECT', codes=defects + exc.codes)
        return out
    except Exception as exc:                                                                  # [verify N3] never raises
        out.update(status='RECORD_DEFECT', codes=defects + ['GATE_RECORD_EXCEPTION:%s:%s' % (name, type(exc).__name__)])
        return out
    defects += [c[len('DEFECT:'):] for c in codes if c.startswith('DEFECT:')]
    fails = [c for c in codes if not c.startswith('DEFECT:')]
    if defects:
        out.update(status='RECORD_DEFECT', codes=defects + fails)
        return out
    vcode = 'VERDICT:%s:%s' % (name, _enum(verdict, pattern=_RE_UPPER_CODE))
    data_fails = [c for c in fails if not c.startswith(COVERAGE_CODE_PREFIXES)]
    if verdict == GATE_PASS_VERDICTS[name]:                                                          # [A54 S5]
        if data_fails and name not in VERDICT_ONLY_GATES:
            out.update(status='RECORD_DEFECT', codes=['VERDICT_PASS_CONTRADICTS_DATA:%s' % name] + fails)
            return out
    elif verdict in GATE_FAIL_VERDICTS[name]:
        if not fails and name not in VERDICT_ONLY_GATES:
            out.update(status='RECORD_DEFECT', codes=['VERDICT_FAIL_CONTRADICTS_DATA:%s' % name, vcode])
            return out
        fails = [vcode] + fails
    else:
        out.update(status='RECORD_DEFECT', codes=['VERDICT_NOT_REGISTERED:%s' % name, vcode] + fails)
        return out
    out.update(status='FAIL' if fails else 'PASS', codes=fails, _record_json=rec)
    return out


# ============================================================================================ noise, decidability, tests
E_UNAVAILABLE = 'E_UNAVAILABLE_NO_PICARD_INCREMENT'
E_UNAVAILABLE_NONCONTRACTING = 'E_UNAVAILABLE_TAU_NORM_RATIO_GE_1'                                     # [A53 NEW-7]
E_UNAVAILABLE_ROW_RATIO = 'E_UNAVAILABLE_ROW_RATIO_GE_1_A56_N1'                                        # R6 [A56 N1]
# every code under which E is UNAVAILABLE (-> undecidable -> R-PAIR, branch PICARD: A48 AMB-05, A50 root item 1); any other
# code is a record problem (decidability not computable -> INCOMPLETE).  [A54 B4] a pass-row gap is unavailable too, and a test
# whose R-PAIR does not resolve it reads INCOMPLETE (evaluate_pair_test / the B4 pending step).
E_UNAVAILABLE_CODES = (E_UNAVAILABLE, E_UNAVAILABLE_NONCONTRACTING, PASS_ROW_GAP, E_UNAVAILABLE_ROW_RATIO)


PICARD_Q_CAP = None              # R6 [A58 RI-18] the A51 F2 cap q = min(0.9, ..) is REMOVED (stricter): q/(1-q) exactly for q < 1


def _tau_norm(d, ids, tau):
    """[A51 F2] ||d||_tau = max_i |d_i| / tau_i."""
    return max(abs(d[i]) / tau[i] for i in ids)


def picard_noise_detail(run, ids, tau):
    """[A51 F2] (ruled pre-result; replaces R1's per-row ratio) the a-posteriori contraction bound in the norm in which the
    contraction is measured, as TIGHTENED by [A54 S7], [A56 N1] and [A58 RI-18] and restricted by [A53 NEW-7] and [A54 B4].  With the Picard increments
    d_k = v_k - v_(k-1) (observe_every_pass):
      ||d_k||_tau = max_i |d_k,i| / tau_i;
      [A54 B4] a pass recorded without rows, or pass indices not consecutive from 1: E UNAVAILABLE (PASS_ROW_GAP);
      [A53 NEW-7] an observed tau-norm ratio >= 1 on either of the last two ratios: E UNAVAILABLE (TAU_NORM_RATIO_GE_1);
      q = the largest of the last two observed ratios ||d_k||_tau / ||d_(k-1)||_tau (with only one ratio, that one); R6 [A58
          RI-18]: no cap (R5 read min(0.9, ..)); q < 1 here by NEW-7;
      norm bound  N_i = tau_i ||d_last||_tau q / (1 - q);
      per-row ratio q_i = |d_last,i| / |d_prev,i| from the last two increments; R6 [A56 N1]: ANY row with q_i >= 1 (same-sign or
          alternating; |d_prev,i| = 0 < |d_last,i| is q_i = +inf) makes E UNAVAILABLE for the run (ROW_RATIO_GE_1 -> R-PAIR);
          a row with d_last,i = 0 has q_i = 0 and bound 0 (0/0 read as 0: DECLARED);
      [A54 S7] same-sign row (d_last,i * d_prev,i > 0): S_i = |d_last,i| q_i / (1 - q_i) (R6 [A58 RI-18]: q_i uncapped);
      R6 [A56 N1] alternating row (d_last,i * d_prev,i < 0): A_i = |d_last,i| q_i / (1 + q_i) (the remaining tail of a geometric
          series of ratio -q_i);
      E_i = max(N_i, S_i, A_i);
      exactly one increment (two pass rows): E_i = tau_i ||d_last||_tau (q/(1-q) taken as 1; no ratio, no per-row bound);
      no increment (one pass row): E unavailable (A48 AMB-05 -> undecidable -> R-PAIR).
    A ratio with ||d_(k-1)||_tau = 0 is +inf when ||d_k||_tau > 0 (so NEW-7 makes E unavailable); 0/0 is read as 0 (it can
    only occur when the later increments are 0 or another ratio is +inf: DECLARED).  The geometric bound assumes the observed
    ratio is the map's contraction factor: DECLARED; A54 S7 checks it per row on the run's own increments (same-sign rows) and
    contraction_observed is reported.  Thresholds are unchanged; E decides only decidability.
    [verify D3] a missing or non-finite row in the passes used is a record problem (INCOMPLETE), never a number."""
    pr = run.get('pass_rows') or []
    final = (run.get('adapted') or {}).get('rows') or {}
    if run.get('pass_rows_s9'):                                                     # R6 [A54 S9] a record defect, never a number
        return None, run['pass_rows_s9'], {}
    if run.get('pass_rows_gap'):                                                                       # [A54 B4]
        return None, PASS_ROW_GAP, {'pass_rows_gap': run['pass_rows_gap']}
    if not pr:
        return None, 'NO_PASS_ROWS', {}
    use = pr[-4:]
    if not all(_num(q.get(i)) for q in use for i in ids):
        return None, 'PASS_ROWS_NONFINITE_OR_MISSING', {}
    if any(pr[-1][i] != final.get(i) for i in ids):
        return None, 'FINAL_ROWS_NOT_LAST_PASS_ROWS', {}
    if len(pr) < 2:
        return None, E_UNAVAILABLE, {'increments': 0}
    d = [{i: use[j][i] - use[j - 1][i] for i in ids} for j in range(1, len(use))]
    nrm = [_tau_norm(x, ids, tau) for x in d]
    ratios = []
    for j in range(1, len(nrm)):
        a, b = nrm[j], nrm[j - 1]
        ratios.append(a / b if b > 0 else (math.inf if a > 0 else 0.0))
    det = {'increments': len(pr) - 1, 'tau_norm_last': nrm[-1],
           'tau_norm_ratios_used': [r if math.isfinite(r) else None for r in ratios[-2:]],
           'contraction_observed': all(r < 1 for r in ratios) if ratios else None,
           'label': 'A51 F2 tau-norm bound, uncapped (A58 RI-18), with the A54 S7 same-sign and A56 N1 alternating per-row bounds; '
                    'NEW-7, A56 N1 (a row ratio >= 1) and B4 make E unavailable'}
    if any(r >= 1 for r in ratios[-2:]):                                                              # [A53 NEW-7]
        det['q'] = None
        return None, E_UNAVAILABLE_NONCONTRACTING, det
    per_row = {i: 0.0 for i in ids}
    row_kind = {i: None for i in ids}
    if not ratios:
        fac, q = 1.0, None                                                                             # exactly one increment
    else:
        q = max(ratios[-2:])                                                                           # R6 [A58 RI-18] uncapped
        fac = q / (1.0 - q)
        dl, dp = d[-1], d[-2]
        ge1 = []
        for i in ids:                                                                                   # [A54 S7] [A56 N1]
            a_, b_ = abs(dl[i]), abs(dp[i])
            if a_ == 0:
                continue                                                                               # q_i = 0: bound 0
            if b_ == 0:
                ge1.append(i)                                                                          # q_i = +inf
                continue
            qi = a_ / b_
            if qi >= 1:
                ge1.append(i)
                continue
            if dl[i] * dp[i] > 0:
                per_row[i], row_kind[i] = a_ * qi / (1.0 - qi), 'SAME_SIGN'
            else:
                per_row[i], row_kind[i] = a_ * qi / (1.0 + qi), 'ALTERNATING'
        if ge1:                                                                                         # R6 [A56 N1]
            det.update(q=q, rows_with_ratio_ge_1=ge1)
            return None, E_UNAVAILABLE_ROW_RATIO, det
    norm_b = {i: tau[i] * nrm[-1] * fac for i in ids}
    E = {i: max(norm_b[i], per_row[i]) for i in ids}
    det.update(q=q, factor=fac, rows_where_per_row_bound_exceeds_norm_bound=[i for i in ids if per_row[i] > norm_b[i]],
               per_row_bound_kind={i: row_kind[i] for i in ids if row_kind[i]})
    if not all(math.isfinite(x) for x in E.values()):
        return None, 'E_NONFINITE', det
    return E, None, det


def picard_noise(run, ids, tau):
    """[A51 F2] E_i(run) (see picard_noise_detail).  tau: {row id: tau_i} (the pinned V005 tau, ctx['tau'])."""
    E, code, _ = picard_noise_detail(run, ids, tau)
    return E, code


def route_a_noise(label, run, validity, ea_gate, ids):
    """[R1 route_a_noise] E^A_i(run): the run's route-A uv_tail record when its row order is VERIFIED (probe_R_m = the
    registered row radii; A48 AMB-22, verify G4), else the EA replay record (row radii checked by gate EA)."""
    info = (validity or {}).get('_uvt_info') or {}
    if info.get('E_A_rows_km_s') is not None:
        return dict(zip(ids, info['E_A_rows_km_s'])), 'route_a_record'
    if (ea_gate or {}).get('status') != 'PASS':
        return None, 'EA_UNAVAILABLE:%s (EA record %s)' % (label, (ea_gate or {}).get('status', 'MISSING'))
    per = ((ea_gate or {}).get('_record_json') or {}).get('per_case') or {}
    e = per.get(label)
    if isinstance(e, dict) and KINDS['num12>=0'](e.get('E_A_rows_km_s')):
        return dict(zip(ids, e['E_A_rows_km_s'])), 'EA_record'
    return None, 'EA_UNAVAILABLE:%s' % label


def rpair_branch_row(und, ratio, ids):
    """R10 [A69 note 3] (AMB-07) the R-PAIR branch row: the undecidable row with the largest (E + E^A)/tau; on an EXACT tie, the
    LOWEST row index in row_ids order (deterministic; never the dict or set order)."""
    pos = {i: k for k, i in enumerate(ids)}
    return min(und, key=lambda i: (-ratio[i], pos[i]))


def pair_noise(la, lb, R, V, ea_gate, ctx):
    """[R1 decidable_iff] E_i(P) + E^A_i(P) <= tau_i/8 on every row; R-PAIR branch from the worst undecidable row (AMB-07).
    E unavailable (no increment) -> undecidable, branch DECLARED PICARD (A48 AMB-05; the branch is unnamed: root item G1)."""
    ids, tau = ctx['ids'], ctx['tau']
    out = {'members': [la, lb], 'E_rule': 'A51 F2 tau-norm a-posteriori bound'}
    Ea, ca, da = picard_noise_detail(R[la], ids, tau)
    Eb, cb_, db = picard_noise_detail(R[lb], ids, tau)
    out['picard_bound'] = {la: da, lb: db}                                                             # [A51 F2] reported
    Aa, sa = route_a_noise(la, R[la], V.get(la), ea_gate, ids)
    Ab, sb = route_a_noise(lb, R[lb], V.get(lb), ea_gate, ids)
    bad = [c for c in (ca, cb_) if c and c not in E_UNAVAILABLE_CODES] + [x for x in (sa, sb) if x.startswith('EA_UNAVAILABLE')]
    if bad:
        out.update(decidable=None, reason=bad)
        return out
    unav = [c for c in (ca, cb_) if c in E_UNAVAILABLE_CODES]
    if unav:                                          # [A48 AMB-05] [A53 NEW-7] [A54 B4] E unavailable -> R-PAIR, PICARD
        out.update(decidable=False, undecidable_rows=list(ids), reason=sorted(set(unav)), rpair_branch=RPAIR_BRANCH_E_UNAVAILABLE,
                   rpair_branch_row=None, rpair_branch_basis='A50 root item 1 (A48 AMB-05: E unavailable -> R-PAIR; branch PICARD; '
                                                             'A53 NEW-7 / A54 B4 unavailable codes included)')

        return out
    E = {i: Ea[i] + Eb[i] for i in ids}
    EA = {i: Aa[i] + Ab[i] for i in ids}
    ratio = {i: (E[i] + EA[i]) / tau[i] for i in ids}
    und = [i for i in ids if E[i] + EA[i] > DECIDABLE_FRACTION * tau[i]]
    out.update(E_pair=E, EA_pair=EA, noise_over_tau=ratio, undecidable_rows=und, decidable=not und, EA_sources=[sa, sb])
    if und:
        # R10 [A69 note 3] (AMB-07): on an EXACT tie in (E + E^A)/tau the branch row is the LOWEST row index (row_ids order),
        # explicitly: the key orders by the ratio descending, then by the row index ascending (r8 held this by max() returning the
        # first maximum in row_ids order; the rule is now stated in code)
        worst = rpair_branch_row(und, ratio, ids)
        out['rpair_branch'] = 'ROUTE_A' if EA[worst] > E[worst] else 'PICARD'
        out['rpair_branch_row'] = worst
        out['rpair_branch_basis'] = 'A48 AMB-07 (worst row by (E + E^A)/tau; an exact tie: the lowest row index, A69 note 3)'
    return out


def row_stat(ra, rb, ctx):
    ids, tau, sig = ctx['ids'], ctx['tau'], ctx['sigma']
    d = {i: rb[i] - ra[i] for i in ids}
    return {'delta_km_s': d, 'delta_over_tau': {i: d[i] / tau[i] for i in ids}, 'delta_over_sigma': {i: d[i] / sig[i] for i in ids},
            'max_abs_over_tau': max(abs(d[i]) / tau[i] for i in ids)}


def t1_test(r2, r3, r4, ctx):
    """[V005 shape_pass] AND [RA6] per-row clause; TINY exemption only inside RA6 [A47 I2]; FLOOR_LIKE per RA6 wording."""
    ids, tau = ctx['ids'], ctx['tau']
    d23 = {i: r3[i] - r2[i] for i in ids}
    d34 = {i: r4[i] - r3[i] for i in ids}
    D23 = max(abs(d23[i]) / tau[i] for i in ids)
    D34 = max(abs(d34[i]) / tau[i] for i in ids)
    tau_clause = D34 <= 1.0
    max_contraction = D34 <= 0.5 * D23
    shape_pass = tau_clause and max_contraction                                                       # V005 literally
    per = {}
    for i in ids:
        if abs(d23[i]) <= TINY_FRACTION * tau[i] and abs(d34[i]) <= TINY_FRACTION * tau[i]:
            per[i] = 'TINY_EXEMPT'                                                                     # [RA6] TINY (DECLARED)
        elif d23[i] == 0:
            per[i] = 'PASS' if d34[i] == 0 else 'FAIL_ZERO_D23'
        else:
            ok = d23[i] * d34[i] >= 0 and abs(d34[i]) <= 0.5 * abs(d23[i])
            per[i] = 'PASS' if ok else ('FAIL_SIGN' if d23[i] * d34[i] < 0 else 'FAIL_RATIO')
    per_row_ok = all(x in ('PASS', 'TINY_EXEMPT') for x in per.values())
    passed = shape_pass and per_row_ok                                                                 # [A47 I2]
    fail_by = [] if passed else ([c for c, ok in (('TAU_CLAUSE', tau_clause), ('MAX_CONTRACTION', max_contraction),
                                                    ('PER_ROW', per_row_ok)) if not ok])
    floor_like = (not passed) and D23 <= 1.0 and D34 <= 1.0                                            # [RA6] FLOOR_LIKE
    q = D34 / D23 if D23 > 0 else None
    tail = {i: ({'q': abs(d34[i]) / abs(d23[i]), 'non_contracting': not abs(d34[i]) < abs(d23[i])} if d23[i] != 0 else
                {'q': None, 'non_contracting': True}) for i in ids}
    return {'status': 'PASS' if passed else 'FAIL', 'Dhat_2_3': D23, 'Dhat_3_4': D34, 'q_sequence': q,
            'shape_pass_V005': shape_pass, 'per_row_clause': per, 'per_row_clause_pass': per_row_ok,
            'tiny_rows': [i for i in ids if per[i] == 'TINY_EXEMPT'], 'fail_by': fail_by, 'floor_like': floor_like,
            'delta_2_3': d23, 'delta_3_4': d34, 'per_row_tail_diagnostic': tail}


def thresholded(stat, th, per_row=True):
    if per_row:
        return all(abs(x) <= th for x in stat['delta_over_tau'].values())
    return stat['max_abs_over_tau'] <= th


def apply_flag(out, flagged_runs):
    """[A48 AMB-04] flags are evaluated per test: a flagged test that passes is PASS_FLAGGED (passes, flag carried); one that
    fails is UNDECIDABLE_FLAGGED (triggers no failure outcome).  Pending / floor statuses are kept (flag listed)."""
    out['flagged_runs'] = sorted(flagged_runs)
    out['raw_status'] = out['status']
    if flagged_runs:
        if out['status'] == 'PASS':
            out['status'] = 'PASS_FLAGGED'
        elif out['status'] == 'FAIL':
            out['status'] = 'UNDECIDABLE_FLAGGED'
    return out


def rb_fp(R, gates, ctx, eff_flag, RP=None, RPV=None):
    """[R1 RB_FP] [R1 L9] RB-FP_i = 2 eps_max |dv_i/dlambda| kappa_i <= tau_i/10; noise term recorded.
    R1: kappa undefined (sum of the shell effects 0) is not a pass: the row is UNDEFINED and RB_FP reads INCOMPLETE (A1e).
    R6 [A56 N2]: when the E of C4T or C4T-A is UNAVAILABLE (NEW-7, A56 N1, a B4 gap, no increment), RB_FP reads E from the PICARD
    R-PAIR 'RB_FP' (12-pass reruns of C4T and C4T-A admitting their route A): RPAIR_PENDING until it is run; both members valid
    and their E available -> RB_FP is read on the members (rows and E, as every R-PAIR-read test; DECLARED, source RPAIR); a
    member still unavailable (or with a gap) -> INCOMPLETE ('an unresolved one still reads INCOMPLETE').  A record problem
    (not an unavailable code) stays INCOMPLETE."""
    ids, tau = ctx['ids'], ctx['tau']
    g = gates['RB_FP']
    rec = g.get('_record_json') or {}
    eps = gates['EPS'].get('derived', {}).get('eps_max')
    out = {'status': None}
    flagged = [c for c in PAIRS['RB_FP'] if eff_flag(c)]
    if g['status'] != 'PASS' or gates['EPS']['status'] != 'PASS' or eps is None:
        out.update(status='INCOMPLETE', reason='RB_FP %s / EPS %s' % (g['status'], gates['EPS']['status']))
        return apply_flag(out, flagged)
    if rec.get('eps_max') != eps:                                                                     # defensive (cross_gate_checks)
        out.update(status='INCOMPLETE', reason='RB_FP eps_max differs from the EPS certificate')
        return apply_flag(out, flagged)
    E1, c1 = picard_noise(R['C4T'], ids, tau)                                                         # [A51 F2] [A48 AMB-09]
    E2, c2 = picard_noise(R['C4T-A'], ids, tau)
    va, vb = R['C4T']['adapted']['rows'], R['C4T-A']['adapted']['rows']
    out['source'] = 'base'
    if c1 or c2:
        codes = [c for c in (c1, c2) if c]
        if any(c not in E_UNAVAILABLE_CODES for c in codes):
            out.update(status='INCOMPLETE', reason=codes)
            return apply_flag(out, flagged)
        rp = (RP or {}).get(RPAIR_RB_FP)                                                                  # R6 [A56 N2]
        if rp is None:
            out.update(status='RPAIR_PENDING', reason=codes, rpair_branch='PICARD',
                       rpair_branch_basis='A56 N2: E of C4T / C4T-A unavailable -> the PICARD R-PAIR RB_FP (12-pass reruns admitting '
                                          'their route A)')
            return apply_flag(out, flagged)
        keys = {m: '%s@RPAIR:%s' % (m, RPAIR_RB_FP) for m in PAIRS['RB_FP']}
        bad = [k for k in keys.values() if not (RPV or {}).get(k, {}).get('valid_all')]
        if bad:
            out.update(status='INCOMPLETE', reason='RPAIR_MEMBER_INVALID_OR_MISSING:%s' % bad)
            return apply_flag(out, flagged)
        runs = rp['_runs']
        E1, c1 = picard_noise(runs['C4T'], ids, tau)
        E2, c2 = picard_noise(runs['C4T-A'], ids, tau)
        if c1 or c2:
            out.update(status='INCOMPLETE', reason='A56 N2: still unresolved on the RB_FP R-PAIR members: %s'
                                                   % [c for c in (c1, c2) if c])
            return apply_flag(out, flagged)
        va, vb = runs['C4T']['adapted']['rows'], runs['C4T-A']['adapted']['rows']
        out['source'] = 'RPAIR'
        out['rpair_branch'] = 'PICARD'
    shells = rec['shells']
    dV = {i: [rec['dV_static_shells_km_s'][x][j] for x in shells] for j, i in enumerate(ids)}
    rows = {}
    for i in ids:
        Ep = E1[i] + E2[i]
        dvdl = (abs(vb[i] - va[i]) + Ep) / LAMBDA_STEP
        tot = sum(dV[i])
        if tot == 0:
            rows[i] = {'dv_dlambda_km_s': dvdl, 'kappa': None, 'RB_FP_km_s': None, 'noise_term_km_s': None,
                       'dV_static_tail_km_s': tot, 'pass': None, 'status': 'KAPPA_UNDEFINED'}
            continue
        kappa = sum(abs(x) for x in dV[i]) / abs(tot)
        val = RB_FP_FACTOR * eps * dvdl * kappa
        rows[i] = {'dv_dlambda_km_s': dvdl, 'kappa': kappa, 'RB_FP_km_s': val,
                   'noise_term_km_s': RB_FP_FACTOR * kappa * eps * Ep / LAMBDA_STEP, 'dV_static_tail_km_s': tot,
                   'pass': bool(val <= TH['RB_FP'] * tau[i])}
    undefined = [i for i in ids if rows[i]['pass'] is None]
    status = 'FAIL' if any(r['pass'] is False for r in rows.values()) else ('INCOMPLETE' if undefined else 'PASS')
    out.update(status=status, rows=rows, eps_max=eps, assumption='first-order response DECLARED, UNTESTED')
    if undefined and status == 'INCOMPLETE':
        out['reason'] = 'kappa undefined (shell sum 0) on rows %s' % [i[-2:] for i in undefined]
    return apply_flag(out, flagged)


def sr_k(gates, rbfp, ctx):
    """[R1 SR_K] [R1 L6]: pairwise K-dependence (NOT_UV_RESIDUAL clause) and the SR term max(|D4|, |D4| A_i)."""
    ids, tau = ctx['ids'], ctx['tau']
    rec = gates['SR_K'].get('_record_json') or {}
    if gates['SR_K']['status'] != 'PASS':
        return {'status': 'INCOMPLETE'}
    D = {K: dict(zip(ids, rec['Delta_km_s'][K])) for K in ('2', '3', '4')}
    pair = {i: max(abs(D['3'][i] - D['2'][i]), abs(D['4'][i] - D['3'][i])) / tau[i] for i in ids}
    out = {'status': 'COMPUTED', 'Delta_km_s': D, 'pairwise_K_dependence_over_tau': pair,
           'pairwise_within_quarter_tau': all(x <= TH['NOT_UV_SRK'] for x in pair.values()),
           'label': 'static only; fixed-point UNTESTED (deciding test C4T-SR)'}
    rows = (rbfp or {}).get('rows')
    if rows and all(rows[i].get('kappa') is not None for i in ids):
        term, A = {}, {}
        for i in ids:
            dvs = rows[i]['dV_static_tail_km_s']
            A[i] = (rows[i]['dv_dlambda_km_s'] / abs(dvs)) if dvs != 0 else float('inf')
            t = max(abs(D['4'][i]), abs(D['4'][i]) * A[i]) if math.isfinite(A[i]) else (abs(D['4'][i]) if D['4'][i] == 0 else float('inf'))
            term[i] = t
        out.update(A_i={i: (A[i] if math.isfinite(A[i]) else None) for i in ids},
                   SR_term_km_s={i: (term[i] if math.isfinite(term[i]) else None) for i in ids},
                   SOURCE_QUADRATURE_MATERIAL=any((not math.isfinite(term[i])) or term[i] > tau[i] for i in ids))
    return out


def evaluate_pair_test(pid, R, V, RP, RPV, eff_flag, gates, ctx, threshold, decidable_rule, per_row=True):
    """One pair test, read on its data (decidability / R-PAIR bookkeeping or plain pass/fail), then flags applied per test
    [A48 AMB-04].  Picard-branch R-PAIR members carry their base's route-A flag (V6: same route A); route-A-branch members
    carry their own."""
    la, lb = PAIRS[pid]
    out = {'pair': pid, 'members': [la, lb], 'threshold_over_tau': threshold, 'decidability_rule': decidable_rule}
    base_flags = [m for m in (la, lb) if eff_flag(m)]
    if not decidable_rule:
        st = row_stat(R[la]['adapted']['rows'], R[lb]['adapted']['rows'], ctx)
        out.update(stat=st, status='PASS' if thresholded(st, threshold, per_row) else 'FAIL', source='base')
        return apply_flag(out, base_flags)
    nz = pair_noise(la, lb, R, V, gates.get('EA'), ctx)
    out['noise'] = nz
    if nz['decidable'] is None:
        out.update(status='INCOMPLETE', reason=nz['reason'])
        return apply_flag(out, base_flags)
    if nz['decidable']:
        st = row_stat(R[la]['adapted']['rows'], R[lb]['adapted']['rows'], ctx)
        out.update(stat=st, status='PASS' if thresholded(st, threshold, per_row) else 'FAIL', source='base')
        return apply_flag(out, base_flags)
    rp = RP.get(pid)                                                                                   # [R1 R-PAIR] once
    if rp is None:
        out.update(status='RPAIR_PENDING', rpair_branch=nz['rpair_branch'], rpair_branch_row=nz.get('rpair_branch_row'),
                   rpair_branch_basis=nz.get('rpair_branch_basis'))
        return apply_flag(out, base_flags)
    if rp.get('branch') != nz['rpair_branch']:
        out.update(status='INCOMPLETE', reason='RPAIR_BRANCH_MISMATCH: manifest %s, rule %s' % (rp.get('branch'), nz['rpair_branch']))
        return apply_flag(out, base_flags)
    keys = {m: '%s@RPAIR:%s' % (m, pid) for m in (la, lb)}
    bad = [k for k in keys.values() if not RPV.get(k, {}).get('valid_all')]
    if bad:
        out.update(status='INCOMPLETE', reason='RPAIR_MEMBER_INVALID_OR_MISSING:%s' % bad)
        return apply_flag(out, base_flags)
    flags = base_flags if rp['branch'] == 'PICARD' else [k for k in keys.values() if eff_flag(k)]
    R2 = {la: RP[pid]['_runs'][la], lb: RP[pid]['_runs'][lb]}
    V2 = {la: RPV[keys[la]], lb: RPV[keys[lb]]}
    if rp['branch'] == 'PICARD':                                                                       # same route A (V6): its E^A
        for m in (la, lb):
            if (V2[m].get('_uvt_info') or {}).get('E_A_rows_km_s') is None and (V.get(m) or {}).get('_uvt_info'):
                V2[m] = dict(V2[m], _uvt_info=V[m]['_uvt_info'])
    ea = gates.get('EA')
    if rp['branch'] == 'ROUTE_A':
        ea = _rpair_ea_view(ea, pid)
    elif ea:                                                                                           # Picard reruns keep route A:
        ea = _rpair_ea_view(ea, pid, fallback_base=True)                                               # ONLY the base entries apply
    nz2 = pair_noise(la, lb, R2, V2, ea, ctx)
    out['noise_rpair'] = nz2
    if nz2['decidable'] is None:
        out.update(status='INCOMPLETE', reason=nz2['reason'])
    elif nz2['decidable'] is False and PASS_ROW_GAP in (nz2.get('reason') or []):                   # [A54 B4] a record gap on a
        out.update(status='INCOMPLETE', reason='A54 B4: an R-PAIR member has a pass-row gap (record gap; the R-PAIR does not '   # member is
                                               'resolve it)')                                                               # not a reading
    elif nz2['decidable']:
        st = row_stat(R2[la]['adapted']['rows'], R2[lb]['adapted']['rows'], ctx)
        out.update(stat=st, status='PASS' if thresholded(st, threshold, per_row) else 'FAIL', source='RPAIR')
    else:
        out['status'] = 'UNDECIDABLE_AT_ITERATION_FLOOR'                                               # neither pass nor fail
    return apply_flag(out, flags)


def _rpair_ea_view(ea_gate, pid, fallback_base=False):
    """ROUTE_A-branch reruns read E^A from EA per_case '<label>@RPAIR:<pid>' when they have no verified tail record (C5H).
    PICARD-branch reruns (fallback_base) admit their base route A (A53; V6: same identity, same route-A result sha), so ONLY the
    base entries apply.  R6 [r5 recheck order F1]: an @RPAIR entry never replaces its base's E^A; it must equal the base's entry
    (picard_ea_entry_code, checked in evaluate_v007; a contradicting entry makes the member invalid)."""
    if not ea_gate:
        return ea_gate
    per = ((ea_gate.get('_record_json') or {}).get('per_case')) or {}
    if fallback_base:
        view = {k: v for k, v in per.items() if '@' not in k}
    else:      # R10 [A71] re-keyed by label through unique_map (g_EA admits only exact '<label>@RPAIR:<pair>' keys: never raises)
        try:
            view = unique_map([(k.split('@')[0], v) for k, v in per.items() if k.endswith('@RPAIR:' + pid)], 'EA', 'per_case')
        except DuplicateEntry:
            view = {}
    return dict(ea_gate, _record_json={'per_case': view})


PICARD_EA_ENTRY_CODE = 'RPAIR_PICARD_MEMBER_EA_ENTRY_NOT_THE_BASE_ENTRY_A53'


def picard_ea_entry_code(ea_gate, key):
    """R6 [r5 recheck order F1] a PICARD member admits its base's route A, so its E^A is its base's.  An EA entry for the member
    ('<label>@RPAIR:<pid>') must be canonically equal to the base's entry ('<label>') outside result_sha256 (the cross-referenced
    run sha, which differs by construction); an entry with no base entry to compare is a contradiction too (stricter, DECLARED).
    Read only from a PASSing EA record.  Returns None or PICARD_EA_ENTRY_CODE."""
    if (ea_gate or {}).get('status') != 'PASS':
        return None
    per = ((ea_gate.get('_record_json') or {}).get('per_case')) or {}
    if key not in per:
        return None
    base = key.split('@RPAIR:')[0]

    def strip(e):
        return {k: v for k, v in e.items() if k != 'result_sha256'} if isinstance(e, dict) else e
    if base not in per or canon(strip(per[key])) != canon(strip(per[base])):
        return PICARD_EA_ENTRY_CODE
    return None


def srb_rot_readable(gates, ctx):
    """[A52.5] SRB_ROT is read only when the EPS record carries the envelope bound (rule EPS_ENVELOPE_RULE) with coverage
    >= sqrt(2) x the production K_big (the registered C4T uv_tail outer.K_big_inverse_kpc); R5 [A54]: EPS coverage >= sqrt(2)
    x 2P (never below 64 /kpc), which supersedes A52.5's sqrt(2) x P (stricter).  Returns (readable, reason)."""
    env = (gates.get('EPS') or {}).get('derived', {}).get('envelope_bound')
    if (gates.get('EPS') or {}).get('status') != 'PASS':
        return False, 'A52.5: EPS not PASS; SRB_ROT not read'
    if not env:
        return False, 'A52.5: no successor EPS envelope bound (per-shell sup above 15 /kpc is a lower bound); SRB_ROT not read'
    if not env.get('rule_ok'):
        return False, 'A52.5: EPS envelope_bound rule is not %s; SRB_ROT not read' % EPS_ENVELOPE_RULE
    if env.get('dominates_actual_every_shell') is not True:                                         # R7 [A57.4] (SF3)
        return False, 'A57.4: the EPS envelope does not dominate the actual-set value on every shell; SRB_ROT not read'
    edge = coverage_edge_2P(production_kbig(ctx))
    if edge is None:
        return False, 'A52.5: production K_big (registered C4T uv_tail outer.K_big_inverse_kpc) unreadable; SRB_ROT not read'
    if not (_num(env.get('coverage_max_inverse_kpc')) and env['coverage_max_inverse_kpc'] >= edge):
        return False, 'A52.5 / A54: EPS envelope coverage below sqrt(2) x 2P; SRB_ROT not read'
    return True, None


def flag_rulings(gates):
    """[A48 AMB-19] {(flag, run): disposition} from a PASSing FLAG_RULINGS record; only CLEARED rules (clears) a flag."""
    g = gates.get('FLAG_RULINGS') or {}
    if g.get('status') != 'PASS':
        return {}
    # R10 [A71] built by unique_map: a PASSing record has no repeated (flag, run) (g_FLAG_RULINGS refuses one), so this never raises
    return unique_map([((x['flag'], x['run']), x) for x in g.get('derived', {}).get('rulings', [])], 'FLAG_RULINGS', 'rulings')


def ruled_flags(gates):
    return {k for k, x in flag_rulings(gates).items() if x['disposition'] == 'CLEARED'}


# ============================================================================================ decision
def _rpair_leaf_values(run, branch):
    num = ((_normalized(run) or run.get('spec_for_reading') or {}).get('numerics')) if run.get('present') else None
    out = {}
    for k in RPAIR_NUMERICS_LEAVES.get(branch, ()):
        cur, found = num, True
        for p in k.split('.'):
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                found = False
                break
        out[k] = canon(cur) if found else None
    return out


def _invalidate(v, code):
    """[A50 B1] add a V3 code to a validity record and recompute its verdict."""
    if code not in v.get('V3_mismatch', []):
        v['V3_mismatch'] = list(v.get('V3_mismatch', [])) + [code]
    v['V3'] = False
    v['failed'] = [k for k in ('V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'I1T') if k in v and v[k] is False] + \
        [x for x in v.get('failed', []) if x in ('ALIAS', 'missing', 'unregistered')]
    v['valid_all'] = False
    if v.get('reading') is None or str(v.get('reading')).startswith('INVALID:'):
        v['reading'] = 'INVALID:%s' % ','.join(v['failed'])


def _numerics_of(run):
    return ((_normalized(run) or run.get('spec_for_reading') or {}).get('numerics')
            if run.get('present') and not run.get('unreadable') else None)


def b0_extra(gb0):
    """The B0-derived inputs of case_validity (only from a PASSing B0 record): every spec sha of its sets (A48 AMB-13), the EXT set
    (A52.3) and the EXT entries' member evidence (A53 r4 validity F1 option (a))."""
    ok = (gb0 or {}).get('status') == 'PASS'
    d = (gb0 or {}).get('derived', {}) if ok else {}
    return {'b0_spec_shas': set(d.get('b0_spec_shas') or []) if ok else None,
            'b0_ext_spec_shas': set(d.get('b0_ext_spec_shas') or []) if ok else None,
            'b0_ext_entries': dict(d.get('b0_ext_entries') or {}) if ok else None}


def rpair_untriggered(RP, R, V, gates, ctx):
    """[A53 NEW-17] the pair ids the manifest names R-PAIR members for although their R-PAIR was NOT triggered: the base pair's
    decidability is KNOWN and decidable.  Decidability unknown (a base run absent or unreadable, E^A unavailable, a record
    problem) does not trigger an R-PAIR either, but then no test is decided on the members (the pair reads INCOMPLETE before the
    members are consulted): those are not refused (DECLARED; the refusal needs decidability known, Claude3 R3-5)."""
    out = []
    for pid in sorted(RP or {}):
        la, lb = PAIRS[pid]
        if not ((R.get(la) or {}).get('present') and (R.get(lb) or {}).get('present')):
            continue
        if pid == RPAIR_RB_FP:              # R6 [A56 N2] triggered iff the E of C4T or C4T-A is unavailable; both available: refused
            try:
                codes = [picard_noise(R[x], ctx['ids'], ctx['tau'])[1] for x in (la, lb)]
            except Exception:
                continue
            if all(c is None for c in codes):
                out.append(pid)
            continue
        try:
            nz = pair_noise(la, lb, R, V, gates.get('EA'), ctx)
        except Exception:
            continue
        if nz.get('decidable') is True:
            out.append(pid)
    return out


B4_UNIT_CASES = {'T1': TEST_RUNS['T1'], 'T1_H': PAIRS['T1_H'], 'T1_S': PAIRS['T1_S'], 'T2': PAIRS['T2'], 'T2c': PAIRS['T2c'],
                 'T3_KLO': PAIRS['T3_KLO'], 'T3_KHI': PAIRS['T3_KHI'], 'RB_FP': PAIRS['RB_FP'], 'SRB_ROT': ('C4T',)}


def b4_gap_pending(R, units):
    """[A54 B4] a case whose record has a pass-row gap reads INCOMPLETE unless an R-PAIR resolves it: resolved iff the case is a
    member of a resolvable unit (the decidability pairs and, R6 [A56 N2], RB_FP) and EVERY such unit it belongs to was read on
    its R-PAIR members (source RPAIR).
    Each unresolved gap is a pending step sitting at the earliest outcome of the units that read the case."""
    out = []
    for lab in REGISTERED:
        run = R.get(lab) or {}
        if not run.get('pass_rows_gap'):
            continue
        dps = [u for u in RPAIR_RESOLVABLE if lab in PAIRS[u]]                            # R6 [A56 N2]: RB_FP is resolvable
        if dps and all((units.get(u) or {}).get('source') == 'RPAIR' for u in dps):
            continue
        uses = [u for u, cs in B4_UNIT_CASES.items() if lab in cs]
        earliest = min((UNIT_EARLIEST_OUTCOME[u] for u in uses), key=outcome_position) if uses else 'IMPLEMENTATION_DEFECT'
        out.append({'step': 'A54 B4 pass-row gap on %s' % lab, 'earliest_outcome': earliest,
                    'detail': '%s: %s (E unavailable; no R-PAIR resolves it)' % (lab, run['pass_rows_gap'])})
    return out


def gate_fail_next_step(g):
    """R6 (r5 recheck validity F2; NEW-30, DECLARED reporting only, the reading is unchanged): the next step of a gate that FAILS,
    named at every reading even when an earlier outcome stops the reading before that gate's group is read."""
    if g in NO_RUN_GATES:
        return NEXT_STEP['NO_RUN']
    if g in CERT_NUMERICS_GATES:
        return NEXT_STEP['NUMERICS_UNCERTIFIED']
    if g in CERT_LAPSE_GATES:
        return NEXT_STEP['NON_LAPSE_TAIL_MATERIAL']
    if g == 'T2I':
        return T2I_DEFECT_NEXT
    if g == 'I4':
        return I4_NEXT
    return 'the %s gate fails: its test reads as the decision rule names it once the reading reaches it' % g


def evaluate_v007(ctx, R, IDR, gates, RP=None, packets=None):
    """The whole V007 reading.  R: {label: read_run}, IDR: {identity run: read_run}, gates: {name: evaluate_gate (+_record_json)},
    RP: {pair_id: {'branch', '_runs': {member: read_run}}}.  Returns the report body (validity, gates, tests, decision).
    [A50 'Outcome order, final']: 1 NO_RUN; INCOMPLETE (cases/records, tests unread); NUMERICS_UNCERTIFIED / NON_LAPSE;
    then the T-tests are read: 2 the first-applicable decided failure outcome (R1 order); 3 UNDECIDABLE_ROUTE_A_TAIL;
    4 UNDECIDABLE_AT_ITERATION_FLOOR (both undecidable readings listed when both apply); else INCOMPLETE (UNRESOLVED) if a
    step is pending; 5 FLAG_PENDING_RULING; 6 ADOPT_TAIL.  A reading made while a step at an earlier position is pending is
    marked PROVISIONAL, with those steps listed (A48 AMB-17; A50 root item 3)."""
    RP = RP or {}
    packets = packets or {}
    gi = gates.get('I1T', {})
    i1t = {'status': gi.get('status'), 'per': gi.get('derived', {}).get('i1t_per_case') if gi.get('status') in ('PASS', 'FAIL') else None}
    gb0 = gates.get('B0', {})
    extra = b0_extra(gb0)
    c5r = R.get(C5H, {})
    c5h_num = _numerics_of(c5r)
    V = {lab: case_validity(lab, R.get(lab, {'present': False, 'absent': 'NOT_IN_MANIFEST'}), ctx, packets.get(lab), i1t, c5h_num,
                            None, extra) for lab in REGISTERED}
    IV = {n: identity_run_validity(n, IDR.get(n, {'present': False, 'absent': 'NOT_IN_MANIFEST'}), ctx) for n in IDENTITY_RUNS}
    untriggered = rpair_untriggered(RP, R, V, gates, ctx)                                             # [A53 NEW-17]
    if untriggered:
        raise Refused('REFUSED: the manifest names R-PAIR members for %s, whose R-PAIR was not triggered (the base pair is '
                      'decidable): A53 NEW-17 refuses such a manifest at load, before any test is read' % untriggered,
                      'RPAIR_NOT_TRIGGERED_A53_NEW17')
    RPV = {}
    for pid, rp in RP.items():
        runs = rp['_runs']
        # [A50 B1] each R-PAIR member is validated against its partner: C4T-D5@RPAIR:T2 against C5H@RPAIR:T2 (RA1), not the base C5H
        partner_c5h = _numerics_of(runs[C5H]) if (pid == 'T2' and C5H in runs) else None
        for m in sorted(runs, key=lambda x: 0 if x == C5H else 1):
            key = '%s@RPAIR:%s' % (m, pid)
            RPV[key] = case_validity(key, runs[m], ctx, packets.get(key), i1t, partner_c5h if pid == 'T2' else c5h_num,
                                     {'base': m, 'branch': rp.get('branch'), 'base_run': R.get(m, {})}, extra)
        # [A50 B1] [R1 R-PAIR] the registered R-PAIR leaves are byte-equal between the two members
        mems = sorted(runs)
        if len(mems) == 2 and all(runs[x].get('present') for x in mems):
            la_, lb_ = (_rpair_leaf_values(runs[x], rp.get('branch')) for x in mems)
            if la_ != lb_:
                for x in mems:
                    _invalidate(RPV['%s@RPAIR:%s' % (x, pid)], 'RPAIR_LEAVES_NOT_BYTE_EQUAL_BETWEEN_MEMBERS')
        if rp.get('branch') == 'PICARD':          # R6 [r5 recheck order F1] a Picard member's EA entry must be its base's entry
            for x in mems:
                c_ = picard_ea_entry_code(gates.get('EA'), '%s@RPAIR:%s' % (x, pid))
                if c_:
                    _invalidate(RPV['%s@RPAIR:%s' % (x, pid)], c_)
    # [verify D4] aliasing: one result under two registered labels (cases, identity runs, R-PAIR members) is invalid for both
    shas = {}
    for lab, run in list(R.items()) + list(IDR.items()) + [('%s@RPAIR:%s' % (m, pid), x) for pid, rp in RP.items()
                                                            for m, x in rp['_runs'].items()]:
        if run.get('present') and run.get('result_sha256'):
            shas.setdefault(run['result_sha256'], []).append(lab)
    aliased = sorted({lab for labs in shas.values() if len(labs) > 1 for lab in labs})
    for lab in aliased:
        tgt = V.get(lab) or RPV.get(lab)
        if tgt is not None:
            tgt['V1_codes'] = tgt.get('V1_codes', []) + ['ALIASED_RESULT_SHA']
            tgt['failed'] = tgt.get('failed', []) + ['ALIAS']
            tgt['valid_all'] = False
            tgt['reading'] = tgt.get('reading') or 'ALIASED_RESULT_SHA'
        elif lab in IV:
            IV[lab]['codes'] = IV[lab]['codes'] + ['ALIASED_RESULT_SHA']
            IV[lab]['valid'] = False
    rep = {'validity': V, 'identity_runs': IV, 'rpair_validity': RPV, 'gates': {k: {x: y for x, y in g.items() if x != '_record_json'}
                                                                                    for k, g in gates.items()},
           'accepted_route_a_iteration': {lab: V[lab].get('accepted_route_a_iteration') for lab in REGISTERED},
           'c5h_admission_AMB20': ctx['c5h_admission'],
           # [R3 order N2] an invalid R-PAIR member makes only its test INCOMPLETE (contingent members are not registered
           # cases under A47 I1: DECLARED, root to confirm); its per-member next step is named here and in the reading
           'rpair_member_next_steps': {k: next_steps_for_case(v, ctx) for k, v in sorted(RPV.items()) if not v.get('valid_all')}}
    dec = {'outcome': None, 'position': None, 'a50_group': None, 'reasons': [], 'next_step': None, 'tests_read': False,
           'provisional': False, 'marking': None, 'provisional_on': []}
    rep['decision'] = dec

    # ---- [A54 S4] every reading, NO_RUN included, names every missing or invalid case, identity run and gate (A47 I1), with
    # its next step; computed before any reading so that no earlier outcome can hide a case (Claude3 H1-F1)
    inc, nxt = [], {}
    for lab in REGISTERED:
        if not V[lab]['valid_all']:
            inc.append('%s %s reading=%s' % (lab, V[lab]['failed'], V[lab]['reading']))
            nxt[lab] = next_steps_for_case(V[lab], ctx)
    for n in IDENTITY_RUNS:
        if not IV[n]['valid'] or IV[n]['ro1_codes']:
            inc.append('identity run %s invalid or missing %s %s' % (n, IV[n]['codes'], IV[n]['ro1_codes']))
            nxt[n] = 'Run / repair the identity-gate run (gate %s); a second identical failure is a defect for review' % IDENTITY_GATE_OF_RUN[n]
    for g in required_gates(ctx['route_a_mode']):
        if gates.get(g, {}).get('status') == 'MISSING':
            inc.append('gate record %s missing' % g)
            nxt[g] = 'produce the %s record before the T-tests are read (RA13: gates on real records before the seal)' % g
    if ctx['route_a_mode'] == 'parallel8' and gates.get('I4', {}).get('status') == 'FAIL':           # [A47 I4] [verify D7]
        inc.append('I4 FAIL %s: parallel8 route A not licensed' % gates['I4']['codes'])
        nxt['I4'] = I4_NEXT
    defective = [g for g in ALL_GATES if gates.get(g, {}).get('status') == 'RECORD_DEFECT']
    failing = [g for g in ALL_GATES if gates.get(g, {}).get('status') == 'FAIL']                    # R6 (r5 validity F2, NEW-30)
    named = {'cases_identity_runs_and_gates_missing_or_invalid': list(inc),
             'gates_record_defect': ['%s %s' % (g, gates[g]['codes']) for g in defective],
             'gates_failing_reported': {g: {'codes': gates[g]['codes'], 'next_step': gate_fail_next_step(g)} for g in failing},
             'rpair_members_invalid': sorted(k for k, v in RPV.items() if not v.get('valid_all')),
             'next_steps': dict(nxt, **{g: NEXT_STEP['NO_RUN'] + ' (A48 AMB-02: fix the record or gate and re-review)' for g in defective}),
             'rule': 'A54 S4: named at every reading, NO_RUN included (A47 I1)'}
    rep['named'] = named
    dec['named'] = named

    def decide(outcome, reasons, next_step=None, position=None, **kw):
        dec.update(outcome=outcome, position=position or outcome_position(outcome), a50_group=A50_GROUP[outcome], reasons=reasons,
                   next_step=next_step if next_step is not None else NEXT_STEP[outcome], **kw)
        return rep
    # ---- 1 NO_RUN [R1] + AMB-01/AMB-02 (record defects of any gate; RA5 (a) RO1 firing in an identity run)
    nr = ['%s FAIL %s' % (g, gates[g]['codes']) for g in NO_RUN_GATES if gates.get(g, {}).get('status') == 'FAIL']
    nr += ['%s RECORD_DEFECT %s' % (g, gates[g]['codes']) for g in defective]
    nr += ['RA5(a): RO1 fired in identity-gate run %s -> %s fails' % (n, IDENTITY_GATE_OF_RUN[n]) for n in IDENTITY_RUNS
           if IV[n].get('ro1_fired') is True]
    if nr:
        defect = [g for g in ('B2', 'B3') if gates.get(g, {}).get('status') == 'FAIL']
        return decide('NO_RUN', nr, subtype='IMPLEMENTATION_DEFECT_OF_GATE:%s' % defect if defect else None,
                      also_named_missing_or_invalid=list(inc))                                      # [A54 S4]
    # ---- 1 INCOMPLETE [A47 I1]: any registered case / identity-gate run invalid or missing, any required record missing
    if inc:
        return decide('INCOMPLETE', inc, next_step=nxt, subtype='CASES_OR_RECORDS')
    # ---- 1 NUMERICS_UNCERTIFIED / NON_LAPSE_TAIL_MATERIAL [R1] [RA7]
    nu = ['%s FAIL %s' % (g, gates[g]['codes']) for g in CERT_NUMERICS_GATES if gates[g]['status'] == 'FAIL']
    lo = ['%s FAIL %s' % (g, gates[g]['codes']) for g in CERT_LAPSE_GATES if gates[g]['status'] == 'FAIL']
    if nu or lo:                                                                                       # AMB-03: one position
        ns = {k: NEXT_STEP[k] for k, on in (('NUMERICS_UNCERTIFIED', nu), ('NON_LAPSE_TAIL_MATERIAL', lo)) if on}
        return decide('NUMERICS_UNCERTIFIED' if nu else 'NON_LAPSE_TAIL_MATERIAL', nu + lo, next_step=ns,
                      also_named=['NON_LAPSE_TAIL_MATERIAL'] if (nu and lo) else [])
    # ---- T-tests are read from here on
    dec['tests_read'] = True
    rulings = flag_rulings(gates)
    cleared = {k for k, x in rulings.items() if x['disposition'] == 'CLEARED'}
    gmt = gates.get('MT') or {}
    mt_failed = set(gmt.get('derived', {}).get('mt_failed_runs') or []) if gmt.get('status') in ('PASS', 'FAIL') else set()

    def raw_flag(key):
        """[A50 S2] the run's tail record flag, or an MT verdict FAIL for that run."""
        v = V.get(key) or RPV.get(key) or {}
        return bool((v.get('uvt') or {}).get('flagged')) or key in mt_failed

    def eff_flag(key):
        """[A48 AMB-04/19] a run's TAIL_SOURCE_UNDERCONVERGED flag, unless a CLEARED ruling names that run.  A Picard-branch
        R-PAIR member admits its base's route A (V6), so its flag is the base's flag (A50 root item 10)."""
        if '@RPAIR:' in key:
            base, pid = key.split('@RPAIR:', 1)
            if (RP.get(pid) or {}).get('branch') == 'PICARD':
                return eff_flag(base)
        return raw_flag(key) and (FLAG_TSU, key) not in cleared
    T = {}
    t1 = t1_test(*(R[c]['adapted']['rows'] for c in TEST_RUNS['T1']), ctx)
    T['T1'] = apply_flag(t1, [c for c in TEST_RUNS['T1'] if eff_flag(c)])
    T['T1_H'] = evaluate_pair_test('T1_H', R, V, RP, RPV, eff_flag, gates, ctx, TH['T1_H'], True)
    T['T1_S'] = evaluate_pair_test('T1_S', R, V, RP, RPV, eff_flag, gates, ctx, TH['T1_S'], False, per_row=False)  # AMB-06
    if gates['T2I']['status'] != 'PASS':                                                               # [RA3] [A48 AMB-10]
        T['T2'] = {'pair': 'T2', 'status': 'NOT_READ', 'reason': 'T2I %s %s (RA3: read before T2)' % (gates['T2I']['status'], gates['T2I']['codes']),
                   'flagged_runs': [m for m in PAIRS['T2'] if eff_flag(m)]}
    else:
        T['T2'] = evaluate_pair_test('T2', R, V, RP, RPV, eff_flag, gates, ctx, TH['T2'], True)
    T['T2c'] = evaluate_pair_test('T2c', R, V, RP, RPV, eff_flag, gates, ctx, TH['T2c'], False)
    T3a = evaluate_pair_test('T3_KLO', R, V, RP, RPV, eff_flag, gates, ctx, TH['T3'], True)
    T3b = evaluate_pair_test('T3_KHI', R, V, RP, RPV, eff_flag, gates, ctx, TH['T3'], True)
    T['T3'] = {'pairs': {'T3_KLO': T3a, 'T3_KHI': T3b}, 'status': _combine([T3a['status'], T3b['status']])}
    T['RB_FP'] = rb_fp(R, gates, ctx, eff_flag, RP, RPV)                                               # R6 [A56 N2]
    srb_ok, srb_why = srb_rot_readable(gates, ctx)                                                       # [A52.5]
    if srb_ok:
        T['SRB_ROT'] = apply_flag({'status': gates['SRB_ROT']['status'], 'codes': gates['SRB_ROT']['codes'],
                                   'note': 'gate record on the saved C4T state: flag-evaluated on C4T (A50 root item 7)'},
                                  ['C4T'] if eff_flag('C4T') else [])
    else:
        T['SRB_ROT'] = {'status': 'NOT_READ', 'reason': srb_why, 'gate_status': gates['SRB_ROT']['status']}
    T['SR_K'] = sr_k(gates, T['RB_FP'], ctx)
    rep['tests'] = T
    flag_keys = [k for k in list(T_CASES) + sorted(k for k in RPV if (RP.get(k.split('@RPAIR:')[1]) or {}).get('branch') == 'ROUTE_A')
                 if eff_flag(k)]
    raw_flags = [k for k in list(T_CASES) + sorted(RPV) if raw_flag(k)]
    rep['flags'] = {'TAIL_SOURCE_UNDERCONVERGED': raw_flags, 'TAIL_SOURCE_UNDERCONVERGED_unruled': flag_keys,
                    'TAIL_SOURCE_UNDERCONVERGED_from_MT_verdict_FAIL': sorted(mt_failed),
                    'SOURCE_QUADRATURE_MATERIAL': T['SR_K'].get('SOURCE_QUADRATURE_MATERIAL'),
                    'rulings': {'%s:%s' % k: x['disposition'] for k, x in rulings.items()}}
    rep['ro1_recorded'] = {lab: V[lab]['ro1'] for lab in T_CASES if V[lab]['ro1'].get('fired')}
    rep['rows_km_s'] = {lab: R[lab]['adapted']['rows'] for lab in REGISTERED}
    rep['reported'] = reported_items(R, gates, ctx)
    units = {'T1': T['T1'], 'T1_H': T['T1_H'], 'T1_S': T['T1_S'], 'T2': T['T2'], 'T2c': T['T2c'], 'T3_KLO': T3a,
             'T3_KHI': T3b, 'RB_FP': T['RB_FP'], 'SRB_ROT': T['SRB_ROT']}
    st = {u: x['status'] for u, x in units.items()}
    rep['test_status'] = dict(st, T3=T['T3']['status'])
    PASSING = ('PASS', 'PASS_FLAGGED')
    PENDING = ('RPAIR_PENDING', 'INCOMPLETE', 'NOT_READ', 'RECORD_DEFECT', 'MISSING')
    pend = [{'step': u, 'earliest_outcome': UNIT_EARLIEST_OUTCOME[u], 'detail': _pending_detail(units[u])} for u in units if st[u] in PENDING]
    pend += b4_gap_pending(R, units)                                                                  # [A54 B4]
    decided = []                                                                                       # [A48 AMB-17]
    if gates['T2I']['status'] == 'FAIL':                                                               # [A48 AMB-10]
        decided.append(('IMPLEMENTATION_DEFECT', ['T2I fails %s' % gates['T2I']['codes']], T2I_DEFECT_NEXT, 'T2I'))
    elif st['T2'] == 'FAIL':
        decided.append(('IMPLEMENTATION_DEFECT', ['T2 decidable and fails (no flagged run)'], None, 'T2'))
    if st['T2c'] == 'FAIL':
        decided.append(('SOURCE_RULE_MATERIAL', ['T2c fails (> tau/2 on a row)'], None, None))
    k3 = [u for u in ('T3_KLO', 'T3_KHI') if st[u] == 'FAIL']
    if k3:                                                                     # [A54] next step with P read from the case block
        decided.append(('KBIG_NOT_CONVERGED', ['%s decidable and fails' % k3], kbig_next_step(production_kbig(ctx)), None))
    bi = [u for u in ('RB_FP', 'SRB_ROT') if st[u] == 'FAIL']
    if bi:
        decided.append(('BOUND_INSUFFICIENT', ['%s fails' % bi], None, None))
    if st['T1'] == 'FAIL':                                                                             # T1-fail split
        if t1['floor_like']:
            decided.append(('FLOOR_LIKE', ['T1 fails only by a contraction clause %s with Dhat_T(2,3)=%.4g <= 1 and '
                                           'Dhat_T(3,4)=%.4g <= 1' % (t1['fail_by'], t1['Dhat_2_3'], t1['Dhat_3_4'])], None, None))
        else:
            srk = T['SR_K'].get('pairwise_within_quarter_tau')
            t2c = T['T2c']
            split = None
            # [R3 order F1] [A48 AMB-17] with SR_K unavailable, the T2c clause alone can fully decide SRKD (T2c decided,
            # unflagged, with a statistic, > tau/4 on a row rules out NOT_UV_RESIDUAL whatever SR_K reads)
            t2c_decided = (t2c.get('stat') is not None and t2c.get('status') not in PENDING and not t2c.get('flagged_runs'))
            t2c_over = t2c_decided and not all(abs(x) <= TH['NOT_UV_T2c'] for x in t2c['stat']['delta_over_tau'].values())
            if srk is None and t2c_over:
                decided.append(('SOURCE_REPRESENTATION_K_DEPENDENT', ['T1 fails %s; T2c > tau/4 on a row (T2c decided and '
                                                                      'unflagged; SR_K unavailable, not needed: A48 AMB-17)'
                                                                      % t1['fail_by']], None, 'T2c'))
            elif srk is None:
                split = 'T1-fail split (NOT_UV_RESIDUAL vs SOURCE_REPRESENTATION_K_DEPENDENT): SR_K unavailable'
            elif not srk:
                decided.append(('SOURCE_REPRESENTATION_K_DEPENDENT', ['T1 fails %s; SR-K pairwise > tau/4 on a row' % t1['fail_by']],
                                None, None))
            elif t2c.get('stat') is None or t2c['status'] in PENDING:
                split = 'T1-fail split: T2c unavailable'
            elif t2c.get('flagged_runs'):
                split = 'T1-fail split rests on the flagged T2c runs %s (A48 AMB-04)' % t2c['flagged_runs']
            else:
                t2c_q = all(abs(x) <= TH['NOT_UV_T2c'] for x in t2c['stat']['delta_over_tau'].values())
                if not t2c_q:
                    decided.append(('SOURCE_REPRESENTATION_K_DEPENDENT', ['T1 fails %s; T2c > tau/4 on a row' % t1['fail_by']],
                                    None, None))
                elif flag_keys:
                    split = ('T1-fail split: NOT_UV_RESIDUAL requires no TAIL_SOURCE_UNDERCONVERGED flag; unruled %s '
                             '(the split would rest on a flag: A50 root item 5)' % flag_keys)
                else:
                    decided.append(('NOT_UV_RESIDUAL', ['T1 fails %s; T2c <= tau/4 every row; SR-K pairwise <= tau/4; no flag'
                                                        % t1['fail_by']], None, None))
            if split:
                pend.append({'step': 'T1-fail split', 'earliest_outcome': 'NOT_UV_RESIDUAL', 'detail': split})
    if st['T1'] in PASSING and st['T1_H'] == 'FAIL':
        decided.append(('HIGHER_K_DISAGREEMENT', ['T1 passes%s and T1_H fails (> tau/2 on a row)'
                                                  % (' (flag carried: %s)' % T['T1']['flagged_runs'] if st['T1'] == 'PASS_FLAGGED' else '')],
                        None, None))
    if st['T1_S'] == 'FAIL':
        decided.append(('SHAPE_DISAGREEMENT', ['T1_S fails (max |dv|/tau > 2)'], None, None))
    floor = [u for u in ('T1_H', 'T2', 'T3_KLO', 'T3_KHI') if st[u] == 'UNDECIDABLE_AT_ITERATION_FLOOR']
    flagged_failed = [u for u in units if st[u] == 'UNDECIDABLE_FLAGGED']                              # [A48 AMB-04]
    undecidable = (['UNDECIDABLE_ROUTE_A_TAIL'] if flagged_failed else []) + (['UNDECIDABLE_AT_ITERATION_FLOOR'] if floor else [])
    decided.sort(key=lambda d: outcome_position(d[0]))
    rep['decided_readings'] = [d[0] + ('(%s)' % d[3] if d[3] else '') for d in decided]
    rep['undecidable_readings'] = list(undecidable)
    pending = ['%s: %s' % (p['step'], p['detail']) for p in pend]
    rep['pending_steps'] = pending

    def provisional(outcome, with_flagged):
        """[A50] the steps at an earlier position than outcome that are still pending: pending units (and, for a decided
        failure, flagged-undecidable tests whose resolution could still read an earlier outcome: DECLARED, IMPL_R2)."""
        p0 = outcome_position(outcome)
        on = ['%s (could read %s): %s' % (p['step'], p['earliest_outcome'], p['detail']) for p in pend
              if outcome_position(p['earliest_outcome']) < p0]
        if with_flagged:
            on += ['%s (could read %s): UNDECIDABLE_FLAGGED, awaits a flag ruling or the registered rerun'
                   % (u, UNIT_EARLIEST_OUTCOME[u]) for u in flagged_failed if outcome_position(UNIT_EARLIEST_OUTCOME[u]) < p0]
        return {'provisional': bool(on), 'marking': 'PROVISIONAL' if on else None, 'provisional_on': on}
    if decided:                                                                                        # [A50] group 2
        o, why, ns, sub = decided[0]
        return decide(o, why, next_step=ns, subtype=sub, also_decided=rep['decided_readings'][1:],
                      undecidable_readings=undecidable, pending_steps=pending, **provisional(o, True))
    if undecidable:                                                                                    # [A50] groups 3, 4
        o = undecidable[0]
        why, ns = [], {}
        if flagged_failed:
            runs = sorted({r_ for u in flagged_failed for r_ in units[u].get('flagged_runs', [])})
            why.append('flagged tests fail and are undecidable: %s; flagged runs %s; no decided failure outcome applies'
                       % (flagged_failed, runs))
            ns['UNDECIDABLE_ROUTE_A_TAIL'] = 'rerun %s with seed source_rtol/10 (R1)' % runs
        if floor:
            why.append('still undecidable after R-PAIR: %s' % floor)
            ns['UNDECIDABLE_AT_ITERATION_FLOOR'] = NEXT_STEP['UNDECIDABLE_AT_ITERATION_FLOOR']
        return decide(o, why, next_step=ns[o] if len(ns) == 1 else ns, undecidable_readings=undecidable,
                      also_named=undecidable[1:], pending_steps=pending, **provisional(o, False))
    sqm = T['SR_K'].get('SOURCE_QUADRATURE_MATERIAL')
    if sqm is None:
        pend.append({'step': 'SOURCE_QUADRATURE_MATERIAL', 'earliest_outcome': 'FLAG_PENDING_RULING',
                     'detail': 'flag not computable (RB_FP rows absent or kappa undefined)'})
        pending.append('SOURCE_QUADRATURE_MATERIAL flag not computable (RB_FP rows absent or kappa undefined)')
    not_pass = [u for u in units if st[u] not in PASSING and st[u] not in PENDING]
    if pending or not_pass:                                                                            # [A48 AMB-17]
        return decide('INCOMPLETE', ['unresolved: %s' % (pending + ['%s %s' % (u, st[u]) for u in not_pass])],
                      next_step='run the pending R-PAIR / supply the missing input named in the reasons; ADOPT_TAIL and '
                                'FLAG_PENDING_RULING need every step resolved (A48 AMB-17)', subtype='UNRESOLVED',
                      pending_steps=pending, rpair_member_next_steps=rep['rpair_member_next_steps'])
    unruled = []
    if sqm is True and (FLAG_SQM, 'C4T') not in cleared:
        unruled.append(FLAG_SQM)
    unruled += ['%s:%s' % (FLAG_TSU, k) for k in flag_keys]
    if unruled:
        reruns = ['%s on %s: %s' % (k[0], k[1], x['root_decision']) for k, x in rulings.items() if x['disposition'] == 'RERUN_ORDERED']
        return decide('FLAG_PENDING_RULING', ['every gate and test passes; unruled flags %s' % unruled],
                      next_step=NEXT_STEP['FLAG_PENDING_RULING'] + ('; registered reruns ordered: %s' % reruns if reruns else ''))
    if gates['I1T']['status'] != 'PASS' or gates['T2I']['status'] != 'PASS':                           # [verify D1] defensive
        return decide('INCOMPLETE', ['I1T %s / T2I %s' % (gates['I1T']['status'], gates['T2I']['status'])], subtype='UNRESOLVED')
    u = carried_uncertainty(R, T, ctx)
    return decide('ADOPT_TAIL', ['decision rule holds: B-gates, EPS, LO, DOUBLING, GQ, I1T, T2I, SRB_ROT, RB_FP pass; '
                                 'T1, T1_H, T1_S, T2, T2c, T3 pass; no flag unruled'],
                  adopted='cube K=4 tail-corrected (C4T)', carried_numerical_uncertainty_km_s=u['u'], u_over_tau=u['u_over_tau'],
                  u_over_sigma=u['u_over_sigma'], carried_terms=u['terms'])


def _combine(sts):
    """Display status of T3 (the decision reads the two pairs separately): a decided FAIL first (A48 AMB-17)."""
    order = ('FAIL', 'UNDECIDABLE_AT_ITERATION_FLOOR', 'UNDECIDABLE_FLAGGED', 'INCOMPLETE', 'RPAIR_PENDING', 'NOT_READ',
             'PASS_FLAGGED', 'PASS')
    for o in order:
        if o in sts:
            return o
    return 'INCOMPLETE'


def _pending_detail(t):
    if not isinstance(t, dict):
        return t
    if 'pairs' in t:
        return {k: _pending_detail(v) for k, v in t['pairs'].items()}
    d = {'status': t.get('status')}
    for k in ('reason', 'rpair_branch', 'rpair_branch_row', 'rpair_branch_basis', 'flagged_runs'):
        if t.get(k):
            d[k] = t[k]
    return d


def carried_uncertainty(R, T, ctx):
    """[R1 carried_uncertainty_u_i] u_i = |C4T-C3T| + |C6T-C4T| + |S4T-C4T| + SR term + RB-FP_i (km/s)."""
    ids, tau, sig = ctx['ids'], ctx['tau'], ctx['sigma']
    v = {c: R[c]['adapted']['rows'] for c in ('C3T', 'C4T', 'C6T', 'S4T')}
    terms = {'K34': {i: abs(v['C4T'][i] - v['C3T'][i]) for i in ids}, 'K46': {i: abs(v['C6T'][i] - v['C4T'][i]) for i in ids},
             'shape': {i: abs(v['S4T'][i] - v['C4T'][i]) for i in ids},
             'SR': {i: T['SR_K']['SR_term_km_s'][i] for i in ids}, 'RB_FP': {i: T['RB_FP']['rows'][i]['RB_FP_km_s'] for i in ids}}
    u = {i: (None if any(terms[k][i] is None for k in terms) else sum(terms[k][i] for k in terms)) for i in ids}
    return {'u': u, 'u_over_tau': {i: (None if u[i] is None else u[i] / tau[i]) for i in ids},
            'u_over_sigma': {i: (None if u[i] is None else u[i] / sig[i]) for i in ids}, 'terms': terms,
            'labels': {'SR': 'static only; fixed-point UNTESTED, deciding test C4T-SR', 'RB_FP': 'first-order response DECLARED, UNTESTED'}}


def reported_items(R, gates, ctx):
    """[R1 D_m4] v009 harmonic m4 row window, C4T vs C4R3; [RA10] a0/a4/a8 at query 03 (reported, not deciding); [R1 LO_NGC]."""
    out = {}
    c4r3 = ctx.get('c4r3_adapted')
    out['D_m4'] = {'C4T_m4_row_window': R['C4T']['adapted'].get('m4_row_window'),
                   'C4R3_m4_row_window': None if c4r3 is None else c4r3.get('m4_row_window'), 'use': 'reported'}
    h = gates.get('HARMONICS') or {}
    want = ('C4T', 'C4T-D5', 'C6T', 'C4R3', 'C5H', 'C6')
    rows = ((h.get('_record_json') or {}).get('rows')) if h.get('status') == 'PASS' else None
    out['RA10_harmonics'] = {'status': h.get('status', 'MISSING'), 'rows': rows,
                             'cases_missing': [c for c in want if not any(x.get('case') == c for x in (rows or []))],
                             'use': 'reported, not deciding (A42.4 open item)'}
    out['LO_NGC'] = {'status': (gates.get('LO_NGC') or {}).get('status', 'MISSING'),
                     'scope': 'NGC N-tests are not read as passed before LO_NGC passes; not part of the DDO decision'}
    return out


# ============================================================================================ blinded outputs (A47 I3)
# [verify blinding B1] structural backstop: after the source-site enums, every string of a blinded output is scanned for a
# decimal or exponent number (64-hex shas masked first); any such token that is not one of the compare's own code constants
# is replaced by <REDACTED_NUMBER> and the output carries blinding_redaction_applied = true.  Integers in identifiers
# (col0001, C2R3, ROW_05) are not decimals; record-controlled strings reach codes only through _enum / exact labels.
_RE_HEX64 = re.compile(r'[0-9a-f]{64}')
# R5 [A54 S6] (Claude3 H1-F5, H1-N5): a decimal or exponent number is caught WHEREVER it sits, including glued to letters
# (x61.2222222) and with a leading dot (.25); r4's look-behind let a number attached to a letter through.
# R6 [r5 recheck validity F7]: also a trailing-dot number ('61.') and any run of 5 or more digits, glued to letters or not
# ('k412345678'); 64-hex shas are masked first, and no compare code constant carries a 5-digit run.
_RE_NUMBER = re.compile(r'[-+]?(?:\d+\.\d+(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?|\d+[eE][-+]?\d+|\d+\.(?!\d)|\d{5,})')
ALLOWED_NUMBER_TOKENS = ('1e-4', '1e-12', '0.05', '0.005', '0.1', '1.0', '2.0', '64.0', '32.0')


def _blind_str(x, hit):
    masked = _RE_HEX64.sub(lambda m: 'h' * 64, x)            # same length: spans align with x; shas cannot match a number
    res, pos = [], 0
    for m in _RE_NUMBER.finditer(masked):
        if m.group(0) in ALLOWED_NUMBER_TOKENS:
            continue
        a, b = m.span()
        res += [x[pos:a], '<REDACTED_NUMBER>']
        pos = b
        hit.append(True)
    res.append(x[pos:])
    return ''.join(res)


_RE_PATH_SEG = re.compile(r'[A-Za-z_][A-Za-z0-9_]*(?:\[\d+\])?\Z|\d{1,2}\Z|<[a-z_]+(?:\[\d+\])?>\Z')


def blind_path(path):
    """[A54 S6] a record path in a blinded output: every '/'-segment must be a registered identifier (a plain key, a small index,
    a <placeholder>), a registered case / identity-run / gate label or an R-PAIR key; any other (record-controlled) segment is
    replaced by <RECORD_KEY_REDACTED>.  Returns (path, redacted?)."""
    if not isinstance(path, str):
        return '<RECORD_KEY_REDACTED>', True
    segs, red = [], False
    for x in path.split('/'):
        ok = bool(_RE_PATH_SEG.match(x)) or x in REGISTERED or x in IDENTITY_RUNS or x in ALL_GATES or rpair_key_ok(x, REGISTERED)
        segs.append(x if ok else '<RECORD_KEY_REDACTED>')
        red = red or not ok
    return '/'.join(segs), red


def blind_strings(obj, hit):
    if isinstance(obj, str):
        return _blind_str(obj, hit)
    if isinstance(obj, dict):
        # R10 [A71] two keys that blind to one string would keep the last value: the later one is kept under a disambiguated key
        out = {}
        for j, (k, v) in enumerate(obj.items()):
            k2 = _blind_str(k, hit) if isinstance(k, str) else k
            if k2 in out:
                k2 = '%s<BLINDED_KEY_COLLISION_%d>' % (k2, j)
                hit.append(True)
            out[k2] = blind_strings(v, hit)
        return out
    if isinstance(obj, list):
        return [blind_strings(v, hit) for v in obj]
    return obj


def blinded_case(v):
    """Validity booleans and reason codes ONLY (no row value, no number of any kind)."""
    out = {'label': v['label'], 'present': v['present'], 'valid_all': bool(v.get('valid_all')), 'failed': list(v.get('failed', [])),
           'reading': v.get('reading'), 'V1_codes': list(v.get('V1_codes', [])), 'V2_codes': list(v.get('V2_codes', [])),
           'V3_mismatch': list(v.get('V3_mismatch', [])), 'V6_codes': list(v.get('V6_codes', [])),
           'bracket_misses': list(v.get('misses', []) or [])}
    for k in ('V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'I1T'):
        if k in v:
            out[k] = None if v[k] is None else bool(v[k])
    out['ro1'] = {k: (v.get('ro1') or {}).get(k) for k in ('required', 'present', 'fired', 'armed')}
    out['ro1']['event_codes'] = ['%s:%s' % (e['code'], e['refusal']) for e in (v.get('ro1') or {}).get('events', [])]
    out['uvt'] = {k: (v.get('uvt') or {}).get(k) for k in ('required', 'present', 'flagged', 'E_A_row_order')}
    hit = []
    out = blind_strings(out, hit)
    out['blinding_redaction_applied'] = bool(hit)
    assert_no_numbers(out)
    return out


def blinded_gate(g):
    hit = []
    fr = []
    for x in g['fields_read']:                                                                       # [A54 S6]
        y, r_ = blind_path(x)
        fr.append(y)
        if r_:
            hit.append(True)
    xr = {}
    for j, (k, x) in enumerate(g.get('crossref', {}).items()):
        k2, r_ = blind_path(k)
        if r_:
            hit.append(True)
        if k2 in xr:                             # R10 [A71] two crossref fields blinded to one path: both kept (never last-wins)
            k2 = '%s<BLINDED_KEY_COLLISION_%d>' % (k2, j)
            hit.append(True)
        xr[k2] = {'target': x['target'] if (x['target'] in REGISTERED or x['target'] in IDENTITY_RUNS or rpair_key_ok(x['target'], REGISTERED)
                                            or x['target'] is None) else '<RECORD_KEY_REDACTED>',
                  'target_present': x.get('target_present'), 'equal': x.get('equal')}
    out = {'gate': g['gate'], 'status': g['status'], 'codes': list(g['codes']), 'fields_read': fr,
           'record_sha256': (g.get('record') or {}).get('sha256'), 'crossref': xr}
    out = blind_strings(out, hit)
    out['blinding_redaction_applied'] = bool(hit)
    assert_no_numbers(out)
    return out


def assert_no_numbers(obj, where='$'):
    if isinstance(obj, bool) or obj is None or isinstance(obj, str):
        return
    if isinstance(obj, (int, float)):
        raise AssertionError('BLINDING: number at %s' % where)
    if isinstance(obj, dict):
        for k, x in obj.items():
            assert_no_numbers(x, where + '.' + str(k))
        return
    if isinstance(obj, (list, tuple)):
        for j, x in enumerate(obj):
            assert_no_numbers(x, '%s[%d]' % (where, j))
        return
    raise AssertionError('BLINDING: unexpected type at %s' % where)


def finite_or_null(obj, path='$', acc=None):
    """[verify D6] non-finite numbers become null and are named (the report then dumps with allow_nan=False)."""
    if isinstance(obj, bool) or obj is None or isinstance(obj, str):
        return obj
    if isinstance(obj, (int, float, np.integer, np.floating)):
        x = obj.item() if hasattr(obj, 'item') else obj
        if isinstance(x, float) and not math.isfinite(x):
            acc.append(path)
            return None
        return x
    if isinstance(obj, dict):
        # R10 [A71] str(k) of two distinct keys (1 and '1') would collide: refused (an internal invariant of the report)
        return unique_map([(str(k), finite_or_null(v, '%s.%s' % (path, k), acc)) for k, v in obj.items()], 'REPORT', path)
    if isinstance(obj, (list, tuple)):
        return [finite_or_null(v, '%s[%d]' % (path, j), acc) for j, v in enumerate(obj)]
    if isinstance(obj, set):
        return [finite_or_null(v, path, acc) for v in sorted(obj)]
    return str(obj)


# ============================================================================================ field contract (FIELDS.md)
FIELD_CONTRACT = {
    'run_result_json (<run dir>/result.json; driver schema %s)' % RESULT_SCHEMA: [
        ('schema', 'str', 'V1'), ('status', 'str', 'V1 (COMPLETED)'), ('valid', 'bool', 'V1'),
        ('rows[].id, rows[].speed_km_s', 'list', 'V1: exactly the 12 V005 row ids, EACH ONCE (R1, verify D2), finite; test statistics'),
        ('passes[].rows[].id/speed_km_s', 'list', 'A54 S9 (R6): every recorded pass row-set carries exactly the 12 registered row ids, each once (no duplicate, no unknown, none missing; every entry an object with a string id), checked before any dict is built; otherwise RECORD_DEFECT of the run (V1 PASS_ROWS_NOT_EXACTLY_THE_12_REGISTERED_IDS_EACH_ONCE_A54_S9): the case reads INCOMPLETE.  E_i noise allowance: A51 F2 tau-norm bound with q uncapped (A58 RI-18), max with the A54 S7 same-sign per-row bound |d|q_i/(1-q_i) and the A56 N1 alternating per-row bound |d|q_i/(1+q_i); E unavailable when a tau-norm ratio >= 1 (A53 NEW-7) or any row ratio q_i >= 1 (A56 N1) (the last four pass rows = up to three increments; finite, all 12 ids); last pass rows must equal rows'),
        ('passes[].pass', 'int', 'A54 B4: every pass carries a non-empty rows list and passes[k].pass = k + 1 (consecutive from 1); otherwise a record gap: E unavailable (R-PAIR), INCOMPLETE unless an R-PAIR resolves it (R6: the decidability pairs and RB_FP, A56 N2); V2 cross-check needs the last two passes intact.  A pass with no row-set (rows absent, null or []) is a B4 gap; a row-set that is present but not exactly the 12 ids is S9 (R7, r6 recheck order B1: including a present row-set that is not a list -- a dict, {}, a string, a number)'),
        ('passes[-1].max_abs_change_km_s', 'num', 'V2 (<= 0.0125); R1: = max_i |d_last_i| over the 12 rows (verify D9)'),
        ('passes[-1].field', 'str', 'V4/V5 final field packet (via V005 adapt_result)'),
        ('final_pass', 'any', 'read by V005 adapt_result (transitive, verify N1)'),
        ('driver_sha256', 'sha', 'V3 drivers_allowed; = receipt pins.driver.sha256'),
        ('call_spec_sha256', 'sha', 'V3 (C5H: 60b46130); = receipt pins.spec.sha256'),
        ('normalized_spec/galaxy', 'str', 'V3 DDO154'), ('normalized_spec/physical', 'dict', 'V3 = V005 anchor'),
        ('normalized_spec/coefficients', 'dict', 'V3 = V005 anchor'),
        ('normalized_spec/numerics/picard/{passes,speed_change_bound_km_s,observe_every_pass}', 'any', 'V3 (6/0.01/true; R-PAIR Picard 12/0.0025/true)'),
        ('normalized_spec/numerics/brackets', 'dict', 'V3 RA4 block (canonical-JSON equal to C5H spec 60b46130)'),
        ('normalized_spec/numerics/composite_grid_spec', 'dict|null', 'V3 registered grid'),
        ('normalized_spec/numerics/truncation/{shape,kmax_inverse_kpc}', 'any', 'V3'),
        ('normalized_spec/numerics/route_a/max_iterations', 'int', 'V3 = 32 (A47 I5)'),
        ('normalized_spec/numerics/route_a/column_workers', 'int', 'V3 = 8 (route-A mode parallel8) or 1 (serial_with_exemption); C5H 8; an R-PAIR PICARD member (T-case or C5H) 1 (A53: it admits its base route A)'),
        ('normalized_spec/numerics/route_a/ro1_workers', 'bool', 'A52.3/A53: true on a C5H R-PAIR ROUTE_A member; ABSENT on a C5H R-PAIR PICARD member; never on a T-case'),
        ('normalized_spec/numerics (whole)', 'dict', 'V3: T-cases register /numerics WHOLE in the case block (R1, verify S3)'),
        ('normalized_spec/numerics/uv_tail', 'dict', 'V3 via the registered /numerics; the pinned library normalizes it to uv_tail_config_sha256 (verify S4); must be run-invariant'),
        ('normalized_spec/<every pointer in the case block normalized_spec_equal>', 'any', 'V3'),
        ('normalized_spec/numerics/route_a/seed_source_rtol_factor', 'num', 'A48 AMB-14: absent or 1.0 on every run except an R-PAIR ROUTE_A member (= 0.1)'),
        ('route_a_outcome/{result_path,result_sha256}', 'str/sha', 'route-A attempt result (sha from bytes must match); an R-PAIR PICARD member: result_sha256 = its base run\'s (A53 V6)'),
        ('route_a_outcome/classification', 'str', 'V3 = CONVERGED'),
        ('route_a_outcome/converged_iteration', 'int', 'reported accepted iteration (A47 I5); = uv_tail accepted_iteration'),
        ('route_a_outcome/ro1/{rule,fired,events[],armed,worker_sha256,binding_sha256}', 'dict', 'R11 (A77.2, parsed strictly): exactly these keys (plus inadmissible_record when the driver kept one), worker/binding a sha256 or null (an armed block: both shas), a fired block exactly one event, no event twice by (query, phi_rad, R_kpc, refusal), and the serial / parallel kind from a POSITIVE integer column_workers of the admitted attempt; RA5 RO1 record (A48 AMB-15); A49.2: armed true on every ro1_required case (T-cases, the C5H R-PAIR ROUTE_A member) and on Z2 / Z2-OFF (A50 root item 12); B0prime_RERUN (A52.1) and the C5H R-PAIR PICARD member (A53): block REQUIRED with armed false, fired false; a T-case R-PAIR PICARD member: the record equals its base run\'s canonically and the worker kind is the admitted base attempt\'s (A53 R3-4); unarmed (armed false, fired false, worker/binding null) elsewhere; armed: worker_sha256 in the custody list (R7, A62.3: the driver v010 r5 workers, serial fbe9ae79 for column_workers 1, parallel 869ce387 otherwise; on a case whose REGISTERED uv_tail source_rule is nodes_v001, i.e. C4T-D5 and its R-PAIR member, the r5 nodes_v001 RO1 workers instead: serial 0ae245d8, parallel a5277172, R4 validity F1, DECLARED; the r4 workers 9f74d465 / d676ecb2 / dbb331db / 5a4c7d41 are no longer accepted), binding_sha256 = 86af6198 (unchanged by A62.3) (A50 root items 11, 12); events[].{code,refusal,query,phi_rad,R_kpc,numerator,denominator,after_convergence} (each present; query an int or null; phi_rad, R_kpc, numerator, denominator a finite number or null, as the c2v002 binding 86af6198 writes them: R3 validity F1); refusal one of the three EXACT A49.1 texts; after_convergence true; R6 (r5 validity F3): a block carrying the key inadmissible_record (v010 r4 ro1_outcome keeps an inadmissible readout-refusal record there) reads RO1_INADMISSIBLE_RECORD: invalid on every case, identity run and R-PAIR member'),
        ('identity/route_a/custody/identity_sha256', 'sha', 'V6 (R-PAIR PICARD members: = the base run\'s; ROUTE_A members: must differ, order N-c / NEW-16)'),
        ('residual_diagnostics/azimuthal_harmonics/{per_radius_max[].m4, radial_nodes_m}', 'list', 'D_m4 (reported)'),
        ('stage_records[].{name,kind,exit_code,stage_dir}', 'list', 'failure reading (BRACKET_HULL_MISS, route-A readout refusal); name: kept only if on the exact driver-constant allow-list (A50 N1), else STAGE_NOT_ON_ALLOW_LIST'),
        ('reasons[]', 'list of str', 'REFUSED/BLOCKED reason codes (each reason\'s first identifier token; R11, A75 A08: every reason, not only reasons[0]; a reason given twice is named)')],
    'run_side_files': [
        ('<run dir>/finish.json: result_sha256', 'sha', 'V1 custody (= sha256 of result.json bytes)'),
        ('<run dir>.receipt.json: schema', 'str', '= %s; REQUIRED for every run case, identity run and R-PAIR member (A48 AMB-26)' % RECEIPT_SCHEMA),
        ('<run dir>.receipt.json: result.{sha256,path}', 'sha/str', '= sha256 of result.json bytes; path resolves to this result.json'),
        ('<run dir>.receipt.json: pins.{spec,driver}.sha256', 'sha', '= result call_spec_sha256 / driver_sha256'),
        ('<run dir>.receipt.json: driver_status', 'str', '= result status'),
        ('<run dir>.receipt.json: status, exit_code, stop_reason', 'any', 'COMPLETED result: FINISHED, 0, null; stop_reason in {WALL_CAP, RSS_CAP, OUTPUT_CAP}'),
        ('<run dir>/start.json: normalized_spec', 'dict', 'V3/bracket reading of a failed call whose result.json lacks normalized_spec'),
        ('<run dir>/start.json: call_spec_sha256; <run dir>.receipt.json.launch.json: pins.spec.sha256', 'sha', 'test-mode full-mode interlock only (registered C5H call 60b46130 refused before the seal); R6 (r5 validity F1): before any file is read, the realpath of each of result.json, finish.json, start.json, .receipt.json and .receipt.json.launch.json is checked against the registered C5H run (a file-level symlink into it is refused, rc 2), and an audit-hook guard refuses any other open into it during the run'),
        ('<stage_dir>/columns/finish.json: failures[].{index,message}', 'list', 'bracket miss (message contains BRACKET; prefix an upper-case code)'),
        ('<route_a stage_dir>/attempt_*/failure.json: type, message', 'str', 'route-A readout refusal reading (type: identifier)'),
        ('<passes[-1].field>/finish.json: outputs/refreshed_prepared.npz {path, sha256}', 'dict', 'V4/V5 packet (transitive via V005 adapt_result, verify N1)'),
        ('refreshed_prepared.npz members wavevectors, weighted_responses', 'npz', 'V4/V5 (transitive via V005 packet_checks)'),
        ('<passes[-1].rotation>/finish.json: base_K_values_SI', 'any', 'transitive via V005 adapt_result')],
    'route_a_attempt_result (route_a_outcome.result_path): result/uv_tail = %s' % UVT_RA_RECORD_SCHEMA: [
        ('schema', 'str', '= %s' % UVT_RA_RECORD_SCHEMA), ('outcome', 'str', '= CONVERGED_FINITE_FIXED_POINT'),
        ('production_admissible', 'bool', 'true (IA6)'), ('admissibility', 'str', '= production'),
        ('config_sha256', 'sha', '= case block uv_tail_config_sha256'), ('flags', 'list', '[] or [TAIL_SOURCE_UNDERCONVERGED]'),
        ('monitor_status', 'str', 'M_T_WITHIN_THRESHOLD | FLAGGED'), ('M_T_threshold', 'num', '= 0.25'),
        ('M_T_accepted', 'num', 'flag iff > 0.25'), ('accepted_iteration', 'int', '= route_a_outcome.converged_iteration'),
        ('E_A_rows_km_s_accepted', 'list|null', 'E^A_i: 12 values, km/s, row_ids order; USED only with probe_R_m below'),
        ('probe_R_m (optional)', 'num12', 'A48 AMB-22: = the 12 registered row radii (m, row_ids order); absent -> E^A from the EA record')],
}


def gate_field_contract():
    """Gate-record fields read by the g_* functions.  Kept next to the functions; the tests delete each fixed-path field of a
    complete synthetic record and require RECORD_DEFECT naming it, and check that every path a gate reads is listed here."""
    common = [('schema', 'str', '= %s' % GATE_SCHEMA), ('gate', 'str', '= the gate name'),
              ('verdict', 'str', 'the pass verdict below, or a registered failing verdict (A54 S5: FAIL; EPS also EPS_UNCERTIFIED, GQ also UV_TAIL_GAS_QUADRATURE_UNCERTIFIED, I1T also UV_TAIL_SOURCE_MISMATCH); any other verdict is a RECORD_DEFECT; a verdict contradicting the record\'s own data (failing verdict, no failing clause; or pass verdict with a failing data clause; coverage shortfalls excepted) is a RECORD_DEFECT; B0, B0prime_DRY, RB_FP, SR_K, EA, HARMONICS, FLAG_RULINGS carry no recomputed failing clause, so their failing verdict reads FAIL'),
              ('producer/path', 'str', 'producing tool; R10 (A69 note 1): must be the ROOT-REGISTERED path of this producer (registry producers[<gate>][].path, compared by realpath; else RECORD_DEFECT PRODUCER_PATH_NOT_ROOT_REGISTERED_A69_1), and the file\'s BYTES must hash to the registered sha now (else PRODUCER_BYTES_NOT_THE_REGISTERED_SHA_A69_1)'),
              ('producer/sha256', 'sha', 'its sha256; R7 (A62.2): must be ROOT-REGISTERED for this gate in the producer registry (else RECORD_DEFECT PRODUCER_NOT_ROOT_REGISTERED_A62_2; no registry supplied: PRODUCER_REGISTRY_ABSENT_A62_2); a synthetic or fixture record is refused this way'),
              ('(every JSON object and every list the gate maps)', 'any', 'R10 (A71): a duplicate JSON key is a RECORD_DEFECT (GATE_RECORD_UNREADABLE:<gate>:DuplicateKey with DUPLICATE_JSON_KEY_A71:object[i]:members[j]:members[k]:<gate>); a list entry repeating another entry\'s key (a shell range, a roster, a geometry, a (case, stage) build, a spec sha in one set, a (flag, run) ruling, an RB_FP label or range, an EPS shell range) is a RECORD_DEFECT DUPLICATE_ENTRY_A71:<gate>:<list>[i]:<list>[j] naming both entries by index, read before any mapping is built (never last-wins)'),
              ('numbers_producer/{path,sha256} (optional)', 'str, sha', 'R11 (r10 recheck validity N5): when a successor record names the tool that computed its numbers, the file at that absolute path must hash to that sha (else RECORD_DEFECT NUMBERS_PRODUCER_BYTES_NOT_THE_NAMED_SHA_R11; not a registry entry: DECLARED)'),
              ('(the record file itself: sha256 of its bytes)', 'sha', 'R8 (A67 N2): must be one of the gate\'s root-registered records of record, producer registry gate_records[<gate>] (else RECORD_DEFECT GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2; a gate absent from gate_records fails closed), unless root marked the gate %s (bound by its registered producer pin and bytes; SR_K included by A88)' % GATE_RECORD_AFTER_SEAL)]
    ident = [('comparator/{path,sha256}', 'str, sha', 'R7 (A57.3; r6 recheck validity SF4 (b)): the identity comparator the record was built with (c2v004 or its r5 pin-swap successor; A70: c2v006 for the seal); sha in the registry identity_comparators (else RECORD_DEFECT); R10 (A69 note 1, stricter): path = the registered path of that sha and the file bytes hash to it'),
             ('tokens/{path,sha256}', 'str, sha', 'R7 (A59): the token set used (for Z2 the set that REPLACES the base mapping on the new side); sha in the registry identity_tokens[<gate>] (else RECORD_DEFECT); R10 (A69 note 1, stricter): path registered, bytes hashed')]
    G = {
        'B0': [('maps/EXT', 'dict', ''), ('maps/GEO', 'dict', ''), ('spec_sets/{EXT,GEO,NGC}', 'nonempty_list of {label,sha256}', 'GEO must hold 2029f26a.., 4ac5527a..; a used key-equivalence map needs C5H 60b46130 in a set (A48 AMB-13); each C5H R-PAIR member call spec in EXT (A52.3); R10 (A71): a sha listed twice in one set is a RECORD_DEFECT naming both'),
               ('spec_sets/EXT[].{projection_sha256,declared_differences}', 'optional: sha, list', 'A53 r4 validity F1 option (a): REQUIRED on the EXT entry of each C5H R-PAIR member spec: its projection to v009-EXT form, and declared_differences = exactly the pointers of /numerics/route_a/{ro1_workers,seed_source_rtol_factor} the member carries (ROUTE_A both; PICARD none)')],
        'B0prime_DRY': [('files_compared', 'nonempty_list', 'must include DRYRUN_REPORT.json, DRYRUN_PLAN.txt'), ('spec_sets/{EXT,GEO,NGC}', 'nonempty_list', '')],
        'B0prime_RERUN': [('run_result_sha256', 'sha', '= sha of the B0prime_RERUN identity run'), ('reference_result_sha256', 'sha', '= f33eb362.. (v009-GEO deciding (i))'),
                          ('call_spec_sha256', 'sha', '= 4ac5527a..'), ('declared_exceptions', 'list', ''), ('differences_outside_declared', 'list', 'must be []'), ('tail', 'str', '= OFF')] + ident,
        'B0_FA': [('cases/{A1,A2,A4}/status', 'str', '= REFUSED'), ('cases/{A1,A2,A4}/code', 'str', '= ROUTE_A_CHECKPOINT_MISSING')],
        'B1': [('run_result_sha256', 'sha', '= Z2 run'), ('reference_result_sha256', 'sha', '= 883b37a0..'), ('tail', 'str', '= ON'),
               ('outer_K_big_equals_K', 'bool', 'true'), ('precondition_L/verdict', 'str', '= PASS_BITWISE_EQUAL'),
               ('precondition_L/reference_result_sha256', 'sha', '= b76f7afc..'), ('declared_exceptions', 'list', ''), ('differences_outside_custody', 'list', 'must be []')] + ident,
        'B1_OFF': [('run_result_sha256', 'sha', '= Z2-OFF run'), ('reference_result_sha256', 'sha', '= 883b37a0..'), ('tail', 'str', '= OFF'),
                   ('declared_exceptions', 'list', ''), ('differences_outside_custody', 'list', 'must be []')] + ident,
        'B2': [('O_cube_K_out_inverse_kpc', 'num', '= 12'), ('azimuths', 'int', '= 16'),
               ('per_state/{C2R3,C3R3,C4R3}/state_result_sha256', 'sha', 'R3 result shas'), ('per_state/<s>/max_row_diff_km_s', 'num>=0', '<= 1e-4'),
               ('per_state/<s>/sanity_vs_KB12_km_s', 'num>=0', '<= 0.05')],
        'B3': [('independent_lane', 'str', 'Claude3|Claude4'), ('imports_tail_library', 'bool', 'false'), ('state_result_sha256', 'sha', '= C4R3 aac01962..')]
              + [('cases/{cube_O8,cylinder_O8}/%s' % k, 'num>=0', '%s %g' % (op, t)) for k, op, t in B3_TOL]
              + [('cases/{cube_O8,cylinder_O8}/hi_v003_L67_pass', 'bool', 'true')],
        'B0_RO1': [('part_a/identity_runs/{Z2,Z2-OFF,B0prime_RERUN}/result_sha256', 'sha', 'cross-checked'),
                   ('part_a/identity_runs/<run>/ro1_fired', 'bool', 'false'), ('part_b/checkpoint_source', 'str', 'C6 iteration-8 checkpoint'),
                   ('part_b/recorded_code', 'str', '= %s' % RO1_CODE), ('part_b/query', 'int', '= 3'), ('part_b/handed_to_route_b', 'bool', 'true'),
                   ('part_c/cases[].{kind,expected,observed}', 'nonempty_list', 'kinds include OTHER_EXCEPTION, REFUSAL_BEFORE_CONVERGENCE; expected = observed = CALL_FAILED; R11 (A79.1): each kind once (else RECORD_DEFECT naming both cases)')],
        'B0_N3': [('files_scanned', 'nonempty_list of non-empty str', 'R11 (A79.1): each path once'), ('constructions[].{file,line,guarded}', 'nonempty_list', 'all guarded; R11 (A79.1): each (file, line) once (else RECORD_DEFECT naming both)'),
                  ('runtime_checks', 'list', 'includes B0prime_RERUN, B1_OFF')],
        'EPS': [('eps_max', 'num>=0', '>= every eps_refined'), ('evaluator_sha256', 'sha', 'starts f58de0dc'),
                ('coverage_inverse_kpc/DDO', 'range2', '[<=2, >= max(64, sqrt(2) x 2P)] (A54; P = registered C4T K_big = 128 by A55: 362.04)'), ('coverage_inverse_kpc/NGC', 'range2', '[<=2, >=46] (A58 RI-17: ceil(sqrt(2) x 32))'),
                ('shells[].{range_inverse_kpc,eps_base,eps_refined,refinements}', 'nonempty_list', 'eps_refined <= 1.1 eps_base; refinements <= 1 (R1: 2 failures -> EPS_UNCERTIFIED, read strictly); R7 (r6 recheck validity SF4 (a)): the union of the shell ranges covers the declared DDO and NGC coverage without a gap (else RECORD_DEFECT); R10 (A71): one range twice is a RECORD_DEFECT naming both'),
                ('shells[].{eps,eps_envelope,eps_actual_set}', 'optional num>=0', 'R7 (A57.4; validity SF3): when present, eps_max >= every shell eps (the registered per-shell value); envelope_bound.eps_max_envelope_all_shells >= every shell eps_envelope; with dominates_actual_every_shell true, eps_envelope >= eps_actual_set on every shell and the envelope maximum >= eps_max (else RECORD_DEFECT)'),
                ('envelope_bound/{rule,coverage_max_inverse_kpc}', 'optional dict: str, num>=0', 'A52.5 (DECLARED R4 contract): the successor EPS envelope bound; rule = %s; SRB_ROT is read only when present with coverage >= max(64, sqrt(2) x 2P) (A54; P = the registered C4T uv_tail outer.K_big_inverse_kpc); absent -> SRB_ROT NOT_READ (never a defect)' % EPS_ENVELOPE_RULE),
                ('envelope_bound/{eps_max_envelope_all_shells,dominates_actual_every_shell}', 'num>=0, bool (required when envelope_bound is present)', 'R7 (A57.4 "envelope consumers read the full-envelope fields"; validity SF3): SRB_ROT is read only when dominates_actual_every_shell is true; RB_FP keeps eps_max (A52.5, R1 RB_FP; NEW-44)'),
                ('envelope_dominates_actual_every_shell', 'optional bool (top level)', 'R8 (A67 N4; A54 S5): when present, = envelope_bound/dominates_actual_every_shell; a disagreement, or this field with no envelope_bound block, is a RECORD_DEFECT'),
                ('eps_max_envelope_all_shells', 'optional num>=0 (top level)', 'R8 (A67 N4, DECLARED stricter: NEW-53): when present, = envelope_bound/eps_max_envelope_all_shells (exactly); a disagreement, or this field with no envelope_bound block, is a RECORD_DEFECT')],
        'DOUBLING': [('ddo_state_result_sha256', 'sha', '= C4R3'), ('ddo_max_change_over_tau', 'num>=0', '<= 1/20 (max over the K_big values below)'),
                     ('ddo_K_big_inverse_kpc', 'nonempty_list of num', 'R6 (A58 RI-03, DECLARED field): the K_big values doubled; must include P and 2P (128 and 256)'),
                     ('ddo_gas_M_s', 'int', 'R6 (A58 RI-03, A57; DECLARED field): = 128; R10 (A68 CHK-1): = the registered uv_tail gas.M_s of the case block (which must be 128)'),
                     ('ngc_operator_sha256', 'sha', '= e6453d52..'), ('ngc_max_change_over_theta', 'num>=0', '<= 1/20')],
        'GQ': [('rosters[].{roster,k_range_inverse_kpc,M_s,M_s_doubled,nodes,max_abs_diff_over_P0}', 'nonempty_list',
                'roster in DDO_<T-case label> | NGC_T120L; nodes 4096, M_s_doubled = 2 M_s, max <= 1e-12; M_s = 128 on every DDO roster and 96 on NGC_T120L (R6, A57 ruling 1; else RECORD_DEFECT); R10 (A68 CHK-1): every DDO roster M_s = the registered uv_tail gas.M_s of the case block (else RECORD_DEFECT; a superseded M_s 64 certificate refuses in an MS128 context); R10 (A71): one roster (name, geometry, k range) twice is a RECORD_DEFECT; named DDO_C2T and DDO_C3T >= their case\'s registered K_big read from the case block (R7, RA7, validity SF1: 128 at P = 128; never below 32), '
                'DDO_C4T>=max(64, 2P), NGC_T120L>=32 /kpc; per geometry the union of k ranges covers DDO [2, max(64, 2P)], NGC [2,32] (A48 AMB-12, RA7, A54)'),
               ('rosters[].all_nodes/{max_abs_diff_over_P0,nodes}', 'num>=0, int (every DDO roster)', 'R7 (A57.1 "all nodes, not only sampled ones"; validity SF2; DECLARED names = the certificates_v003 full_domain block): max <= 1e-12 (else UV_TAIL_GAS_QUADRATURE_UNCERTIFIED:<roster>:ALL_NODES), nodes >= 4096 (else RECORD_DEFECT); R8 (A67 SF1): nodes = the root-registered production node count of the roster\'s geometry (producer registry gq_all_nodes_counts), and nodes = 4096 (the sample) always refuses (else RECORD_DEFECT)'),
               ('rosters[].geometry', 'str (every DDO roster)', 'R8 (A67 SF1; DECLARED field = the certificates_v003 assembler\'s geometry = the gq_full part record label, e.g. C2T_KB128): a geometry registered in gq_all_nodes_counts (else RECORD_DEFECT); never emitted (A54 S6); R10 (r8 recheck validity SF1, order N1): = the label derived from the roster\'s own kept / outer blocks (C<K>T_KB<K_big>, S<K>T_SPHERE_KB<K_big>, C<K>T-C<K_out>c), and named by ONE DDO roster only (A71) (else RECORD_DEFECT)'),
               ('rosters[].kept/{shape,K_inverse_kpc}, rosters[].outer/{shape,K_big_inverse_kpc | K_out_inverse_kpc}', 'dict (every DDO roster)', 'R10 (r8 recheck validity SF1; DECLARED fields: the certificates_v003 assembler writes them): kept = the roster case\'s kept node set (C2T cube 2, C3T cube 3, C4T and every C4T-* cube 4, C6T cube 6, S4T sphere 4); outer cylinder K_big or cube K_out (integral); the roster k range does not reach above the outer edge (else RECORD_DEFECT)'),
               ('gas_M_s_DDO, source_gas_M_s (top level, optional)', 'int', 'R10 (A68 CHK-1): when present, = the registered uv_tail gas.M_s (else RECORD_DEFECT)'),
               ('gas_M_s_NGC (top level, optional)', 'int', 'R11 (r10 recheck validity note; A57 ruling 1): when present, = the NGC registered M_s 96 (else RECORD_DEFECT)'),
               ('rosters[].roster (semantic identity)', 'str', 'R11 (A79.1, A75.6): each roster NAME once (else RECORD_DEFECT DUPLICATE_ENTRY_A71:GQ:rosters[i]:rosters[j]); every DDO roster carries its fixed-map geometry (DDO_C2T -> C2T_KB<K_big of C2T>, DDO_C3T -> C3T_KB<K_big of C3T>, DDO_C4T -> C4T_KB<2P>; every other DDO_<case> -> its registered case node set) (else RECORD_DEFECT GQ_<roster>_GEOMETRY_NOT_THE_FIXED_MAP_GEOMETRY_A75_6_A79_1); one NGC_T120L roster reaching its registered [2, 32] (AMB-12; a shortfall: GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT, A50 root item 8)'),
               ('rosters[].all_kperp_nodes_bound_over_P0, rosters[].all_nodes/all_kperp_nodes_bound_over_P0', 'optional num>=0', 'R7: when present, <= 1e-12 (else UV_TAIL_GAS_QUADRATURE_UNCERTIFIED:<roster>:ALL_KPERP_NODES)')],
        'LO': [('state_result_sha256', 'sha', '= C4R3'), ('source_gas_M_s', 'int', 'R6 (A57 ruling 1, A58 RI-06; DECLARED field): the M_s of the source the certificate was computed with; = 128; R10 (A68 CHK-1): = the registered uv_tail gas.M_s of the case block (LO_CERT_V003 without it, or an M_s 64 record, refuses in an MS128 context)'),
               ('gas_M_s, tail_config_gas/M_s, build/roster_gas/M_s (optional)', 'int', 'R10 (A68 Records, DECLARED stricter): each, when present, = source_gas_M_s (else RECORD_DEFECT)'),
               ('shells[].{range_inverse_kpc,max_over_tau}', 'nonempty_list', 'R6 (A58 RI-06): the partition (4,5],(5,6],(6,8],(8,12],(12,16],(16,32],(32,64],(64,128],(128,256],(256,363], each present (else RECORD_DEFECT) and <= 0.005; A54: the shells cover [4, max(64, sqrt(2) x 2P)] without a gap (else RECORD_DEFECT) and every other shell <= 0.005; R10 (A71, Codex2 0442 B1): one range listed twice is a RECORD_DEFECT naming both shells (r8 kept the last); R10 (A69 note 2): no shell below K = 4 (else RECORD_DEFECT)'),
               ('summed_max_over_tau', 'num>=0', '<= 0.05')],
        'LO_NGC': [('operator_sha256', 'sha', '= e6453d52..'), ('shells[].{range_inverse_kpc,max_over_theta}', 'nonempty_list', '(2,3],(3,4],(4,6],(6,8],(8,12],(12,16] each <= 0.005; R10 (A71): one range twice is a RECORD_DEFECT naming both; R11 (r10 recheck order N2): EVERY shell the record carries <= 0.005 (an extra or near-alias failing shell reads FAIL) and none below K = 2 (else RECORD_DEFECT)'),
                   ('summed_max_over_theta', 'num>=0', '<= 0.05')],
        'I1T': [('builds[].{case,stage,max_rel,nodes}', 'nonempty_list', 'case = T-case label or <label>@RPAIR:<pair> (every tail build, verify D5); every T-case covered; max_rel <= 1e-12, nodes 4096; R10 (A71): one (case, stage) twice is a RECORD_DEFECT naming both')],
        'T2I': [('case', 'str', '= C5H'), ('region', 'str', '= G5\\G4'), ('c5h_result_sha256', 'sha', 'cross-checked'),
                ('components/{route_a_updated,offset_new_body_fourier_J,feedback_gas_source_feedback}', 'num>=0', '<= 1e-12'), ('max_rel', 'num>=0', '<= 1e-12')],
        'SRB_ROT': [('case', 'str', '= C4T'), ('c4t_result_sha256', 'sha', 'cross-checked'), ('srb_rot_km_s', 'num12>=0', '<= tau_i/10')],
        'RB_FP': [('case', 'str', '= C4T'), ('c4t_result_sha256', 'sha', 'cross-checked'), ('eps_max', 'num>=0', '= EPS eps_max'),
                  ('shells', 'nonempty_list of unique non-empty str labels', 'A54 S6: a label never enters a code or a blinded output (read by index, <shells[j]>)'), ('dV_static_shells_km_s', 'dict', 'R7 (A62.1): its keys are exactly the listed shells'), ('dV_static_shells_km_s/<shells[j]>', 'num12', 'per-shell static tail row effect on saved C4T'),
                  ('shell_ranges_inverse_kpc', 'list of range2, aligned with shells (lo < hi)', 'R7 (A62.1, DECLARED field): the |k| range of each shell; the union covers the C4T tail domain [4, sqrt(2) x P] (P read from the case block; 181.02 at P = 128) without a gap, and no two ranges overlap (else RECORD_DEFECT: a partial-domain record must not PASS); R8 (A67 N3): the lowest edge is exactly 4 and the highest exactly sqrt(2) x P (= math.sqrt(2) * P, the producer\'s float; emitted unrounded: r8 recheck validity N3): an excess or a shortfall is a RECORD_DEFECT; R10 (A69 note 2): a range below K reads RB_FP_SHELL_BELOW_K_A69_2 too; R10 (A71): one range or one label twice is a RECORD_DEFECT naming both'),
                  ('full_tail_domain', 'bool', 'R7 (A62.1): = true (the launch-packet shell producer writes false on a fixture partial domain; else RECORD_DEFECT)')],
        'SR_K': [('states/{C2R3,C3R3,C4R3}', 'sha', 'R3 result shas'), ('Delta_km_s/{2,3,4}', 'num12', 'Delta_i(K); R8 (A67 N2): any two of the three bitwise identical (every row, float.hex) is a RECORD_DEFECT (DECLARED: any pair, stricter than all three; NEW-54); A88: the SR_K record may be registered by sha or PRODUCED_AFTER_THE_SEAL; both require root-registered producer pins and byte verification, and identical-Delta rejection remains unchanged')],
        'EA': [('per_case', 'dict', 'E^A replay per case (A48 AMB-08)'), ('per_case/C5H', 'dict', 'required (C5H has no tail record)'),
               ('per_case/<label>/result_sha256', 'sha', 'cross-checked; label exact: <label> or <label>@RPAIR:<pair>'),
               ('per_case/<label>/E_A_rows_km_s', 'num12>=0', 'E^A_i km/s'), ('per_case/<label>/accepted_iteration', 'int', ''),
               ('per_case/<label>/row_radii_m', 'num12', '= the 12 registered row radii (m, row_ids order; A48 AMB-22)')],
        'MT': [('per_case', 'dict', 'covers every T-case; R-PAIR keys <label>@RPAIR:<pair> optional'), ('per_case/<label>/{result_sha256,M_T_accepted,flags}', 'any', 'flags = [TAIL_SOURCE_UNDERCONVERGED] iff M_T_accepted > 0.25; record verdict PASS iff no run fails, FAIL iff some run fails (A50 S2: that run is flagged); cross-checked against the run tail records')],
        'HARMONICS': [('rows[].{case,source,query,R_kpc,a0,a4,a8,units}', 'nonempty_list', 'RA10 reported (C4T, C4T-D5, C6T, C4R3, C5H, C6); R11 (A79.1): a row is identified by (case, source, query): one given twice is a RECORD_DEFECT naming both')],
        'FLAG_RULINGS': [('rulings[].{flag,run,run_result_sha256,evidence,disposition,reason,root_decision}', 'list',
                          'A48 AMB-19: flag in {TAIL_SOURCE_UNDERCONVERGED, SOURCE_QUADRATURE_MATERIAL}; run = T-case label or R-PAIR key (C4T for SQM); '
                          'disposition CLEARED (reason required) | RERUN_ORDERED; only CLEARED clears; R10 (A71): one (flag, run) ruled twice is a RECORD_DEFECT naming both (r8: the last ruling won)')],
        'I4': [('tail', 'str', '= ON'), ('driver_sha256', 'sha', 'in every T-case drivers_allowed'), ('serial_result_sha256', 'sha', ''),
               ('parallel_result_sha256', 'sha', ''), ('v8c_f1_fix_confirmed', 'bool', 'true'), ('bitwise_equal', 'bool', 'true'),
               ('differences_outside_custody', 'list', 'must be [] (A47 I4; required in route-A mode parallel8)')]}
    return common, G


def _cell(x):
    return str(x).replace('|', '\\|')


def write_field_contract(path):
    if Path(path).exists():                                                                       # [verify blinding NOTE]
        raise Refused('REFUSED: %s exists (the field contract is never overwritten)' % path, 'FIELD_CONTRACT_EXISTS')
    common, G = gate_field_contract()
    L = ['# FIELDS_R12_CX3V002.md: field contract of kmax_tail_compare_c2v007_r12_cx3v002.py (V007 compare R11, Claude2 root lane)', '',
         'Generated by `python3 -I -B kmax_tail_compare_c2v007_r12_cx3v002.py --write-field-contract FIELDS_R12_CX3V002.md` from FIELD_CONTRACT and',
         'gate_field_contract() in the script.  Producers (driver v010, RO1 successors, gate/replay tools) must emit exactly',
         'these names.  A record lacking a field, or carrying the wrong type, makes that gate RECORD_DEFECT (or the case V3',
         'mismatch) with code `FIELD_MISSING:<where>:<path>` / `FIELD_TYPE_<kind>:<where>:<path>` (E-SEAL1 lesson).',
         'Every JSON input is read strictly: a duplicate key is refused (manifest, case block, prereg, registry, build record,',
         'pinned files) or a defect (records).  R10 (A71, no last-wins anywhere): every list the compare turns into a mapping',
         'rejects a repeated key BEFORE the mapping is built, naming both entries by index (DUPLICATE_ENTRY_A71:<where>:<list>[i]:',
         '<list>[j]; a JSON object: DUPLICATE_JSON_KEY_A71:object[n]:members[i]:members[j]); in a gate record that is a RECORD_DEFECT,',
         'in a run record a read code (the run is invalid), in the case block, registry or a pinned input a refusal.  The JSON files',
         'the pinned V005 compare reads by itself (the last pass\'s field and rotation finish.json) are strictly parsed first, and a',
         'field packet whose zip directory repeats a member name reads V4/V5 False (NPZ_DUPLICATE_MEMBER_A71).',
         'Paths are `/`-separated keys; `[]` is a list element; `{a,b}` is each of the named keys; `<x>` is a variable key.', '',
         'Pinned inputs read by the compare itself (not producer fields): REVIEW_V009 3bce7c02 (verdict, blocking_findings,',
         'shas_reviewed.*.sha256), the C5H dry run cbd2885d (call_spec_sha256, driver_sha256, binding_blockers,',
         'remaining_refusals.{unexplained,beyond_pending_inputs}), the reviewed C5 spec 09ff5a96 (diffed against 60b46130), the',
         'DDO154 binding f42c7c65 (query_rows[].{id,radius_m}), the tail library c28d4209 (normalize_config), the dry run',
         'normalized_spec.numerics (A50 S1 reference of the C5H run), and the RO1 custody files (sha256 only; R7, A62.3: the',
         'driver v010 r5 cascade, workers fbe9ae79 / 869ce387, binding 86af6198 unchanged; A50 root items 11, 12; and the r5',
         'nodes_v001 RO1 workers 0ae245d8 / a5277172, accepted only on a case whose registered uv_tail source rule is nodes_v001:',
         'R4 validity F1), the driver v010 r5 b5cc62af and the r5 cascade map a7281e10 (declared_sha_map: each pin is the r5 image',
         'of the r4 sha it replaces; the binding is not remapped).', '',
         'R-PAIR members (manifest `rpair`): each member is validated against its base run (only the registered R-PAIR leaves',
         'may differ: PICARD picard.{passes,speed_change_bound_km_s} and route_a.column_workers = 1 (A53); ROUTE_A',
         'route_a.seed_source_rtol_factor = 0.1) and its partner (those leaves byte-equal; C4T-D5@RPAIR:T2 RA1-equal to',
         'C5H@RPAIR:T2).  A53: a PICARD member ADMITS its base run\'s route A: route_a_identity_sha256 and',
         'route_a_outcome.result_sha256 equal the base\'s (V6), its route-A tail record equals the base\'s, a T-case member\'s RO1',
         'record equals the base\'s canonically (worker kind from the admitted attempt), and the C5H PICARD member carries no',
         'route_a.ro1_workers and an ro1 block armed false, fired false.  A ROUTE_A member recomputes route A (own identity,',
         'order N-c / NEW-16); the C5H ROUTE_A member carries route_a.ro1_workers true and runs armed (A52.3).  A C5H member runs',
         'v010 tail OFF: driver in the C4T-D5 drivers_allowed, B0 covering 60b46130 (A50 B1, root item 11), its own call spec in',
         'the B0 EXT set with projection_sha256 and declared_differences (A53 r4 validity F1 option (a)).  A53 NEW-17: a manifest',
         'naming R-PAIR members for a pair whose base is decidable is REFUSED at load (full mode; rc 2, no report).', '',
         'R6 (A56 N2): RB_FP has a PICARD R-PAIR, manifest key RB_FP, members C4T and C4T-A (`C4T@RPAIR:RB_FP`,',
         '`C4T-A@RPAIR:RB_FP`, 12-pass reruns admitting their base route A, under every A53 PICARD rule above).  It is named only when',
         'the E of C4T or C4T-A is unavailable (NEW-17 otherwise); RB_FP is then read on the two members (rows and E).  Each member',
         'run is its own directory (one run under two labels is ALIAS).  R6 (r5 recheck order F1): a PICARD member reads its base\'s',
         'EA entries only; an EA entry `<label>@RPAIR:<pair>` for a PICARD member must equal its base\'s entry outside result_sha256',
         '(else the member is invalid, RPAIR_PICARD_MEMBER_EA_ENTRY_NOT_THE_BASE_ENTRY_A53).  R6 (r5 recheck order N4, recorded):',
         'B0 EXT evidence that is partial (one of projection_sha256 / declared_differences) is a B0 RECORD_DEFECT (NO_RUN), while',
         'absent evidence makes only the member invalid (INCOMPLETE); both fail closed.', '',
         'Identity runs (A50 root item 12, A52.1): Z2 and Z2-OFF (= Z2_OFF_RO1, spec 894e5b3a) carry ro1 armed true, fired false,',
         'worker/binding on the custody list; B0prime_RERUN (spec 4ac5527a, admitted route A) carries ro1 armed false, fired false.',
         'A fired armed identity run reads NO_RUN (RA5 (a)) and carries RO1_FIRED_IN_IDENTITY_RUN (A53 r4 validity F3).',
         'R8 (A67 N1): every identity run (Z2, Z2-OFF, B0prime_RERUN) carries result driver_sha256 = b5cc62af.. (driver v010 r5;',
         'the receipt driver pin equals it); otherwise the run is invalid (%s).' % IDENTITY_DRIVER_CODE, '',
         'Generic T3 (A54): P = the registered C4T uv_tail outer.K_big_inverse_kpc; C4T-KLO registers K_big = P/2 and C4T-KHI',
         'K_big = 2P (the R1 labels C4T-K16 / C4T-K64 are retired); every other T-case K_big = P except C4T-C5c (cube K_out 5);',
         'EPS and LO coverage >= max(64, sqrt(2) x 2P); the case block is refused otherwise (A54 S8 content rules below).',
         'R6: P = PRODUCTION_K_BIG_A55 = 128 (A55, A56 follow-up 1): C4T-KLO 64, C4T-KHI 256, coverage 362.04; every T-case uv_tail',
         'gas.M_s = 128 (A57 ruling 1; read on C4T, equal elsewhere by S8).', '',
         'R7 (A62.2; r6 recheck validity SF4 (b)), R8 (A67 SF1, N2) and R10 (A69 note 1, NEW-52, A71): the PRODUCER REGISTRY,',
         'root-registered (pinned at the seal as PIN_PRODUCER_REGISTRY; in test mode `--test-producer-registry FILE`), schema',
         '%s: keys `schema`,' % PRODUCER_REGISTRY_SCHEMA,
         '`producers` {gate name: [{path, sha256} of a registered producer tool]}, `identity_comparators` [{path, sha256}],',
         '`identity_tokens` {B1, B1_OFF, B0prime_RERUN: [{path, sha256}]} (R10, A69 note 1: every file is hashed from bytes at',
         'load, a missing file or wrong sha REFUSES the registry, and again at every gate read), `gate_records` {gate name: [sha256',
         'of a registered record of record (file bytes)] or the string %s} (R8, A67 N2; R10, NEW-52: the string is accepted only' % GATE_RECORD_AFTER_SEAL,
         'for %s; every other gate still requires a registered record sha), `gq_all_nodes_counts`' % ', '.join(GATE_RECORD_AFTER_SEAL_ALLOWED),
         '{geometry label: production node count, an int > 4096} (R8, A67 SF1: root takes them from the gq_full part records),',
         'optional `note`; unknown keys, a missing required key, a duplicate key or a duplicate list entry are REFUSED.',
         'Every gate record\'s producer/sha256 must be listed for its gate (SR_K and every replay gate included), and the record',
         'itself must be listed in gate_records for its gate (unless the gate is marked %s); a synthetic or fixture' % GATE_RECORD_AFTER_SEAL,
         'record is a RECORD_DEFECT, which reads NO_RUN (A48 AMB-02; R8, r7 recheck order N1: the r7 wording named a second,',
         'per-gate reading that had no case in the code).  The identity gates\' comparator/sha256 and tokens/sha256 must be listed too.  With',
         'no registry every gate record is a RECORD_DEFECT (fail closed).  R7 (A62.3): every T-case drivers_allowed is exactly',
         '[b5cc62af.. v010 r5]; R10 (A72): exactly [the sealed driver of the active driver build].', '',
         'R10 (A72): the DRIVER BUILD record (pinned at the seal as PIN_DRIVER_BUILD_RECORD; in test mode `--test-driver-build-record',
         'FILE`, or the built-in r5 set when none is given), schema %s: keys `schema`, `build` (r5 | r6, anything' % DRIVER_BUILD_SCHEMA,
         'else REFUSED), `predecessor` (r4 for r5, r5 for r6), `predecessor_shas` {driver, worker, worker_parallel, nodes_worker,',
         'nodes_worker_parallel}, `driver`, `cascade_map` {path, sha256}, `ro1_custody` {worker, worker_parallel, binding} and',
         '`ro1_nodes_custody` {worker, worker_parallel} of {path, sha256}, optional `check_record` {path, sha256} (required in sealed',
         'mode: the independent check of that build) and `note`.  r5 must equal the A62.3 pins; r6 must be the pin-only image of r5',
         '(predecessor shas = r5, binding 86af6198 unchanged, a new %s, files under the driver_r6 tree or the unchanged r5' % DRIVER_FILE_NAME,
         'file, the cascade map declared_sha_map mapping each changed r5 sha to its r6 image).  Every sha is hashed from bytes.  The',
         'active build supplies the T-case drivers_allowed, the I4 driver, the A67 N1 identity-run driver and the RO1 custody lists.', '',
         'R12 (A91): duplicate-key JSON check_record bytes refuse BEFORE text fallback, naming both object/member positions;',
         'driver_build_codes propagates the defect and activate_driver_build preserves the naming in blinded refusal output.',
         'Legitimate text-format PASS controls retain NEW-73 behavior. Duplicate NPY headers name npz_members[i] and both',
         'header_keys[first]/header_keys[repeat] positions. No record-controlled key text is emitted.', '',
         'R10 (A68 CHK-1): the LO, GQ and DOUBLING certificates are bound to the REGISTERED uv_tail gas.M_s of the case block',
         '(cases.C4T normalized_spec_equal./numerics.uv_tail.gas.M_s, which must be the A57 production 128): an M_s 64 certificate',
         'refuses in an MS128 context, and a direct gate call with an M_s 64 context refuses too.', '',
         'R10 (Codex2 0442 S1): in --validity-only and --gates-only an early refusal prints only its fixed refusal code on stderr',
         '(`REFUSED: <CODE> (blinded mode: refusal detail withheld ...)`), never record-controlled input; any other exception there',
         'prints `REFUSED: INTERNAL_EXCEPTION:<type>`, rc 2.', '',
         'R10 (Claude3 0065 H-07): the C5H interlock (test-mode full mode) also refuses a /.vol (by-inode) path, a path any ancestor',
         'of which is a registered run directory by (st_dev, st_ino), and a multiply-linked regular file on the registered run\'s',
         'device (a possible hard link into it; the run directory is never listed), and an interlock marker (start.json, the launch',
         'record) that is unreadable or carries a duplicate key (A75 S01).  The CLI refuses a repeated option, a repeated --case label',
         'and an abbreviated option (A71: argparse would keep the last).', '',
         'R10 (A75.1 A05, A75.6): a named GQ roster reach (DDO_C2T, DDO_C3T, DDO_C4T, NGC_T120L) is met by ONE roster that spans from its',
         'case\'s kept K (NGC: 2) to the reach and, for the DDO names, carries the fixed-map geometry DDO_C2T -> C2T_KB<K_big of C2T>,',
         'DDO_C3T -> C3T_KB<K_big of C3T>, DDO_C4T -> C4T_KB<2P> (else GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT); same-name rosters are never',
         'merged.  R10 (A77.2): every RO1 record follows the role table of its case family: DDO cases the r5 workers fbe9ae79 (serial) /',
         '869ce387 (parallel), C4T-D5 and its R-PAIR member the nodes_v001 workers 0ae245d8 / a5277172, binding 86af6198 for both; serial or',
         'parallel by the admitted attempt\'s column_workers (a Picard member: its base\'s, A53); any other worker or binding (the NGC',
         'workers b6c4586d / ee0510df, the NGC binding 52dc4065) makes the run invalid.  Under an r6 build the r6 images apply (A72).', '',
         'R11 (A79.1, semantic identity): every duplicate guard keys on the entry\'s SEMANTIC identity, never on whole-object equality:',
         'a GQ roster by its NAME (one roster per name; the fixed roster -> geometry map applies to EVERY roster, required or extra:',
         'DDO_C2T -> C2T_KB<K_big of C2T>, DDO_C3T -> C3T_KB<K_big of C3T>, DDO_C4T -> C4T_KB<2P>, and every other DDO_<case> -> the',
         'node set its case registers in the case block; a mismatch is a RECORD_DEFECT; one NGC_T120L roster, reaching its registered',
         'range [2, 32] (A48 AMB-12; a shortfall reads FAIL, A50 root item 8)); a B0_RO1 part_c case by its kind; a B0_N3 construction by (file, line) and a scanned file by its path; a',
         'HARMONICS row by (case, source, query); an RO1 event by (query, phi_rad, R_kpc, refusal) (a fired block carries exactly one',
         'event, as driver v010 ro1_outcome writes it).  R11 (A79.2): the command line is parsed by a parser whose error() raises a',
         'coded refusal (CLI_<CATEGORY>_A79_2; argv text is never printed, in any mode), abbreviations are off, a repeated option is',
         'refused naming both argv positions, help / usage is never printed in a blinded mode, and --case is a --validity-only',
         'option only.  R11 (A79.3, A79.5): the C5H path guard refuses every path when a registered run directory cannot be',
         'stat\'ed (C5H_REGISTERED_RUN_IDENTITY_UNAVAILABLE_A79_3; full test mode refuses at start), compares NFC forms, reads a',
         'leading // as /, and resolves the path itself in kernel order (a symlink is followed before a later ..), checking the',
         'registered name, /.vol and the registered (st_dev, st_ino) at every resolved prefix before touching its child, then',
         'stat-walks every prefix of realpath(path); nothing inside the registered run is stat\'ed or opened.  R11 (A79.4): a field',
         'packet is read once (its bytes must hash to the recorded sha), and before NumPy loads it: a raw member name twice',
         '(NPZ_DUPLICATE_MEMBER_A71), two members behind one NumPy logical key (NPZ_LOGICAL_NAME_COLLISION_A79_4), a member name',
         'not ending in .npy (NPZ_EXTENSIONLESS_MEMBER_A79_4) and every member\'s NPY header failing the strict audit (magic, version,',
         'a dict literal with exactly descr / fortran_order / shape, no key twice) read V4/V5 False.  R11 (A79.6 / A75.3): every',
         'duplicate refusal names both entries by index or JSON path (DUPLICATE_ENTRY_A71 / DUPLICATE_JSON_KEY_A71 position codes,',
         'printed in blinded modes too; they carry indices and constant list names only).', '']

    n = 1
    for sec, rows in FIELD_CONTRACT.items():
        L += ['## %d. %s' % (n, sec), '', '| path | kind | read for |', '|---|---|---|']
        L += ['| `%s` | %s | %s |' % (p_, _cell(k), _cell(w)) for p_, k, w in rows]
        L.append('')
        n += 1
    L += ['## %d. Case block (`--case-block` or prereg binding_inputs.case_block {path, sha256}), schema %s' % (n, CASE_BLOCK_SCHEMA), '',
          '| path | kind | rule |', '|---|---|---|',
          '| `schema` | str | = %s |' % CASE_BLOCK_SCHEMA, '| `route_a_mode` (optional) | str | parallel8 / serial_with_exemption; must equal the compare parameter |',
          '| `cases/<label>` for exactly %s | dict | |' % ', '.join(REGISTERED),
          '| `cases/<label>/grid` | str | %s |' % ', '.join('%s=%s' % kv for kv in EXPECTED_GRID.items()),
          '| `cases/<label>/truncation` | dict | cube/null; S4T sphere/4.0 |',
          '| `cases/<label>/drivers_allowed` | list of sha | C5H: [999331af.. v009-EXT]; every T-case exactly [b5cc62af.. v010 r5] (R7, A62.3, A58 RI-01) |',
          '| `cases/<label>/tail`, `ro1_required` | bool | true for T-cases, false for C5H |',
          '| `cases/<label>/uv_tail_config_sha256` | sha | T-cases; = pinned-library normalize_config(registered uv_tail).sha256 = route-A record config_sha256 |',
          '| `cases/<label>/call_spec_sha256` | sha | C5H only: 60b46130.. |',
          '| `cases/<label>` keys | case-entry key allow-list | R11 (r10 recheck validity N4): T-cases %s; C5H %s (any other key REFUSES the case block) |'
          % ('/'.join(CASE_ENTRY_KEYS_T), '/'.join(CASE_ENTRY_KEYS_C5H)),
          '| `cases/<label>/normalized_spec_equal` | {pointer: value} | T-cases: must register `/numerics` WHOLE; R6: C4T uv_tail gas.M_s = 128 (A57) and K_big P = 128 (A55); registered numerics pairwise distinct; uv_tail distinct for %s; seed_source_rtol_factor absent or 1.0; C4T-D5 `/numerics` = the C5H spec 60b46130 numerics as normalized by its dry run cbd2885d, except composite_grid_spec, uv_tail (route_a.column_workers in serial_with_exemption) and mapped keys (RA1, A50 S1); A54 S8: composite_grid_spec = the registered grid, truncation as the prereg, uv_tail enabled and lapse_only, source_rule continuum_v001 (C4T-D5: nodes_v001 with ext_grid = G5), outer cylinder K_big P (C4T-KLO P/2, C4T-KHI 2P; C4T-C5c cube K_out 5), lambda_scale 1.0 (C4T-A 1.05), every other uv_tail key equal to C4T\'s |'

          % ', '.join('%s/%s' % ab for ab in UV_TAIL_MUST_DIFFER),
          '| `key_equivalence_map` (optional) | list of {pointer, absent_equivalent_value, b0_identity_evidence} | A48 AMB-13: a v010-added /numerics key dropped from the C4T-D5 vs C5H equality only when C4T-D5 carries exactly that value and C5H lacks it or equals it; B0 must cover 60b46130 |', '']
    n += 1
    L += ['## %d. Manifest (`--manifest`), schema %s' % (n, MANIFEST_SCHEMA), '', '| key | value |', '|---|---|',
          '| `cases` | {label: run dir} for the labels above (missing label -> INCOMPLETE) |',
          '| `identity_runs` | {Z2, Z2-OFF, B0prime_RERUN: run dir} |',
          '| `gates` | {gate name: record path}; names: %s |' % ', '.join(ALL_GATES),
          '| `rpair` (optional) | {pair id in %s: {branch: PICARD or ROUTE_A, members: {label: run dir}}}; RB_FP (A56 N2): PICARD only, members C4T and C4T-A, named only when the E of C4T or C4T-A is unavailable |' % ', '.join(RPAIR_MANIFEST_IDS), '',
          'Unknown keys, labels or gate names, and duplicate keys, are REFUSED.', '',
          'Producer notes (R3, from the R2 recheck): each R-PAIR pair needs its OWN member runs (one run directory named by two',
          'pairs is one result under two labels: ALIAS, invalid for both; order N3).  Supply the MT record only when every T-case',
          'run exists (an MT record cannot cover an absent case: it is a RECORD_DEFECT, NO_RUN, which hides the case-level',
          'INCOMPLETE next step; order N6).  In test mode, full mode refuses any manifest slot (cases, identity_runs, rpair',
          'members) whose run is the registered C5H run by name, launch record or start.json call spec (validity F2).', '',
          'Producer notes (R4, from the R3 recheck): the name check is case-insensitive and a directory that is the registered',
          'C5H run directory under another name is refused by os.stat identity (validity F5).  A ROUTE_A-branch R-PAIR member',
          'recomputes route A (seed source_rtol/10): its result route_a_identity_sha256 must differ from its base run\'s (order',
          'N-c).  C4T-D5 and its R-PAIR member run the nodes_v001 RO1 workers; every other case the continuum ones (validity F1).',
          'The B1_OFF and B0prime_RERUN gate producers must declare, in their records, the RO1-worker differences of the run',
          'against its v009 reference (validity F3; not read by the compare: a producer declaration for root).', '']
    n += 1
    L += ['## %d. Gate records (one JSON file per gate; schema %s)' % (n, GATE_SCHEMA), '', 'Common fields (every gate):', '',
          '| path | kind | rule |', '|---|---|---|'] + ['| `%s` | %s | %s |' % (a, _cell(b), _cell(c)) for a, b, c in common] + ['']
    groups = {'NO_RUN group (FAIL -> NO_RUN)': NO_RUN_GATES, 'NUMERICS_UNCERTIFIED group': CERT_NUMERICS_GATES,
              'NON_LAPSE_TAIL_MATERIAL group': CERT_LAPSE_GATES, 'other required': OTHER_REQUIRED_GATES,
              'route-A mode gate (required in parallel8; FAIL -> INCOMPLETE with the A47 I4 next step)': MODE_GATES,
              'optional / reported': OPTIONAL_GATES}
    for gname, members in groups.items():
        L += ['### %s' % gname, '']
        for g in members:
            L += ['#### %s (pass verdict `%s`)' % (g, GATE_PASS_VERDICTS[g]), '', '| path | kind | rule |', '|---|---|---|']
            L += ['| `%s` | %s | %s |' % (a, _cell(b), _cell(c)) for a, b, c in G[g]]
            L.append('')
    Path(path).write_text('\n'.join(L) + '\n')


# ============================================================================================ table and CLI
def table_text(rep, ctx):
    ids = ctx['ids']
    order = ('C2T', 'C3T', 'C4T', 'C6T', 'S4T', 'C4T-D5', 'C4T-C5c', 'C4T-KLO', 'C4T-KHI', 'C4T-A', 'C5H')
    rows = rep.get('rows_km_s') or {}
    L = ['row  tau_i  ' + ''.join('%10s' % c for c in order)]
    for i, rid in enumerate(ids):
        L.append('%s %6.3f  ' % (rid[-2:], ctx['tau'][rid]) + ''.join(('%10.4f' % rows[c][rid]) if c in rows else '%10s' % '-' for c in order))
    return '\n'.join(L) + '\n'


def load_strict_file(path, what):
    tag = re.sub(r'[^A-Z]+', '_', what.upper()).strip('_')
    try:
        return loads_strict(Path(path).read_bytes())
    except DuplicateKey as exc:
        raise Refused('REFUSED: %s has a duplicate JSON key (verify D8; %s)' % (what, exc.code), '%s_DUPLICATE_JSON_KEY_A71' % tag,
                      exc.code)                                                       # R11 [A79.6] both members named
    except (OSError, ValueError) as exc:
        raise Refused('REFUSED: %s unreadable (%s)' % (what, type(exc).__name__), '%s_UNREADABLE' % tag)


def load_manifest(path):
    m = load_strict_file(path, 'manifest')
    if not isinstance(m, dict) or m.get('schema') != MANIFEST_SCHEMA:
        raise Refused('REFUSED: manifest schema must be %s' % MANIFEST_SCHEMA, 'MANIFEST_SCHEMA')
    extra = set(m) - {'schema', 'cases', 'identity_runs', 'gates', 'rpair', 'note'}
    if extra:
        raise Refused('REFUSED: unknown manifest keys %s' % sorted(extra), 'MANIFEST_UNKNOWN_KEYS')
    for key, allowed in (('cases', REGISTERED), ('identity_runs', IDENTITY_RUNS), ('gates', ALL_GATES), ('rpair', RPAIR_MANIFEST_IDS)):
        if not isinstance(m.get(key) or {}, dict):
            raise Refused('REFUSED: manifest %s must be an object' % key, 'MANIFEST_%s_NOT_AN_OBJECT' % key.upper())
        bad = sorted(set(m.get(key) or {}) - set(allowed))
        if bad:
            raise Refused('REFUSED: unknown %s %s' % (key, bad), 'MANIFEST_UNKNOWN_%s' % key.upper())
    for pid, rp in (m.get('rpair') or {}).items():
        if not isinstance(rp, dict) or rp.get('branch') not in ('PICARD', 'ROUTE_A') or set(rp.get('members') or {}) != set(PAIRS[pid]):
            raise Refused('REFUSED: rpair %s must name branch PICARD|ROUTE_A and members %s' % (pid, PAIRS[pid]), 'MANIFEST_RPAIR_ENTRY')
        if pid == RPAIR_RB_FP and rp.get('branch') != 'PICARD':                                       # R6 [A56 N2]
            raise Refused('REFUSED: rpair RB_FP is a PICARD R-PAIR only (A56 N2: the Picard path of C4T / C4T-A)', 'MANIFEST_RPAIR_RB_FP_NOT_PICARD')
    # R11 (Claude3 0072 NOTE, helper K): every run directory and gate path is a non-empty string (or null: absent); a number, a list
    # or an object is refused here with a fixed code (r10: INTERNAL_EXCEPTION:TypeError in the blinded modes, an uncaught TypeError
    # in full mode, or the misleading interlock text for a case directory)
    slots = [v for key in ('cases', 'identity_runs', 'gates') for v in (m.get(key) or {}).values()]
    slots += [v for rp in (m.get('rpair') or {}).values() for v in ((rp or {}).get('members') or {}).values()]
    if not all(v is None or (isinstance(v, str) and v) for v in slots):
        raise Refused('REFUSED: MANIFEST_PATH_NOT_A_STRING_R11 (every run directory and gate path must be a non-empty string or null)',
                      'MANIFEST_PATH_NOT_A_STRING_R11')
    return m


NPY_MAGIC = b'\x93NUMPY'
NPY_HEADER_KEYS = ('descr', 'fortran_order', 'shape')                  # numpy format: the header dict carries exactly these keys
NPY_VERSIONS = {1: (2, 'latin1'), 2: (4, 'latin1'), 3: (4, 'utf8')}    # numpy _header_size_info: length bytes, encoding


def npz_member_index_codes(names):
    """R11 [A79.4] (Codex2 0456 / CX2-R10-A71-B1; r10 recheck order B1; helper I R-2): the member-name checks of an NPZ archive, made
    on the ZIP directory before NumPy maps anything.  numpy 2.3.5 NpzFile (the pinned runtime, _npyio_impl L198-201) exposes
    files = [n.removesuffix('.npy')] and looks a key up in {logical -> raw} updated by {raw -> raw}: a key two different members
    answer to is a collision even when the raw names differ (weighted_responses.npy and an extensionless weighted_responses: NumPy
    reads the extensionless one).  Returns [] or the codes, each naming both members by index (A79.6):
      NPZ_DUPLICATE_MEMBER_A71:npz_members[i]:npz_members[j]        a raw name twice (the r10 code);
      NPZ_LOGICAL_NAME_COLLISION_A79_4:npz_members[i]:npz_members[j]  two members behind one NumPy key;
      NPZ_EXTENSIONLESS_MEMBER_A79_4:npz_members[i]                   a member whose name does not end in '.npy' (refused outright)."""
    out = []
    d = unique_keys_codes(names, 'PACKET', 'npz_members')
    out += ['NPZ_DUPLICATE_MEMBER_A71:%s' % c.split(':', 2)[2] for c in d]
    keymap = {}
    for j, nm in enumerate(names):                       # NumPy's own order: logical names first, then raw names override
        keymap.setdefault(nm[:-4] if nm.endswith('.npy') else nm, []).append(j)
    for j, nm in enumerate(names):
        keymap.setdefault(nm, []).append(j)
    seen = set()
    for key, js in keymap.items():
        u = sorted(set(js))
        if len(u) > 1 and tuple(u[:2]) not in seen and not d:
            seen.add(tuple(u[:2]))
            out.append('NPZ_LOGICAL_NAME_COLLISION_A79_4:npz_members[%d]:npz_members[%d]' % (u[0], u[1]))
    out += ['NPZ_EXTENSIONLESS_MEMBER_A79_4:npz_members[%d]' % j for j, nm in enumerate(names) if not nm.endswith('.npy')]
    return out


def npy_header_audit_code(z, info, i):
    """R11 [A79.4 'the strict header audit everywhere'] (A74.1 class): EVERY member's NPY header, whatever its name, parsed as numpy
    would but strictly: the NPY magic, a known version (1.0 / 2.0 / 3.0, numpy's length size and encoding), the declared length
    present, a dict LITERAL (AST only; nothing evaluated beyond literal_eval of a node already checked) whose keys are string
    constants, none twice (numpy's literal_eval keeps the last), and exactly descr / fortran_order / shape.  None, or one code naming
    the member by index; R12 A91 duplicates append header_keys[first] and header_keys[repeat], with no raw key text.
    Other failures retain NPY_HEADER_<WHAT>_A79_4:npz_members[i]."""
    tag = 'npz_members[%d]' % i
    try:
        with z.open(info) as f:
            head = f.read(8)
            if len(head) < 8 or head[:6] != NPY_MAGIC:
                return 'NPY_MEMBER_WITHOUT_NPY_MAGIC_A79_4:%s' % tag
            if head[6] not in NPY_VERSIONS or head[7] != 0:
                return 'NPY_HEADER_VERSION_NOT_KNOWN_A79_4:%s' % tag
            nlen, enc = NPY_VERSIONS[head[6]]
            lb = f.read(nlen)
            hl = int.from_bytes(lb, 'little') if len(lb) == nlen else -1
            hdr = f.read(hl) if hl >= 0 else b''
            if hl < 0 or len(hdr) != hl:
                return 'NPY_HEADER_TRUNCATED_A79_4:%s' % tag
        tree = ast.parse(hdr.decode(enc).strip(), mode='eval')
    except (UnicodeDecodeError, SyntaxError, ValueError):
        return 'NPY_HEADER_NOT_A_DICT_LITERAL_A79_4:%s' % tag
    if not isinstance(tree.body, ast.Dict) or not all(isinstance(k, ast.Constant) and isinstance(k.value, str) for k in tree.body.keys):
        return 'NPY_HEADER_NOT_A_DICT_LITERAL_A79_4:%s' % tag
    ks = [k.value for k in tree.body.keys]
    first = {}
    for j, key in enumerate(ks):
        if key in first:
            return 'NPY_HEADER_DUPLICATE_KEY_A71:%s:header_keys[%d]:header_keys[%d]' % (tag, first[key], j)
        first[key] = j
    if sorted(ks) != sorted(NPY_HEADER_KEYS):
        return 'NPY_HEADER_KEYS_NOT_THE_NPY_SET_A79_4:%s' % tag
    try:
        ast.literal_eval(tree.body)
    except (ValueError, SyntaxError, TypeError):
        return 'NPY_HEADER_NOT_A_DICT_LITERAL_A79_4:%s' % tag
    return None


def npz_duplicate_member_code(pk):
    """R10 [A71] (the c2v005 NPZ class) the field packet's ZIP directory checked before the pinned V005 packet_checks loads it with
    numpy.  R11 [A79.4]: the packet BYTES are read once (and must hash to the recorded sha when the record gives one), and from those
    bytes, before NumPy loads anything: the member-name checks (npz_member_index_codes: raw names, NumPy logical names, extensionless
    members refused outright) and the strict header audit of EVERY member (npy_header_audit_code).  Returns None (absent, or clean),
    or the first code (V4 / V5 False: the case is invalid).  An unreadable archive is NPZ_UNREADABLE_A79_4 (r10: left to packet_checks)."""
    p = (pk or {}).get('path') if isinstance(pk, dict) else None
    if not isinstance(p, str) or not Path(p).is_file():
        return None
    try:
        raw = Path(p).read_bytes()
    except OSError:
        return 'NPZ_UNREADABLE_A79_4'
    want = pk.get('sha256')
    if want is not None and sha256_bytes(raw) != want:
        return 'NPZ_BYTES_NOT_THE_RECORDED_SHA_A79_4'
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            infos = z.infolist()
            names = [x.filename for x in infos]
            codes = npz_member_index_codes(names)
            if codes:
                return codes[0]
            for i, info in enumerate(infos):
                c = npy_header_audit_code(z, info, i)
                if c:
                    return c
    except (OSError, zipfile.BadZipFile, ValueError, RuntimeError, EOFError, NotImplementedError):
        return 'NPZ_UNREADABLE_A79_4'
    return None


def npy_header_duplicate_key_code(p, names):
    """Kept for readers of r10: the strict header audit (npy_header_audit_code) of every member of the archive at p."""
    try:
        with zipfile.ZipFile(p) as z:
            for i, info in enumerate(z.infolist()):
                c = npy_header_audit_code(z, info, i)
                if c:
                    return c
    except (OSError, zipfile.BadZipFile, ValueError):
        return 'NPZ_UNREADABLE_A79_4'
    return None


def compute_packets(ctx, todo):
    packets = {}
    for key, run in todo:
        base = key.split('@')[0]
        if not run.get('present') or run.get('unreadable') or (run.get('adapted') or {}).get('status') != 'COMPLETED':
            continue
        case = {'shape': EXPECTED_TRUNCATION[base]['shape'], 'kmax_inverse_kpc': EXPECTED_TRUNCATION[base]['kmax_inverse_kpc']}
        code = npz_duplicate_member_code((run['adapted'] or {}).get('field_packet'))                   # R10 [A71]
        if code:
            packets[key] = {'V4': False, 'V5': False, 'reason': code}
            continue
        try:
            packets[key], _ = ctx['C5M'].packet_checks(run['adapted'], case, ctx['grids'][EXPECTED_GRID[base]], None, False)
        except Exception as exc:
            packets[key] = {'V4': False, 'V5': False, 'reason': '%s' % type(exc).__name__}
    return packets


def read_all(ctx, manifest, labels=None, with_packets=True, sha_only_cases=False):
    """sha_only_cases (--gates-only, verify blinding B2): cases and R-PAIR members are read by the sha256 of their bytes only."""
    cb = ctx['case_block']['cases']
    rd = (lambda lab, d, ro1: read_run_sha_only(lab, d)) if sha_only_cases else (lambda lab, d, ro1: read_run(lab, d, ctx, ro1))
    R = {lab: rd(lab, (manifest.get('cases') or {}).get(lab), cb[lab].get('ro1_required')) for lab in (labels or REGISTERED)}
    IDR = {} if labels else {n: read_run(n, (manifest.get('identity_runs') or {}).get(n), ctx, True) for n in IDENTITY_RUNS}
    RP = {}
    if not labels:
        for pid, rp in (manifest.get('rpair') or {}).items():
            RP[pid] = {'branch': rp['branch'], '_runs': {mem: rd('%s@RPAIR:%s' % (mem, pid), d, cb[mem].get('ro1_required'))
                                                         for mem, d in rp['members'].items()}}
    packets = {}
    if with_packets and not sha_only_cases:
        packets = compute_packets(ctx, list(R.items()) + [('%s@RPAIR:%s' % (m, pid), run) for pid, rp in RP.items()
                                                          for m, run in rp['_runs'].items()])
    return R, IDR, RP, packets


def runs_sha_map(R, IDR, RP=None):
    """{label: result sha}.  R10 [A71] built by unique_map over the case labels, identity-run names and R-PAIR keys (disjoint by
    construction: REGISTERED, IDENTITY_RUNS and '<label>@RPAIR:<pair>'; a collision raises rather than keeping the last)."""
    pairs = [(lab, run.get('result_sha256')) for lab, run in list(R.items()) + list(IDR.items()) if run.get('present')]
    for pid, rp in (RP or {}).items():
        for mem, run in rp['_runs'].items():
            if run.get('present'):
                pairs.append(('%s@RPAIR:%s' % (mem, pid), run.get('result_sha256')))
    return unique_map(pairs, 'RUNS', 'labels')


def cross_gate_checks(gates, R, RP=None, skip_mt=False):
    """Cross-record consistency (RECORD_DEFECT on mismatch): RB_FP eps_max = EPS eps_max; MT flags = run tail records (incl.
    R-PAIR members, verify D5).  skip_mt: --gates-only reads no tail record (sha-only cases), the MT cross-check is not run."""
    rb, ep = gates.get('RB_FP') or {}, gates.get('EPS') or {}
    if rb.get('status') in ('PASS', 'FAIL') and ep.get('status') in ('PASS', 'FAIL') \
            and rb['derived'].get('eps_max') != ep['derived'].get('eps_max'):
        rb.update(status='RECORD_DEFECT', codes=rb['codes'] + ['CROSSREF_MISMATCH:RB_FP:eps_max'])
    mt = gates.get('MT') or {}
    runs = unique_map(list(R.items()) + [('%s@RPAIR:%s' % (mem, pid), run) for pid, rp in (RP or {}).items()   # R10 [A71]
                                          for mem, run in rp['_runs'].items()], 'RUNS', 'labels')
    if mt.get('status') in ('PASS', 'FAIL'):                                                         # [A50 S2] FAIL is read too
        if skip_mt:

            mt['crosscheck'] = 'MT_FLAG_CROSSCHECK_NOT_RUN_GATES_ONLY'
        else:
            for lab, fl in mt['derived'].get('mt_flags', {}).items():
                run = runs.get(lab) or {}
                rec = run.get('uvt_record') or {}
                if run.get('present') and sorted(rec.get('flags') or []) != sorted(fl):
                    mt.update(status='RECORD_DEFECT', codes=mt['codes'] + ['CROSSREF_MISMATCH:MT:per_case/%s/flags' % lab])
    return gates


def read_gates(ctx, manifest, R, IDR, names=None, RP=None, skip_mt=False):
    runs_sha = runs_sha_map(R, IDR, RP)
    gates = {g: evaluate_gate(g, (manifest.get('gates') or {}).get(g), ctx, runs_sha) for g in (names or ALL_GATES)}
    return cross_gate_checks(gates, R, RP, skip_mt)


def write_json_new(path, obj):
    """[verify D6] sanitize non-finite values to null (named), serialize fully, then create the file (mode x)."""
    acc = []
    clean = finite_or_null(obj, '$', acc)
    if isinstance(clean, dict) and acc:
        clean['nonfinite_values_nulled'] = acc
    txt = json.dumps(clean, indent=1, allow_nan=False) + '\n'
    with open(path, 'x') as f:
        f.write(txt)
    return clean


# R11 [A79.2] (Codex2 0453 / BR-S1; r10 recheck order B3, validity B1; helper I P5 X02): the command-line parser never prints argv
# text.  Its error() raises a typed refusal whose text is a fixed category code; abbreviations are off (allow_abbrev=False); a
# repeated option is refused before parsing, naming both argv positions; help / usage is never printed in a blinded mode.
CLI_ERROR_CATEGORIES = (('unrecognized arguments', 'CLI_UNRECOGNIZED_ARGUMENT_A79_2'), ('invalid choice', 'CLI_INVALID_CHOICE_A79_2'),
                        ('expected one argument', 'CLI_EXPECTED_ONE_ARGUMENT_A79_2'),
                        ('ignored explicit argument', 'CLI_IGNORED_EXPLICIT_ARGUMENT_A79_2'),
                        ('ambiguous option', 'CLI_AMBIGUOUS_OPTION_A79_2'),
                        ('the following arguments are required', 'CLI_REQUIRED_ARGUMENT_MISSING_A79_2'),
                        ('not allowed with argument', 'CLI_MUTUALLY_EXCLUSIVE_A79_2'), (' value: ', 'CLI_INVALID_VALUE_A79_2'),
                        ('expected ', 'CLI_ARGUMENT_COUNT_A79_2'))
CLI_PARSE_ERROR_OTHER = 'CLI_PARSE_ERROR_A79_2'
BLINDED_FLAGS = ('--validity-only', '--gates-only')


def cli_error_code(message):
    """R11 [A79.2] the fixed category code of an argparse error message (the message itself is never printed)."""
    m = str(message)
    return next((c for k, c in CLI_ERROR_CATEGORIES if k in m), CLI_PARSE_ERROR_OTHER)


class CodedArgumentParser(argparse.ArgumentParser):
    """R11 [A79.2] an ArgumentParser whose error() raises Refused with a fixed code only (argparse's own error() prints the usage and
    argv-derived text to stderr before SystemExit, which r10's blinded handler never saw); exit() never prints its message; in a
    blinded mode a help or usage print is itself refused."""

    def __init__(self, *a, blinded=False, **k):
        k['allow_abbrev'] = False
        super().__init__(*a, **k)
        self._blinded = bool(blinded)

    def error(self, message):
        code = cli_error_code(message)
        raise Refused('REFUSED: %s (command-line parse error; argv text withheld, A79.2)' % code, code)

    def exit(self, status=0, message=None):
        if status:
            raise Refused('REFUSED: CLI_EXIT_A79_2 (argv text withheld, A79.2)', 'CLI_EXIT_A79_2')
        raise SystemExit(0)

    def _print_message(self, message, file=None):
        if self._blinded:
            raise Refused('REFUSED: CLI_HELP_OR_USAGE_NOT_PRINTED_IN_BLINDED_MODE_A79_2', 'CLI_HELP_OR_USAGE_NOT_PRINTED_IN_BLINDED_MODE_A79_2')
        super()._print_message(message, file)


def argv_is_blinded(argv_):
    """R11 [A79.2] a blinded mode is named by --validity-only / --gates-only, also in the '--flag=value' form (which argparse refuses
    for a store_true option: the refusal is then printed as a blinded code too)."""
    return any(isinstance(x, str) and x.split('=', 1)[0] in BLINDED_FLAGS for x in argv_)


def repeated_flag_naming(argv_):
    """R10 [A71] argparse keeps the LAST of a repeated option: refused (each option once; --case is checked per label).  R11 [A79.6]
    both argv positions named: DUPLICATE_ENTRY_A71:CLI:argv[i]:argv[j] (indices only).  None when no option repeats."""
    keys = [(x.split('=', 1)[0] if isinstance(x, str) and x.startswith('--') and x.split('=', 1)[0] != '--case' else ('VALUE', j))
            for j, x in enumerate(argv_)]
    d = unique_keys_codes(keys, 'CLI', 'argv')
    return d[0] if d else None


def main(argv=None):
    """R6: the audit-hook guard armed in test-mode full mode is always disarmed on return (r5 recheck validity F1).
    R10 [Codex2 0442 S1]: in a blinded mode (--validity-only / --gates-only) no exception text ever reaches stderr: a refusal prints
    its fixed code only, and any other exception prints REFUSED: INTERNAL_EXCEPTION:<type name> with rc 2 (the full mode and the
    field-contract mode keep their r8 behaviour).  R11 [A79.2]: a command-line parse error is a coded refusal in every mode."""
    argv_ = sys.argv[1:] if argv is None else list(argv)
    blinded = argv_is_blinded(argv_)
    try:
        return _main(argv)
    except Refused as exc:
        print(refusal_text(exc, blinded), file=sys.stderr)
        return 2
    except Exception as exc:
        if not blinded:
            raise
        print('REFUSED: INTERNAL_EXCEPTION:%s (blinded mode: detail withheld, A54 S6 / A47 I3)' % type(exc).__name__, file=sys.stderr)
        return 2
    finally:
        interlock_guard(False)


def _main(argv=None):
    argv_ = sys.argv[1:] if argv is None else list(argv)          # R10 [A71] argparse keeps the LAST of a repeated flag: refused
    ap = CodedArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
                             blinded=argv_is_blinded(argv_))                                   # R11 [A79.2]
    rep_ = repeated_flag_naming(argv_)
    if rep_:                                                                 # R11 [A79.6] both argv positions named
        raise Refused('REFUSED: REPEATED_CLI_FLAG_A71 (a repeated option would be read last-wins; each option once)',
                      'REPEATED_CLI_FLAG_A71', rep_)
    ap.add_argument('--prereg')
    ap.add_argument('--manifest')
    ap.add_argument('--case-block')
    ap.add_argument('--outdir')
    ap.add_argument('--route-a-mode', choices=sorted(ROUTE_A_MODES))
    ap.add_argument('--validity-only', action='store_true')
    ap.add_argument('--gates-only', action='store_true')
    ap.add_argument('--case', action='append')
    ap.add_argument('--no-packets', action='store_true', help='skip V4/V5 packet reads (they then read False)')
    ap.add_argument('--test-allow-unpinned-prereg', action='store_true')
    ap.add_argument('--test-producer-registry', help='test mode only: a producer registry file (A62.2); sealed mode reads the pinned one')
    ap.add_argument('--test-driver-build-record', help='test mode only (R10, A72): a driver BUILD record (r5 / r6); sealed mode reads the pinned one')
    ap.add_argument('--write-field-contract')
    a = ap.parse_args(argv_)
    blinded = bool(a.validity_only or a.gates_only)                                                # R10 [Codex2 0442 S1]
    if a.case and not a.validity_only:                  # R11 (r10 recheck validity B1 note) --case is a --validity-only option only
        raise Refused('REFUSED: CLI_CASE_ONLY_IN_VALIDITY_ONLY_A79_2 (--case is read by --validity-only only)', 'CLI_CASE_ONLY_IN_VALIDITY_ONLY_A79_2')
    if a.write_field_contract:
        try:
            write_field_contract(a.write_field_contract)
        except Refused as exc:
            print(str(exc), file=sys.stderr)
            return 2
        return 0
    if not (a.prereg and a.manifest and a.outdir):
        print('REFUSED: --prereg, --manifest and --outdir are required', file=sys.stderr)
        return 2
    if a.validity_only and a.gates_only:
        print('REFUSED: --validity-only and --gates-only are exclusive', file=sys.stderr)
        return 2
    out = Path(a.outdir)
    if out.exists():
        print('REFUSED: outdir exists', file=sys.stderr)
        return 2
    try:
        try:
            psha = sha256_file(a.prereg)
        except OSError as exc:
            raise Refused('REFUSED: prereg unreadable (%s)' % type(exc).__name__, 'PREREG_UNREADABLE')
        test_mode = psha != V007_PREREG_SHA256
        if test_mode and not a.test_allow_unpinned_prereg:
            raise Refused('REFUSED: prereg sha %s is not the pinned V007 prereg (%s)' % (psha, V007_PREREG_SHA256 or 'PENDING_FROM_BYTES'),
                          'PREREG_NOT_THE_PINNED_V007_PREREG')
        if not test_mode and PIN_ADDENDUM_V005 is None:                                                # [A48] freeze before pin
            raise Refused('REFUSED: sealed mode needs the frozen V005 addendum (A47, A48) pinned (PIN_ADDENDUM_V005)', 'SEALED_PIN_ADDENDUM_V005_PENDING')
        if not test_mode and PRODUCTION_K_BIG_A55 is None:                                             # [A54] A55 sets P
            raise Refused('REFUSED: sealed mode needs the A55 production K_big (PRODUCTION_K_BIG_A55, PENDING_A55)', 'SEALED_PRODUCTION_K_BIG_PENDING')
        if not test_mode and PIN_V010_R5_CHECK is None and PIN_DRIVER_BUILD_RECORD is None:            # R7 [A62.3]; R10 [A72]
            raise Refused('REFUSED: sealed mode needs the record of the v010 r5 check (A62.3: the r5 custody pins are verified from '
                          'bytes when the r5 check lands; PIN_V010_R5_CHECK pending), or, by A72, the registered driver BUILD '
                          'record with its check record', 'SEALED_PIN_V010_R5_CHECK_PENDING')
        if not test_mode and PIN_PRODUCER_REGISTRY is None:                                            # R7 [A62.2]
            raise Refused('REFUSED: sealed mode needs the root-registered producer registry (A62.2; PIN_PRODUCER_REGISTRY pending)',
                          'SEALED_PIN_PRODUCER_REGISTRY_PENDING')
        if not test_mode and (a.test_producer_registry or a.test_driver_build_record):
            raise Refused('REFUSED: --test-producer-registry / --test-driver-build-record are test-mode options (sealed mode reads the pins)',
                          'TEST_OPTION_IN_SEALED_MODE')
        if not test_mode and PIN_DRIVER_BUILD_RECORD is None:                                          # R10 [A72]
            raise Refused('REFUSED: sealed mode needs the registered driver BUILD record (A72: r5 or r6; PIN_DRIVER_BUILD_RECORD pending)',
                          'SEALED_PIN_DRIVER_BUILD_RECORD_PENDING_A72')
        # R10 [A72] the sealed-driver pin set is activated FIRST (validate_case_block reads the sealed driver)
        if test_mode:
            bobj = load_driver_build_record(a.test_driver_build_record)[0] if a.test_driver_build_record else None
        else:
            bobj = load_driver_build_record(PIN_DRIVER_BUILD_RECORD[0], PIN_DRIVER_BUILD_RECORD[1])[0]
        bld = activate_driver_build(bobj)
        if not test_mode and bld.get('check_record') is None:                                          # R7 [A62.3]; R10 [A72]
            raise Refused('REFUSED: sealed mode needs the record of the independent check of the sealed driver build (A62.3 / A72; '
                          'check_record pending)', 'SEALED_DRIVER_BUILD_CHECK_RECORD_PENDING')
        if not test_mode and bld['build'] == 'r5' and PIN_V010_R5_CHECK is None:                       # R7 [A62.3]
            raise Refused('REFUSED: sealed mode needs the record of the v010 r5 check (A62.3: the r5 custody pins are verified from '
                          'bytes when the r5 check lands; PIN_V010_R5_CHECK pending)', 'SEALED_PIN_V010_R5_CHECK_PENDING')
        pre = load_strict_file(a.prereg, 'prereg')
        cbp = (pre.get('binding_inputs') or {}).get('case_block') if isinstance(pre, dict) else None
        if isinstance(cbp, dict):
            if a.case_block and str(Path(a.case_block).resolve()) != str(Path(cbp['path']).resolve()):
                raise Refused('REFUSED: --case-block differs from the prereg case block', 'CASE_BLOCK_DIFFERS_FROM_THE_PREREG')
            cb_path, cb_sha = cbp['path'], cbp['sha256']
        elif a.case_block and test_mode:
            cb_path, cb_sha = a.case_block, None
        else:
            raise Refused('REFUSED: no case block (prereg binding_inputs.case_block, or --case-block in test mode)', 'CASE_BLOCK_ABSENT')
        try:
            cb_raw = Path(cb_path).read_bytes()
        except OSError as exc:
            raise Refused('REFUSED: case block unreadable (%s)' % type(exc).__name__, 'CASE_BLOCK_UNREADABLE')
        if cb_sha is not None and sha256_bytes(cb_raw) != cb_sha:
            raise Refused('REFUSED: case block sha mismatch', 'CASE_BLOCK_SHA_MISMATCH')
        cb = load_strict_file(cb_path, 'case block')
        mode_sources = [x for x in (pre.get('route_a_mode'), (cb or {}).get('route_a_mode') if isinstance(cb, dict) else None,
                                    a.route_a_mode) if x is not None]
        if len(set(map(str, mode_sources))) > 1:
            raise Refused('REFUSED: route-A mode differs between prereg/case block/CLI: %s' % mode_sources, 'ROUTE_A_MODE_SOURCES_DIFFER')
        mode = mode_sources[0] if mode_sources else ROUTE_A_MODE_DEFAULT                               # [A47 I4]
        why = validate_case_block(cb, route_a_mode=mode)                                               # [A50 S1] mode-aware
        if why:
            raise Refused('REFUSED: case block: %s' % why, 'CASE_BLOCK_INVALID')
        if test_mode:                                                                                    # R7 [A62.2]
            reg = load_producer_registry(a.test_producer_registry) if a.test_producer_registry else None
        else:
            reg = load_producer_registry(PIN_PRODUCER_REGISTRY[0], PIN_PRODUCER_REGISTRY[1])
        ctx = build_context(mode, cb, reg)
        manifest = load_manifest(a.manifest)
        if test_mode and not (a.validity_only or a.gates_only):                                         # [verify blinding B4]
            ic = registered_identity_code()                     # R11 [A79.3] an unavailable registered identity refuses, never empty
            if ic:
                raise Refused('REFUSED: %s (test mode, pre-seal, full mode: a registered C5H run directory cannot be stat\'ed, so its '
                              'identity is unknown; nothing is read, A79.3)' % ic, ic)
            why = None                                                    # [R3 validity F2] every run path of the manifest
            for slot, d in manifest_run_paths(manifest):
                w = c5h_interlock(d)
                if w:
                    why = '%s (manifest slot %s)' % (w, slot)
                    break
            if why:
                raise Refused('REFUSED: test mode (pre-seal) full mode on the registered C5H call: %s; only --validity-only and '
                              '--gates-only may read it before the seal (A47 I3)' % why, 'C5H_INTERLOCK_FULL_MODE_PRE_SEAL')
            ctx['interlock_side_paths'] = True                                     # [A53 F2] record side paths too (read_run)
            interlock_guard(True)                                          # R6 [validity F1] audit-hook guard on every open
    except Refused as exc:
        print(refusal_text(exc, blinded), file=sys.stderr)                                             # R10 [Codex2 0442 S1]
        return 2
    head = {'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'test_mode': bool(test_mode),
            'prereg': {'path': str(Path(a.prereg).resolve()), 'sha256': psha},
            'case_block': {'path': str(Path(cb_path).resolve()), 'sha256': sha256_bytes(cb_raw)},
            'manifest': {'path': str(Path(a.manifest).resolve()), 'sha256': sha256_file(a.manifest)},
            'script_sha256': sha256_file(__file__), 'route_a_mode': mode,
            'pins_verified': {'V004_addendum': PIN_ADDENDUM_V004[1], 'V005_prereg': PIN_PREREG_V005[1], 'V005_compare': PIN_COMPARE_V005[1],
                              'V006R1_prereg': PIN_PREREG_V006R1[1], 'draft_R1': PIN_DRAFT_R1[1], 'C5H_spec': PIN_C5H_SPEC[1],
                              'REVIEW_V009': PIN_REVIEW_V009[1], 'C5H_dryrun': PIN_C5H_DRYRUN[1], 'C5_spec_reviewed': PIN_C5R3_SPEC_REVIEWED[1],
                              'row_radii_binding': PIN_ROW_RADII_BINDING[1], 'uv_tail_library': PIN_UVT_LIB[1],
                              'V005_addendum': PIN_ADDENDUM_V005, 'driver_v010_r5': PIN_DRIVER_V010_R5[1],
                              'r5_cascade_map': PIN_R5_CASCADE_MAP[1], 'RO1_custody': {k: v[1] for k, v in PIN_RO1_CUSTODY.items()},
                              'RO1_nodes_custody': {k: v[1] for k, v in PIN_RO1_NODES_CUSTODY.items()},
                              'v010_r5_check': PIN_V010_R5_CHECK,
                              'driver_build_record': PIN_DRIVER_BUILD_RECORD and PIN_DRIVER_BUILD_RECORD[1],      # R10 [A72]
                              'sealed_driver_build': {'build': bld['build'], 'driver': bld['driver']['sha256'],
                                                      'RO1_custody': {k: v['sha256'] for k, v in bld['ro1_custody'].items()},
                                                      'RO1_nodes_custody': {k: v['sha256'] for k, v in bld['ro1_nodes_custody'].items()}}},
            'producer_registry': {'source': None if ctx.get('producer_registry') is None else ('test' if test_mode else 'pinned'),
                                  'sha256': (ctx.get('producer_registry') or {}).get('sha256')},
            'cited_not_pinned': {'path': ADDENDUM_V005_CITED + ' (A47, A48; open until frozen)',
                                 'sha256_at_run': sha256_file(ADDENDUM_V005_CITED) if Path(ADDENDUM_V005_CITED).is_file() else None}}
    if a.validity_only:                                                                                 # [A47 I3]
        labels = a.case or []
        if len(set(labels)) != len(labels):                                     # R10 [A71 B12] a --case label given twice
            dn = unique_keys_codes(labels, 'CLI', 'case')                       # R11 [A79.6] both --case entries named (by index)
            print('REFUSED: REPEATED_CASE_LABEL_A71 [%s]' % naming_text(dn[0]), file=sys.stderr)
            return 2
        if not labels or any(x not in REGISTERED for x in labels):
            print('REFUSED: --validity-only needs --case with registered labels', file=sys.stderr)
            return 2
        R, _, _, packets = read_all(ctx, manifest, sorted(set(labels)), with_packets=not a.no_packets)
        gates = read_gates(ctx, manifest, R, {}, names=['I1T', 'B0'])
        gi = gates['I1T']
        i1t = {'status': gi['status'], 'per': gi.get('derived', {}).get('i1t_per_case') if gi['status'] in ('PASS', 'FAIL') else None}
        extra = b0_extra(gates['B0'])
        if C5H in R:
            c5r = R[C5H]
            c5h_num = ((_normalized(c5r) or c5r.get('spec_for_reading') or {}).get('numerics')
                       if c5r.get('present') and not c5r.get('unreadable') else None)
        elif 'C4T-D5' in labels:                                                                        # [verify blinding B3]
            c5h_num = read_numerics_only((manifest.get('cases') or {}).get(C5H))
        else:
            c5h_num = None
        body = {'schema': SCHEMA_REPORT + '_VALIDITY_ONLY', 'blinded': True,
                'statement': 'validity/admissibility booleans and reason codes only; no row value, speed or other number is written or printed (A47 I3)',
                **{k: head[k] for k in ('test_mode', 'route_a_mode', 'script_sha256')},
                'cases': {lab: blinded_case(case_validity(lab, R[lab], ctx, packets.get(lab), i1t, c5h_num, None, extra)) for lab in labels},
                'I1T_gate': blinded_gate(gates['I1T']), 'B0_gate': blinded_gate(gates['B0'])}
        assert_no_numbers(body)
        out.mkdir(parents=True)
        write_json_new(out / 'VALIDITY_ONLY.json', body)
        print(json.dumps(body, indent=1))
        return 0
    if a.gates_only:                                                                                    # [RA13] blinded
        R, IDR, RP, _ = read_all(ctx, manifest, with_packets=False, sha_only_cases=True)               # [verify blinding B2]
        gates = read_gates(ctx, manifest, R, IDR, RP=RP, skip_mt=True)
        hit = []
        idv = {n: identity_run_validity(n, IDR[n], ctx) for n in IDENTITY_RUNS}
        body = {'schema': SCHEMA_REPORT + '_GATES_ONLY', 'blinded': True,
                'statement': 'gate statuses and reason codes only; case results read by sha256 of their bytes only; no row value '
                             'or record number is written or printed',
                **{k: head[k] for k in ('test_mode', 'route_a_mode', 'script_sha256')},
                'gates': {g: blinded_gate(x) for g, x in gates.items()},
                'mt_crosscheck': (gates.get('MT') or {}).get('crosscheck', 'NOT_APPLICABLE'),
                'identity_runs': blind_strings({n: {'valid': bool(idv[n]['valid']) and not idv[n]['ro1_codes'],      # [R3 validity F3]
                                                    'codes': list(idv[n]['codes']) + list(idv[n]['ro1_codes'])} for n in IDENTITY_RUNS}, hit)}
        body['blinding_redaction_applied'] = bool(hit)
        assert_no_numbers(body)
        out.mkdir(parents=True)
        write_json_new(out / 'GATES_ONLY.json', body)
        print(json.dumps(body, indent=1))
        return 0
    R, IDR, RP, packets = read_all(ctx, manifest, with_packets=not a.no_packets)
    gates = read_gates(ctx, manifest, R, IDR, RP=RP)
    c4r3 = Path(PIN_R3['C4R3'][0])
    ok4 = sha256_file(c4r3) == PIN_R3['C4R3'][1]
    if ok4:                                         # R10 [A71 / T05] the pinned C4R3's adapter side files are parsed strictly first
        try:
            ok4 = not adapter_side_file_codes(_read_json(c4r3)[0])
        except (OSError, ValueError):
            ok4 = False
    ctx['c4r3_adapted'] = ctx['C5M'].adapt_result(c4r3) if ok4 else None
    if _GUARD['active'] and _GUARD['refused']:                       # R6 [validity F1] an open into the registered run was refused
        print('REFUSED: test mode (pre-seal) full mode: %d open(s) into the registered C5H run were refused by the interlock guard; '
              'no report is written (A47 I3)' % _GUARD['refused'], file=sys.stderr)
        return 2
    try:
        ev = evaluate_v007(ctx, R, IDR, gates, RP, packets)
    except Refused as exc:                                                       # [A53 NEW-17] refused at load: no report
        print(str(exc), file=sys.stderr)
        return 2
    for v in list(ev['validity'].values()) + list(ev['rpair_validity'].values()):
        v.pop('_uvt_info', None)
    report = {'schema': SCHEMA_REPORT, **head,
              'inputs': {lab: {'dir': run.get('dir'), 'result_sha256': run.get('result_sha256'),
                               'last_change_km_s': (run.get('adapted') or {}).get('last_change_km_s')} for lab, run in R.items()},
              **ev}
    out.mkdir(parents=True)
    clean = write_json_new(out / 'KMAX_TAIL_COMPARISON.json', report)
    txt = (table_text(ev, ctx) if ev['decision']['tests_read'] else '(T-tests not read: %s)\n' % ev['decision']['outcome'])
    txt += '\nDECISION: %s\n' % json.dumps(clean['decision'], indent=1, allow_nan=False)
    with open(out / 'KMAX_TAIL_COMPARISON_TABLE.txt', 'x') as f:
        f.write(txt)
    print(txt)
    return 0


if __name__ == '__main__':
    sys.exit(main())
