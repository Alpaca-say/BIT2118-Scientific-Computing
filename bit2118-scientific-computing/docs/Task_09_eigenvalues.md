# Task 9 – Eigenvalues and Eigenvectors

**Code:** [`Task_09_eigenvalues.py`](../code/Task_09_eigenvalues.py) · [`Task_09_extension.py`](../code/Task_09_extension.py)
**Output:** [`original`](../outputs/Task_09_eigenvalues_output.txt) · [`extension`](../outputs/Task_09_extension_output.txt)

## B. Inputs and mathematical operation
| Item | Value |
|---|---|
| Input | 4 × 4 adjacency matrix of an undirected network (links A–B, A–C, B–C, B–D, C–D) |
| Operation | solve Av = λv with `np.linalg.eig`, take the largest eigenvalue, normalize its eigenvector so the scores sum to 1 (eigenvector centrality), and verify ‖Av − λv‖ |

## C. Changing an input
I added the missing link **A–D**, making every node connected to every other (complete graph K₄).

| network | dominant λ | centrality (A, B, C, D) |
|---|---|---|
| original | 2.5616 | 0.2192, 0.2808, 0.2808, 0.2192 |
| with A–D | 3.0000 | 0.25, 0.25, 0.25, 0.25 |

More links raise the dominant eigenvalue and remove the differences in importance.

## D. Meaning of the output
The dominant eigenvalue 2.5616 (= (1+√17)/2) measures how strongly connected the network is. B and C score **0.2808** each and A and D **0.2192**: B and C are linked to three nodes, while A and D have only two links, and each also benefits from being linked to well-connected nodes. The verification error (≈ 1.5×10⁻¹⁵) confirms that Av = λv holds. No graph is produced.

## E. Related real-world case: influence of towns in a simplified Kenyan road network
**Assumptions:** 8 towns with simplified main-road links (not an exact road map): Nairobi–Nakuru, Nairobi–Naivasha, Naivasha–Nakuru, Nakuru–Eldoret, Eldoret–Kisumu, Nakuru–Kisumu, Nairobi–Machakos, Machakos–Mombasa, Nairobi–Mombasa, Nairobi–Nyeri. All links are treated as equal.
**Input data:** 8 × 8 symmetric adjacency matrix.
**Output:** dominant eigenvalue 2.9139.

| town | links | centrality |
|---|---|---|
| Nairobi | 5 | 0.2069 |
| Nakuru | 4 | 0.1821 |
| Naivasha | 2 | 0.1335 |
| Mombasa, Machakos | 2 | 0.1081 each |
| Eldoret, Kisumu | 2 | 0.0952 each |
| Nyeri | 1 | 0.0710 |

If Nairobi is removed, the network breaks into **3 disconnected groups** (Nakuru–Naivasha–Eldoret–Kisumu, Machakos–Mombasa, and Nyeri alone).
**Interpretation:** Nairobi and Nakuru are the most central. Naivasha beats Mombasa and Machakos even with the same number of links because it is attached to those two important towns. This shows that eigenvector centrality counts the *quality* of neighbours, not only their number, and that Nairobi is a single point of failure in this simplified model.
