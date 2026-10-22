# M2_FIXTURES_0457_V001: implementation fixtures for the 0456 admission residence transport

This is helper **M2** of the Claude4 independent review lane (dispatch 0457). It is a review only. Codex1 owns the physics, launches and acceptance.

- Author files were never edited.
- The harness ran only on a byte-identical snapshot of the author module.
- Everything used a synthetic double. There was no project sampler import, no L4 or production sampling, and no use of project result arrays, raw captures or target data.
- Every run was single-threaded with tiny explicit states.
- Physical status: not_assessed. Numerical mixing efficacy is for root's measured run.

## Pinned inputs (all verified by SHA256)

| item | sha256 |
|---|---|
| Dispatch 0457 | `efdc659f32dc08f972fe0ae98c5dc11239be8fdb47fab35869f7aa06f0125f13` |
| Author contract 0456 | `4b33c8e4fa8d1928700f2754954206346143f59a60929ca27222c285cddb87ac` |
| Correction 0459: the owner is the public `("admission", ("vertex", label))` | `5c4b7d4c329222fd34322db47ee4412fc12e0df7018e7318abe1b17f89df1af2` |
| Pinned Birth transport, run as the harness control | `6f866bda7eda7b56cb9ae7a1247cb365c16c9b40cb996af650452f8823f9f6e8` |
| Sampler V004, read as text only | `7d0798923302bb36763c6b4f6212c944872b2b9c2f50021183d918a19dbd03c9` |
| Sampler V006, which re-exports the V004 functions unchanged | `896cadbbe4059a77b33f370d643cfa7657c0e031d61d1aa46886e88eb4f576b7` |
| Operator V003, read as text only | `a04f87954b68bb2dcc5a1af42a465b1d554ed1fc14d9b22d43e05e3e664f7f07` |
| Author module `admission_residence_transport_c3v001.py` | `5b19e90ee4fcf86a0b8fe570abb607ae23c8047771abc4ab317c167f1837d653` |
| Author interface `INTERFACE_0456_V001.md` | `337a7973f008b2846aa334dde8855106db14371d7cca5270a899a552cd517e58` |

The author module is the one named in FROM_CLAUDE3 message 0009 (done-0456). It was copied to `M2_snapshot_5b19e90e/`, and `cmp` confirmed the copy identical. Its hash was unchanged after the run.

## Synthetic double (`M2_sampler_double_v001.py`)

**Sampler API.** The API transcribes V004 semantics:

| function | V004 lines | semantics reproduced |
|---|---|---|
| `_Stop` / `_BudgetStop` | 862-885 | status `incomplete` for a budget stop |
| `_budget_check` | 2049 | injectable hook; every checkpoint label is logged |
| `_op` | 2101 | a budget check before and after every operator call |
| `_keys_equal` | 2125 | as V004 |
| `_enumeration_tick` | 2188 | enforces the enumeration cap |
| `_channels_from_records` | 2206 | W = \|amp\|·multiplier; a zero multiplier drops the mark; a negative multiplier is `unsupported`; a nonfinite one is `failed` |
| `_record_groups` | 2286 | exact owner formats |
| `_palette_members` / `_palette_channels` | 2331 / 2353 | group-restricted palette |
| `_segment_core` | 2650 | returns {state, key, D, r, Da, row, allk} |
| `_target_key` | 2704 | caches the key in the channel |
| `_event_from_channel` | 2711 | builds the event record |
| `_summed_rate`, `_no_self_loop`, `_reverse_check` | 2737-2791 | as V004 |
| `_check_times` / `_net_increments` | 2794 / 2807 | as V004 |
| `_unique_mark` | 3207 | a duplicate is `_Stop('failed')` |

