# S4-R-C1 design brief: LO producer successor and per-point certificate registry (31 points)

**Scope.** This is a synthesis by the Claude3 lane for the S4-R-C1 build (A122). Work began at 2026-10-19T07:13:21Z, read from `date -u`.

**How it was done.**
- Read-only. No producer, driver, guard, wrapper or native_preflight was executed on real inputs.
- Nothing was opened under runs_ext, `UVT_*`, C5H or an NGC3198 target.
- My only writes are three key and table scripts in my scratch folder.
- Maps 3 and 4 (GQ/EPS-rho and the points map) were cut off in the task text. I rebuilt their content from bytes. Sibling scratch files served only as pointers, and every key below was recomputed by my own script.

**Labels.**
- **TESTED**: read or recomputed from bytes in this session.
- **FORMAL**: inference from code or records.
- **UNTESTED**: an estimate nobody has measured.

Short pins such as `(24abe3bc)` are the first 8 hex digits of the sha256. Full paths and shas are listed in the Pins section at the end.

---

## 0. What changed since the maps

- **V006 addendum.** It is now `78f04f7f` (read at 07:37Z), and A123–A128 have been appended.
  - A125 (L293-322): V007 sealed at 07:00:44Z.
  - A127 (L330-362): step 2 was relaunched as R2 at 07:31:06Z, after a ps-sum RSS artifact stopped C4T-KHI.
  - So CP-1 window (b) is open now. The A122 text (L237-251) is unchanged. (TESTED)
- **v006r10_c4 (A126).** The wrapper `ef3d3d69` differs from r9 `24abe3bc` only in its core pin. The core `dc895f8a` differs from r9 `a595c5c0` only in its adoption-policy pin (diff).
  - So `certificate_check`, `point_identity` and `Mapper.build` are unchanged, and the bundle contract below holds under r9 and r10_c4. (TESTED)
- **guard v008 `f27a4868` and v009 `5986c4c5`.** They differ from guard007 `42bf0ce9` only in two places: the generated-buffer owner sha (now the r10_c4 wrapper) and the A124 disk guard.
  - `lexical_path` (L25-30), the fence (L190) and the fenced `certificate_check` (L210) are unchanged. Risk R1 below therefore persists. (TESTED, diff)

---

## 1. The exact per-point bundle contract

### 1.1 Registry entry (C1 `tail_readiness.certificate_registry`)

**Key.** Key = sha256 of the canonical JSON (sorted keys, separators `(',',':')`, `allow_nan=False`) of:
`point_identity = {driver_sha256: b5cc62af…, physical, coefficients, numerics minus uv_tail.eps_certificate and uv_tail.lo_certificate}`.
- Source: core L34-38 and L233-238 (`a595c5c0`). The same form appears in the guard (L21-26), guard007 (L74-75) and custody (L25-29, L80-86). (TESTED)
- The label and both slots are outside the key, so keys do not depend on slot values. (TESTED)

**Record.** Each record is `{identity, bundle, eps_certificate, lo_certificate}`, and each pin is exactly `{path, sha256}`.
- The wrapper L86-90 requires `rec['identity'] == ident`. Otherwise it returns `CERTIFICATE_POINT_MISSING_OR_MISMATCHED`. It then uses only `rec['bundle']` (L119).
- Mapper L249-259 reads `rec['eps_certificate']` and `rec['lo_certificate']` (a KeyError if either is absent), runs `read_pinned` on each and copies them into the spec's uv_tail slots.
- No code checks a registry schema field. (TESTED) Write one anyway, together with a generator pin. (FORMAL)

### 1.2 Bundle manifest

Sources: guard L84-102, L133, L142, L153-154 (`5f1e49e6`); wrapper L140-147.
- `schema`: `UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001`.
- `identity` equals `point_identity(spec)`.
- `custody` equals exactly the five-key dict that the pinned deriver returns at PRELAUNCH: `{grid_sha256, background_sha256, geometry_sha256, modules_sha256, row_contract_sha256}`.
  - Sources: guard L16-17, L77-80, L87-88; custody L136-139, L143-144 (`6810b7c3`).
  - `background_sha256` includes `physical`, so custody is unique per point. (TESTED)
- `domain` is exactly `{K_inverse_kpc: 4.0, K_big_inverse_kpc: 128.0}`. The guard also allows 64, but `validate_block` (core L220-221) forces 128.
- `prelaunch` holds three pins: `{EPS, GQ, LO_ENVELOPE}`.
- `driver_certificate_bindings` equals `{eps_certificate, lo_certificate}` as they stand in the spec's slots (wrapper L145-147).
- `acceptance_rule`: `ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED`.
- `states` and `parent_prelaunch_bundle` are used only at acceptance (guard L155-219; wrapper L141-144).
- **File constraints.** These apply to the bundle, each proof and each proof producer:
  - the path resolves under `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts`;
  - the file is at most 8 MiB;
  - no path component starts with `uvt_` (case-insensitive) or equals `kmax_a2f10_c5h_run_v001` (guard L37-55, L105, L115);
  - under guard007's fence, no component contains `ngc3198` (guard007 L29). (TESTED)

### 1.3 The three proofs

All three share these fields (guard L104-117):
- schema `UNT_CALIBRATION_POINT_PROOF_CX2V001`, status `TESTED`, verdict `PASS`;
- `point_sha256` equals the key;
- `custody_sha256` equals `digest(custody)`;
- a `producer` pin whose sha is in the approved set and whose bytes re-hash under claude_artifacts.

**EPS proof.**
- Gate `EPS`, `envelope_rule` `A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS`.
- `shells` start at exactly 4.0, are contiguous with hi > lo, and reach at least ceil(√2·128) = 182.
- Each shell has `refinement_failures` as an int in {0, 1}, and a finite `eps ≥ eps_envelope ≥ 0` (guard L119-140).
- The wrapper adds three checks (L148-159):
  - `driver_certificate` equals the spec's eps slot;
  - the slot file re-hashes;
  - the producer pin is an element of `approved_certificate_producers`, compared as a whole dict.
- The only producer is `adapt_eps` (adapter v003 `4de70486` L167-198). It sets `driver_certificate = numeric_ref`, the point's EPS numeric record. So every point's eps slot is its own cx2v002 EPS record. (TESTED)

**GQ proof.**
- Gate `GQ`, method `GEOMETRY_UNIFORM_COLUMN_BOUND`.
- `all_columns_included`, `all_production_kperp_nodes` and `nonnegative_masses_required` are all true.
- `M_s` 128, `M_s_doubled` 256, `K_big_inverse_kpc` 128.0.
- b and z are finite and ≥ 0, z < 1, and b/(1−z) ≤ 1e-12 (guard L142-152). There is no driver_certificate check.
- The producer is `gq_producer_cx2v005` (`2832ceb9`) `produce()` (L60-65). It emits this proof directly. (TESTED)

