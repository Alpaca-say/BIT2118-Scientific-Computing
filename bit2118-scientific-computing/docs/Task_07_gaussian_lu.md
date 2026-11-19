# Task 7 – Gaussian Elimination and LU Decomposition

**Code:** [`Task_07_gaussian_lu.py`](../code/Task_07_gaussian_lu.py) · [`Task_07_extension.py`](../code/Task_07_extension.py)
**Output:** [`original`](../outputs/Task_07_gaussian_lu_output.txt) · [`extension`](../outputs/Task_07_extension_output.txt)

## B. Inputs and mathematical operation
| Item | Value |
|---|---|
| Matrix A | [[4,−1,0],[−1,4,−1],[0,−1,3]], fixed |
| Right-hand sides | three measurement vectors b = [15,10,10], [16,11,9], [14,12,11] |
| Operation | factor PA = LU **once** (`lu_factor`), then for each b do forward and back substitution (`lu_solve`); compare with `np.linalg.solve` |

## C. Changing an input
Doubling b (15,10,10 → 30,20,20) doubles the solution (5,5,5 → 10,10,10), which shows the system is linear. Changing the **size** of the problem shows the real benefit of LU: for a 600 × 600 matrix and 400 different b vectors, solving from scratch each time took 1.74 s, while factoring once and reusing L and U took 0.068 s (≈ 26× faster; the ratio varies by machine).

## D. Meaning of the output
Measurement set 1 gives (5, 5, 5), sets 2 and 3 give (5.317, 5.268, 4.756) and (4.902, 5.610, 5.537). All residual norms are about 10⁻¹⁵, i.e. zero to machine precision, and the direct solver agrees with the LU result for set 1. No graph is produced.

## E. Related real-world case: resistor network on a solar mini-grid
**Assumptions:** four nodes with the conductance matrix G (siemens) below. G is symmetric and positive definite. A solar source injects current I₁(t) = 10·sin(π(t−6)/12) A at node 1 between 06:00 and 18:00, and a constant 0.5 A load is drawn at node 4. G stays the same every hour; only the current vector changes.
G = [[3,−1,0,0],[−1,3.5,−1.5,0],[0,−1.5,3.5,−1],[0,0,−1,2]]
**Input data:** 13 hourly current vectors; G is factored once.
**Output (selected):** at 12:00 (10 A) the node voltages are [3.776, 1.328, 0.580, 0.040] V; at 09:00 [2.665, 0.924, 0.378, −0.061] V; at 06:00 and 18:00 (no sun) [−0.017, −0.052, −0.109, −0.305] V. All residuals ≤ 2×10⁻¹⁵.
**Interpretation:** node voltages follow the sun's shape and are largest nearest the source. At night the only current is the 0.5 A load, so voltages become slightly negative (the load pulls the network below the reference). Since the same matrix is used for each hour, LU decomposition is exactly the right tool.
