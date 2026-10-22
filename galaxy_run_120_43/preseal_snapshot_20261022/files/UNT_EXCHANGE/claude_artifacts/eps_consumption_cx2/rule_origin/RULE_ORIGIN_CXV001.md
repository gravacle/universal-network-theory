# EPS 1.1× refinement rule: original provenance and stated rationale

`date -u`: Wed Oct 21 17:23:20 UTC 2026

**FORMAL conclusion:** the 1.1× rule is a registered finite-sampling refinement-stability criterion. Its originating design and preregistration explicitly call EPS an estimate, not a proven supremum. No derivation of the specific 10% cutoff from an observational-error budget, numerical roundoff bound, Lipschitz constant, or rigorous enclosure was found in the examined source chain. It should not be described as such a theorem. This is a scoped provenance finding, not a claim that no other historical discussion exists.

## Origin and registration chain

1. **Design motivation.** The original design review K6, `DESIGN_V001_CHECK` lines 140–150, distinguishes the field-level expression from a full row bound and says ε is a maximum over a declared finite sample, not a certified sup (line 148). The successor `DESIGN_V002` describes its correction as a sampled-with-refinement certificate labelled an estimate, not a proven sup (line 57).
2. **Earliest explicit 1.1 rule located in this examined chain.** `DESIGN_V002` §1.5, lines 235–240, prescribes 13 lattice-symmetric plus 13 midpoint directions, 64 radial samples per decade in each unit shell, refinement to 26+26 directions and 128 per decade, and ε_refined ≤ 1.1 ε_base. Two failed refinements yield EPS_UNCERTIFIED and block T runs. It explicitly labels the certificate an estimate, not a proven sup. The file's line 3 says design only, not adopted: this establishes design origin, not by itself binding authority.
3. **Machine-readable preregistration.** The accompanying `DRAFT_PREREG` `/gates_before_any_T_result/EPS` states the same rule and the same limitation. The early `ORIGINAL_EPS_PRODUCER` docstring lines 1–12 explicitly points to prereg V007 draft R1 and design V002 §1.5; its `certify` lines 38–52 implement acceptance at L1/L0 ≤1.1, or after the extra L2/L1 ≤1.1 test, with two failures uncertified.
4. **Root confirmation.** `ROOT_V005_FROZEN` A50 item 9 (line 132) confirms that two EPS refinement failures are uncertified, citing R1. A52.5 (line 219) explicitly acknowledges under-sampling of per-shell ε above about 15/kpc despite a converged global ε_max; it requires the successor envelope treatment and labels existing affected values lower bounds pending that treatment. A57.4 (line 425) requires envelope consumers to read full-envelope fields and numerical sup searches to be labelled estimates, not proofs.
5. **Binding sealed text.** `SEALED_PREREG` `/gates_before_any_T_result/EPS` retains 1.1, the two-failure refusal, and both the opening warning that numerical sup searches are estimates rather than proofs and the closing warning that this is not a proven sup. Its source list explicitly includes R1, A50 item 9, A52.5 and A57.4. This is the strongest byte-pinned registration located here, distinct from the earlier unadopted design.
6. **Current per-point implementation.** `POINT_PRODUCER` lines 139–160 retains the same two comparisons over 26/52/104 directions and 64/128/256 radial samples per decade. The returned `certified` flag means at most one failed refinement before stability is achieved. Its module header (lines 3–6) expressly separates the registered discrete rule from cardinal-torus numerical search and says finite/search maxima are estimates/lower bounds on the continuous supremum, never a rigorous enclosure.

## What the rule does and does not justify

**FORMAL:** comparing two finite sample maxima can diagnose sensitivity to this particular increase in sampling density. It cannot, without an additional regularity or verified enclosure argument, bound values between the sampled points. The threshold is one-sided (`refined <= 1.1 * base`), not an absolute error bound and not a symmetric relative error estimate. The current gate has no additive absolute floor and no dependence on the governing maximum across shells. Tiny shells can therefore fail the same ratio threshold as a dominant shell.

