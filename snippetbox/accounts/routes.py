from flask import render_template, request, redirect, url_for, flash, session

from snippetbox.accounts import blueprint, forms
from snippetbox.accounts.models import AccountModel, InvalidCredentialsError
from snippetbox.utils.forms import Field
from snippetbox.utils import db


@blueprint.get("/create")
def create():
    form = forms.AccountCreateForm()
    return render_template("accounts/create.jinja", form=form)


@blueprint.post("/create")
def create_submit():
    email = request.form["email"]
    password = request.form["password"]

    form = forms.AccountCreateForm(email=email, password=password)
    accounts = AccountModel(db.get_connection())

    form.check_field(
        Field.not_blank(form.email), "email", "This field cannot be blank"
    )
    form.check_field(
        Field.is_valid_email(form.email), "email", "This is not a valid email"
    )
    form.check_field(
        not accounts.email_exists(form.email),
        "email",
        "This email already exists",
    )
    form.check_field(
        Field.not_blank(form.password), "password", "This field cannot be blank"
    )
    form.check_field(
        Field.min_chars(form.password, 8),
        "password",
        "This field cannot be less than 8 characters long",
    )

    if not form.is_valid:
        return render_template("accounts/create.jinja", form=form), 422

    accounts = AccountModel(db.get_connection())
    accounts.insert(form.email, form.password)

    flash("Account successfully created!")

    return redirect(url_for("accounts.login"))


@blueprint.get("/login")
def login():
    form = forms.LoginForm()
    return render_template("accounts/login.jinja", form=form)


@blueprint.post("/login")
def login_submit():
    email = request.form["email"]
    password = request.form["password"]

    form = forms.LoginForm(email, password)
    accounts = AccountModel(db.get_connection())

    try:
        account = accounts.authenticate(form.email, form.password)
    except InvalidCredentialsError:
        form.add_non_field_error("Email or password is incorrect")
        return render_template("accounts/login.jinja", form=form)

    # When a user successfully logs in, we store their account's
    # id in their session. To know if a request is coming from an
    # authenticated user, we only need to check if their session
    # contains an id.
    session["account_id"] = account.id
    flash("You've successfully logged in!")
    return redirect(url_for("home"))


@blueprint.get("/logout")
def logout():
    # To log out means to remove the user's account id from its session.
    session.pop("account_id", None)
    flash("You've successfully logged out!")
    return redirect(url_for("home"))
