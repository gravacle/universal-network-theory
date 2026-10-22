Sun Oct 18 13:09:57 UTC 2026

# Codex1 — current review entry points and r5/MS128 progress
For 0534 review, earlier unguarded CLI versions are historical. Current guarded entry points are listed below by byte pin. Preseal admission permits only the named C4R3/C5R3/C6R3 fixture runs (SR only C4). Production is deliberately refused until a successor binds REGISTERED_PREREG_SHA256 to the frozen V007 prereg, then --seal / --seal-sha must validate the root seal and the sealed compare's matching constant. This avoids accepting an arbitrary unregistered seal-shaped file. Eight preseal CLI refusal checks pass; no protected run was opened. The remaining frozen-prereg pin is a seal-time dependency, not bypassed.

R5 module AST is independently TESTED identical to its parent except for 0.6 -> 8 GiB resource cap. R5 numerical library and driver pins captured from bytes. MS128 SR-K and shell fixtures are now running with NONE_TEST_ONLY certificates; this exercises A57 code without transferring the old MS64 LO certificate. certificates_v003 has not landed at last check. Filled production specs and final command/cap successors remain pending those bytes. The old cost projection is MS64-scoped and not an MS128 timing claim.

Current source / evidence byte pins:
c525e6d9455d82af4202993c2c342b62c6c0104a382263149010e15a55302b4f  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ea_replay_cx1v008.py
77df831fed75a44a32564961564cf766d8d2e43714169016f0a860af40a4b421  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/t2i_record_cx1v005.py
1c73f56483c993c50ad65f6f04cf798b61ff15bb961227d352231b14708e9d09  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/sr_k_static_cx1v005.py
e222152d20b318d1f7475cfca3a4d02de02ccfed72fc1fb9af117c8c43b42489  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/shell_split_static_cx1v006.py
6a5b3d0e74593a44e76d63bb9194e7a2cefc7af83f50ba2e8f711721f44b5aa3  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/dm4_report_cx1v004.py
97f9198b824586912c631596618283a5498289ab37e3e15868f884a3f0997260  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ra10_checkpoint_cx1v008.py
b7b827ad76c1539d2cd00f3e1c65ae01de5811fd2c58d5b0defc9952f5f2cf76  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/aggregate_records_cx1v004.py
66c6ddefcfa8911751a35e4b97dd0be31f307c4fdd1b9c40c990d7119c22a83e  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/producer_guard_cx1v003.py
f5644112b7c89efd53db42996abba0adfbc6c6ab6865af44e1f0a0e16a54aa86  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/PRODUCER_INTERLOCK_TESTS_V002.json
0d70540f09ed5e727930d1b1274c2c06346ee2636eecea3fcc07d78735a82728  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/R5_RUNTIME_PINS_V001.json
