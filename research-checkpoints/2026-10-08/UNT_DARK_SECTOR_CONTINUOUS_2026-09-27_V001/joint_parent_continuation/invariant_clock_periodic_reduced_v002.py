"""Reflection-Galerkin arithmetic for the predeclared reduced chart.

The action and initial data are reflection invariant: u/pi_u odd, all other
chart fields even. V001 checked that input sector but let floating-point
RHS roundoff leak outside its tangent space. Evaluate the RHS in the stated
symmetry basis by paired even/odd averaging; no physical Fourier harmonic
in that sector is removed, and no accepted state, charge, constraint or
mean shear is reset. Record the entire discarded roundoff remainder.
Input parity checks and all numerical/physical acceptance gates unchanged.
"""
import numpy as np
from invariant_clock_periodic_reduced_v001 import Reduced as Parent

class Reduced(Parent):
    def rhs(self,x,chart,return_fields=True):
        out,rec=super().rhs(x,chart,return_fields=True)
        signs=np.array([1,1,-1,1,1,1,-1,1])[:,None]
        symmetric=(out+signs*out[:,self.mirror])/2
        rec['reflection_remainder']=out-symmetric
        rec['reflection_remainder_component_relative']=np.max(abs(out-symmetric),axis=1)/np.maximum(np.max(abs(out),axis=1),1e-30)
        return (symmetric,rec) if return_fields else symmetric
