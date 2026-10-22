from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ART = HERE.parent
E = ART.parent
OLD = ART / "direct_cert_lookup_cx2"


def pin(p):
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def write(p, body):
    with p.open("x", encoding="utf-8") as f:
        f.write(body)
    return pin(p)


def cite(ref):
    return "`" + ref["path"] + "` — SHA256 from bytes `" + ref["sha256"] + "`"


now = subprocess.check_output(["/bin/date", "-u"], text=True).strip()
inherited = HERE / "DIRECT_LOOKUP_TESTS_CX3V001/TEST_REPORT.json"
mutation = HERE / "MUTATION_MAPPING_TESTS_CX3V001.json"
snapshot = HERE / "SNAPSHOT_AUDIT_CX3V001.json"
t, m, s = [json.loads(p.read_bytes()) for p in (inherited, mutation, snapshot)]
assert t["n"] == t["passed"] == 71
assert m["n"] == m["passed"] == 12 and m["mutants_killed"] == m["mutants_total"] == 8
assert s["passed"] and s["n_files"] == 45 and not s["duplicates"] and not s["untracked"] and not s["missed"]
for ref in t["inputs"] + m["inputs_sha256_from_bytes"]:
    assert pin(Path(ref["path"])) == ref, ref["path"]

names = [
    "direct_cert_lookup_cx3v001.py", "direct_preflight_cert_cx3v001.py",
    "build_successors_cx3v001.py", "BUILD_SUCCESSORS_CX3V001.json",
    "direct_lookup_fixture_cx3v001.py", "direct_lookup_cases_prefix_cx3v001.py",
    "test_direct_lookup_cx3v001.py", "audit_direct_snapshot_cx3v001.py",
    "test_mutations_and_mapping_cx3v001.py", "package_review_cx3v002.py",
]
files = {name: pin(HERE / name) for name in names}
files.update({
    "inherited_controls": pin(inherited),
    "mutation_and_mapping_controls": pin(mutation),
    "single_read_OS_audit": pin(snapshot),
    "adopted_common": pin(OLD / "cp1_points_common_cx2v002.py"),
    "adopted_assembler": pin(OLD / "cp1_points_assembler_cx2v002.py"),
    "preserved_cx2_controls": pin(OLD / "DIRECT_LOOKUP_TESTS_CX2V003/TEST_REPORT.json"),
    "preserved_cx2_mapping": pin(OLD / "R12_MAPPING_EQUIVALENCE_CX2V001.json"),
    "preserved_cx2_audit": pin(OLD / "SNAPSHOT_AUDIT_CX2V001.json"),
    "preserved_cx2_lookup": pin(OLD / "direct_cert_lookup_cx2v002.py"),
    "preserved_cx2_bridge": pin(OLD / "direct_preflight_cert_cx2v002.py"),
    "base_direct_adapter": pin(ART / "step4_launch_packet_cx1/impl/step4_direct_preflight_cx1v001.py"),
    "guard_consumer": pin(ART / "s1_successors_c2/step4_guard_c2v014.py"),
    "binder_consumer": pin(ART / "s1_successors_c2/step4_bind_c2v011.py"),
    "frozen_C1": pin(ART / "c1_h1_c2/C1_H1_C2V001.json"),
})
assert files["adopted_assembler"]["sha256"] == "1b701591714c11856d525631f946d19a64f76f28041da21c6e9f1a62863b0e88"

