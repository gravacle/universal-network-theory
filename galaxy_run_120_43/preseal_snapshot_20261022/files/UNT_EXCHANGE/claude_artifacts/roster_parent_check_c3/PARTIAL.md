2026-10-22T14:17:54Z backlog #7 build started (D038): wrapper roster_builder_parent_check_c3v001.py written; tests next (real build/pass/step7/custody via test_inherited_cx3v003 world).
2026-10-22T14:23:01Z test_roster_parent_check_c3v001.py written (real step7 + custody commits via the cw8 inherited world; custody breach by chmod); first run next.
2026-10-22T14:23:42Z test v001 aborted at custody H2 (base custody main lets the post-commit FileNotFoundError escape uncaught); v001 kept as draft; v002 records escaped exceptions.
2026-10-22T14:24:19Z test v002: 28/36, 8 failures were a test bug (ledger() read inside the READS window); v003 fixes the window.
2026-10-22T14:25:12Z test v003 36/36, 5/5 mutants; README written; review request to Codex1 next.
2026-10-22T14:30:48Z Codex1 0295 B7-1 (abspath vs kernel '..' through symlink) accepted; wrapper c3v002 written (raw-prefix parent); test v004 next with Codex1's 3 controls.
2026-10-22T14:33:03Z c3v002 46/46, 7/7 mutants (record dca25dcd); README C3V002 written; delta review request to Codex1 next.
2026-10-22T14:38:49Z Codex1 0297 B7-2 accepted (trailing-slash symlink follow); c3v003 written; kernel matrix 14/14 agree; test v006 next.
2026-10-22T14:40:33Z c3v003 51/51, 9/9 mutants, K1 14/14 kernel agreement; README C3V003; delta request to Codex1.
2026-10-22T14:46:44Z Codex1 0298 B7-3 accepted (realpath hides missing component before '..'); c3v004 written (raw readlink chain); 22-shape matrix agrees; test v008 next.
2026-10-22T14:48:16Z c3v004 55/55, 11/11 mutants, K1 22/22; README C3V004.
