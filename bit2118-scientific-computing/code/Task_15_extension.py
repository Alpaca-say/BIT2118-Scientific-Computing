"""Task 15 extension. Case: matatu GPS data - speed (km/h), acceleration and over-speed detection."""
import numpy as np
import matplotlib.pyplot as plt

# ---------- PART 1: change the step size h (error of forward vs central differences) ----------
print("PART 1 - derivative of f(x)=sin(x) at x=1 (true value cos(1)=%.10f)" % np.cos(1))
for h in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-13):
    fwd = (np.sin(1+h) - np.sin(1))/h
    cen = (np.sin(1+h) - np.sin(1-h))/(2*h)
    print(f"h={h:.0e}: forward error={abs(fwd-np.cos(1)):.2e}  central error={abs(cen-np.cos(1)):.2e}")
print("Error falls as h shrinks, then rises again for very small h because of round-off (Task 4 idea).")

# ---------- PART 2: matatu ----------
# ASSUMPTIONS: GPS position along the road sampled every 5 s for 2 minutes. True speed profile: accelerate,
# cruise, brief burst of speeding, then brake. Positions have 1.5 m of GPS noise.
rng = np.random.default_rng(3)
t = np.arange(0, 125, 5.0)
v_true = np.interp(t, [0,30,60,80,100,120], [0,16,18,26,10,0])          # m/s
pos = np.concatenate([[0], np.cumsum((v_true[1:]+v_true[:-1])/2 * np.diff(t))])
noisy = pos + rng.normal(0, 1.5, t.size)
speed = np.gradient(noisy, t)                 # central differences inside, one-sided at the ends
accel = np.gradient(speed, t)
kmh = speed*3.6
limit = 80
print("\nPART 2 - matatu trip, speed limit 80 km/h")
print(f"Max estimated speed: {kmh.max():.1f} km/h at t={t[kmh.argmax()]:.0f} s | true max {v_true.max()*3.6:.1f} km/h")
over = t[kmh > limit]
print("Times above limit (s):", over.tolist())
print(f"Max acceleration {accel.max():.2f} m/s^2, max braking {accel.min():.2f} m/s^2")
harsh = t[accel < -1.5]
print("Harsh-braking instants (< -1.5 m/s^2):", harsh.tolist())
print(f"Average speed from total distance: {pos[-1]/t[-1]*3.6:.1f} km/h over {pos[-1]/1000:.2f} km")
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
ax[0].plot(t, v_true*3.6, "k", label="True speed"); ax[0].plot(t, kmh, "o-", label="From noisy GPS")
ax[0].axhline(limit, color="r", ls="--", label="Limit"); ax[0].set_xlabel("Time (s)"); ax[0].set_ylabel("Speed (km/h)"); ax[0].legend(); ax[0].grid(True); ax[0].set_title("Speed")
ax[1].plot(t, accel, "o-"); ax[1].axhline(0, color="k", lw=0.8); ax[1].set_xlabel("Time (s)"); ax[1].set_ylabel("Acceleration (m/s^2)"); ax[1].grid(True); ax[1].set_title("Acceleration (2nd derivative)")
plt.savefig("../figures/task15_extension_matatu.png", dpi=130, bbox_inches="tight")
