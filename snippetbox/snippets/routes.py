from flask import redirect, render_template, url_for, request, flash, session

from snippetbox.snippets import blueprint, forms
from snippetbox.snippets.models import SnippetModel
from snippetbox.utils import db
from snippetbox.utils.forms import Field


@blueprint.get("/")
def index():
    account_snippets = []
    # We now show only snippets created by the user who is currently
    # logged in.
    account_id = session.get("account_id")
    if account_id is not None:
        snippets = SnippetModel(db.get_connection())
        account_snippets = snippets.account_snippets(account_id)
    return render_template("/snippets/index.jinja", snippets=account_snippets)


@blueprint.get("/create")
def create():
    # Users who are not logged in (i.e., whose session does not include
    # their account id), should not be able to create a snippet.
    if session.get("account_id") is None:
        return redirect(url_for("accounts.login"))

    form = forms.SnippetCreateForm()
    return render_template("/snippets/create.jinja", form=form)


@blueprint.post("/create")
def create_submit():
    account_id = session.get("account_id")
    if account_id is None:
        return redirect(url_for("accounts.login"))

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
    snippets.insert(form.title, form.content, form.valid_days, int(account_id))

    flash("Snippet successfully created!")

    return redirect(url_for("home"))
