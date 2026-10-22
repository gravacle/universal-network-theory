# verify_targetfree_1: an independent recheck of T7 currency and the 14 V005 section pins of the miss-reading prereg r2
# (round 2), written separately from the object's check (it does not import it). Byte slicing, not text joins.
# Reads only: the round-2 PREREG and V005 snapshot copies named on the command line. Writes one JSON (exclusive create).
# usage: python3 -I -B recheck_t7_vtf1.py OUT.json PREREG.md V005_SNAPSHOT.md [V005_SNAPSHOT.md ...]
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_vtf1  # noqa: F401  (installs the audit hook)
import hashlib, json, re


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sec11(prereg_b):
    t = prereg_b.decode('utf-8')
    i = t.index('\n## 11. ')
    j = t.find('\n## ', i + 1)
    return t[i:] if j < 0 else t[i:j]


def pins(s11):
    out = []
    for line in s11.split('\n'):
        if not line.startswith('| A'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        m = re.fullmatch(r'A(\d+)', cells[0])
        h = re.fullmatch(r'`([0-9a-f]{64})`', cells[-1])
        if m and h:
            out.append({'n': int(m.group(1)), 'ends_before': cells[-2], 'sha': h.group(1)})
    return out


def nochange(s11):
    k = '**Read with no change to this text:**'
    i = s11.index(k) + len(k)
    j = s11.index('. ', i)
    body = s11[i:j]
    got, parts = set(), []
    for part in body.split(','):
        part = part.strip()
        parts.append(part)
        m = re.fullmatch(r'A(\d+)(?:–A(\d+))?', part)
        if not m:
            raise ValueError('unparsed no-change part %r' % part)
        a = int(m.group(1)); b = int(m.group(2) or a)
        got.update(range(a, b + 1))
    return body, parts, got


def line_offsets(b):
    offs, pos = [], 0
    for ln in b.split(b'\n'):
        offs.append((pos, ln))
        pos += len(ln) + 1
    return offs


def section_bytes(b, n, marker):
    offs = line_offsets(b)
    head = ('## A%d:' % n).encode()
    starts = [k for k, (p, ln) in enumerate(offs) if ln.startswith(head)]
    if len(starts) != 1:
        return None, len(starts)
    k0 = starts[0]
    end = len(b)
    for k in range(k0 + 1, len(offs)):
        p, ln = offs[k]
        if ln.startswith(b'## '):
            end = p
            break
    if marker and marker != 'next heading':
        mk = marker.strip('`').encode()
        cut = None
        for k in range(k0 + 1, len(offs)):
            p, ln = offs[k]
            if p >= end:
                break
            if ln.startswith(mk):
                cut = p
                break
        if cut is None:
            return None, 'marker not found'
        end = cut
    return b[offs[k0][0]:end], 1


def headings(b):
    t = b.decode('utf-8')
    strict = [(i + 1, int(m.group(1)), line) for i, line in enumerate(t.split('\n'))
              for m in [re.match(r'## A(\d{1,3})\b', line)] if m]
    loose = [(i + 1, line) for i, line in enumerate(t.split('\n'))
             if re.match(r'\s*#{1,6}\s*(?:entry\s+)?[Aa]\s*\d', line, re.I) and not re.match(r'## A\d{1,3}\b', line)]
    return strict, loose


def main():
    out_path, prereg_path = sys.argv[1], sys.argv[2]
    snaps = sys.argv[3:]
    pb = open(prereg_path, 'rb').read()
    s11 = sec11(pb)
    P = pins(s11)
    body, parts, NC = nochange(s11)
    cited = {p['n'] for p in P}
    res = {'prereg': prereg_path, 'prereg_sha256': sha(pb), 'pinned_entries': ['A%d' % p['n'] for p in P],
           'n_pins': len(P), 'no_change_text': body, 'no_change_parts': parts,
           'no_change_expanded': ['A%d' % n for n in sorted(NC)], 'overlap_cited_and_no_change': sorted(cited & NC),
           'snapshots': []}
    for sp in snaps:
        b = open(sp, 'rb').read()
        strict, loose = headings(b)
        nums = sorted({n for _, n, _ in strict})
        later = [n for n in nums if n >= 47 and n not in cited and n not in NC]
        dup = sorted({n for _, n, _ in strict if [x for _, x, _ in strict].count(n) > 1})
        pr = []
        for p in P:
            sb, cnt = section_bytes(b, p['n'], p['ends_before'])
            cur = sha(sb) if sb is not None else None
            pr.append({'entry': 'A%d' % p['n'], 'ends_before': p['ends_before'], 'stated': p['sha'], 'current': cur,
                       'match': cur == p['sha'], 'count': cnt})
        res['snapshots'].append({
            'path': sp, 'sha256': sha(b), 'n_bytes': len(b), 'max_heading': max(nums),
            'headings_ge47': ['A%d' % n for n in nums if n >= 47],
            'later_not_cited_not_no_change': ['A%d' % n for n in later],
            'duplicate_headings': dup, 'heading_like_lines_not_matched_by_strict_rule': loose,
            'later_heading_lines': [(ln, line) for ln, n, line in strict if n in later],
            'pins_all_match': all(x['match'] for x in pr), 'pins': pr})
    with open(out_path, 'x') as f:
        f.write(json.dumps(res, indent=1, ensure_ascii=False) + '\n')
    for s in res['snapshots']:
        print(s['sha256'][:8], 'max', s['max_heading'], 'later', s['later_not_cited_not_no_change'],
              'pins_all_match', s['pins_all_match'], 'loose', len(s['heading_like_lines_not_matched_by_strict_rule']))


if __name__ == '__main__':
    main()
