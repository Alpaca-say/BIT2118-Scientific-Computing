"""Task 3 extension. Case: mobile-money style transaction fees on 1,000,000 transactions."""
import numpy as np, timeit

# ---------- PART 1: change the array size ----------
print("PART 1 - effect of changing N (number of latency values)")
for N in (10_000, 1_000_000, 5_000_000):
    rng = np.random.default_rng(42)
    x = rng.uniform(5, 250, N)
    def loop():
        out = []
        for v in x:
            out.append((v/1000.0)**2)
        return out
    def vec():
        return (x/1000.0)**2
    tl = timeit.timeit(loop, number=1)
    tv = timeit.timeit(vec, number=3)/3
    print(f"N={N:>9,}: loop={tl:.4f}s vectorized={tv:.5f}s speed-up={tl/tv:.0f}x")

# ---------- PART 2: new case ----------
# ASSUMPTIONS (illustrative tariff, NOT an official rate card):
#   amount <=100: fee 0 ; 101-1,000: 11 ; 1,001-10,000: 30 ; 10,001-70,000: 108 ; above: 0.2% of amount
#   exchange rate 1 USD = 129 KES (assumed)
rng = np.random.default_rng(1)
amount_kes = np.round(rng.lognormal(mean=6.2, sigma=1.3, size=1_000_000))
amount_kes = np.clip(amount_kes, 10, 150_000)

def fee_loop(a):
    out = []
    for v in a:
        if v <= 100: out.append(0.0)
        elif v <= 1000: out.append(11.0)
        elif v <= 10000: out.append(30.0)
        elif v <= 70000: out.append(108.0)
        else: out.append(0.002*v)
    return out

def fee_vec(a):
    return np.select([a <= 100, a <= 1000, a <= 10000, a <= 70000],
                     [0.0, 11.0, 30.0, 108.0], default=0.002*a)

t_loop = timeit.timeit(lambda: fee_loop(amount_kes), number=1)
t_vec = timeit.timeit(lambda: fee_vec(amount_kes), number=3)/3
fees = fee_vec(amount_kes)
assert np.allclose(fees, fee_loop(amount_kes))
print("\nPART 2 - transaction fees for 1,000,000 simulated transactions")
print(f"Total value moved: KES {amount_kes.sum():,.0f}  (USD {amount_kes.sum()/129:,.0f})")
print(f"Total fees: KES {fees.sum():,.0f}  | average fee: KES {fees.mean():.2f} | effective rate {fees.sum()/amount_kes.sum():.3%}")
print(f"Median transaction: KES {np.median(amount_kes):,.0f} | 95th percentile: KES {np.percentile(amount_kes,95):,.0f}")
print(f"Loop {t_loop:.3f}s vs vectorized {t_vec:.4f}s -> {t_loop/t_vec:.0f}x faster")
