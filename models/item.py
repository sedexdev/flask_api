from typing import Dict
from db.db import db


class Item(db.Model):
    """
    Creates new item objects so create new items for use
    throughout the API
    """

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('Store')

    def __init__(self, name: str, price: float, store_id: int) -> None:
        self.name = name
        self.price = price
        self.store_id = store_id

    @classmethod
    def get_by_name(cls, name: str) -> Dict:
        return cls.query.filter_by(name=name).first()

    def as_json(self) -> Dict:
        return {'name': self.name, 'price': self.price}

    def get_all(self) -> Dict:
        return {'items': [self.as_json() for item in Item.query.all()]}

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
