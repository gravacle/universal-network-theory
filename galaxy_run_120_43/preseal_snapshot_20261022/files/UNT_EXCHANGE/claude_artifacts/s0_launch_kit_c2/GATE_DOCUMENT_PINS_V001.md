# Gate-document pins for the S0 pre-launch V006 entry (M-15 (a)+(1)), C2V001

Built Mon Oct 19 16:25:33 UTC 2026 by the Claude2 root-workflow lane `s0_launch_kit_c2`. Machine copy: `GATE_DOCUMENT_PINS_V001.json` (`afa1df05bf6329997adccf160dc6fd56534c59b914332c264c79512df1e7ce36`). Every sha256 below was computed from the file's bytes at build time (TESTED) and equals the lane map's value.

## Why this entry is needed

- **TESTED:** V006 at build (`185486dc6c28a5f9fd45adb331667bb71a6f7f1afb9491a7e2905809ff62b9f5`) carries 0 of these 15 sha256 values in full; 4 appear only as 8-hex prefixes (`be148bab`, `07745bbf`, `1d5eef1b`, `3ae7981a`). M-15 (a) needs the sha256 pinned, so the entry must be appended **before the first step-5 NGC launch receipt** (the seed serial `.launch.json`).
- **FORMAL:** the strict r3a root-listed row-gate set (REGISTERED_INVALID_ROW_GATE_CX3V001) is empty. The entry still states the list, because a missing list is GATE_STATUS_LIST_DEFECT. A row gate first adopted later, at RUNBOOK step 4, is LATE by rule.
- The launch kit's `s0_prelaunch_record_c2v001.py` reads exactly these lines. Any line that starts with a pin keyword and does not match the form makes it refuse.

| Name | sha256 | Class | In V006 at build |
|---|---|---|---|
| NTEST_K32_COMPARE_COMPLETE | `6f095f64` | N_GATE_AND_M7_TSR_PIN | ABSENT |
| NTEST_N1_RING_RADII | `8867c376` | N_GATE_INPUT_AND_M7_TSR_PIN | ABSENT |
| ROUTE_B_GL4_NODES | `ec1dcca5` | ROW_RULE_INPUT_AND_M7_TSR_PIN | ABSENT |
| GQ_NGC_91_MS96 | `be148bab` | NUMERICS_CONDITION_I6 | PREFIX_ONLY_be148bab |
| LO_NGC_K32 | `07745bbf` | LAUNCH_CUSTODY_PIN | PREFIX_ONLY_07745bbf |
| EPS_NGC91_ANCHOR | `1d5eef1b` | ENVELOPE_SOURCE | PREFIX_ONLY_1d5eef1b |
| I1T_NGC_T120L | `3ae7981a` | NUMERICS_CONDITION_I6_D4 | PREFIX_ONLY_3ae7981a |
| S0_POINT_EPS_SEED | `efdc430a` | PER_POINT_CERTIFICATE_NUMERICS_I6_D4 | ABSENT |
| S0_POINT_EPS_J0 | `8270b6b3` | PER_POINT_CERTIFICATE_NUMERICS_I6_D4 | ABSENT |
| S0_POINT_EPS_J1 | `bfac8f57` | PER_POINT_CERTIFICATE_NUMERICS_I6_D4 | ABSENT |
| S0_POINT_EPS_J2 | `5dd9900a` | PER_POINT_CERTIFICATE_NUMERICS_I6_D4 | ABSENT |
| S0_GQ_BINDING_SEED | `903a7d6c` | PER_POINT_CERTIFICATE_CUSTODY_D4 | ABSENT |
| S0_GQ_BINDING_J0 | `cc6113ce` | PER_POINT_CERTIFICATE_CUSTODY_D4 | ABSENT |
| S0_GQ_BINDING_J1 | `4fc1d744` | PER_POINT_CERTIFICATE_CUSTODY_D4 | ABSENT |
| S0_GQ_BINDING_J2 | `934c0a47` | PER_POINT_CERTIFICATE_CUSTODY_D4 | ABSENT |

## Text for root to paste (replace `<n>` with the entry number; the parser takes the entry id from the `## A<digits>` heading)

````
## A<n>: pre-launch gate-document pins for M-15 (a)+(1); root-listed row gates known at launch: none

