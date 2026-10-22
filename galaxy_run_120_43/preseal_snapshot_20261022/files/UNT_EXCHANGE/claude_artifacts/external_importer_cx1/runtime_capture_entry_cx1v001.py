"""Uninstalled launch-time capture entry. Requires a separately reviewed, byte-pinned inventory.
--validate-only checks the contract; it is never runtime or launch evidence.
No driver execution. Importing reviewed dependencies is permitted only in capture mode.
"""
import sys,os,json,hashlib,argparse,types,importlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
HELPERS = {'runtime_policy_cx1v001': 'a20d03fe9a7bc3c4ec0cb9fafa0bbbd8c91b41a43cfbec7f087c4b9468672269', 'runtime_fingerprints_cx1v002': '5ec4f8c652917321c449d84b3272ed6f97504b002312ba8d89da583c1b00fc31', 'runtime_capture_assembly_cx1v001': '71386d7a06f3d010fc2d0c842fca2142b1527e7fef1870f4fa816b340e816251'}
class Refusal(ValueError): pass
def need(ok,reason):
 if not ok: raise Refusal(reason)
def strict(raw):
 def pairs(items):
  d={}
  for k,v in items:
   need(k not in d,'DUPLICATE_JSON_KEY');d[k]=v
  return d
 def constant(_):raise Refusal('NONFINITE_JSON')
 return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=constant)
def preflight(args):
 need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1,'REQUIRE_ISOLATED_NO_BYTECODE')
 raw=Path(args.inventory).read_bytes()
 need(hashlib.sha256(raw).hexdigest()==args.inventory_sha256,'INVENTORY_HASH')
 inv=strict(raw)
 need(type(inv) is dict and inv.get('schema')=='CX1_RUNTIME_INVENTORY_V001','INVENTORY_SCHEMA')
 need(inv.get('unresolved_dynamic')==[],'UNRESOLVED_DYNAMIC')
 names=inv.get('module_names')
 need(type(names) is list and all(type(n) is str and n and all(x.isidentifier() for x in n.split('.')) for n in names),'MODULE_NAMES')
 need(len(names)==len(set(names)) and {'numpy','scipy'}.issubset(names),'MODULE_COVERAGE')
 need(inv.get('audit_complete') is True,'INVENTORY_AUDIT_REQUIRED')
 need(not any(k.startswith('DYLD') for k in os.environ),'FORBIDDEN_DYLD')
 return inv
def load_helpers():
 root=Path(__file__).resolve().parent
 for name,expected in HELPERS.items():
  need(name not in sys.modules,'HELPER_ALREADY_LOADED')
  p=root/(name+'.py');raw=p.read_bytes()
  need(hashlib.sha256(raw).hexdigest()==expected,'HELPER_HASH')
  m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m
  exec(compile(raw,str(p),'exec'),m.__dict__)
 return sys.modules['runtime_capture_assembly_cx1v001']
def capture(args,inv):
 need(sys.platform=='darwin','MACOS_REQUIRED')
 need(args.output is not None,'OUTPUT_REQUIRED')
 need(not Path(args.output).exists(),'OUTPUT_EXISTS')
 assembly=load_helpers();policy=sys.modules['runtime_policy_cx1v001']
 env=policy.effective_environment(dict(os.environ))
 for k in list(os.environ):
  if k.startswith('PYTHON'):del os.environ[k]
 for k in policy.THREADS:os.environ[k]='1'
 for name in inv['module_names']:importlib.import_module(name)
 # Include transitive imports and capture-tool imports conservatively. Unknown
 # file/version identities refuse rather than silently dropping a module.
 modules={n:m for n,m in sys.modules.copy().items() if m is not None and n!='__main__' and n not in HELPERS}
 names=sorted(modules)
 expanded={**inv,'module_names':names,'requested_module_names':inv['module_names']}
 flags={n:getattr(sys.flags,n) for n in dir(sys.flags) if not n.startswith('_') and type(getattr(sys.flags,n)) in (int,bool)}
 def fact(command):
  r=subprocess.run(command,check=True,capture_output=True,text=True,timeout=10)
  value=r.stdout.strip();need(bool(value),'EMPTY_PLATFORM_FACT');return value
 record=assembly.assemble(inventory=expanded,resolved_modules=modules,package_roots=modules,
  inherited_environment=env,interpreter_path=sys.executable,sys_version=sys.version,
  sys_flags=flags,stdlib_names=sys.stdlib_module_names,
  macos_build=fact(['/usr/bin/sw_vers','-buildVersion']),
  hardware_model=fact(['/usr/sbin/sysctl','-n','hw.model']),
  captured_utc=datetime.now(timezone.utc).isoformat(),
  producer_pin={'path':str(Path(__file__).resolve()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
 record['inventory_pin']={'path':str(Path(args.inventory).resolve()),'sha256':args.inventory_sha256}
 record['helper_pins']=HELPERS
 # Root supplies launch association externally; this record alone never proves it.
 record['launch_association']='REQUIRES_ROOT_BINDING'
 with Path(args.output).open('x') as f:json.dump(record,f,indent=2,allow_nan=False);f.write('\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('--inventory',required=True);p.add_argument('--inventory-sha256',required=True);p.add_argument('--output');p.add_argument('--validate-only',action='store_true');a=p.parse_args()
 try:
  inv=preflight(a)
  if a.validate_only:print('PASS: inventory contract only; no runtime capture');return 0
  capture(a,inv);return 0
 except (ValueError,OSError,ImportError,subprocess.SubprocessError):
  # Do not echo exception payloads, paths, environment values, or imported data.
  print('FAIL: capture refused',file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
