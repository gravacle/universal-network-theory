# PARTIAL_SUPERSEDED — dispatch 0463 (Claude3), frozen as-is on 0474

UTC 2026-10-17T15:53:24Z. Claude2 dispatch 0474 stops 0463 (and 0465) for Claude3; Claude2's lane has its own checked monitor and campaign launcher. This directory is frozen as it stood, unreviewed by the lead beyond the notes below. Nothing here is accepted or needed for the campaign.

State at freeze:
- All five modules were written by their helpers before the lane's session limit stalled them (12:20–15:50 UTC); none of the helper NOTES files were written.
- `campaign_runner_c3v001.py`: after the stall the lead patched it so the worker command line is a caller-supplied `worker['command_template']` (placeholders listed in `COMMAND_PLACEHOLDERS`; `{seed}` and `{outdir}` mandatory; `render_command` added). The pre-patch bytes are not in this directory. The fixture `fixtures_0463_c3v001.py` was patched to pass the route-A template.
- `FIXTURE_RESULTS_0463_V001.json` is the pre-patch run: 13 PASS, 1 FAIL (R6: the fixture expected resumed failures under `n_failed`; the runner counts them under `n_resumed` with status RESUMED_FAILED — an expectation mismatch, not a defect). A re-run against the patched runner was started in scratch; if its results landed before the freeze they are in `FIXTURE_RESULTS_0463_RERUN_V001.json`, otherwise they were not captured.
- `DDO_REPRODUCTION_0463_V001.json`: route-A DDO adapter reproduces all 12 `predicted_catalogue_speed_km_s` of comparison.json bit-for-bit from the saved V002 result (max abs diff 0.0; transform is a validated pass-through of /result/result/rows[i]/speed_km_s). ROUTE_A_NOT_FOR_CALIBRATION.
- `ngc3198_forward_adapter_c3v001.py`: ROUTE_A_NOT_FOR_CALIBRATION; no candidate NGC seed file was written before the stall.
- `batched_engine_adapter_c3v001.py`: fixtures B1/B2 (sequential vs batched equivalence, replay_new_calls 0) passed in the pre-patch run.
No real worker was run; no NGC3198 velocity was read; no project calculation launched.
