from typing import Dict, Tuple
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.user import User


class APIUser(Resource):
    """
    Describes an endpoint used for registering users in
    the sqlite database andfetching users. Methods allowed:
        - GET, POST
    """

    _parser = reqparse.RequestParser()
    _parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field is required')
    _parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field is required')

    @jwt_required()
    def get(self) -> Dict:
        return [user.as_json() for user in User.query.all()]

    def post(self) -> Tuple:
        data = self._parser.parse_args()
        username = data['username']
        password = data['password']
        try:
            user = User(username, password)
            if not user.verify_username(username):
                return {'error': 'Username is taken'}, 409
            if not user.verify_password(password):
                return user.password_error()
            user.save()
            return {'msg': 'User created successfully'}, 201
        except Exception:
            return {"error": "Internal server error"}, 500
