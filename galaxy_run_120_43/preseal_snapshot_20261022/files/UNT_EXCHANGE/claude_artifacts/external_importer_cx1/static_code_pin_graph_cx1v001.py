"""Conservative source-only pin graph. Never imports or executes audited source."""
import ast,hashlib,json,re
from pathlib import Path

def constants(tree,path):
 env={'__file__':str(path)};unresolved=[]
 def value(n):
  if isinstance(n,ast.Constant):return n.value
  if isinstance(n,ast.Name):return env[n.id]
  if isinstance(n,ast.Call) and not n.keywords:
   if isinstance(n.func,ast.Name) and n.func.id=='Path' and len(n.args)==1:return Path(value(n.args[0]))
   if isinstance(n.func,ast.Attribute) and n.func.attr=='resolve' and not n.args:
    obj=value(n.func.value)
    if isinstance(obj,Path):return obj.resolve()
  if isinstance(n,ast.Attribute) and n.attr=='parent':
   obj=value(n.value)
   if isinstance(obj,Path):return obj.parent
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):
   left,right=value(n.left),value(n.right)
   if isinstance(left,Path) and type(right) is str:return left/right
  if isinstance(n,(ast.Tuple,ast.List)):return tuple(value(x) for x in n.elts)
  if isinstance(n,ast.Dict):return {value(k):value(v) for k,v in zip(n.keys,n.values)}
  raise ValueError('unsupported expression')
 for node in tree.body:
  if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
   name=node.targets[0].id
   try:env[name]=value(node.value)
   except (ValueError,KeyError,TypeError):
    unresolved.append({'name':name,'line':node.lineno})
 return env,unresolved

def code_pairs(value):
 if isinstance(value,(list,tuple)) and len(value)==2 and isinstance(value[0],(Path,str)) and str(value[0]).endswith('.py') and type(value[1]) is str and re.fullmatch('[0-9a-f]{64}',value[1]):
  yield Path(value[0]),value[1]
 elif isinstance(value,dict):
  for v in value.values():yield from code_pairs(v)
 elif isinstance(value,(list,tuple)):
  for v in value:yield from code_pairs(v)

def audit(seeds,limit=256):
 queue=list(seeds);seen=set();records=[];edges=[];blocked=[]
 while queue:
  path,expected=queue.pop(0);path=Path(path);key=(str(path),expected)
  if key in seen:continue
  seen.add(key)
  if len(seen)>limit:raise ValueError('AUDIT_LIMIT')
  real=path.resolve()
  if path.suffix!='.py' or any(x in str(real) for x in ['/runs/','/runs_ext/','C5H','/UVT_']):
   blocked.append({'path':str(path),'reason':'SOURCE_BOUNDARY'});continue
  raw=path.read_bytes();actual=hashlib.sha256(raw).hexdigest()
  if actual!=expected:
   blocked.append({'path':str(path),'expected':expected,'actual':actual,'reason':'PIN_MISMATCH'});continue
  tree=ast.parse(raw);env,unresolved=constants(tree,path)
  imports=[ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
  for name,v in env.items():
   for child,sha in code_pairs(v):
    edges.append({'from':str(path),'constant':name,'to':str(child),'sha256':sha});queue.append((child,sha))
  records.append({'path':str(path),'sha256':actual,'imports':imports,'unresolved_assignments':unresolved})
 return {'schema':'CX1_STATIC_CODE_PIN_GRAPH_V001','coverage_complete':False,'records':records,'edges':edges,'blocked':blocked,'limits':['Literal top-level pin tuples only; dynamic CLI/spec patches and runtime branching unresolved','No module execution; no package runtime identity captured','Includes conservative unused constant pins; does not establish selected execution graph']}
