"""Saved evidence only. No producer imports, interpolation, ODE or compilation.

Stdout-only audit of the immutable ordinary PRIMAT qualification receipts.
"""
import base64
import hashlib
import json
import math
from pathlib import Path
import zlib

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
B = J/'bbn_inputs_v001/primat_c_reference_v001'
D = B/'build_ordinary_v001'
R = D/'receipts'
files = {}
checks = 0
failures = []

def sha(raw): return hashlib.sha256(raw).hexdigest()
def enc(x): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def test(ok,label):
    global checks
    checks += 1
    if not ok: failures.append(label)
def close(a,b,label,rtol=2e-12,atol=1e-30):
    test(math.isfinite(a) and math.isfinite(b) and abs(a-b)<=atol+rtol*max(abs(a),abs(b)),label)
def raw(p):
    p=Path(p)
    if not p.is_absolute(): p=ROOT/p
    p.relative_to(ROOT)
    assert not any(q.is_symlink() for q in (p,*p.parents))
    x=p.read_bytes(); files[str(p.relative_to(ROOT))]=sha(x); return x
def read(p): return json.loads(raw(p))
def artifact(a):
    x=raw(a['path']);test(sha(x)==a['sha256'] and len(x)==a['bytes'],'artifact '+a['path'])
def packed(x):
    test(x['codec']=='zlib+base64','codec')
    z=zlib.decompressobj();v=z.decompress(base64.b64decode(x['data'],validate=True));v+=z.flush()
    test(z.eof and not z.unused_data and not z.unconsumed_tail,'single complete zlib stream')
    test(len(v)==x['bytes'] and sha(v)==x['sha256'],'packed raw bytes')
    return v

freeze_path=D/'PRIMAT_ORDINARY_SUPERVISOR_V001_FROZEN.json'
freeze=read(freeze_path);fh=sha(raw(freeze_path))
test(fh=='1ef54049931289f2c8715d56f080566e1aecb01e483aada8681fe7b985d7ed00','pinned freeze')
test(sha(enc(freeze['files']))==freeze['input_digest'],'freeze input digest')
for p,h in freeze['files'].items(): test(sha(raw(p))==h,'frozen '+p)
test(freeze['member_census']==dict(code=46,data=24,licenses=2,derived_library=2),'input census')
def packet(p):
    w=read(p);test(w['freeze_sha256']==fh,'packet freeze '+str(p))
    test(sha(enc(w['payload']))==w['payload_sha256'],'payload '+str(p));return w['payload']
def invocation(v):
    test(v['returncode']==0 and v['resource_stop'] is None and v['exception'] is None and not v['resource_monitor_errors'],'completed invocation')
    return packed(v['stdout']),packed(v['stderr'])

manifest=read(B/'PRIMAT_ORDINARY_BUILD_MANIFEST_V001.json')
build=packet(D/'PRIMAT_ORDINARY_BUILD_V001.json')
test(build['status']=='BUILD_COMPLETE' and len(build['commands'])==24,'build census')
test(build['input_digest']==freeze['input_digest'] and build['manifest_sha256']==sha(raw(B/'PRIMAT_ORDINARY_BUILD_MANIFEST_V001.json')),'build inputs')
version=packet(R/'compiler_version.json');invocation(version['invocation'])
test(build['compiler_version_sha256']==sha(raw(R/'compiler_version.json')),'compiler version binding')
for i,(c,a) in enumerate(zip(manifest['commands'],build['commands'])):
    artifact(a);p=packet(R/f'command_{i:03d}.json');invocation(p['invocation']);artifact(p['output'])
    test(p['command']==c and p['invocation']['argv']==c['argv'] and p['status']=='COMMAND_COMPLETE','command '+str(i))
    test(p['compiler_version_sha256']==build['compiler_version_sha256'] and p['input_digest']==freeze['input_digest'],'command ancestry')
    intent=packet(R/f'command_{i:03d}_intent.json');test(intent['command']==c and intent['input_digest']==freeze['input_digest'],'command intent')
