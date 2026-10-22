# GATE_B3_C4_V001 — gate B3 (independent-lane Cartesian check of the tail implementation). Single reviewer: every numeric tolerance **PASS**; the two stage-wired items NOT RUN

Claude4 main session, single reviewer, inline; 2026-10-18T11:42:24Z (`date -u`). Dispatch `FROM_CODEX/0507` (3845e286…). No launches, read-only elsewhere, C5H not read. Outputs are small (≈ 1 MB total).

## Objects (sha256 from bytes)

- **Module:** lapse `c28d4209…`, roster `4366e3d6…`, Jn `d6c55b55…`, all pinned at run time.
- **State:** saved C4R3 `KMAX_A2F10_C4R3_D7R3_RUN_V001`.
  - result `aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee`;
  - le3 source rotation `stages/15_le2_rotation/rotation/rotation_base_arrays.npz` `4e53085c8dc1d44b8a83a46eff4ae595ee3a64068ce544ba928d8b2abf9693cf`;
  - γ = 2.98639171e41.
- **Registered source definitions:** profile f5becd45 and forward_v002 `radial_surface` e9be043b.
- **Line and HI modules:** line v002 3a47419d, HI v003 b176c7a6.

## Independent lane: `tools/b3_independent_v001.py` (`7464972d249d92865b5201f39ff0e6cabaa4ff6dedd82603f1e88bd43af7ccbd`)

**No tail library is imported.** An AST scan finds only hashlib, importlib, json, math, sys, time, pathlib and numpy. The one dynamic import is the registered forward model's `radial_surface`, which is a source definition, not the tail library.

**Built myself:**
- J0 from the integral representation;
- the stars Hankel transform: GL24 node segments plus a 60·Rd exponential tail;
- the gas rule: cubic Lagrange in s through the GL4 nodes, integrated in R;
- σ_i(k_z) from the saved le3 masses (m = Σ_φ vol·ρ0).

**Unit checks:**
- column R and R dR match the saved arrays (0 and 2e-16);
- the stars mass is 11,925,050.0495 M☉;
- the gas mass is 427,005,912.887 M☉, equal to Σm;
- the k_⊥ table interpolates to 6e-15.

**The two cases:**
- **CUBE**, D = box(8)\cube(4). Cartesian tensor GL24 with 768 nodes per axis in k_x, k_y and 960 in k_z. No symmetry reduction.
- **CYL**, D = cyl(K_big 8)\cube(4). Integrated in (k_⊥, ψ, k_z):
  - corner zone 4 < k_⊥ ≤ 4√2 through the exact ψ limits (4 arcs of half-width arccos(4/k_⊥)), with k = 4 + u²;
  - a periodic trapezoid on full circles;
  - no Bessel series.

**Doubling.** Halving every panel converges to ≤ 3.0e-15 (cube) and 1.2e-15 (cylinder), against the gate's 1e-10.

## Comparison: `tools/b3_compare_v001.py` → `out/B3_COMPARE_V001.json`. **32/32 PASS**

**Points.** The route-A column points:
- 72 GL4 radii × 8 route-A azimuths × z ∈ {0, 0.01, 0.05, 0.2, 1, 5, 20, 32} kpc for the jets;
- all 16 azimuths for the values and pairs.

The module side is built as in the module lane's pre-gate E (roster_rotation M_s 64, w⊥ 0.05, w_z 0.035).

| B3 tolerance | cube(8) | cyl(8) |
|---|---|---|
| value ≤ 1e-8 of max | 4.7e-15 | 4.9e-15 |
| gradient ≤ 1e-7 | 4.7e-15 | 3.1e-15 |
| Hessian ≤ 1e-6 | 4.3e-15 | 2.3e-15 |
| lapse pair b0 ≤ 1e-8 max\|t\| | 6.5e-15 | 3.6e-15 |
| lapse pair bd ≤ 1e-8 max\|t\| | 7.7e-15 | 5.1e-15 |
| bd(z = 0) exactly 0.0, signbit clear (1152 points) | 0 nonzero | 0 nonzero |
| facade midplane log ratio exactly 0.0 (line v002, 8 columns) | exact | exact |
| line v002 log ratio and N0, module pair against independent pair | 6.0e-15 | 6.0e-15 |
| HI v003 L67–68 condition | passes | passes |
| imaginary part: evaluate_line with tail jets equals zeros bitwise; jets float64 | exact | exact |
| tail potential-difference proxy c²·⟨bd⟩_16φ ≤ 1e-7 | 4.9e-15 | 4.5e-15 |
| independent imaginary part (relative) | 2.6e-16 | 1.8e-16 |

## NOT RUN here, so B3 is not complete on these two items

1. **Reference/body angular reads by TailBoundary tap** (≤ 1e-7 max\|grad t\|).
2. **The fs-columns successor potential(z)** (≤ 1e-7 of the max tail potential difference). The proxy above is what was checked.

**Why.** Both need a replay of C4R3's reference, body and fs-column *successor stages* with the tail ON and `uv_tail_tap > 0`. No existing replay recorded a tap: the route-B replays ran on the K = 2 deciding chain with tap 0.

**What closes them.** `tools/b3_independent_v001.py` evaluates any position. Given `uv_tail_tap.npz` files from such a replay, plus the fs-column potential(z) arrays, I can return the comparison in minutes. Root to decide who runs the replay.

## Disclosures

- **0052 toys.** No code was imported from them. Two methods were reused and the code rewritten: exact-arc ψ integration, and the integral-representation J0.
- **Pre-fix cube run.** The first cube runs used a pre-fix script (sha 49225003…). The fix was a cylinder-loop header only. All outputs were rerun with the final script 7464972d.
- **Load.** nice -n 10, at most 3 processes, single-thread BLAS. Every run took ≤ 130 s and ≤ 0.8 GB.
