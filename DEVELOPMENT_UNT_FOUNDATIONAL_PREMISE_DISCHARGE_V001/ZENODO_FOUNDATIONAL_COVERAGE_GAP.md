# Zenodo foundational coverage gap

**Audit date:** 2026-09-25
**Archive inspected:**
`publication/zenodo_reproduction_v001/dist/zenodo-upload-v1.0.0/universal-network-theory-reproduction-v1.0.0.zip`

**Archive size:** `333113506` bytes
**SHA-256:**
`26cde042a9e709be59da23afd083fb2ec2d5e476bf267e3713f3a59151d20c25`

**Source manifest:** `publication/zenodo_reproduction_v001/capsule_manifest.json`
**Manifest SHA-256:**
`75b8a80ad8dc39e92d1a3b031469fbe1019fc1a072d6b7bf3fd97abd0794dca9`

The existing archive is internally intact: all 225 manifest-declared archive
paths are present; its build ledger contains 346 file records; and the audit
found zero missing declared files or build/hash mismatches. The coverage issue
below is therefore a curation-boundary issue, not archive corruption.

## Finding

The archive is internally consistent with its declared purpose: it calls itself
a curated finite relational reproduction capsule for `L = 4` through `L = 12`.
It is not a complete reproduction package for every foundational step in the
record-to-geometry/gravity program.

That distinction explains much of the apparent mismatch. The package contains
the finite headline evidence and the conditional gravity closure, but several
theorems, negative results, and the RGRL adoption record needed to audit the
meaning of that closure are available only in the broader Git repository. A
reader of the ZIP alone can therefore see the endpoint more easily than the
foundational path and its failed alternatives.

The frozen master closure, architecture, and proof index bytes in the ZIP agree
with Git tag `v1.0.0` and differ from current post-release working bytes. They
must not be retrofitted into the existing archive. Any correction or supplement
requires a new version with its own freeze and audit.

## Byte-level initial crosswalk

The table below is based on the finished ZIP member list, not on filenames
assumed from the source tree.

| Foundational item | Repository role | ZIP status | Consequence |
|---|---|---|---|
| Finite L4-L12 theorem, audit, evidence, and ARGER reconstruction | Main finite release result | Included | Headline finite claim is reproducible at the capsule's declared ceiling. |
| `GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md` and audit | Conditional macroscopic endpoint | Included twice: root/navigation and `gravity/` | The implication is visible and auditable as a document. |
| `GRAVITY_FORMATION_THEORY_CLOSURE_V001.md` and audit | Public GFT closure | Included under `gravity/` | Public closure wording is present. |
| `GRAVITY_RGRL_POST_ADOPTION_STRUCTURAL_THEOREM_V001.md` | Post-adoption structural composition | Included | Some adopted-branch structure is visible. |
| Audit of the post-adoption structural theorem | Independent ceiling for the preceding theorem | Omitted | The theorem is present without its dedicated audit packet. |
| `GRAVITY_RGRL_ADOPTION_V001.md` and audit | Exact statement that RGRL is an adopted physical postulate rather than evidence | Omitted | The most important logical status is stated inside the closure, but its controlling adoption packet is not independently packaged. |
| PMICS theorem and hostile audit | Load-bearing curvature-capacity lemma cited by the closure | Omitted | A ZIP-only reviewer cannot reproduce or inspect the theorem that supplies the stated intrinsic-curvature capacity. |
| PMSR theorem and hostile audit | Load-bearing finite pair-memory/source reciprocity lemma cited by the closure | Omitted | The exact same-parent partial bridge and its noncommuting-F3 ceiling cannot be inspected from the ZIP. |
| SDCP/EX theorem and hostile audit | Conditional six-spatial-equations plus Ward/constraints closure cited by the closure | Omitted | The exact implication is visible only through the endpoint document, not its theorem packet. |
| RIEHB theorem and hostile audit | Conditional post-geometry Einstein-Hilbert/back-reaction mechanism cited by the closure | Omitted | The common-metric, coefficient-sign, tangent-span, and explicit-force premises cannot be audited from the capsule source packet. |
| GL6AV theorem and independent audit | Same-parent retained-formation/collective-clock and partial metric-bridge evidence | Omitted | A genuine foundational dynamics result and its explicit ceiling are invisible as executable source. |
| GL6BQ theorem | Author-claimed exact non-Ricci boundary for the authenticated finite orientation orbit, plus a separate conditional degree-six-design theorem | Omitted, and not publication-ready | The negative and conditional claims must remain split. Their manifest-listed verifier/result/verification/self-audit files are absent from the current tree and no distinct hostile audit was located. Restore and audit before promotion or packaging. |
| `GRAVITY_DEFINED_V001.md` and G2 replay | Early Gauss-Bonnet/topology construction, with superseded physical identification | Source packet omitted; summarized in included `REGISTER_V001.md` | History is discoverable, but the exact source/replay and supersession context are not a first-class packet. |
| H15 carrier-holonomy test | Exact finite negative result: tested carrier curvature and record content are independent | Source packet omitted; summarized in included `REGISTER_V001.md` | The rejected curvature shortcut is not directly reproducible from the capsule. |
| `GRAVITY_RECORD_FIRST_DIRECT_PROOF_PLAN_V001.md` | Current deeper-derivation map | Omitted | The distinction between working closure and stronger microscopic derivation is harder to follow. |
| `GRAVITY_NO_LAB_PROOF_TASK_PLAN_V001.md` | Open proof obligations | Omitted | Remaining work is not represented as a reproducible dependency surface. |
| `GRAVITY_EMERGENCE_EXPERIMENT_REGISTER_V001.md` | Exact, computed, and negative emergence lanes | Omitted | Much of the program's nontrivial foundational and falsification record is absent. |
| Full AURFT closure packet and dependency closure | Load-bearing universal record-formation chain | Partial: theorem/audit included, packet support and most pinned dependencies omitted | The public result is present, but its complete repository proof packet is not capsule-reproducible. |

