from pathlib import Path
import ast,hashlib,json,math,subprocess,resource
E=Path(__file__).parent/'s1_independent'
P=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1')
E.mkdir(exist_ok=False)
checks=[]
def ck(n,x):
    checks.append({'name':n,'pass':bool(x)})
    if not x:raise AssertionError(n)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
pins={'postseal_records_cx1v006_cx3v001.py':'4024d82a8ec59ba339f00214066798ea905d1234466d29db2e8bb5e5869de366','srb_rot_record_cx1v008_cx3v001.py':'2757847a0a2c6da7ab83dc5b203cbfd8c2291da57e430d4ce0cff99ceb4628cc'}
trees={}
for name,pin in pins.items():
    ck('Selected source pin '+name,sha(P/name)==pin)
    trees[name]=ast.parse((P/name).read_bytes())
post=trees['postseal_records_cx1v006_cx3v001.py']
defs=[n for n in post.body if isinstance(n,ast.FunctionDef) and n.name in ('pairs','loads')]
for n in defs:n.decorator_list=[]
scope={'json':json,'math':math}
exec(compile(ast.Module(body=defs,type_ignores=[]),'<exact parser AST; decorators omitted>','exec'),scope)
loads=scope['loads']
for text in ('1e309','-1e309','{"a":1e309}','[0,1e309]','NaN','Infinity','-Infinity','{"a":1,"a":2}'):
    try:loads(text)
    except ValueError:pass
    else:raise AssertionError('parser accepted '+text)
    ck('Parser refusal '+text,True)
for text in ('1e308','-1e308','1e-4000','-0.0','{"a":[1,2.5,null]}'):
    ck('Finite parser equality '+text,loads(text)==json.loads(text))
class Guard:
    def __init__(self,stamp=None,refuse=False):self.calls=[];self.payload=stamp;self.refuse=refuse
    def stamp(self,r,f):self.calls.append('stamp');return r if self.payload is None else self.payload
    def check_run_path(self,p,allow_registered=False):
        self.calls.append('guard')
        if self.refuse:raise ValueError('SYNTHETIC_PATH_REFUSAL')
for name,tree in trees.items():
    main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    tail=main.body[-3:]
    ck('Publication tail starts complete serialization '+name,isinstance(tail[0],ast.Assign) and ast.unparse(tail[0].targets[0])=='serialized' and 'allow_nan=False' in ast.unparse(tail[0]))
    ck('Publication tail checks path second '+name,isinstance(tail[1],ast.Expr) and ast.unparse(tail[1].value).startswith('G.check_run_path('))
    ck('Publication tail single exclusive open '+name,isinstance(tail[2],ast.With) and ast.unparse(tail[2].items[0].context_expr)=="open(out, 'x')")
    code=compile(ast.Module(body=tail,type_ignores=[]),'<exact publication AST suffix>','exec')
    stem=name[:-3]
    for label,rec in [('inf',{'x':float('inf')}),('nan',{'x':float('nan')}),('object',{'x':object()})]:
        out=E/(stem+'_'+label+'.json');g=Guard()
        try:exec(code,{'G':g,'json':json,'rec':rec,'__file__':str(P/name),'out':str(out)})
        except (ValueError,TypeError):pass
        else:raise AssertionError('serialization succeeded '+label)
        ck(name+' serialization refusal precedes guard/open '+label,g.calls==['stamp'] and not out.exists())
    out=E/(stem+'_positive.json');g=Guard();rec={'finite':1.25,'nested':[1,None,False]}
    exec(code,{'G':g,'json':json,'rec':rec,'__file__':str(P/name),'out':str(out)})
    before=out.read_bytes()
    ck(name+' finite output exact legacy json bytes',before==json.dumps(rec,indent=1,allow_nan=False).encode() and not before.endswith(b'\n'))
    ck(name+' publication call order',g.calls==['stamp','guard'])
    try:exec(code,{'G':Guard(),'json':json,'rec':{'replacement':2},'__file__':str(P/name),'out':str(out)})
    except FileExistsError:pass
    else:raise AssertionError('existing output replaced')
    ck(name+' existing output stays unchanged',out.read_bytes()==before)
    refused=E/(stem+'_guard_refused.json');g=Guard(refuse=True)
    try:exec(code,{'G':g,'json':json,'rec':rec,'__file__':str(P/name),'out':str(refused)})
    except ValueError:pass
    else:raise AssertionError('guard refusal ignored')
    ck(name+' synthetic final path guard refusal precedes open',g.calls==['stamp','guard'] and not refused.exists())
for name,pin in pins.items():ck('Source unchanged '+name,sha(P/name)==pin)
result={'date_u':subprocess.check_output(['date','-u'],text=True).strip(),'status':'TESTED_PASS','passed':len(checks),'failed':0,'checks':checks,
 'source_pins':[{'path':str(P/n),'sha256':h} for n,h in pins.items()],
 'scope':'Independent exact AST parser and three-statement publication suffix execution only. Entry decorators omitted and guard replaced by traceable synthetic stub. No full main, comparator, reconstruction, real admission or scientific computation executed. Actual guard behavior is outside this test scope.',
 'failure_bytes_limit':'A filesystem I/O failure after exclusive creation can still leave a partial file; claim is refusal before output creation for JSON serialization/finite failures only.',
 'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'harness':{'path':str(Path(__file__)),'sha256':sha(__file__)},
 'files':[{'path':str(p),'sha256':sha(p)} for p in E.iterdir() if p.is_file()]}
with (E/'RESULTS_CX3V001.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'passed':len(checks),'sha256':sha(E/'RESULTS_CX3V001.json')}))
