from typing import Dict
from db.db import db


class Store(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('Item', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_by_name(cls, name: str) -> Dict:
        return Store.query.filter_by(name=name).first()

    def error(self, msg: str, code: int) -> Dict:
        return {'error': msg}, code

    def as_json(self) -> Dict:
        return {
            'name': self.name,
            'items': [item.as_json() for item in self.items.all()]}

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
