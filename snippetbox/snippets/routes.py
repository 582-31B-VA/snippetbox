from flask import redirect, render_template, url_for, request

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
    # We use "[]" and not "get" to retrieve the form date so that Flask
    # can return an error to the client if the form doesn't have the
    # required fields.
    title = request.form["title"]
    content = request.form["content"]
    valid_days = int(request.form["valid_days"])

    # We store the values received from the client into the form object.
    # This will allow us to validate each field (see below) and to
    # repopulate the form if there are errors.
    form = forms.SnippetCreateForm(title, content, valid_days)

    # See the Form definition in "snippetbox/utils/forms.py".
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
        # The form object contains the errors because we used
        # "check_field" to validate the form. If there are errors, the
        # template will be able to show them.
        return render_template("snippets/create.jinja", form=form), 422

    snippets = SnippetModel(db.get_connection())
    snippets.insert(form.title, form.content, form.valid_days)

    return redirect(url_for("home"))
