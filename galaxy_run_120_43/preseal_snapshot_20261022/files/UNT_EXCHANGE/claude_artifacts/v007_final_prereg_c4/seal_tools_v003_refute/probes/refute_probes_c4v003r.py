# Claude4 seal tools v003 REFUTER (stage REFUTE; folder seal_tools_v003_refute). Bypass and regression probes, run from inside a work copy
# of the published v003 suite's main() so that they reuse its fixtures (ns = main()'s locals, gl = the test module's globals). Every file
# created here is an exclusive create inside the suite's run folder (the suite's own audit hook and fence_c4v002 enforce it). Every
# dispositions, revision and frozen-variant text is SYNTHETIC REFUTER text, not root's. Nothing is launched; no compare is run.
# Each probe records: id, lens, what, expect, verdict, codes, notes, bypass (True = the tool PASSED / built a record where the D-05 rule
# says it must not), detail.
import copy, hashlib, json, os, re, sys, unicodedata
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4')
R6 = EX / 'r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json'
R6_SHA = 'd28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9'
R6_READ = EX / 'r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md'
V005_FINAL = 'c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1'
SEL_R6 = EX / 'r6/SELECTED_R6_C4V001.json'
SEL_R6_SHA = '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0'
R5_READ = EX / 'r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md'
TXT = 'SYNTHETIC REFUTER TEXT (Claude4 v003 refuter): not root text'


