"""Prospective saved-state early source exchange/readout. Root alone executes.
No producer import, background root, atomic call, trajectory or quadrature solve.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import sys
import time

BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_EARLY_EVOLVED_SOURCE_CONSERVATION_V003'
PARENT='CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004'
PROTOCOL_SHA='110711e4f95616a11f6ff1b27b38c4636ff89fe0d73ea0be8ea5507624540fc6'
PINS={
 'constrained_u_early_evolved_source_conservation_v002.py':'7cc14c75340d9f29ca5155ec1bf870164d7957be584be0fc7ae20a3b970be126',
 'CONSTRAINED_U_EARLY_EVOLVED_SOURCE_CONSERVATION_V002.md':'5235b399a1b50c3c3f7f33eb61a33cff4069b0198618ded3f68190d2502aefcd',
 'constrained_u_early_evolved_source_conservation_v001.py':'1752b47b97e61c9fa19bc0f2b91cfb4c82ff904bdfebffc9fc520b414e49bfc7',
 'CONSTRAINED_U_EARLY_EVOLVED_SOURCE_CONSERVATION_V001.md':'12c898850d6f8d6803705aba1bc007d8dd33f50ed7ed27aea7042a4a5b98cc87',
 'constrained_u_clock_gradient_early_transfer_v004.py':'a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07',
 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004.md':'8d7f33f6b336488e92ed6b516dd196a66f7ee2929bda5a72e7a258fe34ac9cd5',
 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_ADIABATIC_HIERARCHY_V001.md':'1014e8689d23c35b47c2e47b7e4bed2b2b3f0f329aca061b5df3586c249fc7d2',
 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_RESULT.json':'2df066c32b5140d91e2194166940128e92611d7c1ab5d97ae8846fdc73e565c2',
 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_RECEIPT.json':'b4959fb0e1c07179e34ab6a3de0e8075162f87624d7c9e2a8ecd83b16b1ab564'}
SPECS=[('BASE',4096,32,96,128,1e-7,'HALF',1),('TIME',8192,32,96,128,1e-7,'HALF',1),
 ('MODES',8192,64,96,128,1e-7,'HALF',1),('HIERARCHY',8192,32,128,160,1e-7,'HALF',1),
 ('START',8192,32,96,128,5e-8,'HALF',1),('ATOMIC',8192,32,96,128,1e-7,'DEFAULT',1),
 ('THIN',8192,32,96,128,1e-7,'HALF',2)]
OMEGAS=(.1,1.,10.,100.)
KB,C,CBAR=.02,1.98,.99
ROUND=4096*sys.float_info.epsilon
SEALS={};CREATED={};CHECKS=0;MAX_ROUND_FRACTION=0.;RUN_SOURCE=''

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def require(flag,name):
    global CHECKS
    CHECKS+=1
    if not flag:raise AssertionError(name)
def close(a,b,env,name):
    global MAX_ROUND_FRACTION
    scale=max(abs(a)+abs(b),env,1e-300);error=abs(a-b)
    require(all(math.isfinite(x) for x in (a,b,env)) and error<=ROUND*scale,name)
    MAX_ROUND_FRACTION=max(MAX_ROUND_FRACTION,error/scale)
def seal(p,h):
    p=Path(p).resolve()
    require(p.is_relative_to(BASE.parent.parent.resolve()) or (str(p)=='/usr/bin/clang' and h=='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'),'input path')
    require(sha(p)==h,'input seal '+str(p));SEALS[str(p)]=h
def recheck():
    for p,h in {**SEALS,**CREATED}.items():
        if sha(p)!=h:raise AssertionError('Changed sealed bytes '+p)
    if sha(__file__)!=RUN_SOURCE:raise AssertionError('Changed readout source')
def write(name,obj,raw=False):
    data=obj if raw else (json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    p=BASE/name
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);CREATED[str(p.resolve())]=sha(p);return sha(p)
def state_names(spec):
    ns,lg,ln=spec[2:5]
    return ['Psi','delta_b','Hstar_u_b','delta_gamma','Hstar_u_gamma','delta_nu','Hstar_u_nu','delta_n_clock','Hstar_V_phi']+['F_gamma_'+str(l) for l in range(2,lg+1)]+['G_gamma_'+str(l) for l in range(lg+1)]+['F_nu_'+str(l) for l in range(2,ln+1)]+['z_'+str(i) for i in range(ns)]+['zd_'+str(i) for i in range(ns)]

def authenticate():
    require(all('PENDING' not in h for h in [PROTOCOL_SHA,*PINS.values()]),'final parent pins required')
    for n,h in {**PINS,STEM+'.md':PROTOCOL_SHA}.items():seal(BASE/n,h)
    p=read(BASE/(PARENT+'_RESULT.json'));r=read(BASE/(PARENT+'_RECEIPT.json'));m=p['manifest']
    require(r['lineage']==m and r['source_sha256']==m['source_sha256']==PINS['constrained_u_clock_gradient_early_transfer_v004.py'],'parent source/lineage')
    require(r['result_sha256']==PINS[PARENT+'_RESULT.json'] and p['status']==r['status'],'parent result/status')
    require(m['trials']==[list(s) for s in SPECS] and m['omegas']==list(OMEGAS) and len(m['targets'])==68,'fixed census')
    g=p['numerical_gates'];require(len(g)==527 and all(type(x['passed']) is bool for x in g),'527 unchanged dispositions')
    require(p['all_numerical_gates_passed']==all(x['passed'] for x in g),'parent aggregate')
    require(p['status']==('NEW_EARLY_TRANSFER_ARITHMETIC_PASS' if all(x['passed'] for x in g) else 'NEW_EARLY_TRANSFER_ARITHMETIC_FAILED'),'retain parent failures')
    for path,h in m['inputs'].items():seal(path,h)
    for suf,key in (('_MANIFEST.json','manifest_sha256'),('_REPORT.md','report_sha256'),('_JOURNAL.jsonl','journal_sha256')):seal(BASE/(PARENT+suf),r[key])
    require(read(BASE/(PARENT+'_MANIFEST.json'))==m,'saved manifest equality')
    for path,h in r['checkpoint_seals'].items():seal(path,h)
    require(sum(Path(t).name.startswith(PARENT+'_') for t in r['checkpoint_seals'])==222,'111 current-parent checkpoint pairs; inherited pairs retained')
    events=[json.loads(t) for t in (BASE/(PARENT+'_JOURNAL.jsonl')).read_text().splitlines()]
    expected=[(s[0],n) for s in SPECS for n in range(0,s[1]+1,512)]
    actual=[];owner=None
    for e in events:
        require(e['owner']=='root' and type(e['pid']) is int and e['pid']>0 and e['source_sha256']==m['source_sha256'] and e['manifest_sha256']==r['manifest_sha256'],'root event binding')
        if e['event']=='OWNER_START':owner=e['pid'];continue
        require(e['pid']==owner,'owner epoch')
        if e['event']=='OWNER_COMPLETE':
            require(e==events[-1] and e['result_sha256']==r['result_sha256'] and e['gates']==527 and e['passed']==sum(x['passed'] for x in g) and e['status']==p['status'],'natural closure')
            continue
        require(e['event']=='CHECKPOINT','checkpoint event');actual.append((e['trial'],e['n']))
        pn=PARENT+'_'+e['trial']+'_CP_'+str(e['n']).zfill(6)+'.json';cn=pn[:-5]+'_COMMIT.json';co=read(BASE/cn)
        require(e['payload']==pn and sha(BASE/pn)==e['sha256'] and sha(BASE/cn)==e['commit_sha256'],'checkpoint hashes')
        require(co['payload']==pn and co['sha256']==e['sha256'] and co['n']==e['n'] and co['meta']['lineage']==m,'committed parent')
    require(events[0]['event']=='OWNER_START' and events[-1]['event']=='OWNER_COMPLETE' and actual==expected,'complete ordered natural parent')
    require(len(p['rows'])==7,'seven parent trials')
    for tr,spec in zip(p['rows'],SPECS):
        require(tr['label']==spec[0] and tr['spec']==list(spec) and tr['state_names']==state_names(spec),'trial/axes')
        require([s['x'] for s in tr['snapshots']]==m['targets'] and all(len(s['cases'])==4 for s in tr['snapshots']),'ordered 68 x four snapshots')
        last=read(BASE/(PARENT+'_'+spec[0]+'_CP_'+str(spec[1]).zfill(6)+'.json'))
        require(last['snapshots']==tr['snapshots'] and last['step_errors']==tr['step_errors'] and last['dense_errors']==tr['dense_errors'],'final lossless state custody')
        require(last['state']==[s['state'] for s in tr['snapshots'][-1]['cases']],'final state equality')
    return p

def frame(s,tr,fixed,omega):
    y=s['state'];require(len(y)==len(tr['state_names']),'full-state axes')
    Y=dict(zip(tr['state_names'],y));bg=s['background'];h,b,r,w,c,Q=(bg[k] for k in ('h','b','r','w','cs','Q'))
    hd,cd=bg['h_dt'],bg['cs_dt'];rg,rn=r*fixed['fgamma'],r*(1-fixed['fgamma']);q=.01*299792458/(1000*fixed['Hunit']*s['a'])
    psi,db,ub,dg,ug,dn,un,d,V=(y[i] for i in range(9));nodes,weights=tr['snodes'],tr['weights']
    z=[Y['z_'+str(i)] for i in range(len(weights))];zd=[Y['zd_'+str(i)] for i in range(len(weights))]
    require(len(nodes)==len(weights)==tr['spec'][2] and min(nodes)>0 and min(weights)>0,'all positive modes retained')
    Z=math.fsum(a*t for a,t in zip(weights,z));Zd=math.fsum(a*t for a,t in zip(weights,zd));Ze=math.fsum(a*abs(t) for a,t in zip(weights,z));Zde=math.fsum(a*abs(t) for a,t in zip(weights,zd))
    shear=rg*Y['F_gamma_2']+rn*Y['F_nu_2'];phi=psi-2*shear/q**2
    mom=math.fsum((b*ub,4*rg*ug/3,4*rn*un/3,w*V));psid=mom-h*phi
    L=Q*q;Ld=-h*(1+3*c)*L;Ldd=(h*h*(1+3*c)**2-hd*(1+3*c)-3*h*cd)*L
    v=Z/L;vd=(Zd-Ld*v)/L;Gamma=d+3*h*V;n=vd-c*Gamma;P=.5*KB*q*n+CBAR*Z;sigma=s['sigma'];Bq=1+(fixed['ell_native']*q)**2
    Vd=phi+c*Gamma;dd=3*psid-q*q*V-CBAR*Q*q*sigma/w
    forces=[-3*h*t-omega**2*a*a*(Bq*u-q*n-sigma) for a,u,t in zip(nodes,z,zd)]
    Zdd=math.fsum(a*t for a,t in zip(weights,forces));vdd=(Zdd-2*Ld*vd-Ldd*v)/L
    nd=vdd-cd*Gamma-c*(dd+3*hd*V+3*h*Vd);Pd=.5*KB*q*(nd-h*n)+CBAR*Zd
    sources=dict(baryon=b*(db+3*h*ub),photon=rg*(dg+4*h*ug),neutrino=rn*(dn+4*h*un),phase=w*Gamma,polarization=-q*P,shear=shear)
    Ec,Ep=sources['phase'],sources['polarization'];Ecd=-3*h*(1+c)*w*Gamma+w*(dd+3*hd*V+3*h*Vd);Epd=h*q*P-q*Pd
    exchange=3*w*(b*(ub-V)+4*rg*(ug-V)/3+4*rn*(un-V)/3);rhs=-w*q*q*V+exchange
    balance=math.fsum((Ecd,Epd,3*h*Ec,3*h*Ep,-rhs));Euler=math.fsum((Pd,2*h*P,CBAR*Q*sigma))
    # Operation envelopes precede every canceled mean, field, force and quotient.
    phie=abs(psi)+2*(rg*abs(Y['F_gamma_2'])+rn*abs(Y['F_nu_2']))/q**2
    psie=b*abs(ub)+4*rg*abs(ug)/3+4*rn*abs(un)/3+w*abs(V)+abs(h)*phie
    Ge=abs(d)+3*abs(h*V);Vde=phie+abs(c)*Ge;dde=3*psie+q*q*abs(V)+CBAR*abs(Q*q*sigma)/w
    ve=Ze/L;vde=(Zde+abs(Ld)*ve)/L;ne=vde+abs(c)*Ge;Pe=.5*KB*q*ne+CBAR*Ze
    Zdde=math.fsum(a*(3*abs(h*t)+omega**2*u*u*(abs(Bq*vz)+q*ne+abs(sigma))) for a,u,vz,t in zip(weights,nodes,z,zd))
    vdde=(Zdde+2*abs(Ld)*vde+abs(Ldd)*ve)/L;nde=vdde+abs(cd)*Ge+abs(c)*(dde+3*abs(hd*V)+3*abs(h)*Vde)
    Pde=.5*KB*q*(nde+abs(h)*ne)+CBAR*Zde
    Ecde=3*abs(h*(1+c))*w*Ge+w*(dde+3*abs(hd*V)+3*abs(h)*Vde);Epde=abs(h*q)*Pe+q*Pde
    rhse=w*q*q*abs(V)+3*w*(b*(abs(ub)+abs(V))+4*rg*(abs(ug)+abs(V))/3+4*rn*(abs(un)+abs(V))/3)
    balenv=Ecde+Epde+3*abs(h)*(w*Ge+q*Pe)+rhse+q*(Pde+2*abs(h)*Pe+CBAR*abs(Q*sigma))
    close(balance,-q*Euler,balenv,'off-shell exchange identity')
    for key,value,env in [('n_U',n,ne),('P',P,Pe),('Z',Z,Ze),('Zd',Zd,Zde),('Phi',phi,phie),('pi_U',V-v,abs(V)+ve)]:close(value,s[key],env,'saved '+key)
    envelopes=dict(baryon=b*(abs(db)+3*abs(h*ub)),photon=rg*(abs(dg)+4*abs(h*ug)),neutrino=rn*(abs(dn)+4*abs(h*un)),phase=w*Ge,polarization=q*Pe,shear=rg*abs(Y['F_gamma_2'])+rn*abs(Y['F_nu_2']))
    for key,value in sources.items():close(value,s['signed_sources'][key],envelopes[key],'signed source '+key)
    Eb=sources['baryon'];other=math.fsum(sources[k] for k in ('photon','neutrino','phase','polarization'));normal=math.fsum((q*q*psi,Eb,other))
    nen=q*q*abs(psi)+math.fsum(envelopes[k] for k in ('baryon','photon','neutrino','phase','polarization'))
    force_num=math.fsum((-q*q*phi,-Eb,-other,-2*shear))
    lens_num=math.fsum((-.5*q*q*phi,-.5*q*q*psi,-Eb,-other,-shear))
    close(force_num,-normal,nen+q*q*phie+2*envelopes['shear'],'raw signed force/normal identity')
    close(lens_num,-normal,nen+.5*q*q*(phie+abs(psi))+envelopes['shear'],'raw signed lens/normal identity')
    ratios={};fractions={};refusal='ZERO_SIGNED_BARYON_DENOMINATOR' if Eb==0 else None
    if Eb:
        ratios=dict(force_metric=-.99*q*q*phi/Eb,lens_metric=-.99*q*q*(phi+psi)/(2*Eb),force_source=.99*(1+(other+2*shear)/Eb),lens_source=.99*(1+(other+shear)/Eb))
        fractions={key:value/Eb for key,value in sources.items() if key!='baryon'}
        close((ratios['force_metric']-ratios['force_source'])*Eb,-.99*normal,nen+q*q*phie,'signed force/normal identity')
        close((ratios['lens_metric']-ratios['lens_source'])*Eb,-.99*normal,nen+q*q*(phie+abs(psi)),'signed lens/normal identity')
    require(s['source_ratios']['refusal']==refusal,'signed denominator refusal')
    heads=s['domain_heads'];require(type(heads['inside_sampled_linear_domain']) is bool,'sampled domain type')
    return dict(a=s['a'],x=s['x'],signed_sources=sources,source_derivatives=dict(phase=Ecd,polarization=Epd),phase_polarization_exchange=exchange,
        phase_polarization_balance_residual=balance,omitted_normal_Euler_residual=Euler,off_shell_identity_residual=balance+q*Euler,
        operation_envelope=balenv,signed_baryon_denominator=Eb,source_fractions=fractions,source_ratios=ratios,ratio_refusal=refusal,
        signed_comoving_normal_residual=normal,parent_domain_heads=heads,parent_source_ratios=s['source_ratios'],
        scope='Instantaneous saved-state source algebra; derivatives are action vertices, not independently observed time derivatives')

def main():
    global RUN_SOURCE
    RUN_SOURCE=sha(__file__);tick=time.monotonic();p=authenticate();fixed=p['manifest']['fixed'];rows=[];count=0
    for tr in p['rows']:
        snapshots=[]
        for snap in tr['snapshots']:
            cases=[frame(s,tr,fixed,omega) for s,omega in zip(snap['cases'],OMEGAS)];count+=len(cases);snapshots.append(dict(x=snap['x'],cases=cases))
        rows.append(dict(label=tr['label'],spec=tr['spec'],snapshots=snapshots))
    require(count==1904,'7 x 68 x 4 complete source frames');recheck()
    out=dict(status='SAVED_SOURCE_EXCHANGE_ARITHMETIC_PASS',parent_status=p['status'],parent_all_numerical_gates_passed=p['all_numerical_gates_passed'],
        parent_numerical_gates=p['numerical_gates'],parent_comparisons=p['comparisons'],parent_endpoint_source_resolution=p['endpoint_source_resolution'],
        inputs=dict(SEALS),source_sha256=RUN_SOURCE,frame_count=count,checks=CHECKS,rounding_coefficient=ROUND,
        maximum_operation_scaled_error=MAX_ROUND_FRACTION,rows=rows,elapsed_seconds=time.monotonic()-tick,
        units='tau=Hstar_SI*t; density/pressure unit=c_p^2*Hstar_SI^2/(4pi Gbare), Gbare=.99GN; source derivative unit=density_unit*Hstar_SI',
        scope='All original527 dispositions retained; arithmetic source exchange does not qualify failed evolution, tiny source ratios, unsampled domain, halo, data agreement or absent physical formation')
    rh=write(STEM+'_RESULT.json',out)
    lines=['# Evolved early source exchange V003','',out['status'],'Parent: '+p['status'],f'{count} saved frames; {CHECKS} arithmetic/custody controls.','',
        'All seven trials, four inertias and527 parent dispositions remain in JSON. Signed phase, polarization, radiation and shear are retained.',
        'The independently reconstructed exchange residual equals minus q times the omitted-normal Euler residual. No trajectory or background root was evaluated.','',
        '| Trial | omega/Hstar | Eb | phase/Eb | pol/Eb | force/GN | lens/GN | sampled domain |','|---|---:|---:|---:|---:|---:|---:|---|']
    for tr in rows:
        for omega,c in zip(OMEGAS,tr['snapshots'][-1]['cases']):
            r,f=c['source_ratios'],c['source_fractions'];lines.append(f"| {tr['label']} | {omega} | {c['signed_baryon_denominator']} | {f.get('phase')} | {f.get('polarization')} | {r.get('force_source')} | {r.get('lens_source')} | {c['parent_domain_heads']['inside_sampled_linear_domain']} |")
    lines+=['','Ratios retain the signed baryon denominator and refuse exact zero; numerical conditioning is inherited from the parent endpoint-resolution records. These are evolved linear-source readouts, not stationary halo predictions.']
    recheck();mh=write(STEM+'_REPORT.md',('\n'.join(lines)+'\n').encode(),True)
    write(STEM+'_RECEIPT.json',dict(status=out['status'],source_sha256=RUN_SOURCE,input_sha256=dict(SEALS),result_sha256=rh,report_sha256=mh,output_sha256=dict(CREATED)))
    recheck();print(json.dumps(dict(status=out['status'],checks=CHECKS,frame_count=count,result_sha256=rh)),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:raise SystemExit('Root alone executes after final pins/full review')
    if any(BASE.glob(STEM+'_*')):raise SystemExit('Existing readout runtime preserved; no overwrite/retry/error mutation')
    try:main()
    except Exception as exc:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        write(STEM+'_FAILED_'+stamp+'.json',dict(status='SAVED_READOUT_ERROR_PRESERVED',error=repr(exc),source_sha256=sha(__file__),checks=CHECKS))
        raise
