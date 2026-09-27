"""Regression and refusal checks for additive AURFT manifest resolution."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from manifest_resolution import CustodyRefusal, resolve_manifest_item


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
LOCAL = "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001"
ROOTED = "LANE_RFT_CAUCHY_TIME_SLICE_ONTIC_COVERAGE_V001"
ORIGINAL = ROOT / "LANE_RFT_AXIOMATIC_URFT_CLOSURE_V001/verify_axiomatic_urft_closure.py"
SUCCESSOR = PACKET / "verify_axiomatic_urft_closure_v002.py"


class ResolutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.lane = self.root / LOCAL
        self.lane.mkdir()
        self.manifest = self.lane / "MANIFEST.sha256"
        self.content = b"authenticated local content\n"
        self.sha = sha256(self.content).hexdigest()
        self.target = self.lane / "README.md"
        self.target.write_bytes(self.content)
        self.manifest.write_text(f"{self.sha}  README.md\n")

    def test_root_readme_cannot_shadow_local(self):
        (self.root / "README.md").write_text("different repository navigation\n")
        self.assertEqual(resolve_manifest_item(self.root, self.manifest, "README.md"), self.target)

    def test_matching_root_copy_is_not_a_fallback_for_missing_local(self):
        (self.root / "README.md").write_bytes(self.content)
        self.target.unlink()
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, self.manifest, "README.md")

    def test_hash_disagreement_is_not_resolved_by_search(self):
        (self.root / "README.md").write_bytes(self.content)
        self.target.write_text("changed local bytes\n")
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, self.manifest, "README.md")

    def test_duplicate_name_is_refused(self):
        self.manifest.write_text(f"{self.sha}  README.md\n{self.sha}  README.md\n")
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, self.manifest, "README.md")

    def test_malformed_digest_is_refused(self):
        self.manifest.write_text("invalid  README.md\n")
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, self.manifest, "README.md")

    def test_traversal_is_refused(self):
        self.manifest.write_text(f"{self.sha}  ../README.md\n")
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, self.manifest, "../README.md")

    def test_absolute_path_is_refused(self):
        self.manifest.write_text(f"{self.sha}  {self.target}\n")
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, self.manifest, str(self.target))

    def test_symlinked_file_is_refused(self):
        other = self.lane / "authentic-copy.md"
        other.write_bytes(self.content)
        self.target.unlink()
        self.target.symlink_to(other)
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, self.manifest, "README.md")

    def test_undeclared_manifest_is_refused(self):
        unknown = self.root / "UNKNOWN_MANIFEST.sha256"
        unknown.write_text(f"{self.sha}  README.md\n")
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, unknown, "README.md")

    def test_undeclared_item_is_refused(self):
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, self.manifest, "OTHER.md")

    def test_mixed_base_local_entry_is_refused(self):
        self.manifest.write_text(f"{self.sha}  {LOCAL}/README.md\n")
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, self.manifest, f"{LOCAL}/README.md")

    def test_root_scoped_manifest_requires_explicit_prefix(self):
        lane = self.root / ROOTED
        lane.mkdir()
        target = lane / "THEOREM.md"
        target.write_bytes(self.content)
        manifest = lane / "MANIFEST.sha256"
        manifest.write_text(f"{self.sha}  {ROOTED}/THEOREM.md\n")
        self.assertEqual(resolve_manifest_item(self.root, manifest, f"{ROOTED}/THEOREM.md"), target)
        manifest.write_text(f"{self.sha}  THEOREM.md\n")
        with self.assertRaises(CustodyRefusal):
            resolve_manifest_item(self.root, manifest, "THEOREM.md")

    def test_original_authenticated_bytes_are_preserved(self):
        self.assertEqual(sha256(ORIGINAL.read_bytes()).hexdigest(),
                         "ac79663cd126b945bc022c95ba094f40addca4e28e3e24312f70ba9d0f15b77d")

    def test_original_check_payload_unchanged_except_resolver(self):
        def payload(path):
            text = path.read_text()
            body = text[text.index("checks: list"):]
            return re.sub(r"def resolve_manifest_item\(.*?\n\n\nfor relative in sorted",
                          "RESOLVER\n\nfor relative in sorted", body, count=1, flags=re.S)
        self.assertEqual(payload(ORIGINAL), payload(SUCCESSOR))

    def test_actual_successor_replays_all_original_checks(self):
        result = subprocess.run([sys.executable, "-B", str(SUCCESSOR)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("TOTAL 74/74 PASS", result.stdout)
        self.assertIn("NATURAL_UDCL_VALIDITY FALSIFIABLE_NOT_EXECUTABLY_PROVED", result.stdout)
        self.assertEqual(len(re.findall(r"^A\d+ PASS ", result.stdout, re.M)), 74)


if __name__ == "__main__":
    unittest.main(verbosity=2)
