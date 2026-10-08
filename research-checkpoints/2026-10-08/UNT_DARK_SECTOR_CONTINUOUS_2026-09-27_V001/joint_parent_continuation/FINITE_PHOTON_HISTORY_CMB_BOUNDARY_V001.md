# Finite photon history: ruler uncertainty versus the CMB initial state

2026-09-29. Analytical, no new numerical calculation, observation, physical history or source change. This concerns the explicitly conditional macroscopic scalar/Q=0 model and imported ordinary photon interactions. It neither assumes an initial singularity/inflation nor derives a thermal or correlated photon population from the native network.

## 1. What the existing uncertainty means

The frozen acoustic calculation integrates the owned history only to `A_c=1/a_c=10^7`. At each drag endpoint it retains

    r_s = r_s[drag,A_c] + r_early,     0 <= r_early <= B_old(A_c).

`B_old` uses positive hard-material/baryonic lower expansion bounds; it intentionally does not assume ordinary photons persist before that boundary. This is a physical conditional-history interval, not quadrature error. The audited finite case 8 has an early-tail width about 0.20646 Mpc; its total drag/ruler interval remains wider, about 0.21155 Mpc, and its precision flag remains false. The dust case has a much wider old tail. None of these receipts, bounds, gates or flags changes here.

A scalar ruler interval cannot by itself bound every CMB transfer. Even in a free, normalized acoustic oscillator, two sound distances differing by delta_r give the exact propagator difference

    ||Rot(k[r+delta_r])-Rot(kr)||_2
       = 2|sin(k delta_r/2)| <= min(2,k|delta_r|).             (1)

Thus a small fractional ruler uncertainty is not automatically a small phase error at every k, especially near a zero of a particular transfer component. Equation (1) is only the free-oscillator comparison, not a bound on the gravitationally forced, baryon-loaded, diffusing photon system or its relative power-spectrum error.

## 2. A finite extension can be bounded without any origin hypothesis

If an extension is wanted, add it explicitly over **only** a finite interval `A_c <= A <= A_i`. A minimal background assumption is that the same positive massless photon population obeys the ordinary source-free energy equation on that interval:

    rho_gamma A^-4 = constant,    T_gamma=T0 A.               (2)

This preserves an already specified Planck occupation distribution; it does not create one. Balanced continual emission/replacement is not ruled out by zero net energy source, but its perturbation/noise/collision operator is extra physics and cannot be inferred from (2). Thomson scattering alone also does not supply a blackbody-creation mechanism.

Let `q_H=Omega_H Q/E1 >= 0` be the already owned hard quartic radiation lower coefficient. If the same material current remains adopted on this finite interval and other included density terms are nonnegative, then

    H(A) >= H_cal sqrt(F) A^2,
    F=Omega_gamma+q_H.                                      (3)

An additionally declared conserved ordinary neutrino component may be added to F; it is not required for the photon-only bound. All Omegas in (3) are the saved H_cal normalization, not silently renormalized actual-H0 fractions. In a strict dust-limit member q_H=0; the positive photon term still gives a finite F. Any negative density contribution would have to be retained in a different lower bound.

With the owned baryon loading `B=3 Omega_b/(4 Omega_gamma)` and tight-coupling sound speed `c_s=c/sqrt[3(1+B/A)]`, the finite added sound distance satisfies

    0 <= Delta r_s <= c/(sqrt(3) H_cal sqrt(F))
        * (2/B)[sqrt(1+B/A_c)-sqrt(1+B/A_i)]
      <= c/(sqrt(3) H_cal sqrt(F)) (1/A_c-1/A_i).             (4)

The first expression integrates the known baryon factor exactly against the radiation-only lower H bound; it has the continuous B=0 limit given by the second expression. Its square-root difference should be rationalized in an implementation. Retaining positive baryonic expansion gives the stronger, still elementary one-dimensional upper comparison

    Delta r_s <= c/(sqrt(3)H_cal)
      integral_(1/A_i)^(1/A_c) dy /sqrt[(F+Omega_b y)(1+B y)]. (5)

These are conservative bounds, not claims of saturation by the actual history. The interval earlier than A_i is **not removed**. If the old material-only assumptions remain owned there, retain `B_old(A_i)` separately; otherwise leave that prehistory unspecified. In particular the convenient A_i→infinity version of (4) is not available without extending its photon/material assumptions to that whole domain. No such extension is adopted here.

## 3. An opacity bound does not erase acoustic preparation

An implementable finite-slice CMB calculation already has all the background it needs on `1 <= A <= A_i`, without assigning an earlier sound horizon. It must supply its initial photon/baryon/hard/neutrino state instead.

