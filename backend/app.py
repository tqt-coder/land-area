from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash, make_response
from flask_cors import CORS, cross_origin
import mysql.connector
import bcrypt
import jwt
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
from werkzeug.datastructures import ImmutableMultiDict
import cv2
# Load environment variables from .env file
load_dotenv()

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
        print('================>> connected DB')
    except Exception as e:
        print(f"The error '{e}' occurred")
    return connection

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        headers = dict(request.headers)  # Convert headers to a dictionary
        authorization = request.headers.get('Authorization')
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split()[1]
            print(token)
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

# @app.route('/get_area', methods=['GET'])
# @login_required
# def get_area():
#     ward_code = request.args.get('ward_code')
#     connection = createConnectDB()
#     cursor = connection.cursor()
#     cursor.execute('SELECT land_area FROM landarea.wards WHERE code = %s', [ward_code])
#     rows = cursor.fetchall()
#     cursor.close()
#     response = jsonify(rows)
#     response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
#     response.headers.add('Access-Control-Allow-Credentials', 'true')
#     return response

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

        print('An email with a password reset link has been sent.', 'info')
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
            print('Your password has been updated!', 'success')
            str_url = os.getenv('FLASK_CORS_ORIGINS') + '/login'
            return redirect(str_url)
        except Exception as e:
            print(f'Error updating password: {e}', 'error')
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
    response = make_response(jsonify({'status': 200, 'message': 'You have been logged out.', 'type': 'info'}))
    response.set_cookie('tooken', '', expires=0)  # Remove the cookie
    return response


def merge_large_img(data: json = {}):
    # Check tree
    if data == {}:
        root = "annotations"
        flag = True
    else:
        anno_keys = ("province", "district", "ward")
        if all(check_json(key, data) for key in anno_keys):
            root,flag = check_dir_tree(dir_tree= ["data","annotations", data['province'], data["district"],data["ward"]])
        else:
            flag = True
            root = data['annotations'].replace("\\","\\\\").replace("/","\\\\")
            print(root)
    try:
        if flag:
            size_path = root.replace("annotations","mask")
            W, H = read_size(root=size_path)

            index = []
            for i in range(H,1, -1):
                index.append([x for x in range(W*i-W, W*i)])
            index.append(np.arange(W-1,-1,-1))
            # index1=[i for i in range(56,64)]
            # index2=[i for i in range(48,56)]
            # index3=[i for i in range(40,48)]
            # index4=[i for i in range(32,40)]
            # index5=[i for i in range(24,32)]
            # index6=[i for i in range(16,24)]
            # index7=[i for i in range(8,16)]
            # index8 = np.arange(7, -1, -1)
            # index = [index1, index2, index3, index4, index5, index6, index7, index8]
            big_images=merging_row(index[0], folder_path=root)
            for i in index[1:]:
                try:
                    image=merging_row(i, folder_path=root)
                    big_images = np.concatenate((big_images, image))
                except:
                    image=merging_row(i, folder_path=root, flag=False)
                    big_images = np.concatenate((big_images, image))
            return big_images
        else:
            return False
    except:
        return False

def get_area_total(big_images,mask):
    print(calculate_area(big_images, mask))
    unique_values, counts = np.unique(mask, return_counts=True)
    print(unique_values, counts)
    total_sum = sum(calculate_area(big_images, mask).values())
    return total_sum

def sub(image: np.ndarray,x1:int, y1:int, x2:int, y2:int)-> np.ndarray:
    submatrix = [row[x1:x2] for row in image[y2:y1]]
    resized_submatrix = np.resize(submatrix,(y1 - y2, x2 - x1))
    return resized_submatrix

## Download Images
@app.route("/download_img", methods=['POST'])
def download_img():
    province = request.json['province']
    district = request.json['district']
    ward = request.json['ward']
    data = {
        'province': province,
        'district': district,
        'ward': ward,
        'lst_img': [1]
    }
    print('data',data)
    if province is not None or district is not None or ward is not None:
        str_url = 'FinalProject/backend/data/images' + province + '/' + district + '/' + ward

        geo_series, G = get_custom_image(data=data)
        if "lst_img" not in data or data["lst_img"]==[]:
            save_npy(geo_series,G, data)
        for idx, bound in enumerate(geo_series):
            try:
                run(idx=data['lst_img'][idx],bound=bound.bounds, data=data)
            except:
                run(idx=idx,bound=bound.bounds,data=data)
        response = jsonify({ 'message': str_url,'status': 200})
        print({ 'message': str_url,'status': 200})
        response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    else:
        response = jsonify({ 'message': '','status': 400})
        print({ 'message': '','status': 400})
        response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

