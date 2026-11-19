"""Task 6 extension. Case: dairy-farm feed mix (3 ingredients, 3 requirements)."""
import numpy as np

# ---------- PART 1: change the observed totals ----------
A = np.array([[4.0, 2.0],[8.0, 12.0]])
print("PART 1 - changing the observed totals of the server problem")
for b in ([20,72], [26,76], [26,96]):
    x = np.linalg.solve(A, np.array(b, float))
    print(f"CPU={b[0]}, RAM={b[1]} -> Type A={x[0]:.3f}, Type B={x[1]:.3f}")
print("The last case gives fractional servers, which is physically impossible: the data/assumption is inconsistent.")
S = np.array([[4.0, 2.0],[8.0, 4.0]])
print("det of dependent system:", np.linalg.det(S), "(singular - no unique solution)")

# ---------- PART 2: feed ration ----------
# ASSUMPTIONS (illustrative nutrient values per kg of feed, not laboratory figures):
#   ingredient:        maize bran, sunflower cake, lucerne hay
#   crude protein kg:      0.09        0.34          0.18
#   energy (MJ ME):         12.0        10.5           8.5
#   calcium (g):             0.6         3.0          12.0
# Target: a 100 kg batch with 17 kg protein and 1,000 MJ energy; calcium (>= 450 g) is checked afterwards.
A = np.array([[1.0, 1.0, 1.0],      # row 1: total mass (kg)
              [0.09, 0.34, 0.18],   # row 2: protein (kg)
              [12.0, 10.5, 8.5]])   # row 3: energy (MJ)
b = np.array([100.0, 17.0, 1000.0])
x = np.linalg.solve(A, b)
print("\nPART 2 - feed mix (mass, protein, energy rows)")
print("kg of maize bran, sunflower cake, lucerne hay:", np.round(x, 2))
print("Check A@x =", np.round(A @ x, 4), " residual norm =", np.linalg.norm(b - A @ x))
ca = np.array([0.6, 3.0, 12.0]) @ x
print(f"Calcium delivered: {ca:.0f} g in 100 kg  (target 450 g -> {'OK' if ca>=450 else 'SHORT'})")
print("All amounts non-negative:", bool((x >= 0).all()))
print("Condition number of A:", round(np.linalg.cond(A), 1))
