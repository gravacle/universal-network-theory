import json, sys
def leaves(x, p=''):
    if isinstance(x, dict):
        if not x: yield p, {}
        for k, v in x.items(): yield from leaves(v, p + '/' + k)
    else: yield p, x
a = dict(leaves(json.load(open(sys.argv[1])))); b = dict(leaves(json.load(open(sys.argv[2]))))
for k in sorted(set(a) | set(b)):
    if a.get(k, '<ABSENT>') != b.get(k, '<ABSENT>'):
        print(k, '|', str(a.get(k, '<ABSENT>'))[:150], '->', str(b.get(k, '<ABSENT>'))[:150])
