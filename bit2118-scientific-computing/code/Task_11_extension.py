"""Task 11 extension. Case: true monthly and annual interest rate of a 12-month motorbike/boda loan."""
import warnings
import numpy as np
from scipy.optimize import root_scalar
warnings.filterwarnings('ignore')

# ---------- PART 1: change initial investment and starting guess ----------
def make(cf):
    npv = lambda r: sum(c/(1+r)**t for t, c in enumerate(cf))
    d = lambda r: sum(-t*c/(1+r)**(t+1) for t, c in enumerate(cf) if t > 0)
    return npv, d
print("PART 1 - investment project (inflows 3000, 3500, 4000, 2500)")
for init in (-10000, -12000, -8000):
    npv, d = make([init, 3000, 3500, 4000, 2500])
    s = root_scalar(npv, fprime=d, x0=0.10, method="newton", xtol=1e-12)
    print(f"initial investment {init}: IRR = {s.root:.4%} (Newton, {s.iterations} iterations)")
npv, d = make([-10000, 3000, 3500, 4000, 2500])
for x0 in (0.0, 0.5, 2.0):
    s = root_scalar(npv, fprime=d, x0=x0, method="newton", xtol=1e-12)
    ok = s.converged and abs(s.root - 0.115425) < 1e-4
    msg = f"IRR={s.root:.4%} after {s.iterations} iterations" if ok else "FAILED - Newton jumped to a useless region (rate below -100%)"
    print(f"starting guess {x0}: {msg}")

# ---------- PART 2: loan ----------
# ASSUMPTIONS: loan KES 120,000 received now; 12 monthly repayments of KES 11,500 (illustrative figures).
loan, pay, n = 120_000, 11_500, 12
cf = [loan] + [-pay]*n               # borrower's perspective
npv, d = make(cf)
newton = root_scalar(npv, fprime=d, x0=0.02, method="newton", xtol=1e-12)
secant = root_scalar(npv, x0=0.01, x1=0.05, method="secant", xtol=1e-12)
m = newton.root
print("\nPART 2 - loan of KES 120,000, 12 x KES 11,500")
print(f"Monthly rate (Newton): {m:.4%} in {newton.iterations} iterations")
print(f"Monthly rate (Secant): {secant.root:.4%} in {secant.iterations} iterations")
print(f"Nominal annual rate (x12): {12*m:.2%} | effective annual rate: {(1+m)**12-1:.2%}")
print(f"Total repaid KES {pay*n:,} -> total interest KES {pay*n-loan:,} ({(pay*n-loan)/loan:.1%} of the loan)")
print(f"NPV at solution: {npv(m):.6f}")
# what if the lender adds a 3% processing fee deducted upfront?
cf2 = [loan*0.97] + [-pay]*n
npv2, d2 = make(cf2)
m2 = root_scalar(npv2, fprime=d2, x0=0.02, method="newton", xtol=1e-12).root
print(f"With a 3% upfront fee: monthly {m2:.4%}, effective annual {(1+m2)**12-1:.2%}")
