# Result

Target status:
`PASS_CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT`, `17/17`.

| N | `J_connector` | capacity / N=0 | `tau` | tau / tau0 |
|---:|---:|---:|---:|---:|
| 0 | `0.5000000000039362` | `1` | `1.222689868854405` | `1` |
| 1 | `0.42815973374869076` | `0.8563194674906403` | `1.3455677498194254` | `1.1004979955220782` |
| 2 | `0.36531361324457556` | `0.7306272264833994` | `2.971600967337824` | `2.4303799704515874` |
| 3 | `0.3308471281165849` | `0.6616942562279607` | `2.86146468598496` | `2.3403029328001215` |

Connector capacity decreases strictly over the measured `N=0..3` window.
The formal linear zero is `N=8.620405864210246`, outside the L8 rail's
finite write capacity, so `N_crit` and pinch-off remain undefined.

First-arrival time is not monotone because `tau(3)<tau(2)`. Thus this packet
does not establish a monotone accumulation delay. In all cases `tau` is an
operational graph first-arrival time, not gravitational time dilation or
Shapiro delay.