**LO_ENVELOPE proof.**
- Gate `LO_ENVELOPE`. `driver_certificate` equals the spec's lo slot. `covers_all_consumed_states` is True. The producer is approved (wrapper L148-161).
- The guard contains 0 occurrences of `LO_ENVELOPE` (grep). No consumer checks any LO number at prelaunch.
- **No producer exists.** (TESTED)
- Consequence: the numbers must be checked inside the new adapter. (FORMAL)

### 1.4 Records behind the proofs (per point)

**EPS numeric record.**
- Schema `UNT_POINT_EPS_NUMERICAL_CX2V001`, from `point_response_producer_cx2v002` (`a1dcdea8`) `produce_eps` with settings `registered` over the full domain.
- 178 unit shells, [4,5] through [181,182]. Each shell has:
  - discrete levels of 26, 52 and (if refined) 104 directions;
  - an envelope: 12³ torus × 200 hemisphere directions × 3 radii = 1,036,800 grid points, then 8 starts on the first shell and 9 on later shells (the 9th is the previous shell's optimum), × 48 candidates × up to 120 iterations;
  - an actual-set search: 2,000 + 8,000 directions at 256 per decade, with local refinement.
- Plus 14 dense audits, at 20³ × 400 × 5 with 16 starts, on the shells starting at 4, 5, 6, 8, 12, 16, 19, 32, 45, 63, 64, 100, 128 and 181.
- Sources: producer L31-39, L112-136, L183-245, L288-329. The adapter enforces the counts, seeds and starts (L56-164). (TESTED)

**EPS review (one per point, written after the record exists).**
- Schema `UNT_POINT_EPS_REVIEW_CX2V001`, verdict `APPROVED`.
- `numeric_ref` is the exact record pin, plus `point_sha256` and `custody_sha256`.
- `accepts_registered_numerical_estimate_not_rigorous_sup` is true, and `adapter_sha256` is `4de70486…`.
- Its sha must be in `approved_review_sha256`, and a1dcdea8 and 4de70486 must be in `approved_producer_sha256` (adapter L177-188). (TESTED)

**LO numeric record (successor, see section 2).**
- It embeds the full registered rho record (`rec['rho']`, lo_core L448, L461).
- So the "rho table" lives inside the LO record. No consumer reads a standalone rho record. (TESTED)

**GQ record.** One per point. (TESTED)

### 1.5 C1, policy and guard007 preconditions (root items)

**C1 tail_readiness.**
- `certificate_registry`, `certificate_policy_review`, `custody_deriver` and `state_enumerator` must each be a pin dict.
- `approved_certificate_producers` must be a non-empty list of pins (wrapper L59-66).
- The r9 config today (`721c7230`): producers `[]`, policy review null, registry null, `custody_deriver` = custody_cx2v002 (`6810b7c3`), `state_enumerator` = consumed_states_cx2v010 (`e48cca3c`), both slots `PENDING_UV_TAIL_CERTIFICATE`. (TESTED)

**certificate_policy_review.** Checked by `checked_gate`, core L66-82 and wrapper L70-75.
- schema `DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001`, status TESTED, `ok` true;
- fields equal to: driver_sha256 (r5), custody_deriver, state_enumerator, the same approved_certificate_producers list, guard_sha256 `5f1e49e6…`;
- `driver_slot_rule` `POINT_EPS_AND_REVIEWED_PRELAUNCH_LO_ENVELOPE`;
- `post_state_handoff` `TAIL_CERTIFICATE_ACCEPTANCE_CX2V001`. (TESTED)

**Approved producers, minimal set (FORMAL).** EPS adapter v003 `4de70486`, GQ producer v005 `2832ceb9`, and the new LO_ENVELOPE adapter.
- The custody `pin()` writes `str(Path(__file__))` unresolved (custody L48-49), and the wrapper compares whole dicts (L158).
- So the runner must import each producer from its canonical absolute path. (TESTED code; FORMAL consequence)

**guard007 (and v009).**
- Each readiness pin is verified (L200-201); a null registry gives `PIN_REQUIRED`.
- Producers must be non-empty, and each must be an allowlisted source (L202-205). The custody deriver and the enumerator must also be allowlisted (L205).
- Under the fence, every `.py` file opened under `/Research/` must be in `cfg['sources']` (L114-122). That includes every file the custody deriver hashes through `uvt_static_pins`. (TESTED)

### 1.6 PRELAUNCH with an unregistered point, a null registry, or pending slots

- **Unregistered point.**
  - The wrapper returns `CERTIFICATE_POINT_MISSING_OR_MISMATCHED` (L86-90), and the bare `prelaunch_check` raises `CERTIFICATE_PREFLIGHT` (L178-180).
  - guard007 `positive_gate` then raises `Refusal NATIVE_GATE_REFUSED` (L153, L210).
  - There is no TAIL_REANCHOR exemption in the code. (TESTED)
  - Claude4's fenced look-alike probe (`4cfc6283`) recorded this refusal for TAIL_REANCHOR, the seed and an adaptive point. (TESTED there)
- **Null registry.** The bare r9 `prelaunch_check` skips the certificate check (L178). guard007 refuses with `PIN_REQUIRED`. (TESTED)
- **Pending slots.** The driver refuses PENDING slots (L1076-1082) and checks a filled slot by sha only (L1086; library `2026f2b6` L664-674).
  - Slot pins enter the normalized uv_tail config sha (library L114-129), and through it the spec bytes and the cache id (wrapper L52-55). (TESTED)

### 1.7 Ready vs missing

- **Existing GQ record.** `GQ_P128_MS128_C000_R5_CX2V001` (`a785ccca`) is a correct-form GQ proof for HEADLINE_CORNER_000: point_sha256 `64dc775b…`, custody `c0b20cc7…`, b/(1−z) = 3.14e-14, seconds 37.13. (TESTED)
  - It passes PRELAUNCH only if the re-derived custody equals `c0b20cc7` and its producer is approved. (FORMAL)
- **Nothing else exists.** No full registered EPS or rho record and no LO envelope exist in `calib_tail_readiness_cx2` or `review_certs_per_point_c4` (grep for `full_registered_search_executed: true` and `numerical_envelope_executed: true`). (TESTED)

---

## 2. LO successor: the minimal change (physics first, then code)

### 2.1 What LO certifies

**The lapse-only omission.**
- The production tail beyond the K4 cube, out to the K_big cylinder, enters field component 0 (the lapse) only. Components 1–9 (spatial metric and volume) are omitted.
- Certificate LO bounds the effect of that omission.
- A failure reads NON_LAPSE_TAIL_MATERIAL. A design successor then carries all 10 components (design V002 L59, L254-261, L657). (TESTED)

**The indicator.** |Δv_i,s| ≤ |v_i| R_i ρ_s B1_s / 4 (lo_core `12d36305` L8-11; per-row ratio L165).
- **ρ_s** is the registered numerical search of 4γ_eff|k|²‖C̄^-1/2 mat(x[1:7]) C̄^-1/2‖₂ (producer L171-180, L332-364).
  - It is invariant in s and depends on γ/Eref and ℓ_F (analysis `4084bd59` L8, L12-15).
- **B1_s** is a production-node quadrature of 2|S| · pref · w_kp · k · w_z · c0/|k| over the tail domain, with pref = λ/(4γ_eff(2π)³) (L109-139, L383-398).
  - So B1 ∝ 1/γ_eff for a fixed source.
- **Pass rule.** Every shell max ≤ 0.005 τ_i, taking the max over the 12 rows, and the sum ≤ 0.05 τ_i (L171).
  - τ comes from prereg v005 through the custody row contract (custody L119-128): [0.4, 0.2, 0.175, 0.125, 0.1, 0.05, 0.05, 0.05, 0.075, 0.15, 0.175, 0.325] km/s.
  - That is 0.25 m/s per shell at the tightest rows. (TESTED)

**What CP-1 needs: the prelaunch conditional envelope.**
- |S| is replaced by the majorant c² Σ_i |Π_i(k⊥)| Σ_c cap_ci / (2π rdr_i), plus a stars term (L270-294, L386-391). The majorant does not depend on k_z.
- It is evaluated on the point's exact K128 production nodes (L364-367): unit shells from 4 to 182, aggregated into the 9 ρ shells [4,5,6,8,12,16,32,64,128,182] (L380-381; producer L116-121).
- It is valid only on the condition that every constructed or consumed source and readout stays inside the caps (L460; `enforce_caps` L322-358). (TESTED)

**Physics risk (FORMAL).**
- The envelope discards cross-column radial cancellation and the vertical phase. So B1_env ≥ B1_actual, and the gap grows with k.
- No envelope has ever been computed, so its inflation over the actual-state LO is unknown. The anchor's actual-state value is 3.95e-4 τ on (128,256] at K256 (LO_CERT_V004 `1c384f76`).
- At the six Q∞≈161 points, Codex2's fixed-source replay already reads 0.00654 τ (corner_00) and 0.00604 τ (corner_01), above 0.005.
  - That replay used enclosing shells to 256, the anchor's saved source and the anchor's speeds (box report `3ff6070b` L13-20).
  - An honest failure there is plausible before any inflation is added.

**How to read a failure (FORMAL).**
- An actual-state failure means NON_LAPSE_TAIL_MATERIAL.
- `CONSERVATIVE_CAP_ENVELOPE_ABOVE_THRESHOLD` (lo_core L455) means the bound cannot certify the point, so LO stays BLOCKED. It is not a finding that the non-lapse tail is material.
- Neither result may be relabelled. Caps may not be re-tuned after the number is seen.

### 2.2 Why v004 can never pass (TESTED)

- **finish() overwrites every result.** `finish()` L25-40 always sets:
  - `certificate_status` and `verdict` to UNAVAILABLE;
  - `production_admissible` to False;
  - `point_status` to NOT_ADMITTED or INCOMPLETE;
  - the blocker `LO_GUARD_AND_DRIVER_CERTIFICATE_ADAPTER_REVIEW_PENDING`, if nothing else blocked.
- **Every return path goes through it** (L43-46, L52-82, L91-94).
- **This is intended.** See the docstring at L6 and 0528 item 2 (`d11654e5` L6): "Until then, prelaunch LO reads UNAVAILABLE and the point is not admitted."
- **The core never says PASS either.**
  - Its best verdicts are `CONDITIONAL_NUMERICAL_EVIDENCE_REVIEW_REQUIRED` (L457) and `CURRENT_LO_NUMERICAL_EVIDENCE_REVIEW_REQUIRED` (L264).
  - Its record uses the schema `UNT_POINT_LO_NUMERICAL_CX2V001` with gate `LO` and `driver_certificate` None. Its limitation reads "standalone evidence schema; not a driver slot certificate" (L178-187).
- **The conditional path blocks unless all of the following exist** (L411-439):
  - a cap contract;
  - a cap review whose sha is in the caller's trusted list, with verdict APPROVED;
  - `producer_sha256` = 12d36305 and `response_producer_sha256` = a1dcdea8;
  - the enforcement flags `every_constructed_and_consumed_state`, `reject_before_consume` and `complete_stage_inventory_reviewed`, plus an enforcement module pin;
  - three convention and coverage flags.
  - The facade adds `distinct_from_producer_lane` and `reviewer_lane` (v004 L87-93).
- **No LO adapter exists**, while EPS has `adapt_eps`.
- **Writers are fenced to Codex2's folder.** The CLI writers only write inside it (custody L146-151; lo_core L526).
- **Review and registration.** Claude4's review `bc211c3a` is PASS with 0 blocking, scoped to the producer build. Its N1 records this exact point. Nothing is registered.

### 2.3 Minimal successor (FORMAL design)

**Keep byte-unchanged:**
- lo_core `12d36305`, point_response_producer `a1dcdea8`, custody `6810b7c3`, and lo_config `6654d93c` if it is used.
- This keeps Claude4's review valid, and the cap-review binding `producer_sha256 = 12d36305` (L424) still holds.

**Add three files** in a new Claude3 folder under claude_artifacts. No path component may start with `uvt_` or contain `ngc3198`.

- **(a) Prelaunch facade.**
  - It keeps v004's distinct-lane check and calls `produce_conditional_lo(spec, cap_ref, review_ref=…, trusted_review_hashes=…, settings='registered', shell_ranges=None, context=ctx)`.
  - It maps outcomes without overriding them. A result is clean only when all of these hold:
    - verdict `CONDITIONAL_NUMERICAL_EVIDENCE_REVIEW_REQUIRED`;
    - `blockers == []`;
    - `numerical_envelope_executed`;
    - `covers_all_consumed_states`;
    - `rho.full_registered_search_executed`;
    - `rho.settings == 'registered'`.
  - A clean result reads `ENVELOPE_AVAILABLE`, with `production_admissible` still False.
  - Every other result is BLOCKED or UNAVAILABLE, with the core's blockers kept verbatim. So 0528 item 2 still holds whenever caps, review or enforcement are missing.
- **(b) LO_ENVELOPE adapter, modelled on `adapt_eps`.** It:
  - re-derives custody;
  - reads the LO record by pin and checks schema and kind `PRELAUNCH_CONDITIONAL_SOURCE_ENVELOPE`, identity and custody, and that its producers are 12d36305 and a1dcdea8 and are approved;
  - checks that the cap and review refs are readable, the review is APPROVED and the reviewer is distinct;
  - recomputes, from `per_row_over_tau`, the 4→182 tiling, every shell max ≤ 0.005 and the sum ≤ 0.05;
  - recommended (as for EPS): requires a distinct per-point LO numeric review that binds the record bytes;
  - emits a `PROOF_SCHEMA` gate `LO_ENVELOPE` TESTED/PASS proof containing point_sha256, custody_sha256, `producer` = the adapter pin, `driver_certificate` = the LO numeric record pin (the lo slot), `covers_all_consumed_states` True, shells, `summed_max_over_tau`, `row_contract_sha256`, the cap and review refs, and the condition text.
- **(c) Writer.** An exclusive-create writer (`open('xb')`, same encoding as custody L149), confined to the Claude3 folder.

**Not needed for CP-1.** The per-state acceptance LO adapter (guard L205-219) belongs to CP-2/R-B5, which A122 does not assign.

**Decisive outside dependency (FORMAL).**
- The cap review cannot truthfully set the enforcement flags or the module pin until an enforcement module exists.
- No run-path code calls `enforce_caps`. A grep over `driver_r5`, `route_a`, `route_b`, `module`, `v006r9`, `v006r10_c4` and `step4_launch_packet_cx1` finds nothing; only the LO family and tests match. (TESTED)
- Driver r5 is fixed (A96). So enforcement can only be a post-run, pre-acceptance check over each call's enumerated consumed states (`consumed_states_cx2v010` + reconstruction → `enforce_caps`).
- Without it, lo_core returns `REVIEWED_ENFORCEMENT_MODULE_MISSING` / `CAP_ENFORCEMENT_*` (L426-431).

### 2.4 Inputs per point (prelaunch)

- **Spec.** The dry-plan spec bytes are enough, because identity excludes the slots (section 3).
- **Point context.** `PR.point_context(spec)` (producer L73-109) gives custody plus a new Binder with Eref = s·Eref_J and γ_eff = s·γ. Compute it once and pass it as `context=` to EPS and LO.
- **Cap contract** `UNT_POINT_LO_CAPS_CX2V001` (lo_core L297-319):
  - identity and custody;
  - `component_names`;
  - `component_column_TV_mass_caps_kg` of shape (n_components, 4·(len(s_edges)−1));
  - `mass_convention` `ACTUAL_PROPER_SOURCE_TOTAL_VARIATION_PER_COLUMN`;
  - `fixed_registered_stars_multiplier_abs`;
  - `gas_z_abs_max_m` ≤ z_src_max (32 kpc in the C4T block);
  - `readout_caps` {row_ids, row_contract_sha256, R_m, tau_km_s as in the contract, speed_abs_max_km_s}.
- **Cap review**, per point (scope check L421), with the fields listed in 2.2.
- **Speed policy.** Set it in this LO coverage object, not in custody. The custody row contract carries `speed_reference_policy: PENDING_REVIEWED_LO_COVERAGE_OBJECT` inside `row_contract_sha256` (custody L124-128, L139). Editing custody would change every proof's custody_sha256. (TESTED)

---

## 3. The 31 points (keys TESTED: my own recompute from spec bytes with the core L34-38/L233-238 recipe)

- All 31 specs share one numerics-minus-slots digest, `0f004670c902…`. The C4T FILLED spec (`de6d7d77`) has the same digest and gives the anchor key. (TESTED)
- Specs 1–28 are `step4_launch_readiness_c4/dryplans/specs_v001/specs/*.json`. Specs 29–31 are the engine's synthetic wave plan, `calib_tail_readiness_cx2/v006r7/dryplans_v001/P128_MS128_jacobian_0{0,1,2}.json` (mode `SYNTHETIC_ENGINE_WAVE_PLAN`, STATIC_DRY_RESULTS `947b78dc`).
- Their keys equal an independent re-derivation from coordinates `50e7288e` (u0 + 0.05 e_j; engine v003b `6ec8b2d0` L1183-1220).
- The seed key equals the one Claude4's mapper probe recorded (`4cfc6283`). (TESTED)
- Corner code cXYZ gives (s, γ/Eref, ℓ_F) at lower (0) or upper (1):
  - s ∈ {0.050771, 0.20308};
  - γ/Eref ∈ {2.0085e-17, 2.0085e-15};
  - ℓ_F ∈ {4.9525e19, 1.9810e20} m.
  - Trial values (anchor, seed, distance points) are 0.10154, 2.0085e-16 and 9.905e19 m.
- Q∞ = c⁴/(16πG·s·γ), as at lo_core L478.

| # | point key (full) | point(s) | calls | D Mpc | Q∞ | spec sha (8) |
|---|---|---|---|---|---|---|
| 1 | `8ad6ca4e867854dad71f56a97fda66f7d7b295473092a0bec84a4aca968635f8` | TAIL_REANCHOR, WORKERS_8_CANDIDATE_ANCHOR, HEADLINE_TRIAL | HEADLINE11 #0-#2 | 4.04 | 8.062 | 5fc6f0bd |
| 2 | `64dc775b80425f8a890e4b23aa985922b19bfe9512456ebf51b0207b4e2eba80` | HEADLINE_CORNER_000 (GQ record a785ccca exists) | HEADLINE11 #3 | 4.04 | 161.2 | f3c72d95 |
| 3 | `4890508b11bcbd7af814748552125e6b963cd238cf3783b15160b2c5a8c1ba5b` | HEADLINE_CORNER_001 | HEADLINE11 #4 | 4.04 | 161.2 | 850c8e22 |
| 4 | `cf78cc9a812ec13578dec8f2af7f9bc50d275965029176672661547b9c415f43` | HEADLINE_CORNER_010 | HEADLINE11 #5 | 4.04 | 1.612 | 77c54de5 |
| 5 | `b6de7aa886bb243c13cfc55aa64ce49b80180eaf5992ebcb229e3c84ee2609d4` | HEADLINE_CORNER_011 | HEADLINE11 #6 | 4.04 | 1.612 | 4c8bb2bc |
| 6 | `1f0f44c1bcdb42ebc9a928a983c7121f456e18ce09efc57fb2848ff5f1d4655e` | HEADLINE_CORNER_100 | HEADLINE11 #7 | 4.04 | 40.31 | 28011f30 |
| 7 | `662d198de1dfd5f09e1c4ce3f503a836dd53f2abf493ba59af54f7a06203c2d3` | HEADLINE_CORNER_101 | HEADLINE11 #8 | 4.04 | 40.31 | 478ae40f |
| 8 | `caec85f43de6f021c36e96d08aae9263156f1f9f13a689effe14a82df0a545dd` | HEADLINE_CORNER_110 | HEADLINE11 #9 | 4.04 | 0.4031 | ef8b7d4c |
| 9 | `6b98a3645842963857902644850e4851da5d55408828c1b20e4dcb438fde37d5` | HEADLINE_CORNER_111 | HEADLINE11 #10 | 4.04 | 0.4031 | 36e0ffdb |
| 10 | `54c432f396692faf536b9404c9e3d5d4db43faa8aaeea415c67c4bc28a85ab9e` | SENS_CORNER_C000_DLO | SENS_LO9 #0 | 3.98107 | 161.2 | 9202dbd7 |
| 11 | `4becefe561f0cb909b532547e0a817f3b3b167a72c88e3e2ad298ab349685d52` | SENS_CORNER_C001_DLO | SENS_LO9 #1 | 3.98107 | 161.2 | e5600f4b |
| 12 | `31fff1d0ce2cf95282a576f1e7cb9af2b01d37ce565088769656597ee7212b08` | SENS_CORNER_C010_DLO | SENS_LO9 #2 | 3.98107 | 1.612 | 5f6f5d00 |
| 13 | `97b390858255b548c4581b310f18a914fefb0141c58a57954bb0ca7ad76d69c2` | SENS_CORNER_C011_DLO | SENS_LO9 #3 | 3.98107 | 1.612 | a17dce28 |
| 14 | `2984a4188b131d794e281cfd193339bfd2d6710e09dcbd7bb06dc40cff0a2657` | SENS_CORNER_C100_DLO | SENS_LO9 #4 | 3.98107 | 40.31 | a8115a44 |
| 15 | `27f18eeb43b2e37233035cea1185bb4f0c49335b188eb80a267e5ff009623cb5` | SENS_CORNER_C101_DLO | SENS_LO9 #5 | 3.98107 | 40.31 | 36c04ad0 |
| 16 | `2097d210588c4d78f0a5fbac1675d8f48778a53c9798e55f278f84ea0568e762` | SENS_CORNER_C110_DLO | SENS_LO9 #6 | 3.98107 | 0.4031 | 6b7f30f1 |
| 17 | `39a63954cc81c01c0d9a14c085df3eff58c1bb8ce8c57771077e35dd7d01d035` | SENS_CORNER_C111_DLO | SENS_LO9 #7 | 3.98107 | 0.4031 | 338184cb |
| 18 | `1c1f3d896912930687b79e48f0e13576ed912cfaf87a2c64dceff7c81fae2de3` | SENS_CORNER_C000_DHI | SENS_HI9 #0 | 4.1115 | 161.2 | aefd2f8d |
| 19 | `abba6ef95f58a7c7d57655ca07e3c497ff9d550fcb33f15824909152fe004b04` | SENS_CORNER_C001_DHI | SENS_HI9 #1 | 4.1115 | 161.2 | fc4d321f |
| 20 | `1b19d71d11118cc23903b8ee8b6fdc3ffd2fbc3373eb17a08797a73e76ae3149` | SENS_CORNER_C010_DHI | SENS_HI9 #2 | 4.1115 | 1.612 | e06b845f |
| 21 | `a8a7f0b703a22d4965f2c8fe22d6a46eb53c4b488ec55604bd3cd322766b0260` | SENS_CORNER_C011_DHI | SENS_HI9 #3 | 4.1115 | 1.612 | e6a3e5ea |
| 22 | `24283deb79ee0c31501ba7a2d5e9f17f38a67b7c837f217347bfd1eb3c3686b0` | SENS_CORNER_C100_DHI | SENS_HI9 #4 | 4.1115 | 40.31 | 4ae5c8c7 |
| 23 | `b04418e4e2b21900e3bfa9286224c2d7da56348f74d036d27f958ae8af5820c6` | SENS_CORNER_C101_DHI | SENS_HI9 #5 | 4.1115 | 40.31 | 97545b83 |
| 24 | `ad55e0fb26f9e7b184efb4b0f8e9e5cca5a1f017e25b4286ef99d7dfeda58b0a` | SENS_CORNER_C110_DHI | SENS_HI9 #6 | 4.1115 | 0.4031 | 348928f2 |
| 25 | `79e77b5302f28ecc09a8bbc2084a0f47a47b953c032abcd365b17848a1a10426` | SENS_CORNER_C111_DHI | SENS_HI9 #7 | 4.1115 | 0.4031 | 1b3fde18 |
| 26 | `a863b917b5775584afed12985b5f1c0e81d1376238835ff3719417f7b2f189ab` | SENS_DISTANCE_LOWER | SENS_LO9 #8 | 3.98107 | 8.062 | e020397c |
| 27 | `cb8ca22bffc51d4ea6713f028f2a1ed816210c3d3b631161b5d83c3d055cfcc2` | SENS_DISTANCE_UPPER | SENS_HI9 #8 | 4.1115 | 8.062 | 49bce3b5 |
| 28 | `6944e210d071c17b502fd5188ea8967503dbf9bb1d5530b67d0b151da02b13cd` | CAMPAIGN_W1_SEED (about 1e-15 off the anchor; R-D10) | campaign wave 1 | 4.04 | 8.062 | 3958aed3 |
| 29 | `39a36ac345a431922b6b64a3dafbdc2202ad2d5dbcd07439bf9aee73ea870f71` | Jacobian +s (u = seed + 0.05 e_s) | campaign wave 2 | 4.04 | 7.522 | 7488b3c7 |
| 30 | `2a17398ba37976a713e2631272d4578de679af4fd49d07fa80651c2345aa7e39` | Jacobian +γ/Eref | campaign wave 2 | 4.04 | 6.404 | 5b51529a |
| 31 | `a1b7660c2ebc9540b17d76972f91ea683dc0f21e4ecf3ac58e9755405ad0a90c` | Jacobian +ℓ_F | campaign wave 2 | 4.04 | 8.062 | e93e2022 |

**Notes on the table.**
- **Coverage.** The 33 direct calls (SPEC_HANDOFF_C4V003 `9c4fcb2b`) are 29 tail-ON calls with 27 distinct keys, plus 4 tail-OFF DIII calls that need `tail_off_policy`, not a registry entry. With the seed that makes 28; with the 3 Jacobian points it makes 31. (TESTED)
- **Jacobian points (FORMAL).** They are used only if the seed call is VALID and the engine evaluates each +side at the full step (engine L1183-1220).
- **Wave 3.** In the synthetic fixture (`8d19fecc`), wave 3 is a 6-call "march" wave at u0 ± 0.1 e_j, not the −side points. So without R-C8 the campaign still stops at wave 3. (TESTED fixture; FORMAL for real runs)
- **LO risk ranking by Q∞ (FORMAL, fixed-source reasoning).**
  - Q∞ 161.2: rows 2, 3, 10, 11, 18, 19; the replay is already above 0.005.
  - Q∞ 40.3: rows 6, 7, 14, 15, 22, 23; roughly 5× the anchor.
  - All others are at or below the anchor's Q∞.

---

## 4. Tooling: build vs reuse

**Reuse unchanged (pinned):**
- custody_cx2v002 `6810b7c3`: the C1 custody_deriver.
- point_response_producer_cx2v002 `a1dcdea8`: `point_context`, `produce_eps`, `produce_rho`.
- point_response_admission_adapter_cx2v003 `4de70486`: `adapt_eps`, the EPS proof producer.
- gq_producer_cx2v005 `2832ceb9`: the GQ proof producer.
- lo_core_r5_cx2v001 `12d36305`: `produce_conditional_lo`, `validate_caps`, `enforce_caps`.
- certificate_guard_cx2v003 `5f1e49e6`: `verify_bundle`, used for an offline self-check of each bundle.
- consumed_states_cx2v010 `e48cca3c`: the C1 state_enumerator pin, and the base for the enforcement module.
- The core's `point_identity`, transcribed, for key checks.
- The existing GQ record `a785ccca`, if root approves the producer.

**Build (Claude3; reviewed by Codex1 under A115):**
1. The LO prelaunch facade successor (section 2.3a).
2. The LO_ENVELOPE adapter (2.3b).
3. **The CP-1 runner.** For each point:
   - load the pinned spec and verify its key against section 3;
   - compute the context once;
   - run GQ, then EPS, then wait for the EPS review, then run `adapt_eps`;
   - then (needs caps and cap review) run LO, wait for the LO review, run the LO adapter, and write the manifest.
   - Other requirements:
     - write every file by exclusive create in its own folder (the producer CLIs cannot write there; custody L146-151);
     - import producers by their canonical absolute paths (R4);
     - record seconds and peak RSS for each stage;
     - refuse smoke settings;
     - pass a memory gate before each point (section 5);
     - run EPS shells sequentially within a point, and parallelize only across points (adapter L66-70).
4. **The registry assembler and verifier.**
   - It writes one registry carrying a schema, a generator pin and the 31 entries, plus a manifest of every pin.
   - It replicates wrapper L86-90 and L145-161 offline, and runs the guard's `verify_bundle(phase='prelaunch')` with the derived custody and the approved list.
5. **Review-record templates** (EPS review, cap review, LO review) and a reviewer checklist. The reviewer writes and signs the records; the tool never approves its own output.
6. **Synthetic self-tests with MUST_FAIL cases:**
   - missing or non-distinct cap review;
   - an envelope above threshold stays BLOCKED;
   - smoke or partial shells;
   - custody or point mismatch;
   - slot binding not equal to the proof's `driver_certificate`;
   - unapproved producer;
   - a `uvt_` path component;
   - a file over 8 MiB.
7. **The CP-1 run sheet** for root.

**Not in S4-R-C1; these are dependencies:**
- the cap values (root);
- the enforcement module and its operator (root to assign; CP-2 class);
- the per-state LO adapter (R-B5);
- the guard fix for R1 (Codex1 and root);
- C1 and the policy review (root, R-A1).

---

## 5. CP-1 compute and timing (UNTESTED unless marked)

| Stage per point | Basis | Estimate |
|---|---|---|
| GQ | One record: 37.13 s (a785ccca; TESTED) | ~0.6 min |
| EPS: 178 shells + 14 audits | V007 EPS tool at the anchor (EPS_SAMPLES_V005 `b1651296`): the 178 shells in [4,182) sum to 955.3 s (mean 5.37 s); audits ≤ (2417.4 − 1997.5)/18 = 23.3 s each (arithmetic TESTED) | ~1,280 s ≈ 21 min (UNTESTED: different producer, point and QoS) |
| LO envelope B1 | 20,736 × 51,200 nodes. N⊥ from the GQ record (TESTED); N_z = 128/0.02 × 8 (FORMAL, consistent with 102,400 at K256). K256 B1 diagnostic: 891.3 s for two quadratures at ~4× the nodes (`573e51f5`) | ~1–4 min |
| ρ: 9 shells | One 1,036,800-solve grid plus refinement per shell | ~0.5–1 min |
| Contexts and adapters | `point_context` recomputed per producer call unless shared; never timed | ~1–2 min |
| **Per point** | | **~25–30 min at the V007 tool's speed; ~40–90 min at background QoS** |

**Background QoS.** It confines CP-1 to the 12 perflevel1 (efficiency) cores (A85 L1270, L1276). The slowdown factor of 1.5–3× is FORMAL.

**Totals.**
- CPU time for 31 points: ~13–15.5 h at normal QoS, ~20–46 h at background QoS.
- Wall time with k concurrent single-thread processes, sharing the E-cores with SR_K and other lane work: k = 4 gives ~5–12 h; k = 6 gives ~3.5–8 h.
- Memory per process: about 0.3–1 GB (FORMAL). The EPS audit arrays are 2 × 128 MB, and the box replay peaked below 100 MB.

**Phase split.**
- GQ and EPS (~90% of compute) need no caps, so they can start as soon as the runner is reviewed.
- LO (~10%) waits for the caps, the cap reviews and the enforcement ruling.
- Bundles finalize only after each point's EPS review (adapter L182-188).
- About 62–93 distinct-lane review records are needed (31 EPS + 31 cap + 31 LO if adopted). That review time is unestimated.

**Window.** Step 2 R2 started at 07:31Z (A127) and is projected at 10–16 h (A89, UNTESTED). So window (b) ends around 17:30–23:30Z (FORMAL). EPS should start early.

**First bundle (A122): use the anchor key 8ad6ca4e.**
- It cross-checks EPS against EPS_CERT_V006 on overlapping shells.
- It measures the envelope's inflation over LO_CERT_V004.
- Run HEADLINE_CORNER_000 second, since it has the worst Q∞ and an existing GQ record.
- If the envelope fails at the anchor, stop and get a root ruling before spending around 30 × 25+ min.

**Memory gate.** Use the launcher's own metric, `memory_pressure` free %, not ps-RSS sums (A127). Start a point only if free memory is at least 25% plus the CP-1 peak plus a margin. Pause while a T-case waits for admission (A72 L780; A122 L240).

**Optional saving (needs a root ruling and a reviewed adapter; not assumed).**
- EPS is analytically invariant in s and D at fixed (γ/Eref, ℓ_F) (analysis L8, L12, L16). So the 31 points span only 7–8 symbol pairs.
- `adapt_eps` scopes each record to one point, so sharing results needs a new adapter plus a check that results are bitwise invariant. (FORMAL)

---

## 6. Open questions only root can answer (with recommendations)

1. **Caps: the values and their physical basis.** Per-column TV mass caps per component across every route-A and route-B stage roster, the stars multiplier cap, the gas z cap and the row-speed caps.
   - 0528 item 2 says the build enforces them and a distinct lane reviews them. The build index names "Claude2 + distinct scientific reviewer" (`6bc25482` remaining[1]).
   - *Recommendation:* derive the caps by a rule from each point's geometry (column masses × the roster's maximum component multiplicity, using TV for signed offsets), and freeze them before any LO number is seen.
