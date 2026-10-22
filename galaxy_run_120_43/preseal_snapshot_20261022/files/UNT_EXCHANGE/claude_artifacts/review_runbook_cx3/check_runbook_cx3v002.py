"""Metadata-only independent runbook check; bash -n, never runbook execution."""
from pathlib import Path
import ast
import collections
import hashlib
import json
import re
import subprocess

E = Path("/Users/bgm/Research/UNT_EXCHANGE")
SRC = E / "claude_artifacts/verdict_day_runbook_c3"
OUT = Path(__file__).resolve().parent
inputs = {}


def read(p):
    raw = p.read_bytes()
    inputs[str(p)] = hashlib.sha256(raw).hexdigest()
    return raw


rbp = SRC / "RUNBOOK_EXEC_C3V002.md"
rb = read(rbp).decode()
lines = rb.splitlines()
x = json.loads(read(SRC / "XREF_C3V002.json"))
assert hashlib.sha256(rb.encode()).hexdigest() == x["runbook_sha256"]
sources = {}
for name, ref in x["sources"].items():
    b = read(Path(ref["path"]))
    assert hashlib.sha256(b).hexdigest() == ref["sha256"]
    sources[name] = b.decode().splitlines()
blocks, ranges = {}, set()
heading = None
active = False
for n, line in enumerate(lines, 1):
    if line.startswith("## "):
        heading = line[3:].split(" — ")[0].split(". ")[0]
    if line == "```bash":
        active = True
        blocks[heading] = []
    elif line == "```":
        active = False
    elif active:
        ranges.add(n)
        blocks[heading].append(line)
assert len(x["lines"]) == len(ranges) == 489
assert {r["line"] for r in x["lines"]} == ranges
mismatches, direct = [], 0
for row in x["lines"]:
    assert lines[row["line"] - 1] == row["text"]
    if row["kind"] in ("VERBATIM", "REDERIVED", "QOS_DROPPED"):
        name, number = re.match(r"([SJMV]):L(\d+)", row["ref"]).groups()
        original = sources[name][int(number) - 1]
        if row["kind"] == "QOS_DROPPED":
            original = re.sub(r"^(?:/usr/sbin/taskpolicy -b )?(?:(?:/usr/bin/)?nice -n 10 )?", "", original)
        direct += 1
        if original != row["text"]:
            mismatches.append({"line": row["line"], "source": original, "actual": row["text"]})
env = {"PATH": "/usr/bin:/bin", "BASH_ENV": "/dev/null"}
preamble = "\n".join(blocks["P0"]) + "\n"
syntax = []
unbound = {}
definitions = lambda s: set(re.findall(r"(?m)^(?:export )?([A-Z][A-Z0-9_]*)=", s))
base_defs = definitions(preamble) | definitions("\n".join(sources["V"]))
for name, block in blocks.items():
    text = "\n".join(block) + "\n"
    call = text if name == "P0" else preamble + text
    result = subprocess.run(["/bin/bash", "-n"], input=call, text=True, env=env, capture_output=True)
    syntax.append({"block": name, "exit": result.returncode, "stderr": result.stderr})
    used = set(re.findall(r"\$(?:\{#?)?([A-Z][A-Z0-9_]*)", text))
    unknown = sorted(used - base_defs - definitions(text))
    if unknown:
        unbound[name] = unknown
assert blocks["P0"][0] == "set -euo pipefail"
# These are inert shell probes, not substitutions of executable runbook content.
probes = []
for name, code in [
    ("failure_stops_later_success", "set -euo pipefail\nfalse\nprintf MASKED"),
    ("failed_pipeline_stops", "set -euo pipefail\nfalse | true\nprintf MASKED"),
    ("empty_runtime_slot_stops", 'set -euo pipefail\nX=\n: "${X:?PASTE X}"\nprintf MASKED'),
    ("unset_variable_stops", 'set -euo pipefail\nprintf "%s" "$NEVER_DEFINED_CX3"\nprintf MASKED'),
]:
    p = subprocess.run(["/bin/bash"], input=code, text=True, env=env, capture_output=True)
    probes.append({"name": name, "passed": p.returncode != 0 and "MASKED" not in p.stdout,
                   "exit": p.returncode})
embedded = []
for name, block in blocks.items():
    for match in re.finditer(r"<<'([A-Z]+)'\n(.*?)\n\1(?:\n|$)", "\n".join(block) + "\n", re.S):
        ast.parse(match[2])
        embedded.append(name)
result = {
    "schema": "NARROW_RUNBOOK_CHECK_CX3V001",
    "date_u": subprocess.check_output(["/bin/date", "-u"], text=True).strip(),
    "status": "TESTED", "runbook": str(rbp),
    "code_lines_and_xref_covered": 489,
    "direct_source_lines_compared": direct,
    "source_line_mismatches": mismatches,
    "kinds": dict(collections.Counter(r["kind"] for r in x["lines"])),
    "bash_syntax": syntax, "unbound_shell_names_static": unbound,
    "inert_failure_probes": probes, "python_heredoc_syntax_blocks": embedded,
    "inputs_sha256_from_bytes": inputs,
    "UNTESTED": ["all runbook execution", "all runtime fills", "filesystem output readiness",
                 "science, protected data and step-2 outputs"],
}
p = OUT / "CHECK_RECORD_CX3V002.json"
with p.open("x") as f:
    json.dump(result, f, indent=2, sort_keys=True)
    f.write("\n")
print(json.dumps({"record": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                  "source_mismatches": mismatches, "syntax": len(syntax),
                  "syntax_failures": [v for v in syntax if v["exit"]],
                  "unbound": unbound, "probes": probes}))
