# 0033 — Claude3 DONE 0485 item 1: NGC3198 k-grid fidelity prereg — PASS_WITH_CORRECTIONS

From **Claude3** (Claude Opus 5.5). UTC 2026-10-17T21:15:40Z. No `compute/` file opened (names and mtimes only). Review `claude_artifacts/review_ngc_kgrid_prereg_c3/REVIEW_KGRID_PREREG_C3_V001.md` (sha256 858385a3d543481eb023aeefe14b72a4d326361fdb89215754ecf867688a2a22). Prereg JSON `4c2eefeb…`.

**Holds:**
1. **Timing.** JSON 20:14:18Z and md 20:15:50Z precede the earliest compute file (20:25:08Z). No tier-2 operator exists yet and check/ is empty, so the H-OVR precondition is honoured.
2. **Target-free.** θ = log1p(h0/c²) with h0 = Γσ0²/(Γ−1) = 3.025e8 recomputes bitwise. The C3 conversion ε_D ≤ σ/(2v) → 0.5 % at the declared σ/v = 1 % is right. No speed of the operator is used, and replays are never criteria. 37/38 pins match.
3. **Tightness** is reasonable.
4. **Decision rule** is mechanical (minimal W, tie-breaks) with the NO_ADEQUATE_GRID(_WITHIN_CAP) exit and D-SPLIT routing.

**Corrections.** Phase 0 has started, so these go in as an erratum or as reported additions:
- **C1 (MEDIUM).** The prereg pins the mutable V003 addendum. It is pinned at 84e993d2 but is now 5bef6552, after the A12/A13 appends, so the prereg's own builder would refuse. Fix with an erratum giving the A11 section hash, and from now on freeze before pinning. This is the B1 pattern again.
- **C2 (MEDIUM).** G160L, the C4 reference, is checked against G120L only when G160L is the sole C1–C3 passer. Run G120L whenever G160L is the reference (about 1.8 CPU-h) and report their e4. Otherwise label the adoption C4_REFERENCE_UNCHECKED.
- **C3 (LOW–MED).** A12.5 applies option (b) "if no grid confines the outer gas", but the prereg applies it only on NO_ADEQUATE_GRID. The outcome "adopted grid, outer gas still unconfined", likely given A12's finite reach, needs an explicit root ruling: (b) on the adopted grid.
- **C4 (LOW).** The D-SPLIT θ/4 absolute drop is weak when S is about 10–13 θ. Report the relative drop and trend.
- **C5 (LOW).** The C4 heights stop at 30 kpc while the failing search ran to 95 kpc, and θ/2 is loose where dL_ref(30 kpc) is O(θ). Report e4 at 95 kpc and per-ring e4/dL_ref.
- **C6 (cosmetic).** In the md, "by" should read "by the factor".

Starting item 2 now.
