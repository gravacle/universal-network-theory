"""Exact initial-series test of loading at L0 on the declared K2,2 support.

Edge 2=L1--R0 is NONINCIDENT to the initial carrier, not separated by an owned
physical distance. The initial graph is blank/disconnected. Original hard-core
qutrit transfer signs are retained. No force, binding, metric or dark-mass claim.
Link occupation is NOT automatically the transport of a newly injected probe:
hard-core blocking and source/probe preparation must also be accounted for.

All five prospective cases retain their own complete empty baseline. Lambda_R,
g_psi_r and g_rb vanish; four continuing (eps_r=g_wr=1) writer clocks factor
exactly, theta=sqrt(5)*tau/hbar. Their storage/copy energies remain in the ledger.
Fraction coefficients through order eight only: no finite-time propagation,
selected ages, numerical imports or finite-time remainder bound. One atomic
no-overwrite numerical JSON result preserves the complete audit; compact stdout.
"""
import sys
sys.dont_write_bytecode = True
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json
import os
import resource
import tempfile
import time

HERE = Path(__file__).resolve().parent
BS = HERE/"../recovered_sources/BS_MICRO_ACTION.md"
BS_SHA = "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec"
ORDER = 8
EDGES = ((0, 2), (0, 3), (1, 2), (1, 3))
BASE = dict(h=F(1, 2), Delta=F(4), U_d=F(1), d_star=F(1),
            epsilon_psi=F(1), j=F(1, 4), t=F(1, 2))


def matvec(matrix, vector):
    return [sum((a*b for a, b in zip(row, vector) if a and b), F(0)) for row in matrix]


def powers(action, size):
    result = [[F(int(i == 0)) for i in range(size)]]
    for _ in range(ORDER+1):
        result.append(action(result[-1]))
    return result


def series(vectors, operator):
    applied = [operator(v) for v in vectors[:ORDER+1]]
    answer = []
    for order in range(ORDER+1):
        real, imag = F(0), F(0)
        for n in range(order+1):
            m = order-n
            term = sum((a*b for a, b in zip(vectors[n], applied[m]) if a and b), F(0))/F(factorial(n)*factorial(m))
            phase = (n-m) % 4  # i^n (-i)^m; every retained operator is real.
            if phase == 0: real += term
            if phase == 1: imag += term
            if phase == 2: real -= term
            if phase == 3: imag -= term
        answer.append((real, imag))
    return answer


def combine(*parts):
    return [tuple(sum((part[n][c] for part in parts), F(0)) for c in (0, 1)) for n in range(ORDER+1)]


def scale(values, factor):
    return [(factor*a, factor*b) for a, b in values]


