# Task 2 – NumPy Arrays and Numerical Computation

**Code:** [`Task_02_numpy_arrays.py`](../code/Task_02_numpy_arrays.py) · [`Task_02_extension.py`](../code/Task_02_extension.py)
**Output:** [`original`](../outputs/Task_02_numpy_arrays_output.txt) · [`extension`](../outputs/Task_02_extension_output.txt)

## B. Inputs and mathematical operation
| Item | Value |
|---|---|
| Input | 24 hourly temperatures in °C (17.5 to 29.4), stored in one NumPy array |
| Operations | mean = Σxᵢ/n, minimum, maximum, and the vectorized conversion F = 1.8C + 32 applied to every element at once |

## C. Changing an input
I changed the 12:00 reading from **29.4 °C to 38.0 °C** (a heat spike or faulty sensor).

| | mean | min | max | median | std |
|---|---|---|---|---|---|
| original | 23.12 | 17.50 | 29.40 | 22.75 | 4.17 |
| changed | 23.48 | 17.50 | 38.00 | 22.75 | 4.99 |

The mean rises by 0.36 °C (the extra 8.6 °C is shared over 24 readings), the maximum jumps by the full 8.6 °C, and the standard deviation increases. The **median did not move**, which shows why the median is more robust against a single bad sensor reading.

## D. Meaning of the output
The daily mean is **23.12 °C**, the coldest hour was 17.50 °C (early morning) and the warmest 29.40 °C (around midday). The first six Fahrenheit values (65.3 … 66.2 °F) are the same readings on another scale; no loop was needed because NumPy applies `1.8*x + 32` to the whole array. There is no graph in this task.

## E. Related real-world case: greenhouse monitoring with 3 sensors
**Assumptions:** three sensors record hourly for 24 h; temperature follows a daily sine cycle (mean 24 °C, amplitude 8 °C) plus sensor offsets (0, +1.5, −1.0 °C) and small random noise (σ = 0.4 °C); a fault of +9 °C is injected on sensor 2 at 13:00. Crops are stressed above 30 °C.
**Input data:** a 3 × 24 array (`readings`), generated with seed 7 so results are reproducible.
**Output (summary):**
- Per-sensor means: 23.84, 25.77 and 23.00 °C.
- Hours above 30 °C: 5, 7 and 4 for sensors 1, 2 and 3.
- The anomaly detector (distance from the median of the three sensors at the same hour) flagged **sensor 2 at 13:00, 11.2 °C away**.

**Interpretation:** `axis=1` gives one statistic per sensor and `axis=0` one per hour, so a 2-D array replaces many loops. Sensor 2 reports the highest mean and the most hot hours, but part of that is the injected fault, so a farmer should check the sensor before switching on shading or ventilation.
