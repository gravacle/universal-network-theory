"""Per-attempt streaming facade over reviewed Fourier V005, no numerics changed.
Use a NEW log directory on every resumed attempt; start_iteration is the actual
checkpoint restart iteration. Log locations never enter the prepared dictionary.
"""
import hashlib
import json
from pathlib import Path
import types
import numpy as np

BASE_SHA256='7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491'


def make_fourier_module(*, base_module, log_directory, start_iteration):
    """Return actual ModuleType with __file__ for checkpoint _module_pin.

    Replace prepared['modules']['fourier'] explicitly with this facade and merge
    facade.source_pins into prepared['source_pins'] before calling the reviewed
    composite-source adaptor. Retain its original V004 pin as historical custody.
    This factory is per-run; it neither mutates base nor shares a global counter.
    Root pins THIS file independently. The embedded base pin is checked here.
    No callback is inserted in fourier_arguments/checkpoint's serializable input.
    """
    if type(start_iteration)is not int or start_iteration<0:
        raise ValueError('Explicit nonnegative checkpoint iteration required')
    base_path=Path(base_module.__file__).resolve()
    if hashlib.sha256(base_path.read_bytes()).hexdigest()!=BASE_SHA256:
        raise ValueError('Reviewed Fourier V005 base pin mismatch')
    own_path=Path(__file__).resolve()
    pins={str(own_path):hashlib.sha256(own_path.read_bytes()).hexdigest(),str(base_path):BASE_SHA256}
    directory=Path(log_directory);directory.mkdir(exist_ok=False)
    with (directory/'custody.json').open('x') as f:
        json.dump(dict(source_pins=pins,start_iteration=start_iteration,
            scope='One exclusive node log per prepare/iteration; new directory for each resume attempt. Prepared metadata excludes attempt paths.'),f,allow_nan=False)
        f.flush()
    iteration=start_iteration
    def serial(v):
        if isinstance(v,np.ndarray): return serial(v.tolist())
        if isinstance(v,np.generic): return serial(v.item())
        if isinstance(v,complex): return dict(real=v.real,imag=v.imag)
        if isinstance(v,dict): return {str(k):serial(x) for k,x in v.items()}
        if isinstance(v,(list,tuple)): return [serial(x) for x in v]
        return v
    def prepare(**arguments):
        nonlocal iteration
        if 'node_diagnostic_callback' in arguments or 'retain_node_diagnostics' in arguments:
            raise ValueError('Streaming policy is fixed by this explicit adapter')
        index=iteration;iteration+=1
        path=directory/('iteration_%06d_nodes.jsonl'%index)
        count=0
        try:
            with path.open('x') as stream:
                def emit(record):
                    nonlocal count
                    stream.write(json.dumps(serial(record),allow_nan=False,separators=(',',':'))+'\n')
                    stream.flush();count+=1
                prepared=base_module.prepare(**arguments,node_diagnostic_callback=emit,
                    retain_node_diagnostics=False)
            # Exactly the base returned dictionary: no attempt/path/time metadata
            # can make a restored checkpoint's prepared digest differ.
            with (directory/('iteration_%06d_complete.json'%index)).open('x') as f:
                json.dump(dict(iteration=index,node_records=count,node_log=path.name),f,allow_nan=False);f.flush()
            return prepared
        except Exception as exc:
            with (directory/('iteration_%06d_failure.json'%index)).open('x') as f:
                json.dump(dict(iteration=index,node_records=count,type=type(exc).__name__,message=str(exc)),f,allow_nan=False);f.flush()
            raise
    def evaluate_prepared(**arguments):
        return base_module.evaluate_prepared(**arguments)
    def evaluate(*,physical_positions,boundary_fields,boundary_gradient,boundary_hessian,**arguments):
        return evaluate_prepared(prepared=prepare(**arguments),physical_positions=physical_positions,
            boundary_fields=boundary_fields,boundary_gradient=boundary_gradient,boundary_hessian=boundary_hessian)
    module=types.ModuleType('owned_streamed_fourier_per_run_adapter_v001')
    module.__file__=str(own_path)
    module.prepare=prepare;module.evaluate_prepared=evaluate_prepared;module.evaluate=evaluate
    module.source_pins=pins
    return module
