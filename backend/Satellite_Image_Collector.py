import os
import json
import time
import math
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from shapely.geometry import Point, Polygon

from image_downloading import image_size, check_dir_tree
from shapely.geometry.base import BaseGeometry

from geo_func import split_polygon, read_geopandas_data

def check_json(key: str,data: json):
    if key in data and data[key]!= "":
        return True
    return False

def get_npy(data: json) -> np.ndarray:
    mask_keys = ("province_mask", "district_mask", "ward_mask")
    if all(check_json(key, data) for key in mask_keys):
        root,flag = check_dir_tree(dir_tree= ["data","mask",data["province_mask"],data["district_mask"],data["ward_mask"]])
    else:    
        root,flag = check_dir_tree(dir_tree= ["data","mask",data["province"],data["district"],data["ward"]])
    if flag:
        mask = np.load(os.path.join(root,"mask.npy"))
        return mask
    return flag

def is_point_inside_polygon(path,point):
    return path.contains_point(point)

def check_num_img(geo_series):
    num = len(geo_series)
    if math.sqrt(num).is_integer():
        return math.sqrt(num)
    else:
        W = 1     
        for i in range(2,int(num/2)+1):
            H = num/i
            if H.is_integer() and abs(H-i) <= abs(num/W-W):
                W = i
        return W

def save_size(W: int, H: int, root: str):
    with open(f"{root}\\\\size.txt", "w", encoding="utf-8") as file:
        file.write(str(W) + "\n")
        file.write(str(H) + "\n")

def read_size(root: str):
    with open(f"{root}\\\\size.txt", "r", encoding="utf-8") as file:
        # Read the width and height values from the file
        W = int(file.readline().strip())
        H = int(file.readline().strip())
    return W, H

def save_npy(geo_series, G, data):

    start = time.time()
    if 'W_num' in data and data['W_num']!='':
        W_num = int(data['W_num'])
    else:
        W_num = check_num_img(geo_series)
    print(W_num)

    tf_lon, _, _, tf_lat = geo_series[geo_series.index[-1]-W_num+1].bounds
    _, br_lat, br_lon, _ = geo_series[0].bounds

    W, H = image_size(tf_lat, tf_lon, br_lat, br_lon, zoom=19)
    print(W,H)
    dx = (br_lon-tf_lon)/W
    dy = (tf_lat-br_lat)/H

    valuesx = np.arange(0, W)
    oney = np.ones((1,H), dtype=int)
    image_dx = valuesx.reshape((W,1))*oney

    valuesy = np.arange(H,0, -1)
    onex = np.ones((W,1), dtype=int)
    image_dy = valuesy.reshape((1,H))*onex

    lon = np.add(image_dx*dx, tf_lon)
    lat = np.add(image_dy*dy, br_lat)
    area = {}
    boundary = G
    path = Path(list(boundary.exterior.coords)) 
    mask = np.full(lat.shape, False, dtype=bool)
    print(lon.shape, lat.shape)
    for i in range(W):
        if(i%500 == 0):
            print(time.time()-start)
        for j in range(H):
            mask[i,j] = is_point_inside_polygon(path,(lon[i][j], lat[i][j]))
    root, _ = check_dir_tree(["data","mask",data["province"],data["district"],data["ward"]])
    np.save(os.path.join(root,"mask"), mask)  
    save_size(W=round(W_num), H= round(len(geo_series)/W_num), root=root)
    

def get_geometry(province: str, district: str, ward: str) -> BaseGeometry:
    geo= read_geopandas_data(province=province, district=district, ward=ward)
    G = np.random.choice(geo.geometry.values)
    return G

def get_custom_image(data: json):
    province = data['province']
    district = data['district']
    ward = data['ward']
    if 'lst_img' in data:
        lst_img = data['lst_img']
    else:
        lst_img =[]
    G = get_geometry(province=province, district=district, ward=ward)
    squares   = split_polygon(G,shape='square',thresh=0,side_length=0.005)
    if len(lst_img) > 0:
        lst_squares = [squares[i] for i in lst_img]
    else:
        lst_squares = squares
    geo_series = gpd.GeoSeries(lst_squares)

    # # Create a figure and an axes object.
    # fig, ax = plt.subplots()
    # # Display the GeoSeries object on the axes object.
    # geo_series.plot(color = 'red', ax=ax)
    # geo.exterior.plot(color='blue', ax= ax)
    # plt.show()
    return geo_series, G