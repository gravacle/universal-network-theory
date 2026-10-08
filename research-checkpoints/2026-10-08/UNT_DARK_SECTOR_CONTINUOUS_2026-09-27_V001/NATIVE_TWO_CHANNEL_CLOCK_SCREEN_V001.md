# Native two-channel clock and probe-calibration screen V001

2026-09-27. Exact analysis only; no numerical run, new probe preparation,
lower-band projection, physical metric assignment or parent transfer.

**Result:** the native record response is not a pure common time rescaling
of the two carrier channels, even with a uniform additive potential. Their
dimensionless frequency ratio changes. This rejects that specific clock-only
interpretation, not all possible common metrics in a multiband medium.
Both channels remain consistent with one common, explicitly known BS
interaction law; its detuning can be reconstructed jointly.

Read inputs:

- `TWO_BAND_ANALYTICAL_BRIDGE.md`, SHA256
  `97c8ab39d450048897f0f324a479cf6a37b584e8cbafc4dc9e7b1d517ecd07a8`.
- Recovered `BS_MICRO_ACTION.md`, SHA256
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
  Its recovery provenance records matched packet/dependency hashes. The
  recovered copy was read fully and rehashed; no historical placeholder was
  hydrated. BS05 supplies an operational boundary-clock calibration, not a
  spacetime clock. BS09/BS11 supply transfer and occupied-record feedback.
  BS16 is explicitly an elliptic diagnostic, while BS20–BS21 remain a
  source/response template until their operators and completion are frozen.

## 1. A calibration-independent two-frequency identity

Use the inherited fixed-q block, in the native hbar=1 frequency units,

    H_q=C_q I-hX_a+(b_q-jX_C)n,
    h=1, j=1/2, b_q=9/4-q/2, C_q=3+q.

For general fixed h,j>0 put

    d_+(b)=sqrt[(b-j)^2+4h^2],
    d_-(b)=sqrt[(b+j)^2+4h^2],
    D(b)=d_-(b)-d_+(b),
    nu_L=j-D/2, nu_U=j+D/2.

These are the within-lower-band and within-upper-band carrier transition
frequencies. The function sqrt(x^2+4h^2) has derivative of magnitude strictly
less than one, so |D(b)|<2j for finite b. Thus both frequencies are positive
and |A|<1 below. Since x/sqrt(x^2+4h^2) is strictly increasing,

    D'(b)=(b+j)/d_-(b)-(b-j)/d_+(b)>0.

Thus b_1=b_0-lambda_R with lambda_R>0 gives

    nu_L(1)>nu_L(0),      nu_U(1)<nu_U(0),
    nu_L(q)+nu_U(q)=2j.

Define the dimensionless contrast

    A(q)=[nu_U(q)-nu_L(q)]/[nu_U(q)+nu_L(q)]=D(b_q)/(2j).

It obeys A(1)<A(0). This is independent of a common frequency-unit choice
and of all additive energy offsets. Equivalently nu_U/nu_L changes. This
uses the exact two-band spectrum, not a mean-link replacement.

## 2. Exactly which common-clock claim fails

For fixed intrinsic probe parameters, a pure common-clock model predicts

    nu_L(q)=a(q) nu_L(0),    nu_U(q)=a(q) nu_U(0),

with the same positive a for both channels. Equality of their sum forces
a(q)=1, while the strict inequalities above contradict that prediction for
q=1. A uniform scalar potential C(q)I cannot help because it cancels from
all gaps. Even separate band-constant offsets cannot change either within-
band gap. The native -lambda_R q n term is not such an offset: it changes
the link-mediated band mixing.

The comparison keeps the lower/upper channel labels fixed. Under b -> -b,
D changes sign and the unlabelled pair of within-band frequencies merely
swaps. An unlabelled spectrum alone therefore cannot establish the signed
contrast or exclude that relabelling. The inherited q=0,1 detunings are both
positive, so this sign-swap ambiguity does not explain their change.