def pack(values):
    return dict(x_real=[str(a) for a, _ in values], x_imag=[str(b) for _, b in values],
                theta_even_real={str(n): str(values[n][0]/F(5**(n//2))) for n in range(0, ORDER+1, 2)},
                theta_even_imag={str(n): str(values[n][1]/F(5**(n//2))) for n in range(0, ORDER+1, 2)})


def dense_terms(p, occupied):
    nc = 4 if occupied else 1
    size = 16*nc
    names = ("incidence_gap", "degree_penalty", "incidence_flips", "carrier_storage", "current_square", "carrier_hopping")
    terms = {name: [[F(0) for _ in range(size)] for _ in range(size)] for name in names}
    for mask in range(16):
        bits = [(mask >> e) & 1 for e in range(4)]
        degrees = [sum(bits[e] for e, pair in enumerate(EDGES) if v in pair) for v in range(4)]
        for carrier in range(nc):
            row = mask*nc+carrier
            terms["incidence_gap"][row][row] = p["Delta"]*sum(bits)
            terms["degree_penalty"][row][row] = p["U_d"]*sum((d-p["d_star"])**2 for d in degrees)
            terms["carrier_storage"][row][row] = p["epsilon_psi"]*int(occupied)
            terms["current_square"][row][row] = p["j"]*degrees[carrier] if occupied else F(0)
            for e in range(4):
                terms["incidence_flips"][row][(mask ^ (1 << e))*nc+carrier] = -p["h"]
            if occupied:
                for e, (u, v) in enumerate(EDGES):
                    if bits[e] and carrier in (u, v):
                        terms["carrier_hopping"][row][mask*nc+(v if carrier == u else u)] = -p["t"]
    H = [[sum((term[i][j] for term in terms.values()), F(0)) for j in range(size)] for i in range(size)]
    return H, terms


def sparse_rows(p, occupied):
    """Independent adjacency-list builder, not read from dense components."""
    nc, rows = (4 if occupied else 1), []
    for graph in range(16):
        neighbors = [[] for _ in range(4)]
        for left in range(2):
            for right in range(2):
                if graph & (1 << (2*left+right)):
                    neighbors[left].append(2+right)
                    neighbors[2+right].append(left)
        graph_energy = p["Delta"]*graph.bit_count()+p["U_d"]*sum((len(group)-p["d_star"])**2 for group in neighbors)
        for c in range(nc):
            diagonal = graph_energy+(p["epsilon_psi"]+p["j"]*len(neighbors[c]) if occupied else 0)
            row = [(graph*nc+c, diagonal)]+[((graph ^ (1 << e))*nc+c, -p["h"]) for e in range(4)]
            if occupied:
                row += [(graph*nc+other, -p["t"]) for other in neighbors[c]]
            rows.append(row)
    return rows


def main():
    start = time.perf_counter()
    target = HERE/"native_remote_loading_series_v001_results.json"
    if target.exists() or target.is_symlink():
        raise FileExistsError("Refusing to overwrite "+str(target))
    source_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if hashlib.sha256(BS.read_bytes()).hexdigest() != BS_SHA:
        raise RuntimeError("Original BS source pin changed")
    checks, output_cases = [], []
    def check(name, got, expected=F(0)):
        residual = got-expected
        checks.append(dict(name=name, passed=residual == 0, exact_residual=str(residual)))
    def audit(name, values):
        for n, (real, imag) in enumerate(values):
            check(name+":imag:"+str(n), imag)
            if n % 2: check(name+":odd:"+str(n), real)
    clock_H, clock_X = [[F(0), F(1)], [F(1), F(1)]], [[F(0), F(1)], [F(1), F(0)]]
    clock_vectors = powers(lambda v: matvec(clock_H, v), 2)
    record_energy = scale(series(clock_vectors, lambda v: [F(0), v[1]]), F(4))
    copy_energy = scale(series(clock_vectors, lambda v: matvec(clock_X, v)), F(4))
    zero_series = [(F(0), F(0)) for _ in range(ORDER+1)]
    for n, value in enumerate(combine(record_energy, copy_energy)):
        check("four_factorized_clocks:energy_real:"+str(n), value[0])
        check("four_factorized_clocks:energy_imag:"+str(n), value[1])
    for m in range(1, 5):
        check("four_records:storage_oracle:"+str(2*m), record_energy[2*m][0], F(8*(-1)**(m+1)*5**(m-1), factorial(2*m)))
    cases = (("native", {}), ("j_off", {"j": F(0)}), ("t_off", {"t": F(0)}),
             ("U_d_off", {"U_d": F(0)}), ("j_t_off", {"j": F(0), "t": F(0)}))
    for label, changes in cases:
        p, arms, internal = dict(BASE, **changes), {}, {}
        for occupied, arm in ((False, "empty"), (True, "source_L0")):
            tag, nc = label+":"+arm, (4 if occupied else 1)
            H, terms = dense_terms(p, occupied)
            rows = sparse_rows(p, occupied)
            sparse_action = lambda v: [sum((a*v[c] for c, a in row if a and v[c]), F(0)) for row in rows]
            check(tag+":dimension", len(H), 64 if occupied else 16)
            for key, matrix in dict(terms, total=H).items():
                check(tag+":Hermitian:"+key, max(abs(matrix[i][j]-matrix[j][i]) for i in range(len(H)) for j in range(len(H))))
            for col in range(len(H)):
                basis = [F(int(i == col)) for i in range(len(H))]
                check(tag+":independent_column:"+str(col), max(abs(a-b) for a, b in zip(sparse_action(basis), [r[col] for r in H])))
            vectors = powers(lambda v: matvec(H, v), len(H))
            other = powers(sparse_action, len(H))
            for n in range(ORDER+2):
                check(tag+":independent_power:"+str(n), max(abs(a-b) for a, b in zip(vectors[n], other[n])))
            norm = series(vectors, lambda v: v)
            links = [series(vectors, lambda v, e=e: [a*((i//nc >> e) & 1) for i, a in enumerate(v)]) for e in range(4)]
            carriers = [series(vectors, lambda v, c=c: [a*int(occupied and i % nc == c) for i, a in enumerate(v)]) for c in range(4)]
            energies = {key: series(vectors, lambda v, matrix=matrix: matvec(matrix, v)) for key, matrix in terms.items()}
            energies.update(record_storage=record_energy, writer_copy=copy_energy, writer_storage=zero_series)
            total_energy = combine(*energies.values())
            independent_energy = series(vectors, sparse_action)
            E0 = 4*p["U_d"]*p["d_star"]**2+int(occupied)*p["epsilon_psi"]
            for key, values in dict(norm=norm, total_energy=total_energy, **energies).items(): audit(tag+":"+key, values)
            for e, values in enumerate(links): audit(tag+":edge:"+str(e), values)
            for c, values in enumerate(carriers): audit(tag+":carrier:"+str(c), values)
            for n in range(ORDER+1):
                check(tag+":norm:"+str(n), norm[n][0], F(int(n == 0)))
                check(tag+":complete_energy:"+str(n), total_energy[n][0], E0 if n == 0 else F(0))
                check(tag+":independent_energy:"+str(n), total_energy[n][0], independent_energy[n][0])
                check(tag+":carrier_count:"+str(n), sum(carriers[c][n][0] for c in range(4)), F(int(occupied and n == 0)))
                for a, b in ((0, 1), (2, 3)):
                    check(tag+":edge_reflection:"+str((a, b, n)), links[a][n][0], links[b][n][0])
                check(tag+":carrier_reflection:"+str(n), carriers[2][n][0], carriers[3][n][0])
                if not occupied: check(tag+":empty_edge_symmetry:"+str(n), links[0][n][0], links[2][n][0])
                if p["t"] == 0:
                    for c in range(4): check(tag+":no_hopping_carrier:"+str((c, n)), carriers[c][n][0], F(int(occupied and c == 0 and n == 0)))
            for e in range(4): check(tag+":edge_leading2:"+str(e), links[e][2][0], p["h"]**2)
            internal[arm] = dict(links=links, carriers=carriers, energy=total_energy, H=H)
            arms[arm] = dict(reduced_dimension=len(H), dimension_with_factored_records=16*len(H), initial_complete_energy=str(E0),
                             edges=[pack(v) for v in links], carriers=[pack(v) for v in carriers], norm=pack(norm),
                             complete_energy=pack(total_energy), component_energies={key: pack(v) for key, v in energies.items()})
        contrasts = [combine(internal["source_L0"]["links"][e], scale(internal["empty"]["links"][e], F(-1))) for e in range(4)]
        kappa = p["Delta"]+2*p["U_d"]*(1-2*p["d_star"])
        local4 = -p["h"]**2*(2*kappa*p["j"]+p["j"]**2+p["t"]**2)/12
        for e, values in enumerate(contrasts):
            check(label+":loading_order0:"+str(e), values[0][0])
            check(label+":loading_order2:"+str(e), values[2][0])
            check(label+":loading_order4:"+str(e), values[4][0], local4 if e < 2 else F(0))
            if label == "j_t_off":
                for n in range(ORDER+1): check(label+":full_link_null:"+str((e, n)), values[n][0])
        if label == "j_t_off":
            empty_H, source_H = internal["empty"]["H"], internal["source_L0"]["H"]
            check(label+":exact_tensor_identity_null", max(abs(source_H[i][j]-int(i % 4 == j % 4)*empty_H[i//4][j//4]
                  -int(i == j)*p["epsilon_psi"]) for i in range(64) for j in range(64)))
        energy_difference = combine(internal["source_L0"]["energy"], scale(internal["empty"]["energy"], F(-1)))
        for n in range(ORDER+1): check(label+":source_energy_difference:"+str(n), energy_difference[n][0], p["epsilon_psi"] if n == 0 else F(0))
        output_cases.append(dict(case=label, parameters={key: str(value) for key, value in p.items()}, blank_link_gap=str(kappa),
                                 arms=arms, edge_loading_contrasts=[pack(v) for v in contrasts], complete_energy_difference=pack(energy_difference)))
    check("self_source_unchanged", F(int(hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != source_sha)))
    passed = all(c["passed"] for c in checks)
    output = dict(status="COMPLETE" if passed else "FAILED_IDENTITIES", source_sha256=source_sha, input_sha256={str(BS): BS_SHA},
                  order=ORDER, method="Exact Fraction dense/basis versus independent sparse-edge actions", time_variable="x=tau/hbar",
                  edge_order=EDGES, initial_state="All incidence/record blanks; empty carrier or one fixed-content carrier at L0",
                  clock_premise=dict(lambda_R=0, g_psi_r=0, g_rb=0, epsilon_r=1, g_wr=1, epsilon_w=0,
                                     theta="sqrt(5)*x", even_conversion="coefficient[2m]/5^m",
                                     odd_conversion="coefficient[n]/5^(n/2); all x coefficients retained even on failed checks"),
                  cases=output_cases, checks=checks, check_counts=dict(total=len(checks), passed=sum(c["passed"] for c in checks)),
                  qualifications=dict(nonincident_support_edge_not_physical_distance=True, injected_probe_transport_not_inferred=True,
                                      physical_force=False, binding_energy=False, physical_metric=False, dark_mass_assignment=False,
                                      preparation_apparatus_instantiated=False, finite_time_remainder_bound=False),
                  runtime=dict(wall_seconds=time.perf_counter()-start, max_rss_raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                               max_rss_units="bytes" if sys.platform == "darwin" else "KiB"))
    data = json.dumps(output, separators=(",", ":")).encode()
    fd, temporary = tempfile.mkstemp(prefix="native_remote_loading_series_v001_", suffix=".tmp", dir=HERE)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, target)
    finally:
        os.unlink(temporary)
    result_sha = hashlib.sha256(data).hexdigest()
    if hashlib.sha256(target.read_bytes()).hexdigest() != result_sha:
        raise RuntimeError("Published result hash mismatch")
    summaries = [dict(case=case["case"], parameters=case["parameters"], blank_link_gap=case["blank_link_gap"],
                      edge_loading_contrasts=case["edge_loading_contrasts"],
                      source_carrier_arrivals=case["arms"]["source_L0"]["carriers"]) for case in output_cases]
    print(json.dumps(dict(status=output["status"], path=str(target), sha256=result_sha, bytes=len(data),
                          source_sha256=source_sha, check_counts=output["check_counts"],
                          failures=[c for c in checks if not c["passed"]], cases=summaries,
                          runtime=output["runtime"]), separators=(",", ":")))
    return 0 if passed else 1


if __name__ == "__main__":
    if sys.argv[1:] != ["--run"]:
        raise SystemExit("Explicit --run required; exact coefficients only")
    try:
        code = main()
    except Exception as error:
        print(json.dumps(dict(status="ERROR", error_type=type(error).__name__, error=str(error))))
        code = 1
    raise SystemExit(code)
