# REVIEW 0455 EXACTNESS V001: exact scalar-force evaluator (c2v001)

**Role:** distinct reviewer, not author. Lens: EXACTNESS/MATH. I wrote neither the module nor the fixtures. This review was done independently of the other 0455 reviewer, whose file I did not read.

**Verdict: PASS_WITH_NOTES.** There are no blocking issues. The grouped evaluation is the same finite sum as the direct sum, up to regrouping roundoff, for dn and for all three gradient components. The admission expressions are bitwise identical to the 0449 LINEAR form. The gradient reality checks are scaled by the supplied length.

## Hashes (sha256 computed from bytes on 2026-10-16)

| File | sha256 | Pin |
|---|---|---|
| Task 0455 `FROM_CODEX/0455_2026-10-16_claude2_exact_scalar_force_acceleration.md` | `b467a0c0c6e2fe3498a44ebdecca110776528dde7b4304d204cd42e64c67062c` | match |
| Line module `owned_fixed_xy_fourier_line_v002.py` (read only) | `3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18` | match |
| 0449 `nonzero_cached_feedback_c2v001.py` (read only; LINEAR convention only) | `1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95` | match |
| Reviewed module `exact_scalar_force_c2v001.py` | `0dab62be91cfd793949ef251aa3e731b4544e7131606599784762cb4101175ea` | matches author report |
| Reviewed `INTERFACE_0455_V001.md` | `c5b00a771adbca4b9748e4e0405a98c6737cafc8a0aca80358d5b4c11b855dff` | matches author report |
| Fixtures `fixtures_0455_c2v001.py` | `d1b28438273fab010ef4b3e28e07d1047f86916c9e0541ea5d232903e59b917e` | matches fixture report |

I did not modify anything. I did not touch 0449 or 0452 and did not open any project or .npz data.

## What was checked by reading the code

**1. Finite sum (lines 386–508).**
- **Dense stack.** It is built fresh on every call (lines 434–438) as `D[0][q,p] = SUM a_j` over the waves with (kz, pair) = (q, p), using `np.add.at`. Duplicates are therefore summed, and holes stay exactly zero. Then `D[1] = (1j kx_p) D[0]` and `D[2] = (1j ky_p) D[0]`.
- **Transverse phase.** `E[c,p] = exp(1j*(x_c kx_p + y_c ky_p))` (lines 452–456).
- **Collapse.** `C_f[c,q] = SUM_p E[c,p] D_f[q,p]` via `einsum('cp,qp->cq', optimize=False)` (line 463). The z line is `Cz = C_0 * (1j kz_q)` (line 465).
- **Per point.** `SUM_q exp(1j kz_q z_point) C_f[col(point), q]` (lines 476–486). This uses the exact z of each point. The column-to-local index comes from the sorted point order and the column offsets (lines 470–475), which I verified to be correct.
- **Result.** This equals `SUM_j a_j exp(i k_j.x)` and `SUM_j (i k_j) a_j exp(i k_j.x)`. Each phase is computed as the product of the transverse and vertical exponentials, so the regrouping changes only roundoff.
- **What is not in the sum.** The module never applies a weight, factor 2, c^2, reflection, symmetry, mode removal or `.real` inside the sum. The only `.real` uses are at line 269 (inside the reality bound) and lines 593–596 (after reality admission).

**2. Grouping (lines 174–197, 314–335).**
- Waves are grouped by exact-equal (kx, ky) using lexsort plus an adjacent `!=` test on both keys, and by exact-equal kz using a stable argsort.
- Points are grouped by exact-equal (x, y). z is free within a column.
- Since -0.0 == 0.0, signed zeros merge into one group. The representative changes only the signs of zeros, and the INTERFACE documents this.
- No complete Cartesian product is assumed: the dense S is indexed only at supplied cells.

**3. Admission (lines 554–628).**
- All four reality reports are evaluated before any failure:
  - `n_b` and `L*grad n_b` with the base tolerances;
  - `dn` and `L*grad dn` with the increment tolerances.
- Each check is `|Im v| <= atol + rtol |Re v|` with a finite value and a finite bound.
- Then `Nb = 1 + Re n_b > 0` is required. The test `~(Nb > 0)` also catches NaN.
- Then lines 597, 602 and 608–610 apply the formula. After stripping indentation, these lines are textually identical to 0449 lines 402, 407 and 413–417 (checked with `diff`): `delta_phi = c_squared * (dn / lapse_base)` and `grad_delta_phi = c_squared * (grad_dn / nb3 - dn[..., None] * grad_nb / (nb3 * nb3))`, with `c_squared = c*c`.
- The complex `dn_complex` and `grad_dn_complex` are kept in the COMPLETE outputs, and in `retained` on failure.
- `hessian` is a string, `NONE EVALUATED`. No array is returned.

**4. Identity and caching.**
- **Geometry.** It holds read-only float64 copies. On every call it recomputes the geometry digest over the arrays plus the counts header, and requires the supplied waves and points to have the same sha256 (dtype, shape and C-order bytes) as at preparation.
- **Base.** The base is bound to the points' sha256 and carries an integrity digest. Admission requires the base point sha to equal the finite-sum point sha.
- **Per call.** Amplitudes, S and the collapsed lines are rebuilt on every call. No source-dependent key exists in the geometry record.

