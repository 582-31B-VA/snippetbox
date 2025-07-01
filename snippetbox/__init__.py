from flask import Flask

from snippetbox import snippets, cli
from snippetbox.utils import db

from config import Config


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Applications need some kind of configuration. There are different
    # settings you might want to change depending on the application
    # environment like toggling the debug mode, setting the secret key,
    # and other such environment-specific things.
    #
    # The "config" attribute of the Flask object is where we store these
    # configuration values. The "from_object" method allows to set these
    # values these values from a given object.
    app.config.from_object(Config)

    # Like routes, commands need to be registered with our app.
    app.cli.add_command(cli.init)

    app.register_blueprint(snippets.blueprint)
    app.add_url_rule("/", endpoint="home", view_func=snippets.routes.index)

    # This tells Flask to call the "close_connection" function when
    # cleaning up after returning the response. That way, we don't have
    # to do it manually.
    app.teardown_appcontext(db.close_connection)

    return app
