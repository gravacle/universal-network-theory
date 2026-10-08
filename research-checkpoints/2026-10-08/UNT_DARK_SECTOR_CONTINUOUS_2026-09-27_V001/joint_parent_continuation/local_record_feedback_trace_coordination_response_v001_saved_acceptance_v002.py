#!/usr/bin/env python3
"""Authored acceptance check by a distinct scalar-moment route; root alone runs."""
import json, math, hashlib, sys, traceback, time
from decimal import Decimal, getcontext
from pathlib import Path

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT / 'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME = 'LOCAL_RECORD_FEEDBACK_TRACE_COORDINATION_RESPONSE_V001'
STEM = 'local_record_feedback_trace_coordination_response_v001'
CP = J / (STEM + '_checkpoints')
OUT, REPORT, ERROR = [J / (NAME + s) for s in ('_AUDIT_V002.json', '_AUDIT_V002.md', '_AUDIT_ERROR_V002.json')]
PINS = {NAME + '_RESULT.json': '530dd7bdc929246c46b2335a233a3c49b9350ffd365318060c4eb1ab183d2e0f',
        NAME + '_RESULT.md': '132e2ca21074936ecada1d42a6a487891ae52e5b7384a00bf6da646459263b1b',
        NAME + '_RECEIPT.json': 'a00ceb07fb5e44dca1cbffc053f92421cf6a08a9f6161b42668f32fe23736849',
        NAME + '.md': '15803e409afbdcbf5081be1d942479e28ad21f2bb3e28be05077849300a0fae2',
        STEM + '.py': 'bb180466db356576b6e75fda2eae094577ded94f05247911e6ea6a3a1d2d9439',
        STEM + '_saved_acceptance.py': '60ee30724d3cb380bc09312e319a671dbd6ebdbe5a357e71ae6c5d29a6abf863',
        NAME + '_AUDIT_ERROR.json': '6498845b12c719d161e706da2b646e6a16701adaccce3de6bc6c0a372a2b63a2',
        'local_record_feedback_trace_coordination_precision_diagnostic_v001.py': '91ac670eb69bd7e334f1944722e2a0787e55762b17d534efdce53f28ede9941c',
        NAME + '_PRECISION_DIAGNOSTIC.json': 'e7f0c63f3000828cb26d9700d747d38002621bccdecc0cb1003634086b40172b'}
FIELDS = ('A', 'B', 'C', 'determinant', 'S_T_fixed_Q', 'S_Q_fixed_T', 'T_response_relaxed',
          'response_reduction', 'coupling_fraction', 'df_du_fixed_Q', 'Gamma_TT_candidate',
          'Gamma_TQ_candidate', 'Gamma_QQ_candidate', 'Gamma_TT_relaxed_candidate', 'candidate_stiffness_reduction')
COUNT, MAX_REL, INPUTS, ACTIVE = 0, 0., {}, None

def sha(path):
    d = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for x in iter(lambda: stream.read(1 << 20), b''): d.update(x)
    return d.hexdigest()

def read(path): return json.loads(Path(path).read_bytes())
def canonical(value): return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def need(ok, label):
    global COUNT
    COUNT += 1
    if not ok: raise AssertionError(label)

def flat(value):
    if isinstance(value, (tuple, list)): return [x for v in value for x in flat(v)]
    if isinstance(value, Decimal): return [float(value)]
    return [value]

def close(label, value, target):
    global MAX_REL
    a, b = flat(value), flat(target); need(len(a) == len(b), label + ' shape')
    need(all(isinstance(x, (int, float)) and math.isfinite(x) for x in a + b), label + ' finite')
    residual = math.sqrt(math.fsum((x - y) ** 2 for x, y in zip(a, b)))
    scale = max(1., math.sqrt(math.fsum(y * y for y in b))); MAX_REL = max(MAX_REL, residual / scale)
    need(residual <= 3e-11 * scale, label + ' norm comparison')

def register(path, wanted):
    path = Path(path).resolve(); need(sha(path) == wanted, 'input seal ' + str(path))
    key = str(path.relative_to(ROOT)); need(key not in INPUTS or INPUTS[key] == wanted, 'consistent seal')
    INPUTS[key] = wanted

