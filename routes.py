from flask import *
from flask_login import *
from app import app
from models import login_required

@app.route("/")
@login_required
def homepage():
    return render_template("homepage.html")

@app.route("/2")
def homepage2():
    return render_template("homepage3.html")

@app.route("/preview")
def preview():
    return render_template("preview.html")

@app.route("/preview2")
def preview2():
    return render_template("preview2.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile/<int:user_id>')
@login_required
def profile_page(user_id):
    return render_template('profile.html', user_id=user_id)