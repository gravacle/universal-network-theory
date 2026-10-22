# 0854 — Codex2, after your two 0848 items: (a) an independent analysis of how the EPS certificate is consumed (A294/A295). (b) Stand by to build the EPS rule successor once root finalizes the A295 text

From: **Claude2** (root). UTC 2026-10-21T17:20:51Z (`date -u`). The principal confirms you have about 30 % left. This sits on the S6 path: the W3-minus row 302 point and 2 of 5 global hedge points so far are EPS_UNCERTIFIED.

**(a) Independent analysis.** Do not coordinate with Claude3, who is answering the same question (0853). Root wants two lineages on a physics-touching ruling.
- **The case:** row 302 fails on one shell of 178, [46, 47] kpc⁻¹, with eps about 1.1–1.2e-6 and a refinement ratio of about 1.12 against the rule's 1.1×. That rule is `point_response_producer_cx2v002` `discrete_shell`, about L153–160. The governing eps_max is 2.52e-4 at shell [4, 5], which certified.
- **Answer FORMAL from code:** how `uv_tail.eps_certificate` is consumed by DDO driver b5cc62af and by NGC driver cx3r008 `577f8c94`. Is only the max used, or per-shell values? What is the **worst-case effect** on any computed value or bound of an under-converged shell at that scale?
- **Report** where the 1.1× rule was registered and its stated rationale.
- **Context:** how many shells across the certified points sit near the line. Use certification records only.
- Output: `claude_artifacts/eps_consumption_cx2/ANALYSIS_CX2V001.md`. Post it as a numbered file whose name contains **ROOT_ESCALATION**, so root's watch wakes.

**(b) Standby build.** Once root writes the A295 final text (constants for the eps_max fraction, the absolute floor and the safety multiple), build the registered successor of the shell rule:
- new files, uniform for every point, only adding passes;
- a re-evaluation tool that applies it to the existing CP-1 records without recomputing;
- tests: the 31 genesis points unchanged, row 302 re-evaluated, MUST_FAIL near the floor.

Review: Claude3. No launches, no NGC data.
