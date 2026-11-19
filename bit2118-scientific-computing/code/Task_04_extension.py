"""Task 4 extension. Case: banking - adding 10 cents a million times."""
import numpy as np, math
from decimal import Decimal

# ---------- PART 1: change the approximation of sqrt(2) ----------
print("PART 1 - improving the approximation of sqrt(2)")
true = np.sqrt(2)
for approx in (1.4, 1.41, 1.414, 1.4142, 1.41421356):
    ab = abs(true-approx); rel = ab/true
    print(f"approx={approx:<11} abs err={ab:.3e}  rel err={rel:.4%}")

# ---------- PART 2: accumulated round-off in money calculations ----------
# ASSUMPTION: a savings system credits KES 0.10 interest-like amounts 1,000,000 times; exact total = 100,000.00
n = 1_000_000
naive = 0.0
for _ in range(n):
    naive += 0.1
fsum = math.fsum([0.1]*n)
dec = sum([Decimal("0.10")]*n)
np_sum = np.sum(np.full(n, 0.1))
print("\nPART 2 - summing 0.10 one million times (true answer 100000)")
print(f"naive float loop : {naive:.10f}  error={abs(naive-100000):.3e}")
print(f"numpy sum        : {np_sum:.10f}  error={abs(np_sum-100000):.3e}")
print(f"math.fsum        : {fsum:.10f}  error={abs(fsum-100000):.3e}")
print(f"Decimal          : {dec}  (exact)")
print("naive == 100000 ?", naive == 100000, "| np.isclose ->", np.isclose(naive, 100000))
# Catastrophic cancellation / stability with another formula
print("\nStable vs direct formula, f(x)=(sqrt(1+x)-1)/x, x=1e-15")
x = 1e-15
print("direct:", (np.sqrt(1+x)-1)/x, "| stable:", 1/(np.sqrt(1+x)+1), "| true ~ 0.5")
