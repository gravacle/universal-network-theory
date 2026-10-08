# Floating-return C8 initial moving-clock corollary V001

This is an analytical consequence of the already counted C8 computational reference. It selects no saved age or charge parameter and adds no dynamics. The preparation is exactly one fixed-content carrier with density `I8/8` and eight blank records. The incidence graph is the supplied occupied C8, its eligible graph is K4,4, and the logical Hamiltonian is

\[
H=\frac{19}{2}I-tA_{C8}+\gamma\sum_v p_vX_v+A_R\sum_vq_v,
\qquad t=\gamma=\frac1{10},\quad q_v=(I-Z_v)/2.
\]

The field self-energy is retained. The three candidate values are (A_R=1/8,7/40,1/4). The variable (x=\tau/\hbar) has the same units as the frozen C8 packet. All statements concern the faithful joint dressed readout (B_v=Z_v-iY_v). A return-traced bare local clock, a physical atomic clock, a metric lapse or a proper-time calibration is not supplied by this result.

For any chosen site define (\beta(x)=\langle B_v\rangle). The exact initial state gives

\[
\beta(0)=1,\qquad \dot\beta(0)=2i\gamma/8=i/40,
\qquad \nu_0=\operatorname{Im}\frac{\dot\beta(0)}{\beta(0)}=1/40.
\]

Dots here denote (x) derivatives. Let (J_v=i[H_{\rm hop},p_v]). On this C8, (\|J_v\|=t\sqrt2). Since (p_v) commutes with all record Pauli operators, the same full Hamiltonian gives

\[
\dot B_v=2\gamma p_vY_v+i(A_RX_v+2\gamma p_vZ_v),
\]

\[
\ddot B_v=-2\gamma A_Rp_vX_v-4\gamma^2p_vZ_v
 +i(A_R^2I+4\gamma^2p_v)Y_v
 +2\gamma J_v(Y_v+iZ_v).
\]

In particular (\|Y+iZ\|=2), so conservative state-independent bounds are

\[
C_1=A_R+4\gamma\ \ge\ \|\dot B_v\|,
\qquad
C_2=A_R^2+2\gamma A_R+8\gamma^2+4\gamma t\sqrt2
\ \ge\ \|\ddot B_v\|.
\]

For the exact normalized preparation, take

\[
r=\min\left\{\frac1{4C_1},
 \frac{\nu_0}{4(C_2+C_1\nu_0)}\right\}.
\]

For (0\le x\le r), ( |\beta(x)-1|\le C_1r\le1/4), hence ( |\beta(x)|\ge3/4). Also

\[
\left|\frac{\dot\beta(x)}{\beta(x)}-\dot\beta(0)\right|
\le\frac43(C_2+C_1\nu_0)x\le\nu_0/3.
\]

Thus the exact initial local phase chart has (\nu(x)\ge2\nu_0/3=1/60>0) throughout this short interval. The same mathematics holds for the negative extension of the time-independent unitary, although the physically prepared trajectory here uses the one-sided interval. The bound is for the exact declared preparation, rather than an outward-rounded validation of floating-point saved trajectories.

| (A_R) | (C_1) | (C_2) | Sufficient (r), approximately |
|---:|---:|---:|---:|
| (1/8) | 0.525 | 0.177193542495 | 0.0328396798235 |
| (7/40) | 0.575 | 0.202193542495 | 0.0288592236342 |
| (1/4) | 0.65 | 0.249068542495 | 0.0235565895291 |

This earns a short initial inverse phase chart for moving matter in each candidate. It does not make the clock globally monotone. The saved C8 run shows later negative instantaneous phase rates in all three passive candidates, including (A_R<2\gamma); the pinned-carrier monotonicity theorem therefore cannot be transferred to this moving-carrier preparation. The (gamma=0) blank controls have zero phase rate and are excluded from this positive-rate corollary.

The physical clock generator, source-dependent encoding, causal connectors, formed geometry and common galaxy/expansion normalization remain separate obligations. Ideal copy-off retained record values retain their independently recorded controller work; this phase bound does not supply a free hold or a reservoir.

## Fixed references

| File in this directory | SHA256 |
|---|---|
| FLOATING_RETURN_C8_FORMATION_CLOCK_V001.md | eb04c848f360295df81c18240a2617c18a152190c1b6caa1a38abba3d2a08cbc |
| floating_return_c8_formation_clock_v001.py | 7a6b06343be8258370274f250b6d72a08bcb60cff000bbc090a98c4f093521df |
| FLOATING_RETURN_C8_FORMATION_CLOCK_V001_RESULT.json | 08ec6908d430536cf64fa5d1445e8ae95831515a5dfbdb9c318c029ab6409a43 |
| FLOATING_RETURN_C8_FORMATION_CLOCK_V001_RECEIPT.json | a01f7b80aeb90c2fa568536279607d1e514c3f4922db475220eeae7c9357f6ef |
| FLOATING_RETURN_C8_FORMATION_CLOCK_V001_AUDIT.json | cbf95d3678aff4ba91ad8ca2acff196394d38174fd8cb746b425d69bdce39d6b |

No scientific worker or new trajectory was used to derive this corollary. The decimal radii only evaluate the displayed sufficient bound.
