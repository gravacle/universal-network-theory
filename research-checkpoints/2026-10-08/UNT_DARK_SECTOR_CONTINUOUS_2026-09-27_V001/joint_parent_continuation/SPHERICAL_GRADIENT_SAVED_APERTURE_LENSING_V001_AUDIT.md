# Saved-only acceptance of the common finite-aperture lensing prediction V001

2026-10-06 UTC. Independent acceptance after root confirmed natural exit 0. **PASS: 3,651 scalar and metadata assertions**, all 48 mass/case/impact rows, 36 grid comparisons and 324 saved numerical controls. This audit used stdlib saved-data arithmetic only: no producer import, field contraction, ray integration, PDE, Hamiltonian action or eigensolver.

All 16 recorded input hashes match current bytes and remained unchanged across the audit. The twelve parent cases retain their recorded converged/qualified status, mode axes and path-enclosing support. Complete frozen row/control labels and thresholds, physical impact units, radians/arcseconds, same-Plummer baryonic aperture, signed gradient fraction, A_lens normalization and finite-aperture asymptotic reference agree. All twelve displayed finest-grid rows exactly match the JSON serialization.

Largest stored mesh A_lens change is 0.0012383668355518962, below 0.02. Largest stored 8/16 A_lens error is 4.440892098500626e-16. The 8/16 integrals were not serialized; this audit authenticates their saved errors and frozen criteria rather than independently recomputing those integrals. Subtracting the separately saved full/local angles is a redundant check subject to cancellation: it differs from the directly integrated tiny gradient angle by at most 1.7986584424138113e-10 relative. The matched gradient remains evaluated directly; the audit changes no producer criterion.

Finest-grid full/same-Plummer enhancements span 7.4674999627936485 to 65.65201541671226. For the 10^9 solar-mass case at b/rM=10, the full angle is approximately 0.051723665 arcsec, enhancement 15.456286, and gradient change -0.04319266 percent. These are conditional prepared-source, leading weak-metric predictions over Rcap=150rM. They do not supply an observed lensing score, an infinite logarithmic-tail closure, exact zero slip, or a shared cosmological history. Earlier lensing evidence remains intact.

## Sealed outputs

| Artifact | SHA256 |
|---|---|
| SPHERICAL_GRADIENT_SAVED_APERTURE_LENSING_V001_RESULT.json | 5c988e58376facccdcf893d14f1e3f699e1e782fda15421322e4bd9fb9e50735 |
| SPHERICAL_GRADIENT_SAVED_APERTURE_LENSING_V001_RESULT.md | 153387932db74d2454c5a6e51d5f5ba5ae862442eff1df6330a4f31a9bf53a0b |

## Authenticated input custody

| Input | SHA256 |
|---|---|
| SPHERICAL_GRADIENT_FORWARD_V001_RESULT.json | 657fa06ac5fe875a6ccef405b8061c42eb63f4715ed7878ee16f6836e10682f7 |
| spherical_gradient_saved_aperture_lensing_v001.py | 4341587d1bc217608b927064a21b2cb16b5bff06fee4e1c813ccd9428ad70feb |
| SPHERICAL_GRADIENT_SAVED_APERTURE_LENSING_V001.md | 70763c72e80c42de69ef075daffea63ecac8a7ef9d8795dcc574a19d72fe3813 |
| SPHERICAL_GRADIENT_COMMON_LENSING_CLOSURE_V001.md | a4221d6ed0d5b0fed266e9fc8e27fa190b3f911e39cc7d218912418d1cc69b57 |
| SPHERICAL_GRADIENT_FORWARD_V001_M10000000_CASE_0.json | 66c80b22c534cb0f759eb7a6fc8390ddbfeafcb41fbd8d8f96d8c9286740785d |
| SPHERICAL_GRADIENT_FORWARD_V001_M10000000_CASE_1.json | 24d2a03f77e73898601b9492b18a1926e4c967a125d0cc966f8007b3e7142417 |
| SPHERICAL_GRADIENT_FORWARD_V001_M10000000_CASE_2.json | e1b1b227d58becb03098588cf52ac9a6f78b85c9507a978d7688c486a85940e9 |
| SPHERICAL_GRADIENT_FORWARD_V001_M10000000_CASE_3.json | d4ce9c2a55ecde6ebf3ed11c589264e6cd731573a0201480b7ce4b46130c9a3f |
| SPHERICAL_GRADIENT_FORWARD_V001_M1000000000_CASE_0.json | da23fee741702022bb4b10f11e668c1ffe61e7cfcd753ca042aca5be81518021 |
| SPHERICAL_GRADIENT_FORWARD_V001_M1000000000_CASE_1.json | f9e23e10224dfc38b335fd05bc8a70d556b560685920ad9d8252cbb12044bf9a |
| SPHERICAL_GRADIENT_FORWARD_V001_M1000000000_CASE_2.json | 0f1134f81dfed288f1d287484ff0c955ada3df86ad3d265fedda57840ad11e72 |
| SPHERICAL_GRADIENT_FORWARD_V001_M1000000000_CASE_3.json | 315b97f4c5570d0c3d02528451419d55a3a0065ecfdd3f7836b1fd868ec8635d |
| SPHERICAL_GRADIENT_FORWARD_V001_M100000000000_CASE_0.json | 6825253545868662f775d525be35856e66cc8d72dc35fcdf09693eb1206a7ea0 |
| SPHERICAL_GRADIENT_FORWARD_V001_M100000000000_CASE_1.json | 19c409a75002fdc14b5a0d38721f98d0398a5705e10a66cc5a259dd9f776c2cc |
| SPHERICAL_GRADIENT_FORWARD_V001_M100000000000_CASE_2.json | 431e8207abb72e8a3dc7d605d0f55999d1832ad595ff900dd37229d97355956b |
| SPHERICAL_GRADIENT_FORWARD_V001_M100000000000_CASE_3.json | ae0e582521cd662d0431a8c8f885dd5a0c8f38ff4fb80b14bf87694c0609587f |
