# R2-A closure lens: list top-level key structure of named target-free records (no values printed).
import json, sys, hashlib
def strict(path):
    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d: raise ValueError('dup %r' % k)
            d[k] = v
        return d
    b = open(path, 'rb').read()
    return hashlib.sha256(b).hexdigest(), json.loads(b.decode('utf-8'), object_pairs_hook=hook)
def shape(o, depth=0, maxd=2):
    if isinstance(o, dict):
        if depth >= maxd: return '{%d keys}' % len(o)
        return {k: shape(v, depth+1, maxd) for k, v in o.items()}
    if isinstance(o, list): return '[list len %d]' % len(o)
    return type(o).__name__
for p in sys.argv[1:]:
    h, d = strict(p)
    print(p, h)
    print(json.dumps(shape(d), indent=1)[:3000])
