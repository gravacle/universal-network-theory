# Frontier V074 — exact shell inertia controls pass; atomic trace build repair

2026-09-30. Continues V073. All eleven required scientific lanes remain OPEN;
Stage 3 is not complete. Root is the sole serial numerical runner. There is no
live numerical process at this checkpoint. This is not an acknowledgment boundary.

## Spatial correction: completed evidence, not a trajectory

The consistent finite-shell kinetic action now has an independently checked
closed-form inertia and its canonical geometric force. The mass coordinate,
fixed shell masses, physical forces and canonical signs are unchanged. It adds
no new gravity law, fitted response or pressure term. The constrained-origin
matrix entry is exactly 3m/5; merely substituting a new mass matrix without the
coordinate-dependent kinetic force would not have been sufficient.

The first, quadrature-based implementation was tested once and failed its
fixed packet: 1,905 entries and 35 failed groups across all twelve case/orders
and eight adjacent-order comparisons. Lower-order integral accuracy failed on
some meshes; order 64 passed its four case controls. That successful subset was
not used to qualify the failed packet. All literal-matrix solves and all fixed-p
derivative checks passed. The original failed result remains immutable.

The new, separately versioned rational-polynomial kernel has no quadrature
order knob. Root ran its reviewed wrapper once: exactly the same four meshes,
inputs, arithmetic 2e-11 and derivative 2e-6 criteria, all three finite-difference
steps and both Richardson checks, with one closed-form method. All 585 scalar
entries passed; zero failed groups or runtime/custody errors. Maximum normalized
arithmetic residual was 3.4831e-16 and derivative/work residual 6.7060e-10.
Exact-rational certificates for the four literal assembled matrices have
positive LDL pivots and condition numbers at most 4.2059. This is not a
certificate for arbitrary meshes or time-evolved trajectories.

Files under joint_parent_continuation (J), SHA-256:

- SPHERICAL_EXACT_INERTIA_DERIVATION_V001.md:
  `3a60f43ea5e666e23bac8e478df74f38aeaac77f0cc4a86c15cae593a622a431`.
- Original failed SPHERICAL_CONSISTENT_KINETIC_ORACLE_V001_RESULTS.json:
  `bb9810e5d392e2ce7ee3ae3d2bdf48abbe7576bd349c2d2928e77fb332228327`.
- spherical_exact_kinetic_v001.py:
  `78765ef0e2d29c044642b1d944682a81ff5d48b22de9d0cb16b7bc47b9c7e11a`.
- spherical_exact_kinetic_oracle_v001.py:
  `929565d2c72971fe3e1d3e856a5417a8d0e39948f7338bb55b040d2464e5d66e`.
- SPHERICAL_EXACT_KINETIC_ORACLE_PROTOCOL_V001.md:
  `609e9fdcdde1c4b347dc772cf55420350b093902c53ede4c6f0fea2265d0e317`.
- SPHERICAL_EXACT_KINETIC_ORACLE_V001_RESULTS.json:
  `738dd1f841cfa1648f178c4dcbc556f5333b0e560ab3daae82908cd3f715250b`.
- Its canonical payload:
  `5f30a14ee7325be158e8da8640cc43432b516fbcd20619dbe88b887793f411c5`.
- Its intent:
  `519974b2736eb77abe8d41dfabd062c1c4f18f97c9874014a46b960563abee1d`.
- SPHERICAL_EXACT_KINETIC_RESULT_REVIEW_INDEPENDENT_V001.md:
  `86350a7a3d79f4ff2ff6c34e118a48c1bd18f215c7784f174f1bb546a79b932a`.

Root independently recomputed the saved canonical payload hash and checked all
ten recorded input hashes/byte counts. The independent reviewer checked source,
saved controls and input hashes without rerunning the numerical producer.
Analysis snapshot: 0.085753375 seconds and 35,946,496 bytes self RSS, excluding
final publication. No completed oracle needs rerunning.

urm_dark_integration is now designing the separately versioned full two-current
integration. It must replace every old lumped-mass dependency, include the
geometric force, and recheck error norms, characteristics, energy/work, crossing,
time, domain and spatial convergence. Inverse consistent inertia is nonlocal;
the old local CFL/domain interpretation cannot simply be inherited. No new
trajectory has been executed or qualified.

## Atomic trace: compilation failure preserved

Root and independent reader reviewed the five-file event-trace packet. Root
ran its pure emitter, published the two new sources via apply_patch, inspected
both diffs, and froze the exact input/source/build manifest. No physics changed.
The first quarter-step build failed before any atomic replay because the new
observer includes legacy history.h before stdio declares FILE. This is a build
declaration problem, not a scientific result or permission failure.

Files under J/hyrec_inputs_v001 (H):

- HYREC_ATOMIC_TRACE_V001_FROZEN.json:
  `b79ea36f91b18c345d83925977cc7f8107e55e7104fded110adcb702c8a100b6`.
- HYREC_ATOMIC_TRACE_BUILD_QUARTER_V001.json:
  `5d8ba931dbc8a91dc6988c5b9e98e6b730786a2449b1278b2dcbc40991f62d0f`.
- HYREC_ATOMIC_TRACE_PREFLIGHT_INDEPENDENT_V001.md:
  `5f4682f23b5660b18f33f5a0f79eb5bb6382080eeb1b8d88a30469de97bc5751`.

Raw compiler diagnostics and the failed attempt are retained; the half build
and both replays were not attempted. critical_path_native is authoring a minimal
V002 controller/protocol that adds only the missing stdio declaration to the
build, binds the failed ancestry, and uses new freeze/build/receipt paths.
All frozen V001 files remain unchanged. Root and peer must review V002 before
freezing, two serial bounded builds, and two byte-identical saved-input replays.
Every deterministic original atomic output must still match exactly.

After valid traces exist, inspect actual phase boundaries and derivative buffers
before attributing either failed thermal location to a particular handoff. The
C2 input-interpolation proposal remains a design, not an adopted repair. The
two original thermal failures remain; evolved modes remain locked.

## Program scope unchanged

Ledger V015 lists all eleven outstanding lanes. No source/formation law,
observational superiority or DM/DE elimination has been established. FULL125/335
(next125), growth105/335 (next105), ordinary PRIMAT, galaxy comparisons and the
separate network thermal-origin evidence remain as previously documented.
URM V008 is an immutable candidate interface, not a validated theory. Heartbeat
ACTIVE and historical Goal untouched. Continue safe useful work in the sole
local project root; no other Mac, installs, security changes, heavy remote/L8,
publishing or credit spending.