**Operator.**
- **State.** The state is the tuple `(slots, edgeset, inc, p, q, s, dm)`, in V003 key order.
- **Primitives.** flip and hop (owner `(kind, ("edge", (a, b)))`), bind (`("bind", ("vertex", v))`), birth and birth_rev (`("birth", owner, cut_labels)`, with two cuts per owner so that N_fwd = 2 occurs), and admit and admit_rev with owner `("admission", ("vertex", label))`.
- **Admission rules** are exactly V003 L1590-1595: admit iff (p,s) = (0,0) → (1,1); admit_rev iff (1,1) → (0,0); q is kept.
- **Newborn vertices** map through `group` to their original, so the group palette contains marks at more than one vertex.

**Synthetic, deliberately not V003 physics.**
- Multipliers are endpoint-symmetric (Hermitian) functions of the admitted count A and the active-slot count S. This makes the event W ratios nontrivial.
- Zero multipliers remove marks: flip at A ≥ 2, and admission into A > 2.
- D = d_h − Σ j·reads. It has admission-dependent terms U·A(A−1)/2, e_p, e_s and sources on N_adm and N_part.
- Self-check: on all 69,632 states of the main double, the API layer equals the raw physics and every mark is Hermitian.

**Fixture-only variants:**
- ladder: N_fwd ≠ N_rev;
- `admit_rev` that resets an edge bit: not an exact inverse;
- a duplicate admission mark;
- nonfinite D or W;
- finite but overflowing D;
- `read_rows` failure;
- opaque (unindexable) state and key objects;
- a non-V003 admission owner family.

## Oracle

The oracle uses only the raw operator physics, never the API layer or the module under test.

- **Path weight:** log π(path) = −Σ_i (t_{i+1}−t_i) D(x_i) + Σ_k log W(e_k), with t_0 = 0 and t_{k+1} = β.
- **Proposal:**
  - choose a vertex with probability 1/|R|;
  - choose a mark with probability 1/N_f among the exact-owner marks at dwell 0;
  - transform every dwell, requiring the inverse mark with canonical old target;
  - require closure and reverse-roster membership, and replay every event.
- **Hastings ratio:** L = log(N_f/N_r) − Σ dt·ΔD + Σ log(W_new/W_old). It is cross-checked against log π(Y) − log π(X) + log(N_f/N_r) to within 1e-12.

## Measurement method

**Scripted RNG.** Every draw is logged. The harness checks the draw bounds: the first draw is over the full frozen roster and the second over the N_f actual marks.

**logMH** is measured two ways:
- exactly, from the diag entry when one is unambiguous;
- as a black box, by acceptance bracketing at u = e^L·(1 ∓ 1e-9).

**Exact detailed balance.**
- The space is every closed path with k ∈ {0, 2} (fixed times) on tiny doubles.
- The module kernel is built as a black box: a depth-first search over integer draws.
- Acceptance thresholds come from a bracket at 1e-10 relative or from a full 60-step log-bisection.
- The pass condition is π(X)K(X,Y) = π(Y)K(Y,X) to |Δlog| ≤ 1e-9, and K_module = K_oracle to 1e-9 relative.

**Doubles used:**

| double | states | closed paths | features |
|---|---|---|---|
| DB3 | 256 | 864 | 3 vertices, admission cap, hop, flip, bind |
| DB3 with defect | 256 | 720 | non-inverse `admit_rev` |
| DBL | 32 | 112 | ladder, N_f ≠ N_r; full bisection |
| DBB | 48 | 200 | Birth; full bisection |

**Every invocation** checks:
- deep equality of the input path (numpy-aware) and unchanged object ids;
- that the sampler namespace was not patched;
- the outcome contract.

## Admission catalogue

Categories: required = correctness or detailed-balance relevant; contract = 0456 items that do not affect DB; template = Birth-reference behaviour; info = no pass/fail.