For the direct photon line-of-sight boundary the attenuation is exp(-tau_i). A useful finite-domain certificate is available if `x_e >= x_min > 0` is explicitly qualified over `[A_c,A_i]`. For a finite-gap member the existing exact bound `E(A)<=Q A^4+D A^2` gives

    H(A) <= H_cal A^2 sqrt(F_up),
    F_up=Omega_rad+q_H+Omega_b/A_c
         +Omega_H D/(E1 A_c^2)+max(Omega_Lambda,0)/A_c^4.

Consequently

    Delta tau >= c sigma_T n_H0 x_min
                  (A_i-A_c)/(H_cal sqrt(F_up)).              (6)

Use consistent SI units in (6). In the strict dust-limit member replace the hard Q,D terms by its exact matter term, `Omega_m/A_c`, rather than taking a singular finite-gap D limit. Fully ionized composition is a separately named high-temperature approximation; without a bound on x_e, (6) is not certified. A later, already qualified optical depth only strengthens the attenuation. The finite direct-brightness boundary can then be bounded in its chosen absolute norm by `exp(-tau_i)||F_i+4Phi_i||`; polarization has its corresponding attenuated boundary.

Crucially, the Thomson collision operator conserves the photon monopole and couples the dipole to baryon momentum. It damps anisotropy/slip, **not every acoustic density/velocity or metric mode**. Neutrino and hard-fluid perturbations also retain their own state. Even an enormous optical depth therefore does not justify deleting the initial acoustic phase or assigning a zero prehistory ruler.

## 4. Smallest closed alternative for the actual CMB calculation

The shortest defensible route is the already proposed finite initial slice at A_i=A_c, with no new background extrapolation:

1. Declare one common constrained initial state for photons, polarization, baryons, ordinary neutrinos, hard fluid and metric. An exact finite-slice column (or a single declared coherent combination of the existing two columns) is legitimate. Alternatively qualify a regular adiabatic state over a specified preceding finite interval. Neither is automatically selected by the network, nor interchangeable with the other.
2. Give that same state one shared stochastic covariance—for example the previously counted As/ns spectrum. A chosen column ratio is an additional state assumption or shared calibration if freed, not a separate arbitrary function for each k or observable. Validate constraints, tight-coupling/series order and the finite photon/polarization boundary at the actual same-state material fractions.
3. Integrate the complete collisional/metric system from that slice. Then there is no missing prehistory contribution in the **initial-value problem**: its effect, if any, is in the declared initial state. This does not mean setting the old `r_early` interval to zero, or upgrading an old BAO interval receipt to a precise prediction.
4. Use the same evolved baryon/photon state for the acoustic feature and TT/TE/EE/lensing. Do not attach a freely selected scalar early sound phase to the old profiled BAO curve independently of the CMB state. If finite-slice preparation materially changes the acoustic feature template, its compatibility with a compressed BAO-ruler interpretation must also be tested.

For fixed coefficients the exact linear relation is `Y_f=U(f,i)Y_i`; differences of initial states propagate as `U deltaY_i`. For differing background/thermal continuations the variation-of-constants identity additionally contains `integral U(f,s) deltaA(s) Y(s) ds`. Neither term is controlled merely by the scalar sound-distance interval. An implementation can retain the initial columns and their covariance, direct boundary response, and transported earlier/later-slice comparisons instead of claiming a universal scalar error bar.

Moving the initial slice is a numerical consistency test only if it transports the **same state**. Resetting an independently chosen zero/shear/regular column at each new slice is a different preparation and must be labeled as such. No physical k cutoff is inferred from the finite computational interval.

This is a useful and limited conditional photon continuation/state test. It imports ordinary propagation and a finite thermal initial state, not an origin story. A later native common-temperature/correlation mechanism could replace that preparation assumption, but need not be derived before the explicitly conditional empirical model is tested.

## Source binding

- `FINITE_SLICE_CMB_PREPARATION_AND_BOLTZMANN_ROUTE_V001.md`: `7b9a4952f279d9a32b6a6d5de9338f01b50bd3cbd6a1eab8cced8bad5f593cd4` (full read).
- `finite_pressure_bao_ruler_v001.py`: `b59ab0f88e39234929eb6fa4d0a53bba0b1bf4dc4fbd9891b704b5cd89e19bf1` (owned background/acoustic/tail source).
- `SAME_ACTION_RADIATION_ASYMPTOTE_V001.md`: `913160e3e485d3b6ddc64a66a47a0c06c40b6cd350bb8764df5629f848b49002` (full read; finite-gap bounds).
- `HYREC_CASE008_REVIEW_V002.md`: `60e6b858d40a581a54459732c3078b0a7c8a369a2ddef50fefb49ae1f6697515` (unchanged saved physical-tail scope).
