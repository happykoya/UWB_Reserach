import cv2
import numpy as np

# 中心座標
center = (400, 400)
# 頂点間の距離
side_length = 30  # cm

# 正三角形の頂点を計算
vertex1 = (center[0], center[1] - int(side_length * np.sqrt(3) / 2))  # 上の頂点
vertex2 = (center[0] + int(side_length / 2), center[1] + int(side_length * np.sqrt(3) / 2))  # 右下の頂点
vertex3 = (center[0] - int(side_length / 2), center[1] + int(side_length * np.sqrt(3) / 2))  # 左下の頂点

# 描画用の空の画像を作成
img = np.zeros((800, 800, 3), dtype=np.uint8) *255

# 正三角形を描画
cv2.line(img, vertex1, vertex2, (255, 255, 255), 2)
cv2.line(img, vertex2, vertex3, (255, 255, 255), 2)
cv2.line(img, vertex3, vertex1, (255, 255, 255), 2)

# 画像を表示
cv2.imshow("Triangle", img)
cv2.waitKey(0)
cv2.destroyAllWindows()