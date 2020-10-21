from src.resources import database
from src.tables import users, wallets, ledger

async def create_user(email="test@test.com", name="test"):
    query = users.insert()
    user = {
        "email": email,
        "password": "password",
        "name": name
    }
    user["id"] = await database.execute(query, user)
    return user

async def create_wallet(user_id, balance=1000, name="test", enabled=True):
    query = wallets.insert()
    wallet = {
        "name": name,
        "user_id": user_id,
        "balance": balance,
        "enabled": enabled
    }
    wallet['id'] = await database.execute(query, wallet)
    wallet['updated_at'] = (await database.fetch_one(
        wallets.select().where(wallets.c.id == wallet['id'])
    ))['updated_at']
    return wallet

async def create_transaction(sender, recipient, amount, label="test"):
    query = ledger.insert().returning(ledger.c.created_at)
    tr = {
        "label": label,
        "account_from": sender,
        "account_to": recipient,
        "amount": amount
    }
    tr["created_at"] = await database.execute(query, tr)
    return tr

async def get_balance(account_id):
    query = wallets.select().where(wallets.c.id == account_id)
    res = await database.fetch_one(query)
    return res['balance']
