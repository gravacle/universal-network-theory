"""Read-only verification followed by one new immutable verification receipt."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}


manifest = ROOT / "HASHES_CX2V003.txt"
lines = manifest.read_text().splitlines()
assert lines and len(lines) == len(set(lines))
for line in lines:
    digest, path = line.split("  ", 1)
    assert sha(Path(path).read_bytes()) == digest, path
readme = ROOT / "README_PHASE1_NGC_LAUNCH_CX2V003.md"
contract = ROOT / "README_CONTRACT_CX2V003.md"
assert contract.read_bytes() in readme.read_bytes()
r1 = ROOT / "test_records_cx2v003/RUN1/TEST_RECORD.json"
r2 = ROOT / "test_records_cx2v003/RUN2/TEST_RECORD.json"
assert r1.read_bytes() == r2.read_bytes()
record = json.loads(r1.read_bytes())
assert len(record["cases"]) == 681 and all(r["status"] == "PASS" for r in record["cases"])
assert sum("MUTANT_" in r["name"] for r in record["cases"]) == 78
assert not record["refusal_not_exercised"]
assert not record["interfaces"]["all_public_command_read_audit"]["violations"]
for filename in ("phase1_ngc_launch_cx2v003.py", "test_phase1_ngc_launch_cx2v003.py"):
    path = ROOT / filename
    compile(path.read_bytes(), str(path), "exec")
date_u = subprocess.check_output(["/bin/date", "-u"], env=dict(os.environ, LC_ALL="C"), text=True).strip()
receipt = {
    "schema": "P112_ARTIFACT_VERIFICATION_CX2V003", "date_u": date_u, "status": "TESTED_PASS",
    "manifest": pin(manifest), "manifest_entries_verified": len(lines), "readme": pin(readme),
    "documentation_contract": pin(contract), "readme_contains_exact_contract": True,
    "test_records": [pin(r1), pin(r2)], "byte_identical": True, "passing_per_run": 681,
    "mutants_killed_per_run": 78, "named_refusal_coverage_complete": True, "audit_violations": [],
    "verifier": pin(Path(__file__).resolve()),
    "limits": "Artifact and synthetic test verification only; no scientific launch or production acceptance.",
}
path = ROOT / "ARTIFACT_VERIFICATION_CX2V003.json"
raw = (json.dumps(receipt, sort_keys=True, indent=1) + "\n").encode()
with path.open("xb") as f:
    f.write(raw)
    f.flush()
    os.fsync(f.fileno())
    os.fchmod(f.fileno(), 0o444)
print(json.dumps({"verified": len(lines), "receipt": pin(path)}))
