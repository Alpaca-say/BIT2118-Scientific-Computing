"""Task 14 extension. Case: maize yield response to fertilizer."""
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def rmse(y, yh): return float(np.sqrt(np.mean((y-yh)**2)))
# ---------- PART 1: change the model degree for the server data ----------
users = np.array([50,100,150,200,250,300,350], float)
resp = np.array([82,95,115,145,185,238,305], float)
print("PART 1 - server data with polynomial models of different degree")
for deg in (1, 2, 3, 5):
    c = np.polyfit(users, resp, deg)
    print(f"degree {deg}: RMSE={rmse(resp, np.polyval(c, users)):.2f} ms | prediction at 400 users = {np.polyval(c, 400):.1f} ms")
print("Higher degree always lowers RMSE on the data, but extrapolation (400 users) becomes less trustworthy.")

# ---------- PART 2: maize yield ----------
# ASSUMPTIONS: illustrative field-trial data; fertilizer in kg/ha, yield in t/ha.
fert = np.array([0,25,50,75,100,125,150], float)
yld = np.array([1.8,2.6,3.3,3.8,4.1,4.2,4.2])
quad = lambda x, a, b, c: a*x**2 + b*x + c
sat = lambda x, ymax, k, y0: y0 + (ymax - y0)*(1 - np.exp(-k*x))
pq, _ = curve_fit(quad, fert, yld)
ps, cov = curve_fit(sat, fert, yld, p0=[4.5, 0.02, 1.8])
print("\nPART 2 - maize yield vs fertilizer")
print(f"Quadratic: y = {pq[0]:.6f}x^2 + {pq[1]:.5f}x + {pq[2]:.3f} | RMSE={rmse(yld, quad(fert,*pq)):.3f} t/ha")
print(f"Saturating: y = {ps[2]:.3f} + ({ps[0]:.3f}-{ps[2]:.3f})(1-exp(-{ps[1]:.4f}x)) | RMSE={rmse(yld, sat(fert,*ps)):.3f} t/ha")
print("Parameter standard errors (saturating):", np.round(np.sqrt(np.diag(cov)), 4))
x_opt = -pq[1]/(2*pq[0])
print(f"Quadratic peak at {x_opt:.0f} kg/ha (yield {quad(x_opt,*pq):.2f} t/ha)")
for x in (175, 200):
    print(f"Prediction at {x} kg/ha: quadratic={quad(x,*pq):.2f}, saturating={sat(x,*ps):.2f} t/ha")
xs = np.linspace(0, 200, 300)
plt.scatter(fert, yld, label="Field data", zorder=3)
plt.plot(xs, quad(xs,*pq), label="Quadratic"); plt.plot(xs, sat(xs,*ps), label="Saturating exponential")
plt.xlabel("Fertilizer (kg/ha)"); plt.ylabel("Maize yield (t/ha)"); plt.title("Maize response to fertilizer"); plt.legend(); plt.grid(True)
plt.savefig("../figures/task14_extension_maize.png", dpi=130, bbox_inches="tight")
