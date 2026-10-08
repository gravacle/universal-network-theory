"""Independent Decimal recombination of saved reference arithmetic; no fit."""
import hashlib
import json
import math
from decimal import Decimal as D, getcontext
from pathlib import Path

getcontext().prec = 48
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent.parent
STEM='PRESSURE_BOUND_REFERENCE_V001'


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dec(x): return D(str(x))
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def lower(e,s4): return ((s4+3*e).sqrt()-s4.sqrt())**2/9
def capacity(w,s4): return 4*s4*w/(1-3*w)**2


def main():
    rp,fp=HERE/(STEM+'_RESULTS.json'),HERE/(STEM+'_FROZEN.json')
    r,f=json.loads(rp.read_text()),json.loads(fp.read_text());v=r['payload']
    assert r['status']=='COMPLETE' and not v['failures']
    assert r['freeze_sha256']==sha(fp)
    assert r['payload_sha256']==hashlib.sha256(canon(v)).hexdigest()
    for name,h in f['files'].items():
        p=(PROJECT/name).resolve();p.relative_to(PROJECT);assert sha(p)==h,name
    assert f['config']==v['config']
    assert len(v['checks'])==len({c['name'] for c in v['checks']})==256
    assert all(c['passed'] and 0<=c['normalized_error']<=v['config']['tolerance'] for c in v['checks'])
    old=json.loads((HERE/'COSMOLOGY_CLOSURE_ARITHMETIC.json').read_text())
    assert len(v['rows'])==18 and sum(len(x['capacities']) for x in v['rows'])==54
    assert len(v['synthetic_controls'])==14
    eps=dec(v['config']['epsilon']);s4=(1-eps**6)/6
    pi=D('3.1415926535897932384626433832795028841971693993751')
    maxima={};count=0

    def check(label,actual,wanted):
        nonlocal count
        wanted=float(wanted);err=abs(actual-wanted)
        relative=err/max(abs(actual),abs(wanted),1e-300)
        assert relative<5e-13 or err==0,(label,actual,wanted,relative)
        maxima[label]=max(maxima.get(label,0.),relative);count+=1

    check('S4',v['S4'],s4)
    output=[]
    for i,(row,previous) in enumerate(zip(v['rows'],old['rows'])):
        assert row['row_index']==i
        for key in ('reference_case','reference_input','bbn'):
            assert row[key]==previous[key],key
        assert row['inherited_reference_r']==previous['reference_r']
        inp=row['reference_input'];h0=dec(inp['H0_km_s_Mpc'])
        hb=h0/dec(v['config']['mpc_km']);gstar=3*pi*dec(inp['a0_m_s2'])/8
        ob=dec(row['bbn']['omega_b'])/(h0/100)**2
        oe=1-dec(inp['Omega_Lambda_ref'])-ob
        factor=3*(1-eps**2)*(dec(v['config']['c_m_s'])*hb/gstar)**2/4
        energy=factor*oe
        check('H0',row['H0_s_inverse'],hb);check('gstar',row['inherited_relaxed_gstar_m_s2'],gstar)
        check('Omega_b',row['baryon_Omega_at_reference_H0'],ob)
        check('Omega_exc',row['required_Omega_excitation'],oe)
        check('factor',row['E_per_unit_Omega'],factor)
        check('E',row['required_dimensionless_energy'],energy)
        assert row['positive_required_energy']==(energy>0)==row['bound_applicable_to_positive_required_energy']
        if energy>0:
            p=lower(energy,s4);w=p/energy
            check('P_floor',row['P_lower_bound'],p);check('w_floor',row['w_lower_bound'],w)
            assert 0<p<energy/3
        else:
            assert row['P_lower_bound'] is None and row['w_lower_bound'] is None
        for c,defined in zip(row['capacities'],v['config']['wmax']):
            assert c['wmax_definition_not_observation']==defined
            ec=capacity(dec(defined),s4);oc=ec/factor
            check('E_capacity',c['E_capacity'],ec);check('Omega_capacity',c['Omega_capacity'],oc)
            if energy>0:check('capacity_ratio',c['positive_required_to_capacity'],energy/ec)
            else:assert c['positive_required_to_capacity'] is None
        output.append(dict(row=i,reference_case=row['reference_case'],bbn=row['bbn']['name'],
                           E=float(energy),Omega_exc=float(oe),w_floor=float(p/energy),
                           capacity_ratios=[c['positive_required_to_capacity'] for c in row['capacities']]))
    for c in v['synthetic_controls']:
        kind=c['kind']
        if kind=='bound_identity':check('synthetic_floor',c['P_floor'],lower(dec(c['E']),s4))
        elif kind=='inverse_capacity':check('synthetic_inverse',c['E_capacity'],capacity(dec(c['w']),s4))
        else:
            weights,gaps,second,fourth=[list(map(dec,c[k])) for k in ('weights','gaps','second_moments','fourth_moments')]
            if kind=='saturated_moments':
                # Recover the declared exact fixture rather than treating its
                # rounded binary moment representations as exact Decimals.
                for got,d in zip(second,gaps):check('synthetic_second_moment',float(got),d*d)
                for got,d in zip(fourth,gaps):check('synthetic_fourth_moment',float(got),d**4)
                second=[d*d for d in gaps];fourth=[d**4 for d in gaps]
            moment=sum(w*d**4 for w,d in zip(weights,gaps))
            v2=sum(w*d*d*x/2 for w,d,x in zip(weights,gaps,second))
            pp=sum(w*x/4 for w,x in zip(weights,fourth));ee=2*v2+3*pp
            for label,wanted in [('S4',moment),('V2',v2),('P',pp),('E',ee)]:check('synthetic_moments_'+label,c[label],wanted)
            assert v2*v2<=moment*pp+D('1e-45') and lower(ee,moment)<=pp+D('1e-45')
    result=dict(status='PASS_INDEPENDENT_SAVED_ARITHMETIC',audit_source_sha256=sha(Path(__file__)),
        result_sha256=sha(rp),freeze_sha256=sha(fp),payload_sha256=r['payload_sha256'],
        authenticated_input_count=len(f['files']),original_checks=256,rows=18,capacities=54,
        independent_arithmetic_checks=count,max_relative_differences=maxima,
        minimum_w_floor=min(x['w_floor'] for x in output),maximum_w_floor=max(x['w_floor'] for x in output),
        reference_rows=output,source_assumptions=old['assumptions'],
        uncertainty_scope='Fixed central-value references; BBN error metadata retained, not propagated.',
        seconds=r['seconds'],peak_self_rss_bytes=r['peak_self_rss_bytes'])
    print(json.dumps(result,sort_keys=True,allow_nan=False))


if __name__=='__main__':main()
