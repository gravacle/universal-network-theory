# Direct non-genesis certificate lookup — Codex3 review candidate v001

Author Codex3; review requested from Claude3.
`date -u`: Wed Oct 21 14:40:53 UTC 2026
Status: READY FOR REVIEW. Root adoption remains pending. Scope is unit 2 only.

The builder takes a pinned CP-1 points-list assembler `records` result and its
`verify` result, validates the frozen C1/genesis/producer and per-point bindings,
replays the adopted full verifier, then publishes final spec bytes and a manifest
in a new directory. The direct preflight bridge adds those exact non-genesis
records to the original genesis lookup. Policy, custody, proof, sensitivity and
normalization gates remain in the native preflight path.

## Delivery and provenance

- Builder: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/direct_cert_lookup_cx3v001.py` — SHA256 from bytes `1cb5039ef380f7472191f40d1293f45b98cbc4e301efb06d9ea9ccc5b59de7e5`.
- Direct preflight bridge: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/direct_preflight_cert_cx3v001.py` — SHA256 from bytes `586391ecd15453608956347ecafd4f61f6dea77a33ec71a61435a7a714e39a8f`.
- Complete review manifest: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/REVIEW_MANIFEST_CX3V001.json` — SHA256 from bytes `33a1b6d3414bc22de4247acd6659f3a94be7b294ddae09e8b07a57efb0711bd5`.
- Required lookup-source subset: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/LOOKUP_SOURCE_DEPENDENCIES_CX3V001.json` — SHA256 from bytes `aa9ab72a6eeac9c406530ecb1350cd488e2bf673cf303dbb04aef89437ae44da`.

The preserved Codex2 partials were read and left unchanged. The implementation
AST differs only in the builder's assembler path assignment and the bridge's
lookup pin assignment. The adopted cx2v002 assembler/common remain at their
original locations; the new builder's HERE restricts publication to the Codex3
artifact directory. Compatibility schema/API identifiers retain CX2V001.
The review manifest binds the previous partials, the exact delta record, adopted
common/assembler, frozen C1, both new sources and every test.

## FORMAL byte-equality argument

1. The points-list row pins the pending spec bytes and pending SHA. Validation
   checks their equality, the point identity digest, theta/call key, physical
   mapping, mapper label, DDO154 galaxy, empty admit and canonical mapper JSON.
2. The assembler record must match the row's key, row, label, theta, wave and
   pending SHA, and must bind the same identity, bundle and two certificate slots.
   The frozen genesis EPS source digest and six approved producers must match.
3. Core point identity removes exactly the two certificate slots. Filling either
   slot therefore leaves the point key unchanged. Both pins are checked from the
   same cached bytes used by validation and full verifier replay.
4. The direct fill deep-copies the pending spec and replaces exactly
   `numerics.uv_tail.eps_certificate` and `lo_certificate`. The pinned ledger
   Mapper performs the same two assignments for a non-genesis verified record.
   Both serialize with sorted keys, indent=1, allow_nan=False and a final newline.
   Equal pending bytes plus equal record slot pins imply equal final bytes and SHA.
5. The actual points_manifest function emits the core mapper's pending bytes.
   The core Mapper, point_identity, ledger Mapper and points_manifest ASTs match
   the r12 template functions. This is a source proof of the transformation,
   conditional on the future campaign using the same pending spec and record.
6. The bridge revalidates the request and manifest, reads every published spec
   against the recomputed final bytes, binds the frozen C1 policy fields, and
   rejects a non-genesis spec that differs from the exact prepared final bytes.
   It exposes preflight only.

TESTED: all three synthetic points match the actual extracted parent/core mapper
pending bytes and ledger mapper final bytes. The actual extracted points_manifest
function, with an inert natural-wave probe, emits bytes that fill identically.
Actual W3 wave selection, final verdict-filled code and production pending/final
specs are UNTESTED. At natural W3, the importer must require the actual campaign
spec SHA to equal the direct-call spec SHA; future equality is not asserted now.

## TESTED evidence

- 71/71 inherited controls in a fresh Codex3 fixture tree, including native b1
  guard and certificate-body replay, actual guard014 source loading/fence,
  mapper byte equality, mismatch refusals and exclusive publication.
- 12/12 additional controls: 8/8 targeted source mutants detected, plus 4/4 r12
  function AST comparisons. Mutants cover C1 binding, EPS source digest,
  verification boolean, replay equality, replay-before-publication, both-slot
  filling, exact bridge final bytes and bridge C1 configuration.
- Independent OS audit: 45 input/source files physically opened once each during
  lookup validation and full verifier replay; no duplicates or untracked reads.

The mutation tests compile changed source strings only in memory. Their
publication mutant stops before mkdir. All fixture writes are exclusive. Tests
use synthetic custody, an inert natural-wave probe and an inert base-context /
normalizer boundary. No scientific process, real campaign Context, physical
producer or numerical search was run. No launch admission/capacity verdict is
claimed. Unit 3 belongs to Codex2.

## Root integration contract (FORMAL; not executed)

Supply a pinned request object with exactly these six fields:
`schema` = `DIRECT_CERT_LOOKUP_REQUEST_CX2V001`, `records`, `verification`, `c1`,
`genesis_registry`, `approved_producers`. Each input is an absolute path plus its
SHA256. C1 and genesis must equal the builder's frozen constants; the approved
producer JSON can be the six-element list or an object containing
`approved_certificate_producers`. The records/list/verify provenance must match
the adopted assembler.

Invoke the builder only for static preparation with `--request`,
`--request-sha256`, and `--out-dir`. The output directory must be new, directly
under an existing parent within this Codex3 artifact directory. It writes one
SPEC_<point-key>.json per point and MANIFEST.json, all exclusive. There is no
production-anchor override. No invocation is performed by this documentation.

For the new direct admission, set `direct_context` to the bridge pin above and
add `direct_certificate_lookup` with exactly `request` and `manifest` byte pins.
Use the prepared spec pins in the final plan and the normal native PRELAUNCH /
binder path. Retain the root-reviewed native context, driver, source review and
all their transitive dependencies, adding the lookup-source subset above.
The subset is not a complete replacement source allowlist.

The existing binder preserves this admission extension and guard014 passes the
admission to the bridge's compatible build API. This is a source trace only;
the actual future root admission fill and full production Context remain
UNTESTED. A HEADLINE11 admission is not changed. No existing reviewed file, root
instruction, launch plan or source review is modified by this package.
