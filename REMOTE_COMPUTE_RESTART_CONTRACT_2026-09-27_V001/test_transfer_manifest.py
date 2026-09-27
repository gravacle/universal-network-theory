#!/usr/bin/env python3
"""Negative tests for SSH transfer admission; no network access is used."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import transfer_manifest as transfer


class TransferManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "bundle"
        (self.root / "nested").mkdir(parents=True)
        (self.root / "nested" / "input.bin").write_bytes(b"\x00\x01\xff")
        (self.root / "runner.py").write_bytes(b"print('not executed')\n")
        self.allowlist = self.base / "allowlist.txt"
        self.allowlist.write_text("nested/input.bin\nrunner.py\n", encoding="utf-8")
        self.manifest = self.base / "MANIFEST.json"

    def build(self) -> str:
        return transfer.build_manifest(self.root, self.allowlist, self.manifest)

    def test_exact_round_trip(self) -> None:
        digest = self.build()
        result = transfer.verify_manifest(self.root, self.manifest, digest)
        self.assertEqual(result["file_count"], 2)
        self.assertEqual(result["total_bytes"], 25)

    def test_wrong_digest_and_changed_file_rejected(self) -> None:
        digest = self.build()
        with self.assertRaisesRegex(transfer.TransferError, "manifest SHA-256 mismatch"):
            transfer.verify_manifest(self.root, self.manifest, "0" * 64)
        (self.root / "nested" / "input.bin").write_bytes(b"\x00\x01\x00")
        with self.assertRaisesRegex(transfer.TransferError, "file byte count or SHA-256 mismatch"):
            transfer.verify_manifest(self.root, self.manifest, digest)

    def test_extra_file_rejected_unless_explicit_overlay_mode(self) -> None:
        digest = self.build()
        (self.root / "unlisted.txt").write_text("extra", encoding="utf-8")
        with self.assertRaisesRegex(transfer.TransferError, "missing or extra files"):
            transfer.verify_manifest(self.root, self.manifest, digest)
        self.assertTrue(transfer.verify_manifest(self.root, self.manifest, digest,
                                                 allow_extras=True)["allow_extras"])

    def test_symlink_rejected_even_in_overlay_mode(self) -> None:
        digest = self.build()
        (self.root / "nested" / "input.bin").unlink()
        (self.root / "nested" / "input.bin").symlink_to(self.root / "runner.py")
        with self.assertRaisesRegex(transfer.TransferError, "symlink in file route"):
            transfer.verify_manifest(self.root, self.manifest, digest, allow_extras=True)

    def test_traversal_duplicate_and_noncanonical_allowlist_rejected(self) -> None:
        for text in ("../outside\n", "runner.py\nrunner.py\n", "runner.py\r\n",
                     "bad\tname\n"):
            with self.subTest(text=text):
                self.allowlist.write_bytes(text.encode("ascii"))
                with self.assertRaises(transfer.TransferError):
                    self.build()

    def test_git_metadata_component_rejected(self) -> None:
        for name in (".git/config", "nested/.git/config"):
            with self.subTest(name=name):
                self.allowlist.write_text(name + "\n", encoding="utf-8")
                with self.assertRaisesRegex(transfer.TransferError, "local Git metadata"):
                    self.build()

    def test_manifest_duplicate_key_and_record_mutation_rejected(self) -> None:
        self.build()
        raw = self.manifest.read_text(encoding="ascii")
        self.manifest.write_text(raw.replace('"schema":', '"schema":"bogus","schema":', 1),
                                 encoding="ascii")
        digest = transfer.sha256_bytes(self.manifest.read_bytes())
        with self.assertRaisesRegex(transfer.TransferError, "duplicate JSON key"):
            transfer.verify_manifest(self.root, self.manifest, digest)
        data = json.loads(raw)
        data["files"][0]["bytes"] += 1
        self.manifest.write_bytes(transfer.canonical_bytes(data))
        digest = transfer.sha256_bytes(self.manifest.read_bytes())
        with self.assertRaisesRegex(transfer.TransferError, "file byte count or SHA-256 mismatch"):
            transfer.verify_manifest(self.root, self.manifest, digest)

    def test_owner_once_manifest(self) -> None:
        self.build()
        with self.assertRaisesRegex(transfer.TransferError, "owner-once manifest"):
            self.build()


if __name__ == "__main__":
    unittest.main()
