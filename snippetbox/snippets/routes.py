from flask import redirect, render_template, url_for, request, flash

from snippetbox.snippets import blueprint, forms
from snippetbox.snippets.models import SnippetModel
from snippetbox.utils import db
from snippetbox.utils.forms import Field


@blueprint.get("/")
def index():
    snippets = SnippetModel(db.get_connection())
    return render_template("/snippets/index.jinja", snippets=snippets.latest())


@blueprint.get("/create")
def create():
    form = forms.SnippetCreateForm()
    return render_template("/snippets/create.jinja", form=form)


@blueprint.post("/create")
def create_submit():
    title = request.form["title"]
    content = request.form["content"]
    valid_days = int(request.form["valid_days"])

    form = forms.SnippetCreateForm(title, content, valid_days)

    form.check_field(
        Field.not_blank(form.title), "title", "This field cannot be blank"
    )
    form.check_field(
        Field.max_chars(form.title, 100),
        "title",
        "This field cannot be more than 100 characters long",
    )
    form.check_field(
        Field.not_blank(form.content),
        "content",
        "This field cannot be blank",
    )
    form.check_field(
        Field.permitted_value(form.valid_days, [1, 7, 365]),
        "expires",
        "This field must equal 1, 7 or 365",
    )

    if not form.is_valid:
        return render_template("snippets/create.jinja", form=form), 422

    snippets = SnippetModel(db.get_connection())
    snippets.insert(form.title, form.content, form.valid_days)

    # A nice touch to improve our user experience is to display a
    # one-time confirmation message which the user sees after they've
    # added a new snippet. A confirmation message like this should only
    # show up for the user once (immediately after creating the snippet)
    # and no other users should ever see the message. This type of
    # message is known as a "flash message" or a "toast".
    #
    # To make this work, we need to start sharing data (or state)
    # between HTTP requests for the same user. The most common way to do
    # that is to implement a *session* for the user.
    #
    # Flask provides the "flash" function to store a message in a user's
    # session, and the "get_flashed_messages" function to get hold of
    # the message in templates.
    flash("Snippet successfully created!")

    return redirect(url_for("home"))
