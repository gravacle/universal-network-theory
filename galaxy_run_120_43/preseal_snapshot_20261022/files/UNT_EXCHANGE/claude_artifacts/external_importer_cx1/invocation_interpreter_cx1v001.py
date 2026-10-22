"""Bind invocation spelling to captured interpreter bytes without executing it.
Caller must authenticate the D005 identity; this checks present filesystem association,
not historical launch execution or future resistance to filesystem changes.
"""
from pathlib import Path
from register_two_stage_cx1v003 import sha
from request_guard_cx1v002 import require

def check(snapshot,*,python,identity):
 require(type(python) is str and Path(python).is_absolute(),'PYTHON_INVOCATION_PATH')
 require(type(identity) is dict and set(identity)=={'realpath','sha256'} and type(identity['realpath']) is str and Path(identity['realpath']).is_absolute() and sha(identity['sha256']),'PYTHON_CAPTURE_IDENTITY')
 try:before=str(Path(python).resolve(strict=True))
 except (OSError,RuntimeError):require(False,'PYTHON_RESOLUTION')
 require(before==identity['realpath'],'PYTHON_REALPATH_ASSOCIATION')
 snapshot.pin(dict(path=before,sha256=identity['sha256']))
 try:after=str(Path(python).resolve(strict=True))
 except (OSError,RuntimeError):require(False,'PYTHON_RESOLUTION_AFTER')
 require(after==before,'PYTHON_RESOLUTION_CHANGED')
 return dict(prerequisites_only=True,python=python,interpreter=dict(identity))
