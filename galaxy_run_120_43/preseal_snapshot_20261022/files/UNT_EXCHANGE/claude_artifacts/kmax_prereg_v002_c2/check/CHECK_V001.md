# CHECK_V001: independent check of KMAX_MATRIX_PREREG_V002 and kmax_compare_c2v002

**Verdict: PASS_WITH_ADVISORIES.**

- The prereg (`0024b63e…`) and the sealed compare script (`e42336a7…`) implement the CHECK_V001 corrections D1–D8 (and D13) and root decisions (a)–(e), as the prereg states them, exactly. No change to either file is needed before the C2 result exists.
- The specs differ from the anchor base spec (`fe1ad000…`) only in the fields the matrix declares, and the admission links are right.
- **SEAL_RECORD:** its binding claim holds. It was sealed at 15:03:47Z, before any convergence-case result at the anchor existed; C2 (`A2_ANCHOR_F3_RUN_V001`) still had no `result.json` at 15:22Z. One sentence of its statement is not supported by the file metadata (F1). It needs a one-line addendum from the sealer, not a re-seal.

**Who checked and how.**
- The checker is the Claude2 lane and did not write the kit.
- Scripts and outputs are in this `check/` directory. Hashes, computed from bytes, are in `HASHES_CHECK_V001.txt`.
- numpy only, single thread (thread environment variables set to 1), runtime `codex-primary-runtime python3 -I -B`. Nothing was launched.
- From the σ source, only `rows[*].id` and `rows[*].quoted_random_sigma_km_s` were used.
- One incident by this checker is recorded in §6.

## 1. What reproduces

| Claim | Result | Evidence |
|---|---|---|
| `HASHES.txt` (53 entries) | 53/53 verify from bytes | shell check |
| Every `{path, sha256}` in the prereg: supersedes ×2, binding inputs ×13, anchor coefficients | 16/16 verify | inline hash walk; the same files are re-hashed by K01 and K02 where they are loaded |
| Author tests, 35/35 | Reproduced. `TEST_RESULTS.json` is byte-identical (`e0581808…`) and was run on the sealed compare sha | `rerun_tests_V001/` |
| τ_i = 0.25σ_i | Equal to the σ source rows in row order. τ_picard = 0.25·min τ_i = 0.0125. Band shift 8.73% on every row; Σ(τ/σ)² = 0.75; cross term 6.0 at r_i = +σ_i | K02.1 |
| Grid blocks | Byte-equal to V001 and to v003 `DECLARED_LARGE_GRIDS`. Axes are 72/84/96/92 | K02.2a–c |
| Masks | The compare's `driver_mask` equals the `truncation_mask` of both v001 and v003, bitwise, on the real G2/G3/G4 at K = 2/3/4. Kept counts 344048/362592, 525992/567504 and 755080/834048 | K02.2d |
| Driver normalization | Every case spec normalizes under each allowed driver. G2 cases normalize identically under v001 and v003 | K02.3 |

## 2. D1–D8, D13 and root decisions (a)–(e)

The source of (a)–(e) is the prereg's own `supersedes.changes` list; see F2.

