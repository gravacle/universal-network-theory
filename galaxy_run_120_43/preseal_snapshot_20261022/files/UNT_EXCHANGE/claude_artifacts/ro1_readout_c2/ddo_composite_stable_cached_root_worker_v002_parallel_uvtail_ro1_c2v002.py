"""Root-only inert CLI binding of accepted composite/0424 full gas trial.
No launch or physical defaults. Large known Fourier arrays saved as immutable NPZ.
PARALLEL c2v001: adds required --column-workers N (solver bind_column_workers view);
LOCAL paths made absolute because this successor lives outside the reviewed tree.
UVTAIL c2v001 (Claude2 tail_scheme_impl_c2/route_a; successor of 9dbdaf11; TAIL_SCHEME_DESIGN_V002 sec 3.5, R1 IA6):
RO1 c2v001 (Claude2 ro1_readout_c2; successor of dac9efcb; ROOT_DECISIONS V004 ADDENDUM A42.2): LOCAL binding -> the RO1
binding successor (post-convergence circular-trial readout refusal record); nothing else changes.
RO1 c2v002 (successor of the RO1 c2v001 worker 867d2c87; ROOT_DECISIONS V005 ADDENDUM A49.1): LOCAL binding -> the RO1 c2v002
binding (message set adds DEGENERATE_RADIAL_EULER); nothing else changes.
required --uv-tail-config/-sha256 (UNT_UV_TAIL_ROUTE_A_REQUEST_C2V001 JSON), --eps-certificate/-sha256 and
--lo-certificate/-sha256 (must equal the request's certificate entries, or NONE_TEST_ONLY for both), and
--uv-tail-sidecar-directory. uv_tail.enabled false -> the binding gets uv_tail=None (reviewed statements).
LOCAL binding and stable_adapter (facade) -> the uvtail successors; the controller and module-lane library files are pinned (UVT).
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time
import numpy as np

H=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit')
O=H.parent/'coefficient_method'
LOCAL={
 'stable_adapter':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/owned_stable_lapse_hi_facade_uvtail_c2v001.py'),'191fb7bd91708b6aae9fdc21d1bf81c01482374ae5b6f80cbaad5a9a8438af9c'),  # UVTAIL successor of 2caca496
 'stable_line':(H/'owned_fixed_xy_fourier_line_v002.py','3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18'),
 'stable_hi':(H/'hi_two_sided_free_boundary_v003.py','b176c7a604079027cbca565aae81d0ec69ea9b3f47430d7e58c03cd21a7838f9'),
 'prep':(O/'ddo_actual_initial_source_preparation_v007.py','ac905597b1aa06da3a0178bfa629f6256b78cc87e8b1b05fcea22b3f6df25a42'),
 'binding':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py'),'86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885'),  # RO1 c2v002 successor of a28ee6ff
 'composite':(O/'owned_composite_prepared_coupled_gas_adapter_v001.py','75092cf64cf5293d9e1a5b28b2c909d875c1f5a1b3e9d185f71f065ccff49ec3'),
 'stream':(H/'owned_scalar_lapse_inverse_cache_v001.py','7b9816aea218d638c2eece184df22e29ca18b68547f3d04193780c2eff96a529'),
 'base':(H/'owned_physical_fourier_metric_quadrature_v005.py','7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491'),
 'prediction':(O/'galaxy_coupled_fourier_hi_prediction_v005.py','54136c71403c90b82f5b150672bf218577bf837c345798ec5f770adf31ba8c72')}
ARRAY_KEYS={'wavevectors','weighted_responses','metric_source_fourier_J',
 'reconstructed_gas_fourier_J','last_metric_source_fourier_J','last_gas_fourier_J',
 'gas_fourier_J','current_source_fourier_J','fixed_source_fourier_J'}

# UVTAIL c2v001: tail controller + module-lane library (sha256 from bytes; the controller's PINS must agree).
UVT={'uvt_controller':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001.py'),'51d32e7b2b8c83c7544c24d64ea3161007fbec35769a64a869972efac055cb68'),
 'uvt_lib':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/owned_uv_tail_lapse_v001.py'),'c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22'),
 'uvt_roster':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/uv_tail_source_roster_c2v001.py'),'4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'),
 'uvt_provider':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/module/posix_libm_bessel_jn_provider_c2v001.py'),'d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171')}
UVT_FLAGS=('uv-tail-config','uv-tail-config-sha256','eps-certificate','eps-certificate-sha256','lo-certificate',
 'lo-certificate-sha256','uv-tail-sidecar-directory')


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('seed','seed-sha256','solver','solver-sha256','checkpoint-module','checkpoint-module-sha256','outdir','checkpoint-directory'):
        p.add_argument('--'+name,required=True)
    p.add_argument('--resume',action='store_true')
    for name in UVT_FLAGS: p.add_argument('--'+name,required=True)  # UVTAIL
    p.add_argument('--column-workers',type=int,required=True)
    p.add_argument('--start-iteration',type=int,required=True)
    a=p.parse_args()
    if a.start_iteration<0 or (not a.resume and a.start_iteration!=0): raise ValueError('Explicit actual restart iteration required')
    if not 1<=a.column_workers<=64: raise ValueError('Explicit column worker count 1..64 required')
    paths=dict(LOCAL,solver=(Path(a.solver),a.solver_sha256),checkpoint=(Path(a.checkpoint_module),a.checkpoint_module_sha256),uvt_controller=UVT['uvt_controller'])
    pins={}
    for path,expected in list(paths.values())+[(Path(a.seed),a.seed_sha256)]:
        path=path.resolve()
        if sha(path)!=expected: raise ValueError('Input pin mismatch: '+str(path))
        pins[str(path)]=expected
    # UVTAIL: library pins, the request bytes, and the certificate flags against the request (before any work).
    for name in ('uvt_lib','uvt_roster','uvt_provider'):
        path,expected=UVT[name];path=path.resolve()
        if sha(path)!=expected: raise ValueError('Input pin mismatch: '+str(path))
        pins[str(path)]=expected
    if sha(a.uv_tail_config)!=a.uv_tail_config_sha256: raise ValueError('Input pin mismatch: '+str(Path(a.uv_tail_config).resolve()))
    pins[str(Path(a.uv_tail_config).resolve())]=a.uv_tail_config_sha256
    uv_request=json.loads(Path(a.uv_tail_config).read_text())
    uv_cfg=uv_request.get('uv_tail') if isinstance(uv_request,dict) else None
    if not isinstance(uv_cfg,dict) or type(uv_cfg.get('enabled')) is not bool: raise ValueError('UV-tail request with boolean uv_tail.enabled required')
    for flag in ('eps_certificate','lo_certificate'):
        given=(getattr(a,flag),getattr(a,flag+'_sha256'));c=uv_cfg.get(flag)
        declared=('NONE_TEST_ONLY','NONE_TEST_ONLY') if c=='NONE_TEST_ONLY' else (c.get('path'),c.get('sha256')) if isinstance(c,dict) else None
        if given!=declared: raise ValueError('UV-tail '+flag+' flags differ from the request')
        if given[0]!='NONE_TEST_ONLY':
            if sha(given[0])!=given[1]: raise ValueError('Input pin mismatch: '+str(Path(given[0]).resolve()))
            pins[str(Path(given[0]).resolve())]=given[1]
    uv_record=dict(request={'path':str(Path(a.uv_tail_config).resolve()),'sha256':a.uv_tail_config_sha256},
        enabled=uv_cfg['enabled'],sidecar_directory=str(Path(a.uv_tail_sidecar_directory).resolve()))
    seed=json.loads(Path(a.seed).read_text())
    for path,expected in seed['pins'].items():
        if sha(path)!=expected: raise ValueError('Seed provenance mismatch: '+path)
    # Validate required physical seed coordinates before expensive preparation.
    ni=seed['numerical_inputs']
    physical_parameters={k:ni[k] for k in ('Eref_J','ell_F_m','gamma','solar_mass_kg','kpc_m')}
    numerical_controls={k:v for k,v in ni.items() if k!='progress_directory'}
    numerical_controls['uv_tail']=uv_record  # UVTAIL
    out=Path(a.outdir);out.mkdir(exist_ok=False)
    blobs=out/'arrays';blobs.mkdir()
    sequence=0
    def encode(value,key=None):
        nonlocal sequence
        if isinstance(value,np.ndarray):
            if key in ARRAY_KEYS:
                name='%06d_%s.npz'%(sequence,key);sequence+=1
                path=blobs/name
                with path.open('xb') as f: np.savez(f,array=value);f.flush()
                return {'array_file':str(path.resolve()),'sha256':sha(path),'member':'array',
                        'shape':list(value.shape),'dtype':value.dtype.str,'format':'numpy_npz_no_pickle'}
            if value.size>100000: raise ValueError('Unclassified large result array: '+str(key))
            return encode(value.tolist())
        if isinstance(value,np.generic): return encode(value.item())
        if isinstance(value,complex): return {'real':value.real,'imag':value.imag}
        if isinstance(value,dict): return {str(k):encode(v,str(k)) for k,v in value.items()}
        if isinstance(value,(list,tuple)): return [encode(v) for v in value]
        return value
    def save(name,value):
        record=encode(value)
        with (out/name).open('x') as f: json.dump(record,f,allow_nan=False,separators=(',',':'));f.flush()
    started=time.monotonic()
    save('start.json',dict(seed=seed,input_pins=pins,worker_pin=sha(__file__),
        checkpoint_directory=str(Path(a.checkpoint_directory).resolve()),resume=a.resume,
        start_iteration=a.start_iteration,uv_tail=uv_record,column_workers=a.column_workers,scope='Root-selected provisional candidate; no calibration or convergence asserted.'))
    mods={}
    try:
        for name,(path,_) in paths.items():
            spec=importlib.util.spec_from_file_location('root_composite_'+name,path)
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);mods[name]=module
        if {k:(str(p),s) for k,(p,s) in mods['uvt_controller'].PINS.items()}!={k:(str(UVT['uvt_'+k][0]),UVT['uvt_'+k][1]) for k in ('lib','roster','provider')}:
            raise ValueError('UV-tail controller library pins differ from this worker')  # UVTAIL
        with (out/'progress.jsonl').open('x') as log:
            def progress(event):
                # Array content durable before its JSON reference is committed.
                record=encode(event);record['elapsed_seconds']=time.monotonic()-started
                log.write(json.dumps(record,allow_nan=False,separators=(',',':'))+'\n');log.flush()
            ck=dict(module=mods['checkpoint'],directory=a.checkpoint_directory,
                mode='resume' if a.resume else 'new',caller_identity=dict(
                    seed={'path':str(Path(a.seed).resolve()),'sha256':a.seed_sha256},
                    code_pins=pins,physical_parameters=physical_parameters,
                    numerical_controls=numerical_controls,worker={'path':str(Path(__file__).resolve()),'sha256':sha(__file__)},
                    boundary_prescription='Reviewed prep boundary perturbations unchanged; N=1,Cbar restored once.'))
            result=mods['binding'].evaluate(prep_module=mods['prep'],prep_arguments=seed['numerical_inputs'],
                solver_module=mods['solver'].bind_column_workers(a.column_workers),accepted_solver_sha256=a.solver_sha256,
                composite_adapter=mods['composite'],streaming_adapter=mods['stream'],streaming_base=mods['base'],
                prediction_module=mods['prediction'],stable_adapter=mods['stable_adapter'],
                stable_line_module=mods['stable_line'],stable_hi_module=mods['stable_hi'],
                accepted_module_pins=pins,checkpoint=ck,
                node_log_directory=out/'node_diagnostics',start_iteration=a.start_iteration,progress_callback=progress,
                uv_tail=None if not uv_cfg['enabled'] else dict(controller_module=mods['uvt_controller'],request=uv_request,
                    sidecar_directory=Path(a.uv_tail_sidecar_directory)))
        save('result.json',dict(result=result,seed_pin=a.seed_sha256,input_pins=pins,
            elapsed_seconds=time.monotonic()-started,accepted_for_calibration=False))
        save('finish.json',dict(status='RETURNED_ACTUAL_RESULT',elapsed_seconds=time.monotonic()-started,
            result_path=str((out/'result.json').resolve()),result_sha256=sha(out/'result.json')))
    except Exception as exc:
        save('failure.json',dict(status='FAILED',type=type(exc).__name__,message=str(exc),
            elapsed_seconds=time.monotonic()-started,input_pins=pins,
            scope='Already committed progress arrays and genuine checkpoint retained; no replacement result.'))
        raise

if __name__=='__main__': main()
