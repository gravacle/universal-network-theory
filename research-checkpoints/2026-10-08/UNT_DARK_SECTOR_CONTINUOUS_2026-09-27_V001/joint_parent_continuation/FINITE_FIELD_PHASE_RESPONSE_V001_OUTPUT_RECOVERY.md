# Finite-field output recovery — 2026-09-29

The first frozen V001 numerical launch exited 0 after approximately 8.5 seconds,
but its stdout exceeded the command tool's approximately 1 MiB retained-output
limit despite a requested 600,000-token output budget. The retained text contains
a tool truncation marker in its middle. It is not a complete scientific artifact.
The host JSON parser therefore refused it. The retained tail reports zero
failed controls, but neither that summary nor individual results qualify as
a complete authenticated scientific artifact from this truncated capture.

The producer source, prospective freeze, numerical controls, model and full
1,296-row census remain unchanged. The small rerunnable job is repeated solely
to recover the full stdout, with stdout_paged_capture_v001.py as a transparent
in-process output holder. It runs the exact source through runpy, captures stdout
in memory, and emits 32,768-character acknowledged pages with a whole-stdout hash.
It writes no files, launches no child process and imposes no scientific deadline.
Root reassembles the exact text and publishes it with apply_patch. This changes
output delivery, not scientific formulas, parameters, tolerances or acceptance.

The tool-visible first run's exit status is not being substituted for inspected
numerical evidence. Only a complete authenticated retained result and its review
can qualify this census. The first truncated attempt remains documented here.
