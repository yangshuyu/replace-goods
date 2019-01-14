import flask_restful
from flask import (Flask, jsonify, request, current_app, abort)
# from flask_jwt_extended import JWTManager
# from flask_security import SQLAlchemySessionUserDatastore
from flask_cors import CORS
#
# import api.models
# from api.libs.interface_tips import InterfaceTips
# from api.libs.error import error
from api.config import load_config
# # from extensions import (db, migrate, redis_store, security, celery, mail, es, cache, sentry)
from api.resources import BLUEPRINTS
# from api.libs.utils import generate_signature_v1, generate_salt
# from api.services.redis import redis_client
# from api.services.suuid import SUUIDConverter

from api.extensions import (db, migrate, redis_store, mail, cache)


def create_app(app_name='api', blueprints=None):
    app = Flask(app_name)
    config = load_config()
    app.config.from_object(config)

    if blueprints is None:
        blueprints = BLUEPRINTS
    blueprints_resister(app, blueprints)
    extensions_load(app)

    return app


def blueprints_resister(app, blueprints):
    for bp in blueprints:
        app.register_blueprint(bp)


def extensions_load(app):
    db.init_app(app)
    migrate.init_app(app, db)
    redis_store.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    CORS(app, resources={r"*": {"origins": "*", "expose_headers": "X-Total"}})
