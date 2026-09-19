#!/usr/bin/env python3

import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from durable_evidence import EvidenceError, canonical_json_bytes, immutable_write_bytes, immutable_write_json, load_json


class PersistenceTests(unittest.TestCase):
    def test_owner_once_is_idempotent_for_identical_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "record.json"
            first = immutable_write_json(path, {"answer": 42})
            second = immutable_write_json(path, {"answer": 42})
            self.assertEqual(first, second)
            self.assertEqual(load_json(path), {"answer": 42})
            self.assertFalse(path.stat().st_mode & stat.S_IWUSR)

    def test_owner_once_rejects_different_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "record.bin"
            immutable_write_bytes(path, b"first")
            with self.assertRaises(EvidenceError):
                immutable_write_bytes(path, b"second")

    def test_canonical_json_rejects_nan(self):
        with self.assertRaises(ValueError):
            canonical_json_bytes({"bad": float("nan")})


if __name__ == "__main__":
    unittest.main()

