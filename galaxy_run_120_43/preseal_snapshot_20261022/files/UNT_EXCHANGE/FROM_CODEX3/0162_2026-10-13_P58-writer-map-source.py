"""Codex3 P58 V001. SOURCE ONLY; root alone executes numerical checks.
Column kernel convention: destination a, source b. No I/O or run on import.
This is a dense METHOD instrument, not a native backend or physical classifier.
Requires NumPy supplied by root. Companion theory0161 and receipt0160.
"""
import math
import numpy as np


def _parent(H, labels, tol):
    H = np.asarray(H, dtype=complex)
    if H.ndim != 2 or H.shape[0] != H.shape[1] or not H.shape[0]:
        raise ValueError("nonempty square parent required")
    if not np.isfinite(H).all() or not math.isfinite(tol) or tol <= 0:
        raise ValueError("finite parent and positive finite tolerance required")
    if np.max(np.abs(H-H.conj().T)) > tol:
        raise ValueError("non-Hermitian parent")
    labels = list(labels)
    if len(labels) != len(H) or any(type(x) is not int for x in labels):
        raise ValueError("one integer outcome label per basis state required")
    names = sorted(set(labels))
    groups = [np.flatnonzero(np.asarray(labels) == name) for name in names]
    return H, names, groups


def _kernel(U, groups):
    # The map deliberately retains the block ranks in its input lift.
    return np.array([[np.sum(np.abs(U[np.ix_(a, b)])**2)/len(b)
                      for b in groups] for a in groups], dtype=float)


def _unitary(vals, vecs, time):
    return (vecs*np.exp(-1j*time*vals)) @ vecs.conj().T


def audit_population_map(H, labels, time, retained_labels=(), tol=1e-11):
    """Inspect a complete computational partition on a finite dense H.

    Does not certify native physical state, Gamma, E1/E2/E3, scale or reach.
    `tol` is a floating method tolerance, not an analytic error bound.
    Retained restriction never renormalizes lost probability.
    """
    H, names, groups = _parent(H, labels, tol)
    if not math.isfinite(time) or time <= 0:
        raise ValueError("positive finite time required")
    retained_labels = list(retained_labels)
    if len(set(retained_labels)) != len(retained_labels):
        raise ValueError("duplicate retained labels")
    if any(name not in names for name in retained_labels):
        raise ValueError("unknown retained label")
    vals, vecs = np.linalg.eigh(H)
    U = _unitary(vals, vecs, time)
    U2 = _unitary(vals, vecs, 2*time)
    K, K2 = _kernel(U, groups), _kernel(U2, groups)
    ranks = np.array([len(g) for g in groups], dtype=float)
    L = np.zeros_like(K)
    for a, ga in enumerate(groups):
        for b, gb in enumerate(groups):
            if a != b:
                L[a,b] = np.sum(np.abs(H[np.ix_(ga,gb)])**2)/ranks[b]
    for b in range(len(groups)):
        L[b,b] = -np.sum(L[:,b])
    retained = [names.index(name) for name in retained_labels]
    escape = (1-K[np.ix_(retained,retained)].sum(axis=0)).tolist()
    # Find an actual cross-partition matrix element. A +/- phase witness has
    # identical basis probabilities; its derivative in the target block differs.
    witness = None
    for a, ga in enumerate(groups):
        for b, gb in enumerate(groups):
            if a == b:
                continue
            for i in ga:
                for j in gb:
                    hij = H[i,j]
                    if abs(hij) <= tol:
                        continue
                    plus = np.zeros(len(H), complex)
                    minus = np.zeros(len(H), complex)
                    plus[i] = minus[i] = 1/np.sqrt(2)
                    plus[j] = 1j*np.exp(-1j*np.angle(hij))/np.sqrt(2)
                    minus[j] = -plus[j]
                    Pa = np.zeros_like(H)
                    Pa[ga,ga] = 1
                    derivative = 1j*(H@Pa-Pa@H)
                    rp = float(np.vdot(plus,derivative@plus).real)
                    rm = float(np.vdot(minus,derivative@minus).real)
                    witness = {"i":int(i),"j":int(j),"outcome":names[a],
                               "probability_defect":float(np.max(np.abs(abs(plus)**2-abs(minus)**2))),
                               "q_rate_plus":rp,"q_rate_minus":rm,
                               "energy_difference":float((np.vdot(plus,H@plus)-np.vdot(minus,H@minus)).real)}
                    break
                if witness is not None:
                    break
            if witness is not None:
                break
        if witness is not None:
            break
    return {"scope":"FINITE_DENSE_METHOD_ONLY_NATIVE_ENSEMBLE_UNDETERMINED",
            "labels":names,"ranks":ranks.tolist(),"time":time,"tolerance":tol,
            "K":K.tolist(),"K_2t":K2.tolist(),"K_t_squared":(K@K).tolist(),
            "composition_defect":(K2-K@K).tolist(),
            "composition_defect_max":float(np.max(np.abs(K2-K@K))),
            "column_sum_defect":float(np.max(np.abs(K.sum(axis=0)-1))),
            "rank_measure_defect":float(np.max(np.abs(K@ranks-ranks))),
            "uniform_outcome_defect":float(np.max(np.abs(K.sum(axis=1)-1))),
            "weighted_symmetry_defect":float(np.max(np.abs(K*ranks-(K*ranks).T))),
            "unitarity_defect":float(np.max(np.abs(U.conj().T@U-np.eye(len(H))))),
            "short_time_coefficient":L.tolist(),
            "retained_labels":retained_labels,"retained_escape":escape,
            "same_probability_witness":witness,
            "H1":"UNDETERMINED","H2":"UNDETERMINED"}


def proposed_method_controls(tol=1e-10):
    """ROOT-RUN ONLY. Positive, null, unequal-rank and refusal partners.

    Returns data and computed check booleans; never calls itself on import.
    No physical conclusions are returned even if every method check passes.
    """
    bind = audit_population_map([[0,1],[1,0]],[0,1],math.pi/4,[1],tol)
    null = audit_population_map([[0,0],[0,2]],[0,1],math.pi/4,[1],tol)
    unequal = audit_population_map([[0,0,1],[0,0,0],[1,0,0]],
                                   [0,0,1],math.pi/4,[1],tol)
    checks = {
        "bind_normalized":bind["column_sum_defect"] < tol,
        "bind_composition_failure_half":abs(bind["composition_defect_max"]-0.5) < tol,
        "bind_retained_escape_half":abs(bind["retained_escape"][0]-0.5) < tol,
        "same_population_opposite_rates":abs(bind["same_probability_witness"]["q_rate_plus"]
                                             +bind["same_probability_witness"]["q_rate_minus"]) < tol
                                             and abs(bind["same_probability_witness"]["q_rate_plus"]) > 0.9,
        "commuting_identity":null["composition_defect_max"] < tol and null["same_probability_witness"] is None,
        "unequal_rank_conserved":unequal["rank_measure_defect"] < tol,
        "unequal_uniform_measure_fails":unequal["uniform_outcome_defect"] > 0.2,
    }
    for name,H,labels in [("nonhermitian",[[0,1],[0,0]],[0,1]),
                           ("incomplete_partition",[[0,1],[1,0]],[0])]:
        try:
            audit_population_map(H,labels,1,tol=tol)
        except ValueError:
            checks["refuses_"+name] = True
        else:
            checks["refuses_"+name] = False
    return {"checks":checks,"all_method_checks":all(checks.values()),
            "bind_control":bind,"commuting_control":null,"unequal_rank_control":unequal,
            "status":"METHOD_ONLY_NO_PHYSICAL_ACCEPTANCE"}
