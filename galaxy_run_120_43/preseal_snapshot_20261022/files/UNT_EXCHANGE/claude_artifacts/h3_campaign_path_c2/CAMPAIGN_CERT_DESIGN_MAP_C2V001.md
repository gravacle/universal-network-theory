# Campaign per-point certification: design map C2V001 (V006 A191, commission 2)

Claude2 for root. Stamp (`date -u` before writing): Tue Oct 20 02:18:50 UTC 2026 (Mon 21:18 CDT). It proposes; root rules.
Read-only. Nothing was launched, and no run tree, step-2 tree or NGC3198 file was opened. From V006 (`b1c63b6f`) only A122, A133, A134, A139, A143, A145, A146, A147, A158, A188 and A191 were read, by line range. Every other source was reached through a path+sha citation and was sha-checked from bytes (section 8). Labels: TESTED (read or ran here), FORMAL (from code or records), UNTESTED (forecast).

**Short names.**
- W = q5b1 wrapper `7a6af535`.
- C = core. Lines are cited from placeholder r12_c4 `192d0863`, which equals r10_c4 `dc895f8a` except at L200 (README L34).
- P = parent v005 `c75a889f`. H = acceptance handoff v004 `5ff464cc`. G = b1 guard `9e3fc109`.
- CP-1: R = runner `3f5e5c18`, K = common `53f10e6e`, AS = registry assembler `cb5c61ee`, S = CP-1 root run sheet `75481f2b`.
- B = S4-R-C1 design brief `699d8ea8`. F = ROOT_ITEMS_FINAL_C4V004 `97a762e1`. RM = H3 README `6d2b4ee2`. W1S = W1 run sheet `6ab42522`. ACC = `h3_accept_call_c2v001` `05651663`.

## 0. Bottom line

1. **Per-point certification of engine-chosen points was designed but never built (FORMAL).**
   - Claude4's R-C8 (F L263-269) found the conflict now called F5. It recommended an append-only, hash-chained registry ledger: the config and the cache id bind its genesis and policy, each new point gets its prelaunch bundle from the approved producers when its wave is planned, and the entry is verified at plan, cache put and cache reuse.
   - R-B3 was to carry it (F L174).
   - Root adopted only R-C8's bridge: 31 points, including the seed and the 3 Jacobian points (A122 L240; F L208, L268).
   - The r10_c4 and q5b1 wrappers still hash the whole `tail_readiness` into the cache id (W L51-55; B L26).
2. **What each planned point needs before planning:** one registry record whose bundle carries EPS, GQ and LO_RHO_SLOT proofs from approved producers (section 1). CP-1's stages and post-run steps produce exactly these. But runner c3v004 certifies only its fixed 31-row table.
3. **F5, recommended: build R-C8 into the wrapper source of the verdict regeneration.**
   - The wrapper bytes and the cache id change at the verdict anyway (RM L49-52), and the work dir does not exist yet. So W1 starts in a work dir whose cache id never has to change.
   - Pre-registration alone stops at wave 3 (march0).
   - Fallback: open a new work dir at march0 and rerun waves 1-2.
4. **Timing (UNTESTED).**
   - Phase 1 pays nothing. Its snapshot ends before the first march0 call (A133 L467), and waves 1-2 are CP-1 rows 28-31.
   - Phase 2 pays the per-wave certification in series: 49.5 h (22 rounds × 2.25 h, 111 points, waves 3-16 of the assumed ENGINE_SHAPED list). That moves A188's "about 9-10 Nov" (L2248) to about 11-12 Nov.
5. **F6.** A134 Q2/Q3/Q5 and A158 make the handoff's own three-valued `rows_are_model_output` the classification of record (H L86, L349-351). No ruling maps a reading to an engine class.
   - Proposal: freeze the map now (section 5).
   - Build a certified MODEL_INVALID path for the two NOT_MODEL_OUTPUT readings in the same regeneration (W L331 "later certified successor"; F R-C4 L231-237).
   - Every undecided reading halts for a root ruling.
6. **The deciding and capability runs are real forward calls, not CP-1 records.**
   - By design they are HEADLINE11 #0-#10, which run at CP-1 rows 1-9 (section 6).
   - W1 cannot pass its gates until those 11 calls are FINISHED and ACCEPTED.

## 1. What a planned point needs, who produces it, and when

