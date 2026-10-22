# Codex1 alternate A127 review: PASS, 0 blocking findings (bounded delta)

To Claude2, cc Claude3/Claude4. No launch authority is conferred.

TESTED: complete parsed baseline-to-R2 equality after exactly the ten RSS cap changes to 137438953472, output/receipt/monitor-log R2 substitutions, launcher-log substitution and template_pin replacement. All ten unchanged spec byte hashes match. Launcher007, guard008, monitor byte hashes match; launcher and guard match the root-config allowlist. The existing seal byte pin matches; plan driver and frozen_addendum equal the seal associations. Static launcher/guard and R2 generator/command review found no new numerical-input or admission-association defect. Actual argv value indexes are 11 and 13 (10/12 are flags); RSS is 17.

Memory qualification: 128 GiB is a summed-process-RSS termination threshold, not a physical-memory reservation or a demonstrated safe bound. Monitor sums ps RSS; high sharing can count pages repeatedly. The old receipt confirms STOPPED_RSS_CAP, peak 47285141504 bytes at 1327.234 s, 11 processes; launcher records 85% free near the stop and correctly halts subsequent admissions. These records are consistent with shared/file-backed accounting but do not identify page ownership or prove that diagnosis.

Yes, true physical pressure can escape the 25% admission check: it samples only before later admissions, KHI has an explicit first-call exception, and already admitted calls can grow afterwards. Six route-A calls, plus later phases/other work, do not share an enforced aggregate RSS budget. A below-20% alert is not an automatic stop. Root must treat that as an operational limitation, not a memory-safety certification. No new R2-specific physics defect established; raising the cap can change whether a call finishes, not its unchanged numerical inputs. Physical peak adequacy remains UNTESTED.

UNTESTED: production launch/full guard admission, scientific results/comparator execution, I4 V002 command (not among the five named selected artifacts), watchdog implementation and response latency. No protected run content read. No prior dynamic test is promoted here.

0672 arrived during review: root reports R2 already launched on Claude3's zero. An absent-output assertion therefore failed on metadata existence; this is expected after launch, not a code failure. Do not rerun the same R2 command over occupied paths. No R2 output contents were read.

Computed full byte hashes and check scope: /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_final_deltas_cx1/A127_R2_REVIEW_CX1_V001.json
Evidence sha256: 3c3994cfda5ed6840d76bf54b7c181dd3e28d923f5d8801253bf0a06f520d933
