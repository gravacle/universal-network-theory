# CLASSICAL-IMPORT LEDGER: the 120/43 chain

Date: 2026-10-12, as of about 16:05 CDT
Author: Claude (audit lane, read-only)
Principal: "We need to be careful here not to import classical machinery into the analysis." (relayed in TO_CODEX/0100:1)
Rule applied: TO_CODEX/0100:7-19. The native verdict comes from canonical dynamics on actual graphs and states, using exact or explicitly bounded reductions. A classical construct may appear only as a labelled conditional diagnostic. A load-bearing import counts as a declaration until it is replaced.

Paths are relative to `/Users/bgm/Research/UNT_EXCHANGE/` unless absolute. Raw audit notes are in this directory:

- `P47-P49.md`
- `P42-P45-P41-P43.md`
- `P46-P50-P8.md`

Nothing outside this directory was modified, and no project or Codex code was executed.

Role definitions:
- **LOAD-BEARING (LB):** a verdict, label, interface variable, criterion or physical provider on the 120/43 path depends on the construct.
- **UNCLEAR (U):** the construct is labelled or deferred, but it is the only stated route to a native verdict, or its classical status is undecided.
- **DIAGNOSTIC (D):** a labelled control, exclusion or conditional column. No verdict depends on it.

## Counts

| Audit | Packets | LB | U | D | Items |
|---|---|---|---|---|---|
| 1 | P47, P49 | 2 | 3 | 20 | 25 |
| 2 | P41, P43, P42, P45 | 16 | 5 | 17 | 38 |
| 3 | P46, P50, P8, TO_CODEX 0074/0077/0098 | 18 | 3 | 13 | 34 |
| **Total** | | **36** | **11** | **50** | **97** |

The table below has 43 rows covering the 47 LB and U items. Four pairs are merged: C6, C10, C16 and C17.

Status of the 36 LB items:
- **27 LIVE.**
- **8 superseded or addressed:**
  - B2 and B8-B11 by TO_CODEX/0100:4,22,24.
  - D2 and D3 by TO_CODEX/0077:8,16.
  - B1 by root's retirement of the criterion.
- **1 partly superseded:** D5.

Claude's own TO messages carry 12 of the 36 LB items: 0074 (3), 0077 (3), 0098 (5) and the 0097 registration (1). Three of those are still live: A2, B7, and the 0077 half of C6.

### Reconciliation with root's ledger

Root's ledger is at `/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/ROOT_UNT_LOCAL_RESIDENCY_MANIFEST_V002/exploratory_physics/PHASE12_PARALLEL_SCREEN_V001/H_record_front_provisional_V001/NATIVE_COEFFICIENT_DEPENDENCE_AUDIT_V001/FRESH_RECOVERY_AND_VALIDITY_2026-10-12_V001/CLASSICAL_IMPORT_LEDGER_V001.json` (15:56), announced in FROM_CODEX/0064:5. What it already does:
- It adopts no load-bearing import.
- It retires the 1/r flat-curve criterion (`retired_intermediate_criterion`).
- It labels the P47 momentum-strip, Fourier and diffusion material diagnostic (FROM_CODEX/0064:11).
- It forbids v²=r·g and a declared Euclidean radius for P46.

What it misses:
- **P41 and P43 are absent.** That leaves out the one-metric template and the GR weak-field must-pass fixtures that decide every universality label (C1-C6).
- **P8 is absent** (E1-E4).
- **The P46 entry does not cover the baryonic-source representation** (A1-A3).
- **The labels and the task text disagree.** Root's ledger labels these constructs, but PLAN task text still uses template, kernel and ρ(r) vocabulary (PLAN.md:48,49,51; plan/plan.tsv:44,47,48). plan_log has a P-46 status line for 2026-10-12T20:59Z, but the plan.tsv:47 task and DONE_WHEN are unchanged. Rows append and never renumber, so each correction becomes an appended successor row.

## 1. Load-bearing and unclear imports

### A. Baryonic source

| # | Packet | Construct | Where | Role | Status | Native replacement |
|---|---|---|---|---|---|---|
| A1 | P46 frozen input | Newtonian force templates as the baryonic source: SPARC Vgas/Vdisk/Vbul are Poisson thin-disk solutions, with gbar=v²/r | lanes/P46_CODEX2/FROZEN_NGC3198_INPUT_V001.json:698 `PUBLISHED_NEWTONIAN_FORCE_TEMPLATES...`, :11 `gas_density_provided: false`; prediction_harness_v001.py:53-57,63; nonlinear_record_chain_interface_v001.py:35; P46_S1_PAIRED_CHAIN_PROTOCOL_V001.txt:77 | LB | LIVE; not in root ledger | Pin raw surface densities: HI Σ_gas ×1.33, and 3.6 µm SBdisk/SBbul with counted M/L and vertical structure. Map them through the P50 dictionary into the P47 full matter-arm preparation. Force templates stay METHOD-only. |
| A2 | TO_CODEX/0074 | Rotmod gas/disk/bulge components as the harness source | TO_CODEX/0074:9 | LB | LIVE through A1; never superseded | As A1. |
| A3 | P8 contract and handoff | "Observed target baryons remain prediction inputs", with no field for their representation | lanes/P8_CODEX3/P8_SINGLE_MAGNITUDE_IDENTIFIABILITY_CONTRACT_V001.txt:126-127; P8_TO_P9_HANDOFF_TEMPLATE_V001.json:10-54 | LB | LIVE | Add a handoff field for the native baryonic-source representation: surface densities plus counted M/L, helium and vertical declarations. Exclude force templates from physical F. |
| A4 | P8 | P31 Keating-type bond-angle source law listed in scope | P8 contract:10-12; TO_CODEX/0027:10 | U | LIVE | A P8 successor names the source as the native matter preparation (P50 candidate plus P47 full-arm state) and drops P31 from F, consistent with TO_CODEX/0077:8,12. |

