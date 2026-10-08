# Ordinary PRIMAT C baseline: prospective qualification V001

This is an inert implementation/qualification packet, not an executed BBN
result. It uses the pinned ordinary C solver and its selected physical data.
There is **no conserved-scalar H modification, inferred hard gap, abundance
likelihood, new neutrino reheating calculation, or recalibration** in this run.
The existing conserved-scalar implementation route remains a separate task.

## 1. Exact source and side-effect boundary

Project root is `/Users/bgm/Documents/ChatGPT/Universal Network Theory` (ROOT).
J is its `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation`;
B is `J/bbn_inputs_v001/primat_c_reference_v001`.
Upstream is commit `4bf97d5082eee54b9df50d88f43182bb651fea80` of
`CyrilPitrou/primat`, under `B/upstream` with its original relative layout.

`PRIMAT_C_READONLY_DEPENDENCY_MANIFEST_V001.json` is bound at
`5ec0ccea45d547b639ebcdaf86f059b1518256ea6e709829ec0e47980e4cc38e`.
It owns precisely 46 code files (22 C, 24 headers), 24 data files, and two
license notices. The code receipt is `CODE_ACQUISITION_V001.json`,
`658aea594695eb28ce1698b21d38ac8df582d2cce65c330016e4575193c939ef`.
All 24 data members must have completed byte receipts before compilation/run;
normalizations must retain the raw bytes and both raw/published hashes.
The adapter uses only these fixed paths. No arbitrary input argument, overlay,
environment-based data discovery, download, installer, or external process is
invoked by the adapter. GPL notices remain present.

`J/derive_primat_readonly_sources_v001.py` is a **stdout-only source
transformer**, not a C compiler or science producer. Root executes it once
after review, publishes its JSON as
`B/PRIMAT_READONLY_DERIVED_SOURCE_V001.json`, and publishes its two exact
base64-decoded C files using apply_patch. The receipt binds original hashes,
new hashes, and complete unified diffs. Upstream is never edited. The only
derived library units are `plasma.c` and `weak_rates.c`; the other 20 C units
and all headers remain byte-identical. The transformer itself was syntax and
exact-anchor checked without execution during authorship.

The derived behavior is fail-closed input handling, not altered valid-data
physics:

- QED requires the matching modern e2/e3 pair; no legacy, analytic, or
  recompute branch is reachable. Both tables must be finite, have four
  columns, at least four rows, equal row counts, and identical increasing
  positive temperature columns.
- Electron thermodynamics requires its matching fingerprint and readable,
  finite, five-column increasing grid. A read error remains an error; a
  missing/stale table cannot trigger quadrature or a cache write.
- Nonthermal and thermal weak tables require both expected filename and
  matching header fingerprint, finite three-column increasing grids. Miss,
  mismatch, malformed data, or a race making the file unreadable is fatal;
  no table generation or thermal VEGAS fallback is allowed. Signed thermal
  *corrections* are retained; positivity is tested on the physical total
  forward/backward rates rather than requiring every correction be positive.
- Table interpolation arithmetic on valid input is unchanged. The library's
  deterministic neutron-lifetime normalization remains active; disabling
  generation does not mean all arithmetic is replaced with copied outputs.

Legacy generation code remains in the derived source after unconditional
guards so the diff is minimal and auditable; it is unreachable for this
adapter. Cache-directory helper calls before the guards only construct path
strings. File-writing APIs are not called and all their configuration gates
are disabled. Failure stdout/stderr is preserved by the external invocation
receipt, including process termination, malformed/partial JSON, and nonzero
exit. The ordinary adapter does not write its own result files.

## 2. Fixed physical and numerical inputs

`B/derived_ordinary_v001/unt_primat_ordinary_v001.c` accepts exactly one of
`default` or `refined`. It invokes the reviewed direct APIs in this order:
configuration, plasma, nuclear rates, rate variations (zero defaults),
standard background, nuclear network, in-memory result assembly. It does not
call the stock main, CLI, Monte Carlo code, or `custom_background` shortcut.

Both profiles use the unchanged pinned defaults:

| Input | Value |
|---|---:|
| h | 0.6766 |
| omega_b | 0.02242 |
| omega_c | 0.11933 |
| present photon temperature | 2.7255 K |
| neutron lifetime | 878.4 s |
| Newton constant | 6.6743e-11 SI (converted by the library setter) |
| extra DeltaNeff, chemical potentials, analytic distortions | 0 |
| QED, radiative, finite-mass, thermal, NEVO spectral corrections | enabled |
| standard background temperature span | 40 to 0.001 MeV |
| nuclear eras | 10 to 1 to 0.11 to 0.001 MeV |
| network | small: eight species, 12 nuclear reactions plus n/p |
| master nuclear rate grid | 1000 nodes; unchanged upstream endpoints |
| background temperature sampling | 600 per decade |
| electron table | 2000 rows; existing selected cache |
| nonthermal/thermal weak sampling | 80/20 per decade; existing caches |

`default` uses nuclear relative tolerance 1e-7, `refined` 1e-8. Upstream HT
RK45 and MT/LT BDF equations, Jacobians, absolute tolerances and LT's factor
10 relative-tolerance convention remain unchanged. This is a nuclear ODE
refinement only: it does not establish background-grid, rate-table,
thermal-cache Monte Carlo, or NEVO physical/model convergence. The fixed
data/cache selection must not be regenerated to follow an outcome.

