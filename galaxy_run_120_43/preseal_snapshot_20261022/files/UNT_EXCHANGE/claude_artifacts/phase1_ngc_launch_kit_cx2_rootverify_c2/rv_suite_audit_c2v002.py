"""Root verify (Claude2 lineage), P-112 CX2V001 (audit v002: realpath check, read sites, coverage case): re-run Codex2's synthetic suite in-process under an
audit hook that records every open/spawn/signal made with P-112 code on the stack.

Synthetic only. Writes only under --out (a new directory, exclusive create). No network.
"""
import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import traceback
import types
from pathlib import Path

KIT = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2/"
TOOL = KIT + "phase1_ngc_launch_cx2v001.py"
TOOL_SHA = "a72d96c150ca1c638474cddba23f5264374c7ae9aa285c3d38ebfb3e61519bb1"
TESTS = KIT + "test_phase1_ngc_launch_cx2v001.py"
TESTS_SHA = "fd50301bbbe4e4d6e91ad30a4881eaab6f54a1ab77a1856edea04b9d9670b76e"
VENDOR_RUN1 = KIT + "test_records_cx2v001/RUN1/TEST_RECORD.json"
VENDOR_RUN1_SHA = "50e0951bfe19216e143a8e90785e9569a9fd795334acc1a605144df08d1a5e15"
V006 = ("/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/"
        "CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md")
OUTDIR_COMPONENT = re.compile(r"^NGC_P1_.+_RUN_(?:CX2V001|C2V003A)_A[0-9]+$")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verified(path, want):
    raw = Path(path).read_bytes()
    if sha(raw) != want:
        raise SystemExit("PIN_MISMATCH " + path)
    return raw


def forbidden_reason(path):
    """Paths P-112 must never open (brief section 3, A223). Existence checks are not opens."""
    if path == V006:
        return None  # the named exception
    parts = Path(path).parts
    low = [p.lower() for p in parts]
    base = low[-1] if low else ""
    if base in ("result.json", "finish.json", "progress.jsonl"):
        return "RESULT_FILE"
    if "stages" in low:
        return "STAGES"
    if any("ngc3198" in p for p in low):
        return "NGC3198_COMPONENT"
    if any(p == "v007_postseal_records" for p in low) or "a_side" in low or ".codex" in low:
        return "SEALED_OR_CODEX"
    if path.endswith((".receipt.json.stdout.txt", ".receipt.json.stderr.txt")):
        return "RECEIPT_STDIO"
    for i, p in enumerate(parts[:-1]):
        if OUTDIR_COMPONENT.match(p):
            return "INSIDE_OUTDIR"
    return None


