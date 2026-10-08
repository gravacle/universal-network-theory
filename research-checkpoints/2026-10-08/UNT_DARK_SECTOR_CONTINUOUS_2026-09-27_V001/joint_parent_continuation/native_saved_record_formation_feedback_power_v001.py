#!/usr/bin/env python3
"""Root-only exact saved BS10 record/feedback-power audit; no propagation."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import traceback
AUTHOR_DRAFT=False
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
HERE=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
STEM='NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001'
SOURCE=HERE/'native_saved_record_formation_feedback_power_v001.py'
PROTOCOL=HERE/(STEM+'.md')
OWNER=HERE/(STEM+'_OWNER_START.json');MANIFEST=HERE/(STEM+'_MANIFEST.json')
JOURNAL=HERE/(STEM+'_JOURNAL.jsonl');RESULT=HERE/(STEM+'_RESULT.json')
REPORT=HERE/(STEM+'_REPORT.md');RECEIPT=HERE/(STEM+'_RECEIPT.json');ERROR=HERE/(STEM+'_ERROR.json')
PARENT_CP=HERE/'bs10_two_record_formation_v001_checkpoints'
PARENT_RESULT=HERE/'BS10_TWO_RECORD_FORMATION_V001_RESULT.json'
PARENT_MANIFEST=PARENT_CP/'manifest.json';PARENT_JOURNAL=PARENT_CP/'events.jsonl'
UD,LR,LJ,ER,EP,HFLIP,THOP=1.,.5,.25,1.,1.,.1,.1
DIM=1536;OP_TOL,EIG_TOL,OBS_TOL=1e-11,2e-10,2e-10
OUTPUTS={};RECORDS=[];RAW={};CONTEXT={};SERIAL=0;CONTROL_SERIAL=0;NP=None;SELF_SHA=None
FLAGS={k:False for k in ('physical_Hilbert_stress','physical_record_current','phase_charge_exchange','stable_record_birth','entropy_production','physical_clock','physical_geometry','physical_native_inertia','galactic_force','galactic_formation_history','observational_fit','cosmological_integration','Stage3_complete')}
PINS={
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/reviewed_native_saved_record_formation_feedback_power_v001_488_fa69d907.py':'fa69d907458dddf11bf6e6d52f8423494cad2113bfa368c8a808405714d0daa0',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/reviewed_native_saved_record_formation_feedback_power_v001_19_a780f8ef.md':'a780f8ef70c722d3f7723e77b92f227d0444e0a74d9a3250ab36da7385a384e9',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/NATIVE_RECORD_CURRENT_AND_ENERGY_INTERFACE_AUDIT_V001.md':'5fd894d41f10eb446d73c575b379caa84fa189c539e0fb6a1e49c2de4f4bd359',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_TWO_RECORD_FORMATION_V001.md':'e16fe99f48b6a9bc925652941d872196d5a678b3b264d5d8ff31b2d014162f96',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_TWO_RECORD_FORMATION_V001_RESULT.json':'d90a5ff3fd1d6b9a8a536cce762c5104b8ec9cbccf9d3ef0e6289c082ed95cbc',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS10_TWO_RECORD_FORMATION_V001_RESULT.md':'9f4713c9953987ff87b63e8253f2318768ad737c53a61152a17e2f704cee9032',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS11_DYNAMIC_CARRIER_SOURCE_V001.md':'14ed3bf623571e6f90524aa8788b8b3af0f960be86e00d4eb23206e465d65fca',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS11_DYNAMIC_CARRIER_SOURCE_V001_RESULT.json':'5d01cb9d1bdb793e1c9b12ecd4d6d2ca0f296add81741660c5aceda9dd45aa3f',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS11_DYNAMIC_CARRIER_THERMAL_V001_RESULT.json':'488a21003ac9107b75c71f391308950720c9af8b2fc578cb6ecbfd7607aa7dff',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS11_HELD_FEEDBACK_LOOP_SOURCE_V001.md':'9f22e77099b19a8b45b36d61dbb4fbe3f98c0746604980e676761079048f4210',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/BS11_HELD_FEEDBACK_LOOP_SOURCE_V001_RESULT.json':'a753eda50dc71b286eda9f54cce0ecc6a085e707757ad8420e2894d4b376310b',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/CROSS_U_ACTIVE_RECORD_FORMATION_CURRENT_AND_ENERGY_SOURCE_V001.md':'3e4ac570af650d9182adfea576a0c0982c1fef52715132f14e49f999ae66ca28',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_ACTIVE_RECORD_MECHANISM_AND_STATE_V001.md':'cbaf606bd32eda90af290b10aa5fd72a566ba07a62a7386ad1dee3584bf0bf70',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/NATIVE_SAVED_RECORD_FORMATION_FEEDBACK_POWER_V001.md':'bf28c601d7369ad1038d73576b82196c0a3596f7422114fcfd5768925b8dd44b',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001.py':'41843d768cde60d3a5404cc1db3e6bd799eb8aa0778856c2d7e020a7bce74428',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/events.jsonl':'ad229ee067d9203bd34afe868d3b45b6c5ecb652cea7ed4e36c08f002c8bccd5',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0.eigensystem.npz':'99e0c22b385a09c401c3f50f29ebfba0b5f3dc60511e7a072de2dc08c1dce855',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0.json':'7fea7729bb650a435e7823fdf1fbd60f0d8628c36a7877ee8e883201de99335a',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0.started.json':'98c8a53ac9a9c22a2f4cd534c4fbd21de9a6c420f5caa8f4a4f7a7abf8f4fdae',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_early0_minus.json':'f65ba8239259c850afa74e03416bd72b4af3136dbf3bc4ddbbe970b98e2c5895',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_early0_minus.state.npz':'62cf0a52a893d53afa9ef3c4143d7175d895bf747187f299422bf1e86b062c9a',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_early0_plus.json':'cdafec1cb4e8cf22c764d7fae040412652811f66d10884ce221f6eeecbcba230',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_early0_plus.state.npz':'9d7b070b968adbc2e13eaa8f17781bac6f230f94f4237b82147df088b5f48704',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_early1_minus.json':'f255dd9e0b289898ab2121036f0e4a1a85d64b42d421cffbb52f48ab084477b6',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_early1_minus.state.npz':'405b74f04a2e5efad181eeac3f9b3e9d686210b967ae78a58f3194c6d84dfe63',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_early1_plus.json':'7c6213dcdcf2bfb075bed58b6b0b9d1d28ecba617eb2ee878894c3f54a632b06',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_early1_plus.state.npz':'daafe3b7a63e442fdb16bbe5b0d837e485c9bd549cfdf69dbcae695bf0f15c20',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main0.json':'7e9d0cfa241964ae4de0bf4c673b759b408496faa389e78c351a5b700dc3248e',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main0.state.npz':'7c92751d6490bb45f8a5cc3343e12ca3e501ab4a11d826e9a95dbd2502ba9068',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main1.json':'5e99a44ecd131a97753441224a18bd9a39eb52d921eec6da59501c7e4033cb1f',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main1.state.npz':'58f4091f8da667f98053c821174bc1ed7c6306a5a9731c6f43238fc9170e5c55',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main2.json':'331fce2c4f670432057c37216524cd82b8b2202e16eaaa76c5f970c396a75501',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main2.state.npz':'18b6618742ae143960c5a3bb286bf5c0c8ac231e242f413f9a3507606fe7e1d6',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main3.json':'cd54a2b04534ae9a18640150860fd0f4eef35e467aff71c816d7f45f780fece6',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main3.state.npz':'29a4bf9721a46230da5212ae1633633086c3a94e848a2ab2d34a1e196fb49b2b',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main4.json':'f4282374da7d88dead54e08824bf67d39a1f46c1ab0c07327c8933e6a0c0c572',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main4.state.npz':'7d41ef3ee44d3f3cc4d6a62c302979798c76e2c9ad8bd5876db25b0e04b0d717',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main5.json':'a042945c9390139d4795d4adca18be10c1111765a4e9bd77301fa32123ca3f6d',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main5.state.npz':'bd5e64bfbe535a2cc99850b3707f3209a9faf83c7c83514d265d5b826eb57c4d',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main6.json':'d9594b6504616b893ca46bc575efc16ba4b7701965bf933cadf2bf61e75037c2',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n21_main6.state.npz':'9e2c7e6ca1cb56b57d04719a3aa5e1bd5e9b2403e24df2efd07d533662288d03',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_early0_minus.json':'bd91c1547dfcf8e0541231050f4c18614bd135c25560d9b03cb5d4545cdd762f',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_early0_minus.state.npz':'6d7f79f72ecba6f4233a2b0f367e0b269afa31d54393209e751133d052592bb7',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_early0_plus.json':'56b5ad1aa62e6f58bc1e8ea582de47a8fc68b421d53bfef55b0cab8f43ce8dd7',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_early0_plus.state.npz':'8c25509b65d40e6f37daa8f300191e0bb9bb48d73dc3853e08e37db94d28b938',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_early1_minus.json':'4e2be9bf2e514f6611aa5f8b103d9ff53aa7fb66441d26dc10ec94140190e176',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_early1_minus.state.npz':'07d3606546653520c9e0b8a0a16cd549c89b69979f2de56bb1e357befb9fd692',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_early1_plus.json':'9bb23f216cf8f9089b7e6ba018f7eca9f999caadabe1e13edf9e7912ab1cb97c',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_early1_plus.state.npz':'a66a24b5103cb5451a199601ef6bd7740a83d46960119ee135d57166367858a6',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main0.json':'56139d4eb10e3f50f6ee90fbb28c8e00a125890e9d8f8c08ff7c962d4d61bb39',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main0.state.npz':'2ba1b929a02836526594c0452a0c905f505ebe405ccee5f463d9d3b5c1d87c1f',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main1.json':'86d27c032b66258062aa2e37257f23e05379cf471e3f57fb92c94e5867df579e',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main1.state.npz':'353291b7348ae812014a24691a512823f6fe7039b32c59d3abc2bb5effd719f0',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main2.json':'264238101c23310ba582633e9ffaf891e933f9b32b3f24d081f2933a9c16b127',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main2.state.npz':'0d0422201159775bc586c7971152b82b616b0ea1837f598841beff51e8068335',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main3.json':'88423878e1bee4013fd1443ca361f63715c42db0933f879e9ff712f9a8e9fd13',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main3.state.npz':'bba687cf43dc41d3fe82e895f050e2dce5c3e6261c4d80f69cbf8c3298daaa7e',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main4.json':'93e1a2740377cb3299945c1a4fb2c4194fb8ace6bfd19cbec3d254bfc78d875a',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main4.state.npz':'4c5ea1f6e69448b929ce2aec90fb0abd787a18e6730cf6a5ee3114201bff939c',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main5.json':'54fe8376c277dd378f7817d4b48397fe26dcb1d21686ee7521e4931e4658897f',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main5.state.npz':'ad0903b9613607cc3048d183024e6ae8fb771fe27e2fa3bd644caa5cb37513ea',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main6.json':'be3c617d9e0c4db41543493991437abbfb48c9929d99a8beadcc5509ff2c75c5',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g0_n42_main6.state.npz':'9fcaece6b30c1cf0eef370830e47594def90e59cfa772f4e9e4471bbfdb833a2',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1.eigensystem.npz':'b6d08511fa4fcaa061a8e08dbe7dd98b06d9ee9ebf82e1648de4eb5829e3847b',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1.json':'f714f9363a958e3843fb65b24ddadbd4fb3e2a2d0c6b3e81a9f3be683f92e358',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1.started.json':'b5bcfcb27772f906dd2f8d1c031defe569360c3c1546d9cc534b1a5c7c6a70bd',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_early0_minus.json':'47c0459c5616996afabf5a730cdd316bf54cba6938976ba177c8cc99aef1a636',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_early0_minus.state.npz':'b266f52cff7c6979a085e0e0020504b393887df07d878d93923bd5f1610ed7cc',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_early0_plus.json':'a283ea5f47441d4ed7e0ef15552a3e768f8a8973bb1d3d321e735a3c2008c042',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_early0_plus.state.npz':'73f80155a085702a0717ffed6d1314438159245ca8aff40346943b92801a4dec',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_early1_minus.json':'254abb03806dbd32a75cdfa9f04bdc2610c4deed088c1fb7a8ea7a80c5e4b535',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_early1_minus.state.npz':'4d98ccaf1bd2b289a4c4bbd6b573bf9567f6f2fe5b3c55ce4a28bd2ba9eee2f9',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_early1_plus.json':'9ec8e4ce151087cb5a05204df0d100ce76dfac9f573129641a89e48f024afad5',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_early1_plus.state.npz':'c9c2d9af52ee5d5e83d1dd0142dd76283ce08c9da00449a6fef1d4bf13946382',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main0.json':'02438933237cd79e4c273f076b1fae89eeb067f884c15c3b9bbfec3bf8f91880',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main0.state.npz':'63fba50a8e334766ac8d25e95c7e50d0e52ee2fc368998cdbb62e909613a6310',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main1.json':'1b2e15af9065fa9d4dd733760eb0ab0232bc6743dd5ca9b49c30c6d4e1057168',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main1.state.npz':'7e96cb7f91ac773d282d8f3ffd2d7a1364b30b864080c17d91b94829eaf30445',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main2.json':'48150689c2403b78074fa58a702cf69ddeb433bb9f97cfd4bd053838d6ec579e',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main2.state.npz':'ecf8ca285ba8a6d29e4d8d372081f9a94d290d50520ca224abc34d371ca377e1',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main3.json':'ad7f7dc3311a6702acba2e71d21a0ae9b982b729372d8731a932959ac45d9fa0',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main3.state.npz':'b996293bcf8f9ef761c1818b66965dcb44bc2abfbd6cdb9b47423d3f77eaafe1',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main4.json':'b6fc452baf781027a6661ba0c770a43b9209ed2e091dd659d84193142be62fd0',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main4.state.npz':'05d4480e505c8dceec658c1881ef60e931913e0ed70029edd0065000ac0f6270',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main5.json':'d273c8168d2a1efeb75368c300243d3800a71a862742c7267c7010201b9bd1b1',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main5.state.npz':'f3cb19bbf9b53fde61bba159cdceb8398633e0f52144ef51b49154ba17b70bd1',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main6.json':'bf2de5a930f6a107b0063e079f12e155f3856a7b474873b24c7f00db524c998d',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n21_main6.state.npz':'933ea8c7c061972ba5aa75984f8b74d23e16dee73f9083b89542604861080e76',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_early0_minus.json':'a9c71e1f53b3b0720e886fa0f6eb1a3837a70b000fdb86d0a5f035ddebcfb117',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_early0_minus.state.npz':'48348f57f65ffd5c22a6bf3a2d5688371ac01c97f5579f3fbb8045e65fc3ae63',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_early0_plus.json':'6fe795fc16eaf5fe767b4c3e1b0e6b650c4bb5b59704aa4b19305ed82df0dfea',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_early0_plus.state.npz':'508b14a7a8dfee46521af47c91212686610ea21722ad032262fa07beb53691f2',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_early1_minus.json':'974d2beccf4ce571df24fd7e04233dedeed8907d68db79580979e3a51070ddfe',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_early1_minus.state.npz':'69c17e67216227336b69d5434c179b0fa010f9717a411a11f72a6b7647ff967a',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_early1_plus.json':'32dc56abc2e41c46087db275352adec94a8874ea403cc9992788d540f8db5bc3',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_early1_plus.state.npz':'a58dcbff8cbd3fab8c75b94bc263e2361925e03997de4f52a966c3e6e00e439c',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main0.json':'c0329aea8d56af1c9dc84f9fddf9f277ba52e9b0ace9ad4ec1d49f12364ae75c',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main0.state.npz':'d794120c9249751b2e0a539ba216915792d04c1a79d776cb2684bee9e2d3eeba',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main1.json':'5e5396bebc4618ab4cfdc7e6cfbe5805c1ab8b82c827dcdc961231e285c50490',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main1.state.npz':'90b732711beca3b59209d5229a75746a4b526ff222d13085e58774a2a3a7866a',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main2.json':'dc3ecff12db2fc33ddfff06f2078b9b564b7637e1b7be6b0b11c8403d5f2a4d3',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main2.state.npz':'cd9ac6e0a6802c309e72bf8576b5184595401998ec87dff801dfc08fb7bdbfaa',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main3.json':'48dfa2dba173fb550f044926ec7b34df54e01416784a5f270d761206d835a3f7',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main3.state.npz':'e12a0574a4760cdf1547df6eba538da8be009e2ce9d4d68403baa84a3ec7fc19',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main4.json':'817b7929878e2e5974d4474488821d49550a9ee54920167f7776bac656e5132f',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main4.state.npz':'115dce180d620437dc31fba77006ff49490acee70ec9794fd9437bcdc81fe84f',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main5.json':'64bad487988367c2ca3adc24f315c5e612d6b1cb22cdd9a5ec4f30fb470848e4',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main5.state.npz':'0e412073353ba845806ac4b1aece16bef6d12fa338159dfd23d743a8644a107e',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main6.json':'79745770404ef1371d9ee2cc7b48e42255aa17b4e4e30044055f213e6fd771ab',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/g1_n42_main6.state.npz':'ef49df23fda55f6d6db61c6172f9a93e1732c7b712627a3c6f8206e1394d44e8',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs10_two_record_formation_v001_checkpoints/manifest.json':'ff9c2b6f6e6d16a546a386c96a61ce44f6b2f69deda3925a0502c50185ef9e6d',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs11_dynamic_carrier_source_v001.py':'c8e49941c89864568202b102c9d0c6dd7bfc94d204977027230eafda96d31b8d',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs11_dynamic_carrier_source_v001_checkpoints/Nc1_q0.npz':'813f3ad05f9aa4a60a926c850d3a9b6bda801b876fc6b63590c65f1be393da24',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/bs11_held_feedback_loop_source_v001.py':'b6e305e31f99679510d6c146839b91623391754f29be14e93f2f03014f6be596',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md':'00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec',
    '/Users/bgm/Documents/ChatGPT/Universal Network Theory/program-worktree/MODEL.md':'3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607',
}

def basis(np):
    rows=np.arange(DIM);ns=rows//24;carrier=(rows//4)%6;r=rows%4
    nb=np.array([[(n>>e)&1 for e in range(6)] for n in range(64)],dtype=float)
    p=np.eye(6)[carrier];q=np.zeros((DIM,6));q[:,0]=r&1;q[:,3]=(r>>1)&1
    pos=np.array([(np.cos(2*np.pi*v/6),np.sin(2*np.pi*v/6)) for v in range(6)])
    reflected_n=np.array([sum(((int(n)>>e)&1)<<((-e-1)%6) for e in range(6)) for n in ns])
    reflection=(reflected_n*6+((-carrier)%6))*4+r
    links={};transfers={};copies={}
    for e in range(6):
        links[e]=(rows,((ns^(1<<e))*6+carrier)*4+r)
        use=(nb[ns,e]==1)&((carrier==e)|(carrier==(e+1)%6));src=rows[use]
        newcarrier=np.where(carrier[use]==e,(e+1)%6,e)
        transfers[e]=(src,(ns[use]*6+newcarrier)*4+r[use])
    for bit,v in enumerate((0,3)):
        src=rows[carrier==v];copies[v]=(src,(ns[src]*6+carrier[src])*4+(r[src]^(1<<bit)))
    return dict(rows=rows,ns=ns,carrier=carrier,r=r,nb=nb,p=p,q=q,pos=pos,
                allpos=np.vstack([pos,2*pos]),reflection=reflection,
                links=links,transfers=transfers,copies=copies)

def build(np,g,s):
    H=np.zeros((DIM,DIM));G=[np.zeros_like(H),np.zeros_like(H)]
    diagonal=np.zeros(DIM);gd=np.zeros((DIM,2));parts={}
    degree=np.array([1+s['nb'][s['ns'],(v-1)%6]+s['nb'][s['ns'],v] for v in range(6)]).T
    parts['active_degree']=UD*np.sum((degree-2)**2,axis=1)
    parts['exterior_degree']=np.full(DIM,6*UD)
    parts['carrier_storage']=np.full(DIM,EP)
    parts['external_current_square']=np.full(DIM,LJ)
    parts['record_storage']=ER*s['q'].sum(axis=1)
    parts['external_record_feedback']=-LR*s['q'].sum(axis=1)
    parts['internal_current_square']=np.zeros(DIM);parts['internal_record_feedback']=np.zeros(DIM)
    for v in range(6):
        onsite=UD*(degree[:,v]-2)**2+ER*s['q'][:,v]+EP*s['p'][:,v]
        ext=LJ*s['p'][:,v]-LR*s['q'][:,v]
        diagonal+=onsite+UD+ext
        gd+=(onsite+2*UD+1.5*ext)[:,None]*s['pos'][v]
    for e in range(6):
        nxt=(e+1)%6;w=(s['pos'][e]+s['pos'][nxt])/2;n=s['nb'][s['ns'],e]
        a=s['p'][:,e]+s['p'][:,nxt]-2*s['p'][:,e]*s['p'][:,nxt]
        current=LJ*n*a;records=-LR*n*(s['q'][:,e]+s['q'][:,nxt])
        parts['internal_current_square']+=current;parts['internal_record_feedback']+=records
        diagonal+=current+records;gd+=(current+records)[:,None]*w
        for mapping,coefficient in [(s['links'][e],-HFLIP),(s['transfers'][e],-THOP)]:
            src,dst=mapping;H[src,dst]+=coefficient
            for i in range(2):G[i][src,dst]+=coefficient*w[i]
    for v,mapping in s['copies'].items():
        src,dst=mapping;H[src,dst]+=g
        for i in range(2):G[i][src,dst]+=g*s['pos'][v,i]
    H[s['rows'],s['rows']]=diagonal
    for i in range(2):G[i][s['rows'],s['rows']]=gd[:,i]
    return H,G,parts,degree

def enc(value):
    if isinstance(value,dict):return {str(k):enc(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [enc(v) for v in value]
    if hasattr(value,'item'):return enc(value.item())
    if isinstance(value,float) and not math.isfinite(value):raise ValueError('Nonfinite JSON scalar')
    return value

def encoded(value):return (json.dumps(enc(value),sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def exclusive(path,data):
    data=data if isinstance(data,bytes) else encoded(data)
    with Path(path).open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    Path(path).chmod(0o444);OUTPUTS[str(path)]=sha(path)
    if Path(path).read_bytes()!=data:raise RuntimeError('Publication bytes differ')
    return OUTPUTS[str(path)]
def journal(kind,**data):
    row=encoded(dict(event=kind,pid=os.getpid(),utc=datetime.now(timezone.utc).isoformat(),**data))
    with JOURNAL.open('ab') as f:f.write(row.replace(b'\n',b'')+b'\n');f.flush();os.fsync(f.fileno())

def authenticate():
    for p,h in PINS.items():
        if sha(p)!=h:raise RuntimeError('Pinned bytes changed: '+p)
    result=json.loads(PARENT_RESULT.read_text());m=json.loads(PARENT_MANIFEST.read_text())
    ev=[json.loads(s) for s in PARENT_JOURNAL.read_text().splitlines()]
    if result['status']!='QUALIFIED_ARITHMETIC' or result['check_count']!=656 or result['passed_count']!=656 or result['failed_count']!=0 or result['next_unfinished'] is not None:raise RuntimeError('Parent terminal qualification')
    if result['pid']!=24707 or m['pid']!=24707 or ev[-1]['event']!='run_complete' or ev[-1]['status']!=result['status'] or ev[-1]['pid']!=24707:raise RuntimeError('Parent owner/closure')
    if result['input_sha256']!=m['input_sha256'] or any(PINS.get(p)!=h for p,h in result['input_sha256'].items()):raise RuntimeError('Parent input map')
    controls=list(result['checks']);admitted=[];keys=set()
    for ig,g in enumerate((0.,.1)):
        h=result['Hamiltonians'][ig];label='g'+str(ig)
        if h['g']!=g or h['failed_count'] or len(h['states'])!=22:raise RuntimeError('Parent Hamiltonian census')
        hp=PARENT_CP/(label+'.json')
        if json.loads(hp.read_text())!=h:raise RuntimeError('Parent Hamiltonian record mismatch')
        commits=[x for x in ev if x['event']=='Hamiltonian_complete' and x['key']==label]
        if len(commits)!=1 or commits[0]['sha256']!=PINS[str(hp)]:raise RuntimeError('Parent Hamiltonian journal')
        if PINS.get(h['eigensystem_path'])!=h['eigensystem_sha256']:raise RuntimeError('Parent eigenpair binding')
        controls+=h['checks'];rows=[]
        for start in (21,42):
            schedule=[('main'+str(k),t,False) for k,t in enumerate((0.,1.,2.,5.,10.,20.,50.))]
            schedule += [('early'+str(k)+'_'+sign,sgn*t,True) for k,t in enumerate((.001,.002)) for sign,sgn in (('plus',1),('minus',-1))]
            for timekey,tau,early in schedule:
                key=label+'_n'+str(start)+'_'+timekey
                rr=next(x for x in h['states'] if Path(x['state_path']).name==key+'.state.npz')
                if key in keys:raise RuntimeError('Duplicate parent state')
                keys.add(key);rp=PARENT_CP/(key+'.json');ap=PARENT_CP/(key+'.state.npz')
                if rr['g']!=g or rr['start']!=start or rr['tau']!=tau or rr['auxiliary_early_arm'] is not early or rr['failed_count']:raise RuntimeError('Parent state identity')
                if json.loads(rp.read_text())!=rr or PINS[str(ap)]!=rr['state_sha256'] or rr['eigensystem_sha256']!=h['eigensystem_sha256'] or rr['input_sha256']!=result['input_sha256']:raise RuntimeError('Parent state/payload binding')
                cs=[x for x in ev if x['event']=='state_complete' and x['key']==key]
                if len(cs)!=1 or cs[0]['sha256']!=PINS[str(rp)] or cs[0]['failed']!=0:raise RuntimeError('Parent state journal')
                rows.append((key,rr));controls+=rr['checks']
        admitted.append((label,h,rows))
    if len(keys)!=44 or len(controls)!=656 or any(c['passed'] is not True for c in controls):raise RuntimeError('Parent full control census')
    return result,admitted,controls

def finite(np,a):
    a=np.asarray(a)
    return a.dtype.kind in 'biufc' and bool(np.isfinite(a).all())

def checkpoint(np,key,arrays,meta,qualified=True):
    global SERIAL
    SERIAL+=1;p=HERE/(STEM+'_'+str(SERIAL).zfill(5)+'_'+key+'.npz');cp=p.with_suffix('.COMMIT.json')
    local={str(k):np.asarray(v) for k,v in arrays.items()}
    if any(a.dtype.kind=='O' for a in local.values()):raise TypeError('Object checkpoint operand')
    if qualified and any(not finite(np,a) for a in local.values()):raise ArithmeticError('Nonfinite qualified checkpoint')
    text=encoded(dict(meta,record_key=key,serial=SERIAL,source_sha256=SELF_SHA,parent_result_sha256=PINS[str(PARENT_RESULT)],operand_schema_qualified=qualified)).decode()
    detached=json.loads(text);local['metadata_json']=np.array(text)
    with p.open('xb') as f:np.savez(f,**local);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);ph=sha(p);OUTPUTS[str(p)]=ph
    commit=dict(checkpoint=p.name,sha256=ph,metadata=detached,arrays={n:dict(shape=list(a.shape),dtype=a.dtype.str) for n,a in local.items()},owner_pid=os.getpid(),status='ACCEPTED_RAW' if qualified else 'UNQUALIFIED_RAW')
    exclusive(cp,commit)
    with np.load(p,allow_pickle=False) as z:
        if set(z.files)!=set(local):raise RuntimeError('Checkpoint array names changed')
        for n,a in local.items():
            b=z[n]
            if a.shape!=b.shape or a.dtype!=b.dtype or not (np.array_equal(a,b,equal_nan=True) if a.dtype.kind in 'biufc' else np.array_equal(a,b)):raise RuntimeError('Checkpoint array reread')
        if json.loads(str(z['metadata_json']))!=detached:raise RuntimeError('Checkpoint metadata reread')
    rec=dict(npz=str(p),npz_sha256=ph,commit=str(cp),commit_sha256=OUTPUTS[str(cp)],metadata=detached,commit_object=commit)
    RECORDS.append(rec);journal('checkpoint',key=key,npz=p.name,npz_sha256=ph,commit=cp.name,commit_sha256=OUTPUTS[str(cp)])
    return dict(npz=p.name,npz_sha256=ph,commit=cp.name,commit_sha256=OUTPUTS[str(cp)])

def check(np,checks,name,actual,expected,tol,scale=1.):
    global CONTROL_SERIAL
    CONTROL_SERIAL+=1;prefix='control_'+str(CONTROL_SERIAL).zfill(5)+'_'+name
    a=np.asarray(actual);b=np.asarray(expected);RAW[prefix+'_actual']=a;RAW[prefix+'_expected']=b
    CONTEXT.update(control_ordinal=CONTROL_SERIAL,control_name=name)
    if a.shape!=b.shape or not finite(np,a) or not finite(np,b) or not math.isfinite(float(scale)) or scale<=0:raise ArithmeticError('Control operand schema/finite')
    error=float(np.max(np.abs(a-b))) if a.size else 0.
    passed=error<=tol*scale
    checks.append(dict(name=name,passed=passed,maximum_absolute_error=error,scale=float(scale),tolerance=float(tol),raw_prefix=prefix))
    return passed

def operators(np,s,g,parts):
    diagonal=sum(parts.values());off={'incidence_flip':(s['links'],-HFLIP),'carrier_hopping':(s['transfers'],-THOP),'record_copy':(s['copies'],g)}
    names=list(parts)+list(off)
    def apply(name,v):
        v=np.asarray(v)
        if name in parts:return parts[name].reshape((DIM,)+(1,)*(v.ndim-1))*v
        out=np.zeros_like(v,dtype=np.result_type(v.dtype,np.float64));maps,c=off[name]
        for src,dst in maps.values():out[src]+=c*v[dst]
        return out
    def total(v):
        v=np.asarray(v);out=diagonal.reshape((DIM,)+(1,)*(v.ndim-1))*v
        for name in off:out=out+apply(name,v)
        return out
    def deriv(q,v):return 1j*(total(q*v)-q*total(v))
    return names,apply,total,deriv

def process_state(np,key,row,s,H,G,E,V,parts,ops):
    global RAW,CONTROL_SERIAL
    RAW={};CONTROL_SERIAL=0;CONTEXT.clear();CONTEXT.update(state_key=key,g=row['g'],tau=row['tau'],start=row['start'])
    with np.load(row['state_path'],allow_pickle=False) as z:
        if set(z.files)!=set(('complete_state','input_sha256_json','eigensystem_sha256','tau','start','g')):raise RuntimeError('State header names')
        psi=z['complete_state'].copy();RAW['complete_state']=psi
        if psi.shape!=(DIM,) or psi.dtype!=np.dtype('<c16') or not finite(np,psi):raise ArithmeticError('State schema')
        if json.loads(str(z['input_sha256_json']))!=row['input_sha256'] or str(z['eigensystem_sha256'])!=row['eigensystem_sha256'] or float(z['tau'])!=row['tau'] or int(z['start'])!=row['start'] or float(z['g'])!=row['g']:raise RuntimeError('State embedded metadata')
    names,apply,total,deriv=ops;checks=[];Hpsi=H@psi;RAW['H_state']=Hpsi
    eigenH=V@(E*(V.T@psi));RAW['eigenpair_H_state']=eigenH
    scale=max(1.,float(np.max(np.abs(Hpsi))))
    check(np,checks,'same_complete_eigen_action',eigenH,Hpsi,EIG_TOL,scale)
    ca=np.stack([apply(n,psi) for n in names]);RAW['component_actions']=ca
    check(np,checks,'eleven_component_action',ca.sum(axis=0),Hpsi,OP_TOL,scale)
    means=np.array([np.vdot(psi,a) for a in ca]);RAW['component_means_complex']=means
    old=np.array([row['complete_energy_components'][n] for n in names]);RAW['copied_component_means']=old
    check(np,checks,'component_means_saved',means.real,old,OBS_TOL,max(1.,float(np.max(np.abs(old)))))
    energy=np.vdot(psi,Hpsi);RAW['complete_energy_complex']=energy
    check(np,checks,'complete_energy_saved',np.array(energy.real),np.array(row['complete_energy']),OBS_TOL,max(1.,abs(row['complete_energy'])))
    norm=float(np.vdot(psi,psi).real);RAW['original_state_norm']=np.array(norm)
    check(np,checks,'state_norm_saved',np.array(norm),np.array(sum(row['record_probabilities'])),OBS_TOL)
    prob=np.abs(psi)**2;qm=prob@s['q'];nm=prob@s['nb'][s['ns']];pm=prob@s['p']
    RAW.update(record_means=qm,incidence_means=nm,carrier_means=pm)
    check(np,checks,'record_means_saved',qm,np.array(row['record_mean']),OBS_TOL)
    check(np,checks,'incidence_means_saved',nm,np.array(row['incidence_mean']),OBS_TOL)
    check(np,checks,'carrier_means_saved',pm,np.array(row['carrier_mean']),OBS_TOL)
    q=s['q'].T;n=s['nb'][s['ns']].T;p=s['p'].T
    rq=np.stack([deriv(x,psi) for x in q]);rn=np.stack([deriv(x,psi) for x in n]);rp=np.stack([deriv(x,psi) for x in p]);RAW.update(record_rate_actions=rq,incidence_rate_actions=rn,carrier_rate_actions=rp)
    cq=apply('record_copy',psi);lf=apply('incidence_flip',psi);hp=apply('carrier_hopping',psi)
    onlyq=np.stack([1j*(apply('record_copy',x*psi)-x*cq) for x in q]);onlyn=np.stack([1j*(apply('incidence_flip',x*psi)-x*lf) for x in n]);onlyp=np.stack([1j*(apply('carrier_hopping',x*psi)-x*hp) for x in p]);RAW.update(copy_only_record_rate_actions=onlyq,flip_only_incidence_rate_actions=onlyn,hop_only_carrier_rate_actions=onlyp)
    check(np,checks,'record_rate_local_copy_only',rq,onlyq,OP_TOL,scale)
    check(np,checks,'incidence_rate_flip_only',rn,onlyn,OP_TOL,scale)
    check(np,checks,'carrier_rate_hop_only',rp,onlyp,OP_TOL,scale)
    check(np,checks,'carrier_total_rate_zero',rp.sum(axis=0),np.zeros(DIM,dtype=complex),OP_TOL,scale)
    rates=np.array([[np.vdot(psi,a) for a in rr] for rr in (rq,rn,rp)]);RAW['all_rates_complex']=rates
    check(np,checks,'occupation_rates_real',rates.imag,np.zeros((3,6)),OBS_TOL,scale)
    link=[];birth=[];mean_link=[];mean_birth=[]
    for e in range(6):
        qe=q[e]+q[(e+1)%6];ne=n[e]
        link.append(-LR/2*(qe*rn[e]+deriv(ne,qe*psi)))
        birth.append(-LR/2*(ne*(rq[e]+rq[(e+1)%6])+deriv(qe,ne*psi)))
        mean_link.append(-LR*float(rates[1,e].real)*(qm[e]+qm[(e+1)%6]))
        mean_birth.append(-LR*nm[e]*float((rates[0,e]+rates[0,(e+1)%6]).real))
    link=np.stack(link);birth=np.stack(birth);external=-LR*rq.sum(axis=0);RAW.update(feedback_link_power_actions=link,feedback_record_power_actions=birth,feedback_external_record_power_action=external,mean_factorized_link_powers=np.array(mean_link),mean_factorized_record_powers=np.array(mean_birth))
    fb=parts['internal_record_feedback']+parts['external_record_feedback'];direct=1j*(total(fb*psi)-fb*total(psi));split=link.sum(axis=0)+birth.sum(axis=0)+external;RAW.update(feedback_direct_power_action=direct,feedback_split_power_action=split)
    check(np,checks,'feedback_Hermitian_Leibniz_action',split,direct,OP_TOL,scale)
    ll=np.array([np.vdot(psi,a) for a in link]);bb=np.array([np.vdot(psi,a) for a in birth]);ee=np.vdot(psi,external);dd=np.vdot(psi,direct)
    RAW.update(feedback_link_powers_complex=ll,feedback_record_powers_complex=bb,feedback_external_power_complex=ee,feedback_direct_power_complex=dd,link_connected_powers=ll.real-np.array(mean_link),record_connected_powers=bb.real-np.array(mean_birth))
    check(np,checks,'feedback_Leibniz_expectation',np.array(ll.sum()+bb.sum()+ee),np.array(dd),OBS_TOL,max(1.,abs(dd)))
    check(np,checks,'feedback_piece_powers_real',np.r_[ll.imag,bb.imag,ee.imag,dd.imag],np.zeros(14),OBS_TOL,scale)
    power_actions=np.stack([1j*(total(a)-apply(name,Hpsi)) for name,a in zip(names,ca)]);RAW['component_power_actions']=power_actions
    powers=np.array([np.vdot(psi,a) for a in power_actions]);fast=np.array([2*np.vdot(a,Hpsi).imag for a in ca]);RAW.update(component_powers_complex=powers,component_power_independent=fast)
    check(np,checks,'component_power_two_routes',powers.real,fast,OBS_TOL,max(1.,float(np.max(np.abs(fast)))))
    check(np,checks,'component_powers_real',powers.imag,np.zeros(11),OBS_TOL,scale)
    check(np,checks,'complete_energy_power_zero',np.array(powers.sum()),np.array(0j),OBS_TOL,scale)
    selected=powers[names.index('internal_record_feedback')]+powers[names.index('external_record_feedback')]
    check(np,checks,'feedback_complete_component_power',np.array(dd),np.array(selected),OBS_TOL,scale)
    ga=np.stack([a@psi for a in G]);RAW['complete_source_actions']=ga
    gm=np.array([np.vdot(psi,a) for a in ga]);RAW['complete_source_means_complex']=gm
    check(np,checks,'complete_source_means_saved',gm.real,np.array(row['complete_source_mean']),OBS_TOL,max(1.,float(np.max(np.abs(gm)))))
    gdot=np.stack([1j*(total(a)-G[k]@Hpsi) for k,a in enumerate(ga)]);RAW['complete_source_power_actions']=gdot
    gp=np.array([np.vdot(psi,a) for a in gdot]);gfast=np.array([2*np.vdot(a,Hpsi).imag for a in ga]);RAW.update(complete_source_powers_complex=gp,complete_source_power_independent=gfast)
    check(np,checks,'complete_source_power_two_routes',gp.real,gfast,OBS_TOL,max(1.,float(np.max(np.abs(gfast)))))
    check(np,checks,'complete_source_powers_real',gp.imag,np.zeros(2),OBS_TOL,scale)
    check(np,checks,'complete_energy_sources_real',np.r_[means.imag,energy.imag,gm.imag],np.zeros(14),OBS_TOL,scale)
    if len(checks)!=24:raise RuntimeError('State prospective control census')
    summary=dict(state_key=key,g=row['g'],start=row['start'],tau=row['tau'],auxiliary_early_arm=row['auxiliary_early_arm'],raw_original_norm=norm,signed_record_rates=rates[0].real.tolist(),signed_incidence_rates=rates[1].real.tolist(),signed_carrier_rates=rates[2].real.tolist(),feedback_link_power=float(ll.real.sum()),feedback_record_power_internal=float(bb.real.sum()),feedback_record_power_external=float(ee.real),feedback_power=float(dd.real),component_energy=dict(zip(names,means.real.tolist())),component_power=dict(zip(names,powers.real.tolist())),affine_source_mean=gm.real.tolist(),affine_source_power=gp.real.tolist(),signed_connected_link_power=float(RAW['link_connected_powers'].sum()),signed_connected_record_power=float(RAW['record_connected_powers'].sum()),explicit_external_source_work=0.,controls=checks,qualified=all(x['passed'] for x in checks),parent_state_npz=Path(row['state_path']).name,parent_state_sha256=row['state_sha256'])
    summary['checkpoint']=checkpoint(np,key,RAW,summary)
    return summary

def recheck(ownerbytes,strict=True,owner_required=True):
    for p,h in PINS.items():
        if sha(p)!=h:raise RuntimeError('Input seal changed')
    if owner_required and (not OWNER.exists() or OWNER.read_bytes()!=ownerbytes):raise RuntimeError('Owner bytes changed')
    for r in RECORDS:
        if sha(r['npz'])!=r['npz_sha256'] or sha(r['commit'])!=r['commit_sha256'] or json.loads(Path(r['commit']).read_text())!=r['commit_object']:raise RuntimeError('Complete pair closure')
        with NP.load(r['npz'],allow_pickle=False) as z:
            if set(z.files)!=set(r['commit_object']['arrays']):raise RuntimeError('Final pair array names')
            if json.loads(str(z['metadata_json']))!=r['metadata']:raise RuntimeError('Final pair metadata')
            for k,d in r['commit_object']['arrays'].items():
                a=z[k]
                if list(a.shape)!=d['shape'] or a.dtype.str!=d['dtype'] or (k!='metadata_json' and r['metadata']['operand_schema_qualified'] and not finite(NP,a)):raise RuntimeError('Final pair schema/finite')
    if strict:
        expected={Path(r['npz']).name for r in RECORDS};actual={p.name for p in HERE.glob(STEM+'_*.npz')}
        ce={Path(r['commit']).name for r in RECORDS};ca={p.name for p in HERE.glob(STEM+'_*.COMMIT.json')}
        if expected!=actual or ce!=ca:raise RuntimeError('Orphan payload/commit')
    for p,h in OUTPUTS.items():
        if Path(p)!=JOURNAL and sha(p)!=h:raise RuntimeError('Output seal changed')

def failure(exc,ownerbytes):
    trace=traceback.format_exc();preservation=None
    if NP is not None and RAW:
        try:checkpoint(NP,'ERROR_RAW',RAW,dict(error_context=CONTEXT,traceback=trace),False)
        except BaseException:preservation=traceback.format_exc()
    preserved_receipt_sha=sha(RECEIPT) if RECEIPT.exists() else None
    for p in HERE.glob(STEM+'*'):
        if p==PROTOCOL or not p.is_file() or p==ERROR:continue
        p.chmod(0o444);OUTPUTS[str(p)]=sha(p)
    orphans=[p.name for p in HERE.glob(STEM+'_*.npz') if str(p) not in {r['npz'] for r in RECORDS}]
    obj=dict(status='CLOSED_ERROR',pid=os.getpid(),source_sha256=SELF_SHA,error_context=CONTEXT,traceback=trace,raw_preservation_traceback=preservation,inputs=PINS,outputs=dict(OUTPUTS),records=RECORDS,unqualified_orphan_payloads=orphans,preserved_receipt_sha256=preserved_receipt_sha,physical_flags=FLAGS)
    if not ERROR.exists():exclusive(ERROR,obj)
    if not RECEIPT.exists():exclusive(RECEIPT,dict(status='CLOSED_ERROR',pid=os.getpid(),inputs=PINS,outputs=dict(OUTPUTS),records=RECORDS,physical_flags=FLAGS))
    if preserved_receipt_sha is not None and sha(RECEIPT)!=preserved_receipt_sha:raise RuntimeError('Prior receipt changed')
    recheck(ownerbytes,False,OWNER.exists() and OWNER.read_bytes()==ownerbytes)

def main():
    global NP,SELF_SHA,RAW,CONTROL_SERIAL
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root-execute',action='store_true');args=p.parse_args()
    if not args.root_execute:print(json.dumps(dict(prospective=True,AUTHOR_DRAFT=AUTHOR_DRAFT,states=44,new_controls=1076,parent_controls=656,planned_pairs=46)));return 0
    if AUTHOR_DRAFT:raise RuntimeError('Author draft refuses execution')
    if sys.platform!='darwin' or Path(__file__).resolve()!=SOURCE.resolve():raise RuntimeError('Root Mac/source context')
    existing=[x for x in HERE.glob(STEM+'*') if x!=PROTOCOL]
    if existing:raise FileExistsError('Exclusive namespace already used')
    parent,admitted,oldcontrols=authenticate();SELF_SHA=sha(SOURCE)
    ownerbytes=encoded(dict(pid=os.getpid(),utc=datetime.now(timezone.utc).isoformat(),source_sha256=SELF_SHA,parent_pid=24707,parent_result_sha256=PINS[str(PARENT_RESULT)]))
    allstates=[];allchecks=[];hrecords=[]
    try:
        exclusive(OWNER,ownerbytes)
        exclusive(MANIFEST,dict(pid=os.getpid(),source_sha256=SELF_SHA,inputs=PINS,parent_result_sha256=PINS[str(PARENT_RESULT)],states=44,new_controls=1076,parent_controls=656,planned_pairs=46,units=dict(tau='hbar/Ud fixture',rates='Ud/hbar',powers='Ud^2/hbar',Ud=1.,hbar=1.,physical_conversion=None),physical_flags=FLAGS))
        JOURNAL.touch(exist_ok=False);journal('OWNER_START',source_sha256=SELF_SHA)
        for n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[n]='1'
        import numpy as np
        NP=np;s=basis(np)
        for label,h,rows in admitted:
            RAW={};CONTROL_SERIAL=0;CONTEXT.clear();CONTEXT.update(Hamiltonian=label,g=h['g'])
            with np.load(h['eigensystem_path'],allow_pickle=False) as z:
                if set(z.files)!=set(('complete_eigenvalues','eigenvectors_columns','input_sha256_json','matrix_sha256_json','g')):raise RuntimeError('Eigenpair names')
                E=z['complete_eigenvalues'].copy();RAW['complete_eigenvalues']=E;V=z['eigenvectors_columns'].copy();RAW['eigenvectors_columns']=V
                if E.shape!=(DIM,) or V.shape!=(DIM,DIM) or E.dtype!=np.dtype('<f8') or V.dtype!=np.dtype('<f8') or not finite(np,E) or not finite(np,V):raise ArithmeticError('Full eigenpair schema')
                if json.loads(str(z['input_sha256_json']))!=parent['input_sha256'] or json.loads(str(z['matrix_sha256_json']))!=h['matrix_sha256'] or float(z['g'])!=h['g']:raise RuntimeError('Eigenpair embedded identity')
            H,G,parts,degree=build(np,h['g'],s);RAW.update(H=H,Gx=G[0],Gy=G[1],degree=degree,record_diagonal=s['q'],incidence_diagonal=s['nb'][s['ns']],carrier_diagonal=s['p'])
            ops=operators(np,s,h['g'],parts);names,apply,total,deriv=ops;hc=[]
            for k,a in [('H',H),('Gx',G[0]),('Gy',G[1])]:
                digest=hashlib.sha256(np.ascontiguousarray(a,dtype='<f8').tobytes()).hexdigest()
                check(np,hc,'saved_'+k+'_matrix_sha256',np.array(digest==h['matrix_sha256'][k],dtype=int),np.array(1),0.)
                check(np,hc,k+'_Hermitian',np.array(float(np.max(np.abs(a-a.T)))),np.array(0.),OP_TOL,max(1.,float(np.max(np.abs(a)))))
            Hrec=np.diag(sum(parts.values()))
            for maps,c in ((s['links'],-HFLIP),(s['transfers'],-THOP),(s['copies'],h['g'])):
                for src,dst in maps.values():Hrec[src,dst]+=c
            RAW['eleven_component_matrix']=Hrec
            check(np,hc,'complete_H_component_reconstruction',np.array(float(np.max(np.abs(Hrec-H)))),np.array(0.),OP_TOL,max(1.,float(np.max(np.abs(H)))))
            storage=[];birth=[];degrees=[]
            for start in (21,42):
                seed=np.zeros(DIM,dtype=complex);seed[start*24]=1.;hs=total(seed);qs=s['q'][:,0]
                qrate=deriv(qs,seed);storage.append(2*np.vdot(ER*qrate,hs).imag)
                ne=s['nb'][s['ns']].T;qq=s['q'].T;born=np.zeros(DIM,dtype=complex)
                for e in range(6):
                    qe=qq[e]+qq[(e+1)%6]
                    born+=-LR/2*(ne[e]*deriv(qe,seed)+deriv(qe,ne[e]*seed))
                born+=-LR*sum((deriv(x,seed) for x in qq),start=np.zeros(DIM,dtype=complex))
                birth.append(2*np.vdot(born,hs).imag);degrees.append(float(degree[start*24,0]))
            RAW.update(onset_storage_power_derivative=np.array(storage),onset_feedback_birth_power_derivative=np.array(birth),onset_source_degrees=np.array(degrees))
            expected_s=np.full(2,2*ER*h['g']**2);expected_b=-2*LR*np.array(degrees)*h['g']**2
            check(np,hc,'existing_seed_storage_power_onset',np.array(storage),expected_s,OP_TOL)
            check(np,hc,'existing_seed_feedback_birth_power_onset',np.array(birth),expected_b,OP_TOL)
            check(np,hc,'existing_seed_degree2_record_birth_power_cancel',np.array(storage)+np.array(birth),np.zeros(2),OP_TOL)
            if len(hc)!=10:raise RuntimeError('Hamiltonian control census')
            for name,a in parts.items():RAW['diagonal_component_'+name]=a
            hr=checkpoint(np,label+'_H_INPUT',RAW,dict(Hamiltonian=label,g=h['g'],component_names=names,controls=hc,qualified=all(x['passed'] for x in hc),parent_eigensystem_sha256=h['eigensystem_sha256']))
            hrecords.append(dict(Hamiltonian=label,g=h['g'],checkpoint=hr,controls=hc));allchecks+=hc
            if any(not x['passed'] for x in hc):raise ArithmeticError('Full H certification refuses states')
            for key,row in rows:
                summary=process_state(np,key,row,s,H,G,E,V,parts,ops);allstates.append(summary);allchecks+=summary['controls']
            del H,G,E,V,parts,degree,ops
        if len(allstates)!=44 or len(allchecks)!=1076 or len(RECORDS)!=46:raise RuntimeError('Whole prospective census')
        recheck(ownerbytes)
        status='ARITHMETIC_PASS' if all(c['passed'] for c in allchecks) else 'ARITHMETIC_FAILED'
        result=dict(status=status,pid=os.getpid(),inputs=PINS,source_sha256=SELF_SHA,parent_pid=24707,parent_result_sha256=PINS[str(PARENT_RESULT)],copied_parent_checks=oldcontrols,copied_parent_status=parent['status'],old_check_count=656,new_controls=allchecks,new_control_count=1076,passed=sum(c['passed'] for c in allchecks),failed=sum(not c['passed'] for c in allchecks),Hamiltonians=hrecords,states=allstates,records=RECORDS,physical_flags=FLAGS,physical_unknowns=dict(metric_source=None,SI_clock=None,galaxy_force=None,phase_charge_exchange=None,formation_history=None,stable_record_birth=None))
        exclusive(RESULT,result)
        report=('# Saved active-record/feedback-energy diagnostic V001\n\nStatus '+status+'. New controls '+str(result['passed'])+'/1076; all656 original predicates copied unchanged.\n\nAll44 signed local writing, incidence/carrier rates and correlated full feedback powers are retained. This is native finite supported reversible arithmetic; no entropy production, phase-charge source, physical stress or galaxy-force claim.\n')
        exclusive(REPORT,report.encode());journal('CLOSED',status=status,new_controls=1076,states=44,pairs=46)
        JOURNAL.chmod(0o444);OUTPUTS[str(JOURNAL)]=sha(JOURNAL);recheck(ownerbytes)
        receipt=dict(status='CLOSED',outcome=status,pid=os.getpid(),source_sha256=SELF_SHA,inputs=dict(PINS),outputs=dict(OUTPUTS),records=RECORDS,physical_flags=FLAGS)
        exclusive(RECEIPT,receipt);recheck(ownerbytes)
        if json.loads(RECEIPT.read_text())!=receipt:raise RuntimeError('Complete receipt mismatch')
        print(json.dumps(dict(status=status,states=44,new_controls=1076,passed=result['passed'],failed=result['failed'],old_controls=656,pairs=46,result_sha256=OUTPUTS[str(RESULT)],receipt_sha256=OUTPUTS[str(RECEIPT)])))
        return 0 if status=='ARITHMETIC_PASS' else 3
    except BaseException as exc:
        failure(exc,ownerbytes);raise

if __name__=='__main__':sys.exit(main())
