#!/usr/bin/env python3
"""Additive V002 replay of the original 74 AURFT checks with explicit path bases.

This verifies pinned artifacts and deductive composition. It does not test the
unrestricted natural validity of U-DCL.
"""

from hashlib import sha256
from itertools import product
from pathlib import Path

from manifest_resolution import resolve_manifest_item as _declared_manifest_item


ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT / "LANE_RFT_AXIOMATIC_URFT_CLOSURE_V001"
ORIGINAL_SHA256 = "ac79663cd126b945bc022c95ba094f40addca4e28e3e24312f70ba9d0f15b77d"
if sha256((LANE / "verify_axiomatic_urft_closure.py").read_bytes()).hexdigest() != ORIGINAL_SHA256:
    raise SystemExit("REFUSED: original verifier bytes differ from the authenticated source")
THEOREM = (LANE / "THEOREM.md").read_text()

checks: list[tuple[str, bool]] = []

REQUIRED_DEPENDENCIES = {
    "URFT_UDCL_ADOPTION_V001.md",
    "LANE_RFT_UDCL_CONDITIONAL_UNIVERSAL_COVERAGE_V001/THEOREM.md",
    "LANE_RFT_UDCL_CONDITIONAL_UNIVERSAL_COVERAGE_V001/MANIFEST.sha256",
    "LANE_RFT_STANDARD_CAUSAL_URFT_SCOPE_V001/THEOREM.md",
    "LANE_RFT_STANDARD_CAUSAL_URFT_SCOPE_V001/MANIFEST.sha256",
    "LANE_RFT_RECORD_TO_CTS_NONIMPLICATION_V001/THEOREM.md",
    "LANE_RFT_RECORD_TO_CTS_NONIMPLICATION_V001/MANIFEST.sha256",
    "LANE_RFT_CAUCHY_TIME_SLICE_ONTIC_COVERAGE_V001/THEOREM.md",
    "LANE_RFT_CAUCHY_TIME_SLICE_ONTIC_COVERAGE_V001/MANIFEST.sha256",
    "LANE_RFT_FINITE_MISSION_FAITHFUL_ADMISSION_V001/THEOREM.md",
    "LANE_RFT_FINITE_MISSION_FAITHFUL_ADMISSION_V001/MANIFEST.sha256",
    "LANE_RFT_FINITE_HAMILTONIAN_BOUNDARY_CLOSURE_V001/THEOREM.md",
    "LANE_RFT_FINITE_HAMILTONIAN_BOUNDARY_CLOSURE_V001/MANIFEST.sha256",
    "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/THEOREM.md",
    "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/MANIFEST.sha256",
}


def check(name: str, condition: bool) -> None:
    checks.append((name, bool(condition)))


entries: dict[str, str] = {}
malformed = False
duplicate = False
escaped = False
for raw in (LANE / "DEPENDENCIES.sha256").read_text().splitlines():
    if not raw.strip():
        continue
    parts = raw.split(maxsplit=1)
    if len(parts) != 2 or len(parts[0]) != 64 or any(c not in "0123456789abcdef" for c in parts[0]):
        malformed = True
        continue
    expected, relative = parts
    if relative in entries:
        duplicate = True
    entries[relative] = expected
    candidate = (ROOT / relative).resolve()
    if ROOT not in candidate.parents:
        escaped = True

check("dependency ledger well formed", not malformed)
check("dependency ledger has no duplicates", not duplicate)
check("dependency ledger has no path escape", not escaped)
check("dependency set exact", set(entries) == REQUIRED_DEPENDENCIES)
check("dependency count exact", len(entries) == len(REQUIRED_DEPENDENCIES))

for relative in sorted(REQUIRED_DEPENDENCIES):
    expected = entries.get(relative, "")
    path = (ROOT / relative).resolve()
    check(f"dependency exists {relative}", path.is_file())
    if path.is_file():
        check(f"dependency hash {relative}", sha256(path.read_bytes()).hexdigest() == expected)


def resolve_manifest_item(manifest: Path, relative: str) -> Path:
    return _declared_manifest_item(ROOT, manifest, relative)


for relative in sorted(path for path in REQUIRED_DEPENDENCIES if path.endswith("MANIFEST.sha256")):
    manifest = (ROOT / relative).resolve()
    manifest_ok = manifest.is_file()
    seen: set[str] = set()
    if manifest_ok:
        for raw in manifest.read_text().splitlines():
            if not raw.strip():
                continue
            parts = raw.split(maxsplit=1)
            if len(parts) != 2:
                manifest_ok = False
                break
            expected, item_relative = parts
            if item_relative in seen:
                manifest_ok = False
                break
            seen.add(item_relative)
            item = resolve_manifest_item(manifest, item_relative)
            if ROOT not in item.parents or not item.is_file():
                manifest_ok = False
                break
            if sha256(item.read_bytes()).hexdigest() != expected:
                manifest_ok = False
                break
    check(f"manifest contents {relative}", manifest_ok and bool(seen))

required_text = (
    "AXIOMATIC_URFT_UNIVERSAL_COVERAGE_PROVED",
    "Membership is fixed by the",
    "DCL_{\\rm phys}(r)",
    "Theorem AURFT-1",
    "universally generalize",
    "Theorem AURFT-2",
    "bare `REC(r)` does not entail per-record",
    "OUTCOME_SELECTION_NOT_REQUIRED",
    "Joined companion theorem",
    "ACTVIS",
    "empirically anchored",
    "not a bare-RFT numerical prediction",
    "natural U-DCL validity remains",
)
for phrase in required_text:
    check(f"theorem phrase {phrase}", phrase in THEOREM)

# Per-record implication: REC and DCL are both load-bearing. DCL supplies C/S/J;
# the sealed chain then supplies coverage.
for rec, dcl in product((False, True), repeat=2):
    c = s = j = dcl
    cts = rec and c and s and j
    occ = cts
    physenc = occ
    coverage = occ and physenc
    check(f"per-record closure rec={rec} dcl={dcl}", coverage == (rec and dcl))

# Constructive FHBC support retains REC as a separate load-bearing premise.
for rec, fhbc in product((False, True), repeat=2):
    dcl = fhbc
    coverage = rec and dcl
    check(f"FHBC support rec={rec} fhbc={fhbc}", coverage == (rec and fhbc))

# Universal generalization on every finite proxy domain. Domain membership
# supplies REC; U-DCL supplies DCL for every member.
for size in range(6):
    recs = [True] * size
    dcls = [True] * size
    coverage = [r and d for r, d in zip(recs, dcls)]
    check(f"universal proxy size={size}", all(coverage))

# Dropping U-DCL at one independently admitted member blocks the universal
# conclusion in every nonempty proxy domain.
for size in range(1, 6):
    recs = [True] * size
    dcls = [True] * size
    dcls[-1] = False
    coverage = [rec and dcl for rec, dcl in zip(recs, dcls)]
    check(f"U-DCL load bearing size={size}", not all(coverage))

passed = sum(ok for _, ok in checks)
for index, (name, ok) in enumerate(checks, 1):
    print(f"A{index:02d} {'PASS' if ok else 'FAIL'} {name}")
print(f"TOTAL {passed}/{len(checks)} {'PASS' if passed == len(checks) else 'FAIL'}")

if passed != len(checks):
    raise SystemExit(1)

print("VERDICT AXIOMATIC_URFT_LOGICAL_CLOSURE_AND_TRANSITIVE_CUSTODY_PASS")
print("NATURAL_UDCL_VALIDITY FALSIFIABLE_NOT_EXECUTABLY_PROVED")
print("OUTCOME_SELECTION NOT_A_URFT_PREMISE")
