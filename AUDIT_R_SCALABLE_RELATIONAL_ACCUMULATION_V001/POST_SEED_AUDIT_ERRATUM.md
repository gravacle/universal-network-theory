# Post-seed bounded audit erratum

The independent hostile read found two non-physical reporting/custody defects
after the L4/L6/L8 target and blind rows completed:

1. `PROTOCOL.md` labels one-complex128 state sizes as `7.38 KiB` at L4 and
   `10.96 MiB` at L8. The exact binary sizes are `7.734375 KiB` and
   `11.222397 MiB`. The byte formula `16 D_L` and all exact dimensions are
   correct; only those two displayed unit conversions are wrong.
2. Five checks in the original preflight look for
   `TARGET_DIR/HISTORY_L*.json`, while target workers write
   `TARGET_DIR/RAW_HISTORY/HISTORY_L*.json`. The pre-output freeze commit
   `a0e88add861298c6ae2cd6af883c8080779f366a` itself contains no target or
   blind raw history or aggregate result. The supplemental verifier checks
   that commit tree at the exact intended paths.

The reviewer also recommended replacing the target/blind JSON's hardcoded
`blocked_null_state_error=0` with a preserved structural certificate. The
supplement independently reconstructs the source and blocked basis supports
at L4, L6, and L8 and proves they are disjoint. This certifies that the local
admission generator has no matrix element on a loaded/occupied blocked source.

No raw history, interval, threshold, observable, classification, or claim
boundary is changed. The original frozen protocol and preflight remain
preserved; this file is a dated correction and audit supplement.
