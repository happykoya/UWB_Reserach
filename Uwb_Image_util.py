#!/usr/bin/env python3
#-*- coding: utf-8 -*
#Date:2024/04/18 ~ 
#Author:Koya Okuse
#UWB研究用のUtil関数(画像出力用)
import serial.tools.list_ports
from pprint import pprint as pp
import cv2
import numpy as np
import math
import sympy as sp
import itertools
import pandas as pd

#色付き描画用
#BGR
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

YELLOW = (0, 255, 255)
FUNCIA = (255, 0, 255)
MAROON = (0, 0, 128)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 画面の幅と高さ
IMAGE_W = 800
IMAGE_H = 800

#フォント設定
FONT =  cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_THINKNESS = 1

# 白い画面を生成
IMAGE = np.ones((IMAGE_H, IMAGE_W, 3), dtype=np.uint8) * 255

# 画面の中心座標
center_x = IMAGE_W // 2
center_y = IMAGE_H // 2

class ImageDrawer(object):
    def __init__(self):
        self.uwb_tag = ["TagID:0","TagID:1","TagID:2"]
        self.uwb_ank = ["AnkerID:0","AnkerID:1","AnkerID:2"]
        self.text_size0 = cv2.getTextSize(self.uwb_tag[0], FONT, FONT_SCALE, FONT_THINKNESS)[0]
        self.text_size1 = cv2.getTextSize(self.uwb_tag[1], FONT, FONT_SCALE, FONT_THINKNESS)[0]
        self.text_size2 = cv2.getTextSize(self.uwb_tag[2], FONT, FONT_SCALE, FONT_THINKNESS)[0]
        
        self.text_size0_ank = cv2.getTextSize(self.uwb_ank[0], FONT, FONT_SCALE, FONT_THINKNESS)[0]
        self.text_size1_ank = cv2.getTextSize(self.uwb_ank[1], FONT, FONT_SCALE, FONT_THINKNESS)[0]
        self.text_size2_ank = cv2.getTextSize(self.uwb_ank[2], FONT, FONT_SCALE, FONT_THINKNESS)[0]
        
        self.dpi = 25.4
        self.vertex0_x = center_x
        self.vertex0_y = center_y - int(10 / self.dpi * 96)  # cmをピクセルに変換 (96self.dpiを仮定)
        self.text0_x = self.vertex0_x - self.text_size0[0] // 2
        self.text0_y = self.vertex0_y - 10  # テキストの位置を微調整
        
        self.vertex1_x = center_x - int(10 / self.dpi * 96 * np.cos(np.radians(30)))  # 30度の角度を考慮
        self.vertex1_y = center_y + int(10 / self.dpi * 96 * np.sin(np.radians(30)))  # 30度の角度を考慮
        self.text1_x = self.vertex1_x - self.text_size1[0] // 2
        self.text1_y = self.vertex1_y - 10  # テキストの位置を微調整
        
        self.vertex2_x = center_x + int(10 / self.dpi * 96 * np.cos(np.radians(30)))  # 30度の角度を考慮
        self.vertex2_y = center_y + int(10 / self.dpi * 96 * np.sin(np.radians(30)))  # 30度の角度を考慮
        self.text2_x = self.vertex2_x - self.text_size2[0] // 2
        self.text2_y = self.vertex2_y - 10  # テキストの位置を微調整
        
        self.vertex_list = [(self.vertex0_x, self.vertex0_y),
                            (self.vertex1_x, self.vertex1_y),
                            (self.vertex2_x, self.vertex2_y)]
        self.anc_x = None
        self.anc_y = None
        
    def PlotUWBTagPoint(self):
        # 三角形を描画
        triangle_cnt = np.array( [[self.vertex0_x, self.vertex0_y], [self.vertex1_x, self.vertex1_y], [self.vertex2_x, self.vertex2_y]] )
        cv2.drawContours(IMAGE, [triangle_cnt], 0, (0, 0, 0), 1)
        
        cv2.circle(img = IMAGE,
                    center = (self.vertex0_x,self.vertex0_y),
                    radius = 3,
                    color = RED,
                    thickness = -1)

        cv2.circle(img = IMAGE,
                    center = (self.vertex1_x,self.vertex1_y),
                    radius = 3,
                    color = BLUE,
                    thickness = -1)
        
        cv2.circle(img = IMAGE,
                    center = (self.vertex2_x,self.vertex2_y),
                    radius = 3,
                    color = GREEN,
                    thickness = -1)
        
    def PlotRangeCircle(self, result_dict):
        range_data = float(result_dict["Range_data"])
        #print(result_dict)
        #範囲を示す円の半径を計算
        radius_px = int(range_data*100)
        if result_dict["Tag_id"] == 0:
            cv2.circle(IMAGE, (self.vertex0_x, self.vertex0_y), radius_px, RED, 3)
            
        elif result_dict["Tag_id"] == 1:
            cv2.circle(IMAGE, (self.vertex1_x, self.vertex1_y), radius_px, BLUE, 3)
        
        elif result_dict["Tag_id"] == 2:
            cv2.circle(IMAGE, (self.vertex2_x, self.vertex2_y), radius_px, GREEN, 3)
    
    def PlotAnkerPoint(self,distance_list):
        distance_m = []
        ancker_point = []
        for distance in distance_list:
            distance_m.append(int(float(distance[2])*100))
        
        self.anc_x, self.anc_y = self.FindCoord(distance_m=distance_m)
        try:
            self.text1_x_ank = self.anc_x - self.text_size1_ank[0] // 2
            self.text1_y_ank = self.anc_y - 10
        except:
            self.text1_x_ank = None
            self.text1_y_ank = None
            
        if self.anc_x != None and self.anc_y != None:
            #アンカーの座標をプロット
            cv2.circle(img = IMAGE,
                        center = (self.anc_x, self.anc_y),
                        radius = 4,
                        color = BLACK,
                        thickness = -1)
            #cv2.line(IMAGE, self.vertex_list[0], (self.anc_x,self.anc_y), RED, 2)
            #cv2.line(IMAGE, self.vertex_list[1], (self.anc_x,self.anc_y), BLUE, 2)
            #cv2.line(IMAGE, self.vertex_list[2], (self.anc_x,self.anc_y), GREEN, 2)
                
    def FindCoord(self, distance_m):
        #UWBで取得できる検出円には誤差が認められるため,
        #推定されたAnkerの位置群から重心を算出する
        ans_list = []
        estimation_xy = []
        A = distance_m[0]**2 - self.vertex0_x**2 - self.vertex0_y**2
        B = distance_m[1]**2 - self.vertex1_x**2 - self.vertex1_y**2
        C = distance_m[1]**2 - self.vertex2_x**2 - self.vertex2_y**2
        anc_x = sp.Symbol('x')
        anc_y = sp.Symbol('y')
        equation1 = (anc_x**2 - 2*self.vertex0_x*anc_x) + (anc_y**2 - 2*self.vertex0_y*anc_y) - A
        equation2 = (anc_x**2 - 2*self.vertex1_x*anc_x) + (anc_y**2 - 2*self.vertex1_y*anc_y) - B
        equation3 = (anc_x**2 - 2*self.vertex2_x*anc_x) + (anc_y**2 - 2*self.vertex2_y*anc_y) - C
        variables = [equation1,equation2,equation3]
        
        #AB,AC,BCの全てを試す
        for pair in itertools.combinations(variables, 2):
            ans_list = sp.solve([pair[0], pair[1]])

            for _list in ans_list:
                try:
                    if float(_list[anc_x]) > 0 and float(_list[anc_y]) > 0:
                        x = int(_list[anc_x])
                        y = int(_list[anc_y])
                        estimation_xy.append((x,y))
                except:
                        pass
        if len(estimation_xy)  == 0: return None, None
        elif len(estimation_xy) == 1: return estimation_xy[0][0], estimation_xy[0][1]
        elif len(estimation_xy) == 2: return self.CalculateCentroid(estimation_xy)
        else:
            points = []
            closest_point_to_closest = None
            min_distance_to_closest = float('inf')
            # すべての点の組み合わせの距離を計算し、最も距離が近い2点を見つける
            # その2点のうちどちらかに最も近い距離の点,合計3点を求める   
            min_distance = float('inf')
            closest_points = None
            
            for i in range(len(estimation_xy)):
                for j in range(i+1, len(estimation_xy)):
                    point1 = estimation_xy[i]
                    point2 = estimation_xy[j]
                    dist = self.GetDistance(point1, point2)
                    if dist < min_distance:
                        min_distance = dist
                        closest_points = (point1, point2)
            
            points.append(closest_points[0])
            points.append(closest_points[1])
            
            for point in estimation_xy:
                if point != closest_points[0] and point != closest_points[1]:
                    dist_to_first = self.GetDistance(point, closest_points[0])
                    dist_to_second = self.GetDistance(point, closest_points[1])
                    if dist_to_first < min_distance_to_closest or dist_to_second < min_distance_to_closest:
                        closest_point_to_closest = point
                        min_distance_to_closest = min(dist_to_first, dist_to_second)
                        
            points.append(closest_point_to_closest)           
            return self.CalculateCentroid(points=points)


