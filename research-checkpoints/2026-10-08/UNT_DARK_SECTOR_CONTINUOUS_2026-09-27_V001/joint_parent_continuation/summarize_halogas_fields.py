"""Complete-census descriptive summary/figure; no solver, fitting or case selection."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import disk_solver as law

ROOT = Path(__file__).resolve().parent
NAMES = {40: 'HALOGAS40_ML36_RETAINED_V001', 120: 'HALOGAS120_ML36_RETAINED_V001'}
CONTROL = 'ML36_CAL_HI1_H21_V001'


def load(path, frozen):
    record = json.loads(path.read_text())
    assert record['freeze_sha256'] == law.sha(frozen)
    p = record['payload']
    assert record['payload_sha256'] == hashlib.sha256(law.encode(p)).hexdigest()
    return p


def main():
    out = ROOT/'HALOGAS_FIELD_DESCRIPTIVE_SUMMARY.json'
    figure = ROOT/'NGC3198_HI_SOURCE_CONTRAST.png'
    assert not out.exists() and not figure.exists()
    frozen = ROOT/'HALOGAS_FIELD_FROZEN.json'
    spec = json.loads(frozen.read_text())
    for name, digest in spec['files'].items():
        assert law.sha(ROOT/name) == digest
    final = load(ROOT/'HALOGAS_FIELD_RESULTS.json', frozen)
    assert final['status'] == 'COMPLETE' and len(final['case_files_sha256']) == 8
    hashes = {'HALOGAS_FIELD_FROZEN.json': law.sha(frozen),
              'HALOGAS_FIELD_RESULTS.json': law.sha(ROOT/'HALOGAS_FIELD_RESULTS.json')}
    cases, check_count = {}, 0
    for name, digest in final['case_files_sha256'].items():
        assert law.sha(ROOT/name) == digest
        p = load(ROOT/name, frozen)
        assert p['case']+'.json' == name and all(p['checks'].values())
        cases[p['model'], p['N'], p['extent'], p['newtonian']] = p
        hashes[name] = digest
        check_count += len(p['checks'])
    assert set(cases) == {(model,n,l,newton) for model in NAMES.values()
                         for n,l,newton in ((256,255,False),(320,1023,False),(512,255,False),(512,255,True))}
    old_freeze = ROOT/'STELLAR_CALIBRATION_FROZEN.json'
    old = {}
    for newton in (False, True):
        name = f'{CONTROL}_N512_L255_Newton{int(newton)}.json'
        old[newton] = load(ROOT/name, old_freeze)
        assert all(old[newton]['checks'].values())
        hashes[name] = law.sha(ROOT/name)
    baseline_rows = old[False]['comparison']
    labels = ('R_ge_0_kpc', 'R_ge_2_kpc', 'R_ge_8_kpc')
    summary = {'role': 'post-exposure fixed-plane retained-emission source sensitivity; no fit',
        'status': 'COMPLETE', 'checked_cases': 8, 'case_check_count': check_count,
        'input_sha256': hashes, 'script_sha256': law.sha(Path(__file__)),
        'control_rms_kms': {str(n): {k: old[n]['summaries_descriptive_only'][k]['rms_kms'] for k in labels} for n in old},
        'models': {}}
    for width, model in NAMES.items():
        nonlinear = cases[model,512,255,False]
        newton = cases[model,512,255,True]
        assert nonlinear['component_masses_Msun'] == newton['component_masses_Msun']
        for p in (nonlinear,newton):
            assert [(r['R'],r['velocity'],r['error']) for r in p['comparison']] == [(r['R'],r['velocity'],r['error']) for r in baseline_rows]
            assert all(r['prediction'] is not None for r in p['comparison'])
        selected = []
        for i, row in enumerate(nonlinear['comparison']):
            if row['R'] in (5.78,12.05,24.03,44.08):
                selected.append({'R_kpc': row['R'], 'observed_kms': row['velocity'],
                    'old_gas_network_kms': baseline_rows[i]['prediction'],
                    'modern_gas_network_kms': row['prediction'],
                    'modern_gas_newton_kms': newton['comparison'][i]['prediction']})
        assert len(selected) == 4
        summary['models'][model] = {'width_arcsec': width,
            'component_masses_Msun': nonlinear['component_masses_Msun'],
            'network_rms_kms': {k: nonlinear['summaries_descriptive_only'][k]['rms_kms'] for k in labels},
            'newtonian_rms_kms': {k: newton['summaries_descriptive_only'][k]['rms_kms'] for k in labels},
            'fine_mesh_comparison': nonlinear['numerical_comparison'],
            'remote_domain_comparison': cases[model,320,1023,False]['numerical_comparison'],
            'illustrative_radii_used_in_previous_comparison': selected,
            'all43_network_rows': nonlinear['comparison'], 'all43_newtonian_rows': newton['comparison']}
    im = Image.new('RGB',(1440,1050),'#fafaf8')
    d = ImageDraw.Draw(im)
    font = lambda n: ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',n)
    ink,grey,grid = '#172b37','#68747c','#dfe4e4'
    colors = {40:'#087f83',120:'#7856a7','old':'#74818a','newton':'#bf621e'}
    d.text((100,28),'Hydrogen source test: same response law, no dark halo',fill=ink,font=font(32))
    d.text((100,77),'NGC 3198 | fixed calibrated stars, molecular gas, distance and geometry | all 43 radii',fill=grey,font=font(21))
    panels = ((155,625,-20,215,'Circular speed (km/s)'),(743,943,-105,55,'Predicted minus observed (km/s)'))
    left,right = 100,1370
    def pos(r,y,p):
        top,bottom,low,high,_=p
        return left+r/46*(right-left),bottom-(y-low)/(high-low)*(bottom-top)
    for ip,panel in enumerate(panels):
        top,bottom,low,high,label=panel
        d.text((left,top-33),label,fill=ink,font=font(20))
        for r in range(0,46,5):
            px,_=pos(r,0,panel)
            d.line((px,top,px,bottom),fill=grid)
            if ip:
                d.text((px-10,bottom+8),str(r),fill=grey,font=font(18))
        for y in ((0,40,80,120,160,200) if not ip else (-100,-50,0,50)):
            _,py=pos(0,y,panel)
            d.line((left,py,right,py),fill=grid if y else '#abb5ba',width=1 if y else 2)
            d.text((left-55,py-10),str(y),fill=grey,font=font(18))
        curves=[(baseline_rows,colors['old'],3)]
        for width,model in NAMES.items():
            curves.append((cases[model,512,255,True]['comparison'],colors['newton'],2))
            curves.append((cases[model,512,255,False]['comparison'],colors[width],3))
        for rows,color,line_width in curves:
            values=[r['residual'] if ip else r['prediction'] for r in rows]
            assert min(values)>=low and max(values)<=high
            d.line([pos(r['R'],v,panel) for r,v in zip(rows,values)],fill=color,width=line_width)
        for row in baseline_rows:
            value=0 if ip else row['velocity']
            px,py=pos(row['R'],value,panel)
            _,pylo=pos(row['R'],value-row['error'],panel)
            _,pyhi=pos(row['R'],value+row['error'],panel)
            assert low<=value-row['error']<=value+row['error']<=high
            d.line((px,pyhi,px,pylo),fill=grey)
            d.ellipse((px-3,py-3,px+3,py+3),fill=ink)
    for x,y,color,label in ((100,663,colors['old'],'Network: old gas'),(530,663,colors[40],'Network: modern 40 arcsec'),
                            (100,701,colors['newton'],'Newtonian: modern gas (both)'),(530,701,colors[120],'Network: modern 120 arcsec')):
        d.line((x,y,x+35,y),fill=color,width=3)
        d.text((x+47,y-13),label,fill=ink,font=font(20))
    d.text((1100,650),'Dots: observed',fill=ink,font=font(20))
    d.text((625,983),'Radius (kpc)',fill=ink,font=font(21))
    d.text((100,1020),'Modern profiles retain masked emission; not a full warped-gas reconstruction or an uncertainty band. No velocity fit.',fill=grey,font=font(18))
    im.save(figure)
    summary['figure_sha256']=law.sha(figure)
    summary['payload_sha256']=hashlib.sha256(law.encode(summary)).hexdigest()
    law.save_new(out,summary)
    print(json.dumps({key:{k:v for k,v in value.items() if not k.startswith('all43')}
                      for key,value in summary['models'].items()}))


if __name__=='__main__':
    main()
