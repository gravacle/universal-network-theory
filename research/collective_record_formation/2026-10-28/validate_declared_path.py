"""Independent small-system check of the declared path scaling calculation."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).parent
data = json.loads((ROOT / 'declared_path_dynamics_results.json').read_text())
I = np.eye(2)
X = np.array([[0., 1.], [1., 0.]])
Z = np.diag([1., -1.])

def at(op, site, M):
    out = np.array([[1.]])
    for j in reversed(range(M)):
        out = np.kron(out, op if j == site else I)
    return out

checks = []
for model in data['models']:
    M, Ud = model['M_links'], model['Ud']
    if M not in (1, 3, 5) or Ud not in (1., 4.):
        continue
    dim = 1 << M
    xs = [at(X, i, M) for i in range(M)]
    zs = [at(Z, i, M) for i in range(M)]
    # Build the expanded Pauli form, independently of the bit-counting sparse H.
    H = -sum(xs) + Ud/2 * (zs[0] + zs[-1])
    H += Ud*(M+1)/2 * np.eye(dim)
    for i in range(M-1):
        H += Ud/2 * (zs[i] @ zs[i+1])
    ns = [(np.eye(dim)-z)/2 for z in zs]
    blank = np.zeros(dim, dtype=complex)
    blank[0] = 1
    for row in model['results']:
        if row['time'] not in (0.5, 1., 4.):
            continue
        state = expm(-1j * row['time'] * H) @ blank
        ev = lambda A: float(np.vdot(state, A @ state).real)
        means = np.array([ev(n) for n in ns])
        C = np.array([[ev(a @ b) for b in ns] for a in ns]) - np.outer(means, means)
        errors = [float(np.max(np.abs(means-row['single_link_occupations'])))]
        if M > 1:
            errors += [abs(float(np.diag(C,1).mean())-row['nearest_neighbor_connected_covariance_mean']),
                       abs(float(C[0,-1])-row['end_to_end_connected_covariance'])]
        checks.append({'M': M, 'Ud': Ud, 'time': row['time'], 'maximum_error': max(errors)})

maximum = max(c['maximum_error'] for c in checks)
result = {'method': 'Dense matrix exponential of independently expanded Pauli Hamiltonian',
          'checks': checks, 'maximum_error': maximum, 'tolerance': 1e-10,
          'passed': maximum < 1e-10}
(ROOT / 'scaling_validation.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'checks': len(checks), 'maximum_error': maximum, 'passed': result['passed']}))
if not result['passed']:
    raise SystemExit('Independent validation failed')
