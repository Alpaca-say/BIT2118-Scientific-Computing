# Task 3 – Mathematical Functions and Vectorization

**Code:** [`Task_03_vectorization.py`](../code/Task_03_vectorization.py) · [`Task_03_extension.py`](../code/Task_03_extension.py)
**Output:** [`original`](../outputs/Task_03_vectorization_output.txt) · [`extension`](../outputs/Task_03_extension_output.txt)

## B. Inputs and mathematical operation
| Item | Value |
|---|---|
| Input | 1,000,000 simulated latencies, uniform between 5 and 250 ms (seed 42) |
| Operation | convert ms → s (divide by 1000) then square: yᵢ = (xᵢ/1000)² |
| Comparison | a Python `for` loop versus the vectorized expression, timed with `timeit` |

## C. Changing an input
I changed the number of values N (the input size).

| N | loop time | vectorized time | speed-up |
|---|---|---|---|
| 10,000 | 0.0014 s | 0.00003 s | ≈ 49× |
| 1,000,000 | 0.164 s | 0.0019 s | ≈ 87× |
| 5,000,000 | 0.805 s | 0.0131 s | ≈ 61× |

Loop time grows almost linearly with N. The vectorized version also grows linearly but with a far smaller constant, so it stays 50–90× faster (exact ratios change from run to run, depending on the computer).

## D. Meaning of the output
The first five squared values (e.g. 0.0379 s²) are identical in both versions; only the method differs. The original run showed the loop taking about 0.18 s against 0.0033 s for the vectorized code, roughly **55× faster**. The reason is that NumPy executes the loop in compiled C on a contiguous block of memory, whereas Python interprets each iteration. No graph is produced.

## E. Related real-world case: transaction fees on 1,000,000 mobile-money payments
**Assumptions (illustrative tariff, not an official rate card):** fee = 0 up to KES 100; 11 up to 1,000; 30 up to 10,000; 108 up to 70,000; 0.2 % above that. Amounts are log-normal (median ≈ KES 500), clipped between 10 and 150,000. Exchange rate assumed at 129 KES per USD.
**Input data:** 1,000,000 simulated amounts (seed 1).
**Output:** total value KES 1.14 billion (≈ USD 8.9 million); total fees KES 16.1 million; average fee KES 16.15; effective fee rate 1.41 %; median transaction KES 493 and 95th percentile KES 4,166. The vectorized `np.select` was about 7× faster than the loop.
**Interpretation:** the fee is a flat amount within each band, so small payments pay a much higher percentage than large ones (the effective rate of 1.41 % is much larger than the 0.2 % charged on the largest payments). Vectorization is still faster, but less dramatically (≈7×) because `np.select` evaluates several conditions on the whole array.
