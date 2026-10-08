"""HELD closed-JSON local axial-scale tangent; no NPZ, producer or operator calls."""
import argparse
import hashlib
import json
import math
import resource
import traceback
from datetime import datetime, timezone
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from pathlib import Path

BASE=Path(__file__).resolve().parent
STEM='READONLY_CLOSED_BASELINE43_LOCAL_AXIAL_SCALE_TANGENT_V002'
AUTHOR_DRAFT=False
PRODUCER_SOURCE=('baseline_DIRECT43_general_raw_jet_diagnostic_v003.py', 'fae2f715dd379f3ff9e38e61785ebc8d23620c5a51fd214920486475450bc29b')
PRODUCER_RESULT=('BASELINE_DIRECT43_GENERAL_RAW_JET_DIAGNOSTIC_V002_RESULT.json', '790ef96dca9285bcb4394b5fe74b8b232e4c577c69303f1690197ea686214dda')
PRODUCER_RECEIPT=('BASELINE_DIRECT43_GENERAL_RAW_JET_DIAGNOSTIC_V002_RECEIPT.json', 'ccb6433236d382bcc84ded0df8616be3dc6cc8fd61682e89f1000e7c01f33340')
PRODUCER_PROOF=('READONLY_NATURAL_CLOSED_BASELINE_DIRECT43_GENERAL_DIAGNOSTIC_SEALS_V001.json', '3c9cfe64bcacb2703a6d44377cb361bb11b56b5ef1512af777f4943e10ad439d', 'READONLY_NATURAL_CLOSED_BASELINE_DIRECT43_GENERAL_DIAGNOSTIC_SEALS_VERIFIED')
SELECTED_MAP=('HELD_CLOSED_BASELINE43_LOCAL_AXIAL_SCALE_TANGENT_SELECTED_JSON_V001.json', 'dbc0897491a7eb32829849e39d210d4d7ccbc6087e270f8fe10ed0bf5940b8f4')
PINS={
 'author_fragment_baseline_DIRECT43_raw_jet_pair_v001.py':'07cbcd0af964ba2531c12878e629b9c58ce56bff23fa94bd5471d83162ab2dd9',
 'author_fragment_general_raw_jet_instantaneous_geodesic_v001.py':'b357de459494d9bad5bb0963ee2c3236ca8265872ebaf583062e54b03b40602b',
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8',
 'OBSERVER_COMMON_FLRW_ANGULAR_DRIFT_VERSUS_EVOLVING_BOUND_ORBITS_SOURCE_AUDIT_V002.json':'d64a37006d35acde9d75d86baa1c32e8221ba2d4753ff85bfe6c6d3075ea0cf6',
}

def load(name,digest):
    p=BASE/name
    assert p.suffix in ('.json','.py') and p.stat().st_size<=4*1024*1024
    assert not p.stat().st_flags&0x40000000, 'No FileProvider recall by this worker'
    b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==digest,name
    return json.loads(b) if p.suffix=='.json' else b.decode()

def fraction(q):
    assert set(q)=={'numerator','denominator'} and isinstance(q['numerator'],str) and isinstance(q['denominator'],str)
    n,d=int(q['numerator']),int(q['denominator']);assert d>0
    return F(n,d)

def serial(q):
    if isinstance(q,F):return dict(numerator=str(q.numerator),denominator=str(q.denominator))
    if isinstance(q,dict):return {k:serial(v) for k,v in q.items()}
    if isinstance(q,(tuple,list)):return [serial(v) for v in q]
    return q