def atom(path, value):
    with Path(path).open('xb') as stream:
        stream.write(canonical(value) + b'\n'); stream.flush()
        import os
        os.fsync(stream.fileno())

def mean(values): return math.fsum(values) / len(values)
def moment(blocks):
    return ([mean([b[0][i] for b in blocks]) for i in range(2)],
            [[mean([b[1][i][j] for b in blocks]) for j in range(2)] for i in range(2)])

def matrix(moment_, beta):
    m, s = moment_
    return [[beta * (s[i][j] - m[i] * m[j]) for j in range(2)] for i in range(2)]

def precise_moment(blocks):
    n = len(blocks); d = Decimal.from_float
    return ([sum(d(b[0][i]) for b in blocks)/n for i in range(2)],
            [[sum(d(b[1][i][j]) for b in blocks)/n for j in range(2)] for i in range(2)])

def precise_values(moment_, beta):
    x = matrix(moment_, Decimal(beta)); a,b,c = x[0][0],(x[0][1]+x[1][0])/2,x[1][1]; det=a*c-b*b
    def ratio(u,v):return u/v if v != 0 else None
    red,rev=ratio(b*b,c),ratio(b*b,a)
    return dict(zip(FIELDS,[a,b,c,det,a-red if red is not None else None,c-rev if rev is not None else None,
        a,red,ratio(b*b,a*c),ratio(-b,c),ratio(c,det),ratio(-b,det),ratio(a,det),ratio(1,a),ratio(b*b,a*det)]))

def precise_jk(vectors):
    n,p=len(vectors),len(vectors[0]); center=[sum(v[j] for v in vectors)/n for j in range(p)]
    return [[Decimal(n-1)/n*sum((v[i]-center[i])*(v[j]-center[j]) for v in vectors)
             for j in range(p)] for i in range(p)]

def derive(x):
    a, b, c = x[0][0], (x[0][1] + x[1][0]) / 2, x[1][1]; det = a * c - b * b
    def ratio(u, v): return u / v if v != 0 and math.isfinite(u / v) else None
    reduction, rev = ratio(b*b, c), ratio(b*b, a)
    vals = [a, b, c, det, a - reduction if reduction is not None else None,
            c - rev if rev is not None else None, a, reduction, ratio(b*b, a*c), ratio(-b,c),
            ratio(c,det), ratio(-b,det), ratio(a,det), ratio(1,a), ratio(b*b,a*det)]
    spread = math.sqrt((a-c)*(a-c)+4*b*b); eigen = [(a+c-spread)/2, (a+c+spread)/2]
    cond = eigen[1]/eigen[0] if eigen[0] > 0 else None
    gamma = [[c/det,-b/det],[-b/det,a/det]] if det != 0 else None
    residual = math.sqrt(math.fsum((math.fsum(x[i][k]*gamma[k][j] for k in range(2))-(i==j))**2
                                  for i in range(2) for j in range(2))) if gamma else None
    flags = []
    if not all(math.isfinite(v) for v in flat(x)+eigen): flags.append('NONFINITE')
    if eigen[0] <= 0: flags.append('NONPOSITIVE')
    if cond is None or cond > 1e8: flags.append('CONDITIONING')
    if residual is None or not math.isfinite(residual) or residual > 3e-11*max(1.,cond or 1.): flags.append('INVERSE_RESIDUAL')
    return dict(zip(FIELDS,vals)), {'eigenvalues': eigen, 'condition_number':cond,
                                  'inverse_residual':residual, 'refusal_flags':flags}, gamma

def jk(vectors):
    n, p = len(vectors), len(vectors[0]); center = [mean([v[j] for v in vectors]) for j in range(p)]
    return [[(n-1)/n*math.fsum((v[i]-center[i])*(v[j]-center[j]) for v in vectors)
             for j in range(p)] for i in range(p)]

