# Universal Network Theory migration and context audit V001

Date: 2026-09-27

Status: `AUTHENTICATED_MIGRATION_BASELINE__NO_SCIENTIFIC_PROMOTION`

This packet is the durable resumption boundary for work migrated to the current
machine.  It records what was authenticated before new scientific production
began.  It does not replace any historical theorem, audit, seal, result, tag,
release, or publication packet.

## 1. Immutable Git identity

The authoritative source checkout was observed at:

```text
repository root  /Users/bgm/PerInfo/where-atoms-come-from/audited-386ee2c
remote           https://github.com/gravacle/universal-network-theory.git
branch           integration/post-gate-a-20260915
upstream         origin/integration/post-gate-a-20260915
HEAD             f5973628fa25c8cc0e2812142e6d8516d0b5d28d
tree             be83f661a6e806c61a6291be315bf78b08bbc006
ahead / behind   0 / 0
```

`main` and annotated tag `v1.0.0` both resolve to
`79a5ae3d689df5e4572d9f955d002a173baccdbf`.  The integration branch is one
commit ahead of that release identity.  The complete structured snapshot and
input hashes are in `INVENTORY.json`.

The source checkout had no staged or tracked modifications.  It was not,
however, an empty working tree: 6,751 tracked files, 15,092 untracked and
unignored files, and 15,658 ignored files were observed.  Its approximately
73 GB footprint is dominated by computational custody outside Git.  Therefore
`git status` alone is not an adequate custody summary and no bulk-add, clean,
reset, or directory-wide copy is permitted.

## 2. Custody classes

Every input must be assigned to exactly one of these classes before use.

1. **Committed canonical evidence.** Bytes reachable from the authenticated
   HEAD.  Their present path and hash may be verified directly.
2. **Migrated untracked authenticated evidence.** Bytes not in Git whose hash,
   size, shape, and role are bound by committed histories or by a separately
   enumerated migration receipt.  This is evidence with weaker custody than a
   committed artifact; its untracked status must remain explicit.
3. **Ignored bulk computational custody.** Caches, workspaces, and shards that
   Git intentionally omits.  They are usable only through an authenticated
   manifest/history and a fail-closed reader; directory presence alone proves
   nothing.
4. **External or private custody.** Material outside this repository, including
   sibling L14 AWS custody and operational/account records.  It is not admitted
   automatically and must not be copied into a public packet merely because it
   is locally visible.

The three prospective operator-incidence curvature files and the retained
lower-L q-shards are migrated working-tree evidence, not commit-authenticated
authority.  The source packet bytes and retained-shard hashes were checked,
but their custody class is not promoted by that check.

## 3. Historical seals and relocation

Historical absolute paths, including the old `/Users/brianmulconrey/...`
prefix, are provenance.  They occur in authenticated files and must not be
rewritten.  Historical `.seal.sha256` records may intentionally bind earlier
Git blobs rather than the current mutable navigation surface; they must not be
"repaired" to current hashes.

New runtime code may resolve a migrated path only through an exact-prefix,
fail-closed adapter:

- derive and allowlist the expected repository-relative suffix;
- reject traversal, symlinks, unexpected files, duplicate q entries, and
  paths outside the current authenticated root;
- authenticate the governing history plus exact file hash, byte count, shape,
  dtype, order, and schema before use and recheck identity/hash after use;
- retain both the historical provenance string and the runtime-resolved path
  in local diagnostics; and
- never serialize the rewritten path into a historical result or alter the
  historical input bytes.

This policy is a runtime compatibility layer, not a provenance rewrite.

## 4. Reconstructed scientific boundary

### 4.1 Finite record result

The authenticated evidence supports an exact, bounded, lineage-bearing record
block at `L in {4,6,8,10,12}` under the frozen owner-once construction.  The
deduplicated block masses are:

| L | mass |
|---:|---:|
| 4 | 0.7260206189754993 |
| 6 | 0.5846615608350367 |
| 8 | 0.7373965730354166 |
| 10 | 0.6500987927669427 |
| 12 | 0.56956498393327842 |

