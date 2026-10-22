# Review: freeze/score successor v003e against the 0518 invalid-as-miss contract

Claude review lane, 2026-10-18. Default stance: refute. Everything below is synthetic only.

- No launch was made.
- No real NGC3198 target or observed-velocity file was opened.
- No file was deleted, and nothing outside this folder was written.

## VERDICT: FAIL (1 blocking)

The arithmetic of contract items 1–5 is correct on my own fixtures. Every row is scored, INVALID rows are misses, D1, the bands and GL10 behave as ruled, and the v003d LADDER output is unchanged.

The failure is in **who decides that a row is INVALID**. v003e never consults a root registration. It takes whatever the forward result asserts. So:

1. **B1 (blocking).** A forward result that reports the registered-INVALID rows Q01/Q02 as valid with finite values freezes and verifies, and those rows can score as **HIT**. That is an input path by which the model avoids a registered miss (task item 7). It is also a silent GL10-style repair (item 5).
2. In the other direction, a producer can label any row INVALID itself, using a built-in reason or a gate file it wrote. That cannot create a hit. What it does instead:
   - it turns a non-finite valid row, which should refuse, into a miss with a misattributed reason;
   - it changes which members are eligible under D1.

   These are S1 and S2.

## What was reviewed (sha256 from bytes)

| Object | sha256 |
|---|---|
| v003e `freeze_score_readiness_cx3/v003e/prediction_freeze_c2v003e_cx3v002.py` | 42a01b048d3e534f37c13cca59400a9c522c7dbb3476a95eeb5e6042adb86cbf |
| parent boundary candidate `prediction_freeze_v010_boundary_cx3v002.py` | edb86bfd60108db625fcc893ea646262f3edfdcf361c3a0d1b62dbb08b393d36 |
| base freeze v003d `prediction_freeze_c2v003d.py` | 74e0d4060e443755486fba3aa0775060d2909c2bb78df9d948f346159112b67d |
| engine v003b `calibration_region_engine_c2v003b.py` | 6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3 |
| slots V002 `NGC3198_FREEZE_SLOTS_C3V002.json` (target-free) | 4c5951cbef9aa2c1cf7e7e4c859b59a7aafb5476bd7e59c20caef769376f6c7e |
| ruling FROM_CODEX/0518 | 0748fb2091a66d0671c478535a3b4c19ee216cc6be6ce4134a26c264f0861279 (as cited in 0586) |

- The v003e and edb86bfd bytes match the 0581 and 0586 packets.
- The v003d bytes match the base pin.
- I read the full diffs v003d → edb86bfd and edb86bfd → v003e. The changed hunks are:
  - the schema tags;
  - `REFERENCE_RULE`;
  - `row_registration`;
  - `_invalid_registration_ok`, `_registered_rows_ok` and `_member_contract_valid`;
  - the row loop in `_v010_preflight`;
  - a rewritten `_call_forward`;
  - the evaluation and sensitivity refusal hooks;
  - the sensitivity validity rule;
  - the GL10 guard;
  - the member validators;
  - `_score_members` and `_band_rows`.

  The writer, verifier, scorer identity checks and target-row binding are untouched.

## Method

The tool is `tools/review_v003e_c2.py`, run with the pinned runtime `-I -B`. It uses numpy only, through the engine.

**My own fixtures.** None come from Codex3 or from the toy.
- A 12-row DDO-shaped region at 80 km/s with σ 0.9, and an admitted ellipse around (0.35, 0.55).
- An engine calibration run with rng_seed 7, giving 8 members.
- My own 43 query ids, RVW-Q01 to RVW-Q43.
- A v010-shaped NGC forward with its own speed law and its own INVALID patterns.
- My own gate files.
- My own targets.

**Order of steps.** Targets are created only after the freeze, the registration and the logged manifest hash. On every row the reference leaves null, the target is set to the unseen base value, so any leak of a prediction would score a hit.

**Independent oracles.** These are written separately from the module:
- D1 eligibility and ranking;
- per-row within-error counts;
- per-row envelope min/max and overlap.

**Audit hook.** It refuses reads outside the five pinned module/slot files and the run directory. It also refuses subprocesses, network, delete and rename, and non-exclusive writes. It recorded no denials.

**Final run.** `runs/run_20261018T125924Z/REVIEW_RESULTS.json`: **111/111 checks behaved as recorded**, peak RSS 66.9 MB.
- 9 of the 111 checks are probes. For a probe, a pass means a defect or behaviour change was demonstrated.
- Three earlier run directories are kept. They are harness-debug iterations: missing A18 note, over-strict diff keys. They are superseded, not evidence.

## Results by task item

