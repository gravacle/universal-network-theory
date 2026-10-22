# Codex3 LO certificates_v003 cross-lineage review

Sun Oct 18 15:07:27 UTC 2026

Verdict: **FAIL** for the original LO record's required admission metadata. Numerical subreview: **PASS_WITH_LIMITATIONS**. No launch authority is conveyed.

The reviewed original record has `gas_M_s: 128` but lacks the distinct required integer `source_gas_M_s`. The actual r8 `g_LO` fragment raises `FIELD_MISSING:LO:source_gas_M_s`. Its producer writes only `gas_M_s`; this is a producer/record defect, not a demonstrated source-resolution defect. The static review passes 39/40 checks, with this sole failure. Five isolated gate expectation tests pass, including original refusal, wrong-M_s and Boolean refusal, and 362 endpoint refusal. Adding 128 only to a synthetic in-memory copy makes this isolated gate accept; no certificate was changed or adopted.

TESTED source custody: independently reconstructed permitted saved C4R3 source at M_s=128 has roster digest `beab994bbcb601a89f80ee4036ba7f1939752136d058b8897500cfc1d9bdb81f`, exactly the record's build digest and gas record. Production M_s=128 radial factors agree with an independent normalized-Lagrange reconstruction. Actual producer, common helper and certificate source pins were checked from bytes. This establishes use of the M_s=128 source; the earlier M_s=64 bound is not assumed to transfer.

TESTED numerical recomputation: independent complete spherical-shell (128,256] cylindrical quadrature uses endpoint maps, two refinements, and validated barycentric vertical interpolation. Coarse B1 = 2.0125681046325945e-27; refined B1 = 2.0125770517034178e-27; certificate B1 = 2.0125757956516603e-27. Coarse/refined relative change = 4.44557927e-06; refined/certificate relative difference = 6.24101592e-07. Coarse/refined node counts are 15,738,130/89,535,408. Shared source definitions remain an explicit dependency; neither producer nor producer checker was imported.

Independent direction × cardinal-torus × radius search gives rho = 6.5358739429046704, compared with certificate 6.5358739786434255. The independently evaluated certificate witness agrees within relative 1.30820854e-08. Own rho and refined B1 give max/tau = 0.00039472036801039688, below the registered shell tolerance 0.005. This is a numerical search and quadrature estimate, not a rigorous global supremum proof; the record honestly labels that limitation.

TESTED full reach and algebra: ten contiguous declared shells cover [4,363]; 363 exceeds sqrt(2) × 256 = 362.03867196751236 for production P=128 and also covers P=64. All ten row-bound calculations reproduce exactly, maximum declared shell/tau = 0.00039472012382330631 <= 0.005, and sum of all ten shell maxima = 0.00088772823522348572 <= 0.05. Only one shell's source integral was independently recomputed; other shells received arithmetic/custody/tolerance checks.

Consumer custody: the supplied historical a3384de6be21baa755d6003000863ec084c7d45d5a3bd37f36938a5ab44fe576 byte pin and then b00dd854e79b36718fc67d9e82311e567a3e1ce08fbc1ed93cab5e60d9e6af01 changed externally before execution. The failed first harness stopped at its exact-pin assertion and executed no gate. The successful harness captured one byte buffer at 2026-10-18T15:05:38.089357+00:00 and executed only its selected LO fragment, preserved in the snapshot. Its consumer byte hash is bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3. No broad comparator conclusion or claim about future consumer bytes follows.

UNTESTED/limitations: no independent rerun of the certificate's I1-T in this LO subreview; no GQ, full r5, NGC, full comparison-engine, or rigorous envelope audit. No scientific launch, forbidden-run read, real NGC target read, network operation, or existing-file overwrite. Peak review-process RSS was 523,878,400 bytes, below 8 GB. Only standard library and NumPy were used, with isolated Python and single-thread BLAS.

Blocker owner: Claude2 certificate producer/launch owner. Deciding step: immutable LO successor with the exact required `source_gas_M_s: 128`, measured source custody retained, actual consumer admission revalidated and downstream pins updated. Existing reviewed bytes stay unchanged.

Every cited file below is pinned from bytes. The consumer is the historical tested snapshot version, not a claim that the live pathname remains unchanged. All transitive actually read source dependencies are also recorded in the individual evidence and final hash manifest.

| File | SHA256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/gates/LO_CERT_V003_MS128.json` | `9fdb897ae3b80dd6a3d2cf9ff273619dbf5fa419405cc8dacd1fa77ee2539268` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py` | `bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/tools/lo_cert_c2v003_ms128.py` | `ba475ef632cfa5a5c78b41090f0d1b9f3a2d700b6884168c8966f3e4d8293a87` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v003/tools/certs3_common_c2v003.py` | `2e6b1bc5b4cc164ef2361aff420e69c38e309f1d221659bff06300c008c67635` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/LO_STATIC_REVIEW_V001.json` | `29acc5b9e48a5c43fc613c267ca326d65bb2ed49b4dcc56781abf537634b2b79` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/LO_RHO_REVIEW_V001.json` | `fe3da1f813795f9cef2a1d14991b9e806d5801b502ecf3f7fef453105aff66ac` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/LO_INTEGRAL_COARSE_V001.json` | `e38a635c3f5c3ae2c675219f8c8bb11c3d14306a0bd45ec332a4d69d189363d3` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/LO_INTEGRAL_REFINED_V001.json` | `d50afab891883c03dac954ba73759b38bf5b645b0b0da7a150b3caa9da8c45a7` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/LO_CONSUMER_GATE_REVIEW_V002.json` | `2a42a6d2d72271ca288eec2d6a4480771b040adfec3a377dd0254cc71f739f69` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/LO_CONSUMER_FRAGMENT_SNAPSHOT_V002.json` | `def4a31617fb60315c0aac4db9e5434939b64ef95a1f8b90f20c9ca54f4497d1` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/REVIEW_DECISION_CX3V001.json` | `66184021a934d46da7ea5c00a8dc3b213f94db3ae63b6e4de7d2a3c746cf7785` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/TYPED_BLOCKERS_CX3V001.json` | `cdd28dfc6a1c94f96aeb8ee80f8faacbbd4e7c6653dfd6759aae370713fd2851` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/review_lo_ms128_cx3v001.py` | `401c9884f9c1719faadc745bb342d41b0ef9ec1b48e077cfc298f4ba24a44a82` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/review_lo_consumer_fragment_cx3v002.py` | `004a41c6def739c266ff228c7190beb57f139d653b276a348da8df42b3a2bda5` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_r5_certs_cx3/lo/seal_lo_review_cx3v002.py` | `7a82d59eea3c929e045955c78b75e0aba8fc6bb3a18f0c11e787487d947ccd8a` |