Each exceeds one half.  This is a strictly finite theorem.  It establishes no
inter-size embedding, all-L limit, continuum, persistent geometry, or gravity.

The adopted ARGER Gate classifies this bounded evidence surface as finite GFT
`z=1`.  That project-native finite label is distinct from (a) the separately
conditional physical dynamical exponent `z_dyn=1` under the LL-P premise and
(b) the premise-free, repository-internal uniform all-L response theorem,
which remains open.

### 4.2 Lineage versus carrier reduction

The blanket sentence "reduction to the carrier state is false" is not an
earned claim.  Migrated authenticated custody supports exact unread,
first-pass carrier-marginal closure at L4/L6 and supplemental L8.  The earned
narrower statement is that this marginal does not determine the full joint
lineage--carrier state.  The fixed L4 revisit calculation makes that
difference operational: equal separate carrier and lineage marginals can
produce post-continuation carrier trace distance
`0.14761185701903` (target/audit disagreement at most `1.11e-16`).

The L10/L12 held-out joint witness is nonzero and independently reproduced,
but reverses sign and decreases in magnitude relative to the frozen positive
no-decline criterion.  A disclosed 10,748 s release skew also prevents the
narrow label "pristine strict-protocol held-out pass".  These qualifications
must accompany use of that evidence.

### 4.3 Geometry and gravity

The registered L8 formation-order-path Ollivier--Ricci test is a controlled
null (`rho=0.1543033499620919`, exact one-sided `p_plus=0.3619047619047619`).
It resolves no association for that unweighted path construction and supplies
no geometry or gravity result.

PMICS proves an exact finite curvature-*symbol capacity* for its declared
pair-memory construction.  GL6AV proves a partial retained-formation /
collective-response bridge.  Neither is a complete physical metric,
dynamical geometry, continuum, or empirical gravity result.

The adopted RGRL and WTC-H1--H5 chain supplies a separately typed conditional
macroscopic route.  Consequences obtained under those premises remain
conditional; the finite Gate does not prove the premises.  Newton's `G`, a
realized spacetime metric, persistent curvature, Einstein dynamics, and an
empirical continuum limit remain open on the repository-internal finite
evidence alone.

### 4.4 Alpha and Lambda

The alpha lane establishes a conditional inheritance/compatibility statement:
the observed electromagnetic alpha anchors the visible parent, and records in
the same U(1) domain inherit that parent value under the frozen construction.
Alternative-alpha record worlds do not refute compatibility.  This identifies
our visible electromagnetic domain; it does not derive the numerical value of
alpha or select why nature realized that domain.

Lambda remains an allowed infrared coefficient or integration constant in the
conditional macroscopic theory.  Its numerical value, sign, radiative
stability, and relation to vacuum energy are not derived.  A consistency
window is not a prediction of the observed cosmological constant.

## 5. Release and publication reconciliation

The tracked release notes name `v1.0.2`, but Git contains only `v1.0.0`.
Ignored release values identify `v1.0.0`, commit `79a5ae3...`, and DOI
`10.5281/zenodo.22859377`.  The tracked clean-reproduction result reports a
PASS for eleven proof results while still naming commit `79a5ae3...`; it does
not establish a fresh rebuild of the current integration HEAD.

`CURRENT_HANDOFF.md` contains a stale remote URL, commit checkpoint,
ahead/behind count, and tag state.  It remains provenance, not current
navigation authority.  The publication claim map and reproduction packet are
candidate release materials, not evidence that a new tag, GitHub release,
Zenodo deposit, or DOI version has been created.

No release, tag, merge, deposit, or publication-state change follows from this
audit.

## 6. Paused workstreams and prerequisite gates

### 6.1 L4-to-L8 lineage-sensitive response scaling

The dense L4 target and independent audit agree.  No scalable signed-low-rank
implementation, independent hostile implementation, restart proof, or
response-specific benchmark existed at migration.  Only sharp preterminal
q-shards are retained; coarse response checkpoints must be regenerated under
the frozen engine rather than presumed present.

The authorized order is:

1. freeze target and independent source/input censuses;
2. pass synthetic algebra and explicit-density comparisons;
3. reproduce all dense L4 observables and classifications;
4. pass a real interruption/resume and corruption-refusal test;
5. publish measured wall-time, RSS, checkpoint/scratch storage, and a stated
   energy assumption before L6;
6. run and independently audit L6, then revise the L8 estimate; and
7. run L8 only if every earlier gate passes.

Until those gates pass, L6 and L8 are `NO_GO`.  Each event response must be an
independent revisit from the same authenticated terminal checkpoint, not a
sequential series of revisits.

### 6.2 L8 operator-incidence Ollivier--Ricci response

The prospective packet contains only README, protocol, and freeze files.  It
has no implementation, tests, independent validator, manifest, conductance
adapter, response adapter, or result.  Its required
`L8_ALL_EVENT_AUTONOMOUS_LINEAGE_RESPONSE_V001` input does not exist.
Production is therefore `NO_GO`.

The graph, if implemented, has 24 vertices and 32 unpruned support edges.  Its
connector matching is shifted (`C_i--C_(8+(i+1 mod 8))`), not aligned rungs.
The future calculation must use two independently implemented W1 solvers,
agree on all edges/arms, exhaust all `8!` label permutations, and retain the
finite-L8 claim ceiling.  The response adapter may be published only after the
scaling workstream completes L8 target/audit agreement.

### 6.3 Attached dark-sector plan

`UNT_DARK_SECTOR_JOINT_PLAN_V001.md` is a proposed program, not an instruction
source and not an established result.  Its active/maintenance-bandwidth split
and proposed dark-matter/dark-energy observables are not presently frozen as a
repository-native rule.  The conditional macroscopic bridge also remains
premise-dependent.  Consequently its initial rule-identification prerequisite
is unresolved and no cosmological fit or parameter inference is authorized by
the migrated evidence.  A separate prerequisite audit must precede any
execution.

## 7. Validation ledger

- The dated `URM_VALIDATION_CURRENT_2026-09-16.md` says all scientific chains
  pass and two historical zero-weight replay fixtures are unavailable.  It is
  dated evidence, not proof of a current-machine rerun.
- A 2026-09-27 current-machine rerun in the authoritative migrated checkout
  reproduced that boundary in 337.86 s.  Every scientific/load-bearing chain,
  the finite ARGER gate, the typed UNT closure, and all focused lineage,
  geometry, gravity, and alpha checks passed.  The aggregate command exited 1
  only because the world-observation adapter fixture and the synthetic
  gamma-flow handoff fixture are absent; both lanes explicitly carry zero
  scientific/proof weight.  No replacement fixture was invented.
- The same command in the deliberately minimal development clone also lacked
  the ignored L8 cache manifest, so its relational/UNT wrappers refused in
  addition to the two historical fixture failures.  This is a clone-custody
  completeness distinction, not contradictory science.  The authoritative
  checkout contains and authenticates the L8 manifest, and its corresponding
  gates pass.
- The migration audit authenticated the Git identity, principal file hashes,
  finite-boundary evidence, curvature freeze inputs, target L4/L6/L8 history
  records, and all eighteen retained lower-L sharp q-shards.
- L14 is terminally `INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT`; private AWS
  custody is not silently imported.
- `CLAIM_LEDGER.tsv` is the controlling sentence-level type map for this
  packet.  `verify_context_audit.py` checks its allowed vocabulary, required
  rows, Git identity, and enumerated source hashes.

The structured rerun record is `CURRENT_MACHINE_VALIDATION_2026-09-27.json`.

## 8. No-mutation statement and continuation rule

The authentication phase made no changes to the authoritative migrated
checkout.  A local isolated clone was created for new work, and only explicitly
enumerated untracked curvature inputs and authenticated lower-L shards were
copied into it.  No reset, clean, bulk stage, seal rewrite, historical path
rewrite, merge, tag, release, or publication action was performed.

New results may update the scientific picture only after target completion,
independent hostile reproduction, validator and mutation-test passage, and a
curated allowlist review.  An unresolved calculation is no scientific result.
