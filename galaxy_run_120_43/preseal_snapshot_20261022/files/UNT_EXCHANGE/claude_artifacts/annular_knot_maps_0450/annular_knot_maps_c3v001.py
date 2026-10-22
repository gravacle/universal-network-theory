"""Inert annular-knot radial trial maps on the saved 72x32 quadrature (dispatch 0450, Claude3, c3v001).

Root contract: UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/
ANNULAR_KNOT_RADIAL_CORRECTION_CHOICE_V001.json,
sha256 58ffcbb86cd6512bb02ddf384a593311d1a9483f73f0cd83633432a9f5ef073e.
Numerical discretization correction only: the same 72x32 physical points, roots,
zeta, quadrature weights and root radial derivatives; no field, forcing, entropy,
source or force-law change; no density projection, Euler solve, regularization or
physical acceptance.  Physical status: not_assessed.

* build_annular_scalar_maps recovers the 19 annular edges in s=(R/L)^2 from the
  18 ordered four-point Gauss-Legendre groups of the existing radial nodes
  (verified, never guessed), then builds natural-cubic cardinal splines in s on
  those edges with the pinned binding-v002 spline helper.  Scalar maps are
  V=B_j P_a, partial_R V=B_R,j P_a - B_j P'_a (center_R+zeta*height_R)/height and
  partial_z V=B_j P'_a/height, shape 2304x152 (trial 19x8, quadrature 72x32).
* build_annular_regular_helicity_maps is the reviewed v001 Cartesian-regular
  helicity construction generalized solely from 576 to 152 scalar columns: same
  exponents |m+1|,|m-1|,|m|, normalization from the actual dimensionless stacked
  maps, the same eight true-outer xi_R=0 rows, complete QR and rank threshold,
  no free-surface xi_z lid; m=1..6.  It returns the same physical map names.

Pinned reusable references (sha256 custody assertions supplied by the caller):
v001 scalar maps (old_scalar_maps producer) and binding v002 (_spline_matrices).
The v001 helicity module is the reference generalized here, not imported.
Interface: INTERFACE_0450_V001.md.
"""

import numbers

import numpy as np

__all__ = ["build_annular_scalar_maps", "build_annular_regular_helicity_maps",
           "MODULE_VERSION", "CONTRACT_SHA256", "OLD_SCALAR_MAP_SHA256",
           "OLD_HELICITY_MAP_SHA256", "BINDING_MODULE_SHA256"]

MODULE_VERSION = "c3v001"
CONTRACT_SHA256 = "58ffcbb86cd6512bb02ddf384a593311d1a9483f73f0cd83633432a9f5ef073e"
OLD_SCALAR_MAP_SHA256 = "3bd792bafcfc32f5e0ed9e7cc62bdfec67a3ec185bd80ce1981f90dbe30db943"
OLD_HELICITY_MAP_SHA256 = "280149dc028260d865604948633bb8a1332c5ee01be916895c02df42e2b280c6"
BINDING_MODULE_SHA256 = "87866875f8a6883f62b778c123326f3c65090fdacae4fe8c79913e07b4405462"
SCALAR_STATUS = "ANNULAR_KNOT_SCALAR_MAPS"

NR, NQ, NV = 72, 32, 8      # radial nodes, vertical quadrature points per column, Legendre coefficients
NGROUP, NGL = 18, 4         # annuli, Gauss-Legendre points per annulus
NEDGE = NGROUP + 1          # 19 annular edges = radial spline knots
NSCALAR = NEDGE * NV        # 152 scalar trial columns, index j*8+a


def finite(a, name):
    a = np.asarray(a)
    if not np.isfinite(a).all():
        raise ValueError("Nonfinite " + name)
    return a


def _real_array(value, name, shape):
    """Real (integer/floating) finite array of exact shape, as float64; complex is rejected."""
    a = np.asarray(value)
    if a.dtype.kind not in "iuf":
        raise ValueError(f"{name}: real integer/floating array required, got dtype {a.dtype}")
    if a.shape != shape:
        raise ValueError(f"{name}: shape {shape} required, got {a.shape}")
    return finite(a.astype(np.float64, copy=False), name)


