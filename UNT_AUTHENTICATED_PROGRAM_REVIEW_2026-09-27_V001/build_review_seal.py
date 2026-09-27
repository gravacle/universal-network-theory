#!/usr/bin/env python3
"""Build the new review manifest after editing; never alter historical seals."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from verify_review import BASE, TREE, PACKET, ROOT, verify_baseline, artifact_paths, safe_destination

SCOPES = [
    PACKET.name,
    "AUTHENTICATED_REPLAY_CUSTODY_REPAIR_2026-09-27_V001",
    "CUSTODY_RECOVERY_NUMERICS_2026-09-27_V001",
    "AUDIT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001",
    "DEVELOPMENT_R_LINEAGE_CARRIER_REDUCTION_V001",
    "DEVELOPMENT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001",
    "CURRENT_REVIEW_2026-09-27.md",
]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def publish_json(path, payload, replace=False):
    safe_destination(str(path.relative_to(ROOT)))
    raw = (json.dumps(payload, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".review-draft-", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        safe_destination(str(path.relative_to(ROOT)))
        if replace:
            os.replace(temporary, path)
        else:
            os.link(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replace-draft-seal", action="store_true")
    args = parser.parse_args()
    out = PACKET / "REVIEW_SEAL.json"
    safe_destination(str(out.relative_to(ROOT)))
    safe_destination(str((PACKET / "EVIDENCE.json").relative_to(ROOT)))
    artifact_paths()
    if out.exists() and not args.replace_draft_seal:
        raise SystemExit("Refusing existing seal; draft replacement must be explicit")
    baseline_count = verify_baseline()
    base_names = set(subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-tree", "-rz", "--name-only", BASE]
    ).decode().strip("\0").split("\0"))
    claims = json.loads((PACKET / "CLAIMS.json").read_text())
    names = {p for row in claims["claims"] for p in row["evidence"]}
    names.update({"README.md", "CURRENT_HANDOFF.md", "PROOF_GUIDE.md",
                  "DEVELOPMENT_UNT_FOUNDATIONAL_PREMISE_DISCHARGE_V001/FOUNDATIONAL_CLAIM_LEDGER.tsv",
                  "MIGRATION_CONTEXT_AUDIT_2026-09-27_V001/INVENTORY.json",
                  "MIGRATION_CONTEXT_AUDIT_2026-09-27_V001/CURRENT_MACHINE_VALIDATION_2026-09-27.json",
                  "publication/zenodo_reproduction_v001/capsule_manifest.json",
                  "publication/zenodo_reproduction_v001/PUBLICATION_CLAIM_MAP.tsv"})
    for path in PACKET.rglob("*.md"):
        for match in re.findall(r"[A-Za-z0-9_][A-Za-z0-9_.-]*(?:/[A-Za-z0-9_.-]+)+", path.read_text()):
            match = match.removeprefix("program-worktree/")
            if match in base_names:
                names.add(match)
    for path in PACKET.glob("checks*/RESULTS.json"):
        for row in json.loads(path.read_text())["checks"]:
            if row["script"] in base_names:
                names.add(row["script"])
    sources = []
    for name in sorted(names):
        if name not in base_names:
            raise ValueError("claim evidence not present at baseline: " + name)
        raw = (ROOT / name).read_bytes()
        blob = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", BASE + ":" + name]).decode().strip()
        sources.append({"path": name, "bytes": len(raw), "sha256": digest(raw), "git_blob": blob})
    publish_json(PACKET / "EVIDENCE.json", {
        "schema": "UNT_REVIEW_BASELINE_EVIDENCE_V001", "baseline_commit": BASE,
        "baseline_tree": TREE, "baseline_files_preserved": baseline_count,
        "scope": "Cited source anchors and check entrypoints; whole baseline preservation independently checked. No transitive replay completeness is implied.",
        "sources": sources}, replace=args.replace_draft_seal)
    artifacts = []
    for name in artifact_paths():
        raw = (ROOT / name).read_bytes()
        artifacts.append({"path": name, "bytes": len(raw), "sha256": digest(raw)})
    publish_json(out, {"schema": "UNT_PROGRAM_REVIEW_SEAL_V001",
        "baseline_commit": BASE, "baseline_tree": TREE,
        "meaning": "Byte-custody manifest, not a scientific or empirical truth certificate.",
        "artifacts": sorted(artifacts, key=lambda x:x["path"])}, replace=args.replace_draft_seal)
    print(f"SEALED {len(artifacts)} artifacts, {len(sources)} cited baseline sources, {baseline_count} preserved baseline files")


if __name__ == "__main__":
    main()