**5. Lane.**
- My own AST scan found no `@`, dot, matmul, vdot, inner or tensordot. Every einsum has `optimize=False`.
- There is no errstate, seterr or warnings use, and no I/O.
- Imports are numpy and stdlib only. The top level holds only definitions.
- All five public functions are keyword-only with zero defaults.
- Importing under `-W error` is inert.

**6. INTERFACE.**
- The line references (581–610, 597, 609 and 610) are correct.
- The limit formulas match the code (lines 321 and 339–344).
- The byte multipliers (48, 40, 64 and 56) agree with the temporaries that are actually allocated.
- The 72^3 op counts are correct: 5,184 x 72 = 373,248; 3 x 373,248 = 1,119,744 MAC per column; 72 exponentials and 288 MAC per point.
- The module's own op tally equals the INTERFACE formula exactly (checked on a synthetic case).

## What was executed

Interpreter: root python `-I -B` with `VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`, numpy 2.3.5, Python 3.12.14. Data: synthetic only. Scratch directory: `/private/tmp/claude-501/-Users-bgm-MB-Work/573ea246-f21c-48d3-b8cc-d28a1f8b2c42/scratchpad/r0455/REVIEW_0455_EXACTNESS_V001/`.

**1. Fixture script** (`fixtures_0455_c2v001.py --module ... --outdir fixture_run`)
- Result: BINDING 40/40 PASS and ADVISORY 7/7 PASS in 0.50 s.
- Result JSON `fixture_run/fixtures_0455_result_0dab62be91cfd793.json`, sha256 `2bcfb38aec87278ada122af76c1f11df7e4119601f668dcb476194ef5b89b531`. It differs from the fixture author's JSON only because it is a different run and the elapsed times differ.
- Log: `fixture_run.log`, sha256 `6672e142…558c`.

**2. Reviewer adversarial checks** (`review_spot.py`, sha256 `719bf30f6e431ccc422701e9b34cd4e011a8e46196047622ad8e93ed1ed63970`; log `spot_run.log`, `65ce6a40…a930`)
- **Result:** all 43 checks OK (0 FAIL).
- **Oracle:** my own direct per-wave finite sum, with no grouping and a single-angle phase `kx x + ky y + kz z`.
- **High-precision oracle:** an 80-digit Decimal finite sum. It uses exact float products, reduction modulo 2π with a Machin π, and Taylor cos/sin.

| Case | Errors (relative to Σ\|a\| and Σ\|k_j\|\|a\|) |
|---|---|
| A1/A2: irregular signed anisotropic waves (67 pairs x 27 kz) with holes; pair-only and kz-only sharing; duplicates and triplicates; a merged ±0 column; ±0 k; unsorted waves; nonuniform unsorted z; off-column and repeated points; chunks (1,1), (2,3), (3,2), (5,7), (64,1000) | field 5.1e-16; grad x/y/z 4.7e-16 / 7.6e-16 / 1.3e-15; identical across chunkings |
| A3: against the 80-digit oracle | module field 2.3e-16 / grad 6.7e-16; float direct sum 2.2e-16 / 1.0e-15 |
| B1: extreme coordinates, astrophysical (L = 6e19 m) | against 80-digit truth: module 5.2e-17 / 5.1e-17; direct 2.5e-17 / 4.6e-17 |
| B2: extreme coordinates, tiny (1e-12 m) | module 6.8e-17 / 1.1e-16; direct 1.1e-16 / 1.4e-16 |
| B3: extreme coordinates, large angles (\|angle\| up to 1.3e6 rad) | module 2.4e-12 / 4.4e-12; direct float 2.3e-12 / 6.9e-12. Both sit at the eps·\|angle\| floor; the module is no worse than the direct sum. |
| B4–B6: overflowing phase or i k a | FAILED_CLOSED under both errstate ignore and raise, with retention |
| B7: amplitude scaling by 2^±700 under errstate raise | bitwise exact |
| C1–C5: all k = 0 (dn = Σa, grad exactly 0); nine duplicates of one wave; cancelling duplicates; single non-Hermitian wave (imaginary part kept, no reflection or factor 2); analytic single wave (i kx, i ky, i kz) | each ≤ 1.4e-15 absolute, inside an eps·(1+\|angle\|) bound |
| C6–C11: 3-D point shape; Fortran-order and strided equal-valued inputs; same bytes in another shape; reordered waves; a ±0-swapped wave | 3-D shape correct; Fortran/strided accepted bitwise; other shape, reordering and ±0 swap rejected (INVALID_INPUT) |
| C12: (x, y) = ±0 merged column with ±0 z | ≤ 7.7e-17 |
| D1–D5: amplitudes refreshed in the same caller buffer; earlier result untouched; no shared memory between calls for dn, the dense stack or the amplitude copy; geometry read-only with no source-dependent keys; tampered kz representative; base copy not aliased | fresh result equals direct; tampered kz rejected (INVALID_INPUT); no aliasing |
| E1: admission against an independent 0449 LINEAR transcription (c = 299792458, L = 2.5) | bitwise equal; the algebraic alternative c²(Nb∇dn − dn∇nb)/Nb² agrees to 4e-16; one-call path equals two-stage path bitwise |
| E2: 4th-order finite difference of deltaPhi (quotient-rule sign) | 6.6e-12 absolute |
| E3: Im(grad n_b) = 1e-6 /m with atol = 1e-5 | L = 1 and 9 admitted; L = 11 and 100 rejected on `base_gradient_length_scaled` only |
| E4: all four reality reports present; reality failure precedes Nb ≤ 0 | confirmed, with dn retained |
| E5: rtol honoured | confirmed |
| E6: n_b = −0.999999, −1, −1.0000001 | admitted, rejected, rejected |
| E7: base imaginary part within tolerance | discarded only after admission (bitwise equal to a pure-real base) |
| E8: Hessian | none returned |
| F1: 200,000 irregular waves (4e10 cells) | FAILED_CLOSED at dense_limit in 0.04 s with no allocation |
| G1: synthetic signed 72^3 lattice in a 6e19 m box (5,184 x 72) against direct | 1.6e-17 / 1.6e-17 |
| G2: shuffled 60 % subset of that lattice | 1.3e-17 / 3.3e-17 |

