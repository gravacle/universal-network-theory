"""Private parent classifier adaptation: original spec physical path only.
Uninstalled; requires authenticated ctx._cx1_original_spec_path resolver.
"""
import ast,hashlib,types
from snapshot_cx1v001 import Refusal
SHA='c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'

def build_classifier(raw,filename,private_parent):
    if hashlib.sha256(raw).hexdigest()!=SHA:raise Refusal('PARENT_VERSION')
    tree=ast.parse(raw)
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='CampaignExecutor')
    fn=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='_classify')
    target=ast.dump(ast.parse("d/'spec.json'",mode='eval').body)
    class Adapt(ast.NodeTransformer):
        count=0
        def visit_BinOp(self,node):
            if ast.dump(node)==target:
                self.count+=1
                return ast.copy_location(ast.parse('ctx._cx1_original_spec_path(d)',mode='eval').body,node)
            return self.generic_visit(node)
    transform=Adapt();fn=transform.visit(fn)
    if transform.count!=2:raise Refusal('PARENT_SPEC_PATH_COUNT')
    fn.name='_classify_external';temp={}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),filename,'exec'),temp)
    f=temp[fn.name]
    adapted=types.FunctionType(f.__code__,private_parent.__dict__,fn.name,f.__defaults__)
    adapted.__kwdefaults__=f.__kwdefaults__
    return adapted
