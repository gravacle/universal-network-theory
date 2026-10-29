# First native calculation: a retained record controls link dynamics

Date: 2026-10-28  
Status: worked analytic example from the existing finite model, with a numerical gate check. **No electromagnetic derivation or new theorem is claimed.**

## Purpose

Start from defined physical-model variables and operations rather than introducing a new object called a bend. This calculation follows the already specified handoff writer into retained memory and then computes the subsequent link response.

The relevant source is [FPMH, sections 2–6](https://github.com/gravacle/universal-network-theory/blob/79a5ae3d689df5e4572d9f955d002a173baccdbf/LANE_CROSS_RFT_MGFT_FINITE_PAIR_MEMORY_HANDOFF_V001/THEOREM.md). [PESC, sections 1–2](https://github.com/gravacle/universal-network-theory/blob/79a5ae3d689df5e4572d9f955d002a173baccdbf/LANE_CROSS_RFT_ALPHA_GRA_DB_F3_PAIR_ELIGIBILITY_SUCCESSOR_COMPOSITION_V001/THEOREM.md) identifies the same link factor with successor incidence and places its gate within a larger interacting parent.

This also sharpens the earlier discussion: the photon record example assumes EM, while this separate finite handoff witness has no explicit EM field or Maxwell action. It supplies quantum preparations and interactions. It is not a demonstrated physical implementation independent of EM.

## 1. Declared inputs

The finite model supplies two carrier qutrits A and B, each with a unique blank and two content states; the initially blank relation registers L, K, and G; and a blank link a. L is the fresh writer target, K is active retained memory, and G is a quarantine register. The finite census also includes the source, routing, controllers, clock, work/reference factors, and readout history.

The source preparation, common writing unitary, source isolation, positive hold, route operation, link interaction, and fixed read are inputs. Ordinary unitary quantum evolution is used. The calculation does not derive these primitives from a deeper dynamics.

For a worked example choose content 0. This choice is not a physical spin interpretation.

## 2. Formation versus a matched history without handoff

The actual-handoff arm F starts with content at A and a blank B. The sham arm S starts with the same content already at B. In both arms L=K=G=a=0.

One common supplied unitary exchanges, for either content c,

|c, blank, 0>_ABL <-> |blank, c, 1>_ABL,

and fixes the prepositioned sham |blank, c, 0>. It is the same operation in both arms.

| Stage | Actual handoff F | Prepositioned sham S |
|---|---|---|
| Before writing | A contains 0; B blank; L=0 | A blank; B contains 0; L=0 |
| After the common writer | A blank; B contains 0; L=1 | A blank; B contains 0; L=0 |
| After KEEP routing | L=0, K=1 | L=0, K=0 |

The final carrier states match. The relation register retains whether the handoff occurred, not the content value. The writer transfers content; it does not clone it.

After writing, source couplings are off. A strictly positive identity hold, or a declared common hold commuting with L, retains the distinction. The supplied KEEP operation SWAP(L,K) moves it into active memory. The alternative BREAK routes the formed relation into G, preserving the information while removing it from the active link/read path.

The source specifies an exact writing unitary. It does not provide a calibrated formation duration or a unique microscopic pulse implementing it.

## 3. Calculate the subsequent link response

Let P_K=|1><1|_K. The supplied gate is

H_gate = -h P_K tensor X_a, with h>0.

The commutator [H_gate,P_K tensor I_a]=0. Therefore this interaction preserves the stored memory while allowing link motion.

Write theta=h*t/hbar for time measured from the start of the gate stage. Starting from a=0:

- K=0: a remains |0>.
- K=1: a becomes cos(theta)|0> + i sin(theta)|1>.

Consequently,

P(a=1 | F,KEEP,t) = sin^2(theta),  
P(a=1 | S,KEEP,t) = 0.

| theta | Link-occupation probability, F/KEEP | Link-occupation probability, S/KEEP | Complete (K,a) read contrast |
|---|---:|---:|---:|
| 0 | 0 | 0 | 1 |
| pi/4 | 1/2 | 0 | 1 |
| pi/2 | 1 | 0 | 1 |
| pi | 0 | 0 | 1 |

The complete fixed read already distinguishes the histories through K, even when the link probabilities coincide. At t=pi*hbar/(2h), the link flips with certainty in the formation/KEEP arm, up to a phase. This time is a link-response duration, not the record-formation time.

If the gate remains active, the link continues to oscillate. Retained memory does not mean permanently occupied or frozen links. The BREAK and sham cases have K=0 and no gate-driven flip in this reduced model.

These are consequences of the supplied interaction. They establish a finite conditional record-to-link response, not an electromagnetic field.

## 4. A control for the proposed collective extension

For the gate term alone, take two fixed retained memories K1=K2=1 and two blank links. The reduced Hamiltonian is

H_gate,2 = -h (X_1 tensor I_2 + I_1 tensor X_2).

The terms commute, and the propagator factorizes into the product of the two single-link propagators. From the product blank, the connected occupation covariance remains zero. Adding independent copies therefore does not, by itself, introduce coupling among their dynamics.

This is a deliberately restricted control, not a claim about the full F3 parent. PESC's full parent also includes shared degree-energy terms and incidence-dependent carrier transport. Those terms cannot be dropped when assessing collective behavior in that parent.

## 5. What was checked computationally

[native_gate_check.py](native_gate_check.py) evaluates matrix exponentials of the supplied four-dimensional memory/link Hamiltonian at the four times above. It checks the memory commutator, link probabilities, complete read contrast, and the two-link gate-only factorization. It does not numerically reconstruct the full handoff device or certify its entire physical census.

The computed maximum discrepancy from the stated identities was 5.20740757162067e-16, within the declared tolerance 1e-12. The two-link connected occupation covariance at theta=pi/4 was -5.551115123125783e-17, consistent with zero at floating-point precision.

Run with the existing NumPy/SciPy dependencies:

```bash
python3 native_gate_check.py > native_gate_results.json
```

The saved [results](native_gate_results.json) contain the actual output. All numerical evolution uses h=hbar=1, equivalently dimensionless theta; no measured physical duration is asserted.

## 6. Next bounded calculation

Choose one finite configuration permitted by the existing formation and support rules. Declare its boundary conditions and preparation. Include its already admitted shared interactions, preserve source isolation and retained memory, and compare its collective response with the independent-gate control.

The immediate question is whether the shared terms produce a nonfactorizing, accessible response while the records remain retained. A closed-loop transition is a useful target only on a configuration that actually admits one. Charge/flux structure, field dynamics, and coupling to sources must still be justified before an EM interpretation. Neither a single controlled link nor a nonzero correlation alone establishes electromagnetism.
