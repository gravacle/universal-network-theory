"""0546/0549 compose a K32-only compare with91/kpc certificate admission."""
from pathlib import Path
R=Path(__file__).parent
s=(R/'ntests_compare_c2v010.py').read_text().replace('import ntests_core_cxv003 as Core','import ntests_core_k32_cxv001 as Core\nimport audit_k32_cxv001 as AK\nimport validate_kept_k32_cxv001 as VK\nAK.V=VK\nP.A=AK')
s=s.replace('if end<32.', 'if end<91.').replace('coverage [2,32] absent','coverage [2,91] absent')
s=s.replace("if k!='GQ_NGC'", "if k not in ('GQ_NGC','EPS_NGC')")
s=s.replace("(*Core.REQUIRED,'GQ_NGC')", "(*Core.REQUIRED,'GQ_NGC','EPS_NGC')")
s=s.replace("elif k in P.A.P.CERT_NAMES:","elif k=='EPS_NGC':allowed |= p.resolve()==(P.A.P.CERT/'EPS_CERT_V006.json').resolve()\n   elif k in P.A.P.CERT_NAMES:")
s=s.replace("if not allowed:raise ValueError('RECORD_PATH_REFUSED '+k)","if k in ('EPS_NGC','LO_NGC'):allowed |= p.resolve().is_relative_to(ROOT.parent/'tail_scheme_impl_c2/certificates_ngc_k32')\n   if not allowed:raise ValueError('RECORD_PATH_REFUSED '+k)")
s=s.replace('(\"certificates_v002\",\"certificates_v003\")','("certificates_v002","certificates_v003","certificates_ngc_k32")')
pos=s.index('\ndef compare(records):')
extra='''
def coverage91(r,name):
 if not isinstance(r,dict):raise Core.Pending(name+' missing')
 if r.get('verdict')!=('CERTIFIED' if name=='EPS_NGC' else 'PASS'):raise Core.Pending(name+' not certified')
 if name=='EPS_NGC':
  cov=r.get('coverage_inverse_kpc',{}).get('NGC',[])
  if len(cov)!=2 or cov[0]>2 or cov[1]<91:raise Core.Pending('EPS_NGC declared coverage91 absent')
 spans=[]
 for x in r.get('shells',[]):
  span=x.get('range_inverse_kpc')
  Core.need(isinstance(span,list) and len(span)==2 and all(type(y) in (float,int) and math.isfinite(y) for y in span) and 0<=span[0]<span[1],name+' shell range')
  spans.append(span)
 end=2.
 for lo,hi in sorted(spans):
  if lo<=end:end=max(end,hi)
 if end<91:raise Core.Pending(name+' shell coverage91 absent')
'''
s=s[:pos]+extra+s[pos:]
s=s.replace("r['GQ_NGC_required']=True", """for name in ('EPS_NGC','LO_NGC'):
  try:coverage91(records.get(name),name)
  except Core.Pending as e:pending.append(str(e))
  except Exception as e:bad.append(name+': '+str(e))
 for name,obj in base.items():
  if name.startswith('N') and obj.get('production_K_big')!=32:bad.append(name+': production_K_big32 required')
 if bad:r.update(outcome='N_NO_RUN',tests_read=False,defects=bad,pending=pending)
 elif pending:r.update(outcome='N_INCOMPLETE',tests_read=False,pending=pending)
 r['production_K_big']=32;r['N3_prime_cutoffs']=[16,64];r['required_coverage_inverse_kpc']=91
 r['GQ_NGC_required']=True""")
compile(s,'ntests_compare_k32_cxv001.py','exec')
with (R/'ntests_compare_k32_cxv001.py').open('x') as f:f.write(s)
print('K32 compare constructed; tests pending')
