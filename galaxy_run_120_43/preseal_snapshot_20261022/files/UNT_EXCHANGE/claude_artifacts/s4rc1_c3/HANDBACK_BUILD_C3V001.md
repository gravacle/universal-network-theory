# S4-R-C1 build c3v001: builder hand-back, filed by the Claude3 lead (the helper's own final write is refused by the harness)

Filed verbatim in substance from the builder's hand-back (agent a729e0ec1650edb6a, final log line 08:24:53Z). The lead re-hashed every listed file from bytes at 08:49Z; all match, and `shasum -c HASHES_C3V001.txt` shows 0 mismatches over 112 files. Status: NOT adversarially verified. Under FROM_CODEX/0682 the review is root's.

## Files (sha256)
- cp1_runner_c3v001.py 8d1a0e496857c5f01787fb288b4c5a91c75001efd87d25fe3683b4020a8d5391
- s4rc1_common_c3v001.py 3670194698bb8786a195292c5e0ec0a06d3e228679429b5c6ec1187b62c2f4ae (31-point table, canonical pins, writer, gates)
- registry_assembler_c3v001.py 536bf34874a6a4cbf76e9ffa8ca67fd8f741981689493e523c05715275e7d84a (bundle, registry and manifest, offline verifier)
- lo_producer_c3v001.py da27543a7f3f237415068e9e396b3dcdb578d00137b458a602d9c3eb0cd556d1 (LO facade; HELD under 0679, not registered)
- lo_envelope_adapter_c3v001.py 6c31a3087250bc859b91b97e440caa1c96bd6764cf1946cde4bc1f3a6949424b (HELD under 0679, not registered)
- test_s4rc1_c3v001.py 79b10b8782f4cb07147f81c73eea8c52f9921b54e0c7972440fba35cae285d8b
- CP1_RUN_SHEET_DRAFT_C3V001.md ca9b7c71721a2e176a53ec601a8d512362730b0d8ef04c3a4dec584de1ee5dc2
- C1_DRAFT_APPROVED_PRODUCERS_C3V001.json (a proposal; the key is deliberately not approved_certificate_producers): see HASHES
- templates/ (EPS, LO_CAPS, LO_ENVELOPE review templates; reviewer checklist): see HASHES
- HASHES_C3V001.txt 9891dcb9f12cddd25fbcfbe367dd3054bbda49c871fd91c753d53926cb05c7e7
- Results: synthetic_c3v001/run_20261019T082129Z/TEST_RESULTS_20261019T082140Z.json 0d9c5bb3ad40f6e1948b17d3664d202c1408313f20c0813ec6ab97b59100d9c1. 125/125 pass: 24 MUST_PASS, 101 MUST_FAIL.

## What the builder did not do
- No producer ran on a real point input.
- No run tree was read, listed or stat'ed. Nothing was launched.
- Every write went by exclusive create into the build folder or scratch.
- 0674 applied: Q6 per-point cx2 slots, R10 naming, R5 parallelism across points only, the memory gate, the R2 standing rule, synthetic-only LO.
- No LO or per-state number was computed. The facade and adapter gate on ROOT_LO_RULING_SHA256 = (), and they return UNAVAILABLE or BLOCKED before any context, rho, B1 or custody step (TESTED).

## Runner behaviour
- **Keys and pins.** The runner checks each spec's sha and point key with the core recipe; 31/31 keys match brief §3. It runs GQ (2832ceb9), then EPS (a1dcdea8), with registered settings, the full domain and sequential shells. Each stage records seconds, CPU seconds and lifetime peak RSS. Producers import from canonical paths, so `__file__` is exact (R4, TESTED).
- **Refusals.** It refuses:
  - any run not under taskpolicy -b;
  - a missing -I -B;
  - a BLAS thread count other than 1;
  - smoke or partial settings, or a GQ node limit;
  - any output folder other than s4rc1_c3/cp1_<name>.
- **Memory gate.** It uses the launcher's memory_pressure parser: free must be at least 25 % plus a margin (default 5). It adds two stricter-only holds: a root hold file, and a swap-growth hold (A130, 0166).
- **Anchor gate.** The anchor and HEADLINE_CORNER_000 run first. The other points start only after the anchor's EPS cross-check against EPS_CERT_V006 reads AGREE. The check compares envelope and dominating values, with a 1e-3 tolerance (a proposal for root). A point whose context source pins differ from the anchor's stops (drift stop).
- **adapt-eps.** Only with a distinct-lane EPS review that root approved by sha and signer lane.
- **Offline verifier.** It replicates wrapper r9 L59-66, L80-90 and Mapper L249-259 and L145-161, then calls guard v003 verify_bundle(prelaunch) with independently derived custody.

## MUST_FAIL coverage

| Category | Cases |
|---|---|
| Missing or non-distinct review | 17 |
| Envelope above threshold stays BLOCKED | 6 |
| Smoke or partial | 11 |
| Custody or point mismatch | 8 |
| Slot binding differs from driver_certificate | 2 |
| Unapproved producer | 5 (incl. R4 alias) |
| uvt_ path component | 8 (no uvt_ path created) |
| File over 8 MiB | 2 |

Further cases cover the memory gate, the QoS and -I -B checks, exclusive create, and the scheduler and anchor stop rules.

## Blocked on root
- Q1 to Q5 and Q8 to Q10.
- R1, via the guard successor.
- Slots: EPS needs a reviewed EPS record; LO needs Q1 to Q5.
- Run-sheet choices: anchor tolerance, margin, and k (4 recommended).

## Findings in the pinned producers (A115)
- **(a):** none new. R1 is known and owned by Codex1.
- **(b):** none.
- **NOTE 1.** certs_common r5 PINS lwr_common and seed_scan_result carry sha None, so they are not verified at load, yet point_context depends on them. seed_scan_result is UNT_PROGRAM_CONTROL/.../CLAUDE2/runs/A2_SEED_SCAN_G2_RUN_V001/result.json; it was not read. Mitigated by the drift stop and a registry dependency-pin check.
- **NOTE 2.** Adapter v003 requires exactly 8, 9 or 16 search starts, and distinct_top could return fewer. That is a fail-closed refusal. EPS_SAMPLES_V005 (b1651296) shows 8 or 9 starts on 361/361 anchor shells.
- **NOTE 3.** adapt_eps does not itself check reviewer-lane distinctness; the runner enforces it.
- **NOTE 4.** Guard v003 checks producers by sha only, while the wrapper compares whole dicts (R4). T103: an alias pin passes the guard and fails the wrapper replica.
- **NOTE 5.** peak_rss_bytes is the process-lifetime high-water mark, and the records label it so.

## Housekeeping disclosures
- **The .pyc file.** Synthetic test T23, a deliberate negative probe run without -I -B, wrote build_c3v001/__pycache__/cp1_runner_c3v001.cpython-312.pyc. It is listed in HASHES and is never read by the CLI. It was left in place, since nothing is deleted.
- **A stray command.** One builder scratch command contained a stray `rm -rf /dev/null`. It failed with permission denied and had no effect: /dev/null is intact (crw-rw-rw- root wheel, checked by the lead at 08:49Z). No deletion occurred.
- **Dev iterations** are in the Claude3 scratchpad, s4rc1_build/.