| When | Record | Checked at | Produced by |
|---|---|---|---|
| Plan: make_plan builds each call, then prelaunch (P L3306-3309 → W L202-211) | Registry record at `digest(point_identity(spec))`: `{identity, bundle, eps_certificate, lo_certificate}`, with identity equal (B L35-45) | W L86-90. The mapper copies both slots into the spec (C L249-259) and hashes it (C L261-263) | AS `assemble_registry` (L274-330), which root pins as `tail_readiness.certificate_registry` |
| Plan | Prelaunch bundle: identity, custody, domain, `prelaunch {EPS, GQ, LO_RHO_SLOT}`, `driver_certificate_bindings` = the spec slots, acceptance rule | W L119, L140-147; G L84-102, L153-154 | AS `assemble_bundle` (L220-272) |
| Plan | EPS proof: TESTED PASS, point and custody shas, envelope, shells out to the edge, approved producer | W L148-159; G L104-117, L133-140 | R stage EPS (producer `a1dcdea8`, S L175), then `adapt-eps` with the per-point instance of the one EPS policy review (S L92-96; A134 Q8 L499) |
| Plan | GQ proof: geometry-uniform all-column bound, b/(1−z) ≤ 1e-12 | G L142-152 | R stage GQ (`2832ceb9`, S L174) |
| Plan | LO_RHO_SLOT proof plus the registered ρ record (RHO_G, registered, full search, coverage complete), which is the lo slot | W L160-172 | R stage RHO attempt a (S L176), then slot proof `cd10cd59` at root's post-run registration (S L98; A146 L862) |
| Every resume, cache put and cache open | The same record, unchanged | W L259-264, L290-293; P C4-2 resume L3405-3433 | none: this is why the registry must be append-only |
| After FINISHED | Per-state LO, GQ/GQ_SIGNED and SRB-ROT; POST_STATE_BUNDLE with `parent_prelaunch_bundle` = the registered bundle; per-state ρ equal to the slot ρ on 10 keys | W L95-118, L137-144, L173-191; G L155-221 | ACC (L160-176), then H `accept_call` (A158 L1288), then the entry's reingest (W L335-358) |

- **No per-point human review (FORMAL).**
  - There is one EPS policy review, instantiated per point by script, and no cap or LO reviews (A134 Q8 L499).
  - The approved producers are a fixed set: `eps_adapter`, `gq_producer`, `lo_slot_proof` (K L90; C1 adds the slot proof, A145 L857, A158 L1291).
  - So certifying a new point is compute plus scripted proofs. It needs no new review, producer or config field.
- **CP-1 per wave?** The producers and proofs are the same, but the c3v004 tools are not ready (FORMAL):
  - the runner and assembler take only the fixed `POINTS` table (K L92-127; R `load_spec` L241-257; AS L312-313 `complete_31_point_table`);
  - rows after the anchor need the anchor's context and AGREE in the same out-root (R L516-521, L821-825; S L129-134, L188).
  - A manifest-input successor is needed. It touches no approved producer, policy review or cache-key field.

## 2. Why the registry pin is in the frozen config and the cache key

- **(a) Cache id.**
  - W L52-55 hashes all of `tail_readiness` (registry pin included) together with the wrapper and guard bytes. The comment at L51 reads: "Certificate scope/producer/enumerator/registry changes make a new cache."
  - A work dir holds one cache id (P L59-63, L3094-3100, L3134-3147).
  - The config is frozen from W1 until the march0 plan (A137 N-C: W1S L255; RM L55).
- **(b) Spec bytes.** The mapper writes the registered slots into every spec (C L249-263), which ties the registry to three other gate inputs:
  - the 9 probe spec shas, which key the capability rows (C L319-333);
  - the seed spec sha (P L1788);
  - the adoption derivation, which binds both of those (P L1859-1862) and the registry pin itself (W L218-223; builder L116, L120).
  - R-C1: the slots "change the mapper bytes the capability evidence binds" (F L209).
- **(c) Design premise: the registry is fixed before the campaign.**
  - "Freeze the registry before HEADLINE11, and never edit it afterwards" (B L441); "never change its probe-point entries afterwards" (F L212).
  - R-C8 kept that premise for the genesis and moved growth out of the key. It was never built.
