"""Task 2 extension: (1) parameter change, (2) new real-world case.
Case: greenhouse temperature sensors (3 sensors x 24 hours) for a Kenyan flower/tomato farm."""
import numpy as np

# ---------- PART 1: change one input ----------
base = np.array([18.5,18.0,17.8,17.5,17.9,19.0,21.5,23.8,25.6,27.1,28.3,29.0,
                 29.4,29.1,28.5,27.6,26.2,24.8,23.4,22.1,21.0,20.2,19.6,19.0])
changed = base.copy()
changed[12] = 38.0            # one faulty/heat-spike reading at 12:00 (was 29.4)
print("PART 1 - changing the 12:00 reading from 29.4 C to 38.0 C")
for name, arr in [("original", base), ("changed", changed)]:
    print(f"{name:9s} mean={arr.mean():.2f}  min={arr.min():.2f}  max={arr.max():.2f}  "
          f"median={np.median(arr):.2f}  std={arr.std():.2f}")

# ---------- PART 2: new real-world case ----------
rng = np.random.default_rng(7)
hours = np.arange(24)
# assumption: daily sinusoidal cycle peaking ~14:00, sensor-specific offset, small noise
daily = 24 + 8*np.sin((hours - 8) * np.pi / 12)
offsets = np.array([[0.0], [1.5], [-1.0]])            # 3 sensors
readings = daily + offsets + rng.normal(0, 0.4, (3, 24))   # shape (3, 24)
readings[1, 13] += 9                                  # injected fault on sensor 2 at 13:00
print("\nPART 2 - greenhouse, array shape:", readings.shape)
print("Per-sensor mean (C):", np.round(readings.mean(axis=1), 2))
print("Per-hour mean across sensors, first 6:", np.round(readings.mean(axis=0)[:6], 2))
print("Hours above 30 C per sensor:", (readings > 30).sum(axis=1))
f = 1.8*readings + 32
print("Sensor 1 max in Fahrenheit:", round(f[0].max(), 1))
# simple anomaly detector: deviation from the other sensors' median at the same hour
med = np.median(readings, axis=0)
dev = np.abs(readings - med)
sensor, hour = np.unravel_index(dev.argmax(), dev.shape)
print(f"Largest deviation: sensor {sensor+1} at {hour:02d}:00 differs by {dev[sensor,hour]:.1f} C (suspected fault)")
