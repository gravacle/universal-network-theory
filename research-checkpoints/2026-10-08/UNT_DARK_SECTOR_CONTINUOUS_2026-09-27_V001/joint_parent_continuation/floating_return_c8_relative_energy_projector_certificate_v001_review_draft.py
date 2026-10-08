#!/usr/bin/env python3
"""Exact saved C8 symmetry/characteristic/root census; root-only execution.
No eigensolver, baseline dynamics, preparation, producer import or RNG replay.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[key]='1'
import sys,json,hashlib,math,time,traceback
from pathlib import Path
from fractions import Fraction as F
import numpy as np
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_RELATIVE_ENERGY_PROJECTOR_CERTIFICATE_V001'
STEM='floating_return_c8_relative_energy_projector_certificate_v001'
CP=J/(STEM+'_checkpoints');RESULT=J/(NAME+'_RESULT.json');MD=J/(NAME+'_RESULT.md');RECEIPT=J/(NAME+'_RECEIPT.json');ERROR=J/(NAME+'_ERROR.json')
PINS={'FLOATING_RETURN_C8_RELATIVE_ENERGY_SPECTRAL_RESPONSE_V001.md': 'b8337f327c8503e505f2099c38bd61550ae005ca369a886fce076b9be802ed6a', 'LOCAL_RECORD_FEEDBACK_OCCUPIED_INCIDENCE_MEMORY_LAW_V001.md': '9239dcce75623cee38dd2ca4df78686b4d75f87d4baa975139549a29f15a0f26', 'FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_RESULT.json': 'd7e4e759b357dd8154567a8a103c433f72236d5b0799123a67b6d40c628baae4', 'FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_RECEIPT.json': '7896e0b78db294fe3b66886449d088afee4a6a413ee27056d09b6dde5ed05669', 'FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_AUDIT.json': 'bd324e35eaf8bafa7b8686d49f6d1e4add0ad48c8deb6189d21ed2177f5687d7', 'FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_AUDIT.md': '21c242bf4ed545facdc63dc574a26bb06efd594a5e66cc2bf33dae08708af750', 'floating_return_c8_tagged_probe_reaction_v001_checkpoints/reaction_eigensystems.npz': '06432406fd969f8ec3c8d93a606207ff5c4bd1ce0deb0281b87e41e190ebcc1a'}
PROTOCOL_SHA='3f89380ea9a8b042bcfa71e73460a455a50c067cb9e1f1da910d111eac3f17f3'
CYCLE=(0,4,3,7,2,6,1,5);EDGES=tuple(zip(CYCLE,CYCLE[1:]+CYCLE[:1]))
REFLECTION={CYCLE[k]:CYCLE[(1-k)%8] for k in range(8)}
BOUND=512;WIDTH=F(1,2**36);DEPTH=128;SPLIT_BUDGET=262144;TOL=5e-10
CHECKS=[];INPUTS={};COMMITS={};STARTED=False;ACTIVE={};SPLITS=0

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(name,ok):
    CHECKS.append({'name':name,'passed':bool(ok)})
    if not ok:raise AssertionError(name)
def write(p,x):
    with Path(p).open('xb') as f:f.write(canon(x)+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)
def event(x):
    with (CP/'journal.jsonl').open('ab') as f:f.write(canon(x)+b'\n');f.flush();os.fsync(f.fileno())
def commit(p,x):
    h=write(p,x);COMMITS[p.name]=h;event({'event':'stage_saved','file':p.name,'sha256':h});return h

def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def primitive(a,positive=True):
    a=trim(a)
    if a==[0]:return a
    g=0
    for x in a:g=math.gcd(g,abs(x))
    a=[x//g for x in a]
    if positive and a[-1]<0:a=[-x for x in a]
    return a

def multiply(a,b):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for k,y in enumerate(b):r[i+k]+=x*y
    return trim(r)

def deriv(a):return trim([i*a[i] for i in range(1,len(a))] or [0])

def remainder(a,b):
    """Primitive pseudo-remainder, used only for sign-insensitive gcd."""
    r=trim(a);b=trim(b)
    if b==[0]:raise ZeroDivisionError('zero polynomial')
    while r!=[0] and len(r)>=len(b):
        shift=len(r)-len(b);lc=r[-1];scale=b[-1]
        r=[scale*x for x in r]
        for i,x in enumerate(b):r[i+shift]-=lc*x
        r=primitive(r)
    return r

def gcd_poly(a,b):
    a,b=primitive(a),primitive(b)
    while b!=[0]:a,b=b,remainder(a,b)
    return primitive(a)

def divide(a,b):
    """Exact monic integer division, with complete remainder guard."""
    r=trim(a);q=[0]*max(1,len(a)-len(b)+1)
    check('monic exact factor',b[-1]==1)
    while r!=[0] and len(r)>=len(b):
        shift=len(r)-len(b);c=r[-1];q[shift]+=c
        for i,x in enumerate(b):r[i+shift]-=c*x
        r=trim(r)
    check('zero factor remainder',r==[0]);return trim(q)

def signed_remainder(a,b):
    r=[F(x) for x in a];b=[F(x) for x in b]
    while trim(r)!=[0] and len(trim(r))>=len(b):
        r=trim(r);shift=len(r)-len(b);c=r[-1]/b[-1]
        for i,x in enumerate(b):r[i+shift]-=c*x
        r=trim(r)
    den=1
    for x in r:den=math.lcm(den,x.denominator)
    return primitive([-int(x*den) for x in r],positive=False)

def sturm(a):
    seq=[a,deriv(a)]
    while seq[-1]!=[0]:
        r=signed_remainder(seq[-2],seq[-1])
        if r==[0]:break
        seq.append(r)
    check('squarefree Sturm terminal',len(seq[-1])==1 and seq[-1]!=[0]);return seq

def sign_at(p,x):
    n,d=x.numerator,x.denominator;h=p[-1];power=1
    for c in reversed(p[:-1]):power*=d;h=h*n+c*power
    return (h>0)-(h<0)

def variations(seq,x):
    signs=[z for p in seq if (z:=sign_at(p,x))]
    return sum(a!=b for a,b in zip(signs,signs[1:]))

def count(seq,a,b):return variations(seq,a)-variations(seq,b)

def bump(depth):
    global SPLITS
    SPLITS+=1
    check('bounded Sturm depth/splits',depth<=DEPTH and SPLITS<=SPLIT_BUDGET)

def isolate(seq,degree,atom):
    check('all atom roots real/in fixed bounds',count(seq,F(-BOUND),F(BOUND))==degree)
    stack=[(F(-BOUND),F(BOUND),0,degree)];roots=[]
    while stack:
        a,b,depth,n=stack.pop()
        if n==0:continue
        if n==1 and b-a<=WIDTH:roots.append({'atom':atom,'lo':a,'hi':b,'depth':depth});continue
        bump(depth+1);mid=(a+b)/2;left=count(seq,a,mid)
        check('exact Sturm partition',0<=left<=n)
        stack.extend(((mid,b,depth+1,n-left),(a,mid,depth+1,left)))
    check('complete atom isolation census',len(roots)==degree);return roots

def refine(root,seq):
    a,b=root['lo'],root['hi'];mid=(a+b)/2;left=count(seq,a,mid)
    check('one-root refinement',left in (0,1));bump(root['depth']+1)
    root.update(lo=a if left else mid,hi=mid if left else b,depth=root['depth']+1)

def separate(roots,seqs):
    while True:
        roots.sort(key=lambda r:r['lo']);pair=next(((a,b) for a,b in zip(roots,roots[1:]) if a['hi']>b['lo']),None)
        if pair is None:return roots
        for r in pair:refine(r,seqs[r['atom']])

def matmul_left(a,p):
    n=len(a);rows=[[(k,x) for k,x in enumerate(row) if x] for row in a]
    return [[sum(x*p[k][j] for k,x in row) for j in range(n)] for row in rows]

def characteristic(a):
    n=len(a);power=[[int(i==k) for k in range(n)] for i in range(n)];traces=[];coeff=[1]
    for k in range(1,n+1):
        power=matmul_left(a,power);traces.append(sum(power[i][i] for i in range(n)))
        numerator=-sum(coeff[k-j]*traces[j-1] for j in range(1,k+1))
        check('Newton exact divisibility',numerator%k==0);coeff.append(numerator//k)
    h=[[int(i==k) for k in range(n)] for i in range(n)]
    for c in coeff[1:]:
        h=matmul_left(a,h)
        for i in range(n):h[i][i]+=c
    check('exact Cayley Hamilton',not any(x for row in h for x in row))
    return list(reversed(coeff)),traces

def determinant(a,x):
    n=len(a);m=[[x*int(i==j)-a[i][j] for j in range(n)] for i in range(n)];prev=1
    for k in range(n-1):
        pivot=m[k][k];check('nonzero Bareiss leading pivot',pivot!=0)
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=pivot*m[i][j]-m[i][k]*m[k][j];check('exact Bareiss division',v%prev==0);m[i][j]=v//prev
        for i in range(k+1,n):m[i][k]=0
        prev=pivot
    return m[-1][-1]

def expected(two,s):
    labels=[(a,b) for a in range(8) for b in range(8) if a!=b] if two else [(v,) for v in range(8)]
    d=len(labels);index={p:i for i,p in enumerate(labels)};a=[[0]*(2*d) for _ in range(2*d)]
    for bit in (0,1):
        for i,p in enumerate(labels):
            col=bit*d+i;a[col][col]=20*(8+len(p))+(40+10*s if bit==0 else 0);a[(1-bit)*d+i][col]=-4
            for ei,(u,v) in enumerate(EDGES):
                if ei==0 and bit==0:continue
                a[col][col]+=5*int((u in p)!=(v in p))
                for species,site in enumerate(p):
                    target=v if site==u else u if site==v else None
                    if target is None or target in p:continue
                    q=list(p);q[species]=target;a[bit*d+index[tuple(q)]][col]-=2
    return a,labels

def symmetry_blocks(a,labels,two):
    n=len(a);d=len(labels);idx={p:i for i,p in enumerate(labels)}
    rr=[bit*d+idx[tuple(REFLECTION[v] for v in p)] for bit in (0,1) for p in labels]
    ss=[bit*d+idx[tuple(reversed(p))] for bit in (0,1) for p in labels] if two else list(range(n))
    check('complete symmetric integer action',all(a[i][j]==a[j][i] for i in range(n) for j in range(n)))
    for perm in (rr,ss):check('exact involution/action symmetry',all(perm[perm[i]]==i for i in range(n)) and all(a[perm[i]][perm[j]]==a[i][j] for i in range(n) for j in range(n)))
    check('commuting exact symmetries',all(rr[ss[i]]==ss[rr[i]] for i in range(n)))
    chars=((1,1),(1,-1),(-1,1),(-1,-1)) if two else ((1,1),(1,-1))
    answer=[];resolution=[[F(0) for _ in range(n)] for _ in range(n)]
    for sc,rc in chars:
        unseen=set(range(n));basis=[]
        while unseen:
            i=min(unseen);g=((i,1),(rr[i],rc),(ss[i],sc),(rr[ss[i]],sc*rc)) if two else ((i,1),(rr[i],rc))
            orbit={z for z,c in g};unseen-=orbit;values={z:sum(c for y,c in g if y==z) for z in orbit}
            if not any(values.values()):continue
            scale=values[i];check('nonzero orbit representative',scale!=0)
            check('integer signed orbit basis',all(v in (-abs(scale),abs(scale)) for v in values.values()))
            basis.append({z:v//scale for z,v in values.items()})
        dims=[len(w) for w in basis];m=len(basis);k=[[0]*m for _ in range(m)]
        for j,w in enumerate(basis):
            aw=[sum(a[i][l]*c for l,c in w.items()) for i in range(n)]
            for i,u in enumerate(basis):
                numerator=sum(c*aw[l] for l,c in u.items());check('integer similar block',numerator%dims[i]==0);k[i][j]=numerator//dims[i]
            check('complete exact intertwiner',all(aw[l]==sum(u.get(l,0)*k[i][j] for i,u in enumerate(basis)) for l in range(n)))
        check('positive Gram self adjoint',all(dims[i]*k[i][j]==dims[j]*k[j][i] for i in range(m) for j in range(m)))
        for w,gram in zip(basis,dims):
            for i,c in w.items():
                for j,e in w.items():resolution[i][j]+=F(c*e,gram)
        answer.append((sc,rc,k,dims,basis))
    check('complete symmetry resolution',all(resolution[i][j]==int(i==j) for i in range(n) for j in range(n)))
    check('fixed symmetry block dimensions',[len(x[2]) for x in answer]==([32,24,24,32] if two else [8,8]));return answer

def atoms_from(polys):
    atoms=[]
    for p in polys:
        f=divide(p,gcd_poly(p,deriv(p)));old=atoms;atoms=[]
        for a in old:
            g=gcd_poly(a,f)
            if g==[1]:atoms.append(a);continue
            q=divide(a,g)
            if q!=[1]:atoms.append(q)
            atoms.append(g);f=divide(f,g)
        if f!=[1]:atoms.append(f)
    atoms.sort(key=lambda p:(len(p),tuple(p)))
    check('pairwise coprime spectral atoms',all(gcd_poly(a,b)==[1] for i,a in enumerate(atoms) for b in atoms[i+1:]));return atoms

def main():
    global STARTED
    if sys.argv[1:]!=['--execute']:raise SystemExit('Requires exact root --execute.')
    if any(p.exists() for p in (CP,RESULT,MD,RECEIPT,ERROR)):raise SystemExit('Exclusive reserved path exists.')
    for f,h in {**PINS,NAME+'.md':PROTOCOL_SHA}.items():
        check('input byte seal '+f,sha(J/f)==h);INPUTS[str((J/f).relative_to(ROOT))]=h
    INPUTS[str(Path(__file__).resolve())]=sha(__file__)
    parent='FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001';p=read(J/(parent+'_RESULT.json'));r=read(J/(parent+'_RECEIPT.json'));audit=read(J/(parent+'_AUDIT.json'))
    check('accepted parent result/receipt',r['result_raw_sha256']==sha(J/(parent+'_RESULT.json')) and r['result_canonical_sha256']==hashlib.sha256(canon(p)).hexdigest() and p['failed']==r['failed']==0 and all(x['passed'] for x in p['checks']) and p['input_sha256']==r['input_sha256'])
    check('accepted saved audit identity',audit['audit_status']=='PASS' and audit['failed_assertions']==0 and audit['result_raw_sha256']==r['result_raw_sha256'] and audit['receipt_sha256']==sha(J/(parent+'_RECEIPT.json')))
    data=J/'floating_return_c8_tagged_probe_reaction_v001_checkpoints/reaction_eigensystems.npz'
    check('receipt-owned eigenbasis checkpoint',r['checkpoint_sha256'][data.name]==sha(data))
    CP.mkdir();STARTED=True;started=time.monotonic();mh=write(CP/'manifest.json',{'PID':os.getpid(),'input_sha256':INPUTS,'parameters':{'M20_scale':20,'bound':BOUND,'width_M20':str(WIDTH),'depth':DEPTH,'split_budget':SPLIT_BUDGET,'native_action_tolerance':TOL,'new_eigensolver_calls':0,'census':'12tagged+6reference blocks;6loading rows;384saved modes'}});COMMITS['manifest.json']=mh;event({'event':'started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':INPUTS})
    with np.load(data,allow_pickle=False) as z:
        check('true frozen cycle',z['cycle_global_nodes'].tolist()==list(CYCLE));check('global tagged pair map',z['ordered_tagged_pairs'].tolist()==[[a,b] for a in range(8) for b in range(8) if a!=b]);check('global full q words',z['global_record_bits'].tolist()==[[(q>>v)&1 for q in range(256)] for v in range(8)])
        saved={key:z[key].copy() for key in ('tagged_base_matrices','reference_base_matrices','tagged_base_eigenvalues','reference_base_eigenvalues')}
    summaries=[];allblocks=[]
    for sector,two in (('tagged',True),('reference',False)):
        records=[]
        for s in range(3):
            ACTIVE.update(sector=sector,loading=s,stage='exact_small_symmetry_characteristic')
            a,labels=expected(two,s);err=float(np.max(abs(np.asarray(a,dtype=float)/20-saved[sector+'_base_matrices'][s])))
            check('frozen integer action matches native saved block',math.isfinite(err) and err<=TOL);check('fixed full operator row bound',max(sum(abs(x) for x in row) for row in a)<BOUND)
            for sc,rc,k,dims,basis in symmetry_blocks(a,labels,two):
                poly,traces=characteristic(k);detcontrols=[]
                for x in (-1,0,1):
                    value=sum(c*x**i for i,c in enumerate(poly));det=determinant(k,x);check('independent exact determinant polynomial',value==det);detcontrols.append({'x':x,'polynomial':value,'Bareiss_determinant':det})
                record={'sector':sector,'s':s,'S_character':sc,'R_character':rc,'dimension':len(k),'integer_similar_block':k,'Gram_diagonal':dims,'signed_orbit_basis':basis,'characteristic_ascending':poly,'power_traces':traces,'determinant_controls':detcontrols,'native_saved_action_error':err}
                commit(CP/('%s_s%d_S%+d_R%+d.json'%(sector,s,sc,rc)),record);records.append(record);allblocks.append(record)
        ACTIVE.update(sector=sector,stage='exact_atoms_Sturm_order')
        atoms=atoms_from([x['characteristic_ascending'] for x in records]);seqs=[sturm(a) for a in atoms];roots=[]
        for i,(a,seq) in enumerate(zip(atoms,seqs)):roots+=isolate(seq,len(a)-1,i)
        roots=separate(roots,seqs)
        multiplicities=[]
        for record in records:
            f=record['characteristic_ascending'];ms=[]
            for atom in atoms:
                m=0
                while gcd_poly(f,atom)==atom:f=divide(f,atom);m+=1
                ms.append(m)
            check('complete component reconstruction',f==[1] and sum(m*(len(a)-1) for m,a in zip(ms,atoms))==record['dimension']);multiplicities.append(ms)
        root_rows=[]
        for index,root in enumerate(roots):
            ai=root['atom'];ms=[sum(multiplicities[k][ai] for k,r0 in enumerate(records) if r0['s']==s) for s in range(3)]
            root_rows.append({'root_ID':sector+'_root%03d'%index,'atom':ai,'M20_interval':[str(root['lo']),str(root['hi'])],'native_interval':[str(root['lo']/20),str(root['hi']/20)],'multiplicity_by_loading':ms,'component_multiplicity':[m[ai] for m in multiplicities]})
        rows=[]
        for s in range(3):
            ordered=[(rr,root) for rr,root in zip(root_rows,roots) for _ in range(rr['multiplicity_by_loading'][s])];old=saved[sector+'_base_eigenvalues'][s]
            check('complete sorted saved mode census',len(ordered)==len(old)==(112 if two else 16) and bool(np.all(np.diff(old)>=0)))
            maxerr=0.
            for e,(rr,root) in zip(old,ordered):
                error=abs(float((root['lo']+root['hi'])/40)-float(e));maxerr=max(maxerr,error);check('ordered exact root aligns old numerical mode',math.isfinite(error) and error<=TOL)
            rows.append({'sector':sector,'s':s,'saved_native_eigenvalues':old.tolist(),'mode_exact_root_ID':[rr['root_ID'] for rr,root in ordered],'maximum_numerical_alignment_error':maxerr,'dimension':len(old),'projector_scope':'Exact root/multiplicity census; numerical vectors/responses retain separate residual and1e-9unresolved qualification.'})
        stage={'sector':sector,'coprime_atoms_ascending':atoms,'signed_Sturm_sequences':seqs,'component_labels':[{k:r0[k] for k in ('s','S_character','R_character','dimension')} for r0 in records],'component_atom_multiplicities':multiplicities,'root_intervals':root_rows,'loading_rows':rows,'proper_clock_or_metric_calibration':False}
        commit(CP/(sector+'_root_census.json'),stage);summaries.append(stage)
    check('complete fixed certificate census',len(allblocks)==18 and len(summaries)==2 and sum(r0['dimension'] for stage in summaries for r0 in stage['loading_rows'])==384 and len(COMMITS)==21)
    for f,h in INPUTS.items():check('unchanged final input '+f,sha(ROOT/f)==h)
    result={'status':'PASS_EXACT_SAVED_RELATIVE_ENERGY_ROOT_CENSUS','failed':0,'passed':len(CHECKS),'checks':CHECKS,'sector_census':summaries,'component_count':18,'saved_mode_count':384,'Sturm_splits':SPLITS,'input_sha256':INPUTS,'manifest_sha256':mh,'PID':os.getpid(),'elapsed_seconds':time.monotonic()-started,'scope':'Exact action/symmetry/polynomial/root labels only; no new eigensystem, physical dephasing implementation, response precision, passivity, gravity or state adoption.'}
    raw=write(RESULT,result);ch=hashlib.sha256(canon(result)).hexdigest();event({'event':'result_saved','raw_sha256':raw,'canonical_sha256':ch})
    with MD.open('x') as f:
        f.write('# Exact relative-energy projector census V001\n\nPASS:18 exact symmetry blocks,6 complete loading rows and384 sorted saved numerical modes. All roots, multiplicities, signed Sturm sequences and interval labels remain in JSON/checkpoints. This certifies the spectral census; it does not qualify numerical response projectors/near poles, physical passivity or gravity. No old dynamics/eigensolver/preparation replay.\n\nResult SHA256: '+raw+'\n');f.flush();os.fsync(f.fileno())
    for f,h in INPUTS.items():
        if sha(ROOT/f)!=h:raise RuntimeError('input changed after result '+f)
    rh=sha(MD);event({'event':'report_saved','sha256':rh})
    cmap={p.name:sha(p) for p in CP.iterdir() if p.name!='journal.jsonl'}
    if cmap!=COMMITS or len(cmap)!=21:raise RuntimeError('incomplete21checkpoint map')
    receipt={'status':result['status'],'failed':0,'passed':result['passed'],'input_sha256':INPUTS,'checkpoint_sha256':cmap,'result_raw_sha256':raw,'result_canonical_sha256':ch,'report_sha256':rh,'journal_prefix_sha256':sha(CP/'journal.jsonl'),'PID':os.getpid()}
    rr=write(RECEIPT,receipt);event({'event':'receipt_saved','sha256':rr});print(json.dumps({'status':result['status'],'result_raw_sha256':raw,'receipt_sha256':rr,'Sturm_splits':SPLITS}),flush=True)

if __name__=='__main__':
    try:main()
    except Exception as error:
        if STARTED and not ERROR.exists():
            eh=write(ERROR,{'status':'EXECUTION_ERROR_PRESERVED','error':repr(error),'traceback':traceback.format_exc(),'active':ACTIVE,'checks':CHECKS,'input_sha256':INPUTS,'committed_sha256':COMMITS,'source_sha256':sha(__file__),'PID':os.getpid()});event({'event':'error','sha256':eh})
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
