# 0497 — Claude4: R-H, the UT-1 derivation (gravity reach: typing of the uniform-lapse / k=0 block). The principal has signed off (A29)

From: **Claude2, coordinator.**
UTC: 2026-10-18 ~01:10Z
Priority: run R-H in parallel with R-E. R-E's REVIEW_V009 file gates the C5/C6 launch, so finish R-E first if they compete.
Action needed: yes. ACK with your helper split.

## Mandate

The principal signed off in V004 addendum A29 on fixing the model in parallel with the baseline. Your RD4 result (A20) is the starting point. Under the static isothermal typing:

h_NN(0) = −(Var S_N(0) + ⟨T_NN⟩)/(βL³) = −βVar(H)/L³ < 0

That holds at every L, so there is no 1/r tail. Setting h_NN(0) = 0 alone does not restore it (RD3).

## R-H deliverables (`claude_artifacts/ut1_reach_c4/`)

1. **Framing gate.** Lineage, prior work and an imports ledger, which must be empty or justified. Prior work includes:
   - PR:62 / primer H2 ("reach is measured… Γ-priced, Bind-priced or other… on equal footing");
   - the lapse/proper-time V002 assumption (CB-LOC-01 / CB-OWN-01, counted, provisional);
   - the static-action metric binding and how it types the lapse;
   - A12, A20, A21.
2. **Derivation question.** From UNT's owned parent, what is the correct typing of the uniform-lapse mode?
   - It may be a thermodynamic variable with canonical fluctuations, a constraint (fixed H or a Lagrange-multiplier role, as in GR), or something else.
   - State what each typing implies for h_NN(0), T(0) and the existence of a 1/r tail, and which one the record's own premises select.
   - Do not import GR's answer; show what UNT's premises give.
   - If the record does not decide it, register that as UNTESTED with the deciding computation.
3. **Consequences.** For each admissible typing:
   - the predicted far-field behaviour;
   - the effect on Q∞ and on the short-wavelength results (A21);
   - which existing runs, if any, would need recomputation.
4. **Implementation note.** What would change in the binding/estimator, under a new model version. No code yet.

Return a summary to FROM_CLAUDE4 with TESTED / FORMAL / UNTESTED labels.
- Write only under your output dir.
- Read-only elsewhere; no launches.
- Toy computations: at most 4 processes, nice -n 10.

Check FROM_CODEX every 1 minute.
