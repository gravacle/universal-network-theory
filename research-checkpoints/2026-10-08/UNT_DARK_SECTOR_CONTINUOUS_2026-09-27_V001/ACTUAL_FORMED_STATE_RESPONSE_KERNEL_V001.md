# Exact susceptibility of the actual formed state

2026-09-27. New analytical continuation; no numerical physics run, new
preparation, ground projection, cooling, or physical dephasing is assumed.
Resident flags were checked before reading `TWO_BAND_ANALYTICAL_BRIDGE.md`,
`NATIVE_TWO_CHANNEL_CLOCK_SCREEN_V001.md`, and the minimal-join README.
Their formation, two-band decomposition, clock obstruction, and reported
upper-band weight are prior results, not new results of this note. The
original dataless computation/output files were not opened.

**Result.** The actual nonstationary state has an exact two-time response,
including coherences. Its energy-dephased comparator retains the full excited
population and has up to four response poles. The reported 13.05% upper-band
weight guarantees positive static susceptibility and positive low-frequency
kinetic coefficient for this native spectrum, even without knowing how that
population is distributed. It does not establish passivity at every line.
The positive static susceptibility also preserves a local negative
shared-source cross energy on a population-preserving adiabatic branch.

## 1. Only four unnormalized two-level blocks are needed

Use the already derived hold Hamiltonian

    H_q=C_q I−hX_a+(b_q−jX_C)n,
    h=1, j=1/2, b_q=9/4−q/2, C_q=3+q, q=0,1.

Let a=(q,s), s=±1 the carrier-X parity, and set

    x_a=b_q−js,
    d_a=√(x_a²+4h²),
    E_{±,a}=C_q+(x_a±d_a)/2.

The lower/upper link eigenvectors are exactly those in the two-band note.
In that ordered basis,

    n_a = [[(1−x_a/d_a)/2, h/d_a],
           [h/d_a, (1+x_a/d_a)/2]].                  (1)

Trace the postformation state over spectator labels and retain its diagonal
q,s blocks. Write these UNNORMALIZED matrices as

    ρ_a = [[p_{−,a}, c_a], [c_a*, p_{+,a}]],
    p_a=p_{−,a}+p_{+,a},    w_a=p_{−,a}−p_{+,a}.

Then Σ_a p_a=1 and |c_a|²≤p_{−,a}p_{+,a}. The hold keeps p_± fixed and
c_a(t)=c_a exp(+id_at/ℏ). Cross-q and cross-parity coherences need not be
discarded from the state: they simply make zero contribution to the
commutator below because n and H preserve q,s. The same is true of traced
spectator coherences. These four 2×2 matrices determine the entire n-source
response, although they do not determine every carrier observable.

## 2. Exact nonstationary retarded kernel

For a perturbation H→H−f(t)n, with f in energy units,

    δ〈n(t)〉=∫dt′ χ(t,t′)f(t′)+O(f²),
    χ(t,t′)=(i/ℏ)θ(t−t′)Tr ρ[n_H(t),n_H(t′)].       (2)

Let Δ=t−t′ and δ_a=d_aΔ/ℏ. Direct multiplication of (1) gives

    χ_a(t,t′)=θ(Δ) 2h/(ℏd_a²) ×
      {[h w_a+x_a Re c_a(t′)]sin δ_a
       −x_a Im c_a(t′)[1−cos δ_a]},
    χ(t,t′)=Σ_a χ_a(t,t′).                          (3)

The sign and phase convention use c_a=ρ_{−,+}; reversing that convention
requires conjugating c in (3). For a pure lower state in one block,
w=1,c=0, (3) recovers the previously derived ground oscillator. For a pure
upper state its sign reverses. For a formed state the response depends on
the launch time t′ through its existing coherences; it cannot generally be
represented by one susceptibility χ(ω).

All four native x_a are nonzero and all four d_a are distinct. Consequently
stationarity of this kernel for every t,t′ requires c_a=0 in every relevant
block; the distinct oscillations cannot cancel identically. Coherences
between blocks remain invisible here. In the more general special case
x_a=0, that block's coherence drops out of the commutator, even though its
unperturbed occupation can still oscillate.

A nonstationary state is not made passive by reading a positive instantaneous
coefficient in (3). Its unperturbed occupation contains

    〈n(t)〉_a=p_a/2−x_a w_a/(2d_a)
                 +(2h/d_a)Re c_a(t).

An appropriately timed weak cyclic source can extract first-order work
from a nonconstant expectation: W^(1)=−∫ḟ(t)〈n(t)〉dt. Its sign can be
reversed by reversing the source. Passivity assertions below refer to the
stationary comparator and the specified source channel.

## 3. Energy dephasing retains all populations, including inversion

The mathematical comparator D_H(ρ)=Σ_E P_EρP_E has c_a=0 and the SAME
p_±,a. It retains exact energy-degenerate coherences; none changes this
response. Its stationary susceptibility is

    χ̄(ω)=Σ_a 2h²w_a /
          {d_a[d_a²−ℏ²(ω+i0)²]}.                   (4)

For positive frequencies,

    Im χ̄(ω)=Σ_a [πh²w_a/(ℏd_a²)]δ(ω−d_a/ℏ).      (5)

The native pole energies are

    {d_a}={√89,√113,√145,√185}/4.

For distinct gaps, nonnegative absorption for every weak cyclic n-source
is equivalent to w_a≥0 for every a. If gaps coincide in another model,
the total residue at each shared gap is the condition. Positive total
Σw_a or positive χ̄(0) alone does not imply this passivity. It is a
statement about this source channel, not arbitrary controls that mix
carrier parity or record sectors.

