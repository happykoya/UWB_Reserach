#!/usr/bin/env python3
#-*- coding: utf-8 -*
#Date:2024/04/18 ~ 
#Author:Koya Okuse
#UWBデータから推定距離を取得する
import serial
import serial.tools.list_ports
from pprint import pprint as pp
import json
import cv2
import time
import numpy as np
import math
import re
import sys
import struct
from collections import deque

from Uwb_util import (Get_ALLCom,ReadData,ReadTagData,DistanceData,PredictBirch,PredictKMeans)
from Uwb_Image_util import ImageDrawer, IMAGE

UWB_DATA = [{"anc":0,"tag":0},{"anc":0,"tag":1},{"anc":0,"tag":2},
            {"anc":1,"tag":0},{"anc":1,"tag":1},{"anc":1,"tag":2},
            {"anc":2,"tag":0},{"anc":2,"tag":1},{"anc":2,"tag":2}]
instance_list = []

#--------------------------------------------------------------#
class UWB:
    def __init__(self,anc_id, tag_id):
        self.anc_id = anc_id
        self.tag_id = tag_id
        self.distance = None
        
    def GetRangeData(self,result_dict):
        self.distance = result_dict["Range_data"]


def MakeUWBInstance():
    for uwb in UWB_DATA:
        instance_list.append(UWB(uwb["anc"],uwb["tag"]))

def UpdateData(tmp_dict):
    for instance in instance_list:
        if instance.anc_id == tmp_dict["Anker_id"] and instance.tag_id == tmp_dict["Tag_id"]:
            instance.GetRangeData(tmp_dict)

#--------------------------------------------------------------#
#ser = serial.Serial(Get_FristCom(), 115200)
#ser.write("begin".encode('UTF-8'))
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
image = ImageDrawer()
ser = Get_ALLCom()
for s in ser:
    s.write("begin".encode('UTF-8'))


def ANC_main():
    while True:
        ReadData(ser=ser)
        print("------------------------------------")
        ser.write("begin".encode('UTF-8'))
        ser.reset_input_buffer()

def TAG_main():
    while True:
        distance_list = []
        current_anker_points = []
        IMAGE.fill(255)
        for s in ser:
            tmp_dict = ReadTagData(ser=s)
            UpdateData(tmp_dict=tmp_dict)
            image.PlotRangeCircle(tmp_dict)
        print("++++++++++++++++++++++++++++++++++++")
        for instance in instance_list:
            print("Anker:{0} Tag:{1} dinstance:{2} m".format(instance.anc_id,instance.tag_id,instance.distance))
            if instance.distance != None: 
                distance_list.append([instance.anc_id,instance.tag_id, instance.distance])
        print("++++++++++++++++++++++++++++++++++++")
        image.PlotUWBTagPoint()
        #image.PlotAnkerPoint(distance_list=distance_list)
        #image.PlotAnkerEstimationPoint(distance_list=distance_list)
        current_anker_points = image.FindCoordEstimation(distance_list=distance_list)
        DD.GatherDistanceData(new_data=current_anker_points)
        #print("data num:",DD.data_queue)
            #data_labels = PredictBirch(data_cluster=DD.data_queue)
        data_labels, cluster_sizes = PredictKMeans(data_cluster=DD.data_queue,n_cluster=3)
        try:
            print(data_labels)
            image.PlotAnkerEstimationPoint(data_labels,DD.data_queue,cluster_sizes)
        except:
            pass
            
        image.ShowComment()
        image.ShowWindow()
        for s in ser:
            s.write("begin".encode('UTF-8'))
            s.reset_input_buffer()
        #time.sleep(0.5)

if __name__ == '__main__':
    #ANC_main()
    max_length = 60
    factor = 3
    MakeUWBInstance()
    DD = DistanceData(max_length=max_length)
    TAG_main()