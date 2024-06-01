from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, flash, make_response
# from flask_mysqldb import MySQL
import mysql.connector
import re
from flask_cors import CORS
import io  # Import the 'io' module

import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from calc_area import *
import time
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os
import bcrypt
from functools import wraps
import jwt
import datetime
from datetime import timezone

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tranquoctuan3112001@gmail.com'
app.config['MAIL_PASSWORD'] = 'lssx inbu qnuh crmi'  # App-specific password

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
# Enable CORS with specific options
CORS(app)

def createConnectDB():
    connection = None
    try:
        connection = mysql.connector.connect(
        # user='root', password='1234', host='mysql-app-container', database='landarea'
        user='root', password='1234', host='127.0.0.1', port=3333, database='landarea'
        )
        print('================>> connected DB')
    except Exception as e:
        print(f"The error '{e}' occurred")
    return connection

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            flash('Please log in to access this page.', 'warning')
            obj = {
                'status': 403,
                'isSuccess': False,
                'type': 'error'
            }
            return jsonify(obj)
        
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # You can perform additional checks on the payload if needed
            if 'email' not in payload:
                raise jwt.InvalidTokenError('Invalid token')
        except jwt.ExpiredSignatureError:
            flash('Token has expired.', 'warning')
            obj = {
                'status': 403,
                'isSuccess': False,
                'type': 'error'
            }
            return jsonify(obj)
        except (jwt.InvalidTokenError, jwt.DecodeError):
            flash('Invalid token.', 'warning')
            obj = {
                'status': 403,
                'isSuccess': False,
                'type': 'error'
            }
            return jsonify(obj)
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        token = s.dumps(email, salt='email-confirm')

        msg = Message('Password Reset Request', sender='your-email@gmail.com', recipients=[email])
        link = url_for('reset_with_token', token=token, _external=True)
        msg.body = f'Your password reset link is {link}'
        mail.send(msg)

        print('An email with a password reset link has been sent.', 'info')
        return jsonify({'status': 200, 'message': 'An email with a password reset link has been sent.','type': 'info'})

    return render_template('forgot.html')

@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    connection = createConnectDB()
    cursor = connection.cursor()

    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'

    if request.method == 'POST':
        new_password = request.form['password']

        try:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('UPDATE users SET password = %s WHERE email = %s', (hashed_password, email))
            connection.commit()
            print('Your password has been updated!', 'success')
            return jsonify({'status': 401, 'message': 'Your password has been updated!','type': 'success'})
        except Exception as e:
            print(f'Error updating password: {e}', 'error')
            return jsonify({'status': 500, 'message': 'Internal Server Error','type': 'error'})
        finally:
            cursor.close()
            connection.close()

    return render_template('reset_with_token.html')

@app.route("/provinces")
@login_required
def getAllProvinces():
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT code,name,full_name FROM landarea.provinces;')
    rows = cursor.fetchall()
    result = []
    for row in rows:
        obj = {
            'code': row[0],
            'name': row[1],
            'full_name': row[2]
        }
        result.append(obj)
    
    # Process the data as needed
    print(result)
    cursor.close()
    return jsonify(result)

@app.route("/districts")
# /districts?province_code=x
@login_required
def getDistrictsByProvinceCode():
    province_code = request.args.get('province_code')
    print('================>> province_code ' + province_code)
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT code,name,full_name,province_code FROM landarea.districts where province_code=%s', [province_code])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        obj = {
            'code': row[0],
            'name': row[1],
            'full_name': row[2],
            'province_code': row[3]
        }
        result.append(obj)
    
    # Process the data as needed
    print(result)
    cursor.close()
    return jsonify(result)

@app.route("/wards")
# /wards?district_code=x
@login_required
def getWardsByDistrictCode():
    district_code = request.args.get('district_code')
    print('================>> districtCode ' + district_code)
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT code,name,full_name,district_code FROM landarea.wards where district_code=%s', [district_code])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        obj = {
            'code': row[0],
            'name': row[1],
            'full_name': row[2],
            'district_code': row[3],
        }
        result.append(obj)
    
    # Process the data as needed
    print(result)
    cursor.close()
    return jsonify(result)

@app.route('/get_area', methods=['GET'])
@login_required
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
    cursor.execute('SELECT land_area FROM landarea.wards where code=%s', [ward_code])
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

@app.route('/', methods=['GET'])
def homepage():
    return render_template('form.html')

def merge_large_img():
    folder_path = "./animation"
    index1 = [i for i in range(56, 64)]
    index2 = [i for i in range(48, 56)]
    index3 = [i for i in range(40, 48)]
    index4 = [i for i in range(32, 40)]
    index5 = [i for i in range(24, 32)]
    index6 = [i for i in range(16, 24)]
    index7 = [i for i in range(8, 16)] 
    index8 = np.arange(7, -1, -1)
    index = [index1, index2, index3, index4, index5, index6, index7, index8]
    big_images = merging_row(index[0], folder_path=folder_path)
    for i in index[1:]:
        image = merging_row(i, folder_path=folder_path)
        big_images = np.concatenate((big_images, image))
    return big_images

def get_area_total():
    print(calculate_area(big_images, mask))
    unique_values, counts = np.unique(mask, return_counts=True)
    print(unique_values, counts)
    total_sum = sum(calculate_area(big_images, mask).values())
    return total_sum

def sub(image: np.ndarray, x1: int, y1: int, x2: int, y2: int) -> np.ndarray:
    submatrix = [row[x1:x2] for row in image[y2:y1]]
    resized_submatrix = np.resize(submatrix, (y1 - y2, x2 - x1))
    return resized_submatrix

# ========================== calc area
# mask = np.load('./mask.npy')
# new_mask = np.rot90(mask, k=1)
# big_images = merge_large_img()
# big_images[new_mask == False] = 0
# ==================
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    
    connection = createConnectDB()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Generate a token
            now = datetime.datetime.now(timezone.utc)
            expiration_time = now + datetime.timedelta(days=1)  # Token expiration time
            payload = {
                'email': email,
                'exp': expiration_time
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            # Create a response with the token as a cookie
            response = make_response(jsonify({'status': 200, 'type': 'success'}))
            response.set_cookie('token', token, expires=expiration_time, httponly=True)
            return response
        else:
            print('Invalid email or password', 'error')
            return jsonify({'status': 401, 'message': 'Invalid email or password','type': 'error'})
    except Exception as e:
        print(f'Error logging in: {e}', 'error')
        return jsonify({'status': 500, 'message': 'Internal Server Error','type': 'error'})
    finally:
        cursor.close()
        connection.close()

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    connection = createConnectDB()
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Email already exists', 'error')
            return jsonify({'status': 401, 'message': 'Email already exists','type': 'error'})
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, hashed_password))
            connection.commit()
            session['email'] = email
            return jsonify({'status': 200, 'message': 'Create account successfully','type': 'success'})
    except Exception as e:
        print(f'Error registering user: {e}', 'error')
        return {'status': 500, 'message': 'Internal Server Error','type': 'error'}
    finally:
        cursor.close()
        connection.close()

@app.route('/logout')
def logout():
    session.pop('email', None)
    print('You have been logged out.', 'info')
    return jsonify({'status': 200, 'message': 'You have been logged out.','type': 'info'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
