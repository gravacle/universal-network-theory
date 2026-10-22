# Claude4 r5 helper: derive make_v007_final_draft_c4v005_p3.py from _p2 (dry run dry_gen_2 inspected: correct). Changes: (1) the delta names the
# generator file actually run; (2) delta rows show normalized clause names; (3) entry-table rows lose a doubled period; (4) the registry candidate
# is C3V009 (32ddadcb; Claude3 0087; anticipated by A101; listed in dispatch 0626), with C3V008 as A101's baseline; (5) root item RI-37 on
# Claude3's SR_K producer-pin reading. Anchored edits only (each exactly once); exclusive create.
import difflib, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC, DST = HERE / 'make_v007_final_draft_c4v005_p2.py', HERE / 'make_v007_final_draft_c4v005_p3.py'
t0 = SRC.read_bytes().decode()
t = t0
EDITS = [
    ("'Each line is one recorded edit applied to r4 (e3b6b5b2) by make_v007_final_draft_c4v005.py, with its trace to a ruling (A-entry), a rehearsal defect '",
     "'Each line is one recorded edit applied to r4 (e3b6b5b2) by ' + Path(__file__).name + ', with its trace to a ruling (A-entry), a rehearsal defect '"),
    ("    D += ['| %d | `%s` | %s | %s | %s | %s |' % (i + 1, c['clause'], c['kind'],",
     "    D += ['| %d | `%s` | %s | %s | %s | %s |' % (i + 1, norm(c['clause']), c['kind'],"),
    ("r['section_sha256'], ('%s. Clauses: %s' % (r['scope'], ', '.join(",
     "r['section_sha256'], ('%s. Clauses: %s' % (r['scope'].rstrip('.'), ', '.join("),
    ("            ('registry_c3v007', CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V007.json', '34bbfe40'),\n",
     "            ('registry_c3v007', CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V007.json', '34bbfe40'),\n"
     "            ('registry_c3v009', CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json', '32ddadcb'),\n"
     "            ('validate_r12_c3v009_case_block_of_record', CA / 'producer_registry_c3/out/VALIDATE_R12_C3V009_CASEBLOCK_OF_RECORD.json', '537d1a42'),\n"
     "            ('Claude3_0087', EX / 'FROM_CLAUDE3/0087_2026-10-18_registry-V009-BUILD_V007-producers-final.md', '0f99076e'),\n"
     "            ('dispatch_0626', EX / 'FROM_CODEX/0626_2026-10-18_claude3_codex2_seal_assembly_prestage.md', 'c555ee94'),\n"),
    ("    pr['named_candidates_verified_from_bytes'] = {\n        'C3V008_final_A101': P['registry_c3v008'],\n",
     "    pr['named_candidates_verified_from_bytes'] = {\n"
     "        'C3V009_candidate': dict(P['registry_c3v009'], note=('C3V008 plus BUILD_V007\\'s four post-seal producer pins (SRB_ROT 2757847a; MT, I1T and '\n"
     "                                                            'FLAG_RULINGS 4024d82a) and nothing else (Claude3 0087); on r12 with the case block of '\n"
     "                                                            'record 76309ae3 all 13 registered records PASS and B0_N3, B0_RO1, I4 fail closed '\n"
     "                                                            '(VALIDATE_R12_C3V009_CASEBLOCK_OF_RECORD 537d1a42); anticipated by A101 and listed in '\n"
     "                                                            'dispatch 0626; a record filling B0_N3, B0_RO1 or I4 means a V010')),\n"
     "        'C3V008_final_A101': P['registry_c3v008'],\n"),
    ("    addsrc(pr, ['A88', 'A92', 'A99.5', 'A100', 'A101'])\n",
     "    addsrc(pr, ['A88', 'A92', 'A99.5', 'A100', 'A101', 'Claude3 0087'])\n"),
    ("        ('A9. Producer registry of record: C3V008 (f189cd3f; final under A101; 13 records PASS on r12), then V009 with BUILD_V007\\'s post-seal producers (V6-N4). '\n"
     "         'It carries SR_K by producer pins with PRODUCED_AFTER_THE_SEAL (A88), c2v007r2 and its tokens and the R5_V001 records (A92), B2 C3V003 (A101), the 0598 '\n"
     "         'records, and B0_N3, B0_RO1 and I4 once built (empty slots fail closed).', 'PENDING (V009; Claude3)', 'A62.2; A67 N2; A69.1; A88; A99.5; A101'),\n",
     "        ('A9. Producer registry of record: candidate C3V009 (32ddadcb; Claude3 0087) = C3V008 (f189cd3f, final under A101) plus BUILD_V007\\'s four post-seal '\n"
     "         'producer pins (V6-N4); 13 registered records PASS on r12 with the case block of record. It carries SR_K by producer pins with PRODUCED_AFTER_THE_SEAL '\n"
     "         '(A88), c2v007r2 and its tokens and the R5_V001 records (A92), B2 C3V003 (A101), the 0598 records; B0_N3, B0_RO1 and I4 are empty and fail closed '\n"
     "         '(a record filling one means a V010).', 'CANDIDATE V009; root pins at assembly (RI-37 on the SR_K producer pin)', 'A62.2; A67 N2; A69.1; A88; A99.5; A101'),\n"),
    ("         ['A62.3', 'A67', 'A69']),\n    ]\n",
     "         ['A62.3', 'A67', 'A69']),\n"
     "        ('RI-37', 'PENDING_ROOT_RULING (registry reading)', 'tests.SR_K; seal_slots.producer_registry',\n"
     "         'Claude3 0087 registers only aggregate_records v008 (9794123d) as the SR_K gate-record producer in C3V009; sr_k_static v009 (cc2eb3bb) writes per-state '\n"
     "         'component records (schema UNT_SR_K_STATE_CX1V001), whose custody is a runbook item (r12 review note B-N3). PRODUCER_INDEX_V009_CX3V001 lists both '\n"
     "         'under SR_K. The SR_K clause names both as the sealed pinned producers (A88).', 'unchanged (A88 wording).',\n"
     "         'RECOMMENDATION ONLY: root confirms Claude3\\'s reading (the aggregator alone is the gate-record producer; sr_k_static custody on the producer side, '\n"
     "         'in the RUNBOOK), or rules both into the registry.', ['A88', 'A99.5', 'Claude3 0087']),\n"
     "    ]\n"),
    ("    log('root_items.RI-28..RI-36', 'new', [], ['A81 RI-20', 'A99.1', 'R-10', 'R-09', 'GAP-18', 'GAP-14', 'A99.3', 'D-09', 'GAP-05'], 'open items at r5')\n",
     "    log('root_items.RI-28..RI-37', 'new', [], ['A81 RI-20', 'A99.1', 'R-10', 'R-09', 'GAP-18', 'GAP-14', 'A99.3', 'D-09', 'GAP-05', 'A88'], 'open items at r5')\n"),
]
for old, new in EDITS:
    n = t.count(old)
    assert n == 1, (n, old[:90])
    t = t.replace(old, new)
with open(DST, 'x') as f:
    f.write(t)
d = ''.join(difflib.unified_diff(t0.splitlines(True), t.splitlines(True), SRC.name, DST.name))
print('p3 sha256', hashlib.sha256(DST.read_bytes()).hexdigest(), '| diff lines', len(d.splitlines()))