Pinned before the first step-5 NGC launch receipt (A142 item 6; M-15 (a)+(1); r3a section 4 L453-454). Each sha256 is from bytes (s0_launch_kit_c2 GATE_DOCUMENT_PINS_V001.json afa1df05bf6329997adccf160dc6fd56534c59b914332c264c79512df1e7ce36). Root-listed row gates known at launch: none (FORMAL: no REGISTERED_INVALID_ROW_GATE_CX3V001 document exists; any gate first adopted at RUNBOOK step 4 is LATE).

```
GATE_PIN NTEST_K32_COMPARE_COMPLETE 6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json
GATE_PIN NTEST_N1_RING_RADII 8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json
GATE_PIN ROUTE_B_GL4_NODES ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json
GATE_PIN GQ_NGC_91_MS96 be148bab4d80ef412d55d2011cac2e3a1d44725a0ba21a4d2bf43c7ffbdc1a76 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/GQ_NGC_91_MS96_V001.json
GATE_PIN LO_NGC_K32 07745bbf6d5c35d5a8568de7fc9e78b8c3bd8c3e371680dc8869c42a893c0382 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json
GATE_PIN EPS_NGC91_ANCHOR 1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json
GATE_PIN I1T_NGC_T120L 3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/I1T_NGC_T120L_V001.json
GATE_PIN S0_POINT_EPS_SEED efdc430a561ae936d860f85ec050f22a10f17c03aad7ad17fc2150744dcde563 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_968c915bece706ea_C4V002_s0seed.json
GATE_PIN S0_POINT_EPS_J0 8270b6b3eb9daddd01e32f7c6cc0fd143afd6b751ff9ced310ac92ca365586da /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_3d7785669b549d6f_C4V002_s0j0.json
GATE_PIN S0_POINT_EPS_J1 bfac8f57233e904aed30f68594645b5b9c97697e47ce088e9d18e7a8fe4aff1e /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_ab7bf95317b37652_C4V002_s0j1.json
GATE_PIN S0_POINT_EPS_J2 5dd9900a7db31003cb1b1054c156f6ac73b062375bae3a423990e782a2ccfdfc /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_4b9b4ec88eb2d94c_C4V002_s0j2.json
GATE_PIN S0_GQ_BINDING_SEED 903a7d6c88804bb99175ec78927184f210fa1fb07c32c985c294ef0546d0b979 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_968c915bece706ea_C4V002_gqseedA.json
GATE_PIN S0_GQ_BINDING_J0 cc6113ce39adaa3b24154848d099fec693aec15b91f09c3f9ca74299448d5f27 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_3d7785669b549d6f_C4V002_gqj0A.json
GATE_PIN S0_GQ_BINDING_J1 4fc1d744f2d0cb38a08d086aa8c20603bbd3b43c7c27a9a0d0d83665091402ca /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_ab7bf95317b37652_C4V002_gqj1A.json
GATE_PIN S0_GQ_BINDING_J2 934c0a4774b9153e7fbe25d72c743eff529079644f3fdc03ab060dc25833f3e0 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_4b9b4ec88eb2d94c_C4V002_gqj2A.json
ROOT_LISTED_ROW_GATES NONE
```
````

## Lines for the RI45-09 / RI45-13 entries (same parser; written when the values exist)

- RI45-09, after `phase1_point_handoffs_c2v001`: `HANDOFF_PIN S0_SEED <sha256 of the seed handoff> <its absolute path>` (and `S0_J0`, `S0_J1`, `S0_J2`).
- RI45-13, after the DRY run of `launch_s0_serial_root_c2v001.sh` prints the filled spec sha: `SPEC_PIN S0_SEED_SERIAL <sha256> <absolute path of the DRY fill>` (and `S0_J0_SERIAL` …, `S0_SEED_CW8_TWIN`).
- A135.5: `WATCH_PIN MEMORY_WATCH <sha256> <absolute path of the NGC-extended GiB watch script>`.
- For the seed launch, every line it needs (all GATE_PIN lines, ROOT_LISTED_ROW_GATES, HANDOFF_PIN S0_SEED, SPEC_PIN S0_SEED_SERIAL, WATCH_PIN) must be in V006 before the M-15 record. V006 is then write-frozen until the seed's `.launch.json` exists. The J and twin lines may follow after that.
