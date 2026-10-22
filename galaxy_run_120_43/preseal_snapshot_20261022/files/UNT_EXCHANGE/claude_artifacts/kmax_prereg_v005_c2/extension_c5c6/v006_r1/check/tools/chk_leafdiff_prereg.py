import json,sys
def leaves(o,p=""):
    if isinstance(o,dict):
        if not o: yield p,{}
        for k,v in o.items(): yield from leaves(v,p+"/"+str(k))
    elif isinstance(o,list):
        if not o: yield p,[]
        for i,v in enumerate(o): yield from leaves(v,p+"/"+str(i))
    else: yield p,o
a=dict(leaves(json.load(open(sys.argv[1])))); b=dict(leaves(json.load(open(sys.argv[2]))))
for k in sorted(set(a)|set(b)):
    if a.get(k,"<ABSENT>")!=b.get(k,"<ABSENT>"):
        print(k); print("  A:",json.dumps(a.get(k,"<ABSENT>"))[:600]); print("  B:",json.dumps(b.get(k,"<ABSENT>"))[:600])
