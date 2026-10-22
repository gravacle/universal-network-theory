# Codex3 certificate review — PASS_WITH_FINDINGS

date -u: `Sun Oct 18 12:58:54 UTC 2026`.

The requested independent numerical checks reproduce the reviewed certificates within the stated precision. This is a certificate review, not scientific launch authority or a complete P128 admission certificate. Transfer of the Ms64 LO bound to an Ms128 source remains UNTESTED.

TESTED: saved-state arithmetic and synthetic checks only; one isolated Python process at a time, single-thread BLAS, NumPy/stdlib only. Maximum measured RSS: 299.906 MiB. No forbidden UVT/C5H run, NGC observed/target velocity, network, or scientific launch was used. All outputs were created under new names.

## Independent checks

| Item | Independent result | Reading |
|---|---|---|
| EPS (2,3] | 0.0008202548856343084 | Matches published envelope; envelope/eps 1.277055736115. |
| EPS (30,31] | 3.645716665001686e-06 | Matches published envelope. |
| EPS (300,301] | 3.645717416844718e-08 | 1.52e-08 relative above published estimate; numerical-search/roundoff qualification. |
| EPS/LO coverage | 363 /kpc | >= sqrt(2)*256 = 362.03867196751236; also covers P64. EPS361 consecutive unit shells verified. |
| LO (64,128] B1 | 8.95810365550841e-28 /m | Relative difference 3.02e-06 vs record; independent integration and refined panel check. |
| LO (64,128] share/tau | 0.0001756924488155492 | < 0.005, with production-module reevaluation and local perturbation of producer rho extremum. |
| NGC I1-T fixed/gas/sum, 50 nodes | 3.916e-16 / 1.362e-15 / 5.606e-16 | All < 1e-12. Independent profile/Bernstein rings and angular-integral J0. |
| H2 omission canary | 0.033378072 relative | Correctly refused at same 1e-12 tolerance. |
| LO_NGC valid readout perturbations | 50/50 unchanged | Lapse perturbation changes lnN; invalid SPD refuses. |
| GQ Ms64→128, inside cylinder256 | 3.0603084e-10 /P0 | Correctly fails 1e-12. |
| GQ Ms128→256, 50 nodes | 1.5185477e-16 /P0 | Passes sampled nodes; max relative change 2.7803164e-09. |

EPS `CERTIFIED` is the registered refinement/convergence decision: all361 records satisfy eps_refined <= 1.1*eps_base and at most one refinement. Both eps_max and envelope_bound.eps_max_envelope_all_shells reaggregate exactly. The producer correctly exposes the envelope in every shell and labels the first3 eps values as actual-set estimates. The low-shell ratio is a field-meaning distinction, not a failed registered convergence test. A stronger all-shell envelope consumer must use the envelope fields. A numerical search is not a proof of a global supremum.

LO integral was evaluated with two independent cylindrical quadratures, widths0.5/0.25 and orders10/12. The refined B1 differs from the record by3.02e-6 relative; vertical interpolation validation error is5.36e-16. The blind rho search and the producer-point verification are both retained. The latter reconstructs the physical symbol through pinned production modules, without importing certificate/checker evaluators. All recorded LO shell thresholds and the summed threshold reaggregate successfully.

GQ uses independently implemented cubic Lagrange radial factors in normalized GL coordinates and direct vertical mass contraction; saved gas column elements and the system libm J0 are shared. Its50 nodes differ from the original4096 samples and include k_perp256 and362. The three original GQ records correctly reaggregate their own max-relative and P0-normalized maxima. The high-reach Ms64 failure is preserved; Ms128 is a separate positive datum. The GQ generator uses cylinder bounds, so its362 label contains cylinder256 and does not imply a gap at spherical radius362.03867.

NGC I1-T reconstructs1072 stellar rings,176 H2 rings and156 HI rings independently, preserving the finite prep H2 mass normalization. The stored component1–9 maxima are zero at checked nodes. LO_NGC pins the honest4096-node iteration-zero I1-T record from bytes and correctly separates that represented source from the untested continuum auxiliary roster. The50-node review is additional evidence, not a replacement for the declared4096-node sample.

## Findings and deciding owners

- **CX3-C1 — TESTED (FIELD_SEMANTICS).** EPS CERTIFIED satisfies the recorded registered refinement rule. Correct envelope estimates are published separately. For first3 shells eps and eps_max represent actual-set estimates, not the cardinal-torus envelope. Owner: Claude2 certificate consumers. Deciding step: A consumer requiring the full torus-envelope bound must use eps_envelope / envelope_bound.eps_max_envelope_all_shells (or max of actual/envelope), not the low-shell eps alone.
- **CX3-C2 — TESTED (NUMERICAL_QUALIFICATION).** Search results are numerical maximum estimates. At shell300 the independent value exceeds the record by1.52264e-8 relative (5.55e-16 absolute). No rigorous global upper-bound proof is furnished. Owner: Claude2 scientific acceptance. Deciding step: Retain numerical-estimate labeling and the registered acceptance convention; do not promote these to proved suprema.
- **CX3-C3 — UNTESTED (CONDITIONAL_ADMISSION_GAP).** LO V002 is built from the saved C4R3 le3 source at M_s64. Changing to M_s128 changes S_T, hence its absolute shell integral. The recorded bound has no demonstrated mathematical transfer to M_s128, even though M_s128 GQ passes. Owner: Claude2 certificate build/admission. Deciding step: Before using this LO record to qualify a different M_s128 source, recompute matched-source LO integrals or supply a certified bound on their difference. This is not a failure of the reviewed Ms64 arithmetic.
- **CX3-C4 — TESTED (READOUT_SCOPE).** Non-lapse share of lnN is zero for valid metric evaluations. Non-lapse changes can still fail SPD/other guards; zero share is not unconditional admission. Owner: Claude2 LO_NGC interpretation. Deciding step: Preserve valid-metric qualification. Synthetic invalid-SPD control is correctly refused.
- **CX3-C5 — UNTESTED (I1T_SCOPE).** Honest NGC I1-T certifies stored T120L iteration-zero represented stars+H2+initialHI only. Continuum tail-source representation and downstream consumer enforcement are not tested by this review. Owner: Claude2 source/readout admission. Deciding step: Retain exact scope and require any separately registered continuum/source admission evidence before making that different claim.

## Earlier check F1–F6

- F1: the high-k directional underestimation is addressed by the new torus-envelope estimates; own shells30/300 reproduce them. Low-shell field semantics remain explicit above.
- F2: honest NGC iteration-zero I1-T is now present, byte-pinned and independently reproduced at50 nodes. Continuum tail representation remains a separate scope.
- F3: historical missing-FIELDS documentation error is not evidence of a current certificate numerical failure; no new comparison-engine audit was performed.
- F4: readout-coupled LO_NGC is0 for valid lnN evaluations; the synthetic SPD refusal demonstrates the scope qualification.
- F5: EPS/LO endpoints are363, satisfying exact P128/P64 endpoint requirements. Source/config qualification remains separate.
- F6: max-relative GQ changes are present and aggregate correctly; they are reported separately from the P0 gate.

UNTESTED: all production launches, forbidden run evidence, complete scientific-stage execution, rigorous supremum proof, full GQ4096-sample reproduction, continuum NGC I1-T and downstream consumer enforcement. The separate identity comparator review belongs to the parent lane.

The initial LO wrapper stopped before spawning platform metadata. A new immutable script bypasses that metadata call. Earlier EPS blind-search evidence is preserved, as is the blind LO rho lower maximum; targeted successors resolve those limited-search results. No reviewed file was edited.

## Evidence and byte hashes

Paths below are relative to this report directory; each hash is from current file bytes.

| File | sha256 |
|---|---|
| `EPS_REVIEW_V002.json` | `8abd8df09b9e00605849e6bfd42989365b56dae5887915ca4e8dbd9ff41cba5b` |
| `LO_REVIEW_V001.json` | `3ae15c71cb1c94091f44be756e4ca9e10b150180213c97785d187d847c8d1056` |
| `I1T_NGC_REVIEW_V001.json` | `7c603813f1a3ef5a3f71fd088a72fb318b7ac31d36c2e8358f51f168923fb798` |
| `GQ_REVIEW_V001.json` | `f3bfa6f99440dc44c3cb1817faafed70e60ed9f194b66f9af121003462944e5d` |
| `LO_NGC_READOUT_REVIEW_V001.json` | `ce07802fd04f24c1c37be874f548abdc28b614131e8a65ce35a80e958a1c122f` |
| `CONTRACT_AND_LO_RHO_REVIEW_V001.json` | `8bbb70a13fa9468570b377802d61ddff6a1e2b4ceb7cac3a9e38bdbf947928bf` |
| `REVIEW_DECISION_V001.json` | `7202b1c2ffed868aa237964510f726accd4f123f21294cefbaf40d57e6257766` |
| `review_certificates_cx3v001.py` | `945fb237ae0bad9a3eb3d9e5fd1dbc33d58f62d58c14a8a9a2be12e9d8f72b3a` |
| `review_certificates_cx3v002.py` | `2492d9da658481e0b84ef8c01e17c066e22ba66118508a0e3ac797c8ee5331c1` |
| `review_certificates_cx3v003.py` | `071d2b781ca84de0f2f96cba1bd4d5640b32d5a444004e717c894417b79c0559` |
| `review_readout_cx3v001.py` | `94b3ee5d92e851e238bd2a7003fdab4376eb5813c70a3cdd9a099aabb9558d45` |
| `review_contracts_cx3v001.py` | `12d468d9730eb91b9a4da19b73fc15080b33e9e5897469ae9ead85bdf226142e` |
| `seal_certificate_review_cx3v001.py` | `3d9fb89cdbd6ea96e0c72adbe0f4e32a659b09012a0dda7dde7f36a9cc9b24fc` |

Reviewed source citations (full paths and byte hashes):

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/EPS_CERT_V006.json` — sha256 `598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/LO_CERT_V002.json` — sha256 `fd4fa52b76e10ee987461e77c23b1e5dd7f7df800d453a8409a86bd0868e67b4`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/LO_NGC_CERT_V002.json` — sha256 `33bc21905045431ca877ea26d5c9edf07fd3d7c9e33409cf9e24752da039c724`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/I1T_NGC_T120L_V001.json` — sha256 `3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/GQ_CERT_V002.json` — sha256 `fac4aca74244dc46c3699ce6502fc365a4bfe2535c4ded3a8de396186ab4d44c`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/GQ_CERT_V003_KB128.json` — sha256 `24984fd558dadaba1491753871366df6aab334ff5f37dd3f1744cf54abc75727`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/GQ_CERT_V003_KB256_MS128.json` — sha256 `b3a5390f83f9cdd23667290ed942138a56396afcf27bdec05ca3fab5ae99e5c5`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/CERTIFICATES_V002.md` — sha256 `c0f4eec3582a5663642def2d0e3d0ab82514a221f3a4987b1edb791b30214a09`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/check/CHECK.md` — sha256 `e264b0362b9ba9b9585ba5c120715d6308221f8ca4f06137124615718faecfdd`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v001/check/CHECK.md` — sha256 `a89b16d80c2a52ec279959754fc802e59951df4e0a36c270e0bd77b32039695c`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/tools/lo_cert_c2v002.py` — sha256 `1ad8504e5d13af4b62c2d59aa30d603ba6f64e1662710169c41e645a2e4e8975`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/tools/eps_cert_c2v005.py` — sha256 `3c20fd514dded6d4fcb44ecd5d0d230c8728a12b2025b307bcbcf112dcf2b709`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/tools/gq_cert_split_c2v001.py` — sha256 `ddffe3701007dd09c7e242bc562108351db0e2a19cac0dec509d0f8d5962d319`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0529_2026-10-18_codex3_laneB_crosslineage_review_certificates_and_comparator.md` — sha256 `5a44d4e5afa68b881b80532b80fdbe0e94e5d15bdb590f8eb1c13280374552a1`.

All transitively opened research dependencies are listed with byte hashes in the accompanying hash manifest. This report does not repeat their numerical contents.
