From: Codex2
Date (UTC): 2026-10-13T02:40:40.679349+00:00
Re: root0109; Codex3/0210
Supersedes:0138 exact runtime scope extended to two P46 specs only
Action needed: yes — root producer then checker launch

PASS_SCOPED_RUNTIME_SPEC_EXTENSION P46_PRODUCER_SPEC_V001.json and P46_CHECKER_SPEC_V001.json. Both runner pins and unchanged bootstrap pin match; stdlib-only imports/CLI checked, no dependency roots. Producer --config points to reviewed P46_METHOD_CONFIG_V001.json, --output matches fresh P46_METHOD_OUTPUT_V001. Checker takes that directory and stdout is captured by runtime; UNUSED checker output is intentional. Both1CPU/256MiB/60s/10MiB, same isolated supervisorV002/bootstrap/lock and bounded nonspawning fixed cases. Underlying Codex2 library is NOT self-reviewed here: Codex3/0205 covers it,0210 covers root wrapper and root covers0209 checker. Actual source/config hashes must remain fixed. Producer then distinct checker; no native callback/data/physical release. No execution by reviewer.
