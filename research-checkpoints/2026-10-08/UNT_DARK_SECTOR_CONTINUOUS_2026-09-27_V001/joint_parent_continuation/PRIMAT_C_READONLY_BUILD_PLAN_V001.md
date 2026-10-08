# PRIMAT C: bounded data closure and no-generation build path

2026-09-29. Additive source review and prospective implementation plan. No
download, compilation, producer import, rate-table generation, ODE solve or
abundance scoring was performed by this review. The existing
`PRIMAT_CONSERVED_SCALAR_IMPLEMENTATION_ROUTE_V001.md` is unchanged. This plan
implements its conserved scalar density under the explicitly prescribed NEVO
history; it does not solve the changed neutrino collision/reheating problem.

## 1. Source custody and the executable subset

All upstream paths refer to [PRIMAT commit
4bf97d5082eee54b9df50d88f43182bb651fea80](https://github.com/CyrilPitrou/primat/tree/4bf97d5082eee54b9df50d88f43182bb651fea80).
The local directory is `bbn_inputs_v001/primat_c_reference_v001/` (B below).
`IMPLEMENTATION_READ_RECEIPT_V004.json`, SHA256
`16ca3eed90336d4ae6e290a27548b7e0bbdd2ce62575aeda1c3c723c83e60225`, binds
the five additional implementations: cache, plasma, weak rates, network data
and nuclear network, 253,682 bytes. All five byte counts, SHA256 values and
Git-blob SHA1 identities were independently verified. Plasma and cache were
read completely; the complete loading, interpolation, setup, miss/write,
solver/output and teardown paths relevant to this adapter were read in the
other three. Unused VEGAS integrands and post-BBN matrix-exponential internals
are not independently certified by this source-path review.

The proposed library subset is **22 C sources plus 24 headers, 716,000 upstream
bytes**. The exact enumerated paths/Git identities are in
`B/PRIMAT_C_READONLY_DEPENDENCY_MANIFEST_V001.json`; it excludes `main.c`,
`cli.c`, `ini.c`, `mc.c` and the three CLI/INI/MC headers. It includes API,
config, background, plasma, neutrino history, weak rates, nuclear network,
network data/builder, cache/constants, splines/tables, quadrature, ODE RK/BDF,
linear algebra, log/xalloc, QED pressure, RNG and VEGAS. The last three remain
link dependencies of unchanged objects, not permission to execute fallback
table generation. No Python wrapper, Makefile target, tests, fuzzing, package
installer, archive checkout or `clean` command is needed. `cpr_compile_network`
constructs stoichiometric arrays in memory; it does not invoke a compiler.

The inventory is a bounded acquisition plan, not a claim that every listed
source has already been acquired/read or linked successfully. Final quoted
include/symbol closure and source-side-effect review must use the actual
retrieved bytes. The subsequently supplied `IMPLEMENTATION_READ_RECEIPT_V005.json`
(SHA `21429951f1362fc8480407966a606e1249686184f000325133bca7b63b826c5a`)
binds QED pressure source, `small.txt`, `COPYING` and `LICENCE`. These identities
were independently checked; QED source and the license notice were read.
`LICENCE` explicitly permits GPL version 3 or later. Its recorded one-final-LF
local normalization and the earlier failed `LICENSE` URL remain evidence,
not hidden corrections. Preserve both license files and source notices.

## 2. Required ordinary data, not a repository-wide data tree

For the unchanged small-network, zero-chemical-potential, QED/NEVO/spectral/
thermal-corrected ordinary branch, the runtime closure is 24 files,
**2,295,836 upstream bytes**. All filenames, byte counts and Git-blob identities
are now resolved by the actual small-network list plus
`DATA_TREE_METADATA_V001.json` (SHA `94c2c016c10763420d26b3f63878767d775847a1e05840232d05ffbd59ac5c00`)
and `CSV_TREE_METADATA_V001.json` (SHA `c338ea911a978d074d850bdcafb2f62b36361a95240d1ffc5761eaf6a1b74305`).
These are metadata receipts, not claims that all data bytes have been fetched.

The complete selected source/data/license packet is 72 files and 3,047,769
upstream bytes. Reusing the authenticated local sources and five already
captured data files leaves **49 new files, 2,070,485 bytes**: 30 code files
(185,861 bytes) and 19 data files (1,884,624 bytes). No other tree contents
are requested.

| Category | Count | Reason |
| --- | ---: | --- |
| `csv/nuclides.csv`, `csv/reactions_large.csv`, `csv/detailed_balance.csv` | 3 | Config and nuclear loading read these even for `small` |
| `nuclear/networks/small.txt` | 1 | Owns exact selected reactions and table basenames |
| One table for each of its 12 thermonuclear reactions | 12 | Forward rates plus published error columns; no invented replacements |
| `NEVO/NEVOPRIMAT_col_1_7.csv`, `NEVO/NEVOPRIMAT.csv`, `NEVO/NEVOGrid.csv` | 3 | Thermodynamic history, 80-column spectral history and its grid |
| Two QED, one electron and two weak caches below | 5 | Reuse fixed ordinary physics without regeneration |

The twelve reaction names are `n_p__d_g`, `d_p__He3_g`, `d_d__He3_n`,
`d_d__t_p`, `t_p__a_g`, `t_d__a_n`, `t_a__Li7_g`, `He3_n__t_p`,
`He3_d__a_p`, `He3_a__Be7_g`, `Be7_n__Li7_p`, `Li7_p__a_a`.
The pinned `small.txt` has now been read and explicitly selects
`<reaction>_primat.txt` for each of these twelve; the manifest records each
separate actual path rather than relying on that naming pattern. The
prepended `n__p` channel uses the weak rates, not
a thirteenth nuclear rate file. `decays.txt` is not needed by this twelve-
reaction nonweak list. `large`, `small_parthenope`, NoQED histories, custom
overlays, analytic distortions, extra-rho tables, MC ensembles and decay-era
output are outside this first adapter.

The full spectral/grid pair is operationally mandatory even when weak caches
hit: `build_nevo_table` still loads it with the ordinary spectral flag on.
Disabling that flag to omit a file would change ordinary physics and cache
identity. The full table must have 6 thermodynamic plus 80 spectral columns,
paired with its 80-row grid; the actual source table receipt, not this expected
shape alone, is the authority.

Three exact plasma snapshots already exist in `primat_source_reference/`:
electron `0c03542043bd1b1a`, QED e2 and e3. Reuse their authenticated bytes.
The earlier NEVO thermodynamic snapshot explicitly normalized CRLF to LF:
local 105,643 bytes/SHA `7b5d0ad0a1f61ac10211da485122e4c54f903637243e280dbe6ff41681d2eab7`,
upstream 106,243 bytes/SHA `5df90294a15118bc6815bfcb2f7f4134e7924e026798adf739e1b66a91531699`.
It is valid numeric input under its recorded normalization, but must not be
represented as raw byte-identical upstream. No silent newline conversions or
replacement of that old evidence are authorized here.

## 3. Cache identity and the fail-closed change that is actually needed

Independent canonical-JSON/hash arithmetic, using the pinned C defaults,
gives the following exact filenames relative to `primat/data/`:

```
cache_plasma_weak/plasma/QED_pressure_correction_e2.txt
cache_plasma_weak/plasma/QED_pressure_correction_e3.txt
cache_plasma_weak/plasma/electron_thermo_0c03542043bd1b1a.txt
cache_plasma_weak/weak/nTOp_4a901fa9a22a2694.txt
cache_plasma_weak/weak/nTOp_thermal_161a90e5f33a626a.txt
```

Constants subset hashes are weak `4ab3da329a744f2d`, thermal
`947c354d0bb81d7f`, electron `9b50cb6e5f18cc20`, QED
`386578535a377e55`; both QED files require fingerprint `f93000cee7e086cf`.
All canonical fields are retained as literal JSON strings in the manifest
so `40.0`/`100.0`/`0.0` cannot silently become integer tokens. The
cache hash is the first 16 hex characters of SHA256 of sorted compact JSON;
do not substitute a filename guess or only compare its suffix.

At these fixed ordinary histories, changing omega_b, h, scalar density, the
hard gap or neutron lifetime does not change the stored weak integrals.
Lifetime normalization is applied separately. This is conditional on the
same Tnu(Tgamma), spectral data and ordinary constants, not a claim that real
neutrino reheating is expansion-independent. Fingerprints key NEVO paths,
not their raw contents, so separate complete data-byte authentication is
essential. Numerical background sampling is part of the nonthermal cache
key; changing it from 600 to 1200 points/decade cannot be called an unchanged
cache hit. Any independent background-representation refinement must preserve
and explicitly name the fixed cached-rate grid rather than silently rekeying
or recomputing ordinary rates.

The inspected fallback behavior is concrete:

* QED first requires both current files to match their fingerprints. It can
  otherwise accept legacy tables or compute new pressure tables. Disallow
  both fallback routes in the derived read-only branch.
* Electron mismatch/miss/read failure falls through to quadrature and then
  attempts cache-directory creation and writing even with the normal
  recompute flag false. Setting output flags false is therefore insufficient.
* Nonthermal weak and thermal readers test existence of the generated
  filename, not the file's fingerprint header. Missing nonthermal data runs
  quadrature; missing thermal data runs VEGAS. Turning off save flags alone
  prevents some writes, not this scientific generation.
* `cpr_cache_write` creates a temporary file and renames it over its target.
  It is not a safe no-overwrite publication interface and must never be
  reached by the new adapter.

Minimal derived guards reject a missing, unreadable or mismatched current
cache **before** each generation/legacy branch. Preserve upstream sources
and publish exact derived diffs. Before launch, independently bind raw hashes,
fingerprint headers, finite values, positive monotone temperature grids and
column counts; require matching e2/e3 row counts and temperatures (the loader
indexes the second array using the first one's count). Thermal corrections
are signed; do not impose positivity on each thermal column. Require
nonnegative *total physical weak rates* at the actual solver evaluations.
The ordinary `cpr_compute_fn` normalization still performs small deterministic
quadratures on cache hits; it is not table generation and must not be omitted.

## 4. Contained adapter and serial build

Use one explicit absolute data root under this project, no environment-based
data search, no `~` expansion, no user-nuclear/cache overlay, no custom network.
Check every resolved path remains under that root. Set and assert:

```
custom_background=NULL; external_scale_factor=0;
user_nuclear_dir=NULL; cache_dir=NULL;
weak_rate_cache=1; save_nTOp=save_nTOp_thermal=0;
recompute_electron_thermo=recompute_qed_corrections=0;
all output_* file switches=0; decay_era=0;
show_progress=verbose=debug=0;
spectral_distortions=incomplete_decoupling=QED_corrections=1;
thermal_corrections=radiative_corrections=finite_mass_corrections=1;
analytic_distortions=0; all chemical potentials=0;
DeltaNeff=fEDE=0; extra_rho absent; rate variations absent.
```

Clear the optional `CPR_NN_DEBUG` environment flag. Do not call stock main,
CLI, MC, decay output or background writers. The direct in-memory sequence is
`config -> plasma -> nuclear_rates -> apply_variations -> standard_background
-> nuclear_network_solve -> assemble_results`, followed by reverse-order
cleanup. The adapter owns stdout JSON and stderr diagnostics; the parent
publisher retains raw streams/exit status on every failure. Capture full
configuration, raw data/source hashes, species/reaction order, background and
abundance history, all current/energy/reheating diagnostics, and initial-data
qualification. Do not only emit fitted D/H or helium summaries.

After source/data receipts and the small adapter/diffs are reviewed, a root-
owned serial build can use literal commands of the form

```
clang -std=gnu11 -O2 -Wall -Wextra -pthread -I<owned_include>
      -c <one_authenticated_source> -o <new_owned_object>
clang <literal_22_object_list> <new_adapter_object>
      <owned_material_object_if_candidate> -lm -pthread -o <new_binary>
```

No shell wildcard, `make`, `pip`, `ar` installation, network access, deletion
or system change is required. Retain full per-command argv, environment,
compiler identity, output and object/binary hashes; exact-receipt reuse only.
The ordinary build does not yet require the scalar material provider. A
candidate build adds the already qualified same-action material provider
and only the explicit H-matter replacement/current diagnostics from the
route note. It must not call the upstream custom-background shortcut, add
a second dark density or rematch Lambda.

## 5. Resource sizing and first useful qualification

This is a small serial chemistry problem, not a cosmological grid solve.
The small network has 8 species and 12 thermonuclear reactions plus n↔p;
HT integrates 2 abundances, then MT/LT integrate 8 with analytic Jacobians.
At default settings the background has approximately 2,761 temperature
nodes. The two 12-by-1000 forward/median/error table triples occupy 576,000
double-array bytes; the 600-by-80 retained neutrino distortion array is
384,000 bytes, before reader temporaries and smaller arrays. The fixed arrays
therefore have megabyte, not gigabyte, scale. These are allocation arithmetic,
not a measured RSS guarantee: accepted-step histories grow dynamically and
the remaining ODE/source files still require their own review. The README's
example runtime is not a runtime promise on this machine.

Use one default ordinary benchmark first, retaining elapsed time and actual
peak RSS; then one dust-replacement identity and the first already owned
finite-gap state with its unchanged proxy comparator. No simultaneous
producer, automatic large census or arbitrary wall-time cutoff is implied.
Numerical refinement must be prospectively separated into nuclear precision,
rate-grid interpolation, background ODE and temperature representation;
do not change a fingerprinted ordinary rate grid without an explicit new
input/qualification. Baseline, dust identity and physical candidate statuses
remain separate; a failed control must not delete or relabel a candidate run.

A useful exact initial-state diagnostic costs no second chemistry solve.
During HT, with the same specified background and Yn+Yp=1,

    dot Yn = Gamma_pn - (Gamma_np+Gamma_pn) Yn,
    |delta Yn(t_weak)| = |delta Yn(t_start)| exp(-K),
    K = integral_start^weak (Gamma_np+Gamma_pn) dt.        (1)

The source rates are physical s^-1 here. Thus a finite 10 MeV nuclear start
can report an actual contraction bound for arbitrary initial n/p fraction,
not merely rate/H at one point. Propagating this through Saha seeding and
nonlinear MT/LT chemistry requires the appropriate Jacobian/variation bound;
(1) alone is not a D/H or helium error bar. Positivity and baryon-number
residuals must be retained through all eras. Ordinary table/reaction
uncertainties and the changed-heating response remain distinct from numerical
convergence, and no missing joint theory covariance is invented.

The immediate deliverable is an exact, contained conserved-scalar versus
old-proxy abundance comparison under the same prescribed ordinary history.
It repairs the scalar source history, not every BBN approximation, and is
not a thermal-origin or neutrino-free-streaming test.
