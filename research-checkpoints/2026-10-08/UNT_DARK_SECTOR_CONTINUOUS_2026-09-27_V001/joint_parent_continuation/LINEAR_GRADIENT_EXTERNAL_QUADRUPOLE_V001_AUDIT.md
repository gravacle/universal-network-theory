# Linear gradient-parent quadrupole: independent audit

2026-10-04. **51/51 checks pass**, runtime 0.031 seconds. No producer was imported, no physical field equation was solved, and no parameter was fitted. Frozen source/protocol hashes, all 12 saved controls, saved refinement/qualification arithmetic, sensitivity labels and SI conversions agree. Original files remain unchanged; the numerical slot was released after the audit.

## Coefficient and independent calculation

The saved qualified coefficient is

    Cq = 0.16358956064579733,
    Q2_lin = Cq GM/ell^3.

An independent calculation gives the truncated integral `0.16358954953991905`, differing by **6.79e-8 relative** from the saved value. Its positive omitted tails have analytic bounds `1.4257904324e-9` (ultraviolet) and `1.6482068232e-22` (infrared). These differences are well within the original `1e-3` numerical qualification gate. The saved coefficient and receipts are retained rather than replaced by an audit estimate.

The audit changes all three integration representations:

1. Let `g=ge/gc`, and obtain `t0+t0^3=g` by Newton iteration. Substitute `z=t0/t`, so the spectral weight is

       2s ds -> [(1+t0^2) z^2(z^2+3t0^2)/(z^2+t0^2)^2] dz.

   This removes the fractional-power soft-endpoint behavior of the original s integral. The weight and its first moment were checked at 96/192/384 nodes.

2. Integration by parts gives the strictly positive angular representation

       -I2 = (2 beta/KT) integral_0^1
                    u^2(1-u^2)/(1+beta u^2)^2 du.

   It uses neither subtraction of two nearly equal kernels nor subtraction of large angular terms. It reproduces the small-anisotropy coefficient `-I2 = 4 beta/(15 KT)+...`, vanishes exactly at isotropy, and passes 32/64-point refinement.

3. Integrate in `log q` on `[-16,20]` with composite Gauss rules of order 8/16 per unit interval, rather than the producer's `q=x/(1-x)` map. The independently varied calculations agree to about `2e-14` relative on the truncated interval. This is numerical convergence evidence, not a rigorous roundoff enclosure.

## Infinite-tail control

The first continuum spectral moment is available exactly:

    M2 = integral_0^1 2s t(s)^2 ds
       = g [2 atan(1/t0) + t0/(1+t0^2)]
       = 4.074707877780128  (primary external field).

Using `KT >= q^2/(1+q^2)` and `KL-KT <= 2 M2/q^4`, the missing ultraviolet contribution to Cq obeys

    tail_UV <= 8 M2/(15 pi)
               [1/qmax + 2/(3 qmax^3) + 1/(5 qmax^5)].

For the infrared, `KT >= t0^2/(1+t0^2)` and `KL-KT <= 1` give

    tail_IR <= 4 qmin^3/[45 pi (t0^2/(1+t0^2))^2].

These are continuum truncation bounds, independent of a finite spectral-node asymptotic test. Combining them with the displayed finite quadrature values is not advertised as a certified floating-point interval. Higher spectral moments need not converge, so a uniform higher-order inverse-q Taylor series was not assumed.

The two external-field sensitivities independently reproduce the saved coefficients within the same audit tolerance. Their original label remains **individually admissible, not separately refined producer sequences**.

## Fourier normalization, cusp and units

With `phi(k)=-4 pi GM/[k^2 K(k,u)]`, angular projection of `Hzz-Hxx` gives

    Q2 = -(Hzz-Hxx)
       = -GM/(pi ell^3) integral q^2 dq integral P2(u)/K du.

The Fourier prefactor, sign and angular projection are correct. At large q, `K^-1=1+q^-2+O(q^-4)`: besides the Newtonian point singularity, the local potential contains the isotropic cusp `+GM R/(2 ell^2)`. That cusp must be removed before an origin Hessian is defined. Its angular quadrupole vanishes; the remaining projected integral converges. This is not permission to differentiate the un-subtracted point-source potential as a smooth function at the origin.

The saved 1 pc illustration is correctly `7.3895090342433345e-31 s^-2`; 10/100 pc scale as `ell^-3`. Parsecs, GM and `rM/ell` agree. The chosen lengths are illustrations, not inferred parameters.

## Scientific ceiling

This audit confirms the **linearized external-equilibrium Green coefficient** of the explicitly changed linear-source gradient model. It does not prove that linearization controls the central Solar field or arbitrarily soft modes, that a finite source matches this exterior, or that the full nonlinear theory passes Cassini. The isolated monopole plateau and this external linearized quadrupole cannot be combined into a full Solar prediction without nonlinear matching. No previous galaxy score, cosmological success, native formation law or response-time calibration is inherited by this calculation.

Audit JSON: `LINEAR_GRADIENT_EXTERNAL_QUADRUPOLE_V001_AUDIT.json`, SHA256 `1d7d615ac64091c8d79a02086a9d9fcda830cb3e083cb129788c8025c6d6555b`. All audit/source/result hashes and detailed checks are retained there.
