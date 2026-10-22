"""Named per-call caps for the sched_s45 v004 parameter files (Claude2 sched_s45_c2, caps_s45_c2v004).

caps_s45_c2v003 (6831829e) with the A166 change only (V006 addendum A166, 2026-10-19 19:21:38Z: memory gating is removed;
per-call RSS caps rise to physical RAM for every new launch; wall caps, output caps and the disk guard are kept):
  * RAM_BYTES = 137,438,953,472 B (128 GiB, the machine's physical RAM; A166);
  * DDO tail-ON RSS cap: 64 GiB -> RAM_BYTES;  DDO DIII tail-OFF RSS cap: 16 GiB -> RAM_BYTES;
  * unchanged: DDO_TAIL_ON_WALL_CAP_S (A140 N4, still the one named wall constant, PROVISIONAL until root re-derives it
    from the step-2 receipts), the orphan-wait margin, DDO_TAIL_ON_OUTPUT_CAP_BYTES (A140 N5, 80 GiB), the DIII wall
    (13 h) and output (96 GiB) caps;
  * removed: the NGC S0 / twin call caps (A166 build 2: the S0 kit C2V003 owns the NGC commands and their RSS = RAM).
build_params_s45_c2v004.py loads this module from its pinned bytes and writes every DDO per-call cap from these constants
and from nothing else.  N4 rebuild: copy this file to a NEW folder, change DDO_TAIL_ON_WALL_CAP_S (and its status text),
then run  build_params_s45_c2v004.py --caps NEW/caps.py --caps-sha256 H --out-dir NEW --tag S45_C2V005.
Importing this module does nothing.
"""
MODULE_NAME = 'caps_s45_c2v004'
GiB = 1 << 30
RAM_BYTES = 137438953472                 # A166: physical RAM (hw.memsize), the RSS cap of every new launch

# ---- N4 (A140): the single named DDO wall-cap constant.  PROVISIONAL: root sets it from the step-2 receipts before W1.
DDO_TAIL_ON_WALL_CAP_S = 100800
DDO_TAIL_ON_WALL_CAP_STATUS = ('PROVISIONAL_ROOT_SETS_FROM_STEP2_RECEIPTS: v002 value (28 h, DERIVED from the step-2 route-B '
                               'U 24,027 s); A140 N4: root re-derives it from the step-2 receipts before W1')
DDO_ORPHAN_WAIT_MARGIN_S = 600          # R9 relation kept: orphan_wait.cap_s = wall cap + 600 s

# ---- N5 (A140): DDO tail-ON per-call output cap (kept by A166: a full disk fails runs)
DDO_TAIL_ON_OUTPUT_CAP_BYTES = 80 * GiB
DDO_TAIL_ON_RSS_CAP_BYTES = RAM_BYTES    # A166 (was 64 GiB)

# ---- DIII tail-OFF: wall and output unchanged (R-D5); RSS = RAM (A166, was 16 GiB)
DDO_TAIL_OFF_CAPS = {'wall_cap_s': 46800, 'rss_cap_bytes': RAM_BYTES, 'output_cap_bytes': 96 * GiB}


def tail_on_caps():
    """DDO tail-ON per-call caps (campaign, HEADLINE, SENS, POST_S1) as ints."""
    return {'wall_cap_s': int(DDO_TAIL_ON_WALL_CAP_S), 'rss_cap_bytes': int(DDO_TAIL_ON_RSS_CAP_BYTES),
            'output_cap_bytes': int(DDO_TAIL_ON_OUTPUT_CAP_BYTES)}


def tail_off_caps():
    return dict(DDO_TAIL_OFF_CAPS)


def orphan_wait_cap_s():
    return float(DDO_TAIL_ON_WALL_CAP_S + DDO_ORPHAN_WAIT_MARGIN_S)
