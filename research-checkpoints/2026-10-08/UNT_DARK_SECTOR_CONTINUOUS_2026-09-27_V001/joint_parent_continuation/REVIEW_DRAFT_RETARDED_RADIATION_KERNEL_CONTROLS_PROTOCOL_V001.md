# Retarded radiation kernel controls V001

Prospective 2026-10-06 04:51 UTC. This is the first reusable mathematical control packet for the new same-action Volterra method. Root alone launches `constrained_u_retarded_radiation_kernel_controls_v001.py --execute` after full static review and fresh process ownership. The author does not run numerical kernels, quadrature, old modules, trajectories or benchmarks. This packet consumes no physical forcing history and makes no galaxy or cosmological transfer prediction.

## Fixed mathematical contract

Conformal eta is a length; k is inverse length and Gamma is inverse length. The normalized panel is Delta=1 length unit, b=k Delta and a=Gamma Delta. For l=0,1,2, derivative r=0,1,2,3 and source power p=0,1,2, retain

    K(l,r,p;a,b)=integral_0^1 exp(-a v) v^p j_l^(r)(b v) dv.

The full fixed census has b=(0,.125,1,4,16,64), a=(0,1e-8,.1,1,10,48,100,1e6): 1,728 rows. Every row includes panel Gauss16 and32, independent angular Gauss128 and256, both angular imaginary remainders, and the panel tail bound. No row is excluded by size, sign, opacity, Bessel value or an expected physical result.

The panel method evaluates spherical Bessel derivatives by their factorial series for |x|<4 and literal sin/cos rational formulas otherwise. The coefficients are differentiated symbolically by the source helper, through r=3. Composite Gauss panels have at most8 units of phase/opacity span. For a>48 transform t=a v, integrate0..48, and retain the omitted-tail bound exp(-48)/a; the bound follows |j_l^(r)|<=1 from its angular representation and v^p<=1. It is an explicit absolute kernel bound, not a physical source-memory truncation bound.

The independent method integrates over mu using j_l^(r)(x)=i^l integral_-1^1 P_l(mu)(-i mu)^r exp(-i x mu)dmu/2. Its radial polynomial moment is evaluated directly as I_p(z)=integral_0^1 exp(-z v)v^p dv, z=a+i b mu, through a power series near zero and the exact recurrence I_p=(p I_(p-1)-exp(-z))/z otherwise. This route uses no spherical Bessel helper or panel quadrature. Angular128/256 and panel16/32 are separately compared. All four row gates have fixed2e-10 allowance, with2e-12 angular-reality allowance; their observed errors and all failures remain saved. These are kernel arithmetic tolerances, not relaxed tolerances for the active527 physical trajectory gates.

## Primitive and endpoint controls

Retain j_l^(r) versus independent angular projection at nine fixed arguments0,.125,1,3.999,4,8,16,32,64 (108 rows). The mixed absolute/relative error gate is2e-11. Verify the exact zero-argument derivatives and Thomson collision endpoint terms, including zero photon-monopole quadrupole source, intensity l2 Pi/10, polarization l0 Pi/2 and l2 Pi/10. No source term is dropped.

Use primitives J0=Si(x), J1=-j0(x), J2=Si(x)/2-3j1(x)/2. For positive x>8, Si(x)=pi/2-cos(x)F(x)-sin(x)G(x), with positive Laplace integrals F=x^-1 integral exp(-u)/[1+(u/x)^2]du and G=x^-2 integral u exp(-u)/[1+(u/x)^2]du. Laguerre32/64 are checked against independent composite Legendre16/32 on u0..64 plus the explicit e^-64/x and65e^-64/x^2 tails. At x<=8 use the fixed factorial series. The twelve fixed Si arguments are0,.125,1,4,7.999,8,8.001,16,64,256,4096,100000; save both routes and every difference, tolerance2e-11.

Check all three primitive increments over widths.25,1,4 at starts0,4,8,64,4096,100000 against direct Gauss32/64 Bessel integration (54 rows), tolerance2e-11. This tests finite increments rather than differencing large primitive constants numerically to infer derivatives. High-x primitive controls are not a claim of a full large-phase angular quadrature.

## Exact staged scope and custody

The formulas transport a supplied angular state and polynomial source panel; future coupled calculation must solve the true low moments, baryons, physical metric and every native kinetic mode together. Variable visibility/source-panel interpolation, actual source-memory variation, gas/thermal/START errors and completed-parent full-state comparison remain explicit controls of that following worker. No fixed-source line-of-sight table is labeled an exact galaxy solver. No calibration, HYREC call, physical history or primordial fit occurs here.

The ten exclusive immutable checkpoints are ordered BESSEL, PRIMITIVES, then one PANEL bundle per each of eight opacity values (ten CP/COMMIT pairs). Each root journal event and commit binds source, manifest, input hashes, root PID, stage, index and payload bytes. This small packet has no resume path; any existing runtime prefix is preserved and refused, including incomplete files. Canonical JSON is encoded before exclusive open; every saved scalar is a built-in type. Publication occurs after full checkpoint schema/census/hash and root journal checks. Source and all consumed parent files are rehashed before and after final RESULT/REPORT/RECEIPT. Runtime is bounded by the fixed census; no process timeout or kill is used.

The namespace is CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001_*, distinct from the active early-transfer worker. All rows, checks, maxima and failures are retained, without retuning a method after outcomes. The report will state arithmetic PASS/FAIL only. It does not certify the following coupled field solution, observational agreement or a primordial state.

## Frozen analytical/source parents

| Parent | SHA256 |
|---|---|
| CONSTRAINED_U_GALAXY_SCALE_REGULAR_SEED_AND_RETARDED_RADIATION_KERNEL_V001.md | 0a2a64f56ee544cd0b4f0c0ce21240fb8d4cde7ebcb877231519e6f02fade639 |
| CONSTRAINED_U_CLOCK_GRADIENT_EARLY_ADIABATIC_HIERARCHY_V001.md | 1014e8689d23c35b47c2e47b7e4bed2b2b3f0f329aca061b5df3586c249fc7d2 |
| constrained_u_clock_gradient_early_transfer_v004.py | a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07 |
