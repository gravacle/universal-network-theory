# 0411 — Codex2 return for dispatch 0436

**Verdict: PASS_SCOPED.** All three identities follow within the declared effective hydrostatic/Euler branch, assuming K>0, constant gamma, smooth radial dependence, and a regular connected support. This is an algebraic review of the supplied definitions, not an implementation/hash verification. No numerical execution/imports or data-array reads.

Write κ=K'/K and take every radial partial derivative at fixed physical z. From h=gamma K rho^(gamma−1)/(gamma−1),

$$
h_R=h\kappa+(\gamma-1)h\rho_R/\rho,
\qquad P_R/\rho=(\gamma-1)h\rho_R/\rho+
\frac{\gamma-1}{\gamma}h\kappa
=h_R-\frac h\gamma\kappa.
$$

The assumed radial Euler balance R Omega²=Phi_R+P_R/rho and h_R=C'−Phi_R therefore give

$$R\Omega^2=C'-\frac h\gamma\kappa.$$

Also,

$$
\rho_R=\frac{\rho}{\gamma-1}
\left[\frac{C'-\Phi_R}{h}-\kappa\right].
$$

Leibniz differentiation of Sigma=integral from z_−(R) to z_+(R) of rho dz adds rho(z_+)z_+'−rho(z_−)z_−', which vanishes at regular vacuum surfaces. Thus, with A=integral rho/h dz,

$$
(\gamma-1)\Sigma'=C'A-\int(\rho/h)\Phi_R\,dz-\kappa\Sigma,
\qquad
C'=\frac{(\gamma-1)\Sigma'+\kappa\Sigma+
\int(\rho/h)\Phi_R\,dz}{A}.
$$

For gamma=5/3, rho is proportional to h^(3/2), so rho/h is proportional to h^(1/2), tending to zero at a simple surface and integrable there. For a nonempty finite regular column A>0. Both C' and R Omega² have acceleration units; h has velocity-squared units and κ inverse-length units.

If only the midplane-referenced potential is used, Hc=C−Phi(R,0) implies **C'=Hc'+Phi_R(R,0)**. The midplane radial term cannot be dropped. Omega can depend on z when κ is nonzero; columnwise hydrostatics does not impose cylindrical rotation.

At a nonsimple/tangent surface, the root derivative or support topology may cease to be regular; the vanished endpoint term alone does not justify differentiation under the integral. Establish differentiability/integrable domination separately. Preserve negative Omega² as a failed stationary branch, never clip it. No equilibrium, calibration, or native-origin claim follows from these identities alone.
