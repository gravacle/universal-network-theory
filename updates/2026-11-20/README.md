# UNT puzzle program: progress update, 2026-11-20

This folder is a curated snapshot of the Universal Network Theory (UNT) "puzzle
program" as of 2026-11-20 (about 13:00 UTC). It is a progress record, not a
release and not a claim of completion. **No card is fully green yet.**

## Who is working on it

- **The principal** owns the research program, sets goals and answers definition
  questions about what UNT means.
- **Claude2** is the coordinator lane. Since 2026-11-19 it also takes its own
  clear recommended answers on pending definitions, under an explicit
  delegation from the principal (see `decisions/`). Each such decision is
  marked "coordinator, under principal delegation" and is reversible.
- **Claude3** keeps the one puzzle map (the scoreboard) and governs the card
  grades. Claude3 was out of credits for part of 2026-11-20; Claude2 and Claude1
  picked up its in-flight checks, chairs and referee work.
- **Claude1** hosts work batches (on 2026-11-20, batch 26 "what a Birth builds").
- **Codex2** (a GPT-family model running in Codex) acts as the **second model
  family**: it re-checks results produced by the Claude lanes, with its own code.

## The goal

"From records to atoms": starting from a stated, simple early state of the
network (allowed as an initial condition), show that UNT's own rules produce
the features of the physical world, up to atom-like composites and the
hydrogen 1/n^2 level pattern. Every extra term or assumption needed along the
way is listed openly (decision PD-01A).

**Alpha** (the strength of electric attraction, about 1/137) is treated as a
**landed setting**: UNT should supply the allowed range and a
setting-to-alpha map; the measured value picks our universe's setting and is
never claimed as derived (PD-02, PD-03).

## How cards are graded

Each physical feature is a "card". A card is graded on six criteria:

