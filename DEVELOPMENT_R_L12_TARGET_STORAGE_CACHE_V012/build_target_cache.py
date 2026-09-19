#!/usr/bin/env python3
"""Hard-locked builder for the target V012 portable storage-only index cache."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import resource
import shutil
import stat
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V004_DIR = ROOT / "DEVELOPMENT_R_L12_PREFIX_HISTORY_ENGINE_V001"
sys.path.insert(0, str(V004_DIR))
import compute_prefix_history_v004 as v004  # noqa: E402


METHOD = HERE / "METHOD.md"
CONSUMER = HERE / "consume_target_cache.py"
PREFLIGHT = HERE / "validate_preflight.py"
PRODUCTION_VALIDATORS = HERE / "production_obligation_validators.py"
FREEZE = HERE / "FREEZE.json"
PREFLIGHT_MUTATION_LEDGER = HERE / "PREFLIGHT_MUTATION_LEDGER_V001.json"
DUAL_GATE = HERE / "DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json"
CACHE_PARENT = HERE / "CACHE_PAYLOADS_V012"
V005_DIR = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005"
V005_AUDIT_DIR = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V005"
V005_FREEZE = V005_DIR / "FREEZE.json"
V005_PREFLIGHT = V005_DIR / "PREFLIGHT_RESULT_V002.json"
V005_DUAL_GATE = V005_DIR / "DUAL_SIX_HOUR_OBSTRUCTION_GATE_V005.json"
V005_PACKET_AUDIT = V005_DIR / "HOSTILE_PACKET_AUDIT_V002.json"
V005_HOSTILE_AUDIT = V005_AUDIT_DIR / "HOSTILE_AUDIT_RESULT_V001.json"
RUNTIME_COMPATIBILITY_OBSTRUCTION = V005_AUDIT_DIR / "TARGET_V005_RUNTIME_COMPATIBILITY_OBSTRUCTION_V001.json"
V006_DIR = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006"
V006_AUDIT_DIR = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V006"
V006_METHOD = V006_DIR / "METHOD.md"
V006_BUILDER = V006_DIR / "build_target_cache.py"
V006_CONSUMER = V006_DIR / "consume_target_cache.py"
V006_PREFLIGHT = V006_DIR / "validate_preflight.py"
V006_FREEZE = V006_DIR / "FREEZE.json"
V006_PREFLIGHT_RESULT = V006_DIR / "PREFLIGHT_RESULT_V001.json"
V006_HOSTILE_OBSTRUCTION = V006_AUDIT_DIR / "HOSTILE_AUDIT_OBSTRUCTION_V001.json"
V007_DIR = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007"
V007_AUDIT_DIR = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V007"
V007_DUAL_GATE = V007_DIR / "DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V007.json"
V007_HOSTILE_AUDIT = V007_AUDIT_DIR / "HOSTILE_AUDIT_RESULT_V001.json"
V007_RUNTIME_OBSTRUCTION = V007_AUDIT_DIR / "TARGET_V007_RUNTIME_COMPATIBILITY_OBSTRUCTION_V001.json"
V008_DIR = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008"
V008_AUDIT_DIR = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V008"
V008_DUAL_GATE = V008_DIR / "DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V008.json"
V008_HOSTILE_AUDIT = V008_AUDIT_DIR / "HOSTILE_AUDIT_RESULT_V001.json"
V008_POSTBUILD_AUDIT = V008_AUDIT_DIR / "POSTBUILD_PAYLOAD_AUDIT_V001.json"
V008_BINDING_OBSTRUCTION = V008_AUDIT_DIR / "V008_POSTBUILD_AUDIT_BINDING_OBSTRUCTION_V001.json"
V009_DIR = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V009"
V009_AUDIT_DIR = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V009"
V009_HOSTILE_OBSTRUCTION = V009_AUDIT_DIR / "HOSTILE_AUDIT_OBSTRUCTION_V001.json"
V010_DIR = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V010"
V010_AUDIT_DIR = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V010"
V010_HOSTILE_OBSTRUCTION = V010_AUDIT_DIR / "HOSTILE_AUDIT_OBSTRUCTION_V001.json"
V010_CUSTODY_CORRECTION = V010_AUDIT_DIR / "AUDIT_RECORD_CUSTODY_CORRECTION_V001.json"
V011_DIR = ROOT / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V011"
V011_AUDIT_DIR = ROOT / "AUDIT_R_L12_TARGET_STORAGE_CACHE_V011"
V011_HOSTILE_OBSTRUCTION = V011_AUDIT_DIR / "HOSTILE_AUDIT_OBSTRUCTION_V001.json"
AUDIT_OBLIGATION_CONTRACT_SHA256 = {
    "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/AUDIT_OBLIGATIONS_V001.json": "49a1a5901249c0476ebd775d60b9342436e4391a2a97b9c08f1082247b719e77",
    "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/METHODOLOGY.md": "8c31f58ee451b531b946b3537d327fe3300502627280c324d20916a10caeedd9",
    "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/validate_obligation_spec.py": "476224a7ba126ca9d21f3a6fb253dcced9b2ce7ef8a06fd419fb673c2e5611d6",
    "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/VALIDATION_RESULT_V001.json": "ebd33e8e45b8d32428cd98f18f5f010da3ac4c0b7e566ce1ba70a1bc8f53714c",
    "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/MANIFEST.sha256": "d09b52766166054df66baf4d972d9de830056faad6985ee353792da7c23fff6d",
}
AUTHORIZATION_DAG_MODEL_SHA256 = {
    "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/README.md": "8da7cc25a23292703ec852531df393ed1dda803576eb35f735cd5854a2f2af3b",
    "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/RESULT.json": "caf7c3e8fed94f61cd6d2b8a7555200ed61207c76d3d683d515d7451fe528d98",
    "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/VERIFICATION.txt": "394dcf0e9ccfd5aa0fef24c02b3f5ca2437382434ccc15d4b52895da352983d6",
    "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/authorization_model.py": "182c73d94494b1c78aee8bbed7de7371519c9074461a74101b136eb9d7f5898c",
    "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/exhaustive_check.py": "3ac1ea92d421ddda248164c0591d94084626559dfcd6e6a7fb0847b4a26b58ab",
    "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/MANIFEST.sha256": "da9ae68138e9fcb716ee8ff7d962199f60b0241daf2a70a7e1695e85870ed499",
}
DUAL_LAUNCH_COORDINATOR_SHA256 = {
    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/README.md": "0a4b0694fca19f56c0628c3ad663859ac5697187af151f7e4501ab42f2f477db",
    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/RESULT.json": "7779aeb44f9ad75b47819d96074acb2c4f0604414ba40337d3b22008b32b144e",
    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/VERIFICATION.txt": "220e65b89ce75c774d9ee8f129bda32f97e824a46b4593a0f0ade7a7a337492d",
    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/dual_launch_coordinator.py": "9f70c3b05dfd9ca0045858f43065d6958872a066551ff74e899eb0a19b496af7",
    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/production_dual_l12_launcher.py": "067bdec60d4fe40e5d961241a7408677f8950ea7d68e7dbb3d8dc0f9db83f163",
    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/synthetic_fixtures.py": "3e4389ded1d9550f744c8433c6a7e1be1ed337d6c93979b4df1e9f183c5b62d2",
    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/test_dual_launch_coordinator.py": "49294c74c9c6f4ab9bf3207bf1b80ef12445d448727b51be714c21b0e52aa2c9",
    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/test_production_dual_l12_launcher.py": "c353bc29c23598bb7d209d48372de64fd7aa807837bb6c67f801fece28acd54d",
    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/MANIFEST.sha256": "3aae4f7bce5ce3910c87e36bddd36c61d990ed3f72b37db286a3f6c06920a1bd",
}
TRACK_C_REFINEMENT_SHA256 = {
    "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/independent_final_auditor.py": "cb1681c870b8382d9e7a83bec9df0830699d7b1015ed19b24360a3dbd4ae207e",
    "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/production_dag_refinement.py": "ec84094f6d4df6cb22a6fbae2205242f51e8217261e47b5b0fb460d245da5d56",
    "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001/production_evidence_orchestrator.py": "d85275417f92961a2809822bcfc635d9e23e16bc7ad4fde43183ddcb78620b20",
}
TARGET_V004 = V004_DIR / "compute_prefix_history_v004.py"
TARGET_L12_GATE_V004 = V004_DIR / "TARGET_L12_GATE_V004.json"
HOSTILE_V003 = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "independent_prefix_history_v003.py"
TARGET_METHOD_V004 = V004_DIR / "Q_SHARDED_TARGET_METHOD_V004.md"
TARGET_FREEZE_V004 = V004_DIR / "FROZEN_METHOD_V004.json"
HOSTILE_METHOD_V003 = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "V003_L12_EXECUTABLE_METHOD.md"
HOSTILE_FREEZE_V003 = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "FROZEN_MANIFEST_V003.json"
PRESERVED_WORKSPACE_CUSTODY = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "PRESERVED_WORKSPACE_CUSTODY_V002.json"
PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001" / "PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_V001.json"
TARGET_V004_INVARIANTS = V004_DIR / "TARGET_V004_INVARIANTS.json"
INDEPENDENT_L10_GATE_V002 = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/L10_GATE_V002.json"
TARGET_V004_SHA256 = "c626cabd09eeea41f63513f7218a82b5418b767bad0d2aace66f0a9feac8a1f7"
TARGET_L12_GATE_V004_SHA256 = "629ab8bc8e3c2a70c8e79a788ddeb6bafd3503491cef3b331bcc97a1555c2359"
HOSTILE_V003_SHA256 = "cc4e1195283f60fddab1d70831965bd14a09435fd4aca2ee7fdde7e2d7e5ba7f"
TARGET_METHOD_V004_SHA256 = "864113577059c5214923d4d1709e0d2a4483131f816b42bc43f7fc14a72b19ef"
TARGET_FREEZE_V004_SHA256 = "d98f994572a2830746bbb305bfa0146f417662abebc2bf5861e48c05071e90d2"
HOSTILE_METHOD_V003_SHA256 = "32a6f397c586328c07fdefc1aae0b4bb8e98de7783386c209104a68d577b418a"
HOSTILE_FREEZE_V003_SHA256 = "99ef9fca46e7baaa11b6700279a35ff936db3175ca56ea78b936c074dfe3845d"
PRESERVED_WORKSPACE_CUSTODY_SHA256 = "1d9a11359f0ba5298520ff51354badef4173dd070e829652d026b6317007aeb6"
PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_SHA256 = "9dfaefcb6db713e03ea0774bb6a044774c0fed9a07aee48be12058e366291000"
TARGET_V004_INVARIANTS_SHA256 = "ee0ec87dcbd963dc0cc5acb70b7dcc6eb5bee81efa2c6bf766c2e382e57fae34"
INDEPENDENT_L10_GATE_V002_SHA256 = "c94685d15e15016c5d10673857b96bf1b9ee0ec1a1da3b0d11a9957320f18eb2"
CANONICAL_V004_HISTORY_SHA256 = {
    "4": "8bf8f4eb54781c599a9fb3ae407207e08504396128c82e1e838d5b47a1d564b2",
    "6": "06ccf6f419b8e743c6aea014c90ba1598786fc5bb28331488cde0f0846215f33",
    "8": "affc775a91186883b5dd7c7180340b06105523ad5744c38a470331c1a631868a",
    "10": "873e45b6b37654910947711af1d8dc93d0def8ea0ef994587db206ab47b4267c",
}
CANONICAL_V004_HISTORY_PATH = {
    "4": V004_DIR / "CONTROL_HISTORY/TARGET_V004_L4.json",
    "6": V004_DIR / "CONTROL_HISTORY/TARGET_V004_L6.json",
    "8": V004_DIR / "CONTROL_HISTORY/TARGET_V004_L8.json",
    "10": V004_DIR / "BENCHMARK/TARGET_V004_QSHARD_L10.json",
}
RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256 = "be0608223cc97f1fa07c28cfa1fdbf77cf26cfffa5660eee719d5c879e8b1a2d"
V006_HOSTILE_OBSTRUCTION_SHA256 = "f1a1d88c266c5e099b929d9cc38ec3008c662ebf70afafbd1a10c798ebf151f4"
V006_CUSTODY_SHA256 = {
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/METHOD.md": "de6f9d61afb2c2640d9ce9fe09391cbb89fc875a15f410525631d706b304996d",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/build_target_cache.py": "5621fe08c44e87b0f5805c8c6c220c859a828115ad6a1e72ef32540dd3d42d8a",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/consume_target_cache.py": "c61de2b158a7b9e1ef69a9f3f22519ba017bf43f7bea5be09c92a68ae915452c",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/validate_preflight.py": "f962cca5a609ca05db35110c8c80da04f9367ec5b9da67c7e5462394c716aaa4",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/FREEZE.json": "91acd3fbe6bc1c1fe96fd002dda95d908d8c1e3d4939acda4c999225955fef35",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/PREFLIGHT_RESULT_V001.json": "0c9f1097c811ba31e3f7496e9e83fe17ff6b0103aad6dac309c541e8e57d71bc",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V006/HOSTILE_AUDIT_OBSTRUCTION_V001.json": V006_HOSTILE_OBSTRUCTION_SHA256,
}
V007_RUNTIME_OBSTRUCTION_SHA256 = "a9cb384baef15fc72a61f0009b67d8e5aef95b14084f767b2168ef70efbd4d62"
V007_DUAL_GATE_SHA256 = "72356cdbc5e0395a2f40bc6e5b7c206d79ef50d83debc5e8ae70d9e753f3c4cb"
V007_HOSTILE_AUDIT_SHA256 = "b458f6a9920add7daf105a762e35e889c185d97679ad360ff25355c6014492be"
V007_CACHE_MANIFEST_SHA256 = {
    "4": "b1af0bb1b34d8714ed782023c91244e7c07aa01ca2278ac30feac2f15b05c196",
    "6": "bb72911bf97b62eebd317470119c47466791db3380f029b40a14ec5d530cb48e",
    "8": "cff175b0977f5f44bd40822d17524f276528f4f30ae30996c5207492af743af2",
    "10": "dba22bd5761b274a9d7436d79063a8d9cb7ec62ddba8750211e3fbbb6a086f54",
    "12": "320809281dd7a1d6fe45e1c45dbaa8d43504195a4784cfaddde2e680a87317a3",
}
V007_CUSTODY_SHA256 = {
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/METHOD.md": "e76b4a717dc2f8e661132ba5339ee1c3126eca2e7e60b12ce0d12fbc8815ba34",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/build_target_cache.py": "c4cef11649df1554113a0c237e2a206f02bc2543236da862d32c3c1bea5e50fe",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/consume_target_cache.py": "fad3abe46967927d7395447e89b64584c445a4b194dda96dd5df85c91785b35a",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/validate_preflight.py": "d8319342a3bc09ff3d45f905b7ec50beffaa66e8014b90527dfaa5cd8959d6e7",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/FREEZE.json": "e1b8ce278442fca7f7b7355662c71a7f6df6a3d603d5e960cd79bcda50ea2c34",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/PREFLIGHT_RESULT_V001.json": "887c80ca5f960d22affd75453ead4dda12688fb3300be0c3345440dc99a0e0c6",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V007.json": V007_DUAL_GATE_SHA256,
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V007/HOSTILE_AUDIT_RESULT_V001.json": V007_HOSTILE_AUDIT_SHA256,
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V007/TARGET_V007_RUNTIME_COMPATIBILITY_OBSTRUCTION_V001.json": V007_RUNTIME_OBSTRUCTION_SHA256,
}
V008_BINDING_OBSTRUCTION_SHA256 = "2dc1cbedaf72579666e97404e624e1e974c015572c24c2f4d834d933e075f390"
V008_DUAL_GATE_SHA256 = "3e9c39e48bcd121b64557c77c16c87c071d69fc0196927a41629807fa98db1bf"
V008_HOSTILE_AUDIT_SHA256 = "9951a9cc4ee1cc9e1857fbbfb26585ce2972e12a8bac7f529c3e4a04513808fc"
V008_POSTBUILD_AUDIT_SHA256 = "201ff07c2611202a69d69f5b37e71c052d32c860e2fb2e7a4f651ef74d81e6b1"
V008_CACHE_MANIFEST_SHA256 = {
    "4": "17fec475c294b93929bde12ae18d9895a2138ad5ec6cff68fe0ee0ba4db9a2c3",
    "6": "26f6a2ae81a5ddad4f8f2fa42a99de34c26ba9b46737370ffd2cff92c944ed04",
    "8": "e3f729d3ba24e885bd624ea41dbf4703080d550b2562281d4117ae390e2610af",
    "10": "54606cf3761146a9b7a559fde73690ec7c0c465f9ca611d245d9e58d5af2c5bf",
    "12": "cdf99de4098c899498996da11104c9150054e8bdf9f9428222117961249f9252",
}
V008_CUSTODY_SHA256 = {
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008/METHOD.md": "97630927ee43a3db9f95ef12c923eab7c8e17980fb992cc770327c930ed6ab61",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008/build_target_cache.py": "bce0d87ee4873dfd2fcbb0325a1a93b779adc448ba134f634510129534d97076",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008/consume_target_cache.py": "4bf1caeb9f2c86fb225aff87fc7245c9c792c72902134c6aae72dd31f429cd84",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008/validate_preflight.py": "03691e5cfff2c847b72183eb6bab4fcfc18f72f4911c7a86574baa977a42bf76",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008/FREEZE.json": "89ebc631da9407bd5d7c09be7530fec5f9faa1cc78477d0f51127b3eb4ac5244",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008/PREFLIGHT_RESULT_V001.json": "dc4a48383ec82247cb540cd9fd0af58acbf99ed8085d6d8262465f56d30030d1",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008/DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V008.json": V008_DUAL_GATE_SHA256,
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V008/HOSTILE_AUDIT_RESULT_V001.json": V008_HOSTILE_AUDIT_SHA256,
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V008/POSTBUILD_PAYLOAD_AUDIT_V001.json": V008_POSTBUILD_AUDIT_SHA256,
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V008/V008_POSTBUILD_AUDIT_BINDING_OBSTRUCTION_V001.json": V008_BINDING_OBSTRUCTION_SHA256,
}
V009_HOSTILE_OBSTRUCTION_SHA256 = "ff063573868b96aa14b1bdee218c4d6e2c039b8ba844e9753a21e7a48d8965fc"
V009_CUSTODY_SHA256 = {
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V009/METHOD.md": "647df1865a7cb0f9c6e912cab31ccbfa37f841d4dcaedfcefb5e0e2fe635ba9d",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V009/build_target_cache.py": "e4f60be6f6636fb4acb3e08be6bf5e55f4ca7885d82b8ae35e2b2a4666d36005",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V009/consume_target_cache.py": "9e1c41304bce385dabbc53f75894c04d822f68a171b387621d1ae3966d919141",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V009/validate_preflight.py": "8b64dcbf789ec3259b9e241ea7a5ffc9540e4b8ac1518290c43028e396a12f99",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V009/FREEZE.json": "7afd41c92916f5b70fdcdddcb6352a7f0b1caf60978bbd0703e1c7da50e2b565",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V009/PREFLIGHT_RESULT_V001.json": "96ce5f66b94a3380cf43b3d3b04f570f73b8652e13300a7df8ead8930d3a4b9b",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V009/HOSTILE_AUDIT_OBSTRUCTION_V001.json": V009_HOSTILE_OBSTRUCTION_SHA256,
}
V010_HOSTILE_OBSTRUCTION_SHA256 = "ae4238262273d5529c6a84985553669768714cfb5889e8793fdb52750dd927cf"
V010_CUSTODY_CORRECTION_SHA256 = "3e8f129a4b36ed3f71ab7783d99e9f0cab3e23d5b9254c71eea6e94fc6b1f5d1"
V010_CUSTODY_SHA256 = {
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V010/METHOD.md": "6ac286f7b132a6c98160e0de92299a80fc610483517e4d527d32735631588a38",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V010/build_target_cache.py": "b3a07705c9fa8fafe725dae239bfec11090acc2ee2acc87bd62deaabd7b43f5d",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V010/consume_target_cache.py": "58e60f37f2e8712945a4af4296fe98e0a3271dd0ad494c1b39edcb0ea2e0c054",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V010/validate_preflight.py": "168b3f93121093d80d16be5bc11db564d89e12d4598e7e510bdf60f7e5848acd",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V010/FREEZE.json": "5c5588769c323487971b8d18ae4b875dc1322df8cf6aa976707ebcafe09d04cf",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V010/PREFLIGHT_RESULT_V001.json": "126cc6574b377e0424cd108d0e02dc99c1b86644f022a0fa750991d965dd8320",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V010/HOSTILE_AUDIT_OBSTRUCTION_V001.json": V010_HOSTILE_OBSTRUCTION_SHA256,
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V010/AUDIT_RECORD_CUSTODY_CORRECTION_V001.json": V010_CUSTODY_CORRECTION_SHA256,
}
V011_HOSTILE_OBSTRUCTION_SHA256 = "0dc595ff78e4fa5d81a42a285d3b74ce93758dd8bb42c836471bd3e3e898e2f6"
V011_CUSTODY_SHA256 = {
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V011/METHOD.md": "08c29a2fae7c3e3e6b415f535113e3c7f0bae9ebeb6ae853cbcfd94430f88a5f",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V011/build_target_cache.py": "bcc882f3fb6ba866834aaceab05c2304bbec5b5a3f9c1469dd623a786d5e95f0",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V011/consume_target_cache.py": "f61fb54672b0cd8adc9385a8535d3ead3395b797352fc83ebb50b7536b623c30",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V011/validate_preflight.py": "84332d639e6323efee5ecd730800b7d538453dc29955a57824b823363bbbd01a",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V011/FREEZE.json": "537f3c2995abd3d0cb7e8cd838cd0ee1a6a513c9ccdd9997926c4a165dbbce22",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V011/PREFLIGHT_RESULT_V001.json": "1e8c6f1c982781516423226e099b67ba3b7b2fc3cbe61b9d610029a83880a63c",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V011/HOSTILE_AUDIT_OBSTRUCTION_V001.json": V011_HOSTILE_OBSTRUCTION_SHA256,
}
FUTURE_HOSTILE_AUDIT_PATH = "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/HOSTILE_AUDIT_RESULT_V001.json"
FUTURE_HOSTILE_AUDIT_SCHEMA = "TARGET_V012_PREPAYLOAD_HOSTILE_AUDIT_V001"
FUTURE_HOSTILE_AUDIT_CLASSIFICATION = "PASS_TARGET_V012_PREPAYLOAD_CONTROL_PLANE"
FUTURE_POSTBUILD_AUDIT_PATH = "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/POSTBUILD_PAYLOAD_AUDIT_V001.json"
FUTURE_POSTBUILD_AUDIT_SCHEMA = "TARGET_V012_POSTBUILD_PAYLOAD_AUDIT_V001"
FUTURE_POSTBUILD_AUDIT_CLASSIFICATION = "PASS_TARGET_V012_FRESH_STORAGE_CACHE_PAYLOADS"
FUTURE_PHYSICAL_GATE_AUDIT_PATH = "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_GATE_HOSTILE_AUDIT_V001.json"
FUTURE_PHYSICAL_GATE_AUDIT_SCHEMA = "TARGET_V012_PHYSICAL_GATE_HOSTILE_AUDIT_V001"
FUTURE_PHYSICAL_GATE_AUDIT_CLASSIFICATION = "PASS_TARGET_V012_PHYSICAL_GATE_BINDINGS"
FUTURE_PREPAYLOAD_ABSENCE_CENSUS = {
    "DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json": False,
    "PHYSICAL_EXECUTION_GATE_V012.json": False,
    "CONTROL_EXECUTION_AUTHORIZATION_GATE_V012.json": False,
    "CACHED_CONTROL_L4_L8_GATE_V012.json": False,
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json": False,
    "L10_EXECUTION_AUTHORIZATION_GATE_V012.json": False,
    "CACHED_L10_GATE_V012.json": False,
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_AUDIT_V001.json": False,
    "TARGET_L12_EXECUTION_GATE_V012.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_HOSTILE_L10_CROSS_GATE_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_READY_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_READY_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_LAUNCH_HANDSHAKE_V002.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_WORKER_RELEASE_V002.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_COMMAND_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_COMMAND_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_RELEASE_ACK_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_RELEASE_ACK_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_V012_WORKER_COMPLETION_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/HOSTILE_V004R4_WORKER_COMPLETION_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_TELEMETRY_V001.json": False,
    "AUDIT_R_L12_PARALLEL_EXECUTION_V001/FINAL_L12_TARGET_HOSTILE_AUDIT_V001.json": False,
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json": False,
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json": False,
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS": False,
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHED_L10_GATE_V004R4.json": False,
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json": False,
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS": False,
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES": False,
    "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_L12_EXECUTION_GATE_V004R4.json": False,
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/POSTBUILD_PAYLOAD_AUDIT_V001.json": False,
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_GATE_HOSTILE_AUDIT_V001.json": False,
    "CACHE_PAYLOADS_V012": False,
    "PHYSICAL_OUTPUTS": False,
    "WORKSPACES": False,
}
V005_DUAL_GATE_SHA256 = "025c71d92d0caa977ee466f76b0749213da87cedeabb3093c0116256b977d19b"
V005_CACHE_MANIFEST_SHA256 = {
    "4": "da4395fb7b0e99d38b84cf9f6bcf771b18a9e335e32dc9c23b20a11a6a16160c",
    "6": "925c8772e5de3b10bfaea4729fb5b46443cce8986041092405c75654b299dd7a",
    "8": "5eaeea70dc0b99abac7ecea164ba72e82828a81c9af7ae971857412705cfe27c",
    "10": "4052d0d0e57cc1ccc91352eaa3a136ee9a8cb812f3f5dd2e35ee676432c98cfc",
    "12": "59e437956c46f03c03cc2d2a8bf6e89645ce330170106fabf779d6d408b9dbea",
}
SUPPORTED = (4, 6, 8, 10, 12)
WORD_DTYPE = np.dtype("<u4")
OFFSET_DTYPE = np.dtype("<u8")
INDEX_DTYPE = np.dtype("<i4")
SCRATCH_LIMIT = 20 * 2**30
OVERHEAD_RESERVE = 2**20
MAPPED_CACHE_LIMIT = 512 * 2**20
BUILDER_RSS_LIMIT = 4 * 2**30
HISTORICAL_OBSTRUCTION_WALL_LIMIT = 6 * 3600.0
WALL_LIMIT = 30 * 3600.0
PARALLEL_HOSTILE_RSS_LIMIT = 16 * 2**30
PARALLEL_HOSTILE_AUTHENTICATION_PEAK = 252_944_080
PARALLEL_TARGET_AUTHENTICATION_PEAK = 252_944_080
PARALLEL_AGGREGATE_PEAK = (
    v004.RSS_LIMIT
    + PARALLEL_TARGET_AUTHENTICATION_PEAK
    + PARALLEL_HOSTILE_RSS_LIMIT
    + PARALLEL_HOSTILE_AUTHENTICATION_PEAK
)
PARALLEL_HOST_TOTAL_MINIMUM = 48_000_000_000
PARALLEL_HOST_HEADROOM_MINIMUM = PARALLEL_HOST_TOTAL_MINIMUM - PARALLEL_AGGREGATE_PEAK
# The physical state is stored as 23 simultaneous L12 NPY shards at the
# maximum two-prefix window.  Their 128-byte headers are filesystem bytes and
# therefore belong in the launch-floor certificate even though they are not
# numerical array payload.
PARALLEL_TARGET_SCRATCH_MINIMUM = 9_600_954_452
PARALLEL_HOSTILE_SCRATCH_MINIMUM = 9_600_935_128
PARALLEL_FILESYSTEM_MINIMUM = (
    PARALLEL_TARGET_SCRATCH_MINIMUM + PARALLEL_HOSTILE_SCRATCH_MINIMUM
)
EVIDENCE_SHA256 = {
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_OBSTRUCTION.json": "9cfd793ded33b561c10ff7c93b8ffcb9cfe272f4efe7966fe8fd6c53413aeb62",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_EXECUTION_LOG.md": "455359f7092acf93845f5494b40215e6264d9123fcc019be5b030f2adc7b79aa",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/TARGET_V004_WALL_MONITOR.json": "b0882a97540d822ec96c093c1571d069f379f370a915c33fe213b18d7c118b6d",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_OBSTRUCTION.json": "9281e055ea3bf8564960e303a2fa84feb99960c028bc0adc75bc2be7ba0a3aac",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_EXECUTION_LOG.md": "9db56f21e55bbf800a07248a6ab67845cf6e5b0648c737d91ea19ac25d9d4c4a",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/OBSTRUCTION_EVIDENCE/HOSTILE_V003_WALL_MONITOR.json": "13ebfe63f7b5b6103b51c3ec2b5a062342c73adc18f77738518834bd04a873c3",
}
PREDECESSOR_CUSTODY_SHA256 = {
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/FREEZE.json": "035d378a2d71a273f87275c61e31435c955061b0777c36ec2973c99dc3a950d2",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/PREFLIGHT_RESULT_V002.json": "885a4dc499064338271d9f096fc82e93a807e4a54872d97399c39d6cd258a603",
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/DUAL_SIX_HOUR_OBSTRUCTION_GATE_V005.json": V005_DUAL_GATE_SHA256,
    "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V005/HOSTILE_PACKET_AUDIT_V002.json": "6cc048377d54935976f1eb1560f249d48481fb1b26d28c47469232843d0f0a5b",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V005/HOSTILE_AUDIT_RESULT_V001.json": "772d5aa4d746f444c77b1a0e545464bc2b47af254839a5951ae4745d9f1793b9",
    "AUDIT_R_L12_TARGET_STORAGE_CACHE_V005/TARGET_V005_RUNTIME_COMPATIBILITY_OBSTRUCTION_V001.json": RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256,
}


class Refusal(RuntimeError):
    pass


class StableAuthorityCustody:
    """Retain authenticated authority descriptors until publication completes."""

    def __init__(self) -> None:
        self._entries: dict[str, dict[str, object]] = {}

    @staticmethod
    def _key(path: Path) -> str:
        return os.path.abspath(os.fspath(path))

    @staticmethod
    def _require_canonical_path(key: str, label: str) -> None:
        """Reject aliases introduced through any symlinked path component."""
        absolute = Path(key)
        try:
            resolved = absolute.resolve(strict=False)
        except OSError as error:
            raise Refusal(f"{label} canonical path resolution failed") from error
        if resolved != absolute:
            raise Refusal(f"{label} path traverses a symlink alias")

    def authenticate(
        self, path: Path, label: str, expected_sha256: str | None,
        require_immutable_mode: bool,
    ) -> tuple[int, str]:
        key = self._key(path)
        self._require_canonical_path(key, label)
        existing = self._entries.get(key)
        if existing is not None:
            self.verify_one(path, label)
            digest = existing["sha256"]
            if expected_sha256 is not None and digest != expected_sha256:
                raise Refusal(f"{label} hash mismatch")
            if require_immutable_mode and not existing["immutable"]:
                raise Refusal(f"{label} is not immutable")
            return int(existing["descriptor"]), str(digest)
        try:
            path_metadata = os.lstat(path)
        except OSError as error:
            raise Refusal(f"{label} ordinary file absent") from error
        if stat.S_ISLNK(path_metadata.st_mode) or not stat.S_ISREG(path_metadata.st_mode):
            raise Refusal(f"{label} is not an ordinary non-symlink file")
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = os.open(path, flags)
        except OSError as error:
            raise Refusal(f"{label} could not be opened without following links") from error
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode):
                raise Refusal(f"{label} is not an ordinary file")
            if (path_metadata.st_dev, path_metadata.st_ino) != (before.st_dev, before.st_ino):
                raise Refusal(f"{label} path/descriptor identity mismatch")
            immutable = not bool(before.st_mode & 0o222)
            if require_immutable_mode and not immutable:
                raise Refusal(f"{label} is not immutable")
            digest = sha256_descriptor(descriptor)
            if expected_sha256 is not None and digest != expected_sha256:
                raise Refusal(f"{label} hash mismatch")
            identity = (
                before.st_dev, before.st_ino, before.st_size,
                before.st_mtime_ns, before.st_ctime_ns,
            )
            self._entries[key] = {
                "descriptor": descriptor,
                "identity": identity,
                "sha256": digest,
                "immutable": immutable,
                "path": Path(key),
            }
            # Re-resolve after descriptor authentication so a parent-directory
            # substitution concurrent with the open cannot enter custody.
            self._require_canonical_path(key, label)
            self.verify_one(path, label)
            return descriptor, digest
        except BaseException:
            # Authentication owns this newly inserted entry until success.
            # Never retain a closed descriptor after a concurrent path-alias
            # refusal; a later FD reuse must not be closed by custody cleanup.
            self._entries.pop(key, None)
            os.close(descriptor)
            raise

    def verify_one(self, path: Path, label: str) -> None:
        key = self._key(path)
        entry = self._entries.get(key)
        if entry is None:
            raise Refusal(f"{label} was not authenticated into retained custody")
        self._require_canonical_path(key, label)
        descriptor = int(entry["descriptor"])
        before_identity = entry["identity"]
        try:
            current = os.fstat(descriptor)
            linked = os.lstat(path)
        except OSError as error:
            raise Refusal(f"{label} custody path/descriptor disappeared") from error
        current_identity = (
            current.st_dev, current.st_ino, current.st_size,
            current.st_mtime_ns, current.st_ctime_ns,
        )
        if (
            current_identity != before_identity
            or stat.S_ISLNK(linked.st_mode)
            or not stat.S_ISREG(linked.st_mode)
            or (linked.st_dev, linked.st_ino) != (current.st_dev, current.st_ino)
            or sha256_descriptor(descriptor) != entry["sha256"]
        ):
            raise Refusal(f"{label} changed during retained descriptor custody")

    def digest(self, path: Path, label: str) -> str:
        self.verify_one(path, label)
        return str(self._entries[self._key(path)]["sha256"])

    def has(self, path: Path) -> bool:
        return self._key(path) in self._entries

    def verify_all(self) -> None:
        for entry in list(self._entries.values()):
            self.verify_one(Path(entry["path"]), f"retained authority {entry['path']}")

    def close(self) -> None:
        for entry in self._entries.values():
            os.close(int(entry["descriptor"]))
        self._entries.clear()


AUTHORITY_CUSTODY: StableAuthorityCustody | None = None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(16 * 2**20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def immutable_json(
    path: Path, label: str, expected_sha256: str | None = None,
    require_immutable_mode: bool = True,
) -> tuple[dict[str, object], str]:
    retained = AUTHORITY_CUSTODY is not None
    if retained:
        descriptor, actual_sha256 = AUTHORITY_CUSTODY.authenticate(
            path, label, expected_sha256, require_immutable_mode
        )
    else:
        if path.is_symlink() or not path.is_file():
            raise Refusal(f"{label} immutable ordinary file absent")
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise Refusal(f"{label} is not an ordinary file")
        if require_immutable_mode and before.st_mode & 0o222:
            raise Refusal(f"{label} is not immutable")
        raw = bytearray()
        digest = hashlib.sha256()
        offset = 0
        while block := os.pread(descriptor, 16 * 2**20, offset):
            raw.extend(block)
            digest.update(block)
            offset += len(block)
        parsed_sha256 = digest.hexdigest()
        if retained and parsed_sha256 != actual_sha256:
            raise Refusal(f"{label} retained descriptor digest mismatch")
        actual_sha256 = parsed_sha256
        if expected_sha256 is not None and actual_sha256 != expected_sha256:
            raise Refusal(f"{label} hash mismatch")

        def exact_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
            value: dict[str, object] = {}
            for key, item in pairs:
                if key in value:
                    raise Refusal(f"{label} duplicate JSON key: {key}")
                value[key] = item
            return value

        def reject_constant(token: str) -> object:
            raise Refusal(f"{label} nonfinite JSON constant: {token}")

        record = json.loads(
            raw.decode("utf-8"), object_pairs_hook=exact_object,
            parse_constant=reject_constant,
        )
        after = os.fstat(descriptor)
        if (
            (before.st_dev, before.st_ino, before.st_size,
             before.st_mtime_ns, before.st_ctime_ns)
            != (after.st_dev, after.st_ino, after.st_size,
                after.st_mtime_ns, after.st_ctime_ns)
            or sha256_descriptor(descriptor) != actual_sha256
        ):
            raise Refusal(f"{label} descriptor changed during authentication")
        if not isinstance(record, dict):
            raise Refusal(f"{label} is not an object")
        if retained:
            AUTHORITY_CUSTODY.verify_one(path, label)
        return record, actual_sha256
    finally:
        if not retained:
            os.close(descriptor)


def sha256_descriptor(descriptor: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while block := os.pread(descriptor, 16 * 2**20, offset):
        digest.update(block)
        offset += len(block)
    return digest.hexdigest()


def stable_file_sha256(
    path: Path, label: str, expected_sha256: str | None = None,
    require_immutable_mode: bool = True,
) -> str:
    if AUTHORITY_CUSTODY is not None:
        _descriptor, digest = AUTHORITY_CUSTODY.authenticate(
            path, label, expected_sha256, require_immutable_mode
        )
        return digest
    if path.is_symlink() or not path.is_file():
        raise Refusal(f"{label} immutable ordinary file absent")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or (require_immutable_mode and before.st_mode & 0o222)
        ):
            raise Refusal(f"{label} is not immutable")
        digest = sha256_descriptor(descriptor)
        if expected_sha256 is not None and digest != expected_sha256:
            raise Refusal(f"{label} hash mismatch")
        after = os.fstat(descriptor)
        if (
            (before.st_dev, before.st_ino, before.st_size,
             before.st_mtime_ns, before.st_ctime_ns)
            != (after.st_dev, after.st_ino, after.st_size,
                after.st_mtime_ns, after.st_ctime_ns)
            or sha256_descriptor(descriptor) != digest
        ):
            raise Refusal(f"{label} descriptor changed during authentication")
        return digest
    finally:
        os.close(descriptor)


def immutable_file_sha256(path: Path, label: str) -> str:
    return stable_file_sha256(path, label, require_immutable_mode=True)


def exact_tree_equal(actual: object, expected: object) -> bool:
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return (
            set(actual) == set(expected)
            and all(exact_tree_equal(actual[key], value) for key, value in expected.items())
        )
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            exact_tree_equal(left, right) for left, right in zip(actual, expected)
        )
    return bool(actual == expected)


def strict_json_object_bytes(raw: bytes, label: str) -> dict[str, object]:
    """Decode one exact finite JSON object without filesystem side effects."""
    if type(raw) is not bytes:
        raise Refusal(f"{label} is not raw JSON bytes")

    def exact_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                raise Refusal(f"{label} duplicate JSON key: {key}")
            value[key] = item
        return value

    def reject_constant(token: str) -> object:
        raise Refusal(f"{label} nonfinite JSON constant: {token}")

    try:
        record = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=exact_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Refusal(f"{label} is not strict UTF-8 JSON") from error
    if not isinstance(record, dict):
        raise Refusal(f"{label} is not a JSON object")
    return record


def _dispatch_production_obligation(
    artifact_id: str, record: dict[str, object], *, mutation_class: str,
    fixture_mode: bool,
) -> None:
    if (
        not isinstance(artifact_id, str) or not artifact_id
        or not isinstance(mutation_class, str) or not mutation_class
    ):
        raise Refusal("audit-obligation production dispatch identity malformed")
    try:
        import production_obligation_validators as validators
    except ImportError as error:
        raise Refusal("production obligation validator module absent") from error
    if Path(getattr(validators, "__file__", "")).resolve() != PRODUCTION_VALIDATORS:
        raise Refusal("production obligation validator module path mismatch")
    try:
        validators.validate_record(
            artifact_id, record,
            mutation_class=mutation_class,
            fixture_mode=fixture_mode,
        )
    except (AssertionError, KeyError, RuntimeError, TypeError, ValueError) as error:
        raise Refusal(
            f"{artifact_id} production obligation validator refusal: {error}"
        ) from error


def validate_production_obligation(
    artifact_id: str, record: dict[str, object],
) -> None:
    """Apply the independent native-schema validator on the live sink path."""
    if not isinstance(record, dict):
        raise Refusal("production obligation record is not an object")
    _dispatch_production_obligation(
        artifact_id, record, mutation_class="PRODUCTION_NATIVE_RECORD",
        fixture_mode=False,
    )


def validate_audit_obligation_fixture(
    artifact_id: str, raw_json_bytes: bytes, *, mutation_class: str,
) -> None:
    """Route byte-mutated native records through that same validator set."""
    record = strict_json_object_bytes(
        raw_json_bytes, f"{artifact_id} {mutation_class} native fixture"
    )
    _dispatch_production_obligation(
        artifact_id, record, mutation_class=mutation_class, fixture_mode=True,
    )


def exact_refusal_match(actual: object, expected: str) -> bool:
    """Accept one single-line native refusal grammar, never a loose substring."""
    if not isinstance(actual, str) or not actual or "\n" in actual:
        return False
    if actual.endswith(expected):
        return True
    if expected == "duplicate JSON key":
        marker = expected + ": "
        prefix, separator, detail = actual.partition(marker)
        return bool(separator and prefix and detail and detail.strip() == detail)
    if expected == "nonfinite JSON constant":
        marker = expected + ": "
        prefix, separator, detail = actual.partition(marker)
        return bool(
            separator and prefix
            and detail in {"NaN", "Infinity", "-Infinity"}
        )
    return False


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_DIRECTORY", 0)
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _unlink_if_owned_at(
    parent_descriptor: int, name: str, device: int, inode: int,
) -> bool:
    try:
        metadata = os.stat(
            name, dir_fd=parent_descriptor, follow_symlinks=False,
        )
    except FileNotFoundError:
        return False
    if (
        stat.S_ISREG(metadata.st_mode)
        and (metadata.st_dev, metadata.st_ino) == (device, inode)
    ):
        os.unlink(name, dir_fd=parent_descriptor)
        return True
    return False


def atomic_publish_json(
    path: Path, record: dict[str, object], label: str,
    custody: StableAuthorityCustody, *, parent_descriptor: int | None = None,
) -> str:
    """Durably publish a no-clobber JSON record, then reauthenticate custody."""
    parent = path.parent
    StableAuthorityCustody._require_canonical_path(
        os.path.abspath(os.fspath(parent)), f"{label} parent",
    )
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    owns_parent_descriptor = parent_descriptor is None
    if parent_descriptor is None:
        parent_descriptor = os.open(parent, parent_flags)
    try:
        try:
            destination = os.stat(
                path.name, dir_fd=parent_descriptor, follow_symlinks=False,
            )
        except FileNotFoundError:
            destination = None
        parent_before = os.fstat(parent_descriptor)
        parent_path_before = os.stat(parent, follow_symlinks=False)
        if (
            destination is not None
            or not stat.S_ISDIR(parent_before.st_mode)
            or (parent_path_before.st_dev, parent_path_before.st_ino)
            != (parent_before.st_dev, parent_before.st_ino)
        ):
            raise Refusal(
                f"{label} canonical destination is not an absent ordinary path"
            )
        try:
            raw = (json.dumps(
                record, indent=2, sort_keys=True, allow_nan=False,
            ) + "\n").encode("utf-8")
        except (TypeError, ValueError) as error:
            raise Refusal(f"{label} is not finite serializable JSON") from error
        if not exact_tree_equal(strict_json_object_bytes(raw, label), record):
            raise Refusal(f"{label} JSON round-trip changed exact types or values")
        temporary_name = (
            f".{path.name}.staging-{os.getpid()}-{time.time_ns()}"
        )
        flags = (
            os.O_RDWR | os.O_CREAT | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = os.open(
            temporary_name, flags, 0o400, dir_fd=parent_descriptor,
        )
        identity: tuple[int, int] | None = None
        try:
            offset = 0
            while offset < len(raw):
                written = os.write(descriptor, raw[offset:])
                if written <= 0:
                    raise OSError(f"{label} staging write made no progress")
                offset += written
            os.fsync(descriptor)
            os.fchmod(descriptor, 0o444)
            # Persist both payload bytes and the immutable mode before the
            # no-clobber link publishes this inode inside the held directory.
            os.fsync(descriptor)
            before = os.fstat(descriptor)
            identity = (before.st_dev, before.st_ino)
            if (
                not stat.S_ISREG(before.st_mode)
                or before.st_nlink != 1
                or before.st_size != len(raw)
                or sha256_descriptor(descriptor)
                != hashlib.sha256(raw).hexdigest()
            ):
                raise Refusal(f"{label} staging descriptor authentication failed")
            custody.verify_all()
            StableAuthorityCustody._require_canonical_path(
                os.path.abspath(os.fspath(parent)), f"{label} parent",
            )
            parent_now = os.stat(parent, follow_symlinks=False)
            if (
                not stat.S_ISDIR(parent_now.st_mode)
                or (parent_now.st_dev, parent_now.st_ino)
                != (parent_before.st_dev, parent_before.st_ino)
            ):
                raise Refusal(f"{label} canonical parent identity drift")
            try:
                os.link(
                    temporary_name, path.name,
                    src_dir_fd=parent_descriptor,
                    dst_dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
            except FileExistsError as error:
                raise Refusal(
                    f"{label} canonical destination appeared before commit"
                ) from error
            linked_metadata = os.fstat(descriptor)
            canonical_flags = (
                os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )
            canonical = os.open(
                path.name, canonical_flags, dir_fd=parent_descriptor,
            )
            try:
                observed = os.fstat(canonical)
                if (
                    not stat.S_ISREG(observed.st_mode)
                    or observed.st_mode & 0o222
                    or observed.st_nlink != 2
                    or (
                        observed.st_dev, observed.st_ino, observed.st_size,
                        observed.st_mtime_ns, observed.st_ctime_ns,
                    ) != (
                        linked_metadata.st_dev, linked_metadata.st_ino,
                        linked_metadata.st_size, linked_metadata.st_mtime_ns,
                        linked_metadata.st_ctime_ns,
                    )
                    or sha256_descriptor(canonical)
                    != hashlib.sha256(raw).hexdigest()
                    or not exact_tree_equal(
                        strict_json_object_bytes(
                            os.pread(canonical, observed.st_size, 0), label
                        ), record,
                    )
                ):
                    raise Refusal(f"{label} postpublication authentication failed")
                if not _unlink_if_owned_at(
                    parent_descriptor, temporary_name, *identity,
                ):
                    raise Refusal(f"{label} staging custody changed after commit")
                os.fsync(parent_descriptor)
                published = os.fstat(descriptor)
                canonical_after = os.fstat(canonical)
                path_after = os.stat(
                    path.name, dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
                StableAuthorityCustody._require_canonical_path(
                    os.path.abspath(os.fspath(parent)), f"{label} parent",
                )
                parent_after = os.stat(parent, follow_symlinks=False)
                if (
                    published.st_nlink != 1
                    or canonical_after.st_nlink != 1
                    or (canonical_after.st_dev, canonical_after.st_ino)
                    != identity
                    or (path_after.st_dev, path_after.st_ino) != identity
                    or not stat.S_ISDIR(parent_after.st_mode)
                    or (parent_after.st_dev, parent_after.st_ino)
                    != (parent_before.st_dev, parent_before.st_ino)
                ):
                    raise Refusal(f"{label} final canonical custody mismatch")
            finally:
                os.close(canonical)
            custody.verify_all()
            return hashlib.sha256(raw).hexdigest()
        finally:
            if identity is None:
                current = os.fstat(descriptor)
                identity = (current.st_dev, current.st_ino)
            _unlink_if_owned_at(
                parent_descriptor, temporary_name, *identity,
            )
            # Never remove a canonical link after publication.  A post-link
            # failure remains inspectable and makes a retry refuse no-clobber.
            os.close(descriptor)
    finally:
        if owns_parent_descriptor:
            os.close(parent_descriptor)


def exact_int(value: object) -> bool:
    return type(value) is int


def rss_bytes() -> int:
    observed = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return observed * 1024 if sys.platform.startswith("linux") else observed


def carrier_words(length: int, q: int) -> np.ndarray:
    return np.asarray(v004.sealed.fixed_words(2 * length, q), dtype=WORD_DTYPE)


def lineage_words(prefix: int, q: int) -> np.ndarray:
    return np.asarray(v004.sealed.fixed_words(prefix, q), dtype=WORD_DTYPE)


def operator_q_bytes(length: int, q: int) -> int:
    edge_pairs = 3 * length * (math.comb(2 * length - 2, q - 1) if q else 0)
    return 4 * math.comb(2 * length, q) + 8 * edge_pairs + 8 * (3 * length + 1)


def operator_bytes(length: int) -> int:
    return sum(operator_q_bytes(length, q) for q in range(length + 1))


def admission_bytes(length: int) -> int:
    return sum(
        8 * math.comb(2 * length - 1, q)
        for event in range(length)
        for q in range(event + 1)
    )


def lineage_mask_bytes(length: int) -> int:
    return sum(4 * 2**prefix for prefix in range(length))


def lineage_map_bytes(length: int) -> int:
    return sum(8 * 2**prefix for prefix in range(length - 1))


def payload_bytes(length: int) -> int:
    return operator_bytes(length) + admission_bytes(length) + lineage_mask_bytes(length) + lineage_map_bytes(length)


def maximum_state_bytes(length: int) -> int:
    if length == 1:
        return 16
    dimensions = [
        sum(math.comb(prefix, q) * math.comb(2 * length, q) for q in range(prefix + 1))
        for prefix in range(length)
    ]
    return 16 * max(dimensions[index] + dimensions[index + 1] for index in range(length - 1))


def maximum_state_file_bytes(length: int) -> int:
    """Exact two-prefix complex payload plus one 128-byte NPY header per shard."""
    if type(length) is not int or length < 1:
        raise Refusal("state-file length must be a positive exact integer")
    simultaneous_shards = 1 if length == 1 else 2 * length - 1
    return maximum_state_bytes(length) + 128 * simultaneous_shards


def maximum_cache_window_bytes(length: int) -> int:
    return max(terminal_cache_peak_bytes(length), authentication_cache_peak_bytes(length))


def carrier_word_bytes(length: int, q: int) -> int:
    return 4 * math.comb(2 * length, q)


def admission_pair_bytes(length: int, q: int) -> int:
    return 8 * math.comb(2 * length - 1, q)


def terminal_cache_peak_bytes(length: int) -> int:
    # During child-one routing for old q, V004 still holds the old carrier-word
    # view and both admission maps while the q+1 destination sector is mapped.
    return max(
        operator_q_bytes(length, q + 1)
        + carrier_word_bytes(length, q)
        + admission_pair_bytes(length, q)
        for q in range(length)
    )


def authentication_cache_peak_bytes(length: int) -> int:
    # Conservative descriptor/mapping authentication peak: all carrier word
    # views, the largest non-word operator sector, and the largest admission
    # pair.  This intentionally dominates the implementation's close timing.
    all_carrier_words = sum(carrier_word_bytes(length, q) for q in range(length + 1))
    largest_nonword_operator = max(
        operator_q_bytes(length, q) - carrier_word_bytes(length, q)
        for q in range(length + 1)
    )
    largest_admission_pair = max(admission_pair_bytes(length, q) for q in range(length))
    return all_carrier_words + largest_nonword_operator + largest_admission_pair


def expected_file_count(length: int) -> int:
    operator = 4 * (length + 1)
    admission = 2 * sum(event + 1 for event in range(length))
    masks = sum(prefix + 1 for prefix in range(length))
    maps = 2 * sum(prefix + 1 for prefix in range(length - 1))
    return operator + admission + masks + maps


def safe_repo_file(relative: object, digest: object, label: str) -> Path:
    if (
        not isinstance(relative, str)
        or not relative
        or not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
        or Path(relative).is_absolute()
        or ".." in Path(relative).parts
    ):
        raise Refusal(f"{label}: unsafe path")
    candidate = ROOT / relative
    try:
        path = candidate.resolve()
    except (OSError, RuntimeError) as error:
        raise Refusal(f"{label}: unsafe path") from error
    if candidate.is_symlink() or not path.is_relative_to(ROOT.resolve()) or not path.is_file():
        raise Refusal(f"{label}: custody mismatch")
    stable_file_sha256(
        path, label, digest, require_immutable_mode=False
    )
    return path


def frozen_dependencies() -> dict[str, object]:
    return {
        "target_v004_implementation": TARGET_V004_SHA256,
        "target_v004_method": TARGET_METHOD_V004_SHA256,
        "target_v004_freeze": TARGET_FREEZE_V004_SHA256,
        "target_v004_original_l12_gate": TARGET_L12_GATE_V004_SHA256,
        "hostile_v003_implementation": HOSTILE_V003_SHA256,
        "hostile_v003_method": HOSTILE_METHOD_V003_SHA256,
        "hostile_v003_freeze": HOSTILE_FREEZE_V003_SHA256,
        "preserved_workspace_custody_v002": PRESERVED_WORKSPACE_CUSTODY_SHA256,
        "preserved_workspace_cross_diagnostic_v001": PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_SHA256,
        "target_v004_invariants": TARGET_V004_INVARIANTS_SHA256,
        "independent_l10_gate_v002": INDEPENDENT_L10_GATE_V002_SHA256,
        "canonical_v004_history_sha256_by_L": CANONICAL_V004_HISTORY_SHA256,
        "target_v005_runtime_compatibility_obstruction_v001": RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256,
        "target_v006_hostile_audit_obstruction_v001": V006_HOSTILE_OBSTRUCTION_SHA256,
        "target_v007_runtime_compatibility_obstruction_v001": V007_RUNTIME_OBSTRUCTION_SHA256,
        "target_v008_postbuild_audit_binding_obstruction_v001": V008_BINDING_OBSTRUCTION_SHA256,
        "target_v009_hostile_audit_obstruction_v001": V009_HOSTILE_OBSTRUCTION_SHA256,
        "target_v010_hostile_audit_obstruction_v001": V010_HOSTILE_OBSTRUCTION_SHA256,
        "target_v010_audit_record_custody_correction_v001": V010_CUSTODY_CORRECTION_SHA256,
        "target_v011_hostile_audit_obstruction_v001": V011_HOSTILE_OBSTRUCTION_SHA256,
        "v012_audit_obligation_contract_v001": AUDIT_OBLIGATION_CONTRACT_SHA256[
            "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/AUDIT_OBLIGATIONS_V001.json"
        ],
        "v012_audit_obligation_contract_manifest": AUDIT_OBLIGATION_CONTRACT_SHA256[
            "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/MANIFEST.sha256"
        ],
        "v012_authorization_dag_model_v001": AUTHORIZATION_DAG_MODEL_SHA256[
            "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/authorization_model.py"
        ],
        "v012_authorization_dag_model_result_v001": AUTHORIZATION_DAG_MODEL_SHA256[
            "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/RESULT.json"
        ],
        "v012_authorization_dag_model_manifest": AUTHORIZATION_DAG_MODEL_SHA256[
            "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/MANIFEST.sha256"
        ],
        "v012_dual_launch_coordinator_packet": DUAL_LAUNCH_COORDINATOR_SHA256,
        "v012_production_dag_refinement_sources": TRACK_C_REFINEMENT_SHA256,
    }


def frozen_storage_census() -> dict[str, dict[str, int]]:
    answer: dict[str, dict[str, int]] = {}
    for length in SUPPORTED:
        payload = payload_bytes(length)
        state = maximum_state_file_bytes(length)
        answer[str(length)] = {
            "payload_bytes": payload,
            "maximum_live_state_bytes": state,
            "state_plus_cache_bytes": state + payload,
            "terminal_cache_peak_bytes": terminal_cache_peak_bytes(length),
            "authentication_cache_peak_bytes": authentication_cache_peak_bytes(length),
            "maximum_cache_window_bytes": maximum_cache_window_bytes(length),
            "state_plus_cache_plus_reserve_bytes": state + payload + OVERHEAD_RESERVE,
        }
    return answer


def require_audit_preparation_contracts() -> None:
    obligation_result, _ = immutable_json(
        ROOT / "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/VALIDATION_RESULT_V001.json",
        "V012 audit-obligation validation",
        AUDIT_OBLIGATION_CONTRACT_SHA256[
            "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/VALIDATION_RESULT_V001.json"
        ],
    )
    expected_obligation_counts = {
        "V011_findings_mapped": 6,
        "V012_checklist_items_mapped": 18,
        "artifact_mutation_assignments": 477,
        "artifact_rule_statements": 375,
        "artifacts": 26,
        "independence_checks": 17,
        "mutation_classes": 36,
        "positive_fixtures": 33,
        "scope_checks": 24,
        "stages": 17,
        "structural_checks": 1305,
    }
    if (
        set(obligation_result) != {
            "schema", "classification", "matrix_sha256", "methodology_sha256",
            "validator_sha256", "target_validator_imported",
            "canonical_gate_cache_workspace_history_or_physics_created",
            "counts", "claim_boundary",
        }
        or obligation_result.get("schema")
        != "TARGET_V012_AUDIT_OBLIGATION_SPEC_VALIDATION_V001"
        or obligation_result.get("classification")
        != "PASS_PREREGISTERED_AUDIT_OBLIGATION_SPEC"
        or obligation_result.get("matrix_sha256")
        != AUDIT_OBLIGATION_CONTRACT_SHA256[
            "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/AUDIT_OBLIGATIONS_V001.json"
        ]
        or obligation_result.get("methodology_sha256")
        != AUDIT_OBLIGATION_CONTRACT_SHA256[
            "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/METHODOLOGY.md"
        ]
        or obligation_result.get("validator_sha256")
        != AUDIT_OBLIGATION_CONTRACT_SHA256[
            "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/validate_obligation_spec.py"
        ]
        or obligation_result.get("target_validator_imported") is not False
        or obligation_result.get(
            "canonical_gate_cache_workspace_history_or_physics_created"
        ) is not False
        or obligation_result.get("counts") != expected_obligation_counts
        or any(type(value) is not int or value <= 0
               for value in obligation_result["counts"].values())
        or obligation_result.get("claim_boundary")
        != "AUDIT_PREPARATION_VALIDATION_ONLY__NO_GATE_CACHE_WORKSPACE_HISTORY_OR_PHYSICS_RESULT"
    ):
        raise Refusal("V012 audit-obligation contract validation mismatch")

    dag_result, _ = immutable_json(
        ROOT / "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/RESULT.json",
        "V012 authorization-DAG model result",
        AUTHORIZATION_DAG_MODEL_SHA256[
            "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/RESULT.json"
        ],
    )
    if (
        dag_result
        != {
            "checker_sha256": AUTHORIZATION_DAG_MODEL_SHA256[
                "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/exhaustive_check.py"
            ],
            "graph": {"direct_edges": 22, "stages": 18, "transitive_edges": 147},
            "malformed_inputs": {"malformed_input_refusals": 12},
            "model_sha256": AUTHORIZATION_DAG_MODEL_SHA256[
                "AUDIT_PREPARATION_R_L12_AUTHORIZATION_STATE_MODEL_V001/authorization_model.py"
            ],
            "predecessor_mutations": {
                "direct_failed_predecessor_mutations": 22,
                "direct_invalid_predecessor_mutations": 22,
                "direct_missing_predecessor_mutations": 22,
                "global_negative_state_action_refusals": 648,
            },
            "reachability": {
                "final_adjudication_witness_position": 18,
                "l10_authorization_witness_position": 9,
                "l12_handshake_witness_position": 15,
                "l4_l6_l8_independently_enabled_after_base_gate": [
                    "CONTROL_L4", "CONTROL_L6", "CONTROL_L8"
                ],
            },
            "result": "PASS",
            "schema": "l12_authorization_state_model_check_v1",
            "scope": "abstract authorization ordering only; no physical compute or authority files",
            "state_space": {
                "boolean_states": 262144,
                "invalid_state_action_refusals": 4718124,
                "invalid_states": 262118,
                "legal_states": 26,
                "validator_oracle_agreements": 262144,
            },
            "transitions": {
                "allowed_transitions": 33,
                "bfs_reachable_states": 26,
                "duplicate_transition_refusals": 232,
                "legal_state_action_attempts": 468,
                "missing_predecessor_refusals": 203,
            },
        }
        or any(
            type(value) is not int
            for section in ("graph", "malformed_inputs", "predecessor_mutations", "state_space", "transitions")
            for value in dag_result[section].values()
        )
    ):
        raise Refusal("V012 authorization-DAG model result mismatch")


def validate_freeze_document(freeze: object) -> dict[str, object]:
    if not isinstance(freeze, dict):
        raise Refusal("V012 freeze is not an object")
    if set(freeze) != {
        "schema",
        "status",
        "frozen_before_nonphysical_preflight_output",
        "cache_payload_created",
        "physical_history_executed",
        "current_v004_target_or_hostile_execution_interrupted",
        "current_v004_workspace_output_or_cache_read_or_modified",
        "sealed_input_commit",
        "files",
        "sealed_dependencies",
        "obstruction_evidence",
        "predecessor_compatibility_custody",
        "predecessor_v006_obstruction_custody",
        "predecessor_v007_obstruction_custody",
        "predecessor_v008_obstruction_custody",
        "predecessor_v009_obstruction_custody",
        "predecessor_v010_obstruction_custody",
        "predecessor_v011_obstruction_custody",
        "hard_locks",
        "storage_census_including_offsets_and_full_masks",
        "resource_limits",
        "claim_boundary",
    }:
        raise Refusal("V012 freeze top-level census mismatch")
    if (
        freeze.get("schema") != "TARGET_L12_STORAGE_CACHE_FREEZE_V012"
        or freeze.get("status") != "FROZEN_BEFORE_NONPHYSICAL_PREFLIGHT_V001_OUTPUT"
        or freeze.get("frozen_before_nonphysical_preflight_output") is not True
        or freeze.get("cache_payload_created") is not False
        or freeze.get("physical_history_executed") is not False
        or freeze.get("current_v004_target_or_hostile_execution_interrupted") is not False
        or freeze.get("current_v004_workspace_output_or_cache_read_or_modified") is not False
        or freeze.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or freeze.get("claim_boundary")
        != "AUDIT_BOUND_COMPATIBILITY_SUCCESSOR_PRE_PAYLOAD__NO_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
    ):
        raise Refusal("V012 freeze identity/status/claim mismatch")
    files = freeze.get("files")
    expected_paths = {
        "METHOD.md": METHOD,
        "build_target_cache.py": Path(__file__),
        "consume_target_cache.py": CONSUMER,
        "validate_preflight.py": PREFLIGHT,
        "production_obligation_validators.py": PRODUCTION_VALIDATORS,
    }
    if not isinstance(files, dict) or set(files) != set(expected_paths):
        raise Refusal("V012 frozen file census mismatch")
    for name, path in expected_paths.items():
        digest = files.get(name)
        if (
            not isinstance(digest, str)
            or len(digest) != 64
            or immutable_file_sha256(path, f"V012 frozen source {name}") != digest
        ):
            raise Refusal(f"V012 frozen file drift: {name}")
    if freeze.get("sealed_dependencies") != frozen_dependencies():
        raise Refusal("V012 frozen dependency census mismatch")
    dependency_paths = {
        TARGET_V004: TARGET_V004_SHA256,
        TARGET_METHOD_V004: TARGET_METHOD_V004_SHA256,
        TARGET_FREEZE_V004: TARGET_FREEZE_V004_SHA256,
        TARGET_L12_GATE_V004: TARGET_L12_GATE_V004_SHA256,
        HOSTILE_V003: HOSTILE_V003_SHA256,
        HOSTILE_METHOD_V003: HOSTILE_METHOD_V003_SHA256,
        HOSTILE_FREEZE_V003: HOSTILE_FREEZE_V003_SHA256,
        PRESERVED_WORKSPACE_CUSTODY: PRESERVED_WORKSPACE_CUSTODY_SHA256,
        PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC: PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_SHA256,
        TARGET_V004_INVARIANTS: TARGET_V004_INVARIANTS_SHA256,
        INDEPENDENT_L10_GATE_V002: INDEPENDENT_L10_GATE_V002_SHA256,
        RUNTIME_COMPATIBILITY_OBSTRUCTION: RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256,
        V006_HOSTILE_OBSTRUCTION: V006_HOSTILE_OBSTRUCTION_SHA256,
        V007_RUNTIME_OBSTRUCTION: V007_RUNTIME_OBSTRUCTION_SHA256,
        V008_BINDING_OBSTRUCTION: V008_BINDING_OBSTRUCTION_SHA256,
        V009_HOSTILE_OBSTRUCTION: V009_HOSTILE_OBSTRUCTION_SHA256,
        V010_HOSTILE_OBSTRUCTION: V010_HOSTILE_OBSTRUCTION_SHA256,
        V010_CUSTODY_CORRECTION: V010_CUSTODY_CORRECTION_SHA256,
        V011_HOSTILE_OBSTRUCTION: V011_HOSTILE_OBSTRUCTION_SHA256,
        **{ROOT / relative: digest
           for relative, digest in AUDIT_OBLIGATION_CONTRACT_SHA256.items()},
        **{ROOT / relative: digest
           for relative, digest in AUTHORIZATION_DAG_MODEL_SHA256.items()},
        **{ROOT / relative: digest
           for relative, digest in DUAL_LAUNCH_COORDINATOR_SHA256.items()},
        **{ROOT / relative: digest
           for relative, digest in TRACK_C_REFINEMENT_SHA256.items()},
        **{path: CANONICAL_V004_HISTORY_SHA256[length]
           for length, path in CANONICAL_V004_HISTORY_PATH.items()},
    }
    immutable_contract_paths = {
        ROOT / relative
        for relative in (
            set(AUDIT_OBLIGATION_CONTRACT_SHA256)
            | set(AUTHORIZATION_DAG_MODEL_SHA256)
            | set(DUAL_LAUNCH_COORDINATOR_SHA256)
            | set(TRACK_C_REFINEMENT_SHA256)
        )
    }
    for path, digest in dependency_paths.items():
        stable_file_sha256(
            path,
            f"V012 frozen dependency {path.name}",
            digest,
            require_immutable_mode=path in immutable_contract_paths,
        )
    require_audit_preparation_contracts()
    if freeze.get("obstruction_evidence") != EVIDENCE_SHA256:
        raise Refusal("V012 frozen obstruction-evidence census mismatch")
    for relative, digest in EVIDENCE_SHA256.items():
        path = ROOT / relative
        stable_file_sha256(
            path, f"V012 obstruction evidence {relative}", digest,
            require_immutable_mode=False,
        )
    if freeze.get("predecessor_compatibility_custody") != PREDECESSOR_CUSTODY_SHA256:
        raise Refusal("V012 predecessor-compatibility census mismatch")
    for relative, digest in PREDECESSOR_CUSTODY_SHA256.items():
        path = ROOT / relative
        stable_file_sha256(
            path, f"V012 predecessor compatibility {relative}", digest,
            require_immutable_mode=False,
        )
    if freeze.get("predecessor_v006_obstruction_custody") != V006_CUSTODY_SHA256:
        raise Refusal("V012 predecessor-V006 obstruction census mismatch")
    for relative, digest in V006_CUSTODY_SHA256.items():
        path = ROOT / relative
        stable_file_sha256(
            path, f"V012 predecessor V006 {relative}", digest,
            require_immutable_mode=False,
        )
    if freeze.get("predecessor_v007_obstruction_custody") != V007_CUSTODY_SHA256:
        raise Refusal("V012 predecessor-V007 obstruction census mismatch")
    for relative, digest in V007_CUSTODY_SHA256.items():
        path = ROOT / relative
        stable_file_sha256(
            path, f"V012 predecessor V007 {relative}", digest,
            require_immutable_mode=False,
        )
    if freeze.get("predecessor_v008_obstruction_custody") != V008_CUSTODY_SHA256:
        raise Refusal("V012 predecessor-V008 obstruction census mismatch")
    for relative, digest in V008_CUSTODY_SHA256.items():
        path = ROOT / relative
        stable_file_sha256(
            path, f"V012 predecessor V008 {relative}", digest,
            require_immutable_mode=False,
        )
    if freeze.get("predecessor_v009_obstruction_custody") != V009_CUSTODY_SHA256:
        raise Refusal("V012 predecessor-V009 obstruction census mismatch")
    for relative, digest in V009_CUSTODY_SHA256.items():
        path = ROOT / relative
        stable_file_sha256(
            path, f"V012 predecessor V009 {relative}", digest,
            require_immutable_mode=False,
        )
    if freeze.get("predecessor_v010_obstruction_custody") != V010_CUSTODY_SHA256:
        raise Refusal("V012 predecessor-V010 obstruction census mismatch")
    for relative, digest in V010_CUSTODY_SHA256.items():
        path = ROOT / relative
        stable_file_sha256(
            path, f"V012 predecessor V010 {relative}", digest,
            require_immutable_mode=False,
        )
    if freeze.get("predecessor_v011_obstruction_custody") != V011_CUSTODY_SHA256:
        raise Refusal("V012 predecessor-V011 obstruction census mismatch")
    for relative, digest in V011_CUSTODY_SHA256.items():
        path = ROOT / relative
        stable_file_sha256(
            path, f"V012 predecessor V011 {relative}", digest,
            require_immutable_mode=False,
        )
    hard_locks = {
        "dual_obstruction_and_compatibility_gate": "DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE_V012.json",
        "dual_obstruction_and_compatibility_gate_present_at_freeze": False,
        "independent_hostile_audit": FUTURE_HOSTILE_AUDIT_PATH,
        "independent_hostile_audit_present_at_freeze": False,
        "postbuild_payload_audit": FUTURE_POSTBUILD_AUDIT_PATH,
        "postbuild_payload_audit_present_at_freeze": False,
        "physical_execution_gate": "PHYSICAL_EXECUTION_GATE_V012.json",
        "physical_execution_gate_present_at_freeze": False,
        "physical_gate_hostile_audit": FUTURE_PHYSICAL_GATE_AUDIT_PATH,
        "physical_gate_hostile_audit_present_at_freeze": False,
        "control_execution_authorization_gate": "CONTROL_EXECUTION_AUTHORIZATION_GATE_V012.json",
        "control_execution_authorization_gate_present_at_freeze": False,
        "cached_control_l4_l8_gate": "CACHED_CONTROL_L4_L8_GATE_V012.json",
        "cached_control_l4_l8_gate_present_at_freeze": False,
        "cached_control_l4_l8_gate_audit": "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_CONTROL_L4_L8_GATE_AUDIT_V001.json",
        "cached_control_l4_l8_gate_audit_present_at_freeze": False,
        "l10_execution_authorization_gate": "L10_EXECUTION_AUTHORIZATION_GATE_V012.json",
        "l10_execution_authorization_gate_present_at_freeze": False,
        "cached_l10_gate": "CACHED_L10_GATE_V012.json",
        "cached_l10_gate_present_at_freeze": False,
        "cached_l10_gate_audit": "AUDIT_R_L12_TARGET_STORAGE_CACHE_V012/CACHED_L10_GATE_AUDIT_V001.json",
        "cached_l10_gate_audit_present_at_freeze": False,
        "target_l12_execution_gate": "TARGET_L12_EXECUTION_GATE_V012.json",
        "target_l12_execution_gate_present_at_freeze": False,
        "target_hostile_l10_cross_gate": "AUDIT_R_L12_PARALLEL_EXECUTION_V001/TARGET_HOSTILE_L10_CROSS_GATE_V001.json",
        "target_hostile_l10_cross_gate_present_at_freeze": False,
        "parallel_l12_run_schedule_gate": "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_V001.json",
        "parallel_l12_run_schedule_gate_present_at_freeze": False,
        "parallel_l12_run_schedule_gate_audit": "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_SCHEDULE_GATE_AUDIT_V001.json",
        "parallel_l12_run_schedule_gate_audit_present_at_freeze": False,
        "dual_l12_launch_handshake": "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_LAUNCH_HANDSHAKE_V002.json",
        "dual_l12_launch_handshake_present_at_freeze": False,
        "dual_l12_worker_release": "AUDIT_R_L12_PARALLEL_EXECUTION_V001/DUAL_L12_WORKER_RELEASE_V002.json",
        "dual_l12_worker_release_present_at_freeze": False,
        "parallel_l12_telemetry": "AUDIT_R_L12_PARALLEL_EXECUTION_V001/SHARED_AGGREGATE_TELEMETRY_V001.json",
        "parallel_l12_telemetry_present_at_freeze": False,
        "final_l12_audit": "AUDIT_R_L12_PARALLEL_EXECUTION_V001/FINAL_L12_TARGET_HOSTILE_AUDIT_V001.json",
        "final_l12_audit_present_at_freeze": False,
        "hostile_v004r4_cache_build_authorization": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json",
        "hostile_v004r4_cache_build_authorization_present_at_freeze": False,
        "hostile_v004r4_l10_execution_authorization": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/L10_EXECUTION_AUTHORIZATION_GATE_V004R4.json",
        "hostile_v004r4_l10_execution_authorization_present_at_freeze": False,
        "hostile_v004r4_cache_payloads": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_CACHE_PAYLOADS",
        "hostile_v004r4_cache_payloads_present_at_freeze": False,
        "hostile_v004r4_cached_l10_gate": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/CACHED_L10_GATE_V004R4.json",
        "hostile_v004r4_cached_l10_gate_present_at_freeze": False,
        "hostile_v004r4_postbuild_payload_audit": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json",
        "hostile_v004r4_postbuild_payload_audit_present_at_freeze": False,
        "hostile_v004r4_physical_outputs": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_PHYSICAL_OUTPUTS",
        "hostile_v004r4_physical_outputs_present_at_freeze": False,
        "hostile_v004r4_workspaces": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V004R4_WORKSPACES",
        "hostile_v004r4_workspaces_present_at_freeze": False,
        "hostile_v004r4_l12_execution_gate": "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/HOSTILE_L12_EXECUTION_GATE_V004R4.json",
        "hostile_v004r4_l12_execution_gate_present_at_freeze": False,
    }
    if not exact_tree_equal(freeze.get("hard_locks"), hard_locks):
        raise Refusal("V012 frozen gate census mismatch")
    if not exact_tree_equal(
        freeze.get("storage_census_including_offsets_and_full_masks"),
        frozen_storage_census(),
    ):
        raise Refusal("V012 frozen storage/resource census mismatch")
    resources = {
        "numerical_workset_bytes": v004.v3.CAP_BYTES,
        "mapped_cache_bytes": MAPPED_CACHE_LIMIT,
        "builder_rss_bytes": BUILDER_RSS_LIMIT,
        "consumer_rss_bytes": v004.RSS_LIMIT,
        "scratch_bytes": SCRATCH_LIMIT,
        "overhead_reserve_bytes": OVERHEAD_RESERVE,
        "wall_seconds": int(WALL_LIMIT),
        "parallel_l12": {
            "target_rss_limit_bytes": v004.RSS_LIMIT,
            "target_authentication_peak_bytes": PARALLEL_TARGET_AUTHENTICATION_PEAK,
            "hostile_rss_limit_bytes": PARALLEL_HOSTILE_RSS_LIMIT,
            "hostile_authentication_peak_bytes": PARALLEL_HOSTILE_AUTHENTICATION_PEAK,
            "combined_conservative_peak_bytes": PARALLEL_AGGREGATE_PEAK,
            "minimum_host_total_bytes": PARALLEL_HOST_TOTAL_MINIMUM,
            "minimum_host_headroom_bytes": PARALLEL_HOST_HEADROOM_MINIMUM,
            "target_scratch_minimum_bytes": PARALLEL_TARGET_SCRATCH_MINIMUM,
            "hostile_scratch_minimum_bytes": PARALLEL_HOSTILE_SCRATCH_MINIMUM,
            "combined_filesystem_minimum_bytes": PARALLEL_FILESYSTEM_MINIMUM,
            "maximum_telemetry_age_seconds": 300,
        },
    }
    if not exact_tree_equal(freeze.get("resource_limits"), resources):
        raise Refusal("V012 frozen resource limits mismatch")
    validate_production_obligation("A01_FREEZE_AND_SOURCE_PACKET", freeze)
    return freeze


def require_frozen_census() -> dict[str, object]:
    if FREEZE.is_symlink() or not FREEZE.is_file():
        raise Refusal("V012 freeze absent or symlinked")
    freeze, _digest = immutable_json(FREEZE, "V012 freeze")
    return validate_freeze_document(freeze)


def require_original_target_gate() -> dict[str, object]:
    gate, _digest = immutable_json(
        TARGET_L12_GATE_V004, "original target gate", TARGET_L12_GATE_V004_SHA256,
        require_immutable_mode=False,
    )
    if (
        gate.get("schema") != "R_TARGET_Q_SHARDED_HISTORY_GATE_V004"
        or gate.get("classification") != "PASS_TARGET_Q_SHARDED_L4_L10_GATE_V004"
        or gate.get("implementation_sha256") != TARGET_V004_SHA256
        or gate.get("checks_passed") != 273
        or gate.get("checks_total") != 273
        or gate.get("failures") != []
        or set(gate.get("histories", {})) != {"4", "6", "8", "10"}
    ):
        raise Refusal("original target V004 L4-L10 gate content mismatch")
    return gate


def require_preserved_workspace_custody() -> dict[str, object]:
    record, _ = immutable_json(
        PRESERVED_WORKSPACE_CUSTODY, "preserved L12 workspace custody",
        PRESERVED_WORKSPACE_CUSTODY_SHA256, require_immutable_mode=False,
    )
    if (
        record.get("schema") != "L12_PRESERVED_WORKSPACE_CUSTODY_V002"
        or record.get("classification") != "PASS_PRESERVED_H11_STRUCTURAL_CUSTODY_OBSERVATION"
        or record.get("checks_passed") != 48
        or record.get("checks_total") != 48
        or record.get("target", {}).get("implementation_sha256") != TARGET_V004_SHA256
        or record.get("hostile", {}).get("implementation_sha256") != HOSTILE_V003_SHA256
    ):
        raise Refusal("preserved L12 workspace custody content mismatch")
    return record


def require_preserved_workspace_cross_diagnostic() -> dict[str, object]:
    record, _ = immutable_json(
        PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC,
        "preserved L12 workspace cross-diagnostic",
        PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_SHA256,
        require_immutable_mode=False,
    )
    shards = record.get("shards")
    if (
        record.get("schema") != "L12_PRESERVED_INCOMPLETE_COARSE_H11_CROSS_DIAGNOSTIC_V001"
        or record.get("classification")
        != "INCOMPLETE_COARSE_PARTIAL_STATE_DIAGNOSTIC__NOT_A_HISTORY_OR_RESTART_GATE"
        or record.get("source_custody_sha256") != PRESERVED_WORKSPACE_CUSTODY_SHA256
        or record.get("completed_history_output_present") is not False
        or record.get("eligible_as_restart_state") is not False
        or record.get("eligible_as_target_hostile_equivalence_result") is not False
        or record.get("maximum_absolute_amplitude_difference") != 0.00004826848271244497
        or record.get("maximum_difference_q") != 11
        or record.get("within_final_history_tolerance") is not False
        or record.get("stability_check")
        != "every source shard was SHA-256 hashed before and after comparison and remained unchanged"
        or record.get("disposition")
        != "preserve both workspaces as obstruction evidence; do not promote or consume their incomplete coarse states; rerun complete cached histories independently"
        or not isinstance(shards, list)
        or len(shards) != 12
        or [row.get("q") for row in shards if isinstance(row, dict)] != list(range(12))
    ):
        raise Refusal("preserved L12 workspace cross-diagnostic content mismatch")
    if any(
        type(row.get("maximum_absolute_amplitude_difference")) not in (int, float)
        or not math.isfinite(float(row["maximum_absolute_amplitude_difference"]))
        or float(row["maximum_absolute_amplitude_difference"]) < 0.0
        or (int(row["q"]) <= 10 and float(row["maximum_absolute_amplitude_difference"]) > 1.05e-12)
        or (int(row["q"]) == 11 and row["maximum_absolute_amplitude_difference"] != 0.00004826848271244497)
        for row in shards
    ):
        raise Refusal("preserved L12 workspace cross-diagnostic shard bounds mismatch")
    return record


def require_runtime_compatibility_obstruction() -> dict[str, object]:
    record, _ = immutable_json(
        RUNTIME_COMPATIBILITY_OBSTRUCTION,
        "target V005 runtime-compatibility obstruction",
        RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256,
        require_immutable_mode=False,
    )
    if (
        record.get("schema") != "TARGET_V005_CACHE_RUNTIME_COMPATIBILITY_OBSTRUCTION_V001"
        or record.get("classification")
        != "FAIL_PREPHYSICAL_CACHE_AUTHENTICATION__SUPERSEDE_TARGET_V005_PAYLOADS"
        or record.get("stage")
        != "first independent CacheContext authentication after storage-only payload construction"
        or record.get("command_scope")
        != "read-only authentication of L4 before any physical-execution gate, workspace, or history"
        or record.get("exception_type") != "TypeError"
        or record.get("exception") != "stat() got an unexpected keyword argument 'follow_symlinks'"
        or record.get("failing_implementation_sha256")
        != "99caa8f7c0f4cffb4710519ac402c8d56ebbf28121002e1cf39cbd497df80171"
        or record.get("failing_line") != 171
        or record.get("additional_occurrences") != [391, 405, 416]
        or record.get("dual_gate_sha256") != V005_DUAL_GATE_SHA256
        or record.get("cache_manifests") != V005_CACHE_MANIFEST_SHA256
        or record.get("payload_bytes_are_preserved") is not True
        or record.get("payloads_eligible_for_consumption") is not False
        or record.get("physical_execution_gate_present") is not False
        or record.get("physical_workspace_created") is not False
        or record.get("physical_history_output_created") is not False
        or record.get("required_disposition")
        != "preserve V005 gate and payload bytes as superseded compatibility-obstruction evidence; implement, freeze, preflight, and independently audit a V006 successor; build new payloads under a distinct canonical path"
    ):
        raise Refusal("target V005 runtime-compatibility obstruction content mismatch")
    stable_file_sha256(
        V005_DUAL_GATE, "superseded V005 dual gate", V005_DUAL_GATE_SHA256,
        require_immutable_mode=False,
    )
    for length, digest in V005_CACHE_MANIFEST_SHA256.items():
        path = V005_DIR / "CACHE_PAYLOADS" / f"L{length}" / "CACHE_MANIFEST.json"
        stable_file_sha256(
            path, f"superseded V005 L{length} manifest", digest,
            require_immutable_mode=False,
        )
    if any(
        path.exists()
        for path in (
            V005_DIR / "PHYSICAL_EXECUTION_GATE_V005.json",
            V005_DIR / "PHYSICAL_OUTPUTS",
            V005_DIR / "WORKSPACES",
        )
    ):
        raise Refusal("superseded V005 acquired a physical gate, workspace, or output")
    return record


def require_v006_hostile_audit_obstruction() -> dict[str, object]:
    for relative, digest in V006_CUSTODY_SHA256.items():
        safe_repo_file(relative, digest, "target V006 obstruction parent")
    record, _ = immutable_json(
        V006_HOSTILE_OBSTRUCTION, "target V006 hostile-audit obstruction",
        V006_HOSTILE_OBSTRUCTION_SHA256, require_immutable_mode=False,
    )
    summary = record.get("adversarial_summary")
    failures = record.get("failures")
    disposition = record.get("required_disposition")
    absences = record.get("absence_census_at_audit")
    if (
        record.get("schema") != "TARGET_V006_HOSTILE_AUDIT_OBSTRUCTION_V001"
        or record.get("classification")
        != "FAIL_CONTROL_PLANE_AUTHORIZATION_NOT_AUDIT_BOUND_AND_SCHEDULE_CUSTODY_NOT_HOSTILE_BOUND"
        or record.get("resolved") is not False
        or record.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006"
        or record.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or record.get("frozen_files")
        != {
            "METHOD.md": V006_CUSTODY_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/METHOD.md"],
            "build_target_cache.py": V006_CUSTODY_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/build_target_cache.py"],
            "consume_target_cache.py": V006_CUSTODY_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/consume_target_cache.py"],
            "validate_preflight.py": V006_CUSTODY_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/validate_preflight.py"],
            "FREEZE.json": V006_CUSTODY_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/FREEZE.json"],
            "PREFLIGHT_RESULT_V001.json": V006_CUSTODY_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V006/PREFLIGHT_RESULT_V001.json"],
        }
        or not isinstance(summary, dict)
        or summary.get("checks_attempted") != 277
        or summary.get("checks_passed") != 275
        or summary.get("checks_failed") != 2
        or not isinstance(failures, list)
        or [row.get("id") for row in failures if isinstance(row, dict)]
        != ["V006-AUTHORIZATION-AUDIT-BINDING", "V006-PARALLEL-SCHEDULE-HOSTILE-CUSTODY"]
        or any(row.get("severity") != "BLOCKING" and row.get("severity") != "BLOCKING_FOR_L12" for row in failures)
        or not isinstance(absences, dict)
        or any(value is not False for value in absences.values())
        or not isinstance(disposition, dict)
        or disposition.get("v006_authorization") != "DO_NOT_AUTHORIZE_OR_BUILD"
        or disposition.get("successor")
        != "Create and freeze a distinct V007 successor; do not amend the frozen V006 sources."
        or record.get("claim_boundary")
        != "HOSTILE_CONTROL_PLANE_AUDIT_FAILURE_ONLY__NONPHYSICAL_ARITHMETIC_REMAINS_VALID__NO_CACHE_HISTORY_SPECTRUM_Z1_CONTINUUM_OR_GRAVITY"
    ):
        raise Refusal("target V006 hostile-audit obstruction content mismatch")
    return record


def require_v007_runtime_compatibility_obstruction() -> dict[str, object]:
    for relative, digest in V007_CUSTODY_SHA256.items():
        safe_repo_file(relative, digest, "target V007 obstruction parent")
    record, _ = immutable_json(
        V007_RUNTIME_OBSTRUCTION,
        "target V007 runtime-compatibility obstruction",
        V007_RUNTIME_OBSTRUCTION_SHA256,
    )
    if (
        record.get("schema") != "TARGET_V007_CACHE_RUNTIME_COMPATIBILITY_OBSTRUCTION_V001"
        or record.get("classification")
        != "FAIL_PREPHYSICAL_CACHE_AUTHENTICATION__SUPERSEDE_TARGET_V007_PAYLOADS"
        or record.get("stage")
        != "first actual CacheContext authentication after fresh V007 storage-only payload construction"
        or record.get("command_scope")
        != "read-only authentication of L4 before any physical-execution gate, workspace, or history"
        or record.get("exception_type") != "ValueError"
        or record.get("exception") != "cannot mmap an empty file"
        or record.get("failing_implementation")
        != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/consume_target_cache.py"
        or record.get("failing_implementation_sha256")
        != V007_CUSTODY_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V007/consume_target_cache.py"]
        or record.get("failing_line") != 403
        or record.get("trigger_path")
        != "CacheContext.__init__ -> validate_index_identities -> open(carrier_q_00_sources.i32) -> numpy.memmap"
        or record.get("trigger_record_bytes") != 0
        or record.get("affected_lengths") != list(SUPPORTED)
        or record.get("dual_gate_sha256") != V007_DUAL_GATE_SHA256
        or record.get("independent_prepayload_hostile_audit_sha256")
        != V007_HOSTILE_AUDIT_SHA256
        or record.get("cache_manifests") != V007_CACHE_MANIFEST_SHA256
        or record.get("payload_bytes_are_preserved") is not True
        or record.get("payloads_eligible_for_consumption") is not False
        or record.get("physical_execution_gate_present") is not False
        or record.get("physical_workspace_created") is not False
        or record.get("physical_history_output_created") is not False
        or record.get("required_disposition")
        != "preserve V007 gate and payload bytes as superseded compatibility-obstruction evidence; implement, freeze, preflight, and independently audit a V008 successor; build new payloads under a distinct canonical path"
        or record.get("claim_boundary")
        != "RUNTIME_CONTROL_PLANE_FAILURE_ONLY__NO_HISTORY_PHYSICS_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("target V007 runtime-compatibility obstruction content mismatch")
    for length, digest in V007_CACHE_MANIFEST_SHA256.items():
        path = V007_DIR / "CACHE_PAYLOADS_V007" / f"L{length}" / "CACHE_MANIFEST.json"
        stable_file_sha256(path, f"superseded V007 L{length} manifest", digest)
    if any(
        path.exists()
        for path in (
            V007_DIR / "PHYSICAL_EXECUTION_GATE_V007.json",
            V007_DIR / "PHYSICAL_OUTPUTS",
            V007_DIR / "WORKSPACES",
        )
    ):
        raise Refusal("superseded V007 acquired a physical gate, workspace, or output")
    return record


def require_v008_postbuild_binding_obstruction() -> dict[str, object]:
    for relative, digest in V008_CUSTODY_SHA256.items():
        safe_repo_file(relative, digest, "target V008 obstruction parent")
    record, _ = immutable_json(
        V008_BINDING_OBSTRUCTION,
        "target V008 postbuild-audit binding obstruction",
        V008_BINDING_OBSTRUCTION_SHA256,
    )
    audit_binding = record.get("postbuild_payload_audit")
    if (
        record.get("schema") != "TARGET_V008_POSTBUILD_AUDIT_BINDING_OBSTRUCTION_V001"
        or record.get("classification")
        != "FAIL_CLOSED__POSTBUILD_PAYLOAD_AUDIT_NOT_ENFORCED_BY_PHYSICAL_GATE_VALIDATOR"
        or record.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008"
        or record.get("frozen_consumer_sha256")
        != V008_CUSTODY_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008/consume_target_cache.py"]
        or record.get("physical_gate_validator") != "consume_target_cache.py:require_physical_gate"
        or audit_binding
        != {
            "path": "AUDIT_R_L12_TARGET_STORAGE_CACHE_V008/POSTBUILD_PAYLOAD_AUDIT_V001.json",
            "sha256": V008_POSTBUILD_AUDIT_SHA256,
            "schema": "TARGET_V008_POSTBUILD_PAYLOAD_AUDIT_V001",
            "classification": "PASS_TARGET_V008_FRESH_STORAGE_CACHE_PAYLOADS",
            "checks_passed": 3483,
            "checks_total": 3483,
        }
        or record.get("cache_manifests") != V008_CACHE_MANIFEST_SHA256
        or record.get("v008_payload_bytes_are_preserved") is not True
        or record.get("v008_payloads_eligible_for_physical_consumption") is not False
        or record.get("physical_execution_gate_present") is not False
        or record.get("physical_workspace_created") is not False
        or record.get("physical_history_output_created") is not False
        or record.get("required_disposition")
        != "preserve V008 sources, gates, caches, and audits as obstruction evidence; create a distinct frozen V009 successor whose physical authorization hard-binds the future postbuild payload audit and an independent physical-gate audit before any history workspace can be created"
        or record.get("claim_boundary")
        != "CONTROL_PLANE_BINDING_OBSTRUCTION_ONLY__POSTBUILD_PAYLOAD_AUDIT_PASSES_BUT_NO_PHYSICAL_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("target V008 postbuild-audit binding obstruction content mismatch")
    postbuild, _ = immutable_json(
        V008_POSTBUILD_AUDIT, "target V008 postbuild payload audit",
        V008_POSTBUILD_AUDIT_SHA256,
    )
    if (
        postbuild.get("schema") != "TARGET_V008_POSTBUILD_PAYLOAD_AUDIT_V001"
        or postbuild.get("classification") != "PASS_TARGET_V008_FRESH_STORAGE_CACHE_PAYLOADS"
        or postbuild.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V008"
        or postbuild.get("checks_total") != 3483
        or postbuild.get("checks_passed") != 3483
        or postbuild.get("failures") != []
        or postbuild.get("manifest_sha256_by_L") != V008_CACHE_MANIFEST_SHA256
        or postbuild.get("no_symlinked_or_writable_payload_inputs") is not True
        or postbuild.get("physical_gate_or_history_executed") is not False
    ):
        raise Refusal("target V008 postbuild payload audit content mismatch")
    for length, digest in V008_CACHE_MANIFEST_SHA256.items():
        path = V008_DIR / "CACHE_PAYLOADS_V008" / f"L{length}" / "CACHE_MANIFEST.json"
        stable_file_sha256(path, f"superseded V008 L{length} manifest", digest)
    if any(
        path.exists()
        for path in (
            V008_DIR / "PHYSICAL_EXECUTION_GATE_V008.json",
            V008_DIR / "PHYSICAL_OUTPUTS",
            V008_DIR / "WORKSPACES",
        )
    ):
        raise Refusal("superseded V008 acquired a physical gate, workspace, or output")
    return record


def require_v009_hostile_audit_obstruction() -> dict[str, object]:
    for relative, digest in V009_CUSTODY_SHA256.items():
        safe_repo_file(relative, digest, "target V009 obstruction parent")
    record, _ = immutable_json(
        V009_HOSTILE_OBSTRUCTION, "target V009 hostile-audit obstruction",
        V009_HOSTILE_OBSTRUCTION_SHA256,
    )
    summary = record.get("adversarial_summary")
    replay = record.get("preflight_replay")
    failures = record.get("failures")
    disposition = record.get("required_disposition")
    if (
        record.get("schema") != "TARGET_V009_HOSTILE_AUDIT_OBSTRUCTION_V001"
        or record.get("classification")
        != "FAIL_POSTBUILD_CHECK_CENSUS_UNVALIDATED_AND_BASE_PHYSICAL_GATE_NOT_EXACT"
        or record.get("resolved") is not False
        or record.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V009"
        or record.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or not isinstance(summary, dict)
        or summary.get("checks_attempted") != 6
        or summary.get("checks_passed") != 1
        or summary.get("checks_failed") != 5
        or not isinstance(replay, dict)
        or replay.get("checks_total") != 285
        or replay.get("checks_passed") != 285
        or replay.get("zero_length_cache_runtime_checks") != 5
        or not isinstance(failures, list)
        or [row.get("id") for row in failures if isinstance(row, dict)]
        != ["V009-POSTBUILD-CHECK-CENSUS", "V009-BASE-PHYSICAL-GATE-EXACTNESS"]
        or any(row.get("severity") != "BLOCKING" for row in failures)
        or not isinstance(disposition, dict)
        or disposition.get("v009_authorization") != "DO_NOT_AUTHORIZE_OR_BUILD"
        or disposition.get("successor")
        != "Create and freeze a distinct V010 successor; preserve V009 source, freeze, preflight, and this failure record without amendment."
        or record.get("claim_boundary")
        != "HOSTILE_CONTROL_PLANE_AUDIT_FAILURE_ONLY__NO_GATE_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        or record.get("v005_v006_v007_v008_bytes_preserved") is not True
        or any(value is not False for value in record.get("absence_census_at_audit", {}).values())
    ):
        raise Refusal("target V009 hostile-audit obstruction content mismatch")
    return record


def require_v010_hostile_audit_obstruction_and_correction() -> tuple[dict[str, object], dict[str, object]]:
    for relative, digest in V010_CUSTODY_SHA256.items():
        safe_repo_file(relative, digest, "target V010 obstruction parent")
    record, _ = immutable_json(
        V010_HOSTILE_OBSTRUCTION, "target V010 hostile-audit obstruction",
        V010_HOSTILE_OBSTRUCTION_SHA256,
    )
    correction, _ = immutable_json(
        V010_CUSTODY_CORRECTION, "target V010 audit-record custody correction",
        V010_CUSTODY_CORRECTION_SHA256,
    )
    summary = record.get("adversarial_summary")
    replay = record.get("preflight_replay")
    failures = record.get("failures")
    disposition = record.get("required_disposition")
    wrong_value = "ff063573868b96aa14b1bdee218c4d6e2c039b8ba844e9753a21ef74d81e6b1"
    if (
        record.get("schema") != "TARGET_V010_HOSTILE_AUDIT_OBSTRUCTION_V001"
        or record.get("classification")
        != "FAIL_POSTBUILD_CHECK_TYPES_NOT_EXACT_AND_PHYSICAL_GATE_AUDIT_CENSUS_UNATTESTED"
        or record.get("resolved") is not False
        or record.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V010"
        or record.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or not isinstance(summary, dict)
        or summary.get("checks_attempted") != 12
        or summary.get("checks_passed") != 9
        or summary.get("checks_failed") != 3
        or not isinstance(replay, dict)
        or replay.get("checks_total") != 288
        or replay.get("checks_passed") != 288
        or not isinstance(failures, list)
        or [row.get("id") for row in failures if isinstance(row, dict)]
        != [
            "V010-POSTBUILD-CHECK-EXACT-INTEGER-TYPES",
            "V010-PHYSICAL-GATE-AUDIT-EXACT-CENSUS-ATTESTATION",
        ]
        or any(row.get("severity") != "BLOCKING" for row in failures)
        or not isinstance(disposition, dict)
        or disposition.get("v010_authorization") != "DO_NOT_AUTHORIZE_OR_BUILD"
        or disposition.get("successor")
        != "Create and freeze a distinct V011 successor; preserve V010 source, freeze, preflight, and this failure record without amendment."
        or record.get("predecessor_obstruction_custody", {}).get(
            "target_v009_hostile_audit_obstruction_sha256"
        ) != wrong_value
        or record.get("claim_boundary")
        != "HOSTILE_CONTROL_PLANE_AUDIT_FAILURE_ONLY__NO_GATE_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        or record.get("v005_v006_v007_v008_v009_bytes_preserved") is not True
        or any(value is not False for value in record.get("absence_census_at_audit", {}).values())
    ):
        raise Refusal("target V010 hostile-audit obstruction content mismatch")
    if (
        correction.get("schema") != "TARGET_V010_AUDIT_RECORD_CUSTODY_CORRECTION_V001"
        or correction.get("classification")
        != "CORRECT_V010_FAIL_RECORD_V009_OBSTRUCTION_SHA256_ONLY"
        or correction.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or correction.get("record_corrected")
        != {
            "path": "AUDIT_R_L12_TARGET_STORAGE_CACHE_V010/HOSTILE_AUDIT_OBSTRUCTION_V001.json",
            "sha256": V010_HOSTILE_OBSTRUCTION_SHA256,
        }
        or correction.get("correct_binding")
        != {
            "path": "AUDIT_R_L12_TARGET_STORAGE_CACHE_V009/HOSTILE_AUDIT_OBSTRUCTION_V001.json",
            "sha256": V009_HOSTILE_OBSTRUCTION_SHA256,
        }
        or correction.get("correction", {}).get("recorded_value") != wrong_value
        or correction.get("correction", {}).get("recorded_value_length") != 63
        or correction.get("v010_authorization") != "DO_NOT_AUTHORIZE_OR_BUILD"
        or correction.get("v010_failure_record_remains_immutable") is not True
        or any(value is not False for value in correction.get("physical_state", {}).values())
        or correction.get("claim_boundary")
        != "AUDIT_RECORD_CUSTODY_CORRECTION_ONLY__NO_PASS_GATE_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("target V010 custody correction content mismatch")
    return record, correction


def require_preflight_mutation_ledger(
    binding: object, freeze: dict[str, object], freeze_sha256: str,
) -> dict[str, object]:
    if not isinstance(binding, dict) or set(binding) != {
        "path", "sha256", "schema", "classification", "case_count",
        "positive_sink_call_count", "mutation_sink_call_count",
        "obligation_matrix_sha256", "validator_module_sha256",
    }:
        raise Refusal("V012 mutation-ledger binding malformed")
    expected_binding_identity = {
        "path": "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PREFLIGHT_MUTATION_LEDGER_V001.json",
        "schema": "TARGET_V012_PREPAYLOAD_MUTATION_LEDGER_V001",
        "classification": "PASS_EXECUTED_PREREGISTERED_MUTATION_ASSIGNMENTS",
        "case_count": 477,
        "positive_sink_call_count": 33,
        "mutation_sink_call_count": 477,
        "obligation_matrix_sha256": AUDIT_OBLIGATION_CONTRACT_SHA256[
            "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/AUDIT_OBLIGATIONS_V001.json"
        ],
        "validator_module_sha256": freeze["files"][
            "production_obligation_validators.py"
        ],
    }
    if (
        any(type(binding.get(key)) is not int for key in (
            "case_count", "positive_sink_call_count", "mutation_sink_call_count",
        ))
        or any(binding.get(key) != value for key, value in expected_binding_identity.items())
    ):
        raise Refusal("V012 mutation-ledger binding identity mismatch")
    ledger_path = safe_repo_file(
        binding["path"], binding.get("sha256"), "V012 preflight mutation ledger"
    )
    ledger, ledger_sha256 = immutable_json(
        ledger_path, "V012 preflight mutation ledger", binding.get("sha256")
    )
    matrix_path = ROOT / "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/AUDIT_OBLIGATIONS_V001.json"
    matrix, _ = immutable_json(
        matrix_path, "V012 audit obligation matrix",
        expected_binding_identity["obligation_matrix_sha256"],
    )
    artifacts = matrix.get("artifacts")
    if (
        not isinstance(artifacts, list)
        or len(artifacts) != 26
        or any(not isinstance(artifact, dict) for artifact in artifacts)
    ):
        raise Refusal("V012 mutation-ledger obligation artifacts malformed")
    expected_rows: list[tuple[str, str, str, str]] = []
    positive_ids: list[str] = []
    for artifact in artifacts:
        artifact_id = artifact.get("id")
        positive = artifact.get("positive_fixture")
        variants = artifact.get("positive_fixture_variants", [])
        mutation_fixture_map = artifact.get("mutation_fixture_by_class", {})
        mutations = artifact.get("mutation_classes")
        if (
            not isinstance(artifact_id, str)
            or not isinstance(positive, dict)
            or not isinstance(positive.get("id"), str)
            or not isinstance(variants, list)
            or any(
                not isinstance(variant, dict)
                or not isinstance(variant.get("id"), str)
                for variant in variants
            )
            or not isinstance(mutation_fixture_map, dict)
            or any(
                not isinstance(key, str) or not isinstance(value, str)
                for key, value in mutation_fixture_map.items()
            )
            or not isinstance(mutations, list)
            or any(not isinstance(item, str) for item in mutations)
        ):
            raise Refusal("V012 mutation-ledger matrix row malformed")
        fixture_ids = [positive["id"], *[variant["id"] for variant in variants]]
        if (
            len(fixture_ids) != len(set(fixture_ids))
            or not set(mutation_fixture_map).issubset(mutations)
            or not set(mutation_fixture_map.values()).issubset(fixture_ids)
        ):
            raise Refusal("V012 mutation-ledger fixture routing malformed")
        positive_ids.extend(fixture_ids)
        for mutation in mutations:
            fixture_id = mutation_fixture_map.get(mutation, positive["id"])
            expected_rows.append((
                f"MCASE_{len(expected_rows) + 1:04d}", artifact_id,
                fixture_id, mutation,
            ))
    if len(expected_rows) != 477 or len(positive_ids) != 33 or len(set(positive_ids)) != 33:
        raise Refusal("V012 mutation-ledger reconstructed matrix census mismatch")
    expected_keys = {
        "schema", "classification", "audited_packet", "sealed_input_commit",
        "obligation_matrix_path", "obligation_matrix_sha256", "freeze_sha256",
        "source_sha256", "positive_fixture_sha256_by_id",
        "mutated_fixture_sha256_by_case_id", "validator_module",
        "production_hook", "positive_sink_call_count", "mutation_sink_call_count",
        "case_count", "checks_passed", "checks_total",
        "canonical_artifact_created", "cases", "claim_boundary",
    }
    source_sha256 = freeze.get("files")
    positive_hashes = ledger.get("positive_fixture_sha256_by_id")
    mutation_hashes = ledger.get("mutated_fixture_sha256_by_case_id")
    cases = ledger.get("cases")
    if (
        set(ledger) != expected_keys
        or ledger.get("schema") != expected_binding_identity["schema"]
        or ledger.get("classification") != expected_binding_identity["classification"]
        or ledger.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or ledger.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or ledger.get("obligation_matrix_path")
        != "AUDIT_PREPARATION_R_L12_TARGET_STORAGE_CACHE_V012/AUDIT_OBLIGATIONS_V001.json"
        or ledger.get("obligation_matrix_sha256")
        != expected_binding_identity["obligation_matrix_sha256"]
        or ledger.get("freeze_sha256") != freeze_sha256
        or not exact_tree_equal(ledger.get("source_sha256"), source_sha256)
        or ledger.get("validator_module") != {
            "path": (
                "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/"
                "production_obligation_validators.py"
            ),
            "sha256": freeze["files"]["production_obligation_validators.py"],
        }
        or ledger.get("production_hook")
        != "build_target_cache.validate_audit_obligation_fixture"
        or type(ledger.get("positive_sink_call_count")) is not int
        or ledger.get("positive_sink_call_count") != 33
        or type(ledger.get("mutation_sink_call_count")) is not int
        or ledger.get("mutation_sink_call_count") != 477
        or type(ledger.get("case_count")) is not int
        or ledger.get("case_count") != 477
        or type(ledger.get("checks_passed")) is not int
        or ledger.get("checks_passed") != 477
        or type(ledger.get("checks_total")) is not int
        or ledger.get("checks_total") != 477
        or ledger.get("canonical_artifact_created") is not False
        or ledger.get("claim_boundary")
        != "EXECUTED_PRODUCTION_VALIDATOR_MUTATION_EVIDENCE_ONLY__NO_GATE_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
        or not isinstance(positive_hashes, dict)
        or set(positive_hashes) != set(positive_ids)
        or len(set(positive_hashes.values())) != 33
        or not isinstance(mutation_hashes, dict)
        or set(mutation_hashes) != {row[0] for row in expected_rows}
        or len(set(mutation_hashes.values())) != 477
        or any(
            not isinstance(value, str) or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
            for value in list(positive_hashes.values()) + list(mutation_hashes.values())
        )
        or not isinstance(cases, list)
        or len(cases) != 477
    ):
        raise Refusal("V012 mutation-ledger content/census mismatch")
    row_keys = {
        "case_id", "artifact_id", "fixture_id", "mutation_class",
        "byte_mutation", "expected_refusal", "actual_refusal",
        "positive_fixture_sha256", "mutated_fixture_sha256",
        "mutation_evidence_sha256", "production_hook", "validator_function",
        "production_sink_calls",
        "canonical_artifact_created", "passed",
    }
    try:
        import production_obligation_validators as validators
    except ImportError as error:
        raise Refusal("production obligation validator module absent") from error
    if (
        Path(getattr(validators, "__file__", "")).resolve() != PRODUCTION_VALIDATORS
        or stable_file_sha256(
            PRODUCTION_VALIDATORS, "production obligation validators",
            freeze["files"]["production_obligation_validators.py"],
            require_immutable_mode=True,
        ) != freeze["files"]["production_obligation_validators.py"]
    ):
        raise Refusal("production obligation validator module custody mismatch")
    a22_hook_by_fixture = {
        "PF_A22_TARGET_AUTH": "dual_launch_coordinator.DualLaunchCoordinator.admit_authorization",
        "PF_A22_HOSTILE_AUTH": "dual_launch_coordinator.DualLaunchCoordinator.admit_authorization",
        "PF_A22_READY": "dual_launch_coordinator.DualLaunchCoordinator.commit_handshake",
        "PF_A22_HANDSHAKE": "dual_launch_coordinator.DualLaunchCoordinator.commit_handshake",
        "PF_A22_RELEASE": "dual_launch_coordinator.DualLaunchCoordinator.release_workers",
        "PF_A22_COMMAND": "dual_launch_coordinator.DualLaunchCoordinator.admit_release_ack",
        "PF_A22_ACK": "dual_launch_coordinator.DualLaunchCoordinator.admit_release_ack",
        "PF_A22_COMPLETION": "dual_launch_coordinator.DualLaunchCoordinator.admit_worker_completion",
    }
    a22_expected_refusal = {
        "M06_BOOL_FOR_INT": "process_id must be an exact integer >= 1",
        "M07_FLOAT_INT_ALIAS": "release command process_id must be an exact integer >= 1",
        "M10_IDENTITY_OR_CLAIM": "worker release ACK schema mismatch",
        "M11_HASH_OR_PATH": "process start token must be a lowercase SHA-256",
        "M17_PROVENANCE_DROP_SWAP": "worker READY hash reconstruction mismatch",
        "M19_STAGE_BYPASS": "handshake authorizations exact key census mismatch",
        "M23_HANDSHAKE_TELEMETRY": "worker release ACK digest mismatch",
        "M24_UNLOCK_AUDIT_BINDING": "release token mismatch",
        "M30_COMPLETION_BOOL_PROCESS_ID": "worker completion process_id must be an exact integer >= 1",
        "M31_COMPLETION_FLOAT_PROCESS_ID": "worker completion process_id must be an exact integer >= 1",
        "M32_COMPLETION_SCHEMA": "worker completion schema mismatch",
        "M33_COMPLETION_OUTPUT_HASH": "worker completion output hash must be a lowercase SHA-256",
        "M34_COMPLETION_WORKER_IDENTITY": "worker completion identity mismatch",
        "M35_COMPLETION_STAGE_BYPASS": "worker completion requires both release ACKs",
        "M36_COMPLETION_EPOCH_WINDOW": "worker completion outside execution wall window",
    }
    for row, expected in zip(cases, expected_rows):
        case_id, artifact_id, fixture_id, mutation_class = expected
        custody_hook = {
            "M12_SYMLINK_OR_WRITABLE": "validate_preflight.read_strict_immutable_json",
            "M13_DESCRIPTOR_TOCTOU": "validate_preflight.validate_held_descriptor_identity",
            "M25_IMPORT_TARGET_VALIDATOR": "validate_preflight.validate_independent_auditor_source_bytes",
            "M28_PREMATURE_ARTIFACT": "validate_preflight.require_artifacts_absent",
        }.get(mutation_class)
        expected_hook = custody_hook or (
            a22_hook_by_fixture[fixture_id]
            if artifact_id == "A22_TARGET_L12_AUTHORIZATION"
            else "build_target_cache.validate_audit_obligation_fixture"
        )
        expected_validator = custody_hook or (
            a22_hook_by_fixture[fixture_id]
            if artifact_id == "A22_TARGET_L12_AUTHORIZATION"
            else validators.VALIDATOR_FUNCTION_BY_ARTIFACT[artifact_id]
        )
        expected_refusal = (
            a22_expected_refusal.get(
                mutation_class,
                validators.MUTATION_EXPECTED_REFUSAL[mutation_class],
            )
            if artifact_id == "A22_TARGET_L12_AUTHORIZATION"
            else validators.FINAL_NATIVE_MUTATION_REFUSAL.get(
                (artifact_id, mutation_class),
                validators.MUTATION_EXPECTED_REFUSAL[mutation_class],
            )
        )
        if (
            not isinstance(row, dict)
            or set(row) != row_keys
            or tuple(row.get(key) for key in (
                "case_id", "artifact_id", "fixture_id", "mutation_class"
            )) != expected
            or not isinstance(row.get("byte_mutation"), str)
            or not row["byte_mutation"]
            or row.get("expected_refusal") != expected_refusal
            or not isinstance(row.get("actual_refusal"), str)
            or not exact_refusal_match(
                row["actual_refusal"], row["expected_refusal"]
            )
            or row.get("positive_fixture_sha256") != positive_hashes[fixture_id]
            or row.get("mutated_fixture_sha256") != mutation_hashes[case_id]
            or not isinstance(row.get("mutation_evidence_sha256"), str)
            or len(row["mutation_evidence_sha256"]) != 64
            or any(character not in "0123456789abcdef"
                   for character in row["mutation_evidence_sha256"])
            or row.get("production_hook") != expected_hook
            or row.get("validator_function") != expected_validator
            or type(row.get("production_sink_calls")) is not int
            or row["production_sink_calls"] != 1
            or row.get("canonical_artifact_created") is not False
            or row.get("passed") is not True
        ):
            raise Refusal("V012 mutation-ledger ordered case reconstruction mismatch")
    if ledger_sha256 != binding["sha256"]:
        raise Refusal("V012 mutation-ledger digest binding mismatch")
    return ledger


def require_future_v012_hostile_audit(
    specification: object, freeze: dict[str, object],
    preflight_result_sha256: str | None = None,
) -> dict[str, object]:
    if not isinstance(specification, dict) or set(specification) != {"path", "sha256"}:
        raise Refusal("V012 independent hostile-audit gate specification malformed")
    if specification.get("path") != FUTURE_HOSTILE_AUDIT_PATH:
        raise Refusal("V012 independent hostile-audit path mismatch")
    path = safe_repo_file(
        specification.get("path"), specification.get("sha256"),
        "V012 independent hostile audit",
    )
    audit, _digest = immutable_json(
        path, "V012 independent hostile audit", specification.get("sha256")
    )
    expected_preflight_sha256 = (
        preflight_result_sha256
        if preflight_result_sha256 is not None
        else stable_file_sha256(
            HERE / "PREFLIGHT_RESULT_V001.json", "V012 preflight result",
            require_immutable_mode=True,
        )
    )
    preflight, _ = immutable_json(
        HERE / "PREFLIGHT_RESULT_V001.json", "V012 preflight result",
        expected_preflight_sha256,
    )
    preflight_checks = preflight.get("checks")
    if (
        not isinstance(preflight_checks, dict)
        or not preflight_checks
        or any(type(value) is not int or value <= 0
               for value in preflight_checks.values())
    ):
        raise Refusal("V012 preflight check census malformed")
    freeze_sha256 = stable_file_sha256(
        FREEZE, "V012 freeze", require_immutable_mode=True
    )
    mutation_binding = preflight.get("mutation_ledger")
    require_preflight_mutation_ledger(mutation_binding, freeze, freeze_sha256)
    expected_checks = {
        "frozen_source_files": 5,
        "sealed_dependency_files": 44,
        "v011_exact_type_repairs": 6,
        "audit_obligation_artifacts": 26,
        "audit_obligation_positive_fixtures": 33,
        "audit_obligation_mutation_classes": 36,
        "audit_obligation_mutation_assignments": 477,
        "authorization_dag_states": 262144,
        "preflight_checks_replayed": sum(preflight_checks.values()),
        "absence_census_records": len(FUTURE_PREPAYLOAD_ABSENCE_CENSUS),
    }
    required_keys = {
        "schema", "classification", "auditor_role", "audited_packet",
        "sealed_input_commit", "audited_freeze_sha256", "audited_files_sha256",
        "preflight_result_sha256", "checks", "checks_passed", "checks_total", "failures",
        "mutation_ledger",
        "no_symlinked_inputs", "v005_v006_v007_v008_v009_v010_v011_bytes_preserved", "absence_census",
        "payload_or_history_executed", "claim_boundary",
    }
    if set(audit) != required_keys:
        raise Refusal("V012 independent hostile-audit key census mismatch")
    if (
        audit.get("schema") != FUTURE_HOSTILE_AUDIT_SCHEMA
        or audit.get("classification") != FUTURE_HOSTILE_AUDIT_CLASSIFICATION
        or audit.get("auditor_role") != "INDEPENDENT_HOSTILE_READ_ONLY_REVIEW"
        or audit.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
        or audit.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or audit.get("audited_freeze_sha256") != freeze_sha256
        or audit.get("audited_files_sha256") != freeze["files"]
        or audit.get("preflight_result_sha256") != expected_preflight_sha256
        or not exact_tree_equal(audit.get("mutation_ledger"), mutation_binding)
        or audit.get("checks") != expected_checks
        or any(type(value) is not int or value <= 0
               for value in audit["checks"].values())
        or type(audit.get("checks_total")) is not int
        or audit["checks_total"] != sum(audit["checks"].values())
        or type(audit.get("checks_passed")) is not int
        or audit.get("checks_passed") != audit["checks_total"]
        or audit.get("failures") != []
        or audit.get("no_symlinked_inputs") is not True
        or audit.get("v005_v006_v007_v008_v009_v010_v011_bytes_preserved") is not True
        or not isinstance(audit.get("absence_census"), dict)
        or any(type(value) is not bool or value is not False
               for value in audit["absence_census"].values())
        or audit["absence_census"] != FUTURE_PREPAYLOAD_ABSENCE_CENSUS
        or audit.get("payload_or_history_executed") is not False
        or audit.get("claim_boundary")
        != "V012_PREPAYLOAD_CONTROL_PLANE_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("V012 independent hostile-audit content mismatch")
    validate_production_obligation("A03_PREPAYLOAD_AUDIT", audit)
    return audit


def require_v011_hostile_audit_obstruction() -> dict[str, object]:
    for relative, digest in V011_CUSTODY_SHA256.items():
        safe_repo_file(relative, digest, "target V011 obstruction parent")
    record, _ = immutable_json(
        V011_HOSTILE_OBSTRUCTION, "target V011 hostile-audit obstruction",
        V011_HOSTILE_OBSTRUCTION_SHA256,
    )
    expected_files = {
        Path(relative).name: digest
        for relative, digest in V011_CUSTODY_SHA256.items()
        if relative.startswith("DEVELOPMENT_")
        and Path(relative).name in {
            "METHOD.md", "build_target_cache.py", "consume_target_cache.py",
            "validate_preflight.py",
        }
    }
    if (
        not isinstance(record, dict)
        or record.get("schema") != "TARGET_V011_HOSTILE_AUDIT_OBSTRUCTION_V001"
        or record.get("classification")
        != "FAIL_EXACT_RECORD_TYPES_REMAIN_UNENFORCED_ACROSS_AUDIT_AND_OUTER_AUTHORIZATION_RECORDS"
        or record.get("resolved") is not False
        or record.get("auditor_role") != "INDEPENDENT_HOSTILE_READ_ONLY_REVIEW"
        or record.get("audited_packet") != "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V011"
        or record.get("sealed_input_commit") != "42f1ea3301ccf98802c07f3330d52999385cba0b"
        or record.get("audited_freeze_sha256")
        != V011_CUSTODY_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V011/FREEZE.json"]
        or record.get("preflight_result_sha256")
        != V011_CUSTODY_SHA256["DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V011/PREFLIGHT_RESULT_V001.json"]
        or record.get("audited_files_sha256") != expected_files
        or record.get("preflight_replay", {}).get("checks_total") != 292
        or record.get("preflight_replay", {}).get("checks_passed") != 292
        or record.get("adversarial_summary", {}).get("checks_attempted") != 48
        or record.get("adversarial_summary", {}).get("checks_passed") != 32
        or record.get("adversarial_summary", {}).get("checks_failed") != 16
        or [row.get("id") for row in record.get("failures", []) if isinstance(row, dict)]
        != [
            "V011-PREPAYLOAD-AUDIT-CHECKS-PASSED-EXACT-TYPE",
            "V011-POSTBUILD-AUDIT-CHECKS-PASSED-EXACT-TYPE",
            "V011-PHYSICAL-GATE-AUDIT-CHECKS-PASSED-EXACT-TYPE",
            "V011-POSTBUILD-NESTED-CENSUS-EXACT-TYPES",
            "V011-PREPAYLOAD-ABSENCE-CENSUS-EXACT-BOOLEANS",
            "V011-OUTER-AUTHORIZED-LENGTHS-EXACT-INTEGERS",
        ]
        or any(row.get("severity") != "BLOCKING" for row in record.get("failures", []))
        or record.get("required_disposition")
        != {
            "successor": "Create and freeze a distinct V012 successor; preserve V011 source, freeze, preflight, and this failure record without amendment.",
            "v011_authorization": "DO_NOT_AUTHORIZE_OR_BUILD",
        }
        or record.get("v005_v006_v007_v008_v009_v010_bytes_preserved") is not True
        or record.get("no_symlinked_inputs") is not True
        or record.get("payload_or_history_executed") is not False
        or any(type(value) is not bool or value is not False
               for value in record.get("absence_census_at_audit", {}).values())
        or record.get("claim_boundary")
        != "HOSTILE_CONTROL_PLANE_AUDIT_FAILURE_ONLY__NO_GATE_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY_RESULT"
    ):
        raise Refusal("target V011 hostile-audit obstruction content mismatch")
    return record


def validate_obstruction_rows(rows: object) -> list[dict[str, object]]:
    if (
        not isinstance(rows, list)
        or len(rows) != 2
        or any(not isinstance(row, dict) for row in rows)
        or [row.get("role") for row in rows] != ["target", "hostile"]
    ):
        raise Refusal("exact ordered target/hostile obstruction pair absent")
    expected = {
        "target": (TARGET_V004_SHA256, TARGET_METHOD_V004_SHA256, TARGET_FREEZE_V004_SHA256),
        "hostile": (HOSTILE_V003_SHA256, HOSTILE_METHOD_V003_SHA256, HOSTILE_FREEZE_V003_SHA256),
    }
    custody_paths: set[Path] = set()
    custody_digests: set[str] = set()
    records: list[dict[str, object]] = []
    for row in rows:
        if set(row) != {"role", "path", "sha256"}:
            raise Refusal("obstruction gate row schema mismatch")
        role = row["role"]
        record_path = safe_repo_file(row.get("path"), row.get("sha256"), f"{role} obstruction")
        if record_path in custody_paths or row["sha256"] in custody_digests:
            raise Refusal("obstruction/evidence paths or hashes are not globally distinct")
        custody_paths.add(record_path)
        custody_digests.add(row["sha256"])
        record, _ = immutable_json(
            record_path, f"{role} obstruction record", row["sha256"],
            require_immutable_mode=False,
        )
        implementation_sha256, method_sha256, freeze_sha256 = expected[role]
        if (
            record.get("schema") != "L12_SIX_HOUR_RESOURCE_OBSTRUCTION_V005"
            or record.get("classification") != "SIX_HOUR_RESOURCE_OBSTRUCTION"
            or record.get("L") != 12
            or record.get("role") != role
            or record.get("resolved") is not False
            or record.get("physical_output_created") is not False
        ):
            raise Refusal("current execution did not record a six-hour obstruction")
        if (
            not exact_int(record.get("wall_limit_seconds"))
            or record["wall_limit_seconds"] != int(HISTORICAL_OBSTRUCTION_WALL_LIMIT)
        ):
            raise Refusal("obstruction changed frozen wall limit")
        wall = record.get("wall_seconds")
        if (
            type(wall) not in (int, float)
            or not math.isfinite(float(wall))
            or float(wall) < HISTORICAL_OBSTRUCTION_WALL_LIMIT
        ):
            raise Refusal("obstruction did not reach the frozen wall limit")
        if (
            record.get("implementation_sha256") != implementation_sha256
            or record.get("method_sha256") != method_sha256
            or record.get("freeze_sha256") != freeze_sha256
        ):
            raise Refusal("obstruction implementation/method/freeze custody mismatch")
        for evidence_key in ("execution_log", "monitor_evidence"):
            evidence = record.get(evidence_key)
            if not isinstance(evidence, dict) or set(evidence) != {"path", "sha256"}:
                raise Refusal(f"obstruction {evidence_key} record mismatch")
            evidence_path = safe_repo_file(
                evidence.get("path"), evidence.get("sha256"), f"{role} {evidence_key}"
            )
            evidence_digest = evidence["sha256"]
            if evidence_path in custody_paths or evidence_digest in custody_digests:
                raise Refusal("obstruction/evidence paths or hashes are not globally distinct")
            custody_paths.add(evidence_path)
            custody_digests.add(evidence_digest)
            if evidence_key == "monitor_evidence":
                monitor, _ = immutable_json(
                    evidence_path, f"{role} wall-monitor evidence",
                    evidence_digest, require_immutable_mode=False,
                )
                monitor_wall = monitor.get("observed_wall_seconds")
                if (
                    monitor.get("schema") != "L12_WALL_MONITOR_EVIDENCE_V005"
                    or monitor.get("L") != 12
                    or monitor.get("role") != role
                    or monitor.get("implementation_sha256") != implementation_sha256
                    or monitor.get("wall_limit_seconds")
                    != int(HISTORICAL_OBSTRUCTION_WALL_LIMIT)
                    or type(monitor_wall) not in (int, float)
                    or not math.isfinite(float(monitor_wall))
                    or float(monitor_wall) < HISTORICAL_OBSTRUCTION_WALL_LIMIT
                    or monitor.get("termination_reason") != "WALL_LIMIT_REACHED"
                    or monitor.get("physical_output_created") is not False
                    or monitor.get("workspace_preserved") is not True
                ):
                    raise Refusal("independent wall-monitor evidence mismatch")
        records.append(record)
    if len(custody_paths) != 6 or len(custody_digests) != 6:
        raise Refusal("six globally distinct obstruction/evidence records absent")
    return records


def require_dual_gate(length: int) -> dict[str, object]:
    freeze = require_frozen_census()
    if DUAL_GATE.is_symlink() or not DUAL_GATE.is_file():
        raise Refusal("cache payload locked: V012 dual obstruction/compatibility gate is absent")
    gate, _digest = immutable_json(DUAL_GATE, "V012 dual authorization gate")
    return validate_dual_gate_document(gate, length, freeze)


def validate_dual_gate_document(
    gate: object, length: int, freeze: dict[str, object],
    preflight_result_sha256: str | None = None,
) -> dict[str, object]:
    if not isinstance(gate, dict):
        raise Refusal("cache payload locked: V012 dual gate is not an object")
    required_keys = {
        "schema", "classification", "method_sha256", "builder_sha256",
        "consumer_sha256", "preflight_sha256", "freeze_sha256",
        "target_v004_sha256", "hostile_v003_sha256",
        "preserved_workspace_custody_sha256",
        "preserved_workspace_cross_diagnostic_sha256",
        "runtime_compatibility_obstruction_sha256", "superseded_v005_dual_gate_sha256",
        "superseded_v005_cache_manifest_sha256_by_L", "authorized_cache_lengths",
        "v006_hostile_audit_obstruction_sha256", "preflight_result_sha256",
        "v007_runtime_compatibility_obstruction_sha256",
        "superseded_v007_dual_gate_sha256",
        "superseded_v007_cache_manifest_sha256_by_L",
        "v008_postbuild_audit_binding_obstruction_sha256",
        "superseded_v008_dual_gate_sha256",
        "superseded_v008_cache_manifest_sha256_by_L",
        "v009_hostile_audit_obstruction_sha256",
        "v010_hostile_audit_obstruction_sha256",
        "v010_audit_record_custody_correction_sha256",
        "v011_hostile_audit_obstruction_sha256",
        "independent_hostile_audit", "obstructions", "claim_boundary",
    }
    if set(gate) != required_keys:
        raise Refusal("cache payload locked: V012 dual gate key census mismatch")
    if gate.get("schema") != "TARGET_V012_DUAL_OBSTRUCTION_AND_COMPATIBILITY_GATE" or gate.get("classification") != "AUTHORIZE_TARGET_V012_FRESH_CACHE_AFTER_V005_V006_V007_V008_V009_V010_AND_V011_CONTROL_PLANE_OBSTRUCTIONS":
        raise Refusal("cache payload locked: dual obstruction classification absent")
    required = {
        "method_sha256": freeze["files"]["METHOD.md"],
        "builder_sha256": freeze["files"]["build_target_cache.py"],
        "consumer_sha256": freeze["files"]["consume_target_cache.py"],
        "preflight_sha256": freeze["files"]["validate_preflight.py"],
        "freeze_sha256": stable_file_sha256(FREEZE, "V012 freeze"),
        "target_v004_sha256": TARGET_V004_SHA256,
        "hostile_v003_sha256": HOSTILE_V003_SHA256,
        "preserved_workspace_custody_sha256": PRESERVED_WORKSPACE_CUSTODY_SHA256,
        "preserved_workspace_cross_diagnostic_sha256": PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_SHA256,
        "runtime_compatibility_obstruction_sha256": RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256,
        "superseded_v005_dual_gate_sha256": V005_DUAL_GATE_SHA256,
        "v006_hostile_audit_obstruction_sha256": V006_HOSTILE_OBSTRUCTION_SHA256,
        "v007_runtime_compatibility_obstruction_sha256": V007_RUNTIME_OBSTRUCTION_SHA256,
        "v008_postbuild_audit_binding_obstruction_sha256": V008_BINDING_OBSTRUCTION_SHA256,
        "v009_hostile_audit_obstruction_sha256": V009_HOSTILE_OBSTRUCTION_SHA256,
        "v010_hostile_audit_obstruction_sha256": V010_HOSTILE_OBSTRUCTION_SHA256,
        "v010_audit_record_custody_correction_sha256": V010_CUSTODY_CORRECTION_SHA256,
        "v011_hostile_audit_obstruction_sha256": V011_HOSTILE_OBSTRUCTION_SHA256,
        "superseded_v007_dual_gate_sha256": V007_DUAL_GATE_SHA256,
        "superseded_v008_dual_gate_sha256": V008_DUAL_GATE_SHA256,
        "preflight_result_sha256": (
            preflight_result_sha256
            if preflight_result_sha256 is not None
            else stable_file_sha256(
                HERE / "PREFLIGHT_RESULT_V001.json", "V012 preflight result"
            )
        ),
    }
    for key, expected in required.items():
        if gate.get(key) != expected:
            raise Refusal(f"dual obstruction gate does not pin {key}")
    if gate.get("superseded_v005_cache_manifest_sha256_by_L") != V005_CACHE_MANIFEST_SHA256:
        raise Refusal("dual obstruction gate does not pin superseded V005 cache manifests")
    if gate.get("superseded_v007_cache_manifest_sha256_by_L") != V007_CACHE_MANIFEST_SHA256:
        raise Refusal("dual obstruction gate does not pin superseded V007 cache manifests")
    if gate.get("superseded_v008_cache_manifest_sha256_by_L") != V008_CACHE_MANIFEST_SHA256:
        raise Refusal("dual obstruction gate does not pin superseded V008 cache manifests")
    if gate.get("claim_boundary") != "CONTROL_PLANE_AUTHORIZATION_ONLY__NO_CACHE_HISTORY_OR_PHYSICS_RESULT":
        raise Refusal("dual obstruction gate claim boundary mismatch")
    authorized = gate.get("authorized_cache_lengths")
    if (
        not isinstance(authorized, list)
        or not authorized
        or any(type(value) is not int for value in authorized)
        or authorized != sorted(set(authorized))
        or any(value not in SUPPORTED for value in authorized)
        or length not in authorized
    ):
        raise Refusal("dual obstruction gate does not authorize cache size")
    validate_obstruction_rows(gate.get("obstructions"))
    require_preserved_workspace_custody()
    require_preserved_workspace_cross_diagnostic()
    require_runtime_compatibility_obstruction()
    require_v006_hostile_audit_obstruction()
    require_v007_runtime_compatibility_obstruction()
    require_v008_postbuild_binding_obstruction()
    require_v009_hostile_audit_obstruction()
    require_v010_hostile_audit_obstruction_and_correction()
    require_v011_hostile_audit_obstruction()
    require_future_v012_hostile_audit(
        gate.get("independent_hostile_audit"), freeze, preflight_result_sha256
    )
    validate_production_obligation("A04_UNIVERSAL_CUSTODY_GATE", gate)
    return gate


def exact_operator_arrays(length: int, q: int, edges: list[tuple[int, int, str]]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    words = carrier_words(length, q)
    if len(words) != math.comb(2 * length, q):
        raise AssertionError("carrier basis census")
    if len(set(map(int, words))) != len(words) or any(bin(int(word)).count("1") != q for word in words):
        raise AssertionError("carrier basis identity")
    reference = np.asarray(v004.sealed.fixed_words(2 * length, q), dtype=WORD_DTYPE)
    if not np.array_equal(words, reference):
        raise AssertionError("target fixed_words order changed")
    lookup = {int(word): index for index, word in enumerate(words)}
    offsets = [0]
    sources: list[np.ndarray] = []
    targets: list[np.ndarray] = []
    for u, v, _label in edges:
        source = np.flatnonzero((((words >> u) & 1) == 1) & (((words >> v) & 1) == 0)).astype(INDEX_DTYPE)
        expected = math.comb(2 * length - 2, q - 1) if q else 0
        if len(source) != expected:
            raise AssertionError("oriented exchange census")
        toggle = (1 << u) | (1 << v)
        target = np.fromiter(
            (lookup[int(words[int(index)]) ^ toggle] for index in source),
            dtype=INDEX_DTYPE,
            count=len(source),
        )
        if len(np.unique(source)) != len(source) or len(np.unique(target)) != len(target):
            raise AssertionError("exchange rank injectivity")
        if any(int(words[int(right)]) != (int(words[int(left)]) ^ toggle) for left, right in zip(source, target)):
            raise AssertionError("exchange XOR identity")
        sources.append(source)
        targets.append(target)
        offsets.append(offsets[-1] + len(source))
    return (
        words,
        np.asarray(offsets, dtype=OFFSET_DTYPE),
        np.concatenate(sources) if sources else np.empty(0, dtype=INDEX_DTYPE),
        np.concatenate(targets) if targets else np.empty(0, dtype=INDEX_DTYPE),
    )


def exact_admission_arrays(length: int, event: int, q: int, old_words: np.ndarray, next_words: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    blank = np.flatnonzero(((old_words >> event) & 1) == 0).astype(INDEX_DTYPE)
    expected = math.comb(2 * length - 1, q)
    if len(blank) != expected:
        raise AssertionError("admission blank-column census")
    lookup = {int(word): index for index, word in enumerate(next_words)}
    destination = np.fromiter(
        (lookup[int(old_words[int(index)]) | (1 << event)] for index in blank),
        dtype=INDEX_DTYPE,
        count=len(blank),
    )
    if len(np.unique(destination)) != len(destination):
        raise AssertionError("admission destination injectivity")
    if any(int(next_words[int(right)]) != (int(old_words[int(left)]) | (1 << event)) for left, right in zip(blank, destination)):
        raise AssertionError("admission exact add-event identity")
    return blank, destination


def exact_lineage_maps(prefix: int, q: int, old_words: np.ndarray, same_words: np.ndarray, added_words: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    same_lookup = {int(word): index for index, word in enumerate(same_words)}
    added_lookup = {int(word): index for index, word in enumerate(added_words)}
    stay = np.fromiter((same_lookup[int(word)] for word in old_words), dtype=INDEX_DTYPE, count=len(old_words))
    accepted = np.fromiter(
        (added_lookup[int(word) | (1 << prefix)] for word in old_words),
        dtype=INDEX_DTYPE,
        count=len(old_words),
    )
    if len(np.unique(stay)) != len(stay) or len(np.unique(accepted)) != len(accepted):
        raise AssertionError("lineage maps are not injective")
    if any(int(same_words[int(rank)]) != int(word) for word, rank in zip(old_words, stay)):
        raise AssertionError("lineage stay identity")
    if any(int(added_words[int(rank)]) != (int(word) | (1 << prefix)) for word, rank in zip(old_words, accepted)):
        raise AssertionError("lineage accepted identity")
    return stay, accepted


def verify_directory_binding(path: Path, descriptor: int, label: str) -> None:
    """Bind a canonical directory name to one retained directory descriptor."""
    canonical = os.path.abspath(os.fspath(path))
    StableAuthorityCustody._require_canonical_path(canonical, label)
    try:
        held = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
    except OSError as error:
        raise Refusal(f"{label} directory binding disappeared") from error
    if (
        not stat.S_ISDIR(held.st_mode)
        or not stat.S_ISDIR(named.st_mode)
        or (held.st_dev, held.st_ino) != (named.st_dev, named.st_ino)
    ):
        raise Refusal(f"{label} path/descriptor identity mismatch")


def open_cache_output_roots(output: Path) -> tuple[int, int, int]:
    """Create and retain the exact packet-local cache root without path races."""
    expected_output = CACHE_PARENT / output.name
    if (
        os.path.abspath(os.fspath(output))
        != os.path.abspath(os.fspath(expected_output))
        or output.name not in {f"L{length}" for length in SUPPORTED}
    ):
        raise Refusal("cache payload path must be packet-local canonical L directory")
    directory_flags = (
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    StableAuthorityCustody._require_canonical_path(
        os.path.abspath(os.fspath(HERE)), "target cache packet root",
    )
    packet_descriptor = os.open(HERE, directory_flags)
    cache_parent_descriptor: int | None = None
    output_descriptor: int | None = None
    try:
        verify_directory_binding(HERE, packet_descriptor, "target cache packet root")
        try:
            cache_parent_metadata = os.stat(
                CACHE_PARENT.name, dir_fd=packet_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            os.mkdir(CACHE_PARENT.name, mode=0o755, dir_fd=packet_descriptor)
            os.fsync(packet_descriptor)
            cache_parent_metadata = os.stat(
                CACHE_PARENT.name, dir_fd=packet_descriptor,
                follow_symlinks=False,
            )
        if not stat.S_ISDIR(cache_parent_metadata.st_mode):
            raise Refusal("cache parent is not a packet-local ordinary directory")
        cache_parent_descriptor = os.open(
            CACHE_PARENT.name, directory_flags, dir_fd=packet_descriptor,
        )
        opened_cache_parent = os.fstat(cache_parent_descriptor)
        if (
            (opened_cache_parent.st_dev, opened_cache_parent.st_ino)
            != (cache_parent_metadata.st_dev, cache_parent_metadata.st_ino)
        ):
            raise Refusal("target cache parent changed while being retained")
        verify_directory_binding(
            CACHE_PARENT, cache_parent_descriptor, "target cache parent",
        )
        try:
            os.stat(output.name, dir_fd=cache_parent_descriptor,
                    follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise Refusal("refuse overwrite target cache payload")
        os.mkdir(output.name, mode=0o755, dir_fd=cache_parent_descriptor)
        os.fsync(cache_parent_descriptor)
        created_output = os.stat(
            output.name, dir_fd=cache_parent_descriptor,
            follow_symlinks=False,
        )
        output_descriptor = os.open(
            output.name, directory_flags, dir_fd=cache_parent_descriptor,
        )
        opened_output = os.fstat(output_descriptor)
        if (
            not stat.S_ISDIR(created_output.st_mode)
            or (opened_output.st_dev, opened_output.st_ino)
            != (created_output.st_dev, created_output.st_ino)
        ):
            raise Refusal("target cache output changed while being retained")
        verify_directory_binding(output, output_descriptor, "target cache output")
        return packet_descriptor, cache_parent_descriptor, output_descriptor
    except BaseException:
        if output_descriptor is not None:
            os.close(output_descriptor)
        if cache_parent_descriptor is not None:
            os.close(cache_parent_descriptor)
        os.close(packet_descriptor)
        raise


def raw_write(
    parent_descriptor: int, name: str, array: np.ndarray,
    metadata: dict[str, object],
) -> tuple[dict[str, object], int, tuple[int, int, int, int, int, int, int]]:
    try:
        os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except FileNotFoundError:
        pass
    else:
        raise Refusal(f"refuse overwrite cache member: {name}")
    normalized = np.ascontiguousarray(array)
    flags = (
        os.O_RDWR | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(name, flags, 0o400, dir_fd=parent_descriptor)
    try:
        raw = normalized.tobytes(order="C")
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                raise OSError(f"cache member {name} write made no progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        observed = os.fstat(descriptor)
        named = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        digest = hashlib.sha256(raw).hexdigest()
        identity = (
            observed.st_dev, observed.st_ino, observed.st_size,
            observed.st_mtime_ns, observed.st_ctime_ns, observed.st_nlink,
            stat.S_IMODE(observed.st_mode),
        )
        named_identity = (
            named.st_dev, named.st_ino, named.st_size,
            named.st_mtime_ns, named.st_ctime_ns, named.st_nlink,
            stat.S_IMODE(named.st_mode),
        )
        if (
            not stat.S_ISREG(observed.st_mode)
            or observed.st_mode & 0o222
            or observed.st_nlink != 1
            or named_identity != identity
            or observed.st_size != len(raw)
            or sha256_descriptor(descriptor) != digest
        ):
            raise Refusal(f"cache member {name} descriptor authentication failed")
    except BaseException:
        os.close(descriptor)
        raise
    record = {
        "path": name,
        "dtype": normalized.dtype.str,
        "shape": list(normalized.shape),
        "bytes": observed.st_size,
        "sha256": digest,
    }
    record.update(metadata)
    return record, descriptor, identity


def guard_builder(started: float) -> None:
    if rss_bytes() > BUILDER_RSS_LIMIT:
        raise MemoryError("cache builder RSS guard exceeded")
    if time.monotonic() - started > WALL_LIMIT:
        raise TimeoutError("cache builder wall guard exceeded")


def build(length: int, output: Path) -> None:
    global AUTHORITY_CUSTODY
    if AUTHORITY_CUSTODY is not None:
        raise Refusal("nested builder authority-custody session")
    session = StableAuthorityCustody()
    held_cache_descriptors: list[int] = []
    AUTHORITY_CUSTODY = session
    try:
        _build_with_custody(length, output, held_cache_descriptors)
    finally:
        for descriptor in reversed(held_cache_descriptors):
            os.close(descriptor)
        session.close()
        AUTHORITY_CUSTODY = None


def _build_with_custody(
    length: int, output: Path, held_cache_descriptors: list[int],
) -> None:
    if length not in SUPPORTED:
        raise Refusal("unsupported cache length")
    require_original_target_gate()
    authorization = require_dual_gate(length)
    expected_output = CACHE_PARENT / f"L{length}"
    if (
        os.path.abspath(os.fspath(output))
        != os.path.abspath(os.fspath(expected_output))
    ):
        raise Refusal("cache payload path must be packet-local canonical L directory")
    required = payload_bytes(length) + maximum_state_file_bytes(length) + OVERHEAD_RESERVE
    if required >= SCRATCH_LIMIT:
        raise Refusal("exact state/cache certificate exceeds scratch limit")
    if maximum_cache_window_bytes(length) > MAPPED_CACHE_LIMIT:
        raise Refusal("one-q cache window exceeds mapped-cache limit")
    if shutil.disk_usage(HERE).free < required:
        raise Refusal("free scratch is below exact state/cache certificate")
    custody = {
        TARGET_V004: TARGET_V004_SHA256,
        HOSTILE_V003: HOSTILE_V003_SHA256,
        TARGET_METHOD_V004: TARGET_METHOD_V004_SHA256,
        TARGET_FREEZE_V004: TARGET_FREEZE_V004_SHA256,
        HOSTILE_METHOD_V003: HOSTILE_METHOD_V003_SHA256,
        HOSTILE_FREEZE_V003: HOSTILE_FREEZE_V003_SHA256,
        TARGET_L12_GATE_V004: TARGET_L12_GATE_V004_SHA256,
        PRESERVED_WORKSPACE_CUSTODY: PRESERVED_WORKSPACE_CUSTODY_SHA256,
        PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC: PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_SHA256,
        RUNTIME_COMPATIBILITY_OBSTRUCTION: RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256,
    }
    for path, expected in custody.items():
        stable_file_sha256(
            path, f"retained build authority {path.name}", expected,
            require_immutable_mode=False,
        )
    packet_descriptor, cache_parent_descriptor, output_descriptor = (
        open_cache_output_roots(output)
    )
    held_cache_descriptors.extend(
        (packet_descriptor, cache_parent_descriptor, output_descriptor)
    )
    started = time.monotonic()
    files: list[dict[str, object]] = []
    member_descriptors: list[int] = []
    member_identities: list[tuple[int, int, int, int, int, int, int]] = []
    edges = v004.sealed.graph(length)
    words_by_q: dict[int, np.ndarray] = {}
    measured_operator = 0
    measured_admission = 0
    measured_lineage_masks = 0
    measured_lineage_maps = 0
    for q in range(length + 1):
        words, offsets, sources, targets = exact_operator_arrays(length, q, edges)
        words_by_q[q] = words
        for role, suffix, array in (
            ("words", "words.u32", words),
            ("offsets", "offsets.u64", offsets),
            ("sources", "sources.i32", sources),
            ("targets", "targets.i32", targets),
        ):
            record, descriptor, identity = raw_write(
                output_descriptor, f"carrier_q_{q:02d}_{suffix}", array,
                {"kind": "operator", "q": q, "role": role},
            )
            held_cache_descriptors.append(descriptor)
            member_descriptors.append(descriptor)
            member_identities.append(identity)
            files.append(record)
            measured_operator += int(record["bytes"])
        guard_builder(started)
    for event in range(length):
        for q in range(event + 1):
            blank, destination = exact_admission_arrays(length, event, q, words_by_q[q], words_by_q[q + 1])
            for role, array in (("blank", blank), ("destination", destination)):
                record, descriptor, identity = raw_write(
                    output_descriptor,
                    f"admission_n_{event:02d}_q_{q:02d}_{role}.i32", array,
                    {"kind": "admission", "event": event, "q": q, "role": role},
                )
                held_cache_descriptors.append(descriptor)
                member_descriptors.append(descriptor)
                member_identities.append(identity)
                files.append(record)
                measured_admission += int(record["bytes"])
        guard_builder(started)
    lineage_by_key: dict[tuple[int, int], np.ndarray] = {}
    for prefix in range(length):
        for q in range(prefix + 1):
            words = lineage_words(prefix, q)
            lineage_by_key[(prefix, q)] = words
            record, descriptor, identity = raw_write(
                output_descriptor,
                f"lineage_n_{prefix:02d}_q_{q:02d}_words.u32", words,
                {"kind": "lineage_mask", "prefix": prefix, "q": q, "role": "words"},
            )
            held_cache_descriptors.append(descriptor)
            member_descriptors.append(descriptor)
            member_identities.append(identity)
            files.append(record)
            measured_lineage_masks += int(record["bytes"])
    for prefix in range(length - 1):
        for q in range(prefix + 1):
            stay, accepted = exact_lineage_maps(
                prefix,
                q,
                lineage_by_key[(prefix, q)],
                lineage_by_key[(prefix + 1, q)],
                lineage_by_key[(prefix + 1, q + 1)],
            )
            for role, array in (("stay", stay), ("accepted", accepted)):
                record, descriptor, identity = raw_write(
                    output_descriptor,
                    f"lineage_n_{prefix:02d}_q_{q:02d}_{role}.i32", array,
                    {"kind": "lineage_map", "prefix": prefix, "q": q, "role": role},
                )
                held_cache_descriptors.append(descriptor)
                member_descriptors.append(descriptor)
                member_identities.append(identity)
                files.append(record)
                measured_lineage_maps += int(record["bytes"])
        guard_builder(started)
    measured = measured_operator + measured_admission + measured_lineage_masks + measured_lineage_maps
    expected = payload_bytes(length)
    if (
        measured_operator != operator_bytes(length)
        or measured_admission != admission_bytes(length)
        or measured_lineage_masks != lineage_mask_bytes(length)
        or measured_lineage_maps != lineage_map_bytes(length)
        or measured != expected
        or len(files) != expected_file_count(length)
    ):
        raise AssertionError("cache file/byte census mismatch")
    if AUTHORITY_CUSTODY is None:
        raise AssertionError("builder authority custody unexpectedly absent")
    AUTHORITY_CUSTODY.verify_all()
    authenticated_hashes = {
        "builder": AUTHORITY_CUSTODY.digest(Path(__file__), "V012 builder"),
        "consumer": AUTHORITY_CUSTODY.digest(CONSUMER, "V012 consumer"),
        "preflight": AUTHORITY_CUSTODY.digest(PREFLIGHT, "V012 preflight"),
        "production_validators": AUTHORITY_CUSTODY.digest(
            PRODUCTION_VALIDATORS, "V012 production obligation validators"
        ),
        "method": AUTHORITY_CUSTODY.digest(METHOD, "V012 method"),
        "freeze": AUTHORITY_CUSTODY.digest(FREEZE, "V012 freeze"),
        "dual_gate": AUTHORITY_CUSTODY.digest(DUAL_GATE, "V012 dual gate"),
        "preflight_result": AUTHORITY_CUSTODY.digest(
            HERE / "PREFLIGHT_RESULT_V001.json", "V012 preflight result"
        ),
    }
    manifest = {
        "schema": "TARGET_PREFIX_HISTORY_STORAGE_CACHE_V012",
        "status": "COMPLETE_HASH_PINNED_TARGET_STORAGE_ONLY_CACHE",
        "L": length,
        "basis_order": "TARGET_FIXED_WORDS_LEXICOGRAPHIC_COMBINATION_ORDER",
        "lineage_identity": "FULL_CANONICAL_MASK",
        "edge_layout": [list(edge) for edge in edges],
        "hamiltonian_exchange_coefficient": -1,
        "files": files,
        "payload": {
            "operator_bytes": measured_operator,
            "admission_bytes": measured_admission,
            "lineage_mask_bytes": measured_lineage_masks,
            "lineage_map_bytes": measured_lineage_maps,
            "total_bytes": measured,
            "file_count": len(files),
        },
        "resource_certificates": {
            "maximum_live_state_bytes": maximum_state_file_bytes(length),
            "state_plus_cache_bytes": maximum_state_file_bytes(length) + measured,
            "overhead_reserve_bytes": OVERHEAD_RESERVE,
            "maximum_cache_window_bytes": maximum_cache_window_bytes(length),
            "terminal_cache_peak_bytes": terminal_cache_peak_bytes(length),
            "authentication_cache_peak_bytes": authentication_cache_peak_bytes(length),
            "mapped_cache_limit_bytes": MAPPED_CACHE_LIMIT,
            "scratch_limit_bytes": SCRATCH_LIMIT,
            "builder_rss_limit_bytes": BUILDER_RSS_LIMIT,
            "consumer_rss_limit_bytes": v004.RSS_LIMIT,
            "wall_limit_seconds": WALL_LIMIT,
        },
        "builder_sha256": authenticated_hashes["builder"],
        "consumer_sha256": authenticated_hashes["consumer"],
        "preflight_sha256": authenticated_hashes["preflight"],
        "production_obligation_validators_sha256": authenticated_hashes[
            "production_validators"
        ],
        "method_sha256": authenticated_hashes["method"],
        "freeze_sha256": authenticated_hashes["freeze"],
        "dual_obstruction_gate_sha256": authenticated_hashes["dual_gate"],
        "target_v004_sha256": TARGET_V004_SHA256,
        "target_v004_original_l12_gate_sha256": TARGET_L12_GATE_V004_SHA256,
        "hostile_v003_sha256": HOSTILE_V003_SHA256,
        "target_v004_method_sha256": TARGET_METHOD_V004_SHA256,
        "target_v004_freeze_sha256": TARGET_FREEZE_V004_SHA256,
        "hostile_v003_method_sha256": HOSTILE_METHOD_V003_SHA256,
        "hostile_v003_freeze_sha256": HOSTILE_FREEZE_V003_SHA256,
        "preserved_workspace_custody_sha256": PRESERVED_WORKSPACE_CUSTODY_SHA256,
        "preserved_workspace_cross_diagnostic_sha256": PRESERVED_WORKSPACE_CROSS_DIAGNOSTIC_SHA256,
        "runtime_compatibility_obstruction_sha256": RUNTIME_COMPATIBILITY_OBSTRUCTION_SHA256,
        "v006_hostile_audit_obstruction_sha256": V006_HOSTILE_OBSTRUCTION_SHA256,
        "v007_runtime_compatibility_obstruction_sha256": V007_RUNTIME_OBSTRUCTION_SHA256,
        "v008_postbuild_audit_binding_obstruction_sha256": V008_BINDING_OBSTRUCTION_SHA256,
        "v009_hostile_audit_obstruction_sha256": V009_HOSTILE_OBSTRUCTION_SHA256,
        "v010_hostile_audit_obstruction_sha256": V010_HOSTILE_OBSTRUCTION_SHA256,
        "v010_audit_record_custody_correction_sha256": V010_CUSTODY_CORRECTION_SHA256,
        "v011_hostile_audit_obstruction_sha256": V011_HOSTILE_OBSTRUCTION_SHA256,
        "preflight_result_sha256": authenticated_hashes["preflight_result"],
        "independent_hostile_audit_sha256": authorization["independent_hostile_audit"]["sha256"],
        "superseded_v005_dual_gate_sha256": V005_DUAL_GATE_SHA256,
        "superseded_v005_cache_manifest_sha256_by_L": V005_CACHE_MANIFEST_SHA256,
        "superseded_v007_dual_gate_sha256": V007_DUAL_GATE_SHA256,
        "superseded_v007_cache_manifest_sha256_by_L": V007_CACHE_MANIFEST_SHA256,
        "superseded_v008_dual_gate_sha256": V008_DUAL_GATE_SHA256,
        "superseded_v008_cache_manifest_sha256_by_L": V008_CACHE_MANIFEST_SHA256,
        "canonical_cache_root": str(output),
        "claim_boundary": "TARGET_V012_PORTABLE_STORAGE_INDICES_ONLY__NO_HISTORY_SPECTRUM_OR_GRAVITY",
    }
    manifest_path = output / "CACHE_MANIFEST.json"
    observed_names = set(os.listdir(output_descriptor))
    if observed_names != {str(record["path"]) for record in files}:
        raise AssertionError("cache payload member census changed before manifest")
    # Every member descriptor and the output-directory descriptor remain held
    # through publication, so no path substitution can change the cache set
    # authenticated by the manifest.
    if not (
        len(files) == len(member_descriptors) == len(member_identities)
    ):
        raise AssertionError("cache member retained-custody census mismatch")
    for record, descriptor, identity in zip(
        files, member_descriptors, member_identities,
    ):
        observed = os.fstat(descriptor)
        named = os.stat(
            str(record["path"]), dir_fd=output_descriptor,
            follow_symlinks=False,
        )
        observed_identity = (
            observed.st_dev, observed.st_ino, observed.st_size,
            observed.st_mtime_ns, observed.st_ctime_ns, observed.st_nlink,
            stat.S_IMODE(observed.st_mode),
        )
        named_identity = (
            named.st_dev, named.st_ino, named.st_size,
            named.st_mtime_ns, named.st_ctime_ns, named.st_nlink,
            stat.S_IMODE(named.st_mode),
        )
        if (
            not stat.S_ISREG(observed.st_mode)
            or observed.st_mode & 0o222
            or observed.st_nlink != 1
            or observed_identity != identity
            or named_identity != identity
            or observed.st_size != record["bytes"]
            or sha256_descriptor(descriptor) != record["sha256"]
        ):
            raise Refusal(f"new target cache member {record['path']} custody changed")
    verify_directory_binding(output, output_descriptor, "target cache output")
    validate_production_obligation("A05_FIVE_CACHE_SET", manifest)
    manifest_digest = atomic_publish_json(
        manifest_path, manifest, "target cache manifest", AUTHORITY_CUSTODY,
        parent_descriptor=output_descriptor,
    )
    # Once the canonical manifest link exists, no later failure deletes it.
    # Incomplete publication remains inspectable and makes a retry refuse.
    os.fchmod(output_descriptor, 0o555)
    os.fsync(output_descriptor)
    os.fsync(cache_parent_descriptor)
    verify_directory_binding(output, output_descriptor, "target cache output")
    AUTHORITY_CUSTODY.verify_all()
    manifest_descriptor = os.open(
        manifest_path.name,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
        dir_fd=output_descriptor,
    )
    held_cache_descriptors.append(manifest_descriptor)
    manifest_metadata = os.fstat(manifest_descriptor)
    if (
        not stat.S_ISREG(manifest_metadata.st_mode)
        or manifest_metadata.st_mode & 0o222
        or manifest_metadata.st_nlink != 1
        or sha256_descriptor(manifest_descriptor) != manifest_digest
    ):
        raise Refusal("published target cache manifest custody changed")
    guard_builder(started)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, choices=SUPPORTED, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        build(args.length, args.output)
    except (AssertionError, MemoryError, OSError, Refusal, TimeoutError, ValueError, json.JSONDecodeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
