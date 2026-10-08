"""Saved-only independent hard-barotrope qualification audit; no provider calls."""
import base64,collections,hashlib,json,math
from pathlib import Path
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def raw(p):
    p=Path(p);p.relative_to(ROOT)
    if p.resolve()!=p:raise RuntimeError('Noncanonical input')
    return p.read_bytes()
def main():
    failures=[];n=0;maxima={}
    def ck(k,v):
        nonlocal n
        n+=1
        if not v:failures.append(k)
    def close(k,a,b,at=2e-13,rt=2e-9):
        e=abs(a-b)/(at+rt*max(abs(a),abs(b)))
        maxima[k]=e;ck(k,math.isfinite(e) and e<=1)
    pins={'FROZEN':'0c860d03db9490555f4e64ff5f2f95803d1583b00bf175c8ed5fb738d6720f6f',
          'BUILD':'80e4f91eb481ccff59ba2462cf07618bfd4e2ae8c67e927cc40f5a79a03d73ff',
          'BENCHMARK':'a01a7f522fb731a4b447d0a5105b7f076763f776ce3e46702b5b4f4ecb93bb0a',
          'RESULTS':'ef0b3b0503a0d8ffd3df1cbdfe2972176a821de2e2cd3a8e8a99e810b693272b'}
    wrappers={}
    for key,h in pins.items():
        b=raw(J/('HARD_BAROTROPE_QUALIFICATION_V001_'+key+'.json'));ck('raw '+key,sha(b)==h)
        wrappers[key]=json.loads(b)
    f=wrappers['FROZEN']
    for path,h in f['files'].items():ck('member '+path,sha(raw(ROOT/path))==h)
    for key in ('BUILD','BENCHMARK','RESULTS'):
        w=wrappers[key];ck('freeze '+key,w['freeze_sha256']==pins['FROZEN'])
        ck('payload '+key,sha(enc(w['payload']))==w['payload_sha256'])
    b=wrappers['BUILD']['payload'];ck('build',b['status']=='COMPLETE_BUILD')
    binary=raw(b['binary']['path']);ck('binary',sha(binary)==b['binary']['sha256'] and len(binary)==b['binary']['bytes'])
    ck('compiler argv',b['compiler']['argv']==f['build_argv'])
    for label,p in [('version',b['version']),('compiler',b['compiler'])]:
        ck(label+' success',p['returncode']==0 and p['exception'] is None)
        for channel in ('stdout','stderr'):
            ck(label+' '+channel,sha(base64.b64decode(p[channel+'_base64'],validate=True))==p[channel+'_sha256'])
    inv=json.loads(raw(J/'BBN_SHARED_INVERSE_V001_RESULTS.json'))['payload']
    states={(s['background_id'],s['point_id'],s['spectrum_index']):s for s in inv['state_rows']}
    histories=[]
    for bi in range(5):histories.extend(json.loads(raw(J/f'FINITE_PRESSURE_BAO_RULER_V001_BACKGROUND_{bi}.json'))['payload']['records'])
    histories.sort(key=lambda r:(r['background_id'],r['point_id']))
    reports={}
    for typ in ('BENCHMARK','RESULTS'):
        p=wrappers[typ]['payload'];m=p['material'];tag=typ+' '
        ck(tag+'status',p['validation_error'] is None and p['comparison_failures']==[] and m['failures']==[] and m['status']=='COMPLETE_MATERIAL_QUALIFICATION')
        ck(tag+'configuration',p['configuration']==f['configuration'])
        proc=p['process'];ck(tag+'process',proc['returncode']==0 and proc['exception'] is None)
        for channel in ('stdout','stderr'):
            buf=base64.b64decode(proc[channel+'_base64'],validate=True)
            ck(tag+channel+' hash',sha(buf)==proc[channel+'_sha256'])
            if channel=='stdout':ck(tag+'stdout parsed',json.loads(buf)==m)
        selected=histories if typ=='RESULTS' else [histories[0],next(r for r in histories if r['finite_gap'])]
        lines=[];mapping=[];meta=[];byid={}
        for r in selected:
            idx=histories.index(r);bi,pi=r['background_id'],r['point_id']
            meta.append(dict(history_id=idx,background_id=bi,point_id=pi,point_roles=r['point_roles'],finite_gap=r['finite_gap']))
            for si in range(4):
                s=states[(bi,pi,si)];rid=4*idx+si;finite=r['finite_gap'];byid[rid]=(r,s)
                v=[rid,1 if finite else 2,1 if si==0 else 0,s['R'] if finite else 0.,s['I'] if finite else 0.,s['hard_energy'] if finite else 0.,s['Omega_exc'],s['w'] if finite else 0.,s['cI2'] if finite else 0.,s['omega']/s['R'] if finite else 0.,r['r1']]
                lines.append(' '.join(str(x) for x in v))
                mapping.append(dict(id=rid,history_id=idx,background_id=bi,point_id=pi,spectrum_index=si,status=s['status']))
        ck(tag+'stdin',sha((f'1 {len(lines)}\n'+'\n'.join(lines)+'\n').encode())==p['stdin_sha256'])
        ck(tag+'mapping',mapping==p['retained_label_mapping'] and meta==p['history_metadata'])
        ck(tag+'census',p['history_count']==len(selected) and p['label_count']==len(mapping))
        rows={r['id']:r for r in m['rows']};ck(tag+'row ids',len(rows)==len(m['rows']) and set(rows)==set(byid)|{-1,-2,-3,-4})
        expected=collections.Counter(census=1);epochs=0;comparisons=[]
        def comp(a,b):
            comparisons.append(abs(a-b)/(2e-13+2e-9*max(abs(a),abs(b))))
        for rid,row in rows.items():
            label=tag+str(rid)+' ';syn=rid<0;finite=row['kind']==1
            ck(label+'initialization',row['init_status']==[0,0] and row['failed_checks']==0 and row['synthetic']==syn)
            full=syn or rid%4==0;aa=[1.,10.,1000.] if syn else p['configuration']['epoch_A'] if full else [1.]
            ck(label+'epochs',[r[0] for r in row['epochs']]==aa and all(len(r)==10 for r in row['epochs']) and row['full']==full)
            if not syn:
                old,s=byid[rid];ck(label+'kind',finite==old['finite_gap'])
            expected['initialization']+=2;expected['invalid_inputs']+=4 if finite else 2
            rb=row['epochs'][0][5]
            for ep in row['epochs']:
                A,er,w,cs,om,r,dw,dcs,ar,ref=ep;epochs+=1
                for k,c in [('GL64_128',4),('conservation',3),('trace_virial',1),('energy_envelope',1),('fluid_rhs',7),('gauge_stress',4),('evaluation',2)]:expected[k]+=c
                if finite:
                    for k,c in [('Simpson_GL',3),('Simpson1024_2048',3),('independent_action',1)]:expected[k]+=c
                    if A==1:expected['saved_anchor']+=4
                    close(label+str(A)+' energy ratio',er,(r*(2+r))/(rb*(2+rb)),at=2e-13,rt=2e-11)
                    ck(label+str(A)+' domain',r>0 and om>0 and 0<w<=1/3+1e-14 and 0<cs<=1/3+1e-14)
                    close(label+str(A)+' dw identity',dw,-3*(1+w)*(cs-w),at=2e-13,rt=2e-10)
                    ck(label+str(A)+' action residual',abs(ar)<2e-9 and abs(ref)<2e-9)
                    if not syn and A==1:
                        for v,t in [(w,s['w']),(cs,s['cI2']),(om,s['omega']/s['R']),(r,old['r1'])]:close(label+'anchor '+str(t),v,t,at=1e-300 if t in (s['w'],s['cI2'],old['r1']) else 2e-13)
                else:
                    expected['explicit_dust']+=4
                    ck(label+str(A)+' dustnull',om is None and r is None and w==cs==dw==dcs==ar==ref==0)
                    close(label+str(A)+' dust energy',er,A**3,rt=2e-11)
                ck(label+str(A)+' envelope',A**3*(1-2e-10)<=er<=A**4*(1+2e-10))
                if full and 1<A<1e7:
                    expected['evaluation']+=2;expected['Richardson_derivative']+=5;expected['FD_step_refinement']+=5
            if not syn and full:
                ee={e[0]:e for e in row['epochs']}
                for oldep in old['epochs']:
                    if oldep['A'] in ee:
                        e=ee[oldep['A']]
                        for index,key in [(1,'energy_over_present'),(2,'w'),(3,'cI2')]:comp(e[index],oldep[key])
        for r in selected:
            idx=histories.index(r);ref=rows[4*idx]['epochs'][0]
            for si in range(1,4):
                other=rows[4*idx+si]['epochs'][0]
                for k in ([2,3,4,5] if r['finite_gap'] else [2,3]):comp(ref[k],other[k])
        ck(tag+'C category census',dict(expected)==m['counts'] and sum(expected.values())==m['checks'])
        ck(tag+'all saved C maxima',all(math.isfinite(x) and 0<=x<=1 for x in m['maximum_tolerance_fractions'].values()))
        ck(tag+'comparison count',len(comparisons)==p['comparison_count'] and p['comparison_nonfinite']==0)
        close(tag+'comparison maximum',max(comparisons),p['comparison_maximum'],at=1e-16,rt=1e-12)
        ck(tag+'independent saved comparisons',max(comparisons)<=1)
        reports[typ]=dict(histories=len(selected),labels=len(mapping),epochs=epochs,original_C_checks=m['checks'],original_comparison_checks=len(comparisons),C_group_maxima=m['maximum_tolerance_fractions'],seconds=proc['seconds'])
    p=wrappers['RESULTS']['payload'];ranges={}
    for A in p['configuration']['epoch_A']:
        ep=[r['epochs'][p['configuration']['epoch_A'].index(A)] for r in p['material']['rows'] if r['id']>=0 and r['full'] and r['kind']==1]
        ranges[str(A)]={k:[min(e[i] for e in ep),max(e[i] for e in ep)] for i,k in [(1,'energy_ratio'),(2,'w'),(3,'ca2')]}
    out=dict(schema='HARD_BAROTROPE_QUALIFICATION_SAVED_AUDIT_V001',status='PASS' if not failures else 'FAIL',checks=n,failures=failures,
      input_hashes=pins,frozen_member_count=len(f['files']),source_sha256=sha(raw(Path(__file__).resolve())),reports=reports,finite_history_ranges=ranges,
      max_audit_tolerance_fraction=max(maxima.values()),scope='Saved hashes/arrays/algebra only. Quadrature, inversion, FD and C evaluation were not rerun; their original maxima are source-bound certificates.')
    print(json.dumps(out,sort_keys=True,indent=2,allow_nan=False));return bool(failures)
if __name__=='__main__':raise SystemExit(main())