- **What actually has to stay bound:** only the genesis entries (the probe points and the seed, which feed (b)) and the policy.
  - Growth needs no binding in the key. Each cache entry binds its own bundle and handoff and is re-verified on open (W L259-272).
  - Each WAVE_PLAN binds the slot-carrying spec sha (P L3310-3312; resume check L3405-3433; reingest W L349).

## 3. F5: the options and the recommended path

**3.1 Pre-registration (in place; covers waves 1-2 only).**
- Row 28 is the W1 seed.
- Rows 29-31 are u = seed + 0.05 e_j. They are fixed before any result if the seed is VALID and each +side is taken at full step (B L276, L321; F L208).
- Wave 2 is 3 calls, because the probe plans one call per Jacobian branch (P L2529, L2600-2611; F L268 "waves 1-2 (4 calls)").
- From march0 on, every point depends on earlier results (F L264-265), so pre-registration cannot cover it.
- TESTED (synthetic): EA15 refuses, and with wave 2 pre-registered EB15/EB16 run (RM L56-57).
- **Deciding test for rows 29-31:** after W1's acceptance, the read-only probe lists the wave-2 keys. They must equal `39a36ac3…`, `2a17398b…` and `a1b7660c…` (K L124-126).

**3.2 Re-pinning the registry each wave: not viable.**
- Each new pin is a new cache id (W L52-55) and needs a new adoption derivation (W L219).
- C4-2 then forces a new work dir, and every earlier wave reruns (P L3094-3100).

**3.3 The R-C8 ledger (recommended). A minimal wrapper-only diff:**
- The core is untouched. The wrapper can re-patch `O.Mapper` the same way the core does (C L266).
- **Config:**
  - `tail_readiness.certificate_registry` stays the genesis, CP-1's 31-point registry;
  - a new field `certificate_ledger = {path, schema}` carries no head sha. So the cache id (L52-55), the policy gate (L59-77), the adoption binding (L219) and the gate digest never move as the ledger grows;
  - the policy review is not signed yet (RM L99). It binds the ledger rule beside the slot rule (L74).
- **One lookup:** `lookup(ident)` = genesis ∪ ledger. It is used by the mapper (C L249-259), `certificate_check` (W L86-90), `write_acceptance` (W L237-238) and the acceptance step (ACC L160-163).
- **Ledger rules:**
  - hash-chained and append-only;
  - a key already in the genesis or the ledger is refused, so the probe, seed and planned spec bytes stay stable;
  - an entry is accepted only if its bundle passes the same prelaunch check (W L119-194, with G `verify_bundle` in the prelaunch phase) against the config's approved producers.
- **Placement and locking.** The ledger lives in the work dir, as R-C8 says (the work dir can never move, RM L197). It is appended under the parent Lock while no run holds it. Every wave already halts for acceptance (RM L130, L143).
- **When: in the verdict regeneration, before W1.**
  - Its cost adds no custody event, because the B2 fix (A191 L2304-2305) already forces successors of the entry template, the generator (which pins the entry, L23-24, and the wrapper source WRAPQ, L22) and the regenerator (which pins the generator, L42).
  - The ledger adds one reviewed wrapper source to that set.
  - Review: Claude4 after Fri 19:00Z together with the H3 path (A191 L2319); Codex1 reviews the generator diff (A129).
- **Needed only by wave 3, so it can be built during waves 1-2:**
  - a manifest tool. It turns the next wave's probe misses into mapper-built specs with pending slots. Use W `wave` (L370-373, probe only): `plan` cannot list unregistered points (P L3836 → L3309);
  - CP-1 c3v005 with manifest input, either continuing on the same out-root as Phase B did (S L56-62) or pinning the c3v004 anchor records;
  - an append mode for the assembler.

**3.4 Fallback, if the ledger misses the verdict.**
- Run W1 and wave 2 on the current chain. Phase 1 needs nothing more.
- At the march0 plan, where the A137 N-C window ends (W1S L255), open a new work dir on the ledger chain.
- Waves 1-2 rerun there: the cache cannot carry over (C4-2), and the anchor alias is disabled (C L101-102).
- Cost: about 2 call walls on Phase 2's path (UNTESTED; provisional wall cap 37 h, A188 L2229).

**Per-wave procedure under 3.3 (root):**
1. Accept wave k's calls (RM L130-143).
2. Read the next wave's misses with the read-only probe.
3. Write the manifest, then run CP-1 c3v005 on the keys that are not yet registered.
4. Per point: `adapt-eps`, the slot proof and the bundle. Then run `verify --c1` (S L233).
5. Append to the ledger under the lock, and record the head sha in the wave record.
6. Relaunch without `--new-campaign` (RM L143).

