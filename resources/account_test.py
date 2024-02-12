# import pytest
# from app import create_app
# from db import db
# from models import AccountModel

# @pytest.fixture
# def client():
#     app = create_app()
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#             yield client
#             db.session.remove()
#             db.drop_all()

# def test_get_account(client):
#     # Create a test account
#     account = AccountModel(name="Test Account")
#     db.session.add(account)
#     db.session.commit()

#     # Send a GET request to the /account endpoint
#     response = client.get('/account/Test Account')
#     assert response.status_code == 200

#     # Verify the response data matches the expected account data
#     assert response.json['name'] == "Test Account"

# def test_delete_account(client):
#     # Create a test account
#     account = AccountModel(name="Test Account")
#     db.session.add(account)
#     db.session.commit()

#     # Send a DELETE request to the /account endpoint
#     response = client.delete('/account/Test Account')
#     assert response.status_code == 200

#     # Verify the account is deleted
#     assert AccountModel.query.filter_by(name="Test Account").first() is None

# def test_create_account(client):
#     # Send a POST request to create a new account
#     response = client.post('/account', json={"name": "New Test Account"})
#     assert response.status_code == 201

#     # Verify the response data matches the expected account data
#     assert response.json['name'] == "New Test Account"