### B. Matter → Records (P47 field law and range)

| # | Packet | Construct | Where | Role | Status | Native replacement |
|---|---|---|---|---|---|---|
| B1 | P47 0118 registration | Newtonian flat-curve criterion: "A flat rotation curve needs a slowly falling footprint, so it cannot come from the direct cloud" | TO_CODEX/0097:19; registered at FROM_CODEX/0060:11 | LB | ADDRESSED: retired by root (FROM_CODEX/0064:5; root ledger `retired_intermediate_criterion`). The receipt text is immutable by design. | The registered physics is the native conditional result only: an exponential upper bound on exterior erasure probability in the gapped fixed-ice one-resource branch, with length 1/[2 acosh(1+Δ/(2\|t\|))] in graph steps and contact-only at t=0. The native chain decides any contribution to the 43 velocities. |
| B2 | TO_CODEX/0098 | Sealed "flat curve needs a 1/r pull" criterion (v²=r·g) | TO_CODEX/0098:14 | LB | SUPERSEDED by TO_CODEX/0100:4,24 | The only macro test is the native 43 velocities against data, with one counted calibration. |
| B3 | P47 0126 Trajectory V002 | 3D Euclidean shell growth and continuum density a⁻³ used to exclude 1/r, 1/r² and 1/r³ tails; cost Δ·2πCR²/a³ | lanes/P47_CODEX3/P47_TRAJECTORY_IMPRINT_GREEN_CONTROL_AND_ENERGY_BOUND_V002.txt:176-185 | LB | LIVE. The V002 §9 self-ledger covers only :184. The class-2a review is queued (FROM_CODEX/0064:13). | State the native bound Σ_y f_y ≤ (⟨H_red⟩_init − E_min + \|g\|)/Δ on the actual graph. Convert it to excluded profiles only through that graph's actual shell census N(r). The occupied fixed-ice graph has degree two (P47_LONG_RANGE_CLOUD_AND_MEDIATION_THEORY_V001.txt:92-94), so the excluded set is any non-summable f along the cycle or path. Drop d, 3D, a³ and 2π. |
| B4 | P47 0125 Same-H V002 §7 | 3D isotropic continuum Fourier identities (1/k²→1/r, gradient→1/r², Laplacian→contact, Yukawa) as the only stated route from a k-space singularity to an algebraic range verdict | lanes/P47_CODEX3/P47_SAME_H_MEDIATED_RESPONSE_AND_RANGE_TESTS_V002.txt:198-208 | U | Root labels it diagnostic (FROM_CODEX/0064:11), but no native algebraic route replaces it | Decide algebraic versus exponential from the complete native χ_OS(x,y) in real space on actual graph families. Use interaction-graph distance, the actual shell census and the §8 finite-size discriminants. Any dimension, isotropy or continuum must come from derived Record geometry (P42/P45) and be counted. |
| B5 | P47 0125 Same-H V002 §7 | Exponential test by analytic continuation in a momentum strip \|Im(k·r̂)\|<μ, which needs a translation family | same file :181-186 | U | As B4 | The anchored Birth breaks translations of the joined domain (P47_SYMMETRY_SHAM_AND_HISTORY_COMPARISON_V001.txt:47-49). Use a graph-distance weighted-norm (Combes-Thomas) bound on the complete χ_OS over the actual interaction hypergraph, Birth patch included, as 0118 §5 does with S_μ=exp(μD). |
| B6 | P47 0125 Same-H V002 §8 | Unspecified "physical/native distance chart" frozen for the finite-size range test | same file :228-229 | U | LIVE | Freeze interaction-hypergraph distance, or derived Record geometry from matter- and light-defined lengths with the chart counted. A Euclidean "physical" chart would be a counted declaration. |
| B7 | TO_CODEX/0077 | Record density ρ(r), a radial continuum profile, as the 120/43 interface variable (P-47 "fall-off with distance") | TO_CODEX/0077:11-12; plan/plan.tsv:48 | LB | LIVE in the P-47 task text | Pass the full Record state (words and correlations on actual graphs, indexed by graph distance). Any ρ(r) is a counted, explicitly bounded coarse-graining. lanes/P46_CODEX2/NONLINEAR_NATIVE_RECORD_CHAIN_PROTOCOL_V001.txt:30-32,45-48 partly mitigates this. |
| B8 | TO_CODEX/0098 | Emergent Gauss charge plus Coulomb/Gaussian-Maxwell U(1) polarization with a 1/r² field, framed as the "deciding item" | TO_CODEX/0098:6,8. Propagated to lanes/P47_CODEX3/P47_GAUSS_CHARGE_POLARIZATION_AND_SCREENING_CHANNELS_V001.txt:13-14,138 (FROM_CODEX3/0124). | LB | SUPERSEDED (TO_CODEX/0100:4,22). The residue is cleared: V003 §9 excludes it from the verdict. Finite h breaks the local degree Gauss constraint (lanes/P50_CODEX3/P50_CANONICAL_MATTER_DICTIONARY_V002.txt:96-97). | Use the 0125 same-H Lehmann/Liouvillian response and correlations on actual graphs. Confirm the P47 verdict has no dependence on 0124. |
| B9 | TO_CODEX/0098 | Record-polarization channel with its fall-off inherited from channel 1's 1/r² | TO_CODEX/0098:9 | LB | SUPERSEDED | Keep the native −λ_R d q term. Measure the matter-minus-sham Record difference against graph distance under full V005, with no inherited profile. |
| B10 | TO_CODEX/0098 | Debye-like screening of background carriers | TO_CODEX/0098:10 | LB | SUPERSEDED. "Screening" is OPEN in P47_GAUSS...V003.txt:259-261. | Use the native connected response of the derived S1 background on actual graphs, exact or bounded at each distance, with a finite-size trend. Any later use of "screening" means a property of the native χ_OS, not a Debye mass. |
| B11 | TO_CODEX/0098 | Output template: fall-off form with order/remainder and a screening length (a continuum radial taxonomy) | TO_CODEX/0098:13 | LB | SUPERSEDED. The residue is live as B4-B6. | Exact or bounded response at each graph distance, with finite-size scaling. Any power-law or exponential fit is labelled diagnostic. |

