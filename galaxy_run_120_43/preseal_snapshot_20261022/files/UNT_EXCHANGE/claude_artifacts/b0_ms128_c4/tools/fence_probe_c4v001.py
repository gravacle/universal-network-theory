# Claude4 RI-31 (A113, dispatch 0650) fence smoke probe.  Run as SCRIPT under tools/run_fenced_c4st2.py before any driver
# child: it shows the runner's 8/8 fence selftest and v002 exception probes pass with this folder as review root, and that
# nothing is BLOCKED after the selftests.  It opens no file, spawns nothing and writes nothing.
import sys

sys.stdout.write('FENCE_PROBE_C4V001 OK\n')
