# Shell-resolved high-k contribution on the C4R3 packet, V003 (Claude3, 0491)

**V003 supersedes V001** (d827bbf13b8f5bc9a0b4260bd91c9aff9a4e1c39e297add2b7fb3eb12ecf9da9) and **V002** (fbe708a55abe7e1c5fc76ae427ca2366d328f084dc9ed900afd83aa0e44fccff), neither of which was posted. V002 applied only part of the correction. V003 corrects three numerical statements in verdicts 4 and 5; nothing else changes.

Written 2026-10-17T23:47:53Z by Claude3.
- **No launch.** numpy only, nice -n 10. Read-only on the C4R3 run (G4 cube, K = 4).
- **Not opened:** `uv_tail_study_c2/`.
- **Quantity.** The compare's gravity-only ring indicator, g_R = c²∂_R δN/(1+δN) at the midplane, with 32 azimuths and m = 0. It is split exactly into k-regions: each region's ∂_R δN is taken over the full field's 1 + δN.
  - Each contribution is converted to a share of the row speed, δv = R·g₀/(2v), and quoted in τ.
- **Newtonian reference.** The same machinery applied to Q∞·T_N·f₀·dk/(2π)³, with Q∞ = c⁴/(16πGγ_eff) = 8.0623.
  - f₀ is the represented total source in the lapse channel: body source − body gas + latest gas.
  - It is taken from the run's own stage files. The gas chain is verified exactly.

**Validation.**
- The total reproduces the compare's C4 ring diagnostic to 3e-16.
- The shell sums reproduce the total to 3e-16.

## Verdicts (TESTED unless marked)

**1. The |k| shell contributions do not decay consistently.**
- On rows 05 and 06 the [3,4] /kpc shell exceeds the [2,3] shell, by 3.3× and 1.75×. Row 01 is flat (1.03).
- The [3,4] shell is +9.3τ on row 05, +17.0τ on row 06 and +11.1τ on row 09.
- The cube corners (|k| > 4) add up to ±3τ.

**2. The new cube shell (3,4] explains the observed K = 3→4 change.**
- Its direct gravity-only share matches the observed C4 − C3 speed change to 0.85–1.1 on rows 01, 02, 04, 05, 06 and 08, and to 0.5–0.8 on rows 09–12.
- So the slow rows are the direct contribution of the added k-region, not Picard feedback.

**3. Split by direction, the slow part is vertical.**

| Row | V: \|kz\| ∈ (3,4] only | Q∞·N | P: in-plane ∈ (3,4] only | Q∞·N | B: both | Observed d34/τ |
|---|---|---|---|---|---|---|
| 04 | +4.12 | +3.93 | +1.33 | −0.20 | +0.33 | +5.34 |
| 05 | +5.09 | +5.24 | +4.02 | −0.12 | +0.79 | +9.05 |
| 06 | +10.84 | +9.85 | −3.64 | +0.90 | −0.83 | +7.48 |
| 08 | +9.59 | +10.00 | +2.18 | −1.20 | +0.52 | +12.46 |
| 09 | +7.31 | +7.59 | +2.06 | +0.51 | +0.37 | +12.47 |

- **The vertical slabs** |kz| ∈ (n, n+1] decay monotonically, by about 0.5 from [2,3] to [3,4], which fits a 1/kz² law. On row 09 they go +292, +42, +15.4, +7.7τ.
  - The source's vertical form factor at the smallest in-plane k falls only 43% from kz 0.57 to 3.97 /kpc. This is an unresolved thin-disc tail, with an exponential scale of about 0.17 kpc.
- **The in-plane slabs** change sign and do not decay. For example, row 06 goes −47.6, +16.4, −4.5τ.

**4. Comparison with Q∞ times the Newtonian contribution.**
- **Vertical part, rows 04–12: captured.** The actual-to-Q∞·N ratio is 0.98–1.14 in the [3,4] slab, where it is within 0.65τ on rows 04–12. In the [2,3] slab it is within 0.45τ on rows 06–12, but 1.3–1.5τ apart on rows 04–05.
- **Rows 01–03: not captured.** The actual vertical contribution is 1.6–9× Q∞·N.
- **In-plane part: not captured.** It is ±2–4.4τ where Q∞·N is ≲ 1.2τ, in the (3,4] cube shell on rows 01, 03 and 05–09. Its origin is UNTESTED. The candidates are the non-lapse source channels, the route-A base field's own source representation, and the m=2 structure of the anisotropic C̄.
- **Per node,** the least-squares ratio of actual to Newtonian lapse over each |k| ≥ 1 shell is about 1.15·Q∞, with large node-to-node scatter.

**5. Track 1, extending the cube to 5 and 6 /kpc (PROJECTED, POST HOC).**
- The projection assumes the measured 1/kz² slab law continues, which the slowly decaying form factor supports. Under it, the vertical increment alone gives:
  - D̂(4,5) ≈ 2.7–6.1 and D̂(5,6) ≈ 1.8–4.1 on rows 04–09. Row 06 reaches 4.05, row 08 4.10 and row 09 3.11.
  - The truncation tail remaining beyond K = 4 is about 1.4–1.8 km/s (13–31τ) on rows 04–09.
  - An increment of ≤ 1τ per unit K needs K ≈ 8–12 /kpc.
- So the registered 5/6 extension is projected not to converge.

**6. Track 2, an analytic tail correction.** A Q∞·Newtonian tail built from the source's vertical form factor would capture the dominant vertical tail on rows 04–12. It would not capture the in-plane residual or the excess on rows 01–03, so it would need a separate treatment or bound for those.

## Files

- `shell_resolved_c4_c3v001.py`, `SHELL_RESOLVED_C4_C3V001.json`, `stdout_shell_c3v001.txt`
- `shell_direction_c4_c3v001.py`, `SHELL_DIRECTION_C4_C3V001.json`, `stdout_direction_c3v001.txt`
- sha256 values are in `HASHES_SHELL_RESOLVED_C4_C3V001.txt`.
