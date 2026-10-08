# Independent operational-ruler review V001

2026-09-29. Reviewed the complete `SUBDIVISION_OPERATIONAL_RULER_V001.md`, SHA-256 `9d42618e853336a12b534b6eaef779abf94e9e092dd5924e1e1405e565f6c10d`. Outcome: **analytically accepted, no correction required.** No numerical worker was used.

The harmonic interior equation gives exactly `Lambda=K_BB-K_BI(K_II-omega² M_I)^(-1)K_IB`, excluding boundary inertia only because the note accounts for it separately. For the three equal segments, the two internal eigenvectors give poles at `c_s/mu` and `3c_s/mu`, visible respectively to symmetric and antisymmetric endpoint forcing. Static matching at `c_s=3c` does not remove either accessible pole.

Inserting the exact static interpolation of the two interior coordinates into their kinetic energy yields `M_added=(mu/9)[[5,4],[4,5]]`. Its eigenvalues are `mu` and `mu/9`; endpoint diagonal-mass changes cannot cancel its off-diagonal term. With the note's positive S, the spectral inequality `S²/(1-omega² S) <= S/(omega_D²-omega²)` verifies the resolvent error bound (6) below the first Dirichlet pole.

The discrete sine spectrum, acoustic scaling and continuum-refinement limits in (7)–(10) follow from the stated local mass–spring action. Holding segment stiffness/inertia fixed stretches a calibrated route; rescaling stiffness alone preserves static conductance but changes timing; preserving a fixed continuum interval requires repartitioning the kinetic measure and boundary weights as well. These are experimentally distinguishable assignments on the same graph, not three native derivations.

At fixed canonical momenta, differentiating `pi²/(2mu)` gives the negative kinetic contribution in the coefficient-work formula (11). New-coordinate preparation, coupling changes and possible clock changes therefore remain in the energy ledger. The result is a useful operational test of expansion versus refinement, without identifying graph count with physical volume, supplying a cosmological formation rate or promoting the declared scalar probe to native photons.
