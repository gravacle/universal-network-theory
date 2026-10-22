# Claude4 (dispatch 0583), revision r4: successor of c4v003. Reads the r3 draft (07397846) from bytes and integrates V005 A81 (the
# rulings on RI-19..RI-26) as recorded clause edits; adds the one item still open (RI-27: the prereg <-> compare pin cycle). Every pin is
# computed from bytes; a missing file or a sha prefix that differs is refused. Seal slots stay PENDING. Output: r4/ (no overwrite).
# Usage: TS=$(date -u +%Y-%m-%dT%H:%M:%SZ) [DRY_DIR=...] python3 -I -B make_v007_final_draft_c4v004.py
import copy, hashlib, json, os, re
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE'); CA = EX / 'claude_artifacts'
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
OUT = CA / 'v007_final_prereg_c4' / 'r4'
R3 = CA / 'v007_final_prereg_c4/r3/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R3.json'
R3_SHA = '073978466df470bda3dccfa53da619df9835aeee6a7f217bbb2802045da6bf49'
V005 = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
V005_READ_R4 = '82b567bfa945ab5bcc9075c23e5925397a7dcaa74096bb20f739dcf253957e86'   # pasted from shasum at 17:51Z (adds A81 to r3's 4b937ec1)
COMPARE_R10 = CA / 'v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin(p, prefix=None):
    p = Path(p)
    if not p.is_file():
        raise SystemExit('missing ' + str(p))
    h = sha(p)
    if prefix and not h.startswith(prefix):
        raise SystemExit('pin prefix %s != %s for %s' % (prefix, h[:8], p))
    return {'path': str(p), 'sha256': h}


def cl(text, *sources):
    return {'text': text, 'sources': list(sources)}


