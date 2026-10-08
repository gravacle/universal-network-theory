"""Finite N2 mobile-carrier ground band versus its second-order Hamiltonian.

AUTHORING ONLY until explicitly invoked with --run. Original same-content
hard-core qutrit transfers, not fermionic/Jordan-Wigner signs. Records are
blank and held, all copying/port couplings are off; no clock is fabricated.
Q=0,1,2 sectors have dimensions 16,64,96. The low band is compared with the
carrier-space virtual-link operator, retaining the complete baseline energy.

Only h=1/2 has native Omega=1. Smaller h are explicitly changed-Omega,
finite-size asymptotic controls. Pair-addition energy is not spatial binding,
a force, gravity, or a demonstration of preparation/relaxation. A negative
2*alpha coefficient is reported separately from the pair-addition energy.

The inherited 1e-10 allowance is an assigned arithmetic allowance, not a
certified roundoff bound, a fitted tolerance, or a scientific-success gate.
The finite-size R4 bound is tested only in its sufficient domain v<gap/4;
native parameters outside that domain are NOT a failed scientific check.
No subprocesses, network, source imports, trajectories, or source overwrite.
"""

import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import tempfile
import time

HERE = Path(__file__).resolve().parent
BS = HERE.parent / "recovered_sources" / "BS_MICRO_ACTION.md"
BS_SHA = "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec"
OUTPUT = HERE / "native_mobile_carrier_effective_v001_results.json"
EDGES = ((0, 2), (0, 3), (1, 2), (1, 3))
TOL = 1e-10
THREAD_KEYS = ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
               "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
BASE = dict(Delta=4., U_d=1., d_star=1., epsilon_psi=1.)
np = None  # Imported only inside the explicitly requested run.


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode()


def carrier_operators(number):
    """Tensor-site hard-core transfer: every legal exchange has sign +1."""
    masks = [m for m in range(16) if m.bit_count() == number]
    index = {m: k for k, m in enumerate(masks)}
    size = len(masks)
    xor_ops, transfers = [], []
    for u, v in EDGES:
        xor, transfer = np.zeros((size, size)), np.zeros((size, size))
        for col, mask in enumerate(masks):
            one = ((mask >> u) & 1) != ((mask >> v) & 1)
            xor[col, col] = float(one)
            if one:
                transfer[index[mask ^ (1 << u) ^ (1 << v)], col] = 1.
        xor_ops.append(xor)
        transfers.append(transfer)
    return masks, xor_ops, transfers


def full_components(p, number, masks, xor_ops, transfers):
    """Incidence tensor carrier construction; mask-major tensor ordering."""
    size, ident_g, ident_c = len(masks), np.eye(16), np.eye(len(masks))
    bits = np.array([[(m >> e) & 1 for e in range(4)] for m in range(16)])
    degrees = np.array([[sum(bits[m, e] for e, edge in enumerate(EDGES) if v in edge)
                         for v in range(4)] for m in range(16)])
    n_ops = [np.diag(bits[:, e].astype(float)) for e in range(4)]
    flip_sum = np.zeros((16, 16))
    for mask in range(16):
        for e in range(4):
            flip_sum[mask ^ (1 << e), mask] += 1.
    terms = dict(
        carrier_storage=p["epsilon_psi"]*number*np.eye(16*size),
        incidence_gap=np.kron(np.diag(p["Delta"]*bits.sum(axis=1)), ident_c),
        complete_degree_penalty=np.kron(np.diag(p["U_d"]*
            ((degrees-p["d_star"])**2).sum(axis=1)), ident_c),
        incidence_flips=-p["h"]*np.kron(flip_sum, ident_c),
        current_square=p["j"]*sum(np.kron(n, c) for n, c in zip(n_ops, xor_ops)),
        carrier_hopping=-p["t"]*sum(np.kron(n, t) for n, t in zip(n_ops, transfers)))
    total = sum(terms.values())
    link_number = np.kron(np.diag(bits.sum(axis=1).astype(float)), ident_c)
    return total, terms, link_number


