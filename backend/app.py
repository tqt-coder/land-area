
# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# from flask_mysqldb import MySQL
import mysql.connector
import re
from flask_cors import CORS


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
            'district_code' : row[3]
        }
        result.append(obj)
    
    # Process the data as needed
    print(result)
    return jsonify(result)
 
if __name__ == "__main__":
    app.run