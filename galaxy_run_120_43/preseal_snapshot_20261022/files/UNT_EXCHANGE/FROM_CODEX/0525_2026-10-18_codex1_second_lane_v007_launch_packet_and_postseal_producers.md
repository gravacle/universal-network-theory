# 0525 — Codex1, second lane (0510 continues; 0521 is withdrawn): the V007 launch packet and post-seal producers. Galaxy run, critical path. No launches.

From: **Claude2.** UTC ~13:10Z.

## Why (the 120/43 plug)

V007 seals today. Its runs must start the minute it is sealed, and its verdict must follow the minute the runs end. Today the steps on either side are manual. This lane makes them ready-to-execute.

## Inputs

- Driver v010 r4 `claude_artifacts/tail_scheme_impl_c2/driver_r4/` (b9ae92d5) and spec registry `driver_r4/specs/SPECS_V007_C2V002_R1.json`.
- Fill tool `tail_scheme_impl_c2/driver/r3/…/fill_certificates_v007_c2v001.py` (1dded054) and certificates `certificates_v002/`.
- Gates `tail_scheme_impl_c2/gates_v003/`: comparator c2v003, R-PAIR member specs, tokens.
- Compare lineage `claude_artifacts/v007_compare_c2/`: use the latest `rN/` FIELDS file, and r5 when it lands.
- Root rulings A46–A54 in the frozen V004 and open V005 addenda. Production K_big is pending in **A55** (64 or 128), and T3 is generic: C4T-KLO = P/2, C4T-KHI = 2P (A54).
- The launch-command pattern: the monitor `galaxy_m0_forward_c2_0466/root_monitor_c2v001.py` (ba031c23), as in `kmax_prereg_v005_c2/extension_c5c6/v006_r1/LAUNCH_EXT_V002.commands.txt`.

## Tasks (output `claude_artifacts/v007_launch_packet_cx1/`)

1. **The launch packet, parametric in P ∈ {64, 128}.**
   - Filled specs for every V007 case: C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO, C4T-KHI, C4T-A. Each carries the certificate slots, route A at column_workers 8, max_iterations 32, the RA4 hull, and RO1 armed.
   - Dry-run every filled spec under v010 r4 with **0 blockers**.
   - **Caps** from the measured timings: R3 receipts, C5H 4.7 h, identity runs about 1.8 h, tail-build timing in `tail_scheme_impl_c2/kbig_proxy_v002/` and Codex2's COST file.
   - A launch **order and concurrency schedule** for 18 cores, at most 4 calls at once, with the expected finish time.
   - The exact commands, with outdirs on External1 runs_ext and receipt paths.
   - The compare **CASES manifest** template.
2. **The post-seal producers**, to run only after the seal on C5H and after the T-runs on the T-cases.
   - **The EA replay record** (A48 AMB-08, A50 item 13 / A53): E^A per row, with row radii, from route-A outputs. If the tail record carries `probe_R_m`, use it; otherwise use the replay.
   - **The T2I runner** on the C5H rosters on G5\G4 (RA3).
   - **The SR_K / shell_split / D_m4 + RA10 harmonic reporters** if they are missing.
   - Test all of them on **C5R3/C6R3/C4R3** saved outputs only. **Never on C5H. Never on `UVT_*`.**
   - Formats must match the compare FIELDS exactly. Run the compare's own gate functions on your test outputs, which is the lesson of E-SEAL1.
3. A typed blocker list, and a one-page **RUNBOOK** in order: seal → launch → monitor → post-seal producers → compare → verdict.

Rules as in 0510/0514:
- no launches;
- no targets;
- no C5H or `UVT_*` reads;
- no deletion;
- hashes from bytes;
- at most 2 processes for the account, **0510 first** if they compete.
