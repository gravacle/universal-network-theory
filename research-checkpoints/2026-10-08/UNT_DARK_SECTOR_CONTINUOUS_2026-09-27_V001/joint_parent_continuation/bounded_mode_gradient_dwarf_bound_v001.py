"""Tiny new hybrid virial arithmetic; reuse authenticated old moments."""
from pathlib import Path
import hashlib
import json
import math
import time
HERE=Path(__file__).resolve().parent
OUT=HERE/'BOUNDED_MODE_GRADIENT_DWARF_BOUND_V001_RESULT.json'
if OUT.exists(): raise SystemExit('Refusing overwrite')
start=time.monotonic()
raw=(HERE/'COMPACT_DWARF_ISOLATED_BOUND_V001_RESULT.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='6fe41c1fdb3f971a449ad34ec58adcd9c4fdb062659e174d306f9e55e4e26bd9'
old=json.loads(raw)
repairraw=(HERE/'COMPACT_DWARF_ISOLATED_BOUND_V002_REPAIR_RESULT.json').read_bytes()
repair=json.loads(repairraw)
assert old['status']=='FAILED' and repair['status']=='TECHNICAL_CONTROL_RECOVERED'
assert repair['source_result_sha256']==hashlib.sha256(raw).hexdigest()
assert all(v['repaired_control']['passed'] for v in repair['references'])
replaced={v['repaired_control']['name'] for v in repair['references']}
assert all(c['passed'] for c in old['controls'] if c['name'] not in replaced)
pc=648000*149597870700/math.pi
a,ell,rap=28*pc,100*pc,67*pc
gmnom=1.3271244e20; target=3700.
fap=rap*rap/(rap*rap+a*a)
checks,rows=[],[]
def err(x,y): return abs(x-y)/max(1.,abs(x),abs(y))
def check(name,value):
    checks.append(dict(name=name,error=float(value),tolerance=2e-12,
                       passed=bool(math.isfinite(value) and value<=2e-12)))
check('aperture_reference',err(fap,old['aperture_fraction']))
check('aperture_independent_form',err(fap,1/(1+(a/rap)**2)))
for prior in old['rows']:
    mass=prior['M_nominal_solar']; GM=mass*gmnom
    C=GM/(2*ell*ell)
    newton=3*math.pi*GM/(32*a)
    extra=GM*a/(ell*ell); total=newton+extra
    glob=math.sqrt(total)/1000; aperture=math.sqrt(total/fap)/1000
    den=fap*target*target-newton
    ceiling=math.sqrt(GM*a/den)/pc if den>0 else None
    tag=str(mass)
    check(tag+'_saved_Newton_moment',err(newton,prior['Newton_second_moment_m2_s2']))
    check(tag+'_anomalous_term',err(extra,2*a*C))
    check(tag+'_dimensionless_total',err(total/(GM/a),3*math.pi/32+(a/ell)**2))
    check(tag+'_aperture_identity',err((aperture*1000)**2*fap,total))
    check(tag+'_exact_doubled_extra',err(extra,2*prior['extra_second_moment_upper_m2_s2']))
    if ceiling is not None:
        ellinv=ceiling*pc
        check(tag+'_original_inequality_inversion',err((newton+GM*a/ellinv**2)/fap,target*target))
        check(tag+'_sqrt2_old_ceiling',err(ceiling,math.sqrt(2)*prior['necessary_ell_ceiling_pc_for_3p7_km_s']))
    rows.append(dict(M_nominal_solar=mass,M_to_L_nominal=prior['M_to_L_nominal'],
                     anomalous_force_upper_m_s2=C,Newton_second_moment_m2_s2=newton,
                     extra_second_moment_upper_m2_s2=extra,total_second_moment_upper_m2_s2=total,
                     global_LOS_upper_km_s=glob,aperture_LOS_upper_km_s=aperture,
                     inversion_denominator_m2_s2=den,necessary_ell_ceiling_pc_for_3p7_km_s=ceiling))
for row in rows[1:]:
    ratio=row['M_nominal_solar']/rows[0]['M_nominal_solar']
    check(str(ratio)+'_mass_scaling',err(row['total_second_moment_upper_m2_s2']/rows[0]['total_second_moment_upper_m2_s2'],ratio))
    check(str(ratio)+'_speed_scaling',err(row['aperture_LOS_upper_km_s']/rows[0]['aperture_LOS_upper_km_s'],math.sqrt(ratio)))
payload=dict(status='QUALIFIED' if all(c['passed'] for c in checks) else 'FAILED',
             scope='conditional isolated outward hybrid branch and conservative stationary Plummer virial bound',
             inputs=dict(ell_pc=100,a_pc=28,aperture_pc=67,GM_nominal_sun=gmnom,
                         parsec_metres=pc,exposed_reference_sigma_km_s=3.7,external_field=0),
             source_inputs_sha256={'COMPACT_DWARF_ISOLATED_BOUND_V001_RESULT.json':hashlib.sha256(raw).hexdigest(),
                                   'COMPACT_DWARF_ISOLATED_BOUND_V002_REPAIR_RESULT.json':hashlib.sha256(repairraw).hexdigest()},
             old_failed_receipt_preserved=True,aperture_fraction=fap,rows=rows,checks=checks,
             passed=sum(c['passed'] for c in checks),total=len(checks),
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             protocol_sha256=hashlib.sha256((HERE/'BOUNDED_MODE_GRADIENT_DWARF_BOUND_V001.md').read_bytes()).hexdigest(),
             elapsed_seconds=time.monotonic()-start)
canonical=json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
with OUT.open('x') as stream:
    json.dump(dict(payload=payload,payload_sha256=hashlib.sha256(canonical).hexdigest()),stream,indent=2,allow_nan=False)
print(json.dumps(dict(status=payload['status'],passed=payload['passed'],total=payload['total'],
                     elapsed_seconds=payload['elapsed_seconds'],rows=rows),indent=2))
