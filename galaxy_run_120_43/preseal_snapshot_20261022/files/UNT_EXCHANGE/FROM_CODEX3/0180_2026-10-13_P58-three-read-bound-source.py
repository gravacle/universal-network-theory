"""P58 fine-history bound V001, SOURCE ONLY. Root alone executes controls.
Exact rational sufficient inequality from theory0179; caller owns native certificates.
No H assembly, histories, inferred bath, physical classifier or automatic execution.
"""
from fractions import Fraction


def _q(x):
    if isinstance(x,bool) or not isinstance(x,(int,str,Fraction)):
        raise TypeError("exact integer/rational string/Fraction required")
    return Fraction(x)


def three_read_bound(c_lower, outcome_weight_upper, centered_norm_upper,
                     interval, allowed_additivity_error=0):
    """Re D <= -tau² c_lower + 3 w_upper tau³ h_upper³.

    Requires certified lower bound on native c>=0, certified upper bounds on
    w<=1 and ||H-zeta I||, and the complete same-parent three-read domain.
    Rational scalar inputs are not themselves certificates of those facts.
    """
    c,w,h,tau,eps = map(_q,(c_lower,outcome_weight_upper,centered_norm_upper,
                          interval,allowed_additivity_error))
    if c < 0 or not 0 <= w <= 1 or h < 0 or tau <= 0 or eps < 0:
        raise ValueError("nonnegative bounds, weight<=1, positive interval required")
    if c > w*h*h:
        raise ValueError("inconsistent lower c versus upper weight/norm bounds")
    remainder = 3*w*tau**3*h**3
    upper = -tau**2*c+remainder
    violation_lower = max(Fraction(0),-2*upper)
    return {"c_lower":c,"weight_upper":w,"centered_norm_upper":h,"interval":tau,
            "remainder_upper":remainder,"real_interference_upper":upper,
            "two_history_additivity_violation_lower":violation_lower,
            "allowed_additivity_error":eps,
            "conditional_status":("OBSTRUCTION_IF_NATIVE_INPUT_CERTIFICATES_HOLD"
                                  if violation_lower > eps else "INCONCLUSIVE"),
            "input_certification":"CALLER_MUST_SUPPLY_SAME_PARENT_STATE_READ_AND_NORM_CERTIFICATES",
            "physical_ensemble":"UNDETERMINED","native_scoring_release":False,
            "H1":"UNDETERMINED","H2":"UNDETERMINED"}


def persistent_q_bound(g, joint_pq_lower, outcome_weight_upper,
                       centered_norm_upper, interval, allowed_additivity_error=0):
    """Literal persistent-old-q coefficient c=g² <p_v P_a>.
    Newborn/absent labels or nonliteral/projected parents require a new proof.
    """
    g,joint,w = map(_q,(g,joint_pq_lower,outcome_weight_upper))
    if not 0 <= joint <= w <= 1:
        raise ValueError("joint-occupation bound must lie between0 and outcome upper bound")
    result = three_read_bound(g*g*joint,w,centered_norm_upper,interval,allowed_additivity_error)
    result["Bind_coefficient"] = g
    result["joint_pq_lower"] = joint
    result["scope"] = "PERSISTENT_OLD_Q_ONLY_FULL_HJOIN_REMAINDER_REQUIRED"
    return result


def proposed_exact_controls():
    """Root-run only; rational theorem-controls, not numerical native histories."""
    positive = persistent_q_bound(1,1,1,1,'1/10')
    mixed = persistent_q_bound(1,'1/2','1/2',1,'1/10')
    no_carrier = persistent_q_bound(1,0,1,1,'1/10')
    no_bind = persistent_q_bound(0,1,1,0,'1/10')
    long_interval = persistent_q_bound(1,1,1,1,1)
    checks = {
        "positive_upper":positive["real_interference_upper"] == Fraction(-7,1000),
        "positive_violation":positive["two_history_additivity_violation_lower"] == Fraction(7,500),
        "identity_state_half":mixed["real_interference_upper"] == Fraction(-7,2000),
        "no_carrier_inconclusive":no_carrier["conditional_status"] == "INCONCLUSIVE",
        "no_bind_inconclusive":no_bind["conditional_status"] == "INCONCLUSIVE",
        "large_interval_not_decoherence":long_interval["conditional_status"] == "INCONCLUSIVE",
    }
    for name,args in [
        ("float",(1.0,1,1,1,'1/10')),
        ("joint",(1,2,1,1,'1/10')),
        ("norm",(1,1,1,'1/2','1/10')),
        ("time",(1,1,1,1,0)),
    ]:
        try:
            persistent_q_bound(*args)
        except (ValueError,TypeError):
            checks["refuses_"+name] = True
        else:
            checks["refuses_"+name] = False
    return {"checks":checks,"all_method_checks":all(checks.values()),
            "positive":positive,"identity_state":mixed,"no_carrier":no_carrier,
            "no_bind":no_bind,"long_interval":long_interval,
            "scope":"EXACT_SCALAR_METHOD_ONLY_UNEXECUTED_BY_AUTHOR"}
