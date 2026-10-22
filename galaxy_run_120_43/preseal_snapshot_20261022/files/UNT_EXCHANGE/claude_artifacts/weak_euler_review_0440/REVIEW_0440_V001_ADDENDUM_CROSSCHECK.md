# REVIEW_0440_V001 addendum: supplementary cross-check completed, verdict unchanged

Claude4, 2026-10-16, about 19:40 UTC. REVIEW_0440_V001.md (SHA-256 1eba74f1346f6140b3b83b7d9ea70eb1971c2f5a20ac382e1e6e2aa767e05420) is left exactly as posted in FROM_CLAUDE4/0002. **The verdict is still PASS, with no defects, on 8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da.** No supplementary outbox return is needed.

## Adversarial cross-check of the yardsticks

Files: CROSSCHECK_C4_V001.md (SHA-256 cbe1a47329e350dd0572892f81871d7a25a48d04244721bf0016c184db3c4a00) and crosscheck_c4_v001.py (701e6834bae41fab1064055a9c964186bafa5889fe277096bf7d5737b9db8e78).

**Errors found:** none in the H2 reference transcription, and none in H1's oracle or derivation.

**Agreement between the yardsticks:**
- 216 random complex cases with mixed-sign Omega: H1's oracle and H2's reference agree to 3.6e-15 (A, Frobenius norm) and 5.5e-16 (b).
- 96 root-structured cases agree to 7.2e-16.
- 180 cases in exact rational (Fraction) arithmetic put every floating-point route within 3.5e-15.
- The pinned contract text, evaluated mechanically, reproduces the reference.

**Harness reproduced:**
- 46/46 checks pass; both result JSONs reproduce byte-identically.
- The mutation study catches 27/27 mutants, plus 26 additional mutants of the cross-checker's own. Two independent correct implementations pass, so the harness does not give false failures.

**Independent physics checks:**
- The hand re-derivation of M_p matches the contract text to 1.8e-16.
- A Cartesian finite-difference check of delta v and delta a agrees to 8.2e-11.
- The phi-conjugation weak identity holds to 9.4e-16.
- With a thermal-wind-consistent background, A is Hermitian to 4.0e-16 over 54 cases.

## Coverage notes from the cross-check, now closed on the frozen module

File: crosscheck_frozen_c4lead_v002_signs.py, with results in _py312.json and _py39.json.

- **Negative and mixed-sign Omega.** These are now value-checked, not just accepted.
- **nfree = 1 with npoints > 1.** Shapes (7,1) and (16,1) are now included.

Over 192 cases (all-positive, all-negative and mixed Omega; shapes (7,1), (16,1), (5,3), (4,4); m = 1..6), the module agrees with the H2 reference on all seven outputs to 7.7e-16 and with H1's oracle to 6.9e-16. Results are identical under Python 3.12.14 with numpy 2.3.5 and under Python 3.9.6 with numpy 2.0.2. The module hash was unchanged.
