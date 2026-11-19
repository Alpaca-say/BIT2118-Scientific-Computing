# Task 5 – Matrix Algebra and Matrix Operations

**Code:** [`Task_05_matrix_algebra.py`](../code/Task_05_matrix_algebra.py) · [`Task_05_extension.py`](../code/Task_05_extension.py)
**Output:** [`original`](../outputs/Task_05_matrix_algebra_output.txt) · [`extension`](../outputs/Task_05_extension_output.txt)

## B. Inputs and mathematical operation
| Item | Value |
|---|---|
| Input | the four corners of a unit square, a 45° rotation matrix R and a scaling matrix S = diag(2, 1.5) |
| Operations | matrix product T = R·S, then each point p becomes T·p (written for row vectors as `points @ T.T`), and the determinant of T |

## C. Changing an input
| angle | scale (x, y) | det(T) | image of corner (1, 1) |
|---|---|---|---|
| 45° | (2, 1.5) | 3.000 | (0.354, 2.475) |
| 90° | (2, 1.5) | 3.000 | (−1.5, 2.0) |
| 45° | (1, 1) | 1.000 | (0, 1.414) |
| 45° | (2, 0) | 0.000 | (1.414, 1.414) |

The angle changes **where** the shape points but not its area (determinant stays 3); the scale factors change the area (det = sx·sy). A zero scale gives a determinant of 0: the square collapses onto a line and the transformation cannot be reversed (no inverse).

## D. Meaning of the output
The transformed square has corners (0,0), (1.414,1.414), (0.354,2.475) and (−1.061,1.061): a stretched, tilted parallelogram. The determinant **3.0** (= 2 × 1.5, because rotation has determinant 1) means the area grows from 1 to 3. Positive determinant means orientation is preserved (no mirror image). No graph is produced.

## E. Related real-world case: survey-drone waypoints using homogeneous coordinates
**Assumptions:** a drone flight plan (in metres) is drawn on a local grid. It must be scaled by 1.2 (map-unit correction), rotated by 30° to align with the field and shifted by (100, 50) m. A 3 × 3 matrix (homogeneous coordinates) lets the translation be done by multiplication too.
**Input data:** six waypoints (0,0), (50,0), (50,20), (0,20), (0,40), (50,40).
**Output:** M = T·R·S has 2×2 part [[1.0392, −0.6], [0.6, 1.0392]] and shift (100, 50). The new route runs from (100, 50) to (127.96, 121.57). All five leg lengths grew by a ratio of exactly 1.2, the determinant of the 2×2 part is 1.44 (= 1.2²) and applying M⁻¹ returns the original path (error ≈ 10⁻¹⁴).
**Interpretation:** order matters: scaling, then rotating, then translating is not the same as the reverse. Rotation and translation preserve distances and the uniform scale multiplies them by 1.2 and areas by 1.44. This is the same mathematics used in graphics and robot path planning.
