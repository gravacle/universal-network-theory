"""Phase derivation from resolved paths, prereg C-1.1.
External adapter must resolve all three actual paths before invoking this pure rule.
No manifest phase field is used. PHASE_2 is the complement of PHASE_1.
"""
from pathlib import PurePosixPath

class PhaseDefect(ValueError):pass

def _resolved(value):
    if type(value) is not str or not value or not value.startswith('/'):
        raise PhaseDefect('PHASE_MISMATCH')
    path=PurePosixPath(value)
    if '..' in path.parts:raise PhaseDefect('PHASE_MISMATCH')
    return path

def derive_phase(calibration_path,phase1_root,phase2_root,named_phase):
    call,p1,p2=map(_resolved,(calibration_path,phase1_root,phase2_root))
    if p1==p2 or p1 in p2.parents or p2 in p1.parents:
        raise PhaseDefect('PHASE_MISMATCH')
    derived='PHASE_1' if call==p1 or p1 in call.parents else 'PHASE_2'
    if named_phase!=derived:raise PhaseDefect('PHASE_MISMATCH')
    return derived
