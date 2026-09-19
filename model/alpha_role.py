#!/usr/bin/env python3
"""Zero-input URM certificate for the alpha ALLOW/REQUIRE/SELECT role.

The certificate keeps three different quantifiers separate.  The declared
finite construction ALLOWS an exact construction-scoped interval and therefore
a non-singleton set of domain alpha values.  Once governing-domain ancestry and
the comparison context are independently established, every ACTVIS record that
satisfies SAI1--SAI8 REQUIRES the governing domain's alpha value and RG
trajectory.  Alpha is constitutive domain identity.  A law that SELECTS the
governing domain or its numerical boundary value remains open.

This module authenticates existing theorem and hostile-audit text.  It accepts
no caller data, performs no empirical fit, does not derive 1/137, and makes no
gravity or numerical-G claim.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping, NoReturn


SCHEMA = "WAC_ALPHA_ALLOW_REQUIRE_SELECT_CERTIFICATE_V003"
CLAIM_CLASS = (
    "RFT_ALPHA_CONSTRUCTION_SCOPED_ALLOW_INTERVAL_EXACT__"
    "GOVERNING_DOMAIN_ALPHA_REQUIREMENT_EXACT_CONDITIONAL__"
    "DOMAIN_SELECTION_OPEN"
)
ROLE_ID = "A-AL2"
SOURCE_OFFICIAL_DISPOSITION = (
    "RFT_ALPHA_NONSELECTION_EXACT__"
    "ACTIVE_EM_RECORD_WORLD_NONSINGLETON_EXACT__"
    "EMPIRICALLY_ANCHORED_SAME_VISIBLE_U1_INHERITANCE_EXACT_CONDITIONAL__"
    "FULL_UNIVERSE_ALPHA_CARDINALITY_OPEN"
)
OFFICIAL_DISPOSITION = (
    "RFT_ALPHA_CONSTRUCTION_SCOPED_ALLOW_INTERVAL_EXACT__"
    "GOVERNING_DOMAIN_ALPHA_REQUIREMENT_EXACT_CONDITIONAL__"
    "DOMAIN_SELECTION_OPEN__"
    "FULL_UNIVERSE_ALPHA_CARDINALITY_OPEN"
)

_REPOSITORY_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class _TextPin:
    label: str
    path: str
    sha256: str
    required_markers: tuple[str, ...]
    kind: str = "AUTHORITATIVE_TEXT"


_TEXT_ARTIFACTS = (
    _TextPin(
        "sector_inheritance_theorem",
        "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/THEOREM.md",
        "71fbde2ac52a9f8e2c23fc873837e88e7a1513afc2dd801869b3ad41229fe9da",
        (
            "# Same-Sector Alpha Inheritance and Non-Embedding Theorem",
            "## 8. The alpha `ALLOW/REQUIRE/SELECT` ladder",
            "Thus present recordhood does not numerically select alpha",
            "Equation (20) is open.",
        ),
    ),
    _TextPin(
        "sector_inheritance_result",
        "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/RESULT.md",
        "08a839bcb87426a0227ba4fa031aa6d1bda1702ce30dddfd4b06b1733d80b7ce",
        (
            "# Executed result",
            SOURCE_OFFICIAL_DISPOSITION,
            "## `ALLOW/REQUIRE/SELECT` interpretation",
            "It is not a parameter-free calculation of the observed numeral",
        ),
    ),
    _TextPin(
        "active_em_interval_theorem",
        "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/ALTERNATIVE_RECORD_WORLD.md",
        "e0a53db328db825511932f8e8890b3f7b62b5b1823934e53464a10ee11d386bc",
        (
            "# Canonical-\\(U(1)\\) alternative-alpha record-world theorem",
            "\\alpha>{-\\ln(1-\\delta)\\over4\\pi B^2}",
            "{\\cal A}_{\\rm RF}^{\\rm EM,toy}(\\Pi;\\chi)",
            "These are mean-energy constraints, not hard energy-support cutoffs",
        ),
    ),
    _TextPin(
        "sector_inheritance_audit",
        "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/AUDIT.md",
        "22376484d6f1dd2ebbc07e8569a19bba32ec0dd7e95f6e5d7e8fc8a38a4cb725",
        (
            "# Hostile audit of same-sector alpha inheritance",
            "Every same-action subsystem inherits that coefficient",
            "Why nature realized that numerical value | Open.",
            "Repeated construction failure is not an exhaustive no-go.",
        ),
    ),
    _TextPin(
        "scope_theorem",
        "DEVELOPMENT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/FORMAL_SCOPE_THEOREM.md",
        "00cf12c9b9e3c3fd64b08264134eba2844d277e81313712c42ea010e991f0f23",
        (
            "# Formal scope theorem for `ALLOW`, `REQUIRE`, and `SELECT`",
            "`ALLOW` does not imply `REQUIRE`.",
            "`SELECT` does not imply `REQUIRE`",
            "The host-sector use of `REQUIRE` is therefore not a production operator.",
        ),
    ),
    _TextPin(
        "scope_theorem_hostile_audit",
        "AUDIT_ALLOW_REQUIRE_SCOPE_REPAIR_V001/INDEPENDENT_HOSTILE_AUDIT.md",
        "c2e9e09d85d461b1855a5bc77b953727e50998fc9fa0db4810cb1880efb7c405",
        (
            "PASS_HOSTILE_ALLOW_REQUIRE_SCOPE_REPAIR_V001",
            "mechanical contract: 300/300 PASS",
            "hostile semantic screen: 102/102 PASS",
            "No Gate B, continuum, Ward, graviton, Poincare/Virasoro, anomaly, emergence,\n"
            "or gravity promotion is made by this audit.",
        ),
    ),
    _TextPin(
        "active_em_algebraic_witness_verifier",
        "LANE_RFT_ALPHA_SECTOR_INHERITANCE_V001/verify_alpha_sector_inheritance.py",
        "bb7f52e135e2035c07f74d282457af9d73b75ff701ef7d2908e3e97e73cdac74",
        (
            "Algebraic witnesses for alpha nonselection, inheritance, and phase locking.",
            'check("first fixed-control cavity contrast is exactly 1/2"',
            'check("second fixed-control cavity contrast is exactly 15/16"',
            "physical REC/FCLPD premises are analytic, not executable certifications",
        ),
        "EXECUTABLE_ALGEBRAIC_WITNESS_REGRESSION",
    ),
)


class AlphaRoleRefusal(RuntimeError):
    """A pinned alpha-role artifact or exact scope predicate failed."""


def _refuse(message: str) -> NoReturn:
    raise AlphaRoleRefusal("ALPHA ROLE REFUSES: " + message)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _root_path(relative: str) -> Path:
    posix = PurePosixPath(relative)
    if posix.is_absolute() or not posix.parts or ".." in posix.parts:
        _refuse(f"unsafe custody path: {relative}")
    path = _REPOSITORY_ROOT.joinpath(*posix.parts)
    try:
        path.resolve(strict=False).relative_to(_REPOSITORY_ROOT.resolve())
    except (OSError, ValueError):
        _refuse(f"custody path escapes repository: {relative}")
    return path


def _load_text(pin: _TextPin) -> str:
    path = _root_path(pin.path)
    try:
        if not path.is_file() or path.is_symlink():
            _refuse(f"custody object is absent, non-file, or symlinked: {pin.path}")
        payload = path.read_bytes()
    except OSError as exc:
        _refuse(f"custody object is unreadable: {pin.path}: {exc}")
    if _sha256_bytes(payload) != pin.sha256:
        _refuse(f"SHA-256 mismatch: {pin.path}")
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        _refuse(f"custody object is not UTF-8: {pin.path}: {exc}")
    if "\r" in text or "\x00" in text:
        _refuse(f"custody object contains forbidden bytes: {pin.path}")
    for marker in pin.required_markers:
        if marker not in text:
            _refuse(f"required marker is absent from {pin.path}: {marker}")
    return text


def _expect(condition: bool, message: str) -> None:
    if not condition:
        _refuse(message)


def _verify_evidence() -> dict[str, str]:
    evidence = {pin.label: _load_text(pin) for pin in _TEXT_ARTIFACTS}
    theorem = evidence["sector_inheritance_theorem"]
    result = evidence["sector_inheritance_result"]
    interval_theorem = evidence["active_em_interval_theorem"]
    audit = evidence["sector_inheritance_audit"]
    scope = evidence["scope_theorem"]
    scope_audit = evidence["scope_theorem_hostile_audit"]

    _expect(
        "|{\\cal A}_{\\rm RF}^{\\rm EM,toy}|\\ge2" in theorem
        and "ACTIVE_EM_RECORD_WORLD_NONSINGLETON_EXACT" in result
        and "At least two fixed-control canonical-\\(U(1)\\) finite record worlds exist"
        in audit,
        "active-EM non-singleton ALLOW theorem changed",
    )
    _expect(
        "1-e^{-e^2B^2}>\\delta" in interval_theorem
        and "\\alpha>{-\\ln(1-\\delta)\\over4\\pi B^2}" in interval_theorem
        and "I_\\chi\\cap" in interval_theorem
        and "\\left({-\\ln(1-\\delta)\\over4\\pi B^2},\\infty\\right)"
        in interval_theorem,
        "active-EM exact ALLOW interval theorem changed",
    )
    _expect(
        "SAI1–SAI8" in theorem
        and "\\operatorname{ACTVIS}(r,W)" in theorem
        and "\\operatorname{REQUIRE}_{W}^{\\rm sameU1}" in theorem
        and "conditional inheritance by records with independently established"
        in result
        and "same-visible-\n\\(U(1)\\) ancestry" in result,
        "conditional same-sector REQUIRE theorem changed",
    )
    _expect(
        "\\operatorname{SELECT}_{\\rm parent}" in theorem
        and "allowed parent setting became actual" in theorem
        and "selector exists" in theorem
        and "`SELECT_parent` is an independent dynamical proposition" in scope,
        "open SELECT boundary changed",
    )
    _expect(
        "complete-universe numerical requirement would be a separately proved"
        in scope
        and "FULL_UNIVERSE_ALPHA_CARDINALITY_OPEN" in result
        and "Multiple complete realistic alpha-worlds contain ordinary records | Not proved"
        in audit,
        "complete-universe cardinality boundary changed",
    )
    _expect(
        "hostile semantic screen: 102/102 PASS" in scope_audit
        and "300/300 PASS" in scope_audit,
        "scope-repair hostile audit no longer passes",
    )
    return evidence


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _certificate() -> Mapping[str, Any]:
    return _freeze(
        {
            "schema": SCHEMA,
            "claim_class": CLAIM_CLASS,
            "role_id": ROLE_ID,
            "official_disposition": OFFICIAL_DISPOSITION,
            "custody": {
                "artifact_count": len(_TEXT_ARTIFACTS),
                "artifacts": tuple(
                    {
                        "label": pin.label,
                        "path": pin.path,
                        "sha256": pin.sha256,
                        "kind": pin.kind,
                    }
                    for pin in _TEXT_ARTIFACTS
                ),
            },
            "typed_vocabulary": {
                "ALLOW": "MEMBERSHIP_IN_DECLARED_DOMAIN_ATTAINABLE_SET",
                "REQUIRE": "DOMAIN_RELATIVE_UNIVERSAL_CONDITION",
                "SELECT": "SEPARATELY_SUPPLIED_DYNAMICAL_ACTUALIZATION_LAW",
            },
            "ALLOW": {
                "status": "PROVED_EXACT_ACTIVE_EM_CONSTRUCTION_INTERVAL_AND_NONSINGLETON",
                "domain": "FINITE_ACTIVE_EM_TOY_RECORD_WORLDS",
                "construction_scoped_interval": {
                    "status": "PROVED_EXACT_ANALYTIC_FOR_DECLARED_IDEAL_ACTIVE_EM_PACKET",
                    "set": "I_chi intersect ((-ln(1-delta))/(4*pi*B^2), infinity)",
                    "conditions": "B^2>0; 0<=delta<1; asserted alpha lies in I_chi",
                    "zero_floor_specialization": "I_chi intersect (0, infinity)",
                    "read_contrast": "1-exp(-4*pi*alpha*B^2)",
                    "optional_mean_energy_upper_bound":
                        "alpha<=E_max/(4*pi*hbar*omega*B^2)",
                    "complete_universe_interval_proved": False,
                    "gft_majority_gate": False,
                },
                "cardinality_lower_bound": 2,
                "witness_domain_alpha_values": ("9/(400*pi)", "9/(100*pi)"),
                "witness_read_contrasts": ("1/2", "15/16"),
                "fixed_controls": True,
                "alpha_vertex_load_bearing": True,
                "algebraic_witness_regression_checks": 41,
                "algebraic_witness_regression_proves_physical_premises": False,
                "complete_universe_nonsingleton_proved": False,
            },
            "REQUIRE": {
                "status": "PROVED_EXACT_CONDITIONAL_GOVERNING_DOMAIN_ALPHA_REQUIREMENT",
                "governing_domain_precondition":
                    "GOVERNING_DOMAIN_ANCESTRY_AND_ALPHA_VALUE_INDEPENDENTLY_ESTABLISHED",
                "record_precondition": "ACTVIS_AND_SAI1_THROUGH_SAI8",
                "conclusion":
                    "REQUIRE_GOVERNING_DOMAIN_ALPHA_AND_UNIQUE_RG_MATCHING_TRAJECTORY",
                "physical_interpretation":
                    "CONSTITUTIVE_DOMAIN_IDENTITY",
                "domain_alpha_value_source":
                    "INDEPENDENT_MEASUREMENT_OR_DECLARED_GOVERNING_DOMAIN_DATA",
                "private_same_sector_alpha_allowed": False,
                "different_alpha_within_same_governing_domain_allowed": False,
                "changing_alpha_defines_different_domain_structure": True,
                "governing_domain_value_derived_by_requirement": False,
                "governing_domain_ancestry_derived_by_certificate": False,
            },
            "SELECT": {
                "status": "OPEN",
                "governing_domain_selector_supplied": False,
                "numerical_value_selector_supplied": False,
                "realized_occupancy_is_selection_proof": False,
                "complete_universe_singleton_requirement": "OPEN",
            },
            "claim_ceilings": {
                "numerical_one_over_137_derived": False,
                "parameter_free_alpha_prediction": False,
                "complete_universe_alpha_interval": False,
                "cavity_half_contrast_is_gravity_gate": False,
                "governing_domain_ancestry_from_bare_recordhood": False,
                "governing_domain_emergence": False,
                "alpha_required_for_every_actvis_record_in_governing_domain": True,
                "alpha_required_without_established_domain_ancestry": False,
                "gravity_emergence": False,
                "einstein_gravity": False,
                "numerical_G": False,
            },
            "executable_scope": {
                "caller_arguments": 0,
                "empirical_fit_performed": False,
                "new_physics_calculated": False,
                "documentary_theorem_and_audit_regression_only": True,
            },
        }
    )


@dataclass(frozen=True)
class AlphaRole:
    """Immutable handle for the domain-alpha modal-role certificate."""

    @property
    def claim_class(self) -> str:
        return CLAIM_CLASS

    def certificate(self) -> Mapping[str, Any]:
        _verify_evidence()
        return _certificate()


def alpha_role() -> AlphaRole:
    """Verify pinned alpha-role evidence and return its zero-input handle."""
    _verify_evidence()
    return AlphaRole()


def alpha_role_certificate() -> Mapping[str, Any]:
    """Return the immutable ALLOW/REQUIRE/SELECT certificate."""
    return alpha_role().certificate()
