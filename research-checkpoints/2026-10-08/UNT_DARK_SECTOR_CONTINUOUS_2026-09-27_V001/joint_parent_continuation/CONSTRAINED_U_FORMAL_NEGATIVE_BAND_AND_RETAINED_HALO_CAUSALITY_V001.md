# Formal negative-band and retained-halo causality V001

This is an analytical derivation for the declared power-log preparation, not an execution packet, numerical rank result, new seed or physical-state adoption. No coefficient, source, background, eigenproblem or matrix helper was called. The running producer and all existing controls remain unchanged.

The exact parents are `constrained_u_full_regular_coefficients_v002.py`, SHA256 `5583cb3670bbe5cd6b02761d046434619e3f0768f7abb78f0c2816ef376ac4a5`; its protocol `CONSTRAINED_U_FULL_REGULAR_COEFFICIENTS_V002.md`, SHA256 `d89311fdf49a8f54c214a06886048755abdc4489ec8d02dde0774b625bcb1ba8`; and design `CONSTRAINED_U_FULL_REGULAR_INITIAL_COEFFICIENT_PACKET_DESIGN_V002.md`, SHA256 `69415077f30cd5b6ecaa14397605d36157860bed4edc10b833ac3843aca58ae6`. This proof concerns the represented formal equations and their exact-source analogue; it does not certify the arbitrary numerical/sparse pivot ordering by inspection.

Let j denote relative order in each declared weighted coordinate and let D=j+partial_log act on its degree-at-most-two log polynomial. The physical coefficient order is j, even when its equation occurs in a shifted negative band. Work within the fixed positive radiation, opacity, charge and mode chart: hr,q0,g0,r0,Qc>0, 0<Rnu<1, KB,C>0 and positive mode weights/frequencies. With x=1/eps>0, norm=x-log(1+x)>0; hence alpha and c3=1/(norm*d0*qinf) are finite positive. No numerical value of either represented logarithm is needed for these signs.

The weighted proper generator divided by h has only two forward-order poles. Photon/polarization collisions have pole1, so their coefficient at order j is determined by residual row j-1. The slip W has pole2, so W_j is determined by row j-2. All other leading descriptor and reaction rows begin at relative order0. The scalar positive fast factors are g0/hr and g0/(r0*hr). For Fgamma2,G0,G2 the collision matrix is I-u*1^T, u=(1/10,1/2,1/10), with positive eigenvalues1,1,3/10.

The full leading photon range is triangular in multipole number after this three-component block. Fgamma_l at order j uses Fgamma_(l-1) at the same j; its following moment enters four orders later under the declared powers. G1 uses current G0/G2; higher polarization moments then use their preceding moment. The exceptional G0/G2 streaming terms also enter four orders later. Thus all photon fast coefficients at j<=5 can be determined from same-order V and already determined lower-order data. No following moment with a larger j is needed.

The W range row uses current U_j and Gamma_gamma_j, lower W coefficients, and Fgamma2_(j-1). Its factor g0/(r0*hr) is invertible. This handles the complete j=0,1 negative band as well as the higher W rows; it does not assume the entire singular fast matrix is invertible on slow coordinates.

After these range equations, the slow same-order core has the following operators, with all omitted terms already known from smaller relative orders:

`hr(D+3)U_j=Gamma_gamma_j/4+lower`,

`hr(D+3)w_nu,j=Gamma_nu,j/4-Fnu2_j/2+lower`,

`(D+2)Fnu2_j=8q0^2 V_j/(15hr)+lower`,

`hr[D+3+8Rnu/(5(D+2))]V_j=R_j+lower`.

The difference Gamma_gamma-Gamma_nu has divisor D+2. Their common component has divisor `D+2-2/(D+3)=(D+1)(D+4)/(D+3)`. Gamma_b and Gamma_phi use D+2. Higher neutrino moments use l+j+partial_log, with the following moment entering at j+2. For j>=0 every scalar diagonal above is strictly positive. Taking the highest log coefficient first makes partial_log a triangular nilpotent contact, so the same positivity gives a unique finite polynomial-log solution.

