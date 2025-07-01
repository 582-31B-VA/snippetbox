from flask import Flask

from snippetbox import snippets

# The most straightforward way to create a Flask application is to
# create a global "Flask" instance directly at the top of your code,
# like we did previously. While this is simple, it can make cause some
# tricky issues as the project grows.
#
# Instead of creating a Flask instance globally, we create it inside a
# function known as the "application factory". Any setup the application
# needs will happen inside the function, then the application will be
# returned.


def create_app():
    app = Flask(__name__)
    app.register_blueprint(snippets.blueprint)

    # The "add_url_rule" function maps the "/" URL to the "index" view
    # function in the "snippets.routes" module. This is necessary because
    # we want to keep the snippets logic in the "snippets" package.

    app.add_url_rule("/", endpoint="home", view_func=snippets.routes.index)

    return app
