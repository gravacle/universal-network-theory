# Erratum check 0402 (V001)

- Role: distinct checker, not author. I did not write the 0401 crosswalk, its source check, the 0108 return or the 0402 erratum.
- Checked file: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_coordinate_interface_0401/NATIVE_COORDINATE_INTERFACE_CROSSWALK_0401_ERRATUM_0402_V001.md` SHA256 `aad7ba85bbcf581b40f7efc6c7cbfd72f44901f06d9c2edda05a0677f1641cb6` (6251 bytes), recomputed from bytes; it matches the author report.
- Scope: this addendum only (0402 l.8). The full 0401 source review is not repeated.
- Read-only throughout. No code, numerical calculation, network, calibration/target data, parameter or phase-profile choice, source hunt, or framework/physical adoption. 0400 was not opened, and no link in the root review was followed.
- This is not a galaxy-launch authorization. The proper-time question remains pending with the principal (0402 l.15; root `proper_time_proposal` NOT_ADOPTED_ANSWER_PENDING).

## Pins (recomputed from bytes before reading; all match)

- 0402 `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0402_2026-10-15_native_coordinate_counting_clarification.md` SHA256 `0cdc634718bd3eb67c7ec7d37956044b6fa1db680a80184b88d74fbeebbc3e85`
- Root review `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NATIVE_COORDINATES0401_ROOT_REVIEW_V001.json` SHA256 `977878cea4d7cda1e686842b405f6ff53fb3c59b644e6b0ccff8585d824cf2c7`
- 0401 crosswalk `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_coordinate_interface_0401/NATIVE_COORDINATE_INTERFACE_CROSSWALK_0401_V001.md` SHA256 `d0a45f1c2768134e27421c5b35abe6ddfd2c45e0dfe21af2bfa3669f3eb3a422` (16338 bytes)
- 0401 source check `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_coordinate_interface_0401/SOURCE_CHECK_0401_V001.md` SHA256 `b6e36f4421e844039b035fd906947397cf2c1f6dc2ea439063d869ecff3918de` (14769 bytes)
- S3 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/OWNED_FIXED_PROFILE_OFFDIAGONAL_INDEPENDENCE_AND_TWELVE_COORDINATES_PROPOSED_V001.md` SHA256 `66d71e9c0a53b498b5e105796fc52656fcc7b7917d5ca88789f25018605645db`
- S2 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/OWNED_UNIFORM_DIAGONAL_SEVEN_COORDINATE_OPERATOR_RANK_PROPOSED_V001.md` SHA256 `604cc21f716623786f7db3c9083d47c7299882befd3b76cff1dfa974c3745398`
- 0108 `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE2/0108_2026-10-15_done-0401.md` SHA256 `2be35ceff231a32d9b4e5bb0c17247732eb2a4910f8d360d4f371efce72b6651` (6355 bytes)

The two 0401 files and 0108 are unchanged. Their hashes and byte counts equal the root custody list (root l.9–21).

## Verdict

**CONFIRMED_WITH_CORRECTIONS.**
- Items 1, 3 and 4 match 0402 and the root review with no weakening and no extra claim.
- Two reading-level corrections:
  - K1: item 2 drops root C2's "phase/profile".
  - K2: recorded item (d) attributes a request to "the task", which 0402 does not contain.
- The erratum stands when read with K1 and K2.
- Nothing in it adopts physics, chooses a parameter or phase profile, or authorizes a launch.

## Per-item results

### Item 1: Birth row. PASS

- **Original wording (quoted).**
  - Crosswalk l.41 has the operator `Σ_c m_c·[e^{i·phi_eps}·B_c + e^{−i·phi_eps}·B_c†]`, the sign cell "+ (× phase × m_c)" and the sentence "m_c is a positive integer multiplicity of identical listed transitions".
  - 0108 l.34 has `Σ_c m_c [e^{iφε} B_c + e^{−iφε} B_c†]` with sign "+".
  - Erratum l.15–16 strikes all three m_c parts. Its "Replace" expression is an ASCII transliteration of these lines: the location and content match, but it is not a byte-verbatim quote.
- **Replacement formula.**
  - Erratum: `sum_c [exp(i phi_eps) B_c + exp(-i phi_eps) B_c^dagger]`, with c over primitive canonical Birth channels and m_c = 1.
  - 0402 l.10: "sum_c [exp(i phi) B_c + exp(-i phi) B_c dagger], with m_c=1".
  - Root C1 (l.29): "sum_c [exp(i phi) B_c + exp(-i phi) B_c^dagger], with no extra multiplicity: m_c=1".
  - The three agree. PASS.
- **Matrix-entry multiplicity.** Erratum l.17 matches 0402 l.10: "Multiplicity arises automatically at a matrix entry when channels share its input/output". The quote "Identical input/output matrix entries add through this sum" is verbatim at root l.29. PASS.
- **m_gamma.**
  - Erratum l.18: "allowed only after documented grouping of identical WHOLE maps, with each class enumerated once. Shared outputs alone do not establish map identity."
  - 0402 l.10 says the same.
  - Root C1: "documented equivalence classes of identical whole channel maps exactly once. Sharing selected outputs does not make whole maps identical."
  - PASS.
- **S3 (lines opened).** S3 l.19 reads: "Its matrix element is epsilon times a positive integer channel multiplicity if there is more than one identical listed transition; the canonical identical-source cut/slot convention ordinarily gives one."
  - The erratum quote (l.19) is verbatim, truncated with an ellipsis.
  - Its reading (a matrix-element multiplicity, not an extra multiplier on each primitive channel) is the 0402 l.10 sentence.
  - PASS.
- **Closing the m_c open item.** Erratum l.20 closes the m_c part of crosswalk l.117 and 0108 l.80. This follows directly from root C1's m_c=1 under primitive enumeration, so it is not an extra claim. The channel-list part of those items stays a bounded item under item 4.

### Item 2: Formal chart derivative. PASS with correction K1

- **Locations are correct.**
  - Crosswalk l.28 column head: "(= ∂H/∂coordinate, with the other eleven, C and the fixed phases/profile held fixed)".
  - Crosswalk l.54: "(A) Reparameterized coordinates held fixed".
  - 0108 l.20 and l.44.
  - Block B: crosswalk l.58–78 and 0108 l.46–58.
- **Formal derivative.** The erratum's "formal derivative in the affine chart" matches 0402 l.11 ("formal affine-chart derivative") and root C2 ("formal affine Hamiltonian chart"). PASS.
- **Chain rule and second derivatives.**
  - "follows the displayed chain rule" matches 0402 l.11.
  - The second-derivative sentence matches root C2 ("Vanishing second coordinate derivatives do not remove physical contacts").
  - Crosswalk l.98 does already state it: "That does NOT eliminate physical-source, nonlinear-coefficient, preparation or metric contacts."
  - PASS.
- **K1 (correction).**
  - Erratum l.24 lists "the identity, source and preparation changes it induces" and cites "root C2, l.33".
  - Root C2 reads: "A physical raw-parameter variation follows its actual Jacobian, induced common identity, phase/profile, source and preparation changes."
  - The cited root list includes phase/profile, and the erratum's list drops it.
  - 0402 l.11 ("including identity/source/preparation changes") is a non-exhaustive "including" and does not conflict with root C2. Recorded item (b) therefore records a difference that needs no resolution.
  - Correction: read erratum l.24 with root C2's full wording. A physical raw-parameter variation follows its actual Jacobian, including the induced common-identity, phase/profile, source and preparation changes.
  - This chooses no phase or profile. It says only that a raw variation may move them.

### Item 3: Ice wording. PASS

- **Original wording locations (quoted).**
  - 0108 l.68: "That excludes ice, local ground, local Q_i=1, r=0, a single N, nonuniform profiles, graph-I cells, other Q−M sectors and other donor laws."
    - Erratum l.27 withdraws the first five items, quoted as a prefix.
    - Erratum l.32 states that the remaining four are unaffected. This matches crosswalk l.94: "does not extend unchanged to nonuniform profiles, graph I cells, another Q−M sector or other donor/slot invariants".
  - Crosswalk l.94: "It is not restricted to ice, local grounds, local Q_i=1, r=0 or a single N (S2 l.14; S3 l.7)." The same line also has "on ice D, S, P_s and Q_s vanish".
  - Grep: the crosswalk contains neither "not ice" nor "excludes ice". Among the 0401 files, "excludes ice" occurs only at 0108 l.68. SOURCE_CHECK l.161 quotes crosswalk l.94 correctly.
- **Restatement.**
  - 0402 l.12: "not restricted to strict ice, but does not exclude strict-ice states".
  - Root C4 (l.41): "contains strict-ice and other restricted states; it is not restricted to them" and "must not be read as removing those states".
  - The erratum carries the root's broader version (local grounds, "other restricted states"). PASS.
- **S2 l.14 (opened):** "It is NOT restricted to ice, local grounds, local Q_i=1, r=0 or a single N." Its five items are the five withdrawn. PASS.
- **S2 l.40 (opened):** "on strict ice, D=S=P_s=Q_s=0; at fixed N the nu term is also an identity."
  - Erratum l.30 matches.
  - The root C4 sentence "What fails under restriction is the full operator-rank claim, not their membership in the preparation sector" also matches l.30.
  - PASS.
- **Checker N2.** Checker N2 is at SOURCE_CHECK l.177 ("Author l.94 says "on ice" where S2 l.40 says "on strict ice"") and at 0108 l.76. The erratum cites it correctly.

### Item 4: Bounded open items. PASS

- Locations are correct: crosswalk l.112–123 and 0108 l.79–84.
- The text matches 0402 l.13 and root C3 (l.37): "Unresolved items in the bounded0401 read set are not program-wide absences.0400 already recovers zero-phase hopping and Bind definitions."
- The three root C3 additions (conjugate Hermitian reverse phases, no physical hopping profile selected, current primitive owners and guards rather than witnesses) are transcribed without change of meaning.
- No source hunt and no phase-profile choice. 0400 is stated as not opened.
- The erratum does not claim that root C3's conjugate-reverse-phase sentence closes crosswalk l.115. No extra claim.

### Recorded items (a)–(d)

- (a) True: S3 l.19 has no whole-map grouping rule and no shared-output caveat. This is a provenance note, not a gap.
- (b) See K1. No conflict exists; read root C2 as governing.
- (c) True. Item 3 already carries root C4's broader text, so nothing remains.
- (d) The substance is verified by grep (see item 3).
  - **K2 (correction).** The erratum says: "The task asked for "'not ice' / 'excludes ice'" to be quoted from both the 0401 file and 0108."
  - The only task pinned in the erratum is 0402 (erratum l.4). 0402 contains no such request; its only ice phrase is "'excludes ice'" at l.12. The request came from an unpinned dispatch brief.
  - Correction: read "the task" in (d) as the author's dispatch brief, not 0402.
- None of (a)–(d) is a new program gap, and none implies a source hunt or a phase choice.

## Citation audit

Each cited line was opened and found accurate:
- 0402: l.8, l.10, l.11, l.12, l.13, l.15.
- Root review: custody l.7–23; C1 l.29, C2 l.33, C3 l.37, C4 l.41; status l.2; proper_time_proposal l.55.
- S3 l.19.
- S2 l.14 and l.40.
- Crosswalk: l.28, l.41, l.54, l.58–78, l.94, l.98, l.112–123, l.117.
- SOURCE_CHECK l.161 and l.177 (N2).
- 0108: l.14, l.20, l.34, l.44, l.46–58, l.68, l.76, l.79–84, l.80.

The only misattribution is K2.

## Scope scan

- Erratum l.11 states the scope as documentary only: "No code, numerical calculation, parameter or phase-profile choice, source hunt, or framework/physical adoption. This is not a galaxy-launch authorization."
- Erratum l.36 and l.39 repeat that there is no hunt and no profile selection.
- The value m_c=1 is root C1's counting convention under primitive enumeration, not a parameter choice. No phase is set to zero.
- PASS.

## Not verifiable by this checker (author attestations)

- That the erratum was written by exclusive create.
- That nothing was written under Universal Network Theory.
- That 0400 was not opened.

## Custody

- This file was created by exclusive create (`set -o noclobber`) in `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_coordinate_interface_0401/`.
- Files opened: the erratum, 0402, the root review, the crosswalk, 0108, S3 l.1–30, S2 l.12–16 and l.38–42, and SOURCE_CHECK l.155–180 plus a grep.
- Only shasum, wc, cat, sed, awk and grep were used for reading.
- No existing file was overwritten, moved, deleted or chmodded.
