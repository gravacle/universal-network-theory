"""Inert paired line/HI facade for the reviewed sequential0424 callback chain.
Requires an actual fresh line evaluation for each uncached HI metric callback.
Only the adopted zero boundary perturbations are admitted. No solver mutation.
UVTAIL c2v001 (Claude2 tail_scheme_impl_c2/route_a; successor of 2caca496; TAIL_SCHEME_DESIGN_V002 sec 2.1 A4, 2.3):
optional uv_tail = the bound TailBoundary. uv_tail=None executes the reviewed statements. Supplied: the boundary
jets must equal, bitwise (dtype, shape, bytes), uv_tail.jet_for_line(line, z) -- the slot carries exactly the
UV-tail jet and nothing else -- and the lapse pair is uv_tail.lapse_pair (R0 expm1 form: bd(z=0) == 0.0, so the
midplane log ratio is exactly 0.0 and HI v003 L67-68 holds).
"""
from pathlib import Path
import types
import math
import numpy as np


def make_modules(*,line_module,hi_module,reality_atol,reality_rtol,uv_tail=None):
    own=str(Path(__file__).resolve());last={};serial=0
    def prepare_line(**kw):return line_module.prepare_line(**kw)
    def evaluate_line(**kw):
        nonlocal serial
        for name in (('boundary_fields','boundary_gradient','boundary_hessian') if uv_tail is None else ()):
            a=np.asarray(kw[name])
            if not np.isfinite(a).all() or np.any(a!=0):
                raise ValueError('Stable lapse facade admits adopted zero boundary perturbations only')
        if uv_tail is not None:
            expected=uv_tail.jet_for_line(kw['line'],kw['z_m'])
            for name in ('boundary_fields','boundary_gradient','boundary_hessian'):
                a=np.asarray(kw[name]);e=expected[name]
                if a.dtype!=e.dtype or a.shape!=e.shape or not np.isfinite(a).all() or a.tobytes()!=e.tobytes():
                    raise ValueError('UV-tail stable lapse facade admits exactly the bound UV-tail boundary jet only')
        value=line_module.evaluate_line(**kw)
        serial+=1;last.clear();last.update(serial=serial,line=kw['line'],z=kw['z_m'])
        return value
    def solve_hi_column(*,metric_at_z,**kw):
        radius=float(kw['radius_m']);bound_line=None
        def metric(z):
            nonlocal bound_line
            before=serial;packet=dict(metric_at_z(z))
            if serial!=before+1 or last['z']!=z:
                raise ValueError('HI callback must perform one fresh bound vertical-line evaluation')
            line=last['line']
            if bound_line is None:bound_line=line
            if line is not bound_line:raise ValueError('Changed source/column line inside HI solve')
            actual_radius=math.hypot(line['x_m'],line['y_m'])
            if not math.isclose(actual_radius,radius,rel_tol=8*np.finfo(float).eps,abs_tol=0.):
                raise ValueError('HI radius and actual Fourier column differ')
            ns=line['fields'].shape[2]
            if ns!=1:raise ValueError('HI preparation requires one actual total source family')
            b0,bd=(np.zeros(ns),np.zeros(ns)) if uv_tail is None else uv_tail.lapse_pair(line['x_m'],line['y_m'],z,ns)
            stable=line_module.lapse_difference(line=line,z_m=z,boundary_lapse_at_zero=b0,
                boundary_lapse_difference=bd,reality_atol=reality_atol,reality_rtol=reality_rtol)
            packet['log_lapse_ratio_from_midplane']=float(stable['log_lapse_ratio_from_midplane'][0])
            return packet
        return hi_module.solve_hi_column(metric_at_z=metric,**kw)
    line=types.ModuleType('owned_stable_lapse_line_facade');line.__file__=own
    line.prepare_line=prepare_line;line.evaluate_line=evaluate_line
    hi=types.ModuleType('owned_stable_lapse_hi_facade');hi.__file__=own
    hi.solve_hi_column=solve_hi_column
    return line,hi
