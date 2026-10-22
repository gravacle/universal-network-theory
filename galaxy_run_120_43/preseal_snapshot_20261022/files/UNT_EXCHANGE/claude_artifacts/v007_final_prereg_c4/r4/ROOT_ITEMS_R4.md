# Root items r4: KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4 (unsealed)

RI-19 to RI-26 are resolved by A81. One item is open: RI-27. Nothing else is open.

## RI-27: CONFLICT (pin cycle) (OPEN)

- **Status:** OPEN
- **Clause:** `seal_slots.compare; seal_record_requirements[2]`
- **Issue:** 0580 asks the prereg to carry the compare round's path and sha as a seal slot, and the prereg also says "the compare pins at seal: V007_PREREG_SHA256 (this text once sealed)". The compare carries `V007_PREREG_SHA256 = None`, "set at the seal (the seal record then pins this script)" (compare r10 L166). A prereg that names the sealed compare's sha and a compare that names the sealed prereg's sha cannot both hold. The same cycle would arise if the frozen addendum cited the sealed prereg's sha, since the prereg names the frozen addendum.
- **Draft:** the compare slot holds the final round's reviewed source (seal-time pins unset, `None`); the sealed compare is created after the sealed prereg and named only in the SEAL_RECORD; the frozen addendum cites no sealed-prereg sha.
- **Recommendation:** RECOMMENDATION ONLY: rule the acyclic order reviewed compare source -> sealed prereg (names that source) -> sealed compare (sets exactly V007_PREREG_SHA256, PIN_ADDENDUM_V005, PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK and PIN_PRODUCER_REGISTRY) -> SEAL_RECORD (names the sealed prereg and the sealed compare); have the seal check verify that the sealed compare differs from the reviewed source only in those lines; and have the frozen addendum cite no sealed-prereg sha.
- **Sources:** 0580 item 2; seal_record_requirements[2] (A67 seal-time pins); compare r10 L150-166; A81 RI-19; A81 RI-26

## RI-01: CONFLICT (input table) (RESOLVED)

- **Status:** RESOLVED: A58 RI-01 (r5) with the A72 branch: driver slot PENDING
- **Clause:** `binding_inputs.driver`
- **Issue:** 0526 lists driver v010 r4 b9ae92d5; A55.2-3 make the sealed driver v010 r5 ("the sealed driver is the one the gates ran on"), not yet on disk.
- **Draft:** binds r5 PENDING_FROM_BYTES with r4 b9ae92d5 and its build record as base.
- **Sources:** 0526; A55.2; A55.3; 0530

## RI-02: CONFLICT (BLOCKING for adoption) (RESOLVED)

- **Status:** RESOLVED: A57.1: production gas M_s = 128 for every DDO tail-corrected case; GQ at M_s 128 over the full DDO reach on all nodes and LO recomputed at M_s 128 required before the seal (integrated; certificates_v003 PENDING)
- **Clause:** `GQ / production_tail.gas / T3`
- **Issue:** A55.1 puts C4T-K256 (K_big 256) in T3. RA7 requires GQ at M_s vs 2M_s <= 1e-12 P0 over [K, K_big] for every roster used. certificates_v002 (TESTED): at the registered M_s 64, DDO_C4T [4,256] reaches 5.9e-10 P0; the bound first exceeds 1e-12 at k_perp = 227.6 /kpc; certified only for K_big <= 128 (GQ_CERT_V003_KB128 24984fd5). M_s 128 passes to [K,362] (GQ_CERT_V003_KB256_MS128 b3a5390f, not registered). Compare r5 implements S8 strictly (NEW-26): every T-case uv_tail equals C4T's outside {outer, lambda_scale, source_rule}, so under that implementation M_s cannot differ for C4T-K256 alone. As written, C4T-K256 reads NUMERICS_UNCERTIFIED.
- **Draft:** keeps M_s 64 and records the conflict; options for root: (a) M_s 128 for every tail-corrected case (then GQ_CERT_V003_KB256_MS128 applies, plus an LO rebuild at M_s 128: B1 insensitive <= 1.1e-7, certificates_v002 sec 2); (b) add gas.M_s to the S8 exception set for C4T-K256 only; (c) another K_big pair.
- **Sources:** A46 RA7; A55.1; A54 S8; certificates_v002 sec 4-5

## RI-03: UNDEFINED (RESOLVED)

