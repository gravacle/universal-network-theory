"""Post-existing-data, source-only arithmetic; no force solve or fitted parameter."""
from pathlib import Path
import bisect
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
INPUTS = [ROOT / 'NGC3198_BARYON_INPUT.json',
          ROOT.parent / 'ngc3198_sparc_excerpt_v001.txt']
leroy = json.loads(INPUTS[0].read_text())['rows']
sparc = [line.split() for line in INPUTS[1].read_text().splitlines()
         if line and not line.startswith('#')]
lr = [row['radius_kpc'] for row in leroy]
ls = [row['stars_Msun_pc2'] for row in leroy]
sr = [float(row[2]) for row in sparc]
ss = [0.5 * float(row[8]) for row in sparc]

def interp(r, s, x):
    assert r[0] <= x <= r[-1]
    i = min(bisect.bisect_right(r, x) - 1, len(r) - 2)
    return s[i] + (s[i+1]-s[i])*(x-r[i])/(r[i+1]-r[i])

def annular_mass(r, s, a, b):
    """Exact integral of the declared linear interpolant, no endpoint model."""
    knots = [a] + [x for x in r if a < x < b] + [b]
    result = 0.0
    for left, right in zip(knots, knots[1:]):
        value = interp(r, s, left)
        slope = (interp(r, s, right)-value)/(right-left)
        width = right-left
        result += width*(left*value+(left*slope+value)*width/2+slope*width**2/3)
    return 2*math.pi*1e6*result

# Leroy C1 and SPARC M_sun,3.6 + IRAC channel1 Vega zero point.
luminosity_per_intensity = 1e4*10**(0.4*3.24)/280.9
conversion_ratio = 0.5*luminosity_per_intensity/280
rows = []
for radius, sigma in zip(lr, ls):
    if radius < sr[0]:
        continue
    comparison = interp(sr, ss, radius)
    rows.append({'R_kpc': radius, 'Leroy_Msun_pc2': sigma,
                 'SPARC_ML3p6_0p5_Msun_pc2': comparison,
                 'density_ratio': comparison/sigma,
                 'ratio_after_conversion_only': comparison/(sigma*conversion_ratio)})
inner = [row for row in rows if 3 <= row['R_kpc'] <= 8]
mass_comparisons = []
for a, b in [(0.32, 15.1), (2, 15.1), (3, 8), (8, 15.1)]:
    ml, ms = annular_mass(lr, ls, a, b), annular_mass(sr, ss, a, b)
    mass_comparisons.append({'annulus_kpc': [a, b], 'Leroy_Msun': ml,
                             'SPARC_ML3p6_0p5_Msun': ms,
                             'ratio': ms/ml,
                             'ratio_after_conversion_only': ms/(ml*conversion_ratio)})
result = {
    'role': 'exploratory source-only arithmetic after existing first coarse field; no validation or preregistration claim',
    'input_sha256': {str(p.relative_to(ROOT.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in INPUTS},
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'Lsun3p6_pc2_per_MJy_sr': luminosity_per_intensity,
    'SPARC_mass_per_intensity_ML0p5': 0.5*luminosity_per_intensity,
    'Leroy_equivalent_ML3p6': 280/luminosity_per_intensity,
    'same_imaging_same_geometry_mass_conversion_ratio': conversion_ratio,
    'hypothetical_cos73_over_cos72': math.cos(math.radians(73))/math.cos(math.radians(72)),
    'inner_3_to_8_kpc_density_ratio_range': [min(r['density_ratio'] for r in inner), max(r['density_ratio'] for r in inner)],
    'inner_after_conversion_only_ratio_range': [min(r['ratio_after_conversion_only'] for r in inner), max(r['ratio_after_conversion_only'] for r in inner)],
    'mass_comparisons': mass_comparisons,
    'all_22_comparable_Leroy_radii': rows,
    'omitted_Leroy_radius_kpc': 0.3,
    'omission_reason': 'SPARC excerpt starts at 0.32 kpc; no extrapolation invented'
}
print(json.dumps(result, indent=2, allow_nan=False))
