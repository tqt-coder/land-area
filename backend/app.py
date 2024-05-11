
# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
# from flask_mysqldb import MySQL
import mysql.connector
import re
from flask_cors import CORS
import os
import io  # Import the 'io' module

app = Flask(__name__)
# Enable CORS with specific options
CORS(app)

connection = mysql.connector.connect(
    # user='root', password='1234', host='mysql-app-container', database='landarea'
    user='root', password='1234', host='127.0.0.1',port=3333, database='landarea'
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


if __name__ == "__main__":
    app.run(debug=True)