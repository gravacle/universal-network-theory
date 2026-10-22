"""Root0845/0847 capture entry prototype; requires review and external launch binding.
--validate-only verifies helper/source pins and AST inventory, never captures runtime.
"""
import sys,os,ast,json,hashlib,types,argparse,subprocess
from pathlib import Path
from datetime import datetime,timezone
from importlib import metadata
from importlib.machinery import PathFinder
HELPERS={'runtime_policy_cx1v001': 'a20d03fe9a7bc3c4ec0cb9fafa0bbbd8c91b41a43cfbec7f087c4b9468672269', 'runtime_fingerprints_cx1v002': '5ec4f8c652917321c449d84b3272ed6f97504b002312ba8d89da583c1b00fc31', 'runtime_distribution_cx1v001': 'ce5f784dbe2d328a614df2ce2fa6dc24b89817678846c70c0fccef9e98a11228', 'runtime_distribution_bytes_cx1v003': '3af50366d51e0913e3580a78df26fb0e228a00574d44af7410b1c9acf418d000', 'runtime_distribution_owned_bytes_cx1v003': 'ebc90499108f4246e8b7a90ce313827e008dcf614c57df160f2f0817aa0a9eb2', 'runtime_distribution_discovery_cx1v005': '77d0e134738fb4b59c6c1ae038991bdc93e73b9303a1488e00ff44aedeeac194', 'runtime_distribution_record_cx1v004': '13fb69482de279bf758da158763c30d3951d3003bb3958da6ccbe500e317b522'}
SOURCE_PINS=[{'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py', 'sha256': 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'}, {'path': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/ddo_composite_stable_cached_root_worker_v002.py', 'sha256': 'c4cb682669993afbad3c623a010244cc8a31b9fcbacfe44e6bc692bf2d5895a4'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo_homotopy_reference_root_worker_v001_gal_c2v005.py', 'sha256': 'cdf155e8161a89fd78518bbe048fae2b8114a5fb04b0fb770c30a8502308eb7f'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo_saved_root_body_array_root_v002_gal_c2v005.py', 'sha256': '7387493b6e2e153afd0e2352cf630edd32944d641dc563a706381983add0b1e3'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo_body_source_offset_root_v003_gal_c2v005.py', 'sha256': '1ee18dcdcc42fc2465cebcc120297f262839fc4506249416b4d71d6a00be3dd4'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo_fixed_K_free_surface_root_v001_gal_c2v005.py', 'sha256': '2699cc76777621aea33398acb394ec880189399623a24dd0fb6d76e9ed0a0011'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo_free_surface_rotation_root_v001_gal_c2v005.py', 'sha256': 'a49085e96e8b5f241b45e72682140b4b6892fa6171ca8c8d42fc28b0eaa61e85'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo_free_surface_native_feedback_root_v002_gal_c2v005.py', 'sha256': '77ac558786dbe8dc932ff1d902200f85d570f058b903e7253acb31d40a2cb99b'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo_fixed_K_free_surface_root_v003_gal_c2v005.py', 'sha256': '1f473e39a7634e86bc49edfd1a409ca787c92a7031b761b734933e7401d31ba0'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo_fixed_K_free_surface_root_v005_gal_c2v005.py', 'sha256': '99fab2857b3f18e1f05c78da81c9d1dc2b4206e65aaadb4ed0fd78b8a639bea1'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo_free_surface_rotation_root_v005_gal_c2v005.py', 'sha256': 'be1c913f4cfe3f6ccafd5d48bd2fb68856fa080ad8da016091ec237c652bef25'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo_free_surface_native_feedback_root_v004_gal_c2v005.py', 'sha256': 'b3a8424e15343bbf3dc80430d3170f385718eb96d5cc5789fa66e3be5b30b02e'}, {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/stages/ddo12_lower_entropy_column_mean_root_v004_gal_c2v005.py', 'sha256': 'ae78b012d079ceffd62af1dbc8c59c4aaf97cbc30e697eca8b58cd03fb732d38'}]
MONITOR_PIN={'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py', 'sha256': 'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'}
class Refusal(ValueError):pass
def need(ok,reason):
 if not ok:raise Refusal(reason)
def verified(pin):
 raw=Path(pin['path']).read_bytes();need(hashlib.sha256(raw).hexdigest()==pin['sha256'],'PIN_MISMATCH');return raw
def prepare():
 need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1,'ISOLATION_REQUIRED')
 need(hasattr(sys,'stdlib_module_names') and hasattr(metadata,'packages_distributions'),'INTERPRETER_API_REQUIRED')
 root=Path(__file__).resolve().parent
 for name,sha in HELPERS.items():
  need(name not in sys.modules,'HELPER_ALREADY_LOADED')
  path=root/(name+'.py');raw=verified({'path':str(path),'sha256':sha})
  module=types.ModuleType(name);module.__file__=str(path);sys.modules[name]=module
  exec(compile(raw,str(path),'exec'),module.__dict__)
 imports=set()
 for pin in SOURCE_PINS:
  tree=ast.parse(verified(pin))
  for node in ast.walk(tree):
   if isinstance(node,ast.Import):imports.update(x.name.split('.')[0] for x in node.names)
   elif isinstance(node,ast.ImportFrom):
    need(node.level==0,'RELATIVE_IMPORT_UNRESOLVED')
    if node.module:imports.add(node.module.split('.')[0])
 verified(MONITOR_PIN)
 return sorted(imports)
def capture(output,imports):
 need(sys.platform=='darwin','MACOS_REQUIRED');need(not Path(output).exists(),'OUTPUT_EXISTS')
 policy=sys.modules['runtime_policy_cx1v001']
 env=policy.effective_environment(dict(os.environ));need(not any(k.startswith('DYLD') for k in env),'FORBIDDEN_DYLD')
 for key in list(os.environ):
  if key.startswith('PYTHON'):del os.environ[key]
 for key in policy.THREADS:os.environ[key]='1'
 discovery=sys.modules['runtime_distribution_discovery_cx1v005'].discover(import_roots=imports,stdlib_names=sys.stdlib_module_names,search_path=list(sys.path),metadata=metadata,find_spec=PathFinder.find_spec,prefix_root=sys.prefix)
 def fact(command):
  result=subprocess.run(command,check=True,capture_output=True,text=True,timeout=10)
  need(bool(result.stdout.strip()),'PLATFORM_FACT_EMPTY');return result.stdout.strip()
 build=fact(['/usr/bin/sw_vers','-buildVersion']);hardware=fact(['/usr/sbin/sysctl','-n','hw.model'])
 need({k:v for k,v in os.environ.items() if policy.whitelist(k)}==env,'ENVIRONMENT_CHANGED')
 flags={k:getattr(sys.flags,k) for k in dir(sys.flags) if not k.startswith('_') and type(getattr(sys.flags,k)) in (int,bool)}
 path=Path(__file__).resolve()
 record=sys.modules['runtime_distribution_record_cx1v004'].assemble(discovery=discovery,interpreter_path=sys.executable,driver_pin=SOURCE_PINS[0],monitor_pin=MONITOR_PIN,inherited_environment=env,sys_version=sys.version,sys_flags=flags,macos_build=build,hardware_model=hardware,captured_utc=datetime.now(timezone.utc).isoformat(),producer_pin={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 record['source_inventory']=SOURCE_PINS;record['import_roots']=imports;record['helper_pins']=HELPERS
 with Path(output).open('x') as f:json.dump(record,f,indent=2,allow_nan=False);f.write('\n')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--validate-only',action='store_true');parser.add_argument('--output');args=parser.parse_args()
 try:
  imports=prepare()
  if args.validate_only:print('PASS: pinned source inventory only; no runtime capture');return 0
  need(args.output is not None,'OUTPUT_REQUIRED');capture(args.output,imports);return 0
 except (ValueError,OSError,ImportError,subprocess.SubprocessError):
  print('FAIL: capture refused',file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
