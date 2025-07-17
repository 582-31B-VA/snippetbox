from flask import Blueprint

blueprint = Blueprint("accounts", __name__, url_prefix="/accounts")

from snippetbox.accounts import routes
