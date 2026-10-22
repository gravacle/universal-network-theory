# V006 section excerpts for 0817

Wed Oct 21 11:43:22 UTC 2026

Source /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md SHA256 1e70df1e53b74446ee33d002dd3bc0725519a1cd39f13b99a56b9c2d43c26531

460: ## A133: two-phase protocol, a fast provisional result then full validation (principal's direction; 2026-10-19 10:43Z, before any step-4 result)
461: 
462: **Why.**
463: - **The principal's direction:** "arrive at a high confidence result first using less compute intensive path and then continue with the higher overhead approach as complete validation."
464: - **Text of record:** `A133_TWO_PHASE_PROTOCOL_V001.md` (`cd92ef91`). It is a root workflow draft: one drafter, two refuters (integrity and feasibility), and a synthesizer.
465: 
466: **Adopted as written, with the build owners changed below.**
467: - **Phase 1** adds no DDO calls. It is a read-only snapshot of the registered campaign at B_P1, the forward calls before its first `march0` call. Its estimate u_A is the engine's own `primary_anchor`. NGC runs at the snapshot's v003g members plus three FD points.
468: - **Phase 1 result.** It is frozen as FREEZE_INCOMPLETE and scored as PROVISIONAL (PHASE-1).
469: - **Phase 2** is the registered step 4 and the full step-5 set, **unchanged**. It runs and is scored whatever Phase 1 shows, and it is the score of record.
470: - **The agreement test** (section 4: AT-0a, AT-0b and AT-1, with the allowance from τ_i = 0.25σ_i and hull_growth_tol) is frozen now. Its outcomes are COVERED, SUPERSEDED and NON_DISCRIMINATING.
471: - **Blinding order.** The section-2 order is adopted as written. Above all:
472:   - no Phase-1 NGC launch before r3a is published as a SEAL CANDIDATE;
473:   - no Phase-1 NGC value is read before r3a and the M-12 classifier are sealed.
474: - **Not adopted:** Gauss–Newton or Broyden steps beyond the engine's registered repair (section 9).
475: - **The NGC serial/8-worker identity pair** (A132) is the first NGC launch.
476: 
477: **Build owners (0678 and 0680 credit limits).**
478: - **Root workflows:** `phase1_c2v001.py` (snapshot, handoff, fdplan, band, agree); the roster builder and RUNBOOK_V002; the S1 template and launch path. Claude3 reviews each.
479: - **Claude4:** r3a (the re-render, as SEAL CANDIDATE) and M-12 classifier A.
480: - **Codex1:** M-12 classifier B, the only build that needs a different lineage, plus single-pass reviews of r3a and the RI45-06 producer.
481: - **RI45-02 and RI45-08:** root workflows, with Claude3 reviewing.
482: 
483: **Indicative timeline (CDT; UNTESTED; T0 is the step-3 verdict):**
484: 
485: | Milestone | Low | Expected | High |
486: |---|---|---|---|
487: | Phase 1 scored | Thu 10-22 | **Sat 10-24** | Sat 10-31 |
488: | Phase 2 scored | about Mon 11-02 | **about Thu 11-05** | about Sun 11-15 |
489: 
490: The scheduling-fix successors (budget 20/24; `sched_s45_c2`) are ruled separately when their workflow returns.
491: 
530: ## A135: the step-5 NGC path for Phase 1 (root build `step5_path_c2`, verifier 0 blocking) and the S0 rulings (2026-10-19 12:40Z)
531: 
532: **Objects:** `claude_artifacts/step5_path_c2/`. README `fba1a70a`, HASHES `27fb117f`; 83/83 in two record runs; verifier 0 blocking.
533: 
534: | Object | sha |
535: |---|---|
536: | POLICY_C2V001 | `0c781a17` |
537: | Serial template (column_workers 1) | `68a19360` |
538: | CW8 twin template | `1aa66269` |
539: | Filler | `ec417e76` |
540: | Point handoffs | `7d3b7c3c` |
541: | Identity comparator | `8e857fff` |
542: | STEP5_REGISTRY | `38a75614` |
543: | Caps | `e7fa8c58` |
544: 
545: **Rulings (item numbers follow the build report):**
546: 1. **Adoption.** The path is adopted on Claude3's review (lean; due Mon 10-19 20:00 CDT). Adopted with it: RI45-02 (a), RI45-08 (a, cx3r008 only), RI45-12 (a, interface A), the Phase-1 handoff schema (`A133_PHASE1_POINT_THETA_FIXED_TARGET_FREE`) and the new label rule.
547: 2. **S0 certificate pins.**
548:    - **EPS:** each S0 point's own record, from Claude4's S0 successor, with rule (b) per 0693.
549:    - **GQ:** re-bound to `be148bab`.
550:    - **`uv_tail.lo_certificate`:** under A134, the per-point registered ρ record at that S0 θ (NGC geometry).
551:    - **Post-run per-state LO acceptance (Q2/Q3) applies to NGC calls as to DDO calls.** Claude3 extends its slot-proof producer to NGC S0 points, or posts by 17:00 CDT that it cannot; root then builds it.
552: 3. **Caps.**
553: 
554:    | Call | Wall | RSS | Output |
555:    |---|---|---|---|
556:    | Serial | 610,324 s (2× the U estimate) | 32 GiB | 64 GiB |
557:    | CW8 twin | 22,752 s | 86 GiB | 32 GiB |
558: 
559:    The twin's planned stop after iterations 0–1 is not a failure; the twin is never a member.
560: 4. **The identity verdict compares 2 iterations,** which covers the first warm-state transfer.
561: 5. **Memory.** The identity pair runs only after step 2's last receipt. Root extends the memory watch to NGC processes and labels its units GiB.
562: 6. **RI45-05.** The V007 adoption pin is the sealed compare's verdict report.
563: 7. **C1 is the tail-era CX2V006 lineage** (v006r9 `721c7230`, plus the s45 scheduling successor once it is reviewed). S0 is identical under V005A and CX2V006 (TESTED). AT-0a re-checks this at the Phase-1 freeze.
564: 8. **RI45-24 (PAR8-SF1)** is root's V006 entry, before T0. RI45-25 comes before the first step-5 result.
565: 9. **RI45-13** applies per launched spec: a fresh dry plan with the real pins, the spec sha registered, and a driver sha check. Root reads the blocker lists.
566: 10. **phase1 `handoff`** needs a successor that supports one certificate map per member, before any member after u_A launches. S0 is not affected. Root builds it by Wed 10-21.
567: 11. **The carriers successor** is adopted before any carrier is extracted from a step-5 result.
568: 
590: ## A137: the Phase-1 tool (34eaef36) passes review; three rulings fixed before their deciding moments (Claude3 0191) (2026-10-19 13:05Z)
591: 
592: - **Review.** Claude3 0191: 0 blocking, and the verifier holds.
593: - **N-C, campaign config freeze (before W1).**
594:   - Any campaign-config change, **including the sched v002 config `05a2f987`**, lands before campaign wave 1.
595:   - From W1 until the `march0` plan is written, no campaign-config edit is allowed.
596:   - Root keeps the exact prefix-config bytes, as a byte copy, and passes them to snapshot, handoff and at0a.
597: - **N-B, the AT-1 FD-noise term e_q (before any at1).** e_q is the **member-displacement bound Σ_k 2ε_k |Δ_m,k| / h_k**: the FD truncation bound of the linear map at member m's own displacement.
598:   - The tool's band-optimum reading does not bound the K-error, so it is not used.
599:   - This is fixed now, before any number. A133 §4 is amended accordingly (erratum E_A133_1).
600: - **L5, B_P1 on a corner anchor with no `march0` wave.** B_P1 is the number of forward calls before the first call whose family is outside {seed, jacobian, repair, gd_pre}. This generalizes "first `march0`". Root builds the one-line successor, and Claude3 reviews it.
601: - **Process deviation, recorded (register).**
602:   - Claude3's review lens ran one unfiltered recursive grep over `claude_artifacts/` for about 2 min. It printed about 10 bytes of `*.py` names, showed no file content and used nothing.
603:   - The traversal could include `c5h_hull_c2/`. C5H blinding ended at the V007 seal (07:00:44Z), and no NGC3198 target content was printed.
604:   - Remedy: lane helper prompts forbid broad recursive grep or find; only named paths are opened.
605: - **phase1_c2v002 (root build, 13:40Z).**
606:   - Object: `phase1_c2v002.py` (`d64351ec`), tests `b1aedebc`, HASHES_V002 `af8509bb`.
607:   - Tests: 103/103 in two record runs. The root verifier read PASS, 0 blocking. Only L5 and N-B change; the march0-boundary outputs are byte-identical to v001; corner seeds pass.
608:   - **Ruling, before any at1:** ε_k in e_q is the row's L1 `eps_q`, the largest ε over u_A and the three F points, applied to every axis. It is a valid bound, possibly loose. A tighter per-axis ε would need a new at1 input and is not adopted.
609:   - Claude3 reviews v002.
610: - **Second process deviation (Claude3 0194), recorded.**
611:   - What ran: about 13:34Z, one unpruned `find claude_artifacts -maxdepth 3 -name <driver file>` by a verifier whose prompt predates A137.
612:   - What it touched: it listed names only inside about 20 folders whose names contain runs or C5H. It read no file, and C5H blinding had already ended.
613:   - Effect: none. Later prompts carry the named-paths-only rule.
614: 
645: ## A140: sched v002 decisions before W1 (Claude4 0192: 0 blocking) (2026-10-19 14:25Z; recorded 14:55Z)
646: 
647: **Recorded late.** Dispatch 0706 published this ruling at 14:25Z, and root then omitted it from this file. It is entered here as erratum E_A140_1, with the text unchanged.
648: 
649: - **N1.** The machine gate gets per-driver foreign-tree classes: an NGC class for cx3r008 serial trees, sized from Claude4's RI45-12 estimate, plus a cw8 twin class. Root builds gate v003, re-simulates with S0 ×4 plus the twin, and Claude4 reviews the delta.
650: - **N2.** The cw8 twin runs only when no DDO route-A call is in flight. Campaign and direct admissions are held for its ≤ 22,752 s. It is not on the critical path.
651: - **N3.** The S0 NGC output cap is 136 GiB, superseding A135's 64 GiB. NGC outputs go to External1.
652: - **N4.** Root re-derives the DDO per-call wall from the step-2 receipts before W1.
653: - **N5.** The DDO output cap is 80 GiB, to be confirmed against the receipts.
654: - **V2** is decided at H3.
655: 
656: All of this lands in the campaign config before W1 (A137 N-C).
657: 
658: **r3a SEAL CANDIDATE (Claude4 0194).**
659: - **Text:** `miss_reading_prereg_c4/r3a_sc2/PREREG_MISS_READING_R3A.md` (`9a2f177f`); ROOT_ITEMS_R3A (`63f1bf74`); classifier "none" until M-12 is built.
660: - **Gate:** the hard gate before a Phase-1 NGC launch (A133) is **met**.
661: - **Before the seal:** root rules M-1 to M-16. The seal comes before any Phase-1 NGC value is read.
662: 
663: ## A141: the step-5 NGC path is adopted (Claude3 0200: 0 blocking); launch rules L1–L4; a conduct note (2026-10-19 15:02Z, the time 0707 was published; the header first read 15:10Z, erratum E_A141_1)
664: 
665: **Adoption.** A135 item 1 is satisfied. The `step5_path_c2` objects are adopted as built.
666: 
667: **Launch rules:**
668: - **L1, output cap.** The NGC serial output cap is **136 GiB** (A140 N3), above Claude3's suggested 96 GiB and the derived U total. An OUTPUT_CAP stop under A133 §3(c) is rerun with the output cap raised. A cap is not a physics input, so this changes no value.
669: - **L2, units.** The gate's campaign reserve is **29.1 GB**, from 27.1 GiB in consistent units. Gate v003 states every threshold in one unit, and Claude4's v003 delta review checks it.
670: - **L3, path spelling.** The comparator's `--serial`/`--twin` are spelled exactly as root_monitor's `--outdir`, in absolute `/Volumes/External1/...` form, never through the `runs_ext` link.
671: - **L4, twin stop.** The twin's planned stop is root's kill trigger once iteration 1 is COMPLETED and its sidecar iteration record exists. That keeps the pair inside the gate's spike window. Any twin cap stop is planned, not a failure.
672: 
673: **Text errata to the step5_path_c2 README (L5, L6; erratum E_S5P_1).** These are recorded here, and the pinned bytes are left unchanged.
674: - "RI45-02 (a) and RI45-08 (a) closed" holds for the S0 path only.
675: - HASHES has 29 entries.
676: - The registry omits the comparison-spec .md, which HASHES does cover.
677: - The threshold is 8.79 GB.
678: 
679: None of these changes a code path or a value.
680: 
681: **Conduct (register).**
682: - Claude3's lens opened `NGC3198_FREEZE_SLOTS_CX3V003.json` (`d3859b42`), which its prompt rule did not name as a model file. The verifier showed the chain did not need it.
683: - Claude3 confirms whether the file holds any observed NGC3198 velocity. Until it does, the item is recorded as an open blinding check.
684: - **Blinding check closed (15:10Z).**
685:   - Claude3 0202 confirmed it from the transcripts: only the two geometry slots reached any output.
686:   - Root then took a structure-only listing of `d3859b42` (key names, types and lengths; no values printed). It holds the 43 query rows with radius and index fields only (`Rad_text`, `radius_kpc`, `query_id`, `data_row_index`, GL4/GL10 flags, N2 truncation), the geometry and projection slots (distance, inclinations), alternatives, citations and truncation pins, and a `target_free` field.
687:   - **There is no velocity, error or rotation-curve field. Blinding is intact.**
688: - Remedy: prompts now name every NGC3198-named file a lane may open.
689: 
746: ## A143: sched v003 machine gate is adopted pending Claude4's review; the disk guard and the identity-pair order (2026-10-19 15:28Z)
747: 
748: **Build.** Root workflow wf_cfaab36f, at `claude_artifacts/sched_s45_c2/v003/`.
749: - HASHES `ca1eadca`; gate `736a3438`; config `d9241676`; CAPS `35f66b6a`; direct params C2V003A `4adc296b`.
750: - Tests 176/176. The verifier found 0 blocking and 13 notes (NO_FIX_NEEDED `fba85ff1`).
751: - With no cx3r008 tree on the machine, v003 decides exactly as v002. W1 no longer halts at U, and the twin spends 0 h beside DDO route A.
752: - **Adopted, subject to Claude4's delta review returning 0 blocking,** including the L2 units check (A141). It lands before W1 (A137 N-C).
753: 
754: **D1, disk guard (verifier note 4).**
755: - With the 80 GiB guard, engine wave 15 (24 calls) would need 1,940 GiB of free space and would halt.
756: - **Ruling:** the guard is separated from the cap. `disk_guard.per_call_bytes` = 2 × the largest per-call output measured in the step-2 receipts, rounded up to a whole GiB. Root re-derives it together with N4 at step 2's end, in one config successor before W1.
757: - Unchanged: the per-call output caps (DDO 80 GiB, NGC 136 GiB) and the per-start check (one output cap plus 20 GiB).
758: - The guard only sizes admission; it changes no value, and the cap still stops a runaway call.
759: - **Storage forecast.** Root computes it from W1's measured outputs (campaign plus step 5, against External1 and internal free space) and assigns volumes before the first step-5 call. External1 stays connected.
760: 
761: **D2, identity-pair order (verifier note 5).**
762: - The twin and a serial NGC tree in route A cannot be admitted together (83.7 > 83 GB).
763: - **Ruling:**
764:   - The serial S0 calls of record launch first.
765:   - The twin, at the same θ, starts when the gate admits it: no serial NGC tree and no DDO route-A call in route A, and only between HEADLINE and W1 or between waves (note 2).
766:   - "Pair" in A133 §1.4 means the same θ, not the same start.
767:   - The twin stays off the critical path (A140 N2), and it is killed after iteration 1 (A141 L4).
768: 
769: **D3, launch form (notes 1 and 2).**
770: - The monitor command must carry exactly `--driver-sha256 <64 hex>` and an absolute `--spec`.
771: - Root's twin launch script refuses any other form, confirms that `--hold-check` exits 3 once the twin is up, and refuses to start mid-wave.
772: 
773: **D4, serial class (note 7).** If an S0 call's measured route-A peak exceeds 22.4 GB, root builds a gate successor before admitting any further NGC call. The watch alerts on that peak.
774: 
775: **D5 (note 9).** A DDO tree whose pool has closed is not "in flight" for step5_path L146. The rule exists to prevent memory spikes, and a closed pool has none.
776: 
777: **Errata, with no rebuild:**
778: - note 10: the test docstring;
779: - note 11: the "16–28 h faster" claim is overstated, and the README table governs;
780: - note 12: the N4 rebuild must name C2V003A (`4adc296b`) as its predecessor;
781: - note 13: test portability.
782: 
899: ## A147: gate v003 adopted (Claude4 0203: 0 blocking, 13 NOTEs); rulings L3-01, L3-02, L3-03 and L3-06 before W1 (2026-10-19 16:35:44Z)
900: 
901: **Adoption.** sched v003 is adopted (A143), as the gate for W1 and for every cx3r008 launch.
902: - Claude4 0203 found 0 blocking. Its verifier refuted none of the 13 NOTEs, and 0204 is an erratum to L3-06.
903: - Units, computed values and the per-driver classes HOLD.
904: 
905: **L3-01, the disk guard. A143 D1 is withdrawn; option (a) is adopted.**
906: - The parent orchestrator refuses a guard below the cap (`c75a889f` L1747-1749, test K04b). So the guard stays at the 80 GiB cap.
907: - Wave 15's need, 24 × 80 GiB + 20 GiB = 1,940 GiB free at admission, is met by volume planning, not by the guard.
908: - **Measured.** One step-2 case (C4T_D5) is 17.4 GB. External1 has 2,877 GiB free and the internal disk 1,024 GiB, read at 16:35:44Z.
909: - **Forecast (UNTESTED until W1 is measured):** about 120 × 17 GB ≈ 2.1 TB for the campaign, plus the step-5 NGC outputs. That is tight against External1 alone.
910: - **Rule.** Root re-forecasts from W1's measured outputs and assigns volumes before the free space on the campaign volume falls below the next wave's need plus all NGC outputs. If both volumes together cannot hold the program, root alerts the principal before W1 + 2 days. No deletion; only verified moves.
911: - **Unchanged:** the wall cap is still re-derived at step 2's end (N4). It needs a build_params successor (L3-08) that also names C2V003A (`4adc296b`) as its predecessor (A143 note 12).
912: 
913: **L3-02, units (A141 L2): relabel only.**
914: - 72 and 83 are the measured 72.0 and 83.2 GiB, kept as the stricter GB limits, and swap is stated in GiB. The net error is strict: 1.5 GB at d2 and 0.4 GB at d1.
915: - The limits are not converted to true GB. Converting them would admit the twin beside a serial NGC route-A tree, against A143 D2 (test G35d).
916: - The 29.1 GB reserve is root's A133 procedure for S0 admission. That admission takes the stricter of the A133 check and gate v003's `ngc_admission`.
917: 
918: **L3-03, the launch form applies to every cx3r008 launch, S0 included.**
919: - The form is exactly `--driver-sha256 <64 hex>` and `--spec <absolute path>`, each with a space; the `=` forms are not used.
920: - After each launch, root reads `--hold-check` runs[].kind and phase:
921:   - each S0 must read NGC_SERIAL;
922:   - the twin must read NGC_TWIN.
923: - If a run reads GENERIC or NGC_UNIDENTIFIED, root stops that launch at once, before it can hold W1. It is recorded as a procedural mis-launch, not a scientific failure, and relaunched in the correct form.
924: - The S0 launch kit (root workflow `s0-launch-kit`) carries this check.
925: 
926: **L3-06 (with erratum 0204), the 103 GB rule.**
927: - With S0 ×4 U peaks coinciding beside a gate-admitted DDO route-A call, the total can reach about 125-128 GB. That is over the A133 103 GB rule but below RAM. It is reachable but unlikely.
928: - **No gate successor.** It would cost campaign throughput.
929: - **Mitigation, which changes no value:** the A130 lever. The watch alerts when the total footprint passes 95 GB or swap passes 8 GB, and root SIGSTOPs Phase-1 NGC processes first (A133 §1.4).
930: - A jetsam kill fails closed and goes through rule (c).
931: 
932: **Noted, no W1 decision:** L3-04 (the D4 alert is in GB, measured by the A130 watch), L3-05, L3-07, L3-09 (any driver successor needs a gate successor), L3-10, L3-11, L3-12 and L3-13.
933: 
1457: ## A166: principal's direction to stop micromanaging the Mac's resources; memory gating is removed, RSS caps rise to RAM, and only hang, disk and correctness rules remain (2026-10-19 19:21:38Z)
1458: 
1459: **The principal's direction (verbatim):** "can we stop micro managing the macs resources? The macs tend to do that very well on their own when jobs are just run." It follows the 19:14Z vm_stat reading and A165.
1460: 
1461: **Ruling. This is timing-only: no computed value can change, because every computation is deterministic and swap or compression affect speed only.**
1462: 
1463: **Removed for every launch from now on:**
1464: - the machine-gate memory admission (sched v002/v003 d1, d2, knee and hard limits, NGC/twin classes, the twin hold, the route-A cap);
1465: - the A133 §1.4 103 GB rule;
1466: - the A143 D2 memory ordering and the A147 L3-03 kind check (both existed only to make the gate classify);
1467: - CP-1's physical floor and swap hold (from Phase B on);
1468: - the S1 overlap memory condition (guard012).
1469: 
1470: **Jobs now start as their own design and order allow.** macOS schedules memory, compression and swap.
1471: 
1472: **Per-call RSS caps rise to physical RAM, 137,438,953,472 B, for every new launch:** DDO 64 GiB becomes RAM, and the NGC serial 32 GiB becomes RAM.
1473: - A cap stop is value-relevant (A133 (f)), so a memory cap must never kill an honest run.
1474: - Raising a cap before launch changes no value.
1475: - Under A133 (c), the RSS-at-RAM rerun form is now the first-run form.
1476: 
1477: **Kept, because they are not memory micromanagement:**
1478: - the per-call **wall caps**, which guard against hung runs (A133 (c) reruns with the wall doubled);
1479: - the per-call **output caps** and the **disk admission guard**, because a full disk fails runs;
1480: - every correctness and custody rule (M-15, pins, kill of the twin after iteration 1 to save compute, identity comparison, and so on).
1481: - The A130 memory and swap **watch stays passive: alerts only, with no automatic throttling**. Root intervenes only on an actual failure.
1482: 
1483: **Running now, left untouched:**
1484: - step 2 (V007 R2, under its sealed launch);
1485: - CP-1 Phase A (pid 6974; A134 N2 forbids restarting with workers live).
1486: - CP-1 Phase B starts with allowance 0, margin 0, per-worker 0, k 8 and swap hold effectively off.
1487: 
1488: **Builds, before their first use, in one root workflow:**
1489: 1. **sched v004:** the campaign runs on the R9 config with the original campaign v005, which has no memory gate. It changes only: output cap 80 GiB, wall cap (A140 N4, from the step-2 receipts), RSS cap = RAM, disk guard. The direct-batch params C2V004 drop the hold predicate and the memory admission. Claude4 reviews the delta before W1.
1490: 2. **S0 kit C2V003:** launches root_monitor directly, with no gate admission or kind check, RSS = RAM and the twin free to start after the seed. Claude3 reviews the delta before the first S0 launch.
1491: 3. **guard013:** a POST_S1 overlap with the campaign is admitted with no memory condition. Claude4 reviews it in place of guard012, along with the S1 path.
1492: 
1804: ## A177: results of the A172 builds, roster builder c2v006 and NGC acceptance c2v003; rulings on their root items; the M-12 seal route (0751); the NGC roster recipes are commissioned (2026-10-19 20:49:32Z)
1805: 
1806: **sched v004a: ADOPTED** (`sched_s45_c2/v004a/`; config `63dac53de88303404c64e899856485bd912a4c493e44a93af0a6cb393240e4ec`; HASHES `72f9ac3a`).
1807: - Root verify: 0 blocking, 33/33 twice. Claude4 0236: PASS on the one leaf.
1808: - Only `max_concurrent` (1 → 8) and an appended note change. The cache id is unchanged.
1809: - The CPU process budget 17 limits concurrency to 5 calls (campaign L203).
1810: - **W1 wall rebuild (Claude4 0243 N1; builder item 1): the two-step path is ruled.**
1811:   1. Run the A140 N4 rebuild from the step-2 receipts.
1812:   2. Apply `SCHED_DELTA_S45_C2V004A.json` with apply v002.
1813:   3. Leaf-diff against v004a. Only the wall, the orphan wait and the notes may differ (TESTED, Y04A).
1814: - **The wall rule goes into the W1 record (0243 N2).** It states the receipts used (FINISHED/COMPLETED `elapsed_seconds` only, with their shas), the scaling to 32 iterations plus setup, post-loop and route B, the margin, and the contention factor.
1815: - **The 48 h wave cap (0243 N9).** With budget-bound concurrency, long waves may stop as INFRA with NOT_STARTED calls. Root resumes each from its verified receipts; no value changes. The apply-tool successor that raises `campaign_wall_cap_s` is built after Thu and reviewed after Claude4's Fri reset.
1816: 
1817: **S0 kit C2V003a: ADOPTED pending Claude3's C2V002 → C2V003a delta review** (`s0_launch_kit_c2/`, HASHES_S0_KIT_C2V003A).
1818: - **Results.** Root verify: 0 blocking, 28/28 + 84/84, the same row for row over two runs and the verifier's rerun.
1819: - **N1:** a 300 s parse wait.
1820: - **N4:** the twin's cap is RAM × 11, its tree's maximum process count confirmed from the driver bytes.
1821: - **R1:** the serial tree has up to 3 processes (route B column_workers 2). **The serial cap stays at RAM.** The measured serial footprint is about 22 GB under ps-sum, roughly a fifth of RAM, so in practice a RAM cap cannot stop an honest serial. Root applies the RAM × n rule if a serial ever passes half of RAM.
1822: - **R2:** if a launch record is still unparseable at the bound, the kit cannot stop the run, because it needs the record's child_pid (NOT_KILLED_TARGET_REFUSED, exit 5). **Root then stops the driver by hand** through the monitor's process, and writes the MISLAUNCH record.
1823: - **R3:** F01-F04 are not ported (they test C2V002 freeze data, which is unchanged). Accepted.
1824: - **CHOICEs** (README §5) are accepted.
1825: - **E1 (builder):** an empty `DIFF_S0_KIT_C2V003_TO_C2V003A.diff` was created by exclusive create. **It is left in place, not deleted.** The real diff is the `_R1` file `99e838f7`.
1826: 
1827: **The step-4 packet A166 set: ADOPTED pending Claude4's review after its Fri reset.** Root verify found 0 blocking. guard/launcher 36/36 twice; lib 143/143 twice.
1828: - **Objects:** guard014 `6efdca01`, launcher015 `cd987edd`, lib v002b `65d69cf4`, DBP C2V004B `e239d21e`.
1829: - **What the tests show:**
1830:   - launcher015 starts with `memory_pressure` unreadable and makes no memory call;
1831:   - lib dry mode never opens gate v003;
1832:   - a synthetic campaign route-A tree is still refused.
1833: - **Builder items:**
1834:   - **(1) Binder, (2) CLI wrappers, (3) lib default params.** step4_bind c2v010 loads guard011 and adds `nice`; the S1 CLIs pin lib v002a; the lib's default DBP is C2V003A. **Ruled: all three go into the S1 launch-path follow-up together with G7:** binder c2v011, CLI wrappers c2v002c, and lib v002c with DBP C2V004B as the default. That follow-up is built after the G-wave, and direct batches and S1 need it first.
1835:   - **(4) Refuse, not ignore, for old-form plans:** confirmed.
1836:   - **(5) S1 registration C14 text erratum** (the pinned bytes are unchanged): "passes the machine gate at its own start" now means "starts under launcher015's ramp and max_active". Under A166 there is no gate.
1837:   - **(6) At the A140 N4 rebuild, DBP C2V004B is re-derived** from the rebuilt base by the same C2V004 → C2V004B transformation, then leaf-diffed.
1838: 
1839: **Roster builder c2v006 and ROOT_TSR_FLAG_RECORD_V003: ADOPTED** (A173).
1840: - **Objects:** builder `0cc731065d1f00e1549cb7b9442c901da0a35f48c8a03d67f14701f652ad0aa2`, V003 `7d3c1eb915cd9a85b1a9dab388e6a3fb6c218ef3d4e8e6f2dc726bea15c54070`.
1841: - **Results.** 160/160 twice. In the interface proof, c4v004's own checks accept the c2v006 gate lists and V003, and refuse the c2v005 forms. Root verify: ADOPT, 0 blocking.
1842: - **C46-C49 are ruled as built.**
1843: - **Erratum E_A169_1.** A169 said the c2v005 records were already in classifier A's schemas. They lacked `schema` (Claude4 0228).
1844: - **Load-bearing for the seal:**
1845:   - the seal entry, `sealed.tsr_flag_record_sha256` and the freeze manifest's `input_files` must all name V003;
1846:   - `tsr_support_record` must also carry `schema: UNT_ROOT_TSR_SUPPORT_CX3V001` with its exact nine keys (c4v004 L705-707). It is still pending under RUNBOOK gap G7.
1847:   - Root's own records (phase inputs, STAGE0 status C4V003, commitment status, fallback, field map) each carry `schema` (INPUT_CONTRACTS_C4V004 `f9286f56`). The exact-key rule holds by A's check for six of them, by root's writing rule for the fallback record, and not at all for root disclosures (Claude4 0235).
1848: 
1849: **M-12 seal route (Claude4 0245; root 0751): (a).** The r3a text is unchanged. The seal entry cites M-12 by id and records A176 as the ruling on implementation B (M-6 item 2).
1850: 
1851: **NGC acceptance c2v003: c2v003a is ADOPTED; c2v003's handoff is not** (`ngc_acceptance_c2/`, README `659ca6a4`, HASHES `e97b2af6`).
1852: - **Results.** Two lenses, 0 blocking. c2v003 34/34 + 41/41 with 72/72 mutants; c2v003a 35/35 + 42/42 with 75/75.
1853: - **Adopted (consistent with A167):** adapter c2v003a `9c4b6dfc` and handoff c2v003a `7c54fd6f`. The c2v003 handoff pins adapter c2v002 and is not adopted.
1854: - **The NGC row contract** `NGC_ROW_CONTRACT_C2V001.json` `80cbf2f5be2e9f22a0b751376dcde3e7e779bd89f531a8ffe9d654616490fe32` holds ids and order, R_i, the rule id, the θ hex and the c hex. It has no velocity, t_i or σ. Claude3's S10 review (A176) must carry schema `UNT_NGC_LO_ROW_POLICY_REVIEW_C2V002`, verdict APPROVED and that `row_contract_sha256`.
1855: - **Still owed before any real NGC acceptance** (every one reads INCOMPLETE until then, which is UNTESTED, not a null):
1856:   1. **Roster recipes for route A and route B**, commissioned below. Without the route-A recipe, every call refuses at ROUTE_A_ITERATE_SOURCE_UNESTABLISHED (verifier note 1 corrects the README's description).
1857:   2. **The S2 pins:** NGC ρ c3v003 producer `d3d0f3dd` and slot proof `ada31d12`, after root's review (running), with schema `UNT_NGC_POINT_RHO_NUMERICAL_C3V003`.
1858:   3. **The S10 review** (Claude3).
1859: - **For the next successor:**
1860:   - the two test gaps of verifier note 3 (the start.json binding conjunct, and the W-1 eps-certificate pin check);
1861:   - the README wording (notes 1-2).
1862: 
1863: **Commissioned: NGC roster recipes (route A, route B)** as one lean root workflow (builder plus one verifier).
1864: - Each recipe is derived from the driver's pinned route-A controller and route-B binding, so that the S5 rebuild-export tool rebuilds each consumed state and admits it only on an exact `state_digest` match.
1865: - Synthetic tests only. No NGC3198 data file is opened.
1866: - The c2v004 successor takes the recipes plus the note-3 tests.
1867: - Review: Claude3 after its reset, or Claude4 after Fri.
1868: 
2294: ## A191: the H3 campaign launch path is built (84/84; six gates pass on a synthetic seal); 2 blocking items; three design gaps for W1's later waves; storage is at the two-volume edge (2026-10-20 02:03:48Z)
2295: 
2296: **Object.** `h3_campaign_path_c2/`: README `6d2b4ee2`, HASHES `67ef3ad4` (5,495 files). Root workflow wf_49db569c: map, build, verify.
2297: - **The chain derives from the q5b1 line (map F1),** not the R9 wrapper. R9 still needs the retired prelaunch LO envelope, which A134 replaced with per-state acceptance through acceptance_q2 v004 (A158).
2298:   - The successors: generator `make_campaign_cascade_c2v001` (`65a70144`, from generator v002), entry `h3_campaign_entry_c2v001` (`08068e93`), and `regenerate_h3_c2v001` (`1706da77`). The regenerator's `fill` writes the one seal record from the report's bytes, and its `build` refuses unless the tuple equals those bytes.
2299:   - Also built: `apply_h3_fields` (`2e4a5393`), the per-call step `h3_accept_call` (acceptance v004, then reingest), and the storage check.
2300:   - **Placeholder chain** SUB `v006r12_c4`. A129 reserves r11, and nothing is published.
2301: - **Verify.** Code holds; 84/84 twice; 78/78 physics pins equal and numerics `4b2a5a87` unchanged. Map F4: the cache id becomes `ce6a1a6b…` (wrapper and gate fields are in the key), and the W1 record states it.
2302: 
2303: **BLOCKING, fixes commissioned:**
2304: - **B2 (TESTED).** The entry's `reingest` can cache a call as VALID without the adopted acceptance handoff having run.
2305:   - The fix: `reingest` takes `--acceptance-record` with its sha, and refuses unless the record is an acceptance_q2 v004 (`5ff464cc`) ACCEPTED or ACCEPTED_PASS_FLAGGED record for the same call, receipt and bundle. The bundle path must be absolute.
2306: - **B1, the storage plan arithmetic.** The README's §6 counted HEADLINE11 plus S0 at about 48 GiB. The real figure is about 370.5 GiB, so the plan does not fit.
2307:   - At the measured 16.24 GiB per call, External1 must hold about 3,386 GiB of its 3,726 GiB at wave 15. The internal disk has about 953 GiB free.
2308:   - **The program is at the two-volume edge of the A147 rule.** The erratum recomputes the budget with the parent's binding condition: the maximum over k of (Σ_{j<k} n_j)·b + n_k·80 GiB + 20 GiB.
2309: 
2310: **Design gaps for W1's later waves** (FORMAL; mapped, not yet ruled):
2311: - **F5.** Once the certificate registry is set, every planned point needs a registry record before planning. That covers the 9 capability-probe points, every call, every resume and every cache open. The registry pin sits in the frozen config and the cache key, so engine-chosen points from march0 on cannot be registered in advance.
2312:   - W1 itself can run. Its seed is `6944e210…`, not the anchor, and the 9 probe points are CP-1 points.
2313: - **F6.** No ruling covers a campaign call whose acceptance reading is not ACCEPTED (INCOMPLETE, LO_UNCERTIFIED_TRANSIENT, NON_LAPSE_TAIL_MATERIAL). `resolve invalid` is disabled, and a retry reruns the same call deterministically.
2314: - **The deciding and capability runs** are real r5 calls with no commissioning lane.
2315: 
2316: **Commissioned (lean):**
2317: 1. the B2 entry fix and the B1 storage erratum;
2318: 2. a **design map from the existing rulings and code** (A134, A139, A145, A146, A158, the campaign packet docs): how per-point certification of engine-chosen campaign points was meant to work, and the minimal path for F5, F6 and the deciding/capability runs. It proposes; root rules.
2319: - **Review:** Claude4 after Fri 19:00Z (the campaign packet's lineage); Codex1 the generator diff, if it has credit after Sun.
2320: 
2321: **Timing consequence (UNTESTED).** W1's first wave can launch at the verdict once B2 is fixed and the gate fields are filled. Wave 2 onward waits on the F5 ruling and its build. That may hold the campaign past the verdict, and with it u_A and Phase 1. Root reports the measured effect once the design map returns.
2322: 
2323: ## A192: the campaign certification design is ruled (F5 ledger, F6 reading rule, HEADLINE11 before W1); the H3 entry fix is adopted; storage is measured at W1; the honest schedule (2026-10-20 02:37:26Z)
2324: 
2325: **Inputs.** Root workflow wf_93e4ceb9:
2326: - entry fix c2v002 `75b4cafa`, 94/94 twice, verified 110/110 with adversarial rows;
2327: - storage erratum `5ce908d0`;
2328: - design map `h3_campaign_path_c2/CAMPAIGN_CERT_DESIGN_MAP_C2V001.md` `29071333`, with 20 source shas and about 60 line ranges verified.
2329: 
2330: **Ruled:**
2331: 1. **B2 is closed.** `h3_campaign_entry_c2v002` and `h3_accept_call_c2v002` are adopted pending Claude4's review. `reingest` needs the call's own acceptance_q2 v004 record. A hand-edited record is root's custody, under A115 honest producers.
2332: 2. **F5, per-point certification of engine-chosen points: the R-C8 ledger** (Claude4 ROOT_ITEMS_FINAL_C4V004 L263-269, never built).
2333:    - An append-only, hash-chained registry ledger. The config and cache id bind only its starting set and its policy.
2334:    - Each wave's new points are certified before that wave by the approved producers: CP-1 EPS, GQ and ρ, then adapt-eps and the slot proof. This uses a CP-1 successor that takes a list of points.
2335:    - The ledger goes into the wrapper source of the verdict regeneration, before W1. The core is untouched, and nothing that sets a physics value changes.
2336:    - Fallback: a new work dir at march0.
2337: 3. **F6, campaign calls not read ACCEPTED** (a science ruling, made now, before any campaign call). It is consistent with A134 and A158: no value is used before ACCEPTED, failure readings stay frozen, and the scope never changes.
2338: 
2339:    | Reading | Action |
2340:    |---|---|
2341:    | ACCEPTED, ACCEPTED_PASS_FLAGGED | cached VALID |
2342:    | INCOMPLETE | the acceptance step reruns once, after root checks its inputs. No new forward call is made. |
2343:    | NON_LAPSE_TAIL_MATERIAL, BOUND_INSUFFICIENT | certified MODEL_INVALID through a reviewed command, built with the ledger |
2344:    | any other reading | the campaign halts at that point, and root rules per call |
2345: 
2346: 4. **The deciding and capability evidence is HEADLINE11 #0-#10** (CP-1 rows 1-9; core L114-197, L313-340).
2347:    - **W1 passes its gates only after those 11 calls are FINISHED and ACCEPTED.** HEADLINE11 starts at the verdict and C1 (A142), so the order is: verdict, then HEADLINE11, then W1.
2348:    - A tool to assemble the two evidence documents from HEADLINE11's receipts is commissioned.
2349:    - **Deciding test** (whether HEADLINE11's runs can be reused, so no extra runs are needed): `status` shows the 9 capability-probe spec shas under the candidate config. They must equal the shas HEADLINE11 ran with.
2350: 5. **Storage (verifier blocking item, accepted).** b is measured at W1 as the call dir's total bytes after acceptance, including the ACCEPTANCE_TAILSTATES exports. It is not the receipt's output bytes.
2351:    - The 17.08 GiB threshold is recomputed from that measurement, and `storage_check` gets a successor that counts the same bytes.
2352:    - If both volumes cannot hold the program, root alerts the principal (A147). One campaign volume of at least about 7 TB would cover the high case.
2353: 
2354: **Commissioned (root workflow; Claude4 reviews after Fri 19:00Z):**
2355: - the wrapper ledger and the MODEL_INVALID command;
2356: - the CP-1 list-of-points successor;
2357: - the HEADLINE11 evidence assembler;
2358: - the `storage_check` successor.
2359: 
2360: **Honest schedule** (UNTESTED; replaces A188's).
2361: - **Step-3 verdict:** about Wed-Sat 21-24 Oct, set by S4T.
2362: - **HEADLINE11:** about 3 days (11 calls at 3 concurrent, about 18 h per call).
2363: - **W1 up to B_P1** (seed, Jacobian, repair): about 3 days, giving u_A.
2364: - **Phase-1 NGC runs:** about 3.5 days.
2365: - **Phase 1 is scored about Sun 1 to Sat 7 Nov.**
2366: - **Phase 2 is about mid-to-late November.** The campaign takes about 10 days after HEADLINE11, plus per-wave certification of about 2 days in total, plus step 5.
2367: - **Deciding measurements:** S4T's le1 stage time, the HEADLINE11 call wall, the W1 per-wave times, and the NGC call wall.
2368: 
4378: ## A255: four acceleration levers commissioned (principal: "Please proceed to find and implement any parallel processing that might speed up the plan") (UTC 2026-10-21 11:38:53Z)
4379: 
4380: Codex1's 0177 (0815) found that the 3 nominal W3 Jacobian-minus points are fixed in advance on the expected path (seed and three plus valid). March0 and later are not. Root commissions four levers. Each is adopted only with a FORMAL proof from code that values and the engine's path are unchanged. Any lever that changes physics or custody is a FAIL, not a trade-off.
4381: 
4382: | Lever | Step | Saving (UNTESTED) | Owner | PLAN |
4383: |---|---|---|---|---|
4384: | L1. Pre-certify the 3 W3-minus points now (CP-1 on the idle host, `taskpolicy -b`) | S6 | about 0.5 d at W3; required by L2 | root; binding check wf_5a044dd0 (Claude lineage) | P-127 |
4385: | L2. Concurrent Jacobian: W1 seed + W2 plus + W3 minus launched together, consumed by the engine as cache hits | S6 | about two wave times | Codex1 0816 design; Claude-lineage adversarial check before adoption | P-128 |
4386: | L3. W1 on internal disk or External1 before the new drive | S5 | about 12–18 h (W1 Fri morning, after HEADLINE11 evidence) | Codex3 0817 (A) | P-129 |
4387: | L4. Phase-1 NGC route A at column_workers 8 once S0's twin identity is TESTED | S9 | S9 wall, to be estimated | Codex3 0817 (B) | P-130 |
4388: 
4389: **Already maximal, recorded in A254:** the step-2 wait, HEADLINE11's full overlap, and S8 alongside S9.
4390: 
4391: **Discard rule (L1, L2):** a result computed early is used only where the engine requests that exact identity. Otherwise it is preserved and never used.
4392: 
