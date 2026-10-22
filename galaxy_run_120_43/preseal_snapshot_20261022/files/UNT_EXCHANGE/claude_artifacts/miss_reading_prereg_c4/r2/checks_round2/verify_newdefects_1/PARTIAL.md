# PARTIAL — verify_newdefects_1 (finding R2B-01)

Started 2026-10-18T20:30:57Z (date -u). Lens: adversarial verification, refute by default.

Status: folder created; hash check of round2 object pending.

## 20:3x-20:45Z progress (date -u stamps at write: see end)

- Object hashes: all 9 listed files match HASHES_R2.txt from bytes (PREREG 97d5ce33..., MAP 38cd6852..., ROOT_ITEMS 4907cf01..., NUMBER_PROVENANCE ff6ca9b8..., TF_CHECK 624f278e..., TF_MUT 4445a9bf..., tools 4ae4f705 / dc812342 / 2132078f); HASHES_R2.txt itself 2e3cf0c6...
- V005 read at 2026-10-18T20:34:29Z: sha256 7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2 (1462 lines). A98.2 at L956-959 confirms the core defect text.
- 0619 238858d1..., Codex2 0490 3a922168..., Codex2 REVIEW_CX2V001 7e3b6211... read.
- Quotes L119, L209, L212, L324, L487, L492 verified in PREREG bytes.
- v003g module 48a1e48a...: _ladder_row (NON_FINITE_SIGMA_RATIO only if residual/sigma non-finite; scorer requires sigma finite > 0, velocity finite); _root_result_rows: a gate applies only to rows the producer reported valid:false -> a gate cannot invalidate a producer-valid row.
- Working hypothesis: core (a) confirmed; (b) confirmed for C16b; C16d not an instance; (c) conclusion holds but the lens witnesses (C16a/b, C16c/d, C17c/d) change the producer output, not a gate decision. Fix has gaps (unqualified S rule in JSON text; L201 makes P14/P15 never hold; P6 under value semantics; finding's threshold makes S depend on gate timing).
- Next: independent synthetic reproduction script in tools/.
2026-10-18T20:41:44Z

## Progress: reproduction done
- tools/verify_r2b01.py (own classifier from the r2 text; no lens code imported) -> VERIFY_R2B01_RESULTS.json; tools/verify_r2b01_edges.py -> VERIFY_R2B01_EDGES.json. Fence installed; no file reads except own script.
- r2 text, 40,000 synthetic outcomes: OUTER_FAILURE def1 != def2 in 1585 = exactly the outcomes with N_v(OUTER)>=1 and every non-INVALID OUTER row unsigned (0 others); coverage failures 21, all of the characterized form; sign-class pattern with zero signed misses 3712.
- Early vs LATE gate on the same producer-INVALID rows (r2): m, defined S, Delta_out, GROWING never change; P1, P1g, P2, P3, P4, P6, P11, P12, P13 never removed; removed P5 2023, P7 149, P8 1, P9 415. So C17c->C17d (P1g) is a producer-output change, not a gate effect (G4: Delta_out +1 under both).
- Fix: FQ/explicit works (0 disagreements, 0 coverage failures); FQ/strict (L201 literal) makes it worse (18702 disagreements, 1401 coverage failures); FJ (unqualified) + value semantics gives P6 on the all-hit outcome; FQ threshold makes sign classes depend on gate timing (P1 removed 2243, P1g 731, P6 556); alternative FB (withhold iff miss-dominated and M-U < H) keeps 0 changes.
- V005 re-read 2026-10-18T20:48:24Z: 70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e (A101 added); A98 section L965-977 sha 181248d9...; content unchanged from the 20:34:29Z read.
- Next: VERIFY.md, REVIEW.md, HASHES.txt.
2026-10-18T20:49:49Z

## Final
- VERIFY.md and REVIEW.md written. Outcome: R2B-01 NOT REFUTED; BLOCKING confirmed; fix not sufficient as written (L201 trap, unqualified S rule in JSON wording, gate-timing dependence of the M-U < N_v/2 threshold, incomplete edits). Better fix: withhold S iff Z miss-dominated and M-U < H; exempt P14/P15 definedness tests from L201; P6 requires defined S.
- HASHES.txt written last.
2026-10-18T20:53:15Z
