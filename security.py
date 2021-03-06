from typing import Dict
from werkzeug.security import check_password_hash
from models.user import User


def authenticate(username: str, password: str) -> Dict:
    user = User.get_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        return user


def identify(payload: Dict) -> Dict:
    user_id = payload['identity']
    return User.get_by_id(user_id)