2. **Enforcement point (decisive).**
   - Define `reject_before_consume` as rejection after the run and before acceptance, over the enumerated consumed states.
   - Assign the module's builder and its operator. R-B5 has no operator.
   - Without the module pin, prelaunch LO stays UNAVAILABLE by code and by 0528.
3. **Direct calls.** Do the 29 tail-ON direct calls get a post-run cap and LO acceptance before their outputs are read (H3 capability, SENS)?
   - If not, their only LO evidence is an envelope whose condition is never enforced. *Recommendation:* yes, at least the enforcement check.
4. **The |v_i| speed policy** (custody L126) and the uncertainty carrier (L127). Set them in the cap contract, not in custody.
5. **The LO route if the envelope fails.** What is the route if the envelope fails at the anchor? How are the six Q∞≈161 points read if they fail?
   - The options are: per-state acceptance as the LO route, which needs a policy or wrapper ruling because r9 requires `covers_all_consumed_states` at prelaunch; a tighter, reviewed envelope core; or the NON_LAPSE_TAIL_MATERIAL design successor.
   - Never cap tuning.
6. **The anchor key's slots.** Per-point cx2 records (*recommended*: uniform and compatible with `adapt_eps`), or the V007 values EPS_CERT_V006 `598c8fa3` and LO_CERT_V004 `1c384f76`?
   - The V007 values would need adapters that wrap V007 certificates. `adapt_eps` refuses them on schema and producer (L172, L181), and F03 allows "at most" 3 V007 slots (`7d0cdb28` L82-98).
