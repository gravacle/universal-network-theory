# Independent spectral convention and low-curvature review

2026-09-27. Analytic/source review only; no physics run, source replay, spectrum
fit, remote action or modification of historical files.

**Finding:** the raw determinant ranks are correct, but inserting the raw
volume supertrace directly into RIEHB's negative-prefactor symbol would mix
conventions. Correct reconciliation permits both positive induced Ricci
stiffness and positive vacuum density in this reference benchmark. A separate
pure-shell low-curvature self-consistency test then fails.

## 1. Inputs and primary normalization checks

Resident local inputs inspected:

- FA conformal-selector INDEPENDENT_HOSTILE_AUDIT.md:
  cc6741f3d5fc078396995e8a4431c2084cb102340c934d092bf6f428d2670cb5.
- RIEHB THEOREM.md, particularly IB03, IB06–IB10 and the sign/matching premises:
  e73c077d1402ebab9a6061b060b9b24e9ac323b25809cccc706f4365da7a5e2f.

The original EY files were reported dataless and were not imported or replayed.
The resident FA audit supplies the reference inventory and dictionary
R_R=-R_V. Neither this inventory nor the modes' UNT origin is derived here.

Visser's Table 1 gives (k0,k1)=(1,0) for a conformal real scalar,
(2,-1/6) for a Weyl field and (2,-2/3) for a massless vector. Equations
10–12 account for squaring and insert fermion statistics once. Equations
18–21 use a positive proper-time volume coefficient and an action
-Lambda_V-R_V/(16 pi G); Lambda_V has energy-density units here.
[Primary paper, PDF pages 3–5 and 9](https://arxiv.org/pdf/gr-qc/0204062)

The Weyl rank is two, not one and not four: squaring the first-order operator
does not authorize an extra halving of an already chiral two-component trace.
This concerns the parity-even determinant sector with the required anomaly
and phase treatment; it does not derive a complete chiral parent.

For a gauge-fixed vector, a complex Grassmann ghost contributes twice the
real-scalar heat trace with a minus sign relative to the common half
prefactor. Thus k0=4-2=2, not four and not one. The corresponding coefficients
combine once; adding ghosts again to the already combined massless-vector
table row would double count. Vassilevich's equation 3.53 explicitly gives
a_k(vector)-2 a_k(ghost).
[Primary heat-kernel review, section 3.4](https://arxiv.org/pdf/hep-th/0306138)

Consequently, for the declared 4 conformal real scalars, 45 Weyl fields and
12 massless vectors, with the ordinary statistical sign applied once,

    K0 := str k0 = 4 - 45*2 + 12*2 = -62,
    K1 := str k1 = 4*0 - 45*(-1/6) + 12*(-2/3) = -1/2.

These are reference-spectrum, common massless-shell sums, not the complete
same-parent UNT spectrum, thresholds or matched gravitational coefficients.

## 2. Load-bearing sign reconciliation

Let Delta2=kappa^2-mu^2>0 and Delta4=kappa^4-mu^4>0. Restoring hbar, the
source convention followed by R_R=-R_V gives

    C0 = +hbar K0 Delta4/(64 pi^2),
    CR = -hbar K1 Delta2/(32 pi^2),
    rho_vac = -C0.

The curvature change reverses the Ricci term, not the volume term. This is
why agreement on CR alone cannot authenticate a guessed volume sign.

If the formal RIEHB negative common prefactor is retained,

    C0 = -hbar A0^R Delta4/(64 pi^2),
    CR = -hbar A1^R Delta2/(32 pi^2),

the compatible dictionary is

    A0^R = -K0,       A1^R = K1.

The two A symbols here are convention-matched coefficients; A0^R must not be
labelled the unchanged raw statistical mode rank. Equivalently, the overall
action convention and curvature conversion must both be carried through
the signed coefficient bookkeeping. No freely chosen physical correction
or fitted counterterm is introduced by this dictionary.

For N additional minimally coupled real scalar determinants,

    K0=N-62,               K1=(N-3)/6,
    A0^R=62-N,             A1^R=(N-3)/6,
    C0=-(62-N)hbar Delta4/(64 pi^2),
    CR=(3-N)hbar Delta2/(192 pi^2).

For nonnegative integer N, positive CR and positive rho_vac overlap at
N=0,1,2. Exact raw volume cancellation at N=62 does not retain positive CR
in this narrow common-shell, minimally coupled scalar extension.

### Preserved rejected analytical assignment

The initial proposal set A0^R=K0=N-62 while retaining A1^R=K1 and the negative
RIEHB prefactor. That algebra would require N>62 for positive vacuum density
and N<3 for positive CR. Its empty intersection is mathematically correct
*for that different stipulated sign ledger*, but is not the convention-matched
Visser/EY reference spectrum. It is rejected as a claimed physical benchmark.
This failed assignment is preserved here rather than silently converted into
a purported no-go result. Historical source files remain untouched.

## 3. Independent check of the new low-curvature screen

Now add explicit extra assumptions: source-free stationary leading Einstein
response, pure-shell dominance, the common massless shell above, no cancelling
pre/matching volume term or retained source, and negligible higher-order
remainder. The action convention gives C0=-2 CR Lambda, hence for N=0,1,2,

    Lambda = 3(62-N)/(2(3-N)) * (kappa^2+mu^2).

The source-free four-dimensional Einstein trace is R=4 Lambda. Therefore

    |R|/mu^2 = 6(62-N)/(3-N) * (kappa^2/mu^2+1)
              > 12(62-N)/(3-N).

The strict lower bounds are respectively 248, 366 and 720. They contradict
the RIEHB low-curvature expansion premise for this attempted stationary
approximation. Even in a maximally symmetric realization, where a curvature
component scales as R/12, the required small ratio is absent.

**Accepted interpretation:** this pure-shell two-derivative vacuum stationary
point is not a controlled low-curvature prediction. The calculation does not
solve the high-curvature theory, prove that no full stationary branch exists,
exclude additional matched/retained contributions, or refute UNT. It identifies
the need for parent-owned cancellation, additional physical contributions,
different thresholds/spectrum, or a valid treatment outside this expansion.
Choosing such terms merely to fit the desired cosmology would not derive them.

## Disposition

Accept the standard determinant normalization, corrected convention dictionary
and conditional low-curvature validity test. Reject the initial mismatched
sign assignment as an authenticated reference-spectrum conclusion. Neither
the healthy signs nor the validity failure determines dark abundance,
vacuum magnitude, a physical cutoff, a complete parent spectrum or the
matched total Newton/cosmological coefficients.
