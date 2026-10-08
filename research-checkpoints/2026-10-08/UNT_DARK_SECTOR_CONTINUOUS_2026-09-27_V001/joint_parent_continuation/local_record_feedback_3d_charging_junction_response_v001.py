#!/usr/bin/env python3
"""NEW saved finite-M charging/junction responses; no producer/H/RNG imports."""
from pathlib import Path
import hashlib,json,math,os,re,sys,time,traceback
import numpy as np

J=Path(__file__).resolve().parent
NAME='LOCAL_RECORD_FEEDBACK_3D_CHARGING_JUNCTION_RESPONSE_V001'
JOINT='LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001'
QUERY='LOCAL_RECORD_FEEDBACK_3D_QUERY_RESPONSE_RECOVERY_V001'
STRAIN='LOCAL_RECORD_FEEDBACK_3D_SIX_STRAIN_CHARGING_STIFFNESS_V001'
SOURCE=Path(__file__).resolve();PROTOCOL=J/(NAME+'.md')
PROTOCOL_SHA='570c4862d9e000be2ba5fe467a4310bd1ed1f8cb82a8e6b7330b1cf4b67523a7'
PARENTS=[(JOINT,'local_record_feedback_3d_pair_coordination_response_v001',180914),
 (QUERY,'local_record_feedback_3d_query_response_recovery_v001',364),
 (STRAIN,'local_record_feedback_3d_six_strain_charging_stiffness_v001',13500)]
PCP=J/(PARENTS[0][1]+'_checkpoints')
CP=J/'local_record_feedback_3d_charging_junction_response_v001_checkpoints'
RESULT,REPORT,RECEIPT=(J/(NAME+s) for s in ('_RESULT.json','_RESULT.md','_RECEIPT.json'))
H0=.2;V=54;N=27;UNIFORM=np.array([1.,1.,1.,0.,0.,0.])
R=np.r_[np.ones(12),-1,-1]/2
CHECKS=[];STAGES={};CREATED=False;ACTIVE=None

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def require(ok,label):
    if not ok:raise RuntimeError('Custody: '+label)
def unpack(v):return np.asarray(v['real'])+1j*np.asarray(v['imag']) if isinstance(v,dict) else np.asarray(v)
def pack(v):
    a=np.asarray(v);return {'real':a.real.tolist(),'imag':a.imag.tolist()} if np.iscomplexobj(a) else a.tolist()
