# Fixed-q4 volume and correlation-relaxation screen V001

2026-09-27. New analytical consequence of the resident q4 definitions; no
numerical run, source alteration, remote action or transfer to BS/owner-once.
This tests an **adopted** information-to-spatial-metric interface. It does
not derive that interface, physical time, gravity or a cosmological history.

## Resident evidence and exact operational ceiling

File flags were checked before reads. The EW pair-memory theorem, its
verifier and GL6T theorem/ledger were dataless and were not read or hydrated.
The following resident evidence was read without executing its verifiers:

- EW `INDEPENDENT_HOSTILE_AUDIT.md`, SHA256
  `71c4529413a66ebc657709807643486089a058cf0e84a7964ae153aa4da93984`.
  Sections 2–3 attest four binary variables s_a, contrast X=Ps on
  V=1-perp, pair statistics s_a s_b, a minimal nine-parameter exponential
  family, and F=Cov(X) with F(0)=I_V. Finite pair parameters at theta=0
  give full support, zero single-port means, and a rank-six derivative
  partial_(J_ab)F|_0=v_a v_b^T+v_b v_a^T, v_a=P e_a. The resulting inverse
  function theorem is local. Section 5 leaves physical soldering, time,
  shared-edge gluing, stress and gravity open. This is resident audit
  testimony about the old packet, not a fresh replay of its unavailable bytes.
- GL6T `verify_lineage_gated_q4_e2_response.py`, SHA256
  `7185eeb5867aa8d0225aadc828c272f30e4c6ae4281ec2fe28c319579c1a374d`.
  Resident source checks the factorized response
  D=-8hx I_6-4hxz^2 A_L and its A1/E2/T2 sectors. Its supporting theorem
  and dependency evidence were not replayed.
- GL6U `THEOREM.md`, SHA256
  `3f23084cd7e5fa500d331c6e9739b6f0b3e7875bdce3b33f5369eafd54bc7965`,
  and `verify_degree_interaction_q4_response.py`, SHA256
  `7da9c7b02ddec845b952ce42410bda39df3b8af8977b6a380d6b5f73389b7419`.
  U04 gives H=-h sum X_a+Delta d+U_d[(d-dstar)^2+
  sum_a(n_a-dstar)^2], with n_a=(1-Z_a)/2. U06–U10 give an exact
  five-state symmetric reduction. U11–U13 define the double-commutator
  response D=-8hx I_6-4hy A_L, with y=<X_1 Z_2 Z_3>, and eigenvalues
  -8h(x+2y), -8h(x-y), -8hx. The retarded entrance slope is D/hbar^2.
  The theorem explicitly does **not** establish a physical six-source
  dilation, normalized two-time kernel or same-query metric calibration.

Thus a six-dimensional response D is not the three-dimensional covariance
metric F, and full rank of D does not identify a metric evolution. GL6U's
generally nonzero z also prevents identifying its native state with EW's
zero-mean theta=0 family just by sharing four binary labels. The bound below
needs only the displayed covariance definition; applying it as geometry to
any other parent still requires that parent's explicit operational map.

## 1. A sharp finite-cell bound beyond the old tangent theorem

Put P=I_4-11^T/4, m=E[s], S=sum_a s_a and F=Cov(Ps)|_V. For **any**
joint distribution of four values s_a in {-1,+1},

    tr_V F = 4 - ||m||^2 - Var(S)/4
           = 4 - E[S^2]/4 - ||Pm||^2 <= 4.

This follows from s^T s=4 and P^2=P, not from a continuum limit. F is
positive semidefinite. The arithmetic/geometric mean inequality for its
three eigenvalues gives

    det F <= (tr F/3)^3 <= (4/3)^3.

For finite full-support parameters of the EW family, F is positive definite
and tr F<4, because states with S!=0 retain positive probability. Both upper
bounds are then strict. The supremum is sharp: the uniform distribution on
the six S=0 configurations has m=0, F=(4/3)I_V. In the zero-field family it
is approached by an equal antiferromagnetic pair parameter tending to minus
infinity. This is a mathematical boundary distribution, not a free physical
preparation or evidence that the native dynamics reaches it.

