"""Task 12 extension. Case: locating a phone from distances to two cell towers (circle-circle intersection)."""
import numpy as np
from scipy.optimize import root

# ---------- PART 1: change radius and initial guess ----------
def eqs_factory(R):
    return lambda z: [z[0]**2 + z[1]**2 - R**2, z[1] - (z[0]**2 - 1)]
print("PART 1 - circle x^2+y^2=R^2 and parabola y=x^2-1")
for R, guess in [(2, [1,1]), (3, [1,1]), (3, [2,2]), (0.5, [1,1]), (2, [0,-3])]:
    f = eqs_factory(R)
    s = root(f, guess)
    res = np.abs(f(s.x)).max()
    print(f"R={R} guess={guess}: x={np.round(s.x,4)} success={s.success} max residual={res:.1e}")
print("R=0.5: the parabola never reaches the small circle, so no real intersection exists even though a solver returns a point.")
# analytic check for R=2 : y^2+y-3=0
print("Analytic y for R=2:", np.round(np.roots([1,1,-3]),4), "(the negative root gives x^2<0 -> not real)")

# ---------- PART 2: two towers ----------
# ASSUMPTIONS: tower T1 at (0,0) km, tower T2 at (6,0) km. Measured distance to T1 = 5 km, to T2 = 4 km.
def towers(z, d1=5.0, d2=4.0):
    x, y = z
    return [x**2 + y**2 - d1**2, (x-6)**2 + y**2 - d2**2]
print("\nPART 2 - phone location from two towers")
for guess in ([3,3], [3,-3]):
    s = root(towers, guess)
    print(f"guess={guess}: position=({s.x[0]:.4f}, {s.x[1]:.4f}) km, residuals={np.round(towers(s.x),12)}, success={s.success}")
x_exact = (5**2 - 4**2 + 6**2)/(2*6); y_exact = np.sqrt(25 - x_exact**2)
print(f"Analytic check: x={x_exact:.4f}, y=+/-{y_exact:.4f}")
# a third tower resolves the ambiguity
s3 = root(towers, [3,3])
d3_true = np.hypot(s3.x[0]-3, s3.x[1]-6)
d3_alt = np.hypot(s3.x[0]-3, -s3.x[1]-6)
print(f"Distance from T3 at (3,6) km to the two candidates: {d3_true:.3f} km vs {d3_alt:.3f} km -> a third range measurement picks the correct one.")
