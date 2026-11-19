"""Task 20 extension. Case: probability that a mobile-money agent runs out of cash float in one day."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ---------- PART 1: change std, capacity and N in the server-overload problem ----------
print("PART 1 - server overload, N = 100,000 unless stated (exact normal value in brackets)")
for cap, mu, sd, N, seed in [(1000,850,120,100_000,42), (1000,850,200,100_000,42), (1100,850,120,100_000,42), (1000,850,120,100,1), (1000,850,120,100,2), (1000,850,120,100,3)]:
    rng = np.random.default_rng(seed)
    p = (rng.normal(mu, sd, N) > cap).mean()
    exact = 1 - norm.cdf((cap-mu)/sd)
    se = np.sqrt(p*(1-p)/N)
    print(f"cap={cap} sd={sd} N={N:>7,} seed={seed}: estimate={p:.4%} (theory {exact:.4%}), standard error={se:.4%}")
print("Small N gives noisy answers that change with the seed; larger N or a different mean/sd shifts the risk.")

# ---------- PART 2: agent float ----------
# ASSUMPTIONS: an agent serves a random number of customers per day (Poisson mean 60). Each customer either
# withdraws (60%) a lognormal amount (median KES 2,500) or deposits (40%) a lognormal amount (median KES 3,000).
# Opening cash float = KES 150,000; cash falls with withdrawals and rises with deposits.
rng = np.random.default_rng(2024)
N = 200_000
float_cash = 150_000
min_cash = np.empty(N); end_cash = np.empty(N)
for i in range(N):
    n = rng.poisson(60)
    is_w = rng.random(n) < 0.6
    amt = rng.lognormal(np.log(np.where(is_w, 2500, 3000)), 0.8)
    path = float_cash + np.cumsum(np.where(is_w, -amt, amt))
    min_cash[i] = path.min() if n else float_cash
    end_cash[i] = path[-1] if n else float_cash
stockout = (min_cash < 0)
p = stockout.mean(); se = np.sqrt(p*(1-p)/N)
print("\nPART 2 - agent cash float simulation, 200,000 simulated days")
print(f"P(cash runs out at some point in the day) = {p:.3%}  (95% CI {p-1.96*se:.3%} to {p+1.96*se:.3%})")
print(f"Mean closing cash: KES {end_cash.mean():,.0f} | 5th percentile of closing cash: KES {np.percentile(end_cash,5):,.0f}")
for fl in (100_000, 150_000, 200_000, 250_000):
    pr = ((min_cash - float_cash + fl) < 0).mean()
    print(f"opening float KES {fl:>7,}: stock-out probability {pr:.3%}")
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].hist(end_cash/1000, bins=60); ax[0].axvline(0, color="r"); ax[0].set_xlabel("Closing cash (KES thousand)"); ax[0].set_ylabel("Number of simulated days"); ax[0].set_title("Closing cash distribution"); ax[0].grid(True)
floats = np.arange(50_000, 300_001, 10_000)
ax[1].plot(floats/1000, [((min_cash - float_cash + fl) < 0).mean()*100 for fl in floats]); ax[1].set_xlabel("Opening float (KES thousand)"); ax[1].set_ylabel("Stock-out probability (%)"); ax[1].set_title("Risk vs opening float"); ax[1].grid(True)
plt.savefig("../figures/task20_extension_float.png", dpi=130, bbox_inches="tight")
# pi estimate (textbook example)
rng = np.random.default_rng(5)
for n in (1_000, 100_000, 5_000_000):
    pts = rng.random((n, 2)); est = 4*np.mean((pts**2).sum(axis=1) <= 1)
    print(f"pi estimate with {n:>9,} points: {est:.5f} (error {abs(est-np.pi):.5f})")
