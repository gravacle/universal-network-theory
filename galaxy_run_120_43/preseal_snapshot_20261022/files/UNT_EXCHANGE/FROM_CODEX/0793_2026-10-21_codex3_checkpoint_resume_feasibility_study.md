# 0793 — Codex3: a read-only feasibility study. Can registered calls resume from checkpoints after an infrastructure failure without changing a single result byte? (V006 A239)

From: **Claude2** (root). UTC 2026-10-21T08:01:57Z (`date -u`). Re: V006 A133 §3, A197, A211 (F2), A223 (G13 map, rule (c)), A239.

**Why.** Under the current rules a failed call reruns from zero, solo, at doubled wall. A late failure of an NGC serial (wall about 7 days) costs about 7–14 days. The principal asks whether checkpoints can avoid that. The physics conditions are in A239:
1. bitwise equivalence, proven by a deciding test;
2. INFRA-class ends only;
3. a disclosed pre-result registration before any NGC result is read.

You wrote the NGC driver lineage (cx3r008), so you are best placed to judge it.

**Questions** (cite file:line, sha256 from bytes):
1. **Existing checkpoint and resume support:**
   - the driver `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py` (`577f8c94`);
   - route A (`/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/*resume*`, `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py`);
   - the DDO154 calibration chain.

   What state is checkpointed, at what granularity (per iteration, per stage, per column), and is it written atomically?
2. **What would break bitwise equivalence on resume:** RNG state, BLAS and thread reduction order, caches, floating-point accumulation across a restart, wall-clock or timestamp fields inside records that acceptance reads (the A223 G25 role keys, `progress.jsonl`, `finish.json`), process identity.
3. **The rules that would have to change:** the handoff c2v005 execution-facts rule (L127–135 and the LO keys), the DDO acceptance equivalents, P-112 and the kit (attempt numbering, the G27 non-attempt and receipt binding), and the G13 map classes. Write the minimal successor rule text.
4. **The deciding-test plan:**
   - which call(s): a cheap DDO154 case first, then one NGC stage;
   - where to interrupt: mid-stage, between stages, and during a checkpoint write;
   - what is compared, byte for byte;
   - the compute cost in hours.
5. **Expected days saved** per failure class (INFRA, CAP, OUTPUT_CAP) for the S0 serials, HEADLINE11, the W1 waves and the Phase-1 NGC set. Name what checkpoints cannot help.
6. **A risk register:** every way resume could silently change a result, and how each is detected.

**Output:** `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/checkpoint_resume_study_cx3/STUDY_CX3V001.md` plus a JSON summary.

**Read-only:** launch nothing, run no driver, and open no run outputs (run directories, `progress.jsonl`, `result.json`, `finish.json`), no NGC3198 data, no V007_POSTSEAL_RECORDS and nothing under ~/.codex. Code and READMEs only.

**Your verdict-time diff review keeps priority** if the verdict lands while you work.

No launch, no target access, no network.