7. **R1 remedy.** Rule that the fix lies in a guard successor, with no custody change, before CP-1 builds bundles.
8. **Who signs the per-point reviews?** That is 31 EPS, 31 cap and, if adopted, 31 LO reviews. Codex1 is A122's tooling reviewer. May one policy-level review be instantiated per point by a tool?
9. **C1 content.** The approved-producer pins and the `certificate_policy_review` (section 1.5). Freeze the registry before HEADLINE11, and never edit it afterwards (R-C1 `97a762e1` L211).
10. **Physics note.** The per-point EPS has no magnitude gate. Sampled |1−q| reaches 0.0125 at corner_00 on [4,5] (box report L9), against about 6.4e-4 at the anchor.
    - The RB-FP remainder that uses ε_max (design V002 L242-251) was evaluated only at V007's anchor. Does step 4 need a per-point remainder bound?

---

## 7. Risks under A115 (honest path only)

**R1: guard007 refuses every registered tail-ON point at PRELAUNCH.** Blocking for the launch path, not for CP-1 compute.
- Inside guard007's fence, the custody deriver opens `driver_r5/cascade/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py` (pinned `1e27430c`, driver L326). guard007, v008 and v009 refuse it with `PROTECTED_PATH_REFUSED`.
- **Chain:**
  1. guard007 L190 → L210 calls `certificate_check`;
  2. the wrapper L92-93 calls `derive_custody`;
  3. custody L129 calls `uvt_static_pins`;
  4. the driver L1215-1222 runs `verify_pin`, which opens the file at L525;
  5. guard007 `_audit` L114-117 runs `safe_path`;
  6. `lexical_path` L29 refuses the `uvt_` prefix.
