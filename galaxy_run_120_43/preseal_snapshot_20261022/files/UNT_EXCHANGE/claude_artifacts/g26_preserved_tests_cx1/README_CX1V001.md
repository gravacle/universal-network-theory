A267 backlog6: G26 preserved-fixture test successors

Run either selected test with the fixed Python runtime -I -B and a fresh output directory. Both use the preserved c2v004 synthetic calibration/region bytes and their original sha256 values. The embedded historical region path remains in the calibration record; a strict test-only reader redirects that exact name to the preserved region. An independent audit hook denies all reads under the original temporary fixture root, including before inherited audit setup. The original inherited fixture audit continues to restrict process/network/file access. No G26 or scientific source changes.

Functional47/47; restoring mutants13/13 killed. The successor diff is confined to source-folder lookup, preserved fixture locations, strict legacy-read denial, and exact region read redirection. No original file changed. Review packet carries hashes of both original/selected tests, unchanged production source, manifest, fixtures and saved evidence.
