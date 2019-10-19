import datetime
import os
from functools import partial

import click
from flask import Flask, current_app, Response
from flask.cli import with_appcontext
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, MethodNotAllowed

from api import blueprints
from api.blueprints import create_user
from api.config import ProdConfig, TestConfig, DevConfig, config
from api.exceptions import (
    validation_error_handler,
    AuthenticationException,
    authn_exception_handler,
    AuthorizationException,
    authz_exception_handler,
    UserExistsException,
    RoleExistsException,
    role_exists_exception_handler,
    user_exists_exception_handler,
)
from api.extensions import db, migrate
from api.models import User
from api.service import add_user, add_role


def create_app(config_obj=config()):
    """Create the Flask app with the specified configuration.

    This function initialises the flask app, associated database connection, migration functionality, blueprints
    (routes), error handlers and ensures the database contains the expected initialisation data.

    :param config_obj `Config` object to configure the app with. By default it is what is returned by `config()`.
    :return Configured flask application
    """
    app = Flask(__name__)
    app.response_class.default_mimetype = "application/json"

    # Config
    app.config.from_object(config_obj)

    # Database
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    app.register_blueprint(blueprints.user_blueprint)
    app.register_blueprint(blueprints.auth_blueprint)

    # Error handlers
    app.errorhandler(ValidationError)(partial(validation_error_handler, app))
    app.errorhandler(AuthenticationException)(partial(authn_exception_handler, app))
    app.errorhandler(AuthorizationException)(partial(authz_exception_handler, app))
    app.errorhandler(UserExistsException)(partial(user_exists_exception_handler, app))
    app.errorhandler(RoleExistsException)(partial(role_exists_exception_handler, app))

    # Initialisation
    app.before_first_request(initial_data(app))
    return app


def initial_data(app):
    """Ensure the initial data is in the database."""

    def init():
        app.logger.info("Ensuring admin role exists")
        try:
            add_role(name="admin")
            app.logger.info("Created admin role?")
        except RoleExistsException:
            app.logger.info("Admin role already exists")
        except Exception as err:
            app.logger.error(f"Error when creating admin role: {str(err)}")
            raise err

        app.logger.info("Ensuring admin user exists")
        try:
            add_user(
                first_name="Admin",
                last_name="",
                email=app.config["ADMIN_EMAIL"],
                password=app.config["ADMIN_PASSWORD"],
                role_names=["admin"],
            )
            app.logger.info("Created admin user")
        except UserExistsException:
            app.logger.info("Admin user already exists")
        except Exception as err:
            app.logger.error(f"Error when creating admin user: {str(err)}")
            raise err

    return init
