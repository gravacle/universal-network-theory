"""Shape-only repair of V001's interrupted diagnostic.

The reused Gauss integrator expects a matrix of state columns, not a1-D
vector. V001 raised a NumPy solve shape error before any trajectory or
result file. Preserve V001 unchanged. Adapt its vector call to one column;
all scientific inputs, equations, steps, criteria and readouts unchanged.
The result's dependency hashes add V001; self hash identifies this wrapper.
"""
from pathlib import Path
import hashlib
import plane_high_mode_transfer_v001 as prior

original=prior.newton.gauss_step
def vector_step(y,x,dx,mm):
    return original(y[:,None],x,dx,mm)[:,0]

if __name__=='__main__':
    prior.newton.gauss_step=vector_step
    prior.OUT=prior.BASE/'PLANE_HIGH_MODE_TRANSFER_V002_RESULT.json'
    # Existing writer uses its module __file__ and docstring for provenance.
    prior.__doc__=__doc__+'\n'+prior.__doc__
    prior.__file__=__file__
    prior.main()
