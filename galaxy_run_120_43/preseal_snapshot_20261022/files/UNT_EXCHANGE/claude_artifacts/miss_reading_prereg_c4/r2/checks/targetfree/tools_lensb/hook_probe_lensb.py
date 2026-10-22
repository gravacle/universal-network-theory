# Lens B: does the audit hook of check_target_free_c4v001.py really block target-like opens and writes?
# Part 1 calls the hook function directly with synthetic audit-event tuples: nothing is opened.
# Part 2 (this process) installs the real hook and attempts writes and indirect opens on canary files inside --work only.
#   Every path used is inside --work; the only forbidden-term string used ('lelli', a term of the tool's own deny-list that is
#   not in the review rules' list) names a file that does not exist, so no data can be opened.
# Part 3 shows that T.run() alone, as the generator and the mutation test call it, runs with no hook.
# usage: python3 -I -B hook_probe_lensb.py --round1 R1 --work NEW_DIR --out RES.json   (run part 3 with --part3-only in a fresh process)
import argparse, json, os, sys


def outcome(fn):
    try:
        fn()
        return 'ALLOWED'
    except PermissionError as e:
        return 'REFUSED_BY_HOOK: %s' % (str(e)[:80],)
    except FileNotFoundError:
        return 'NOT_REFUSED_BY_HOOK (reached the OS: FileNotFoundError)'
    except Exception as e:
        return 'OTHER: %s %s' % (type(e).__name__, str(e)[:80])


def part1(T):
    W = '/nonexistent_lensb_probe'
    probes = [
        ('open read, deny-listed term', 'open', (W + '/NGC3198_rotmod.dat', 'r', 0)),
        ('open read, deny-listed term (bytes path)', 'open', ((W + '/sparc/x').encode(), 'rb', 0)),
        ('open read, C5H run path', 'open', (W + '/runs_ext/KMAX_A2F10_C5H_RUN_V001/result.json', 'r', 0)),
        ('open read, UVT_ run path', 'open', (W + '/runs_ext/UVT_Z2_A2F10_RUN_V001/result.json', 'r', 0)),
        ('open read, other NGC3198 source name', 'open', (W + '/THINGS/NGC3198_curve.txt', 'r', 0)),
        ('open read, fullwidth deny-listed term', 'open', (W + '/ＳＰＡＲＣ/x.txt', 'r', 0)),
        ('open by file descriptor', 'open', (3, 'r', 0)),
        ('open write mode', 'open', (W + '/x.json', 'w', 0)),
        ('os.open O_WRONLY', 'open', (W + '/x.json', None, os.O_WRONLY)),
        ('os.listdir of a deny-listed dir', 'os.listdir', (W + '/sparc',)),
        ('os.scandir of a deny-listed dir', 'os.scandir', (W + '/sparc',)),
        ('os.truncate', 'os.truncate', (W + '/x.json', 0)),
        ('os.mkdir', 'os.mkdir', (W + '/d', 0o777, -1)),
        ('os.symlink', 'os.symlink', (W + '/a', W + '/b', -1)),
        ('os.link', 'os.link', (W + '/a', W + '/b', -1, -1)),
        ('os.chmod', 'os.chmod', (W + '/a', 0o600, -1)),
        ('os.utime', 'os.utime', (W + '/a', None, None, -1)),
        ('os.exec', 'os.exec', ('/bin/sh', ['sh'], None)),
        ('os.posix_spawn', 'os.posix_spawn', ('/bin/sh', ['sh'], None)),
        ('os.fork', 'os.fork', ()),
        ('socket.getaddrinfo', 'socket.getaddrinfo', ('example.org', 80, 0, 0, 0)),
        ('os.remove (listed)', 'os.remove', (W + '/a', -1)),
        ('subprocess.Popen (listed)', 'subprocess.Popen', ('/bin/sh', ['sh'], None, None)),
    ]
    return [{'probe': n, 'event': e, 'outcome': outcome(lambda e=e, a=a: T._hook(e, a))} for n, e, a in probes]


def part2(T, work, out):
    os.makedirs(work)                                       # must not exist
    canary = os.path.join(work, 'canary_truncate.txt')
    canary_w = os.path.join(work, 'canary_write.txt')
    for p in (canary, canary_w):
        with open(p, 'x') as f:
            f.write('synthetic canary\n')
    link = os.path.join(work, 'innocent_name_link.json')
    os.symlink('lelli_named_target_that_does_not_exist.json', link)    # dangling: the target does not exist
    T._OUT.append(os.path.abspath(out))
    sys.addaudithook(T._hook)                               # from here on, the real hook is active in this process
    res = []
    res.append({'probe': 'open(canary, "w")', 'outcome': outcome(lambda: open(canary_w, 'w'))})
    res.append({'probe': 'os.open(canary, O_WRONLY)', 'outcome': outcome(lambda: os.open(canary_w, os.O_WRONLY))})
    res.append({'probe': 'direct open of the deny-listed name', 'outcome': outcome(lambda: open(os.path.join(work, 'lelli_named_target_that_does_not_exist.json')))})
    res.append({'probe': 'open through a symlink with an innocent name', 'outcome': outcome(lambda: open(link))})
    before = os.path.getsize(canary)
    o = outcome(lambda: os.truncate(canary, 0))
    res.append({'probe': 'os.truncate(canary, 0)', 'outcome': o, 'size_before': before, 'size_after': os.path.getsize(canary)})
    res.append({'probe': 'os.mkdir in work', 'outcome': outcome(lambda: os.mkdir(os.path.join(work, 'made_under_hook')))})
    res.append({'probe': 'os.symlink in work', 'outcome': outcome(lambda: os.symlink('canary_write.txt', os.path.join(work, 'link_made_under_hook')))})
    res.append({'probe': 'os.link (hard link) in work', 'outcome': outcome(lambda: os.link(canary_w, os.path.join(work, 'hardlink_made_under_hook.txt')))})
    res.append({'probe': 'os.chmod canary', 'outcome': outcome(lambda: os.chmod(canary_w, 0o600))})
    with open(out, 'x') as f:                               # the one write the hook allows
        f.write(json.dumps({'schema': 'LENSB_HOOK_PROBE_V001', 'part1_direct_calls': part1(T), 'part2_installed_hook': res},
                           indent=1, ensure_ascii=False) + '\n')


def part3(T, round1, work):
    class A:
        pass
    a = A()
    a.dir, a.provenance = round1, os.path.join(round1, 'NUMBER_PROVENANCE_R2.json')
    a.slots = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
    a.expect_slots_sha = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
    r = T.run(a)
    o = outcome(lambda: open(os.path.join(work, 'lelli_named_target_that_does_not_exist.json')))
    print(json.dumps({'part3_T_run_verdict': r['verdict'], 'open_of_deny_listed_name_after_T_run_without_main': o}))


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--round1', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--out')
    ap.add_argument('--part3-only', action='store_true')
    a = ap.parse_args()
    sys.path.insert(0, os.path.join(a.round1, 'tools'))
    import check_target_free_c4v001 as T
    if a.part3_only:
        part3(T, a.round1, a.work)
    else:
        part2(T, os.path.abspath(a.work), a.out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
