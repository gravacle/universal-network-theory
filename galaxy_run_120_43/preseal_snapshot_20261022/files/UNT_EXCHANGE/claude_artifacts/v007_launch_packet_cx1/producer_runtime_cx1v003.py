"""Load only byte-pinned r5 numerical libraries; no output or run access."""
import sys as _guard_sys
from pathlib import Path as _GuardPath
_guard_sys.path.insert(0, str(_GuardPath(__file__).parent))
import producer_guard_cx1v007 as _root_guard
_root_guard.admission(__file__)
import hashlib, importlib.util, json, sys
from pathlib import Path
P = Path(__file__).parent / 'R5_RUNTIME_PINS_V001.json'

@_root_guard.guarded
def bind(T):
    pins = json.loads(P.read_bytes())['pins']
    for key in ('module', 'roster', 'provider'):
        ref = pins[key]
        raw = Path(ref['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != ref['sha256']:
            raise ValueError('R5_RUNTIME_PIN_MISMATCH:' + key)
        name = 'cx1_r5_' + key
        if name not in sys.modules:
            sp = importlib.util.spec_from_file_location(name, ref['path'])
            m = importlib.util.module_from_spec(sp)
            sys.modules[name] = m
            sp.loader.exec_module(m)
        setattr(T, {'module': 'UVT', 'roster': 'RS', 'provider': 'PV'}[key], sys.modules[name])
    return pins
