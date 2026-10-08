"""Root-only saved arithmetic; no producer/background/trajectory calls."""
from pathlib import Path
from decimal import Decimal, localcontext
import datetime, hashlib, json, math, os, sys

BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_COSMIC_SAVED_DENSITY_CANCELLATION_V001'
PROTOCOL_SHA='a1c51129d6f7fa9cb9ed1e878d1f361a759f20e0f86446a10b47cce113f5919c'
PARENT='CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V005'
PINS={PARENT+'_RESULT.json':'cf005bce78fcd7358c37f6bb53051128b02bf764c1dd8f346d410864931d6c27',
 PARENT+'_RECEIPT.json':'dddb4e40e9dc9c5148245a6d35670cf173b989d61f1fd0d6fe3e9a6e9705f697',
 'constrained_u_clock_gradient_early_transfer_v005.py':'bfee912d66cbfd91b9d80630c15cbe1cf32c4c905f0d736c4491113f01d84b20',
 PARENT+'.md':'027233e02902b2905a5f172e3aaec6ab297a956e5e66a1f058ffbb36f66c93a6'}
VARIABLES=('comoving_baryon_density','comoving_radiation_density','comoving_clock_density')

def require(ok,message):
    if not ok: raise AssertionError(message)

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def finite(v):
    if type(v) is dict:
        require(all(type(k) is str for k in v),'Native keys')
        for value in v.values(): finite(value)
    elif type(v) is list:
        for value in v: finite(value)
    else:
        require(type(v) in (str,int,float,bool,type(None)),'Native JSON')
        require(type(v) is not float or math.isfinite(v),'Finite JSON')

def canonical(v):
    finite(v)
    return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def decimal_strings(v):
    if type(v) is Decimal: return str(v)
    if type(v) is dict: return {k:decimal_strings(x) for k,x in v.items()}
    if type(v) is list: return [decimal_strings(x) for x in v]
    return v

def write(path,value):
    encoded=canonical(decimal_strings(value))
    with path.open('xb') as stream: stream.write(encoded)
    path.chmod(0o444)
    return sha(path)

def lift(v):
    require(type(v) in (int,float),'Actual numeric input')
    return Decimal.from_float(v) if type(v) is float else Decimal(v)

def left_sum(values):
    ans=0.0
    for value in values: ans+=value
    return ans

def state_arithmetic(case,fgamma):
    y=case['state']; bg=case['background']
    h,b,r,w=(bg[k] for k in ('h','b','r','w'))
    rg,rn=r*fgamma,r*(1-fgamma)
    H,B,RG,RN,W=map(lift,(h,b,rg,rn,w))
    coordinates={}; exact={}
    for name,di,ui,m in [('baryon',1,2,3),('photon',3,4,4),('neutrino',5,6,4),('clock',7,8,3)]:
        d,u=lift(y[di]),lift(y[ui]);c=d+m*H*u; envelope=abs(d)+m*abs(H*u)
        coordinates[name]=dict(delta=d,u=u,h=H,m=m,contrast=c,envelope=envelope,
            cancellation_ratio=envelope/abs(c) if c else None,zero_contrast=(c==0))
        exact[name]=(B if name=='baryon' else RG if name=='photon' else RN if name=='neutrino' else W)*c
    exact['radiation']=exact['photon']+exact['neutrino']
    saved=dict(baryon=case['readouts'][8],radiation=case['readouts'][9],clock=case['readouts'][10],
        photon=case['signed_sources']['photon'],neutrino=case['signed_sources']['neutrino'])
    terms=[lift(x) for x in case['normal_terms']]
    moment=B*lift(y[2])+Decimal(4)/3*(RG*lift(y[4])+RN*lift(y[6]))+W*lift(y[8])
    rebuilt=[terms[0],3*H*moment,B*lift(y[1]),RG*lift(y[3]),RN*lift(y[5]),W*lift(y[7]),terms[6]]
    comoving=[terms[0],exact['baryon'],exact['photon'],exact['neutrino'],exact['clock'],terms[6]]
    return dict(raw_core=y[:9],binary_weights=dict(h=h,b=b,rg=rg,rn=rn,w=w),coordinates=coordinates,
        exact_weighted_sources=exact,saved_weighted_sources=saved,
        final_readout_rounding={k:lift(saved[k])-exact[k] for k in saved},
        normal=dict(held_saved_terms=case['normal_terms'],exact_sum_saved_terms=sum(terms,Decimal(0)),
            original_binary_sum=left_sum(case['normal_terms']),original_denominator=max(left_sum([abs(x) for x in case['normal_terms']]),case['normal_floor']),
            original_error=case['normal_error'],rebuilt_seven_terms=rebuilt,
            rebuilt_seven_sum=sum(rebuilt,Decimal(0)),rebuilt_comoving_sum=sum(comoving,Decimal(0)),
            held_metric_native_endpoints=True))

def pair_arithmetic(other,fine,fgamma):
    a,f=state_arithmetic(other,fgamma),state_arithmetic(fine,fgamma)
    deltas={}
    for name in a['coordinates']:
        x,z=a['coordinates'][name],f['coordinates'][name]
        dd,du,dh=x['delta']-z['delta'],x['u']-z['u'],x['h']-z['h']
        terms=[dd,x['m']*z['h']*du,x['m']*z['u']*dh,x['m']*dh*du]
        delta=x['contrast']-z['contrast']
        deltas[name]=dict(exact_contrast_difference=delta,independent_delta_terms=terms,
            identity_residual=delta-sum(terms,Decimal(0)))
    return dict(other=a,fine=f,contrast_differences=deltas,
        exact_source_differences={k:a['exact_weighted_sources'][k]-f['exact_weighted_sources'][k] for k in a['exact_weighted_sources']})

