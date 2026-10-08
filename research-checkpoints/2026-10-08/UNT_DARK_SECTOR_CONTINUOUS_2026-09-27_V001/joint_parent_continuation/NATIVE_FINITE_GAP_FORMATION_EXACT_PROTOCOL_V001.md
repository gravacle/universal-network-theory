# Exact polynomial check of finite gap formation

This prospective check is limited to the conditional four-dimensional channel
in `NATIVE_FINITE_GAP_FORMATION_V001.md`. Source authors and independent reviewers
do not import or execute it. Root may freeze and execute it only after source
review. It performs no parameter scan, eigensolve, numerical evolution, state
fit or observational comparison. The positive or negative physical verdict is
not a test target: the already derived coefficient identities are the targets.

## Fixed algebra and census

Use system then fragment tensor order, basis
`(blank,blank),(blank,occupied),(occupied,blank),(occupied,occupied)`.
In units where coefficients multiply `u^n=(tau/hbar)^n`, the complete on-pulse
Hamiltonian apart from a fixed support identity c_d I is

```
[[0,  0,       g,             0],
 [0, nu,       0,             g],
 [g,  0, epsilon,        lambda],
 [0,  g,  lambda, epsilon + nu]].
```

The initial joint density is `diag(1/2,0,1/2,0)`. epsilon, g, lambda and nu are
independent symbolic variables, not sampled points. epsilon stands for
`epsilon_r-lambda_R*d` only after the unrestricted result is known. nu>=0 is
needed for the stated energy sign, not enforced by substituting a positive
test number. Scalar c_d is retained in the physical ledger; the script checks
that an identity commutes and that every higher density coefficient has zero
trace. No volume derivative of c_d is claimed zero.

The program constructs `C_0=rho0`, `C_(n+1)=[H,C_n]` through n=6 using exact
stdlib Fraction coefficients and sparse multivariate polynomial dictionaries.
The Taylor density coefficient is `(-i)^n*C_n/n!`. The output serializes the
real or imaginary-i factor explicitly, including odd reduced coherences.
It does not pretend the density-matrix series is even. Real symmetric energy
and occupation observables must have vanishing odd coefficients.

The fixed observable census is q, held energy epsilon*q, active energy
epsilon*q+gX, fragment energy nu*q_b, copying interaction lambda*q*X_b,
formation energy gX and total on-pulse energy. Every coefficient through six
is serialized as an exact rational polynomial. The complete reduced cell
density coefficients and both switch-off work series are retained as well.

## Exact criteria fixed before execution

Every comparison is exact polynomial equality. There are no floating-point
values, tolerances, chosen durations, favorable degree selections or substituted
signs. The prospective gates are:

- Initial trace one; both switch-on expectations zero; fixed identity and held
  q-source commutators zero.
- `C_n^T=(-1)^n*C_n`, zero density trace at n>0, every real-observable odd
  coefficient zero, and total on-pulse energy conserved coefficient by coefficient.
- At every order 1 through 6, both ledgers hold:
  `Delta Es+Delta Eb=-<V>` and `Delta Eh+Delta Eb=-<V>-g<X>`.
- Reduced coefficients through order six vanish when g, lambda or nu is zero,
  consistent with the separate exact held/zero-gap controls. This finite check
  does not replace their all-orders analytic proofs.
- Reduced density has no correction below fourth order. For input I/2, the
  reduced fourth nested commutator is `-2*lambda^2*nu*g*X`; after 4! division
  this is `-lambda^2*nu*g*X/12`.
- Fragment energy coefficient at order two is `nu*lambda^2/2`. Active energy
  coefficient at order four is `-lambda^2*nu*g^2/6`; formation switch-off is
  its opposite. Held population has zero coefficients at orders 1 through 5.
- Held population at order six is `-epsilon*g^2*lambda^2*nu/72`, and held
  energy is `-epsilon^2*g^2*lambda^2*nu/72`.

These are independently hand-derived identities being checked by explicit
matrix algebra, not results discovered by a fit. A mismatch remains a failed
check with the actual polynomial preserved. The all-zero epsilon leading
coefficient is not an all-orders record-conservation claim. A negative leading
energy term establishes only a sufficiently-short-duration tendency under the
declared inputs, not a passive attractor or a derived galaxy mechanism.

## Custody and bounded execution

The source is `native_finite_gap_formation_exact_v001.py` in the existing
`joint_parent_continuation` directory. It imports only Python standard-library
modules, never another model or producer. All operations require the sole root
`/Users/bgm/Documents/ChatGPT/Universal Network Theory` as working directory.
`freeze` hashes source, this protocol, the analytic note and six pinned existing
evidence files. It refuses previous new-attempt intents/results and publishes
`NATIVE_FINITE_GAP_FORMATION_EXACT_V001_FROZEN.json` exclusively. `run` checks
the same freeze, writes an exclusive intent, and is a separate command; neither
operation launches the next.

The fixed bounds are dimension four, order six, four polynomial variables,
at most 4096 terms per polynomial and at most 1 MiB serialized result. The
calculation has no data-dependent order/step loop. Root must retain the normal
external monitored 10 s wall and sampled 256 MiB process-group RSS limits.
The child sets CPU soft/hard limits 5/6 s and checks a cooperative 10 s deadline
during polynomial multiplication. These are distinct bounds: sampled RSS is
not an unsampled memory guarantee, and a hard kill may leave an intent without
a child result. Root retains the process streams/failure receipt in that event.
No heavy or remote worker is needed.

The child keeps partial check rows and polynomial series in its result object,
catches ordinary exceptions and rechecks source/input pins before success.
Successful or failed results use atomic no-overwrite same-directory publication
with a hashed wrapper. A caught failure is retained as `EXACT_CHECK_FAILED_RETAINED`;
an absent result after a hard kill is not a pass and cannot be silently retried
under the same identifier. Unusual failure of publication itself may likewise
leave only the attempt and root's external receipt. Existing artifacts are never
replaced or used as writable scratch space.

Success means `EXACT_POLYNOMIAL_IDENTITIES_COMPLETE_NOT_PHYSICAL_QUALIFICATION`.
Both success and failure keep physical qualification, formed-state completion,
thermal qualification and Stage 3 completion false. The active and held energy
are distinguished, controller and blank-supply costs remain explicit, physical
degree/density matching remains open, and held q self-response remains zero.
