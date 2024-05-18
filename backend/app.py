
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

app = Flask(__name__)
# Enable CORS with specific options
CORS(app)

connection = mysql.connector.connect(
    user='root', password='1234', host='mysql-app-container', database='landarea'
    # user='root', password='1234', host='127.0.0.1',port=3333, database='landarea'
 )
print('================>> connected DB')

 

@app.route("/provinces")
def getAllProvinces():
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
    return jsonify(result)

@app.route("/districts")
# /districts?province_code=x
def getDistrictsByProvinceCode():
    province_code = request.args.get('province_code')
    print('================>> province_code ' + province_code)
    cursor = cursor = connection.cursor()
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
    return jsonify(result)
 
@app.route("/wards")
# /wards?district_code=x
def getWardsByDistrictCode():
    district_code = request.args.get('district_code')
    print('================>> districtCode ' + district_code)
    cursor = cursor = connection.cursor()
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
    return jsonify(result)

@app.route("/img")
# /wards?ward_code=x
def getImageByCode():
    ward_code = request.args.get('ward_code')
    print('================>> ward_code: ' + ward_code)
    cursor = cursor = connection.cursor()
    cursor.execute('SELECT code, land_image FROM landarea.wards where code=%s',[ward_code])
    image_data = cursor.fetchone()
    cursor.close()
    if image_data:
        response = send_file(
                io.BytesIO(image_data[1]),
                mimetype='image/png'
            )
        return response
    else:
        return 'Image not found'

# Images 
@app.route("/upload") 
def serve_image(): 
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    ward_code = request.form.get('ward_code') 
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        cursor = connection.cursor()
        cursor.execute("""Update landarea.wards set land_image = (%s) where code = (%s)""", (file.read(),ward_code))
        connection.commit()
        cursor.close()
        return 'File uploaded and saved to database successfully'

@app.route('/get_area', methods=['GET'])
def get_area():
    params = request.args.to_dict()
    if params:
        data = {key: int(value) for key, value in params.items()}
        img = sub(image=big_images, x1=data['x1'], y1=data['y1'],x2=data['x2'],y2=data['y2'])
        new_models = sub(image=new_mask, x1=data['x1'], y1=data['y1'],x2=data['x2'],y2=data['y2'])  
        
        area = calculate_area(image=img, mask=new_models)
        print(area)
        return jsonify({"img":img.tolist(), 'area': str(area)})
        # return jsonify(area)
    else:
        return "Successfull Start!"

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

mask = np.load('./mask.npy')
new_mask = np.rot90(mask, k=1)
big_images = merge_large_img()
big_images[new_mask == False] = 0

if __name__ == "__main__":
    app.run(debug=True)