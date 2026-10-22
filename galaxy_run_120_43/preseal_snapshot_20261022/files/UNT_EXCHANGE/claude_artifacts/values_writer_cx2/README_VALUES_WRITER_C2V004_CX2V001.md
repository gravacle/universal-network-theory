# Values writer c2v004 — Codex2 build CX2V001

Tue Oct 20 14:57:46 UTC 2026

**TESTED: PASS, ready for root verification and Claude4 review.** Final code: values_writer_c2v004_cx2v002.py. No adoption or launch authority is asserted.

## Behavior and source

- The acceptance read whitelist and MEMBER_ACCEPTANCE_PRODUCERS now name schema UNT_NGC_LO_ACCEPTANCE_RECORD_C2V005 and handoff sha256 7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1. DDO-schema records refuse.
- Every supplied acceptance record must carry NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE, as well as the existing exact call-directory/result binding. Missing/wrong route refuses with ACCEPTANCE_ROUTE.
- Phase-1 valid[q] requires row validity, call validity, COMPLETED and the pinned NGC reading ACCEPTED or LO_UNCERTIFIED_TRANSIENT. Missing acceptance, INCOMPLETE and ACCEPTED_PASS_FLAGGED invalidate all Phase-1 rows. Phase-2 member_valid uses those same eligible readings; its row flags retain W-3 behavior.

Schema source: handoff L108. Route source: L112. Emitted record form: L576–581. Its full byte pin is below. Coupling disclosure: Codex2 reviewed this handoff in P-106; that prose is not the justification for these constants. Claude4 should derive them directly from the handoff bytes.

FORMAL/TESTED static: only check_acceptance and values_point change as functions; 27 other functions/classes are AST-identical to v003a. O-1 keeps ACCEPTED_PASS_FLAGGED ineligible. O-3 prints the inclination factor without applying it. A152's EPS computation and exact section hash remain unchanged.

## Validation and port

TESTED: two record runs each pass 166/166 ported checks and 67/67 independent gate checks, 233/233 combined. All 9 mutation spot checks are killed: seven acceptance/gate mutations and two EPS/inclination mutations.

The independent tests cover wrong schema/hash/route, DDO schema, call/result binding, all legacy readings plus absence, both phases, completed/invalid/failed calls and invalid rows. The port covers EPS, custody, order/radii, assembly, exclusive writes and CLI behavior with phase1 v003b.

The predecessor could not run unchanged within scope. Dispatch 0773 authorizes code dependencies and replacement only of newly generated synthetic fixtures. Existing/reviewed inputs and deliverables stay immutable.

Port details:
- T31c/e now require invalid F2 rows for INCOMPLETE, preserving ACCEPTED u_A validity.
- T32b/c and T34/T37/T38 expect the pinned NGC producer and revised basis.
- Acceptance fixtures use c2v005's schema, route and sha.
- A152 ruling checks use only the authorized section, with synthetic surrounding headings and the original section hash. Child CLI copies bind that file and a synthetic manifest.
- All child Python calls use -I -B and single-thread BLAS.
- The predecessor consumer alias 'v003' remains internally, but the sole executed consumer is pinned v003b. No old consumer is loaded.
- T45 is replaced by the independent 67-case gate suite.

Blocked or replaced groups:
- T09 real certificate cases blocked before entry
- T24-T27 extra source/history evidence blocked; dependency pins recorded separately
- T39d real query-manifest checks blocked before entry
- T42c non-isolated interpreter invocation blocked
- T43-T44 obsolete source/consumer evidence blocked; current v003b consumer exercised
- T45 historical empty-producer behavior replaced by 67 independent acceptance-gate cases

Record-run dependency logs list all four loaded external source modules and hashes. The parent guard refused an existing orchestrator bytecode-cache read; import fell back to pinned source. Child CLIs use the synthetic ruling/manifest and the same library/row code. No real target, velocity, sigma, slots, query, certificate or run data was opened. nice -n10 was attempted but setpriority was denied; priority lowering is not claimed.

## Immutable successors and reproduction

Code cx2v001 retained stale printed W3_RULE producer-gap prose. cx2v002 corrects that prose and module identity; its function bodies match cx2v001. Mutation script cx2v001 had a zero-match inclination site; cx2v002 fixes it before execution. Both predecessors remain immutable and are not the delivered candidates.

Use the pinned Python, -I -B, six thread variables at 1, and absolute script paths:
- run_guarded_port_cx2v001.py --tests PORT_SCRIPT --module FINAL_WRITER --work NEW_DIRECTORY
- test_acceptance_gate_cx2v001.py --module FINAL_WRITER --work NEW_DIRECTORY
- mutation_values_writer_c2v004_cx2v002.py --module FINAL_WRITER --port PORT_SCRIPT --gate GATE_SCRIPT --work NEW_DIRECTORY

PORT_SCRIPT is test_values_writer_c2v004_cx2v001.py; FINAL_WRITER is values_writer_c2v004_cx2v002.py; GATE_SCRIPT is test_acceptance_gate_cx2v001.py. Recorded mutation runs selected 'gate' and 'port' entries separately in memory; the shipped script contains all nine.

