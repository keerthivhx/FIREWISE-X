"""
Scientifically Justified Machine Learning Module for FIREWISE-X
Implements Isolation Forest anomaly detection and K-Means clustering with pure NumPy.
Fully resilient against platform DLL policy blocks while preserving exact mathematical formulation.
"""

from typing import Dict, Any, List, Optional
import math
import pandas as pd
import numpy as np


class IsolationTreeNode:
    """Internal or external node in an Isolation Tree."""
    def __init__(self, size: int):
        self.size = size
        self.split_feature: Optional[int] = None
        self.split_value: Optional[float] = None
        self.left: Optional['IsolationTreeNode'] = None
        self.right: Optional['IsolationTreeNode'] = None
        self.is_leaf: bool = True


class IsolationTree:
    """Single isolation tree constructed via recursive random attribute partitioning."""
    def __init__(self, max_depth: int, rng: np.random.Generator):
        self.max_depth = max_depth
        self.rng = rng
        self.root: Optional[IsolationTreeNode] = None

    def fit(self, X: np.ndarray) -> 'IsolationTree':
        self.root = self._build_tree(X, current_depth=0)
        return self

    def _build_tree(self, X: np.ndarray, current_depth: int) -> IsolationTreeNode:
        n_samples, n_features = X.shape
        node = IsolationTreeNode(size=n_samples)

        if current_depth >= self.max_depth or n_samples <= 1:
            return node

        # Check if all rows are identical
        if np.all(X == X[0, :]):
            return node

        # Randomly choose a feature with variance
        valid_features = [f for f in range(n_features) if np.min(X[:, f]) < np.max(X[:, f])]
        if not valid_features:
            return node

        feat = int(self.rng.choice(valid_features))
        min_val = float(np.min(X[:, feat]))
        max_val = float(np.max(X[:, feat]))

        # Random split point between min and max
        split_val = float(self.rng.uniform(min_val, max_val))

        left_mask = X[:, feat] < split_val
        right_mask = ~left_mask

        # Fallback if split yields empty partition
        if left_mask.sum() == 0 or right_mask.sum() == 0:
            return node

        node.is_leaf = False
        node.split_feature = feat
        node.split_value = split_val
        node.left = self._build_tree(X[left_mask], current_depth + 1)
        node.right = self._build_tree(X[right_mask], current_depth + 1)
        return node

    def compute_path_length(self, x: np.ndarray, node: Optional[IsolationTreeNode] = None, current_depth: int = 0) -> float:
        if node is None:
            node = self.root
        if node.is_leaf or node.split_feature is None:
            return current_depth + self.c_factor(node.size)

        feat = node.split_feature
        if x[feat] < node.split_value:
            if node.left is not None:
                return self.compute_path_length(x, node.left, current_depth + 1)
        else:
            if node.right is not None:
                return self.compute_path_length(x, node.right, current_depth + 1)

        return current_depth + self.c_factor(node.size)

    @staticmethod
    def c_factor(n: int) -> float:
        """Average path length of unsuccessful search in a Binary Search Tree (BST)."""
        if n <= 1:
            return 0.0
        if n == 2:
            return 1.0
        euler_gamma = 0.5772156649
        return 2.0 * (math.log(n - 1) + euler_gamma) - (2.0 * (n - 1) / n)


