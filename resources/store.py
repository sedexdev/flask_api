from typing import Dict, Tuple, Union
from flask_restful import Resource
from flask_jwt import jwt_required

from models.store import Store


class ItemStore(Resource):
    """
    Describes a store used for grouping Items.
    Methods allowed:
        - GET, POST, DELETE
    """

    @jwt_required()
    def get(self, name: str) -> Union[Dict, Tuple]:
        try:
            store = Store.get_by_name(name)
            if not store:
                return store.error('Store not found', 404)
            return store.as_json()
        except Exception:
            return {'error': 'Internal server error'}, 500

    def post(self, name: str) -> Tuple:
        try:
            store = Store.get_by_name(name)
            if store:
                return store.error('Store name already exists', 409)
            store = Store(name)
            store.save()
            return {'msg': 'Store created successfully'}, 201
        except Exception:
            return {'error': 'Internal server error'}, 500

    def delete(self, name: str) -> Union[Dict, Tuple]:
        try:
            store = Store.get_by_name(name)
            if not store:
                return store.error('Store not found', 404)
            store.delete()
            return {'msg': 'Store deleted successfully'}
        except Exception:
            return {'error': 'Internal server error'}, 500


class StoreList(Resource):
    """
    Describes a resource for fetching all Store objects.
    Methods allowed:
        - GET
    """

    @jwt_required()
    def get(self) -> Union[Dict, Tuple]:
        try:
            return {'stores': [store.as_json() for store in Store.query.all()]}
        except Exception:
            return {'error': 'Internal server error'}, 500
