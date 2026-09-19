#!/usr/bin/env python3
"""Optional Git-only provenance for superseded relational adjudications.

This module is deliberately outside the governing URM and reproduction
capsule.  It preserves replayable custody for prior Stage-4--Stage-6
adjudications without making any of them an input to the ARGER Gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Mapping

import relational_accumulation as current


SCHEMA = "WAC_RELATIONAL_HISTORICAL_STAGE6_PROVENANCE_V001"

_ARTIFACTS = (
    current._ArtifactPin(
        "stage4",
        "AUDIT_R_L12_NUMERICAL_REPAIR_V003_STAGE4R1/STAGE4R1_EXECUTION_RECORD.json",
        "d6a19729482e29f686247c025e651357af5ff2515e4bd1d53c20e88edec94a23",
        (
            ("schema", "L12_V003R1_STAGE4R1_EXECUTION_RECORD_V001"),
            ("status", "PASS_EXACT_STAGE4_ADJUDICATION"),
        ),
    ),
    current._ArtifactPin(
        "stage5",
        (
            "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003_STAGE5R1/"
            "STAGE5R1_EXECUTION_RECORD.json"
        ),
        "52391568ac35cdb96e524205a65bc6b34b38e89ba1b4bf342caa7b5b997db9b6",
        (
            ("schema", "L12_V003R1_STAGE5R1_EXECUTION_RECORD_V001"),
            ("status", "PASS_AUTHENTICATED_STAGE5_MANIFEST"),
        ),
    ),
    current._ArtifactPin(
        "stage6r2",
        (
            "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/"
            "ADJUDICATION_V002_L12_V003R1_STAGE6R2.json"
        ),
        "43c7c19daaf24902d2699c337851eca35a03c3db69f8e3f55f3b0142f87e137d",
        (
            ("schema", "RELATIONAL_INTERVAL_SPECTRUM_ADJUDICATION_V001"),
            ("classification", "AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12"),
        ),
    ),
    current._ArtifactPin(
        "stage6r2_execution",
        (
            "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_COMPATIBILITY_V001_STAGE6R2/"
            "STAGE6R2_EXECUTION_RECORD.json"
        ),
        "0173dfe264b3d4f4ec146033c9de8c764a012f5a5bebb4e0b089ebb1b902afbd",
        (
            ("schema", "L12_V003R1_STAGE6R2_EXECUTION_RECORD_V001"),
            ("status", "COMPLETE__PAUSED_BEFORE_STAGE7"),
        ),
    ),
    current._ArtifactPin(
        "record_flow",
        (
            "DEVELOPMENT_R_L12_RECORD_FLOW_BRIDGE_V001/"
            "RECORD_FLOW_BRIDGE_REPORT_V001.json"
        ),
        "4a02db3eaea066a4c65bce921fcfaaffcc7e731b057d06f4c50180b6e38b40a6",
        (
            ("schema", "L12_AUTHENTICATED_RECORD_FLOW_BRIDGE_V001"),
            ("status", "PASS"),
            ("classification", "AUTHENTICATED_L12_RECORD_FLOW_SECTOR_BRIDGE"),
        ),
    ),
    current._ArtifactPin(
        "stage6r3",
        (
            "DEVELOPMENT_R_L12_STAGE6R3_RECORD_FLOW_ADJUDICATION_V001/"
            "STAGE6R3_SUPPLEMENTAL_ADJUDICATION_V001.json"
        ),
        "7fa2062f18be3c90c9167e917974d1cc609273da623966e4068f1c0d1133e2b4",
        (
            ("schema", "L12_STAGE6R3_RECORD_FLOW_SUPPLEMENTAL_ADJUDICATION_V001"),
            (
                "classification",
                "STAGE6R3_RECORD_FLOW_OBSERVED__ORIGINAL_Z1_GATE_REMAINS_REJECTED",
            ),
            ("status", "COMPLETE_FAIL_CLOSED_SUPPLEMENTAL_ADJUDICATION"),
        ),
    ),
    current._ArtifactPin(
        "lineage_support",
        (
            "DEVELOPMENT_R_L12_LINEAGE_RESOLVED_SUPPORT_V001/"
            "LINEAGE_RESOLVED_SUPPORT_REPORT_V001.json"
        ),
        "182a78f3ef11c72d5089a488e85cb9f91e842f1950d3d5a474f7678bfd23ca08",
        (
            ("schema", "L12_LINEAGE_RESOLVED_SUPPORT_RECONSTRUCTION_V001"),
            (
                "classification",
                "LINEAGE_RESOLVED_Q5_SUPPORT_BELOW_REQUIRED_THRESHOLD",
            ),
            ("status", "COMPLETE__READ_ONLY_RECONSTRUCTION"),
        ),
    ),
    current._ArtifactPin(
        "earlier_same_slice_l14",
        "DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001/RESULT.json",
        "8a69f780a372ae436ef2fe458af80f7fa1ba70d8c93b21d91524c6e9819d753d",
        (
            ("schema", "R_CONNECTED_RECORD_TRAJECTORY_L4_L14_V001"),
            (
                "classification",
                "HOSTILE_AUDITED_INPUT_APPEND__FINITE_RAW_RECORD_TRAJECTORY",
            ),
        ),
    ),
)


def _verify_evidence() -> dict[str, dict[str, Any]]:
    """Verify the optional, non-governing Stage-4--Stage-6 chain."""
    current._verify_progression_source()
    json_pins = current._GOVERNING_ARTIFACTS + _ARTIFACTS
    evidence = {pin.label: current._load_json(pin) for pin in json_pins}
    pins = {pin.label: pin for pin in json_pins}
    current._verify_current_base(evidence)

    exact = evidence["exact_l12"]
    current._expect(
        exact.get("target_history_sha256")
        == "079499e7b989e1ba45b1c397882c8638106be149ccb994058a3703b235736764"
        and exact.get("hostile_history_sha256")
        == "cbac18fd5033f83e4eadbfb16b46c89584455987e0b75fa6a33a33821246851c"
        and exact.get("blind_history_sha256")
        == "e95a40bb24a9d997c9ecf639799263cf14cdb5d52171e9c24fe7fbcedbfcc1cb",
        "exact L12 archived identities changed",
    )

    stage4 = evidence["stage4"]
    current._expect(
        stage4.get("exact_adjudication_sha256") == pins["exact_l12"].sha256,
        "Stage-4R1 does not bind exact L12",
    )
    current._expect(
        stage4.get("schema_projection_only") is True
        and stage4.get("physics_changed") is False
        and stage4.get("numerical_data_changed") is False,
        "Stage-4R1 ceased to be a schema-only projection",
    )

    stage5 = evidence["stage5"]
    current._expect(
        stage5.get("manifest_sha256") == pins["manifest"].sha256,
        "Stage-5 record does not bind its manifest",
    )
    current._expect(
        stage5.get("stage4_exact_adjudication_sha256") == pins["exact_l12"].sha256,
        "Stage-5 record does not bind exact L12",
    )
    current._expect(
        stage5.get("manifest_sector_count") == 24
        and stage5.get("manifest_status")
        == "PASS_RELATIONAL_ACCUMULATION_L4_L12__SPECTRUM_MANIFEST_READY",
        "Stage-5 authenticated manifest status changed",
    )

    stage6 = evidence["stage6r2"]
    current._expect(
        stage6.get("manifest_sha256") == pins["manifest"].sha256,
        "Stage-6R2 does not bind the Stage-5 manifest",
    )
    current._expect(
        len(stage6.get("atom_results", ())) == 24,
        "Stage-6R2 atom adjudication count changed",
    )
    for index, atom_id in ((20, "A020"), (21, "A021")):
        row = stage6["atom_results"][index]
        current._expect(
            row.get("atom", {}).get("atom_id") == atom_id
            and row.get("passes") is True
            and row.get("target_classification", {}).get("passes") is True
            and row.get("blind_classification", {}).get("passes") is True,
            f"Stage-6R2 individual {atom_id} status changed",
        )
    components = stage6.get("passing_components", ())
    current._expect(
        len(components) == 1
        and components[0].get("atom_indices") == [20, 21]
        and components[0].get("qualifies") is False,
        "Stage-6R2 component rejection changed",
    )

    stage6_execution = evidence["stage6r2_execution"]
    current._expect(
        stage6_execution.get("stage6_result_sha256") == pins["stage6r2"].sha256,
        "Stage-6R2 execution record does not bind adjudication",
    )
    current._expect(
        stage6_execution.get("stage6_classification")
        == "AUTHENTICATED_RELATIONAL_Z1_REJECTED_L4_L12"
        and stage6_execution.get("stage7_started") is False,
        "Stage-6R2 execution boundary changed",
    )

    flow = evidence["record_flow"]
    flow_inputs = {
        row.get("label"): row.get("sha256")
        for row in flow.get("authenticated_json_inputs", ())
    }
    current._expect(
        flow_inputs.get("stage6_adjudication") == pins["stage6r2"].sha256
        and flow_inputs.get("stage5_manifest") == pins["manifest"].sha256,
        "record-flow sidecar does not bind Stage 5 and Stage 6R2",
    )
    current._expect(
        flow.get("conclusion", {}).get("stage6_frozen_result_modified") is False
        and "NOT_PHYSICAL_VERTEX_OR_STATIC_ATOM_ADJACENCY"
        in flow.get("claim_boundary", "")
        and "NO_RETROACTIVE_STAGE6_OVERRIDE" in flow.get("claim_boundary", ""),
        "record-flow typed non-override boundary changed",
    )

    stage6r3 = evidence["stage6r3"]
    stage6r3_inputs = {
        row.get("label"): row.get("sha256")
        for row in stage6r3.get("authenticated_inputs", ())
    }
    current._expect(
        stage6r3_inputs.get("stage6r2") == pins["stage6r2"].sha256
        and stage6r3_inputs.get("flow_report") == pins["record_flow"].sha256,
        "Stage-6R3 does not bind Stage-6R2 and record flow",
    )
    current._expect(
        stage6r3.get("predecessor", {}).get("modified") is False
        and stage6r3.get("stage7_gate", {}).get("authorized") is False,
        "Stage-6R3 changed its predecessor or authorized Stage 7",
    )
    shared = stage6r3.get("aggregation_rules", {}).get("shared_arithmetic", {})
    endpoint = Decimal(shared.get("q4_plus_q6_endpoint_sector_mass", "NaN"))
    required = Decimal(shared.get("additional_q5_mass_required_for_0_50", "NaN"))
    current._expect(
        Decimal("0.5") - endpoint == required == Decimal("0.13347106334515118"),
        "Stage-6R3 exact threshold arithmetic changed",
    )

    lineage = evidence["lineage_support"]
    current._expect(
        lineage.get("prior_artifacts_mutated") is False
        and lineage.get("stage7_started") is False,
        "lineage reconstruction mutated archived evidence or started Stage 7",
    )
    lineage_docs = lineage.get("authenticated_documents", {})
    current._expect(
        lineage_docs.get("flow", {}).get("sha256") == pins["record_flow"].sha256
        and lineage_docs.get("stage6", {}).get("sha256") == pins["stage6r2"].sha256
        and lineage_docs.get("stage6r3", {}).get("sha256")
        == pins["stage6r3"].sha256
        and lineage_docs.get("manifest", {}).get("sha256") == pins["manifest"].sha256,
        "lineage reconstruction custody chain changed",
    )
    threshold = lineage.get("threshold_adjudication", {})
    current._expect(
        lineage.get("target", {}).get("strict_common_lineage_pbar_support")
        == 0.11570852222694002
        and lineage.get("hostile", {}).get("strict_common_lineage_pbar_support")
        == 0.11570852222694036
        and threshold.get("conservative_support") == 0.11570852222694002
        and threshold.get("threshold_cleared") is False,
        "lineage support adjudication changed",
    )
    progression = dict(
        (label, value) for label, value, _ in current._LOWER_BOUND_PROGRESSION
    )
    current._expect(
        progression["L12_TARGET"]
        == lineage["target"]["strict_common_lineage_pbar_support"]
        and progression["L12_HOSTILE"]
        == lineage["hostile"]["strict_common_lineage_pbar_support"]
        and progression["L12_CONSERVATIVE"] == threshold["conservative_support"],
        "lower-bound progression no longer binds the L12 adjudication",
    )
    current._expect(
        progression["L08"] < progression["L10"] < progression["L12_CONSERVATIVE"],
        "declared L08/L10/L12 progression is not strictly increasing",
    )

    earlier = evidence["earlier_same_slice_l14"]
    current._expect(
        any(row.get("L") == 14 for row in earlier.get("rows", ())),
        "earlier same-slice trajectory lost its L14 row",
    )
    current._expect(
        "NO_FIT_OR_EXTRAPOLATION" in earlier.get("scope", "")
        and "GRAVITY" in earlier.get("not_claimed", ""),
        "earlier same-slice L14 ceiling changed",
    )
    return evidence


def _certificate(evidence: dict[str, dict[str, Any]]) -> Mapping[str, Any]:
    stage4 = evidence["stage4"]
    stage5 = evidence["stage5"]
    stage6 = evidence["stage6r2"]
    stage6_execution = evidence["stage6r2_execution"]
    component = stage6["passing_components"][0]
    flow = evidence["record_flow"]
    stage6r3 = evidence["stage6r3"]
    lineage = evidence["lineage_support"]
    threshold = lineage["threshold_adjudication"]
    earlier = evidence["earlier_same_slice_l14"]
    shared = stage6r3["aggregation_rules"]["shared_arithmetic"]
    flow_edges = flow["typed_topology"]["certified_sector_flow_edges"]
    json_pins = current._GOVERNING_ARTIFACTS + _ARTIFACTS

    return current._freeze(
        {
            "schema": SCHEMA,
            "role": "OPTIONAL_HISTORICAL_PROVENANCE_ONLY",
            "governing_certificate_input": False,
            "custody": {
                "artifact_count": len(json_pins) + 1,
                "artifacts": tuple(
                    {
                        "label": pin.label,
                        "path": pin.path,
                        "sha256": pin.sha256,
                        "kind": "JSON",
                    }
                    for pin in json_pins
                )
                + (
                    {
                        "label": "lower_bound_progression_extractor",
                        "path": current._PROGRESSION_SOURCE_PATH,
                        "sha256": current._PROGRESSION_SOURCE_SHA256,
                        "kind": "SOURCE",
                    },
                ),
            },
            "stage4_projection": {
                "schema": stage4["schema"],
                "status": stage4["status"],
                "schema_projection_only": stage4["schema_projection_only"],
                "physics_changed": stage4["physics_changed"],
                "numerical_data_changed": stage4["numerical_data_changed"],
            },
            "stage5_manifest_provenance": {
                "schema": stage5["schema"],
                "status": stage5["status"],
                "manifest_status": stage5["manifest_status"],
                "manifest_sector_count": stage5["manifest_sector_count"],
            },
            "stage6r2": {
                "schema": stage6["schema"],
                "classification": stage6["classification"],
                "execution_status": stage6_execution["status"],
                "role": "HISTORICAL_PROVENANCE_ATOMWISE_CONJUNCTION",
                "retroactively_modified": False,
                "individually_passing_atoms": ("A020", "A021"),
                "component_atom_indices": component["atom_indices"],
                "component_mass_by_L": component["pbar_mass_by_L"],
                "component_qualifies": component["qualifies"],
                "stage7_authorized": False,
                "claim_boundary": stage6["claim_boundary"],
            },
            "record_flow_sidecar": {
                "schema": flow["schema"],
                "classification": flow["classification"],
                "status": flow["status"],
                "relation_type": "SEPARATELY_TYPED_RECORD_FLOW_DIAGNOSTIC",
                "q4_to_q5": {
                    "target": flow_edges[0]["target_transferred_norm_squared"],
                    "hostile": flow_edges[0]["hostile_transferred_norm_squared"],
                },
                "q5_to_q6": {
                    "target": flow_edges[1]["target_transferred_norm_squared"],
                    "hostile": flow_edges[1]["hostile_transferred_norm_squared"],
                },
                "deduplicated_q4_q5_q6_mass": flow["mass"]["deduplicated_q4_q5_q6"],
                "arithmetic_threshold_crossed": flow["mass"]["threshold_crossed"],
                "physical_vertex": False,
                "static_atom_adjacency": False,
                "entanglement_claim": False,
                "stage6r2_modified": False,
                "stage6_override_authorized": False,
                "stage7_authorized": False,
                "claim_boundary": flow["claim_boundary"],
            },
            "stage6r3": {
                "schema": stage6r3["schema"],
                "classification": stage6r3["classification"],
                "status": stage6r3["status"],
                "role": "HISTORICAL_PROVENANCE_SUPPLEMENTAL_ADJUDICATION",
                "q4_plus_q6_endpoint_mass_decimal":
                    shared["q4_plus_q6_endpoint_sector_mass"],
                "required_q5_mass_decimal":
                    shared["additional_q5_mass_required_for_0_50"],
                "common_lineage_intersection_authenticated": False,
                "stage7_authorized": False,
                "claim_boundary": stage6r3["claim_boundary"],
            },
            "lineage_support": {
                "schema": lineage["schema"],
                "classification": lineage["classification"],
                "status": lineage["status"],
                "role": "SEPARATE_STRICT_COMPLETED_COMMON_LINEAGE_DIAGNOSTIC",
                "target": lineage["target"]["strict_common_lineage_pbar_support"],
                "hostile": lineage["hostile"]["strict_common_lineage_pbar_support"],
                "conservative": threshold["conservative_support"],
                "required": threshold["required_q5_common_lineage_support"],
                "shortfall": threshold["shortfall"],
                "target_hostile_absolute_difference":
                    threshold["target_hostile_absolute_difference"],
                "threshold_cleared": threshold["threshold_cleared"],
                "measure": "DECLARED_FINITE_PBAR_Q_COMMON_LINEAGE_SUPPORT",
                "stage7_authorized": False,
                "claim_boundary": lineage["claim_boundary"],
            },
            "lower_bound_progression": {
                "source_path": current._PROGRESSION_SOURCE_PATH,
                "source_sha256": current._PROGRESSION_SOURCE_SHA256,
                "table": tuple(
                    {"scale": label, "support": value, "authority": authority}
                    for label, value, authority in current._LOWER_BOUND_PROGRESSION
                )
                + (
                    {
                        "scale": "L14",
                        "support": current.L14_STATUS,
                        "authority": (
                            "PRESERVED_INCOMPLETE_RUN__NO_L14_VALUE_OR_"
                            "SCIENTIFIC_ADJUDICATION"
                        ),
                    },
                ),
                "strictly_increasing_through_l12": True,
                "l08_l10_cache_trusted": True,
                "l08_l10_independent_hostile_reconstruction": False,
                "l12_independent_hostile_reconstruction": True,
                "fit_performed": False,
                "monotone_continuation_theorem": False,
                "asymptotic_extrapolation_theorem": False,
                "l14_value_inferred": False,
                "claim_boundary": (
                    "FINITE_DECLARED_EXTRACTION__NO_FIT_NO_FORECAST__"
                    "CACHE_TIER_IS_NOT_A_RELIABILITY_DISCOUNT"
                ),
            },
            "earlier_same_slice_l14": {
                "schema": earlier["schema"],
                "classification": earlier["classification"],
                "scope": earlier["scope"],
                "is_current_relational_scout": False,
                "satisfies_current_l14_seam": False,
                "reason": (
                    "FINITE_RAW_SAME_SLICE_TRAJECTORY_LACKS_CURRENT_OWNER_ONCE_"
                    "TARGET_HOSTILE_PHASE2_AND_FINAL_GATE_REPORT"
                ),
            },
            "scientific_effect": "NONE__HISTORICAL_PROVENANCE_ONLY",
        }
    )


@dataclass(frozen=True)
class HistoricalStage6Provenance:
    """Immutable handle for optional, non-governing provenance."""

    @property
    def role(self) -> str:
        return "OPTIONAL_HISTORICAL_PROVENANCE_ONLY"

    def certificate(self) -> Mapping[str, Any]:
        return _certificate(_verify_evidence())


def historical_stage6_provenance() -> HistoricalStage6Provenance:
    """Verify and expose the segregated Stage-4--Stage-6 archive."""
    _verify_evidence()
    return HistoricalStage6Provenance()


def historical_stage6_provenance_certificate() -> Mapping[str, Any]:
    """Return optional provenance with no governing effect."""
    return historical_stage6_provenance().certificate()
