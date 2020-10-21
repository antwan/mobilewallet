from src.app import app
from src.resources import database
from .utils import create_user, create_wallet, create_transaction, get_balance
import pytest
import asyncio


async def _authenticate(client):
    user = await create_user()
    # Login
    url = app.url_path_for("login")
    response = client.post(url, json={
        "email": user['email'],
        "password": user['password']
    })
    assert response.status_code == 200
    return user


@pytest.mark.asyncio
async def test_successful_get_transactions(client):
    user1 = await _authenticate(client)
    user2 = await create_user(email='user2@test.com')
    wallet1 = await create_wallet(user1['id'])
    wallet2 = await create_wallet(user2['id'])
    wallet3 = await create_wallet(user2['id'])

    transaction1 = await create_transaction(wallet1['id'], wallet2['id'], 100, '1spending')
    transaction2 = await create_transaction(wallet1['id'], wallet2['id'], 1, '2spending')
    transaction3 = await create_transaction(wallet3['id'], wallet1['id'], 10, '3refund')
    transaction4 = await create_transaction(wallet2['id'], wallet2['id'], 300, '4saving')

    # Retrieve transactions
    url = app.url_path_for("transactions")
    response = client.get(url)
    assert response.status_code == 200
    expected = [{
        'sender': str(transaction1['account_from']),
        'recipient': str(transaction1['account_to']),
        'amount': transaction1['amount'],
        'label': transaction1['label'],
        'created_at': transaction1['created_at'].isoformat()
    }, {
        'sender': str(transaction2['account_from']),
        'recipient': str(transaction2['account_to']),
        'amount': transaction2['amount'],
        'label': transaction2['label'],
        'created_at': transaction2['created_at'].isoformat()
    }, {
        'sender': str(transaction3['account_from']),
        'recipient': str(transaction3['account_to']),
        'amount': transaction3['amount'],
        'label': transaction3['label'],
        'created_at': transaction3['created_at'].isoformat()
    }]
    assert response.json() == expected

@pytest.mark.asyncio
async def test_successful_create_transaction(client):
    user1 = await _authenticate(client)
    user2 = await create_user(email='user2@test.com')
    wallet1 = await create_wallet(user1['id'], balance=1000)
    wallet2 = await create_wallet(user2['id'], balance=1000)

    # Create transaction
    data = {
        "sender": str(wallet1['id']),
        'recipient': str(wallet2['id']),
        'label': 'payment',
        'amount': 400
    }
    url = app.url_path_for("transactions")
    response = client.post(url, json=data)
    assert response.status_code == 201
    assert response.json()['amount'] == data['amount']

    balance1 = await get_balance(wallet1['id'])
    assert balance1 == 600
    balance2 = await get_balance(wallet2['id'])
    assert balance2 == 1400

# Test error with input, unsufficient funds, etc
