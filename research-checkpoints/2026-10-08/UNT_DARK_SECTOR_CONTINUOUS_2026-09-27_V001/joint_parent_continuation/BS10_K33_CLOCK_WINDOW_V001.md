# K3,3 local phase-clock windows V001 — prospective saved-data protocol

2026-10-05 UTC. Owner observer_cosmography. Derivative-bound application to the SAME declared clock, H and96 saved clock readouts. No vector, source, Hamiltonian, clock choice, phase orientation or propagation changes. Prepare source/protocol before outcomes; root/independent final preflight and fresh live ownership must precede ONE modest local saved-data worker. No automatic replay/resume.

## Recovered inputs and exact native derivative bounds

Authenticate `BS10_K33_INTERNAL_CLOCK_V001_RESULT.json`, raw SHA256 4d728596bfad33eb5006dab3c1c62d3f66a34ed909c9bcd8f94231e34f150ff4 and canonical payload d22dd535d35a504878308c3bc5ea9b8a84c19cd998f5b17429bc0a8e60d774c0; its protocol4700b457f5f5886e2291ee27131ef6dae71c25e4c352b017591494f9606ee23d, source78191f1f80bde1792cc915e32a71bf466d3891046f79c081a8f43ec95373b540 and report3e2ed3b359bd0a3249b8d82be9b831d5cbab1498ec1926835a8ae25e54de17a4. Check its manifest, every original input byte/hash, all16 row/journal commits and report/result seal; repeat input authentication before final sealing. The native source ancestry is the sealed `bs10_k33_unclamped_formation_v001.py` (SHA256 2a6d6326592dee5fb04ba47776ea495df68c0acdf7dce22f26f4be0eae0a1b6c), whose full tuple/field action already supplies all original vectors. No producer/helper is executed here.

Use B=Z0-iY0, hbar=1, actual degree operator d0, P0 and delta=1-d0/2. The previous exact commutator gives

    C=i[H,B]=2g P0Y0+i(delta X0+2g P0Z0),
    ||C||<=1+4g<=C1=1.4.                                 (1)

Since d0=0..3, ||delta||<=1. The record part of i[H,C] is

    -2g delta P0X0-4g^2P0Z0+i(delta^2+4g^2P0)Y0,

with norm<=1+2g+8g^2<=1.28. Three incident graph flips contribute at most3h_N lambdaR=.3. In the one-carrier sector the occupied hop star satisfies ||[Hhop,P0]||<=t sqrt(3), so its additional contribution is<=4g t sqrt(3)=.06928204 at g=.1,t=.1. All other unchanged terms commute in this derivative. Thus

    ||i[H,C]|| <=1.28+.3+.06928204 < C2=1.65.               (2)

These common bounds cover BOTH frozen g values without selecting a favorable state. Root, native agent and independent analytical review agreed on(1,2) and the radius algebra before the window outcomes. Physical energy, record feedback and all other terms remain in H; commuting away from this derivative is not an energy subtraction.

## Whole census, conditional norm and radius

Retain all g=0,.1; starts0/413; ages0,5,20,50; delays0,.1,.5,1,2,5. Every96-point clock status remains. All48 exact zero-rate g0 points receive no window and explicit null bounds, not a fictitious zero-size physical clock. Apply the formulas only to the already qualified g.1 points without selecting a new age or clock orientation.

For each point recover the previously assigned vector/scalar error budgets e_psi,e_beta,e_dot,e_nu, the raw squared vector norm n_raw and raw beta/beta_dot/nu. A raw near-unit norm is not itself an exact invariant. Use the conservative upper bound

    Nplus=max(1,(sqrt(n_raw)+e_psi)^2),
    bminus=|beta|-e_beta,
    dplus=|beta_dot|+e_dot,
    numinus=|nu|-e_nu.                                    (3)

Nplus covers the normalized exact parent-seed target1 and the conditionally assigned exact state within the saved-vector error budget. No baseline vector is normalized or clipped here. These certificates are conditional on those frozen floating-error budgets, not directed-rounding proofs that the actual floating vectors have the assigned errors.

Calculate the frozen radius

    r1=bminus/(4C1 Nplus),
    r2=numinus/[4Nplus(C2/bminus+C1 dplus/bminus^2)],
    r=min(r1,r2).                                         (4)

Store a conservatively rounded radius r_cert=nextafter(r,0) and both components. With |t-t0|<=r_cert, the exact native derivative bounds imply

    |beta(t)-beta(t0)|<=C1 Nplus r_cert<=bminus/4,
    |beta(t)|>=3bminus/4,
    |nu(t)-nu(t0)|<=(4/3)Nplus r_cert
                      (C2/bminus+C1 dplus/bminus^2)
                   <=numinus/3.

The orientation at the starting point is therefore stable, and |nu(t)|>=2numinus/3 throughout this local baseline interval. This is a positive local interval application; it does not rescue a global monotone clock across the already saved positive/negative rates.

The clock is a SOURCE-OFF BASELINE clock. At source delay0 use the one-sided baseline interval[0,r_cert] and retain `SOURCE_BOUNDARY_TANGENT_ONLY`; a phase-shifting pulse still need not have an accessible phase-matched readout at that boundary. For interior delays use the conservative post-source radius r_post=min(r_cert,delay/2), with delay interval[delay-r_post,delay+r_post]. This is an exact derivative-bound neighborhood under the existing autonomous H, not a newly propagated trajectory. It neither certifies a finite kicked phase match nor simulates an apparatus. Absolute native ages are the frozen preparation age plus these conditional delay endpoints.

## Arithmetic controls, outputs and completion

Freeze scalar checks for input census/status, finite positive margins/radii, r_cert<=r1,r2, native norm upper bound, amplitude-change<=bminus/4 and rate-change<=numinus/3. Use absolute1e-14*max(1,compared magnitude) only for checking floating calculations; save raw residuals and inequalities. Radius is rounded toward0, and C2 exceeds its proved common upper bound. Keep all conditionals/rounding limits; no statistical uncertainty, physical seconds, observational threshold or large-window requirement is introduced. Small or disjoint windows are scientific outcomes, not arithmetic failures or a trigger to rerun.

Own only this protocol, `bs10_k33_clock_window_v001.py`, `BS10_K33_CLOCK_WINDOW_V001_RESULT.json/.md` and exclusive `bs10_k33_clock_window_v001_checkpoints/`. Refuse existing outputs. One manifest records PID/PPID/host, all input hashes and fixed criteria; save each of16 completed snapshot window/check JSONs with fsynced append journal seals, then the canonical/raw result and report seals. Preserve partial/error rows; no new full vectors are needed. The worker uses Python standard-library JSON/hash/arithmetic only, with no NumPy, native helper import, H apply, eigensolver, recurrence or propagation. One local process, normal elapsed/RSS recording, no heavy model or new memory guard, installation, otherMac, Goal or scheduler. Root owns launch/session and existing continuation log/ledger integration. Qualification is a conditional local native ensemble-clock window; no atomic/photon clock, physical lapse, ruler, metric, galaxy normalization, expansion history, superiority or Stage3 completion is inferred.
