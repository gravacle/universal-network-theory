# R2-A closure lens: which events does the ROUND-2 check's own audit hook (check_target_free_c4v002._hook) refuse?
# Every probe acts only on innocuous canary names inside --work (this lens folder). No target-like path is ever opened.
import json, os, sys
R2T, work, outp = sys.argv[1], os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
sys.path.insert(0, R2T)
import check_target_free_c4v002 as T
os.makedirs(work)
canary = os.path.join(work, 'canary.txt')
with open(canary, 'x') as f:
    f.write('closure-lens canary 17 bytes\n')
T._OUT.append(outp)
sys.addaudithook(T._hook)
res = {}
def probe(name, fn):
    try:
        fn(); res[name] = 'ALLOWED'
    except PermissionError as e:
        res[name] = 'REFUSED: %s' % str(e)[:80]
    except Exception as e:
        res[name] = 'ERROR %s: %s' % (type(e).__name__, str(e)[:80])
probe('open_read_canary', lambda: open(canary).read())
probe('open_write_canary', lambda: open(canary, 'a').write('x'))
probe('os.truncate_canary', lambda: os.truncate(canary, 0))
probe('size_after_truncate', lambda: res.__setitem__('canary_size', os.path.getsize(canary)))
probe('os.mkdir_in_work', lambda: os.mkdir(os.path.join(work, 'newdir')))
probe('os.symlink_in_work', lambda: os.symlink(canary, os.path.join(work, 'innocent_link')))
probe('open_via_symlink', lambda: open(os.path.join(work, 'innocent_link')).read())
probe('os.chmod_canary', lambda: os.chmod(canary, 0o644))
probe('os.listdir_work', lambda: os.listdir(work))
probe('os.remove_canary', lambda: os.remove(canary))
probe('os.rename_canary', lambda: os.rename(canary, canary + '.x'))
probe('subprocess', lambda: __import__('subprocess').run(['/usr/bin/true']))
with open(outp, 'x') as f:
    f.write(json.dumps(res, indent=1, sort_keys=True) + '\n')
print(json.dumps(res, indent=1, sort_keys=True))
