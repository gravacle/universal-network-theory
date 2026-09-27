#!/usr/bin/env python3
"""Verify this review's bytes and preserved baseline; not a scientific PASS."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path(__file__).resolve().parent
BASE = "e640dd9061a8c288d1273ceacfc9f58c85a9773a"
TREE = "c4517ca37feaf50aa7e7fa549f1b1998dc85f527"
BASELINE_COUNT = 7006
SCOPES = [
    PACKET.name,
    "AUTHENTICATED_REPLAY_CUSTODY_REPAIR_2026-09-27_V001",
    "CUSTODY_RECOVERY_NUMERICS_2026-09-27_V001",
    "AUDIT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001",
    "DEVELOPMENT_R_LINEAGE_CARRIER_REDUCTION_V001",
    "DEVELOPMENT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001",
    "CURRENT_REVIEW_2026-09-27.md",
]


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def load(path):
    return json.loads(path.read_text(), object_pairs_hook=strict_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def safe_file(relative):
    target = safe_destination(relative)
    if not target.is_file():
        raise ValueError("missing file: " + relative)
    return target


def safe_destination(relative):
    path = PurePosixPath(relative)
    if (not relative or path.is_absolute() or ".." in path.parts
            or "\\" in relative or path.as_posix() != relative):
        raise ValueError("unsafe or noncanonical path: " + relative)
    target = ROOT
    for part in path.parts:
        target /= part
        if target.is_symlink():
            raise ValueError("symlink not admitted: " + relative)
    return target


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def artifact_paths():
    found = []
    for scope in SCOPES:
        target = safe_destination(scope)
        if not target.exists():
            raise ValueError("missing curation scope: " + scope)
        files = [target] if target.is_file() else sorted(target.rglob("*"))
        for path in files:
            if "__pycache__" in path.parts or path == PACKET / "REVIEW_SEAL.json":
                continue
            safe_destination(str(path.relative_to(ROOT)))
            if path.is_file():
                found.append(str(path.relative_to(ROOT)))
    if len(found) != len(set(found)):
        raise ValueError("overlapping artifact scopes")
    return sorted(found)


def verify_seal(seal):
    if (set(seal) != {"schema", "baseline_commit", "baseline_tree", "meaning", "artifacts"}
            or seal["schema"] != "UNT_PROGRAM_REVIEW_SEAL_V001"
            or seal["baseline_commit"] != BASE or seal["baseline_tree"] != TREE):
        raise ValueError("seal identity/schema")
    seen = set()
    for item in seal["artifacts"]:
        if set(item) != {"path", "bytes", "sha256"}:
            raise ValueError("artifact schema")
        name = item["path"]
        if name in seen:
            raise ValueError("duplicate artifact: " + name)
        seen.add(name)
        raw = safe_file(name).read_bytes()
        if len(raw) != item["bytes"] or sha(raw) != item["sha256"]:
            raise ValueError("artifact hash/length: " + name)
    if seen != set(artifact_paths()):
        raise ValueError("artifact census differs")
    return seen


def verify_baseline():
    if git("rev-parse", BASE + "^{tree}").decode().strip() != TREE:
        raise ValueError("baseline tree identity")
    entries = git("ls-tree", "-rz", BASE).split(b"\0")
    count = 0
    for entry in entries:
        if not entry:
            continue
        metadata, path = entry.split(b"\t", 1)
        mode, kind, expected = metadata.split()
        if kind != b"blob" or mode not in (b"100644", b"100755"):
            raise ValueError("unsupported baseline object: " + path.decode())
        raw = safe_file(path.decode()).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if blob != expected.decode():
            raise ValueError("baseline bytes changed: " + path.decode())
        count += 1
    return count


def main():
    seal = load(safe_file(str((PACKET / "REVIEW_SEAL.json").relative_to(ROOT))))
    seen = verify_seal(seal)
    baseline_count = verify_baseline()
    if baseline_count != BASELINE_COUNT:
        raise ValueError("baseline file count")
    evidence = load(PACKET / "EVIDENCE.json")
    if (set(evidence) != {"schema", "baseline_commit", "baseline_tree", "baseline_files_preserved", "scope", "sources"}
            or evidence["schema"] != "UNT_REVIEW_BASELINE_EVIDENCE_V001"
            or evidence["baseline_commit"] != BASE or evidence["baseline_tree"] != TREE
            or evidence["baseline_files_preserved"] != baseline_count):
        raise ValueError("evidence schema/baseline")
    evidence_names = set()
    for item in evidence["sources"]:
        if set(item) != {"path", "bytes", "sha256", "git_blob"}:
            raise ValueError("evidence item schema")
        name = item["path"]
        if name in evidence_names:
            raise ValueError("duplicate evidence source")
        evidence_names.add(name)
        safe_file(name)
        raw = git("show", BASE + ":" + name)
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if (sha(raw) != item["sha256"] or len(raw) != item["bytes"]
                or blob != item["git_blob"] or raw != safe_file(name).read_bytes()):
            raise ValueError("evidence differs from baseline: " + name)
    claims = load(PACKET / "CLAIMS.json")
    if (set(claims) != {"schema", "baseline_commit", "scope", "claims"}
            or claims["schema"] != "UNT_CURRENT_CLAIM_REVIEW_V001"
            or claims["baseline_commit"] != BASE
            or {row["id"] for row in claims["claims"]} != {f"UNT-R{i:02d}" for i in range(1, 27)}
            or len(claims["claims"]) != 26):
        raise ValueError("claim schema/census")
    for claim in claims["claims"]:
        if set(claim) != {"id", "type", "domain", "statement", "conditions", "excludes", "evidence", "next_decisive_step"} or not all(claim.values()):
            raise ValueError("claim row schema/blank field")
        if not set(claim["evidence"]) <= evidence_names:
            raise ValueError("unbound claim evidence")
    for results_path in sorted(PACKET.glob("checks*/RESULTS.json")):
        results = load(results_path)
        for check in results["checks"]:
            log_path = results_path.parent / check["log"]
            raw = safe_file(str(log_path.relative_to(ROOT))).read_bytes()
            if sha(raw) != check["log_sha256"] or len(raw) != check["log_bytes"]:
                raise ValueError("check log differs: " + str(log_path))
            if sha(safe_file(check["script"]).read_bytes()) != check["script_sha256"]:
                raise ValueError("check source differs: " + check["id"])
    print(json.dumps({"status": "PASS_REVIEW_BYTE_CUSTODY_NOT_PHYSICAL_PROOF",
                      "baseline_files_preserved": baseline_count,
                      "review_and_repair_artifacts": len(seen),
                      "baseline_evidence_sources": len(evidence["sources"]),
                      "scientific_failures_waived": False}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit("FAIL_REVIEW_CUSTODY: " + str(error))
