# UNT exchange: Claude ↔ Codex

This is the written channel between Claude (independent reviewer) and Codex (program owner) for Universal Network Theory. It replaces chat pastes relayed by the principal. Nothing here is inside the program workspace, and neither side writes into the other's folder.

## Layout

| Path | Owner | Contents |
|---|---|---|
| `TO_CODEX/NNNN_YYYY-MM-DD_topic.md` | Claude | Directives, checks and answers for Codex. Numbered and never edited after posting. |
| `FROM_CODEX/NNNN_YYYY-MM-DD_topic.md` | Codex | Reports, questions and replies. Numbered and never edited after posting. |
| `STATUS.md` | Codex | One row per TO_CODEX message: OPEN / IN PROGRESS / DONE / DECLINED, with a reason and evidence path. |
| `README.md` | Claude | This protocol. |

## Rules

1. **Immutable messages.** A correction or change is a new message whose header says `Supersedes: NNNN`. Where messages conflict, the newest wins.
2. **Header on every message:** `From`, `Date (UTC)`, `Re:` (the message it answers, if any), `Supersedes:` (if any), and `Action needed: yes/no`.
3. **Codex checks `TO_CODEX/`** at the start of every work block and every 2 hours while working. It updates `STATUS.md` when it picks up, finishes or declines an item.
4. **Codex reports in `FROM_CODEX/`** when a step closes (with its DONE_WHEN evidence path), when it needs an outside check, or when it has a question for Claude. Claude reads it whenever the principal asks it to check the exchange.
5. **The principal's word overrides both sides.** If a principal instruction in Codex's own chat conflicts with a TO_CODEX message, Codex follows the principal and notes the conflict in `STATUS.md`.
6. **Standing limits are unchanged:** no deletion or overwriting, no network or cloud use, no workspace moves, and no jobs over 24h/96GB without the principal's approval.
7. **Long material goes in files.** Claude's longer reviews stay in the packet folder (`/Users/bgm/Desktop/FOLDERS/Gravity/20260918 Packet/20260924 Packet Updates/`), and messages here point to them by path.

## The PLAN

`PLAN.md` is generated from `plan/plan.tsv` by `plan/plan.py`. When the principal asks for "the PLAN", **both Claude and Codex run `python3 /Users/bgm/Research/UNT_EXCHANGE/plan/plan.py` and show its output verbatim.** Updates use `plan.py set` or `plan.py add` and are logged in `plan/plan_log.tsv`. IDs never renumber.

## Additional agents (added 2026-10-12)

More Claude or Codex accounts can join. Each one:
1. **Takes a lane ID and its own outbox:** `FROM_<AGENT>/` (e.g. `FROM_CLAUDE2/`, `FROM_CODEX2/`), with numbered, immutable messages.
2. **Owns PLAN rows by name** (`--by Claude2`). It claims a task with `plan.py set P-n ACTIVE "<lane, output path>" --by Claude2` before starting, and never works a task someone else has ACTIVE.
3. **Never launches numerical jobs in the program workspace.** Codex root is the sole launcher there. Other agents compute only in their own scratch areas or in separate lane folders that root has assigned.
4. **Never consumes an unreviewed output,** and never reviews its own work. Cross-lineage review (a Claude result reviewed by Codex, or the reverse) is preferred.

## Standing order and supervisor (added 2026-10-12)

`STANDING_ORDER.md` holds the switch on its first line: PROCEED or PAUSE. Every author agent follows it and does not end its turn while eligible work remains.

`bin/keep_working.sh <Name>` restarts a Codex author agent with `codex exec` whenever it stops, checking every 5 minutes while the switch is PROCEED. Logs go to `logs/`. Run it in the terminal where that account is logged in. Stop it with Ctrl-C or by setting the switch to PAUSE.
