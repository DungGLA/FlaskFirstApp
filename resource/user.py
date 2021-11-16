import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import ( create_access_token,
                                 create_refresh_token,
                                 get_jwt_identity,
                                 jwt_required,
                                 get_jwt
                                )
from model.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                         )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                         )

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exist.'}, 400

        user = UserModel(**data)
        user.save_to_db()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data['username'], data['password']))
        #
        # connection.commit()
        # connection.close()
        return {"message": "User creates successfully."}, 201

class UserLogin(Resource):
    @classmethod
    def post(cls):
        # 1: get data from parser
        data = _user_parser.parse_args()
        # 2: find user in db
        user = UserModel.find_by_username(data['username'])
        # 3: check password
        # 4: create access token
        # 5: create refresh token
        # 6: return them

        # This is what the `authenticate()` function used to do
        if user and safe_str_cmp(user.password, data['password']):
            # identity = is what the `identity()` function used to do
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401

class TokenRefresh(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti'] # jti is "JWT ID", a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {'message': 'Successful logged out.'}
