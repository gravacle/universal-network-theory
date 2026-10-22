"""0845 distribution RECORD identity; never imports the scientific/package code.
Caller resolves distribution metadata under the selected isolated interpreter.
No installed-file fallback yet: distributions without RECORD refuse.
"""
from pathlib import Path
import re
from runtime_fingerprints_cx1v002 import FileFingerprints
class DistributionRefusal(ValueError):pass
def need(ok,reason):
 if not ok:raise DistributionRefusal(reason)
def capture_distribution(distribution,*,site_root,files=None):
 files=files or FileFingerprints()
 name=distribution.metadata.get('Name');version=distribution.version
 need(type(name) is str and bool(name) and type(version) is str and bool(version),'DISTRIBUTION_METADATA')
 entries=distribution.files
 need(entries is not None,'DISTRIBUTION_FILE_LIST_MISSING')
 records=[x for x in entries if len(Path(str(x)).parts)>=2 and Path(str(x)).name=='RECORD' and Path(str(x)).parent.name.endswith('.dist-info')]
 need(len(records)==1,'DISTRIBUTION_RECORD_REQUIRED')
 root=Path(site_root).resolve(strict=True)
 path=Path(distribution.locate_file(records[0])).resolve(strict=True)
 need(root.is_dir() and root in path.parents,'DISTRIBUTION_RECORD_OUTSIDE_SITE')
 pin=files.capture(path)
 return dict(name=re.sub(r'[-_.]+','-',name).lower(),version=version,identity_basis='distribution_RECORD',record=pin)
def compare_distributions(direct,campaign):
 def identities(rows):
  out={}
  for r in rows:
   need(r['name'] not in out,'DUPLICATE_DISTRIBUTION')
   out[r['name']]=(r['version'],r['record']['sha256'])
  return out
 need(identities(direct)==identities(campaign),'DISTRIBUTION_MISMATCH')
 return True
