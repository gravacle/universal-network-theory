# INTERFACE_0439_V001: weak Euler assembly kernel c3v001

- Module: `weak_euler_assembly_c3v001.py` in this directory, `module_version` `c3v001`, sha256 `8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da`.
- Root contract `CODEX1/ADDITIONAL_CLAUDE_WEAK_EULER_TASKS_V001.json`, sha256 `5c30449de636b1f3da751d07ad90caafe964ed19444b0648df8fd9726ade9ebe`.
- Physical status `not_assessed`. Inert, pure numpy assembly with no solve. It imports only `math`, `numbers` and `numpy`. Load it by path with `importlib.util.spec_from_file_location`.

## Signature
`assemble_weak_euler(*, R, rho, P, K_R, K_z, P_R, P_z, Omega, Omega_R, Omega_z, volume_weights, U_R, U_phi, U_z, divU, G, f_R, f_phi, f_z, m, gamma, normalization_scale, provenance) -> dict`

All 23 arguments are keyword-only and required, with no defaults. A missing, positional or unknown argument raises Python's native TypeError.

## Arguments (n = npoints, k = nfree, w = volume_weights; all arrays finite)
| name | shape | dtype rule | meaning / convention |
|---|---|---|---|
| `R` | (n,) | int/float to float64, > 0 | cylindrical radius of each row; fixes n >= 1 |
| `rho`, `P` | (n,) | int/float to float64, > 0 | background density, pressure (P = K rho^gamma) |
| `K_R`, `K_z` | (n,) | int/float to float64 | dK/dR, dK/dz of the background K |
| `P_R`, `P_z` | (n,) | int/float to float64 | dP/dR, dP/dz |
| `Omega` | (n,) | int/float to float64 | angular velocity; v0 = R Omega phi_hat |
| `Omega_R`, `Omega_z` | (n,) | int/float to float64 | dOmega/dR, dOmega/dz (vertical shear retained) |
| `volume_weights` | (n,) | int/float to float64, > 0 | quadrature weight w, used once per integral; the kernel adds no 2 pi, R or other factor |
| `U_R`, `U_phi`, `U_z` | (n,k) | int/float/complex to complex128 | trial = test displacement maps, xi = U y (Galerkin); `U_R` fixes k >= 1 |
| `divU` | (n,k) | int/float/complex to complex128 | div xi with d/dphi = +i m |
| `G` | (n,k) | int/float/complex to complex128 | Eulerian density map, weak -div(rho xi), used exactly as supplied |
| `f_R`, `f_phi`, `f_z` | (n,) | int/float/complex to complex128 | modal grad(dPhi), same exp(+i m phi) convention, supplied once by root |
| `m` | scalar | `type(m) is int`, 1 <= m <= 6 | azimuthal mode; one contraction for every m |
| `gamma` | scalar | numbers.Real (not bool) with `float(gamma) == 5.0/3.0` | adiabatic index |
| `normalization_scale` | scalar | numbers.Real (not bool), finite, > 0 | divides A and b only |
| `provenance` | str | at least one non-whitespace character | echoed unchanged |

Bool, object and string dtypes are rejected everywhere. Real vectors also reject complex, so no imaginary part is discarded. Integer, float16/32/64 and complex64/128 inputs convert exactly; integers are exact only up to 2^53 in magnitude, and `longdouble` is float64 on this arm64 runtime. An array that already has the target dtype is read without a copy and never written.

## Returns: a new dict with exactly 18 keys
- `A`: complex128 (k,k), contract A / normalization_scale. `b`: complex128 (k,), contract b / normalization_scale.
- `E`, `PM`, `VR`, `VP`, `VZ`: complex128 (n,k), exactly unscaled.
- `m` (int), `gamma` (float), `normalization_scale` (float), `provenance` (the same str object), `npoints` (int), `nfree` (int).
- `physical_status` = `'not_assessed'`; `scaled_outputs` = `('A','b')`; `unscaled_outputs` = `('E','PM','VR','VP','VZ')`; `contract_sha256`; `module_version` = `'c3v001'`.
- There are no acceptance, solution, spectrum or tolerance keys.

