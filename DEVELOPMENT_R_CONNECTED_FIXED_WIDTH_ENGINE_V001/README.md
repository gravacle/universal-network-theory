# Connected fixed-width engine V001

This target validates a guarded fixed-width implementation candidate on the
sealed L4/L6/L8/L10 histories before any L14 allocation. It constructs the
complete finite orbits with compiled chunk-permutation tables, stores one
unaggregated transition per active owner-once edge, and obtains the two raw
representative current expectations from signed finite edge-orbit sums.

The engine must reproduce all sealed occupations and oriented currents. Its
current reduction is an operator calculation in the already-declared finite
support; it does not insert a continuity equation, grid, or Ward axiom.

The validator must finish with
`PASS__R_CONNECTED_FIXED_WIDTH_ENGINE__40/40` and preserve canonical
`RESULT.json` within `5e-9`. The engine is not authorized for L14 use until
this packet passes independent hostile audit.
