from flask import render_template, request, redirect, url_for, jsonify, send_file, session, flash
from wtforms.fields.html5 import DateTimeLocalField
from flask_bootstrap import Bootstrap

from saleapp import app, dao, utils, login
from flask_login import login_user, login_required
from flask_login import logout_user
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, ValidationError, IntegerField
from wtforms.validators import Required, EqualTo, Regexp
import json
from saleapp.models import *
import hashlib


bootstrap = Bootstrap(app)
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login-admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)
    return redirect("admin")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)



if __name__ == "__main__":
    from saleapp.admin import *

    app.run(debug=True, port=5000)
