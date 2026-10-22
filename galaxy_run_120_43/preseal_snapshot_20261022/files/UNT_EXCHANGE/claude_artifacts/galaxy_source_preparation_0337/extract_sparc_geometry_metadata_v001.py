"""INERT allowed-field extractor for SPARC galaxy-sample geometry metadata (task 0337 part 3). ROOT runs it; the author has not.

Source: SPARC Table1 in MRT form (SPARC_Lelli2016c.mrt). Allowed fields ONLY: Galaxy, D, e_D, f_D, Inc, e_Inc
(in-file MRT header bytes 1-34). Each data line is truncated to 34 bytes BEFORE any other use, so Vflat, e_Vflat
(bytes 87-96) and all other columns are never read into a variable. Fails closed if the in-file header's labels,
byte ranges, formats or units differ from the allowed schema. Errors print fixed codes only. Refuses to overwrite.
NOTE: the CDS ReadMe (SPARC_ReadMe.html) documents table1.dat with DIFFERENT byte positions (e.g. Dist 16-21).
This extractor uses the local MRT file's own in-file header, which governs its bytes.
"""
import hashlib,json,re,sys
from pathlib import Path
SRC=('/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/external_ddo154_v001/SPARC_Lelli2016c.mrt','5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243')
ALLOWED={'Galaxy':(1,11,'A11','---'),'D':(14,19,'F6.2','Mpc'),'e_D':(20,24,'F5.2','Mpc'),'f_D':(25,26,'I2','---'),'Inc':(27,30,'F4.1','deg'),'e_Inc':(31,34,'F4.1','deg')}
MAXBYTE=34
F_D_NOTE={'1':'Hubble-Flow assuming H0=73 km/s/Mpc and correcting for Virgo-centric infall','2':'Magnitude of the Tip of the Red Giant Branch','3':'Cepheids Magnitude-Period Relation','4':'Ursa Major Cluster of Galaxies','5':'Supernovae Light Curve'}
OBJECTS={'NGC3198':['NGC3198','NGC 3198'],'DDO154':['DDO154','DDO 154','NGC4789A','NGC 4789A']}
FIELD=re.compile(r'^\s*(\d+)-\s*(\d+)\s+(\S+)\s+(\S+)\s+(\S+)')
class Fail(Exception):pass
def main(argv):
 if len(argv)!=2:raise Fail('E_USAGE')
 outp=Path(argv[1])
 if outp.exists():raise Fail('E_OUTPUT_EXISTS')
 b=Path(SRC[0]).read_bytes()
 if hashlib.sha256(b).hexdigest()!=SRC[1]:raise Fail('E_PIN')
 try:lines=b.decode('ascii').splitlines()
 except UnicodeDecodeError:raise Fail('E_ENCODING')
 del b
 seps=[i for i,l in enumerate(lines[:200]) if re.fullmatch(r'-{20,}',l.strip())]
 if not seps:raise Fail('E_HEADER')
 hdr={}
 for l in lines[:seps[-1]]:
  m=FIELD.match(l)
  if m:hdr[m.group(5)]=(int(m.group(1)),int(m.group(2)),m.group(3),m.group(4))
 for k,v in ALLOWED.items():
  if hdr.get(k)!=v:raise Fail('E_SCHEMA')
 found={}
 for n,l in enumerate(lines[seps[-1]+1:],seps[-1]+2):
  l=l[:MAXBYTE]  # truncate before use: nothing beyond e_Inc is retained
  name=l[0:11].strip()
  for obj,aliases in OBJECTS.items():
   if name in aliases:
    if obj in found:raise Fail('E_DUPLICATE_OBJECT')
    rec={k:l[a-1:e].strip() for k,(a,e,fmt,u) in ALLOWED.items()}
    rec['f_D_meaning']=F_D_NOTE.get(rec['f_D'])
    rec['source_line_number']=n
    found[obj]=rec
 del lines
 result={'schema':'SPARC_GEOMETRY_ALLOWED_FIELDS_V001','source':{'path':SRC[0],'sha256':SRC[1]},'allowed_fields':{k:{'bytes':[a,e],'format':f,'unit':u} for k,(a,e,f,u) in ALLOWED.items()},
  'excluded':'every byte beyond 34 (luminosity, radii, surface brightnesses, MHI, RHI, Vflat, e_Vflat, Q, Ref)','objects':found,
  'missing_objects':[o for o in OBJECTS if o not in found],'exposure_labels':{'NGC3198':'development-exposed','DDO154':'calibration-only; not blind'},
  'interpretation':'Catalogue values as published; e_D and e_Inc are catalogue mean errors, not covariance; no geometry is chosen or adopted.'}
 with outp.open('x') as f:json.dump(result,f,indent=1)
 print(json.dumps({'status':'OK','output':str(outp),'objects_found':sorted(found),'missing':result['missing_objects']}))
if __name__=='__main__':
 try:main(sys.argv)
 except Fail as e:print(json.dumps({'status':'FAILED','code':str(e)}));sys.exit(2)
 except Exception as e:print(json.dumps({'status':'FAILED','code':'E_UNEXPECTED','type':type(e).__name__}));sys.exit(3)
