"""Rehome the preserved Codex2 partial; keep the adopted assembler byte pin."""
from pathlib import Path
import ast
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
OLD = HERE.with_name("direct_cert_lookup_cx2")
pins = {}


def read(name):
    p = OLD / name
    b = p.read_bytes()
    pins[name] = {"path": str(p), "sha256": hashlib.sha256(b).hexdigest()}
    return b.decode()


def put(name, value):
    p = HERE / name
    with p.open("x", encoding="utf-8") as f:
        f.write(value)
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def replace_once(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new)


lookup_old = read("direct_cert_lookup_cx2v002.py")
lookup = replace_once(
    lookup_old, "str(HERE/'cp1_points_assembler_cx2v002.py')",
    "str(ART/'direct_cert_lookup_cx2/cp1_points_assembler_cx2v002.py')",
)
lp = put("direct_cert_lookup_cx3v001.py", lookup)
adapter_old = read("direct_preflight_cert_cx2v002.py")
old_lookup_pin = repr(pins["direct_cert_lookup_cx2v002.py"])
assert old_lookup_pin in adapter_old
adapter = replace_once(adapter_old, old_lookup_pin, repr(lp))
ap = put("direct_preflight_cert_cx3v001.py", adapter)
products = {"lookup": lp, "adapter": ap}

renames = {
    "direct_lookup_fixture_cx2v003.py": "direct_lookup_fixture_cx3v001.py",
    "direct_lookup_cases_prefix_cx2v003.py": "direct_lookup_cases_prefix_cx3v001.py",
    "test_direct_lookup_cx2v003.py": "test_direct_lookup_cx3v001.py",
    "audit_direct_snapshot_cx2v001.py": "audit_direct_snapshot_cx3v001.py",
}
for old, new in renames.items():
    s = read(old)
    for before, after in {
        **renames,
        "direct_cert_lookup_cx2v002.py": "direct_cert_lookup_cx3v001.py",
        "direct_preflight_cert_cx2v002.py": "direct_preflight_cert_cx3v001.py",
        "DIRECT_LOOKUP_TESTS_CX2V003": "DIRECT_LOOKUP_TESTS_CX3V001",
        "SNAPSHOT_AUDIT_CX2V001": "SNAPSHOT_AUDIT_CX3V001",
        "HERE/'cp1_points_assembler_cx2v002.py'": "ART/'direct_cert_lookup_cx2/cp1_points_assembler_cx2v002.py'",
    }.items():
        s = s.replace(before, after)
    products[new] = put(new, s)

# Rehoming changes only the two exact pin/path assignments in implementation.
def without_assignment(source, name):
    tree = ast.parse(source)
    tree.body = [n for n in tree.body if not (
        isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)
    )]
    return ast.dump(tree, include_attributes=False)

assert without_assignment(lookup, "ASSEMBLER") == without_assignment(lookup_old, "ASSEMBLER")
assert without_assignment(adapter, "LOOKUP") == without_assignment(adapter_old, "LOOKUP")
record = {
    "schema": "DIRECT_LOOKUP_REHOME_CX3V001",
    "date_u": subprocess.check_output(["/bin/date", "-u"], text=True).strip(),
    "status": "TESTED",
    "implementation_delta": [
        "Lookup ASSEMBLER points to the existing adopted cx2v002 bytes at their original absolute path.",
        "Adapter LOOKUP pins the rehomed Codex3 lookup bytes.",
        "All other implementation AST is unchanged from the preserved Codex2 candidate.",
        "HERE now restricts exclusive output directories to direct_cert_lookup_cx3.",
    ],
    "inputs": pins, "outputs": products,
}
print(json.dumps(put("BUILD_SUCCESSORS_CX3V001.json", json.dumps(record, indent=2, sort_keys=True) + "\n")))