def run(ns, gl):
    C, T1, T3, T4, G = gl['C'], gl['T1'], gl['T3'], gl['T4'], ns['G']
    rd = Path(ns['run'])
    xw, xwb, disp, cli, A = gl['xw'], gl['xwb'], ns['disp'], gl['cli'], ns['A']
    text_of_record, sealed_prereg_for, full_set, args_for, use = (ns['text_of_record'], ns['sealed_prereg_for'], ns['full_set'], ns['args_for'],
                                                                   ns['use'])
    FB, frozen, RC0, RC0s, COV, NMAX, SECS = ns['FB'], ns['frozen'], ns['RC0'], ns['RC0s'], ns['COV'], ns['NMAX'], ns['SECS']
    f_62, f_62u, tor_62, tor_62u, TOR, sp, slots_p, sc, a, D0 = (ns['f_62'], ns['f_62u'], ns['tor_62'], ns['tor_62u'], ns['TOR'], ns['sp'],
                                                                 ns['slots_p'], ns['sc'], ns['a'], ns['D0'])
    reviewed, reviewed13, sR, slots, newl, newl13, B, template, dsha = (ns['reviewed'], ns['reviewed13'], ns['sR'], ns['slots'], ns['newl'],
                                                                         ns['newl13'], ns['B'], ns['template'], ns['dsha'])
    pin, rpin, edited, with_section = gl['pin'], gl['rpin'], gl['edited'], gl['with_section']
    EDIT62, R12, DRIVER, PKT, OPEN_ADD, BUILD_V007 = gl['EDIT62'], gl['R12'], gl['DRIVER'], gl['PKT'], gl['OPEN_ADD'], gl['BUILD_V007']
    sub = rd / 'refuter'
    out = []
    n_ = [0]

    def nm(stem):
        n_[0] += 1
        return 'R%03d_%s' % (n_[0], re.sub(r'\W+', '_', stem))

    def codes(r):
        return [f['code'] for f in (r or {}).get('failures', [])]

    def notes(r):
        return sorted({x['code'] for x in (r or {}).get('notes', [])})

    def put(pid, lens, what, expect, verdict, cds, nts=(), bypass=False, detail=''):
        out.append({'id': pid, 'lens': lens, 'what': what, 'expect': expect, 'verdict': verdict, 'codes': list(cds), 'notes': list(nts),
                    'bypass': bool(bypass), 'detail': detail})

    def t1(pid, lens, what, res, expect_pass, detail=''):
        v = res['verdict']
        put(pid, lens, what, 'PASS' if expect_pass else 'REFUSE', v, codes(res), notes(res), bypass=(v == 'PASS' and not expect_pass), detail=detail)
        return res

    def acopy(base, **over):
        b = A()
        b.__dict__.update(base.__dict__)
        b.__dict__.update(over)
        return b

    def t4build(pid, lens, what, b, expect_record, detail=''):
        r, t = T4.safe_build(b)
        v = 'RECORD_BUILT' if t is not None else r['verdict']
        put(pid, lens, what, 'RECORD_BUILT' if expect_record else 'REFUSE (no record)', v, codes(r), notes(r), bypass=(t is not None and not expect_record),
            detail=detail)
        return r, t

    def tor_for(fz, stem, **kw):
        return text_of_record(nm('tor_' + stem) + '.json', ptb=str(fz), **kw)

    def fzfile(stem, raw):
        return xwb(sub / nm(stem) / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', raw)

    use(TOR)
    # ===================== A. bare names via every entry point (expected: refused)
    r, t = T4.safe_build(acopy(a, covered_later='A%d' % NMAX))
    put('A1', 'bare names', 'tool 4 API: covered_later is a bare string, not a list', 'REFUSE (no record)', 'RECORD_BUILT' if t else r['verdict'], codes(r),
        bypass=t is not None)
    r = T3.run(slots_p, sp, TOR, frozen=frozen, covered_later=('',), dispositions=D0, text_of_record_addendum=RC0s, reviewed=reviewed, sealed_compare=sc)
    t1('A2', 'bare names', 'tool 3 API: covered_later=("",) (one empty name)', r, False)
    base1 = ['--prereg', str(sp), '--frozen', str(frozen), '--addendum-at-text-of-record', RC0s, '--dispositions', D0[0], '--dispositions-sha', D0[1]]
    for pid, extra in (('A3', ['--covered-later']), ('A4', ['--', '--covered-later', COV[0]]), ('A5', ['--covered-later='])):
        rc, so, se = cli(T1.main, base1 + extra)
        try:
            cds = [f['code'] for f in json.loads(so).get('failures', [])]
        except ValueError:
            cds = ['<no JSON verdict>']
        put(pid, 'bare names', 'tool 1 CLI argv tail %r' % (extra,), 'REFUSE COVERED_LATER_BARE_NAMES_REFUSED', 'PASS' if rc == 0 else 'REFUSE(rc=%r)' % rc, cds,
            bypass=(rc == 0))
    rc, so, se = cli(T4.main, ['--check-admission-config', '/nonexistent.json', '--seal-record', '/nonexistent.json', '--covered-later', COV[0]])
    put('A6', 'bare names', 'tool 4 admission-mode CLI with --covered-later', 'REFUSE (exit 2, stdout empty)', 'rc=%r stdout=%r' % (rc, so[:40]),
        [f['code'] for f in json.loads(se).get('failures', [])] if se.strip().startswith('{') else [se[:80]], bypass=(rc == 0))
    rc, so, se = cli(T3.main, ['--slots', str(slots_p), '--prereg', str(sp), '--text-of-record', str(TOR), '--covered-later', 'A1'])
    put('A7', 'bare names', 'tool 3 CLI with --covered-later A1', 'REFUSE', 'PASS' if rc == 0 else 'REFUSE(rc=%r)' % rc,
        [f['code'] for f in json.loads(so).get('failures', [])] if so.strip().startswith('{') else [so[:80]], bypass=(rc == 0))

    # ===================== B. changed_text: PV-D05-1 variants (0640 says a generic string never satisfies the substring test)
    old62 = SECS[62][0][1]                                         # RC0's A62 = FB's A62 (RC0 lacks only A<NMAX>)
    assert T1.sections(RC0.read_bytes())[62][0][1] == old62
    new62 = T1.sections(f_62.read_bytes())[62][0][1]

    def shortest_new(new, old):
        for L in range(1, 40):
            for i in range(0, len(new) - L + 1):
                s = new[i:i + L]
                if s not in old:
                    try:
                        return s.decode('utf-8')
                    except UnicodeDecodeError:
                        continue
        return None
    sn = shortest_new(new62, old62)
    r = T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, nca={'A62': sn}), text_of_record_addendum=RC0s)
    t1('B1', 'changed_text', 'C-01 A62 edit disposed no_change_after_change with the SHORTEST new excerpt %r (%d bytes): a contentless fragment' % (sn, len(sn.encode())),
       r, False, detail='README L61 / tool 1 header: "a generic string never passes"; the substring test accepts any new fragment')
    r = T1.run(tor_62u, f_62u, None, dispositions=disp(f_62u, later=COV, nca={'A62': 'é'}), text_of_record_addendum=RC0s)
    t1('B2', 'changed_text', 'the NFC A62 edit disposed with changed_text = one character "\\u00e9" (absent from the old A62)', r, False)
    ws = next(w for w in ('\t', '\n\n\n', '   ', ' ', '​') if w.encode('utf-8') not in old62)
    f_ws = fzfile('A62_edit_with_new_whitespace', edited(FB, 62, 'SYNTHETIC REFUTER EDIT INSIDE A62:%sthe A62 rule now reads otherwise. %s\n' % (ws, TXT)))
    tor_ws = tor_for(f_ws, 'A62_ws')
    r = T1.run(tor_ws, f_ws, None, dispositions=disp(f_ws, later=COV, nca={'A62': ws}), text_of_record_addendum=RC0s)
    t1('B3', 'changed_text', 'a substantive A62 edit disposed with a WHITESPACE-ONLY changed_text %r (non-empty, new, absent from old)' % ws, r, False,
       detail='0640/task rule: changed_text "non-empty"; whitespace-only is not refused (why_no_prereg_effect and reason are stripped, changed_text is not)')
    tail = new62[-24:].decode('utf-8', 'replace')
    r = T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, nca={'A62': tail + '## A63:'}), text_of_record_addendum=RC0s)
    t1('B4', 'changed_text', 'changed_text spanning the A62/A63 section boundary', r, False)
    r = T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, nca={'A62': EDIT62[:30].upper()}), text_of_record_addendum=RC0s)
    t1('B5', 'changed_text', 'changed_text in another case than the bytes', r, False)
    r = T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, nca={'A62': EDIT62[:30].replace(' ', ' ')}), text_of_record_addendum=RC0s)
    t1('B6', 'changed_text', 'changed_text with NBSP for spaces (a whitespace normalization trick)', r, False)

    # ===================== C. reasons and why_no_prereg_effect that are "non-empty after strip" but carry nothing
    for pid, z in (('C1', '​'), ('C2', '﻿'), ('C3', '⁠'), ('C4', '\x00'), ('C5', '­')):
        r = T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o, z=z: o['entries'][0].update(reason=z)), text_of_record_addendum=RC0s)
        t1(pid, 'reason', 'L row A%d no_change whose reason is only %s (U+%04X, category %s)' % (NMAX, unicodedata.name(z, 'NUL'), ord(z), unicodedata.category(z)),
           r, False, detail='Python str.strip() keeps it, so the reason is "non-empty after strip" yet empty to a reader')
    r = T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(reason=' 　')), text_of_record_addendum=RC0s)
    t1('C6', 'reason', 'control: reason NBSP + ideographic space (Unicode whitespace) refuses', r, False)
    r = T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, nca={'A62': EDIT62[:30]}, mutate=lambda o: o['entries'][1].update(
        why_no_prereg_effect='​')), text_of_record_addendum=RC0s)
    t1('C7', 'reason', 'CH row A62 no_change_after_change (correct changed_text) whose why_no_prereg_effect is only U+200B', r, False)
    D_zw = disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(reason='​'))
    rr, tt = t4build('C8', 'reason', 'tool 4 end to end: the L row reason is only U+200B', acopy(a, dispositions=D_zw), False)
    if tt:
        led = json.loads(tt).get('later_entry_dispositions') or {}
        out[-1]['detail'] = 'record built; its later_entry_dispositions.content.entries[0].reason = %r' % ((led.get('content') or {}).get('entries', [{}])[0].get('reason'),)

    # ===================== D. prereg_revision: self-reference and non-revisions (rule: an existing pinned file, not the prereg under check)
    tb = tor_62.read_bytes()
    cp1 = xwb(sub / (nm('prereg_copy_plus_newline') + '.json'), tb + b'\n')
    r = T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, revised=['A62'], mutate=lambda o: o['entries'][1].update(prereg_revision=pin(cp1))),
               text_of_record_addendum=RC0s)
    t1('D1', 'prereg_revision', 'revised A62 whose prereg_revision is the prereg under check plus one trailing newline (same JSON, new sha)', r, False)
    cp2 = xw(sub / (nm('prereg_reserialized') + '.json'), json.dumps(json.loads(tb), indent=2, sort_keys=True) + '\n')
    r = T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, revised=['A62'], mutate=lambda o: o['entries'][1].update(prereg_revision=pin(cp2))),
               text_of_record_addendum=RC0s)
    t1('D2', 'prereg_revision', 'revised A62 whose prereg_revision is the same prereg re-serialized (indent 2, sorted keys)', r, False)
    D_tor = disp(frozen, revised=COV, mutate=lambda o: o['entries'][0].update(prereg_revision=pin(TOR)))
    r = T3.run(slots_p, sp, TOR, frozen=frozen, dispositions=D_tor, text_of_record_addendum=RC0s, reviewed=reviewed, sealed_compare=sc)
    t1('D3', 'prereg_revision', 'tool 3: L row A%d revised whose prereg_revision is the TEXT OF RECORD itself (tool 1 there checks the sealed prereg)' % NMAX, r, False)
    rr, tt = t4build('D4', 'prereg_revision', 'tool 4 end to end: L row revised, prereg_revision = the text of record (the sealed prereg\'s own text)',
                     acopy(a, dispositions=D_tor), False)
    if tt:
        rv = ((json.loads(tt).get('later_entry_dispositions') or {}).get('content') or {}).get('entries', [{}])[0].get('prereg_revision')
        out[-1]['detail'] = 'record built; recorded prereg_revision %r == text of record pin: %s; record prereg = the sealed prereg %s' % (
            rv, rv == pin(TOR), C.sha(sp)[:8])
    for pid, ref, what in (('D5', pin(f_62), 'the frozen copy itself'), ('D6', pin(RC0), 'the read copy'), ('D7', pin(OPEN_ADD), 'the open V005 addendum')):
        r = T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, revised=['A62'], mutate=lambda o, ref=ref: o['entries'][1].update(prereg_revision=ref)),
                   text_of_record_addendum=RC0s)
        t1(pid, 'prereg_revision', 'revised A62 whose prereg_revision is %s (a pinned file that is not a prereg)' % what, r, False,
           detail='class disclosed by Codex1 0093 and README L65 (mechanical pin only)')
    lnk = sub / (nm('symlink_to_prereg') + '.json')
    os.symlink(str(tor_62), str(lnk))
    r = T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, revised=['A62'], mutate=lambda o: o['entries'][1].update(
        prereg_revision={'path': str(lnk), 'sha256': C.sha(lnk)})), text_of_record_addendum=RC0s)
    t1('D8', 'prereg_revision', 'control: prereg_revision is a symlink to the prereg (resolved path and sha both catch it)', r, False)

    # ===================== E. bytes outside every "## A<n>:" section (r5 section_rule): a non-entry heading or the preamble
    i63 = FB.index(b'\n## A63:') + 1
    f_e1 = fzfile('A62_correction_heading', FB[:i63] + ('## A62 (correction): %s. The A62 rule now reads otherwise.\n\n' % TXT).encode() + FB[i63:])
    r = T1.run(tor_for(f_e1, 'E1'), f_e1, None, dispositions=disp(f_e1, later=COV), text_of_record_addendum=RC0s)
    t1('E1', 'non-entry bytes', 'frozen copy = read-copy bytes + a "## A62 (correction): ..." section inserted before "## A63:"; only the usual L row', r, False,
       detail='changed_sections=%r dispositions_required=%r' % (r.get('changed_sections'), r.get('dispositions_required')))
    iN = FB.index(b'\n## A%d:' % NMAX) + 1                          # the closed V005 has no final newline: insert before the newest heading line
    for pid, head in (('E2', '## A107 :'), ('E3', '## A107.'), ('E4', '##  A107:'), ('E5', '## a107:'), ('E6', '## A107 —')):
        f_e = fzfile('later_' + pid, FB[:iN] + ('%s %s: a later ruling that changes the prereg.\n\n' % (head, TXT)).encode('utf-8') + FB[iN:])
        r = T1.run(tor_for(f_e, pid), f_e, None, dispositions=disp(f_e, later=COV), text_of_record_addendum=RC0s)
        t1(pid, 'non-entry bytes', 'a later ruling under the near-miss heading %r (no entry section changes); dispositions name only A%d' % (head, NMAX), r, False,
           detail='later_entries=%r dispositions_required=%r changed_sections=%r' % (r.get('later_entries'), r.get('dispositions_required'), r.get('changed_sections')))
    f_e2e = fzfile('later_E2e_eof', FB + ('\n## A107 : %s: a later ruling appended at the end.\n' % TXT).encode('utf-8'))
    r = T1.run(tor_for(f_e2e, 'E2e'), f_e2e, None, dispositions=disp(f_e2e, later=COV), text_of_record_addendum=RC0s)
    t1('E2e', 'non-entry bytes', 'the same appended at EOF (A%d, an L entry, gains a newline; its row pins that section); the A107 text is in no section' % NMAX,
       r, False, detail='later_entries=%r dispositions_required=%r' % (r.get('later_entries'), r.get('dispositions_required')))
    f_e7 = fzfile('preamble_ruling', ('%s: a preamble ruling that changes the prereg.\n' % TXT).encode() + FB)
    r = T1.run(tor_for(f_e7, 'E7'), f_e7, None, dispositions=disp(f_e7, later=COV), text_of_record_addendum=RC0s)
    t1('E7', 'non-entry bytes', 'a ruling added to the preamble (before "## A47:")', r, False, detail='README L237 / build B-N2 disclose the preamble only')
    # E8: tool 4 end to end, with the open V005 modelled as equal to the E2 variant (a SYNTHETIC r12 copy citing it, as the suite's A90 case)
    f_e8 = fzfile('later_E8_for_tool4', FB[:iN] + ('## A107 : %s: a later ruling that changes the prereg.\n\n' % TXT).encode() + FB[iN:])
    rv8 = R12.read_bytes().decode('utf-8').splitlines(keepends=True)
    ic = [i for i, l in enumerate(rv8) if l.startswith('ADDENDUM_V005_CITED = ')]
    assert len(ic) == 1
    rv8[ic[0]] = 'ADDENDUM_V005_CITED = %r   # SYNTHETIC REFUTER copy: models the open V005 equal to the E8 variant\n' % str(f_e8)
    rev8 = xw(sub / (nm('reviewed_r12_copy_citing_E8') + '.py'), ''.join(rv8))
    impl8 = xw(sub / (nm('IMPL_STANDIN_E8') + '.md'), '# SYNTHETIC REFUTER IMPL stand-in for the test copy %s\n' % C.sha(rev8))
    newl8 = xw(sub / (nm('NEW_ITEMS_E8') + '.json'), dict(json.loads(newl.read_bytes()), compare_impl=pin(impl8)))
    plan8p, cmd8p = sub / (nm('BOUND_PLAN_E8') + '.json'), sub / (nm('BOUND_COMMAND_E8') + '.txt')
    B.bind(str(template), str(DRIVER), dsha, str(f_e8), C.sha(f_e8), str(plan8p), str(cmd8p))
    plan8 = json.loads(plan8p.read_bytes())
    s8 = copy.deepcopy(slots)
    s8['frozen_addendum'] = dict(plan8['frozen_addendum'])
    s8['launch_packet'] = {'build': dict(slots['launch_packet']['build']), 'bound_plan': rpin(plan8p), 'bound_command': rpin(cmd8p)}
    s8['admission_entry'] = {'launcher': dict(plan8['launcher']), 'guard': dict(plan8['guard'])}
    s8['compare_reviewed_source'] = rpin(rev8)
    tor8 = tor_for(f_e8, 'E8')
    sl8, sp8, sc8 = full_set(nm('E8'), s8, tor8, src=rev8)
    use(tor8)
    rr, tt = t4build('E8', 'non-entry bytes', 'tool 4 end to end: frozen = open V005 (modelled) with a "## A107 :" later ruling; dispositions name only A%d' % NMAX,
                     args_for(sl8, sp8, tor8, sc8, frozen=str(f_e8), dispositions=disp(f_e8, later=COV), reviewed=str(rev8), new_item_list=str(newl8)), False)
    if tt:
        out[-1]['detail'] = 'record built: frozen_addendum %s (holds the A107 text); later_entry_dispositions rows %r' % (
            json.loads(tt)['frozen_addendum']['sha256'][:8], [x['entry'] for x in json.loads(tt)['later_entry_dispositions']['content']['entries']])
    use(TOR)

    # ===================== F. TOCTOU (simulated: the bytes a check reads are swapped between two reads of one path)
    D62nc = disp(f_62, later=COV)                                   # computed before the patch (sections of the real A62-edited file)
    real_rb = Path.read_bytes
    tgt = os.path.realpath(str(f_62))
    cnt = [0]

    def swapped(self):
        if os.path.realpath(str(self)) == tgt:
            cnt[0] += 1
            if cnt[0] >= 2:
                return FB                                               # the A62 edit "is undone" after the first (sha) read
        return real_rb(self)
    Path.read_bytes = swapped
    try:
        r = T1.run(tor_62, f_62, None, dispositions=D62nc, text_of_record_addendum=RC0s)
    finally:
        Path.read_bytes = real_rb
    t1('F1', 'TOCTOU', 'tool 1: the frozen file (A62 edited, no A62 row) is swapped back to the unedited bytes after its first read (the sha read)', r, False,
       detail='reads of the frozen path: %d; pinned frozen sha %s (the edited file %s); r2 has the same three reads' % (
           cnt[0], (r.get('pins_verified', {}).get('frozen') or {}).get('sha256', '')[:8], C.sha(f_62)[:8]))
    r0 = T1.run(tor_62, f_62, None, dispositions=D62nc, text_of_record_addendum=RC0s)
    t1('F1c', 'TOCTOU', 'control: the same call without the swap refuses (ENTRY_SECTION_CHANGED)', r0, False)
    slf, spf, scf = full_set(nm('toctou'), slots, TOR)
    real_t3 = T4.T3.run
    seen3 = {}

    def t3_then_swap(*aa, **kk):
        res3 = real_t3(*aa, **kk)
        seen3['pin'] = (res3.get('pins_verified') or {}).get('sealed_prereg')
        d = json.loads(Path(spf).read_bytes())
        d['status'] = d.get('status', '') + ' [SYNTHETIC REFUTER: changed after tool 3 checked this file]'
        with open(spf, 'w') as f:                                     # a refuter work fixture in the run folder, rewritten on purpose
            f.write(json.dumps(d, indent=1, ensure_ascii=False) + '\n')
        return res3
    T4.T3.run = t3_then_swap
    try:
        rr, tt = T4.safe_build(args_for(slf, spf, TOR, scf))
    finally:
        T4.T3.run = real_t3
    recp = (json.loads(tt).get('prereg') if tt else None) or {}
    put('F2', 'TOCTOU', 'tool 4: the sealed prereg changes after tool 3 (and tool 1 inside it) verified it, before the record is built',
        'REFUSE (no record)', 'RECORD_BUILT' if tt else rr['verdict'], codes(rr), bypass=bool(tt) and recp.get('sha256') != (seen3.get('pin') or {}).get('sha256'),
        detail='tool 3 verified sealed_prereg %s; the record pins prereg %s; the sealed compare pins V007_PREREG_SHA256 of the checked bytes, so the '
               'compare itself refuses the swapped prereg at run time (r13 L5674-5676, FORMAL)' % (
                   ((seen3.get('pin') or {}).get('sha256') or '')[:8], (recp.get('sha256') or '')[:8]))

    # ===================== G. strict JSON gaps in the dispositions file
    d0t = Path(D0[0]).read_bytes().decode('utf-8')
    reason0 = json.dumps(json.loads(d0t)['entries'][0]['reason'], ensure_ascii=False)
    Dsur = disp(None, raw=d0t.replace(reason0, '"\\ud800 SYNTHETIC REFUTER"', 1))
    r = T1.run(sp, frozen, None, dispositions=Dsur, text_of_record_addendum=RC0s)
    t1('G1', 'strict JSON', 'reason holds a lone-surrogate escape "\\ud800 ..." (valid JSON, no UTF-8 form): tool 1', r, False)
    rr, tt = t4build('G1b', 'strict JSON', 'the same file through tool 4', acopy(a, dispositions=Dsur), False)
    for pid, raw, what in (('G2', d0t.encode('utf-8').replace(b'SYNTHETIC TEST ROW', b'SYNTHETIC \xff TEST ROW', 1), 'an invalid UTF-8 byte inside a string'),
                           ('G3', d0t.encode('utf-8').replace(b'SYNTHETIC TEST ROW', b'SYNTHETIC \xed\xa0\x80 TEST ROW', 1), 'a UTF-8-encoded surrogate'),
                           ('G4', d0t.replace('"entry"', '"\\u0065ntry": "A1", "entry"', 1).encode('utf-8'), 'a duplicate key spelled with an escape'),
                           ('G5', (d0t.rstrip('\n') + ' {}\n').encode('utf-8'), 'trailing data after the object'),
                           ('G6', d0t.encode('utf-32'), 'UTF-32 bytes'),
                           ('G7', d0t.replace(reason0, '1e400', 1).encode('utf-8'), 'a reason that is an overflowing number (1e400 -> inf)')):
        r = T1.run(sp, frozen, None, dispositions=disp(None, raw=raw), text_of_record_addendum=RC0s)
        t1(pid, 'strict JSON', what, r, False)

    # ===================== I. REAL prereg r6 d28c95f5 (SELECTED, Codex1 0109) with its read copy c01b3c51 and a FROZEN-named copy of the closed V005
    assert C.sha(R6) == R6_SHA and C.sha(R6_READ) == V005_FINAL and C.sha(SEL_R6) == SEL_R6_SHA and C.sha(OPEN_ADD) == V005_FINAL
    assert R6_SHA in SEL_R6.read_bytes().decode('utf-8')
    F6 = fzfile('r6_frozen_copy', R6_READ.read_bytes())
    R6R = str(R6_READ)
    r = T1.run(R6, F6, None, (), True, None, R6R)
    t1('I1', 'REAL r6', 'tool 1 on prereg r6 with its read copy and a FROZEN-named copy of c01b3c51, no dispositions file (dry run only for path_to_be)', r, True,
       detail='dispositions_required=%r changed_sections=%r later_entries=%r notes=%r' % (r.get('dispositions_required'), r.get('changed_sections'),
                                                                                         r.get('later_entries'), notes(r)))
    r = T1.run(R6, F6, None, (), False, None, R6R)
    put('I2', 'REAL r6', 'the same without the dry-run flag: the only refusal is the CLAUDE2 path_to_be', 'REFUSE exactly FROZEN_PATH_NOT_PATH_TO_BE', r['verdict'],
        codes(r), notes(r), bypass=False, detail='exact match: %s' % (sorted(set(codes(r))) == ['FROZEN_PATH_NOT_PATH_TO_BE']))
    r = T1.run(R6, F6, V005_FINAL, (), True, disp(F6, rows=[]), R6R)
    t1('I3', 'REAL r6', 'r6 with --expect-frozen-sha c01b3c51 and a dispositions file with entries []', r, True)
    r = T1.run(R6, F6, None, (), True, None, str(R5_READ))
    t1('I4', 'REAL r6', 'r6 given r5\'s read copy 70a48f51', r, False)
    r = T1.run(R6, F6, None, ('A106',), True, None, R6R)
    t1('I5', 'REAL r6', 'r6 with a bare covered_later A106', r, False)
    F6b = F6.read_bytes()
    for pid, n in (('I6', 47), ('I7', 62), ('I8', 81), ('I9', 106)):
        fz = fzfile('r6_edit_A%d' % n, edited(F6b, n, 'SYNTHETIC REFUTER EDIT INSIDE A%d: %s.\n' % (n, TXT)))
        r = T1.run(R6, fz, None, (), True, None, R6R)
        t1(pid, 'REAL r6', 'C-01 on r6: an edit inside A%d with no dispositions file' % n, r, False, detail='codes %r' % sorted(set(codes(r))))
        if n == 62:
            r2_ = T1.run(R6, fz, None, (), True, disp(fz, nca={'A62': 'SYNTHETIC REFUTER EDIT INSIDE A62'}), R6R)
            t1('I7c', 'REAL r6', 'control: that A62 edit with a correct no_change_after_change row passes', r2_, True)
            r3_ = T1.run(R6, fz, None, (), True, disp(fz, later=['A62']), R6R)
            t1('I7p', 'REAL r6', 'PV-D05-1 on r6: that A62 edit with plain no_change', r3_, False)
    i63r = F6b.index(b'\n## A63:') + 1
    i106r = F6b.index(b'\n## A106:') + 1
    for pid, raw, what in (('I10', F6b[:i63r] + ('## A62 (correction): %s. The A62 rule now reads otherwise.\n\n' % TXT).encode() + F6b[i63r:],
                            'a "## A62 (correction):" section inserted before "## A63:"'),
                           ('I11', F6b[:i106r] + ('## A107 : %s: a later ruling that changes the prereg.\n\n' % TXT).encode() + F6b[i106r:],
                            'a later ruling under "## A107 :" inserted before "## A106:"'),
                           ('I11e', F6b + ('\n## A107 : %s: a later ruling appended at the end.\n' % TXT).encode(),
                            'a later ruling under "## A107 :" appended at EOF (A106, a table row, gains a newline)'),
                           ('I12', ('%s: a preamble ruling.\n' % TXT).encode() + F6b, 'a preamble ruling')):
        fz = fzfile('r6_' + pid, raw)
        r = T1.run(R6, fz, None, (), True, None, R6R)
        t1(pid, 'REAL r6', 'r6 vs a frozen copy = c01b3c51 + %s, no dispositions file' % what, r, False,
           detail='frozen %s != c01b3c51; dispositions_required=%r changed_sections=%r' % (C.sha(fz)[:8], r.get('dispositions_required'), r.get('changed_sections')))
        r = T1.run(R6, fz, V005_FINAL, (), True, None, R6R)
        t1(pid + 'x', 'REAL r6', 'the same with --expect-frozen-sha c01b3c51 (root\'s A106.3 byte equality)', r, False)
    # tool 3 and tool 4 on r6 (slots: the REAL BUILD_V007 set of the suite with r13 as the reviewed source). r6x = r6 with ONE leaf changed:
    # seal_slots.frozen_addendum.path_to_be = the suite's FROZEN-named copy of the closed V005 (the real CLAUDE2 path is never created here).
    d6 = json.loads(R6.read_bytes())
    d6['seal_slots']['frozen_addendum']['path_to_be'] = str(Path(frozen).resolve())
    R6x = xw(sub / (nm('r6x_path_to_be_in_run_folder') + '.json'), json.dumps(d6, indent=1, ensure_ascii=False) + '\n')
    s6 = copy.deepcopy(sR)
    s6['compare_reviewed_source'] = rpin(reviewed13)
    sl6, sp6, sc6 = full_set(nm('r6x'), s6, R6x, src=reviewed13)
    T3.TEXT_OF_RECORD_SHA = T3.TEXT_OF_RECORD_PENDING
    r = T3.run(sl6, sp6, R6x, frozen=frozen, dispositions=None, text_of_record_addendum=R6R, reviewed=str(reviewed13), sealed_compare=sc6,
               text_of_record_sha=C.sha(R6x))
    t1('I13', 'REAL r6', 'tool 3 on r6x (r6 with path_to_be moved into the run folder), r13 reviewed source, read copy c01b3c51, no dispositions file', r, True,
       detail='codes %r; passthrough dispositions_required=%r later_entry_dispositions=%r' % (sorted(set(codes(r))), (r.get('passthrough') or {}).get(
           'dispositions_required'), (r.get('passthrough') or {}).get('later_entry_dispositions')))
    sl6b, sp6b, sc6b = full_set(nm('r6_real_bytes'), s6, R6, src=reviewed13)
    r = T3.run(sl6b, sp6b, R6, frozen=frozen, dispositions=None, text_of_record_addendum=R6R, reviewed=str(reviewed13), sealed_compare=sc6b,
               text_of_record_sha=C.sha(R6))
    put('I14', 'REAL r6', 'tool 3 on the real r6 bytes d28c95f5: refuses only because the frozen copy is not at the CLAUDE2 path_to_be',
        'REFUSE exactly FROZEN_SLOT_NOT_PATH_TO_BE, T1:FROZEN_PATH_NOT_PATH_TO_BE', r['verdict'], codes(r), notes(r), bypass=False,
        detail='exact match: %s' % (sorted(set(codes(r))) == ['FROZEN_SLOT_NOT_PATH_TO_BE', 'T1:FROZEN_PATH_NOT_PATH_TO_BE']))
    r13x = T3.run(sl6, sp6, R6x, frozen=frozen, dispositions=None, text_of_record_addendum=R6R, reviewed=str(reviewed13), sealed_compare=sc6,
                  text_of_record_sha=C.sha(R6x))
    pt6 = r13x.get('passthrough') or {}
    km6 = xw(sub / (nm('KEY_MAP_OF_THE_REAL_CASE_BLOCK') + '.json'), {'schema': T4.KEY_MAP_SCHEMA, 'key_equivalence_map': pt6.get('key_equivalence_map'),
                                                                      'note': 'SYNTHETIC REFUTER input: the key map of the real case block 76309ae3'})
    sh6 = C.sha(sc6)
    mode6 = pt6.get('route_a_mode')
    g6 = ns['body_file'](ns['gates_body'](sh6, route_a_mode=mode6))
    v6 = ns['body_file'](ns['validity_body'](sh6, route_a_mode=mode6), 'VALIDITY_ONLY.json')
    rr, tt = t4build('I15', 'REAL r6', 'tool 4 on r6x with r13 (reviewed copy) and an r13-sealed compare, no dispositions file (key map and B6 bodies of the real '
                     'case block, route-A mode %r)' % mode6, args_for(
        sl6, sp6, R6x, sc6, dispositions=None, addendum_at_text_of_record=R6R, reviewed=str(reviewed13), new_item_list=str(newl13), text_of_record_sha=C.sha(R6x),
        key_equivalence_map=str(km6), gates_only_output=str(g6), validity_only_output=str(v6)), True)
    rec6 = json.loads(tt) if tt else {}
    if tt:
        out[-1]['detail'] = 'later_entry_dispositions=%r addendum_at_text_of_record=%r text_of_record=%r' % (
            rec6.get('later_entry_dispositions'), rec6.get('addendum_at_text_of_record'), rec6.get('text_of_record'))
        seal6 = xw(sub / (nm('SEAL_RECORD_R6X') + '.json'), tt)
        cfg6 = {'schema': C.ADMISSION_SCHEMA, 'authority': dict(C.AUTHORITY), 'seal': pin(seal6), 'prereg': rec6['prereg'], 'compare': rec6['compare'],
                'build': rec6['build'], 'producer_allowlist': rec6['admission_allowlist']}
        cfg6p = xw(sub / (nm('ROOT_SEAL_ADMISSION_R6X') + '.json'), cfg6)
        t1('I16', 'REAL r6', 'admission check on the r6x SEAL_RECORD (real BUILD_V007 15 rows)', T4.check_admission_config(cfg6p, seal6), True)
        G.CONFIG = cfg6p
        os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfg6p)
        try:
            G.admission(str(PKT / 'route_a_token_launcher_cx1v007.py'))
            og = 'admitted'
        except BaseException as e:
            og = '%s: %s' % (type(e).__name__, e)
        put('I17', 'REAL r6', 'the real guard v008 admission() on that config (CONFIG patched to the run folder; nothing started)', 'admitted', og, [], bypass=False)
        b7t = BUILD_V007.read_bytes().decode('utf-8')
        allow7 = rec6['admission_allowlist']
        olds = {p: h for h, p in re.findall(r'^([0-9a-f]{64})  (/\S+\.py)$', b7t, re.M) if h[:8] in ('9fbdb0ca', '500f8b6a')}
        for pid, al, what in (('J1', dict(allow7, **olds), '17 rows (+ the superseded writers 9fbdb0ca, 500f8b6a)'),
                              ('J2', {p: h for h, p in C.build_allowlist((PKT / 'BUILD_V006.md').read_bytes().decode('utf-8'))}, 'BUILD_V006\'s 15 rows')):
            cw = xw(sub / (nm('W7S1_' + pid) + '.json'), dict(cfg6, producer_allowlist=al))
            t1(pid, 'W7-S1', 'admission check, r6x record, config with %s' % what, T4.check_admission_config(cw, seal6), False)
        q = json.loads(tt)
        txt_dup = json.dumps(q, indent=1, sort_keys=True).replace('\n "sealed_by": {', '\n "sealed_by": {"identity": "WRONG"},\n "sealed_by": {', 1) + '\n'
        sdup = xw(sub / (nm('SEAL_RECORD_DUP_SEALED_BY') + '.json'), txt_dup)
        cdup = xw(sub / (nm('ROOT_SEAL_ADMISSION_DUP') + '.json'), dict(cfg6, seal=pin(sdup)))
        t1('J3', 'B8', 'a SEAL_RECORD with two sealed_by keys (first wrong, last = AUTHORITY): v003 check', T4.check_admission_config(cdup, sdup), False)
        G.CONFIG = cdup
        os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cdup)
        try:
            G.admission(str(PKT / 'route_a_token_launcher_cx1v007.py'))
            og = 'admitted'
        except BaseException as e:
            og = '%s: %s' % (type(e).__name__, e)
        put('J3g', 'B8', 'the same record under the real guard v008 (json.loads keeps the last key)', 'admitted (guard is looser; v003 stricter)', og, [])
    G.CONFIG = rd / 'NO_CONFIG_AFTER_REFUTER.json'
    os.environ.pop('UNT_ROOT_ADMISSION_SHA256', None)
    use(TOR)
    end_sha = C.sha(OPEN_ADD)
    put('Z1', 'environment', 'the open V005 is still c01b3c51 after the refuter probes', 'c01b3c51', end_sha[:8], [], bypass=False)
    res = {'schema': 'UNT_V003_REFUTER_PROBES_C4R001', 'run_dir': str(rd), 'probe_module_sha256': C.sha(__file__), 'r6': {'path': str(R6), 'sha256': R6_SHA},
           'r6_read_copy': {'path': str(R6_READ), 'sha256': V005_FINAL}, 'selected_r6': {'path': str(SEL_R6), 'sha256': SEL_R6_SHA},
           'tools': {k: C.sha(Path(T1.__file__).parent / k) for k in ('seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py',
                                                                      'check_slot_fill_c4v003.py', 'build_seal_record_c4v003.py', 'print_driver_build_record_c4v003.py')},
           'probes': out, 'bypasses': [p['id'] for p in out if p['bypass']]}
    with open(rd / 'REFUTER_PROBES_C4R001.json', 'x') as f:
        json.dump(res, f, indent=1)
    for p in out:
        print('PROBE %-5s %-16s bypass=%-5s %-24s %s :: %s' % (p['id'], p['lens'], p['bypass'], p['verdict'][:24], p['what'][:110], ','.join(sorted(set(p['codes'])))[:200]))
    print('PROBES', len(out), 'bypasses', res['bypasses'])
    return res
