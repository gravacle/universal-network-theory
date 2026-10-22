# VERIFY: adversarial check of targetfree finding B-1 (miss-reading prereg r2, round 1)

- **Written:** 2026-10-18T19:34:03Z (`date -u`). Started 19:19:48Z.
- **Verifier:** a Claude4 helper, under dispatch 0585 (`9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd`) and the 0592 lens workflow. Refute by default. This folder is the only place written. The object was not edited.
- **Object:** `claude_artifacts/miss_reading_prereg_c4/r2/round1/`. All 10 entries of HASHES_R2.txt match `shasum -a 256`, for example PREREG `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143`, ROOT_ITEMS `1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f`, check tool `85457a43c654aa13b49fa528b786a615e99a51eaa29b4ba42687a2c0f3396cc7`.
- **Finding checked:** B-1 in `checks/targetfree/REVIEW.md` (SHOULD_FIX): "the seal and all root rulings can come after the NGC predictions exist".
- **Root decisions read:**
  - V005 (open) at 19:21:30Z: `50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477`.
  - V005 again at 19:33:21Z: `6145a1f92cbace8d36f86a7c15be4d79ee6992717a5c57438cdd62045e070c7c`. The only difference is the new A93 at L890 (cx3r007 accepted; should-fix items "before any step-5 launch").
  - Both copies are in `snapshots/`. V005 line numbers below refer to `6145a1f9`; lines before L890 are the same in both copies.
  - V004 `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` and V003 `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468`: both match.
- **Rules kept:**
  - No NGC3198 target, observed-velocity, rotmod, Vobs, MassModels or SPARC path was opened.
  - Nothing under `runs_ext/KMAX_A2F10_C5H_RUN_V001` was read, listed or stat'ed, and no `UVT_*` file was read.
  - Nothing was launched.
  - The only computation is a dimensionless synthetic toy (§5): numpy only, `python3 -I -B`, thread variables set to 1.

## Verdict

| question | answer |
|---|---|
| Refuted? | **No.** Every claim in B-1 is confirmed from bytes. Two small imprecisions (§2.2) do not change it. |
| Is the quoted text there and defective? | **Yes** (§1). |
| Does the evidence say what is claimed? | **Yes** (§2.1). Further evidence strengthens it (§2.3). |
| Severity | **SHOULD_FIX, agreed** (§3). Not BLOCKING, because sealing the text as it stands, now, would be safe: no step-5 output exists yet. Not a NOTE, because the live schedule puts the rulings after step 5. |
| Would the fix work? | **In direction, yes. As worded, no** (§4). "produced or read" contradicts the next sentence. The fallback covers only the M rulings, not later wording changes. "Exactly as written" cannot be carried out for M-7, and is conditional for M-11. Who must stay blind is not stated. An amended fix is given in §4.2. |

## 1. The quoted text is present and defective

- **r2 L12** (Status block): "**Seal.** Root seals this text before any NGC3198 target is opened (A60; 0585), by registering its sha256 in a root entry (root item M-6)."
  - Present, verbatim.
- **ROOT_ITEMS_R2 M-6 item 1 (L117):** "in a root entry made before any target access".
  - Present, with the same single bound.
- **r2 L369–372, the four residual-risk rows:** each closes only "before the seal": "Root may change them only before the seal (M-3)", "Root fixes it before the seal (M-7)", "They are fixed before the seal (M-9)". L370 adds "NEAR cannot be steered after targets".
  - All present.
- **No r2 clause ties the seal or any root ruling to step 5.**
  - In the prereg and ROOT_ITEMS, "step 5" occurs only at r2 L367, and only for the numerics: "Choosing K_big, M_s or certificates after targets | All are fixed before step 5 (A64; A81 RI-23)."
  - So the author used step 5 as a bound for the numerics, but not for the reading rules.
- **The object itself plans the seal near step 6:**
  - ROOT_ITEMS L220: the M-12 classifier "is sealed together with this text (its sha in the same seal entry)";
  - L226: "It costs a few hours of target-free work, off the critical path until step 6."
- **This is inherited, not a regression.** V001 L4 (`6aecf0cb…`) reads: "Root seals it before the score step opens the targets."

**The defect is real.** Nothing in the text stops root from ruling M-1, M-2, M-3, M-7, M-9, M-10 or M-11 after the step-5 predictions, bands and envelope exist. Those are the tier definition, the zone cuts, the thresholds, the radial support, the DT-S0G rule, the twin rule and the E1(b) carrier.