@app.route('/get_area', methods=['POST','GET'])
@login_required
def get_area():
    annotations = request.json['urlAnnotations']
    mask = request.json['urlMask']
    data = {
        'annotations': annotations,
        'mask': mask
    }
    print('data',data)
    if annotations is not None or mask is not None:
        # data = {key: value for key, value in params.items()}
        mask = get_npy(data=data)
        big_images = merge_large_img(data=data)
        # Change link img
        if isinstance(mask, np.ndarray) and isinstance(big_images, np.ndarray):
            new_mask = np.rot90(mask, k=1)
            if new_mask.shape == big_images.shape:
                resized_mask = new_mask
            else:
                new_mask_shape = new_mask.shape
                # Resize new_mask to match big_images if dimensions differ
                resized_big_images = cv2.resize(big_images, (new_mask_shape[1], new_mask_shape[0]))

            resized_big_images[new_mask == False] = False 
            area = calculate_area(image=resized_big_images, mask=new_mask)
            serializable_area = {int(k): v for k, v in area.items()}

                # Serialize the dictionary to JSON
                # json_data = json.dumps(serializable_area)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'land_img_{timestamp}.jpg'
            plt.imshow(resized_big_images)
            plt.axis('off')
 
                # Construct the file path for saving the image in the static/img directory
            file_path = os.path.join('static', 'img', filename)

                # Save the displayed image
            plt.savefig(file_path, bbox_inches='tight', pad_inches=0, transparent=True)

            # Close the plot to release resources
            plt.close()

                
            image_url = url_for('static', filename='img/' + filename,_external=True)

                # response = jsonify({"img":big_images.tolist(), 'area': serializable_area,'status': 200, 'image_url': image_url})
            response = jsonify({ 'area': serializable_area,'status': 200, 'image_url': image_url})
            print({ 'area': serializable_area,'status': 200, 'image_url': image_url})
            response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
        else:
            response = jsonify({ 'area': null,'status': 500})
            response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
    else:
        response = jsonify({ 'area': null,'status': 500})
        response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

@app.route('/get_inference', methods=['POST','GET'])
@login_required
def get_inference():
    p_province  = request.args.get('province')
    p_district  = request.args.get('district')
    p_ward      = request.args.get('ward')
    data        = {
        'province': p_province,
        'district': p_district,
        'ward'    : p_ward,
        'lst_img' : [0]
    }
    print('data',data)
    if data and ( p_province is not None or p_district is not None or ward is not None):
        is_download_complete = download_img(data)
        data2 = data
        if is_download_complete:
            # data = {key: value for key, value in params.items()}
            mask = get_npy(data=data2)
            big_images = merge_large_img(data=data2)
            # Change link img
            if isinstance(mask, np.ndarray) and isinstance(big_images, np.ndarray):
                new_mask = np.rot90(mask, k=1)
                if new_mask.shape == big_images.shape:
                    resized_mask = new_mask
                else:
                    new_mask_shape = new_mask.shape
                    # Resize new_mask to match big_images if dimensions differ
                    resized_big_images = cv2.resize(big_images, (new_mask_shape[1], new_mask_shape[0]))  
                resized_big_images[new_mask == False] = False
                area = calculate_area(image=resized_big_images, mask=new_mask)
                serializable_area = {int(k): v for k, v in area.items()}

                # Serialize the dictionary to JSON
                # json_data = json.dumps(serializable_area)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'land_img_{timestamp}.jpg'
                plt.imshow(resized_big_images)
                plt.axis('off')

                # Construct the file path for saving the image in the static/img directory
                file_path = os.path.join('static', 'img', filename)

                # Save the displayed image
                plt.savefig(file_path, bbox_inches='tight', pad_inches=0, transparent=True)

                # Close the plot to release resources
                plt.close()

                
                image_url = url_for('static', filename='img/' + filename,_external=True)

                # response = jsonify({"img":big_images.tolist(), 'area': serializable_area,'status': 200, 'image_url': image_url})
                response = jsonify({ 'area': serializable_area,'status': 200, 'image_url': image_url})
                print({ 'area': serializable_area,'status': 200, 'image_url': image_url})
                response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
                response.headers.add('Access-Control-Allow-Credentials', 'true')
                return response
            else:
                return "Not having annotations or images!!!"
        else:
            response = jsonify({ 'area': null,'status': 500})
            response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
    else:
        response = jsonify({ 'area': null,'status': 500})
        response.headers.add('Access-Control-Allow-Origin', os.getenv('FLASK_CORS_ORIGINS'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response


# import torch
# from mmengine.model.utils import revert_sync_batchnorm
# from mmseg.apis import init_model, inference_model, show_result_pyplot
# config_file = './configs/segformer/segformer_mit-b5_8xb2-160k_loveda-640x640.py'
# checkpoint_file = '/mmsegmentation/data/segformer.pth'
# # build the model from a config file and a checkpoint file
# model = init_model(config_file, checkpoint_file, device='cuda')


@app.route('/predict_data', methods=['POST'])
def predict_data():
    params = request.args.to_dict()
    if params:
        data = {key: value for key, value in params.items()}
        root, flag = check_dir_tree(["data","images",data["province"],data["district"],data["ward"]])
        root = root.replace("\\","\\\\")

        for filename in os.listdir(root):
            image_path = os.path.join(root, filename)

            save_dir,_ = check_dir_tree(["data","annotations",data["province"], data["district"],data["ward"]])
            save_dir = root.replace("\\","\\\\")
            result = inference_model(model, image_path)
            vis_iamge = show_result_pyplot(model, image_path, result, save_dir =save_dir,
                                        opacity=1.0, show=False,  draw_gt=True, with_labels=False)
            # vis_iamge = show_result_pyplot(model, image_path, result, save_dir ='data/results/',
            #                             opacity=1.0, show=False,  draw_gt=True, with_labels=False)

        return "abc"
    return "done have model"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
