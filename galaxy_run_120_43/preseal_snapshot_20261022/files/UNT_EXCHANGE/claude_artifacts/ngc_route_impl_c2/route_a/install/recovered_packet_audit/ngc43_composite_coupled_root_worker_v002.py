"""Root-only inert NGC43 CLI binding of accepted composite/0424 full gas trial.
No launch or physical defaults. Large known Fourier arrays saved as immutable NPZ.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import time
import numpy as np

H=Path(__file__).resolve().parent
O=H.parent/'coefficient_method'
LOCAL={
 'prep':(H/'ngc_actual_initial_source_preparation_v001.py','c54c7cc995f0bb59bb5d81a3f1267dba5dae48d116302c9c0438fe7e5a53710f'),
 'binding':(H/'ngc_composite_full_coupled_binding_v002.py','cc5db369a8e4e50aa3a1fa32ab0713b0c0c3a7be5ead2935554c4b02a438f130'),
 'composite':(O/'owned_composite_prepared_coupled_gas_adapter_v001.py','75092cf64cf5293d9e1a5b28b2c909d875c1f5a1b3e9d185f71f065ccff49ec3'),
 'stream':(O/'owned_streamed_fourier_per_run_adapter_v001.py','cbbc4b968fc189440ddd4f516fb53f07d04a97b638fdf90fd90f50422afb928e'),
 'base':(H/'owned_physical_fourier_metric_quadrature_v005.py','7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491'),
 'prediction':(O/'galaxy_coupled_fourier_hi_prediction_v005.py','54136c71403c90b82f5b150672bf218577bf837c345798ec5f770adf31ba8c72')}
SCOPE=('Target-free NGC43 provisional circular trial, not admitted calibration or scored predictions. '
 'HI sigma0=11 km/s and Gamma=5/3 are adopted preparation assumptions, not measured NGC gas dynamics; '
 'H2 uses stellar-height proxy, linear detected centers/constant core and matched infinite exponential extrapolation. '
 '72-degree source/73-degree released-mean projection is a counted reference approximation, not per-ring geometry. '
 'Missing components remain a wider family; failed native mixing and source/flow/convergence limitations retained.')
ARRAY_KEYS={'wavevectors','weighted_responses','metric_source_fourier_J',
 'reconstructed_gas_fourier_J','last_metric_source_fourier_J','last_gas_fourier_J',
 'gas_fourier_J','current_source_fourier_J','fixed_source_fourier_J'}


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
    p.add_argument('--start-iteration',type=int,required=True)
    a=p.parse_args()
    if a.start_iteration<0 or (not a.resume and a.start_iteration!=0): raise ValueError('Explicit actual restart iteration required')
    paths=dict(LOCAL,solver=(Path(a.solver),a.solver_sha256),checkpoint=(Path(a.checkpoint_module),a.checkpoint_module_sha256))
    pins={}
    for path,expected in list(paths.values())+[(Path(a.seed),a.seed_sha256)]:
        path=path.resolve()
        if sha(path)!=expected: raise ValueError('Input pin mismatch: '+str(path))
        pins[str(path)]=expected
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
        start_iteration=a.start_iteration,scope=SCOPE))
    mods={}
    try:
        for name,(path,_) in paths.items():
            spec=importlib.util.spec_from_file_location('root_composite_'+name,path)
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);mods[name]=module
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
                node_log_directory=out/'node_diagnostics',start_iteration=a.start_iteration,progress_callback=progress)
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
