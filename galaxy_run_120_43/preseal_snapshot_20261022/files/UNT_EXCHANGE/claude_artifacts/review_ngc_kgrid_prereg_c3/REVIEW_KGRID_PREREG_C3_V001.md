# REVIEW_KGRID_PREREG_C3_V001 — Claude3 distinct review of the NGC3198 k-grid fidelity preregistration (0485 item 1)

Reviewer: Claude3 (Claude Opus 5.5). **No `compute/` file was opened** before or while writing this verdict: compute was inspected by file names and mtimes only. Read-only; no launches; no NGC3198 velocity or σ read.

Bytes: `PREREG_KGRID_FIDELITY_V001.json` `4c2eefeb8a4e191d20173036fe0aa5e641799c70a97b96d354d0984742449869` (equals the md's and HASHES.txt's statement); `.md` `55f25369f8746e3fc3f2de626e7e4e48722db104bb92c80dd5d377a438239b99`; builder `e50e4efa…`.

## Verdict: PASS_WITH_CORRECTIONS

### 1. Timing — holds
File mtimes (UTC): JSON 20:14:18Z; md and HASHES.txt 20:15:50Z; the earliest `compute/` file is `compute/tools/kg_lib_v001.py` at 20:25:08Z and the Phase-0 logs are at 20:26:42Z (the dispatch's "20:40Z" is later still). No tier-2 operator directory exists (`compute/ops` holds only G80C/G80E14/G80L/G80EL tier-1 and the G80C/G80E14 H-OVR reproductions that gate V2 needs), and `check/` is empty, so the "H-OVR diff reviewed before any tier-2 preparation" precondition is honoured so far. Mtimes are plausibility evidence, not a seal.

### 2. Target-free and tied to program quantities — holds
- θ = log1p(h0/c²) with h0 = Γσ0²/(Γ−1) = (5/3)(11 km/s)²/(2/3) = 3.025e8 m² s⁻²; I recompute 3.3657664138980042e-09, bitwise equal to the prereg (and h0 is the same 3.025e8 as the fs nominal bracket).
- The C3 conversion is correct: v² = c² R dlnN/dR ⇒ ε_v = ε_D/2 + O(ε_D²); ε_v·v ≤ τ = σ/4 ⇒ ε_D ≤ σ/(2v); with the declared σ_ref/v = 1 % (P3, counted, no NGC σ or v read) ε_v ≤ 0.25 % and ε_D ≤ 0.5 %. The registered consequence (bound exceeds τ_i by the factor 0.01·v_i/σ_i when σ_i/v_i < 1 %) is arithmetically right.
- Criteria never evaluate a speed or radial derivative of the program operator, and replays and roots are never criteria, so the grid cannot be selected by its predictions or by whether the gas is confined. C3 radii are target-free (0.70 + 0.25j kpc and 44.08 kpc); ring radii come from the HI source reference only.
- Pins: 37 of 38 match their bytes (see C1).

### 3. Tightness — reasonable, with two notes (C4, C5)
C1 (S < θ on all 100 rings to 66.904 kpc) ties the azimuthal error directly to the threshold the free boundary uses. C2 (≤ 1 % for K1 a = 3, 5, 10 kpc and K2 to 52.7 kpc) is failed by G80C (63 % at a = 3) but is plausibly attainable by tier-2 grids whose formal panel heights exceed the tested radius plus height; a = 10 already passes on G80C. C3 is derived, not chosen. C4 (e4 < θ/2 absolute) is the only test of the operator's own vertical profile. C1 may be structurally unpassable at the fixed kmax = 2 cube if cube-corner m = 4/8 structure alone exceeds θ at outer rings; the prereg routes this through D-SPLIT TRUNCATION_SHAPE rather than hiding it.

### 4. Decision rule — mechanical, with an explicit NO_ADEQUATE_GRID exit
Pass iff gates V1–V5 and C1–C4; adopt the minimal-W passer, ties to tier 1 then list order; NO_ADEQUATE_GRID (or _WITHIN_CAP, with unevaluated grids counted as not passing) routes by D-SPLIT class; C4_REFERENCE_DEGRADED if G160L cannot be evaluated; "no change after Phase 0 starts; any change is a new version". Gates stop the run before any criterion is read.

## Corrections
Phase 0 has started, so V001 must not change. Each item below is either an erratum or a reported (non-decisive) addition, unless root issues a V002 before any criterion value is read.

- **C1 (MEDIUM) — the prereg pins a mutable decisions file.** `root_decisions_ngc_V003_addendum` is pinned at `84e993d2…` but now hashes `5bef6552…` (mtime 20:54:32Z). A12 and A13 were appended after 20:14Z. The prereg's own builder, which "refuses on any digest mismatch", can no longer reproduce it, and the A11 mandate text cannot be verified byte-for-byte against the pinned version. This is the B1 pattern again, and the addendum's own rule ("seeds pin a decisions file only once it is frozen") applies to preregs as well. Fix: record an erratum giving the A11 section's text hash, or a byte snapshot if one can be recovered. From now on, freeze a decisions file before pinning it, or pin per-section hashes.
- **C2 (MEDIUM) — the C4 reference is self-checked only in one branch.** G160L is compared with G120L only "if G160L is the only C1–C3 passer". When a cheaper grid passes C4 against G160L, the reference's own convergence rests only on the isotropic known fields (P4 is UNTESTED for this anisotropic operator, and the prereg itself notes that two under-resolved grids can agree). Fix: evaluate G120L whenever G160L serves as the C4 reference; it is about 1.8 CPU-h and fits within the cap. Report G160L-vs-G120L e4 as a registered diagnostic, and label any adoption where it is ≥ θ/2, or not evaluated, C4_REFERENCE_UNCHECKED.
- **C3 (LOW–MEDIUM) — option (b) condition, reconciled with A12.** The prereg (and A11) make roster truncation (b) the fallback only on NO_ADEQUATE_GRID. A12 item 5, written after the prereg, applies (b) "if no grid confines the outer gas". Because the prereg rightly never tests confinement, the outcome "ADOPT_<id>, but the adopted grid's replays leave outer columns unconfined", which A12's finite-reach result makes likely, is not routed by the prereg. Fix: state in the root decisions that A12.5 then governs: truncate on the adopted grid, record the mass fraction, and mark query rows beyond the cut INVALID.
- **C4 (LOW) — the D-SPLIT QUADRATURE_LIMITED test is absolute.** "S(Gf−1) − S(Gf) ≥ θ/4" is met by a small relative change on rings where S ≈ 10–13 θ, even when S converges to a nonzero (possibly physical, P1) limit. That biases attribution away from NOT_GRID. It affects next-step selection only. Report the relative drop and the three-grid trend alongside.
- **C5 (LOW) — the C4 height range and the marginal rings.** The decisive heights stop at |z| = 30 kpc, while the failing column's search ran to 95 kpc. An absolute θ/2 is also loose where dL_ref(30 kpc) is itself O(θ), which is exactly at the outer rings where confinement is marginal. Report e4 at 95 kpc next to R4, and report e4/dL_ref per ring. Flag rings with dL_ref(30 kpc) < 2θ.
- **C6 (cosmetic).** In the md, "exceeds τ_i by 0.01·v_i/σ_i" should read "by the factor"; the JSON is right.
