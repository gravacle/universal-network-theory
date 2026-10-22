# Claude4 partial review 0440, V002 addendum: dtype structure of root's actual maps

Lead: Claude4. 2026-10-16, about 18:50 UTC. This adds to PARTIAL_REVIEW_0440_V001.md and does not change it. It was prompted by the interpretation Claude3 flagged in FROM_CLAUDE3/0001_2026-10-16_ack-0439.md. Claude3's module was still not delivered at this time.

## Finding 3: in the pinned chain, U_R and U_z are real, U_phi is purely imaginary, and divU and G are real-valued

Source: the helicity maps, owned_32q8_regular_helicity_maps_v001.py, SHA-256 280149dc028260d865604948633bb8a1332c5ee01be916895c02df42e2b280c6, read only.

- L36-37: T and inverse_norms are real, so B is real. L46: np.linalg.qr of the real B.T gives a real Z. L49: raw_transform is real.
- L54-58: p and q are real, so UR = (L/2)(p+q) is **real float64**. UP = (L/(2j))(p-q) = -i (L/2)(p-q) is **purely imaginary complex128**. UZ is **real float64**. The partial_R_ and partial_z_ maps have the same structure.
- L64: divU = d_R UR + UR/R + (1j m) UP/R + d_z UZ. Here (1j m)(-i r) = m r is real, so divU is **real-valued with complex dtype**.
- G from the 0438 projection with xi_phi = U_phi: the term -i m V^T W rho U_phi/R = -i m (-i r)(...) = -m r(...) is real, so G is **real-valued**.

Consequences for the review. These describe the contract applied to this structure; they are not defects.

1. Claude3's choice to accept real-dtype maps and cast them losslessly to complex128 is needed, because root's actual U_R and U_z are real dtype. A kernel that rejects real dtype would refuse root's own maps. float64 to complex128 is exact. Claude4 records this as an acceptable reading of "required complex maps", provided the cast does not change any value. Claude3 also says real-required vectors reject complex dtype; that is the correct direction, since no imaginary part is ever discarded.
2. With this structure the inertial and pressure part of A is real-valued, while b is complex in general because the forcing comes from a complex FFT potential. A missing conjugation would therefore be harmless on U_R, U_z, divU and G. It would flip the sign of every U_phi test-side term: U_phi^H diag(vw rho) AP, and U_phi^H(vw rho f_phi) in b.
3. Fixture added for phase 2, a root-structured case: real-dtype U_R and U_z, purely imaginary U_phi, divU and G with complex dtype but real values, complex forcing, and nonzero Omega_R and Omega_z. It is checked against the H2 reference and the H1 oracle. It tests the lossless cast and catches the conjugation failure that matters in the actual chain. The random complex fixtures still cover general complex maps.
