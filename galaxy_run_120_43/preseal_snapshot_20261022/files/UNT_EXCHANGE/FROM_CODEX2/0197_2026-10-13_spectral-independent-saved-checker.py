"""SOURCE ONLY: independent scalar spectral controls saved checker.
No NumPy, eigensolver, producer import or author-side execution.
Root owns launch, full runtime census and final adjudication.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
PINS = {'method': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_SPECTRAL_CODEX3/spectral_comparator_v003.py', 'sha256': 'ad4b3f0e7d9abd9f05e8989578fea82772ae6586c016435c1df9998a29e5ed56'}, 'controls': {'path': '/Users/bgm/Research/UNT_EXCHANGE/lanes/P49_SPECTRAL_CODEX3/spectral_controls_v002.py', 'sha256': '55c6d5705e9f03159a376b8db317607ef39f9d718fa285ce141c4e9eefa7d914'}}
RUNNER_PIN = 'd41aa81b5f9e21a0242dd94723bd82ef11115608ef021c275c4f620bf18cff9a'
NAMES = ['degenerate_identity_basis','degenerate_rotated_basis',
 'near_degenerate_distinct_levels','nondegenerate_eigh','identity_eigh',
 'absolute_shift_undo','nonorthogonal_full_basis','missing_eigenvector',
 'rounded_seed_reference_range_scope','second_moment_overflow','nonhermitian_input']
def need(ok,label):
    if not ok:raise ValueError(label)

def decode(raw):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'duplicate JSON');out[k]=v
        return out
    def bad(x):raise ValueError('nonfinite JSON')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)

def encode(v):
    if isinstance(v,complex):return {'real':v.real,'imag':v.imag}
    if isinstance(v,dict):return {k:encode(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [encode(x) for x in v]
    return v

def compare(a,b,label,strict=False):
    if isinstance(b,dict):
        need(type(a) is dict and set(a)==set(b),label+' fields')
        for k in b:compare(a[k],b[k],label+'/'+k,strict)
    elif isinstance(b,list):
        need(type(a) is list and len(a)==len(b),label+' length')
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,label+'/'+str(i),strict)
    elif type(b) in (float,int):
        tol=(1e-28+5e-15*abs(b)) if strict else 2e-12
        need(type(a) in (float,int) and math.isfinite(a) and abs(a-b)<=tol,label+' number')
    else:need(type(a)==type(b) and a==b,label+' literal')

def diag(xs):return [[complex(x if i==j else 0) for j in range(len(xs))] for i,x in enumerate(xs)]
def inner(x,y):return sum(a.conjugate()*b for a,b in zip(x,y))
def apply(h,x):return [sum(a*b for a,b in zip(row,x)) for row in h]
def vector(v):return [complex(x['real'],x['imag']) for x in v]

def fixed_inputs():
    rotation=[[.6+0j,-.8+0j,0j],[.8+0j,.6+0j,0j],[0j,0j,1+0j]]
    delta=2.0**-40
    near=[[.64*delta+0j,-.48*delta+0j,0j],[-.48*delta+0j,.36*delta+0j,0j],[0j,0j,2+0j]]
    matrices=[diag([0,0,2]),diag([0,0,2]),near,[[0j,-1+0j],[-1+0j,0j]],
              diag([1,1]),diag([0,0,2]),diag([0,0,2]),diag([0,0,2]),
              diag([1]),diag([1e200]),[[0j,1+0j],[0j,0j]]]
    energies=[[0,0,2],[0,0,2],[0,delta,2],None,None,[0,0,2],[0,0,2],[0,0],[1],[1e200],[0,0]]
    bases=[diag([1,1,1]),rotation,rotation,None,None,rotation,diag([2,2,2]),
           [[1+0j,0j],[0j,1+0j],[0j,0j]],diag([1]),diag([1]),diag([1,1])]
    rows=[]
    for i,h in enumerate(matrices):
        n=len(h);psi=[1]+[0]*(n-1)
        if i==8:psi=[1+2.5e-13]
        rows.append({'rows':[[[j,z] for j,z in enumerate(row) if z!=0] for row in h],
          'supplied_eigenvalues':energies[i],'supplied_eigenvectors':bases[i],
          'seeds':{'e0':psi},'diagonal_reads':{'P0':[1]+[0]*(n-1)},
          'row_scale':max(1.0,max(sum(abs(z) for z in row) for row in h)),
          'shift':7.0 if i==5 else 0.0,'eigh_requested':i in (3,4)})
    return rows

def reconstruct(inp,actual,index):
    n=len(inp['rows']);h=[[0j]*n for _ in range(n)]
    for i,row in enumerate(inp['rows']):
        for j,z in row:h[i][j]=z
    eigen=actual['actual_eigenvalues'];v=[vector(row) for row in actual['actual_eigenvectors']]
    need(len(eigen)==n and len(v)==n and all(len(row)==n for row in v),'complete eigensystem')
    if inp['eigh_requested']:
        compare(eigen,[-1.,1.] if index==3 else [1.,1.],'analytic eigenvalues',True)
    else:
        compare(eigen,inp['supplied_eigenvalues'],'supplied eigenvalues retained',True)
        compare(encode(v),encode(inp['supplied_eigenvectors']),'supplied eigenvectors retained',True)
    cols=[[v[i][j] for i in range(n)] for j in range(n)]
    residual=[]
    for e,col in zip(eigen,cols):
        residual.append(math.sqrt(sum(abs(x-e*y)**2 for x,y in zip(apply(h,col),col))))
    gram2=sum(abs(inner(a,b)-(i==j))**2 for i,a in enumerate(cols) for j,b in enumerate(cols))
    if inp['eigh_requested']:
        need(max(residual)<=2e-12 and math.sqrt(gram2)<=2e-12,'actual eigh independent analytic validation')
    psi=[complex(x) for x in inp['seeds']['e0']]
    weights=[abs(inner(col,psi))**2 for col in cols]
    amplitudes=[inner(col,psi) for col in cols]
    shift=inp['shift'];hp=[x+shift*y for x,y in zip(apply(h,psi),psi)]
    def block_read(groups):
        # Sum explicit coherent rank-one projector amplitudes, never diagonal
        # probabilities inside a degenerate block. Full tiny vector retained.
        value=0.;blockweights=[]
        for lo,hi in groups:
            projected=[sum(cols[j][i]*amplitudes[j] for j in range(lo,hi)) for i in range(n)]
            value+=abs(projected[0])**2
            blockweights.append([sum(weights[lo:hi])])
        return {'values_by_read_then_seed':[[value]],'groups_half_open':groups,
                'weights_by_group_then_seed':blockweights,'exact_block_certificate':False}
    single=block_read([[j,j+1] for j in range(n)])
    grouped=[]
    for tau in (1e-10,1e-8):
        threshold=tau*inp['row_scale'];cuts=[0]
        cuts.extend(j for j in range(1,n) if eigen[j]-eigen[j-1]>threshold);cuts.append(n)
        result=block_read([[a,b] for a,b in zip(cuts,cuts[1:])])
        result.update(tau=tau,absolute_threshold=threshold,grouping_scope='FLOAT_GAP_SENSITIVITY_ONLY_NOT_CERTIFIED_DEGENERACY')
        grouped.append(result)
    rf=math.sqrt(sum(x*x for x in residual));gf=math.sqrt(gram2)
    passed=rf/inp['row_scale']<=1e-9 and gf<=1e-8
    result={'status':'NUMERICAL_COMPARATOR_ONLY_EXACT_DE_UNRESOLVED' if passed else 'NUMERICAL_DIAGNOSTICS_FAILED',
      'seed_names':['e0'],'read_names':['P0'],'dimension':n,'shifted_eigenvalues':eigen,
      'absolute_eigenvalues':[e+shift for e in eigen],'energy_shift_undone':shift,
      'residual_column_l2':residual,'residual_frobenius':rf,'full_gram_frobenius':gf,
      'full_gram_block_records':[{'lo':0,'hi':n,'squared_frobenius':gram2}],
      'residual_relative_target':1e-9,'gram_target':1e-8,'diagnostics_passed':passed,
      'diagnostic_matrix':'ROUNDED_STORED_H','seed_norms':[sum(abs(x)**2 for x in psi)],
      'all_eigenmode_weights':[[w] for w in weights],'eigenmode_weight_sums':[sum(weights)],
      'original_energy':[inner(psi,hp)],'original_second_moment':[sum(abs(x)**2 for x in hp)],
      'singleton_basis_diagonal_comparator':single,'coherent_group_comparators':grouped,
      'normalized_reference_read_ranges':[[1.,1.]] if n==1 else [[0.,1.]],
      'reference_range_scope':'CONDITIONAL_ON_EXTERNALLY_AUTHENTICATED_EXACT_NORMALIZED_STATE_AND_EXACT_READ',
      'ranges_apply_to_rounded_supplied_seed':False,'desired_certified_word_half_width':'1/1024',
      'desired_certified_word_precision_met':False,'exact_DE_certified':False,'exact_degeneracy_certified':False,
      'Bohr_spacing_certified':False,'physical_state_selected':False,'EOS_claim':False,
      'native_prediction_release':False,'error_scope':'FLOAT_DIAGNOSTICS_WITHOUT_OUTWARD_ROUNDING_NOT_PROOF'}
    invariant={0:(1.,1.),1:(337/625,1.),2:(337/625,1.),3:(.5,.5),4:(None,1.),5:(337/625,1.),6:(16.,16.)}
    if index in invariant:
        a,b=invariant[index]
        if a is not None:compare(single['values_by_read_then_seed'][0][0],a,'analytic singleton invariant')
        for g in grouped:compare(g['values_by_read_then_seed'][0][0],b,'analytic coherent invariant')
    if index==8:need(result['seed_norms'][0]>1 and single['values_by_read_then_seed'][0][0]>1,'rounded seed exceeds reference range without renormalization')
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();root=args.input
    need(root.is_dir() and not root.is_symlink() and root.resolve()==root,'plain absolute input directory')
    names={'START.json','SOURCE_SNAPSHOTS.json','RESULTS.json','FINISH.json'}
    names|={'CALL_%02d_%s.json'%(i,k) for i in range(11) for k in ('PRE','RETURN')}
    entries=list(root.iterdir())
    need({p.name for p in entries}==names and all(p.is_file() and not p.is_symlink() for p in entries),'whole26filecensus')
    need(sum(p.stat().st_size for p in entries)<=16*2**20,'whole bounded input')
    raws={p.name:p.read_bytes() for p in entries};docs={n:decode(b) for n,b in raws.items()}
    snap=docs['SOURCE_SNAPSHOTS.json'];need(set(snap)==set(PINS),'complete two snapshots')
    for role,pin in PINS.items():need(type(snap[role]) is str and hashlib.sha256(snap[role].encode()).hexdigest()==pin['sha256'],'full source snapshot '+role)
    compare(docs['START.json'],{'scope':'P49_SPECTRAL_ELEVEN_METHOD_CONTROLS_ONLY','sources':PINS,
      'runner_sha256':RUNNER_PIN,'call_names':NAMES,'native_solve_released':False,'external_supervisor_required':True},'START')
    calls=[]
    errors={7:'complete square eigensystem census',9:'finite energy and second moment',10:'stored Hermitian matrix'}
    for i,(name,inp) in enumerate(zip(NAMES,fixed_inputs())):
        pre=docs['CALL_%02d_PRE.json'%i];compare(pre,encode({'name':name,'inputs':inp}),name+'/PRE',True)
        record=docs['CALL_%02d_RETURN.json'%i]
        need(type(record) is dict and set(record)=={'name','actual'} and record['name']==name,'return envelope')
        actual=record['actual']
        if i in errors:
            expected={'inputs':inp,'refused':True,'exception':'ValueError','message':errors[i]}
        else:
            expected={'inputs':inp,'refused':False,'value':reconstruct(inp,actual,i),
                      'actual_eigenvalues':actual['actual_eigenvalues'],'actual_eigenvectors':actual['actual_eigenvectors']}
        compare(actual,encode(expected),name+'/RETURN')
        compare(actual['inputs'],pre['inputs'],name+'/unaltered actual input',True)
        calls.append(record)
    literals={'degenerate_whole_block_P0':'1','rotated_singleton_P0':'337/625',
      'near_distinct_exact_DE_P0':'337/625','near_merged_group_comparator_P0':'1',
      'nondegenerate_exact_DE_P0':'1/2','identity_exact_DE_P0':'1','shifted_absolute_seed_energy':'7',
      'nonorthogonal_full_basis':'NUMERICAL_DIAGNOSTICS_FAILED','missing_eigenvector':'ValueError',
      'nonhermitian_input':'ValueError','rounded_seed_reference_range_scope':'CONDITIONAL_REFERENCE_ONLY_NOT_SUPPLIED_SEED_BOUND',
      'second_moment_overflow':'ValueError: finite energy and second moment'}
    compare(docs['RESULTS.json'],{'calls':calls,'call_count':11,'expected_exact_mathematics_not_computed_by_flags':literals,
      'scope':'DEGENERACY_SENSITIVE_MANUFACTURED_COMPARATORS','acceptance':'DISTINCT_SAVED_CHECKER_REQUIRED',
      'native_exact_DE_certified':False,'physical_state_selected':False},'RESULTS')
    compare(docs['FINISH.json'],{'status':'RAW_METHOD_OUTPUT_AWAITING_DISTINCT_SAVED_CHECKER',
      'call_names':NAMES,'call_count':11,'native_solve_released':False,'exact_DE_certified':False,
      'scientific_source_closing_hashes_match':True},'FINISH')
    for name,raw in raws.items():need((root/name).read_bytes()==raw,'closing bytes '+name)
    report={'status':'INDEPENDENT_ELEVEN_SPECTRAL_SAVED_CONTROLS_PASS','author':'Codex2',
      'complete_files':26,'returned_diagnostics':8,'actual_refusals':3,'nonorthogonal_diagnostic_failure_checked':True,
      'output_absolute_tolerance':2e-12,'input_tolerance':'1e-28+5e-15*abs(expected)',
      'original_files':{n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in raws.items()},
      'numeric_comparison_only_not_outward_certificate':True,'native_exact_DE_certified':False,
      'requires_distinct_root_adjudication':True,'physical_release':False,
      'resource_acceptance':'ORIGINAL_ROOT_PROCESS_AND_WHOLE_RUNTIME_CUSTODY_REQUIRED'}
    with args.output.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

if __name__=='__main__':main()
