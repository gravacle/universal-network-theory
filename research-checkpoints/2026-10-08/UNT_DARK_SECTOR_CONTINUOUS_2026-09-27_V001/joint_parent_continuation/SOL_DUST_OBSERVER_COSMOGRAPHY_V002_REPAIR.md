# Retain V001 and refine only its four failed angular gates

2026-10-05 UTC. V001 is permanently FAILED:27861/27865 controls passed.
Only qeff and q RMS changes for T1000000,r=7,t=tmax,phases7 and9 missed
the frozen2e-7 tolerance. This protocol is frozen before repair arithmetic.
No state, eligibility criterion, observer weighting or tolerance is changed.
The other states and their original coefficients are reused, not rerun.

These near-small-H directions require better angular integration. Remove
azimuth quadrature error analytically. At polar mu=n3,

    Hn=A+B cos(2phi), D=(A-B)(A+B)>0,
    I1=<1/Hn>=D^-1/2, I2=<1/Hn^2>=A D^-3/2,
    I3=(2A^2+B^2)/(2D^(5/2)),
    I4=A(2A^2+3B^2)/(2D^(7/2)),
    J2=<cos(2phi)/Hn^2>=-B/D^(3/2),
    J3=-3AB/(2D^(5/2)),
    J4=-B(4A^2+B^2)/(2D^(7/2)),
    T4=<cos^2(2phi)/Hn^4>=A(A^2+4B^2)/(2D^(7/2)).

Decompose Epp_even=L+M cos(2phi), G=N+O cos(2phi). L,M are even in mu;
N,O are odd. The antipodal cancellation is exact. Then

    qeff=<L I3+M J3-3 I1>_mu/<I1>_mu,
    <q>=<L I2+M J2-3>_mu,
    <q^2>=<(L^2+N^2)I4+2(LM+NO)J4+(M^2+O^2)T4
             -6(L I2+M J2)+9>_mu.

Use512 and1024 Gauss-Legendre polar nodes, only for the two implicated
observer rows. Require normalized changes in Heff,qeff,q RMS<=2e-7 as
originally fixed. Control all eight azimuth identities against8192 uniform
azimuth samples at mu=0,.3,.9 for those rows, to1e-10 normalized error;
check Heff eigenvalue bounds and parity at1e-10. Verify the original canonical
seal, original source/input hashes and exact list of four failed gates.

Write a separate repair receipt with the old raw hash, source/protocol
hashes, refined rows and controls. The V001 raw data/status remain unchanged.
A combined result is qualified only if all replacement and new controls
pass and all original non-replaced controls pass. This is an arithmetic
repair, not a favorable physical criterion or new cosmological observation.
