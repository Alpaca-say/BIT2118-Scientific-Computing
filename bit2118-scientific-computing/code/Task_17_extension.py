"""Task 17 extension. Case: logistic adoption of a new mobile app among 40 million potential users."""
import numpy as np
import matplotlib.pyplot as plt

def euler_cooling(h, k=0.12, T0=90.0, Ta=25.0, end=30.0):
    t = np.arange(0, end + h/2, h); T = np.zeros_like(t); T[0] = T0
    for i in range(len(t)-1): T[i+1] = T[i] + h*(-k*(T[i]-Ta))
    return t, T, Ta + (T0-Ta)*np.exp(-k*t)

# ---------- PART 1: change step size h and constant k ----------
print("PART 1 - cooling problem, final error at t=30 for different h")
for h in (5.0, 1.0, 0.1, 0.01):
    t, T, ex = euler_cooling(h)
    print(f"h={h:<5}: Euler={T[-1]:.4f}  exact={ex[-1]:.4f}  error={abs(T[-1]-ex[-1]):.5f}")
print("Halving h roughly halves the error (Euler is first-order).")
print("Stability: h*k > 2 makes Euler oscillate and blow up")
for h, k in ((10, 0.12), (20, 0.12)):
    t, T, ex = euler_cooling(h, k=k, end=100)
    print(f"h={h}, k={k}, hk={h*k:.1f}: Euler values {np.round(T[:5],1)} (exact tends to 25)")

# ---------- PART 2: logistic growth ----------
# ASSUMPTIONS: dP/dt = r P (1 - P/K), P in millions, K=40, r=0.9 per year, P0=0.5; time in years.
r, K, P0 = 0.9, 40.0, 0.5
exact = lambda t: K/(1 + (K/P0 - 1)*np.exp(-r*t))
def euler_log(h, end=10.0):
    t = np.arange(0, end + h/2, h); P = np.zeros_like(t); P[0] = P0
    for i in range(len(t)-1): P[i+1] = P[i] + h*r*P[i]*(1 - P[i]/K)
    return t, P
print("\nPART 2 - logistic adoption, users in millions")
fig, ax = plt.subplots()
tt = np.linspace(0, 10, 400); ax.plot(tt, exact(tt), "k", label="Exact")
for h in (2.0, 1.0, 0.25):
    t, P = euler_log(h)
    print(f"h={h:<4}: P(10 years) = {P[-1]:.3f} M | exact {exact(10):.3f} M | max error {np.abs(P-exact(t)).max():.3f} M")
    ax.plot(t, P, "o-", ms=3, label=f"Euler h={h}")
t_half = np.log(K/P0 - 1)/r
print(f"Exact time to reach 50% saturation (20 M users): {t_half:.2f} years")
t, P = euler_log(0.01)
print(f"Euler (h=0.01) first time above 20 M: {t[np.argmax(P>=20)]:.2f} years")
ax.set_xlabel("Years"); ax.set_ylabel("Users (millions)"); ax.set_title("Logistic app adoption, Euler vs exact"); ax.legend(); ax.grid(True)
plt.savefig("../figures/task17_extension_logistic.png", dpi=130, bbox_inches="tight")