def main():
    require(sys.argv[1:]==['--root-owned'],'Root launch only')
    paths={name:BASE/name for name in PINS}
    seals={str(path):PINS[name] for name,path in paths.items()}
    seals[str(Path(__file__).resolve())]=sha(__file__)
    seals[str(BASE/(STEM+'.md'))]=PROTOCOL_SHA
    def recheck():
        for path,digest in seals.items(): require(sha(path)==digest,'Unchanged bytes '+path)
    result_path,receipt_path=BASE/(STEM+'_RESULT.json'),BASE/(STEM+'_RECEIPT.json')
    require(not result_path.exists() and not receipt_path.exists(),'Exclusive unused publication')
    recheck(); started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result=json.loads(paths[PARENT+'_RESULT.json'].read_text());receipt=json.loads(paths[PARENT+'_RECEIPT.json'].read_text())
    finite(result);finite(receipt)
    require(receipt['result_sha256']==PINS[PARENT+'_RESULT.json'] and receipt['source_sha256']==PINS['constrained_u_clock_gradient_early_transfer_v005.py'],'Closed result/source binding')
    gates=result['numerical_gates'];require(len(gates)==527 and sum(g['passed'] for g in gates)==499,'Preserve499/527 and28 failures')
    failures=[g for g in gates if not g['passed']]
    selected=[g for g in failures if g['name'] in ('time_refinement','start_refinement')]
    require(len(selected)==24 and len([g for g in failures if g['name']=='normal_error' and g['trial']=='BASE'])==4,'Exact failed census')
    expected={(name,omega,var) for name in ('time_refinement','start_refinement') for omega in (.1,1.,10.,100.) for var in VARIABLES}
    require({(g['name'],g['omega'],g['variable']) for g in selected}==expected,'All24 inherited gates')
    trials={v['label']:v for v in result['rows']};fine=trials['TIME'];omegas=result['manifest']['omegas']
    require(omegas==[.1,1.,10.,100.] and len(result['readout_names'])==15,'Fixed case/readout order')
    rows=[]
    with localcontext() as context:
        context.prec=160
        for gate in selected:
            label='time' if gate['name']=='time_refinement' else 'start';other=trials['BASE' if label=='time' else 'START']
            require(len(fine['snapshots'])==len(other['snapshots'])==68,'All68 saved targets')
            oi=omegas.index(gate['omega']);vi=result['readout_names'].index(gate['variable'])
            comp=next(c for c in result['comparisons'] if c['label']==label)
            peak=-1.0;index=None;difference=None
            for j,(a,f) in enumerate(zip(other['snapshots'],fine['snapshots'])):
                require(a['x']==f['x'],'Same saved target')
                value=a['cases'][oi]['readouts'][vi]-f['cases'][oi]['readouts'][vi]
                if abs(value)>peak: peak,index,difference=abs(value),j,value
            den=comp['normalization'][oi][vi]
            require(peak==comp['maximum_trace_difference'][oi][vi] and peak/den==gate['error'],'Original first peak/error identity')
            a,f=other['snapshots'][index]['cases'][oi],fine['snapshots'][index]['cases'][oi]
            rows.append(dict(original_gate=gate,other_trial=other['label'],reference='TIME',first_peak_index=index,
                x=a['x'],a=a['a'],original_signed_difference=difference,original_normalization=den,
                arithmetic=pair_arithmetic(a,f,result['manifest']['fixed']['fgamma'])))
    ended=datetime.datetime.now(datetime.timezone.utc).isoformat();recheck()
    output=dict(status='SAVED_DENSITY_CANCELLATION_DESCRIPTIVE',owner='root',pid=os.getpid(),start_utc=started,end_utc=ended,
        source_sha256=seals[str(Path(__file__).resolve())],protocol_sha256=PROTOCOL_SHA,input_sha256={name:PINS[name] for name in PINS},
        decimal_precision=160,original_status=result['status'],original_gates=gates,original_pass=499,original_fail=28,
        inherited_fixed=result['manifest']['fixed'],rows=rows,
        late_sampled_domain_heads=[c['domain_heads'] for c in fine['snapshots'][-1]['cases']],
        physical_qualification=False,original_failures_promoted=False,J4_result_present=False,
        scope='Final-readout rounding isolated; propagated versus prepared-state origin remains unseparated; no trajectory or physical qualification.')
    digest=write(result_path,output);recheck();require(sha(result_path)==digest,'Published result bytes')
    receipt_out=dict(owner='root',pid=os.getpid(),start_utc=started,end_utc=ended,source_sha256=output['source_sha256'],
        protocol_sha256=PROTOCOL_SHA,input_sha256=output['input_sha256'],result_sha256=digest,result=str(result_path),
        original_pass=499,original_fail=28,selected_rows=24,physical_qualification=False)
    rec=write(receipt_path,receipt_out);recheck();require(sha(result_path)==digest and sha(receipt_path)==rec,'Final output seals')
    print('Saved24 density peaks; all28 inherited failures retained.')

if __name__=='__main__': main()
