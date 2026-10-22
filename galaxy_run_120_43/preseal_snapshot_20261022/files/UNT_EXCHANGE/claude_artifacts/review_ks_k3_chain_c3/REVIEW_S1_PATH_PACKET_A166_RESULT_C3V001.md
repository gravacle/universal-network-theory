# Claude3 direct lens: S1 launch path C2V002C + packet A166 set (A185, 0760). Verdict PASS, 0 blocking (A115)

Object: claude_artifacts/s1_successors_c2/:
- lib s1_path_lib_c2v002c 99e2be17; CLIs d4e31013 / 2b120b89 / 4716bb69; binder step4_bind_c2v011 d3d9702e; README 135a0426; HASHES_S1_PATH_C2V002C 7bba21e1.
- Packet A166: guard014 6efdca01, launcher015 cd987edd, lib v002b 65d69cf4, DBP C2V004B e239d21e.

TESTED
- HASHES_S1_PATH_C2V002C 19/19, HASHES_G14 24/24 and HASHES_A 17/17 verify from bytes. The third column is the byte size; I checked sha + path.
- Every shipped diff rebuilds its target exactly from the pinned predecessor:
  - lib f961839b -> 65d69cf4 -> 99e2be17;
  - fill 953e698d -> 2b120b89, read 4530dd25 -> 4716bb69, launch_root aa49ef4a -> d4e31013;
  - binder 4d07dca3 -> d3d9702e;
  - guard 593bebb6 -> 6efdca01;
  - launcher 5d6af4a7 -> cd987edd.

FORMAL (diff reading)
- A166 removed only the memory gating:
  - guard014 drops guard013's memory fields and refuses a rule that still carries them, keeping max_active, poll 60 and the ramp.
  - launcher015 has no memory_pressure read and no nice >= 10. The lock, max_active, ramp, single-thread BLAS, caffeinate and drain-on-failure are kept. This closes Claude4's 0229 note that the launcher ramp still memory-gated the S1 overlap.
  - lib v002b removes the machine gate, memory_pressure and the A133 rule.
  - binder c2v011 loads guard014 by path and sha, runs no nice, and refuses nice/renice in argv. The single-thread BLAS env is kept as a determinism guard.
  - Custody and fail-closed checks are the predecessors'.
- lib v002c: the wrapper is KS5'' 51a6fb27 (G7), the DBP is C2V004B, and S1_FENCE_SOURCES are KS5 e394ae94, KS1 ad020470 (+6810b7c3), KS2 99c29df6, G4 e00ab71d, G3 producer c3699c78, G1 6af9ed6c and G6c 4ea0c2ca. These equal the G-wave section 7 pins I checked (0254).

NOT RE-RUN (root's folder-bound suites)
- Root's runs: S1C 163/163 twice (44ccde14, 6556abd7) with the deciding test passing; G14 36/36 twice; S1B 143/143 twice.

NOTES (none blocking)
- N1: guard014 refuses a plan rule that still has guard013's memory fields (MEMORY_ADMISSION_FIELD_REFUSED). Root's plan of record must be rewritten without them (fail closed).
- N2: lib v002c's replay refuses fill records written by v002b (FILL_RECORD_STATIC_PINS_NOT_REPLAYED, disclosed). Any v002b fill must be refilled; the spec bytes are identical.
- N3: The S1 fence sources do not include the G2 SRB adapter, because the prelaunch does not open it. G2 stays a root-supplied handoff dep (0254 N1).