- **Labels.** The predicate is TESTED: transcribed and evaluated on the path string, it flags `uvt_route_b_binding_c2v001_r5.py`. The end-to-end refusal is FORMAL: never executed.
- Claude4's probe stopped at the registry lookup, and its record shows `uvt_component_opens: []` (`4cfc6283`).
- A custody-side fix would change every custody_sha256, so this must be decided before CP-1.

**R2: physics (FORMAL).** The conditional envelope may fail broadly, and likely fails at the Q∞-161 points. Preserve the readings. An envelope failure is not NON_LAPSE_TAIL_MATERIAL, and the caps must not be re-tuned after results.

**R3 (TESTED).** `adapt_eps` binds the eps slot to the cx2v002 record. So the anchor key cannot carry V007's EPS slot through existing tools (question 6).

**R4 (TESTED).**
- The producer CLIs write only inside Codex2's folder. CP-1 therefore needs its own runner and writer.
- Proof `producer` pins are unresolved path strings, and the wrapper matches them as whole dicts (custody L48-49; wrapper L158). A runner that imports producers through another path produces proofs the wrapper refuses.

**R5 (TESTED).** EPS starts depend on the previous shell (producer L300; adapter L66-70). Parallel-by-shell output would be refused, so parallelize across points only.

**R6 (TESTED).** The cap review binds `producer_sha256 = sha(lo_core)` (L424). Any edit to lo_core voids every cap review.

