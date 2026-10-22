# REVIEW_COMPARE_R14_C4V001: compare r14, delta review of record (Claude4, cross-lineage)

- **Reviewer:** lane Claude4 (synthesis stage, run by a Claude4 helper). Cross-lineage: Codex1 built r14.
- **Authority:** dispatch 0651 (`8bed78cb8f63d033ce080b1e8170e57d1e31bc1a06c268d784ade65e5c16e9ba`) and root entry A114 in V006. Severity follows A115, the blocking criterion root set during this review. A116, A117 and A118 were appended to V006 during this stage; each was read and applied (§6).
- **Written:** 2026-10-19T04:10Z and after (`date -u`). Refute by default. Every claim is labelled TESTED (run or hashed from bytes in this review), FORMAL (read from bytes, not executed) or UNTESTED. AUTHOR-RUN marks builder counts that were not re-run.
- **Relation to Claude4 0134** (`d42bb2a1a32df17da1d84b11717c0b2d361f416c82ab911421e4e62135254b88`, 03:59:28Z). That post stated the verdict of record and said this consolidated file would follow. This file re-checks every lens finding from bytes and reaches the same verdict and the same blocking count. It adds one item that 0134 did not have (**R4**) and one caveat (**R3**).

## Verdict

**PASS_WITH_FINDINGS. 0 BLOCKING** (A115: (a) 0, (b) 0). **4 SHOULD_FIX, 12 NOTE.**

- **Scope.** The r14 source `f3f9ba7e…` as published under **SELECTED_R14_CX1V002 `6b650ece…`** (IMPL V002 `2ba6d12e…`), which is the selection A116.1 and A117 name.
- **The dispatched selection is superseded.** SELECTED_R14_CX1V001 `dc74949d…` is superseded by V002, and seal tool 4 would refuse it (R1). Do not seal from it.
- **No SHOULD_FIX item is in r14's bytes.** All four are publication or seal-path items, and each one fails closed.
- **Why nothing blocks under the dispatch rule** ("makes r14 wrong as the compare of record, or prevents the seal with r14"):
  - r14 is exactly A114.1: one 6-byte insertion.
  - Its behaviour changes only for I4.
  - The seal tools of record (v004) accept r14 with only the compare slot value changed. Tool 4 passes with IMPL V002. Tools 2 and 3 see the compare slot only through `seal_slots.compare.value`, never through its rule text.
  - What still refuses r14 is the r13-bound pre-stage c3v020. Some inputs are not yet final: V003 is still a draft, the NEW-item list successor is not published, and V010 was published at 04:13Z but is not yet selected. A114, A116, A117 and A118 already order all of this, and no change to r14 could or needs to fix it.
- **Why nothing blocks under A115.** No finding is reachable by honest pinned producers acting on genuine records, and none can change a physics reading. `g_I4`, its fields and its parallel8 role are byte-identical to r13. Only the moment at which the I4 record may enter has changed.

## 1. Object, every pin from bytes (TESTED: `shasum` at 03:41Z, then again inside the fenced run at 04:02:56Z)

| File | sha256 |
|---|---|
| r14 source `v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py` (410439 B) | `f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7` |
| SELECTED_R14_CX1V001.json, as dispatched (superseded) | `dc74949d1d4f19336661f8ce85e9a85de0176837adad61c7a9585a147f933533` |
| **SELECTED_R14_CX1V002.json** (the selection of record) | `6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a` |
| FIELDS_R14_CX1V002.md (selected fields) | `2ce9f1c710bb16ad1224ab49ec0713dd4f3fd48a04d730c78cfc3ed0ffdb7fe4` |
| FIELDS_R14_CX1V001.md (generated contract) | `a33b153b40e3a709cbbf095908007c737e90c3383e6a113d30c786732e800c83` |
| COMPARE_V007_IMPL_R14.md (IMPL V001) | `854cad0d269161bff1fc314cdb2801df000eeb0d94ea004ef659d62edfb44680` |
| **COMPARE_V007_IMPL_R14_CX1V002.md** (IMPL of record) | `2ba6d12ecc36ab444365348573b7f49a02a12a818dd15d67de35d77300fa17c9` |
| VALIDATION_R14_CX1V001.json | `930ca7bc78e74134aeac46851a6bbf9481e78f9ce3862b77d370b716dd8380ec` |
| author harness tests_…_r14_cx1v001.py | `998e0c2eb7309fd2a2135bc27974b95899f2f3583116312ccb7476120a1555c6` |
| SOURCE_DELTA_CX1V001.json | `56a95b7ef983608b89b5f4c30799fa9ea578eb69c7e01ccb31de96b8bf92ec51` |
| HASHES_R14_CX1V001.json / HASHES_R14_CX1V002.json | `8b92153a0200953df2e4df8e1993cfcade58ddc4b6b5536439359a9119be5a8f` / `46b811c188834d8a72293d60d6ed792c8130dc31a565d40ac8884713e8b4d317` |
| BUILD_PROGRESS_CX1V001.json | `d246fa90dd5032ae6f6801056d1763b498fa6aba5534346b0d379a7e0ace0d01` |
| parent r13 source (superseded) | `f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157` |

