"""Future-only all-43 formatter. No metric, baseline model or observation is evaluated.

The caller supplies parsed saved baseline JSON, explicit field paths, 43 revised
velocities and their interval flags, provenance and admission status. This module
does not load/publish files, import producers, select an observer or qualify data.
"""
import json
import math
import statistics

AUTHOR_DRAFT = True


def report43_path(value, keys):
    assert isinstance(keys, (list, tuple)) and all(isinstance(k, (str, int)) for k in keys)
    for key in keys:
        value = value[key]
    return value


def report43_number(value, optional=False):
    if optional and value is None:
        return None
    assert type(value) in (int, float) and math.isfinite(value)
    return float(value)


def report43_statistics(rows, family):
    values = [row[family] for row in rows]
    missing = [i for i, value in enumerate(values) if value['velocity_kms'] is None]
    if missing:
        return dict(rows=43, valid_rows=43-len(missing), invalid_indices=missing,
                    all43_statistics=None, reason='All-43 statistics withheld; missing values are retained.')
    residual = [value['residual_kms'] for value in values]
    standardized = [value['residual_sigma'] for value in values]
    percent = [value['residual_percent'] for value in values]
    stats = dict(mean_signed_residual_kms=math.fsum(residual)/43,
                 mean_absolute_residual_kms=math.fsum(abs(x) for x in residual)/43,
                 median_absolute_residual_kms=statistics.median(abs(x) for x in residual),
                 root_mean_square_residual_kms=math.sqrt(math.fsum(x*x for x in residual)/43),
                 max_absolute_residual_kms=max(abs(x) for x in residual),
                 chi_square=math.fsum(x*x for x in standardized),
                 chi_square_per_row=math.fsum(x*x for x in standardized)/43,
                 within_measured_1sigma=sum(value['within_measured_1sigma'] for value in values),
                 median_absolute_percent=None if any(x is None for x in percent)
                 else statistics.median(abs(x) for x in percent),
                 mean_absolute_percent=None if any(x is None for x in percent)
                 else math.fsum(abs(x) for x in percent)/43)
    return dict(rows=43, valid_rows=43, invalid_indices=[], all43_statistics=stats,
                reason='Descriptive; no fit, degrees-of-freedom correction or physical acceptance gate.')


