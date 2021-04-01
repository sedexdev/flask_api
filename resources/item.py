from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import Item


class StoredItem(Resource):
    """
    Describes an item resource that has a name and price.
    Allowed methods are:
        - GET, POST, PUT, DELETE
    """

    _parser = reqparse.RequestParser()
    _parser.add_argument(
        'price',
        type=float,
        required=True,
        help='The price of this item is required'
    )
    _parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='The store ID of this item is required'
    )

    @jwt_required()
    def get(self, name):
        try:
            item = Item.get_by_name(name)
            if item:
                return item.as_json()
            return {'error': f"'{name}' not found"}, 404
        except Exception:
            return {"error": "Internal server error"}, 500

    def post(self, name):
        data = self._parser.parse_args()
        if Item.get_by_name(name):
            return {'error': 'Item already exists'}, 404
        try:
            item = Item(name, **data)
            item.save()
            return {'msg': 'Item added successfully'}, 201
        except Exception:
            return {"error": "Internal server error"}, 500

    def put(self, name):
        data = self._parser.parse_args()
        try:
            item = Item.get_by_name(name)
            if not item:
                item = Item(name, **data)
                item.save()
                return {'msg': 'Item added successfully'}, 201
            else:
                item.price = data['price']
                item.save()
                return {'msg': 'Item updated successfully'}
        except Exception:
            return {"error": "Internal server error"}, 500

    def delete(self, name):
        item = Item.get_by_name(name)
        if not item:
            return {'error': 'Item not found'}, 404
        try:
            item.delete()
            return {'msg': 'Item deleted successfully'}
        except Exception:
            return {"error": "Internal server error"}, 500


class ItemList(Resource):
    """
    Describes a list of item resources that have a name and price.
    Allowed methods are:
        - GET
    """

    @jwt_required()
    def get(self):
        try:
            return [item.as_json() for item in Item.query.all()]
        except Exception:
            return {"error": "Internal server error"}, 500