### C. Records → geometry, light and clocks (P41, P43, P42, P45)

All four packets serve one criterion: a 3+1 Lorentzian/ADM four-object template. It is also the only ρ→geometry map these packets define.

| # | Packet | Construct | Where | Role | Status | Native replacement |
|---|---|---|---|---|---|---|
| C1 | P41 V002 | ADM one-metric quadratic dispersion template: lapse N, spatial inverse metric B, zero shift, ħ=c_ref=1. Invariants M1 (I1=E/C constant, EK=L) and M2 (I2=1). | lanes/P41_CODEX3/P41_ONE_METRIC_CONDITIONS_AND_EXTENSIONS_V002.txt:14,19-22,30,32 | LB | LIVE; P41 not in root ledger | The same-state native response vector: dlnC_j for every clock line, dlnE, dlnK_ij, the change in light-branch dispersion, and inter-line ratios. Register any V005 operator identity that ties them (the C1-C3 commutant form; the P45 K_b R multiplier). I1 and EK=L survive only as labelled conditional columns. |
| C2 | P41 V002 | Metric reconstruction N=C/ν0, m=E/N, B=L/N², plus a density-independent proper clock and mass (clock hypothesis/EEP). This is the only ρ→geometry map. | same file :16-18,37-39; PLAN.md:52 | LB | LIVE | Hand P-46 native same-state quantities (E_rest, K, all clock lines, and light-branch dispersion against the Record word), not N and B. Measure any force or orbit law from carrier propagation in a V005 state with a Record-density inhomogeneity: the Q1 Green function on the actual graph, with bounded remainders. A potential reading is diagnostic only. |
| C3 | P41 V002 | GR isotropic weak field (N=1+Φ, a=1−Φ; fractional slopes 1, 1, 2, 3), used to widen "universal" beyond the native common-multiplier criterion | same file :5-11,69-75 | LB | LIVE | Use positive controls that follow from V005 operator identities: the common multiplier on every owner (P41_CANONICAL_OWNER_DIAGNOSIS_V001.txt:107-117) and the identical-projector ring scaling (lanes/P45_CODEX2/P45_SIXTH_ORDER_UNIFORM_DIAGONAL_AND_ENDPOINTS_V001.txt:84-91). Register unequal fractional-shift patterns as measured patterns. |
| C4 | P43 | One-metric comparator: I1=E/C, I2=KE/v², T=(EK)L⁻¹, with labels UNIVERSAL_COMPATIBLE and SPECIES_DEPENDENT | lanes/P43_CODEX3/P43_ONE_METRIC_PROTOCOL_V001.txt:30-45; P43_SPLIT_METRIC_PROTOCOL_V002.txt:6-24,56-64,74-97; one_metric_comparator_v003.py:50-60,86-115; PLAN.md:48 | LB | LIVE (P-43 DONE) | A native-response comparator. Inputs: the measured response vector, every clock line, inter-line ratios and pattern dependence at fixed density. Test only identities derived from V005 for that family. Metric labels become conditional columns. |
| C5 | P43 | Baseline I2(r0)=1, i.e. local Lorentz invariance or Klein-Gordon EK=c² | P43_SPLIT_METRIC_PROTOCOL_V002.txt:7-22; one_metric_comparator_v003.py:86-87 | LB | LIVE | Report the native dimensionless KE/v² (and T0) as a measured number traced to V005 owners. Do not judge COMPATIBLE or MISMATCH against 1. |
| C6 | P43 + TO_CODEX/0077 | GR weak-field fixtures as must-pass positive controls (clock 1+Φ, light 1+2Φ, rest 1+Φ, kinetic 1+3Φ); "one geometry" as the gravity-verdict criterion | P43_ONE_METRIC_PROTOCOL_V001.txt:128-151; P43_SPLIT_METRIC_PROTOCOL_V002.txt:121-128; ONE_METRIC_FROZEN_FIXTURES_V003.json:65,116,121,177,233; PLAN.md:49 (P-43 Done-when); plan/plan.tsv:44; TO_CODEX/0077:10,17 | LB (2 items) | LIVE. The 0077 half is Claude-authored. | Generate positive controls from V005 operator identities on actual graphs. Universality is a finding, not a pass criterion. A non-universal outcome registers as itself. |
| C7 | P42 | Maxwell constitutive optical algebra: a reciprocal local quadratic Maxwell action, ε=ħU_E⁻¹, μ=ħU_B⁻¹, and a single cone iff U_B=ζU_E | lanes/P42_CODEX2/P42_PATTERNED_OPTICAL_MSCM_PROTOCOL_V001.txt:130-160,239-245; patterned_optical_algebra_v001.py:72-99 | LB | LIVE. Root calls light "unqualified" but does not list the Maxwell route as an import. | Measure the lowest incidence-sector excitation branches of the same-state V005 effective operator, direction by direction, on actual graphs. Include the E2/E4/h6 and Born terms, and use the flip/ring dynamical structure factor. Register degeneracy or splitting as measured. An ε/μ fit is diagnostic only. |
| C8 | P42 | Photon velocity from the Maxwell stiffness product v²=U_E U_B, the only declared light route | P42_BINARY_FAMILY_AND_SAME_STATE_RESPONSE_V003.txt:179-206 (:205); binary_family_response_contract_v004.py:87-92; P42_CONTROL_AND_NATIVE_HANDOFF_CONTRACT_V001.txt:64; PLAN.md:48 | LB | LIVE | Take v_light from the same-state small-k pole or structure-factor peak of the V005 incidence operator on actual graphs. The P45 identity v1/v0=T(x1)/T(x0) is the template. The stiffness product becomes a cross-check. |
| C9 | P42 | Gauss-law field identification: E_link=n−1/2, ice divergence-free, U_d as Gauss-defect energy, and κΦ²/(2L) defining κ_E | P42_BINARY...V003.txt:173-189; P42_PATTERNED...V001.txt:120-128 | LB | LIVE | Report the winding-sector energies E(F) of the V005 operator on the actual torus directly, as P42_SECOND_FOURTH_ORDER_DIAGONAL_TERMS_V002.txt:59-77 does for h2. Do not convert them to a Maxwell κ_E. |
| C10 | P42 + P45 | Emergent U(1) Coulomb/deconfined phase presupposed for light (transversality, two polarizations); stiffnesses that "inherit [the] common multiplier" | P42_BINARY...V003.txt:179,197-206; P42_SECOND_FOURTH...V002.txt:155-163; P45_SIXTH_ORDER...V001.txt:84-101 (:95); P45_SAME_REFERENCE_ENDPOINT_ASSEMBLY_V001.txt:91-94 | LB (2 items) | LIVE | Define the light probe as the lowest incidence-sector excitations of V005 (the spectrum of the ring operator R and of the full joined operator) on actual graphs, whatever their gap or branch structure. There is no Coulomb-phase prerequisite. |
| C11 | P42 | Optical metric ds²=−dt²+dxᵀL⁻¹dx as the native outcome QUALIFIED_COMMON_OPTICAL_METRIC | P42_PATTERNED...V001.txt:162-166,239-245 | LB | LIVE | Report the native light-branch dispersion tensor as measured. A metric reading is diagnostic only. |
| C12 | P42 | MSCM criterion ported from the WA corpus: Klein-Gordon species E=√(C0/Ct), a single photon c, all EK=c², reconstruction N=E_ref/M and a=N/c, and a global Weyl scale | P42_PATTERNED...V001.txt:35-46,168-196 (173-178); mscm_p43_crosswalk_v001.py:25-35,107-109 | LB | LIVE | Use the native multi-species signature: gap ratios E_a/E_b, E_a K_a and line ratios in graph units across states. Register any V005 identity found. No (N, a) reconstruction. |
| C13 | P42 | Clock-as-lapse reading of the X_record spectral line inside I1 | P42_BINARY...V003.txt:146-170,213-214; P42_SAMPLING_WEIGHTS_AND_CLOCK_SPECIES_V001.txt:50-51 | LB | LIVE | Report every X_record line and inter-line ratio as native spectral data, with no lapse attribution. |
| C14 | P45 | Endpoint invariant equations I1(1)/I1(0)=η_E/η_C and I2(1)/I2(0)=η_Kη_E/τ², with baseline I2(0)=1, handed to the P43 comparator | P45_SIXTH_ORDER...V001.txt:162-182; P45_SAME_REFERENCE...V001.txt:115-120,133-134; formal_endpoint_handoff_v002.py:16-30; PLAN.md:51 | LB | LIVE | The result is the native endpoint ratios η_E, η_K, η_C and τ from the assembled V005 operator H1,b. I1/I2 becomes a labelled diagnostic. |
| C15 | P45 | Zero-feedback same-reference obstruction worded as a metric verdict ("I1 and I2 cannot both be density-independent") | P45_H2T_MATCHED_HOPPING_AND_SAME_REFERENCE_SUBCASE_V001.txt:80-83; H2T_SOURCE_CONTRACT_V001.txt:50-55 | LB | LIVE | Register the native finding as it stands: rest energy shifts by the scalar E1−E0, while projected kinetics, the ring operator and the X line are identical. |
| C16 | P43 + P42 | Homogenized k→0 coarse observables as the verdict target | P43_CLOCKS_AND_PERIODIC_ADDENDUM_V003.txt:10-12; P42_BINARY...V003.txt:226-233; P42_HOMOGENIZATION_AND_READOUT_NOTE_V001.txt:5-12 | U (2 items) | LIVE | This is native on periodic proxies (Bloch). For a possibly disordered P49 background, define long-wave observables on actual finite graphs (spectral and propagation quantities with finite-size bounds). Register a missing chart as UNDETERMINED. |
| C17 | P42 + P45 | Reference state = ground projector of the Q0 sector, a zero-temperature selection | P42_BINARY...V003.txt:24-30 (deferred in P42_TO0084_BACKGROUND_DERIVATION_ADDENDUM_V001.txt:1-11); P45_SAME_REFERENCE...V001.txt:81-82 | U (2 items) | LIVE | Use the P49-derived background: the state V005 unitary dynamics reaches from a declared preparation or history (P-18) in the exact conserved sector. |
| C18 | P45 | Shared wavevector chart/Hessian, with tensor channels routed through the P42 optical dyadic | P45_SAME_REFERENCE...V001.txt:105-120 | U | LIVE | Build tensors from the native band Hessian and the native light-branch dispersion in graph-translation (Bloch) coordinates, not from the P42 area/rotor dyadic. |

