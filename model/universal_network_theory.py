#!/usr/bin/env python3
"""Zero-input URM certificate for the Universal Network Theory closure.

This module composes four already bounded URM certificates and pins the master
closure theorem.  Composition preserves the proof type of every component:
U-DCL coverage is conditional on the adopted postulate, alpha inheritance is
conditional on a fixed governing domain and SAI/ACTVIS, the finite ARGER
result is an authenticated finite classification, and the Einstein response is
conditional on adopted RGRL and WTC-H1 through WTC-H5.  In particular, the
finite L4--L12 result does not directly imply the Einstein equation.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, NoReturn

import alpha_role as alpha
import gravity_formation_theory as gft
import relational_accumulation as relational
import udcl_postulate as udcl


SCHEMA = "WAC_UNIVERSAL_NETWORK_THEORY_CLOSURE_CERTIFICATE_V001"
THEOREM_ID = "UNT-CLOSURE-V001"
CLAIM_CLASS = (
    "EXACT_MASTER_TYPED_COMPOSITION_INSIDE_DECLARED_UNT_WORKING_SYSTEM__"
    "COMPONENT_PROOF_TYPES_AND_PREMISES_PRESERVED"
)
DISPOSITION = (
    "UNT_WORKING_THEORY_CLOSED_BY_TYPED_COMPOSITION__RFT_COVERAGE__"
    "DOMAIN_ALPHA_REQUIREMENT__FINITE_GFT_Z1__"
    "RECORD_CONDITIONED_GEOMETRY__CONDITIONAL_EINSTEIN_RESPONSE"
)

THEOREM_PATH = "UNIVERSAL_NETWORK_THEORY_CLOSURE_THEOREM_V001.md"
THEOREM_SHA256 = "39cd16d9dfb38b0335ffae45339ec6491da5806d86c98f3cc4cb9db69824bd75"

_REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
_WTC_PREMISES = (
    "WTC_H1_ADOPTED_RGRL_A_THROUGH_C",
    "WTC_H2_QUALIFIED_OBSERVABLE_MEMORY_REALIZATION",
    "WTC_H3_COMPLETE_SAME_METRIC_LEADING_RESPONSE_CLASS",
    "WTC_H4_COMPLETE_WARD_STATIONARITY_AND_CONSTRAINT_CUSTODY",
    "WTC_H5_GUARDED_ACTUAL_WORLD_ENDPOINT_MATCHING",
)
_THEOREM_MARKERS = (
    "# Universal Network Theory Closure Theorem",
    f"**Theorem ID:** `{THEOREM_ID}`",
    DISPOSITION,
    "Coverage-U for whichever admissible actual record is supplied by the parent\n"
    "physical dynamics.",
    "every `ACTVIS` record in that typed governing domain.",
    "The finite Gate classification and the conditional thermodynamic exponent are\n"
    "two complete, separately typed results.",
    "The finite Gate classification and the infrared response theorem are independent\n"
    "completed layers of GFT.",
    "No implication from a finite ARGER Gate pass to satisfaction of RGRL or\n"
    "`WTC-H1` through `WTC-H5` is claimed.",
    "Separately, under adopted RGRL and `WTC-H1` through `WTC-H5`, GFT\n"
    "derives the conditional macroscopic reciprocal Einstein response",
)


class UniversalNetworkTheoryRefusal(RuntimeError):
    """The master theorem or one of its typed component certificates failed."""


def _refuse(message: str) -> NoReturn:
    raise UniversalNetworkTheoryRefusal("UNIVERSAL NETWORK THEORY REFUSES: " + message)


def _expect(condition: bool, message: str) -> None:
    if not condition:
        _refuse(message)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _load_theorem() -> str:
    path = _REPOSITORY_ROOT / THEOREM_PATH
    try:
        if not path.is_file() or path.is_symlink():
            _refuse("closure theorem is absent, non-file, or symlinked")
        payload = path.read_bytes()
    except OSError as exc:
        _refuse(f"closure theorem is unreadable: {exc}")
    if _sha256_bytes(payload) != THEOREM_SHA256:
        _refuse("closure theorem SHA-256 mismatch")
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        _refuse(f"closure theorem is not UTF-8: {exc}")
    if "\r" in text or "\x00" in text:
        _refuse("closure theorem contains forbidden carriage-return or NUL bytes")
    for marker in _THEOREM_MARKERS:
        if marker not in text:
            _refuse(f"closure theorem required marker is absent: {marker}")
    return text


def _verify_components() -> tuple[
    Mapping[str, Any],
    Mapping[str, Any],
    Mapping[str, Any],
    Mapping[str, Any],
]:
    try:
        udcl_certificate = udcl.udcl_postulate_certificate()
        alpha_certificate = alpha.alpha_role_certificate()
        relational_certificate = relational.relational_accumulation_certificate()
        gft_certificate = gft.gravity_formation_theory_certificate()
    except (
        udcl.UDCLPostulateRefusal,
        alpha.AlphaRoleRefusal,
        relational.RelationalAccumulationRefusal,
        gft.GravityFormationTheoryRefusal,
    ) as exc:
        _refuse(f"typed component certificate failed: {exc}")

    _expect(udcl_certificate["schema"] == udcl.SCHEMA, "U-DCL schema changed")
    _expect(
        udcl_certificate["exact_results"]["universal"]
        == "UDCL_IMPLIES_ALL_DOMAIN_RECORDS_HAVE_COVERAGE_U",
        "U-DCL Coverage-U conclusion changed",
    )
    _expect(
        udcl_certificate["exact_results"]["theorem_status"]
        == "EXACT_CONDITIONAL_ON_ADOPTED_POSTULATE",
        "U-DCL proof type changed",
    )
    _expect(
        udcl_certificate["scientific_status"]["nature_obeys_UDCL"]
        == "NOT_ESTABLISHED_BY_THIS_CERTIFICATE",
        "U-DCL natural-validity ceiling changed",
    )
    _expect(
        udcl_certificate["nonconsequences"]["objective_actualization"] is False
        and udcl_certificate["nonconsequences"]["outcome_selection_or_forcing"]
        is False,
        "RFT/U-DCL was promoted to outcome actualization or selection",
    )

    _expect(alpha_certificate["schema"] == alpha.SCHEMA, "alpha schema changed")
    _expect(
        alpha_certificate["ALLOW"]["status"]
        == "PROVED_EXACT_ACTIVE_EM_CONSTRUCTION_INTERVAL_AND_NONSINGLETON",
        "alpha ALLOW proof type changed",
    )
    _expect(
        alpha_certificate["REQUIRE"]["status"]
        == "PROVED_EXACT_CONDITIONAL_GOVERNING_DOMAIN_ALPHA_REQUIREMENT",
        "alpha REQUIRE proof type changed",
    )
    _expect(alpha_certificate["SELECT"]["status"] == "OPEN", "alpha SELECT ceiling changed")

    _expect(
        relational_certificate["schema"] == relational.SCHEMA,
        "relational-accumulation schema changed",
    )
    gate = relational_certificate["governing_arger_gate"]
    _expect(
        gate["decision"] == "PASS_FINITE_DISCRETE_GFT_Z1_L4_L12",
        "finite ARGER decision changed",
    )
    _expect(
        relational_certificate["gravity_formation_boundary"]
        ["conditional_rgrl_wtc_infrared_response"]
        == "SEPARATE_EXISTING_GFT_LAYER_UNCHANGED",
        "finite and infrared GFT layers are no longer separate",
    )
    _expect(
        relational_certificate["gravity_formation_boundary"]
        ["continuum_einstein_or_empirical_gravity_from_this_gate"] is False,
        "finite ARGER Gate was promoted to Einstein or empirical gravity",
    )
    _expect(
        relational_certificate["dynamic_z1"]["same_model_ll_p"]["status"]
        == "CONDITIONAL_PHYSICAL_THEOREM",
        "LL-P dynamical-z=1 proof type changed",
    )
    _expect(
        relational_certificate["dynamic_z1"]["finite_arger_gate_is_dynamic_exponent_proof"]
        is False,
        "finite ARGER Gate was promoted to a dynamical-exponent proof",
    )

    _expect(gft_certificate["schema"] == gft.SCHEMA, "GFT schema changed")
    closure = gft_certificate["conditional_closure"]
    _expect(
        closure["status"] == "EXACT_AXIOMATIC_WORKING_THEORY_CLOSURE",
        "RGRL/WTC response proof type changed",
    )
    _expect(closure["premises"] == _WTC_PREMISES, "WTC premise set changed")
    _expect(
        gft_certificate["scientific_status"]["nature_obeys_RGRL"]
        == "NOT_ESTABLISHED_BY_THIS_CERTIFICATE",
        "RGRL empirical ceiling changed",
    )
    _expect(
        gft_certificate["scientific_status"]["numerical_G_from_record_variables"]
        == "OPEN_NOT_DERIVED",
        "numerical-G ceiling changed",
    )
    _expect(
        gft_certificate["exact_results"]["causal_volume_metric"]
        == "EXACT_INSIDE_ADOPTED_RGRL_A",
        "record-conditioned four-dimensional geometry result changed",
    )
    _expect(
        gft_certificate["exact_results"]["six_mode_lineage_ancestry"]
        == "EXACT_INSIDE_ADOPTED_RGRL_B_C",
        "local spatial metric-deformation ancestry result changed",
    )

    return (
        udcl_certificate,
        alpha_certificate,
        relational_certificate,
        gft_certificate,
    )


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _certificate() -> Mapping[str, Any]:
    _load_theorem()
    udcl_certificate, alpha_certificate, relational_certificate, gft_certificate = (
        _verify_components()
    )
    gate = relational_certificate["governing_arger_gate"]
    dynamic = relational_certificate["dynamic_z1"]["same_model_ll_p"]
    response = gft_certificate["conditional_closure"]

    return _freeze(
        {
            "schema": SCHEMA,
            "theorem_id": THEOREM_ID,
            "claim_class": CLAIM_CLASS,
            "disposition": DISPOSITION,
            "custody": {
                "theorem_path": THEOREM_PATH,
                "theorem_sha256": THEOREM_SHA256,
                "component_schemas": {
                    "universal_record_coverage": udcl_certificate["schema"],
                    "domain_alpha_requirement": alpha_certificate["schema"],
                    "finite_gravity_formation": relational_certificate["schema"],
                    "conditional_gravitational_response": gft_certificate["schema"],
                },
            },
            "typed_composition": {
                "operator": "EXACT_TYPED_CONJUNCTION_WITHOUT_PROOF_TYPE_PROMOTION",
                "universal_record_coverage": {
                    "proof_type": "EXACT_CONDITIONAL_ON_ADOPTED_UDCL_POSTULATE",
                    "domain": udcl_certificate["postulate"]["domain"],
                    "conclusion": udcl_certificate["exact_results"]["universal"],
                    "natural_udcl_validity_established": False,
                },
                "domain_alpha_requirement": {
                    "allow_proof_type": alpha_certificate["ALLOW"]["status"],
                    "allow_interval": alpha_certificate["ALLOW"]
                    ["construction_scoped_interval"]["set"],
                    "require_proof_type": alpha_certificate["REQUIRE"]["status"],
                    "governing_domain_precondition": alpha_certificate["REQUIRE"]
                    ["governing_domain_precondition"],
                    "record_precondition": alpha_certificate["REQUIRE"]["record_precondition"],
                    "conclusion": alpha_certificate["REQUIRE"]["conclusion"],
                    "select_status": alpha_certificate["SELECT"]["status"],
                },
                "finite_gravity_formation": {
                    "proof_type": "AUTHENTICATED_FINITE_RESULT_UNDER_ADOPTED_ARGER_GATE",
                    "gate_id": gate["gate_id"],
                    "classified_object": gate["classified_object"],
                    "finite_sizes": gate["finite_sizes"],
                    "unique_selected_sector_count": gate["finite_visibility"]
                    ["unique_sector_count"],
                    "minimum_R_low": gate["finite_visibility"]["minimum_R_low"],
                    "decision": gate["decision"],
                    "finite_gate_proof_obligation": relational_certificate
                    ["gravity_formation_boundary"]["finite_gate_proof_obligation"],
                    "continuum_or_einstein_gravity_from_finite_gate": False,
                },
                "conditional_dynamic_z1": {
                    "proof_type": dynamic["status"],
                    "premise_id": dynamic["premise_id"],
                    "density_interval": dynamic["density_interval"],
                    "conclusion": dynamic["conclusion"],
                    "independent_of_finite_arger_gate_decision": dynamic
                    ["independent_of_finite_arger_gate_decision"],
                },
                "record_conditioned_geometry_and_response": {
                    "proof_type": "EXACT_CONDITIONAL_WORKING_THEORY_IMPLICATION",
                    "rgrl_status": gft_certificate["rgrl"]["status"],
                    "rgrl_clauses": gft_certificate["rgrl"]["clauses"],
                    "four_dimensional_record_conditioned_geometry": gft_certificate
                    ["exact_results"]["causal_volume_metric"],
                    "complete_local_spatial_metric_deformation_ancestry": gft_certificate
                    ["exact_results"]["six_mode_lineage_ancestry"],
                    "metric_deformation_ancestry_kind": gft_certificate
                    ["exact_results"]["six_mode_ancestry_kind"],
                    "wtc_premises": response["premises"],
                    "response_status": response["status"],
                    "common_physical_metric": response["common_physical_metric"],
                    "leading_nonlinear_Einstein_response": response
                    ["leading_nonlinear_Einstein_response"],
                    "observed_G_endpoint": response["observed_G_endpoint"],
                    "nature_obeys_RGRL_established": False,
                    "parameter_free_numerical_G_derived": False,
                },
            },
            "type_boundary": {
                "finite_arger_and_rgrl_wtc_are_separately_typed": True,
                "finite_arger_gate_discharges_all_rgrl_wtc_premises": False,
                "l12_finite_gate_directly_implies_einstein_equation": False,
                "conditional_response_requires_declared_rgrl_wtc_premises": True,
                "composition_adds_new_physical_premise": False,
                "composition_changes_component_proof_status": False,
            },
            "claim_ceilings": {
                "natural_udcl_validity": False,
                "governing_domain_or_alpha_selected": False,
                "finite_gate_is_asymptotic_dynamic_z1_proof": False,
                "finite_l12_directly_derives_einstein_equation": False,
                "rgrl_empirically_confirmed": False,
                "wtc_premises_derived_from_l12": False,
                "microscopic_f3_derives_rgrl_b": False,
                "parameter_free_numerical_G": False,
                "l14_scientific_result": False,
            },
            "executable_scope": {
                "caller_arguments": 0,
                "physics_recalculated": False,
                "empirical_test_performed": False,
                "new_deduction_beyond_pinned_typed_composition": False,
                "scientific_output": "PINNED_TYPED_COMPOSITION_CERTIFICATE_ONLY",
            },
        }
    )


@dataclass(frozen=True)
class UniversalNetworkTheory:
    """Immutable handle for the pinned UNT master typed composition."""

    @property
    def claim_class(self) -> str:
        return CLAIM_CLASS

    @property
    def theorem_sha256(self) -> str:
        return THEOREM_SHA256

    def certificate(self) -> Mapping[str, Any]:
        """Verify every component afresh and return an immutable certificate."""
        return _certificate()


def universal_network_theory() -> UniversalNetworkTheory:
    """Verify the master theorem and typed components with zero caller input."""
    _load_theorem()
    _verify_components()
    return UniversalNetworkTheory()


def universal_network_theory_certificate() -> Mapping[str, Any]:
    """Return the immutable zero-input UNT closure certificate."""
    return universal_network_theory().certificate()
