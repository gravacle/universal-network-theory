#!/usr/bin/env python3
"""Restore exact small progression inputs; preflight all transitive dependencies.

The six larger L10 state shards stay outside Git. An optional --source-root can
provide missing hash-bound shards from an explicitly selected local custody
root. Without it, a clean clone reports remaining missing external inputs.
No state evolution, cache regeneration or scientific-result publication occurs.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile

from restore_l8_manifest import ROOT, PACKET, safe_path, authenticated_bytes, require

MODULE = "model/relational_accumulation.py"
MODULE_SHA = "d04ebd84c7dc98bd9d6aafae6c97aaf6430e994797138762be2cc87dcfb8bba4"
CACHE_BASE = "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/CACHE_PAYLOADS_V012"

def parse_pins(root):
    source = authenticated_bytes(safe_path(root, MODULE), MODULE_SHA)
    wanted = {"_PROGRESSION_SOURCE_PATH", "_PROGRESSION_SOURCE_SHA256", "_PROGRESSION_INPUT_PINS"}
    values = {}
    def literal(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Tuple):
            return tuple(literal(item) for item in node.elts)
        if isinstance(node, ast.Name) and node.id in values:
            return values[node.id]
        raise ValueError("nonliteral progression pin expression")
    for statement in ast.parse(source).body:
        if isinstance(statement, ast.Assign) and len(statement.targets) == 1:
            target = statement.targets[0]
            if isinstance(target, ast.Name) and target.id in wanted:
                require(target.id not in values, "duplicate progression pin declaration")
                values[target.id] = literal(statement.value)
    require(set(values) == wanted, "progression pin declaration census")
    pairs = values["_PROGRESSION_INPUT_PINS"]
    require(len(pairs) == 13 and len(dict(pairs)) == 13, "progression input pin census")
    return dict(pairs)

def manifests_and_indexes(root, pins):
    manifests = []
    indexes = []
    for length in (8, 10):
        relative = CACHE_BASE + "/L%d/CACHE_MANIFEST.json" % length
        included = PACKET + "/RECOVERED_INPUTS/L%d_CACHE_MANIFEST.json" % length
        data = authenticated_bytes(safe_path(root, included), pins[relative])
        manifest = json.loads(data)
        ledger = manifest["files"]
        by_name = {entry["path"]: entry for entry in ledger}
        require(len(by_name) == len(ledger), "duplicate cache ledger entry")
        manifests.append({"path": relative, "included": included, "sha256": pins[relative],
                          "bytes": len(data)})
        for q in range(4, length):
            names = ("admission_n_%02d_q_%02d_blank.i32" % (length - 1, q),
                     "lineage_n_%02d_q_%02d_words.u32" % (length - 1, q))
            for name in names:
                entry = by_name[name]
                require(type(entry["bytes"]) is int and entry["bytes"] >= 0, "index byte count")
                require(math.prod(entry["shape"]) * 4 == entry["bytes"], "index shape/byte census")
                indexes.append({"path": CACHE_BASE + "/L%d/" % length + name,
                                "included": PACKET + "/RECOVERED_INPUTS/PROGRESSION_INDEX/L%d/" % length + name + ".payload",
                                "sha256": entry["sha256"], "bytes": entry["bytes"]})
    require(len(manifests) == 2 and len(indexes) == 20, "manifest/index census")
    return manifests, indexes

def publish_exact(root, relative, raw, digest):
    require(hashlib.sha256(raw).hexdigest() == digest, "publication source digest")
    destination = safe_path(root, relative)
    if destination.exists():
        authenticated_bytes(destination, digest)
        return "EXISTING_IDENTICAL_PRESERVED"
    parent = root
    for component in Path(relative).parts[:-1]:
        parent = parent / component
        if not parent.exists():
            parent.mkdir()
        require(parent.is_dir() and not parent.is_symlink(), "unsafe destination ancestor")
    fd, name = tempfile.mkstemp(prefix=".progression-recovery-", dir=parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        safe_path(root, relative)
        os.link(str(temporary), str(destination))
    finally:
        temporary.unlink()
    authenticated_bytes(destination, digest)
    return "RESTORED_EXACT_AUTHENTICATED_INPUT"

def run(root, source_root=None, preflight_only=False):
    pins = parse_pins(root)
    manifests, indexes = manifests_and_indexes(root, pins)
    actions = []
    if not preflight_only:
        for record in manifests + indexes:
            raw = authenticated_bytes(safe_path(root, record["included"]), record["sha256"])
            require(len(raw) == record["bytes"], "included payload byte count")
            action = publish_exact(root, record["path"], raw, record["sha256"])
            actions.append({"path": record["path"], "action": action})
        if source_root is not None:
            for relative, digest in pins.items():
                if not relative.endswith(".npy"):
                    continue
                destination = safe_path(root, relative)
                if destination.exists():
                    authenticated_bytes(destination, digest)
                    continue
                raw = authenticated_bytes(safe_path(source_root, relative), digest)
                action = publish_exact(root, relative, raw, digest)
                actions.append({"path": relative, "action": action})
    all_pins = list(pins.items()) + [(item["path"], item["sha256"]) for item in indexes]
    missing = []
    verified = []
    for relative, digest in all_pins:
        path = safe_path(root, relative)
        if not path.exists():
            missing.append({"path": relative, "sha256": digest})
            continue
        raw = authenticated_bytes(path, digest)
        verified.append({"path": relative, "sha256": digest, "bytes": len(raw)})
    return {"schema": "UNT_PROGRESSION_RECOVERY_PREFLIGHT_V001",
            "status": "PASS_ALL_33_PROGRESSION_INPUTS_AUTHENTICATED" if not missing else "INCOMPLETE_MISSING_EXTERNAL_INPUTS",
            "source_module_sha256": MODULE_SHA, "verified": verified, "missing": missing,
            "actions": actions, "new_evolution": False,
            "raw_state_shards_embedded_in_git_packet": False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    try:
        result = run(args.root.absolute(), args.source_root.absolute() if args.source_root else None,
                     args.preflight_only)
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "REFUSED", "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["missing"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