| ID | case | category |
|---|---|---|
| A01, A02 | Zero-event `admit` / `admit_rev`: exact diagonal ratio −β·ΔD; draws; logMH by diag and bracket | required |
| A03, A04, A24 | Forward then reverse (forced acceptance) returns the original path exactly, with logMH(B→A) = −logMH(A→B). A04 uses k = 4: per-dwell ΔD varies and replayed admission and bind W change. A24 is a rotated path whose first and wrap segment are one object | required |
| A05 | birth and birth_rev events replayed under admission, with W change | required |
| A06-A08 | Dwell guard: admission or hop changes v mid-path; a zero multiplier removes the mark | required |
| A09, A10 | Replay impossible: bind after `admit_rev`; flip multiplier becomes 0 | required |
| A11 | Inverse-canonical mismatch, in an interior dwell and in the reference dwell | required |
| A12, A13 | Empty owner: self-loop with exactly one draw and no resampling | required |
| A14 | Roster is the exact owner; a same-group newborn admission mark is excluded | contract |
| A15 | Roster factors N_f ≠ N_r (ladder): log(1/2) and log 2 cases, with composition | required |
| A16-A19 | Nonfinite D or W, overflowing ΔD, read/source failure: `_Stop('failed')`, input unchanged | required |
| A20 | Budget interruption at every checkpoint (accept, replay-fail and empty paths): `_BudgetStop` propagates and the path is unchanged | required |
| A20d | No accepted-type diagnostic is mutated under any interruption | contract |
| A21 | Enumeration-cap interruption at every enumeration | required |
| A22, A23 | Event cap, malformed path, unknown label; stored-event W, owner or target inconsistency → `_Stop` | template |
| A22r | Roster must be a unique, nonempty tuple | required |
| A25 | Opaque state and key objects: no hard-coded tuple-index reads anywhere | required |
| A26 | Duplicate admission mark → `_Stop('failed')` | required |
| A27 | Inert-move detector: every legal proposal with u below threshold changes; a 300-move numpy-RNG chain changes | required |
| A28 | Diagnostics: counters present; read-integral net and absolute changes equal the oracle | contract |
| A29 | Static AST: import inert, no state/key tuple-index reads, no sampler writes or globals | required |
| A30-A32 | Exact DB, and kernel equal to the oracle, on DB3, DBL and the defect DB3 | required |
| A18i, A33i | Info probes | info |

Every fixture checks that its own construction is valid (the oracle status matches the intended case) and that it is sensitive: the W term is nonzero and ΔD is non-uniform.

## Results

### Harness validation: `M2_results_birth_control_v001.json`

**Birth control** on the pinned 6f866bda module: 10/10 required and 1/1 template fixtures pass (781 checks).
- **logMH** is bitwise equal to the oracle in all 9 comparisons, including the count factor log 2. Forward+reverse sums are exactly 0.
- **Composition** is exact for k = 0 and k = 4, and for the rotated path.
- **Guards** are self-loops, and all 120 budget checkpoints and the enumeration caps were checked.
- **Exact DB** holds on DBB, with 80 pairs and all 40 thresholds by full black-box bisection.
- **Detector positive controls:**
  - the opaque key raises TypeError at Birth's `key[6]`;
  - the static check flags Birth L107 `new['key'][6].bit_count()`.
- **Observation (reference behaviour, not a harness failure).** Interrupting Birth at its commit checkpoint (L110) leaves `birth_residence_read_integral_change_sum`, the absolute sum and the donor diagnostic already updated (L99-109). The path stays atomic; only diagnostics are affected.

**Reference transcription** (test-only; written from 0456 and the Birth reference, never from the author code): 28/28 required, 3/3 contract and 2/2 template fixtures pass.

**Transcription mutants:** all 15 are detected.

