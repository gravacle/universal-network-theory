# Saved EPS certification census — CX2V001

Date: `Wed Oct 21 17:23:50 UTC 2026` (`/bin/date -u`).

TESTED: saved-record arithmetic and internal consistency. No EPS recomputation, solver launch, scientific admission, or run output access. Nice unavailable (sandbox); 0514 waiver.

Snapshot: 31/31 genesis records and 17/27 current-list records, each with178 shells. Missing current EPS and stage rows: [408, 409, 410, 411, 506, 507, 508, 509, 510, 511]. Missing means absent at this snapshot; completion or failure is UNTESTED.

A shell count is one point-specific shell instance. Terminal ratio is eps_refined/eps_base; initial ratio is saved level1/level0. Descriptive near bins do not propose a new rule.

| Cohort | Points | Shells | Terminal (1.05,1.10] | Terminal (1.09,1.10] | Terminal >1.10 | Initial >1.10 |
|---|---:|---:|---:|---:|---:|---:|
| genesis_31_certified_points | 31 | 5518 | 111 | 12 | 0 | 207 |
| current_all_available_points | 17 | 3026 | 62 | 5 | 3 | 128 |
| current_certified_points_only | 14 | 2492 | 47 | 1 | 0 | 112 |
| current_uncertified_points_only | 3 | 534 | 15 | 4 | 3 | 16 |
| all_certified_points | 45 | 8010 | 158 | 13 | 0 | 319 |
| all_available_points | 48 | 8544 | 173 | 17 | 3 | 335 |

Each uncertified point has exactly one uncertified shell; stored shell eps is dominated by eps_envelope in all three cases. The governing eps_max shell [4,5] is certified in each. These numerical facts are not a bound on unknown missed extrema.

- Row302, shell[46.0, 47.0]: base=1.086706276298699e-06, refined=1.2200030085063318e-06, terminal ratio=1.122661233412251; stored eps/envelope=1.90905655250706e-06; point eps_max=0.0002524697669156195; stored shell eps / eps_max=0.007561525389077993. Record `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P302_6f4604efe6d7fe34_W0003_P02_a1/EPS_NUMERIC_6f4604efe6d7fe34.json`, sha256 `3babf8f45719220ac161b5e784cb86e2684129e94be5715848088ae61910dc72`.
- Row501, shell[76.0, 77.0]: base=2.0515159770972957e-07, refined=2.2612939432065104e-07, terminal ratio=1.1022550974260659; stored eps/envelope=3.996529016614403e-07; point eps_max=0.00014427372487046952; stored shell eps / eps_max=0.0027701017771618007. Record `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P501_421cb796874019be_W0005_P01_a1/EPS_NUMERIC_421cb796874019be.json`, sha256 `52cc2502b60b53ad14a55fbb94f900e0a7d06e4f256233a9decbb5c48c33ab06`.
- Row504, shell[73.0, 74.0]: base=5.513229043296874e-07, refined=6.182243054153602e-07, terminal ratio=1.121347037390027; stored eps/envelope=1.1605583652984919e-06; point eps_max=0.00038653149525746944; stored shell eps / eps_max=0.003002493663615798. Record `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P504_cdc5592d149fa9ef_W0005_P04_a1/EPS_NUMERIC_cdc5592d149fa9ef.json`, sha256 `0005d1615277d4c48ab1c1541e9f7c059bb18d11fc13bb13a9da860202d4a3dd`.

All48 record/stage pairs agree on record byte pins, point keys,178 contiguous [4,182] unit shells, status and maximum. All31 genesis record hashes match registry pins. Final refinement fields agree with saved level pairs and saved certification decisions. All records expressly deny rigorous_supremum and production_admissible.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/census/CENSUS_CX2V001.json` — sha256 `d9659d9000b74390f49d9a10b2168ca3021e98ba6fbef4380dfe3fa5505d5756`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/census/INPUT_BYTES_CX2V001.json` — sha256 `2a3b96f15321dd1973cd451f06ad9db0e9bce896727c7abf5f3c52fbd0e4ba2e`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_consumption_cx2/census/census_eps_cx2v001.py` — sha256 `8fa7180e2385b5f6bea97f37a8c29ad717226ff531b9fdb52e105027f1ad7fc4`.

Every input cited by the calculations is listed with its path and bytes-derived sha256 in INPUT_BYTES_CX2V001.json, including the genesis registry and all EPS/stage records. The JSON retains per-point counts, exact failed-shell values, tight/wide bins, and the maximum certified terminal ratio per cohort.

