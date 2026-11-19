"""Task 5 extension. Case: robotics/drone waypoints using 3x3 homogeneous matrices (rotate, scale, translate)."""
import numpy as np

# ---------- PART 1: change angle and scale ----------
def build(angle_deg, sx, sy):
    a = np.deg2rad(angle_deg)
    R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    S = np.diag([sx, sy])
    return R @ S
pts = np.array([[0,0],[1,0],[1,1],[0,1]], float)
print("PART 1 - changing parameters on the unit square")
for ang, sx, sy in [(45,2,1.5),(90,2,1.5),(45,1,1),(45,2,0)]:
    M = build(ang, sx, sy)
    out = pts @ M.T
    print(f"angle={ang:>3} scale=({sx},{sy}) det={np.linalg.det(M):6.3f}  point (1,1) -> {np.round(out[2],3)}")
print("scale y = 0 -> det 0 (singular): the square collapses to a line and cannot be inverted.")

# ---------- PART 2: homogeneous coordinates ----------
# ASSUMPTION: drone survey path in a field, local grid in metres. We rotate the path 30 deg to align
# with the field boundary, scale by 1.2 (map-unit correction) and shift by (100, 50) m.
path = np.array([[0,0],[50,0],[50,20],[0,20],[0,40],[50,40]], float)
ang = np.deg2rad(30)
R = np.array([[np.cos(ang), -np.sin(ang), 0],[np.sin(ang), np.cos(ang), 0],[0,0,1]])
S = np.diag([1.2, 1.2, 1])
T = np.array([[1,0,100],[0,1,50],[0,0,1]], float)
M = T @ R @ S                       # scale first, then rotate, then translate
hom = np.c_[path, np.ones(len(path))]
new = (hom @ M.T)[:, :2]
print("\nPART 2 - drone waypoints")
print("Combined 3x3 matrix:\n", np.round(M, 4))
print("Transformed waypoints:\n", np.round(new, 2))
# distances are preserved up to the scale factor
d_old = np.linalg.norm(np.diff(path, axis=0), axis=1)
d_new = np.linalg.norm(np.diff(new, axis=0), axis=1)
print("Leg length ratios new/old:", np.round(d_new/d_old, 3))
# inverse brings us back
back = (np.c_[new, np.ones(len(new))] @ np.linalg.inv(M).T)[:, :2]
print("Round trip error:", np.abs(back-path).max())
print("Determinant of 2x2 part:", round(np.linalg.det(M[:2,:2]),3), "(= 1.2^2, area scales by 1.44)")
