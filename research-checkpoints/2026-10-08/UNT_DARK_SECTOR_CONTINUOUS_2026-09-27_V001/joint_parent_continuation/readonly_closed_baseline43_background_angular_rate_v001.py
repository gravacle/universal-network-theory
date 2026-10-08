"""Authorized closed-JSON exact-rational postprocessing; no producer imports/replay."""
import ast
import hashlib
import json
import resource
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'READONLY_CLOSED_BASELINE43_BACKGROUND_ANGULAR_RATE_V001_RESULT.json'
PINS = {
 'READONLY_CLOSED_BASELINE43_ANGULAR_TIMESCALES_V001_RESULT.json':'4a8aaf4206ce9ecf0bb3095da90a82843f3d368a11f9c53fb4d4c8b5d9fdcad0',
 'ROOT_DIRECT43_ORIGINAL_BASELINE_SELECTED_INPUTS_VERIFIED_V001.json':'222a7afa2f2a34b32bde77334a686fbfbfc29e2506e6ddc599d5e19d2c76cb0e',
 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00000_INPUT.npz.COMMIT.json':'6c0812bcf14a981d47769506c971dd8546f59fff05eb62d0ae6cc7db09fabdd6',
 'DIRECT43_ORIGINAL_BASELINE_PREPARATION_V003_00000_INPUT.npz.COMMIT.json':'ae9f30162e7edd1a41988dff1aa7b8cc624868247eb74a968e14a3b0b8b4b431',
 'cross_u_whole_slice_cauchy_data_v002.py':'6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7',
 'cross_u_whole_slice_q1_adm_residual_v001.py':'c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a',
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'direct43_original_baseline_preparation_v003.py':'68fff180edacd39e1d88c828201f6ea6c5018eaec78bbdd2e4bb90f4528ae336',
 'author_fragment_direct43_owned_baseline_field_law_v004.py':'99ea2904f4b699764f0e186b9cb7d05db691bb5dc91a5019ee7199bb850ce7b1',
 'author_fragment_baseline_DIRECT43_raw_jet_pair_v001.py':'07cbcd0af964ba2531c12878e629b9c58ce56bff23fa94bd5471d83162ab2dd9',
 'author_fragment_general_raw_jet_instantaneous_geodesic_v001.py':'b357de459494d9bad5bb0963ee2c3236ca8265872ebaf583062e54b03b40602b',
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8',
}

def fraction(q):
    return F(int(q['numerator']), int(q['denominator']))

def serial(q):
    if isinstance(q, F):
        return dict(numerator=str(q.numerator), denominator=str(q.denominator))
    if isinstance(q, dict):
        return {k:serial(v) for k,v in q.items()}
    if isinstance(q, (list, tuple)):
        return [serial(v) for v in q]
    return q

def display(q):
    with localcontext() as ctx:
        ctx.prec=40
        return str(Decimal(q.numerator)/Decimal(q.denominator))

