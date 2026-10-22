import ast,json,hashlib
from pathlib import Path
p=Path(__file__).parent;g=json.loads((p/'PIN_GRAPH_V002.json').read_text());assert not g['issues']
tokens={'ROUTE_A_NO_FIXED_POINT','ITERATION_BUDGET_EXHAUSTED'}
for name,row in g['modules'].items():
 raw=Path(name).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256'];t=ast.parse(raw)
 parents={id(c):n for n in ast.walk(t) for c in ast.iter_child_nodes(n)};sites=[]
 for n in ast.walk(t):
  if not isinstance(n,ast.Constant) or n.value not in tokens:continue
  parent=parents[id(n)]
  if isinstance(parent,ast.Compare):continue
  if n.value=='ROUTE_A_NO_FIXED_POINT':
   assert isinstance(parent,ast.Assign) and n.lineno in (1916,3566,6107,7853,9066)
   cls='NO_EXCEPTION_OUTCOME' if n.lineno==1916 else 'RouteANoFixedPoint'
   rationale='nonconverged source classification; FAILED_SOURCE_PREPARATION excluded by result gate' if n.lineno==1916 else 'RouteANoFixedPoint exception handler; no fixed point'
  else:
   assert isinstance(parent,ast.Call) and isinstance(parent.func,ast.Name) and parent.func.id=='_finish'
   assert Path(name).name.startswith('coupled_hi_fourier_source_iteration_')
   cls='NO_EXCEPTION_OUTCOME';rationale='terminal _finish after unchanged bounded iteration loop; converged_finite_fixed_point=False'
  sites.append({'token':n.value,'line':n.lineno,'model_outcome':True,'exception_class':cls,'rationale':rationale})
 row['sites']=sorted(sites,key=lambda s:s['line'])
registries={}
for root in g['roots']:
 seen=set();todo=[root]
 while todo:
  q=todo.pop()
  if q in seen:continue
  seen.add(q);todo.extend(r['path'] for r in g['modules'][q]['refs'])
 registries[g['modules'][root]['sha256']]={'complete':True,'root':root,'modules':[{'path':q,**g['modules'][q]} for q in sorted(seen)]}
with (p/'CAUSE_VOCABULARY_CXV002.json').open('x') as f:json.dump(registries,f,sort_keys=True,indent=2)
print(json.dumps({k:{'modules':len(v['modules']),'sites':sum(len(r['sites']) for r in v['modules'])} for k,v in registries.items()}))
