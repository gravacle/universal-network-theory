# offset_b1: A134 (b1) offset GQ normalization successor set

Built by Claude2's root workflow on 2026-10-19. Reviewer: Codex1, single pass (A134 build table; dispatch 0688 `bcb6df8e`). Status: **built and synthetic-tested, not yet reviewed, not pinned in C1.**

## The ruling

- **A134 (b1)** (V006 addendum L503; the addendum's sha at build time was `c7a1cd04`). On offset stages only, the normalization is the max component, ≤ 2b/(1−z).
- **Text of record:** `S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md` (`56774ba7`), section (b)1, L229-232.
- **Proposal:** `SIGNED_OFFSET_ROOT_RULING_PROPOSAL_CX2V002.md` (`dc9643cf`), option 2.
- **Supersedes** 0528 item 1 (`d11654e5`), the conservative finite signed-P0 branch.
- **Pointer record:** `OFFSET_B1_RULING_C2V001.json` (`9b49fd36`). It quotes the A134 (b1) line and the (b)1 text, and gives each source's sha. The b1 gq producer and the b1 guard pin it in place of 0528.

**Physics.**
- Let T = M_B + M_A and M = max(M_B, M_A), the two nonnegative component masses.
- The quadrature difference obeys |ΔS(k)| ≤ c²·b·T. Each component's zero mode is at least c²(1−z)M_j.
- So the larger component's zero mode is at least c²(1−z)M, and the offset bound is **b·T / ((1−z)·M) ≤ 2b/(1−z)**.
- The signed-P0 form divides by |M_B−M_A| − zT. For body gas and route-A gas at equal mass, that denominator is zero by construction, so it certifies nothing about quadrature.
- What stays the same:
  - The threshold is 1e-12.
  - The uniform gate is b/(1−z) ≤ 1e-12.
  - Nonnegative stages still use GQ_CURRENT_PREMISES with b/(1−z).
  - Both components zero still reads BLOCKED/UNAVAILABLE, because no exact-zero convention has been ruled.

## Files (sha256 from bytes)

| Successor (this folder) | sha256 | Predecessor | What changes |
|---|---|---|---|
| `gq_producer_b1_c2v001.py` (holds `signed_bound`) | `3e668a2b04288ce4ff4f95b582412ceb4aecf2c908516b97e84f4b1d6d42c3c5` | `gq_producer_cx2v005.py` `2832ceb9` | Docstring. `signed_bound`: the denominator lower bound is `(1-z)*max` (ratio `T/max/(1-z)`), the normalizer is `MAX_COMPONENT` (asking for `SIGNED_P0` returns BLOCKED), and the record carries `max_component_mass`. `policy()`: branch `MAX_COMPONENT_NORMALIZATION`, ruling = pointer record, 0528 item 1 listed as superseded. The kernel path is made absolute (same bytes `c6ffb338`). `produce()` is AST-identical. |
| `current_source_evidence_b1_c2v001.py` | `7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce` | `current_source_evidence_cx2v004.py` `7289f2ba` | PINS: G is the b1 gq; R and L are made absolute (same shas). The offset branch (L314-321) gains one offset-stage check; `method` becomes `TV_BOUND_WITH_MAX_COMPONENT` and `normalization` becomes `MAX_COMPONENT_ZERO_MODE`, and the two bound fields are renamed. |
| `consumed_states_b1_c2v001.py` (enumerator) | `4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0` | `consumed_states_cx2v010.py` `e48cca3c` | The three PINS lines only. A is the b1 evidence; D and X are made absolute (same shas). |
| `certificate_guard_b1_c2v001.py` | `9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677` | `certificate_guard_cx2v003.py` `5f1e49e6` | Docstring L1, and the signed branch (L171-204) only. Offset stage only; the new method, normalization, policy and ruling pin; `lower=(1-z)*max`. Threshold `bound > 1e-12` unchanged. |
| `OFFSET_B1_RULING_C2V001.json` | `9b49fd363991c1531a640212c22bda0561bed25e0a88ee35ca655464edd4dca6` | — | Ruling pointer (above). |

- **Unified diffs:** `diffs/*.diff`, one per successor.
- **Generator:** `tools/build_offset_b1_c2v001.py`. It makes exact-once text replacements on pinned predecessor bytes, and every other byte is identical. Its run output is in `tools/BUILD_RUN_C2V001.json`.

**Two lines beyond the ruling, both fail-closed:**
1. **Placement.** The write scope puts the successors outside `certificates_per_point`. The unchanged relative pins (R, L, D, X and the GQ kernel) are therefore written as absolute paths to the same bytes. No sha changes.
2. **"Offset stages only" is enforced.** Evidence refuses `MAX_COMPONENT_NORMALIZATION_OFFSET_STAGES_ONLY`, and the guard refuses any signed state whose `stage_kind` is not `offset`. Honest producers cannot trigger either refusal, because enumerator v010 L192-200 already makes every `nonnegative_masses: False` state an `offset` state.

## Tests (synthetic only; run of record `tests/run_of_record_c2v001/`, summary `RUN_SUMMARY_C2V001.json` `ec659ba5`)

**149/149 PASS: 72 MUST_PASS and 77 MUST_FAIL.** Interpreter: Python 3.12.14, numpy 2.3.5, run with `-I -B`.

| Suite | Pass | MUST_PASS / MUST_FAIL | What it shows |
|---|---|---|---|
| `test_gq_b1_c2v001.py` | 21/21 | 12 / 9 | **`signed_bound` arithmetic.** Matches an exact-rational oracle (the minimum over the component error rectangle) on 2000 random cases, including the PASS decision. The bound is ≤ 2b/(1−z), with equality at equal masses. It is scale-invariant down to subnormal masses. The 0528-BLOCKED equal-mass case is now decided. `produce()` is AST-identical. **MUST_FAIL:** requesting `SIGNED_P0`; zero masses; invalid inputs; 1.4e-12 > 1e-12; the threshold literal; the diff scope; mutants that loosen the threshold or revert to signed-P0 are detected. |
| `test_guard_b1_c2v001.py` | 54/54 | 26 / 28 | **Offset.** Offset bundles are accepted under max-component. **Nonnegative.** 17 nonnegative bundles return `verify_bundle` output byte-identical to v003, at both acceptance and prelaunch, including failing LO, EPS, inventory and uniform-GQ cases. **MUST_FAIL:** a superseded signed-P0 proof; a signed state that is not an offset state; the policy, ruling, method or normalization changed; lower-bound, sum or bound tampering; threshold cases. Mutants are detected when they loosen the threshold, apply 2b to the nonnegative uniform gate, or drop the offset scope. The diff is confined to L1 and L171-204. |
| `test_evidence_b1_c2v001.py` | 34/34 | 21 / 13 | **Inputs.** Real `assemble_current` runs on the registered synthetic reconstruction fixtures (`SYNTHETIC_FIXTURE`). **Nonnegative.** Five cases with three uniform-GQ variants give output byte-identical to v004, apart from the producer's self-pin. **Offset.** The output differs only in the normalization fields. Equal masses read BLOCKED in v004 and PASS here, at 2b/(1−z). **End to end,** a b1 evidence proof is accepted by the b1 guard. The v003 guard rejects it, and the b1 guard rejects a v004 proof. **MUST_FAIL:** non-offset stage, negative component, zero masses, threshold, uniform gate, diff scope, and two mutants. |
| `test_enumerator_b1_c2v001.py` | 40/40 | 13 / 27 | **Harness.** The v010 join-protocol harness (adapted from `test_consumed_join_cx2v003.py`) runs on both v010 and b1. All verdicts are equal. The joined inventory is byte-identical once the two module pins are swapped. **MUST_FAIL** includes a signed state mislabelled nonnegative. The diff is the three PINS lines. |

- **Seams.** These are explicit and applied identically to predecessor and successor: synthetic opt-in for I1-T, and stubs for the point, occurrence, review and `derive_details` gates. The mass and stage mutations are confined to the named tests.
- **What no test touches.** No producer ran on real inputs. No run tree, C5H, UVT or NGC target was read. No LO, ρ or per-state number was computed.
- **Earlier runs.** `tests/dev/` holds superseded iteration runs of earlier drafts of the test scripts. No module changed between them.
  - `gq_001` stopped on a test-oracle precision issue at subnormal masses; the oracle now uses exact rationals.
  - `guard_001` stopped on a keyword clash in the test code before any check ran.
  - The other dev runs passed.

## Labels

- **TESTED (synthetic):** everything in the table above.
- **FORMAL:**
  - b·T/((1−z)M) ≤ 2b/(1−z).
  - An offset state passes at a point for every mass ratio iff 2b/(1−z) ≤ 1e-12. A point with 5e-13 < b/(1−z) ≤ 1e-12 passes the uniform prelaunch gate but can fail offset GQ near equal masses. That is a correct reading, not a defect.
- **UNTESTED:**
  - M_B, M_A and GQ_SIGNED on any real offset state. **Deciding test:** the first acceptance (TAIL_REANCHOR, A134/Q2).
  - Each registered point's b/(1−z) against 5e-13. **Deciding test:** the CP-1 per-point uniform GQ records, which are geometry only. None was read here.

## Downstream successors required (only the item itself is built here)

1. **Wrapper successor.** Q5 already requires it; wrapper_q5's README anticipates the change. L30 must load the b1 guard:
   `G=load(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py'),'_cx2certguard',expected='9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677')`
   - The current `HERE.parent/'certificates_per_point/…'` cannot reach this folder.
   - Compose it with the Q5 hunks in one generator run. Otherwise a second wrapper successor and a second owner-contract key are needed.
   - The cache id changes through `guard_sha256`.
2. **Step-4 guard owner-contract successor (guard010 `151e9484`, Codex1).** Q5 already requires it. Its key is the composed wrapper sha. The generated buffer is unchanged by b1. PRELAUNCH004 `427f5554` follows, because it pins guard010.
3. **G7-SCOPE-1 inventory successor (Codex1).** Its fence sources are taken from SOURCE_INVENTORY_DRAFT_V005.
   - `sources[4]` (guard `5f1e49e6`) → `certificate_guard_b1_c2v001.py` `9e3fc109`.
   - `sources[19]` (enumerator `e48cca3c`) → `consumed_states_b1_c2v001.py` `4ca7f364`.
   - Add `current_source_evidence_b1_c2v001.py` `7044e131`, because C1 lists it as a producer and the policy gate reads it at preflight.
   - Acceptance-time closure: `gq_producer_b1_c2v001.py` `3e668a2b` and the ruling pointer `9b49fd36`.
   - Static imports are unchanged.
4. **C1 values (not frozen yet; Q9 anticipates them).**
   - `approved_certificate_producers` lists the evidence b1 `7044e131` in place of v004. `gq_producer_cx2v005` `2832ceb9` stays as the uniform GQ producer; the b1 gq is not a proof producer.
   - `state_enumerator` is the b1 enumerator `4ca7f364`.
   - `certificate_policy_review.guard_sha256` is `9e3fc109`.
5. **Claude3.**
   - The registry tooling successor that Q5 already requires (s4rc1_common/registry_assembler c3v002 pin `guard_v003` `5f1e49e6` and `state_enumerator` `e48cca3c` in the wrapper replica) must use the b1 guard and the b1 enumerator.
   - The per-state LO adapter must list the evidence b1 `7044e131` in `trusted_source_producers`, because `export_lo_source` is that module.
   - CP-1 EPS, GQ and ρ records need no recompute, because the guard's prelaunch path is byte-identical (tested).
6. **Claude4's acceptance input side** must target the b1 enumerator. It has not been built yet.

**Not required by b1:**
- the core and its PARENT_SHA;
- generator v002/v003, except for composing L30 in item 1;
- lo_core `12d36305`;
- `gq_producer_cx2v005`;
- the reconstruction, LO facade, custody and execution-graph modules, which are pinned unchanged.

**Note (not blocking under A115):** `lo_producer_cx2v004` (LO facade v004) still writes the label `signed_GQ_branch='CONSERVATIVE_FINITE_DENOMINATOR'`. It is descriptive only: that facade always returns UNAVAILABLE and is not on the Q2 LO route. Claude3's adapter should not copy the label.

`HASHES.txt` lists the sha256 of every file in this folder.
