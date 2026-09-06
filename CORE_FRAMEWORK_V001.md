# CORE FRAMEWORK — WHERE ATOMS COME FROM — V001 — 2026-08-18

**THIS IS THE PROGRAM'S ANCHOR.** Every later statement refers to the definition below. It is not
re-shaped; it is amended only by a registered erratum.

---

## WHAT THE RECORD LEVEL IS NOT MEASURED AGAINST

> **The principal, standing:** *"We want to connect Γ with classical gravity via emergence from
> records. We are NOT trying to equate Γ and gravity at the record level."* And: *"Γ is where gravity
> comes from."*

**CLASSICAL GRAVITY IS NOT EXPECTED AT THE RECORD LEVEL AND IS NEVER THE TEST.** A record-level
quantity that fails to look like Newtonian or Einsteinian gravity has failed nothing. The claim is
**emergence at scale**, so the record level should NOT resemble the emergent form.

**THE BANNED COMPARISONS — importing any of these to the record level is the error, not a finding:**
an inverse-square law, `r⁻²`, a `1/r` potential, `G`, a metric, a geodesic, the Einstein equations,
"gravity needs …", or any statement of the form *"the record-level quantity should be shaped like
gravity"*.

**WHAT MAY BE REQUIRED OF A RECORD-LEVEL SOURCE, AND ALL OF IT IS ABOUT ACCUMULATION, NOT SHAPE:**
extensive, additive over disjoint regions, not a mere count, and **sign-definite so it accumulates
rather than screening**. **A falloff EXPONENT IS NOT AMONG THEM.** The exponent is a property of the
emergent description and may not be assumed at the level it emerges from.

**A CLASSICAL-SHAPED NULL READS TWO WAYS** — the different-shape hypothesis, or no gravity present —
and same-function/different-shape is an **assumption with no falsifier yet**, never a baseline.

**`replicate/on_finding.sh` scans for these comparisons and flags them.** This is a check, not a
reminder: the program has rediscovered this at least four times, and every previous statement of it
was a doctrine row that became a checkbox.

---

## WHAT "PROOF" MEANS IN THIS PROGRAM

> **The principal, 2026-08-20:**
>
> > *"The PROOF must be something that any physicist anywhere in the world can run against their real
> > world data and confirm that it works as asserted. That is a proof. Otherwise we're not proving
> > anything other than that we can construct equations."*

> > *"PROOF means that someone anywhere in the world can prove that our calculation agrees with **any
> > record surface**."* — 2026-08-20

**A row is `PROVED` only if it names (1) the MEASURABLE QUANTITY in units, (2) the PREDICTED VALUE or
relation, (3) WHAT WOULD FALSIFY IT, and (4) `RECORDS VERIFIED:` listing at least TWO STRUCTURALLY
DIFFERENT real record surfaces — different MECHANISM, not different parameters. One record is an
instance, not a proof.** `ledger/status.py` **refuses** the status otherwise — this
is enforced by the tool, not by a checklist, because every previous guard was a checklist item and
H-3 stayed open for the life of the program regardless.

**A result about the five clauses is `FORMAL`, not `PROVED`.** Formal results are real mathematics and
are kept as such; they are not claims about the world. **H-3: the five clauses are ours, and nothing
says the world's records meet them.**

---

## THE AMENDED DEFINITION — GROUNDED IN THE WORLD'S RECORDS (O-51, adopted 2026-08-20)

**Why it changed.** The five clauses below were stipulated. Tested against ~20 real records —
HDD/FePt/CoCrPt grains, tape, flash, MRAM, AgBr latent image, DNA, synapse, zircon U-Pb, mica fission
track, ice core, lava TRM, CMB photon polarisation, superconducting flux quantum, B−L — **ZERO
satisfy them.** The clauses are, near-verbatim, *"R is a logical Pauli of a passive self-correcting
quantum memory"* — **objects not known to exist below 4D at finite temperature.**