1. derived (follows from UNT's rules);
2. not put in by hand;
3. stable under UNT's native moves;
4. predicted before it was compared with nature;
5. independently checked by a second model family;
6. scoped (it says exactly what it does and does not cover).

Statuses, from strongest to weakest:

| status | meaning |
|---|---|
| Placed | meets all six criteria (the only green status) |
| Placed, if a rule change is adopted | would be placed, but needs a rule change that is not adopted |
| Placed, awaiting independent check | meets everything except the second-model-family check |
| PATH EXISTS | a concrete route is shown (often on a supplied block), with named missing steps |
| OPEN | no route shown yet |
| AGAINST | the evidence argues against the card as currently set up |

**"One model family" caveat.** Almost all results were produced and checked by
Claude models. A card turns green only after a second model family confirms
it. Codex2 started second-family checks on 2026-11-20 (results below), but the
map owner has not yet regraded any card with them. Until then, every grade
below is a one-model-family grade.

## Card status

Grades as Claude3 last wrote them (scoreboard as of 2026-11-20T00:13:56Z;
counts: 5 PATH EXISTS, 10 OPEN, 0 placed, 0 against), with the coordinator's
notes on what changed today. Criteria columns use the order above
(Y = met, - = not met).

| card | status | criteria 1-6 | note |
|---|---|---|---|
| fermion sign and exclusion | PATH EXISTS | `- - - Y Y Y` | Sign pattern counted as a landed setting; showing that UNT particles on it behave as fermions is still open. |
| spin-1/2 | OPEN | `- - - - - -` | A pairing headline was REFUTED today (sign error); exchange sign is the shared gap with shells and exclusion (PD-53). |
| shells of 2n^2 | OPEN | `- - - - - -` | Still n^2 per shell, exactly half of 2n^2. |
| opposite unit charges | PATH EXISTS | `Y Y - - Y Y` | Same charge unit across written and unwritten backgrounds confirmed by two families (fixed background labels). |
| charge thirds | OPEN | `- - - - - -` | Sharp thirds on a supplied three-way pattern recorded as a clue only (PD-57). |
| alpha allowed range and its setting | OPEN | `- - - - - -` | Alpha stays a setting; no native price found yet that would give the allowed range. |
| light (a photon-like field) | PATH EXISTS | `- - - - - -` | On a supplied 3D block; the wave itself is not yet shown. |
| hydrogen 1/n^2 levels | OPEN, **recommended to PATH EXISTS (PD-55), pending the map owner's regrade** | `- - - - - -` | Direct one-over-distance pull measured on a supplied 3D block (details below). |
| three-body nuclear binding | OPEN | `- - - - - -` | So far a contact effect only. |
| a persistent atom-like composite | OPEN | `- - - - - -` | A contact bond holds, but nothing yet makes a group last. |
| three dimensions | OPEN | `- - - - - -` | No grown network reads three-dimensional on both rulers (many routes closed today). |
| one limiting speed | PATH EXISTS | `- - - - - -` | A limit on lasting motion on a supplied block; locking check confirmed today. |
| gravity | OPEN | `- - - - - -` | Grown material does not settle into the thin state where the pull would work. |
| an arrow of time | PATH EXISTS | `- Y - - - -` | Principal decision PD-42: growth is the arrow (PD-42A: net growth; formed records never undone). |
| dark energy | OPEN | `- - - - - -` | Referee ruled AGAINST on the current clock (PD-37); principal chose to test first (PD-43) before any clock change. |

Settings counted openly as inputs (not derived): the fermion sign pattern,
alpha, and the stated early state.

## Key results of the last two days

### 2026-11-19

- First card movement of the program: the **arrow of time** moved to PATH
  EXISTS; later **light** and **one limiting speed** moved to PATH EXISTS, both
  on a supplied three-dimensional block (not a grown one).
- The principal answered more than twenty definition questions (PD-07A to PD-34):
  for example one heir per Birth, gamma as the released carrier, light as a
  wave in the links, charge as a site off its surroundings' normal link count.
- The principal delegated clear recommended answers to the coordinator
  (PD-35 onward are mostly coordinator decisions; most are "test first" and
  adopt nothing).

### 2026-11-20

Positive or partly positive:

- **Hydrogen.** On a supplied 3D block the pull between two opposite charges
  was measured directly, twice, with separate code: it follows one over
  distance at about 0.85 +- 0.10 of the expected strength (R^2 0.992). The
  batch-22 chair recommended moving the card to PATH EXISTS; the coordinator
  recorded that recommendation as PD-55 for Claude3 to apply. The named missing
  step is the pull at the atom's own size. A bounded ground-state follow-up
  (seat HB) found a positive square-law cost of steady flow on 512 sites, but
  larger blocks failed their gates; HB is **unchecked**.
- **Second model family started.** Codex2 (GPT family) checked seven results
  (charge unit, arrow of time, gravity relaxation, locking, live-link ruler,
  seam census, scale). All seven came back CONFIRMED_WITH_CORRECTIONS, and
  Codex2 reproduced a headline growth run with its own code for five of them.
  These checks are not yet folded into the grades.
- **Opposite charges.** The same unit of charge holds against both backgrounds,
  confirmed by both model families, as long as background labels stay fixed.

Negative results and refutations:

- **Spin pairing: REFUTED.** A pairing headline used ring trades with the wrong
  sign. With the sign corrected, a 12-site stand-in shows an exact paired lowest
  level, but on a faithful 96-site block the degeneracy comes from the
  surroundings, not from the signs. No card moves.
- **Exchange sign.** An exact negative from batch 26: with every existing
  setting, nothing that moves on a fixed network swaps with a minus sign. A
  minus sign for carriers would need a rule change.
- **Dark energy: AGAINST on today's clock.** If elapsed time is the count of
  record-events over the whole network (PD-37), expansion cannot keep speeding
  up in a three-dimensional network. A proposed local clock turned out to be
  close to a tautology (it is the logarithm of the global count). The
  principal chose to test first (PD-43) rather than change the clock.
- **Three dimensions.** Many routes were closed: undo at the growing tips
  changes nothing; locking small pieces leaves no live 3D part; handed-down
  region labels add about zero stretch; seam-crossing cut preferences fail;
  "about 2" is not forced by what a Birth builds (looser cuts raise the reading
  but make the network too dense); grown bodies follow "whole = one layer + 1"
  with layers reading only about 1.2 to 1.9; the slab-thickness test's kill
  fired (PD-63 parks it). No grown network reads three-dimensional on both
  rulers.
- **Gravity.** Grown material still does not settle into the thin, mostly
  unwritten state where the pull would follow space; the card stays OPEN.
- **Records as charges.** Grown records behave like lone charges, not
  dipole-free groups as an atom would need; whether that is a real clash is
  undecided until a body reads three-dimensional.
- An "ice model" insight for alpha turned out to be already on file; it is
  not new.

Process notes: three work seats were stopped by an API safeguard because of
how their prompts were worded; the prompts were corrected and the seats
relaunched (no results from them yet). Some insight notes in `results/` come
from seats still in progress and are informal.

### In progress

- A comparison of UNT with Chain Theory is in progress. No Chain Theory
  material is included in this update.
- Claude3's regrade of the map with today's checks (including PD-55).
- Second-family checks of the hydrogen pull and other batch-22 results (Codex2).

## What is in this folder

| path | contents |
|---|---|
| `README.md` | this note |
| `BOARD.html` | the puzzle board as shown to the principal (static copy; auto-refresh removed) |
| `decisions/` | every principal decision record (PD-01 to PD-64) and the delegation record; `DECISIONS_INDEX.md` lists them |
| `results/` | today's seat, check, chair and referee files, and Codex2's second-family checks; `RESULTS_INDEX.md` gives path, sha256, verdict and a plain summary |
| `MANIFEST_SHA256.txt` | sha256 of every file in this folder |

Files keep the absolute working paths they were written with; those paths
refer to the authors' working tree and are not needed to read the results.
