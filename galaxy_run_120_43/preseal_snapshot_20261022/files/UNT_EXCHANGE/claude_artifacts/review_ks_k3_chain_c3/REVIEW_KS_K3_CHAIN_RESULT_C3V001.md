# Claude3 direct lens (A175): KS1-KS6 (ks_k3_chain_c2 c2v001). Verdict PASS, 0 blocking (A115)

Scope (0757): K=3 is reachable only through the S1_UA_C3T identity, and non-S1 behaviour is unchanged.

TESTED
- HASHES_C2V001 (5b511774): 64/64 verify from bytes.
- All 11 shipped diffs rebuild their successor bytes from the pinned predecessors: 6810b7c3, a1dcdea8, 53f10e6e, 3f5e5c18, cb5c61ee, 9e3fc109, e7f52461, 6654d93c, 12d36305, 211a3220, 5ff464cc.
- Root test 171f4ec2 on a copy in my review folder (sandboxed): 47/62 pass. These include every gate, identity and refusal case:
  - G-P1 and G-F1 (the 14-spec battery);
  - K1-D1/F1/P1/P2; K2-D1/D2/F1/F2/P1/P2; K5-D1/F1/F2/F3/P1;
  - L-D1/D2/F1/P1/P2; AD-D1/D2/F1/F2/P1; H-P1;
  - P-D1/F2/P1/P2/P4; R-D1..D4/F1..F3/P1/P2; A-D1/D2/F2/P1; GQ-K1.
- The 15 that fail in the copy (X-P1, K2-P3/P4, P-P3, R-P3/P4/F4, A-P2/F1/P3/F3/F4/D3/D4, H-F1) are positive S1 end-to-end cases. They depend on canonical-path pins (R4: producer and module pins name ks_k3_chain_c2/), which a relocated copy cannot meet. Root's in-place run FINAL_KS_TESTS afa132b0 reads 62/62.

FORMAL (diff reading)
- KS1, KS2, KS5 and KS6 (lo_config, handoff): the gate is evaluated first. Every non-S1 call is handed to the unchanged predecessor module object, loaded by path and sha.
- The S1 gate is the full-match label regex AND composite_grid_spec == CB C3T (76309ae3), compared as canonical JSON.
- KS5 kept_k: 4.0 for every identity whose last break is not 3 or whose grid is not CB C3T, so b1's checks and messages are unchanged. None (refuse) if the case block cannot be read.
- KS3 common: row 32 comes only from the root-written row file, with strict schema, sha, point-key, not-one-of-31, S1-gate and distance checks. It is read only for a token or key that none of the 31 rows takes.

NOTES (none blocking)
- N1: The S1 positive tests cannot be reproduced outside root's folder (canonical pins by design). They rest on root's in-place run.
- N2: If the case block cannot be read, KS1 and the KS6 handoff treat the spec as non-S1 (K4 path), which refuses an S1 spec, and KS5 returns None and refuses. Both fail closed.
- N3: The KS6 handoff's load_deps accepts either adapter pin. A non-S1 call is delegated to 5ff464cc, which refuses the KS6 pin (fail closed).
- N4: Necessary, not sufficient (README section 7): the enumerator, evidence and SRB successors and the rho prelaunch check (KS4'/KS5'') come with the G-wave. S1_UA_C3T needs its own KS5-bound C1.
- Not re-run by me: the ported predecessor suites (295/222/129/54/25); root's FINAL_PORT_* runs cover them. KS3 runner, KS4 assembler, KS5', KS6 lo_core and the adapter were not read line by line. Their differential tests pass in my copy.
