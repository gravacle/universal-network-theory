"""NEW same-action BBN-yield helium constrained-U .99-GN HYREC pair.
Authoring/static review only; root alone launches --execute. No legacy imports.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import math
import os
import subprocess
import time

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent
ATOMIC=BASE/'hyrec_inputs_v001'
STEM='CONSTRAINED_U_CLOCK_GRADIENT_BBN_HELIUM_RECOMBINATION_PAIR_V001'
PROTOCOL_SHA='738a2a0301ab6227d5e430ec41f4251f60f6b24fe7ae5267de1e5e99034b3de8'
PINS={'constrained_u_clock_gradient_flrw_reduced_chart_v002.py': '6d9878bb854bc7147aefcdcd358c6cecd16087a9577960f10686f5c4d17094b9', 'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_REDUCED_CHART_V002.md': '5d644d9d07d6d2dbf4f44a20e329e30965ef0c558a052359bda102dc0b5aba1b', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json': 'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f', 'invariant_clock_acoustic_v001.py': '9cd21314b29d11cedba04eb6e53799aa7847d40c1280718913d2a392bb3db396', 'hyrec_standard_oracle_v001.py': '2b176013f136aafd9495e448c882d1b6860769004be1027c90b5f094880be269', 'NETWORK_THERMAL_ASSUMPTIONS_AND_OBSERVABLES_V001.md': 'b2158042a2ce0867f5984e72cdea06b536975e1817fa48a9198272c0d394fffc', 'hyrec_inputs_v001/HYREC_LOCAL_BUILD_V001.json': 'b92abea8bc12c963f531976fadecb751402c26625d49b9b8da7bc81d8ebcd63d', 'hyrec_inputs_v001/build_bin_v001/HYREC_LOCAL_BUILD_V001_FROZEN.json': '1e9689c9519e7517bbab34cf61d04f599bafd5ed9fb474703f47188c164f22a0', 'hyrec_inputs_v001/HYREC_SOURCE_RECEIPT_V001.json': 'd569777d0103c2db74d4af7e1841738a3bb8fc662efa4c7933ea190f2ad4a400', 'INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_DEFAULT_INPUT.txt': 'c0220b397f81d2bb39ffa337a9a6e7d571d6a992a83cbf046e0795c8920e744c', 'INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_DEFAULT_OUTPUT.json': '782bf0351bc99e1d72f9cbf215cec95ae99dd0f571d47574d160300208461274', 'INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_HALF_INPUT.txt': '4655b5424f2409fc75d693c8e28e65843b63671a4505f98d5d92a2383efeda59', 'INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_HALF_OUTPUT.json': 'f1e9312dc9f1f696a7e65d06f345da9daad814e0076456f9986665f51bb997c1', 'constrained_u_clock_gradient_recombination_pair_v001.py': '41d62be6e215c956864035361d65d529eaa02689b557a2ec11536433a1caf42a', 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V001.md': '85d51b922c6ed9b3a84e67c3d9b35d3a77d9efafe34e320276ead5697dfd2088', 'constrained_u_clock_gradient_recombination_pair_v002.py': '3cf9dbb9c68a1a1495e255de68cc399a2c2242a4edaa1acfc8bb870dd1cb29f4', 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002.md': '09c2ee0071903b262c702cd8c91e1a9050d99f813c0a085ca042d630a537b54e', 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RESULT.json': '008d86b296fc7c5856b5827b4cb3c0a7646e4cbe526cc0d7cd9013f02fbfeed4', 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RECEIPT.json': '1f210c196856d56294c13c35d7630e88f986015892df4f2856b5d2ce95dedcb4', 'constrained_u_clock_gradient_bbn_pair_v001.py': '58ace9542a18cf63a89fe446b4ea40fb834ff6961ceb91185c71ff4732e8a8d5', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001.md': 'f4315e97ef6d4a2585c5f6402a5aed9fa4ba9ad193877567498ed1d099a8c5ff', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RESULT.json': '64e55eefc0079b75994dc749f5e8853835cd3bc72a2566e9627f8b98851fdc36', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_RECEIPT.json': 'e7a9cc7d8f3b59e3b9351a7a3253d5ad4e806a49340908b067600d71783d6685', 'CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001_REFINED_STDOUT.txt': 'd0ec0ef40b5202420b1f064bb42b5101eb6008936cfafe8ab69b2862ca44d225'}
BACKGROUND_SPAN_SHA='eb224e42c6c567b0339b18cdf54a1d8c4f005810b6d6952fee9efee4983b7ec2'
MPC=3.0856775814913673e22
SCALE=math.sqrt(.99/.98)
ARMS=('DEFAULT','HALF')
SEALS={}
CREATED={}


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def bounded(path):
    p=Path(path).resolve()
    if not p.is_relative_to(ROOT.resolve()):raise ValueError('Path escapes project')
    return p

def seal(path,expected):
    p=bounded(path)
    if sha(p)!=expected:raise AssertionError('Changed input '+str(p))
    if str(p) in SEALS and SEALS[str(p)]!=expected:raise AssertionError('Conflicting seal')
    SEALS[str(p)]=expected

def recheck(source_sha):
    for p,h in dict(SEALS,**CREATED).items():
        if sha(p)!=h:raise AssertionError('Changed sealed file '+p)
    if sha(__file__)!=source_sha:raise AssertionError('Changed source')

def write(name,value,raw=False):
    p=BASE/name
    data=value if raw else (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);h=sha(p);CREATED[str(p.resolve())]=h
    return h

def journal(event,**data):
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:
        f.write(json.dumps(dict(time=now(),event=event,**data),sort_keys=True)+'\n')


def background(x, fixed):
    a = math.exp(x)
    eps, d0, OA, OB, OR, rG = (fixed[k] for k in ('eps', 'd0', 'OA', 'OB', 'OR', 'rG'))
    norm = 1/eps-math.log1p(1/eps)
    d = d0/a**3
    target = .5*eps*norm*d
    s = target
    for _ in range(5):
        qbar = math.sqrt(1+eps*s/(1+s))
        dq = eps/(2*qbar*(1+s)**2)
        s -= (s*qbar-target)/(qbar+s*dq)
    qbar = math.sqrt(1+eps*s/(1+s))
    dq = eps/(2*qbar*(1+s)**2)
    pex = (math.log1p(s)-s/(1+s))/norm
    cs = eps*s/(2+(4+3*eps)*s+2*(1+eps)*s*s)
    b, r = 1.5*OB/rG/a**3, 1.5*OR/rG/a**4
    w = 1.5*OA/rG*qbar*d
    rho = 1.5*OA/rG*(1+qbar*d-pex)
    h = math.sqrt((2/3)*(b+r+rho))
    den=2+(4+3*eps)*s+2*(1+eps)*s*s
    ds_dt=-3*h*s/(1+s*dq/qbar)
    cs_dt=eps*(2-2*(1+eps)*s*s)*ds_dt/(den*den)
    Q=fixed['Q0_over_Hstar']*qbar
    return dict(a=a, h=h, b=b, r=r, w=w, rho=rho, cs=cs, qbar=qbar,
                h_dt=-b-4*r/3-w, cs_dt=cs_dt, Q=Q,
                s=s, charge=d, charge_error=abs(2*qbar*s/(eps*norm)/d-1))


def authenticate_bbn():
    b='CONSTRAINED_U_CLOCK_GRADIENT_BBN_PAIR_V001'
    result=json.loads((BASE/(b+'_RESULT.json')).read_text());receipt=json.loads((BASE/(b+'_RECEIPT.json')).read_text())
    raw=json.loads((BASE/(b+'_REFINED_STDOUT.txt')).read_text())
    if (result['status']!=receipt['status'] or result['status']!='FIXED_NEVO_NEW_ACTION_NUMERICALLY_QUALIFIED'
        or len(result['numerical_gates'])!=39 or not all(g['passed'] for g in result['numerical_gates'])
        or receipt['result_sha256']!=PINS[b+'_RESULT.json'] or receipt['source_sha256']!=PINS['constrained_u_clock_gradient_bbn_pair_v001.py']
        or result['lineage']['source_sha256']!=receipt['source_sha256'] or result['lineage']['inputs']!=receipt['inputs']
        or raw['final']!=result['finals']['REFINED']['final'] or raw['profile']!='refined' or raw['status']!='COMPLETE_FIXED_NEVO_SCREEN'):
        raise AssertionError('Accepted same-action BBN parent')
    for p,h in receipt['inputs'].items():
        if Path(p).resolve()==Path('/usr/bin/clang').resolve():
            if sha(p)!=h:raise AssertionError('Inherited compiler seal')
            SEALS[str(Path(p).resolve())]=h
        else:seal(p,h)
    for p,h in receipt['output_sha256'].items():seal(p,h)
    seal(BASE/(b+'_MANIFEST.json'),receipt['manifest_sha256']);seal(BASE/(b+'_JOURNAL.jsonl'),receipt['journal_sha256'])
    events=[json.loads(x) for x in (BASE/(b+'_JOURNAL.jsonl')).read_text().splitlines()]
    if ([e['event'] for e in events]!=['OWNER_START']+['CHECKPOINT']*3+['OWNER_COMPLETE']
        or events[0]['owner']!='root' or events[0]['source_sha256']!=receipt['source_sha256']
        or [e['stage'] for e in events[1:4]]!=['BUILD','DEFAULT','REFINED']):raise AssertionError('BBN natural source closure')
    for stage,event,cp in zip(('BUILD','DEFAULT','REFINED'),events[1:4],result['stages']):
        pn=b+'_'+stage+'_CP.json';cn=b+'_'+stage+'_CP_COMMIT.json';co=json.loads((BASE/cn).read_text())
        if (co!=dict(stage=stage,lineage=result['lineage'],payload=pn,sha256=sha(BASE/pn))
            or event['commit_sha256']!=sha(BASE/cn) or json.loads((BASE/pn).read_text())!=cp):raise AssertionError('BBN committed arm')
    value=raw['final']['YPCMB']
    if value!=.24445561896834236 or not 0<value<1:raise AssertionError('Frozen refined helium yield')
    return value


def authenticate():
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
    parent=(BASE/'constrained_u_clock_gradient_flrw_reduced_chart_v002.py').read_text()
    node=next(n for n in ast.parse(parent).body if isinstance(n,ast.FunctionDef) and n.name=='background')
    if hashlib.sha256(ast.get_source_segment(parent,node).encode()).hexdigest()!=BACKGROUND_SPAN_SHA:
        raise AssertionError('Background span changed')
    own=Path(__file__).read_text()
    own_node=next(n for n in ast.parse(own).body if isinstance(n,ast.FunctionDef) and n.name=='background')
    if ast.get_source_segment(own,own_node)!=ast.get_source_segment(parent,node):raise AssertionError('Background copy differs')
    cal=json.loads((BASE/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json').read_text())
    for p,h in cal['hashes'].items():seal(p,h)
    receipt=json.loads((ATOMIC/'HYREC_LOCAL_BUILD_V001.json').read_text())
    freeze=ATOMIC/receipt['freeze']['path'];seal(freeze,receipt['freeze']['sha256'])
    for n,h in json.loads(freeze.read_text())['files'].items():seal(ROOT/n,h)
    upstream=json.loads((ATOMIC/'HYREC_SOURCE_RECEIPT_V001.json').read_text())
    for item in upstream['files']:
        p=ATOMIC/'upstream'/item['name'];seal(p,item['sha256'])
        if p.stat().st_size!=item['bytes']:raise AssertionError('Upstream length')
    for b in ('default','half'):seal(ATOMIC/receipt['binaries'][b]['path'],receipt['binaries'][b]['sha256'])
    selected,old=cal['selected'],cal['fixed'];ctx=cal['trials'][-1]['atomic_invocation']['context']
    if (old['rG']!=.98 or old['KB']!=.02 or old['Q0_over_H0']!=100. or ctx['background']!='KX'
        or ctx['fixed']['H0_km_s_Mpc']!=selected['Hunit'] or ctx['fixed']['omega_b_cos']!=selected['OB']
        or ctx['physical_omega_b']!=selected['physical_omega_b'] or ctx['YHe']!=selected['YHe']
        or ctx['Neff']!=selected['Neff'] or selected['Hunit']!=old['H0_km_s_Mpc']):
        raise AssertionError('Selected inventory identity')
    fixed=dict(Hunit=selected['Hunit'],OA=old['omega_A'],OB=selected['OB'],OR=ctx['OR'],
               d0=old['d0'],eps=old['eps'],rG=.98/.99,Q0_over_Hstar=old['Q0_over_H0'])
    ordinary=dict(omega_b=selected['physical_omega_b'],T0=ctx['T0'],YHe=authenticate_bbn(),
                  Neff=selected['Neff'],Hstar=selected['Hunit'],YHe_old_fixture=selected['YHe'],
                  helium_source='Accepted same-action BBN refined YPCMB; no fit')
    return receipt,fixed,ordinary


def packet(arm,fixed,ordinary,source_sha):
    oldname='INVARIANT_CLOCK_ACOUSTIC_V001_JOINT3_FINAL_CANDIDATE_'+arm+'_INPUT.txt'
    lines=(BASE/oldname).read_text().splitlines();head=lines[0].split();pars=lines[1].split()
    count=105859 if arm=='DEFAULT' else 211717
    expected=[ordinary[k] for k in ('omega_b','T0','YHe','Hstar')]
    old_expected=[ordinary[k] for k in ('omega_b','T0','YHe_old_fixture','Hstar')]
    if (len(head)!=3 or head[:2]!=['UNT_HYREC_EXTERNAL_V001','JOINT3_FINAL_CANDIDATE_'+arm]
        or len(pars)!=5 or list(map(float,pars[:4]))!=old_expected or int(pars[4])!=count
        or len(lines)!=count+2):raise AssertionError('Old native packet identity')
    pairs=[tuple(map(float,line.split())) for line in lines[2:]]
    if any(len(p)!=2 or not all(math.isfinite(t) for t in p) or p[1]<=0
           or abs(p[0]-i*8000/count)>2e-12*max(1,p[0]) for i,p in enumerate(pairs)):
        raise AssertionError('Old native H-grid')
    zz=[p[0] for p in pairs];hh=[p[1]*SCALE for p in pairs]
    err=max(abs(hh[i]/(fixed['Hunit']*1000/MPC*background(-math.log1p(zz[i]),fixed)['h'])-1)
            for i in [round((count-1)*k/64) for k in range(65)])
    context=dict(action='NEW constrained U/phase gradient, uncompressed',source_sha256=source_sha,
        arm=arm,fixed=fixed,ordinary=ordinary,old_packet_sha256=PINS[oldname],
        H_scale=SCALE,old_Gcos_over_GN=.98,new_bare_G_over_GN=.99,calibration_replayed=False)
    claim=hashlib.sha256(json.dumps(context,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    label='CONSTRAINED_U_BBN_HELIUM_RECOMB_'+arm
    header=['UNT_HYREC_EXTERNAL_V001 '+label+' '+claim,
            ' '.join(format(t,'.17g') for t in expected)+' '+str(count)]
    header.extend(format(z,'.17g')+' '+format(h,'.17g') for z,h in zip(zz,hh))
    return ('\n'.join(header)+'\n').encode(),context,claim,label,zz,hh,err


def output_controls(data,arm,ordinary,claim,label,zz,hh,background_error):
    count=len(zz);step=1. if arm=='DEFAULT' else .5;expected_n=8001 if arm=='DEFAULT' else 16001
    if (data['status']!='COMPLETE_ATOMIC_HISTORY_ONLY' or data['mode']!='external'
        or data['case_id']!=label or data['input_sha256_claimed_by_caller']!=claim
        or data['MODEL']!=3 or data['native_Nz']!=count or not data['zero_injection']
        or data['dlna']!=(8.49e-5 if arm=='DEFAULT' else 4.245e-5)
        or data['columns']!=['z','xe_per_H','Tm_K','external_grid_H_s_inverse_or_null']
        or data['output_count']!=expected_n or len(data['rows'])!=expected_n
        or data['H_grid_dz']!=8000/count or data['H_grid_last_z']!=zz[-1]
        or not 0<=data['first_H_query_z']<=zz[-1]):raise AssertionError('New atomic output schema')
    for key,value in [('omega_b',ordinary['omega_b']),('T0_K',ordinary['T0']),
                      ('YHe_atomic',ordinary['YHe']),('Hcal_km_s_Mpc',ordinary['Hstar'])]:
        if data[key]!=value:raise AssertionError('Atomic parameter '+key)
    bounds=[];temps=[];herror=[]
    dx=8000/count
    for i,row in enumerate(data['rows']):
        if len(row)!=4 or row[0]!=i*step or not all(math.isfinite(x) for x in row[:3]):raise AssertionError('Atomic row census')
        z,xe,tm,Hout=row
        if xe<0 or tm<=0:raise AssertionError('Negative thermal output')
        bounds.append(max(0.,xe-(1+2*data['fHe'])))
        temps.append(max(0.,tm/(ordinary['T0']*(1+z))-1))
        if z>zz[-1]:
            if i!=expected_n-1 or Hout is not None:raise AssertionError('Unexpected H-null')
        else:
            if Hout is None or not math.isfinite(Hout) or Hout<=0:raise AssertionError('Missing H')
            ix=max(1,min(count-3,math.floor(z/dx)));nodes=[(ix-1+k)*dx for k in range(4)]
            val=0.
            for k in range(4):
                weight=math.prod((z-nodes[l])/(nodes[k]-nodes[l]) for l in range(4) if l!=k)
                val+=hh[ix-1+k]*weight
            herror.append(abs(Hout/val-1))
    nH=11.223846333047e-6*ordinary['omega_b']*(1-ordinary['YHe'])
    fHe=ordinary['YHe']/(1-ordinary['YHe'])/3.97153
    if data['fHe']!=fHe:raise AssertionError('Helium normalization')
    return [dict(name=arm+'_'+n,error=e,tolerance=t,passed=math.isfinite(e) and e<=t) for n,e,t in
            [('H_background_65',background_error,1e-10),('output_H_cubic',max(herror),5e-13),
             ('xe_bound',max(bounds),1e-8),('Tm_bound',max(temps),1e-8),('nH0',abs(data['nH0_cm3']/nH-1),1e-14)]]


def main():
    tick=time.monotonic();receipt,fixed,ordinary=authenticate();source_sha=sha(__file__)
    for suffix in ('_RESULT.json','_REPORT.md','_RECEIPT.json'):
        if (BASE/(STEM+suffix)).exists():raise FileExistsError('Completed artifact exists')
    lineage=dict(source_sha256=source_sha,input_sha256=dict(SEALS),fixed=fixed,ordinary=ordinary,arms=list(ARMS))
    mp=BASE/(STEM+'_MANIFEST.json')
    if mp.exists():
        if json.loads(mp.read_text())!=lineage:raise AssertionError('Resume lineage mismatch')
        CREATED[str(mp.resolve())]=sha(mp)
    else:write(mp.name,lineage)
    jp=BASE/(STEM+'_JOURNAL.jsonl');events=[json.loads(x) for x in jp.read_text().splitlines()] if jp.exists() else []
    commits=[e for e in events if e['event']=='CHECKPOINT']
    if any(e['event'] not in ('OWNER_START','CHECKPOINT') or e.get('source_sha256')!=source_sha for e in events):raise AssertionError('Journal schema/source')
    if any(e['event']=='OWNER_START' and (e.get('owner')!='root' or not isinstance(e.get('pid'),int) or e['pid']<=0) for e in events):raise AssertionError('Root owner identity')
    if [e['arm'] for e in commits]!=list(ARMS[:len(commits)]) or len(commits)>2:raise AssertionError('Checkpoint order')
    journal('OWNER_START',pid=os.getpid(),owner='root',source_sha256=source_sha)
    outputs=[];invocations=[];gates=[]
    for index,arm in enumerate(ARMS):
        raw,context,claim,label,zz,hh,berr=packet(arm,fixed,ordinary,source_sha)
        names={key:STEM+'_'+arm+'_'+suffix for key,suffix in
               [('input','INPUT.txt'),('output','OUTPUT.json'),('stderr','STDERR.txt'),('cp','CP.json'),('commit','CP_COMMIT.json')]}
        if index<len(commits):
            e=commits[index];cp=json.loads((BASE/names['cp']).read_text());commit=json.loads((BASE/names['commit']).read_text())
            if e['commit_sha256']!=sha(BASE/names['commit']) or commit!=dict(arm=arm,lineage=lineage,
                checkpoint=names['cp'],sha256=sha(BASE/names['cp'])) or set(cp)!={'context','command','elapsed_seconds','files'} or cp['context']!=context
                or set(cp['files'])!={'input','output','stderr'}
                or cp['command']!=[str(ATOMIC/receipt['binaries'][arm.lower()]['path']),str(ATOMIC/'upstream')+'/', 'external']
                or not math.isfinite(cp['elapsed_seconds']) or cp['elapsed_seconds']<0):raise AssertionError('Checkpoint identity')
            for key in ('input','output','stderr'):
                if cp['files'][key]['name']!=names[key] or sha(BASE/names[key])!=cp['files'][key]['sha256']:raise AssertionError('Checkpoint file')
                CREATED[str((BASE/names[key]).resolve())]=cp['files'][key]['sha256']
            if (BASE/names['input']).read_bytes()!=raw or (BASE/names['stderr']).read_bytes():raise AssertionError('Resume input/stderr')
            CREATED[str((BASE/names['cp']).resolve())]=sha(BASE/names['cp']);CREATED[str((BASE/names['commit']).resolve())]=sha(BASE/names['commit'])
        else:
            if any((BASE/n).exists() for n in names.values()):raise FileExistsError('Orphan arm prefix, no overwrite')
            recheck(source_sha);write(names['input'],raw,True)
            binary=ATOMIC/receipt['binaries'][arm.lower()]['path']
            command=[str(binary),str(ATOMIC/'upstream')+'/', 'external'];begin=time.monotonic()
            proc=subprocess.run(command,input=raw,capture_output=True,check=False)
            write(names['output'],proc.stdout,True);write(names['stderr'],proc.stderr,True)
            if proc.returncode or proc.stderr:raise RuntimeError('Atomic failure, raw prefix retained')
            recheck(source_sha)
            cp=dict(context=context,command=command,elapsed_seconds=time.monotonic()-begin,
                files={k:dict(name=names[k],sha256=sha(BASE/names[k])) for k in ('input','output','stderr')})
            write(names['cp'],cp);commitsha=write(names['commit'],dict(arm=arm,lineage=lineage,checkpoint=names['cp'],sha256=sha(BASE/names['cp'])))
            journal('CHECKPOINT',arm=arm,commit_sha256=commitsha,source_sha256=source_sha)
        data=json.loads((BASE/names['output']).read_text())
        gates.extend(output_controls(data,arm,ordinary,claim,label,zz,hh,berr));outputs.append(data);invocations.append(cp)
        print(json.dumps(dict(arm=arm,status='ATOMIC_CHECKPOINT_COMPLETE',output_sha256=sha(BASE/names['output']))),flush=True)
    coarse,fine=outputs[0]['rows'],outputs[1]['rows'][::2]
    if len(coarse)!=len(fine) or any(a[0]!=b[0] for a,b in zip(coarse,fine)):raise AssertionError('Paired z census')
    for key,col in [('xe_refinement',1),('Tm_refinement',2)]:
        err=max(abs(a[col]-b[col])/(max(1e-3,abs(b[col])) if col==1 else abs(b[col])) for a,b in zip(coarse,fine))
        gates.append(dict(name=key,error=err,tolerance=2e-3,passed=math.isfinite(err) and err<=2e-3))
    if len(gates)!=12:raise AssertionError('Frozen twelve-gate census')
    status='NEW_ATOMIC_PAIR_ARITHMETIC_PASS' if all(g['passed'] for g in gates) else 'NEW_ATOMIC_PAIR_ARITHMETIC_FAILED'
    result=dict(status=status,all_numerical_gates_passed=all(g['passed'] for g in gates),lineage=lineage,
        invocations=invocations,numerical_gates=gates,atomic_outputs=[c['files']['output'] for c in invocations],
        elapsed_seconds=time.monotonic()-tick,scope='NEW BBN-yield helium recombination; same-action fixed-NEVO yield parent, no BBN rerun/fit/thermal origin/CMB output')
    recheck(source_sha);rsha=write(STEM+'_RESULT.json',result)
    report='# NEW constrained-U BBN-yield helium recombination pair V001\n\n'+status+'; '+str(sum(g['passed'] for g in gates))+'/12 gates PASS.\n\n'
    report+='Physical density/charge inventory unchanged; accepted same-action refined BBN YPCMB supplies helium; every input H scaled by sqrt(.99/.98); both xe/Tm histories newly computed.\n\n| Gate | Error | Tolerance | PASS |\n|---|---:|---:|---|\n'
    for g in gates:report+=f"| {g['name']} | {g['error']:.12g} | {g['tolerance']} | {g['passed']} |\n"
    report+='\nLossless default/half tables are in the sealed OUTPUT.json files; no new perturbation or observational claim.\n'
    rep=write(STEM+'_REPORT.md',report.encode(),True);recheck(source_sha)
    journal('OWNER_COMPLETE',status=status,result_sha256=rsha,gate_count=12)
    write(STEM+'_RECEIPT.json',dict(status=status,lineage=lineage,result_sha256=rsha,report_sha256=rep,
        manifest_sha256=sha(mp),journal_sha256=sha(jp),output_sha256=dict(CREATED)))
    print(json.dumps(dict(status=status,result_sha256=rsha,elapsed_seconds=result['elapsed_seconds'])),flush=True)
    return 0 if result['all_numerical_gates_passed'] else 3


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true')
    if not parser.parse_args().execute:raise SystemExit('Refusing atomic work without --execute')
    try:raise SystemExit(main())
    except Exception as exc:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        write(STEM+'_FAILED_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(exc),pid=os.getpid(),time=now()))
        raise
