# BIT 2118 Scientific Computing – Group Work (Individual Repository)

**Student:** _your name_ · **Reg. No.:** _your registration number_ · **Group:** _your group_

This repository contains my individual submission for the Scientific Computing group work (Tasks 2–20). For **every task** it contains:

1. the **original program** from the brief (`code/Task_XX_*.py`), run and its output saved;
2. an **extension program** (`code/Task_XX_extension.py`) that (a) changes at least one input/parameter and (b) solves a **different but related real-world case**;
3. a **write-up** (`docs/Task_XX_*.md`) covering the brief's requirements B–E:
   - **B** – input values and the mathematical operation,
   - **C** – change in an input/parameter and how the result changes,
   - **D** – the output explained in words, with graph interpretation,
   - **E** – the new case: assumptions, input data, output and interpretation.

All numbers quoted in the write-ups were produced by running the code (see `outputs/`). Graphs are in `figures/`.

## Repository structure
```
code/       original programs and extension programs (Task_02 … Task_20)
docs/       one Markdown write-up per task
outputs/    text output of every program
figures/    graphs saved by the programs
run_all.sh  re-runs everything
requirements.txt
```

## How to run
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
./run_all.sh                     # or: cd code && python Task_02_numpy_arrays.py
```
Requires Python 3.9+ and NumPy ≥ 2.0 (`np.trapezoid` in Task 16; on older NumPy use `np.trapz`). Scripts save figures to `../figures`, so run them from inside `code/`. Timing results (Tasks 3 and 7) differ slightly from computer to computer; everything else is reproducible because random generators use fixed seeds.

## Task index
| Task | Topic | Real-world case added | Write-up |
|---|---|---|---|
| 2 | NumPy arrays | greenhouse sensors (3 × 24 array) | [docs](docs/Task_02_numpy_arrays.md) |
| 3 | Vectorization | fees on 1,000,000 mobile-money payments | [docs](docs/Task_03_vectorization.md) |
| 4 | Floating-point errors | adding small money amounts a million times | [docs](docs/Task_04_numerical_errors.md) |
| 5 | Matrix algebra | drone waypoints with 3 × 3 transforms | [docs](docs/Task_05_matrix_algebra.md) |
| 6 | Linear systems | dairy-farm feed mix | [docs](docs/Task_06_linear_systems.md) |
| 7 | Gaussian elimination / LU | solar mini-grid resistor network | [docs](docs/Task_07_gaussian_lu.md) |
| 8 | Iterative methods | temperature along a 50-node rod | [docs](docs/Task_08_iterative_linear.md) |
| 9 | Eigenvalues | influence of towns in a road network | [docs](docs/Task_09_eigenvalues.md) |
| 10 | Bisection / fixed point | business break-even points | [docs](docs/Task_10_bisection_fixed_point.md) |
| 11 | Newton / secant | true interest rate of a loan | [docs](docs/Task_11_newton_secant.md) |
| 12 | Nonlinear equations | phone location from two cell towers | [docs](docs/Task_12_nonlinear_equations.md) |
| 13 | Interpolation | gaps in solar-panel output | [docs](docs/Task_13_interpolation.md) |
| 14 | Curve fitting | maize yield vs fertilizer | [docs](docs/Task_14_curve_fitting.md) |
| 15 | Numerical differentiation | matatu speed and acceleration from GPS | [docs](docs/Task_15_numerical_differentiation.md) |
| 16 | Numerical integration | estate water volume from flow readings | [docs](docs/Task_16_numerical_integration.md) |
| 17 | Euler method | logistic adoption of a mobile app | [docs](docs/Task_17_euler_ode.md) |
| 18 | `solve_ivp` | SIR epidemic model | [docs](docs/Task_18_scipy_ode.md) |
| 19 | Optimization | minimum-cost daily food plan | [docs](docs/Task_19_optimization.md) |
| 20 | Monte Carlo | will a mobile-money agent run out of cash? | [docs](docs/Task_20_monte_carlo.md) |

## Notes and assumptions
- Data in the new cases are **illustrative** (assumed prices, tariffs, nutrient values and so on), not official figures. Each write-up states its assumptions.
- One small fix to the brief's code: in Task 13 the time grid is clipped to the data range because `np.arange` with a fractional step can overshoot 14 by a rounding error, which `interp1d` rejects.
- Several programs print extra lines (for example iteration counts) so that results can be discussed in the write-ups.

## References
Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., … Oliphant, T. E. (2020). Array programming with NumPy. *Nature, 585*(7825), 357–362.

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering, 9*(3), 90–95.

Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., … SciPy 1.0 Contributors. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods, 17*(3), 261–272.
