"""Parse primary baryonic profiles; never turn absent measurements into zero."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT/'leroy2008_table7.dat'


def optional(value):
    return float(value) if value.strip() else None


def mass_piecewise_linear(radius, surface):
    """Msun for kpc radii and Msun/pc^2, exact on linear density segments."""
    value = 0.
    for left, right, sigma, next_sigma in zip(radius, radius[1:], surface, surface[1:]):
        width = right-left
        delta = next_sigma-sigma
        value += width*(left*sigma+(left*delta+width*sigma)/2+width*delta/3)
    return 2*math.pi*1e6*value


def main():
    fields = {'radius_kpc': (9,13), 'radius_over_r25': (14,18),
              'HI_Msun_pc2': (19,24), 'HI_rms': (25,28),
              'H2_Msun_pc2': (29,35), 'H2_rms': (36,40),
              'stars_Msun_pc2': (41,48), 'stars_rms': (49,54)}
    rows = []
    for original in RAW.read_text().splitlines():
        line = original.ljust(82)
        if line[:8].strip() == 'NGC 3198':
            row = {key: optional(line[a:b]) for key,(a,b) in fields.items()}
            row['raw_line'] = original
            rows.append(row)
    assert len(rows) == 23
    assert all(rows[i]['radius_kpc'] < rows[i+1]['radius_kpc'] for i in range(22))
    assert rows[2]['stars_Msun_pc2'] == 105 and rows[2]['stars_rms'] == 1
    assert sum(row['H2_Msun_pc2'] is None for row in rows) == 13
    summaries = {}
    for component in ('HI','H2','stars'):
        present = [row for row in rows if row[component+'_Msun_pc2'] is not None]
        radii = [row['radius_kpc'] for row in present]
        values = [row[component+'_Msun_pc2'] for row in present]
        annular = mass_piecewise_linear(radii, values)
        # Not an observation: retain this tiny unmeasured central disk separately.
        flat_core = math.pi*1e6*radii[0]**2*values[0]
        log_mass = {'HI':10.1, 'H2':8.8, 'stars':10.1}[component]
        summaries[component] = {
            'profile_radial_range_kpc': [radii[0],radii[-1]],
            'profile_annular_mass_Msun_linear_interpolation': annular,
            'unmeasured_core_mass_Msun_if_flat': flat_core,
            'measured_profile_plus_flat_core_Msun': annular+flat_core,
            'table4_aperture_kpc': 19.5,
            'table4_mass_Msun_from_rounded_log': 10**log_mass,
            'table4_rounding_only_mass_interval_Msun': [10**(log_mass-.05),10**(log_mass+.05)],
            'table4_minus_profile_and_flat_core_Msun': 10**log_mass-annular-flat_core,
            'warning': 'Not a tail detection or limit: profile interpolation, central model, conversion systematics and rounded aperture masses differ.'}
    payload = {
        'galaxy':'NGC 3198', 'role':'exposed development input; no velocity scoring',
        'sources_sha256': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                           for name in ('leroy2008_table7.dat','leroy2008_table4.dat',
                                        'leroy2008_ReadMe.html','prepare_galaxy_input.py')},
        'conventions': {'distance_Mpc':13.8, 'inclination_degrees':72,
                        'gas_helium_factor_already_included':1.36,
                        'stellar_ML_K_band':.5,
                        'missing_H2':'null, not measured zero',
                        'RMS_1_with_present_density':'numeric scatter, not upper-limit flag'},
        'rows':rows, 'mass_accounting':summaries,
        'remaining_source_choices':['central continuation','outer gas and stellar continuation',
                                    'missing molecular-gas treatment','vertical geometry/warp']}
    destination = ROOT/'NGC3198_BARYON_INPUT.json'
    with destination.open('x') as stream:
        json.dump(payload,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')
    print(json.dumps(summaries,indent=2))


if __name__ == '__main__':
    main()
