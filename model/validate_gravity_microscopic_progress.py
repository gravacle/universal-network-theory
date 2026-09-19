#!/usr/bin/env python3
"""Fail-closed zero-input validator for the GL6T--GL6CS URM checkpoint."""

from __future__ import annotations

import hashlib
import inspect
from pathlib import Path
import tempfile
from types import MappingProxyType
from unittest import mock

import gravity_formation_theory as gft
import gravity_microscopic_progress as gmp
from project_model import URM


passed = 0


def check(condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError("gravity microscopic progress validation failed")
    passed += 1


def refused(callable_object) -> bool:
    try:
        callable_object()
    except gmp.GravityMicroscopicProgressRefusal:
        return True
    return False


def type_error(callable_object) -> bool:
    try:
        callable_object()
    except TypeError:
        return True
    return False


def mutate(mapping, key, value) -> None:
    mapping[key] = value


def main() -> int:
    check(tuple(inspect.signature(gmp.gravity_microscopic_progress).parameters) == ())
    check(tuple(inspect.signature(gmp.gravity_microscopic_progress_certificate).parameters) == ())
    check(type_error(lambda: gmp.gravity_microscopic_progress({})))
    check(type_error(lambda: gmp.gravity_microscopic_progress_certificate(data={})))

    progress = gmp.gravity_microscopic_progress()
    certificate = progress.certificate()
    check(progress.claim_class == gmp.CLAIM_CLASS)
    check(certificate["schema"] == gmp.SCHEMA)
    check(gmp.SCHEMA == "WAC_GRAVITY_MICROSCOPIC_PROGRESS_CERTIFICATE_V008")
    check(certificate["claim_class"] == gmp.CLAIM_CLASS)
    check(certificate["relationship_to_V014"] == "ADDITIVE_PROGRESS_SURFACE__V014_MEANING_UNCHANGED")
    check(isinstance(certificate, MappingProxyType))
    check(isinstance(certificate["exact_results"], MappingProxyType))
    check(isinstance(certificate["controlled_evidence"], MappingProxyType))
    check(isinstance(certificate["custody"]["packets"], tuple))
    check(refused(lambda: gmp._root_path("../outside")))
    resolver_lane = (
        "LANE_CROSS_RFT_GRA_GL6AZ_RECORD_AUTHENTICATED_"
        "PRETHERMAL_MISSION_IDENTIFIABILITY_V001"
    )
    resolver_manifest_relative = f"{resolver_lane}/MANIFEST.sha256"
    resolver_manifest = gmp._root_path(resolver_manifest_relative)
    resolver_readme_digest = next(
        line.split(maxsplit=1)[0]
        for line in resolver_manifest.read_text(encoding="utf-8").splitlines()
        if line.endswith("  README.md")
    )
    resolved_relative, resolved_path = gmp._declared_target(
        resolver_manifest_relative,
        "README.md",
        resolver_readme_digest,
    )
    check(
        resolved_relative == f"{resolver_lane}/README.md"
        and resolved_path == gmp._root_path(resolved_relative)
    )
    with tempfile.TemporaryDirectory(prefix="wac-gmp-resolver-") as temporary:
        resolver_root = Path(temporary)
        packet = resolver_root / "LANE"
        packet.mkdir()
        payload = b"same bytes\n"
        expected_digest = hashlib.sha256(payload).hexdigest()
        (resolver_root / "README.md").write_bytes(payload)
        (packet / "README.md").write_bytes(payload)
        with mock.patch.object(gmp, "_REPOSITORY_ROOT", resolver_root):
            multiple_refused = refused(
                lambda: gmp._declared_target(
                    "LANE/MANIFEST.sha256",
                    "README.md",
                    expected_digest,
                )
            )
            zero_refused = refused(
                lambda: gmp._declared_target(
                    "LANE/MANIFEST.sha256",
                    "README.md",
                    "0" * 64,
                )
            )
    check(multiple_refused and zero_refused)
    check(refused(lambda: gmp._verify_seal(gmp._PACKETS[-1].author_dir, "0" * 64, "0" * 64)))
    check(type_error(lambda: mutate(certificate, "schema", "changed")))
    check(type_error(lambda: mutate(certificate["exact_results"], "gravity", True)))

    check(certificate["custody"]["packet_count"] == 34)
    check(tuple(row["gate"] for row in certificate["custody"]["packets"]) == (
        "GL6T", "GL6U", "GL6AA", "GL6AF", "GL6AG", "GL6AH", "GL6AI",
        "GL6AK", "GL6AM", "GL6AN", "GL6AO", "GL6AP", "GL6AQ", "GL6AR",
        "GL6AS", "GL6AT", "GL6AU", "GL6AV", "GL6AW", "GL6AX", "GL6AY",
        "GL6AZ", "GL6BA", "GL6BB", "GL6BC", "GL6CH", "GL6CJ", "GL6CL",
        "GL6CM", "GL6CN", "GL6CO", "GL6CQ", "GL6CR", "GL6CS",
    ))
    check(certificate["custody"]["declared_hash_rows_checked"] == 1567)
    check(all(row["audit_disposition"].startswith("PASS") for row in certificate["custody"]["packets"]))
    check(all(len(row["author_claim_sha256"]) == 64 for row in certificate["custody"]["packets"]))
    check(all(len(row["audit_sha256"]) == 64 for row in certificate["custody"]["packets"]))
    check(certificate["custody"]["packets"][7]["audit_claim_file"] == "POSTFREEZE_AUDIT.md")
    check(certificate["custody"]["packets"][15]["author_claim_file"] == "RESULT.md")
    check(certificate["custody"]["packets"][15]["theorem_sha256"] is None)
    ba_packet = certificate["custody"]["packets"][22]
    check(ba_packet["author_directory"] == (
        "LANE_CROSS_RFT_GRA_GL6BA_AUTHENTICATED_PAIR_FINITE_MISSION_COLLAR_V001"
    ))
    check(ba_packet["audit_directory"] == (
        "AUDIT_G_GL6BA_AUTHENTICATED_PAIR_FINITE_MISSION_COLLAR_V001"
    ))
    check(ba_packet["theorem_sha256"] == (
        "d7ce0a7527a68f49e6ea2ee8edbb400a142fbb49297d8fe99cae78ffa0154ab0"
    ))
    check(ba_packet["audit_sha256"] == (
        "03bda2dba369211542dfef1af065490e21033483443cd6a67a21b06bf74e0bc9"
    ))
    check(ba_packet["audit_disposition"] == (
        "PASS__FULL_F3_FINITE_FPSS_COLLAR_EXACT__FINITE_BOUNDARY_COEFFICIENTS_"
        "CROSSING_CENSUS_PORT_DISTANCE_DUHAMEL_AND_TAYLOR_CONSTANTS_EXACT__"
        "AUTHENTICATED_BINARY_MARGINAL_ONLY__ALL_FINITE_R_AND_TIME__"
        "R2_AND_R5_OVER2_LICENSED_WITHOUT_ADHH__NO_GRAVITY_PROMOTION"
    ))
    bb_packet = certificate["custody"]["packets"][23]
    check(bb_packet["author_directory"] == (
        "LANE_CROSS_RFT_GRA_GL6BB_SELECTED_MISSION_PARTIAL_IDENTIFIABILITY_V001"
    ))
    check(bb_packet["audit_directory"] == (
        "AUDIT_G_GL6BB_SELECTED_MISSION_PARTIAL_IDENTIFIABILITY_V001"
    ))
    check(bb_packet["theorem_sha256"] == (
        "ed67f9d3bcd972fd4298c927280bbb522b9e129c5b0c15166a18c7e640ef6f88"
    ))
    check(bb_packet["audit_sha256"] == (
        "7fc77b9bb0054494c3b9e1120840e6899c06961cf1d26a2ef2fe2bd6cd08e3f2"
    ))
    check("SIGMA_ONLY_CLAIM_CONFINED" in bb_packet["audit_disposition"])
    bc_packet = certificate["custody"]["packets"][24]
    check(bc_packet["author_directory"] == (
        "LANE_CROSS_RFT_GRA_GL6BC_FINITE_COLLAR_RECIPROCAL_LINEAGE_OBSTRUCTION_V001"
    ))
    check(bc_packet["audit_directory"] == (
        "AUDIT_G_GL6BC_FINITE_COLLAR_RECIPROCAL_LINEAGE_OBSTRUCTION_V001"
    ))
    check(bc_packet["theorem_sha256"] == (
        "6355e6e1dda470e363122f5e3342c01346dc81e8992d05b1436f30b899041ea6"
    ))
    check(bc_packet["audit_sha256"] == (
        "a4979ef8d0183576e5ba32db7f6f7184e0afabe29f62bfa9f1edb2ce80c6ac45"
    ))
    check("FIXED_FINITE_CYLINDER_ZERO_STABLE_UNDER_REFINEMENT" in (
        bc_packet["audit_disposition"]
    ))
    latest_packets = certificate["custody"]["packets"][-9:]
    check(all(row["audit_acceptance_marker"] is not None for row in latest_packets))
    check(latest_packets[-2]["audit_sha256"] == (
        "ce307504587c50628b9204436f267c794d7325318c995fff78cd1c96faffafa1"
    ))
    check("UNIQUE_EINSTEIN_RAY" in latest_packets[-2]["audit_acceptance_marker"])
    check(latest_packets[-1]["audit_acceptance_marker"] == "## Disposition: PASS")
    check("GL6CP" not in tuple(row["gate"] for row in certificate["custody"]["packets"]))
    check(certificate["custody"]["historical_audit_count"] == 1)
    check(len(certificate["custody"]["historical_audits"]) == 1)
    check(certificate["custody"]["historical_audits"][0]["gate"] == "GL6AY_PRE_REPAIR_FAIL")
    check(certificate["custody"]["historical_audits"][0]["audit_disposition"] == (
        "FAIL__REPAIR_REQUIRED__GLOBAL_LOCK_PROJECTOR_AND_DRESSED_SUBSPACE_SCOPE"
    ))
    check(certificate["custody"]["historical_audits"][0]["status"] == (
        "SUPERSEDED_BY_REPAIRED_AUTHOR_AND_POST_REPAIR_PASS"
    ))

    exact = certificate["exact_results"]
    expected_legacy_exact = {
        "record_gated_local_pair_response": {
            "premise": "N=0;U_d=0;h>0;Delta>0;0<vartheta<2*pi",
            "KEEP": "D=-8*h*x*I6-4*h*x*z^2*A_L",
            "sectors": (
                "D_A1=-8*h*x*(1+2*z^2)",
                "D_E2=-8*h*x*(1-z^2)",
                "D_T2=-8*h*x",
            ),
            "open_domain_rank": 6,
            "matched_BREAK": "D_BREAK=0",
        },
        "interaction_owned_nonfactorization": (
            "y-x*z^2=-(16/3)*h^3*U_d*(tau/hbar)^4+O((tau/hbar)^6)"
        ),
        "authenticated_finite_atlas": {
            "shared_child": "J_e^1=J_f^1 iff c=c_prime",
            "edge_distance": "d_G(m,n)=one_half*norm_1(n-m)=1",
            "translation_cocycle": "sum_closed_path(delta)=0",
            "frame_cocycle": "T_ln*T_nm=T_lm",
            "premise": "INDEPENDENTLY_FORMED_NODE_ID_AND_PORT_LABEL_RECORDS",
        },
        "formation_pattern_source_threshold": {
            "premise": "N=0;U_d=0;h>0;Delta>0;0<vartheta<2*pi",
            "fixed_E_restriction": (
                "ZERO_OR_ONE_FORMED_LINK_GIVES_ZERO__EXACTLY_TWO_GIVES_RANK_ONE"
            ),
            "two_formed": "E^T*D^(ab)*E=-16*h*x*(1-z)*w_ab^T*w_ab",
            "scope": "FIXED_E_X_E_RESTRICTION_NOT_BROKEN_S4_INVARIANT_BLOCK",
        },
        "matched_neighbor_response": {
            "premise": (
                "N=1;h=U_d=E0>0;Delta=6*E0;d_star=2;delta=0;"
                "receiver_c_in_{1,2,3}"
            ),
            "reference": "MATCHED_TO_SOURCE_PATTERN_0000_WITH_RECEIVERS_FIXED_FORMED_KEEP",
            "expansion_variable": "u=E0*tau/hbar",
            "expansion": (
                "Delta_mu_c^E=-(5626/42525)*u^12*kappa_c*w_0c+O(u^14)"
            ),
        },
        "homogeneous_direct_edge_propagation": {
            "premise": "GENERAL_N_DIRECT_EDGE;delta=0",
            "raw": "Delta_Q_n6=-128*h^4*U_d^2*u_b_in",
            "normalized_witness": "Delta_mu_n=(8/45)*u^6*u_b_in+O(u^8)",
            "irrep": "u_b_in=one_half*one+one_half*s_b in A1_plus_T2",
            "direct_E": "E_TRANSPOSE*x_q=0_AT_EVERY_ORDER",
            "displayed_helper_E": (
                "NONZERO_ON_INCOMPLETE_ENDPOINT_INCIDENCE__CANCELS_ON_COMPLETE_"
                "HOMOGENEOUS_INTERIOR_ENDPOINT_INCIDENCE"
            ),
        },
        "uniform_quasilocal_influence_envelope": {
            "active_link_degree": "degree_L(e)=q(child)+2<=6",
            "lambda_F3": "48*abs(U_d)/hbar",
            "tail": (
                "norm_commutator<=2*norm(A)*norm(B)*T_distance(lambda_F3*abs(t))"
            ),
            "exponential": (
                "norm_commutator<=2*norm(A)*norm(B)*exp(-mu*(d_cell-v_mu*abs(t)))"
            ),
            "v_mu": "lambda_F3*exp(mu)/mu",
            "v_1": (
                "48*e*abs(U_d)/hbar_CELL_STEPS_PER_PARENT_TIME_UPPER_ENVELOPE_ONLY"
            ),
        },
    }
    check(all(exact[key] == value for key, value in expected_legacy_exact.items()))
    check(tuple(exact) == (
        "record_gated_local_pair_response",
        "interaction_owned_nonfactorization",
        "authenticated_finite_atlas",
        "formation_pattern_source_threshold",
        "matched_neighbor_response",
        "homogeneous_direct_edge_propagation",
        "uniform_quasilocal_influence_envelope",
        "authenticated_a3_bulk_dynamics",
        "authenticated_finite_window_bulk_response",
        "native_degree_lock_sector",
        "complete_order6_locked_hamiltonian",
        "locked_ir_representation_and_response_boundary",
        "authenticated_E_loop_selection_boundary",
        "locked_hexagon_thermodynamic_sector",
        "native_hexagon_collective_response",
        "order6_quantum_ice_crosswalk",
        "vg0_first_character_static_closure",
        "record_conditioned_collective_clock_and_typed_atlas",
        "anisotropic_folner_twist_closure",
        "all_fixed_order_port_and_twist_stability",
        "finite_coupling_prethermal_locked_bridge",
        "record_authenticated_prethermal_mission_identifiability",
        "authenticated_pair_finite_mission_collar",
        "selected_mission_partial_identifiability",
        "finite_collar_reciprocal_lineage_obstruction",
        "complete_order6_t2_future_writer",
        "same_parent_six_direction_pair_operator_access",
        "global_fourier_tensor_writer",
        "finite_component_stationary_writer_response",
        "complete_t2_first_source_through_h6",
        "cycle_response_tensor_extension_test",
        "stationary_response_observable_moment_rules",
        "direct_cubic_ward_einstein_classifier",
        "strict_lock_accumulation_horizon",
    ))
    check(exact["record_gated_local_pair_response"]["open_domain_rank"] == 6)
    check(exact["record_gated_local_pair_response"]["matched_BREAK"] == "D_BREAK=0")
    check("U_d" in exact["interaction_owned_nonfactorization"])
    check(exact["authenticated_finite_atlas"]["premise"] == "INDEPENDENTLY_FORMED_NODE_ID_AND_PORT_LABEL_RECORDS")
    check(
        "EXACTLY_TWO_GIVES_RANK_ONE"
        in exact["formation_pattern_source_threshold"]["fixed_E_restriction"]
    )
    check(
        "5626/42525" in exact["matched_neighbor_response"]["expansion"]
        and exact["matched_neighbor_response"]["expansion_variable"]
        == "u=E0*tau/hbar"
        and "O(u^14)" in exact["matched_neighbor_response"]["expansion"]
        and "O(tau^14)" not in exact["matched_neighbor_response"]["expansion"]
    )
    check(
        exact["homogeneous_direct_edge_propagation"]["premise"]
        == "GENERAL_N_DIRECT_EDGE;delta=0"
        and exact["homogeneous_direct_edge_propagation"]["direct_E"]
        == "E_TRANSPOSE*x_q=0_AT_EVERY_ORDER"
    )
    check("CANCELS" in exact["homogeneous_direct_edge_propagation"]["displayed_helper_E"])
    check(exact["uniform_quasilocal_influence_envelope"]["lambda_F3"] == "48*abs(U_d)/hbar")
    check("UPPER_ENVELOPE_ONLY" in exact["uniform_quasilocal_influence_envelope"]["v_1"])

    check(exact["authenticated_a3_bulk_dynamics"] == {
        "premise": "SELECTED_HOMOGENEOUS_ALL_FORMED_F3_MEMBER_ON_A3_X_FOUR_PORTS",
        "site_set": "L=A3_x_{1,2,3,4}",
        "pair_interaction_degree": 6,
        "lambda_F3": "48*abs(U_d)/hbar",
        "boundary_comparison": (
            "norm(tau_t^S(A)-tau_t^R(A))<=3*norm(A)*abs(X)*"
            "sum_{r=R}^infinity(2r+1)^3*T_{r-r_X+1}(lambda_F3*abs(t))"
        ),
        "bulk_limit": "BOUNDARY_INDEPENDENT_STRONGLY_CONTINUOUS_QUASILOCAL_DYNAMICS",
        "stationary_state": "AT_LEAST_ONE_JOINT_TIME_TRANSLATION_S4_INVARIANT_STATE_EXISTS_NOT_SELECTED",
        "spectral_measure": "mu_AB(B)=mu_A1(B)*P_A1+mu_E(B)*P_E+mu_T2(B)*P_T2",
    })
    check(exact["authenticated_finite_window_bulk_response"]["retarded_kernel"] == (
        "G^R_{beta,alpha}(t)=i*E_star^2/(2*hbar)*Theta(t)*"
        "omega([tau_t(M_beta),M_alpha])"
    ))
    check(exact["authenticated_finite_window_bulk_response"]["commutator_measure"] == (
        "NOT_POSITIVE_WITHOUT_PASSIVITY_OR_KMS"
    ))
    check(exact["native_degree_lock_sector"]["hamiltonian"] == (
        "H=-h*sum_e X_e+U_d*sum_v(k_v-2)^2+C"
    ))
    check(exact["native_degree_lock_sector"]["linear_Ward_no_go"] == (
        "[H,k_v-2]=-i*h*sum_{e_incident_v}Y_e"
    ))
    check("893M/1080" in exact["complete_order6_locked_hamiltonian"]["formula"])
    check(exact["complete_order6_locked_hamiltonian"]["hexagon_amplitude"] == "-63/8")
    check(exact["locked_ir_representation_and_response_boundary"]["mismatch"] == (
        "Hom_S4(T2,E)=0"
    ))
    check(exact["authenticated_E_loop_selection_boundary"]["uniform_locked_variance"] == (
        "(8/3)*norm(c)^2"
    ))
    check("product_{e_in_C}kappa_e" in (
        exact["authenticated_E_loop_selection_boundary"]["retained_support_gate"]
    ))
    check(exact["locked_hexagon_thermodynamic_sector"]["finite_component"] == (
        "H_C=-t*A_C;Delta_C=t*(rho_C-lambda_2(C))"
    ))
    check(exact["locked_hexagon_thermodynamic_sector"]["variance_bound"] == (
        "Delta_L<=18*t*norm(w)_infinity^2*L/Var(F_L)"
    ))
    check(exact["native_hexagon_collective_response"]["conserved_density"] == (
        "CENTERED_PORT_T2"
    ))
    check(exact["native_hexagon_collective_response"]["single_mode_bound"] == (
        "Delta_T2(chi;u)<=f_u(chi)/S_u_plus(chi)"
    ))
    check(exact["order6_quantum_ice_crosswalk"]["exact_parameter"] == "v/g=0")
    check(exact["order6_quantum_ice_crosswalk"]["distinct_RK_point"] == "v/g=1")
    check(exact["vg0_first_character_static_closure"]["oscillator_bound"] == (
        "f_u(q_L)<=6*J*sin(pi/L)^2"
    ))
    check(exact["vg0_first_character_static_closure"]["component_gap_bound"] == (
        "Delta_C(L)<=6*J*sin(pi/L)^2/S_u,L(q_L)"
    ))
    check("alpha<2" in (
        exact["vg0_first_character_static_closure"]["static_exponent_premise"]
    ))
    check("O(J/L)" in (
        exact["vg0_first_character_static_closure"]["alpha_one_consequence"]
    ))
    check("product_{e_in_c}kappa_e" in (
        exact["record_conditioned_collective_clock_and_typed_atlas"]["record_conditioned_loop"]
    ))
    check("q^6*H_hex(1)" in (
        exact["record_conditioned_collective_clock_and_typed_atlas"]["homogeneous_formal_family"]
    ))
    check(exact["record_conditioned_collective_clock_and_typed_atlas"]["tetrahedral_evaluation"] == (
        "rank(E)=4;im(E)=A1_plus_T2;ker(E)=E"
    ))
    check("NOT_ONE_PHYSICAL_METRIC_TANGENT" in (
        exact["record_conditioned_collective_clock_and_typed_atlas"]["typed_atlas"]
    ))
    check(exact["anisotropic_folner_twist_closure"]["translation_character"] == (
        "Y*U0*Y^-1=-U0"
    ))
    check("4*pi^2*J*L0*L2/L1" in (
        exact["anisotropic_folner_twist_closure"]["gap_bound"]
    ))
    check(exact["anisotropic_folner_twist_closure"]["folner_sequence"] == (
        "(L0,L1,L2)=(m,2*m^3,m);m>=5_ODD"
    ))
    check("SELECTED_GNS" in (
        exact["anisotropic_folner_twist_closure"]["closure_scope"]
    ))
    check(exact["all_fixed_order_port_and_twist_stability"]["contractible_port_law"] == (
        "Delta_N_a=0_FOR_a=0,1,2,3"
    ))
    check(exact["all_fixed_order_port_and_twist_stability"]["minimum_winding_hamming_distance"] == (
        "2*L_min"
    ))
    check("r<2*L_min" in (
        exact["all_fixed_order_port_and_twist_stability"]["fixed_order_scope"]
    ))
    check("T_L" in (
        exact["all_fixed_order_port_and_twist_stability"]["quasilocal_gap_dichotomy"]
    ))
    check("NO_UNIFORM_FINITE_COUPLING" in (
        exact["all_fixed_order_port_and_twist_stability"]["exact_ceiling"]
    ))
    check(exact["finite_coupling_prethermal_locked_bridge"]["parent"] == (
        "H=U_d*N_def-h*sum_e(X_e);N_def=sum_v(k_v-2)^2"
    ))
    check("U_d>=9*pi*v_0/kappa_0" in (
        exact["finite_coupling_prethermal_locked_bridge"]
        ["historical_GL6AY_compact_application_hypotheses"]
    ))
    check(exact["finite_coupling_prethermal_locked_bridge"]["historical_application_status"] == (
        "SUPERSEDED_NOT_ERASED_BY_GL6AZ_RESTORED_SOURCE_PROOF_DOMAIN"
    ))
    check("R>=nubar_0" in (
        exact["finite_coupling_prethermal_locked_bridge"]["current_application_license"]
    ))
    check("REMAINDER_RETAINED" in (
        exact["finite_coupling_prethermal_locked_bridge"]["exact_normal_form"]
    ))
    check("LICENSED_ONLY_UNDER_GL6AZ_CORRECTED_DOMAIN" in (
        exact["finite_coupling_prethermal_locked_bridge"]["exact_normal_form"]
    ))
    check("P_S^0=chi(N_S=0)" in (
        exact["finite_coupling_prethermal_locked_bridge"]["local_collar"]
    ))
    check("D_2(L)<=" in (
        exact["finite_coupling_prethermal_locked_bridge"]["finite_second_twist_moment"]
    ))
    check("0<r_1<ln(3/2)/4" in (
        exact["finite_coupling_prethermal_locked_bridge"]["local_observable_horizon"]
    ))
    check("P_L_TO_Q_L_LEAKAGE_NEEDS_NO_WINDING" in (
        exact["finite_coupling_prethermal_locked_bridge"]["topology_boundary"]
    ))
    check("NOT_ERASED_BY_GL6AZ" in (
        exact["finite_coupling_prethermal_locked_bridge"]["local_collar_status"]
    ))
    check("NOT_EXACT_ALL_TIME_LOCKED_PHASE" in (
        exact["finite_coupling_prethermal_locked_bridge"]["exact_ceiling"]
    ))
    az = exact["record_authenticated_prethermal_mission_identifiability"]
    check(az["dimensionless_inputs"] == "R=U_d/h__sigma_obs=h*(t_Q-t_F)/hbar")
    check("R>=nubar_0" in az["corrected_source_proof_domain"])
    check(az["restored_high_branch"] == "R/nubar_0>=1")
    check(az["first_smallness_floor"] == "R>=36*pi*e=307.4304320162484")
    check(az["restored_scale_separation_floor"] == (
        "R>=432*pi*e^2=10028.190682380982"
    ))
    check("18665728.0078" in az["complete_universal_floor"])
    check("D_TV(p^H,p^eff)<=Kbar_3(M_beta)/(2*R)" in (
        az["authenticated_binary_marginal"]
    ))
    check("NO_POSTSELECTION" in az["authenticated_binary_marginal"])
    check("R=Delta_def/(2*A_X)" in az["native_calibration"])
    check("sigma_obs=A_X*(t_Q-t_F)/hbar" in az["mission_clock"])
    check("ADMITS_EVERY_POSITIVE_R" in az["non_identifiability"])
    check("R_IN_{2,5/2}" in az["admitted_member_boundary"])
    check("APPLY_AUTHENTICATED_BINARY_MARGINAL_BOUND" in az["inside_domain_branch"])
    check("SHARPER_FINITE_MISSION_LOCAL_OBSERVABLE_THEOREM" in az["outside_domain_branch"])
    check("SUFFICIENT_NOT_NECESSARY_DOMAIN" in az["exact_ceiling"])

    ba = exact["authenticated_pair_finite_mission_collar"]
    check("DOES_NOT_CHANGE_GL6AZ_CORRECTED_PRETHERMAL_DOMAIN" in (
        ba["relationship_to_GL6AZ"]
    ))
    check(ba["full_parent"] == (
        "H/h=R*N_def-sum_p(X_p)__R=U_d/h__N_def=sum_v(k_v-2)^2"
    ))
    check(ba["dimensionless_inputs"] == "R=U_d/h__sigma_obs=h*(t_Q-t_F)/hbar")
    check("EVERY_FINITE_PHYSICAL_R>0" in ba["validity"])
    check("R=0_DECOUPLED_CASE_EXACT" in ba["validity"])
    check("NO_LARGE_R_OR_PRETHERMAL_HYPOTHESIS" in ba["validity"])
    check(ba["primary_physical_scope"] == (
        "EVERY_COMPLETE_FINITE_AUTHENTICATED_ALL-FORMED/MATCH_FPSS_"
        "EXTERIOR_Omega_IN_F_L_WITH_Lambda_L_STRICTLY_INTERIOR"
    ))
    check("abs(B_L)=(10*L^3+15*L^2+11*L+3)/3" in ba["collar"])
    check(ba["cross_boundary_pairs"] == "12*(3*L^2+3*L+1)")
    check(ba["influence_argument"] == "48*R*abs(sigma_obs)")
    check(ba["operator_error"] == (
        "norm(tau_sigma^(R,Omega)(M_beta)-tau_sigma^(R,L)(M_beta))<="
        "min(2,2*(3*L^2+3*L+1)*T_(2*L+1)(48*R*abs(sigma_obs)))"
    ))
    check(ba["binary_pair_DTV"] == (
        "D_TV(p^Omega,p^(L))<=min(1,(3*L^2+3*L+1)*"
        "T_(2*L+1)(48*R*abs(sigma_obs)))"
    ))
    check("EXACT_REDUCTION_OF_THE_SAME_COMPLETE_MISSION" in ba["state_ownership"])
    check("PROSPECTIVELY_SELECTED_ACTIVE_MEMBER" in ba["no_postselection_scope"])
    check("PAIR_COARSENING_SUMS_EVERY_RETAINED_FLAG_VALUE" in (
        ba["no_postselection_scope"]
    ))
    check("NO_OBSERVED_SUCCESS_POSTSELECTION" in ba["no_postselection_scope"])
    check("NOT_FULL_FLAG_OUTPUT_TV" in ba["no_postselection_scope"])
    check(ba["interaction_cluster_radius"] == "ceil(m/2)_FOR_m_PAIR_INSERTIONS")
    check("MATCH_THROUGH_ORDER_4*L+1" in ba["ordinary_taylor_match"])
    check("POSSIBLE_EXTERIOR_WORD_ORDER_4*L+2" in ba["ordinary_taylor_match"])
    check("T_(2*L+1)(48*R*abs(sigma_obs))<=delta" in ba["certified_radius"])
    check("SUFFICIENT_NOT_OPTIMAL" in ba["certified_radius"])
    check(ba["admitted_members"] == (
        "R=2_GIVES_96*abs(sigma_obs)__"
        "R=5/2_GIVES_120*abs(sigma_obs)__BOTH_DIRECTLY_LICENSED"
    ))
    check("ONLY_A_PROOF_DEVICE" in ba["collar_cut_scope"])
    check("NOT_ONE_INFINITE_AUTHENTICATED_RECORD_OR_MISSION" in ba["quasilocal_scope"])
    check("SUPPLY_THE_SELECTED_COLLAR_REDUCED_POSTFORMATION_STATE" in (
        ba["remaining_physical_payload"]
    ))
    check("NO_SELECTED_R_sigma_obs_CLOCK_STATE" in ba["exact_ceiling"])
    check("NO_GRAVITON_RICCI_EINSTEIN_GRAVITY_OR_G" in ba["exact_ceiling"])

    bb = exact["selected_mission_partial_identifiability"]
    check(bb["selected_mission_triple"] == "(R,sigma_obs,omega_L)")
    check("R_IN_{2,5/2}_ARE_DIAGNOSTIC_MEMBERS_ONLY" in bb["current_custody"])
    check("[0,1]" in bb["sharp_state_free_probability_interval"])
    check("AT_FIXED_R_AND_s" in bb["sharp_state_free_probability_interval"])
    check("NO_AUTHENTICATED_PREPARATION_CIRCUIT" in bb["sharpness_scope"])
    check("EACH_COLLAR_VALUE_REMAINS_PAIRED" in bb["pointwise_robust_interval"])
    check("ADDS_eta_NOT_2eta" in bb["trace_distance_state_radius"])
    check(bb["prepared_blank_L0_dimension"] == 5)
    check("-10R" in bb["prepared_blank_L0_hamiltonian"])
    check(bb["prepared_blank_pair_plus_weights"] == "(1,1/2,1/3,1/2,1)")
    check("R*expectation(G)" in bb["prepared_blank_energy_identity"])
    check("1-1/(3R)" in bb["prepared_blank_all_time_collar_bound"])
    check("5/6" in bb["prepared_blank_admitted_member_bounds"])
    check("13/15" in bb["prepared_blank_admitted_member_bounds"])
    check(bb["L0_exterior_error"] == (
        "epsilon_0(R,s)=min(1,exp(48*R*abs(s))-1)"
    ))
    check("11/6-exp(96*abs(sigma_obs))" in (
        bb["conditional_complete_mission_intervals"]
    ))
    check("28/15-exp(120*abs(sigma_obs))" in (
        bb["conditional_complete_mission_intervals"]
    ))
    check("ONLY_FOR_THE_DECLARED_PREPARED_BLANK_TWO_MEMBER" in bb["sigma_only_scope"])
    check("AUTHENTICATED_(R,sigma_obs,omega_L)" in bb["actual_selected_mission_payload"])
    check("NO_PHYSICAL_DEFAULT" in bb["calculator_scope"])
    check("NO_COMPLETE_PARENT_SUBSTITUTION_WITHOUT_GL6BA_ERROR" in bb["exact_ceiling"])

    bc = exact["finite_collar_reciprocal_lineage_obstruction"]
    check("SOURCE_OFF_FROZEN_POSTFORMATION" in bc["current_parent_schedule"])
    check("P_e^K*X_e" in bc["route_lift"])
    check("Pi_beta=product_e" in bc["route_projector"])
    check("T_(2L+1)(48R*abs(s))" in bc["collar_tail"])
    check("p^(Omega,BREAK)=p^(L,BREAK)" in bc["all_BREAK_exact_control"])
    check(bc["one_tail_contrast_interval"] == (
        "max(0,d_L-delta_L)<=d_Omega<=min(1,d_L+delta_L)"
    ))
    check("d_L>delta_L_IMPLIES_d_Omega>0" in bc["positive_certificate"])
    check("TWO_NONTRIVIAL_ARMS_PAY_TWO_TAILS" in bc["one_tail_scope"])
    check("Pr_j(beta)=Pr_0(beta)" in bc["support_word_conservation"])
    check("chi^R_(Pi_beta,B)=chi^R_(B,Pi_beta)=0" in (
        bc["retarded_reciprocity_zero"]
    ))
    check("WRITER_AND_ROUTE_OPERATIONS_ARE_NOT_ALLOWED_B" in bc["zero_algebra_scope"])
    check("COMPLETE_UNCONDITIONED_READ" in bc["read_scope"])
    check("FIXED_FINITE_SUPPORT_WORD_CYLINDER" in bc["refinement_scope"])
    check("NO_INFINITE_ROUTE_WORD_PROJECTOR" in bc["refinement_scope"])
    check("sin^2(2s)/2" in bc["forward_positive_control"])
    check("W_j_FOR_FRESH_K_new" in bc["missing_operational_channel"])
    check("ALL_WORK_CONTROLLER_RESOURCE" in bc["missing_operational_channel"])
    check("DERIVATIVE_IS_UNDEFINED" in bc["future_writer_boundary"])
    check("IDENTITY_SPECTATOR_K_new_GIVES_EXACT_ZERO" in bc["future_writer_boundary"])
    check("MINIMAL_ONLY_AS_THE_OPERATIONAL_TYPE" in bc["operational_minimality"])
    check("NOT_A_CLAIM_THAT_GRAVITY_REQUIRES_INSERTING_A_NEW_WRITER" in (
        bc["operational_minimality"]
    ))
    check("REPEATEDLY_WITH_THE_ACCUMULATED_F3_COLLECTIVE_STATE" in (
        bc["nonexclusive_phase_route"]
    ))
    check("NOT_DERIVED_BY_THIS_CHECKPOINT" in bc["nonexclusive_phase_route"])
    check("ONLY_FOR_THE_CURRENT_SOURCE_OFF_FROZEN_POSTFORMATION_PARENT" in (
        bc["exact_ceiling"]
    ))
    check("NO_SELECTED_MODERATE_R_SIGNAL" in bc["exact_ceiling"])

    check("105/16" in exact["complete_order6_t2_future_writer"]["off_diagonal"])
    check(exact["same_parent_six_direction_pair_operator_access"]["rank"] == 6)
    check("32/363" in exact["global_fourier_tensor_writer"]["analytic_rank_domain"])
    check("RECIPROCITY_POSITIVITY" in (
        exact["finite_component_stationary_writer_response"]["properties"]
    ))
    check("VANISHES_POINTWISE_THROUGH_ORDER6" in (
        exact["complete_t2_first_source_through_h6"]["diagonal_vertex"]
    ))
    check(exact["cycle_response_tensor_extension_test"]["rotational_extendibility"] == (
        "c+d=kappa/2"
    ))
    check("kappa=Z_T/3" in (
        exact["stationary_response_observable_moment_rules"]["coefficients"]
    ))
    check(exact["direct_cubic_ward_einstein_classifier"]["ward_coefficient_matrix"] == (
        "180_BY_9_RANK8_NULLITY1"
    ))
    check("CHI_wr=O(r^-12)" in (
        exact["strict_lock_accumulation_horizon"]["required_enhancement"]
    ))

    evidence = certificate["controlled_evidence"]
    check(tuple(evidence) == ("quantum_ice_v_over_g_zero",))
    check(evidence["quantum_ice_v_over_g_zero"]["claim_class"] == (
        "NUMERICAL_AND_EFFECTIVE_EVIDENCE_NOT_A_PHASE_GAP_OR_POLE_THEOREM"
    ))
    check("0.6_plus_or_minus_0.1" in evidence["quantum_ice_v_over_g_zero"]["Benton"])

    check(len(certificate["open_gates"]) == 17)
    check(certificate["open_gates"][0].startswith("ISOTROPIC_V_OVER_G_ZERO_PHASE_CONTROL"))
    check(certificate["open_gates"][1].startswith("EXACT_ALL_TIME_FINITE_H_OVER_U_D"))
    check(certificate["open_gates"][2].startswith("SELECTED_AUTHENTICATED_ACTUAL_MISSION"))
    check(certificate["open_gates"][3].startswith(
        "INSIDE_DOMAIN_EXACT_NORMS_AND_Kbar_3_FOR_THE_PRETHERMAL_ROUTE"
    ))
    check("d_L_GREATER_THAN_delta_L" in certificate["open_gates"][4])
    check("REPEATED_URFT_FORMATION" in certificate["open_gates"][6])
    check("THERMODYNAMIC_STATIONARY_STATE" in certificate["open_gates"][7])
    check("SOURCE_SECOND_A1_E2_T2" in certificate["open_gates"][8])
    check("LAWFUL_1PI_OR_QUOTIENT_KERNEL" in certificate["open_gates"][9])
    check("WARD_NULL_FROM_F3_RELATIONAL_REDUNDANCY" in certificate["open_gates"][10])
    check(certificate["open_gates"][-1] == "MICROSCOPIC_RICCI_COEFFICIENT_AND_G_MODEL")
    check(all(value is False for value in certificate["ceilings"].values()))
    check(certificate["ceilings"][
        "finite_mission_collar_selects_physical_R_sigma_clock_or_state"
    ] is False)
    check(certificate["ceilings"][
        "finite_mission_collar_is_one_fixed_collar_for_unbounded_time"
    ] is False)
    check(certificate["ceilings"][
        "finite_mission_binary_pair_DTV_is_full_retained_flag_TV"
    ] is False)
    check(certificate["ceilings"][
        "induced_collar_cut_is_a_separately_authenticated_physical_mission"
    ] is False)
    check(certificate["ceilings"][
        "quasilocal_limit_is_one_infinite_authenticated_record"
    ] is False)
    check(certificate["ceilings"]["full_F3_finite_mission_collar_is_gravity_or_G"] is False)
    check(certificate["ceilings"][
        "state_free_zero_one_interval_authenticates_every_endpoint_preparation"
    ] is False)
    check(certificate["ceilings"][
        "sigma_obs_is_the_sole_missing_datum_for_an_actual_selected_mission"
    ] is False)
    check(certificate["ceilings"][
        "one_tail_contrast_bound_applies_when_both_arms_have_nontrivial_tails"
    ] is False)
    check(certificate["ceilings"][
        "retained_support_word_conservation_fixes_the_entire_K_density_matrix"
    ] is False)
    check(certificate["ceilings"][
        "current_source_off_reciprocity_zero_is_a_universal_gravity_no_go"
    ] is False)
    check(certificate["ceilings"][
        "missing_operational_writer_requires_a_unique_new_Hamiltonian_term"
    ] is False)
    check(certificate["ceilings"][
        "repeated_URFT_formation_collective_phase_route_is_derived_here"
    ] is False)
    check(all(certificate["ceilings"][key] is False for key in (
        "h6_pair_source_writer_is_authenticated_record_formation",
        "six_direction_pair_operator_access_is_a_physical_metric",
        "global_Fourier_writer_chart_is_calibrated_spacetime",
        "finite_component_writer_response_is_a_selected_bulk_phase",
        "complete_t2_first_source_through_h6_is_all_orders_source_closure",
        "t2_extension_condition_is_full_rotational_or_Ricci_completion",
        "observable_moment_equations_are_satisfied_by_a_selected_state",
        "connected_response_is_the_physical_1PI_quotient_kernel",
        "direct_Ward_classifier_derives_the_F3_Ward_identity",
        "Einstein_ray_classification_is_gravity_or_G",
        "GL6CP_REPAIR_REQUIRED_is_promotable",
        "fixed_cell_scale_obstruction_is_a_global_no_go",
        "fixed_cell_scale_obstruction_proves_noncommuting_limits",
    )))
    check(certificate["custody"]["verification"].endswith(
        "ACCUMULATION_HORIZON_CUSTODY"
    ))
    check(certificate["executable_scope"]["caller_arguments"] == 0)
    check(certificate["executable_scope"]["physics_recalculated"] is False)
    check(certificate["executable_scope"]["gravity_solver"] is False)

    delegated = URM.gravity_microscopic_progress_certificate()
    check(delegated["schema"] == gmp.SCHEMA)
    check(URM.gravity_microscopic_progress().claim_class == gmp.CLAIM_CLASS)
    check(URM.gravity_formation_theory_certificate()["schema"] == gft.SCHEMA)
    check(gft.SCHEMA == "WAC_GRAVITY_FORMATION_THEORY_CERTIFICATE_V014")
    check(delegated["ceilings"]["gravity_derived_here"] is False)
    check(delegated["ceilings"]["G_calculated_here"] is False)

    expected = 249
    check(passed + 1 == expected)
    print(f"GRAVITY MICROSCOPIC PROGRESS: {passed}/{expected} PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
