# Universal registered-ball Maxwell response controls V001

Prospective protocol, 2026-10-06 UTC. Root alone launches the frozen worker after full independent source/protocol reviews and fresh process ownership. The author has not called any numerical definition, quadrature, spectrum, source, coefficient or rate. This packet computes only a dimensionless universal support function; no physical Eunit, R_cell, kappa, stationary population, rate, photon history or thermal state is chosen.

## Exact same-support observable

The frozen stationary note defines F(u)=3[sin(u)−u cos(u)]/u^3, F(0)=1, and

    J(z)=(105/2)∫_0^1 dx x^3(1−x)^3 ∫_-1^1 dc (1−c)^2
         F(z sqrt[1−2x(1−x)(1−c)])^2.

Changing variable s²=1−2x(1−x)(1−c) gives weighted angular measure s(1−s²)² ds/4. For a fixed s the admitted x interval |1−2x|≤s has length s. Reversing the positive integration order therefore proves the independent reduced expression

    J(z)=(105/8)∫_0^1 ds s²(1−s²)² F(zs)^2.

Neither expression changes the support or source law. Their normalized separation moments are exactly M_n=105/[(2n+3)(2n+5)(2n+7)], n≥0. In particular M0=1, M1=1/3, M2=5/33 and M3=35/429. The same ball average proves |F|≤1, hence 0<J(z)≤1 at finite real z and J0=1.

The characteristic function of the difference of two independent unit-ball projections is F(u)^2. Its cosine Taylor remainder gives

    F(u)^2=1−u²/5+3u⁴/175−4u⁶/4725+O(u⁸),
    |J(z)−(1−z²/15+z⁴/385)|≤4|z|⁶/57915.

The last inequality uses the exact sixth moment and is a mathematical remainder bound, not a fit. It does not declare the quartic approximation accurate at large z.

## Frozen census and representations

All12 mathematical points are z=(0,.01,.1,.25,.5,1,2,4,8,16,32,64). All positive Gauss–Legendre orders64/128/256 independently contract BOTH the original2D and reduced1D expressions. Every order saves its full node/weight vectors, all12 signed response pairs, all nine moment pairs n0..8 and every criterion. Every coarse arm remains even if unresolved at a large z.

F is evaluated by12 literal Taylor terms for |u|≤.5 and the literal sin/cos formula otherwise. The Taylor recurrence is t_(n+1)=−t_n*u²/[(2n+2)(2n+5)]. Its first omitted term and alternating remainder are bounded by40^−12 throughout this branch. The direct formula is independently compared with that series at u=(.01,.025,.05,.1,.25,.5), and F0 is checked. There is no gap/frequency/source filtering or favorable post-outcome grid selection.

Each order has69 controls: one positive ordered node/weight check; two measure normalizations;18 exact moment comparisons;24 positive-unit-bound checks;12 independent1D/2D comparisons; two J0 checks; and ten quartic-remainder checks at z=(0,.01,.1,.25,.5). The summary has58 controls: six formfactor representation comparisons, F0, three exact rational Taylor coefficient identities, and48 refinements comprising both64→128 and128→256 for both methods at every point. Total265 criteria are fixed before execution.

Ordinary normalization, moment, formfactor and response comparisons use2e−11. The comparison scale is the sum of the two absolute results (exact moment magnitude for a moment); the response refinement has a fixed1e−300 numerical floor. Bound violation is max(0,−J,J−1), with J≤0 explicitly failed. The quartic inequality uses its actual analytic remainder plus a fixed roundoff allowance2e−11*(1+|quartic|); the excess divided by that allowance must be≤1. Exact fraction witnesses compare −1/15,+1/385,−4/57915 with independently written coefficient/moment products. No physical-success threshold is inferred from these arithmetic checks.

All265 statuses and signed coarse/fine differences are saved. A numerical failure gives RESPONSE_CONTROLS_NOT_QUALIFIED/exit3 while retaining every arm. No arm, denominator, tolerance or point changes after outcome inspection. A completed mathematical control does not qualify any physical rate or stationary environment.

## Inputs, ownership and closure

The seven direct inputs below and this protocol are byte-authenticated. The two completed prior result/receipt bindings and all6624 Dyson/all4716 outgoing arithmetic flags are checked as preserved dispositions only; none of their matrices, native preparations, spectral moments, coefficients or saved effects is contracted. No legacy producer/helper import, eigenproblem, propagator or trajectory is invoked. NumPy provides only the new positive quadrature nodes and array contraction.

The exclusive uppercase namespace is NATIVE_REGISTERED_MAXWELL_BALL_RESPONSE_CONTROLS_V001. Five canonical payload/COMMIT pairs are AUTH, ORDER64, ORDER128, ORDER256, SUMMARY. A fresh run refuses orphan runtime files before creating its manifest. Resume requires an exact manifest, nonempty OWNER_START journal, complete ordered authenticated prefix, exact owner PID/epoch, canonical finite payloads, full arm grid/node/weight/moment/criterion schema and matching completed input dispositions. It refuses closed result/receipt/report or FAILED prefixes and never overwrites them.

Inputs and own source are rehashed before every checkpoint and publication. Each file is exclusively created after canonical JSON encoding and protected0444. The final five-pair census is revalidated before result/report publication. The exact root terminal event includes result/status/265 controls/five checkpoints; the closed journal is protected0444 and its SHA enters the output map before receipt creation and the postpublication recheck. A fresh uninterrupted lifecycle has OWNER_START, five CHECKPOINT events and OWNER_COMPLETE. Resume creates a new root owner epoch without altering completed pairs. Genuine entered exceptions preserve an exclusive FAILED artifact; an already closed attempt is not changed.

Source: native_registered_maxwell_ball_response_controls_v001.py. No worker result or runtime prefix exists at the author's freeze check. Root's fresh prelaunch check owns that statement at execution time.

| Frozen direct input | SHA256 |
|---|---|
| NATIVE_REGISTERED_MAXWELL_STATIONARY_EMISSION_AND_DEBIT_V001.md | 595e89b2993a81530250176a636df4639aec493b9f399997500112a14d44c536 |
| NATIVE_REGISTERED_CELL_OUTGOING_MAXWELL_PAIR_KERNEL_V001.md | f4debb30c540386d39179fdcfc244373ac6a2bcab9f04f27fa32c0f404c88c8c |
| NATIVE_REGISTERED_MAXWELL_DYSON_ENERGY_LEDGER_V001.md | 2ab45d4575ee2c8569a5e1a59f38dbbf3b4c60854f3ef63100e82ccd6a987306 |
| NATIVE_CANONICAL_MAXWELL_DYSON_ENERGY_CONTROL_V001_RESULT.json | b6ef391337e96998976eab6d9b99b3e90369b88e2c2f47fcfc23e59bd62f1dd4 |
| NATIVE_CANONICAL_MAXWELL_DYSON_ENERGY_CONTROL_V001_RECEIPT.json | 94c8c845c16b2f6d4978afda790f6a70f31ee33e799d5e581aae3d174913cdce |
| NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001_RESULT.json | 9ad2f9890d5e909c048c0353365b75a22b86570c91d45488fb6d19b5e018de1b |
| NATIVE_REGISTERED_CELL_OUTGOING_SOURCE_V001_RECEIPT.json | 0c5bf238307def809f53b05cf37e773385542da8816952af89d7308a74832c7e |
