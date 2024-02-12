"""
Module: sale_item.py
"""
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import SaleItemModel
from schemas import SaleItemSchema, SaleItemUpdateSchema

blp = Blueprint("SaleItems", "SaleItems", description="Operations on sale items")

@blp.route("/saleitem/<string:store_id>")
class Item(MethodView):
    """
    Item
    """
    @blp.response(200, SaleItemSchema)
    def get(self, store_id):
        """
        To get store through id
        """
        saleitem = SaleItemModel.query.get_or_404(store_id)
        return saleitem

    def delete(self, store_id):
        """
        To delete store through id
        """
        saleitem = SaleItemModel.query.get_or_404(store_id)
        db.session.delete(saleitem)
        db.session.commit()
        return {"message": "Sale Item deleted."}

@blp.route("/saleitem/<string:store_id>/<string:item_id>")
class ItemUpdate(MethodView):
    """
    Item
    """
    @blp.arguments(SaleItemUpdateSchema)
    @blp.response(200, SaleItemSchema)
    def put(self, item_data, store_id, item_id):
        """
        To update item through id
        """
        saleitem = SaleItemModel.query.filter(
            SaleItemModel.id == item_id, SaleItemModel.store_id == store_id).first()
        if not saleitem:
            return {"message": "Sale Item not found."}, 404
        saleitem.price = item_data.get("price", saleitem.price)
        saleitem.name = item_data.get("name", saleitem.name)
        saleitem.stock = item_data.get("stock", saleitem.stock)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Failed to update Sale Item.", "error": str(e)}, 500
        return saleitem

@blp.route("/saleitem")
class ItemList(MethodView):
    """
    ItemList
    """
    @blp.response(200, SaleItemSchema(many=True))
    def get(self):
        """
        To get saleitems
        """
        return SaleItemModel.query.all()

    @blp.arguments(SaleItemSchema)
    @blp.response(201, SaleItemSchema)
    def post(self, item_data):
        """
        To update salesitems data
        """
        item = SaleItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
            return item
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
