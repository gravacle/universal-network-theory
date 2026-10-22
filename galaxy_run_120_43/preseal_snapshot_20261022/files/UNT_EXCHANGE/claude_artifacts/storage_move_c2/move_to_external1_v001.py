"""Move a Research directory to the same relative path on External1, verified, leaving a symlink.

Usage: python3 -I move_to_external1_v001.py <abs source dir under /Users/bgm/Research> [--workers N] [--dry]

Steps (any failure stops before the source is touched):
  1. preconditions: source is a real directory (not a symlink), destination absent, no open files (lsof +D),
     nothing modified in the last QUIET_S seconds;
  2. manifest of the source (relative path, type, size, mtime_ns, link target);
  3. copy with ditto (preserves metadata/xattrs);
  4. verify every regular file by size + sha256 (source vs destination), every symlink by target,
     every directory present; file counts equal;
  5. re-check the source manifest is unchanged since step 2 and lsof is still empty;
  6. rename source -> source.__moved_to_external1__ (same volume, atomic), create symlink source -> destination,
     check the symlink resolves and that 3 sampled files read back with the verified sha256;
  7. remove the renamed internal copy.
Rollback: rm the symlink; ditto <destination> <source>.
A JSON record of each move (manifest sha256, counts, bytes, timings) is written next to this script under log/.
"""
import hashlib, json, os, subprocess, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

SRC_ROOT = '/Users/bgm/Research'
DST_ROOT = '/Volumes/External1/Research'
QUIET_S = 600
LOG = Path(__file__).resolve().parent / 'log'


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 24), b''):
            h.update(b)
    return h.hexdigest()


def pair_hash(args):
    s, d = args
    return s, sha256(s), sha256(d)


def manifest(root):
    out = {}
    for dp, dns, fns in os.walk(root, followlinks=False):
        for n in dns + fns:
            p = os.path.join(dp, n)
            r = os.path.relpath(p, root)
            st = os.lstat(p)
            if os.path.islink(p):
                out[r] = ('l', 0, st.st_mtime_ns, os.readlink(p))
            elif os.path.isdir(p):
                out[r] = ('d', 0, 0, '')
            else:
                out[r] = ('f', st.st_size, st.st_mtime_ns, '')
    return out


def lsof_open(root):
    r = subprocess.run(['lsof', '+D', root], capture_output=True, text=True)
    return [ln for ln in r.stdout.splitlines()[1:] if ln.strip()]


def die(msg):
    print('REFUSED: ' + msg)
    sys.exit(2)


def main():
    src = os.path.abspath(sys.argv[1])
    workers = int(sys.argv[sys.argv.index('--workers') + 1]) if '--workers' in sys.argv else 6
    dry = '--dry' in sys.argv
    if not src.startswith(SRC_ROOT + '/'):
        die('source not under ' + SRC_ROOT)
    dst = DST_ROOT + src[len(SRC_ROOT):]
    if os.path.islink(src) or not os.path.isdir(src):
        die('source is not a real directory')
    if os.path.exists(dst):
        die('destination exists: ' + dst)
    if not os.path.ismount('/Volumes/External1'):
        die('External1 not mounted')
    t0 = time.time()
    m0 = manifest(src)
    newest = max([v[2] for v in m0.values() if v[0] == 'f'] or [0]) / 1e9
    if time.time() - newest < QUIET_S:
        die(f'modified {time.time() - newest:.0f} s ago (< {QUIET_S} s)')
    op = lsof_open(src)
    if op:
        die('open files:\n' + '\n'.join(op[:20]))
    nbytes = sum(v[1] for v in m0.values() if v[0] == 'f')
    nfiles = sum(1 for v in m0.values() if v[0] == 'f')
    print(f'source {src}\ndest   {dst}\nfiles {nfiles} bytes {nbytes} ({nbytes / 1e9:.1f} GB)')
    if dry:
        print('DRY: preconditions pass')
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    t1 = time.time()
    subprocess.run(['ditto', src, dst], check=True)
    t2 = time.time()
    m1 = manifest(dst)
    if set(m1) != set(m0):
        die(f'entry sets differ: missing {len(set(m0) - set(m1))}, extra {len(set(m1) - set(m0))}')
    for r, v in m0.items():
        w = m1[r]
        if v[0] != w[0] or v[1] != w[1] or v[3] != w[3]:
            die('type/size/link mismatch at ' + r)
    files = [(os.path.join(src, r), os.path.join(dst, r)) for r, v in m0.items() if v[0] == 'f']
    digests = {}
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for s, hs, hd in ex.map(pair_hash, files, chunksize=8):
            if hs != hd:
                die('sha256 mismatch at ' + s)
            digests[os.path.relpath(s, src)] = hs
    t3 = time.time()
    if manifest(src) != m0:
        die('source changed during copy; destination left in place, source untouched')
    op = lsof_open(src)
    if op:
        die('files opened during copy:\n' + '\n'.join(op[:20]))
    man_path = dst.rstrip('/') + '.SHA256_MANIFEST.json'
    man_bytes = json.dumps(digests, sort_keys=True, indent=0).encode()
    Path(man_path).write_bytes(man_bytes)
    held = src + '.__moved_to_external1__'
    os.rename(src, held)
    try:
        os.symlink(dst, src)
        for r in sorted(digests)[:: max(1, len(digests) // 3)][:3]:
            if sha256(os.path.join(src, r)) != digests[r]:
                raise RuntimeError('readback mismatch via symlink at ' + r)
    except Exception as e:
        if os.path.islink(src):
            os.unlink(src)
        os.rename(held, src)
        die(f'symlink step failed, source restored: {e}')
    subprocess.run(['rm', '-rf', held], check=True)
    t4 = time.time()
    rec = {'source': src, 'destination': dst, 'files': nfiles, 'bytes': nbytes,
           'entries': len(m0), 'manifest': man_path, 'manifest_sha256': hashlib.sha256(man_bytes).hexdigest(),
           'utc_done': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'seconds': {'scan': t1 - t0, 'copy': t2 - t1, 'verify': t3 - t2, 'swap': t4 - t3}}
    LOG.mkdir(exist_ok=True)
    (LOG / (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '_' + Path(src).name + '.json')).write_text(json.dumps(rec, indent=1))
    print('MOVED ' + json.dumps(rec))


if __name__ == '__main__':
    main()
