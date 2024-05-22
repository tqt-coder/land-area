
# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
# from flask_mysqldb import MySQL
import mysql.connector
import re
from flask_cors import CORS
import os
import io  # Import the 'io' module

import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from calc_area import *
import time
app = Flask(__name__)
# Enable CORS with specific options
CORS(app)

def createConnectDB():
    connection = None
    try:
        connection = mysql.connector.connect(
        # user='root', password='1234', host='mysql-app-container', database='landarea'
        user='root', password='1234', host='127.0.0.1',port=3333, database='landarea'
        )
        print('================>> connected DB')
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

 

@app.route("/provinces")
def getAllProvinces():
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT code,name,full_name FROM landarea.provinces;')
    rows = cursor.fetchall()
    result = []
    for row in rows:
        obj = {
            'code'      : row[0],
            'name'      : row[1],
            'full_name' : row[2]
        }
        result.append(obj)
    
    # Process the data as needed
    print(result)
    cursor.close()
    return jsonify(result)

@app.route("/districts")
# /districts?province_code=x
def getDistrictsByProvinceCode():
    province_code = request.args.get('province_code')
    print('================>> province_code ' + province_code)
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT code,name,full_name,province_code FROM landarea.districts where province_code=%s',[province_code])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        obj = {
            'code'          : row[0],
            'name'          : row[1],
            'full_name'     : row[2],
            'province_code' : row[3]
        }
        result.append(obj)
    
    # Process the data as needed
    print(result)
    cursor.close()
    return jsonify(result)
 
@app.route("/wards")
# /wards?district_code=x
def getWardsByDistrictCode():
    district_code = request.args.get('district_code')
    print('================>> districtCode ' + district_code)
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT code,name,full_name,district_code FROM landarea.wards where district_code=%s',[district_code])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        obj = {
            'code'          : row[0],
            'name'          : row[1],
            'full_name'     : row[2],
            'district_code' : row[3],
        }
        result.append(obj)
    
    # Process the data as needed
    print(result)
    cursor.close()
    return jsonify(result)


@app.route('/get_area', methods=['GET'])
def get_area():
    # params = request.args.to_dict()
    ward_code = request.args.get('ward_code')
    params = {
        'x1': 0,
        'y1': 12000,
        'x2': 2000,
        'y2': 10000
    }
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT land_area FROM landarea.wards where code=%s',[ward_code])
    rows = cursor.fetchall()
    cursor.close()
    # ========================== calc area
    # if params:    
    #     area = calculate_area(image=big_images, mask=new_mask)
    #     area_fixed = {str(k): v for k, v in area.items()}
    #     print(area_fixed)
    #     return jsonify(area_fixed)
    # ==========================
    return rows
    


def merge_large_img():
    folder_path = "./animation"
    index1=[i for i in range(56,64)]
    index2=[i for i in range(48,56)]
    index3=[i for i in range(40,48)]
    index4=[i for i in range(32,40)]
    index5=[i for i in range(24,32)]
    index6=[i for i in range(16,24)]
    index7=[i for i in range(8,16)] 
    index8 = np.arange(7, -1, -1)
    index = [index1, index2, index3, index4, index5, index6, index7, index8]
    big_images=merging_row(index[0], folder_path=folder_path)
    for i in index[1:]:
        image=merging_row(i, folder_path=folder_path)
        big_images = np.concatenate((big_images, image))
    return big_images


def get_area_total():
    print(calculate_area(big_images, mask))
    unique_values, counts = np.unique(mask, return_counts=True)
    print(unique_values, counts)
    total_sum = sum(calculate_area(big_images, mask).values())
    return total_sum


def sub(image: np.ndarray,x1:int, y1:int, x2:int, y2:int)-> np.ndarray:
    submatrix = [row[x1:x2] for row in image[y2:y1]]
    resized_submatrix = np.resize(submatrix,(y1 - y2, x2 - x1))
    return resized_submatrix


 # ========================== calc area
# mask = np.load('./mask.npy')
# new_mask = np.rot90(mask, k=1)
# big_images = merge_large_img()
# big_images[new_mask == False] = 0
# ==================
if __name__ == "__main__":
    app.run(debug=True)