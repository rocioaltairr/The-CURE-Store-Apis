"""
Model: store.py
"""
from db import db

class StoreModel(db.Model):
    """
    Model: StoreModel
    """
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    saleitems = db.relationship(
        "SaleItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"
    )
