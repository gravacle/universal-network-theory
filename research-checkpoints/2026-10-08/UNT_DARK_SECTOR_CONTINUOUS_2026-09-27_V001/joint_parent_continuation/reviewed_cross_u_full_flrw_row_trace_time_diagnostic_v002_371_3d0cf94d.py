"""Guarded bounded root-only original-row, trace and local time-step diagnostic."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,time,traceback,copy
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V002'
FAILED='CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001'
COPIED_CASE_FILES=['CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_TRACE_FINE_K1_O0_CASE.json', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_RADIATION_FINE_K1_O0_CASE.json', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_TRACE_FINE_K1_O1_CASE.json', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_RADIATION_FINE_K1_O1_CASE.json', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_TRACE_FINE_K1_O2_CASE.json']
REFUSED_FILE=FAILED+'_028_REFUSED.npz'
REFUSED_COMMIT=REFUSED_FILE+'.COMMIT.json'
PARENT='CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001'
PARENT_SOURCE='cross_u_full_flrw_core_baryon_recovery_v001.py'
AUTHOR_GUARD=True
ROW_GATE=2e-11
WORKING_STOP=1e-13
INCREMENT_GATE=1e-6
CORRECTIONS=6
PROTOCOL_SHA='ef37ab204dbfd04d0eacabd4f628818aaf44283d18e7c35348f5070c12ef19f3'
PINS={'cross_u_full_flrw_core_baryon_recovery_v001.py': 'd9efb102c8a60a0845dde9fd4a3c9020d7f5e210c10a995a53faa0ba68e71b31', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001.md': 'f73ffcb2e311602e4a6ca4dfeeef7121cbf3113878e45ab04826daa40a3a4419', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_RESULT.json': 'b96a588b0421bf88666899e846bf50229305db0401b4bad546591e46e2f8576d', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_REPORT.md': '441d557f3d61c9566bb549a57eb33ce9ae1256f449d892def240a3dba8605c8a', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_RECEIPT.json': 'be1491ac72166d7fc51a7ff7d40ccd99142a215200e338cc034bba025a8ae22b', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_MANIFEST.json': '8ef61d1bbd705ba0e8c4af6f81a9337d72a35b0a65b015f9800472aec94dbf45', 'cross_u_full_flrw_core_row_diagnostic_v001.py': '7f701443b0601ee47ef996133fbe1bd3a09535fbb6b9fc3c7a27705b5eb183b8', 'constrained_u_shared_eps_ngc_pantheon_v001.py': '03809b3c3798563725450bb4b7cf8c91654525ad874b6bc38e85da7c8cd22c52', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_000000.npz': 'd160f91bd421e1a48c3aa9b66eb8cfde9bee24d89b4a4a3d381124e3162cd28a', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_000000_COMMIT.json': 'ad1009ea069a389b130f411ddedf0de02e17c7d4e020287ea9d45bb1b69f897d', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_002176.npz': '47930b1935ad64c07145c824141ce47231ef45f657a87c31dfa09cd229f6e664', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_002176_COMMIT.json': 'b521f4b840ca5384f1213113599859674c797afd25a0e803c21c47b67844c6f9', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_003456.npz': 'b3933d3e6121506c57cea09855098627f032fb9dfd962ceddf07eaae9b169d08', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_003456_COMMIT.json': '2195335d5917d4a3183c192701bb24e5f12066e7bd3fa0c939110182c4b58eef', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_004096.npz': '0ff807e24062969917034bda598ee7296fa96cf6c73c6cc3489a6d4ed35c4cc0', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_004096_COMMIT.json': 'b97fa0c2382b27f5f032f015f1f025c44e65c260d9be6f0146dc0d94dbbe8045', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_000000.npz': 'be24fc7a5b503ac0573b60d8ddcfc2df6f4e20091bae52a56d1e2fa4fd339121', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_000000_COMMIT.json': '9af5587c9d8f204bce342339b2841a01fce1532611fb4ea299f14bda70460902', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_002176.npz': '0685867149a22bfb95169a3c7b1e6eb8ce46d7f513f5821c0d0a7a3ad9f273fa', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_002176_COMMIT.json': '54f47e4e4ee758d2cf9d6bfa9bc6564bccb393b885c31b552268fa6524c317f9', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_003456.npz': '82f2888e6112fbdc086697cc6f59cc95d9fd827f7f052b673c480a527b642b4f', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_003456_COMMIT.json': '070342e6f4551028f88c9dddc0360fa2d241210b58ae73f448fa4feec01b45f0', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_004096.npz': '47d9ab6a27ae18fcdb8421dcfd865afde691a415ab3428ed3a8e120b3494c104', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_004096_COMMIT.json': 'e5bb222f389c532bdcdc84c4915b81c58e0fe019f6ac12325b0fe4b62175eed5', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_000000.npz': '103fde82397ed76f2d450980ea6bd902ebe49698604368814f8f8485dc4b2131', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_000000_COMMIT.json': '1561fb4c1c7ea0f7c7188347c1ad1f962cdf4f341f3adb39b61898aa3bca0f0b', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_002176.npz': 'cb39b15c3e4e6c7bc4a61971a6d1ca6db72250f41791252a28b7f7568a561700', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_002176_COMMIT.json': '8d5510f630045da4227e832eb9203f7ff4ea970d975c957ff1a9dbbd32888c80', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_003456.npz': 'd33e0a8757722fc4bb9ae8bd31e4f05438b9ba23916c452cc3ce885d0f85e701', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_003456_COMMIT.json': '94df268d12ed16a3e7405316fb17b7adfcc770c76f7ec4b3e6f8126800e5fef0', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_004096.npz': 'b8db09fdcab4748c3058284172e24429dcd43ce0eca5ac469b8172795e105996', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_004096_COMMIT.json': '9b09b372f7ac715482dd28d4208478f73f9b21beb024a45bdeed53e03a9abd46', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_000000.npz': '843943bb7d8929eaf4990e898cae470b36e32051a4417e3a2ca5a4aed7880bbb', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_000000_COMMIT.json': 'f44d86a1a67f9613d8a7e3d67fd1f9cdc1c8c3de93a59a6d1a67567a2365359b', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_002176.npz': 'c9c0829740c99a7c5e92c74c1baa507951e01d6bca3097bd40449ad91003e898', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_002176_COMMIT.json': '292578f9496297313ff97619836b3dc88c1fd629d9993f754f6966e1f9d1e48f', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_003456.npz': '84e49cfb02d7636794e8aade78141d6a750796f1a5c0c554e66a770967df8e6a', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_003456_COMMIT.json': '78553338f12a092186e077531b6b98c7ad6aaee82de4009c52d266e41626322a', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_004096.npz': 'd17bd6572bc6c9516b9bcaf5847af8ebe0885a5822380430541a6a466f6edc05', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_004096_COMMIT.json': '19102a33ba64616be65886d0ca7071610987d588e33ee0b57ed76f868f8b957e', 'cross_u_full_flrw_row_trace_time_diagnostic_v001.py': 'e34e0abd28265b4d5ba11b0f823a4a626ba855ba0dea1cf5353ecf7a3cf7021c', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001.md': '6659c18b3277c9cef21ab74c15e92b0a7a676331e5bc2365c9ed16848ce4d5a9', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_RECEIPT.json': 'ddb6db2c2b64ebe3f03eb49fbaca6e5d2143a7e3d8c27c3126315cdef37cea55', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_ERROR.json': '76887a5aa992899b05b319e46186e03998d5e874f276941bf6d1deaec115311d', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_MANIFEST.json': '0f5d9e93700394dbb5de14737b56b01124a9a4ea2a1a8e16cfc5af1afdac9548', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_028_REFUSED.npz': '6f86018f37cf196388292f8334fecc573fcec27756c3789d6e7da409ab591b8b', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_028_REFUSED.npz.COMMIT.json': 'c292b2c8441eaa36888285939cb47b8effc808de2ba41fd06a9c6a5e64f85ddb', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_TRACE_FINE_K1_O0_CASE.json': '3507555a03e53fb58bcea056c0c73529ef5f2760587ca7e9a2d44f85eff28cb1', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_RADIATION_FINE_K1_O0_CASE.json': 'b3849a072aa01cbf17542e915c6a76ed370722ce70506f0c61b4c8fb4cf5116f', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_TRACE_FINE_K1_O1_CASE.json': 'd73e1ba22451aa644c04aef332c9ac5423c2d05576c8907bfa86b9221e3fb29b', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_RADIATION_FINE_K1_O1_CASE.json': '65b4c4f2fbb3f5dc0d1bcae9b62cd20f1eea5d9dd5a4bdf3af7d4e974eb527a3', 'CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V001_TRACE_FINE_K1_O2_CASE.json': '4224e050c5d0a0526f207c71799ced238b735179fb2a2879a896d8f689391339', 'reviewed_cross_u_full_flrw_row_trace_time_diagnostic_v002_371_eb621255.py': 'eb6212555125c5588d93d35ec45699fd6219f79ae07241096aff7865180571a9', 'reviewed_CROSS_U_FULL_FLRW_ROW_TRACE_TIME_DIAGNOSTIC_V002_19_dded1ee3.md': 'dded1ee3b85a85d6e2e4b06797c38a4e5c90073ca22eeb5790b31c2e3e072c5b'}
HELPER_SPANS={'bg': '9b1ab946ffe194f9bcddba16db78efe37ae2eb6ccc88ec47f12c53e1bd1480b4', 'legendre': '671e20cd8fe47819e23ccd8c2630c4625427fad284b8f6e175d50fcbc3178c2b', 'layout': 'd0bb5af30d66aea5a3fe46973bed4794f105ac4fa2258fe9dab723b6fbcdd666', 'equilibrated_solve': '44de3a9f06e518e6c8d9fcf523ebc60955917e519e94cfcccf8277574ab91dcb', 'phase_nodes': '776ba8b11d9cc0045a46fa2ae56e5706ff4983333192be23e6e24e455dc1389a', 'radiation_weights': '1638e5d3a9720d8859764796aac05cdbc03508db8d484f24771f235409ff13fe', 'radiation_map': '74ac265694702b9e63e2eba5e203f8df2c92b60d2125b31363f79978b704e3dd', 'rate_matrix': '9105eae6adf8501c617e2444c76625b56ec97dc4bab03802f447d5d962dd9da2', 'native_map': '4c1a95c744613d8d0f6299f5d9171279f9b9176478a8ce66afbc04b501ce1f17', 'panel_step': '0b720cf76986cc68579fabd4fba399f8e8f77d6f8d33dd2b6ab587bc5869a7f5', 'original': 'b1b6beface6fd23010de1b7a5440b5d2be5405d9fefe6e98fecfdc3162e675c7', 'metric_increment': '2f287109e8f9944c289d6052e79b735398b7257828b3ef548686604bc8fbba5c'}
TARGETS=[{'group': 'trace', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O0', 'ns': 32, 'nstep': 4096, 'omega': 0.1}, 'target_step': 2235, 'start_step': 2176, 'recorded_maximum': {'a': 0.12339813437242188, 'error': 6.21485697744202e-11, 'nstep': 2235}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_002176.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_002176_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_004096_COMMIT.json'}}, {'group': 'radiation', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O0', 'ns': 32, 'nstep': 4096, 'omega': 0.1}, 'target_step': 3475, 'start_step': 3456, 'recorded_maximum': {'a': 0.4974819680632731, 'error': 4.330052524553588e-05, 'nstep': 3475}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_003456.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_003456_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_004096_COMMIT.json'}}, {'group': 'trace', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O1', 'ns': 32, 'nstep': 4096, 'omega': 1.0}, 'target_step': 2235, 'start_step': 2176, 'recorded_maximum': {'a': 0.12339813437242188, 'error': 6.214632687409076e-11, 'nstep': 2235}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_002176.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_002176_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_004096_COMMIT.json'}}, {'group': 'radiation', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O1', 'ns': 32, 'nstep': 4096, 'omega': 1.0}, 'target_step': 3475, 'start_step': 3456, 'recorded_maximum': {'a': 0.4974819680632731, 'error': 4.330052572139095e-05, 'nstep': 3475}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_003456.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_003456_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_004096_COMMIT.json'}}, {'group': 'trace', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O2', 'ns': 32, 'nstep': 4096, 'omega': 10.0}, 'target_step': 2235, 'start_step': 2176, 'recorded_maximum': {'a': 0.12339813437242188, 'error': 6.204543368201336e-11, 'nstep': 2235}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_002176.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_002176_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_004096_COMMIT.json'}}, {'group': 'radiation', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O2', 'ns': 32, 'nstep': 4096, 'omega': 10.0}, 'target_step': 3475, 'start_step': 3456, 'recorded_maximum': {'a': 0.4974819680632731, 'error': 4.330056599093413e-05, 'nstep': 3475}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_003456.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_003456_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_004096_COMMIT.json'}}, {'group': 'trace', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O3', 'ns': 32, 'nstep': 4096, 'omega': 100.0}, 'target_step': 2235, 'start_step': 2176, 'recorded_maximum': {'a': 0.12339813437242188, 'error': 5.6707034420657606e-11, 'nstep': 2235}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_002176.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_002176_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_004096_COMMIT.json'}}, {'group': 'radiation', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O3', 'ns': 32, 'nstep': 4096, 'omega': 100.0}, 'target_step': 3475, 'start_step': 3456, 'recorded_maximum': {'a': 0.4974819680632731, 'error': 4.3300698286853574e-05, 'nstep': 3475}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_003456.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_003456_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_004096_COMMIT.json'}}]
INITIALS=[{'group': 'initial', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O0', 'ns': 32, 'nstep': 4096, 'omega': 0.1}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_000000_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O0_CP_004096_COMMIT.json'}, 'recorded_normal_maximum': {'a': 0.010002376227028327, 'error': 1.2072746688377474e-06, 'nstep': 1}}, {'group': 'initial', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O1', 'ns': 32, 'nstep': 4096, 'omega': 1.0}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_000000_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O1_CP_004096_COMMIT.json'}, 'recorded_normal_maximum': {'a': 0.010002376227028327, 'error': 1.2072746688377474e-06, 'nstep': 1}}, {'group': 'initial', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O2', 'ns': 32, 'nstep': 4096, 'omega': 10.0}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_000000_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O2_CP_004096_COMMIT.json'}, 'recorded_normal_maximum': {'a': 0.010002376227028327, 'error': 1.2072746688377474e-06, 'nstep': 1}}, {'group': 'initial', 'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O3', 'ns': 32, 'nstep': 4096, 'omega': 100.0}, 'start': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_000000_COMMIT.json'}, 'terminal': {'payload': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_004096.npz', 'commit': 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_FINE_K1_O3_CP_004096_COMMIT.json'}, 'recorded_normal_maximum': {'a': 0.010002376227028327, 'error': 1.2072746688377474e-06, 'nstep': 1}}]
INPUTS={};OUTPUTS={};RECORDS=[];CONTROLS=[];OWNER={};SOURCE_SHA=None;CONTEXT={}
COUNTS=dict(replay_attempted=0,candidate_attempted=0)
FAILURE_RAW={}
INHERITED_RECORDS=[]
class NumericalRefusal(ArithmeticError):pass
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def now():return datetime.now(timezone.utc).isoformat()

def finite(x):return float(x) if math.isfinite(float(x)) else None

def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
    if 'np' in globals() and isinstance(v,np.ndarray):return canonical(v.tolist())
    if 'np' in globals() and isinstance(v,np.generic):return canonical(v.item())
    if type(v) is float and not math.isfinite(v):raise ValueError('Nonfinite metadata; retain raw array with a null descriptor')
    if v is None or type(v) in (str,int,float,bool):return v
    raise TypeError(type(v).__name__)

def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def seal(name,h):
    p=(BASE/name).resolve()
    if not p.is_relative_to(BASE.parent) or sha(p)!=h:raise ValueError('Input seal '+name)
    if name in INPUTS and INPUTS[name]!=h:raise ValueError('Conflicting input '+name)
    INPUTS[name]=h

def recheck():
    for n,h in dict(INPUTS,**OUTPUTS).items():
        if sha(BASE/n)!=h:raise ValueError('Changed protected bytes '+n)
    if sha(__file__)!=SOURCE_SHA:raise ValueError('Changed own source')

def publish(name,v):
    raw=encode(v);p=BASE/name
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444)
    if p.read_bytes()!=raw:raise IOError('Exact JSON byte reread')
    OUTPUTS[name]=sha(p);return OUTPUTS[name]

def checkpoint(tag,arrays,metadata):
    schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}
    text=encode(dict(metadata,owner=OWNER,schema=schema)).decode();meta=json.loads(text)
    name=f'{STEM}_{len(RECORDS):03d}_{tag}.npz';p=BASE/name
    with p.open('xb') as f:np.savez_compressed(f,metadata=np.asarray(text),**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);OUTPUTS[name]=sha(p)
    rec=dict(file=name,sha256=OUTPUTS[name],metadata=meta)
    commit=name+'.COMMIT.json';ch=publish(commit,rec);rec=dict(rec,commit_file=commit,commit_sha256=ch);RECORDS.append(rec)
    with np.load(p,allow_pickle=False) as n:
        if set(n.files)!=set(arrays)|{'metadata'} or str(n['metadata'])!=text:raise ValueError('Own NPZ full schema')
        for k,v in arrays.items():
            if not np.array_equal(n[k],v,equal_nan=True):raise ValueError('Own NPZ raw array '+k)
    return rec

def full_reread():
    for rec in RECORDS:
        if json.loads((BASE/rec['commit_file']).read_text())!={k:rec[k] for k in ('file','sha256','metadata')}:raise ValueError('Exact own COMMIT record')
        with np.load(BASE/rec['file'],allow_pickle=False) as n:
            if json.loads(str(n['metadata']))!=rec['metadata'] or set(n.files)!={'metadata'}|set(rec['metadata']['schema']):raise ValueError('Exact own metadata/schema')
            for k,s in rec['metadata']['schema'].items():
                v=n[k]
                if list(v.shape)!=s['shape'] or str(v.dtype)!=s['dtype'] or bool(np.all(np.isfinite(v)))!=s['finite']:raise ValueError('Own shape/dtype/finite classification')
    if {r['file'] for r in RECORDS}!={p.name for p in BASE.glob(STEM+'_*.npz')} or {r['commit_file'] for r in RECORDS}!={p.name for p in BASE.glob(STEM+'_*.COMMIT.json')}:raise ValueError('Own exact pair census')

def exact_control(name,passed,context):
    item=dict(name=name,passed=bool(passed),context=context);CONTROLS.append(item)
    if not passed:raise ValueError('Exact arithmetic/provenance control '+name)
    return item

def closed_parent():
    for name,want in PINS.items():seal(name,want)
    seal(STEM+'.md',PROTOCOL_SHA);seal(str(Path(__file__).resolve()),SOURCE_SHA)
    receipt=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text());result=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());manifest=json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text())
    if receipt['owner']!='root' or receipt['pid']!=70938 or receipt['status']!='NUMERICAL_FAILED' or result['status']!=receipt['status'] or receipt['source_sha256']!=PINS[PARENT_SOURCE] or receipt['result_sha256']!=PINS[PARENT+'_RESULT.json'] or receipt['manifest_sha256']!=PINS[PARENT+'_MANIFEST.json'] or result['manifest']!=manifest:raise ValueError('Actual naturally closed repaired FINE parent')
    if receipt['checkpoint_pairs']!=265 or receipt['evolution_checkpoint_pairs']!=264 or receipt['zero_control_checkpoint_pairs']!=1 or receipt['predicate_count']!=137 or len(result['rows'])!=8 or len(result['controls'])!=137 or sum(c['passed'] for c in result['controls'])!=125:raise ValueError('Preserved full repaired parent census/dispositions')
    if manifest['owner']!='root' or manifest['pid']!=receipt['pid'] or manifest['source_sha256']!=PINS[PARENT_SOURCE] or manifest['ai']!=.01 or manifest['af']!=1. or manifest['correction_cap']!=CORRECTIONS or manifest['prospective_tolerances']['rows']!=ROW_GATE:raise ValueError('Same physical fixture and solver limits')
    pending=[receipt];seen=set()
    while pending:
        rc=pending.pop()
        for kind in ('input_sha256','output_sha256'):
            for name,want in rc.get(kind,{}).items():
                seal(name,want);p=(BASE/name).resolve()
                if p.name.endswith('_RECEIPT.json') and p not in seen:
                    seen.add(p);pending.append(json.loads(p.read_text()))
    if result['physical_flags']!=manifest['physical_flags'] or result['qualification']!=manifest['physical_flags'] or any(manifest['physical_flags'].values()):raise ValueError('Every physical qualification remains false')
    selected={v['trial']['name']:v for v in result['rows'] if v['trial']['k']==.1}
    if set(selected)!={v['trial']['name'] for v in INITIALS}:raise ValueError('Exactly four k=.1 frequency families')
    for target in TARGETS:
        row=selected[target['trial']['name']];key='trace_error' if target['group']=='trace' else 'radiation_density'
        if row['trial']!=target['trial'] or row['maxima'][key]!=target['recorded_maximum'] or row['terminal_checkpoint']!=target['terminal']['payload'] or target['start_step']!=((target['target_step']-1)//128)*128:raise ValueError('Prebound actual first attaining local target')
    if sum(t['target_step']-t['start_step'] for t in TARGETS)!=312 or len(TARGETS)!=8 or len(INITIALS)!=4:raise ValueError('Fixed bounded target census')
    return result,manifest

def failed_parent():
    rc=json.loads((BASE/(FAILED+'_RECEIPT.json')).read_text());error=json.loads((BASE/(FAILED+'_ERROR.json')).read_text());mf=json.loads((BASE/(FAILED+'_MANIFEST.json')).read_text())
    if rc['status']!='ERROR' or rc['checkpoint_pairs']!=29 or len(rc['output_sha256'])!=65 or rc['owner']!=mf['owner'] or rc['owner']!=error['owner'] or rc['owner']['owner']!='root' or rc['owner']['pid']!=72754 or rc['source_sha256']!=PINS['cross_u_full_flrw_row_trace_time_diagnostic_v001.py']:raise ValueError('Actual closed failed diagnostic owner/census')
    if rc['input_sha256']!=error['input_sha256'] or rc['input_sha256']!=mf['input_sha256'] or set(rc['output_sha256'])!=set(error['output_sha256'])|{FAILED+'_ERROR.json'}:raise ValueError('Exact failed diagnostic full maps')
    if error['context']!=dict(group='radiation',trial='FINE_K1_O2',nstep=3475) or error['type']!='ValueError' or error['message']!='Exact arithmetic/provenance control baseline_maximum_radiation_FINE_K1_O2':raise ValueError('Exact original refusal point')
    if any(mf['qualification'].values()) or mf['qualification']!=error['qualification'] or rc['closed']<=rc['owner']['started']:raise ValueError('Preserved qualification/closure')
    for kind in ('input_sha256','output_sha256'):
        for name,h in rc[kind].items():seal(name,h)
    if {p.name for p in BASE.glob(FAILED+'_*')}!=set(rc['output_sha256'])|{FAILED+'_RECEIPT.json'}:raise ValueError('Original failed namespace exact set')
    records=[]
    for name in sorted(n for n in rc['output_sha256'] if n.endswith('.COMMIT.json')):
        r=json.loads((BASE/name).read_text())
        if set(r)!={'file','sha256','metadata'} or r['file']+'.COMMIT.json'!=name or rc['output_sha256'][r['file']]!=r['sha256'] or r['metadata']['owner']!=rc['owner']:raise ValueError('Original full COMMIT dictionary')
        records.append(dict(r,commit_file=name,commit_sha256=rc['output_sha256'][name]))
    if len(records)!=29 or records[-1]['file']!=REFUSED_FILE:raise ValueError('Original exact pair order')
    return rc,error,mf,records

def read_failed(record,scratch):
    with np.load(BASE/record['file'],allow_pickle=False) as z:
        arrays={k:z[k].copy() for k in z.files if k!='metadata'}
        scratch.update({'failed_'+k:v for k,v in arrays.items()});FAILURE_RAW.update(scratch)
        actual=json.loads(str(z['metadata']))
    if actual!=record['metadata'] or set(arrays)!=set(actual['schema']):raise ValueError('Original full saved schema')
    for k,v in arrays.items():
        if actual['schema'][k]!=dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) or not np.all(np.isfinite(v)):raise ValueError('Original saved array classification '+k)
    return arrays

def inherited_cases(records,parent,mf):
    copied=[];byfile={r['file']:r for r in records}
    for name in COPIED_CASE_FILES:
        case=json.loads((BASE/name).read_text());t=case['target'];key='trace_error' if t['group']=='trace' else 'radiation_density'
        if case['status']!='DIAGNOSTIC_COMPLETE' or not case['parent_failures_unchanged'] or case['qualification']!=mf['qualification']:raise ValueError('Exact complete inherited case')
        expected=[r for r in records if r['metadata']['target']==t]
        if case['own_checkpoints']!=expected:raise ValueError('Exact inherited case checkpoint membership')
        snapshots={}
        for rec in expected:snapshots[rec['file']]=read_failed(rec,{})
        base=case['baseline'];bm=base['metadata']['baseline'];tm=json.loads((BASE/t['terminal']['commit']).read_text())['metadata']
        ctx=dict(target=t,provenance='Saved serialized operands only; no inherited panel replay',source_case=name,source_case_sha256=PINS[name])
        exact_control('inherited_baseline_history_'+t['group']+'_'+t['trial']['name'],bm['solver_history']==tm['solver_history'][:t['target_step']],ctx)
        observed=bm['summary']['trace_error'] if t['group']=='trace' else bm['local_increments']['radiation_density']
        exact_control('inherited_baseline_maximum_'+t['group']+'_'+t['trial']['name'],observed==t['recorded_maximum']['error'],ctx)
        candidate=case['candidates'][0]['panels'][0]['checkpoint'];aa=snapshots[base['file']];bb=snapshots[candidate['file']]
        exact_control('inherited_same_original_matrix_'+t['group']+'_'+t['trial']['name'],np.array_equal(aa['raw_core_matrix'],bb['raw_core_matrix']) and np.array_equal(aa['raw_core_rhs'],bb['raw_core_rhs']),ctx)
        if any(byfile[r['file']]!=r for r in expected):raise ValueError('Inherited unchanged record closure')
        copied.append(case);FAILURE_RAW.clear()
    if len(copied)!=5 or len(CONTROLS)!=15:raise ValueError('Inherited fixed control/case census')
    used={r['file'] for c in copied for r in c['own_checkpoints']}
    for record in records:
        if record['file'] not in used:read_failed(record,{});FAILURE_RAW.clear()
    return copied

def load_environment(fixed):
    text=(BASE/PARENT_SOURCE).read_text();tree=ast.parse(text);lines=text.splitlines();defs=[]
    for node in tree.body:
        if isinstance(node,ast.FunctionDef) and node.name in HELPER_SPANS:
            span='\n'.join(lines[node.lineno-1:node.end_lineno])+'\n'
            if hashlib.sha256(span.encode()).hexdigest()!=HELPER_SPANS[node.name]:raise ValueError('Unchanged helper span '+node.name)
            defs.append(node)
    if len(defs)!=12:raise ValueError('Exact twelve original helper definitions')
    env=dict(np=np,math=math,CP=299792.458,KB=.02,C=1.98,KBL=.01,CL=.99,FLOOR=1e-13,RAW={},CORE_HISTORY=[],CONTEXT={},ROW_TOL=ROW_GATE,CORRECTION_CAP=CORRECTIONS,fixed_for_domain=fixed)
    exec(compile(ast.Module(body=defs,type_ignores=[]),str(BASE/PARENT_SOURCE),'exec'),env)
    p=BASE/'constrained_u_shared_eps_ngc_pantheon_v001.py';text=p.read_text();node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='background');span='\n'.join(text.splitlines()[node.lineno-1:node.end_lineno])+'\n'
    if hashlib.sha256(span.encode()).hexdigest()!='8881f1df923d053d1d4b7ce06bfe4a50e856a62b49a25546a8d7e7a0d9f12bf2':raise ValueError('Literal unchanged physical background')
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(p),'exec'),env)
    return env

def admitted(target,manifest,scratch):
    files=target['start'];cp=json.loads((BASE/files['commit']).read_text());meta=cp['metadata'];trial=target['trial'];step=target.get('start_step',0)
    expected=dict(schema=1,trial=trial['name'],nstep=step,failed=False,payload=files['payload'],payload_sha256=PINS[files['payload']],metadata=meta,owner='root',pid=manifest['pid'],source_sha256=PINS[PARENT_SOURCE],manifest_sha256=PINS[PARENT+'_MANIFEST.json'])
    if cp!=expected:raise ValueError('Exact admitted immutable COMMIT')
    with np.load(BASE/files['payload'],allow_pickle=False) as n:
        arrays={k:n[k].copy() for k in n.files if k!='metadata'};scratch.update({'admitted_'+k:v for k,v in arrays.items()});actual=json.loads(str(n['metadata']))
    keys={'schema','trial','nstep','x','frames','maxima','input_sha256','layout','columns','physical_flags','solver_history'}
    if actual!=meta or set(meta)!=keys or meta['schema']!=1 or meta['trial']!=trial or meta['nstep']!=step or meta['input_sha256']!=manifest['input_sha256'] or meta['physical_flags']!=manifest['physical_flags'] or meta['columns']!=['metric','common_velocity'] or len(meta['solver_history'])!=step:raise ValueError('Complete admitted metadata/history')
    frames=step//128+1;nst=0 if step==0 else 3;shapes=dict(core=(11,2),native=(48,2,2),angular=(81,2),frame_core=(frames,11,2),frame_native=(frames,48,2,2),frame_angular=(frames,81,2),last_stage_core=(nst,11,2),last_stage_native=(nst,48,2,2),last_stage_angular=(nst,81,2))
    if set(arrays)!=set(shapes) or [v['nstep'] for v in meta['frames']]!=list(range(0,step+1,128)) or meta['x']!=math.log(manifest['ai'])+step*((math.log(manifest['af'])-math.log(manifest['ai']))/4096):raise ValueError('Exact admitted full-state/frame chart')
    for key,value in arrays.items():
        if value.shape!=shapes[key] or value.dtype!=np.dtype('complex128' if 'angular' in key else 'float64') or not np.all(np.isfinite(value)):raise ValueError('Admitted shape/dtype/finite '+key)
    if any(not np.array_equal(arrays['frame_'+k][-1],arrays[k]) for k in ('core','native','angular')) or (nst and any(not np.array_equal(arrays['last_stage_'+k][-1],arrays[k]) for k in ('core','native','angular'))):raise ValueError('Full last-state/stage identity')
    terminal=json.loads((BASE/target['terminal']['commit']).read_text())
    if terminal['payload']!=target['terminal']['payload'] or terminal['payload_sha256']!=PINS[target['terminal']['payload']] or terminal['metadata']['trial']!=trial or terminal['nstep']!=4096 or terminal['failed'] or terminal['source_sha256']!=PINS[PARENT_SOURCE] or terminal['manifest_sha256']!=PINS[PARENT+'_MANIFEST.json']:raise ValueError('Bound terminal history')
    terminal_meta=terminal['metadata'];terminal_expected=dict(schema=1,trial=trial['name'],nstep=4096,failed=False,payload=target['terminal']['payload'],payload_sha256=PINS[target['terminal']['payload']],metadata=terminal_meta,owner='root',pid=manifest['pid'],source_sha256=PINS[PARENT_SOURCE],manifest_sha256=PINS[PARENT+'_MANIFEST.json'])
    if terminal!=terminal_expected:raise ValueError('Complete exact terminal COMMIT')
    history=terminal_meta['solver_history']
    if len(history)!=4096 or history[:step]!=meta['solver_history']:raise ValueError('Immutable baseline history prefix')
    return meta,arrays,history

def snapshot_summary(env,nodes,natives,angles,bgs,lay,scratch):
    ss=[]
    for i in range(3):
        snap=env['original'](nodes[i],natives[i],angles[i],bgs[i+1],lay);ss.append(snap)
        for key,value in snap.items():
            if isinstance(value,np.ndarray):scratch['stage'+str(i)+'_'+key]=value.copy()
        scratch['stage'+str(i)+'_trace_envelope']=abs(snap['trace_terms']).sum(axis=0)
    summary={key:float(max(np.max(abs(snap[key])) for snap in ss)) for key in ('normal_error','trace_error','density_identity_error','momentum_identity_error')}
    summary.update(normal_absolute=float(max(np.max(abs(s['normal'])) for s in ss)),trace_absolute=float(max(np.max(abs(s['trace'])) for s in ss)),working_stop_reached=env['CORE_HISTORY'][-1]['final_error']<=WORKING_STOP,original_core_gate=env['CORE_HISTORY'][-1]['final_error']<=ROW_GATE,original_trace_gate=summary['trace_error']<=ROW_GATE)
    if not all(math.isfinite(v) for k,v in summary.items() if type(v) is float):raise NumericalRefusal('Nonfinite instantaneous diagnostic; raw nodes retained')
    return ss,summary

def take_panel(env,core,native,angular,x,dx,trial,manifest,lay,step,working,scratch):
    env['RAW'].clear();env['ROW_TOL']=working;env['CONTEXT']=dict(trial=trial['name'],nstep=step)
    scratch.update(left_core=core.copy(),left_native=native.copy(),left_angular=angular.copy())
    nodes,natives,angles,bgs,checks=env['panel_step'](core,native,angular,x,dx,trial['k'],manifest['fixed'],env['background'],lay)
    scratch.update({'raw_'+k:v.copy() for k,v in env['RAW'].items()});scratch.update(core_nodes=nodes.copy(),native_nodes=natives.copy(),angular_nodes=angles.copy())
    ss,summary=snapshot_summary(env,nodes,natives,angles,bgs,lay,scratch);summary['panel_checks']=checks
    return nodes,natives,angles,ss,summary

def window_increment(left,panels,dx,scratch):
    after=panels[-1][-1];specs=[('Psi','metric_momentum'),('delta_b','ordinary_density'),('d','phase_density'),('delta_r','radiation_density'),('S','proper_trace_increment'),('E','whole_density_increment')];summary={}
    for key,name in specs:
        values=[]
        for snapshots in panels:
            for z in snapshots[:2]:
                g=z['background']
                if key=='S':source=g['B']*z['Phi']+z['pressure']-2*g['r']*z['F'][2]/3
                elif key=='E':source=-3*g['h']*z['pressure']+3*g['B']*z['Psi_dot']-g['q']**2*z['S']
                else:source=z[{'Psi':'Psi_dot','delta_b':'delta_b_dot','d':'d_dot','delta_r':'delta_r_dot'}[key]]
                values.append((z['a']**3 if key in ('S','E') else 1)*source/g['h']*dx/2)
        terms=np.asarray(values);l=(left['a']**3 if key in ('S','E') else 1)*left[key];r=(after['a']**3 if key in ('S','E') else 1)*after[key];res=r-l-terms.sum(axis=0);envelope=abs(l)+abs(r)+abs(terms).sum(axis=0);floor=1e-13*(left['a']**3 if key in ('S','E') else 1);relative=abs(res)/np.maximum(envelope,floor)
        scratch.update({name+'_left':np.asarray(l).copy(),name+'_right':np.asarray(r).copy(),name+'_source_terms':terms.copy(),name+'_residual':res.copy(),name+'_envelope':envelope.copy(),name+'_relative':relative.copy()})
        error=float(np.max(relative))
        if not math.isfinite(error):raise NumericalRefusal('Nonfinite window diagnostic; raw increment arrays retained')
        summary[name]=dict(error=finite(error),original_gate=math.isfinite(error) and error<=INCREMENT_GATE,absolute_max=finite(np.max(abs(res))))
    return summary

def candidates(target,left,lay,manifest,parent,baseline=None):
    records=[];trial=target['trial'];grid=target.get('grid_sizes');sizes=grid if grid else ([1] if target['group']=='trace' else [1,2,4]);baseline_raw=baseline
    for size in sizes:
        env=load_environment(manifest['fixed']);env['CORE_HISTORY']=[];core,native,angular=(left[k].copy() for k in ('core','native','angular'));x0=math.log(manifest['ai']);original_dx=(math.log(manifest['af'])-math.log(manifest['ai']))/4096
        x=x0 if grid else x0+(target['target_step']-1)*original_dx;dx=(math.log(manifest['af'])-math.log(manifest['ai']))/size if grid else original_dx/size;count=1 if grid else size;snaps=[];row=[]
        left_clock=x if grid else (x0+(target['target_step']-2)*original_dx)+original_dx
        first=env['original'](core,native,angular,env['bg'](left_clock,trial['k'],manifest['fixed'],env['background']),lay)
        for i in range(count):
            scratch=dict(input_core=core.copy(),input_native=native.copy(),input_angular=angular.copy());CONTEXT.update(candidate_size=size,subpanel=i+1)
            try:
                COUNTS['candidate_attempted']+=1
                nodes,natives,angles,ss,summary=take_panel(env,core,native,angular,x+i*dx,dx,trial,manifest,lay,target.get('target_step',1),WORKING_STOP,scratch)
                snaps.append(ss);summary['local_increments']=env['metric_increment'](first if i==0 else snaps[-2][-1],ss[:2],ss[-1],dx)
                if baseline_raw is not None and size==1:
                    exact_control('same_original_matrix_'+target['group']+'_'+trial['name'],np.array_equal(scratch['raw_core_matrix'],baseline_raw['raw_core_matrix']) and np.array_equal(scratch['raw_core_rhs'],baseline_raw['raw_core_rhs']),dict(target=target))
                increment=window_increment(first,snaps,dx,scratch)
                rec=checkpoint('CANDIDATE',scratch,dict(group=target['group'],trial=trial,target=target,candidate_size=size,subpanel=i+1,local_dx=dx,x=x+i*dx,summary=summary,stage_snapshots=ss,whole_candidate_window=increment,solver_history=copy.deepcopy(env['CORE_HISTORY']),unaccepted=True,scope='Original equations and thresholds; tighter working stop/local subdivision only'))
                row.append(dict(checkpoint=rec,summary=summary,whole_window=increment));core,native,angular=nodes[-1].copy(),natives[-1].copy(),angles[-1].copy()
            except Exception as exc:
                scratch.update({'available_raw_'+k:v for k,v in env['RAW'].items()});checkpoint('CANDIDATE_REFUSED',scratch,dict(target=target,context=CONTEXT,type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc(),unaccepted=True));raise
        records.append(dict(size=size,panel_count=count,panels=row,final_window=row[-1]['whole_window'],maxima={k:max(z['summary'][k] for z in row) for k in ('normal_error','trace_error','density_identity_error','momentum_identity_error','normal_absolute','trace_absolute')}))
    return records

def descriptive_scaling(answers):
    rows=[]
    for old,new in zip(answers,answers[1:]):
        ratio=new['size']/old['size'];fields={k:(old['maxima'][k],new['maxima'][k]) for k in old['maxima']}
        fields.update({'window_'+k:(old['final_window'][k]['error'],new['final_window'][k]['error']) for k in old['final_window']})
        for key,(a,b) in fields.items():
            valid=a is not None and b is not None and a>0 and b>0 and math.isfinite(a) and math.isfinite(b)
            rows.append(dict(field=key,old_size=old['size'],new_size=new['size'],old_error=a,new_error=b,error_ratio=finite(a/b) if valid else None,apparent_order=finite((math.log(a)-math.log(b))/math.log(ratio)) if valid else None,reason=None if valid else 'Nonpositive or nonfinite error; descriptive order undefined'))
    return rows

def one_case(target,manifest,parent,recovered=None):
    global CONTEXT
    first=len(RECORDS);scratch={};env=None;replayed=0;CONTEXT=dict(group=target['group'],trial=target['trial']['name']);case={}
    try:
        env=load_environment(manifest['fixed']);lay=env['layout'](32,64,target['trial']['omega'])
        if recovered is None:
            meta,arrays,history=admitted(target,manifest,scratch)
            if meta['layout']!=canonical(dict(nodes=lay['nodes'],weights=lay['weights'],mu=lay['mu'],weight_sum=lay['weight_sum'])):raise ValueError('Original quadrature registration')
            checkpoint('INPUT',scratch,dict(target=target,parent_metadata=meta,unaccepted=False,scope='Byte-bound saved input only'))
        else:
            saved=read_failed(recovered,scratch);md=recovered['metadata']
            if md['target']!=target or md['type']!='ValueError' or md['message']!='Exact arithmetic/provenance control baseline_maximum_radiation_FINE_K1_O2' or not md['unaccepted']:raise ValueError('Exact recovered refused target')
            arrays={k:saved['left_'+k].copy() for k in ('core','native','angular')}
            shapes=dict(core=(11,2),native=(48,2,2),angular=(81,2))
            if any(arrays[k].shape!=shapes[k] for k in arrays):raise ValueError('Complete recovered left-state dimensions')
            history=json.loads((BASE/target['terminal']['commit']).read_text())['metadata']['solver_history'];meta=dict(solver_history=history[:target['target_step']-1])
            checkpoint('INPUT',scratch,dict(target=target,refused_record=recovered,parent_history_prefix_copied_not_replayed=True,unaccepted=False))
        if target['group']=='initial':
            answers=candidates(dict(target,grid_sizes=[4096,8192,16384]),arrays,lay,manifest,parent)
        else:
            env['CORE_HISTORY']=copy.deepcopy(meta['solver_history']);core,native,angular=(arrays[k].copy() for k in ('core','native','angular'));x0=math.log(manifest['ai']);dx=(math.log(manifest['af'])-math.log(manifest['ai']))/4096
            firststep=target['target_step'] if recovered is not None else target['start_step']+1
            # Preserve the actual previous panel's endpoint arithmetic, not an independently rounded equivalent.
            bx=x0 if firststep==1 else (x0+(firststep-2)*dx)+dx
            before=env['original'](core,native,angular,env['bg'](bx,.1,manifest['fixed'],env['background']),lay)
            for step in range(firststep,target['target_step']+1):
                CONTEXT.update(nstep=step);scratch={};left=dict(core=core.copy(),native=native.copy(),angular=angular.copy())
                COUNTS['replay_attempted']+=1
                nodes,natives,angles,ss,summary=take_panel(env,core,native,angular,x0+(step-1)*dx,dx,target['trial'],manifest,lay,step,ROW_GATE,scratch);replayed+=1
                core,native,angular=nodes[-1].copy(),natives[-1].copy(),angles[-1].copy()
                if step<target['target_step']:before=ss[-1]
            if recovered is None:
                exact_control('baseline_history_'+target['group']+'_'+target['trial']['name'],env['CORE_HISTORY']==history[:target['target_step']],dict(target=target,provenance='Authenticated start history plus unchanged newly replayed prefix'))
            else:
                for key,actual in [('core_nodes',nodes),('native_nodes',natives),('angular_nodes',angles),('raw_core_matrix',scratch['raw_core_matrix']),('raw_core_rhs',scratch['raw_core_rhs'])]:
                    if not np.array_equal(saved[key],actual):raise ValueError('Recovered original target bit equality '+key)
                exact_control('recovered_last_panel_history_'+target['trial']['name'],env['CORE_HISTORY'][-1]==history[target['target_step']-1],dict(target=target,provenance='Only newly reproduced target record checked; preceding prefix is copied, not replay-certified'))
            local=env['metric_increment'](before,ss[:2],ss[-1],dx);observed=summary['trace_error'] if target['group']=='trace' else local['radiation_density']
            exact_control('baseline_maximum_'+target['group']+'_'+target['trial']['name'],observed==target['recorded_maximum']['error'],dict(target=target,observed=observed,carried_endpoint_clock=True))
            baseline_summary=dict(summary=summary,local_increments=local,solver_history=copy.deepcopy(env['CORE_HISTORY']),stage_snapshots=ss,history_provenance='Only last target record replayed; earlier prefix copied' if recovered is not None else 'Authenticated start prefix plus unchanged replay')
            baseline=checkpoint('BASELINE',scratch,dict(target=target,replayed_panels=replayed,baseline=baseline_summary,unaccepted=False,original_clock_expression=bx,direct_left_clock_expression=x0+(firststep-1)*dx,clock_expression_difference=finite(bx-(x0+(firststep-1)*dx)),refused_source=recovered,scope='Unchanged local replay with original carried endpoint clock; no new full trajectory'))
            answers=candidates(target,left,lay,manifest,parent,scratch)
        case=dict(status='DIAGNOSTIC_COMPLETE',target=target,replayed_panels=replayed,candidates=answers,descriptive_scaling=descriptive_scaling(answers),baseline=baseline if target['group']!='initial' else None,own_checkpoints=copy.deepcopy(RECORDS[first:]),qualification=manifest['physical_flags'],parent_failures_unchanged=True,recovered_refused_record=recovered)
    except Exception as exc:
        if env is not None:scratch.update({'refusal_raw_'+k:v for k,v in env['RAW'].items()})
        checkpoint('REFUSED',scratch,dict(target=target,context=CONTEXT,type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc(),unaccepted=True))
        if not isinstance(exc,(NumericalRefusal,ArithmeticError,np.linalg.LinAlgError)):raise
        case=dict(status='REFUSAL_RETAINED',target=target,replayed_panels=replayed,own_checkpoints=copy.deepcopy(RECORDS[first:]),type=type(exc).__name__,message=str(exc),qualification=manifest['physical_flags'],parent_failures_unchanged=True)
    publish(STEM+'_'+target['group'].upper()+'_'+target['trial']['name']+'_CASE.json',case);return case

def main():
    global np,SOURCE_SHA,OWNER,INHERITED_RECORDS
    if AUTHOR_GUARD:raise RuntimeError('Guarded author draft; independent review and root freeze required')
    if list(BASE.glob(STEM+'_*')):raise FileExistsError('Unused namespace; no resume or prefix overwrite')
    SOURCE_SHA=sha(__file__);tick=time.monotonic();parent,manifest=closed_parent();failed_rc,failed_error,failed_manifest,INHERITED_RECORDS=failed_parent();OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=SOURCE_SHA);mh=None;cases=[];copied=[]
    try:
        remaining=[t for t in TARGETS if t['trial']['name']=='FINE_K1_O3'];recovered_target=next(t for t in TARGETS if t['group']=='radiation' and t['trial']['name']=='FINE_K1_O2')
        mh=publish(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,parent_manifest=manifest,failed_receipt_sha256=PINS[FAILED+'_RECEIPT.json'],failed_manifest=failed_manifest,copied_case_files=COPIED_CASE_FILES,recovered_target=recovered_target,remaining_targets=remaining,initials=INITIALS,max_replay_panels=79,max_candidate_panels=27,working_stop=WORKING_STOP,original_row_gate=ROW_GATE,original_increment_gate=INCREMENT_GATE,correction_cap=CORRECTIONS,qualification=manifest['physical_flags']))
        for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[name]='1'
        import numpy as np
        if np.__version__!=manifest['numpy_version']:raise ValueError('Same NumPy float64 runtime')
        copied=inherited_cases(INHERITED_RECORDS,parent,failed_manifest)
        recovered=next(r for r in INHERITED_RECORDS if r['file']==REFUSED_FILE)
        cases.append(one_case(recovered_target,manifest,parent,recovered))
        for target in remaining+INITIALS:cases.append(one_case(target,manifest,parent))
        completed=all(c['status']=='DIAGNOSTIC_COMPLETE' for c in cases);replay=sum(c['replayed_panels'] for c in cases);panels=sum(a['panel_count'] for c in cases for a in c.get('candidates',[]))
        if len(cases)!=7 or len(copied)!=5 or COUNTS['replay_attempted']>79 or COUNTS['candidate_attempted']>27 or replay>79 or panels>27 or (completed and (replay!=79 or panels!=27 or len(CONTROLS)!=24 or len(RECORDS)!=37)):raise ValueError('Exact bounded recovery census')
        lookup={(c['target']['group'],c['target']['trial']['name']):c for c in copied+cases};coherent=[lookup[(t['group'],t['trial']['name'])] for t in TARGETS+INITIALS]
        inherited_success_pairs=[r for c in copied for r in c['own_checkpoints']]
        if len(inherited_success_pairs)!=27 or (completed and len(inherited_success_pairs)+len(RECORDS)!=64):raise ValueError('Exact coherent inherited/new pair census')
        full_reread();closed_parent();failed_parent();recheck();status='DIAGNOSTIC_COMPLETE' if completed else 'REFUSALS_RETAINED'
        result=dict(status=status,owner=OWNER,manifest_sha256=mh,cases=coherent,new_cases=cases,inherited_cases_copied_exactly=copied,inherited_success_checkpoint_records=inherited_success_pairs,controls=CONTROLS,replayed_panels=replay,candidate_panels=panels,attempted_panels=COUNTS,original_failure_copied_exactly=failed_error,parent_controls_copied_exactly=parent['controls'],parent_rows_copied_exactly=parent['rows'],original_parent_controls_copied_exactly=parent['original_parent_controls_copied_exactly'],original_parent_comparisons_copied_exactly=parent['original_parent_comparisons_copied_exactly'],qualification=manifest['physical_flags'],physical_flags=manifest['physical_flags'],elapsed_seconds=time.monotonic()-tick)
        rh=publish(STEM+'_RESULT.json',result);raw=('# Bounded row/trace/time V002 recovery\n\n'+status+'; five completed inherited cases unchanged, seven recovery cases.\n\nOriginal failures stay unchanged. Carried-clock roundoff recovery is not a physical state or full-history replacement. Corrected trace is algebraic rounding sensitivity; moving normal and radiation windows are distinct.\n').encode();rp=BASE/(STEM+'_REPORT.md')
        with rp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        rp.chmod(0o444)
        if rp.read_bytes()!=raw:raise IOError('Exact report byte reread')
        OUTPUTS[rp.name]=sha(rp);recheck();receipt=dict(status=status,owner=OWNER,closed=now(),source_sha256=SOURCE_SHA,manifest_sha256=mh,result_sha256=rh,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),checkpoint_pairs=len(RECORDS),coherent_success_pairs=len(inherited_success_pairs)+len(RECORDS),cases=12,new_cases=7,inherited_cases=5,controls=len(CONTROLS),replayed_panels=replay,candidate_panels=panels,attempted_panels=COUNTS)
        publish(STEM+'_RECEIPT.json',receipt)
        if json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())!=canonical(receipt):raise ValueError('Exact closed receipt reread')
        full_reread();closed_parent();failed_parent();recheck();print(status,rh,flush=True);return 0 if completed else 3
    except Exception as exc:
        existing=BASE/(STEM+'_RECEIPT.json')
        if FAILURE_RAW:checkpoint('ERROR_RAW',FAILURE_RAW,dict(context=CONTEXT,type=type(exc).__name__,message=str(exc),unaccepted=True))
        error=dict(owner=OWNER,time=now(),context=CONTEXT,type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=manifest['physical_flags'])
        if existing.exists():error['protected_existing_receipt_sha256']=sha(existing);OUTPUTS[existing.name]=sha(existing)
        publish(STEM+'_ERROR.json',error)
        if not existing.exists():publish(STEM+'_RECEIPT.json',dict(status='ERROR',owner=OWNER,closed=now(),source_sha256=SOURCE_SHA,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),checkpoint_pairs=len(RECORDS)))
        full_reread();recheck();raise

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--root-owned',action='store_true');args=parser.parse_args()
    if not args.root_owned:raise RuntimeError('Root-owned diagnostic only')
    raise SystemExit(main())
