import ast,json,re,hashlib
from pathlib import Path
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
roots=[BASE/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',BASE/'ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py']
class Unknown(Exception):pass
def evaluate(n,env):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.Name):
  if n.id in env:return env[n.id]
  raise Unknown()
 if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):return Path(evaluate(n.left,env))/evaluate(n.right,env)
 if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add):return evaluate(n.left,env)+evaluate(n.right,env)
 if isinstance(n,(ast.Tuple,ast.List)):return tuple(evaluate(x,env) for x in n.elts)
 if isinstance(n,ast.Dict):
  out={}
  for k,v in zip(n.keys,n.values):
   try:out[evaluate(k,env)]=evaluate(v,env)
   except (Unknown,TypeError,KeyError):pass
  return out
 if isinstance(n,ast.Subscript):return evaluate(n.value,env)[evaluate(n.slice,env)]
 if isinstance(n,ast.Attribute) and n.attr=='parent':return Path(evaluate(n.value,env)).parent
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('Path','str') and len(n.args)==1:
  return (Path if n.func.id=='Path' else str)(evaluate(n.args[0],env))
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='resolve' and not n.args:return Path(evaluate(n.func.value,env)).absolute()
 raise Unknown()
def scan(p):
 raw=p.read_bytes();tree=ast.parse(raw);env={'__file__':str(p)}
 # Only evaluate expressions with the above literal/path whitelist; never execute source.
 for node in tree.body:
  if isinstance(node,ast.Assign):
   try:v=evaluate(node.value,env)
   except (Unknown,TypeError,KeyError,ValueError):continue
   for t in node.targets:
    if isinstance(t,ast.Name):env[t.id]=v
 refs=[];unresolved=[]
 for n in ast.walk(tree):
  if isinstance(n,(ast.Tuple,ast.List)) and len(n.elts)==2:
   try:h=evaluate(n.elts[1],env)
   except (Unknown,TypeError,KeyError,ValueError):continue
   if not isinstance(h,str) or not re.fullmatch('[0-9a-f]{64}',h):continue
   try:q=str(evaluate(n.elts[0],env))
   except (Unknown,TypeError,KeyError,ValueError):
    unresolved.append({'line':n.lineno,'expression':ast.unparse(n),'sha256':h});continue
   if q.endswith('.py'):refs.append({'path':q,'sha256':h,'line':n.lineno})
 # Companion PATH/SHA constants are also pinned imports.
 for key,h in env.items():
  if isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h):
   stem=re.sub(r'_SHA(?:256)?$', '',key)
   for k in (stem,stem+'_PATH'):
    q=env.get(k)
    if isinstance(q,(str,Path)) and str(q).endswith('.py'):
     refs.append({'path':str(q),'sha256':h,'line':0})
 # Literal path/sha dicts and explicit hash-comparison arguments.
 for node in ast.walk(tree):
  if isinstance(node,ast.Dict):
   for k,v in zip(node.keys,node.values):
    try:q,h=str(evaluate(k,env)),evaluate(v,env)
    except (Unknown,TypeError,KeyError,ValueError):continue
    if q.endswith('.py') and isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h):refs.append({'path':q,'sha256':h,'line':node.lineno})
  if isinstance(node,ast.Compare) and len(node.comparators)==1 and isinstance(node.left,ast.Call) and len(node.left.args)==1:
   try:q,h=str(evaluate(node.left.args[0],env)),evaluate(node.comparators[0],env)
   except (Unknown,TypeError,KeyError,ValueError):continue
   if q.endswith('.py') and isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h):refs.append({'path':q,'sha256':h,'line':node.lineno})
 return raw,refs,unresolved
queue=list(roots);seen={};issues=[]
while queue:
 p=queue.pop(0)
 if str(p) in seen:continue
 if not p.is_absolute() or any(x in p.parts for x in ('runs','runs_ext')) or 'C5H' in str(p):
  issues.append({'path':str(p),'reason':'EXCLUDED_PATH'});continue
 try:raw,refs,u=scan(p)
 except (OSError,SyntaxError) as e:issues.append({'path':str(p),'reason':type(e).__name__});continue
 seen[str(p)]={'sha256':hashlib.sha256(raw).hexdigest(),'refs':refs,'unresolved':u}
 queue.extend(Path(x['path']) for x in refs)
 if len(seen)>1000:raise RuntimeError('bound')
for p,row in seen.items():
 for ref in row['refs']:
  if ref['path'] in seen and seen[ref['path']]['sha256']!=ref['sha256']:issues.append({'parent':p,**ref,'reason':'HASH_MISMATCH'})
obj={'roots':[str(p) for p in roots],'modules':seen,'issues':issues}
with (Path(__file__).parent/'PIN_GRAPH_V002.json').open('x') as f:json.dump(obj,f,indent=2)
print(json.dumps({'modules':len(seen),'issues':issues,'unresolved':[{ 'path':p,'sites':r['unresolved']} for p,r in seen.items() if r['unresolved']]},indent=2))
