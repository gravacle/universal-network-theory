# Native coordinate interface crosswalk 0401: erratum/addendum for 0402 (V001)

- Author role: author, Claude helper. A different helper must check this addendum (0402 l.8).
- Task 0402: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0402_2026-10-15_native_coordinate_counting_clarification.md` SHA256 `0cdc634718bd3eb67c7ec7d37956044b6fa1db680a80184b88d74fbeebbc3e85`
- Root review: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/NATIVE_COORDINATES0401_ROOT_REVIEW_V001.json` SHA256 `977878cea4d7cda1e686842b405f6ff53fb3c59b644e6b0ccff8585d824cf2c7` (status ACCEPTED_SCOPED_WITH_ROOT_COUNTING_QUALIFICATION_C1)
- Preserved unchanged (pins recomputed from bytes before writing; they match the root review custody list, l.7–23):
  - `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_coordinate_interface_0401/NATIVE_COORDINATE_INTERFACE_CROSSWALK_0401_V001.md` SHA256 `d0a45f1c2768134e27421c5b35abe6ddfd2c45e0dfe21af2bfa3669f3eb3a422`
  - `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_coordinate_interface_0401/SOURCE_CHECK_0401_V001.md` SHA256 `b6e36f4421e844039b035fd906947397cf2c1f6dc2ea439063d869ecff3918de`
  - `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE2/0108_2026-10-15_done-0401.md` SHA256 `2be35ceff231a32d9b4e5bb0c17247732eb2a4910f8d360d4f371efce72b6651`
- Lines cited: S3 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/OWNED_FIXED_PROFILE_OFFDIAGONAL_INDEPENDENCE_AND_TWELVE_COORDINATES_PROPOSED_V001.md` SHA256 `66d71e9c0a53b498b5e105796fc52656fcc7b7917d5ca88789f25018605645db`; S2 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/OWNED_UNIFORM_DIAGONAL_SEVEN_COORDINATE_OPERATOR_RANK_PROPOSED_V001.md` SHA256 `604cc21f716623786f7db3c9083d47c7299882befd3b76cff1dfa974c3745398`.
- Scope: documentary correction only. These four points qualify 0108 l.14 ("CONFIRMED, with no errata"). No code, numerical calculation, parameter or phase-profile choice, source hunt, or framework/physical adoption. This is not a galaxy-launch authorization. The proper-time question remains pending with the principal (0402 l.15; root `proper_time_proposal` NOT_ADOPTED_ANSWER_PENDING).

## Corrections

1. **Birth row** (crosswalk l.41; 0108 l.34). Replace `sum_c m_c [exp(i phi_eps) B_c + exp(-i phi_eps) B_c^dagger]` with `sum_c [exp(i phi_eps) B_c + exp(-i phi_eps) B_c^dagger]`, where c runs over primitive canonical Birth channels and m_c = 1.
   - Strike "× m_c" from the sign column, and strike the l.41 sentence defining m_c as a multiplicity of identical listed transitions.
   - Multiplicity arises automatically at a matrix entry when channels share its input and output (root C1, l.29: "Identical input/output matrix entries add through this sum").
   - An explicit m_gamma is allowed only after documented grouping of identical WHOLE maps, with each class enumerated once. Shared outputs alone do not establish map identity (0402 l.10; root C1).
   - S3 l.19 states a matrix-element multiplicity ("Its matrix element is epsilon times a positive integer channel multiplicity…"). It is not an extra multiplier on each enumerated primitive channel.
   - The m_c part of open item crosswalk l.117 / 0108 l.80 is closed by this point.

2. **Formal chart derivative** (crosswalk l.28 column head and l.54 block A; 0108 l.20, l.44). "Holding the other coordinates and C fixed" denotes a formal derivative in the affine chart.
   - An actual raw-parameter change follows the displayed chain rule (block B: crosswalk l.58–78; 0108 l.46–58).
   - That change includes the identity, source and preparation changes it induces (0402 l.11; root C2, l.33).
   - Vanishing second coordinate derivatives do not remove physical contacts (root C2; already stated at crosswalk l.98).

3. **Ice wording.** Withdraw 0108 l.68: "That excludes ice, local ground, local Q_i=1, r=0, a single N".
   - The full preparation-sector chart is not restricted to strict ice, and it does not exclude strict-ice states (0402 l.12; root C4, l.41).
   - Root C4 extends this to local grounds and to "other restricted states". S2 l.14 lists all five restrictions named in 0108 l.68 as restrictions the sector is "NOT restricted to".
   - Restricting to strict ice changes the rank claim. On strict ice D=S=P_s=Q_s=0, and at fixed N the nu term is an identity (S2 l.40). What fails under restriction is the full operator-rank claim, not those states' membership in the sector (root C4).
   - The crosswalk does not contain "not ice" or "excludes ice". Its l.94 wording ("It is not restricted to ice, local grounds, local Q_i=1, r=0 or a single N") matches S2 l.14 and stands, with "ice" read as strict ice (S2 l.40; checker N2).
   - The rest of 0108 l.68 (nonuniform profiles, graph-I cells, other Q−M sectors, other donor laws) is unaffected.

4. **Bounded open items** (crosswalk l.112–123; 0108 l.79–84). These items are unresolved only within the bounded 0401 read set. They are not new program gaps.
   - 0400 already recovers the zero-phase hopping and Bind definitions (0402 l.13; root C3, l.37).
   - No new source hunt and no phase-profile choice follows from them.
   - Root C3 adds three points:
     - Hermitian reverse phases must be conjugate when such a profile is used.
     - No physical hopping profile is selected.
     - Current primitive owners and guards apply; the separating-transition witnesses are not a replacement implementation.
   - 0400 itself was not opened for this addendum.

**Recorded, not resolved.**
- (a) S3 l.19 does not state the whole-map grouping rule or the shared-output caveat. Those come from 0402 l.10 and root C1. S3 adds that the canonical convention "ordinarily gives one".
- (b) Root C2 also lists "phase/profile" among the induced changes; 0402 l.11 does not.
- (c) 0402 l.12 names only strict ice, while root C4 also names local grounds and other restricted states.
- (d) The task asked for "'not ice' / 'excludes ice'" to be quoted from both the 0401 file and 0108. The excluding phrase occurs only in 0108 (l.68). SOURCE_CHECK l.161 quotes crosswalk l.94 correctly.
