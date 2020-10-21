import typesystem
from datetime import datetime
from decimal import Decimal

class UserCredentials(typesystem.Schema):
    email = typesystem.String()
    password = typesystem.String()

class Wallet(typesystem.Schema):
    id = typesystem.String(title='Wallet ID')
    name = typesystem.String(title='Wallet name')
    balance = typesystem.Integer(title='Balance in pennies')
    last_transaction = typesystem.DateTime(title='Last transaction')

class TransactionFilter(typesystem.Schema):
    wallet = typesystem.String(title='Wallet to filter on', format='uuid', allow_blank=True)

class Transaction(typesystem.Schema):
    sender = typesystem.String(title='Sender account', format='uuid')
    recipient = typesystem.String(title='Recipient account', format='uuid')
    amount = typesystem.Integer(title='Transaction amount', exclusive_minimum=0)
    label = typesystem.String(title='Label', max_length=100, default='')
    created_at = typesystem.DateTime(title='Date created', default=datetime.utcnow())

    @classmethod
    def validate(cls, *args, **kwargs):
        ret = super().validate(*args, **kwargs)
        if ret['sender'] == ret['recipient']:
            raise typesystem.ValidationError(
                text='Sender and recipient account should be different',
                code='identical_accounts'
            )
        return ret
