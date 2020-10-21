from src.app import app
from .utils import create_user
import pytest


@pytest.mark.asyncio
async def test_logout(client):
    url = app.url_path_for("logout")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_successful_login(client):
    user = await create_user()

    url = app.url_path_for("login")
    response = client.post(url, json={
        "email": user['email'],
        "password": user['password']
    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_unsuccessful_login(client):
    user = await create_user()

    url = app.url_path_for("login")
    response = client.post(url, json={
        "email": user['email'],
        "password": "wrong_password"
    })
    assert response.status_code == 403
    assert response.text == "Invalid credentials"


@pytest.mark.asyncio
async def test_login_no_data(client):
    user = await create_user()

    url = app.url_path_for("login")
    response = client.post(url)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_flow(client):
    user = await create_user()

    url = app.url_path_for("login")
    response = client.post(url, json={
        "email": user['email'],
        "password": user['password']
    })

    assert response.status_code == 200

    url = app.url_path_for("logout")
    response = client.get(url)
    assert response.status_code == 200
