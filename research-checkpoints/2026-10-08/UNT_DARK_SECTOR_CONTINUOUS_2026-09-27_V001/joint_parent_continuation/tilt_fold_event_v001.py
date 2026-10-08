"""On-solution homogeneous fold, unchanged broadened action/preparation.

Restart the last regular saved 1024-step snapshot, NOT a failed RK stage.
Use constitutive s as curve parameter, not a replacement physical clock:
dt/ds=-Q_s Schur/(c N). Original physical Hamilton equations times dt/ds
are regular at the fold. Reconstruct pi_b by H=0; independently monitor
the scalar charge F=0, which is preserved analytically. Stop at Schur=0.
The bracket past the fold is only a mathematical event locator, never a
future physical continuation. No fitted coefficients, changed action,
branch filter, homogeneous initial-seed change or general UNT exclusion.

Freeze 128/256/512 serial steps in s from saved value to -.996, with
bisection of first Schur sign change. Require physical-RHS dictionary
preflight <=1e-8 with floor1, charge residual |F/M|<=1e-9, event relative
Schur <=1e-8, event-state refinement<=1e-7 with floor1, pi_b tangent<=1e-6.
Check positive rest d,A and report N and proper-time curvature. These
are numerical identity gates, not observational or all-state acceptance.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import homogeneous_tilt_saturation_v001 as prior
import homogeneous_tilt_extended_branch_v001 as ext

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'HOMOGENEOUS_TILT_EXTENDED_BRANCH_V001_RESULT.json'
OUT=BASE/'TILT_FOLD_EVENT_V001_RESULT.json'


class Curve:
    def __init__(self,model,piph):
        self.m=model;self.piph=piph;self.piT=6*model.OB

    def physical(self,s,y):
        # y=(ln A,ln B,pi_a,sigma,Z,phase increment,proper-time increment,ln abar)
        al,bl,pia,sig,Z,phase,t,x=y;m=self.m
        V=math.exp(al+2*bl);B2=math.exp(2*bl);c=math.sqrt(1+sig*sig)
        Q,charge,d,K,dm,qr=map(float,m.constitutive(s))
        Qs=m.Q0*m.eps/(2*qr*(1+s)**2)
        p=sig*Q/c;e=(Z-m.C*p)/m.KB
        root=math.sqrt(p*p+m.bs*m.bs);j=m.lam*abs(p)/root
        jt=m.lam*abs(p)*(p*p+2*m.bs*m.bs)/root**3
        J=m.lam*(abs(p)*root-m.bs*m.bs*math.asinh(abs(p)/m.bs))
        Dp=m.C*(e-(1+j)*p);A=m.C*(2/m.KB+jt)
        M=self.piph/(2*V);F=c*charge+sig*Dp-M
        E=V*(m.KB*e*e+m.C*p*p+m.C*J-2*K)+self.piph*Q/c+self.piT
        pib=pia/2+4*V*E/pia;k=(pia-pib)/(4*V);l=-pia/(4*V)
        L=m.KB*e*e+2*m.C*e*p-m.C*p*p-m.C*J+2*K
        S=Q*Dp+charge*p;sdot=e-k*sig;Zdot=S/c-2*l*Z
        Mdot=-(k+2*l)*M
        N=(sig*charge/c+Dp-sig*A*Q/c**3)*sdot+sig*m.C/m.KB*Zdot-Mdot
        schur=c*c*d-sig*sig*A
        h=m.bg(x)[5]
        flow=np.array([k,l,-E+V*L-2*V*Z*e-2*V*sig*S/c,
                       sdot,Zdot,Q/c,1.,h])
        dt_ds=-Qs*schur/(c*N)
        return dict(Q=Q,Qs=Qs,KQ=charge,d=d,A=A,c=c,F=F,M=M,N=N,Schur=schur,
                    E=E,V=V,pib=pib,pib_dot=-2*E+2*V*L,k=k,l=l,
                    flow=flow,dt_ds=dt_ds)

    def rhs(self,s,y):
        g=self.physical(s,y)
        if abs(g['N'])<1 or g['d']<=0 or g['A']<=0:
            raise ValueError('regular parameter assumption failed')
        return g['flow']*g['dt_ds']

    def rk4(self,s,y,ds):
        a=self.rhs(s,y);b=self.rhs(s+ds/2,y+ds*a/2)
        c=self.rhs(s+ds/2,y+ds*b/2);d=self.rhs(s+ds,y+ds*c)
        return y+ds*(a+2*b+2*c+d)/6

    def receipt(self,s,y):
        g=self.physical(s,y)
        # Partial Schur_Q, holding all canonical/geometrical variables fixed.
        dh=1e-7
        sq=(self.physical(s+dh,y)['Schur']-self.physical(s-dh,y)['Schur'])/(2*dh*g['Qs'])
        return dict(s=s,state=y.tolist(),a_reference=math.exp(y[7]),physical_tilt=float(y[3]),
                    Q=g['Q'],KQ=g['KQ'],KQQ=g['d'],longitudinal_coefficient=g['A'],
                    F_relative=g['F']/g['M'],Schur=g['Schur'],Schur_relative=g['Schur']/(g['c']**2*g['d']),
                    N=g['N'],rest_speed_squared=g['A']/g['d'],
                    mean_expansion=(g['k']+2*g['l'])/3,shear=g['k']-g['l'],
                    time_Q_curvature=-sq/(g['c']*g['N']),time_s_derivative=g['dt_ds'],
                    proper_time_increment=float(y[6]))


def main():
    beg=time.monotonic();src=json.loads(SOURCE.read_text());saved=json.loads(prior.base.SOURCE.read_text())
    snap=src['rows'][-1]['snapshots'][-1];z=np.array(snap['state']);x=math.log(snap['a'])
    m=ext.Model(saved);g=m.unpack(x,z);s0=float(g['s'][0]);a=math.exp(x)
    curve=Curve(m,float(g['piph'][0]));h=g['h']
    y0=np.array([x+z[0,0],x+z[1,0],g['pia'][0],g['sig'][0],g['Z'][0],0.,0.,x])
    rhs=m.rhs(x,z)[:,0];fa,fb,un,ph,pa,pb,pu,pc=z[:,0]
    expected=np.array([h*(1+rhs[0]),h*(1+rhs[1]),
        -4*a**3*h*h*(rhs[4]+(3+g['hx'])*(1+pa)),
        h*math.exp(-fa)*(rhs[2]-un*rhs[0]),h*math.exp(-2*fb)*(rhs[6]-2*pu*rhs[1]),
        float(g['q'][0]),1.,h])
    pre=float(np.max(abs(curve.physical(s0,y0)['flow']-expected)/np.maximum(abs(expected),1.)))
    if pre>1e-8:raise ValueError(f'RHS dictionary mismatch {pre}')
    rows=[]
    for steps in (128,256,512):
        y=y0.copy();s=s0;ds=(-.996-s0)/steps;snaps=[];maxF=0.;event=None
        for i in range(steps):
            gi=curve.physical(s,y);maxF=max(maxF,abs(gi['F']/gi['M']))
            if i%(steps//16)==0:snaps.append(curve.receipt(s,y))
            yn=curve.rk4(s,y,ds);gn=curve.physical(s+ds,yn)
            if gn['Schur']<=0:
                lo=0.;hi=1.
                for _ in range(44):
                    mid=(lo+hi)/2;ym=curve.rk4(s,y,ds*mid)
                    if curve.physical(s+ds*mid,ym)['Schur']>0:lo=mid
                    else:hi=mid
                se=s+ds*(lo+hi)/2;ye=curve.rk4(s,y,ds*(lo+hi)/2)
                event=curve.receipt(se,ye);snaps.append(event)
                maxF=max(maxF,abs(event['F_relative']));break
            s+=ds;y=yn
        if event is None:raise ValueError('event not bracketed')
        # Check the eliminated momentum on a regular state along s.
        dscheck=1e-6;flow=curve.rhs(s0,y0);g0=curve.physical(s0,y0)
        fd=(curve.physical(s0+dscheck,y0+dscheck*flow)['pib']-
            curve.physical(s0-dscheck,y0-dscheck*flow)['pib'])/(2*dscheck)
        target=g0['pib_dot']*g0['dt_ds'];tangent=abs(fd-target)/max(abs(target),1e-8)
        rows.append(dict(steps=steps,event=event,snapshots=snaps,maximum_charge_residual=maxF,
                         eliminated_momentum_tangent_error=tangent))
    def compare(r1,r2):
        y1=np.array(r1['event']['state']);y2=np.array(r2['event']['state'])
        return float(max(np.max(abs(y1-y2)/np.maximum(abs(y2),1.)),abs(r1['event']['s']-r2['event']['s'])))
    checks=dict(rhs_dictionary=pre<=1e-8,
                charge_constraint=max(r['maximum_charge_residual'] for r in rows)<=1e-9,
                event_schur=max(abs(r['event']['Schur_relative']) for r in rows)<=1e-8,
                refinement=compare(rows[1],rows[2])<=1e-7,
                eliminated_momentum=max(r['eliminated_momentum_tangent_error'] for r in rows)<=1e-6,
                positive_rest_cone=all(r['event']['KQQ']>0 and r['event']['longitudinal_coefficient']>0 for r in rows))
    deps=['homogeneous_tilt_saturation_v001.py','homogeneous_tilt_extended_branch_v001.py',
          'plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py']
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (SOURCE,prior.base.SOURCE)},
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in deps},
        source_snapshot_a=snap['a'],preflight_rhs_error=pre,rows=rows,
        coarse_refinement=compare(rows[0],rows[1]),fine_refinement=compare(rows[1],rows[2]),
        controls=checks,all_controls_passed=all(checks.values()),elapsed_seconds=time.monotonic()-beg)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('protocol','rows')},indent=2))
    print(json.dumps(rows[-1]['event'],indent=2))
    if not all(checks.values()):raise SystemExit(1)


if __name__=='__main__':main()
