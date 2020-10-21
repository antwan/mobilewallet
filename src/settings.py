
from starlette.config import Config
import databases

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
SECRET = config("SECRET", cast=str)
TESTING = config("TESTING", cast=bool, default=False)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=databases.DatabaseURL,
    default="postgresql://admin:admin@db:5432/mobilewallet",
)
if DATABASE_URL.dialect == "postgres":
    DATABASE_URL = DATABASE_URL.replace(dialect="postgresql")  # pragma: nocover

TEST_DATABASE_URL = DATABASE_URL.replace(database="test_" + DATABASE_URL.database)
