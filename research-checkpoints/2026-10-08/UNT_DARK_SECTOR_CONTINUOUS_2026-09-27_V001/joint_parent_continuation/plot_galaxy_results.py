"""Static scientific figure of every frozen source variant; no fit or solver."""
import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import disk_solver as law

ROOT = Path(__file__).resolve().parent


def main():
    models = ((1, 1), (0, 1), (1, 0), (0, 0))
    data, hashes = {}, {}
    freeze_hash = law.sha(ROOT / 'GALAXY_FIELD_FROZEN.json')
    for hi, h2 in models:
        for n, extent, newton in ((256, 255, 0), (320, 1023, 0), (512, 255, 0), (512, 255, 1)):
            path = ROOT / f'galaxy_HI{hi}_H2{h2}_N{n}_L{extent}_Newton{newton}.json'
            obj = json.loads(path.read_text())
            p = obj['payload']
            assert obj['freeze_sha256'] == freeze_hash
            assert obj['payload_sha256'] == hashlib.sha256(law.encode(p)).hexdigest()
            assert p['case'] == path.stem and all(p['checks'].values())
            hashes[path.name] = law.sha(path)
            if n == 512:
                data[hi, h2, newton] = p['comparison']
    baseline = data[1, 1, 0]
    assert all([(r['R'], r['velocity'], r['error']) for r in rows] ==
               [(r['R'], r['velocity'], r['error']) for r in baseline] for rows in data.values())
    assert all(r['prediction'] is not None for rows in data.values() for r in rows)
    out = ROOT / 'NGC3198_FIXED_SOURCE_COMPARISON.png'
    assert not out.exists(), 'Preserve the existing figure.'
    im = Image.new('RGB', (1440, 1050), '#fafaf8')
    d = ImageDraw.Draw(im)
    font_path = '/System/Library/Fonts/Supplemental/Arial.ttf'
    font = lambda size: ImageFont.truetype(font_path, size)
    ink, grey, grid = '#172b37', '#68747c', '#dfe4e4'
    colors = {0: '#087f83', 1: '#bf621e'}
    fills = {0: '#b6dddd', 1: '#ebccae'}
    d.text((104, 32), 'NGC 3198: fixed ordinary matter, no dark halo', font=font(34), fill=ink)
    d.text((104, 82), 'Conditional network-response law versus Newtonian gravity | all 43 measured radii', font=font(23), fill=grey)
    panels = [(160, 630, -20, 210, 'Circular speed (km/s)'),
              (725, 940, -105, 55, 'Predicted minus observed (km/s)')]
    left, right = 104, 1370

    def pos(r, value, panel):
        top, bottom, ymin, ymax, _ = panel
        return (left + r / 46 * (right-left), bottom - (value-ymin)/(ymax-ymin)*(bottom-top))

    for pi, panel in enumerate(panels):
        top, bottom, ymin, ymax, label = panel
        d.text((left, top-33), label, font=font(21), fill=ink)
        for x in range(0, 46, 5):
            px, _ = pos(x, 0, panel)
            d.line((px, top, px, bottom), fill=grid, width=1)
            if pi == 1:
                d.text((px-12, bottom+10), str(x), font=font(19), fill=grey)
        ticks = range(0, 201, 40) if pi == 0 else (-100, -50, 0, 50)
        for y in ticks:
            _, py = pos(0, y, panel)
            d.line((left, py, right, py), fill=grid if y else '#acb6ba', width=1 if y else 2)
            d.text((left-62, py-11), str(y), font=font(19), fill=grey)
        for newton in (1, 0):
            curves = [data[hi, h2, newton] for hi, h2 in models]
            value = lambda row: row['prediction'] if pi == 0 else row['residual']
            lo = [min(value(rows[i]) for rows in curves) for i in range(43)]
            hi = [max(value(rows[i]) for rows in curves) for i in range(43)]
            assert min(lo) >= ymin and max(hi) <= ymax
            polygon = [pos(r['R'], v, panel) for r, v in zip(baseline, lo)]
            polygon += [pos(r['R'], v, panel) for r, v in reversed(list(zip(baseline, hi)))]
            d.polygon(polygon, fill=fills[newton])
            for rows in curves:
                d.line([pos(r['R'], value(r), panel) for r in rows], fill=colors[newton], width=2)
            d.line([pos(r['R'], value(r), panel) for r in curves[0]], fill=colors[newton], width=4)
        for row in baseline:
            y = row['velocity'] if pi == 0 else 0
            x, py = pos(row['R'], y, panel)
            _, low = pos(row['R'], y-row['error'], panel)
            _, high = pos(row['R'], y+row['error'], panel)
            assert ymin <= y-row['error'] <= y+row['error'] <= ymax
            d.line((x, high, x, low), fill=grey, width=1)
            d.ellipse((x-3, py-3, x+3, py+3), fill=ink)
    for x, color, label in ((180, colors[0], 'Network response'), (590, colors[1], 'Newtonian, baryons only')):
        d.line((x, 668, x+46, 668), fill=color, width=4)
        d.text((x+59, 654), label, font=font(23), fill=ink)
    d.text((1120, 654), 'Dots: observed', font=font(21), fill=ink)
    d.text((650, 980), 'Radius (kpc)', font=font(22), fill=ink)
    d.text((104, 1020), 'Narrow shaded spans: four prescribed gas-tail variants, not confidence bands. No velocity fit.', font=font(19), fill=grey)
    im.save(out)
    law.save_new(ROOT / 'GALAXY_FIGURE_CUSTODY.json', {
        'script_sha256': law.sha(Path(__file__)), 'input_sha256': hashes,
        'figure_sha256': law.sha(out), 'plotted_rows_per_model': 43,
        'model_count': 4, 'mode': 'descriptive_no_fit_all_frozen_source_variants'})
    print(out)


if __name__ == '__main__':
    main()
