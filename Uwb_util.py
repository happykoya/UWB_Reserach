#!/usr/bin/env python3
#-*- coding: utf-8 -*
#Date:2024/04/18 ~ 
#Author:Koya Okuse
#UWB研究用のUtil関数
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
import pandas as pd

#Ancの時はtid=Noneになる
ANC_Data = {'Id':None,
            'UWB Module Role':None}

TAG_Data = {'tid':None,
            'range':None,
            'rssi':None}

#USBPortの接続をシリアル通信で行う(最後に接続されたものだけ認識する)
#Portの確定
def Get_FristCom():
    port_list = serial.tools.list_ports.comports()
    if len(port_list) <= 0:
        print("No COM")
        return ""
    else:
        #print("Connect First COM")
        for com in port_list:
            print("com:",com)
            return list(com)[0]

def Get_ALLCom():
    serial_list = []
    port_list = serial.tools.list_ports.comports()
    if len(port_list) <= 0:
        print("No COM")
        return ""
    else:
        print("ALL COM")
        for com in port_list:
            #print("com:",list(com)[0])
            ser = serial.Serial(list(com)[0], 115200)
            serial_list.append(ser)
        
        #pp(serial_list)
        return serial_list
        
#UWBのデータを辞書型にして保存する
#tid = タグID
#mask = ??
#seq = データ番号(何番目のデータか)
#range = 推定距離
#rssi = 通信強度
#rangeとrssiのデータ添字は対応している
def Get_UWBdataANC(input_string):
    data_dict = {}
    # キーと値を抽出して辞書に保存する
    pattern = re.compile(r'([^=,]+):([^=,]+)')
    matches = pattern.findall(input_string)
    for match in matches:
        key = match[0].strip()
        value = match[1].strip()
        # 値が "(...)" の形式であれば、括弧内のデータのみを抽出
        if key == "range" or key == "rssi":
            value = Pattern_RangeRssi(key=key, input_string=input_string)
        data_dict[key] = value
    return data_dict

#rangeとrssiの正規表現用関数
def Pattern_RangeRssi(key, input_string):
    pattern = re.compile( key+r':\((.*?)\)')
    match = pattern.search(input_string)
    if match:
        return match.group(1)
    else:
        return None

def Set_UWBdataANC(input_dict):
    for key, value in input_dict.items():
        if key in ANC_Data:
            ANC_Data.update({key: value})
        elif key in TAG_Data:
            TAG_Data.update({key: value})
     
#選択したUWBアンカーからデータを取得
def ReadData(ser):
    try:
        #for _serial in serial_list:
        line = ser.readline().decode('UTF-8').replace('\n', '')
        result = Get_UWBdataANC(line)
        Set_UWBdataANC(result)
        
        if result != {}:
            print("result:",line)
        elif result == {}:
            print("[LOG]:",line)
        print(type(line))
    except Exception as e:
        print(e.args)
        pass

#TagをPCに接続して使用する場合
def ReadTagData(ser):
    line = str(ser.readline().hex())
    raw_result = Split_RawData(line)
    result = Get_UWBdataTAG(raw_data=raw_result)
    #print("result:",result)
    return result

def Split_RawData(hex_data):
    # 16進数文字列を2バイトずつに分割する
    try:
        split_data = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
    except:
        print("error")
        #split_data = 
    return split_data

def Get_UWBdataTAG(raw_data):
    result_dict = {"Anker_id":None,
                   "Tag_id": None,
                   "Range_data":None}
    
    #print(raw_data)
    anc_data = bytes.fromhex(raw_data[0])
    decoded_string = anc_data.decode('utf-8')
    
    if decoded_string == "A":
        result_dict["Anker_id"] = 0
    elif decoded_string == "B":
        result_dict["Anker_id"] = 1
    elif decoded_string == "C":
        result_dict["Anker_id"] = 2
    try:  
        result_dict["Tag_id"] = int(int(raw_data[1]))
    except:
        result_dict["Tag_id"] = "?"
    range_data = Get_Rangedata(raw_data[3:-1])
    result_dict["Range_data"] = range_data
    
    return result_dict
    
def Get_Rangedata(raw_range):
    data = "".join(raw_range)
    # ヘキサデシマル文字列をバイト列に変換
    binary_data = bytes.fromhex(data)
    try:
    # 'f'は32ビットの浮動小数点数を表すフォーマット文字
        decimal_number = struct.unpack('<f', binary_data)[0]
    except:
        decimal_number = 0.0
    
    value = "{:.4f}".format(decimal_number)
    return value


#-------------------------------------------------------#
from collections import deque
from sklearn.cluster import Birch, KMeans
class DistanceData:
    def __init__(self,max_length):
        self.data_queue = deque(maxlen=max_length)
    
    def GatherDistanceData(self,new_data):
        for data in new_data:
            self.data_queue.append(data)
        
def PredictKMeans(data_cluster,n_cluster):
    kmeans = KMeans(n_clusters=n_cluster, random_state=0, n_init="auto").fit(data_cluster)
    labels = kmeans.labels_
    cluster_sizes = pd.Series(labels).value_counts().sort_index()
    return labels, cluster_sizes
    

def PredictBirch(data_cluster,branching_factor):
    brc = Birch(n_clusters=None, branching_factor=branching_factor)
    brc.fit(data_cluster)
    labels = brc.predict(data_cluster)
    return labels