# Mutable Stage-3 exact pretty-input compatibility candidate

Stage 2 has published the exact authenticated A18 cross-gate as owner-once
pretty JSON (`publication_json_bytes`).  The target L12 cache manifest uses
the same framing.  The frozen Stage-3 launcher retains and verifies the
correct file and parent identities but admits JSON only when raw bytes equal
the compact `canonical_json_bytes` representation.

This candidate changes only an explicit two-artifact registry: A18 and the
target L12 manifest, each at two exact call-site labels.  It first
uses the original launcher open in non-JSON mode, thereby preserving all of
the frozen descriptor, immutable-file, inode, parent, and hash custody.  It
then requires the pinned A18 SHA-256, strict ASCII JSON with duplicate and
non-finite rejection, exact Stage-2 publication serialization, and the frozen
production identity semantics.  A18 also passes the frozen A18 validator.
The hostile manifest and A20-A22 remain compact.  All other opens delegate
unchanged.  The global classmethod is restored in `finally`.

Before exposing any mode, the executable authenticates its sibling compact
`SOURCE_FREEZE.json`, the exact source/test/README member census and hashes,
and the complete previously frozen Stage-3 dependency packet.  Every member
must be an immutable ordinary single-link file reached through an ordinary
canonical repository path.

The exact command-line surface is:

```sh
python3 -B stage3_a18_framing_compatibility.py plan
python3 -B stage3_a18_framing_compatibility.py dry-run
python3 -B stage3_a18_framing_compatibility.py publish
python3 -B stage3_a18_framing_compatibility.py launch
python3 -B test_stage3_a18_framing_compatibility.py
```

Only `plan` has been invoked on the canonical tree for this mutable candidate.
No test or plan invocation publishes A20-A22, launches workers, or changes a
physical history.  Freeze and two independent same-hash hostile reviews are
required before the already-authorized production sequence can use `dry-run`,
`publish`, or `launch`.
