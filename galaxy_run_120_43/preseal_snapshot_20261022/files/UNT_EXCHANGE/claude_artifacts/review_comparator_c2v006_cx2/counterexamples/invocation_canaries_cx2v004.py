"""0553 independent c2v005 invocation/value canaries; synthetic files only.
Successor v003 adds exact v005 RA_PINSET dependencies and adopts the strict v005 complete-tail request/manifest contract. Old v001 is preserved.

All mutations happen in memory before exclusive creation. No imported checker
builder or copied run fixture; no subprocess, solver, real-run reads or network.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[k]='1'
import argparse
import contextlib
import copy
import datetime
import hashlib
import io
import json
import resource
import sys
import time
import types
from pathlib import Path
import numpy as np

import hashlib as _hashlib
_g=Path(__file__).resolve().parent/'guard_cx2v001.py';_b=_g.read_bytes();assert _hashlib.sha256(_b).hexdigest()=='b6c741172795a8ee2e769063a80faefc9795ee27b338ae0ab9990a620a7848a1';exec(compile(_b,str(_g),'exec'),globals())

EX=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
GEO=(str(EX/'stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py'),'237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb')
HR=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit')
REF_BIND=(str(HR/'ddo_composite_stable_cached_binding_v002.py'),'d81b24b7150c846a5b70c82a8668daaaef53335ced062763980a33cdbc90b6d5')
REF_FAC=(str(HR/'owned_stable_lapse_hi_facade_v001.py'),'2caca496183cdee6e95f9d0c9e3234734aa49b4ba08d0b0b50f02908f84beeb7')
attempts=[]
def audit(event,args):
    if event in ('subprocess.Popen','os.system','os.posix_spawn','os.fork','socket.connect'):
        attempts.append(event);raise RuntimeError('NO_LAUNCH_OR_NETWORK '+event)
    if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
        p=os.path.realpath(os.fsdecode(args[0]))
        if 'KMAX_A2F10_C5H_RUN_V001' in p or '/runs_ext/UVT_' in p or '/.codex/' in p:
            raise RuntimeError('FORBIDDEN_READ '+p)
        if 'NGC3198' in p and any(w in p.lower() for w in ('observed','target','rotmod')):
            raise RuntimeError('FORBIDDEN_TARGET '+p)
sys.addaudithook(audit)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pin(p):p=Path(p);return {'path':str(p.resolve()),'sha256':sha(p.read_bytes())}
def raw_json(obj):return (json.dumps(obj,sort_keys=True,indent=1,allow_nan=False)+'\n').encode()
def load(p,h,name):
    raw=Path(p).read_bytes()
    if sha(raw)!=h:raise ValueError('BYTE_PIN_MISMATCH '+str(p))
    m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m
    exec(compile(raw,str(p),'exec'),m.__dict__);return m
def jfile(p,d):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw_json(d))
    return pin(p)

class Tree:
    """Independent compact old-schema tree, fixed before publication."""
    def __init__(self,root,role,gate,m,drv,cm):
        self.root=root;self.role=role;self.files={};self.links={};self.gate=gate
        new=role=='NEW';tail=gate=='Z2' and new
        driver=tuple(m.DRIVER) if new else GEO
        self.add('start.json',{'driver':driver[0],'driver_sha256':driver[1]})
        self.add('inputs/seed_c2v001.json',{'numerical_inputs':{'source_rtol':2.5e-7},'probe_tag':'cx2 independent invocation'})
        seed_sha=sha(raw_json(self.files['inputs/seed_c2v001.json'][1]))
        bind=tuple(map(str,drv.RO1_ROUTE_A['binding']));fac=tuple(map(str,drv.AUX_UVT['facade']))
        worker=tuple(map(str,drv.RO1_ROUTE_A['worker_parallel'])) if tail else tuple(map(str,drv.PARALLEL_ROUTE_A['worker']))
        solver=tuple(map(str,drv.AUX_UVT['solver_parallel'])) if tail else tuple(map(str,drv.PARALLEL_ROUTE_A['solver']))
        outcome={'classification':'CONVERGED'}
        if gate=='B0P_RERUN':outcome['ro1']={'rule':'RO1','armed':False,'fired':False,'events':[],'worker_sha256':None,'binding_sha256':None}
        if tail:outcome['ro1']={'rule':'RO1','armed':True,'fired':False,'events':[],'worker_sha256':worker[1],'binding_sha256':bind[1]}
        result={'driver_sha256':driver[1],'status':'COMPLETED','valid':True,'final_pass':2,'speeds_km_s':[3.25],
                'rows':[{'id':'CX2_SYNTHETIC_ONLY','speed_km_s':3.25}],
                'passes':[{'pass':2,'rows':[{'id':'CX2_SYNTHETIC_ONLY','speed_km_s':3.25}],'max_abs_change_km_s':0.125}],
                'route_a_outcome':outcome,'scope':'Invented protocol fixture; no scientific interpretation'}
        self.add('result.json',result)
        self.add('finish.json',{'status':'COMPLETED','result_sha256':sha(raw_json(result)),'result_path':str(root/'result.json'),'retries':0})
        st='11_reference';script=drv.SCRIPTS_UVT['reference'] if tail else drv.SCRIPTS['reference']
        argv=['--columns','0,2,5','--tolerance','0.00025']
        if tail:
            self.add('inputs/uv_tail_config.json',{'uv_tail':{'enabled':True},'fixture':'CX2'})
            csha=sha(raw_json(self.files['inputs/uv_tail_config.json'][1]))
            argv+=['--uv-tail-config',str(root/'inputs/uv_tail_config.json'),'--uv-tail-config-sha256',csha,'--uv-tail-admit-test-only']
        self.add('stages/'+st+'/request.json',{'name':'reference','kind':'reference','script':str(script[0]),'script_sha256':script[1],'argv':argv,'numeric_contract':{'matrix':[[2.0,7],[True,-0.0]]}})
        self.add('stages/'+st+'/reference/finish.json',{'status':'SYNTHETIC_REFERENCE','matrix':[[0.25,-0.5],[1.0,2.0]]})
        self.files['stages/'+st+'/reference/response.npz']=('npz',{'matrix':np.arange(12,dtype=np.float64).reshape(3,4)})
        if gate=='B0P_RERUN':return
        ra='stages/07_route_a';seedpath=str(root/'inputs/seed_c2v001.json')
        argv=['--seed',seedpath,'--seed-sha256',seed_sha,'--solver',solver[0],'--solver-sha256',solver[1],
              '--outdir',str(root/ra/'attempt_000'),'--checkpoint-directory',str(root/ra/'checkpoint'),
              '--start-iteration','0','--column-workers','8']
        bp='Independent fixture boundary';nc={'source_rtol':2.5e-7}
        pins={seedpath:seed_sha,solver[0]:solver[1],(bind if tail else REF_BIND)[0]:(bind if tail else REF_BIND)[1],(fac if tail else REF_FAC)[0]:(fac if tail else REF_FAC)[1]}
        start={'worker_pin':worker[1],'input_pins':pins,'checkpoint_directory':str(root/ra/'checkpoint'),'resume':False,'start_iteration':0,'column_workers':8}
        if tail:
            for extra_p,extra_h in (drv.AUX_UVT['controller'],drv.UVT_LIB['lib'],drv.UVT_LIB['roster'],drv.UVT_LIB['provider']):
                pins[str(Path(extra_p).resolve())]=extra_h
            q='inputs/uv_tail_route_a_request.json';self.add(q,{'schema':'UNT_UV_TAIL_ROUTE_A_REQUEST_C2V001','uv_tail':{'enabled':True}})
            qsha=sha(raw_json(self.files[q][1]));pins[str(root/q)]=qsha
            rec={'request':{'path':str(root/q),'sha256':qsha},'enabled':True,'sidecar_directory':str(root/ra/'uv_tail_sidecar')}
            argv+=['--uv-tail-config',str(root/q),'--uv-tail-config-sha256',qsha,'--eps-certificate','NONE_TEST_ONLY','--eps-certificate-sha256','NONE_TEST_ONLY','--lo-certificate','NONE_TEST_ONLY','--lo-certificate-sha256','NONE_TEST_ONLY','--uv-tail-sidecar-directory',rec['sidecar_directory']]
            start['uv_tail']=rec;nc['uv_tail']=rec;bp+=' UV-TAIL c2v001 fixture'

        self.add(ra+'/request.json',{'name':'route_a','kind':'route_a','script':worker[0],'script_sha256':worker[1],'argv':argv})
        self.add(ra+'/attempt_000/start.json',start)
        self.files[ra+'/attempt_000/arrays/000007_probe.npz']=('npz',{'lattice':np.arange(15,dtype=np.float64).reshape(3,5)})
        self.files[ra+'/checkpoint/blobs/independent_blob.npy']=('raw',np.array([2.0,4.0,8.0]).tobytes())
        self.add(ra+'/checkpoint/iteration_0000/COMPLETED.json',{'iteration':0,'residual':4.0e-9,'attempt':'cx2'})
        caller={'seed':{'path':seedpath,'sha256':seed_sha},'code_pins':pins,'numerical_controls':nc,'boundary_prescription':bp,'worker':{'path':worker[0],'sha256':worker[1]}}
        ident={'format':cm.FORMAT,'kind':'identity','identity':{'caller':{'sha256':cm.digest(caller),'record':cm.encode(caller)}},'identity_sha256':'9'*64}
        ident['payload_sha256']=cm._sha(cm._canonical(ident));self.files[ra+'/checkpoint/IDENTITY.json']=('raw',cm._canonical(ident)+b'\n')
        if tail:
            md='stages/09_route_a_tail_manifest';mf=md+'/manifest/ROUTE_A_TAIL_MANIFEST.json'
            self.add(mf,{'schema':'SYNTHETIC_MANIFEST_ONLY','fixture':True})
            mh=sha(raw_json(self.files[mf][1]));mw=drv.AUX_UVT['manifest_writer'];ck=drv.AUX['checkpoint_module']
            ma=['--seed',seedpath,'--seed-sha256',seed_sha,'--attempt-directory',str(root/ra/'attempt_000'),
                '--checkpoint-directory',str(root/ra/'checkpoint'),'--checkpoint-module',str(ck[0]),'--checkpoint-module-sha256',ck[1],
                '--uv-tail-request',str(root/q),'--uv-tail-request-sha256',qsha,'--outdir',str(root/md/'manifest')]
            self.add(md+'/request.json',{'name':'route_a_tail_manifest','kind':'route_a_tail_manifest','script':str(mw[0]),'script_sha256':mw[1],'argv':ma})
            self.obj('stages/11_reference/request.json')['argv']+=['--route-a-tail-manifest',str(root/mf),'--route-a-tail-manifest-sha256',mh]
            rb=argv[argv.index('--uv-tail-config'):-2]
            self.obj('result.json')['uv_tail']={'enabled':True,'config':{'path':str(root/'inputs/uv_tail_config.json'),'sha256':csha},
                'request':{'path':str(root/q),'sha256':qsha},'manifest':{'path':str(root/mf),'sha256':mh},
                'admissibility':'test_only','test_only_flag':['--uv-tail-admit-test-only'],
                'certificates':{'eps_certificate':['NONE_TEST_ONLY','NONE_TEST_ONLY'],'lo_certificate':['NONE_TEST_ONLY','NONE_TEST_ONLY']},
                'route_a_argv':rb,'truncation_argv':'{"shape":"cube"}'}
        self.obj('finish.json')['result_sha256']=sha(raw_json(self.obj('result.json')))

    def add(self,p,d):self.files[p]=('json',copy.deepcopy(d))
    def obj(self,p):return self.files[p][1]
    def publish(self):
        for rel,(kind,value) in self.files.items():
            p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True)
            if kind=='json':jfile(p,value)
            else:
                with p.open('xb') as f:
                    if kind=='raw':f.write(value)
                    elif kind=='npz':np.savez(f,**value)
                    else:raise ValueError(kind)
        for rel,target in self.links.items():
            p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(target)

def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument('--comparator',required=True);ap.add_argument('--sha256',required=True);ap.add_argument('--out',required=True);ap.add_argument('--driver',choices=('r4','r5'),required=True);ap.add_argument('--only-baselines',action='store_true');a=ap.parse_args(argv)
    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=False);started=time.monotonic()
    m=load(a.comparator,a.sha256,'cx2_invocation_comparator');m.DRIVER[:]=list(m.DRIVERS[a.driver]);drv=m.load_driver();cm=m.load_cm();rows=[]
    owners={'F02':'REQUEST','F03':'REQUEST','F04':'REQUEST','F05':'REQUEST','F06':'REQUEST','F07':'REQUEST','F08':'SCRIPT_CUSTODY','F09':'SCRIPT_CUSTODY','F10':'REQUEST','F11':'REQUEST','F12':'REQUEST','F15':'STAGES','F16':'STAGES','F17':'STAGES','F18':'INVENTORY','F19':'INVENTORY','F20':'STAGE_SET','F22':'REQUEST','F23':'REQUEST'}
    ref_req='stages/11_reference/request.json';ra_req='stages/07_route_a/request.json';arr='stages/11_reference/reference/response.npz'
    def case(name,gate,expected,mut=None,note='',required_failure=()):
        required_failure=tuple(set(required_failure)|({owners[name[:3]]} if name[:3] in owners else set()))
        d=out/name;d.mkdir();r=Tree(d/'REF','REF',gate,m,drv,cm);n=Tree(d/'NEW','NEW',gate,m,drv,cm)
        tokens=[]
        if gate=='Z2':
            for old,new,label in ((REF_BIND,drv.RO1_ROUTE_A['binding'],'BINDING'),(REF_FAC,drv.AUX_UVT['facade'],'FACADE')):
                tokens.extend([[old[0],str(new[0]),'<'+label+'_PATH>'],[old[1],new[1],'<'+label+'_SHA>']])
        if gate=='Z2':
            for kind in sorted(drv.UVT_TAIL_KINDS):
                old,new=drv.SCRIPTS[kind],drv.SCRIPTS_UVT[kind]
                tokens.extend([[str(old[0]),str(new[0]),'<UVT_'+kind+'_PATH>'],[old[1],new[1],'<UVT_'+kind+'_SHA>']])
        if mut:mut(r,n,tokens,d)
        r.publish();n.publish();tp=d/'TOKENS.json';jfile(tp,{'declared':tokens})
        op=d/'REPORT.json';argv=['--driver',a.driver,'--gate',gate,'--reference',str(r.root),'--new',str(n.root),'--tokens',str(tp),'--out',str(op)]
        stderr=io.StringIO();stdout=io.StringIO();exception=None
        try:
            with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):m.main(argv)
        except (Exception,SystemExit) as e:exception=type(e).__name__+': '+str(e)
        rep=json.loads(op.read_bytes()) if op.exists() else {}
        verdict=rep.get('verdict','REFUSED');passed=(verdict=='PASS_BITWISE_EQUAL') if expected=='PASS' else (verdict in ('FAIL','REFUSED'))
        passed=passed and all(k in (rep.get('failing') or []) for k in required_failure)
        if name=='F08_Z2_NEW_base_equals_REF_with_tokens':passed=passed and rep.get('checks',{}).get('TOKENS_POLICY',{}).get('pass') is True
        rows.append({'name':name,'gate':gate,'expected':expected,'actual':verdict,'pass':passed,'failing':rep.get('failing'),
                     'owner_details':{k:rep.get('checks',{}).get(k) for k in required_failure},'exception':exception,'note':note,'required_failure':list(required_failure),'report':pin(op) if op.exists() else None,'tokens':pin(tp)})
        print(name,expected,verdict,rep.get('failing'),flush=True)
    case('P00_distinct_invocation_baseline','B0P_RERUN','PASS')
    case('P01_Z2_correct_explicit_replacement','Z2','PASS')
    if not a.only_baselines:
        def req(n):return n.obj(ref_req)
        case('F02_swap_nontail_option_values','B0P_RERUN','FAIL',lambda r,n,t,d:req(n).update(argv=['--columns','0.00025','--tolerance','0,2,5']))
        case('F03_duplicate_nontail_option','B0P_RERUN','FAIL',lambda r,n,t,d:req(n)['argv'].extend(['--tolerance','0.00025']))
        case('F04_joined_tail_assignment','Z2','FAIL',lambda r,n,t,d:req(n)['argv'].extend(['--uv-tail-config='+str(n.root/'inputs/uv_tail_config.json')]))
        case('F05_tail_missing_value_at_end','Z2','FAIL',lambda r,n,t,d:req(n)['argv'].append('--uv-tail-config'))
        case('F06_duplicate_valid_tail_config','Z2','FAIL',lambda r,n,t,d:req(n)['argv'].extend(['--uv-tail-config',str(n.root/'inputs/uv_tail_config.json')]),'Both duplicates are inside the run; unlike the old checker outside-first duplicate.')
        case('F07_route_A_only_flag_on_reference','Z2','FAIL',lambda r,n,t,d:req(n)['argv'].extend(['--eps-certificate','NONE_TEST_ONLY']))
        def base_new(r,n,t,d):
            old=drv.SCRIPTS['reference'];req(n)['script']=str(old[0]);req(n)['script_sha256']=old[1]
            # Keep all declared tokens in valid replace mode; raw script must still fail.
        case('F08_Z2_NEW_base_equals_REF_with_tokens','Z2','FAIL',base_new,'NEW base script must fail even when REF and NEW raw paths/hashes are equal; the declared token set remains valid replace mode.',required_failure=('SCRIPT_CUSTODY',))
        case('F09_NEW_base_hash_wrong','B0P_RERUN','FAIL',lambda r,n,t,d:req(n).update(script_sha256='0'*64))
        case('F10_request_nested_signed_zero','B0P_RERUN','FAIL',lambda r,n,t,d:req(n)['numeric_contract']['matrix'][1].__setitem__(1,0.0))
        case('F11_request_nested_int_float','B0P_RERUN','FAIL',lambda r,n,t,d:req(n)['numeric_contract']['matrix'][0].__setitem__(1,7.0))
        case('F12_request_nested_bool_int','B0P_RERUN','FAIL',lambda r,n,t,d:req(n)['numeric_contract']['matrix'][1].__setitem__(0,1))
        case('P13_equal_nested_signed_zero','B0P_RERUN','PASS',lambda r,n,t,d:[x.obj(ref_req).update(numeric_contract={'signed_zero_vector':[-0.0,-0.0]}) for x in (r,n)])
        def equal_mixed(r,n,t,d):
            for x in (r,n):x.obj(ref_req)['numeric_contract']={'mixed':[1,1.0,-0.0,0.0,False]}
        case('P14_equal_distinct_scalar_types','B0P_RERUN','PASS',equal_mixed)
        def complex_zero(r,n,t,d):
            r.files[arr]=('npz',{'z':np.array([complex(2.0,0.0)])});n.files[arr]=('npz',{'z':np.array([complex(2.0,-0.0)])})
        case('F15_npz_imaginary_signed_zero','B0P_RERUN','FAIL',complex_zero)
        def dtype(r,n,t,d):
            r.files[arr]=('npz',{'n':np.array([3,5],dtype=np.int32)});n.files[arr]=('npz',{'n':np.array([3,5],dtype=np.float32)})
        case('F16_npz_integer_float_dtype','B0P_RERUN','FAIL',dtype)
        def order(r,n,t,d):
            z=np.arange(12,dtype=np.float64).reshape(3,4);r.files[arr]=('npz',{'m':np.array(z,order='C')});n.files[arr]=('npz',{'m':np.array(z,order='F')})
        case('F17_npz_C_F_storage_difference','B0P_RERUN','FAIL',order,'Original P17 becomes MUST_FAIL under c2v006 ARRAY_POLICY: storage order is identity for NPZ too.',required_failure=('STAGES',))
        case('F18_extra_dangling_symlink','B0P_RERUN','FAIL',lambda r,n,t,d:n.links.update({'dangling_alias.json':str(d/'NO_SUCH_TARGET.json')}))
        def external_link(r,n,t,d):
            target=d/'external_target.json';jfile(target,{'outside_fixture_tree':True});n.files.pop('stages/11_reference/reference/finish.json');n.links['stages/11_reference/reference/finish.json']=str(target)
        case('F19_external_symlink_different_payload','B0P_RERUN','FAIL',external_link)
        case('F20_extra_stage_directory_symlink','B0P_RERUN','FAIL',lambda r,n,t,d:n.links.update({'stages/22_alias_reference':str(n.root/'stages/11_reference')}))
        case('P21_exact_tail_block_prefix_insertion','Z2','PASS',lambda r,n,t,d:req(n).update(argv=req(n)['argv'][4:]+req(n)['argv'][:4]),'Route-B comparison permits the same exact contiguous block before the unchanged ordinary argv; route-A still requires suffix.')
        case('F22_tail_flag_on_reference_side','Z2','FAIL',lambda r,n,t,d:r.obj(ref_req)['argv'].extend(['--uv-tail-admit-test-only']))
        case('F23_manifest_outside_run','Z2','FAIL',lambda r,n,t,d:req(n)['argv'].extend(['--route-a-tail-manifest',str(d/'outside_manifest.json')]))
    rep={'date_u':os.environ.get('CX2_DATE_U'),'execution_note':'nice unavailable (sandbox); 0514 waiver','schema':'CX2_INVOCATION_VALUE_CANARIES_V003','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'status':'TESTED' if pin(a.comparator)['sha256']==a.sha256 else 'STALE','selected_driver':a.driver,'tested_sha256':a.sha256,'byte_pin_unchanged_after':pin(a.comparator)['sha256']==a.sha256,'comparator':pin(a.comparator),'source':pin(__file__),'rows':rows,
         'passed':sum(r['pass'] for r in rows),'total':len(rows),'unexpected':[r['name'] for r in rows if not r['pass']],
         'all_trees_synthetic':True,'scientific_launches':0,'process_network_attempts':attempts,
         'elapsed_s':time.monotonic()-started,'max_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'limits':['Synthetic comparator protocol cases only. No identity claim for any scientific run.',
                   'Full-main verdicts are reported; failed positive controls invalidate interpretation of dependent negatives.']}
    p=jfile(out/'RESULT.json',rep);print(json.dumps({'passed':rep['passed'],'total':rep['total'],'unexpected':rep['unexpected'],'result':p}))
if __name__=='__main__':main()
