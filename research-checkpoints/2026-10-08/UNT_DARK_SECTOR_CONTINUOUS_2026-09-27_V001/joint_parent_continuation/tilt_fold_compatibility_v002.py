"""Serialization-only repair: V001 left a partial JSON on NumPy bool.
Preserve that partial file and V001. No equations, inputs or gates change.
This writer converts NumPy scalars and explicitly hashes the implementation.
"""
from pathlib import Path
import hashlib
import numpy as np
import tilt_fold_compatibility_v001 as prior

original=prior.json.dump
def dump(data,stream,**kw):
    data['dependencies_sha256']['tilt_fold_compatibility_v001.py']=hashlib.sha256((prior.BASE/'tilt_fold_compatibility_v001.py').read_bytes()).hexdigest()
    return original(data,stream,default=lambda obj:obj.item() if isinstance(obj,np.generic) else None,**kw)

if __name__=='__main__':
    prior.OUT=prior.BASE/'TILT_FOLD_COMPATIBILITY_V002_RESULT.json'
    prior.__doc__=__doc__+'\n'+prior.__doc__;prior.__file__=__file__
    prior.json.dump=dump
    # Final console dump has the same scalar conversion requirement.
    old_dumps=prior.json.dumps
    prior.json.dumps=lambda data,**kw:old_dumps(data,default=lambda obj:obj.item() if isinstance(obj,np.generic) else None,**kw)
    prior.main()
