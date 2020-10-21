from . import settings
import databases

if settings.TESTING:
    database = databases.Database(settings.TEST_DATABASE_URL, force_rollback=True)
else:  # pragma: nocover
    database = databases.Database(settings.DATABASE_URL)


def url_for(*args, **kwargs):
    from .app import app

    return app.url_path_for(*args, **kwargs)
