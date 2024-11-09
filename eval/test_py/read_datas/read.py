# -*- coding=utf-8 -*-
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import os
import cv2


def parse_csv(csv_path, CLASS_NAME):
    '''
    输入：
        csv_path: csv的文件路径
    输出：
        从csv文件中提取信息, 格式为[[img_name, [[x_min, y_min, x_max, y_max, confidence],...],
                                [img_name, [[x_min, y_min, x_max, y_max, confidence],...],...]
    '''
    results = list()
    coord_confidence_s = list()
    img_name_2 = str()
    with open(csv_path) as csvfile:
        mLines = csvfile.readlines()
        for mStr in mLines:
            row = mStr.split(",")
            img_name_1 = row[0]
            coord = row[1].split()
            x_min = int(coord[0])
            y_min = int(coord[1])
            x_max = x_min + int(coord[2])
            y_max = y_min + int(coord[3])
            confidence = float(row[2])  # 取结果文档中的分数2-head 4-smoke 6-phone
            name = str(row[3].split()[0])  # 取结果文档中的标签
            if img_name_1 != img_name_2 and mStr != mLines[0] and coord_confidence_s:
                result = [img_name_2, coord_confidence_s]
                results.append(result)
                coord_confidence_s = []
            img_name_2 = img_name_1
            coord_confidence = [x_min, y_min, x_max, y_max, confidence]
            # person，vehicle，rider，tricycles
            if CLASS_NAME == name:
                coord_confidence_s.append(coord_confidence)
            if mStr == mLines[-1] and coord_confidence_s:
                result = [img_name_2, coord_confidence_s]
                results.append(result)
    return results


def parse_xml(xml_path, CLASS_NAME):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, coords格式为[[x_min, y_min, x_max, y_max],...]
    '''
    tree = ET.parse(xml_path)
    root = tree.getroot()
    objs = root.findall('object')
    coords = list()
    for ix, obj in enumerate(objs):
        name = obj.find('name').text
        box = obj.find('bndbox')
        x_min = int(float(box.find('xmin').text))
        y_min = int(float(box.find('ymin').text))
        x_max = int(float(box.find('xmax').text))
        y_max = int(float(box.find('ymax').text))
        width = x_max - x_min
        height = y_max - y_min
        if CLASS_NAME == name:
            coords.append([x_min, y_min, x_max, y_max])
    return coords

def readCsv(filename, usecols, header=None):
    try:
        data_csv=pd.read_csv(filename,sep=None,engine='python',usecols=usecols,header=header, encoding='utf-8')
    except:
        data_csv=pd.read_csv(filename,sep=None,engine='python',usecols=usecols,header=header)
    return data_csv


def fileToArray(pd_data):
    data = pd_data.dropna(axis=0, how='any')
    data_new = data.values
    data_array = np.array(data_new)
    return data_array


def err_drawing(CLASS_NAME, ERR_S, img_paths, outimg_paths):
    res = readCsv('error_analysis_{}_{}.csv'.format(CLASS_NAME, ERR_S), (0, 1, 2, 3), header=0)
    res = fileToArray(res)
    for cells in res:
        # 0:图片名字 1:坐标:x y w h 2:分数 3:类名
        jpg_name = cells[0]
        threshold = cells[2]
        class_name = cells[3]
        # 获取坐标
        coordinate = cells[1]
        coordinate = (coordinate.split(' '))
        x, y, w, h = int(coordinate[0]), int(coordinate[1]), (int(coordinate[2]) - int(coordinate[0])), (
                    int(coordinate[3]) - int(coordinate[1]))
        # 获取对应图片路径，并按照坐标画框
        img_path = os.path.join(img_paths , jpg_name)
        save_jpg_name = outimg_paths + jpg_name
        if os.path.exists(save_jpg_name):
            img = cv2.imread(save_jpg_name)
        else:
            img = cv2.imread(img_path)
        # 颜色坐标:绿色0,255,0 红色0,0,255  蓝色255,0,0 黄色255,255,0
        colour = (0,0,255)
        cv2.rectangle(img, (x, y), ((x + w), (y + h)), colour, 2)
        # biaoqian = class_name + str(threshold)
        cv2.putText(img, str(threshold), (x, (y + int(h / 2))), cv2.FONT_HERSHEY_COMPLEX, 1, colour, 2)
        # 存放路径
        save_jpg_name = os.path.join(outimg_paths ,jpg_name)
        cv2.imwrite(save_jpg_name, img)