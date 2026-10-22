date -u: Sun Oct 18 14:53:27 UTC 2026

This runbook describes the root-owned production procedure required by 0545 F5. Claude2 remains the sole scientific launcher. This build performed synthetic replay/tests only; it does not authorize launches or target access.

Use the exact module and slots bytes listed below. All six declared alternatives, their full metadata and order must equal slots V003. The primary is BR_A_F10_PRIMARY. STAGE0_GRID_OUTER remains NOT_EVALUATED_BEFORE_FREEZE in the adopted slots. A finished future run does not permit a producer to flip that status: root must approve a new slots/module-pin successor before it can be admitted as evaluated. It never delays the headline and, when separately adopted, uses the already-admitted headline DDO154 calibration points with only its registered coefficient grid changed.

First pass, before any target access:

1. Under the root launch workflow, obtain and save each required member's raw forward result and immutable byte pin, separately for each evaluated alternative. Preserve failed/exception records as well. Cut records come from the corresponding v011 runs; they are never fabricated or inferred from target velocities.
2. Determine and record D1 from those member results using the registered finite-on-valid, nonempty-valid-set rule and target-free cut/INVALID metadata. Plan the resulting sensitivity theta coordinates, run them under the root workflow, and save their raw results and byte pins. The final replay must reproduce this D1 identity.
3. Gather the run-produced cut pins and gate registrations for every member and every evaluated sensitivity theta, including failed members and failed sensitivity attempts. Where a context has no cut, record that fact explicitly as null; do not guess a cut or borrow another member's cut.

Root registration, still before target access:

4. Root adopts a target-free per-alternative registration roster. Each roster binds the exact slots record, query-manifest pin, complete explicit query-ID mapping, approved gates and exact-theta cut contexts. Root supplies the external path/SHA256 pins. The complete mapping contains all six alternatives, including NOT_EVALUATED ones; each evaluated theta has exactly one matching context when PER_THETA is used. Duplicate, missing or one-ulp-different contexts refuse.
5. Pin and retain all dependent bytes: slots, query manifest, root rosters, cut/gate records, shared GL-node artifact and its sources, registered route-B config, and the stage0 grid pin. These files must remain byte-identical through scoring. Registration establishes authorization/custody; the freeze reader does not independently certify physical confinement or the scientific validity of a cut.

Second pass, still before target access:

6. Build a replay adapter indexed by alternative identity and exact theta. It returns only the saved, byte-verified raw result for that key. It must not launch a new solver, silently substitute another point or invent a successful result for a failed point.
7. Call evaluate_envelopes with the selected alternative's external root roster pin, select_reference_member for D1, and evaluate_sensitivity with the same root pin. Verify the D1 identity and sensitivity plan against pass one. If they differ, root resolves the source/registration discrepancy and creates approved successors before proceeding; existing pins are not edited.
8. Call write_freeze_manifest with the full exact alternatives declaration, all required evaluated results, raw-result provenance and the six-entry row_registration_rosters mapping. Preserve all43 member rows. Verify the manifest and registration, and log the resulting manifest byte SHA256 before any target access.

Scoring phase, only when root authorizes it:

9. Pass the frozen manifest, registration, previously logged expected manifest SHA256 and the same external root roster mapping to score_after_freeze. The scorer re-verifies bytes, identities, exact alternatives and row registrations before using target values. No roster, cut or reference may be chosen after targets are seen.
10. The primary and ordinary full-row alternatives retain their43-row denominators. Every registered null INVALID is a miss. STAGE0_GRID_OUTER, only after evaluated adoption, scores its registered OUTER subset Q36–Q43 (R>=30kpc), denominator8, separately with headline=false. Its inner rows are absent from that alternative's score calculation. Under the current slots it remains unscored NOT_EVALUATED_BEFORE_FREEZE.

Units and boundary arithmetic:

Query radii are bound by query ID through the verified manifest, independently of row-file ordering. Rad_unit must be exactly kpc. Cut/support comparisons deliberately use R_m=R_kpc*kpc_m and cut_m=cut_kpc*kpc_m to match the producer. Outer is R_m>=cut_m; gap is last_retained_GL_node_m<R_m<cut_m. Exact-cut rows are outer; exact-last-node rows remain supported. A positive floating-point multiplication can round adjacent kpc values to the same metre value, so a one-ulp-neighbour threshold can differ from direct kpc comparison. TESTED on the frozen43 radii:8 have such a neighbouring cut; direct-kpc/metre comparisons agreed at every registered GL4-node cut. The metre form is the implemented authority; producer/roster contradictions refuse rather than being rounded away.

TESTED: synthetic two-pass raw-save, root registration, replay and freeze;163/163 own regression/delta checks and238/238 adapted independent reviewer checks. The positive stage0 subset arithmetic is unit-tested; the public adopted path is the NOT_EVALUATED fallback. UNTESTED: actual scientific runs, production roster adoption/physical cut certification, evaluated-stage0 public freeze under a future approved slots successor, and real-target scoring.

Pinned implementation and authority inputs:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` — SHA256 `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` — SHA256 `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0545_2026-10-18_codex3_freeze_v003g_small_fixes.md` — SHA256 `4049a3f81b524f5622e0eda6510eeee60c7a6b10fea97ea6c648d0b9698b84a5`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0548_2026-10-18_codex3_register_stage0_grid_outer_alternative.md` — SHA256 `7bf03716c95fc9d9ae06ebb038c69b6e9ed8452f2414919b35cae20365decace`
