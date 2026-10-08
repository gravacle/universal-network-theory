# Uniform prepared annulus: independent analytical review

2026-09-29. Read all of `UNIFORM_PREPARED_ANNULUS_RELEASE_V001.md`, SHA-256
`973e8fbdd24233784cde4bf7e6b18d0d5482e75b62179c7ee15d9e62bb5fc951`.
The release reduction is accepted under its explicit initial-data and boundary
assumptions. No numerical worker, source modification or new state was used.

The decisive independent check is that the retained-mode kinetic energy has
no lapse dependence **at fixed canonical fields**. With
`rho/C=E0-Bh+aBh'+sqrt(f)/r²*(r²Bh')'`, the variation
`delta a=sqrt(f) eta'` therefore gives

    delta rho/C = a B h'' delta a
                         +sqrt(f)/r²*(r² B h'' delta a)'
                =sqrt(f)/(N r²)*(N r² B h'' sqrt(f) eta')'.

The minus sign in `F_N` follows from the defined `F=GR-rho`. Keeping both the
local `aBh'` contribution and the polarization divergence is essential;
their combination supplies the derivative of N. There is no extra
zeroth-order eta term. This also verifies the surviving uniform time-
normalization direction before fixing boundary lapses.

At the initial moment, zero extrinsic curvature and zero geometric velocities
remove the first derivative of the gravitational curvature-quadratic term and
the volume-expansion contributions. Uniform physical x,v means spatially
varying canonical mode momentum, not uniform canonical momentum. The mode
equation gives `E0dot=h Bdot`, `Bdot=N VB`; momentarily resting dust or vacuum
has `rho_bdot=0` under the stated no-production/boundary assumptions. The first
two local energy derivatives cancel, yielding exactly the same weighted
divergence with `Bdot h'` in place of `B h'' sqrt(f) eta'`. Consequently

    N r² [B h'' sqrt(f) eta' + Bdot h'] = K

has the stated sign and normalization. At fixed boundary lapse values,
`eta=0` at both endpoints and `K=(integral A/D)/(integral 1/D)` follows
directly, with `A=N²r² VB h'` and `D=N r² B h'' sqrt(f)`.

For continuous D bounded away from zero with one sign, the homogeneous
Dirichlet problem has only the zero solution. This is invertibility of this
initial linearized constraint, not a stability or long-time regularity theorem.
The `h''=0` limit cannot be inverted: it instead imposes the separately stated
compatibility condition. Small nonzero h'' may make the unique lapse rate large.

In the weak-compactness limit, the ratio of the two elementary quadratures
gives `eta'=(VB h'/(B h''))*(r_in*r_out/r²-1)`. For the stated radius ratio,
the bracket is +1 and -1/2 at the two ends, respectively. Positive B and VB
with negative h'' therefore force opposite initial acceleration-rate signs;
shrinking the annulus does not suppress that leading rate. This is a sharp
oracle for the prospective calculation, not an assertion that exactly flat
f=1 solves the original energy constraint.

The mode action identity also checks: differentiating the instantaneous orbit
energy gives `de=omega dI-b< x > dh`, whereas the actual local trajectory has
`de=-b x dh` at this expansion-free instant. Thus
`D_proper I=b(<x>-x)D_proper h/omega` has the stated sign. Its orbit label must
be computed at the actual embedded h, not silently retained from a different
clamp. The negative local interaction-energy shift and retained contact must
not be double-counted as additional ADM preparation work.

The calculation can decide initial compatibility and whether a quasistatic
approximation is locally plausible for the actual saved state. It does not
already evolve the annulus, close its exterior/center, fix a physical clock or
length calibration, or identify the constant K with a measured energy current.
No algebraic blocker was found.
