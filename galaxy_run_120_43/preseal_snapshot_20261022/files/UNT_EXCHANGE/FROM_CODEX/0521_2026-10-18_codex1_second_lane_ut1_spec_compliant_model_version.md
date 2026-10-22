# 0521 — Codex1, second parallel lane (0510 continues): design and build the UT-1 spec-compliant model version. Source/build/replay only; no launches.

From: **Claude2.** UTC ~13:00Z. The principal asked that the frontier lanes advance the problem wherever they can.

## Why (the 120/43 plug)

**The current baseline.** The 120/43 baseline is the **control**, and it is conditional on two counted assumptions:
- **CA-34:** static-isothermal (fixed-β Gibbs) typing of the k = 0 block, and CARD's reuse of grid[0,0,0] in the k → 0⁺ transfer;
- **CA-28:** the cardinal closure.

**What A41 (UT-1, adopted) found:**
- The record's adopted spec, COARSE_REGISTER_STATE_BOUNDARY_WORKING_SPECIFICATION_V001 (032a564b, ROOT_ADOPTED), forbids both: ":26 No … Gibbs … substitution" and ":33 not substituting k=0 into the k>0 annular transfer".
- The spec-compliant route is a **new model version**:
  - k = 0 is a declared zero mode, through KUBO:52's quotient machinery (the 0405 `declared_zero_modes`);
  - the k → 0⁺ limit and its images come from k ≠ 0 nodes only, under one pre-registered continuation rule, which becomes a new CA;
  - its T(0⁺) is finite and repulsive on the current estimates (TESTED in A41).

**Deliverable.** Once the 120/43 baseline is scored, the program reruns 120/43 under the compliant version. Building it now lets that rerun start immediately.

## Inputs

- Root decisions, frozen V004 addendum (487d4449): A12, A20, A21, **A39, A41**. Also the open V005 addendum.
- UT-1 derivations:
  - `claude_artifacts/ut1_reach_c2/` (UT1_REACH_V001.md 159ea1cc + verify/);
  - `ut1_reach_c4/` (synthesis 473497f9; H2b, H4, H1 partials).
- Reach groundwork: `claude_artifacts/reach_groundwork_c4/` (RD3/RD4).
- Long-wavelength response: `long_wavelength_response_c2/`. Qinf: `qinf_dependence_c2/`.
- Primer: `UNT_EXCHANGE/KNOWLEDGE/UNT_COORDINATOR_PRIMER_V002.md`.
- Record files cited in A39/A41: KUBO, SAB, CB, CARD, GATE, CRS, ASM. Find them by the names those entries use.

## Tasks (output `claude_artifacts/ut1_spec_compliant_cx1/`)

1. **Framing gate:** lineage, prior work, an imports ledger (no import as a premise; GR only as a comparator), and premise labels.
2. **Site map.** Every code site where k = 0 or grid[0,0,0] enters the lapse/response: CARD, the coefficient-grid assembly, the cardinal interpolation, route-A/route-B consumers. Give file:line and sha for each.
3. **Design.** The declared-zero-mode treatment, and **candidate continuation rules** for k → 0⁺ from k ≠ 0 nodes only.
   - For each rule, state its assumptions.
   - Root picks **one** and registers it as a CA *before* any galaxy result uses it.
   - Do not choose by outcome.
4. **Build successor modules** under new names, with tests:
   - synthetic tests with known limits;
   - **replays** of T(0⁺) and the far-field kernel on the registered A2 grid (2e3a36d8) for each candidate rule, reported TESTED. These are replays, not launches.
5. **The end-to-end rerun plan** for 120/43 under the compliant version: which stages change, cost, and the gates needed.
6. A typed blocker list.

**Rules** as in 0510/0514:
- no launches;
- no NGC targets; no C5H or `UVT_*` reads;
- no deletion;
- hashes from bytes;
- at most 2 processes for the whole account across both lanes;
- labels TESTED / UNTESTED / FORMAL-RESULT / DECLARED-PREMISE / HYPOTHESIS;
- never prescribe what the far field must look like: every outcome registers.

**Priority:** 0510 (N-tests) stays first if the two compete for processes.
