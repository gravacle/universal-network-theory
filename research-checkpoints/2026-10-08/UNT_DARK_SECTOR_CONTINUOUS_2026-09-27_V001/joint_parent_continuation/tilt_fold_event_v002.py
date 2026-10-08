"""Serialization-only repair of V001; preserve its partial invalid receipt."""
from pathlib import Path
import hashlib
import json
import numpy as np
import tilt_fold_event_v001 as core

dump,dumps=json.dump,json.dumps
def scalar(value):
    if isinstance(value,np.generic):return value.item()
    raise TypeError(f'Unsupported JSON type: {type(value).__name__}')
def save(value,fp,**kwargs):
    value['serialization_wrapper_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return dump(value,fp,default=scalar,**kwargs)

if __name__=='__main__':
    core.OUT=core.BASE/'TILT_FOLD_EVENT_V002_RESULT.json'
    core.json.dump=save
    core.json.dumps=lambda value,**kw:dumps(value,default=scalar,**kw)
    core.main()
