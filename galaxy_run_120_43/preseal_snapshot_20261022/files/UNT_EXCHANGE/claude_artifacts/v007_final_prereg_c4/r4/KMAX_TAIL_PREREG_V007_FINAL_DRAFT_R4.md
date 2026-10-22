# KMAX_TAIL_PREREG_V007: final draft r4 (UNSEALED)

FINAL DRAFT r4 (NOT SEALED). Assembled by Claude4 (dispatch 0583) from r3 07397846, integrating V005 A81 (the rulings on RI-19 to RI-26; open addendum observed 82b567bfa945ab5bcc9075c23e5925397a7dcaa74096bb20f739dcf253957e86 at assembly). Written before any V007 (tail-corrected) result exists; nothing was launched; C5H, UVT_* and targets were not read. Root fills the named seal slots and seals. One root item is open (RI-27, the prereg/compare pin cycle); nothing else is open.

**Assembly:** Claude4, single author, UTC 2026-10-18T17:56:01Z. Base: r3 `073978466df470bda3dccfa53da619df9835aeee6a7f217bbb2802045da6bf49`. Dispatch 0583 `854e1898c13a839ed07f1e85225dc9651f1c4e0e246cbd2fff1fac6898fa55fe`.

The full clause text is in the JSON; `CLAUSE_SOURCE_MAP_R4.md` traces every clause; `DELTA_R3_R4.md` lists the A81 edits.

## Seal slots (root fills at seal assembly; never guessed)

- **frozen_addendum**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Root exclusively creates the immutable copy at seal assembly, after the last pre-seal entry; the seal check verifies that every A-entry this text cites is present in the frozen bytes; its path and sha go to the binder and into the SEAL_RECORD. The frozen addendum must not cite the sealed prereg's sha (draft shas may be cited), or the pins would cycle (RI-27).  
  *Sources: 0576; 0574; RUNBOOK_V005 step 3; A78; A81 RI-26; RI-27 (draft)*
- **driver**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Path and full sha from bytes at seal; the SEAL_RECORD names it; the launcher refuses a plan whose driver differs (C4-S1, guard v008 / launcher v007); every identity run and every T-run carries driver_sha256 equal to it, and no T-run starts before the seal names it (A67 N1, extended to T-runs by A81 RI-24).  
  *Sources: A58 RI-01; A72; A67 N1; A78; 0574; A81 RI-24*
- **compare**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. The final compare round: r11, or the fix round r12 if r11's rechecks force one (A80). V007 seals on the round whose three recheck lenses and whose distinct reviews of record (Claude3 and Codex2) report 0 blocking (A81 RI-20). This slot holds that round's reviewed source, with its seal-time pin constants still unset (`None`; the bytes the reviews examined), path and sha. The sealed compare (V007_PREREG_SHA256 set to the sealed prereg sha, plus PIN_ADDENDUM_V005, PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK and PIN_PRODUCER_REGISTRY) is created after the sealed prereg and is named only in the SEAL_RECORD; it may differ from the reviewed source only in those pin lines (RI-27, as drafted; compare r10 L166: "set at the seal (the seal record then pins this script)").  
  *Sources: A79; A80; 0582; A75; A71; A58 RI-10; A81 RI-20; RI-27 (draft); compare r10 L150-166*
- **identity_comparator**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. The c2v007-lineage round whose own check and Codex2's review report 0 blocking (A81 RI-21); c2v004-c2v006 are superseded and not used at the seal.  
  *Sources: A68; A70; A74; A76; A81 RI-21*
- **identity_gate_records**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Only the identity-comparator slot round's outputs on the identity runs of the driver in the driver slot (Z2, Z2_OFF_RO1, B0prime_RERUN), using the A59 replace-mode tokens derived from that driver, with the raw successor-custody check; each carries driver_sha256 = the driver slot (A81 RI-21, A67 N1).  
  *Sources: A59; A67 N1; A72.3; A74; A76; A81 RI-21*
- **launch_packet**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. BUILD_V005 (46bc5b5d) with the bound plan and command that the build-only binder writes from the selected template, the chosen driver and the frozen addendum (exclusive create). The binder runs after the addendum is frozen and the driver is chosen, and before the SEAL_RECORD is written; the SEAL_RECORD names the bound plan and command shas; root verifies both from bytes immediately before running the command. A validate()-level template-equality check is optional and not required (A81 RI-25). The pending r5 template V010 refuses validation by design.  
  *Sources: A78; 0576; 0577; 0574; Claude4 0079; A81 RI-25*
- **certificates**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Root confirms each record of record at seal assembly; every record states source_gas_M_s where it depends on M_s, equal to the case block's gas.M_s, which must be 128 for DDO. LO_NGC is reported only in V007: the V007 LO_NGC slot takes the LO_NGC record of record that exists at seal assembly; coverage to 91 gates the NGC N-test compare (step 5), not the V007 seal (A81 RI-23). DOUBLING is one merged record, registered before the seal (A81 RI-22).  
  *Sources: A70; A67 SF2; A68; A73; A64.2; A58 RI-03; A79 NEW-67; A81 RI-22; A81 RI-23*
