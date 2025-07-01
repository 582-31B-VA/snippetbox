from flask import render_template

from snippetbox.snippets import blueprint

# This is where we will define view functions for the "snippets"
# blueprint.
#
# Because of the blueprint's URL prefix, the URL for all these routes
# will start with "/snippets". For instance, the URL for this route is
# actually "/snippets/".


@blueprint.get("/")
def index():
    return render_template("/snippets/index.jinja")
