from flask import (Flask,
                   render_template
                   )


app = Flask(__name__)
app.secret_key = 'bezhan200910203040'


def get_err(err):
    with app.app_context():
        return render_template("error_p.html", reall_error=err)
