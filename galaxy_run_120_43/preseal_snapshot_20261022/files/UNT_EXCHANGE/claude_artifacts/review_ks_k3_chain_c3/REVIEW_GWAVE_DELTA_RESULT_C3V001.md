# Claude3 direct lens (A175): G-wave delta on KS1-KS6 (A182). Verdict PASS, 0 blocking (A115)

Scope (0758): K=3 is reachable only through S1_UA_C3T, non-S1 behaviour is unchanged, and the section 7 S1 C1 and handoff deps agree with the code.

TESTED
- README b a3ec369f; HASHES_GWAVE_C2V001 4c74539d: 78/78 verify from bytes.
- All 15 G-wave diffs rebuild their successor bytes exactly from the pinned predecessors:
  - G3: c6ffb338, 2832ceb9, 3e668a2b;
  - G4: 4de70486;
  - G1: cd10cd59;
  - G6: 6d59f1d0, 7044e131, 4ca7f364;
  - G2: 08e9ac0a;
  - KS5'': 66560a6a;
  - KS3': 736d2e7e, 54595c2d;
  - KS4': 080ed171;
  - KS6': 8fa371a7, 6642d209.

FORMAL
- Each successor evaluates KS1's S1_UA_C3T gate first and hands every other spec to the unchanged predecessor object, loaded by path and sha. Read for G3 geometry and producer and for G2. In G3 the S1 path changes only the kept-region K (L39: 4 -> kept_k = 3).
- Section 7 pins agree with the code: G6c 4ea0c2ca (KS3' common PINS and KS6' adapter); producers G4 e00ab71d, G3 c3699c78 and G1 6af9ed6c (KS3' common); KS5 e394ae94 (common, KS5''); KS6' adapter c8dc59a1 and G6b 65834e9b (KS6' handoff); KS5'' 51a6fb27 (common).

NOT RE-RUN (relies on root's in-place runs)
- test_gwave_c2v001 hard-requires its run dir under ks_k3_chain_c2/synthetic/ (L330). Under my no-write rule I did not run it in root's folder.
- Root in-place results: GWAVE 43/43 (786e2b32); ports KS 62/62 (0fe61651), CP-1 295/295 (7ba56c8a), proof side 222/222 on R2 (5c5a7c39), S1K3 25/25 (a8b68c58).
- The first proof-side port run read 221/222, on H02_F11 only. Suites run in parallel in one folder broke the nothing-outside-synthetic snapshot (README section 8).

NOTES (none blocking)
- N1: The G2 SRB adapter (7eb456cd) for the S1 call is a root-supplied handoff dep. No code pins it per S1: the KS6' handoff checks only its LO adapter pin, as v004 did. Root must supply G2, not 08e9ac0a, for row 32 (section 7 HO). A per-S1 pin would make this fail closed.
- N2: The G-wave suite cannot be re-run outside root's folder. The relocation limit on canonical pins is the same as for KS1-KS6.
- N3: Section 7 RUN: real GQ, EPS and rho at row 32 are UNTESTED. The deciding test is the CP-1 row-32 run itself.
- Codex1's distinct-lineage G3 check (FROM_CODEX1/0158) reads PASS.
