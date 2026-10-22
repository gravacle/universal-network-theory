# D034 diagnostic selector: exact command form

Documentation addendum for review B5-1 (Claude3 0376). This adds no adoption or launch authority. The reviewed entry bytes remain unchanged.

`select-workers` must be the first argument after the script path. The following is a command template; root supplies the actual absolute config path, its byte SHA-256, and a new diagnostic filename with an existing parent:

```sh
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cw8_hardening_cx1/select_workers_diagnostic_cx1v001.py select-workers --config /ABSOLUTE/CONFIG.json --config-sha256 CONFIG_BYTE_SHA256 --refusal-record /ABSOLUTE/EXISTING_PARENT/NEW_LOCK_REFUSAL.json
```

If root supplies a forecast, append both `--forecast /ABSOLUTE/FORECAST.json` and `--forecast-sha256 FORECAST_BYTE_SHA256`. These are the unchanged launcher's paired options. This entry has no launch command.

The diagnostic is written only for `CW8_CHOICE_LOCK_ROOT`, `CW8_CHOICE_LOCK_FILE`, or `CW8_CHOICE_LOCK_IDENTITY`. Successful selection writes no diagnostic. A diagnostic never supplies a serial or cw8 choice. No filename is reused, no parent is created, and `worker_choices` is forbidden in the diagnostic path. For a missing launch root, use an existing directory outside that root. Root must preserve the refusal and resolve its cause; diagnostic existence does not authorize a retry or launch.

Normal lock-refusal publication preserves rc 2 and the original CLI JSON. As review B5-2/B5-3 records, a tool-pin failure before CLI entry fails closed with a traceback; a publication race or I/O failure can instead report its own failure. The entry is intended for a one-shot process (B5-4). B5-5 independent end-to-end evidence remains in `verify_c3_backlog5`; B5-6 is a harmless dead expression in the test only. Those notes do not change the review PASS.
