#!/usr/bin/env python3
"""NEW exact first-jet query contraction; root alone executes --execute."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import sys
import time

BASE = Path(__file__).resolve().parent
STEM = "LOCAL_RECORD_FEEDBACK_AUTONOMOUS_BIRTH_QUERY_LEADING_RESPONSE_V001"
PROTOCOL = BASE / (STEM + ".md")
PROTOCOL_SHA = "3a4d29cc904bb5ded9a56fdac6319f4789b8185fd6fe6d7add22edc7ca4d1260"
PINS = {
    "LOCAL_RECORD_FEEDBACK_NATIVE_AUTONOMOUS_BIRTH_QUERY_RANK_V002.md": "c723da48f7fb6e8a418e15ade6d0489d52caac33fa643353e8a302c280548974",
    "LOCAL_RECORD_FEEDBACK_NATIVE_RECORD_DONOR_FORMATION_V001.md": "45b99f9642d9cf757460cb8a65ea1d27f1bbb9eac9b23674b1cf879adeabed4f",
    "LOCAL_RECORD_FEEDBACK_Q4_CONSERVING_FORMATION_CANDIDATE_V001.md": "07323053b75b947b35712f0ac8fc4ce04c2766131cd4e684fd64167321b51f3c",
    "LOCAL_RECORD_FEEDBACK_Q4_CONDITIONAL_NEWSTAR_QUERY_V001.md": "34eb3374dfeb849fb24d85dd305e1a1e791c3b15392bfccd097456626fe92ff3",
    "LOCAL_RECORD_FEEDBACK_PRESENCE_CONDITIONED_MEMORY_SOURCE_JOIN_V001.md": "357ba38e685fc080df036bfc59b608c50e402c7183359a61338188076eceb958",
    "LOCAL_RECORD_FEEDBACK_NATIVE_COUNT_RESOURCE_REFERENCE_AND_PRESENCE_QUOTIENT_V003.md": "1f962738e7a64bf423a338b82a7b2790a20bfff06d67e700c23b73eb40faa199",
    "LOCAL_RECORD_FEEDBACK_NATIVE_RECORD_DONOR_SPARSE_VERIFICATION_V001.md": "9706c0e14a348c701882ff408e94abe2bc452773ef66fbfdd30d135dc92da11d",
    "local_record_feedback_native_record_donor_sparse_verification_v001.py": "85dbd31c4f76d493df2394f44a18320ccdb83f170d67efea0109e15c6d69da55",
}
H = F(1, 5)
W = H * H / 4
NMAT = ((1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1))
CHECKS = []
AUTH = {}


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pack(x):
    if isinstance(x, F):
        return str(x.numerator) if x.denominator == 1 else str(x)
    if isinstance(x, dict):
        return {str(k): pack(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [pack(v) for v in x]
    return x


def write_json(path, data):
    with path.open("x", encoding="utf-8") as f:
        json.dump(pack(data), f, sort_keys=True, indent=2, allow_nan=False)
        f.write("\n")
    path.chmod(0o444)


def exact(name, actual, expected):
    ok = actual == expected
    row = {"name": name, "passed": ok}
    if not ok:
        row.update(actual=pack(actual), expected=pack(expected))
    CHECKS.append(row)


def zeros():
    return [[F(0) for _ in range(6)] for _ in range(6)]


def outer(a, b):
    return [[a[i] * b[j] for j in range(6)] for i in range(6)]


def rank(matrix):
    a = [list(row) for row in matrix]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [x / scale for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                scale = a[i][c]
                a[i] = [x - scale * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def query(target_word):
    zr = [1 - 2 * ((target_word >> i) & 1) for i in range(4)]
    zl = [1 - 2 * ((target_word >> (i + 4)) & 1) for i in range(4)]
    xa = [F(sum(n * z for n, z in zip(row, zr)), 2) for row in NMAT]
    xb = [-F(sum(n * z for n, z in zip(row, zl)), 2) for row in NMAT]
    return xa + xb


def repeated(word):
    return word | (word << 4)


def in_repetition_image(word):
    return (word & 15) == ((word >> 4) & 15)


def transitions(word):
    base = repeated(word)
    out = []
    for label, shift in (("A_right_single", 0), ("B_left_single", 4)):
        for i in range(4):
            out.append((label, i, base ^ (1 << (i + shift))))
    for i in range(4):
        out.append(("encoded_old_pair", i, base ^ (1 << i) ^ (1 << (i + 4))))
    return out


def contraction(base, selected):
    m0 = query(base)
    m2 = [F(0) for _ in range(6)]
    s2 = zeros()
    jump_c2 = zeros()
    saved = []
    for label, port, target in selected:
        x = query(target)
        delta = [a - b for a, b in zip(x, m0)]
        for i in range(6):
            m2[i] += W * delta[i]
            for j in range(6):
                s2[i][j] += W * (x[i] * x[j] - m0[i] * m0[j])
                jump_c2[i][j] += W * delta[i] * delta[j]
        saved.append({"class": label, "port": port, "target_word": target,
                      "query": x, "delta_query": delta,
                      "amplitude_coefficient_i_tau": H / 2,
                      "probability_coefficient_tau2": W,
                      "repetition_image": in_repetition_image(target)})
    c2 = [[s2[i][j] - m2[i] * m0[j] - m0[i] * m2[j]
           for j in range(6)] for i in range(6)]
    return {"mean0": m0, "mean_tau2": m2, "second_moment_tau2": s2,
            "centered_covariance_tau2": c2, "jump_covariance_tau2": jump_c2,
            "rank": rank(c2), "transitions": saved}


def expected_matrix(full):
    diagonal = 2 if full else 1
    return [[H * H * (diagonal if i == j else -1 if i % 3 == j % 3 else 0)
             for j in range(6)] for i in range(6)]


def check_modes(name, matrix, full):
    for axis in range(3):
        for sign, label in ((1, "common"), (-1, "difference")):
            v = [F(0)] * 6
            v[axis], v[axis + 3] = F(1), F(sign)
            eig = H * H * ((1 if sign == 1 else 3) if full else (0 if sign == 1 else 2))
            actual = [sum(matrix[i][j] * v[j] for j in range(6)) for i in range(6)]
            exact(name + "_" + label + "_" + str(axis), actual, [eig * x for x in v])


def compute_rows():
    exact("tetra_row_gram", [[sum(NMAT[i][k] * NMAT[j][k] for k in range(4))
                              for j in range(3)] for i in range(3)],
          [[4 if i == j else 0 for j in range(3)] for i in range(3)])
    exact("tetra_column_sum", [sum(row) for row in NMAT], [0, 0, 0])
    rows = []
    for word in range(16):
        base = repeated(word)
        tx = transitions(word)
        label = "word_" + str(word)
        exact(label + "_base_image", in_repetition_image(base), True)
        exact(label + "_transition_census", len(tx), 12)
        exact(label + "_distinct_transitions", len({x[2] for x in tx}), 12)
        exact(label + "_no_base_transition", base in {x[2] for x in tx}, False)
        image_tx = [x for x in tx if in_repetition_image(x[2])]
        exact(label + "_image_census", len(image_tx), 4)
        exact(label + "_image_classes", [x[0] for x in image_tx], ["encoded_old_pair"] * 4)
        full, image = contraction(base, tx), contraction(base, image_tx)
        for name, value, flag in (("full", full, True), ("image", image, False)):
            c2 = value["centered_covariance_tau2"]
            exact(label + "_" + name + "_two_routes", c2, value["jump_covariance_tau2"])
            exact(label + "_" + name + "_matrix", c2, expected_matrix(flag))
            exact(label + "_" + name + "_rank", value["rank"], 6 if flag else 3)
            factor = -H * H if flag else -H * H / 2
            exact(label + "_" + name + "_mean", value["mean_tau2"],
                  [factor * x for x in value["mean0"]])
            exact(label + "_" + name + "_symmetry", c2, list(map(list, zip(*c2))))
            check_modes(label + "_" + name, c2, flag)
        m0 = full["mean0"]
        dyad = outer(m0, m0)
        exact(label + "_padded_dyad_rank", rank(dyad), 1 if any(m0) else 0)
        unchanged_delta = [x - x for x in m0]
        exact(label + "_unchanged_query_contribution", outer(unchanged_delta, unchanged_delta), zeros())
        rows.append({"word": word, "word_bits_msb_to_lsb": format(word, "04b"),
                     "donor_q": 0, "eligible": False, "conditional": None,
                     "status": "NO_BIRTH_CONDITIONAL_UNDEFINED", "new_presence": "0",
                     "raw_pG": None, "physical_metric_qualified": False})
        rows.append({"word": word, "word_bits_msb_to_lsb": format(word, "04b"),
                     "donor_q": 1, "eligible": True, "status": "LEADING_CONDITIONAL_COEFFICIENT",
                     "conditional_requires": "epsilon != 0 and sufficiently small nonzero time",
                     "conditional": {"full": full, "reverse_image": image},
                     "p_new": "epsilon^2*tau^2+O(tau^4)",
                     "raw_pG": {"symbolic_factor": "epsilon^2*tau^4",
                                "matrix_factor": full["centered_covariance_tau2"],
                                "remainder": "O(tau^6)"},
                     "padded_covariance_tau2": {"symbolic_factor": "epsilon^2",
                                                 "dyad_matrix_factor": dyad, "rank": rank(dyad)},
                     "padded_covariance_tau4_complete": "NOT_COMPUTED",
                     "physical_metric_qualified": False, "field_rank_qualified": False})
    exact("all_word_donor_rows", [(r["word"], r["donor_q"]) for r in rows],
          [(w, q) for w in range(16) for q in (0, 1)])
    exact("eligible_refused_census", [sum(r["eligible"] for r in rows), sum(not r["eligible"] for r in rows)], [16, 16])
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        parser.error("root-owned execution requires --execute; static review must not import this source")
    paths = {k: BASE / (STEM + "." + suffix) for k, suffix in
             (("result", "RESULT.json"), ("report", "RESULT.md"),
              ("receipt", "RECEIPT.json"), ("error", "ERROR.json"))}
    if any(p.exists() for p in paths.values()):
        raise RuntimeError("exclusive outputs already exist; no overwrite or resume")
    start, started = time.perf_counter(), utc()
    try:
        for name, pin in {**PINS, PROTOCOL.name: PROTOCOL_SHA}.items():
            actual = sha(BASE / name)
            if actual != pin:
                raise RuntimeError("input seal mismatch: " + name)
            AUTH[name] = actual
        AUTH[Path(__file__).name] = sha(Path(__file__))
        rows = compute_rows()
        failed = sum(not c["passed"] for c in CHECKS)
        status = "COMPLETE_EXACT_LEADING_QUERY_CHECKS_PASSED" if not failed else "ARITHMETIC_FAILED"
        result = {"status": status, "PID": os.getpid(), "started_UTC": started,
                  "input_sha256": dict(AUTH), "native_h": H, "rows": rows,
                  "census": {"rows": 32, "words": 16, "eligible": 16, "refused": 16},
                  "checks": CHECKS, "check_count": len(CHECKS), "failed": failed,
                  "units": {"tau": "Eunit*t_proper/hbar", "epsilon": "epsilon_physical/Eunit",
                            "h_physical": "Eunit/5", "Eunit": "SYMBOLIC_UNSELECTED",
                            "epsilon_physical": "SYMBOLIC_UNSELECTED"},
                  "scope": {"new_H_application": False, "producer_import": False,
                            "numerical_propagation": False, "physical_metric_qualification": False,
                            "cosmic_duration": False, "closed_transition_orbit": False}}
        write_json(paths["result"], result)
        lines = ["# Autonomous birth-query leading coefficient result V001", "", status, "",
                 "All sixteen cut words and both donor occupancies retained. Fractions are exact.", "",
                 "| Word | Initial A mean | Full leading rank | Image leading rank | Padded tau2 rank |",
                 "|---|---|---|---|---|"]
        for row in rows:
            if row["eligible"]:
                c = row["conditional"]
                lines.append("| " + str(row["word"]) + " | " + str(pack(c["full"]["mean0"][:3]))
                             + " | " + str(c["full"]["rank"]) + " | " + str(c["reverse_image"]["rank"])
                             + " | " + str(row["padded_covariance_tau2"]["rank"]) + " |")
        lines += ["", "Blank-donor conditional refusals: all words0 through15; epsilon=0 also has no birth.", "",
                  "Full leading eigenvalue factors: h^2 (three),3h^2 (three). Image: zero (three),2h^2 (three).",
                  "Raw pG starts epsilon^2*tau^4; padded tau2 dyad is separate. No physical metric or field rank is qualified.",
                  "No time, Eunit or physical epsilon selected; the complete padded tau4 coefficient is not computed.", "",
                  "Exact checks: " + str(len(CHECKS)) + "; failed: " + str(failed) + "."]
        with paths["report"].open("x", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        paths["report"].chmod(0o444)
        for name, pin in AUTH.items():
            if sha(BASE / name) != pin:
                raise RuntimeError("post-output input changed: " + name)
        write_json(paths["receipt"], {"status": status, "PID": os.getpid(),
                   "started_UTC": started, "closed_UTC": utc(),
                   "elapsed_seconds": time.perf_counter() - start, "input_sha256": dict(AUTH),
                   "result_sha256": sha(paths["result"]), "report_sha256": sha(paths["report"]),
                   "check_count": len(CHECKS), "failed": failed})
        print(json.dumps({"status": status, "rows": len(rows), "checks": len(CHECKS), "failed": failed}))
        return 3 if failed else 0
    except Exception as error:
        prefix = {k: sha(p) for k, p in paths.items() if k != "error" and p.exists()}
        write_json(paths["error"], {"status": "EXECUTION_ERROR_PRESERVED", "PID": os.getpid(),
                   "started_UTC": started, "closed_UTC": utc(), "input_sha256": dict(AUTH),
                   "exception_type": type(error).__name__, "exception": str(error),
                   "check_count": len(CHECKS), "checks": CHECKS, "actual_prefix_sha256": prefix})
        raise


if __name__ == "__main__":
    sys.exit(main())
