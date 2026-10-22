"""INERT target-free extractor for the NGC3198 43-query manifest (task 0337 part 2). ROOT runs it; the author has not.

Emits ONLY: original data-row order, a stable query ID derived from that order, the Rad column (decimal text as
published), its documented unit, and reference-distance metadata. Every other column is parsed only to validate
the row width and is discarded at once; it is never written or printed. Errors print a fixed code, never content.
Fails closed on any pin, schema, count, finiteness, uniqueness or order violation. Refuses to overwrite output.
Standard library only.
"""
import hashlib,json,math,re,sys
from pathlib import Path
J='/Users/bgm/Research/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
ROTMOD=(J+'/sparc_official_NGC3198_rotmod.dat','17b774ad11e7dd745a067073b76f1909d4de32fa87616df12b64da3f225cf953')
MASSMODELS=(J+'/external_ddo154_v001/SPARC_MassModels_Lelli2016c.mrt','9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c')
EXPECTED_ROWS=43
EXPECTED_ROTMOD_COLUMNS=['Rad','Vobs','errV','Vgas','Vdisk','Vbul','SBdisk','SBbul']  # SPARC Rotmod format; verified in-file, fail closed
DEC=re.compile(r'^[0-9]+(\.[0-9]+)?$')
DIST=re.compile(r'^#\s*Distance\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*Mpc\s*$')
MRT_FIELD=re.compile(r'^\s*(\d+)-\s*(\d+)\s+(\S+)\s+(\S+)\s+(\S+)')
MRT_REQUIRED={'ID':(1,11,'A11','---'),'D':(13,18,'F6.2','Mpc'),'R':(20,25,'F6.2','kpc')}
class Fail(Exception):pass
def pin(path,sha):
 b=Path(path).read_bytes();h=hashlib.sha256(b).hexdigest()
 if h!=sha:raise Fail('E_PIN')
 return b,{'path':path,'sha256':h,'bytes':len(b)}
def rotmod_rows(b):
 try:lines=b.decode('ascii').splitlines()
 except UnicodeDecodeError:raise Fail('E_ENCODING')
 header=[(i,l) for i,l in enumerate(lines,1) if l.startswith('#')]
 cols=[(i,l[1:].split()) for i,l in header if l[1:].split()[:1]==['Rad']]
 if len(cols)!=1 or cols[0][1]!=EXPECTED_ROTMOD_COLUMNS:raise Fail('E_SCHEMA_COLUMNS')
 units=[l[1:].split() for i,l in header if i==cols[0][0]+1]
 if len(units)!=1 or len(units[0])!=len(EXPECTED_ROTMOD_COLUMNS) or units[0][0]!='kpc':raise Fail('E_SCHEMA_UNITS')
 dist=[(i,DIST.match(l)) for i,l in header if DIST.match(l)]
 ref=({'value_text':dist[0][1].group(1),'unit':'Mpc','source':'rotmod header line %d (strict regex)'%dist[0][0]} if len(dist)==1 else None)
 rows=[];prev=None
 for i,l in enumerate(lines,1):
  if not l.strip() or l.startswith('#'):continue
  f=l.split()
  if len(f)!=len(EXPECTED_ROTMOD_COLUMNS):raise Fail('E_ROW_FIELDS')
  rad=f[0];del f
  if not DEC.match(rad):raise Fail('E_RAD_FORMAT')
  v=float(rad)
  if not math.isfinite(v) or v<=0:raise Fail('E_RAD_VALUE')
  if prev is not None and v<=prev:raise Fail('E_ORDER')
  prev=v;rows.append((i,rad))
 if len(rows)!=EXPECTED_ROWS:raise Fail('E_COUNT')
 return rows,ref
