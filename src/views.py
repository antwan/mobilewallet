from decimal import Decimal
from sqlalchemy import desc, text, select
import json
import functools
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, RedirectResponse

from .resources import database
from .serializers import UserCredentials, Wallet, Transaction
from .tables import users, wallets, ledger
from json.decoder import JSONDecodeError
from src.serializers import TransactionFilter


def requires_authentication(status_code=403):
    """ Views that require authentication. User is passed as argument """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request):
            if not 'user_id' in request.session:
                raise HTTPException(status_code=401)

            query = users.select().where(
                (users.c.id == request.session.get('user_id')) &
                (users.c.enabled == True)
            )
            current_user = await database.fetch_one(query)

            if current_user is None:
                raise HTTPException(status_code)
            return await func(request, current_user)
        return wrapper
    return decorator


async def _get_input(request, serializer_class, input_type='body'):
    """ Utility to parse and validate data from JSON input """
    try:
        data = (await request.json()) if input_type == 'body' else request.query_params
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail='Invalid input %s' % input_type)
    parsed_data, errors = serializer_class.validate_or_error(data)
    if errors:
        raise HTTPException(status_code=400, detail=json.dumps(dict(errors)))
    return parsed_data


async def login(request):
    """ User login view """

    credentials = await _get_input(request, UserCredentials)

    query = users.select().where(
        (users.c.email == credentials.email) &
        (users.c.password == credentials.password)
    )
    authenticated_user = await database.fetch_one(query)

    if not authenticated_user:
        raise HTTPException(status_code=403, detail='Invalid credentials')

    request.session["user_id"] = authenticated_user["id"]
    return JSONResponse()


async def logout(request):
    """ User logout view """

    request.session.clear()
    return JSONResponse()


@requires_authentication()
async def balances(request, current_user):
    """ Displays list of balances for all user accounts """

    query = wallets.select().where(
        (wallets.c.user_id == current_user['id']) &
        (wallets.c.enabled == True)
    )
    user_wallets = await database.fetch_all(query)

    data = [
        dict(Wallet(
            id=str(wallet['id']),
            name=wallet['name'],
            balance=wallet['balance'],
            last_transaction=wallet['updated_at']
        ))
        for wallet in user_wallets
    ]
    return JSONResponse(data)


@requires_authentication()
async def transactions(request, current_user):
    """ Creates a new transaction or displays list of transactions """

    # Transaction creation
    if request.method == "POST":
        new_transaction = await _get_input(request, Transaction)

        # Data validation
        sender_wallet = await database.fetch_one(
            wallets.select().where(
                (wallets.c.user_id == current_user['id']) &
                (wallets.c.id == new_transaction['sender']) &
                (wallets.c.enabled == True)
            )
        )
        if not sender_wallet:
            raise HTTPException(status_code=400, detail='Invalid sender account')

        recipient_wallet = await database.fetch_one(
            wallets.select().where(
                (wallets.c.id == new_transaction['recipient']) &
                (wallets.c.user_id == users.c.id) &
                (wallets.c.enabled == True) &
                (users.c.enabled == True)
            )
        )
        if not recipient_wallet:
            raise HTTPException(status_code=400, detail='Invalid recipient account')

        if sender_wallet['balance'] < new_transaction['amount']:
            raise HTTPException(status_code=400, detail='Insufficient balance in sender account')

        # Processes the transaction
        async with database.transaction():
            q = ledger.insert().values(
                label=new_transaction['label'],
                account_from=new_transaction['sender'],
                account_to=new_transaction['recipient'],
                amount=new_transaction['amount']
            )
            await database.execute(q)
            q = wallets.update().values(
                balance=wallets.c.balance - new_transaction['amount']
            ).where(wallets.c.id==new_transaction['sender'])
            await database.execute(q)
            q = wallets.update().values(
                balance=wallets.c.balance + new_transaction['amount']
            ).where(wallets.c.id==new_transaction['recipient'])
            await database.execute(q)

            data = dict(new_transaction)
            return JSONResponse(data, status_code=201)

    # Retrieves and display all transactions
    else:
        extra_filters = True
        filters = await _get_input(request, TransactionFilter, 'querystring')
        if filters and filters.get('wallet'):
            extra_filters = (wallets.c.id == filters.get('wallet'))

        sent_transactions = select(ledger.c).select_from(
            ledger.join(wallets, wallets.c.id == ledger.c.account_from)
        ).where(
            (wallets.c.user_id == current_user['id']) & extra_filters
        )
        received_transactions = select(ledger.c).select_from(
            ledger.join(wallets, wallets.c.id == ledger.c.account_to)
        ).where(
            (wallets.c.user_id == current_user['id']) & extra_filters
        )

        query = sent_transactions.union(received_transactions).order_by(desc(text('created_at')))
        user_transactions = await database.fetch_all(query)

        data = [
            dict(Transaction(
                sender=tr['account_from'],
                recipient=tr['account_to'],
                amount=tr['amount'],
                label=tr['label'],
                created_at=tr['created_at']
            ))
            for tr in user_transactions
        ]
        return JSONResponse(data)