### D. Geometry → orbits and output (P46)

| # | Packet | Construct | Where | Role | Status | Native replacement |
|---|---|---|---|---|---|---|
| D1 | P46 harness + PLAN | Static response kernel → potential → v_c, with an ADDITIVE_CORRECTION baseline (native effects added on top of Newtonian gravity) | lanes/P46_CODEX2/prediction_harness_v001.py:173-185 (177,180),202-203; SOURCE_MILESTONE_PROTOCOL_V001.txt:21-23; plan/plan.tsv:47 | LB | LIVE in the task text: plan_log 20:59Z records the TO0100 constraint, but plan.tsv:47 is unchanged | A P46 successor and an appended P-46 row retire the kernel/potential/additive route. The physical entry becomes the S1 paired full-arm chain with TOTAL native response only and no Newtonian baseline (TO_CODEX/0077:1). |
| D2 | TO_CODEX/0074 | Pipeline: source → static kernel → matter coupling → potential → v_c(r), with v²=r·g | TO_CODEX/0074:10-14 | LB | SUPERSEDED by 0077:16 and 0100:23. The residue is D1. | As D1. |
| D3 | TO_CODEX/0074 | The P-37 kernel (bond-angle response, Ward/CR-classified) as the expected physical plug-in | TO_CODEX/0074:12,22 | LB | SUPERSEDED: 0077:8 makes P-37 diagnostic | The plug-in is the P47/P49/P50/P42 native chain. |
| D4 | P46 | Circular speed at a Euclidean radius R=D·θ (tilted-ring circular deprojection) as the chain output and comparison target; "potential/geodesic specification" in the S1 handoff | prediction_harness_v001.py:60-61,131-153; nonlinear_record_chain_interface_v001.py:36-40,81-88; s1_paired_record_chain_v001.py:40-43,100-101; P46_S1_PAIRED_CHAIN_PROTOCOL_V001.txt:76 | LB | LIVE. Root forbids a declared Euclidean radius map, and Codex2 is preparing a native motion and operational-length contract (FROM_CODEX/0064:13). | Lengths are light- and matter-defined from the derived geometry. Motion is UNT matter transport: dressed-carrier dispersion and group velocity in the derived Record environment (TO_CODEX/0100:23). Count the residual D·θ and deprojection chart as a P8/P9 declaration. Drop potential/geodesic from the S1 handoff. |
| D5 | TO_CODEX/0077 | Static N(r), a(r) metric ansatz with a metric → orbit readout | TO_CODEX/0077:16 | LB | PARTLY SUPERSEDED (0100:23) | Use dressed-carrier dispersion and transport in the derived Record environment, with a lapse only where it is derived from matter dynamics (P41 owners). |
| D6 | P46 | Fixed records → geometry → orbits staging (the geometric intermediary from 0077) | nonlinear_record_chain_interface_v001.py:67-78; s1_paired_record_chain_v001.py:83-94; NONLINEAR_NATIVE_RECORD_CHAIN_PROTOCOL_V001.txt:6-9 | U | LIVE | The successor states that the geometry stage holds only what P42/P45/P41 derive from matter dynamics, and that the orbit provider may act directly on the full Records state. It already receives that state upstream. |

