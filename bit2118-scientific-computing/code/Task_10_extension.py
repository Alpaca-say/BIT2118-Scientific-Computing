"""Task 10 extension. Case: break-even production quantity of a small business with falling price."""
import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt

# ---------- PART 1: change bracket, tolerance and starting point (heat-balance model) ----------
f = lambda T: T - 25 - 10*np.exp(-T/20)
g = lambda T: 25 + 10*np.exp(-T/20)
print("PART 1 - heat-balance problem")
for br, tol in [([20,40],1e-10), ([0,100],1e-10), ([20,40],1e-3)]:
    s = root_scalar(f, bracket=br, method="bisect", xtol=tol)
    print(f"bracket={br} xtol={tol:g}: root={s.root:.6f}, iterations={s.iterations}")
for T0 in (30.0, 10.0, 100.0):
    T, n = T0, 0
    while n < 200:
        Tn = g(T); n += 1
        if abs(Tn-T) < 1e-10: T = Tn; break
        T = Tn
    print(f"fixed point from T0={T0}: {T:.6f} in {n} iterations")
# a bad rearrangement: T = 2T - 25 - 10 exp(-T/20)  -> |g'| > 1, does not converge
bad = lambda T: 2*T - 25 - 10*np.exp(-T/20)
T = 30.0
for _ in range(10): T = bad(T)
print("bad rearrangement x=2x-f(x) after 10 steps ->", round(T, 3), "(moves away from 27.53)")

# ---------- PART 2: break-even ----------
# ASSUMPTIONS: price per unit falls with volume: p(q)=500-0.02q (KES); cost = 20,000 + 150q + 0.01q^2
profit = lambda q: q*(500 - 0.02*q) - (20000 + 150*q + 0.01*q**2)
r1 = root_scalar(profit, bracket=[1, 1000], method="bisect", xtol=1e-9)
r2 = root_scalar(profit, bracket=[5000, 20000], method="bisect", xtol=1e-9)
qmax = 350/(2*0.03)
print("\nPART 2 - break-even analysis")
print(f"Lower break-even: {r1.root:.2f} units (bisection, {r1.iterations} iterations)")
print(f"Upper break-even: {r2.root:.2f} units (bisection, {r2.iterations} iterations)")
print(f"Maximum profit at q = {qmax:.0f}: KES {profit(qmax):,.0f}")
print("Profit is positive only between the two break-even points.")
# fixed-point for the lower root: q = (20000 + 0.03 q^2)/350
q = 100.0
for k in range(100):
    qn = (20000 + 0.03*q**2)/350
    if abs(qn-q) < 1e-10: break
    q = qn
print(f"Fixed-point (q=(20000+0.03q^2)/350) lower break-even: {qn:.4f} in {k+1} iterations")
qs = np.linspace(0, 13000, 400)
plt.plot(qs, profit(qs)); plt.axhline(0, color="k", lw=0.8)
for r in (r1.root, r2.root): plt.axvline(r, ls="--", color="gray")
plt.xlabel("Units produced and sold (q)"); plt.ylabel("Profit (KES)"); plt.title("Break-even points of a small business"); plt.grid(True)
plt.savefig("../figures/task10_extension_breakeven.png", dpi=130, bbox_inches="tight")
