# Origin of the residual that Q∞·Newtonian misses on the C4R3 packet, V002 (Claude3, 0493)

**V002 supersedes V001** (1c6a51e37d0429d4cafdd07678a9546186ba011dcba0424f790b39a139a0bc1a), which was never posted. It corrects the all-k row of the shares table: the ranges of r_total and of the candidate 2 share. Nothing else changes.

Written 2026-10-17T23:59:01Z by Claude3.
- **Hygiene.** No launch; numpy only, nice -n 10. Read-only on the C4R3 stage files. `uv_tail_study_c2/` was not opened.
- **Script.** `origin_c3v001.py`, with output in `ORIGIN_C3V001.json` and `stdout_origin_c3v001.txt`. The k→0 check is in `stdout_k0_ratio_c3v001.txt`.

## Exact structure of the field (TESTED from bytes)

U is the run's own per-node unit response: all 10 fields, already weighted.

| Identity | Relative error |
|---|---|
| offset packet = U·δsource | 0.0 |
| each feedback packet = U·Δgas | 0.0 |
| refreshed_17 = refreshed_13 + U·Δgas_17 | 3e-14 |
| total = G4 + U·(f_now − f_G4) | 2.3e-16 |

Here f_now = body − body gas + latest gas, and f_G4 = body − offset δ.

- **Every route-B source is lapse-only.** Body, offset δ and gas have components 1–9 exactly 0.
- **The route-A base G4 is exactly U·s(k) with one scalar s per node.** The spread of G4_j/U_j across the 10 fields is 2e-16 at the median node and 7e-16 at the 99th percentile.
- So route A's base is the same linear response, applied to its own lapse-only source representation s(k).

## Shares

Residual r = actual − Q∞·T_N·f_now·dk/(2π)³ is split exactly into three terms. The split closes to ≤ 4e-15τ in every region.
- **Candidate 2:** G4 − U·f_G4.
- **Candidate 3:** (Q − Q̄(|k|))·wT_N·f_now.
- **Candidate 4:** (Q̄(|k|) − Q∞)·wT_N·f_now.

| Region | r_total (τ), rows 01..12 | Candidate 2 share | Candidates 3+4 |
|---|---|---|---|
| (3,4] in-plane-only, part (a) | +2.49 +0.40 −4.20 +1.53 +4.14 −4.54 −4.34 +3.38 +1.55 −0.69 −0.39 +0.09 | **100%** | ≤ 0.005τ |
| (3,4] kz-only | +1.20 +3.24 +2.06 +0.18 −0.15 +0.99 +0.60 −0.41 −0.28 +0.07 +0.11 −0.02 | **100%** | ≤ 0.005τ |
| kz slab (2,3], rows 01–03, part (b) | +2.54 +5.35 +2.66 | **100%** | ≤ 0.005τ |
| kz slab (3,4], rows 01–03, part (b) | +1.71 +3.29 +1.21 | **100%** | ≤ 0.005τ |
| all k | rows 01–08: +13.9 to +34.0; rows 09–12: +1.1 to +9.5 | rows 01–08: 100–118%; rows 09–12: 129–189% | candidate 4: -0.02 to -2.92τ, at low k where Q < Q∞; candidate 3: -0.01 to -0.66τ; these offset part of candidate 2 |

**Candidate 1, non-lapse channels: 0, TESTED.** Every source and the base are lapse-only.

**Candidates 3 and 4: about 0 in the tail, TESTED.**
- At |k| 3–4 /kpc, Q = U₀/(wT_N) is 8.0614–8.0621 along x, y, z, xy, x−y, xz and xyz, against Q∞ = 8.0623. That is |Q − Q∞| ≤ 1e-3.
- Im Q/Re Q ≤ 6e-17.
- Q̄ is 8.0588 at 1.5 /kpc and 8.0619 at 3.5 /kpc.

**Candidate 2, source representation: all of (a) and (b), TESTED.** Route A's base source s(k) differs from route B's analytic f_G4(k):

| k-region | s/f_G4, median (10–90%) |
|---|---|
| k → 0 | **1.0279** (route A carries 2.8% more total lapse source) |
| k_perp < 0.5 /kpc | 1.037 (1.028–1.057) |
| k_perp 1–2 | 1.13 (0.60–1.64) |
| k_perp 2–3 | 1.05 (0.88–1.12) |
| k_perp 3–4 | 1.02 (0.87–1.06) |
| k_perp > 4 | 0.95 (0.87–1.03) |

So the two routes differ in normalization and in their in-plane form factor. Which representation is the registered physical source is UNTESTED and is root's decision.

## What a tail correction needs to bring rows 01–12 within 1τ

- **The linear operator is not the issue.** Q(k) = Q∞ to 1e-4 at |k| ≥ 3 /kpc, so a Q∞·T_N tail is exact for it.
- **The source is the issue.** The tail must use the source the field actually carries, f_eff = f_now + (s − f_G4).
  - With f_eff, the uncaptured remainder in the (3,4] shell is ≤ 0.005τ on every row (TESTED).
  - With route B's analytic f_now, it misses up to ±4.5τ in-plane, and +1.2 to +5.4τ per slab on rows 01–03.
- **Two ways to get there:**
  - **(i)** An analytic evaluation of route A's source construction at any k, giving an analytic in-plane and vertical form factor of s beyond K.
  - **(ii)** One source representation for both routes, with route A's base built from route B's analytic source. Then the analytic vertical Q∞·N tail suffices, with the remainder at the candidate 3+4 level.
- **k_xy resolution.** The residual is not under-resolution of the field in k_xy. If route A's source is sampled, its in-plane spectrum must be resolved up to the largest k the tail uses. That requirement is UNTESTED quantitatively.
- **An explicit bound alone cannot reach 1τ.** The unmodelled in-plane part reaches 4.5τ in a single unit-K shell.
- **Separately, the 2.8% normalization difference at k → 0** between the routes is a source-consistency question for root.