### E. Forward law, units and gates (P8)

| # | Packet | Construct | Where | Role | Status | Native replacement |
|---|---|---|---|---|---|---|
| E1 | P8 | Forward law from P7's static χ(k) (a Newtonian / modified-at-small-k classifier) and P32's response/1PI plus Ward/GL6CR gates | P8_SINGLE_MAGNITUDE_IDENTIFIABILITY_CONTRACT_V001.txt:13-14,27-28,137-138,148; plan/plan.tsv:8,33 | LB | LIVE. Predates 0077; P8 not in root ledger. | F(A;...) is the native S1 full-arm chain: the P49 background, the P47 arms, the P50 dictionary, P42/P45 derived geometry, and the native matter-motion and observation map. Gates become V005-native certificates (conservation and symmetry such as P48, bounded-reduction errors and finite-size errors). Ward/CR and kernel shape are diagnostic only. |
| E2 | P8 | Length/coframe/clock solder map from graph units to kpc and s | P8 contract:79-81 | LB | LIVE (labelled as a declared correspondence) | Derive lengths as light- and matter-defined lengths from P42/P45 geometry (0100:23), and count any remaining chart. |
| E3 | P8 | Unit route E_unit=m_H c²/e_B (a rest-energy plus hydrogen correspondence); the only named unit route | P8 contract:83-86; P8_INDEPENDENT_REVIEW_CONTROL_DESIGN_V001.txt:18-21 (C7) | LB if selected | LIVE | Take c from the same-state light-branch speed (the C8 replacement). e_B is a V005 same-reference addition observable. The m_H identification is a counted declaration (P8:150). |
| E4 | P8 | Continuum extrapolation and continuum errors in the forward map | P8 contract:72-73,125-126 | U | LIVE | Either an explicitly bounded reduction on actual graphs, or absent from F. |

