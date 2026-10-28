"""Plot the fixed-time finite-size results without fitting or extrapolation."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
data = json.loads((ROOT / 'declared_path_dynamics_results.json').read_text())
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'svg.fonttype': 'none'})
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))
for Ud, color in [(1., '#176b93'), (4., '#c56924')]:
    models = sorted([m for m in data['models'] if m['Ud']==Ud and m['M_links']>=3], key=lambda m:m['M_links'])
    counts = [m['M_links'] for m in models]
    rows = [next(r for r in m['results'] if r['time']==4.) for m in models]
    axes[0].plot(counts, [r['nearest_neighbor_connected_covariance_mean'] for r in rows],
                 '-o', color=color, label=f'$U_d/h={Ud:g}$', linewidth=1.8, markersize=4)
    axes[1].plot(counts, [abs(r['end_to_end_connected_covariance']) for r in rows],
                 '-o', color=color, label=f'$U_d/h={Ud:g}$', linewidth=1.8, markersize=4)
axes[0].axhline(0, color='#6b7280', linestyle='--', linewidth=1, label='Independent controls: 0')
axes[0].set_title('Adjacent links develop correlations')
axes[0].set_ylabel('Mean adjacent occupation covariance')
axes[0].set_ylim(-0.01, 0.17)
axes[0].legend(frameon=False, loc='upper right', fontsize=9)
axes[1].set_title('Distant response depends on size and coupling')
axes[1].set_ylabel('Absolute end-to-end occupation covariance')
axes[1].set_yscale('log')
axes[1].text(0.03, 0.05, 'Independent controls are exactly zero\n(and cannot appear on a log scale).',
             transform=axes[1].transAxes, fontsize=8.5, color='#4b5563')
for ax in axes:
    ax.set_xlabel('Number of links M')
    ax.set_xticks([3,5,7,9,11,13,15])
    ax.grid(alpha=0.17)
fig.suptitle('First finite scaling sweep: a declared interacting path', fontsize=14, y=0.99)
fig.text(0.5, 0.015, 'Common blank; t = 4 in units of hbar/h; endpoint terms retained.\nFinite dynamics only: no EM identification or extrapolation to larger sizes.',
         ha='center', fontsize=9, color='#4b5563')
fig.tight_layout(rect=(0,0.09,1,0.94))
fig.savefig(ROOT/'scaling_correlations.svg', bbox_inches='tight')
fig.savefig(ROOT/'scaling_correlations_preview.png', dpi=140, bbox_inches='tight')
print('Saved scaling_correlations.svg')
