"""Runtime capture assembly. Inputs must be measured by a launch-time entry, not supplied by candidates.
This library does not discover imports or authenticate the audited inventory.
"""
from runtime_policy_cx1v002 import effective_environment,validate_record,need
from runtime_fingerprints_cx1v002 import FileFingerprints,module_fingerprint

def assemble(*, inventory, resolved_modules, package_roots, inherited_environment,
             interpreter_path, sys_version, sys_flags, stdlib_names, macos_build,
             hardware_model, captured_utc, producer_pin, files=None):
 need(type(inventory) is dict and inventory.get('schema')=='CX1_RUNTIME_INVENTORY_V001','CAPTURE_INVENTORY_SCHEMA')
 need(inventory.get('unresolved_dynamic')==[],'CAPTURE_UNRESOLVED_DYNAMIC')
 names=inventory.get('module_names')
 need(type(names) is list and all(type(n) is str and n for n in names) and len(names)==len(set(names)) and {'numpy','scipy'}.issubset(names),'CAPTURE_INVENTORY_NAMES')
 need(type(resolved_modules) is dict and set(resolved_modules)==set(names),'CAPTURE_RESOLUTION_COVERAGE')
 need(type(sys_flags) is dict and sys_flags.get('isolated')==1 and sys_flags.get('dont_write_bytecode')==1,'CAPTURE_ISOLATED_FLAGS')
 need(type(captured_utc) is str and bool(captured_utc),'CAPTURE_TIME')
 files=files or FileFingerprints();interpreter=files.capture(interpreter_path)
 records=[]
 for name in sorted(names):
  module=resolved_modules[name]
  canonical=getattr(module,'__name__',None)
  need(type(canonical) is str and resolved_modules.get(canonical) is module,'CAPTURE_MODULE_ALIAS_UNBOUND')
  fingerprint=module_fingerprint(module,files=files,interpreter=interpreter,sys_version=sys_version,stdlib_names=stdlib_names,package_roots=package_roots)
  records.append(dict(fingerprint,name=name,canonical_name=canonical))
 record=dict(schema='CX1_RUNTIME_CAPTURE_V001',coverage_complete=True,
  inventory=inventory,producer=producer_pin,captured_utc=captured_utc,
  interpreter=interpreter,sys_version=sys_version,sys_flags=dict(sys_flags),
  macos_build=macos_build,hardware_model=hardware_model,
  effective_environment=effective_environment(inherited_environment),modules=records)
 validate_record(record)
 return record
