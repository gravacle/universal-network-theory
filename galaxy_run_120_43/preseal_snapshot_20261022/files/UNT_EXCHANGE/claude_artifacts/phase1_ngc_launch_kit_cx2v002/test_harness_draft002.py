"""Exclusive synthetic test runner for the draft P112 implementation."""
import argparse
import ast
import hashlib
import json
import os
import subprocess
import traceback
import types
from pathlib import Path


def hash_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def exclusive(path, raw):
    with Path(path).open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
        os.fchmod(f.fileno(), 0o444)
    return {"path": str(path), "sha256": hash_bytes(raw)}


class Suite:
    def __init__(self, tool, root, tool_sha):
        self.tool_path, self.root = Path(tool), Path(root)
        raw = self.tool_path.read_bytes()
        if hash_bytes(raw) != tool_sha:
            raise ValueError("tool pin mismatch")
        self.tool_sha = tool_sha
        self.module = types.ModuleType("_p112_synthetic_review")
        self.module.__file__ = str(self.tool_path)
        exec(compile(raw, str(self.tool_path), "exec"), self.module.__dict__)
        self.root.mkdir()
        self.rows, self.interfaces = [], {}
        self.refusals, self.current_case = {}, "fixture_setup"
        old_init = self.module.Refusal.__init__
        def tracked(error, code, detail=None):
            self.refusals.setdefault(code, set()).add(self.current_case)
            old_init(error, code, detail)
        self.module.Refusal.__init__ = tracked

    def eq(self, left, right):
        if left != right:
            raise AssertionError((left, right))

    def refuses(self, code, action):
        try:
            action()
        except self.module.Refusal as e:
            self.eq(e.code, code)
            return
        raise AssertionError("expected " + code)

    def any_refusal(self, action):
        try:
            action()
        except self.module.Refusal:
            return
        raise AssertionError("expected a refusal")

    def raw_write(self, path, raw):
        return exclusive(path, raw)

    def write_refusal_fixture(self, path, doc):
        report = {"counts": {}, "last_observation": {}, "date_u": self.module.date_u()}
        pin = self.raw_write(str(path) + ".observations.json", self.module.encoded(report))
        doc = dict(doc, rule=doc["rule"] + " observations_sha256=" + pin["sha256"])
        return self.raw_write(path, self.module.encoded(doc))

    def bytes_fixture(self, name, raw):
        path = self.root / name
        return exclusive(path, raw)

    def fixture(self, name, obj):
        return self.bytes_fixture(name, self.module.encoded(obj))

    def case(self, name, action):
        if any(r["name"] == name for r in self.rows):
            raise AssertionError("duplicate test " + name)
        self.current_case = name
        try:
            action()
            self.rows.append({"name": name, "status": "PASS"})
        except Exception as e:
            self.rows.append({"name": name, "status": "FAIL", "detail": repr(e),
                              "trace": traceback.format_exc(limit=5)})
        finally:
            self.current_case = "fixture_setup"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--tool-sha256", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--components", nargs="+", required=True)
    ap.add_argument("--groups", nargs="+", required=True)
    a = ap.parse_args()
    suite = Suite(a.tool, a.out, a.tool_sha256)
    namespace, pins = {}, []
    for source in a.components:
        raw = Path(source).read_bytes()
        pins.append({"path": source, "sha256": hash_bytes(raw)})
        exec(compile(raw, source, "exec"), namespace)
    for group in a.groups:
        namespace[group](suite)
    date = subprocess.check_output(["/bin/date", "-u"], env=dict(os.environ, LC_ALL="C"), text=True).strip()
    record = {"schema": "P112_DRAFT_TEST_RECORD_CX2V001", "date_u": date, "tool_sha256": suite.tool_sha,
              "test_sources": pins, "cases": suite.rows, "interfaces": suite.interfaces}
    record["refusal_coverage"] = {code: sorted(names) for code, names in sorted(suite.refusals.items())}
    codes = set()
    for node in ast.walk(ast.parse(suite.tool_path.read_text())):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            index = 1 if node.func.id == "need" else 0 if node.func.id == "Refusal" else None
            if index is not None and len(node.args) > index:
                for arg in ast.walk(node.args[index]):
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        codes.add(arg.value)
    record["refusal_not_exercised"] = sorted(codes - set(suite.refusals))
    pin = exclusive(suite.root / "TEST_RECORD.json", suite.module.encoded(record))
    failures = [r for r in suite.rows if r["status"] != "PASS"]
    print(json.dumps({"tested": len(suite.rows), "failed": len(failures), "failures": failures, "refusal_missing_count": len(record["refusal_not_exercised"]), "record": pin}))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