def orthogonal_check(label, moments_, beta, vals):
    if vals['C'] == 0: return
    m,s = moments_; k = vals['B']/vals['C']
    variance = Decimal(beta)*(s[0][0]-k*(s[0][1]+s[1][0])+k*k*s[1][1]-(m[0]-k*m[1])**2)
    covariance = Decimal(beta)*(s[0][1]-k*s[1][1]-(m[0]-k*m[1])*m[1])
    close(label + ' residual-variance Schur', variance, vals['S_T_fixed_Q'])
    close(label + ' orthogonality', covariance, 0.)

def audit_row(row, blocks, parent_row, condition):
    global ACTIVE
    label = row['id']; ACTIVE = label; n = len(blocks)
    need(n == row['block_count'] and row['block_measurements'] == 32, label + ' block census')
    need((row['condition'],row['beta'],row['epsilon'],row['parent_status'],row['parent_condition_status']) ==
         (parent_row['condition'],parent_row['beta'],parent_row['epsilon'],parent_row['status'],condition['status']), label + ' lineage')
    close(label+' raw means',[b[0] for b in blocks],row['raw_paired_block_means']['mean'])
    close(label+' raw seconds',[b[1] for b in blocks],row['raw_paired_block_means']['second'])
    m = moment(blocks); x = matrix(m,row['beta']); vals,diag,gamma = derive(x)
    close(label+' central chi',x,row['chi']); close(label+' mean density',[v/math.sqrt(54) for v in m[0]],row['mean_density_TQ'])
    close(label+' complete D density',1+(m[0][0]-m[0][1])/(2*math.sqrt(54)),parent_row['estimates']['scalars'][1])
    close(label+' parent chi',x,parent_row['joint_estimates']['chi_TQ_density_independent'])
    moments = [moment(blocks[:i]+blocks[i+1:]) for i in range(n)]
    replicas = [matrix(v,row['beta']) for v in moments]; descriptions = [derive(v) for v in replicas]
    precise_moments = [precise_moment(blocks)]+[precise_moment(blocks[:i]+blocks[i+1:]) for i in range(n)]
    precise = [precise_values(v,row['beta']) for v in precise_moments]
    vals=precise[0]; descriptions=[(p,d[1],d[2]) for p,d in zip(precise[1:],descriptions)]
    close(label+' all chi replicas',replicas,row['chi_replicas'])
    for ri,(v,d,g) in enumerate([(vals,diag,gamma)]+descriptions):
        savedvals = row['central'] if ri == 0 else row['derived_replicas'][ri-1]
        savedd = row['central_diagnostics'] if ri == 0 else row['replica_diagnostics'][ri-1]
        need(list(savedvals) == sorted(FIELDS), label + ' scalar field set')
        for key in FIELDS:
            if v[key] is None: need(savedvals[key] is None,label+key+' undefined')
            else: close(label+str(ri)+key,v[key],savedvals[key])
        for key in ('eigenvalues','condition_number','inverse_residual'):
            if d[key] is None: need(savedd[key] is None,label+key+' undefined')
            else: close(label+str(ri)+key,d[key],savedd[key])
        need(d['refusal_flags'] == savedd['refusal_flags'],label+' algebraic refusal')
        orthogonal_check(label+str(ri),precise_moments[ri],row['beta'],v)
    cv = jk([flat(x) for x in replicas]); close(label+' chi covariance',cv,row['chi_component_jackknife_covariance'])
    se = [[math.sqrt(cv[2*i+j][2*i+j]) for j in range(2)] for i in range(2)]
    close(label+' chi errors',se,row['chi_SE'])
    available = [k for k in FIELDS if vals[k] is not None and all(d[0][k] is not None for d in descriptions)]
    need(available == row['paired_derived_covariance_labels'],label+' paired field order')
    dcov = precise_jk([[v[0][k] for k in available] for v in descriptions]); close(label+' nonlinear covariance',dcov,row['paired_derived_jackknife_covariance'])
    for i,k in enumerate(available): close(label+k+' error',math.sqrt(dcov[i][i]),row['derived_SE'][k])
    flags = diag['refusal_flags'].copy(); err = 3*math.sqrt(math.fsum(v*v for v in flat(se)))
    if diag['eigenvalues'][0] <= err: flags.append('BLOCK_ERROR_DOMINATED')
    if any(d[1]['refusal_flags'] for d in descriptions): flags.append('REPLICA_REFUSAL')
    if condition['status'] != 'FINITE_GRID_PILOT_DIAGNOSTICS_PASSED' or 'MIXING_UNQUALIFIED' in parent_row['status']: flags.append('MIXING_UNQUALIFIED')
    need(flags == row['inverse_refusal_flags'],label+' inherited inverse/mixing refusal')
    close(label+' error criterion',err,row['three_SE_Frobenius_scale'])
    if gamma is not None: close(label+' candidate Gamma',gamma,row['Gamma_candidate'])
    need((row['qualified_Gamma'] is not None)==(gamma is not None and not flags),label+' inverse qualification')
    if not flags: close(label+' qualified Gamma',gamma,row['qualified_Gamma'])
    status = 'SCALAR_STATIC_INVERSE_DIAGNOSTICS_PASSED_ONLY' if gamma is not None and not flags else 'INVERSE_UNQUALIFIED_'+'_'.join(flags)
    need(status==row['inverse_status'] and row['mechanical_or_metric_stiffness_qualification'] is False and
         row['source_contacts_uu_uf_ff']==[0,0,0], label+' statuses/contacts')
    return {'id':label,'block_count':n,'parent_condition_status':condition['status'],
            'inverse_status':status,'fixed_Q_response':float(vals['S_T_fixed_Q']) if vals['S_T_fixed_Q'] is not None else None,
            'relaxed_response':float(vals['A'])}

