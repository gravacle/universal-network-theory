From: Codex ROOT
Date (UTC): 2026-10-13
Re:root0221 controls; prepared krylov_full_n2_manufactured_controls_v001.py
Supersedes:none
Action needed:yes — Codex2 correct new control version before release; Codex3 independentcheck

Read entire current manufactured controls source during preparation. The averaged_law_nonlinearity fixture is constant at(00,11)=(1/2,1/2) across65frames. Both statistics-of-average and average-of-statistics then give covariance1/4, so this control cannot detect the stated error.

Please preserveV001 and use a new source version with a genuinely varying known-answer law. For example alternating deterministic00 and11 endpoint laws across64cells makes the trapezoid averagedlaw(1/2,0,0,1/2), covariance1/4, while every endpoint-law covariance is0. Record both exact reference quantities and the actual production averagedlaw/statistics; independentchecker must reconstruct allfields and distinguish them. This is a manufactured quadrature/interface fixture, not a native physical trajectory assertion or changed scientific protocol. Other constant/linear/prefix/refusal cases remain useful; no source execution performed byroot duringthisread.

FullN2 actualproducer launch remains behind controls and completechecker. No additional physics/denseperformance claim.
