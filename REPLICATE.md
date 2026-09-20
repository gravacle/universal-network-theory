# REPLICATE — how to check this program yourself

**Everything here is re-runnable. Nothing asks you to take a number on trust.**

```bash
git clone https://github.com/gravacle/universal-network-theory && cd universal-network-theory
./replicate/reproduce.sh --seals     # fast: verify every SHA-256 manifest
./replicate/reproduce.sh             # full: re-run every script, diff against sealed output
```

Requires **Python 3.9+** and **numpy** only. No network, no GPU, no data download. The heaviest
script needs a few minutes; `--quick` skips those.

`reproduce.sh` **exits non-zero** if any seal fails, any script's output differs from the sealed
`.txt` beside it, or the status grid does not regenerate byte-for-byte from its ledger.

```bash
python3 replicate/check_proof.py           # the proof's own gate: refuses a stale claim
python3 model/validate_project.py           # the URM's 24 project/D-25 gates
python3 model/validate_geometry.py          # 33 geometry gates; chains the above
python3 model/validate_historywise_gravity_discriminant.py  # 84 formal-only custody/ceiling checks
python3 model/validate_urm.py               # 176 family gates plus model/data/frontier/formal chains
```

---

## WHAT IS CLAIMED

Read in this order. Each is short and each links to the numbers behind it.

| | document | what it is |
|---|---|---|
| 1 | `CORE_FRAMEWORK_V001.md` | **the anchor** — the five clauses defining a record |
| 2 | `THIRD_TERM_V001.md` | Γ, defined **only by the function it performs** (R1–R3) |
| 2b | `GLOSSARY.md` | **every term, and whose it is** — BORROWED, RENAMING, or OURS. Read it before believing any claim is a discovery |
| 3 | `MODEL.md` | **the model** — records constructed from `(H,{L_k})` and nothing else |
| 4 | `STATUS_LEDGER_V001.md` | **every claim, with its status and its evidence** — generated, never typed |
| 4b | `THE_PLAN_V001.md` | **the road to a proven process** — every task with a checkable DONE WHEN. `./ledger/plan.py` |
| 5 | `PROOF_V002.md` | **the proof** — the narration of the Universal Record Model: every claim a model function, its validator gate, its grounding and its ledger row. `python3 replicate/check_proof.py` is its gate |
| 5a | `PROCESS_V002.md` | **the process as it now stands** — every sentence cites a ledger row |
| 5b | `RECORD_FORMATION_V001.md` | what a formation process must deliver |
| 6 | `REGISTER_V001.md` | the append-only record, including **everything withdrawn** |

**Start with the ledger.** It is the whole program in one grid: 90+ rows, each with a status from a
**closed vocabulary**, the evidence, what blocks it, and **what would refute it**.

---

## HOW TO CHECK ONE CLAIM

Every row names its lane. Example — the record-count law, row **C-14**:

```bash
cd model && python3 count_law.py
```

You should see **22 PASS, 0 FAIL**, and a control showing the naive reading fails on `[3,3]`,
`[6,6]`, `[5,5]`. If you get anything else, the claim is wrong and we want to know.

**Is any of it an artefact of one carrier?** That is the question `T-9` exists for:

```bash
cd LANE_T9_CARRIERINDEP && python3 t9_sweep.py
```

**32 PASS, 0 FAIL** across `[[8,2,2]]` toric, `[[8,1,2]]` **non-manifold**, and `[[4,2,2]]` which is
not a lattice at all.

**Every row now says what carries it.** `T-9` was reopened by external review — it had been marked
DONE while satisfying neither branch of its own DONE_WHEN — and the audit was then run for real:
six probes over all 150 rows in scope, **defaulting every row to `SINGLE-CARRIER`**, with an
adversarial refuter required to confirm each `TWO-CARRIER` claim against the row's actual result on
structurally different carriers. Same model at another size or parameter set never counted.

```bash
cut -f1,2 LANE_T9_AUDIT/T9_carrier_audit.tsv        # the mark on every row
```

**`SINGLE-CARRIER` 113 · `TWO-CARRIER` 22 · `NOT-CARRIER-SHAPED` 15**, coverage 150/150. Rows
registered after the audit carry no mark and count as `UNAUDITED`, which is not a `TWO-CARRIER` mark.
The one `PROVED` row, `C-71`, is `TWO-CARRIER`. **`PROOF_V002.md` prints the mark beside
every row it cites, and `check_proof.py` refuses a claim that rests on a single carrier without
saying so.**

---

## HOW TO READ A NUMBER HONESTLY

This program has caught itself reporting artefacts as results more than once. Three rules were
adopted because of it, and every script follows them:

- **A zero is only a measurement if a POSITIVE CONTROL beside it would have registered a non-zero.**
  Look for the control before believing any zero.
- **A check that cannot fail is not a check** (`D-8`). `check(..., True)` is decoration; a fit with no
  noise floor beside it is decoration.
- **The ensemble average `Tr(Rρ)` is blind to record formation** (`D-6`). A fair coin has mean zero
  and every flip is definite. Negative verdicts warranted only by an expectation value are void.

---

## WHAT IS **NOT** ESTABLISHED

Stated here so you do not have to find it.

**Almost everything in this program is `FORMAL`** — real mathematics about the program's own
stipulated definition, saying nothing by itself about the world (`H-3`, `PARTIAL`). **Exactly one
row meets the `PROOF` bar: `C-71`**, naming its quantity in units, its predicted relation, its
falsifier on a standard instrument, and `RECORDS VERIFIED` on two structurally different
mechanisms. **Its surfaces are MODELLED** — constants pinned to literature classes, patterns from
sealed seeds — so what is scored is an encoding-level statement on two real *mechanisms*; **no device
was measured.** What is offered to you is the falsifier: a within-part Vt-distribution shift on a
flash tester. `ledger/status.py` enforces the two-surface requirement and nothing else; the other
three requirements are enforced by the registrar reading the row.

**Empirical contact is thin, and it is no longer zero.** Beyond that row it consists of `T-41`'s
pinned external anchors — published azobenzene half-life, the Weller–Moser magnetic stability rule,
NAND detrapping activation energy — placed beside the model's own numbers, sources in
`LANE_T41_EXTERNAL/CITATIONS.md`. **Everything else is the model against its own closed form.**

**Three ledger rows have not caught up with that**, and the honest thing is to say so rather than
quietly fix them: `X-4`, `T-VI.3` and `T-VI.4` are still `BLOCKED` with texts reading *"empirical
contact is zero"* and *"no distinguishing prediction"*. Both predate `T-41` and predate `C-84`, which
registered **three surviving distinguishing statements** after each candidate was attacked by three
rival advocates. Their external checks are owed. **The rows are flagged, not yet re-audited.**

**No claim here is that gravity has been derived.** `PROOF_V002.md` §6 makes the one comparison the
program permits and prints, in the same sentences, the three conditions of four that are not earned.