- **Status:** RESOLVED: A58 RI-03 (rules; DOUBLING at 128/256 required)
- **Clause:** `production_tail.quadrature`
- **Issue:** R1's quadrature block (N_z_plus 12800, R/z eval and source extents) was set for K_big 32; no ruling restates it for K_big 128/256.
- **Draft:** defers node counts and extents to the registered P128 uv_tail configs (sha in each case block, S8).
- **Sources:** R1; A55.1; A54 S8

## RI-04: UNDEFINED (RESOLVED)

- **Status:** RESOLVED: A57.1: GQ over the full DDO reach (K_big up to 256/362) on all nodes; the draft takes the stricter edge sqrt2 * 2P = 362.04 (integrated)
- **Clause:** `GQ coverage edge`
- **Issue:** Compare r5 NEW-23: GQ DDO edge max(64, 2P) vs sqrt2*2P (A54 names only EPS and LO). DERIVED (not TESTED): for a cylinder outer region the gas factor P_i depends on k_perp <= K_big, so 2P = 256 covers C4T-K256, and the kept-cube corner zone reaches only sqrt2*K; certificates_v002 profiles GQ per k_perp.
- **Draft:** states the RA7/AMB-12 rule; edge for root.
- **Sources:** A46 RA7; A48 AMB-12; A54; compare r5 NEW-23

## RI-05: CONFLICT (wording) (RESOLVED)

- **Status:** RESOLVED: A58 RI-05
- **Clause:** `brackets; production_tail.P`
- **Issue:** RA4 enumerates C4T-K16 and C4T-K64 (retired R1 labels); A55.1 says "every tail-corrected case uses cylinder K_big = 128", which cannot hold for C4T-C5c (cube K_out 5), the T3 cases (64, 256) or S4T (sphere tail).
- **Draft:** RA4 list with C4T-K64/C4T-K256; K_big 128 for every case not otherwise specified.
- **Sources:** A46 RA4; A55.1; A46 RA2

## RI-06: UNDEFINED (RESOLVED)