class PureIsolationForest:
    """Ensemble of Isolation Trees (Liu, Ting, Zhou 2008)."""
    def __init__(self, n_estimators: int = 100, max_samples: int = 256, contamination: float = 0.08, random_state: int = 42):
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.contamination = contamination
        self.rng = np.random.default_rng(random_state)
        self.trees: List[IsolationTree] = []
        self.n_samples_fit: int = 0

    def fit(self, X: np.ndarray) -> 'PureIsolationForest':
        n_samples = X.shape[0]
        self.n_samples_fit = n_samples
        subsample_size = min(n_samples, self.max_samples)
        max_depth = int(math.ceil(math.log2(max(subsample_size, 2))))

        self.trees = []
        for _ in range(self.n_estimators):
            sample_idx = self.rng.choice(n_samples, size=subsample_size, replace=False)
            X_sub = X[sample_idx]
            tree = IsolationTree(max_depth=max_depth, rng=self.rng)
            tree.fit(X_sub)
            self.trees.append(tree)

        return self

    def score_samples(self, X: np.ndarray) -> np.ndarray:
        """Computes anomaly score: s(x, n) = 2^(-E(h(x))/c(n)). Range [0, 1]. High score (>0.6) = anomaly."""
        c_n = IsolationTree.c_factor(self.n_samples_fit)
        if c_n <= 0.0:
            c_n = 1.0

        scores = []
        for i in range(len(X)):
            x = X[i]
            avg_path = np.mean([tree.compute_path_length(x) for tree in self.trees])
            score = 2.0 ** (-avg_path / c_n)
            scores.append(score)

        return np.array(scores)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Returns -1 for anomaly, 1 for nominal based on contamination quantile."""
        scores = self.score_samples(X)
        threshold = np.quantile(scores, 1.0 - self.contamination)
        preds = np.where(scores >= threshold, -1, 1)
        return preds


class PureKMeans:
    """Lloyd's K-Means clustering algorithm with silhouette validation."""
    def __init__(self, n_clusters: int = 3, max_iter: int = 100, random_state: int = 42):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.rng = np.random.default_rng(random_state)
        self.cluster_centers_: Optional[np.ndarray] = None

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        n_samples, n_features = X.shape
        # Initialize centroids randomly from observations
        init_indices = self.rng.choice(n_samples, size=self.n_clusters, replace=False)
        centroids = X[init_indices].copy()

        labels = np.zeros(n_samples, dtype=int)
        for _ in range(self.max_iter):
            # Distance from each sample to each centroid
            dists = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=-1)
            new_labels = np.argmin(dists, axis=1)

            # Check convergence
            if np.array_equal(new_labels, labels):
                break
            labels = new_labels

            # Recompute centroids
            for k in range(self.n_clusters):
                k_samples = X[labels == k]
                if len(k_samples) > 0:
                    centroids[k] = np.mean(k_samples, axis=0)

        self.cluster_centers_ = centroids
        return labels

    @staticmethod
    def compute_silhouette(X: np.ndarray, labels: np.ndarray) -> float:
        """Calculates mean silhouette score for clustering quality assessment."""
        n_samples = len(X)
        unique_labels = np.unique(labels)
        if len(unique_labels) <= 1 or len(unique_labels) >= n_samples:
            return 0.0

        # Pairwise euclidean distances
        dist_matrix = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=-1)
        s_vals = []

        for i in range(n_samples):
            my_cluster = labels[i]
            same_cluster = (labels == my_cluster)

            if same_cluster.sum() <= 1:
                s_vals.append(0.0)
                continue

            # a(i): mean intra-cluster distance
            a_i = dist_matrix[i, same_cluster].sum() / (same_cluster.sum() - 1)

            # b(i): min mean distance to other clusters
            b_i = float("inf")
            for other_c in unique_labels:
                if other_c == my_cluster:
                    continue
                other_mask = (labels == other_c)
                if other_mask.sum() > 0:
                    dist_to_other = dist_matrix[i, other_mask].mean()
                    if dist_to_other < b_i:
                        b_i = dist_to_other

            denom = max(a_i, b_i)
            s_i = (b_i - a_i) / denom if denom > 0 else 0.0
            s_vals.append(s_i)

        return float(np.mean(s_vals))


