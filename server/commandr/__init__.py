# Code for this file taken and adapted from:
# http://flask.pocoo.org/docs/1.0/tutorial/factory/

import os

from flask import Flask


# Create the app and add configurations
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'commandr.sqlite'),
)

# Check that the instance folder (used for the database) exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Import and register blueprints
from . import db
db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

from . import dashboard
app.register_blueprint(dashboard.bp)
app.add_url_rule('/', endpoint='index')

from .util import api
app.register_blueprint(api.bp)

