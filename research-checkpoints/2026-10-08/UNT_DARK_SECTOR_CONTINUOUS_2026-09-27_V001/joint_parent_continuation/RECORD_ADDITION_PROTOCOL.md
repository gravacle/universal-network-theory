# Prospective native two-endpoint record-addition test

2026-09-28. Freeze this protocol and its sources before producing results.
This is a new small BS preparation, not an extension of the old one-record
formed evidence by pretending its qutrit can have occupation two.

## Question and fixed parent

Does the actual coherently formed two-record state exhibit the different
record-addition energies of its lower and upper link bands, and does its
complete energy ledger agree with the native source identities? Report all
populations; a lower-band energy diagnostic is not substituted for the state.
No physical volume, clock equation of state, cosmological abundance or
continuum phase is inferred by this test.

Use the native two-node, one-link hold terms with two endpoint record
registers. At each endpoint a local writer is fixed occupied in the SAME
declared content x. The writers are conserved controls with epsilon_w=0.
The subspace |B>,|x> of each record is exactly invariant under the listed
copying and hold terms. Keeping records L,R, link, and one-carrier position
gives 2*2*2*2=16 states. This is an explicit invariant restriction, not
postselection of a formed state. Choosing the other common content gives an
identical, separately labelled block; no unlisted writer coherence is used.

Factor order: (record_L, record_R, link, carrier), binary index 0 blank/left,
index 1 occupied/right. The carrier has exactly one occupied register across
the two nodes. The initial vector is |B,B,link=0,carrier=L>, index zero.

All original one-link parameters are retained:

    h=1, Delta=4, U_d=1, d_star=1,
    epsilon_psi=1, epsilon_r=1, epsilon_w=0,
    t_hop=.5, lambda_R=.5, lambda_J=.25, g=1.

Let R=q_L+q_R and n be link occupation. With X_C the carrier transfer,

    H_hold=3 I+R-X_link+(2.25 I-.5 R-.5 X_C)n,
    H_form=H_hold+g(X_record_L+X_record_R).

The implementation also builds H from the original ten term types,
including both degree penalties and the current-squared term, before
checking this compact form. Both writer-copy terms are present and locally
owned. No carrier-to-record or reservoir copy is newly added.

## Fixed schedule and controls

Form for duration 1 in the inherited hbar=1 Hamiltonian units. Then switch
both copying couplings to zero. The switch work is measured, not set to
zero. Hold observations are at 0,.25,.5,1,2 after the switch. These are
finite internal observation times, not a claim about physical run times.

Three prospectively fixed cases, no optimization:

1. Native coefficients above.
2. lambda_R=0 throughout formation and hold; all other parameters unchanged.
3. g=0 throughout formation and hold; all other parameters unchanged.

Each case starts from its declared initial vector. Controls are never
represented as holding the native case's formed state fixed. Their initial
complete energy is 3. The g=0 case must retain blank records. Copy-off is a
causal control, not a source for the native formation population.

## Prospective checks and reported observables

Absolute tolerance is 1e-11, inherited from the original 36-state join.
No scientific amplitude or population is given a success threshold.

- Hermiticity and full term reconstruction; exact charge/count projectors.
- Exact held spectra and projectors for R=0,1,2, beta=+/- and carrier-X
  s=+/-. Every R=1 endpoint multiplicity is retained; numerical degenerate
  eigenvectors are not matched to an arbitrary basis.
- Full analytic matrix reconstruction and eigenvalue multiset, including
  both link bands; exact first and second addition differences. For native
  lambda_R>0 the lower-band second difference is negative and the upper is
  positive; feedback-off makes both zero. These are diagnostics of labelled
  eigenbranches, not equilibrium selection.
- Instantaneous addition operator identity on each blank endpoint:
  A^dag H_hold A-P_blank H_hold P_blank
  =P_blank(epsilon_r I-lambda_R n). Report its unnormalized work on each
  actual formed blank sector and the sector probability; this is a readout
  decomposition, not a prepared postselected replacement.
- Native commutators [R,[H_form,R]]=-g(X_L+X_R) and
  [n,[H_form,n]]=h X_link, the production-current sign, and the zero held
  charge response. Store actual formation current and response slopes.
- Eigenspectral and independently implemented scaled-Taylor propagation
  for formation and every hold time. The Taylor recurrence is adapted from
  the fully read original compute_join.py; its exact-arithmetic tail bound
  is not promoted to a floating-point error certificate.
- Full formation energy conservation; measured switch work
  -g<X_L+X_R>; held energy conservation and its equality to the complete
  term and populated-band sums. Preserve the formed 16-component vector,
  all band/count weights and record-sector coherences through that vector.

The actual state weights are outputs, never fitted to a desired curvature
or cosmological density. A sudden addition costs 1-.5<n> in the native case;
adiabatically followed branch differences include a changed link state and
are reported separately.

## Execution and custody

Only the root runs the worker. `record_addition_compute.py freeze` writes
`RECORD_ADDITION_FROZEN.json` with exact source hashes, without numerical
propagation. The no-argument invocation first authenticates that freeze and
then writes `RECORD_ADDITION_RESULTS.json` exclusively. Existing files are
not overwritten. There is one process, one numerical-library thread and
complete JSON is flushed to a temporary file before atomic no-overwrite
publication, so an interrupted partial write is not accepted as a result.
only 16-by-16 dense matrices with fixed loops. No new timer cutoff, retry,
large system, external data or parameter search is used. This tiny job can
be rerun if interrupted; no checkpoint system is added.