def _real_scalar(value, name):
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError(f"{name}: real number required")
    value = float(value)
    if not np.isfinite(value):
        raise ValueError(f"{name}: finite value required")
    return value


def build_annular_scalar_maps(*, old_scalar_maps, old_scalar_map_sha256, radial_nodes_m,
                              radial_RdR_weights_m2, outer_radius_m, binding_module,
                              binding_module_sha256, edge_absolute_tolerance,
                              weight_relative_tolerance):
    """Annular-knot 19x8 scalar trial maps on the existing 72x32 points.  See module docstring."""
    # ----------------------------------------------------------- custody pins
    if old_scalar_map_sha256 != OLD_SCALAR_MAP_SHA256:
        raise ValueError("old_scalar_map_sha256: reviewed v001 scalar-map pin required")
    if binding_module_sha256 != BINDING_MODULE_SHA256:
        raise ValueError("binding_module_sha256: pinned binding v002 spline helper required")
    spline = getattr(binding_module, "_spline_matrices", None)
    if not callable(spline):
        raise ValueError("binding_module: pinned _spline_matrices helper required")
    tol_s = _real_scalar(edge_absolute_tolerance, "edge_absolute_tolerance")
    tol_w = _real_scalar(weight_relative_tolerance, "weight_relative_tolerance")
    if tol_s < 0 or tol_w < 0:
        raise ValueError("Explicit finite nonnegative edge/weight tolerances required")

    # ------------------------------------------------- radial nodes and weights
    L = _real_scalar(outer_radius_m, "outer_radius_m")
    R = _real_array(radial_nodes_m, "radial_nodes_m", (NR,))
    wr = _real_array(radial_RdR_weights_m2, "radial_RdR_weights_m2", (NR,))
    if not L > 0 or np.any(R <= 0) or np.any(R >= L) or np.any(np.diff(R) <= 0) or np.any(wr <= 0):
        raise ValueError("Actual ordered interior radial nodes, positive RdR weights and true outer radius required")

    # ------------------------------------------------- old pinned scalar geometry
    if not isinstance(old_scalar_maps, dict) or old_scalar_maps.get("trial_shape") != [NR, NV] \
            or old_scalar_maps.get("quadrature_shape") != [NR, NQ] \
            or not isinstance(old_scalar_maps.get("arrays"), dict):
        raise ValueError("old_scalar_maps: actual v001 72x8 trial / 72x32 quadrature maps required")
    old = old_scalar_maps["arrays"]
    keys = ("value", "zeta", "weights_RdRdz", "roots_m", "root_radial_derivatives", "radial_derivative")
    if any(k not in old for k in keys):
        raise ValueError("old_scalar_maps: arrays " + ", ".join(keys) + " required")
    Vold = _real_array(old["value"], "old value", (NR * NQ, NR * NV))
    zeta = _real_array(old["zeta"], "old zeta", (NR, NQ))
    wq = _real_array(old["weights_RdRdz"], "old weights_RdRdz", (NR * NQ,))
    roots = _real_array(old["roots_m"], "old roots_m", (NR, 2))
    root_R = _real_array(old["root_radial_derivatives"], "old root_radial_derivatives", (NR, 2))
    DR_old = _real_array(old["radial_derivative"], "old radial_derivative", (NR, NR))
    # Same vertical geometry and degree-7 Legendre maps as v001 (identical expressions).
    center = np.mean(roots, axis=1)
    height = (roots[:, 1] - roots[:, 0]) / 2
    if np.any(height <= 0):
        raise ValueError("old roots_m: positive half-heights required")
    P = np.polynomial.legendre.legvander(zeta, 7)
    dP = np.stack([np.polynomial.legendre.legval(zeta, np.polynomial.legendre.legder(np.eye(8)[a]))
                   for a in range(8)], axis=-1)
    idx = np.arange(NR)
    if not np.array_equal(Vold.reshape(NR, NQ, NR, NV)[idx, :, idx, :], P):
        raise ValueError("old_scalar_maps: value blocks do not reproduce Legendre maps of the stored zeta")
    # Root radial derivatives preserved exactly as v001 computed them from its 72-knot spline.
    center_R = np.einsum("ij,j->i", DR_old, center, optimize=False)
    height_R = np.einsum("ij,j->i", DR_old, height, optimize=False)
    if not np.array_equal(root_R, np.stack((center_R - height_R, center_R + height_R), axis=-1)):
        raise ValueError("old_scalar_maps: root_radial_derivatives do not reproduce from the stored radial_derivative")
    # The supplied RdR weights must be those inside the preserved quadrature weights:
    # weights_RdRdz = wr x wz with sum(wz) = 2*height per column (v001 construction).
    column = wq.reshape(NR, NQ).sum(axis=1)
    custody = float(np.max(np.abs(column - 2 * height * wr) / (2 * height * wr)))
    if not custody <= tol_w:
        raise ValueError(f"radial_RdR_weights_m2 do not match the preserved weights_RdRdz (relative {custody:.3e})")

    # ------------------------------------- annular edges from the GL groups in s
    x, w = np.polynomial.legendre.leggauss(NGL)
    s = (R / L) ** 2
    groups = s.reshape(NGROUP, NGL)
    mid = groups.mean(axis=1)                 # least-squares centre (symmetric GL nodes, sum(x)=0)
    half = (groups @ x) / (x @ x)             # least-squares half-width in s
    if np.any(half <= 0):
        raise ValueError("radial_nodes_m: each four-node group must be an increasing GL group in s")
    node_residual = float(np.max(np.abs(groups - (mid[:, None] + half[:, None] * x[None, :]))))
    lo, hi = mid - half, mid + half
    adjacent = float(np.max(np.abs(hi[:-1] - lo[1:])))
    s0_residual, s18_residual = float(abs(lo[0])), float(abs(hi[-1] - 1.0))
    worst = max(node_residual, adjacent, s0_residual, s18_residual)
    if not worst <= tol_s:
        raise ValueError(
            "radial_nodes_m are not 18 contiguous four-point GL groups in s=(R/L)^2 on [0,1] at "
            f"edge_absolute_tolerance: node {node_residual:.3e}, adjacent {adjacent:.3e}, "
            f"s0 {s0_residual:.3e}, s18 {s18_residual:.3e}; no edge is guessed")
    edges = np.empty(NEDGE)
    edges[0], edges[-1] = 0.0, 1.0
    edges[1:-1] = 0.5 * (hi[:-1] + lo[1:])    # the two estimates agree within tolerance
    if np.any(np.diff(edges) <= 0):
        raise ValueError("Recovered annular edges are not strictly increasing")
    expected_wr = (L * L / 2) * (np.diff(edges) / 2)[:, None] * w[None, :]   # R dR = (L^2/2) ds
    weight_residual = float(np.max(np.abs(wr.reshape(NGROUP, NGL) - expected_wr) / expected_wr))
    if not weight_residual <= tol_w:
        raise ValueError(f"radial_RdR_weights_m2 are not the GL weights of the recovered annuli "
                         f"(relative {weight_residual:.3e})")

    # ----------------------- natural cubic cardinal splines in s on the 19 edges
    values, derivatives = spline(edges, list(s) + [1.0])
    values = finite(np.asarray(values, float), "spline values")
    derivatives = finite(np.asarray(derivatives, float), "spline s-derivatives")
    if values.shape != (NR + 1, NEDGE) or derivatives.shape != (NR + 1, NEDGE):
        raise ValueError("Spline helper returned unexpected shapes")
    B = values[:NR]                                         # B_j(s_i), 72x19
    B_R = (2 * R / L ** 2)[:, None] * derivatives[:NR]      # dB_j/dR = (2R/L^2) dB_j/ds
    outer = values[NR]
    if not np.array_equal(outer, np.eye(NEDGE)[-1]):
        raise ValueError("Spline helper did not give the exact unit outer trace at s=1")

    # ------------------------------------------------------- 2304x152 scalar maps
    # -d(zeta)/dR at fixed z for zeta=(z-center(R))/height(R), with preserved v001 root slopes.
    slope = (center_R[:, None] + zeta * height_R[:, None]) / height[:, None]
    V = np.einsum("ij,ila->ilja", B, P, optimize=False)
    VR = np.einsum("ij,ila->ilja", B_R, P, optimize=False) \
        - np.einsum("ij,ila->ilja", B, dP * slope[:, :, None], optimize=False)
    VZ = np.einsum("ij,ila->ilja", B, dP / height[:, None, None], optimize=False)
    V, VR, VZ = (a.reshape(NR * NQ, NSCALAR) for a in (V, VR, VZ))
    parity = (-1.0) ** np.arange(NV)
    arrays = dict(
        value=V, partial_R=VR, partial_z=VZ,
        weights_RdRdz=wq.copy(), zeta=zeta.copy(), roots_m=roots.copy(),
        root_radial_derivatives=root_R.copy(),
        outer_coefficient_trace=np.kron(outer[None, :], np.eye(NV)),   # exact xi trace rows at s=1
        lower_surface_trace=np.kron(B, parity[None, :]),            # zeta=-1 value at the 72 radial nodes
        upper_surface_trace=np.kron(B, np.ones((1, NV))),            # zeta=+1 value at the 72 radial nodes
        radial_value=B, radial_derivative=B_R,
        annular_edges_s=edges, annular_edges_R_m=L * np.sqrt(edges))
    if any(not np.isfinite(a).all() for a in arrays.values()):
        raise ValueError("Nonfinite annular scalar maps")
    return dict(
        status=SCALAR_STATUS, arrays=arrays, trial_shape=[NEDGE, NV], quadrature_shape=[NR, NQ],
        edge_recovery=dict(
            gl_nodes=x, gl_weights=w, max_node_residual_s=node_residual,
            max_adjacent_edge_mismatch_s=adjacent, s0_residual=s0_residual, s18_residual=s18_residual,
            max_weight_relative_residual=weight_residual, weights_custody_max_relative=custody,
            edge_absolute_tolerance=tol_s, weight_relative_tolerance=tol_w),
        provenance=dict(
            module_version=MODULE_VERSION, contract_sha256=CONTRACT_SHA256,
            old_scalar_map_sha256=old_scalar_map_sha256, binding_module_sha256=binding_module_sha256,
            outer_radius_m=L, radial_nodes_m=R.copy()),
        scope=("Natural-cubic cardinal splines in s=(R/L)^2 on the 19 recovered annular edges times "
               "degree-7 Legendre in zeta; the same 72x32 points, quadrature weights, roots, zeta and "
               "root radial derivatives as v001. V is not block diagonal: radial cardinal splines have "
               "global support."),
        not_supplied=("No density projection: the 0438 block-diagonal projection does not apply to these "
                      "maps (root uses pointwise Gkin). No helicity transform here, fluid solve, surface lid, "
                      "regularization, convergence claim or physical acceptance."))


