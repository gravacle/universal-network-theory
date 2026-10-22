"""Independent Phase-1 band-column calculation; never a tier or stop.
Record/row identity and byte pin checks belong to the external adapter.
"""
import math

def finite(value):
    if type(value) not in (int,float):return False
    try:return math.isfinite(value)
    except OverflowError:return False

def band_entry(query_id,row,target,sigma):
    if query_id in ('NGC3198-Q01','NGC3198-Q02'):
        return {'overlaps':None,'code':'Q01_Q02_ALWAYS_NOT_AVAILABLE','fd_noise_not_bounded':False}
    def blank(code):return {'overlaps':None,'code':code,'fd_noise_not_bounded':False}
    if type(row) is not dict:return blank('L1_ROW_DEFECT')
    if row.get('status')=='NOT_AVAILABLE':return blank('L1_ROW_NOT_AVAILABLE')
    if row.get('status')!='AVAILABLE':return blank('L1_ROW_DEFECT')
    lo,hi=row.get('lo'),row.get('hi');noise=row.get('fd_noise')
    if not finite(lo) or not finite(hi):return blank('L1_ROW_DEFECT')
    if type(noise) is not dict and noise!='FD_NOISE_NOT_BOUNDED':return blank('L1_ROW_DEFECT')
    if not finite(target) or not finite(sigma) or sigma<=0:return blank('TARGET_PAIR_DEFECT')
    # Use the ordinary numeric endpoints specified by [v-sigma,v+sigma].
    # Overflow to infinity is safe for comparisons to finite lo/hi.
    overlaps=lo<=target+sigma and hi>=target-sigma
    return {'overlaps':overlaps,'code':None,'fd_noise_not_bounded':noise=='FD_NOISE_NOT_BOUNDED'}