R_j for j>0 has divisor j+partial_log and is forced by U_(j-2), w_nu,(j-2) and still later phase-pressure data. R0 is fixed by the declared curvature amplitude and zero leading logs. Importantly, the Gamma operator uses the literal Rd=S+h*c*Gamma directly, not the derivative of an unconstrained R halo. It therefore cannot import R5 or R6 into a retained Gamma coefficient.

For native order j, the leading derivative equations give `z_ij=omega_i^2 sigma_j/[hr^2(D+6)(D+7)]`. The leading constraint is `n_j=hr(D+7)Z_j/L0-c3*Gamma_phi,j`, where L0=Qc*q0 and Z_j=sum_i w_i z_ij. Substitution into the reaction numerator cancels every same-order Z term exactly, leaving

`sigma_j=hr L0 c3(D+6)Gamma_phi,j/Delta0+lower`,

`Delta0=sum_i w_i omega_i^2+(C/KB)Qc^2>0`.

The equivalent leading normal Euler is `hr(D+6)(KB*q0/2)n_j=-CBAR*Qc*sigma_j`. All native diagonal factors are positive. norm enters through the off-diagonal c3 forcing, not a selection divisor. Native gradient and finite frequency enter two and four orders later, and reaction feedback reaches Gamma_phi at j+4. All modes remain in this argument.

Absolute pressure/log changes h first at relative a4; charge and sound corrections begin at a3. Multiplying those corrections by a fast pole changes a shifted row index but never makes an already range-eliminated coefficient depend on a larger physical j. They are lower-order forcing. The leading constants of the fast, radiation/core and native selection blocks consequently do not depend on log(alpha/qinf) or on a numerical rationalization of norm.

The extracted slow/reaction rows determine j0..4, photon fast rows determine j0..5, and W rows determine j0..6. A natural independent halo-coordinate basis is j5/6 of the eight non-W core fields (R,Gamma_b,U,Gamma_gamma,Gamma_nu,w_nu,Gamma_phi,V), all127 neutrino moments, all64 native z/zd coordinates and both reactions; together with j6 of all192 photon/polarization coordinates. This describes a basis by causality, not a claim about the particular free columns chosen by the sparse algorithm.

Photon j5 is slaved to free V5 and lower data. W5/6 are slaved to the corresponding free U/Gamma_gamma halo, Fgamma2 at j4/5 and lower data. Those slaved coefficients do not impose an extra condition on the independent halo coordinates. Photon shear and photon feedback into U occur one order later; W feedback into Gamma_b/Gamma_gamma occurs four/five orders later; higher-neutrino and native feedback have the delays above. Consequently no halo basis direction changes any retained j0..4 coefficient. R5/6 enter V only in its unextracted j5/6 rows, and do not enter retained Phi or Gamma.

The log-degree-three extraction does not hide another halo condition. Fixed coefficients through j3 have no logarithm; the first background log can force degree1 at j4. Free halo log-degree-two data can feed only the last extracted fast coefficients through log-independent leading factors. A background log multiplying those halo data first occurs beyond the retained rows. partial_log lowers log degree. Thus the extracted degree-three rows are compatibility identities of this orderwise construction, rather than new physical selection pivots.

This supplies an orderwise retained-uniqueness and halo-independence argument for the declared formal preparation. It does not change the source's qualification flags, claim a computed global rank, or substitute for the saved full negative-band, left-null and free-direction witnesses. Any actual incompatible row or retained free direction remains an immutable refusal and requires diagnosis against this equivalence, rather than a fitted incoming mode, softened threshold or silent deletion. Higher unextracted coefficients, exact source implementation, finite casting, finite-start adequacy and physical cosmic preparation retain their separate scope.
