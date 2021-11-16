import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from db import db

from Security import authenticate, identity
from resource.user import UserRegister, UserLogin, TokenRefresh, UserLogout
from resource.item import Item, ItemList
from resource.store import Store, StoreList

app = Flask(__name__)

# app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLACHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# To know when an object had changed, but not been saved to the db, the extension flask SQLAchemy was tracking every
# change that we made to the SQLAchemy session and that took some resources.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Jose' # app.config['JWT_SECRET_KEY']
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)

# jwt = JWT(app, authenticate, identity) # /auth
jwt = JWTManager(app) # not create /auth

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification faild.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': 'The token has been revoke.',
        'error': 'token_revoked'
    }), 401

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

db.init_app(app)
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5000)