> ### **THE WORLD USES ENERGETIC AND KINETIC PROTECTION. THE EXACT CLAUSES ASSUME TOPOLOGICAL
> ### PROTECTION. THAT IS A MECHANISM MISMATCH, AND THE PROGRAM'S OWN O-16 MEASURED IT FROM INSIDE
> ### BEFORE THE CENSUS CONFIRMED IT FROM OUTSIDE.**

**THE ONE MOVE:** the clauses were written for the **CARRIER ALONE**. They are now stated on
**CARRIER ⊗ LOCAL BATH**, with declared tolerances `(T, t_m, δ, t_w, Δ, W, N_r)`.

| | amended clause |
|---|---|
| **(i′)** | a commuting **spectral family** `{P_a}`, not necessarily an involution |
| **(ii′)** | **durable to `t_m`** — O-5's width bound, `δ = ħ/t_m`. *Never failed against nature: tolerances `1e-41`–`1e-52 J`, 20+ orders of slack* |
| **(iii′)** | non-constant on the **closed system's energy shell**, width `√(C_v k_B T²) ≥ ΔE_config`. *A 1 cm³ bath gives ~10 GeV against the census's worst offset, 0.5 MeV* |
| **(iv′)** | writable by an **energy-conserving dilation unitary** on carrier ⊗ writer ⊗ bath; cost is **free energy**, floor `kT ln2 + ΔE_config`. *This is O-4's untested "or a physical channel" reading* |
| **(v′)** | every single-region flip costs `≥ E_b`, `E_b/kT ≫ 1`. Census: 61 (HDD), ~120 (flash), ~50 (DNA), 220 (zircon), **780 (single-domain magnetite)** |

**ALL ~20 REAL RECORDS PASS THE AMENDED CLAUSES.**

> ### **THE EXACT CLAUSES BELOW ARE RETAINED AND RENAMED: THEY ARE THE `T → 0`, `t_m → ∞`, `W = 0`,
> ### `E_b → ∞` CORNER — "DEF-A". Every one of the 162 FORMAL rows remains a true theorem about that
> ### corner. What they are not is a statement about the world, which has approximately zero
> ### residents there.**

**And this answers H-6 as a by-product: records are macroscopic because the amended clauses require a
macroscopic bath to export the write energy — not because the carrier must be big.**

---

## THE DEFINITION — DEF-A, THE EXACT CORNER

Let `H` be a Hamiltonian and `{L_k}` the jump operators of an open system. **`R` is a RECORD if:**

| | clause | meaning |
|---|---|---|
| **(i)** | `R = R†`, `R² = I` | it is a **bit** |
| **(ii)** | `[H,R] = 0` and `[L_k,R] = 0` ∀k | it is **durable** — by T1 its value cannot change |
| **(iii)** | `R` is not constant on some eigenspace of `H` | it is **non-trivial** — it distinguishes states of the *same energy*, so it is not a function of `H` |
| **(iv)** | some **admissible** `U` has `U†RU = −R` | it is **writable** |
| **(v)** | **no admissible** operation on a **single** contractible region does | it is **protected** |

> **"ALPHA" NAMES A GENERIC COUPLING STRENGTH** — the magnitude of the local terms that do not
> respect the record's structure. **It is NOT the fine structure constant.** No result in this program
> depends on its value (T-10: 28 settings over `λ = 0.05`–`3.0`, no conclusion moved), and **nothing
> here is dimensionful.** What its value would set is the RATE of formation, `χ ~ λ^{2n*}`, which is
> connected to no physical number. (T-22, `H-2`.)