Every sha the dispatch gives equals its bytes. Nothing differed, so there was no stop. SELECTED V002 was re-hashed at 04:09:53Z and was unchanged.

**Reference inputs** (TESTED, from bytes):

| Input | sha256 |
|---|---|
| r13 IMPL | `274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3` |
| r13 FIELDS | `7b116b0103fdeb83d2cd358976e2c901be15313ad7f9ab8d159af6d9ee3bb365` |
| r12 FIELDS_R12_CX3V002 | `5cc95a06dbe91275cd891e9832a0b7709301ac076a1ce49a3a675d76ee1a967f` |
| r13 harness | `71c7b516bca41a8b0779e5da39704a84d1188bdeeb8f3df4920f843faae7e5aa` |
| misnamed r14 harness copy | `b00e533adf3f62846f5fe4da3fb74bd73655a37c4065c438dcb37736c7c4d059` |
| seal tool 4 | `9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41` |
| seal tool 3 | `316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af` |
| seal tool 2 | `c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1` |
| seal tool 1 | `a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4` |
| seal_common | `101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21` |
| SELECTED_SEAL_TOOLS_V004 | `593c59faf39074b14579f927ae17c5aeda1f7450ee4a9f264f96a1f2c7b195e0` |
| disclosures V001 | `b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6` |
| disclosures V002 | `a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3` |
| disclosures V003_DRAFT (unchanged through 04:09:53Z) | `21968a07f50d6bf5dda9e64cfa61c7e3ec80bca9943c0f84956611ac99b8be3e` |
| r6 SELECTED | `7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0` |
| prereg r6 text of record (JSON) | `d28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9` |
| ROOT_ITEMS_R6 | `11136b1ac5197bc22a49d7463eb68e6b181bf6613c55a36a8262080610d6611a` |
| case block | `76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71` |
| pre-stage ROOT_SEAL_STEPS_c3v020.sh | `36058df84bb2088970be442bc64445a4c6939b45df3e9cb3294cedef62c65ac0` |
| pre-stage selection c3v009 | `9e10eae111ba322806195273e149831da60a99956e7e0e0f01f46711f0f62167` |
| registry V009 | `32ddadcb7567213f42288004f19def122da1d8c4db1a426f0f888bc3242484e8` |

**V006 moved four times during this review.** It was `ca5d7ae3…` at the lenses' first read (03:20Z, prefix from the lens reports), then:

| Time read | V006 sha256 | Change |
|---|---|---|
| 03:41Z | `63e7802ffaec4f2846239a198eba0348b5dcce055af55d6c922446785563f4cf` | A115 |
| 03:58:53Z | `3d4cbe565faa2711dd9e910e781090e2a2063ed9a31b77015d03e684bb8aadce` | A116 |
| 04:01:09Z | `963f4bf13066455f768cf500b204e7999ec87b45fad05d8d8c3f5959ad88d9e3` | A117 |
| 04:09:53Z | `8ac68396110fd789471d65e4bff663f07d6132a08fcf52df4d54784a197000ff` | A118 |

The A114 section (L120–L140) hashes to `21720e08ab96db7ce401d3cc67290c34f206a92b6ebdef9972cb20733c4becdb` at every read from 03:35Z (lens) to 04:10Z (TESTED). That it is also unchanged since 03:20Z is FORMAL: a lens compared it by eye.

## 2. What r14 is (TESTED, `synthesis/scripts/synth_checks_c4v003.py`, section S1)

- **The delta.** r14 = r13 with `'SR_K')` → `'SR_K', 'I4')` on L341, the last element of `GATE_RECORD_AFTER_SEAL_ALLOWED`.
  - The old line is unique in r13 and the new line is unique in r14.
  - The forward step on r13 gives `f3f9ba7e…`, and the exact inverse gives `f5adfd11…`. The size grows by 6 bytes (410433 → 410439).
  - Both files have 5865 newlines and no CR, and L341 is the only line that differs.
