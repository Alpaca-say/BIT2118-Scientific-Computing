"""Task 7 extension. Case: 4-node resistor network on a solar mini-grid with a source that changes each hour."""
import numpy as np, time
from scipy.linalg import lu_factor, lu_solve

# ---------- PART 1: change the measurement vector, and the matrix size ----------
A = np.array([[4,-1,0],[-1,4,-1],[0,-1,3]], float)
lu, piv = lu_factor(A)
print("PART 1a - changing b: scaling b by 2 doubles x (linearity)")
b = np.array([15,10,10], float)
print("b   ->", lu_solve((lu,piv), b))
print("2*b ->", lu_solve((lu,piv), 2*b))
print("\nPART 1b - cost: factor once vs solve from scratch, n=600, 400 right-hand sides")
rng = np.random.default_rng(0)
n, m = 600, 400
M = rng.random((n, n)) + n*np.eye(n)
B = rng.random((n, m))
t0 = time.perf_counter()
for j in range(m): np.linalg.solve(M, B[:, j])
t_direct = time.perf_counter() - t0
t0 = time.perf_counter()
f = lu_factor(M)
for j in range(m): lu_solve(f, B[:, j])
t_lu = time.perf_counter() - t0
print(f"solve each time: {t_direct:.3f}s | LU once + {m} solves: {t_lu:.3f}s | speed-up {t_direct/t_lu:.1f}x")

# ---------- PART 2: nodal analysis ----------
# ASSUMPTIONS: 4 internal nodes; conductances in siemens. Node 1 is fed by a solar source through 1 ohm.
# G*V = I where I1 = source current (A) that varies by hour; all other injections are small loads.
G = np.array([[ 3.0,-1.0, 0.0, 0.0],
              [-1.0, 3.5,-1.5, 0.0],
              [ 0.0,-1.5, 3.5,-1.0],
              [ 0.0, 0.0,-1.0, 2.0]])
lu, piv = lu_factor(G)
hours = np.arange(6, 19)
source = 10*np.maximum(0, np.sin((hours-6)*np.pi/12))      # amps injected at node 1
print("\nPART 2 - hour, source current (A), node voltages (V)")
for h, s in zip(hours, source):
    I = np.array([s, 0, 0, -0.5])        # constant 0.5 A load at node 4
    V = lu_solve((lu, piv), I)
    print(f"{h:02d}:00  I={s:5.2f}  V={np.round(V,3)}  residual={np.linalg.norm(I-G@V):.1e}")
print("G is symmetric positive definite:", np.allclose(G, G.T) and np.all(np.linalg.eigvalsh(G) > 0))