def main():
    start=time.perf_counter(); need(sys.argv[1:]==['--execute'],'exact root --execute required');getcontext().prec=50
    need(not any(p.exists() for p in (OUT,REPORT,ERROR)),'exclusive audit outputs')
    for filename,digest in PINS.items(): register(J/filename,digest)
    old_error=read(J/(NAME+'_AUDIT_ERROR.json'));precision=read(J/(NAME+'_PRECISION_DIAGNOSTIC.json'))
    need(old_error['active']=='c2_B' and old_error['status']=='AUDIT_ERROR_PRESERVED' and
         precision['status']=='PRECISION_DIAGNOSTIC_NO_QUALIFICATION_CHANGE' and precision['precision_digits']==50 and
         tuple(precision['fields'])==FIELDS and precision['preserved_error_sha256']==PINS[NAME+'_AUDIT_ERROR.json'], 'preserved failed attempt and precision evidence')
    result,receipt=read(J/(NAME+'_RESULT.json')),read(J/(NAME+'_RECEIPT.json'))
    need(hashlib.sha256(canonical(result)).hexdigest()==receipt['result_canonical_sha256'],'canonical result')
    need(receipt['passed']==result['passed']==len(result['checks'])==6472 and result['failed']==receipt['failed']==0 and
         all(c['passed'] for c in result['checks']),'all parent arithmetic checks')
    need(result['input_sha256']==receipt['input_sha256'] and result['status']==receipt['status'],'parent inputs/status')
    lines=(CP/'journal.jsonl').read_bytes().splitlines(keepends=True);events=[json.loads(x) for x in lines]
    need(len(lines)==25 and len(receipt['checkpoint_sha256'])==21,'journal/checkpoint census')
    need(hashlib.sha256(b''.join(lines[:-1])).hexdigest()==receipt['journal_prefix_sha256'] and
         events[-1]['event']=='receipt_complete' and events[-1]['sha256']==PINS[NAME+'_RECEIPT.json'],'journal prefix/receipt')
    for kind,suffix in (('result_complete','_RESULT.json'),('report_complete','_RESULT.md')):
        need(sum(e['event']==kind and e.get('filename')==NAME+suffix and e.get('sha256')==PINS[NAME+suffix] for e in events)==1,'result/report journal commit')
    for filename,digest in receipt['checkpoint_sha256'].items():
        register(CP/filename,digest); need(sum(e.get('filename')==filename and e.get('sha256')==digest for e in events)==1,'unique CP commit')
    register(CP/'journal.jsonl',sha(CP/'journal.jsonl'))
    manifest=read(CP/'manifest.json');need(manifest['input_sha256']==receipt['input_sha256'] and
        sum(e['event']=='started' and e['input_sha256']==receipt['input_sha256'] and
            e['manifest_sha256']==receipt['checkpoint_sha256']['manifest.json'] for e in events if e['event']=='started')==1,'manifest/start')
    for filename,digest in receipt['input_sha256'].items(): register(ROOT/filename,digest)
    parent=read(J/'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.json')
    need(len(parent['chains'])==16 and len(parent['conditions'])==4 and len(result['rows'])==20,'20 dataset census')
    expected=[r['id'] for r in parent['chains']]+['condition%d'%r['condition'] for r in parent['conditions']]
    need([r['id'] for r in result['rows']]==expected and len(set(expected))==20,'ordered unique rows')
    chains={r['id']:r for r in parent['chains']};conditions={r['condition']:r for r in parent['conditions']};summaries=[]
    for row in result['rows']:
        need(read(CP/(row['id']+'.json'))==row,'row checkpoint/result identity')
        old=chains[row['id']] if row['id'] in chains else conditions[row['condition']]
        labels=[row['id']] if row['id'] in chains else old['chain_ids']; blocks=[]
        for label in labels:
            raw=chains[label]['joint_block_raw_moments']; means,seconds=raw['mean_TQ_density_scaled'],raw['second_TQ_density']
            need(len(means)==len(seconds)==32,'original scalar block count');blocks.extend(zip(means,seconds))
        summaries.append(audit_row(row,blocks,old,conditions[row['condition']]))
    need(sum(r['block_count'] for r in summaries)==1024,'1024 paired replicas')
    for filename,digest in INPUTS.items():need(sha(ROOT/filename)==digest,'unchanged input '+filename)
    audit={'status':'SAVED_ACCEPTANCE_CHECK_V002_PASSED','assertions':COUNT,'failed':0,'rows':summaries,
           'replicas':1024,'maximum_relative_norm_residual':MAX_REL,'input_sha256':INPUTS,
           'audit_source_sha256':sha(__file__),'elapsed_seconds':time.perf_counter()-start,
           'method':'original scalar moments; unchanged float primitive controls; Decimal50 exact-binary nonlinear reconstruction and covariance; residual oracle; no producer/NumPy/H/RNG replay',
           'precision_digits':50,'unchanged_comparison_tolerance':3e-11,'preserved_V001_error_sha256':PINS[NAME+'_AUDIT_ERROR.json'],
           'independent_authorship_claim':False,'physical_or_metric_stiffness_qualification':False}
    atom(OUT,audit)
    text='# Trace–coordination saved acceptance check V002\n\nPASS: %d assertions; all20 datasets/1024 paired replicas.\n\nV001 failed at the float nonlinear covariance reconstruction and remains preserved. V002 uses Decimal50 on the exact binary parent-input values for every nonlinear field/covariance and residual oracle. The original3e-11 criterion, primitive controls, paired errors and all inverse/mixing refusals are unchanged. This is an authored acceptance check, peer-reviewed before root execution.\n\nMaximum normalized residual: %.12g. No H, sampler, RNG or producer import/replay.\n'%(COUNT,MAX_REL)
    with REPORT.open('x') as stream:
        stream.write(text);stream.flush()
        import os
        os.fsync(stream.fileno())
    print(json.dumps({'status':'PASS','assertions':COUNT,'audit_sha256':sha(OUT),'report_sha256':sha(REPORT)}),flush=True)

if __name__=='__main__':
    try:main()
    except Exception as e:
        if not ERROR.exists():atom(ERROR,{'status':'AUDIT_ERROR_PRESERVED','type':type(e).__name__,'error':str(e),
            'traceback':traceback.format_exc(),'active':ACTIVE,'completed_assertions':COUNT,'input_sha256':INPUTS,
            'audit_source_sha256':sha(__file__)})
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