| Item | In prereg | In compare script | Tested |
|---|---|---|---|
| D1: pass iff D̂34 ≤ 1 and D̂34 ≤ ½·D̂23; tail is a diagnostic only | `shape_pass`, `tail_diagnostic` | l.302; per-row and sequence tails, never used in the decision | K02.4d–h: the V001 A1 fixture q = 0.95 gives NOT_CONVERGED (tail 18.8 τ_06 reported); margins 0.999 and 1.001; q = 0.501 |
| D2: u_i adds the max passing-shape spread at K = 4 | rule 6 | l.357–358 | K02.4b, per row |
| D3: V5 gates nonzero rows == expected kept rows | V5 | l.136–137 | K02.6a–d (real 72³): over-masked fails; unmasked-as-S2 fails; sphere-as-cube fails. K02.7b (real 96³) |
| D4: m≥1 bullet withdrawn | `why_tau` has no such bullet | n/a | read |
| D5: χ² bound limited to the bias² term | `why_tau[2]`; cross term +6.0 stated | n/a | K02.1e |
| D6: pre-named next step per gate; passes 6 in new specs | `gate_next_steps` V1–V6 | l.326–331 | K02.4n, 4o and 4z2. K01: all 12 v002 specs have passes 6 |
| D7: P6 precondition plus declared recovery | `bracket_precondition_P6` | `--bracket-recovery`; the block replaces the anchor block for every case; changed keys reported | K02.4u–v. See A1 |
| D8: V3 checks against the registered block; modal block reported | V3 | l.204–213, 229 | K02.4s: an odd C4 is named alone. K02.4t: a 6/10 odd majority is named; the 4 registered cases stay valid |
| D13: m4 over 0.4–6.0 kpc; candidates within 1.10·min; null → all; ties → cube, sphere, cylinder | `m4_statistic`, rule 5 | l.76–80, 349–356 | K02.5j–n; K02.7a (window excludes 0.2 and 12.8 kpc) |
| (a) per-row τ; τ_inner = τ_i; shape bound 2τ_i; Picard 0.0125 | `criterion` | l.196–199, 224, 310, 342 | K02.4i–j: 0.36 km/s on row 01 adopts; 0.055 km/s on row 06 fails. K02.5h–i: 2.1 τ_06 vs 1.9 τ_06 |
| (b) anchor blocks copied verbatim from the base spec | `anchor` | V3 against `anchor` | K01: physical, brackets and column_workers in all 12 specs equal the base spec |
| (c) drivers by grid | `drivers_allowed` | l.240–243 | K02.5a–e |
| (d) C2 = F3, passes 4, Picard equivalence | `bound_call`, `picard_equivalence` | l.231–239 | K02.4w–z2. Driver source v001 l.1076–1077, 1118, 1147: with a bound set, the passes count only enters through `last`, so a passes-4 call that stopped with change ≤ 0.01 is the passes-6 trajectory |
| (e) NOT_CONVERGED next step: 5–6/kpc, prep budget ≥ 120 | rules 3–4 | l.337–346 | K02.4d |
| Rule order: INCOMPLETE, then INNER_UNRESOLVED, then NOT_CONVERGED, then ADOPT | rules 1–5 | l.325–366 | K02.4l–n |

The end-to-end run is K02.7a. It runs `main()` on the **sealed** prereg (test_mode false) with real-size packets for all 10 cases and real grids. The outcome is ADOPT/sphere, and all V4/V5 gates pass.

The script and its synthetic tests are `k02_compare_adversarial_c2chk.py` → `K02_COMPARE_ADVERSARIAL_V001.json`, 72/72. K02.7c is a probe whose PASS confirms advisory A1.

## 3. Specs, the matrix and admission (K01)

The 12 v002 files are the 3 wave-1 specs and the 9 templates. Each was compared with `fe1ad000…` key by key:
- **Fields that differ:** only `label`, `numerics.composite_grid_spec`, `numerics.truncation`, `numerics.picard.passes` (4 → 6) and `admit`. There are no other diffs.
- **Grid and truncation:** each equals the registered block for its case.
- **Label:** each carries the prereg sha.
- **Generator diff:** the generator-vs-patched diff contains only `passes 4 → 6` and the S2/Y2 placeholder binding.

Admission links:
- S2/Y2 point at the F3 outdir.
- S3/Y3 point at `<C3 out>`, and S4/Y4 at `<C4 out>`.
- `fill` refuses a cube whose physical block, coefficients, grid, truncation, brackets or Picard bound differ. A cross-grid or cross-physics fill is therefore impossible.
- The constraint "S2/Y2 run under the cube's driver (v001)" is enforced by V6 (K02.5c).

## 4. SEAL_RECORD

