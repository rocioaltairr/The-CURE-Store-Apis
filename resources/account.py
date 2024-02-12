"""
Module: account.py
Description: Defines views for account-related operations.
"""
import os
import sqlite3

from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import AccountModel
from schemas import AccountSchema, UpdateAccountSchema
from .crypt.encrypt import encrypted_password, decrypt_password

blp = Blueprint("Accounts", "accounts", description="Operations on accounts")

DB_FILENAME = os.path.realpath("./instance/data.db")

@blp.route("/accountname/<string:account_name>")
class AccountName(MethodView):
    """
    View for retrieving and deleting an account by ID.
    """
    @blp.response(200, AccountSchema)
    def get(self, account_name):
        """
        Retrieve an account by NAME.
        """
        with sqlite3.connect(DB_FILENAME) as con:
            cur = con.cursor()
            # cur.execute(f"SELECT * FROM accounts WHERE name='{account_name}'")
            sql = "SELECT * FROM accounts WHERE name=?"
            params = (account_name,)
            cur.execute(sql, params)
            result = cur.fetchone()
            if result:
                column_names = ["id", "actor", "name", "user_name", "code", "login_attempts"]
                return jsonify(dict(zip(column_names, result)))
            return {"message": "Account not found"}, 404

@blp.route("/login")
class UserLogin(MethodView):
    """
    Account Login
    """
    @blp.arguments(AccountSchema)
    def post(self, user_data):
        """
        Account Login
        """
        user = AccountModel.query.filter(
            AccountModel.user_name == user_data['user_name']).first()
        if user.name == user_data['user_name'] and decrypt_password(user.code) == user_data['code']:
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        abort(401, message="Invalid credentials.")

@blp.route("/account/<int:account_id>")
class Account(MethodView):
    """
    View for retrieving and deleting an account by ID.
    """
    @blp.response(200, AccountSchema)
    def get(self, account_id):
        """
        Get an account by id.
        """
        account = AccountModel.query.get_or_404(account_id)
        if account:
            return account
        abort(404, message="Can't find data.")

    def delete(self, account_id):
        """
        Delete an account by ID.
        """
        account = AccountModel.query.get_or_404(account_id)
        db.session.delete(account)
        db.session.commit()
        return {"message": "account deleted"}, 200

    @blp.arguments(UpdateAccountSchema)
    @blp.response(200, AccountSchema)
    def put(self, account_data, account_id):
        """
        Update an account by ID.
        """
        account = AccountModel.query.get_or_404(account_id)

        for key, value in account_data.items():
            setattr(account, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500,
                  message="An error occurred updating the account.")
        return account

@blp.route("/account")
class AccountList(MethodView):
    """
    View for retrieving all accounts and creating a new account.
    """
    @blp.response(200, AccountSchema(many=True))
    def get(self):
        """
        Retrieve all accounts.
        """
        accounts = AccountModel.query.all()
        for account in accounts:
            account.code = decrypt_password(account.code)
        return accounts

    @blp.arguments(AccountSchema)
    @blp.response(201, AccountSchema)
    def post(self, account_data):
        """
        Create a new account.
        """
        account = AccountModel(**account_data)
        account.code = encrypted_password(account_data["code"])
        try:
            db.session.add(account)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A account with that name already exists.",
            )
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred creating the account."
            )
        return account