def publish(name,value):
    p=BASE/name;b=(json.dumps(serial(value),sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(b)
    p.chmod(0o444);assert p.read_bytes()==b
    return dict(file=name,sha256=hashlib.sha256(b).hexdigest())

def scalar(words,kind,slot):
    pair=words[kind]
    for i in slot:pair=pair[i]
    assert len(pair)==2
    exact=tuple(map(fraction,pair));flat=slot[0]*16+slot[1]*4+slot[2] if kind=='dg' else slot[0]*4+slot[1]
    assert all(F.from_float(float.fromhex(words['word_hex'][kind][w][flat]))==v for w,v in zip(('hi','lo'),exact))
    return exact,sum(exact,F(0))

def outward(q,lower):
    with localcontext() as ctx:
        ctx.prec=8;ctx.rounding=ROUND_FLOOR if lower else ROUND_CEILING
        return str(Decimal(q.numerator)/Decimal(q.denominator))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
    assert not AUTHOR_DRAFT and args.root_run,'HELD: root release after independent FULL review required'
    for pin in (PRODUCER_SOURCE,PRODUCER_RESULT,PRODUCER_RECEIPT,PRODUCER_PROOF,SELECTED_MAP):assert all(v is not None for v in pin)
    assert not list(BASE.glob(STEM+'_*')),'Exclusive own result/event/error prefix required'
    selected=load(*SELECTED_MAP);proof=load(*PRODUCER_PROOF[:2])
    assert selected['status']=='HELD_CLOSED_BASELINE43_LOCAL_AXIAL_SCALE_TANGENT_SELECTED_JSON_V001'
    assert selected['source_closure_proof']==list(PRODUCER_PROOF) and proof['status']==PRODUCER_PROOF[2]
    assert selected['producer_source']==list(PRODUCER_SOURCE) and selected['producer_result']==list(PRODUCER_RESULT) and selected['producer_receipt']==list(PRODUCER_RECEIPT)
    assert proof['naturally_closed'] is True and proof['exit_code']==0
    assert proof['all_input_seals_verified'] is proof['all_output_seals_verified'] is proof['all_success_role_seals_verified'] is True
    assert (proof['event_count'],proof['role_count'],proof['control_count'])==(43,990,0)
    assert (proof['input_count'],proof['output_count'])==(194,1983)
    assert proof['source_sha256']==PRODUCER_SOURCE[1] and proof['result_sha256']==PRODUCER_RESULT[1] and proof['receipt_sha256']==PRODUCER_RECEIPT[1]
    assert proof['owner']==selected['source_scientific_owner'] and proof['owner']['source_sha256']==PRODUCER_SOURCE[1]
    assert proof['qualification']==selected['qualification'] and len(proof['qualification'])==9 and all(v is False for v in proof['qualification'].values())
    load(*PRODUCER_SOURCE)
    for name,digest in PINS.items():load(name,digest)
    omega=load(*selected['omega_intervals'])
    assert omega['baseline_owner']==proof['owner'] and omega['selection']['chosen_branch']==1 and omega['selection']['events']==43
    assert len(selected['rows'])==len(omega['rows'])==43 and omega['qualification']==proof['qualification']
    originals={r['ordinal']:r for r in proof['records']};rateSI=F(299792458)/F.from_float(3.085677581491367e19)
    current={};completed=[];rows=[]
    try:
        for index,(selection,angular) in enumerate(zip(selected['rows'],omega['rows'])):
            current=dict(index=index,R_kpc=selection['R'],record=selection['record'])
            assert selection['index']==angular['index']==index and angular['selected_branch']==1 and angular['physical_adoption'] is False
            assert selection['R']==angular['R_kpc'] and math.isfinite(selection['R']) and selection['R']>0
            rec=selection['record'];original=originals[selection['ordinal']]
            assert rec=={k:original[k] for k in ('file','sha256','commit_file','commit_sha256')}
            assert original['failed'] is False and original['owner_equal'] is original['embedded_metadata_equal'] is True
            commit=load(rec['commit_file'],rec['commit_sha256']);md=commit['metadata']
            assert commit['file']==rec['file'] and commit['sha256']==rec['sha256']
            assert md['owner']==proof['owner'] and md['failed'] is False and md['physical_adoption'] is False and md['baseline_only'] is True
            assert md['qualification']==proof['qualification'] and md['role']==original['role']==f'EVENT_{index:02d}_GENERAL_INPUT_INTERVAL_DOMAINS'
            assert md['context']['index']==index and md['context']['R']==selection['R'] and md['context']['radial_side']=='left' and md['context']['vertical_side']=='upper'
            assert angular['completed_readout']==proof['events'][index]['readout_ref']
            words=md['completed_payload']['bounds']['authentic_output_words'];assert words['completed_raw_pair']==selection['completed_raw_pair']
            assert words['all_original_word_hex_preserved'] is words['all_output_dyadic_words_authenticated'] is True
            pairs={};values={};current['represented_operands']=dict(pairs=pairs,sums=values)
            for n,kind,slot in (('g_phi_phi','g',(3,3)),('dt_g_phi_phi','dg',(0,3,3)),('dR_g_phi_phi','dg',(1,3,3)),('dphi_g_phi_phi','dg',(3,3,3))):
                current['active_scalar']=dict(name=n,kind=kind,slot=slot)
                pairs[n],values[n]=scalar(words,kind,slot)
            omSI=tuple(map(fraction,angular['Omega_SI']));assert 0<omSI[0]<=omSI[1]
            om=tuple(v/rateSI for v in omSI)
            result=dict(index=index,R_kpc=selection['R'],input_ref=rec,completed_raw_pair=selection['completed_raw_pair'],Omega_readout=angular['completed_readout'],
              Omega_model_interval=om,Omega_SI_interval=omSI,represented_input_word_pairs=pairs,represented_input_sums=values,
              wZ_model=F(0),raw_phi_preserved=True,coordinate_speed_not_normal_observer_speed=True,
              C_squared=values['g_phi_phi'],circumferential_radius_interpretation_admitted=False,
              source_or_installed_rounding_accuracy_admitted=False,old_radial_root_recomputed=False,geodesic_or_history_or_physical_adoption=False)
            if values['g_phi_phi']<=0 or values['dR_g_phi_phi']==0:
                result.update(status='LOCAL_AXIAL_SCALE_DOMAIN_REFUSAL',reason='g_phi_phi_nonpositive' if values['g_phi_phi']<=0 else 'radial_derivative_exact_zero',wR_model_interval=None,coordinate_radial_speed_kms_interval=None)
            else:
                wt,wr,wp=(values[n] for n in ('dt_g_phi_phi','dR_g_phi_phi','dphi_g_phi_phi'))
                linked=[dict(Omega_model=v,wR_model=-(wt+v*wp)/wr) for v in om]
                for v in linked:v['constant_C_squared_total_derivative']=wt+v['wR_model']*wr+v['Omega_model']*wp;assert v['constant_C_squared_total_derivative']==0
                speeds=tuple(sorted(v['wR_model'] for v in linked));si_speed=tuple(v*F(299792458,1000) for v in speeds)
                result.update(status='REPRESENTED_LOCAL_AXIAL_SCALE_TANGENT_ENCLOSED',linked_endpoint_witnesses=linked,wR_model_interval=speeds,
                  coordinate_radial_speed_kms_interval=si_speed,display_coordinate_radial_speed_kms=(outward(si_speed[0],True),outward(si_speed[1],False)),
                  interval_scope='Fixed authentic represented g/dg; supplied Omega interval. No a priori physical/source-error budget.')
            current['completed_local_tangent']=result;rows.append(result)
            completed.append(publish(f'{STEM}_{index:02d}_EVENT.json',dict(owner_scope='closed_baseline_JSON_postprocessing',row=result,qualification=proof['qualification'])))
        resolved=[r for r in rows if r['wR_model_interval'] is not None]
        ranges=None
        if resolved:
            q=(min(r['coordinate_radial_speed_kms_interval'][0] for r in resolved),max(r['coordinate_radial_speed_kms_interval'][1] for r in resolved))
            ranges=dict(coordinate_radial_speed_kms=q,display=(outward(q[0],True),outward(q[1],False)))
        out=dict(status='CLOSED_BASELINE43_LOCAL_AXIAL_SCALE_TANGENTS_MEASURED',source=dict(file=Path(__file__).name,sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
          created_utc=datetime.now(timezone.utc).isoformat(),producer_proof=PRODUCER_PROOF,selected_map=SELECTED_MAP,omega_input=selected['omega_intervals'],baseline_owner=proof['owner'],
          rows=rows,completed_events=completed,event_count=43,resolved_count=len(resolved),refusal_count=43-len(resolved),ranges=ranges,
          formula='wR=-(partial_t g_phi_phi + Omega partial_phi g_phi_phi)/partial_R g_phi_phi, wZ=0; C=sqrt(g_phi_phi)',
          SI_conversion='dR_metre/dt_second = cp_SI*wR_model; km/s=cp_SI*wR_model/1000. No lapse/shift normal-observer conversion.',
          interpretation='Instantaneous coordinate tangent to constant local axial scale. Old Omega root assumed wR=0; this does not solve a new radial root, restore a residual, or construct a geodesic/history.',
          actual_axisymmetry_admitted=False,circumferential_radius_interpretation_admitted=False,raw_phi_projected=False,qualification=proof['qualification'],
          producer_or_operator_replayed=False,numeric_archives_decoded=False,source_or_installed_rounding_accuracy_admitted=False,physical_adoption=False,
          peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        ref=publish(STEM+'_RESULT.json',out);print(out['status'],len(rows),len(resolved),ref['sha256'])
    except BaseException:
        publish(STEM+'_ERROR.json',dict(status='SAVED_JSON_TANGENT_POSTPROCESSING_FAILED',traceback=traceback.format_exc(),active=current,completed_events=completed,qualification=proof['qualification'],physical_adoption=False))
        raise

if __name__=='__main__':main()
