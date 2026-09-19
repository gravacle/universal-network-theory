# PROOF — WHERE ATOMS COME FROM — V002 — reconciled 2026-09-15

> **"We need a model to work on that represents the full project."** — the principal, 2026-08-20
>
> **"The model should be the overall representation of the proof."** — the principal, 2026-08-20

This generated document narrates the **UNIVERSAL RECORD MODEL** — `MODEL.md`,
`model/project_model.py`, and the executable certificate modules. Every claim carries a model
function or explicitly says `none`, a validator gate or explicitly says `none`, its grounding, and
its ledger row. A narrated dependency is not promoted merely because it appears here.

**`PROOF_V001.md` is not superseded as mathematics.** Its Theorems A–D stand unchanged; what this
document changes is their siting. They are statements about the **DEF-A corner** — §4 — and they are
`FORMAL`. The program's proof is no longer those theorems; it is the model, and this is the model's
narration.

---

## 0.1 WHAT `PROOF` MEANS IN THIS DOCUMENT

> **The principal, 2026-08-20:** *"The PROOF must be something that any physicist anywhere in the
> world can run against their real world data and confirm that it works as asserted. That is a proof.
> Otherwise we're not proving anything other than that we can construct equations."*

A row is `PROVED` only when it names **(1)** the measurable quantity in units, **(2)** the predicted
value or relation, **(3)** what would falsify it, and **(4)** at least **two structurally different
real record surfaces** — different mechanism, never different parameters.

**Only requirement (4) is enforced by a tool.** `ledger/status.py` refuses the status unless the row's
grounding carries a `RECORDS VERIFIED:` line naming at least two distinct surfaces. Requirements
(1)–(3) are enforced by the registrar reading the row, and by nothing else. That asymmetry is stated
here because a bar half-enforced by a tool and half by a person is exactly the shape every guard in
this program had before it started refusing.

**One row in this program holds that status: `C-71`, and §3 states it in full.** Its measurement is
a *within-part comparison* — the shift of a programmed page's `V_t` distribution against the same
part's own erased population — so it needs no absolute baseline, and that is why it survived the
erratum below.

**`C-72` was `PROVED` and is now `PARTIAL`, on this document's own finding.** Writing §3 surfaced
that its registered prediction, *"the ratio is 1 for every data pattern"*, was an **algebraic identity
of scoring an erased cell as exactly zero charge** — the sealed lane's own source says so — while the
same model layer gives those cells a `±5 e` residual, under which the ratio is `0.968`–`0.980` and
depends on the pattern. That is `C-72`'s **own registered falsifier**, fired by its own model. A
replacement protocol was drafted and then **refuted by two independent refuters**: the ratio is not
translation-free, so it needs `V_t,neutral` to better than the tolerance it is bounding, which is not
a datasheet number. **What survives is computed and confirmed** — a data-independent floor with no `N`
in it, against an orientation surface that screens as `N^{-1/2}`, so the two encodings differ in kind
and their separation grows as `√N`. What does not survive is a runnable prediction. The repair is
`T-50`.

**`C-71`'s surface is MODELLED** — constants pinned to literature classes, patterns drawn from sealed
seeds. `RECORDS VERIFIED` names two structurally different real *mechanisms* whose standards were
scored inside the model; **no device was measured.** What is offered to the outside is the falsifier.

Every other claim here is `FORMAL`, `DEFINED`, `CANDIDATE`, `PARTIAL` or `OPEN`, and each block prints
its own. **A `FORMAL` result is real mathematics about the program's own stipulated definition and is
not a claim about the world** (`H-3`, `PARTIAL`, standing).

**This document does not claim that gravity has been derived.** §5 states what has been computed;
§6 makes the one comparison the program permits, with the conditions that are not earned named in
the same sentences as the result.

---

## 0.2 HOW TO READ A CLAIM BLOCK

Every claim is one block. The five cells are the claim's whole warrant:

| cell | what it is |
|---|---|
| **model** | the URM function that carries the claim. `none` means narration, and the scope cell says why |
| **gate** | the validator check that fires on it, as `file :: check name`. `none` means no gate exists yet |
| **grounding** | where the numbers come from: a sealed lane, a `D-25` provenance entry, or a pinned external source |
| **rows** | the rows it rests on, each with its **status** and its **carrier mark**. A row is a claim in `ledger/status_ledger.tsv` or a task in `ledger/plan.tsv`; a task prints its plan status and the tier `PLAN`, and is never carrier evidence |
| **scope** | the caveat that travels with the claim wherever it is quoted — what the claim does **not** say |

The carrier mark is the `T-9` audit's verdict (`LANE_T9_AUDIT/T9_carrier_audit.tsv`): `TWO-CARRIER`
means the result stands on two structurally different carriers; `SINGLE-CARRIER` means one;
`NOT-CARRIER-SHAPED` means the result is not the kind of thing a carrier carries.

**`UNAUDITED` means the row carries no mark at all**, and it is not a weaker `SINGLE-CARRIER`. The
audit's original scope was the then-live `FORMAL`, `PROVED` and `MEASURED` rows, and its T-52
extension brought every later in-scope row through the same audit. `DEFINED`, `PARTIAL`, `CANDIDATE`,
`OPEN` and `BLOCKED` rows remain unaudited unless an extension explicitly reaches them. **A block
resting on no `TWO-CARRIER` row opens its scope
cell with `SINGLE-CARRIER —`**, and an unaudited row never lifts that requirement.

**Of the 157 retained audit verdicts, 116 are `SINGLE-CARRIER`, 22 are
`TWO-CARRIER`, and 19 are `NOT-CARRIER-SHAPED`.** Those verdicts cover all 156
rows currently in the audit's `FORMAL`/`PROVED`/`MEASURED` status scope; the
extra retained verdict is C-72, which moved to `PARTIAL` after it was audited.
That is the program's state, printed rather than described.

---

## 0.3 HOW TO CHECK THIS DOCUMENT

Each line runs from the repository root:

```bash
python3 replicate/check_proof.py      # this document's own gate — expect GATE PASSED
python3 LANE_RFT_AXIOMATIC_URFT_CLOSURE_V001/verify_axiomatic_urft_closure.py
python3 model/validate_gravity_formation_theory.py
python3 model/validate_relational_accumulation.py
python3 model/validate_urm.py         # aggregate comparison against the dated baseline
```

The first three scientific families above are focused gates. The AURFT verifier passes 74/74 after
the manifest resolver was made lane-local-first, the Gravity Formation Theory validator passes, and
the relational validator passes 177 checks. **The aggregate URM validator is not advertised as
green.** Its dated pre-reconciliation baseline is `URM_VALIDATION_BASELINE_2026-09-15.md`: ARROW
26/27, an absent zero-scientific-weight `lakeshore_vsm` adapter/check, and an absent synthetic-gamma
fixture. A current run must be compared with that baseline so inherited failures are not mislabeled
as relational regressions and a partial pass is not printed as an aggregate success.

The broader clean-reproduction debt remains `T-35`; release reconciliation is `T-57`; publication
and deposit remain blocked under `T-58` until the scientific and human release inputs are complete.

`check_proof.py` **refuses** a block with a missing field, a row that is in neither the ledger nor the
plan, a row that is `WITHDRAWN` or `FAILED`, a status or carrier mark that has gone stale against the
record, an unmarked single-carrier block, a model function or gate name that does not exist, the word
`PROVED` without a `PROVED` row behind it, or a banned classical-gravity comparison outside §6. It
exits `2` rather than passing when it cannot read the ledger or the audit.

**What it does not reach is section prose.** R1–R9 and R11 parse `### P-` blocks only and close at the
next heading; only R10's `D-1` scan reads the whole file. **Every section header in this document,
§0 included, cites no ledger row and is enforced by nothing but that scan** — which is why the headers
below carry no claim that is not also in a block. Closing that gap is the gate's own standing debt.

**What this document does not have, stated up front.** {{STATS}} The blocks without a gate are
narration over sealed lane output, and each one says so in its scope cell. Closing that gap — every
claim in this proof gated by a check in `model/` — is the proof's own standing debt.
