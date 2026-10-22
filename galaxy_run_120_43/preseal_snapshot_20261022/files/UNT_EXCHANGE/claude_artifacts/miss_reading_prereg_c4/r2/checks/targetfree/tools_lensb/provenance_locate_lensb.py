# Lens B: for every number in NUMBER_PROVENANCE_R2.json, locate it in the target-free sources the provenance names.
# Reads only: the r2 provenance JSON, root decisions V003/V004, the V005 copy taken at review, slots V003 (query block),
# RUNBOOK_V001 and the v003g module. Writes only --out (exclusive create). Hits are listed for manual confirmation.
# usage: python3 -I -B provenance_locate_lensb.py --prov PROV.json --v005 V005_COPY --out OUT.json
import argparse, hashlib, json, re

ROOT = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
SRC = {
    'V003': ROOT + 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V003_ADDENDUM.md',
    'V004': ROOT + 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md',
    'RUNBOOK': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/RUNBOOK_V001.md',
    'MODULE': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py',
}
SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'


def entry_of(lines, i):
    for j in range(i, -1, -1):
        m = re.match(r'^## (A\d+)', lines[j])
        if m:
            return m.group(1)
    return None


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--prov', required=True)
    ap.add_argument('--v005', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    SRC['V005'] = a.v005
    texts = {k: open(p, encoding='utf-8').read() for k, p in SRC.items()}
    shas = {k: hashlib.sha256(open(p, 'rb').read()).hexdigest() for k, p in SRC.items()}
    slots_raw = open(SLOTS, 'rb').read()
    slots = json.loads(slots_raw)
    rad = {r['query_id']: r['Rad_text'] for r in slots['query_block']['rows']}
    prov = json.load(open(a.prov, encoding='utf-8'))
    out = {'schema': 'LENSB_PROVENANCE_LOCATE_V001', 'source_sha256': shas,
           'slots_sha256': hashlib.sha256(slots_raw).hexdigest(), 'numbers': {}}
    for num, v in prov['numbers'].items():
        rec = {'category': v['category'], 'uses': v['uses'], 'hits': []}
        if v['category'] == 'QUERY_RADIUS':
            rec['slots_rad_text'] = {q: rad.get(q) for q in v.get('query_ids', [])}
        pat = re.compile(r'(?<![\w.])' + re.escape(num) + r'(?![\w]|\.\d)')
        for k, t in texts.items():
            lines = t.split('\n')
            for i, l in enumerate(lines):
                if pat.search(l):
                    rec['hits'].append({'src': k, 'line': i + 1, 'entry': entry_of(lines, i) if k.startswith('V00') else None,
                                        'text': l.strip()[:160]})
        rec['n_hits'] = len(rec['hits'])
        rec['hits'] = rec['hits'][:6]
        out['numbers'][num] = rec
    with open(a.out, 'x', encoding='utf-8') as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    for num, rec in out['numbers'].items():
        if rec['category'] in ('MODEL_DIAGNOSTIC', 'GEOMETRY_REGISTERED', 'BARYON_MODEL_REGISTERED', 'NUMERICS_RULING', 'QUERY_RADIUS'):
            print('%-8s %-24s n=%-3d %s %s' % (num, rec['category'], rec['n_hits'],
                                              ['%s:%d(%s)' % (h['src'], h['line'], h['entry']) for h in rec['hits'][:4]],
                                              rec.get('slots_rad_text', '')))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
