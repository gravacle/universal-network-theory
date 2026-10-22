"""Root verify (Claude2 lineage): static A226 single-read inventory of P-112 CX2V001.

Every call site that reads file bytes (read_bytes, open, pin_of, read_pin, read_v006, try_launch_json,
wait_launch_json, load_verified) is listed from the AST of the pinned bytes and classified by hand.
Writes one JSON file by exclusive create.
"""
import ast
import hashlib
import json
import os
import sys
from pathlib import Path

TOOL = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2/phase1_ngc_launch_cx2v001.py"
TOOL_SHA = "a72d96c150ca1c638474cddba23f5264374c7ae9aa285c3d38ebfb3e61519bb1"

DEFECT_B1 = ("DEFECT_A226_B1: launch.json is checked on one read (wait_launch_json L1980 / stop_launch_failure L1925) and "
             "the LAUNCH/MISLAUNCH record pins sha256, utc and child_pid from a later read (L1956, L1960)")
DEFECT_B2 = ("DEFECT_A226_B2: the monitor receipt is parsed and classified OFF_SPEC/NO_RUN_DIRECTORY from read L1469, "
             "but the non-attempt pin (status, assembly record) is hashed from a second read L1474")
DEFECT_B3 = ("DEFECT_A226_B3: --verify byte-compares read L1771 and reports the registry pin hashed from read L1773")
VERIFIED = "OK_VERIFIED_REREAD: pin_of hashes read 1; read_pin re-reads, hashes that buffer against the pin, parses it (fail-closed)"
CLASSES = {
    190: "WRITE_EXCLUSIVE", 196: "DIR_FSYNC",
    255: "OK_SINGLE_READ: read_pin hashes the buffer it parses",
    262: "PIN_SOURCE: hash-only read (followed by read_pin where parsed)",
    266: "OK_SINGLE_READ_EXEC: load_verified execs the hashed buffer",
    715: "OK_SINGLE_READ: V006 bytes feed gate, pin parse and RESIDUAL_RETRY lines from one buffer",
    726: "OK_SINGLE_READ", 754: "NOTE_INHERENT: own-bytes hash is a second read of the executing script (0444)",
    755: "OK_SINGLE_READ", 757: "OK_SINGLE_READ_EXEC", 759: "OK_SINGLE_READ_EXEC",
    803: VERIFIED, 804: VERIFIED, 815: VERIFIED, 816: VERIFIED, 829: VERIFIED, 830: VERIFIED,
    845: "OK_SINGLE_READ", 846: "OK_SINGLE_READ", 847: "OK_SINGLE_READ", 848: "OK_SINGLE_READ", 849: "OK_SINGLE_READ",
    854: "OK_HASH_CHECK_ONLY", 866: "OK_SINGLE_READ", 872: "OK_SINGLE_READ", 873: "OK_SINGLE_READ",
    885: "OK_SINGLE_READ", 894: "OK_SINGLE_READ", 906: "OK_SINGLE_READ",
    919: "OK_SINGLE_READ (point.key re-read later via finish_call L928, also verified)",
    920: "OK_HASH_CHECK_ONLY", 921: VERIFIED, 922: VERIFIED, 928: "OK_SINGLE_READ", 939: "OK_SINGLE_READ",
    1050: "UNPINNED: argv file hash for the declared-list match (no pin is recorded from it)",
    1123: "UNPINNED_READER (no guard_read: follows a symlink alias; see blinding finding)",
    1136: "SEE " + "B1 (checked read)",
    1186: VERIFIED, 1201: VERIFIED,
    1234: "UNPINNED: sampler liveness read",
    1266: "UNPINNED: sampler reads utc_start/utc_end (no guard_read)",
    1290: "UNPINNED: work file", 1295: "UNPINNED: work file",
    1317: VERIFIED, 1318: VERIFIED, 1370: VERIFIED, 1371: VERIFIED,
    1381: "OK_SINGLE_READ", 1400: "OK_HASH_CHECK_ONLY: 0782 per-invocation log re-hash",
    1469: DEFECT_B2 + " (first read; no guard_read)", 1474: DEFECT_B2 + " (second read)",
    1481: VERIFIED, 1484: VERIFIED, 1515: "OK_SINGLE_READ",
    1533: "OK_HASH_ONLY: refusal-invocation logs, after every absent check", 1534: "OK_HASH_ONLY",
    1581: VERIFIED, 1582: VERIFIED, 1610: VERIFIED, 1611: VERIFIED, 1628: VERIFIED, 1629: VERIFIED,
    1641: VERIFIED, 1642: VERIFIED,
    1692: "NOTE: V006 re-read for the cutoff copy; the copy records the digest of this same buffer (V006 is unpinned and grows)",
    1698: "OK_COPY_VERIFY", 1701: "OK_COPY_VERIFY", 1712: "OK_HASH_ONLY",
    1726: VERIFIED, 1727: VERIFIED,
    1771: DEFECT_B3 + " (compared read)", 1773: DEFECT_B3 + " (pinned read)",
    1810: "WRITE_EXCLUSIVE",
    1819: "NOTE_CROSS_PROCESS: hash check, then the dry harness/driver are executed by path in a child",
    1829: VERIFIED, 1830: VERIFIED,
    1837: "NOTE_CROSS_PROCESS: hash check of the memory watch; liveness by ps",
    1872: VERIFIED, 1873: VERIFIED,
    1899: "NOTE_CROSS_PROCESS: hash check, then kit kill-target executed by path",
    1925: DEFECT_B1 + " (MISLAUNCH path: stop decision read)",
    1956: DEFECT_B1 + " (record read)", 1960: DEFECT_B1 + " (third read when the file did not parse)",
    1979: "OK_VERIFIED_REREAD: m15 record re-read against the plan's pin",
    1980: DEFECT_B1 + " (checked read)",
    1985: "NOTE_CROSS_PROCESS: hash check, then twin kill watch executed by path",
    2018: VERIFIED, 2019: VERIFIED,
    2023: "UNPINNED: invocation.json / monitor_pid.json (bound to the plan pin by value)",
    2058: "NOTE_CROSS_PROCESS: driver/monitor hash check; executed by path (monitor re-attests both pins in launch.json)",
    2083: "UNPINNED: sampler first-sample work file",
    2142: "OK_SINGLE_READ (verify only)",
    2149: "NOTE_CROSS_PROCESS: stop record pins launch.json after kit kill-target read it in its own process",
    2180: "OK_SINGLE_READ", 2207: "OK_SINGLE_READ",
}
NAMES = {"pin_of", "read_pin", "read_bytes", "open", "read_v006", "try_launch_json", "load_verified", "read_text",
         "wait_launch_json"}