- **SOURCE_DELTA.** Its `diff` equals `difflib.unified_diff(r13, r14)` (876 chars), and `exact_inverse_restores_parent` is true.
- **Every use of the tuple.** Its name occurs on exactly L332 (comment), L341 (definition), L1106 (docstring), L1122 (the loader's membership test), L1126 (the refusal text, `'/'.join`), L1184 (`gate_record_sha_codes`, membership) and L5172 (the FIELDS text, `', '.join`). There are no other references (7 occurrences of `AFTER_SEAL_ALLOWED`). There is no loop over the set and no dependence on its order.
- **No other change.** `g_I4` (L3741–L3759) is byte-identical in r13 and r14, and its body makes no `xr` call. The word `A114` occurs nowhere in r14. r14 has no runtime self-name check: its only file-name strings are docstrings and the inherited FIELDS heading, and `script_sha256` is computed from `__file__`.

## 3. Behaviour of the token (TESTED under fence_c4v002 on synthetic inputs, unless marked)

r13 and r14 were compiled from their verified bytes and called in-process.

- **The loader, swept over all 25 `ALL_GATES`** (`{g: PRODUCED_AFTER_THE_SEAL}`).
  - r13 accepts exactly the nine: SRB_ROT, RB_FP, T2I, EA, MT, I1T, FLAG_RULINGS, HARMONICS and SR_K.
  - r14 accepts the nine plus I4.
  - Every refusal is `PRODUCER_REGISTRY_GATE_RECORDS`.
  - Every gate A114 names is refused: B0, B1, B2, B3, EPS, GQ, LO, LO_NGC, DOUBLING, and the identity gates B1, B1_OFF and B0prime_RERUN. So is the B0 family the list does not name: B0prime_DRY, B0_FA, B0_RO1 and B0_N3.
  - The file route through `load_producer_registry` agrees: r14 accepts I4 and refuses EPS, and r13 refuses both.
- **`gate_record_sha_codes` on hand-built registries.** r13 and r14 differ only on I4: `[]` against `GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:I4`. r14 refuses all 15 gates outside the ten.
- **The 12 A114 MUST assertions, replicated.** r14 passes 12/12. r13 passes 11/12, failing only `A114_MUST_I4_TOKEN_ACCEPTED`. The author log `author_v002.stdout.txt` (`d8ccd0be…`) shows the 12 lines PASS, at lines 622–633, and 718/718 overall (AUTHOR-RUN).
- **`evaluate_gate('I4')` under a token registry with a registered synthetic producer:**

  | Input | Result |
  |---|---|
  | no path, or a path not yet written | MISSING `GATE_RECORD_MISSING:I4` |
  | a valid record | PASS |
  | an empty file | RECORD_DEFECT `GATE_RECORD_UNREADABLE:I4:JSONDecodeError` |
  | a placeholder (verdict PENDING, no `bitwise_equal`) | RECORD_DEFECT `GATE_RECORD_FIELD_MISSING:I4:bitwise_equal` |
  | an unregistered producer | RECORD_DEFECT `PRODUCER_NOT_ROOT_REGISTERED_A62_2:I4` (the token does not bypass the producer pin) |
  | `bitwise_equal` false with verdict FAIL | FAIL `I4_SERIAL_PARALLEL_NOT_BITWISE_EQUAL` |
  | the same, but with the PASS verdict | RECORD_DEFECT `VERDICT_PASS_CONTRADICTS_DATA:I4` |
  | tail OFF, or a driver not in every T-case | defects `I4_TAIL_NOT_ON`, `I4_DRIVER_NOT_REGISTERED_FOR_EVERY_T_CASE` |
  | a sha-list registry naming another sha | RECORD_DEFECT `GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:I4` (the token waives this check; a list binds it) |
  | a sha-list registry naming the record's own sha | PASS |
  | r13 with a hand-built token registry | RECORD_DEFECT `…TOKEN_NOT_ALLOWED…:I4`, the contradiction A114 describes |

- **Modes.** In both rounds, `required_gates('parallel8')` contains I4 and `serial_with_exemption` does not. In the case block `76309ae3…`, `route_a_mode` is `parallel8`; that is its only value, and it was the only key read.
- **The reading** (FORMAL, r14 L4539–L4572; also TESTED by lens 2 through a stubbed `evaluate_v007`, 60/60).
  - A required gate that reads MISSING joins `inc`, so the reading is INCOMPLETE before any T-test.
  - In parallel8, an I4 FAIL adds "parallel8 route A not licensed" (INCOMPLETE, `I4_NEXT`).
  - Any RECORD_DEFECT reads NO_RUN.
  - So before the real I4 record exists, I4 never reads PASS and parallel8 route A is never licensed.
- **FIELDS.**
  - The regenerated r13 contract is `5cc95a06…`, equal to r12 FIELDS_R12_CX3V002.
  - The regenerated r14 contract is `a33b153b…`, equal to FIELDS V001.
  - The two differ only on L66, `…, SR_K, I4; every other gate still requires a registered record sha…`.
- **The real registry V009** (`32ddadcb…`, 25 producer gates) loads identically under r13 and r14. A V009 copy with `gate_records.I4 = PRODUCED_AFTER_THE_SEAL`, standing in for the expected V010, is accepted by r14 and refused by r13 (`PRODUCER_REGISTRY_GATE_RECORDS`).

## 4. Seal integration (TESTED unless marked)

- **Tool 4 v004 `new_items_codes`** (loaded from its folder; seal_common, tool 2 and tool 3 verified from bytes), with reviewed sha `f3f9ba7e…`:
  - IMPL V001 `854cad0d` → `NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE`;
  - IMPL V002 `2ba6d12e` → pass;
  - the r13 IMPL → refused;
  - SELECTED V001 offered as the IMPL → pass (the check is a substring test).
  - IMPL V001 contains neither the full sha nor the 8-hex prefix. IMPL V002 is IMPL V001's bytes plus "Reviewed source binding (Claude4 0129)", which names `f3f9ba7e…` in full.
- **The selections.** SELECTED V002 differs from V001 only in `implementation`, `note`, `supersedes_selection` (`dc74949d…`) and `utc`.
- **Tool 4 `manual_disclosures_form_codes`.**
  - V002 and V003_DRAFT pass.
  - On synthetic copies of V003_DRAFT: the N1 spec sha placed inside the A114 row's `text` passes. The same sha as an extra row key is refused with `MANUAL_DISCLOSURES_ROOT_DISCLOSURE_ROW`, because rows are exactly `{id, source, text}`.
  - An `E_R6_2` row in `root_disclosures` passes. A top-level `e_r6_2_text` key is refused with `MANUAL_DISCLOSURES_KEYS`.
- **E_R6_1.** Tool 4's `E_R6_1` (UTF-8 sha `c28202b0909371f43180ca832e4652f3d835a977852cde5c261842315deb33f4`) equals r6 SELECTED `basis.erratum_E_R6_1` and V003_DRAFT `e_r6_1_text`. It names the r13 IMPL `274f7049` and contains no "r14".
- **V003_DRAFT's A114 row** names r14 `f3f9ba7e…`, SELECTED_R14_CX1V002 and IMPL V002 `2ba6d12e…`, and says "supersedes r13".
- **Tool 3 (A116.4 asks this).**
  - Its source never reads a `rule` key (FORMAL).
  - It maps the prereg's `compare` slot to `compare_reviewed_source`.
  - A sealed prereg holding r14 as the compare value, with r6's rule wording, equals the text of record outside `seal_slots.<k>.value` (`blank_slot_values`), so it passes.
  - Editing the rule wording would differ, which is `SEALED_PREREG_TEXT_CHANGED`.
  - Tool 2's prereg check reads only `seal_slots.compare.value` (FORMAL, L120–L124). Lens 3 TESTED `run()` PASS on r14 with a synthetic sealed copy.
  - **No v004 tool checks the slot value against the rule text, and v004 needs no change for r14.** This agrees with Claude4 0133.
- **The pre-stage.**
  - **Refusals (FORMAL).** c3v020 L272 sets `COMPARE_R13_SHA="f5adfd11…"`, and L365 refuses any other reviewed compare ("must be r13 f5adfd11").
  - **Predecessor pins.** L222 pins disclosures V002 and L241 pins registry V009. L271's superseded list lacks `f5adfd11`.
  - **Role pins that still hold.** L218/L377 role-pin r6 SELECTED's stored `impl_of_record_r13`. That still holds with r14, so it is not a refusal.
  - **The SELECTED-record check** (L405–L413) is generic. Re-implemented here, it passes both r14 selections and refuses V002-against-r13 (`SELECTED_SOURCE_DIFFERS`).
  - **The successor.** A `seal_assembly_c3/c3v010_prestage/` folder has existed since 04:01Z, but there was no c3v010 selection as of 04:09:53Z. It was not read.
- **C-08.**
  - r13 and r14 carry the same 19 NEW ids with identical first-line maps.
  - All 19 rows of V002 (citing r13) and of V003_DRAFT (citing r14) sit on their id's first line in both files. The cited lines are identical, and the row keys are `{new_item_id, file, line, declared_in_r13}`.
- **Publication pins.**
  - 114 of 114 `{path, sha256[, bytes]}` pins in the seven publication records match their bytes, and none names a protected path.
  - The pin graph is acyclic: SELECTED V001 → VALIDATION; SELECTED V002 → VALIDATION and SELECTED V001; HASHES V001 → BUILD_PROGRESS, SELECTED V001, SOURCE_DELTA and VALIDATION; HASHES V002 → HASHES V001 and SELECTED V002.

## 5. Findings (final severity; the A115 class is given for each)

### SHOULD_FIX

**R1. The dispatched SELECTED_R14_CX1V001 cannot be sealed; seal from SELECTED_R14_CX1V002.** Closed in the publication; downstream pins pending. A115: NOTE class (fails closed). TESTED. From lens 1 N1 and lens 3 F1.
- **Claim.** V001's IMPL `854cad0d` does not name the r14 sha. So tool 4 v004 refuses any NEW-item list that pins it, with `NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE`. V002 (`6b650ece`, 03:19:19Z) supersedes V001 by sha and changes only the IMPL pin, to `2ba6d12e`, which passes.
- **Fix.** Use V002 only, as A116.1, A117 and A118 already do. Every downstream IMPL pin must be `2ba6d12e`, never `854cad0d`: the NEW-item list (A118: `NEW_ITEM_DISPOSITIONS_V007_COMPLETE.json`), c3v010 and V003.

**R2. Seal-path successors must exist before the seal.** Today each one either refuses r14 or is not final. Open; not in r14. A115: NOTE class (fail closed). FORMAL and TESTED. From lens 3 F2 and F7; ordered by A116.4, A117 and A118.
- **Claim.**
  - (i) The selected pre-stage c3v009 → c3v020 refuses r14 (L272, L365) and pins disclosures V002 and registry V009.
  - (ii) Disclosures V003 is still DRAFT (`21968a07`). It has the A114 row, but not yet the `E_R6_2` row (A116.2) or the N1 spec sha (A117).
  - (iii) Registry V010 is published but not yet selected. C3V010 (`b843587733ea2a532b522c69657dc5aab11cb33771acd3f20a4c4f3656c2331b`) appeared at 04:13Z. In a fenced snapshot it loads under r14 (ACCEPT; I4 = PRODUCED_AFTER_THE_SEAL; 25 producer gates) and is refused by r13 (`PRODUCER_REGISTRY_GATE_RECORDS`). Its I4 entry is one exact `{path, sha256}` pin of `ri33_c3/i4/write_i4_record_c3v001.py` (`4d6263f6…`), with no N1 field (TESTED). Its content is reviewed in Claude4's separate V010 delta (0132), not here.
  - (iv) The NEW-item list successor must pin IMPL V002.
- **Fix.**
  - c3v010 accepts only r14 `f3f9ba7e`, adds `f5adfd11` to the superseded list, and pins V003 final and V010. It may keep the r6 role check of `impl_of_record_r13`.
  - V003 final adds `E_R6_2` as a `root_disclosures` row (R4 lists one more clause it must name) and places the N1 spec sha inside the A114 row's `text`.
  - V010 = V009 + the B0_N3 and B0_RO1 records + `gate_records.I4 = PRODUCED_AFTER_THE_SEAL` + `producers.I4` = the I4 producer pin. C3V010 has this shape and loads under r14 (TESTED snapshot, (iii)); root selects it after its own delta review.

**R3. The C2T N1 spec sha has no field in r14's registry schema.** Ruled by A117; open until V003 final. A115: class (a) for V010, as 0134 says, and none for r14, which needs no change. TESTED. From lens 2 S2.
- **Claim.** A114.3 and 0651 put the sha "in V010's I4 entry". In schema C2V003:
  - an extra key in the producer pin is refused with `PRODUCER_REGISTRY_PRODUCERS`;
  - a top-level key is refused with `PRODUCER_REGISTRY_UNKNOWN_KEYS`;
  - a dict for `gate_records.I4` is refused with `PRODUCER_REGISTRY_GATE_RECORDS`;
  - a sha list in `gate_records.I4` makes the genuine I4 record `RECORD_DEFECT …A67_N2:I4`, so the reading is NO_RUN.

  A117 moves the pin into V003's A114 row. Tool 4 accepts it there only inside the row's `text`.
- **Caveat on 0134's alternative.** Registering the spec file as a second `producers.I4` pin does load. But it makes the spec file an accepted I4 producer: a record naming it as producer reads PASS (TESTED). A117's choice avoids this.
- **Fix.** V003 final carries the sha in the A114 row text. In V010, `gate_records.I4` must be exactly the token and `producers.I4` exactly `[{path, sha256}]` of the I4 producer. The C3V010 snapshot already has that shape (R2(iii)). Root verifies the N1 spec from bytes at launch (A117).

**R4 (new in this synthesis). The E_R6_2 scope in A116.2 misses one r6 clause that r14 contradicts.** Open; for V003. A115: NOTE class (documentation; no reader; no change to any reading). TESTED. Script `prereg_r6_wording_c4v001.py`, output `synthesis/out/prereg_r6_wording_20261019T040941Z.json`.
- **Claim.**
  - The prereg r6 text of record (`d28c95f5`, the file c3v020 L213 pins as `PREREG_TOR`) carries `gates_before_any_T_result.after_seal_marker_policy.text`. It says: "PRODUCED_AFTER_THE_SEAL is accepted only for the nine gates … (A88; r13 GATE_RECORD_AFTER_SEAL_ALLOWED L341 …) … The token is refused for EPS, GQ, LO, LO_NGC, DOUBLING, B0-B3 and the identity gates … and for every other gate (r13)."
  - Under r14 the token is also accepted for I4. A116.2 lists only `seal_slots.compare.rule` and `seal_slots.producer_registry.rule` as outdated r6 wording.
  - No code reads this clause: r14, the six v004 tool files and c3v020 have 0 occurrences of `after_seal_marker_policy` or `gates_before_any_T_result`.
  - Tool 3's text-of-record equality means the clause will be sealed verbatim.
- **Fix.** Root names this clause in V003's E_R6_2 row as well: "the after-seal token set is the nine plus I4 under A114/A116". The clause text stays unedited in the sealed prereg.

### NOTE

**R5. An I4 record is bound only by its producer pin and its own fields.** A115 NOTE: it matters only for non-genuine or misdirected records. TESTED. From lens 2 S1, downgraded from SHOULD_FIX as in 0134; the behaviour is inherited from r13 and outside A114's one-line scope.
- **Claim.** `g_I4` makes no `xr` call. A record naming the registered producer reads PASS when its `parallel_result_sha256` is not the C2T result (crossref `{}`), and when serial equals parallel. (Lens 2 TESTED that SR_K binds pinned states and that SRB_ROT cross-references its run.)
- **Recommendation for the I4-producer review** (Claude4's V010 delta, 0132), and for root:
  - the producer takes N8 from the V007 C2T T-run's registered directory, and N1 from the root-launched companion;
  - it verifies the N1 spec against the V003 pin;
  - it refuses when the two trees are the same, or when their result shas are equal;
  - root checks `parallel_result_sha256` against the manifest's C2T result when the record lands.

**R6. Stale inherited prose.** No behaviour effect. TESTED. From lens 1 N2, lens 2 N1 and lens 3 F3.
- The comment at L332–L334 still reads "…the B-gates, I4) is registered by record sha".
- L1125 (refusal text), L1178 (docstring) and FIELDS V001 L261 cite A88 only.
- The FIELDS V002 preamble discloses this. Correct it in a later round.

**R7. Author test coverage.** TESTED and FORMAL. From lens 1 N3 and N4, lens 2 N4 and lens 3 F4.
- Only `A114_MUST_I4_TOKEN_ACCEPTED` separates r14 from r13.
- No MUST names B0prime_DRY, B0_FA, B0_RO1 or B0_N3. This review TESTED them as refused.
- No author test drives the token through `evaluate_gate`, because `registry_with_records` (L531–L542; L541 replaces a token by a sha set) prevents it.
- The inherited `…ONLY_ON_THE_NINE…` test (L4316) asserts against the module's own set, and its name still says NINE.
- Optional later: an exact ten-gate assertion and an evaluate-path test.

**R8. FIELDS V002 edits the inherited text without saying so.** TESTED. From lens 1 N5 and N6.
- V002 is a new 6-line preamble, then the r13 explanation with its "SHA256 from bytes" block removed (it pinned 0629 `ca8606b0`, r13 `f5adfd11`, r12 FIELDS `5cc95a06` and SOURCE_DELTA `f87a921d`). "The inherited field specification follows verbatim." becomes "## Current generated contract". FIELDS V001 follows exactly.
- The harness FIELDS test (L5210–L5211) only checks r14 against its own V001. The independent check is §3: r13 regen equals r12, and r14 regen equals V001.
- The seal tools read no FIELDS file; tool 3 cites "FIELDS r12" field names only.

**R9. Hygiene of copied files.** TESTED. From lens 1 N7 and lens 3 F5.
- `r14/tests_kmax_tail_compare_c2v007_r13_cx3v001.py` (`b00e533a`) carries r13's harness name, but it is the failed v001 r14 harness. It differs from `998e0c2e` only at L5210–L5211.
- `r14/tools/author_entry_cx3v001.py` (`9bccb5fa`) differs from r13's (`83b34341`) only in the harness path. It was never used: AUTHOR_EXIT_V002 calls the guard directly, and `out/author_cx3v001` does not exist.
- The four record/mutation tools differ from r13 by path substitution only, and `run_checks` and the guard (`fc69b438`) are identical. The IMPL does not mention the substitutions.

**R10. Unpinned evidence.** TESTED. From lens 1 N8.
- `out/author_v002/TEST_SUMMARY.json` (`42c4961f8af24836d7da99ba699802a150b06bd68e931b544ed81a42e1a558e1`) is pinned nowhere. It shows 718/718, script `f3f9ba7e` and tests `998e0c2e`, which agrees with the pinned stdout `d8ccd0be`.
- The v001 guard logs and the real and mutation stdout are also unpinned.
- HASHES says its scope is not exhaustive.

**R11. Tool 4's NEW-item IMPL check is a substring test.** Any pinned file containing the sha passes, SELECTED V001 included. TESTED. Tamper-robustness for a later tool version. From lens 3 F6.

**R12. Disclosure constraints, confirmed.** TESTED. From lens 3 F7 and A116.4.
- E_R6_1 stays byte-identical and keeps naming the r13 IMPL. The succession goes in V003 rows.
- The sealed prereg must keep r6's rule wording verbatim, because tool 3 requires it.
- No v004 tool checks the compare slot value against the rule text.

**R13. C-08 wording.** TESTED. From lens 1 N10 and lens 3 F8.
- The 19 rows are correct for r13 and for r14.
- But `c08_confirmation` says each id is "carried as a [NEW-n] tag", while only `[NEW-52]` is ever bracketed, first at L1106. Wording only.

**R14. Root chronology.** TESTED, except the 03:14Z mtime, which is a lens observation. From lens 1 N9 and lens 2 N5, plus this stage. Root's stamps are forward-dated:
- A114's header says 03:35Z, but BUILD_PROGRESS cites "0651/A114" at 03:15:27Z, and Claude4 0129, posted at 03:15:42Z, cites A114 as read in V006.
- Dispatch 0651 says "UTC 03:36Z", but it was acked by sha at 03:15:42Z; its file mtime is 03:14Z.
- 0652 says 03:32Z, with mtime 03:28Z.
- A116 says 03:58Z, with mtime 03:53:56Z.
- A117 says 04:05Z, with mtime 04:00:44Z, read at 04:01:09Z.
- A118 says 04:10Z, with mtime 04:06:50Z.
- V003_DRAFT (mtime 03:19Z) says C-08 was checked at "~03:45Z".

None of this affects "before any T result". Root should stamp from `date -u`.

**R15. `evaluate_v007` with no 'I4' key passes group 1.** `gates.get(g, {})` treats an absent key as not MISSING. The behaviour is inherited and identical in r13. The CLI cannot reach it:
- the full decision path (L5830) calls `read_gates` with no `names`, so it evaluates `ALL_GATES` (L5528–L5531);
- the only partial call (L5788, `names=['I1T', 'B0']`) is in the validity-only branch, which writes VALIDITY_ONLY.json and returns before any reading.

Direct callers must pass every gate. FORMAL here; lens 2 TESTED it. From lens 2 N2.

**R16. A partial or placeholder I4 file reads NO_RUN, not INCOMPLETE.** It fails closed. The manifest should name the I4 record only after the producer has finished writing it. TESTED (§3). From lens 2 N3.

## 6. Lens findings: merged, dropped, corrected; root entries during this stage

- **Mapping.**
  - Lens 1: N1→R1, N2→R6, N3/N4→R7, N5/N6→R8, N7→R9, N8→R10, N9→R14, N10→R13.
  - Lens 2: A-a to A-d are confirmations, folded into §3. S1→R5, S2→R3, N1→R6, N2→R15, N3→R16, N4→R7, N5→R14.
  - Lens 3: F1→R1, F2→R2, F3→R6, F4→R7, F5→R9, F6→R11, F7→R12 and R2(ii), F8→R13.
- **Nothing was refuted.**
- **Severity changes.**
  - Lens 2 S1: SHOULD_FIX → NOTE. Under A115 it affects only non-genuine or misdirected records, and it is inherited; this matches 0134.
  - Lens 1 N1: NOTE → SHOULD_FIX, as R1, because a seal tool refuses the dispatched selection.
  - R4 is new.
- **Corrections to the lens texts** (none changes a result):
  - Lens 3 says "all 26 gates"; its probe iterates `ALL_GATES`, which has 25 entries (TESTED).
  - Lens 3 lists c3v020 L218/L377 among the r13 bindings. Those role-pin r6's stored `impl_of_record_r13`, which still holds; only L272/L365 refuse r14.
  - The lens counts of constants (207 vs 206) and of definitions (231 vs 209 code objects) differ only in method. Both find that only `GATE_RECORD_AFTER_SEAL_ALLOWED` differs.
- **Root entries appended while this stage ran**, each read from V006 bytes:
  - **A116:** the compare slot is r14 with SELECTED V002 and IMPL V002; erratum E_R6_2; c3v010 ordered. This resolves R1's choice and orders R2(i).
  - **A117:** r14 is the compare of record, on Claude3 0124 and Claude4 0134; the N1 spec pin moves to V003. This resolves R3.
  - **A118:** NEW-30 and NEW-44 ruled; "r14 stays as reviewed"; the NEW-item list's compare_impl is IMPL V002, consistent with R1.

  None of them conflicts with this review.

## 7. TESTED, FORMAL, UNTESTED

- **TESTED.**
  - Everything in §1 to §4 not marked FORMAL. The fenced runs are `run_20261019T040256Z` (126/126 checks), `prereg_r6_wording_20261019T040941Z` (4/4) and the C3V010 load snapshot `v010_load_20261019T041505Z`.
  - The bash and Python checks on named files: the guard is identical; the entry tool is path-only and unused; the rmi tools are path-only; TEST_SUMMARY; the author log's MUST lines.
- **FORMAL.**
  - The reading code at L4539–L4572, and `read_gates` at L5528–L5531 with its three CLI call sites (L5788, L5812, L5830).
  - c3v020's L272, L365, L222, L241, L271, L218 and L377, read and not executed.
  - Tool 2's slot check (L120–L124).
  - Tool 3 never reads a `rule` key.
  - The harness's `registry_with_records` L541.
  - RI-33's "once the runs exist" (ROOT_ITEMS_R6 L38, a recommendation line).
  - A114's text unchanged since 03:20Z (lens, by eye).
- **UNTESTED.**
  - Not reviewed here:
    - the I4 producer `write_i4_record_c3v001.py`, whose bytes the loader only hashed;
    - the N1 spec;
    - the content of V010, which was only loaded;
    - V003 final, c3v010 and the NEW-item list successor, which are not published.
  - The I4 run pair and any real I4 record.
  - Tool 4 `build()` on real slots.
  - Tool 2 `run()` in this stage (lens 3 TESTED it).
  - `evaluate_v007` in this stage (lens 2 TESTED it).
  - The author 718, real-record 70 and mutation 96 suites, which were not re-run (AUTHOR-RUN; logs checked).
  - Any production or scientific execution.

## 8. Evidence of this stage (paths under `review_compare_r14_c4/`)

| Path | sha256 / note |
|---|---|
| `tools/fence_c4v002.py`, `tools/run_fenced_c4st2.py` | `c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5`, `fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25` (byte-identical copies, `cmp`) |
| `synthesis/scripts/synth_checks_c4v003.py` (the run of record) | `4917ebc6551bf7474eb1c3595d0424a765d7499548f2349925e76871c09d204f` |
| `synthesis/out/run_20261019T040256Z/SYNTH_CHECKS_C4.json` (126/126) | `72b79fe0a64b5cf0917a884788058caba3cc61a6d0ede776e33a039e437d0639` |
| `synthesis/out/run_20261019T040256Z.stdout.txt` / `.stderr.txt` (fence 8/8, 15/15, `blocked_after_selftest: []`) | `5defb1d1c36a9b5d6d61be9c5db96144d3d1368b7bcf8db8212e8e3a4fe9ffb6` / `b38ae4e67da9136b61ac139c09c2bded78983e85854e9fdc166c756ec3e2a281` |
| `synthesis/scripts/prereg_r6_wording_c4v001.py` / its output `synthesis/out/prereg_r6_wording_20261019T040941Z.json` | `ff89aac0ba718e0fbf854d68b00e13e54df25784b81fd8db1fe8a797d7d9c872` / `3e015dc343996d25ee04be456fb72a6b91edc8fea225d88507de7ee1730b06a0` |
| `synthesis/scripts/v010_load_c4v001.py` / its output `synthesis/out/v010_load_20261019T041505Z.json` | `65b4f7aec0a4b95129cfc3e0f04fc53e8502ad8e85e43835185d38c0d43c7b03` / `8e259ba243a31a1632f28383e8830712aeee56a0fa6c2b922c643ed4b8086c83` |
| earlier runs, kept | see below |

- **`run_20261019T035845Z`** stopped at S0 on the V006 pin (63e7802f → 3d4cbe56).
- **`run_20261019T040027Z`** used `synth_checks_c4v001.py` `bd8ab946`. It scored 122/123. Its one FAIL was my probe's wrong expected code for the r13 control of the pre-stage check: SELECTED V002 carries r13's path in `supersedes_selected_source`, so the refusal comes from the `selected_source` equality instead. v002 fixed that.
- **`run_20261019T040101Z`** used v002 `b6793d1c`. It stopped at S0 on V006 (→ 963f4bf1).
- **v003** keeps V006 out of the stop pins and pins the A114 section instead.
- `synth_checks_c4v001.py` was edited in place between `run_20261019T035845Z` and `run_20261019T040027Z` (the V006 re-pin and the A116/S11 checks), so its final bytes `bd8ab946` are what the second run executed. The other script versions are separate files.
- `HASHES_REVIEW_COMPARE_R14_C4V001.txt` is written last and lists every file here, this review included.

## 9. Conduct

- **Writes.** Only inside `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_compare_r14_c4`, as new files: `PARTIAL.md`, which was appended to; `tools/`; `synthesis/`; this review; and the HASHES file. No lens file and no author file was edited. Nothing was deleted, moved or sent over the network.
- **Execution.**
  - r13 and r14 ran only in-process under fence_c4v002, compiled from their sha-verified bytes, on synthetic producers, records and registries.
  - Tool 4's `new_items_codes` and `manual_disclosures_form_codes`, and tool 3's `blank_slot_values`, were called in-process.
  - No driver, production comparator, seal-tool CLI or `--validity-only` was run, and nothing was launched.
  - Heavy runs used `taskpolicy -b`, the thread variables set to 1, and `python3 -I -B`.
- **Protected data.**
  - No NGC3198 target or observed-velocity data, `runs_ext`, C5H or `UVT_*` run output was opened, listed or stat-ed.
  - The c3v020 script text that names the C5H directory was read as text only.
  - Inside `r14/out/`, these were read:
    - named author logs: AUTHOR_EXIT_V002.json, `author_v002/TEST_SUMMARY.json` and `author_v002.stdout.txt`;
    - the evidence files the publication records pin, hashed by exact path for the 114-pin check (54 distinct paths). These include 24 `out/author_guard_v002/GUARD_*.json` logs, the real and mutation guard logs, `real_v001.json` and `MUTATION_R13.json`. None of the paths carries a protected word, and nothing was refused by the fence.
    - One `test -e` checked the absent `out/author_cx3v001`.
  - Neither `r14/out/` nor `author_guard_v002/` was listed. The inert C5H stand-in directory that the author guard created inside `author_guard_v002/` was not touched.
- **Searches and listings.**
  - grep ran on named files only, with no recursive content search.
  - The two registry loads (V009, and the C3V010 snapshot) hashed their pinned producer and comparator files read-only, under the fence. None of those paths carries a protected word.
  - One-level `ls` was run on `seal_assembly_c3/` (with `c3v009_prestage/` and `root_inputs/`), `producer_registry_c3/` and its `out/`, `v007_final_prereg_c4/` (with `r6/`, `r5/case_block/`, `seal_tools_v004/` and `seal_tools_v004/tools/`), `v007_compare_c2/r12`, `r13` and `r14`, `FROM_CLAUDE4/`, `FROM_CODEX/` and this review folder.
  - An explicit `stat -f` was run only on the V006 decision file.
  - The only walk was a no-follow walk of this review folder: 0 symlinks, 0 hard links and 0 protected-name paths.
- **Shas and times.** Every sha was pasted from `shasum` or from script output. Times come from `date -u`.
