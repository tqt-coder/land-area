from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash, make_response
from flask_cors import CORS, cross_origin
import mysql.connector
import bcrypt
import jwt
import logging
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from dotenv import load_dotenv
import os
from image_downloading import run, check_dir_tree
from render_report import calculate_area, merging_row
from Satellite_Image_Collector import get_custom_image, get_npy, save_npy, read_size, check_json
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import torch
from mmengine.model.utils import revert_sync_batchnorm
from mmseg.apis import init_model, inference_model, show_result_pyplot

config_file = 'segformer_mit-b5_8xb2-160k_loveda-640x640.py'
checkpoint_file = 'segformer.pth'
# build the model from a config file and a checkpoint file
model = init_model(config_file, checkpoint_file, device='cpu')
if not torch.cuda.is_available():
    model = revert_sync_batchnorm(model)

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure Flask application from environment variables
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['MAIL_SERVER'] = os.getenv('FLASK_MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('FLASK_MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('FLASK_MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('FLASK_MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('FLASK_MAIL_PASSWORD')

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Enable CORS with specific origin and support credentials
CORS(app, resources={r"/*": {"origins": os.getenv('FLASK_CORS_ORIGINS')}}, supports_credentials=True)

def process_path(text: str):
    parts = text.split('/')
    if parts[-1] == "":
        parts = parts[:-1]
    return parts[-3], parts[-2], parts[-1]

def createConnectDB():
    connection = None
    try:
        connection = mysql.connector.connect(
            user=os.getenv('FLASK_DB_USER'),
            password=os.getenv('FLASK_DB_PASSWORD'),
            host=os.getenv('FLASK_DB_HOST'),
            port=int(os.getenv('FLASK_DB_PORT')),
            database=os.getenv('FLASK_DB_NAME')
        )
        logger.info('Connected to DB')
    except Exception as e:
        logger.error(f"The error '{e}' occurred")
    return connection

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        headers = dict(request.headers)  # Convert headers to a dictionary
        authorization = request.headers.get('Authorization')
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split()[1]
            logger.info(f"Token received: {token}")
            if not token:
                obj = {
                    'status': 403,
                    'isSuccess': False,
                    'type': 'error'
                }
                return jsonify(obj)
            
            try:
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                if 'email' not in payload:
                    raise jwt.InvalidTokenError('Invalid token')
            except jwt.ExpiredSignatureError:
                obj = {
                    'status': 403,
                    'isSuccess': False,
                    'type': 'error'
                }
                return jsonify(obj)
            except (jwt.InvalidTokenError, jwt.DecodeError):
                obj = {
                    'status': 403,
                    'isSuccess': False,
                    'type': 'error'
                }
                return jsonify(obj)
            
            return f(*args, **kwargs)
    return decorated_function

@app.route('/provinces', methods=['GET'])
@login_required
def getAllProvinces():
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT code, name, full_name FROM landarea.provinces;')
    rows = cursor.fetchall()
    result = [{'code': row[0], 'name': row[1], 'full_name': row[2]} for row in rows]
    cursor.close()
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/districts', methods=['GET'])
@login_required
def getDistrictsByProvinceCode():
    province_code = request.args.get('province_code')
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT code, name, full_name, province_code FROM landarea.districts WHERE province_code = %s', [province_code])
    rows = cursor.fetchall()
    result = [{'code': row[0], 'name': row[1], 'full_name': row[2], 'province_code': row[3]} for row in rows]
    cursor.close()
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/wards', methods=['GET'])
@login_required
def getWardsByDistrictCode():
    district_code = request.args.get('district_code')
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT code, name, full_name, district_code FROM landarea.wards WHERE district_code = %s', [district_code])
    rows = cursor.fetchall()
    result = [{'code': row[0], 'name': row[1], 'full_name': row[2], 'district_code': row[3]} for row in rows]
    cursor.close()
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/forgot', methods=['POST'])
def forgot():
    email = request.json.get('email')

    if email:
        token = s.dumps(email, salt='email-confirm')

        msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[email])

        # HTML formatted email content with a clickable link
        link = url_for('reset_with_token', token=token, _external=True)
        image_url = url_for('static', filename='img/logo_email.jpg',_external=True)

        msg.html = render_template('reset_email.html', name=email, link=link, img=image_url)

        mail.send(msg)

        logger.info('An email with a password reset link has been sent.')
        return jsonify({'status': 200, 'message': 'An email with a password reset link has been sent.','type': 'info'})
    else:
        return jsonify({'status': 400, 'message': 'Email address not provided.', 'type': 'error'})

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
            logger.info('Your password has been updated!')
            str_url = os.getenv('FLASK_CORS_ORIGINS') + '/login'
            return redirect(str_url)
        except Exception as e:
            logger.error(f'Error updating password: {e}')
            return jsonify({'status': 500, 'message': 'Internal Server Error','type': 'error'})
        finally:
            cursor.close()
            connection.close()

    return render_template('reset_with_token.html')

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
            now = datetime.now(timezone.utc)
            expiration_time = now + timedelta(days=1)
            payload = {
                'email': email,
                'exp': expiration_time
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            response = make_response(jsonify({'status': 200, 'type': 'success','token': token}))
            response.set_cookie('jwt', token, httponly=True, expires=expiration_time)
            logger.info('Login successful')
            return response
        else:
            logger.warning('Login failed. Invalid credentials')
            return jsonify({'status': 401, 'message': 'Invalid credentials', 'type': 'error'})
    except Exception as e:
        logger.error(f'Error while querying the database: {e}')
        return jsonify({'status': 500, 'message': 'Internal Server Error', 'type': 'error'})
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