Now explicitly **adopt** g=ell_F^2 F as a spatial metric in a fixed reference
coordinate frame, with fixed positive information-to-length ruler ell_F.
Its metric volume density is nu=ell_F^3 sqrt(det F). Relative to the uniform
reference F_ref=I_V,

    nu/nu_ref <= (4/3)^(3/2),

strict for the finite full-support family. Under isotropy the corresponding
linear-scale bound is a/a_ref<=sqrt(4/3). Local rank-six surjectivity does not
contradict this finite-range constraint; it guarantees only a neighborhood.

**Essential scope:** this is not a universal bound on cosmological e-folds.
For an arbitrary positive initial F_i,

    nu_f/nu_i <= sqrt[(4/3)^3 / det F_i].

An initially near-collapsed metric can therefore permit a very large finite
expansion ratio. The fixed cell has no positive state-independent lower
volume bound. Enlarging the cell system, changing ell_F or changing the
metric prescription is also outside the fixed-cell premise and needs its
own rule. No restriction on those alternative constructions is proved here.

## 2. Finite-path integrability and what it does not say

Along a differentiable positive-definite path in this family,

    Theta_F := d ln nu/dt = (1/2) tr(F^(-1) dot F)

for fixed ell_F. Therefore its time integral is exactly the endpoint
quantity (1/2) ln[det F_f/det F_i]. A loop returning to the same F has zero
net metric-volume change. On the specified instantaneous statistical family,
the corresponding parameter-space volume one-form is exact; a closed loop
of its full parameters cannot accumulate extra volume by path choice.
This says nothing about dissipated work or a history-dependent state outside
that family. If ell_F varies, add 3 dot ell_F/ell_F to Theta_F.

From F_ref=I, an interval with Theta_F>=Theta_min>0 has duration at most
(3/2)ln(4/3)/Theta_min under the fixed-cell premises. There is no analogous
bound on instantaneous rate, repeated expansion/contraction, or arbitrarily
long expansion whose rate tends to zero. This is an endpoint kinematic
constraint, not a dynamical no-go or an operational clock calibration.

## 3. A precise isotropic relaxation test

For a permutation-symmetric law, write E[s_a s_b]=c and E[s]=m0 1. The
contrast covariance is F=(1-c)I_V. This holds even for m0!=0, because the
uniform mean vector is projected out. Equal pair moments without that mean
condition would not alone suffice. The binary-label
constraint gives -1/3<=c<=1; c=1 is metric-degenerate. For fixed ell_F,

    a proportional to sqrt(1-c),
    H_a = dot a/a = -dot c/[2(1-c)],
    ddot a/a = -ddot c/[2(1-c)] - dot c^2/[4(1-c)^2].

Here dots refer to one specified time. They represent cosmological proper-
time acceleration only if the clock/lapse identification is separately
supplied; a time reparameterization can change an apparent acceleration.

As a **prospective law to screen**, take ordinary single-exponential decay
c=c_inf+A exp(-gamma t), with A,gamma>0 and the entire interval inside the
allowed range. It gives dot a>0 but ddot a<0. It cannot supply accelerated
expansion under the stated fixed-ruler/proper-time interface. More generally,
acceleration requires

    ddot c < -dot c^2/[2(1-c)].

Neither EW nor the GL6T/GL6U diagnostic supplies this correlation law or a
proper clock. This result rejects only a proposed exponential-relaxation
completion of the adopted metric, not q4, the network program, or a different
microscopic response. A changing ruler, cell law or lapse cannot be used as
an unlogged correction after this restricted completion is scored.

## Decision and cheapest next use

The new result is a sharp finite-range/endpoint test and a conditional
acceleration discriminator, not another tangent-rank calculation. Before a
new run, ask any proposed q4 completion to state its actual c(t) or F(t),
initial metric, clock, fixed or dynamical ruler, and how cells are counted
and glued. Check the displayed identities analytically. Do not identify the
known pair-source response with dot F or infer a pressure from it. No new
numerical calculation is needed for these checks; microscopic work/stress
and a physical metric calibration remain separate load-bearing claims.
