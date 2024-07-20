try:
    import datetime
    import psycopg2
    import bcrypt
    import jwt

    from flask import Flask, render_template, request, jsonify
    from psycopg2.extras import RealDictCursor
    from utils.db_conn import get_db_connection

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    @app.route('/')
    def home():
        return render_template('home.html')


    @app.route('/login')
    def login():
        return render_template('login.html')


    @app.route('/register')
    def register():
        return render_template('register.html')


    @app.route('/api/register', methods=['POST'])
    def api_register():
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({'message': str(e)}), 400
        finally:
            cur.close()
            conn.close()

        return jsonify({'message': 'User registered successfully'}), 201


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
        return render_template('index.html')


    if __name__ == '__main__':
        app.run(debug=True)


except Exception as e:
    from err_utils import get_err

    get_err(e)
