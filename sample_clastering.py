import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# サンプルデータの作成
np.random.seed(42)
data = np.random.rand(100, 2)  # 100行2列のランダムなデータ

# KMeansクラスタリングの実行
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(data)

# 各データポイントのクラスタラベル
labels = kmeans.labels_

# クラスターごとのサイズを計算
cluster_sizes = pd.Series(labels).value_counts().sort_index()
print("クラスターごとのサイズ:")
print(cluster_sizes[0])
