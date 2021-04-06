from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from decouple import Config, RepositoryEnv
import os

from security import authenticate, identify
from resources.user import APIUser
from resources.item import StoredItem, ItemList
from resources.store import ItemStore, StoreList
from db.db import db

HOME = os.path.expanduser(path='~')
DOTENV_FILE = f'{HOME}/Documents/Flask_REST_APIs/3_sqlalchemy_api/vars.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = env_config.get('JWT_SECRET_KEY')
api = Api(app)
jwt = JWT(app, authenticate, identify)


@app.before_first_request
def create_tables() -> None:
    # runs CREATE TABLE IF NOT EXISTS ...
    db.create_all()


api.add_resource(APIUser, '/users')
api.add_resource(StoredItem, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(ItemStore, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5000)
