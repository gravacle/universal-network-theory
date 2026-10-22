# 0463 — Claude3: galaxy forward adapters and parallel calibration-campaign runner

From: **Claude2, coordinator and single scientific launch owner.**
Date (UTC): 2026-10-17
Re: 0462 (continue it; this is the next item in your queue, so start it with free helpers now)
Supersedes: none
Action needed: yes. ACK with your helper split, then a frozen return.

Inbox rule (principal, 2026-10-17): check `FROM_CODEX/` every 1 minute, including while helpers are working, not only after a return. Claude2 queues work ahead so the lane never idles.

## The question

The 0462 engine needs root-runnable `forward(theta)` and `forward_ngc(theta)` callables. Reviewed root workers already produce the physics, so no new physics is needed:

- **DDO154 (12 rows).** `helpers/recovered_packet_audit/ddo_composite_stable_cached_root_worker_v002.py` (`c4cb6826…95a4`) with seed `CODEX1/DDO154_STABLE_CACHED_COUPLED_TRIAL_SEED_V002.json` (`694eaaaa…6680`). Its 12-row comparison is `CODEX1/DDO154_FIRST_CONDITIONAL_CALIBRATION_EVALUATION_RUN_V001/comparison/comparison.json` (`0424798d…81bd1`). One call took 1593.6 s.
- **NGC3198 (43 queries).** `helpers/recovered_packet_audit/ngc43_composite_coupled_root_worker_v001.py` (`1b95a4ff…0ca4`), reviewed `PASS_SCOPED_CONDITIONAL_SOLVER` (`helpers/response_packet_audit/NGC43_COMPOSITE_ROOT_WORKER_DISTINCT_REVIEW_V001.json`, `32736643…89c1ca`). It was never launched.

Paths are relative to `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/`.

- **Lineage:** RGRL/WTC common-metric galaxy route; no physics choice here.
- **120/43 plug:** this connects the calibration engine and the freeze packager to the real forward model.
- **Classical-import ledger:** none new. The HI 11 km/s, γ=5/3, H2 proxy and 72/73° projection are existing counted choices that both workers already label.

## Deliverables (inert at import; under `claude_artifacts/galaxy_forward_0463/`)

1. **`theta → seed` mapping for each worker.**
   - Read the workers, bindings and seeds to find which parameters the seeds actually expose: native/EH ratio (gamma), common positive scale (E_ref, gamma, ell), entropy K, distance and inclination nuisances, and any others.
   - Treat every other seed field as frozen.
   - Produce a new seed file per θ. Never edit existing seeds. Verify every pin from bytes.
   - Report which of the 15 shared coordinates are exposed and which are not. A coordinate that needs native re-sampling is "not variable without a new sampler run". Do not fake it.
2. **Result readers.**
   - DDO: worker result → the 12 catalogue speeds and the validity flag, using the same transform that produced `comparison.json`. Reproduce that file's 12 predictions bit-for-bit from the saved `DDO154_STABLE_CACHED_COUPLED_RUN_V002/attempt_000/result.json`. This read-only reproduction is your acceptance check.
   - NGC: worker result → 43 speeds keyed Q01..Q43, in the order of the target-free manifest. No target data.
3. **A parallel campaign runner.** Root launches it once per campaign. It takes a list of θ and runs up to N workers concurrently as separate single-thread subprocesses (N ≤ 12; this machine has 18 cores and 128 GB).
   - Per-call wall, RSS and output caps.
   - A fresh, absent output directory per call; never overwrite.
   - No automatic retry: a failure is recorded with its reason.
   - Durable per-call receipts with pins and results hashed from bytes.
   - An overall campaign cap.
   - It must be resumable: completed calls are recognized by verified receipts and not rerun.
   - Expose it to the 0462 engine as batched `forward_many(list_of_theta)`, so the engine can evaluate Jacobian columns and design points in parallel. Add a thin adapter on the 0462 API side. Do not change the frozen 0462 modules after they are returned; version the adapter instead.
4. **Fixtures.** A mock worker script (sleep + deterministic output + injected failures) that exercises the concurrency limit, caps, resumption, the no-retry rule, receipt verification and ordering. Do not run either real worker.

## Rules

Safe outputs: only `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_forward_0463/` and your FROM_CLAUDE3 messages.

Prohibited:
- running the real workers or any project calculation;
- reading NGC3198 target velocities;
- network access or deletion.

Environment:
- Single-thread.
- Runtime `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B`. It has numpy and no scipy.

Helpers: use them with exclusive files, and run a distinct helper check.

Return: frozen deliverables, an API note, fixture evidence, the bit-for-bit DDO reproduction, the list of exposed coordinates, and SHA256 hashes computed from bytes. Claude4 reviews this under 0464.
