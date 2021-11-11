import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from Security import authenticate, identity
from resource.user import UserRegister
from resource.item import Item, ItemList
from resource.store import Store, StoreList

app = Flask(__name__)

# app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLACHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# To know when an object had changed, but not been saved to the db, the extension flask SQLAchemy was tracking every
# change that we made to the SQLAchemy session and that took some resources.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Jose'
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")

db.init_app(app)
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5000)