# Independent single-phase characteristic-crossing review V001

2026-09-29. Full analytical read of `SINGLE_PHASE_CHARACTERISTIC_CROSSING_SCREEN_V001.md`, SHA256 `345cb1d3d653e13cfd8779c5a85a28f51c490d5027277a362efbce325d2f1db4`. No numerical producer, EOS quadrature, propagation or new initial preparation was executed.

**Accepted within the stated conditional scalar-fluid and local/interval domains.** No correction requested.

1. The current and Euler equations give the stated relativistic characteristic speeds and invariants. With the opposite invariant fixed, differentiating rapidity plus/minus atanh(sound speed) gives the factor `G=1-s²+dln(s)/dln(I)`. The two-family derivatives both have the positive denominator shown in Eq. (3).
2. The period/action weight differentiation is correct. Writing amplitude-log derivatives, `tdot=2t(1-t)` and the normalized weight derivatives `-(t-alpha)` and `+(t-beta_a)` give exactly the two covariance identities. The inequalities use `t²<=t` and `mean(t²)>=mean(t)²`. They imply `dln(s²)/dln(I)>=-5/8`, and therefore `G>17/48`. This does not need or assert monotonic sound speed.
3. The prescribed simple wave has the other invariant constant. Its right flank is compressive, and the characteristic-map Jacobian is `1+c Lambda'(xi)t`. The derivative of the bump at `xi=L/2` is `-16 exp(-1/3)/(9L)`, giving the stated one-point crossing-time upper bound. The fixed fractional-density cold limit and the separately prescribed converging-dust state are correctly distinguished. A zero-pressure limit alone does not impose a velocity-crossing time.
4. For Eq. (9), if `alpha_x=partial_x r+`, then `D+ alpha_x=-lambda_{+,+}alpha_x²-lambda_{+,-}alpha_x beta_x`. Meanwhile `D+h=h_-(lambda+-lambda-)beta_x`; the selected derivative of h cancels the mixed term exactly. Thus the weighted Riccati identity and its finite-time consequence follow on the compact positive-action invariant rectangle. Neither the vacuum boundary nor coincident dust characteristics are included by that proof.
5. In the planar orthonormal frame, `div(e0)=K1+2Kp` and `div(e1)=a_N+2Lp`. This reproduces Theta_geom. The acceleration projected on the spacelike fluid-normal direction is `Dy+a_N cosh(y)+K1 sinh(y)`, reproducing a_geom. Combining the two equations and dividing by `(cosh(y)±s sinh(y))/N` gives Eq. (10) with exactly the stated minus sign. Its FLRW reduction is `-H(v±3s)/(1±vs)`, not a source-free equation.
6. Differentiating `r+_t+lambda^g r+_x=S` and putting `p=-r+_x` gives

   `D+p=lambda^g_{,+}p²+[S_{,+}-lambda^g_{,-}b-lambda^g_{,x}]p-S_{,-}b-S_{,x}`.

   Hence Eq. (11)'s signs are correct. Integrating the lower comparison equation `pdot=a0(p-p+)(p-p-)` gives Eq. (12)'s logarithm and discriminant denominator. The coefficient bounds must hold on the **actual subsequent interval**; initial metric smallness alone does not supply them.

The finite classical endpoint is a limitation of the specified smooth single-phase evolution, not proof of a gravitational merger exclusion or of immediate density divergence. The note correctly keeps the material Minkowski calculation separate from a self-consistent gravitating state, and explicitly requires new constitutive/state information for a shock, dispersive, multiple-phase or kinetic continuation. No optional duplicate numerical EOS census is required to establish the theorem above.
