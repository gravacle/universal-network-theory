"""0513 successor: replay-only in-process resource guard. No reviewed file is edited."""
import ngc_ring_tail_ctx_c2v001 as BASE
from ngc_ring_tail_ctx_c2v001 import *
_ORIGINAL_MODULES=BASE.modules
OVERRIDE={'bytes':4*2**30,'reason':'replay-only resource guard, 0513',
          'module_sha256':'c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22'}

def modules():
    U,RS,PV=_ORIGINAL_MODULES()
    U.TAIL_MEMORY_CAP_BYTES=OVERRIDE['bytes']
    return U,RS,PV

def ctx_with_tail(kbig=2.,shape='cube',doubled=False):
    BASE.modules=modules
    try:ctx,cols=BASE.ctx_with_tail(kbig,shape,doubled)
    finally:BASE.modules=_ORIGINAL_MODULES
    ctx.memory_cap_override=dict(OVERRIDE)
    return ctx,cols
