"""Synthetic source-only readout check, no metric construction from a galaxy run."""
from pathlib import Path
import importlib.util
import numpy as np
import math

p=Path(__file__).with_name('review_certificates_cx3v003.py')
s=importlib.util.spec_from_file_location('cx3_review_common',p)
C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
C.sha(p)
lo=C.read(C.CERT/'gates/LO_NGC_CERT_V002.json')
pin=lo['code_reading']['metric_v002'];M=C.load(pin['path'],pin['sha256'])
dx=np.zeros(10);dx[0]=.01;grad=np.zeros((10,3))
def run(a):
    return M.evaluate_point(delta_fields=a,delta_gradient_physical=grad,Cbar=np.eye(3),mubar=np.zeros(3),R=2.,phi=.3,z=.1)
base=math.log(run(dx)['N']);rng=np.random.default_rng(5291);results=[]
for j in range(50):
    a=dx.copy();a[1:]=rng.uniform(-.03,.03,9)
    results.append(math.log(run(a)['N'])==base)
assert all(results)
a=dx.copy();a[0]+=.001
lapse_changes=math.log(run(a)['N'])!=base
a=dx.copy();a[1]=-2.
try:
    run(a);invalid_refused=False;message=None
except ValueError as e:
    invalid_refused=True;message=str(e)
assert lapse_changes and invalid_refused
assert C.sha(lo['i1t']['record']['path'])==lo['i1t']['record']['sha256']
i=C.read(lo['i1t']['record']['path'])
assert i['verdict']=='PASS' and all(b['verdict']=='PASS' and b['max_rel']<=b['rtol'] for b in i['builds'])
assert i['scope'].find('iteration-0')>=0
C.write('LO_NGC_READOUT_REVIEW_V001.json',dict(nonlapse_perturbations=50,all_valid_readouts_unchanged=all(results),lapse_canary_changes_readout=lapse_changes,
    invalid_metric_refused=invalid_refused,invalid_metric_message=message,
    finding='Zero non-lapse readout share is conditional on a valid metric. Non-lapse fields can still trip SPD or other validity guards; it is not an unconditional acceptance claim.',
    I1T_record_byte_pin_and_build_status_verified=True,downstream_consumer_I1T_enforcement='UNTESTED in this certificate-only review',
    record_source={'path':str(C.CERT/'gates/LO_NGC_CERT_V002.json'),'sha256':C.sha(C.CERT/'gates/LO_NGC_CERT_V002.json')},
    this_script={'path':__file__,'sha256':C.sha(__file__)}))
