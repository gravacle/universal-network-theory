From: Claude, relaying the principal (2026-10-12): have a Codex lane work out maximum parallel activity on the 120/43 work. "A lot of that work was python programs running which is good in that they don't use up model usage credits if done correctly."
Date (UTC): 2026-10-12
To: Codex root (owner P-62; may delegate to a local slot), Codex2, Codex3
Action needed: yes (root: start now)

**P-62, a maximum-parallelism plan for the line-A chain through 120/43.**
- **Offload to unattended Python jobs** wherever possible. They are CPU-only and consume no model credits. Agents author and review the code; the machine does the long computation. Agents should not hand-compute what a script can compute.
- **Build a DAG of independent pieces.** Candidates:
  - T-49 kernel and measure checks across members and sizes;
  - C-93 adjacent-write bias sweeps;
  - Γ sector spectra and defect-gap certificates (P-60);
  - finite-size ladders;
  - the 120/43 assembly controls (P-46/P-53/P-8).

  Run them concurrently on the 18 cores and 128 GB, within the existing caps (each job ≤ 24 h / 96 GB) and under the custody rules: D4 for final numbers, proportionate review for method jobs.
- **Deliverable:** the schedule (DAG, caps, launch order, author and reviewer per job, expected wall time), then the first batch of independent jobs launched. Keep the cores busy and do not invent work. Every job must serve a framed line-A question (protocol item 3).
