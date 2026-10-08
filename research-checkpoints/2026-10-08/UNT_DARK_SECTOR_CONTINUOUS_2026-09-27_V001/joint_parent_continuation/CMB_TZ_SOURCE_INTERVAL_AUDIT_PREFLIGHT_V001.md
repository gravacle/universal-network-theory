# Temperature–redshift source intervals: independent preflight V001

Accepted unchanged as a conditional endpoint translation. Full input JSON, protocol, worker and the inherited continuous-source analysis were read. No producer was imported or executed.

Reviewed SHA256 identities:

- `CMB_TZ_SOURCE_INTERVAL_INPUTS_V001.json`: `a7f2fd7f0ac34d11b1eb2c63d6f77f5b6d4df9cb4df1e969a1bb1cc88b4ce171`.
- `CMB_TZ_SOURCE_INTERVAL_PROTOCOL_V001.md`: `be71d5870829f479fec95347a3e0e5257839fd7122c1b879e863558f79923f47`.
- `cmb_tz_source_intervals_v001.py`: `916a6d72672dfce6e3df1953c5fa4e567e612f5c7a29d1437d0e6e46900c127b`.
- Inherited analytical source: `b4cb12de9a11767f91b6441d860711e09f4f8e64ec7d1517c5065e7ffbe50ad4`.

The exact adopted Planckian/redshift interface gives dln(aT)/dt=u, hence L=ln[T0(1+z)/Tz]. Redshift-rescaled energy and comoving-number endpoint ratios give F_E=1−exp(−4L), F_N=1−exp(−3L), both increasing functions of L. Code signs, monotone temperature extrema, marginal-error rectangle corners, constant-beta mapping, half-energy oracle and negative-source retention are correct. Intersecting with L>=0 is necessary for pointwise nonnegative production, but does not itself demonstrate a nonnegative time-resolved rate. Net fractions do not measure gross photon replacement.

The fixed summaries were independently checked against primary pages on 2026-09-29:

- [Fixsen](https://arxiv.org/abs/0911.1955): combined T0=2.72548 +/-0.00057 K, not an independent second spectrum likelihood.
- [Muller et al.](https://arxiv.org/abs/1212.5456): non-LTE/MCMC 5.08 +/-0.10 K at quoted68% confidence.
- [Kotani et al., pinned v1](https://arxiv.org/html/2509.20760v1): 5.13 +/-0.06 K and actual absorber z=0.88582; same PKS1830 SW object, conditional LTE/weak-collision/covering-factor/variability assumptions. These two measurements must not be multiplied as independent likelihoods here.
- [Riechers et al.](https://arxiv.org/abs/2202.00693): 16.4–30.2 K one-sigma interval at z=6.34, with water/starburst radiative-transfer assumptions.
- [Saro et al.](https://arxiv.org/abs/1312.2462):158 clusters over0.05<z<1.35, SPT-only exponent0.017 with−0.028/+0.030. The paper denotes it alpha; the input's beta is the explicitly identical exponent convention, not another parameter. No combined-literature value is used.

The code is stdlib/stdout-only, checks project and file binding before run, and freezes all four local inputs. No free fitting interface or new observation threshold exists. It retains the declared central-temperature result separately from the rectangle of reported marginal errors; neither that rectangle nor endpoint clipping is promoted to joint confidence coverage.

This tests an adopted net source history under ordinary photons/redshift and measurement interpretations. It requires neither inflation nor a zero-scale-factor origin, but does not derive a native photon source or invalidate balanced replacement. No statistical significance beyond the supplied summaries or global cosmological exclusion is licensed.
