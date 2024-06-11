import os
import json
import time
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from shapely.geometry import Point, Polygon

from image_downloading import image_size, check_dir_tree
from shapely.geometry.base import BaseGeometry

from geo_func import split_polygon, read_geopandas_data

def get_npy(data: json) -> np.ndarray:
    # hard code
    # root,flag = check_dir_tree(dir_tree= ["data","mask",data["province"],data["district"],data["ward"]])
    root,flag = check_dir_tree(dir_tree= ["data","mask","Lâm Đồng","Đà Lạt","10"])
    if flag:
        mask = np.load(os.path.join(root,"mask.npy"))
        return mask
    return flag

def is_point_inside_polygon(path,point):
    return path.contains_point(point)

def save_npy(geo_series, data):

    start = time.time()
    tf_lon, _, _, tf_lat = geo_series[56].bounds
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
    boundary = Polygon(geo_series[geo_series.index[0]])
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
    return geo_series