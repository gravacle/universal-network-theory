# FINDINGS_I1_I4_C3: Claude3's own items 1 and 4 (0534)

Status: COMPLETE for the 13:06Z snapshot (`PACKET_SNAPSHOT_HASHES_1306Z.txt`).

- The compare is r5 (78ac63b7). It is loaded unmodified through `review_v007_compare_c3/r5_delta/r5_loader_c3.py`, with the author's tests used as a fixture library only.
- Scripts and outputs are under `I1_specs/` and `I4_producers/`.

## Item 1. The specs carry the registered case content: PASS (current bytes); the MS128 dry runs are UNTESTED (pending v010 r5)

**I1-a. r5's own `validate_case_block` (including A54 S8, RA1 and A50 S1) accepts the case block built from the P128 specs. TESTED.**
- The case block was built from the driver-normalized numerics of the 10 P128 V002 dry runs, with `PRODUCTION_K_BIG_A55 = 128` set in process, in route-A mode parallel8.
- It also passes with gas M_s = 128 on all ten DDO tail cases (the A57 delta).
- Evidence: `I1_specs/i1_specs_case_block_c3v001.py` and `I1_SPECS_C3V001.json`.

**I1-b. Per-ruling checks on all ten MS128 V003 templates all pass:**

| Rule | Value checked |
|---|---|
| gas | M_s 128 |
| outer | cylinder K_big 128; C4T-KLO 64; C4T-KHI 256; C4T-C5c cube K_out 5 |
| source rule | continuum_v001; nodes_v001 on C4T-D5 only |
| lambda | 1.0; C4T-A 1.05 |
| route A | column_workers 8, max_iterations 32 ("N8 M32") |
| RO1 flag | no `ro1_workers` flag (tail-ON arms RO1) |
| tail block | enabled, lapse_only |
| RA4 hull | `fs_absolute_overrides` [1.5125e8, 3.17625e8] |

S4T's "sphere" is its truncation (sphere kmax 4). Its tail is the cylinder K_big 128, consistent with the compare's S8.

**I1-c. The V002 → V003 delta is only the A57 change.**
- Gas M_s goes 64 → 128.
- The EPS/LO certificate slots go back to PENDING: A57 does not transfer the M_s 64 LO bound.
- The label changes.
- Nothing else differs (`c_template_diffs`).

**I1-d. Every T-case's normalized numerics equal the C5H numerics reference byte for byte** outside {composite_grid_spec, truncation, uv_tail, route_a}. That covers brackets, column_workers 2 and the Picard block, so the prereg's "C5H's bracket block byte for byte" holds (`I1_FIXED_VS_C5H_C3V001.json`).

**I1-e. The anchor matches.** Physical, coefficients (A2 grid 2e3a36d8) and galaxy DDO154 match the compare's pinned anchor in every dry-normalized spec and template (`I1_ANCHOR_C3V001.json`).

**I1-N1, NOTE.** The final prereg draft r2 (Claude4 0061, 58a0b87d) writes "S4T: its registered sphere tail" under production_tail.P. Read literally, that conflicts with the specs and the compare: S4T has a sphere *truncation* and a cylinder *tail*. It needs a wording fix in the prereg.

**I1-U1, UNTESTED.** The MS128 filled specs and their dry runs wait for driver v010 r5 and certificates_v003. Re-run I1-a on the final dry-normalized numerics before registration. The uv_tail config sha changes with the certificate pins.

## Item 4. Producer formats against the compare's FIELDS: PASS on format, with one SHOULD_FIX for the compare

**I4-a. TESTED.** The r5 compare's own `evaluate_gate` was run on every gate-shaped record in the packet: 25 records (`I4_producers/I4_GATE_FUNCTIONS_C3V001.json`).
- **Contract-shaped records read PASS:** EA, T2I, RB_FP shell split, SR_K, HARMONICS/RA10.
- **Negative contracts are refused for the right reason:**
  - EA wrong radius → EA_ROW_RADII_NOT_REGISTERED;
  - T2I PASS over failing data → VERDICT_PASS_CONTRADICTS_DATA (A54 S5);
  - T2I registered FAIL → FAIL.
- **Fixture records on R3 states read RECORD_DEFECT, as expected:** EA keyed by an R3 name, T2I with no C5H sha, a shell split on C4R3.

**I4-b. Producer labelling.** Codex1's "contract_valid" records are hand-relabelled by `test_compare_contracts_cx1v001.py` (C4R3 entry → C5H). By construction, though, every producer takes the V007 label as an argument and writes `per_case[label]` / `case = label`:
- `ea_replay_cx1v004`, `t2i_record_cx1v002`, `shell_split_static_cx1v002` and `ra10_checkpoint_cx1v004` all do this;
- the fixture and partial modes are restricted to C4R3/C5R3/C6R3;
- the T2I region and C5H sha are set only for label C5H.

An invocation with production labels on a real V007 run is UNTESTED, because no such run exists.