def main():
    out = Path(sys.argv[1])
    raw = Path(TOOL).read_bytes()
    if hashlib.sha256(raw).hexdigest() != TOOL_SHA:
        raise SystemExit("PIN_MISMATCH")
    src = raw.decode()
    tree = ast.parse(src)
    owner = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for sub in ast.walk(node):
                if hasattr(sub, "lineno"):
                    owner.setdefault(sub.lineno, []).append(node.name)
    rows = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
            if name in NAMES:
                rows.append({"line": node.lineno, "function": owner.get(node.lineno, ["<module>"])[-1], "call": name,
                             "source": ast.get_source_segment(src, node)[:120],
                             "class": CLASSES.get(node.lineno, "UNCLASSIFIED")})
    rows = sorted({(r["line"], r["call"], r["source"]): r for r in rows}.values(), key=lambda r: (r["line"], r["call"]))
    unclassified = [r for r in rows if r["class"] == "UNCLASSIFIED"]
    doc = {"schema": "P112_ROOTVERIFY_STATIC_A226_C2V001", "tool": {"path": TOOL, "sha256": TOOL_SHA},
           "rule": "V006 A226 ruling 1 (single-read binding on P-112) as stated in A222: read once, hash that buffer "
                   "against its pin, parse that same buffer. A226's assessment scopes the class to two reads inside one "
                   "process; cross-process execution by path is listed as NOTE_CROSS_PROCESS.",
           "sites": rows, "unclassified": unclassified,
           "defects": [DEFECT_B1, DEFECT_B2, DEFECT_B3]}
    data = (json.dumps(doc, sort_keys=True, indent=1) + "\n").encode()
    with out.open("xb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
        os.fchmod(fh.fileno(), 0o444)
    print(json.dumps({"sites": len(rows), "unclassified": len(unclassified), "sha256": hashlib.sha256(data).hexdigest()}))


if __name__ == "__main__":
    main()
