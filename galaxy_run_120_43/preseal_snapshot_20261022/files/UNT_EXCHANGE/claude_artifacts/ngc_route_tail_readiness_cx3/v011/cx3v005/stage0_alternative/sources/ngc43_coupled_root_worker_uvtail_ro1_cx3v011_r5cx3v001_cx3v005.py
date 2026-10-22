"""Root-only inert NGC43 CLI binding of accepted composite/0424 full gas trial.
No launch or physical defaults. Large known Fourier arrays saved as immutable NPZ.
UVTAIL c2v001 (Claude2 tail_scheme_impl_c2/route_a; successor of 42bdd23e; TAIL_SCHEME_DESIGN_V002 sec 3.5, R1 IA6):
RO1 c2v001 (Claude2 ro1_readout_c2; successor of 5a330089; ROOT_DECISIONS V004 ADDENDUM A42.2): LOCAL binding -> the RO1
binding successor (post-convergence circular-trial readout refusal record); nothing else changes.
RO1 c2v002 (successor of the RO1 c2v001 worker 856de207; ROOT_DECISIONS V005 ADDENDUM A49.1): LOCAL binding -> the RO1 c2v002
binding (message set adds DEGENERATE_RADIAL_EULER); nothing else changes.
required --uv-tail-config/-sha256 (UNT_UV_TAIL_ROUTE_A_REQUEST_C2V001 JSON), --eps-certificate/-sha256 and
--lo-certificate/-sha256 (must equal the request's certificate entries, or NONE_TEST_ONLY for both), and
--uv-tail-sidecar-directory. uv_tail.enabled false -> the binding gets uv_tail=None (reviewed statements).
LOCAL binding -> the uvtail successor; the controller and module-lane library files are pinned (UVT).
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import time
import numpy as np

H=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_impl_c2/route_a/install/recovered_packet_audit')
O=H.parent/'coefficient_method'
LOCAL={
 'prep':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/sources/ngc_actual_initial_source_preparation_cx3v011_cx3v005.py'),'d578889248f0e2f7a40ded8c6645a14811ac8ba59c192e4e6ef243dde06db5f8'),
 'binding':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/route_a/ngc_composite_full_coupled_binding_uvtail_ro1_cx3v011.py'),'9b5ce82adea46c8e660f44b0fc91e8dbe5d0616cc1de1fd4467878ef3b5c0668'),  # RO1 c2v002 successor of 06a1ba9c
 'composite':(O/'owned_composite_prepared_coupled_gas_adapter_v001.py','75092cf64cf5293d9e1a5b28b2c909d875c1f5a1b3e9d185f71f065ccff49ec3'),
 'stream':(O/'owned_streamed_fourier_per_run_adapter_v001.py','cbbc4b968fc189440ddd4f516fb53f07d04a97b638fdf90fd90f50422afb928e'),
 'base':(H/'owned_physical_fourier_metric_quadrature_v005.py','7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491'),
 'prediction':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/route_a/ngc_coupled_fourier_hi_prediction_cx3v011.py'),'7ae28901023974005fac9a5dc4126941371b1522837b02c81cdb5811573c1e98')}
SCOPE=('Target-free NGC43 provisional circular trial, not admitted calibration or scored predictions. '
 'HI sigma0=11 km/s and Gamma=5/3 are adopted preparation assumptions, not measured NGC gas dynamics; '
 'H2 uses stellar-height proxy, linear detected centers/constant core and matched infinite exponential extrapolation. '
 '72-degree source/73-degree released-mean projection is a counted reference approximation, not per-ring geometry. '
 'Missing components remain a wider family; failed native mixing and source/flow/convergence limitations retained.')
ARRAY_KEYS={'wavevectors','weighted_responses','metric_source_fourier_J',
 'reconstructed_gas_fourier_J','last_metric_source_fourier_J','last_gas_fourier_J',
 'gas_fourier_J','current_source_fourier_J','fixed_source_fourier_J'}

# UVTAIL c2v001: tail controller + module-lane library (sha256 from bytes; the controller's PINS must agree).
UVT={'uvt_controller':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001_r5.py'),'c5bdd0553968e3f00b61db89f7944cebe51166006f58b727a7aed2a9b6a434fc'),
 'uvt_lib':(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py'),'2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
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
    p.add_argument('--start-iteration',type=int,required=True)
    a=p.parse_args()
    if a.start_iteration<0 or (not a.resume and a.start_iteration!=0): raise ValueError('Explicit actual restart iteration required')
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
    tolerance=seed['numerical_inputs']['h2_tail_mass_rtol']
    if isinstance(tolerance,bool) or not isinstance(tolerance,(float,int)) or not math.isfinite(tolerance) or tolerance<=0:
        raise ValueError('Explicit positive finite seed h2_tail_mass_rtol required')
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
        start_iteration=a.start_iteration,uv_tail=uv_record,scope=SCOPE))
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
                solver_module=mods['solver'],accepted_solver_sha256=a.solver_sha256,
                composite_adapter=mods['composite'],streaming_adapter=mods['stream'],streaming_base=mods['base'],
                prediction_module=mods['prediction'],accepted_module_pins=pins,checkpoint=ck,
                node_log_directory=out/'node_diagnostics',start_iteration=a.start_iteration,progress_callback=progress,
                uv_tail=None if not uv_cfg['enabled'] else dict(controller_module=mods['uvt_controller'],request=uv_request,
                    sidecar_directory=Path(a.uv_tail_sidecar_directory)))
        save('result.json',dict(result=result,seed_pin=a.seed_sha256,input_pins=pins,
            elapsed_seconds=time.monotonic()-started,accepted_for_calibration=False,scope=SCOPE))
        save('finish.json',dict(status='RETURNED_ACTUAL_RESULT',elapsed_seconds=time.monotonic()-started,
            result_path=str((out/'result.json').resolve()),result_sha256=sha(out/'result.json')))
    except Exception as exc:
        save('failure.json',dict(status='FAILED',type=type(exc).__name__,message=str(exc),
            elapsed_seconds=time.monotonic()-started,input_pins=pins,
            scope='Already committed progress arrays and genuine checkpoint retained; no replacement result.'))
        raise

if __name__=='__main__': main()
