from pathlib import Path
import hashlib,json,ast,difflib,subprocess
P=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1')
E=Path(__file__).parent/'s1_independent'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(n):return ast.dump(n,include_attributes=False)
checks=[];deltas=[]
for old,new in [('postseal_records_cx1v006.py','postseal_records_cx1v006_cx3v001.py'),('srb_rot_record_cx1v008.py','srb_rot_record_cx1v008_cx3v001.py')]:
    a=(P/old).read_text();b=(P/new).read_text();aa=ast.parse(a);bb=ast.parse(b)
    assert len(aa.body)==len(bb.body)
    changed=[(x,y) for x,y in zip(aa.body,bb.body) if dump(x)!=dump(y)]
    names=[getattr(x,'name',type(x).__name__) for x,y in changed]
    expected=['loads','main'] if old.startswith('postseal') else ['Import','main']
    assert names==expected,(old,names)
    checks.append({'name':old+' changed AST top-level nodes only','pass':True,'nodes':names})
    for x,y in changed:
        if isinstance(x,ast.FunctionDef) and x.name=='main':
            assert len(y.body)==len(x.body)+1
            assert [dump(z) for z in x.body[:-2]]==[dump(z) for z in y.body[:-3]]
            assert dump(x.body[-2])==dump(y.body[-2])
            before=x.body[-1];after=y.body[-1]
            assert dump(before.items[0])==dump(after.items[0])
            oldcall=before.body[0].value;newcall=y.body[-3].value
            assert ast.unparse(oldcall.func)=='json.dump' and ast.unparse(newcall.func)=='json.dumps'
            assert dump(oldcall.args[0])==dump(newcall.args[0]) and len(newcall.args)==1
            assert ast.unparse(oldcall.args[1])=='f'
            assert [dump(z) for z in oldcall.keywords]==[dump(z) for z in newcall.keywords]
            assert ast.unparse(after.body[0])=='f.write(serialized)'
            checks.append({'name':old+' exact publication-only main AST delta','pass':True})
        elif isinstance(x,ast.FunctionDef) and x.name=='loads':
            assert len(x.body)==2 and len(y.body)==3
            assert dump(x.body[0])==dump(y.body[0])
            newret=y.body[-1].value;oldret=x.body[-1].value
            assert dump(newret.func)==dump(oldret.func) and [dump(z) for z in newret.args]==[dump(z) for z in oldret.args]
            assert [dump(z) for z in newret.keywords[:-1]]==[dump(z) for z in oldret.keywords]
            assert newret.keywords[-1].arg=='parse_float' and ast.unparse(newret.keywords[-1].value)=='finite_float'
            assert y.body[1].name=='finite_float'
            checks.append({'name':old+' parser adds only finite_float hook and local finite check','pass':True})
        else:
            assert ast.unparse(x)=='import postseal_records_cx1v006 as C'
            assert ast.unparse(y)=='import postseal_records_cx1v006_cx3v001 as C'
            checks.append({'name':old+' sole dependency import follows successor','pass':True})
    text=''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=old,tofile=new))
    out=E/(new+'.diff.txt')
    with out.open('x') as f:f.write(text)
    deltas.append({'old':{'path':str(P/old),'sha256':sha(P/old)},'new':{'path':str(P/new),'sha256':sha(P/new)},'diff':{'path':str(out),'sha256':sha(out)}})
r={'date_u':subprocess.check_output(['date','-u'],text=True).strip(),'status':'TESTED_PASS','passed':len(checks),'checks':checks,'deltas':deltas,
 'scope':'Exact AST source-delta audit; runtime semantics outside independently executed parser/publication slices remain source inference.',
 'prior_harness_attempt':'A first inline audit wrongly assumed the old writer was f.write(json.dumps(...)); its AST assertion failed before artifact writes. The actual predecessor is json.dump(...,f). This corrected audit verifies the exact dump-to-dumps change. No producer source changed.',
 'harness':{'path':str(Path(__file__)),'sha256':sha(__file__)}}
p=E/'SOURCE_DELTA_CX3V002.json'
with p.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(json.dumps({'passed':len(checks),'sha256':sha(p)},indent=2))
