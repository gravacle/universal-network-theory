# Finite-pressure BAO/ruler worker — independent preflight

Accepted by full read and focused pre-outcome read of the final changes, without importing or running the producer. This binds the following settled bytes.

- `finite_pressure_bao_ruler_v001.py`: `b59ab0f88e39234929eb6fa4d0a53bba0b1bf4dc4fbd9891b704b5cd89e19bf1`
- `FINITE_PRESSURE_BAO_RULER_PROTOCOL_V001.md`: `4b5c21615b8723473277ec32a8eadefd620457a21d63dc9a63880c6c0053c384`
- `FINITE_PRESSURE_BAO_AND_RULER_DESIGN_V001.md`: `891c7b0c2d0a91872bdde2988e8bf4414762beda836be700a2197a861160f00f`

## Checked algebra and implementation

The dimensionless action is f(r)=r*bar(r), with bar(0)=1/2 and f'(r)=(1+r)/(2 Omega). Thus t=log(r/r1) gives dA/dt=A*r*f'/(3f), exactly the implemented `A*lam/3` factor in all distance and horizon integrals. The monotone endpoint bracket is correct. The positive pressure integral and cI2 derivative have the proper factors; the separately implemented dust limit has zero pressure/hard horizon but nonzero gravitating energy.

The inherited s-to-r conversion r=2s^2/(1-s^2), inverse energy normalization and cancellation among the four spectrum/numerical copies are correct. This cancellation concerns homogeneous normalized history, not their physical gap, source scale, vacuum matching or spatial response. All 67 inverse points and five contexts remain represented, including local-table qualification and point roles.

Cholesky whitening, nonnegative one-parameter ruler profiling, derivative sign at the amplitude boundary and covariance contributions are consistent. The exact final DESI DH,DM order is retained. The same-background dust comparator has the same total dust coefficient and ordinary radiation; historical zero-radiation shapes are checked separately. No hidden refit of the inverse point, background, scalar gap or vacuum occurs.

The ordinary photon-baryon sound speed and hard cI2 are kept separate. Integration units c/Hcal are Mpc. The positive early-tail bound follows by integrating the lower density Omega_b*A^3+q4*A^4 and independently the total-dust lower bound; it does not continue an assumed photon a^-4 history through annihilation. Inverting the truncated integral at target and target-minus-tail has the correct lower/upper endpoint orientation. Null/outside-domain cases are not replaced with a standard drag epoch.

## Custody, controls and scope

The pinned inverse and old BAO freeze manifests already contain the relevant flattened ancestry, including the exact 13-vector and covariance files. Their raw and payload links are checked before use. The new worker writes only stdout, reads no remote data, imports no ancestral producer and sets single-thread numerical limits. Freeze mode performs no prediction. The first finite row is a fixed-order timing benchmark, not an outcome-selected physical case.

Prospective independent angle/distance/acoustic quadratures, fresh-node Simpson controls, synthetic covariance recovery and output qualification are distinct from an empirical success criterion. The suggested direct A=1 comparison to saved original action/frequency/w/cI2 was added at the existing material tolerance and checked by focused read. The hard sound speed now takes the square root directly, without clipping. The new predeclared `run-background 0..4` interface changes only sequential packaging: each subset reports its identity and 67 histories; all five are required for the complete 335-history census. Benchmark-only status is explicit. These changes introduce no new scientific selection or tolerance. This note is not a certification of future numerical outcomes.

The only fitted BAO freedom here is the exposed common ruler amplitude for each retained conditional point. The computed endpoint is a **required** drag epoch, not recombination. Massless-neutrino and post-annihilation thermal history, conditional scalar action and BBN-proxy inputs remain assumptions. No CMB spectrum, acoustic-ruler prediction, native-photon origin or universal model-selection result follows. The external HyRec implementation mentioned in the design was not inspected or qualified by this preflight.
