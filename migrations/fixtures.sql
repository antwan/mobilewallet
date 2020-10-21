INSERT INTO "users" ("id", "name", "email", "password") VALUES
    (1, 'Alice', 'alice@gmail.com', 'password'),
    (2, 'Bob', 'bob@gmail.com', 'password'),
    (3, 'Carol', 'carol@gmail.com', 'password'),
    (4, 'Dan', 'dan@gmail.com', 'password')
;

INSERT INTO "wallets"("user_id", "balance", "name") VALUES
    (1, 10000, 'Savings'),
    (1, 5000, 'Cash'),
    (2, 5000, 'Travel money'),
    (2, 7000, 'Main account'),
    (3, 1000, 'Savings'),
    (4, 5000, 'Card')
;