## Failure behaviour
- Arguments are validated in signature order. A failure raises ValueError whose message contains the quoted parameter name, such as `'U_phi'`. `R` fixes n. `U_R` is validated first among the maps and fixes k, so a map whose shape differs from `U_R` is the one named. Unconvertible input (for example a ragged list) and float overflow of a scalar raise the same ValueError.
- After computing, `E`, `PM`, `VR`, `VP`, `VZ` (in that order), each contraction operand, then `A` and `b` must be finite. Otherwise ValueError names the returned array: `'A'` covers its integrands, because a BLAS may skip multiplications by exact zeros, and `'b'` covers its forcing integrands. The function fails closed with no clipping, repair or partial result.
- Floating-point errors are suppressed inside a scoped `np.errstate(all="ignore")` and caught by these explicit checks. The result does not depend on the caller's `np.seterr`, and no warning is printed.

## Compatibility with the 0438/0441 density map
- `G` must be the (n,k) map `G = V @ coefficients` from `project_density_map`. It must be built with xi_R, xi_phi, xi_z equal to these `U_R`, `U_phi`, `U_z` (column j of G is the density of column j of U), mode = `m`, the same `rho` and `R`, quadrature weights W = `volume_weights`, and the same point ordering. The kernel cannot check this.
- Both kernels use exp(+i m phi). The 0438 term `-1j*mode*V^H((W*rho/R)[:,None]*xi_phi)` is the adjoint of the +i m/R azimuthal derivative in -div(rho xi). 0439 uses +i m Omega for v0.grad.

## Root helicity maps (`owned_32q8_regular_helicity_maps_v001.py`)
`U_R` = `'UR'` (float64), `U_phi` = `'UP'` (complex128), `U_z` = `'UZ'` (float64), `divU` = `'divU'` (complex128), each of shape (2304, 1720). Rows follow `rr = np.repeat(radial_nodes_m, 32)`, and `R` must be that per-row radius. The real `U_R` and `U_z` are accepted and cast.

## Memory and flops at n = 2304, k = 1720
One complex map is 2304*1720*16 B = 63.4 MB. A float64 map is 31.7 MB, a complex k x k array is 47.3 MB, and an isfinite bool map is 4.0 MB. Allocations:
1. Cast copies of maps that are not already complex128, held for the call. Root's case is `U_R` and `U_z`: 2 x 63.4 = 126.8 MB. The maximum is 5 maps, 317.0 MB.
2. Validation makes one transient bool map at a time. All vectors are at most 37 KB.
3. Returned maps `E`, `PM`, `VR`, `VP`, `VZ`: 317.0 MB. Building `E`, `PM` and `VP` needs one transient 63.4 MB product at a time.
4. A is contracted one group at a time. Each group uses a scratch integrand Y (63.4 MB), one transient product while Y is built (63.4 MB), then a transient conjugated copy of the test map during its product (63.4 MB). The accumulator A (47.3 MB) is returned; groups 2 to 4 also make one transient k x k product (47.3 MB).
5. b uses three matrix-vector products, each with a transient conjugated copy (63.4 MB).

Peak use beyond caller-held inputs is the casts, the 5 returned maps, 2 scratch maps and 2 k x k arrays. That is 665.3 MB in root's case and 855.5 MB at most. After return, 364.4 MB stays held (the 5 maps, A and b). Root's inputs add 253.6 MB. tracemalloc at n = 576, k = 430 measured 10.498 map-equivalents against a formula of 10.493 (root's dtypes), and 13.497 against 13.493 with all maps cast. BLAS workspace is not traced.

Flops: four zgemm of 1720 x 2304 x 1720 (k x n times n x k), 54.5 GFLOP each and 218.1 GFLOP total. b takes three zgemv, 95.1 MFLOP. About 53 elementwise passes over (n,k) arrays are memory-bound.

## Not supplied
- No solve, inverse, pseudoinverse, ridge, clipping, spectrum, solution, tolerance or acceptance.
- No boundary-trace certification: the pressure surface term is dropped under root's continuum weak-domain zero-flux assumption.
- No density reconstruction, pressure reset, extra quadrature factor or m = 0 forcing, and no physical assessment.

## Discrepancy with pinned v002 lines 44-58
None in the equations. Lines 44-48, 52-54 and 58 match the contract term by term after renaming W to Omega, WR/WZ to Omega_R/Omega_z, RR to R, vol to w, wrho to w*rho and im to 1j*m. v002 computes three things the contract instead supplies: divU (line 49), the forcing gradients f_R, f_phi, f_z (lines 55-57, from the FFT of angular_forcing_dPhi + lagged_feedback_Phi), and G (line 43, just before the range). The forcing gradients are therefore a supplied input in addition to G and divU. The grouped contraction applies line 54's weights w*P_R/rho and w*P_z/rho to G instead of to U^H. By associativity the result is identical.
