"""Independent saved endpoint arithmetic; no producer import or execution."""
from pathlib import Path
import hashlib,json,math
J=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def main():
    count=0;fail=[];maximum=0
    def ck(k,v):
        nonlocal count
        count+=1
        if not v:fail.append(k)
    def close(k,a,b):
        nonlocal maximum
        e=abs(a-b);maximum=max(maximum,e);ck(k,math.isfinite(e) and e<=2e-14)
    rb=(J/'CMB_TZ_SOURCE_INTERVAL_V001.json').read_bytes();fb=(J/'CMB_TZ_SOURCE_INTERVAL_V001_FROZEN.json').read_bytes()
    j=json.loads(rb);f=json.loads(fb);p=j['payload']
    ck('result pin',sha(rb)=='c1a27492bf8b7ab799e56102dec2ae897f58afcd7ada9a5bd5a0d9dbb0f6d25b')
    ck('freeze',sha(fb)==j['freeze_sha256']=='64d4bd5f5e3a540dcbd662381b4addd179dbddceb1517ed21aa913615e5caf87')
    ck('payload',sha(enc(p))==j['payload_sha256'])
    for x in f['files']:
        b=Path(x['path']).read_bytes();ck('member '+x['path'],len(b)==x['bytes'] and sha(b)==x['sha256'])
    a=json.loads((J/'CMB_TZ_SOURCE_INTERVAL_INPUTS_V001.json').read_bytes());ck('input',a==p['inputs'])
    ck('census',len(p['observations'])==3 and len(p['checks'])==47 and not p['failures'])
    ck('flags',not p['combined_likelihood'] and not p['global_confidence_coverage_claim'] and p['fitted_parameters']==0)
    T=a['T0_K'];dT=a['T0_reported_error_K'];summary=[]
    def mapped(k,x,ratios,positive=False):
        lo,hi=sorted(ratios);L=[-math.log(hi),-math.log(lo)]
        if positive:L=[max(0,L[0]),L[1]]
        for i,l in enumerate(L):
            close(k+' L',x['L'][i],l)
            for n,key in ((4,'F_E'),(3,'F_N')):close(k+key,x[key][i],1-math.exp(-n*l))
    for o,r in zip(a['observations'],p['observations']):
        ck('row identity',o==r['observation']);A=1+o['z'];tl,th=o['T_interval_K']
        fixed=[tl/(T*A),th/(T*A)];rect=[tl/((T+dT)*A),th/((T-dT)*A)]
        for key,ratios,pos in [('fixed_T0',fixed,False),('T0_error_rectangle',rect,False),('nonnegative_net_source_fixed_T0',fixed,True),('nonnegative_net_source_rectangle',rect,True)]:mapped(o['id']+key,r[key],ratios,pos)
        close('zero source',r['zero_source_temperature_K'],T*A)
        close('half energy normalized',(r['temperature_if_half_present_energy_added_K']/(T*A))**4,.5)
        close('redshift',r['display_redshift_temperature_difference_K'],T*(o['display_z']-o['z']))
        ck('constant T',r['constant_temperature_inside_quoted_T_interval']==(tl<=T<=th))
        if o['T_central_K'] is None:ck('central null',r['central_L'] is None)
        else:close('central',r['central_L'],-math.log(o['T_central_K']/(T*A)))
        summary.append({'id':o['id'],'rectangle':r['T0_error_rectangle'],'positive_rectangle':r['nonnegative_net_source_rectangle']})
    b=a['constant_beta_summary'];A=1+b['reported_z_range'][1]
    ratios=[A**(-x) for x in b['beta_interval']]
    mapped('beta signed',p['constant_beta']['signed'],ratios)
    mapped('beta positive',p['constant_beta']['nonnegative'],ratios,True)
    ck('shared absorber',a['observations'][0]['shared_object_group']==a['observations'][1]['shared_object_group'])
    print(json.dumps({'schema':'CMB_TZ_SAVED_AUDIT_V001','status':'PASS' if not fail else 'FAIL','checks':count,'failures':fail,'maximum_absolute_difference':maximum,'result_sha256':sha(rb),'freeze_sha256':sha(fb),'payload_sha256':j['payload_sha256'],'audit_sha256':sha(Path(__file__).read_bytes()),'observations':summary,'constant_beta':p['constant_beta'],'scope':'Saved arithmetic only; separate marginal summaries, no likelihood combination, coverage or photon-turnover inference.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
