"""Descriptive, source-only comparison of authenticated old and modern HI profiles."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import galaxy_density as density

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / 'halogas_source_candidate'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sealed(path):
    value = json.loads(path.read_text())
    check = dict(value)
    digest = check.pop('payload_sha256')
    assert hashlib.sha256(canonical(check)).hexdigest() == digest
    return value


def main():
    target = INPUT / 'OLD_MODERN_HI_COMPARISON.json'
    figure = INPUT / 'OLD_MODERN_HI_COMPARISON.png'
    assert not target.exists() and not figure.exists()
    freeze = sealed(INPUT / 'PLANAR_SOURCE_FROZEN.json')
    for name, digest in freeze['inputs_sha256'].items():
        assert sha(INPUT / name) == digest
    actual = sealed(INPUT / 'PLANAR_SOURCE_RESULTS.json')
    assert actual['freeze_sha256'] == sha(INPUT / 'PLANAR_SOURCE_FROZEN.json')
    assert actual['status'] == 'COMPLETE' and all(c['passed'] for c in actual['checks'])
    original = json.loads((ROOT / 'GALAXY_FIELD_FROZEN.json').read_text())
    for name in ('galaxy_density.py', 'NGC3198_BARYON_INPUT.json'):
        assert sha(ROOT / name) == original['files'][name]
    order = next(o for o in actual['orders'] if o['subpixels_per_axis'] == 8)
    old = density.profiles(True, True)['HI_He']
    output = {'role': 'descriptive source-only, exposed profiles, no force or velocity input',
              'script_sha256': sha(Path(__file__)),
              'input_sha256': {str(p.relative_to(ROOT)): sha(p) for p in (
                  INPUT / 'PLANAR_SOURCE_FROZEN.json', INPUT / 'PLANAR_SOURCE_RESULTS.json',
                  ROOT / 'GALAXY_FIELD_FROZEN.json', ROOT / 'galaxy_density.py',
                  ROOT / 'NGC3198_BARYON_INPUT.json')}, 'profiles': {}}
    for width in (40, 120):
        p = order[f'profile_{width}arcsec']
        g = p['groups']['full']
        rows = []
        for i, (lo, hi) in enumerate(zip(p['r_lo_kpc'], p['r_hi_kpc'])):
            area = math.pi * 1e6 * (hi*hi-lo*lo)
            om = float(2*math.pi*1e6*old.integral(lo, hi)/1.36)
            complete = p['complete_by_conservative_chord_bound'][i]
            rows.append({'lo_kpc': lo, 'hi_kpc': hi, 'complete': complete,
                'old_HI_mass_Msun': om, 'modern_retained_HI_mass_Msun': g['mass_Msun'][i],
                'old_HI_annular_mean_Msun_pc2': om/area,
                'modern_HI_annular_mean_Msun_pc2': g['effective_HI_Msun_pc2_complete_only'][i],
                'modern_minus_old_mass_Msun': g['mass_Msun'][i]-om,
                'modern_positive_sky_fraction': g['positive_fraction_of_footprint'][i],
                'modern_zero_or_replaced_sky_fraction': g['zero_fraction_of_footprint'][i],
                'modern_half_difference_Msun_pc2': p['half_effective_HI_difference_complete_only'][i]})
        inside = [r for r in rows if r['complete']]
        assert all(r['complete'] for r in rows[:len(inside)])
        modern = sum(r['modern_retained_HI_mass_Msun'] for r in inside)
        previous = sum(r['old_HI_mass_Msun'] for r in inside)
        outside = sum(r['modern_retained_HI_mass_Msun'] for r in rows[len(inside):])
        output['profiles'][str(width)] = {'rows': rows,
            'complete_prefix_upper_kpc': inside[-1]['hi_kpc'],
            'complete_prefix_modern_HI_Msun': modern,
            'complete_prefix_old_HI_Msun': previous,
            'complete_prefix_mass_ratio': modern/previous,
            'retained_map_mass_outside_complete_prefix_Msun': outside,
            'outside_fraction_of_retained_map': outside/(modern+outside)}
    # All numerical rows remain in JSON. The plot is explicitly a 0--64 kpc view.
    im = Image.new('RGB', (1400, 940), '#fafaf8')
    draw = ImageDraw.Draw(im)
    font = lambda n: ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', n)
    ink, grey, grid = '#172b37', '#68747c', '#dfe4e4'
    draw.text((95, 25), 'NGC 3198: a source test, before any new gravity solve', fill=ink, font=font(30))
    draw.text((95, 73), 'Bare hydrogen; same fixed distance and plane. Annular masses are conserved.', fill=grey, font=font(21))
    panels = ((148, 526, 0., 6., 'Mean retained H I surface density (solar masses / pc²)'),
              (640, 817, 0., 1., 'Modern map: positive-signal sky-area fraction (not completeness)'))
    left, right = 95, 1340
    def pos(r, y, panel):
        top, bottom, low, high, _ = panel
        return left+r/64*(right-left), bottom-(y-low)/(high-low)*(bottom-top)
    colors = {'old': '#b26c28', 40: '#087f83', 120: '#7856a7'}
    for ip, panel in enumerate(panels):
        top, bottom, low, high, label = panel
        draw.text((left, top-34), label, fill=ink, font=font(21))
        for r in range(0, 65, 8):
            x, _ = pos(r, 0, panel)
            draw.line((x, top, x, bottom), fill=grid)
            if ip == 1:
                draw.text((x-8, bottom+10), str(r), fill=grey, font=font(19))
        for y in ((0, 1, 2, 3, 4, 5, 6) if ip == 0 else (0, .5, 1)):
            _, py = pos(0, y, panel)
            draw.line((left, py, right, py), fill=grid)
            draw.text((left-44, py-10), f'{y:g}', fill=grey, font=font(18))
        if ip == 0:
            rr = np.linspace(0, 64, 513)
            draw.line([pos(float(r), float(old.sigma(r))/1.36, panel) for r in rr], fill=colors['old'], width=4)
        for width in (120, 40):
            points = []
            for row in output['profiles'][str(width)]['rows']:
                if row['lo_kpc'] >= 64:
                    break
                value = row['modern_HI_annular_mean_Msun_pc2'] if ip == 0 else row['modern_positive_sky_fraction']
                assert value is not None and low <= value <= high
                points += [pos(row['lo_kpc'], value, panel), pos(min(64, row['hi_kpc']), value, panel)]
            draw.line(points, fill=colors[width], width=3)
    for x, color, label in ((95, colors['old'], 'Old adopted profile'), (485, colors[40], 'Modern 40-arcsec bins'), (945, colors[120], 'Modern 120-arcsec bins')):
        draw.line((x, 563, x+38, 563), fill=color, width=4)
        draw.text((x+49, 550), label, fill=ink, font=font(20))
    draw.text((600, 857), 'Radius (kpc)', fill=ink, font=font(21))
    draw.text((95, 894), 'Zero replacements are not measured absent gas. No beam deconvolution, uncertainty band, warp or velocity fit.', fill=grey, font=font(18))
    im.save(figure)
    output['figure_sha256'] = sha(figure)
    output['plot_range_kpc'] = [0, 64]
    output['payload_sha256'] = hashlib.sha256(canonical(output)).hexdigest()
    with target.open('x') as stream:
        json.dump(output, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')
    print(json.dumps({k: {name: value for name, value in v.items() if name != 'rows'}
                      for k, v in output['profiles'].items()}))


if __name__ == '__main__':
    main()
