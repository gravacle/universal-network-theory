# Output-capture retry, unchanged numerical experiment

Source 00 finished with exit code0 and reported COMPLETE, but its 54,110-token
stdout exceeded the caller's 35,000-token capture allowance. The tool retained
only a truncated representation, so no authenticated result JSON could be
published from that capture. The received output is preserved as
HALO_COMPARATOR_V002_SOURCE_00_CAPTURE_TRUNCATED.txt.

The same frozen V002 worker is rerun with a larger caller output allowance.
No code, input, parameter, row, objective, search, tolerance or freeze changes.
This is a technical capture retry; the incomplete capture is not scientific
acceptance. All subsequent source results are captured with the same larger
allowance and saved before proceeding to the next source.
