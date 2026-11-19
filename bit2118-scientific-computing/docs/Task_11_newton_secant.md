# Task 11 – Root Finding: Newton-Raphson and Secant Methods

**Code:** [`Task_11_newton_secant.py`](../code/Task_11_newton_secant.py) · [`Task_11_extension.py`](../code/Task_11_extension.py)
**Output:** [`original`](../outputs/Task_11_newton_secant_output.txt) · [`extension`](../outputs/Task_11_extension_output.txt)

## B. Inputs and mathematical operation
| Item | Value |
|---|---|
| Cash flows | −10,000 now, then 3,000, 3,500, 4,000, 2,500 in years 1–4 |
| Equation | NPV(r) = Σ CFₜ/(1+r)ᵗ = 0; the root r is the internal rate of return (IRR) |
| Newton-Raphson | rₙ₊₁ = rₙ − NPV(rₙ)/NPV′(rₙ), start 0.10, derivative supplied |
| Secant | same idea, derivative replaced by the slope through two points (0.05 and 0.20) |

## C. Changing an input
| initial investment | IRR |
|---|---|
| −10,000 (original) | 11.5425 % |
| −12,000 | 3.3298 % |
| −8,000 | 22.9604 % |

A larger investment for the same returns sharply lowers the IRR. I also changed the starting guess: 0.0 and 0.5 both converged to 11.5425 % (6 and 8 iterations, versus 4 from 0.10), but a start of **2.0 failed**: the first Newton step jumps to a rate below −100 %, a meaningless region. Newton is fast but needs a reasonable start.

## D. Meaning of the output
Both methods give an IRR of **11.542461 %**: the yearly return that makes the discounted inflows equal the 10,000 investment. NPV at the solution is 0.000000. Newton needed 4 iterations and secant 7: Newton's quadratic convergence is faster per step, but secant needs no derivative. If the company's cost of capital is below 11.54 %, the project adds value. No graph is produced.

## E. Related real-world case: true interest rate of a 12-month loan
**Assumptions (illustrative):** a borrower receives KES 120,000 now and repays KES 11,500 at the end of each of 12 months. We want the monthly rate r with 120,000 − Σ 11,500/(1+r)ᵗ = 0.
**Input data:** cash flows +120,000 and 12 × (−11,500).
**Output:** monthly rate **2.2185 %** (Newton, 4 iterations; secant 6 iterations); nominal annual rate 26.62 %; effective annual rate **30.12 %**; total interest KES 18,000 (15 % of the loan). If a 3 % processing fee is deducted upfront (the borrower receives 116,400), the monthly rate becomes 2.7212 % and the effective annual rate **38.01 %**.
**Interpretation:** quoting "15 % interest" hides the true cost because the borrower repays the principal gradually: the real annual rate is about 30 %, and the fee pushes it to 38 %. Comparing loans by IRR gives a fair comparison.