The ZIP does include `REGISTER_V001.md` in its URM material and another pinned
proof-packet layout. That supplies historical summaries, but a summary is not a
substitute for the theorem/audit/replay packet when the result is load bearing.

## What is missing conceptually

The current archive is strongest at:

```text
finite record envelope -> adopted finite Gate classification
conditional RGRL/WTC hypotheses -> Einstein-Hilbert response
```

It is weaker as a self-contained account of:

```text
why earlier geometry candidates failed
what exact partial geometry/response lemmas survived
which physical bridges were adopted rather than derived
what must still be proved for microscopic record dynamics to earn gravity
```

This is a coverage gap, not evidence that the omitted work never happened. The
repository shows that it did happen. It also shows that some early
interpretations were superseded and several attractive shortcuts failed.

The gravity closure makes the gap mechanically checkable: all 11 hash-pinned
files in its source table are absent from the manifest/ZIP, including RGRL
adoption, the frozen final theorem/audit, and the PMICS, PMSR, RIEHB, and
SDCP/EX theorem/audit pairs. Their current local hashes match the hashes printed
by the included closure, so the issue is omission rather than dependency drift.

## Minimal next-version supplement

Without changing the current published record, a future version should add a
small foundational supplement containing:

1. the completed `FOUNDATIONAL_CLAIM_LEDGER.tsv`, dependency DAG, and this
   release crosswalk;
2. the complete AURFT closure packet, its six missing upstream theorem packets,
   and the absent alpha manifest-pinned bytes required by that closure;
3. the RGRL adoption record and audit, plus the audit of the already included
   post-adoption structural theorem;
4. the existing PMICS, PMSR, RIEHB, and SDCP/EX theorem/audit/verifier custody,
   each wrapped by a new explicit status/coverage manifest where the historical
   lane does not already contain a complete manifest, plus the frozen final
   theorem/audit bytes pinned by the record-first closure;
5. a corrected topology/methods appendix containing G7, the narrow surviving
   G2 corollary, H9's wrong-object correction, H14's carrier-observable
   selection, and the corrected finite Z2 H15 negative control;
6. GL6AV and its independent audit as an extended partial-bridge appendix;
7. a curated extract of the gravity emergence register containing every result
   that is load bearing or route closing; and
8. a machine-readable claim-to-file map stating `included`, `summary-only`,
   `historical/superseded`, `publication hold`, or `external repository
   dependency`.

GL6BQ should remain on publication hold until its manifest-listed packet files
are restored and it receives a distinct audit. The current master closure and
its new audit may enter only after new-version bytes are frozen; neither may be
presented as if it audited the frozen `v1.0.0` archive.

Do not add superseded `PROOF_V001`, the L12-only block theorem/audit, legacy
Stage-6 wrapper/classifier machinery, failed L14 assets, or active partial
outputs. Their corrected successors or disposition records already carry the
relevant history.

The supplement should not claim that packaging a theorem strengthens it. Its
purpose is to make the actual proof structure—including adopted premises,
negative results, and open arrows—visible to a hostile independent reviewer.

## Publication rule proposed by this audit

Any theorem used by a public closure should meet one of two conditions:

- its full theorem/audit/replay custody is inside the release; or
- the release identifies it explicitly as an external historical dependency
  and states that the capsule does not reproduce it.

No omitted premise should be presented as if omission meant proof, and no
superseded historical result should be restored merely to make the package look
more complete.
