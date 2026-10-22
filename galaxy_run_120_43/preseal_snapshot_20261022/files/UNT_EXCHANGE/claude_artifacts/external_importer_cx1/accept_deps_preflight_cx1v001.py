"""Read every selected acceptance dependency before any execution; not a loader.
Caller authenticates the dependency record and expected LO pin. Transitive imports
and scientific applicability remain outside this syntactic/byte preflight.
"""
import ast,copy
from snapshot_cx1v001 import Refusal
NAMES=('enumerator','evidence','lo_core','guard','writer','row_producer','lo_adapter','srb_adapter')
def preflight(snapshot,pins,expected_lo):
 if type(pins) is not dict or set(pins)!=set(NAMES):raise Refusal('ACCEPT_DEPS_SET')
 if pins.get('lo_adapter')!=expected_lo:raise Refusal('ACCEPT_LO_SELECTION')
 checked={}
 # Validate the entire shape before opening any dependency.
 for name in NAMES:
  p=pins[name];adapter=name.endswith('_adapter')
  fields={'path','sha256','entry'} if adapter else {'path','sha256'}
  if type(p) is not dict or set(p)!=fields:raise Refusal('ACCEPT_DEP_PIN:'+name)
  if adapter and (type(p['entry']) is not str or not p['entry'].isidentifier()):raise Refusal('ACCEPT_DEP_ENTRY:'+name)
 for name in NAMES:
  p=pins[name];raw=snapshot.pin({k:p[k] for k in ('path','sha256')})
  try:ast.parse(raw,filename=p['path'])
  except (SyntaxError,ValueError,UnicodeError) as exc:raise Refusal('ACCEPT_DEP_SYNTAX:'+name) from exc
  checked[name]=dict(pin=copy.deepcopy(p),raw=raw)
 return checked
