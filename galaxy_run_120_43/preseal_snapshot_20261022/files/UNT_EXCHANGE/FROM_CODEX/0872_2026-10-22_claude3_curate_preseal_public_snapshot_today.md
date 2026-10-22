# 0872 — Claude3, **priority now** (ahead of 0871 item 2): curate a pre-NGC public snapshot for GitHub. Root pushes it today, after its 13:00 CDT reset and before the S0 launch, **only with the principal's explicit OK** (V006 A311)

From: **Claude2** (root). UTC 2026-10-22T14:48:08Z (`date -u`). The principal suggested a git update today, before any NGC3198 run. The target repo `gravacle/universal-network-theory` is **PUBLIC**. Its last push was 2026-10-08.

**Build a staging folder** `/Users/bgm/Research/UNT_PUBLIC_SNAPSHOT_20261022/` (a new folder) by **copying**. Do not move anything.

**Include:**
- the sealed and candidate preregistration texts (r3a and their siblings);
- the V005 and V006 decision registers;
- PLAN and STEPS;
- every adopted tool's source (`.py`/`.sh`) and its README;
- reviews and verify RESULT files;
- the certification **records** (CP-1 EPS, GQ and ρ JSONs; the registry; C1);
- DBP params, the verdict-day runbook and sheets;
- dispatches FROM_CODEX and the lane outboxes.

**Exclude:**
- run trees and outputs (UNT_INTERNAL_RUNS, External1 paths, any `out/`, receipts' result payloads);
- every NGC3198 observational, target, sigma or slot file;
- step-2 stage outputs;
- `~/.codex`;
- any file over 20 MB;
- caches, inert fixture runs and test scratch.

**Scan everything you include** for:
- credentials, tokens and keys;
- email addresses: **remove or redact personal emails**, and list every hit for root;
- absolute home paths (allowed, but list them);
- anything NGC3198-data-like.

**Produce:**
- a manifest with every file, its size and sha256;
- the total size;
- `SNAPSHOT_README.md`, which explains the blinding state: no NGC3198 value has been read, S4T is pending, the seal is pending;
- a top-level hash of the manifest.

Post `READY` with the size and the scan results. **Do not run any git command and do not push.** Root does that after the principal's OK.
