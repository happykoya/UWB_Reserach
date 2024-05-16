import sympy as sp
import cv2
import numpy as np
import math
import itertools

# 画面の幅と高さ
IMAGE_W = 800
IMAGE_H = 800

# 白い画面を生成
IMAGE = np.ones((IMAGE_H, IMAGE_W, 3), dtype=np.uint8) * 255

#色付き描画用
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
YELLOW = (0,255,255)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 画面の中心座標
center_x = IMAGE_W // 2
center_y = IMAGE_H // 2

dpi = 25.4

vertex0_x = 400
vertex0_y = 400

vertex1_x = 420
vertex1_y = 420

vertex2_x = 400
vertex2_y = 420

print("0x,0y:",vertex0_x, vertex0_y)
print("1x,1y:",vertex1_x, vertex1_y)
print("1x,1y:",vertex2_x, vertex2_y)

list_ = [0.94,1.1200,0.77]
distance_dpi = []
ans_list = []
ansxy = []
points = []
for distance in list_:
    distance_dpi.append(int((distance*100)))
    
A = distance_dpi[0]**2 - vertex0_x**2 - vertex0_y**2
B = distance_dpi[1]**2 - vertex1_x**2 - vertex1_y**2
C = distance_dpi[2]**2 - vertex2_x**2 - vertex2_y**2

anc_x = sp.Symbol('x')
anc_y = sp.Symbol('y')
equation1 = (anc_x**2 - 2*vertex0_x*anc_x) + (anc_y**2 - 2*vertex0_y*anc_y) - A
equation2 = (anc_x**2 - 2*vertex1_x*anc_x) + (anc_y**2 - 2*vertex1_y*anc_y) - B
equation3 = (anc_x**2 - 2*vertex2_x*anc_x) + (anc_y**2 - 2*vertex2_y*anc_y) - C
variables = [equation1,equation2,equation3]

#AB,AC,BCの全てを試す
for pair in itertools.combinations(variables, 2):
    ans_list = sp.solve([pair[0], pair[1]])

    for _list in ans_list:
        try:
            if float(_list[anc_x]) > 0 and float(_list[anc_y]) > 0:
                x = int(_list[anc_x])
                y = int(_list[anc_y])
                ansxy.append((x,y))
        except:
                pass
       
print("ansxy:",ansxy)
#---------------------------------------------------------------------#
def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# すべての点の組み合わせの距離を計算し、最も距離が近い2点を見つける
min_distance = float('inf')
closest_points = None

for i in range(len(ansxy)):
    for j in range(i+1, len(ansxy)):
        point1 = ansxy[i]
        point2 = ansxy[j]
        dist = distance(point1, point2)
        if dist < min_distance:
            min_distance = dist
            closest_points = (point1, point2)

points.append(closest_points[0])
points.append(closest_points[1])

# 最も距離が近い2点の組み合わせを表示
print("Closest points:", closest_points)

# 最も距離が近い2点のうちどちらかに最も近い点を見つける
closest_point_to_closest = None
min_distance_to_closest = float('inf')

for point in ansxy:
    if point != closest_points[0] and point != closest_points[1]:
        dist_to_first = distance(point, closest_points[0])
        dist_to_second = distance(point, closest_points[1])
        if dist_to_first < min_distance_to_closest or dist_to_second < min_distance_to_closest:
            closest_point_to_closest = point
            min_distance_to_closest = min(dist_to_first, dist_to_second)

# 最も距離が近い2点のうちどちらかに最も近い点を表示
print("Closest point to the closest pair:", closest_point_to_closest)
points.append(closest_point_to_closest)


#---------------------------------------------------------------------#
def PlotUWBTagPoint():
        # 三角形を描画
        triangle_cnt = np.array( [[vertex0_x, vertex0_y], [vertex1_x, vertex1_y], [vertex2_x, vertex2_y]] )
        cv2.drawContours(IMAGE, [triangle_cnt], 0, (0, 0, 0), 1)
        
        cv2.circle(img = IMAGE,
                    center = (vertex0_x,vertex0_y),
                    radius = 3,
                    color = RED,
                    thickness = -1)

        cv2.circle(img = IMAGE,
                    center = (vertex1_x,vertex1_y),
                    radius = 3,
                    color = BLUE,
                    thickness = -1)
        
        cv2.circle(img = IMAGE,
                    center = (vertex2_x,vertex2_y),
                    radius = 3,
                    color = GREEN,
                    thickness = -1)

def PlotAnkerPoint():
    for _tuple in ansxy:
        cv2.circle(img = IMAGE, 
                   center = _tuple, 
                   radius = 5, 
                   color = BLACK,
                   thickness = -1)
        
    for _point in points:
        cv2.circle(img = IMAGE, 
                   center = _point, 
                   radius = 5, 
                   color = YELLOW,
                   thickness = -1)
        

def PlotRangeCircle():
        cv2.circle(IMAGE, (vertex0_x, vertex0_y), distance_dpi[0], RED, 3)
        cv2.circle(IMAGE, (vertex1_x, vertex1_y), distance_dpi[1], BLUE, 3)
        cv2.circle(IMAGE, (vertex2_x, vertex2_y), distance_dpi[2], GREEN, 3)
        
        #アンカーの座標をプロット
        PlotAnkerPoint()
        
        #cv2.line(IMAGE, (vertex0_x, vertex0_y), (x,y), RED, 2)
        #cv2.line(IMAGE, (vertex1_x, vertex1_y), (x,y), BLUE, 2)
        #cv2.line(IMAGE, (vertex2_x, vertex2_y), (x,y), GREEN, 2)

def ShowWindow():
    while True:
        cv2.imshow("UWB Map", IMAGE)
        cv2.waitKey(1)

PlotUWBTagPoint()
PlotRangeCircle()
ShowWindow()
#-------------------------------------------------------------#
