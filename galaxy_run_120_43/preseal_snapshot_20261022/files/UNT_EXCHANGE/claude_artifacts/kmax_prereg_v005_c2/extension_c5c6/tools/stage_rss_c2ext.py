"""Post-hoc (read-only): peak sampled tree RSS of saved monitored runs, split into the route-A window and the rest.
Route-A window = [0, mtime(stages/01_route_a/attempt_000/finish.json) - receipt utc_start]; for admitted-prefix runs
(no computed route A) everything is route B. Samples are the monitor's own (poll 2 s, tree RSS via ps). Prints JSON."""
import json, sys, os, datetime
from pathlib import Path
R = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
out = {}
for name in sys.argv[1:]:
    rec = json.loads((R / (name + '.receipt.json')).read_text())
    t0 = datetime.datetime.strptime(rec['utc_start'][:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc).timestamp()
    fin = R / name / 'stages/01_route_a/attempt_000/finish.json'
    ra_end = (os.stat(fin).st_mtime - t0) if fin.is_file() else 0.0
    s = [x for x in rec['samples'] if x[1] is not None]
    ra = [x[1] for x in s if x[0] <= ra_end]
    rb = [x[1] for x in s if x[0] > ra_end]
    out[name] = {'elapsed_s': round(rec['elapsed_seconds'], 1), 'route_a_window_s': round(ra_end, 1),
                 'peak_rss_bytes': rec['peak_rss_bytes'], 'route_a_peak_rss_bytes': max(ra) if ra else None,
                 'route_b_peak_rss_bytes': max(rb) if rb else None, 'peak_output_bytes': rec['peak_output_bytes'],
                 'caps': rec['caps'], 'n_samples': rec['n_samples'], 'samples_cover_run': bool(s) and s[-1][0] >= rec['elapsed_seconds'] - 10}
print(json.dumps(out, indent=1))
