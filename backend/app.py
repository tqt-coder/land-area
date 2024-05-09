
# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# from flask_mysqldb import MySQL
import mysql.connector
import re
 
 
app = Flask(__name__)
connection = mysql.connector.connect(
    user='root', password='1234', host='mysql-app-container', database='landarea'
 )
print('================>> connected DB')

 

@app.route("/provinces")
def getAllProvinces():
    cursor = connection.cursor()
    cursor.execute('SELECT code,name,full_name FROM landarea.provinces;')
    allData = cursor.fetchall()
    print(list(allData))
    return jsonify(list(allData ))

@app.route("/districts")
# /districts?province_code=x
def getDistrictsByProvinceCode():
    province_code = request.args.get('province_code')
    print('================>> province_code ' + province_code)
    cursor = cursor = connection.cursor()
    cursor.execute('SELECT code,name,full_name,province_code FROM landarea.districts where province_code=%s',[province_code])
    allData = cursor.fetchall()
    return jsonify(list(allData ))
 
@app.route("/wards")
# /wards?district_code=x
def getWardsByDistrictCode():
    district_code = request.args.get('district_code')
    print('================>> districtCode ' + district_code)
    cursor = cursor = connection.cursor()
    cursor.execute('SELECT code,name,full_name,district_code FROM landarea.wards where district_code=%s',[district_code])
    allData = cursor.fetchall()
    return jsonify(list(allData ))

 
if __name__ == "__main__":
    app.run