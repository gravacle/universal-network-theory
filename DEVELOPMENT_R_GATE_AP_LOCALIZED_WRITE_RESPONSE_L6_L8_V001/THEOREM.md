# Direct finite localized-write response at L6 and L8

The authenticated terms-off source slice writes `W_R=1/2` into even site zero
of one connected component. After source shutdown, the original owner-once
support evolves at `kappa=pi/2`. Direct full-space calculations reproduce the
sealed unperturbed occupation/current vectors and compare complete perturbed
and baseline histories.

| raw finite record | L6 | L8 |
|---|---:|---:|
| terminal `sum Delta q` | `0.5000000000000504` | `0.5000000000000144` |
| `sum_e |Delta J_e|` | `1.8139724403785475` | `2.045357955508373` |
| `max_e |Delta J_e|` | `0.18634272297931076` | `0.18700819005396008` |
| total absolute-throughput change | `+0.3087514330085446` | `+0.4509448411799237` |
| connector absolute-throughput change | `-0.09115966508399204` | `-0.09366810066406672` |
| response-weighted mean edge radius | `1.2640345991204631` | `1.4401637115338672` |
| effective responding-edge count | `13.803153785538104` | `15.636993901062127` |
| full differential residual L1 | `1.6314727346866675e-12` | `1.6536771951791707e-12` |

Every edge has nonzero differential current at both sizes. The edge-shell L1
profiles are:

- L6, radii 0--3: `0.5036822, 0.4729591, 0.6920286, 0.1453026`;
- L8, radii 0--4: `0.5045314, 0.4844919, 0.7561383, 0.2519039, 0.0482926`.

Thus the lower-size disturbance is neither uniform nor a monotone radial
decay. It spreads across every finite shell, has a reproducible radius-two
aggregate maximum, and is much smaller on the farthest edge shell. This is a
finite oscillatory profile. It does not establish a locality law or physical
boundary reflection; the radius is shortest-path distance on the supplied
support only.

The source half-record is retained globally within numerical controls, and
the source-inclusive differential ledger closes to raw L1 about `1.7e-12`.
Those remainder terms are unassigned, not defects. L10/L12/L14 and the full
ladder classification remain open, as does Gate A-P. No grid, continuum,
Ward structure, phase, graviton, or gravity is promoted.
