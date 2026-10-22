# Root items — KMAX_TAIL_PREREG_V007_FINAL_DRAFT (unsealed)

Places where the rulings conflict, leave a clause undefined, or depend on an input not yet built. Each one gives what the draft currently does.

## RI-01 — CONFLICT (input table)

- **Clause:** `binding_inputs.driver`
- **Issue:** 0526 lists driver v010 r4 b9ae92d5; A55.2-3 make the sealed driver v010 r5 ("the sealed driver is the one the gates ran on"), not yet on disk.
- **Draft:** binds r5 PENDING_FROM_BYTES with r4 b9ae92d5 and its build record as base.
- **Sources:** 0526; A55.2; A55.3; 0530

## RI-02 — CONFLICT (BLOCKING for adoption)

- **Clause:** `GQ / production_tail.gas / T3`
- **Issue:** A55.1 puts C4T-K256 (K_big 256) in T3. RA7 requires GQ at M_s vs 2M_s <= 1e-12 P0 over [K, K_big] for every roster used. certificates_v002 (TESTED): at the registered M_s 64, DDO_C4T [4,256] reaches 5.9e-10 P0; the bound first exceeds 1e-12 at k_perp = 227.6 /kpc; certified only for K_big <= 128 (GQ_CERT_V003_KB128 24984fd5). M_s 128 passes to [K,362] (GQ_CERT_V003_KB256_MS128 b3a5390f, not registered). Compare r5 implements S8 strictly (NEW-26): every T-case uv_tail equals C4T's outside {outer, lambda_scale, source_rule}, so under that implementation M_s cannot differ for C4T-K256 alone. As written, C4T-K256 reads NUMERICS_UNCERTIFIED.
- **Draft:** keeps M_s 64 and records the conflict; options for root: (a) M_s 128 for every tail-corrected case (then GQ_CERT_V003_KB256_MS128 applies, plus an LO rebuild at M_s 128: B1 insensitive <= 1.1e-7, certificates_v002 sec 2); (b) add gas.M_s to the S8 exception set for C4T-K256 only; (c) another K_big pair.
- **Sources:** A46 RA7; A55.1; A54 S8; certificates_v002 sec 4-5

## RI-03 — UNDEFINED

- **Clause:** `production_tail.quadrature`
- **Issue:** R1's quadrature block (N_z_plus 12800, R/z eval and source extents) was set for K_big 32; no ruling restates it for K_big 128/256.
- **Draft:** defers node counts and extents to the registered P128 uv_tail configs (sha in each case block, S8).
- **Sources:** R1; A55.1; A54 S8

## RI-04 — UNDEFINED

- **Clause:** `GQ coverage edge`
- **Issue:** Compare r5 NEW-23: GQ DDO edge max(64, 2P) vs sqrt2*2P (A54 names only EPS and LO). DERIVED (not TESTED): for a cylinder outer region the gas factor P_i depends on k_perp <= K_big, so 2P = 256 covers C4T-K256, and the kept-cube corner zone reaches only sqrt2*K; certificates_v002 profiles GQ per k_perp.
- **Draft:** states the RA7/AMB-12 rule; edge for root.
- **Sources:** A46 RA7; A48 AMB-12; A54; compare r5 NEW-23

## RI-05 — CONFLICT (wording)

- **Clause:** `brackets; production_tail.P`
- **Issue:** RA4 enumerates C4T-K16 and C4T-K64 (retired R1 labels); A55.1 says "every tail-corrected case uses cylinder K_big = 128", which cannot hold for C4T-C5c (cube K_out 5), the T3 cases (64, 256) or S4T (sphere tail).
- **Draft:** RA4 list with C4T-K64/C4T-K256; K_big 128 for every case not otherwise specified.
- **Sources:** A46 RA4; A55.1; A46 RA2

## RI-06 — UNDEFINED

