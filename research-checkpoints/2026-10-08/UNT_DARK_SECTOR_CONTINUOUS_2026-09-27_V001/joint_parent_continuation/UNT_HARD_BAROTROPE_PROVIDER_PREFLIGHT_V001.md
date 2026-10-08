# Independent inert hard-barotrope provider preflight

Accepted after full read of header, C source and protocol. No compilation, import, quadrature, inversion, CLASS or physical producer was executed.

- Header `unt_hard_barotrope_v001.h`: `abfade89af77e4000bccd169c1ea18226315621f7dcb665901efa879e3a4aab6`.
- Source `unt_hard_barotrope_v001.c`: `3003b89d4dcd14a599cf924390b6b4a2151bb14e4221a2336458d89509a3c39d`.
- Protocol `UNT_HARD_BAROTROPE_PROVIDER_PROTOCOL_V001.md`: `308c605954106d70b7376b5665ae2ed2b47725b4a10b663509089ebf539a567a`.

The normalization I=R^3 f(r), e=R^4(r/2+r^2/4), omega/R=pi/(2j) and both positive action/period integrals agree with the retained zero-source quartic. The mapped GL weight is pi/[2(1-z^2)P_n'(z)^2]; both roots and total pi/2 normalization are checked. Kahan sums, paired angular endpoints and the independent prospective Simpson/saved-state checks are appropriate; GL64 versus GL128 alone is a resolution test, not an independent method.

The inversion bounds are valid. From f>=r/2 and f>=r^(3/2)/(2sqrt2), r_hi=min(2i,2i^(2/3)); with r_lo=r_hi/4, f<=r sqrt(1+r)/2 gives a strict lower bracket on either side of i=1. The implemented log-coordinate margin and safeguarded Newton slope 1+beta/2 preserve that bracket and require the actual log-action residual, not just a narrow interval.

Pressure w=r<M4>/(2+r) and trace 4<M2>/(2+r) avoid cancellation. For the two normalized weights the ln(b) derivatives alpha_dot=2<t(1-t)>_P−Var_P(t), beta_dot=2<t(1-t)>_A+Var_A(t) give exactly the coded derivative of ca2=alpha/(2+beta). The conversion to ln(a) multiplies by −3/(2+beta) where appropriate because I proportional a^-3. Consequently all conservation derivatives, rho_lnln=9(rho+p)(1+ca2), w_ln and ca2_ln have the stated signs/factors. Dust is explicitly separate, not chosen by a small-pressure threshold; undefined orbit coordinates must be serialized as labeled nulls by its later harness.

The saved unweighted R,I1,e1 anchor is retained. The constructor reports and gates reconstructed/saved energy disagreement at 2e−10; normalizing density by the same quadrature-consistent reference makes rho(1)=rho1 exact. This disclosed numerical normalization is not a new physical abundance fit. The caller must not multiply the supplied present physical density by beta again, nor treat the diagnostic 3p and rho−3p split as independent fluids.

The stress and conformal-length RHS helpers reproduce the Q=0 barotropic equations with the provided metric continuity/Euler factors. They neither impose Phi=Psi nor solve the metric or initial constraints. The exact cancellation of the usual gauge/rest-frame entropy correction relies on cs2=ca2 and on the selected Q=0 branch. The matched vacuum and ordinary species remain separate.

The implementation has no I/O, process calls, heap allocation, mutable cache or CLASS dependency. Explicit finite arithmetic/slice failures must be retained, not replaced with a dust approximation. No load-bearing source defect was identified. This acceptance concerns the standalone material algorithm and conditional interface only; the prospective root-owned numerical harness and the separately enumerated CLASS initial-state, thermal and stress integration changes remain unexecuted/unqualified.
