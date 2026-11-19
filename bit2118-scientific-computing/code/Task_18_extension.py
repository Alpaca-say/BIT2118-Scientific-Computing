"""Task 18 extension. Case: SIR epidemic model (infectious disease outbreak) with solve_ivp."""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ---------- PART 1: change R (RC circuit) ----------
print("PART 1 - RC circuit: changing the resistance (Vs=5 V, C=1 mF)")
Vs, C = 5.0, 0.001
for R in (1000.0, 4700.0, 220.0):
    sol = solve_ivp(lambda t, V: [(Vs-V[0])/(R*C)], (0, 5), [0.0], t_eval=np.linspace(0, 5, 200), rtol=1e-9, atol=1e-11)
    tau = R*C
    exact = Vs*(1-np.exp(-sol.t/tau))
    t63 = sol.t[np.argmax(sol.y[0] >= 0.632*Vs)]
    print(f"R={R:>6.0f} ohm: tau={tau:.3f} s | V(1 s)={np.interp(1, sol.t, sol.y[0]):.3f} V | V(5 s)={sol.y[0,-1]:.3f} V | time to 63% ~ {t63:.2f} s | max err={np.abs(sol.y[0]-exact).max():.1e}")
sol = solve_ivp(lambda t, V: [(0-V[0])/(1000*C)], (0, 5), [5.0], t_eval=[0,1,2,5])
print("Discharging from 5 V through 1 kohm: V at 0,1,2,5 s =", np.round(sol.y[0], 3))

# ---------- PART 2: SIR model ----------
# ASSUMPTIONS: population N = 1,000,000; 10 initially infectious; gamma = 1/10 per day (10-day infectious period).
N, I0 = 1_000_000, 10
def sir(t, y, beta, gamma):
    S, I, R = y
    return [-beta*S*I/N, beta*S*I/N - gamma*I, gamma*I]
gamma = 0.1
print("\nPART 2 - SIR outbreak (N=1,000,000)")
t_eval = np.linspace(0, 365, 366)
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for beta in (0.30, 0.20, 0.15):
    sol = solve_ivp(sir, (0, 365), [N-I0, I0, 0], t_eval=t_eval, args=(beta, gamma), rtol=1e-8, atol=1e-8)
    S, I, R = sol.y
    R0 = beta/gamma
    final = R[-1]/N
    print(f"beta={beta:.2f} (R0={R0:.1f}): peak infectious={I.max():,.0f} on day {sol.t[I.argmax()]:.0f}; total infected by day 365={final:.1%}; conservation check max |S+I+R-N|={np.abs(S+I+R-N).max():.1e}")
    ax[0].plot(sol.t, I, label=f"R0={R0:.1f}")
    if beta == 0.30:
        ax[1].plot(sol.t, S, label="Susceptible"); ax[1].plot(sol.t, I, label="Infectious"); ax[1].plot(sol.t, R, label="Recovered")
print("With R0 = 1.5 (beta=0.15) the outbreak is smaller and later, 'flattening the curve'.")
# vaccination: 40% immune at start
v = 0.4
sol = solve_ivp(sir, (0, 365), [N*(1-v)-I0, I0, N*v], t_eval=t_eval, args=(0.30, gamma), rtol=1e-8, atol=1e-8)
print(f"With 40% initially immune (beta=0.30): peak infectious={sol.y[1].max():,.0f}; herd-immunity threshold 1-1/R0 = {1-1/3:.1%}")
ax[0].set_xlabel("Day"); ax[0].set_ylabel("Infectious people"); ax[0].set_title("Effect of transmission rate"); ax[0].legend(); ax[0].grid(True)
ax[1].set_xlabel("Day"); ax[1].set_ylabel("People"); ax[1].set_title("SIR curves, R0 = 3"); ax[1].legend(); ax[1].grid(True)
plt.savefig("../figures/task18_extension_sir.png", dpi=130, bbox_inches="tight")