def revised_43_observer_report(baseline_document, revised_rows, *, baseline_row_path,
                               baseline_fields, provenance, admission_status, prediction_kind,
                               prediction_scope):
    """Return data+Markdown; caller owns authentic file admission and publication.

    baseline_fields maps radius/observed/sigma/model to explicit per-row key paths.
    revised_rows has R_kpc, velocity_kms (finite or None), interval_flags and note.
    Percent means 100*(model-observed)/observed; sigma is the saved measured error.
    Catalogue radius matching is exact; observer/radius mapping belongs to caller.
    """
    assert prediction_kind in ('local_metric_circular_snapshot', 'evolved_tracer', 'reduced_pipeline')
    assert isinstance(prediction_scope, dict) and prediction_scope
    assert isinstance(provenance, dict) and provenance
    assert isinstance(admission_status, dict) and admission_status
    # These are quoted supplied records, never an admission performed by this formatter.
    provenance = json.loads(json.dumps(provenance, allow_nan=False, sort_keys=True))
    admission_status = json.loads(json.dumps(admission_status, allow_nan=False, sort_keys=True))
    prediction_scope = json.loads(json.dumps(prediction_scope, allow_nan=False, sort_keys=True))
    assert set(baseline_fields) == {'radius', 'observed', 'sigma', 'model'}
    old = report43_path(baseline_document, baseline_row_path)
    assert isinstance(old, list) and isinstance(revised_rows, list) and len(old) == len(revised_rows) == 43
    rows = []
    for index, (saved, new) in enumerate(zip(old, revised_rows)):
        radius = report43_number(report43_path(saved, baseline_fields['radius']))
        observed = report43_number(report43_path(saved, baseline_fields['observed']))
        sigma = report43_number(report43_path(saved, baseline_fields['sigma']))
        assert radius > 0 and observed >= 0 and sigma > 0
        assert radius == report43_number(new['R_kpc']) and (not rows or radius > rows[-1]['R_kpc'])
        flags = new['interval_flags']
        assert isinstance(flags, dict) and all(isinstance(k, str) and k and type(v) is bool for k,v in flags.items())
        assert isinstance(new['note'], str)
        row = dict(index=index, R_kpc=radius, Vobs_kms=observed, measured_sigma_kms=sigma,
                   measured_interval_1sigma_kms=[observed-sigma, observed+sigma],
                   interval_flags=dict(flags), note=new['note'])
        velocities = (report43_number(report43_path(saved, baseline_fields['model']), optional=True),
                      report43_number(new['velocity_kms'], optional=True))
        for family, velocity in zip(('old', 'new'), velocities):
            delta = None if velocity is None else velocity-observed
            row[family] = dict(velocity_kms=velocity, residual_kms=delta,
                               residual_percent=None if delta is None or observed == 0 else 100*delta/observed,
                               residual_sigma=None if delta is None else delta/sigma,
                               within_measured_1sigma=None if delta is None else abs(delta) <= sigma)
        row['new_minus_old_velocity_kms'] = None if any(v is None for v in velocities) else velocities[1]-velocities[0]
        row['change_in_absolute_residual_kms'] = None if any(v is None for v in velocities) else abs(row['new']['residual_kms'])-abs(row['old']['residual_kms'])
        rows.append(row)
    summary = {family: report43_statistics(rows, family) for family in ('old', 'new')}
    changes = None
    if all(summary[family]['all43_statistics'] is not None for family in ('old', 'new')):
        changes = {key: summary['new']['all43_statistics'][key]-value
                   for key, value in summary['old']['all43_statistics'].items()
                   if value is not None and summary['new']['all43_statistics'][key] is not None}
    result = dict(prediction_kind=prediction_kind, supplied_prediction_scope=prediction_scope,
                  supplied_provenance=provenance,
                  supplied_admission_status=admission_status, rows=rows, summary=summary,
                  new_minus_old_all43_statistics=changes, formatter_performed_admission=False,
                  uncertainty_scope='Saved measured sigma; no model uncertainty or covariance inferred.')
    lines = ['# Revised 43-point comparison', '', prediction_kind, '',
             'Admission status (caller supplied): ' + json.dumps(admission_status, sort_keys=True), '',
             'Prediction scope (caller supplied): ' + json.dumps(prediction_scope, sort_keys=True), '',
             'Residuals are model minus observation. Percent uses Vobs; sigma uses the saved measured error. '
             'The ±sigma interval flags and summaries are descriptive.', '',
             '| R kpc | Vobs | sigma | Old v | New v | Old delta | New delta | Old % | New % | Old sigma | New sigma | Old/New in ±sigma | Interval flags |',
             '|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|:---|']
    def fmt(value):
        return 'undefined' if value is None else format(value, '.9g')
    for row in rows:
        a,b = row['old'],row['new']
        cells = [row['R_kpc'],row['Vobs_kms'],row['measured_sigma_kms'],a['velocity_kms'],b['velocity_kms'],
                 a['residual_kms'],b['residual_kms'],a['residual_percent'],b['residual_percent'],a['residual_sigma'],b['residual_sigma']]
        within = '/'.join('undefined' if x is None else ('yes' if x else 'no') for x in (a['within_measured_1sigma'],b['within_measured_1sigma']))
        flags = ', '.join(k+'='+str(v).lower() for k,v in sorted(row['interval_flags'].items())) or '(none supplied)'
        flags = flags.replace('|','\\|').replace('\n',' ')
        lines.append('| '+' | '.join([fmt(x) for x in cells]+[within,flags])+' |')
    lines += ['', 'All-43 aggregates (JSON; no incomplete-row subset score):', '',
              '```json', json.dumps(dict(summary=summary,new_minus_old=changes), indent=2, sort_keys=True, allow_nan=False),
              '```', '', 'Supplied provenance:', '', '```json',
              json.dumps(provenance, indent=2, sort_keys=True, allow_nan=False), '```', '']
    result['markdown'] = '\n'.join(lines)
    json.dumps(result, allow_nan=False)  # Refuse nonfinite derived summary; no data substitution.
    return result