| Claim | Status |
|---|---|
| C2 `result.json`/`finish.json` absent at seal | **Confirmed.** Still absent at 15:22Z; stages 01–04 only |
| No other case launched; specs generated after the seal | **Confirmed.** No run dir has been created since the seal. Prereg 15:00:06Z, compare 15:03:23Z, RUN_V002 tests 15:03:30Z, seal 15:03:47Z, specs from 15:04:07Z |
| C2 bound call | **Confirmed.** `launch.json` pins spec `fe1ad000…` (the bytes of the base spec), driver v001 `75b0c08a…`, caps 3 GiB / 14400 s / 8 GiB, 14:35:58Z |
| KMAX_C2_A2_RUN_V001 and F10 are not anchor cases | **Confirmed.** KMAX_C2 is spec `7c7330bf…` (γ 2.94e41, s = 1); its monitor log says BLOCKED. F10 is spec `a93c95b9…` (γ 2.94e42, s = 0.1015) and has no result |
| "No result.json, finish.json or stage output under A2_ANCHOR_*/KMAX_* was read before or during sealing" | **Not supported by the metadata (F1)** |

How the timestamps were read:
- **The volume's access-time rule.** It was measured on a scratch file: a read updates atime only when atime ≤ mtime.
- **What a timestamp therefore shows.** atime > mtime means the file was read after its last write, and atime is the time of the first such read. atime ≤ mtime means it has not been read since that write.
- **What K03 found.** `K03_SEAL_EVIDENCE_V001.json` uses `os.stat` only. Every pre-seal read in the anchor dirs falls into one of these groups:
  - the driver reading its own files back within milliseconds of writing them;
  - F3 `inputs/call_spec.json` at 14:54:30Z (the sealer's hash, as claimed);
  - the launch files at 14:55:59Z and 14:57:58Z (as claimed);
  - **one scan at 14:56:28.909Z** (F1).
- **What the sealer did not read.** F3's route-A `finish.json`, `progress.jsonl`, node_diagnostics and reference `start.json` were not read between their last write and 15:08:31Z, after the seal.

## 5. Findings

**F1 (custody; addendum needed, not a re-seal).** One process read 5,791 `.json` files at 14:56:28.909Z, about 7 min before the seal. It read them in the same millisecond, and only `.json` files: no `.jsonl` and no `.npy`. The files were:
- in **both** F3 and F10: every route-A checkpoint file (iterations 0–4 × 576 columns, START/COMPLETED, `IDENTITY.json`, attempts) plus `attempt_000/start.json` and `operator_identity.json`;
- F10 `inputs/call_spec.json`;
- 10 files in REPRO_PINNED_FULL_RUN_V001.

Metadata cannot identify the reader. These are route-A (stage 01) state. No route-B pass, row or convergence quantity existed then: the reference stage started at 15:02:59Z, and no threshold depends on route A. So the precondition that the prereg was sealed before any anchor result holds.
- **Next step:** the sealer states whether this scan was theirs. If it was, append an addendum to SEAL_RECORD that names it, before the C2 result is read.

**F2 (provenance).** The prereg cites "root decisions (a)–(e) of the Claude2 coordinator". The bound `root_decisions` file (`c8bf13d3…`) contains only A1/A2. No file in UNT_EXCHANGE or in CLAUDE2 outside `runs/` states (a)–(e). They were checked against the prereg's own text, and (a) against CHECK_V001 Speed item 4.
- **Next step:** the coordinator records (a)–(e) in a file and its sha is added by addendum.

**Advisories.** The sealed files are unchanged; each advisory has a workaround or a next step.
- **A1 (D7 recovery enforcement).** `--bracket-recovery` accepts a block that changes a non-override key or narrows an entry. Probe K02.7c: `rfs_factors` changed was accepted and only listed in `changed_rule_keys`. The prereg allows only widening the missed columns' override entries.
  - Until a compare successor refuses this, the reviewer confirms that `changed_rule_keys` ⊆ {fs_absolute_overrides, rfs_factor_overrides, le_factor_overrides} and that every changed interval contains the old one.
- **A2 (robustness).** The driver writes a non-finite `max_abs_change_km_s` as a string (`'nan'`). `evaluate()` then raises a TypeError at V2 (K03 probe), so no report is written.
  - If that happens, drop the case from CASES.json and record why. The case is then reported missing, so the outcome stays INCOMPLETE under rule 1.
- **A3 (launch hygiene, before wave 1).** There is no v002 campaign file. `generator_raw/wave1/CAMPAIGN_KMAX_WAVE1_C2V001.json` lists the raw passes-4 specs, including C2.
  - Launched from it, C3/C4/R would fail V3 (picard_passes), and C2 would be duplicated.
  - Mark it NOT-FOR-LAUNCH, or write a v002 campaign: C3, C4 and R under v003 from `specs_anchor/v002/wave1/`.
- **A4 (CHECK D15 still open for the compare).** The compare invocation does not set thread environment variables.
  - The decision arithmetic is elementwise and is not affected. Only the ring diagnostic's matmul could change in its last bits.
  - Export the variables in the command.
- **A5 (minor).**
  - V3 compares the whole coefficients block (path and sha) where the text says "coefficients sha". This is stricter; there is no false fail on the generated specs (K02.4a).
  - V3 does not gate `column_workers`, which matches the text; all specs use 2.
- **A6 (cosmetic).** Two next-step texts point at the wrong remedy, while the outcome is still correct:
  - an unparsable `result.json` is reported as "missing" with the next step "run the registered case"; the real cause is in `read_errors`;
  - when the cube is missing, its admitted cases are named under V6 with a "regenerate" next step, but the real remedy is to run the cube.

**Textual.**
- **T1.** `why_tau[3]` says "without loosening the per-row band shift or the bias-squared bound". That holds for V001's *stated* worst-case bounds (8.7%, 0.75). The realised values do loosen:
  - Σ(τ/σ)² goes from 0.264 under V001 to 0.75;
  - the row-01 band shift goes from 1.1% to 8.7%.
  - This is the choice root (a) made; "within the same stated bounds" would say it exactly.
- **T2.** In `shape_pass`, "each row's remaining tail is at most τ_i" assumes the contraction continues at q ≤ ½, extrapolated from two differences. That is consistent with "no tail adopted".
- **T3.** The seal statement lists only `inputs/call_spec.json`, but `ANCHOR_PLAN_EQUIVALENCE` also uses the F3 input seed sha (`346a9161…`). It is an input, so the omission is harmless.
- **T4.** `HASHES.txt` also omits the dry-run stdout/stderr, the probe `DRYRUN_PLAN.txt` files and the RUN_V001 outputs, which its header does not mention.

## 6. Checker incident (recorded so it is not attributed to the sealer)

At 15:08:31–33Z, after the seal, two of this checker's `grep -r` literal-string searches ran over the CLAUDE2 tree, `runs/` included.
- **What was read.** By grep semantics they read the bytes of files under `runs/A2_ANCHOR_*` and `runs/KMAX_*`, including the route-A `stages/…/result.json` files and `KMAX_C2_A2_RUN_V001/result.json`.
- **What was seen.** The output was filtered to exclude `/runs/` paths, so no byte of those files was displayed or used. F3 has no top-level result.
- **Rule broken.** This breaks this check's read rule.
- **Effect on the prereg.** None; it happened after the seal.
- **Effect on the evidence.** It reset atime to 15:08:31–33Z on files not read since their last write, and that reset is itself the evidence for §4's last bullet.
- **Files outside the lane directory.** Scratch files went to the session scratchpad, not to this directory. They are the atime probe, two stat helpers and about 800 MB of full-size mock packets in `scratchpad/k02_packets_v001`. The K02.7 reports reference those packets.

## 7. Next steps (pre-named)

1. Sealer: F1 addendum, before the C2 result is read.
2. Coordinator: F2 record plus its sha.
3. Before wave-1 launch: A3.
4. At comparison time: A4 (thread environment) and the A1 and A2 handling above. No threshold or rule changes.
5. In a future compare version, only if one is needed for another reason: refuse non-widening recovery blocks (A1), and coerce a non-numeric change to "V2 fails" (A2).