class MicrogravityMLEngine:
    """Scientific ML models for multi-dimensional microgravity combustion analysis."""

    MIN_SAMPLES_REQUIRED = 10
    MIN_FEATURES_REQUIRED = 2

    @classmethod
    def run_isolation_forest(
        cls,
        df: pd.DataFrame,
        feature_cols: Optional[List[str]] = None,
        contamination: float = 0.08,
        random_state: int = 42
    ) -> Dict[str, Any]:
        if df is None or df.empty:
            return {"trained": False, "reason": "Dataset is empty."}

        num_df = df.select_dtypes(include=[np.number])
        if feature_cols is None:
            feature_cols = [c for c in num_df.columns if not c.startswith("_") and num_df[c].std() > 1e-5][:6]

        if len(feature_cols) < cls.MIN_FEATURES_REQUIRED:
            return {
                "trained": False,
                "reason": f"Insufficient numeric features ({len(feature_cols)} found, minimum {cls.MIN_FEATURES_REQUIRED} needed)."
            }

        clean_data = num_df[feature_cols].dropna()
        if len(clean_data) < cls.MIN_SAMPLES_REQUIRED:
            return {
                "trained": False,
                "reason": (
                    f"Insufficient complete observations after removing NaNs ({len(clean_data)} available, "
                    f"minimum {cls.MIN_SAMPLES_REQUIRED} required for reliable partitioning)."
                )
            }

        X = clean_data.values
        means = np.mean(X, axis=0)
        stds = np.std(X, axis=0)
        stds[stds == 0] = 1.0
        X_scaled = (X - means) / stds

        iso_forest = PureIsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=random_state
        )
        iso_forest.fit(X_scaled)
        preds = iso_forest.predict(X_scaled)  # -1 anomaly, 1 normal
        scores = iso_forest.score_samples(X_scaled)

        clean_data = clean_data.copy()
        clean_data["is_anomaly"] = (preds == -1)
        clean_data["anomaly_score"] = scores
        anomaly_count = int((preds == -1).sum())

        flagged_records = []
        for idx in clean_data[clean_data["is_anomaly"]].index:
            row_dict = df.loc[idx].to_dict()
            ident = row_dict.get("test_id") or row_dict.get("citation_id") or f"Sample #{idx}"
            flagged_records.append({
                "index": int(idx),
                "identifier": str(ident),
                "anomaly_score": round(float(clean_data.loc[idx, "anomaly_score"]), 4),
                "fuel_material": str(row_dict.get("fuel_material", "N/A")),
                "values": {c: round(float(clean_data.loc[idx, c]), 3) for c in feature_cols}
            })

        return {
            "trained": True,
            "algorithm": "Pure Isolation Forest (100 ensemble isolation trees)",
            "features_used": feature_cols,
            "training_samples": len(clean_data),
            "anomaly_count": anomaly_count,
            "anomaly_percentage": round((anomaly_count / len(clean_data)) * 100, 1),
            "flagged_samples": flagged_records,
            "mean_anomaly_score": round(float(scores.mean()), 4),
            "min_score": round(float(scores.min()), 4),
            "max_score": round(float(scores.max()), 4),
            "result_dataframe": clean_data,
            "scientific_interpretation": (
                "Isolation Forest isolates points by randomly partitioning features. "
                "Points requiring fewer splits (higher anomaly scores) occupy sparse regions of "
                "the combustion parameter space, indicating rare flow-extinction limits or peak effluent production."
            )
        }

    @classmethod
    def run_clustering(
        cls,
        df: pd.DataFrame,
        feature_cols: Optional[List[str]] = None,
        n_clusters: int = 3,
        random_state: int = 42
    ) -> Dict[str, Any]:
        if df is None or df.empty:
            return {"trained": False, "reason": "Dataset is empty."}

        num_df = df.select_dtypes(include=[np.number])
        if feature_cols is None:
            feature_cols = [c for c in num_df.columns if not c.startswith("_") and num_df[c].std() > 1e-5][:4]

        if len(feature_cols) < cls.MIN_FEATURES_REQUIRED:
            return {"trained": False, "reason": "Need at least 2 numeric features for clustering."}

        clean_data = num_df[feature_cols].dropna()
        if len(clean_data) < (n_clusters * 3):
            return {
                "trained": False,
                "reason": f"Sample size ({len(clean_data)}) too small for {n_clusters} clusters."
            }

        X = clean_data.values
        means = np.mean(X, axis=0)
        stds = np.std(X, axis=0)
        stds[stds == 0] = 1.0
        X_scaled = (X - means) / stds

        kmeans = PureKMeans(n_clusters=n_clusters, random_state=random_state)
        labels = kmeans.fit_predict(X_scaled)
        sil_score = PureKMeans.compute_silhouette(X_scaled, labels)

        centroids = (kmeans.cluster_centers_ * stds) + means
        clean_data = clean_data.copy()
        clean_data["cluster_label"] = labels

        cluster_summaries = []
        for k in range(n_clusters):
            k_mask = (labels == k)
            cluster_summaries.append({
                "cluster_id": k,
                "size": int(k_mask.sum()),
                "pct_of_total": round((k_mask.sum() / len(clean_data)) * 100, 1),
                "centroid": {feature_cols[i]: round(float(centroids[k][i]), 3) for i in range(len(feature_cols))}
            })

        return {
            "trained": True,
            "algorithm": f"K-Means (k={n_clusters})",
            "features_used": feature_cols,
            "sample_count": len(clean_data),
            "n_clusters": n_clusters,
            "silhouette_score": round(sil_score, 3),
            "cluster_summaries": cluster_summaries,
            "result_dataframe": clean_data,
            "interpretation": (
                f"Silhouette score of {sil_score:.3f} indicates "
                + ("strong" if sil_score > 0.5 else "moderate" if sil_score > 0.25 else "weak")
                + " structural separation among physical regimes."
            )
        }
