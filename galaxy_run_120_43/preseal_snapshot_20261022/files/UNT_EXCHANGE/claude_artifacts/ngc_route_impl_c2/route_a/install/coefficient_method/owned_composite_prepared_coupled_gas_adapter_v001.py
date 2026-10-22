"""Inert thin binding to root/Claude 0424's explicit fixed-source API.
No solver implementation, source averaging, parameter defaults or auto-launch.
"""
import hashlib
import inspect
from pathlib import Path


def solve_prepared(*, prepared, solver_module, accepted_solver_sha256,
                   preparation_file, accepted_preparation_sha256,
                   c_m_s, max_iterations, relaxation, source_atol_J, source_rtol,
                   reality_atol, reality_rtol, checkpoint, progress_callback=None):
    """Use a reviewed prep dictionary and an explicitly accepted 0424 solver.

    checkpoint is an explicit None or existing checkpoint configuration. Its
    caller identity is extended, without mutating the caller, to bind this join.
    The complete solver result is returned unchanged (including failures).
    """
    def pin(path, expected):
        path = Path(path).resolve()
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError('Accepted source pin mismatch: '+str(path))
        return {'path': str(path), 'sha256': actual}

    solver_pin = pin(solver_module.__file__, accepted_solver_sha256)
    prep_pin = pin(preparation_file, accepted_preparation_sha256)
    if 'fixed_source_fourier_J' not in inspect.signature(solver_module.solve).parameters:
        raise ValueError('0424 fixed-source interface not available; no fallback')
    if prepared['analytic_initial_azimuth'] is not True or prepared['fixed_source_fourier_J'] is None:
        raise ValueError('Actual analytic initial-source preparation required')
    if prepared['composite_grid_spec'] is None:
        raise ValueError('Explicit composite grid required')
    # Module and data pins are verified before handing arrays to the solver.
    for path, expected in prepared['source_pins'].items():
        pin(path, expected)
    custody = dict(adapter=pin(__file__, hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
        solver=solver_pin, preparation=prep_pin,
        source_pins=dict(prepared['source_pins']),
        composite_grid_spec=prepared['composite_grid_spec'],
        grid_description=prepared['grid_description'],
        quadrature_weight_sum=prepared['quadrature_weight_sum'],
        quadrature_weight_sum_expected=prepared['quadrature_weight_sum_expected'],
        bessel_custody=prepared['bessel_custody'],
        source_convention='analytic fixed stars and thin-HI initialization only; updated gas retains actual phi columns')
    ck = None
    if checkpoint is not None:
        ck = dict(checkpoint)
        identity = dict(ck['caller_identity'])
        if 'composite_source_binding' in identity:
            raise ValueError('Composite source identity already assigned')
        identity['composite_source_binding'] = custody
        ck['caller_identity'] = identity
    mods = prepared['modules']
    # In particular source_module remains the ordinary Cartesian Fourier source
    # transform. Only the solver's FIXED term uses the analytic override.
    result = solver_module.solve(
        fixed_positions_m=prepared['fixed_positions_m'],
        fixed_integrated_columns_J=prepared['fixed_integrated_columns_J'],
        fixed_source_fourier_J=prepared['fixed_source_fourier_J'],
        initial_gas_fourier_J=prepared['initial_gas_fourier_J'],
        gas_columns=prepared['gas_columns'],
        fourier_arguments=prepared['fourier_arguments'],
        boundary_jet_at_positions=prepared['boundary'],
        source_module=mods['source'], fourier_module=mods['fourier'],
        metric_module=mods['metric'], hi_module=mods['hi'],
        quadrature_module=mods['quadrature'],
        vertical_fourier_module=mods['vertical_line'],
        c_m_s=c_m_s, max_iterations=max_iterations, relaxation=relaxation,
        source_atol_J=source_atol_J, source_rtol=source_rtol,
        reality_atol=reality_atol, reality_rtol=reality_rtol,
        checkpoint=ck, progress_callback=progress_callback)
    return {'result': result, 'binding_custody': custody}
