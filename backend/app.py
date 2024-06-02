from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash, make_response
from flask_cors import CORS, cross_origin
import mysql.connector
import bcrypt
import jwt
import datetime
from datetime import timezone
from functools import wraps
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tranquoctuan3112001@gmail.com'
app.config['MAIL_PASSWORD'] = 'lssx inbu qnuh crmi'  # App-specific password

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Enable CORS with specific origin and support credentials
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

def createConnectDB():
    connection = None
    try:
        connection = mysql.connector.connect(
            user='root', password='1234', host='127.0.0.1', port=3333, database='landarea'
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
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
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
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
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
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/get_area', methods=['GET'])
@login_required
def get_area():
    ward_code = request.args.get('ward_code')
    connection = createConnectDB()
    cursor = connection.cursor()
    cursor.execute('SELECT land_area FROM landarea.wards WHERE code = %s', [ward_code])
    rows = cursor.fetchall()
    cursor.close()
    response = jsonify(rows)
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.json['email']
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
            return redirect('http://localhost:3000/login')
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
            now = datetime.datetime.now(timezone.utc)
            expiration_time = now + datetime.timedelta(days=1)
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

@app.route('/', methods=['GET'])
def homepage():
    return render_template('form.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
