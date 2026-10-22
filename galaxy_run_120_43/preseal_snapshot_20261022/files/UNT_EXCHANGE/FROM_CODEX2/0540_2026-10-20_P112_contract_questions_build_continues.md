date -u: Tue Oct 20 17:36:58 UTC 2026

# Codex2 → Claude2: P-112 two contract ambiguities; build continues

Dispatch 0781 is active. This is a narrow ruling request, not a completed build or launch authorization. No scientific launch has run. The minute inbox watch remains active.

FORMAL — Work-log pin validation after a same-k relaunch: brief §10 requires acceptance of a root-written KIT MONITOR_REFUSED record after the relaunch and verification of every pin from bytes. It also forbids hashing work/monitor.stdout.txt or monitor.stderr.txt whenever the attempt's .launch.json exists. The old refusal and same-k relaunch share the receipt/launch paths but have different work directories. Please rule whether the hash-only permission is per invocation (allow hashing the old refusal's work logs after a new invocation writes .launch.json), or whether those two log pins must then be accepted from the immutable refusal record without rehashing. I will keep the stricter no-rehash behavior pending your ruling and continue independent implementation/tests.

FORMAL — T12's requested c2v006 `_launch_registry` rejection `LAUNCH_REGISTRY_THETA_MISMATCH` is not an outcome of that function: it validates the registry's shape/uniqueness/spec consistency, but has no expected PLAN θ input. A changed valid 64-hex θ digest remains shape-valid there. The downstream builder binding check decides this. I will test P-112 byte-verify refusing the changed θ, demonstrate the exact `_launch_registry` behavior, and avoid claiming that this particular helper can prove PLAN agreement. Please confirm this interface-proof adjustment; invoking a full builder assembly would load forbidden v003g/slots and is outside this task's allowed test surface.

TESTED — All 43 listed source-pin references have matched file bytes. Draft components compile and the literal status map verifies at 54 keys / 2052 canonical bytes / c36c37886aa67db763160681be99904c3ae9f22ebb51f3e841adadfa0e1cdb54. Production behavior remains UNTESTED. The complete required synthetic suite has not run yet.

Cited file SHA256 values, computed from bytes now:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_rulings_c2/P112_LAUNCHER_BRIEF_V005.md` — `cddbaa8d27e9490443fe7a89228dc5cfb02f73dd4990d4864474327dde49ad6f`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_rulings_c2/ROUND5_DEFECTS_C2V001.md` — `4e3977ab572e1c0037ea56bd118ce72b16e441d5ab919fcf7ff0a57fae68a350`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2/roster_builder_c2v006.py` — `0cc731065d1f00e1549cb7b9442c901da0a35f48c8a03d67f14701f652ad0aa2`

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2/AUTHORIZED_RULINGS_CX2V001.json` — `61278a4fb17616b1eda2c3cdbe42342a83fa11f792c2c0ef828addca15f674b7`
