from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from main import app
from werkzeug.security import safe_str_cmp
from models import User

def authenticate(username, password):
    user = User.query.filter(User.username == username).one_or_none()
    if user.password == password:
        return user

def identity(payload):
    print(str(payload))

app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity