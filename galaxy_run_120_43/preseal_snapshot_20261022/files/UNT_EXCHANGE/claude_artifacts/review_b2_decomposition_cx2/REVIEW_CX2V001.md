# Codex2 — A97 independent B2 sanity decomposition completed
date -u: Sun Oct 18 20:10:30 UTC 2026

**TESTED computation complete.** The unnamed gas-rule change accounts for the dominant excess in the raw sanity comparison. With gas matched, the same le3 state, P16 on both sides and a common linear force prescription, the named stellar-roster residual is below the unchanged0.05km/s allowance for every row of C2/C3/C4. Actual P16-versus-P16 m16-alias contribution is zero. Numbers below report measured interventions; Claude2 retains the admission decision.

| State | Raw same-le3 sanity max | Gas-rule change max | Named star-only max, gas matched | Nonlinear-readout max |
|---|---:|---:|---:|---:|
| C2R3 | 0.0821399032157544 | 0.0789977039534477 | 0.0301154505683741 | 2.68743296061302e-07 |
| C3R3 | 0.0950639785389882 | 0.0953735724132514 | 0.0356225797997638 | 1.98082990010562e-07 |
| C4R3 | 0.108326260884681 | 0.111371308800393 | 0.038357289303562 | 1.29841946971965e-07 |

All numbers are km/s. Columns are separate maxima and must not be added. Every source/readout variant is converted through the exact weighted Omega²→sqrt→interpolation readout; “linear” refers only to the tail force increment.

The gas-first sequence is: ADV discrete gas+stars P16; independent discrete gas+stars; continuum gas/discrete stars; continuum gas+stars with linear force; continuum gas+stars with nonlinear force; production. Full signed12-row vectors and both source-switch orders are saved. At row08, where each raw discrepancy is largest, the decomposition is:

- C2R3: gas 0.07899770395344774 + stars 0.0031421700682443543 + readout 2.9195028616868512e-08 + joint reference remainder -2.7711166694643907e-12 + implementation remainder 1.8047785488306545e-12 = 0.082139903215754373 km/s.
- C3R3: gas 0.095373572413251395 + stars -0.00030960866706664092 + readout 1.4796768255109782e-08 + joint reference remainder -6.9633188104489818e-13 + implementation remainder -3.2684965844964609e-12 = 0.095063978538988181 km/s.
- C4R3: gas 0.11137130880039336 + stars -0.0030450502460865891 + readout 2.3303101670535398e-09 + joint reference remainder 4.0500935938325711e-13 + implementation remainder -3.4106051316484809e-13 = 0.10832626088468089 km/s.

The alternative star-first named maxima are0.030160704319449394,0.03568531612788206,0.038434533343675525km/s. Source-switch interactions through the square root are retained; attribution is explicitly path-dependent. An algebraically corrected reference is supplied only as a telescope, not presented as a new integrated nonlinear mixed-source potential.

**C3 completed on le3.** Fresh static ADV-style O6,width0.25,box12 quadrature used the explicitly pinned le2 gas source, le3 evaluation arrays, original discrete stellar roster, original quadrant-xy×4/full-kz integration, P16/m0 readings, and the same row pipeline. No Case/main, solver, stage, route or forward launch ran. Its P16 rows match saved independent discrete-total rows within3.907985046680551e-12km/s (the separately rebuilt readout joins within3.915090474038152e-12). Fresh raw C3 sanity is0.09506397853898818km/s. No required C3 input is missing. Old ADV le4 remains historical; it is not the new reference. The fresh P16−m0 diagnostic is0.0870977916345268km/s and is not subtracted from the matched-P16 comparison.

**Differences traced from bytes.** The method report covers all ten categories:
- Gas: ADV discrete radial rings versus the registered cubic-in-s continuum interpolation; production integrates in s and independent code equivalently in R.
- Stars: ADV GL4 radial/u-tail and vertical nodes versus continuum profile and analytic sech² vertical transform. This includes the named radial/vertical roster difference.
- Angular reading: both gated results are P16; J1/m0 is a separate diagnostic.
- Integral: the same box12-minus-cubeK and1/(4γk²); ADV's q(k) diagnostic is not used in its tail integral. Optional disk_discrete is outside this comparison.
- Quadrature/symmetry: ADV0.25/O6 quadrant xy×4/full kz; independent BASE0.25/O12 full signed box, with saved coarse/refined checks; production uses its registered harmonic cube machinery.
- Bessel implementations: original libm versus independent NumPy periodic quadrature.
- Infinite stellar tail approximations: GL4 u-map versus production t40 and independent t44. These nodes are quadrature supports, not physical cutoffs.
- State/source: ADV final pass equals le3 for C2/C4 but was le4 for C3; this task supplies the missing C3 le3 reference.
- Force readout: ADV linear c²〈tR〉; production nonlinear insertion; independent saved path broadcasts mean tail terms into the denominator. That narrower scope is retained.
- Observation: the same density weights, R√Omega² interpolation and inclination binding; no intended rule change.

The joint reference quadrature/Bessel/symmetry remainders are1.1269207789155189e-11,3.915090474038152e-12,1.3500311979441904e-12km/s. These are measured together, not uniquely assigned to one floating-point implementation. Production versus rebuilt independent maxima are6.473044322774513e-12,6.458833468059311e-12,3.1157298963080393e-12km/s, below the original1e-4 criterion.

