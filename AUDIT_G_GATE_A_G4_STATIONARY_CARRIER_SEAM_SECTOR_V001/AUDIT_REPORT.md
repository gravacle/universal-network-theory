# Independent hostile audit

## Disposition

`PASS_SECTOR_QUALIFIED`.

The packet is defensible only with `OWNER_CENSUS_DELTA.json.scope =
carrier_sector_only` treated as load-bearing. None of its four promotions is
a completed full-parent GK02 row.

## Independent reconstruction

For `V=(Z/4Z)^3`, there are 64 labels. Pairing each label with its positive
step along each of three generators produces 192 ordered representatives.
At `L=4`, no representative is the reverse of another positive-generator
representative, so their 192 unordered supports are distinct. Every vertex
has three tails and three heads.

With incidence `-1` at a tail and `+1` at a head, internal columns cancel for
every region. Independent singleton tests give three outward and three inward
supports per cell. The transverse 16-cell slab has 16 outward and 16 inward
supports. Every full-graph column sums to zero, proving global telescoping
without counting a physical edge twice.

On the BS07 active block ordered as `A=|x,B>`, `B=|B,x>`, direct matrices give
`[T,q_a]=-iJ` and `[T,q_b]=+iJ`. With BS09 `H=-tT`, this becomes
`dot(q_a)=-(t/hbar)J` and `dot(q_b)=+(t/hbar)J`, matching the packet's
orientation. The previously audited branch weight `1/2` and native transfer
integral one embed as current `1/2`, with two exact zero cell residuals.

For finite real `beta>=0`, `exp(-beta H)/Tr exp(-beta H)` exists, is positive,
and commutes with `H` by functional calculus. This proves existence of a
stationary carrier-sector member, not its physical selection. The product
qutrit projectors resolve the identity. Consequently summing the finite CTP
effects at equal branches gives `Tr(U rho U^dagger)=1`. That is sufficient
for the claimed finite carrier-sector generator and complete carrier read.

## Hostile scope finding

The delta's values `EXACT_GLOBAL_G4_CARRIER_SECTOR`,
`EXACT_GLOBAL_OWNER_ONCE_TELESCOPING`,
`EXACT_STATIONARY_GIBBS_MEMBER__PHYSICAL_SELECTION_OPEN`, and
`EXACT_COMPLETE_PRODUCT_QUTRIT_READ` are accepted only under the JSON's
top-level `carrier_sector_only` scope and the theorem's repeated sector
qualification:

- connector means only native BS09 carrier edges;
- seam/period means only their oriented carrier-current telescoping;
- state means existence of one Gibbs carrier-sector member, with selection
  and the stationary full-parent state open;
- measure means only the complete product-qutrit carrier read, not the full
  apparatus or global physical measure.

Reading any of these as completing a full GK02 owner would be false. The
packet itself blocks that reading by retaining general boundary apparatus,
matching outside the carrier sector, retained field, support, constraint, and
the lawful quotient as undefined and by marking the global stationary action
`OWNER_INCOMPLETE`.

The equilibrium mean current being zero is compatible with the nonzero
source-driven history: the latter is a solution of the same continuity
operator equations but is not claimed to be the Gibbs history.

Plan-level Gate A remains open. Gate B remains unauthorized. No Ward identity,
grid, graviton, or gravity result is promoted.