An exact single oscillator occurs only when every nonzero residue belongs
to one gap. With these four distinct gaps, at most one w_a may be nonzero.
For that gap d with weight w>0,

    χ̄(ω)^−1 = D−Z_t(ω+i0)²,
    D=d³/(2h²w),    Z_t=ℏ²d/(2h²w).                (6)

Thus the ground ratio D/Z_t=d²/ℏ² survives a population mixture within
one gap, but the two coefficients both acquire 1/w. For a normalized
two-level mixture, w=1−2p_upper. There is no justification for applying
one such correction using the TOTAL upper weight when several gaps
contribute. A zero or negative w is respectively invisible or active,
not a positive oscillator with the ground coefficients.

## 4. A positive low-frequency response survives the actual excited weight

Define the signed moments

    C_k=Σ_a 2h²w_a/d_a^(2k+3),  k=0,1,2,... .

Below the smallest pole, with y=ℏω,

    χ̄(ω)=C_0+y²C_1+O(y⁴),
    χ̄(ω)^−1=D_eff−Z_eff ω²+O(ω⁴),
    D_eff=1/C_0,
    Z_eff=ℏ²C_1/C_0².                              (7)

Let η=Σp_+,a, d_min=√89/4 and d_max=√185/4. Without assuming any
individual w_a positive, the exact population bound is

    C_k ≥ 2h²[(1−η)/d_max^(2k+3)
                         −η/d_min^(2k+3)].         (8)

Therefore C_k>0 whenever

    η < d_min^(2k+3)/[d_min^(2k+3)+d_max^(2k+3)].

The prior reported η=0.1305499137438213 satisfies this inequality for
BOTH k=0 and k=1. The stricter k=1 threshold is

    89^(5/2)/[89^(5/2)+185^(5/2)] ≈ 0.138.

Hence C_0>0 and C_1>0, and both D_eff and Z_eff are positive for the
dephased ACTUAL population distribution. This conclusion does not depend
on a ground projection, fitted relaxation law, or unmeasured within-band
population distribution. It still permits a negative absorption residue
at an individual gap. Higher moments have stricter bounds and are not
all certified positive by η alone.

The approximation is quantitatively controlled. For real |y|<d_min, set
r=y²/d_min²<1. Then

    |χ̄−C_0−y²C_1|
      ≤ [y⁴/(1−r)]Σ_a 2h²|w_a|/d_a⁷,              (9)
    |χ̄−C_0|
      ≤ [r/(1−r)]Σ_a 2h²|w_a|/d_a³.

If the second bound is at most εC_0 with ε<1, inversion is controlled
as well. With δχ=χ̄−C_0 and R_4 the first bound, the error of the
inverse approximation in (7) is at most

    R_4/C_0² + |δχ|²/[C_0³(1−ε)].

The apparent pole of this truncated inverse is not thereby a physical
new low-frequency mode: the exact poles remain those in (4). In
particular, n has no carrier intraband pole below j=1/2. A low-frequency
filter can expose an off-resonant susceptibility, not a second n-clock
at those carrier frequencies.

## 5. Negative shared-source energy without a ground-state replacement

For the stationary comparator, consider a sufficiently slow weak source
−f n that adiabatically transports each existing eigenpopulation without
changing p_±,a. The exact population-preserving branch energy is

    E_ad(f)=Σ_a [p_−,a E_−,a(f)+p_+,a E_+,a(f)],
    E_±,a(f)=C_q+[x_a−f±√((x_a−f)²+4h²)]/2.

Direct differentiation gives

    E_ad″(0)=−C_0<0.                                (10)

For two weak sources coupling to the SAME n, f=f_1+f_2, its cross term
is −C_0 f_1 f_2. The same excited population retained above therefore
allows local negative shared-source curvature. For a formal record bias
f=λ_R δq it is −λ_R²C_0. This is a population-preserving adiabatic energy
branch, not minimization over states or a thermodynamic free energy.
It does not prove the same cross-cost for a finite binary insertion, a
sudden formed-state trajectory, spatial attraction, or universal gravity.
All scalar and source-work terms remain in the complete branch energy.

## 6. Controlled comparison with the actual two-time response

Averaging the LAUNCH TIME t′ over a declared interval of width T while
keeping delay Δ fixed multiplies c_a(t′) by its exact sinc factor,
with magnitude at most |c_a|min(1,2ℏ/(d_aT)). Equation (3) gives

    |〈χ(t′+Δ,t′)〉_T−χ̄(Δ)|
      ≤Σ_a [4h|x_a||c_a|/(ℏd_a²)]
          |sin(d_aΔ/(2ℏ))| min(1,2ℏ/(d_aT)).        (11)

This is a response-specific error bound. It does not invoke a smallest
irrelevant spectator splitting or drop the upper population. Launch-time
averaging is a mathematical or explicitly declared measurement operation,
not a claim that waiting destroys coherence. At one unaveraged launch
time, use (3) or the same bound with the final minimum replaced by one.

The required next numerical input is only p_−,a, p_+,a, Re c_a and
Im c_a for each of the four q,s blocks of the SAME saved postformation
state, in the eigenvector convention of (1). These determine the exact
two-time kernel, the dephased line residues and passivity, C_0,C_1, and
every coefficient in (9) and (11). This extraction retains all outcomes
and excited populations. A separate sham comparison can use the same
formula with its own complete saved state; neither state should be
replaced by an independently prepared ground state.