class Audit:
    def __init__(self):
        self.case = "setup"
        self.opens = []        # (case, path, mode, flags)
        self.spawns = []       # (case, argv0, argv)
        self.signals = []      # (case, event, args)
        self.forbidden = []

    def from_p112(self):
        frame = sys._getframe(2)
        while frame is not None:
            if frame.f_code.co_filename == TOOL:
                return True
            frame = frame.f_back
        return False

    def hook(self, event, args):
        if event == "open":
            target = args[0]
            if not isinstance(target, (str, bytes)):
                return
            if not self.from_p112():
                return
            path = target.decode() if isinstance(target, bytes) else target
            mode, flags = args[1], args[2]
            sites, frame = [], sys._getframe(1)
            while frame is not None and len(sites) < 2:
                if frame.f_code.co_filename == TOOL:
                    sites.append("%s@%d" % (frame.f_code.co_name, frame.f_lineno))
                frame = frame.f_back
            self.opens.append((self.case, path, mode, flags, " <- ".join(sites)))
            real = os.path.realpath(path)
            for spelling in dict.fromkeys((path, real)):
                reason = forbidden_reason(spelling)
                if reason is not None:
                    self.forbidden.append({"case": self.case, "path": path, "realpath": real,
                                           "reason": reason, "mode": mode})
                    break
        elif event == "subprocess.Popen":
            if self.from_p112():
                argv = args[1]
                if isinstance(argv, (list, tuple)):
                    argv = [a if isinstance(a, str) else repr(a) for a in argv]
                self.spawns.append((self.case, str(args[0]), argv))
        elif event in ("os.kill", "os.killpg"):
            if self.from_p112():
                self.signals.append((self.case, event, [int(a) for a in args]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    tool_raw = verified(TOOL, TOOL_SHA)
    tests_raw = verified(TESTS, TESTS_SHA)
    vendor_run1 = json.loads(verified(VENDOR_RUN1, VENDOR_RUN1_SHA))
    started = subprocess.check_output(["/bin/date", "-u"], env=dict(os.environ, LC_ALL="C"), text=True).strip()
    audit = Audit()
    sys.addaudithook(audit.hook)
    T = types.ModuleType("_rootverify_vendor_tests")
    T.__file__ = TESTS
    exec(compile(tests_raw, TESTS, "exec"), T.__dict__)
    suite = T.Suite(TOOL, str(out), TOOL_SHA)  # creates `out` (mkdir, must be new)
    original_case = suite.case

    def tracked_case(name, action):
        audit.case = name
        try:
            return original_case(name, action)
        finally:
            audit.case = "between:" + name
    suite.case = tracked_case
    for group in T.ALL_GROUPS:
        audit.case = "group:" + group
        try:
            getattr(T, group)(suite)
        except Exception as error:
            suite.rows.append({"name": "GROUP_" + group, "status": "FAIL", "detail": repr(error),
                               "trace": traceback.format_exc(limit=5)})
    codes = set()
    for node in ast.walk(ast.parse(tool_raw.decode())):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            index = 1 if node.func.id == "need" else 0 if node.func.id == "Refusal" else None
            if index is not None and len(node.args) > index:
                for arg in ast.walk(node.args[index]):
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        codes.add(arg.value)
    missing = sorted(codes - set(suite.refusals))
    suite.case("EVERY_NAMED_REFUSAL_EXERCISED", lambda: suite.eq(missing, []))
    mine = [{"name": r["name"], "status": r["status"]} for r in suite.rows]
    theirs = [{"name": r["name"], "status": r["status"]} for r in vendor_run1["cases"]]
    # A226 dynamic evidence: a path read (non-exclusive, non-write) two or more times by P-112 frames in one case.
    reads, site_sets = {}, {}
    for case, path, mode, flags, site in audit.opens:
        is_read = (isinstance(mode, str) and "r" in mode and not any(c in mode for c in "wxa+")) or (
            mode is None and isinstance(flags, int) and (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT)) == 0
            and not os.path.isdir(path))
        if is_read:
            reads.setdefault(case, {}).setdefault(path, 0)
            reads[case][path] += 1
            site_sets.setdefault((case, path), []).append(site)
    combos = {}
    for (case, path), sites in site_sets.items():
        if len(sites) >= 2:
            key = " | ".join(sorted(set(sites)))
            combos.setdefault(key, {"cases": set(), "example_basename": Path(path).name})["cases"].add(case)
    combos = {k: {"n_cases": len(v["cases"]), "example_basename": v["example_basename"]} for k, v in sorted(combos.items())}
    multi = {}
    for case, paths in reads.items():
        for path, n in paths.items():
            if n >= 2:
                base = Path(path).name
                multi.setdefault(base if not base.startswith("P112_") else re.sub(r"_A[0-9]+", "_A<k>", base), set()).add(case)
    finished = subprocess.check_output(["/bin/date", "-u"], env=dict(os.environ, LC_ALL="C"), text=True).strip()
    record = {
        "schema": "P112_ROOTVERIFY_SUITE_AUDIT_C2V002",
        "tool": {"path": TOOL, "sha256": TOOL_SHA}, "tests": {"path": TESTS, "sha256": TESTS_SHA},
        "vendor_run1": {"path": VENDOR_RUN1, "sha256": VENDOR_RUN1_SHA},
        "started_date_u": started, "date_u": finished,
        "cases_total": len(mine), "cases_failed": [r for r in suite.rows if r["status"] != "PASS"],
        "refusal_codes_static": len(codes), "refusal_codes_not_exercised": missing,
        "case_list_equal_to_vendor_run1": mine == theirs,
        "case_names": [r["name"] for r in suite.rows],
        "audit": {
            "scope": "in-process only: P-112 frames in this interpreter. CLI/sampler subprocesses are not hooked.",
            "p112_open_events": len(audit.opens),
            "forbidden_opens": audit.forbidden,
            "distinct_paths_opened": len({o[1] for o in audit.opens}),
            "multi_read_site_combinations": combos,
            "multi_read_basenames_per_case": {k: sorted(v)[:12] + (["..."] if len(v) > 12 else [])
                                              for k, v in sorted(multi.items())},
            "spawned_by_p112": sorted({(" ".join(argv[:5]) if isinstance(argv, list) else str(argv))[:240]
                                       for _, _, argv in audit.spawns}),
            "signals_by_p112": [{"case": c, "event": e, "args": x} for c, e, x in audit.signals],
        },
    }
    raw = (json.dumps(record, sort_keys=True, indent=1) + "\n").encode()
    with (out / "ROOTVERIFY_SUITE_AUDIT.json").open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
        os.fchmod(f.fileno(), 0o444)
    print(json.dumps({"cases": len(mine), "failed": len(record["cases_failed"]), "missing": missing,
                      "equal_to_vendor": mine == theirs, "forbidden_opens": len(audit.forbidden),
                      "open_events": len(audit.opens), "signals": len(audit.signals),
                      "audit_sha256": sha(raw)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
