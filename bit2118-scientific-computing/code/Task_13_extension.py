"""Task 13 extension. Case: filling gaps in solar PV output (kW) measured every 1 h or 2 h."""
import numpy as np
from scipy.interpolate import interp1d, CubicSpline
import matplotlib.pyplot as plt

# ---------- PART 1: change the data (remove the 11:00 reading) ----------
hours = np.array([8,9,10,11,12,13,14], float)
temp = np.array([18.0,20.0,22.5,24.0,25.0,25.5,25.0])
print("PART 1 - original data vs data with the 11:00 value missing, estimate at 10:30 and 11:00")
keep = hours != 11
for label, h, t in [("all points", hours, temp), ("no 11:00", hours[keep], temp[keep])]:
    lin = interp1d(h, t); cub = CubicSpline(h, t)
    print(f"{label:11s}: linear(10.5)={float(lin(10.5)):.2f} cubic(10.5)={float(cub(10.5)):.2f} | linear(11)={float(lin(11)):.2f} cubic(11)={float(cub(11)):.2f}  (measured 24.00)")

# ---------- PART 2: solar PV output ----------
# ASSUMPTIONS: a 5 kW array; true output P(t)=5*sin(pi*(t-6)/12) between 06:00 and 18:00 (clear day). We pretend
# only some samples are measured, then compare interpolation with the true curve.
P = lambda t: 5*np.sin(np.pi*(np.asarray(t, float)-6)/12)
fine = np.linspace(6, 18, 721)
print("\nPART 2 - interpolation error vs the true clear-day curve (kW)")
results = {}
for step in (1, 2, 3):
    th = np.arange(6, 18+0.1, step); ph = P(th)
    lin = interp1d(th, ph); cub = CubicSpline(th, ph)
    e_lin = np.abs(lin(fine) - P(fine)); e_cub = np.abs(cub(fine) - P(fine))
    results[step] = (th, ph, lin, cub)
    print(f"sampling every {step} h: max error linear={e_lin.max():.4f}  cubic={e_cub.max():.4f}  | RMSE linear={np.sqrt((e_lin**2).mean()):.4f} cubic={np.sqrt((e_cub**2).mean()):.4f}")
t_est = 12.5
th, ph, lin, cub = results[2]
print(f"At 12:30 with 2-hourly data: true={float(P(t_est)):.3f}  linear={float(lin(t_est)):.3f}  cubic={float(cub(t_est)):.3f}")
# extrapolation warning
try:
    interp1d(th, ph)(19.0)
except ValueError as e:
    print("Asking for 19:00 (outside data range) ->", "ValueError (interp1d refuses to extrapolate)")
print("CubicSpline extrapolates silently to 19:00:", round(float(cub(19.0)), 3), "kW (true value is 0 -> misleading)")
plt.plot(fine, P(fine), "k", lw=1, label="True curve")
plt.scatter(th, ph, label="2-hourly measurements", zorder=3)
plt.plot(fine, lin(fine), label="Linear"); plt.plot(fine, cub(fine), label="Cubic spline")
plt.xlabel("Hour of day"); plt.ylabel("Solar output (kW)"); plt.title("Interpolating solar PV output"); plt.legend(); plt.grid(True)
plt.savefig("../figures/task13_extension_solar.png", dpi=130, bbox_inches="tight")