This is a state-independent spectral exclusion of a **pure lapse/rate
rescaling with frozen intrinsic dispersions**. It is not a general metric
no-go. A common spatial geometry acting on distinct nonlinear bands, or a
record-dependent material self-energy on one geometry, can change their
frequencies differently. The present two-site system supplies neither a
continuum momentum family nor the physical ruler and principal symbol needed
to decide that stronger question. Position-dependent potentials and other
constitutive effects are not excluded merely by rejecting a uniform offset.

## 3. What a constructive common-parent calibration can recover

The two frequencies determine j=(nu_L+nu_U)/2. Given the independently
fixed h and |A|<1, the detuning is uniquely reconstructed as

    b=A sqrt[j^2+4h^2/(1-A^2)].

This follows by squaring d_-^2-d_+^2=4bj and keeping the sign of D.
At A=0 the unique solution is b=0; the displayed inverse includes that
case without dividing by A. The endpoint |A|=1 is excluded for h>0 and
finite b, rather than being another invertible calibration point.
Both channels therefore infer a single native interaction parameter without
assigning each its own metric. This reconstructs BS dynamics, not length.

Independent bare-link frequencies provide an additional check:

    b=(d_-^2-d_+^2)/(4j),
    h^2=[d_-^2+d_+^2-2b^2-2j^2]/8.

The already-derived cross-band carrier lines give a stronger same-parent
closure without separately supplying h. For assigned, resolved lines of
one specified four-level block, set M=d_-+d_+ and

    omega_lo=M/2-j,       omega_hi=M/2+j.

Then the four carrier lines must obey

    omega_hi-omega_lo=nu_L+nu_U=2j,
    M=omega_hi+omega_lo,
    b=A M/2,
    h^2=(1-A^2)(M^2-4j^2)/16.

The last two identities follow from (d_--d_+)(d_-+d_+)=4bj
and the sum of their squares; they hold for either sign of b, including
b=0. M>2j and |A|<1 give h^2>0. Thus the line assignments test spectral
closure and reconstruct the same native h,j,b, rather than assigning a
metric to each channel. Unlabelled peaks or an unconditioned multi-q
mixture can have assignment ambiguities; the readout coefficients below
must also make the relevant lines visible. These are cross-band labels,
not an assertion that their frequencies exceed every within-band line
for all h,j,b.

A stronger common-geometry proposal must first fix how one geometric
configuration enters each band's dispersion and every allowed material
coupling. Then the same geometric parameters must account jointly for the
carrier and link spectra, with no channel-by-channel geometric fit. A
record-dependent material parameter derived from the same action may be
included honestly; leaving an arbitrary function per band makes this test
non-identifying. Agreement only with a lower-band hopping is insufficient.

## 4. Actual state and operational readout

The actual native formed state has both band populations; its upper weight
is reported as 0.1305499137438213. Occupation alone does not guarantee a
visible within-band oscillation. The bare carrier readout contains terms
rho_(beta,+;gamma,-) times the link-state overlaps, and these coefficients
can vanish. Therefore the spectral exclusion is exact, while an operational
two-line test additionally requires two nonzero, resolved readout coefficients
or a separately frozen response protocol. No such new experiment is claimed.

Keep all formed-state populations and coherences and the complete mixture of
record sectors. Either retain all outcomes of a joint record/carrier read or
predict the unconditioned union of lines with its existing amplitudes and
weights. Do not select a successful lower-band subensemble and call it the
original state. Frequency selection may define a restricted effective probe,
but it narrows the claim and does not erase the other band's energy.

## Next action

Use A(q) as an exact null test against a proposed pure-clock interpretation.
For a genuine one-metric proposal, supply the same-parent dispersion/ruler
map and test both channels through that map. The recovered BS action leaves
that map open; no q4 Fisher metric or owner-once geometry is imported here.
The current constructive conclusion is common interaction dynamics with a
non-universal clock-only response, not established operational gravity.
