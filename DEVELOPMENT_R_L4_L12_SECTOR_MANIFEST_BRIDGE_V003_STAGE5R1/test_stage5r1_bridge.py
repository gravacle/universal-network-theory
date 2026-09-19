#!/usr/bin/env python3
"""Focused regression tests for the Stage5R1 Decimal interface repair."""

from __future__ import annotations

import importlib.util
import unittest
from decimal import Decimal
from pathlib import Path


HERE = Path(__file__).resolve().parent
MODULE = HERE / "build_manifest_stage5r1.py"


def load_module():
    specification = importlib.util.spec_from_file_location("stage5r1", MODULE)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class Stage5R1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()
        cls.bridge = cls.module.load_module(
            cls.module.V003_BRIDGE, "frozen_v003_stage5_projection_test"
        )
        cls.builder = cls.bridge.load_predecessor()
        cls.source = {
            "target_sha256": cls.builder.sha256_file(
                cls.module.ROOT / cls.bridge.TARGET_L12
            ),
            "blind_sha256": cls.builder.sha256_file(
                cls.module.ROOT / cls.bridge.BLIND_L12
            ),
            "audit_sha256": cls.builder.sha256_file(
                cls.module.ROOT / cls.bridge.AUDIT_L12
            ),
        }
        cls.audit = cls.builder._load_history(
            cls.module.ROOT,
            cls.bridge.AUDIT_L12,
            cls.source["audit_sha256"],
            "Stage5R1 regression audit",
        )

    def test_original_validator_exposes_decimal_interface_bug(self) -> None:
        with self.assertRaisesRegex(
            self.builder.ManifestRefusal, "identity/result mismatch"
        ):
            self.bridge.validate_v003_l12_audit(
                self.audit, self.source, self.builder
            )

    def test_projection_passes_complete_original_validator(self) -> None:
        self.module.project_decimal_tolerance(
            self.audit,
            self.source,
            self.builder,
            self.bridge.validate_v003_l12_audit,
        )
        self.assertIs(type(self.audit["tolerance"]), Decimal)
        self.assertEqual(self.audit["tolerance"], Decimal("1e-8"))

    def test_projection_rejects_changed_exact_value(self) -> None:
        changed = dict(self.audit)
        changed["tolerance"] = Decimal("1.0000001e-8")
        with self.assertRaisesRegex(
            self.module.Stage5R1Refusal, "exact tolerance changed"
        ):
            self.module.project_decimal_tolerance(
                changed,
                self.source,
                self.builder,
                self.bridge.validate_v003_l12_audit,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
