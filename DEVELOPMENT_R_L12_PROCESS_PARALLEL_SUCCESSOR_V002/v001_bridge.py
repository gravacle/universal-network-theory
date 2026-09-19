#!/usr/bin/env python3
"""Load the frozen V001 numerical kernels for the V002 publication wrapper.

V002 changes parent-side persistence and branch supervision only.  The worker
kernels and numerical semantics remain the already-reviewed V001 sources.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V001 = ROOT / "DEVELOPMENT_R_L12_PROCESS_PARALLEL_SUCCESSOR_V001"
if not V001.is_dir() or V001.is_symlink():
    raise RuntimeError("frozen V001 numerical packet is absent or unsafe")
if str(V001) not in sys.path:
    sys.path.append(str(V001))

parallel_runtime = importlib.import_module("parallel_runtime")
target_parallel = importlib.import_module("target_parallel")
hostile_parallel = importlib.import_module("hostile_parallel")
target = target_parallel.target
hostile = hostile_parallel.hostile

# Both frozen adapter modules temporarily prioritize their own directory while
# loading.  Restore V002's script directory as the import authority for all
# subsequent parent-wrapper imports, while leaving V001 available to spawned
# workers by module name.
while str(V001) in sys.path:
    sys.path.remove(str(V001))
sys.path.append(str(V001))
