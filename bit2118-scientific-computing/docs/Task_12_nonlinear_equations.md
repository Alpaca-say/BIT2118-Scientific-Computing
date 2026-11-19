# Task 12 – Polynomial and Nonlinear Equation Solving

**Code:** [`Task_12_nonlinear_equations.py`](../code/Task_12_nonlinear_equations.py) · [`Task_12_extension.py`](../code/Task_12_extension.py)
**Output:** [`original`](../outputs/Task_12_nonlinear_equations_output.txt) · [`extension`](../outputs/Task_12_extension_output.txt)

## B. Inputs and mathematical operation
| Item | Value |
|---|---|
| Equations | circle x² + y² = 4 and parabola y = x² − 1, written as residuals F(x, y) = [x² + y² − 4, y − x² + 1] |
| Initial guesses | (1, 1) and (−1, 1) |
| Operation | `scipy.optimize.root` iterates (a Newton-type method) until both residuals are near zero |

## C. Changing an input
| radius R | guess | result | comment |
|---|---|---|---|
| 2 | (1, 1) | (1.5175, 1.3028) | original |
| 3 | (1, 1) or (2, 2) | (1.8364, 2.3723) | bigger circle, intersection moves up and out; both guesses agree |
| 0.5 | (1, 1) | solver returns (0.50, −0.50) but `success = False`, residual 0.25 | **no intersection exists** |
| 2 | (0, −3) | `success = False`, residual 0.94 | a poor guess leaves the solver stuck |

Algebra confirms the first row: substituting x² = y + 1 gives y² + y − 3 = 0, so y = 1.3028 or −2.3028. The negative root would need x² = −1.3028, which is impossible for real x, so there are only two real intersections, at x = ±1.5175.

## D. Meaning of the output
Starting at (1, 1) the solver finds **(1.5175, 1.3028)** and from (−1, 1) it finds **(−1.5175, 1.3028)**: the two points where the parabola crosses the circle, mirror images because both curves are symmetric about the y-axis. The residuals are about 10⁻¹³ and `Converged: True`, which verifies the answers. Always check `success` and the residuals, as the R = 0.5 case shows. No graph is produced.

## E. Related real-world case: locating a phone from two cell towers
**Assumptions:** tower T1 is at (0, 0) km and T2 at (6, 0) km. The phone is measured at 5 km from T1 and 4 km from T2 (distance measurements are exact).
**Equations:** x² + y² = 25 and (x − 6)² + y² = 16.
**Output:** from guess (3, 3) the solver gives **(3.7500, 3.3072) km** and from (3, −3) it gives **(3.7500, −3.3072) km**. The analytic result (x = (25 − 16 + 36)/12 = 3.75, y = ±3.3072) matches.
**Interpretation:** two circles meet at two points mirrored across the line joining the towers, so two towers cannot tell "north" from "south" of that line. A third tower resolves it: for example, a tower at (3, 6) km would measure about 2.8 km if the phone is at the upper point and 9.3 km if it is at the lower one. This is the idea behind trilateration in positioning systems.
