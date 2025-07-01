import os

import click
from flask import current_app

from snippetbox.utils.db import get_connection


# "click" allows us to execute functions from the command line.
# This "init" function, for instance, can be executed with the command
# "uv run flask --app snippetbox init".
@click.command
def init() -> None:
    """Initialize the app (create database, etc.)"""

    # Make sure the "instance" folder and the database file exist.
    # Create them if they don't.
    os.makedirs(current_app.instance_path, exist_ok=True)
    open(current_app.config["DATABASE_PATH"], "a").close()

    # Apply the schema to the database.
    with current_app.open_resource("schema.sql") as file:
        schema = file.read().decode("utf8")
        db = get_connection()
        db.executescript(schema)
