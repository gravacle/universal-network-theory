"""Public design §3.8 adapter, retaining v001 exact metric arithmetic and the reviewed parent.
ctx_with_tail(cid,label,state,mask) returns (checker, roster module, context).
"""
import math
import numpy as np
import ngc_ring_tail_ctx_c2v001 as L
KG=L.load(L.KG/'compute/tools/kg_lib_v001.py','ngc_public_kg')
L.verify(L.ART/'ngc_route_a_freeboundary_c2/check/tools/replay_c1.py')
L.verify(L.ART/'ngc_route_a_freeboundary_c2/check/tools/sweep_c1.py')
C,S=KG.checker()

class TailCtx(C.Ctx):
    def __init__(self,tail_boundary):
        super().__init__();self.tb=tail_boundary;self.tail=tail_boundary.state
    def metric_point(self,R,phi,z):
        if self.tail.empty:return super().metric_point(R,phi,z)
        pos=np.array([[R*math.cos(phi),R*math.sin(phi),z]])
        if (R,phi)!=self._k:
            self._line=self.line.prepare_line(prepared=self.prepared,x_m=float(pos[0,0]),y_m=float(pos[0,1]));self._k=(R,phi)
        pk=self.line.evaluate_line(line=self._line,z_m=z,**self.tb(pos))
        d=pk['fields'][0,:,0];g=pk['gradient'][0,:,0,:]
        for a in (d,g):
            sc=float(np.linalg.norm(a.real));im=float(np.linalg.norm(a.imag))
            if not all(math.isfinite(v) for v in (im,sc)) or im>self.ratol+self.rrtol*sc:raise ValueError('NONREAL_PHYSICAL_METRIC')
        return self.metric.evaluate_point(delta_fields=d.real,delta_gradient_physical=g.real,Cbar=self.Cbar,mubar=self.mubar,R=R,phi=phi,z=z)
    def kept_delta_n(self,R,phi,z):
        # Reuse the exact prepared line. No exp(log(N)) reconstruction.
        pos=np.array([[R*math.cos(phi),R*math.sin(phi),z]])
        if (R,phi)!=self._k:
            self._line=self.line.prepare_line(prepared=self.prepared,x_m=float(pos[0,0]),y_m=float(pos[0,1]));self._k=(R,phi)
        zero=dict(boundary_fields=np.zeros((1,10,1)),boundary_gradient=np.zeros((1,10,1,3)),boundary_hessian=np.zeros((1,10,1,3,3)))
        pk=self.line.evaluate_line(line=self._line,z_m=z,**zero)
        value=pk['fields'][0,0,0]
        if not math.isfinite(value.real) or not math.isfinite(value.imag) or abs(value.imag)>self.ratol+self.rrtol*abs(value.real):raise ValueError('NONREAL_KEPT_LAPSE')
        return float(value.real)
    def solve(self,*a,**k):raise RuntimeError('REPLAY_ONLY_NO_SOLVER')

def ctx_with_tail(cid,label,state,mask='cube'):
    L.env()
    if (cid,label)!=('T120L','hovr') or mask not in ('cube','sphere'):raise ValueError('UNREGISTERED_OPERATOR')
    if state.record.get('kept')!={'shape':mask,'K_inverse_kpc':2.}:raise ValueError('KEPT_MISMATCH')
    if not state.record.get('production_admissible'):raise ValueError('NONADMISSIBLE_STATE')
    L.certificates();L.verify(L.OP/'OPERATOR.json');L.verify(L.OP/'PREP.json')
    U,_,_=L.modules();ctx=TailCtx(U.TailBoundary(state,order=1));KG.OPS=L.KG/'phase23/ops'
    ctx.prepared,_=KG.load_operator(cid,label)
    if mask=='sphere':
        keep=np.linalg.norm(ctx.prepared['wavevectors'],axis=1)*C.KPC<=2.
        ctx.prepared={k:a[keep] for k,a in ctx.prepared.items()}
    ctx._k=None;ctx._line=None
    return C,S,ctx

def ngc_iter0_roster(prep_json,ops_dir):
    if L.OP.resolve()!=L.Path(ops_dir).resolve():raise ValueError('UNREGISTERED_OPERATOR')
    if prep_json!=L.json.loads(L.verify(L.OP/'PREP.json').read_text()):raise ValueError('PREP_MISMATCH')
    _,RS,_=L.modules();return L.source(RS)
