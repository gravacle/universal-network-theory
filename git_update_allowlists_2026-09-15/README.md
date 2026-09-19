# Git update allowlists

This directory prepares, but does not authorize, eight proposed commits for
`gravacle/where-atoms-come-from`.  It does not stage, commit, push, tag, change
a remote, or publish anything.

Each `allowlist_*.txt` is an exact repository-relative path manifest.  Paths
not named in one of those files are not candidates for that proposed commit.
`candidate_inventory.tsv` records every currently modified tracked or
untracked, unignored path and assigns it one of four dispositions:

- `selected`: present in exactly one commit allowlist;
- `excluded`: caught by a categorical ban; or
- `deferred`: deliberately withheld from this public update until its stated
  portability or sanitization condition is met; or
- `manual_review`: deliberately absent from every allowlist until a person
  decides whether to include, exclude, or defer it.

`review_resolutions.tsv` is the exact-path adjudication record for the former
review queue. It distinguishes selected-and-content-approved files from
included, excluded, and deferred files and records a reason for every
decision. `manual_review.tsv` contains only unresolved paths; its current
header-only state is enforced by the verifier.

The inventory refresher is fail-closed: it never adds a path to an allowlist.
Any new worktree file becomes either categorically excluded or manual review.
Run:

```sh
python3 git_update_allowlists_2026-09-15/refresh_candidate_inventory.py
python3 git_update_allowlists_2026-09-15/verify_allowlists.py
```

The verifier requires an empty Git index; proves the allowlists are disjoint;
checks every selected path exists and remains modified or untracked; compares
the complete live candidate set with the recorded inventory; refuses excluded
path classes, common secret patterns, and live AWS identifier patterns; and
rejects any selected file at or above GitHub's normal 100,000,000-byte limit.
It also requires exactly the eight groups below, pins group 08 to the sole L14
terminal-disposition record, and rejects superseded blueprint, Stage-6, or L14
runtime paths from group 07. Current group-07 JSON, Markdown, and TSV proof
surfaces are also checked for retired Stage-6 terminology. The sole exception
is the exact set of 18 hash-pinned native Hamiltonian/probe inputs selected by
the Gate closure; their two historical directory names contain `STAGE6R2`, but
no adjudication, classifier, record-flow, or supplemental Stage-6 artifact is
admitted.

## Commit groups

1. Repository hygiene and the curation boundary.
2. Canonical L12 execution-control foundation.
3. L12 execution, repair, and adjudication.
4. Cross-scale theorem, finite ARGER Gate, and the separately typed
   L08/L10/L12 progression diagnostic. Historical Stage-6 development remains
   repository provenance only; it is not a governing proof dependency.
5. Reproducible L14 implementation and historical attempt custody, excluding
   raw AWS state. The selected surface remains subject to identifier review;
   the run itself is terminal and incomplete.
6. URM and proof reconciliation through authenticated L12. The governing
   finite result is the adopted ARGER Gate: exact bounded membership,
   deduplicated mass above `0.50`, and authenticated positive finite probe
   visibility across all 13 unique sectors.
7. Zenodo reproduction preparation for the governing finite proof path. The
   release packet excludes the retired Stage-6 classifier machinery and treats
   L14 only through its terminal no-result disposition.
8. L14 terminal disposition:
   `INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT`, with no L14 numerical value.

The final release reconciliation remains a later, separately reviewed commit.
The L14 computation is not pending and is not a prerequisite for the adopted
finite Gate.

## Current preparation state

The 2026-09-19 post-adjudication theorem and publication refresh passes the fail-closed
verifier with an empty Git index:

- `15,731` total candidates: `43` tracked modifications and `15,688` untracked
  files;
- dispositions: `663` selected, `15,054` excluded, `14` explicitly deferred,
  and `0` manual review;
- selected groups: `01=17`, `02=117`, `03=210`, `04=165`, `05=59`, `06=63`,
  `07=31`, and `08=1`;
- `0` unresolved review-queue rows; the exact decisions for all former `229`
  rows are retained in `review_resolutions.tsv`; and
- largest selected file: `2,747,554` bytes, below GitHub's normal single-file
  limit.

Group 07 is the exact 31-file frozen Zenodo-preparation tree. It contains no
retired Stage-6 release machinery or L14 runtime payload, includes the final
Universal Network Theory Major Proof Index and Universal Network Theory Closure
Theorem in publication formats plus executable closures, and consumes the
canonical strict progression record from group 04 without duplicating its
source copy.

This verified snapshot is still a preparation record. The review queue is
fully adjudicated, but no allowlist or resolution row authorizes a commit or
push.

## Categorical exclusions

The plan excludes cache payloads, workspaces, packaged runtimes, wheels,
generated source archives, progress and log journals, raw AWS allocation and
launch state, paid-attempt records, activation commands, and nested retired or
duplicated custody trees. The superseded Zenodo planning blueprint is also
excluded in favor of the current executable reproduction packet. Exclusion
means "not in this Git update," not deletion from disk.

## Resolved review policy

Superseded L12 V005--V011 packets, the V002 L14 implementation, duplicated
compact evidence, generated test-artifact trees, raw worker state, and the
retired Stage-6 exploratory adapter are explicitly excluded. Three sealed
historical schedule files are included in group 02. Eighteen selected L14
source/audit files passed content review. Fourteen paths are explicitly
deferred: live-AWS-bound source/audits, nonportable generated manifests and
early feasibility outputs, and the unexecuted workstation-bound account
handoff protocol. No directory-wide admission rule was used; every former
review row has an exact-path resolution followed by both checks above.
