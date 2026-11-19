"""Task 19 extension. Case: minimum-cost daily food plan for a student (illustrative prices and nutrients)."""
import numpy as np
from scipy.optimize import minimize

# ---------- PART 1: change cost and required capacity of the original server problem ----------
def solve(cA, cB, need):
    cons = {"type":"ineq", "fun": lambda z: 100*z[0] + 170*z[1] - need}
    r = minimize(lambda z: cA*z[0] + cB*z[1], x0=[5,3], method="SLSQP", bounds=[(0,None),(0,None)], constraints=cons)
    best = None
    for a in range(0, 40):
        for b in range(0, 40):
            if 100*a + 170*b >= need:
                c = cA*a + cB*b
                if best is None or c < best[0]: best = (c, a, b)
    return r, best
print("PART 1 - server allocation under different parameters")
for cA, cB, need in [(12,18,1000), (8,18,1000), (12,18,1500), (12,10,1000)]:
    r, best = solve(cA, cB, need)
    print(f"cost A={cA}, B={cB}, capacity>={need}: continuous A={r.x[0]:.2f}, B={r.x[1]:.2f}, cost={r.fun:.2f} | integer best (cost,A,B)={best}")
print("Cost per unit capacity: A=%.3f, B=%.3f -> the cheaper capacity wins; the optimum sits at a vertex of the feasible region." % (12/100, 18/170))

# ---------- PART 2: food plan ----------
# ASSUMPTIONS (illustrative, per 100 g): cost KES, energy kcal, protein g
foods = ["maize flour","dry beans","dagaa (small fish)","cabbage/sukuma"]
cost = np.array([ 7.0, 18.0, 35.0,  6.0])
kcal = np.array([360., 340., 310.,  30.])
prot = np.array([  8.,  21.,  55.,   2.])
need_kcal, need_prot, need_veg = 2200., 65., 2.0          # veg: at least 200 g (2 units)
f = lambda x: cost @ x
cons = [{"type":"ineq","fun": lambda x: kcal @ x - need_kcal},
        {"type":"ineq","fun": lambda x: prot @ x - need_prot},
        {"type":"ineq","fun": lambda x: x[3] - need_veg}]
bnds = [(0, 8), (0, 6), (0, 3), (0, 6)]                    # max 800 g flour, 600 g beans, 300 g dagaa, 600 g veg
r = minimize(f, x0=[4,2,1,2], method="SLSQP", bounds=bnds, constraints=cons)
print("\nPART 2 - minimum-cost daily food plan")
print("success:", r.success)
for n, q in zip(foods, r.x): print(f"{n:20s}: {q*100:6.0f} g")
print(f"Energy: {kcal@r.x:.0f} kcal (need {need_kcal:.0f}) | Protein: {prot@r.x:.1f} g (need {need_prot:.0f}) | Cost: KES {r.fun:.2f}/day")
# sensitivity: what if dagaa price doubles?
cost2 = cost.copy(); cost2[2] = 70
r2 = minimize(lambda x: cost2 @ x, x0=[4,2,1,2], method="SLSQP", bounds=bnds, constraints=cons)
print(f"If dagaa price doubles: dagaa {r2.x[2]*100:.0f} g, beans {r2.x[1]*100:.0f} g, cost KES {r2.fun:.2f}/day")
# compare with linprog (exact LP solver) for validation
from scipy.optimize import linprog
lp = linprog(cost, A_ub=-np.vstack([kcal, prot]), b_ub=-np.array([need_kcal, need_prot]),
             bounds=[(0,8),(0,6),(0,3),(2,6)])
print(f"linprog check: cost KES {lp.fun:.2f}, amounts (g) {np.round(lp.x*100)}")