| mutant | detected by | genuine DB violation |
|---|---|---|
| D sign flipped | A01-A05, A14, A15, A24, A25, A27 | all doubles |
| Count ratio inverted | A15 | DBL only (native N = 1) |
| W ratio omitted | A04, A05, A24, A25 | all doubles |
| Extra admission amplitude | everywhere (also breaks reciprocity) | all doubles |
| Extra time density, log β | everywhere | all doubles |
| Target-key checks removed | A11 | defect DB3 only (the native inverse is exact) |
| Only reference dwell transformed | A04/A05 expected `changed`, got `rejected` | DB holds; kernel ≠ contract (inert) |
| Roster restricted to eligible vertices | first-draw bound, A12, A13 | DB3 and defect DB3 (the cap changes eligibility); on DBL kernel ≠ contract only |
| Resample on empty owner | A12, A13 (extra draws) | DB3 and defect DB3 (the cap changes eligibility); on DBL kernel ≠ contract only |
| Bare `("vertex", v)` owner | A27 and all legal cases: inert | DB holds; kernel ≠ contract |
| Stale row/Da | segment equality and diagnostics | kernel identical |
| Diagnostics written before the commit checkpoint | A20d | kernel identical |
| In-place commit | immutability, outcome contract | kernel identical |
| Wrap dwell omitted | D-term checks | all doubles |
| Uniform dt | A04, A24, A25 | all doubles |

### Author module: `M2_results_c3_v001.json`

**c3v001, snapshot `5b19e90e`: 29/29 required, 3/3 contract and 2/2 template fixtures pass (1,379 checks). No defect was found within M2's scope.**

- **Diagonal ratio and Hastings terms.**
  - logMH is bitwise equal to the oracle in all 19 comparisons, and all 7 forward+reverse sums are exactly 0.0.
  - A01: L = −0.7020000000000001 = −β·ΔD.
  - A04: L = 0.8995113254635071, with D term −0.369 and W term 1.268511325463507.
  - Ladder (A15): L = −0.8101471805599452 with N_f = 1 and N_r = 2; then 0.5761471805599453 and 1.3951471805599454 with N_f = 2 and N_r = 1.
- **Exact detailed balance, with the module kernel equal to the oracle kernel:**
  - DB3: 696 pairs;
  - DBL: 208 pairs, 104 thresholds by full bisection;
  - defect DB3: 288 pairs. The guards keep DB even though the operator's `admit_rev` is not an exact inverse.
- **Interruptions.**
  - 196 budget interruptions (129 + 63 + 4 checkpoints) and 20 enumeration-cap interruptions. All leave the input path unchanged and commit nothing partially.
  - No accepted counter or read sum is written before the commit checkpoint (L145-156). The extra 'between' checkpoints are exactly 5 dwell plus 4 event hooks (129 versus 120).
- **Selection.**
  - Draws are the vertex over |R| = 3, then the mark over N_f; the uniform is drawn only when L < 0.
  - The same-group newborn mark is excluded (L60-66).
- **Opaque-key run and static AST:** clean. The only tuple-index read is the owner `ch['owner'][1]` at L65, in the fail-closed owner branch; it is not a state or key read.