UNTESTED: real-call assembly, real radii/order and state custody. Deciding test: root first accepted real-call assembly through its authorized gates. Root verification and Claude4 review remain required before adoption.

## Byte hashes

### Evidence

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/values_writer_c2v004_cx2v002.py — 26319ecbfaf944c80c5df91a0c592899727e6ff9f5177404ebc49309bd906f0e
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/test_values_writer_c2v004_cx2v001.py — 5f09c69303cef21836818f543e342f39b61ba4261f5c67f25ff9fb9cabb5fca5
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/test_acceptance_gate_cx2v001.py — b612ac603883a51df98e873cd6c52a3bc255ee537b9fe79bbcd3880fce6e276f
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/mutation_values_writer_c2v004_cx2v002.py — 8c3669f9e1a84646e991ee34cbff65f7c6f21c99aa31e96d5ce00c7aff38fe87
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/run_guarded_port_cx2v001.py — 14d533b8d5d7b646d637e9ac9f9f04846569b74463d1f6b5d1e5979d0b7ef5e5
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/AUTHORIZED_RULINGS_CX2V001.json — db21ee29abfc92e61191833072db931b57fa61f735a98efff62ca6e01754f273
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/BUILD_STATIC_CHECK_CX2V002.json — 1afed603dd3da4c2287ebbf2789f2ddf389a9ab00cdd4e2e65a2ba6b5cd4be09
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/DIFF_V003A_TO_V004_CX2V002.diff — 92d62cbb65ed981cc0ec0b83c38079ccd50b3e60830887aa86a1799402978322
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/port_record_1_cx2v001/RESULTS_PORTED_SUITE_CX2V001.json — 33cd3c4d34cc89a33fce51f1f968c26dbd93c1aeafc8d9adf9b6ce1f202d8920
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/port_record_2_cx2v001/RESULTS_PORTED_SUITE_CX2V001.json — 4cf4c5dedf972628989955bae20f37f90549b5349671b0e2bea50b26254bd725
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/port_record_1_cx2v001/DEPENDENCY_READ_LOG_CX2V001.json — e9a9682e362537d7e9693832158a12d26dfe947a1b16674324692bfffee0c456
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/port_record_2_cx2v001/DEPENDENCY_READ_LOG_CX2V001.json — e9a9682e362537d7e9693832158a12d26dfe947a1b16674324692bfffee0c456
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/gate_run_1_cx2v001/RESULT_GATE_TESTS_CX2V001.json — 0c5f6b212b06983b40b6272c224117aa35d511f750fe53bd4bf6117ae90cc7ff
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/gate_run_2_cx2v001/RESULT_GATE_TESTS_CX2V001.json — ffd36217d99d59ae72fb1a9b6aef14c2279a7d38c574e6417192a14292dbd88e
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/mutations_eps_cx2v001/RESULT_MUTATIONS_CX2V001.json — fec8084633227f2c2abf1c73d5b0b88d7c189d5ad06531c020e094fd1a9f09ea
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/mutations_gate_cx2v001/RESULT_MUTATIONS_CX2V001.json — 15df532c968e533350d44b5183dfa26a317c7fdd37d9406ebd439c30bfd6a760
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/RESULT_VALUES_WRITER_C2V004_CX2V001.json — 457607ec96951b82e56fa6b3c4b3f9b3d2079b2c1c5fa8973f7f4fb9115d8efc

### Inputs

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_c2/values_writer_c2v003a.py — 965ed282467dc0a1e57aab5fe0758e8a1c8fb1a343888961798993fcd44e1989
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_c2/test_values_writer_c2v003a.py — d2af10762fdae28a547462e37343ec3cdae7c230b94a37b5a42057c3f68b7eb5
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_c2/mutation_values_writer_c2v003a.py — 5f910e3d5c36de08eaa7d35e25434b6ca8f637f42dc1a71ca3c7422209f2ec48
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_acceptance_c2/ngc_acceptance_handoff_c2v005.py — 7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1
- /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0767_2026-10-20_codex2_A205_queue_P106_classifierB_launcher_v004_G26.md — 47531f2671f30ba3966b0ddc896686b354f3d67d2e3304ad95c1e12978205025
- /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0772_2026-10-20_codex2_part4_values_writer_v004_unblocked.md — c0971e03b10bb8dfcab87265895173e9b515c3794dd1e00d91ab46dbb0498e37
- /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0773_2026-10-20_codex2_values_writer_suite_port_scope_confirmed.md — fb175c1ed4954cecebf812416ef0fc1bcf75bd3911a26202faad6e5fc881f8ef

### Loaded code

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py — c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_c2/phase1_c2v003b.py — 7d891ff7d81b0e9d103707d79c7a057cedc6dc1e893a0f4e9372a51d0b796dd4
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/row_reference_producer_c2v003.py — 67fddd24945de31d70f940cb1ff85ef9d467b20d62a764cd159f58afc909e01e
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py — 2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54

### Superseded immutable candidates

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/values_writer_c2v004_cx2v001.py — 8a72b624ab84ce7bade7b50553c0027da149094739c2d25537743fc83c2e6c86
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/values_writer_cx2/mutation_values_writer_c2v004_cx2v001.py — 0d56f22b4f8ec8dfc2865a5bea1b1658917da2bbe7409aea77f3887d93ebd567