The original source history already makes this limitation concrete. `HISTORICAL_EPS_V003` lines 3–10 documents inverse-cache nodes exceeding the sampled per-shell estimate by up to 1.29× although the 1.1 refinement rule passed; it retains the rule but expands the values used by the field-bound calculation using dense and node maxima. `HISTORICAL_EPS_V005` lines 6–8 separately preserves the rule as the verdict criterion while lines 9–21 describe envelope and actual-set searches feeding the numerical per-shell values. These are source-recorded historical findings, **not numerical results independently re-tested in this helper task**.

**Implication for the parent analysis:** neither passage of 1.1 nor the observed 1.12 failure alone supplies a rigorous worst-case bound on the true continuous response or downstream error. Any finite worst-case statement must identify an independently justified upper bound and the consumer's sensitivity/weights; treating the observed refinement difference as a guaranteed upper bound would go beyond this registration. This helper does not decide the actual consumer bound or choose a new threshold.

## Current authority boundary

The captured `ROOT_V006` A294 calls the current rule purely relative and says amendment requires a root physics-process ruling. A295 is a ruling in principle; its final constants are explicitly deferred until the requested analysis. No fraction, floor, safety multiple or successor is inferred or built here. No Claude3 new analysis was read and no cross-lineage coordination occurred.

## Verification scope and evidence

**TESTED:** byte SHA256 calculations, JSON selection of the EPS clauses, and eight literal source comparisons recorded in the evidence file. **FORMAL:** provenance and control-flow/math interpretations above. **UNTESTED here:** numerical re-evaluation, any certification output, any continuous-supremum enclosure, consumer propagation, and production execution. No reviewed Python module was imported or executed; no scientific command, run-tree access, NGC data, postseal records, session logs or network were used.

All paths below cite source bytes; referenced run or certificate paths inside those sources were not dereferenced.

- **DESIGN_V002**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_design_c2/v002/TAIL_SCHEME_DESIGN_V002.md`
  SHA256 `cdb16d1c42da39cf8eabe253b7192f4f391d19adfdd026e57a6971837a6aa944`
- **DESIGN_V001_CHECK**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_design_c2/check/CHECK_V001.md`
  SHA256 `006e8463161c5456cac6c053b9ef690c063622c1da9f7b1f0909250d7438fcd2`
- **DRAFT_PREREG**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_design_c2/v002/KMAX_TAIL_PREREG_V007_DRAFT.json`
  SHA256 `357c0738344a3266b21506b7ab5e4278524a837fc8ccd831cd4222f7cfa8a0a7`
- **SEALED_PREREG**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/V007_SEAL_ASSEMBLY/KMAX_TAIL_PREREG_V007_SEALED.json`
  SHA256 `b2989012c92161a7da3dd10d0148e1607422416d369fc4ebe164217758b5c695`
- **ROOT_V005_FROZEN**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md`
  SHA256 `c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1`
- **ROOT_V006**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md`
  SHA256 `ea88b1809e9f630c07844fd66e88bce2950d4def4fb605dff8ce9a01b655a581`
- **ORIGINAL_EPS_PRODUCER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v001/tools/eps_cert_c2v001.py`
  SHA256 `6bf0afba04b8a676bf3d721b20a7d60de60d99b9a065968078674fd75998714c`
- **HISTORICAL_EPS_V003**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v001/tools/eps_cert_c2v003.py`
  SHA256 `a97c1a8f7a8c9965b2d16c2ab87fbe948b3e2173aeca243f1c85d85d7706487d`
- **HISTORICAL_EPS_V005**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/tools/eps_cert_c2v005.py`
  SHA256 `3c20fd514dded6d4fcb44ecd5d0d230c8728a12b2025b307bcbcf112dcf2b709`
- **POINT_PRODUCER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/point_response_producer_cx2v002.py`
  SHA256 `a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231`
- **DISPATCH_0854**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0854_2026-10-21_codex2_independent_eps_consumption_analysis_then_rule_successor_standby.md`
  SHA256 `9669f5d4fa93931ad0d546d2ac9834f962ad946b57f45a3695023a92b234ae5c`
- **Selected-source evidence and eight mechanical checks**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/rule_origin/RULE_ORIGIN_EVIDENCE_CXV001.json`
  SHA256 `20f38a12f63087aa2950bc51ca15af55b06c5eb287885735a2ef183dc0529a3c`
