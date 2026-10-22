# Claude4 r6 refute helper (r6_check), checks (3)/(5): every {path, sha256} pin in prereg r6 verified from bytes.
# A pin is any JSON object with a string 'path' and a string 'sha256'. Before any file access the path is screened by name:
# a runs_ext component, a UVT_* component, the C5H run name, target words (rotmod, vobs, massmodels, sparc) or an NGC3198 name
# (other than a .py source or a root decision addendum) is NOT opened or stat'ed; it is reported instead. Pins whose sha is
# not 64 hex (e.g. PENDING) are reported, not opened. Bytes are hashed only; no content is printed.
# Read-only; writes OUT.json by exclusive create.
# usage: python3 -I -B pins_r6chk.py R5.json R6.json OUT.json
import fnmatch, hashlib, json, os, re, sys

HEX = re.compile(r'^[0-9a-f]{64}$')
ADD = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V00*_ADDENDUM*.md'


def protected(p):
    low = p.casefold()
    comps = low.split('/')
    if 'runs_ext' in comps:
        return 'runs_ext'
    if any(c.startswith('uvt_') for c in comps[:-1]) or (comps[-1].startswith('uvt_') and not comps[-1].endswith('.py')):
        return 'UVT component'
    if 'kmax_a2f10_c5h_run_v001' in low:
        return 'C5H name'
    for w in ('rotmod', 'vobs', 'massmodels', 'sparc'):
        if w in low:
            return 'target word'
    if ('ngc3198' in low or 'ngc_3198' in low) and not low.endswith('.py') and not fnmatch.fnmatchcase(os.path.basename(p), ADD):
        return 'NGC3198 name'
    return None


def pins(o, path, out):
    if isinstance(o, dict):
        if isinstance(o.get('path'), str) and isinstance(o.get('sha256'), str):
            out.append((path, o['path'], o['sha256']))
        for k, v in o.items():
            pins(v, path + '.' + k, out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            pins(v, '%s[%d]' % (path, i), out)


def main():
    r5p, r6p, outp = sys.argv[1:4]
    d5 = json.load(open(r5p, 'rb'))
    d6 = json.load(open(r6p, 'rb'))
    p5, p6 = [], []
    pins(d5, '', p5)
    pins(d6, '', p6)
    cache = {}
    rows = []
    for jp, fp, sh in p6:
        row = {'json_path': jp, 'path': fp, 'sha256': sh}
        why = protected(fp)
        if why:
            row['result'] = 'NOT_OPENED_PROTECTED_NAME: ' + why
        elif not HEX.match(sh):
            row['result'] = 'NOT_A_SHA: ' + sh[:40]
        elif not fp.startswith('/'):
            row['result'] = 'RELATIVE_PATH'
        else:
            if fp not in cache:
                try:
                    with open(fp, 'rb') as fh:
                        cache[fp] = hashlib.sha256(fh.read()).hexdigest()
                except OSError as e:
                    cache[fp] = 'ERROR %s' % type(e).__name__
            got = cache[fp]
            row['result'] = 'OK' if got == sh else ('MISMATCH got %s' % got)
        rows.append(row)
    s5 = set((fp, sh) for _, fp, sh in p5)
    s6 = set((fp, sh) for _, fp, sh in p6)
    paths5 = {}
    for _, fp, sh in p5:
        paths5.setdefault(fp, set()).add(sh)
    changed_sha_same_path = sorted(fp for fp, sh in s6 - s5 if fp in paths5 and sh not in paths5[fp])
    res = {'r6_pins': len(p6), 'r6_distinct_path_sha': len(s6), 'r5_pins': len(p5), 'r5_distinct_path_sha': len(s5),
           'ok': sum(1 for r in rows if r['result'] == 'OK'),
           'not_ok': [r for r in rows if r['result'] != 'OK'],
           'new_in_r6_distinct': sorted('%s %s' % x for x in s6 - s5),
           'gone_from_r5_distinct': sorted('%s %s' % x for x in s5 - s6),
           'same_path_new_sha': changed_sha_same_path,
           'rows': rows}
    with open(outp, 'x') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print(json.dumps({k: res[k] for k in ('r6_pins', 'r6_distinct_path_sha', 'r5_pins', 'ok', 'same_path_new_sha')}, indent=1))
    print('NOT_OK:')
    for r in res['not_ok']:
        print('  ', r['result'], r['json_path'], r['path'][-90:])
    print('NEW IN R6 (distinct path/sha):', len(res['new_in_r6_distinct']))
    for x in res['new_in_r6_distinct']:
        print('  +', x[-150:])
    print('GONE FROM R5:', len(res['gone_from_r5_distinct']))
    for x in res['gone_from_r5_distinct']:
        print('  -', x[-150:])


if __name__ == '__main__':
    main()
