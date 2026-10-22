# ADDENDUM CHECK 0399 V001: USAGE_CONTRACT_0397_V002 range addendum

Role: distinct checker, not author. I did not write the addendum, either V002 review, V002 code or either contract. Date 2026-10-15. Scope: the range addendum (0399 last paragraph) only; the 0399 source map is not checked here.

## Verdict: CONFIRMED_WITH_CORRECTIONS

The addendum is one paragraph, makes every required statement, traces each technical claim to a cited review finding and to v002 code lines, and makes no overclaim. One LOW attribution correction (C1) is recorded here because exclusive create forbids rewriting the addendum. Seven INFO notes; none changes the substance.

## Hashes (sha256 computed from bytes with `shasum -a 256`)

| File (claude_artifacts/scalar_metric_solve_0397/ unless noted) | sha256 | Expected | Match |
|---|---|---|---|
| USAGE_CONTRACT_0397_V002_RANGE_ADDENDUM_V001.md | f286b0d88bce27384281953995714c71d7502091838c549a19f768f3dd8e05cb | author report | yes |
| REVIEW_0397_V002_SOURCE_DELTA.md | 5df6d6966c4b8c72ca2e1b71d90a9a53763814d57b6e10494a1bf394c5e89eda | brief; addendum L5 | yes |
| REVIEW_0397_V002_ADVERSARIAL.md | 3b086bcf00984afb781095d588307ec6c81c2c66ed091108c2c5304c5d56ea6b | brief; addendum L5 | yes |
| USAGE_CONTRACT_0397_V002.md | e8f8f4fbb75b718e7df09d593d7893c70b1342cea1c59e03fb1df985bf1852b9 | brief; addendum L3 | yes (unchanged) |
| scalar_metric_particular_solve_v002.py | ef767fd79f60852e23ec0de29b04737cf4acfacca3461d83f5b3d01413abaecf | brief; addendum L2 | yes (unchanged) |
| scalar_metric_particular_solve_v001.py | c7dbbba8ccb5bff025cf874410d769e96b7757b214d77d7f7f2fbf8c420dc0db | brief | yes (unchanged) |
| USAGE_CONTRACT_0397_V001.md | e8ffbf92fd6b0a68568929f07552bf3715318f4c659b151236236f681bc2afbf | brief | yes (unchanged) |
| REVIEW_0397_V001.md | 8da4c9c2f2a5b0379602645aa8a54571d26e8573d0fbc576d8035216a7147f68 | source-delta L18 | yes (unchanged) |
| AUTHOR_NOTES_0397_V001.md | d51f0ad9070a310888aa741e7092d02e46cb897d2882bed74763350b6158cc60 | source-delta L20 | yes (unchanged) |
| AUTHOR_DELTA_0397_V002.md | d5a66103777af47e3185ce5f77bc7b17e87ad9f4f13aad44037e7acb9bbdecb8 | source-delta L23 | yes (unchanged) |
| FROM_CODEX/0399_2026-10-15_native_energy_owner_support_source_map.md | e92722fc326ffa12a29304991d16251501a0439c696d0821a4b389f63e25b070 | read as data | n/a |

Mismatches: none. Directory listing: the addendum (20:20:23) is the only file newer than the reviews (19:55, 20:01); every earlier file keeps its pre-review mtime; no new code file, `__pycache__` or `.pyc`.

## Required-item checks

| Item | Result | Where |
|---|---|---|
| One paragraph | yes | prose is the single paragraph at L5, after a heading line (L1) and two hash pin lines (L2–L3) (I5) |
| Finite admission is not all-scale reliability | yes | L5: "Finite admission does not mean the module is reliable at every scale." |
| Norm underflow | yes | L5 (i) |
| K0 underflow giving the k = 0 operator | yes | L5 (ii) |
| Non-escalated prefactor overflow | yes | L5 (iii) |
| Root controls: ordinary magnitudes and fatal warnings | yes | L5, matching 0399 last paragraph ("The root reviewed controls use ordinary magnitudes and fatal warnings.") |
| No code change or new case | yes | L1 and L5 final sentence; no new code file in the directory |
| No existing file modified | yes | all hashes above match |
| No overclaim | yes | no all-scale safety, no "fixed", no physical or prediction claim; "V002 therefore stays qualified to its tested scope" matches 0399 |

## Claim trace (review finding; v002 code lines, read as text)