## 2. The evidence

### 2.1 Each cited item, checked from bytes

| cited | what the bytes say | status |
|---|---|---|
| V005 L513 (A60) | "Root rules on them and seals the prereg **before targets are opened**, in the freeze step." | CONFIRMED (verbatim) |
| "the freeze step comes after step 5" | V005 L739 (A70): "Step 6's freeze code is ready." L848 (A77): "before any NGC route A/B run (step 5)". 0603 L5 sets up the "steps 6–7" rehearsal, which is the freeze (item 2) and then the score (item 3). | CONFIRMED |
| RUNBOOK_V001 L9, step 1 (`9557b5aa…`) | L7: "First pass, before any target access"; L9: "obtain and save each required member's raw forward result". The heading "Root registration" (L13) and step 4 (L15) come after it. | CONFIRMED |
| RUNBOOK steps 2, 4 and 7 need only finiteness, cut records and projections | L10: D1 by "finite-on-valid, nonempty-valid-set rule and target-free cut/INVALID metadata". L15: rosters from slots, pins, gates and cut contexts. L21: the step-7 calls. Module `48a1e48a…` REFERENCE_RULE (L85) and SELECTION_RULE (L66) choose members by finiteness, "projection onto the identified right vectors (unit-box u space)" and log_index, never by predicted values. The module contains no `print`, no logging and no `__main__`. | CONFIRMED: no human needs to read a prediction to freeze |
| V004 L747 (A41) | "Static present-mass gravity cannot supply NGC3198's flat outer curve under any owned typing." L747 is inside A41 (L717–752). | CONFIRMED |
| 0594 L3 (`19e874ec…`) | "Step 5 launches after the V007 adoption (step 3) and the DDO recalibration (step 4) name the admitted calibration point(s)." At 19:31Z, A93 (V005 L890–895) still places its should-fix items "before any step-5 launch", and A92 (L896) is V007 identity-gate work. | CONFIRMED: step 5 has not launched, so the fix is still available |
| V005 L24 (A47 I3) | "**RA13 blinding.** Before the seal, the gate functions run on C5H only as validity/admissibility booleans and reason codes, with no row value printed or written. The seal record states that no row value was shown." | CONFIRMED |
| V004 L28 (A15) | "These are written before any NGC3198 target is opened and before calibration." | CONFIRMED |
| T1–T6 cannot detect this | Check tool header (L3–L8): T1–T4 scan the text for names, units, symbols and numbers; T5 checks pins; T6 checks the tag map. None of them knows when a rule was chosen. | CONFIRMED |

### 2.2 Imprecisions in the finding (minor; they do not change it)

1. **"C-Status" is not an r2 clause tag.**
   - The Status block (r2 L3–13) has no `[C-…]` tag and no row in CLAUSE_SOURCE_MAP_R2.md, although L13 says "Each clause carries a tag in square brackets".
   - T6 only checks the tags that exist, so the untagged seal clause escapes it. INDEX_R2 L24, "Every clause is mapped (T6)", therefore over-claims slightly.
   - Any fix to the seal clause should give it a tag and a map row.
2. **"after step 5 has saved every NGC prediction" overstates slightly.** Not every prediction exists before the freeze:
   - the sensitivity-θ runs are planned and run inside the freeze's first pass (RUNBOOK L10, step 2);
   - the STAGE0 runs come after the headline runs (A65.2, V005 L1265).

   The headline member predictions and the PRIMARY envelope inputs do exist before the freeze, and that is enough for B-1.

### 2.3 Evidence B-1 did not cite (all of it strengthens B-1)

- **The coordinator's live deadline is step 6.**
  - 0606 (`dbb80c77…`) L5: "Each needs a carrier or a ruling before step 6".
  - L11: "5. Adoption of the unsealed prereg and the production classifier."
- **A reading decision is already scheduled at the freeze.**
  - Codex3's step-5 root items (`ROOT_ITEMS_CX3V002.json`, `3e9e31d4…`), R12: "Root decides its radial-support interval before freezing flags."
  - Codex3's launch order (`LAUNCH_ORDER_CX3V002.md`, `829a8cb6…`) puts the first freeze pass (its item 6) after every headline run (items 4–5). It mentions neither the prereg seal nor any blinding of step-5 values.