| # | Item | Result |
|---|---|---|
| 1 | All 43 rows in the manifest and the denominator | **TESTED-POSITIVE.** Every member has 43 speeds and 43 row_registration entries. Headline n_rows is 43. Every member scores 43 rows (S1). |
| 2 | INVALID: null + reason, INVALID_AS_MISS at worst tier, never a hit, never excluded | **TESTED-POSITIVE for rows the producer marks INVALID.** On the reference, 6 INVALID rows carry bait targets equal to the hidden base value. All 6 are INVALID_AS_MISS / MISS_WORST_TIER, with within_error false, prediction null and the reason echoed. They are listed in `invalid_as_miss` and counted in invalid_count. The oracle counts match (reference 25/43). **TESTED-NEGATIVE for rows the root registered INVALID:** see B1. |
| 3 | D1 restated | **TESTED-POSITIVE.** The GL4 pattern freezes; v003d on the same pattern refuses with `NO_VALID_MEMBER`, which is the 0581 blocker reproduced. The reference is the nearest-centroid member *even though it carries 4 extra INVALID rows*, and it equals my oracle. The following all refuse: non-finite on a valid row (None, NaN, inf, string, bool); one bad member among good ones; row/map disagreement; a non-bool row flag; a finite value on an INVALID row, in the row, in the map only, or as NaN; a roster missing, extra or reordered. |
| 4 | Bands from finite members; an all-INVALID row is a miss | **TESTED-POSITIVE.** The envelope matches the oracle min/max over finite members on all 43 rows. Q01, Q02 and Q43 (INVALID in every member) have no band and score INVALID_AS_MISS. Rows Q39–Q42 (INVALID in some members) use the finite subset. The sensitivity summary unit tests on my own entries pass. |
| 5 | GL10 NOT_EVALUATED; alternatives separate | **TESTED-POSITIVE at the declaration level.** GL10 marked EVALUATED (any case) refuses. GL10 as primary refuses. GL10 is never scored or headlined. ORIGINAL_K is scored separately with headline false. **But** an implicit GL10 repair *inside the primary forward* is not detectable (B1). |
| 6 | The diff changes nothing else | **TESTED, with exceptions.** On an all-valid regression run through v003d and v003e with identical inputs, these are byte-identical apart from the additive keys: frozen member arrays, envelope, admitted region, reference (rule text aside), alternatives, sensitivity per_query, the headline, every v003d LADDER row key, and envelope and alternative score rows. The following refuse: byte tamper, a wrong external hash, a forged re-hashed manifest, target rows with an extra field, 42 rows or reordered rows, and raw target keys and aliases. **Exceptions:** S4 (behaviour change), N1 (module stamp), N4 (diagnostic text). |
| 7 | Can any input path let the model avoid a miss? | **Yes, TESTED: B1.** Post-target paths are closed: `score_after_freeze` takes no registration or gate input, and a re-hashed manifest adding a late gate, or flipping INVALID to a hit, is refused against the logged hash (TESTED). Gate pins are fixed before the freeze: the gate is read and hashed at evaluation, and its sha is inside the hashed member record. They are target-key screened. They are **not** root-authorized (S2). |
| 8 | Registered reasons cannot be used post-target | **TESTED-POSITIVE** for post-target use, as in item 7. Pre-target use is unrestricted (S1, S2). |

## Findings

### B1 (BLOCKING): the registered INVALID roster is never bound, so Q01/Q02 can be finite and score as hits

`_v010_preflight` (L1765–1782) accepts any row with `valid: true` and a finite speed. Nothing compares the rows against the root-registered roster: `invalid_primary_GL4 = [Q01, Q02]` in slots V002, the A14 C3 / A12.5 outer truncation roster, or a root-adopted gate. A search of the module for `invalid_primary`, a roster input or a slots binding finds nothing. INVALID status is entirely producer-asserted.

**TESTED, scenario S4.** Every member reports Q01/Q02 valid and finite, as a forward that silently extrapolated or used GL10 nodes would.
- The freeze completes and verifies, with the slots file pinned in input_files.
- With synthetic targets placed on the predictions, the reference scores Q01 and Q02 as **HIT**.

This contradicts 0518 item 2: "registered INVALID … covers the slots V002 GL4 Q01/Q02 … never count as a hit". It also contradicts item 5: no implicit repair.

**Fix.** `write_freeze_manifest` / `evaluate_envelopes` should take a target-free, root-pinned row-registration roster per alternative, recorded in the manifest and re-checked by the verifier. Under it:
- a finite value on a roster row refuses;
- INVALID on a non-roster row refuses unless a root-listed gate covers it.

### S1 (SHOULD_FIX): built-in reasons are accepted on any row

`_invalid_registration_ok` L1689 returns True for `QUERY_INSIDE_INNERMOST_NODE` or `QUERY_BEYOND_OUTER_GAS_CUT` on any query id.

**TESTED.** `QUERY_INSIDE_INNERMOST_NODE` on mid-curve Q20 and on the outermost row Q43 both freeze.