#------------------------------------------------------------------------------------------#
    def PlotAnkerEstimationPoint(self,data_labels, anker_points_cluster, cluster_sizes):
        sorted_series = cluster_sizes.sort_values(ascending=False)
        if len(data_labels) == len(anker_points_cluster):
            for i in range(len(anker_points_cluster)):
                #アンカーの座標をプロット
                if data_labels[i] == sorted_series.index[0]:
                    cv2.circle(img = IMAGE,
                                center = anker_points_cluster[i],
                                radius = 5,
                                color = YELLOW,
                                thickness = -1)
                    
                if data_labels[i] == sorted_series.index[1]:
                    cv2.circle(img = IMAGE,
                                center = anker_points_cluster[i],
                                radius = 5,
                                color = FUNCIA,
                                thickness = -1)
                
                if data_labels[i] == sorted_series.index[2]:
                    cv2.circle(img = IMAGE,
                                center = anker_points_cluster[i],
                                radius = 5,
                                color = MAROON,
                                thickness = -1)
    
    def FindCoordEstimation(self, distance_list):
        distance_m = []
        for distance in distance_list:
            distance_m.append(int(float(distance[2])*100))
            
        ans_list = []
        estimation_xy = []
        A = distance_m[0]**2 - self.vertex0_x**2 - self.vertex0_y**2
        B = distance_m[1]**2 - self.vertex1_x**2 - self.vertex1_y**2
        C = distance_m[1]**2 - self.vertex2_x**2 - self.vertex2_y**2
        anc_x = sp.Symbol('x')
        anc_y = sp.Symbol('y')
        equation1 = (anc_x**2 - 2*self.vertex0_x*anc_x) + (anc_y**2 - 2*self.vertex0_y*anc_y) - A
        equation2 = (anc_x**2 - 2*self.vertex1_x*anc_x) + (anc_y**2 - 2*self.vertex1_y*anc_y) - B
        equation3 = (anc_x**2 - 2*self.vertex2_x*anc_x) + (anc_y**2 - 2*self.vertex2_y*anc_y) - C
        variables = [equation1,equation2,equation3]
        
        #AB,AC,BCの全てを試す
        for pair in itertools.combinations(variables, 2):
            ans_list = sp.solve([pair[0], pair[1]])

            for _list in ans_list:
                try:
                    if float(_list[anc_x]) > 0 and float(_list[anc_y]) > 0:
                        x = int(_list[anc_x])
                        y = int(_list[anc_y])
                        estimation_xy.append((x,y))
                except:
                        pass
                    
        return estimation_xy
