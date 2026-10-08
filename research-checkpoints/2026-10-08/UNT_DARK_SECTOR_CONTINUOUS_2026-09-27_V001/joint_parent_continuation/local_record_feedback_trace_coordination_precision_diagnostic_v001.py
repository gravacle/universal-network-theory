"""One failed-row arithmetic diagnosis; no qualification or tolerance change."""
from pathlib import Path
from decimal import Decimal, localcontext
import json, hashlib, math, os

J = Path(__file__).resolve().parent
NAME = 'LOCAL_RECORD_FEEDBACK_TRACE_COORDINATION_RESPONSE_V001'
OUT = J / (NAME + '_PRECISION_DIAGNOSTIC.json')
PINS = {
    NAME + '_RESULT.json': '530dd7bdc929246c46b2335a233a3c49b9350ffd365318060c4eb1ab183d2e0f',
    'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.json': '74042b5f40401085c151b10b4e32cda5257ca09c86a831f1ef98965abf4649a8',
}
D = Decimal.from_float

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def covariance(vectors):
    n = len(vectors)
    center = [sum(v[k] for v in vectors) / n for k in range(len(vectors[0]))]
    return [[Decimal(n-1) / n * sum((v[i]-center[i]) * (v[k]-center[k]) for v in vectors)
             for k in range(len(center))] for i in range(len(center))]

def precise_replicas(blocks, fields, beta):
    means, seconds = blocks
    n = len(means)
    result = []
    for omitted in range(n):
        m = [sum(D(means[k][a]) for k in range(n) if k != omitted) / (n-1) for a in range(2)]
        s = [[sum(D(seconds[k][a][b]) for k in range(n) if k != omitted) / (n-1)
              for b in range(2)] for a in range(2)]
        x = [[Decimal(beta) * (s[a][b]-m[a]*m[b]) for b in range(2)] for a in range(2)]
        a, b, c = x[0][0], (x[0][1]+x[1][0])/2, x[1][1]
        det = a*c-b*b
        assert a != 0 and c != 0 and det != 0
        values = dict(zip(fields, [a,b,c,det,a-b*b/c,c-b*b/a,a,b*b/c,b*b/(a*c),-b/c,
                                  c/det,-b/det,a/det,1/a,b*b/(a*det)]))
        result.append([values[f] for f in fields])
    return result

def comparison(a, b):
    error = math.sqrt(math.fsum(float(x-y)**2 for u,v in zip(a,b) for x,y in zip(u,v)))
    scale = max(1., math.sqrt(math.fsum(float(y)**2 for v in b for y in v)))
    return {'norm_error':error, 'scale':scale, 'relative_norm_error':error/scale,
            'unchanged_tolerance':3e-11, 'within_unchanged_tolerance':error <= 3e-11*scale}

assert not OUT.exists()
for f,h in PINS.items():
    assert sha(J/f) == h, f
error_path = J / (NAME + '_AUDIT_ERROR.json')
error_sha = sha(error_path)
failed = json.loads(error_path.read_text())
assert failed['active'] == 'c2_B'
producer = json.loads((J/(NAME+'_RESULT.json')).read_text())
parent = json.loads((J/'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.json').read_text())
row = next(r for r in producer['rows'] if r['id'] == 'c2_B')
old = next(r for r in parent['chains'] if r['id'] == 'c2_B')
fields = row['paired_derived_covariance_labels']
expected_fields = ['A', 'B', 'C', 'determinant', 'S_T_fixed_Q', 'S_Q_fixed_T',
                   'T_response_relaxed', 'response_reduction', 'coupling_fraction', 'df_du_fixed_Q',
                   'Gamma_TT_candidate', 'Gamma_TQ_candidate', 'Gamma_QQ_candidate',
                   'Gamma_TT_relaxed_candidate', 'candidate_stiffness_reduction']
assert fields == expected_fields and len(row['derived_replicas']) == 32
with localcontext() as context:
    context.prec = 50
    saved_cov = [[D(v) for v in u] for u in row['paired_derived_jackknife_covariance']]
    serialized = covariance([[D(v[f]) for f in fields] for v in row['derived_replicas']])
    own = row['raw_paired_block_means']
    own_cov = covariance(precise_replicas((own['mean'],own['second']),fields,row['beta']))
    independent = old['joint_block_raw_moments']
    parent_cov = covariance(precise_replicas((independent['mean_TQ_density_scaled'],
                                            independent['second_TQ_density']),fields,row['beta']))
    comparisons = {'serialized_replica_JK_vs_saved':comparison(serialized,saved_cov),
                   'same_input_precise_covariance_vs_saved':comparison(own_cov,saved_cov),
                   'parent_input_precise_covariance_vs_saved':comparison(parent_cov,saved_cov),
                   'two_precise_input_routes':comparison(parent_cov,own_cov)}
    matrices = {k:[[str(v) for v in u] for u in a] for k,a in
                [('serialized_JK',serialized),('own_input',own_cov),('parent_input',parent_cov)]}
for f,h in PINS.items():
    assert sha(J/f) == h, f
assert sha(error_path) == error_sha
result = {'status':'PRECISION_DIAGNOSTIC_NO_QUALIFICATION_CHANGE', 'row':'c2_B',
          'precision_digits':50, 'input_floats':'exact binary Decimal.from_float',
          'fields':fields, 'comparisons':comparisons, 'covariance_matrices':matrices,
          'input_sha256':PINS, 'preserved_error_sha256':error_sha,
          'source_sha256':sha(Path(__file__))}
with OUT.open('x') as stream:
    json.dump(result,stream,sort_keys=True,indent=2,allow_nan=False)
    stream.write('\n');stream.flush();os.fsync(stream.fileno())
print(json.dumps(comparisons,sort_keys=True))
