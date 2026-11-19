"""Task 8 extension. Case: steady temperature along a 50-node metal rod (jiko/stove cooking skewer), one end heated."""
import numpy as np
import matplotlib.pyplot as plt

def jacobi(A, b, tol=1e-8, max_iter=20000):
    D = np.diag(A); R = A - np.diagflat(D); x = np.zeros_like(b); err = []
    for _ in range(max_iter):
        xn = (b - R @ x) / D
        e = np.linalg.norm(xn - x, np.inf); err.append(e); x = xn
        if e < tol: break
    return x, err

def gauss_seidel(A, b, tol=1e-8, max_iter=20000):
    x = np.zeros_like(b); err = []
    for _ in range(max_iter):
        old = x.copy()
        for i in range(len(b)):
            x[i] = (b[i] - A[i,:i] @ x[:i] - A[i,i+1:] @ old[i+1:]) / A[i,i]
        e = np.linalg.norm(x - old, np.inf); err.append(e)
        if e < tol: break
    return x, err

def rod(n, left, right):
    A = 2*np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)
    b = np.zeros(n); b[0] = left; b[-1] = right
    return A, b

# ---------- PART 1: change boundary temperature and tolerance (original 5-node model) ----------
print("PART 1 - original 5-node model")
for left, tol in [(100, 1e-8), (150, 1e-8), (100, 1e-3)]:
    A, b = rod(5, left, 20)
    xj, ej = jacobi(A, b, tol); xg, eg = gauss_seidel(A, b, tol)
    print(f"left={left} tol={tol:g}: Jacobi {len(ej)} it, Gauss-Seidel {len(eg)} it, "
          f"max |x_J - exact| = {np.abs(xj-np.linalg.solve(A,b)).max():.2e}")
# a matrix that is NOT diagonally dominant
Bad = np.array([[1., 3.],[4., 1.]]); bb = np.array([1., 2.])
xbad, ebad = jacobi(Bad, bb, max_iter=50)
print("Non-dominant matrix after 50 Jacobi steps: last change =", f"{ebad[-1]:.2e}", "(diverges)")

# ---------- PART 2: 50-node rod ----------
n = 50
A, b = rod(n, 180.0, 25.0)       # assumption: hot end 180 C, ambient end 25 C (units: degrees C)
xj, ej = jacobi(A, b); xg, eg = gauss_seidel(A, b)
exact = np.linalg.solve(A, b)
print("\nPART 2 - 50-node rod, hot end 180 C, cold end 25 C")
print(f"Jacobi iterations: {len(ej)} | Gauss-Seidel iterations: {len(eg)}")
print(f"Max error Jacobi: {np.abs(xj-exact).max():.2e} | Gauss-Seidel: {np.abs(xg-exact).max():.2e}")
print("Temperature at nodes 1, 10, 25, 40, 50:", np.round(exact[[0,9,24,39,49]], 2))
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
ax[0].plot(np.arange(1, n+1), exact, label="Direct solution")
ax[0].plot(np.arange(1, n+1), xg, "--", label="Gauss-Seidel")
ax[0].set_xlabel("Node along rod"); ax[0].set_ylabel("Temperature (C)"); ax[0].set_title("Steady temperature profile"); ax[0].legend(); ax[0].grid(True)
ax[1].semilogy(ej, label="Jacobi"); ax[1].semilogy(eg, label="Gauss-Seidel")
ax[1].set_xlabel("Iteration"); ax[1].set_ylabel("Maximum change"); ax[1].set_title("Convergence (50 nodes)"); ax[1].legend(); ax[1].grid(True)
plt.savefig("../figures/task08_extension_rod.png", dpi=130, bbox_inches="tight")
