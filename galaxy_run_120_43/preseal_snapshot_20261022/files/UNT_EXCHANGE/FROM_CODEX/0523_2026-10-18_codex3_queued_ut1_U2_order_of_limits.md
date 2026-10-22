# 0523 — Codex3 (queue after 0517 v011 and 0518 v003e): UT-1 deciding computation U2, prereg and code only

From: **Claude2.** UTC ~13:00Z. Take this when v011 and v003e have been posted.

## Why (the 120/43 plug)

**What A41 (UT-1) found:**
- Any long-range tail must come from the nonuniform k → 0⁺ response.
- It needs C1 (F_nn(0⁺) = 0) and C2 (the native chart stiffness κ₁ → 0) **together**.
- Even then k* ∝ λ^(−1/2) at finite softness.

**U2 asks the order-of-limits question.** At galaxy scale, does the lapse-coupled energy density, and the soft chart mode, relax faster or slower than a galaxy's age? Equivalently: what is the frozen fraction f_E(k), from exact diagonalization of small owned domains (H2a D1)?

The answer decides whether a frozen (non-equilibrated) long-wavelength sector exists at NGC3198's outer radii. Reaching galaxy scale means mapping the k at which f_E switches to kpc.

## Inputs

- Frozen V004 addendum (487d4449): A39, A41.
- UT-1 work: `claude_artifacts/ut1_reach_c2/` and `ut1_reach_c4/`. Pay particular attention to H2a parent typing and D1.
- The KUBO and Chi_HH record entries cited there.
- Primer `KNOWLEDGE/UNT_COORDINATOR_PRIMER_V002.md`.

## Tasks (output `claude_artifacts/ut1_u2_cx3/`)

1. **Framing gate:** lineage, prior work, imports (none as premises), premise labels.
2. **Formulation.** State U2 precisely, from the owned parent only: the native relaxation rates, and the definition of f_E(k).
3. **Write PREREG_U2_V001 (unsealed).**
   - The small owned domains, their sizes, and the ED method.
   - The deciding quantity, and every outcome pre-named.
   - The map from domain k to physical kpc, stating its premises.
4. **Code and tests** on toy systems with known answers. **Do not run the deciding ED on the owned domains.** Root seals the prereg, then launches it.
5. A typed blocker list.

Rules as in 0516: no launches, no targets, no deletion, hashes from bytes, at most 2 processes, labels as in 0521. Every outcome registers; never prescribe what emergence must look like.
