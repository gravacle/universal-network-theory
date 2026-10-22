# summarize_console_r5chk.py -- read-only: print verdict, codes and fence summary of each captured console file.
# usage: python3 -I -B summarize_console_r5chk.py FILE.console.txt [...]
import sys, json, re
for p in sys.argv[1:]:
    t = open(p).read()
    summ = None
    m = re.search(r'^R5CHK_FENCE_SUMMARY (.*)$', t, re.M)
    if m:
        summ = json.loads(m.group(1))
        body = t[:m.start()]
    else:
        body = t
    # first JSON object in the body
    j = None
    i = body.find('{')
    while i != -1 and j is None:
        try:
            j, end = json.JSONDecoder().raw_decode(body[i:])
        except ValueError:
            i = body.find('{', i + 1)
    name = p.rsplit('/', 1)[-1].replace('.console.txt', '')
    if isinstance(j, dict) and 'verdict' in j:
        codes = [f['code'] for f in j.get('failures', [])]
        notes = [n['code'] for n in j.get('notes', [])]
        print('%-10s verdict=%s failures=%d %s' % (name, j['verdict'], len(codes), codes))
        print('           notes=%s' % notes)
    else:
        lines = [l for l in body.splitlines() if l.strip()]
        print('%-10s (no verdict JSON) tail: %s' % (name, ' | '.join(lines[-4:])[:900]))
    if summ:
        print('           fence %s/%s blocked_after=%s guard=%s exit=%s' % (summ['selftest'], summ['selftest_v002'], summ['blocked_after_selftests'],
                                                                    summ['stat_list_guard_refused'], summ['exit_code']))
    else:
        print('           NO FENCE SUMMARY LINE')
