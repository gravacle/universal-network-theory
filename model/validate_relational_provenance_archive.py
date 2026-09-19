#!/usr/bin/env python3
"""Validate the segregated, non-governing relational provenance archive."""

from __future__ import annotations

from decimal import Decimal
import hashlib
import inspect
from types import MappingProxyType

import relational_accumulation as current
import relational_accumulation_historical as archive


passed = 0


def check(condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError("relational provenance archive validation failed")
    passed += 1


def refused(callable_object) -> bool:
    try:
        callable_object()
    except current.RelationalAccumulationRefusal:
        return True
    return False


def main() -> int:
    check(tuple(inspect.signature(
        archive.historical_stage6_provenance
    ).parameters) == ())
    check(tuple(inspect.signature(
        archive.historical_stage6_provenance_certificate
    ).parameters) == ())

    handle = archive.historical_stage6_provenance()
    certificate = handle.certificate()
    second = archive.historical_stage6_provenance_certificate()
    check(handle.role == "OPTIONAL_HISTORICAL_PROVENANCE_ONLY")
    check(certificate == second and certificate is not second)
    check(isinstance(certificate, MappingProxyType))
    check(certificate["schema"] == archive.SCHEMA)
    check(certificate["role"] == "OPTIONAL_HISTORICAL_PROVENANCE_ONLY")
    check(certificate["governing_certificate_input"] is False)
    check(certificate["scientific_effect"] == "NONE__HISTORICAL_PROVENANCE_ONLY")

    json_pins = current._GOVERNING_ARTIFACTS + archive._ARTIFACTS
    rows = certificate["custody"]["artifacts"]
    check(certificate["custody"]["artifact_count"] == len(json_pins) + 1)
    check(tuple(row["label"] for row in rows) ==
          tuple(pin.label for pin in json_pins) +
          ("lower_bound_progression_extractor",))
    for pin, row in zip(json_pins, rows):
        path = current._root_path(pin.path)
        check(path.is_file() and not path.is_symlink())
        check(hashlib.sha256(path.read_bytes()).hexdigest() == pin.sha256)
        check(row["path"] == pin.path and row["sha256"] == pin.sha256)

    stage4 = certificate["stage4_projection"]
    check(stage4["schema_projection_only"] is True)
    check(stage4["physics_changed"] is False)
    check(stage4["numerical_data_changed"] is False)
    stage5 = certificate["stage5_manifest_provenance"]
    check(stage5["status"] == "PASS_AUTHENTICATED_STAGE5_MANIFEST")
    check(stage5["manifest_sector_count"] == 24)

    stage6 = certificate["stage6r2"]
    check(stage6["classification"] == "AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12")
    check(stage6["role"] == "HISTORICAL_PROVENANCE_ATOMWISE_CONJUNCTION")
    check(stage6["retroactively_modified"] is False)
    check(stage6["stage7_authorized"] is False)
    check(stage6["individually_passing_atoms"] == ("A020", "A021"))

    flow = certificate["record_flow_sidecar"]
    check(flow["deduplicated_q4_q5_q6_mass"] == "0.56956498393327842")
    check(flow["arithmetic_threshold_crossed"] is True)
    check(flow["stage6r2_modified"] is False)
    check(flow["stage6_override_authorized"] is False)
    check(flow["stage7_authorized"] is False)

    stage6r3 = certificate["stage6r3"]
    endpoint = Decimal(stage6r3["q4_plus_q6_endpoint_mass_decimal"])
    required = Decimal(stage6r3["required_q5_mass_decimal"])
    check(endpoint == Decimal("0.36652893665484882"))
    check(required == Decimal("0.13347106334515118"))
    check(Decimal("0.5") - endpoint == required)
    check(stage6r3["common_lineage_intersection_authenticated"] is False)
    check(stage6r3["stage7_authorized"] is False)

    lineage = certificate["lineage_support"]
    check(lineage["target"] == 0.11570852222694002)
    check(lineage["hostile"] == 0.11570852222694036)
    check(lineage["conservative"] == 0.11570852222694002)
    check(lineage["required"] == 0.1334710633451512)
    check(lineage["shortfall"] == 0.01776254111821117)
    check(lineage["threshold_cleared"] is False)

    progression = certificate["lower_bound_progression"]
    check(progression["strictly_increasing_through_l12"] is True)
    check(progression["fit_performed"] is False)
    check(progression["l14_value_inferred"] is False)
    check(certificate["earlier_same_slice_l14"][
        "satisfies_current_l14_seam"
    ] is False)

    original_load_json = current._load_json
    blocked_labels = {pin.label for pin in archive._ARTIFACTS}

    def unavailable_archive(pin):
        if pin.label in blocked_labels:
            current._refuse(f"simulated unavailable archive artifact: {pin.label}")
        return original_load_json(pin)

    try:
        current._load_json = unavailable_archive
        check(refused(archive.historical_stage6_provenance_certificate))
    finally:
        current._load_json = original_load_json

    print(f"RELATIONAL_PROVENANCE_ARCHIVE: PASS ({passed} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
