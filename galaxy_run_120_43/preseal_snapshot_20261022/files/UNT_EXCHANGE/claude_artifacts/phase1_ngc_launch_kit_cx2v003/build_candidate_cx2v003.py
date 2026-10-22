"""Exclusive creation of a synthetic test candidate from immutable components."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, text):
    with path.open("x") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    path.chmod(0o444)
    return {"path": str(path), "sha256": sha(path)}

def latest(prefix):
    stems = sorted({f.name.split("_draft")[0] for f in ROOT.glob(prefix + "*_draft*.py")})
    return [sorted(ROOT.glob(stem + "_draft*.py"))[-1] for stem in stems]

label = sys.argv[1]
assert label.isalnum()
parts = latest("source_part_")
tool = ROOT / ("phase1_ngc_launch_cx2v003_" + label + ".py")
source = "\n\n".join(f.read_text() for f in parts)
compile(source, str(tool), "exec")
tool_pin = write(tool, source)
test_parts = latest("test_part_")
harness = sorted(ROOT.glob("test_harness_draft*.py"))[-1]
prefix = harness.read_text().split("\ndef main():", 1)[0]
footer = "\nALL_GROUPS =" + (ROOT / "BASELINE_TEST_PROGRAM_CX2V002.py").read_text().split("\nALL_GROUPS =", 1)[1]
if any(f.name.startswith("test_part_260_") for f in test_parts):
    footer = footer.replace("\ndef main():", '\nALL_GROUPS += ["v003_regression_cases", "v003_mutation_cases"]\n\ndef main():')
tests = prefix + "\n\n" + "\n\n".join(f.read_text() for f in test_parts) + footer
tests = tests.replace("P112_TEST_RECORD_CX2V002", "P112_TEST_RECORD_CX2V003")
tests = tests.replace("P112_TEST_EXECUTION_CX2V002", "P112_TEST_EXECUTION_CX2V003")
test = ROOT / ("test_phase1_ngc_launch_cx2v003_" + label + ".py")
compile(tests, str(test), "exec")
test_pin = write(test, tests)
date_u = subprocess.check_output(["/bin/date", "-u"], env=dict(os.environ, LC_ALL="C"), text=True).strip()
stamp = write(ROOT / ("PREFLIGHT_STAMP_" + label + ".json"), json.dumps({"date_u": date_u}) + "\n")
manifest = {"date_u": date_u, "tool": tool_pin, "tests": test_pin, "stamp": stamp,
            "components": [{"path": str(f), "sha256": sha(f)} for f in parts + [harness] + test_parts]}
write(ROOT / ("CANDIDATE_COMPONENTS_" + label + ".json"), json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"tool": tool_pin, "tests": test_pin, "stamp": stamp,
                  "out": str(ROOT / ("test_records_" + label))}))
