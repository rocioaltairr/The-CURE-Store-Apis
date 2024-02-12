"""
Module: schemas.py
"""
from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    """
    PlainItemSchema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    stock = fields.Int(required=True)

class PlainAccountSchema(Schema):
    """
    PlainAccountSchema
    """
    id = fields.Int(dump_only=True)
    actor = fields.Str()
    name = fields.Str()
    user_name = fields.Str()
    code = fields.Str()
    login_attempts = fields.Int()

class UpdateAccountSchema(Schema):
    """
    UpdateAccountSchema
    """
    actor = fields.Str()
    name = fields.Str()
    user_name = fields.Str()
    code = fields.Str()
    login_attempts = fields.Int()

class ItemSchema(PlainItemSchema):
    """
    Item Schema
    """
    account_id = fields.Int(required=True, load_only=True)
    account = fields.Nested(PlainAccountSchema(), dump_only=True)

class ItemUpdateSchema(Schema):
    """
    ItemUpdateSchema
    """
    name = fields.Str()
    price = fields.Float()
    stock = fields.Int()

class AccountSchema(PlainAccountSchema):
    """
    AccountSchema
    """
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class LoginSchema(Schema):
    """
    AccountSchema
    """
    message = fields.Str()


class PlainSaleItemSchema(Schema):
    """
    PlainSaleItemSchema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    stock = fields.Int(required=True)

class PlainStoreSchema(Schema):
    """
    PlainStoreSchema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()

class SaleItemSchema(PlainSaleItemSchema):
    """
    SaleItemSchema
    """
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)

class SaleItemUpdateSchema(Schema):
    """
    SaleItemUpdateSchema
    """
    name = fields.Str()
    price = fields.Float()
    stock = fields.Int()

class StoreSchema(PlainStoreSchema):
    """
    StoreSchema
    """
    saleitems = fields.List(fields.Nested(PlainSaleItemSchema()), dump_only=True)
