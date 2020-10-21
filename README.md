# 💸 MobileWallet bank API

This is a simple demo bank API written in Python. It provides basic features such as accounts and transfers.

## Installation and running

This project can be deployed using docker. Make sure it is installed on your maching, and type the following commands:
```
    make init
    make run
```

Additional commands are available and documented in the `Makefile`, e.g to connect the shell or the database. You can also initialize the DB without provisonning data using `make db-start db-upgrade`

## Using the API

Once running, you can browse the documentation by visting `http://localhost:8000/docs`. This will describe all the endpoints available.
You can consume data on this API using any HTTP client. Some rich clients such as Postman can prefill data structure using the [API schema file](http://localhost:8000/docs/schema.yml).

First connect as an user using the `/login` endpoint, and check your wallets balances and transactions.

The following users and wallets are created with provisionning scripts:
|Email          |Password  |
|---------------|----------|
|alice@gmail.com|`password`|
|bob@gmail.com  |`password`|
|carol@gmail.com|`password`|
|dan@gmail.com  |`password`|

## Design notes

This project is based on the fairly recent Python ASGI environment, that aim to provide fast and async-capable web services. This choice of libraries can be a reasonnable candidate for a production API with high perforance and availability requirements, as this allow to process many requests simultanously with coroutines.

The following tools and libraries have been used:
- Starlette, an async REST web framework
- uvicorn, as an ASGI application server
- typesystem for data sanitization and serialization
- APIStar to provide doc and schema
- PostgreSQL as relational DB
- SqlAlchemy and databases to access DB asynchronously
- Alembic for data structure migrations
- Docker for ease of deployment
- pytest as a unit-test framework

### Authentication
The authentication mechanism is a dummy one that use plain text passwords and sessions. Some sophisticated libraries could be used here to provide more advanced authentication mechanisms (OAuth, etc).

### ORM and model
- An async-compatible ORM could have been used instead (e.g Gino) to manipulate, but for the sake of minimalism and performance this was not the case here.
- The ledger model is simplist too, as the balances make authority over the ledger. Another approach could have been to use wallet balances as a cache of the sum of the transactions, but this would require to populate ledger with anonymous transactions from the outside world so funds are available.

### Infrastructure & monitoring
Monitoring can be dealt with a variety of strategies. Logging and metrics analysis can be done without hurting performance thanks to the async approach, e.g. using queue handlers to aynschronously record metrics and/or log entries. This can then be attached to any relevant log/metric aggregator, such as AWS Cloudwatch or Prometheus.

## Possible extensions
- Pagination, Ordering, and advanced filtering
- More comprehensive transaction history (account holder names, relative amounts)
- Feature extensions, such as recipient lists, transaction requests, etc.
- More sophisticated web-based API (e.g using content negociation to server JSON or HTML)