## 4. Per-wave timing and the schedule effect (UNTESTED)

- **Basis:** CP-1 takes 2.25 h per point at background QoS, 8 in parallel (root's measurement).
- A wave's certification takes ⌈n_new/8⌉ × 2.25 h.
- It runs in series with the campaign: wave k+1's points exist only once wave k is cached (P L2568-2611).
- **Shape:** the ENGINE_SHAPED list (W1S L236, ASSUMED). Waves 1-2 are already covered by the genesis (rows 28-31).

| Wave | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| New points | 2 | 1 | 1 | 1 | 10 | 10 | 24 | 8 | 2 | 1 | 10 | 10 | 24 | 7 | 111 |
| CP-1 rounds (k = 8) | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 1 | 1 | 1 | 2 | 2 | 3 | 1 | 22 |
| CP-1 wall (h) | 2.25 | 2.25 | 2.25 | 2.25 | 4.5 | 4.5 | 6.75 | 2.25 | 2.25 | 2.25 | 4.5 | 4.5 | 6.75 | 2.25 | 49.5 |

- **Phase 1** (A133 L467; A188 L2244-2247): no F5 cost, provided a Jacobian +step is not invalid. An invalid +step adds one round (2.25 h) for its halving points before wave 3 (FORMAL).
- **Phase 2:** +49.5 h (about 2.1 days) in series, plus the operator steps of 14 cycles (not measured). A188's "about 9-10 Nov" (L2248) becomes about 11-12 Nov.
- **Lever:**
  - between waves the campaign is idle, so CP-1 can run at normal QoS with k up to 16 (per-worker peak 2 GiB, S L116);
  - at k = 16 there are 16 rounds, ≤ 36 h at 2.25 h per round. Normal QoS was about 2× faster per point for GQ+EPS (S L203);
  - measure it on wave 3, following A122's "first bundle is timed end to end" (L240).
- **Fallback 3.4** adds about 2 call walls.

## 5. F6: what A134 and A158 imply, and the minimal rule

**What the rulings imply:**
- A134 Q2/Q3 (L496): no value is used before acceptance.
- A134 Q5 (L498): the failure readings are frozen, with no tighter envelope and no scope change. The 0690 reading points are at L523-528.
- A158 (L1288): H is the enforcement point for the campaign. H fixes:
  - `outputs_are_evidence` only for ACCEPTED and ACCEPTED_PASS_FLAGGED;
  - `rows_are_model_output` False for NON_LAPSE_TAIL_MATERIAL and BOUND_INSUFFICIENT;
  - `rows_are_model_output` None for every other reading (H L86, L349-351).
- The anchor stop fires only at key `8ad6ca4e…` (H L46, L353-356). The campaign seed is `6944e210…` (K L123; F L346), so the stop never fires for a campaign call (FORMAL). It does fire for HEADLINE11 #0 (section 6).

**What the code does today:**
- A reading other than ACCEPTED exits 13 and caches nothing (ACC L174-187). The call stays INFRA.
- `invalid` is refused (W L326-331, L312).
- A retry reruns the same spec, so it gets the same reading. The next run halts HALTED_UNRESOLVED (P L3494-3500).
- Caching MODEL_INVALID also needs a certificate-OK acceptance (P L175; W L260, L296-303). So a certified invalid needs wrapper code (W L331). R-C4 says to decide this before wave 1 (F L231-237).

**Proposed rule (freeze it before any campaign reading exists):**

| Reading | Action |
|---|---|
| ACCEPTED, ACCEPTED_PASS_FLAGGED | Reingest VALID (built; binds the acceptance record under the B2 fix) |
| INCOMPLETE | Rerun the acceptance step once with root-checked deps. H writes a new attempt dir (L19-22, L90-91), and no forward call reruns. If it is still INCOMPLETE, it falls under the last row |
| NON_LAPSE_TAIL_MATERIAL, BOUND_INSUFFICIENT | Certified MODEL_INVALID through a reviewed `reingest-invalid`. It caches only with an H record of that reading for this call, receipt and registered bundle, bound by sha as in the B2 fix, with failure_class `TAIL_ACCEPTANCE_<reading>`. The value is never evidence; the engine treats that θ as it treats any invalid θ. Disclosed under A134 Q5 |
| LO_UNCERTIFIED_TRANSIENT, UNDECIDABLE_FLAGGED, INCOMPLETE that remains | No class. The campaign halts at that θ, as it does today, and root rules per call. No retry and no numerics change (Q5) |

- The certified-invalid code must be in the W1 wrapper, because the cache id binds the wrapper bytes (W L54). Build it with the ledger. Using it is root's act, call by call.
- **Deciding measurement:** HEADLINE11's 11 readings, then the first campaign readings. The corners include Q∞ = 161.2, the highest LO risk (B L323-326; a FORMAL ranking).

## 6. The deciding test and the 9 capability-probe runs

**They are not CP-1 records.** CP-1 makes GQ, EPS and ρ certificates (S L172-178). The gates need finished forward calls.
- **`deciding_test` (C L114-197)** needs:
  - exactly two runs, `reanchor` and `workers_8` (L129-132);
  - both fresh (`admit {}`, L144);
  - the numerics equal to the config block without the slots (L147);
  - `reanchor` at the registered A2F10 point and equal to the config anchor pins (L149-157);
  - results COMPLETED and valid (L158-162), with an exact driver replay (L163-166) and 8 workers (L176-178);
  - FINISHED/COMPLETED receipts checked by the pinned monitor (L179-182; P L721-733);
  - distinct results (L190-191).
- **`driver_capability` (C L313-340)** needs one row per probe spec sha (the trial point plus 8 corners, P L2041-2054). Each row must carry `run_mode_admitted` and a FINISHED/COMPLETED receipt for exactly that spec sha (C L325-333).
  - P's docstring calls this layer a "dry-run" (L2057), but the core override needs finished calls.
- **A146's "deciding test" (L865) is a different object:** CP-1's anchor ρ pair (S L58, L192).

**By design they are HEADLINE11.**
- CP-1 row 1 names TAIL_REANCHOR, WORKERS_8_CANDIDATE_ANCHOR and HEADLINE_TRIAL, which are HEADLINE11 #0-#2.
- Rows 2-9 are the corners, HEADLINE11 #3-#10 (K L96-104; B L287-295; F L209).

**TESTED here, from sha-checked spec bytes:**
- HEADLINE_CORNER_000 (`f3c72d95`) and HEADLINE_CORNER_111 (`36e0ffdb`) are campaign-mapper specs: their label is `DDO154 cx2v006 theta …; point …` (C L260), with the slots PENDING.
- CAMPAIGN_W1_SEED (`3958aed3`) is the W1 dry plan's seed spec (W1S L339).
- TAIL_REANCHOR (`5fc6f0bd`) is the template spec, with `admit {}`.
- HEADLINE_TRIAL's own spec was not read (UNTESTED).

**Deciding test for reusing HEADLINE11** (read-only, at RM V3/V4):
- Under the candidate config, `status` reports `driver_capability.normalization[].spec_sha256` (C L319, L337).
- If those equal the spec shas that HEADLINE11 #2-#10 ran with, HEADLINE11's receipts are the 9 capability rows, #0/#1 are the deciding rows, and no further run is needed.
- If not, 9 real calls at those exact bytes still have to run.

**Conditions on using them:**
- They need A134 Q2 acceptance before use in H3 (A134 L496; HEADLINE11 is among the 29 tail-ON direct calls, B L320; H L2-4).
- #0 is the anchor: an LO FAIL there is the step-4 stop (A134 L528), and that blocks W1's gates.

**Missing tool (lean):** a read-only assembler that writes the two evidence documents from HEADLINE11's receipts, results and finish files. The builder only checks those documents (RM L123).

**Schedule (the dependency is FORMAL; its size is UNTESTED):**
- `run` checks every gate before it writes anything (W1S L18). So W1 waits until HEADLINE11 #0-#10 are FINISHED and ACCEPTED and both documents are pinned.
- A134 expected H2 on Tue Oct 20 (L521). If HEADLINE11 is done by the verdict, A188's "W1 about Sat 24 Oct" (L2243) holds. Otherwise W1, u_A and Phase 1 move by HEADLINE11's remaining wall.

## 7. Proposed rulings (root rules)

1. **F5:** adopt R-C8 as in 3.3, inside the verdict regeneration. The genesis is CP-1's 31-point registry. If the ledger misses the verdict, use 3.4.
2. **Per-wave certification:**
   - commission CP-1 c3v005 (manifest input, the same producers and proofs, assembler append mode) and the manifest tool, by wave 3;
   - builder: Claude3; Codex1 gives a single pass (precedent: the A134 build table, L512).
3. **F6:** freeze the four-row map of section 5 now, and build the certified-invalid path together with the ledger.
4. **Deciding and capability evidence:** name HEADLINE11 #0-#10 as the source, subject to the equality test in section 6, and commission the evidence assembler as a root workflow.
5. **Wave records:** each wave record carries the ledger head sha, the CP-1 manifest sha and the per-point bundle shas.

## 8. Sources (sha256 from bytes, 02:1xZ)

| File | sha256 |
|---|---|
| CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md (sections listed only) | b1c63b6f9059fe370bb37ccbffd7762968ac9dd7340526911d649786b729a7ce |
| h3_campaign_path_c2/README_H3_CAMPAIGN_PATH_C2V001.md | 6d2b4ee2d6bb4dc71b0bd6aa62d046f9e0ac74443b2968f81df057fd04e8ca5e |
| CLAUDE2/W1_RUN_SHEET/W1_RUN_SHEET_V001.md | 6ab425228706602d79a61fab3446b4174c7a82d523a623fb6df2aeaefe4da2f4 |
| calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py | 7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d |
| h3_campaign_path_c2/placeholder_chain/v006r12_c4/calibration_core_cx2v006r12_c4.py | 192d086348fed9307da99732c0ef146bb336a3d605afc1e9e56b6ce959ad1a73 |
| calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py | c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d |
| s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py | 5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8 |
| s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py | 9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677 |
| h3_campaign_path_c2/h3_accept_call_c2v001.py | 05651663cfa2e9159068c9f7aa939a0cefc749b6acc79d4a677cf87f7c2af2ba |
| h3_campaign_path_c2/build_adoption_derivation_c2v001.py | 01a4cbae729a0c44df2ea1f4cc500ae95669cb9ff6a7541bc94621c23c2294bd |
| h3_campaign_path_c2/make_campaign_cascade_c2v001.py | 65a701449bd72d654ec3ad59b01e30d3c89c8025988c9d0ce435c25ca1fa5358 |
| h3_campaign_path_c2/regenerate_h3_c2v001.py | 1706da776372191f619d02937b4388025b113fcb023b7da83a4300e410e3cc8f |
| h3_campaign_path_c2/h3_campaign_entry_c2v001.py | 08068e93904fa12bd7d6bb9ceaca6b37b85cc884fa8091d8a7d59900e5a0c4bd |
| CLAUDE2/CP1_C3V004_ROOT/CP1_RUN_SHEET_ROOT_C3V004.md (cited A146 L889) | 75481f2bcf70cb903506711c36d7761b7fdb3a4f65026d1cad72efb773149bb0 |
| s4rc1_c3/build_c3v004/cp1_runner_c3v004.py | 3f5e5c188d4a6967afdb3bfab805d1cc8650e9c26793895096be55ca8f4f1a48 |
| s4rc1_c3/build_c3v004/s4rc1_common_c3v004.py | 53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083 |
| s4rc1_c3/build_c3v004/registry_assembler_c3v004.py | cb5c61ee3d515588394c694b115aca733426db670385eddf92ed389894d065b0 |
| s4rc1_c3/UNDERSTAND_S4RC1_SYNTH_C3V001.md (cited K L6) | 699d8ea8cb0bf8665eab02cb543ca275b45aeb7866813c0da50b63c14d87f4b0 |
| step4_launch_readiness_c4/launch_order/ROOT_ITEMS_FINAL_C4V004.md (cited B L525) | 97a762e1cf2c7eb76e7f77b4c708cfc5452dd5b72452b2bf86ffc9e369e6b704 |
| step4_launch_readiness_c4/dryplans/specs_v001/specs/{TAIL_REANCHOR, HEADLINE_CORNER_000, HEADLINE_CORNER_111, CAMPAIGN_W1_SEED}.json (pins K L96, L97, L104, L123; label, admit, slot and workers fields only) | 5fc6f0bd…, f3c72d95…, 36e0ffdb…, 3958aed3… (full shas equal K) |

Unless a path above is under CLAUDE2/, it is relative to `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/`.
