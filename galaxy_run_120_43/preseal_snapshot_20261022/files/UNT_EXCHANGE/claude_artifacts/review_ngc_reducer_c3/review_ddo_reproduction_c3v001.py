import json, hashlib, importlib.util, sys
H="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13"
R='claude_artifacts/ngc_route_impl_c2/reducer'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def load(name,p):
    s=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
saved=f'{H}/CODEX1/DDO154_MONOTONE_SOURCE_RECONSTRUCTION_RUN_V001/source.json'; v2p=f'{H}/helpers/recovered_packet_audit/ddo_monotone_bernstein_source_controls_v002.py'; prof=f'{H}/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json'
E={'pins':{saved:sha(saved),v2p:sha(v2p),prof:sha(prof)}}
S=json.load(open(saved)); V3=json.load(open(f'{R}/DDO154_V003_REPRODUCTION_DRYRUN_V001/source.json'))
shared=sorted(set(S)&set(V3)); diff=[k for k in shared if S[k]!=V3[k]]
E['saved_vs_v003_file']={'shared_keys':shared,'differing_shared_keys':diff,'only_in_saved':sorted(set(S)-set(V3)),'only_in_v003':sorted(set(V3)-set(S)),
 'controls_bitwise': S['source_record']['boundary_controls_Msun_pc2']==V3['source_record']['boundary_controls_Msun_pc2'] and S['source_record']['middle_controls_Msun_pc2']==V3['source_record']['middle_controls_Msun_pc2']}
# diagnostics may legitimately differ in key sets; report sub-diffs for dict keys
for k in diff:
    if isinstance(S[k],dict) and isinstance(V3[k],dict):
        E['saved_vs_v003_file']['subdiff_'+k]={'keys_differing':[kk for kk in set(S[k])|set(V3[k]) if S[k].get(kk)!=V3[k].get(kk)]}
# in-memory V002 vs V003 on the DDO record with all-F directions
rec=json.load(open(prof))['galaxies']['DDO154']['HI_plus_He']
v2=load('v2',v2p); v3=load('v3',f'{R}/segment_monotone_bernstein_source_controls_v003.py')
import inspect
sig2=inspect.signature(v2.reduce_source).parameters; E['v002_reduce_source_params']=list(sig2)
kw={'record':rec,'max_sweeps':200000,'kkt_tolerance':1e-10}
r2=v2.reduce_source(**kw); r3=v3.reduce_source(directions='F'*len(rec['annular_means_Msun_pc2']),**kw)
E['in_memory']={'v002_status':r2['status'],'v003_status':r3['status'],'controls_bitwise':r2['source_record']['boundary_controls_Msun_pc2']==r3['source_record']['boundary_controls_Msun_pc2'] and r2['source_record']['middle_controls_Msun_pc2']==r3['source_record']['middle_controls_Msun_pc2'],
 'objective_equal':r2['diagnostics']['objective']==r3['diagnostics']['objective'],'sweeps':(r2['diagnostics']['sweeps'],r3['diagnostics']['sweeps']),
 'v002_controls_equal_saved_file': r2['source_record']['boundary_controls_Msun_pc2']==S['source_record']['boundary_controls_Msun_pc2'],
 'shared_keys_equal_v002_v003':[k for k in set(r2)&set(r3) if r2[k]!=r3[k]]}
json.dump(E,open(sys.argv[1],'w'),indent=1); print(json.dumps(E,indent=1)[:3000])
