# Non-gating S1 exact-refusal controls

Backlog #4 / A284 N1. The existing release suite accepts arbitrary exceptions in several controls. This addition requires the actual guard Refusal type and the exact expected code for nine previously surviving guard mutants, plus the precise launcher lock path for L05. It also runs a positive full guard admission on the inherited synthetic fixture.

Result: 10/10 controls PASS and 10/10 single-check mutants detected. W05/W08 were equivalent survivors in Claude3 review0285 and are intentionally excluded.

Run with the fixed Python interpreter, -I -B, then this test path and a new absolute work directory that does not exist. The test pins the inherited release harness bytes and executes only its setup prefix; it does not run the legacy release checks or workers. Mutants replace one guard requirement in memory, or the launcher LOCK constant, and restore it after each probe. No production source is edited.

Synthetic boundaries: native context/policy/replay and disk fixtures from the release harness. No scientific process, actual lock acquisition, mounted-volume read, run tree or network. The audit fence remains active. These controls are non-gating and do not certify production C1s, real launches or contention.

Exact pins are in REVIEW_PACKET_CX1V001.json; output evidence is /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_refusal_probes_cx1/inert_20261022T135135359573Z/REFUSAL_PROBES_REPORT.json.
