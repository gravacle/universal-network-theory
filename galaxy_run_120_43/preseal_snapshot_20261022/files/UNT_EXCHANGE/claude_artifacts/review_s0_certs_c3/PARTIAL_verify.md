# PARTIAL_verify.md (adversarial verifier of the Claude3 S0-cert static lens; append only)
2026-10-19T16:17:21Z start: read CURRENT_INSTRUCTIONS.md; scratch at /private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/71ea3fb2-2be2-4b38-b919-d6ca63cf052f/scratchpad/s0certs_review/verify/
2026-10-19T16:17:58Z read posts 0199 (5baa7864), C3/0184 (ae3cbb5a), 0693 (24166a6d), 0694 (c6dd59f1), 0685 (92d9943c), 0708 (f136e96a), 0711 (84f75d01)
2026-10-19T16:18:36Z shas from bytes match: producer 8972822b, fence b5a6aa09, EPS efdc430a/8270b6b3/bfac8f57/5dd9900a, GQ 903a7d6c/cc6113ce/4fc1d744/934c0a47, GQ writer f4ee064d, S0 1be5ed70, pred 79a5ac1d/175b995b, r1 b349379a, review e6bcca96, pins c0390172
2026-10-19T16:19:12Z read producer 8972822b in full (665 lines)
2026-10-19T16:20:25Z read S0 record 1be5ed70 and s0theta_c4v001 (950d774a)
2026-10-19T16:20:54Z read qinf_eval L70-160 (f58de0dc), certs_common PINS/pin/qinf_binder/q_of (1946a394)
2026-10-19T16:21:33Z read pinload_c4v002 (b8ae4b06) in full; guard_report cls = given in RUN_INPUTS (L308-309) confirmed
2026-10-19T16:22:56Z structure of records, r1 b349379a and GQ binding read (json only)
2026-10-19T16:23:30Z rec_check: 4 records sha ok; keys recompute (29-key, both forms); Eeff/geff bitwise; 89 shells 0 defects; eps=max(env,act) all shells; all envelope; CERTIFIED; custody 24 true + 3 write=false; run-tree opens 3/3/4; refused 0 blocked 0; no 43-list, no km/row keys
2026-10-19T16:23:58Z physics.py: N2 exponents reproduced (J0 -5.5e-8..2.2e-8; J1 -0.99999999..-0.99996569; J2 -3.0000000..-2.9998960; max dep 7.9e-6); N3 seed-vs-r1 env 3.29e-9, base 2.1e-9, dense 4.6e-9, actual onset (22,23], max 19.75% at (49,50]; (65,66] 1.0119 vs 1.1460; seed-vs-J0 actual -16.6%..+14.4%, eps 3.8e-9
2026-10-19T16:24:26Z iters.py: env/actual iteration counts differ seed-vs-r1 from (2,3] while env start values agree ~1e-12..3e-10 through (32,33]: rng stream not path-dependent; local-search path sensitivity only (supports N3)
2026-10-19T16:25:33Z read fence_c4v004 (b5a6aa09) in full: D1(a) lexical casefold rule L120-129, pin exception first L229-230, no-follow walk L172-222, os.open wrapper L324-331, selftest policy-only
2026-10-19T16:25:47Z read runner run_fenced_c4st4 (9327b0b5); selftest count 8+76+14+1=99, runner probes 7+25=32 from code
2026-10-19T16:25:54Z stderr summaries: 4 EPS + 4 GQ runs selftest 99/99, probes 32/32, blocked_after [], rc 0, script shas 8972822b / f4ee064d
2026-10-19T16:26:28Z read GQ writer gq_binding_c4v002 (f4ee064d): L119 reads V006 addendum (N5 FORMAL ok)
2026-10-19T16:26:56Z timing_guard.py: 40 program files + 3 pins per run; only NGC3198-named opens are the 2 pins; no ROOT_DECISIONS; refused/blocked empty; walls 1700.374/1695.22/4379.069/4379.501; cpu/runnable 0.83/0.83/0.26/0.26; QoS bg 1233.8/1230.1/1168.5/1168.1; J1 cpu 740 s at t=2402; step2 13.3..16.8
2026-10-19T16:27:05Z gq_check.py: 4 bindings sha ok, bind be148bab (bytes verified), 545.0, PASS, no compute, open item carried, V006 read ad07fd42, utc 13:48:41Z
2026-10-19T16:27:39Z read eps_ngc91_c2v001 (2e59a461) main L42-121; run_eps transcription checked: rng consumers L55, env_search L75, actual_search L78, audit env_search L107 same order; dropped L47-52, L62-66, L74, L79-83, L92-95 consume no rng (FORMAL)
2026-10-19T16:28:15Z c1_check2: seed eps == anchor r1 flat eps within 3.3e-9 on lo>=5; (2,5] raised x1.277/1.639/1.326 by rule (b); anchor-only inputs never exceed envelope at r1 (dropping them cannot lower eps)
2026-10-19T16:29:17Z smoke1 (febaa666) vs r1: (2,9] rule/dense/env/actual bitwise equal; audit differs by rng position as cmp1 (1bde21a8) states
2026-10-19T16:29:37Z lwr_common (758740eb) Binder L92-166 uses only self.Eref/self.ell/self.gam (FORMAL item 1 holds)
2026-10-19T16:30:07Z chain modules: certs_common uses ANCHOR_UNSCALED only in qinf_binder/repro (not called); eps_cert_c2v002 L.SEED only in its main (not called); certs2 Envelope uses B.* and L.A_BRAVAIS only: binding reaches numerics (FORMAL)
2026-10-19T16:31:46Z diffs: stored producer/fence diffs == fresh diff -u (bodies fc99c573 / d0f05389); 5 and 3 hunks; ast: CHAIN/LWR_COMMON unchanged; removed COMPARE/DDO_ANCHOR_KEY/FIELDS/POINT_NOTE/rel; DATA lost 5 anchor files (N8 ok)
2026-10-19T16:32:02Z custody: 24 true flags enumerated (tables 3, pre/post 2, nofollow, seedscan, lwr parse 9 incl ANCHOR_CHECK 3, lwr ok, only-pins, root25 named, reader identity 5); grid_check true; thread env 1; nice 0
2026-10-19T16:33:25Z pins_cmp: fence PINNED_RUN_INPUTS and loader RUN_INPUTS (ast-folded) == root pin file c0390172 completed_run_inputs
2026-10-19T16:33:36Z rng_stream: envelope start_values agree with seed on all 89 shells (r1 2.7e-9, J0 4.8e-9; J1/J2 = power law to 7.9e-6) and audit dense values agree: rng consumption data-independent; actual-set spread is deterministic local-search path sensitivity (sharpens N3)
2026-10-19T16:33:54Z read BUILD_NOTES_C4V001 (ec25ee9b)
2026-10-19T16:34:59Z diffs shas == BUILD_NOTES s6; FENCE_SELFTEST t1 ed4d6e63. VERDICT: lens holds (holds=true). Minor non-material corrections: N3 audit band 1-3.0e-9..1+1.01e-9 (not +-1.0e-9); N3 actual onset (22,23] not every outer shell; N6 write=false also forced by guard. No reclassification. Own NOTEs: custody hard gate L579-582 omits guard_refused/fence_blocked; runner summaries byte-identical across runs (52acd8ee EPS, 47ff7def GQ). Conduct: builtins (echo/printf/date/set/cd) and scratch-only cat-heredoc/head/tail/wc/shasum ran without -b; all program-tree reads/lists/hashes/diffs/python used taskpolicy -b; python imports json/hashlib/ast only; no NGC3198-named file or run-tree path opened/listed/stat-ed.
