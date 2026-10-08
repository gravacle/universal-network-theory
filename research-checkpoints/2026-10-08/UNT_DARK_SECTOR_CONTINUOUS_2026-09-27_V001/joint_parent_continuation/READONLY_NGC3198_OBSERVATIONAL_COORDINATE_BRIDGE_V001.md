# NGC3198 observational coordinate bridge audit

The published SPARC kpc radius reaches the source, grid and historical velocity query unchanged. There is no EPS or eta factor in the radius registration. The coordinate used by the leading cylindrical solver is not an already solved proper or circumference radius.

| Stage | Actual registration |
|---|---|
| Official SPARC rotmod | `Rad` in kpc, distance13.8Mpc;43 rows, unchanged `Vobs`/`errV` in km/s |
| SPARC stellar source | Official43 `(Rad, SBdisk)` pairs; fixed M/L=.5, central continuation and EXP24/3.14kpc tail already declared; no velocity inversion |
| HI source | Begeman24 angular radii0–11.5arcmin converted once at13.8Mpc; old tilted-ring surface reduction retained, then the declared coplanar thin-sheet approximation |
| Leroy activity/molecular rows | Literal23 catalogue radii0.3–15.1kpc at13.8Mpc and72°; no second deprojection or radius-r25 rescaling; activity outside support remains `None` |
| FINE_Q3 grid |173 radial/89 vertical nodes, nested old nodes/cells,0–128kpc; query uses the official `Rad` directly |
| Q1 readout |Containing-cell slope of saved midplaneψ; both one-sided slopes at a grid node. Legacy readout retains its nodal-gradient interpolation. All43 signed `v²` identities agree. |

The code coordinate is r=Rphysical/L0 with L0=1kpc. Its fixed SI anchors are a0=1.00598332817e-10m/s², L0=3.08567758149e+19m and c=299792458m/s. Hence Φ=Bψ with B=a0L0/c²=3.45382177098e-08, and the historical weak readout is v0²=r(a0L0/10⁶)ψr in (km/s)². A0_V=3104.1402031 supplies that conversion once. Eta=a0/(cHstar)=0.153403540768 controls field normalization, not radius. EPS=1e−5 enters the phase law/domain and source, not a dimensional length conversion. The macro ell=.1 means100pc in this chart; it does not earn a microscopic ruler.

For a full static zero-shift chart, circumference radius is ρ=√gφφ=Rexp(−Ψ), proper radial length follows hRR, and the normal-observer circular speed is v²/c²=RΦ′/(1−RΨ′). The general axisymmetric/time-dependent case also needs the meridional shift, explicit time derivatives and ordinary equations. The current43 Q1/legacy values are preserved weak diagnostics, not final full-metric geodesic predictions.

Only the173 sealed scalar midplane values were decoded. They give ψ∈[-29.6952175043,0] and Φ∈[-1.0256198871e-06,0]. **Conditionally setting Ψ=Φ** gives |ρ/R−1|≤1.02562041305e-06; at44.08kpc this is≤0.0452093pc. The same maximum bounds the fractional proper radial-length difference without integrating a field. Across the43 saved slopes, max|RΦ′|=3.05537665199e-07, and the conditional zero-shift spatial-denominator speed change is≤1.52768867556e-07 relative. These are **not bounds on an unsolved Ψ, exterior, shift or full metric**.

SPARC imports distance13.8±1.4Mpc (fractional quoted error10.1449%), inclination73°±3°. Leroy imports72°. For a held line-of-sight speed only, replacing73° by72° would multiply a deprojected speed by sin73°/sin72°=1.00551832575, a+0.5518% change. The70°/76° ratios are1.01767826501/0.985580715308. These are counterfactual geometry ratios, not applied corrections, independent error bars or a fitted nuisance model. Actual warped-ring geometry and distance/inclination covariance are not supplied by the compact rotmod file.

At13.8Mpc one arcsecond corresponds to66.9042879931pc and one arcminute to4.01425727959kpc; the HI angular endpoint therefore becomes46.1639587153kpc. Equivalent angles in the JSON are inferred only from the tabulated rounded radii; they are not recovered raw sky measurements. Photon-band reconstruction uses the already face-on Leroy SFR components to obtain Iνcos72°; this is not a second spatial-radius correction.

The frozen source conventions are imported, not optimized against residuals. The old fixed-density protocol's1.2e−10 acceleration is a legacy law anchor; the current S_cross solver uses the authenticated a0 above. Both share the same physical radial units. The primary-source chain identified by the parent survey review is Da06/Be91/Be87; no THINGS or HALOGAS catalogue was substituted in this audit.

The remaining observational bridge is a forward comparison from a genuinely solved full metric and rotating ordinary flow to the same observed ring/sky geometry, including the measured distance/inclination convention and ordinary noncircular/pressure effects. Merely relabeling the inherited R asρ, changing inclination silently, or treating the historical Newton readout as the physical final velocity would not complete that bridge.

Audit PID29108 naturally closed0. Sealed source/data/COMMIT hashes and all43 query/readout identities were checked; only173 saved midplane scalars and stored readout arithmetic were used. No producer/helper/operator/field/Gram/inverse/eigen/solve/evolution replay or parameter change occurred. An auditor-only metadata-member assumption (`metadata_json` versus the authentic `metadata`) was preserved and corrected; producer bytes were untouched. All physical qualifications remain false.

[Signed43-row context, coordinate brackets, units, potential bounds and input seals](/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/READONLY_NGC3198_OBSERVATIONAL_COORDINATE_BRIDGE_V001.json)

JSON SHA256: `e71461bb84f0c5d6c855e11a0d411c8e2ddc3c974b12c0e2accd211e1fafb3ae`

Audit source SHA256: `d5cac67e145e40cbcc20c694d8f51f67e7023d5943767504ed309aa0571865b0`
