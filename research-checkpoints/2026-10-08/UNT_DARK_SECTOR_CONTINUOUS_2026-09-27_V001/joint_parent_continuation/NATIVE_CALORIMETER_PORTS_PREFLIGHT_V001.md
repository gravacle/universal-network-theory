# Independent native calorimeter preflight

Accepted after complete source/protocol read and a focused read of the authenticated native-operator and Chebyshev-action definitions. No producer import, scientific execution, eigenproblem or propagation was performed by this reviewer.

- `native_calorimeter_ports_v001.py`: `dd04a76c43d7b649fa1829c678924040651b96a78efa6d78dc105df78b5e40f9`.
- `NATIVE_CALORIMETER_PORTS_PROTOCOL_V001.md`: `7b343eec0228adc3a1cc4c3de0f4c42bc8c1017b5fd166932def658c22ba006c`.
- Settled mechanism note: `3fd418d5674018b7f115cce6b8bfe0b8fa0c5d1e82531e4cbcdf51c744396e65`. Its amendment adds the independently checked rational 13/16 and 25/32 kick coefficients; the earlier analytical review remains applicable with this explicitly recorded new binding.

## Implementation and scientific checks

The source authenticates the old raw result, canonical payload, complete statuses and flat transitive source manifest before loading definitions. It uses the actual saved age-dependent native states, not newly propagated/dephased preparations. Tensor order native64⊗probe0⊗probe3, number/lowering operators, edge indices 0/3, three number-state inputs and twelve on-Hamiltonians agree with the protocol. Every old state/age/frequency/duration and both prospective couplings remain, giving 648 rows, 36 independent action comparisons and 324 coupling pairs.

The reduced density formula rho=psi.T@psi.conj() correctly traces out native64 under this reshape convention. Its lowering means and cross operator give 〈sigma+_0 sigma−_3〉, hence the leading K03 entry, not its conjugate. The vacuum coherent-mean phase is −i g exp(−i omega T)〈F+〉. Ground-to-excited probabilities use emission diagonals, initially excited losses use absorption diagonals, including when the other independent probe starts excited. Connected cross subtracts the product of the actual means.

The parity/Dyson bounds are valid with ||V||≤2. For b=2|g|T, r2=cosh(b)−1 and r3=sinh(b)−b, changed-number projectors annihilate the initial state and yield 2b r3+r3²+r2². The vacuum cross operator acts only in the odd one-excitation sector, removing the r2² term. Its connected bound adds the two leading-mean/remainder cross terms and remainder product. Both absolute deviations and g-normalized coefficients are retained; no assumed factor-four error ratio is imposed. The fixed roundoff allowance is not a thermal-success tolerance or relative precision certificate for a tiny response.

All initial number states have zero interaction mean. Absolute native, probe and interaction energies are retained during the constant H_on interval, with W_on=0 and W_off=−E_interaction. The checked final free-energy increase equals this signed external switch work. Positive probe gain is therefore not mislabeled as work-free emission. The density and energy checks, eigensystem/unitarity tests, Gershgorin enclosure and independent Chebyshev vector action are appropriately distinct controls.

The worker writes no files or installs anything; only root executes and publishes stdout. A numerical failure is retained in a `FAILED_CHECKS` payload. Its main function does not turn that payload into a nonzero shell exit, so root must inspect status/failures rather than infer qualification from exit zero. This is an interpretation of the existing schema, not a requested source change.

No load-bearing defect or correction was identified. This preflight licenses the declared conditional port test, not physical photons, a Gibbs bath, irreversible rates, a cosmological temperature, or an identified actuator/contact/volume dictionary. The opposite-kick memory counterexample and the matched-energy cycle contrast remain separate exact analytical results; the new switched port experiment does not silently prepare those kicks.
