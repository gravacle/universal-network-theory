# Retained-state C barotrope qualification: prospective root-run unit

2026-09-29. No author compilation, provider import/evaluation, background
integration or scientific execution. This adds a test executable and a
stdlib-only receipt driver; the accepted provider, pinned CLASS and
ordinary CLASS adapter are unchanged. No observational target is tested.

## Exact census and roles

Authenticate the unchanged BBN inverse result/freeze and all five completed
`FINITE_PRESSURE_BAO_RULER_V001_BACKGROUND_{0..4}.json` packets, their
payload identities and full frozen ancestors. These contain 67 points times
5 backgrounds = 335 distinct normalized histories, with all four inherited
spectral-copy labels = 1340 retained states. There are 295 finite histories
(1180 finite labels) and 40 explicitly ideal-dust histories (160 labels).
Finite and dust counts are checked, not inferred by a tiny-pressure cut.

Run the complete history for spectrum-index0 of each (background,point).
The already derived/evaluated same-normalized-history identity permits this
computational reuse; it does not delete the other three physical labels.
Every copy undergoes its own present-time constructor, saved R/I/e/w/ca2/
omega anchor, quadrature, conservation, invalid-input and stress checks;
all four present normalized r/w/ca2/omega are compared. No copy is selected
because of its result. The finite constructor receives unweighted saved
`hard_energy`, `I`, and `R`; density rho1=`Omega_exc` is expressed in common
Hcal-normalized units. Homogeneity of all stress identities makes the test
independent of multiplying all densities by (Hcal/c)^2 to CLASS units.

Fixed history epochs are A=1,11,101,501,1101,3001,10001,10^7. The first seven
are compared to the saved BAO material epochs; 10^7 tests the already owned
domain endpoint, without adding an earlier history. Context a in [10^-7,1].

Preserve the provider protocol's independent algorithm controls:
r1=10^-12,10^-6,1,10^6 at R=rho1=1 and A=1,10,1000. These are explicitly
synthetic numerical controls, not four new physical candidates. Their I1
is computed only at root execution by independent uniform-theta
Simpson2048. Their known energy is r1/2+r1^2/4. All are always retained.

## Science implementation and independent controls

`unt_hard_barotrope_qualification_v001.c` is a standalone stdin/stdout test
program. It links only the accepted provider and libm. No CLASS or upstream
producer is linked, imported or executed. The Python driver transmits the
authenticated input numbers and retains the input digest and label map.

Primary C provider order128 is compared with order64. At each evaluated
finite orbit the executable independently evaluates period/action/pressure
using uniform-angle Simpson1024 and2048. Its ca2 uses the separate
curvature formula

    j=integral q^-1/2, ell=integral(1+sin^2 theta)q^-3/2,
    bar=(2/pi)integral cos^2 theta sqrt(q), Omega=pi/(2j),
    ca2=r bar Omega ell/[2j(1+r)].

The provider instead uses normalized derivative weights/covariances. The
Simpson rule uses neither provider nodes nor its inversion or moments.
At the provider-returned r, check log independent action against the exact
retained I1 a^-3/R^3. This is an independent residual test of the inversion,
not a second root fit. It requires no new scientific state or preparation.

Fixed tolerances, before outcomes:

* GL resolution, Simpson/method, saved material history and copy comparison:
  absolute2e-13 plus relative2e-9. Independent action residual:2e-9 absolute.
* Saved present w/ca2/r and Simpson action refinement: relative2e-9 with
  merely1e-300 denominator floor, so tiny positive states are not ignored.
* Conservation, stress/gauge and trace: absolute2e-13 plus relative2e-11.
* Log-scale derivative steps h=1e-3 and5e-4; fourth-order Richardson from
  the two centered estimates: absolute2e-11 plus relative2e-6. Density
  second derivative: absolute2e-8 plus relative2e-6. Raw step differences
  have separate absolute2e-10 (second derivative2e-7), relative5e-5 gates.
* Energy bound A^3<=rho/rho1<=A^4 allows relative2e-10 at the endpoints.
* The provider's pre-existing constructor2e-10, virial2e-11, inversion and
  quadrature normalization gates remain unchanged, not relaxed by this test.

Derivatives are checked only at interior epochs (A>1 and A<10^7) so no
undeclared future/earlier evolution is used. The endpoints retain all
material/conservation/anchor checks; the derivative skip is explicit.
Differentiate rho/rho_at_center and p/rho_at_center to control scaling,
as well as w and ca2. No differencing of huge absolute density numbers
against a fixed unit floor is used.