| Addendum claim | Review finding | Code |
|---|---|---|
| (i) norms lose precision below ~1.5e-154, square to 0 below ~1.6e-162 | source-delta N1 (L104); adversarial N3 (L41) | `_vector_norm` L120–122 (sum of v.real² + v.imag², then sqrt) |
| nonzero residual gives residual_norm 0.0 and relative_residual_to_F 0.0 | source-delta N1; adversarial N3 | L325–326; L359; finite gates L337–346, L361–367 pass 0.0; packaged L375–386; ok L396 |
| nonzero F_eff or s_max·q_norm gives 0.0, ratio None; contract "denominator … exactly 0" describes the computed value | source-delta N1; adversarial N3 | L327–328; L336 (Python-float product); `!= 0.0` at L359–360; contract V002 L37 |
| window ~1e-154 to 1e154; 0.0 or None outside it is not evidence of exactness | source-delta N1 suggested line; adversarial N3 (AUTHOR_DELTA range) | as above |
| (ii) k² or k²/(4πG_EH) underflows (k ≲ 1.6e-162; k ≲ 5.6e-12 at G_EH = 1e300); off-diagonals exactly 0; k = 0 operator, scope-excluded; packaged with ok True | adversarial N2 (L40, L101) | L284 k2; L285 prefactor; L288–289 off-diagonals prefactor·(−k2); finite check L295 passes; ok L396; contract L79 excludes k = 0 modes |
| numpy default `under='ignore'`, no warning even when escalated | adversarial N2 | L284, L288–289 are numpy scalar operations; numpy 2.0.2 `_ufunc_config.py` L134 (geterr docstring defaults) read as text, consistent |
| (iii) G_EH > ~1.43e307: 4πG_EH overflows, prefactor 0, K0 exactly zero; fatal under root's policy, ok True without escalation | adversarial N1 (L39, L100) | L285 `4.0 * np.pi * np.float64(G_in)` then `1.0 / inf`; L288–289 zero entries; L295 passes; A = Pi_eff at L293 |
| qualifies contract L60 and L37 at extreme magnitudes | adversarial L16 (N1, N2 vs L60); N3 (L37, L60); source-delta N1 (L37) | contract V002 L37, L60 quoted correctly |
| does not reopen any closed 0398 item | source-delta N1 ("item 3 stays CLOSED"); adversarial L16 and closure table L137–138 | n/a |

## Findings

| ID | Severity | Addendum text | Finding |
|---|---|---|---|
| C1 | LOW (attribution) | L5: "both checkers find that these paths require extreme magnitudes" | The source-delta checker reports only path (i) (its N1); it records no finding on K0 underflow (ii) or prefactor overflow (iii). The "extreme magnitudes" finding for (ii) and (iii) is the adversarial checker's alone (adversarial L16 "Both need extreme magnitudes in the caller's normalization"; N3 for (i)). Corrected reading: the checkers' stated thresholds for all three paths are extreme magnitudes, from source-delta N1 for (i) and adversarial N1–N3 for (i)–(iii). The substance and the conclusion are unchanged. |
| I1 | INFO | (ii) "it is still packaged with ok True"; (iii) "the zero K0 is packaged with ok True" | ok True also needs the solve and diagnostics stages to pass (L310–374, L396). For example, in (iii) A = Pi_eff, and a singular Pi_eff fails at L311–313. Adversarial N1 says "ok can be True". The paragraph's framing ("can still produce") covers this, so read both sentences as "can be packaged". |
| I2 | INFO | "Together these paths qualify the contract's 'no value is replaced by zero'" | The adversarial review says paths (ii) and (iii) falsify contract L60 on those paths (L16). "Qualify … at extreme magnitudes" is compatible and is not an overclaim, but it is softer: on those paths L60 does not hold. Adversarial N1 also contradicts contract L74 ("They also apply whenever warnings are not escalated"); the addendum does not list L74, although (iii) states the substance. |
| I3 | INFO | "(iii) Prefactor overflow" | The label comes from the 0399 wording. The quantity that overflows is 4πG_EH (L285); the prefactor itself becomes 0.0. Adversarial's numerical table uses "prefactor overflows" for the opposite path (tiny G_EH, giving nan in K0[0][0], which is caught). The addendum's mechanism text is correct and resolves the ambiguity. |
| I4 | INFO | (ii) "The result is the k = 0 operator" | This is exact when k² itself underflows at L284. When only prefactor·k² underflows (for example G_EH = 1e300), the off-diagonals are exactly 0, which is the k = 0 structure (det K0 = 0, whereas the true det is −k⁴/(4πG_EH)² ≠ 0). K0[1][1] = prefactor·(k² − 3z²) (L289), so it keeps any surviving k² term after rounding. This follows adversarial N2 as stated and is not material. |
| I5 | INFO | layout | The addendum is a heading line, two hash pin lines and one prose paragraph. In rendered Markdown, L2–L3 form a separate block. This meets "one-paragraph addendum" in substance. |
| I6 | INFO | citations | The addendum cites review finding IDs and contract lines but no code lines. 0399 does not require code lines; the claim trace above supplies them. |
| I7 | INFO | (ii) "even when warnings are escalated" | This holds for escalation by Python warnings filter with numpy's default errstate, and the addendum says "numpy's default". A caller that sets `np.seterr(under='warn'/'raise')` would get a warning or an exception. The addendum does not claim otherwise. |

No finding asserts that a problem is fixed or that the module is safe at all scales. The addendum asserts neither.

## Execution statement

- Static reading only. I did not import or execute scalar_metric_particular_solve_v001.py or _v002.py, and I ran no UNT, Codex, project or Python script. I used no network, installed no package and did no computation. The IEEE thresholds were checked by hand against the reviewers' stated values.
- Text read: the addendum; both V002 reviews; USAGE_CONTRACT_0397_V002.md; v002.py L270–398 (end of file) and L112–123 (`_vector_norm`, needed to trace (i)); the 0399 task file, read as data; numpy 2.0.2 `_ufunc_config.py` (grep of text only).
- Tools: shasum, ls, find, cat, sed, awk, grep, wc.
- Writes: only this file, created by exclusive create (bash noclobber). No existing file was modified, moved or deleted. Nothing was written under Universal Network Theory. No file whose name matches a forbidden pattern was opened.

Role: distinct checker, not author.
