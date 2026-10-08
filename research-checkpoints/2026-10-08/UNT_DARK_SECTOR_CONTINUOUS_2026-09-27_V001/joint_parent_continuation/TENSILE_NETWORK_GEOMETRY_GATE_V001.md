# Tensile network geometry: prospective material gate V001

2026-10-05 UTC. New calculation after the completed kinetic/Coulomb gate; no previous worker is rerun. Two small disjoint local workers are permitted under the user's updated concurrency instruction. Root owns only these new tensile-geometry files.

## Three mechanical constructions, with assumptions counted

The question is which actual tension geometry can supply negative pressure and stable waves, without choosing a favorable function of cosmic volume. This gate adopts conserved, cold, isotropic, affinely deformed material elements. Their physical reference census and tension are fixed. This is a declared effective material realization, not an already derived BS11 network phase, formed universe or galaxy law.

For an isotropic central-bond potential U(s), fixed complete reference/rest R, E=R+U, V=V0s^3:

pV=-sU'/3; KV=(s²U''-2sU')/9; muV=(s²U''+4sU')/15.

Thus mu=3K/5-6p/5. Requiring K>0, positive enthalpy and causal longitudinal waves implies 9K<=5rho+13p, hence w>-5/13 and component q>-1/13. The K>0 premise is load-bearing: a solid with negative bulk can have stable acoustic waves when actual shear compensates it. This is not a bound on all UNT or all solids.

1. Hookean bonds: U=A(s-1)^2/2 from actual bond extension squared. At s=9/5,R/A=21/20: E/A=137/100, active V/A=-7/100, KV/A=1/25, muV/A=3/5, enthalpy V/A=89/100, cL²/c²=84/89, cT²/c²=60/89, q=-7/274. This is an instantaneous conditional covariant material witness. Large strain and relativistic stiffness do not follow from a literal nonrelativistic spring approximation. A relaxed reference-to-witness history is not supplied.
2. Constant-tension links: E(F)=R+D<|F n|>, with normalized fixed sphere measure. At F=sI, E=R+Ds; w_link=-1/3 and active E+3pV=R, so no acceleration from the cold links alone.
3. Constant-tension surfaces: E(F)=R+D<|cof(F)n|>. D is the owned reference tension times reference area, fixed by the material census. This area follows the physical surface element, not a picked volume-energy function. At F=sI, E=R+Ds², pV=-2Ds²/3, KV=-2Ds²/9, muV=4Ds²/15, MV=2Ds²/15. The enthalpy is R+Ds²/3. For R>=0, both acoustic modes are stable and causal despite negative bulk; at R=0, cT²/c²=4/5,cL²/c²=2/5. Acceleration under Einstein/common-metric homogeneous matching requires Ds²>R, after all additional donors and ordinary matter are counted.

Own surface derivation: under F=sI+epsilon a outer m, the cofactor is exactly s²[I+(epsilon/s)((a dot m)I-m outer a)]. The rank-one second derivative is D[4|a|²|m|²-2(a dot m)²]/15. It gives the quoted transverse and longitudinal coefficients after multiplying by s²/V. This includes prestress and is not obtained by retaining only the longitudinal bond derivative.

The covariant tension premise is a Nambu-Goto worldsheet for links or worldvolume for surfaces, coupled to the same metric as ordinary probes. Static lapse coupling is linear at fixed configuration: uniform lapse contact is zero. Geometry alone does not establish a critical gravitational susceptibility, environmental MOND response, physical clock normalization, native record origin, topology retention or formation. Existing native quantum/source and Coulomb failures remain.

Relevant primary context: [Battye et al. 2005](https://arxiv.org/abs/hep-th/0501244) calculates stability of cold isotropic string/membrane solids; [Battye et al. 2006](https://arxiv.org/abs/hep-th/0512207) treats anisotropic and non-affine lattices; [Avelino et al. 2006](https://arxiv.org/abs/astro-ph/0612444) finds scaling rather than frustration in its tested junction models. These are existing physical constructions, not evidence for UNT formation or superiority. The current gate derives its finite geometry directly above.

## Frozen gates before execution

One small NumPy process, bundled runtime, one BLAS thread. Exclusive outputs and protocol/source hashes; no data download, optimization, abundance/history choice or earlier driver import.

- Exact rational Hooke witness and central-bond identity above.
- For strings and surfaces, sphere grids12x24 and24x48; s=[0.8,1,1.8,2], R/D=[0,1,4]; normalization and isotropic moments tolerance1e-11.
- Directions (a,m)=(ex,ey),(ex,ex), and fixed normalized a=(1,2,-1),m=(2,-1,3). Freeze relative strain steps [.01,.005,.0025]; Richardson quadratic extrapolation of the last two steps. Rank-one energy Hessian tolerance2e-7, normalized by max(1,|exact|).
- Pressure/bulk by log-volume differences with the same frozen steps and extrapolation, tolerance2e-7. At nonzero prestress, bulk is (E_logVlogV-E_logV)/V. Check mu,M and acoustic ratios from the same energy; no free shear interpolation.
- Acceleration and causality classifications are outcomes, not pass conditions. R is an illustrative declared co-moving rest control, not an adopted ordinary-matter inventory or cosmological calibration.

Completion qualifies material geometry/arithmetic only. Exact next action is native source/contact and formed-state matching, including any required area or non-affine degree, with energy counted once. All Stage3 lanes remain open.
