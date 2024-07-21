import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, url_for
import psycopg2
import bcrypt
import jwt
import datetime
from psycopg2.extras import RealDictCursor
from utils.db_conn import get_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Путь для сохранения загруженных файлов
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # 16 MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Проверка расширения файла
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/users')
def get_users():
    return render_template('users.html')


# Маршрут для загрузки изображений
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo_url = url_for('static', filename='images/' + filename)
        return jsonify({'photo_url': photo_url}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400


@app.route('/api/users', methods=['GET'])
def api_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    # Добавляем путь к изображению для каждого пользователя
    for user in users:
        if user['photo_filename']:
            user['photo_url'] = url_for('static', filename='images/' + user['photo_filename'])
        else:
            user['photo_url'] = url_for('static', filename='images/default.png')  # Изображение по умолчанию
    return jsonify(users), 200


@app.route('/api/register', methods=['POST'])
def api_register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    file = request.files['photo']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo_filename = filename

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password_hash, photo_filename) VALUES (%s, %s, %s, %s)",
                    (username, email, password_hash, photo_filename))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'User registered successfully!'}), 201

    return jsonify({'error': 'Invalid file format'}), 400


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        return jsonify({'access_token': token})

    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/profile')
def profile():
    return render_template('index.html'), 200




if __name__ == '__main__':
    from models import create_tables

    create_tables()
    app.run(debug=True)
