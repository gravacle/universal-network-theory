# Hard-reaction attribution V001: independent preflight

Accepted 2026-09-29 after complete source/protocol and analytical-design read.
No module import, producer execution, new outcome inspection or frozen-source
modification was performed for this review.

Bound source `clamped_hard_reaction_attribution_v001.py`:
`fae9bf1e327bf9ad1828fbe2399c6ddc8cc9f585f61956f2b390a3cb90f6ca8d`.

Bound protocol `CLAMPED_HARD_REACTION_ATTRIBUTION_PROTOCOL_V001.md`:
`49b24e5ec7142860e3b8b49effedd220cabc7ea03222efa4f6aa1b16fff3bf16`.

The four original N16 cases and two original guesses are retained. Saved
physical roots/iterates supply comparisons, never new seeds. Recursive
original-input custody, exact case/result hashes and the additional sources
are bound before execution. Stdout-only publication and guarded import of
the frozen implementation introduce no file writes or scientific execution
at import. Temporary evaluator dispatch is restored in try/finally.

The residual is assembled directly from unchanged polarized flux minus only
the soft reaction. Its Jacobian retains the complete material/phase flux
tensor and lapse dependence, with the exact soft derivative 2Fsoft. Thus the
production Newton matrix does not numerically subtract a large hard J term.
The separately computed final-state identity

    J0=Jphysical-epsilon² Jstatic/Kb
       +epsilon(2Fhard-F_Phi) n.grad/Kb

has the correct signs and normalization. The full-model residual satisfies
Rphysical=R0-epsilon deltaT_hard/Kb. Its field and integrated defect are saved,
along with all hard energies, pressure, action and unchanged DeltaU.

Inherited prerequisite, finite-difference, quadrature and flux controls remain
unchanged. Active-set/domain exclusions cannot silently qualify a Jacobian;
nonconvergence remains a retained outcome. Pair qualification requires both
original and counterfactual solves and controls, so a failed physical branch
cannot be promoted to a measured equilibrium difference.

This intervention deliberately breaks the original action's source relation.
It can attribute solver/equilibrium behavior to the hard volume reaction,
but is not a replacement theory, an energy-free physical state, a repaired
galaxy prediction or a stability proof. The numerical resolution and mixed
clamp-corner limitations remain. No load-bearing defect was found.
