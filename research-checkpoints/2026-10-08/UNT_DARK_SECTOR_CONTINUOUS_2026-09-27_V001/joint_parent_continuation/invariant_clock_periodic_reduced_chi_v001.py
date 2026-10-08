"""Equivalent chi-primary reconstruction; no driver or state projection.

Parent handles exact momentum constraint and dynamical mean pi_a unchanged.
Only the local H solve is parametrized by independent delta_chi. Recovered
pi_b never feeds back through the old inverse to obtain accepted fields.
Inherited fields is used once for a STARTING GUESS only, not final dynamics.
The exact Hamiltonian derivative is 4 V c b_dot Kchi. Original receipts and
all tolerances remain unchanged. Positive transverse expansion is required.
"""
import numpy as np
from invariant_clock_periodic_reduced_v003 import Reduced as Parent
from invariant_clock_periodic_reduced_v001 import ConstraintReconstructionError
from invariant_clock_periodic_chi_v001 import PeriodicChi, LocalInverseError

class Reduced(Parent):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.core=PeriodicChi(self.m,self.n,self.k)
        self.core.dx=self.dx

    def _local_h(self,x,state,piT,target,ds_guess=None):
        z=state.copy()
        guess=self.core.fields(x,z,ds_guess=ds_guess)
        dchi=guess['delta_chi'].copy()
        ds_guess=guess['ds'].copy()
        history=[]
        for iteration in range(self.local_iterations):
            g=self.core.fields_chi(x,z,dchi,ds_guess=ds_guess)
            z=g['state'];ds_guess=g['ds']
            if np.any(g['bdot']<=0) or np.any(g['Kchi']<=0):
                raise ConstraintReconstructionError('chi chart regular branch lost',
                    dict(iteration=iteration,min_bdot=float(np.min(g['bdot'])),min_Kchi=float(np.min(g['Kchi']))))
            cc=self.core.constraints(x,z,piT,fields=g)
            hs,_,_=self._scales(g,cc,piT,target)
            norm=float(np.max(abs(cc['Hamiltonian'])))
            last=dict(iteration=iteration,H_absolute=norm,H_scale=hs,H_relative=norm/hs)
            history.append(last)
            if norm/hs<=self.local_tolerance:return z,g,cc,last
            step=cc['Hamiltonian']/(4*g['V']*g['c']*g['bdot']*g['Kchi'])
            accepted=False
            for half in range(self.backtracks):
                trial=dchi-step*2.**(-half)
                try:
                    gt=self.core.fields_chi(x,z,trial,ds_guess=g['ds'])
                    ct=self.core.constraints(x,gt['state'],piT,fields=gt)
                except (LocalInverseError,ValueError):continue
                if np.all(gt['bdot']>0) and np.all(gt['Kchi']>0) and np.max(abs(ct['Hamiltonian']))<norm:
                    dchi,ds_guess,accepted=trial,gt['ds'],True
                    break
            if not accepted:raise ConstraintReconstructionError('chi local Hamiltonian backtracking failed',dict(history=history))
        raise ConstraintReconstructionError('chi local Hamiltonian iteration cap',dict(history=history))
