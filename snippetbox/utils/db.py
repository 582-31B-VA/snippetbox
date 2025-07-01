from sqlite3 import Connection, connect

from flask import current_app, g


# The term "model" comes from an architecture pattern called
# "Model-View-Controller" ("MVC" for short). A model's sole
# responsability is to manage data. It bridges the gap between
# our Python program and our database. See "snippets/models.py"
# for an example of a model.
class Model:
    def __init__(self, db: Connection):
        self.db = db


# Helper functions for managaing database connections.
# See: https://flask.palletsprojects.com/en/stable/tutorial/database/


def get_connection() -> Connection:
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = connect(current_app.config["DATABASE_PATH"])
    return g.db


def close_connection(_e: BaseException | None = None) -> None:
    """Close the connection if the request is connected to the database."""
    db = g.pop("db", None)
    if db is not None:
        db.close()
