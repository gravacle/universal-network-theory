"""Runtime record under root rulings 0845/0847. Capture facts require root launch binding."""
from pathlib import PurePosixPath
from datetime import datetime
from runtime_policy_cx1v001 import effective_environment,whitelist,THREADS,need
from runtime_fingerprints_cx1v002 import FileFingerprints

def sha(x):return type(x) is str and len(x)==64 and all(c in '0123456789abcdef' for c in x)
def validate(record):
 need(type(record) is dict and record.get('schema')=='CX1_RUNTIME_DISTRIBUTIONS_V001','RUNTIME_SCHEMA')
 need(record.get('coverage_definition')=='ROOT_0845_0847','RUNTIME_COVERAGE_RULE')
 env=record.get('effective_environment')
 need(type(env) is dict and all(type(k) is str and type(v) is str and whitelist(k) for k,v in env.items()),'RUNTIME_ENV')
 need(not any(k.startswith(('PYTHON','DYLD')) for k in env),'RUNTIME_FORBIDDEN_ENV')
 need(all(env.get(k)=='1' for k in THREADS),'RUNTIME_THREADS')
 producer=record.get('producer')
 need(type(producer) is dict and type(producer.get('path')) is str and producer['path'].startswith('/') and sha(producer.get('sha256')),'RUNTIME_PRODUCER')
 try:captured=datetime.fromisoformat(record.get('captured_utc','').replace('Z','+00:00'))
 except (ValueError,TypeError,AttributeError):need(False,'RUNTIME_CAPTURE_TIME')
 need(captured.tzinfo is not None,'RUNTIME_CAPTURE_TIMEZONE')
 identities={}
 for k in ('interpreter','driver','monitor'):
  pin=record.get(k) or {};need(sha(pin.get('sha256')) and type(pin.get('realpath')) is str and pin['realpath'].startswith('/'),'RUNTIME_PIN:'+k)
  identities[k]=pin['sha256']
 for k in ('sys_version','macos_build','hardware_model','captured_utc'):
  need(type(record.get(k)) is str and bool(record[k]),'RUNTIME_METADATA:'+k)
 flags=record.get('sys_flags');need(type(flags) is dict and flags.get('isolated')==1 and flags.get('dont_write_bytecode')==1,'RUNTIME_FLAGS')
 rows=record.get('distributions');need(type(rows) is list and bool(rows),'RUNTIME_DISTRIBUTIONS')
 packages={}
 for row in rows:
  need(type(row) is dict,'DISTRIBUTION_ROW')
  name=row.get('name');need(type(name) is str and name and name not in packages,'DISTRIBUTION_NAME')
  need(type(row.get('version')) is str and bool(row['version']) and sha(row.get('sha256')) and row.get('identity_basis')=='sorted_relative_names_and_file_bytes_v001','DISTRIBUTION_IDENTITY')
  need(type(row.get('files')) is list and bool(row['files']),'DISTRIBUTION_FILE_EVIDENCE')
  paths=[]
  for item in row['files']:
   need(type(item) is dict,'DISTRIBUTION_FILE_ROW')
   path=item.get('path');need(type(path) is str and bool(path) and not PurePosixPath(path).is_absolute() and '..' not in PurePosixPath(path).parts and str(PurePosixPath(path))==path,'DISTRIBUTION_RELATIVE_PATH')
   need(type(item.get('size')) is int and item['size']>=0 and sha(item.get('sha256')),'DISTRIBUTION_FILE_IDENTITY')
   need(type(item.get('outside_RECORD')) is bool and type(item.get('excluded_from_equality')) is bool,'DISTRIBUTION_FILE_FLAGS')
   need(item['excluded_from_equality']==('__pycache__' in PurePosixPath(path).parts),'DISTRIBUTION_EXCLUSION_RULE')
   paths.append(path)
  need(paths==sorted(set(paths)),'DISTRIBUTION_FILE_ORDER')
  packages[name]=(row['version'],row['sha256'])
 bindings=record.get('import_bindings');need(type(bindings) is list,'IMPORT_BINDINGS')
 imports={}
 for bind in bindings:
  need(type(bind) is dict and type(bind.get('origin')) is str and bind['origin'].startswith('/'),'IMPORT_ORIGIN')
  name=bind.get('import');need(type(name) is str and name and name not in imports and bind.get('distribution') in packages,'IMPORT_ASSOCIATION')
  imports[name]=bind['distribution']
 need({'numpy','scipy'}.issubset(imports),'MANDATORY_PACKAGES')
 need(set(imports.values())==set(packages),'UNASSOCIATED_DISTRIBUTION')
 identities.update(packages=packages,imports=imports,threads={k:env[k] for k in THREADS},macos_build=record['macos_build'])
 return identities

def assemble(*,discovery,interpreter_path,driver_pin,monitor_pin,inherited_environment,sys_version,sys_flags,macos_build,hardware_model,captured_utc,producer_pin):
 files=FileFingerprints()
 pins={'interpreter':files.capture(interpreter_path)}
 for name,pin in [('driver',driver_pin),('monitor',monitor_pin)]:
  actual=files.capture(pin['path']);need(actual['sha256']==pin['sha256'],'PIN_MISMATCH:'+name);pins[name]=actual
 record=dict(schema='CX1_RUNTIME_DISTRIBUTIONS_V001',coverage_definition='ROOT_0845_0847',scientific_module_identity='Same pinned driver; exec_verified lines 577-586 and SCRIPTS table enforce scientific module pins per root0845.',**pins,**discovery,effective_environment=effective_environment(inherited_environment),sys_version=sys_version,sys_flags=sys_flags,macos_build=macos_build,hardware_model=hardware_model,captured_utc=captured_utc,producer=producer_pin,launch_association='REQUIRES_ROOT_BINDING')
 validate(record);return record

def compare(a,b):
 need(validate(a)==validate(b),'RUNTIME_MISMATCH')
 return {'equal_under':'ROOT_0845_0847','launch_association_verified':False}
