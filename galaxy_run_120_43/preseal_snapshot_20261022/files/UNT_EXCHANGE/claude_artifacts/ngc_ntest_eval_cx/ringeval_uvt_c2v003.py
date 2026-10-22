"""Design §3.8 CLI: GRID LABEL RS RE --tail-config CFG --tail-sha SHA [--z95] [--store-kept].
Output defaults to an exclusive file inside this build's out/. Only registered saved-operator cases allowed.
"""
import argparse,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ngc_ring_tail_ctx_c2v001 as L
import ngc_ring_tail_ctx_c2v002 as B
import ngc_ring_tail_ctx_c2v003 as P

def main(mask='cube'):
    ap=argparse.ArgumentParser();ap.add_argument('grid');ap.add_argument('label');ap.add_argument('start',type=int);ap.add_argument('end',type=int)
    ap.add_argument('--tail-config',required=True);ap.add_argument('--tail-sha',required=True)
    ap.add_argument('--z95',action='store_true');ap.add_argument('--store-kept',action='store_true');ap.add_argument('--output')
    a=ap.parse_args()
    if (a.grid,a.label)!=('T120L','hovr') or not 0<=a.start<a.end<=156:raise ValueError('UNREGISTERED_ROSTER')
    path=Path(a.tail_config)
    if not path.resolve().is_relative_to(L.HERE):raise ValueError('CONFIG_PATH_SCOPE')
    if L.sha(path)!=a.tail_sha:raise ValueError('CONFIG_HASH')
    U,_,_=L.modules();raw=json.loads(path.read_text());cfg=U.normalize_config(raw)
    big=cfg['outer'].get('K_big_inverse_kpc');fine=cfg['quadrature']['order']==12
    if big not in (2.,8.,16.,32.) or cfg!=L.config(U,big,fine):raise ValueError('UNREGISTERED_CONFIG')
    name=a.output or f'out/{mask}_K{big:g}_{cfg["sha256"][:12]}_{a.start:03d}_{a.end:03d}.json'
    if (L.HERE/name).exists() or not (L.HERE/name).resolve().is_relative_to(L.HERE):raise ValueError('OUTPUT_REFUSED')
    built,cols=B.ctx_with_tail(big,mask,fine)
    _,_,ctx=P.ctx_with_tail('T120L','hovr',built.tail,mask)
    zs=L.ZK if a.z95 else L.ZK[:7];rows=[]
    for o in range(a.start,a.end):
        row=dict(ordinal=o,R_kpc=cols[32*o]['R_m']/L.KPC,lnN=[])
        if a.store_kept:row['kept_delta_n']=[]
        for j in range(32):
            col=cols[32*o+j];R=col['R_m'];phi=col['phi']
            row['lnN'].append([ctx.lnN(R,phi,z*L.KPC) for z in zs])
            if a.store_kept:row['kept_delta_n'].append([ctx.kept_delta_n(R,phi,z*L.KPC) for z in zs])
        rows.append(row);print('ring',o,flush=True)
    rec=dict(schema='NGC_RING_UVT_C2V001',label='TESTED',operator_sha256=L.OP_SHA,kbig=big,shape=mask,doubled=fine,
        z_kpc=list(zs),azimuths=32,rows=rows,tail_record=ctx.tail.record,tail_digest=ctx.tail.digest,
        memory_cap_override=B.OVERRIDE,config_file=dict(path=str(path),sha256=a.tail_sha),stored_kept=a.store_kept)
    print(L.write(name,rec),flush=True)
if __name__=='__main__':main()