The baseline deliberately preserves upstream's ordinary background
bookkeeping, including its omission of baryon rest energy from the displayed
Hubble density sum. It must not be advertised as a newly corrected complete
cosmology. A future scalar change must explicitly own its ordinary matched
control, the baryon contribution, the exact a-current, vacuum matching and
the prescribed-neutrino-history limitation; these are not silently folded
into this baseline.

## 3. Prospective controls and complete output

All accepted HT/MT/LT history rows are retained in original order, including
any shared era endpoints; no clipping, sorting, downsampling or selecting
final abundances. Species order and integer mass numbers are included.
Every row is checked for finite positive time, nondecreasing time order,
finite raw abundance, `Y >= -1e-12`, and
`abs(sum((N+Z)*Y)-1) <= 1e-8`. The small negative allowance is a declared
numerical tolerance, not a changed value: every raw signed Y remains output.
Final positive D/H, 0<YPBBN,YPCMB<1 and positive finite Neff are required.
Reaction stoichiometric conservation is already checked by the unchanged
network builder; accepted-history baryon conservation is a separate check.

All background nodes are output with time in seconds, temperature in MeV,
dimensionless a, H in s^-1, three neutrino temperatures, baryon mass density
in g/cm^3 and physical n/p rates in s^-1. Background time/a must increase,
temperature decrease, and time/T/a/H/rhoB be finite positive. Physical weak
rates must be finite nonnegative where T<=10 MeV. At higher T their two
fields are explicitly null with a domain reason, not an asserted cache
extrapolation. Nonfinite emitted numbers are counted and fail qualification;
these nulls are distinct from the intentional above-10-MeV rate nulls.

Raw stage errors are `FAILED_STAGE`; completed arithmetic with failed controls
is `FAILED_CONTROLS`; only completed internal controls yield
`COMPLETE_ORDINARY_ONLY`. That status does **not** include two-profile
qualification. After both immutable results exist, independently recompute:

- relative D/H difference, denominator refined D/H, <=5e-5;
- absolute YPBBN and YPCMB differences, each <=1e-5;
- relative Neff difference, denominator refined Neff, <=2e-12 (the
  background is not changed by nuclear tolerance);
- full finite/history/conservation checks above for both profiles.

All differences and failures must be reported, not only passing observables.
These tolerances are prospective numerical controls, not observational error
bars, posterior confidence, or a claim of precision better than source data.
Published/library benchmark abundances may be displayed descriptively with
their exact convention and provenance, never made into an outcome-selected
gate. No observed D/H or helium likelihood is scored here.

## 4. Actual HT initial-memory diagnostic

The actual two-state HT generator is

    dYn/dt = Gamma_pn Yp - Gamma_np Yn,   Yn+Yp=1.

For two solutions of this same fixed generator, their initial difference
obeys exactly

    delta Yn(tweak) = delta Yn(tstart) exp(-K),
    K = integral_tstart^tweak (Gamma_np+Gamma_pn) dt.

The adapter queries the actual background and rate accessors on 2049 fixed
equally spaced log-time points between t(10 MeV) and t(1 MeV). It retains
every `[t,T,Gamma_np,Gamma_pn,t*(Gamma_np+Gamma_pn)]` row. Composite Simpson
with 2048 and nested 1024 intervals estimates K; normalized difference
`abs(K2048-K1024)/max(1,abs(K2048)) <= 2e-5` is a prospective quadrature
control, **not a rigorous integral error bound**. `-K2048` is reported as a
log contraction estimate to avoid underflow pretending that memory is
exactly zero. It involves no additional ODE or assumed equilibrium reset.
This exact HT identity plus approximate integral does not bound subsequent
nonlinear nuclear seed sensitivity or final abundance errors.

## 5. Explicit local build and invocation custody

`B/PRIMAT_ORDINARY_BUILD_MANIFEST_V001.json` contains literal argv arrays:
22 library compilations (20 upstream + two reviewed derived), one adapter
compilation, one link. Use existing `/usr/bin/clang`, GNU11, O2, Wall/Wextra,
pthread, the exact fixed include directory and libm. No stock Makefile,
shell wildcard, pip, package manager, generated build system, system change,
parallel compiler, cleanup, or installation. Only `B/build_ordinary_v001`
is the new object/binary destination. Root creates that exact directory if
absent, records compiler version, then executes the immutable argv serially.

For every command, bind manifest/source/header/derived receipt hashes,
working directory, argv, environment, exit status, complete raw stdout and
stderr, and successful output hash. Never overwrite unexplained old outputs;
resumption requires exact prior command/input/output receipt identity. Bind
independent reviews additively, avoiding a circular self-review pin. Before
each profile invocation, authenticate the binary, all inputs and no-generation
derived source receipt. Use one process at a time and `OMP_NUM_THREADS=1`,
`OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`,
`VECLIB_MAXIMUM_THREADS=1`; `CPR_NN_DEBUG` must be absent.

The numerical library is C/libm/pthread only and this driver launches no
threads or subprocesses. Tables are a few MB, the eight-species history is
O(number of accepted steps), and background/rate arrays are small. This is a
sizing argument, not measured RSS/runtime: root first measures the complete
ordinary default invocation, preserves it, then runs the fixed refined
profile. There is no arbitrary science wall cutoff or hidden retry. A fatal
invocation is unfinished evidence, not a completed scientific comparison.

No files in this packet have been compiled, imported as a producer, or run
by its author. Root owns transformation publication, compilation and both
scientific invocations after full input authentication and independent review.
