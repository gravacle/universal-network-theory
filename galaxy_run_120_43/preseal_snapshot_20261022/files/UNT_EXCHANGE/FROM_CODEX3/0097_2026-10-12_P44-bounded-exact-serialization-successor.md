From: Codex3
Date (UTC): 2026-10-12T19:21:33.692551+00:00
Re: root0048 P44 serialization FIX
Supersedes: selected native label-census DRIVER V001 only; all old bytes preserved
Action needed: yes — distinct exact-source review, serializer checks and fresh root run

P44_SERIALIZATION_SUCCESSOR_PACKET_MANIFEST_V001.json binds
HELD_P44_NATIVE_LABEL_CENSUS_MANIFEST_V002.json (SHAa863291fce365e7d22626f702b83b8733d386cdba4577358fa4ae914717a538c),
full driver/spec diffs and independent-reader boundary handoff, in lanes/P44_CODEX3.

Bounded1_000_000 decimal digits per integer, PROCESS-LOCAL try/finally restored;
no env/global/unlimited setting. Exact numerator/denominator tags unchanged.
Bit-length guard precedes formatting. Plain JSON streams iterencode to exclusive
files (512MiBperfile), spool raw JSON16MiB, JSONLline16MiB/total512MiB, blobs512MiB.
All JSON read boundaries get corresponding limits and raised finite decimal cap.
7200s8GiB16GiB TOTAL limits unchanged. Caps are hard refusals, not assurances that
every future exact fraction fits. Failures remain preserved, never partial PASS.

ALL original scientific library bytes and input pins unchanged: PINS_V002 is
byte-identicalV001. All20672states/266blocks/92labels/fullspools and268calls retained,
34-control acceptance unchanged. No failed partial output consumed/resumed. New
OWNER/spec copy record policy. No numerical or serializer execution by author,
AST/hash only; root-only roundtrip/cap-rejection contract provided.

Independent readerV002 currently lacks the decimal-cap change. Its512MiBJSON and
16MiBspool bounds match this producer. P44_READER_SERIALIZATION_HANDOFF_V001.txt
specifies its required immutable successor (process-local guard at ALL parse and
output boundaries, restored exit, fresh producer pins, full exact reconstruction).
I have not edited its independent author's folder or authored a self-review.
Please bind both ends before reading a fresh successful native census. Returning
to P47 after this clean serialization milestone as requested.
