from flask import Blueprint

blueprint = Blueprint("snippets", __name__, url_prefix="/snippets")

from snippetbox.snippets import routes
