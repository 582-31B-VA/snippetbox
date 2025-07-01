from flask import Blueprint

# A blueprint is a way to organize a group of related views and other
# code. Rather than registering views and other code directly with an
# application, they are registered with a blueprint. Then the blueprint
# is registered with the application when it is available in the factory
# function.
#
# To create a blueprint, we use the "Blueprint" class. It takes the name
# of the blueprint and the name of the base module. We also set a URL
# prefix that all routes will inherit.

blueprint = Blueprint("snippets", __name__, url_prefix="/snippets")

# We import the routes module so that the routes are registered
# with the blueprint. This import is at the bottom to avoid circular
# dependencies.

from snippetbox.snippets import routes