def main():
    ts = os.environ['TS']
    if sha(R3) != R3_SHA:
        raise SystemExit('r3 pin')
    doc = json.loads(R3.read_text())
    v005_observed = sha(V005)
    vt = V005.read_text()
    if '## A81:' not in vt:
        raise SystemExit('V005 addendum lacks A81')
    later = re.findall(r'^## (A8[2-9]|A9\d)\b', vt, re.M)
    disp0583 = pin(EX / 'FROM_CODEX/0583_2026-10-18_claude4_prereg_r4_with_A81.md', '854e1898')
    cmp_src = COMPARE_R10.read_text()
    for needle in ('V007_PREREG_SHA256 = None', 'the seal record then pins this script', 'PIN_ADDENDUM_V005 = None', 'PIN_DRIVER_BUILD_RECORD = None'):
        if needle not in cmp_src:
            raise SystemExit('compare r10 evidence missing: ' + needle)
    changes = []

    def node(path):
        d = doc
        for k in path:
            d = d[k]
        return d

    def upd(path, text=None, add=(), append=None, why=''):
        c = node(path)
        if text is not None:
            c['text'] = text
        if append:
            c['text'] = c['text'].rstrip() + ' ' + append
        for s in add:
            if s not in c['sources']:
                c['sources'].append(s)
        changes.append({'clause': '.'.join(str(x) for x in path), 'kind': 'rewritten' if text is not None else ('extended' if append else 'sources'),
                        'added_sources': list(add), 'why': why})

    def log(clause, kind, srcs, why):
        changes.append({'clause': clause, 'kind': kind, 'added_sources': list(srcs), 'why': why})

    slots = doc['seal_slots']
    # RI-19 + RI-25 + RI-24 + RI-27: the publication order (seal_record_requirements[4])
    sr = doc['seal_record_requirements']
    if not sr[4]['text'].startswith('Publication order (0561'):
        raise SystemExit('r3 seal_record_requirements[4] is not the publication-order clause')
    upd(('seal_record_requirements', 4), text=
        'Order of record (0561; A81 RI-19, the erratum to A72 H-01, whose "its sha goes in the seal record" is superseded). At seal assembly root exclusively creates, in '
        'this order: (1) the frozen copy of the V005 addendum, after the last pre-seal entry (A81 RI-26); (2) with the driver chosen (A72), and under r6 a fresh, empty, '
        'root-created cache directory (A81 RI-24), the bound plan and command written by the build-only binder (0576; A81 RI-25); (3) the sealed prereg text, this draft '
        'with every seal slot filled; (4) the sealed compare (RI-27, as drafted); (5) the SEAL_RECORD, naming the sealed prereg sha (the first pin), the sealed compare, '
        'the driver, the frozen addendum, the bound plan and command shas and, under r6, the cache directory; (6) the ROOT_SEAL_ADMISSION config, pinning the SEAL_RECORD\'s '
        'full sha; (7) a separate SEAL_ADMISSION_RECEIPT naming both, posted in a numbered root packet. The RUNBOOK verifies the published config sha before invoking any '
        'source; records embed the config, seal and compare shas. No file is edited after it is created. Root verifies the bound plan and command shas from bytes '
        'immediately before running the command.', add=('A81 RI-19', 'A81 RI-24', 'A81 RI-25', 'A81 RI-26'), why='A81 RI-19/24/25/26')
    upd(('seal_record_requirements', 5), text=
        'RI-10\'s adoption rule applies to every NEW item the final compare IMPL declares (adopted as text if stricter on adoption and gap-filling, rejected if looser); the '
        'IMPL lists each one with its disposition and its MUST_FAIL tests (A75), and the seal record quotes that list.', add=('A81 RI-20',), why='A81 RI-20')
    if not sr[2]['text'].startswith('The compare pins at seal: V007_PREREG_SHA256'):
        raise SystemExit('r3 seal_record_requirements[2] is not the compare-pin clause')
    upd(('seal_record_requirements', 2), append='These seal-time pins (with PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK and PIN_PRODUCER_REGISTRY) are the only lines in '
        'which the sealed compare may differ from the reviewed source of the final round; the prereg names the reviewed source, the SEAL_RECORD names the sealed '
        'compare (RI-27, as drafted).', add=('RI-27 (draft)',), why='acyclic prereg/compare pins')
    sr.append(cl('Any A-entry after A81 that touches this text needs a successor revision or an explicit no-change note in the seal record; the seal check verifies that every '
                 'A-entry this text cites is present in the frozen bytes.', 'A81 RI-26'))
    log('seal_record_requirements[%d]' % (len(sr) - 1), 'new', ['A81 RI-26'], 'A81 RI-26')
    # slots
    slots['frozen_addendum']['rule'] = ('Root exclusively creates the immutable copy at seal assembly, after the last pre-seal entry; the seal check verifies that every A-entry '
                                        'this text cites is present in the frozen bytes; its path and sha go to the binder and into the SEAL_RECORD. The frozen addendum must not '
                                        'cite the sealed prereg\'s sha (draft shas may be cited), or the pins would cycle (RI-27).')
    slots['frozen_addendum']['sources'] += ['A81 RI-26', 'RI-27 (draft)']
    slots['driver']['rule'] = ('Path and full sha from bytes at seal; the SEAL_RECORD names it; the launcher refuses a plan whose driver differs (C4-S1, guard v008 / launcher '
                               'v007); every identity run and every T-run carries driver_sha256 equal to it, and no T-run starts before the seal names it (A67 N1, extended '
                               'to T-runs by A81 RI-24).')
    slots['driver']['sources'] += ['A81 RI-24']
    slots['compare']['rule'] = ('The final compare round: r11, or the fix round r12 if r11\'s rechecks force one (A80). V007 seals on the round whose three recheck lenses and '
                                'whose distinct reviews of record (Claude3 and Codex2) report 0 blocking (A81 RI-20). This slot holds that round\'s reviewed source, with its '
                                'seal-time pin constants still unset (`None`; the bytes the reviews examined), path and sha. The sealed compare (V007_PREREG_SHA256 set to the sealed '
                                'prereg sha, plus PIN_ADDENDUM_V005, PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK and PIN_PRODUCER_REGISTRY) is created after the sealed '
                                'prereg and is named only in the SEAL_RECORD; it may differ from the reviewed source only in those pin lines (RI-27, as drafted; '
                                'compare r10 L166: "set at the seal (the seal record then pins this script)").')
    slots['compare']['sources'] += ['A81 RI-20', 'RI-27 (draft)', 'compare r10 L150-166']
    slots['identity_comparator']['rule'] = ('The c2v007-lineage round whose own check and Codex2\'s review report 0 blocking (A81 RI-21); c2v004-c2v006 are superseded and not '
                                            'used at the seal.')
    slots['identity_comparator']['sources'] += ['A81 RI-21']
    slots['identity_gate_records']['rule'] = ('Only the identity-comparator slot round\'s outputs on the identity runs of the driver in the driver slot (Z2, Z2_OFF_RO1, '
                                              'B0prime_RERUN), using the A59 replace-mode tokens derived from that driver, with the raw successor-custody check; each carries '
                                              'driver_sha256 = the driver slot (A81 RI-21, A67 N1).')
    slots['identity_gate_records']['sources'] += ['A81 RI-21']
    slots['launch_packet']['rule'] = ('BUILD_V005 (46bc5b5d) with the bound plan and command that the build-only binder writes from the selected template, the chosen driver and '
                                      'the frozen addendum (exclusive create). The binder runs after the addendum is frozen and the driver is chosen, and before the SEAL_RECORD '
                                      'is written; the SEAL_RECORD names the bound plan and command shas; root verifies both from bytes immediately before running the command. '
                                      'A validate()-level template-equality check is optional and not required (A81 RI-25). The pending r5 template V010 refuses validation by design.')
    slots['launch_packet']['sources'] += ['A81 RI-25']
    c = slots['certificates']
    c['rule'] = ('Root confirms each record of record at seal assembly; every record states source_gas_M_s where it depends on M_s, equal to the case block\'s gas.M_s, which '
                 'must be 128 for DDO. LO_NGC is reported only in V007: the V007 LO_NGC slot takes the LO_NGC record of record that exists at seal assembly; coverage to '
                 '91 gates the NGC N-test compare (step 5), not the V007 seal (A81 RI-23). DOUBLING is one merged record, registered before the seal (A81 RI-22).')
    c['named_candidates_verified_from_bytes']['LO_NGC_91'] = ('NOT_ON_DISK_AT_ASSEMBLY (Codex1 0049). For V007 the slot takes the LO_NGC record of record existing at seal '
                                                              'assembly (A81 RI-23); coverage to 91 gates the NGC N-test compare, not this seal.')
    c['named_candidates_verified_from_bytes']['DOUBLING_merged'] = 'NOT_ASSEMBLED (A81 RI-22: one merged record, both halves, DDO <= tau/20 and NGC <= theta/20)'
    c['sources'] += ['A81 RI-22', 'A81 RI-23']
    slots['cache_directory_r6_only'] = {'value': 'PENDING_ROOT_AT_SEAL_ASSEMBLY (only if A72 adopts r6)', 'rule':
                                        'A fresh, empty directory that root creates and names in the SEAL_RECORD; no pre-warming before the seal (the T-runs populate it, KHI '
                                        'first); every T-run records its cache mode and directory; the compare refuses a T-run whose mode or directory differs from the '
                                        'registered one (A81 RI-24).', 'sources': ['A72', 'A81 RI-24']}
    log('seal_slots', 'slots rewritten', ['A81 RI-20', 'A81 RI-21', 'A81 RI-22', 'A81 RI-23', 'A81 RI-24', 'A81 RI-25', 'A81 RI-26'],
        'A81 slot rules; new slot cache_directory_r6_only')
    # clauses
    upd(('fixed_across_all_cases', 'production_tail', 'tail_table_cache'), append=
        'Under r6 (A81 RI-24): the cache directory is a fresh, empty, root-created directory named in the SEAL_RECORD; there is no pre-warming before the seal (the T-runs '
        'populate the cache themselves, KHI first); every T-run records its cache mode and cache directory, and the compare refuses a T-run whose mode or directory differs '
        'from the registered one; no T-run starts before the seal names the driver, and every T-run\'s driver_sha256 equals the driver slot (extending A67 N1 to T-runs).',
        add=('A81 RI-24',), why='A81 RI-24')
    upd(('fixed_across_all_cases', 'production_tail', 'gas'), append=
        'A81 RI-23 (conditional, adopted): if GQ_NGC at M_s 96 fails anywhere on [2, 91], the NGC gas M_s becomes 128, and LO_NGC and DOUBLING\'s NGC half are recomputed at '
        'that value.', add=('A81 RI-23',), why='A81 RI-23')
    upd(('gates_before_any_T_result', 'DOUBLING'), text=
        'One merged DOUBLING record, registered before the seal (A79 NEW-61) and read by the compare as one gate; both halves must pass (A81 RI-22). DDO half: (w/2, o+4) at '
        'K_big {128, 256} with gas M_s 128, the max change over tau on the static rows of saved C4R3 le3, <= tau_i/20 (A58 RI-03; the DDO half PASSed at 128 and 256, max '
        '4.7e-13 tau, independently recomputed, A73). NGC half: operator e6453d52, K_big 32, the NQ max change over theta, <= theta/20 (declared in A81 by analogy with '
        'RI-03, before any NGC target is opened). It keeps RI-03\'s production-128 rule (A79 NEW-67).', add=('A81 RI-22',), why='A81 RI-22')
    upd(('gates_before_any_T_result', 'LO_NGC'), text=
        'LO_NGC is the readout-coupled share, the quantity the N-tests read (lnN only, metric v002 L76); the field-level indicator is carried as an auxiliary field; the record '
        'carries an honest i1t field. In V007, LO_NGC is reported only (R1 L180): the V007 LO_NGC slot takes the LO_NGC record of record that exists at seal assembly '
        '(A81 RI-23). NGC I1-T of stars + H2 against the T120L fixed source must pass before any NGC N-test is read; the NGC N-tests get their own small compare, and no '
        'NGC N-test is read until LO_NGC, EPS_NGC and GQ_NGC to 91 are all slotted; coverage to 91 gates that NGC N-test compare (step 5), not the V007 seal (A81 RI-23, '
        'A64.2). Shells are keyed on range; a duplicate is a RECORD_DEFECT (A75 A01); an NGC roster with a different range refuses (A79.1).',
        add=('A81 RI-23',), why='A81 RI-23')
    n = doc['ngc3198_N_tests']
    n['reading_gate_A81'] = 'No NGC N-test is read until LO_NGC, EPS_NGC and GQ_NGC to 91 are all slotted; coverage to 91 gates this NGC N-test compare (step 5), not the V007 seal (A81 RI-23).'
    n['sources'] = list(n['sources']) + ['A81 RI-23']
    log('ngc3198_N_tests.reading_gate_A81', 'new', ['A81 RI-23'], 'A81 RI-23')
    # root items
    A81 = {'RI-19': '0561 is the order of record; A81 is the erratum to A72 H-01 (integrated in seal_record_requirements[4])',
           'RI-20': 'adopted: RI-10\'s rule for every NEW item; V007 seals on the round whose three recheck lenses and distinct reviews report 0 blocking',
           'RI-21': 'adopted: the c2v007-lineage round with 0 blocking; records of record only on the driver slot\'s identity runs',
           'RI-22': 'one merged DOUBLING record; NGC half <= theta/20, declared in A81',
           'RI-23': 'adopted (conditional M_s 128 for NGC); LO_NGC in V007 is reported only; coverage to 91 gates the NGC N-test compare, not the V007 seal',
           'RI-24': 'fresh, empty, root-created cache directory named in the SEAL_RECORD; no pre-warming; mode and directory recorded per T-run; T-run driver sha = driver slot',
           'RI-25': 'the SEAL_RECORD names the bound plan and command shas; binder after the freeze and driver choice, before the SEAL_RECORD; template check optional',
           'RI-26': 'adopted: freeze after the last pre-seal entry; seal check verifies cited entries; later entries need a revision or a no-change note'}
    for r in doc['root_items']:
        if r['id'] in A81:
            if r['status'] != 'OPEN':
                raise SystemExit('expected %s open in r3' % r['id'])
            r['status'] = 'RESOLVED: A81 ' + r['id'] + ': ' + A81[r['id']]
    log('root_items', 'resolved', ['A81'], 'RI-19..RI-26 resolved by A81')
    doc['root_items'].append({
        'id': 'RI-27', 'kind': 'CONFLICT (pin cycle)', 'clause': 'seal_slots.compare; seal_record_requirements[2]',
        'issue': '0580 asks the prereg to carry the compare round\'s path and sha as a seal slot, and the prereg also says "the compare pins at seal: V007_PREREG_SHA256 (this '
                 'text once sealed)". The compare carries `V007_PREREG_SHA256 = None`, "set at the seal (the seal record then pins this script)" (compare r10 L166). A prereg '
                 'that names the sealed compare\'s sha and a compare that names the sealed prereg\'s sha cannot both hold. The same cycle would arise if the frozen '
                 'addendum cited the sealed prereg\'s sha, since the prereg names the frozen addendum.',
        'draft': 'the compare slot holds the final round\'s reviewed source (seal-time pins unset, `None`); the sealed compare is created after the sealed prereg and named only in the '
                 'SEAL_RECORD; the frozen addendum cites no sealed-prereg sha.',
        'recommendation': 'RECOMMENDATION ONLY: rule the acyclic order reviewed compare source -> sealed prereg (names that source) -> sealed compare (sets exactly '
                          'V007_PREREG_SHA256, PIN_ADDENDUM_V005, PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK and PIN_PRODUCER_REGISTRY) -> SEAL_RECORD (names the '
                          'sealed prereg and the sealed compare); have the seal check verify that the sealed compare differs from the reviewed source only in those '
                          'lines; and have the frozen addendum cite no sealed-prereg sha.',
        'sources': ['0580 item 2', 'seal_record_requirements[2] (A67 seal-time pins)', 'compare r10 L150-166', 'A81 RI-19', 'A81 RI-26'], 'status': 'OPEN'})
    log('root_items.RI-27', 'new', ['0580', 'compare r10 L166'], 'pin cycle found while ordering the checklist')
    doc['root_items'].sort(key=lambda r: (r['status'] != 'OPEN', r['id']))
    # header
    doc['revision'] = 'r4'
    doc['status'] = ('FINAL DRAFT r4 (NOT SEALED). Assembled by Claude4 (dispatch 0583) from r3 07397846, integrating V005 A81 (the rulings on RI-19 to RI-26; open addendum '
                     'observed %s at assembly). Written before any V007 (tail-corrected) result exists; nothing was launched; C5H, UVT_* and targets were not read. Root fills the '
                     'named seal slots and seals. One root item is open (RI-27, the prereg/compare pin cycle); nothing else is open.' % v005_observed)
    doc['assembly'] = dict(doc['assembly'], utc=ts, dispatch=disp0583, base={'path': str(R3), 'sha256': R3_SHA},
                           rulings_read=dict(doc['assembly']['rulings_read'], V005_addendum_open_observed={'path': str(V005), 'sha256': v005_observed},
                                             V005_addendum_reads=doc['assembly']['rulings_read']['V005_addendum_reads'] + [
                                                 {'read': 'r4 read, 17:51Z: adds A81 only (diff against 4b937ec1)', 'sha256': V005_READ_R4},
                                                 {'read': 'r4 generation (this run)', 'sha256': v005_observed}]))
    doc['decision_pins_pending_at_seal']['V005_addendum_frozen_copy']['entries'] = 'A47-A81; cited by name until frozen'
    doc['cites_by_name'][0] = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM: A47-A81 (open; pinned by its frozen copy, PENDING)'
    if later:
        doc['entries_after_A81_at_assembly'] = later
    doc['supersedes_draft'] = {'path': str(R3), 'sha256': R3_SHA}
    # checklist in root execution order
    check = [
        ('A. Before seal assembly (any order; each must be complete before step B1)', '', ''),
        ('A1. Final compare round (r11, or r12): three recheck lenses and the distinct reviews of record (Claude3, Codex2) report 0 blocking; its IMPL lists every NEW item with disposition and MUST_FAIL tests. Fix its reviewed source (seal-time pins unset, `None`) for the compare slot.', 'PENDING (r11 building)', 'A80; A81 RI-20'),
        ('A2. Identity comparator: the c2v007-lineage round whose own check and Codex2\'s review report 0 blocking.', 'PENDING', 'A81 RI-21'),
        ('A3. A72 decision: r5, or r6 if (a) independent check incl. stale-cache attacks, (b) bitwise equality at K_big 32/128/256 and (c) a measured net saving all hold. r6: BUILD, cascade map and template published.', 'PENDING', 'A72'),
        ('A4. r5 only: CASCADE_MAP_R5_ADDENDUM written (immutable inventory addendum).', 'PENDING', 'A69'),
        ('A5. Identity runs of the chosen driver (Z2, Z2_OFF_RO1, B0prime_RERUN; reruns on r6 with the cache if r6) compared by the A2 round, with A59 replace-mode tokens from that driver and the raw successor-custody check: records of record.', 'PENDING', 'A81 RI-21; A59; A67 N1'),
        ('A6. Successor B0 tool and B0 record rerun (B0-EMPTY rule) on the chosen driver.', 'PENDING (no A-entry records completion)', 'A54; 0530'),
        ('A7. Certificates of record confirmed: EPS_CERT_V006 598c8fa3, LO_CERT_V004_MS128 1c384f76, GQ_CERT_V005_MS128 fbceefe6 (V004 FAIL control); I1T_NGC; the V007 LO_NGC slot takes the LO_NGC record of record existing now (reported only).', 'DDO DONE; root confirms', 'A70; A81 RI-23'),
        ('A8. The merged DOUBLING record (DDO half PASS; NGC half from NQ at K_big 32, <= theta/20), registered.', 'PENDING', 'A81 RI-22; A73'),
        ('A9. Producer registry: producer paths, producer shas, gate-record shas of record (SR_K included).', 'PENDING', 'A62.2; A67 N2; A69.1'),
        ('A10. Key-equivalence map assembled for the seal record.', 'PENDING', 'A48 AMB-13'),
        ('B. Seal assembly (strict order; every file exclusively created; none edited afterwards)', '', ''),
        ('B1. Freeze the V005 addendum: exclusive-create ..._V005_ADDENDUM_FROZEN.md after the last pre-seal entry; verify every A-entry this text cites (A47-A81) is present; any later entry touching this text gets a revision or a no-change note; it cites no sealed-prereg sha.', 'PENDING', 'A81 RI-26; 0576; RI-27'),
        ('B2. Fix the driver path and sha (A3). r6 only: create a fresh, empty cache directory (no pre-warming).', 'PENDING', 'A72; A81 RI-24'),
        ('B3. Run the build-only binder (template for the chosen driver; driver path and sha; frozen addendum path and sha): bound plan and command, exclusive create, under the build folder.', 'PENDING', '0576; A81 RI-25'),
        ('B4. Write the sealed prereg: this text with every seal slot filled from bytes (frozen addendum, driver, compare reviewed source, identity comparator and records, launch packet with bound plan and command, certificates, producer registry; r6 cache directory).', 'PENDING', '0580; A81'),
        ('B5. Create the sealed compare: the A1 reviewed source with exactly the seal-time pins set (V007_PREREG_SHA256 = B4\'s sha, PIN_ADDENDUM_V005, PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK, PIN_PRODUCER_REGISTRY); verify it differs from the reviewed source only in those lines.', 'PENDING', 'RI-27 (draft); A67'),
        ('B6. Run `--gates-only` and `--validity-only --case C5H` with the sealed compare on the real records; keep their output for the SEAL_RECORD; no row value shown.', 'PENDING', 'A46 RA13; A47 I3'),
        ('B7. Exclusive-create the SEAL_RECORD: sealed prereg sha (first pin), sealed compare, driver, frozen addendum, bound plan and command shas, r6 cache directory; B6 output; E5-08; raw successor custody; the NEW-item disposition list; key-equivalence map; no-row-shown statement.', 'PENDING', 'A81 RI-19/25; A62; A59; A58 RI-10'),
        ('B8. Exclusive-create the ROOT_SEAL_ADMISSION config pinning the SEAL_RECORD\'s full sha, prereg, compare and BUILD_V005; its producer_allowlist names exactly the 13 BUILD_V005 sources (launcher v007 and guard v008 by exact path).', 'PENDING', '0561; A78 N2; FORMAT_V004'),
        ('B9. Exclusive-create the SEAL_ADMISSION_RECEIPT naming the config and seal shas; post it in a numbered root packet.', 'PENDING', '0561; A81 RI-19'),
        ('C. Launch (Claude2 only)', '', ''),
        ('C1. Verify the receipt and config against the numbered root packet; export UNT_ROOT_ADMISSION_SHA256 from the published value (never from the local file).', 'PENDING', 'RUNBOOK_V005 step 3'),
        ('C2. Verify the bound plan and command shas from bytes immediately before running the command; run it (ramp-gated; KHI first).', 'PENDING', 'A81 RI-25; A72; 0559'),
        ('Already DONE (preconditions)', '', ''),
        ('Driver r5 built (b5cc62af), dry runs 25/25, Codex3 review PASS_WITH_FINDINGS; a Claude-lineage check (driver_r5/check, 89a6de88) PASS_WITH_FINDINGS.', 'DONE', 'A67; A69'),
        ('B3 gate final PASS (GATE_B3_C4_V002 465cb3c3); PICARD member specs gates_v004 PASS; P128/M_s 128 spec set registered (c7023846); launch packet BUILD_V005 (46bc5b5d) reviewed PASS.', 'DONE', 'R1 B3; A68; A72; A78; Claude4 0079'),
        ('SUPERSEDED', '', ''),
        ('Compare r8 and r10; comparators c2v004-c2v006; r2/r3 checklist orderings.', 'SUPERSEDED', 'A79; A80; A76; this revision'),
    ]
    # write
    out = Path(os.environ['DRY_DIR']) if os.environ.get('DRY_DIR') else OUT
    out.mkdir(parents=True, exist_ok=True)

    def write(name, text):
        p = out / name
        with p.open('x') as f:
            f.write(text)
        return p
    write('KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json', json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    D = ['# Delta r3 → r4 (KMAX_TAIL_PREREG_V007_FINAL_DRAFT)', '', 'Each line is one recorded edit applied to r3 (07397846) by the r4 generator. Source of the rulings: '
         'V005 A81 (open addendum %s).' % v005_observed, '', '| # | clause | kind | added sources | why |', '|---|---|---|---|---|']
    D += ['| %d | `%s` | %s | %s | %s |' % (i + 1, c_['clause'], c_['kind'], '; '.join(c_['added_sources']), c_['why']) for i, c_ in enumerate(changes)]
    write('DELTA_R3_R4.md', '\n'.join(D) + '\n')
    ri = doc['root_items']
    Rr = ['# Root items r4: KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4 (unsealed)', '', 'RI-19 to RI-26 are resolved by A81. One item is open: RI-27. Nothing else is open.', '']
    for r in ri:
        Rr += ['## %s: %s (%s)' % (r['id'], r['kind'], 'OPEN' if r['status'] == 'OPEN' else 'RESOLVED'), '', '- **Status:** %s' % r['status'], '- **Clause:** `%s`' % r['clause'],
               '- **Issue:** %s' % r['issue'], '- **Draft:** %s' % r['draft']]
        if 'recommendation' in r:
            Rr.append('- **Recommendation:** %s' % r['recommendation'])
        Rr += ['- **Sources:** %s' % '; '.join(r['sources']), '']
    write('ROOT_ITEMS_R4.md', '\n'.join(Rr))
    S = ['# SEAL_CHECKLIST r4: V007, in the order root will execute it', '', 'State at assembly (%s). The draft is unsealed; the slots stay PENDING.' % ts, '',
         '| step | state | source |', '|---|---|---|']
    for a, b, c_ in check:
        S.append('| **%s** | | |' % a if not b else '| %s | %s | %s |' % (a, b, c_))
    write('SEAL_CHECKLIST_R4.md', '\n'.join(S) + '\n')
    rows = []

    def walk(prefix, obj):
        if isinstance(obj, dict) and 'text' in obj and 'sources' in obj:
            rows.append((prefix, obj['sources']))
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(prefix + '.' + k if prefix else k, v)
    for sec in ('binding_inputs', 'fixed_across_all_cases', 'pairing_and_decidability_rule', 'gates_before_any_T_result', 'tests', 'decision_rule', 'run_list'):
        walk(sec, doc[sec])
    for o in doc['outcomes_first_applicable']:
        rows.append(('outcomes_first_applicable.%s' % o['outcome'], o['sources']))
    for i, r in enumerate(doc['seal_record_requirements']):
        rows.append(('seal_record_requirements[%d]' % i, r['sources']))
    rows.append(('ngc3198_N_tests', doc['ngc3198_N_tests']['sources']))
    for k, s in doc['seal_slots'].items():
        rows.append(('seal_slots.%s' % k, s['sources']))
    rows.append(('not_v007_text_scope', doc['not_v007_text_scope']['sources']))
    M = ['# Clause → source map, r4: KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4 (unsealed)', '', '| clause | sources |', '|---|---|']
    M += ['| `%s` | %s |' % (k, '; '.join(s)) for k, s in rows]
    write('CLAUSE_SOURCE_MAP_R4.md', '\n'.join(M) + '\n')
    H = ['# KMAX_TAIL_PREREG_V007: final draft r4 (UNSEALED)', '', doc['status'], '', '**Assembly:** Claude4, single author, UTC %s. Base: r3 `%s`. Dispatch 0583 `%s`.' % (
        ts, R3_SHA, disp0583['sha256']), '', 'The full clause text is in the JSON; `CLAUSE_SOURCE_MAP_R4.md` traces every clause; `DELTA_R3_R4.md` lists the A81 edits.', '']
    H.extend(['## Seal slots (root fills at seal assembly; never guessed)', ''])
    for k, s in doc['seal_slots'].items():
        H.append('- **%s**: value `%s`. %s  \n  *Sources: %s*' % (k, s['value'], s['rule'], '; '.join(s['sources'])))
    H.extend(['', '## Seal record requirements', ''])
    for r in doc['seal_record_requirements']:
        H.append('- %s *(%s)*' % (r['text'], '; '.join(r['sources'])))
    H.extend(['', '## Clauses changed in r4', ''])
    for c_ in changes:
        H.append('- `%s` (%s): %s' % (c_['clause'], c_['kind'], c_['why']))
    H.extend(['', '## Root items', '', 'RI-19 to RI-26: RESOLVED by A81. OPEN: RI-27 (see `ROOT_ITEMS_R4.md`). Nothing else is open.', ''])
    write('KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.md', '\n'.join(H) + '\n')
    hrows = ['%s  ./%s' % (sha(p), p.relative_to(out)) for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'HASHES_R4.txt']
    write('HASHES_R4.txt', '\n'.join(hrows) + '\n')
    print('written', out, len(hrows), 'files; V005 observed', v005_observed, '; later entries', later, '; edits', len(changes),
          '; open', [r['id'] for r in ri if r['status'] == 'OPEN'])


if __name__ == '__main__':
    main()
