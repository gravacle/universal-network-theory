# Ordinary PRIMAT baseline: independent preflight V001

Verdict: accepted for the declared root-owned transformation, build and two-profile qualification. No load-bearing correction is requested. This is a source/contract review, not a compilation, run, abundance result or convergence claim.

## Exact reviewed packet

All four files were read completely. Paths are relative to `joint_parent_continuation`; B denotes `bbn_inputs_v001/primat_c_reference_v001`.

| File | SHA-256 |
|---|---|
| `PRIMAT_ORDINARY_BASELINE_PROTOCOL_V001.md` | `f316e483e125a2bbb3076baf3c13eb21242a983b8df43668f600eaf05cff7af1` |
| `derive_primat_readonly_sources_v001.py` | `0810fd350466622689a115bca1f368a91d64b41b5faf9a13b768cb3d7b15b38f` |
| `B/derived_ordinary_v001/unt_primat_ordinary_v001.c` | `3021c54cf72e990875f763f7f44d597d05c202674ad13c9e2b152c343fdafc7a` |
| `B/PRIMAT_ORDINARY_BUILD_MANIFEST_V001.json` | `7df47e6d272a326d56b1067f75d59f18e5a9f8b0f0104e1856275c8737e27f90` |

The manifest binds upstream commit `4bf97d5082eee54b9df50d88f43182bb651fea80`. Relevant pinned upstream configuration, plasma, weak-rate, background, network, result-assembly, logging and ODE code was also inspected directly; the review did not execute the transformer or import a producer.

## API, physics and units

The direct initialization/solve/result-assembly sequence matches the library API. The eight-species order is verified against the actual LT network before its integer mass numbers are used. The adapter reports the library's distinct BBN and CMB helium conventions without substituting one for the other; D/H uses the final proton abundance. The retained HT initial neutron fraction is the upstream rate-balanced seed, not a new preparation inferred from the memory diagnostic.

Background temperatures and Hubble arguments are MeV, while weak-rate accessors take Kelvin. The explicit conversion is in the correct direction. Background time and H are seconds and inverse seconds, and `cpr_bg_rhoB_BBN` returns g/cm^3. The physical rate accessors include the library neutron-lifetime normalization. Signed thermal corrections are not confused with nonnegative total rates. The log-time integral uses dt=t d(log t), including the required factor t, and both Simpson weights are correct.

The ordinary standard background and fixed NEVO prescription are unchanged. In particular, the documented omission of baryon rest energy from the upstream Hubble sum is preserved, not silently repaired or advertised as a complete new cosmology. There is no candidate hard component, fitted abundance, altered reheating, or observational success gate.

## Fail-closed input and output boundary

Both transformed units preserve valid-table interpolation and normalization. The QED guard precedes analytic generation and excludes all legacy layouts; paired grids must match. Electron-cache misses, fingerprint mismatches and read failures return before quadrature or writes. The weak-cache header checks precede loading; malformed nonthermal/thermal tables and thermal read races return before generation or VEGAS. Helpers reached before these guards only construct paths. Dead generation branches are retained in the text but are unreachable on this adapter's guarded route.

The adapter restricts arguments and all 24 input paths, rejects symlink-resolved substitutions, disables all output/cache gates, and calls no file-output API. Library logging uses stderr. JSON nonfinite values are exposed as null and cause failed qualification rather than being silently dropped; intentional above-10-MeV weak-rate nulls are distinguished. Complete raw process stdout/stderr and abnormal termination remain the root invocation receipt's responsibility.

This packet supplies an explicit manifest and manual execution contract, not an executable build supervisor: root must enforce exact input/derived hashes, absent-or-authenticated output targets and command receipts before executing literal argv. Acceptance does not substitute for those checks or authorize unexplained overwrites.

## Refinement, evidence and bounded work

The two profiles retain identical physical inputs, tables, background sampling, initial state and network; only nuclear relative tolerance changes by ten, retaining upstream absolute tolerances and LT multiplier. This is a fair nuclear-ODE refinement, not evidence of independent background/cache/NEVO convergence. Full library history is retained without adapter clipping or selection (the upstream assembler itself omits duplicate MT/LT seed rows); raw signed abundances and conservation defects remain inspectable.

The declared abundance/refinement controls and HT quadrature comparison are fixed before outcomes. `COMPLETE_ORDINARY_ONLY` does not imply the cross-profile comparison passed. The exact two-state HT memory identity is correctly distinguished from its approximate quadrature and from nonlinear final-abundance sensitivity.

Work is a fixed small network, fixed table grids, and one serial process. Upstream RK caps attempts at 100000 and BDF at 200000 per invocation, with finite Newton/step-floor handling; these are inherited solver safety limits, not scientific acceptance thresholds. Histories scale with accepted steps and must be captured in full. Runtime/RSS are not measured by this review; the protocol's default-first measurement and preservation of any failure are essential before proceeding to the refined profile. No new wall-time, tolerance or data-dependent retry rule is introduced here.

No compiler, producer, source transformer, numerical integration, download or upstream edit was performed in this review.
