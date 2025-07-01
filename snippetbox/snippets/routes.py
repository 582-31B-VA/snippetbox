from flask import redirect, render_template, url_for

from snippetbox.snippets import blueprint
from snippetbox.snippets.models import SnippetModel
from snippetbox.utils import db


@blueprint.get("/")
def index():
    # We are now fetching the latest snippets from the database.
    snippets = SnippetModel(db.get_connection())
    return render_template("/snippets/index.jinja", snippets=snippets.latest())


# This creates some dummy data and inserts a snippet in our database.
@blueprint.post("/create")
def create():
    title = "O snail"
    content = "O snail\nClimb Mount Fuji,\nBut slowly, slowly!"
    valid_days = 7
    snippets = SnippetModel(db.get_connection())
    snippets.insert(title, content, valid_days)
    return redirect(url_for("home"))
