"""
Module: store.py
"""
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema
from flask_jwt_extended import jwt_required

blp = Blueprint("Stores", "stores", description="Operations on stores")

@blp.route("/store/<string:store_name>")
class Store(MethodView):
    """
    Store
    """
    @blp.response(200, StoreSchema)
    def get(self, store_name):
        """
        To get store's data
        """
        store = StoreModel.query.get_or_404(store_name)
        return store

    def delete(self, store_name):
        """
        To delete store
        """
        store = StoreModel.query.get_or_404(store_name)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200


@blp.route("/store")
class StoreList(MethodView):
    """
    StoreList
    """
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """
        To get store data
        """
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        """
        To add store
        """
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store