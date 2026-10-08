"""Small prospective arithmetic checks, not a cosmological fit or simulation."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "GEOMETRIC_GRADIENT_EXPANSION_V001_RESULT.json"
if OUT.exists():
    raise SystemExit("Preserve existing result; no overwrite or repeated run.")

ATOL = RTOL = 2e-12
LAPSE_TOL = 2e-8
checks = []

def close(name, got, expected, tol=RTOL):
    ok = abs(got-expected) <= tol * max(1., abs(got), abs(expected))
    checks.append(dict(name=name, got=float(got), expected=float(expected), pass_check=bool(ok)))

AU = 149597870700.0
PC = 648000.0 * AU / math.pi
C_LIGHT = 299792458.0
H = 70.0 * 1000.0 / (1e6 * PC)
ELL = 100.0 * PC
chi = H * ELL / C_LIGHT
close("unit conversion independent ratio", chi, 70.0/10000.0/(C_LIGHT/1000.0))

q = np.array([0.3, -0.7, 1.1])
dy = np.array([[0.2, -0.6, 0.4], [0.8, 0.1, -0.5], [-0.2, 0.7, 0.3]])
for i, curvature in enumerate((np.zeros((3, 3)), np.eye(3)*0.4,
                               np.array([[0.4,0.1,-0.2],[0.1,0.8,0.3],[-0.2,0.3,-0.1]]))):
    deriv = np.column_stack((curvature @ q, dy))
    metric = np.diag([-1., 1., 1., 1.])
    raw = float(np.trace(deriv @ metric @ deriv.T))
    projected = float(np.sum(dy*dy))
    close(f"Lorentzian identity {i}", raw, projected-float(np.linalg.norm(curvature @ q)**2))

# N variation holds a, adot, q and coordinate qdot fixed.
scale, adot, planck2, bb, kinetic, potential = 1.3, 0.27, 1.2, 0.4, 0.32, 0.71
dd = 3*planck2-bb/2
def lagrange(lapse):
    return lapse*scale**3 * (-dd*(adot/(lapse*scale))**2 + kinetic/lapse**2-potential)
step = 1e-5
derivative = (lagrange(1+step)-lagrange(1-step))/(2*step)/scale**3
close("lapse constraint", derivative, dd*(adot/scale)**2-kinetic-potential, LAPSE_TOL)

for i, (x, v2, rest) in enumerate(((1e-8, .7, .3), (.1, 1., 0.), (1., .4, .6), (3., .8, .2))):
    total = rest+(1+x*x)*v2
    fraction = x*x*v2/total
    bound = x*x/(1+x*x)
    checks.append(dict(name=f"positive energy bound {i}", fraction=fraction,
                       bound=bound, pass_check=fraction <= bound+ATOL))

result = dict(
    status="PASS" if all(c["pass_check"] for c in checks) else "FAIL",
    meaning="Local algebra/unit checks only; analytic activation criterion is chi > 1.",
    inputs=dict(H_km_s_Mpc=70., ell_pc=100., parsec_m=PC, c_m_s=C_LIGHT),
    chi=chi, chi_squared=chi*chi,
    homogeneous_gravity_fraction_upper=chi*chi/(1+chi*chi),
    activation_H_km_s_Mpc=C_LIGHT/ELL*(1e6*PC)/1000.,
    activation_length_Gpc=C_LIGHT/H/PC/1e9,
    operator_multiplier_activation_lower=1/(chi*chi),
    controls=checks, control_count=len(checks),
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    note_sha256_at_execution=hashlib.sha256((HERE/"GEOMETRIC_GRADIENT_EXPANSION_V001.md").read_bytes()).hexdigest(),
)
with OUT.open("x") as f:
    json.dump(result, f, indent=2, allow_nan=False)
    f.write("\n")
print(json.dumps(result, indent=2))
if result["status"] != "PASS":
    raise SystemExit(1)