- **The closest precedent blinds model outputs, not targets.**
  - V005 L189 (inside A51): "Only the status field and the key names of result.json were read; no row, speed or pass value was opened. C5H stays blinded until V007 is sealed, and before the seal it is read only through the compare's `--validity-only` mode (A47 I3)."
  - So the program already treats model outputs that bear on a prereg's outcome as blinded until that prereg is sealed.
- **Root reasons from public knowledge of the curve.**
  - 0522 L9: "A41 says static present-mass gravity cannot give a flat outer curve under any owned typing. So outer-row misses are expected".
  - 0522 L27 required r2's self-check "of whether any rule could be steered by the outcome". This channel is missing from C-9.
- **Two steering channels need no knowledge of the target at all.**
  1. The PRIMARY band width is visible in step-5 outputs. It decides whether M-1(a) absorbs outer misses as NEAR, so M-1 can be chosen knowing it. This contradicts the claim in C-9 L370 that "NEAR cannot be steered".
  2. A15 E1(b) (M-11) compares two model quantities. With step-5 outputs and a carrier in hand, its result is known before root chooses between (a), report it, and (b), NOT_AVAILABLE. That is a selective-reporting channel.
- **The principal's frame.** CURRENT_INSTRUCTIONS (`59ada35c…`):
  - L114: "Freeze model/parameters or admitted region, prediction protocol and predictions before target scoring."
  - L133 discourages "documentary cycles", so the fix should need no new tooling. The amended fix below needs none.

## 3. Severity: SHOULD_FIX stands

- **Why not a NOTE.**
  - The window is planned, not hypothetical: 0606 L5/L11, ROOT_ITEMS L226 and Codex3 R12 all put the reading decisions at step 6, or "before freezing flags", which is after step 5.
  - The toy in §5 shows that once the predictions are known, the choice of option largely decides P1 in marginal cases.
  - The program's own precedent (A47 I3; V005 L189) blinds model outputs before a prereg seal.
- **Why not BLOCKING.**
  - No sentence of r2 is false. Its blinding claims are about targets, and they hold.
  - Sealing the text as it stands, before step 5, would be safe.
  - The hazard is a missing guard that must be added before the seal, which is exactly what SHOULD_FIX means.

## 4. The proposed fix

### 4.1 Problems with the fix as worded

1. **"Produced or read" contradicts the next sentence.**
   - "Before any step-5 … output value is produced or read" means, literally, before step 5 runs. That makes "Until the seal, step-5 outputs are read validity-only" vacuous.
   - Read literally, it also gates step 5 on root's twelve rulings and on the M-12 classifier, which is sealed with the text. Root's account is nearly out of usage (0592), so this is a new schedule dependency.
   - The fix should bound **reading** and say that step 5 is never delayed for the seal.
2. **The fallback covers only the M rulings.**
   - The r3 fix rounds will change wording: B-2's support interval, B-4's precedence rule and B-5's first-score rule.
   - If those changes are drafted after step-5 values are readable, they are steerable in the same way, and "every M item is adopted exactly as written" does not touch them.
   - The M-12 classifier is also outside the fallback.
3. **"Exactly as written" is not always executable.**
   - M-7 "exactly as stored in that record" yields a point, not an interval. That flags no row, so P10 becomes vacuous. This is lens B-2's finding, and Codex3's R12 confirms it independently: "Current single sampled radius flags no query".
   - M-11's recommendation is itself conditional: "(b), unless root wants (a) and an owner can build it before the freeze".
   - The fallback needs defaults for both.
4. **It does not say who stays blind.** The bound must also cover:
   - the author, who drafts r3 and the classifier;
   - every reviewer of this text or the classifier, for example 0610 item 3 (Codex2).
5. **It names "M-1 to M-12".** Root items added in r3 would be outside the bound. It should read "every root item of this text".
6. **The validity-only view still shows reading-relevant facts.** The cut and roster records reveal the INVALID set, including OUTER, which bears on P0, P9 and N_v(OUTER). That is needed for the freeze and is harmless, but the attestation should list what was seen.
7. **Framing.** The stricter timing amends root's own A60 ("in the freeze step") and the 0606 deadline. It belongs in M-6 as a recommendation for root to rule, as the finding proposes. C-Status should then cite M-6, not state the timing as already ruled.

### 4.2 Amended fix (no new tooling)

