"""Read-only, standard-library reconstruction of a published Newtonian residual.

Exploratory arithmetic, not a UNT prediction, fit, likelihood, or scored gate.
All NGC3198 rows retained. Printed examples use nearest radii to 10, 20, 40 kpc
(ties choose lower radius), rather than selecting by residual. Baseline M/L=0.5
is an adopted illustrative SPARC convention, not a measured value or UNT input.
Sensitivity values 0.2, 0.7, 1.0 are diagnostic, not a confidence interval.
No network/Monte Carlo/subprocess activity, no generated files. At most 100 rows,
16 KiB input, and five CPU seconds; exact rational intermediate arithmetic.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import sqrt
from pathlib import Path
import resource

resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
data_path = Path(__file__).with_name("ngc3198_sparc_excerpt_v001.txt")
if data_path.is_symlink() or data_path.stat().st_size > 16384:
    raise ValueError("Unexpected input route or size")
raw = data_path.read_bytes()
rows = []
for line in raw.decode("ascii").splitlines():
    if line.startswith("#") or not line.strip():
        continue
    fields = line.split()
    if len(fields) != 10 or fields[0] != "NGC3198":
        raise ValueError("Unexpected source row")
    row = tuple(map(F, fields[1:]))
    distance, radius, speed, error, gas, disk, bulge, sb_disk, sb_bulge = row
    if distance != F("13.8") or radius <= 0 or error < 0 or disk <= 0 or bulge != 0:
        raise ValueError("Unexpected source value")
    rows.append(row)
    if len(rows) > 100:
        raise ValueError("Input bound exceeded")
assert len(rows) == 43
assert all(a[1] < b[1] for a, b in zip(rows, rows[1:]))
assert rows[0][1] == F("0.32") and rows[-1][1] == F("44.08")

def signed_square(value):
    return value * abs(value)

assert signed_square(F("-1.43")) == -F("2.0449")

def calculate(row, mass_to_light):
    _, radius, speed, error, gas, disk, _, _, _ = row
    bar2 = signed_square(gas) + mass_to_light * signed_square(disk)
    if bar2 <= 0:
        raise ValueError("No inward baryon-only circular speed at this radius")
    observed2 = speed * speed
    residual2 = observed2 - bar2
    ratio = observed2 / bar2
    required_ml = (observed2 - signed_square(gas)) / signed_square(disk)
    # Exact independent reconstruction and units cancellation checks.
    assert signed_square(gas) + required_ml * signed_square(disk) == observed2
    assert ratio == (observed2 / radius) / (bar2 / radius)
    assert residual2 + bar2 == observed2
    return bar2, residual2, ratio, required_ml

print("EXPLORATORY REFERENCE INFERENCE ONLY; NOT UNT VALIDATION")
print("input_sha256", sha256(raw).hexdigest())
print("rows", len(rows), "inclination_deg=73 (catalogue); baseline_ML=0.5")
print("R_kpc Vobs_kms Vbar_kms gobs_over_gbar residual_v2_kms2 required_template_ML")
for row in rows:
    bar2, residual2, ratio, required_ml = calculate(row, F("0.5"))
    print(f"{float(row[1]):.2f} {float(row[2]):.2f} {sqrt(float(bar2)):.6f} "
          f"{float(ratio):.6f} {float(residual2):.6f} {float(required_ml):.6f}")
print("DISPLAY_ROWS_NEAREST_10_20_40_KPC")
for target in (10, 20, 40):
    row = min(rows, key=lambda r: (abs(r[1] - target), r[1]))
    fields = [f"R={float(row[1]):.2f}"]
    for ml in ("0.2", "0.5", "0.7", "1.0"):
        _, _, ratio, _ = calculate(row, F(ml))
        fields.append(f"ML={ml}:ratio={float(ratio):.6f}")
    print(" ".join(fields))
negative = [float(r[1]) for r in rows if calculate(r, F("0.5"))[1] < 0]
print("negative_residual_radii_kpc", negative)
print("No residual clipped; no full observational uncertainty or significance calculated.")
