import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE username = ?"
        # result = cursor.execute(query, (username,))
        # row = result.fetchone()
        #
        # if row:
        #     # user = User(row[0], row[1], row[2])
        #     user = UserModel(*row)
        # else:
        #     user = None
        #
        # connection.close()
        # return user
        # user @classmethod and cls instead of self
        # that means is that now we are using current class, which is user, as opposed to hard coding the class name at line 19

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE id = ?"
        # result = cursor.execute(query, (id,))
        # row = result.fetchone()
        #
        # if row:
        #     user = UserModel(*row)
        # else:
        #     user = None
        #
        # connection.close()
        # return user
