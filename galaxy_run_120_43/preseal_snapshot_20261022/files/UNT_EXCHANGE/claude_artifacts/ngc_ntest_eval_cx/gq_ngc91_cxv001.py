"""0546 target-free NGC gas transform check at M_s96 versus192 to91/kpc. No operator solve.
Uses exact AST function bodies from pinned GQ certificate sources; no DDO source reads.
"""
import ast,hashlib,json,math,sys,time,types
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
import ngc_ring_tail_ctx_c2v005 as L
P=L.ART/'tail_scheme_impl_c2'
def extract(path,digest,names,namespace):
 raw=path.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('GQ_SOURCE_PIN')
 tree=ast.parse(raw);nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in names]
 if {x.name for x in nodes}!=set(names):raise ValueError('FUNCTION_SET')
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),namespace)
 return {'path':str(path),'sha256':digest}
if __name__=='__main__':
 L.env();ns={'np':np,'math':math,'time':time}
 p1=extract(P/'certificates_v001/tools/gq_cert_c2v001.py','806eb23c5daec645ac77e57925ad3f6e34fb001f2c9b18bd197c7a07df285f22',('clone_gas','sample_nodes'),ns)
 ns['G1']=types.SimpleNamespace(clone_gas=ns['clone_gas'],sample_nodes=ns['sample_nodes'])
 p2=extract(P/'certificates_v002/tools/gq_cert_c2v002.py','ffbe4e2e1d797712c337f46833626ef00744d0481d14988fe976856a819bfd46',('gq_roster2',),ns)
 U,RS,PV=L.modules();ros=L.source(RS);cert=L.certificates();jn=PV.create_provider()
 provenance={'operator_sha256':L.OP_SHA,'i1t_record':{'path':str(L.CERT/'I1T_NGC_T120L_V001.json'),'sha256':L.sha(L.CERT/'I1T_NGC_T120L_V001.json')},'scope':'NGC saved initial-gas roster only'}
 row=ns['gq_roster2'](U,RS,jn,ros.gas,96,2.,91.,{'order':8,'w_perp_max_inverse_kpc':.005,'w_z_max_inverse_kpc':.007},136.5,'NGC_T120L',provenance)
 ok=row['max_abs_diff_over_P0']<=1e-12 and row['all_kperp_nodes_bound_over_P0']<=1e-12
 out={'label':'TESTED','gate':'GQ_NGC','schema':'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002','verdict':'PASS' if ok else 'FAIL','rosters':[row],'coverage_inverse_kpc':{'NGC':[2,91]},'threshold_over_P0':1e-12,'producer':{'path':str(Path(__file__).resolve()),'sha256':L.sha(__file__),'version':Path(__file__).stem},'function_sources':[p1,p2],'note':'4096 seeded nodes and conservative bound at every radial grid node; absolute P0 criterion; no target velocities'}
 print(L.write('out/GQ_NGC_91_MS96_V001.json',out),flush=True)
