# load_compare_r5chk.py -- load a compare source UNMODIFIED from its bytes as a module (r5_check helper).
# The sha256 of the bytes must equal the expected sha; the module is exec'd under a non-__main__ name, so main() never runs.
import hashlib, sys, types

def load(path, expected_sha, name='compare_r5chk'):
    b = open(path, 'rb').read()
    h = hashlib.sha256(b).hexdigest()
    if h != expected_sha:
        raise SystemExit('LOADER_REFUSED: %s sha %s != %s' % (path, h, expected_sha))
    m = types.ModuleType(name)
    m.__file__ = path
    sys.modules[name] = m
    exec(compile(b, path, 'exec'), m.__dict__)
    return m, h
