# R2-C lens: verify, from source bytes, every NEW entry of round-2 NUMBER_PROVENANCE_R2.json (node radii, node-derived
# values, indices, counts, post numbers) plus the TSR-flag arithmetic of C-1.4 / M-7. Target-free inputs only: the slots
# V003 query block (ids, Rad_text, Rad_unit), the registered GL4 nodes, the K32 N1 record and compare, V005 (snapshot),
# V003, V001 prereg, the round-1 review files and named exchange posts. Writes one JSON (exclusive create) in this lens folder.
# usage: python3 -I -B verify_provenance_r2c.py --out RESULT.json
import argparse, hashlib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_r2c
fence_r2c.install()

A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
X = '/Users/bgm/Research/UNT_EXCHANGE/'
LENS = fence_r2c.LENS
SRC = {
    'slots': (A + 'freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json', 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'),
    'nodes': (A + 'ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json', 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'),
    'n1': (A + 'ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json', '8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70'),
    'cmp': (A + 'ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json', '6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9'),
    'v001': (A + 'miss_reading_prereg_c4/PREREG_MISS_READING_V001.md', '6aecf0cb340b28f911d0e71c1ef3d6aede5e495309cdd40ee44ae9e49e785345'),
    'v003': ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V003_ADDENDUM.md', '5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468'),
    'v005snap': (LENS + '/snapshots/V005_AT_R2C.md', 'cf9bbf19eae3d2fb0262c31c3a0af43ecc2f100b9295c4075a591716b6ebb9dc'),
    'prov_r2': (A + 'miss_reading_prereg_c4/r2/round2/NUMBER_PROVENANCE_R2.json', 'ff6ca9b84384171285abbbc6d072a21346048884e9deff4fa79b0629f52c98bf'),
    'prereg_r2': (A + 'miss_reading_prereg_c4/r2/round2/PREREG_MISS_READING_R2.md', '97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407'),
    'root_r2': (A + 'miss_reading_prereg_c4/r2/round2/ROOT_ITEMS_R2.md', '4907cf019c7bec62da646dc862f6c36c2b3aa03b11b761f36475c1056e968500'),
    'map_r2': (A + 'miss_reading_prereg_c4/r2/round2/CLAUSE_SOURCE_MAP_R2.md', '38cd6852bdc32c240a6935671c82d618da399dd20e7d6adaa5aa2a26cd24f201'),
}
REVIEWS = [A + 'miss_reading_prereg_c4/r2/checks/%s/REVIEW.md' % k for k in ('fidelity', 'targetfree', 'consistency')]
POSTS = {
    '0032': (X + 'FROM_CODEX1/0032_2026-10-18_gq91_pass_and_latest_rulings.md', '3e8c9fc9e65a10791f8ecbda3702556a851391350f06ed013222bd12876ab2f7'),
    '0056': (X + 'FROM_CODEX1/0056_2026-10-18_ngc_k32_complete_n_fail_n1_a66_open.md', '4b67319dddb4799e71420881f6624fdcd1640cd5f560a4adce06cd2030af72aa'),
    '0058': (X + 'FROM_CODEX1/0058_2026-10-18_0603_synthetic_steps6_7_finished.md', 'fc5af8318febd8dd86037d7aeddff9a590ea8e436deb15f002b9c4775c65cea2'),
    '0618': (X + 'FROM_CODEX3/0618_2026-10-18_dispatch0606_carriers_finished.md', '8939c004e4bea1728eed610e4d98b98dffbe4333be1433c539feb16159de60a7'),
    '0550': (X + 'FROM_CODEX/0550_2026-10-18_codex1_N1_consequence_and_claude4_queue_add.md', '5c686ae8fd82cea995fcdd1ed5bff2d0d688514c45582871cb2b97f231b8b457'),
    '0606': (X + 'FROM_CODEX/0606_2026-10-18_claude4_codex3_steps6_7_rough_edges.md', 'dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e'),
    '0071': (X + 'FROM_CLAUDE4/0071_2026-10-18_done-0545-freeze-v003g-PASS.md', None),
}


def rb(p):
    with open(p, 'rb') as f:
        return f.read()


def section(text, n):
    lines = text.split('\n')
    st = [i for i, l in enumerate(lines) if l.startswith('## ')]
    for j, i in enumerate(st):
        if re.match(r'^## A%d:' % n, lines[i]):
            e = st[j + 1] if j + 1 < len(st) else len(lines)
            return '\n'.join(lines[i:e])
    return ''


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    res = {'schema': 'R2C_PROVENANCE_VERIFY_V001', 'sources': {}, 'entries': {}, 'tsr': {}, 'notes': []}
    raw = {}
    for k, (p, h) in SRC.items():
        b = rb(p)
        got = hashlib.sha256(b).hexdigest()
        res['sources'][k] = {'path': p, 'sha256': got, 'expected': h, 'match': got == h}
        raw[k] = b
    slots = json.loads(raw['slots'])
    rows = slots['query_block']['rows']
    rad = {r['query_id']: r['Rad_text'] for r in rows}
    units = sorted({r['Rad_unit'] for r in rows})
    nodes = json.loads(raw['nodes'])
    nk = nodes['orders']['4']['radii_kpc']
    nm = nodes['orders']['4']['radii_m']
    kpc_m = nodes['kpc_m']
    n1 = json.loads(raw['n1'])
    rr = n1['ring_radii_kpc']
    cmp_ = json.loads(raw['cmp'])
    fr = cmp_['failing_TRUNCATION_SHAPE_rings']
    v005 = raw['v005snap'].decode('utf-8')
    prov = json.loads(raw['prov_r2'])['numbers']
    texts = {k: raw[k].decode('utf-8') for k in ('prereg_r2', 'root_r2', 'map_r2')}

    # rings == nodes, bitwise
    eq_kpc = len(rr) == len(nk) == 100 and all(x == y for x, y in zip(rr, nk))
    eq_hex = all(float(x).hex() == float(y).hex() for x, y in zip(rr, nk))
    eq_m = all(x == y / kpc_m for x, y in zip(rr, nm))
    res['tsr']['n_rings'] = len(rr)
    res['tsr']['n_nodes_order4'] = len(nk)
    res['tsr']['registered_n_columns'] = nodes['orders']['4'].get('registered_n_columns')
    res['tsr']['rings_equal_nodes_kpc_bitwise'] = eq_kpc and eq_hex
    res['tsr']['rings_equal_nodes_m_over_kpc_m'] = eq_m
    for i in (13, 14, 15, 16, 17):
        res['tsr']['node_%d_kpc' % i] = nk[i]
    res['tsr']['failing_ts_rings'] = [{k: v for k, v in r.items()} for r in fr]
    res['tsr']['failing_non_ts_rings'] = cmp_.get('failing_non_TRUNCATION_SHAPE_rings')
    res['tsr']['checks'] = cmp_['checks']
    res['tsr']['outcome'] = cmp_['outcome']
    res['tsr']['gate'] = cmp_['n_route_ab_gate']
    res['tsr']['reason_codes'] = cmp_['n_route_ab_reason_codes']
    res['tsr']['failures'] = cmp_['failures']
    res['tsr']['S_over_theta_15'] = cmp_['S_over_theta'][15]
    res['tsr']['n_S_over_theta_gt_1'] = [i for i, s in enumerate(cmp_['S_over_theta']) if s > 1]
    ordn = fr[0]['ordinal']
    res['tsr']['ordinal_is_0_based_index'] = fr[0]['R_kpc'] == nk[ordn] == rr[ordn]
    # derived flag rule r_{k-1} < R_q < r_{k+1}
    k = ordn
    lo, hi = nk[k - 1], nk[k + 1]
    flagged = [q for q, t in rad.items() if lo < float(t) < hi]
    res['tsr']['flagged_by_derived_rule'] = flagged
    res['tsr']['Q24_Q25_Q26_Q27'] = {q: rad[q] for q in ('NGC3198-Q24', 'NGC3198-Q25', 'NGC3198-Q26', 'NGC3198-Q27')}
    res['tsr']['Q25_between'] = [i for i in range(99) if nk[i] < float(rad['NGC3198-Q25']) < nk[i + 1]]
    res['tsr']['Q26_between'] = [i for i in range(99) if nk[i] < float(rad['NGC3198-Q26']) < nk[i + 1]]
    res['tsr']['metre_form_same'] = [q for q, t in rad.items() if lo * kpc_m < float(t) * kpc_m < hi * kpc_m] == flagged
    # zones
    z = {'INNER': [q for q, t in rad.items() if float(t) < 10.0], 'TRANSITION': [q for q, t in rad.items() if 10.0 <= float(t) < 30.0],
         'OUTER': [q for q, t in rad.items() if float(t) >= 30.0]}
    res['zones'] = {k2: {'n': len(v), 'first': v[0], 'last': v[-1], 'r_first': rad[v[0]], 'r_last': rad[v[-1]]} for k2, v in z.items()}
    res['rad_units'] = units
    res['stage0_outer_rows'] = slots['stage0_registration']['outer_rows']
    res['invalid_primary_GL4'] = slots['query_block']['invalid_primary_GL4']
    res['alternatives_declared'] = [(d.get('id') or d.get('name'), d.get('kind'), d.get('status')) for d in slots['alternatives']['declared']]
    res['slots_rule'] = slots['query_block']['rule']

    E = res['entries']

    def ent(key, ok, how):
        E[key] = {'ok': bool(ok), 'how': how, 'listed': prov.get(key)}

    ent('9.90', '%.2f' % nk[14] == '9.90', 'nodes[4].radii_kpc[14] = %r' % nk[14])
    ent('9.901811', '%.6f' % nk[14] == '9.901811', 'nodes[4].radii_kpc[14] = %r' % nk[14])
    ent('10.540847', '%.6f' % nk[15] == '10.540847' and '%.6f' % fr[0]['radial_support']['R_kpc'] == '10.540847',
        'nodes[15] = %r; compare radial_support.R_kpc = %r' % (nk[15], fr[0]['radial_support']['R_kpc']))
    ent('10.91', '%.2f' % nk[16] == '10.91', 'nodes[16] = %r' % nk[16])
    ent('10.911722', '%.6f' % nk[16] == '10.911722', 'nodes[16] = %r' % nk[16])
    m1, m2 = (nk[14] + nk[15]) / 2, (nk[15] + nk[16]) / 2
    ent('10.22', '%.2f' % m1 == '10.22' and '%.7f' % nk[14] == '9.9018106' and '%.7f' % nk[15] == '10.5408472',
        'midpoint(14,15) = %r; 7-dp operands %s, %s' % (m1, '%.7f' % nk[14], '%.7f' % nk[15]))
    ent('10.73', '%.2f' % m2 == '10.73' and '%.7f' % nk[16] == '10.9117219', 'midpoint(15,16) = %r; 7-dp %s' % (m2, '%.7f' % nk[16]))
    ent('11.04', rad['NGC3198-Q26'] == '11.04', 'slots Rad_text(Q26) = %r' % rad['NGC3198-Q26'])
    ent('14', nk[14] < float(rad['NGC3198-Q25']) < nk[15], 'Q25 between node 14 and 15: %s' % res['tsr']['Q25_between'])
    ent('17', nk[16] < float(rad['NGC3198-Q26']) < nk[17], 'Q26 between node 16 and 17: %s (node17 = %r)' % (res['tsr']['Q26_between'], nk[17]))
    ent('100', len(rr) == len(nk) == 100 and eq_kpc, 'N1 ring_radii_kpc len %d; GL4 radii_kpc len %d; bitwise equal %s' % (len(rr), len(nk), eq_kpc and eq_hex))
    ent('1.014818', '%.6f' % fr[0]['S_over_theta'] == '1.014818', 'compare failing ring S_over_theta = %r' % fr[0]['S_over_theta'])
    s65 = section(v005, 65)
    s66 = section(v005, 66)
    ent('5.20', '−5.20 to −1.76' in s65, "V005 A65 contains '−5.20 to −1.76'")
    ent('1.76', '−5.20 to −1.76' in s65, "V005 A65 contains '−5.20 to −1.76'")
    v001 = raw['v001'].decode('utf-8')
    i22 = [l.strip() for l in v001.split('\n') if '2.2' in l]
    ent('2.2', any('R_d' in l or 'disc' in l.lower() for l in i22), 'V001 lines with 2.2: %s' % i22[:3])
    # review counts
    sev = []
    for p in REVIEWS:
        t = rb(p).decode('utf-8')
        for m in re.finditer(r'^#{2,4} ((?:A|B|L-C)-?\d+)\s*(?:[:.—–-]\s*)?(BLOCKING|SHOULD_FIX|NOTE)\b', t, re.M):
            sev.append((m.group(1), m.group(2), os.path.basename(os.path.dirname(p))))
    res['round1_findings_parsed'] = sev
    ent('57', len(sev) == 57, 'round-1 finding headings parsed: %d' % len(sev))
    serious = [s for s in sev if s[1] in ('BLOCKING', 'SHOULD_FIX')]
    refuted = {'A-01', 'A-02', 'B-1', 'B-2', 'L-C01', 'L-C02'}
    other = [s for s in serious if s[0] not in refuted]
    ent('26', len(other) == 26, 'serious %d; minus the six refuter-checked = %d' % (len(serious), len(other)))
    # posts
    for num, (p, h) in POSTS.items():
        ok = os.path.isfile(p)
        got = hashlib.sha256(rb(p)).hexdigest() if ok else None
        ent(num, ok and (h is None or got == h), 'exists %s; sha %s; expected %s' % (ok, got, h))
    res['fromcodex_0618_also_exists'] = [n for n in os.listdir(X + 'FROM_CODEX') if n.startswith('0618_')]
    # V005 A66 facts restated in the text
    res['a66_has'] = {s: (s in s66) for s in ('ordinal 15, R = 10.54 kpc', '1.0148', '1.1–3.7', 'K = 2', 'radial support')}
    # A-references in the three texts versus pins and the no-change list
    pre = texts['prereg_r2']
    sec11 = pre[pre.index('## 11. Sources'):]
    pins = sorted({int(x) for x in re.findall(r'^\| A(\d{1,3}) \|', sec11, re.M)})
    body_refs = {}
    for k2, t in texts.items():
        tt = t if k2 != 'prereg_r2' else pre[:pre.index('## 11. Sources')]
        for m in re.finditer(r'(?<![\w-])A(\d{2,3})(?:\.\d+)?(?![\w])', tt):
            n = int(m.group(1))
            if n >= 47:
                body_refs.setdefault(n, set()).add(k2)
    res['v005_refs_in_texts'] = {('A%d' % n): sorted(v) for n, v in sorted(body_refs.items())}
    res['v005_pinned'] = ['A%d' % n for n in pins]
    res['v005_cited_not_pinned'] = ['A%d' % n for n in sorted(body_refs) if n not in pins]
    with open(a.out, 'x', encoding='utf-8') as f:
        f.write(json.dumps(res, indent=1, ensure_ascii=False, default=list) + '\n')
    bad = [k2 for k2, v in E.items() if not v['ok']]
    print(json.dumps({'entries_ok': len(E) - len(bad), 'entries_bad': bad, 'tsr': {k2: res['tsr'][k2] for k2 in (
        'rings_equal_nodes_kpc_bitwise', 'rings_equal_nodes_m_over_kpc_m', 'ordinal_is_0_based_index', 'flagged_by_derived_rule',
        'Q25_between', 'Q26_between', 'metre_form_same', 'n_S_over_theta_gt_1', 'outcome', 'gate', 'reason_codes')},
        'zones': res['zones'], 'units': units, 'stage0_outer_rows': res['stage0_outer_rows'], 'invalid_primary_GL4': res['invalid_primary_GL4'],
        'sources_match': {k2: v['match'] for k2, v in res['sources'].items()},
        'v005_cited_not_pinned': res['v005_cited_not_pinned'], 'fromcodex_0618': res['fromcodex_0618_also_exists']}, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    raise SystemExit(main())
