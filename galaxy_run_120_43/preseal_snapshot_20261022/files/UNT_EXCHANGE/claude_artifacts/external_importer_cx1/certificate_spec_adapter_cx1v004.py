"""Private certificate method adapter for 0841 explicit original specs.
Uninstalled. Caller supplies an authenticated resolver; this is not admission.
Only the original-spec expression changes. No path aliases or evidence writes.
"""
import ast,hashlib,types
from snapshot_cx1v001 import Refusal
METHOD_SOURCE_SHA='d6fd4515f16647e1be781ab069039ba0d8c4ac923a440adaa78106d87ce843b4'

def build_checker(raw, filename, private_wrapper, *, expected_sha256):
    if hashlib.sha256(raw).hexdigest()!=expected_sha256:raise Refusal('WRAPPER_VERSION')
    tree=ast.parse(raw)
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Context')
    fn=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='certificate_check')
    if hashlib.sha256(ast.get_source_segment(raw.decode('utf-8'),fn).encode('utf-8')).hexdigest()!=METHOD_SOURCE_SHA:raise Refusal('WRAPPER_CERTIFICATE_METHOD_CHANGED')
    found=0
    for n in ast.walk(fn):
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='actual_spec':
            if ast.dump(n.value)!=ast.dump(ast.parse("directory/'spec.json'",mode='eval').body):raise Refusal('SPEC_EXPRESSION_CHANGED')
            # Resolver returns the actual source path for an authenticated direct
            # binding, or the unchanged local path for a local campaign call.
            n.value=ast.parse('self._cx1_original_spec_path(directory)',mode='eval').body
            found+=1
    if found!=1:raise Refusal('SPEC_EXPRESSION_COUNT')
    fn.name='certificate_check_external'
    code=compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),filename,'exec')
    temporary={};exec(code,temporary)
    # Use the private module globals so the existing single-read scope still
    # applies to Path/O/M/G; shared modules and the original method are untouched.
    f=temporary[fn.name]
    adapted=types.FunctionType(f.__code__,private_wrapper.__dict__,fn.name,f.__defaults__)
    adapted.__kwdefaults__=f.__kwdefaults__
    return adapted
