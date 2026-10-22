Thu Oct 22 11:08:38 UTC 2026 | helper started: read-only reader map for relocation-with-custody; folder created; reading 10 named files
Thu Oct 22 11:10:48 UTC 2026 | ORCH c2v005 read: resolve_work_dir L631-669, WORK_DIR.json L3023-3061, SF1 L3113-3132, Cache.open/_verify L2302-2456, classify L2718-2786, collect_evidence L1376-1519, cache_id L1774-1779
Thu Oct 22 11:12:11 UTC 2026 | campaign_c2v005 + core r12_c4 + wrapper q5b1 read (call_%04d formation L174/L199; cache_id wrapper L134-137; ledger genesis L370-373, chain L400-417; certificate_check L162-309; reingest L638-664; reingest_invalid L667-705)
Thu Oct 22 11:12:54 UTC 2026 | entry h3_campaign_entry r12_c4 + h3_accept_call read (locate L153-172, finished L175-191, accept L237-315); next acceptance_handoff_c2v004
Thu Oct 22 11:13:18 UTC 2026 | acceptance_handoff_c2v004 read (accept_call L336-559: resolve(strict) L340, Store.put resolved refs L247-255, tailstates in call dir L227-241); next storage_check
Thu Oct 22 11:13:39 UTC 2026 | storage_check read (move_check L107-138; refusal reasons L110, L123, L132, L134; always NOT_MOVABLE for a call dir inside work dir); next roster_builder (6129 lines, grep first)
Thu Oct 22 11:15:13 UTC 2026 | roster_builder: read helpers L207-262, CommandSnapshot L2418-2475, _receipt L2711-2849 + L4652-4726, _terminal L4786-4892, _assemble L4894-5326, custody L3283-3470 + L5336-5386; next phase1_snapshot + G26
Thu Oct 22 11:16:15 UTC 2026 | roster_builder done (pass serve log realpath L1525-1535, VALIDITY_FIELDS incl served L1712, step7 compare L1847); next g26_freeze
Thu Oct 22 11:18:37 UTC 2026 | line numbers verified for ORCH, wrapper, core, entry, accept step, handoff, storage_check; next roster/G26 line verification then write map
Thu Oct 22 11:20:49 UTC 2026 | all readers mapped; collecting last line refs, then writing READER_MAP_HELPER.md
Thu Oct 22 11:23:59 UTC 2026 | final line refs collected (ORCH classify/verify, WRAP cert checks, HANDOFF, RB, G26); writing READER_MAP_HELPER.md now
Thu Oct 22 11:27:02 UTC 2026 | READER_MAP_HELPER.md body written
Thu Oct 22 11:28:26 UTC 2026 | line-number corrections applied to READER_MAP_HELPER.md (10 fixes after spot-check)
Thu Oct 22 11:29:05 UTC 2026 | second precision pass applied (4 fixes); map final, preparing hand-back
Thu Oct 22 11:29:27 UTC 2026 | DONE. NOTE: line refs in the earlier PARTIAL lines were provisional; the verified refs are in READER_MAP_HELPER.md (sha256 08e35a54a9d1f64b122285b42e4fb8dddebea18797207c97022fb2789f3e8610, 171 lines)
