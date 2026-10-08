# Additive clarification and concurrent-edit record

After the root froze and executed the tiny record-addition calculation, a
reviewer's queued wording clarification reached the protocol. The source
code and all other frozen inputs remained unchanged. A post-run hash check
detected this; it was not treated as a clean unchanged protocol.

The sole change replaced:

    the two nodes. The initial vector is |B,B,link=0,carrier=L>, index zero.

with:

    the two nodes. Its content is fixed to either alphabet value and is conserved;
    either choice gives the same block because carrier-to-record copying is
    absent. The initial vector is |B,B,link=0,carrier=L>, index zero.

The clarification is correct and does not change the implemented Hamiltonian,
state or checks. It is retained here additively. The root restored only this
sentence to recover the original frozen bytes, then checked the complete
source manifest. The intermediate clarified protocol hash was
1ee2d36445be837f491fdb816244605560d0623be67bd0ea06963e36f9027bdd.
No numerical output or freeze was overwritten and no result was selected.
