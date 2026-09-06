# Hostile audit report — connected trajectory L4--L14 V001

## Verdict

**PASS after a bounded label repair, with no numerical discrepancy.** The
repaired target passes `18/18`. The independent append reconstruction passes
`31/31`. The target is eligible to append one finite L14 row and one finite
L12-to-L14 comparator to the sealed L4--L12 trajectory under the stated claim
ceilings.

Before sealing, this audit found that the structured `not_claimed` field
omitted `TREND` and named only `CRITICAL_PHASE` rather than generic `PHASE`.
It also found the README phrase “byte-for-byte as parsed data,” which blurred
serialized-byte identity with parsed-data equality. The target author changed
only those labels: the result/compiler now explicitly withhold `TREND` and
`PHASE`, and the README says “exactly as parsed data.” The numerical rows,
comparators, formulas, and theorem were unchanged. This audit pins and tests
the repaired packet.

## Custody and exact prefix preservation

The sealed L4--L12 result hash is
`8fe9697c833542812bbda78ea5528265b048d1775ace43a7203e1c583c7b5759`.
The sealed L14 target result hash is
`e8134d5311b9bdfd62ce7df5988da803b110516606ce905a1bc49bd65cdb5fbe`;
the L14 hostile summary and detailed-result hashes are respectively
`cf4301e55f0c911196ecfbd2f02d60ebcfc32def3353472dccb87077ca77d204`
and `bfa8fd0eb4ff793662af546408882b84ba55ec0ff38145263d8c9747660919be`.
The L14 hostile verifier was separately replayed at `56/56`.

The independently canonicalized five-row prefix has SHA-256
`936072342c26b649efce4027a8924d9d51b12650834904256fae0ed2b202d2f6`.
The four-comparator prefix has SHA-256
`8c92d99f535ee3956325cde97c5d09add7aea1e93f90fff4d7352f40276ed334`.
Both target prefixes equal the sealed base objects exactly as parsed; their
order remains L4/L6/L8/L10/L12 and L4-to-L6/L6-to-L8/L8-to-L10/L10-to-L12.

The repaired target packet hashes are:

- README: `c0ab043df521d60bbcc4e4bc643ed0234e1a194528a1cb6544703061d8acfc61`;
- result: `8a69f780a372ae436ef2fe458af80f7fa1ba70d8c93b21d91524c6e9819d753d`;
- theorem: `8d95a25f5c1cefc45a8825b06686fddac68295708753b481eadd5a6abddfd34f`;
- compiler: `a9dde10bf870a9b85d9db3bfea4ae5c42d276416d228f93d1306956ac08b0e46`.

## Independent append arithmetic

Without importing the target compiler, the audit rebuilt the L14 row directly
from the sealed L14 result. It obtains 2,744 sites, 1,372 prepared lineages,
98 connected components, 4,116 owner-once edges, and retained expectation
`685.9999999999512`. All 28 internal and 14 connector edges per component are
active.

The independently recomputed target-row observables are:

- internal and connector current magnitudes
  `0.08828506938410692` and `0.08407720521733116`;
- global total and connector throughputs
  `357.60815594816773` and `115.35392555817833`;
- per-retained total and connector throughputs
  `0.5212946879711271` and `0.16815441043467425`;
- even and odd occupation means
  `0.2606473439791989` and `0.23935265602076553`;
- maximum absolute connected-edge correlation `0.03604917681151288`;
- raw record-ledger residual L1/Linf per component
  `1.7719237188629222e-10`/`6.346090319908626e-12`, with global L1 bound
  `1.7364852444856638e-08`.

The independent L12-to-L14 comparator is:

| Quantity | Value |
|---|---:|
| site ratio | `1.587962962962963` |
| retained ratio | `1.587962962962858` |
| total throughput ratio | `1.5879626768798294` |
| total throughput per-retained ratio | `0.9999998198427575` |
| connector throughput ratio | `1.5879628845789442` |
| connector throughput per-retained ratio | `0.9999999506387015` |

The reconstructed row and comparator equal the target append exactly. The
complete reconstructed result, including metadata and ceilings, canonicalizes
to SHA-256
`5c6ea295492ed04c59e36a05753834c66b22c6c3d14345bdf223bbf89dda69bf`
and equals the target result as parsed.

## L14 audit use and claim ceiling

The trajectory correctly uses the canonical L14 target values. It does not
substitute the separate hostile RK4 values. The sealed L14 audit passes
`29/29` and reproduces all target currents within `1.898e-11` and all target
comparator fields within `9.713e-9`; its pinned packet verifier passes `56/56`.

The six residual rows remain raw unassigned numerical record-ledger terms and
are not called defects. No residual is a fit input. The appended comparator is
one finite comparison only. It establishes no monotonicity, trend,
convergence, limit, exponent, fit, scaling law, autonomous support, physical
grid, continuum behavior, Ward identity, phase, graviton, or gravity.
