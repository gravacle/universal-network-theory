"""SOURCE ONLY: root-control ABI to separately authored Code2 integer primitives.
No scientific run at import. Input row-major reference is separately packed from
full control fixture, never aliased to producer's column-major W. Root authenticates
compiler/library gate, all source pins and full runtime before constructing this.
"""
from array import array
import ctypes as C
I64,U64,U32,I32=C.c_int64,C.c_uint64,C.c_uint32,C.c_int32
HOOK=C.CFUNCTYPE(C.c_int,U32,U32,U32)


def need(ok,why):
    if not ok:
        raise ValueError(why)


class Independent:
    def __init__(self,libpin,authenticate,fixture,guard):
        self.guard=guard
        self.exception=None
        self.n=len(fixture['w'])
        n=self.n
        need(1<=n<=10432 and array('q').itemsize==8,'full independent ABI shape')
        self.storage=array('q',(x for row in fixture['w'] for z in row for x in z))
        need(len(self.storage)==2*n*n,'complete row-major reference')
        self.w=(I64*len(self.storage)).from_buffer(self.storage)
        self.l=(I64*n)(*fixture['lam'])
        offsets,indices,values=[0],[],[]
        for row in fixture['rows']:
            for i,z in row:
                indices.append(i);values.extend(z)
            offsets.append(len(indices))
        self.nnz=len(indices)
        self.offsets=(U64*(n+1))(*offsets)
        # Distinct nonnull one-element dummies for empty CSR are contractual.
        self.indices=(U32*max(1,len(indices)))(*indices)
        self.values=(I64*max(1,len(values)))(*values)
        self.hook=HOOK(self._tick)
        authenticate(libpin,retain=False)
        self.lib=C.CDLL(libpin['path'])
        self.g=self.lib.p49i_gram_column
        self.g.argtypes=[U32,U32,C.POINTER(I64),C.POINTER(U64),C.POINTER(I32),C.POINTER(U64),C.POINTER(U64),HOOK]
        self.g.restype=C.c_int
        self.r=self.lib.p49i_residual_column
        self.r.argtypes=[U32,U32,C.POINTER(I64),C.POINTER(I64),U64,C.POINTER(U64),C.POINTER(U32),C.POINTER(I64),
                         C.POINTER(U64),C.POINTER(I32),C.POINTER(U64),C.POINTER(U64),HOOK]
        self.r.restype=C.c_int
        authenticate(libpin,retain=False)
        self.ag=self.lib.p49i_all_gram
        self.ag.argtypes=[U32,C.POINTER(I64),C.POINTER(U64),C.POINTER(U64),HOOK]
        self.ag.restype=C.c_int
        self.ar=self.lib.p49i_all_residual
        self.ar.argtypes=[U32,C.POINTER(I64),C.POINTER(I64),U64,C.POINTER(U64),C.POINTER(U32),C.POINTER(I64),C.POINTER(U64),C.POINTER(U64),HOOK]
        self.ar.restype=C.c_int
        self.wg=self.lib.p49i_weighted
        self.wg.argtypes=[U32,C.POINTER(I64),C.POINTER(U32),U32,U32,C.POINTER(U64),C.POINTER(I32),C.POINTER(U64),HOOK]
        self.wg.restype=C.c_int

    def _tick(self,phase,column,position):
        try:
            self.guard()
            return 0
        except BaseException as error:
            self.exception=error
            return 1

    def column(self,j,kind):
        need(type(j)is int and 0<=j<self.n and kind in ('gram','residual'),'complete independent column domain')
        n=self.n
        mag,sign,norm=(U64*(4*n))(),(I32*(2*n))(),(U64*8)()
        meta=(U64*(3*n if kind=='gram' else n))()
        self.exception=None
        self.guard()
        if kind=='gram':
            status=self.g(n,j,self.w,mag,sign,norm,meta,self.hook)
        else:
            status=self.r(n,j,self.w,self.l,self.nnz,self.offsets,self.indices,self.values,mag,sign,norm,meta,self.hook)
        if self.exception is not None:
            raise self.exception
        need(status==0,'independent compiled column refused status '+str(status))
        values=[]
        for i in range(n):
            z=[]
            for part in (0,1):
                q=2*i+part;m=int(mag[2*q])+(int(mag[2*q+1])<<64);s=int(sign[q])
                need(s in (-1,0,1) and ((s==0)==(m==0)),'canonical independent signed magnitude')
                z.append(s*m)
            values.append(z)
        return {'column':j,'kind':kind,'entries':values,
                'squared_norm':sum(int(norm[k])<<(64*k) for k in range(8)),
                'metadata':list(meta),'status':status}

    def all_norms(self,kind):
        need(kind in ('gram','residual'),'whole norm kind')
        n=self.n;norms=(U64*(8*n))();meta=(U64*(3*n if kind=='gram' else n))()
        self.exception=None;self.guard()
        if kind=='gram':status=self.ag(n,self.w,norms,meta,self.hook)
        else:status=self.ar(n,self.w,self.l,self.nnz,self.offsets,self.indices,self.values,norms,meta,self.hook)
        if self.exception is not None:raise self.exception
        need(status==0,'independent whole norms refused status '+str(status))
        return {'kind':kind,'status':status,'all_squared_column_numerators':[
            sum(int(norms[8*j+k])<<(64*k) for k in range(8)) for j in range(n)],'metadata':list(meta)}

    def weighted(self,weights,first,rank):
        n=self.n
        need(type(first)is int and type(rank)is int and 0<=first<n and 1<=rank<=16 and first+rank<=n,'weighted range')
        need(type(weights)is list and len(weights)==n and all(type(x)is int and 0<=x<=4 for x in weights),'whole weight array')
        wt=(U32*n)(*weights);mag=(U64*(4*rank*rank))();sign=(I32*(2*rank*rank))();bounds=(U64*(2*rank*rank))()
        self.exception=None;self.guard()
        status=self.wg(n,self.w,wt,first,rank,mag,sign,bounds,self.hook)
        if self.exception is not None:raise self.exception
        need(status==0,'independent weighted refused status '+str(status))
        matrix,prebounds=[],[]
        for a in range(rank):
            row,brow=[],[]
            for b in range(rank):
                k=a*rank+b;z=[]
                for part in (0,1):
                    q=2*k+part;m=int(mag[2*q])+(int(mag[2*q+1])<<64);sgn=int(sign[q])
                    need(sgn in (-1,0,1) and ((sgn==0)==(m==0)),'canonical weighted signed magnitude')
                    z.append(sgn*m)
                row.append(z);brow.append(int(bounds[2*k])+(int(bounds[2*k+1])<<64))
            matrix.append(row);prebounds.append(brow)
        return {'status':status,'first':first,'rank':rank,'complete_matrix':matrix,'complete_prebounds':prebounds}
