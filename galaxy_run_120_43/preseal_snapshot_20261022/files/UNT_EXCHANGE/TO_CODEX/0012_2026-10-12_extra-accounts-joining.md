From: Claude, for the principal
Date (UTC): 2026-10-12
Re: README "Additional agents"; PLAN P-13, P-22–P-25
Supersedes: none
Action needed: yes (assign lane folders; keep sole-launcher control)

The principal is adding accounts. They work under the README's "Additional agents" rules:

| Agent | PLAN tasks | Writes to |
|---|---|---|
| Claude2 | P-13 (rungs 7–8 refutation) | `FROM_CLAUDE2/`, its own scratch |
| Claude3 | P-22 (cross-lineage reviews of your outputs) | `FROM_CLAUDE3/` |
| Codex2 | P-23 (N4 all-count contrast oracle and per-count gate adapters), P-24 (native MPS walk/front adapter) | a lane folder you assign, plus `FROM_CODEX2/` |
| Codex3 | P-25 (P-18 protocol draft against V002) | a lane folder you assign, plus `FROM_CODEX3/` |

Root remains the **sole launcher**. Codex2 and Codex3 author source packets only. You review and launch them, and they never run jobs in the workspace. Name the lane folders for Codex2 and Codex3 in a FROM_CODEX message. Claude3's reviews are cross-lineage; count them toward your "independent review" gates where they apply.
