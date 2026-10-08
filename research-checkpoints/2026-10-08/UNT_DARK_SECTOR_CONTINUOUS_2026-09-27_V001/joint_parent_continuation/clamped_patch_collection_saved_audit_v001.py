"""Independent saved comparison arithmetic; explicit four-corner interpolation."""
import base64,bisect,hashlib,json,math,zlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
RESULT=HERE/'CLAMPED_COMMON_PHASE_PATCH_COLLECTION_V001_RESULTS.json'
FREEZE=HERE/'CLAMPED_COMMON_PHASE_PATCH_COLLECTION_V001_FROZEN.json'

def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run():
    wrapper=json.loads(RESULT.read_text());out=wrapper['payload'];freeze=json.loads(FREEZE.read_text())
    assert wrapper['freeze_sha256']==sha(FREEZE)
    assert wrapper['payload_sha256']==hashlib.sha256(encode(out)).hexdigest()
    for name,digest in freeze['files'].items():assert sha(ROOT/name)==digest
    cases=[]
    for i,custody in enumerate(out['custody']):
        p=Path(custody['path']);assert sha(p)==custody['transport_sha256']
        t=json.loads(p.read_text());raw=zlib.decompress(base64.b64decode(t['data']));v=json.loads(raw)
        assert hashlib.sha256(raw).hexdigest()==custody['raw_sha256']==t['raw_sha256']
        assert v['payload_sha256']==hashlib.sha256(encode(v['payload'])).hexdigest()==custody['payload_sha256']
        assert v['payload']['case_index']==i
        cases.append(v['payload'])
    count=0;maxerr=0.;fail=[]
    def check(name,got,wanted):
        nonlocal count,maxerr
        count+=1;err=abs(got-wanted)/max(1.,abs(wanted));maxerr=max(maxerr,err)
        if not math.isfinite(err) or err>2e-11:fail.append(dict(name=name,error=err))
    def fields(case,o):
        f={'u':o['u'],'Phi':[[case['epsilon_scale']*x for x in row] for row in o['u']]}
        for axis in ['radial','vertical']:
            f[axis+'_G']=o['gradients'][axis]
            f[axis+'_m_s2']=[[case['source_row']['gstar']*x for x in row] for row in f[axis+'_G']]
        for name in ['I','I_over_Ib','deltaT_hard','deltaT_soft','deltaT','hard_E','hard_Pi']:f[name]=o['material'][name]
        return f
    def interp(c,f,x,z):
        if not(c[0]<=x<=c[-1] and c[0]<=z<=c[-1]):raise RuntimeError('Extrapolation')
        i=min(bisect.bisect_right(c,x)-1,len(c)-2);j=min(bisect.bisect_right(c,z)-1,len(c)-2)
        s=(x-c[i])/(c[i+1]-c[i]);t=(z-c[j])/(c[j+1]-c[j])
        return (1-s)*((1-t)*f[i][j]+t*f[i][j+1])+s*((1-t)*f[i+1][j]+t*f[i+1][j+1])
    expected=[('grid_N16_to_N32',i,i+1,s,s) for i in [0,2,4,6] for s in [1.,2.]]
    expected += [('clamp_L1_to_L2',i,i+2,s,s) for i in [0,1,4,5] for s in [1.,2.]]
    expected += [('seed1_to_seed2',i,i,1.,2.) for i in range(8)]
    assert len(out['comparisons'])==24
    for index,(row,label) in enumerate(zip(out['comparisons'],expected)):
        assert tuple(row[k] for k in ['kind','first_case','second_case','first_seed','second_seed'])==label
        _,i,j,sa,sb=label;a,b=cases[i],cases[j]
        oa=next(o for o in a['outcomes'] if o['seed_multiplier']==sa);ob=next(o for o in b['outcomes'] if o['seed_multiplier']==sb)
        assert row['both_converged']==(oa['status']==ob['status']=='CONVERGED')
        assert row['both_jacobians_qualified']==(oa['jacobian_qualified'] and ob['jacobian_qualified'])
        ca,cb=a['centres'],b['centres'];edges=a['edges']
        take=[k for k,x in enumerate(ca) if max(ca[0],cb[0])<=x<=min(ca[-1],cb[-1])]
        assert take==row['first_grid_retained_indices']
        assert row['excluded_first_grid_points']==len(ca)**2-len(take)**2
        fa,fb=fields(a,oa),fields(b,ob);assert set(fa)==set(fb)==set(row['metrics'])
        weights=[(edges[k+1]**2-edges[k]**2)/2*(edges[l+1]-edges[l]) for k in take for l in take];total=math.fsum(weights)
        for name in fa:
            av=[fa[name][k][l] for k in take for l in take]
            bv=[interp(cb,fb[name],ca[k],ca[l]) for k in take for l in take]
            delta=[y-x for x,y in zip(av,bv)]
            rms=lambda v:math.sqrt(math.fsum(w*x*x for w,x in zip(weights,v))/total)
            ar,br,dr=rms(av),rms(bv),rms(delta)
            values=dict(weighted_RMS_difference=dr,symmetric_relative_RMS=2*dr/(ar+br) if ar+br else 0.,
                max_absolute_difference=max(map(abs,delta)),first_weighted_RMS=ar,second_weighted_RMS=br,
                signed_range=[min(delta),max(delta)],first_range=[min(av),max(av)],second_range=[min(bv),max(bv)])
            for key,wanted in values.items():
                got=row['metrics'][name][key]
                if isinstance(wanted,list):
                    for k in range(2):check(f'{index}:{name}:{key}:{k}',got[k],wanted[k])
                else:check(f'{index}:{name}:{key}',got,wanted)
    converged=sum(o['status']=='CONVERGED' for p in cases for o in p['outcomes'])
    qualified=sum(o['jacobian_qualified'] for p in cases for o in p['outcomes'])
    assert out['census_complete'] and out['present_cases']==8 and out['missing_cases']==[]
    assert out['all_16_seeds_converged']==(converged==16)
    assert out['all_16_jacobians_qualified']==(qualified==16)
    assert out['numerical_resolution_certified'] is False
    return dict(status='PASS' if not fail else 'FAIL',source_sha256=sha(Path(__file__)),
        collection_sha256=sha(RESULT),collection_freeze_sha256=sha(FREEZE),
        comparison_count=24,metric_checks=count,maximum_scaled_error=maxerr,failures=fail,
        converged_seeds=converged,jacobian_qualified_seeds=qualified,
        scope='Saved-array explicit four-corner remapping and fsum metrics; no producer, constitutive evaluation or field solve.')

if __name__=='__main__':
    p=run();print(encode(dict(payload_sha256=hashlib.sha256(encode(p)).hexdigest(),payload=p)).decode())
