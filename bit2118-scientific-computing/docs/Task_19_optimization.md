# Task 19 – Numerical Optimization

**Code:** [`Task_19_optimization.py`](../code/Task_19_optimization.py) · [`Task_19_extension.py`](../code/Task_19_extension.py)
**Output:** [`original`](../outputs/Task_19_optimization_output.txt) · [`extension`](../outputs/Task_19_extension_output.txt)

## B. Inputs and mathematical operation
| Item | Value |
|---|---|
| Objective | minimize cost = 12x + 18y (x, y = units of Type A and B servers) |
| Constraint | capacity 100x + 170y ≥ 1000 |
| Bounds | x ≥ 0, y ≥ 0; start (5, 3) |
| Operation | `minimize` with the SLSQP method, then a search over whole-server combinations |

## C. Changing an input
| cost A | cost B | required capacity | continuous optimum | cost | best whole servers |
|---|---|---|---|---|---|
| 12 | 18 | 1000 | A 0, B 5.88 | 105.88 | 6 B, cost 108 |
| 8 | 18 | 1000 | A 10, B 0 | 80.00 | 10 A, cost 80 |
| 12 | 18 | 1500 | A 0, B 8.82 | 158.82 | 9 B, cost 162 |
| 12 | 10 | 1000 | A 0, B 5.88 | 58.82 | 6 B, cost 60 |

Making A cheaper (8) flips the answer from "all B" to "all A". Raising the capacity requirement from 1000 to 1500 raises the cost by 50 % (the constraint is active). The winner is the server with the lower **cost per unit of capacity** (A: 0.120, B: 0.106 originally).

## D. Meaning of the output
The optimizer chooses no Type A and **5.882** units of Type B, which gives exactly the required capacity of 1000 at a minimum planning cost of **105.88**. Because B is cheaper per unit capacity, every unit of capacity is bought from B and the constraint is exactly met (it is "active"). Since servers cannot be split, the best whole-server plan is 6 Type B (capacity 1020, cost 108), only 2 % more expensive. No graph is produced.

## E. Related real-world case: minimum-cost daily food plan
**Assumptions (illustrative prices and nutrient values per 100 g, not dietary advice):**

| food | cost (KES) | energy (kcal) | protein (g) |
|---|---|---|---|
| maize flour | 7 | 360 | 8 |
| dry beans | 18 | 340 | 21 |
| dagaa (small fish) | 35 | 310 | 55 |
| cabbage / sukuma | 6 | 30 | 2 |

Requirements: at least 2,200 kcal, 65 g protein and 200 g of vegetables; upper limits of 800 g flour, 600 g beans, 300 g dagaa and 600 g vegetables.
**Output:** 570 g maize flour, 0 g beans, 28 g dagaa and 200 g vegetables, giving 2,200 kcal, 65.0 g protein, cost **KES 61.71 per day**. If the dagaa price doubles, the optimum switches to 100 g beans and no dagaa, cost KES 65.00. `linprog` (an exact linear-programming solver) gave the same plan and cost, which validates the SLSQP result.
**Interpretation:** the cheapest plan is mostly maize flour for energy, plus a small amount of the most cost-effective protein. The optimum sits where the energy and protein constraints are both exactly met and the vegetable constraint is at its minimum. A price change in one food changes the plan only by a small amount in cost (+5 %), which shows how optimization supports budgeting decisions. A real plan would also need other nutrients and variety.
