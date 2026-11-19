# Task 4 – Floating-Point Arithmetic and Numerical Errors

**Code:** [`Task_04_numerical_errors.py`](../code/Task_04_numerical_errors.py) · [`Task_04_extension.py`](../code/Task_04_extension.py)
**Output:** [`original`](../outputs/Task_04_numerical_errors_output.txt) · [`extension`](../outputs/Task_04_extension_output.txt)

## B. Inputs and mathematical operation
| Item | Value |
|---|---|
| Inputs | 0.1 + 0.2 vs 0.3; true √2 vs approximation 1.414; x = 10⁻⁴, 10⁻⁸, 10⁻¹² |
| Operations | absolute error \|true − approx\|, relative error = absolute/\|true\|, and two algebraically equal formulas for (√(1+x) − 1)/x |

## C. Changing an input
I replaced the approximation 1.414 with better and worse values of √2:

| approximation | absolute error | relative error |
|---|---|---|
| 1.4 | 1.42×10⁻² | 1.0051 % |
| 1.41 | 4.21×10⁻³ | 0.2979 % |
| 1.414 | 2.14×10⁻⁴ | 0.0151 % |
| 1.4142 | 1.36×10⁻⁵ | 0.0010 % |
| 1.41421356 | 2.4×10⁻⁹ | ≈ 0 % |

Each extra correct digit cuts the error by about ten times. Truncation (not computer precision) is the source of this error.

## D. Meaning of the output
- `0.1 + 0.2 = 0.30000000000000004` and `== 0.3` is **False**, because 0.1 and 0.2 cannot be stored exactly in binary. `np.isclose` returns True because it accepts a tiny tolerance.
- Absolute error 0.00021356 and relative error 0.0151 % match the hand calculation in the brief.
- For x = 10⁻¹², the "direct" formula gives 0.500044450291 while the stable one gives 0.500000000000. The true answer is ≈ 0.5, so the direct formula has an error of about 4.4×10⁻⁵. Subtracting two almost equal numbers (√(1+x) and 1) destroys significant digits (catastrophic cancellation). The rewritten form 1/(√(1+x)+1) avoids the subtraction. No graph is produced.

## E. Related real-world case: accumulating small money amounts
**Assumptions:** a banking system adds KES 0.10 exactly 1,000,000 times; the true total is KES 100,000.00.
**Input data:** 1,000,000 copies of 0.1.
**Output:**
| method | result | error |
|---|---|---|
| plain float loop | 100000.0000013329 | 1.3×10⁻⁶ |
| `np.sum` | 100000.0000000000 | 2.9×10⁻¹¹ |
| `math.fsum` | 100000.0000000000 | 0 |
| `Decimal` | 100000.00 | exact |

**Interpretation:** the naive loop's answer is not equal to 100000 (`==` gives False) because small round-off errors accumulate. `np.sum` uses pairwise summation, `fsum` tracks the lost bits, and `Decimal` stores decimal fractions exactly, so for money it is the safest choice. A second test with x = 10⁻¹⁵ shows the direct formula returning 0.444 against a true value of 0.5 (an 11 % error), while the stable form gives 0.4999999999999999.
