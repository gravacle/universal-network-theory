"""0843 runtime comparison primitives. Capture/authentication/coverage are separate prerequisites."""
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
class RuntimeRefusal(ValueError):pass

def need(ok,reason):
 if not ok:raise RuntimeRefusal(reason)

def whitelist(name):
 return name in THREADS or name in ('PATH','LANG','TMPDIR') or name.startswith(('PYTHON','DYLD','LC_'))

def effective_environment(inherited):
 need(type(inherited) is dict and all(type(k) is str and type(v) is str for k,v in inherited.items()),'ENVIRONMENT_STRINGS_REQUIRED')
 # Exact monitor normalization: PYTHON* removed, all six thread variables set to 1.
 # DYLD* is retained here so policy refuses it instead of concealing its presence.
 out={k:v for k,v in inherited.items() if whitelist(k) and not k.startswith('PYTHON')}
 out.update({k:'1' for k in THREADS})
 return out

def validate_record(r):
 need(type(r) is dict and r.get('schema')=='CX1_RUNTIME_CAPTURE_V001','RUNTIME_SCHEMA')
 need(r.get('coverage_complete') is True,'RUNTIME_COVERAGE_INCOMPLETE')
 env=r.get('effective_environment')
 need(type(env) is dict and all(type(k) is str and type(v) is str and whitelist(k) for k,v in env.items()),'RUNTIME_ENV_WHITELIST')
 need(not any(k.startswith(('PYTHON','DYLD')) for k in env),'RUNTIME_FORBIDDEN_ENV')
 need(all(env.get(k)=='1' for k in THREADS),'RUNTIME_THREAD_ENV')
 def sha(s):return type(s) is str and len(s)==64 and all(c in '0123456789abcdef' for c in s)
 interp=r.get('interpreter') or {}
 need(sha(interp.get('sha256')) and type(interp.get('realpath')) is str and interp['realpath'].startswith('/'),'RUNTIME_INTERPRETER')
 need(type(r.get('sys_version')) is str and bool(r['sys_version']) and type(r.get('sys_flags')) is dict,'RUNTIME_SYS_METADATA')
 need(type(r.get('macos_build')) is str and bool(r['macos_build']) and type(r.get('hardware_model')) is str and bool(r['hardware_model']),'RUNTIME_PLATFORM')
 modules=r.get('modules');need(type(modules) is list and bool(modules),'RUNTIME_MODULES')
 names=[];comparison=[]
 for m in modules:
  need(type(m) is dict and type(m.get('name')) is str and bool(m['name']) and type(m.get('version')) is str and bool(m['version']) and sha(m.get('sha256')),'RUNTIME_MODULE_IDENTITY')
  canonical=m.get('canonical_name')
  need(type(canonical) is str and bool(canonical),'RUNTIME_CANONICAL_NAME')
  names.append(m['name']);comparison.append((m['name'],canonical,m['version'],m['sha256']))
 need(len(names)==len(set(names)) and {'numpy','scipy'}.issubset(names),'RUNTIME_MODULE_COVERAGE')
 by_name={m['name']:m for m in modules}
 for m in modules:
  canonical=by_name.get(m['canonical_name'])
  need(canonical is not None and canonical['canonical_name']==canonical['name'] and (canonical['version'],canonical['sha256'])==(m['version'],m['sha256']),'RUNTIME_ALIAS_ASSOCIATION')
 return {'interpreter_sha256':interp['sha256'],'modules':sorted(comparison),'threads':{k:env[k] for k in THREADS},'macos_build':r['macos_build']}

def compare_records(direct,campaign):
 a=validate_record(direct);b=validate_record(campaign)
 differences=[k for k in a if a[k]!=b[k]]
 need(not differences,'RUNTIME_MISMATCH:'+','.join(differences))
 return {'prerequisites_only':True,'equal_fields':list(a),'not_compared':['interpreter realpath','sys_version','sys_flags','hardware_model','PATH','LC_*','LANG','TMPDIR','module paths']}
