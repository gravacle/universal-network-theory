"""Independent Codex2 checker of saved Codex3 P61 fixtures; ROOT EXECUTION ONLY.
No numpy/producer import, dynamics calculation, physical input or output mutation.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path

TOL = 1e-9
SOURCE_SHA = '49c8a7212f4e65a81c99a6522487fb0e63da0f583e9c6c7df7d6922792bbcd56'
RUNNER_SHA = '19132d2a5842612fa8df68194ae3e7de8a3cd00c501662a2c3a592606f00ece7'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    need(p.stat().st_size <= 2**20, 'saved JSON exceeds1MiB')
    def pairs(items):
        d = {}
        for k, v in items:
            need(k not in d, 'duplicate JSON key')
            d[k] = v
        return d
    return json.loads(p.read_text(), object_pairs_hook=pairs,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def decoded(x):
    if isinstance(x, dict):
        if set(x) == {'real', 'imag'}:
            need(all(type(v) in (int,float) and math.isfinite(v) for v in x.values()), 'finite complex cell')
            return complex(x['real'], x['imag'])
        return {k: decoded(v) for k, v in x.items()}
    if isinstance(x, list):
        return [decoded(v) for v in x]
    return x


def close(a, e, path='value'):
    if isinstance(e, dict):
        need(isinstance(a,dict) and set(a)==set(e), path+' keys')
        for k in e:
            close(a[k], e[k], path+'.'+k)
    elif isinstance(e, list):
        need(isinstance(a,list) and len(a)==len(e), path+' shape')
        for j, (u,v) in enumerate(zip(a,e)):
            close(u,v,path+'[%d]'%j)
    elif type(e) is bool or e is None or type(e) is str:
        need(type(a) is type(e) and a==e, path+' literal')
    else:
        need(type(a) in (int,float,complex) and
             math.isfinite(a.real) and math.isfinite(a.imag) and abs(a-e)<=TOL,
             path+' numeric')


def intended_inputs():
    # Independent bit-basis construction: nearest-neighbor exchange only swaps01/10.
    def zeros(n=8):
        return [[0j for _ in range(n)] for _ in range(n)]
    H = zeros(); detached = zeros()
    for b in range(8):
        H[b][b] = detached[b][b] = complex(bin(b).count('1'))
        for left,right in [(4,2),(2,1)]:
            if bool(b & left) != bool(b & right):
                H[b ^ left ^ right][b] = 1+0j
                if left==4:
                    detached[b ^ left ^ right][b] = 1+0j
    eye = zeros(); source = zeros(); probe = zeros(); vacuum = zeros(); excited = zeros()
    for b in range(8):
        eye[b][b] = 1+0j
        source[b ^ 4][b] = 1+0j
        probe[b ^ 1][b] = 1+0j
    vacuum[0][0] = 1+0j; excited[4][4] = 1+0j
    offset = deepcopy(H)
    for b in range(8):
        offset[b][b] += 3
    times = [0.0, math.pi/(2*math.sqrt(2)), math.pi/math.sqrt(2)]
    def case(h=H,r=vacuum,w=source,v=probe,t=times):
        return deepcopy({'H':h,'rho0':r,'source':w,'probe':v,'times':t,'tolerance':TOL})
    valid = {'positive':case(), 'detached':case(h=detached), 'identical':case(w=eye),
             'reversed':case(r=excited), 'offset':case(h=offset)}
    density = deepcopy(vacuum); density[0][0]=2+0j; density[1][1]=-1+0j
    asym = deepcopy(H); asym[0][1]=1+0j
    twice = lambda m: [[2*x for x in row] for row in m]
    invalid = {'density':case(r=density), 'hermiticity':case(h=asym),
               'source':case(w=twice(source)), 'dimension':case(w=[[1+0j,0j],[0j,1+0j]]),
               'trace':case(r=twice(vacuum)), 'probe':case(v=twice(probe)),
               'too_many_times':case(t=list(range(33))), 'empty_times':case(t=[]),
               'negative_times':case(t=[-1.0]), 'boolean_times':case(t=[True])}
    return valid, invalid


def check(directory, runner):
    need(sha(runner)==RUNNER_SHA, 'runner pin')
    need(not (directory/'FAILURE.json').exists(), 'producer failure present')
    need(sha(directory/'SOURCE_SNAPSHOT.py')==SOURCE_SHA, 'actual executed source snapshot pin')
    start = load(directory/'START.json'); finish = load(directory/'FINISH.json')
    results = decoded(load(directory/'RESULTS.json'))
    need(start['source_sha256']==SOURCE_SHA and start['runner_sha256']==RUNNER_SHA,
         'start source/runner pins')
    need(sha(Path(start['source']))==SOURCE_SHA, 'current source differs')
    need(start['scope']=='FRESH_MANUFACTURED_P61_METHOD_ONLY' and start['native_scoring_release'] is False,
         'start scope')
    close(start['controls_tolerance'],TOL); close(start['valid_dimensions'],[8])
    close(start['time_count'],3); close(start['generic_time_cap'],32)
    need(finish['status']=='AWAITING_DISTINCT_SAVED_OUTPUT_CHECK' and
         finish['native_scoring_release'] is False,'finish scope')
    need(results['status']=='FRESH_METHOD_CONTROLS_ONLY_NO_NATIVE_FIELD_VERDICT','result scope')
    valid,invalid = intended_inputs()
    close(results['fixture_inputs'],valid,'fixture_inputs')
    close(results['analytic_expected'],[0,-0.5,-2],'analytic_expected')
    costs = {'positive':([1,1,1],[1,0.5,-1],0,1),
             'detached':([1,1,1],[1,1,1],0,1),
             'identical':([1,1,1],[1,1,1],0,0),
             'reversed':([1,0.5,-1],[1,1,1],1,0),
             'offset':([1,1,1],[1,0.5,-1],3,4)}
    top_diagnostics = ['initial_commutation_defect','source_unitarity_defect','probe_unitarity_defect',
                       'eigensystem_residual_2norm','orthogonality_defect']
    row_diagnostics = ['imaginary_cost_residual','sham_trace_error','source_trace_error','unitarity_defect',
                       'evolution_error_estimate','propagation_only_difference_error_estimate']
    for name,(sham,source,e0,e1) in costs.items():
        raw = results[name]
        need(raw['status']=='METHOD_OR_COMPARATOR_ONLY_NOT_FIELD_ACCEPTANCE' and
             raw['native_scoring_release'] is False and raw['H1']==raw['H2']=='UNDETERMINED', name+' scope')
        need(raw['error_scope']=='FLOAT_PROPAGATION_ESTIMATE_ONLY; input/source/probe/arithmetic certification absent',
             name+' error scope')
        close(raw['initial_sham_energy'],e0); close(raw['initial_source_energy'],e1)
        close(raw['initial_source_energy_change'],e1-e0)
        close(raw['read_norm'],1 if name=='detached' else math.sqrt(2))
        close(raw['input_min_eigenvalue'],0)
        for key in top_diagnostics:
            close(raw[key],0,name+'.'+key); need(raw[key]>=0,'nonnegative diagnostic')
        need(len(raw['rows'])==3,name+' three times')
        for j,row in enumerate(raw['rows']):
            close(row['time'],valid[name]['times'][j])
            close(row['sham_cost'],sham[j]); close(row['source_cost'],source[j])
            close(row['difference'],source[j]-sham[j])
            for key in row_diagnostics:
                close(row[key],0,name+'.'+key); need(row[key]>=0,'nonnegative diagnostic')
    guards = results['refusals']
    need(set(guards)==set(invalid),'complete ten refusals')
    messages = {'density':'nonpositive density','hermiticity':'exact stored Hermiticity required',
                'source':'nonunitary source or probe','dimension':'dimension mismatch',
                'trace':'density trace mismatch','probe':'nonunitary source or probe',
                'too_many_times':'at most32 times required',
                'empty_times':'nonempty nonnegative finite times required',
                'negative_times':'nonempty nonnegative finite times required',
                'boolean_times':'nonempty nonnegative finite times required'}
    for name,expected in invalid.items():
        g=guards[name]
        close(g['input'],expected,'refusal.'+name+'.input')
        need(g.get('refused') is True and g.get('exception')=='ValueError' and
             g.get('message')==messages[name] and 'unexpected_return' not in g,
             name+' actual guard failure')
    names=['START.json','SOURCE_SNAPSHOT.py','RESULTS.json','FINISH.json']
    return {'status':'PASS_FIVE_ARMS_TEN_REFUSALS_METHOD_ONLY', 'absolute_tolerance':TOL,
            'native_scoring_release':False,'producer_success_flags_used_as_evidence':False,
            'scientific_error_certificate':False,'resources':'ROOT_SUPERVISOR_ACCEPTANCE_SEPARATE',
            'saved_sha256':{n:sha(directory/n) for n in names}}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('directory',type=Path)
    parser.add_argument('runner',type=Path)
    args=parser.parse_args()
    print(json.dumps(check(args.directory,args.runner),indent=2,allow_nan=False))
