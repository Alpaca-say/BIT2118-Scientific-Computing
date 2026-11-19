# Task 6 – Solution of Systems of Linear Equations

**Code:** [`Task_06_linear_systems.py`](../code/Task_06_linear_systems.py) · [`Task_06_extension.py`](../code/Task_06_extension.py)
**Output:** [`original`](../outputs/Task_06_linear_systems_output.txt) · [`extension`](../outputs/Task_06_extension_output.txt)

## B. Inputs and mathematical operation
| Item | Value |
|---|---|
| Unknowns | x = Type A servers, y = Type B servers |
| Matrix A | [[4, 2], [8, 12]] (CPU and memory per server type) |
| Vector b | [20, 72] (total CPU units and GB observed) |
| Operation | solve A·x = b with `np.linalg.solve`, then check the residual b − A·x |

## C. Changing an input
| CPU total | memory total | Type A | Type B | comment |
|---|---|---|---|---|
| 20 | 72 | 3 | 4 | original |
| 26 | 76 | 5 | 3 | whole numbers: valid |
| 26 | 96 | 3.75 | 5.5 | fractional servers: impossible, so the data are not consistent with the model |

When I made the second row proportional to the first (A = [[4,2],[8,4]]), the determinant became 0: the equations describe the same line and there is no unique solution.

## D. Meaning of the output
3 Type A and 4 Type B servers reproduce the observed totals exactly: 4(3)+2(4) = 20 CPU and 8(3)+12(4) = 72 GB. The residual is 0 (norm 0.0), so the solution satisfies both equations. No graph is produced.

## E. Related real-world case: dairy-farm feed mix
**Assumptions (illustrative nutrient values per kg, not laboratory figures):** maize bran, sunflower cake and lucerne hay contain 0.09, 0.34 and 0.18 kg protein; 12.0, 10.5 and 8.5 MJ energy; and 0.6, 3.0 and 12.0 g calcium. A 100 kg batch must contain 17 kg protein and 1,000 MJ, and at least 450 g calcium.
**Input data:** 3 × 3 matrix (mass, protein, energy rows) and b = [100, 17, 1000].
**Output:** 35.14 kg maize bran, 13.51 kg sunflower cake, 51.35 kg lucerne; residual ≈ 10⁻¹³. Calcium delivered is 678 g (above the 450 g minimum). The condition number is 119.6.
**Interpretation:** all amounts are positive, so the recipe is feasible. A condition number around 120 means the answer is moderately sensitive: small changes in the nutrient figures can change the amounts noticeably, so the farmer should use measured values for the ingredients.