- **Clause:** `LO shells above 64 /kpc`
- **Issue:** R1 registers LO shells to (32,64]; A54/A55 require coverage >= sqrt2*2P (362.04) with every extended shell <= 0.005 tau (compare r5 NEW-22), but no ruling names the partition. LO_CERT_V002 (fd4fa52b) has 10 shells to 363 (per-shell max 3.95e-4 tau at (128,256]).
- **Draft:** requires coverage and per-shell bound; partition for root (proposal: LO_CERT_V002's 10 shells).
- **Sources:** R1; A54; A55.4; compare r5 NEW-22

## RI-07 — UNDEFINED (stale)

- **Clause:** `KBIG_NOT_CONVERGED next step`
- **Issue:** R1: "production K_big 64 under T3prime (32/64/128), EPS and LO to 128" is superseded by P = 128. Compare r5 NEW-24 derives "production K_big 2P under T3prime (P/2P/4P), EPS and LO to 4P" (= 256 under 128/256/512, EPS/LO to sqrt2*512); K_big 512 is outside every current certificate and the memory evidence (Codex1 0011 measured 256).
- **Draft:** "next step: RI-07".
- **Sources:** R1; A55; compare r5 NEW-24; FROM_CLAUDE3/0055 N4

## RI-08 — PENDING INPUT

- **Clause:** `run_list.contingent`
- **Issue:** Compare r5 NEW-20 (real bytes): the registered A52.3 PICARD member specs (C5H 08d350ad: admit {}, column_workers 8, ro1_workers true; D5 template 84621760) predate A53 and read invalid; their B0 EXT entries lack projection_sha256 and declared_differences.
- **Draft:** requires re-registration to the A53 shape before the seal.
- **Sources:** A52.3; A53; compare r5 NEW-20

## RI-09 — STALE

- **Clause:** `run_list.cpu_hours_estimate`
- **Issue:** R1 estimate is for K_big 32.
- **Draft:** labelled STALE; root may supply.
- **Sources:** R1; A55

## RI-10 — PENDING RULINGS

- **Clause:** `compare-lane NEW items`
- **Issue:** Compare r5 NEW-21 (S5 reading details), NEW-22 (coverage edges), NEW-25 (B4/NEW-17 scope), NEW-26 (S8 strictness), NEW-27 (label re-emission), NEW-28 (B0 record field), NEW-29 (carried notes) are lane proposals, not root text. Where a proposal is stricter and fills a gap it should become text before the seal.
- **Draft:** not integrated (only root rulings are integrated).
- **Sources:** compare r5 COMPARE_V007_IMPL_R5.md

## RI-11 — CONFLICT (wording)

- **Clause:** `B1 (Z2)`
- **Issue:** R1 says "serial route A"; the registered Z2 spec 2d5e79d0 sets route_a.column_workers 8 and compares against the PARALLEL_N8 deciding run.
- **Draft:** route A as registered in the spec.
- **Sources:** R1; A47 I4; spec 2d5e79d0 bytes

## RI-12 — UNDEFINED

- **Clause:** `B1 (Z2) token map`
- **Issue:** The pre-seal Z2 ruling derives the token map "from the driver v010 r4 pin tables only"; A55.3 reruns Z2 on r5.
- **Draft:** derives the map from the sealed driver's (r5) pin tables; root confirm.
- **Sources:** A54 pre-seal status; A55.3

## RI-13 — NOTE (base choice)

- **Clause:** `status`
- **Issue:** Claude2's R2 (a0f855db) and R3 (92092f24) drafts integrate A40-A48; 0526 names R1 as the base, so this draft starts from R1 and integrates A46-A55 independently. R3 was not used as text.
- **Draft:** R3 cited for comparison only.
- **Sources:** 0526

## RI-14 — SHOULD_FIX for root (TESTED by Claude3)

- **Clause:** `pairing_and_decidability_rule.noise_allowance`
- **Issue:** A54 S7 sets the per-row bound to 0 for sign-changing rows. Claude3 0055 N1 built a world inside V2 on the tau = 0.05 row (alternating per-row ratio 0.95 under q = 0.083) that reads E/tau 0.023, decidable, and ADOPT_TAIL, while the row's own alternating tail is 0.12 tau; the same-sign history goes to R-PAIR. Proposal there: P_i = |d_last,i| q_i/(1 + q_i) for sign-changing rows.
- **Draft:** transcribes A54 S7 as ruled; the stricter alternative is for root.
- **Sources:** A54 S7; FROM_CLAUDE3/0055 N1

## RI-15 — SHOULD_FIX for root

- **Clause:** `gates_before_any_T_result.RB_FP`
- **Issue:** Claude3 0055 N2: RB_FP has no R-PAIR path; NEW-7 or a B4 gap on C4T leaves the reading INCOMPLETE even after all three C4T R-PAIRs pass (6 runs that cannot resolve it). Root rules either a C4T rerun or RB_FP reading E from the C4T Picard member.
- **Draft:** RB_FP with unavailable E reads INCOMPLETE (A50 item 9 by analogy, fail-closed); next step for root.
- **Sources:** A48 AMB-09; A50 item 9; FROM_CLAUDE3/0055 N2

## RI-16 — CONFLICT (labels)

- **Clause:** `tests.T3; run_list`
- **Issue:** A55 names the T3 cases C4T-K64 and C4T-K256; compare r5 registers the generic labels C4T-KLO/C4T-KHI (case-block schema C2V003) and refuses retired labels (Claude3 0055 A55 follow-up 2).
- **Draft:** uses A55's names; root names the labels producers emit (e.g. KLO = C4T-K64, KHI = C4T-K256).
- **Sources:** A54 (generic T3); A55.1; FROM_CLAUDE3/0055

## RI-17 — CONFLICT (coverage edge)

- **Clause:** `gates_before_any_T_result.EPS (NGC)`
- **Issue:** R1 states NGC EPS coverage [2, 32]; the NGC N3 case uses cylinder K_big 32, whose node |k| reaches sqrt2 * 32 = 45.25, and the module's unit shells end at ceil(sqrt2 * K_big) = 46 (certificates_v002 coverage note; its EPS record covers NGC [2, 46]).
- **Draft:** NGC [2, 46].
- **Sources:** R1; A52.5; certificates_v002