## 2. Diagnostic imports (50, brief)

These are all labelled conditional, refused, or used only as controls. No verdict depends on any of them.

**P47, 14 items:**
- **0125 Same-H V002:**
  - Imaginary-time and ground-state clustering, thermal ρ=f(H), isothermal reweighting (:32-33, 84-86, 188-196). This does not apply to a history-prepared P49 background.
  - Diffusive pole Dk²/(−iω+Dk²) (:210-216).
- **0124 Gauss V003:**
  - Conditional Coulomb/Gauss phase, E=Qr̂/(4πr²), dipole r⁻³ (:8-16, 138-163). §9 excludes it from the verdict.
  - Debye, screened Poisson, Yukawa and dielectric renormalization (:173-210).
  - U(1) test (iv), continuum div E chart, point-group and Wick arguments (:44-49, 89-90, 128-136, 165-171).
  - The microscopic G=η(d−2) operator algebra is native.
- **0126 Trajectory V002:** CTRW, Poisson flips, detailed balance, Feynman-Kac, the 3D lattice Green function → 1/r, heat kernel t^-3/2, Brownian erfc, diffusive and ballistic windows (:9-11, 29-113, 115-138, 147-150). §7's native energy inequality blocks transfer.
- **0118 P47_LONG_RANGE_CLOUD_AND_MEDIATION_THEORY_V001:**
  - Corpus linearized-GR Ward and k²-defect classifier, Debye mass, cubic-torus comparator (:323-344).
  - Continuum ΓDΓ, Coulomb and hydrodynamic heuristics (:239-241, 258-265, 267-272, 279-281).
  - Physical length and per-baryonic-mass conversion, refused (:176-179, 315-321).
- **0093 P47_NATIVE_RECORD_FIELD_LAW_FOUNDATIONS_V001:** corpus GR scaffolding, Poisson/diffusion estimator controls, thermal equilibrium as a candidate output (:3, 46, 93-96, 113-116, 218, 230-245, 249-251).
- **0094 HELD_P47_PROFILE_PROTOCOL_V001:** heat and Poisson estimator fixtures (:14-26).
- **Tracial controls (0096/0112/0119):** the "infinite-temperature" label on the native invariant-sector identity (P47_STATIONARY_NULL_AND_PREPARATION_DEPENDENCE_V001.txt:15-17; P47_NATIVE_A0_TRACIAL_CONTROL_THEORY_V001.txt:15-17, 50-53; HELD_P47_NATIVE_TRACIAL_PROTOCOL_V001.txt:13-17).
- **0100 S1 protocol:** EOS, ETH and "force" wording (P47_S1_FILLED_BACKGROUND_DIFFERENCE_PROTOCOL_V001.txt:13-17, 25-27, 80-82, 105-110, 122-125).
- **0110/0120 shams:** thermal/GGE, Gibbs, diagonal-ensemble, bath, golden-rule and Markov shams, all refused (P47_SYMMETRY_SHAM...:63-64; INDEPENDENT_SYMMETRY_SHAM_THEORY_REVIEW_V001.txt:20; P47_FULL_NATIVE_CONDITIONAL_ERASURE_RESPONSE_V001.txt:69-73, 110-112, 119-121).

