from src.app import app
from .utils import create_user, create_wallet
import pytest


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
async def test_successful_balance_for_one_wallet(client):
    user = await _authenticate(client)
    wallet = await create_wallet(user['id'])

    # Retrieve balances
    url = app.url_path_for("balances")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [{
        'id': str(wallet['id']),
        'name': wallet['name'],
        'balance': wallet['balance'],
        'last_transaction': wallet['updated_at'].isoformat()
    }]


# Test multiple balances, test unauthenticated, etc
