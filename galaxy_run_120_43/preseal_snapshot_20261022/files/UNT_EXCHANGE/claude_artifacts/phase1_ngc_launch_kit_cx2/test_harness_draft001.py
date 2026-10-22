"""Exclusive synthetic test runner for the draft P112 implementation."""
import argparse
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

    def bytes_fixture(self, name, raw):
        path = self.root / name
        return exclusive(path, raw)

    def fixture(self, name, obj):
        return self.bytes_fixture(name, self.module.encoded(obj))

    def case(self, name, action):
        if any(r["name"] == name for r in self.rows):
            raise AssertionError("duplicate test " + name)
        try:
            action()
            self.rows.append({"name": name, "status": "PASS"})
        except Exception as e:
            self.rows.append({"name": name, "status": "FAIL", "detail": repr(e),
                              "trace": traceback.format_exc(limit=5)})


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
    pin = exclusive(suite.root / "TEST_RECORD.json", suite.module.encoded(record))
    failures = [r for r in suite.rows if r["status"] != "PASS"]
    print(json.dumps({"tested": len(suite.rows), "failed": len(failures), "failures": failures, "record": pin}))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