**R7 (FORMAL).** Slot pins enter the spec, config and cache bytes (library L114-129; wrapper L52-55). Re-issuing any record after HEADLINE11 starts invalidates that work.

**R8 (FORMAL).** The bundles are spent if V007 is not ADOPT_TAIL, or if the coordinate spec `50e7288e` changes; the latter affects the seed and Jacobian points (R-C1 disposition; R-D12).

**R9 (FORMAL).** E-core and memory contention with step 2. A CP-1 process must never take free memory below 25% while a T-case waits (A72, A122, A127 metric).

**R10 (TESTED, NOTE).** Successor folders and file names must avoid components starting with `uvt_` and components containing `ngc3198` (guard L42; guard007 L29).

---

## Pins (full sha256, from bytes)

- wrapper r9 `claude_artifacts/calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py` 24abe3bc4f6ee0e3c5d7c89502062cf99464573b35bc5b53c33c14ef2ae888af
- core r9 `…/v006r9/calibration_core_cx2v006r9.py` a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605
- wrapper r10_c4 `…/v006r10_c4/calibration_orchestrator_cx2v006r10_c4.py` ef3d3d69e01999dcfa255a75c98bcdee31a9512f0e284053139ea190ef9445c3
- core r10_c4 `…/v006r10_c4/calibration_core_cx2v006r10_c4.py` dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6
- config r9 `…/v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json` 721c7230f3f3efde6f8406f13a52995ae321248829ab1ee64a2f522ad5582b8e
- guard `…/certificates_per_point/certificate_guard_cx2v003.py` 5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f
- custody `…/certificates_per_point/custody_cx2v002.py` 6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377
- EPS/rho producer `…/certificates_per_point/point_response_producer_cx2v002.py` a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231
- EPS adapter `…/certificates_per_point/point_response_admission_adapter_cx2v003.py` 4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372
- GQ producer `…/certificates_per_point/gq_producer_cx2v005.py` 2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd
- GQ record `…/certificates_per_point/GQ_P128_MS128_C000_R5_CX2V001.json` a785ccca92349515356fdd565848ef6bd7bc1bb31b792defb85b1a843f963a7f
- LO facade v004 `…/certificates_per_point/lo_producer_cx2v004.py` 5db60d0f6db6d481e2f748b19bef08ce425f19a0e463d58727c184d633e03d51
- LO config `…/certificates_per_point/lo_config_r5_cx2v001.py` 6654d93c0241afd230d90bfcf327f16c22dd24c4da1d3eea72602212c2b6ae5a
- LO core `…/certificates_per_point/lo_core_r5_cx2v001.py` 12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e
- state enumerator `…/certificates_per_point/consumed_states_cx2v010.py` e48cca3c35a3d6d3724f74b9407b91f006bd31f2f30f416f9c328ba9e4144ca2
- guard007 `claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v007.py` 42bf0ce9dcd48f734299ace4f07cb92a15563e57a39f5ae40be451e481d1c3de
- guard v009 `…/impl/step4_guard_cx1v009.py` 5986c4c51468d2b1455df9d18b40a501823aa2a53d6e466a0aa4329d972ba6c3
- direct preflight adapter `…/impl/step4_direct_preflight_cx1v001.py` eee61ac61ff93a11c97b9fdd3d6340661f17a92394653e524ac1cd8648d20fd1
- driver r5 `claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6
- tail library `…/driver_r5/module/owned_uv_tail_lapse_v002.py` 2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54
- r5 route-B binding (R1) `…/driver_r5/cascade/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py` 1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329
- LO certificate of record `…/tail_scheme_impl_c2/certificates_v004/gates/LO_CERT_V004_MS128.json` 1c384f763e663d85414f25ef8c02b4291efd88b63353a77961f2e88aca2e204a
- V007 EPS slot `…/certificates_v002/gates/EPS_CERT_V006.json` 598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192
- EPS timing basis `…/certificates_v002/out/EPS_SAMPLES_V005.json` b16512967f313bdf25bd7598ca84bcddd7fd0557c6bd5295579f202356033c0c
- B1 timing basis `…/certificates_v002/out/LO_B1_MS128_V001.json` 573e51f55866037d08c84cf71b7bb76945791704bc88d72fde5803bc53924b9e
- C4T FILLED spec `claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_R5_CX1V004.FILLED.json` de6d7d77d053d9c983f15eca11468fe8520d025ff2ad1f643b2a517a915b1738
- spec handoff `claude_artifacts/step4_launch_readiness_c4/handoff/SPEC_HANDOFF_C4V003.json` 9c4fcb2b1af09ad3f6fbc391e75c7a7006f0359132e7025a9536c06a36a19e7e
- registry probe `…/launch_order/work/registry_probe_v002/REGISTRY_GROWTH_PROBE_C4V002.json` 4cfc628366c0931bc63dd94f171772e602adb384c6d253440b3f29dc3a74c353
- wave fixture `claude_artifacts/calib_tail_readiness_cx2/WAVE_FIXTURE_V001.json` 8d19fecccaea24a4b1c3fa90cef6507317d7fd015e5a3b86d7587a5f3852f4ac
- coordinates `…/calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json` 50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f
- engine `claude_artifacts/calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py` 6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3
- box replay report `…/certificate_analysis/BOX_REPLAY_REPORT_CX2V002.md` 3ff6070b525f7461e88055f3d1935de4b8738ed81a3f2f4989874471c60a5fe9
- certificate analysis `…/certificate_analysis/CERTIFICATE_ANALYSIS_CX2V001.md` 4084bd597d978f58dd4d86d0943839480245a2c350e2a005e6a30d9f9ebeedc7
- per-point requirements `…/certificate_analysis/PER_POINT_REQUIREMENTS_CX2V001.json` 8f690fc91cdd21eff92be599471d0629af3ef66968614af0ebcd4a7e768fc567
- tail design V002 `claude_artifacts/tail_scheme_design_c2/v002/TAIL_SCHEME_DESIGN_V002.md` cdb16d1c42da39cf8eabe253b7192f4f391d19adfdd026e57a6971837a6aa944
- Claude4 review `claude_artifacts/review_certs_per_point_c4/REVIEW_CERTS_PER_POINT_C4V001.md` bc211c3ad9329e12bde2c099f28dbc4ea154f36ba47aac0fe217e9ecc11a03c6
- build index `…/certificates_per_point/CERTIFICATE_BUILD_INDEX_CX2V001.json` 6bc2548240210124db654b81100b9cdac95ba005ba52bfdada43e2e2a41652be
- refute F03 `claude_artifacts/step4_launch_readiness_c4/refute/REFUTE_C4V001.md` 7d0cdb284e917b3fd0243df65047f5d9f214f82fed534064324a96f516ec1f15
- ROOT_ITEMS_STEP45_V002 `claude_artifacts/root_items_step45_c4/ROOT_ITEMS_STEP45_V002.md` 417de6fef408082695e4e3f68530351a0b71a7c1415d784a29199a8a9ec42ee8 (S4-R-C1 at L623-637; rows L550, L552, L559, L569)
- ROOT_ITEMS_FINAL_C4V004 `…/launch_order/ROOT_ITEMS_FINAL_C4V004.md` 97a762e1cf2c7eb76e7f77b4c708cfc5452dd5b72452b2bf86ffc9e369e6b704 (R-C1 L207-213, R-C8 L263-269, R-D10 L345-351). C4V005 `f783f427` carries the same R-C1/R-C8/R-D10 text.
- readiness index V002 `…/step4_launch_readiness_c4/INDEX_STEP4_READINESS_C4V002.md` e58603a1457e97da74ddf0b500e143db5e8cfe198a38aa28e4c657381890fc9d (section 5 L95-160; section 6 L162-171)
- dispatch 0666 `FROM_CODEX/0666_2026-10-19_A122_step4_start_blockers_builders.md` bd3a1d80b9018533f91443140d331a6e17d20dea373c3f18905b1db4aca32319
- ruling 0528 `FROM_CODEX/0528_2026-10-18_codex2_rulings_P0_normalization_and_certificate_admission.md` d11654e5a2ab24944a861372769e75e0a2bbac035feecdf4a54286e3841aae83
- V005 addendum (closed) `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md` c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1 (A72 L753-787, A85 L1266-1282, A95 L1105-1109, A103 L943-953)
- V006 addendum (open; read at 07:37Z) `…/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` 78f04f7f53f3188a6f9f2650daa786e47100c2d6d857aa38b59d72997aae890f (A115 L141-156, A122 L237-251, A125 L293-322, A126 L324-328, A127 L330-362, A128 L364-385)

## Scratch written (my role folder only)

- /private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/71ea3fb2-2be2-4b38-b919-d6ca63cf052f/scratchpad/s4rc1/synth/keys_synth.py
- /private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/71ea3fb2-2be2-4b38-b919-d6ca63cf052f/scratchpad/s4rc1/synth/table_synth.py
- /private/tmp/claude-501/-Users-bgm-Research-UNT-EXCHANGE/71ea3fb2-2be2-4b38-b919-d6ca63cf052f/scratchpad/s4rc1/synth/table_md.py