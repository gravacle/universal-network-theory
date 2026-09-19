"""EVERY SEALED ARROW HEADLINE (F-17, F-18, F-19, F-21, and the PF-2 history F-20 rests
beside), REPRODUCED THROUGH model/arrow.py -- the T-54/T-55 fold-in, T-46 pattern.

Each check recomputes a registered headline number through the arrow layer and gates it
against the SEALED value copied from the lane's own sealed output file:

  F-17   LANE_F1_ARROW/f1_arrow.txt          (threshold sweep: 24 weight-1 observables at
                                              0.00000000; 252 weight-2, max 0.11448276;
                                              closed form exact)
  F-18   LANE_F1_ARROW/f1b_invariance.txt    (weight-1 coupling: I(S:B) = 0.04549256,
                                              chi = 0.00000000 -- the four-row ledger)
  F-19   LANE_F1_ARROW/f1b_invariance.txt    (I(S:B) invariance 3.686e-14 over 12
                                              system-only unitaries; covariance PASS;
                                              fixed-label chi moves 1.145e-01)
  PF-2   LANE_PF2_DYNAMICAL/pf2_history.txt  (the history 0 -> 0.97527192 -> 0.90811968
                                              with <Zbar> exactly constant; the full
                                              reversal control)
  F-21   LANE_PF2_DYNAMICAL/pf2_history.txt  (fragments 0.789366/0.048377/0.678602 under
                                              weight-d; EXACTLY ZERO under weight-1)
                                             -- gated THROUGH RecordModel.redundancy,
                                              which no validator called before T-55.

DISCIPLINE: D-8 -- wherever a computed comparison exists it is the gate (closed form vs
chi; the reversal equality; instrument-vs-instrument cross checks); the transcribed
sealed prints are gated as the SEALED ANCHORS they are, stated as such.  D-15 -- every
zero is gated with a positive control named beside it in the same section.  Plus
API-fidelity probes BEYOND every gated range (lam = 0.5; t = +-3.0; the two-qubit
fragment; a never-sealed bath through the observation gate) -- definition, not shortcut.

Standalone: python3 checks_arrow.py  (exit 0 iff every check passes).
Chained:   from checks_arrow import run_arrow_checks; run_arrow_checks(check)
           in the validate_geometry.py idiom -- check(name, cond, detail="")."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import arrow as AR


# tolerances derived from the sealed print precisions, stated once
TOL8 = 5e-9     # 8-decimal sealed prints (0.11448276, 0.90811968, ...)
TOL6 = 5e-7     # 6-decimal sealed prints (fragment bits 0.789366, ...)
ZERO = 1e-10    # sealed prints of 0.00000000 (measured magnitudes are <= 4e-15 here)


def run_arrow_checks(check):
    C = AR.carrier()
    nS = C['nS']

    # ------------------------------------------------------------ carrier self-checks
    # (the sealed lanes' own preamble: [Zbar,H_S] = 0, ground degeneracy 4, d = 2)
    check("ARROW carrier: ||[Zbar, H0]|| == 0, ground degeneracy 4, dim H_1 == 2, "
          "logical weights (2,2) -- computed from homology, never nominated",
          np.linalg.norm(C['Zbar'] @ C['H0'] - C['H0'] @ C['Zbar']) < 1e-9
          and C['gs'] == 4 and C['dimH1'] == 2 and C['weights'][:2] == (2, 2),
          f"gs={C['gs']} dimH1={C['dimH1']} weights={C['weights']}")

    # ------------------------------------------------------------ F-17: the threshold
    th = AR.arrow_threshold()          # sealed venue: coupling Zbar, lam = 0.8
    cf = th['logical']['closed_form']
    check("F-17 chi(Zbar:B) == closed form from Z_B(+-1) (computed comparison, D-8) "
          "AND == sealed anchor 0.11448276",
          abs(th['logical']['chi_Zbar'] - cf) < 1e-9
          and abs(th['logical']['chi_Zbar'] - 0.11448276) < TOL8,
          f"chi={th['logical']['chi_Zbar']:.8f} closed={cf:.8f}")
    check("F-17 weight-1 sweep: ALL 24 observables at chi == 0 (count computed == 3*C(8,1); "
          "positive control: the weight-2 max in the next check)",
          th[1]['n_swept'] == 24 == 3 * 8 and th[1]['max_chi'] < ZERO,
          f"n={th[1]['n_swept']} max={th[1]['max_chi']:.3e}")
    check("F-17 weight-2 sweep: 252 observables (== 9*C(8,2)), max == chi(Zbar) computed "
          "== sealed anchor 0.11448276 -- the threshold sits at weight d",
          th[2]['n_swept'] == 252 == 9 * 28
          and abs(th[2]['max_chi'] - th['logical']['chi_Zbar']) < 1e-9
          and abs(th[2]['max_chi'] - 0.11448276) < TOL8,
          f"n={th[2]['n_swept']} max={th[2]['max_chi']:.8f} argmax={th[2]['argmax']}")
    check("F-17 chi about the OTHER logical (Zbar2 coupling row of the same instrument) "
          "== 0 (positive control: the Zbar chi gated above)",
          th['logical']['chi_Zbar2'] < ZERO,
          f"chi_Zbar2={th['logical']['chi_Zbar2']:.3e}")
    # API-fidelity probe BEYOND the sealed range: lam = 0.5 was never sealed; the chi
    # instrument must still equal the independent closed form there, at a value that is
    # NOT the sealed 0.11448276 -- definition, not lookup.
    r5 = AR.mean_force_state(C['Zbar'], lam=0.5)
    c5 = AR.chi(r5, C['Zbar'], nS, AR.NB4)
    cf5 = AR.closed_form_chi(0.5)
    check("F-17 PROBE beyond sealed range: lam=0.5 (never sealed) -- chi == closed form "
          "AND != the sealed lam=0.8 value (the law is computed, not stored)",
          abs(c5 - cf5) < 1e-9 and abs(c5 - 0.11448276) > 1e-3,
          f"chi(0.5)={c5:.10f} closed={cf5:.10f}")

    # ------------------------------------------------------------ F-18: the ledger
    led = {row['coupling']: row for row in AR.arrow_ledger()}
    check("F-18 weight-1 coupling ENTANGLES: I(S:B) == sealed anchor 0.04549256 yet "
          "transfers ZERO record bits, chi == 0 -- decoherence and the record's arrow "
          "separated (the zero's positive control is the same row's I > 0)",
          abs(led['Ze']['I_SB'] - 0.04549256) < TOL8 and led['Ze']['chi_record'] < ZERO,
          f"I={led['Ze']['I_SB']:.8f} chi={led['Ze']['chi_record']:.3e}")
    check("F-18 ledger row Zbar: I(S:B) == chi(Zbar:B) (computed equality) == sealed "
          "0.11448276 -- at weight d ALL of the correlation is record information",
          abs(led['Zbar']['I_SB'] - led['Zbar']['chi_record']) < 1e-9
          and abs(led['Zbar']['I_SB'] - 0.11448276) < TOL8,
          f"I={led['Zbar']['I_SB']:.8f} chi={led['Zbar']['chi_record']:.8f}")
    check("F-18 ledger row Zbar2: I(S:B) == sealed 0.11448276 with chi(Zbar:B) == 0 "
          "(the bath learns the OTHER logical, nothing about this record)",
          abs(led['Zbar2']['I_SB'] - 0.11448276) < TOL8
          and led['Zbar2']['chi_record'] < ZERO,
          f"I={led['Zbar2']['I_SB']:.8f} chi={led['Zbar2']['chi_record']:.3e}")
    check("F-18 ledger row identity: I(S:B) == 0 AND chi == 0 (no coupling, no anything; "
          "positive controls: every row above)",
          led['identity']['I_SB'] < ZERO and led['identity']['chi_record'] < ZERO,
          f"I={led['identity']['I_SB']:.3e}")

    # ------------------------------------------------------------ F-19: irreversibility
    inv = AR.arrow_invariance()        # sealed: 12 unitaries, seed 5
    check("F-19 instrument covariance: chi(QOQ' in QrQ') == chi(O in r) to < 1e-8 "
          "(the lane's own bound; sealed print 9.992e-16, blockwise route 3.9e-15)",
          inv['covariance_worst'] < 1e-8, f"worst={inv['covariance_worst']:.3e}")
    check("F-19 I(S:B) invariant under 12 system-only unitaries -- numerically zero "
          "under ZERO (historical sealed transcript: 3.686e-14)",
          abs(inv['mutual_worst']) < ZERO,
          f"worst={inv['mutual_worst']:.3e}")
    check("F-19 chi about the FIXED label MOVES -- sealed anchor 1.145e-01 (the positive "
          "control for the invariance zero: relocatable from inside, never erasable)",
          f"{inv['fixed_label_worst']:.3e}" == "1.145e-01",
          f"worst={inv['fixed_label_worst']:.3e}")

    # ------------------------------------------------------------ PF-2: the history
    times = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, -4.0, 3.0, -3.0]
    hist, states = AR.arrow_history(times, keep_states=(4.0,))
    h = {row['t']: row for row in hist}
    SEALED_HIST = {0.25: 0.40660635, 0.5: 0.81447230, 1.0: 0.97527192,
                   2.0: 0.78665760, 4.0: 0.90811968}
    check("PF-2 history: chi(Zbar:B)(t) == all five sealed anchors "
          "(0.40660635 / 0.81447230 / 0.97527192 / 0.78665760 / 0.90811968)",
          all(abs(h[t]['chi'] - v) < TOL8 for t, v in SEALED_HIST.items()),
          "got=" + str(["%.8f" % h[t]['chi'] for t in (0.25, 0.5, 1.0, 2.0, 4.0)]))
    check("PF-2 chi == 0 EXACTLY at t=0 (product state; positive control: the t=1 "
          "anchor 0.97527192 in the row above)",
          h[0.0]['chi'] < 1e-12, f"chi(0)={h[0.0]['chi']:.3e}")
    check("PF-2 the record is READ, not written: max |<Zbar>(t) - <Zbar>(0)| == 0 over "
          "every time (computed comparison; [Zbar, H_tot] = 0)",
          max(abs(row['value'] - h[0.0]['value']) for row in hist) < 1e-9,
          f"max drift={max(abs(row['value'] - h[0.0]['value']) for row in hist):.3e}")
    check("PF-2 reversal control: chi(-4.0) == chi(+4.0) (computed equality -- the "
          "closed dynamics is exactly reversible; the instrument manufactures nothing)",
          abs(h[-4.0]['chi'] - h[4.0]['chi']) < 1e-9,
          f"|diff|={abs(h[-4.0]['chi'] - h[4.0]['chi']):.3e}")
    check("PF-2 PROBE beyond sealed range: t=+-3.0 (never sealed) -- reversal equality "
          "holds there too, at a value that is none of the sealed anchors",
          abs(h[-3.0]['chi'] - h[3.0]['chi']) < 1e-9
          and all(abs(h[3.0]['chi'] - v) > 1e-3 for v in SEALED_HIST.values()),
          f"chi(3.0)={h[3.0]['chi']:.8f}")
    env = AR.pf2_env()
    r4 = states[4.0]
    I4 = AR.mutual(r4, nS, env.dim)
    check("PF-2 I(S:B)(t=4) == chi(t=4) (computed equality) == sealed anchor 0.90811968 "
          "-- every correlated bit is a record bit under the weight-d coupling",
          abs(I4 - h[4.0]['chi']) < TOL8 and abs(I4 - 0.90811968) < TOL8,
          f"I={I4:.8f} chi={h[4.0]['chi']:.8f}")

    # ------------------------------------------------------------ F-21: redundancy
    # THE WIRE: RecordModel.redundancy, called by no validator before T-55, gated here.
    red = AR.arrow_redundancy()        # weight-d coupling, sealed t = 4.0
    SEALED_FRAGS = (0.789366, 0.048377, 0.678602)
    check("F-21 RecordModel.redundancy (WIRED): whole bath == sealed 0.90811968; "
          "fragments == sealed 0.789366 / 0.048377 / 0.678602 under the weight-d coupling",
          abs(red['whole'] - 0.90811968) < TOL8
          and all(abs(f - s) < TOL6 for f, s in zip(red['fragments'], SEALED_FRAGS)),
          f"whole={red['whole']:.8f} frags={[f'{f:.6f}' for f in red['fragments']]}")
    cross_whole = env.holevo(r4, C['Zbar'], nS)
    cross_frags = [env.holevo(r4, C['Zbar'], nS, fragment=[j]) for j in range(env.nq)]
    check("F-21 cross-instrument: RecordModel.redundancy (complex eigh path) == "
          "Environment.holevo on arrow_history's own t=4 state (real eigh path) -- two "
          "routes, four numbers, one answer (this gate polices the packaging economies)",
          abs(cross_whole - red['whole']) < 1e-9
          and all(abs(a - b) < 1e-9 for a, b in zip(cross_frags, red['fragments'])),
          f"|whole diff|={abs(cross_whole - red['whole']):.3e}")
    red1 = AR.arrow_redundancy(coupling=C['Ze'])
    check("F-21 weight-1 coupling: whole bath AND every fragment EXACTLY ZERO through "
          "RecordModel.redundancy (positive control: the weight-d row two checks up)",
          red1['whole'] < ZERO and all(f < ZERO for f in red1['fragments']),
          f"whole={red1['whole']:.3e} frags={[f'{f:.3e}' for f in red1['fragments']]}")
    pair = env.holevo(r4, C['Zbar'], nS, fragment=[0, 2])
    check("F-21 PROBE beyond sealed range: the two-qubit fragment {0,2} (never sealed) "
          "obeys data processing -- max single fragment <= chi{0,2} <= whole bath",
          max(cross_frags[0], cross_frags[2]) <= pair + 1e-9
          and pair <= cross_whole + 1e-9,
          f"chi{{0,2}}={pair:.8f} in [{max(cross_frags[0], cross_frags[2]):.6f}, "
          f"{cross_whole:.8f}]")

    # ------------------------------------------------------------ observation entry
    # The T-54/T-55 story made executable: a NEW bath observation enters HERE.
    from record_model import Environment
    new_env = Environment(nq=2, energies=(0.9, 1.6), beta=2.0)   # never sealed anywhere
    refused_world = refused_corner = False
    try:
        AR.score_bath_observation(new_env, C['Zbar'])            # world tier, no provenance
    except ValueError:
        refused_world = True
    try:
        AR.score_bath_observation(new_env, C['Zbar'], tier="corner")   # corner, undeclared
    except ValueError:
        refused_corner = True
    check("ENTRY the gate REFUSES a world-tier bath without provenance AND a corner bath "
          "without the DEF-A self-declaration (D-25 at the layer's own door)",
          refused_world and refused_corner)
    sc_d = AR.score_bath_observation(new_env, C['Zbar'], tier="corner", provenance="DEF-A")
    sc_1 = AR.score_bath_observation(new_env, C['Ze'], tier="corner", provenance="DEF-A")
    check("ENTRY a NEW 2-qubit bath (never sealed) scored through the gate: the weight-d "
          "coupling delivers record bits to the whole bath AND to fragments; data "
          "processing holds (max fragment <= whole <= I(S:B))",
          sc_d['holds_record_bits'] and sc_d['redundant_fragments'] >= 1
          and max(sc_d['fragments']) <= sc_d['chi_whole'] + 1e-9
          and sc_d['chi_whole'] <= sc_d['I_SB'] + 1e-9,
          f"chi={sc_d['chi_whole']:.6f} frags={[f'{f:.4f}' for f in sc_d['fragments']]} "
          f"I={sc_d['I_SB']:.6f}")
    check("ENTRY the F-18 discriminator fires on the NEW bath too: the weight-1 coupling "
          "entangles (I > 0) with ZERO record bits -- the threshold is structural, not "
          "a memorized state (positive control: the weight-d entry above)",
          sc_1['entangled_without_record'] and sc_1['I_SB'] > 1e-3
          and sc_1['chi_whole'] < ZERO and sc_1['redundant_fragments'] == 0,
          f"I={sc_1['I_SB']:.6f} chi={sc_1['chi_whole']:.3e}")
    from record_model import RecordModel
    Z2 = np.diag([1.0, -1.0])
    custom = RecordModel(np.zeros((2, 2)), [])
    custom_refused = False
    try:
        AR.score_bath_observation(new_env, Z2, model=custom,
                                  tier="corner", provenance="DEF-A")
    except ValueError as exc:
        custom_refused = "custom RecordModel requires its record" in str(exc)
    mismatch_refused = False
    try:
        AR.score_bath_observation(new_env, Z2, record=C['Zbar'], model=custom,
                                  tier="corner", provenance="DEF-A")
    except ValueError as exc:
        mismatch_refused = "does not match model dimension" in str(exc)
    custom_scored = AR.score_bath_observation(
        new_env, Z2, record=Z2, model=custom, tier="corner", provenance="DEF-A")
    check("ENTRY a custom RecordModel without its own explicit record REFUSES cleanly "
          "instead of pairing with the toric default; the same 2x2 model scores when its "
          "2x2 record is supplied (D-15 positive control)",
          custom_refused and mismatch_refused and custom_scored['chi_whole'] > 0.0
          and custom_scored['I_SB'] + 1e-9 >= custom_scored['chi_whole'],
          f"missing/mismatch refused={custom_refused}/{mismatch_refused} "
          f"chi={custom_scored['chi_whole']:.9f} "
          f"I={custom_scored['I_SB']:.9f}")


if __name__ == "__main__":
    import time
    n_pass = 0
    n_fail = 0

    def check(name, cond, detail=""):
        global n_pass, n_fail
        if cond:
            n_pass += 1
            print(f"  PASS  {name}  {detail}")
        else:
            n_fail += 1
            print(f"  FAIL  {name}  {detail}")

    print("VALIDATE THE ARROW LAYER (F-17/F-18/F-19/F-21 + the PF-2 history) "
          "THROUGH model/arrow.py")
    print("=" * 78)
    t0 = time.time()
    run_arrow_checks(check)
    print("=" * 78)
    print(f"  ARROW: {n_pass} PASS, {n_fail} FAIL   ({time.time() - t0:.0f}s)")
    sys.exit(0 if n_fail == 0 else 1)