def build_annular_regular_helicity_maps(*, scalar_maps, radial_nodes_m, outer_radius_m, m,
                                        rank_relative_tolerance, rank_absolute_tolerance):
    """v001 Cartesian-regular helicity maps on the annular-knot 19x8 scalar maps (2304x448)."""
    if not isinstance(scalar_maps, dict) or scalar_maps.get("status") != SCALAR_STATUS \
            or scalar_maps.get("trial_shape") != [NEDGE, NV] \
            or scalar_maps.get("quadrature_shape") != [NR, NQ] \
            or not isinstance(scalar_maps.get("provenance"), dict) \
            or scalar_maps["provenance"].get("module_version") != MODULE_VERSION:
        raise ValueError("scalar_maps: output of build_annular_scalar_maps (this module version) required")
    if type(m) is not int or not 1 <= m <= 6:
        raise ValueError("Declared modes1..6 only")
    controls = np.asarray([rank_relative_tolerance, rank_absolute_tolerance], float)
    if not np.isfinite(controls).all() or np.any(controls < 0):
        raise ValueError("Explicit finite nonnegative hard-rank controls required")
    L = float(outer_radius_m)
    R = finite(np.asarray(radial_nodes_m, float), "radial nodes")
    if not np.isfinite(L) or L <= 0 or R.shape != (NR,) or np.any(R <= 0) or np.any(R >= L) \
            or np.any(np.diff(R) <= 0):
        raise ValueError("Actual ordered interior radial nodes and true outer radius required")
    if L != scalar_maps["provenance"].get("outer_radius_m") \
            or not np.array_equal(R, scalar_maps["provenance"].get("radial_nodes_m")):
        raise ValueError("radial_nodes_m/outer_radius_m differ from those of the scalar maps")
    a = scalar_maps["arrays"]
    if any(np.iscomplexobj(a[key]) for key in ("value", "partial_R", "partial_z", "outer_coefficient_trace")):
        raise ValueError("Real scalar maps required, no imaginary-part projection")
    V = finite(np.asarray(a["value"], float), "V")
    VR = finite(np.asarray(a["partial_R"], float), "VR")
    VZ = finite(np.asarray(a["partial_z"], float), "VZ")
    T = finite(np.asarray(a["outer_coefficient_trace"], float), "outer trace")
    if V.shape != (NR * NQ, NSCALAR) or VR.shape != V.shape or VZ.shape != V.shape or T.shape != (NV, NSCALAR):
        raise ValueError("Annular scalar-map dimensions")
    result = _regular_helicity_core(V=V, VR=VR, VZ=VZ, T=T, R=R, L=L, m=m,
                                    rank_relative_tolerance=rank_relative_tolerance,
                                    rank_absolute_tolerance=rank_absolute_tolerance)
    result.update(trial_shape=[NEDGE, NV], quadrature_shape=[NR, NQ],
                  annular_edges_s=a["annular_edges_s"].copy(),
                  scalar_map_provenance=dict(scalar_maps["provenance"]),
                  module_version=MODULE_VERSION, reference_generalized=OLD_HELICITY_MAP_SHA256)
    return result