def main():
    assert not OUTPUT.exists(), 'Exclusive new saved-only result required'
    content={}
    for name,digest in PINS.items():
        p=BASE/name
        assert not p.stat().st_flags & 0x40000000, 'No cloud recall in this worker'
        b=p.read_bytes()
        assert hashlib.sha256(b).hexdigest()==digest, name
        content[name]=json.loads(b) if name.endswith('.json') else b.decode()
    saved=content['READONLY_CLOSED_BASELINE43_ANGULAR_TIMESCALES_V001_RESULT.json']
    selected=content['ROOT_DIRECT43_ORIGINAL_BASELINE_SELECTED_INPUTS_VERIFIED_V001.json']
    original=content['CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00000_INPUT.npz.COMMIT.json']['metadata']
    direct=content['DIRECT43_ORIGINAL_BASELINE_PREPARATION_V003_00000_INPUT.npz.COMMIT.json']['metadata']
    assert selected['status']=='ROOT_DIRECT43_ORIGINAL_BASELINE_SELECTED_INPUTS_VERIFIED'
    assert selected['records']['reference_fields']['record']['commit_sha256']==PINS['CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_00000_INPUT.npz.COMMIT.json']
    assert original['owner']['pid']==24903 and direct['owner']['pid']==1071
    assert original['owner']['source_sha256']==PINS['cross_u_whole_slice_cauchy_data_v002.py']
    assert direct['owner']['source_sha256']==PINS['direct43_original_baseline_preparation_v003.py']
    assert original['fixed']['eps']==1e-5
    assert direct['admission']['owned_K_Hbar_uses_original_q1_operation_order'] is True
    assert direct['admission']['reference_fields_record']==selected['records']['reference_fields']['record']
    assert direct['admission']['fixed']['Hbar']==direct['admission']['fixed']['finite_normal_Hbar']
    assert selected['fixed_materials']['Hunit']==original['fixed']['Hunit']
    assert selected['fixed_materials']['background_h']==original['owned_EPS5_background']['h']
    assert all(v is False for v in saved['qualification'].values()) and len(saved['qualification'])==9
    # Authentic general161 constants: exact integer cp, binary64 literal L0.
    grg=ast.parse(content['author_fragment_general_raw_jet_instantaneous_geodesic_v001.py'])
    si=ast.parse(content['author_fragment_model_metric_si_circle_readout_v002.py'])
    assert any(isinstance(q,ast.Constant) and type(q.value) is int and q.value==299792458 for q in ast.walk(grg))
    assert any(isinstance(q,ast.Constant) and type(q.value) is float and q.value==3.085677581491367e19 for q in ast.walk(si))
    cp=F(299792458); L0=F.from_float(3.085677581491367e19)
    Hbar=F.from_float(direct['admission']['fixed']['Hbar'])
    Hunit=F.from_float(original['fixed']['Hunit']); background_h=F.from_float(original['owned_EPS5_background']['h'])
    Hphysical=Hbar*cp/L0
    fixed_operand_H=Hunit*background_h/L0
    target=-2*Hphysical
    rows=[]
    for index,row in enumerate(saved['rows']):
        assert row['index']==index and row['selected_branch']==1 and row['physical_adoption'] is False
        omega=tuple(map(fraction,row['Omega_SI'])); derivative=tuple(map(fraction,row['Omega_dot_SI']))
        assert 0<omega[0]<=omega[1] and derivative[0]<=derivative[1]<0
        corners=[a/b for a in derivative for b in omega]
        ratio=(min(corners),max(corners))
        relative=tuple(sorted(v/target-1 for v in ratio))
        rows.append(dict(index=index,R_kpc=row['R_kpc'],selected_branch=1,
          source_json_path=row['source_json_path'],completed_readout=row['completed_readout'],
          Omega_dot_over_Omega_SI=ratio,minus_two_Hphysical_included=ratio[0]<=target<=ratio[1],
          relative_rate_difference_from_minus_two_H=relative,
          display_relative_difference_ppm=tuple(display(v*1000000) for v in relative),physical_adoption=False))
    assert len(rows)==43
    relative_range=(min(r['relative_rate_difference_from_minus_two_H'][0] for r in rows),max(r['relative_rate_difference_from_minus_two_H'][1] for r in rows))
    out=dict(status='CLOSED_BASELINE43_EXACT_BACKGROUND_ANGULAR_RATE_COMPARISON',
      created_utc=datetime.now(timezone.utc).isoformat(),source=dict(file=Path(__file__).name,sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
      authenticated_inputs=PINS,qualification=saved['qualification'],rows=rows,
      source_scalars=dict(Hunit=Hunit,owned_EPS5_background_h=background_h,saved_owned_Hbar=Hbar,cp_SI=cp,L0_m=L0,
        Hphysical_SI=Hphysical,minus_two_Hphysical_SI=target,exact_fixed_operand_Hphysical_SI=fixed_operand_H,
        saved_Hbar_relative_association_gap=Hphysical/fixed_operand_H-1,
        one_over_two_H_seconds=1/(2*Hphysical),one_over_two_H_Myr=1/(2*Hphysical*F(31557600000000))),
      summary=dict(events=43,intervals_containing_minus_two_H=sum(r['minus_two_Hphysical_included'] for r in rows),
        relative_rate_difference_range=relative_range,display_relative_difference_range_ppm=tuple(display(v*1000000) for v in relative_range),
        display_Hphysical_per_second=display(Hphysical),display_one_over_two_H_Myr=display(1/(2*Hphysical*F(31557600000000)))),
      formulae=dict(Hbar_source='fixed.Hunit / LIGHT * owned_EPS5_background.h (source-ordered rounded value read from closed INPUT)',
        Hphysical='saved_Hbar * exact cp_SI / binary64-L0 exact rational',ratio='endpoint enclosure of saved Omega_dot_SI / saved Omega_SI',
        relative='ratio / (-2 Hphysical) - 1',interval_dependency='independent endpoint enclosure; unknown correlations discarded'),
      source_finding=dict(prescribed_preparation='Q1 reconstruct_owned_K prescribes initial hdot increment 2 N Hbar h and native-p reconstruction; source explicitly denies evolved history.',
        actual_baseline='Separate authentic47969 Q1 TOTAL-rate and60363 correction Fhat lifts are added in139 order; actual TOTAL hdot need not equal the initial conformal increment.',
        gauge_time='Raw chart gauge jets come from owned Gamma/metric_partial. Raw85 copies genuine Ndot/betadot and all R/Z/phi words, then uses actual TOTAL hdot in time product rules.',
        common_scale_interpretation='Background-imposed preparation supplies the common scale. Saved ratios are close but all exclude exact -2H; local lapse/shift/nonaffinity, TOTAL-rate corrections, and raw/source association terms remain.',
        component_attribution='No numerical decomposition or proof that a specific term accounts for the ppm deviations was performed.',
        history='The near-common instantaneous timescale is not an evolved FLRW orbit solution, stability result, or physical-tracer admission.'),
      source_references=dict(cauchy_admission=[332,365],Q1_initial_K=[535,557],Q1_Hbar=[937,947],
        direct_Hbar=[119,124],direct_reference=[61,87],direct_TOTAL_rate=[89,95],raw_time_product_rule=[58,82],general_SI_and_motion=[121,135]),
      array_archive_decoded=False,producer_or_operator_replayed=False,raw_phi_or_time_words_projected=False,
      source_or_installed_rounding_accuracy_admitted=False,persistent_orbit_or_stability_claimed=False,physical_adoption=False,
      peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    b=(json.dumps(serial(out),sort_keys=True,indent=2)+'\n').encode()
    with OUTPUT.open('xb') as f:f.write(b)
    OUTPUT.chmod(0o444)
    assert OUTPUT.read_bytes()==b
    print(out['status'],len(rows),out['summary']['intervals_containing_minus_two_H'],hashlib.sha256(b).hexdigest(),len(b))

if __name__=='__main__':main()