- **producer_registry**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY`. Root-registered producer paths and shas and the gate-record shas of record (A67 N2); the compare hashes the producer bytes, not only the claimed sha (A69.1); SR_K and every replay gate record bound to it (A62.2). Pinned in the compare as PIN_PRODUCER_REGISTRY (A67).  
  *Sources: A62.2; A67 N2; A67 (seal-time pins); A69.1*
- **cache_directory_r6_only**: value `PENDING_ROOT_AT_SEAL_ASSEMBLY (only if A72 adopts r6)`. A fresh, empty directory that root creates and names in the SEAL_RECORD; no pre-warming before the seal (the T-runs populate it, KHI first); every T-run records its cache mode and directory; the compare refuses a T-run whose mode or directory differs from the registered one (A81 RI-24).  
  *Sources: A72; A81 RI-24*

## Seal record requirements

- Before the seal the compare's gate and admissibility functions run on the real input records (the C5H receipt and result if present, the identity-gate records and the RO1 replay); their output goes into the seal record (E-SEAL1). *(A46 RA13)*
- Blinding: on C5H the gate functions run only as validity/admissibility booleans and reason codes, with no row value printed or written; the seal record states that no row value was shown. Record-controlled labels are redacted in blinded modes. *(A47 I3; A54 S6)*
- The compare pins at seal: V007_PREREG_SHA256 (this text once sealed), PIN_ADDENDUM_V005 (frozen V005 sha), PIN_REVIEW_V009 = the preserved original 3bce7c02, PRODUCTION_K_BIG_A55 = 128.0; its custody pins (PIN_RO1_CUSTODY, PIN_RO1_NODES_CUSTODY, the drivers_allowed I4 set) move to r5's re-pinned shas read from r5's BUILD record, verified from bytes. These seal-time pins (with PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK and PIN_PRODUCER_REGISTRY) are the only lines in which the sealed compare may differ from the reviewed source of the final round; the prereg names the reviewed source, the SEAL_RECORD names the sealed compare (RI-27, as drafted). *(0526; A53 (REVIEW_V009); A55; A56 (A55 follow-ups 1, 3); compare r5 NEW-26; RI-27 (draft))*
- Key-equivalence map: every key v010 adds that differs from v009 numerics appears with its absent/default value and B0 evidence. *(A48 AMB-13)*
- Order of record (0561; A81 RI-19, the erratum to A72 H-01, whose "its sha goes in the seal record" is superseded). At seal assembly root exclusively creates, in this order: (1) the frozen copy of the V005 addendum, after the last pre-seal entry (A81 RI-26); (2) with the driver chosen (A72), and under r6 a fresh, empty, root-created cache directory (A81 RI-24), the bound plan and command written by the build-only binder (0576; A81 RI-25); (3) the sealed prereg text, this draft with every seal slot filled; (4) the sealed compare (RI-27, as drafted); (5) the SEAL_RECORD, naming the sealed prereg sha (the first pin), the sealed compare, the driver, the frozen addendum, the bound plan and command shas and, under r6, the cache directory; (6) the ROOT_SEAL_ADMISSION config, pinning the SEAL_RECORD's full sha; (7) a separate SEAL_ADMISSION_RECEIPT naming both, posted in a numbered root packet. The RUNBOOK verifies the published config sha before invoking any source; records embed the config, seal and compare shas. No file is edited after it is created. Root verifies the bound plan and command shas from bytes immediately before running the command. *(0561; 0576; A72 (H-01); A78; 0580; A81 RI-19; A81 RI-24; A81 RI-25; A81 RI-26)*
- RI-10's adoption rule applies to every NEW item the final compare IMPL declares (adopted as text if stricter on adoption and gap-filling, rejected if looser); the IMPL lists each one with its disposition and its MUST_FAIL tests (A75), and the seal record quotes that list. *(A58 RI-10; A81 RI-20)*
- The raw successor-custody check of the Z2 run is recorded (A59). *(A59)*
- Disclosure E5-08: C5R3 ran the C5H driver and spec except for the label and fs overrides, so the C5R3 route-A fixtures the producers were tested on are very likely equal to C5H's route-A values, E^A included; they are not row values, and A47 I3 holds. *(A62 (E5-08))*
- Seal-time pins in the compare: PIN_ADDENDUM_V005 (the frozen copy), PIN_V010_R5_CHECK (or the r6 equivalent under A72), PIN_PRODUCER_REGISTRY; the custody pins follow the A77.2 role table read from the driver slot. *(A67 (seal-time pins); A72; A77.2)*
- CASCADE_MAP_R5_ADDENDUM (the immutable inventory addendum naming the unreachable pin-only successor) exists before the seal if the driver slot is r5. *(A69)*
- The root admission config names the BUILD_V005 launcher and guard sources exactly (the build check is a substring match). *(A78 N2)*
- Any A-entry after A81 that touches this text needs a successor revision or an explicit no-change note in the seal record; the seal check verifies that every A-entry this text cites is present in the frozen bytes. *(A81 RI-26)*

## Clauses changed in r4

- `seal_record_requirements.4` (rewritten): A81 RI-19/24/25/26
- `seal_record_requirements.5` (rewritten): A81 RI-20
- `seal_record_requirements.2` (extended): acyclic prereg/compare pins
- `seal_record_requirements[11]` (new): A81 RI-26
- `seal_slots` (slots rewritten): A81 slot rules; new slot cache_directory_r6_only
- `fixed_across_all_cases.production_tail.tail_table_cache` (extended): A81 RI-24
- `fixed_across_all_cases.production_tail.gas` (extended): A81 RI-23
- `gates_before_any_T_result.DOUBLING` (rewritten): A81 RI-22
- `gates_before_any_T_result.LO_NGC` (rewritten): A81 RI-23
- `ngc3198_N_tests.reading_gate_A81` (new): A81 RI-23
- `root_items` (resolved): RI-19..RI-26 resolved by A81
- `root_items.RI-27` (new): pin cycle found while ordering the checklist

## Root items

RI-19 to RI-26: RESOLVED by A81. OPEN: RI-27 (see `ROOT_ITEMS_R4.md`). Nothing else is open.

