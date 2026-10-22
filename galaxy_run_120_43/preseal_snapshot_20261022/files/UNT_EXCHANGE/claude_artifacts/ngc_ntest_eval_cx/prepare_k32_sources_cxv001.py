"""0546 immutable K32 record/audit successors; exclusive writes. No numerical replay."""
from pathlib import Path
R=Path(__file__).parent
mapping={'assemble_ntests_c2v001':'assemble_k32_cxv001','assemble_ntests_c2v002':'validate_k32_cxv001','assemble_ntests_c2v003':'validate_kept_k32_cxv001','ntests_compare_c2v004':'audit_k32_cxv001','ntests_core_cxv003':'ntests_core_k32_cxv001'}
def shift(s):
 for a,b in [('CUBE16','XXBASEXX'),('CUBE8','XXLOWXX'),('CUBE32','XXHIGHXX'),('SPHERE16','SPHERE32')]:s=s.replace(a,b)
 return s.replace('XXBASEXX','CUBE32').replace('XXLOWXX','CUBE16').replace('XXHIGHXX','CUBE64').replace('_vs_16','_vs_32').replace('8_vs_32','16_vs_32').replace('32_vs_32','64_vs_32')
def refs(s):
 for a,b in mapping.items():s=s.replace(a,b)
 return s
for old,new in mapping.items():
 s=refs(shift((R/(old+'.py')).read_text()))
 if old=='assemble_ntests_c2v002':
  s=s.replace("'CUBE32':(16.","'CUBE32':(32.").replace("'NQ_FINE':(16.","'NQ_FINE':(32.").replace("'SPHERE32':(16.","'SPHERE32':(32.").replace("'CUBE16':(8.","'CUBE16':(16.").replace("'CUBE64':(32.","'CUBE64':(64.")
 if old=='assemble_ntests_c2v003':s=s.replace('raws[1].get','raws[0].get')
 if old=='assemble_ntests_c2v001':s=s.replace("return dict(schema='NGC_NTEST_RECORD_C2V001',test=n","return dict(production_K_big=32,scope_ruling='0546',schema='NGC_NTEST_RECORD_C2V001',test=n")
 with (R/(new+'.py')).open('x') as f:f.write(s)
 compile(s,new,'exec')
print('Five K32 source successors compile; runtime and data validation pending')
