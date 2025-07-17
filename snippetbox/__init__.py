from flask import Flask

from snippetbox import snippets, cli, accounts
from snippetbox.utils import db

from config import Config


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    app.cli.add_command(cli.init)

    app.register_blueprint(snippets.blueprint)
    app.register_blueprint(accounts.blueprint)

    app.add_url_rule("/", endpoint="home", view_func=snippets.routes.index)

    app.teardown_appcontext(db.close_connection)

    return app
