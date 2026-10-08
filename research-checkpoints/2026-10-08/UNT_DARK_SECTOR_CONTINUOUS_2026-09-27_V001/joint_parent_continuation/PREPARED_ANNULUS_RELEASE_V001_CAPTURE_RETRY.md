# Unchanged worker retry for complete stdout capture

2026-09-29. The first frozen worker exited zero and its retained tail reports
COMPLETE. The command-output tool applied a byte cap despite its large token
allowance: 1,048,606 characters were returned with the middle removed. That
capture is not parseable JSON and is preserved in CAPTURE_TRUNCATED.txt.

The exact same frozen worker is rerun without changing inputs, algorithm,
tolerances or census. A read-only wrapper compresses its complete stdout as
zlib/base64 for transport below that output cap. The wrapper records the exact
uncompressed length and SHA-256; root then reads/decompresses its published
transport artifact in bounded chunks and assembles the complete result using
apply_patch. No worker writes files. This addresses transport truncation,
not a failed physical outcome or a scientific retry selected for success.
