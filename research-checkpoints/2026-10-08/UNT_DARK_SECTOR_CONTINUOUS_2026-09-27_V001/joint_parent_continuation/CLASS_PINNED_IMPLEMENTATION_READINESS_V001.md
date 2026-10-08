# Pinned CLASS implementation readiness V001

2026-09-29; metadata/source inspection only. No repository clone/archive, complete source receipt, build, cosmological producer or fit was performed. This prepares the finite-slice route in `FINITE_SLICE_CMB_PREPARATION_AND_BOLTZMANN_ROUTE_V001.md` (SHA256 `7b9a4952f279d9a32b6a6d5de9338f01b50bd3cbd6a1eab8cced8bad5f593cd4`). It does not replace that note's same-state, Q=0, spectrum and thermal-origin qualifications.

## 1. Exact source pin and bounded receipt request

Choose the official **CLASS v3.4.0** tag, commit **64bbab707faf4de4779a9e04edd180fef18d98fa**. The [official tag page](https://github.com/lesgourg/class_public/tags) identifies it; the [full commit](https://github.com/lesgourg/class_public/commit/64bbab707faf4de4779a9e04edd180fef18d98fa) identifies the source revision. This choice is version/provenance based, not a result-dependent solver choice.

`CLASS_SOURCE_INVENTORY_PLAN_V001.json` enumerates **89 files, 3,294,365 raw bytes**, with their pinned Git blob SHA1 and lengths from the official recursive tree API. The API returned `truncated=false`. A first sandbox metadata request failed DNS; a reviewed read-only escalation retrieved metadata. These are **not** SHA256 receipts of locally downloaded source bytes. Raw URL for each later bounded retrieval is

`https://raw.githubusercontent.com/lesgourg/class_public/64bbab707faf4de4779a9e04edd180fef18d98fa/<exact-listed-path>`.

The set is the standalone executable dependency closure, retaining a conservative header set and small reference documents rather than trying to prune individual transitive headers. It contains:

- 34 compiled translation units: 11 tools, 11 source modules including output, one main, and 11 linked external modules.
- 44 headers: 30 include headers, three same-named local Hermite implementation headers in tools, and 11 external headers. The upstream duplicate locations are preserved, not resolved by guessing include precedence.
- Five active data files: four bundled HyRec tables plus the small default heating table. The inactive high-resolution HyRec table is explicitly excluded after reading the pinned header; its metadata remains listed as not requested.
- Six build/reference/attribution documents: Makefile, README, default/explanatory inputs and HyRec/heating READMEs.

No tests, Python package, notebooks, generated output, full documentation tree, web interface, other branches or observational likelihood data are included. Halofit/HMcode/distortions are compile-link dependencies of the unpruned executable, **not** permission to apply those physical prescriptions to our hard fluid.

For a later receipt, retrieve only the enumerated paths into a new project-local upstream directory, verify exact length and `SHA1("blob "+length+NUL+bytes)` against metadata, then record raw SHA256. Preserve upstream bytes and notices; put changes in a distinct derived directory with a complete diff and source manifest. The source API tree has no core LICENSE/COPYING file; the only license-named paths belong to excluded web fonts. The [pinned README](https://raw.githubusercontent.com/lesgourg/class_public/64bbab707faf4de4779a9e04edd180fef18d98fa/README.md) permits use subject to citation of CLASS II. Preserve that text and individual copyright notices; do not invent an SPDX/OSI license designation. This note is not a legal interpretation.

## 2. Exact executable objects and safe local build

The [pinned Makefile](https://raw.githubusercontent.com/lesgourg/class_public/64bbab707faf4de4779a9e04edd180fef18d98fa/Makefile) determines these compile groups:

```text
C++11:
  tools/arrays.c tools/hyperspherical.c
  source/perturbations.c source/primordial.c source/transfer.c
  source/harmonic.c source/lensing.c external/HMcode/hmcode.c

C:
  tools/growTable.c tools/dei_rkck.c tools/sparse.c
  tools/evolver_rkck.c tools/evolver_ndf15.c tools/parser.c
  tools/quadrature.c tools/common.c tools/trigonometric_integrals.c
  source/input.c source/background.c source/thermodynamics.c
  source/fourier.c source/distortions.c source/output.c main/class.c
  external/RecfastCLASS/wrap_recfast.c
  external/heating/injection.c external/heating/noninjection.c
  external/HyRec2020/hyrectools.c external/HyRec2020/helium.c
  external/HyRec2020/hydrogen.c external/HyRec2020/history.c
  external/HyRec2020/wrap_hyrec.c external/HyRec2020/energy_injection.c
  external/Halofit/halofit.c
```

Its intended no-install target is `class`, not `all` or `classy`. The latter invoke Python installation and contain package cleanup. Do not invoke `clean`, archive/install/package targets or any upstream Python helper. More importantly, the original recipes use unquoted working-directory paths; our real workspace contains spaces. Therefore use a small reviewed **explicit-argv build supervisor**, like the owned HYREC build, instead of executing those recipes or inventing a short-path/symlink workaround.

Each C object is compiled with `/usr/bin/clang`, each listed C++ object with `/usr/bin/clang++ -std=c++11`, then linked with clang++, `-pthread` and `-lm`. Include directories are the listed core and five external subdirectories; the standalone baseline uses the upstream HYREC define and a correctly quoted single argv definition of `__CLASSDIR__`. Use a bounded one-job build, ordinary `-O2` initially, no fast-math, no automatic compiler/SDK installation. The exact flags and every path must be sealed with the future build manifest; this is a plan, not an executed command.

The existing HYREC build receipt records Apple clang 17 ARM64. A read-only `clang++ --version` here also returned Apple clang 17.0.0, target arm64-apple-darwin25.5.0; `/usr/bin/ar` and `/usr/bin/make` exist. C++11/standard-library/pthread compatibility is consequently plausible, not proven until compilation. No Fortran, Python scientific extension, pip or external BLAS is required by this executable object list.

The pinned `include/parallel.h` was read completely (7257 bytes, raw SHA256 `91635eeb3def08b110bfbbc3e3be92851129c5a2c46c69f16fed4ee8dcd2946e`). It uses a C++ task pool and honors **OMP_NUM_THREADS=1** before querying a scheduler variable. Set that explicitly; omitting OpenMP compiler flags alone does not force this code to one worker. The source main/output modules will require full side-effect review after receipt. A future adapter should route only requested results to stdout or a new explicit project output directory; analytic initial-spectrum input avoids external-command spectrum paths.

## 3. Required candidate changes, localized and testable

The unmodified executable can serve only as an ordinary-physics baseline. The actual candidate needs these owned changes, while all standard branches remain separately callable:

1. **Material/background:** add a named exact barotrope provider for `e(I1 a^-3)`, `w(a)`, `cI²(a)`, and conservation derivatives, using the same retained action and matched vacuum. Amend the background/header/input interfaces; no CPL fit, independently chosen density or constant Neff replacement. Preserve `H0_code=Hcal sqrt(1+Omega_r)` and all density fractions divided by `1+Omega_r`, so the already calibrated physical densities remain unchanged.
2. **Perturbations/stress:** feed that same time-dependent `cI²=ca²` into both fluid evolution and stress reconstruction; bypass the dark-energy PPF branch. Retain zero hard shear. The inspected stock fluid initial data are not valid for a potentially substantial early radiative hard component. Its regular finite-history or explicitly constrained finite-slice initial vector must include its actual material fractions and ordinary-neutrino shear. Use Newtonian gauge without adding fictitious CDM merely to define a synchronous frame.
3. **Thermodynamics:** use the reviewed FULL, same-H histories/atomic helium mapping and a qualified bridge for xe, Tm, opacity and derivatives. The separately inspected bundled `hydrogen.h` (11868 bytes, SHA256 `1b2c64d108078722dd546f4e8b9bddca2cbe6abdf4b63e44e76fe0e9d58f4e52`) is not the same source/interface as the sealed standalone driver. Its active table names justify the inventory, but do not qualify a silent bundled-SWIFT substitution. Ordinary reionization and gas perturbation closure remain explicit imported inputs.
4. **Finite interval/spectrum/output:** expose the exact finite initial slice and spectrum normalization; preserve or bound the attenuated initial photon/polarization term. Time differences determine line-of-sight projection. A conventional positive conformal-time offset or radiation-era series variable must not be sold as evidence of a physical zero-time singularity. Review all absolute `k*tau` initialization/approximation heuristics when replacing stock start-time logic. Audit species bookkeeping for equality, matter output and lensing so the hard fluid is neither omitted nor double-counted. No independent lensing amplitude or unvalidated nonlinear CDM prescription.

The changes are substantial but finite: a material provider, sound-speed/stress sites, initial-state/start-time handling and a thermal-history bridge. They are not a new Boltzmann theory or a need to rederive ordinary atomic physics. No source change has been made in this readiness task.

## 4. Finite Ai=10^7 covers a useful k range without a zero-time premise

There is a simple **all-history** lower bound, independent of the hard-fluid transition:

\[
 \mathcal H_i=\frac{H_{\rm cal}}{c A_i}\sqrt{
 \Omega_b A_i^3+\Omega_H e(A_i)/e_1+\Omega_\Lambda+\Omega_r A_i^4}
 \ \ge\ \frac{H_{\rm cal}}c\sqrt{\Omega_r}\,A_i .
\]

All retained densities here are nonnegative. The saved background-0 constants are Hcal=73.6 km/s/Mpc and Omega_r=7.721040393166351e-5. Since T0 and the ordinary massless-neutrino convention are shared, Hcal sqrt(Omega_r) is the same across the five backgrounds. At Ai=10^7 this gives

\[
 \mathcal H_i\ge21.5722291\ {\rm Mpc}^{-1};\qquad
 k/\mathcal H_i\le0.02317795\ (k=0.5/{\rm Mpc}),\quad
 \le0.04635590\ (k=1/{\rm Mpc}).
\]

These are direct arithmetic bounds from saved constants, not a new material/perturbation run. They show that a finite early slice can cover high-k primary-CMB work; no artificial restriction to the old 0.1/Mpc late-transfer maximum is needed. However a leading-order long-wave series alone has omitted terms of order `(k/Hcal_conformal)^2`, potentially around 2e-3 at the upper k=1 point. It is **not** a precision initial condition certificate. Use higher-order/constraint-projected data with actual finite material fractions, and move the initialization within the declared finite thermal interval with transported data or an independently qualified regular-series continuation. Do not reset arbitrary columns and call the difference decaying-mode suppression.

For the first full spectral benchmark, propose scalar TT/TE/EE and lensing to displayed ell=3000, with a k-domain comparison reaching **at least 0.5 and 1 Mpc^-1** under unchanged physics. These are numerical tail/initialization tests, not final data-selected cuts. Low-z CMB lensing can require k above the primary-CMB peak-support region; convergence must decide the retained tail rather than silently discarding it. If larger k needs an earlier slice outside the presently owned thermal interval, report that new thermal-domain requirement or retain exact finite-slice data without claiming regular asymptotic preparation. A finite Ai always permits constrained data; it does not automatically justify a particular regular mode at arbitrary k.

The hard component need not be asymptotically relativistic at Ai for every limiting state. Evaluate its actual w and fractions. The dust comparator and near-dust states require the appropriate material-corrected growing data, not the pure-radiation hard relation used out of domain. The finite interval assumes photons with the owned temperature and ordinary interactions; it does not explain their origin or assert inflation.

## 5. Memory and first executable qualification

The 3.29 MB source size is not a RAM estimate. The largest obvious spectral allocation is the lensing Wigner buffer. The inspected [lensing implementation](https://raw.githubusercontent.com/lesgourg/class_public/master/source/lensing.c) has, for TT/TE/EE, approximately

\[
 M_W=8\,[12 N_\mu(l_{\rm unlen}+1)+5(l_{\rm unlen}+1)]\ {m bytes},
\]

or 16 rather than 12 for its higher-order option. The [precision defaults](https://raw.githubusercontent.com/lesgourg/class_public/master/include/precisions.h) use a smaller angular interval in fast mode and a full quadrature in accurate mode. At displayed ell=3000 the discovered default fast dimensions yield about **192 MB** for this buffer; an accurate full-angle choice with unlen=4500 gives about **1.945 GB**, or **2.593 GB** at higher lensing order. These dimension estimates must be rechecked against the pinned received files before execution; they are not measured total RSS or a promised upper bound. The discovered fast angular truncation itself requires accuracy comparison at high ell.

Background/thermal tables, source tables scaling as `8*Nsource*Nk*Ntime`, transfer/radial tables and integrator workspaces add to this. A **few-GB single-history accurate benchmark** is a reasonable planning estimate on the owned 16 GiB machine, not a reservation or hard stop. Do not launch 335 concurrent histories or retain every history's full internal arrays. Root can measure the first prospectively selected standard and candidate benchmark RSS/time, then serialize the retained census. This is resource sizing, not permission to weaken physical resolution from the result.

Minimum meaningful build/physics qualification is: (i) ordinary baseline spectra with no candidate changes active; (ii) material/background/thermal packet equality against saved same-state controls, including normalization; (iii) dust and relativistic perfect-fluid perturbation limits, exact constraints and finite-slice normalization; (iv) time, initialization, hierarchy/tight-coupling, k-tail and angular/lensing refinements. Each is part of the numerical implementation, not another arbitrary native-to-GR approval gate. Root remains the sole compiler/producer. The next authorized implementation decision is whether to retrieve the explicit 89-file receipt and fully review it; this note has not done so.
