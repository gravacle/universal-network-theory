"""Private loader for already root-pinned helper inventories, not a security sandbox.
Verify and compile every inventory byte buffer before executing any helper. Scientific
source inventory and runtime capture execution are outside this loader's remit.
"""
import ast,builtins,hashlib,types,sys
from pathlib import Path

def prepare(components,*,runtime_modules=None):
 runtime_modules={} if runtime_modules is None else dict(runtime_modules)
 if set(runtime_modules)-{'numpy'}:raise ValueError('UNSUPPORTED_RUNTIME_MODULE')
 for name,module in runtime_modules.items():
  if not isinstance(module,types.ModuleType) or module.__name__!=name or sys.modules.get(name) is not module:raise ValueError('RUNTIME_MODULE_IDENTITY')
 if type(components) is not dict or not components:raise ValueError('HELPER_INVENTORY')
 raw={};code={};modules={};active=set()
 for name,pin in components.items():
  if not name.endswith('.py') or not name[:-3].isidentifier() or type(pin) is not dict or set(pin)!={'path','sha256'}:raise ValueError('HELPER_PIN_SHAPE')
  path=Path(pin['path'])
  if not path.is_absolute() or str(path.resolve())!=str(path) or path.name!=name:raise ValueError('HELPER_PATH')
  data=path.read_bytes()
  if hashlib.sha256(data).hexdigest()!=pin['sha256']:raise ValueError('HELPER_HASH:'+name)
  raw[name[:-3]]=(str(path),data)
 for name,(path,data) in raw.items():
  tree=ast.parse(data,filename=path)
  for n in ast.walk(tree):
   roots=[]
   if isinstance(n,ast.Import):roots=[a.name.split('.')[0] for a in n.names]
   elif isinstance(n,ast.ImportFrom):
    if n.level:raise ValueError('RELATIVE_HELPER_IMPORT')
    if n.module:roots=[n.module.split('.')[0]]
   for root in roots:
    if root not in raw and root not in runtime_modules and root not in sys.stdlib_module_names:raise ValueError('UNPINNED_IMPORT:'+root)
  code[name]=compile(tree,path,'exec')
 def load(name):
  if name not in raw:raise ValueError('HELPER_NOT_SELECTED:'+name)
  if name in active:raise ValueError('HELPER_IMPORT_CYCLE:'+name)
  if name in modules:return modules[name]
  module=types.ModuleType(name);module.__file__=raw[name][0]
  def private_import(target,globals=None,locals=None,fromlist=(),level=0):
   root=target.split('.')[0]
   if level:raise ValueError('RELATIVE_HELPER_IMPORT')
   if root in raw:
    if target!=root:raise ValueError('HELPER_SUBMODULE_IMPORT')
    return load(root)
   if root in runtime_modules:
    if target!=root:raise ValueError('RUNTIME_SUBMODULE_IMPORT')
    return runtime_modules[root]
   if root not in sys.stdlib_module_names:raise ValueError('UNPINNED_DYNAMIC_IMPORT:'+root)
   return builtins.__import__(target,globals,locals,fromlist,level)
  module.__dict__['__builtins__']=dict(vars(builtins),__import__=private_import)
  active.add(name)
  try:exec(code[name],module.__dict__)
  finally:active.remove(name)
  modules[name]=module;return module
 return load
