# Independent source review: consistent-inertia state maps

Verdict: **PASS for the inert helper and prospective integration design only**. Reviewer `short_path_adversarial` read both files completely, compared the old force/ledger/error-chart implementation and the exact kernel, and performed algebraic checks. No import, numerical execution, trajectory or new producer was run.

Reviewed source: `spherical_consistent_state_maps_v001.py`, SHA `483ebdcb7fc66532911d6a9eac0eece4e29c3fff2eef063dd397ea31193e2dc4`. Reviewed design: `SPHERICAL_CONSISTENT_SOLVER_INTEGRATION_DESIGN_V001.md`, SHA `a3fc53447b520650b44c5ad16e135745c1c14aefcbf78bf592cfc3d98e135413`. Kernel ancestry remains `spherical_exact_kinetic_v001.py`, SHA `78765ef0e2d29c044642b1d944682a81ff5d48b22de9d0cb16b7bc47b9c7e11a`.

The implemented shell derivative follows `delta M=m F'(q)(delta L-q delta R)/R`. In particular, expanding the previously reviewed factored quadratic contraction gives the off-diagonal factor `(9/5)q(1-q)(1+5q+5q^2+q^3)/(1+q+q^2)^4`, as implemented. The constrained origin contributes constant `3m/5` and zero directional derivative.

From `p=A M v`, the complete peculiar acceleration is `M^-1(f+g)/A - M^-1 Mdot v - H v`, with `Mdot=M'[v/A]`. The code uses those factors and separates named physical responses from geometry, moving inertia and Hubble terms. It does not mislabel an isolated physical kick as a total acceleration. The canonical equation `pdot=g+f` has no extra momentum drag; geometric canonical work cancels the fixed-p geometric derivative of kinetic energy. The old gravity and outer-traction pressure kicks and physical work meanings are preserved by the design.

Each nonlinear error chart uses that state's own mesh and scale factor, and compares actual high- and low-order states. Its last-three hard-ledger normalization matches the old producer; the remaining coordinates are unweighted physical position/velocity variables. No fixed face-mass scaling survives. Kinematic invalidity raises rather than being silently converted into a successful accuracy retry.

This is not review of a complete trajectory driver or empirical verification of the new directional-derivative code. The future producer still needs explicit source authentication, inherited physical/domain guards at every attempted stage and endpoint, retained failed attempted states, the declared nonzero-momentum controls, bounded serial runs and unchanged numerical comparison criteria. The method-name API check alone is not source custody.

The dense inverse-inertia issue is correctly kept distinct from physical superluminality. The proposed old step ceiling has no new CFL proof; finite stage checks do not certify no crossing between stages, and an acoustic travel diagnostic does not establish a strict finite-grid domain of dependence. No continuum, formation, observation or dark-sector qualification follows from this source-level PASS.