**3. `review_spot2.py`** (sha256 `980800bf075e15981fdff3c110236df02972e99b33ecee3ae1e7d2cdbff1b3c4`; log `6feee6c6…de50a`)
- AST lane scan: clean.
- The full prepare, bind and admit path completes under `errstate(all='raise')` on realistic-magnitude synthetic data.
- The op tally equals the INTERFACE formula.
- Synthetic 72^3 lattice with an 8x8 (R, φ) column grid x 6 z: 1.02 ms per column, and agreement with the direct sum of 9.7e-18 / 1.6e-17.

**4. `review_mem.py`** (sha256 `b43e0856f3ea4369388518a2cb57ce46f1a0afbaa568c0f8703bd3419934b68f`)
- Evaluation-only traced peak was 27.4 MB, which confirms the INTERFACE's 27 MB.
- Prepare peak was 27.4 MB.
- A COMPLETE result retains 24.0 MB.

**5. Mutation sensitivity** (`make_mutants.py`, sha256 `e4737dd3b3a1f085c9cf82362245077fa482cf0fd9930ee9e286bbe6e07758f4`; scratch copies only; summary `mutants_summary.log`, sha256 `924e0605…d2c6`)
- My checks killed all 15 single-edit mutants:
  - conjugated transverse phase; conjugated vertical phase;
  - kz derivative sign; kx/ky swap; ky sign;
  - duplicates overwritten instead of summed;
  - Nb² replaced by Nb; quotient sign; 1 − nb;
  - unscaled gradient reality;
  - pair grouping on kx only; y phase using x;
  - column misindexing;
  - `.real` applied before the sum;
  - an extra factor 2 on c².

## Blocking issues

None.

## Notes (non-blocking)

1. **Roundoff only, no certificate.** Exactness here means agreement up to regrouping roundoff. There is no error certificate. Each term carries a phase error of about eps·|angle|, which is the same order as the direct float sum (see B3). For the actual 72^3 box, the angles are O(10²) rad, and the measured agreement is about 1e-17 of Σ|a|.

2. **Retained memory per result.** Every COMPLETE finite-sum result keeps `retained['dense_stack']` (17.9 MB) and the amplitude copy alive, about 24 MB per result for the actual set. `exact_scalar_force` nests the same data. A coupled solver that stores a history of results should drop `retained` or the results themselves. This affects memory only, not correctness.

3. **Limits count entries, not bytes.** The byte multipliers are stated in the INTERFACE, and I verified them against the code. Output and index arrays are O(points + nk), are sized by the caller, and are not separately limited.

4. **Reality gate differs from 0449 by design.** 0449's gradient reality check is unscaled. In 0455, the effective gradient atol is atol/L, as the task requires. If root compares 0455 against the preserved 0449 output, L and the tolerances need to be chosen consistently. The LINEAR values themselves are bitwise the same formula.

5. **Caller errstate governs.** Under a caller `errstate(under='raise')`, legitimately subnormal products fail closed instead of flushing. The direct sum would behave the same way. This is documented.

6. **Column reuse drives the speedup.** The speedup comes from reusing (x, y) columns across z. Points that share no column still avoid the 373,248 exponentials per point, but they pay about 1.1M MAC per point. This matters if root evaluates on a non-columnar point set.

7. **Integer inputs.** `_real_array` accepts integer dtypes. Integers above 2^53 would round on conversion to float64. Identity is taken on the float64 values actually used, so this is consistent and immaterial for physical inputs.

## Scope statement

I used no actual project data, no .npz files, no root workers and no project runs. The only files under `/Users/bgm/Research/Universal Network Theory` that I touched are the read-only line module, which I opened for reading and hashing. The only file I wrote outside the scratch directory is this review, created exclusively with noclobber.
