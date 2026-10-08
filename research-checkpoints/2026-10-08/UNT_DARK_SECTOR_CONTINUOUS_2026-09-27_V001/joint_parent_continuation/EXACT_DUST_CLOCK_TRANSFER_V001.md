# Exact ordinary dust and its optical potential

2026-10-05 UTC. Analytical continuation of ORDINARY_MATTER_CLOCK_ACTION_V001.
Root and endpoint_equations_check derived and checked the dust reduction.
No division by zero sound speed, extra homogeneous dust, or data fit.

## Direct constrained material, not a singular numerical limit

For c=1, use ordinary dust S_d=-(1/2) integral sqrt(-g) varrho
[(partial chi)^2+1], with chi_background=t. Its linear norm constraint
is n=v_dot. A term r(v_dot-n)^2 in its unreduced expansion vanishes exactly
on that constraint. For constant unfiltered beta trace let

    F=1+3beta/2, A=3+2/beta=2F/beta, t_beta=2/beta,
    p=k/a, f=(1+ell^2 p^2)^(-1), g=f^2p^2,
    r=varrho_background/(2M^2)=-F H_dot.

After eliminating lapse and shift the exact quadratic action is

    L/(M^2 a^3)=A(zeta_dot-Hv_dot+rv)^2-6rv zeta_dot
      -r(p^2+3r)v^2+p^2zeta^2+2p^2v_dot zeta+g v_dot^2.

For x=(zeta,v), L/(M^2a^3)=xdot^T K xdot+2xdot^T B x+x^T C x:

    K=[[A,-AH],[-AH,AH^2+g]],
    B=[[0,t_beta r],[p^2,-AHr]],
    C=diag(p^2,t_beta r^2-rp^2), det K=A g>0.

The equation is K xddot+(Kdot+3HK+B-B^T)xdot+(Bdot+3HB-C)x=0.
The density multiplier on shell is

    d=-HA(zeta_dot-Hv_dot+rv)+p^2zeta+g v_dot
     =delta varrho/(2M^2).

Thus d/r is preferred-slice density contrast, while Delta=d/r+3Hv
is gauge-invariant comoving ordinary contrast. Exact dust has zero pressure;
gravitational growth must not be mislabeled a material gradient instability.

## Cancellation-safe variables and physical readouts

Let s=Delta B_shift/a^2=A(zeta_dot-Hn)+t_beta r v and define

    sigma=s/p^2=-B_shift, theta=v-sigma,
    Psi=-zeta+H sigma, D=r Delta/p^2=f^2 n-Psi.

The zeta equation gives s_dot+3Hs=p^2(n+zeta), so the physical lapse
potential Phi=n+B_shift_dot equals Psi at this scalar order. Hence the
same predicted Psi is the Weyl lensing potential, not an extra fitted one.
The exact four-state system is

    Psi_dot=-H Psi+(r/F)theta-(p^2/A)sigma,
    theta_dot=Psi,
    sigma_dot=f^(-2)D+[f^(-2)-1]Psi,
    D_dot=-HD-r(theta+3sigma/A).

Evaluate f^(-2)-1=2(ell p)^2+(ell p)^4 directly. Reconstructions are

    zeta=-Psi+H sigma, v=theta+sigma,
    n=(Psi+D)/f^2, Delta=p^2D/r, delta_N=Delta-3Htheta.

This uses the exact cancellation A H_dot+t_beta r=0, valid because the
constant perturbative trace coefficient matches the homogeneous one.
It is not valid for a k-dependent trace substituted into this system.
The p=0 mode requires separate treatment.

## Physical linearity prerequisite before execution

Small density/metric amplitude alone may not justify this zero-field
quadratic response. The filtered critical restoring coefficient 1-f^2
is small at long wavelength, whereas the deep-MOND constitutive correction
is of order |b|/a0 with b the PREFERRED normal's filtered acceleration,
not automatically c^2 grad Psi. Its linear value is |b|=f c^2 p |n|.

The allowed amplitude must be checked relative to that spatial coefficient
and the full dynamical operator before interpreting a transfer as an actual
cosmic perturbation. A tiny-amplitude transfer can qualify a linear equation,
but cannot be promoted to a finite observed structure or averaged expansion.
The next bounded test will freeze its physical amplitude criterion before
execution. No linear evolution has been run under this note yet.
