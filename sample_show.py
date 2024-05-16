import cv2
import numpy as np
import cv2
import numpy as np

# 画面の幅と高さ
width = 800
height = 800

# 白い画面を生成
image = np.ones((height, width, 3), dtype=np.uint8) * 255

# DPI
dpi = 25.4

# 半径3.0mをピクセルに変換
radius_m = 3.0
radius_px = int(radius_m * dpi)

# 中心座標
center_x = width // 2
center_y = height // 2

# 円を描画
cv2.circle(image, (center_x, center_y), radius_px, (0, 0, 0), 1)

# 画面を表示
cv2.imshow('Circle', image)
cv2.waitKey(0)
cv2.destroyAllWindows()