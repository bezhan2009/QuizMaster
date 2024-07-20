try:
    from flask import Flask, jsonify, url_for, request, render_template, redirect, session
    import psycopg2
    from models import create_tables

    app = Flask(__name__)
    app.secret_key = 'bezhan200910203040'

    def initialize_db():
        try:
            create_tables()
        except psycopg2.Error as e:
            print(f"Error creating tables: {e}")


    initialize_db()


    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')


    if __name__ == '__main__':
        app.run(debug=True)

except Exception as e:
    from err_utils import get_err

    get_err(e)
