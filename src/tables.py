from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean, DateTime, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp()),
    Column("name", String(100), nullable=False),
    Column("email", String(100), nullable=False),
    Column("password", String(100), nullable=False),
    Column("enabled", Boolean, nullable=False, default=text("true"), server_default=text("true")),
    Column("is_admin", Boolean, nullable=False, default=text("false"), server_default=text("false")),
)

wallets = Table(
    "wallets",
    metadata,
    Column("id", UUID(), primary_key=True, nullable=False, server_default=func.uuid_generate_v1()),
    Column("created_at", DateTime, nullable=False, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp()),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("balance", Integer, nullable=False, default=text("0"), server_default=text("0")),
    Column("name", String(100)),
    Column("enabled", Boolean, nullable=False, default=text("true"), server_default=text("true")),
)

ledger = Table(
    "transactions",
    metadata,
    Column("id", UUID(), primary_key=True, nullable=False, server_default=func.uuid_generate_v1()),
    Column("created_at", DateTime, nullable=False, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp()),
    Column("account_from", UUID(), ForeignKey("wallets.id"), nullable=False),
    Column("account_to", UUID(), ForeignKey("wallets.id"), nullable=False),
    Column("amount", Integer, nullable=False, default=text("0"), server_default=text("0")),
    Column("label", String(100)),
)