def _regular_helicity_core(*, V, VR, VZ, T, R, L, m, rank_relative_tolerance, rank_absolute_tolerance):
    """The v001 helicity construction with nscalar=V.shape[1] in place of the fixed 576.

    Every expression below is the v001 expression (owned_32q8_regular_helicity_maps_v001.py,
    lines 27-71) with the literal 576/1152 replaced by n/2n.
    """
    n = V.shape[1]
    rr = np.repeat(R, NQ)
    exponents = (abs(m + 1), abs(m - 1), abs(m))
    factors = [finite((rr / L) ** e, "regularity power") for e in exponents]
    values = [finite(f[:, None] * V, "raw scalar helicity map") for f in factors]
    # Exactly the Euclidean norms of stacked dimensionless (UR,UP,UZ)/L:
    # each transverse helicity contributes1/4+1/4; the vertical contributes1.
    norm_parts = [np.sqrt(.5 * np.sum(values[0] ** 2, axis=0)), np.sqrt(.5 * np.sum(values[1] ** 2, axis=0)),
                  np.sqrt(np.sum(values[2] ** 2, axis=0))]
    norms = finite(np.concatenate(norm_parts), "stacked dimensionless column norms")
    if np.any(norms <= 0):
        raise ValueError("Zero/underflowed trial column; no zero-scale or ridge substitute")
    inverse_norms = finite(1 / norms, "inverse column norms")
    Braw = np.concatenate((.5 * T, .5 * T, np.zeros_like(T)), axis=1)
    B = finite(Braw * inverse_norms[None, :], "normalized hard constraint")
    singular = finite(np.linalg.svd(B, compute_uv=False), "hard singular values")
    threshold = float(rank_absolute_tolerance + rank_relative_tolerance * singular[0])
    if not np.isfinite(threshold):
        raise ValueError("Nonfinite hard rank threshold")
    common = dict(m=m, hard_constraint_raw=Braw, hard_constraint_normalized=B, hard_singular_values=singular,
                  rank_threshold=threshold, column_norms=norms, inverse_column_norms=inverse_norms,
                  normalization="Euclidean norms of stacked raw dimensionless quadrature maps, not a condition-number claim",
                  regularity_exponents=list(exponents), outer_radius_m=L,
                  scope="Numeric trial/test/outer-constraint maps only; no physical solution, gauge removal beyond stated outer constraint, or surface lid")
    if singular[-1] <= threshold:
        return dict(status="UNRESOLVED_OUTER_CONSTRAINT_RANK", **common)
    Q, _ = np.linalg.qr(B.T, mode="complete")
    Z = finite(Q[:, B.shape[0]:], "normalized-coordinate nullspace")
    del Q
    hard_residual = finite(B @ Z, "hard nullspace residual")
    # Raw dimensionless coefficients = diag(1/norms) Z times reduced coefficients.
    raw_transform = finite(inverse_norms[:, None] * Z, "raw coefficient transform")
    plus, minus, vertical = raw_transform[:n], raw_transform[n:2 * n], raw_transform[2 * n:]
    maps = {}

    def transform(parts, prefix):
        # Independent scalar projections bound transient memory; no q*3n raw stack.
        p = finite(parts[0] @ plus, prefix + " plus projection")
        q = finite(parts[1] @ minus, prefix + " minus projection")
        maps[prefix + "R"] = finite((L / 2) * (p + q), prefix + "R")
        maps[prefix + "P"] = finite((L / (2j)) * (p - q), prefix + "P")
        del p, q
        maps[prefix + "Z"] = finite(L * (parts[2] @ vertical), prefix + "Z")

    transform(values, "U")
    radial = [finite(f[:, None] * VR + (e / rr)[:, None] * value, "exact radial product rule")
              for e, f, value in zip(exponents, factors, values)]
    transform(radial, "partial_R_U")
    del radial
    vertical_derivatives = [finite(f[:, None] * VZ, "vertical product rule") for f in factors]
    transform(vertical_derivatives, "partial_z_U")
    del vertical_derivatives, values
    div = finite(maps["partial_R_UR"] + maps["UR"] / rr[:, None] + (1j * m) * maps["UP"] / rr[:, None]
                 + maps["partial_z_UZ"], "cylindrical divergence test map")
    residual_norm = float(np.linalg.norm(hard_residual))
    if not np.isfinite(residual_norm):
        raise ValueError("Nonfinite hard nullspace residual norm")
    return dict(status="REGULAR_HELICITY_MAPS", **common, **maps, divU=div, normalized_nullspace=Z,
                raw_coefficient_transform=raw_transform, hard_nullspace_residual=hard_residual,
                hard_nullspace_residual_norm=residual_norm,
                coordinate_contract="Every physical U and derivative maps the SAME reduced coefficients. Raw coefficients=raw_coefficient_transform@y; normalized coefficients=normalized_nullspace@y. Use identical maps for trial and test.",
                boundary_contract="At true outer R=L powers equal1;8rows impose polynomial xiR=0. No upper/lower xiZ lid; physical-vacuum weak flux remains the declared domain assumption.",
                resource_scope=f"Returned ten{V.shape[0]}x{Z.shape[1]} maps plus coefficient transforms; caller must budget actual memory. No small-memory/conditioning/mixing claim.")
