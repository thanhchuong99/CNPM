from saleapp import app
from saleapp.models import Flight, Airport, User
from functools import wraps
import json
import os
import hashlib


def load_users():
    with open(os.path.join(app.root_path, "data/users.json"), encoding="utf-8") as f:
        return json.load(f)


def check_login(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    users = User.query.filter(User.username == username.strip(), User.password == password.strip()).first()
    if users:
            return users
    return None




