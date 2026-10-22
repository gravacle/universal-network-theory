# independent per-entry section sha extraction for V005 (lens A); read-only
import hashlib, re, sys
p = sys.argv[1]
b = open(p, 'rb').read()
print('file sha256', hashlib.sha256(b).hexdigest(), 'bytes', len(b))
t = b.decode('utf-8')
lines = t.split('\n')
heads = [i for i, l in enumerate(lines) if l.startswith('## ')]
want = {48:'526cfceacade31d16dc4f5c7fd023573515898692d4f40d22bfebc9216008ee6',56:'0e0ef14377f12b3326beb6b1ae0d0ce9c262aeb6fd3c03ce89851a941aa51a47',60:'42c5870ff48dddd19ddddd70d3705ced8231a42011f5c4455b1fdfa7e50b67b8',62:'1e3bbebc12dffcb7e965fec0f99004d3969513152f25e0e84b193420447b8084',63:'8cbe65538dc03ffe1c7f8c84088ce5e7c05791c9b36471ed7f1f2631330f169f',64:'9984d5819d5a86b47d18ebe1747364b71abba146421b65d1ab692f551d14d015',65:'290eac4af1f43d01c2c66a5c5981d0f43d73a7a9bf06388821d5ffd2f6a24e9c',66:'3446953179e036f3e77872dc3e192af6e83b18f7c0486df6a4963643c29224c9',70:'f6b6e253b02e0e41c8fd7d142ff0e205152786db35965e11d5c0ed3f9693d5b2',81:'3829e30c497fcf6b6779379a1eb89070a84a87da31ef35589770f496a906a84e',82:'8a45e4a9378e5c51e5d410f007af5040840cbfa7404f52220bb4db37130ddedc'}
order = []
for j, i in enumerate(heads):
    m = re.match(r'^## A(\d+):', lines[i])
    end = heads[j+1] if j+1 < len(heads) else len(lines)
    body = '\n'.join(lines[i:end]) + ('\n' if end < len(lines) else '')
    if m:
        n = int(m.group(1)); order.append(n)
        if n in want:
            h = hashlib.sha256(body.encode('utf-8')).hexdigest()
            print('A%d lines %d-%d sha %s %s' % (n, i+1, end, h, 'MATCH' if h == want[n] else 'DIFF'))
print('entry order in file:', order)