def safe(v):
    if isinstance(v,dict):return {k:safe(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [safe(x) for x in v]
    if isinstance(v,(float,np.floating)) and not math.isfinite(float(v)):return {'nonfinite':repr(float(v))}
    return v
def close(label,a,b):
    error=float(np.linalg.norm(np.asarray(a)-np.asarray(b)));tol=3e-11*max(1,float(np.linalg.norm(np.asarray(b))))
    c={'label':label,'passed':math.isfinite(error) and error<=tol,'residual':safe(error),'tolerance':tol};CHECKS.append(c)
    if not c['passed']:raise ArithmeticError(label)
def exclusive(p,v):
    with p.open('xb') as f:f.write(canonical(v)+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)
def event(kind,**fields):
    with (CP/'journal.jsonl').open('ab') as f:f.write(canonical({'event':kind,'pid':os.getpid(),**fields})+b'\n');f.flush();os.fsync(f.fileno())
def save(name,v):
    STAGES[name]=exclusive(CP/name,v);event('stage_complete',filename=name,sha256=STAGES[name])

def authenticate():
    actual={};parents={}
    def track(p,wanted=None):
        p=p.resolve();key=os.path.relpath(p,J)
        if key not in actual:actual[key]=sha(p)
        require(wanted is None or actual[key]==wanted,'input '+key)
        return actual[key]
    require(track(PROTOCOL)==PROTOCOL_SHA,'frozen protocol');actual['source']=sha(SOURCE);actual['protocol']=actual.pop(PROTOCOL.name)
    anchors=re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$',PROTOCOL.read_text(),re.M)
    require(len(anchors)==16,'sixteen direct pins')
    for filename,wanted in anchors:track(J/filename,wanted)
    for name,stem,count in PARENTS:
        p,r=read(J/(name+'_RESULT.json')),read(J/(name+'_RECEIPT.json'))
        require(r['result_sha256']==track(J/(name+'_RESULT.json')) and r['report_sha256']==track(J/(name+'_RESULT.md')),'raw/report '+name)
        require(r['result_canonical_sha256']==hashlib.sha256(canonical(p)).hexdigest(),'canonical '+name)
        require(p['input_sha256']==r['input_sha256'] and p['passed']==r['passed']==len(p['checks'])==count and p['failed']==r['failed']==0 and
                all(c['passed'] for c in p['checks']) and p['status']==r['status'],'controls/status '+name)
        directory=J/(stem+'_checkpoints');lines=(directory/'journal.jsonl').read_bytes().splitlines(keepends=True);es=[json.loads(x) for x in lines]
        require(hashlib.sha256(b''.join(lines[:-1])).hexdigest()==r['journal_prefix_sha256'] and es[-1]['event']=='receipt_complete' and
                es[-1]['sha256']==track(J/(name+'_RECEIPT.json')),'journal prefix/receipt '+name)
        track(directory/'journal.jsonl');commits={(e.get('filename'),e.get('sha256')) for e in es}
        for f,h in r['checkpoint_sha256'].items():
            track(directory/f,h);require((f,h) in commits,'checkpoint commit '+f)
        manifest=read(directory/'manifest.json')
        require(manifest['input_sha256']==r['input_sha256'] and any(e['event']=='started' and e['input_sha256']==r['input_sha256'] and
                e['manifest_sha256']==r['checkpoint_sha256']['manifest.json'] for e in es),'manifest/start '+name)
        for f,h in r['input_sha256'].items():
            if f=='core_identity_canonical_sha256':
                require(hashlib.sha256(canonical(manifest['preserved_core_identity'])).hexdigest()==h,'virtual core identity');continue
            track(J/(stem+'.py' if f=='source' else name+'.md' if f=='protocol' else f),h)
        parents[name]=p
    joint=parents[JOINT];ids=[f'c{i}_{s}' for i in range(4) for s in ('I01','I02','B','R')]
    require([r['id'] for r in joint['chains']]==ids and len(joint['conditions'])==4 and joint['characters'][0]==[0,0,0],'fixed census')
    old={r['id']:r for r in joint['chains']};old.update({f"condition{r['condition']}":r for r in joint['conditions']})
    for name in (QUERY,STRAIN):
        rows=parents[name]['rows'];require([r['id'] for r in rows]==ids+[f'condition{i}' for i in range(4)],'all20 '+name)
        require([r['block_count'] for r in rows]==[32]*16+[128]*4 and all(r['block_measurements']==32 and r['parent_status']==old[r['id']]['status'] for r in rows),'blocks/status '+name)
    models=parents[STRAIN]['models'];require([m['AR_fraction'] for m in models]==['1/8','7/40','1/4'],'all fixed branches')
    for m in models:
        require(m['alpha']==m['qstar']==m['qR']==m['U']==1 and m['lambda']==.5,'fixed charging normalization')
        close('model_uniform_'+m['AR_fraction'],UNIFORM@unpack(m['source_rows']),-R)
    return actual,joint,parents,old,models

def load_chain(row,receipt):
    ref=row['checkpoints'][-1];meta=read(PCP/ref['metadata']);label=row['id']
    require(ref['bundle']==label+'_production1024.npz' and ref['metadata']==label+'_production1024.json' and
            ref['bundle_sha256']==meta['bundle_sha256']==receipt['checkpoint_sha256'][ref['bundle']] and
            ref['metadata_sha256']==receipt['checkpoint_sha256'][ref['metadata']] and meta['input_sha256']==receipt['input_sha256'],'terminal seals')
    require(meta['completed_production_sweeps']==row['production_sweeps']==1024 and meta['completed_burn_sweeps']==64 and
            meta['configuration']=={k:row[k] for k in ('seed','beta','epsilon','M','start')},'terminal counters/config')
    with np.load(PCP/ref['bundle'],allow_pickle=False) as z:
        scalar=z['scalar'];diag=z['diagnostic_traces'];q=z['bar_Q_every_production_measurement'][:,0,:]
    require(scalar.shape==(1024,15) and diag.shape==(1024,34) and q.shape==(1024,14),'paired production shapes')
    require(all(np.isfinite(x).all() for x in (scalar,diag,q)),'finite paired traces')
    close(label+'_scalar_trace',scalar,row['scalar_traces']);close(label+'_diagnostic_trace',diag,row['diagnostic_traces'])
    close(label+'_Q14_trace',q,unpack(row['joint_bar_Q_traces'])[:,0,:]);close(label+'_k0_imaginary',q.imag,np.zeros(q.shape))
    beta,eps,M=row['beta'],row['epsilon'],row['M'];close(label+'_betaM',eps*M,beta)
    e,k=scalar[:,6],scalar[:,7];require(np.all(k==np.floor(k)) and np.all(k%2==0) and np.all((k>=0)&(k<=108*M)),'integer temporal kinks')
    close(label+'_scalar_Etrans',scalar[:,0]-scalar[:,1],e);close(label+'_diagnostic_Etrans',diag[:,0]-diag[:,1],e)
    x=eps*H0;th=math.tanh(x);ct=1/th;sech=1/math.cosh(x)**2;csch=1/math.sinh(x)**2;B=108*M
    sh=eps*(B*th+k*(ct-th));shh=eps*eps*(B*sech-k*(csch+sech))
    close(label+'_transverse_estimator',-H0*(B*th+k*(ct-th))/(M*V),e)
    close(label+'_score_energy',sh,-beta*V*e/H0)
    r=q@R;D=1+math.sqrt(N)*r/V;close(label+'_D_from_Q',D,scalar[:,1])
    raw={'q':q,'qE':q*e[:,None],'rr':abs(r)**2,'e':e,'k':k,'sh':sh,'sh2':sh*sh,'shh':shh,'D':D}
    return {key:value.reshape((32,32)+value.shape[1:]).sum(axis=1) for key,value in raw.items()}

def calculate(raw,beta,model,label):
    q,e=raw['q'],raw['e'];r=q@R;D=raw['D'];source=unpack(model['source_rows'])
    score_var=raw['sh2']-raw['sh']**2;score_contact=raw['shh']
    hh=(score_var+score_contact)/(beta*V)
    ah=beta*math.sqrt(N)*(source@(raw['qE']-q*e))/H0;uniform=UNIFORM@ah
    rrvar=raw['rr']-abs(r)**2;dd=beta*N*rrvar/V;Jmean=D+model['AR']+model['alpha'];contact=2*Jmean;cap=contact-dd
    close(label+'_uniform_score_mixed',uniform,-beta*math.sqrt(N)*(R@(raw['qE']-q*e))/H0)
    close(label+'_D_mean',D,1+math.sqrt(N)*r/V)
    coeff=np.array([cap+2*e+2*H0*uniform-H0*H0*hh,4*e/H0+2*uniform-2*H0*hh,-hh])
    for ht in (0.,1.,-1.):
        direct=cap+(2*H0+4*ht)*e/H0+2*(H0+ht)*uniform-(H0+ht)**2*hh
        close(label+'_polynomial_identity_'+str(ht),coeff@np.array([1.,ht,ht*ht]),direct)
    return {'mean_transverse_energy_density':e,'mean_kinks':raw['k'],'mean_h_score':raw['sh'],'variance_h_score':score_var,
            'mean_direct_log_weight_hh_contact':score_contact,'score_variance_density':score_var/(beta*V),
            'score_contact_density':score_contact/(beta*V),'chi_hh_density':hh,'chi_Ah_six_density':ah,'chi_uniform_h_density':uniform,
            'mean_D_density':D,'mean_Jcap_density':Jmean,'charging_contact_density':contact,'chi_DD_density':dd,
            'Kcap_uniform_density':cap,'symbolic_hT_polynomial_coefficients':coeff}

def dataset(label,blocks,beta,query,strain,models):
    count=len(blocks['e']);require(count in (32,128) and all(len(v)==count for v in blocks.values()),'complete block census')
    means={k:v/32 for k,v in blocks.items()};raw={k:v.mean(axis=0) for k,v in means.items()}
    close(label+'_query_Q_blocks',blocks['q'],unpack(query['raw_block_sufficient_sums']['q']))
    close(label+'_query_rr_blocks',blocks['rr'],np.einsum('i,bij,j->b',R,unpack(query['raw_block_sufficient_sums']['qq']),R))
    branches=[]
    for index,model in enumerate(models):
        ACTIVE['branch']=model['AR_fraction'];tag=label+'_AR'+model['AR_fraction'];values=calculate(raw,beta,model,tag+'_central')
        parent=strain['branches'][index];require(parent['AR_fraction']==model['AR_fraction'],'parent branch ordering')
        for new,old in [('charging_contact_density','uniform_contact_density'),('chi_DD_density','uniform_susceptibility_density'),('Kcap_uniform_density','uniform_curvature_density')]:
            close(tag+'_parent_'+new,values[new],unpack(parent['values'][old]))
        replicas=[calculate({k:(count*raw[k]-v[i])/(count-1) for k,v in means.items()},beta,model,tag+f'_replica{i}') for i in range(count)]
        errors={}
        for key in values:
            a=np.array([r[key] for r in replicas]);errors[key]={}
            for part in ('real','imag'):
                aa=getattr(a,part);errors[key][part+'_se']=pack(np.sqrt((count-1)/count*((aa-aa.mean(axis=0))**2).sum(axis=0)))
        branches.append({'AR_fraction':model['AR_fraction'],'parent_status':query['parent_status'],
          'values':{k:pack(v) for k,v in values.items()},'component_errors':errors,
          'leave_one_complete_block_replicas':[{k:pack(v) for k,v in r.items()} for r in replicas]})
        ACTIVE['completed_active_branch_rows']=branches.copy()
    return {'id':label,'beta':beta,'block_count':count,'block_measurements':32,'parent_status':query['parent_status'],
      'raw_block_sufficient_sums':{k:pack(v) for k,v in blocks.items()},'branches':branches,
      'scope':'POSTHOC_FINITE_M_CLAMPED_CHARGING_PLUS_OFFDIAGONAL_JUNCTION_NO_HT_SELECTED'}

def format_report(rows):
    lines=['# Saved charging and junction responses V001','',
      'All fixed parent datasets and three AR branches retained. hT stays symbolic; direct finite-M transverse contact is included.','',
      '| Dataset | AR | chi_hh ± SE | chi_uniform,h ± SE | c0 ± SE | c1 ± SE | c2 ± SE | Parent status |','|---|---|---|---|---|---|---|---|']
    for row in rows:
        for branch in row['branches']:
            v,err=branch['values'],branch['component_errors'];coeff=unpack(v['symbolic_hT_polynomial_coefficients']).real;se=np.asarray(err['symbolic_hT_polynomial_coefficients']['real_se'])
            show=lambda k:f"{unpack(v[k]).real:.9g} ± {err[k]['real_se']:.3g}"
            lines.append(f"| {row['id']} | {branch['AR_fraction']} | {show('chi_hh_density')} | {show('chi_uniform_h_density')} | "+
              ' | '.join(f'{x:.9g} ± {s:.3g}' for x,s in zip(coeff,se))+f" | {row['parent_status']} |")
    require(sum(x.startswith('| c') for x in lines)==60,'sixty branch report rows')
    lines+=['','JSON retains every signed variance/contact, six mixed-source entry, all paired block moments and3,072 correlated replicas with real/imaginary errors.',
      'Inherited diagnostics and failures remain unchanged. These posthoc finite-M canonical sector derivatives do not establish equilibration of the new score, a microscopic hT, complete mechanical stiffness, support stability, physical metric, pressure, expansion or gravity. No favorable parameter window is selected.','']
    return '\n'.join(lines)

def main():
    global CREATED,ACTIVE
    require(sys.argv[1:]==['--execute'],'exact --execute');require(not any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT)),'reserved absence')
    inputs,joint,parents,old,models=authenticate();CP.mkdir();CREATED=True
    save('manifest.json',{'input_sha256':inputs,'pid':os.getpid(),'h0':H0,'symbolic_hT':True,'all20_datasets':True,'AR_fractions':[m['AR_fraction'] for m in models]})
    event('started',input_sha256=inputs,manifest_sha256=STAGES['manifest.json'])
    query={r['id']:r for r in parents[QUERY]['rows']};strain={r['id']:r for r in parents[STRAIN]['rows']}
    receipt=read(J/(JOINT+'_RECEIPT.json'));chainblocks={};rows=[]
    for chain in joint['chains']:
        label=chain['id'];ACTIVE={'dataset':label,'branch':None,'phase':'SAVED_PAIRED_SCORE_EXTRACTION'}
        blocks=load_chain(chain,receipt);chainblocks[label]=blocks
        row=dataset(label,blocks,chain['beta'],query[label],strain[label],models);rows.append(row);save(label+'.json',row)
    for condition in joint['conditions']:
        label='condition'+str(condition['condition']);ACTIVE={'dataset':label,'branch':None,'phase':'POOLED_RAW_BLOCKS_BEFORE_CENTERING'}
        blocks={k:np.concatenate([chainblocks[c][k] for c in condition['chain_ids']]) for k in chainblocks[condition['chain_ids'][0]]}
        row=dataset(label,blocks,condition['beta'],query[label],strain[label],models);rows.append(row);save(label+'.json',row)
    require(authenticate()[0]==inputs,'unchanged inputs before seal');ACTIVE=None
    result={'name':NAME,'input_sha256':inputs,'rows':rows,'symbolic_hT_selected':False,'h0':H0,'checks':CHECKS.copy(),'passed':len(CHECKS),'failed':0,
      'status':'SAVED_FINITE_M_JUNCTION_RESPONSE_PARENT_QUALIFICATIONS_UNCHANGED','elapsed_seconds':time.perf_counter()-T0}
    report=format_report(rows);raw=exclusive(RESULT,result);event('result_complete',filename=RESULT.name,sha256=raw)
    with REPORT.open('x') as f:f.write(report);f.flush();os.fsync(f.fileno())
    event('report_complete',filename=REPORT.name,sha256=sha(REPORT))
    receipt={'result_sha256':raw,'result_canonical_sha256':hashlib.sha256(canonical(result)).hexdigest(),'report_sha256':sha(REPORT),'input_sha256':inputs,
      'checkpoint_sha256':STAGES.copy(),'journal_prefix_sha256':sha(CP/'journal.jsonl'),'passed':len(CHECKS),'failed':0,'pid':os.getpid(),'status':result['status']}
    digest=exclusive(RECEIPT,receipt);event('receipt_complete',filename=RECEIPT.name,sha256=digest)
    print(json.dumps({'passed':len(CHECKS),'failed':0,'result_sha256':raw,'receipt_sha256':digest}),flush=True)

if __name__=='__main__':
    T0=time.perf_counter()
    try:main()
    except Exception as error:
        if CREATED:save('ERROR.json',safe({'error':str(error),'error_type':type(error).__name__,'traceback':traceback.format_exc(),'active':ACTIVE,
          'checks':CHECKS.copy(),'status':'ARITHMETIC_FAILED' if isinstance(error,ArithmeticError) else 'EXECUTION_FAILED'}))
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