artifact(build['binary'])
dep=read(B/'PRIMAT_C_READONLY_DEPENDENCY_MANIFEST_V001.json')
for row in dep['code_files']:
    v=raw(B/'upstream'/row['path'])
    test(len(v)==row['bytes'] and hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()==row['git_blob_sha1'],'code Git blob')
for i,row in enumerate(dep['data_files']):
    a=read(B/f'DATA_ACQUISITION_{i:03d}_V001.json')
    z=zlib.decompressobj();v=z.decompress(base64.b64decode(a['raw_zlib_base64'],validate=True));v+=z.flush()
    test(z.eof and not z.unused_data and len(v)==row['bytes'] and sha(v)==a['raw_sha256'],'data receipt bytes')
    test(hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()==row['git_blob_sha1'],'data Git blob')
    text=v.decode().replace('\r\n','\n');test('\r' not in text,'data CR rule')
    if not text.endswith('\n'):text+='\n'
    test(raw(B/'upstream'/row['path'])==text.encode(),'data published normalization')

results={};summaries={}
for profile,expected in [('default','1c7031401f5a37450946a270c6503e2e6b1ad27103ba70d477956ec728629e60'),('refined','0c76bc2b05e9a821de3c411b5441cbb8f0b1ba8127d2f90bc4b18444e8320475')]:
    path=R/f'run_{profile}.json';test(sha(raw(path))==expected,'pinned '+profile)
    p=packet(path);out,err=invocation(p['invocation']);r=p['result'];results[profile]=r
    test(json.loads(out)==r,'exact stdout parsed result')
    test(p['profile']==profile and p['status']=='ORDINARY_PROFILE_COMPLETE' and p['validation_error'] is None,'run status')
    artifact(p['binary']);artifact(p['build_receipt']);test(p['binary']==build['binary'],'same compiled binary')
    test(p['input_digest']==freeze['input_digest'],'run input binding')
    intent=packet(R/f'run_{profile}_intent.json');test(intent['binary']==p['binary'] and intent['profile']==profile,'run intent')
    test(r['species']==['n','p','H2','H3','He3','He4','Li7','Be7'] and r['mass_numbers']==[1,1,2,3,3,4,7,7],'species')
    n=r['nuclear_history'];bg=r['background'];ht=r['HT_relaxation'];mi=math.inf;de=0.
    for i,row in enumerate(n):
        test(len(row)==12 and all(math.isfinite(x) for x in row) and row[0]>0 and row[1]>0 and row[2]>0,'nuclear schema')
        if i:test(row[0]>=n[i-1][0],'nuclear ordering, duplicate era ends allowed')
        ys=row[4:];baryon=sum(a*y for a,y in zip(r['mass_numbers'],ys));close(baryon,row[3],'saved baryon sum',atol=2e-16)
        test(all(y>=-1e-12 for y in ys) and abs(baryon-1)<=1e-8,'unclipped abundances/conservation')
        mi=min(mi,*ys);de=max(de,abs(baryon-1))
    close(mi,r['controls']['minimum_raw_Y'],'minimum raw abundance',atol=1e-35)
    close(de,r['controls']['maximum_baryon_sum_defect'],'max baryon defect',atol=2e-16)
    weak=0;comoving=[]
    for i,row in enumerate(bg):
        test(len(row)==10 and all(math.isfinite(x) and x>0 for x in row[:8]),'background positive')
        if i:test(row[0]>bg[i-1][0] and row[1]<bg[i-1][1] and row[2]>bg[i-1][2],'background order')
        if row[1]<=10:
            weak+=1;test(all(x is not None and math.isfinite(x) and x>=0 for x in row[8:]),'weak domain')
        else:test(row[8:]==[None,None],'no high-T weak extrapolation')
        comoving.append(row[7]*row[2]**3)
    rho_a3_rel=max(abs(x/comoving[0]-1) for x in comoving)
    test(rho_a3_rel<2e-12,'saved background baryon mass conservation')
    N=len(ht)-1;test(N==2048,'HT census');dl=math.log(ht[-1][0]/ht[0][0])/N
    for i,row in enumerate(ht):
        test(len(row)==5 and all(math.isfinite(x) and x>=0 for x in row),'HT entries')
        close(row[4],row[0]*(row[2]+row[3]),'HT generator')
        close(row[0],ht[0][0]*math.exp(i*dl),'HT log-time node')
    fine=sum((1 if i in (0,N) else 4 if i%2 else 2)*ht[i][4] for i in range(N+1))*dl/3
    coarse=sum((1 if i in (0,N) else 4 if (i//2)%2 else 2)*ht[i][4] for i in range(0,N+1,2))*2*dl/3
    hs=r['HT_relaxation_summary'];qd=abs(fine-coarse)/max(1,abs(fine))
    for k,v in [('K_Simpson_2048',fine),('K_Simpson_1024',coarse),('normalized_difference',qd),('log_contraction_estimate',-fine)]:close(v,hs[k],'HT '+k,atol=5e-15)
    test(qd<=2e-5 and fine>0,'unchanged HT gate')
    y=n[-1][4:];yp=4*y[5];f=dict(YPBBN=yp,YPCMB=(4.0026032541/4*yp)/(4.0026032541/4*yp+1.00782503223*(1-yp)),DoH=y[2]/y[1],He3oH=(y[3]+y[4])/y[1],Li7oH=(y[6]+y[7])/y[1],Neff=sum((t/bg[-1][1])**4 for t in bg[-1][4:7])/(4/11)**(4/3))
    for k,v in f.items():close(v,r['final'][k],'assembled '+k)
    producer_count=19*len(n)+2*len(bg)+weak+2055
    test(producer_count==r['controls']['checks'] and r['controls']['failures']==0 and r['controls']['nonfinite_output_values']==0,'producer check census')
    summaries[profile]=dict(final=r['final'],nuclear_rows=len(n),background_rows=len(bg),HT_rows=len(ht),producer_checks=producer_count,minimum_raw_Y=mi,maximum_baryon_defect=de,rho_a3_relative_span=rho_a3_rel,HT=hs,seconds=p['invocation']['seconds'],sampled_RSS_bytes=p['invocation']['peak_sampled_process_group_rss_bytes'],sampled_RSS_is_not_peak_measurement=True,stdout_sha256=sha(out),stderr_sha256=sha(err))

test(results['default']['background']==results['refined']['background'],'identical fixed ordinary backgrounds')
test(results['default']['HT_relaxation']==results['refined']['HT_relaxation'],'identical fixed HT generator')
test(results['default']['physical']==results['refined']['physical'],'same physical parameters')
test(results['default']['numerical']['nuclear_rtol']==1e-7 and results['refined']['numerical']['nuclear_rtol']==1e-8,'nuclear-only refinement')
comparison=packet(R/'ordinary_comparison.json')
for a in comparison['profiles']:artifact(a)
for c in comparison['checks']:
    name=c['quantity'];a=results['default']['final'][name];b=results['refined']['final'][name]
    diff=(a-b)/(b if c['relative'] else 1);close(diff,c['signed_difference'],'refinement '+name,atol=1e-20)
    tol={'DoH':5e-5,'YPBBN':1e-5,'YPCMB':1e-5,'Neff':2e-12}[name]
    test(tol==c['tolerance'] and c['passed']==(abs(diff)<=tol),'unchanged refinement gate')
test(comparison['status']=='QUALIFIED_ORDINARY_NUCLEAR_REFINEMENT_ONLY' and comparison['per_profile_control_failures']==[0,0],'comparison qualification')
payload=dict(status='PASS_SAVED_ARITHMETIC_ONLY' if not failures else 'FAILED_SAVED_AUDIT',checks=checks,failures=failures,source_sha256=sha(raw(Path(__file__).resolve())),freeze_sha256=fh,files=files,profiles=summaries,comparison=comparison,scope='No library/producer import, atomic/nuclear/background evolution, rate interpolation, compilation or observational likelihood; saved histories and custody only.')
print(enc(dict(payload=payload,payload_sha256=sha(enc(payload)))).decode())