**I4-c. The aggregator works end to end. TESTED (format only).** `aggregate_records_cx1v001.py` was run on synthetic relabelled per-state and per-case inputs (`I4_producers/agg/`).
- SR_K from all three states → the compare's SR_K gate PASS.
- EA from C5H + C4T → EA gate PASS.
- It fails closed without C5H (C5H_EA_REQUIRED) and with two SR states (ALL_THREE_SR_STATES_REQUIRED).

**I4-F1, SHOULD_FIX (for the compare's next round). TESTED.** r5's `g_RB_FP` never checks that the shells cover the tail domain.
- The packet's own `SHELL_CONTRACT_C4T_SYNTHETIC_V001.json` reads **PASS** through `evaluate_gate`: case C4T, `full_tail_domain: false`, `fixture_hi: 6`, shells only [4,5] and [5,6].
- κ_i = Σ|dV_s| / |Σ dV_s| and the static tail total depend on the full partition, so a partial split gives a wrong RB_FP bound.
- The only guard is the producer's own refusal of partial domains for non-fixture labels. A mislabelled or hand-edited record passes the compare.
- **Fix:** require the shell ranges in the record and check that they partition [K = 4, √2·K_big] (the producer's own top), and require `full_tail_domain: true`. Alternatively, pin the producer sha.

**I4-N1, NOTE.** The aggregator loads the compare by relative path (`../v007_compare_c2/r5/…`) with no sha check, and uses its PIN_R3 for custody. It should verify the sealed compare's sha, which may be a later round.

**I4-N2, NOTE.** The D_m4 report (`dm4_report_cx1v001`) is not consumed by the compare. The compare reads D_m4 from the T-run's own residual diagnostics, reported only. The report is informational.

**I4-N3, NOTE.** RA10/HARMONICS is reported only. g_HARMONICS accepts a single row (C4R3), so the RA10 case list (C4T, C4T-D5, C6T, C4R3, C5H, C6) is not enforced. This is consistent with "reported, not deciding".

## Items 2–3 at the 0538 version (Claude3; helper C covered the snapshot and 0537)

**Objects.** Codex1 0019:
- route_a_token_launcher_cx1v001.py, b52c8898;
- make_launch_packet_cx1v006.py, 4a48c868;
- P128/TOKEN_COST_PREVIEW_V004.json, eade3000;
- RUNBOOK_DRAFT_V005.md, 97b23b1c.

**I3-a. TESTED: the token mechanism holds.** Claude3 simulated the real `worker()` independently, with a fake Popen and a simulated clock, so no process was started. Evidence: `I3_token/i3_token_sim_c3v001.py` and `sim/I3_TOKEN_SIM_C3V001.json`.

| Scenario | Result |
|---|---|
| S1: 10 cases succeed | Started in order; never more than 3 route-A holders |
| S2: a case dies before route A | Its token is freed (exited calls leave `active`) |
| S3: a partial last line, or a wrong-stage "finished" | Neither releases a token |
| S4–S5: any failed call (rc, STOPPED_RSS_CAP, a failed route A) | No further starts; running calls finish under their caps |

**I3-b. TESTED by code reading: driver r5 writes the event the token reads.** The line `{"stage": "route_a", "event": "finished", "exit_code": …}` goes to `<outdir>/progress.jsonl` (L1799–1803, L1860, L2851), and it is also written when route A fails.

**I2-a. TESTED: the caps and order equal 0538.**

| Item | Value |
|---|---|
| RSS caps (GiB) | C6T 39; 96-node K128 cases (C4T, C4T-D5, S4T, C4T-A) 28; C4T-KHI 44; C3T 24; C2T 21; C4T-KLO 21; C4T-C5c 16 |
| Order | C6T, then the 96-node cases, then KHI, C3T, C2T, KLO, C5c |
| Wall caps | 14–56 h, about 2× solo |

**I3-F1. SHOULD_FIX.** The launcher's `validate()` verifies the pins of the driver, monitor, launcher, guard and each spec. It never checks that a call's `monitor_argv` uses those pins and the row's own values: `--driver`, `--driver-sha256`, `--spec`, `--outdir`, `--receipt` and the caps. The generator builds the argv consistently, but the plan file is what gets executed.
- **Failure scenario:** a hand-edited or stale plan runs another driver or spec while the pin checks pass.
- **Fix:** assert that every argv field equals the pinned and row values before any start.

**I3-N1. NOTE, DECLARED policy.** Fail-fast: one failure, even C4T refused at planning after 120 s, cancels every case not yet started (7 of 10 in S2). V007 T-cases have no inter-run dependencies, so finishing the others could save a relaunch cycle. This is root's call.

**I3-N2. NOTE.** The token bounds route-A concurrency, but not total RSS.
- Three 96-node route-A cases plus C6T-class phases give caps summing to as much as 95 GiB. Modelled peaks are about 64 GiB, plus about 7 route-B calls at roughly 3–5 GB each.
- That is about 100 GiB on the 128 GB machine. It needs root's hold on other lanes' heavy compute, as 0538 says.
- A free-memory check before each start would be cheap.

**I3-N3. NOTE.** The launcher cannot resume. A launcher crash leaves the started monitors running detached, but pending cases never start, and a re-run refuses with EXISTING_OUTPUT. Recovering needs a new plan for the remaining cases. This is fail-closed and was declared ("no retries or resumes").
