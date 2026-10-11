# FIREWISE-X: Scientific Methodology & Mathematical Foundations

---

## 1. Problem Formulation: Combustion Physics in Reduced Gravity

In terrestrial gravity (\(1g\)), combustion is dominated by **natural buoyant convection**: hot, less dense gaseous reaction products rise at velocities on the order of \(1-2\text{ m/s}\), drawing cool, oxygen-rich ambient air toward the flame base.

In microgravity (\(\mu g\), \(g \approx 10^{-6} g_0\)):
1. **Buoyancy Ceases:** The Grashof number \(Gr = \frac{g \beta (T_f - T_\infty) L^3}{\nu^2} \to 0\).
2. **Diffusion Dominance:** Transport of oxygen and heat is governed strictly by molecular diffusion and forced ambient ventilation (Péclet number \(Pe = \frac{U L}{\alpha}\)).
3. **Spherical Flame Geometry:** Flames transition from teardrop-shaped plumes to rounded diffusion zones.
4. **Smoldering & Extinction Limits:** Slower heat loss allows materials to smolder at low temperatures under sub-atmospheric oxygen levels, while low convective transport can cause flame self-extinction due to product gas asphyxiation.

---

## 2. Ingestion & Transformation Pipeline

All ingested records pass through a transparent transformation pipeline:
1. **Encoding Normalization:** Standardizes UTF-8 and UTF-8-BOM (`utf-8-sig`) headers.
2. **Physical Column Invariance:** Preserves raw flight measurements while providing standardized floating-point representations.
3. **Combustion Kinetics Derivation:**
   $$\Delta [O_2] = [O_2]_{\text{final}} - [O_2]_{\text{initial}} \quad (\% \text{ vol})$$
   $$[O_2]_{\text{consumed}} = [O_2]_{\text{initial}} - [O_2]_{\text{final}} \quad (\% \text{ vol})$$
   $$\Delta [CO_2] = [CO_2]_{\text{final}} - [CO_2]_{\text{initial}} \quad (\% \text{ vol})$$
   $$\Delta [CO] = [CO]_{\text{final}} - [CO]_{\text{initial}} \quad (\text{ppm})$$

---

## 3. Data Quality & Health Score Calculation

A composite Data Health Score (\(0 \le H \le 100\)) is calculated without discarding scientifically meaningful observations:

$$H = 100 \times \left( 0.50 \cdot C + 0.30 \cdot U + 0.20 \cdot B \right)$$

Where:
* **Completeness (\(C\)):**
  $$C = 1 - \frac{\sum \text{Missing Cells}}{\text{Total Rows} \times \text{Total Columns}}$$
* **Uniqueness (\(U\)):**
  $$U = 1 - \frac{\text{Duplicate Rows}}{\text{Total Rows}}$$
* **Physical Boundary Compliance (\(B\)):**
  $$B = 1 - \frac{\text{Boundary Violations}}{\text{Total Evaluated Cells}}$$

---

## 4. Machine Learning & Anomaly Detection Formulation

### Isolation Forest (Liu, Ting, Zhou, 2008)
Isolation Forest isolates anomalies instead of profiling normal points. It constructs an ensemble of \(t=100\) random isolation trees (`iTrees`).

At each internal node:
1. A feature \(q\) is randomly chosen.
2. A split value \(p \sim \text{Uniform}(\min(X_q), \max(X_q))\) is selected.
3. The path length \(h(x)\) is the number of edges from the root to the leaf node.

The anomaly score \(s(x, n)\) is formulated as:
$$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$

Where the average path length of an unsuccessful search in a BST of \(n\) nodes is:
$$c(n) = 2\left(\ln(n - 1) + 0.5772156649\right) - \frac{2(n - 1)}{n}$$

* If \(E(h(x)) \to 0 \implies s(x, n) \to 1\): Point requires few splits to isolate \(\implies\) **Anomaly**.
* If \(E(h(x)) \to n - 1 \implies s(x, n) \to 0\): Point is deeply embedded \(\implies\) **Nominal**.

### Unsupervised Clustering & Silhouette Validation
Clustering utilizes Lloyd's algorithm with Euclidean distance, validated by the silhouette metric:
$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$
Where \(a(i)\) is mean intra-cluster distance and \(b(i)\) is minimum mean nearest-cluster distance.
