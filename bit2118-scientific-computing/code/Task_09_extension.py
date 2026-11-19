"""Task 9 extension. Case: influence of towns in a simplified Kenyan road network (eigenvector centrality)."""
import numpy as np

def centrality(A):
    w, v = np.linalg.eigh(A)            # symmetric matrix -> real eigenvalues
    i = np.argmax(w)
    vec = np.abs(v[:, i]); return w[i], vec / vec.sum()

# ---------- PART 1: change the network by adding the A-D link ----------
A = np.array([[0,1,1,0],[1,0,1,1],[1,1,0,1],[0,1,1,0]], float)
print("PART 1 - original vs. network with extra link A-D")
w, c = centrality(A); print(f"original: lambda={w:.4f}, centrality={np.round(c,4)}")
A2 = A.copy(); A2[0,3] = A2[3,0] = 1
w2, c2 = centrality(A2); print(f"A-D added: lambda={w2:.4f}, centrality={np.round(c2,4)}  (complete graph K4 -> lambda=3, all equal)")

# ---------- PART 2: road network ----------
# ASSUMPTION: simplified main-road links between 8 towns (undirected, unweighted); not an exact road map.
towns = ["Nairobi","Nakuru","Naivasha","Eldoret","Kisumu","Mombasa","Machakos","Nyeri"]
links = [("Nairobi","Nakuru"),("Nairobi","Naivasha"),("Naivasha","Nakuru"),("Nakuru","Eldoret"),
         ("Eldoret","Kisumu"),("Nakuru","Kisumu"),("Nairobi","Machakos"),("Machakos","Mombasa"),
         ("Nairobi","Mombasa"),("Nairobi","Nyeri")]
idx = {t:i for i,t in enumerate(towns)}
G = np.zeros((8,8))
for a,b in links: G[idx[a],idx[b]] = G[idx[b],idx[a]] = 1
w, c = centrality(G)
deg = G.sum(axis=1)
print("\nPART 2 - road network, dominant eigenvalue =", round(w,4))
print(f"{'Town':10s} degree  eigenvector-centrality")
for t in np.argsort(-c):
    print(f"{towns[t]:10s} {int(deg[t]):>5d}   {c[t]:.4f}")
# remove Nairobi to test resilience
keep = [i for i in range(8) if towns[i] != "Nairobi"]
G2 = G[np.ix_(keep, keep)]
ncomp = np.sum(np.isclose(np.linalg.eigvalsh(np.diag(G2.sum(1)) - G2), 0))
print("\nWithout Nairobi the network splits into", ncomp, "disconnected groups (graph Laplacian has that many zero eigenvalues).")
# verification
v = np.linalg.eigh(G)[1][:, -1]
print("Verification ||Gv - lambda v|| =", np.linalg.norm(G@v - w*v))
