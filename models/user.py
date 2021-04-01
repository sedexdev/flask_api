from werkzeug.security import generate_password_hash
from db.db import db


class User(db.Model):
    """
    Creates new user objects so users can ineract with the API
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password_hash = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, _id):
        return User.query.filter_by(id=_id).first()

    def verify_username(self, username):
        user = self.get_by_username(username)
        if user:
            return False
        return True

    def verify_password(self, password):
        length = len(password) >= 12
        upper = any(x.isupper() for x in password)
        lower = any(x.islower() for x in password)
        digit = any(x.isdigit() for x in password)
        return length and upper and lower and digit

    def password_error(self):
        return {'error': {
            'msg': 'Password does not meet criteria',
            'length': 'Must be at least 12 characters',
            'upper': 'Must contain uppercase characters',
            'lower': 'Must contain lowercase characters',
            'digit': 'Must contain numbers',
        }}, 400

    def as_json(self):
        return {'username': self.username, 'password_hash': self.password_hash}

    def save(self):
        db.session.add(self)
        db.session.commit()
