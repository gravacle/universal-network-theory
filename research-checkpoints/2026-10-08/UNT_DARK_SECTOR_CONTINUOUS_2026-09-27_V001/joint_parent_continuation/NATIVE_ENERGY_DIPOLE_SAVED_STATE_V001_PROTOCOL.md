# Energy-dipole discriminator on saved states: prospective V001

2026-09-30. Root-only execution after independent source review and freeze.
This is a SAVED-STATE arithmetic discriminator, not a new physical propagation,
eigensolve, state preparation, spectrum fit, or observational validation.

## Fixed inputs and census

Use precisely the authenticated A/B autonomous-volume result: models A/B,
endpoints minus/plus, and its five saved times0,.01,.02,.04,.08. All20 full96D
vectors are mandatory. Never select an age because its response sign is useful.
The input must have successful conditional-apparatus status, no failed checks,
all physical-promotion flags false, and matching payload/freeze/source hashes.
No producer module is imported or executed. Native and apparatus matrices are
independently assembled by basis-row rules, not loaded as executable code.

The analysis adopts precisely the reviewed bridge's weak-lapse/embedding and
controller-localization premises. It does not derive those premises or close
the ambiguity in full physical metric contacts. All responses are normalized
symbolically by gamma0=ell0/(2c^2); no numerical physical ruler, c, G, a0,
vacuum density or astronomical datum is inserted.

## Independent operator construction

Basis index is Q*32+C*16+rL*8+rR*4+a*2+c. Native n=a, P_L=1-c, P_R=c.
For v=L,R independently assemble the16D local held energy:

    h_v=(n-1)^2+P_v+q_v+2n-(1/2)Xa-(1/4)n Xc
                         +(1/4)n P_v-(1/2)n q_v.

The local full transport is T_v=-(1/4)n Xc+(1/4)n P_v. Include the onsite
formation interaction g Pc X_v at its own endpoint, g=1. At each Q label,

    h_v,A=s^-1(h_v+Pc X_v),
    h_v,B=h_v-T_v-I+s^-1 T_v+s^3 I+Pc X_v.

The two baseline halves sum to the original Eb=2. HQ is the three-site
positive Laplacian with J=1, HC=I-X_C, and both controller energies are placed
at the midpoint for the adopted lapse-gradient source. Confirm
H=HQ+HC+h_L+h_R against the SAVED full Hamiltonian for each model. Record the
local matrices and source/contact matrices so saved-only review remains possible.

Set S=diag(s) on Q, D=h_R-h_L, Ztilde=S D=Z/gamma0. Independently check

    Ztilde_A=D0,
    D0=(1+n/4)(P_R-P_L)+(1-n/2)(q_R-q_L)+Pc(X_R-X_L),
    Ztilde_B=(s+n/4)(P_R-P_L)+s(1-n/2)(q_R-q_L)+s Pc(X_R-X_L).

Check [HQ,Ztilde_A]=0 as bare source-Q independence, not independence of
A's response or formed states. For the B mixed contact, at fixed state,

    C_aeta/gamma0=Ztilde_B-n(P_R-P_L)/4,
    C_aetaeta/gamma0=C_aeta/gamma0.

A's mixed contact is zero. In this EXACT affine apparatus-source family
C_aa=0; this is not a derived statement about missing physical O(a_ext^2)
metric/seagull/boundary terms. Retain common multiplicative uniform lapse
L_v=L0[1+a_ext x_v/c^2], H(L0,a,eta)=L0 H(a,eta), complete controllers included.

For dilation eta, hold J and Omega fixed as declared apparatus data. Use

    B_eta,A=h_L,A+h_R,A, C_etaeta,A=B_eta,A,
    B_eta,B=s^-1 T-6s^3 I, C_etaeta,B=s^-1 T+18s^3 I,
    p_normalized=B_eta/(3 V/V0).

The pressure is in energy-unit/V0 units; no SI volume is assigned.

## Readouts and necessary matching discriminator

At every saved state report full-state means of Ztilde, B_eta, p_normalized,
C_etaeta, C_aeta/gamma0 and n. Report the complex connected Gram matrix for
(Ztilde,B_eta,n), its symmetric real covariance and equal-time commutator
response. No products of separately averaged native/controller operators
replace correlations.

The stored equal-time minus-source matrix is chi_AB=i<[A,B]>=-2 Im Gram_AB
at hbar=1. It is the convention for H=H0-f B. The physical acceleration
source here has H=H0+a Z, so its response uses MINUS chi_AZ; explicit output
metadata retains that sign. No complete two-time kernel is evaluated here.

The primary signed moments, with hbar=1 inherited, are

    S_Z/gamma0^2=<[Ztilde,[H,Ztilde]]>,
    S_n=<[n,[H,n]]>=<s^-1 Xa> for A, or <Xa> for B.

The latter is a separate diagnostic incidence source and is NOT gravitational
response. Evaluate each double commutator both as an operator and through
2(<B H B>-Re<B^2 H>). Check the algebraic initial S_Z=0 for each actual
endpoint/blank/C-on preparation. This null already prevents identifying the
ENTIRE preparation history with one nonzero strictly positive, fixed-inertia
source moment. Later positive moments are necessary, not sufficient, for a
passive mechanical identification; neither stationarity nor positive spectral
weights follows from this moment. Preserve all negative/null values.

No desired sign is a numerical pass condition. Raw signs and a separate
roundoff-resolution classification (positive/negative/unresolved within the
declared2e-10 arithmetic gate) are both retained. Report all-time minima,
maxima and changes descriptively; do not fit a common mass or select a favorable
formation age. A signed first moment is not the galaxy force or a prediction
that dark matter or dark energy has been replaced.

## Ward and conservation controls

For the four energy pieces (HQ,HC,hL,hR), construct J_uv=i[E_u,E_v]. Check
antisymmetry, sum_u J_uv=i[H,E_v], and vanishing sum of energy derivatives.
The moving physical ruler cannot be omitted from the energy-dipole derivative:

    Ztilde_dot=(1/2){S_dot,D}+(1/2){S,D_dot},
    S_dot=i[H,S], D_dot=i[H,D].

Check this against i[H,Ztilde] as an operator and save both contributions at
each state. Even for A, source-Q independence results from cancellation of
these Q-dependent terms, not from discarding controller energy currents.
Check Gram Hermiticity, its defining centered-vector construction, diagonal
nonnegativity within roundoff and pairwise Cauchy-Schwarz; do not run a Gram
eigensolver or advertise these pairwise checks as a full new spectral test.

## Frozen arithmetic/resource/custody contract

All operator, reconstruction, norm, moment, Ward and covariance identities use
2e-10*max(1,maxabs(actual),maxabs(expected)); initial-null and positivity
roundoff gates are absolute2e-10. This conservative double-precision allowance
for96D products/double commutators is inherited from the reviewed apparatus
coefficient gate; it is not chosen from this discriminator's result. No
threshold is an observational tolerance. Failures are retained, not clipped.

One process, all numerical-library threads1; CPU30s, elapsed60s, self-RSS256MiB,
maximum4096 checks. No exponentiation, eigensolve, ODE, fit, propagated state,
new source pulse, installed software or network call. Process CPU bound and
between-operation elapsed/RSS guards apply; exact external wall interruption
belongs to the root supervisor. The source's only numerical matrix operations
are assembly, products, commutators and expectations on the20 owned vectors.

--freeze exclusively publishes a new manifest of protocol/source and all input
hashes. --run verifies the manifest, original result payload and original
freeze/file identities. The optional --output is restricted to the fixed
previously absent NATIVE_ENERGY_DIPOLE_SAVED_STATE_V001_RESULTS.json; without
it the full result is printed. Preserve partial evidence on technical errors.
No frozen input/result is overwritten. Root alone runs the script after review.

All physical-promotion flags remain false: native metric derived, physical
source independently validated, continuous soft spectrum established,
passive mechanical mapping qualified, initial galaxy polarization generated,
vacuum normalization predicted, observational success, and Stage3 completion.

## Resident identities

The companion source pins the exact original result
bc35b592f5547e1f5fc566411ec7e8f7175776d20569fbccf0ae3e6457e74fc1,
original freeze642348d737439d2b87f2abb0f7d0a499955409745554f1bf85cb5b9937474d12,
bridge81b3c455d761667e2645117699e8986c7030290de8b54bc45879112237d2db96,
and every primary/model-source dependency. Current protocol/producer hashes
are added by the root's exclusive prospective freeze, without a circular
self-hash embedded in either authored file.
