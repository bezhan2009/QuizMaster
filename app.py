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
    cur.execute("SELECT * FROM quiz_app.users")
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
        cur.execute("INSERT INTO quiz_app.users (username, email, password_hash, photo_filename) VALUES (%s, %s, %s, %s)",
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
    cur.execute("SELECT * FROM quiz_app.users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        return jsonify({'access_token': token, 'user_id': user['id']})

    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/profile/<int:id_user>/', methods=['GET'])
def profile(id_user):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Получение данных пользователя
    cur.execute("""
        SELECT 
            u.*, 
            ud.gender, ud.surname, ud.name, ud.favorite_subject, 
            ud.cover_filename, ud.achievements, ud.bio, 
            c.title as contact_title 
        FROM quiz_app.users u
        LEFT JOIN quiz_app.user_data ud ON u.id = ud.user_id
        LEFT JOIN quiz_app.contacts c ON ud.contact_id = c.id
        WHERE u.id = %s
    """, (id_user,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        # Заменяем пустые значения по умолчанию
        user['photo_url'] = url_for('static', filename='images/' + (user['photo_filename'] or 'default.png'))
        user['cover_url'] = url_for('static', filename='images/' + (user['cover_filename'] or 'default_cover.png'))
        user['name'] = user['name'] or user['username']
        user['surname'] = user['surname'] or ''
        user['achievements'] = user['achievements'] or None
        user['bio'] = user['bio'] or user['username']
        user['contact_title'] = user['contact_title'] or 'нет контактов'

        return render_template('profile.html', user=user)
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/profile/edit/<int:id_user>/', methods=['GET', 'POST'])
def edit_profile(id_user):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == 'POST':
        # Получение данных из формы
        username = request.form.get('username')
        email = request.form.get('email')
        gender = request.form.get('gender')
        surname = request.form.get('surname')
        name = request.form.get('name')
        favorite_subject = request.form.get('favorite_subject')
        bio = request.form.get('bio')
        contact_id = request.form.get('contact_id')
        achievements = request.form.get('achievements')

        # Обновление данных пользователя
        cur.execute("""
            UPDATE quiz_app.users
            SET username = %s, email = %s
            WHERE id = %s
        """, (username, email, id_user))

        cur.execute("""
            UPDATE quiz_app.user_data
            SET gender = %s, surname = %s, name = %s, favorite_subject = %s,
                bio = %s, contact_id = %s, achievements = %s
            WHERE user_id = %s
        """, (gender, surname, name, favorite_subject, bio, contact_id, achievements, id_user))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('profile', id_user=id_user))

    # Получение текущих данных пользователя для заполнения формы
    cur.execute("""
        SELECT 
            u.*, 
            ud.gender, ud.surname, ud.name, ud.favorite_subject, 
            ud.cover_filename, ud.achievements, ud.bio, 
            c.title as contact_title 
        FROM quiz_app.users u
        LEFT JOIN quiz_app.user_data ud ON u.id = ud.user_id
        LEFT JOIN quiz_app.contacts c ON ud.contact_id = c.id
        WHERE u.id = %s
    """, (id_user,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return render_template('edit_profile.html', user=user)
    else:
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    from models import create_tables

    create_tables()
    app.run(debug=True)