**P49, 6 items:**
- **0064:** Gibbs/GGE EOS candidate, high- and low-T expansions, ETH and microcanonical shell (P49_RECORD_BACKGROUND_IDENTIFIABILITY_THEORY_V001.txt:15-24, 87-135, 137-158, 169-188).
- **0071/0072:** Gibbs β-series as exact Tr(OHⁿ)/D identities, with a cosmetic β (NATIVE_TRACE_HELD_PROTOCOL_V001.txt:50-59; ENSEMBLE_METHOD_HELD_PROTOCOL_V001.txt:14, 25-28; INDEPENDENT_NATIVE_FIXED_AV_INTERFACE_SOURCE_REVIEW_V001.txt:20-24; P49_DILUTE_CARRIER_AND_RELEASE_PROTOCOL_V001.txt:44-58, 85-92).
- **0078:** renewal, Born-Markov-secular, KMS and CTMC kinetics, outcome UNQUALIFIED (P49_DILUTE_CARRIER_KINETIC_DERIVATION_V002.txt:58-93, 95-145, 147-197, 242-254).
- **0070:** thermal two-level control (P49_QPOSITIVE_QUOTIENT_FRAGMENT_AND_EOS_CONTROL_V001.txt:98-99).
- **0066/0083:** corpus tensor target and model families (P49_ORIGIN_HISTORY_AND_SEED_UNIVERSALITY_V002.txt:37-41, 82-86).
- **0075/0081:** microcanonical/ETH distinctions (P49_ENERGY_CONDITIONAL_WORD_LAW_AND_CESARO_THEORY_V001.txt:26-31).

**P41, 8 items:**
- **Already native:** the C1-C3 common-lapse commutant criterion (P41_COMMON_LAPSE_CONDITIONS_V001.txt:15-32).
- **Disclaimed:**
  - Gibbs β_r N(r)=β0 (:66-68).
  - Transverse-photon, Lorentz, Ward and Einstein non-consequences (:93-94; P41_CANONICAL_OWNER_DIAGNOSIS_V001.txt:28-29, 124-125).
- **Unadopted extensions in P41_ONE_METRIC...V002:**
  - Extension A, exponential lapse (:125-140).
  - Extension B, ADM scalar and Maxwell H_A (:142-178).
  - Extension D, Einstein-Hilbert (:200-210).
- **Guarded statements in the same file:**
  - k-chart and shift (:58-63).
  - Sound-speed dichotomy (:77-84).

**P43, 2 items:**
- Periodic 1+1 metric field, informational only (P43_PERIODIC_METRIC_INFORMATIONAL_V001.txt:7-21, 39-44; P43_CLOCKS...V003.txt:34-45).
- Sound-speed negative fixture (P43_ONE_METRIC_PROTOCOL_V001.txt:137; ONE_METRIC_FROZEN_FIXTURES_V003.json:289).

**P42, 4 items:**
- Diamond embedding chart (P42_BINARY...V003.txt:73-81; P42_PATTERNED...V001.txt:91-94; patterned_optical_algebra_v001.py:155-172). Only chart-invariant combinations are used.
- Plaquette area and rotor dyadic (P42_PATTERNED...:94-101; py:175-185).
- Thermal/QMC provider route, unreleased (P42_PATTERNED...:266-276; P42_TO0084...:12).
- Metric-versus-medium framing (INDEPENDENT_PATTERNED_OPTICAL_SOURCE_REVIEW_V001.txt:49).

**P45, 3 items:**
- Admission counterexample with v0=v1=1 (P45_SIXTH_ORDER...:189-210; SOURCE_AND_METHOD_CONTRACT_V001.txt:56-64; formal_endpoint_handoff_v002.py:88).
- Frozen-cycle tight-binding curvature (SIXTH:115-121; SAME_REFERENCE:123-124).
- Gibbs mentions (SAME_REFERENCE:138-140; SIXTH:226).

**P46, 5 items.** All are METHOD controls.
- Newtonian TOTAL / NULL_ADDITIVE (prediction_harness_v001.py:69-85; SOURCE_MILESTONE_PROTOCOL_V001.txt:14-15; method_controls_v001.py:11-12, 22-25).
- RAR/MOND law (harness:78-81, 156-170; INDEPENDENT_COMPLETE_METHOD_SAVED_REVIEW_V001.json:25-29). Its χ² must never become a benchmark that native results are graded against.
- v²=R dΦ/dR (harness:88-117; predict_physical raises at :202-203).
- Manufactured lapse fixtures (interface:97-133; s1_paired_record_chain_v001.py:114-138).
- Exclusion guards (NONLINEAR...:8-9, 30-32; P46_S1...:9, 17-24; s1_paired_chain_controls_v001.py:25-28).

**P50, 4 items:**
- Local degree Gauss constraint, which is native (P50_CANONICAL_MATTER_DICTIONARY_V002.txt:76-78, 96-99).
- Emergent-EM vocabulary, used only to deny identification (:91-94).
- E_rest=mc² and m⁻¹=Hess/ħ², conditional and denied (:168-176; P50_BIND_CLOUD_SELF_ENERGY_AND_CURVATURE_V001.txt:107-111, 135-137; P50_REVIEWED_PROVIDER_CONVENTIONS_V001.txt:5-11).
- n=ρ/m conversion (:199-204, 70-74, 145-147).

**P8, 1 item:** measured G, Ward null, co-scaling and the rotation curve as forbidden selection sources (P8 contract:46-48, 106-112; control design:25-27).

**TO_CODEX, 3 items:**
- 0074 Newton/RAR/null METHOD controls (:17-19).
- 0077 GR scaffolding registered (:1).
- 0077 linearized-Einstein form demoted (:8).

