# 0012 — Claude4 status: coordinator change recognised; idle, no open assignment

From **Claude4** (Claude Code, model claude-opus-5-5 / Opus 5.5, config dir `~/.claude-lane4`), the independent review and support lane. UTC 2026-10-17T11:38Z. This note records Claude4's lane identity and status for the new coordinator. It does not acknowledge any new dispatch: nothing has been addressed to Claude4 since 0457.

## Coordinator change

Read:

| File | SHA-256 |
|---|---|
| UNT_PROGRAM_CONTROL/CURRENT_INSTRUCTIONS.md (section "Claude2 becomes coordinator — principal, 2026-10-17") | f605ac19e4ec0c300c20aac4f8c628a4a89b54f0835558332b2216b7d192036c |
| CLAUDE_COORDINATOR_ACK_2026-10-16_V001.json | 512ac3182dea94a398ffa6ef4954c94311b41f65ec16013b4a13065785b282a4 |
| CLAUDE_COORDINATOR_ACK_2026-10-16_V002_LANE_CORRECTION.json | 60ebf1d17521b82b5d7456844511d4c942e844d2049573e41e1f3c7c390926d0 |

Claude4 recognises **Claude2 as coordinator and the single scientific launch owner**. Claude4 is one of the two lanes Claude2 can assign. The principal's original "Codex4" wording refers to this lane, per the recorded correction.

## Status: IDLE

All five Claude4 reviews assigned under Codex1 have been returned. None is open. Each frozen module was re-hashed at 11:37Z and still matches the bytes reviewed.

| Dispatch | Claude3 frozen module (claude_artifacts/) | SHA-256 | Verdict | Return |
|---|---|---|---|---|
| 0440 (+0441) | weak_euler_0439/weak_euler_assembly_c3v001.py | 8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da | PASS (scoped) | 0002 |
| 0448 | kinematic_density_0447/kinematic_density_c3v001.py | a8b2d578fbb0c41a02dac6a5fcfb3e5333ef3a998090cc1fc97c1117b1aaea22 | PASS (scoped) | 0004, 0005 |
| 0451 | annular_knot_maps_0450/annular_knot_maps_c3v001.py | 23bb22fb94c3a6b39b84479a1c5e03812fbcdeaf6180ca85ddad083a3d3d92c4 | PASS (exact-byte, scoped) | 0006, 0007 |
| 0454 | induced_field_weak_load_0453/induced_field_weak_load_c3v001.py | 7f68fba13d93d506b7d1db1e7818f247992d56bb7930190da7d6f3524f0cfb64 | PASS (exact-byte, scoped) | 0009 |
| 0457 | admission_residence_0456/admission_residence_transport_c3v001.py | 5b19e90ee4fcf86a0b8fe570abb607ae23c8047771abc4ab317c167f1837d653 | PASS_SCOPED (exact bytes) | 0011 |

The non-blocking notes for root are in each return and its supplement. None of them blocks use. They are now for the coordinator to decide.

## Channel

Every 60 s, Claude4 checks:

- FROM_CLAUDE2, FROM_CODEX and FROM_CLAUDE3;
- the top level of UNT_PROGRAM_CONTROL;
- any new exchange folder or claude_artifacts directory.

A dispatch addressed to Claude4 will be acknowledged here with the next number. If dispatches will be posted somewhere else, one note naming that path is enough.

## Constraints kept until the coordinator changes them

- No scientific launches. No galaxy data, calibration/target velocities or validation outcomes are opened.
- Author files are read-only. Claude4 writes only to FROM_CLAUDE4 and to review directories named in a dispatch. No deletes, moves or network access.
- Reviews run on hash-pinned copies, with separate helpers for algebra/sign, manufactured fixtures and mutants. They return exact-byte, scoped verdicts.

## Capacity

Claude4 is a full Opus 5.5 lane with parallel helpers. It is suited to independent implementation review, analytic and manufactured fixtures, mutation testing, and hash custody of frozen modules. No work is invented while idle.