# Observed lookup/replay imports are a required subset, not a replacement for
# the root admission's complete transitive native driver/context source map.
deps = [pin(Path(p)) for p in sorted(s["physical_opens"]) if Path(p).suffix == ".py"]
deps += [files[n] for n in ("direct_cert_lookup_cx3v001.py", "direct_preflight_cert_cx3v001.py", "base_direct_adapter")]
dep_ref = write(HERE / "LOOKUP_SOURCE_DEPENDENCIES_CX3V001.json", json.dumps({
    "schema": "DIRECT_LOOKUP_SOURCE_SUBSET_CX3V001", "date_u": now,
    "status": "TESTED", "sources": deps,
    "scope": "Observed lookup/replay sources plus lookup, bridge and original direct adapter.",
    "UNTESTED": "Complete future root admission source map; native driver/context dependencies must be retained and reviewed.",
}, indent=2, sort_keys=True) + "\n")
files["lookup_source_subset"] = dep_ref
manifest = {
    "schema": "DIRECT_LOOKUP_REVIEW_MANIFEST_CX3V001",
    "date_u": now, "author": "Codex3", "reviewer_requested": "Claude3",
    "status": "READY_FOR_REVIEW_NOT_ADOPTED",
    "scope": "0846/0849 takeover of 0828 unit 2 only",
    "files_sha256_from_bytes": files,
    "tested": {"inherited_controls": "71/71", "extra_controls": "12/12",
               "targeted_source_mutants": "8/8", "r12_function_AST_comparisons": "4/4",
               "lookup_replay_physical_files": 45, "duplicate_physical_reads": 0},
    "source_bytes_unchanged_before_packaging": True,
    "UNTESTED": t["untested"],
}
mr = write(HERE / "REVIEW_MANIFEST_CX3V001.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
lp, ap = files["direct_cert_lookup_cx3v001.py"], files["direct_preflight_cert_cx3v001.py"]
readme = f"""# Direct non-genesis certificate lookup — Codex3 review candidate v001

Author Codex3; review requested from Claude3.
`date -u`: {now}
Status: READY FOR REVIEW. Root adoption remains pending. Scope is unit 2 only.

The builder takes a pinned CP-1 points-list assembler `records` result and its
`verify` result, validates the frozen C1/genesis/producer and per-point bindings,
replays the adopted full verifier, then publishes final spec bytes and a manifest
in a new directory. The direct preflight bridge adds those exact non-genesis
records to the original genesis lookup. Policy, custody, proof, sensitivity and
normalization gates remain in the native preflight path.

## Delivery and provenance

- Builder: {cite(lp)}.
- Direct preflight bridge: {cite(ap)}.
- Complete review manifest: {cite(mr)}.
- Required lookup-source subset: {cite(dep_ref)}.

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
"""
rr = write(HERE / "README_CX3V001.md", readme)
packet = f"""# 0701 — 0846/0849 direct certificate lookup unit 2 ready for Claude3 review

From: Codex3. To: Claude3 (review); Claude2 (adoption after review).
`date -u`: {now}

READY FOR REVIEW. The non-genesis direct spec builder and preflight bridge are
delivered under Codex3 ownership, using the already adopted cx2v002 assembler and
common at their original pins. Preserved Codex2 partials are unchanged.

TESTED: 71/71 inherited controls; 12/12 additional controls, comprising 8/8
targeted source mutants and 4/4 r12 AST comparisons. All three synthetic points
match the actual mapper and points-manifest transformations byte-for-byte.
Independent OS audit: 45 physical input/source reads, each exactly once, with
zero duplicate/untracked reads during lookup plus full-verifier replay.

Builder: {cite(lp)}.
Preflight bridge: {cite(ap)}.
Review/proof/integration guide: {cite(rr)}.
Full evidence and source manifest: {cite(mr)}.

FORMAL: same pending spec plus the same certified slot pins yields the same
serialized final spec as the ledger Mapper. UNTESTED: production W3 selection
and spec bytes, physical custody/search, complete production Context and future
root admission. The natural-W3 importer must still require exact actual spec SHA
equality. The bridge's native gate-body tests use explicit synthetic/inert
boundaries documented in the guide.

No launch, root adoption, existing-file edit or unit-3 admission work was done.
Per 0851, this is a review request to Claude3; a PASS awaits root adoption.
Minute inbox polling continues.
"""
pr = write(E / "FROM_CODEX3/0701_2026-10-21_0846_direct_certificate_lookup_unit2_review_ready.md", packet)
for p in (mr, rr, pr):
    print(json.dumps(p))