- **Status:** RESOLVED: A58 RI-06 (partition)
- **Clause:** `LO shells above 64 /kpc`
- **Issue:** R1 registers LO shells to (32,64]; A54/A55 require coverage >= sqrt2*2P (362.04) with every extended shell <= 0.005 tau (compare r5 NEW-22), but no ruling names the partition. LO_CERT_V002 (fd4fa52b) has 10 shells to 363 (per-shell max 3.95e-4 tau at (128,256]).
- **Draft:** requires coverage and per-shell bound; partition for root (proposal: LO_CERT_V002's 10 shells).
- **Sources:** R1; A54; A55.4; compare r5 NEW-22

## RI-07: UNDEFINED (stale) (RESOLVED)

- **Status:** RESOLVED: A56 N4: "T3prime: production 2P with {P, 4P}; EPS/LO coverage >= sqrt2 * 4P" (integrated)
- **Clause:** `KBIG_NOT_CONVERGED next step`
- **Issue:** R1: "production K_big 64 under T3prime (32/64/128), EPS and LO to 128" is superseded by P = 128. Compare r5 NEW-24 derives "production K_big 2P under T3prime (P/2P/4P), EPS and LO to 4P" (= 256 under 128/256/512, EPS/LO to sqrt2*512); K_big 512 is outside every current certificate and the memory evidence (Codex1 0011 measured 256).
- **Draft:** "next step: RI-07".
- **Sources:** R1; A55; compare r5 NEW-24; FROM_CLAUDE3/0055 N4

## RI-08: PENDING INPUT (RESOLVED)

- **Status:** RESOLVED: A57.2: PICARD member successor specs per A53 with B0 evidence (gates_v004) (integrated; specs PENDING)
- **Clause:** `run_list.contingent`
- **Issue:** Compare r5 NEW-20 (real bytes): the registered A52.3 PICARD member specs (C5H 08d350ad: admit {}, column_workers 8, ro1_workers true; D5 template 84621760) predate A53 and read invalid; their B0 EXT entries lack projection_sha256 and declared_differences.
- **Draft:** requires re-registration to the A53 shape before the seal.
- **Sources:** A52.3; A53; compare r5 NEW-20

## RI-09: STALE (RESOLVED)

- **Status:** RESOLVED: A58 RI-09 (restated UNTESTED)
- **Clause:** `run_list.cpu_hours_estimate`
- **Issue:** R1 estimate is for K_big 32.
- **Draft:** labelled STALE; root may supply.
- **Sources:** R1; A55

## RI-10: PENDING RULINGS (RESOLVED)

- **Status:** RESOLVED: A58 RI-10 (adoption rule; IMPL list quoted in the seal record)
- **Clause:** `compare-lane NEW items`
- **Issue:** Compare r5 NEW-21 (S5 reading details), NEW-22 (coverage edges), NEW-25 (B4/NEW-17 scope), NEW-26 (S8 strictness), NEW-27 (label re-emission), NEW-28 (B0 record field), NEW-29 (carried notes) are lane proposals, not root text. Where a proposal is stricter and fills a gap it should become text before the seal.
- **Draft:** not integrated (only root rulings are integrated).
- **Sources:** compare r5 COMPARE_V007_IMPL_R5.md

## RI-11: CONFLICT (wording) (RESOLVED)

- **Status:** RESOLVED: A58 RI-11
- **Clause:** `B1 (Z2)`
- **Issue:** R1 says "serial route A"; the registered Z2 spec 2d5e79d0 sets route_a.column_workers 8 and compares against the PARALLEL_N8 deciding run.
- **Draft:** route A as registered in the spec.
- **Sources:** R1; A47 I4; spec 2d5e79d0 bytes

## RI-12: UNDEFINED (RESOLVED)

- **Status:** RESOLVED: A58 RI-12 and A59 (replace mode)
- **Clause:** `B1 (Z2) token map`
- **Issue:** The pre-seal Z2 ruling derives the token map "from the driver v010 r4 pin tables only"; A55.3 reruns Z2 on r5.
- **Draft:** derives the map from the sealed driver's (r5) pin tables; root confirm.
- **Sources:** A54 pre-seal status; A55.3

## RI-13: NOTE (base choice) (RESOLVED)

- **Status:** RESOLVED: A58 (Claude2 R2/R3 superseded)
- **Clause:** `status`
- **Issue:** Claude2's R2 (a0f855db) and R3 (92092f24) drafts integrate A40-A48; 0526 names R1 as the base, so this draft starts from R1 and integrates A46-A55 independently. R3 was not used as text.
- **Draft:** R3 cited for comparison only.
- **Sources:** 0526

## RI-14: SHOULD_FIX for root (TESTED by Claude3) (RESOLVED)

- **Status:** RESOLVED: A56 N1: alternating bound |d_last,i| q_i/(1 + q_i) and any per-row q_i >= 1 makes E unavailable (integrated)
- **Clause:** `pairing_and_decidability_rule.noise_allowance`
- **Issue:** A54 S7 sets the per-row bound to 0 for sign-changing rows. Claude3 0055 N1 built a world inside V2 on the tau = 0.05 row (alternating per-row ratio 0.95 under q = 0.083) that reads E/tau 0.023, decidable, and ADOPT_TAIL, while the row's own alternating tail is 0.12 tau; the same-sign history goes to R-PAIR. Proposal there: P_i = |d_last,i| q_i/(1 + q_i) for sign-changing rows.
- **Draft:** transcribes A54 S7 as ruled; the stricter alternative is for root.
- **Sources:** A54 S7; FROM_CLAUDE3/0055 N1

## RI-15: SHOULD_FIX for root (RESOLVED)

- **Status:** RESOLVED: A56 N2: RB_FP reads E from C4T's Picard R-PAIR member; C4T-A the same; both resolvable (integrated)
- **Clause:** `gates_before_any_T_result.RB_FP`
- **Issue:** Claude3 0055 N2: RB_FP has no R-PAIR path; NEW-7 or a B4 gap on C4T leaves the reading INCOMPLETE even after all three C4T R-PAIRs pass (6 runs that cannot resolve it). Root rules either a C4T rerun or RB_FP reading E from the C4T Picard member.
- **Draft:** RB_FP with unavailable E reads INCOMPLETE (A50 item 9 by analogy, fail-closed); next step for root.
- **Sources:** A48 AMB-09; A50 item 9; FROM_CLAUDE3/0055 N2

## RI-16: CONFLICT (labels) (RESOLVED)

- **Status:** RESOLVED: A56 follow-up 2: producers emit C4T-KLO (K_big 64) and C4T-KHI (K_big 256) (integrated)
- **Clause:** `tests.T3; run_list`
- **Issue:** A55 names the T3 cases C4T-K64 and C4T-K256; compare r5 registers the generic labels C4T-KLO/C4T-KHI (case-block schema C2V003) and refuses retired labels (Claude3 0055 A55 follow-up 2).
- **Draft:** uses A55's names; root names the labels producers emit (e.g. KLO = C4T-K64, KHI = C4T-K256).
- **Sources:** A54 (generic T3); A55.1; FROM_CLAUDE3/0055

## RI-17: CONFLICT (coverage edge) (RESOLVED)

- **Status:** RESOLVED: A58 RI-17, then superseded by A64.2 (NGC [2, 91])
- **Clause:** `gates_before_any_T_result.EPS (NGC)`
- **Issue:** R1 states NGC EPS coverage [2, 32]; the NGC N3 case uses cylinder K_big 32, whose node |k| reaches sqrt2 * 32 = 45.25, and the module's unit shells end at ceil(sqrt2 * K_big) = 46 (certificates_v002 coverage note; its EPS record covers NGC [2, 46]).
- **Draft:** NGC [2, 46].
- **Sources:** R1; A52.5; certificates_v002

## RI-18: LENIENCY (DERIVED, for root) (RESOLVED)

- **Status:** RESOLVED: A58 RI-18 (cap removed)
- **Clause:** `pairing_and_decidability_rule.noise_allowance`
- **Issue:** The q cap 0.9 (A51 norm level; S7 same-sign rows) understates a geometric tail for 0.9 < q < 1: the factor q/(1-q) is held at 9 while the series it bounds has factor up to 99 at q = 0.99. NEW-7 and A56 N1 make q >= 1 unavailable but leave the band 0.9 <= q < 1 capped, which is easier on adoption than the uncapped bound. Stricter readings: no cap below 1 (use q/(1-q)), or E unavailable for q >= 0.9.
- **Draft:** transcribes A51/S7 with the cap; stricter reading for root.
- **Sources:** A51 F2; A54 S7; A53 NEW-7; A56 N1

## RI-19: CONFLICT (log vs dispatch) (RESOLVED)

- **Status:** RESOLVED: A81 RI-19: 0561 is the order of record; A81 is the erratum to A72 H-01 (integrated in seal_record_requirements[4])
- **Clause:** `seal_record_requirements[publication order]`
- **Issue:** A72 records H-01 as "its sha goes in the seal record". Dispatch 0561 (15:55Z) adopted the acyclic form instead (SEAL_RECORD, then the config pinning it, then a separate receipt naming both), and FORMAT_V004 / RUNBOOK_V005 implement 0561. No A-entry logs 0561.
- **Draft:** follows 0561 / FORMAT_V004 / RUNBOOK_V005.
- **Recommendation:** RECOMMENDATION ONLY: log 0561 as the A-entry of record (an erratum to A72 H-01), so the frozen addendum states the order the seal uses.
- **Sources:** A72 (H-01); 0561; FORMAT_V004

## RI-20: PENDING INPUT (RESOLVED)

- **Status:** RESOLVED: A81 RI-20: adopted: RI-10's rule for every NEW item; V007 seals on the round whose three recheck lenses and distinct reviews report 0 blocking
- **Clause:** `seal_slots.compare`
- **Issue:** A79/A80: r10 is frozen and superseded for the seal; r11 (or r12) is the final round. RI-10's rule covers NEW-21 to NEW-29 by name; later NEW items (31, 45, 47, 61, 64, 67) were ruled one by one.
- **Draft:** compare slot PENDING with the round named by A80.
- **Recommendation:** RECOMMENDATION ONLY: apply RI-10's adoption rule to every NEW item the final IMPL declares, have that IMPL list each with its disposition and its MUST_FAIL tests (A75), and quote the list in the seal record; seal on the round whose three recheck lenses and the distinct reviews of record (Claude3, Codex2) report 0 blocking.
- **Sources:** A58 RI-10; A75; A79; A80; 0582

## RI-21: PENDING INPUT (RESOLVED)

- **Status:** RESOLVED: A81 RI-21: adopted: the c2v007-lineage round with 0 blocking; records of record only on the driver slot's identity runs
- **Clause:** `seal_slots.identity_comparator, seal_slots.identity_gate_records`
- **Issue:** c2v004-c2v006 are superseded (A68, A70, A76); c2v007 carries B-ID, SF-ARGV, SF-NN and the A73/A74 items; its records directory is empty at assembly. The r4 records (A76) are not seal records (A67 N1).
- **Draft:** slots PENDING.
- **Recommendation:** RECOMMENDATION ONLY: slot the c2v007-lineage round whose own check and Codex2's review report 0 blocking, and take as records of record only its outputs on the driver slot's identity runs, with the A59 replace-mode tokens and the raw successor-custody check.
- **Sources:** A67 N1; A68; A70; A74; A76

## RI-22: UNDEFINED (format) (RESOLVED)

- **Status:** RESOLVED: A81 RI-22: one merged DOUBLING record; NGC half <= theta/20, declared in A81
- **Clause:** `gates.DOUBLING`
- **Issue:** A73 leaves the merged DOUBLING record format pending (FIELDS_R7/R8 shape with both halves).
- **Draft:** requires one merged record with the A73 fields, registered before the seal.
- **Recommendation:** RECOMMENDATION ONLY: one merged record: DDO half (K_big {128, 256}, gas M_s 128, max change over tau per static row of saved C4R3 le3, <= tau/20) and NGC half (operator e6453d52, K_big 32, NQ max change over theta, <= theta/20); both halves must pass; the compare reads it as one gate; its sha is registered before the seal.
- **Sources:** A58 RI-03; A73; A79 NEW-61

## RI-23: CONDITIONAL RULING NEEDED (RESOLVED)

- **Status:** RESOLVED: A81 RI-23: adopted (conditional M_s 128 for NGC); LO_NGC in V007 is reported only; coverage to 91 gates the NGC N-test compare, not the V007 seal
- **Clause:** `fixed_across_all_cases.production_tail.gas (NGC)`
- **Issue:** A64.2: if GQ_NGC at M_s 96 does not hold to 91 /kpc, root rules on M_s 128. No GQ_NGC record to 91 is registered at assembly, and LO_NGC to 91 is absent (Codex1 0049).
- **Draft:** names both branches.
- **Recommendation:** RECOMMENDATION ONLY: if GQ_NGC at M_s 96 fails anywhere on [2, 91], set NGC gas M_s 128 (as A57 did for DDO) and recompute LO_NGC and DOUBLING's NGC half at that M_s; read no NGC N-test until LO_NGC, EPS_NGC and GQ_NGC to 91 are all slotted.
- **Sources:** A64.2; A57; Codex1 0049

## RI-24: UNDEFINED (r6 branch details) (RESOLVED)

- **Status:** RESOLVED: A81 RI-24: fresh, empty, root-created cache directory named in the SEAL_RECORD; no pre-warming; mode and directory recorded per T-run; T-run driver sha = driver slot
- **Clause:** `fixed_across_all_cases.production_tail.tail_table_cache`
- **Issue:** A72.3 says the T-cases run "with the cache" if r6 is adopted, but no rule says where the cache lives, whether it may be pre-warmed before launch, or how a T-run proves it used it. Codex1 waits for the r6 BUILD and cache policy.
- **Draft:** states A72 as ruled; equal footing; no mixed drivers.
- **Recommendation:** RECOMMENDATION ONLY: the r6 BUILD names the cache directory policy; the seal record names it; every T-run records its cache mode and the compare refuses a T-run whose mode differs from the registered one; no T-run starts before the seal names the driver, and every T-run's driver_sha256 equals the driver slot (extending A67 N1 to T-runs).
- **Sources:** A72; A67 N1; Codex1 0047

## RI-25: GAP (binding) (RESOLVED)

- **Status:** RESOLVED: A81 RI-25: the SEAL_RECORD names the bound plan and command shas; binder after the freeze and driver choice, before the SEAL_RECORD; template check optional
- **Clause:** `seal_slots.launch_packet`
- **Issue:** Launcher v007 checks the plan's internal pins against bytes and binds the plan's driver and frozen-addendum pins to the seal (C4-S1). Nothing in code compares the bound plan with the template it came from (its template_pin is recorded, not checked) or with a sealed sha, so which specs and caps are launched is bound to the seal only by procedure.
- **Draft:** launch-packet slot names the bound plan and command as PENDING parts.
- **Recommendation:** RECOMMENDATION ONLY: name the bound plan and command shas in the SEAL_RECORD (or the receipt) and have root verify them from bytes immediately before running the command; optionally, have validate() require that the bound plan equals its pinned template outside the three binding fields.
- **Sources:** A78; 0576; Claude4 0079

## RI-26: PROCEDURE (RESOLVED)

- **Status:** RESOLVED: A81 RI-26: adopted: freeze after the last pre-seal entry; seal check verifies cited entries; later entries need a revision or a no-change note
- **Clause:** `decision_pins_pending_at_seal`
- **Issue:** This text cites A47-A80 by name; the frozen copy is made at seal assembly (0576), possibly after further entries, and the open addendum changed twice while r3 was assembled (reads 03120f0a, 4b937ec1).
- **Draft:** cites by name; frozen copy PENDING.
- **Recommendation:** RECOMMENDATION ONLY: freeze after the last pre-seal entry, and have the seal check verify that every entry this text cites is present in the frozen bytes; any entry after A80 that touches this text needs an r4 or an explicit no-change note.
- **Sources:** 0576; A47-A80
