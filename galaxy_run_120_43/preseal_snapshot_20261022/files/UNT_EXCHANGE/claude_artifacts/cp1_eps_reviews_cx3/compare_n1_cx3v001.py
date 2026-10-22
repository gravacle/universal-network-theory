from pathlib import Path
import re,json,hashlib,subprocess,struct
B=Path('/Users/bgm/Research/UNT_EXCHANGE');D=B/'FROM_CODEX/0763_2026-10-20_codex3_EPS_reviews_rows10_31_signer_approved.md';R=B/'claude_artifacts/s4rc1_c3/cp1_run_c3v004b';O=B/'claude_artifacts/cp1_eps_reviews_cx3'
def h(b):return hashlib.sha256(b).hexdigest()
rows={int(r):(f,rh,nh) for r,f,rh,nh in re.findall(r'\| (\d+) \| (P[^ ]+) \| `([a-f0-9]+)` \| `([a-f0-9]+)` \|',D.read_text())}
def chunk(text,k):
 needle='\n  "'+k+'": ';assert text.count(needle)==1
 start=text.index(needle)+len(needle);v,end=json.JSONDecoder().raw_decode(text,start)
 return text[start:end].encode(),v
def diff(x,y,path=''):
 if type(x)!=type(y):return [path]
 if isinstance(x,dict):
  z=[]
  for k in sorted(set(x)|set(y)):z+=diff(x[k],y[k],path+'/'+k) if k in x and k in y else [path+'/'+k]
  return z
 if isinstance(x,list):
  if len(x)!=len(y):return [path+'/length']
  return [p for i,(u,v) in enumerate(zip(x,y)) for p in diff(u,v,path+'/'+str(i))]
 return [] if (struct.pack('>d',x)==struct.pack('>d',y) if isinstance(x,float) else x==y) else [path]
results=[];pins=[]
for lo in [10,11,12,13,18,19,20,21]:
 hi=lo+4;pair=[]
 for row in [lo,hi]:
  folder,_,prefix=rows[row];key=folder.split('_')[1];p=R/folder/('EPS_NUMERIC_'+key+'.json');raw=p.read_bytes();assert h(raw).startswith(prefix)
  pins.append({'row':row,'path':str(p),'sha256':h(raw)})
  text=raw.decode();pair.append((text,json.loads(raw)))
 entry={'rows':[lo,hi],'groups':{}}
 for k,n in [('shells',178),('envelope_audit',14)]:
  a,aa=chunk(pair[0][0],k);b,bb=chunk(pair[1][0],k);assert len(aa)==len(bb)==n
  entry['groups'][k]={'record_count':n,'raw_json_bytes_equal':a==b,'left_sha256':h(a),'right_sha256':h(b),'byte_length_left':len(a),'byte_length_right':len(b),'typed_bitwise_differences':diff(aa,bb)}
 entry['full_record_difference_paths']=diff(pair[0][1],pair[1][1])
 entry['common_scale_s_values']=[p[1]['identity']['physical']['common_scale_s'] for p in pair]
 entry['common_scale_ratio']=entry['common_scale_s_values'][1]/entry['common_scale_s_values'][0]
 results.append(entry)
report={'schema':'CX3_N1_PAIR_COMPARISON_V001','date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),'status':'TESTED','pairs':results,'all_eight_pairs_raw_bytes_equal':all(g['raw_json_bytes_equal'] and not g['typed_bitwise_differences'] for x in results for g in x['groups'].values()),'inputs':pins,'dispatch':{'path':str(D),'sha256':h(D.read_bytes())},'script':{'path':str(Path(__file__)),'sha256':h(Path(__file__).read_bytes())},'untested':'By-construction cancellation or scientific correctness of common_scale_s independence; assigned to Codex2, no producer executed or inspected here.'}
p=O/'N1_PAIR_COMPARISON_CX3V001.json'
with p.open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({'path':str(p),'sha256':h(p.read_bytes()),'all_eight_pairs_raw_bytes_equal':report['all_eight_pairs_raw_bytes_equal'],'differences':[{ 'rows':x['rows'],'paths':x['full_record_difference_paths']} for x in results]}))
