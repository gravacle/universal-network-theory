"""D002 read-only extraction from the exact pinned envelope implementation.
No START/END production; observation is an in-memory object, never labelled END.
Root START authentication and required coverage remain caller prerequisites.
"""
import ast,copy,hashlib,types
SHA='9d531381615f7b68f2f33bfc19f0aa2bcfe97a4e6f5c0e93187ea8eb35ce8d9a'
def build(raw,path):
 if hashlib.sha256(raw).hexdigest()!=SHA:raise ValueError('ENVELOPE_TOOL_PIN')
 tree=ast.parse(raw);functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 snapshot=functions['snapshot'];compare=functions['compare']
 def assignment(node,name):return isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets)
 begin=next(i for i,n in enumerate(snapshot.body) if assignment(n,'plist'))
 end=next(i for i,n in enumerate(snapshot.body) if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='write_signed')
 obs=ast.parse("def observe(ps,ps_fsha,pins_path):\n label='observation'\n").body[0]
 obs.body+=copy.deepcopy(snapshot.body[begin:end])+[ast.Return(value=ast.Name(id='man',ctx=ast.Load()))]
 begin=next(i for i,n in enumerate(compare.body) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and any(isinstance(a,ast.Constant) and isinstance(a.value,str) and a.value.startswith('PHASE_DIFFERS') for a in ast.walk(n.value)))
 end=next(i for i,n in enumerate(compare.body) if assignment(n,'verdict'))
 cmp=ast.parse("def compare_observation(s,e):\n pass\n").body[0];cmp.body=copy.deepcopy(compare.body[begin:end])
 class Labels(ast.NodeTransformer):
  def visit_Constant(self,node):
   if isinstance(node.value,str):node.value=node.value.replace('END','OBSERVATION').replace('end','observation')
   return node
 cmp=Labels().visit(cmp)
 cmp.body.append(ast.Return(value=ast.Dict(keys=[ast.Constant('problems'),ast.Constant('notes')],values=[ast.Name(id='problems',ctx=ast.Load()),ast.Name(id='notes',ctx=ast.Load())])))
 generated=ast.fix_missing_locations(ast.Module(body=[obs,cmp],type_ignores=[]))
 for n in ast.walk(generated):
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('write_signed','check_out','snapshot','compare'):raise ValueError('OBSERVATION_WRITE_OR_FINAL_CALL')
 module=types.ModuleType('_cx1_readonly_envelope');module.__file__=path
 exec(compile(raw,path,'exec'),module.__dict__)
 exec(compile(generated,path+'#D002-readonly','exec'),module.__dict__)
 return module,ast.unparse(generated)