def independent_entries(p, number, masks):
    """Independent basis-entry builder, without tensor component matrices."""
    count, index = len(masks), {mask: k for k, mask in enumerate(masks)}
    total = np.zeros((16*count, 16*count))
    for graph in range(16):
        present = [e for e in range(4) if graph & (1 << e)]
        degrees = [sum(v in EDGES[e] for e in present) for v in range(4)]
        base = (p["epsilon_psi"]*number+p["Delta"]*len(present)
                +p["U_d"]*sum((d-p["d_star"])**2 for d in degrees))
        for col_c, occupied in enumerate(masks):
            col = graph*count+col_c
            total[col, col] = base
            for e in range(4):
                total[(graph ^ (1 << e))*count+col_c, col] = -p["h"]
            for e in present:
                u, v = EDGES[e]
                if bool(occupied & (1 << u)) != bool(occupied & (1 << v)):
                    total[col, col] += p["j"]
                    moved = occupied ^ (1 << u) ^ (1 << v)
                    total[graph*count+index[moved], col] = -p["t"]
    return total


def run():
    global np
    started = time.perf_counter()
    if OUTPUT.exists() or OUTPUT.is_symlink():
        raise FileExistsError("Refusing to overwrite "+str(OUTPUT))
    if BS.is_symlink() or digest(BS) != BS_SHA:
        raise RuntimeError("Original BS source pin changed")
    source_sha = digest(Path(__file__))
    for key in THREAD_KEYS:
        os.environ[key] = "1"
    import numpy as np
    if any(os.environ.get(key) != "1" for key in THREAD_KEYS):
        raise RuntimeError("Single-thread numerical configuration was not retained")
    checks, cases = [], []

    def check(name, actual, expected=0.):
        error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        checks.append(dict(name=name, residual=error if math.isfinite(error) else None,
            assigned_allowance=TOL, passed=math.isfinite(error) and error <= TOL))

    def upper_check(name, value, bound):
        excess = max(0., float(value-bound))
        check(name, excess)

    def eigensystem(matrix, tag):
        values, vectors = np.linalg.eigh(matrix)
        residual = float(np.max(np.abs(matrix @ vectors-vectors*values)))
        orthogonal = float(np.max(np.abs(vectors.T @ vectors-np.eye(len(values)))))
        reconstruction = float(np.max(np.abs((vectors*values) @ vectors.T-matrix)))
        check(tag+":hermiticity", matrix, matrix.T)
        check(tag+":eigen_residual", residual)
        check(tag+":orthogonality", orthogonal)
        check(tag+":spectral_reconstruction", reconstruction)
        return values, vectors, dict(max_abs_eigen_residual=residual,
            max_abs_orthogonality_residual=orthogonal,
            max_abs_spectral_reconstruction_residual=reconstruction)

    specifications = []
    for family, j, hopping in (("native_couplings", .25, .5),
                               ("j_off", 0., .5), ("t_off", .25, 0.)):
        for denominator in (2, 40, 80, 160):
            specifications.append((family, denominator, j, hopping))
    specifications.extend((("j_t_off_exact_null", 2, 0., 0.),
                           ("j_equals_t_exact_all_h", 2, .5, .5)))

    for family, denominator, j, hopping in specifications:
        p = dict(BASE, h=1./denominator, j=j, t=hopping)
        case_id = family+":h=1/"+str(denominator)
        k = p["Delta"]+2*p["U_d"]*(1-2*p["d_star"])
        determinant = (k+j)**2-hopping**2
        gap_bound = k+min(0., j-abs(hopping))
        if not (k > 0 and determinant > 0 and gap_bound > 0):
            raise RuntimeError("Prospective positive virtual-gap domain changed")
        alpha = p["h"]**2*((k+j)/determinant-1/k)
        effective_hopping = p["h"]**2*hopping/determinant
        v = 4*abs(p["h"])
        applicable = v < gap_bound/4
        remainder = 4*v**4/gap_bound**3 if applicable else None
        sectors = []
        incidence_ground_vector = None
        for number in (0, 1, 2):
            tag = case_id+":Q="+str(number)
            masks, xor_ops, transfers = carrier_operators(number)
            count, ident = len(masks), np.eye(len(masks))
            check(tag+":carrier_dimension", count, math.comb(4, number))
            for e, (xor, transfer) in enumerate(zip(xor_ops, transfers)):
                check(tag+":xor_projector:"+str(e), xor @ xor, xor)
                check(tag+":transfer_square:"+str(e), transfer @ transfer, xor)
                check(tag+":transfer_hermiticity:"+str(e), transfer, transfer.T)
            full, terms, link_number = full_components(p, number, masks, xor_ops, transfers)
            check(tag+":full_dimension", len(full), (16, 64, 96)[number])
            check(tag+":independent_entries", full, independent_entries(p, number, masks))
            check(tag+":component_reconstruction", full, sum(terms.values()))
            for label, term in terms.items():
                check(tag+":component_hermiticity:"+label, term, term.T)
            reference = 4*p["U_d"]*p["d_star"]**2+p["epsilon_psi"]*number
            check(tag+":blank_reference", full[:count, :count], reference*ident)
            h2_inverse = reference*ident
            inverse_rows = []
            for e, (xor, transfer) in enumerate(zip(xor_ops, transfers)):
                addition = k*ident+j*xor-hopping*transfer
                inverse = np.linalg.solve(addition, ident)
                closed_inverse = ((ident-xor)/k+((k+j)*xor+hopping*transfer)/determinant)
                check(tag+":edge_inverse:"+str(e), addition @ inverse, ident)
                check(tag+":closed_edge_inverse:"+str(e), inverse, closed_inverse)
                h2_inverse = h2_inverse-p["h"]**2*inverse
                inverse_rows.append(dict(edge=e, smallest_addition_eigenvalue=
                                         float(np.linalg.eigvalsh(addition)[0])))
            h2 = (reference-4*p["h"]**2/k)*ident-sum(
                alpha*xor+effective_hopping*transfer
                for xor, transfer in zip(xor_ops, transfers))
            check(tag+":effective_inverse_vs_decomposition", h2_inverse, h2)
            # Independent full-space virtual projection, retaining carrier motion
            # inside the nonblank incidence sectors rather than clamping a carrier.
            h0 = full-terms["incidence_flips"]
            eliminated = h0[count:, count:]-reference*np.eye(len(full)-count)
            coupling = terms["incidence_flips"][:count, count:]
            h2_schur = reference*ident-coupling @ np.linalg.solve(eliminated, coupling.T)
            check(tag+":effective_full_space_schur", h2_schur, h2)
            complement_gap = float(np.linalg.eigvalsh(eliminated)[0])
            upper_check(tag+":full_unperturbed_gap_lower_bound", gap_bound, complement_gap)

            values, vectors, diagnostics = eigensystem(full, tag+":full")
            effective_values, effective_vectors, effective_diagnostics = eigensystem(h2, tag+":effective")
            ground_indices = np.flatnonzero(np.abs(values-values[0]) <= TOL)
            ground_vectors = vectors[:, ground_indices]
            projector = ground_vectors @ ground_vectors.T
            rank = len(ground_indices)
            check(tag+":ground_projector_idempotence", projector @ projector, projector)
            check(tag+":ground_projector_trace", np.trace(projector), rank)
            average = lambda op: float(np.trace(ground_vectors.T @ op @ ground_vectors)/rank)
            link_mean = average(link_number)
            blank_weight = float(np.trace(projector[:count, :count])/rank)
            upper_check(tag+":ground_link_nonnegative", -link_mean, 0.)
            upper_check(tag+":ground_link_at_most_four", link_mean, 4.)
            upper_check(tag+":ground_blank_weight_nonnegative", -blank_weight, 0.)
            upper_check(tag+":ground_blank_weight_at_most_one", blank_weight, 1.)
            energy_terms = {label: average(term) for label, term in terms.items()}
            check(tag+":ground_component_energy", math.fsum(energy_terms.values()), float(values[0]))
            base_effective = 4*p["U_d"]*p["d_star"]**2-4*p["h"]**2/k
            analytic_ground = (base_effective,
                base_effective+p["epsilon_psi"]-2*alpha-2*effective_hopping,
                base_effective+2*p["epsilon_psi"]-3*alpha
                    -math.sqrt(alpha**2+8*effective_hopping**2))[number]
            check(tag+":analytic_effective_ground", float(effective_values[0]), analytic_ground)
            ground_error = abs(float(values[0]-effective_values[0]))
            bound_respected = None
            if applicable:
                bound_respected = ground_error <= remainder+TOL
                upper_check(tag+":fourth_order_ground_bound", ground_error, remainder)
            # Link parity eliminates odd-order virtual returns to incidence blank.
            parity = np.diag([(-1.)**(mask.bit_count()) for mask in range(16)])
            parity = np.kron(parity, ident)
            check(tag+":unperturbed_link_parity", parity @ h0 @ parity, h0)
            check(tag+":flip_link_parity", parity @ terms["incidence_flips"] @ parity,
                  -terms["incidence_flips"])
            if number == 0:
                incidence_ground_vector = vectors[:, 0].copy()
            if j == hopping:
                dicke = np.ones(count)/math.sqrt(count)
                for e, (xor, transfer) in enumerate(zip(xor_ops, transfers)):
                    check(tag+":dicke_current_hopping_null:"+str(e), (xor-transfer) @ dicke)
                    upper_check(tag+":current_minus_transfer_positive:"+str(e),
                        -float(np.linalg.eigvalsh(xor-transfer)[0]), 0.)
                product = np.kron(incidence_ground_vector, dicke)
                exact_ground = sectors[0]["ground_energy"]+p["epsilon_psi"]*number if number else float(values[0])
                check(tag+":all_h_additive_ground_oracle", float(values[0]), exact_ground)
                check(tag+":all_h_product_ground_residual", full @ product-exact_ground*product)
            low_vectors = vectors[:, :count]
            low_blank_weight = float(np.sum(low_vectors[:count, :]**2)/count)
            sectors.append(dict(carrier_number=number, carrier_masks=masks,
                dimension=len(full), effective_dimension=count, complete_blank_reference=reference,
                full_spectrum=values.tolist(), effective_spectrum=effective_values.tolist(),
                full_eigensolver=diagnostics, effective_eigensolver=effective_diagnostics,
                lowest_band_rank=count, lowest_band_width=float(values[count-1]-values[0]),
                gap_above_lowest_rank_band=float(values[count]-values[count-1]),
                low_band_average_blank_projector_weight=low_blank_weight,
                ground_energy=float(values[0]), effective_ground_energy=float(effective_values[0]),
                effective_analytic_ground_energy=analytic_ground,
                ground_projector_rank=rank, ground_grouping_absolute_allowance=TOL,
                ground_group_energy_spread=float(values[ground_indices[-1]]-values[0]),
                ground_next_resolved_gap=float(values[rank]-values[0]) if rank < len(values) else None,
                ground_link_number=link_mean, ground_dressed_blank_link_weight=blank_weight,
                ground_complete_component_energies=energy_terms,
                ground_energy_error=ground_error, ground_error_over_h_four=ground_error/p["h"]**4,
                unperturbed_complement_gap=complement_gap, virtual_edge_inverses=inverse_rows,
                rigorous_finite_N_sufficient_domain=applicable,
                finite_N_ground_error_bound=remainder, ground_bound_respected=bound_respected))

        binding = sectors[2]["ground_energy"]+sectors[0]["ground_energy"]-2*sectors[1]["ground_energy"]
        effective_binding = (sectors[2]["effective_ground_energy"]
                             +sectors[0]["effective_ground_energy"]
                             -2*sectors[1]["effective_ground_energy"])
        analytic_binding = alpha+4*effective_hopping-math.sqrt(alpha**2+8*effective_hopping**2)
        check(case_id+":effective_binding_formula", effective_binding, analytic_binding)
        pair_error_bound = 4*remainder if applicable else None
        pair_error = abs(binding-effective_binding)
        pair_bound_respected, sign_certified = None, None
        if applicable:
            pair_bound_respected = pair_error <= pair_error_bound+TOL
            upper_check(case_id+":fourth_order_pair_addition_bound", pair_error, pair_error_bound)
            sign_certified = abs(effective_binding) > pair_error_bound+TOL
        if j == hopping:
            check(case_id+":exact_all_h_additive_binding", binding)
            check(case_id+":effective_all_h_additive_binding", effective_binding)
        if j == 0 and hopping == 0:
            for sector in sectors:
                check(case_id+":null_link_mean:Q="+str(sector["carrier_number"]),
                      sector["ground_link_number"], sectors[0]["ground_link_number"])
                check(case_id+":null_blank_weight:Q="+str(sector["carrier_number"]),
                      sector["ground_dressed_blank_link_weight"], sectors[0]["ground_dressed_blank_link_weight"])
        cases.append(dict(case_id=case_id, family=family, parameters=p,
            h_exact="1/"+str(denominator), Omega=2*p["h"], native_Omega=denominator == 2,
            changed_Omega_asymptotic_control=denominator != 2,
            k=k, determinant=determinant, alpha=alpha, J_effective=effective_hopping,
            pair_coefficient_2alpha=2*alpha, full_pair_addition_energy=binding,
            effective_pair_addition_energy=effective_binding,
            effective_pair_addition_analytic=analytic_binding,
            pair_addition_full_minus_effective=binding-effective_binding,
            pair_addition_absolute_error=pair_error,
            finite_N_pair_addition_error_bound=pair_error_bound,
            pair_addition_bound_respected=pair_bound_respected,
            sign_certified_by_sufficient_bound=sign_certified,
            certified_pair_addition_sign=("positive" if effective_binding > 0 else "negative")
                if sign_certified else None,
            finite_N_gap_lower_bound=gap_bound, perturbation_norm_bound=v,
            rigorous_finite_N_sufficient_domain=applicable,
            finite_N_ground_error_bound=remainder,
            exact_additive_all_h_oracle=j == hopping, sectors=sectors))

    if digest(BS) != BS_SHA or digest(Path(__file__)) != source_sha:
        raise RuntimeError("Source changed during calculation")
    failures = [item for item in checks if not item["passed"]]
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = dict(status="COMPLETE" if not failures else "FAILED_IDENTITIES_OR_BOUND",
        source_sha256=source_sha, input_sha256={str(BS): BS_SHA},
        parameters_frozen_in_source=True, edge_order=EDGES, number_sectors=(0, 1, 2),
        assigned_arithmetic_allowance=TOL, roundoff_certified=False,
        ground_degeneracy_treatment="Normalized full ground projector; eigenvalues grouped within assigned absolute allowance",
        controls_frozen_before_first_run=True, cases=cases, checks=checks, failures=failures,
        check_counts=dict(total=len(checks), passed=len(checks)-len(failures)),
        scope=dict(finite_N=2, original_hard_core_qutrit_signs=True,
            same_content_carriers=True, mobile_carriers_not_clamped=True,
            blank_held_records=True, all_copy_and_port_couplings_off=True,
            physical_clock_supplied=False, physical_distance_supplied=False,
            physical_spatial_binding=False, gravity_identified=False,
            preparation_or_ground_relaxation_supplied=False,
            negative_pair_coefficient_is_not_binding_verdict=True,
            native_outside_sufficient_error_domain_is_not_failure=True),
        threading=dict(configured={key: os.environ[key] for key in THREAD_KEYS},
                       configured_before_numpy_import=True,
                       actual_native_thread_count_measured=False),
        runtime=dict(wall_seconds=time.perf_counter()-started,
            max_rss_bytes=peak if sys.platform == "darwin" else peak*1024))
    data = encoded(result)+b"\n"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=HERE, prefix=OUTPUT.name+".partial.", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, OUTPUT)  # Atomic, exclusive publication; never overwrite.
    finally:
        if temporary is not None:
            temporary.unlink()
    result_sha = hashlib.sha256(data).hexdigest()
    if digest(OUTPUT) != result_sha:
        raise RuntimeError("Published result hash mismatch")
    print(json.dumps(dict(status=result["status"], path=str(OUTPUT), sha256=result_sha,
        source_sha256=source_sha, bytes=len(data), check_counts=result["check_counts"],
        failures=failures, cases=[{key: case[key] for key in
            ("case_id", "pair_coefficient_2alpha", "full_pair_addition_energy",
             "effective_pair_addition_analytic", "rigorous_finite_N_sufficient_domain")}
            for case in cases], runtime=result["runtime"]), separators=(",", ":"), allow_nan=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    if sys.argv[1:] != ["--run"]:
        raise SystemExit("Explicit --run required; finite spectra and second-order comparison only")
    try:
        exit_code = run()
    except Exception as error:
        print(json.dumps(dict(status="ERROR", error_type=type(error).__name__, error=str(error))))
        exit_code = 1
    raise SystemExit(exit_code)