def massmodels_rows(b):
 try:lines=b.decode('ascii').splitlines()
 except UnicodeDecodeError:raise Fail('E_MRT_ENCODING')
 seps=[i for i,l in enumerate(lines[:200]) if re.fullmatch(r'-{20,}',l.strip())]
 if not seps:raise Fail('E_MRT_HEADER')
 fields={}
 for l in lines[:seps[-1]]:
  m=MRT_FIELD.match(l)
  if m:fields[m.group(5)]=(int(m.group(1)),int(m.group(2)),m.group(3),m.group(4))
 for k,v in MRT_REQUIRED.items():
  if fields.get(k)!=v:raise Fail('E_MRT_SCHEMA')
 out=[]
 for l in lines[seps[-1]+1:]:
  l=l[:25]  # never touch bytes beyond the R field
  if l[0:11].strip()!='NGC3198':continue
  out.append((l[12:18].strip(),l[19:25].strip()))
 return out
def main(argv):
 if len(argv)!=2:raise Fail('E_USAGE')
 outp=Path(argv[1])
 if outp.exists():raise Fail('E_OUTPUT_EXISTS')
 rb,rpin=pin(*ROTMOD);rows,ref=rotmod_rows(rb);del rb
 cross={'status':'NOT_RUN'}
 try:
  mb,mpin=pin(*MASSMODELS);mm=massmodels_rows(mb);del mb
  mr=[r for d,r in mm];md=sorted(set(d for d,r in mm))
  same_count=len(mr)==len(rows)
  text_eq=same_count and all(a==b for (i,a),b in zip(rows,mr))
  num_eq=same_count and all(bool(DEC.match(b)) and float(a)==float(b) for (i,a),b in zip(rows,mr))
  cross={'status':'MATCH' if (same_count and num_eq) else 'MISMATCH','source':mpin,'rows_found':len(mr),'text_equal':text_eq,'numeric_equal':num_eq,
         'mismatch_row_indices':[k+1 for k,((i,a),b) in enumerate(zip(rows,mr)) if not DEC.match(b) or float(a)!=float(b)] if same_count else None,
         'reference_distance_texts':md,'reference_distance_unique':len(md)==1}
 except Fail as e:cross={'status':'FAILED','code':str(e)}
 mm_ref=({'value_text':cross['reference_distance_texts'][0],'unit':'Mpc','source':'MassModels MRT field D (bytes 13-18), all NGC3198 rows identical'} if cross.get('reference_distance_unique') else None)
 agree=(None if ref is None or mm_ref is None else float(ref['value_text'])==float(mm_ref['value_text']))
 result={'schema':'NGC3198_TARGET_FREE_QUERY_MANIFEST_V001','object':'NGC3198','aliases':['NGC 3198'],'exposure_label':'development-exposed',
  'source':rpin,'emitted_columns':['data_row_index','query_id','source_line_number','Rad_text','Rad_unit'],'no_other_columns_emitted':True,
  'rad_unit':'kpc','rad_unit_basis':'rotmod units line first token == kpc (checked); SPARC MassModels MRT field R documented as kpc',
  'rows':[{'data_row_index':k+1,'query_id':'NGC3198-Q%02d'%(k+1),'source_line_number':i,'Rad_text':r,'Rad_unit':'kpc'} for k,(i,r) in enumerate(rows)],
  'reference_distance':{'rotmod_header':ref,'massmodels':mm_ref,'agree':agree,'note':'No distance is chosen; null where it cannot be safely established.'},
  'crosscheck_massmodels':cross,'checks':{'row_count':len(rows),'expected':EXPECTED_ROWS,'finite_positive':True,'strictly_increasing':True,'unique_ids':True},
  'not_included':'velocities, their errors, mass-model velocity contributions and surface brightnesses'}
 with outp.open('x') as f:json.dump(result,f,indent=1)
 print(json.dumps({'status':'OK','output':str(outp),'rows':len(rows),'crosscheck':cross['status'],'reference_distance_agree':agree}))
if __name__=='__main__':
 try:main(sys.argv)
 except Fail as e:print(json.dumps({'status':'FAILED','code':str(e)}));sys.exit(2)
 except Exception as e:print(json.dumps({'status':'FAILED','code':'E_UNEXPECTED','type':type(e).__name__}));sys.exit(3)