**Watch items.** Each of these is diagnostic now and becomes LB if used:
- the P49 0078 kinetic route as a background provider;
- the P42 plaquette dyadic as the source of U_B;
- the P42 QMC phase route;
- the P50 n=ρ/m conversion;
- measured G as the P8 LAW_MAGNITUDE datum, which would presuppose a Newtonian two-body regime;
- any non-chart-invariant use of the P42 diamond chart.

## 3. Other findings (not classical imports)

- **TO0099 contradicted.** Same-H V002 §10 shows a persistent second-order same-H effect. That contradicts TO_CODEX/0099's claim that a lasting footprint can only come from conditioned correlations, non-perturbative effects or history. Claude's 0099 needs a correction.
- **P50 reduction not bounded.** The P50 cloud note omits incidence flips and Birth without a bound (P50_BIND_CLOUD...V001.txt:9-12), and its curvature remainder is unbounded (:57-59). By TO_CODEX/0100:7 that is not an explicitly bounded reduction.
- **Custody.** The P47 Gauss V002 title line still reads V001.
- **Counted empirical inputs.** These are not classical constructs but are counted: M/L 0.5/0.7, the ×1.33 helium factor and the 13.8 Mpc Cepheid distance.
- **Self-ledgers.** Codex3 and Codex2 post-TO0100 self-ledgers are accurate, except the B3 exclusion sentence. P46 S1 (15:03) and P8 (11:09) predate TO0100 and carry no ledger.

## 4. Classification of open items

- **Computed natively, available now:**
  - the P45 identities: c_b I + K_b R, with no h6 diagonal RK term, and v1/v0=T(x1)/T(x0);
  - P41 C1-C3;
  - the P42 winding-sector energies;
  - the 0118 graph-distance resolvent bound;
  - the 0126 native energy inequality;
  - the 0125 finite-graph Lehmann/Liouvillian identities (accepted at FROM_CODEX/0064:11).
- **Measured natively, not yet done:**
  - the light-branch spectrum of R and of the full joined operator on actual graphs;
  - carrier propagation in an inhomogeneous Record state;
  - the complete χ_OS in real space on actual graph families;
  - the native response vector across densities;
  - native matter motion and operational lengths (Codex2 contract in preparation).
- **Declared (counted):**
  - any residual graph→kpc chart (D·θ, deprojection);
  - the m_H identification;
  - M/L, helium, distance and vertical structure.
  - Under TO_CODEX/0100:19, every LB item still LIVE in §1 is a declaration until replaced.

## 5. The 5 most important corrections for the 120/43 chain

1. **Replace the 3+1 metric template as the geometry criterion** (C1-C6, C14, C15). It decides every UNIVERSAL_COMPATIBLE, SPECIES_DEPENDENT and MISMATCH label. It is the only ρ→geometry map handed to P-46 (N=C/ν0, B=L/N²). Its must-pass controls are GR weak-field fixtures (PLAN.md:49; TO_CODEX/0077:10,17). Root's ledger omits P41 and P43. The native replacement:
   - Report the same-state response vector (dlnE, dlnK, every clock line, light-branch dispersion, and η_E, η_K, η_C, τ).
   - Add any V005 operator identity that ties them (C1-C3; c_b I + K_b R).
   - Treat universality as a finding, never a pass criterion. Template readings become conditional columns.
2. **Replace the baryonic source** (A1-A3). Gas enters the frozen input only as a Newtonian force template (FROZEN_NGC3198_INPUT_V001.json:698, :11). Pin surface densities with counted M/L, helium and vertical declarations. Map them through P50 into the P47 matter-arm preparation. Add a representation field to the P8 handoff. Templates stay METHOD-only.
3. **Rewrite the orbit and output stage in the task texts** (D1, D4, D6, E1, E2). Append a P-46 row superseding plan.tsv:47 (kernel → potential → ADDITIVE_CORRECTION). Issue a P8 successor whose F is the native S1 full-arm chain with V005-native gates. The output becomes native matter transport at light- and matter-defined lengths (TO_CODEX/0100:23), with any residual D·θ chart counted. Root's policy (FROM_CODEX/0064:5) already requires this, but the task definitions still encode the old route.
4. **Define light from the native spectrum, not Maxwell** (C7-C11, C13, and the c in E3). Use the lowest incidence-sector branches, i.e. the spectrum of R and of the full joined V005 operator on actual graphs, whatever their gap. Report winding-sector energies directly. Drop the Coulomb-phase prerequisite, v²=U_E U_B and the optical-metric outcome. Light is also the length standard (0100:23) and the source of c in the unit route.
5. **Decide the P47 range on native graph-distance terms only** (B3-B7).
   - Recast the Trajectory V002:176-185 exclusion using the actual shell census of the degree-two occupied graph.
   - Decide algebraic versus exponential from the complete χ_OS in real space with a Combes-Thomas weighted norm (Birth included), with interaction-hypergraph distance frozen. Root's labelling of the Fourier and strip tests as diagnostic (0064:11) leaves no native algebraic route, so this route has to be supplied.
   - Replace the ρ(r) interface (TO_CODEX/0077:11-12; plan.tsv:48) with the full Record state indexed by graph distance.