> **ADMISSIBLE `U` ≝ a unitary with `[U,H] = 0`.** (O-4, 2026-08-18. **PROVISIONAL** — one carrier
> family, and DEF-A has **no working fallback**: the registered DEF-A' escape was a miscount.)
> Equivalently, given (i)+(ii): **clause (iv) ⟺ `Tr(P_E R) = 0` on every eigenspace of `H`** — at every
> energy the record's two values are equally available (C-11, and independently the Balance Lemma).
>
> **ERRATUM TO CLAUSE (v), AND IT IS WHY THE WORD WAS NEVER OPTIONAL.** As previously written, (v)
> carried **no** admissibility restriction and was **FALSE OF THE TORIC CODE**: a single-edge `X` on
> `(0,0,H)` satisfies `X†RX = −R` **exactly**. At `L=3`, **1158** single-region Paulis flip `R`; at
> `L=5`, **2.815e15**. **With `admissible` inserted, (v) holds exactly** — `0` admissible flippers in
> 36 certified-contractible regions at `L=3` and `0` in 300 regions up to 24 edges at `L=5`, against
> those same counts as the positive control. Independently reproduced by a second implementation.

> **"CONTRACTIBLE" IN CLAUSE (v) — THE CONVENTION, AND WHICH CARRIER IS CANONICAL.** (O-49, the
> principal, 2026-08-20.) Clause (v) was first tested on a 1D chain by O-48, and there the reading
> matters: on an OPEN chain the whole carrier is one contiguous block, so (v) **FAILS** — smallest
> flipping contractible region exactly `w = n` at every `n = 3..14`, by an exact criterion over every
> unitary on the region, 630 cross-checks, zero disagreements.
>
> **THE CONVENTION ADOPTED, FOR 1D RINGS ONLY:** clause (v) operates under the **standard QEC
> constraint** — locality is bounded by **PROPER sub-regions**, `diam(R) < L`. Under that reading (v)
> **HOLDS** on the ring with distance `n`, and it matches T-11's no-cycle convention.
>
> **1D RINGS ARE A BOUNDARY-CONSTRAINED PROXY, NOT THE CANONICAL CASE.** The convention above is an
> explicit low-dimensional stipulation and is labelled as one wherever it is used. **THE CANONICAL
> BENCHMARK IS THE TORIC CODE**, where clause (v) is realised purely through **manifold homology** —
> the logical operators have genuinely non-contractible support, both distances scale with `L`, and
> no semantic caveat about "contractible" is required. Any result whose truth depends on the 1D
> convention is scoped to the proxy and must say so; results on the torus are not.

**WHY (iii) IS STATED THIS WAY.** If `R = f(H)` its value is fixed by the energy: knowing the energy
tells you the record, so it carries no bit beyond the energy. Phrasing it as *"distinguishes states
of the same energy"* makes that precise **and makes the degeneracy requirement a one-line
consequence** rather than an assumption.

**WHY (iv) AND (v) ARE BOTH REQUIRED.** They are the writable/durable tension the program spent months
on. A record must be settable, and must not be settable by noise. **The definition makes the tension
explicit instead of hiding it.**

### VERIFIED — the definition discriminates (`LANE_P1_DEFINITION/`)

```
                                           (i)      (ii)      (iii)     (iv)      (v)
  toric-code record                       0.0e+00  0.0e+00    4.899   0.0e+00   11.314   ALL PASS
  same R, degeneracy broken locally       PASS     PASS       0.000   PASS      PASS     (iii) FAILS
  R = a function of H                     PASS     PASS       0.000   1.1e+01   PASS     (iii),(iv) FAIL
```

---

## THREE PROPOSITIONS, IMMEDIATE FROM THE DEFINITION

**P-1.** *(iii) ⟹ `H` is degenerate.* `R` is non-scalar on some eigenspace, so that eigenspace has
dimension > 1. **This is P2's forward direction, now one line.**

**P-2.** *(ii)+(iv) ⟹ the writer is built from neither `H` nor `{L_k}`.* `W` anticommutes with `R`
while `H` and every `L_k` commute with it.

**P-3.** *(iv)+(v) ⟹ **NO ADMISSIBLE WRITER FITS INSIDE ONE CONTRACTIBLE REGION**.*

> **THE STRONG READING — "nothing local can write it" — IS NOT MERELY UNPROVEN. IT IS FALSE.**
> Clause (v) quantifies over **single** regions, never over **products**. A clause (v') forbidding
> writes generated by *products* of contractible operations would give the strong reading — **and
> (v') is false by the program's own Theorem D**, which says `d` local terms **do** reach the record.
> **The gap cannot be closed by strengthening (v). The claim had to be weakened, and now is.**
>
> **The minimum-weight admissible writer at `L=3` has weight `3 = d`** and is `XXX` on three edges — a
> **product of three single-edge operators, each individually INADMISSIBLE** (`‖[X_e,H]‖ = 45.255`).
> **The record is written by an operation that is admissible only as a whole.**
**W-29/W-30's obstruction is a consequence of the definition, not an accident of our carrier.**

---

## THE CLAIM THIS FRAMEWORK SUPPORTS

> **A quantum record is a topologically protected degeneracy of a gauge field. EM supplies the field
> and the holonomy that is the record; the topology of the space supplies the record space, the
> unique writer and the protection; alpha destroys it at order `d`.**

Proved: Theorems A–D (`PROOF_V001.md`). Measured: the degeneracy requirement and the fragility
dichotomy. **Full statement and status: `THE_CLAIM_V001.md`.**

---

## EVERYTHING IN THE WAY

**SOLVABLE HERE — these stand between us and a proof.**

| | obstruction | why it blocks | approach | cost |
|---|---|---|---|---|
| **O1** | **P2's converse.** Degeneracy gives (i)–(iii); it does **not** give (ii) compatibility with `{L_k}`, nor (iv) flippability | without it, "record ⟺ degeneracy" is only one-way | construct the record from the degenerate eigenspace and show when a compatible `L_k` set and a flipper exist | **medium — the real work** |
| **O2** | **P3's symmetry half.** That symmetry-protected degeneracy splits at *first* order is measured, not proved | half the fragility dichotomy | degenerate perturbation theory: `PVP` is generic Hermitian on the multiplet once `V` breaks `G`. Needs a genericity statement | medium |
| **O3** | **P4 exhaustiveness.** "Records require topology" needs symmetry+topological to exhaust the sources | the step from 1–3 to 4 | **do not classify degeneracies.** Prove instead: *any degeneracy split at first order cannot carry a noise-surviving record* | low, once restated |
| **O4** | ~~"admissible" in (iv) is undefined~~ **DEFINED (provisional).** The suggested fix "generated by the theory's own operators" is **REFUTED** on the `*`-algebra reading — it makes (iv) **unsatisfiable for every record**, since clause (ii) puts every generator in `R`'s commutant (400 random words: `2.27e-15`; toric: `0.00e+00`; positive control on the real writer: `32.00`). **The second disjunct "or a physical channel" is UNTESTED** — narrowed, not struck | **closed → O-12 closed** |
| **O5** | **(ii) is exact; real records are approximate** | excludes `1/(8g²)`-type records | an approximate clause with a stated tolerance, and check the theorems survive it | medium |

**NOT SOLVABLE HERE — named so they are not mistaken for oversights.**

| | obstruction | why it is out of reach |
|---|---|---|
| **X1** | the topology is a **lattice's**, not spacetime's | nothing in this construction makes it spacetime topology |
| **X2** | it does **not respond to matter content on the tested fixed complex** | **Record-level row withdrawn by registered erratum `5c01e47`; scope repaired 2026-09-06.** Requiring classical matter-response at that record level imports a criterion (**D-1**), and `χ` is a construction parameter there. `G-6` was the then-internal uniqueness question and later failed. The live collective/enlarged-parent questions are `H-1`/`C-77` and conditional `F-3`/`T-II.5`/`H-7`; no response or emergence result is implied. |
| **X3** | **the outcome problem** — which unravelling is physical | the field's open problem; W-35 relocated it, did not solve it |
| **X4** | **empirical contact: zero** | not one number in this program came from a measurement |

**ORDER OF ATTACK: O4 → O3 → O2 → O1 → O5.** O4 and O3 are cheap and unblock the rest; **O1 is the
one that decides whether the claim is a theorem or a strong conjecture.**