#------------------------------------------------------------------------------------------#
    def GetDistance(self,point1,point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def CalculateCentroid(self, points):
        if len(points) < 2:
            raise ValueError("At least two points are required.")

        # 座標の合計を初期化
        sum_x = 0
        sum_y = 0

        # 各点の座標の合計を計算
        for point in points:
            sum_x += point[0]  # x座標の合計
            sum_y += point[1]  # y座標の合計

        # x座標の平均値を計算
        centroid_x = int(sum_x / len(points))
        # y座標の平均値を計算
        centroid_y = int(sum_y / len(points))
        return centroid_x, centroid_y

    
    def ShowComment(self):
        cv2.putText(IMAGE, self.uwb_tag[0], (self.text0_x, self.text0_y), FONT, FONT_SCALE, (0, 0, 0), FONT_THINKNESS)
        cv2.putText(IMAGE, self.uwb_tag[1], (self.text1_x, self.text1_y), FONT, FONT_SCALE, (0, 0, 0), FONT_THINKNESS)
        cv2.putText(IMAGE, self.uwb_tag[2], (self.text2_x, self.text2_y), FONT, FONT_SCALE, (0, 0, 0), FONT_THINKNESS)
        try:
            cv2.putText(IMAGE, self.uwb_ank[1], (self.text1_x_ank, self.text1_y_ank), FONT, FONT_SCALE, (0, 0, 0), FONT_THINKNESS)
        except:
            pass
        
    def ShowWindow(self):
        cv2.imshow("UWB Map", IMAGE)
        cv2.waitKey(1)
    

if __name__ == '__main__':
    image = ImageDrawer()
    image.ShowComment()
    image.PlotUWBTagPoint()
    image.ShowWindow()