1. **Tag and map the seal clause.** Tag it (for example `[C-S]`) and add a map row citing A60 L513, 0522 L19, 0585 L3, 0606 L5/L11 and M-6, so that T6 covers it.
2. **M-6 recommendation, for root to rule.** Root rules every root item of this text, and seals the text together with the M-12 classifier if adopted, before anyone reads a step-5 NGC route-A/B output value. "Output value" means any prediction, band, envelope, sensitivity row or alternative row. "Anyone" means root, the author, and any reviewer of the text or the classifier.
   - **Preferred:** seal before step 5 launches. Step 5 was "more than a day away" at 17:35Z (A80, V005 L1126).
   - **Step 5 is never delayed for the seal.** If it launches first, its outputs are handled status-only until the seal, as was done for C5H (V005 L189; A47 I3): receipt status, exit code, per-row validity booleans, cut and gate records, and reason codes. No value is printed, plotted or opened.
   - **Attestation.** The seal entry attests this and lists the validity information that was seen. Each lane that touched the text or the classifier after step 5 launched states that it read no step-5 value.
3. **Fallback, if any step-5 value is read before the seal.** Before that first read, root registers the sha of the text and the classifier as they then stand. This is the pre-prediction sha.
   - In that version, every open option takes its recommendation, and a rule that cannot be carried out reads NOT_AVAILABLE.
   - Every later change, whether a ruling or a wording change, is POST-PREDICTION: it is listed with its diff in the report header, and the report also gives the classification under the pre-prediction text.
   - A pattern or reading status that holds only under the post-prediction text is EXPLORATORY. This extends C-3's own EXPLORATORY rule.
4. **The same bound applies to the reading decisions now placed at the freeze:**
   - the radial-support interval (M-7; Codex3 R12);
   - the adoption of an evaluated STAGE0 (lens B-3; RUNBOOK L5; A65.2).

   Both are decided on receipts and target-free records only.
5. **C-9 gets a new row:** "Choosing reading rules after the predictions exist | closed by the M-6 timing". If root declines the timing, the row goes among the residual risks instead.

## 5. Reproduction: a toy showing the steering is real (synthetic and dimensionless)

**Files.**
- Script: `tools/steer_toy_v001.py` (`57a6abe825534f37a2892a3aa4b2b26882738c652ba60ff64dd65ff64494319f`).
- Output: `runs/STEER_TOY_V001.json` (`65f7ecf06a7ff2155aadf114d79ddab16011974a918892b9c70593e967e3313f`).

**Setup.**
- 43 synthetic rows: 24, 11 and 8 rows in the three zones, with the rule cuts at 10 and 30.
- The target shape is flat at 1, a non-physical sentinel.
- σ = 0.02.
- "Rough public knowledge" means the curve's level is known to within 3% (standard deviation), plus 1% noise per row.
- The predictions fall below the shape by a fraction d toward the outer edge, and the band half-width is w.
- The toy implements the §1.1 tiers (with the M-1 options) and the §2 rules for P1.
- Each probability comes from 20,000 draws of the unknown target level.

**Results.** Probability that P1 holds, by option:

| case, once predictions are seen | M-1(a), as written | M-1(b), NEAR 1<\|r\|≤2 | M-1(c), no NEAR | M-3, miss-dominated at ≥ 2/3 |
|---|---|---|---|---|
| marginal deficit (d 0.06), wide band (w 0.08) | 0.069 | 0.632 | 0.821 | 0.039 |
| marginal deficit, narrow band (w 0.03) | 0.526 | 0.637 | 0.828 | 0.413 |
| no deficit | 0.054 | 0.103 | 0.253 | 0.035 |
| large deficit (d 0.30) | 1.000 | 1.000 | 1.000 | 1.000 |
| **blind** (d ~ U(0, 0.3), w ~ U(0.01, 0.08)) | 0.756 | 0.839 | 0.904 | 0.708 |

**What it shows.**
- **Marginal case:** once the predictions and the band are visible, the choice between options moves P1 from about 7% to about 82%.
- **Clear-cut cases:** a ruler who has seen the predictions knows that nothing depends on the choice, so it costs nothing.
- **Blind ruler:** knows only the prior averages.
- **Scope:** the toy illustrates the mechanism only. It says nothing about the real galaxy.

## 6. Files in this folder

- `VERIFY.md` (this file);
- `REVIEW.md` (a short summary);
- `PARTIAL.md` (the running log);
- `HASHES.txt`;
- `snapshots/V005_AT_VERIFY.md` (`50fe0f1c…`) and `snapshots/V005_AT_VERIFY_2.md` (`6145a1f9…`);
- `tools/steer_toy_v001.py` and `runs/STEER_TOY_V001.json`.
