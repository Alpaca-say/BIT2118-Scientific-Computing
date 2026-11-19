"""Task 16 extension. Case: daily water volume of an estate from hourly flow-meter readings."""
import numpy as np
from scipy.integrate import simpson, quad
import matplotlib.pyplot as plt

# ---------- PART 1: change one reading and the sampling ----------
t = np.array([0,2,4,6,8,10,12], float)
p = np.array([0.8,1.0,1.4,1.8,1.6,1.2,0.9])
print("PART 1 - smart-meter data")
print(f"original: trapezoid={np.trapezoid(p,t):.3f}  simpson={simpson(p,x=t):.3f} kWh")
p2 = p.copy(); p2[3] = 3.0
print(f"06:00 reading 1.8 -> 3.0 kW: trapezoid={np.trapezoid(p2,t):.3f}  simpson={simpson(p2,x=t):.3f} kWh")
# accuracy test on a known function: integral of sin(x) from 0 to pi = 2
for n in (3, 5, 9, 17):
    x = np.linspace(0, np.pi, n)
    print(f"sin(x) with {n:>2} points: trapezoid error={abs(np.trapezoid(np.sin(x),x)-2):.2e}  simpson error={abs(simpson(np.sin(x),x=x)-2):.2e}")

# ---------- PART 2: estate water demand ----------
# ASSUMPTIONS: hourly flow readings (litres per second) over 24 h (25 readings); morning and evening peaks.
hrs = np.arange(0, 25, 1.0)
flow = 2 + 3.5*np.exp(-((hrs-7)/1.5)**2) + 4.0*np.exp(-((hrs-19)/2.0)**2) + 0.6*np.exp(-((hrs-13)/2.5)**2)  # L/s
sec = hrs*3600
vol_trap = np.trapezoid(flow, sec)/1000      # m^3
vol_simp = simpson(flow, x=sec)/1000
exact, _ = quad(lambda h: (2 + 3.5*np.exp(-((h-7)/1.5)**2) + 4.0*np.exp(-((h-19)/2.0)**2) + 0.6*np.exp(-((h-13)/2.5)**2))*3600, 0, 24)
exact /= 1000
price = 130.0   # KES per m^3, assumed
print("\nPART 2 - estate water volume over 24 h")
print(f"Trapezoid: {vol_trap:.2f} m^3 | Simpson: {vol_simp:.2f} m^3 | adaptive quad (reference): {exact:.2f} m^3")
print(f"Errors: trapezoid {abs(vol_trap-exact):.3f} m^3, Simpson {abs(vol_simp-exact):.3f} m^3")
print(f"Estimated daily cost at KES {price:.0f}/m^3: KES {vol_simp*price:,.0f}")
peak = hrs[flow.argmax()]
print(f"Peak flow {flow.max():.2f} L/s at {peak:.0f}:00")
share = np.trapezoid(flow[17:22], sec[17:22])/1000/vol_trap
print(f"Share of daily water used between 17:00 and 21:00: {share:.1%}")
plt.fill_between(hrs, flow, alpha=0.3); plt.plot(hrs, flow, "o-")
plt.xlabel("Hour of day"); plt.ylabel("Flow (L/s)"); plt.title("Estate water flow - area under curve = daily volume"); plt.grid(True)
plt.savefig("../figures/task16_extension_water.png", dpi=130, bbox_inches="tight")
