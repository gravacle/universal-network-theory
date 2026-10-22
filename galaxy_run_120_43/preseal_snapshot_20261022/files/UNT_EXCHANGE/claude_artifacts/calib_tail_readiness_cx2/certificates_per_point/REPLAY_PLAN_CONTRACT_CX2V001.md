# Own-call replay-plan contract, r5

`date -u`: Sun Oct 18 13:22:46 UTC 2026

Implementation: consumed_states_cx2v010.py. This is a source/custody interface, not scientific launch permission. All refs are exact objects with `path` (absolute file path) and `sha256` (64 lowercase hexadecimal characters computed from those bytes). No discovery of external run folders occurs.

`consumed_states(spec=raw_call_spec, result=raw_result, call_dir=campaign_call_root)` reads `call_dir/out/result.json`, `out/finish.json`, `out/start.json`, `out/inputs/call_spec.json` and `call_dir/TAIL_REPLAY_PLAN.json`. The caller must supply the exact raw archived spec/result objects. A root-level result file is never a fallback.

The immutable plan has exactly five keys:

- `schema`: `DDO154_TAIL_REPLAY_PLAN_CX2V001`.
- `driver_sha256`: `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`.
- `call_result`: exact byte ref to this call's out/result.json.
- `call_spec`: exact byte ref to this call's out/inputs/call_spec.json.
- `replays`: ordered entries containing exactly `ordinal`, `reconstruction`, and `packet`.

Ordinals come from v005 discovery, retaining its original sequence. Include every real state occurrence exactly once, including repeated use of the same state. Exclude the two signed-component placeholder ordinals: those are resolved from the actual reconstructed offset components and never become fictional TailStates. A missing, duplicated, reordered or extra entry fails.

`reconstruction` refers to a DDO154_STATE_REPLAY_DESCRIPTOR_CX2V001 document accepted by reconstruction_cx2v003.replay_state. `packet` refers to a DDO154_I1T_REPLAY_CX2V001 document accepted by current_source_evidence_cx2v004.compute_i1t. Their input refs must name actual saved own-call source/packet arrays. Generated descriptor/recipe metadata may live in the certificate directory; all original source/packet archives must be under call_dir/out. The copied input bytes and all read controls/custody/module pins are rehashed at the end.

Production reconstruction contexts use driver r5 and `replay_scope=PRODUCTION_P128_MS128` (also the default), outer K=128, and integer gas M_s=128. The separate `SYNTHETIC_FIXTURE` context requires an explicit Python keyword opt-in; neither current-source assembly nor complete inventory grants that opt-in. TEST_ONLY state slots remain non-admissible through point/slot validation.

For route-A current/next descriptors, `source.kind=route_a`, `source.iteration` equals the occurrence's actual source index, and `len(source.elements)` equals that index. The descriptor must rebuild that full source/state against its pinned iteration assertion. The accepted boundary and inherited reference/body occurrences must replay this call's exact accepted manifest. Signed offset descriptors and finish records must identify that same manifest; their negative component parent digest must match its accepted full state.

The join independently checks expected stage sequence and all observed Picard passes, discovery custody, actual full state/source hashes and P/F, exact point/configuration, actual occurrence assertion, source-packet I1-T, canonical stage kind, positive gas zero mode for positive states, and both actual nonnegative signed-component rosters. Signed finite-denominator GQ is a separate gate, not inferred from the components. Complete returns only when every required occurrence is verified and every structural blocker is absent.

Return contract: `complete` boolean; `states` have exactly `state_sha256`, `source_sha256`, `stage_kind`, `nonnegative_masses`; `occurrences` preserve discovery; `joined_occurrences` carries every successful real join; `resolved_signed_component_ordinals` identifies discharged source obligations; `verified_files` holds the byte snapshot; `blockers` is typed. Even a complete inventory has `certificate_status=UNAVAILABLE` and `point_status=PENDING_CERTIFICATES`: approved EPS/GQ/LO proofs, producer/packet-binding review and orchestrator acceptance remain separate. Failures keep `complete=false`, `states=[]`, and typed STATE_JOIN_UNAVAILABLE detail.

TESTED: bounded numerical reconstruction, I1-T, pin/scope and protocol tests described in the companion review. UNTESTED: any full production call inventory replay. No actual production plan or claimed complete production inventory was created by these tests.
