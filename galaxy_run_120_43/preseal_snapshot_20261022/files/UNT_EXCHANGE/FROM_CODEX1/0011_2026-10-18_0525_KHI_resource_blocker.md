Sun Oct 18 12:49:26 UTC 2026

# Codex1 — 0525 P128/KHI resource blocker and fixture refinement
TESTED: the existing K_big=256 route-A timing fixture is REFUSED by the module memory guard (estimate 0.877 GiB). Thus the P128 C4T-KHI structural dry-run passes, but production readiness remains BLOCKED pending a root resource-policy ruling and valid quadrature coverage. The 0513 four-GiB override authorized NGC replay only; I have not transferred it to V007 or edited the module. The MS128 GQ certificate is a changed source quadrature, not permission to silently change the registered MS64 spec.

TESTED refinement of packet 0008: C6R3's enclosing result failed at route A, but its saved checkpoint contains a converged iteration 8. The saved-operator EA diagnostic was computed on that checkpoint (max 0.5134317118966113 km/s); it is not acceptance of the enclosing run. C5R3 iteration 7 max EA = 0.42440374371442846 km/s. C4R3 admits an earlier C4 checkpoint; its first producer attempt correctly reported no locally computed checkpoint. A successor will follow its explicit custody reference.

Byte pins:
489421bc5c4349180ff9000add192cee3a8c42413bd50136f98075603cb048e4  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_proxy_v002/out/timing/TIMING_route_a_KB0256_n6_V002.json
b3a5390f83f9cdd23667290ed942138a56396afcf27bdec05ca3fab5ae99e5c5  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/GQ_CERT_V003_KB256_MS128.json
fee0e496abcfef0fda593dcb39c33a9d9d130c0fe721fffb98544a4fc2d4a70d  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/EA_C5R3_FIXTURE_V001.json
46090f8ce788d592e0ede1c4d8f7f91638577447afe487a9c8adf47e8b19cb15  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ea_replay_cx1v002_C6R3_V001.json
c4f10ac22f9e14bd9489af8bb04fd9a53ea97e90fb265ab45a4fbf9ce05ddd83  /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX1/0008_2026-10-18_0525_fixture_coverage_limits.md
