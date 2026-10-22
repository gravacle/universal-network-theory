"""NE4: parent sphere mask arithmetic; same-height sphere tail evaluation."""
from ringeval_uvt_c2v004 import replay

def sphere_replay(kbig=16.,doubled=False,start=0,end=None):
    return replay(kbig,'sphere',doubled,start,end)