Both signed metric-source pairs (metric_continuity,metric_euler)=
(-.17,.11),(.23,-.31), Hconf=.375, k^2=.49, delta=.3, theta=-.2 are
synthetic algebra controls, not constrained cosmological initial data.
Verify the helpers against independent total stress conservation:

    delta_rho'=-3Hconf(delta_rho+delta_p)
                -(rho+p)(theta+metric_continuity),
    [(rho+p)theta]'=-4Hconf(rho+p)theta+k^2 delta_p
                     +(rho+p)metric_euler.

For a declared time-shift T=.0125 check delta_rho_new=delta_rho-rho'T,
delta_p_new=delta_p-p'T, theta_new=theta-k^2 T, and invariant
delta_rho+3Hconf(rho+p)theta/k^2. These test algebraic gauge covariance,
not a metric solution or Phi=Psi assumption.

Explicit dust must give rho=rho1 A^3, w=ca2=ca2_ln=0. Test rejected a=0,
a=1.01, finite I=0 and a deliberately inconsistent saved energy (1.001e1).
Rejecting finite-empty positive-density data is not a dust failure.

## Fixed execution and workload

`hard_barotrope_qualification_v001.py` has four explicit modes:

1. `freeze`: validates all source/data ancestry and prints the complete
   immutable snapshot. Root publishes it as
   `HARD_BAROTROPE_QUALIFICATION_V001_FROZEN.json`.
2. `build`: requires that exact freeze; runs `/usr/bin/clang --version`
   and the explicit argv below. It creates only the named new build
   directory/binary, refuses an existing binary, and prints a complete
   compiler stdout/stderr/binary identity receipt. Root publishes it as
   `HARD_BAROTROPE_QUALIFICATION_V001_BUILD.json`.
3. `benchmark`: requires the matching build/binary; tests the first sorted
   dust history and first sorted finite history, all eight labels, plus
   all four synthetic controls. It is a sizing/control unit, not a new
   favorable-state selection. Root publishes a separate benchmark receipt.
4. `run`: same code/constants over all335/1340, plus four controls. Root
   alone executes after the sizing unit. No tuning or science acceptance
   threshold follows from runtime.

Build argv (each item is a separate argv element, no shell expansion):

    /usr/bin/clang -std=c99 -O2 -Wall -Wextra -Wpedantic -fno-fast-math
    J/unt_hard_barotrope_v001.c
    J/unt_hard_barotrope_qualification_v001.c -lm -o
    J/hard_barotrope_build_v001/unt_hard_barotrope_qualification_v001

The actual frozen argv uses absolute paths. Only the existing compiler is
used; no package fetch, installation, make parallelism or CLASS rebuild.
Inherited include/library injection environment variables are removed.
Compilation warnings are preserved, not suppressed. No author syntax
compile is performed; only a nonexecuting Python AST parse may be used.

The computation is O((335*8+1005)*quadrature_work), bounded to small local
arrays plus a retained failed-check ledger. Dense matrices and ODEs are
absent. The driver captures all child output and compiler identity. No
wall-clock science deadline is imposed. On interruption it terminates only
its own newly created process group and drains the pipes; the five-second
termination grace is cleanup, not a research timeout.

Generated receipts are stdout only. The driver does not overwrite/publish
JSON data or modify originals. The only non-stdout write is the expressly
authorized new compiler output. All input paths must remain inside the
project, with symlinks rejected; build paths remain inside J.

## Output and qualification meaning

The output binary path is checked for symlinks before invoking the compiler,
including a dangling symlink. Existing outputs are never overwritten.
The receipt carries the freeze SHA, canonical payload SHA, exact retained
label/history mapping, stdin SHA, process time/exit/stderr, binary identity
via its build receipt, all primary epoch readouts, check counts/maxima and
every failed check. Epoch tuple labels are explicit; undefined dust r and
omega are null, never invented. All coarse/method/derivative failures remain
in the result. Initialization failures retain the case, branch and return
codes. Evaluation failures retain their case/A and failed boolean check;
their individual provider return code/error string is not serialized.
Neither failure type can create a COMPLETE result. Captured stdout
and stderr are always retained byte-for-byte in base64. A malformed or
unexpected C packet is a failed validation receipt with those captured
bytes, not an exception that discards the invocation.

The Python layer additionally checks the saved material epoch values and
four-copy present identity without rerunning any ancestral producer. It
authenticates the full335-history/1340-label inputs even when the benchmark
executes only two histories; the benchmark output mapping lists only its
two/eight executed histories/labels, with the full originals still bound
by the freeze. The full run has exact completed census; a benchmark is
never promoted to it.

Passing qualifies the numerical material/provider implementation for its
declared finite interval. It is not a CLASS candidate integration, a
recombination/transfer solution, a thermodynamic-origin result, an averaging
proof, or an observational success. The already enumerated finite-slice,
ordinary thermal history and CLASS stress-site integration work remains.
