# Producer registry V003: PASS_WITH_FINDINGS

Date -u: Sun Oct 18 18:55:00 UTC 2026

Registry: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/out/PRODUCER_REGISTRY_C3V003.json` — SHA256 `6b6f76ae301d75878156e7b8f2641215d215ada9017dbcba3b805a99589701a3`.

TESTED: 112/112 predicates met across the two-registry review and owned negative controls. Exact r11 source pin before/after is `a5d10cb1a213931713b9712da0781042d8e02ed5c1e81cda21b97c33b0559c8a`. The actual registry's r11 load outcome is **REFUSED_EXPECTED_SRK_R12_DEPENDENCY**. Registered permitted producer, builder and five gate-record byte pins matched. Registry/build-report producer registrations, record hashes and GQ node-count maps agree. Guard-blocked accesses: 0; forbidden-reference reads: 0. No producer or supplied validation suite was executed.

V003 intentionally requires A88/r12: SR_K uses PRODUCED_AFTER_THE_SEAL. Its refusal on r11 is expected compatibility behavior, not a new A88 finding. A bounded test copy with only the SR_K marker replaced by an empty list passes the remaining schema and byte checks; the actual file was preserved. Actual r12 compatibility is UNTESTED.

Seal-readiness findings: empty producer slots: B0, B0_FA, B0_N3, B0_RO1, B0prime_DRY, B0prime_RERUN, B1, B1_OFF, B2, B3, FLAG_RULINGS, I1T, I4, MT, SRB_ROT. Empty gate-record slots: B0, B0_FA, B0_N3, B0_RO1, B0prime_DRY, B0prime_RERUN, B1, B1_OFF, B2, B3, I4. Identity comparator count is 0. These named slots fail closed; this registry is not complete seal evidence. No claim is made that all gates pass or that root has registered this artifact.

UNTESTED: scientific correctness of the five referenced gate records, production-run identity, full build_context/CLI, actual gate evidence execution and adoption. Other review lanes own gate-specific recomputation. Principal restrictions remain in force; no run trees, C5H/UVT metadata, NGC observed/target velocities, network or session logs were accessed.

Evidence: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_records_cx2/registry/run_20261018T185440Z_62948/RESULTS.json` — SHA256 `aa801aba79f025c821f67cbdc54add266bc6cd822a716076d7d73bee69903575`; owned harness `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_records_cx2/registry/probe_registry_cx2v001.py` — SHA256 `a80f35622f5968c081d096ece79974d66ae5d2fa963c17c576d85f00e5ef124b`. All cited inputs and permitted referenced bytes are byte-pinned in the companion manifest.