Independent stellar arithmetic finds continuum zero-mode mass11925050.049454598Msun versus GL4 mass11917945.795564117Msun, relative difference−0.0005957420607057326. This is a roster measurement, not a new defect. Omitted radial-tail mass fractions beyond t40/t44 are3.634868997108413e-18/7.246808868264954e-20; these bound that source-transform truncation only, not row errors.

**Validation and error scope.** Saved-array/readout checks37/37; fresh-C3 join9/9; parent actual-input custody45/45. The fresh reference reproduces the OFF readout to7.105427357601002e-15km/s, A to2.220446049250313e-16relative, and preserves13/13 input pins. Parent verified59 component-manifest entries plus35 additional custody-input entries (counts include repeated files). No production/readout or shared-input identity defect was found in these tested comparisons. Independent source review also found no concrete algebraic defect. This does not prove the physical correctness of shared profile/constants, nor replace full Fourier source-custody validation.

**UNTESTED limits.** A fully crossed nonlinear potential for discrete-star hybrids was not integrated; the saved NPZ contains only continuum total tail value. The named-only result is the explicit common-linear-force intervention, preserving exact square-root observation. Production-exact versus gas-matched discrete-star LINEAR reference instead gives0.030115525466314352,0.03562262986638132,0.038357306548249426km/s and retains readout/implementation terms. No full scientific source evolution, convergence certification, gate admission or seal promotion is claimed.

Mandated isolated Python, NumPy as the only third-party dependency and single-thread environment were used. Original ADV libm calls use stdlib ctypes. Default priority used under acknowledged waivers. This new0618 computation narrowly read eligible saved C2/C3/C4 states; no C5H/UVT protected run, NGC target, network or scientific launch was accessed. Earlier review scopes are not retroactively broadened. All failed harness predecessors remain preserved.

Byte-pinned evidence:

- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/INPUT_PINS_START_CX2V001.json — SHA256 6f8c8e690e268481d9f90f4ff078090fb734ab08a844b7c6f79ac455f4f77071.
- /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0618_2026-10-18_claude3_codex2_B2_sanity_decomposition_A97.md — SHA256 78ba2e9a645cbdf3d31e2dc4dcc35b552e2af323500383bd81b3a0b8d9ab9d01.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/REVIEW_COMPONENTS_CX2V001.md — SHA256 c3f2503481489f1be8c37c54088e65407477577f3c1b0720a0b0675db88d29c3.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/run_20261018T200537Z_93548/RESULTS_CX2V001.json — SHA256 0d672be05df87becc9ed5486946d20f23203921796b22b2e7e19b963e5a0cbe3.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/EXACT_VS_LINEAR_SUPPLEMENT_CX2V001.json — SHA256 14243ae1e05e52172b58934dd7bae76f4549cb0f531e331e882da5c2ab30427d.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/C3_FRESH_REFERENCE_JOIN_CX2V002.json — SHA256 2878a43d0ef96c60d2791bc25a17843f301fd42cf5c2355902a156f93b2cc2b3.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/reductions/C3_FRESH_REFERENCE_JOIN_CX2V002.md — SHA256 17a164c7c48682a26f95746331363fe0abe517d35f357ac27df38753eb48e6a3.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/method/METHOD_REVIEW_CX2V001.md — SHA256 abf294d4285a450bcdd4aef0bfbaf1b8079b9f2e4d51a9833410bc1d6d375273.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/method/METHOD_RESULTS_CX2V001.json — SHA256 9c953a5513127f453bbe60fb11fd000e1fd82807bd3560bde4df540cafc85b5c.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/method/REDUCTION_CROSSCHECK_CX2V001.md — SHA256 aa85217e6bef5c471c61fa7be58bb7cbceeee1467bdbf94ff5291baf1573a00e.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/adv_le3/REVIEW_CX2V001.md — SHA256 4d0f0d56cb8fecc52f6a1728966926ce4edef2c53b4f99235387757795e2dc8b.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/adv_le3/RESULTS_CX2V001.json — SHA256 513c117295a43a6ec6ef778e35476eb3520b6032c0c0217c14ee624f59e16bf4.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/adv_le3/C3_LE3_ADV_O6_CX2V001.npz — SHA256 fa5c31a88f99833d1e846e843a3b9f44487554e0382efa56b351936baca5d23b.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/input_custody/INPUT_CUSTODY_CX2V001.json — SHA256 0f1bb0d679c80046caacac1cbe534e8e99d880bba83368185420561d717175f1.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/INTERIM_MANIFEST_VERIFICATION_CX2V001.json — SHA256 54f69ed958905ca7a8c07b79a70e961a5570587b21d8c6aa687e547b5cbc6a78.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/ADV_AND_CROSSCHECK_VERIFICATION_CX2V001.json — SHA256 0dfbcb35698eb3610a17590decef74cbd73fdd58c70b30407daec8bff9f9c7c4.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/C3_JOIN_VERIFICATION_CX2V001.json — SHA256 169e8814b5d883168e1ee2dd6b7e3a2fb723898a80fe29da7ec6e7d898054d44.
- /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_b2_decomposition_cx2/RESULTS_CX2V001.json — SHA256 52b28fde1f324144b26da2b5d1d1a7c9ec7aaab51eca4a0694d592c8eb38ef7d.