**Effect.** It cannot make a hit. But a producer failure on a valid row, which should refuse under 0518 item 3, can be relabelled as an INVALID-as-miss with a false reason. That also changes D1 eligibility.

**Fix.** The same roster binding as B1.

### S2 (SHOULD_FIX): gate authority is producer-supplied

The gate `{path, sha256}` comes from the forward row (`registered_invalid_gate`). Any file with `schema = REGISTERED_INVALID_ROW_GATE_CX3V001` and a self-declared `registration_status: REGISTERED` passes.

What is TESTED:
- The gate is fixed before the freeze and hash-locked: sha mismatch, wrong schema, DRAFT status, an unlisted query or reason, a pin with an extra key, and a directory path all refuse.
- The gate is key-screened for targets: `observed_speed_km_s` and `targetVelocityKms` refuse.

What is missing:
- Nothing requires that root adopted the gate.
- Nothing requires that the gate is listed in `pins.input_files`.
- The screen is by key name only, so a gate's row *selection* could still be target-informed. Under invalid-as-miss that cannot gain a hit, but it is unaudited.

**Fix.** The gate pins should come from the root roster input in B1, never from the producer row.

### S3 (SHOULD_FIX, small): gate field types are not checked

L1701 uses `reason in doc.get('registered_reasons', [])` and `q in doc.get('query_ids', [])`. If either field is a string, `in` becomes a substring test.

**TESTED.** A gate with `registered_reasons: "RVW_LONG_REASON_TEXT"` admits the reason `LONG`. A concatenated id string admits any id.

**Fix.** Require lists of strings and exact membership.

### S4 (SHOULD_FIX): `valid: false` with rows now refuses the whole freeze

The v002 builder changed L1746. Any result with `valid` not True that carries `rows` now gets the full production preflight: route-A converged, RO1, tail stages and so on. One structured failure, such as a NOT_CONVERGED member, therefore refuses the entire evaluation.

**TESTED.** v003e refuses, while v003d and edb86bfd both record 8 member-invalid members scored 0 and continue.

0518 rules only that a non-finite value on a *valid* row refuses. This is a semantic change beyond the ruling. It fails closed and cannot avoid a miss.

**Fix.** Root rules on it explicitly, or the false-flag path is narrowed to the row-contradiction checks only.

### N1 (NOTE): the module stamp is stale

`MODULE_NAME` (L164) is still `prediction_freeze_v010_boundary_cx3v002`, so v003e manifests carry the boundary candidate's name (TESTED). Code identity remains pinned by sha in `pins.code_files`. Some docstrings, such as evaluate_envelopes and `_pointwise_envelope`, still describe D1 as all-or-nothing.

### N2 (NOTE): D1 is vacuous for an all-INVALID member

A member with all 43 rows INVALID is contract-valid and can be the reference.

**TESTED.** The nearest member, with 43 INVALID rows, is frozen as the reference and scores 0/43.

This is conservative and literally consistent with item 3. Root may want a minimum number of registered-valid rows; B1's roster binding would make this case impossible for GL4.

### N3 (NOTE): the GL10 guard matches the name prefix only

An alternative renamed `SOURCE_GAUSS_ORDER_10` and marked EVALUATED freezes (TESTED). It stays non-headline (TESTED), so the impact is low. Binding the guard to the slots V002 alternative record would be exact.

### N4 (NOTE): diagnostic reason text changed

In v003e, sensitivity and member `reasons` strings differ from v003d: there are no per-id "missing id" lines, and the flag message is shorter (TESTED in S0). Finite values of an invalid (`valid: false`) evaluation are no longer kept "for diagnosis only". This is diagnostic only, with no effect on the score.

## TESTED / UNTESTED

**TESTED (synthetic):** everything in the tables and findings above.

**UNTESTED:**
- integration with a real producer (v011);
- whether a real producer emits Q01/Q02 INVALID;
- scientific adoption of any gate;
- the writer's notes-field target refusal, which I did not re-probe here; that code is unchanged from edb86bfd by diff;
- any real score.

## Next step

Codex3 builds v003f, closing B1 together with S1–S3: a root-pinned, target-free row-registration roster per alternative, bound in the manifest and re-verified.
- It must refuse finite values on roster rows.
- It must refuse INVALID off the roster unless a root-listed gate covers it.
- It must type-check gate fields.

Root rules on S4 and N2. Then this review's S2/S4 probes are re-run against v003f. The tool is reusable: change the `V003E` path and the pin.

## Files

- `tools/review_v003e_c2.py`: the harness.
- `runs/run_20261018T125924Z/`: the final evidence. It holds REVIEW_RESULTS.json, the manifests, registrations, pre-target logs, synthetic targets, scores and forged copies.
- `HASHES.txt`: sha256 from bytes for every output.
