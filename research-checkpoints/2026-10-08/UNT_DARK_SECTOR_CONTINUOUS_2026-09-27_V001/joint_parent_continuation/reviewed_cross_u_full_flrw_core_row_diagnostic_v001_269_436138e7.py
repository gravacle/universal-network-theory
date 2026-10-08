"""Guarded root-owned bounded diagnostic; no original FLRW trajectory or gate is changed."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,time,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_FULL_FLRW_CORE_ROW_DIAGNOSTIC_V001'
PARENT='CROSS_U_FULL_FLRW_FINITE_SLICE_V001'
PARENT_SOURCE='cross_u_full_flrw_source_constraint_v001.py'
AGGREGATE='CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001'
AUTHOR_GUARD=True
ROW_TOL=2e-11
CORRECTIONS=6
PROTOCOL_SHA='acbbcc5920d0a185b429aeefcc6382d298563a34bbf18c8c0e7eee10178a8ec1'
AGGREGATE_PINS={AGGREGATE+'_RESULT.json':'919bd3091cdda1f7616bd13f63a03c18d66cfe64a7ce68fdceb23f4cd0ab2d5f',AGGREGATE+'_REPORT.md':'166c2b3e95122a5619dca581424be3f8e48291f2b3e45c59af7227ac9cdee755',AGGREGATE+'_RECEIPT.json':'d70f6b6f6974522b896b0a4f389454c730c55ee55221096b199aa16003ed7082'}
PINS={'cross_u_full_flrw_source_constraint_v001.py': '8e2860917a75c44ada5be0df18ac43809dc7fe454846b3787d8a3d3017d1e5c1', 'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_V001.md': '4f2611f0fda44d326034aba5c38bcf532dc69e912f5f3d1d135f335975b5a5a6', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_MANIFEST.json': 'fba438e9df2246cbefa27f0b5226e41f435de8632e035d0660ed8f5bf3f6b77d', 'constrained_u_shared_eps_ngc_pantheon_v001.py': '03809b3c3798563725450bb4b7cf8c91654525ad874b6bc38e85da7c8cd22c52', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O0_CP_002048.npz': '8744b9256057753389feaa991160bc13293d27b0bca9e489ee5115a4dc7b5f41', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O0_CP_002048_COMMIT.json': '432fb060c8056cbc836b47a50f67d8be8472c730b8e69ae42187b4cb9f5f55b4', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O0_CP_001024.npz': '6be579b1ba8fcbb4a33121b153d6a34dcc82bf9ddd1786a17686ac7b5e9867f6', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O0_CP_001024_COMMIT.json': '0127cb26220177a1e6aef6daccdf6938fdad564e146fd1d26a63ef888bda5503', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O1_CP_002048.npz': '2d585e0493e2348cf7c0ab2b1b44fe0f85ca666df6d091924ec73b845c92242a', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O1_CP_002048_COMMIT.json': '75a4012338c77a8c51f7faec80a5692f6b378a632cf92ef675446d8683ae20f6', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O1_CP_000896.npz': '1752b6878b0192b44786c7eb4d573cf2743ef66a25065a4cb99cdae6334c7b70', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O1_CP_000896_COMMIT.json': '1ef467b4a540e0ff4dc49615c2ad77a43935d658a30053baa216c37c670b4f83', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O2_CP_002048.npz': '54be917fd39ad5f6a0fa79d0964a565cda003b741d9b366aa952fcf032a5fffd', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O2_CP_002048_COMMIT.json': 'c7e0a12343ec20bfaac56c502fbbc06d8cd7fde8e80c369702b95b9ca2abbe80', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O2_CP_001024.npz': 'ae3aed08fa8561e9466beb40ca7822d93982a6ab0b0a28644f4fc8a429d3289d', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O2_CP_001024_COMMIT.json': 'ae0a21220bd4e8934c7f993d68915e6163dfb0d2988af33c23790638d0e8778b', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O3_CP_002048.npz': '00c1e699fc56590a86c783b9176d151a923c53d65b38834c2ba2af46a8b20d46', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O3_CP_002048_COMMIT.json': 'f8d7629002d319c75a443ec52729d5a4ad56271e1855d2617dfd24a3385ad00c', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O3_CP_001408.npz': '4d1247c97806795aed32f9d2922759def00e10a54b37e9ea8ad2b8da8ce983ac', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O3_CP_001408_COMMIT.json': '924fc51b8190493ac258eaf828f59c49c503198d1d007b2a248cfadb63321fa7', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O0_CP_002048.npz': '11ac82c4bc67e9a687bc9983dd1895c3f6dfabf7489489c41e15408d7b17744d', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O0_CP_002048_COMMIT.json': 'af5f94b6a092ac0822b1effc505af2c835ee684dd9eb107627738bf3dc3ef46a', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O0_CP_000512.npz': 'fc8b02d769834bf795acb35ed8c934de5c86671dbf1d9a48a7b36a6723dd1fbb', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O0_CP_000512_COMMIT.json': '826b397c6fbc370bb1777d5273f19bafbe56cbc9626236ab6208d0ec2cf2b543', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O1_CP_002048.npz': '016932e90990f41bcc518a38a0eb216794c4f1383c860e7725f2eee2e7802128', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O1_CP_002048_COMMIT.json': '262bd5c031d304b5d76fca394c5d5c4c291a425cb886dec0ed516f0c8c0370f5', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O1_CP_000512.npz': '9e98658cc1d02d723ab5897c7c4904fbc2859aed01d2dadf33a3b27e7112b564', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O1_CP_000512_COMMIT.json': 'd2f7d1bed66bc5c9e5fdf97d17bb9ae3a443b0d4296d46b10748e08434192fd3', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O2_CP_002048.npz': '7791de4aa2d641b56ed17cafa7ab99835bbe43b8038355217f6f94088346ddb8', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O2_CP_002048_COMMIT.json': '6920d563fa715f53944cfe11b0ba7b25bf2b3526a00e98ff719b799d071928f8', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O2_CP_000512.npz': '075c722017b3d13c8ffd43ae98af8fde29cbe59a8c9143d1fe9b6ac498b3a059', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O2_CP_000512_COMMIT.json': '54f9f1dece1d8edc9c8c6402f2f4f2feda9e87568142ed69b00f0988546dbaa3', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O3_CP_002048.npz': '86582b976221688dde38a273878b8f66382d00e44ace06198a216ff0fa8fd7c3', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O3_CP_002048_COMMIT.json': 'bda0c5a6f548ec6f37b2bfee70aaa2f873e0805bfec9a94f2f1035426b8fd548', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O3_CP_000512.npz': '997f54cb1a095429f635d0d1e9cf08fbf921e267e761b3d66769c7fc21752799', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O3_CP_000512_COMMIT.json': 'f15bbcb815be47dc859f347319a8df6f5346322fef73687c8f80834764e1b6c9', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_004096.npz': 'd8a37714fed8e3fe8ddf15eb2b737d0e7ddffe363951318fba8ef4f39c1c93b0', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_004096_COMMIT.json': '35c575fef872e666eb8e8979880026eed850f305e8cc09d51c2810ef23fba404', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_002048.npz': '90fa088c6dc3985c3f1fbee8cd02d7aaefbb4fe57a6372396b8f127ae0cdc8c1', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_002048_COMMIT.json': 'd97eb213fcaaf76d82681391ea85437af7849faedb42f8dacf03cbdbc2854c95', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_004096.npz': '89d8ea254345cbe7d9d924da10d296d908e4cfc3e72b255a4898126589b6f830', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_004096_COMMIT.json': '7a19e0e0196551237ee8f3f0b7fc952f82e01890cb572fbb91c1783e6a993931', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_002048.npz': '66345d1975654ad1b0dd082843e7dd6eea7725e69384b1d0c0d5f0932e9b99fd', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_002048_COMMIT.json': 'a425406f1a332e4fd44f5c5dfd41706f71ba22a46836b3f1d0a9aa188cd260af', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_004096.npz': '2b718ba1612a6033b26a4c2618267e263f95403c0f2a7fe80326114d811d1733', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_004096_COMMIT.json': 'a697e06c974f4b0f373708e11a186a8da1dab15b8b1dc6964916089ba71dceae', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_001920.npz': 'b5b77ca10d66cff751ad1c1e8017f55cacf214f11daf1502a1c3128bccc121ba', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_001920_COMMIT.json': 'c1b5910e09b03d4fd199398c9f204a5fb4f4160691d747d4ec580118e7b1bebe', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_004096.npz': '2036d4fdb1dbeb62d93a635a4f1d3af03903acf4855472e8770fd797935718c5', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_004096_COMMIT.json': '1ba881d3bd477b137ee923f0e510ddc422d7d3ca0540b227f5ce3918bd4a38b2', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_003072.npz': '2eb369206c8ea6957d353ce835e5967a12238d365f40a5fbf19b25cda13417d8', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_003072_COMMIT.json': '95b348eb1fd78fe5b3e2917d389710a6bd278010238c4d3fda3aa4b090ef835c', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_004096.npz': 'd27a837fc06bc394515062523ad5534d2b64457e05ee53473f4543d3b5d9dc48', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_004096_COMMIT.json': '78f02be0069d390f93e2a7cd81b092230bc6e3a0b447818f0d7f37e665139c28', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_001024.npz': 'a8c02317b38003ee3fb1a71ce2159706ff3e4497a5d50f44c839ec1b10bfd253', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_001024_COMMIT.json': 'f58ab258d6f776f2ebf8d6600d92d52658545bcdaa0119d384aa46bc026c6d68', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_004096.npz': '187c35163050d9724c76874acce233b47f3692707844c5331e3261a455353c0a', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_004096_COMMIT.json': '44175d2706bfcc09c4eb8dc98f22f956248e3021bd3e49c362ea1c9227b2fa29', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_001024.npz': '1cdd4d3c92e380d007f6cd80aaf19f8d6b23f29b71c39a44b30e74d2ec5f3b38', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_001024_COMMIT.json': '90a4f0aad8fd590c613dde788f6b8025c256a1ac3f1621e80c32999f3afffd43', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_004096.npz': '0effce576c9290b91e0025ed7a228a1aef0a4291760ac7b906cfbcef39905b31', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_004096_COMMIT.json': '615bc086c7e492ed1eed94c239940023be1a3e51d25309a61d3c6b2481ee898e', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_001024.npz': '4fe2018165815fa73a8aa65c8b285fafca6f7f57f32bcbe9f70f1dbf53dcad63', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_001024_COMMIT.json': '570b3356d45f59b704f52001b2834ee30fb559e5085f2df24d872c0814a22034', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_004096.npz': '732f4743ee1ac602afdc4f7991e1c230bf4409ae827823d9e216135ce2c82f1f', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_004096_COMMIT.json': '601a9dce8eb42565f6431be234ba4d486b9d0ff24f27973ffadf568ec7eb579a', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_001024.npz': '876bd812bd195fdd263138c96ffde390bcd39dfd987b457e8e7207437ecd94ba', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_001024_COMMIT.json': 'ac21545eac676a1feb914946f6336e77338955b1efbfab809426c8e118a00666', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_ERROR.json': 'e128383f1c9a1725ec4480c3ad7e87b99d09a3b699a5bd40bac2414e6df9bb03', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_RECEIPT.json': 'bf5c48b986549b92593ff7d20a4fb05ee5c7b75cbec878ee80c2342db29daafe', 'cross_u_full_flrw_saved_aggregate_recovery_v001.py': 'ef099255955378bd56bad2c7952be118e2c232d0a3aa1a0462633750995f27cd', 'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001.md': 'c6d9d9605c8c3eea7abc62109afdc5bdea77d6c6d0200ff422907806637ca630', 'reviewed_cross_u_full_flrw_core_row_diagnostic_v001_253_c7ae3b5e.py': 'c7ae3b5eb9df1a0b4383d118533bf75c79cbc57c89333cb7aea98aa415f93e29', 'reviewed_cross_u_full_flrw_core_row_diagnostic_v001_17_378ec87f.md': '378ec87f30e0bca009e9b61819c0610e4b14cf6140e916a31e6aebf462dd3e9b'}
HELPER_SPANS={'bg': '9b1ab946ffe194f9bcddba16db78efe37ae2eb6ccc88ec47f12c53e1bd1480b4', 'legendre': '671e20cd8fe47819e23ccd8c2630c4625427fad284b8f6e175d50fcbc3178c2b', 'layout': 'd0bb5af30d66aea5a3fe46973bed4794f105ac4fa2258fe9dab723b6fbcdd666', 'equilibrated_solve': '967354773c918f772aa0be8b0a5fdebebebdec8e94d69fb9e67c6f67807e8a91', 'phase_nodes': '776ba8b11d9cc0045a46fa2ae56e5706ff4983333192be23e6e24e455dc1389a', 'radiation_weights': '1638e5d3a9720d8859764796aac05cdbc03508db8d484f24771f235409ff13fe', 'radiation_map': '74ac265694702b9e63e2eba5e203f8df2c92b60d2125b31363f79978b704e3dd', 'rate_matrix': '9105eae6adf8501c617e2444c76625b56ec97dc4bab03802f447d5d962dd9da2', 'native_map': '4c1a95c744613d8d0f6299f5d9171279f9b9176478a8ce66afbc04b501ce1f17', 'panel_step': '0b720cf76986cc68579fabd4fba399f8e8f77d6f8d33dd2b6ab587bc5869a7f5', 'original': 'cab4580ebde01a773bff15a6f6474bd225b7d02b1c73bf040b18f0df29f1e2da'}
TARGETS=[{'trial': {'arm': 'TIME', 'k': 0.01, 'na': 64, 'name': 'TIME_K0_O0', 'ns': 32, 'nstep': 2048, 'omega': 0.1}, 'target_step': 1028, 'recorded_maximum': {'a': 0.10090350448414476, 'error': 1.391148292504653e-08, 'nstep': 1028}, 'start_step': 1024, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O0_CP_001024.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O0_CP_001024_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O0_CP_002048.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O0_CP_002048_COMMIT.json'}, {'trial': {'arm': 'TIME', 'k': 0.01, 'na': 64, 'name': 'TIME_K0_O1', 'ns': 32, 'nstep': 2048, 'omega': 1.0}, 'target_step': 997, 'recorded_maximum': {'a': 0.09410935838239043, 'error': 1.4095319796151268e-08, 'nstep': 997}, 'start_step': 896, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O1_CP_000896.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O1_CP_000896_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O1_CP_002048.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O1_CP_002048_COMMIT.json'}, {'trial': {'arm': 'TIME', 'k': 0.01, 'na': 64, 'name': 'TIME_K0_O2', 'ns': 32, 'nstep': 2048, 'omega': 10.0}, 'target_step': 1031, 'recorded_maximum': {'a': 0.10158648592743963, 'error': 1.6702714262264342e-08, 'nstep': 1031}, 'start_step': 1024, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O2_CP_001024.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O2_CP_001024_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O2_CP_002048.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O2_CP_002048_COMMIT.json'}, {'trial': {'arm': 'TIME', 'k': 0.01, 'na': 64, 'name': 'TIME_K0_O3', 'ns': 32, 'nstep': 2048, 'omega': 100.0}, 'target_step': 1536, 'recorded_maximum': {'a': 0.316227766016838, 'error': 9.820605770832001e-09, 'nstep': 1536}, 'start_step': 1408, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O3_CP_001408.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O3_CP_001408_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O3_CP_002048.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K0_O3_CP_002048_COMMIT.json'}, {'trial': {'arm': 'TIME', 'k': 0.1, 'na': 64, 'name': 'TIME_K1_O0', 'ns': 32, 'nstep': 2048, 'omega': 0.1}, 'target_step': 535, 'recorded_maximum': {'a': 0.03330128082144737, 'error': 2.6102932708892617e-08, 'nstep': 535}, 'start_step': 512, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O0_CP_000512.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O0_CP_000512_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O0_CP_002048.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O0_CP_002048_COMMIT.json'}, {'trial': {'arm': 'TIME', 'k': 0.1, 'na': 64, 'name': 'TIME_K1_O1', 'ns': 32, 'nstep': 2048, 'omega': 1.0}, 'target_step': 553, 'recorded_maximum': {'a': 0.03467680390075965, 'error': 2.618137219879131e-08, 'nstep': 553}, 'start_step': 512, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O1_CP_000512.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O1_CP_000512_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O1_CP_002048.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O1_CP_002048_COMMIT.json'}, {'trial': {'arm': 'TIME', 'k': 0.1, 'na': 64, 'name': 'TIME_K1_O2', 'ns': 32, 'nstep': 2048, 'omega': 10.0}, 'target_step': 544, 'recorded_maximum': {'a': 0.033982083289425605, 'error': 2.1173541648090022e-08, 'nstep': 544}, 'start_step': 512, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O2_CP_000512.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O2_CP_000512_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O2_CP_002048.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O2_CP_002048_COMMIT.json'}, {'trial': {'arm': 'TIME', 'k': 0.1, 'na': 64, 'name': 'TIME_K1_O3', 'ns': 32, 'nstep': 2048, 'omega': 100.0}, 'target_step': 544, 'recorded_maximum': {'a': 0.033982083289425605, 'error': 1.2641234423376269e-08, 'nstep': 544}, 'start_step': 512, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O3_CP_000512.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O3_CP_000512_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O3_CP_002048.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_TIME_K1_O3_CP_002048_COMMIT.json'}, {'trial': {'arm': 'FINE', 'k': 0.01, 'na': 64, 'name': 'FINE_K0_O0', 'ns': 32, 'nstep': 4096, 'omega': 0.1}, 'target_step': 2085, 'recorded_maximum': {'a': 0.10424768182106901, 'error': 2.0226170204458384e-08, 'nstep': 2085}, 'start_step': 2048, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_002048.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_002048_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_004096.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_004096_COMMIT.json'}, {'trial': {'arm': 'FINE', 'k': 0.01, 'na': 64, 'name': 'FINE_K0_O1', 'ns': 32, 'nstep': 4096, 'omega': 1.0}, 'target_step': 2116, 'recorded_maximum': {'a': 0.10794514772342592, 'error': 2.00394778777578e-08, 'nstep': 2116}, 'start_step': 2048, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_002048.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_002048_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_004096.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_004096_COMMIT.json'}, {'trial': {'arm': 'FINE', 'k': 0.01, 'na': 64, 'name': 'FINE_K0_O2', 'ns': 32, 'nstep': 4096, 'omega': 10.0}, 'target_step': 2031, 'recorded_maximum': {'a': 0.09810682449032393, 'error': 2.178965787183547e-08, 'nstep': 2031}, 'start_step': 1920, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_001920.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_001920_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_004096.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_004096_COMMIT.json'}, {'trial': {'arm': 'FINE', 'k': 0.01, 'na': 64, 'name': 'FINE_K0_O3', 'ns': 32, 'nstep': 4096, 'omega': 100.0}, 'target_step': 3174, 'recorded_maximum': {'a': 0.3546538571361219, 'error': 1.739942089356884e-08, 'nstep': 3174}, 'start_step': 3072, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_003072.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_003072_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_004096.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_004096_COMMIT.json'}, {'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O0', 'ns': 32, 'nstep': 4096, 'omega': 0.1}, 'target_step': 1047, 'recorded_maximum': {'a': 0.03245117815991536, 'error': 2.2685375755877218e-08, 'nstep': 1047}, 'start_step': 1024, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_001024.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_001024_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_004096.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_004096_COMMIT.json'}, {'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O1', 'ns': 32, 'nstep': 4096, 'omega': 1.0}, 'target_step': 1069, 'recorded_maximum': {'a': 0.03326386092717056, 'error': 2.131492331501163e-08, 'nstep': 1069}, 'start_step': 1024, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_001024.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_001024_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_004096.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_004096_COMMIT.json'}, {'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O2', 'ns': 32, 'nstep': 4096, 'omega': 10.0}, 'target_step': 1069, 'recorded_maximum': {'a': 0.03326386092717056, 'error': 2.156714240387225e-08, 'nstep': 1069}, 'start_step': 1024, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_001024.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_001024_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_004096.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_004096_COMMIT.json'}, {'trial': {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O3', 'ns': 32, 'nstep': 4096, 'omega': 100.0}, 'target_step': 1069, 'recorded_maximum': {'a': 0.03326386092717056, 'error': 1.5935114837497646e-08, 'nstep': 1069}, 'start_step': 1024, 'start_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_001024.npz', 'start_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_001024_COMMIT.json', 'terminal_payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_004096.npz', 'terminal_commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_004096_COMMIT.json'}]
INPUTS,OUTPUTS,RECORDS={},{},[]
OWNER,CONTEXT={},{}
SOURCE_SHA=None

class NumericalRefusal(ArithmeticError):
    """Expected arithmetic refusal; never a metadata/publication exception."""
    pass

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

def closed_parent():
    for n,h in dict(PINS,**AGGREGATE_PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(n,h)
    result=json.loads((BASE/(AGGREGATE+'_RESULT.json')).read_text());receipt=json.loads((BASE/(AGGREGATE+'_RECEIPT.json')).read_text())
    original_receipt=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text());original_error=json.loads((BASE/(PARENT+'_ERROR.json')).read_text())
    if receipt['owner']!='root' or receipt['status']!='RECOVERED_NUMERICAL_FAILED' or receipt['result_sha256']!=AGGREGATE_PINS[AGGREGATE+'_RESULT.json']:raise ValueError('Actual closed saved aggregate')
    if receipt['source_sha256']!=PINS['cross_u_full_flrw_saved_aggregate_recovery_v001.py'] or receipt['pid']!=result['aggregation_manifest']['pid'] or receipt['started']!=result['aggregation_manifest']['started']:raise ValueError('Actual aggregation source/owner')
    if original_receipt['status']!='ERROR' or original_receipt['owner']!='root' or original_receipt['pid']!=65046 or original_receipt['message']!='Exact common physical frame abscissae':raise ValueError('Actual original ERROR closure')
    if result['original_error_receipt_copied_exactly']!=original_receipt or result['original_error_copied_exactly']!=original_error or receipt['parent_status']!='ERROR' or receipt['parent_pid']!=65046 or receipt['parent_closed']!=original_receipt['closed']:raise ValueError('Preserved original error ancestry')
    if original_receipt['source_sha256']!=PINS[PARENT_SOURCE] or original_receipt['manifest_sha256']!=PINS[PARENT+'_MANIFEST.json']:raise ValueError('Actual original source/manifest')
    for parent_receipt in (original_receipt,receipt):
        for kind in ('input_sha256','output_sha256'):
            for n,h in parent_receipt[kind].items():seal(n,h)
    manifest=result['manifest']
    if json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text())!=manifest or original_receipt['pid']!=manifest['pid']:raise ValueError('Original natural owner/manifest')
    if result['status']!='RECOVERED_NUMERICAL_FAILED' or len(result['rows'])!=32 or len(result['controls'])!=1889 or len(result['checkpoint_pairs'])!=928 or receipt['checkpoint_pairs']!=928:raise ValueError('Complete original32/928 logical census')
    if any(receipt[k]!=v or result[k]!=v for k,v in dict(logical_predicate_count=1889,available_predicate_count=1888,unverified_predicate_count=1).items()):raise ValueError('Explicit missing zero witness census')
    if sum(c['passed'] is None for c in result['controls'])!=1 or result['controls'][0]['disposition']!='not_serialized_in_parent_ERROR' or result['invalid_original_diagnostic_count']!=64:raise ValueError('No invented predicate/diagnostic qualification')
    if len(result['sample_registration_controls'])!=792 or not all(c['passed'] for c in result['sample_registration_controls']):raise ValueError('Separate recorded-frame registration')
    if result['physical_flags']!=manifest['physical_flags'] or any(manifest['physical_flags'].values()) or any(result['qualification'].values()):raise ValueError('Original/recovered false qualifications')
    selected={r['trial']['name']:r for r in result['rows'] if r['trial']['arm'] in ('TIME','FINE')}
    if set(selected)!={t['trial']['name'] for t in TARGETS}:raise ValueError('Exactly sixteen fixed trials')
    for t in TARGETS:
        r=selected[t['trial']['name']]
        if r['trial']!=t['trial'] or len(r['maxima'])!=16 or r['maxima']['core_rows']!=t['recorded_maximum'] or r['terminal_checkpoint']!=t['terminal_payload']:raise ValueError('Prebound first attaining maximum')
    return result,manifest

def load_environment(fixed):
    text=(BASE/PARENT_SOURCE).read_text();tree=ast.parse(text);lines=text.splitlines();defs=[]
    for n in tree.body:
        if isinstance(n,ast.FunctionDef) and n.name in HELPER_SPANS:
            span='\n'.join(lines[n.lineno-1:n.end_lineno])+'\n'
            if hashlib.sha256(span.encode()).hexdigest()!=HELPER_SPANS[n.name]:raise ValueError('Original helper span '+n.name)
            defs.append(n)
    if len(defs)!=len(HELPER_SPANS):raise ValueError('Exact retained helper inventory')
    env=dict(np=np,math=math,CP=299792.458,KB=.02,C=1.98,KBL=.01,CL=.99,FLOOR=1e-13,RAW={},fixed_for_domain=fixed)
    exec(compile(ast.Module(body=defs,type_ignores=[]),str(BASE/PARENT_SOURCE),'exec'),env)
    bp=BASE/'constrained_u_shared_eps_ngc_pantheon_v001.py';bt=bp.read_text();bg=next(n for n in ast.parse(bt).body if isinstance(n,ast.FunctionDef) and n.name=='background')
    span='\n'.join(bt.splitlines()[bg.lineno-1:bg.end_lineno])+'\n'
    if hashlib.sha256(span.encode()).hexdigest()!='8881f1df923d053d1d4b7ce06bfe4a50e856a62b49a25546a8d7e7a0d9f12bf2':raise ValueError('Literal parent background')
    exec(compile(ast.Module(body=[bg],type_ignores=[]),str(bp),'exec'),env)
    return env

def parent_checkpoint(target,manifest):
    cp=json.loads((BASE/target['start_commit']).read_text())
    expected=dict(schema=1,trial=target['trial']['name'],nstep=target['start_step'],payload=target['start_payload'],payload_sha256=PINS[target['start_payload']],owner='root',pid=manifest['pid'],source_sha256=PINS[PARENT_SOURCE],manifest_sha256=PINS[PARENT+'_MANIFEST.json'],metadata=cp['metadata'],failed=False)
    if cp!=expected:raise ValueError('Exact admitted parent COMMIT dictionary')
    with np.load(BASE/target['start_payload'],allow_pickle=False) as n:
        meta=json.loads(str(n['metadata']));arrays={k:n[k].copy() for k in n.files if k!='metadata'}
    if meta!=cp['metadata'] or meta['trial']!=target['trial'] or meta['nstep']!=target['start_step'] or meta['physical_flags']!=manifest['physical_flags']:raise ValueError('Exact admitted parent metadata')
    if set(arrays)!={'core','native','angular','frame_core','frame_native','frame_angular','last_stage_core','last_stage_native','last_stage_angular'}:raise ValueError('Original complete accepted schema')
    if any(not np.all(np.isfinite(v)) for v in arrays.values()):raise ValueError('Nonfinite admitted parent array')
    t=target['trial'];nf=target['start_step']//(t['nstep']//32)+1;ns=t['ns']+16;na=t['na']+17;nst=0 if target['start_step']==0 else 3
    shapes=dict(core=(11,2),native=(ns,2,2),angular=(na,2),frame_core=(nf,11,2),frame_native=(nf,ns,2,2),frame_angular=(nf,na,2),last_stage_core=(nst,11,2),last_stage_native=(nst,ns,2,2),last_stage_angular=(nst,na,2))
    if set(meta)!=set(['schema','trial','nstep','x','frames','maxima','input_sha256','layout','columns','physical_flags']) or meta['schema']!=1 or meta['columns']!=['metric','common_velocity'] or len(meta['frames'])!=nf:raise ValueError('Original exact accepted metadata schema')
    if meta['input_sha256']!=manifest['input_sha256'] or [f['nstep'] for f in meta['frames']]!=list(range(0,target['start_step']+1,t['nstep']//32)):raise ValueError('Original complete input/frame prefix')
    for k,v in arrays.items():
        dtype=np.complex128 if 'angular' in k else np.float64
        if v.shape!=shapes[k] or v.dtype!=np.dtype(dtype):raise ValueError('Original accepted array dimensions/dtype '+k)
    if any(not np.array_equal(arrays['frame_'+k][-1],arrays[k]) for k in ('core','native','angular')):raise ValueError('Last frame is accepted state')
    if nst and any(not np.array_equal(arrays['last_stage_'+k][-1],arrays[k]) for k in ('core','native','angular')):raise ValueError('Last panel endpoint is accepted state')
    return meta,arrays

def row_data(A,b,y):
    residual=A@y-b;envelope=abs(A)@abs(y)+abs(b);relative=abs(residual)/np.maximum(envelope,1e-13)
    error=float(np.max(relative))
    return dict(residual=residual,envelope=envelope,relative=relative),dict(error=finite(error),gate_passed=math.isfinite(error) and error<=ROW_TOL,finite=bool(np.all(np.isfinite(y))),absolute_max=finite(np.max(abs(residual))))

def scaling(A,b):
    a=A.copy();bb=b.copy();row=np.ones(33);col=np.ones(33);mats=[a.copy()];rhss=[bb.copy()];rrs=[];ccs=[]
    for _ in range(6):
        rr=np.sqrt(np.maximum(np.max(abs(a),axis=1),np.finfo(float).tiny));a/=rr[:,None];bb/=rr[:,None];row/=rr
        cc=np.sqrt(np.maximum(np.max(abs(a),axis=0),np.finfo(float).tiny));a/=cc[None,:];col/=cc
        rrs.append(rr.copy());ccs.append(cc.copy());mats.append(a.copy());rhss.append(bb.copy())
    return dict(scaled_matrix=a,scaled_rhs=bb,row_scale=row,column_scale=col,equilibration_matrices=np.asarray(mats),equilibration_rhs=np.asarray(rhss),equilibration_row_divisors=np.asarray(rrs),equilibration_column_divisors=np.asarray(ccs))

def pivot_evidence(A):
    a=A.copy();perm=np.arange(33);piv=[];relative=[]
    for j in range(33):
        k=j+int(np.argmax(abs(a[j:,j])));a[[j,k]]=a[[k,j]];perm[[j,k]]=perm[[k,j]]
        p=float(a[j,j]);piv.append(p);scale=float(np.max(abs(a[j,j:])))
        relative.append(abs(p)/scale if scale>0 else 0.)
        if not math.isfinite(p) or p==0:break
        if j<32:a[j+1:,j+1:]-=(a[j+1:,j]/p)[:,None]*a[j,j+1:][None,:];a[j+1:,j]=0
    return dict(diagnostic_LU=a,pivot_values=np.asarray(piv),pivot_relative=np.asarray(relative),pivot_permutation=perm)

def corrected_target_diagnostics(env,nodes,natives,angles,bgs,lay):
    old=env['original'](nodes[-1],natives[-1],angles[-1],bgs[-1],lay);g=bgs[-1];contact=g['b']*old['Phi'];trace=np.asarray(old['trace_terms']).copy();trace[0]+=contact
    momentum=np.asarray([old['S_dot']+contact,3*g['h']*old['S'],-g['B']*old['Phi'],-old['pressure'],2*g['r']*old['F'][2]/3])
    arrays=dict(missing_baryon_contact=contact,old_trace_terms=np.asarray(old['trace_terms']),corrected_trace_terms=trace,corrected_momentum_terms=momentum)
    summary=dict(old_trace=old['trace'],old_momentum_identity=old['momentum_identity'],corrected_target_trace=trace.sum(axis=0),corrected_target_momentum=momentum.sum(axis=0),corrected_trace_error=abs(trace.sum(axis=0))/np.maximum(abs(trace).sum(axis=0),1e-13),corrected_momentum_error=abs(momentum.sum(axis=0))/np.maximum(abs(momentum).sum(axis=0),1e-13),scope='Only this target endpoint; no corrected global maximum or inherited pass is claimed')
    return arrays,summary

def one_target(target,manifest):
    global CONTEXT
    first=len(RECORDS);scratch={};env=None;panel_count=0;context=dict(target=target)
    try:
        meta,admitted=parent_checkpoint(target,manifest);scratch.update({'admitted_'+k:v for k,v in admitted.items()});env=load_environment(manifest['fixed']);lay=env['layout'](target['trial']['ns'],target['trial']['na'],target['trial']['omega'])
        if not np.array_equal(np.asarray(meta['layout']['nodes']),lay['nodes']) or not np.array_equal(np.asarray(meta['layout']['weights']),lay['weights']) or not np.array_equal(np.asarray(meta['layout']['mu']),lay['mu']):raise ValueError('Original quadrature registration')
        core=admitted['core'].copy();native=admitted['native'].copy();angular=admitted['angular'].copy();original_solve=env['equilibrated_solve'];capture={}
        def instrument(A,b):
            if context['step']==target['target_step']:capture.update(original_matrix=A.copy(),original_rhs=b.copy())
            y,error=original_solve(A,b)
            if context['step']==target['target_step']:capture['original_solution']=y.copy()
            return y,error
        env['equilibrated_solve']=instrument;x0=math.log(manifest['ai']);dx=(math.log(manifest['af'])-x0)/target['trial']['nstep']
        for i in range(target['start_step'],target['target_step']):
            context.update(step=i+1);CONTEXT=dict(context);env['RAW'].clear()
            scratch.update(left_core=core.copy(),left_native=native.copy(),left_angular=angular.copy())
            nodes,natives,angles,bgs,checks=env['panel_step'](core,native,angular,x0+i*dx,dx,target['trial']['k'],manifest['fixed'],env['background'],lay)
            core,native,angular=nodes[-1].copy(),natives[-1].copy(),angles[-1].copy();panel_count+=1
        if panel_count!=target['target_step']-target['start_step'] or not 1<=panel_count<=128:raise ValueError('Prospective replay panel bound')
        scratch.update(capture);scratch.update(core_nodes=nodes.copy(),native_nodes=natives.copy(),angular_nodes=angles.copy());scratch.update(scaling(capture['original_matrix'],capture['original_rhs']))
        A,b,y=capture['original_matrix'],capture['original_rhs'],capture['original_solution'];rd,rr=row_data(A,b,y);scratch.update({'original_'+k:v for k,v in rd.items()})
        for key,M in [('unscaled',A),('scaled',scratch['scaled_matrix'])]:
            singular=np.linalg.svd(M,compute_uv=False);scratch[key+'_singular_values']=singular
            scratch.update({key+'_'+k:v for k,v in pivot_evidence(M).items()})
        da,ds=corrected_target_diagnostics(env,nodes,natives,angles,bgs,lay);scratch.update(da)
        evidence=dict(original=rr,recorded_maximum=target['recorded_maximum'],replayed_error_exact=(checks['core_rows']==target['recorded_maximum']['error']),replayed_error_difference=finite(checks['core_rows']-target['recorded_maximum']['error']),conditions={key:finite(scratch[key+'_singular_values'][0]/scratch[key+'_singular_values'][-1]) if scratch[key+'_singular_values'][-1]>0 else None for key in ['unscaled','scaled']},target_only_baryon_diagnostic=ds)
        checkpoint('TARGET',scratch,dict(kind='original_target',target=target,replayed_panels=panel_count,evidence=evidence,unaccepted=True))
        correction_rows=[];current=y.copy()
        for iteration in range(1,CORRECTIONS+1):
            if rr['gate_passed']:break
            raw=dict(matrix=A.copy(),rhs=b.copy(),before=current.copy(),before_residual=rd['residual'].copy(),scaled_correction_rhs=-scratch['row_scale'][:,None]*rd['residual'])
            scratch.update(raw);delta_scaled=np.linalg.solve(scratch['scaled_matrix'],raw['scaled_correction_rhs']);raw['scaled_delta']=delta_scaled.copy();delta=scratch['column_scale'][:,None]*delta_scaled;raw['physical_delta']=delta.copy();current=current+delta;raw['candidate']=current.copy();scratch.update(raw)
            rd,rr=row_data(A,b,current);raw.update(rd);scratch.update(raw)
            if not np.all(np.isfinite(current)) or rr['error'] is None:
                checkpoint('CORRECTION_REFUSED',raw,dict(kind='same_matrix_correction',target=target,iteration=iteration,row=rr,unaccepted=True,reason='Nonfinite correction/raw candidate retained'));raise NumericalRefusal('Nonfinite same-matrix correction')
            if hasattr(np,'longdouble'):
                la=np.asarray(A,dtype=np.longdouble);ly=np.asarray(current,dtype=np.longdouble);lb=np.asarray(b,dtype=np.longdouble)
                raw['extended_arithmetic_residual']=la@ly-lb
            checkpoint('CORRECTION',raw,dict(kind='same_matrix_correction',target=target,iteration=iteration,row=rr,unaccepted=True,scope='Same original33 equations; arithmetic candidate only, no native/angular/history adoption'))
            correction_rows.append(dict(iteration=iteration,**rr))
        case=dict(target=target,status='DIAGNOSTIC_COMPLETE',replayed_panels=panel_count,evidence=evidence,corrections=correction_rows,final_row=rr,own_checkpoints=list(RECORDS[first:]),qualification=manifest['physical_flags'],original_gates_unchanged=True)
    except Exception as exc:
        if env is not None:scratch.update({'refusal_raw_'+k:v for k,v in env['RAW'].items()})
        checkpoint('REFUSED',scratch,dict(kind='refusal_raw',target=target,context=context,type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc(),unaccepted=True))
        if not isinstance(exc,(NumericalRefusal,ArithmeticError,np.linalg.LinAlgError)):raise
        case=dict(target=target,status='REFUSAL_RETAINED',replayed_panels=panel_count,type=type(exc).__name__,message=str(exc),own_checkpoints=list(RECORDS[first:]),qualification=manifest['physical_flags'],original_gates_unchanged=True)
    publish(STEM+'_'+target['trial']['name']+'_CASE.json',case);return case

def full_reread():
    for rec in RECORDS:
        if json.loads((BASE/rec['commit_file']).read_text())!={k:rec[k] for k in ('file','sha256','metadata')}:raise ValueError('Exact own COMMIT record')
        with np.load(BASE/rec['file'],allow_pickle=False) as n:
            if json.loads(str(n['metadata']))!=rec['metadata'] or set(n.files)!={'metadata'}|set(rec['metadata']['schema']):raise ValueError('Exact own metadata/schema')
            for k,s in rec['metadata']['schema'].items():
                v=n[k]
                if list(v.shape)!=s['shape'] or str(v.dtype)!=s['dtype'] or bool(np.all(np.isfinite(v)))!=s['finite']:raise ValueError('Own shape/dtype/finite classification')
    if {r['file'] for r in RECORDS}!={p.name for p in BASE.glob(STEM+'_*.npz')} or {r['commit_file'] for r in RECORDS}!={p.name for p in BASE.glob(STEM+'_*.COMMIT.json')}:raise ValueError('Own exact pair census')

def main():
    global np,OWNER,SOURCE_SHA,CONTEXT
    if AUTHOR_GUARD:raise RuntimeError('Guarded author draft; root must bind closed parent and review before execution')
    started=now();tick=time.monotonic();SOURCE_SHA=sha(__file__)
    if list(BASE.glob(STEM+'_*')):raise FileExistsError('Unused diagnostic namespace required; no automatic or in-place resume')
    parent,manifest=closed_parent();import numpy as np
    if np.__version__!=manifest['numpy_version']:raise ValueError('Same numerical runtime registration')
    OWNER=dict(owner='root',pid=os.getpid(),started=started,source_sha256=SOURCE_SHA)
    mh=publish(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,targets=TARGETS,max_panels=2048,max_per_trial=128,max_corrections=CORRECTIONS,row_tolerance=ROW_TOL,parent_manifest=manifest,scope='Sixteen first attaining original core_rows maxima only',qualification=manifest['physical_flags']))
    cases=[]
    try:
        for t in TARGETS:cases.append(one_target(t,manifest))
        if len(cases)!=16 or sum(c['replayed_panels'] for c in cases)>2048:raise ValueError('Bounded complete target census')
        full_reread();recheck();complete=all(c['status']=='DIAGNOSTIC_COMPLETE' for c in cases);status='DIAGNOSTIC_COMPLETE' if complete else 'REFUSALS_RETAINED'
        result=dict(status=status,owner=OWNER,manifest_sha256=mh,cases=cases,parent_controls_copied_exactly=parent['controls'],parent_physical_flags=parent['physical_flags'],parent_status=parent['status'],recovered_aggregate_result_sha256=AGGREGATE_PINS[AGGREGATE+'_RESULT.json'],original_parent_error_sha256=PINS[PARENT+'_ERROR.json'],original_parent_error_receipt_sha256=PINS[PARENT+'_RECEIPT.json'],qualification=manifest['physical_flags'],elapsed_seconds=time.monotonic()-tick)
        rh=publish(STEM+'_RESULT.json',result)
        report=['# Bounded original core-row diagnostic V001','',status,'','Every old failure and source byte remains. Candidate corrections concern only original33-row arithmetic at sixteen target panels. They do not replace a trajectory, diagnose all physical preparation, or earn a full interval qualification.','', '| trial | panels | original error | final error | corrections | original row gate |','|---|---:|---:|---:|---:|---|']
        for c in cases:
            e=c.get('evidence',{}).get('original',{});f=c.get('final_row',{});report.append(f"| {c['target']['trial']['name']} | {c['replayed_panels']} | {e.get('error')} | {f.get('error')} | {len(c.get('corrections',[]))} | {f.get('gate_passed')} |")
        rp=BASE/(STEM+'_REPORT.md');raw=('\n'.join(report)+'\n').encode()
        with rp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        rp.chmod(0o444)
        if rp.read_bytes()!=raw:raise IOError('Exact report byte reread')
        OUTPUTS[rp.name]=sha(rp);recheck()
        receipt=dict(status=status,owner=OWNER,closed=now(),source_sha256=SOURCE_SHA,manifest_sha256=mh,result_sha256=rh,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),checkpoint_pairs=len(RECORDS),targets=16)
        publish(STEM+'_RECEIPT.json',receipt)
        if json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())!=canonical(receipt):raise ValueError('Entire receipt reread')
        full_reread();recheck();print(status,rh,flush=True);return 0 if complete else 3
    except Exception as exc:
        existing=BASE/(STEM+'_RECEIPT.json');error=dict(owner=OWNER,time=now(),context=CONTEXT,type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=manifest['physical_flags'])
        if existing.exists():error['protected_existing_receipt_sha256']=sha(existing)
        publish(STEM+'_ERROR.json',error)
        if not existing.exists():
            receipt=dict(status='ERROR',owner=OWNER,closed=now(),source_sha256=SOURCE_SHA,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),checkpoint_pairs=len(RECORDS))
            publish(STEM+'_RECEIPT.json',receipt)
        recheck();raise

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');args=ap.parse_args()
    if not args.root_owned:raise RuntimeError('Root-owned numerical execution only')
    raise SystemExit(main())