**Author-logic mutants.** 18 mutations were applied to scratch copies of c3v001; author files were never touched.
- **17 are detected,** with the same detection and DB pattern as the transcription mutants.
- **`group_level_roster`** (accept every admission mark in v's group palette) is caught only by contract fixture A14; DB still holds.
- **`bare_owner`** becomes a hard failure, because the L65 fail-closed branch catches it. That is a favourable property.
- **`no_reverse_target_check`** (L115, `if reverse is None or not keys_equal(...)` → `if reverse is None:`) is not detected. It is behaviourally equivalent: 29,856 exhaustive comparisons on DB3, defect DB3 and DBL found 0 differences. By `_unique_mark` uniqueness, `reverse` is the same (inverse kind, owner) mark at the same dwell-0 state, from the same group palette, as `back` at L105-109. Its target was therefore already verified. The check at L115 is defensive and redundant, not a defect.

**Line-specific observations on c3v001 (none blocking):**
- **L132-134.** `math.fsum(terms)` raises a raw `ValueError` ("-inf + inf in fsum"), not a `_Stop`, when dwell terms overflow with opposite signs. This needs \|D\| ≈ 1e308 (A18i, where the input path was unchanged). It is inherited from Birth L86. A single overflowing term is correctly a `_Stop('failed')` (A18). `OverflowError` from fsum intermediate overflow is of the same class and was not separately exercised.
- **L136-137.** `last_proposal` and `legal_transport` are recorded before the Metropolis decision and the commit checkpoint. The A33i probe saw these entries after a post-checkpoint failure. This is proposal-level diagnostic only, as documented in their helper note O5 and in Birth.
- **L74-79.** The roster is validated up front: a `group` of None, or any roster entry with `group[v] != v` (for example a newborn label, even when not chosen), raises `_Stop('failed')`. This is stricter than Birth and consistent with 0456.
- **L146-149.** Pre-existing read sums of the wrong length raise `_Stop('failed')` after the commit checkpoint. The path is unchanged and only proposal-level diagnostics are present (A33i).
- **L65.** A non-V003 admission owner family at the chosen vertex raises `_Stop('failed')`. This is unreachable with V003.

## Detailed balance is not ergodicity

DB is verified only for this restricted move, on enumerated tiny spaces (fixed times, k ≤ 2). The move alone is not ergodic:
- it preserves the times, the event kinds and owners, and every non-admission bit;
- it self-loops whenever v's admission changes mid-path or an event cannot be replayed;
- under V003 it never proposes admissions at newborn vertices.

There is no mixing claim.

## Untested cases

- **Real operator and sampler.** The real V003 operator and V004/V006 sampler were never executed. Not modelled:
  - the support-weight multiplier 1 + Σ n·w, gauge phases and complex κ;
  - real canonical keys;
  - pair, allk and whitened reads;
  - palette verify mode.
- **Integration into V006.** Untested: the sweep schedule and mixture weight, and `run['group']` built from a real graph0 palette binding.
- **DB enumeration limits.** It uses one time configuration for k = 2, and k ≤ 2 only; k = 4 is covered only by targeted fixtures. Thresholds on DB3 and defect DB3 are bracket-confirmed to 1e-10 relative, not fully bisected.
- **N_f ≠ N_r** was tested only on a non-V003 ladder extension. Natively N_f = N_r = 1, which was checked on all 69,632 main-double states.
- **Branches not triggered:** 'Nonfinite read change' and 'Nonfinite cumulative read change' (reads are finite in the double). Also untested: an fsum `OverflowError`, unhashable roster entries (author note O4), and hook exceptions or non-bool hook returns at module level.
- **Out of scope:** ergodicity, mixing and autocorrelation, which root measures.

## Run commands

The interpreter is `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`. Run with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1` and `-I -B`.

```
M2_fixtures_v001.py --birth-control --reference --mutants --out M2_results_birth_control_v001.json
M2_fixtures_v001.py --module M2_snapshot_5b19e90e/admission_residence_transport_c3v001.py \
    --expect-sha 5b19e90ee4fcf86a0b8fe570abb607ae23c8047771abc4ab317c167f1837d653 \
    --author-mutants <scratch dir> --out M2_results_c3_v001.json
```

For a generic module: `--module PATH [--expect-sha SHA] --out JSON`. Runtimes were about 53 s and 62 s.

## Files (sha256)

| file | sha256 |
|---|---|
| `M2_sampler_double_v001.py` | `02ca6cff55b0b1208a7de765ccd8c535bcbfdbe7a248b0f0bc51c930589329bd` |
| `M2_fixtures_v001.py` | `818b532965831ab7f37613b52f96ee0bde4a65fbc364c2ebc618d8baf6577849` |
| `M2_results_birth_control_v001.json` | `d23e3a464e08cdb4927ac37d77fbb16525c6d668b36aee58664b636aae757be2` |
| `M2_results_c3_v001.json` | `559767d3375f0316ed6b5b3c2cdf81f936d524f41a39bac00fe650bc7b0cd7b2` |
| `M2_snapshot_5b19e90e/admission_residence_transport_c3v001.py` | `5b19e90ee4fcf86a0b8fe570abb607ae23c8047771abc4ab317c167f1837d653`, cmp-identical to the author file |
