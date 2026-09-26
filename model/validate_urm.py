"""VALIDATE THE T-54 URM FAMILY LAYERS, THEN THE EXISTING GEOMETRY/PROJECT STACK.

The four family blocks remain independently countable and keep their sealed-lane
semantics: ARROW 27, COUNTLAW 40, CLASSES 52, WRITING 57 (176 gates total).  The
chain then runs validate_geometry.py, which in turn runs validate_project.py and its
D-25 construction/anchor gates, followed by the separate 44-check world-observation
input contract, the separate 38-check generic formation-input contract, and the
separate 48-check origin-neutral gamma-flow contract.  The first two input contracts
and the gamma-flow synthetic fixture carry zero scientific weight.  The chain then
runs the 82-check public-data proof frontier, whose blocker and nonauthoritative
input/theory states never authorize scientific readiness or proof.  Exit code is zero
only when every family gate, the declared gate counts, geometry/project validation,
all four independent data/frontier contracts, the zero-input U-DCL adoption/theorem
certificate, the zero-input historywise-gravity formal discriminant, the bounded
Gravity Formation Theory custody/ceiling gate, and the additive sealed microscopic-
progress checkpoint pass, and the finite relational-accumulation custody/status
gate pass, the separately reported owner-once L10/L12 witness diagnostic
authenticates, and the physical-alpha ALLOW/REQUIRE/SELECT custody gate passes. A
failed signed-persistence prediction is a valid diagnostic outcome and does not
fail the URM; the validator checks that it is reported exactly and grants it no
Gate, RGRL/WTC, alpha, geometry, or gravity weight. The
final Universal Network Theory gate pins the master theorem and checks the exact
typed composition of U-DCL coverage, the governing-domain alpha requirement, finite ARGER
classification, conditional dynamical z=1, and conditional RGRL/WTC response.
It does not promote the finite L4--L12 result into a direct Einstein-equation
derivation.
The alpha gateway certifies a non-singleton finite construction interval and the
conditional governing-domain alpha requirement for every ACTVIS record after domain
ancestry and the domain value are independently established; domain/value selection,
parameter-free 1/137, and every gravity claim remain open.  The U-DCL gateway certifies a
program postulate and conditional theorem, not natural validity; the GFT gateway
certifies the adopted working-theory closure and off-shell/on-shell response
clarification, not empirical RGRL confirmation.  The microscopic checkpoint preserves
the V014 meaning and does not promote a quasi-local envelope or finite-mission
collar to gravity or G.
The relational checkpoint certifies the adopted finite/discrete ARGER Gate
Gravity Formation z=1 result at L4--L12, keeps exact/asymptotic dynamical z=1
separately typed, and records L14 as
INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT.

Use --no-chain to run only the four T-54 family blocks.
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from checks_arrow import run_arrow_checks
from checks_countlaw import run_countlaw_checks
from checks_classes import run_classes_checks
from checks_writing import run_writing_checks


n_pass = 0
n_fail = 0


def check(name, cond, detail=""):
    global n_pass, n_fail
    if cond:
        n_pass += 1
        print(f"  PASS  {name}  {detail}")
    else:
        n_fail += 1
        print(f"  FAIL  {name}  {detail}")


FAMILIES = (
    ("ARROW", 27, run_arrow_checks),
    ("COUNTLAW", 40, run_countlaw_checks),
    ("CLASSES", 52, run_classes_checks),
    ("WRITING", 57, run_writing_checks),
)

print("VALIDATE THE T-54 URM FAMILY LAYERS")
print("=" * 78)
t0 = time.time()
count_shape_ok = True
family_rows = []
for label, expected, runner in FAMILIES:
    print()
    print(f"{label}: expected {expected} gates")
    print("-" * 78)
    p0, f0 = n_pass, n_fail
    tf = time.time()
    runner(check)
    passed, failed = n_pass - p0, n_fail - f0
    observed = passed + failed
    shape_ok = observed == expected
    count_shape_ok &= shape_ok
    family_rows.append((label, passed, failed, observed, expected, time.time() - tf))
    print(f"  {label}: {passed} PASS, {failed} FAIL; gates {observed}/{expected} "
          f"({'COUNT OK' if shape_ok else 'COUNT MISMATCH'}; {time.time() - tf:.1f} s)")

print()
print("=" * 78)
print(f"  T-54 FAMILIES: {n_pass} PASS, {n_fail} FAIL; "
      f"gates {n_pass + n_fail}/176 ({'COUNT OK' if count_shape_ok else 'COUNT MISMATCH'})")

geometry_ok = True
world_input_ok = True
formation_input_ok = True
gamma_flow_ok = True
proof_frontier_ok = True
udcl_postulate_ok = True
historywise_gravity_ok = True
gravity_formation_theory_ok = True
gravity_microscopic_progress_ok = True
relational_accumulation_ok = True
owner_once_joint_witness_ok = True
lineage_order_curvature_ok = True
owner_once_autonomous_continuation_ok = True
alpha_role_ok = True
universal_network_theory_ok = True
if "--no-chain" not in sys.argv:
    print()
    print("CHAIN: validate_geometry.py (which chains the 24-gate project/D-25 validator)")
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run([sys.executable, os.path.join(HERE, "validate_geometry.py")],
                            cwd=HERE)
    geometry_ok = result.returncode == 0
    print("-" * 78)
    print(f"  CHAIN validate_geometry.py: {'PASS' if geometry_ok else 'FAIL'}")
    print()
    print("CHAIN: validate_world_observation.py (44 input checks; zero scientific weight)")
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_world_observation.py")], cwd=HERE
    )
    world_input_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_world_observation.py: "
        + ("PASS" if world_input_ok else "FAIL")
    )
    print()
    print("CHAIN: validate_formation_input.py (38 input checks; zero scientific weight)")
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_formation_input.py")], cwd=HERE
    )
    formation_input_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_formation_input.py: "
        + ("PASS" if formation_input_ok else "FAIL")
    )
    print()
    print("CHAIN: validate_gamma_flow.py (48 checks; synthetic proof weight zero)")
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_gamma_flow.py")], cwd=HERE
    )
    gamma_flow_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_gamma_flow.py: "
        + ("PASS" if gamma_flow_ok else "FAIL")
    )
    print()
    print("CHAIN: validate_proof_frontier.py (82 checks; missing data typed, proof output zero)")
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_proof_frontier.py")], cwd=HERE
    )
    proof_frontier_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_proof_frontier.py: "
        + ("PASS" if proof_frontier_ok else "FAIL")
    )
    print()
    print(
        "CHAIN: validate_udcl_postulate.py "
        "(adopted working postulate and conditional theorem; natural validity open)"
    )
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_udcl_postulate.py")],
        cwd=HERE,
    )
    udcl_postulate_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_udcl_postulate.py: "
        + ("PASS" if udcl_postulate_ok else "FAIL")
    )
    print()
    print(
        "CHAIN: validate_historywise_gravity_discriminant.py "
        "(formal finite-group discriminant; zero physical or empirical proof weight)"
    )
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [
            sys.executable,
            os.path.join(HERE, "validate_historywise_gravity_discriminant.py"),
        ],
        cwd=HERE,
    )
    historywise_gravity_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_historywise_gravity_discriminant.py: "
        + ("PASS" if historywise_gravity_ok else "FAIL")
    )
    print()
    print(
        "CHAIN: validate_gravity_formation_theory.py "
        "(adopted closure/response clarification; empirical RGRL and numerical-G derivation open)"
    )
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_gravity_formation_theory.py")],
        cwd=HERE,
    )
    gravity_formation_theory_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_gravity_formation_theory.py: "
        + ("PASS" if gravity_formation_theory_ok else "FAIL")
    )
    print()
    print(
        "CHAIN: validate_gravity_microscopic_progress.py "
        "(sealed GL6T--GL6CS progress; the GL6CH--GL6CS extension supplies the exact order-six record-dependent writer, rank-six source/read/writer access, stationary response, same-state moment tests, the direct Ward classifier with its unique Einstein ray, and the fixed-cell accumulation horizon; it does not derive the physical F3 Ward identity, gravity, or G)"
    )
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_gravity_microscopic_progress.py")],
        cwd=HERE,
    )
    gravity_microscopic_progress_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_gravity_microscopic_progress.py: "
        + ("PASS" if gravity_microscopic_progress_ok else "FAIL")
    )
    print()
    print(
        "CHAIN: validate_relational_accumulation.py "
        "(adopted finite ARGER Gate; optional history separate; "
        "L14 closed incomplete)"
    )
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_relational_accumulation.py")],
        cwd=HERE,
    )
    relational_accumulation_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_relational_accumulation.py: "
        + ("PASS" if relational_accumulation_ok else "FAIL")
    )
    print()
    print(
        "CHAIN: validate_owner_once_joint_witness.py "
        "(finite L10/L12 association diagnostic; signed persistence failure; non-load-bearing)"
    )
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_owner_once_joint_witness.py")],
        cwd=HERE,
    )
    owner_once_joint_witness_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_owner_once_joint_witness.py: "
        + ("PASS" if owner_once_joint_witness_ok else "FAIL")
    )
    print()
    print(
        "CHAIN: validate_lineage_order_curvature.py "
        "(frozen L8 formation-order Ollivier--Ricci controlled null; non-load-bearing)"
    )
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_lineage_order_curvature.py")],
        cwd=HERE,
    )
    lineage_order_curvature_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_lineage_order_curvature.py: "
        + ("PASS" if lineage_order_curvature_ok else "FAIL")
    )
    print()
    print(
        "CHAIN: validate_owner_once_autonomous_continuation.py "
        "(independently reproduced fixed L4 revisit mechanism; non-load-bearing)"
    )
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [
            sys.executable,
            os.path.join(HERE, "validate_owner_once_autonomous_continuation.py"),
        ],
        cwd=HERE,
    )
    owner_once_autonomous_continuation_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_owner_once_autonomous_continuation.py: "
        + ("PASS" if owner_once_autonomous_continuation_ok else "FAIL")
    )
    print()
    print(
        "CHAIN: validate_alpha_role.py "
        "(construction ALLOW exact; governing-domain REQUIRE conditional; SELECT open)"
    )
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_alpha_role.py")],
        cwd=HERE,
    )
    alpha_role_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_alpha_role.py: "
        + ("PASS" if alpha_role_ok else "FAIL")
    )
    print()
    print(
        "CHAIN: validate_universal_network_theory.py "
        "(master typed composition; finite ARGER and conditional RGRL/WTC remain separate)"
    )
    print("-" * 78)
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "validate_universal_network_theory.py")],
        cwd=HERE,
    )
    universal_network_theory_ok = result.returncode == 0
    print("-" * 78)
    print(
        "  CHAIN validate_universal_network_theory.py: "
        + ("PASS" if universal_network_theory_ok else "FAIL")
    )

print("=" * 78)
overall = (
    n_fail == 0
    and count_shape_ok
    and geometry_ok
    and world_input_ok
    and formation_input_ok
    and gamma_flow_ok
    and proof_frontier_ok
    and udcl_postulate_ok
    and historywise_gravity_ok
    and gravity_formation_theory_ok
    and gravity_microscopic_progress_ok
    and relational_accumulation_ok
    and owner_once_joint_witness_ok
    and lineage_order_curvature_ok
    and owner_once_autonomous_continuation_ok
    and alpha_role_ok
    and universal_network_theory_ok
)
print(f"  URM OVERALL: {'PASS' if overall else 'FAIL'} "
      f"(families {n_pass}/{n_pass + n_fail}, "
      f"counts {'ok' if count_shape_ok else 'MISMATCH'}"
      + ("" if "--no-chain" in sys.argv else
         f", model chain {'ok' if geometry_ok else 'FAILED'}, "
         f"world input {'ok' if world_input_ok else 'FAILED'}, "
         f"formation input {'ok' if formation_input_ok else 'FAILED'}, "
         f"gamma flow {'ok' if gamma_flow_ok else 'FAILED'}, "
         f"proof frontier {'ok' if proof_frontier_ok else 'FAILED'}, "
         f"U-DCL adoption/theorem {'ok' if udcl_postulate_ok else 'FAILED'}, "
         f"historywise-gravity formal discriminant "
         f"{'ok' if historywise_gravity_ok else 'FAILED'}, "
         f"Gravity Formation Theory "
         f"{'ok' if gravity_formation_theory_ok else 'FAILED'}, "
         f"microscopic progress "
         f"{'ok' if gravity_microscopic_progress_ok else 'FAILED'}, "
         f"relational accumulation "
         f"{'ok' if relational_accumulation_ok else 'FAILED'}, "
         f"owner-once joint witness diagnostic "
         f"{'ok' if owner_once_joint_witness_ok else 'FAILED'}, "
         f"lineage-order curvature diagnostic "
         f"{'ok' if lineage_order_curvature_ok else 'FAILED'}, "
         f"L4 autonomous continuation diagnostic "
         f"{'ok' if owner_once_autonomous_continuation_ok else 'FAILED'}, "
         f"alpha role {'ok' if alpha_role_ok else 'FAILED'}, "
         f"Universal Network Theory closure "
         f"{'ok' if universal_network_theory_ok else 'FAILED'}")
      + f"; {time.time() - t0:.1f} s)")
sys.exit(0 if overall else 1)
